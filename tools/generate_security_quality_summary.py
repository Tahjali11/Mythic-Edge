"""Generate a public-safe advisory security-quality summary report."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "security_quality_scanner_summary_aggregation.v1"
REPOSITORY = "Tahjali11/Mythic-Edge"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge"
SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/610"
PARENT_SECURITY_WORKFLOW = "https://github.com/Tahjali11/Mythic-Edge/issues/330"
PROJECT_ROADMAP = "https://github.com/Tahjali11/Mythic-Edge/issues/568"
CONTRACT_REF = "docs/contracts/security_quality_scanner_summary_aggregation.md"
DEFAULT_CWE_REPORT = Path(
    "docs/quality_reports/security/cwe_mapped_local_validation_profile/"
    "2026-07-01-024eda7-cwe-profile-advisory-report.json",
)
REPORT_DIR = Path("docs/quality_reports/security/security_quality_summary")
DEFAULT_NEXT_ROLE = "Codex E: Module Reviewer / contract-test thread"

SOURCE_IDS = {
    "codeql",
    "cwe_profile_report",
    "protected_surface_scan",
    "secret_private_marker_scan",
    "ci_or_repo_check_status",
}

CODEQL_SOURCE_STATES = {"none", "summary-file"}

CODEQL_ALLOWED_KEYS = {
    "source",
    "repository",
    "repository_url",
    "ref",
    "analysis_commit",
    "measured_commit",
    "queried_at_policy",
    "provided_at_policy",
    "state_counts",
    "severity_counts",
    "rule_id_counts",
    "tool_name",
    "source_url",
    "workflow_run_url",
    "freshness_status",
}

SCANNER_ALLOWED_KEYS = {
    "tool",
    "mode",
    "base",
    "head",
    "scanned_paths",
    "changed_paths",
    "skipped_paths",
    "forbidden",
    "warnings",
    "result",
    "freshness_status",
    "symbolic_category_counts",
}

CI_ALLOWED_KEYS = {
    "workflow_name",
    "run_url",
    "conclusion",
    "commit",
    "branch",
    "ref",
    "collected_at_policy",
    "freshness_status",
}

CWE_REPORT_ALLOWED_KEYS = {
    "schema_version",
    "report_id",
    "repository",
    "repository_url",
    "contract_ref",
    "source_issue",
    "parent_issue",
    "source_profile_contract",
    "source_profile_manifest",
    "source_validator",
    "measured_ref",
    "measured_commit",
    "generated_at_policy",
    "run_mode",
    "overall_status",
    "profile_status",
    "profile_family_count",
    "families",
    "validator",
    "blocked_items",
    "non_claims",
    "privacy_redaction",
    "advisory_only",
    "enforcement_authorized",
    "ci_change_authorized",
    "codeql_alert_mutation_authorized",
    "security_assurance_claimed",
    "privacy_assurance_claimed",
    "validation_commands",
    "next_recommended_role",
}

UNSAFE_FIELD_NAMES = {
    "absolute_path",
    "alert",
    "alerts",
    "api_key",
    "codeflows",
    "code_flows",
    "description",
    "descriptions",
    "endpoint",
    "endpoint_value",
    "environment_value",
    "excerpt",
    "excerpts",
    "finding",
    "findings",
    "fingerprint",
    "fingerprints",
    "full_path",
    "local_path",
    "location",
    "locations",
    "message",
    "messages",
    "partialfingerprints",
    "private_path",
    "raw_finding",
    "raw_findings",
    "raw_payload",
    "raw_payloads",
    "raw_sarif",
    "sarif",
    "secret",
    "snippet",
    "snippets",
    "spreadsheet_id",
    "stack_trace",
    "token",
    "uri",
    "webhook_url",
}

UNSAFE_TEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("local_windows_absolute_path", re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]+", re.IGNORECASE)),
    ("local_unix_user_path", re.compile(r"/(?:Users|home)/[^\s\"'<>]+", re.IGNORECASE)),
    ("live_google_script_url", re.compile(r"https://script\.google\.com/macros/s/", re.IGNORECASE)),
    ("private_key_marker", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("credential_assignment", re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*[^<\s][^\s,;]{7,}")),
)

VALIDATION_COMMANDS = (
    r"py -m pytest -q tests\test_security_quality_summary.py",
    r"py -m pytest -q tests\test_cwe_profile_advisory_report.py tests\test_cwe_mapped_local_validation_profile.py",
    r"py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json",
    (
        r"py -m json.tool "
        "docs\\quality_reports\\security\\cwe_mapped_local_validation_profile\\"
        "2026-07-01-024eda7-cwe-profile-advisory-report.json"
    ),
    (
        r"py tools\check_cwe_mapped_local_validation_profile.py "
        r"docs\security\cwe_mapped_local_validation_profile.v1.json"
    ),
    r"py -m ruff check tools\generate_security_quality_summary.py tests\test_security_quality_summary.py",
    r"git diff --check",
    r"py tools\check_agent_docs.py",
    r"path-scoped protected-surface scan over changed files",
    r"path-scoped secret/private-marker scan over changed files",
)

NON_CLAIMS = (
    "This report is advisory workflow evidence only.",
    "This report does not mutate, dismiss, reopen, or close CodeQL alerts.",
    "This report does not prove that CodeQL has zero open alerts.",
    "This report is not formal CWE compliance.",
    "This report is not security assurance.",
    "This report is not privacy assurance.",
    "This report is not release readiness.",
    "This report is not deploy readiness.",
    "This report is not production readiness.",
    "This report is not parser truth, analytics truth, AI truth, or coaching truth.",
)


@dataclass(frozen=True)
class RepoMetadata:
    measured_ref: str
    measured_commit: str


@dataclass(frozen=True)
class LoadedSummary:
    source_id: str
    path_label: str
    data: dict[str, Any]


class UnsafeInputError(ValueError):
    """Raised when a public-safe summary input includes unsafe content."""

    def __init__(self, source_id: str, reason: str) -> None:
        self.source_id = source_id
        self.reason = reason
        super().__init__(f"{source_id}: {reason}")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git_value(repo_root: Path, args: list[str], fallback: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return fallback
    value = completed.stdout.strip()
    return value or fallback


def read_repo_metadata(repo_root: Path | None = None) -> RepoMetadata:
    root = repo_root or _repo_root()
    return RepoMetadata(
        measured_ref=_git_value(root, ["branch", "--show-current"], "unknown"),
        measured_commit=_git_value(root, ["rev-parse", "HEAD"], "unknown"),
    )


def _short_commit(commit: str) -> str:
    safe = commit if isinstance(commit, str) else "unknown"
    return safe[:7] or "unknown"


def default_report_path(report_date: str, measured_commit: str) -> Path:
    return REPORT_DIR / f"{report_date}-{_short_commit(measured_commit)}-security-quality-summary.json"


def _json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def _repo_relative_label(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except (OSError, ValueError):
        return "provided_public_summary_file"


def _normalize_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")


def _walk_json(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []

    def walk(candidate: Any) -> None:
        items.append(("value", candidate))
        if isinstance(candidate, dict):
            for key, child in candidate.items():
                items.append(("key", key))
                walk(child)
        elif isinstance(candidate, list):
            for child in candidate:
                walk(child)

    walk(value)
    return items


def _contains_unsafe_text(text: str) -> bool:
    return any(pattern.search(text) for _, pattern in UNSAFE_TEXT_PATTERNS)


def _validate_public_safe_summary(
    data: dict[str, Any],
    *,
    source_id: str,
    allowed_top_level_keys: set[str],
) -> None:
    for item_type, item in _walk_json(data):
        if not isinstance(item, str):
            continue
        normalized = _normalize_key(item)
        if item_type == "key" and normalized in UNSAFE_FIELD_NAMES:
            raise UnsafeInputError(source_id, "blocked_unsafe_input")
        if item_type == "value" and _contains_unsafe_text(item):
            raise UnsafeInputError(source_id, "blocked_unsafe_input")

    unexpected = set(data) - allowed_top_level_keys
    if unexpected:
        raise UnsafeInputError(source_id, "blocked_unsupported_schema")


def _load_public_summary(
    path: Path,
    *,
    source_id: str,
    allowed_top_level_keys: set[str],
    repo_root: Path,
) -> LoadedSummary:
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise UnsafeInputError(source_id, "blocked_unavailable") from exc

    if not isinstance(data, dict):
        raise UnsafeInputError(source_id, "blocked_unsupported_schema")

    _validate_public_safe_summary(
        data,
        source_id=source_id,
        allowed_top_level_keys=allowed_top_level_keys,
    )
    return LoadedSummary(
        source_id=source_id,
        path_label=_repo_relative_label(path, repo_root),
        data=data,
    )


def _freshness(source_commit: Any, report_commit: str) -> str:
    if not isinstance(source_commit, str) or not source_commit:
        return "unknown"
    return "current" if source_commit == report_commit else "stale"


def _source_entry(
    *,
    source_id: str,
    source_type: str,
    status: str,
    tool_or_authority: str,
    measured_ref: str,
    measured_commit: str,
    collected_at_policy: str,
    freshness_status: str,
    result: str,
    counts: dict[str, Any],
    notes: list[str],
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "source_type": source_type,
        "status": status,
        "tool_or_authority": tool_or_authority,
        "measured_ref": measured_ref,
        "measured_commit": measured_commit,
        "collected_at_policy": collected_at_policy,
        "freshness_status": freshness_status,
        "result": result,
        "counts": counts,
        "public_safe": True,
        "raw_payload_included": False,
        "local_private_data_included": False,
        "notes": notes,
    }


def _not_collected_source(
    *,
    source_id: str,
    source_type: str,
    tool_or_authority: str,
    metadata: RepoMetadata,
) -> dict[str, Any]:
    return _source_entry(
        source_id=source_id,
        source_type=source_type,
        status="not_collected",
        tool_or_authority=tool_or_authority,
        measured_ref=metadata.measured_ref,
        measured_commit=metadata.measured_commit,
        collected_at_policy="not_collected",
        freshness_status="not_collected",
        result="not_collected",
        counts={},
        notes=["No public-safe summary input was provided to this advisory helper."],
    )


def _blocked_source(source_id: str, metadata: RepoMetadata) -> dict[str, Any]:
    return _source_entry(
        source_id=source_id,
        source_type="blocked_input",
        status="blocked_unsafe_input",
        tool_or_authority="input_validator",
        measured_ref=metadata.measured_ref,
        measured_commit=metadata.measured_commit,
        collected_at_policy="blocked",
        freshness_status="unknown",
        result="blocked_unsafe_input",
        counts={},
        notes=["A source input was rejected without echoing unsafe content."],
    )


def _cwe_section(
    loaded: LoadedSummary,
    *,
    metadata: RepoMetadata,
) -> tuple[dict[str, Any], dict[str, Any]]:
    data = loaded.data
    source_commit = str(data.get("measured_commit", "unknown"))
    source_ref = str(data.get("measured_ref", "unknown"))
    freshness_status = _freshness(source_commit, metadata.measured_commit)
    validator = data.get("validator", {})
    validator_counts = {
        "profile_family_count": data.get("profile_family_count", 0),
        "validator_errors": validator.get("errors_count", 0) if isinstance(validator, dict) else 0,
        "validator_warnings": validator.get("warnings_count", 0) if isinstance(validator, dict) else 0,
    }
    source = _source_entry(
        source_id="cwe_profile_report",
        source_type="local_cwe_profile_advisory_report",
        status="collected_current" if freshness_status == "current" else "stale",
        tool_or_authority="tools/generate_cwe_profile_advisory_report.py",
        measured_ref=source_ref,
        measured_commit=source_commit,
        collected_at_policy=str(data.get("generated_at_policy", "manual_or_test_only")),
        freshness_status=freshness_status,
        result=str(data.get("overall_status", "unknown")),
        counts=validator_counts,
        notes=[f"Artifact: {loaded.path_label}"],
    )
    section = {
        "source_state": source["status"],
        "artifact": loaded.path_label,
        "schema_version": data.get("schema_version", "unknown"),
        "report_id": data.get("report_id", "unknown"),
        "measured_ref": source_ref,
        "measured_commit": source_commit,
        "freshness_status": freshness_status,
        "overall_status": data.get("overall_status", "unknown"),
        "profile_status": data.get("profile_status", "unknown"),
        "profile_family_count": data.get("profile_family_count", 0),
        "validator": {
            "result": validator.get("result", "unknown") if isinstance(validator, dict) else "unknown",
            "exit_code": validator.get("exit_code", "unknown") if isinstance(validator, dict) else "unknown",
            "errors_count": validator_counts["validator_errors"],
            "warnings_count": validator_counts["validator_warnings"],
        },
        "advisory_only": data.get("advisory_only") is True,
        "enforcement_authorized": data.get("enforcement_authorized") is True,
        "ci_change_authorized": data.get("ci_change_authorized") is True,
        "codeql_alert_mutation_authorized": data.get("codeql_alert_mutation_authorized") is True,
        "security_assurance_claimed": data.get("security_assurance_claimed") is True,
        "privacy_assurance_claimed": data.get("privacy_assurance_claimed") is True,
    }
    return source, section


def _codeql_section(
    loaded: LoadedSummary | None,
    *,
    metadata: RepoMetadata,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if loaded is None:
        source = _not_collected_source(
            source_id="codeql",
            source_type="github_code_scanning",
            tool_or_authority="GitHub CodeQL code scanning",
            metadata=metadata,
        )
        return source, {"source_state": "not_collected", "lifecycle_claim": "not_collected"}

    data = loaded.data
    source_commit = str(data.get("analysis_commit") or data.get("measured_commit") or "unknown")
    source_ref = str(data.get("ref", "unknown"))
    freshness_status = str(data.get("freshness_status") or _freshness(source_commit, metadata.measured_commit))
    state_counts = data.get("state_counts", {})
    severity_counts = data.get("severity_counts", {})
    rule_id_counts = data.get("rule_id_counts", {})
    counts = {
        "state_counts": state_counts if isinstance(state_counts, dict) else {},
        "severity_counts": severity_counts if isinstance(severity_counts, dict) else {},
        "rule_id_counts": rule_id_counts if isinstance(rule_id_counts, dict) else {},
    }
    source = _source_entry(
        source_id="codeql",
        source_type="github_code_scanning",
        status="provided_by_codex_g",
        tool_or_authority=str(data.get("tool_name", "GitHub CodeQL code scanning")),
        measured_ref=source_ref,
        measured_commit=source_commit,
        collected_at_policy=str(data.get("queried_at_policy") or data.get("provided_at_policy") or "provided_summary"),
        freshness_status=freshness_status,
        result="provided_summary",
        counts=counts,
        notes=[f"Artifact: {loaded.path_label}", "Lifecycle state remains separate from local scanners."],
    )
    section = {
        "source_state": "provided_by_codex_g",
        "lifecycle_claim": "provided_summary_only",
        "ref": source_ref,
        "analysis_commit": source_commit,
        "freshness_status": freshness_status,
        "open_count": counts["state_counts"].get("open", "unknown"),
        "fixed_count": counts["state_counts"].get("fixed", "unknown"),
        "dismissed_count": counts["state_counts"].get("dismissed", "unknown"),
        "severity_counts": counts["severity_counts"],
        "rule_id_counts": counts["rule_id_counts"],
        "source_url": data.get("source_url") or data.get("workflow_run_url") or "not_provided",
        "codeql_alert_mutation_authorized": False,
    }
    return source, section


def _scanner_section(
    loaded: LoadedSummary | None,
    *,
    source_id: str,
    source_type: str,
    tool_or_authority: str,
    metadata: RepoMetadata,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if loaded is None:
        source = _not_collected_source(
            source_id=source_id,
            source_type=source_type,
            tool_or_authority=tool_or_authority,
            metadata=metadata,
        )
        return source, {"source_state": "not_collected", "result": "not_collected"}

    data = loaded.data
    source_commit = str(data.get("head", "unknown"))
    freshness_status = str(data.get("freshness_status") or _freshness(source_commit, metadata.measured_commit))
    counts = {
        "scanned_paths": data.get("scanned_paths", data.get("changed_paths", 0)),
        "skipped_paths": data.get("skipped_paths", 0),
        "forbidden": data.get("forbidden", 0),
        "warnings": data.get("warnings", 0),
        "symbolic_category_counts": data.get("symbolic_category_counts", {}),
    }
    result = str(data.get("result", "unknown"))
    source = _source_entry(
        source_id=source_id,
        source_type=source_type,
        status="provided_summary",
        tool_or_authority=str(data.get("tool", tool_or_authority)),
        measured_ref=str(data.get("base", "unknown")),
        measured_commit=source_commit,
        collected_at_policy="provided_summary",
        freshness_status=freshness_status,
        result=result,
        counts=counts,
        notes=[f"Artifact: {loaded.path_label}", "Scanner result is advisory validation evidence only."],
    )
    section = {
        "source_state": "provided_summary",
        "tool": source["tool_or_authority"],
        "mode": data.get("mode", "unknown"),
        "base": data.get("base", "unknown"),
        "head": source_commit,
        "freshness_status": freshness_status,
        "result": result,
        "counts": counts,
    }
    return source, section


def _ci_section(
    loaded: LoadedSummary | None,
    *,
    metadata: RepoMetadata,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if loaded is None:
        source = _not_collected_source(
            source_id="ci_or_repo_check_status",
            source_type="workflow_status",
            tool_or_authority="repo workflow status",
            metadata=metadata,
        )
        return source, {"source_state": "not_collected", "result": "not_collected"}

    data = loaded.data
    source_commit = str(data.get("commit", "unknown"))
    freshness_status = str(data.get("freshness_status") or _freshness(source_commit, metadata.measured_commit))
    source = _source_entry(
        source_id="ci_or_repo_check_status",
        source_type="workflow_status",
        status="provided_summary",
        tool_or_authority=str(data.get("workflow_name", "repo workflow status")),
        measured_ref=str(data.get("ref") or data.get("branch") or "unknown"),
        measured_commit=source_commit,
        collected_at_policy=str(data.get("collected_at_policy", "provided_summary")),
        freshness_status=freshness_status,
        result=str(data.get("conclusion", "unknown")),
        counts={},
        notes=[f"Artifact: {loaded.path_label}", "Workflow status is not security or release assurance."],
    )
    section = {
        "source_state": "provided_summary",
        "workflow_name": data.get("workflow_name", "unknown"),
        "conclusion": data.get("conclusion", "unknown"),
        "commit": source_commit,
        "ref": source["measured_ref"],
        "freshness_status": freshness_status,
    }
    return source, section


def _overall_status(sources: list[dict[str, Any]]) -> str:
    if any(source["status"] == "blocked_unsafe_input" for source in sources):
        return "blocked_unsafe_input"
    if any(str(source["result"]).startswith("failed") for source in sources):
        return "advisory_failed"
    if any(source["freshness_status"] in {"stale", "unknown"} for source in sources):
        return "advisory_warnings"
    if any(source["status"] == "not_collected" for source in sources):
        return "partial_missing_sources"
    return "advisory_passed"


def _freshness_status(sources: list[dict[str, Any]]) -> str:
    statuses = {source["freshness_status"] for source in sources}
    if "stale" in statuses or len(statuses - {"current"}) > 1:
        return "mixed"
    if statuses == {"current"}:
        return "current"
    if statuses == {"not_collected"}:
        return "not_collected"
    return "unknown"


def _base_report(
    *,
    metadata: RepoMetadata,
    report_date: str,
    sources: list[dict[str, Any]],
    blocked_inputs: list[dict[str, str]],
    codeql: dict[str, Any],
    cwe_profile_report: dict[str, Any],
    protected_surface_scan: dict[str, Any],
    private_marker_scan: dict[str, Any],
    ci_or_repo_check_status: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "report_id": f"security-quality-summary:{_short_commit(metadata.measured_commit)}:{report_date}",
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "source_issue": SOURCE_ISSUE,
        "parent_security_workflow": PARENT_SECURITY_WORKFLOW,
        "project_roadmap": PROJECT_ROADMAP,
        "contract_ref": CONTRACT_REF,
        "measured_ref": metadata.measured_ref,
        "measured_commit": metadata.measured_commit,
        "generated_at_policy": "manual_or_test_only",
        "overall_status": _overall_status(sources),
        "freshness_status": _freshness_status(sources),
        "sources": sources,
        "codeql": codeql,
        "cwe_profile_report": cwe_profile_report,
        "protected_surface_scan": protected_surface_scan,
        "secret_private_marker_scan": private_marker_scan,
        "ci_or_repo_check_status": ci_or_repo_check_status,
        "blocked_inputs": blocked_inputs,
        "non_claims": list(NON_CLAIMS),
        "privacy_redaction": {
            "policy": "symbolic_counts_statuses_refs_and_repo_relative_artifacts_only",
            "unsafe_input_echoed": False,
            "raw_payloads_included": False,
            "raw_finding_lists_included": False,
            "local_private_data_included": False,
            "absolute_paths_included": False,
            "secret_values_included": False,
        },
        "advisory_only": True,
        "enforcement_authorized": False,
        "ci_change_authorized": False,
        "codeql_alert_mutation_authorized": False,
        "security_assurance_claimed": False,
        "privacy_assurance_claimed": False,
        "release_readiness_claimed": False,
        "deploy_readiness_claimed": False,
        "parser_truth_claimed": False,
        "analytics_truth_claimed": False,
        "ai_truth_claimed": False,
        "coaching_truth_claimed": False,
        "validation_commands": list(VALIDATION_COMMANDS),
        "next_recommended_role": DEFAULT_NEXT_ROLE,
    }


def _blocked_report(
    *,
    metadata: RepoMetadata,
    report_date: str,
    blocked_source_id: str,
    reason: str,
) -> dict[str, Any]:
    sources = [_blocked_source(blocked_source_id, metadata)]
    return _base_report(
        metadata=metadata,
        report_date=report_date,
        sources=sources,
        blocked_inputs=[{"source_id": blocked_source_id, "reason": reason}],
        codeql={"source_state": "blocked_unsafe_input"} if blocked_source_id == "codeql" else {},
        cwe_profile_report=(
            {"source_state": "blocked_unsafe_input"} if blocked_source_id == "cwe_profile_report" else {}
        ),
        protected_surface_scan=(
            {"source_state": "blocked_unsafe_input"} if blocked_source_id == "protected_surface_scan" else {}
        ),
        private_marker_scan=(
            {"source_state": "blocked_unsafe_input"} if blocked_source_id == "secret_private_marker_scan" else {}
        ),
        ci_or_repo_check_status=(
            {"source_state": "blocked_unsafe_input"} if blocked_source_id == "ci_or_repo_check_status" else {}
        ),
    )


def _validate_codeql_state_source(codeql_state_source: str) -> None:
    if codeql_state_source not in CODEQL_SOURCE_STATES:
        raise UnsafeInputError("codeql", "blocked_unsupported_mode")


def _required_codeql_summary_path(codeql_summary_path: Path | None) -> Path:
    if codeql_summary_path is None:
        raise UnsafeInputError("codeql", "blocked_unavailable")
    return codeql_summary_path


def generate_report(
    *,
    cwe_report_path: Path | None = None,
    codeql_state_source: str = "none",
    codeql_summary_path: Path | None = None,
    protected_surface_summary_path: Path | None = None,
    private_marker_summary_path: Path | None = None,
    ci_summary_path: Path | None = None,
    report_date: str | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = repo_root or _repo_root()
    metadata = read_repo_metadata(root)
    safe_report_date = report_date or datetime.now(UTC).date().isoformat()

    try:
        cwe_loaded = _load_public_summary(
            root / (cwe_report_path or DEFAULT_CWE_REPORT),
            source_id="cwe_profile_report",
            allowed_top_level_keys=CWE_REPORT_ALLOWED_KEYS,
            repo_root=root,
        )
        codeql_loaded = None
        _validate_codeql_state_source(codeql_state_source)
        if codeql_state_source == "summary-file":
            codeql_loaded = _load_public_summary(
                _required_codeql_summary_path(codeql_summary_path),
                source_id="codeql",
                allowed_top_level_keys=CODEQL_ALLOWED_KEYS,
                repo_root=root,
            )
        protected_loaded = (
            _load_public_summary(
                protected_surface_summary_path,
                source_id="protected_surface_scan",
                allowed_top_level_keys=SCANNER_ALLOWED_KEYS,
                repo_root=root,
            )
            if protected_surface_summary_path is not None
            else None
        )
        marker_loaded = (
            _load_public_summary(
                private_marker_summary_path,
                source_id="secret_private_marker_scan",
                allowed_top_level_keys=SCANNER_ALLOWED_KEYS,
                repo_root=root,
            )
            if private_marker_summary_path is not None
            else None
        )
        ci_loaded = (
            _load_public_summary(
                ci_summary_path,
                source_id="ci_or_repo_check_status",
                allowed_top_level_keys=CI_ALLOWED_KEYS,
                repo_root=root,
            )
            if ci_summary_path is not None
            else None
        )
    except UnsafeInputError as exc:
        return _blocked_report(
            metadata=metadata,
            report_date=safe_report_date,
            blocked_source_id=exc.source_id,
            reason=exc.reason,
        )

    cwe_source, cwe_section = _cwe_section(cwe_loaded, metadata=metadata)
    codeql_source, codeql_section = _codeql_section(codeql_loaded, metadata=metadata)
    protected_source, protected_section = _scanner_section(
        protected_loaded,
        source_id="protected_surface_scan",
        source_type="protected_surface_scanner",
        tool_or_authority="tools/check_protected_surfaces.py",
        metadata=metadata,
    )
    marker_source, marker_section = _scanner_section(
        marker_loaded,
        source_id="secret_private_marker_scan",
        source_type="secret_private_marker_scanner",
        tool_or_authority="tools/check_secret_patterns.py",
        metadata=metadata,
    )
    ci_source, ci_section = _ci_section(ci_loaded, metadata=metadata)
    sources = [codeql_source, cwe_source, protected_source, marker_source, ci_source]

    return _base_report(
        metadata=metadata,
        report_date=safe_report_date,
        sources=sources,
        blocked_inputs=[],
        codeql=codeql_section,
        cwe_profile_report=cwe_section,
        protected_surface_scan=protected_section,
        private_marker_scan=marker_section,
        ci_or_repo_check_status=ci_section,
    )


def write_default_report(report: dict[str, Any], *, report_date: str, repo_root: Path | None = None) -> Path:
    root = repo_root or _repo_root()
    output_path = root / default_report_path(report_date, str(report.get("measured_commit", "unknown")))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # lgtm[py/clear-text-storage-sensitive-data] Contracted public-safe summary artifact after strict input validation.
    output_path.write_text(_json_text(report), encoding="utf-8")
    return output_path.relative_to(root)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwe-report", type=Path, default=None, help="Public-safe CWE advisory report path.")
    parser.add_argument(
        "--codeql-state-source",
        choices=sorted(CODEQL_SOURCE_STATES),
        default="none",
        help="CodeQL lifecycle source mode; live GitHub queries are not supported in this slice.",
    )
    parser.add_argument("--codeql-summary", type=Path, default=None, help="Public-safe CodeQL summary JSON.")
    parser.add_argument(
        "--protected-surface-summary",
        type=Path,
        default=None,
        help="Public-safe protected-surface scanner summary JSON.",
    )
    parser.add_argument(
        "--secret-private-summary",
        dest="private_marker_summary",
        type=Path,
        default=None,
        help="Public-safe secret/private-marker scanner summary JSON.",
    )
    parser.add_argument("--ci-summary", type=Path, default=None, help="Public-safe workflow status summary JSON.")
    parser.add_argument("--write-report", action="store_true", help="Write the default aggregate report artifact.")
    parser.add_argument(
        "--report-date",
        default=datetime.now(UTC).date().isoformat(),
        help="Report artifact date in YYYY-MM-DD format.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = generate_report(
        cwe_report_path=args.cwe_report,
        codeql_state_source=args.codeql_state_source,
        codeql_summary_path=args.codeql_summary,
        protected_surface_summary_path=args.protected_surface_summary,
        private_marker_summary_path=args.private_marker_summary,
        ci_summary_path=args.ci_summary,
        report_date=args.report_date,
    )
    if args.write_report:
        write_default_report(report, report_date=args.report_date)
        print("security quality summary report written")
    else:
        print("security quality summary generated")
    return 2 if report["overall_status"].startswith("blocked") else 0


if __name__ == "__main__":
    raise SystemExit(main())
