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
]

CONTRACTED_TIER3_ENTRY_IDS = {
    "tier3.game_results.game_number",
    "tier3.game_results.game1_winner_team",
    "tier3.game_results.game2_winner_team",
    "tier3.game_results.game3_winner_team",
    "tier3.game_results.game1_result",
    "tier3.game_results.game2_result",
    "tier3.game_results.game3_result",
}

CONTRACTED_TIER3_DEFERRED_FIELDS = {
    "play_draw",
    "starting_player",
    "mulligans",
    "turn_count",
    "opening_hand",
    "game_timing",
    "game_duration",
    "pre_postboard",
    "sideboarding",
    "deck_state",
}


def _entries_by_id() -> dict[str, dict[str, object]]:
    return {entry["entry_id"]: entry for entry in evidence_ledger.iter_ledger_entries()}


def _family(output_family: str) -> dict[str, object]:
    families = evidence_ledger.build_player_log_evidence_ledger()["output_families"]
    return next(family for family in families if family["output_family"] == output_family)


def _tier1_family() -> dict[str, object]:
    return _family("match_identity_and_lifecycle")


def _tier3_family() -> dict[str, object]:
    return _family("game_level_facts")


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
        (4, "sideboarding_and_deck_state", "registered_future"),
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
    assert any("match-scope results are not promoted" in item for item in tier3["notes"])


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

    assert set(entries) == CONTRACTED_TIER1_ENTRY_IDS | CONTRACTED_TIER3_ENTRY_IDS
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
        "runtime_status",
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
