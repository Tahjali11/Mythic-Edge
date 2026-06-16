"""Content scanner for repo-local secret and private-marker patterns."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SEVERITY_ALLOWED = "allowed"
SEVERITY_FORBIDDEN = "forbidden"
SEVERITY_WARNING = "warning"

RESULT_PASSED = "passed"
RESULT_WARNING = "warning"
RESULT_FAILED = "failed"
RESULT_ERROR = "error"

MODE_CHANGED = "changed-files"
MODE_STDIN = "paths-from-stdin"
MODE_ALL = "all-repo-advisory"

MAX_SCAN_BYTES = 1_000_000
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


@dataclass(frozen=True)
class Finding:
    severity: str
    category_id: str
    path: str
    line: int
    reason: str
    excerpt: str
    rule_id: str


@dataclass(frozen=True)
class ScanResult:
    mode: str
    base: str
    head: str
    scanned_paths: tuple[str, ...]
    skipped_paths: tuple[str, ...]
    findings: tuple[Finding, ...]
    error: str = ""

    @property
    def forbidden(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity == SEVERITY_FORBIDDEN)

    @property
    def warnings(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity == SEVERITY_WARNING)

    @property
    def result(self) -> str:
        if self.error:
            return RESULT_ERROR
        if self.forbidden:
            return RESULT_FAILED
        if self.warnings:
            return RESULT_WARNING
        return RESULT_PASSED

    @property
    def exit_code(self) -> int:
        if self.error:
            return 2
        if self.mode != MODE_ALL and self.forbidden:
            return 1
        return 0


def normalize_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    while text.startswith("//"):
        text = text[1:]
    parts = [part for part in text.split("/") if part and part != "."]
    return "/".join(parts)


def _has_placeholder_context(text: str) -> bool:
    lowered = text.lower()
    if re.search(r"<[^>]*(?:redacted|placeholder|token|secret|example|configured)[^>]*>", lowered):
        return True
    if re.search(r"\bYOUR_[A-Z0-9_]+\b", text):
        return True
    return any(marker in lowered for marker in PLACEHOLDER_MARKERS)


def _is_indirect_credential_lookup(value: str) -> bool:
    normalized = value.strip()
    return bool(
        re.match(r"^(?:os\.environ\.get|os\.getenv|_env_text|[A-Za-z_][\w.]*\.get)\(", normalized)
        or re.match(r"^self\.[A-Za-z_][\w.]*\(\)$", normalized)
    )


def _is_python_source_reference(path: str, line: str) -> bool:
    if not path.endswith(".py"):
        return False
    stripped = line.strip()
    if stripped.startswith(
        (
            "def ",
            "class ",
            "return ",
            "if ",
            "elif ",
            "else",
            "for ",
            "while ",
            "with ",
            "try",
            "except",
            "f\"",
            "f'",
        )
    ):
        return True
    if stripped[:1] in {"'", '"'} and ":" in stripped and stripped.endswith(","):
        return True
    if "lambda" in stripped and ":" in stripped:
        return True
    return ":" in stripped and stripped.endswith(",") and not stripped.startswith(("'", '"', "{", "["))


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
        if _is_indirect_credential_lookup(value):
            continue
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
    if _is_python_source_reference(path, line):
        return
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


def _read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _is_binary(data: bytes) -> bool:
    if not data:
        return False
    if b"\0" in data[:4096]:
        return True
    sample = data[:4096]
    control = sum(1 for byte in sample if byte < 9 or (13 < byte < 32))
    return control / len(sample) > 0.30


def _repo_relative_path(raw_path: str | Path, repo_root: Path) -> str:
    text = str(raw_path).strip().replace("\\", "/")
    if not text:
        return ""
    candidate = Path(text)
    if candidate.is_absolute():
        resolved = candidate.resolve(strict=False)
    elif ".." not in Path(normalize_path(text)).parts:
        return normalize_path(text)
    else:
        resolved = (repo_root / normalize_path(text)).resolve(strict=False)
    try:
        return resolved.relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise ValueError(f"path is outside repository root: {raw_path}") from exc


def normalize_candidate_paths(
    paths: Iterable[str | Path],
    *,
    repo_root: str | Path = ".",
    strict_outside_root: bool = False,
) -> tuple[tuple[str, ...], str]:
    root = Path(repo_root).resolve()
    normalized: set[str] = set()
    for raw_path in paths:
        try:
            relative = _repo_relative_path(raw_path, root)
        except ValueError as exc:
            if strict_outside_root:
                return (), str(exc)
            continue
        if relative:
            normalized.add(relative)
    return tuple(sorted(normalized)), ""


def collect_changed_paths(
    base: str,
    *,
    repo_root: str | Path = ".",
    head: str = "HEAD",
) -> tuple[str, ...]:
    command = [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        f"{base}...{head}",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(str(exc)) from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(detail or f"git diff failed with exit code {completed.returncode}")
    return tuple(line for line in completed.stdout.splitlines() if line.strip())


def collect_tracked_paths(*, repo_root: str | Path = ".") -> tuple[str, ...]:
    command = ["git", "ls-files"]
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(str(exc)) from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(detail or f"git ls-files failed with exit code {completed.returncode}")
    return tuple(line for line in completed.stdout.splitlines() if line.strip())


def _skip_finding(path: str, category_id: str, reason: str) -> Finding:
    return Finding(
        severity=SEVERITY_WARNING,
        category_id=category_id,
        path=path,
        line=0,
        reason=reason,
        excerpt=f"<redacted:{category_id}>",
        rule_id=category_id,
    )


def _scan_file(path: str, *, repo_root: Path) -> tuple[tuple[Finding, ...], bool, str]:
    absolute_path = repo_root / path
    if not absolute_path.exists():
        return (
            (
                _skip_finding(
                    path,
                    "ambiguous_private_marker",
                    "Path was selected for scanning but does not exist; skipped.",
                ),
            ),
            False,
            "",
        )
    try:
        if absolute_path.is_symlink():
            target = absolute_path.resolve(strict=True)
            try:
                target.relative_to(repo_root)
            except ValueError:
                return (), False, f"symlink resolves outside repository root: {path}"
    except OSError as exc:
        return (), False, str(exc)

    if not absolute_path.is_file():
        return (), False, ""

    try:
        data = _read_file_bytes(absolute_path)
    except OSError as exc:
        return (), False, str(exc)

    if _is_binary(data):
        return (
            (
                _skip_finding(
                    path,
                    "binary_skipped",
                    "Binary file was not content-scanned.",
                ),
            ),
            False,
            "",
        )
    if len(data) > MAX_SCAN_BYTES:
        return (
            (
                _skip_finding(
                    path,
                    "oversized_skipped",
                    f"Text file exceeds {MAX_SCAN_BYTES} byte scan limit.",
                ),
            ),
            False,
            "",
        )

    decode_warning: tuple[Finding, ...] = ()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("utf-8", errors="replace")
        decode_warning = (
            _skip_finding(
                path,
                "decode_replacement_used",
                "UTF-8 decoding used replacement characters before scanning.",
            ),
        )
    return decode_warning + scan_text(path, text), True, ""


def _sort_findings(findings: Iterable[Finding]) -> tuple[Finding, ...]:
    severity_order = {SEVERITY_FORBIDDEN: 0, SEVERITY_WARNING: 1, SEVERITY_ALLOWED: 2}
    return tuple(
        sorted(
            findings,
            key=lambda item: (
                severity_order.get(item.severity, 9),
                item.path,
                item.line,
                item.category_id,
                item.reason,
            ),
        ),
    )


def evaluate_paths(
    paths: Iterable[str | Path],
    *,
    base: str,
    repo_root: str | Path = ".",
    mode: str = MODE_STDIN,
    head: str = "HEAD",
    strict_outside_root: bool = False,
) -> ScanResult:
    root = Path(repo_root).resolve()
    normalized_paths, error = normalize_candidate_paths(
        paths,
        repo_root=root,
        strict_outside_root=strict_outside_root,
    )
    if error:
        return ScanResult(mode, base, head, (), (), (), error=error)

    findings: list[Finding] = []
    scanned_paths: list[str] = []
    skipped_paths: list[str] = []
    for path in normalized_paths:
        path_findings, scanned, scan_error = _scan_file(path, repo_root=root)
        if scan_error:
            return ScanResult(
                mode,
                base,
                head,
                tuple(scanned_paths),
                tuple(skipped_paths),
                _sort_findings(findings),
                error=scan_error,
            )
        if scanned:
            scanned_paths.append(path)
        else:
            skipped_paths.append(path)
        findings.extend(path_findings)

    return ScanResult(
        mode=mode,
        base=base,
        head=head,
        scanned_paths=tuple(scanned_paths),
        skipped_paths=tuple(skipped_paths),
        findings=_sort_findings(findings),
    )


def run_changed_scan(base: str, *, repo_root: str | Path = ".") -> ScanResult:
    try:
        paths = collect_changed_paths(base, repo_root=repo_root)
    except RuntimeError as exc:
        return ScanResult(MODE_CHANGED, base, "HEAD", (), (), (), error=str(exc))
    return evaluate_paths(paths, base=base, repo_root=repo_root, mode=MODE_CHANGED)


def run_all_scan(*, repo_root: str | Path = ".", base: str = "<not-required>") -> ScanResult:
    try:
        paths = collect_tracked_paths(repo_root=repo_root)
    except RuntimeError as exc:
        return ScanResult(MODE_ALL, base, "HEAD", (), (), (), error=str(exc))
    return evaluate_paths(paths, base=base, repo_root=repo_root, mode=MODE_ALL)


def render_report(result: ScanResult) -> str:
    lines = [
        "Secret / Private Marker Scan",
        f"mode: {result.mode}",
        f"base: {result.base}",
        f"head: {result.head}",
        f"scanned_paths: {len(result.scanned_paths)}",
        f"skipped_paths: {len(result.skipped_paths)}",
        f"forbidden: {len(result.forbidden)}",
        f"warnings: {len(result.warnings)}",
        "",
    ]
    if result.error:
        lines.append(f"ERROR configuration {result.error}")
    else:
        for finding in result.findings:
            if finding.severity not in {SEVERITY_FORBIDDEN, SEVERITY_WARNING}:
                continue
            label = "FORBIDDEN" if finding.severity == SEVERITY_FORBIDDEN else "WARNING"
            lines.append(
                f"{label} {finding.category_id} {finding.path}:{finding.line} - "
                f"{finding.reason} [excerpt: {finding.excerpt}]",
            )

    if lines[-1] != "":
        lines.append("")
    lines.append(f"result: {result.result}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan repository text for secret/private markers.")
    parser.add_argument("--base", help="Base git ref for <base>...HEAD.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--paths-from-stdin",
        action="store_true",
        help="Read newline-delimited paths from stdin instead of running git diff.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan all tracked files in advisory/report-only mode.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    if args.paths_from_stdin and args.all:
        print("--paths-from-stdin and --all cannot be used together", file=sys.stderr)
        return 2
    if not args.all and not args.base:
        print("--base is required unless --all is supplied", file=sys.stderr)
        return 2

    if args.all:
        result = run_all_scan(repo_root=args.repo_root, base=args.base or "<not-required>")
    elif args.paths_from_stdin:
        result = evaluate_paths(
            sys.stdin.read().splitlines(),
            base=args.base,
            repo_root=args.repo_root,
            mode=MODE_STDIN,
            strict_outside_root=True,
        )
    else:
        result = run_changed_scan(args.base, repo_root=args.repo_root)

    output = render_report(result)
    stream = sys.stderr if result.error else sys.stdout
    print(output, file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
