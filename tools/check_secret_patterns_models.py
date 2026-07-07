"""Shared models and vocabulary for the secret/private marker scanner."""

from __future__ import annotations

from dataclasses import dataclass

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
