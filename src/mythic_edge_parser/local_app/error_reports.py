from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Protocol
from urllib.parse import urlparse

from .live_watcher_diagnostics import build_live_watcher_diagnostics_status
from .live_watcher_process import build_live_watcher_process_status
from .paths import LocalAppPaths
from .setup_status import (
    build_analytics_database_status,
    build_health_status,
    build_live_player_log_status,
    build_live_sqlite_capture_status,
    build_live_watcher_status,
    build_setup_status,
)

ERROR_REPORT_PREVIEW_SCHEMA = "quality_app_submit_error_report_codex_triage.v1"
ERROR_REPORT_PREVIEW_STATUS_READY = "preview_ready"
ERROR_REPORT_PREVIEW_STATUS_INVALID = "invalid_request"
ERROR_REPORT_PREVIEW_STATUS_BLOCKED = "blocked_privacy_guard"
ERROR_REPORT_SUBMISSION_OBJECT = "mythic_edge_local_app_error_report_submission"
ERROR_REPORT_SUBMISSION_SCHEMA = "quality_app_error_report_github_submission.v1"
ERROR_REPORT_REPO = "Tahjali11/Mythic-Edge"

ALLOWED_AFFECTED_AREAS = {
    "local_app_ui",
    "install_launch",
    "manual_import",
    "analytics",
    "live_player_log",
    "match_journal",
    "parser",
    "privacy",
    "unknown",
}
ALLOWED_SEVERITIES = {"blocker", "degraded", "annoyance", "question"}
ALLOWED_REPORT_TYPES = {"bug", "feedback", "feature_request"}
BASELINE_LABELS = {"workflow:problem", "layer:dashboard"}
REPORT_TYPE_LABELS = {
    "bug": ("bug", "bug"),
    "feedback": ("feedback", "question"),
    "feature_request": ("feature-request", "enhancement"),
}

EXCLUDED_PRIVATE_DATA = [
    "raw Player.log contents or raw log lines",
    "raw JSONL payloads or saved-event lines",
    "SQLite database contents, WAL, SHM, or journal files",
    "runtime logs and transport-failure payloads",
    "workbook exports",
    "screenshots or attachments",
    "full private local paths",
    "raw hashes of private files",
    "secrets, credentials, tokens, API keys, OAuth material, endpoint values, spreadsheet IDs, and environment values",
    "arbitrary local files and generated/private/local-only artifacts",
]

_BUG_FIELDS = ("expected_behavior", "actual_behavior")
_OPTIONAL_BUG_FIELDS = ("reproduction_steps",)
_FEEDBACK_FIELDS = ("feedback",)
_FEATURE_REQUEST_FIELDS = ("feature_goal", "feature_location", "feature_success")
_REPORT_FREEFORM_FIELDS = ("summary", *_BUG_FIELDS, *_OPTIONAL_BUG_FIELDS, *_FEEDBACK_FIELDS, *_FEATURE_REQUEST_FIELDS)
_PRIVATE_PATH_PATTERN = re.compile(
    r"(?:(?<![A-Za-z0-9_])[A-Za-z]:\\[^\r\n\t|<>\"']+"
    r"|/(?:Users|home|private/var|var/folders|tmp|private/tmp|var/tmp)/[^\r\n\t|<>\"']+)"
)
_ENDPOINT_PATTERN = re.compile(r"\b(?:https?|ftp)://\S+", re.IGNORECASE)
_SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"\b(?:api[_-]?key|token|secret|oauth|webhook|spreadsheet[_-]?id|endpoint)\b\s*[:=]\s*\S+",
    re.IGNORECASE,
)
_TOKEN_PATTERN = re.compile(r"\b(?:ghp|github_pat|sk|xox[baprs])-[-A-Za-z0-9_]{8,}\b", re.IGNORECASE)
_HASH_PATTERN = re.compile(r"\b[a-fA-F0-9]{32,64}\b")


class GitHubIssueSubmitter(Protocol):
    def available_labels(self) -> set[str]:
        ...

    def create_issue(self, *, title: str, body: str, labels: Sequence[str]) -> tuple[str | None, int | None]:
        ...


class GitHubSubmitterError(Exception):
    status: str

    def __init__(self, status: str) -> None:
        super().__init__(status)
        self.status = status


class GhCliIssueSubmitter:
    def __init__(self, *, repo: str = ERROR_REPORT_REPO, timeout_seconds: int = 10) -> None:
        self.repo = repo
        self.timeout_seconds = timeout_seconds

    def available_labels(self) -> set[str]:
        gh_path = shutil.which("gh")
        if gh_path is None:
            raise GitHubSubmitterError("blocked_missing_gh")
        auth = subprocess.run(
            [gh_path, "auth", "status", "--hostname", "github.com"],
            capture_output=True,
            shell=False,
            text=True,
            timeout=self.timeout_seconds,
        )
        if auth.returncode != 0:
            raise GitHubSubmitterError("blocked_gh_unauthenticated")
        labels = subprocess.run(
            [gh_path, "label", "list", "--repo", self.repo, "--limit", "100"],
            capture_output=True,
            shell=False,
            text=True,
            timeout=self.timeout_seconds,
        )
        if labels.returncode != 0:
            raise GitHubSubmitterError("blocked_wrong_repo")
        return {line.split("\t", 1)[0].strip() for line in labels.stdout.splitlines() if line.strip()}

    def create_issue(self, *, title: str, body: str, labels: Sequence[str]) -> tuple[str | None, int | None]:
        gh_path = shutil.which("gh")
        if gh_path is None:
            raise GitHubSubmitterError("blocked_missing_gh")
        with tempfile.TemporaryDirectory(prefix="mythic-edge-error-report-") as temp_dir:
            body_path = Path(temp_dir) / "issue-body.md"
            body_path.write_text(body, encoding="utf-8")
            command = [
                gh_path,
                "issue",
                "create",
                "--repo",
                self.repo,
                "--title",
                title,
                "--body-file",
                str(body_path),
            ]
            for label in labels:
                command.extend(["--label", label])
            result = subprocess.run(
                command,
                capture_output=True,
                shell=False,
                text=True,
                timeout=self.timeout_seconds,
            )
        if result.returncode != 0:
            raise GitHubSubmitterError("submission_failed")
        return _parse_github_issue_url(result.stdout)


def build_error_report_preview(request: object, paths: LocalAppPaths) -> dict[str, object]:
    return _build_error_report_preview(request, paths, external_submission_enabled=True)


def build_error_report_submission(
    request: object,
    paths: LocalAppPaths,
    *,
    submitter: GitHubIssueSubmitter | None = None,
) -> dict[str, object]:
    preview = _build_error_report_preview(request, paths, external_submission_enabled=True)
    if preview["status"] == ERROR_REPORT_PREVIEW_STATUS_INVALID:
        return _submission_response("invalid_request", preview=preview, errors=list(preview["warnings"]))
    if preview["status"] == ERROR_REPORT_PREVIEW_STATUS_BLOCKED:
        return _submission_response("blocked_privacy_guard", preview=preview, errors=list(preview["warnings"]))
    if preview["status"] != ERROR_REPORT_PREVIEW_STATUS_READY:
        return _submission_response("preview_required", preview=preview, errors=["preview_not_ready"])

    report_type = _report_type_from_request(request)
    submitter = submitter or GhCliIssueSubmitter()
    try:
        labels = _labels_for_report(report_type, submitter.available_labels())
        issue_url, issue_number = submitter.create_issue(
            title=str(preview["issue_title"]),
            body=str(preview["issue_body_markdown"]),
            labels=labels,
        )
    except GitHubSubmitterError as error:
        return _submission_response(error.status, preview=preview, errors=[error.status])
    except (OSError, subprocess.SubprocessError, TimeoutError):
        return _submission_response("submission_failed", preview=preview, errors=["submission_failed"])

    if not _is_expected_issue_url(issue_url):
        return _submission_response("blocked_wrong_repo", preview=preview, errors=["unexpected_issue_url"])

    return _submission_response(
        "submitted",
        preview=preview,
        labels=labels,
        issue_url=issue_url,
        issue_number=issue_number,
        submitted=True,
    )


def _build_error_report_preview(
    request: object,
    paths: LocalAppPaths,
    *,
    external_submission_enabled: bool,
) -> dict[str, object]:
    if not isinstance(request, Mapping):
        return _response(
            ERROR_REPORT_PREVIEW_STATUS_INVALID,
            warnings=["request_body_must_be_object"],
            external_submission_enabled=False,
        )

    fields: dict[str, str] = {}
    invalid_fields: list[str] = []
    blocked_fields: list[str] = []
    total_redactions = 0
    redaction_fields: list[str] = []

    report_type = request.get("report_type", "bug")
    if not isinstance(report_type, str) or report_type not in ALLOWED_REPORT_TYPES:
        invalid_fields.append("report_type")
        report_type = "bug"

    required_fields = _required_fields_for_report_type(report_type)
    optional_fields = set(_optional_fields_for_report_type(report_type))
    for field in ("summary", *required_fields, *optional_fields):
        raw_value = request.get(field)
        if field in optional_fields and (raw_value is None or raw_value == ""):
            fields[field] = ""
            continue
        if not isinstance(raw_value, str) or not raw_value.strip():
            invalid_fields.append(field)
            continue
        if _contains_blocked_value(raw_value):
            blocked_fields.append(field)
            continue
        redacted_value, redaction_count = _redact_private_paths(raw_value.strip())
        fields[field] = redacted_value
        total_redactions += redaction_count
        if redaction_count:
            redaction_fields.append(field)

    affected_area = request.get("affected_area")
    if not isinstance(affected_area, str) or affected_area not in ALLOWED_AFFECTED_AREAS:
        invalid_fields.append("affected_area")

    severity = request.get("severity", "degraded")
    if not isinstance(severity, str) or severity not in ALLOWED_SEVERITIES:
        invalid_fields.append("severity")

    frontend_surface = request.get("current_frontend_surface", "local_app_cockpit")
    if not isinstance(frontend_surface, str):
        invalid_fields.append("current_frontend_surface")
    elif _contains_blocked_value(frontend_surface):
        blocked_fields.append("current_frontend_surface")
    else:
        frontend_surface, redaction_count = _redact_private_paths(frontend_surface.strip() or "local_app_cockpit")
        total_redactions += redaction_count
        if redaction_count:
            redaction_fields.append("current_frontend_surface")

    if blocked_fields:
        return _response(
            ERROR_REPORT_PREVIEW_STATUS_BLOCKED,
            warnings=[f"privacy_guard_blocked:{field}" for field in blocked_fields],
            external_submission_enabled=False,
        )

    if invalid_fields:
        return _response(
            ERROR_REPORT_PREVIEW_STATUS_INVALID,
            warnings=[f"invalid_field:{field}" for field in invalid_fields],
            external_submission_enabled=False,
        )

    diagnostics = _build_diagnostic_packet(paths)
    included_categories = [str(entry["category"]) for entry in diagnostics]
    redaction_summary = _redaction_summary(total_redactions, redaction_fields)
    issue_title = _issue_title(fields["summary"], affected_area, report_type)
    issue_body_markdown = _issue_body_markdown(
        issue_title=issue_title,
        fields=fields,
        affected_area=affected_area,
        report_type=report_type,
        severity=severity,
        frontend_surface=frontend_surface,
        diagnostics=diagnostics,
        included_categories=included_categories,
        redaction_summary=redaction_summary,
    )

    return _response(
        ERROR_REPORT_PREVIEW_STATUS_READY,
        issue_title=issue_title,
        issue_body_markdown=issue_body_markdown,
        included_diagnostic_categories=included_categories,
        redaction_summary=redaction_summary,
        external_submission_enabled=external_submission_enabled,
    )


def _response(
    status: str,
    *,
    issue_title: str = "",
    issue_body_markdown: str = "",
    included_diagnostic_categories: list[str] | None = None,
    redaction_summary: list[str] | None = None,
    warnings: list[str] | None = None,
    external_submission_enabled: bool,
) -> dict[str, object]:
    return {
        "schema": ERROR_REPORT_PREVIEW_SCHEMA,
        "status": status,
        "issue_title": issue_title,
        "issue_body_markdown": issue_body_markdown,
        "included_diagnostic_categories": included_diagnostic_categories or [],
        "excluded_private_data": list(EXCLUDED_PRIVATE_DATA),
        "redaction_summary": redaction_summary or [],
        "warnings": warnings or [],
        "next_recommended_role": "Codex A or Codex B after reviewing the sanitized report",
        "external_submission_enabled": external_submission_enabled,
    }


def _submission_response(
    status: str,
    *,
    preview: Mapping[str, object],
    labels: Sequence[str] | None = None,
    issue_url: str | None = None,
    issue_number: int | None = None,
    submitted: bool = False,
    errors: Sequence[str] | None = None,
) -> dict[str, object]:
    ready = preview.get("status") == ERROR_REPORT_PREVIEW_STATUS_READY
    return {
        "object": ERROR_REPORT_SUBMISSION_OBJECT,
        "schema_version": ERROR_REPORT_SUBMISSION_SCHEMA,
        "status": status,
        "external_submission_enabled": True,
        "submitted": submitted,
        "issue_url": issue_url,
        "issue_number": issue_number,
        "issue_title": str(preview.get("issue_title") or ""),
        "issue_body_markdown": str(preview.get("issue_body_markdown") or ""),
        "labels": list(labels or []),
        "fallback_available": ready,
        "warnings": list(preview.get("warnings", [])) if isinstance(preview.get("warnings"), list) else [],
        "errors": list(errors or []),
    }


def _contains_blocked_value(value: str) -> bool:
    return any(
        pattern.search(value)
        for pattern in (
            _ENDPOINT_PATTERN,
            _SECRET_ASSIGNMENT_PATTERN,
            _TOKEN_PATTERN,
            _HASH_PATTERN,
        )
    )


def _redact_private_paths(value: str) -> tuple[str, int]:
    count = 0

    def replace(_: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return "<redacted_local_path>"

    return _PRIVATE_PATH_PATTERN.sub(replace, value), count


def _redaction_summary(redaction_count: int, fields: list[str]) -> list[str]:
    if redaction_count == 0:
        return ["No user-entered private path redactions were needed."]
    field_list = ", ".join(sorted(set(fields)))
    return [f"Redacted {redaction_count} private path marker(s) from: {field_list}."]


def _build_diagnostic_packet(paths: LocalAppPaths) -> list[dict[str, str]]:
    health = build_health_status()
    setup = build_setup_status(paths)
    player_log = build_live_player_log_status(paths)
    watcher = build_live_watcher_status(paths)
    watcher_process = build_live_watcher_process_status(paths)
    live_capture = build_live_sqlite_capture_status(paths)
    diagnostics = build_live_watcher_diagnostics_status(paths)
    analytics_database = build_analytics_database_status(paths)

    return [
        _diagnostic("backend_health", health, "loopback route status only"),
        _diagnostic("setup_status", setup, "aggregate setup status labels only"),
        _diagnostic("live_player_log_status", player_log, "metadata labels only; no Player.log content"),
        _diagnostic("live_watcher_status", watcher, "readiness labels only; watcher is not started"),
        _diagnostic("live_watcher_process_status", watcher_process, "process-control safeguards only"),
        _diagnostic("live_capture_status", live_capture, "SQLite capture capability labels only"),
        _diagnostic("live_watcher_diagnostics", diagnostics, "diagnostic counts and labels only"),
        _diagnostic("analytics_database_status", analytics_database, "schema/status labels only; no table contents"),
        {
            "category": "privacy_boundary",
            "status": "enforced",
            "schema_version": ERROR_REPORT_PREVIEW_SCHEMA,
            "evidence": "report excludes raw artifacts, full paths, secrets, and external submission",
        },
    ]


def _diagnostic(category: str, payload: Mapping[str, object], evidence: str) -> dict[str, str]:
    schema_version = payload.get("schema_version")
    return {
        "category": category,
        "status": str(payload.get("status", "unknown")),
        "schema_version": str(schema_version) if isinstance(schema_version, str) else "unknown",
        "evidence": evidence,
    }


def _required_fields_for_report_type(report_type: str) -> tuple[str, ...]:
    if report_type == "feedback":
        return _FEEDBACK_FIELDS
    if report_type == "feature_request":
        return _FEATURE_REQUEST_FIELDS
    return _BUG_FIELDS


def _optional_fields_for_report_type(report_type: str) -> tuple[str, ...]:
    if report_type == "bug":
        return _OPTIONAL_BUG_FIELDS
    return ()


def _report_type_from_request(request: object) -> str:
    if isinstance(request, Mapping) and request.get("report_type") in ALLOWED_REPORT_TYPES:
        return str(request["report_type"])
    return "bug"


def _labels_for_report(report_type: str, available_labels: set[str]) -> list[str]:
    preferred, fallback = REPORT_TYPE_LABELS.get(report_type, REPORT_TYPE_LABELS["bug"])
    report_label = preferred if preferred in available_labels else fallback
    required = {report_label, *BASELINE_LABELS}
    missing = required - available_labels
    if missing:
        raise GitHubSubmitterError("blocked_label_unavailable")
    return sorted(required)


def _parse_github_issue_url(output: str) -> tuple[str | None, int | None]:
    for token in output.split():
        if _is_expected_issue_url(token):
            issue_number = token.rstrip("/").rsplit("/", 1)[-1]
            return token.strip(), int(issue_number) if issue_number.isdigit() else None
    return None, None


def _is_expected_issue_url(value: str | None) -> bool:
    if not value:
        return False
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and parsed.netloc == "github.com"
        and parsed.path.startswith(f"/{ERROR_REPORT_REPO}/issues/")
        and parsed.path.rstrip("/").rsplit("/", 1)[-1].isdigit()
    )


def _issue_title(summary: str, affected_area: str, report_type: str) -> str:
    normalized = " ".join(summary.split())
    if len(normalized) > 120:
        normalized = normalized[:117].rstrip() + "..."
    return f"[error-report] [{report_type}] [{affected_area}] {normalized}"


def _issue_body_markdown(
    *,
    issue_title: str,
    fields: Mapping[str, str],
    affected_area: str,
    report_type: str,
    severity: str,
    frontend_surface: str,
    diagnostics: list[dict[str, str]],
    included_categories: list[str],
    redaction_summary: list[str],
) -> str:
    diagnostics_lines = "\n".join(
        f"- `{entry['category']}`: `{entry['status']}` ({entry['evidence']})" for entry in diagnostics
    )
    included_lines = "\n".join(f"- `{category}`" for category in included_categories)
    excluded_lines = "\n".join(f"- {item}" for item in EXCLUDED_PRIVATE_DATA)
    redaction_lines = "\n".join(f"- {item}" for item in redaction_summary)
    triage_prompt = _triage_prompt(affected_area)
    return "\n".join(
        [
            f"# {issue_title}",
            "",
            "## Summary",
            fields["summary"],
            "",
            "## Expected Behavior",
            fields.get("expected_behavior", ""),
            "",
            "## Actual Behavior",
            fields.get("actual_behavior", ""),
            "",
            "## Reproduction Steps",
            fields.get("reproduction_steps", ""),
            "",
            "## Routing",
            f"- Report type: `{report_type}`",
            f"- Affected area: `{affected_area}`",
            f"- Severity: `{severity}`",
            f"- Current frontend surface: `{frontend_surface}`",
            "- Suggested next workflow role: Codex A or Codex B",
            "",
            "## Sanitized Diagnostic Packet",
            diagnostics_lines,
            "",
            "## Included Diagnostic Categories",
            included_lines,
            "",
            "## Excluded Private Data",
            excluded_lines,
            "",
            "## Redaction Summary",
            redaction_lines,
            "",
            "## Pasteable Codex Triage Prompt",
            "```text",
            triage_prompt,
            "```",
        ]
    )


def _triage_prompt(affected_area: str) -> str:
    return "\n".join(
        [
            "Use the Mythic Edge agent constitution.",
            "Use $mythic-edge-workflow.",
            "",
            "Act as Codex A or Codex B for a sanitized local-app error report.",
            f"Affected area: {affected_area}",
            "",
            "Treat this report as triage evidence, not parser, analytics, live watcher, "
            "Match Journal, workbook, or AI truth.",
            "Inspect repo files before proposing fixes.",
            "Do not read private local artifacts unless the user explicitly approves a scoped action.",
            "Preserve parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/"
            "production boundaries.",
        ]
    )
