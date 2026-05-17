"""Generate a deterministic repo-wide hardening status report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPORT_KIND = "repo_wide_hardening_status"
REPORT_SCHEMA_VERSION = 1
GENERATOR_PATH = "tools/generate_hardening_report.py"
TRACKER_URL = "https://github.com/Tahjali11/Mythic-Edge/issues/82"
SOURCE_ISSUE_URL = "https://github.com/Tahjali11/Mythic-Edge/issues/100"
BRANCH_NAME = "codex/repo-wide-hardening-run"
EVIDENCE_MODE = "repo_local_and_operator_supplied"
NOT_DECIDED = "not_decided_by_report"
APPROVED_OUTPUT_PREFIX = "docs/contract_test_reports/"
APPROVED_STATUS_REPORT = "docs/contract_test_reports/repo_wide_hardening_status_report.md"
DEFAULT_NEXT_ROLE = "Codex E: Module Reviewer / contract-test thread"

SOURCE_LABELS = {
    "repo_local_artifact",
    "operator_supplied",
    "tool_report",
    "tracker_comment",
    "pr_metadata",
    "ci_summary",
    "missing",
}
CONFIDENCE_LABELS = {"confirmed", "reported", "inferred_from_presence", "missing", "unknown"}
FINALITY_LABELS = {"final", "advisory", "lifecycle_open", "pending_review", "unknown"}
ALLOWED_STATUSES = {"passed", "failed", "warning", "advisory", "not_run", "not_supplied", "missing", "unknown"}
ALLOWED_STATES = {"open", "closed", "merged", "draft", "ready_for_review", "unknown"}

ARTIFACT_GROUPS: tuple[tuple[str, str], ...] = (
    ("baseline report", "docs/contract_test_reports/repo_wide_hardening_baseline.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_validation_selector.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_secret_private_marker_scanner.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_agent_docs_consistency_checker.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_protected_surface_authorization_checker.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_golden_fixture_first_pass.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_drift_detector_baseline_first_pass.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_pyright_advisory_report.md"),
    ("repo-wide contract", "docs/contracts/repo_wide_hardening_report_generator.md"),
    ("implementation handoff", "docs/implementation_handoffs/repo_wide_validation_selector_comparison.md"),
    ("implementation handoff", "docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md"),
    ("implementation handoff", "docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md"),
    (
        "implementation handoff",
        "docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md",
    ),
    (
        "implementation handoff",
        "docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md",
    ),
    ("implementation handoff", "docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md"),
    (
        "implementation handoff",
        "docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md",
    ),
    ("implementation handoff", "docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md"),
    ("implementation handoff", "docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_validation_selector.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_secret_private_marker_scanner.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_protected_surface_authorization_checker.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_workbook_webhook_schema_snapshots.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_golden_fixture_first_pass.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_pyright_advisory_report.md"),
    ("contract-test report", "docs/contract_test_reports/repo_wide_hardening_report_generator.md"),
    ("generated status report", APPROVED_STATUS_REPORT),
    ("repo-local tool", "tools/check_secret_patterns.py"),
    ("repo-local tool", "tools/check_agent_docs.py"),
    ("repo-local tool", "tools/check_protected_surfaces.py"),
    ("repo-local tool", "tools/check_surface_authorization.py"),
    ("repo-local tool", "tools/select_validation.py"),
    ("repo-local tool", "tools/run_pyright_advisory_report.py"),
    ("repo-local tool", GENERATOR_PATH),
)

EXPECTED_VALIDATION_COMMANDS = (
    r"py -m pytest -q tests\test_hardening_report_generator.py",
    r"py tools\generate_hardening_report.py",
    r"py tools\generate_hardening_report.py --output docs\contract_test_reports\repo_wide_hardening_status_report.md",
    "py -m ruff check src tests tools",
    "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run",
    "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run",
    (
        "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run "
        "--authorization-file issue=.tmp\\issue-100.md "
        "--authorization-file contract=docs\\contracts\\repo_wide_hardening_report_generator.md "
        "--authorization-file handoff=docs\\implementation_handoffs\\repo_wide_hardening_report_generator_comparison.md"
    ),
    "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run",
    "git diff --check",
)

_SCRIPT_HOST = "script" + r"\.google" + r"\.com"
_DOCS_HOST = "docs" + r"\.google" + r"\.com"
_WEBHOOK_RE = re.compile(
    r"https://" + _SCRIPT_HOST + r"/macros/s/[A-Za-z0-9_-]{20,}/exec(?:\?[^\s\"'<>)]*)?",
)
_DOC_ID_RE = re.compile(
    r"https://" + _DOCS_HOST + r"/(?:spreadsheets|document|presentation)/d/[A-Za-z0-9_-]{20,}",
)
_WINDOWS_USER_PATH_RE = re.compile(
    r"(?i)[A-Za-z]:[\\/]+Users[\\/]+[^\\/:\r\n\"'<>{}]+(?:[\\/]+[^\r\n\"'<>]*)?",
)
_UNIX_USER_PATH_RE = re.compile(r"/(?:Users|home)/[^/\s\"'<>{}]+(?:/[^\s\"'<>]*)?")
_AUTH_HEADER_RE = re.compile(
    r"(?i)(Authorization\s*:\s*(?:Bearer|Basic|Token)\s+)([A-Za-z0-9._~+/=-]{8,})",
)
_CREDENTIAL_ASSIGNMENT_RE = re.compile(
    r"(?ix)"
    r"\b("
    r"api[_-]?key|apikey|access[_-]?token|refresh[_-]?token|id[_-]?token|auth[_-]?token|"
    r"oauth[_-]?token|token|client[_-]?secret|password|secret|webhook[_-]?url"
    r")\b\s*[:=]\s*(?P<quote>[\"']?)(?P<value>[^\"'\s,;}{]{8,})",
)
_SPREADSHEET_ID_RE = re.compile(
    r"(?i)\b(spreadsheet(?:_?id)?|spreadsheetId|workbook(?:_?id)?|deployment(?:_?id)?)\b"
    r"\s*[:=]\s*[\"']?[A-Za-z0-9_-]{20,}",
)
_GOOGLE_BARE_ID_CANDIDATE_RE = re.compile(r"(?<![A-Za-z0-9_-])([A-Za-z0-9_-]{25,})(?![A-Za-z0-9_-])")
_GIT_SHA_RE = re.compile(r"(?i)[0-9a-f]{40}")
_PRIVATE_KEY_MARKER_RE = re.compile(r"-{5}BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-{5}")
_RAW_LOG_MARKERS = tuple(
    "".join(parts)
    for parts in (
        ("[", "Unity", "CrossThreadLogger", "]"),
        ("[", "Client", " GRE", "]"),
        ("ClientTo", "GRE", "Message"),
        ("ClientTo", "Gre", "message"),
        ("GRE", "Message", "Type_"),
    )
)
_PRIVATE_ARTIFACT_MARKERS = (
    "failed" + "_posts",
    "failed post",
    "queued_webhook",
    "runtime status",
    "runtime" + "_status",
    "status_latest",
    "webhook_successes",
    "webhook_failures",
    "oracle" + "_id",
    "scryfall",
    "tier_snapshot",
)


class ConfigError(Exception):
    """Configuration error that should exit 2 without writing output."""


@dataclass(frozen=True)
class ArtifactStatus:
    group: str
    path: str
    status: str
    source: str = "repo_local_artifact"
    confidence: str = "inferred_from_presence"
    finality: str = "unknown"


@dataclass(frozen=True)
class EvidenceItem:
    label: str
    status: str
    source: str
    confidence: str
    finality: str
    summary: str


@dataclass(frozen=True)
class ManifestData:
    tracker: str
    source_issue: str
    branch: str
    head: str
    issues: tuple[dict[str, str], ...]
    pull_requests: tuple[dict[str, str], ...]
    validation: tuple[dict[str, str], ...]
    ci: tuple[dict[str, str], ...]
    residual_risks: tuple[dict[str, str], ...]
    next_recommended_role: str
    ignored_fields: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class ReportModel:
    repo_root: Path
    artifacts: tuple[ArtifactStatus, ...]
    manifest: ManifestData | None
    missing_evidence: tuple[EvidenceItem, ...]


def normalize_repo_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    text = text.lstrip("/")
    parts = [part for part in text.split("/") if part and part != "."]
    return "/".join(parts)


def _repo_relative_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError as exc:
        raise ConfigError(f"output path is outside the repository root: {path}") from exc


def redact_text(value: object) -> str:
    text = str(value)
    redacted = text

    home = str(Path.home())
    for home_text in {home, home.replace("\\", "/")}:
        if home_text:
            redacted = redacted.replace(home_text, "<redacted-local-path>")

    if any(marker in redacted for marker in _RAW_LOG_MARKERS):
        return "<redacted-raw-log-content>"
    lowered = redacted.lower()
    if any(marker in lowered for marker in _PRIVATE_ARTIFACT_MARKERS) and ("{" in redacted or "payload" in lowered):
        return "<redacted-private-artifact>"

    redacted = _WEBHOOK_RE.sub("<redacted-webhook-url>", redacted)
    redacted = _DOC_ID_RE.sub("<redacted-workbook-or-document-url>", redacted)
    redacted = _SPREADSHEET_ID_RE.sub(
        lambda match: f"{match.group(1)}=<redacted-workbook-or-deployment-id>",
        redacted,
    )
    redacted = _GOOGLE_BARE_ID_CANDIDATE_RE.sub(_redact_google_bare_id_candidate, redacted)
    redacted = _AUTH_HEADER_RE.sub(lambda match: f"{match.group(1)}<redacted-secret>", redacted)
    redacted = _CREDENTIAL_ASSIGNMENT_RE.sub(lambda match: f"{match.group(1)}=<redacted-secret>", redacted)
    redacted = _PRIVATE_KEY_MARKER_RE.sub("<redacted-secret>", redacted)
    redacted = _WINDOWS_USER_PATH_RE.sub("<redacted-local-path>", redacted)
    redacted = _UNIX_USER_PATH_RE.sub("<redacted-local-path>", redacted)
    return redacted


def _redact_google_bare_id_candidate(match: re.Match[str]) -> str:
    candidate = match.group(1)
    if _looks_like_google_bare_id(candidate):
        return "<redacted-google-id>"
    return candidate


def _looks_like_google_bare_id(candidate: str) -> bool:
    if candidate.startswith("AKfycb"):
        return True
    if _GIT_SHA_RE.fullmatch(candidate):
        return False
    has_upper = any(char.isupper() for char in candidate)
    has_lower = any(char.islower() for char in candidate)
    has_digit = any(char.isdigit() for char in candidate)
    has_urlsafe_separator = "-" in candidate or "_" in candidate
    if candidate.startswith(("1", "0")) and has_upper and has_lower:
        return True
    return len(candidate) >= 30 and has_upper and has_lower and (has_digit or has_urlsafe_separator)


def _sanitize_scalar(value: object) -> str:
    return redact_text(value).replace("\r", " ").replace("\n", " ").strip()


def _table_cell(value: object) -> str:
    text = _sanitize_scalar(value)
    return text.replace("|", r"\|") or "not_supplied"


def _safe_source(value: object, default: str, warnings: list[str]) -> str:
    source = _sanitize_scalar(value)
    if not source:
        return default
    if source in SOURCE_LABELS:
        return source
    warnings.append(f"Unsupported source label rendered as {default}: {source}")
    return default


def _safe_status(value: object, warnings: list[str]) -> str:
    status = _sanitize_scalar(value).lower()
    if status in ALLOWED_STATUSES:
        return status
    if status:
        warnings.append(f"Unsupported status rendered as unknown: {status}")
    return "unknown"


def _safe_state(value: object, warnings: list[str]) -> str:
    state = _sanitize_scalar(value).lower()
    if state in ALLOWED_STATES:
        return state
    if state:
        warnings.append(f"Unsupported issue or PR state rendered as unknown: {state}")
    return "unknown"


def _safe_list(payload: dict[str, Any], field: str, warnings: list[str]) -> list[dict[str, Any]]:
    value = payload.get(field, [])
    if value is None:
        return []
    if not isinstance(value, list):
        warnings.append(f"Manifest field ignored because it is not a list: {field}")
        return []
    items: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if isinstance(item, dict):
            items.append(item)
        else:
            warnings.append(f"Manifest list item ignored because it is not an object: {field}[{index}]")
    return items


def load_evidence_manifest(path: str | Path | None) -> ManifestData | None:
    if path is None:
        return None
    manifest_path = Path(path)
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"malformed evidence manifest: {manifest_path}") from exc
    except OSError as exc:
        raise ConfigError(f"unable to read evidence manifest: {manifest_path}") from exc
    if not isinstance(payload, dict):
        raise ConfigError("evidence manifest must be a JSON object")

    warnings: list[str] = []
    expected_fields = {
        "object",
        "schema_version",
        "tracker",
        "source_issue",
        "branch",
        "head",
        "issues",
        "pull_requests",
        "validation",
        "ci",
        "residual_risks",
        "next_recommended_role",
    }
    ignored_fields = tuple(sorted(_sanitize_scalar(key) for key in set(payload) - expected_fields))

    issues: list[dict[str, str]] = []
    for item in _safe_list(payload, "issues", warnings):
        state = _safe_state(item.get("state", "unknown"), warnings)
        issues.append(
            {
                "number": _sanitize_scalar(item.get("number", "not_supplied")),
                "url": _sanitize_scalar(item.get("url", "not_supplied")),
                "state": state,
                "role": _sanitize_scalar(item.get("role", "not_supplied")),
                "note": _sanitize_scalar(item.get("note", "not_supplied")),
                "source": _safe_source(item.get("source", "operator_supplied"), "operator_supplied", warnings),
                "confidence": "reported",
                "finality": "lifecycle_open" if state == "open" else "final" if state == "closed" else "unknown",
            },
        )

    pull_requests: list[dict[str, str]] = []
    for item in _safe_list(payload, "pull_requests", warnings):
        state = _safe_state(item.get("state", "unknown"), warnings)
        pull_requests.append(
            {
                "number": _sanitize_scalar(item.get("number", "not_supplied")),
                "url": _sanitize_scalar(item.get("url", "not_supplied")),
                "state": state,
                "base": _sanitize_scalar(item.get("base", "not_supplied")),
                "merge_commit": _sanitize_scalar(item.get("merge_commit", "not_supplied")),
                "source": _safe_source(item.get("source", "pr_metadata"), "pr_metadata", warnings),
                "confidence": "reported",
                "finality": "final" if state == "merged" else "pending_review" if state == "draft" else "unknown",
            },
        )

    validation: list[dict[str, str]] = []
    for item in _safe_list(payload, "validation", warnings):
        validation.append(
            {
                "command": _sanitize_scalar(item.get("command", "not_supplied")),
                "status": _safe_status(item.get("status", "unknown"), warnings),
                "summary": _sanitize_scalar(item.get("summary", "not_supplied")),
                "source": _safe_source(item.get("source", "operator_supplied"), "operator_supplied", warnings),
                "confidence": "reported",
                "finality": "advisory" if item.get("status") == "advisory" else "final",
            },
        )

    ci: list[dict[str, str]] = []
    for item in _safe_list(payload, "ci", warnings):
        ci.append(
            {
                "context": _sanitize_scalar(item.get("context", "not_supplied")),
                "status": _safe_status(item.get("status", "unknown"), warnings),
                "source": _safe_source(item.get("source", "ci_summary"), "ci_summary", warnings),
                "confidence": "reported",
                "finality": "final",
            },
        )

    residual_risks: list[dict[str, str]] = []
    for item in _safe_list(payload, "residual_risks", warnings):
        residual_risks.append(
            {
                "risk": _sanitize_scalar(item.get("risk", "not_supplied")),
                "severity": _sanitize_scalar(item.get("severity", "unknown")),
                "source": _safe_source(item.get("source", "operator_supplied"), "operator_supplied", warnings),
                "confidence": "reported",
                "finality": "unknown",
            },
        )

    return ManifestData(
        tracker=_sanitize_scalar(payload.get("tracker", TRACKER_URL)),
        source_issue=_sanitize_scalar(payload.get("source_issue", SOURCE_ISSUE_URL)),
        branch=_sanitize_scalar(payload.get("branch", BRANCH_NAME)),
        head=_sanitize_scalar(payload.get("head", "not_supplied")),
        issues=tuple(sorted(issues, key=lambda item: (item["number"], item["url"]))),
        pull_requests=tuple(sorted(pull_requests, key=lambda item: (item["number"], item["url"]))),
        validation=tuple(sorted(validation, key=lambda item: item["command"])),
        ci=tuple(sorted(ci, key=lambda item: item["context"])),
        residual_risks=tuple(sorted(residual_risks, key=lambda item: (item["severity"], item["risk"]))),
        next_recommended_role=_sanitize_scalar(payload.get("next_recommended_role", DEFAULT_NEXT_ROLE))
        or DEFAULT_NEXT_ROLE,
        ignored_fields=ignored_fields,
        warnings=tuple(sorted(warnings)),
    )


def validate_output_path(repo_root: str | Path, output: str | Path) -> Path:
    root = Path(repo_root).resolve()
    raw_output = Path(output)
    target = raw_output if raw_output.is_absolute() else root / raw_output
    relative = _repo_relative_path(target, root)
    normalized = normalize_repo_path(relative)
    if not normalized.startswith(APPROVED_OUTPUT_PREFIX) or not normalized.endswith(".md"):
        raise ConfigError("output path must be a Markdown file under docs/contract_test_reports/")
    return target


def collect_artifact_inventory(
    repo_root: str | Path,
    *,
    output_path: str | Path | None = None,
) -> tuple[ArtifactStatus, ...]:
    root = Path(repo_root).resolve()
    output_relative = ""
    if output_path is not None:
        output_candidate = Path(output_path)
        if not output_candidate.is_absolute():
            output_candidate = root / output_candidate
        output_relative = normalize_repo_path(_repo_relative_path(output_candidate, root))
    artifacts: list[ArtifactStatus] = []
    for group, artifact_path in ARTIFACT_GROUPS:
        exists = (root / artifact_path).exists() or artifact_path == output_relative
        artifacts.append(ArtifactStatus(group=group, path=artifact_path, status="present" if exists else "missing"))
    return tuple(sorted(artifacts, key=lambda item: item.path))


def _missing_item(label: str, summary: str) -> EvidenceItem:
    return EvidenceItem(
        label=label,
        status="not_supplied",
        source="missing",
        confidence="missing",
        finality="unknown",
        summary=summary,
    )


def collect_missing_evidence(
    *,
    artifacts: tuple[ArtifactStatus, ...],
    manifest: ManifestData | None,
) -> tuple[EvidenceItem, ...]:
    missing: list[EvidenceItem] = []
    if manifest is None:
        missing.append(_missing_item("evidence manifest", "No operator-supplied evidence manifest was provided."))
        supplied_validation: set[str] = set()
    else:
        supplied_validation = {item["command"] for item in manifest.validation}
        if not manifest.issues:
            missing.append(_missing_item("issue state", "Issue lifecycle evidence was not supplied."))
        if not manifest.pull_requests:
            missing.append(_missing_item("PR state", "Pull request lifecycle evidence was not supplied."))
        if not manifest.ci:
            missing.append(_missing_item("CI status", "CI evidence was not supplied."))
        if not manifest.validation:
            missing.append(_missing_item("validation results", "Validation command evidence was not supplied."))

    for command in EXPECTED_VALIDATION_COMMANDS:
        if command not in supplied_validation:
            missing.append(_missing_item(f"validation: {command}", "Command result was not supplied."))

    required_fragments = (
        ("protected-surface command result", "check_protected_surfaces.py"),
        ("secret/private-marker command result", "check_secret_patterns.py"),
        ("surface-authorization command result", "check_surface_authorization.py"),
        ("Pyright advisory result", "run_pyright_advisory_report.py"),
    )
    for label, fragment in required_fragments:
        if not any(fragment in item for item in supplied_validation):
            missing.append(_missing_item(label, "Specific tool result was not supplied."))

    for artifact in artifacts:
        if artifact.status == "missing":
            missing.append(_missing_item(f"artifact: {artifact.path}", f"{artifact.group} artifact is missing."))

    return tuple(sorted(missing, key=lambda item: item.label))


def build_report(
    *,
    repo_root: str | Path = ".",
    evidence_manifest: str | Path | None = None,
    output_path: str | Path | None = None,
) -> ReportModel:
    root = Path(repo_root).resolve()
    if not root.exists() or not root.is_dir():
        raise ConfigError(f"unreadable repo root: {repo_root}")
    manifest = load_evidence_manifest(evidence_manifest)
    artifacts = collect_artifact_inventory(root, output_path=output_path)
    missing = collect_missing_evidence(artifacts=artifacts, manifest=manifest)
    return ReportModel(repo_root=root, artifacts=artifacts, manifest=manifest, missing_evidence=missing)


def _render_artifact_table(artifacts: tuple[ArtifactStatus, ...]) -> list[str]:
    lines = ["| Path | Group | Status | Source | Confidence |", "| --- | --- | --- | --- | --- |"]
    for artifact in artifacts:
        lines.append(
            "| "
            + " | ".join(
                (
                    _table_cell(artifact.path),
                    _table_cell(artifact.group),
                    _table_cell(artifact.status),
                    _table_cell(artifact.source),
                    _table_cell(artifact.confidence),
                ),
            )
            + " |",
        )
    return lines


def _render_evidence_rows(items: tuple[dict[str, str], ...], fields: tuple[str, ...]) -> list[str]:
    if not items:
        return ["- not_supplied source=missing confidence=missing finality=unknown"]
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for item in items:
        lines.append("| " + " | ".join(_table_cell(item.get(field, "not_supplied")) for field in fields) + " |")
    return lines


def _validation_rows(manifest: ManifestData | None) -> tuple[dict[str, str], ...]:
    supplied = {item["command"]: item for item in manifest.validation} if manifest else {}
    rows: list[dict[str, str]] = []
    for command in EXPECTED_VALIDATION_COMMANDS:
        item = supplied.get(command)
        if item is None:
            rows.append(
                {
                    "command": command,
                    "status": "not_supplied",
                    "source": "missing",
                    "confidence": "missing",
                    "finality": "unknown",
                    "summary": "not_run",
                },
            )
        else:
            rows.append(item)
    for command, item in sorted(supplied.items()):
        if command not in EXPECTED_VALIDATION_COMMANDS:
            rows.append(item)
    return tuple(rows)


def _rows_matching_validation(manifest: ManifestData | None, fragments: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    rows = [
        item
        for item in _validation_rows(manifest)
        if any(fragment in item["command"] or fragment in item["summary"] for fragment in fragments)
    ]
    return tuple(rows)


def render_markdown(report: ReportModel) -> str:
    manifest = report.manifest
    tracker = manifest.tracker if manifest else TRACKER_URL
    source_issue = manifest.source_issue if manifest else SOURCE_ISSUE_URL
    branch = manifest.branch if manifest else BRANCH_NAME
    next_role = manifest.next_recommended_role if manifest else DEFAULT_NEXT_ROLE

    completed_or_merged: list[dict[str, str]] = []
    open_lifecycle: list[dict[str, str]] = []
    if manifest:
        completed_or_merged.extend(item for item in manifest.issues if item["state"] == "closed")
        completed_or_merged.extend(item for item in manifest.pull_requests if item["state"] == "merged")
        open_lifecycle.extend(item for item in manifest.issues if item["state"] == "open")
        open_lifecycle.extend(item for item in manifest.pull_requests if item["state"] in {"draft", "ready_for_review"})

    missing_rows = tuple(
        {
            "label": item.label,
            "status": item.status,
            "source": item.source,
            "confidence": item.confidence,
            "finality": item.finality,
            "summary": item.summary,
        }
        for item in report.missing_evidence
    )

    lines = [
        "# Repo-Wide Hardening Status Report",
        "",
        f"report_kind: {REPORT_KIND}",
        f"schema_version: {REPORT_SCHEMA_VERSION}",
        f"generator: {GENERATOR_PATH}",
        f"tracker: {tracker}",
        f"source_issue: {source_issue}",
        f"branch: {branch}",
        f"evidence_mode: {EVIDENCE_MODE}",
        f"merge_readiness: {NOT_DECIDED}",
        f"deploy_readiness: {NOT_DECIDED}",
        f"tracker_completion: {NOT_DECIDED}",
        "",
        "## Evidence Sources",
        "",
        "- repo_local_artifact: repository file presence only; not validation success.",
        "- operator_supplied: optional evidence manifest input.",
        "- tool_report: reserved for explicitly supplied tool-report evidence.",
        "- tracker_comment: reserved for explicitly supplied tracker comment evidence.",
        "- pr_metadata: reserved for explicitly supplied PR metadata.",
        "- ci_summary: reserved for explicitly supplied CI summary evidence.",
        "- missing: evidence was not supplied or the artifact is absent.",
        "- confidence labels: confirmed, reported, inferred_from_presence, missing, unknown.",
        "- finality labels: final, advisory, lifecycle_open, pending_review, unknown.",
        "- This report does not decide merge readiness, deploy readiness, issue closure, or tracker completion.",
        "- This status report is not the future post-hardening comparison report.",
        "",
        "## Artifact Inventory",
        "",
        *_render_artifact_table(report.artifacts),
        "",
        "## Completed Or Merged Items",
        "",
        *_render_evidence_rows(
            tuple(completed_or_merged),
            ("number", "url", "state", "source", "confidence", "finality", "note"),
        ),
        "",
        "## Open Lifecycle Items",
        "",
        *_render_evidence_rows(
            tuple(open_lifecycle),
            ("number", "url", "state", "source", "confidence", "finality", "note"),
        ),
        "",
        "## Validation Evidence",
        "",
        *_render_evidence_rows(
            _validation_rows(manifest),
            ("command", "status", "source", "confidence", "finality", "summary"),
        ),
        "",
        "CI summary evidence:",
        "",
        *_render_evidence_rows(
            manifest.ci if manifest else (),
            ("context", "status", "source", "confidence", "finality"),
        ),
        "",
        "## Tool Evidence",
        "",
        *_render_artifact_table(tuple(item for item in report.artifacts if item.group == "repo-local tool")),
        "",
        "## Protected Surface And Secret Scan Evidence",
        "",
        *_render_evidence_rows(
            _rows_matching_validation(
                manifest,
                ("check_protected_surfaces.py", "check_secret_patterns.py", "check_surface_authorization.py"),
            ),
            ("command", "status", "source", "confidence", "finality", "summary"),
        ),
        "",
        "## Pyright Advisory Evidence",
        "",
        *_render_evidence_rows(
            _rows_matching_validation(manifest, ("run_pyright_advisory_report.py", "pyright")),
            ("command", "status", "source", "confidence", "finality", "summary"),
        ),
        "",
        "## Golden Fixture And Drift Baseline Status",
        "",
        *_render_artifact_table(
            tuple(
                item
                for item in report.artifacts
                if "golden_fixture" in item.path or "drift_detector" in item.path
            ),
        ),
        "",
        "## Missing Evidence",
        "",
        *_render_evidence_rows(
            missing_rows,
            ("label", "status", "source", "confidence", "finality", "summary"),
        ),
        "",
        "## Residual Risks",
        "",
    ]
    if manifest and manifest.residual_risks:
        lines.extend(
            _render_evidence_rows(
                manifest.residual_risks,
                ("risk", "severity", "source", "confidence", "finality"),
            ),
        )
    else:
        lines.append("- not_supplied source=missing confidence=missing finality=unknown")
    if manifest and (manifest.warnings or manifest.ignored_fields):
        lines.extend(["", "Manifest configuration notes:"])
        for warning in manifest.warnings:
            lines.append(f"- warning: {_table_cell(warning)}")
        for field in manifest.ignored_fields:
            lines.append(f"- ignored_field: {_table_cell(field)}")
    lines.extend(
        [
            "",
            "## Next Recommended Role",
            "",
            f"- {next_role}",
            "",
            "## Workflow Handoff",
            "",
            "```yaml",
            "workflow_handoff:",
            f'  issue: "{source_issue}"',
            f'  tracker: "{tracker}"',
            '  completed_thread: "C"',
            '  next_thread: "E"',
            f'  next_role: "{next_role}"',
            '  source_artifact: "docs/contracts/repo_wide_hardening_report_generator.md"',
            '  target_artifact: "docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md"',
            '  expected_review_artifact: "docs/contract_test_reports/repo_wide_hardening_report_generator.md"',
            f'  generated_status_report: "{APPROVED_STATUS_REPORT}"',
            '  risk_tier: "Medium"',
            f'  branch: "{branch}"',
            "  readiness:",
            f'    merge_readiness: "{NOT_DECIDED}"',
            f'    deploy_readiness: "{NOT_DECIDED}"',
            f'    tracker_completion: "{NOT_DECIDED}"',
            "  stop_conditions:",
            '    - "Do not treat this generated report as merge or deploy approval."',
            '    - "Do not close #96, #98, #100, or tracker #82 from this report."',
            "```",
            "",
        ],
    )
    return "\n".join(lines)


def write_report(output_path: Path, content: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_name(f"{output_path.name}.tmp")
    temp_path.write_text(content, encoding="utf-8", newline="\n")
    temp_path.replace(output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate the Mythic Edge repo-wide hardening status report.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument("--output", help="Optional Markdown output path under docs/contract_test_reports/.")
    parser.add_argument("--evidence-manifest", help="Optional JSON evidence manifest.")
    parser.add_argument("--format", choices=("markdown",), default="markdown", help="Report format.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    try:
        repo_root = Path(args.repo_root).resolve()
        output_path = validate_output_path(repo_root, args.output) if args.output else None
        report = build_report(
            repo_root=repo_root,
            evidence_manifest=args.evidence_manifest,
            output_path=output_path,
        )
        content = render_markdown(report)
        sys.stdout.write(content)
        if output_path is not None:
            write_report(output_path, content)
    except ConfigError as exc:
        print(f"ERROR configuration - {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR filesystem - {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
