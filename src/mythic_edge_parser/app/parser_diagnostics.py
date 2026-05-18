from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..router import Router
from . import log_drift_sensor
from .config import LOG_PATH, PROJECT_ROOT, STATUS_ROOT
from .diagnostics import sanitize_sensitive_text

OBJECT_KIND = "mythic_edge_parser_diagnostics_report"
SCHEMA_VERSION = "parser_diagnostics.v1"
DEFAULT_PROFILE = "live_game"
ALLOWED_PROFILES = {"fixture", "local_log", "live_game"}
DEFAULT_REPORT_PATH = STATUS_ROOT / "parser_diagnostics_latest.json"

STATUS_PASS = "pass"
STATUS_REVIEW = "review"
STATUS_FAIL = "fail"
STATUS_UNKNOWN = "unknown"

_USER_PATH_RE = re.compile(r"(?i)(/Users/|C:\\Users\\)[^\s,;]+")


@dataclass(slots=True)
class ParserDiagnosticsResult:
    report_path: Path
    report: dict[str, Any]

    def summary_line(self) -> str:
        summary = self.report.get("summary", {})
        return (
            f"Parser diagnostics: {self.report.get('overall_status', STATUS_UNKNOWN)} "
            f"({summary.get('routed_entries', 0)} routed / {summary.get('unknown_entries', 0)} unknown, "
            f"{summary.get('truncation_events', 0)} truncation)"
        )


def build_parser_diagnostics_report(
    source_log: Path,
    *,
    profile: str = DEFAULT_PROFILE,
    runtime_status: dict[str, Any] | None = None,
    drift_baseline: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _build_parser_diagnostics_report(
        source_log=source_log,
        profile=profile,
        runtime_status=runtime_status,
        drift_baseline=drift_baseline,
        input_warnings=[],
    )


def write_parser_diagnostics_report(
    *,
    source_log: Path,
    report_path: Path | None = None,
    profile: str = DEFAULT_PROFILE,
    drift_baseline_path: Path | None = None,
) -> ParserDiagnosticsResult:
    drift_baseline, input_warnings = _load_drift_baseline(drift_baseline_path)
    report = _build_parser_diagnostics_report(
        source_log=source_log,
        profile=profile,
        runtime_status=None,
        drift_baseline=drift_baseline,
        input_warnings=input_warnings,
    )
    output_path = report_path or DEFAULT_REPORT_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return ParserDiagnosticsResult(report_path=output_path, report=report)


def _build_parser_diagnostics_report(
    *,
    source_log: Path,
    profile: str,
    runtime_status: dict[str, Any] | None,
    drift_baseline: dict[str, Any] | None,
    input_warnings: list[str],
) -> dict[str, Any]:
    source_path = Path(source_log)
    normalized_profile = str(profile or "").strip() or DEFAULT_PROFILE
    report = _empty_report(source_path, profile=normalized_profile)

    if normalized_profile not in ALLOWED_PROFILES:
        _apply_input_failure(report, f"unknown_profile:{normalized_profile}")
        return _finalize_report(report, source_path)

    if not source_path.is_file():
        _apply_input_failure(report, "source_log_unreadable")
        return _finalize_report(report, source_path)

    drift_report: dict[str, Any]
    event_evidence: dict[str, Any]
    drift_report = {}
    event_evidence = _empty_event_evidence()
    try:
        baseline = drift_baseline if isinstance(drift_baseline, dict) else {}
        drift_report = log_drift_sensor.build_player_log_drift_report(source_path, baseline_payload=baseline)
        event_evidence = _collect_event_evidence(source_path)
    except Exception as exc:  # pragma: no cover - exercised by focused monkeypatch tests.
        event_evidence["failures"].append(_sanitized_failure("diagnostics_replay", exc))

    _populate_report(
        report,
        profile=normalized_profile,
        drift_report=drift_report,
        event_evidence=event_evidence,
        runtime_status=runtime_status,
        input_warnings=input_warnings,
    )
    return _finalize_report(report, source_path)


def _empty_report(source_log: Path, *, profile: str) -> dict[str, Any]:
    return {
        "object": OBJECT_KIND,
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "profile": profile,
        "overall_status": STATUS_UNKNOWN,
        "summary": {
            "parser_status": STATUS_UNKNOWN,
            "transport_status": STATUS_UNKNOWN,
            "event_families_seen": 0,
            "routed_entries": 0,
            "unknown_entries": 0,
            "truncation_events": 0,
            "parser_failures": 0,
            "transport_failures": 0,
        },
        "source": {
            "log_display_name": _display_name(source_log),
            "source_kind": profile if profile in ALLOWED_PROFILES else STATUS_UNKNOWN,
            "source_path_redacted": _display_name(source_log),
        },
        "privacy": {
            "redaction_applied": True,
            "raw_log_lines_included": False,
            "raw_payloads_included": False,
            "webhook_urls_included": False,
        },
        "parser_health": {
            "status": STATUS_UNKNOWN,
            "reasons": [],
            "entry_counts": {},
            "timestamp_anomalies": {},
            "failures": [],
        },
        "event_family_coverage": {
            "status": STATUS_UNKNOWN,
            "counts_by_kind": {},
            "expected_families": [],
            "missing_expected_families": [],
            "optional_families_seen": [],
        },
        "truncation_and_data_loss": {
            "status": STATUS_UNKNOWN,
            "truncation_count": 0,
            "data_loss_events": [],
        },
        "unknowns_and_degradation": {
            "status": STATUS_UNKNOWN,
            "unknown_signatures": [],
            "unmatched_api_names": [],
            "unmatched_request_api_names": [],
            "drift_flags": [],
        },
        "final_reconciliation": {
            "status": STATUS_UNKNOWN,
            "evidence_present": [],
            "evidence_missing": [],
            "notes": [],
        },
        "transport_health": {
            "status": STATUS_UNKNOWN,
            "webhook_successes": 0,
            "webhook_failures": 0,
            "failed_post_artifacts_seen": False,
            "notes": [],
        },
        "workbook_and_appscript": {
            "status": STATUS_UNKNOWN,
            "checked": False,
            "notes": ["Workbook and Apps Script are not queried by diagnostics v1."],
        },
        "manual_checklist": _manual_checklist(),
        "validation_evidence": {
            "commands": [],
            "fixture_policy": "sanitized_only",
        },
    }


def _populate_report(
    report: dict[str, Any],
    *,
    profile: str,
    drift_report: dict[str, Any],
    event_evidence: dict[str, Any],
    runtime_status: dict[str, Any] | None,
    input_warnings: list[str],
) -> None:
    counts = _entry_counts(drift_report)
    event_counts = _event_counts(drift_report, event_evidence)
    parser_failures = list(event_evidence.get("failures", []))
    parser_failures.extend(_runtime_parser_failures(runtime_status))
    truncation_events = list(event_evidence.get("data_loss_events", []))
    missing_expected = _missing_expected_families(profile, event_counts)
    drift_flags = _drift_flags(
        profile=profile,
        counts=counts,
        missing_expected=missing_expected,
        drift_report=drift_report,
        input_warnings=input_warnings,
        truncation_count=len(truncation_events),
    )

    report["parser_health"] = {
        "status": _parser_health_status(profile, counts, parser_failures),
        "reasons": _parser_health_reasons(profile, counts, parser_failures),
        "entry_counts": counts,
        "timestamp_anomalies": {
            "timestamp_missing": counts.get("timestamp_missing", 0),
            "timestamp_parse_failure": counts.get("timestamp_parse_failure", 0),
        },
        "failures": parser_failures,
    }
    report["event_family_coverage"] = {
        "status": STATUS_REVIEW if missing_expected else STATUS_PASS,
        "counts_by_kind": event_counts,
        "expected_families": _expected_families(profile),
        "missing_expected_families": missing_expected,
        "optional_families_seen": _optional_families_seen(event_counts, profile),
    }
    report["truncation_and_data_loss"] = {
        "status": STATUS_REVIEW if truncation_events else STATUS_PASS,
        "truncation_count": len(truncation_events),
        "data_loss_events": truncation_events,
    }
    report["unknowns_and_degradation"] = {
        "status": STATUS_REVIEW if _has_unknown_or_degraded_evidence(drift_report, drift_flags) else STATUS_PASS,
        "unknown_signatures": _top_items(drift_report, "top_unknown_signatures"),
        "unmatched_api_names": _top_items(drift_report, "top_unmatched_api_names"),
        "unmatched_request_api_names": _top_items(drift_report, "top_unmatched_request_api_names"),
        "drift_flags": drift_flags,
    }
    report["final_reconciliation"] = _final_reconciliation_section(event_counts, event_evidence)
    report["transport_health"] = _transport_health_section(runtime_status)
    report["summary"] = _summary_section(report)
    report["overall_status"] = _overall_status(report)


def _apply_input_failure(report: dict[str, Any], reason: str) -> None:
    report["parser_health"]["status"] = STATUS_FAIL
    report["parser_health"]["reasons"] = [reason]
    report["parser_health"]["failures"] = [{"stage": "input", "error_type": "InputError", "error": reason}]
    report["event_family_coverage"]["status"] = STATUS_UNKNOWN
    report["truncation_and_data_loss"]["status"] = STATUS_UNKNOWN
    report["unknowns_and_degradation"]["status"] = STATUS_UNKNOWN
    report["final_reconciliation"]["status"] = STATUS_UNKNOWN
    report["transport_health"]["status"] = STATUS_UNKNOWN
    report["summary"]["parser_status"] = STATUS_FAIL
    report["summary"]["parser_failures"] = 1
    report["overall_status"] = STATUS_FAIL


def _finalize_report(report: dict[str, Any], source_log: Path) -> dict[str, Any]:
    return _sanitize_report_value(report, redactions=_path_redactions(source_log))


def _empty_event_evidence() -> dict[str, Any]:
    return {
        "counts_by_kind": {},
        "data_loss_events": [],
        "match_completion_events": 0,
        "failures": [],
    }


def _collect_event_evidence(source_path: Path) -> dict[str, Any]:
    router = Router()
    counts_by_kind: dict[str, int] = {}
    data_loss_events: list[dict[str, Any]] = []
    match_completion_events = 0
    failures: list[dict[str, str]] = []

    for entry in log_drift_sensor.iter_log_entries(source_path):
        try:
            events = router.route(entry)
        except Exception as exc:
            failures.append(_sanitized_failure("router", exc))
            continue

        for event in events:
            kind = str(getattr(event, "kind", "")).strip()
            if kind:
                counts_by_kind[kind] = counts_by_kind.get(kind, 0) + 1
            payload = getattr(event, "payload", {}) or {}
            if kind == "MatchState" and payload.get("type") == "match_completed":
                match_completion_events += 1
            if kind == "Truncation" or payload.get("data_loss") is True:
                data_loss_events.append(_data_loss_event_summary(event))

    return {
        "counts_by_kind": dict(sorted(counts_by_kind.items())),
        "data_loss_events": data_loss_events,
        "match_completion_events": match_completion_events,
        "failures": failures,
    }


def _data_loss_event_summary(event: Any) -> dict[str, Any]:
    payload = getattr(event, "payload", {}) or {}
    metadata = getattr(event, "metadata", None)
    return {
        "event_kind": getattr(event, "kind", ""),
        "type": payload.get("type", ""),
        "data_loss": bool(payload.get("data_loss")),
        "recoverable": payload.get("recoverable"),
        "affected_event_family": payload.get("affected_event_family", ""),
        "affected_message_type": payload.get("affected_message_type", ""),
        "game_object_count": payload.get("game_object_count"),
        "annotation_count": payload.get("annotation_count"),
        "drift_flag": payload.get("drift_flag", ""),
        "value_source": payload.get("value_source", ""),
        "confidence": payload.get("confidence", ""),
        "finality": payload.get("finality", ""),
        "raw_bytes_hash": getattr(metadata, "raw_bytes_hash", ""),
    }


def _entry_counts(drift_report: dict[str, Any]) -> dict[str, Any]:
    counts = drift_report.get("entry_counts") if isinstance(drift_report, dict) else {}
    if not isinstance(counts, dict):
        counts = {}
    return {
        "total": _safe_int(counts.get("total")),
        "routed": _safe_int(counts.get("routed")),
        "unknown": _safe_int(counts.get("unknown")),
        "unknown_rate_pct": counts.get("unknown_rate_pct", 0),
        "timestamp_missing": _safe_int(counts.get("timestamp_missing")),
        "timestamp_parse_failure": _safe_int(counts.get("timestamp_parse_failure")),
    }


def _event_counts(drift_report: dict[str, Any], event_evidence: dict[str, Any]) -> dict[str, int]:
    raw_counts = drift_report.get("routed_event_kinds") if isinstance(drift_report, dict) else {}
    if not isinstance(raw_counts, dict) or not raw_counts:
        raw_counts = event_evidence.get("counts_by_kind", {})
    return {
        str(kind): _safe_int(count)
        for kind, count in sorted(raw_counts.items())
        if str(kind).strip()
    }


def _parser_health_status(profile: str, counts: dict[str, Any], parser_failures: list[dict[str, Any]]) -> str:
    if parser_failures:
        return STATUS_FAIL
    if counts.get("total", 0) > 0 and counts.get("routed", 0) == 0:
        return STATUS_FAIL
    if counts.get("unknown", 0) > 0 or counts.get("timestamp_parse_failure", 0) > 0:
        return STATUS_REVIEW
    if profile != "fixture" and counts.get("timestamp_missing", 0) > 0:
        return STATUS_REVIEW
    if counts.get("routed", 0) > 0:
        return STATUS_PASS
    return STATUS_UNKNOWN


def _parser_health_reasons(
    profile: str,
    counts: dict[str, Any],
    parser_failures: list[dict[str, Any]],
) -> list[str]:
    reasons: list[str] = []
    if parser_failures:
        reasons.append("parser_or_router_failure")
    if counts.get("total", 0) > 0 and counts.get("routed", 0) == 0:
        reasons.append("no_routed_parser_events")
    if counts.get("unknown", 0) > 0:
        reasons.append("unknown_entries_present")
    if counts.get("timestamp_parse_failure", 0) > 0:
        reasons.append("timestamp_parse_failure")
    if profile != "fixture" and counts.get("timestamp_missing", 0) > 0:
        reasons.append("timestamp_missing")
    return reasons


def _runtime_parser_failures(runtime_status: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(runtime_status, dict):
        return []
    failures: list[dict[str, Any]] = []
    for key, stage in (("router_failures", "router"), ("event_failures", "event")):
        count = _safe_int(runtime_status.get(key))
        if count > 0:
            failures.append(
                {
                    "stage": stage,
                    "error_type": str(runtime_status.get(f"last_{stage}_error_type") or "RuntimeStatusFailure"),
                    "error": sanitize_sensitive_text(runtime_status.get(f"last_{stage}_error") or f"{key}:{count}"),
                    "count": count,
                }
            )
    return failures


def _expected_families(profile: str) -> list[str]:
    expected = ["GameState_or_Truncation"]
    if profile == "live_game":
        expected.append("DetailedLoggingStatus")
    return expected


def _missing_expected_families(profile: str, counts_by_kind: dict[str, int]) -> list[str]:
    missing: list[str] = []
    if counts_by_kind.get("GameState", 0) <= 0 and counts_by_kind.get("Truncation", 0) <= 0:
        missing.append("GameState_or_Truncation")
    if profile == "live_game" and counts_by_kind.get("DetailedLoggingStatus", 0) <= 0:
        missing.append("DetailedLoggingStatus")
    return missing


def _optional_families_seen(counts_by_kind: dict[str, int], profile: str) -> list[str]:
    concrete_expected = {"GameState", "Truncation"}
    if profile == "live_game":
        concrete_expected.add("DetailedLoggingStatus")
    return sorted(kind for kind, count in counts_by_kind.items() if count > 0 and kind not in concrete_expected)


def _drift_flags(
    *,
    profile: str,
    counts: dict[str, Any],
    missing_expected: list[str],
    drift_report: dict[str, Any],
    input_warnings: list[str],
    truncation_count: int,
) -> list[str]:
    flags: list[str] = []
    flags.extend(f"missing_expected_event_family:{family}" for family in missing_expected)
    if counts.get("unknown", 0) > 0:
        flags.append("unknown_entries_present")
    if counts.get("timestamp_parse_failure", 0) > 0:
        flags.append("timestamp_parse_failure")
    if profile != "fixture" and counts.get("timestamp_missing", 0) > 0:
        flags.append("timestamp_missing")
    if truncation_count > 0:
        flags.append("missing_expected_payload_path")
    baseline_delta = drift_report.get("baseline_delta") if isinstance(drift_report, dict) else {}
    if isinstance(baseline_delta, dict):
        for key in ("new_unknown_signatures", "new_unmatched_api_names", "new_unmatched_request_api_names"):
            if baseline_delta.get(key):
                flags.append(key)
    flags.extend(input_warnings)
    return sorted(dict.fromkeys(flags))


def _has_unknown_or_degraded_evidence(drift_report: dict[str, Any], drift_flags: list[str]) -> bool:
    return bool(
        drift_flags
        or _top_items(drift_report, "top_unknown_signatures")
        or _top_items(drift_report, "top_unmatched_api_names")
        or _top_items(drift_report, "top_unmatched_request_api_names")
    )


def _top_items(drift_report: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw_items = drift_report.get(key) if isinstance(drift_report, dict) else []
    if not isinstance(raw_items, list):
        return []
    output: list[dict[str, Any]] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        output.append({str(k): _sanitize_report_value(v) for k, v in item.items()})
    return output


def _final_reconciliation_section(event_counts: dict[str, int], event_evidence: dict[str, Any]) -> dict[str, Any]:
    evidence_present: list[str] = []
    if event_counts.get("GameResult", 0) > 0:
        evidence_present.append("GameResult")
    if event_evidence.get("match_completion_events", 0) > 0:
        evidence_present.append("MatchState.match_completed")

    if evidence_present:
        return {
            "status": STATUS_PASS,
            "evidence_present": evidence_present,
            "evidence_missing": [],
            "notes": ["Final reconciliation evidence observed from parser-owned events."],
        }
    return {
        "status": STATUS_UNKNOWN,
        "evidence_present": [],
        "evidence_missing": ["GameResult_or_MatchState.match_completed"],
        "notes": ["No completed-game final reconciliation evidence was observed; diagnostics does not infer it."],
    }


def _transport_health_section(runtime_status: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(runtime_status, dict):
        return {
            "status": STATUS_UNKNOWN,
            "webhook_successes": 0,
            "webhook_failures": 0,
            "failed_post_artifacts_seen": False,
            "notes": ["Optional runtime status was not supplied."],
        }

    successes = _safe_int(runtime_status.get("webhook_successes"))
    failures = _safe_int(runtime_status.get("webhook_failures"))
    failed_posts_seen = bool(runtime_status.get("failed_post_artifacts_seen"))
    notes: list[str] = []
    if runtime_status.get("last_webhook_error"):
        notes.append(f"last_webhook_error={sanitize_sensitive_text(runtime_status.get('last_webhook_error'))}")
    if failures > 0:
        notes.append("Webhook failure is transport evidence, not parser-truth failure.")

    status = STATUS_PASS
    if failures > 0 or failed_posts_seen:
        status = STATUS_REVIEW

    return {
        "status": status,
        "webhook_successes": successes,
        "webhook_failures": failures,
        "failed_post_artifacts_seen": failed_posts_seen,
        "notes": notes,
    }


def _summary_section(report: dict[str, Any]) -> dict[str, Any]:
    parser_health = report["parser_health"]
    transport_health = report["transport_health"]
    event_counts = report["event_family_coverage"]["counts_by_kind"]
    entry_counts = parser_health.get("entry_counts", {})
    parser_failures = parser_health.get("failures", [])
    return {
        "parser_status": parser_health.get("status", STATUS_UNKNOWN),
        "transport_status": transport_health.get("status", STATUS_UNKNOWN),
        "event_families_seen": len([kind for kind, count in event_counts.items() if count > 0]),
        "routed_entries": _safe_int(entry_counts.get("routed")),
        "unknown_entries": _safe_int(entry_counts.get("unknown")),
        "truncation_events": _safe_int(report["truncation_and_data_loss"].get("truncation_count")),
        "parser_failures": sum(_safe_int(item.get("count", 1)) for item in parser_failures),
        "transport_failures": _safe_int(transport_health.get("webhook_failures")),
    }


def _overall_status(report: dict[str, Any]) -> str:
    fail_sections = ("parser_health", "event_family_coverage")
    if any(report[section].get("status") == STATUS_FAIL for section in fail_sections):
        return STATUS_FAIL
    review_sections = (
        "parser_health",
        "event_family_coverage",
        "truncation_and_data_loss",
        "unknowns_and_degradation",
        "final_reconciliation",
        "transport_health",
    )
    if any(report[section].get("status") == STATUS_REVIEW for section in review_sections):
        return STATUS_REVIEW
    if (
        report["parser_health"].get("status") == STATUS_PASS
        and report["event_family_coverage"].get("status") == STATUS_PASS
    ):
        return STATUS_PASS
    return STATUS_UNKNOWN


def _load_drift_baseline(path: Path | None) -> tuple[dict[str, Any], list[str]]:
    if path is None or not path.exists():
        return {}, []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}, ["malformed_drift_baseline_json"]
    if not isinstance(payload, dict):
        return {}, ["malformed_drift_baseline_json"]
    return payload, []


def _sanitized_failure(stage: str, exc: Exception) -> dict[str, str]:
    return {
        "stage": stage,
        "error_type": type(exc).__name__,
        "error": sanitize_sensitive_text(exc),
    }


def _sanitize_report_value(value: Any, *, redactions: tuple[str, ...] = ()) -> Any:
    if isinstance(value, dict):
        return {str(key): _sanitize_report_value(item, redactions=redactions) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_report_value(item, redactions=redactions) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_report_value(item, redactions=redactions) for item in value]
    if isinstance(value, str):
        text = sanitize_sensitive_text(value)
        text = _USER_PATH_RE.sub("[redacted-path]", text)
        for redaction in redactions:
            if redaction:
                text = text.replace(redaction, "[redacted-path]")
        return text
    return value


def _path_redactions(path: Path) -> tuple[str, ...]:
    values = [str(path), str(path.parent)]
    try:
        values.append(str(path.resolve(strict=False)))
        values.append(str(path.resolve(strict=False).parent))
    except Exception:
        pass
    return tuple(dict.fromkeys(value for value in values if value))


def _display_name(path: Path) -> str:
    name = Path(path).name
    return name or "[redacted-path]"


def _safe_int(value: Any) -> int:
    try:
        if isinstance(value, bool):
            return int(value)
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _manual_checklist() -> dict[str, list[str]]:
    return {
        "before_run": [
            "Confirm the working branch is codex/parser-reliability-intelligence.",
            "Confirm no raw local logs or generated diagnostics reports are staged.",
            "Start the normal parser runtime.",
            "Verify the runtime status file is updating locally.",
            "Decide whether the run checks parser only or parser plus transport.",
        ],
        "during_run": [
            "Play a fresh MTGA game long enough to exercise GameState evidence.",
            "If possible, let the game reach normal completion.",
            "Do not copy raw log excerpts into notes or repo files.",
            "Note only human-safe context.",
        ],
        "after_run": [
            "Run diagnostics mode against the local log or selected private local slice.",
            "Save the report under ignored local data/status/ or another ignored local path.",
            "Review parser, data-loss, unknown/degraded, reconciliation, and transport sections separately.",
            "Route parser behavior problems to a new issue and contract.",
        ],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a local parser diagnostics acceptance report.")
    parser.add_argument(
        "source_log",
        nargs="?",
        default=str(LOG_PATH),
        help="Path to Player.log or a sanitized fixture.",
    )
    parser.add_argument("--profile", choices=sorted(ALLOWED_PROFILES), default=DEFAULT_PROFILE)
    parser.add_argument("--out", dest="report_path", default=str(DEFAULT_REPORT_PATH))
    parser.add_argument("--drift-baseline", dest="drift_baseline_path", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    result = write_parser_diagnostics_report(
        source_log=Path(args.source_log),
        report_path=Path(args.report_path),
        profile=args.profile,
        drift_baseline_path=Path(args.drift_baseline_path) if args.drift_baseline_path else None,
    )
    print(result.summary_line())
    print(f"Report written: {_safe_report_path(result.report_path)}")
    return 1 if result.report.get("overall_status") == STATUS_FAIL else 0


def _safe_report_path(path: Path) -> str:
    try:
        return str(path.resolve(strict=False).relative_to(PROJECT_ROOT.resolve(strict=False)))
    except Exception:
        return path.name or "[redacted-path]"


if __name__ == "__main__":
    raise SystemExit(main())
