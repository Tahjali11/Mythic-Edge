"""Synthetic-only golden replay fixture and manifest draft builder."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, Literal
from urllib.parse import unquote

from mythic_edge_parser.app.corpus_metadata_diff_generator import (
    CORPUS_MANIFEST_OBJECT,
    CORPUS_MANIFEST_SCHEMA_VERSION,
    CORPUS_METADATA_DIFF_OBJECT,
    CORPUS_METADATA_DIFF_SCHEMA_VERSION,
    SESSION_LEDGER_OBJECT,
    SESSION_LEDGER_SCHEMA_VERSION,
)
from mythic_edge_parser.app.fixture_promotion_proof import (
    FIXTURE_PROMOTION_PROOF_OBJECT,
    FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION,
)
from mythic_edge_parser.app.harvest_review_packets import (
    HARVEST_REVIEW_PACKET_OBJECT,
    HARVEST_REVIEW_PACKET_SCHEMA_VERSION,
)
from mythic_edge_parser.app.local_harvest_candidate_reports import DEFAULT_CREATED_AT_UTC

GOLDEN_REPLAY_DRAFT_PACKET_OBJECT = "mythic_edge_golden_replay_fixture_manifest_draft_packet"
GOLDEN_REPLAY_DRAFT_PACKET_SCHEMA_VERSION = "parser_evidence_golden_replay_fixture_manifest_drafts.v1"
GOLDEN_REPLAY_FIXTURE_DRAFT_OBJECT = "mythic_edge_golden_replay_fixture_draft"
GOLDEN_REPLAY_FIXTURE_DRAFT_SCHEMA_VERSION = "parser_evidence_golden_replay_fixture_draft.v1"
GOLDEN_REPLAY_MANIFEST_DRAFT_OBJECT = "mythic_edge_golden_replay_manifest_draft"
GOLDEN_REPLAY_MANIFEST_DRAFT_SCHEMA_VERSION = "parser_evidence_golden_replay_manifest_draft.v1"

CONTRACT_PATH = "docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md"
LINKED_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/385"
TRACKER = "https://github.com/Tahjali11/Mythic-Edge/issues/388"
PARENT_PRIVATE_EVIDENCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/434"
GOLDEN_REPLAY_MANIFEST_OBJECT = "mythic_edge_golden_replay_manifest"
GOLDEN_REPLAY_MANIFEST_SCHEMA_VERSION = "parser_golden_replay_manifest.v1"
DEFAULT_MAX_FIXTURE_LINE_COUNT = 200

DraftStatus = Literal[
    "draft",
    "draft_ready_for_review",
    "blocked_privacy",
    "blocked_authorization",
    "insufficient_review",
    "insufficient_proof",
    "insufficient_metadata_diff",
    "insufficient_parser_preview",
    "refused_oversized_window",
    "refused_ambiguous_window",
    "refused_multi_family_window",
    "blocked_overclaim",
    "draft_rejected",
    "needs_contract_update",
]
SourceKind = Literal[
    "synthetic_player_log_slice_draft",
    "sanitized_player_log_slice_draft",
    "metadata_only_fixture_draft",
]
SourcePrivacyClass = Literal[
    "synthetic_committable_candidate",
    "sanitized_committable_candidate",
    "committed_count_only",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "requires_review",
]
SanitizationStatus = Literal[
    "synthetic",
    "sanitized_draft",
    "not_applicable_count_only",
    "requires_review",
    "blocked_privacy",
]

DRAFT_STATUSES = frozenset(DraftStatus.__args__)
SOURCE_KINDS = frozenset(SourceKind.__args__)
SOURCE_PRIVACY_CLASSES = frozenset(SourcePrivacyClass.__args__)
SANITIZATION_STATUSES = frozenset(SanitizationStatus.__args__)
ACCEPTED_METADATA_DIFF_STATUSES = frozenset({"diff_ready_for_review", "no_metadata_change"})
ALLOWED_EXPECTED_SECTIONS = frozenset(
    {
        "router_stats",
        "event_family_counts",
        "event_kind_sequence",
        "diagnostics_summary",
        "truncation_and_data_loss",
        "unknowns_and_degradation",
        "parser_state",
        "final_reconciliation",
        "parser_owned_rows",
    },
)
FORBIDDEN_EXPECTED_SECTIONS = (
    "workbook_formulas",
    "workbook_schema_truth",
    "dashboard_logic",
    "apps_script_behavior",
    "webhook_delivery_truth",
    "google_sheets_sync_truth",
    "analytics_aggregates",
    "ai_model_provider_output",
    "coaching_advice",
    "gameplay_advice",
    "player_mistake_labels",
    "hidden_card_inference",
    "archetype_classification",
    "complete_decklists",
    "sealed_pools",
    "draft_pools",
    "private_decklists",
    "deck_names",
    "sideboard_strategy_notes",
    "release_readiness",
    "deploy_readiness",
    "production_readiness",
    "merge_readiness",
    "tracker_completion",
)

_SYMBOLIC_TEXT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_FIELD_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_REPO_RELATIVE_PATH_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
_SENSITIVE_KEY_RE = re.compile(
    r"(^|_)(raw_text|raw_content|raw_line|raw_lines|raw_payload|raw_payloads|raw_hash|raw_hashes|"
    r"private_path|private_paths|local_path|local_paths|exact_offsets|exact_file_sizes|byte_range|"
    r"file_size|timestamp_window|secret|token|api_key|credential)($|_)",
    re.IGNORECASE,
)
_SEMANTIC_PRIVACY_KEY_RE = re.compile(
    r"(^|_)("
    r"account_id|account_ids|display_name|display_names|opponent_id|opponent_ids|"
    r"opponent_identifier|opponent_identifiers|opponent_display_name|opponent_display_names|"
    r"machine_name|machine_names|hostname|hostnames|host_name|host_names|"
    r"local_user|local_users|local_user_name|local_user_names|local_username|local_usernames|"
    r"source_path|source_paths|source_filename|source_filenames|source_file_name|source_file_names|"
    r"deck_id|deck_ids|deck_name|deck_names|decklist|decklists|"
    r"strategy_note|strategy_notes|private_strategy_note|private_strategy_notes|"
    r"sideboard_note|sideboard_notes|sideboarding_note|sideboarding_notes|"
    r"sideboard_strategy_note|sideboard_strategy_notes|"
    r"card_choice|card_choices|"
    r"source_event_timestamp|private_session_timestamp|play_session_timestamp"
    r")($|_)",
    re.IGNORECASE,
)
_GENERIC_NOTE_PRIVACY_KEY_RE = re.compile(
    r"(^|_)(note|notes|comment|comments|annotation|annotations|review_note|review_notes)($|_)",
    re.IGNORECASE,
)
_GENERIC_NOTE_PRIVACY_TEXT_RE = re.compile(
    r"\b("
    r"private\s+note|private\s+notes|strategy\s+note|strategy\s+notes|"
    r"sideboard\s+note|sideboard\s+notes|sideboarding\s+note|sideboarding\s+notes|"
    r"sideboard\s+plan|sideboarding\s+plan|boarding\s+plan|sideboard\s+strategy|"
    r"card[_\s-]+choices?(?:[_\s-]+notes?|\s*:)"
    r")(?=$|[^\w])",
    re.IGNORECASE,
)
_SAFE_FALSE_FLAG_KEYS = frozenset(
    {
        "raw_source_committed",
        "raw_path_included",
        "raw_hash_included",
        "raw_content_included",
        "raw_log_lines_included",
        "raw_payloads_included",
        "raw_private_log_committed",
        "raw_private_logs_included",
        "raw_payload_values_included",
        "private_paths_included",
        "raw_hashes_included",
        "exact_offsets_included",
        "exact_file_sizes_included",
        "local_private_artifacts_committed",
        "local_private_artifacts_included",
        "external_logs_committed",
        "generated_artifacts_written",
        "generated_private_artifacts_included",
        "secrets_or_credentials_included",
    },
)
_SAFE_REFERENCE_KEYS = frozenset(
    {
        "authorized_by_contract",
        "contract",
        "contracts",
        "proposed_fixture_path",
        "proposed_manifest_path",
        "source_artifacts",
        "source_refs",
        "validation_refs",
    },
)
_PATH_REFERENCE_KEYS = frozenset({"proposed_fixture_path", "proposed_manifest_path"})
_SEQUENCE_REFERENCE_KEYS = frozenset({"source_refs", "validation_refs"})
_FORBIDDEN_REPO_PATH_SEGMENTS = frozenset(
    {
        "app-data",
        "app_data",
        "failed_posts",
        "generated",
        "generated_data",
        "private",
        "runtime",
        "sqlite",
        "workbook_exports",
    },
)
_FORBIDDEN_REPO_PATH_FILENAMES = frozenset({"player.log", "utc_log", "utc_log.txt"})
_FORBIDDEN_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"https?://script\.google\.com|https?://hooks\.|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,}|"
    r"(?:^|[^\w:/])(?:/(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b|\b[A-Za-z]:[\\/]|\\\\))",
    re.IGNORECASE,
)
_FORBIDDEN_LABELED_PATH_RE = re.compile(
    r"\b(?!(?:https?|git|ssh):)[A-Za-z_][A-Za-z0-9_-]{0,40}:"
    r"(?:/{1,3}(?:[A-Za-z]:[\\/])?(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b|"
    r"[A-Za-z]:[\\/]|\\\\)",
    re.IGNORECASE,
)
_FORBIDDEN_URI_LOCAL_PATH_RE = re.compile(
    r"\b(?!(?:https?|git|ssh):)[A-Za-z][A-Za-z0-9+.-]*:/{2,}"
    r"(?:(?:localhost|file|\.|127\.0\.0\.1)/)?"
    r"(?:[A-Za-z]:[\\/])?(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b",
    re.IGNORECASE,
)
_OVERCLAIM_KEYS = frozenset(
    {
        "parser_behavior_ready",
        "pipeline_activation_ready_for_issue_388",
        "file_writing_authorized",
        "private_harvest_authorized",
        "fixture_promotion_authorized",
        "corpus_status_change_authorized",
        "parser_behavior_verified",
        "metadata_mutation_authorized",
    },
)


def build_golden_replay_fixture_manifest_draft_packet(
    *,
    harvest_review_packet: Mapping[str, Any] | None,
    promotion_proof: Mapping[str, Any] | None,
    metadata_diff: Mapping[str, Any] | None,
    corpus_manifest: Mapping[str, Any],
    session_ledger: Mapping[str, Any],
    parser_expected_fact_preview: Mapping[str, Any] | None = None,
    draft_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic, review-only fixture/manifest draft packet."""

    context, context_findings = _draft_context(draft_context)
    packet_source, review_issue = _review_source(harvest_review_packet)
    proof_source, proof_issue = _proof_source(promotion_proof)
    diff_source, diff_issue = _metadata_diff_source(metadata_diff)
    corpus_issue = _corpus_manifest_issue(corpus_manifest)
    session_issue = _session_ledger_issue(session_ledger)
    preview_payload, preview_issue, preview_findings = _parser_expected_preview(parser_expected_fact_preview)
    all_inputs = (
        harvest_review_packet,
        promotion_proof,
        metadata_diff,
        corpus_manifest,
        session_ledger,
        parser_expected_fact_preview,
        draft_context,
    )
    upstream_privacy_findings: list[str] = []
    for index, value in enumerate(all_inputs):
        upstream_privacy_findings.extend(_privacy_findings(value, f"input_{index}"))
    privacy_findings = _dedupe([*context_findings, *preview_findings, *upstream_privacy_findings])
    overclaim_reasons = _dedupe(
        [
            *_overclaim_reasons(all_inputs),
            *_expected_section_overclaims(preview_payload),
        ],
    )
    source_kind = _member_or_default(
        context.get("source_kind"),
        SOURCE_KINDS,
        "synthetic_player_log_slice_draft",
    )
    source_privacy_class = _member_or_default(
        context.get("source_privacy_class"),
        SOURCE_PRIVACY_CLASSES,
        "synthetic_committable_candidate",
    )
    sanitization_status = _member_or_default(
        context.get("sanitization_status"),
        SANITIZATION_STATUSES,
        "synthetic",
    )
    family_candidates = _scenario_families(
        preview_payload=preview_payload,
        metadata_diff=metadata_diff,
        promotion_proof=promotion_proof,
        context=context,
    )
    parser_event_families = _parser_event_families(preview_payload, context)
    known_gaps = _known_gaps(metadata_diff, promotion_proof, context)
    window_summary, window_issue = _fixture_window_summary(context)
    authorization_reasons = _authorization_reasons(
        source_privacy_class=source_privacy_class,
        sanitization_status=sanitization_status,
        promotion_proof=promotion_proof,
        metadata_diff=metadata_diff,
    )
    status_reasons = _status_reasons(
        privacy_findings=privacy_findings,
        authorization_reasons=authorization_reasons,
        overclaim_reasons=overclaim_reasons,
        schema_issues=[corpus_issue, session_issue],
        review_issue=review_issue,
        proof_issue=proof_issue,
        diff_issue=diff_issue,
        preview_issue=preview_issue,
        window_issue=window_issue,
        family_candidates=family_candidates,
    )
    draft_status = _draft_status(
        privacy_findings=privacy_findings,
        authorization_reasons=authorization_reasons,
        overclaim_reasons=overclaim_reasons,
        schema_issues=[corpus_issue, session_issue],
        review_issue=review_issue,
        proof_issue=proof_issue,
        diff_issue=diff_issue,
        preview_issue=preview_issue,
        window_issue=window_issue,
        family_candidates=family_candidates,
    )
    source_artifacts = {
        "harvest_review_packet_id": packet_source["harvest_review_packet_id"],
        "promotion_proof_id": proof_source["promotion_proof_id"],
        "metadata_diff_id": diff_source["metadata_diff_id"],
    }
    packet_id = _draft_packet_id(context, source_artifacts)
    fixture_draft_id = _symbolic_or_default(
        context.get("fixture_draft_id"),
        f"{packet_id}:fixture-draft",
    )
    manifest_draft_id = _symbolic_or_default(
        context.get("manifest_draft_id"),
        f"{packet_id}:manifest-draft",
    )
    proposed_fixture_path = _proposed_path(
        context.get("proposed_fixture_path"),
        default=f"docs/drafts/parser_evidence/{fixture_draft_id}.log",
    )
    proposed_manifest_path = _proposed_path(
        context.get("proposed_manifest_path"),
        default=f"docs/drafts/parser_evidence/{manifest_draft_id}.json",
    )
    expected_sections = preview_payload["expected_sections"] if draft_status != "blocked_privacy" else {}
    parser_owned_sections = sorted(expected_sections)
    review_gates = _review_gates()
    authorization_flags = _authorization_flags()
    readiness_flags = _readiness_flags()
    privacy = _privacy_summary(privacy_findings)
    validation = {
        "review_packet_valid": review_issue is None,
        "promotion_proof_valid": proof_issue is None,
        "metadata_diff_valid": diff_issue is None,
        "corpus_manifest_valid": corpus_issue is None,
        "session_ledger_valid": session_issue is None,
        "parser_preview_valid": preview_issue is None,
        "status_reasons": status_reasons,
        "privacy_finding_count": len(privacy_findings),
        "privacy_findings": _privacy_finding_records(privacy_findings),
        "overclaim_reasons": overclaim_reasons,
    }

    fixture_draft = {
        "object": GOLDEN_REPLAY_FIXTURE_DRAFT_OBJECT,
        "schema_version": GOLDEN_REPLAY_FIXTURE_DRAFT_SCHEMA_VERSION,
        "fixture_draft_id": fixture_draft_id,
        "draft_status": draft_status,
        "scenario_families": [] if draft_status == "blocked_privacy" else family_candidates,
        "parser_event_families": [] if draft_status == "blocked_privacy" else parser_event_families,
        "source_kind": source_kind,
        "source_privacy_class": source_privacy_class,
        "sanitization_status": sanitization_status,
        "raw_private_log_committed": False,
        "file_writing_authorized": False,
        "proposed_fixture_path": proposed_fixture_path,
        "fixture_window_summary": window_summary,
        "minimization": _minimization(family_candidates, parser_event_families, window_issue),
        "redaction_summary": _redaction_summary(source_privacy_class, sanitization_status),
        "parser_fact_preview_refs": preview_payload["source_refs"] if draft_status != "blocked_privacy" else [],
        "source_artifacts": source_artifacts,
        "review_gates": review_gates,
        "known_gaps": [] if draft_status == "blocked_privacy" else known_gaps,
        "non_claims": _non_claims(),
    }
    manifest_draft = {
        "object": GOLDEN_REPLAY_MANIFEST_DRAFT_OBJECT,
        "schema_version": GOLDEN_REPLAY_MANIFEST_DRAFT_SCHEMA_VERSION,
        "manifest_draft_id": manifest_draft_id,
        "draft_status": draft_status,
        "proposed_manifest_path": proposed_manifest_path,
        "proposed_fixture_path": proposed_fixture_path,
        "manifest_object": GOLDEN_REPLAY_MANIFEST_OBJECT,
        "manifest_schema_version": GOLDEN_REPLAY_MANIFEST_SCHEMA_VERSION,
        "source": {
            "source_kind": source_kind,
            "source_privacy_class": source_privacy_class,
            "sanitization_status": sanitization_status,
            "raw_private_log_committed": False,
        },
        "coverage": {
            "scenario_families": [] if draft_status == "blocked_privacy" else family_candidates,
            "parser_event_families": [] if draft_status == "blocked_privacy" else parser_event_families,
            "known_gaps": [] if draft_status == "blocked_privacy" else known_gaps,
            "expected_degradation": preview_payload["expected_degradation"],
            "non_claims": _non_claims(),
        },
        "expected_draft": expected_sections,
        "parser_owned_expected_sections": parser_owned_sections,
        "forbidden_expected_sections": list(FORBIDDEN_EXPECTED_SECTIONS),
        "source_artifacts": source_artifacts,
        "review_gates": review_gates,
        "authorization_flags": authorization_flags,
    }
    return {
        "object": GOLDEN_REPLAY_DRAFT_PACKET_OBJECT,
        "schema_version": GOLDEN_REPLAY_DRAFT_PACKET_SCHEMA_VERSION,
        "packet_id": packet_id,
        "created_at_utc": _public_safe_string_or_default(
            context.get("created_at_utc"),
            DEFAULT_CREATED_AT_UTC,
        ),
        "draft_status": draft_status,
        "linked_issue": LINKED_ISSUE,
        "tracker": TRACKER,
        "parent_private_evidence_issue": PARENT_PRIVATE_EVIDENCE_ISSUE,
        "authorized_by_contract": CONTRACT_PATH,
        "source_artifacts": source_artifacts,
        "readiness_flags": readiness_flags,
        "authorization_flags": authorization_flags,
        "fixture_draft": fixture_draft,
        "manifest_draft": manifest_draft,
        "review_gates": review_gates,
        "privacy": privacy,
        "validation": validation,
        "draft_context": context,
        "non_claims": _non_claims(),
    }


def _review_source(review_packet: Mapping[str, Any] | None) -> tuple[dict[str, Any], str | None]:
    if review_packet is None or not isinstance(review_packet, Mapping):
        return _unsupported_review_source("review_packet_missing"), "review_packet_missing"
    if review_packet.get("object") != HARVEST_REVIEW_PACKET_OBJECT:
        return _unsupported_review_source("unsupported_review_packet_object"), "unsupported_review_packet_object"
    if review_packet.get("schema_version") != HARVEST_REVIEW_PACKET_SCHEMA_VERSION:
        return _unsupported_review_source("unsupported_review_packet_schema"), "unsupported_review_packet_schema"
    packet_status = _safe_field_name(str(review_packet.get("packet_status", "unknown")))
    if packet_status != "reviewed_followup_candidate":
        return (
            {
                "harvest_review_packet_schema_version": HARVEST_REVIEW_PACKET_SCHEMA_VERSION,
                "harvest_review_packet_id": _symbolic_or_default(
                    review_packet.get("packet_id"),
                    "harvest-review-packet",
                ),
                "packet_status": packet_status,
            },
            f"review_packet_status_{packet_status}",
        )
    return (
        {
            "harvest_review_packet_schema_version": HARVEST_REVIEW_PACKET_SCHEMA_VERSION,
            "harvest_review_packet_id": _symbolic_or_default(
                review_packet.get("packet_id"),
                "harvest-review-packet",
            ),
            "packet_status": packet_status,
        },
        None,
    )


def _unsupported_review_source(reason: str) -> dict[str, Any]:
    return {
        "harvest_review_packet_schema_version": "unsupported",
        "harvest_review_packet_id": "unavailable",
        "packet_status": "unavailable",
        "unavailable_reason": reason,
    }


def _proof_source(promotion_proof: Mapping[str, Any] | None) -> tuple[dict[str, Any], str | None]:
    if promotion_proof is None or not isinstance(promotion_proof, Mapping):
        return _unsupported_proof_source("proof_missing"), "proof_missing"
    if promotion_proof.get("object") != FIXTURE_PROMOTION_PROOF_OBJECT:
        return _unsupported_proof_source("unsupported_proof_object"), "unsupported_proof_object"
    if promotion_proof.get("schema_version") != FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION:
        return _unsupported_proof_source("unsupported_proof_schema"), "unsupported_proof_schema"
    proof_status = _safe_field_name(str(promotion_proof.get("proof_status", "unknown")))
    if proof_status != "proof_ready_for_review":
        return (
            {
                "promotion_proof_schema_version": FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION,
                "promotion_proof_id": _symbolic_or_default(
                    promotion_proof.get("proof_id"),
                    "fixture-promotion-proof",
                ),
                "proof_status": proof_status,
            },
            f"proof_status_{proof_status}",
        )
    return (
        {
            "promotion_proof_schema_version": FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION,
            "promotion_proof_id": _symbolic_or_default(
                promotion_proof.get("proof_id"),
                "fixture-promotion-proof",
            ),
            "proof_status": proof_status,
        },
        None,
    )


def _unsupported_proof_source(reason: str) -> dict[str, Any]:
    return {
        "promotion_proof_schema_version": "unsupported",
        "promotion_proof_id": "unavailable",
        "proof_status": "unavailable",
        "unavailable_reason": reason,
    }


def _metadata_diff_source(metadata_diff: Mapping[str, Any] | None) -> tuple[dict[str, Any], str | None]:
    if metadata_diff is None or not isinstance(metadata_diff, Mapping):
        return _unsupported_diff_source("metadata_diff_missing"), "metadata_diff_missing"
    if metadata_diff.get("object") != CORPUS_METADATA_DIFF_OBJECT:
        return _unsupported_diff_source("unsupported_metadata_diff_object"), "unsupported_metadata_diff_object"
    if metadata_diff.get("schema_version") != CORPUS_METADATA_DIFF_SCHEMA_VERSION:
        return _unsupported_diff_source("unsupported_metadata_diff_schema"), "unsupported_metadata_diff_schema"
    diff_status = _safe_field_name(str(metadata_diff.get("diff_status", "unknown")))
    if diff_status not in ACCEPTED_METADATA_DIFF_STATUSES:
        return (
            {
                "metadata_diff_schema_version": CORPUS_METADATA_DIFF_SCHEMA_VERSION,
                "metadata_diff_id": _symbolic_or_default(metadata_diff.get("diff_id"), "corpus-metadata-diff"),
                "diff_status": diff_status,
            },
            f"metadata_diff_status_{diff_status}",
        )
    return (
        {
            "metadata_diff_schema_version": CORPUS_METADATA_DIFF_SCHEMA_VERSION,
            "metadata_diff_id": _symbolic_or_default(metadata_diff.get("diff_id"), "corpus-metadata-diff"),
            "diff_status": diff_status,
        },
        None,
    )


def _unsupported_diff_source(reason: str) -> dict[str, Any]:
    return {
        "metadata_diff_schema_version": "unsupported",
        "metadata_diff_id": None,
        "diff_status": "unavailable",
        "unavailable_reason": reason,
    }


def _draft_context(value: Mapping[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    if value is None:
        return {"created_at_utc": DEFAULT_CREATED_AT_UTC}, []
    if not isinstance(value, Mapping):
        return {"created_at_utc": DEFAULT_CREATED_AT_UTC}, ["draft_context:not_mapping"]
    findings = _privacy_findings(value, "draft_context")
    if findings:
        return {"created_at_utc": DEFAULT_CREATED_AT_UTC, "status": "blocked"}, findings
    payload = _sanitize_mapping(value)
    payload.setdefault("created_at_utc", DEFAULT_CREATED_AT_UTC)
    return payload, []


def _corpus_manifest_issue(corpus_manifest: Mapping[str, Any]) -> str | None:
    if not isinstance(corpus_manifest, Mapping):
        return "corpus_manifest:not_mapping"
    if corpus_manifest.get("object") != CORPUS_MANIFEST_OBJECT:
        return "corpus_manifest:unsupported_object"
    if corpus_manifest.get("schema_version") != CORPUS_MANIFEST_SCHEMA_VERSION:
        return "corpus_manifest:unsupported_schema"
    if not isinstance(corpus_manifest.get("entries"), Sequence) or isinstance(corpus_manifest.get("entries"), str):
        return "corpus_manifest:entries_not_sequence"
    return None


def _session_ledger_issue(session_ledger: Mapping[str, Any]) -> str | None:
    if not isinstance(session_ledger, Mapping):
        return "session_ledger:not_mapping"
    if session_ledger.get("object") != SESSION_LEDGER_OBJECT:
        return "session_ledger:unsupported_object"
    if session_ledger.get("schema_version") != SESSION_LEDGER_SCHEMA_VERSION:
        return "session_ledger:unsupported_schema"
    if not isinstance(session_ledger.get("sessions"), Sequence) or isinstance(session_ledger.get("sessions"), str):
        return "session_ledger:sessions_not_sequence"
    return None


def _parser_expected_preview(
    value: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], str | None, list[str]]:
    empty = {
        "source_refs": [],
        "scenario_families": [],
        "parser_event_families": [],
        "expected_sections": {},
        "expected_degradation": [],
    }
    if value is None or not isinstance(value, Mapping):
        return empty, "parser_preview_missing", []
    findings = _privacy_findings(value, "parser_expected_fact_preview")
    if findings:
        return empty, None, findings
    source_refs = _safe_string_list(value.get("source_refs"))
    if not source_refs:
        return empty, "parser_preview_source_refs_missing", []
    expected_sections_value = value.get("expected_sections")
    if not isinstance(expected_sections_value, Mapping):
        return empty, "parser_preview_expected_sections_missing", []
    expected_sections: dict[str, Any] = {}
    unsupported_sections: list[str] = []
    for section, payload in sorted(expected_sections_value.items(), key=lambda item: str(item[0])):
        safe_section = _safe_field_name(str(section))
        if safe_section not in ALLOWED_EXPECTED_SECTIONS:
            unsupported_sections.append(safe_section)
            continue
        expected_sections[safe_section] = _sanitize_value(payload)
    if unsupported_sections:
        return {
            **empty,
            "source_refs": source_refs,
            "unsupported_sections": unsupported_sections,
        }, "parser_preview_forbidden_expected_sections", []
    if not expected_sections:
        return empty, "parser_preview_expected_sections_empty", []
    return (
        {
            "source_refs": source_refs,
            "scenario_families": _safe_string_list(value.get("scenario_families")),
            "parser_event_families": _safe_string_list(value.get("parser_event_families")),
            "expected_sections": expected_sections,
            "expected_degradation": _safe_string_list(value.get("expected_degradation")),
        },
        None,
        [],
    )


def _scenario_families(
    *,
    preview_payload: Mapping[str, Any],
    metadata_diff: Mapping[str, Any] | None,
    promotion_proof: Mapping[str, Any] | None,
    context: Mapping[str, Any],
) -> list[str]:
    families: list[str] = []
    families.extend(_safe_string_list(preview_payload.get("scenario_families")))
    if isinstance(metadata_diff, Mapping):
        transition = metadata_diff.get("coverage_transition")
        if isinstance(transition, Mapping):
            families.extend(_safe_string_list(transition.get("families")))
    if isinstance(promotion_proof, Mapping):
        comparison = promotion_proof.get("coverage_comparison")
        if isinstance(comparison, Mapping):
            family = _safe_field_name(str(comparison.get("family", "")))
            if family != "unknown":
                families.append(family)
    families.extend(_safe_string_list(context.get("scenario_families")))
    return _dedupe(sorted(families))


def _parser_event_families(preview_payload: Mapping[str, Any], context: Mapping[str, Any]) -> list[str]:
    families = _safe_string_list(preview_payload.get("parser_event_families"))
    families.extend(_safe_string_list(context.get("parser_event_families")))
    if not families:
        event_counts = preview_payload.get("expected_sections", {}).get("event_family_counts")
        if isinstance(event_counts, Mapping):
            families.extend(_safe_field_name(str(key)) for key in event_counts)
    return _dedupe(sorted(family for family in families if family != "unknown"))


def _known_gaps(
    metadata_diff: Mapping[str, Any] | None,
    promotion_proof: Mapping[str, Any] | None,
    context: Mapping[str, Any],
) -> list[str]:
    gaps: list[str] = []
    gaps.extend(_safe_string_list(context.get("known_gaps")))
    if isinstance(metadata_diff, Mapping):
        proposed_changes = metadata_diff.get("proposed_changes")
        if isinstance(proposed_changes, Mapping):
            for section in ("manifest_entries", "session_entries"):
                entries = proposed_changes.get(section)
                if isinstance(entries, Sequence) and not isinstance(entries, str):
                    for entry in entries:
                        if isinstance(entry, Mapping):
                            gaps.extend(_safe_string_list(entry.get("known_gaps")))
    if isinstance(promotion_proof, Mapping):
        coverage = promotion_proof.get("coverage_comparison")
        if isinstance(coverage, Mapping):
            kind = _safe_field_name(str(coverage.get("status_change_kind", "unknown")))
            if kind != "unknown":
                gaps.append(f"proof_coverage_{kind}")
    if not gaps:
        gaps.append("draft preserves existing known gaps; no corpus status change is authorized")
    return _dedupe(gaps)


def _fixture_window_summary(context: Mapping[str, Any]) -> tuple[dict[str, Any], str | None]:
    value = context.get("fixture_window_summary")
    if not isinstance(value, Mapping):
        return {
            "window_kind": "symbolic_minimal_slice",
            "line_count": None,
            "event_count": None,
            "ordering_required": False,
            "window_notes": ["no fixture window file writing authorized"],
        }, None
    summary = _sanitize_mapping(value)
    line_count = _safe_int(summary.get("line_count", summary.get("source_line_count")))
    event_count = _safe_int(summary.get("event_count"))
    max_line_count = _safe_int(context.get("max_fixture_line_count")) or DEFAULT_MAX_FIXTURE_LINE_COUNT
    summary["line_count"] = line_count
    summary["event_count"] = event_count
    summary["ordering_required"] = summary.get("ordering_required") is True
    summary.setdefault("window_kind", "symbolic_minimal_slice")
    summary.setdefault("window_notes", ["no fixture window file writing authorized"])
    if line_count is not None and line_count > max_line_count:
        return summary, "refused_oversized_window"
    if summary.get("ambiguous_window") is True:
        return summary, "refused_ambiguous_window"
    if summary.get("multi_family_window") is True:
        return summary, "refused_multi_family_window"
    return summary, None


def _draft_packet_id(context: Mapping[str, Any], source_artifacts: Mapping[str, Any]) -> str:
    if isinstance(context.get("packet_id"), str):
        return _symbolic_or_default(context["packet_id"], "golden-replay-draft-packet")
    proof_id = source_artifacts.get("promotion_proof_id") or "golden-replay"
    return _symbolic_or_default(f"{proof_id}:golden-replay-draft-packet", "golden-replay-draft-packet")


def _proposed_path(value: Any, *, default: str) -> str:
    if value is None:
        return default
    if not isinstance(value, str) or _contains_forbidden_text(value):
        return default
    normalized = value.strip()
    if not normalized or normalized.startswith("/") or ".." in normalized.split("/"):
        return default
    if not _REPO_RELATIVE_PATH_RE.match(normalized):
        return default
    return normalized


def _authorization_reasons(
    *,
    source_privacy_class: str,
    sanitization_status: str,
    promotion_proof: Mapping[str, Any] | None,
    metadata_diff: Mapping[str, Any] | None,
) -> list[str]:
    reasons: list[str] = []
    if source_privacy_class in {"blocked_private_evidence", "blocked_external_boundary"}:
        reasons.append(f"source_privacy_class_{source_privacy_class}")
    if sanitization_status == "blocked_privacy":
        reasons.append("sanitization_status_blocked_privacy")
    if isinstance(promotion_proof, Mapping):
        comparison = promotion_proof.get("coverage_comparison")
        if isinstance(comparison, Mapping):
            change_kind = comparison.get("status_change_kind")
            if change_kind in {"blocked_private_evidence", "blocked_external_boundary"}:
                reasons.append(f"proof_coverage_{change_kind}")
    if isinstance(metadata_diff, Mapping):
        transition = metadata_diff.get("coverage_transition")
        if isinstance(transition, Mapping):
            transition_kind = transition.get("transition_kind")
            if transition_kind in {
                "blocked_private_evidence_no_change",
                "blocked_external_boundary_no_change",
            }:
                reasons.append(f"metadata_{transition_kind}")
    return _dedupe(reasons)


def _draft_status(
    *,
    privacy_findings: Sequence[str],
    authorization_reasons: Sequence[str],
    overclaim_reasons: Sequence[str],
    schema_issues: Sequence[str | None],
    review_issue: str | None,
    proof_issue: str | None,
    diff_issue: str | None,
    preview_issue: str | None,
    window_issue: str | None,
    family_candidates: Sequence[str],
) -> str:
    if privacy_findings:
        return "blocked_privacy"
    if authorization_reasons:
        return "blocked_authorization"
    if overclaim_reasons:
        return "blocked_overclaim"
    if any(schema_issues):
        return "needs_contract_update"
    if review_issue:
        if "status_" in review_issue or "missing" in review_issue:
            return "insufficient_review"
        return "needs_contract_update"
    if proof_issue:
        if "status_" in proof_issue or "missing" in proof_issue:
            return "insufficient_proof"
        return "needs_contract_update"
    if diff_issue:
        if "status_" in diff_issue or "missing" in diff_issue:
            return "insufficient_metadata_diff"
        return "needs_contract_update"
    if preview_issue:
        if preview_issue == "parser_preview_forbidden_expected_sections":
            return "blocked_overclaim"
        return "insufficient_parser_preview"
    if window_issue in DRAFT_STATUSES:
        return window_issue
    if not family_candidates:
        return "refused_ambiguous_window"
    if len(family_candidates) > 1:
        return "refused_multi_family_window"
    return "draft_ready_for_review"


def _status_reasons(
    *,
    privacy_findings: Sequence[str],
    authorization_reasons: Sequence[str],
    overclaim_reasons: Sequence[str],
    schema_issues: Sequence[str | None],
    review_issue: str | None,
    proof_issue: str | None,
    diff_issue: str | None,
    preview_issue: str | None,
    window_issue: str | None,
    family_candidates: Sequence[str],
) -> list[str]:
    reasons = [
        *(issue for issue in schema_issues if issue),
        *(f"privacy:{finding}" for finding in privacy_findings),
        *(f"authorization:{reason}" for reason in authorization_reasons),
        *(f"overclaim:{reason}" for reason in overclaim_reasons),
    ]
    for issue in (review_issue, proof_issue, diff_issue, preview_issue, window_issue):
        if issue:
            reasons.append(issue)
    if not family_candidates:
        reasons.append("scenario_family_missing")
    elif len(family_candidates) > 1:
        reasons.append("multiple_scenario_families")
    return _dedupe([_safe_field_name(reason) for reason in reasons])


def _expected_section_overclaims(preview_payload: Mapping[str, Any]) -> list[str]:
    unsupported = preview_payload.get("unsupported_sections")
    if isinstance(unsupported, Sequence) and not isinstance(unsupported, str):
        return [f"forbidden_expected_section_{_safe_field_name(str(section))}" for section in unsupported]
    return []


def _overclaim_reasons(values: Sequence[Any]) -> list[str]:
    reasons: list[str] = []
    for value in values:
        reasons.extend(_overclaim_reasons_in_value(value, "input"))
    return _dedupe(reasons)


def _overclaim_reasons_in_value(value: Any, label: str) -> list[str]:
    reasons: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_label = _safe_field_name(str(key))
            if key_label in _OVERCLAIM_KEYS and item is True:
                reasons.append(f"{label}.{key_label}_true")
            reasons.extend(_overclaim_reasons_in_value(item, f"{label}.{key_label}"))
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for index, item in enumerate(value):
            reasons.extend(_overclaim_reasons_in_value(item, f"{label}.{index}"))
    return reasons


def _minimization(
    scenario_families: Sequence[str],
    parser_event_families: Sequence[str],
    window_issue: str | None,
) -> dict[str, Any]:
    return {
        "single_primary_scenario_family": len(scenario_families) == 1,
        "parser_event_family_count": len(parser_event_families),
        "window_refusal_status": window_issue,
        "file_writing_authorized": False,
        "fixture_promotion_authorized": False,
        "notes": [
            "draft describes a minimal proposed replay slice only",
            "future file writing requires a separate contract",
        ],
    }


def _redaction_summary(source_privacy_class: str, sanitization_status: str) -> dict[str, Any]:
    return {
        "source_privacy_class": source_privacy_class,
        "sanitization_status": sanitization_status,
        "raw_private_log_committed": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "local_private_artifacts_committed": False,
        "external_logs_committed": False,
        "redaction_categories": ["raw_lines", "raw_payloads", "private_paths", "secrets"],
    }


def _privacy_summary(privacy_findings: Sequence[str]) -> dict[str, Any]:
    return {
        "raw_private_log_committed": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "local_private_artifacts_committed": False,
        "external_logs_committed": False,
        "privacy_finding_count": len(privacy_findings),
        "privacy_findings": _privacy_finding_records(privacy_findings),
    }


def _review_gates() -> list[str]:
    return [
        "harvest_review_packet_accepted",
        "fixture_promotion_proof_ready_for_review",
        "metadata_diff_ready_or_no_change",
        "privacy_check_passed",
        "protected_surface_check_passed",
        "minimal_public_safe_draft_reviewed",
        "later_contract_authorizes_file_writing",
        "later_review_approves_corpus_metadata_change",
    ]


def _authorization_flags() -> dict[str, bool]:
    return {
        "file_writing_authorized": False,
        "private_harvest_authorized": False,
        "fixture_promotion_authorized": False,
        "corpus_status_change_authorized": False,
    }


def _readiness_flags() -> dict[str, bool]:
    return {
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
    }


def _non_claims() -> list[str]:
    return [
        "not_parser_truth",
        "not_golden_replay_pass_evidence",
        "not_fixture_promotion_authority",
        "not_file_writing_authority",
        "not_corpus_metadata_mutation_authority",
        "not_corpus_status_movement",
        "not_private_evidence_approval",
        "not_issue_388_or_381_activation",
        "not_parser_behavior_ready",
        "not_release_readiness",
        "not_deploy_readiness",
        "not_production_readiness",
        "not_analytics_truth",
        "not_ai_truth",
        "not_coaching_truth",
        "not_full_parser_regression_parity",
    ]


def _privacy_finding_records(findings: Sequence[str]) -> list[dict[str, str]]:
    records = []
    for index, finding in enumerate(findings, start=1):
        field, _, reason = finding.partition(":")
        records.append(
            {
                "finding_id": f"golden-replay-draft-privacy-finding-{index}",
                "field": _safe_field_name(field),
                "reason": _safe_field_name(reason or "forbidden"),
            },
        )
    return records


def _privacy_findings(value: Any, label: str) -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_label = _safe_field_name(str(key))
            key_text = str(key)
            if key_text in _PATH_REFERENCE_KEYS and _contains_forbidden_reference_path(item):
                findings.append(f"{label}.{key_label}:forbidden_path")
                continue
            if key_text in _SEQUENCE_REFERENCE_KEYS:
                findings.extend(_reference_path_findings(item, f"{label}.{key_label}"))
            if _contains_private_value(item) and _SEMANTIC_PRIVACY_KEY_RE.search(key_text):
                findings.append(f"{label}.{key_label}:forbidden_semantic_key")
                continue
            if _GENERIC_NOTE_PRIVACY_KEY_RE.search(key_text) and _contains_forbidden_generic_note(item):
                findings.append(f"{label}.{key_label}:forbidden_semantic_note")
                continue
            if (
                _SENSITIVE_KEY_RE.search(key_text)
                and key_text not in _SAFE_FALSE_FLAG_KEYS
                and key_text not in _SAFE_REFERENCE_KEYS
                and _contains_private_value(item)
            ):
                findings.append(f"{label}.{key_label}:forbidden_key")
                continue
            findings.extend(_privacy_findings(item, f"{label}.{key_label}"))
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for index, item in enumerate(value):
            findings.extend(_privacy_findings(item, f"{label}.{index}"))
    elif isinstance(value, str) and _contains_forbidden_text(value):
        findings.append(f"{label}:forbidden_text")
    return _dedupe(findings)


def _contains_private_value(value: Any) -> bool:
    return value not in (False, None, "", [], {})


def _contains_forbidden_generic_note(value: Any) -> bool:
    if isinstance(value, str):
        return bool(_GENERIC_NOTE_PRIVACY_TEXT_RE.search(value))
    if isinstance(value, Mapping):
        return any(_contains_forbidden_generic_note(item) for item in value.values())
    if isinstance(value, Sequence):
        return any(_contains_forbidden_generic_note(item) for item in value)
    return False


def _reference_path_findings(value: Any, label: str) -> list[str]:
    findings: list[str] = []
    if isinstance(value, str):
        if _contains_forbidden_reference_path(value):
            findings.append(f"{label}:forbidden_path")
    elif isinstance(value, Mapping):
        for key, item in value.items():
            findings.extend(_reference_path_findings(item, f"{label}.{_safe_field_name(str(key))}"))
    elif isinstance(value, Sequence):
        for index, item in enumerate(value):
            findings.extend(_reference_path_findings(item, f"{label}.{index}"))
    return _dedupe(findings)


def _contains_forbidden_reference_path(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    decoded = value.strip()
    for _ in range(2):
        decoded = unquote(decoded)
    normalized = decoded.replace("\\", "/").strip()
    if not normalized:
        return False
    if _contains_forbidden_text(normalized):
        return True
    if (
        normalized.startswith("/")
        or normalized.startswith("~")
        or normalized == ".."
        or normalized.startswith("../")
        or "/../" in normalized
        or normalized.endswith("/..")
    ):
        return True
    parts = [part.lower() for part in normalized.split("/") if part and part != "."]
    return any(part in _FORBIDDEN_REPO_PATH_SEGMENTS for part in parts) or (
        bool(parts) and parts[-1] in _FORBIDDEN_REPO_PATH_FILENAMES
    )


def _sanitize_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, item in sorted(value.items(), key=lambda item: str(item[0])):
        safe_key = _safe_field_name(str(key))
        output[safe_key] = _sanitize_value(item)
    return output


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return _sanitize_mapping(value)
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_sanitize_value(item) for item in value]
    if isinstance(value, str):
        return _public_safe_string_or_default(value, "unavailable")
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int | float):
        return value
    return str(value)


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        return []
    output = []
    for item in value:
        if not isinstance(item, str):
            continue
        safe_item = _public_safe_string_or_default(item, "unavailable")
        if safe_item != "unavailable":
            output.append(safe_item)
    return _dedupe(output)


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def _symbolic_or_default(value: Any, default: str) -> str:
    if isinstance(value, str) and _SYMBOLIC_TEXT_RE.match(value) and not _contains_forbidden_text(value):
        return value
    return default


def _member_or_default(value: Any, accepted: frozenset[str], default: str) -> str:
    if isinstance(value, str) and value in accepted:
        return value
    return default


def _public_safe_string_or_default(value: Any, default: str) -> str:
    if not isinstance(value, str) or _contains_forbidden_text(value):
        return default
    return value


def _safe_field_name(value: Any) -> str:
    if not isinstance(value, str):
        return "unknown"
    value = value.strip()
    if not value or _contains_forbidden_text(value):
        return "unknown"
    normalized = re.sub(r"[^A-Za-z0-9._:-]+", "_", value).strip("_")
    if not normalized or not _FIELD_NAME_RE.match(normalized):
        return "unknown"
    return normalized


def _contains_forbidden_text(value: str) -> bool:
    decoded = value
    for _ in range(2):
        decoded = unquote(decoded)
    return any(
        pattern.search(decoded)
        for pattern in (
            _FORBIDDEN_TEXT_RE,
            _FORBIDDEN_LABELED_PATH_RE,
            _FORBIDDEN_URI_LOCAL_PATH_RE,
        )
    )


def _dedupe(values: Sequence[str] | Any) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output
