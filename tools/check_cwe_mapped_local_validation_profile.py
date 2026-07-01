"""Validate the advisory CWE-mapped local validation profile manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_PROFILE_PATH = Path("docs/security/cwe_mapped_local_validation_profile.v1.json")

PROFILE_ID = "mythic_edge.security.cwe_mapped_local_validation_profile"
REPOSITORY = "Tahjali11/Mythic-Edge"
CONTRACT_REF = "docs/contracts/security_cwe_mapped_local_validation_profile.md"
SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/590"
PARENT_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/330"

EXPECTED_PRIMARY_CWES: dict[str, str] = {
    "local_path_traversal": "CWE-22",
    "generated_filename_id_to_path": "CWE-73",
    "subprocess_command_line_invocation": "CWE-78",
    "url_host_validation": "CWE-187",
    "secret_private_artifact_exposure": "CWE-538",
    "temporary_file_handling": "CWE-377",
    "workflow_permission_scope": "CWE-732",
}

EXPECTED_RELATED_CWES: dict[str, set[str]] = {
    "local_path_traversal": {"CWE-73"},
    "generated_filename_id_to_path": {"CWE-22"},
    "subprocess_command_line_invocation": {"CWE-88"},
    "url_host_validation": {"CWE-1023", "CWE-184"},
    "secret_private_artifact_exposure": {"CWE-532"},
    "temporary_file_handling": {"CWE-378", "CWE-379"},
    "workflow_permission_scope": {"CWE-276"},
}

REQUIRED_ENVELOPE_FIELDS = {
    "schema_version",
    "profile_id",
    "repository",
    "repository_url",
    "contract_ref",
    "source_issue",
    "parent_issue",
    "generated_at_policy",
    "profile_status",
    "enforcement_authorized",
    "codeql_alert_mutation_authorized",
    "families",
}

REQUIRED_FAMILY_FIELDS = {
    "family_id",
    "title",
    "summary",
    "primary_cwe_id",
    "primary_cwe_title",
    "primary_cwe_mapping_status",
    "primary_cwe_reference",
    "related_cwe_ids",
    "scanner_cwe_provenance",
    "discouraged_or_prohibited_cwe_provenance",
    "codeql_rule_ids",
    "local_detector_ids",
    "local_test_refs",
    "allowed_evidence",
    "forbidden_evidence",
    "reporting_policy",
    "rollout_status",
    "non_claims",
    "mapping_rationale",
    "mapping_review_status",
}

ALLOWED_PROFILE_STATUSES = {
    "contract_only",
    "advisory_profile",
    "advisory_local_check",
    "blocking_candidate",
    "blocking_enabled",
}
ALLOWED_ROLLOUT_STATUSES = {
    "contract_only",
    "advisory_available",
    "advisory_match",
    "warning_only",
    "no_finding",
    "review_required",
    "blocked",
    "unsupported",
    "blocking_candidate",
    "blocking_enabled",
}
ALLOWED_MAPPING_STATUSES = {"ALLOWED", "ALLOWED-WITH-REVIEW"}
ALLOWED_MAPPING_REVIEW_STATUSES = {
    "accepted_exact",
    "accepted_related",
    "needs_review",
    "rejected_too_broad",
    "rejected_discouraged_mapping",
    "rejected_prohibited_mapping",
    "rejected_placeholder_or_invented",
}
PROHIBITED_PRIMARY_CWES = {"CWE-20", "CWE-200", "CWE-275", "CWE-2000"}
DISCOURAGED_OR_PROHIBITED_PROVENANCE = {
    "url_host_validation": {"CWE-20"},
    "secret_private_artifact_exposure": {"CWE-200"},
    "workflow_permission_scope": {"CWE-275"},
}
REQUIRED_FALSE_FLAGS = {
    "ci_change_authorized",
    "enforcement_authorized",
    "codeql_alert_mutation_authorized",
    "parser_behavior_change_authorized",
    "security_assurance_claimed",
    "privacy_assurance_claimed",
}

UNSAFE_TEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("local_windows_absolute_path", re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]+", re.IGNORECASE)),
    ("local_unix_user_path", re.compile(r"/(?:Users|home)/[^\s\"'<>]+", re.IGNORECASE)),
    ("live_google_script_url", re.compile(r"https://script\.google\.com/macros/s/", re.IGNORECASE)),
    ("private_key_marker", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("credential_assignment", re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*[^<\s][^\s,;]{7,}")),
)


@dataclass(frozen=True)
class ProfileIssue:
    code: str
    location: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    profile_path: str
    family_count: int
    errors: tuple[ProfileIssue, ...]
    warnings: tuple[ProfileIssue, ...] = ()

    @property
    def passed(self) -> bool:
        return not self.errors

    @property
    def exit_code(self) -> int:
        return 0 if self.passed else 1


def load_profile(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("profile manifest must be a JSON object")
    return data


def _safe_issue(code: str, location: str, message: str) -> ProfileIssue:
    return ProfileIssue(code=code, location=location, message=message)


def _append_missing_fields(
    errors: list[ProfileIssue],
    item: dict[str, Any],
    required_fields: set[str],
    location: str,
) -> None:
    for field in sorted(required_fields - item.keys()):
        errors.append(_safe_issue("cwe_mapping_missing", location, f"missing field {field}"))


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def _walk_strings(value: Any, location: str = "$") -> list[tuple[str, str]]:
    if isinstance(value, str):
        return [(location, value)]
    if isinstance(value, list):
        items: list[tuple[str, str]] = []
        for index, item in enumerate(value):
            items.extend(_walk_strings(item, f"{location}[{index}]"))
        return items
    if isinstance(value, dict):
        items = []
        for key, item in value.items():
            items.extend(_walk_strings(item, f"{location}.{key}"))
        return items
    return []


def _validate_public_safe_text(data: dict[str, Any]) -> list[ProfileIssue]:
    errors: list[ProfileIssue] = []
    for location, text in _walk_strings(data):
        for code, pattern in UNSAFE_TEXT_PATTERNS:
            if pattern.search(text):
                errors.append(
                    _safe_issue(
                        "unsafe_report_output",
                        location,
                        f"unsafe text pattern {code}",
                    ),
                )
    return errors


def _validate_envelope(data: dict[str, Any]) -> list[ProfileIssue]:
    errors: list[ProfileIssue] = []
    _append_missing_fields(errors, data, REQUIRED_ENVELOPE_FIELDS, "$")

    expected_values = {
        "schema_version": "1",
        "profile_id": PROFILE_ID,
        "repository": REPOSITORY,
        "contract_ref": CONTRACT_REF,
        "source_issue": SOURCE_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "generated_at_policy": "manual_or_test_only",
    }
    for field, expected in expected_values.items():
        if field in data and data[field] != expected:
            errors.append(_safe_issue("cwe_mapping_missing", "$", f"{field} must be {expected}"))

    profile_status = data.get("profile_status")
    if profile_status not in ALLOWED_PROFILE_STATUSES:
        errors.append(_safe_issue("unsupported_surface", "$", "profile_status is not recognized"))
    if profile_status in {"blocking_candidate", "blocking_enabled"}:
        errors.append(
            _safe_issue(
                "enforcement_not_authorized",
                "$",
                "blocking profile status is not authorized",
            ),
        )

    for flag in sorted(REQUIRED_FALSE_FLAGS):
        if data.get(flag) is not False:
            errors.append(_safe_issue("enforcement_not_authorized", "$", f"{flag} must be false"))

    if data.get("codeql_alert_mutation_authorized") is not False:
        errors.append(
            _safe_issue(
                "codeql_alert_mutation_not_authorized",
                "$",
                "CodeQL alert mutation must remain false",
            ),
        )

    if data.get("security_assurance_claimed") is not False:
        errors.append(
            _safe_issue(
                "security_assurance_not_authorized",
                "$",
                "security assurance must not be claimed",
            ),
        )
    if data.get("privacy_assurance_claimed") is not False:
        errors.append(
            _safe_issue(
                "security_assurance_not_authorized",
                "$",
                "privacy assurance must not be claimed",
            ),
        )

    families = data.get("families")
    if not isinstance(families, list):
        errors.append(_safe_issue("cwe_mapping_missing", "$", "families must be a list"))

    return errors


def _validate_family_shape(family: dict[str, Any], location: str) -> list[ProfileIssue]:
    errors: list[ProfileIssue] = []
    _append_missing_fields(errors, family, REQUIRED_FAMILY_FIELDS, location)

    for field in (
        "family_id",
        "title",
        "summary",
        "primary_cwe_id",
        "primary_cwe_title",
        "primary_cwe_mapping_status",
        "primary_cwe_reference",
        "reporting_policy",
        "rollout_status",
        "mapping_rationale",
        "mapping_review_status",
    ):
        if field in family and not _is_non_empty_string(family[field]):
            errors.append(_safe_issue("cwe_mapping_missing", location, f"{field} must be a string"))

    for field in (
        "related_cwe_ids",
        "scanner_cwe_provenance",
        "discouraged_or_prohibited_cwe_provenance",
        "codeql_rule_ids",
        "local_detector_ids",
        "local_test_refs",
        "allowed_evidence",
        "forbidden_evidence",
        "non_claims",
    ):
        if field in family and not _is_string_list(family[field]):
            errors.append(_safe_issue("cwe_mapping_missing", location, f"{field} must be a string list"))

    return errors


def _validate_family_mapping(family: dict[str, Any], location: str) -> list[ProfileIssue]:
    errors: list[ProfileIssue] = []
    family_id = family.get("family_id")
    if not isinstance(family_id, str):
        return errors

    expected_primary = EXPECTED_PRIMARY_CWES.get(family_id)
    if expected_primary is None:
        errors.append(_safe_issue("unsupported_surface", location, "family_id is not in the v1 profile"))
        return errors

    primary_cwe = family.get("primary_cwe_id")
    if primary_cwe != expected_primary:
        errors.append(
            _safe_issue(
                "cwe_mapping_too_broad",
                location,
                f"{family_id} primary CWE must be {expected_primary}",
            ),
        )
    if primary_cwe in PROHIBITED_PRIMARY_CWES:
        errors.append(
            _safe_issue(
                "cwe_mapping_prohibited",
                location,
                "primary CWE is prohibited or discouraged for this profile",
            ),
        )

    mapping_status = family.get("primary_cwe_mapping_status")
    if mapping_status not in ALLOWED_MAPPING_STATUSES:
        errors.append(
            _safe_issue(
                "cwe_mapping_placeholder_or_invented",
                location,
                "primary_cwe_mapping_status is not allowed",
            ),
        )

    mapping_review_status = family.get("mapping_review_status")
    if mapping_review_status not in ALLOWED_MAPPING_REVIEW_STATUSES:
        errors.append(
            _safe_issue(
                "cwe_mapping_placeholder_or_invented",
                location,
                "mapping_review_status is not recognized",
            ),
        )
    if isinstance(mapping_review_status, str) and mapping_review_status.startswith("rejected_"):
        errors.append(
            _safe_issue(
                "cwe_mapping_prohibited",
                location,
                "rejected mappings cannot appear in the advisory profile",
            ),
        )

    rollout_status = family.get("rollout_status")
    if rollout_status not in ALLOWED_ROLLOUT_STATUSES:
        errors.append(_safe_issue("unsupported_surface", location, "rollout_status is not recognized"))
    if rollout_status in {"blocking_candidate", "blocking_enabled"}:
        errors.append(
            _safe_issue(
                "enforcement_not_authorized",
                location,
                "blocking rollout status is not authorized",
            ),
        )

    related = set(family.get("related_cwe_ids", []))
    expected_related = EXPECTED_RELATED_CWES.get(family_id, set())
    missing_related = expected_related - related
    if missing_related:
        errors.append(
            _safe_issue(
                "cwe_mapping_missing",
                location,
                f"missing required related CWE count {len(missing_related)}",
            ),
        )

    scanner_provenance = set(family.get("scanner_cwe_provenance", []))
    discouraged = set(family.get("discouraged_or_prohibited_cwe_provenance", []))
    expected_discouraged = DISCOURAGED_OR_PROHIBITED_PROVENANCE.get(family_id, set())
    if expected_discouraged and not expected_discouraged <= scanner_provenance:
        errors.append(
            _safe_issue(
                "cwe_mapping_missing",
                location,
                "missing expected scanner CWE provenance",
            ),
        )
    if expected_discouraged and not expected_discouraged <= discouraged:
        errors.append(
            _safe_issue(
                "cwe_mapping_discouraged_provenance_missing",
                location,
                "discouraged scanner CWE provenance must be recorded separately",
            ),
        )

    for cwe_id in scanner_provenance & PROHIBITED_PRIMARY_CWES:
        if cwe_id not in discouraged:
            errors.append(
                _safe_issue(
                    "cwe_mapping_discouraged_provenance_missing",
                    location,
                    "discouraged scanner CWE provenance must be recorded separately",
                ),
            )

    return errors


def validate_profile(data: dict[str, Any], profile_path: str = "<profile>") -> ValidationResult:
    errors: list[ProfileIssue] = []
    warnings: list[ProfileIssue] = []

    errors.extend(_validate_envelope(data))
    errors.extend(_validate_public_safe_text(data))

    families = data.get("families")
    family_count = len(families) if isinstance(families, list) else 0
    if isinstance(families, list):
        seen_family_ids: set[str] = set()
        for index, family in enumerate(families):
            location = f"$.families[{index}]"
            if not isinstance(family, dict):
                errors.append(_safe_issue("cwe_mapping_missing", location, "family must be an object"))
                continue
            errors.extend(_validate_family_shape(family, location))
            errors.extend(_validate_family_mapping(family, location))
            family_id = family.get("family_id")
            if isinstance(family_id, str):
                if family_id in seen_family_ids:
                    errors.append(
                        _safe_issue("cwe_mapping_placeholder_or_invented", location, "duplicate family_id")
                    )
                seen_family_ids.add(family_id)

        expected_families = set(EXPECTED_PRIMARY_CWES)
        if seen_family_ids != expected_families:
            errors.append(
                _safe_issue(
                    "cwe_mapping_missing",
                    "$.families",
                    "family set must exactly match the v1 profile",
                ),
            )

    return ValidationResult(
        profile_path=profile_path,
        family_count=family_count,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def _safe_display_path(path_text: str) -> str:
    path = Path(path_text)
    if not path.is_absolute():
        return path_text
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except (OSError, ValueError):
        return "<profile-path>"


def render_report(result: ValidationResult) -> str:
    lines = [
        "CWE-Mapped Local Validation Profile",
        f"path: {_safe_display_path(result.profile_path)}",
        f"families: {result.family_count}",
        f"errors: {len(result.errors)}",
        f"warnings: {len(result.warnings)}",
    ]
    for issue in result.errors:
        lines.append(f"ERROR {issue.code} {issue.location}: {issue.message}")
    for issue in result.warnings:
        lines.append(f"WARNING {issue.code} {issue.location}: {issue.message}")
    lines.append(f"result: {'passed' if result.passed else 'failed'}")
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "profile",
        nargs="?",
        default=str(DEFAULT_PROFILE_PATH),
        help="Path to the CWE profile manifest JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    profile_path = Path(args.profile)

    try:
        data = load_profile(profile_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: unable to load profile: {exc}", file=sys.stderr)
        return 2

    result = validate_profile(data, profile_path=str(profile_path))
    print(render_report(result))
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
