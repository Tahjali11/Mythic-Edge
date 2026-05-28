from __future__ import annotations

from copy import deepcopy

from mythic_edge_parser.app.opponent_card_observations import (
    OPPONENT_CARD_OBSERVATION_OBJECT,
    OPPONENT_CARD_OBSERVATIONS_OBJECT,
    SCHEMA_VERSION,
    build_opponent_card_observation,
    build_opponent_card_observations_payload,
)


def _opponent_spell_entry() -> dict:
    return {
        "timestamp": "2026-05-18T00:00:00+00:00",
        "match_id": "match-observed",
        "game_number": 1,
        "game_state_id": 123,
        "turn_number": 4,
        "action_type": "spell_cast",
        "cast_mode": "",
        "instance_id": 456,
        "grp_id": 789,
        "observed_grp_id": 789,
        "overlay_grp_id": "",
        "object_source_grp_id": "",
        "parent_id": "",
        "identity_hint_source": "direct_grp_id",
        "actor_relation": "opponent",
        "actor_seat_id": 2,
        "local_seat_id": 1,
        "card_name": "Visible Spell",
        "display_name": "Visible Spell",
        "resolution_status": "confirmed",
        "name_resolution_source": "grp_id_catalog",
        "layout": "",
        "card_faces": [],
        "from_zone_type": "ZoneType_Hand",
        "to_zone_type": "ZoneType_Stack",
        "raw_action_types": ["ActionType_Cast@seat2"],
        "annotation_types": [],
        "annotation_categories": [],
    }


def test_build_opponent_card_observation_for_visible_spell_preserves_parser_evidence() -> None:
    entry = _opponent_spell_entry()
    original = deepcopy(entry)

    observation = build_opponent_card_observation(entry)

    assert entry == original
    assert observation == {
        "object": OPPONENT_CARD_OBSERVATION_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "match_id": "match-observed",
        "game_number": 1,
        "game_state_id": 123,
        "timestamp": "2026-05-18T00:00:00+00:00",
        "turn_number": 4,
        "actor_relation": "opponent",
        "actor_seat_id": 2,
        "local_seat_id": 1,
        "instance_id": 456,
        "grp_id": 789,
        "observed_grp_id": 789,
        "overlay_grp_id": "",
        "object_source_grp_id": "",
        "parent_id": "",
        "identity_hint_source": "direct_grp_id",
        "card_name": "Visible Spell",
        "display_name": "Visible Spell",
        "resolution_status": "confirmed",
        "name_resolution_source": "grp_id_catalog",
        "layout": "",
        "card_faces": [],
        "action_type": "spell_cast",
        "cast_mode": "",
        "source_evidence": "action_array",
        "evidence_status": "observed",
        "value_source": "observed",
        "confidence": "high",
        "visibility": "action_visible",
        "from_zone_type": "ZoneType_Hand",
        "to_zone_type": "ZoneType_Stack",
        "raw_action_types": ["ActionType_Cast@seat2"],
        "annotation_types": [],
        "annotation_categories": [],
        "degradation_flags": [],
        "review_required": False,
    }


def test_build_opponent_card_observation_derives_actor_seat_from_action_array() -> None:
    entry = _opponent_spell_entry()
    entry.pop("actor_seat_id")

    observation = build_opponent_card_observation(entry)

    assert observation is not None
    assert observation["actor_seat_id"] == 2
    assert observation["source_evidence"] == "action_array"
    assert observation["confidence"] == "high"


def test_observation_preserves_observed_and_canonical_identity_when_they_differ() -> None:
    entry = _opponent_spell_entry()
    entry["grp_id"] = 100
    entry["observed_grp_id"] = 200
    entry["overlay_grp_id"] = 300
    entry["object_source_grp_id"] = 100
    entry["parent_id"] = 99
    entry["identity_hint_source"] = ""

    observation = build_opponent_card_observation(entry)

    assert observation is not None
    assert observation["grp_id"] == 100
    assert observation["observed_grp_id"] == 200
    assert observation["overlay_grp_id"] == 300
    assert observation["object_source_grp_id"] == 100
    assert observation["parent_id"] == 99
    assert observation["identity_hint_source"] == "object_source_grp_id"


def test_non_opponent_entries_do_not_emit_observations_and_missing_seats_are_degraded() -> None:
    local_entry = _opponent_spell_entry()
    local_entry["actor_relation"] = "local"
    missing_local_seat = _opponent_spell_entry()
    missing_local_seat.pop("local_seat_id")
    missing_actor_seat = _opponent_spell_entry()
    missing_actor_seat.pop("actor_seat_id")
    missing_actor_seat["raw_action_types"] = []

    assert build_opponent_card_observation(local_entry) is None
    assert build_opponent_card_observation({"actor_relation": "unknown"}) is None
    assert build_opponent_card_observation("not-a-mapping") is None  # type: ignore[arg-type]

    missing_local = build_opponent_card_observation(missing_local_seat)
    missing_actor = build_opponent_card_observation(missing_actor_seat)
    assert missing_local is not None
    assert missing_local["actor_seat_id"] == 2
    assert missing_local["local_seat_id"] == ""
    assert missing_local["evidence_status"] == "degraded"
    assert missing_local["value_source"] == "unknown"
    assert missing_local["confidence"] == "low"
    assert missing_local["degradation_flags"] == ["missing_seat_mapping"]

    assert missing_actor is not None
    assert missing_actor["actor_seat_id"] == ""
    assert missing_actor["local_seat_id"] == 1
    assert missing_actor["evidence_status"] == "degraded"
    assert missing_actor["degradation_flags"] == ["missing_seat_mapping"]


def test_hidden_draw_from_library_to_hand_does_not_emit_clean_observation() -> None:
    entry = _opponent_spell_entry()
    entry["action_type"] = "card_drawn"
    entry["from_zone_type"] = "ZoneType_Library"
    entry["to_zone_type"] = "ZoneType_Hand"
    entry["raw_action_types"] = ["ActionType_Draw@seat2"]

    assert build_opponent_card_observation(entry) is None


def test_missing_card_identity_emits_degraded_review_observation_without_guessing() -> None:
    entry = _opponent_spell_entry()
    entry["grp_id"] = ""
    entry["observed_grp_id"] = ""
    entry["card_name"] = ""
    entry["display_name"] = ""
    entry["resolution_status"] = ""

    observation = build_opponent_card_observation(entry)

    assert observation is not None
    assert observation["grp_id"] == ""
    assert observation["card_name"] == ""
    assert observation["display_name"] == ""
    assert observation["resolution_status"] == "unresolved"
    assert observation["evidence_status"] == "degraded"
    assert observation["value_source"] == "unknown"
    assert observation["confidence"] == "low"
    assert observation["degradation_flags"] == [
        "missing_card_identity",
        "name_resolution_unresolved",
    ]
    assert observation["review_required"] is True


def test_candidate_and_contradicted_names_remain_lower_confidence_enrichment() -> None:
    candidate_entry = _opponent_spell_entry()
    candidate_entry["card_name"] = "Candidate Card"
    candidate_entry["display_name"] = "Candidate Card? [grpId 789]"
    candidate_entry["resolution_status"] = "candidate"

    contradicted_entry = _opponent_spell_entry()
    contradicted_entry["card_name"] = "Contradicted Card"
    contradicted_entry["display_name"] = "[grpId 789]"
    contradicted_entry["resolution_status"] = "contradicted"

    candidate = build_opponent_card_observation(candidate_entry)
    contradicted = build_opponent_card_observation(contradicted_entry)

    assert candidate is not None
    assert candidate["card_name"] == ""
    assert candidate["display_name"] == "Candidate Card? [grpId 789]"
    assert candidate["resolution_status"] == "candidate"
    assert candidate["evidence_status"] == "observed"
    assert candidate["confidence"] == "medium"
    assert candidate["degradation_flags"] == ["name_resolution_candidate"]
    assert candidate["review_required"] is True

    assert contradicted is not None
    assert contradicted["card_name"] == ""
    assert contradicted["resolution_status"] == "contradicted"
    assert contradicted["evidence_status"] == "conflict"
    assert contradicted["confidence"] == "low"
    assert contradicted["degradation_flags"] == ["name_resolution_contradicted"]
    assert contradicted["review_required"] is True


def test_contradictory_actor_seat_evidence_is_review_required_conflict() -> None:
    entry = _opponent_spell_entry()
    entry["actor_seat_id"] = 3
    entry["raw_action_types"] = ["ActionType_Cast@seat2"]

    observation = build_opponent_card_observation(entry)

    assert observation is not None
    assert observation["actor_seat_id"] == 3
    assert observation["evidence_status"] == "conflict"
    assert observation["value_source"] == "conflict"
    assert observation["confidence"] == "low"
    assert observation["degradation_flags"] == ["action_seat_conflict"]
    assert observation["review_required"] is True


def test_unresolved_known_id_preserves_id_and_uses_placeholder_display_name() -> None:
    entry = _opponent_spell_entry()
    entry["card_name"] = ""
    entry["display_name"] = ""
    entry["resolution_status"] = "unresolved"

    observation = build_opponent_card_observation(entry)

    assert observation is not None
    assert observation["grp_id"] == 789
    assert observation["display_name"] == "[grpId 789]"
    assert observation["evidence_status"] == "observed"
    assert observation["confidence"] == "high"
    assert observation["degradation_flags"] == []
    assert observation["review_required"] is False


def test_build_opponent_card_observations_payload_counts_degraded_and_review_entries() -> None:
    clean = _opponent_spell_entry()
    local = _opponent_spell_entry()
    local["actor_relation"] = "local"
    degraded = _opponent_spell_entry()
    degraded["grp_id"] = ""
    degraded["observed_grp_id"] = ""
    degraded["display_name"] = ""
    degraded["card_name"] = ""

    payload = build_opponent_card_observations_payload(
        [clean, local, degraded, "not-a-mapping"],  # type: ignore[list-item]
        match_id="match-observed",
    )

    assert payload["object"] == OPPONENT_CARD_OBSERVATIONS_OBJECT
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["match_id"] == "match-observed"
    assert payload["total_observations"] == 2
    assert payload["degraded_observations"] == 1
    assert payload["review_required"] is True
    assert [observation["actor_relation"] for observation in payload["observations"]] == ["opponent", "opponent"]
