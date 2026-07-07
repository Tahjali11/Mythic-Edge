"""Path normalization and classification for the protected-surface gate."""

from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Iterable

try:
    from tools.check_protected_surfaces_models import (
        FORBIDDEN_RULES,
        PROTECTED_RULES,
        SEVERITY_ALLOWED,
        SEVERITY_FORBIDDEN,
        SEVERITY_WARNING,
        Classification,
        GateResult,
        Rule,
    )
except ModuleNotFoundError:  # pragma: no cover - script-local import fallback.
    from check_protected_surfaces_models import (
        FORBIDDEN_RULES,
        PROTECTED_RULES,
        SEVERITY_ALLOWED,
        SEVERITY_FORBIDDEN,
        SEVERITY_WARNING,
        Classification,
        GateResult,
        Rule,
    )


def normalize_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    text = text.lstrip("/")
    parts = [part for part in text.split("/") if part and part != "."]
    return "/".join(parts)


def _matches_pattern(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        if any(marker in prefix for marker in "*?[]"):
            return fnmatch.fnmatchcase(path, pattern)
        return path == prefix or path.startswith(f"{prefix}/")
    return fnmatch.fnmatchcase(path, pattern)


def _matches_rule(path: str, rule: Rule) -> bool:
    name = path.rsplit("/", 1)[-1]
    return any(_matches_pattern(path, pattern) for pattern in rule.patterns) or any(
        fnmatch.fnmatchcase(name, pattern) for pattern in rule.filename_patterns
    )


def _is_documented_fixture(path: str) -> bool:
    return path.startswith("tests/fixtures/")


def _is_token_credential_filename(path: str) -> bool:
    name = path.rsplit("/", 1)[-1].lower()
    stem, dot, extension = name.rpartition(".")
    if not dot:
        stem = name
        extension = ""
    credential_extensions = {
        "",
        "env",
        "json",
        "secret",
        "txt",
        "key",
        "pem",
        "yml",
        "yaml",
    }
    if extension not in credential_extensions:
        return False
    return (
        stem == "token"
        or stem.startswith("token_")
        or stem.startswith("token-")
        or stem.endswith("_token")
        or stem.endswith("-token")
        or "api_token" in stem
        or "access_token" in stem
        or "refresh_token" in stem
        or "auth_token" in stem
        or "webhook_token" in stem
    )


def classify_path(path: str | Path) -> Classification:
    normalized = normalize_path(path)

    for rule in FORBIDDEN_RULES:
        if rule.category_id in {
            "local_mtga_log",
            "raw_workbook_export",
        } and _is_documented_fixture(normalized):
            continue
        if _matches_rule(normalized, rule):
            return Classification(
                normalized,
                SEVERITY_FORBIDDEN,
                rule.category_id,
                rule.reason,
            )

    if _is_token_credential_filename(normalized):
        return Classification(
            normalized,
            SEVERITY_FORBIDDEN,
            "webhook_api_credential",
            "Integration credential files must not be committed.",
        )

    for rule in PROTECTED_RULES:
        if _matches_rule(normalized, rule):
            return Classification(
                normalized,
                SEVERITY_WARNING,
                rule.category_id,
                rule.reason,
            )

    return Classification(
        normalized,
        SEVERITY_ALLOWED,
        "allowed",
        "No protected-surface classification.",
    )


def classify_paths(paths: Iterable[str | Path]) -> tuple[Classification, ...]:
    return tuple(classify_path(path) for path in paths)


def evaluate_paths(
    paths: Iterable[str | Path],
    *,
    base: str,
    head: str = "HEAD",
    error: str = "",
) -> GateResult:
    normalized_paths = tuple(normalize_path(path) for path in paths)
    return GateResult(
        base=base,
        head=head,
        changed_paths=normalized_paths,
        classifications=classify_paths(normalized_paths),
        error=error,
    )
