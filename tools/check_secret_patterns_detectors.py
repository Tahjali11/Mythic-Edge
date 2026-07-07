"""Text detectors for the secret/private marker scanner."""

# ruff: noqa: I001

from __future__ import annotations

import re

try:
    from tools.check_secret_patterns_models import (
        Finding,
        SEVERITY_FORBIDDEN,
        SEVERITY_WARNING,
    )
except ModuleNotFoundError:  # pragma: no cover - used when check_secret_patterns.py is run as a script.
    from check_secret_patterns_models import (
        Finding,
        SEVERITY_FORBIDDEN,
        SEVERITY_WARNING,
    )

MAX_EXCERPT_CHARS = 160

PLACEHOLDER_MARKERS = (
    "example",
    "fake",
    "dummy",
    "placeholder",
    "redacted",
    "test",
    "sample",
    "configured",
    "not-real",
)

SANITIZED_FIXTURE_MARKERS = (
    "sanitized",
    "synthetic",
    "local-user",
    "opponent-user",
    "match-regression-",
    "deck-uuid",
)

WEBHOOK_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"https://script\.google\.com/macros/s/[A-Za-z0-9_-]{20,}/exec(?:\?[^\s\"'<>)]*)?",
    ),
    re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/_-]{20,}"),
    re.compile(r"https://discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9._-]{20,}"),
)

AUTH_HEADER_RE = re.compile(
    r"(?i)\b(Authorization\s*:\s*(?:Bearer|Basic|Token)\s+)([A-Za-z0-9._~+/=-]{12,})",
)
CREDENTIAL_ASSIGNMENT_RE = re.compile(
    r"(?ix)"
    r"\b("
    r"api[_-]?key|apikey|"
    r"access[_-]?token|refresh[_-]?token|id[_-]?token|auth[_-]?token|"
    r"oauth[_-]?token|token|"
    r"client[_-]?secret|password|secret|"
    r"webhook[_-]?url"
    r")\b"
    r"\s*[:=]\s*"
    r"(?P<quote>[\"']?)"
    r"(?P<value>[^\"'\s,;}{]{8,})",
)
PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")
UNIX_USER_PATH_RE = re.compile(
    r"(?P<prefix>/(?:Users|home)/)(?P<user>[^/\s\"'<>{}]+)(?P<rest>/[^\s\"'<>]*)?",
)
WINDOWS_USER_PATH_RE = re.compile(
    r"(?P<prefix>[A-Za-z]:[\\/]+Users[\\/]+)(?P<user>[^\\/:\r\n\"'<>{}]+)(?P<rest>[\\/]+[^\r\n\"'<>]*)?",
)
SPREADSHEET_ID_RE = re.compile(
    r"(?i)\b(spreadsheet(?:_?id)?|spreadsheetId)\b\s*[:=]\s*[\"']?[A-Za-z0-9_-]{30,}",
)
SPREADSHEET_URL_RE = re.compile(
    r"https://docs\.google\.com/spreadsheets/d/[A-Za-z0-9_-]{30,}",
)
WORKBOOK_FILE_RE = re.compile(r"(?i)(?:^|[\s\"'=/\\])[^\"'\s<>]*\.(?:xlsx|xlsm|xls)\b")

RAW_PLAYER_LOG_MARKERS = (
    re.compile(r"\[UnityCrossThreadLogger\]"),
    re.compile(r"\[Client GRE\]"),
    re.compile(r"\bClientToGREMessage\b"),
    re.compile(r"\bClientToGremessage\b"),
    re.compile(r"\bGREMessageType_"),
)

FAILED_POST_RE = re.compile(
    r"(?i)(data/failed_posts|failed_posts|failed post|failed_post|webhook queue|queued_webhook_payload)",
)
RUNTIME_STATUS_RE = re.compile(
    r"(?i)(data/status|runtime status|runtime_status|status_latest|webhook_successes|webhook_failures)",
)
GENERATED_DATA_RE = re.compile(
    r"(?i)(data/oracle_data|data/tier_sources|data/decklists|oracle_id|scryfall|tier_snapshot)",
)


def _has_placeholder_context(text: str) -> bool:
    lowered = text.lower()
    if re.search(r"<[^>]*(?:redacted|placeholder|token|secret|example|configured)[^>]*>", lowered):
        return True
    if re.search(r"\bYOUR_[A-Z0-9_]+\b", text):
        return True
    return any(marker in lowered for marker in PLACEHOLDER_MARKERS)


def _is_policy_path(path: str) -> bool:
    return path.startswith(
        (
            "docs/contracts/",
            "docs/decisions/",
            "docs/archive/",
            "docs/agent_threads/",
            "docs/templates/",
            "docs/implementation_handoffs/",
            "docs/contract_test_reports/",
        ),
    ) or path in {
        "docs/agent_constitution.md",
        "docs/agent_rules.yml",
        "docs/codex_module_workflow.md",
        ".github/pull_request_template.md",
        ".github/ISSUE_TEMPLATE/module_workflow.yml",
        "tools/check_secret_patterns.py",
        "tools/check_secret_patterns_detectors.py",
        "tools/check_secret_patterns_models.py",
        "tests/test_check_secret_patterns.py",
    }


def _fixture_is_sanitized(path: str, file_text: str) -> bool:
    if not path.startswith("tests/fixtures/"):
        return False
    lowered = file_text.lower()
    return any(marker in lowered for marker in SANITIZED_FIXTURE_MARKERS)


def _safe_excerpt(
    line: str,
    category_id: str,
    span: tuple[int, int] | None = None,
) -> str:
    if category_id in {
        "raw_player_log_content",
        "failed_post_payload",
        "runtime_status_payload",
        "generated_data_dump",
        "workbook_export_marker",
    }:
        prefix = ""
        if category_id == "raw_player_log_content":
            marker_match = re.match(r"(\[[A-Za-z ]+\])", line)
            if marker_match:
                prefix = f"{marker_match.group(1)} "
        return f"{prefix}<redacted:{category_id}>"

    preview = line.rstrip("\r\n")
    if category_id == "private_local_path":
        preview = UNIX_USER_PATH_RE.sub(lambda match: f"{match.group('prefix')}<redacted>/...", preview)
        preview = WINDOWS_USER_PATH_RE.sub(
            lambda match: f"{match.group('prefix')}<redacted>\\...",
            preview,
        )
        if len(preview) > MAX_EXCERPT_CHARS:
            preview = f"{preview[: MAX_EXCERPT_CHARS - 3]}..."
        return preview or "<redacted>"

    if span is not None:
        start, end = span
        preview = f"{preview[:start]}<redacted:{category_id}>{preview[end:]}"

    preview = AUTH_HEADER_RE.sub(r"\1<redacted:credential_value>", preview)
    preview = PRIVATE_KEY_RE.sub("<redacted:credential_value>", preview)
    for pattern in WEBHOOK_PATTERNS:
        preview = pattern.sub("<redacted:live_webhook_url>", preview)
    preview = SPREADSHEET_URL_RE.sub("<redacted:workbook_export_marker>", preview)
    preview = SPREADSHEET_ID_RE.sub(
        lambda match: f"{match.group(1)}=<redacted:workbook_export_marker>",
        preview,
    )
    if category_id != "live_webhook_url":
        preview = CREDENTIAL_ASSIGNMENT_RE.sub(
            lambda match: f"{match.group(1)}=<redacted:credential_value>",
            preview,
        )
    preview = UNIX_USER_PATH_RE.sub(lambda match: f"{match.group('prefix')}<redacted>/...", preview)
    preview = WINDOWS_USER_PATH_RE.sub(
        lambda match: f"{match.group('prefix')}<redacted>\\...",
        preview,
    )

    if len(preview) > MAX_EXCERPT_CHARS:
        preview = f"{preview[: MAX_EXCERPT_CHARS - 3]}..."
    return preview or "<redacted>"


def _make_finding(
    *,
    severity: str,
    category_id: str,
    path: str,
    line: int,
    reason: str,
    rule_id: str,
    raw_line: str,
    span: tuple[int, int] | None = None,
) -> Finding:
    return Finding(
        severity=severity,
        category_id=category_id,
        path=path,
        line=line,
        reason=reason,
        excerpt=_safe_excerpt(raw_line, category_id, span),
        rule_id=rule_id,
    )


def _append_webhook_findings(
    findings: list[Finding],
    *,
    path: str,
    line_number: int,
    line: str,
) -> None:
    for pattern in WEBHOOK_PATTERNS:
        for match in pattern.finditer(line):
            value = match.group(0)
            if _has_placeholder_context(value):
                findings.append(
                    _make_finding(
                        severity=SEVERITY_WARNING,
                        category_id="placeholder_secret_reference",
                        path=path,
                        line=line_number,
                        reason="Webhook-looking value is clearly placeholder or redacted.",
                        rule_id="webhook-placeholder",
                        raw_line=line,
                        span=match.span(),
                    ),
                )
                continue
            findings.append(
                _make_finding(
                    severity=SEVERITY_FORBIDDEN,
                    category_id="live_webhook_url",
                    path=path,
                    line=line_number,
                    reason="Live-looking webhook or Apps Script deployment URL.",
                    rule_id="live-webhook-url",
                    raw_line=line,
                    span=match.span(),
                ),
            )


def _append_credential_findings(
    findings: list[Finding],
    *,
    path: str,
    line_number: int,
    line: str,
) -> None:
    if PRIVATE_KEY_RE.search(line):
        findings.append(
            _make_finding(
                severity=SEVERITY_FORBIDDEN,
                category_id="credential_value",
                path=path,
                line=line_number,
                reason="Private key marker is credential material.",
                rule_id="private-key-marker",
                raw_line=line,
            ),
        )

    for match in AUTH_HEADER_RE.finditer(line):
        value = match.group(2)
        severity = SEVERITY_WARNING if _has_placeholder_context(value) else SEVERITY_FORBIDDEN
        category_id = "placeholder_secret_reference" if severity == SEVERITY_WARNING else "credential_value"
        reason = (
            "Authorization value is clearly placeholder or redacted."
            if severity == SEVERITY_WARNING
            else "Authorization header contains a non-placeholder value."
        )
        findings.append(
            _make_finding(
                severity=severity,
                category_id=category_id,
                path=path,
                line=line_number,
                reason=reason,
                rule_id="authorization-header",
                raw_line=line,
                span=match.span(2),
            ),
        )

    for match in CREDENTIAL_ASSIGNMENT_RE.finditer(line):
        value = match.group("value")
        if value.startswith("<") and value.endswith(">"):
            placeholder = True
        else:
            placeholder = _has_placeholder_context(value)
        severity = SEVERITY_WARNING if placeholder else SEVERITY_FORBIDDEN
        category_id = "placeholder_secret_reference" if placeholder else "credential_value"
        reason = (
            "Credential-looking assignment uses a placeholder value."
            if placeholder
            else "Credential-looking assignment contains a non-placeholder value."
        )
        findings.append(
            _make_finding(
                severity=severity,
                category_id=category_id,
                path=path,
                line=line_number,
                reason=reason,
                rule_id="credential-assignment",
                raw_line=line,
                span=match.span("value"),
            ),
        )


def _append_private_path_findings(
    findings: list[Finding],
    *,
    path: str,
    line_number: int,
    line: str,
) -> None:
    for pattern in (UNIX_USER_PATH_RE, WINDOWS_USER_PATH_RE):
        for match in pattern.finditer(line):
            value = match.group(0)
            if _has_placeholder_context(value):
                findings.append(
                    _make_finding(
                        severity=SEVERITY_WARNING,
                        category_id="artifact_path_reference",
                        path=path,
                        line=line_number,
                        reason="Local artifact path is documented with placeholder context.",
                        rule_id="placeholder-local-path",
                        raw_line=line,
                        span=match.span(),
                    ),
                )
                continue
            findings.append(
                _make_finding(
                    severity=SEVERITY_FORBIDDEN,
                    category_id="private_local_path",
                    path=path,
                    line=line_number,
                    reason="Absolute local user path is private machine state.",
                    rule_id="private-local-path",
                    raw_line=line,
                    span=match.span(),
                ),
            )


def _append_player_log_findings(
    findings: list[Finding],
    *,
    path: str,
    line_number: int,
    line: str,
    file_text: str,
) -> None:
    if not any(pattern.search(line) for pattern in RAW_PLAYER_LOG_MARKERS):
        return
    if _fixture_is_sanitized(path, file_text):
        findings.append(
            _make_finding(
                severity=SEVERITY_WARNING,
                category_id="sanitized_fixture_marker",
                path=path,
                line=line_number,
                reason="Player.log marker appears inside a sanitized fixture context.",
                rule_id="sanitized-fixture-player-log-marker",
                raw_line=line,
            ),
        )
        return
    if _is_policy_path(path) or _has_placeholder_context(line):
        findings.append(
            _make_finding(
                severity=SEVERITY_WARNING,
                category_id="ambiguous_private_marker",
                path=path,
                line=line_number,
                reason="Player.log marker appears in policy, docs, or placeholder context.",
                rule_id="ambiguous-player-log-marker",
                raw_line=line,
            ),
        )
        return
    findings.append(
        _make_finding(
            severity=SEVERITY_FORBIDDEN,
            category_id="raw_player_log_content",
            path=path,
            line=line_number,
            reason="Raw Player.log-style content outside sanitized fixture context.",
            rule_id="raw-player-log-content",
            raw_line=line,
        ),
    )


def _append_artifact_payload_findings(
    findings: list[Finding],
    *,
    path: str,
    line_number: int,
    line: str,
) -> None:
    lowered = line.lower()
    line_is_jsonish = "{" in line or ":" in line
    if FAILED_POST_RE.search(line) and (line_is_jsonish or "payload" in lowered):
        severity = SEVERITY_WARNING if _is_policy_path(path) or _has_placeholder_context(line) else SEVERITY_FORBIDDEN
        category_id = "artifact_path_reference" if severity == SEVERITY_WARNING else "failed_post_payload"
        findings.append(
            _make_finding(
                severity=severity,
                category_id=category_id,
                path=path,
                line=line_number,
                reason="Failed-post queue or payload marker appears in text.",
                rule_id="failed-post-payload",
                raw_line=line,
            ),
        )
    if RUNTIME_STATUS_RE.search(line) and line_is_jsonish:
        severity = SEVERITY_WARNING if _is_policy_path(path) or _has_placeholder_context(line) else SEVERITY_FORBIDDEN
        category_id = "artifact_path_reference" if severity == SEVERITY_WARNING else "runtime_status_payload"
        findings.append(
            _make_finding(
                severity=severity,
                category_id=category_id,
                path=path,
                line=line_number,
                reason="Runtime status snapshot marker appears in text.",
                rule_id="runtime-status-payload",
                raw_line=line,
            ),
        )
    if GENERATED_DATA_RE.search(line) and line_is_jsonish:
        severity = SEVERITY_WARNING if _is_policy_path(path) or _has_placeholder_context(line) else SEVERITY_FORBIDDEN
        category_id = "artifact_path_reference" if severity == SEVERITY_WARNING else "generated_data_dump"
        findings.append(
            _make_finding(
                severity=severity,
                category_id=category_id,
                path=path,
                line=line_number,
                reason="Generated data dump marker appears in text.",
                rule_id="generated-data-dump",
                raw_line=line,
            ),
        )
    if SPREADSHEET_ID_RE.search(line) or SPREADSHEET_URL_RE.search(line) or WORKBOOK_FILE_RE.search(line):
        placeholder = _is_policy_path(path) or _has_placeholder_context(line)
        severity = SEVERITY_WARNING if placeholder else SEVERITY_FORBIDDEN
        category_id = "artifact_path_reference" if placeholder else "workbook_export_marker"
        findings.append(
            _make_finding(
                severity=severity,
                category_id=category_id,
                path=path,
                line=line_number,
                reason="Workbook export or spreadsheet identifier marker appears in text.",
                rule_id="workbook-export-marker",
                raw_line=line,
            ),
        )


def scan_text(path: str, text: str) -> tuple[Finding, ...]:
    findings: list[Finding] = []
    for index, line in enumerate(text.splitlines(), start=1):
        _append_webhook_findings(findings, path=path, line_number=index, line=line)
        _append_credential_findings(findings, path=path, line_number=index, line=line)
        _append_private_path_findings(findings, path=path, line_number=index, line=line)
        _append_player_log_findings(
            findings,
            path=path,
            line_number=index,
            line=line,
            file_text=text,
        )
        _append_artifact_payload_findings(findings, path=path, line_number=index, line=line)
    return tuple(findings)
