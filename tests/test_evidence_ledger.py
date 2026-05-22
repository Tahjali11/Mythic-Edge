from __future__ import annotations

import builtins
import copy
import importlib
import json

from mythic_edge_parser.app import evidence_ledger

CONTRACTED_TIER1_FIELDS = [
    "match_id",
    "player_team",
    "opponent_team",
    "local_system_seat_id",
    "participant_team_mapping",
    "match_started_at",
    "match_finished_at",
    "match_winner_team",
    "match_result",
    "match_sync_status",
    "games_won",
    "games_lost",
    "total_games",
    "match_win_flag",
    "game_win_rate",
]

CONTRACTED_TIER1_ENTRY_IDS = {
    "tier1.match_identity.match_id",
    "tier1.participants.player_team",
    "tier1.participants.opponent_team",
    "tier1.participants.local_system_seat_id",
    "tier1.participants.participant_team_mapping",
    "tier1.match_lifecycle.match_started_at",
    "tier1.match_lifecycle.match_finished_at",
    "tier1.match_result.match_winner_team",
    "tier1.match_result.match_result",
    "tier1.match_lifecycle.match_sync_status",
    "tier1.match_aggregates.games_won",
    "tier1.match_aggregates.games_lost",
    "tier1.match_aggregates.total_games",
    "tier1.match_aggregates.match_win_flag",
    "tier1.match_aggregates.game_win_rate",
}

CONTRACTED_AGGREGATE_FIELDS = {
    "games_won",
    "games_lost",
    "total_games",
    "match_win_flag",
    "game_win_rate",
}

CONTRACTED_PARTICIPANT_FIELDS = {
    "player_team",
    "opponent_team",
    "local_system_seat_id",
    "participant_team_mapping",
}

CONTRACTED_PARTICIPANT_ENTRY_IDS = {
    "tier1.participants.player_team",
    "tier1.participants.opponent_team",
    "tier1.participants.local_system_seat_id",
    "tier1.participants.participant_team_mapping",
}

CONTRACTED_TIER3_FIELDS = [
    "game_number",
    "game1_winner_team",
    "game2_winner_team",
    "game3_winner_team",
    "game1_result",
    "game2_result",
    "game3_result",
    "game1_starting_player",
    "game2_starting_player",
    "game3_starting_player",
    "game1_play_draw",
    "game2_play_draw",
    "game3_play_draw",
    "game1_mulligans",
    "game2_mulligans",
    "game3_mulligans",
    "total_mulligans",
    "game1_opening_hand_size",
    "game2_opening_hand_size",
    "game3_opening_hand_size",
    "game1_opening_hand",
    "game2_opening_hand",
    "game3_opening_hand",
    "game1_mulliganed_away",
    "game2_mulliganed_away",
    "game3_mulliganed_away",
    "game1_turn_count",
    "game2_turn_count",
    "game3_turn_count",
    "game1_first_event_time",
    "game2_first_event_time",
    "game3_first_event_time",
    "game1_last_event_time",
    "game2_last_event_time",
    "game3_last_event_time",
    "game1_duration_seconds",
    "game2_duration_seconds",
    "game3_duration_seconds",
    "game1_pre_postboard",
    "game2_pre_postboard",
    "game3_pre_postboard",
]

CONTRACTED_TIER3_ENTRY_IDS = {
    "tier3.game_results.game_number",
    "tier3.game_results.game1_winner_team",
    "tier3.game_results.game2_winner_team",
    "tier3.game_results.game3_winner_team",
    "tier3.game_results.game1_result",
    "tier3.game_results.game2_result",
    "tier3.game_results.game3_result",
    "tier3.play_draw.game1_starting_player",
    "tier3.play_draw.game2_starting_player",
    "tier3.play_draw.game3_starting_player",
    "tier3.play_draw.game1_play_draw",
    "tier3.play_draw.game2_play_draw",
    "tier3.play_draw.game3_play_draw",
    "tier3.mulligans.game1_mulligans",
    "tier3.mulligans.game2_mulligans",
    "tier3.mulligans.game3_mulligans",
    "tier3.mulligans.total_mulligans",
    "tier3.opening_hand.game1_opening_hand_size",
    "tier3.opening_hand.game2_opening_hand_size",
    "tier3.opening_hand.game3_opening_hand_size",
    "tier3.opening_hand.game1_opening_hand",
    "tier3.opening_hand.game2_opening_hand",
    "tier3.opening_hand.game3_opening_hand",
    "tier3.opening_hand.game1_mulliganed_away",
    "tier3.opening_hand.game2_mulliganed_away",
    "tier3.opening_hand.game3_mulliganed_away",
    "tier3.turn_count.game1_turn_count",
    "tier3.turn_count.game2_turn_count",
    "tier3.turn_count.game3_turn_count",
    "tier3.game_timing.game1_first_event_time",
    "tier3.game_timing.game2_first_event_time",
    "tier3.game_timing.game3_first_event_time",
    "tier3.game_timing.game1_last_event_time",
    "tier3.game_timing.game2_last_event_time",
    "tier3.game_timing.game3_last_event_time",
    "tier3.game_duration.game1_duration_seconds",
    "tier3.game_duration.game2_duration_seconds",
    "tier3.game_duration.game3_duration_seconds",
    "tier3.pre_postboard.game1_pre_postboard",
    "tier3.pre_postboard.game2_pre_postboard",
    "tier3.pre_postboard.game3_pre_postboard",
}

CONTRACTED_PLAY_DRAW_ENTRY_IDS = {
    "tier3.play_draw.game1_starting_player",
    "tier3.play_draw.game2_starting_player",
    "tier3.play_draw.game3_starting_player",
    "tier3.play_draw.game1_play_draw",
    "tier3.play_draw.game2_play_draw",
    "tier3.play_draw.game3_play_draw",
}

CONTRACTED_PLAY_DRAW_FIELDS = {
    "game1_starting_player",
    "game2_starting_player",
    "game3_starting_player",
    "game1_play_draw",
    "game2_play_draw",
    "game3_play_draw",
}

CONTRACTED_MULLIGAN_ENTRY_IDS = {
    "tier3.mulligans.game1_mulligans",
    "tier3.mulligans.game2_mulligans",
    "tier3.mulligans.game3_mulligans",
    "tier3.mulligans.total_mulligans",
}

CONTRACTED_MULLIGAN_FIELDS = {
    "game1_mulligans",
    "game2_mulligans",
    "game3_mulligans",
    "total_mulligans",
}

CONTRACTED_OPENING_HAND_ENTRY_IDS = {
    "tier3.opening_hand.game1_opening_hand_size",
    "tier3.opening_hand.game2_opening_hand_size",
    "tier3.opening_hand.game3_opening_hand_size",
    "tier3.opening_hand.game1_opening_hand",
    "tier3.opening_hand.game2_opening_hand",
    "tier3.opening_hand.game3_opening_hand",
    "tier3.opening_hand.game1_mulliganed_away",
    "tier3.opening_hand.game2_mulliganed_away",
    "tier3.opening_hand.game3_mulliganed_away",
}

CONTRACTED_OPENING_HAND_FIELDS = {
    "game1_opening_hand_size",
    "game2_opening_hand_size",
    "game3_opening_hand_size",
    "game1_opening_hand",
    "game2_opening_hand",
    "game3_opening_hand",
    "game1_mulliganed_away",
    "game2_mulliganed_away",
    "game3_mulliganed_away",
}

CONTRACTED_TURN_COUNT_ENTRY_IDS = {
    "tier3.turn_count.game1_turn_count",
    "tier3.turn_count.game2_turn_count",
    "tier3.turn_count.game3_turn_count",
}

CONTRACTED_TURN_COUNT_FIELDS = {
    "game1_turn_count",
    "game2_turn_count",
    "game3_turn_count",
}

CONTRACTED_GAME_TIMING_ENTRY_IDS = {
    "tier3.game_timing.game1_first_event_time",
    "tier3.game_timing.game2_first_event_time",
    "tier3.game_timing.game3_first_event_time",
    "tier3.game_timing.game1_last_event_time",
    "tier3.game_timing.game2_last_event_time",
    "tier3.game_timing.game3_last_event_time",
}

CONTRACTED_GAME_DURATION_ENTRY_IDS = {
    "tier3.game_duration.game1_duration_seconds",
    "tier3.game_duration.game2_duration_seconds",
    "tier3.game_duration.game3_duration_seconds",
}

CONTRACTED_TIMING_DURATION_FIELDS = {
    "game1_first_event_time",
    "game2_first_event_time",
    "game3_first_event_time",
    "game1_last_event_time",
    "game2_last_event_time",
    "game3_last_event_time",
    "game1_duration_seconds",
    "game2_duration_seconds",
    "game3_duration_seconds",
}

CONTRACTED_PRE_POSTBOARD_ENTRY_IDS = {
    "tier3.pre_postboard.game1_pre_postboard",
    "tier3.pre_postboard.game2_pre_postboard",
    "tier3.pre_postboard.game3_pre_postboard",
}

CONTRACTED_PRE_POSTBOARD_FIELDS = {
    "game1_pre_postboard",
    "game2_pre_postboard",
    "game3_pre_postboard",
}

CONTRACTED_TIER3_DEFERRED_FIELDS = {
    "deck_state",
}

CONTRACTED_TIER4_FIELDS = [
    "sideboarding_entered",
    "submit_deck_seen",
    "submitted_deck_cards",
]

CONTRACTED_TIER4_SIGNAL_ENTRY_IDS = {
    "tier4.sideboarding_submit_deck.sideboarding_entered",
    "tier4.sideboarding_submit_deck.submit_deck_seen",
}

CONTRACTED_TIER4_ENTRY_IDS = {
    *CONTRACTED_TIER4_SIGNAL_ENTRY_IDS,
    "tier4.submitted_deck_cards.submitted_deck_cards",
}

CONTRACTED_TIER4_DEFERRED_FIELDS: set[str] = set()

CONTRACTED_TIER4_DECK_STATE_BOUNDARY_FORBIDDEN_OUTPUT_FIELDS = {
    "deck_state",
    "active_deck_state",
    "deck_identity",
    "deck_name",
    "deck_id",
    "sideboard_delta",
    "card_name",
    "collection_ownership",
    "archetype",
    "matchup_plan",
    "gameplay_advice",
    "player_mistake_label",
}

CONTRACTED_TIER4_DECK_STATE_BOUNDARY_NOTE_FRAGMENTS = (
    "Issue #161 keeps broader deck_state deferred",
    "there is no tier4.deck_state entry",
    "no deck_state seed field",
    "Runtime active submitted-deck artifacts",
    "runtime active deck state",
    "active deck profiles",
    "collection/deck matching",
    "card catalog lookup",
    "local decklists",
    "GRP candidate reports",
    "not parser truth for broad deck state",
    "requires review or degraded provenance",
    "Deck names, deck IDs, sideboard deltas",
    "card names, collection ownership",
    "model-provider output, and AI remain outside parser truth",
)


def _entries_by_id() -> dict[str, dict[str, object]]:
    return {entry["entry_id"]: entry for entry in evidence_ledger.iter_ledger_entries()}


def _family(output_family: str) -> dict[str, object]:
    families = evidence_ledger.build_player_log_evidence_ledger()["output_families"]
    return next(family for family in families if family["output_family"] == output_family)


def _tier1_family() -> dict[str, object]:
    return _family("match_identity_and_lifecycle")


def _tier3_family() -> dict[str, object]:
    return _family("game_level_facts")


def _tier4_family() -> dict[str, object]:
    return _family("sideboarding_and_deck_state")


def _signal_ids(entry: dict[str, object], key: str) -> set[str]:
    return {signal["signal_id"] for signal in entry[key]}


def _all_signal_ids(entry: dict[str, object]) -> set[str]:
    return _signal_ids(entry, "direct_evidence") | _signal_ids(entry, "fallback_evidence")


def test_vocabulary_constants_match_contract_slice() -> None:
    assert evidence_ledger.VALUE_SOURCES == (
        "observed",
        "derived",
        "inferred",
        "unknown",
        "conflict",
        "legacy_enriched",
    )
    assert evidence_ledger.CONFIDENCE_LEVELS == ("high", "medium", "low", "unknown")
    assert evidence_ledger.FINALITY_LABELS == ("live", "provisional", "final", "reconciled")
    assert evidence_ledger.INVARIANT_STATUSES == (
        "passed",
        "failed",
        "not_applicable",
        "not_checked",
        "degraded",
    )
    assert evidence_ledger.DRIFT_FLAGS == (
        "missing_expected_event_family",
        "missing_expected_payload_path",
        "changed_signal_type",
        "new_unknown_event_family",
        "new_unknown_payload_path",
        "fallback_used",
        "weak_fallback_used",
        "conflicting_evidence",
        "invariant_failed",
        "schema_snapshot_missing",
        "fixture_gap",
        "parser_exception",
        "transport_failure",
        "workbook_drift",
        "deployment_drift",
        "sensitive_evidence_redacted",
    )


def test_build_ledger_returns_stable_top_level_shape() -> None:
    ledger = evidence_ledger.build_player_log_evidence_ledger()

    assert ledger["object"] == evidence_ledger.LEDGER_OBJECT
    assert ledger["schema_version"] == evidence_ledger.LEDGER_SCHEMA_VERSION
    assert ledger["ledger_version"] == evidence_ledger.LEDGER_VERSION
    assert ledger["source_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/128"
    assert ledger["parent_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/11"
    assert ledger["related_adrs"] == ["docs/decisions/ADR-0003-player-log-drift-policy.md"]
    assert ledger["branch_target"] == "codex/parser-reliability-intelligence"
    assert ledger["privacy"] == {
        "raw_private_logs_included": False,
        "raw_payload_values_included": False,
        "source_paths_are_repo_relative_or_symbolic": True,
    }
    assert ledger["vocabulary"] == {
        "value_sources": list(evidence_ledger.VALUE_SOURCES),
        "confidence_levels": list(evidence_ledger.CONFIDENCE_LEVELS),
        "finality_labels": list(evidence_ledger.FINALITY_LABELS),
        "drift_flags": list(evidence_ledger.DRIFT_FLAGS),
        "invariant_statuses": list(evidence_ledger.INVARIANT_STATUSES),
    }
    assert "generated_at" not in ledger


def test_output_family_registry_contains_required_seven_families() -> None:
    families = evidence_ledger.build_player_log_evidence_ledger()["output_families"]

    assert [(family["tier"], family["output_family"], family["status"]) for family in families] == [
        (1, "match_identity_and_lifecycle", "seeded_sample"),
        (2, "queue_format_rank_event_context", "registered_future"),
        (3, "game_level_facts", "seeded_sample"),
        (4, "sideboarding_and_deck_state", "seeded_sample"),
        (5, "card_identity_and_gameplay_actions", "registered_future"),
        (6, "runtime_health_and_drift_detection", "registered_future"),
        (7, "derived_analytics_outputs", "registered_future"),
    ]
    tier1 = _tier1_family()
    assert tier1["seed_fields"] == CONTRACTED_TIER1_FIELDS
    assert tier1["future_fields"] == []
    assert CONTRACTED_PARTICIPANT_FIELDS.issubset(tier1["seed_fields"])
    assert any("Issue #137 maps participant" in item for item in tier1["notes"])

    tier3 = _tier3_family()
    assert tier3["seed_fields"] == CONTRACTED_TIER3_FIELDS
    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert CONTRACTED_PLAY_DRAW_FIELDS.issubset(tier3["seed_fields"])
    assert "play_draw" not in tier3["future_fields"]
    assert "starting_player" not in tier3["future_fields"]
    assert CONTRACTED_MULLIGAN_FIELDS.issubset(tier3["seed_fields"])
    assert "mulligans" not in tier3["future_fields"]
    assert CONTRACTED_OPENING_HAND_FIELDS.issubset(tier3["seed_fields"])
    assert "opening_hand" not in tier3["future_fields"]
    assert CONTRACTED_TURN_COUNT_FIELDS.issubset(tier3["seed_fields"])
    assert "turn_count" not in tier3["future_fields"]
    assert CONTRACTED_TIMING_DURATION_FIELDS.issubset(tier3["seed_fields"])
    assert "game_timing" not in tier3["future_fields"]
    assert "game_duration" not in tier3["future_fields"]
    assert CONTRACTED_PRE_POSTBOARD_FIELDS.issubset(tier3["seed_fields"])
    assert "pre_postboard" not in tier3["future_fields"]
    assert any("match-scope results are not promoted" in item for item in tier3["notes"])
    assert any("Issue #139 maps starting-player and play/draw" in item for item in tier3["notes"])
    assert any("Issue #140 maps per-game and total mulligan" in item for item in tier3["notes"])
    assert any("Issue #143 maps opening-hand size" in item for item in tier3["notes"])
    assert any("Issue #145 maps turn-count provenance" in item for item in tier3["notes"])
    assert any("Issue #147 maps game timing and duration" in item for item in tier3["notes"])
    assert any("Issue #149 maps pre/postboard provenance" in item for item in tier3["notes"])
    assert "sideboarding" not in tier3["future_fields"]

    tier4 = _tier4_family()
    assert tier4["seed_fields"] == CONTRACTED_TIER4_FIELDS
    assert set(tier4["future_fields"]) == CONTRACTED_TIER4_DEFERRED_FIELDS
    assert "sideboarding_entered" not in tier4["future_fields"]
    assert "submit_deck_seen" not in tier4["future_fields"]
    assert "submitted_deck_cards" not in tier4["future_fields"]
    assert any("Issue #151 maps sideboarding_entered" in item for item in tier4["notes"])
    assert any("Issue #159 maps submitted_deck_cards" in item for item in tier4["notes"])
    assert any("Counts and submitted-deck signature" in item for item in tier4["notes"])
    assert any("Issue #161 keeps broader deck_state deferred" in item for item in tier4["notes"])


def test_seed_entry_maps_match_id_evidence_signals() -> None:
    entry = _entries_by_id()["tier1.match_identity.match_id"]

    assert entry["entry_id"] == "tier1.match_identity.match_id"
    assert entry["tier"] == 1
    assert entry["output_family"] == "match_identity_and_lifecycle"
    assert entry["output_field"] == "match_id"
    assert entry["display_name"] == "MTGA Match ID"
    assert entry["parser_owner"] == "src/mythic_edge_parser/app/state.py"
    assert entry["model_surface"] == "MatchSummary.to_match_log_row"
    assert entry["downstream_surfaces"] == ["MatchLogRow", "GameLogRow", "match_history"]
    assert entry["parser_managed_truth"] is True
    assert entry["coverage_status"] == "seeded_sample"
    assert entry["recommended_review_modules"] == [
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/parsers/match_state.py",
        "src/mythic_edge_parser/parsers/gre/game_state.py",
        "src/mythic_edge_parser/parsers/gre/game_result.py",
    ]
    assert {signal["signal_id"] for signal in entry["direct_evidence"]} == {
        "match_state.match_id",
        "game_state.identity.match_id",
        "game_result.identity.match_id",
    }
    assert entry["fallback_evidence"][0]["signal_id"] == "parser_context.current_match_id"
    assert entry["fallback_evidence"][0]["value_source_when_used"] == "derived"


def test_tier1_match_lifecycle_and_aggregate_entries_are_mapped() -> None:
    entries = _entries_by_id()
    output_fields = {entry["output_field"] for entry in entries.values()}

    assert set(entries) == CONTRACTED_TIER1_ENTRY_IDS | CONTRACTED_TIER3_ENTRY_IDS | CONTRACTED_TIER4_ENTRY_IDS
    assert CONTRACTED_TIER1_ENTRY_IDS.issubset(entries)
    assert all(entries[entry_id]["tier"] == 1 for entry_id in CONTRACTED_TIER1_ENTRY_IDS)
    assert all(
        entries[entry_id]["output_family"] == "match_identity_and_lifecycle"
        for entry_id in CONTRACTED_TIER1_ENTRY_IDS
    )
    assert set(CONTRACTED_TIER1_FIELDS).issubset(output_fields)
    assert CONTRACTED_AGGREGATE_FIELDS.issubset(output_fields)


def test_participant_entries_are_mapped_and_validate() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_PARTICIPANT_ENTRY_IDS.issubset(entries)
    for entry_id in CONTRACTED_PARTICIPANT_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 1
        assert entry["output_family"] == "match_identity_and_lifecycle"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True
        assert evidence_ledger.validate_ledger_entry(entry) == []


def test_player_team_entry_documents_sources_unknowns_and_context_limits() -> None:
    entry = _entries_by_id()["tier1.participants.player_team"]

    assert entry["display_name"] == "player_team"
    assert entry["model_surface"] == "MatchSummary.player_team"
    assert _signal_ids(entry, "direct_evidence") == {
        "match_state.players.selected_local_player_team",
        "game_state.system_seat_ids.local_player_team",
        "client_action.local_player_team",
    }
    assert _signal_ids(entry, "fallback_evidence") == {
        "parser_context.current_player_team",
        "parser_state.match_summary.player_team",
    }
    assert "player_facing_results_require_known_non_conflicting_player_team" in entry["invariant_checks"]
    assert "known_winner_does_not_repair_missing_player_team" in entry["invariant_checks"]
    assert any(
        "whitespace-only strings, zero, string zero, and booleans" in item
        for item in entry["degradation_behavior"]
    )
    assert any("LOCAL_PLAYER_INDEX" in item for item in entry["notes"])
    assert all(signal["privacy_class"] == "path_only_no_values" for signal in entry["direct_evidence"])


def test_opponent_team_entry_is_derived_from_player_team_only() -> None:
    entry = _entries_by_id()["tier1.participants.opponent_team"]

    assert entry["value_source_policy"]["direct"] == "derived"
    assert entry["direct_evidence"][0]["signal_id"] == "parser_state.match_summary.opponent_team"
    assert entry["fallback_evidence"][0]["signal_id"] == "ledger.tier1.participants.player_team_dependency"
    assert entry["fallback_evidence"][0]["normalized_payload_path"] == "ledger.entries[tier1.participants.player_team]"
    assert "opponent_team_derived_only_from_known_player_team" in entry["invariant_checks"]
    assert "opponent_team_not_guessed_when_player_team_unknown" in entry["invariant_checks"]
    assert any("not 1 or 2" in item for item in entry["degradation_behavior"])
    assert any("hidden cards, decklists, archetypes, or advice" in item for item in entry["degradation_behavior"])


def test_local_system_seat_entry_documents_game_state_match_state_and_degradation() -> None:
    entry = _entries_by_id()["tier1.participants.local_system_seat_id"]
    signals = {
        signal["signal_id"]: signal
        for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
    }

    assert signals["game_state.system_seat_ids.local_system_seat"]["raw_payload_path"] == (
        "greToClientMessages[].systemSeatIds[0]"
    )
    assert signals["match_state.players.selected_local_player_seat"]["raw_payload_path"] == (
        "matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.reservedPlayers[].systemSeatId"
    )
    assert signals["gameplay_actions.local_seat_id"]["normalized_payload_path"] == "GameplayGameState.local_seat_id"
    assert "local_private_zone_interpretation_requires_known_local_seat" in entry["invariant_checks"]
    assert "actor_relation_requires_known_local_and_actor_seats" in entry["invariant_checks"]
    assert any("zero, string zero, and booleans are unknown" in item for item in entry["degradation_behavior"])


def test_participant_team_mapping_entry_documents_cross_surface_dependencies() -> None:
    entry = _entries_by_id()["tier1.participants.participant_team_mapping"]

    assert _signal_ids(entry, "direct_evidence") == {
        "match_state.players.participant_team_mapping",
        "game_state.players.participant_team_mapping",
    }
    assert _signal_ids(entry, "fallback_evidence") == {
        "client_action.participant_team_supplement",
        "parser_context.participant_team_carry_forward",
        "opponent_card_observations.missing_seat_mapping_dependency",
    }
    assert "participant_mapping_stays_parser_owned" in entry["invariant_checks"]
    assert "missing_mapping_degrades_player_relative_outputs" in entry["invariant_checks"]
    assert any("missing player_team or local_system_seat_id" in item for item in entry["degradation_behavior"])
    assert any("hidden cards, decklists, archetypes" in item for item in entry["degradation_behavior"])


def test_existing_entries_cite_participant_player_team_provenance() -> None:
    entries = _entries_by_id()
    dependent_entry_ids = {
        "tier1.match_result.match_result",
        "tier1.match_aggregates.games_won",
        "tier1.match_aggregates.games_lost",
        "tier1.match_aggregates.match_win_flag",
        "tier1.match_aggregates.game_win_rate",
        "tier3.game_results.game1_result",
        "tier3.game_results.game2_result",
        "tier3.game_results.game3_result",
    }

    for entry_id in dependent_entry_ids:
        entry = entries[entry_id]
        assert "ledger.tier1.participants.player_team_dependency" in _all_signal_ids(entry)
        assert any("Issue #137" in note for note in entry["notes"])


def test_lifecycle_time_entries_document_required_sources_and_aliases() -> None:
    entries = _entries_by_id()
    start = entries["tier1.match_lifecycle.match_started_at"]
    finish = entries["tier1.match_lifecycle.match_finished_at"]

    assert start["display_name"] == "MGTA Start Time"
    assert {signal["signal_id"] for signal in start["direct_evidence"]} == {
        "match_state.match_started.timestamp"
    }
    assert start["fallback_evidence"][0]["signal_id"] == "parser_state.match_summary.first_event_time"
    assert start["direct_evidence"][0]["value_source_when_used"] == "observed"
    assert start["fallback_evidence"][0]["value_source_when_used"] == "derived"

    assert finish["display_name"] == "MTGA End Time"
    assert {signal["signal_id"] for signal in finish["direct_evidence"]} == {
        "game_result.match_complete.timestamp",
        "match_state.match_complete.timestamp",
    }
    assert finish["fallback_evidence"][0]["signal_id"] == "parser_state.match_summary.last_event_time"
    assert any("live rows leave MTGA End Time blank" in item for item in finish["degradation_behavior"])


def test_match_winner_entry_documents_precedence_unknowns_and_fallback_gate() -> None:
    entry = _entries_by_id()["tier1.match_result.match_winner_team"]

    assert {signal["signal_id"] for signal in entry["direct_evidence"]} == {
        "game_result.results.match_scope_winner",
        "match_state.game_results.match_scope_winner",
    }
    assert entry["fallback_evidence"][0]["signal_id"] == "game_result.top_level_match_complete_winner"
    assert entry["fallback_evidence"][0]["confidence_when_used"] == "medium"
    assert "top_level_winner_fallback_requires_match_complete" in entry["invariant_checks"]
    assert "unknown_winner_values_do_not_overwrite_known_winner" in entry["invariant_checks"]
    assert any("0, and string 0 are unknown" in item for item in entry["degradation_behavior"])
    assert any("game-level result aggregation must not infer" in item for item in entry["degradation_behavior"])


def test_match_winner_game_result_evidence_paths_match_parser_raw_shape() -> None:
    entry = _entries_by_id()["tier1.match_result.match_winner_team"]
    signals = {
        signal["signal_id"]: signal
        for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
    }

    assert signals["game_result.results.match_scope_winner"]["raw_payload_path"] == (
        "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId"
    )
    assert signals["game_result.top_level_match_complete_winner"]["raw_payload_path"] == (
        "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId"
    )


def test_match_result_and_sync_status_are_derived_parser_state_entries() -> None:
    entries = _entries_by_id()
    result = entries["tier1.match_result.match_result"]
    sync_status = entries["tier1.match_lifecycle.match_sync_status"]

    assert result["display_name"] == "Match Win?"
    assert result["value_source_policy"]["direct"] == "derived"
    assert {signal["signal_id"] for signal in result["fallback_evidence"]} == {
        "parser_state.match_summary.match_winner_team_dependency",
        "parser_state.match_summary.player_team_dependency",
        "ledger.tier1.participants.player_team_dependency",
    }
    assert "match_result_not_directly_observed_as_win_loss" in result["invariant_checks"]

    assert sync_status["display_name"] == "MTGA Sync Status"
    assert sync_status["value_source_policy"]["direct"] == "derived"
    assert sync_status["direct_evidence"][0]["signal_id"] == "parser_state.match_summary_ready"
    assert {signal["signal_id"] for signal in sync_status["fallback_evidence"]} == {
        "parser_state.live_match_log_row",
        "models.match_summary.to_match_log_row.final_argument",
    }
    assert any("webhook delivery do not decide finality" in item for item in sync_status["degradation_behavior"])


def test_aggregate_entries_are_derived_matchsummary_metadata() -> None:
    entries = _entries_by_id()
    expected = {
        "tier1.match_aggregates.games_won": (
            "Games Won",
            "MatchSummary.game_wins",
            "parser_state.match_summary.game_wins",
        ),
        "tier1.match_aggregates.games_lost": (
            "Games Lost",
            "MatchSummary.game_losses",
            "parser_state.match_summary.game_losses",
        ),
        "tier1.match_aggregates.total_games": (
            "Total Games",
            "MatchSummary.total_games",
            "parser_state.match_summary.total_games",
        ),
        "tier1.match_aggregates.match_win_flag": (
            "Match Win Flag",
            "MatchSummary.match_win_flag",
            "parser_state.match_summary.match_win_flag",
        ),
        "tier1.match_aggregates.game_win_rate": (
            "Game Win %",
            "MatchSummary.game_win_rate",
            "parser_state.match_summary.game_win_rate",
        ),
    }

    for entry_id, (display_name, model_surface, direct_signal) in expected.items():
        entry = entries[entry_id]
        assert entry["display_name"] == display_name
        assert entry["model_surface"] == model_surface
        assert entry["parser_owner"] == "src/mythic_edge_parser/app/models.py"
        assert entry["value_source_policy"]["direct"] == "derived"
        assert entry["value_source_policy"]["fallback"] == "derived"
        assert entry["direct_evidence"][0]["signal_id"] == direct_signal
        assert entry["direct_evidence"][0]["value_source_when_used"] == "derived"
        assert "aggregate_fields_derived_not_observed" in entry["invariant_checks"]


def test_game_count_aggregate_entries_document_dependencies_and_blank_behavior() -> None:
    entries = _entries_by_id()
    games_won = entries["tier1.match_aggregates.games_won"]
    games_lost = entries["tier1.match_aggregates.games_lost"]
    total_games = entries["tier1.match_aggregates.total_games"]

    assert {signal["signal_id"] for signal in games_won["fallback_evidence"]} == {
        "parser_state.match_summary.game_winner_dependencies",
        "parser_state.match_summary.player_team_dependency",
        "ledger.tier1.participants.player_team_dependency",
        "parser_state.match_summary.total_games_display_dependency",
    }
    assert {signal["signal_id"] for signal in games_lost["fallback_evidence"]} == {
        "parser_state.match_summary.completed_game_dependencies",
        "parser_state.match_summary.game_wins_dependency",
        "parser_state.match_summary.player_team_dependency",
        "ledger.tier1.participants.player_team_dependency",
    }
    assert {signal["signal_id"] for signal in total_games["fallback_evidence"]} == {
        "parser_state.match_summary.game_wins_dependency",
        "parser_state.match_summary.game_losses_dependency",
    }

    assert "game_wins_not_greater_than_total_games" in games_won["invariant_checks"]
    assert "game_losses_not_greater_than_total_games" in games_lost["invariant_checks"]
    assert "games_won_plus_games_lost_equals_total_games" in total_games["invariant_checks"]
    assert any("workbook-facing Games Won is blank" in item for item in games_won["degradation_behavior"])
    assert any("workbook-facing Games Lost is blank" in item for item in games_lost["degradation_behavior"])
    assert any(
        "blank Total Games with no completed game evidence is expected" in item
        for item in total_games["degradation_behavior"]
    )


def test_match_win_flag_and_game_win_rate_document_dependency_invariants() -> None:
    entries = _entries_by_id()
    match_win_flag = entries["tier1.match_aggregates.match_win_flag"]
    game_win_rate = entries["tier1.match_aggregates.game_win_rate"]

    assert {signal["signal_id"] for signal in match_win_flag["fallback_evidence"]} == {
        "parser_state.match_summary.match_wl_dependency",
        "ledger.tier1.match_result.match_result_dependency",
        "ledger.tier1.participants.player_team_dependency",
    }
    assert "match_win_flag_agrees_with_match_result" in match_win_flag["invariant_checks"]
    assert "match_win_flag_blank_when_match_result_blank" in match_win_flag["invariant_checks"]
    assert "match_win_flag_not_inferred_from_game_aggregates" in match_win_flag["invariant_checks"]
    assert any("do not infer Match Win Flag" in item for item in match_win_flag["degradation_behavior"])

    assert {signal["signal_id"] for signal in game_win_rate["fallback_evidence"]} == {
        "parser_state.match_summary.game_wins_dependency",
        "parser_state.match_summary.total_games_dependency",
        "ledger.tier1.participants.player_team_dependency",
    }
    assert "game_win_rate_equals_game_wins_div_total_games" in game_win_rate["invariant_checks"]
    assert "game_win_rate_blank_when_total_games_zero" in game_win_rate["invariant_checks"]
    assert "game_win_rate_within_zero_and_one" in game_win_rate["invariant_checks"]
    assert any("no completed games is expected" in item for item in game_win_rate["degradation_behavior"])


def test_aggregate_entries_reference_tier3_game_result_dependencies() -> None:
    entries = _entries_by_id()
    aggregate_ids = {
        "tier1.match_aggregates.games_won",
        "tier1.match_aggregates.games_lost",
        "tier1.match_aggregates.total_games",
        "tier1.match_aggregates.game_win_rate",
    }

    for entry_id in aggregate_ids:
        assert any("tier3.game_results" in note for note in entries[entry_id]["notes"])


def test_tier3_game_result_entries_are_mapped() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_TIER3_ENTRY_IDS.issubset(entries)
    for entry_id in CONTRACTED_TIER3_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 3
        assert entry["output_family"] == "game_level_facts"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True


def test_tier3_game_number_entry_documents_slot_identity_sources() -> None:
    entry = _entries_by_id()["tier3.game_results.game_number"]

    assert entry["display_name"] == "Game Number"
    assert entry["model_surface"] == "GameSummary.to_game_log_row"
    assert {signal["signal_id"] for signal in entry["direct_evidence"]} == {
        "game_result.identity.game_number",
        "game_result.game_info.game_number",
        "game_state.identity.game_number",
    }
    assert {signal["signal_id"] for signal in entry["fallback_evidence"]} == {
        "parser_context.current_game_number",
        "match_state.game_results.list_order",
    }
    assert "game_number_must_be_slot_1_2_or_3" in entry["invariant_checks"]
    assert "per_game_results_require_known_game_number" in entry["invariant_checks"]
    assert any("does not create or guess a game slot" in item for item in entry["degradation_behavior"])


def test_tier3_game_winner_entries_document_game_scope_sources_and_non_promotion() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.game_results.{game_label}_winner_team"]
        direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
        fallback_signals = {signal["signal_id"]: signal for signal in entry["fallback_evidence"]}

        assert entry["display_name"] == f"g{game_number}_winner_team"
        assert entry["parser_owner"] == "src/mythic_edge_parser/app/state.py"
        assert direct_signals[f"game_result.{game_label}.game_scope_winner"]["confidence_when_used"] == "high"
        assert direct_signals[f"match_state.{game_label}.game_scope_winner"]["confidence_when_used"] == "medium"
        assert direct_signals[f"game_result.{game_label}.game_scope_winner"]["raw_payload_path"] == (
            "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId"
        )
        assert direct_signals[f"match_state.{game_label}.game_scope_winner"]["raw_payload_path"] == (
            "matchGameRoomStateChangedEvent.gameRoomInfo.finalMatchResult.resultList[].winningTeamId"
        )
        assert fallback_signals[f"game_result.{game_label}.top_level_legacy_winner"]["confidence_when_used"] == "medium"
        assert fallback_signals["tier3.game_results.game_number_dependency"]["required_for_final"] is True
        assert f"{game_label}_winner_does_not_promote_match_scope_result" in entry["invariant_checks"]
        assert "latest_valid_nested_game_scope_result_wins" in entry["invariant_checks"]
        assert any("whitespace zero, and bool winners are unknown" in item for item in entry["degradation_behavior"])
        assert any("match-scope results" in item for item in entry["degradation_behavior"])


def test_tier3_game_result_entries_are_derived_from_winner_and_player_team() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.game_results.{game_label}_result"]
        fallback_signals = {signal["signal_id"] for signal in entry["fallback_evidence"]}

        assert entry["parser_owner"] == "src/mythic_edge_parser/app/models.py"
        assert entry["value_source_policy"]["direct"] == "derived"
        assert entry["direct_evidence"][0]["signal_id"] == f"parser_state.match_summary.{game_label}_result"
        assert entry["direct_evidence"][0]["normalized_payload_path"] == (
            f"MatchSummary._game_result_fields().g{game_number}_result"
        )
        assert fallback_signals == {
            f"ledger.tier3.game_results.{game_label}_winner_team_dependency",
            "parser_state.match_summary.player_team_dependency",
            "ledger.tier1.participants.player_team_dependency",
        }
        assert f"{game_label}_result_derived_from_winner_and_player_team" in entry["invariant_checks"]
        assert f"{game_label}_result_missing_winner_not_inferred_loss" in entry["invariant_checks"]
        assert f"{game_label}_result_not_inferred_from_match_result_or_aggregates" in entry["invariant_checks"]
        assert any("unplayed game slot is expected" in item for item in entry["degradation_behavior"])
        assert any("match result, match winner, aggregate counts" in item for item in entry["degradation_behavior"])


def test_tier3_play_draw_entries_are_mapped_and_validate() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_PLAY_DRAW_ENTRY_IDS.issubset(entries)
    for entry_id in CONTRACTED_PLAY_DRAW_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 3
        assert entry["output_family"] == "game_level_facts"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True
        assert evidence_ledger.validate_ledger_entry(entry) == []


def test_tier3_starting_player_entries_document_explicit_turn_one_and_inference_sources() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.play_draw.{game_label}_starting_player"]
        direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
        fallback_signals = {signal["signal_id"]: signal for signal in entry["fallback_evidence"]}

        assert entry["display_name"] == f"g{game_number}_starting_player"
        assert entry["model_surface"] == f"MatchSummary.effective_starting_player({game_number})"
        assert direct_signals[f"client_action.{game_label}.choose_starting_player"][
            "raw_message_type"
        ] == "ClientMessageType_ChooseStartingPlayerResp"
        assert direct_signals[f"client_action.{game_label}.choose_starting_player"][
            "confidence_when_used"
        ] == "high"
        assert direct_signals[f"game_state.{game_label}.turn_one_active_player_team"][
            "confidence_when_used"
        ] == "high"
        assert direct_signals[f"game_state.{game_label}.turn_one_active_player_seat"][
            "confidence_when_used"
        ] == "low"
        assert "tier3.game_results.game_number_dependency" in fallback_signals
        assert "ledger.tier1.participants.participant_team_mapping_dependency" in fallback_signals
        assert f"{game_label}_starting_player_turn_one_evidence_requires_turn_number_1" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_starting_player_unknown_like_values_are_unknown" in entry[
            "invariant_checks"
        ]
        assert any("seat-only starting-player evidence is degraded" in item for item in entry["degradation_behavior"])
        assert all(signal["privacy_class"] == "path_only_no_values" for signal in entry["direct_evidence"])

    game1 = entries["tier3.play_draw.game1_starting_player"]
    assert "model.game1.inferred_starting_player_from_previous_game" not in _all_signal_ids(game1)
    assert "game1_starting_player_not_inferred_from_previous_game" in game1["invariant_checks"]
    assert game1["value_source_policy"]["fallback"] == "derived"

    game2 = entries["tier3.play_draw.game2_starting_player"]
    assert "model.game2.inferred_starting_player_from_previous_game" in _all_signal_ids(game2)
    assert "ledger.tier3.game_results.game1_winner_team_dependency" in _all_signal_ids(game2)
    assert "ledger.tier1.participants.player_team_dependency" in _all_signal_ids(game2)
    assert "ledger.tier1.participants.opponent_team_dependency" in _all_signal_ids(game2)
    assert game2["value_source_policy"]["fallback"] == "inferred"
    assert any(
        signal["signal_id"] == "model.game2.inferred_starting_player_from_previous_game"
        and signal["value_source_when_used"] == "inferred"
        for signal in game2["fallback_evidence"]
    )

    game3 = entries["tier3.play_draw.game3_starting_player"]
    assert "model.game3.inferred_starting_player_from_previous_game" in _all_signal_ids(game3)
    assert "ledger.tier3.game_results.game2_winner_team_dependency" in _all_signal_ids(game3)
    assert "ledger.tier1.participants.player_team_dependency" in _all_signal_ids(game3)
    assert "ledger.tier1.participants.opponent_team_dependency" in _all_signal_ids(game3)
    assert game3["value_source_policy"]["fallback"] == "inferred"
    assert any(
        signal["signal_id"] == "model.game3.inferred_starting_player_from_previous_game"
        and signal["value_source_when_used"] == "inferred"
        for signal in game3["fallback_evidence"]
    )


def test_tier3_play_draw_entries_are_derived_from_starting_player_and_participants() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.play_draw.{game_label}_play_draw"]
        fallback_signals = _signal_ids(entry, "fallback_evidence")

        assert entry["display_name"] == f"G{game_number} Play / Draw"
        assert entry["model_surface"] == f"MatchSummary.game_play_draw({game_number})"
        assert entry["value_source_policy"]["direct"] == "derived"
        assert entry["direct_evidence"][0]["signal_id"] == f"parser_state.match_summary.{game_label}_play_draw"
        assert entry["direct_evidence"][0]["value_source_when_used"] == "derived"
        assert f"ledger.tier3.play_draw.{game_label}_starting_player_dependency" in fallback_signals
        assert "ledger.tier1.participants.player_team_dependency" in fallback_signals
        assert f"{game_label}_play_draw_requires_starting_player_and_player_team" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_play_draw_missing_starting_player_not_draw" in entry["invariant_checks"]
        assert f"{game_label}_play_draw_expected_blank_when_unplayed" in entry["invariant_checks"]
        assert any("missing starting player leaves play/draw blank" in item for item in entry["degradation_behavior"])
        assert any(
            "played game" in item and "degraded and review-worthy" in item
            for item in entry["degradation_behavior"]
        )
        assert all(signal["privacy_class"] == "path_only_no_values" for signal in entry["fallback_evidence"])

    game2 = entries["tier3.play_draw.game2_play_draw"]
    assert "ledger.tier1.participants.opponent_team_dependency" in _all_signal_ids(game2)
    assert "ledger.tier3.game_results.game1_winner_team_dependency" in _all_signal_ids(game2)
    assert "game2_play_draw_exposes_inferred_starting_player_dependency" in game2["invariant_checks"]

    game3 = entries["tier3.play_draw.game3_play_draw"]
    assert "ledger.tier1.participants.opponent_team_dependency" in _all_signal_ids(game3)
    assert "ledger.tier3.game_results.game2_winner_team_dependency" in _all_signal_ids(game3)
    assert "game3_play_draw_exposes_inferred_starting_player_dependency" in game3["invariant_checks"]


def test_tier3_play_draw_remains_independent_from_mulligan_entries() -> None:
    tier3 = _tier3_family()
    entries = _entries_by_id()

    assert "play_draw" not in tier3["future_fields"]
    assert "starting_player" not in tier3["future_fields"]
    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert "sideboarding" not in tier3["future_fields"]
    assert "pre_postboard" not in tier3["future_fields"]
    assert not any("mulligan" in entry_id for entry_id in entries if entry_id.startswith("tier3.play_draw."))
    for entry_id in CONTRACTED_PLAY_DRAW_ENTRY_IDS:
        assert any("Issue #140 mulligan provenance remains deferred" in note for note in entries[entry_id]["notes"])


def test_tier3_mulligan_entries_are_mapped_and_validate() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_MULLIGAN_ENTRY_IDS.issubset(entries)
    for entry_id in CONTRACTED_MULLIGAN_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 3
        assert entry["output_family"] == "game_level_facts"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True
        assert evidence_ledger.validate_ledger_entry(entry) == []


def test_tier3_mulligan_entries_document_client_action_state_and_context_sources() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.mulligans.{game_label}_mulligans"]
        direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
        all_signals = _all_signal_ids(entry)

        assert entry["display_name"] == f"G{game_number} Mulligans"
        assert entry["model_surface"] == f"MatchSummary.games[{game_number}].mulligans"
        assert direct_signals[f"client_action.{game_label}.mulligan_response"][
            "raw_message_type"
        ] == "ClientMessageType_MulliganResp"
        assert direct_signals[f"client_action.{game_label}.mulligan_response"][
            "normalized_payload_path"
        ] == "payload.decision"
        assert direct_signals[f"client_action.{game_label}.mulligan_response"][
            "confidence_when_used"
        ] == "high"
        assert direct_signals[f"parser_state.match_summary.{game_label}_mulligans"][
            "value_source_when_used"
        ] == "derived"
        assert f"parser_state.mulligan_counts.{game_label}" in all_signals
        assert "tier3.game_results.game_number_dependency" in all_signals
        assert "parser_context.current_match_id" in all_signals
        assert "parser_context.current_game_number" in all_signals
        assert f"{game_label}_mulligans_unknown_decisions_not_high_confidence" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_mulligans_blank_display_not_zero" in entry["invariant_checks"]
        assert f"{game_label}_mulligans_not_inferred_from_opening_hand_size" in entry[
            "invariant_checks"
        ]
        assert any(
            "unknown, blank, malformed, or future decision values" in item
            for item in entry["degradation_behavior"]
        )
        assert any("contextless fallback zero" in item for item in entry["degradation_behavior"])
        assert any("duplicate or replayed ClientAction" in item for item in entry["degradation_behavior"])
        assert all(
            signal["privacy_class"] == "path_only_no_values"
            for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
        )


def test_total_mulligans_entry_is_derived_from_per_game_counts() -> None:
    entry = _entries_by_id()["tier3.mulligans.total_mulligans"]

    assert entry["display_name"] == "MTGA Mulligans"
    assert entry["model_surface"] == "MatchSummary.total_mulligans"
    assert entry["value_source_policy"]["direct"] == "derived"
    assert entry["value_source_policy"]["fallback"] == "derived"
    assert entry["direct_evidence"][0]["signal_id"] == "parser_state.match_summary.total_mulligans"
    assert entry["direct_evidence"][0]["value_source_when_used"] == "derived"
    assert _signal_ids(entry, "fallback_evidence") == {
        "ledger.tier3.mulligans.game1_mulligans_dependency",
        "ledger.tier3.mulligans.game2_mulligans_dependency",
        "ledger.tier3.mulligans.game3_mulligans_dependency",
    }
    assert "total_mulligans_equals_sum_of_per_game_counts" in entry["invariant_checks"]
    assert "total_mulligans_derived_not_observed" in entry["invariant_checks"]
    assert "total_mulligans_does_not_count_unplayed_slot_blanks" in entry["invariant_checks"]
    assert "total_mulligans_final_zero_and_live_blank_are_distinct" in entry["invariant_checks"]
    assert any("final MTGA Mulligans zero is valid" in item for item in entry["degradation_behavior"])
    assert any("live MTGA Mulligans blank is expected" in item for item in entry["degradation_behavior"])
    assert any("opening-hand size, card analytics" in item for item in entry["degradation_behavior"])


def test_tier3_mulligan_scope_documents_opening_hand_consumers_and_defers_analytics() -> None:
    tier3 = _tier3_family()
    entries = _entries_by_id()

    assert CONTRACTED_PLAY_DRAW_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_MULLIGAN_ENTRY_IDS.issubset(entries)
    assert "mulligans" not in tier3["future_fields"]
    assert CONTRACTED_OPENING_HAND_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TURN_COUNT_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_TIMING_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_DURATION_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_PRE_POSTBOARD_ENTRY_IDS.issubset(entries)
    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert "sideboarding" not in tier3["future_fields"]
    assert "opening_hand" not in tier3["future_fields"]
    assert "pre_postboard" not in tier3["future_fields"]
    for entry_id in CONTRACTED_MULLIGAN_ENTRY_IDS:
        entry = entries[entry_id]
        assert any("Opening-hand" in note or "opening-hand" in note for note in entry["notes"])


def test_tier3_opening_hand_entries_are_mapped_and_validate() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_OPENING_HAND_ENTRY_IDS.issubset(entries)
    for entry_id in CONTRACTED_OPENING_HAND_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 3
        assert entry["output_family"] == "game_level_facts"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True
        assert evidence_ledger.validate_ledger_entry(entry) == []
        assert all(
            signal["privacy_class"] == "path_only_no_values"
            for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
        )


def test_tier3_opening_hand_size_entries_document_exact_and_mulligan_fallback_sources() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.opening_hand.{game_label}_opening_hand_size"]
        direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
        fallback_signals = _signal_ids(entry, "fallback_evidence")

        assert entry["display_name"] == "Opening Hand Size"
        assert entry["model_surface"] == f"MatchSummary.games[{game_number}].opening_hand_size()"
        assert direct_signals[f"game_state.{game_label}.local_private_hand_snapshot"][
            "value_source_when_used"
        ] == "observed"
        assert direct_signals[f"parser_state.match_summary.{game_label}_opening_hand_size"][
            "normalized_payload_path"
        ] == f"MatchSummary.games[{game_number}].opening_hand_size()"
        assert f"ledger.tier3.opening_hand.{game_label}_opening_hand_dependency" in fallback_signals
        assert f"ledger.tier3.mulligans.{game_label}_mulligans_dependency" in fallback_signals
        assert "tier3.game_results.game_number_dependency" in fallback_signals
        assert "ledger.tier1.participants.local_system_seat_id_dependency" in fallback_signals
        assert f"{game_label}_opening_hand_size_exact_length_precedes_mulligan_fallback" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_opening_hand_size_fallback_is_derived_not_observed" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_opening_hand_size_blank_when_game_not_started" in entry[
            "invariant_checks"
        ]
        assert any("fallback opening-hand size is derived" in item for item in entry["degradation_behavior"])
        assert any("placeholder-containing exact lists" in item for item in entry["degradation_behavior"])
        assert any("data loss, truncation" in item for item in entry["degradation_behavior"])


def test_tier3_exact_opening_hand_entries_document_ownership_resolution_and_privacy() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.opening_hand.{game_label}_opening_hand"]
        direct_signals = _signal_ids(entry, "direct_evidence")
        fallback_signals = _signal_ids(entry, "fallback_evidence")

        assert entry["display_name"] == "Opening Hand"
        assert entry["model_surface"] == f"MatchSummary.games[{game_number}].opening_hand"
        assert f"game_state.{game_label}.local_private_hand_zone" in direct_signals
        assert f"game_state.{game_label}.local_private_hand_instance_ids" in direct_signals
        assert f"game_state.{game_label}.instance_grp_lookup" in direct_signals
        assert f"grp_id_catalog.{game_label}.card_name_resolution" in direct_signals
        assert f"parser_state.hand_snapshot_history.{game_label}" in direct_signals
        assert f"parser_state.match_summary.{game_label}_opening_hand" in direct_signals
        assert "ledger.tier1.participants.local_system_seat_id_dependency" in fallback_signals
        assert "ledger.tier1.participants.participant_team_mapping_dependency" in fallback_signals
        assert f"ledger.tier3.mulligans.{game_label}_mulligans_dependency" in fallback_signals
        assert f"{game_label}_opening_hand_requires_local_private_hand_ownership" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_opening_hand_requires_turn_number_1" in entry["invariant_checks"]
        assert f"{game_label}_opening_hand_requires_expected_size_when_known" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_opening_hand_placeholder_lists_are_degraded_and_may_serialize_blank" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_opening_hand_not_reconstructed_from_mulligans_or_ai" in entry[
            "invariant_checks"
        ]
        assert any("malformed owner-seat evidence" in item for item in entry["degradation_behavior"])
        assert any("missing GRP mapping" in item for item in entry["degradation_behavior"])
        assert any("may serialize blank" in item for item in entry["degradation_behavior"])
        assert any("AI must not populate exact opening hand" in item for item in entry["degradation_behavior"])


def test_tier3_mulliganed_away_entries_document_discarded_and_bottomed_sources() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.opening_hand.{game_label}_mulliganed_away"]
        direct_signals = _signal_ids(entry, "direct_evidence")
        fallback_signals = _signal_ids(entry, "fallback_evidence")

        assert entry["display_name"] == "Mulliganed Away"
        assert entry["model_surface"] == f"MatchSummary.games[{game_number}].mulliganed_away"
        assert f"parser_state.latest_hand_snapshot.{game_label}" in direct_signals
        assert f"parser_state.hand_snapshot_history.{game_label}" in direct_signals
        assert f"parser_state.bottomed_cards_capture.{game_label}" in direct_signals
        assert f"parser_state.match_summary.{game_label}_mulliganed_away" in direct_signals
        assert f"ledger.tier3.mulligans.{game_label}_mulligans_dependency" in fallback_signals
        assert f"ledger.tier3.opening_hand.{game_label}_opening_hand_dependency" in fallback_signals
        assert "ledger.tier1.participants.local_system_seat_id_dependency" in fallback_signals
        assert f"{game_label}_mulliganed_away_not_evidence_for_mulligan_count" in entry[
            "invariant_checks"
        ]
        assert (
            f"{game_label}_mulliganed_away_bottomed_diff_requires_prior_longer_snapshot_and_final_hand"
            in entry["invariant_checks"]
        )
        assert f"{game_label}_mulliganed_away_not_inferred_from_opening_hand_size" in entry[
            "invariant_checks"
        ]
        assert any("not evidence for mulligan count" in item for item in entry["degradation_behavior"])
        assert any("prior longer snapshot" in item for item in entry["degradation_behavior"])
        assert any("non-keep mulligan flow" in item for item in entry["degradation_behavior"])
        assert any("may serialize blank" in item for item in entry["degradation_behavior"])


def test_tier3_opening_hand_scope_preserves_prior_entries_and_defers_remaining_game_facts() -> None:
    tier3 = _tier3_family()
    entries = _entries_by_id()

    assert CONTRACTED_PLAY_DRAW_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_MULLIGAN_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_OPENING_HAND_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TURN_COUNT_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_TIMING_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_DURATION_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_PRE_POSTBOARD_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_OPENING_HAND_FIELDS.issubset(tier3["seed_fields"])
    assert "opening_hand" not in tier3["future_fields"]
    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert "sideboarding" not in tier3["future_fields"]
    assert "turn_count" not in tier3["future_fields"]
    assert "game_timing" not in tier3["future_fields"]
    assert "game_duration" not in tier3["future_fields"]
    assert "pre_postboard" not in tier3["future_fields"]
    assert not any(entry_id.startswith("tier3.sideboarding.") for entry_id in entries)
    assert not any(entry_id.startswith("tier3.deck_state.") for entry_id in entries)


def test_tier3_turn_count_entries_are_mapped_and_validate() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_TURN_COUNT_ENTRY_IDS.issubset(entries)
    for entry_id in CONTRACTED_TURN_COUNT_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 3
        assert entry["output_family"] == "game_level_facts"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True
        assert evidence_ledger.validate_ledger_entry(entry) == []
        assert all(
            signal["privacy_class"] == "path_only_no_values"
            for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
        )


def test_tier3_turn_count_entries_document_game_state_extractor_and_model_sources() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.turn_count.{game_label}_turn_count"]
        direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
        fallback_signals = _signal_ids(entry, "fallback_evidence")

        assert entry["display_name"] == f"G{game_number} Turn Count"
        assert entry["parser_owner"] == "src/mythic_edge_parser/app/state.py"
        assert entry["model_surface"] == f"MatchSummary.games[{game_number}].turn_count"
        assert {"MatchLogRow", "GameLogRow", "match_history"}.issubset(entry["downstream_surfaces"])
        assert direct_signals[f"game_state.{game_label}.turn_info_turn_number"][
            "raw_payload_path"
        ] == "greToClientMessages[].gameStateMessage.turnInfo.turnNumber"
        assert direct_signals[f"game_state.{game_label}.turn_info_turn_number"][
            "value_source_when_used"
        ] == "observed"
        assert direct_signals[f"game_state.{game_label}.identity_turn_number"][
            "normalized_payload_path"
        ] == "payload.identity.turn_number"
        assert direct_signals[f"game_state.{game_label}.payload_turn_number"][
            "normalized_payload_path"
        ] == "payload.turn_number"
        assert direct_signals[f"extractor.{game_label}.turn_number"][
            "normalized_payload_path"
        ] == "_extract_turn_info(payload, context).turn_number"
        assert direct_signals[f"parser_state.match_summary.{game_label}_turn_count"][
            "normalized_payload_path"
        ] == f"MatchSummary.games[{game_number}].turn_count"
        assert f"queued_game_state.{game_label}.turn_info_turn_number" in fallback_signals
        assert f"ledger.tier3.game_results.{game_label}_game_number_dependency" in fallback_signals
        assert f"ledger.tier3.turn_count.{game_label}_turn_count_prior_observation" in fallback_signals


def test_tier3_turn_count_entries_document_max_observed_blank_and_degraded_inputs() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.turn_count.{game_label}_turn_count"]

        assert entry["value_source_policy"] == {
            "direct": "observed",
            "fallback": "derived",
            "missing": "unknown",
            "contradiction": "conflict",
        }
        assert "inferred" not in entry["value_source_policy"].values()
        assert "legacy_enriched" not in entry["value_source_policy"].values()
        assert entry["confidence_policy"]["weak_fallback"] == "low"
        assert f"{game_label}_turn_count_requires_game_slot_identity" in entry["invariant_checks"]
        assert f"{game_label}_turn_count_uses_max_observed_positive_turn_number" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_turn_count_blank_output_is_not_zero" in entry["invariant_checks"]
        assert f"{game_label}_turn_count_zero_is_unknown_not_valid" in entry["invariant_checks"]
        assert f"{game_label}_turn_count_negative_or_boolean_evidence_degraded" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_turn_count_not_reconstructed_from_duration_or_actions" in entry[
            "invariant_checks"
        ]
        assert (
            f"{game_label}_turn_count_not_inferred_from_results_play_draw_mulligans_or_opening_hand"
            in entry["invariant_checks"]
        )
        assert f"{game_label}_turn_count_queued_fallback_is_reviewable" in entry["invariant_checks"]
        assert any("boolean-like or float-like values" in item for item in entry["degradation_behavior"])
        assert any("negative or zero turn values" in item for item in entry["degradation_behavior"])
        assert any("queued GameState fallback" in item for item in entry["degradation_behavior"])
        assert any("later lower observations" in item for item in entry["degradation_behavior"])
        assert any("truncation or data-loss" in item for item in entry["degradation_behavior"])
        assert any("must not populate turn count" in item for item in entry["degradation_behavior"])
        assert "fallback_used" in entry["drift_flags"]
        assert "weak_fallback_used" in entry["drift_flags"]
        assert "conflicting_evidence" in entry["drift_flags"]


def test_tier3_turn_count_scope_preserves_prior_entries_and_defers_timing_analytics() -> None:
    tier3 = _tier3_family()
    entries = _entries_by_id()

    assert CONTRACTED_PLAY_DRAW_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_MULLIGAN_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_OPENING_HAND_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TURN_COUNT_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_TIMING_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_DURATION_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_PRE_POSTBOARD_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TURN_COUNT_FIELDS.issubset(tier3["seed_fields"])
    assert "turn_count" not in tier3["future_fields"]
    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert "sideboarding" not in tier3["future_fields"]
    assert "game_timing" not in tier3["future_fields"]
    assert "game_duration" not in tier3["future_fields"]
    assert "pre_postboard" not in tier3["future_fields"]
    assert not any(entry_id.startswith("tier3.sideboarding.") for entry_id in entries)
    assert not any(entry_id.startswith("tier3.deck_state.") for entry_id in entries)
    for entry_id in CONTRACTED_TURN_COUNT_ENTRY_IDS:
        assert any("without changing parsing or update behavior" in note for note in entries[entry_id]["notes"])


def test_tier3_timing_entries_are_mapped_and_validate() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_GAME_TIMING_ENTRY_IDS.issubset(entries)
    for entry_id in CONTRACTED_GAME_TIMING_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 3
        assert entry["output_family"] == "game_level_facts"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True
        assert evidence_ledger.validate_ledger_entry(entry) == []
        assert all(
            signal["privacy_class"] == "path_only_no_values"
            for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
        )


def test_tier3_timing_entries_document_timestamps_state_endpoints_and_fallbacks() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        first_entry = entries[f"tier3.game_timing.{game_label}_first_event_time"]
        last_entry = entries[f"tier3.game_timing.{game_label}_last_event_time"]

        for entry, endpoint in ((first_entry, "first"), (last_entry, "last")):
            direct_signals = _signal_ids(entry, "direct_evidence")
            fallback_signals = _signal_ids(entry, "fallback_evidence")

            assert entry["display_name"] == (
                f"Game {game_number} {'First' if endpoint == 'first' else 'Last'} Observed Event Time"
            )
            assert entry["parser_owner"] == "src/mythic_edge_parser/app/state.py"
            assert entry["model_surface"] == f"MatchSummary.games[{game_number}].{endpoint}_event_time"
            assert {
                f"game_state.{game_label}.event_timestamp",
                f"client_action.{game_label}.event_timestamp",
                f"game_result.{game_label}.event_timestamp",
                f"parser_state.match_summary.{game_label}_first_event_time",
                f"parser_state.match_summary.{game_label}_last_event_time",
            }.issubset(direct_signals)
            assert {
                "router.timestamp_missing",
                "router.timestamp_parse_failure",
                "extractor.safe_iso.runtime_clock_fallback",
                f"ledger.tier3.game_results.{game_label}_game_number_dependency",
            }.issubset(fallback_signals)
            assert entry["value_source_policy"] == {
                "direct": "observed",
                "fallback": "derived",
                "missing": "unknown",
                "contradiction": "conflict",
            }
            assert "inferred" not in entry["value_source_policy"].values()
            assert "legacy_enriched" not in entry["value_source_policy"].values()
            assert f"{game_label}_{endpoint}_event_time_requires_game_slot_identity" in entry[
                "invariant_checks"
            ]
            observed_label = "first" if endpoint == "first" else "latest"
            assert (
                f"{game_label}_{endpoint}_event_time_is_{observed_label}_observed_parser_event_for_slot"
                in entry["invariant_checks"]
            )
            assert f"{game_label}_{endpoint}_event_time_not_inferred_from_results_or_turn_count" in entry[
                "invariant_checks"
            ]
            assert any("_safe_iso runtime-clock fallback" in item for item in entry["degradation_behavior"])
            assert any(
                "truncation, summarization, rotation, or data loss" in item
                for item in entry["degradation_behavior"]
            )
            assert any("must not populate game timing" in item for item in entry["degradation_behavior"])

        assert "game1_first_event_time_not_arena_internal_start_time".replace("game1", game_label) in first_entry[
            "invariant_checks"
        ]
        assert f"{game_label}_last_event_time_not_arena_internal_end_time" in last_entry["invariant_checks"]
        assert (
            f"{game_label}_last_event_time_row_timestamp_fallback_is_reviewable"
            in last_entry["invariant_checks"]
        )
        assert any("row timestamp fallback" in item for item in last_entry["degradation_behavior"])


def test_tier3_duration_entries_document_endpoint_dependencies_and_clamp_behavior() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_GAME_DURATION_ENTRY_IDS.issubset(entries)
    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.game_duration.{game_label}_duration_seconds"]
        direct_signals = _signal_ids(entry, "direct_evidence")
        fallback_signals = _signal_ids(entry, "fallback_evidence")

        assert entry["display_name"] == "Game Duration"
        assert entry["parser_owner"] == "src/mythic_edge_parser/app/models.py"
        assert entry["model_surface"] == f"MatchSummary.games[{game_number}].duration_seconds()"
        assert {
            f"parser_state.match_summary.{game_label}_duration_seconds",
            f"model.game_summary.{game_label}_duration_seconds",
        }.issubset(direct_signals)
        assert {
            f"ledger.tier3.game_timing.{game_label}_first_event_time_dependency",
            f"ledger.tier3.game_timing.{game_label}_last_event_time_dependency",
            f"model.duration_seconds.{game_label}_clamp_behavior",
            "router.timestamp_missing",
            "router.timestamp_parse_failure",
        }.issubset(fallback_signals)
        assert entry["value_source_policy"] == {
            "direct": "derived",
            "fallback": "derived",
            "missing": "unknown",
            "contradiction": "conflict",
        }
        assert "inferred" not in entry["value_source_policy"].values()
        assert "legacy_enriched" not in entry["value_source_policy"].values()
        assert entry["confidence_policy"]["direct"] == "medium"
        assert entry["confidence_policy"]["weak_fallback"] == "low"
        assert f"{game_label}_duration_requires_first_and_last_event_times" in entry["invariant_checks"]
        assert f"{game_label}_duration_seconds_uses_model_duration_seconds" in entry["invariant_checks"]
        assert f"{game_label}_duration_blank_is_unknown_not_zero" in entry["invariant_checks"]
        assert f"{game_label}_duration_zero_is_reviewable_clamped_or_equal_endpoint" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_duration_not_arena_clock_rope_or_clock_pressure" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_duration_not_reconstructed_from_turn_count_results_actions_or_ai" in entry[
            "invariant_checks"
        ]
        assert any("blank first or last endpoint" in item for item in entry["degradation_behavior"])
        assert any("invalid ISO endpoint strings" in item for item in entry["degradation_behavior"])
        assert any("clamped to zero" in item for item in entry["degradation_behavior"])
        assert any("not Arena clock, rope timer" in item for item in entry["degradation_behavior"])
        assert any("must not populate duration" in item for item in entry["degradation_behavior"])
        assert all(
            signal["privacy_class"] == "path_only_no_values"
            for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
        )


def test_tier3_timing_duration_scope_preserves_prior_entries_and_defers_remaining_game_facts() -> None:
    tier3 = _tier3_family()
    entries = _entries_by_id()

    assert CONTRACTED_PLAY_DRAW_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_MULLIGAN_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_OPENING_HAND_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TURN_COUNT_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_TIMING_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_DURATION_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_PRE_POSTBOARD_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TIMING_DURATION_FIELDS.issubset(tier3["seed_fields"])
    assert "game_timing" not in tier3["future_fields"]
    assert "game_duration" not in tier3["future_fields"]
    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert "sideboarding" not in tier3["future_fields"]
    assert "pre_postboard" not in tier3["future_fields"]
    assert not any(entry_id.startswith("tier3.sideboarding.") for entry_id in entries)
    assert not any(entry_id.startswith("tier3.deck_state.") for entry_id in entries)
    assert any("Issue #147 maps game timing and duration provenance" in note for note in tier3["notes"])


def test_tier3_pre_postboard_entries_are_mapped_and_validate() -> None:
    entries = _entries_by_id()

    assert CONTRACTED_PRE_POSTBOARD_ENTRY_IDS.issubset(entries)
    for entry_id in CONTRACTED_PRE_POSTBOARD_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 3
        assert entry["output_family"] == "game_level_facts"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True
        assert evidence_ledger.validate_ledger_entry(entry) == []
        assert all(
            signal["privacy_class"] == "path_only_no_values"
            for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
        )


def test_tier3_pre_postboard_entries_document_slot_mapping_and_row_sources() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        expected_label = "Preboard" if game_number == 1 else "Postboard"
        entry = entries[f"tier3.pre_postboard.{game_label}_pre_postboard"]
        direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
        fallback_signals = {signal["signal_id"]: signal for signal in entry["fallback_evidence"]}

        assert entry["display_name"] == "Pre / Postboard"
        assert entry["parser_owner"] == "src/mythic_edge_parser/app/models.py"
        assert entry["model_surface"] == 'GameSummary.to_game_log_row()["Pre / Postboard"]'
        assert {"GameLogRow", "match_history", "state_snapshots"}.issubset(entry["downstream_surfaces"])
        assert direct_signals[f"parser_state.match_summary.{game_label}_game_number"][
            "normalized_payload_path"
        ] == f"MatchSummary.games[{game_number}].game_number"
        assert direct_signals[f"parser_state.match_summary.{game_label}_game_number"][
            "value_source_when_used"
        ] == "derived"
        assert direct_signals[f"model.game_summary.{game_label}_pre_postboard_label"][
            "normalized_payload_path"
        ] == 'GameSummary.to_game_log_row()["Pre / Postboard"]'
        assert direct_signals[f"game_log_row.{game_label}_pre_postboard"][
            "normalized_payload_path"
        ] == 'GameLogRow["Pre / Postboard"]'
        assert f"expected {expected_label}" in direct_signals[
            f"model.game_summary.{game_label}_pre_postboard_label"
        ]["missing_behavior"]
        assert f"ledger.tier3.game_results.{game_label}_game_number_dependency" in fallback_signals
        assert "parser_context.current_game_number" in fallback_signals
        assert f"game_summary.{game_label}_has_summary_data" in fallback_signals
        assert fallback_signals["parser_context.current_game_number"][
            "confidence_when_used"
        ] == "low"
        assert fallback_signals[f"game_summary.{game_label}_has_summary_data"][
            "allowed_types"
        ] == ["bool"]


def test_tier3_pre_postboard_entries_reject_sideboarding_and_downstream_truth() -> None:
    entries = _entries_by_id()

    for game_number in (1, 2, 3):
        game_label = f"game{game_number}"
        entry = entries[f"tier3.pre_postboard.{game_label}_pre_postboard"]

        assert entry["value_source_policy"] == {
            "direct": "derived",
            "fallback": "derived",
            "missing": "unknown",
            "contradiction": "conflict",
        }
        assert "observed" not in entry["value_source_policy"].values()
        assert "inferred" not in entry["value_source_policy"].values()
        assert "legacy_enriched" not in entry["value_source_policy"].values()
        assert entry["confidence_policy"]["direct"] == "high"
        assert entry["confidence_policy"]["weak_fallback"] == "low"
        assert f"{game_label}_pre_postboard_requires_game_slot_identity" in entry["invariant_checks"]
        assert f"{game_label}_pre_postboard_derived_from_game_number" in entry["invariant_checks"]
        assert f"{game_label}_pre_postboard_game1_preboard_game2_game3_postboard" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_pre_postboard_postboard_not_sideboarding_proof" in entry[
            "invariant_checks"
        ]
        assert f"{game_label}_pre_postboard_not_submitted_deck_or_deck_state_evidence" in entry[
            "invariant_checks"
        ]
        assert (
            f"{game_label}_pre_postboard_not_inferred_from_format_queue_results_turn_count_timing_or_ai"
            in entry["invariant_checks"]
        )
        assert f"{game_label}_pre_postboard_unplayed_slot_unknown_not_standalone_truth" in entry[
            "invariant_checks"
        ]
        assert any("Postboard without sideboarding-entered evidence" in item for item in entry["degradation_behavior"])
        assert any("Postboard without submit-deck evidence" in item for item in entry["degradation_behavior"])
        assert any("Best-of-One or unknown-format" in item for item in entry["degradation_behavior"])
        assert any("must not populate pre/postboard truth" in item for item in entry["degradation_behavior"])
        assert "match_summary.sideboarding_entered_not_pre_postboard_evidence" in entry["notes"]
        assert "match_summary.submit_deck_seen_not_pre_postboard_evidence" in entry["notes"]
        assert "submitted_deck_contents_not_pre_postboard_evidence" in entry["notes"]


def test_tier3_pre_postboard_scope_preserves_prior_entries_and_defers_deck_state() -> None:
    tier3 = _tier3_family()
    entries = _entries_by_id()

    assert CONTRACTED_PLAY_DRAW_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_MULLIGAN_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_OPENING_HAND_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TURN_COUNT_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_TIMING_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_GAME_DURATION_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_PRE_POSTBOARD_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_PRE_POSTBOARD_FIELDS.issubset(tier3["seed_fields"])
    assert "pre_postboard" not in tier3["future_fields"]
    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert "sideboarding" not in tier3["future_fields"]
    assert not any(entry_id.startswith("tier3.sideboarding.") for entry_id in entries)
    assert not any(entry_id.startswith("tier3.deck_state.") for entry_id in entries)
    assert any("Issue #149 maps pre/postboard provenance" in note for note in tier3["notes"])


def test_tier4_sideboarding_submit_deck_entries_are_mapped_and_validate() -> None:
    entries = _entries_by_id()
    tier4 = _tier4_family()

    assert CONTRACTED_TIER4_ENTRY_IDS.issubset(entries)
    assert tier4["status"] == "seeded_sample"
    assert tier4["seed_fields"] == CONTRACTED_TIER4_FIELDS
    assert set(tier4["future_fields"]) == CONTRACTED_TIER4_DEFERRED_FIELDS
    assert "sideboarding_entered" not in tier4["future_fields"]
    assert "submit_deck_seen" not in tier4["future_fields"]

    for entry_id in CONTRACTED_TIER4_SIGNAL_ENTRY_IDS:
        entry = entries[entry_id]
        assert entry["tier"] == 4
        assert entry["output_family"] == "sideboarding_and_deck_state"
        assert entry["coverage_status"] == "seeded_sample"
        assert entry["parser_managed_truth"] is True
        assert {"MatchLogRow", "match_history", "state_snapshots", "MATCH_LOG_SYNC_FIELDS"}.issubset(
            entry["downstream_surfaces"]
        )
        assert entry["value_source_policy"] == {
            "direct": "observed",
            "fallback": "derived",
            "missing": "unknown",
            "contradiction": "conflict",
        }
        assert evidence_ledger.validate_ledger_entry(entry) == []
        assert all(
            signal["privacy_class"] == "path_only_no_values"
            for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
        )


def test_tier4_deck_state_boundary_keeps_broad_deck_state_deferred() -> None:
    tier3 = _tier3_family()
    tier4 = _tier4_family()
    entries = _entries_by_id()
    output_fields = {entry["output_field"] for entry in entries.values()}

    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert "deck_state" in tier3["future_fields"]
    assert tier4["seed_fields"] == CONTRACTED_TIER4_FIELDS
    assert set(tier4["future_fields"]) == CONTRACTED_TIER4_DEFERRED_FIELDS
    assert "deck_state" not in tier4["seed_fields"]
    assert "deck_state" not in tier4["future_fields"]
    assert not any(entry_id.startswith("tier4.deck_state.") for entry_id in entries)
    assert output_fields.isdisjoint(CONTRACTED_TIER4_DECK_STATE_BOUNDARY_FORBIDDEN_OUTPUT_FIELDS)


def test_tier4_deck_state_boundary_family_notes_document_downstream_surfaces() -> None:
    tier4_notes = " ".join(_tier4_family()["notes"])

    for fragment in CONTRACTED_TIER4_DECK_STATE_BOUNDARY_NOTE_FRAGMENTS:
        assert fragment in tier4_notes


def test_tier4_deck_state_boundary_keeps_runtime_and_enrichment_bounded() -> None:
    entry = _entries_by_id()["tier4.submitted_deck_cards.submitted_deck_cards"]
    direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
    fallback_signals = {signal["signal_id"]: signal for signal in entry["fallback_evidence"]}

    assert set(direct_signals) == {
        "client_action.submitted_deck_cards.specialized_submit_deck_resp",
        "client_action.submitted_deck_cards.deck_cards",
        "client_action.submitted_deck_cards.sideboard_cards",
        "client_action.submitted_deck_cards.request_context",
        "client_action.submitted_deck_cards.event_timestamp_context",
    }
    assert {
        "active_submitted_deck_artifact",
        "runtime_active_deck_state",
        "active_deck_profile",
        "grp_id_candidate_report",
    }.issubset(entry["downstream_surfaces"])

    bounded_fallbacks = {
        "diagnostics.active_submitted_deck_artifact",
        "diagnostics.submitted_deck_counts_and_signature",
        "runtime_surfaces.active_deck_state",
        "grp_id_candidates.submitted_deck_snapshot",
    }
    assert bounded_fallbacks.issubset(fallback_signals)
    for signal_id in bounded_fallbacks:
        assert fallback_signals[signal_id]["required_for_final"] is False
        assert fallback_signals[signal_id]["value_source_when_used"] == "derived"
        assert fallback_signals[signal_id]["finality_when_used"] == "provisional"
        assert fallback_signals[signal_id]["privacy_class"] == "path_only_no_values"

    assert any("mismatch between parser event lists" in item for item in entry["degradation_behavior"])
    assert any(
        "downstream decklist matching or GRP scoring disagreement" in item
        for item in entry["degradation_behavior"]
    )
    assert any("not broad deck-state truth" in note for note in entry["notes"])


def test_tier4_sideboarding_entry_documents_signal_row_and_boundaries() -> None:
    entry = _entries_by_id()["tier4.sideboarding_submit_deck.sideboarding_entered"]
    direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
    fallback_signals = {signal["signal_id"]: signal for signal in entry["fallback_evidence"]}

    assert entry["display_name"] == "MTGA Sideboard Entered"
    assert entry["parser_owner"] == "src/mythic_edge_parser/app/state.py"
    assert entry["model_surface"] == "MatchSummary.sideboarding_entered"
    assert direct_signals["client_action.sideboarding_entered.enter_sideboarding_req"]["raw_message_type"] == (
        "ClientMessageType_EnterSideboardingReq"
    )
    assert direct_signals["client_action.sideboarding_entered.raw_message_type_path"]["raw_payload_path"] == (
        "raw_client_action.payload.type"
    )
    assert direct_signals["parser_state.match_summary.sideboarding_entered"][
        "normalized_payload_path"
    ] == "MatchSummary.sideboarding_entered"
    assert direct_signals["match_log_row.mtga_sideboard_entered_yes"]["normalized_payload_path"] == (
        'MatchSummary.to_match_log_row()["MTGA Sideboard Entered"]'
    )
    assert "model.match_summary.sideboarding_entered_surfaces" in direct_signals
    assert fallback_signals["parser_context.current_match_id"]["missing_behavior"].startswith("state.py ignores")
    assert fallback_signals["match_log_row.mtga_sideboard_entered_no_or_blank"]["missing_behavior"] == (
        "final No is derived parser-state absence, not absolute source-log absence proof"
    )
    assert "sideboarding_entered_requires_current_match_context" in entry["invariant_checks"]
    assert "sideboarding_entered_not_pre_postboard_truth" in entry["invariant_checks"]
    assert "sideboarding_entered_not_submit_deck_truth" in entry["invariant_checks"]
    assert "sideboarding_entered_not_submitted_deck_contents" in entry["invariant_checks"]
    assert any("duplicate sideboarding signals collapse" in item for item in entry["degradation_behavior"])
    assert any("live blank represents provisional absence" in item for item in entry["degradation_behavior"])
    assert any("must not populate sideboarding_entered truth" in item for item in entry["degradation_behavior"])
    assert any("submitted deck card contents remain deferred" in note for note in entry["notes"])


def test_tier4_submit_deck_entry_documents_signal_row_and_boundaries() -> None:
    entry = _entries_by_id()["tier4.sideboarding_submit_deck.submit_deck_seen"]
    direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
    fallback_signals = {signal["signal_id"]: signal for signal in entry["fallback_evidence"]}

    assert entry["display_name"] == "MTGA Submit Deck Seen"
    assert entry["parser_owner"] == "src/mythic_edge_parser/app/state.py"
    assert entry["model_surface"] == "MatchSummary.submit_deck_seen"
    assert direct_signals["client_action.submit_deck_seen.specialized_submit_deck_resp"][
        "parser_event_type"
    ] == "submit_deck_resp"
    assert direct_signals["client_action.submit_deck_seen.specialized_submit_deck_resp"]["raw_message_type"] == (
        "ClientMessageType_SubmitDeckResp"
    )
    assert direct_signals["client_action.submit_deck_seen.generic_submit_deck_resp"]["raw_message_type"] == (
        "ClientMessageType_SubmitDeckResp"
    )
    assert direct_signals["parser_state.match_summary.submit_deck_seen"][
        "normalized_payload_path"
    ] == "MatchSummary.submit_deck_seen"
    assert direct_signals["match_log_row.mtga_submit_deck_seen_yes"]["normalized_payload_path"] == (
        'MatchSummary.to_match_log_row()["MTGA Submit Deck Seen"]'
    )
    assert "model.match_summary.submit_deck_seen_surfaces" in direct_signals
    assert fallback_signals["client_action.submit_deck_seen.empty_or_malformed_card_lists"][
        "normalized_payload_path"
    ] == "payload.deck_cards + payload.sideboard_cards"
    assert fallback_signals["match_log_row.mtga_submit_deck_seen_no_or_blank"]["missing_behavior"] == (
        "final No is derived parser-state absence, not absolute source-log absence proof"
    )
    assert "submit_deck_seen_requires_current_match_context" in entry["invariant_checks"]
    assert "submit_deck_seen_not_sideboarding_entered_truth" in entry["invariant_checks"]
    assert "submit_deck_seen_not_submitted_deck_contents" in entry["invariant_checks"]
    assert "submit_deck_seen_allows_empty_or_malformed_card_lists" in entry["invariant_checks"]
    assert any("empty normalized deck_cards or sideboard_cards" in item for item in entry["degradation_behavior"])
    assert any("without prior sideboarding-entered signal" in item for item in entry["degradation_behavior"])
    assert any("must not populate submit_deck_seen truth" in item for item in entry["degradation_behavior"])
    assert any("submitted deck card contents remain deferred" in note for note in entry["notes"])


def test_tier4_submitted_deck_cards_entry_documents_card_content_sources() -> None:
    entry = _entries_by_id()["tier4.submitted_deck_cards.submitted_deck_cards"]
    direct_signals = {signal["signal_id"]: signal for signal in entry["direct_evidence"]}
    fallback_signals = {signal["signal_id"]: signal for signal in entry["fallback_evidence"]}

    assert entry["display_name"] == "Submitted Deck Cards"
    assert entry["parser_owner"] == "src/mythic_edge_parser/parsers/client_actions.py"
    assert entry["model_surface"] == "ClientActionEvent.payload.deck_cards + ClientActionEvent.payload.sideboard_cards"
    assert {"active_submitted_deck_artifact", "runtime_active_deck_state", "grp_id_candidate_report"}.issubset(
        entry["downstream_surfaces"]
    )
    assert direct_signals["client_action.submitted_deck_cards.specialized_submit_deck_resp"][
        "parser_event_type"
    ] == "submit_deck_resp"
    assert direct_signals["client_action.submitted_deck_cards.specialized_submit_deck_resp"][
        "raw_message_type"
    ] == "ClientMessageType_SubmitDeckResp"
    assert direct_signals["client_action.submitted_deck_cards.deck_cards"][
        "normalized_payload_path"
    ] == "payload.deck_cards"
    assert direct_signals["client_action.submitted_deck_cards.sideboard_cards"][
        "normalized_payload_path"
    ] == "payload.sideboard_cards"
    assert direct_signals["client_action.submitted_deck_cards.request_context"][
        "normalized_payload_path"
    ] == "payload.game_state_id + payload.resp_id + payload.request_id"
    assert direct_signals["client_action.submitted_deck_cards.event_timestamp_context"][
        "normalized_payload_path"
    ] == "EventMetadata.timestamp"
    assert fallback_signals["client_action.submitted_deck_cards.raw_mainboard_paths"][
        "raw_payload_path"
    ].startswith("raw_client_action.payload.submitDeckResp.deckCards")
    assert fallback_signals["client_action.submitted_deck_cards.raw_sideboard_paths"][
        "raw_payload_path"
    ].startswith("raw_client_action.payload.submitDeckResp.sideboardCards")
    assert "diagnostics.active_submitted_deck_artifact" in fallback_signals
    assert "runtime_surfaces.active_deck_state" in fallback_signals
    assert "grp_id_candidates.submitted_deck_snapshot" in fallback_signals
    assert all(
        signal["privacy_class"] == "path_only_no_values"
        for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
    )


def test_tier4_submitted_deck_cards_entry_documents_policies_and_facets() -> None:
    entry = _entries_by_id()["tier4.submitted_deck_cards.submitted_deck_cards"]
    fallback_signals = {signal["signal_id"]: signal for signal in entry["fallback_evidence"]}

    assert entry["value_source_policy"] == {
        "direct": "observed",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    }
    assert entry["confidence_policy"] == {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    }
    assert entry["finality_policy"] == {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    }
    assert fallback_signals["diagnostics.submitted_deck_counts_and_signature"][
        "normalized_payload_path"
    ] == (
        "len(payload.deck_cards) + len(payload.sideboard_cards) + "
        "submitted_deck_signature(payload.deck_cards, payload.sideboard_cards)"
    )
    assert fallback_signals["diagnostics.submitted_deck_counts_and_signature"][
        "value_source_when_used"
    ] == "derived"
    assert "submitted_deck_cards_counts_and_signature_are_derived_facets_only" in entry["invariant_checks"]
    assert any("Counts and submitted-deck signature are derived facets" in note for note in entry["notes"])
    assert not any(entry["output_field"].endswith(suffix) for suffix in ("_count", "_signature", "_timestamp"))


def test_tier4_submitted_deck_cards_entry_documents_degradation_and_repeated_payloads() -> None:
    entry = _entries_by_id()["tier4.submitted_deck_cards.submitted_deck_cards"]

    assert "submitted_deck_cards_requires_submit_deck_resp_event" in entry["invariant_checks"]
    assert "submitted_deck_cards_requires_non_empty_normalized_card_list" in entry["invariant_checks"]
    assert "submitted_deck_cards_empty_or_malformed_lists_are_unknown_or_degraded" in entry["invariant_checks"]
    assert "submitted_deck_cards_not_submit_deck_seen_boolean_truth" in entry["invariant_checks"]
    assert "submitted_deck_cards_not_sideboarding_or_pre_postboard_truth" in entry["invariant_checks"]
    assert "submitted_deck_cards_not_deck_state_or_deck_identity_truth" in entry["invariant_checks"]
    assert any("both deck_cards and sideboard_cards empty" in item for item in entry["degradation_behavior"])
    assert any("truthy malformed direct sources" in item for item in entry["degradation_behavior"])
    assert any(
        "raw preserved payload paths with empty normalized lists" in item
        for item in entry["degradation_behavior"]
    )
    assert any("repeated submit-deck payloads remain event-scoped" in item for item in entry["degradation_behavior"])
    assert any("runtime state is latest-observed fallback" in note for note in entry["notes"])
    assert any("preserve #151 submit_deck_seen" in note for note in entry["notes"])


def test_tier4_submitted_deck_cards_entry_rejects_downstream_truth() -> None:
    entry = _entries_by_id()["tier4.submitted_deck_cards.submitted_deck_cards"]
    evidence_text = json.dumps(
        {
            "direct_evidence": entry["direct_evidence"],
            "fallback_evidence": entry["fallback_evidence"],
        },
        sort_keys=True,
    )

    for forbidden in (
        "MatchSummary.submit_deck_seen",
        "MTGA Submit Deck Seen",
        "sideboarding_entered",
        "pre_postboard",
        "deck_name",
        "deck_id",
        "decklist_identity",
        "sideboard_delta",
        "card_name",
        "collection_ownership",
        "candidate_score",
        "workbook_formula",
        "apps_script",
        "model_provider",
        "openai",
    ):
        assert forbidden not in evidence_text
    assert any("deck names, deck IDs, sideboard deltas" in item for item in entry["degradation_behavior"])
    assert any("model-provider output, and AI" in item for item in entry["degradation_behavior"])
    assert any("not broad deck-state truth" in note for note in entry["notes"])
    assert any("does not prove deck names" in note for note in entry["notes"])


def test_tier4_entries_reject_downstream_truth_and_preserve_privacy() -> None:
    entries = _entries_by_id()
    forbidden_evidence_fragments = {
        "pre_postboard",
        "queue_type",
        "workbook_formula",
        "apps_script",
        "analytics",
        "archetype",
        "sideboard_delta",
        "deck_signature",
    }

    for entry_id in CONTRACTED_TIER4_SIGNAL_ENTRY_IDS:
        entry = entries[entry_id]
        evidence_text = json.dumps(
            {
                "direct_evidence": entry["direct_evidence"],
                "fallback_evidence": entry["fallback_evidence"],
            },
            sort_keys=True,
        )
        assert all(fragment not in evidence_text for fragment in forbidden_evidence_fragments)
        assert any("Apps Script" in item for item in entry["degradation_behavior"])
        assert any("analytics" in item and "AI" in item for item in entry["degradation_behavior"])
        assert any("sideboard" in item for item in entry["degradation_behavior"])
        assert any("path_only_no_values" == signal["privacy_class"] for signal in entry["direct_evidence"])
        assert all(
            signal["privacy_class"] == "path_only_no_values"
            for signal in (*entry["direct_evidence"], *entry["fallback_evidence"])
        )
        assert any("submitted_deck_cards" in note for note in entry["notes"])


def test_tier4_scope_preserves_prior_entries_and_keeps_deck_contents_deferred() -> None:
    tier3 = _tier3_family()
    tier4 = _tier4_family()
    entries = _entries_by_id()

    assert CONTRACTED_TIER1_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TIER3_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_PRE_POSTBOARD_ENTRY_IDS.issubset(entries)
    assert CONTRACTED_TIER4_ENTRY_IDS.issubset(entries)
    assert "sideboarding" not in tier3["future_fields"]
    assert set(tier3["future_fields"]) == CONTRACTED_TIER3_DEFERRED_FIELDS
    assert set(tier4["seed_fields"]) == set(CONTRACTED_TIER4_FIELDS)
    assert set(tier4["future_fields"]) == CONTRACTED_TIER4_DEFERRED_FIELDS
    assert "submitted_deck_cards" not in tier4["future_fields"]
    assert "tier4.submitted_deck_cards.submitted_deck_cards" in entries
    assert not any(entry_id.startswith("tier4.deck_state.") for entry_id in entries)
    assert any("Pre/postboard labels remain Tier 3" in note for note in tier4["notes"])


def test_builtin_ledger_and_entries_validate_cleanly() -> None:
    ledger = evidence_ledger.build_player_log_evidence_ledger()

    assert evidence_ledger.validate_player_log_evidence_ledger() == []
    assert evidence_ledger.validate_player_log_evidence_ledger(ledger) == []
    for entry in ledger["entries"]:
        assert evidence_ledger.validate_ledger_entry(entry) == []


def test_iter_ledger_entries_is_copy_safe() -> None:
    first_entry = evidence_ledger.iter_ledger_entries()[0]
    first_entry["entry_id"] = "tier1.mutated"
    first_entry["direct_evidence"][0]["signal_id"] = "mutated.signal"

    fresh_entry = evidence_ledger.iter_ledger_entries()[0]

    assert fresh_entry["entry_id"] == "tier1.match_identity.match_id"
    assert fresh_entry["direct_evidence"][0]["signal_id"] == "match_state.match_id"


def test_built_ledger_is_json_serializable_and_deterministic() -> None:
    first = evidence_ledger.build_player_log_evidence_ledger()
    second = evidence_ledger.build_player_log_evidence_ledger()

    assert first == second
    encoded = json.dumps(first, indent=2, sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded) == first


def test_validator_reports_missing_required_fields_without_raising() -> None:
    errors = evidence_ledger.validate_player_log_evidence_ledger({})

    assert "ledger:missing:object" in errors
    assert "ledger:missing:entries" in errors
    assert "ledger:entries_not_list" in errors
    assert evidence_ledger.validate_player_log_evidence_ledger("not-a-mapping") == ["ledger:not_mapping"]


def test_validator_reports_unknown_policy_vocabularies() -> None:
    entry = copy.deepcopy(evidence_ledger.iter_ledger_entries()[0])
    entry["value_source_policy"]["direct"] = "guessed"
    entry["confidence_policy"]["direct"] = "certain"
    entry["finality_policy"]["live"] = "done"
    entry["drift_flags"].append("mystery_drift")
    entry["direct_evidence"][0]["value_source_when_used"] = "guessed"
    entry["direct_evidence"][0]["confidence_when_used"] = "certain"
    entry["direct_evidence"][0]["finality_when_used"] = "done"

    errors = evidence_ledger.validate_ledger_entry(entry)

    assert "entry:value_source_policy:unknown:direct:guessed" in errors
    assert "entry:confidence_policy:unknown:direct:certain" in errors
    assert "entry:finality_policy:unknown:live:done" in errors
    assert "drift_flags:unknown:mystery_drift" in errors
    assert "entry:direct_evidence[0]:evidence:value_source_when_used:unknown:guessed" in errors
    assert "entry:direct_evidence[0]:evidence:confidence_when_used:unknown:certain" in errors
    assert "entry:direct_evidence[0]:evidence:finality_when_used:unknown:done" in errors


def test_validator_reports_duplicate_entry_and_signal_ids() -> None:
    ledger = evidence_ledger.build_player_log_evidence_ledger()
    ledger["entries"].append(copy.deepcopy(ledger["entries"][0]))
    entry = copy.deepcopy(evidence_ledger.iter_ledger_entries()[0])
    entry["fallback_evidence"][0]["signal_id"] = entry["direct_evidence"][0]["signal_id"]

    ledger_errors = evidence_ledger.validate_player_log_evidence_ledger(ledger)
    entry_errors = evidence_ledger.validate_ledger_entry(entry)

    assert "duplicate_entry_id:tier1.match_identity.match_id" in ledger_errors
    assert "duplicate_signal_id:match_state.match_id" in entry_errors


def test_validator_reports_absolute_paths_and_raw_log_like_text() -> None:
    entry = copy.deepcopy(evidence_ledger.iter_ledger_entries()[0])
    entry["parser_owner"] = "/private/example/state.py"
    entry["notes"].append("[UnityCrossThreadLogger]5/19/2026 12:00:00 PM")
    forbidden_note_index = len(entry["notes"]) - 1

    errors = evidence_ledger.validate_ledger_entry(entry)

    assert "privacy:absolute_path:entry.parser_owner" in errors
    assert f"privacy:forbidden_text:entry.notes[{forbidden_note_index}]" in errors


def test_field_evidence_validator_enforces_vocabularies_and_review_rules() -> None:
    payload = {
        "object": evidence_ledger.FIELD_EVIDENCE_OBJECT,
        "schema_version": evidence_ledger.FIELD_EVIDENCE_SCHEMA_VERSION,
        "ledger_version": evidence_ledger.LEDGER_VERSION,
        "entry_id": "tier1.match_identity.match_id",
        "output_family": "match_identity_and_lifecycle",
        "output_field": "match_id",
        "value_source": "observed",
        "confidence": "high",
        "finality": "live",
        "source_event_kind": "MatchState",
        "source_event_type": "match_started",
        "source_payload_paths": ["payload.match_id"],
        "source_event_timestamp": "",
        "drift_flags": [],
        "invariant_status": "not_checked",
        "degraded_reason": "",
        "review_required": False,
    }

    assert evidence_ledger.validate_field_evidence(payload) == []

    invalid = dict(payload)
    invalid.update(
        {
            "value_source": "guessed",
            "confidence": "certain",
            "finality": "done",
            "drift_flags": ["mystery_drift"],
            "invariant_status": "mystery",
        }
    )

    errors = evidence_ledger.validate_field_evidence(invalid)

    assert "field_evidence:value_source:unknown:guessed" in errors
    assert "field_evidence:confidence:unknown:certain" in errors
    assert "field_evidence:finality:unknown:done" in errors
    assert "field_evidence:drift_flags:unknown:mystery_drift" in errors
    assert "field_evidence:invariant_status:unknown:mystery" in errors


def test_field_evidence_review_required_policy_is_validated() -> None:
    payload = {
        "object": evidence_ledger.FIELD_EVIDENCE_OBJECT,
        "schema_version": evidence_ledger.FIELD_EVIDENCE_SCHEMA_VERSION,
        "ledger_version": evidence_ledger.LEDGER_VERSION,
        "entry_id": "tier1.match_identity.match_id",
        "output_family": "match_identity_and_lifecycle",
        "output_field": "match_id",
        "value_source": "conflict",
        "confidence": "low",
        "finality": "final",
        "source_event_kind": "MatchState",
        "source_event_type": "match_started",
        "source_payload_paths": ["payload.match_id"],
        "source_event_timestamp": "",
        "drift_flags": [],
        "invariant_status": "not_checked",
        "degraded_reason": "conflicting evidence",
        "review_required": False,
    }

    assert "field_evidence:invalid_review_required" in evidence_ledger.validate_field_evidence(payload)
    payload["review_required"] = True
    assert evidence_ledger.validate_field_evidence(payload) == []


def test_ledger_data_omits_private_values_and_local_artifact_markers() -> None:
    encoded = json.dumps(evidence_ledger.build_player_log_evidence_ledger(), sort_keys=True)

    for forbidden in (
        "[UnityCrossThreadLogger]",
        "[Client GRE]",
        "https://" + "hooks.",
        "script.google.com",
        "failed_posts",
        "runtime_status_latest",
        "runtime-status",
        "workbook_exports",
        "/" + "Users/",
        "C:" + "\\Users\\",
    ):
        assert forbidden not in encoded


def test_module_reload_has_no_filesystem_dependency(monkeypatch) -> None:
    def forbidden_open(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("evidence_ledger import must not read files")

    monkeypatch.setattr(builtins, "open", forbidden_open)

    reloaded = importlib.reload(evidence_ledger)

    assert reloaded.build_player_log_evidence_ledger()["object"] == evidence_ledger.LEDGER_OBJECT
