from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Any

from ..events import EventMetadata, GameEvent, MatchStateEvent
from ..log.entry import LogEntry
from . import api_common

MATCH_STATE_MARKER = "matchGameRoomStateChangedEvent"
_EVENT_TYPE_BY_STATE_TYPE = {
    "MatchGameRoomStateType_Playing": "match_started",
    "MatchGameRoomStateType_MatchCompleted": "match_completed",
}


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = entry.body
    if MATCH_STATE_MARKER not in body:
        return None
    parsed = api_common.parse_json_from_body(body, MATCH_STATE_MARKER)
    if parsed is None:
        return None
    state_event = _extract_state_event(parsed)
    if not isinstance(state_event, dict):
        return None
    return MatchStateEvent(EventMetadata(timestamp, body.encode()), build_payload(state_event))


def _extract_state_event(parsed: dict[str, Any]) -> dict[str, Any] | None:
    wrapped_state_event = parsed.get(MATCH_STATE_MARKER)
    if isinstance(wrapped_state_event, dict):
        return wrapped_state_event
    if isinstance(parsed.get("gameRoomInfo"), dict):
        return parsed
    return None


def _dict_payload(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _event_type_for_state(state_type: Any) -> str:
    return _EVENT_TYPE_BY_STATE_TYPE.get(str(state_type or "").strip(), "state_changed")


def _game_room_info(state_event: dict[str, Any]) -> dict[str, Any]:
    return _dict_payload(state_event.get("gameRoomInfo"))


def _game_room_config(game_room_info: dict[str, Any]) -> dict[str, Any]:
    return _dict_payload(game_room_info.get("gameRoomConfig"))


def _base_payload(
    *,
    state_type: str,
    game_room_config: dict[str, Any],
    player_source: list[dict[str, Any]],
    state_event: dict[str, Any],
) -> dict[str, Any]:
    return {
        "type": _event_type_for_state(state_type),
        "state_type": state_type,
        "match_id": game_room_config.get("matchId", ""),
        "event_id": _extract_event_id(game_room_config, player_source),
        "players": _build_players(player_source),
        "raw_match_state": state_event,
    }


def _final_result_payload(final_result: dict[str, Any]) -> dict[str, Any]:
    if not final_result:
        return {}
    return {
        "match_completed_reason": final_result.get("matchCompletedReason", ""),
        "game_results": _build_game_results(final_result.get("resultList")),
    }


def build_payload(state_event: dict[str, Any]) -> dict[str, Any]:
    game_room_info = _game_room_info(state_event)
    state_type = game_room_info.get("stateType", "")
    game_room_config = _game_room_config(game_room_info)
    player_source = _select_player_source(game_room_config, game_room_info)
    payload = _base_payload(
        state_type=state_type,
        game_room_config=game_room_config,
        player_source=player_source,
        state_event=state_event,
    )
    final_result = _dict_payload(game_room_info.get("finalMatchResult"))
    payload.update(_final_result_payload(final_result))
    return payload


def _select_player_source(
    game_room_config: dict[str, Any],
    game_room_info: dict[str, Any],
) -> list[dict[str, Any]]:
    reserved_players = _coerce_player_list(game_room_config.get("reservedPlayers"))
    if reserved_players:
        return reserved_players
    return _coerce_player_list(game_room_info.get("players"))


def _coerce_player_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [player for player in value if isinstance(player, dict)]


def _extract_event_id(
    game_room_config: dict[str, Any],
    players: Iterable[dict[str, Any]],
) -> str:
    event_id = str(game_room_config.get("eventId", "") or "").strip()
    if event_id:
        return event_id
    for player in players:
        candidate = str(player.get("eventId", "") or "").strip()
        if candidate:
            return candidate
    return ""


def _build_players(players: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized_players: list[dict[str, Any]] = []
    for player in players:
        normalized_players.append({
            "user_id": player.get("userId", ""),
            "player_name": player.get("playerName", ""),
            "system_seat_id": player.get("systemSeatId", 0),
            "team_id": player.get("teamId", 0),
        })
    return normalized_players


def _build_game_results(result_list: Any) -> list[dict[str, Any]]:
    if not isinstance(result_list, list):
        return []
    game_results: list[dict[str, Any]] = []
    for result in result_list:
        if not isinstance(result, dict):
            continue
        game_results.append({
            "scope": result.get("scope", ""),
            "result": result.get("result", ""),
            "winning_team_id": result.get("winningTeamId", 0),
            "reason": result.get("reason", ""),
        })
    return game_results
