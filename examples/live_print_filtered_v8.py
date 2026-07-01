import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

from mythic_edge_parser import MtgaEventStream
from mythic_edge_parser.app.config import DEFAULT_MTGA_PLAYER_LOG

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOG_PATH = Path(
    os.environ.get(
        "MTGA_PLAYER_LOG",
        str(DEFAULT_MTGA_PLAYER_LOG),
    )
)

PROJECT_ROOT = Path(
    os.environ.get(
        "MYTHICEDGE_PROJECT_ROOT",
        str(DEFAULT_PROJECT_ROOT),
    )
)
MATCH_LOGS_ROOT = Path(os.environ.get("MYTHICEDGE_MATCH_LOGS_ROOT", str(PROJECT_ROOT / "data" / "match_logs")))
OUT_FILENAME_PREFIX = os.environ.get("MYTHICEDGE_OUT_PREFIX", "mtga_filtered_events_v7")
WEBHOOK_URL = os.environ.get("MYTHICEDGE_SHEETS_WEBHOOK", "")
LOCAL_PLAYER_INDEX = int(os.environ.get("MYTHICEDGE_LOCAL_PLAYER_INDEX", "0"))
POST_GAMESTATE_ROWS = os.environ.get("MYTHICEDGE_POST_GAMESTATE", "0").strip().lower() in {
    "1",
    "true",
    "yes",
    "y",
}

# Keep a richer local log than the spreadsheet feed.
KEEP_EVENT_LIFECYCLE_TYPES = {
    "event_join",
    "event_enter_pairing",
    "event_claim_prize",
}

# Keep only client actions that are currently useful for Sheets.
KEEP_CLIENT_ACTION_TYPES = {
    "mulligan_resp",
    "submit_deck_resp",
}

KEEP_GENERIC_CLIENT_MESSAGE_TYPES = {
    "ClientMessageType_ChooseStartingPlayerResp",
    "ClientMessageType_EnterSideboardingReq",
    "ClientMessageType_SubmitDeckResp",
    "ClientMessageType_MulliganResp",
}

# De-dup state: only emit a local turn marker when the actual turn tuple changes.
_LOCAL_TURN_KEYS: set[tuple[Any, ...]] = set()

# Runtime context so result and client-action rows stay attached to a match/game.
_CONTEXT: dict[str, Any] = {
    "current_match_id": "",
    "current_game_number": "",
    "current_player_team": "",
}

# Track cumulative mulligans per (match_id, game_number).
_MULLIGAN_COUNTS: dict[tuple[str, Any], int] = {}

# Track open local log file by event date.
_CURRENT_LOG_DATE: str = ""
_CURRENT_LOG_PATH: Path | None = None

# Keep the sheet feed lean and de-duplicated.
_SHEETS_TURN_KEYS: set[tuple[Any, ...]] = set()
_POSTED_SUBMIT_DECK_KEYS: set[tuple[Any, ...]] = set()
_POSTED_SIDEBOARD_KEYS: set[tuple[Any, ...]] = set()
_LAST_POSTED_RANK: str = ""
_GAME_ROWS_POSTED: set[tuple[Any, Any]] = set()
_MATCH_ROWS_POSTED: set[Any] = set()


def _safe_local_player(players: list[dict[str, Any]]) -> dict[str, Any]:
    if not players:
        return {}
    if 0 <= LOCAL_PLAYER_INDEX < len(players):
        return players[LOCAL_PLAYER_INDEX] or {}
    return players[0] or {}


def _extract_turn_info(payload: dict[str, Any]) -> tuple[Any, Any, Any, Any, Any, Any, Any]:
    """Work around parser limitations by pulling directly from raw_game_state when needed."""
    raw = payload.get("raw_game_state") or {}
    gsm = raw.get("gameStateMessage") if isinstance(raw, dict) else None
    turn_info = gsm.get("turnInfo") if isinstance(gsm, dict) else None
    game_info = gsm.get("gameInfo") if isinstance(gsm, dict) else None

    top_game_info = payload.get("game_info") or {}

    match_id = (
        (game_info or {}).get("matchID")
        or top_game_info.get("matchID")
        or ((raw.get("queuedGameStateMessage") or {}).get("gameStateMessage") or {}).get("gameInfo", {}).get("matchID")
    )
    game_number = (game_info or {}).get("gameNumber") or top_game_info.get("gameNumber")
    turn_number = (turn_info or {}).get("turnNumber") or payload.get("turn_number")
    active_player = (turn_info or {}).get("activePlayer") or payload.get("active_player_seat_id")
    phase = (turn_info or {}).get("phase")
    step = (turn_info or {}).get("step")
    stage = (
        (game_info or {}).get("stage")
        or top_game_info.get("stage")
        or payload.get("stage")
    )
    return match_id, game_number, turn_number, active_player, phase, step, stage


def _extract_starting_player_from_client_action(payload: dict[str, Any]) -> Any:
    """Best-effort extraction across plausible parser payload shapes."""
    for key in (
        "starting_player_system_seat_id",
        "startingPlayerSystemSeatId",
        "chosen_system_seat_id",
        "chosenSystemSeatId",
        "system_seat_id",
        "systemSeatId",
        "seat_id",
        "seatId",
        "selected_system_seat_id",
        "selectedSystemSeatId",
    ):
        if payload.get(key) not in (None, ""):
            return payload.get(key)
    return None


def _context_key(match_id: Any, game_number: Any) -> tuple[Any, Any]:
    return (match_id or _CONTEXT["current_match_id"], game_number or _CONTEXT["current_game_number"])


def _update_context(event: Any) -> None:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind == "MatchState":
        match_id = payload.get("match_id") or _CONTEXT["current_match_id"]
        if match_id:
            _CONTEXT["current_match_id"] = match_id

        players = payload.get("players") or []
        local_player = _safe_local_player(players)
        player_team = local_player.get("team_id") or _CONTEXT["current_player_team"]
        if player_team != "":
            _CONTEXT["current_player_team"] = player_team

        if payload.get("type") == "match_started":
            _CONTEXT["current_game_number"] = 1

    elif kind == "GameState":
        match_id, game_number, _, _, _, _, _ = _extract_turn_info(payload)
        if match_id:
            _CONTEXT["current_match_id"] = match_id
        if game_number not in (None, ""):
            _CONTEXT["current_game_number"] = game_number


def _infer_scope_label(scope_value: Any) -> str:
    text = str(scope_value or "")
    if "MatchScope_Game" in text or text == "Game":
        return "Game"
    if "MatchScope_Match" in text or text == "Match":
        return "Match"
    return text

def _extract_game_result_identity(payload: dict[str, Any]) -> tuple[Any, Any, Any, Any, Any]:
    game_info = payload.get("game_info") or {}
    match_id = game_info.get("matchID") or _CONTEXT["current_match_id"]
    game_number = game_info.get("gameNumber") or _CONTEXT["current_game_number"]
    winning_team = payload.get("winning_team_id", "")
    result_type = payload.get("result_type", "")
    reason = payload.get("reason", "")
    return match_id, game_number, winning_team, result_type, reason


def _next_mulligan_count(match_id: Any, game_number: Any, decision: Any) -> int:
    key = _context_key(match_id, game_number)
    if not key[0] or key[1] in (None, ""):
        return 0

    decision_text = str(decision or "")
    if "Mulligan" in decision_text:
        _MULLIGAN_COUNTS[key] = _MULLIGAN_COUNTS.get(key, 0) + 1
    else:
        _MULLIGAN_COUNTS.setdefault(key, 0)
    return _MULLIGAN_COUNTS[key]


def include_event(event: Any) -> bool:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    # Keep a few extra startup/queue events locally for debugging.
    if kind in {"DetailedLoggingStatus", "MatchState", "GameResult", "Rank"}:
        return True

    if kind == "EventLifecycle":
        return payload.get("type") in KEEP_EVENT_LIFECYCLE_TYPES

    if kind == "ClientAction":
        action_type = payload.get("type")
        if action_type in KEEP_CLIENT_ACTION_TYPES:
            return True
        return (
            action_type == "generic_client_action"
            and payload.get("message_type") in KEEP_GENERIC_CLIENT_MESSAGE_TYPES
        )

    if kind == "GameState":
        match_id, game_number, turn_number, active_player, phase, step, stage = _extract_turn_info(payload)

        # Keep game-over snapshots in local JSONL for debugging.
        if stage == "GameStage_GameOver":
            return True

        # Keep only real turn markers with usable data.
        if turn_number is None or active_player is None:
            return False

        key = (match_id, game_number, turn_number, active_player, phase, step)
        if key in _LOCAL_TURN_KEYS:
            return False
        _LOCAL_TURN_KEYS.add(key)
        return True

    return False


def to_serializable(event: Any) -> dict[str, Any]:
    metadata = getattr(event, "metadata", None)
    payload = getattr(event, "payload", {}) or {}

    row = {
        "kind": getattr(event, "kind", type(event).__name__),
        "timestamp": metadata.timestamp.isoformat() if metadata and metadata.timestamp else None,
        "raw_bytes_hash": getattr(metadata, "raw_bytes_hash", None),
        "payload": payload,
    }

    if row["kind"] == "GameState":
        match_id, game_number, turn_number, active_player, phase, step, stage = _extract_turn_info(payload)
        row["derived"] = {
            "match_id": match_id,
            "game_number": game_number,
            "turn_number": turn_number,
            "active_player_seat_id": active_player,
            "phase": phase,
            "step": step,
            "stage": stage,
        }

    return row


def summarize(event: Any) -> str:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind == "DetailedLoggingStatus":
        return f"DetailedLoggingStatus enabled={payload.get('enabled')}"

    if kind == "EventLifecycle":
        return f"EventLifecycle type={payload.get('type')}"

    if kind == "Rank":
        cc = payload.get("constructed_class")
        cl = payload.get("constructed_level")
        cp = payload.get("constructed_percentile")
        return f"Rank constructed={cc} {cl} percentile={cp}"

    if kind == "MatchState":
        players = payload.get("players") or []
        opponent = ""
        if len(players) >= 2:
            opponent = players[1].get("player_name", "")
        return (
            f"MatchState type={payload.get('type')} state={payload.get('state_type')} "
            f"match_id={payload.get('match_id')} opponent={opponent}"
        )

    if kind == "GameState":
        match_id, game_number, turn_number, active_player, phase, step, stage = _extract_turn_info(payload)
        return (
            f"GameState match={match_id} game={game_number} stage={stage} "
            f"turn={turn_number} active_player_seat_id={active_player} phase={phase} step={step}"
        )

    if kind == "GameResult":
        match_id, game_number, winning_team, result_type, reason = _extract_game_result_identity(payload)
        rows: list[dict[str, Any]] = []

        # Post exactly one current-game row per (match_id, game_number).
        game_key = (match_id, game_number)
        if match_id and game_number not in (None, "") and game_key not in _GAME_ROWS_POSTED:
            _GAME_ROWS_POSTED.add(game_key)
            game_row = dict(base)
            game_row["scope"] = "Game"
            game_row["match_id"] = match_id
            game_row["game_number"] = game_number
            game_row["winner_team"] = winning_team
            game_row["result_type"] = result_type
            game_row["result_reason"] = reason
            rows.append(game_row)

        # If the payload includes a match-scope result, post exactly one match row.
        match_result = None
        for result in (payload.get("results") or []):
            if _infer_scope_label(result.get("scope", "")) == "Match":
                match_result = result
                break

        if match_result and match_id and match_id not in _MATCH_ROWS_POSTED:
            _MATCH_ROWS_POSTED.add(match_id)
            match_row = dict(base)
            match_row["scope"] = "Match"
            match_row["match_id"] = match_id
            match_row["game_number"] = ""
            match_row["winner_team"] = match_result.get("winningTeamId", winning_team)
            match_row["result_type"] = match_result.get("result", result_type)
            match_row["result_reason"] = match_result.get("reason", reason)
            rows.append(match_row)

        return rows

    if kind == "GameState":
        match_id, game_number, turn_number, active_player, phase, step, stage = _extract_turn_info(payload)

        # Keep game-over snapshots in local JSONL for debugging.
        if stage == "GameStage_GameOver":
            return True

        # Keep only real turn markers with usable data.
        if turn_number is None or active_player is None:
            return False

        key = (match_id, game_number, turn_number, active_player, phase, step)
        if key in _LOCAL_TURN_KEYS:
            return False
        _LOCAL_TURN_KEYS.add(key)
        return True

    return False


def to_serializable(event: Any) -> dict[str, Any]:
    metadata = getattr(event, "metadata", None)
    payload = getattr(event, "payload", {}) or {}

    row = {
        "kind": getattr(event, "kind", type(event).__name__),
        "timestamp": metadata.timestamp.isoformat() if metadata and metadata.timestamp else None,
        "raw_bytes_hash": getattr(metadata, "raw_bytes_hash", None),
        "payload": payload,
    }

    if row["kind"] == "GameState":
        match_id, game_number, turn_number, active_player, phase, step, stage = _extract_turn_info(payload)
        row["derived"] = {
            "match_id": match_id,
            "game_number": game_number,
            "turn_number": turn_number,
            "active_player_seat_id": active_player,
            "phase": phase,
            "step": step,
            "stage": stage,
        }

    return row


def summarize(event: Any) -> str:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind == "DetailedLoggingStatus":
        return f"DetailedLoggingStatus enabled={payload.get('enabled')}"

    if kind == "EventLifecycle":
        return f"EventLifecycle type={payload.get('type')}"

    if kind == "Rank":
        cc = payload.get("constructed_class")
        cl = payload.get("constructed_level")
        cp = payload.get("constructed_percentile")
        return f"Rank constructed={cc} {cl} percentile={cp}"

    if kind == "MatchState":
        players = payload.get("players") or []
        opponent = ""
        if len(players) >= 2:
            opponent = players[1].get("player_name", "")
        return (
            f"MatchState type={payload.get('type')} state={payload.get('state_type')} "
            f"match_id={payload.get('match_id')} opponent={opponent}"
        )

    if kind == "GameState":
        match_id, game_number, turn_number, active_player, phase, step, stage = _extract_turn_info(payload)
        return (
            f"GameState match={match_id} game={game_number} stage={stage} "
            f"turn={turn_number} active_player_seat_id={active_player} phase={phase} step={step}"
        )

    if kind == "GameResult":
        return (
            f"GameResult winner_team={payload.get('winning_team_id')} "
            f"result={payload.get('result_type')} reason={payload.get('reason')}"
        )

    if kind == "ClientAction":
        action_type = payload.get("type")
        if action_type == "mulligan_resp":
            return f"ClientAction mulligan decision={payload.get('decision')} request_id={payload.get('request_id')}"
        if action_type == "submit_deck_resp":
            return (
                f"ClientAction submit_deck main_count={len(payload.get('deck_cards') or [])} "
                f"side_count={len(payload.get('sideboard_cards') or [])}"
            )
        return f"ClientAction message_type={payload.get('message_type')}"

    return f"{kind} {payload}"


def _base_sheet_row(event: Any) -> dict[str, Any]:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}
    metadata = getattr(event, "metadata", None)

    timestamp = metadata.timestamp.isoformat() if metadata and metadata.timestamp else ""

    return {
        "timestamp": timestamp,
        "event_family": kind,
        "event_type": payload.get("type", ""),
        "scope": "",
        "match_id": _CONTEXT["current_match_id"],
        "game_number": _CONTEXT["current_game_number"],
        "turn_number": "",
        "active_player": "",
        "player_team": _CONTEXT["current_player_team"],
        "winner_team": "",
        "result_type": "",
        "result_reason": "",
        "mulligan_count": "",
        "submit_deck_seen": False,
        "sideboarding_entered": False,
        "constructed_rank": "",
        "raw_json": json.dumps(to_serializable(event), ensure_ascii=False),
    }


def to_sheet_rows(event: Any) -> list[dict[str, Any]]:
    global _LAST_POSTED_RANK

    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}
    base = _base_sheet_row(event)

    if kind == "MatchState":
        event_type = payload.get("type", "")
        if event_type not in {"match_started", "match_completed"}:
            return []
        base["scope"] = "Match"
        base["event_type"] = event_type
        base["match_id"] = payload.get("match_id") or _CONTEXT["current_match_id"]
        players = payload.get("players") or []
        local_player = _safe_local_player(players)
        base["player_team"] = local_player.get("team_id", _CONTEXT["current_player_team"])
        if payload.get("winning_team_id") not in (None, ""):
            base["winner_team"] = payload.get("winning_team_id")
        return [base]

    if kind == "GameResult":
        results = payload.get("results") or []
        if not results:
            base["scope"] = "Game"
            base["winner_team"] = payload.get("winning_team_id", "")
            base["result_type"] = payload.get("result_type", "")
            base["result_reason"] = payload.get("reason", "")
            return [base]

        rows: list[dict[str, Any]] = []
        for result in results:
            row = dict(base)
            row["scope"] = _infer_scope_label(result.get("scope", "")) or "Game"
            if row["scope"] == "Match":
                row["game_number"] = ""
            row["winner_team"] = result.get("winningTeamId", payload.get("winning_team_id", ""))
            row["result_type"] = result.get("result", payload.get("result_type", ""))
            row["result_reason"] = result.get("reason", payload.get("reason", ""))
            rows.append(row)
        return rows

    if kind == "GameState":
        match_id, game_number, turn_number, active_player, _, _, stage = _extract_turn_info(payload)
        if stage == "GameStage_GameOver":
            return []
        if not POST_GAMESTATE_ROWS:
            # Keep only the minimum needed for play/draw inference on later games.
            if turn_number != 1 or active_player in (None, ""):
                return []
        key = (match_id or _CONTEXT["current_match_id"], game_number or _CONTEXT["current_game_number"], turn_number or 1)
        if key in _SHEETS_TURN_KEYS:
            return []
        _SHEETS_TURN_KEYS.add(key)

        base["scope"] = "Turn"
        base["match_id"] = match_id or _CONTEXT["current_match_id"]
        base["game_number"] = game_number or _CONTEXT["current_game_number"]
        base["turn_number"] = turn_number or 1
        base["active_player"] = active_player or ""
        return [base]

    if kind == "ClientAction":
        action_type = payload.get("type", "")

        # Promote ChooseStartingPlayer to a Turn row so helper formulas can infer play/draw
        # without needing a flood of GameState rows.
        if action_type == "generic_client_action" and payload.get("message_type") == "ClientMessageType_ChooseStartingPlayerResp":
            chosen_seat = _extract_starting_player_from_client_action(payload)
            if chosen_seat in (None, ""):
                return []
            key = (_CONTEXT["current_match_id"], _CONTEXT["current_game_number"], 1)
            if key in _SHEETS_TURN_KEYS:
                return []
            _SHEETS_TURN_KEYS.add(key)

            base["scope"] = "Turn"
            base["event_type"] = payload.get("message_type")
            base["turn_number"] = 1
            base["active_player"] = chosen_seat
            return [base]

        base["scope"] = "ClientAction"
        base["event_type"] = action_type

        if action_type == "mulligan_resp":
            base["mulligan_count"] = _next_mulligan_count(
                base["match_id"],
                base["game_number"],
                payload.get("decision"),
            )
            return [base]

        if action_type == "submit_deck_resp":
            key = _context_key(base["match_id"], base["game_number"])
            if key in _POSTED_SUBMIT_DECK_KEYS:
                return []
            _POSTED_SUBMIT_DECK_KEYS.add(key)
            base["submit_deck_seen"] = True
            return [base]

        if action_type == "generic_client_action":
            msg_type = payload.get("message_type", "")
            base["event_type"] = msg_type

            if msg_type == "ClientMessageType_EnterSideboardingReq":
                key = _context_key(base["match_id"], base["game_number"])
                if key in _POSTED_SIDEBOARD_KEYS:
                    return []
                _POSTED_SIDEBOARD_KEYS.add(key)
                base["sideboarding_entered"] = True
                return [base]

            if msg_type == "ClientMessageType_SubmitDeckResp":
                key = _context_key(base["match_id"], base["game_number"])
                if key in _POSTED_SUBMIT_DECK_KEYS:
                    return []
                _POSTED_SUBMIT_DECK_KEYS.add(key)
                base["submit_deck_seen"] = True
                return [base]

            if msg_type == "ClientMessageType_MulliganResp":
                base["mulligan_count"] = _next_mulligan_count(
                    base["match_id"],
                    base["game_number"],
                    payload.get("decision") or msg_type,
                )
                return [base]

            return []

        return []

    if kind == "Rank":
        cc = payload.get("constructed_class", "")
        cl = payload.get("constructed_level", "")
        rank_text = f"{cc} {cl}".strip()
        if not rank_text or rank_text == _LAST_POSTED_RANK:
            return []
        _LAST_POSTED_RANK = rank_text
        base["scope"] = "Rank"
        base["constructed_rank"] = rank_text
        return [base]

    # Keep EventLifecycle and DetailedLoggingStatus local-only.
    return []


def post_row_to_google_sheets(row: dict[str, Any]) -> None:
    if not WEBHOOK_URL:
        print("POST skipped: WEBHOOK_URL not set")
        return

    try:
        response = requests.post(WEBHOOK_URL, json=row, timeout=10)
        response.raise_for_status()
        print(f"POST ok: {row.get('event_family')} | {row.get('event_type')} | {row.get('match_id')}")
    except Exception as exc:
        print(f"POST failed: {exc}")


def _event_datetime(event: Any) -> datetime:
    metadata = getattr(event, "metadata", None)
    timestamp = metadata.timestamp if metadata and getattr(metadata, "timestamp", None) else None
    if isinstance(timestamp, datetime):
        return timestamp
    return datetime.now()


def _daily_folder_name(event_dt: datetime) -> str:
    return event_dt.strftime("%m_%d_%y")


def _ensure_daily_log_path(event_dt: datetime) -> Path:
    global _CURRENT_LOG_DATE, _CURRENT_LOG_PATH

    folder_name = _daily_folder_name(event_dt)
    if _CURRENT_LOG_DATE == folder_name and _CURRENT_LOG_PATH is not None:
        return _CURRENT_LOG_PATH

    day_folder = MATCH_LOGS_ROOT / folder_name
    day_folder.mkdir(parents=True, exist_ok=True)

    file_name = f"{OUT_FILENAME_PREFIX}_{folder_name}.jsonl"
    _CURRENT_LOG_DATE = folder_name
    _CURRENT_LOG_PATH = day_folder / file_name
    return _CURRENT_LOG_PATH


async def main() -> None:
    MATCH_LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    stream, subscriber = await MtgaEventStream.start(LOG_PATH)
    print(f"Watching: {LOG_PATH}")
    print(f"Writing daily match logs under: {MATCH_LOGS_ROOT}")
    print(f"Posting full GameState rows to Sheets: {POST_GAMESTATE_ROWS}")
    print(f"Webhook URL: {WEBHOOK_URL if WEBHOOK_URL else '[NOT SET]'}")
    try:
        while True:
            event = await subscriber.recv()
            if event is None:
                break
            if not include_event(event):
                continue

            _update_context(event)
            local_row = to_serializable(event)

            event_dt = _event_datetime(event)
            out_path = _ensure_daily_log_path(event_dt)
            with out_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(local_row, ensure_ascii=False) + "\n")
                f.flush()

            for sheet_row in to_sheet_rows(event):
                post_row_to_google_sheets(sheet_row)

            print(f"[{_daily_folder_name(event_dt)}] {summarize(event)}")
    finally:
        await stream.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
