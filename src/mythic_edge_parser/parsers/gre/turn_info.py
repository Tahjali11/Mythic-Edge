from __future__ import annotations

from typing import Any


def build_turn_info(gsm: dict[str, Any]) -> dict[str, Any]:
    raw_turn_info = _turn_info_payload(gsm)
    if not raw_turn_info:
        return {}

    return {
        "turn_number": _maybe_int(raw_turn_info.get("turnNumber")),
        "phase": _string_field(raw_turn_info.get("phase")),
        "step": _string_field(raw_turn_info.get("step")),
        "active_player_seat_id": _maybe_int(
            _first_present(raw_turn_info.get("activePlayer"), raw_turn_info.get("activePlayerSeatId"))
        ),
        "decision_player_seat_id": _maybe_int(raw_turn_info.get("decisionPlayer")),
        "priority_player_seat_id": _maybe_int(raw_turn_info.get("priorityPlayer")),
        "next_phase": _string_field(raw_turn_info.get("nextPhase")),
        "next_step": _string_field(raw_turn_info.get("nextStep")),
    }


def _turn_info_payload(gsm: dict[str, Any]) -> dict[str, Any]:
    raw_turn_info = gsm.get("turnInfo")
    if isinstance(raw_turn_info, dict):
        return raw_turn_info
    return {}


def _first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _string_field(value: Any) -> str:
    return str(value or "")


def _maybe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
