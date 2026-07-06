"""Result models for the agent docs consistency checker."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from tools.check_agent_docs_contract import (
        RESULT_ERROR,
        RESULT_FAILED,
        RESULT_PASSED,
        RESULT_WARNING,
        SEVERITY_ERROR,
        SEVERITY_WARNING,
    )
except ModuleNotFoundError:
    from check_agent_docs_contract import (
        RESULT_ERROR,
        RESULT_FAILED,
        RESULT_PASSED,
        RESULT_WARNING,
        SEVERITY_ERROR,
        SEVERITY_WARNING,
    )


@dataclass(frozen=True)
class Finding:
    severity: str
    category_id: str
    path: str
    reason: str


@dataclass(frozen=True)
class CheckResult:
    mode: str
    checked_files: tuple[str, ...]
    findings: tuple[Finding, ...]
    error: str = ""

    @property
    def errors(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity == SEVERITY_ERROR)

    @property
    def warnings(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity == SEVERITY_WARNING)

    @property
    def result(self) -> str:
        if self.error:
            return RESULT_ERROR
        if self.errors:
            return RESULT_FAILED
        if self.warnings:
            return RESULT_WARNING
        return RESULT_PASSED

    @property
    def exit_code(self) -> int:
        if self.error:
            return 2
        if self.errors:
            return 1
        return 0


@dataclass(frozen=True)
class Reference:
    source_path: str
    raw_target: str
    resolved_target: str
    context: str
    is_glob: bool
