from datetime import datetime
from typing import Any

from .config import LOCAL_PLAYER_INDEX


def _safe_local_player(players: list[dict[str, Any]]) -> dict[str, Any]:
    if not players:
        return {}
    if 0 <= LOCAL_PLAYER_INDEX < len(players):
        return players[LOCAL_PLAYER_INDEX] or {}
    return players[0] or {}


def _first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _maybe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _safe_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def _raw_game_state_payload(payload: dict[str, Any]) -> dict[str, Any]:
    raw = payload.get("raw_game_state") or {}
    if not isinstance(raw, dict):
        return {}
    return raw


def _raw_game_state_message(payload: dict[str, Any]) -> dict[str, Any]:
    raw = _raw_game_state_payload(payload)
    if not raw:
        return {}

    gsm = raw.get("gameStateMessage")
    if isinstance(gsm, dict):
        return gsm
    return {}


def _queued_game_state_message(payload: dict[str, Any]) -> dict[str, Any]:
    raw = _raw_game_state_payload(payload)
    if not raw:
        return {}

    queued = raw.get("queuedGameStateMessage")
    if isinstance(queued, dict):
        queued_gsm = queued.get("gameStateMessage")
        if isinstance(queued_gsm, dict):
            return queued_gsm
    return {}


def _game_state_dict_section(
    payload: dict[str, Any],
    *,
    top_level_key: str,
    message_key: str,
) -> dict[str, Any]:
    top_level_value = payload.get(top_level_key)
    if isinstance(top_level_value, dict):
        return top_level_value

    raw_message = _raw_game_state_message(payload)
    raw_section = raw_message.get(message_key)
    if isinstance(raw_section, dict):
        return raw_section

    queued_message = _queued_game_state_message(payload)
    queued_section = queued_message.get(message_key)
    if isinstance(queued_section, dict):
        return queued_section

    return {}


def _game_state_list_section(
    payload: dict[str, Any],
    *,
    top_level_key: str,
    message_key: str,
) -> list[dict[str, Any]]:
    top_level_value = payload.get(top_level_key)
    if isinstance(top_level_value, list):
        return [item for item in top_level_value if isinstance(item, dict)]

    raw_message = _raw_game_state_message(payload)
    raw_section = raw_message.get(message_key)
    if isinstance(raw_section, list):
        return [item for item in raw_section if isinstance(item, dict)]

    queued_message = _queued_game_state_message(payload)
    queued_section = queued_message.get(message_key)
    if isinstance(queued_section, list):
        return [item for item in queued_section if isinstance(item, dict)]

    return []


def _queued_game_info(payload: dict[str, Any]) -> dict[str, Any]:
    queued_message = _queued_game_state_message(payload)
    if not queued_message:
        return {}
    return _safe_dict(queued_message.get("gameInfo"))


def _game_state_identity_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return _safe_dict(payload.get("identity"))


def _game_state_game_info(payload: dict[str, Any]) -> dict[str, Any]:
    return _game_state_dict_section(
        payload,
        top_level_key="game_info",
        message_key="gameInfo",
    )


def _game_state_turn_info_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return _game_state_dict_section(
        payload,
        top_level_key="turn_info",
        message_key="turnInfo",
    )


def _game_state_system_seat_ids(payload: dict[str, Any]) -> list[int]:
    top_level = payload.get("system_seat_ids")
    if isinstance(top_level, list):
        normalized: list[int] = []
        for seat_id in top_level:
            normalized_seat = _maybe_int(seat_id)
            if normalized_seat is not None:
                normalized.append(normalized_seat)
        return normalized

    raw = payload.get("raw_game_state") or {}
    if not isinstance(raw, dict):
        return []

    normalized = []
    for seat_id in _safe_list(raw.get("systemSeatIds")):
        normalized_seat = _maybe_int(seat_id)
        if normalized_seat is not None:
            normalized.append(normalized_seat)
    return normalized


def _game_state_players(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return _game_state_list_section(
        payload,
        top_level_key="players",
        message_key="players",
    )


def _game_state_zones(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return _game_state_list_section(
        payload,
        top_level_key="zones",
        message_key="zones",
    )


def _game_state_objects(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return _game_state_list_section(
        payload,
        top_level_key="game_objects",
        message_key="gameObjects",
    )


def _game_state_actions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return _game_state_list_section(
        payload,
        top_level_key="actions",
        message_key="actions",
    )


def _game_state_annotations(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return _game_state_list_section(
        payload,
        top_level_key="annotations",
        message_key="annotations",
    )


def _player_seat_id(player: dict[str, Any]) -> int | None:
    return _maybe_int(
        _first_present(
            player.get("systemSeatNumber"),
            player.get("systemSeatId"),
            player.get("system_seat_id"),
        )
    )


def _player_team_id(player: dict[str, Any]) -> int | None:
    return _maybe_int(_first_present(player.get("teamId"), player.get("team_id")))


def _hydrate_game_state_identity(
    payload: dict[str, Any],
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity = _game_state_identity_payload(payload)
    game_info = _game_state_game_info(payload)
    queued_game_info = _queued_game_info(payload)
    turn_info = _game_state_turn_info_payload(payload)

    payload_match_id = str(
        _first_present(
            identity.get("match_id"),
            game_info.get("matchID"),
            queued_game_info.get("matchID"),
        )
        or ""
    ).strip()
    payload_game_number = _maybe_int(
        _first_present(
            identity.get("game_number"),
            game_info.get("gameNumber"),
            queued_game_info.get("gameNumber"),
        )
    )

    match_id = payload_match_id
    game_number = payload_game_number
    fallback_used = False

    if context:
        if not match_id:
            match_id = str(context.get("current_match_id") or "").strip()
            fallback_used = bool(match_id)
        if game_number is None:
            game_number = _maybe_int(context.get("current_game_number"))
            fallback_used = fallback_used or game_number is not None

    if payload_match_id or payload_game_number is not None:
        identity_source = "payload+context" if fallback_used else "payload"
    elif fallback_used:
        identity_source = "context"
    else:
        identity_source = "missing"

    return {
        "match_id": match_id,
        "game_number": game_number,
        "turn_number": _maybe_int(
            _first_present(
                identity.get("turn_number"),
                turn_info.get("turn_number"),
                turn_info.get("turnNumber"),
                payload.get("turn_number"),
            )
        ),
        "active_player_seat_id": _maybe_int(
            _first_present(
                identity.get("active_player_seat_id"),
                turn_info.get("active_player_seat_id"),
                turn_info.get("activePlayer"),
                turn_info.get("activePlayerSeatId"),
                payload.get("active_player_seat_id"),
            )
        ),
        "phase": str(
            _first_present(identity.get("phase"), turn_info.get("phase"), payload.get("phase")) or ""
        ),
        "step": str(
            _first_present(identity.get("step"), turn_info.get("step"), payload.get("step")) or ""
        ),
        "stage": str(
            _first_present(identity.get("stage"), game_info.get("stage"), payload.get("stage")) or ""
        ),
        "identity_source": identity_source,
    }


def _extract_turn_info(
    payload: dict[str, Any],
    context: dict[str, Any] | None = None,
) -> tuple[Any, Any, Any, Any, Any, Any, Any]:
    identity = _hydrate_game_state_identity(payload, context)
    return (
        identity["match_id"],
        identity["game_number"],
        identity["turn_number"],
        identity["active_player_seat_id"],
        identity["phase"],
        identity["step"],
        identity["stage"],
    )

#Find the starting player seat from a ClientAction payload
def _extract_starting_player_from_client_action(payload: dict[str, Any]) -> Any:
    key_candidates = (
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
    )
    for key in key_candidates:
        if payload.get(key) not in (None, ""):
            return payload.get(key)

    raw_client_action = payload.get("raw_client_action") or {}
    if isinstance(raw_client_action, dict):
        inner_payload = raw_client_action.get("payload") or {}
        if isinstance(inner_payload, dict):
            for key in key_candidates:
                if inner_payload.get(key) not in (None, ""):
                    return inner_payload.get(key)

            choose_starting_player = inner_payload.get("chooseStartingPlayerResp") or {}
            if isinstance(choose_starting_player, dict):
                for key in key_candidates:
                    if choose_starting_player.get(key) not in (None, ""):
                        return choose_starting_player.get(key)
    return None


def _extract_local_team_from_client_action(payload: dict[str, Any]) -> Any:
    key_candidates = (
        "team_id",
        "teamId",
    )
    nested_candidates = (
        "chooseStartingPlayerResp",
        "mulliganResp",
        "submitDeckResp",
    )

    for key in key_candidates:
        if payload.get(key) not in (None, ""):
            return payload.get(key)

    raw_client_action = payload.get("raw_client_action") or {}
    if not isinstance(raw_client_action, dict):
        return None

    inner_payload = raw_client_action.get("payload") or {}
    if isinstance(inner_payload, dict):
        for key in key_candidates:
            if inner_payload.get(key) not in (None, ""):
                return inner_payload.get(key)

        for nested_key in nested_candidates:
            nested = inner_payload.get(nested_key) or {}
            if not isinstance(nested, dict):
                continue
            for key in key_candidates:
                if nested.get(key) not in (None, ""):
                    return nested.get(key)
    return None


def _extract_local_team_from_game_state(payload: dict[str, Any]) -> Any:
    system_seat_ids = _game_state_system_seat_ids(payload)
    if not system_seat_ids:
        return None

    local_seat = system_seat_ids[0]
    for player in _game_state_players(payload):
        seat_id = _player_seat_id(player)
        if seat_id != local_seat:
            continue
        team_id = _player_team_id(player)
        if team_id is not None:
            return team_id
    return None


def _extract_starting_player_from_game_state(payload: dict[str, Any]) -> Any:
    identity = _hydrate_game_state_identity(payload)
    turn_number = identity["turn_number"]
    if turn_number != 1:
        return None

    active_seat = identity["active_player_seat_id"]
    if active_seat in (None, ""):
        return None

    players = _game_state_players(payload)
    if not players:
        return active_seat

    for player in players:
        seat_id = _player_seat_id(player)
        if seat_id != active_seat:
            continue
        team_id = _player_team_id(player)
        if team_id is not None:
            return team_id

    return active_seat


def _extract_local_private_hand_instance_ids(payload: dict[str, Any]) -> list[int]:
    system_seat_ids = _game_state_system_seat_ids(payload)
    local_seat = system_seat_ids[0] if system_seat_ids else None

    for zone in _game_state_zones(payload):
        if _first_present(zone.get("type"), zone.get("zone_type")) != "ZoneType_Hand":
            continue
        if zone.get("visibility") != "Visibility_Private":
            continue
        owner_seat = _maybe_int(_first_present(zone.get("ownerSeatId"), zone.get("owner_seat_id")))
        if local_seat not in (None, "") and owner_seat not in (None, "", local_seat):
            continue
        instance_ids = _safe_list(_first_present(zone.get("objectInstanceIds"), zone.get("object_instance_ids")))
        if not instance_ids:
            return []
        normalized: list[int] = []
        for instance_id in instance_ids:
            normalized_instance = _maybe_int(instance_id)
            if normalized_instance is not None:
                normalized.append(normalized_instance)
        return normalized

    return []


def _extract_instance_grp_lookup(payload: dict[str, Any]) -> dict[int, int]:
    mapping: dict[int, int] = {}
    for game_object in _game_state_objects(payload):
        instance_id = _maybe_int(_first_present(game_object.get("instanceId"), game_object.get("instance_id")))
        grp_id = _maybe_int(
            _first_present(
                game_object.get("grpId"),
                game_object.get("grp_id"),
                game_object.get("overlayGrpId"),
                game_object.get("overlay_grp_id"),
            )
        )
        if instance_id is None or grp_id is None:
            continue
        mapping[instance_id] = grp_id
    return mapping

#Normalize scope text like MatchScope_Game into plain text like "Game" or "Match"
def _infer_scope_label(scope_value: Any) -> str:
    text = str(scope_value or "")
    if "MatchScope_Game" in text or text == "Game":
        return "Game"
    if "MatchScope_Match" in text or text == "Match":
        return "Match"
    return text

#Read match ID, game number, winning team, result type, and reason from a GameResult Payload
def _extract_game_result_identity(payload: dict[str, Any], context: dict[str, Any]) -> tuple[Any, Any, Any, Any, Any]:
    identity = _safe_dict(payload.get("identity"))
    game_info = payload.get("game_info") or {}
    match_id = str(
        identity.get("match_id") or game_info.get("matchID") or context["current_match_id"] or ""
    ).strip()
    game_number = _first_present(
        identity.get("game_number"),
        game_info.get("gameNumber"),
        context["current_game_number"],
    )
    winning_team = payload.get("winning_team_id", "")
    result_type = payload.get("result_type", "")
    reason = payload.get("reason", "")
    return match_id, game_number, winning_team, result_type, reason

#Detect whether a GameResult payload also contains a match-scope result
def _has_match_scope_result(payload: dict[str, Any]) -> bool:
    for result in (payload.get("results") or []):
        if _infer_scope_label(result.get("scope", "")) == "Match":
            return True
    return False

#Gets a safe datetime from the event metadata, falling back to the current time if not available or invalid
def _event_datetime(event: Any) -> datetime:
    metadata = getattr(event, "metadata", None)
    timestamp = metadata.timestamp if metadata and getattr(metadata, "timestamp", None) else None
    if isinstance(timestamp, datetime):
        return timestamp
    return datetime.now()

#Convert an event to ISO datetime text
def _safe_iso(event: Any) -> str:
    return _event_datetime(event).isoformat()
