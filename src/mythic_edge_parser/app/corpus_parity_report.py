from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .diagnostics import sanitize_sensitive_text

MANIFEST_OBJECT = "mythic_edge_parser_corpus_manifest"
MANIFEST_SCHEMA_VERSION = "parser_corpus_manifest.v1"
SESSION_LEDGER_OBJECT = "mythic_edge_parser_corpus_session_ledger"
SESSION_LEDGER_SCHEMA_VERSION = "parser_corpus_session_ledger.v1"
REPORT_OBJECT = "mythic_edge_parser_corpus_compatibility_report"
REPORT_SCHEMA_VERSION = "parser_corpus_compatibility_report.v1"
READINESS_METRICS_SCHEMA_VERSION = "parser_corpus_readiness_metrics.v1"
COMPETITIVE_CORE_SCHEMA_VERSION = "parser_corpus_competitive_core.v1"

CORPUS_ID = "mythic_edge_parser_reliability_corpus_v1"
SCENARIO_FAMILY_VERSION = "parser_corpus_scenario_family.v1"

STATUS_COVERAGE_MAP_READY = "coverage_map_ready"
STATUS_PARTIAL_COVERAGE_MAP_READY = "partial_coverage_map_ready"
STATUS_REVIEW = "review"
STATUS_BLOCKED_PRIVATE = "blocked_private_artifact_risk"
STATUS_BLOCKED_EXTERNAL = "blocked_external_boundary"
STATUS_FAIL = "fail"

ENTRY_TYPES = {
    "golden_replay_manifest",
    "feature_equity_report",
    "diagnostics_report",
    "session_ledger_entry",
    "external_reference_category",
    "local_private_report_summary",
}
SOURCE_KINDS = {
    "sanitized_committed_fixture",
    "synthetic_committed_fixture",
    "committed_count_only_report",
    "local_private_report_only",
    "external_reference_only",
}
COMMIT_STATUSES = {"committed", "local_report_only", "external_reference_only", "deferred"}
PRIVACY_CLASSES = {
    "sanitized_committable",
    "synthetic_committable",
    "committed_count_only",
    "local_private_not_committed",
    "external_reference_metadata_only",
}
SANITIZATION_STATUSES = {
    "sanitized",
    "synthetic",
    "not_applicable_count_only",
    "not_applicable_external_reference",
    "requires_review",
}
COVERAGE_STATUSES = {
    "covered_committed",
    "covered_synthetic",
    "covered_report_only",
    "partial",
    "missing",
    "deferred",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "not_applicable",
}
COVERAGE_STATUS_PRECEDENCE = (
    "covered_committed",
    "covered_synthetic",
    "covered_report_only",
    "partial",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "deferred",
    "missing",
    "not_applicable",
)
COVERAGE_BASIS_VALUES = {
    "parser_behavior_verified",
    "fixture_metadata_only",
    "diagnostics_only",
    "count_ratchet_only",
    "evidence_ledger_only",
    "local_report_only",
    "external_reference_only",
}
EXTERNAL_REFERENCE_STATUSES = {
    "reference_category_present",
    "reference_category_not_checked",
    "reference_not_applicable",
}

SCENARIO_FAMILIES = (
    "manifest.metadata",
    "session.ledger_metadata",
    "core_gameplay.standard_bo1",
    "core_gameplay.standard_bo3",
    "core_gameplay.traditional_bo3",
    "core_gameplay.draft_with_games",
    "core_gameplay.draft_only",
    "core_gameplay.sealed_entry",
    "core_gameplay.sealed_deckbuild",
    "core_gameplay.sealed_matches",
    "log_runtime.detailed_logs_disabled",
    "log_runtime.rotation",
    "log_runtime.malformed_or_headerless",
    "log_runtime.timestamp_anomaly",
    "log_runtime.unknown_entry",
    "connection.reconnect",
    "connection.disconnect",
    "connection.firewall_or_network_drop",
    "connection.connection_error_payload",
    "timer.active_player_timer",
    "timer.inactivity_timeout",
    "timer.pre_match_idle",
    "deck_api.start_hook_deck_snapshot",
    "deck_api.deck_summary",
    "deck_api.deck_upsert",
    "deck_api.event_set_deck",
    "deck_api.store_pack_inbox_or_crafting",
    "gameplay_stress.mulligan",
    "gameplay_stress.opponent_auto_concede",
    "gameplay_stress.conjure",
    "gameplay_stress.spellbook",
    "gameplay_stress.companion_or_large_deck",
    "gameplay_stress.action_attribution",
    "gameplay_stress.event_ordering",
    "drift_debug.gsm_truncation",
    "drift_debug.recycle_or_rollback",
    "drift_debug.missing_message_type",
    "drift_debug.rename_or_rotation_collision",
    "drift_debug.phantom_or_deck_origin",
    "mythic_edge.evidence_ledger_provenance",
    "mythic_edge.confidence_finality_degradation",
    "mythic_edge.workbook_row_coverage",
    "mythic_edge.live_diagnostics",
    "mythic_edge.private_log_report_only_drift",
    "mythic_edge.analytics_readiness_labels",
)

COMPETITIVE_CORE_FAMILIES = (
    "core_gameplay.standard_bo1",
    "core_gameplay.standard_bo3",
    "core_gameplay.traditional_bo3",
    "core_gameplay.draft_with_games",
    "core_gameplay.sealed_matches",
    "gameplay_stress.mulligan",
    "gameplay_stress.opponent_auto_concede",
    "gameplay_stress.conjure",
    "gameplay_stress.spellbook",
    "gameplay_stress.companion_or_large_deck",
    "gameplay_stress.action_attribution",
    "gameplay_stress.event_ordering",
    "timer.active_player_timer",
    "timer.pre_match_idle",
    "timer.inactivity_timeout",
    "drift_debug.gsm_truncation",
)

LOCAL_PATH_PREFIX_PATTERN = "|".join(
    (
        "/" + r"[Uu]sers/",
        "/" + "private/var/",
        "/" + "home/",
        r"[A-Z]:\\" + r"[Uu]sers\\",
    )
)
LOCAL_ABSOLUTE_PATH_PATTERN = re.compile(rf"(?i)({LOCAL_PATH_PREFIX_PATTERN})[^\s,;)>\]\}}\"']+")
SECRET_ASSIGNMENT_PATTERN = re.compile(r"(?i)\b(api[_-]?key|secret|token|webhook)\s*[:=]\s*\S+")

FORBIDDEN_REPORT_PATTERNS = (
    ("local_absolute_path", LOCAL_ABSOLUTE_PATH_PATTERN),
    (
        "raw_log_line_marker",
        re.compile(
            r'(?i)player\.log raw|raw log line|raw_game_state|raw_payload_value|raw_payload_object|"raw_payload"\s*:'
        ),
    ),
    ("webhook_url", re.compile(r"https?://hooks\.[^\s)>\]}\"]+", re.IGNORECASE)),
    ("apps_script_url", re.compile(r"https?://script\.google\.com/[^\s)>\]}\"]+", re.IGNORECASE)),
    ("secret_assignment", SECRET_ASSIGNMENT_PATTERN),
)
FORBIDDEN_PATH_SUFFIXES = (".log", ".log.gz", ".zip", ".sqlite", ".sqlite3", ".db", ".db-wal", ".db-shm")


def build_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = load_corpus_manifest(manifest_path)
    manifest_errors = validate_corpus_manifest(manifest)
    session_ledger: dict[str, Any] | None = None
    session_errors: list[str] = []
    if session_ledger_path is not None:
        session_ledger = load_session_ledger(session_ledger_path)
        session_errors = validate_session_ledger(session_ledger)

    validation_errors = [*manifest_errors, *session_errors]
    taxonomy_families = _taxonomy_family_ids(manifest)
    entries = _manifest_entries(manifest)
    matrix = _coverage_matrix(taxonomy_families, entries, external_reference=external_reference)
    gaps = _gap_records(matrix)
    summary = _summary(matrix)
    readiness_metrics = _readiness_metrics(matrix, summary)
    status = _report_status(validation_errors, summary)
    status_reasons = _status_reasons(validation_errors, summary)

    return _sanitize_report_value(
        {
            "object": REPORT_OBJECT,
            "schema_version": REPORT_SCHEMA_VERSION,
            "status": status,
            "status_reasons": status_reasons,
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "inputs": {
                "corpus_manifest_path": _safe_repo_path(manifest_path),
                "session_ledger_path": _safe_repo_path(session_ledger_path) if session_ledger_path else "",
                "feature_equity_report_supplied": feature_equity_report is not None,
                "external_reference": _external_reference_input(external_reference),
                "explicit_inputs_required": True,
            },
            "summary": summary,
            "readiness_metrics": readiness_metrics,
            "coverage_matrix": matrix,
            "gaps": gaps,
            "privacy": _privacy_section(manifest, session_ledger),
            "protected_surfaces": _protected_surfaces_section(),
            "limitations": _limitations_section(session_ledger_path=session_ledger_path),
        }
    )


def write_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report_path: Path | None = None,
    external_reference_path: Path | None = None,
    report_path: Path | None = None,
) -> dict[str, Any]:
    report = build_corpus_parity_report(
        manifest_path,
        session_ledger_path=session_ledger_path,
        feature_equity_report=_load_optional_json_object(feature_equity_report_path),
        external_reference=_load_optional_json_object(external_reference_path),
    )
    if report_path is not None:
        output_path = Path(report_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return report


def load_corpus_manifest(path: Path) -> dict[str, Any]:
    return _load_json_object(path)


def load_session_ledger(path: Path) -> dict[str, Any]:
    return _load_json_object(path)


def validate_corpus_manifest(payload: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("object") != MANIFEST_OBJECT:
        errors.append("invalid_manifest_object")
    if payload.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        errors.append("invalid_manifest_schema_version")
    if payload.get("corpus_id") != CORPUS_ID:
        errors.append("invalid_corpus_id")

    source_privacy = payload.get("source_privacy")
    if not isinstance(source_privacy, Mapping):
        errors.append("missing_source_privacy")
    else:
        for key in ("raw_private_log_committed", "external_logs_committed", "local_private_artifacts_committed"):
            if source_privacy.get(key) is not False:
                errors.append(f"source_privacy_not_false:{key}")

    taxonomy = payload.get("taxonomy")
    if not isinstance(taxonomy, Mapping):
        errors.append("missing_taxonomy")
    else:
        if taxonomy.get("scenario_family_version") != SCENARIO_FAMILY_VERSION:
            errors.append("invalid_scenario_family_version")
        family_ids = _taxonomy_family_ids(payload)
        missing = sorted(set(SCENARIO_FAMILIES) - set(family_ids))
        unknown = sorted(set(family_ids) - set(SCENARIO_FAMILIES))
        if missing:
            errors.append(f"missing_taxonomy_families:{','.join(missing)}")
        if unknown:
            errors.append(f"unknown_taxonomy_families:{','.join(unknown)}")

    entries = payload.get("entries")
    if not isinstance(entries, list):
        errors.append("entries_must_be_list")
        return errors
    if not entries:
        errors.append("entries_empty")

    seen_entry_ids: set[str] = set()
    for index, raw_entry in enumerate(entries):
        if not isinstance(raw_entry, Mapping):
            errors.append(f"entry_not_object:{index}")
            continue
        entry_id = _string(raw_entry.get("entry_id"))
        if not entry_id:
            errors.append(f"entry_missing_id:{index}")
        elif entry_id in seen_entry_ids:
            errors.append(f"duplicate_entry_id:{entry_id}")
        seen_entry_ids.add(entry_id)
        errors.extend(_entry_validation_errors(raw_entry, entry_id or str(index)))
    errors.extend(_forbidden_content_errors(payload))
    return sorted(dict.fromkeys(errors))


def validate_session_ledger(payload: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("object") != SESSION_LEDGER_OBJECT:
        errors.append("invalid_session_ledger_object")
    if payload.get("schema_version") != SESSION_LEDGER_SCHEMA_VERSION:
        errors.append("invalid_session_ledger_schema_version")
    sessions = payload.get("sessions")
    if not isinstance(sessions, list):
        errors.append("sessions_must_be_list")
        return errors
    if not sessions:
        errors.append("sessions_empty")
    seen_session_ids: set[str] = set()
    for index, raw_session in enumerate(sessions):
        if not isinstance(raw_session, Mapping):
            errors.append(f"session_not_object:{index}")
            continue
        session_id = _string(raw_session.get("session_id"))
        if not session_id:
            errors.append(f"session_missing_id:{index}")
        elif session_id in seen_session_ids:
            errors.append(f"duplicate_session_id:{session_id}")
        seen_session_ids.add(session_id)
        errors.extend(_session_validation_errors(raw_session, session_id or str(index)))
    errors.extend(_forbidden_content_errors(payload))
    return sorted(dict.fromkeys(errors))


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = write_corpus_parity_report(
        Path(args.manifest_path),
        session_ledger_path=Path(args.session_ledger_path) if args.session_ledger_path else None,
        feature_equity_report_path=Path(args.feature_equity_report_path) if args.feature_equity_report_path else None,
        external_reference_path=Path(args.external_reference_path) if args.external_reference_path else None,
        report_path=Path(args.report_path) if args.report_path else None,
    )
    summary = report["summary"]
    readiness = report["readiness_metrics"]
    parser_behavior_ready = "yes" if readiness["parser_behavior_ready"] else "no"
    print(
        "Corpus parity report: "
        f"{report['status']} "
        f"({summary['total_scenario_families']} families; "
        f"committed={summary['covered_committed']}, "
        f"synthetic={summary['covered_synthetic']}, "
        f"report_only={summary['covered_report_only']}, "
        f"blocked={readiness['blocked_families']} "
        f"[private={summary['blocked_private_evidence']}, external={summary['blocked_external_boundary']}], "
        f"missing={summary['missing']}, "
        f"parser_behavior_ready={parser_behavior_ready})"
    )
    if args.report_path:
        print(f"Report written: {_safe_repo_path(Path(args.report_path))}")
    return 1 if report["status"] in {STATUS_FAIL, STATUS_BLOCKED_PRIVATE, STATUS_BLOCKED_EXTERNAL} else 0


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a report-only parser corpus parity compatibility report.")
    parser.add_argument("manifest_path", help="Corpus manifest JSON path.")
    parser.add_argument(
        "--session-ledger",
        dest="session_ledger_path",
        default="",
        help="Optional session ledger JSON.",
    )
    parser.add_argument(
        "--feature-equity-report",
        dest="feature_equity_report_path",
        default="",
        help="Optional feature-equity report JSON.",
    )
    parser.add_argument(
        "--external-reference",
        dest="external_reference_path",
        default="",
        help="Optional category-only external reference JSON.",
    )
    parser.add_argument("--out", dest="report_path", default="", help="Optional local JSON report output path.")
    return parser


def _entry_validation_errors(entry: Mapping[str, Any], entry_id: str) -> list[str]:
    errors: list[str] = []
    _require_value(errors, entry, "entry_type", ENTRY_TYPES, entry_id)
    _require_value(errors, entry, "source_kind", SOURCE_KINDS, entry_id)
    _require_value(errors, entry, "commit_status", COMMIT_STATUSES, entry_id)
    _require_value(errors, entry, "privacy_class", PRIVACY_CLASSES, entry_id)
    sanitization_status = _require_value(errors, entry, "sanitization_status", SANITIZATION_STATUSES, entry_id)
    coverage_status = _require_value(errors, entry, "coverage_status", COVERAGE_STATUSES, entry_id)
    if sanitization_status == "requires_review" and entry.get("commit_status") == "committed":
        errors.append(f"requires_review_entry_committed:{entry_id}")
    if coverage_status == "covered_committed" and entry.get("commit_status") != "committed":
        errors.append(f"covered_committed_entry_not_committed:{entry_id}")
    if entry.get("source_kind") == "external_reference_only" and entry.get("coverage_status") == "covered_committed":
        errors.append(f"external_reference_marked_committed:{entry_id}")
    if entry.get("source_kind") == "local_private_report_only" and entry.get("coverage_status") == "covered_committed":
        errors.append(f"local_private_marked_committed:{entry_id}")
    if not _string(entry.get("linked_issue")):
        errors.append(f"entry_missing_linked_issue:{entry_id}")
    if not _string(entry.get("authorized_by_contract")):
        errors.append(f"entry_missing_authorized_by_contract:{entry_id}")
    for field in ("scenario_families", "parser_event_families", "parser_claim_families", "known_gaps", "review_notes"):
        if not isinstance(entry.get(field), list):
            errors.append(f"entry_field_not_list:{entry_id}:{field}")
    for family in _string_list(entry.get("scenario_families")):
        if family not in SCENARIO_FAMILIES:
            errors.append(f"entry_unknown_scenario_family:{entry_id}:{family}")
    for basis in _string_list(entry.get("coverage_basis")):
        if basis not in COVERAGE_BASIS_VALUES:
            errors.append(f"entry_unknown_coverage_basis:{entry_id}:{basis}")
    if entry.get("entry_type") == "golden_replay_manifest":
        paths = entry.get("paths")
        if not isinstance(paths, Mapping) or not _string(paths.get("golden_replay_manifest")):
            errors.append(f"entry_missing_golden_replay_manifest_path:{entry_id}")
    errors.extend(_path_errors(entry.get("paths"), entry_id))
    return errors


def _session_validation_errors(session: Mapping[str, Any], session_id: str) -> list[str]:
    errors: list[str] = []
    for field in ("title", "record_summary", "format_family", "match_shape"):
        if not _string(session.get(field)):
            errors.append(f"session_missing_{field}:{session_id}")
    _require_value(errors, session, "source_kind", SOURCE_KINDS, session_id)
    _require_value(errors, session, "commit_status", COMMIT_STATUSES, session_id)
    _require_value(errors, session, "privacy_class", PRIVACY_CLASSES, session_id)
    if not isinstance(session.get("scenario_families"), list):
        errors.append(f"session_field_not_list:{session_id}:scenario_families")
    for family in _string_list(session.get("scenario_families")):
        if family not in SCENARIO_FAMILIES:
            errors.append(f"session_unknown_scenario_family:{session_id}:{family}")
    redactions = session.get("report_only_redactions")
    if not isinstance(redactions, Mapping):
        errors.append(f"session_missing_report_only_redactions:{session_id}")
    else:
        for key in ("raw_log_lines_included", "private_paths_included", "raw_payloads_included"):
            if redactions.get(key) is not False:
                errors.append(f"session_redaction_flag_not_false:{session_id}:{key}")
    return errors


def _coverage_matrix(
    taxonomy_families: Sequence[str],
    entries: Sequence[Mapping[str, Any]],
    *,
    external_reference: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    by_family: dict[str, list[Mapping[str, Any]]] = {family: [] for family in taxonomy_families}
    for entry in entries:
        for family in _string_list(entry.get("scenario_families")):
            by_family.setdefault(family, []).append(entry)
    external_families = set(_string_list((external_reference or {}).get("scenario_families")))
    matrix: list[dict[str, Any]] = []
    for family in taxonomy_families:
        family_entries = by_family.get(family, [])
        status = _family_coverage_status(family_entries)
        basis = _family_coverage_basis(family_entries, status)
        matrix.append(
            {
                "scenario_family": family,
                "coverage_status": status,
                "coverage_basis": basis,
                "mythic_edge_entries": sorted(
                    _string(entry.get("entry_id")) for entry in family_entries if _string(entry.get("entry_id"))
                ),
                "external_reference_status": "reference_category_present"
                if family in external_families
                else "reference_category_not_checked",
                "notes": _family_notes(family_entries),
            }
        )
    return matrix


def _gap_records(matrix: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gap_statuses = {"missing", "partial", "deferred", "blocked_private_evidence", "blocked_external_boundary"}
    gaps: list[dict[str, Any]] = []
    for row in matrix:
        status = _string(row.get("coverage_status"))
        if status not in gap_statuses:
            continue
        blocked_by = ["no_committed_safe_fixture"]
        if status == "blocked_private_evidence":
            blocked_by.append("private_evidence_required")
        if status == "blocked_external_boundary":
            blocked_by.append("external_boundary")
        gaps.append(
            {
                "scenario_family": _string(row.get("scenario_family")),
                "gap_status": status,
                "risk_tier": "High" if status.startswith("blocked_") else "Medium",
                "recommended_next_step": "Codex A problem representation or Codex B follow-up contract",
                "blocked_by": blocked_by,
            }
        )
    return gaps


def _summary(matrix: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    counts = Counter(_string(row.get("coverage_status")) for row in matrix)
    return {
        "total_scenario_families": len(matrix),
        "covered_committed": counts["covered_committed"],
        "covered_synthetic": counts["covered_synthetic"],
        "covered_report_only": counts["covered_report_only"],
        "partial": counts["partial"],
        "missing": counts["missing"],
        "deferred": counts["deferred"],
        "blocked_private_evidence": counts["blocked_private_evidence"],
        "blocked_external_boundary": counts["blocked_external_boundary"],
        "not_applicable": counts["not_applicable"],
    }


def _readiness_metrics(matrix: Sequence[Mapping[str, Any]], summary: Mapping[str, int]) -> dict[str, Any]:
    committed_parser_behavior = _parser_behavior_family_count(matrix, status="covered_committed")
    synthetic_parser_behavior = _parser_behavior_family_count(matrix, status="covered_synthetic")
    parser_behavior_ready_family_count = committed_parser_behavior + synthetic_parser_behavior
    total_families = summary.get("total_scenario_families", len(matrix))
    blocked_families = summary.get("blocked_private_evidence", 0) + summary.get("blocked_external_boundary", 0)
    classification_complete = not (
        summary.get("missing", 0) or summary.get("partial", 0) or summary.get("deferred", 0)
    )
    parser_behavior_ready = parser_behavior_ready_family_count == total_families and total_families > 0
    return {
        "schema_version": READINESS_METRICS_SCHEMA_VERSION,
        "classification_complete": classification_complete,
        "parser_behavior_ready": parser_behavior_ready,
        "parser_behavior_ready_family_count": parser_behavior_ready_family_count,
        "total_scenario_families": total_families,
        "committed_parser_behavior_families": committed_parser_behavior,
        "synthetic_parser_behavior_families": synthetic_parser_behavior,
        "report_only_families": summary.get("covered_report_only", 0),
        "blocked_families": blocked_families,
        "blocked_private_evidence_families": summary.get("blocked_private_evidence", 0),
        "blocked_external_boundary_families": summary.get("blocked_external_boundary", 0),
        "missing_families": summary.get("missing", 0),
        "partial_families": summary.get("partial", 0),
        "deferred_families": summary.get("deferred", 0),
        "pipeline_activation_ready_for_issue_388": parser_behavior_ready,
        "pipeline_activation_blockers": _pipeline_activation_blockers(summary),
        "readiness_verdict": _readiness_verdict(
            classification_complete=classification_complete,
            parser_behavior_ready=parser_behavior_ready,
        ),
        "competitive_core": _competitive_core_metrics(matrix),
    }


def _parser_behavior_family_count(matrix: Sequence[Mapping[str, Any]], *, status: str) -> int:
    return sum(
        1
        for row in matrix
        if _is_parser_behavior_ready_row(row) and _string(row.get("coverage_status")) == status
    )


def _is_parser_behavior_ready_row(row: Mapping[str, Any]) -> bool:
    status = _string(row.get("coverage_status"))
    return status in {"covered_committed", "covered_synthetic"} and _is_parser_behavior_row(row)


def _is_parser_behavior_row(row: Mapping[str, Any]) -> bool:
    return "parser_behavior_verified" in _string_list(row.get("coverage_basis"))


def _pipeline_activation_blockers(summary: Mapping[str, int]) -> list[str]:
    blocker_fields = (
        ("covered_report_only", "report_only_families"),
        ("blocked_private_evidence", "blocked_private_evidence_families"),
        ("blocked_external_boundary", "blocked_external_boundary_families"),
        ("missing", "missing_families"),
        ("partial", "partial_families"),
        ("deferred", "deferred_families"),
    )
    return [f"{label}:{summary.get(field, 0)}" for field, label in blocker_fields if summary.get(field, 0)]


def _readiness_verdict(*, classification_complete: bool, parser_behavior_ready: bool) -> str:
    if parser_behavior_ready:
        return "parser_behavior_ready"
    if classification_complete:
        return "classification_complete_not_behavior_ready"
    return "not_classified"


def _competitive_core_metrics(matrix: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_family = {_string(row.get("scenario_family")): row for row in matrix}
    core_rows = [by_family[family] for family in COMPETITIVE_CORE_FAMILIES if family in by_family]
    parser_behavior_count = sum(1 for row in core_rows if _is_parser_behavior_ready_row(row))
    report_only_count = sum(1 for row in core_rows if _string(row.get("coverage_status")) == "covered_report_only")
    blocked_count = sum(
        1
        for row in core_rows
        if _string(row.get("coverage_status")) in {"blocked_private_evidence", "blocked_external_boundary"}
    )
    not_classified_count = sum(
        1 for row in core_rows if _string(row.get("coverage_status")) in {"missing", "partial", "deferred"}
    )
    if parser_behavior_count == len(core_rows) and core_rows:
        status = "behavior_ready"
    elif not_classified_count:
        status = "not_classified"
    else:
        status = "classification_complete_not_behavior_ready"
    return {
        "schema_version": COMPETITIVE_CORE_SCHEMA_VERSION,
        "status": status,
        "total_families": len(core_rows),
        "parser_behavior_ready_family_count": parser_behavior_count,
        "report_only_family_count": report_only_count,
        "blocked_family_count": blocked_count,
    }


def _report_status(validation_errors: Sequence[str], summary: Mapping[str, int]) -> str:
    if validation_errors:
        if any("private" in error or "raw" in error for error in validation_errors):
            return STATUS_BLOCKED_PRIVATE
        if any("external" in error or "manasight" in error for error in validation_errors):
            return STATUS_BLOCKED_EXTERNAL
        return STATUS_FAIL
    if (
        summary.get("missing", 0)
        or summary.get("partial", 0)
        or summary.get("deferred", 0)
        or summary.get("blocked_private_evidence", 0)
        or summary.get("blocked_external_boundary", 0)
    ):
        return STATUS_PARTIAL_COVERAGE_MAP_READY
    return STATUS_COVERAGE_MAP_READY


def _status_reasons(validation_errors: Sequence[str], summary: Mapping[str, int]) -> list[str]:
    if validation_errors:
        return sorted(dict.fromkeys(str(error) for error in validation_errors))
    reasons: list[str] = []
    for key in ("missing", "partial", "deferred", "blocked_private_evidence", "blocked_external_boundary"):
        value = summary.get(key, 0)
        if value:
            reasons.append(f"{key}:{value}")
    return reasons


def _privacy_section(manifest: Mapping[str, Any], session_ledger: Mapping[str, Any] | None) -> dict[str, Any]:
    source_privacy = manifest.get("source_privacy") if isinstance(manifest.get("source_privacy"), Mapping) else {}
    findings = _forbidden_content_errors(manifest)
    if session_ledger is not None:
        findings.extend(_forbidden_content_errors(session_ledger))
    return {
        "raw_private_log_committed": source_privacy.get("raw_private_log_committed") is True,
        "external_logs_committed": source_privacy.get("external_logs_committed") is True,
        "raw_log_lines_in_report": False,
        "local_absolute_paths_redacted": True,
        "forbidden_content_findings": sorted(dict.fromkeys(findings)),
    }


def _protected_surfaces_section() -> dict[str, bool]:
    return {
        "parser_behavior_changed": False,
        "parser_state_final_reconciliation_changed": False,
        "parser_event_classes_changed": False,
        "match_game_identity_changed": False,
        "workbook_schema_changed": False,
        "webhook_payload_shape_changed": False,
        "apps_script_behavior_changed": False,
        "analytics_truth_changed": False,
        "ai_or_model_provider_behavior_changed": False,
    }


def _limitations_section(*, session_ledger_path: Path | None) -> list[str]:
    limitations = [
        "Category coverage is metadata-only and does not prove parser correctness.",
        "External corpus material is used only as category reference, not as imported fixture data.",
        "Missing categories require future scoped issues before fixture expansion.",
        "Reports do not decide merge readiness, deploy readiness, tracker completion, gameplay advice, "
        "analytics truth, AI truth, coaching truth, or production behavior.",
    ]
    if session_ledger_path is None:
        limitations.append("No session ledger input was supplied.")
    return limitations


def _external_reference_input(external_reference: Mapping[str, Any] | None) -> dict[str, str]:
    if external_reference is None:
        return {
            "source": "",
            "source_url": "",
            "usage": "not_supplied",
        }
    return {
        "source": _string(external_reference.get("source")),
        "source_url": _string(external_reference.get("source_url")),
        "usage": "category_reference_only",
    }


def _family_coverage_status(entries: Sequence[Mapping[str, Any]]) -> str:
    if not entries:
        return "missing"
    statuses = {_string(entry.get("coverage_status")) for entry in entries}
    for status in COVERAGE_STATUS_PRECEDENCE:
        if status in statuses:
            return status
    return "missing"


def _family_coverage_basis(entries: Sequence[Mapping[str, Any]], status: str) -> list[str]:
    basis: set[str] = set()
    for entry in entries:
        basis.update(_string_list(entry.get("coverage_basis")))
    if not basis:
        if status == "missing":
            basis.add("external_reference_only")
        elif status == "covered_committed":
            basis.add("fixture_metadata_only")
        elif status == "covered_synthetic":
            basis.add("fixture_metadata_only")
        elif status == "covered_report_only":
            basis.add("local_report_only")
    return sorted(basis)


def _family_notes(entries: Sequence[Mapping[str, Any]]) -> list[str]:
    notes: list[str] = []
    for entry in entries:
        notes.extend(_string_list(entry.get("review_notes")))
    return sorted(dict.fromkeys(notes))


def _manifest_entries(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    entries = payload.get("entries")
    return [entry for entry in entries if isinstance(entry, Mapping)] if isinstance(entries, list) else []


def _taxonomy_family_ids(payload: Mapping[str, Any]) -> list[str]:
    taxonomy = payload.get("taxonomy") if isinstance(payload.get("taxonomy"), Mapping) else {}
    families = taxonomy.get("families") if isinstance(taxonomy, Mapping) else []
    ids: list[str] = []
    if isinstance(families, list):
        for family in families:
            if isinstance(family, str):
                ids.append(family)
            elif isinstance(family, Mapping):
                family_id = _string(family.get("family_id") or family.get("id") or family.get("scenario_family"))
                if family_id:
                    ids.append(family_id)
    return ids


def _require_value(
    errors: list[str],
    payload: Mapping[str, Any],
    field: str,
    allowed_values: set[str],
    object_id: str,
) -> str:
    value = _string(payload.get(field))
    if not value:
        errors.append(f"missing_{field}:{object_id}")
    elif value not in allowed_values:
        errors.append(f"invalid_{field}:{object_id}:{value}")
    return value


def _path_errors(paths: object, entry_id: str) -> list[str]:
    if paths is None:
        return []
    errors: list[str] = []
    if not isinstance(paths, Mapping):
        return [f"entry_paths_not_object:{entry_id}"]
    for key, raw_value in paths.items():
        value = _string(raw_value)
        if not value:
            continue
        normalized = value.replace("\\", "/").lower()
        if Path(value).is_absolute() or normalized.startswith("../") or "/../" in normalized:
            errors.append(f"unsafe_path:{entry_id}:{key}")
        if any(normalized.endswith(suffix) for suffix in FORBIDDEN_PATH_SUFFIXES) and key != "golden_replay_manifest":
            errors.append(f"forbidden_artifact_path:{entry_id}:{key}")
        if "manasight" in normalized and any(normalized.endswith(suffix) for suffix in FORBIDDEN_PATH_SUFFIXES):
            errors.append(f"external_artifact_path:{entry_id}:{key}")
    return errors


def _forbidden_content_errors(value: object) -> list[str]:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    errors: list[str] = []
    for label, pattern in FORBIDDEN_REPORT_PATTERNS:
        if pattern.search(encoded):
            errors.append(f"forbidden_content:{label}")
    return errors


def _load_optional_json_object(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    return _load_json_object(path)


def _load_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"object": "", "schema_version": "", "_load_error": "invalid_json"}
    if not isinstance(payload, dict):
        return {"object": "", "schema_version": "", "_load_error": "json_root_not_object"}
    return payload


def _safe_repo_path(path: Path | None) -> str:
    if path is None:
        return ""
    candidate = Path(path)
    repo_root = Path.cwd()
    try:
        return candidate.resolve().relative_to(repo_root.resolve()).as_posix()
    except (OSError, ValueError):
        value = candidate.as_posix()
        if value.startswith("./"):
            return value[2:]
        if not candidate.is_absolute():
            return value
        return "<outside_repo>"


def _sanitize_report_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _sanitize_report_value(nested) for key, nested in value.items()}
    if isinstance(value, list):
        return [_sanitize_report_value(item) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_report_value(item) for item in value]
    if isinstance(value, str):
        text = sanitize_sensitive_text(value)
        text = LOCAL_ABSOLUTE_PATH_PATTERN.sub("<redacted-local-path>", text)
        return SECRET_ASSIGNMENT_PATTERN.sub("<redacted-secret>", text)
    return value


def _string(value: object) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
