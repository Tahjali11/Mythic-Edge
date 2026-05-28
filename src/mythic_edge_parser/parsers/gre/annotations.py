from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .. import api_common

ANNOTATION_RECORD_OBJECT = "mythic_edge_gre_annotation"
ANNOTATION_COLLECTION_OBJECT = "mythic_edge_gre_annotations"
SCHEMA_VERSION = "parser_gre_annotations.v1"

_SOURCE_ANNOTATIONS = "annotations"
_SOURCE_PERSISTENT_ANNOTATIONS = "persistent_annotations"

_MARKERS_BY_TYPE = {
    "AnnotationType_ObjectIdChanged": "object_id_changed",
    "AnnotationType_ZoneTransfer": "zone_transfer",
    "AnnotationType_ResolutionStart": "resolution_start",
    "AnnotationType_ResolutionComplete": "resolution_complete",
    "AnnotationType_NewTurnStarted": "new_turn_started",
    "AnnotationType_RevealedCardDeleted": "revealed_card_deleted",
    "AnnotationType_Shuffle": "shuffle",
    "AnnotationType_UserActionTaken": "user_action_taken",
    "AnnotationType_ManaPaid": "mana_paid",
    "AnnotationType_AbilityInstanceDeleted": "ability_instance_deleted",
}
_MARKER_DEFAULTS = {marker: False for marker in _MARKERS_BY_TYPE.values()}
_DETAIL_VALUE_KEYS = ("valueInt32", "valueInt64", "valueString", "valueBool")


def normalize_annotation_record(
    raw_annotation: object,
    *,
    source_array: str,
    source_index: int,
) -> dict[str, object]:
    persistent = source_array == _SOURCE_PERSISTENT_ANNOTATIONS
    source_evidence = "persistent_annotation" if persistent else "annotation"
    if not isinstance(raw_annotation, dict):
        return _empty_record(
            source_array=source_array,
            source_index=source_index,
            persistent=persistent,
            source_evidence=source_evidence,
            degradation_flags=["malformed_annotation_record"],
            evidence_status="degraded",
            confidence="low",
            review_required=True,
        )

    degradation_flags: list[str] = []
    type_names = _type_names(raw_annotation.get("type"), degradation_flags)
    affected_ids = _affected_ids(raw_annotation, degradation_flags)
    details = _details(raw_annotation.get("details"), degradation_flags)
    detail_values = _detail_values(details)
    categories = _string_detail_values(details, "category")
    markers = _markers(type_names)
    replacement_pairs = _object_replacement_pairs(markers, details, degradation_flags)
    zone_transfer = _zone_transfer(markers, affected_ids, details)
    trusted_values = bool(type_names or affected_ids or details)

    return {
        "object": ANNOTATION_RECORD_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "source_array": source_array,
        "source_index": source_index,
        "persistent": persistent,
        "annotation_id": _annotation_id(raw_annotation),
        "type_names": type_names,
        "primary_type": type_names[0] if type_names else "",
        "affected_ids": affected_ids,
        "details": details,
        "detail_values": detail_values,
        "categories": categories if markers["zone_transfer"] else [],
        "markers": markers,
        "object_replacement": _record_object_replacement(replacement_pairs),
        "zone_transfer": zone_transfer,
        "source_evidence": source_evidence,
        "evidence_status": _evidence_status(degradation_flags, trusted_values),
        "value_source": _value_source(markers, replacement_pairs, zone_transfer, trusted_values),
        "confidence": _confidence(degradation_flags, trusted_values),
        "degradation_flags": degradation_flags,
        "review_required": bool(degradation_flags),
    }


def normalize_annotation_arrays(
    *,
    annotations: object,
    persistent_annotations: object = None,
    diff_deleted_persistent_annotation_ids: object = None,
) -> dict[str, object]:
    records: list[dict[str, object]] = []
    degradation_flags: list[str] = []
    records.extend(
        _records_from_source(
            annotations,
            source_array=_SOURCE_ANNOTATIONS,
            malformed_flag="malformed_annotations_section",
            collection_degradation_flags=degradation_flags,
        )
    )
    records.extend(
        _records_from_source(
            persistent_annotations,
            source_array=_SOURCE_PERSISTENT_ANNOTATIONS,
            malformed_flag="malformed_persistent_annotations_section",
            collection_degradation_flags=degradation_flags,
        )
    )
    diff_deleted_ids = api_common.normalize_int_list(diff_deleted_persistent_annotation_ids)
    if diff_deleted_persistent_annotation_ids is not None and not isinstance(
        diff_deleted_persistent_annotation_ids, list
    ):
        _append_flag(degradation_flags, "malformed_diff_deleted_persistent_annotation_ids")

    annotation_types: list[str] = []
    marker_types: list[str] = []
    object_replacements: list[dict[str, object]] = []
    zone_transfers: list[dict[str, object]] = []
    for record in records:
        _extend_unique(annotation_types, list(record["type_names"]))
        for type_name in record["type_names"]:
            marker = _MARKERS_BY_TYPE.get(type_name)
            if marker is not None:
                _extend_unique(marker_types, [marker])
        object_replacements.extend(_record_object_replacement_summaries(record))
        zone_transfer = record["zone_transfer"]
        if isinstance(zone_transfer, dict) and record["markers"]["zone_transfer"]:
            zone_transfers.append(_zone_transfer_summary(record, zone_transfer))

    degraded_records = sum(
        1
        for record in records
        if record["degradation_flags"] or record["evidence_status"] in {"degraded", "unknown", "conflict"}
    )
    return {
        "object": ANNOTATION_COLLECTION_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "total_records": len(records),
        "degraded_records": degraded_records,
        "review_required": bool(degradation_flags) or any(bool(record["review_required"]) for record in records),
        "source_arrays": {
            _SOURCE_ANNOTATIONS: sum(1 for record in records if record["source_array"] == _SOURCE_ANNOTATIONS),
            _SOURCE_PERSISTENT_ANNOTATIONS: sum(
                1 for record in records if record["source_array"] == _SOURCE_PERSISTENT_ANNOTATIONS
            ),
        },
        "annotation_types": annotation_types,
        "marker_types": marker_types,
        "diff_deleted_persistent_annotation_ids": diff_deleted_ids,
        "object_replacements": object_replacements,
        "zone_transfers": zone_transfers,
        "degradation_flags": degradation_flags,
        "records": records,
    }


def annotation_categories_for_instance(
    normalized_annotations: Mapping[str, object],
    instance_id: int,
) -> list[str]:
    categories: list[str] = []
    zone_transfers = normalized_annotations.get("zone_transfers")
    if not isinstance(zone_transfers, list):
        return categories
    for zone_transfer in zone_transfers:
        if not isinstance(zone_transfer, dict):
            continue
        if instance_id not in zone_transfer.get("affected_ids", []):
            continue
        _extend_unique(categories, _string_list(zone_transfer.get("categories")))
    return categories


def replacement_instance_ids(
    normalized_annotations: Mapping[str, object],
) -> dict[int, int]:
    replacements: dict[int, int] = {}
    object_replacements = normalized_annotations.get("object_replacements")
    if not isinstance(object_replacements, list):
        return replacements
    for replacement in object_replacements:
        if not isinstance(replacement, dict):
            continue
        original_id = _normalized_int(replacement.get("original_instance_id"))
        new_id = _normalized_int(replacement.get("new_instance_id"))
        if original_id is not None and new_id is not None:
            replacements[original_id] = new_id
    return replacements


def _empty_record(
    *,
    source_array: str,
    source_index: int,
    persistent: bool,
    source_evidence: str,
    degradation_flags: list[str],
    evidence_status: str,
    confidence: str,
    review_required: bool,
) -> dict[str, object]:
    return {
        "object": ANNOTATION_RECORD_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "source_array": source_array,
        "source_index": source_index,
        "persistent": persistent,
        "annotation_id": "",
        "type_names": [],
        "primary_type": "",
        "affected_ids": [],
        "details": [],
        "detail_values": {},
        "categories": [],
        "markers": dict(_MARKER_DEFAULTS),
        "object_replacement": {"original_instance_id": "", "new_instance_id": ""},
        "zone_transfer": {
            "affected_ids": [],
            "categories": [],
            "source_zone_ids": [],
            "destination_zone_ids": [],
            "semantic_hints": [],
        },
        "source_evidence": source_evidence,
        "evidence_status": evidence_status,
        "value_source": "unknown",
        "confidence": confidence,
        "degradation_flags": degradation_flags,
        "review_required": review_required,
    }


def _records_from_source(
    value: object,
    *,
    source_array: str,
    malformed_flag: str,
    collection_degradation_flags: list[str],
) -> list[dict[str, object]]:
    if value is None:
        return []
    if not isinstance(value, list):
        _append_flag(collection_degradation_flags, malformed_flag)
        return []
    return [
        normalize_annotation_record(raw_annotation, source_array=source_array, source_index=source_index)
        for source_index, raw_annotation in enumerate(value)
    ]


def _type_names(value: object, degradation_flags: list[str]) -> list[str]:
    if value is None:
        _append_flag(degradation_flags, "missing_annotation_type")
        return []
    raw_values = value if isinstance(value, list) else [value]
    out: list[str] = []
    for raw_value in raw_values:
        if not isinstance(raw_value, str):
            _append_flag(degradation_flags, "malformed_annotation_type")
            continue
        text = raw_value.strip()
        if text and text not in out:
            out.append(text)
    if not out:
        _append_flag(degradation_flags, "missing_annotation_type")
    return out


def _affected_ids(raw_annotation: dict[str, object], degradation_flags: list[str]) -> list[int]:
    if "affectedIds" in raw_annotation:
        value = raw_annotation.get("affectedIds")
    elif "affected_ids" in raw_annotation:
        value = raw_annotation.get("affected_ids")
    else:
        return []
    if not isinstance(value, list):
        _append_flag(degradation_flags, "malformed_affected_ids")
        return []
    return api_common.normalize_int_list(value)


def _annotation_id(raw_annotation: dict[str, object]) -> int | str:
    for key in ("id", "annotationId", "annotation_id"):
        if key not in raw_annotation:
            continue
        value = _normalized_int(raw_annotation.get(key))
        if value is not None:
            return value
        return ""
    return ""


def _details(value: object, record_degradation_flags: list[str]) -> list[dict[str, object]]:
    if value is None:
        return []
    if not isinstance(value, list):
        _append_flag(record_degradation_flags, "malformed_annotation_details")
        return []
    out: list[dict[str, object]] = []
    for detail in value:
        if not isinstance(detail, dict):
            out.append(_malformed_detail(record_degradation_flags, "malformed_annotation_detail"))
            continue
        detail_flags: list[str] = []
        raw_key = detail.get("key")
        key = raw_key.strip() if isinstance(raw_key, str) else ""
        if not key:
            _append_flag(detail_flags, "malformed_detail_key")
        value_ints = _detail_int_values(detail.get("valueInt32")) + _detail_int_values(detail.get("valueInt64"))
        value_strings = _detail_string_values(detail.get("valueString"), detail_flags)
        value_bools = _detail_bool_values(detail.get("valueBool"))
        record_degradation_flags.extend(flag for flag in detail_flags if flag not in record_degradation_flags)
        out.append(
            {
                "key": key,
                "value_ints": value_ints,
                "value_strings": value_strings,
                "value_bools": value_bools,
                "degradation_flags": detail_flags,
            }
        )
    return out


def _malformed_detail(record_degradation_flags: list[str], flag: str) -> dict[str, object]:
    _append_flag(record_degradation_flags, flag)
    return {
        "key": "",
        "value_ints": [],
        "value_strings": [],
        "value_bools": [],
        "degradation_flags": [flag],
    }


def _detail_values(details: list[dict[str, object]]) -> dict[str, list[object]]:
    values: dict[str, list[object]] = {}
    for detail in details:
        key = detail.get("key")
        if not isinstance(key, str) or not key:
            continue
        rows = values.setdefault(key, [])
        rows.extend(detail["value_ints"])
        rows.extend(detail["value_strings"])
        rows.extend(detail["value_bools"])
    return values


def _detail_int_values(value: object) -> list[int]:
    values = value if isinstance(value, list) else [value]
    return api_common.normalize_int_list(values)


def _detail_string_values(value: object, degradation_flags: list[str]) -> list[str]:
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    out: list[str] = []
    for raw_value in values:
        if not isinstance(raw_value, str):
            _append_flag(degradation_flags, "malformed_detail_string_value")
            continue
        text = raw_value.strip()
        if text:
            out.append(text)
    return out


def _detail_bool_values(value: object) -> list[bool]:
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    return [raw_value for raw_value in values if isinstance(raw_value, bool)]


def _markers(type_names: list[str]) -> dict[str, bool]:
    markers = dict(_MARKER_DEFAULTS)
    for type_name in type_names:
        marker = _MARKERS_BY_TYPE.get(type_name)
        if marker is not None:
            markers[marker] = True
    return markers


def _object_replacement_pairs(
    markers: Mapping[str, bool],
    details: list[dict[str, object]],
    degradation_flags: list[str],
) -> list[tuple[int, int]]:
    if not markers.get("object_id_changed"):
        return []
    original_ids = _int_detail_values(details, "orig_id")
    new_ids = _int_detail_values(details, "new_id")
    pairs = list(zip(original_ids, new_ids, strict=False))
    if len(original_ids) != len(new_ids) or not pairs:
        _append_flag(degradation_flags, "incomplete_object_replacement")
    return pairs


def _record_object_replacement(pairs: list[tuple[int, int]]) -> dict[str, object]:
    if not pairs:
        return {"original_instance_id": "", "new_instance_id": ""}
    original_id, new_id = pairs[0]
    return {"original_instance_id": original_id, "new_instance_id": new_id}


def _record_object_replacement_summaries(record: Mapping[str, object]) -> list[dict[str, object]]:
    if not record["markers"]["object_id_changed"]:
        return []
    details = record.get("details")
    if not isinstance(details, list):
        return []
    summaries: list[dict[str, object]] = []
    for original_id, new_id in zip(_int_detail_values(details, "orig_id"), _int_detail_values(details, "new_id")):
        summaries.append(
            {
                "original_instance_id": original_id,
                "new_instance_id": new_id,
                "source_array": record["source_array"],
                "source_index": record["source_index"],
                "confidence": "high",
            }
        )
    return summaries


def _zone_transfer(
    markers: Mapping[str, bool],
    affected_ids: list[int],
    details: list[dict[str, object]],
) -> dict[str, object]:
    if not markers.get("zone_transfer"):
        return {
            "affected_ids": [],
            "categories": [],
            "source_zone_ids": [],
            "destination_zone_ids": [],
            "semantic_hints": [],
        }
    categories = _string_detail_values(details, "category")
    return {
        "affected_ids": list(affected_ids),
        "categories": categories,
        "source_zone_ids": _int_detail_values(details, "zone_src"),
        "destination_zone_ids": _int_detail_values(details, "zone_dest"),
        "semantic_hints": _semantic_hints(categories),
    }


def _zone_transfer_summary(record: Mapping[str, object], zone_transfer: Mapping[str, object]) -> dict[str, object]:
    return {
        "affected_ids": list(zone_transfer["affected_ids"]),
        "categories": list(zone_transfer["categories"]),
        "source_zone_ids": list(zone_transfer["source_zone_ids"]),
        "destination_zone_ids": list(zone_transfer["destination_zone_ids"]),
        "semantic_hints": list(zone_transfer["semantic_hints"]),
        "source_array": record["source_array"],
        "source_index": record["source_index"],
        "confidence": "medium",
    }


def _string_detail_values(details: list[dict[str, object]], key: str) -> list[str]:
    values: list[str] = []
    for detail in details:
        if detail.get("key") != key:
            continue
        _extend_unique(values, list(detail["value_strings"]))
    return values


def _int_detail_values(details: list[dict[str, object]], key: str) -> list[int]:
    values: list[int] = []
    for detail in details:
        if detail.get("key") != key:
            continue
        values.extend(detail["value_ints"])
    return values


def _semantic_hints(categories: list[str]) -> list[str]:
    hints: list[str] = []
    for category in categories:
        if category == "PlayLand":
            _extend_unique(hints, ["land_play_hint"])
        if category.startswith("Cast"):
            _extend_unique(hints, ["cast_hint"])
        if category == "Resolve":
            _extend_unique(hints, ["resolve_hint"])
    return hints


def _evidence_status(degradation_flags: list[str], trusted_values: bool) -> str:
    if degradation_flags:
        return "degraded"
    if not trusted_values:
        return "unknown"
    return "observed"


def _value_source(
    markers: Mapping[str, bool],
    replacement_pairs: list[tuple[int, int]],
    zone_transfer: Mapping[str, object],
    trusted_values: bool,
) -> str:
    if any(markers.values()) or replacement_pairs or zone_transfer.get("semantic_hints"):
        return "derived"
    if trusted_values:
        return "observed"
    return "unknown"


def _confidence(degradation_flags: list[str], trusted_values: bool) -> str:
    if degradation_flags:
        return "low"
    if trusted_values:
        return "high"
    return "unknown"


def _normalized_int(value: object) -> int | None:
    values = api_common.normalize_int_list([value])
    if values:
        return values[0]
    return None


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _extend_unique(target: list[Any], values: list[Any]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def _append_flag(target: list[str], flag: str) -> None:
    if flag not in target:
        target.append(flag)
