from __future__ import annotations

import json
from copy import deepcopy

from mythic_edge_parser.parsers.gre.annotations import (
    ANNOTATION_COLLECTION_OBJECT,
    ANNOTATION_RECORD_OBJECT,
    SCHEMA_VERSION,
    annotation_categories_for_instance,
    normalize_annotation_arrays,
    normalize_annotation_record,
    replacement_instance_ids,
)


def test_normalize_annotation_arrays_builds_collection_summaries_without_mutation() -> None:
    annotations = [
        {
            "id": "123",
            "type": ["AnnotationType_ObjectIdChanged"],
            "affectedIds": [11],
            "details": [
                {"key": "orig_id", "valueInt32": [11, "12"]},
                {"key": "new_id", "valueInt32": ["99", "100"]},
            ],
        },
        {
            "type": "AnnotationType_ZoneTransfer",
            "affectedIds": ["99", "99"],
            "details": [
                {"key": "category", "valueString": ["CastSpell", "PlayLand", "Resolve"]},
                {"key": "zone_src", "valueInt32": [31]},
                {"key": "zone_dest", "valueInt64": "27"},
            ],
        },
    ]
    persistent_annotations = [{"annotationId": "7", "type": ["AnnotationType_NewTurnStarted"]}]
    original_annotations = deepcopy(annotations)
    original_persistent_annotations = deepcopy(persistent_annotations)

    normalized = normalize_annotation_arrays(
        annotations=annotations,
        persistent_annotations=persistent_annotations,
        diff_deleted_persistent_annotation_ids=[20, "21", True, "bad", 22.1],
    )

    assert json.loads(json.dumps(normalized)) == normalized
    assert annotations == original_annotations
    assert persistent_annotations == original_persistent_annotations
    assert normalized["object"] == ANNOTATION_COLLECTION_OBJECT
    assert normalized["schema_version"] == SCHEMA_VERSION
    assert normalized["total_records"] == 3
    assert normalized["degraded_records"] == 0
    assert normalized["review_required"] is False
    assert normalized["source_arrays"] == {"annotations": 2, "persistent_annotations": 1}
    assert normalized["annotation_types"] == [
        "AnnotationType_ObjectIdChanged",
        "AnnotationType_ZoneTransfer",
        "AnnotationType_NewTurnStarted",
    ]
    assert normalized["marker_types"] == ["object_id_changed", "zone_transfer", "new_turn_started"]
    assert normalized["diff_deleted_persistent_annotation_ids"] == [20, 21]
    assert normalized["object_replacements"] == [
        {
            "original_instance_id": 11,
            "new_instance_id": 99,
            "source_array": "annotations",
            "source_index": 0,
            "confidence": "high",
        },
        {
            "original_instance_id": 12,
            "new_instance_id": 100,
            "source_array": "annotations",
            "source_index": 0,
            "confidence": "high",
        },
    ]
    assert normalized["zone_transfers"] == [
        {
            "affected_ids": [99, 99],
            "categories": ["CastSpell", "PlayLand", "Resolve"],
            "source_zone_ids": [31],
            "destination_zone_ids": [27],
            "semantic_hints": ["cast_hint", "land_play_hint", "resolve_hint"],
            "source_array": "annotations",
            "source_index": 1,
            "confidence": "medium",
        }
    ]
    assert annotation_categories_for_instance(normalized, 99) == ["CastSpell", "PlayLand", "Resolve"]
    assert replacement_instance_ids(normalized) == {11: 99, 12: 100}
    assert normalized["records"][2]["persistent"] is True
    assert normalized["records"][2]["source_evidence"] == "persistent_annotation"


def test_normalize_annotation_arrays_reports_malformed_sections_and_placeholder_records() -> None:
    normalized = normalize_annotation_arrays(
        annotations="not-a-list",
        persistent_annotations={"bad": "shape"},
        diff_deleted_persistent_annotation_ids="not-a-list",
    )

    assert normalized["records"] == []
    assert normalized["total_records"] == 0
    assert normalized["degraded_records"] == 0
    assert normalized["review_required"] is True
    assert normalized["degradation_flags"] == [
        "malformed_annotations_section",
        "malformed_persistent_annotations_section",
        "malformed_diff_deleted_persistent_annotation_ids",
    ]

    with_placeholder = normalize_annotation_arrays(annotations=[None], persistent_annotations=[])
    record = with_placeholder["records"][0]
    assert record["object"] == ANNOTATION_RECORD_OBJECT
    assert record["source_array"] == "annotations"
    assert record["source_index"] == 0
    assert record["persistent"] is False
    assert record["degradation_flags"] == ["malformed_annotation_record"]
    assert record["evidence_status"] == "degraded"
    assert record["confidence"] == "low"
    assert record["review_required"] is True


def test_normalize_annotation_record_normalizes_type_and_affected_id_boundaries() -> None:
    record = normalize_annotation_record(
        {
            "type": [" AnnotationType_Shuffle ", "AnnotationType_Shuffle", 0, None, "CustomType"],
            "affectedIds": [1, "2", " 3 ", True, False, 4.5, "-5", "bad", None, 2],
        },
        source_array="annotations",
        source_index=3,
    )

    assert record["type_names"] == ["AnnotationType_Shuffle", "CustomType"]
    assert record["primary_type"] == "AnnotationType_Shuffle"
    assert record["affected_ids"] == [1, 2, 3, 2]
    assert record["markers"]["shuffle"] is True
    assert "malformed_annotation_type" in record["degradation_flags"]
    assert record["evidence_status"] == "degraded"

    missing_type = normalize_annotation_record({}, source_array="annotations", source_index=0)
    assert missing_type["type_names"] == []
    assert missing_type["primary_type"] == ""
    assert "missing_annotation_type" in missing_type["degradation_flags"]
    assert missing_type["evidence_status"] == "degraded"

    malformed_affected_ids = normalize_annotation_record(
        {"type": "AnnotationType_Shuffle", "affected_ids": "bad"},
        source_array="annotations",
        source_index=0,
    )
    assert malformed_affected_ids["affected_ids"] == []
    assert "malformed_affected_ids" in malformed_affected_ids["degradation_flags"]


def test_normalize_annotation_record_normalizes_detail_value_types() -> None:
    record = normalize_annotation_record(
        {
            "type": "AnnotationType_UserActionTaken",
            "details": [
                {
                    "key": " count ",
                    "valueInt32": [1, "2", True, 3.4, "-1", " 4 "],
                    "valueInt64": "5",
                    "valueString": [" keep ", "", 3],
                    "valueBool": [True, False, 1, "true"],
                },
                {"key": "", "valueString": "bad"},
                "bad",
            ],
        },
        source_array="annotations",
        source_index=0,
    )

    detail = record["details"][0]
    assert detail == {
        "key": "count",
        "value_ints": [1, 2, 4, 5],
        "value_strings": ["keep"],
        "value_bools": [True, False],
        "degradation_flags": ["malformed_detail_string_value"],
    }
    assert record["detail_values"]["count"] == [1, 2, 4, 5, "keep", True, False]
    assert "malformed_detail_string_value" in record["degradation_flags"]
    assert "malformed_detail_key" in record["degradation_flags"]
    assert "malformed_annotation_detail" in record["degradation_flags"]
    assert record["evidence_status"] == "degraded"


def test_object_replacement_and_zone_transfer_degradation_boundaries() -> None:
    incomplete = normalize_annotation_record(
        {
            "type": "AnnotationType_ObjectIdChanged",
            "details": [{"key": "orig_id", "valueInt32": [11]}],
        },
        source_array="annotations",
        source_index=0,
    )

    assert incomplete["object_replacement"] == {"original_instance_id": "", "new_instance_id": ""}
    assert "incomplete_object_replacement" in incomplete["degradation_flags"]

    zone_transfer = normalize_annotation_record(
        {
            "type": "AnnotationType_ZoneTransfer",
            "affectedIds": [99],
            "details": [
                {"key": "category", "valueString": ["PlayLand", "CastSpell", "Resolve", "UnknownCategory"]},
                {"key": "zone_src", "valueInt32": ["31"]},
                {"key": "zone_dest", "valueInt32": ["27"]},
            ],
        },
        source_array="annotations",
        source_index=1,
    )

    assert zone_transfer["categories"] == ["PlayLand", "CastSpell", "Resolve", "UnknownCategory"]
    assert zone_transfer["zone_transfer"] == {
        "affected_ids": [99],
        "categories": ["PlayLand", "CastSpell", "Resolve", "UnknownCategory"],
        "source_zone_ids": [31],
        "destination_zone_ids": [27],
        "semantic_hints": ["land_play_hint", "cast_hint", "resolve_hint"],
    }
    assert "unknown_zone_transfer_category" not in zone_transfer["degradation_flags"]


def test_well_known_markers_normalize_without_inference() -> None:
    normalized = normalize_annotation_arrays(
        annotations=[
            {
                "type": [
                    "AnnotationType_ResolutionStart",
                    "AnnotationType_ResolutionComplete",
                    "AnnotationType_RevealedCardDeleted",
                ]
            },
            {"type": "AnnotationType_Shuffle"},
            {"type": "AnnotationType_UserActionTaken"},
            {"type": "AnnotationType_ManaPaid"},
            {"type": "AnnotationType_AbilityInstanceDeleted"},
            {"type": "AnnotationType_NewTurnStarted"},
        ],
        persistent_annotations=[],
    )

    assert normalized["marker_types"] == [
        "resolution_start",
        "resolution_complete",
        "revealed_card_deleted",
        "shuffle",
        "user_action_taken",
        "mana_paid",
        "ability_instance_deleted",
        "new_turn_started",
    ]
    assert normalized["total_records"] == 6
    assert normalized["degraded_records"] == 0
    assert all(record["source_evidence"] == "annotation" for record in normalized["records"])
