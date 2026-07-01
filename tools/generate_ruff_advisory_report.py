"""Build a deterministic advisory summary from Ruff JSON output."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Any

REPORT_OBJECT = "mythic_edge_quality_ruff_advisory_report"
REPORT_SCHEMA_VERSION = "quality_ruff_advisory_report.v1"
DEFAULT_REPOSITORY = "Tahjali11/Mythic-Edge"
DEFAULT_REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge"
DEFAULT_SCAN_SCOPE = ("src", "tests", "tools")
DEFAULT_COMMAND = "python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json"
EXIT_BEHAVIOR = "advisory_exit_zero"

ALLOWED_DISPOSITIONS = {
    "zero_baseline_candidate",
    "blocker_candidate",
    "advisory",
    "watch_list",
    "cleanup_issue_candidate",
    "protected_surface_review_required",
    "ignore_with_rationale",
    "unsupported",
    "invalid",
}
FORBIDDEN_DISPOSITIONS = {
    "blocking_enabled",
    "ci_ready",
    "parser_ready",
    "security_assured",
    "privacy_assured",
    "production_ready",
    "auto_fixed",
    "truth_confirmed",
}
NON_CLAIMS = (
    "not parser behavior readiness",
    "not pipeline activation readiness for issue #388",
    "not parser truth",
    "not fixture promotion readiness",
    "not corpus readiness",
    "not CI readiness",
    "not release readiness",
    "not deploy readiness",
    "not production readiness",
    "not security assurance",
    "not privacy assurance",
    "not analytics truth",
    "not AI truth",
    "not coaching truth",
)

RULE_CODE_RE = re.compile(r"^[A-Z]+[0-9]+$")
RULE_FAMILY_RE = re.compile(r"^[A-Z]+")
WINDOWS_LOCAL_PATH_RE = re.compile(r"(?i)^[A-Za-z]:[\\/]")
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]{1,}:/+")
SECRET_RE = re.compile(
    r"(?i)("
    r"\bAuthorization\s*:\s*(?:Bearer|Basic|Token)\s+[\"']?[A-Za-z0-9._~+/=-]{12,}|"
    r"\b(?:Bearer|Basic|Token)\s+[\"']?[A-Za-z0-9._~+/=-]{12,}|"
    r"--(?:api[_-]?key|token|access[_-]?token|auth[_-]?token)\s+[\"']?[A-Za-z0-9._~+/=-]{12,}|"
    r"api[_-]?key\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"access[_-]?token\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"refresh[_-]?token\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"id[_-]?token\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"auth[_-]?token\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"oauth[_-]?token\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"token\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"secret\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"[\"']?secret[_ -]?key[\"']?\s*(?::=|=>|[:=])\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"credentials?\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"client[_-]?secret\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"password\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}|"
    r"webhook[_ -]?url\s*[:=]\s*[\"']?\S{8,}|"
    r"ghp_[A-Za-z0-9_]{20,}|"
    r"gho_[A-Za-z0-9_]{20,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|"
    r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|"
    r"sk-[A-Za-z0-9_]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{20,}"
    r")"
)
SECRET_FIELD_NAME_RE = re.compile(
    r"(?i)^("
    r"api[_-]?key|"
    r"access[_-]?token|"
    r"refresh[_-]?token|"
    r"id[_-]?token|"
    r"auth[_-]?token|"
    r"oauth[_-]?token|"
    r"token|"
    r"secret|"
    r"secret[_ -]?key|"
    r"credentials?|"
    r"client[_-]?secret|"
    r"password|"
    r"webhook[_ -]?url"
    r")$"
)
QUOTED_SECRET_FIELD_ASSIGNMENT_RE = re.compile(
    r"(?i)[\"']?"
    r"(?:api[_ -]?key|access[_-]?token|refresh[_-]?token|id[_-]?token|"
    r"auth[_-]?token|oauth[_-]?token|token|secret|secret[_ -]?key|"
    r"credentials?|client[_-]?secret|password|webhook[_ -]?url)"
    r"[\"']?\s*(?::=|=>|[:=])\s*[\"']?\S{8,}"
)
RAW_SOURCE_OR_FIX_MESSAGE_RE = re.compile(
    r"(?m)("
    r"^diff --git\b|"
    r"^@@\s|"
    r"^\s*[+-]\s*(?:def\s+[A-Za-z_][A-Za-z0-9_]*\s*\(|"
    r"class\s+[A-Za-z_][A-Za-z0-9_]*(?:\(|:)|"
    r"import\s+[A-Za-z_][A-Za-z0-9_.]*|"
    r"from\s+[A-Za-z_][A-Za-z0-9_.]*\s+import\s+|"
    r"return\b|if\b|for\b|while\b|raise\b|print\(|"
    r"[A-Za-z_][A-Za-z0-9_]*\s*=)|"
    r"^\s*(?:def\s+[A-Za-z_][A-Za-z0-9_]*\s*\(|"
    r"class\s+[A-Za-z_][A-Za-z0-9_]*(?:\(|:)|"
    r"import\s+[A-Za-z_][A-Za-z0-9_.]*(?:\s|$)|"
    r"from\s+[A-Za-z_][A-Za-z0-9_.]*\s+import\s+)|"
    r"^\s{2,}(?:return\b|if .+:|for .+:|while .+:|raise\b|print\(|"
    r"[A-Za-z_][A-Za-z0-9_]*\s*=)|"
    r"^[A-Za-z_][A-Za-z0-9_]*\s*=|"
    r"(?i:\b(?:autofix diff|fix edit|edit preview|source patch)\b)"
    r")"
)
RAW_PRIVATE_PAYLOAD_RE = re.compile(
    r"(?is)\b(?:raw_log_payload|private_payload|workbook export|sqlite row|runtime artifact)\b"
)
OVERCLAIM_TEXT_RE = re.compile(
    r"(?i)\b("
    r"ci ready|ci readiness|blocking ready|blocking readiness|parser truth|"
    r"security assurance|privacy assurance|release readiness|deploy readiness|"
    r"production readiness|analytics truth|ai truth|coaching truth"
    r")\b"
)
PRIVATE_MARKERS = (
    "Player" + ".log",
    "UTC" + "_Log",
    "workbook export",
    "runtime artifact",
    "failed post",
    "private decklist",
    "private strategy note",
)
AUTOFIX_FLAGS = ("--fix", "--unsafe-fixes", "--fix-only")
GENERATED_PRIVATE_PATH_PREFIXES = ("_review_", "data/")
MEASURED_CHECKOUT_ROOT_MARKERS = ("pyproject.toml", "AGENTS.md", ".git")
PRIVATE_MARKER_FILENAME_OMISSION_POLICY = "symbolic_private_marker_filename_omission"
PRIVATE_MARKER_FILENAME_OMISSION_REASON = "path_omitted_private_marker_filename"
APPROVED_PRIVATE_MARKER_PATH_BUCKETS = frozenset(DEFAULT_SCAN_SCOPE)


class RuffAdvisoryError(ValueError):
    """Raised when advisory input must fail closed."""


@dataclass(frozen=True)
class ReportMetadata:
    repository: str = DEFAULT_REPOSITORY
    repository_url: str = DEFAULT_REPOSITORY_URL
    branch_or_ref: str = "unknown"
    commit: str = "unknown"
    ruff_version: str = "unknown"
    scan_scope: tuple[str, ...] = DEFAULT_SCAN_SCOPE
    commands: tuple[str, ...] = (DEFAULT_COMMAND,)


@dataclass(frozen=True)
class Finding:
    rule_code: str
    filename: str | None
    fix_applicability: str
    omitted_path_reason: str | None = None
    path_scope_bucket: str | None = None


def load_ruff_json(text: str) -> list[dict[str, Any]]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuffAdvisoryError("measurement_blocked_malformed_json") from exc
    if not isinstance(payload, list):
        raise RuffAdvisoryError("measurement_blocked_malformed_json")
    if not all(isinstance(item, dict) for item in payload):
        raise RuffAdvisoryError("unsupported_rule_record")
    return payload


def build_report(
    ruff_records: list[dict[str, Any]],
    *,
    metadata: ReportMetadata | None = None,
    candidate_rule_codes: tuple[str, ...] = (),
    measured_checkout_root: str | PathLike[str] | None = None,
) -> dict[str, Any]:
    report_metadata = metadata or ReportMetadata()
    report_metadata = validate_metadata(report_metadata)
    exact_candidate_codes = normalize_candidate_rule_codes(candidate_rule_codes)
    checkout_root = _resolve_measured_checkout_root(measured_checkout_root)
    findings = tuple(_parse_finding(record, measured_checkout_root=checkout_root) for record in ruff_records)

    summaries = _build_rule_summaries(findings, exact_candidate_codes)
    zero_candidates = tuple(item for item in summaries if item["disposition"] == "zero_baseline_candidate")
    triggered_codes = {finding.rule_code for finding in findings}

    return {
        "object": REPORT_OBJECT,
        "schema_version": REPORT_SCHEMA_VERSION,
        "repository": report_metadata.repository,
        "repository_url": report_metadata.repository_url,
        "branch_or_ref": report_metadata.branch_or_ref,
        "commit": report_metadata.commit,
        "ruff_version": report_metadata.ruff_version,
        "scan_scope": list(report_metadata.scan_scope),
        "commands": list(report_metadata.commands),
        "exit_behavior": EXIT_BEHAVIOR,
        "totals": {
            "findings": len(findings),
            "triggered_rule_codes": len(triggered_codes),
            "zero_baseline_rule_codes": len(zero_candidates),
        },
        "rule_summaries": list(summaries),
        "zero_baseline_candidates": list(zero_candidates),
        "non_claims": list(NON_CLAIMS),
    }


def normalize_candidate_rule_codes(rule_codes: tuple[str, ...]) -> tuple[str, ...]:
    normalized: list[str] = []
    for raw_code in rule_codes:
        code = raw_code.strip().upper()
        if not code:
            continue
        if not is_exact_rule_code(code):
            raise RuffAdvisoryError("candidate_rejected_broad_family")
        normalized.append(code)
    return tuple(sorted(set(normalized)))


def validate_metadata(metadata: ReportMetadata) -> ReportMetadata:
    for value in (
        metadata.repository,
        metadata.repository_url,
        metadata.branch_or_ref,
        metadata.commit,
        metadata.ruff_version,
    ):
        _reject_forbidden_text(value)
        _reject_local_path_text(value)

    scan_scope = tuple(normalize_repo_path(item) for item in metadata.scan_scope)
    commands = tuple(_validate_command_text(command) for command in metadata.commands)
    return ReportMetadata(
        repository=metadata.repository,
        repository_url=metadata.repository_url,
        branch_or_ref=metadata.branch_or_ref,
        commit=metadata.commit,
        ruff_version=metadata.ruff_version,
        scan_scope=scan_scope,
        commands=commands,
    )


def _validate_command_text(command: str) -> str:
    command_text = command.strip()
    if not command_text:
        raise RuffAdvisoryError("unsupported_rule_record")
    _reject_forbidden_text(command_text)
    _reject_local_path_text(command_text)
    command_parts = command_text.split()
    if any(_is_autofix_flag(part) for part in command_parts):
        raise RuffAdvisoryError("autofix_blocked_not_authorized")
    return command_text


def _is_autofix_flag(command_part: str) -> bool:
    return any(
        command_part == flag
        or command_part.startswith(f"{flag}=")
        or command_part.startswith(f"{flag}-")
        for flag in AUTOFIX_FLAGS
    )


def is_exact_rule_code(code: str) -> bool:
    return bool(RULE_CODE_RE.match(code))


def rule_family(rule_code: str) -> str:
    match = RULE_FAMILY_RE.match(rule_code)
    if not match:
        raise RuffAdvisoryError("unsupported_rule_record")
    return match.group(0)


def _parse_finding(record: dict[str, Any], *, measured_checkout_root: Path) -> Finding:
    _reject_secret_like_payload(record)

    rule_code = _require_string(record, "code").upper()
    if not is_exact_rule_code(rule_code):
        raise RuffAdvisoryError("unsupported_rule_record")

    filename = normalize_diagnostic_filename(
        _require_string(record, "filename"),
        measured_checkout_root=measured_checkout_root,
    )
    message = _require_string(record, "message")
    _validate_unemitted_diagnostic_message(message)
    public_filename, omitted_reason, path_scope_bucket = _public_diagnostic_path_or_symbolic_omission(filename)

    return Finding(
        rule_code=rule_code,
        filename=public_filename,
        fix_applicability=_fix_applicability(record.get("fix")),
        omitted_path_reason=omitted_reason,
        path_scope_bucket=path_scope_bucket,
    )


def _require_string(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise RuffAdvisoryError("unsupported_rule_record")
    return value


def normalize_repo_path(path: str) -> str:
    text = path.replace("\\", "/").strip()
    if _contains_local_path(text):
        raise RuffAdvisoryError("measurement_blocked_local_path_leak")
    while text.startswith("./"):
        text = text[2:]
    parts = [part for part in text.split("/") if part and part != "."]
    if any(part == ".." for part in parts):
        raise RuffAdvisoryError("measurement_blocked_local_path_leak")
    if not parts:
        raise RuffAdvisoryError("unsupported_rule_record")
    return "/".join(parts)


def normalize_diagnostic_filename(path: str, *, measured_checkout_root: Path) -> str:
    text = path.strip()
    if not text:
        raise RuffAdvisoryError("unsupported_rule_record")
    if _is_uri_scheme_path(text):
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported")
    if _is_unc_or_double_slash_path(text):
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported")
    if _is_absolute_path_text(text):
        repo_path = _normalize_absolute_diagnostic_filename(text, measured_checkout_root=measured_checkout_root)
    else:
        repo_path = normalize_repo_path(text)
    _reject_forbidden_repo_path(repo_path)
    return repo_path


def _resolve_measured_checkout_root(root: str | PathLike[str] | None) -> Path:
    try:
        if root is None:
            checkout_root = Path.cwd().resolve(strict=False)
        else:
            checkout_root = Path(root).expanduser().resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported") from exc
    _validate_measured_checkout_root(checkout_root)
    return checkout_root


def _validate_measured_checkout_root(root: Path) -> None:
    if not root.is_absolute():
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported")
    if not all((root / marker).exists() for marker in MEASURED_CHECKOUT_ROOT_MARKERS):
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported")


def _is_absolute_path_text(path: str) -> bool:
    text = path.replace("\\", "/")
    return (text.startswith("/") and not text.startswith("//")) or bool(WINDOWS_LOCAL_PATH_RE.match(path))


def _is_unc_or_double_slash_path(path: str) -> bool:
    return path.replace("\\", "/").startswith("//")


def _is_uri_scheme_path(path: str) -> bool:
    return bool(URI_SCHEME_RE.match(path))


def _normalize_absolute_diagnostic_filename(path: str, *, measured_checkout_root: Path) -> str:
    if WINDOWS_LOCAL_PATH_RE.match(path) and not WINDOWS_LOCAL_PATH_RE.match(str(measured_checkout_root)):
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported")
    absolute_path = Path(path).expanduser()
    if not absolute_path.is_absolute():
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported")
    try:
        relative_path = absolute_path.resolve(strict=False).relative_to(measured_checkout_root)
    except ValueError as exc:
        raise RuffAdvisoryError("measurement_blocked_path_outside_checkout") from exc
    except (OSError, RuntimeError) as exc:
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported") from exc
    return normalize_repo_path(relative_path.as_posix())


def _reject_forbidden_repo_path(path: str) -> None:
    if path.startswith("/") or path.startswith("../") or path == ".." or path.startswith("file://"):
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported")
    if WINDOWS_LOCAL_PATH_RE.match(path):
        raise RuffAdvisoryError("measurement_blocked_path_normalization_unsupported")
    if any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in GENERATED_PRIVATE_PATH_PREFIXES):
        raise RuffAdvisoryError("measurement_blocked_local_path_leak")


def _reject_forbidden_text(text: str) -> None:
    _reject_secret_like_text(text)
    if _contains_private_marker_text(text):
        raise RuffAdvisoryError("measurement_blocked_private_marker")


def _reject_secret_like_text(text: str) -> None:
    if SECRET_RE.search(text) or QUOTED_SECRET_FIELD_ASSIGNMENT_RE.search(text):
        raise RuffAdvisoryError("measurement_blocked_secret_like_output")


def _contains_private_marker_text(text: str) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in PRIVATE_MARKERS)


def _public_diagnostic_path_or_symbolic_omission(path: str) -> tuple[str | None, str | None, str | None]:
    _reject_secret_like_text(path)
    if not _contains_private_marker_text(path):
        return path, None, None

    path_scope_bucket = _private_marker_path_scope_bucket(path)
    return None, PRIVATE_MARKER_FILENAME_OMISSION_REASON, path_scope_bucket


def _private_marker_path_scope_bucket(path: str) -> str:
    bucket = path.split("/", 1)[0]
    if bucket not in APPROVED_PRIVATE_MARKER_PATH_BUCKETS:
        raise RuffAdvisoryError("measurement_blocked_private_marker")
    return bucket


def _reject_secret_like_payload(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and _is_secret_like_field_name(key):
                raise RuffAdvisoryError("measurement_blocked_secret_like_output")
            _reject_secret_like_payload(item)
    elif isinstance(value, list):
        for item in value:
            _reject_secret_like_payload(item)
    elif isinstance(value, str):
        _reject_secret_like_text(value)


def _is_secret_like_field_name(value: str) -> bool:
    field_name = value.strip().strip("\"'").replace("-", "_").replace(" ", "_")
    return bool(SECRET_FIELD_NAME_RE.match(field_name))


def _validate_unemitted_diagnostic_message(message: str) -> None:
    _reject_secret_like_text(message)
    if RAW_SOURCE_OR_FIX_MESSAGE_RE.search(message):
        raise RuffAdvisoryError("measurement_blocked_raw_source_snippet_public")
    if RAW_PRIVATE_PAYLOAD_RE.search(message):
        raise RuffAdvisoryError("measurement_blocked_raw_output_public")
    if OVERCLAIM_TEXT_RE.search(message):
        raise RuffAdvisoryError("measurement_blocked_raw_output_public")


def _reject_local_path_text(text: str) -> None:
    normalized = text.replace("\\", "/")
    if _contains_local_path(normalized):
        raise RuffAdvisoryError("measurement_blocked_local_path_leak")


def _contains_local_path(text: str) -> bool:
    return any(_is_local_path_token(token) for token in text.split())


def _is_local_path_token(token: str) -> bool:
    cleaned = token.strip("\"'(),[]{}")
    if not cleaned:
        return False
    if cleaned.startswith(("http://", "https://")):
        return False
    normalized = cleaned.replace("\\", "/")
    if normalized.startswith("//"):
        return True
    if cleaned.startswith("file://"):
        return True
    if "=" in cleaned:
        return _is_local_path_token(cleaned.rsplit("=", 1)[1])
    return bool(WINDOWS_LOCAL_PATH_RE.match(cleaned)) or normalized.startswith("/")


def _fix_applicability(fix: Any) -> str:
    if not isinstance(fix, dict):
        return "unavailable"
    applicability = fix.get("applicability")
    if applicability == "safe":
        return "safe"
    if applicability == "unsafe":
        return "unsafe"
    return "available"


def _build_rule_summaries(
    findings: tuple[Finding, ...],
    candidate_rule_codes: tuple[str, ...],
) -> tuple[dict[str, Any], ...]:
    all_codes = sorted({finding.rule_code for finding in findings} | set(candidate_rule_codes))
    summaries = []
    for code in all_codes:
        code_findings = tuple(finding for finding in findings if finding.rule_code == code)
        affected_paths = tuple(sorted({finding.filename for finding in code_findings if finding.filename}))
        omitted_path_count = sum(1 for finding in code_findings if finding.omitted_path_reason is not None)
        omitted_path_buckets = tuple(
            sorted({finding.path_scope_bucket for finding in code_findings if finding.path_scope_bucket is not None})
        )
        protected_surface = (
            "private_artifact_or_secret_surface"
            if omitted_path_count
            else classify_protected_surface(affected_paths)
        )
        disposition = _disposition_for(code_findings, protected_surface)
        if disposition in FORBIDDEN_DISPOSITIONS or disposition not in ALLOWED_DISPOSITIONS:
            raise RuffAdvisoryError("unsupported_rule_record")
        summary = {
            "rule_code": code,
            "rule_family": rule_family(code),
            "count": len(code_findings),
            "affected_file_count": len(affected_paths) + omitted_path_count,
            "affected_paths": list(affected_paths),
            "autofix_available": _aggregate_autofix(code_findings),
            "unsafe_fix_available": _aggregate_unsafe_fix(code_findings),
            "protected_surface_impact": protected_surface,
            "disposition": disposition,
            "reason": _reason_for(disposition),
        }
        if omitted_path_count:
            summary.update(
                {
                    "omitted_affected_path_count": omitted_path_count,
                    "path_handling_policy": PRIVATE_MARKER_FILENAME_OMISSION_POLICY,
                    "path_omission_reason": PRIVATE_MARKER_FILENAME_OMISSION_REASON,
                    "path_scope_buckets": list(omitted_path_buckets),
                }
            )
        summaries.append(summary)
    return tuple(summaries)


def _disposition_for(findings: tuple[Finding, ...], protected_surface: str) -> str:
    if not findings:
        return "zero_baseline_candidate"
    if protected_surface != "none":
        return "protected_surface_review_required"
    return "advisory"


def _aggregate_autofix(findings: tuple[Finding, ...]) -> str:
    if any(item.fix_applicability == "safe" for item in findings):
        return "safe"
    if any(item.fix_applicability == "unsafe" for item in findings):
        return "unsafe"
    if any(item.fix_applicability == "available" for item in findings):
        return "available"
    return "unavailable"


def _aggregate_unsafe_fix(findings: tuple[Finding, ...]) -> str:
    if any(item.fix_applicability == "unsafe" for item in findings):
        return "yes"
    if findings:
        return "no"
    return "unknown"


def _reason_for(disposition: str) -> str:
    reasons = {
        "zero_baseline_candidate": "Exact rule code has zero findings for this scan scope.",
        "advisory": "Exact rule code has advisory findings and must not block.",
        "protected_surface_review_required": "Findings touch protected surfaces and need dedicated review.",
    }
    return reasons.get(disposition, "Rule requires review before any promotion.")


def classify_protected_surface(paths: tuple[str, ...]) -> str:
    priority = (
        ("private_artifact_or_secret_surface", _is_private_artifact_or_secret_surface),
        ("ci_release_or_deploy_surface", _is_ci_release_or_deploy_surface),
        ("parser_truth_surface", _is_parser_truth_surface),
        ("workbook_webhook_or_appsscript_surface", _is_workbook_webhook_or_appsscript_surface),
        ("analytics_ai_or_coaching_surface", _is_analytics_ai_or_coaching_surface),
        ("evidence_or_corpus_surface", _is_evidence_or_corpus_surface),
        ("governance_or_workflow_surface", _is_governance_or_workflow_surface),
    )
    for label, predicate in priority:
        if any(predicate(path) for path in paths):
            return label
    return "none"


def _is_parser_truth_surface(path: str) -> bool:
    return path.startswith("src/mythic_edge_parser/parsers/") or path in {
        "src/mythic_edge_parser/events.py",
        "src/mythic_edge_parser/router.py",
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/extractors.py",
        "src/mythic_edge_parser/app/event_identity.py",
        "src/mythic_edge_parser/app/gameplay_actions.py",
        "src/mythic_edge_parser/app/transforms.py",
    }


def _is_evidence_or_corpus_surface(path: str) -> bool:
    lowered = path.lower()
    return (
        "corpus" in lowered
        or "golden_replay" in lowered
        or "evidence_" in lowered
        or path.startswith("tests/fixtures/")
    )


def _is_private_artifact_or_secret_surface(path: str) -> bool:
    return path.startswith("data/") or "secret" in path.lower() or "credential" in path.lower()


def _is_workbook_webhook_or_appsscript_surface(path: str) -> bool:
    lowered = path.lower()
    return (
        path.startswith("tools/google_apps_script/")
        or "sheet_" in lowered
        or "webhook" in lowered
        or path == "src/mythic_edge_parser/app/outputs.py"
    )


def _is_analytics_ai_or_coaching_surface(path: str) -> bool:
    lowered = path.lower()
    return "analytics" in lowered or "/ai/" in lowered or "coaching" in lowered


def _is_ci_release_or_deploy_surface(path: str) -> bool:
    return (
        path.startswith(".github/workflows/")
        or path == "pyproject.toml"
        or path.startswith("tools/run_repo_checks")
        or path.startswith("tools/run_touched_file_checks")
    )


def _is_governance_or_workflow_surface(path: str) -> bool:
    return (
        path == "AGENTS.md"
        or path.startswith("docs/agent_")
        or path.startswith("docs/contracts/")
        or path.startswith("docs/templates/")
        or path.startswith("docs/decisions/")
    )


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def _read_text(path_text: str) -> str:
    if path_text == "-":
        return sys.stdin.read()
    try:
        return Path(path_text).read_text(encoding="utf-8")
    except OSError as exc:
        raise RuffAdvisoryError("measurement_blocked_input_unreadable") from exc


def _read_rule_codes(path: Path) -> tuple[str, ...]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RuffAdvisoryError("measurement_blocked_input_unreadable") from exc
    except json.JSONDecodeError as exc:
        raise RuffAdvisoryError("candidate_rejected_broad_family") from exc
    if not isinstance(payload, list) or not all(isinstance(item, str) for item in payload):
        raise RuffAdvisoryError("candidate_rejected_broad_family")
    return tuple(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a sanitized Ruff advisory summary from Ruff JSON.")
    parser.add_argument("--input", default="-", help="Path to Ruff JSON output, or '-' for stdin.")
    parser.add_argument("--rule-code", action="append", help="Exact Ruff rule code to evaluate as a candidate.")
    parser.add_argument("--rule-codes-file", type=Path, help="JSON list of exact Ruff rule codes to evaluate.")
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--repository-url", default=DEFAULT_REPOSITORY_URL)
    parser.add_argument("--branch-or-ref", default="unknown")
    parser.add_argument("--commit", default="unknown")
    parser.add_argument("--ruff-version", default="unknown")
    parser.add_argument("--scan-scope", nargs="+", default=list(DEFAULT_SCAN_SCOPE))
    parser.add_argument("--command", action="append", help="Advisory Ruff command that produced the input.")
    parser.add_argument(
        "--measured-checkout-root",
        type=Path,
        default=None,
        help="Measured checkout root used only to normalize Ruff diagnostic filenames.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        rule_codes = tuple(args.rule_code or ())
        if args.rule_codes_file:
            rule_codes = (*rule_codes, *_read_rule_codes(args.rule_codes_file))
        metadata = ReportMetadata(
            repository=args.repository,
            repository_url=args.repository_url,
            branch_or_ref=args.branch_or_ref,
            commit=args.commit,
            ruff_version=args.ruff_version,
            scan_scope=tuple(args.scan_scope),
            commands=tuple(args.command or ()) or (DEFAULT_COMMAND,),
        )
        records = load_ruff_json(_read_text(args.input))
        report = build_report(
            records,
            metadata=metadata,
            candidate_rule_codes=rule_codes,
            measured_checkout_root=args.measured_checkout_root,
        )
    except (OSError, json.JSONDecodeError, RuffAdvisoryError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(render_json(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
