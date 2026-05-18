import json
from typing import Any

from . import state
from .config import (
    KEEP_CLIENT_ACTION_TYPES,
    KEEP_EVENT_LIFECYCLE_TYPES,
    KEEP_GENERIC_CLIENT_MESSAGE_TYPES,
    POST_GAMESTATE_ROWS,
)
from .extractors import (
    _extract_game_result_identity,
    _extract_instance_grp_lookup,
    _extract_local_private_hand_instance_ids,
    _extract_starting_player_from_client_action,
    _extract_turn_info,
    _has_match_scope_result,
    _hydrate_game_state_identity,
    _safe_local_player,
)


def _event_timestamp(event: Any) -> str:
    metadata = getattr(event, "metadata", None)
    if metadata is not None and getattr(metadata, "timestamp", None) is not None:
        return metadata.timestamp.isoformat()
    return ""


def _base_sheet_row(event: Any) -> dict[str, Any]:
    payload = getattr(event, "payload", {}) or {}
    return {
        "timestamp": _event_timestamp(event),
        "event_family": getattr(event, "kind", type(event).__name__),
        "event_type": payload.get("type", ""),
        "scope": "",
        "match_id": state._CONTEXT["current_match_id"],
        "game_number": state._CONTEXT["current_game_number"],
        "turn_number": "",
        "active_player": "",
        "player_team": state._CONTEXT["current_player_team"],
        "winner_team": "",
        "result_type": "",
        "result_reason": "",
        "mulligan_count": "",
        "submit_deck_seen": False,
        "sideboarding_entered": False,
        "constructed_rank": "",
        "raw_json": json.dumps(to_serializable(event), ensure_ascii=False),
    }


def _local_private_hand_snapshot_key(payload: dict[str, Any]) -> tuple[Any, ...] | None:
    match_id, game_number, turn_number, _, _, _, stage = _extract_turn_info(payload, state._CONTEXT)

    if stage == "GameStage_GameOver":
        return None
    if turn_number not in (None, 1):
        return None

    hand_instance_ids = _extract_local_private_hand_instance_ids(payload)
    if len(hand_instance_ids) < 4 or len(hand_instance_ids) > 7:
        return None

    instance_grp_lookup = _extract_instance_grp_lookup(payload)
    hand_grp_ids = tuple(instance_grp_lookup.get(instance_id) for instance_id in hand_instance_ids)
    return (
        match_id,
        game_number,
        tuple(hand_instance_ids),
        hand_grp_ids,
    )


def _include_client_action(payload: dict[str, Any]) -> bool:
    action_type = payload.get("type")
    if action_type in KEEP_CLIENT_ACTION_TYPES:
        return True
    return action_type == "generic_client_action" and payload.get("message_type") in KEEP_GENERIC_CLIENT_MESSAGE_TYPES


def _include_game_state(payload: dict[str, Any]) -> bool:
    match_id, game_number, turn_number, active_player, phase, step, stage = _extract_turn_info(
        payload,
        state._CONTEXT,
    )

    if stage == "GameStage_GameOver":
        return True

    hand_snapshot_key = _local_private_hand_snapshot_key(payload)
    if hand_snapshot_key is not None:
        if hand_snapshot_key in state._LOCAL_HAND_SNAPSHOT_KEYS:
            return False
        state._LOCAL_HAND_SNAPSHOT_KEYS.add(hand_snapshot_key)
        return True

    if turn_number is None or active_player is None:
        return False

    key = (match_id, game_number, turn_number, active_player, phase, step)
    if key in state._LOCAL_TURN_KEYS:
        return False

    state._LOCAL_TURN_KEYS.add(key)
    return True


def include_event(event: Any) -> bool:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind in {
        "DetailedLoggingStatus",
        "Inventory",
        "MatchState",
        "GameResult",
        "Rank",
        "MatchConnectionState",
        "TcpConnectionClose",
        "WebSocketClosed",
        "ConnectionError",
        "DeckCollection",
        "Truncation",
    }:
        return True

    if kind == "EventLifecycle":
        return payload.get("type") in KEEP_EVENT_LIFECYCLE_TYPES

    if kind == "ClientAction":
        return _include_client_action(payload)

    if kind == "GameState":
        return _include_game_state(payload)

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
        identity = _hydrate_game_state_identity(payload, state._CONTEXT)
        row["derived"] = {
            "match_id": identity["match_id"] or "",
            "game_number": identity["game_number"] if identity["game_number"] is not None else "",
            "turn_number": identity["turn_number"],
            "active_player_seat_id": identity["active_player_seat_id"],
            "phase": identity["phase"],
            "step": identity["step"],
            "stage": identity["stage"],
            "identity_source": identity["identity_source"],
            "identity_ready": bool(identity["match_id"] and identity["game_number"] is not None),
        }

    return row


def _match_state_rows(base: dict[str, Any], payload: dict[str, Any]) -> list[dict[str, Any]]:
    event_type = payload.get("type", "")
    if event_type not in {"match_started", "match_completed"}:
        return []

    row = dict(base)
    row["scope"] = "Match"
    row["event_type"] = event_type
    row["match_id"] = payload.get("match_id") or state._CONTEXT["current_match_id"]

    players = payload.get("players") or []
    local_player = _safe_local_player(players)
    row["player_team"] = local_player.get("team_id", state._CONTEXT["current_player_team"])

    if payload.get("winning_team_id") not in (None, ""):
        row["winner_team"] = payload.get("winning_team_id")

    return [row]


def _game_result_rows(base: dict[str, Any], payload: dict[str, Any]) -> list[dict[str, Any]]:
    match_id, game_number, winning_team, result_type, reason = _extract_game_result_identity(payload, state._CONTEXT)
    rows: list[dict[str, Any]] = []

    game_key = (match_id, game_number)
    if match_id and game_number not in (None, "") and game_key not in state._GAME_ROWS_POSTED:
        state._GAME_ROWS_POSTED.add(game_key)
        row = dict(base)
        row["scope"] = "Game"
        row["match_id"] = match_id
        row["game_number"] = game_number
        row["winner_team"] = winning_team
        row["result_type"] = result_type
        row["result_reason"] = reason
        rows.append(row)

    if match_id and match_id not in state._MATCH_ROWS_POSTED and (
        str(payload.get("match_state", "")) == "MatchState_MatchComplete" or _has_match_scope_result(payload)
    ):
        state._MATCH_ROWS_POSTED.add(match_id)
        row = dict(base)
        row["scope"] = "Match"
        row["match_id"] = match_id
        row["game_number"] = ""
        row["winner_team"] = winning_team
        row["result_type"] = result_type
        row["result_reason"] = reason
        rows.append(row)

    return rows


def _game_state_rows(base: dict[str, Any], payload: dict[str, Any]) -> list[dict[str, Any]]:
    match_id, game_number, turn_number, active_player, _, _, stage = _extract_turn_info(payload, state._CONTEXT)

    if stage == "GameStage_GameOver":
        return []

    if not POST_GAMESTATE_ROWS and (turn_number != 1 or active_player in (None, "")):
        return []

    key = (
        match_id or state._CONTEXT["current_match_id"],
        game_number or state._CONTEXT["current_game_number"],
        turn_number or 1,
    )
    if key in state._SHEETS_TURN_KEYS:
        return []

    state._SHEETS_TURN_KEYS.add(key)
    row = dict(base)
    row["scope"] = "Turn"
    row["match_id"] = match_id or state._CONTEXT["current_match_id"]
    row["game_number"] = game_number or state._CONTEXT["current_game_number"]
    row["turn_number"] = turn_number or 1
    row["active_player"] = active_player or ""
    return [row]


def _client_action_rows(base: dict[str, Any], payload: dict[str, Any]) -> list[dict[str, Any]]:
    action_type = payload.get("type", "")

    if (
        action_type == "generic_client_action"
        and payload.get("message_type") == "ClientMessageType_ChooseStartingPlayerResp"
    ):
        chosen_seat = _extract_starting_player_from_client_action(payload)
        if chosen_seat in (None, ""):
            return []

        key = (
            state._CONTEXT["current_match_id"],
            state._CONTEXT["current_game_number"],
            1,
        )
        if key in state._SHEETS_TURN_KEYS:
            return []

        state._SHEETS_TURN_KEYS.add(key)
        row = dict(base)
        row["scope"] = "Turn"
        row["event_type"] = payload.get("message_type")
        row["turn_number"] = 1
        row["active_player"] = chosen_seat
        return [row]

    row = dict(base)
    row["scope"] = "ClientAction"
    row["event_type"] = action_type

    if action_type == "mulligan_resp":
        row["mulligan_count"] = _reported_mulligan_count(
            row["match_id"],
            row["game_number"],
            payload.get("decision"),
        )
        return [row]

    if action_type == "submit_deck_resp":
        key = state._context_key(row["match_id"], row["game_number"])
        if key in state._POSTED_SUBMIT_DECK_KEYS:
            return []
        state._POSTED_SUBMIT_DECK_KEYS.add(key)
        row["submit_deck_seen"] = True
        return [row]

    if action_type != "generic_client_action":
        return []

    msg_type = payload.get("message_type", "")
    row["event_type"] = msg_type

    if msg_type == "ClientMessageType_EnterSideboardingReq":
        key = state._context_key(row["match_id"], row["game_number"])
        if key in state._POSTED_SIDEBOARD_KEYS:
            return []
        state._POSTED_SIDEBOARD_KEYS.add(key)
        row["sideboarding_entered"] = True
        return [row]

    if msg_type == "ClientMessageType_SubmitDeckResp":
        key = state._context_key(row["match_id"], row["game_number"])
        if key in state._POSTED_SUBMIT_DECK_KEYS:
            return []
        state._POSTED_SUBMIT_DECK_KEYS.add(key)
        row["submit_deck_seen"] = True
        return [row]

    if msg_type == "ClientMessageType_MulliganResp":
        row["mulligan_count"] = _reported_mulligan_count(
            row["match_id"],
            row["game_number"],
            payload.get("decision") or msg_type,
        )
        return [row]

    return []


def _reported_mulligan_count(match_id: Any, game_number: Any, decision: Any) -> int:
    key = state._context_key(match_id, game_number)
    current = state._MULLIGAN_COUNTS.get(key, 0)
    decision_text = str(decision or "").strip().lower()
    if decision_text in {"keep", "kept", "accept", "accepted"}:
        return current
    return current if current > 0 else 1


def _rank_text(payload: dict[str, Any]) -> str:
    constructed_class = payload.get("constructed_class", "")
    constructed_level = payload.get("constructed_level", "")
    constructed_percentile = payload.get("constructed_percentile")

    if constructed_class == "Mythic" and constructed_percentile not in (None, ""):
        return f"Mythic {constructed_percentile}".strip()
    return f"{constructed_class} {constructed_level}".strip()


def _rank_rows(base: dict[str, Any], payload: dict[str, Any]) -> list[dict[str, Any]]:
    rank_text = _rank_text(payload)
    if not rank_text or rank_text == state.get_last_posted_rank():
        return []

    state.set_last_posted_rank(rank_text)
    row = dict(base)
    row["scope"] = "Rank"
    row["constructed_rank"] = rank_text
    return [row]


def to_sheet_rows(event: Any) -> list[dict[str, Any]]:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}
    base = _base_sheet_row(event)

    if kind == "MatchState":
        return _match_state_rows(base, payload)
    if kind == "GameResult":
        return _game_result_rows(base, payload)
    if kind == "GameState":
        return _game_state_rows(base, payload)
    if kind == "ClientAction":
        return _client_action_rows(base, payload)
    if kind == "Rank":
        return _rank_rows(base, payload)
    return []


def _summarize_match_state(payload: dict[str, Any]) -> str:
    players = payload.get("players") or []
    opponent = players[1].get("player_name", "") if len(players) >= 2 else ""
    return (
        f"MatchState type={payload.get('type')} state={payload.get('state_type')} "
        f"match_id={payload.get('match_id')} opponent={opponent}"
    )


def _summarize_game_state(payload: dict[str, Any]) -> str:
    match_id, game_number, turn_number, active_player, phase, step, stage = _extract_turn_info(
        payload,
        state._CONTEXT,
    )
    return (
        f"GameState match={match_id} game={game_number} stage={stage} "
        f"turn={turn_number} active_player_seat_id={active_player} phase={phase} step={step}"
    )


def _summarize_game_result(payload: dict[str, Any]) -> str:
    match_id, game_number, winning_team, result_type, reason = _extract_game_result_identity(payload, state._CONTEXT)
    return (
        f"GameResult match={match_id} game={game_number} winner_team={winning_team} "
        f"result={result_type} reason={reason}"
    )


def _summarize_client_action(payload: dict[str, Any]) -> str:
    action_type = payload.get("type")
    if action_type == "mulligan_resp":
        return f"ClientAction mulligan decision={payload.get('decision')} request_id={payload.get('request_id')}"
    if action_type == "submit_deck_resp":
        return (
            f"ClientAction submit_deck main_count={len(payload.get('deck_cards') or [])} "
            f"side_count={len(payload.get('sideboard_cards') or [])}"
        )
    return f"ClientAction message_type={payload.get('message_type')}"


def _summarize_truncation(payload: dict[str, Any]) -> str:
    return (
        f"Truncation affected={payload.get('affected_message_type')} data_loss={payload.get('data_loss')} "
        f"recoverable={payload.get('recoverable')} game_object_count={payload.get('game_object_count')} "
        f"annotation_count={payload.get('annotation_count')}"
    )


def summarize(event: Any) -> str:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind == "DetailedLoggingStatus":
        return f"DetailedLoggingStatus enabled={payload.get('enabled')}"
    if kind == "MatchConnectionState":
        return f"MatchConnectionState old={payload.get('old')} new={payload.get('new')}"
    if kind == "TcpConnectionClose":
        return f"TcpConnectionClose status={payload.get('status')} reason={payload.get('reason')}"
    if kind == "WebSocketClosed":
        return f"WebSocketClosed closeType={payload.get('closeType')} reason={payload.get('reason')}"
    if kind == "ConnectionError":
        return f"ConnectionError type={payload.get('error_type')}"
    if kind == "DeckCollection":
        return f"DeckCollection decks={len(payload.get('decks') or {})}"
    if kind == "Inventory":
        inventory = payload.get("inventory") or {}
        if isinstance(inventory, dict):
            return f"Inventory keys={len(inventory)}"
        return "Inventory"
    if kind == "EventLifecycle":
        return f"EventLifecycle type={payload.get('type')}"
    if kind == "Rank":
        return (
            f"Rank constructed={payload.get('constructed_class')} "
            f"{payload.get('constructed_level')} percentile={payload.get('constructed_percentile')}"
        )
    if kind == "MatchState":
        return _summarize_match_state(payload)
    if kind == "GameState":
        return _summarize_game_state(payload)
    if kind == "GameResult":
        return _summarize_game_result(payload)
    if kind == "ClientAction":
        return _summarize_client_action(payload)
    if kind == "Truncation":
        return _summarize_truncation(payload)
    return f"{kind} {payload}"
