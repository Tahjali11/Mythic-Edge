from __future__ import annotations

import copy
import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from mythic_edge_parser.app import evidence_ledger

FIELD_RECOVERY_MATRIX_OBJECT = "mythic_edge_parser_field_recovery_matrix"
FIELD_RECOVERY_MATRIX_SCHEMA_VERSION = "parser_field_recovery_matrix.v1"
FIELD_RECOVERY_MATRIX_ROW_OBJECT = "mythic_edge_parser_field_recovery_matrix_row"

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/451"
PIPELINE_TRACKER = "https://github.com/Tahjali11/Mythic-Edge/issues/388"
PARENT_PRIVATE_EVIDENCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/434"

MATRIX_STATUSES = ("planning_matrix_ready", "review_required", "invalid")
RECOVERY_CATEGORIES = (
    "direct",
    "equivalent",
    "derived_bounded",
    "approximate_analytics_only",
    "unavailable",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "review_required",
)
PARSER_OUTPUT_POLICIES = (
    "preserve_existing_parser_behavior",
    "restore_only_after_parser_contract_and_fixture_review",
    "emit_degraded_only_if_existing_parser_contract_allows",
    "blank_or_unknown_until_recovered",
    "never_parser_truth_analytics_only",
    "blocked_until_private_evidence_review",
    "blocked_until_external_boundary_resolved",
    "manual_review_required",
)
ANALYTICS_OUTPUT_POLICIES = (
    "may_display_parser_value_with_evidence_label",
    "may_display_degraded_context_only",
    "may_display_approximate_context_only",
    "may_display_unavailable",
    "must_not_display_as_fact",
    "not_applicable",
)
STALE_SOURCE_BEHAVIORS = (
    "preserve_prior_final_value_with_review_note",
    "lower_confidence_and_mark_degraded",
    "blank_or_unknown_for_new_outputs",
    "route_to_review_required",
    "blocked_until_fresh_evidence",
    "not_applicable",
)
FIELD_FAMILIES = (
    "match",
    "game",
    "queue",
    "rank",
    "participant",
    "gameplay_action",
    "runtime_health",
    "analytics",
    "deck_state",
)
REQUIRED_NON_CLAIMS = (
    "not_parser_truth",
    "not_source_recovery_authority",
    "not_fixture_promotion",
    "not_corpus_status_change",
    "not_private_harvest_authorization",
    "not_parser_behavior_readiness",
    "not_pipeline_activation_readiness",
    "not_merge_readiness",
    "not_deploy_readiness",
    "not_release_readiness",
    "not_production_behavior",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
)
FALSE_READINESS_FLAGS = (
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
)

REQUIRED_MATRIX_FIELDS = (
    "object",
    "schema_version",
    "source_issue",
    "pipeline_tracker",
    "parent_private_evidence_issue",
    "status",
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
    "rows",
    "matrix_summary",
    "non_claims",
)
REQUIRED_ROW_FIELDS = (
    "object",
    "field_id",
    "display_name",
    "field_family",
    "parser_owner",
    "output_surfaces",
    "evidence_ledger_entry_ids",
    "required_direct_evidence",
    "allowed_fallback_evidence",
    "forbidden_fallback_evidence",
    "recovery_category",
    "parser_output_policy",
    "analytics_output_policy",
    "minimum_confidence",
    "allowed_finality",
    "degradation_flags",
    "stale_source_behavior",
    "review_required",
    "restoration_requirements",
    "non_claims",
)
FIELD_ID_RE = re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9_]+)+$")
LOCAL_ABSOLUTE_PATH_RE = re.compile(
    r"(?:file:(?://)?/(?!/)|(^|[\s\"'`(:=\[])/(?!/)|"
    r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]|\\\\)"
)
FORBIDDEN_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"\bPlayer\.log\b|\bUTC_Log\b|https?://hooks\.|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,})",
    re.IGNORECASE,
)


def _row(
    *,
    field_id: str,
    display_name: str,
    field_family: str,
    parser_owner: str,
    output_surfaces: Sequence[str],
    evidence_ledger_entry_ids: Sequence[str],
    required_direct_evidence: Sequence[str],
    allowed_fallback_evidence: Sequence[str],
    forbidden_fallback_evidence: Sequence[str],
    recovery_category: str,
    parser_output_policy: str,
    analytics_output_policy: str,
    minimum_confidence: str,
    allowed_finality: Sequence[str],
    degradation_flags: Sequence[str],
    stale_source_behavior: str,
    review_required: bool,
    restoration_requirements: Sequence[str],
) -> dict[str, Any]:
    return {
        "object": FIELD_RECOVERY_MATRIX_ROW_OBJECT,
        "field_id": field_id,
        "display_name": display_name,
        "field_family": field_family,
        "parser_owner": parser_owner,
        "output_surfaces": list(output_surfaces),
        "evidence_ledger_entry_ids": list(evidence_ledger_entry_ids),
        "required_direct_evidence": list(required_direct_evidence),
        "allowed_fallback_evidence": list(allowed_fallback_evidence),
        "forbidden_fallback_evidence": list(forbidden_fallback_evidence),
        "recovery_category": recovery_category,
        "parser_output_policy": parser_output_policy,
        "analytics_output_policy": analytics_output_policy,
        "minimum_confidence": minimum_confidence,
        "allowed_finality": list(allowed_finality),
        "degradation_flags": list(degradation_flags),
        "stale_source_behavior": stale_source_behavior,
        "review_required": review_required,
        "restoration_requirements": list(restoration_requirements),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


_FIELD_RECOVERY_ROWS: tuple[dict[str, Any], ...] = (
    _row(
        field_id="match.match_id",
        display_name="Match ID",
        field_family="match",
        parser_owner="src/mythic_edge_parser/app/state.py",
        output_surfaces=["MatchSummary.match_id", "MatchLogRow.match_id", "GameLogRow.match_id"],
        evidence_ledger_entry_ids=["tier1.match_identity.match_id"],
        required_direct_evidence=["match_state.match_id"],
        allowed_fallback_evidence=[],
        forbidden_fallback_evidence=[
            "workbook_formula_reconstruction",
            "analytics_match_grouping",
            "stale_runtime_status",
            "model_provider_guess",
        ],
        recovery_category="direct",
        parser_output_policy="preserve_existing_parser_behavior",
        analytics_output_policy="may_display_parser_value_with_evidence_label",
        minimum_confidence="high",
        allowed_finality=["live", "final", "reconciled"],
        degradation_flags=["missing_expected_payload_path", "conflicting_evidence"],
        stale_source_behavior="preserve_prior_final_value_with_review_note",
        review_required=False,
        restoration_requirements=[
            "existing_parser_behavior_only",
            "new_parser_output_still_requires_scoped_parser_contract",
        ],
    ),
    _row(
        field_id="match.event_id",
        display_name="Event ID",
        field_family="queue",
        parser_owner="src/mythic_edge_parser/app/state.py",
        output_surfaces=["MatchSummary.event_id", "MatchLogRow.event_id", "EventIdentity"],
        evidence_ledger_entry_ids=["tier2.queue_format_rank_event_context.event_id"],
        required_direct_evidence=["match_state.event_id.game_room_config"],
        allowed_fallback_evidence=["match_state.event_id.player_fallback"],
        forbidden_fallback_evidence=[
            "event_name_label",
            "dashboard_queue_filter",
            "external_taxonomy_label",
            "ai_event_guess",
        ],
        recovery_category="equivalent",
        parser_output_policy="restore_only_after_parser_contract_and_fixture_review",
        analytics_output_policy="may_display_degraded_context_only",
        minimum_confidence="medium",
        allowed_finality=["live", "provisional"],
        degradation_flags=["fallback_used", "changed_signal_type", "fixture_gap"],
        stale_source_behavior="route_to_review_required",
        review_required=True,
        restoration_requirements=[
            "scoped_codex_a_problem_representation",
            "scoped_codex_b_parser_contract",
            "synthetic_or_sanitized_fixture_evidence",
            "codex_e_review",
        ],
    ),
    _row(
        field_id="game.game1_result",
        display_name="Game 1 Result",
        field_family="game",
        parser_owner="src/mythic_edge_parser/app/state.py",
        output_surfaces=["GameSummary.result", "GameLogRow.game_result"],
        evidence_ledger_entry_ids=[
            "tier3.game_results.game1_result",
            "tier3.game_results.game1_winner_team",
            "tier1.participants.player_team",
        ],
        required_direct_evidence=["game_result.game1.result", "game_result.game1.winner_team"],
        allowed_fallback_evidence=["participant.player_team_mapping"],
        forbidden_fallback_evidence=[
            "match_scope_result_promotion",
            "scoreboard_display_guess",
            "analytics_win_rate_backfill",
            "stale_prior_game_slot",
        ],
        recovery_category="derived_bounded",
        parser_output_policy="restore_only_after_parser_contract_and_fixture_review",
        analytics_output_policy="may_display_degraded_context_only",
        minimum_confidence="medium",
        allowed_finality=["provisional", "final", "reconciled"],
        degradation_flags=["fallback_used", "missing_expected_payload_path", "conflicting_evidence"],
        stale_source_behavior="lower_confidence_and_mark_degraded",
        review_required=True,
        restoration_requirements=[
            "game_scope_evidence_only",
            "participant_mapping_dependency_review",
            "golden_replay_fixture_review",
        ],
    ),
    _row(
        field_id="analytics.card_performance",
        display_name="Card Performance",
        field_family="analytics",
        parser_owner="src/mythic_edge_parser/app/card_performance.py",
        output_surfaces=["local_review_reports"],
        evidence_ledger_entry_ids=["tier7.derived_analytics_outputs.card_performance"],
        required_direct_evidence=[],
        allowed_fallback_evidence=["parser_owned_game_and_card_identity_summaries"],
        forbidden_fallback_evidence=[
            "card_name_truth",
            "deck_identity_truth",
            "opponent_hidden_card_inference",
            "model_provider_card_rating",
        ],
        recovery_category="approximate_analytics_only",
        parser_output_policy="never_parser_truth_analytics_only",
        analytics_output_policy="may_display_approximate_context_only",
        minimum_confidence="low",
        allowed_finality=["provisional"],
        degradation_flags=["weak_fallback_used", "fixture_gap"],
        stale_source_behavior="blank_or_unknown_for_new_outputs",
        review_required=True,
        restoration_requirements=[
            "must_remain_downstream_consumer",
            "must_not_populate_parser_owned_fields",
        ],
    ),
    _row(
        field_id="deck_state.game1_deck_state",
        display_name="Game 1 Deck State",
        field_family="deck_state",
        parser_owner="src/mythic_edge_parser/app/state.py",
        output_surfaces=["local_review_reports"],
        evidence_ledger_entry_ids=[],
        required_direct_evidence=[],
        allowed_fallback_evidence=[],
        forbidden_fallback_evidence=[
            "submitted_deck_payload_as_complete_game_state",
            "collection_match",
            "deck_name_or_deck_id",
            "archetype_label",
        ],
        recovery_category="unavailable",
        parser_output_policy="blank_or_unknown_until_recovered",
        analytics_output_policy="may_display_unavailable",
        minimum_confidence="unknown",
        allowed_finality=["provisional"],
        degradation_flags=["fixture_gap", "missing_expected_event_family"],
        stale_source_behavior="blank_or_unknown_for_new_outputs",
        review_required=True,
        restoration_requirements=[
            "future_scoped_deck_state_contract",
            "parser_owned_source_evidence",
            "fixture_review_before_any_parser_output",
        ],
    ),
    _row(
        field_id="runtime_health.private_log_drift_window",
        display_name="Private Log Drift Window",
        field_family="runtime_health",
        parser_owner="docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md",
        output_surfaces=["local_review_reports"],
        evidence_ledger_entry_ids=[
            "tier6.runtime_health_and_drift_detection.diagnostics_status"
        ],
        required_direct_evidence=[],
        allowed_fallback_evidence=["approved_private_evidence_summary_only"],
        forbidden_fallback_evidence=[
            "unapproved_private_note",
            "local_absolute_path",
            "raw_private_log_excerpt",
            "exact_offset_or_file_size",
        ],
        recovery_category="blocked_private_evidence",
        parser_output_policy="blocked_until_private_evidence_review",
        analytics_output_policy="must_not_display_as_fact",
        minimum_confidence="unknown",
        allowed_finality=["provisional"],
        degradation_flags=["sensitive_evidence_redacted", "fixture_gap"],
        stale_source_behavior="blocked_until_fresh_evidence",
        review_required=True,
        restoration_requirements=[
            "issue_434_approved_private_evidence_scope",
            "public_safe_redaction_review",
            "separate_parser_contract_before_restoration",
        ],
    ),
    _row(
        field_id="runtime_health.firewall_network_drop",
        display_name="Firewall Or Network Drop",
        field_family="runtime_health",
        parser_owner="docs/contracts/parser_corpus_firewall_network_drop_coverage.md",
        output_surfaces=["local_review_reports"],
        evidence_ledger_entry_ids=[],
        required_direct_evidence=[],
        allowed_fallback_evidence=["approved_external_boundary_summary_only"],
        forbidden_fallback_evidence=[
            "os_router_log",
            "packet_capture",
            "network_provider_status",
            "client_disconnected_label_as_cause",
        ],
        recovery_category="blocked_external_boundary",
        parser_output_policy="blocked_until_external_boundary_resolved",
        analytics_output_policy="must_not_display_as_fact",
        minimum_confidence="unknown",
        allowed_finality=["provisional"],
        degradation_flags=["fixture_gap", "new_unknown_event_family"],
        stale_source_behavior="blocked_until_fresh_evidence",
        review_required=True,
        restoration_requirements=[
            "future_external_boundary_contract",
            "public_safe_evidence_review",
            "separate_parser_contract_before_restoration",
        ],
    ),
    _row(
        field_id="gameplay_action.actor_relation",
        display_name="Gameplay Action Actor Relation",
        field_family="gameplay_action",
        parser_owner="src/mythic_edge_parser/app/gameplay_actions.py",
        output_surfaces=["local_review_reports"],
        evidence_ledger_entry_ids=["tier5.gameplay_action.gameplay_action"],
        required_direct_evidence=["gameplay_action.actor_relation"],
        allowed_fallback_evidence=["participant.player_team_mapping"],
        forbidden_fallback_evidence=[
            "opponent_intent_guess",
            "hidden_action_absence",
            "analytics_player_mistake_label",
            "coaching_best_line_label",
        ],
        recovery_category="review_required",
        parser_output_policy="manual_review_required",
        analytics_output_policy="may_display_degraded_context_only",
        minimum_confidence="low",
        allowed_finality=["live", "provisional"],
        degradation_flags=["conflicting_evidence", "fallback_used"],
        stale_source_behavior="route_to_review_required",
        review_required=True,
        restoration_requirements=[
            "resolve_actor_relation_conflict",
            "scoped_parser_contract_if_behavior_changes",
            "focused_parser_tests",
        ],
    ),
)


def build_field_recovery_matrix() -> dict[str, Any]:
    rows = list(iter_field_recovery_rows())
    return {
        "object": FIELD_RECOVERY_MATRIX_OBJECT,
        "schema_version": FIELD_RECOVERY_MATRIX_SCHEMA_VERSION,
        "source_issue": SOURCE_ISSUE,
        "pipeline_tracker": PIPELINE_TRACKER,
        "parent_private_evidence_issue": PARENT_PRIVATE_EVIDENCE_ISSUE,
        "status": "planning_matrix_ready",
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
        "private_harvest_authorized": False,
        "fixture_promotion_authorized": False,
        "corpus_status_change_authorized": False,
        "rows": rows,
        "matrix_summary": _build_matrix_summary(rows),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def iter_field_recovery_rows() -> Iterable[dict[str, Any]]:
    return tuple(copy.deepcopy(row) for row in _FIELD_RECOVERY_ROWS)


def validate_field_recovery_matrix(matrix: Mapping[str, Any] | None = None) -> list[str]:
    payload = build_field_recovery_matrix() if matrix is None else matrix
    if not isinstance(payload, Mapping):
        return ["matrix:not_mapping"]

    errors: list[str] = []
    errors.extend(_missing_required_fields(payload, REQUIRED_MATRIX_FIELDS, "matrix"))
    if payload.get("object") != FIELD_RECOVERY_MATRIX_OBJECT:
        errors.append("matrix:invalid_object")
    if payload.get("schema_version") != FIELD_RECOVERY_MATRIX_SCHEMA_VERSION:
        errors.append("matrix:invalid_schema_version")
    if payload.get("source_issue") != SOURCE_ISSUE:
        errors.append("matrix:invalid_source_issue")
    if payload.get("pipeline_tracker") != PIPELINE_TRACKER:
        errors.append("matrix:invalid_pipeline_tracker")
    if payload.get("parent_private_evidence_issue") != PARENT_PRIVATE_EVIDENCE_ISSUE:
        errors.append("matrix:invalid_parent_private_evidence_issue")
    if payload.get("status") not in MATRIX_STATUSES:
        errors.append("matrix:invalid_status")
    for flag in FALSE_READINESS_FLAGS:
        if payload.get(flag) is not False:
            errors.append(f"matrix:{flag}_must_remain_false")
    errors.extend(_validate_non_claims(payload.get("non_claims"), "matrix:non_claims"))

    rows = payload.get("rows")
    if not isinstance(rows, list):
        errors.append("matrix:rows_not_list")
    else:
        errors.extend(_duplicate_value_errors(rows, key="field_id", label="field_id"))
        for index, row in enumerate(rows):
            row_errors = validate_field_recovery_row(row if isinstance(row, Mapping) else {})
            errors.extend(f"matrix:rows[{index}]:{error}" for error in row_errors)
        errors.extend(_validate_matrix_summary(payload.get("matrix_summary"), rows))

    errors.extend(_privacy_errors(payload, "matrix"))
    return _dedupe_errors(errors)


def validate_field_recovery_row(row: Mapping[str, Any]) -> list[str]:
    if not isinstance(row, Mapping):
        return ["row:not_mapping"]

    errors: list[str] = []
    errors.extend(_missing_required_fields(row, REQUIRED_ROW_FIELDS, "row"))
    field_id = str(row.get("field_id") or "")
    if not FIELD_ID_RE.fullmatch(field_id):
        errors.append("row:invalid_field_id")
    if row.get("object") != FIELD_RECOVERY_MATRIX_ROW_OBJECT:
        errors.append("row:invalid_object")
    _validate_scalar(row.get("field_family"), FIELD_FAMILIES, "row:field_family", errors)
    _validate_scalar(
        row.get("recovery_category"),
        RECOVERY_CATEGORIES,
        "row:recovery_category",
        errors,
    )
    _validate_scalar(
        row.get("parser_output_policy"),
        PARSER_OUTPUT_POLICIES,
        "row:parser_output_policy",
        errors,
    )
    _validate_scalar(
        row.get("analytics_output_policy"),
        ANALYTICS_OUTPUT_POLICIES,
        "row:analytics_output_policy",
        errors,
    )
    _validate_scalar(
        row.get("minimum_confidence"),
        evidence_ledger.CONFIDENCE_LEVELS,
        "row:minimum_confidence",
        errors,
    )
    _validate_scalar(
        row.get("stale_source_behavior"),
        STALE_SOURCE_BEHAVIORS,
        "row:stale_source_behavior",
        errors,
    )
    for key in (
        "output_surfaces",
        "evidence_ledger_entry_ids",
        "required_direct_evidence",
        "allowed_fallback_evidence",
        "forbidden_fallback_evidence",
        "allowed_finality",
        "degradation_flags",
        "restoration_requirements",
    ):
        _validate_string_list(row.get(key), f"row:{key}", errors)
    _validate_string_list(row.get("allowed_finality"), "row:allowed_finality", errors)
    _validate_string_list(row.get("degradation_flags"), "row:degradation_flags", errors)
    for finality in _as_string_list(row.get("allowed_finality")):
        if finality not in evidence_ledger.FINALITY_LABELS:
            errors.append(f"row:allowed_finality:unknown:{finality}")
    for flag in _as_string_list(row.get("degradation_flags")):
        if flag not in evidence_ledger.DRIFT_FLAGS:
            errors.append(f"row:degradation_flags:unknown:{flag}")
    if not isinstance(row.get("review_required"), bool):
        errors.append("row:review_required_not_bool")
    errors.extend(_validate_non_claims(row.get("non_claims"), "row:non_claims"))
    errors.extend(_validate_ledger_references(row))
    errors.extend(_validate_output_boundaries(row))
    errors.extend(_privacy_errors(row, "row"))
    return _dedupe_errors(errors)


def _build_matrix_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "recovery_category_counts": _count_values(rows, "recovery_category", RECOVERY_CATEGORIES),
        "parser_output_policy_counts": _count_values(rows, "parser_output_policy", PARSER_OUTPUT_POLICIES),
        "review_required_count": sum(1 for row in rows if row.get("review_required") is True),
        "summary_is_readiness_metric": False,
    }


def _validate_matrix_summary(value: Any, rows: Sequence[Mapping[str, Any]]) -> list[str]:
    if not isinstance(value, Mapping):
        return ["matrix:matrix_summary_not_mapping"]
    expected = _build_matrix_summary(rows)
    errors: list[str] = []
    if value.get("row_count") != expected["row_count"]:
        errors.append("matrix:matrix_summary:row_count_mismatch")
    if value.get("recovery_category_counts") != expected["recovery_category_counts"]:
        errors.append("matrix:matrix_summary:recovery_category_counts_mismatch")
    if value.get("parser_output_policy_counts") != expected["parser_output_policy_counts"]:
        errors.append("matrix:matrix_summary:parser_output_policy_counts_mismatch")
    if value.get("review_required_count") != expected["review_required_count"]:
        errors.append("matrix:matrix_summary:review_required_count_mismatch")
    if value.get("summary_is_readiness_metric") is not False:
        errors.append("matrix:matrix_summary:summary_is_readiness_metric_must_be_false")
    return errors


def _validate_ledger_references(row: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    known_entry_ids = {entry["entry_id"] for entry in evidence_ledger.iter_ledger_entries()}
    for entry_id in _as_string_list(row.get("evidence_ledger_entry_ids")):
        if entry_id not in known_entry_ids:
            errors.append(f"row:evidence_ledger_entry_ids:unknown:{entry_id}")
            if row.get("review_required") is not True:
                errors.append("row:evidence_ledger_entry_ids:unknown_requires_review_required")
    return errors


def _validate_output_boundaries(row: Mapping[str, Any]) -> list[str]:
    category = row.get("recovery_category")
    parser_policy = row.get("parser_output_policy")
    analytics_policy = row.get("analytics_output_policy")
    confidence = row.get("minimum_confidence")
    review_required = row.get("review_required")
    errors: list[str] = []

    if category != "direct" and parser_policy == "preserve_existing_parser_behavior":
        errors.append("row:blocked_truth_boundary_violation:non_direct_preserves_parser_behavior")
    if category == "direct" and parser_policy != "preserve_existing_parser_behavior":
        errors.append("row:direct_requires_preserve_existing_parser_behavior")
    if category == "equivalent":
        if parser_policy != "restore_only_after_parser_contract_and_fixture_review":
            errors.append("row:equivalent_requires_parser_contract_and_fixture_review")
        if confidence == "high":
            errors.append("row:equivalent_cannot_start_high_confidence")
        if review_required is not True:
            errors.append("row:equivalent_requires_review")
    if category == "derived_bounded":
        if parser_policy not in {
            "restore_only_after_parser_contract_and_fixture_review",
            "emit_degraded_only_if_existing_parser_contract_allows",
        }:
            errors.append("row:derived_bounded_requires_bounded_parser_policy")
        if confidence == "high":
            errors.append("row:derived_bounded_cannot_raise_to_high_confidence")
    if category == "approximate_analytics_only":
        if parser_policy != "never_parser_truth_analytics_only":
            errors.append("row:approximate_analytics_only_cannot_restore_parser_output")
        if analytics_policy != "may_display_approximate_context_only":
            errors.append("row:approximate_analytics_only_requires_approximate_display_policy")
        if confidence not in {"low", "unknown"}:
            errors.append("row:approximate_analytics_only_confidence_too_high")
    if category == "unavailable":
        if parser_policy != "blank_or_unknown_until_recovered":
            errors.append("row:unavailable_requires_blank_or_unknown")
        if analytics_policy != "may_display_unavailable":
            errors.append("row:unavailable_requires_unavailable_display")
        if confidence not in {"low", "unknown"}:
            errors.append("row:unavailable_confidence_too_high")
    if category == "blocked_private_evidence":
        if parser_policy != "blocked_until_private_evidence_review":
            errors.append("row:blocked_private_evidence_requires_private_review_policy")
        if confidence not in {"low", "unknown"}:
            errors.append("row:blocked_private_evidence_confidence_too_high")
    if category == "blocked_external_boundary":
        if parser_policy != "blocked_until_external_boundary_resolved":
            errors.append("row:blocked_external_boundary_requires_external_policy")
        if confidence not in {"low", "unknown"}:
            errors.append("row:blocked_external_boundary_confidence_too_high")
    if category == "review_required":
        if parser_policy != "manual_review_required":
            errors.append("row:review_required_category_requires_manual_review_policy")
        if review_required is not True:
            errors.append("row:review_required_category_requires_review_required_true")
    if category in {
        "equivalent",
        "derived_bounded",
        "approximate_analytics_only",
        "unavailable",
        "blocked_private_evidence",
        "blocked_external_boundary",
        "review_required",
    } and review_required is not True:
        errors.append("row:non_direct_or_blocked_category_requires_review")
    return errors


def _missing_required_fields(value: Mapping[str, Any], fields: Sequence[str], label: str) -> list[str]:
    return [f"{label}:missing:{field}" for field in fields if field not in value]


def _validate_scalar(
    value: Any, allowed: Sequence[str], label: str, errors: list[str]
) -> None:
    if value not in allowed:
        errors.append(f"{label}:unknown:{value}")


def _validate_string_list(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label}_not_list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{label}[{index}]_not_string")


def _validate_non_claims(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    _validate_string_list(value, label, errors)
    if isinstance(value, list) and tuple(value) != REQUIRED_NON_CLAIMS:
        errors.append(f"{label}:mismatch")
    return errors


def _privacy_errors(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            errors.extend(_privacy_errors(item, f"{label}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_privacy_errors(item, f"{label}[{index}]"))
    elif isinstance(value, str):
        if LOCAL_ABSOLUTE_PATH_RE.search(value):
            errors.append(f"privacy:absolute_path:{label}")
        if FORBIDDEN_TEXT_RE.search(value):
            errors.append(f"privacy:forbidden_text:{label}")
    return errors


def _duplicate_value_errors(items: Sequence[Any], *, key: str, label: str) -> list[str]:
    seen: set[str] = set()
    errors: list[str] = []
    for item in items:
        if not isinstance(item, Mapping):
            continue
        value = item.get(key)
        if not isinstance(value, str):
            continue
        if value in seen:
            errors.append(f"duplicate_{label}:{value}")
        seen.add(value)
    return errors


def _count_values(
    rows: Sequence[Mapping[str, Any]], key: str, allowed_values: Sequence[str]
) -> dict[str, int]:
    return {
        value: sum(1 for row in rows if row.get(key) == value)
        for value in allowed_values
    }


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _dedupe_errors(errors: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(errors))
