from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .. import events as event_models
from ..log.entry import LineBuffer
from ..router import Router
from . import evidence_validation_report_wiring, golden_replay, state
from .config import PROJECT_ROOT
from .diagnostics import sanitize_sensitive_text

FEATURE_EQUITY_CORPUS_REPORT_OBJECT = "mythic_edge_feature_equity_corpus_ratchet_report"
FEATURE_EQUITY_CORPUS_REPORT_SCHEMA_VERSION = "parser_feature_equity_corpus_ratchet_report.v1"
FEATURE_EQUITY_CORPUS_BASELINE_OBJECT = "mythic_edge_feature_equity_corpus_ratchet_baseline"
FEATURE_EQUITY_CORPUS_BASELINE_SCHEMA_VERSION = "parser_feature_equity_corpus_ratchet_baseline.v1"

BASELINE_ID = "parser_reliability_feature_equity_corpus_v1"
LINKED_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/119"

STATUS_OK = "ok"
STATUS_REVIEW = "review"
STATUS_DIFF = "diff"
STATUS_FAIL = "fail"

APPROVED_SOURCE_PRIVACY_CLASSES = {"sanitized_committable", "synthetic_committable"}
RATCHET_PRIVACY_CLASS = "committed_count_only"

COUNT_SECTIONS = (
    "input_counts",
    "router_stats",
    "event_family_counts",
    "event_kind_counts",
    "payload_type_counts",
    "parser_claim_counts",
    "game_state_evidence_counts",
    "truncation_and_data_loss",
    "unknowns_and_degradation",
)

EXACT_MATCH_SECTIONS = list(COUNT_SECTIONS)


def build_feature_equity_corpus_report(
    manifest_paths: Sequence[Path],
    *,
    baseline_path: Path | None = None,
    evidence_ledger_review: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    expanded_manifest_paths, expanded_from_directories = _expand_manifest_paths(manifest_paths)
    manifest_records = [_manifest_record(path) for path in expanded_manifest_paths]
    observed = _empty_observed()
    observed["input_counts"] = _input_counts(manifest_records)
    source_file_paths = _source_file_paths(manifest_records)
    privacy = _privacy_section(manifest_records)
    status_reasons: list[str] = []
    fail_reasons: list[str] = []
    review_reasons: list[str] = []
    replay_diff_seen = False

    for record in manifest_records:
        fail_reasons.extend(record.validation_failures)
        if record.fixture_path is not None:
            source_file_paths.add(record.fixture_path)
        if record.replay_result.status == golden_replay.STATUS_FAIL:
            fail_reasons.append(_status_reason("golden_replay_fail", record))
            continue
        if record.replay_result.status == golden_replay.STATUS_DIFF:
            replay_diff_seen = True
            status_reasons.append(_status_reason("golden_replay_diff", record))
        elif record.replay_result.status in {golden_replay.STATUS_REVIEW, golden_replay.STATUS_DEGRADED}:
            review_reasons.append(_status_reason(f"golden_replay_{record.replay_result.status}", record))

        if record.fixture_path is not None:
            fixture_observed = _collect_fixture_observed_counts(record.fixture_path)
            _merge_observed_counts(observed, fixture_observed)

    observed["input_counts"]["source_files_total"] = len(source_file_paths)

    baseline_payload, baseline_section = _load_baseline_section(baseline_path)
    comparison = _comparison_section(
        observed=observed,
        manifest_paths=[_safe_repo_path(path) for path in expanded_manifest_paths],
        baseline_payload=baseline_payload,
    )
    review_reasons.extend(_review_signal_reasons(observed, baseline_payload, comparison))
    if not baseline_section["loaded"] and baseline_path is None:
        review_reasons.append("baseline_missing")
    if baseline_section["validation_errors"]:
        fail_reasons.extend(f"baseline:{error}" for error in baseline_section["validation_errors"])
    if comparison["diff_sections"]:
        replay_diff_seen = True

    status_reasons = _unique_status_reasons(
        [*status_reasons, *fail_reasons, *review_reasons, *comparison["diff_sections"]]
    )
    status = _report_status(
        fail_reasons=fail_reasons,
        diff_seen=replay_diff_seen,
        review_reasons=review_reasons,
    )

    inputs = {
        "manifest_paths": [_safe_repo_path(path) for path in expanded_manifest_paths],
        "manifest_count": len(expanded_manifest_paths),
        "source_file_count": len(source_file_paths),
        "source_file_paths": sorted(_safe_repo_path(path) for path in source_file_paths),
        "input_kind": "golden_replay_manifest",
        "expanded_from_directories": expanded_from_directories,
        "ordering": "sorted_repo_relative_path",
    }

    return _sanitize_report_value(
        {
            "object": FEATURE_EQUITY_CORPUS_REPORT_OBJECT,
            "schema_version": FEATURE_EQUITY_CORPUS_REPORT_SCHEMA_VERSION,
            "status": status,
            "status_reasons": status_reasons,
            "generated_at_utc": _utc_timestamp(),
            "inputs": inputs,
            "baseline": baseline_section,
            "observed": _sorted_value(observed),
            "comparison": _sorted_value(comparison),
            "privacy": _sorted_value(privacy),
            "protected_surfaces": _protected_surfaces_section(),
            "limitations": _limitations_section(),
            "evidence_ledger_review": evidence_validation_report_wiring.evidence_review_section_from_inputs(
                evidence_ledger_review,
                report_context="feature_equity_corpus_ratchet",
            ),
        }
    )


def write_feature_equity_corpus_report(
    manifest_paths: Sequence[Path],
    *,
    baseline_path: Path | None = None,
    report_path: Path | None = None,
    evidence_ledger_review: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    report = build_feature_equity_corpus_report(
        manifest_paths,
        baseline_path=baseline_path,
        evidence_ledger_review=evidence_ledger_review,
    )
    if report_path is not None:
        output_path = Path(report_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = write_feature_equity_corpus_report(
        [Path(path) for path in args.manifests],
        baseline_path=Path(args.baseline_path) if args.baseline_path else None,
        report_path=Path(args.report_path) if args.report_path else None,
        evidence_ledger_review=evidence_validation_report_wiring.evidence_review_inputs_from_args(args),
    )
    summary = report["inputs"]
    print(
        "Feature-equity corpus ratchet: "
        f"{report['status']} "
        f"({summary['manifest_count']} manifests, {summary['source_file_count']} source files)"
    )
    if args.report_path:
        print(f"Report written: {_safe_repo_path(Path(args.report_path))}")
    return 1 if report["status"] == STATUS_FAIL else 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a report-only parser feature-equity corpus ratchet report."
    )
    parser.add_argument(
        "manifests",
        nargs="+",
        help="Golden replay manifest file paths, or directories containing *.manifest.json files.",
    )
    parser.add_argument("--baseline", dest="baseline_path", default="", help="Optional count-only baseline JSON.")
    parser.add_argument("--out", dest="report_path", default="", help="Optional local JSON report output path.")
    evidence_validation_report_wiring.evidence_review_cli_arguments(parser)
    return parser


class _ManifestRecord:
    def __init__(
        self,
        *,
        path: Path,
        payload: dict[str, Any],
        fixture_path: Path | None,
        replay_result: golden_replay.GoldenReplayFixtureResult,
        validation_failures: list[str],
    ) -> None:
        self.path = path
        self.payload = payload
        self.fixture_path = fixture_path
        self.replay_result = replay_result
        self.validation_failures = validation_failures


def _manifest_record(path: Path) -> _ManifestRecord:
    payload = _load_json_object(path)
    source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
    fixture_path = golden_replay._resolve_fixture_path(source.get("log_path")) if source else None
    replay_result = golden_replay.run_golden_replay(path)
    validation_failures = _ratchet_manifest_validation_failures(payload)
    validation_failures.extend(
        failure for failure in replay_result.failures if str(failure).startswith("forbidden_")
    )
    return _ManifestRecord(
        path=path,
        payload=payload,
        fixture_path=fixture_path,
        replay_result=replay_result,
        validation_failures=validation_failures,
    )


def _ratchet_manifest_validation_failures(payload: dict[str, Any]) -> list[str]:
    source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
    failures: list[str] = []
    if not source:
        return failures
    if source.get("raw_private_log_committed") is True:
        failures.append("raw_private_log_committed")
    privacy_class = str(source.get("source_privacy_class") or "").strip()
    if privacy_class and privacy_class not in APPROVED_SOURCE_PRIVACY_CLASSES:
        failures.append(f"unapproved_source_privacy_class:{privacy_class}")
    return failures


def _collect_fixture_observed_counts(fixture_path: Path) -> dict[str, Any]:
    state.reset_runtime_state()
    router = Router()
    event_family_counts: Counter[str] = Counter({kind: 0 for kind in _event_kind_universe()})
    event_kind_counts: Counter[str] = Counter({kind: 0 for kind in _event_kind_universe()})
    payload_type_counts: Counter[str] = Counter()
    parser_claim_counts: Counter[str] = Counter(_empty_parser_claim_counts())
    game_state_evidence_counts = _empty_game_state_evidence_counts()
    try:
        buffer = LineBuffer()
        with fixture_path.open("r", encoding="utf-8", errors="replace") as handle:
            for raw_line in handle:
                if raw_line.startswith("#"):
                    continue
                _collect_entries(
                    buffer.feed(raw_line),
                    router=router,
                    event_family_counts=event_family_counts,
                    event_kind_counts=event_kind_counts,
                    payload_type_counts=payload_type_counts,
                    parser_claim_counts=parser_claim_counts,
                    game_state_evidence_counts=game_state_evidence_counts,
                )
        _collect_entries(
            buffer.flush(),
            router=router,
            event_family_counts=event_family_counts,
            event_kind_counts=event_kind_counts,
            payload_type_counts=payload_type_counts,
            parser_claim_counts=parser_claim_counts,
            game_state_evidence_counts=game_state_evidence_counts,
        )
        stats = router.stats
        return {
            "router_stats": {
                "routed": stats.routed,
                "unknown": stats.unknown,
                "timestamp_missing": stats.timestamp_missing,
                "timestamp_parse_failure": stats.timestamp_parse_failure,
            },
            "event_family_counts": dict(sorted(event_family_counts.items())),
            "event_kind_counts": dict(sorted(event_kind_counts.items())),
            "payload_type_counts": dict(sorted(payload_type_counts.items())),
            "parser_claim_counts": dict(sorted(parser_claim_counts.items())),
            "game_state_evidence_counts": _sorted_value(game_state_evidence_counts),
            "truncation_and_data_loss": {
                "truncation_events": event_family_counts.get("Truncation", 0),
                "fixtures_with_truncation": int(event_family_counts.get("Truncation", 0) > 0),
                "data_loss_markers": game_state_evidence_counts["diff_source_field_counts"].get(
                    "truncation_or_data_loss_evidence",
                    0,
                ),
                "fixtures_with_data_loss": int(
                    event_family_counts.get("Truncation", 0) > 0
                    or game_state_evidence_counts["diff_source_field_counts"].get(
                        "truncation_or_data_loss_evidence",
                        0,
                    )
                    > 0
                ),
                "data_loss_field_counts": {},
            },
            "unknowns_and_degradation": {
                "unknown_entries": stats.unknown,
                "timestamp_missing": stats.timestamp_missing,
                "timestamp_parse_failure": stats.timestamp_parse_failure,
                "degraded_parser_outputs": game_state_evidence_counts["diff_degraded_records"],
                "review_required_outputs": game_state_evidence_counts["diff_review_required"],
                "malformed_records": 0,
                "unsupported_records": 0,
            },
        }
    finally:
        state.reset_runtime_state()


def _collect_entries(
    entries: Sequence[Any],
    *,
    router: Router,
    event_family_counts: Counter[str],
    event_kind_counts: Counter[str],
    payload_type_counts: Counter[str],
    parser_claim_counts: Counter[str],
    game_state_evidence_counts: dict[str, Any],
) -> None:
    for entry in entries:
        for event in router.route(entry):
            kind = str(getattr(event, "kind", type(event).__name__) or "").strip()
            if not kind:
                continue
            payload = getattr(event, "payload", {}) if isinstance(getattr(event, "payload", {}), dict) else {}
            payload_type = str(payload.get("type") or "").strip() or "<missing>"
            event_family_counts[kind] += 1
            event_kind_counts[kind] += 1
            payload_type_counts[f"{kind}:{payload_type}"] += 1
            _count_parser_claim(kind, payload, parser_claim_counts)
            if kind == "GameState":
                _count_game_state_evidence(payload, game_state_evidence_counts)


def _count_parser_claim(kind: str, payload: Mapping[str, Any], parser_claim_counts: Counter[str]) -> None:
    if kind == "MatchState":
        parser_claim_counts["match_lifecycle_claims"] += 1
        if payload.get("type") == "match_completed":
            parser_claim_counts["final_reconciliation_claims"] += 1
    elif kind == "GameResult":
        parser_claim_counts["game_result_claims"] += 1
        parser_claim_counts["final_reconciliation_claims"] += 1
    elif kind == "ClientAction":
        parser_claim_counts["client_action_claims"] += 1
    elif kind == "Rank":
        parser_claim_counts["rank_context_claims"] += 1
    elif kind == "GameState":
        parser_claim_counts["game_state_claims"] += 1
        observations = payload.get("opponent_card_observations")
        if isinstance(observations, Mapping):
            parser_claim_counts["opponent_observation_claims"] += _safe_int(observations.get("total_observations"))


def _count_game_state_evidence(payload: Mapping[str, Any], counts: dict[str, Any]) -> None:
    payload_type = str(payload.get("type") or "").strip()
    counts["game_state_events"] += 1
    if payload_type == "connect_resp":
        counts["connect_resp_events"] += 1
    elif payload_type == "queued_game_state_message":
        counts["queued_game_state_messages"] += 1
    elif payload_type == "game_state_message":
        counts["game_state_message_events"] += 1

    annotations = payload.get("normalized_annotations")
    if isinstance(annotations, Mapping):
        counts["annotations_total_records"] += _safe_int(annotations.get("total_records"))
        counts["annotations_degraded_records"] += _safe_int(annotations.get("degraded_records"))
        counts["annotations_review_required"] += int(bool(annotations.get("review_required")))
        _update_label_counts(counts["annotation_type_counts"], annotations.get("annotation_types"))
        _update_label_counts(counts["annotation_marker_type_counts"], annotations.get("marker_types"))

    timers = payload.get("normalized_timers")
    if isinstance(timers, Mapping):
        counts["timers_total_records"] += _safe_int(timers.get("total_records"))
        counts["timers_degraded_records"] += _safe_int(timers.get("degraded_records"))
        counts["timers_review_required"] += int(bool(timers.get("review_required")))
        _update_label_counts(counts["timer_type_counts"], timers.get("timer_types"))
        time_units = timers.get("time_units_seen")
        if isinstance(time_units, Mapping):
            for key, value in time_units.items():
                timer_time_unit_counts = counts["timer_time_unit_counts"]
                timer_time_unit_counts[str(key)] = timer_time_unit_counts.get(str(key), 0) + _safe_int(value)

    mechanics = payload.get("game_state_diff_mechanics")
    if isinstance(mechanics, Mapping):
        update_kind = str(mechanics.get("update_kind") or "")
        if bool(mechanics.get("is_complete_snapshot")):
            counts["diff_complete_snapshots"] += 1
        if update_kind == "diff":
            counts["diff_incremental_updates"] += 1
        if bool(mechanics.get("queued")):
            counts["diff_queued_messages"] += 1
        prev_status = str(mechanics.get("prev_game_state_id_status") or "")
        if prev_status == "linked":
            counts["diff_previous_state_linked"] += 1
        elif prev_status and prev_status != "not_applicable":
            counts["diff_previous_state_missing"] += 1
        if bool(mechanics.get("deletion_evidence_present")):
            counts["diff_deletion_evidence_present"] += 1
        counts["diff_deleted_instance_ids"] += len(mechanics.get("diff_deleted_instance_ids") or [])
        counts["diff_deleted_annotation_ids"] += len(mechanics.get("diff_deleted_persistent_annotation_ids") or [])
        if mechanics.get("degradation_flags"):
            counts["diff_degraded_records"] += 1
        if bool(mechanics.get("review_required")):
            counts["diff_review_required"] += 1
        _increment_count(counts["diff_evidence_status_counts"], mechanics.get("evidence_status"))
        _increment_count(counts["diff_value_source_counts"], mechanics.get("value_source"))
        _increment_count(counts["diff_confidence_counts"], mechanics.get("confidence"))
        source_fields = mechanics.get("source_fields_used")
        if isinstance(source_fields, Mapping):
            for key, value in source_fields.items():
                if bool(value):
                    source_field_counts = counts["diff_source_field_counts"]
                    source_field_counts[str(key)] = source_field_counts.get(str(key), 0) + 1


def _merge_observed_counts(target: dict[str, Any], source: dict[str, Any]) -> None:
    for section in COUNT_SECTIONS:
        if section == "input_counts":
            continue
        _merge_mapping_counts(target[section], source.get(section, {}))


def _merge_mapping_counts(target: dict[str, Any], source: Mapping[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, Mapping):
            nested = target.setdefault(str(key), {})
            if isinstance(nested, dict):
                _merge_mapping_counts(nested, value)
        else:
            target[str(key)] = _safe_int(target.get(str(key))) + _safe_int(value)


def _input_counts(records: Sequence[_ManifestRecord]) -> dict[str, int]:
    sanitized = 0
    synthetic = 0
    private_rejected = 0
    for record in records:
        source = record.payload.get("source") if isinstance(record.payload.get("source"), dict) else {}
        privacy_class = str(source.get("source_privacy_class") or "").strip()
        if privacy_class == "sanitized_committable":
            sanitized += 1
        if privacy_class == "synthetic_committable":
            synthetic += 1
        if source.get("raw_private_log_committed") is True or (
            privacy_class and privacy_class not in APPROVED_SOURCE_PRIVACY_CLASSES
        ):
            private_rejected += 1
    return {
        "manifests_total": len(records),
        "source_files_total": 0,
        "fixtures_total": len(records),
        "fixtures_sanitized_committable": sanitized,
        "fixtures_synthetic_committable": synthetic,
        "fixtures_private_rejected": private_rejected,
    }


def _empty_observed() -> dict[str, Any]:
    return {
        "input_counts": {
            "manifests_total": 0,
            "source_files_total": 0,
            "fixtures_total": 0,
            "fixtures_sanitized_committable": 0,
            "fixtures_synthetic_committable": 0,
            "fixtures_private_rejected": 0,
        },
        "router_stats": {
            "routed": 0,
            "unknown": 0,
            "timestamp_missing": 0,
            "timestamp_parse_failure": 0,
        },
        "event_family_counts": {kind: 0 for kind in _event_kind_universe()},
        "event_kind_counts": {kind: 0 for kind in _event_kind_universe()},
        "payload_type_counts": {},
        "parser_claim_counts": _empty_parser_claim_counts(),
        "game_state_evidence_counts": _empty_game_state_evidence_counts(),
        "truncation_and_data_loss": {
            "truncation_events": 0,
            "fixtures_with_truncation": 0,
            "data_loss_markers": 0,
            "fixtures_with_data_loss": 0,
            "data_loss_field_counts": {},
        },
        "unknowns_and_degradation": {
            "unknown_entries": 0,
            "timestamp_missing": 0,
            "timestamp_parse_failure": 0,
            "degraded_parser_outputs": 0,
            "review_required_outputs": 0,
            "malformed_records": 0,
            "unsupported_records": 0,
        },
    }


def _empty_parser_claim_counts() -> dict[str, int]:
    return {
        "match_lifecycle_claims": 0,
        "game_result_claims": 0,
        "client_action_claims": 0,
        "rank_context_claims": 0,
        "opponent_observation_claims": 0,
        "game_state_claims": 0,
        "final_reconciliation_claims": 0,
    }


def _empty_game_state_evidence_counts() -> dict[str, Any]:
    return {
        "game_state_events": 0,
        "connect_resp_events": 0,
        "game_state_message_events": 0,
        "queued_game_state_messages": 0,
        "annotations_total_records": 0,
        "annotations_degraded_records": 0,
        "annotations_review_required": 0,
        "annotation_type_counts": {},
        "annotation_marker_type_counts": {},
        "timers_total_records": 0,
        "timers_degraded_records": 0,
        "timers_review_required": 0,
        "timer_type_counts": {},
        "timer_time_unit_counts": {},
        "diff_complete_snapshots": 0,
        "diff_incremental_updates": 0,
        "diff_queued_messages": 0,
        "diff_previous_state_linked": 0,
        "diff_previous_state_missing": 0,
        "diff_deletion_evidence_present": 0,
        "diff_deleted_instance_ids": 0,
        "diff_deleted_annotation_ids": 0,
        "diff_degraded_records": 0,
        "diff_review_required": 0,
        "diff_evidence_status_counts": {},
        "diff_value_source_counts": {},
        "diff_confidence_counts": {},
        "diff_source_field_counts": {},
    }


def _comparison_section(
    *,
    observed: dict[str, Any],
    manifest_paths: list[str],
    baseline_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    comparison: dict[str, Any] = {
        "baseline_present": baseline_payload is not None,
        "sections_compared": [],
        "matching_sections": [],
        "diff_sections": [],
        "review_sections": [],
        "missing_expected_sections": [],
        "unexpected_observed_sections": [],
        "count_diffs": [],
    }
    if baseline_payload is None:
        return comparison

    expected = baseline_payload.get("expected") if isinstance(baseline_payload.get("expected"), dict) else {}
    raw_policy = baseline_payload.get("tolerance_policy")
    policy = raw_policy if isinstance(raw_policy, dict) else {}
    exact_sections = _string_list(policy.get("exact_match_sections")) or list(EXACT_MATCH_SECTIONS)
    minimum_sections = _string_list(policy.get("minimum_sections"))

    baseline_manifest_paths = _string_list(baseline_payload.get("source_manifest_paths"))
    if baseline_manifest_paths != manifest_paths:
        comparison["diff_sections"].append("source_manifest_paths")
        comparison["count_diffs"].append(
            {
                "section": "inputs",
                "key": "source_manifest_paths",
                "expected": baseline_manifest_paths,
                "observed": manifest_paths,
                "delta": len(manifest_paths) - len(baseline_manifest_paths),
                "policy": "exact",
            }
        )

    for section in COUNT_SECTIONS:
        observed_section = observed.get(section)
        expected_section = expected.get(section)
        if expected_section is None:
            comparison["missing_expected_sections"].append(section)
            comparison["diff_sections"].append(section)
            continue
        comparison["sections_compared"].append(section)
        if section in minimum_sections:
            diffs = _minimum_diffs(section, expected_section, observed_section)
        elif section in exact_sections:
            diffs = _exact_diffs(section, expected_section, observed_section)
        else:
            diffs = _exact_diffs(section, expected_section, observed_section)
        if diffs:
            comparison["diff_sections"].append(section)
            comparison["count_diffs"].extend(diffs)
        else:
            comparison["matching_sections"].append(section)

    for section in observed:
        if section not in expected and section not in comparison["unexpected_observed_sections"]:
            comparison["unexpected_observed_sections"].append(section)
    return _dedupe_comparison(comparison)


def _load_baseline_section(path: Path | None) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    section = {
        "path": _safe_repo_path(path) if path is not None else "",
        "present": False,
        "object": "",
        "schema_version": "",
        "baseline_id": "",
        "loaded": False,
        "validation_errors": [],
    }
    if path is None:
        return None, section
    baseline_path = Path(path)
    section["present"] = baseline_path.is_file()
    if not section["present"]:
        section["validation_errors"].append("baseline_unreadable")
        return None, section

    payload = _load_json_object(baseline_path)
    section["object"] = str(payload.get("object") or "")
    section["schema_version"] = str(payload.get("schema_version") or "")
    section["baseline_id"] = str(payload.get("baseline_id") or "")
    validation_errors = _baseline_validation_errors(payload)
    section["validation_errors"] = validation_errors
    section["loaded"] = not validation_errors
    return (payload if section["loaded"] else None), section


def _baseline_validation_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("object") != FEATURE_EQUITY_CORPUS_BASELINE_OBJECT:
        errors.append("invalid_baseline_object")
    if payload.get("schema_version") != FEATURE_EQUITY_CORPUS_BASELINE_SCHEMA_VERSION:
        errors.append("invalid_baseline_schema_version")
    if not str(payload.get("baseline_id") or "").strip():
        errors.append("missing_baseline_id")
    if payload.get("linked_issue") != LINKED_ISSUE:
        errors.append("invalid_linked_issue")
    if not isinstance(payload.get("source_manifest_paths"), list):
        errors.append("invalid_source_manifest_paths")
    source_privacy = payload.get("source_privacy")
    if not isinstance(source_privacy, dict):
        errors.append("invalid_source_privacy")
    else:
        if source_privacy.get("privacy_class") != RATCHET_PRIVACY_CLASS:
            errors.append("invalid_source_privacy_class")
        if source_privacy.get("raw_private_log_committed") is not False:
            errors.append("baseline_raw_private_log_committed_must_be_false")
    expected = payload.get("expected")
    if not isinstance(expected, dict):
        errors.append("invalid_expected")
    else:
        for section in COUNT_SECTIONS:
            if not isinstance(expected.get(section), dict):
                errors.append(f"invalid_expected_section:{section}")
    policy = payload.get("tolerance_policy")
    if not isinstance(policy, dict):
        errors.append("invalid_tolerance_policy")
    return errors


def _review_signal_reasons(
    observed: dict[str, Any],
    baseline_payload: dict[str, Any] | None,
    comparison: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    baseline_expected = baseline_payload.get("expected", {}) if isinstance(baseline_payload, dict) else {}
    if "unknowns_and_degradation" not in comparison.get("diff_sections", []):
        unknowns = observed["unknowns_and_degradation"]
        expected_unknowns = baseline_expected.get("unknowns_and_degradation", {})
        for key in (
            "unknown_entries",
            "timestamp_missing",
            "timestamp_parse_failure",
            "degraded_parser_outputs",
            "review_required_outputs",
            "malformed_records",
            "unsupported_records",
        ):
            value = _safe_int(unknowns.get(key))
            if value > 0 and _safe_int(expected_unknowns.get(key)) != value:
                reasons.append(f"review_signal:{key}")
    if "truncation_and_data_loss" not in comparison.get("diff_sections", []):
        data_loss = observed["truncation_and_data_loss"]
        expected_data_loss = baseline_expected.get("truncation_and_data_loss", {})
        for key in ("truncation_events", "fixtures_with_truncation", "data_loss_markers", "fixtures_with_data_loss"):
            value = _safe_int(data_loss.get(key))
            if value > 0 and _safe_int(expected_data_loss.get(key)) != value:
                reasons.append(f"review_signal:{key}")
    return reasons


def _exact_diffs(section: str, expected: Any, observed: Any) -> list[dict[str, Any]]:
    diffs: list[dict[str, Any]] = []
    for key, expected_value, observed_value in _flatten_comparable_values(expected, observed):
        if expected_value != observed_value:
            diffs.append(
                {
                    "section": section,
                    "key": key,
                    "expected": expected_value,
                    "observed": observed_value,
                    "delta": _numeric_delta(expected_value, observed_value),
                    "policy": "exact",
                }
            )
    return diffs


def _minimum_diffs(section: str, expected: Any, observed: Any) -> list[dict[str, Any]]:
    diffs: list[dict[str, Any]] = []
    for key, expected_value, observed_value in _flatten_comparable_values(expected, observed):
        if _safe_int(observed_value) < _safe_int(expected_value):
            diffs.append(
                {
                    "section": section,
                    "key": key,
                    "expected": expected_value,
                    "observed": observed_value,
                    "delta": _safe_int(observed_value) - _safe_int(expected_value),
                    "policy": "minimum",
                }
            )
    return diffs


def _flatten_comparable_values(expected: Any, observed: Any, prefix: str = "") -> list[tuple[str, Any, Any]]:
    if isinstance(expected, Mapping) or isinstance(observed, Mapping):
        expected_map = expected if isinstance(expected, Mapping) else {}
        observed_map = observed if isinstance(observed, Mapping) else {}
        keys = sorted({str(key) for key in expected_map} | {str(key) for key in observed_map})
        values: list[tuple[str, Any, Any]] = []
        for key in keys:
            child_prefix = f"{prefix}.{key}" if prefix else key
            values.extend(_flatten_comparable_values(expected_map.get(key), observed_map.get(key), child_prefix))
        return values
    return [(prefix, expected, observed)]


def _numeric_delta(expected: Any, observed: Any) -> int | str:
    if isinstance(expected, bool) or isinstance(observed, bool):
        return ""
    if isinstance(expected, int | float) and isinstance(observed, int | float):
        return int(observed - expected)
    return ""


def _privacy_section(records: Sequence[_ManifestRecord]) -> dict[str, Any]:
    forbidden_findings: list[str] = []
    raw_private_log_committed = False
    for record in records:
        source = record.payload.get("source") if isinstance(record.payload.get("source"), dict) else {}
        raw_private_log_committed = raw_private_log_committed or source.get("raw_private_log_committed") is True
        forbidden_findings.extend(
            str(failure) for failure in record.replay_result.failures if str(failure).startswith("forbidden_")
        )
    return {
        "privacy_class": RATCHET_PRIVACY_CLASS,
        "raw_private_log_committed": raw_private_log_committed,
        "raw_log_lines_in_report": False,
        "forbidden_content_findings": sorted(dict.fromkeys(forbidden_findings)),
        "local_absolute_paths_redacted": True,
    }


def _protected_surfaces_section() -> dict[str, bool]:
    return {
        "parser_behavior_changed": False,
        "parser_state_final_reconciliation_changed": False,
        "parser_event_classes_changed": False,
        "match_or_game_identity_changed": False,
        "deduplication_changed": False,
        "workbook_schema_changed": False,
        "webhook_payload_shape_changed": False,
        "apps_script_behavior_changed": False,
        "ci_gate_changed": False,
        "production_behavior_changed": False,
    }


def _limitations_section() -> list[str]:
    return [
        "The ratchet measures corpus coverage shape, not semantic parser correctness.",
        "The ratchet does not inspect live workbook state.",
        "The ratchet does not inspect deployed Apps Script state.",
        "The ratchet does not authorize baseline updates.",
        "The ratchet does not decide merge readiness.",
        "The ratchet does not implement the full Player.log evidence ledger.",
        "The ratchet does not evaluate coaching quality or AI analytics.",
    ]


def _expand_manifest_paths(paths: Sequence[Path]) -> tuple[list[Path], list[str]]:
    manifests: list[Path] = []
    directories: list[str] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            directories.append(_safe_repo_path(path))
            manifests.extend(path.glob("*.manifest.json"))
        else:
            manifests.append(path)
    unique = {str(path.resolve(strict=False)): path for path in manifests}
    sorted_paths = sorted(unique.values(), key=_safe_repo_path)
    return sorted_paths, sorted(dict.fromkeys(directories))


def _source_file_paths(records: Sequence[_ManifestRecord]) -> set[Path]:
    return {record.fixture_path for record in records if record.fixture_path is not None}


def _load_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _event_kind_universe() -> list[str]:
    kinds: list[str] = []
    for value in vars(event_models).values():
        if not isinstance(value, type):
            continue
        try:
            if value is event_models.BaseEvent or not issubclass(value, event_models.BaseEvent):
                continue
        except TypeError:
            continue
        kind = str(getattr(value, "kind", "") or "").strip()
        if kind:
            kinds.append(kind)
    return sorted(dict.fromkeys(kinds))


def _update_label_counts(counter: dict[str, int], values: Any) -> None:
    if not isinstance(values, list):
        return
    for value in values:
        label = str(value or "").strip()
        if label:
            counter[label] = counter.get(label, 0) + 1


def _increment_count(counter: dict[str, int], value: Any) -> None:
    label = str(value or "").strip()
    if label:
        counter[label] = counter.get(label, 0) + 1


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _safe_int(value: Any) -> int:
    try:
        if isinstance(value, bool):
            return int(value)
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _report_status(*, fail_reasons: list[str], diff_seen: bool, review_reasons: list[str]) -> str:
    if fail_reasons:
        return STATUS_FAIL
    if diff_seen:
        return STATUS_DIFF
    if review_reasons:
        return STATUS_REVIEW
    return STATUS_OK


def _status_reason(prefix: str, record: _ManifestRecord) -> str:
    fixture_id = str(record.replay_result.fixture_id or "").strip()
    return f"{prefix}:{fixture_id or _safe_repo_path(record.path)}"


def _unique_status_reasons(reasons: Sequence[str]) -> list[str]:
    clean = [str(reason) for reason in reasons if str(reason)]
    return sorted(dict.fromkeys(clean))


def _dedupe_comparison(comparison: dict[str, Any]) -> dict[str, Any]:
    for key in (
        "sections_compared",
        "matching_sections",
        "diff_sections",
        "review_sections",
        "missing_expected_sections",
        "unexpected_observed_sections",
    ):
        comparison[key] = sorted(dict.fromkeys(comparison[key]))
    comparison["count_diffs"] = sorted(
        comparison["count_diffs"],
        key=lambda item: (str(item.get("section", "")), str(item.get("key", ""))),
    )
    return comparison


def _sorted_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _sorted_value(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_sorted_value(item) for item in value]
    if isinstance(value, tuple):
        return [_sorted_value(item) for item in value]
    return value


def _sanitize_report_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _sanitize_report_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_report_value(item) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_report_value(item) for item in value]
    if isinstance(value, Path):
        return _safe_repo_path(value)
    if isinstance(value, str):
        return sanitize_sensitive_text(value)
    return value


def _safe_repo_path(path: Path | None) -> str:
    if path is None:
        return ""
    target = Path(path)
    try:
        return str(target.resolve(strict=False).relative_to(PROJECT_ROOT.resolve(strict=False))).replace("\\", "/")
    except Exception:
        return target.name or "[redacted-path]"


def _utc_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
