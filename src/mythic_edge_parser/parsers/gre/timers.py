from __future__ import annotations

import math
import re
from collections.abc import Mapping
from typing import Any

from .. import api_common

TIMER_RECORD_OBJECT = "mythic_edge_gre_timer"
TIMER_COLLECTION_OBJECT = "mythic_edge_gre_timers"
SCHEMA_VERSION = "parser_gre_timers.v1"

_SOURCE_ARRAY = "timers"
_CAMEL_BOUNDARY_RE = re.compile(r"(?<!^)(?=[A-Z])")
_NUMERIC_STRING_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$")

_TIMER_ID_KEYS = ("timerId", "timer_id", "id", "timerID")
_STRING_FIELD_KEYS = {
    "type",
    "timerType",
    "timer_type",
    "timerName",
    "timer_name",
    "name",
    "state",
    "timerState",
    "timer_state",
    "phase",
    "step",
}
_TIMER_TYPE_KEYS = ("timerType", "timer_type", "type")
_TIMER_NAME_KEYS = ("timerName", "timer_name", "name")
_TIMER_STATE_KEYS = ("timerState", "timer_state", "state")
_BOOLEAN_FIELD_NAMES = {"running", "paused", "expired", "enabled", "active"}
_SEAT_FIELD_KEYS = {
    "owner_seat_id": ("ownerSeatId", "owner_seat_id"),
    "controller_seat_id": ("controllerSeatId", "controller_seat_id"),
    "player_seat_id": ("playerSeatId", "player_seat_id"),
    "system_seat_id": ("systemSeatId", "system_seat_id"),
    "team_id": ("teamId", "team_id"),
    "player_id": ("playerId", "player_id"),
}
_PLAYER_SEAT_FALLBACK_KEYS = ("seatId", "seat_id")
_EXCLUDED_GENERIC_KEYS = set(_TIMER_ID_KEYS) | set(_PLAYER_SEAT_FALLBACK_KEYS)
for _seat_keys in _SEAT_FIELD_KEYS.values():
    _EXCLUDED_GENERIC_KEYS.update(_seat_keys)

_TIME_WORDS = ("time", "timer", "duration", "elapsed", "remaining", "timeout", "deadline", "rope", "clock")


def normalize_timer_record(
    raw_timer: object,
    *,
    source_index: int,
) -> dict[str, object]:
    if not isinstance(raw_timer, dict):
        return _empty_record(
            source_index=source_index,
            degradation_flags=["malformed_timer_record"],
            evidence_status="degraded",
            confidence="low",
            review_required=True,
        )

    degradation_flags: list[str] = []
    timer_id = _timer_id(raw_timer, degradation_flags)
    seat_fields, direct_seat_ids = _seat_fields(raw_timer, degradation_flags)
    string_fields = _string_fields(raw_timer, degradation_flags)
    boolean_fields = _boolean_fields(raw_timer, degradation_flags)
    numeric_fields, time_values = _numeric_fields(raw_timer, degradation_flags)
    unsupported_field_names = _unsupported_field_names(raw_timer, degradation_flags)
    if _truncation_or_data_loss(raw_timer):
        _append_flag(degradation_flags, "truncation_or_data_loss_evidence")

    trusted_values = bool(
        timer_id != ""
        or any(value != "" for value in seat_fields.values())
        or string_fields
        or boolean_fields
        or numeric_fields
    )
    return {
        "object": TIMER_RECORD_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "source_array": _SOURCE_ARRAY,
        "source_index": source_index,
        "timer_id": timer_id,
        "timer_type": _selected_string_field(string_fields, _TIMER_TYPE_KEYS),
        "timer_name": _selected_string_field(string_fields, _TIMER_NAME_KEYS),
        "timer_state": _selected_string_field(string_fields, _TIMER_STATE_KEYS),
        "seat_fields": seat_fields,
        "direct_seat_ids": direct_seat_ids,
        "numeric_fields": numeric_fields,
        "string_fields": string_fields,
        "boolean_fields": boolean_fields,
        "time_values": time_values,
        "unsupported_field_names": unsupported_field_names,
        "source_evidence": "timer",
        "evidence_status": _evidence_status(degradation_flags, trusted_values),
        "value_source": _value_source(time_values, degradation_flags, trusted_values),
        "confidence": _confidence(time_values, degradation_flags, trusted_values),
        "degradation_flags": degradation_flags,
        "review_required": bool(degradation_flags),
    }


def normalize_timer_array(
    timers: object,
    *,
    turn_info: Mapping[str, object] | None = None,
) -> dict[str, object]:
    records: list[dict[str, object]] = []
    degradation_flags: list[str] = []
    if timers is None:
        records = []
    elif isinstance(timers, list):
        records = [
            normalize_timer_record(raw_timer, source_index=source_index)
            for source_index, raw_timer in enumerate(timers)
        ]
    else:
        _append_flag(degradation_flags, "malformed_timers_section")

    timer_ids: list[int] = []
    timer_types: list[str] = []
    direct_seat_ids: list[int] = []
    time_units_seen = {"seconds": 0, "milliseconds": 0, "unknown": 0}
    for record in records:
        timer_id = record["timer_id"]
        if isinstance(timer_id, int):
            _extend_unique(timer_ids, [timer_id])
        timer_type = record["timer_type"]
        if isinstance(timer_type, str) and timer_type:
            _extend_unique(timer_types, [timer_type])
        _extend_unique(direct_seat_ids, [seat_id for seat_id in record["direct_seat_ids"] if isinstance(seat_id, int)])
        record_time_values = record["time_values"]
        if isinstance(record_time_values, dict):
            time_units_seen["seconds"] += len(record_time_values.get("seconds", []))
            time_units_seen["milliseconds"] += len(record_time_values.get("milliseconds", []))
            time_units_seen["unknown"] += len(record_time_values.get("unknown_unit", []))

    degraded_records = sum(
        1
        for record in records
        if record["degradation_flags"] or record["evidence_status"] in {"degraded", "unknown", "conflict"}
    )
    return {
        "object": TIMER_COLLECTION_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "total_records": len(records),
        "degraded_records": degraded_records,
        "review_required": bool(degradation_flags) or any(bool(record["review_required"]) for record in records),
        "source_array": _SOURCE_ARRAY,
        "timer_ids": timer_ids,
        "timer_types": timer_types,
        "direct_seat_ids": direct_seat_ids,
        "time_units_seen": time_units_seen,
        "contextual_turn_info": _contextual_turn_info(turn_info),
        "degradation_flags": degradation_flags,
        "records": records,
    }


def timer_records_by_direct_seat(
    normalized_timers: Mapping[str, object],
) -> dict[int, list[dict[str, object]]]:
    by_seat: dict[int, list[dict[str, object]]] = {}
    records = normalized_timers.get("records")
    if not isinstance(records, list):
        return by_seat
    for record in records:
        if not isinstance(record, dict):
            continue
        direct_seat_ids = record.get("direct_seat_ids")
        if not isinstance(direct_seat_ids, list):
            continue
        for seat_id in direct_seat_ids:
            if isinstance(seat_id, int):
                by_seat.setdefault(seat_id, []).append(record)
    return by_seat


def _empty_record(
    *,
    source_index: int,
    degradation_flags: list[str],
    evidence_status: str,
    confidence: str,
    review_required: bool,
) -> dict[str, object]:
    return {
        "object": TIMER_RECORD_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "source_array": _SOURCE_ARRAY,
        "source_index": source_index,
        "timer_id": "",
        "timer_type": "",
        "timer_name": "",
        "timer_state": "",
        "seat_fields": _empty_seat_fields(),
        "direct_seat_ids": [],
        "numeric_fields": [],
        "string_fields": [],
        "boolean_fields": [],
        "time_values": {"seconds": [], "milliseconds": [], "unknown_unit": []},
        "unsupported_field_names": [],
        "source_evidence": "timer",
        "evidence_status": evidence_status,
        "value_source": "unknown",
        "confidence": confidence,
        "degradation_flags": degradation_flags,
        "review_required": review_required,
    }


def _timer_id(raw_timer: Mapping[str, object], degradation_flags: list[str]) -> int | str:
    for key in _TIMER_ID_KEYS:
        if key not in raw_timer:
            continue
        timer_id = _id_like_int(raw_timer.get(key))
        if timer_id is None:
            _append_flag(degradation_flags, "malformed_timer_id")
            return ""
        return timer_id
    return ""


def _seat_fields(raw_timer: Mapping[str, object], degradation_flags: list[str]) -> tuple[dict[str, object], list[int]]:
    seat_fields = _empty_seat_fields()
    for canonical_key, raw_keys in _SEAT_FIELD_KEYS.items():
        selected = _selected_direct_id(raw_timer, raw_keys, degradation_flags)
        if selected is not None:
            seat_fields[canonical_key] = selected

    if seat_fields["player_seat_id"] == "":
        fallback = _selected_direct_id(raw_timer, _PLAYER_SEAT_FALLBACK_KEYS, degradation_flags)
        if fallback is not None:
            seat_fields["player_seat_id"] = fallback
    else:
        fallback_values = _valid_direct_values(raw_timer, _PLAYER_SEAT_FALLBACK_KEYS, degradation_flags)
        if fallback_values and any(value != seat_fields["player_seat_id"] for value in fallback_values):
            _append_flag(degradation_flags, "conflicting_timer_seat_fields")

    direct_seat_ids: list[int] = []
    for canonical_key in ("owner_seat_id", "controller_seat_id", "player_seat_id", "system_seat_id"):
        value = seat_fields[canonical_key]
        if isinstance(value, int):
            _extend_unique(direct_seat_ids, [value])
    return seat_fields, direct_seat_ids


def _selected_direct_id(
    raw_timer: Mapping[str, object],
    raw_keys: tuple[str, ...],
    degradation_flags: list[str],
) -> int | None:
    values = _valid_direct_values(raw_timer, raw_keys, degradation_flags)
    if len(set(values)) > 1:
        _append_flag(degradation_flags, "conflicting_timer_seat_fields")
    if values:
        return values[0]
    return None


def _valid_direct_values(
    raw_timer: Mapping[str, object],
    raw_keys: tuple[str, ...],
    degradation_flags: list[str],
) -> list[int]:
    values: list[int] = []
    for key in raw_keys:
        if key not in raw_timer:
            continue
        value = _id_like_int(raw_timer.get(key))
        if value is None:
            _append_flag(degradation_flags, "malformed_timer_seat_field")
            continue
        values.append(value)
    return values


def _string_fields(raw_timer: Mapping[str, object], degradation_flags: list[str]) -> list[dict[str, object]]:
    fields: list[dict[str, object]] = []
    for key, value in raw_timer.items():
        if key in _EXCLUDED_GENERIC_KEYS or _is_boolean_field_name(key):
            continue
        if key in _STRING_FIELD_KEYS:
            if not isinstance(value, str):
                _append_flag(degradation_flags, "malformed_timer_string_field")
                continue
            text = value.strip()
            if text:
                fields.append({"key": key, "normalized_key": _normalize_key(key), "value": text})
            continue
        if isinstance(value, str) and value.strip() and _numeric_value(value) is None:
            fields.append({"key": key, "normalized_key": _normalize_key(key), "value": value.strip()})
    return fields


def _boolean_fields(raw_timer: Mapping[str, object], degradation_flags: list[str]) -> list[dict[str, object]]:
    fields: list[dict[str, object]] = []
    for key, value in raw_timer.items():
        if key in _EXCLUDED_GENERIC_KEYS or key in _STRING_FIELD_KEYS or _looks_numeric_or_time_key(key):
            continue
        if _is_boolean_field_name(key):
            if isinstance(value, bool):
                fields.append({"key": key, "normalized_key": _normalize_key(key), "value": value})
            else:
                _append_flag(degradation_flags, "malformed_timer_boolean_field")
            continue
        if isinstance(value, bool):
            fields.append({"key": key, "normalized_key": _normalize_key(key), "value": value})
    return fields


def _numeric_fields(
    raw_timer: Mapping[str, object],
    degradation_flags: list[str],
) -> tuple[list[dict[str, object]], dict[str, list[dict[str, object]]]]:
    fields: list[dict[str, object]] = []
    time_values: dict[str, list[dict[str, object]]] = {"seconds": [], "milliseconds": [], "unknown_unit": []}
    for key, raw_value in raw_timer.items():
        if key in _EXCLUDED_GENERIC_KEYS or key in _STRING_FIELD_KEYS or _is_boolean_field_name(key):
            continue
        if isinstance(raw_value, (dict, list)):
            continue
        if isinstance(raw_value, bool):
            if _looks_numeric_or_time_key(key):
                _append_flag(degradation_flags, "malformed_timer_numeric_field")
            continue
        value = _numeric_value(raw_value)
        if value is None:
            if _looks_numeric_or_time_key(key):
                _append_flag(degradation_flags, "malformed_timer_numeric_field")
            continue
        normalized_key = _normalize_key(key)
        unit = _time_unit(key)
        field = {"key": key, "normalized_key": normalized_key, "value": value, "unit": unit}
        if unit in {"seconds", "milliseconds"}:
            field["seconds_value"] = _seconds_value(value, unit)
        if value < 0:
            _append_flag(degradation_flags, "negative_timer_value")
        if unit == "seconds":
            time_values["seconds"].append({"key": key, "value": value, "seconds_value": value})
        elif unit == "milliseconds":
            time_values["milliseconds"].append({"key": key, "value": value, "seconds_value": value / 1000.0})
        elif unit == "unknown" and _looks_time_key(key):
            _append_flag(degradation_flags, "unknown_timer_time_unit")
            time_values["unknown_unit"].append({"key": key, "value": value})
        fields.append(field)
    return fields, time_values


def _unsupported_field_names(raw_timer: Mapping[str, object], degradation_flags: list[str]) -> list[str]:
    field_names: list[str] = []
    for key, value in raw_timer.items():
        if not isinstance(value, (dict, list)):
            continue
        field_names.append(key)
        if _looks_timer_related_key(key):
            _append_flag(degradation_flags, "unsupported_timer_field_shape")
    return field_names


def _selected_string_field(fields: list[Mapping[str, object]], keys: tuple[str, ...]) -> str:
    for key in keys:
        for field in fields:
            if field.get("key") == key and isinstance(field.get("value"), str):
                return str(field["value"])
    return ""


def _contextual_turn_info(turn_info: Mapping[str, object] | None) -> dict[str, object]:
    if not isinstance(turn_info, Mapping):
        return {
            "turn_number": "",
            "active_player_seat_id": "",
            "decision_player_seat_id": "",
            "priority_player_seat_id": "",
        }
    return {
        "turn_number": _context_int(turn_info.get("turn_number")),
        "active_player_seat_id": _context_int(turn_info.get("active_player_seat_id")),
        "decision_player_seat_id": _context_int(turn_info.get("decision_player_seat_id")),
        "priority_player_seat_id": _context_int(turn_info.get("priority_player_seat_id")),
    }


def _empty_seat_fields() -> dict[str, object]:
    return {
        "owner_seat_id": "",
        "controller_seat_id": "",
        "player_seat_id": "",
        "system_seat_id": "",
        "team_id": "",
        "player_id": "",
    }


def _evidence_status(degradation_flags: list[str], trusted_values: bool) -> str:
    if "conflicting_timer_seat_fields" in degradation_flags:
        return "conflict"
    if degradation_flags:
        return "degraded"
    if not trusted_values:
        return "unknown"
    return "observed"


def _value_source(
    time_values: Mapping[str, list[dict[str, object]]],
    degradation_flags: list[str],
    trusted_values: bool,
) -> str:
    if "conflicting_timer_seat_fields" in degradation_flags:
        return "conflict"
    if time_values["seconds"] or time_values["milliseconds"] or time_values["unknown_unit"]:
        return "derived"
    if trusted_values:
        return "observed"
    return "unknown"


def _confidence(
    time_values: Mapping[str, list[dict[str, object]]],
    degradation_flags: list[str],
    trusted_values: bool,
) -> str:
    if degradation_flags:
        return "low"
    if not trusted_values:
        return "unknown"
    if time_values["unknown_unit"]:
        return "medium"
    return "high"


def _id_like_int(value: object) -> int | None:
    values = api_common.normalize_int_list([value])
    if values:
        return values[0]
    return None


def _context_int(value: object) -> int | str:
    normalized = _id_like_int(value)
    if normalized is None:
        return ""
    return normalized


def _numeric_value(value: object) -> int | float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        return None
    if isinstance(value, str):
        stripped = value.strip()
        if not _NUMERIC_STRING_RE.match(stripped):
            return None
        numeric = float(stripped)
        if not math.isfinite(numeric):
            return None
        if numeric.is_integer() and "." not in stripped:
            return int(numeric)
        return numeric
    return None


def _seconds_value(value: int | float, unit: str) -> int | float:
    if unit == "milliseconds":
        return value / 1000.0
    return value


def _time_unit(key: str) -> str:
    normalized_key = _normalize_key(key)
    if (
        key.endswith(("Ms", "MS", "Millis", "Milliseconds"))
        or normalized_key.endswith("_milliseconds")
        or normalized_key.endswith("_ms")
    ):
        return "milliseconds"
    if (
        key.endswith(("Sec", "Secs", "Seconds"))
        or normalized_key.endswith("_seconds")
        or normalized_key.endswith("_secs")
        or normalized_key.endswith("_sec")
    ):
        return "seconds"
    if _looks_time_key(key):
        return "unknown"
    return ""


def _looks_time_key(key: str) -> bool:
    normalized_key = _normalize_key(key)
    if normalized_key.endswith("_count") or normalized_key == "count" or "count_" in normalized_key:
        return False
    return any(word in normalized_key for word in _TIME_WORDS)


def _looks_numeric_or_time_key(key: str) -> bool:
    normalized_key = _normalize_key(key)
    return _looks_time_key(key) or normalized_key.endswith("_count") or normalized_key == "count"


def _looks_timer_related_key(key: str) -> bool:
    normalized_key = _normalize_key(key)
    return any(word in normalized_key for word in (*_TIME_WORDS, "seat", "player", "team", "state"))


def _is_boolean_field_name(key: str) -> bool:
    normalized_key = _normalize_key(key)
    return normalized_key in _BOOLEAN_FIELD_NAMES or normalized_key.startswith(("is_", "has_"))


def _truncation_or_data_loss(raw_timer: Mapping[str, object]) -> bool:
    for key in ("truncation_or_data_loss_evidence", "truncationMarker", "dataLoss"):
        if raw_timer.get(key) is True:
            return True
    return False


def _normalize_key(key: str) -> str:
    first_pass = _CAMEL_BOUNDARY_RE.sub("_", str(key)).replace("-", "_")
    return re.sub(r"_+", "_", first_pass).lower().strip("_")


def _extend_unique(target: list[Any], values: list[Any]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def _append_flag(target: list[str], flag: str) -> None:
    if flag not in target:
        target.append(flag)
