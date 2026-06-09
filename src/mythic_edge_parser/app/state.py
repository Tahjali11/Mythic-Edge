# Imports
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .extractors import (
    _extract_game_result_identity,
    _extract_game_result_scope_result,
    _extract_instance_grp_lookup,
    _extract_local_private_hand_instance_ids,
    _extract_local_team_from_client_action,
    _extract_local_team_from_game_state,
    _extract_starting_player_from_client_action,
    _extract_starting_player_from_game_state,
    _extract_turn_info,
    _infer_scope_label,
    _is_known_winner,
    _result_winner,
    _safe_iso,
    _safe_local_player,
)
from .grp_id_catalog import bootstrap_grp_id_catalog, resolve_grp_id_entry
from .models import MatchSummary
from .posting_state import PostingState
from .sheet_schema import GAME_LOG_SYNC_FIELDS as _GAME_LOG_SYNC_FIELDS
from .sheet_schema import MATCH_LOG_SYNC_FIELDS as _MATCH_LOG_SYNC_FIELDS

_DEFAULT_CONTEXT = {
    "current_match_id": "",
    "current_game_number": "",
    "current_player_team": "",
}


@dataclass(slots=True)
class ParserRuntimeState:
    local_turn_keys: set[tuple[Any, ...]] = field(default_factory=set)
    local_hand_snapshot_keys: set[tuple[Any, ...]] = field(default_factory=set)
    sheets_turn_keys: set[tuple[Any, ...]] = field(default_factory=set)
    posting: PostingState = field(default_factory=PostingState)
    last_posted_rank: str = ""
    latest_rank_text: str = ""
    latest_rank_class: Any = ""
    latest_rank_level: Any = ""
    latest_rank_percentile: Any = None
    context: dict[str, Any] = field(default_factory=lambda: dict(_DEFAULT_CONTEXT))
    mulligan_counts: dict[tuple[str, Any], int] = field(default_factory=dict)
    match_summaries: dict[str, MatchSummary] = field(default_factory=dict)
    current_log_date: str = ""
    current_log_path: Path | None = None
    game_instance_grp_ids: dict[tuple[str, int], dict[int, int]] = field(default_factory=dict)
    hand_snapshot_history: dict[tuple[str, int], list[list[str]]] = field(default_factory=dict)
    latest_hand_snapshot: dict[tuple[str, int], list[str]] = field(default_factory=dict)
    bottomed_cards_captured: set[tuple[str, int]] = field(default_factory=set)
    arena_card_lookup: dict[str, dict[str, Any]] | None = None
    arena_card_lookup_ready: bool = False
    gameplay_card_lookup_ready: bool = False

    @staticmethod
    def _replace_set_contents(target: set[Any], values: set[Any]) -> None:
        target.clear()
        target.update(values)

    @staticmethod
    def _replace_dict_contents(target: dict[Any, Any], values: dict[Any, Any]) -> None:
        target.clear()
        target.update(values)

    @property
    def posted_submit_deck_keys(self) -> set[tuple[Any, Any]]:
        return self.posting.posted_submit_deck_keys

    @posted_submit_deck_keys.setter
    def posted_submit_deck_keys(self, values: set[tuple[Any, Any]]) -> None:
        self._replace_set_contents(self.posting.posted_submit_deck_keys, values)

    @property
    def posted_sideboard_keys(self) -> set[tuple[Any, Any]]:
        return self.posting.posted_sideboard_keys

    @posted_sideboard_keys.setter
    def posted_sideboard_keys(self, values: set[tuple[Any, Any]]) -> None:
        self._replace_set_contents(self.posting.posted_sideboard_keys, values)

    @property
    def game_rows_posted(self) -> set[tuple[Any, Any]]:
        return self.posting.game_rows_posted

    @game_rows_posted.setter
    def game_rows_posted(self, values: set[tuple[Any, Any]]) -> None:
        self._replace_set_contents(self.posting.game_rows_posted, values)

    @property
    def match_rows_posted(self) -> set[Any]:
        return self.posting.match_rows_posted

    @match_rows_posted.setter
    def match_rows_posted(self, values: set[Any]) -> None:
        self._replace_set_contents(self.posting.match_rows_posted, values)

    @property
    def posted_match_summaries(self) -> set[str]:
        return self.posting.posted_match_summaries

    @posted_match_summaries.setter
    def posted_match_summaries(self, values: set[str]) -> None:
        self._replace_set_contents(self.posting.posted_match_summaries, values)

    @property
    def posted_match_log_rows(self) -> set[str]:
        return self.posting.posted_match_log_rows

    @posted_match_log_rows.setter
    def posted_match_log_rows(self, values: set[str]) -> None:
        self._replace_set_contents(self.posting.posted_match_log_rows, values)

    @property
    def last_posted_match_log_rows(self) -> dict[str, dict[str, Any]]:
        return self.posting.last_posted_match_log_rows

    @last_posted_match_log_rows.setter
    def last_posted_match_log_rows(self, values: dict[str, dict[str, Any]]) -> None:
        self._replace_dict_contents(self.posting.last_posted_match_log_rows, values)

    @property
    def last_posted_game_log_rows(self) -> dict[tuple[str, int], dict[str, Any]]:
        return self.posting.last_posted_game_log_rows

    @last_posted_game_log_rows.setter
    def last_posted_game_log_rows(self, values: dict[tuple[str, int], dict[str, Any]]) -> None:
        self._replace_dict_contents(self.posting.last_posted_game_log_rows, values)


RUNTIME_STATE = ParserRuntimeState()

# Backward-compatible aliases for modules and tests that mutate live bridge
# containers directly.
_LOCAL_TURN_KEYS = RUNTIME_STATE.local_turn_keys
_LOCAL_HAND_SNAPSHOT_KEYS = RUNTIME_STATE.local_hand_snapshot_keys
_SHEETS_TURN_KEYS = RUNTIME_STATE.sheets_turn_keys
_POSTING_STATE = RUNTIME_STATE.posting
_POSTED_SUBMIT_DECK_KEYS = _POSTING_STATE.posted_submit_deck_keys
_POSTED_SIDEBOARD_KEYS = _POSTING_STATE.posted_sideboard_keys
_GAME_ROWS_POSTED = _POSTING_STATE.game_rows_posted
_MATCH_ROWS_POSTED = _POSTING_STATE.match_rows_posted
_POSTED_MATCH_SUMMARIES = _POSTING_STATE.posted_match_summaries
_POSTED_MATCH_LOG_ROWS = _POSTING_STATE.posted_match_log_rows
_LAST_POSTED_MATCH_LOG_ROWS = _POSTING_STATE.last_posted_match_log_rows
_LAST_POSTED_GAME_LOG_ROWS = _POSTING_STATE.last_posted_game_log_rows
_CONTEXT = RUNTIME_STATE.context
_MULLIGAN_COUNTS = RUNTIME_STATE.mulligan_counts
_MATCH_SUMMARIES = RUNTIME_STATE.match_summaries
_GAME_INSTANCE_GRP_IDS = RUNTIME_STATE.game_instance_grp_ids
_HAND_SNAPSHOT_HISTORY = RUNTIME_STATE.hand_snapshot_history
_LATEST_HAND_SNAPSHOT = RUNTIME_STATE.latest_hand_snapshot
_BOTTOMED_CARDS_CAPTURED = RUNTIME_STATE.bottomed_cards_captured
_CURRENT_LOG_DATE = RUNTIME_STATE.current_log_date
_CURRENT_LOG_PATH = RUNTIME_STATE.current_log_path
_ARENA_CARD_LOOKUP = RUNTIME_STATE.arena_card_lookup
_ARENA_CARD_LOOKUP_READY = RUNTIME_STATE.arena_card_lookup_ready
_GAMEPLAY_CARD_LOOKUP_READY = RUNTIME_STATE.gameplay_card_lookup_ready
_LAST_POSTED_RANK = RUNTIME_STATE.last_posted_rank
_LATEST_RANK_TEXT = RUNTIME_STATE.latest_rank_text
_LATEST_RANK_CLASS = RUNTIME_STATE.latest_rank_class
_LATEST_RANK_LEVEL = RUNTIME_STATE.latest_rank_level
_LATEST_RANK_PERCENTILE = RUNTIME_STATE.latest_rank_percentile


def _effective_arena_card_lookup() -> dict[str, dict[str, Any]] | None:
    global _ARENA_CARD_LOOKUP

    if isinstance(_ARENA_CARD_LOOKUP, dict):
        RUNTIME_STATE.arena_card_lookup = _ARENA_CARD_LOOKUP
        return _ARENA_CARD_LOOKUP
    return RUNTIME_STATE.arena_card_lookup


def _effective_arena_card_lookup_ready() -> bool:
    global _ARENA_CARD_LOOKUP_READY

    if bool(_ARENA_CARD_LOOKUP_READY):
        RUNTIME_STATE.arena_card_lookup_ready = True
        return True
    return RUNTIME_STATE.arena_card_lookup_ready


def _effective_gameplay_card_lookup_ready() -> bool:
    global _GAMEPLAY_CARD_LOOKUP_READY

    if bool(_GAMEPLAY_CARD_LOOKUP_READY):
        RUNTIME_STATE.gameplay_card_lookup_ready = True
        return True
    return RUNTIME_STATE.gameplay_card_lookup_ready


def get_last_posted_rank() -> str:
    global _LAST_POSTED_RANK

    if str(_LAST_POSTED_RANK or "").strip() != str(RUNTIME_STATE.last_posted_rank or "").strip():
        RUNTIME_STATE.last_posted_rank = str(_LAST_POSTED_RANK or "").strip()
    return str(_LAST_POSTED_RANK or "").strip()


def set_last_posted_rank(rank_text: Any) -> None:
    global _LAST_POSTED_RANK

    normalized = str(rank_text or "").strip()
    _LAST_POSTED_RANK = normalized
    RUNTIME_STATE.last_posted_rank = normalized


def _normalized_rank_fields(payload: dict[str, Any]) -> tuple[str, Any, Any, Any]:
    rank_class = payload.get("constructed_class", "")
    rank_level = payload.get("constructed_level", "")
    rank_percentile = payload.get("constructed_percentile")
    if rank_class == "Mythic" and rank_percentile not in (None, ""):
        rank_text = f"Mythic {rank_percentile}".strip()
    else:
        rank_text = f"{rank_class} {rank_level}".strip()
    return rank_text, rank_class, rank_level, rank_percentile


def _store_latest_rank_snapshot(rank_text: Any, rank_class: Any, rank_level: Any, rank_percentile: Any) -> None:
    global _LATEST_RANK_TEXT, _LATEST_RANK_CLASS, _LATEST_RANK_LEVEL, _LATEST_RANK_PERCENTILE

    normalized_rank_text = str(rank_text or "").strip()
    _LATEST_RANK_TEXT = normalized_rank_text
    _LATEST_RANK_CLASS = rank_class
    _LATEST_RANK_LEVEL = rank_level
    _LATEST_RANK_PERCENTILE = rank_percentile
    RUNTIME_STATE.latest_rank_text = normalized_rank_text
    RUNTIME_STATE.latest_rank_class = rank_class
    RUNTIME_STATE.latest_rank_level = rank_level
    RUNTIME_STATE.latest_rank_percentile = rank_percentile


def _latest_rank_snapshot() -> tuple[str, Any, Any, Any]:
    latest_rank_text = str(_LATEST_RANK_TEXT or "").strip()
    if latest_rank_text != str(RUNTIME_STATE.latest_rank_text or "").strip():
        RUNTIME_STATE.latest_rank_text = latest_rank_text
    return (
        latest_rank_text,
        _LATEST_RANK_CLASS,
        _LATEST_RANK_LEVEL,
        _LATEST_RANK_PERCENTILE,
    )


def _apply_rank_snapshot(
    summary: MatchSummary,
    rank_text: Any,
    rank_class: Any,
    rank_level: Any,
    rank_percentile: Any,
    *,
    source: str,
) -> None:
    summary.set_constructed_rank(
        str(rank_text or "").strip(),
        rank_class,
        rank_level,
        rank_percentile,
        source=source,
    )


def _seed_summary_with_latest_rank(summary: MatchSummary) -> None:
    if str(summary.constructed_rank or "").strip():
        return
    rank_text, rank_class, rank_level, rank_percentile = _latest_rank_snapshot()
    if not rank_text:
        return
    _apply_rank_snapshot(
        summary,
        rank_text,
        rank_class,
        rank_level,
        rank_percentile,
        source="carried_forward_pre_match",
    )


def _context_key(match_id: Any, game_number: Any) -> tuple[Any, Any]:
    return (match_id or _CONTEXT["current_match_id"], game_number or _CONTEXT["current_game_number"])


def _normalized_game_key(match_id: Any, game_number: Any) -> tuple[str, int] | None:
    normalized_match_id = str(match_id or _CONTEXT["current_match_id"]).strip()
    if not normalized_match_id:
        return None
    try:
        normalized_game_number = int(game_number or _CONTEXT["current_game_number"])
    except (TypeError, ValueError):
        return None
    return normalized_match_id, normalized_game_number


def _ensure_gameplay_card_lookup() -> None:
    global _GAMEPLAY_CARD_LOOKUP_READY

    if _effective_gameplay_card_lookup_ready():
        return
    arena_lookup = _effective_arena_card_lookup()
    if _effective_arena_card_lookup_ready() and isinstance(arena_lookup, dict):
        RUNTIME_STATE.gameplay_card_lookup_ready = True
        _GAMEPLAY_CARD_LOOKUP_READY = True
        return
    try:
        bootstrap_grp_id_catalog()
    except Exception:
        pass
    RUNTIME_STATE.gameplay_card_lookup_ready = True
    _GAMEPLAY_CARD_LOOKUP_READY = True


def _is_keep_decision(decision: Any) -> bool:
    return str(decision or "").strip().lower() in {"keep", "kept", "accept", "accepted"}


def _placeholder_card_name(instance_id: int, grp_id: Any) -> str:
    try:
        normalized_grp_id = int(grp_id)
    except (TypeError, ValueError):
        return f"[Missing Arena ID for instance {instance_id}]"
    return f"[Arena ID {normalized_grp_id}]"


def _resolve_hand_snapshot(instance_grp_lookup: dict[int, int], hand_instance_ids: list[int]) -> list[str]:
    _ensure_gameplay_card_lookup()
    resolved_cards: list[str] = []
    arena_lookup = _effective_arena_card_lookup()
    arena_lookup_ready = _effective_arena_card_lookup_ready()
    for instance_id in hand_instance_ids:
        grp_id = instance_grp_lookup.get(instance_id)
        if grp_id is None:
            resolved_cards.append(_placeholder_card_name(instance_id, None))
            continue
        card = (
            (arena_lookup or {}).get(str(grp_id), {})
            if arena_lookup_ready and isinstance(arena_lookup, dict)
            else resolve_grp_id_entry(grp_id)
        )
        card_name = str(card.get("resolved_name", "")).strip()
        if not card_name:
            card_name = str(card.get("name", "")).strip()
        if card_name:
            resolved_cards.append(card_name)
            continue
        resolved_cards.append(_placeholder_card_name(instance_id, grp_id))
    return resolved_cards


def _record_hand_snapshot(key: tuple[str, int], cards: list[str]) -> None:
    if not cards:
        return
    history = _HAND_SNAPSHOT_HISTORY.setdefault(key, [])
    if not history or history[-1] != cards:
        history.append(list(cards))
    _LATEST_HAND_SNAPSHOT[key] = list(cards)


def _card_list_difference(source_cards: list[str], kept_cards: list[str]) -> list[str]:
    remaining = Counter(source_cards)
    for card in kept_cards:
        if remaining[card] > 0:
            remaining[card] -= 1
    difference: list[str] = []
    for card in source_cards:
        if remaining[card] > 0:
            difference.append(card)
            remaining[card] -= 1
    return difference


def _capture_bottomed_cards(summary: MatchSummary, game_number: Any, final_hand: list[str]) -> None:
    key = _normalized_game_key(summary.match_id, game_number)
    if key is None or key in _BOTTOMED_CARDS_CAPTURED:
        return

    history = _HAND_SNAPSHOT_HISTORY.get(key, [])
    for prior_snapshot in reversed(history):
        if len(prior_snapshot) <= len(final_hand):
            continue
        bottomed_cards = _card_list_difference(prior_snapshot, final_hand)
        if bottomed_cards:
            summary.add_game_mulliganed_away(game_number, bottomed_cards)
            _BOTTOMED_CARDS_CAPTURED.add(key)
            return


def _record_discarded_mulligan_hand(summary: MatchSummary, match_id: Any, game_number: Any) -> None:
    key = _normalized_game_key(match_id, game_number)
    if key is None:
        return
    discarded_snapshot = _LATEST_HAND_SNAPSHOT.pop(key, None)
    if not discarded_snapshot:
        return
    summary.add_game_mulliganed_away(game_number, discarded_snapshot)


def _record_opening_hand_candidate(summary: MatchSummary, game_number: Any, payload: dict[str, Any]) -> None:
    key = _normalized_game_key(summary.match_id, game_number)
    if key is None:
        return

    hand_instance_ids = _extract_local_private_hand_instance_ids(payload)
    if not hand_instance_ids:
        return
    if len(hand_instance_ids) < 4 or len(hand_instance_ids) > 7:
        return

    turn_match_id, _, turn_number, _, _, _, _ = _extract_turn_info(payload, _CONTEXT)
    if turn_match_id not in (None, "", summary.match_id):
        return

    instance_grp_lookup = _GAME_INSTANCE_GRP_IDS.setdefault(key, {})
    instance_grp_lookup.update(_extract_instance_grp_lookup(payload))
    resolved_cards = _resolve_hand_snapshot(instance_grp_lookup, hand_instance_ids)
    _record_hand_snapshot(key, resolved_cards)

    game = summary.game(game_number)
    if game is None:
        return

    expected_hand_size = max(7 - int(game.mulligans), 0)
    if expected_hand_size and len(hand_instance_ids) != expected_hand_size:
        return
    if turn_number != 1:
        return

    summary.set_game_opening_hand(game_number, resolved_cards)
    _capture_bottomed_cards(summary, game_number, resolved_cards)


def _next_mulligan_count(match_id: Any, game_number: Any, decision: Any) -> int:
    key = (str(match_id or _CONTEXT["current_match_id"]), game_number or _CONTEXT["current_game_number"])

    if not key[0] or key[1] in (None, ""):
        return 0

    text = str(decision or "").strip().lower()
    if text in {"keep", "kept", "accept", "accepted"}:
        return _MULLIGAN_COUNTS.get(key, 0)

    current = _MULLIGAN_COUNTS.get(key, 0) + 1
    _MULLIGAN_COUNTS[key] = current
    return current


def _ensure_match_summary(match_id: str) -> MatchSummary:
    existing = _MATCH_SUMMARIES.get(match_id)
    if existing is not None:
        return existing

    summary = MatchSummary(match_id=match_id)
    _seed_summary_with_latest_rank(summary)
    _MATCH_SUMMARIES[match_id] = summary
    return summary


def _set_first_last(summary: MatchSummary, event: Any) -> None:
    summary.touch(_safe_iso(event))


def _set_local_team(summary: MatchSummary, team_id: Any) -> None:
    if team_id in (None, ""):
        return
    _CONTEXT["current_player_team"] = team_id
    summary.player_team = team_id


def _set_event_id(summary: MatchSummary, event_id: Any) -> None:
    text = str(event_id or "").strip()
    if not text:
        return
    if not summary.event_id:
        summary.event_id = text
        return
    if summary.event_id == "Play" and text != "Play":
        summary.event_id = text


def reset_runtime_state() -> None:
    global _CURRENT_LOG_DATE, _CURRENT_LOG_PATH
    global _ARENA_CARD_LOOKUP, _ARENA_CARD_LOOKUP_READY, _GAMEPLAY_CARD_LOOKUP_READY
    global _LATEST_RANK_TEXT, _LATEST_RANK_CLASS, _LATEST_RANK_LEVEL, _LATEST_RANK_PERCENTILE

    _LOCAL_TURN_KEYS.clear()
    _LOCAL_HAND_SNAPSHOT_KEYS.clear()
    _SHEETS_TURN_KEYS.clear()
    _POSTING_STATE.reset()
    _MULLIGAN_COUNTS.clear()
    _MATCH_SUMMARIES.clear()
    _GAME_INSTANCE_GRP_IDS.clear()
    _HAND_SNAPSHOT_HISTORY.clear()
    _LATEST_HAND_SNAPSHOT.clear()
    _BOTTOMED_CARDS_CAPTURED.clear()

    _CONTEXT.clear()
    _CONTEXT.update(_DEFAULT_CONTEXT)
    RUNTIME_STATE.context = _CONTEXT

    _CURRENT_LOG_DATE = ""
    _CURRENT_LOG_PATH = None
    RUNTIME_STATE.current_log_date = ""
    RUNTIME_STATE.current_log_path = None

    _ARENA_CARD_LOOKUP = None
    _ARENA_CARD_LOOKUP_READY = False
    _GAMEPLAY_CARD_LOOKUP_READY = False
    _LATEST_RANK_TEXT = ""
    _LATEST_RANK_CLASS = ""
    _LATEST_RANK_LEVEL = ""
    _LATEST_RANK_PERCENTILE = None
    RUNTIME_STATE.arena_card_lookup = None
    RUNTIME_STATE.arena_card_lookup_ready = False
    RUNTIME_STATE.gameplay_card_lookup_ready = False
    RUNTIME_STATE.latest_rank_text = ""
    RUNTIME_STATE.latest_rank_class = ""
    RUNTIME_STATE.latest_rank_level = ""
    RUNTIME_STATE.latest_rank_percentile = None

    set_last_posted_rank("")


def _update_match_summary(event: Any) -> None:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind == "MatchState":
        match_id = payload.get("match_id") or _CONTEXT["current_match_id"]
        if not match_id:
            return

        _CONTEXT["current_match_id"] = match_id
        summary = _ensure_match_summary(match_id)
        _set_first_last(summary, event)
        _set_event_id(summary, payload.get("event_id"))

        players = payload.get("players") or []
        team_id = _CONTEXT["current_player_team"] or summary.player_team
        if team_id in (None, ""):
            local_player = _safe_local_player(players)
            team_id = local_player.get("team_id")
        _set_local_team(summary, team_id)

        game_result_index = 1
        for result in payload.get("game_results") or []:
            if not isinstance(result, dict):
                continue
            scope = _infer_scope_label(result.get("scope", ""))
            winning_team = result.get("winning_team_id")
            result_type = result.get("result", "")
            reason = result.get("reason", "")

            if scope == "Game":
                summary.set_game_winner(game_result_index, winning_team)
                game_result_index += 1
            elif scope == "Match" and winning_team not in (None, ""):
                summary.match_winner_team = winning_team
                summary.match_result_type = result_type
                summary.match_result_reason = reason

        if payload.get("type") == "match_started":
            _CONTEXT["current_game_number"] = 1
        return

    if kind == "GameState":
        match_id, game_number, turn_number, _, _, _, _ = _extract_turn_info(payload, _CONTEXT)
        match_id = match_id or _CONTEXT["current_match_id"]
        game_number = game_number or _CONTEXT["current_game_number"]
        if not match_id:
            return

        _CONTEXT["current_match_id"] = match_id
        summary = _ensure_match_summary(match_id)
        _set_first_last(summary, event)
        _set_local_team(summary, _extract_local_team_from_game_state(payload))
        summary.ingest_game_info(payload.get("game_info") or {})
        if game_number not in (None, ""):
            _CONTEXT["current_game_number"] = game_number
            summary.touch_game(game_number, _safe_iso(event))
            summary.set_game_starting_player(
                game_number,
                _extract_starting_player_from_game_state(payload),
            )
            summary.set_game_turn_count(game_number, turn_number)
            _record_opening_hand_candidate(summary, game_number, payload)
        return

    if kind == "Rank":
        rank_text, rank_class, rank_level, rank_percentile = _normalized_rank_fields(payload)
        if not rank_text:
            return

        set_last_posted_rank(rank_text)
        _store_latest_rank_snapshot(rank_text, rank_class, rank_level, rank_percentile)
        match_id = _CONTEXT["current_match_id"]
        if match_id:
            summary = _ensure_match_summary(match_id)
            if not summary.is_ready():
                _set_first_last(summary, event)
                _apply_rank_snapshot(
                    summary,
                    rank_text,
                    rank_class,
                    rank_level,
                    rank_percentile,
                    source="payload",
                )
        return

    if kind == "ClientAction":
        match_id = _CONTEXT["current_match_id"]
        game_number = _CONTEXT["current_game_number"]
        if not match_id:
            return

        summary = _ensure_match_summary(match_id)
        _set_first_last(summary, event)
        action_type = payload.get("type", "")
        _set_local_team(summary, _extract_local_team_from_client_action(payload))
        if game_number not in (None, ""):
            summary.touch_game(game_number, _safe_iso(event))

        if action_type == "mulligan_resp":
            decision = payload.get("decision")
            if not _is_keep_decision(decision):
                _record_discarded_mulligan_hand(summary, match_id, game_number)
            summary.set_game_mulligans(
                game_number,
                _next_mulligan_count(match_id, game_number, decision),
            )
            return

        if action_type == "submit_deck_resp":
            summary.submit_deck_seen = True
            return

        if action_type != "generic_client_action":
            return

        msg_type = payload.get("message_type", "")
        if msg_type == "ClientMessageType_ChooseStartingPlayerResp":
            summary.set_game_starting_player(
                game_number,
                _extract_starting_player_from_client_action(payload),
            )
        elif msg_type == "ClientMessageType_EnterSideboardingReq":
            summary.sideboarding_entered = True
        elif msg_type == "ClientMessageType_SubmitDeckResp":
            summary.submit_deck_seen = True
        elif msg_type == "ClientMessageType_MulliganResp":
            decision = payload.get("decision") or msg_type
            if not _is_keep_decision(decision):
                _record_discarded_mulligan_hand(summary, match_id, game_number)
            summary.set_game_mulligans(
                game_number,
                _next_mulligan_count(match_id, game_number, decision),
            )
        return

    if kind == "GameResult":
        match_id, game_number, winning_team, result_type, reason = _extract_game_result_identity(payload, _CONTEXT)
        if not match_id:
            return

        _CONTEXT["current_match_id"] = match_id
        if game_number not in (None, ""):
            _CONTEXT["current_game_number"] = game_number

        summary = _ensure_match_summary(match_id)
        _set_first_last(summary, event)
        summary.ingest_game_info(payload.get("game_info") or {})

        if _CONTEXT["current_player_team"] not in (None, ""):
            summary.player_team = _CONTEXT["current_player_team"]

        summary.touch_game(game_number, _safe_iso(event))
        has_nested_results = isinstance(payload.get("results"), list)
        game_result = _extract_game_result_scope_result(payload, "Game", require_known_winner=True)
        game_winner = _result_winner(game_result) if game_result is not None else winning_team
        if (game_result is not None or not has_nested_results) and _is_known_winner(game_winner):
            summary.set_game_winner(game_number, game_winner)

        match_result = _extract_game_result_scope_result(payload, "Match", require_known_winner=True)
        match_result_fallback = _extract_game_result_scope_result(payload, "Match", require_known_winner=False)
        if match_result is not None:
            summary.match_winner_team = _result_winner(match_result)
            summary.match_result_type = match_result.get("result", "")
            summary.match_result_reason = match_result.get("reason", "")
            return

        if str(payload.get("match_state", "")) == "MatchState_MatchComplete" and _is_known_winner(winning_team):
            summary.match_winner_team = winning_team
            if match_result_fallback is not None:
                summary.match_result_type = match_result_fallback.get("result", "")
                summary.match_result_reason = match_result_fallback.get("reason", "")
            else:
                summary.match_result_type = result_type
                summary.match_result_reason = reason
        return


def _match_summary_ready(summary: MatchSummary) -> bool:
    return summary.is_ready()


def _normalize_match_log_value(value: Any) -> Any:
    if value in (None, ""):
        return ""
    if isinstance(value, float):
        return round(value, 10)
    return value


def _changed_fields(
    previous_row: dict[str, Any] | None,
    current_row: dict[str, Any],
    sync_fields: tuple[str, ...],
) -> list[str]:
    if previous_row is None:
        return [
            sync_field
            for sync_field in sync_fields
            if _normalize_match_log_value(current_row.get(sync_field)) != ""
        ]

    changed: list[str] = []
    for sync_field in sync_fields:
        previous_value = _normalize_match_log_value(previous_row.get(sync_field))
        current_value = _normalize_match_log_value(current_row.get(sync_field))
        if previous_value != current_value:
            changed.append(sync_field)
    return changed


def build_match_summary_row(match_id: str) -> dict[str, Any] | None:
    summary = _MATCH_SUMMARIES.get(match_id)
    if not summary or not _match_summary_ready(summary):
        return None
    return summary.to_sheet_row()


def build_game_summary_rows(match_id: str) -> list[dict[str, Any]]:
    summary = _MATCH_SUMMARIES.get(match_id)
    if not summary:
        return []
    return summary.to_game_sheet_rows()


def _game_log_key(match_id: Any, game_number: Any) -> tuple[str, int] | None:
    try:
        normalized_game_number = int(game_number)
    except (TypeError, ValueError):
        return None

    normalized_match_id = str(match_id or "").strip()
    if not normalized_match_id:
        return None
    return normalized_match_id, normalized_game_number


def build_match_log_row(match_id: str) -> dict[str, Any] | None:
    summary = _MATCH_SUMMARIES.get(match_id)
    if not summary or not _match_summary_ready(summary):
        return None
    return summary.to_match_log_row(final=True)


def build_live_match_log_row(match_id: str) -> dict[str, Any] | None:
    summary = _MATCH_SUMMARIES.get(match_id)
    if not summary or not summary.match_id:
        return None
    return summary.to_match_log_row(final=False)


def build_match_log_update(match_id: str) -> tuple[dict[str, Any] | None, list[str], bool]:
    summary = _MATCH_SUMMARIES.get(match_id)
    if not summary or not summary.match_id:
        return None, [], False

    is_final = _match_summary_ready(summary)
    row = summary.to_match_log_row(final=is_final)
    previous_row = _POSTING_STATE.last_posted_match_log_rows.get(match_id)
    changed_fields = _changed_fields(previous_row, row, _MATCH_LOG_SYNC_FIELDS)

    if not changed_fields:
        return None, [], is_final
    return row, changed_fields, is_final


def mark_match_log_posted(match_id: str, row: dict[str, Any]) -> None:
    _POSTING_STATE.mark_match_log_posted(match_id, row)


def build_game_log_updates(match_id: str) -> list[tuple[dict[str, Any], list[str], bool]]:
    summary = _MATCH_SUMMARIES.get(match_id)
    if not summary:
        return []

    updates: list[tuple[dict[str, Any], list[str], bool]] = []
    for row in summary.to_game_sheet_rows():
        key = _game_log_key(row.get("MTGA Match ID"), row.get("Game Number"))
        if key is None:
            continue

        previous_row = _POSTING_STATE.last_posted_game_log_rows.get(key)
        changed_fields = _changed_fields(previous_row, row, _GAME_LOG_SYNC_FIELDS)

        if not changed_fields:
            continue

        is_final = str(row.get("Game Result", "")).strip() != ""
        updates.append((row, changed_fields, is_final))

    return updates


def mark_game_log_posted(match_id: str, game_number: Any, row: dict[str, Any]) -> None:
    key = _game_log_key(match_id, game_number)
    if key is None:
        return
    _POSTING_STATE.mark_game_log_posted(key, row)


def get_match_summary(match_id: str) -> MatchSummary | None:
    return _MATCH_SUMMARIES.get(match_id)


def iter_match_summaries() -> list[MatchSummary]:
    return list(_MATCH_SUMMARIES.values())


def get_runtime_state() -> ParserRuntimeState:
    return RUNTIME_STATE


def get_context_snapshot() -> dict[str, Any]:
    return dict(RUNTIME_STATE.context)
