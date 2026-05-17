"""Run Pyright as an advisory check and print a stable Mythic Edge report."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPORT_OBJECT = "mythic_edge_pyright_advisory_report"
REPORT_SCHEMA_VERSION = 1
REPORT_MODE = "advisory"
RUNNER = "tools/run_pyright_advisory_report.py"
GATE_BEHAVIOR = "advisory_non_blocking"
NORMALIZED_PYTHON = "<resolved-python>"
SUMMARY_RE = re.compile(
    r"(?P<errors>\d+)\s+errors?,\s+(?P<warnings>\d+)\s+warnings?,\s+"
    r"(?P<information>\d+)\s+informations?",
)
RULE_RE = re.compile(r"\((?P<rule>report[A-Za-z0-9_]+)\)")
LOCAL_RESOLVER_RULES = {"reportMissingImports", "reportMissingModuleSource"}
WINDOWS_ALIAS_MARKERS = (
    "Python was not found",
    "App execution aliases",
    "Microsoft Store",
)
TOOLING_BLOCKER_MARKERS = (
    "pyright is not installed",
    "No configuration file found",
    "Config file",
    "could not be read",
    "not found",
)


@dataclass(frozen=True)
class PyrightSummary:
    errors: int | None
    warnings: int | None
    information: int | None

    @property
    def total(self) -> int:
        if self.errors is None or self.warnings is None or self.information is None:
            return 0
        return self.errors + self.warnings + self.information


@dataclass(frozen=True)
class FindingClassification:
    type_findings: int
    local_resolver_noise: int
    tooling_config_blockers: int
    type_rules: dict[str, int]
    local_resolver_rules: dict[str, int]
    tooling_config_rules: dict[str, int]


@dataclass(frozen=True)
class AdvisoryReport:
    object: str
    schema_version: int
    mode: str
    project: str
    python: str
    platform: str
    runner: str
    command: str
    pyright_version: str
    exit_code: int
    errors: int | None
    warnings: int | None
    information: int | None
    type_findings: int
    local_resolver_noise: int
    tooling_config_blockers: int
    status: str
    gate_behavior: str
    type_rules: dict[str, int]
    local_resolver_rules: dict[str, int]
    tooling_config_rules: dict[str, int]

    @property
    def helper_exit_code(self) -> int:
        return 2 if self.status in {"tooling_config_blocker", "error"} else 0


def detect_platform(platform_name: str | None = None) -> str:
    name = (platform_name or sys.platform).lower()
    if name.startswith(("win", "cygwin", "msys")):
        return "windows"
    if name == "darwin":
        return "macos"
    if name.startswith("linux"):
        return "linux"
    return "unknown"


def normalize_python_path(_python_executable: str | Path) -> str:
    return NORMALIZED_PYTHON


def _repo_relative_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return redact_local_paths(str(path)).replace("\\", "/")


def _display_project(project: str | Path, repo_root: str | Path) -> str:
    project_path = Path(project)
    if project_path.is_absolute():
        return _repo_relative_path(project_path, Path(repo_root))
    return project_path.as_posix()


def redact_local_paths(text: str) -> str:
    home = str(Path.home())
    redacted = text.replace(home, "<home>")
    redacted = redacted.replace(home.replace("\\", "/"), "<home>")
    return redacted


def parse_summary(output: str) -> PyrightSummary:
    matches = list(SUMMARY_RE.finditer(output))
    if not matches:
        return PyrightSummary(errors=None, warnings=None, information=None)
    match = matches[-1]
    return PyrightSummary(
        errors=int(match.group("errors")),
        warnings=int(match.group("warnings")),
        information=int(match.group("information")),
    )


def _increment(counter: dict[str, int], key: str) -> None:
    counter[key] = counter.get(key, 0) + 1


def _line_is_local_resolver_noise(line: str, rule: str) -> bool:
    if rule in LOCAL_RESOLVER_RULES and "Import " in line and "could not be resolved" in line:
        return True
    return any(marker in line for marker in WINDOWS_ALIAS_MARKERS)


def _line_is_tooling_blocker(line: str) -> bool:
    lowered = line.lower()
    return any(marker.lower() in lowered for marker in TOOLING_BLOCKER_MARKERS)


def classify_pyright_output(output: str, summary: PyrightSummary) -> FindingClassification:
    type_rules: dict[str, int] = {}
    local_rules: dict[str, int] = {}
    tooling_rules: dict[str, int] = {}
    uncategorized_rule_findings = 0

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        rule_match = RULE_RE.search(line)
        rule = rule_match.group("rule") if rule_match else ""
        if _line_is_local_resolver_noise(line, rule):
            _increment(local_rules, rule or "windows_python_alias")
        elif _line_is_tooling_blocker(line):
            _increment(tooling_rules, rule or "tooling_config")
        elif rule:
            _increment(type_rules, rule)
        elif summary.errors is None and line.lower().startswith(("error", "fatal")):
            uncategorized_rule_findings += 1

    type_findings = sum(type_rules.values()) + uncategorized_rule_findings
    known_finding_count = type_findings + sum(local_rules.values())
    if summary.total > known_finding_count and not tooling_rules:
        type_findings += summary.total - known_finding_count

    return FindingClassification(
        type_findings=type_findings,
        local_resolver_noise=sum(local_rules.values()),
        tooling_config_blockers=sum(tooling_rules.values()),
        type_rules=type_rules,
        local_resolver_rules=local_rules,
        tooling_config_rules=tooling_rules,
    )


def _status_for(
    *,
    pyright_exit_code: int,
    summary: PyrightSummary,
    classification: FindingClassification,
) -> str:
    if classification.tooling_config_blockers:
        return "tooling_config_blocker"
    if summary.errors is None and pyright_exit_code != 0:
        return "error"
    if classification.type_findings:
        return "advisory_findings"
    if classification.local_resolver_noise:
        return "local_resolver_noise"
    return "clean"


def build_report(
    *,
    project: str | Path,
    repo_root: str | Path,
    python_executable: str | Path,
    pyright_version: str,
    pyright_exit_code: int,
    output: str,
    platform_name: str | None = None,
) -> AdvisoryReport:
    project_display = _display_project(project, repo_root)
    summary = parse_summary(output)
    classification = classify_pyright_output(output, summary)
    status = _status_for(
        pyright_exit_code=pyright_exit_code,
        summary=summary,
        classification=classification,
    )
    return AdvisoryReport(
        object=REPORT_OBJECT,
        schema_version=REPORT_SCHEMA_VERSION,
        mode=REPORT_MODE,
        project=project_display,
        python=normalize_python_path(python_executable),
        platform=detect_platform(platform_name),
        runner=RUNNER,
        command=f"pyright --project {project_display} --pythonpath <python>",
        pyright_version=pyright_version or "unknown",
        exit_code=pyright_exit_code,
        errors=summary.errors,
        warnings=summary.warnings,
        information=summary.information,
        type_findings=classification.type_findings,
        local_resolver_noise=classification.local_resolver_noise,
        tooling_config_blockers=classification.tooling_config_blockers,
        status=status,
        gate_behavior=GATE_BEHAVIOR,
        type_rules=classification.type_rules,
        local_resolver_rules=classification.local_resolver_rules,
        tooling_config_rules=classification.tooling_config_rules,
    )


def build_tooling_blocker_report(
    *,
    project: str | Path,
    repo_root: str | Path,
    reason: str,
    python_executable: str | Path = NORMALIZED_PYTHON,
    platform_name: str | None = None,
) -> AdvisoryReport:
    project_display = _display_project(project, repo_root)
    return AdvisoryReport(
        object=REPORT_OBJECT,
        schema_version=REPORT_SCHEMA_VERSION,
        mode=REPORT_MODE,
        project=project_display,
        python=normalize_python_path(python_executable),
        platform=detect_platform(platform_name),
        runner=RUNNER,
        command=f"pyright --project {project_display} --pythonpath <python>",
        pyright_version="unknown",
        exit_code=2,
        errors=None,
        warnings=None,
        information=None,
        type_findings=0,
        local_resolver_noise=0,
        tooling_config_blockers=1,
        status="tooling_config_blocker",
        gate_behavior=GATE_BEHAVIOR,
        type_rules={},
        local_resolver_rules={},
        tooling_config_rules={redact_local_paths(reason): 1},
    )


def _format_count(value: int | None) -> str:
    return "unknown" if value is None else str(value)


def render_text(report: AdvisoryReport) -> str:
    lines = [
        "Pyright Advisory Report",
        f"mode: {report.mode}",
        f"project: {report.project}",
        f"python: {report.python}",
        f"platform: {report.platform}",
        f"runner: {report.runner}",
        f"command: {report.command}",
        f"pyright_version: {report.pyright_version}",
        f"exit_code: {report.exit_code}",
        f"errors: {_format_count(report.errors)}",
        f"warnings: {_format_count(report.warnings)}",
        f"information: {_format_count(report.information)}",
        f"type_findings: {report.type_findings}",
        f"local_resolver_noise: {report.local_resolver_noise}",
        f"tooling_config_blockers: {report.tooling_config_blockers}",
        f"status: {report.status}",
        f"gate_behavior: {report.gate_behavior}",
    ]
    if report.type_rules:
        lines.extend(["", "Type Findings:"])
        lines.extend(f"- {rule}: {count}" for rule, count in sorted(report.type_rules.items()))
    if report.local_resolver_rules:
        lines.extend(["", "Local Resolver Noise:"])
        lines.extend(f"- {rule}: {count}" for rule, count in sorted(report.local_resolver_rules.items()))
    if report.tooling_config_rules:
        lines.extend(["", "Tooling / Config Blockers:"])
        lines.extend(f"- {rule}: {count}" for rule, count in sorted(report.tooling_config_rules.items()))
    return "\n".join(lines)


def render_json(report: AdvisoryReport) -> str:
    payload: dict[str, Any] = asdict(report)
    payload["summary"] = {
        "errors": report.errors,
        "warnings": report.warnings,
        "information": report.information,
    }
    payload["classification"] = {
        "type_findings": report.type_findings,
        "local_resolver_noise": report.local_resolver_noise,
        "tooling_config_blockers": report.tooling_config_blockers,
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _run_command(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _pyright_version(*, repo_root: Path) -> str:
    try:
        completed = _run_command(["pyright", "--version"], cwd=repo_root)
    except OSError:
        return "unknown"
    output = (completed.stdout or completed.stderr).strip()
    if completed.returncode != 0 or not output:
        return "unknown"
    return output.removeprefix("pyright").strip() or output


def run_report(
    *,
    project: str | Path = "pyrightconfig.json",
    repo_root: str | Path = ".",
    python_executable: str | Path | None = None,
) -> AdvisoryReport:
    root = Path(repo_root).resolve()
    project_path = Path(project)
    resolved_project = project_path if project_path.is_absolute() else root / project_path
    executable = Path(python_executable or sys.executable)

    if not resolved_project.exists():
        return build_tooling_blocker_report(
            project=project,
            repo_root=root,
            reason="pyrightconfig.json is missing or unreadable",
            python_executable=executable,
        )
    if shutil.which("pyright") is None:
        return build_tooling_blocker_report(
            project=project,
            repo_root=root,
            reason="pyright is not installed or not on PATH",
            python_executable=executable,
        )

    project_display = _display_project(project, root)
    command = [
        "pyright",
        "--project",
        str(resolved_project),
        "--pythonpath",
        str(executable),
    ]
    try:
        completed = _run_command(command, cwd=root)
    except OSError as exc:
        return build_tooling_blocker_report(
            project=project,
            repo_root=root,
            reason=str(exc),
            python_executable=executable,
        )

    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    return build_report(
        project=project_display,
        repo_root=root,
        python_executable=executable,
        pyright_version=_pyright_version(repo_root=root),
        pyright_exit_code=completed.returncode,
        output=output,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Mythic Edge Pyright advisory report.")
    parser.add_argument("--project", default="pyrightconfig.json", help="Pyright project config path.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Report format.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    report = run_report(project=args.project, repo_root=args.repo_root)
    output = render_json(report) if args.format == "json" else render_text(report)
    print(output)
    return report.helper_exit_code


if __name__ == "__main__":
    raise SystemExit(main())
