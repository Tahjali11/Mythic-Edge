"""Schema and vocabulary constants for the parser-owned fact tracker."""

from __future__ import annotations

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/481"
PIPELINE_TRACKER = "https://github.com/Tahjali11/Mythic-Edge/issues/388"
PARENT_PRIVATE_EVIDENCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/434"
CONTRACT_PATH = "docs/contracts/parser_owned_fact_capture_tracker.md"

FACT_TARGET_MATRIX_OBJECT = "mythic_edge_parser_owned_fact_target_matrix"
FACT_TARGET_MATRIX_SCHEMA_VERSION = "parser_owned_fact_target_matrix.v1"
SESSION_CAPTURE_LEDGER_OBJECT = "mythic_edge_parser_owned_fact_session_capture_ledger"
SESSION_CAPTURE_LEDGER_SCHEMA_VERSION = "parser_owned_fact_session_capture_ledger.v1"
COVERAGE_PROGRESS_REPORT_OBJECT = "mythic_edge_parser_owned_fact_coverage_progress_report"
COVERAGE_PROGRESS_REPORT_SCHEMA_VERSION = "parser_owned_fact_coverage_progress_report.v1"

DEFAULT_CREATED_AT_UTC = "1970-01-01T00:00:00Z"
DEFAULT_MATRIX_ID = "competitive-current.seed.v1"
DEFAULT_LEDGER_ID = "competitive-current.session-ledger.v1"
DEFAULT_REPORT_ID = "competitive-current.coverage-progress.v1"
DEFAULT_SCOPE = "competitive_current"

TARGET_MATRIX_STATUSES = (
    "seed_matrix_ready",
    "expanded_matrix_ready",
    "review_required",
    "invalid",
)
COMPETITIVE_SCOPES = (
    "competitive_current",
    "deferred_feature_expansion",
    "support_only",
    "out_of_scope_now",
    "historical_reference",
    "review_required",
)
DEFERRED_REASONS = (
    "bo1_current_phase_deferred",
    "alchemy_conjure_spellbook_current_phase_deferred",
    "store_pack_inbox_crafting_non_competitive_deferred",
    "hidden_card_truth_forbidden",
    "opponent_intent_forbidden",
    "gameplay_advice_forbidden",
    "analytics_only_support",
    "requires_future_contract",
    "requires_private_evidence_approval",
    "requires_external_boundary_resolution",
    "not_applicable",
)
PRIORITIES = ("critical", "high", "medium", "low", "deferred")
FACT_FAMILIES = (
    "match",
    "game",
    "queue",
    "rank",
    "participant",
    "gameplay_action",
    "runtime_health",
    "deck_state",
    "analytics",
)
LIFECYCLE_STATUSES = (
    "out_of_scope_now",
    "deferred_feature_expansion",
    "not_captured",
    "captured_private",
    "candidate_generated",
    "review_packet_created",
    "human_approved",
    "promotion_proof_ready",
    "fixture_manifest_draft_ready",
    "promoted_golden_fixture",
    "confirmed_windows",
    "confirmed_macos",
    "confirmed_cross_platform",
    "rejected_or_noisy",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "review_required",
    "invalid",
)
PLATFORM_KEYS = ("windows", "macos", "cross_platform")
PLATFORM_STATUSES = (
    "not_required",
    "not_captured",
    "captured_private",
    "candidate_generated",
    "review_packet_created",
    "human_approved",
    "promoted_fixture_confirmed",
    "confirmed",
    "rejected_or_noisy",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "unknown",
)
SOURCE_KINDS = (
    "synthetic_fixture",
    "synthetic_player_log",
    "synthetic_utc_log",
    "user_selected_player_log",
    "user_selected_normalized_utc_log",
    "local_harvest_candidate_summary",
    "harvest_review_packet",
    "fixture_promotion_proof",
    "golden_replay_fixture_manifest_draft",
    "corpus_metadata_diff",
    "human_approved_update_record",
)
SYNTHETIC_SOURCE_KINDS = (
    "synthetic_fixture",
    "synthetic_player_log",
    "synthetic_utc_log",
)
PRIVATE_SOURCE_KINDS = (
    "user_selected_player_log",
    "user_selected_normalized_utc_log",
)
FORMAT_FAMILIES = ("standard", "limited", "historic", "alchemy", "unknown")
QUEUE_FAMILIES = ("traditional_bo3", "bo1", "draft", "sealed", "unknown")
MATCH_TYPES = ("traditional_bo3", "bo1", "draft_with_games", "unknown")

FALSE_FLAG_FIELDS = (
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
    "implementation_authorized",
    "file_writing_authorized",
    "issue_creation_authorized",
    "pr_creation_authorized",
)
READINESS_FLAG_FIELDS = (
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
)
AUTHORIZATION_FLAG_FIELDS = (
    "implementation_authorized",
    "file_writing_authorized",
    "issue_creation_authorized",
    "pr_creation_authorized",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
)
REQUIRED_NON_CLAIMS = (
    "not_parser_truth",
    "not_raw_log_reader",
    "not_private_harvest_authorization",
    "not_fixture_promotion",
    "not_corpus_status_change",
    "not_parser_behavior_readiness",
    "not_pipeline_activation_readiness",
    "not_release_readiness",
    "not_deploy_readiness",
    "not_production_behavior",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
    "not_hidden_card_truth",
    "not_gameplay_advice",
    "not_player_mistake_label",
    "not_automatic_truth_approval",
)

MATRIX_REQUIRED_FIELDS = (
    "object",
    "schema_version",
    "matrix_id",
    "scope",
    "target_matrix_status",
    "created_at_utc",
    "source_issue",
    "pipeline_tracker",
    "parent_private_evidence_issue",
    "source_matrix_refs",
    "readiness_flags",
    "authorization_flags",
    "facts",
    "summary",
    "non_claims",
)
FACT_REQUIRED_FIELDS = (
    "fact_id",
    "display_name",
    "fact_family",
    "competitive_scope",
    "deferred_reason",
    "priority",
    "parser_owner",
    "source_field_recovery_matrix_row_ids",
    "evidence_ledger_entry_ids",
    "required_capture_evidence",
    "allowed_capture_sources",
    "forbidden_capture_sources",
    "expected_outputs",
    "platform_requirements",
    "current_lifecycle_status",
    "platform_status",
    "candidate_ids",
    "review_packet_ids",
    "promotion_proof_ids",
    "fixture_draft_ids",
    "promoted_fixture_ids",
    "corpus_entry_ids",
    "known_gaps",
    "next_capture_target",
    "non_claims",
)
LEDGER_REQUIRED_FIELDS = (
    "object",
    "schema_version",
    "ledger_id",
    "scope",
    "updated_at_utc",
    "source_issue",
    "pipeline_tracker",
    "parent_private_evidence_issue",
    "target_matrix_ref",
    "sessions",
    "summary",
    "privacy",
    "readiness_flags",
    "authorization_flags",
    "non_claims",
)
SESSION_REQUIRED_FIELDS = (
    "session_id",
    "platform",
    "source_kind",
    "scope",
    "format_family",
    "queue_family",
    "match_type",
    "capture_started_at_utc",
    "capture_finished_at_utc",
    "source_window_ref",
    "candidate_summary_refs",
    "review_packet_refs",
    "reviewer_decision_refs",
    "promotion_proof_refs",
    "fixture_draft_refs",
    "promoted_fixture_refs",
    "fact_deltas",
    "privacy_scan",
    "environment_summary",
    "remaining_targets",
    "authorization_flags",
    "non_claims",
)
REPORT_REQUIRED_FIELDS = (
    "object",
    "schema_version",
    "report_id",
    "scope",
    "generated_at_utc",
    "target_matrix_ref",
    "session_capture_ledger_ref",
    "previous_report_ref",
    "summary_counts",
    "new_private_captures",
    "new_candidates_generated",
    "reviewer_decisions",
    "promotion_progress",
    "windows_only_confirmations",
    "macos_only_confirmations",
    "cross_platform_confirmations",
    "current_competitive_scope_gaps",
    "deferred_feature_expansion_facts",
    "next_recommended_capture_targets",
    "blocked_or_review_required",
    "privacy",
    "validation",
    "readiness_flags",
    "authorization_flags",
    "non_claims",
)
