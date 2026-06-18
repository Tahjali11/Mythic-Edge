from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from mythic_edge_parser.app import corpus_parity_report as corpus

MANIFEST_PATH = Path("tests/fixtures/parser_corpus/corpus_manifest.v1.json")
SESSION_LEDGER_PATH = Path("tests/fixtures/parser_corpus/session_ledger.v1.json")


def _manifest_payload() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _session_ledger_payload() -> dict:
    return json.loads(SESSION_LEDGER_PATH.read_text(encoding="utf-8"))


def _write_json(tmp_path: Path, name: str, payload: dict) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return path


def _matrix_row(report: dict, scenario_family: str) -> dict:
    return next(row for row in report["coverage_matrix"] if row["scenario_family"] == scenario_family)


def _manifest_entry(manifest: dict, entry_id: str) -> dict:
    return next(entry for entry in manifest["entries"] if entry["entry_id"] == entry_id)


def _session_entry(session_ledger: dict, session_id: str) -> dict:
    return next(session for session in session_ledger["sessions"] if session["session_id"] == session_id)


def test_committed_manifest_and_session_ledger_validate_cleanly() -> None:
    manifest = corpus.load_corpus_manifest(MANIFEST_PATH)
    session_ledger = corpus.load_session_ledger(SESSION_LEDGER_PATH)

    assert corpus.validate_corpus_manifest(manifest) == []
    assert corpus.validate_session_ledger(session_ledger) == []
    assert [family["family_id"] for family in manifest["taxonomy"]["families"]] == list(corpus.SCENARIO_FAMILIES)
    assert _manifest_entry(manifest, "gsm_truncation_marker_synthetic_v1")["coverage_status"] == "covered_synthetic"
    draft_with_games_boundary = _manifest_entry(manifest, "draft_with_games_boundary_report_v1")
    assert draft_with_games_boundary["coverage_status"] == "covered_report_only"
    assert draft_with_games_boundary["scenario_families"] == ["core_gameplay.draft_with_games"]
    assert draft_with_games_boundary["parser_event_families"] == []
    assert draft_with_games_boundary["parser_claim_families"] == [
        "draft_with_games_boundary_report",
        "draft_only_reference_only",
        "draft_parser_family_not_completed_games",
        "limited_game_result_evidence_not_claimed",
        "draft_privacy_boundary",
    ]
    assert draft_with_games_boundary["coverage_basis"] == ["fixture_metadata_only"]
    assert "parser_behavior_verified" not in draft_with_games_boundary["coverage_basis"]
    assert "draft-only" in draft_with_games_boundary["known_gaps"][0]
    assert "completed limited gameplay" in draft_with_games_boundary["known_gaps"][0]
    assert "game-result evidence" in draft_with_games_boundary["known_gaps"][0]
    assert "draft deck construction" in draft_with_games_boundary["known_gaps"][0]
    assert "intentionally report-only" in draft_with_games_boundary["review_notes"][0]
    assert "synthetic GameState anchor" in draft_with_games_boundary["review_notes"][0]
    assert "not draft-with-games evidence" in draft_with_games_boundary["review_notes"][0]
    sealed_entry = _manifest_entry(manifest, "sealed_entry_lifecycle_synthetic_v1")
    assert sealed_entry["coverage_status"] == "covered_synthetic"
    assert sealed_entry["scenario_families"] == ["core_gameplay.sealed_entry"]
    assert sealed_entry["parser_event_families"] == ["MatchState", "EventLifecycle"]
    assert sealed_entry["parser_claim_families"] == ["sealed_event_identity", "event_lifecycle"]
    assert sealed_entry["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "sealed deckbuild and sealed matches remain missing" in sealed_entry["review_notes"][0]
    sealed_match = _manifest_entry(manifest, "sealed_match_synthetic_v1")
    assert sealed_match["coverage_status"] == "covered_synthetic"
    assert sealed_match["scenario_families"] == ["core_gameplay.sealed_matches"]
    assert sealed_match["parser_event_families"] == ["MatchState", "GameState", "GameResult"]
    assert sealed_match["parser_claim_families"] == [
        "sealed_event_identity",
        "sealed_match_state",
        "sealed_game_state",
        "sealed_game_result",
        "match_summary",
    ]
    assert sealed_match["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "sealed deckbuild remains missing" in sealed_match["review_notes"][0]
    sealed_deckbuild = _manifest_entry(manifest, "sealed_deckbuild_synthetic_v1")
    assert sealed_deckbuild["coverage_status"] == "covered_synthetic"
    assert sealed_deckbuild["scenario_families"] == ["core_gameplay.sealed_deckbuild"]
    assert sealed_deckbuild["parser_event_families"] == ["MatchState", "ClientAction"]
    assert sealed_deckbuild["parser_claim_families"] == [
        "sealed_event_identity",
        "sealed_submit_deck_signal",
        "bounded_submit_deck_shape",
        "deckbuild_privacy_boundary",
    ]
    assert sealed_deckbuild["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "submitted card lists" in sealed_deckbuild["review_notes"][0]
    assert "sealed pool contents" in sealed_deckbuild["review_notes"][0]
    connection_error = _manifest_entry(manifest, "connection_error_payload_synthetic_v1")
    assert connection_error["coverage_status"] == "covered_synthetic"
    assert connection_error["scenario_families"] == ["connection.connection_error_payload"]
    assert connection_error["parser_event_families"] == ["ConnectionError"]
    assert connection_error["parser_claim_families"] == [
        "connection_error_event",
        "connection_error_type_discriminator",
        "connection_error_payload_preservation",
        "connection_error_privacy_boundary",
    ]
    assert connection_error["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "does not prove reconnect" in connection_error["review_notes"][0]
    assert "release readiness" in connection_error["review_notes"][0]
    connection_reconnect = _manifest_entry(manifest, "connection_reconnect_synthetic_v1")
    assert connection_reconnect["coverage_status"] == "covered_synthetic"
    assert connection_reconnect["scenario_families"] == ["connection.reconnect"]
    assert connection_reconnect["parser_event_families"] == ["ConnectionError"]
    assert connection_reconnect["parser_claim_families"] == [
        "reconnect_result_payload",
        "reconnect_outcome_payload",
        "gre_connection_lost_reconnect_context",
        "reconnect_privacy_boundary",
    ]
    assert connection_reconnect["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "live reconnect success" in connection_reconnect["known_gaps"][0]
    assert "network reliability" in connection_reconnect["known_gaps"][0]
    assert "firewall or network-drop behavior" in connection_reconnect["known_gaps"][0]
    assert "ConnectionError reconnect result/outcome metadata only" in connection_reconnect["review_notes"][0]
    assert "private smoke" in connection_reconnect["review_notes"][0]
    connection_disconnect = _manifest_entry(manifest, "connection_disconnect_synthetic_v1")
    assert connection_disconnect["coverage_status"] == "covered_synthetic"
    assert connection_disconnect["scenario_families"] == ["connection.disconnect"]
    assert connection_disconnect["parser_event_families"] == [
        "MatchConnectionState",
        "TcpConnectionClose",
        "WebSocketClosed",
    ]
    assert connection_disconnect["parser_claim_families"] == [
        "connection_state_transition",
        "tcp_connection_close_payload",
        "websocket_closed_payload",
        "disconnect_privacy_boundary",
    ]
    assert connection_disconnect["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "does not prove reconnect" in connection_disconnect["review_notes"][0]
    assert "firewall/drop behavior" in connection_disconnect["review_notes"][0]
    firewall_network_drop = _manifest_entry(manifest, "firewall_network_drop_private_evidence_boundary_v1")
    assert firewall_network_drop["entry_type"] == "local_private_report_summary"
    assert firewall_network_drop["source_kind"] == "local_private_report_only"
    assert firewall_network_drop["commit_status"] == "local_report_only"
    assert firewall_network_drop["privacy_class"] == "local_private_not_committed"
    assert firewall_network_drop["sanitization_status"] == "requires_review"
    assert firewall_network_drop["coverage_status"] == "blocked_private_evidence"
    assert firewall_network_drop["scenario_families"] == ["connection.firewall_or_network_drop"]
    assert firewall_network_drop["parser_event_families"] == []
    assert firewall_network_drop["parser_claim_families"] == [
        "firewall_network_drop_private_evidence_required",
        "connection_adjacent_rows_non_claim",
        "network_reliability_non_claim",
        "private_artifact_boundary",
    ]
    assert firewall_network_drop["coverage_basis"] == ["local_report_only"]
    assert "future approved private/live evidence" in firewall_network_drop["known_gaps"][0]
    assert "generic connection errors" in firewall_network_drop["known_gaps"][0]
    assert "reconnect metadata" in firewall_network_drop["known_gaps"][0]
    assert "synthetic text do not prove firewall behavior" in firewall_network_drop["known_gaps"][0]
    assert "blocked by private/live evidence requirements" in firewall_network_drop["review_notes"][0]
    assert "adjacent connection error, reconnect, and disconnect corpus rows do not prove" in (
        firewall_network_drop["review_notes"][0]
    )
    opponent_auto_concede = _manifest_entry(manifest, "opponent_auto_concede_boundary_report_v1")
    assert opponent_auto_concede["coverage_status"] == "covered_report_only"
    assert opponent_auto_concede["scenario_families"] == ["gameplay_stress.opponent_auto_concede"]
    assert opponent_auto_concede["parser_event_families"] == []
    assert opponent_auto_concede["parser_claim_families"] == [
        "opponent_auto_concede_boundary_report",
        "normal_game_result_not_auto_concede",
        "no_action_not_inferred",
        "concession_intent_not_claimed",
        "game_end_edge_fixture_required",
        "gameplay_advice_non_claim",
    ]
    assert opponent_auto_concede["coverage_basis"] == ["fixture_metadata_only"]
    assert "report-only boundary metadata" in opponent_auto_concede["known_gaps"][0]
    assert "normal game-result and final-reconciliation evidence" in opponent_auto_concede["known_gaps"][0]
    assert "does not prove auto-concede behavior" in opponent_auto_concede["known_gaps"][0]
    assert "hidden opponent actions" in opponent_auto_concede["known_gaps"][0]
    assert "normal GameResult" in opponent_auto_concede["review_notes"][0]
    assert "public-taxonomy evidence do not prove" in opponent_auto_concede["review_notes"][0]
    companion_large_deck = _manifest_entry(manifest, "companion_large_deck_boundary_report_v1")
    assert companion_large_deck["coverage_status"] == "covered_report_only"
    assert companion_large_deck["scenario_families"] == ["gameplay_stress.companion_or_large_deck"]
    assert companion_large_deck["parser_event_families"] == []
    assert companion_large_deck["parser_claim_families"] == [
        "companion_large_deck_boundary_report",
        "generic_deck_snapshot_not_companion_or_large_deck",
        "submitted_deck_cards_not_decklist_truth",
        "card_identity_not_deck_shape_truth",
        "companion_legality_not_claimed",
        "decklist_completion_non_claim",
    ]
    assert companion_large_deck["coverage_basis"] == ["fixture_metadata_only"]
    assert "report-only boundary metadata" in companion_large_deck["known_gaps"][0]
    assert "adjacent deck/card evidence surfaces" in companion_large_deck["known_gaps"][0]
    assert "do not prove companion presence" in companion_large_deck["known_gaps"][0]
    assert "large-deck size" in companion_large_deck["known_gaps"][0]
    assert "complete decklist contents" in companion_large_deck["known_gaps"][0]
    assert "generic deck snapshots" in companion_large_deck["review_notes"][0]
    assert "submitted-deck card-content evidence" in companion_large_deck["review_notes"][0]
    assert "card identity provenance" in companion_large_deck["review_notes"][0]
    assert "do not prove companion presence" in companion_large_deck["review_notes"][0]
    gameplay_action_attribution = _manifest_entry(manifest, "gameplay_action_attribution_boundary_report_v1")
    assert gameplay_action_attribution["coverage_status"] == "covered_report_only"
    assert gameplay_action_attribution["scenario_families"] == ["gameplay_stress.action_attribution"]
    assert gameplay_action_attribution["parser_event_families"] == []
    assert gameplay_action_attribution["parser_claim_families"] == [
        "gameplay_action_attribution_boundary_report",
        "gameplay_action_extraction_not_stress_coverage",
        "opponent_card_observation_not_action_attribution_truth",
        "action_log_row_not_causal_truth",
        "analytics_ingest_not_parser_truth",
        "event_ordering_not_claimed",
        "hidden_action_inference_non_claim",
    ]
    assert gameplay_action_attribution["coverage_basis"] == ["fixture_metadata_only"]
    assert "report-only boundary metadata" in gameplay_action_attribution["known_gaps"][0]
    assert "gameplay-action extraction" in gameplay_action_attribution["known_gaps"][0]
    assert "do not prove action-attribution parser stress support" in (
        gameplay_action_attribution["known_gaps"][0]
    )
    assert "event ordering" in gameplay_action_attribution["known_gaps"][0]
    assert "hidden actions" in gameplay_action_attribution["known_gaps"][0]
    assert "gameplay-action extraction" in gameplay_action_attribution["review_notes"][0]
    assert "opponent-card observations" in gameplay_action_attribution["review_notes"][0]
    assert "analytics gameplay-action ingest" in gameplay_action_attribution["review_notes"][0]
    assert "do not prove action-attribution stress support" in gameplay_action_attribution["review_notes"][0]
    gameplay_event_ordering = _manifest_entry(manifest, "gameplay_event_ordering_boundary_report_v1")
    assert gameplay_event_ordering["coverage_status"] == "covered_report_only"
    assert gameplay_event_ordering["scenario_families"] == ["gameplay_stress.event_ordering"]
    assert gameplay_event_ordering["parser_event_families"] == []
    assert gameplay_event_ordering["parser_claim_families"] == [
        "gameplay_event_ordering_boundary_report",
        "parser_timestamps_not_complete_ordering_truth",
        "router_dispatch_order_not_stress_coverage",
        "gameplay_action_order_not_event_sequence_truth",
        "action_attribution_not_event_ordering_truth",
        "diagnostics_replay_reports_not_parser_truth",
        "hidden_action_inference_non_claim",
    ]
    assert gameplay_event_ordering["coverage_basis"] == ["fixture_metadata_only"]
    assert "report-only boundary metadata" in gameplay_event_ordering["known_gaps"][0]
    assert "do not prove event-ordering parser stress support" in gameplay_event_ordering["known_gaps"][0]
    assert "complete event-sequence truth" in gameplay_event_ordering["known_gaps"][0]
    assert "causal ordering truth" in gameplay_event_ordering["known_gaps"][0]
    assert "hidden actions" in gameplay_event_ordering["known_gaps"][0]
    assert "action-attribution support beyond issue #410" in gameplay_event_ordering["known_gaps"][0]
    assert "parser timestamps" in gameplay_event_ordering["review_notes"][0]
    assert "router dispatch order" in gameplay_event_ordering["review_notes"][0]
    assert "gameplay-action row order" in gameplay_event_ordering["review_notes"][0]
    assert "action-attribution report-only coverage" in gameplay_event_ordering["review_notes"][0]
    assert "do not prove complete event-sequence truth" in gameplay_event_ordering["review_notes"][0]
    detailed_logs_disabled = _manifest_entry(manifest, "detailed_logs_disabled_synthetic_v1")
    assert detailed_logs_disabled["coverage_status"] == "covered_synthetic"
    assert detailed_logs_disabled["scenario_families"] == ["log_runtime.detailed_logs_disabled"]
    assert detailed_logs_disabled["parser_event_families"] == ["DetailedLoggingStatus"]
    assert detailed_logs_disabled["parser_claim_families"] == [
        "detailed_logging_status_event",
        "detailed_logs_disabled_marker",
        "detailed_logging_metadata_parser",
        "detailed_logging_privacy_boundary",
    ]
    assert detailed_logs_disabled["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "does not prove live MTGA settings" in detailed_logs_disabled["review_notes"][0]
    assert "unknown-entry routing" in detailed_logs_disabled["review_notes"][0]
    timestamp_anomaly = _manifest_entry(manifest, "timestamp_anomaly_synthetic_v1")
    assert timestamp_anomaly["coverage_status"] == "covered_synthetic"
    assert timestamp_anomaly["scenario_families"] == ["log_runtime.timestamp_anomaly"]
    assert timestamp_anomaly["parser_event_families"] == []
    assert timestamp_anomaly["parser_claim_families"] == [
        "router_timestamp_missing_stat",
        "router_timestamp_parse_failure_stat",
        "router_timestamp_anomalies_aggregate",
        "timestamp_anomaly_privacy_boundary",
    ]
    assert timestamp_anomaly["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "router-owned timestamp_missing" in timestamp_anomaly["review_notes"][0]
    assert "malformed/headerless log handling" in timestamp_anomaly["review_notes"][0]
    assert "unknown-entry routing" in timestamp_anomaly["review_notes"][0]
    assert "real local Player.log timestamp drift" in timestamp_anomaly["review_notes"][0]
    malformed_headerless = _manifest_entry(manifest, "malformed_headerless_synthetic_v1")
    assert malformed_headerless["coverage_status"] == "covered_synthetic"
    assert malformed_headerless["scenario_families"] == ["log_runtime.malformed_or_headerless"]
    assert malformed_headerless["parser_event_families"] == []
    assert malformed_headerless["parser_claim_families"] == [
        "line_buffer_header_classification",
        "line_buffer_headerless_orphan_noise_ignored",
        "line_buffer_unknown_header_boundary",
        "line_buffer_partial_line_boundary",
        "line_buffer_multiline_boundary",
        "malformed_headerless_privacy_boundary",
    ]
    assert malformed_headerless["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "line-buffer and header-boundary metadata only" in malformed_headerless["review_notes"][0]
    assert "unknown-entry routing" in malformed_headerless["review_notes"][0]
    assert "semantic recovery from arbitrary malformed Player.log payloads" in malformed_headerless["review_notes"][0]
    active_player_timer = _manifest_entry(manifest, "active_player_timer_synthetic_v1")
    assert active_player_timer["coverage_status"] == "covered_synthetic"
    assert active_player_timer["scenario_families"] == ["timer.active_player_timer"]
    assert active_player_timer["parser_event_families"] == ["GameState"]
    assert active_player_timer["parser_claim_families"] == [
        "gre_timer_normalization",
        "active_player_timer_record",
        "active_player_timer_direct_seat_evidence",
        "timer_turn_info_context_boundary",
        "timer_time_unit_boundary",
        "timer_privacy_boundary",
    ]
    assert active_player_timer["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "normalized_timers GameState metadata" in active_player_timer["review_notes"][0]
    assert "does not infer timer ownership from turn_info context" in active_player_timer["review_notes"][0]
    assert "inactivity-timeout" in active_player_timer["review_notes"][0]
    assert "clock-pressure" in active_player_timer["review_notes"][0]
    assert "gameplay-advice" in active_player_timer["review_notes"][0]
    pre_match_idle_timer = _manifest_entry(manifest, "pre_match_idle_timer_synthetic_v1")
    assert pre_match_idle_timer["coverage_status"] == "covered_synthetic"
    assert pre_match_idle_timer["scenario_families"] == ["timer.pre_match_idle"]
    assert pre_match_idle_timer["parser_event_families"] == ["GameState"]
    assert pre_match_idle_timer["parser_claim_families"] == [
        "gre_timer_normalization",
        "pre_match_idle_timer_record",
        "pre_match_idle_no_direct_seat_boundary",
        "pre_match_idle_time_unit_boundary",
        "timer_privacy_boundary",
    ]
    assert pre_match_idle_timer["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "no-direct-seat timer shape" in pre_match_idle_timer["review_notes"][0]
    assert "does not infer player ownership" in pre_match_idle_timer["review_notes"][0]
    assert "inactivity timeout" in pre_match_idle_timer["review_notes"][0]
    assert "clock pressure" in pre_match_idle_timer["review_notes"][0]
    assert "gameplay advice" in pre_match_idle_timer["review_notes"][0]
    assert "private Player.log timer drift" in pre_match_idle_timer["known_gaps"][0]
    start_hook_deck_snapshot = _manifest_entry(manifest, "start_hook_deck_snapshot_synthetic_v1")
    assert start_hook_deck_snapshot["coverage_status"] == "covered_synthetic"
    assert start_hook_deck_snapshot["scenario_families"] == ["deck_api.start_hook_deck_snapshot"]
    assert start_hook_deck_snapshot["parser_event_families"] == ["Collection", "DeckCollection"]
    assert start_hook_deck_snapshot["parser_claim_families"] == [
        "start_hook_collection_snapshot",
        "start_hook_deck_collection_snapshot",
        "start_hook_deck_summary_to_deck_map_correlation",
        "start_hook_raw_evidence_preservation",
        "start_hook_deck_snapshot_privacy_boundary",
    ]
    assert start_hook_deck_snapshot["coverage_basis"] == [
        "fixture_metadata_only",
        "parser_behavior_verified",
    ]
    assert "bounded deck snapshot as evidence" in start_hook_deck_snapshot["review_notes"][0]
    assert "does not claim deck identity" in start_hook_deck_snapshot["review_notes"][0]
    assert "deck-summary coverage" in start_hook_deck_snapshot["known_gaps"][0]
    assert "store/pack/inbox/crafting coverage" in start_hook_deck_snapshot["known_gaps"][0]
    deck_summary_boundary = _manifest_entry(manifest, "deck_summary_boundary_report_v1")
    assert deck_summary_boundary["coverage_status"] == "covered_report_only"
    assert deck_summary_boundary["scenario_families"] == ["deck_api.deck_summary"]
    assert deck_summary_boundary["parser_event_families"] == []
    assert deck_summary_boundary["parser_claim_families"] == [
        "deck_summary_boundary_report",
        "start_hook_deck_summaries_reference_only",
        "dedicated_deck_summary_api_not_claimed",
        "deck_summary_privacy_boundary",
    ]
    assert deck_summary_boundary["coverage_basis"] == ["fixture_metadata_only"]
    assert "parser_behavior_verified" not in deck_summary_boundary["coverage_basis"]
    assert "StartHook-bound and report-only" in deck_summary_boundary["known_gaps"][0]
    assert "dedicated deck-summary API parser" in deck_summary_boundary["known_gaps"][0]
    assert "deck-upsert coverage" in deck_summary_boundary["known_gaps"][0]
    assert "store/pack/inbox/crafting coverage" in deck_summary_boundary["known_gaps"][0]
    assert "report-only boundary metadata" in deck_summary_boundary["review_notes"][0]
    assert "does not claim a standalone deck-summary API parser" in deck_summary_boundary["review_notes"][0]
    assert "deck identity/submitted-deck truth" in deck_summary_boundary["review_notes"][0]
    deck_upsert_boundary = _manifest_entry(manifest, "deck_upsert_boundary_report_v1")
    assert deck_upsert_boundary["coverage_status"] == "covered_report_only"
    assert deck_upsert_boundary["scenario_families"] == ["deck_api.deck_upsert"]
    assert deck_upsert_boundary["parser_event_families"] == []
    assert deck_upsert_boundary["parser_claim_families"] == [
        "deck_upsert_boundary_report",
        "event_set_deck_reference_only",
        "submit_deck_reference_only",
        "dedicated_deck_upsert_api_not_claimed",
        "deck_upsert_privacy_boundary",
    ]
    assert deck_upsert_boundary["coverage_basis"] == ["fixture_metadata_only"]
    assert "parser_behavior_verified" not in deck_upsert_boundary["coverage_basis"]
    assert "event-set deck coverage" in deck_upsert_boundary["known_gaps"][0]
    assert "dedicated deck-upsert API parser support" in deck_upsert_boundary["known_gaps"][0]
    assert "submitted-deck truth beyond existing parser-owned fields" in deck_upsert_boundary["known_gaps"][0]
    assert "intentionally report-only" in deck_upsert_boundary["review_notes"][0]
    assert "not deck-upsert evidence" in deck_upsert_boundary["review_notes"][0]
    store_pack_boundary = _manifest_entry(manifest, "store_pack_inbox_crafting_boundary_report_v1")
    assert store_pack_boundary["coverage_status"] == "covered_report_only"
    assert store_pack_boundary["scenario_families"] == ["deck_api.store_pack_inbox_or_crafting"]
    assert store_pack_boundary["parser_event_families"] == []
    assert store_pack_boundary["parser_claim_families"] == [
        "store_pack_inbox_crafting_boundary_report",
        "inventory_info_reference_only",
        "store_api_not_claimed",
        "pack_inbox_crafting_not_claimed",
        "inventory_economy_privacy_boundary",
    ]
    assert store_pack_boundary["coverage_basis"] == ["fixture_metadata_only"]
    assert "parser_behavior_verified" not in store_pack_boundary["coverage_basis"]
    assert "InventoryInfo snapshot parsing" in store_pack_boundary["known_gaps"][0]
    assert "store API parsing" in store_pack_boundary["known_gaps"][0]
    assert "pack-opening parsing" in store_pack_boundary["known_gaps"][0]
    assert "crafting/wildcard truth" in store_pack_boundary["known_gaps"][0]
    assert "intentionally report-only" in store_pack_boundary["review_notes"][0]
    assert "not store/pack/inbox/crafting evidence" in store_pack_boundary["review_notes"][0]
    unknown_entry = _manifest_entry(manifest, "unknown_entry_drift_report_reference_v1")
    assert unknown_entry["coverage_status"] == "covered_report_only"
    assert unknown_entry["scenario_families"] == ["log_runtime.unknown_entry"]
    assert unknown_entry["parser_event_families"] == []
    assert unknown_entry["parser_claim_families"] == [
        "router_unknown_entry_count",
        "drift_unknown_signature_review_samples",
        "drift_unmatched_api_name_review_samples",
        "diagnostics_unknown_entries_review_status",
        "evidence_ledger_unknown_entry_count_boundary",
        "unknown_entry_privacy_boundary",
    ]
    assert unknown_entry["coverage_basis"] == [
        "diagnostics_only",
        "fixture_metadata_only",
        "evidence_ledger_only",
    ]
    assert unknown_entry["paths"]["normalized_drift_report_reference"] == (
        "tests/fixtures/player_log_drift_flush_timing_expected.json"
    )
    assert "flush_timing_corpus_slice.log" not in unknown_entry["paths"].values()
    assert "unknown counts and review samples" in unknown_entry["review_notes"][0]
    assert "does not mean the parser understood the unknown entries" in unknown_entry["review_notes"][0]
    assert "parser support for unknown semantic content" in unknown_entry["known_gaps"][0]
    assert "live private Player.log drift health" in unknown_entry["known_gaps"][0]
    missing_message_type = _manifest_entry(manifest, "missing_message_type_boundary_report_v1")
    assert missing_message_type["coverage_status"] == "covered_report_only"
    assert missing_message_type["scenario_families"] == ["drift_debug.missing_message_type"]
    assert missing_message_type["parser_event_families"] == []
    assert missing_message_type["parser_claim_families"] == [
        "missing_message_type_boundary_report",
        "unknown_entry_not_missing_message_type_truth",
        "gsm_truncation_not_type_field_failure_truth",
        "timestamp_anomaly_not_message_type_truth",
        "generic_client_action_not_drift_debug_support",
        "gre_game_state_message_type_not_recovery_truth",
        "message_recovery_non_claim",
    ]
    assert missing_message_type["coverage_basis"] == ["fixture_metadata_only"]
    assert "report-only boundary metadata" in missing_message_type["known_gaps"][0]
    assert "do not prove missing-message-type parser support" in missing_message_type["known_gaps"][0]
    assert "parser message recovery" in missing_message_type["known_gaps"][0]
    assert "GameState reconstruction" in missing_message_type["known_gaps"][0]
    assert "unknown future MTGA message support" in missing_message_type["known_gaps"][0]
    assert "unknown-entry drift reporting" in missing_message_type["review_notes"][0]
    assert "GSM truncation coverage" in missing_message_type["review_notes"][0]
    assert "generic client-action fallback" in missing_message_type["review_notes"][0]
    assert "do not prove parser message recovery" in missing_message_type["review_notes"][0]
    rename_rotation_collision = _manifest_entry(
        manifest,
        "rename_rotation_collision_boundary_report_v1",
    )
    assert rename_rotation_collision["coverage_status"] == "covered_report_only"
    assert rename_rotation_collision["scenario_families"] == [
        "drift_debug.rename_or_rotation_collision"
    ]
    assert rename_rotation_collision["parser_event_families"] == []
    assert rename_rotation_collision["parser_claim_families"] == [
        "rename_rotation_collision_boundary_report",
        "tailer_rotation_not_collision_truth",
        "log_runtime_rotation_not_collision_truth",
        "recycle_or_rollback_not_collision_truth",
        "unknown_entry_not_collision_truth",
        "timestamp_anomaly_not_collision_truth",
        "missing_message_type_not_collision_truth",
        "file_system_truth_non_claim",
        "duplicate_replay_prevention_non_claim",
    ]
    assert rename_rotation_collision["coverage_basis"] == ["fixture_metadata_only"]
    assert "report-only boundary metadata" in rename_rotation_collision["known_gaps"][0]
    assert "do not prove rename/rotation collision parser support" in (
        rename_rotation_collision["known_gaps"][0]
    )
    assert "live file-system truth" in rename_rotation_collision["known_gaps"][0]
    assert "duplicate/replay prevention" in rename_rotation_collision["known_gaps"][0]
    assert "tailer/stream rotation signals" in rename_rotation_collision["review_notes"][0]
    assert "recycle/rollback boundaries" in rename_rotation_collision["review_notes"][0]
    assert "do not prove live file-system truth" in rename_rotation_collision["review_notes"][0]
    phantom_deck_origin = _manifest_entry(manifest, "phantom_deck_origin_boundary_report_v1")
    assert phantom_deck_origin["coverage_status"] == "covered_report_only"
    assert phantom_deck_origin["scenario_families"] == ["drift_debug.phantom_or_deck_origin"]
    assert phantom_deck_origin["parser_event_families"] == []
    assert phantom_deck_origin["parser_claim_families"] == [
        "phantom_deck_origin_boundary_report",
        "start_hook_deck_snapshot_not_deck_origin_truth",
        "deck_summary_not_deck_origin_truth",
        "deck_upsert_not_deck_origin_truth",
        "submitted_deck_not_phantom_truth",
        "deck_state_boundary_not_deck_origin_truth",
        "card_identity_not_hidden_card_truth",
        "gameplay_action_not_deck_origin_truth",
        "opponent_observation_not_hidden_card_truth",
        "runtime_active_deck_not_parser_truth",
        "analytics_ai_coaching_non_claim",
    ]
    assert phantom_deck_origin["coverage_basis"] == ["fixture_metadata_only"]
    assert "report-only boundary metadata" in phantom_deck_origin["known_gaps"][0]
    assert "do not prove phantom-card parser support" in phantom_deck_origin["known_gaps"][0]
    assert "deck-origin parser support" in phantom_deck_origin["known_gaps"][0]
    assert "hidden-card truth" in phantom_deck_origin["known_gaps"][0]
    assert "complete decklists" in phantom_deck_origin["known_gaps"][0]
    assert "exact deck identity" in phantom_deck_origin["known_gaps"][0]
    assert "adjacent deck" in phantom_deck_origin["review_notes"][0]
    assert "public taxonomy surfaces are non-claims" in phantom_deck_origin["review_notes"][0]
    assert "phantom-card support or deck-origin truth" in phantom_deck_origin["review_notes"][0]
    evidence_ledger_provenance = _manifest_entry(manifest, "evidence_ledger_provenance_report_reference_v1")
    assert evidence_ledger_provenance["coverage_status"] == "covered_report_only"
    assert evidence_ledger_provenance["scenario_families"] == ["mythic_edge.evidence_ledger_provenance"]
    assert evidence_ledger_provenance["parser_event_families"] == []
    assert evidence_ledger_provenance["parser_claim_families"] == [
        "evidence_ledger_schema",
        "evidence_ledger_entries",
        "evidence_schema_snapshot",
        "evidence_schema_drift_report",
        "evidence_invariant_execution",
        "runtime_field_evidence_mapping",
        "validation_report_wiring",
        "runtime_health_summary_boundary",
        "evidence_ledger_privacy_boundary",
    ]
    assert evidence_ledger_provenance["coverage_basis"] == [
        "evidence_ledger_only",
        "fixture_metadata_only",
        "count_ratchet_only",
    ]
    assert "parser_behavior_verified" not in evidence_ledger_provenance["coverage_basis"]
    assert "timer.pre_match_idle" in evidence_ledger_provenance["known_gaps"][0]
    assert "workbook row coverage" in evidence_ledger_provenance["known_gaps"][0]
    assert "confidence/finality/degradation coverage" in evidence_ledger_provenance["known_gaps"][0]
    assert "committed, deterministic provenance metadata" in evidence_ledger_provenance["review_notes"][0]
    assert "does not prove parser correctness for every field" in evidence_ledger_provenance["review_notes"][0]
    assert _session_entry(session_ledger, "gsm_truncation_marker_synthetic_v1")["parser_coverage"] == {
        "event_families": {"Truncation": 1},
        "unknown_entries": 0,
        "truncation_count": 1,
    }
    sealed_session = _session_entry(session_ledger, "sealed_entry_lifecycle_synthetic_v1")
    assert sealed_session["format_family"] == "limited_sealed"
    assert sealed_session["match_shape"] == "sealed_entry_only"
    assert sealed_session["parser_coverage"] == {
        "event_families": {"MatchState": 1, "EventLifecycle": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert sealed_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    connection_disconnect_session = _session_entry(session_ledger, "connection_disconnect_synthetic_v1")
    assert connection_disconnect_session["format_family"] == "connection_runtime"
    assert connection_disconnect_session["match_shape"] == "connection_disconnect_signal_only"
    assert connection_disconnect_session["parser_coverage"] == {
        "event_families": {"MatchConnectionState": 1, "TcpConnectionClose": 1, "WebSocketClosed": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert connection_disconnect_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert connection_disconnect_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    connection_reconnect_session = _session_entry(session_ledger, "connection_reconnect_synthetic_v1")
    assert connection_reconnect_session["format_family"] == "connection_runtime"
    assert connection_reconnect_session["match_shape"] == "connection_reconnect_signal_only"
    assert connection_reconnect_session["parser_coverage"] == {
        "event_families": {"ConnectionError": 5},
        "unknown_entries": 0,
        "truncation_count": 0,
        "reconnect_result_entries": 1,
        "reconnect_outcome_entries": 3,
        "gre_connection_lost_entries": 1,
    }
    assert connection_reconnect_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "live reconnect success" in connection_reconnect_session["known_gaps"][0]
    assert "network reliability" in connection_reconnect_session["known_gaps"][0]
    assert "firewall or network-drop behavior" in connection_reconnect_session["known_gaps"][0]
    assert connection_reconnect_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    detailed_logs_disabled_session = _session_entry(session_ledger, "detailed_logs_disabled_synthetic_v1")
    assert detailed_logs_disabled_session["format_family"] == "log_runtime"
    assert detailed_logs_disabled_session["match_shape"] == "detailed_logging_status_signal_only"
    assert detailed_logs_disabled_session["parser_coverage"] == {
        "event_families": {"DetailedLoggingStatus": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert detailed_logs_disabled_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert detailed_logs_disabled_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    timestamp_anomaly_session = _session_entry(session_ledger, "timestamp_anomaly_synthetic_v1")
    assert timestamp_anomaly_session["format_family"] == "log_runtime"
    assert timestamp_anomaly_session["match_shape"] == "timestamp_anomaly_signal_only"
    assert timestamp_anomaly_session["record_summary"] == "synthetic_router_stats_summary_only"
    assert timestamp_anomaly_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "timestamp_missing": 1,
        "timestamp_parse_failure": 1,
        "timestamp_anomalies": 2,
    }
    assert timestamp_anomaly_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert timestamp_anomaly_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    malformed_headerless_session = _session_entry(session_ledger, "malformed_headerless_synthetic_v1")
    assert malformed_headerless_session["format_family"] == "log_runtime"
    assert malformed_headerless_session["match_shape"] == "line_buffer_boundary_signal_only"
    assert malformed_headerless_session["record_summary"] == "synthetic_line_buffer_summary_only"
    assert malformed_headerless_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "line_buffer_headerless_orphan_lines_ignored": 1,
        "line_buffer_unknown_header_entries": 1,
        "line_buffer_partial_fragments_joined": 1,
        "line_buffer_multiline_entries_finalized": 1,
        "line_buffer_single_line_headers_emitted": 1,
    }
    assert malformed_headerless_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert malformed_headerless_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    active_player_timer_session = _session_entry(session_ledger, "active_player_timer_synthetic_v1")
    assert active_player_timer_session["format_family"] == "timer_runtime"
    assert active_player_timer_session["match_shape"] == "active_player_timer_signal_only"
    assert active_player_timer_session["record_summary"] == "synthetic_timer_normalization_summary_only"
    assert active_player_timer_session["parser_coverage"] == {
        "event_families": {"GameState": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
        "normalized_timer_records": 1,
        "active_player_timer_records": 1,
        "timer_records_with_direct_seat_evidence": 1,
        "timer_records_with_contextual_active_player": 1,
        "timer_records_with_seconds_values": 1,
        "timer_records_with_milliseconds_values": 1,
        "timer_degraded_records": 0,
    }
    assert active_player_timer_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert active_player_timer_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    pre_match_idle_session = _session_entry(session_ledger, "pre_match_idle_timer_synthetic_v1")
    assert pre_match_idle_session["format_family"] == "timer_runtime"
    assert pre_match_idle_session["match_shape"] == "pre_match_idle_timer_signal_only"
    assert pre_match_idle_session["record_summary"] == "synthetic_timer_normalization_summary_only"
    assert pre_match_idle_session["parser_coverage"] == {
        "event_families": {"GameState": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
        "normalized_timer_records": 1,
        "pre_match_idle_timer_records": 1,
        "timer_records_with_direct_seat_evidence": 0,
        "timer_records_without_direct_seat_evidence": 1,
        "timer_records_with_contextual_active_player": 0,
        "timer_records_with_seconds_values": 1,
        "timer_records_with_milliseconds_values": 1,
        "timer_degraded_records": 0,
    }
    assert pre_match_idle_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert pre_match_idle_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    start_hook_session = _session_entry(session_ledger, "start_hook_deck_snapshot_synthetic_v1")
    assert start_hook_session["format_family"] == "deck_api"
    assert start_hook_session["match_shape"] == "start_hook_deck_snapshot_signal_only"
    assert start_hook_session["record_summary"] == "synthetic_start_hook_summary_only"
    assert start_hook_session["parser_coverage"] == {
        "event_families": {"Collection": 1, "DeckCollection": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
        "start_hook_collection_snapshots": 1,
        "start_hook_deck_collection_snapshots": 1,
        "start_hook_correlated_decks": 1,
        "start_hook_orphaned_deck_summaries_skipped": 0,
        "start_hook_malformed_deck_summaries_skipped": 0,
    }
    assert start_hook_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert start_hook_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
        "private_deck_names_included": False,
        "private_collection_data_included": False,
    }
    deck_summary_session = _session_entry(session_ledger, "deck_summary_boundary_report_v1")
    assert deck_summary_session["format_family"] == "deck_api"
    assert deck_summary_session["match_shape"] == "deck_summary_boundary_report_only"
    assert deck_summary_session["record_summary"] == "committed_deck_summary_boundary_metadata_only"
    assert deck_summary_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "start_hook_deck_summaries_reference_entries": 1,
        "dedicated_deck_summary_api_events": 0,
        "dedicated_deck_summary_parser_routes": 0,
    }
    assert deck_summary_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "StartHook-bound report-only evidence" in deck_summary_session["known_gaps"][0]
    assert "dedicated deck-summary API parsing" in deck_summary_session["known_gaps"][0]
    assert "deck-upsert coverage" in deck_summary_session["known_gaps"][0]
    assert "store/pack/inbox/crafting coverage" in deck_summary_session["known_gaps"][0]
    assert deck_summary_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
        "private_deck_names_included": False,
        "private_collection_data_included": False,
    }
    deck_upsert_session = _session_entry(session_ledger, "deck_upsert_boundary_report_v1")
    assert deck_upsert_session["format_family"] == "deck_api"
    assert deck_upsert_session["match_shape"] == "deck_upsert_boundary_report_only"
    assert deck_upsert_session["record_summary"] == "committed_deck_upsert_boundary_metadata_only"
    assert deck_upsert_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "event_set_deck_reference_entries": 1,
        "submit_deck_reference_entries": 1,
        "dedicated_deck_upsert_api_events": 0,
        "dedicated_deck_upsert_parser_routes": 0,
    }
    assert deck_upsert_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "report-only metadata" in deck_upsert_session["known_gaps"][0]
    assert "dedicated deck-upsert API parsing" in deck_upsert_session["known_gaps"][0]
    assert "store/pack/inbox/crafting coverage" in deck_upsert_session["known_gaps"][0]
    assert deck_upsert_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
        "private_deck_names_included": False,
        "private_collection_data_included": False,
    }
    store_pack_session = _session_entry(session_ledger, "store_pack_inbox_crafting_boundary_report_v1")
    assert store_pack_session["format_family"] == "deck_api"
    assert store_pack_session["match_shape"] == "store_pack_inbox_crafting_boundary_report_only"
    assert store_pack_session["record_summary"] == "committed_store_pack_inbox_crafting_boundary_metadata_only"
    assert store_pack_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "inventory_info_reference_entries": 1,
        "dedicated_store_api_events": 0,
        "dedicated_pack_inbox_crafting_events": 0,
        "dedicated_economy_parser_routes": 0,
    }
    assert store_pack_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "report-only metadata" in store_pack_session["known_gaps"][0]
    assert "store API parsing" in store_pack_session["known_gaps"][0]
    assert "inbox/reward parsing" in store_pack_session["known_gaps"][0]
    assert "currency balances" in store_pack_session["known_gaps"][0]
    assert store_pack_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
        "private_deck_names_included": False,
        "private_collection_data_included": False,
        "private_economy_data_included": False,
        "currency_balances_included": False,
        "pack_inventory_included": False,
        "inbox_contents_included": False,
        "crafting_choices_included": False,
    }
    unknown_entry_session = _session_entry(session_ledger, "unknown_entry_drift_report_reference_v1")
    assert unknown_entry_session["format_family"] == "log_runtime"
    assert unknown_entry_session["match_shape"] == "unknown_entry_drift_report_reference_only"
    assert unknown_entry_session["record_summary"] == "normalized_drift_report_reference_only"
    assert unknown_entry_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 7,
        "truncation_count": 0,
        "drift_report_status": "review",
        "unknown_signatures": 4,
        "unmatched_api_names": 3,
        "unmatched_request_api_names": 3,
        "routed_event_families": 0,
    }
    assert unknown_entry_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert unknown_entry_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    missing_message_type_session = _session_entry(session_ledger, "missing_message_type_boundary_report_v1")
    assert missing_message_type_session["format_family"] == "drift_debug"
    assert missing_message_type_session["match_shape"] == "missing_message_type_boundary_report_only"
    assert missing_message_type_session["record_summary"] == (
        "committed_missing_message_type_boundary_metadata_only"
    )
    assert missing_message_type_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "unknown_entry_reference_entries": 1,
        "gsm_truncation_reference_entries": 1,
        "timestamp_anomaly_reference_entries": 1,
        "gre_game_state_reference_entries": 1,
        "client_action_reference_entries": 1,
        "diagnostics_reference_entries": 1,
        "evidence_ledger_reference_entries": 1,
        "dedicated_missing_message_type_fixtures": 0,
        "message_recovery_claims": 0,
        "game_state_reconstruction_claims": 0,
        "unknown_future_message_support_claims": 0,
    }
    assert missing_message_type_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "does not include a dedicated missing-message-type fixture" in (
        missing_message_type_session["known_gaps"][0]
    )
    assert "parser message recovery claim" in missing_message_type_session["known_gaps"][0]
    assert "GameState reconstruction claim" in missing_message_type_session["known_gaps"][0]
    assert "unknown future MTGA message support claim" in missing_message_type_session["known_gaps"][0]
    assert missing_message_type_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "message_bodies_included": False,
        "private_smoke_outputs_included": False,
        "generated_private_runtime_artifacts_included": False,
        "sqlite_files_included": False,
        "workbook_exports_included": False,
        "decklists_included": False,
        "card_choices_included": False,
        "strategy_notes_included": False,
        "credentials_tokens_keys_webhooks_included": False,
    }
    rename_rotation_session = _session_entry(session_ledger, "rename_rotation_collision_boundary_report_v1")
    assert rename_rotation_session["format_family"] == "drift_debug"
    assert rename_rotation_session["match_shape"] == "rename_rotation_collision_boundary_report_only"
    assert rename_rotation_session["record_summary"] == (
        "committed_rename_rotation_collision_boundary_metadata_only"
    )
    assert rename_rotation_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "tailer_rotation_reference_entries": 1,
        "stream_rotation_event_reference_entries": 1,
        "log_drift_reference_entries": 1,
        "diagnostics_reference_entries": 1,
        "golden_replay_reference_entries": 1,
        "feature_equity_reference_entries": 1,
        "dedicated_rename_rotation_collision_fixtures": 0,
        "file_identity_tracking_claims": 0,
        "rename_collision_detection_claims": 0,
        "recycle_collision_detection_claims": 0,
        "duplicate_replay_prevention_claims": 0,
        "private_smoke_success_claims": 0,
        "production_watcher_support_claims": 0,
    }
    assert rename_rotation_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "does not include a dedicated rename/rotation collision fixture" in (
        rename_rotation_session["known_gaps"][0]
    )
    assert "file identity tracking claim" in rename_rotation_session["known_gaps"][0]
    assert "duplicate/replay prevention claim" in rename_rotation_session["known_gaps"][0]
    assert "production watcher support claim" in rename_rotation_session["known_gaps"][0]
    assert rename_rotation_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "file_path_identities_included": False,
        "file_hashes_included": False,
        "byte_size_lists_included": False,
        "capture_date_rows_included": False,
        "private_smoke_outputs_included": False,
        "generated_private_runtime_artifacts_included": False,
        "sqlite_files_included": False,
        "workbook_exports_included": False,
        "decklists_included": False,
        "card_choices_included": False,
        "credentials_tokens_keys_webhooks_included": False,
    }
    phantom_deck_origin_session = _session_entry(session_ledger, "phantom_deck_origin_boundary_report_v1")
    assert phantom_deck_origin_session["format_family"] == "drift_debug"
    assert phantom_deck_origin_session["match_shape"] == "phantom_deck_origin_boundary_report_only"
    assert phantom_deck_origin_session["record_summary"] == (
        "committed_phantom_deck_origin_boundary_metadata_only"
    )
    assert phantom_deck_origin_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "deck_snapshot_reference_entries": 1,
        "deck_summary_reference_entries": 1,
        "deck_upsert_reference_entries": 1,
        "submitted_deck_reference_entries": 1,
        "deck_state_boundary_reference_entries": 1,
        "card_identity_reference_entries": 1,
        "gameplay_action_reference_entries": 1,
        "opponent_observation_reference_entries": 1,
        "diagnostics_reference_entries": 1,
        "evidence_ledger_reference_entries": 1,
        "dedicated_phantom_deck_origin_fixtures": 0,
        "phantom_card_detection_claims": 0,
        "deck_origin_truth_claims": 0,
        "hidden_card_inference_claims": 0,
        "complete_decklist_claims": 0,
        "archetype_classification_claims": 0,
        "gameplay_advice_claims": 0,
        "private_smoke_success_claims": 0,
    }
    assert phantom_deck_origin_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "does not include a dedicated phantom/deck-origin fixture" in (
        phantom_deck_origin_session["known_gaps"][0]
    )
    assert "phantom-card parser support claim" in phantom_deck_origin_session["known_gaps"][0]
    assert "deck-origin parser support claim" in phantom_deck_origin_session["known_gaps"][0]
    assert "hidden-card truth claim" in phantom_deck_origin_session["known_gaps"][0]
    assert "complete decklist claim" in phantom_deck_origin_session["known_gaps"][0]
    assert "private smoke success claim" in phantom_deck_origin_session["known_gaps"][0]
    assert phantom_deck_origin_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
        "deck_names_included": False,
        "deck_ids_included": False,
        "raw_submitted_deck_payloads_included": False,
        "card_choices_included": False,
        "sideboard_choices_included": False,
        "hidden_card_examples_included": False,
        "private_smoke_outputs_included": False,
        "generated_private_runtime_artifacts_included": False,
        "sqlite_files_included": False,
        "workbook_exports_included": False,
        "strategy_notes_included": False,
        "credentials_tokens_keys_webhooks_included": False,
    }
    evidence_ledger_session = _session_entry(session_ledger, "evidence_ledger_provenance_report_reference_v1")
    assert evidence_ledger_session["format_family"] == "mythic_edge_provenance"
    assert evidence_ledger_session["match_shape"] == "evidence_ledger_report_reference_only"
    assert evidence_ledger_session["record_summary"] == "committed_provenance_metadata_summary_only"
    assert evidence_ledger_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "evidence_ledger_output_families": 7,
        "evidence_ledger_entries": 71,
        "evidence_ledger_evidence_signals": 448,
        "evidence_schema_snapshot_status": "pass",
        "evidence_schema_drift_status": "pass",
        "evidence_invariant_execution_status": "pass",
        "executable_invariants": 11,
        "declared_invariants": 425,
        "declared_unique_invariants": 394,
        "runtime_field_evidence_surface": "available_review_sidecar",
        "validation_report_wiring_surface": "available_report_only",
        "runtime_health_surface": "available_summary_only",
    }
    assert evidence_ledger_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert evidence_ledger_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    sealed_match_session = _session_entry(session_ledger, "sealed_match_synthetic_v1")
    assert sealed_match_session["format_family"] == "limited_sealed"
    assert sealed_match_session["match_shape"] == "sealed_match_single_game"
    assert sealed_match_session["parser_coverage"] == {
        "event_families": {"MatchState": 1, "GameState": 1, "GameResult": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert sealed_match_session["game_rows"] == {"count": 1, "result_shape": "single_game_result"}
    assert sealed_match_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    sealed_deckbuild_session = _session_entry(session_ledger, "sealed_deckbuild_synthetic_v1")
    assert sealed_deckbuild_session["format_family"] == "limited_sealed"
    assert sealed_deckbuild_session["match_shape"] == "sealed_deckbuild_submit_deck_signal_only"
    assert sealed_deckbuild_session["parser_coverage"] == {
        "event_families": {"MatchState": 1, "ClientAction": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert sealed_deckbuild_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert sealed_deckbuild_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    connection_error_session = _session_entry(session_ledger, "connection_error_payload_synthetic_v1")
    assert connection_error_session["format_family"] == "connection_runtime"
    assert connection_error_session["match_shape"] == "connection_error_payload_signal_only"
    assert connection_error_session["parser_coverage"] == {
        "event_families": {"ConnectionError": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert connection_error_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert connection_error_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    draft_with_games_session = _session_entry(session_ledger, "draft_with_games_boundary_report_v1")
    assert draft_with_games_session["format_family"] == "limited_draft"
    assert draft_with_games_session["match_shape"] == "draft_with_games_boundary_report_only"
    assert draft_with_games_session["record_summary"] == "committed_draft_with_games_boundary_metadata_only"
    assert draft_with_games_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "draft_only_reference_entries": 1,
        "draft_parser_family_reference_entries": 1,
        "completed_draft_game_rows": 0,
        "game_result_events": 0,
        "match_result_events": 0,
        "dedicated_draft_with_games_fixtures": 0,
    }
    assert draft_with_games_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "report-only metadata" in draft_with_games_session["known_gaps"][0]
    assert "completed limited gameplay" in draft_with_games_session["known_gaps"][0]
    assert "game-result evidence" in draft_with_games_session["known_gaps"][0]
    assert "draft deck construction" in draft_with_games_session["known_gaps"][0]
    assert draft_with_games_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "draft_picks_included": False,
        "draft_pools_included": False,
        "decklists_included": False,
        "private_deck_names_included": False,
        "card_choices_included": False,
        "strategy_notes_included": False,
    }
    opponent_auto_concede_session = _session_entry(session_ledger, "opponent_auto_concede_boundary_report_v1")
    assert opponent_auto_concede_session["format_family"] == "gameplay_stress"
    assert opponent_auto_concede_session["match_shape"] == "opponent_auto_concede_boundary_report_only"
    assert opponent_auto_concede_session["record_summary"] == (
        "committed_opponent_auto_concede_boundary_metadata_only"
    )
    assert opponent_auto_concede_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "normal_game_result_reference_entries": 1,
        "dedicated_auto_concede_fixtures": 0,
        "dedicated_no_action_fixtures": 0,
        "concession_intent_claims": 0,
        "hidden_action_absence_claims": 0,
    }
    assert opponent_auto_concede_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "does not include a dedicated auto-concede/no-action fixture" in (
        opponent_auto_concede_session["known_gaps"][0]
    )
    assert "does not prove concession intent" in opponent_auto_concede_session["known_gaps"][0]
    assert "hidden action absence" in opponent_auto_concede_session["known_gaps"][0]
    assert opponent_auto_concede_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "opponent_identifiers_included": False,
        "private_match_context_included": False,
        "decklists_included": False,
        "card_choices_included": False,
        "strategy_notes_included": False,
    }
    companion_large_deck_session = _session_entry(session_ledger, "companion_large_deck_boundary_report_v1")
    assert companion_large_deck_session["format_family"] == "gameplay_stress"
    assert companion_large_deck_session["match_shape"] == "companion_large_deck_boundary_report_only"
    assert companion_large_deck_session["record_summary"] == (
        "committed_companion_large_deck_boundary_metadata_only"
    )
    assert companion_large_deck_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "deck_snapshot_reference_entries": 1,
        "submitted_deck_reference_entries": 1,
        "card_identity_reference_entries": 1,
        "dedicated_companion_fixtures": 0,
        "dedicated_large_deck_fixtures": 0,
        "companion_legality_claims": 0,
        "decklist_completion_claims": 0,
    }
    assert companion_large_deck_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert "does not include a dedicated companion fixture" in companion_large_deck_session["known_gaps"][0]
    assert "dedicated large-deck fixture" in companion_large_deck_session["known_gaps"][0]
    assert "large-deck size claim" in companion_large_deck_session["known_gaps"][0]
    assert "complete decklist claim" in companion_large_deck_session["known_gaps"][0]
    assert companion_large_deck_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "private_decklists_included": False,
        "raw_submitted_deck_payloads_included": False,
        "deck_names_included": False,
        "deck_ids_included": False,
        "sideboard_choices_included": False,
        "companion_candidates_included": False,
        "card_choices_included": False,
        "strategy_notes_included": False,
        "local_smoke_outputs_included": False,
        "generated_private_runtime_artifacts_included": False,
        "credentials_tokens_keys_webhooks_included": False,
    }
    gameplay_action_attribution_session = _session_entry(
        session_ledger,
        "gameplay_action_attribution_boundary_report_v1",
    )
    assert gameplay_action_attribution_session["format_family"] == "gameplay_stress"
    assert gameplay_action_attribution_session["match_shape"] == (
        "gameplay_action_attribution_boundary_report_only"
    )
    assert gameplay_action_attribution_session["record_summary"] == (
        "committed_gameplay_action_attribution_boundary_metadata_only"
    )
    assert gameplay_action_attribution_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "gameplay_action_reference_entries": 1,
        "opponent_card_observation_reference_entries": 1,
        "action_log_reference_entries": 1,
        "analytics_ingest_reference_entries": 1,
        "dedicated_action_attribution_fixtures": 0,
        "dedicated_event_ordering_fixtures": 0,
        "hidden_action_claims": 0,
        "causal_intent_claims": 0,
        "event_ordering_claims": 0,
    }
    assert gameplay_action_attribution_session["game_rows"] == {
        "count": 0,
        "result_shape": "not_applicable",
    }
    assert "does not include a dedicated action-attribution fixture" in (
        gameplay_action_attribution_session["known_gaps"][0]
    )
    assert "dedicated event-ordering fixture" in gameplay_action_attribution_session["known_gaps"][0]
    assert "hidden-action claim" in gameplay_action_attribution_session["known_gaps"][0]
    assert "causal-intent claim" in gameplay_action_attribution_session["known_gaps"][0]
    assert "event-ordering claim" in gameplay_action_attribution_session["known_gaps"][0]
    assert gameplay_action_attribution_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "private_action_artifacts_included": False,
        "private_smoke_outputs_included": False,
        "generated_private_runtime_artifacts_included": False,
        "decklists_included": False,
        "deck_names_included": False,
        "card_choices_included": False,
        "sideboard_choices_included": False,
        "strategy_notes_included": False,
        "opponent_identifiers_included": False,
        "private_match_context_included": False,
        "credentials_tokens_keys_webhooks_included": False,
    }
    gameplay_event_ordering_session = _session_entry(
        session_ledger,
        "gameplay_event_ordering_boundary_report_v1",
    )
    assert gameplay_event_ordering_session["format_family"] == "gameplay_stress"
    assert gameplay_event_ordering_session["match_shape"] == (
        "gameplay_event_ordering_boundary_report_only"
    )
    assert gameplay_event_ordering_session["record_summary"] == (
        "committed_gameplay_event_ordering_boundary_metadata_only"
    )
    assert gameplay_event_ordering_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "timestamp_reference_entries": 1,
        "router_dispatch_reference_entries": 1,
        "game_state_reference_entries": 1,
        "gameplay_action_reference_entries": 1,
        "diagnostics_reference_entries": 1,
        "golden_replay_reference_entries": 1,
        "feature_equity_reference_entries": 1,
        "dedicated_event_ordering_fixtures": 0,
        "dedicated_action_attribution_fixtures": 0,
        "hidden_action_claims": 0,
        "causal_ordering_claims": 0,
        "complete_sequence_claims": 0,
    }
    assert gameplay_event_ordering_session["game_rows"] == {
        "count": 0,
        "result_shape": "not_applicable",
    }
    assert "does not include a dedicated event-ordering fixture" in (
        gameplay_event_ordering_session["known_gaps"][0]
    )
    assert "complete event-sequence truth" in gameplay_event_ordering_session["known_gaps"][0]
    assert "causal-ordering claim" in gameplay_event_ordering_session["known_gaps"][0]
    assert "hidden-action claim" in gameplay_event_ordering_session["known_gaps"][0]
    assert "action-attribution support beyond issue #410" in (
        gameplay_event_ordering_session["known_gaps"][0]
    )
    assert gameplay_event_ordering_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "private_action_artifacts_included": False,
        "private_smoke_outputs_included": False,
        "generated_private_runtime_artifacts_included": False,
        "decklists_included": False,
        "deck_names_included": False,
        "card_choices_included": False,
        "sideboard_choices_included": False,
        "strategy_notes_included": False,
        "opponent_identifiers_included": False,
        "private_match_context_included": False,
        "credentials_tokens_keys_webhooks_included": False,
    }


def test_build_report_maps_corpus_coverage_without_parser_truth_claims() -> None:
    report = corpus.build_corpus_parity_report(MANIFEST_PATH, session_ledger_path=SESSION_LEDGER_PATH)

    assert report["object"] == corpus.REPORT_OBJECT
    assert report["schema_version"] == corpus.REPORT_SCHEMA_VERSION
    assert report["status"] == "partial_coverage_map_ready"
    assert report["inputs"]["corpus_manifest_path"] == "tests/fixtures/parser_corpus/corpus_manifest.v1.json"
    assert report["inputs"]["session_ledger_path"] == "tests/fixtures/parser_corpus/session_ledger.v1.json"
    assert report["summary"] == {
        "total_scenario_families": len(corpus.SCENARIO_FAMILIES),
        "covered_committed": 6,
        "covered_synthetic": 14,
        "covered_report_only": 13,
        "partial": 3,
        "missing": len(corpus.SCENARIO_FAMILIES) - 42,
        "deferred": 0,
        "blocked_private_evidence": 1,
        "blocked_external_boundary": 5,
        "not_applicable": 0,
    }
    assert _matrix_row(report, "core_gameplay.standard_bo1") == {
        "scenario_family": "core_gameplay.standard_bo1",
        "coverage_status": "covered_committed",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["bo1_match_win_basic"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "core_gameplay.draft_only") == {
        "scenario_family": "core_gameplay.draft_only",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["draft_parser_family"],
        "external_reference_status": "reference_category_not_checked",
        "notes": ["Synthetic draft parser-family slice covers draft events but not full limited match play."],
    }
    assert _matrix_row(report, "core_gameplay.draft_with_games") == {
        "scenario_family": "core_gameplay.draft_with_games",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["draft_with_games_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "The draft-with-games row is intentionally report-only and prevents false parity claims by "
            "documenting why the current draft-only fixture and synthetic GameState anchor are not "
            "draft-with-games evidence; future dedicated coverage remains blocked until Mythic Edge has "
            "owned, sanitized, parser-supported evidence for a completed draft session with games and results."
        ],
    }
    gsm_row = _matrix_row(report, "drift_debug.gsm_truncation")
    assert gsm_row["coverage_status"] == "covered_synthetic"
    assert gsm_row["coverage_status"] != "covered_committed"
    assert gsm_row["coverage_basis"] == [
        "count_ratchet_only",
        "diagnostics_only",
        "fixture_metadata_only",
        "parser_behavior_verified",
    ]
    assert gsm_row["mythic_edge_entries"] == [
        "feature_equity_corpus_baseline_v1",
        "gsm_truncation_marker_synthetic_v1",
    ]
    assert "GSM truncation is parser-owned data-loss evidence, not recovered GameState truth." in gsm_row["notes"]
    assert _matrix_row(report, "core_gameplay.sealed_entry") == {
        "scenario_family": "core_gameplay.sealed_entry",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["sealed_entry_lifecycle_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic sealed entry coverage proves sealed context plus event-entry lifecycle metadata only; "
            "sealed deckbuild and sealed matches remain missing."
        ],
    }
    assert _matrix_row(report, "core_gameplay.sealed_deckbuild") == {
        "scenario_family": "core_gameplay.sealed_deckbuild",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["sealed_deckbuild_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic sealed deckbuild coverage proves sealed context plus bounded submit-deck signal metadata "
            "only; it does not include submitted card lists, sealed pool contents, deck names, card choices, "
            "analytics truth, AI truth, or coaching truth."
        ],
    }
    assert _matrix_row(report, "core_gameplay.sealed_matches") == {
        "scenario_family": "core_gameplay.sealed_matches",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["sealed_match_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic sealed match coverage proves sealed context plus parser-owned match/game result summary "
            "metadata only; sealed deckbuild remains missing."
        ],
    }
    assert _matrix_row(report, "log_runtime.detailed_logs_disabled") == {
        "scenario_family": "log_runtime.detailed_logs_disabled",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["detailed_logs_disabled_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic detailed logs disabled coverage proves parser-owned DetailedLoggingStatus metadata only; "
            "it does not prove live MTGA settings, log rotation, malformed/headerless log handling, timestamp "
            "anomaly handling, unknown-entry routing, private smoke, release readiness, analytics truth, "
            "AI truth, coaching truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "log_runtime.rotation") == {
        "scenario_family": "log_runtime.rotation",
        "coverage_status": "blocked_external_boundary",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": ["external_reference_category_boundary"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Reference categories require future Mythic Edge fixtures or report-only evidence before support claims."
        ],
    }
    assert _matrix_row(report, "log_runtime.malformed_or_headerless") == {
        "scenario_family": "log_runtime.malformed_or_headerless",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["malformed_headerless_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic malformed/headerless coverage proves line-buffer and header-boundary metadata only; "
            "it does not prove unknown-entry routing, log drift detection, log rotation, semantic recovery "
            "from arbitrary malformed Player.log payloads, private smoke, release readiness, analytics truth, "
            "AI truth, coaching truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "log_runtime.timestamp_anomaly") == {
        "scenario_family": "log_runtime.timestamp_anomaly",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["timestamp_anomaly_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic timestamp anomaly coverage proves router-owned timestamp_missing, "
            "timestamp_parse_failure, and timestamp_anomalies stats only; it does not prove "
            "malformed/headerless log handling, unknown-entry routing, log rotation, real local "
            "Player.log timestamp drift, private smoke, release readiness, analytics truth, AI truth, "
            "coaching truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "log_runtime.unknown_entry") == {
        "scenario_family": "log_runtime.unknown_entry",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["diagnostics_only", "evidence_ledger_only", "fixture_metadata_only"],
        "mythic_edge_entries": ["unknown_entry_drift_report_reference_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Unknown-entry coverage proves that existing drift/diagnostics reports can surface unknown counts "
            "and review samples from a committed normalized report reference; it does not mean the parser "
            "understood the unknown entries."
        ],
    }
    assert _matrix_row(report, "drift_debug.missing_message_type") == {
        "scenario_family": "drift_debug.missing_message_type",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["missing_message_type_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Missing-message-type coverage is report-only boundary metadata: unknown-entry drift reporting, "
            "GSM truncation coverage, timestamp-anomaly coverage, generic client-action fallback, GRE "
            "GameState parsing, diagnostics, golden replay, feature-equity behavior, evidence-ledger "
            "provenance, and public taxonomy metadata do not prove parser message recovery, hidden payload "
            "truth, GameState reconstruction, unknown future MTGA message support, release readiness, "
            "production behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
        ],
    }
    assert _matrix_row(report, "drift_debug.rename_or_rotation_collision") == {
        "scenario_family": "drift_debug.rename_or_rotation_collision",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["rename_rotation_collision_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Rename/rotation collision coverage is report-only boundary metadata: tailer/stream rotation "
            "signals, log-runtime rotation boundaries, recycle/rollback boundaries, unknown-entry "
            "reporting, timestamp anomaly reporting, missing-message-type coverage, diagnostics, log-drift "
            "reports, golden replay, feature-equity, corpus parity metadata, and public taxonomy metadata "
            "do not prove live file-system truth, rename/recycle collision handling, duplicate/replay "
            "prevention, private smoke success, parser drift recovery truth, release readiness, production "
            "behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
        ],
    }
    assert _matrix_row(report, "drift_debug.recycle_or_rollback") == {
        "scenario_family": "drift_debug.recycle_or_rollback",
        "coverage_status": "blocked_external_boundary",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": ["external_reference_category_boundary"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Reference categories require future Mythic Edge fixtures or report-only evidence before support claims."
        ],
    }
    assert _matrix_row(report, "drift_debug.phantom_or_deck_origin") == {
        "scenario_family": "drift_debug.phantom_or_deck_origin",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["phantom_deck_origin_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Phantom/deck-origin coverage is intentionally report-only: adjacent deck, card identity, "
            "gameplay-action, opponent-observation, diagnostics, drift, evidence-ledger, runtime, "
            "analytics, AI, coaching, and public taxonomy surfaces are non-claims for phantom-card "
            "support or deck-origin truth."
        ],
    }
    assert _matrix_row(report, "mythic_edge.private_log_report_only_drift") == {
        "scenario_family": "mythic_edge.private_log_report_only_drift",
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "mythic_edge.evidence_ledger_provenance") == {
        "scenario_family": "mythic_edge.evidence_ledger_provenance",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["count_ratchet_only", "evidence_ledger_only", "fixture_metadata_only"],
        "mythic_edge_entries": ["evidence_ledger_provenance_report_reference_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Evidence-ledger provenance coverage proves that Mythic Edge has committed, deterministic "
            "provenance metadata and review scaffolding for parser-owned fact evidence; it does not prove "
            "parser correctness for every field or runtime attachment in every consumer."
        ],
    }
    assert _matrix_row(report, "mythic_edge.confidence_finality_degradation") == {
        "scenario_family": "mythic_edge.confidence_finality_degradation",
        "coverage_status": "partial",
        "coverage_basis": ["count_ratchet_only"],
        "mythic_edge_entries": ["feature_equity_corpus_baseline_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": ["Committed count-only baseline summarizes existing golden replay manifests."],
    }
    assert _matrix_row(report, "mythic_edge.workbook_row_coverage") == {
        "scenario_family": "mythic_edge.workbook_row_coverage",
        "coverage_status": "partial",
        "coverage_basis": ["count_ratchet_only"],
        "mythic_edge_entries": ["feature_equity_corpus_baseline_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": ["Committed count-only baseline summarizes existing golden replay manifests."],
    }
    assert _matrix_row(report, "mythic_edge.live_diagnostics") == {
        "scenario_family": "mythic_edge.live_diagnostics",
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "mythic_edge.analytics_readiness_labels") == {
        "scenario_family": "mythic_edge.analytics_readiness_labels",
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "connection.connection_error_payload") == {
        "scenario_family": "connection.connection_error_payload",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["connection_error_payload_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic connection error payload coverage proves parser-owned ConnectionError payload metadata "
            "only; it does not prove reconnect, disconnect, network reliability, private smoke, release "
            "readiness, analytics truth, AI truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "connection.reconnect") == {
        "scenario_family": "connection.reconnect",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["connection_reconnect_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic reconnect coverage proves parser-owned ConnectionError reconnect result/outcome "
            "metadata only; it does not prove live reconnect resilience, network reliability, firewall/drop "
            "behavior, private smoke, release readiness, analytics truth, AI truth, coaching truth, or "
            "production behavior."
        ],
    }
    assert _matrix_row(report, "connection.disconnect") == {
        "scenario_family": "connection.disconnect",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["connection_disconnect_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic connection disconnect coverage proves parser-owned MatchConnectionState, "
            "TcpConnectionClose, and WebSocketClosed metadata only; it does not prove reconnect, "
            "firewall/drop behavior, network reliability, private smoke, release readiness, analytics truth, "
            "AI truth, coaching truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "connection.firewall_or_network_drop") == {
        "scenario_family": "connection.firewall_or_network_drop",
        "coverage_status": "blocked_private_evidence",
        "coverage_basis": ["local_report_only"],
        "mythic_edge_entries": ["firewall_network_drop_private_evidence_boundary_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Firewall/network-drop coverage is blocked by private/live evidence requirements; adjacent "
            "connection error, reconnect, and disconnect corpus rows do not prove firewall/drop behavior, "
            "network reliability, private smoke success, release readiness, analytics truth, AI truth, "
            "coaching truth, or production behavior."
        ],
    }
    firewall_gap = next(
        gap for gap in report["gaps"] if gap["scenario_family"] == "connection.firewall_or_network_drop"
    )
    assert firewall_gap["gap_status"] == "blocked_private_evidence"
    assert firewall_gap["blocked_by"] == ["no_committed_safe_fixture", "private_evidence_required"]
    assert _matrix_row(report, "gameplay_stress.mulligan") == {
        "scenario_family": "gameplay_stress.mulligan",
        "coverage_status": "covered_committed",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["bo3_sideboard_match_loss"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "gameplay_stress.opponent_auto_concede") == {
        "scenario_family": "gameplay_stress.opponent_auto_concede",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["opponent_auto_concede_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Opponent auto-concede/no-action coverage is report-only boundary metadata: normal GameResult, "
            "local-win, opponent-loss, short-duration, sparse-action, and public-taxonomy evidence do not "
            "prove opponent auto-concede or no-action behavior."
        ],
    }
    assert _matrix_row(report, "gameplay_stress.conjure") == {
        "scenario_family": "gameplay_stress.conjure",
        "coverage_status": "blocked_external_boundary",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": ["external_reference_category_boundary"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Reference categories require future Mythic Edge fixtures or report-only evidence before support claims."
        ],
    }
    assert _matrix_row(report, "gameplay_stress.spellbook") == {
        "scenario_family": "gameplay_stress.spellbook",
        "coverage_status": "blocked_external_boundary",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": ["external_reference_category_boundary"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Reference categories require future Mythic Edge fixtures or report-only evidence before support claims."
        ],
    }
    assert _matrix_row(report, "gameplay_stress.companion_or_large_deck") == {
        "scenario_family": "gameplay_stress.companion_or_large_deck",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["companion_large_deck_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Companion / large-deck coverage is report-only boundary metadata: generic deck snapshots, "
            "submitted-deck card-content evidence, StartHook summaries, card identity provenance, and "
            "public taxonomy metadata do not prove companion presence, companion legality, large-deck "
            "size, complete decklists, deck identity, hidden-card truth, archetype classification, "
            "gameplay advice, analytics truth, AI truth, coaching truth, release readiness, or "
            "production behavior."
        ],
    }
    assert _matrix_row(report, "gameplay_stress.action_attribution") == {
        "scenario_family": "gameplay_stress.action_attribution",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["gameplay_action_attribution_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Gameplay action-attribution coverage is report-only boundary metadata: gameplay-action "
            "extraction, opponent-card observations, ActionLogRow surfaces, analytics gameplay-action "
            "ingest, evidence-ledger provenance, and public taxonomy metadata do not prove "
            "action-attribution stress support, causal truth, hidden actions, hidden cards, opponent "
            "intent, event ordering, player mistakes, gameplay advice, analytics truth, AI truth, "
            "coaching truth, release readiness, or production behavior."
        ],
    }
    assert _matrix_row(report, "gameplay_stress.event_ordering") == {
        "scenario_family": "gameplay_stress.event_ordering",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["gameplay_event_ordering_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Gameplay event-ordering coverage is report-only boundary metadata: parser timestamps, "
            "router dispatch order, gameplay-action row order, action-attribution report-only coverage, "
            "diagnostics reports, golden replay reports, feature-equity reports, evidence-ledger "
            "provenance, analytics ingest, and public taxonomy metadata do not prove complete "
            "event-sequence truth, causal ordering truth, hidden actions, hidden cards, opponent intent, "
            "player mistakes, gameplay advice, analytics truth, AI truth, coaching truth, release "
            "readiness, or production behavior."
        ],
    }
    assert _matrix_row(report, "timer.active_player_timer") == {
        "scenario_family": "timer.active_player_timer",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["active_player_timer_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic active player timer coverage proves parser-owned normalized_timers GameState metadata "
            "only; it does not infer timer ownership from turn_info context or claim clock-pressure, rope, "
            "inactivity-timeout, gameplay-advice, analytics, AI, coaching, release, or production truth."
        ],
    }
    assert _matrix_row(report, "timer.inactivity_timeout") == {
        "scenario_family": "timer.inactivity_timeout",
        "coverage_status": "blocked_external_boundary",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": ["external_reference_category_boundary"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Reference categories require future Mythic Edge fixtures or report-only evidence before support claims."
        ],
    }
    assert _matrix_row(report, "timer.pre_match_idle") == {
        "scenario_family": "timer.pre_match_idle",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["pre_match_idle_timer_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic pre-match idle timer coverage proves parser-owned normalized_timers GameState metadata "
            "for a no-direct-seat timer shape only; it does not infer player ownership, inactivity timeout, "
            "rope behavior, clock pressure, gameplay advice, analytics, AI, coaching, release, or production "
            "truth."
        ],
    }
    assert _matrix_row(report, "deck_api.start_hook_deck_snapshot") == {
        "scenario_family": "deck_api.start_hook_deck_snapshot",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["start_hook_deck_snapshot_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic StartHook deck snapshot coverage proves parser-owned Collection and DeckCollection "
            "StartHook metadata only; it preserves a bounded deck snapshot as evidence and does not claim "
            "deck identity, submitted-deck, sideboard-delta, inventory/economy, analytics, AI, coaching, "
            "release, or production truth."
        ],
    }
    assert _matrix_row(report, "deck_api.deck_summary") == {
        "scenario_family": "deck_api.deck_summary",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["deck_summary_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Deck summary coverage is report-only boundary metadata: Mythic Edge has StartHook "
            "DeckSummaries evidence through the existing DeckCollection parser and #392 coverage, but "
            "does not claim a standalone deck-summary API parser or deck identity/submitted-deck truth."
        ],
    }
    assert _matrix_row(report, "deck_api.deck_upsert") == {
        "scenario_family": "deck_api.deck_upsert",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["deck_upsert_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "The deck-upsert row is intentionally report-only and prevents false parity claims by documenting "
            "why nearby event-set, deck-summary, StartHook, submit-deck, and submitted-deck-card evidence is "
            "not deck-upsert evidence; future dedicated deck-upsert fixture work remains blocked until Mythic "
            "Edge has owned, sanitized, parser-supported evidence."
        ],
    }
    assert _matrix_row(report, "deck_api.event_set_deck") == {
        "scenario_family": "deck_api.event_set_deck",
        "coverage_status": "covered_committed",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["bo1_match_win_basic"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "deck_api.store_pack_inbox_or_crafting") == {
        "scenario_family": "deck_api.store_pack_inbox_or_crafting",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["fixture_metadata_only"],
        "mythic_edge_entries": ["store_pack_inbox_crafting_boundary_report_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "The store/pack/inbox/crafting row is intentionally report-only and prevents false parity claims "
            "by documenting why InventoryInfo, StartHook deck snapshot, deck-summary, deck-upsert, event-set "
            "deck, submit-deck, and submitted-deck-card evidence is not store/pack/inbox/crafting evidence; "
            "future dedicated coverage remains blocked until Mythic Edge has owned, sanitized, "
            "parser-supported evidence for a narrower store, pack, inbox, reward, crafting, transaction, or "
            "economy surface."
        ],
    }
    assert report["privacy"] == {
        "raw_private_log_committed": False,
        "external_logs_committed": False,
        "raw_log_lines_in_report": False,
        "local_absolute_paths_redacted": True,
        "forbidden_content_findings": [],
    }
    assert all(value is False for value in report["protected_surfaces"].values())
    assert any("Reports do not decide merge readiness" in item for item in report["limitations"])


def test_private_manifest_metadata_blocks_without_echoing_sensitive_path(tmp_path: Path) -> None:
    manifest = _manifest_payload()
    private_path = "/" + "Users/example/private/session-data.txt"
    manifest["source_privacy"]["raw_private_log_committed"] = True
    manifest["entries"][0]["review_notes"] = [f"{private_path} should stay out of reports"]
    manifest_path = _write_json(tmp_path, "private-manifest.json", manifest)

    report = corpus.build_corpus_parity_report(manifest_path, session_ledger_path=SESSION_LEDGER_PATH)
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "blocked_private_artifact_risk"
    assert "source_privacy_not_false:raw_private_log_committed" in report["status_reasons"]
    assert "forbidden_content:local_absolute_path" in report["status_reasons"]
    assert private_path not in encoded
    assert "<redacted-local-path>" in encoded


def test_external_artifact_paths_are_blocked_as_reference_boundaries(tmp_path: Path) -> None:
    manifest = _manifest_payload()
    manifest["entries"][0] = deepcopy(manifest["entries"][0])
    manifest["entries"][0]["paths"]["external_log"] = "external/manasight/session.log.gz"
    manifest_path = _write_json(tmp_path, "external-manifest.json", manifest)

    report = corpus.build_corpus_parity_report(manifest_path)

    assert report["status"] == "blocked_external_boundary"
    assert "external_artifact_path:bo1_match_win_basic:external_log" in report["status_reasons"]
    assert "forbidden_artifact_path:bo1_match_win_basic:external_log" in report["status_reasons"]


def test_session_ledger_rejects_non_redacted_report_only_flags(tmp_path: Path) -> None:
    ledger = _session_ledger_payload()
    ledger["sessions"][0]["report_only_redactions"]["private_paths_included"] = True
    ledger_path = _write_json(tmp_path, "session-ledger.json", ledger)

    errors = corpus.validate_session_ledger(corpus.load_session_ledger(ledger_path))

    assert errors == [
        "session_redaction_flag_not_false:standard_bo1_match_win_basic_v1:private_paths_included"
    ]


def test_cli_writes_report_only_when_output_is_explicit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output_path = tmp_path / "corpus-parity-report.json"

    exit_code = corpus.main(
        [str(MANIFEST_PATH), "--session-ledger", str(SESSION_LEDGER_PATH), "--out", str(output_path)]
    )

    captured = capsys.readouterr()
    written_report = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Corpus parity report: partial_coverage_map_ready" in captured.out
    assert "Report written: <outside_repo>" in captured.out
    assert written_report["status"] == "partial_coverage_map_ready"
    assert written_report["inputs"]["explicit_inputs_required"] is True


def test_cli_requires_manifest_path() -> None:
    with pytest.raises(SystemExit) as exc_info:
        corpus.main([])

    assert exc_info.value.code == 2
