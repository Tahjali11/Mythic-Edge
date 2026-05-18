"""Coordinate Mythic Edge repo-wide hardening checks without replacing them."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

OBJECT_KIND = "mythic_edge_hardening_orchestrator"
SCHEMA_VERSION = 1

PROFILE_PLAN = "plan"
PROFILE_QUICK = "quick"
PROFILE_FULL = "full"
PROFILE_POST_HARDENING = "post-hardening"
PROFILES = (PROFILE_PLAN, PROFILE_QUICK, PROFILE_FULL, PROFILE_POST_HARDENING)

RUN_MODE_PLAN = "plan"
RUN_MODE_RUN = "run"

STATUS_PLANNED = "planned"
STATUS_PASSED = "passed"
STATUS_FAILED = "failed"
STATUS_WARNING = "warning"
STATUS_ADVISORY = "advisory"
STATUS_SKIPPED = "skipped"
STATUS_ERROR = "error"

ORCHESTRATOR_PLAN_ONLY = "plan_only"
ORCHESTRATOR_PASSED = "passed"
ORCHESTRATOR_FAILED = "failed"
ORCHESTRATOR_WARNING = "warning"
ORCHESTRATOR_ADVISORY = "advisory"
ORCHESTRATOR_ERROR = "error"

PRIORITY_REQUIRED = "required"
PRIORITY_RECOMMENDED = "recommended"
PRIORITY_ADVISORY = "advisory"

APPROVED_REPORT_PREFIX = "docs/contract_test_reports/"
MAX_SUMMARY_CHARS = 240


class ConfigError(Exception):
    """Configuration error that should exit 2 before command execution."""


@dataclass(frozen=True)
class CommandSpec:
    command_id: str
    priority: str
    command: tuple[str, ...]
    source_tool: str
    compatible_with_stdin_paths: bool = False
    skip_reason: str = ""

    @property
    def command_string(self) -> str:
        return shlex.join(self.command)


@dataclass(frozen=True)
class CommandResult:
    command_id: str
    priority: str
    status: str
    command: str
    source_tool: str
    exit_code: int | None = None
    summary: str = ""
    skip_reason: str = ""


@dataclass(frozen=True)
class OrchestratorResult:
    profile: str
    run_mode: str
    base: str
    commands: tuple[CommandResult, ...]
    error: str = ""

    @property
    def orchestrator_status(self) -> str:
        if self.error or any(item.status == STATUS_ERROR for item in self.commands):
            return ORCHESTRATOR_ERROR
        if self.run_mode == RUN_MODE_PLAN:
            return ORCHESTRATOR_PLAN_ONLY
        if any(
            item.status == STATUS_FAILED and item.priority == PRIORITY_REQUIRED
            for item in self.commands
        ):
            return ORCHESTRATOR_FAILED
        if any(item.status == STATUS_WARNING for item in self.commands):
            return ORCHESTRATOR_WARNING
        if any(item.status == STATUS_ADVISORY for item in self.commands):
            return ORCHESTRATOR_ADVISORY
        return ORCHESTRATOR_PASSED

    @property
    def exit_code(self) -> int:
        if self.orchestrator_status == ORCHESTRATOR_ERROR:
            return 2
        if self.orchestrator_status == ORCHESTRATOR_FAILED:
            return 1
        return 0


Runner = Callable[[Sequence[str], Path, str], subprocess.CompletedProcess[str]]


def _python_command(*parts: str) -> tuple[str, ...]:
    return ("python3", *parts)


def _with_base(tool_path: str, base: str) -> tuple[str, ...]:
    return _python_command(tool_path, "--base", base)


def _append_stdin_flag(command: tuple[str, ...], *, enabled: bool) -> tuple[str, ...]:
    if not enabled:
        return command
    return (*command, "--paths-from-stdin")


def _auth_command(
    *,
    base: str,
    authorization_files: tuple[str, ...],
    paths_from_stdin: bool,
) -> tuple[str, ...]:
    command = list(_with_base("tools/check_surface_authorization.py", base))
    if paths_from_stdin:
        command.append("--paths-from-stdin")
    for item in authorization_files:
        command.extend(["--authorization-file", item])
    return tuple(command)


def build_command_plan(
    *,
    profile: str,
    base: str,
    authorization_files: Iterable[str] = (),
    paths_from_stdin: bool = False,
    evidence_manifest: str = "",
    hardening_report_output: str = "",
) -> tuple[CommandSpec, ...]:
    auth_files = tuple(authorization_files)
    effective_profile = PROFILE_QUICK if profile == PROFILE_PLAN else profile
    commands: list[CommandSpec] = [
        CommandSpec(
            "protected_surface_gate",
            PRIORITY_REQUIRED,
            _append_stdin_flag(
                _with_base("tools/check_protected_surfaces.py", base),
                enabled=paths_from_stdin,
            ),
            "tools/check_protected_surfaces.py",
            compatible_with_stdin_paths=True,
        ),
        CommandSpec(
            "secret_private_marker_scan",
            PRIORITY_REQUIRED,
            _append_stdin_flag(
                _with_base("tools/check_secret_patterns.py", base),
                enabled=paths_from_stdin,
            ),
            "tools/check_secret_patterns.py",
            compatible_with_stdin_paths=True,
        ),
        CommandSpec(
            "validation_selector",
            PRIORITY_REQUIRED,
            _append_stdin_flag(
                _with_base("tools/select_validation.py", base),
                enabled=paths_from_stdin,
            ),
            "tools/select_validation.py",
            compatible_with_stdin_paths=True,
        ),
    ]

    if auth_files:
        commands.append(
            CommandSpec(
                "surface_authorization",
                PRIORITY_RECOMMENDED,
                _auth_command(
                    base=base,
                    authorization_files=auth_files,
                    paths_from_stdin=paths_from_stdin,
                ),
                "tools/check_surface_authorization.py",
                compatible_with_stdin_paths=True,
            ),
        )
    elif profile != PROFILE_PLAN:
        commands.append(
            CommandSpec(
                "surface_authorization",
                PRIORITY_RECOMMENDED,
                _with_base("tools/check_surface_authorization.py", base),
                "tools/check_surface_authorization.py",
                skip_reason="authorization_files_not_supplied",
            ),
        )

    commands.extend(
        [
            CommandSpec(
                "agent_docs_checker",
                PRIORITY_REQUIRED,
                _python_command("tools/check_agent_docs.py"),
                "tools/check_agent_docs.py",
            ),
            CommandSpec(
                "diff_check",
                PRIORITY_REQUIRED,
                ("git", "diff", "--check"),
                "git diff --check",
            ),
        ],
    )

    if effective_profile in {PROFILE_FULL, PROFILE_POST_HARDENING}:
        commands.extend(
            [
                CommandSpec(
                    "full_pytest",
                    PRIORITY_REQUIRED,
                    _python_command("-m", "pytest", "-q", "tests"),
                    "pytest",
                ),
                CommandSpec(
                    "ruff",
                    PRIORITY_REQUIRED,
                    _python_command("-m", "ruff", "check", "src", "tests", "tools"),
                    "ruff",
                ),
                CommandSpec(
                    "pyright_advisory",
                    PRIORITY_ADVISORY,
                    _python_command("tools/run_pyright_advisory_report.py"),
                    "tools/run_pyright_advisory_report.py",
                ),
            ],
        )

    if effective_profile == PROFILE_POST_HARDENING:
        report_command = list(_python_command("tools/generate_hardening_report.py"))
        if evidence_manifest:
            report_command.extend(["--evidence-manifest", evidence_manifest])
        if hardening_report_output:
            report_command.extend(["--output", hardening_report_output])
        commands.append(
            CommandSpec(
                "hardening_report_generator",
                PRIORITY_REQUIRED,
                tuple(report_command),
                "tools/generate_hardening_report.py",
            ),
        )

    return tuple(commands)


def _redact_local_paths(text: str) -> str:
    home = str(Path.home())
    redacted = text
    if home:
        redacted = redacted.replace(home, "<redacted-local-path>")
        redacted = redacted.replace(home.replace("\\", "/"), "<redacted-local-path>")
    redacted = re.sub(
        r"(?i)[A-Za-z]:[\\/]+Users[\\/]+[^\\/:\r\n\"'<>{}]+(?:[\\/]+[^\r\n\"'<>]*)?",
        "<redacted-local-path>",
        redacted,
    )
    redacted = re.sub(
        r"/(?:Users|home)/[^/\s\"'<>{}]+(?:/[^\s\"'<>]*)?",
        "<redacted-local-path>",
        redacted,
    )
    return redacted


def _redact_sensitive_text(text: str) -> str:
    redacted = _redact_local_paths(text)
    redacted = re.sub(
        r"https://script\.google\.com/macros/s/[A-Za-z0-9_-]{20,}/exec(?:\?[^\s\"'<>)]*)?",
        "<redacted-webhook-url>",
        redacted,
    )
    redacted = re.sub(
        r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token|auth[_-]?token|token|secret|password)"
        r"\s*[:=]\s*[^\"'\s,;}{]{8,}",
        r"\1=<redacted-secret>",
        redacted,
    )
    return redacted


def summarize_output(stdout: str, stderr: str, *, max_chars: int = MAX_SUMMARY_CHARS) -> str:
    combined = "\n".join(part for part in (stdout.strip(), stderr.strip()) if part)
    sanitized = _redact_sensitive_text(combined)
    lines = [line.strip() for line in sanitized.splitlines() if line.strip()]
    summary = " | ".join(lines[:3]) if lines else "<no output>"
    if len(summary) > max_chars:
        return f"{summary[: max_chars - 3]}..."
    return summary


def _has_count(output: str, label: str) -> bool:
    match = re.search(rf"(?im)^{re.escape(label)}:\s*([1-9]\d*)\s*$", output)
    return bool(match)


def classify_command_result(
    spec: CommandSpec,
    completed: subprocess.CompletedProcess[str],
) -> str:
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    lowered = output.lower()

    if completed.returncode == 2:
        return STATUS_ERROR
    if spec.command_id == "pyright_advisory":
        if "status: tooling_config_blocker" in lowered or "status: error" in lowered:
            return STATUS_ERROR
        if "status: advisory_findings" in lowered or "status: local_resolver_noise" in lowered:
            return STATUS_ADVISORY
        return STATUS_PASSED if completed.returncode == 0 else STATUS_ERROR
    if completed.returncode != 0:
        return STATUS_FAILED
    if spec.command_id == "secret_private_marker_scan":
        return STATUS_WARNING if "result: warning" in lowered or _has_count(output, "warnings") else STATUS_PASSED
    if spec.command_id == "protected_surface_gate":
        return STATUS_WARNING if _has_count(output, "warnings") else STATUS_PASSED
    if spec.command_id == "surface_authorization":
        if "authorization_status: error" in lowered:
            return STATUS_ERROR
        if "authorization_status: review" in lowered:
            return STATUS_WARNING
        return STATUS_PASSED
    if spec.command_id == "validation_selector":
        return STATUS_WARNING if "selection_status: warning" in lowered else STATUS_PASSED
    if spec.command_id == "agent_docs_checker":
        return STATUS_WARNING if "result: warning" in lowered or _has_count(output, "warnings") else STATUS_PASSED
    return STATUS_PASSED


def _default_runner(
    command: Sequence[str],
    cwd: Path,
    stdin_text: str,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            list(command),
            cwd=cwd,
            check=False,
            input=stdin_text if stdin_text else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        return subprocess.CompletedProcess(list(command), 2, stdout="", stderr=str(exc))


def _planned_result(spec: CommandSpec) -> CommandResult:
    return CommandResult(
        command_id=spec.command_id,
        priority=spec.priority,
        status=STATUS_PLANNED,
        command=spec.command_string,
        source_tool=spec.source_tool,
        summary="planned_not_executed",
    )


def _skipped_result(spec: CommandSpec) -> CommandResult:
    return CommandResult(
        command_id=spec.command_id,
        priority=spec.priority,
        status=STATUS_SKIPPED,
        command=spec.command_string,
        source_tool=spec.source_tool,
        skip_reason=spec.skip_reason,
        summary=spec.skip_reason,
    )


def _executed_result(
    spec: CommandSpec,
    completed: subprocess.CompletedProcess[str],
) -> CommandResult:
    status = classify_command_result(spec, completed)
    return CommandResult(
        command_id=spec.command_id,
        priority=spec.priority,
        status=status,
        command=spec.command_string,
        source_tool=spec.source_tool,
        exit_code=completed.returncode,
        summary=summarize_output(completed.stdout or "", completed.stderr or ""),
    )


def _normalize_stdin_paths(raw_text: str, *, repo_root: Path) -> str:
    normalized: set[str] = set()
    for raw_line in raw_text.splitlines():
        text = raw_line.strip()
        if not text:
            continue
        candidate = Path(text)
        if candidate.is_absolute():
            resolved = candidate.resolve(strict=False)
            try:
                text = resolved.relative_to(repo_root).as_posix()
            except ValueError as exc:
                raise ConfigError("stdin path is outside the repository root: <redacted-outside-repo-path>") from exc
        text = text.replace("\\", "/")
        while text.startswith("./"):
            text = text[2:]
        text = text.lstrip("/")
        parts = [part for part in text.split("/") if part and part != "."]
        if parts:
            normalized.add("/".join(parts))
    return "".join(f"{path}\n" for path in sorted(normalized))


def validate_report_output_path(path_text: str, *, repo_root: str | Path = ".") -> str:
    if not path_text:
        return ""
    root = Path(repo_root).resolve()
    path = Path(path_text)
    resolved = path if path.is_absolute() else root / path
    try:
        relative = resolved.resolve(strict=False).relative_to(root).as_posix()
    except ValueError as exc:
        raise ConfigError("output path must be under docs/contract_test_reports/") from exc
    if not relative.startswith(APPROVED_REPORT_PREFIX) or relative == APPROVED_REPORT_PREFIX.rstrip("/"):
        raise ConfigError("output path must be under docs/contract_test_reports/")
    return relative


def run_orchestrator(
    *,
    profile: str,
    base: str,
    repo_root: str | Path = ".",
    run: bool = False,
    paths_from_stdin: bool = False,
    stdin_text: str = "",
    authorization_files: Iterable[str] = (),
    evidence_manifest: str = "",
    hardening_report_output: str = "",
    runner: Runner = _default_runner,
) -> OrchestratorResult:
    root = Path(repo_root).resolve()
    if not root.exists() or not root.is_dir():
        raise ConfigError(f"invalid repository root: {repo_root}")
    if profile not in PROFILES:
        raise ConfigError(f"unknown profile: {profile}")
    if evidence_manifest and profile != PROFILE_POST_HARDENING:
        raise ConfigError("--evidence-manifest is only valid with --profile post-hardening")
    if hardening_report_output and (profile != PROFILE_POST_HARDENING or not run):
        raise ConfigError("--hardening-report-output is only valid with --profile post-hardening --run")

    report_output = validate_report_output_path(hardening_report_output, repo_root=root)
    stdin_paths = _normalize_stdin_paths(stdin_text, repo_root=root) if paths_from_stdin else ""
    run_mode = RUN_MODE_RUN if run and profile != PROFILE_PLAN else RUN_MODE_PLAN
    plan = build_command_plan(
        profile=profile,
        base=base,
        authorization_files=authorization_files,
        paths_from_stdin=paths_from_stdin,
        evidence_manifest=evidence_manifest,
        hardening_report_output=report_output,
    )

    results: list[CommandResult] = []
    for spec in plan:
        if spec.skip_reason:
            results.append(_skipped_result(spec))
            continue
        if run_mode == RUN_MODE_PLAN:
            results.append(_planned_result(spec))
            continue
        completed = runner(
            spec.command,
            root,
            stdin_paths if spec.compatible_with_stdin_paths else "",
        )
        results.append(_executed_result(spec, completed))

    return OrchestratorResult(
        profile=profile,
        run_mode=run_mode,
        base=base,
        commands=tuple(results),
    )


def render_json(result: OrchestratorResult) -> str:
    return json.dumps(
        {
            "object": OBJECT_KIND,
            "schema_version": SCHEMA_VERSION,
            "profile": result.profile,
            "run_mode": result.run_mode,
            "base": result.base,
            "orchestrator_status": result.orchestrator_status,
            "merge_readiness": "not_decided_by_orchestrator",
            "deploy_readiness": "not_decided_by_orchestrator",
            "tracker_completion": "not_decided_by_orchestrator",
            "commands": [asdict(item) for item in result.commands],
        },
        indent=2,
        sort_keys=True,
    )


def render_text(result: OrchestratorResult) -> str:
    skipped = [item for item in result.commands if item.status == STATUS_SKIPPED]
    warning_advisory = [
        item for item in result.commands if item.status in {STATUS_WARNING, STATUS_ADVISORY}
    ]
    missing = [item for item in result.commands if item.status in {STATUS_SKIPPED, STATUS_ERROR}]
    lines = [
        "Hardening Orchestrator",
        f"schema_version: {SCHEMA_VERSION}",
        f"profile: {result.profile}",
        f"run_mode: {result.run_mode}",
        f"base: {result.base}",
        f"orchestrator_status: {result.orchestrator_status}",
        "merge_readiness: not_decided_by_orchestrator",
        "deploy_readiness: not_decided_by_orchestrator",
        "tracker_completion: not_decided_by_orchestrator",
        "",
        "## Commands",
    ]
    for item in result.commands:
        exit_code = "<not_executed>" if item.exit_code is None else str(item.exit_code)
        detail = item.skip_reason or item.summary
        lines.append(
            f"- {item.command_id} | priority={item.priority} | status={item.status} | "
            f"exit_code={exit_code} | source={item.source_tool} | command={item.command} | summary={detail}",
        )

    lines.extend(["", "## Skipped Commands"])
    if skipped:
        lines.extend(f"- {item.command_id}: {item.skip_reason}" for item in skipped)
    else:
        lines.append("- <none>")

    lines.extend(["", "## Warnings And Advisory Results"])
    if warning_advisory:
        lines.extend(f"- {item.command_id}: {item.status} - {item.summary}" for item in warning_advisory)
    else:
        lines.append("- <none>")

    lines.extend(["", "## Missing Or Not Configured"])
    if missing:
        lines.extend(f"- {item.command_id}: {item.status} - {item.skip_reason or item.summary}" for item in missing)
    else:
        lines.append("- <none>")

    lines.extend(
        [
            "",
            "## Summary",
            "- The orchestrator reports command planning and local execution results only.",
            "- It does not decide validation truth, merge readiness, deploy readiness, or tracker completion.",
            f"- Overall status: {result.orchestrator_status}",
            "",
            "## Workflow Handoff",
            "- Next role depends on the surrounding issue workflow; this output is not a PR, merge, or deploy verdict.",
        ],
    )
    return "\n".join(lines)


def write_summary_output(path_text: str, summary: str, *, repo_root: str | Path = ".") -> None:
    relative = validate_report_output_path(path_text, repo_root=repo_root)
    target = Path(repo_root).resolve() / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(summary, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan or run Mythic Edge repo-wide hardening checks.")
    parser.add_argument("--base", required=True, help="Base git ref for changed-file tools.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument("--profile", choices=PROFILES, default=PROFILE_PLAN, help="Hardening profile.")
    parser.add_argument("--run", action="store_true", help="Execute the selected runnable profile.")
    parser.add_argument(
        "--paths-from-stdin",
        action="store_true",
        help="Read newline-delimited paths once and forward them to compatible tools.",
    )
    parser.add_argument(
        "--authorization-file",
        action="append",
        default=[],
        help="Repeatable kind=path input for tools/check_surface_authorization.py.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Summary format.")
    parser.add_argument(
        "--summary-output",
        default="",
        help="Optional Markdown summary path under docs/contract_test_reports/.",
    )
    parser.add_argument(
        "--hardening-report-output",
        default="",
        help="Optional report-generator output path under docs/contract_test_reports/ for post-hardening --run.",
    )
    parser.add_argument(
        "--evidence-manifest",
        default="",
        help="Optional evidence manifest forwarded to the hardening report generator in post-hardening.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    try:
        result = run_orchestrator(
            profile=args.profile,
            base=args.base,
            repo_root=args.repo_root,
            run=args.run,
            paths_from_stdin=args.paths_from_stdin,
            stdin_text=sys.stdin.read() if args.paths_from_stdin else "",
            authorization_files=args.authorization_file,
            evidence_manifest=args.evidence_manifest,
            hardening_report_output=args.hardening_report_output,
        )
        text_output = render_text(result)
        output = render_json(result) if args.format == "json" else text_output
        if args.summary_output:
            write_summary_output(args.summary_output, text_output, repo_root=args.repo_root)
        print(output)
        return result.exit_code
    except ConfigError as exc:
        result = OrchestratorResult(
            profile=args.profile,
            run_mode=RUN_MODE_PLAN,
            base=args.base,
            commands=(),
            error=str(exc),
        )
        output = render_json(result) if args.format == "json" else render_text(result)
        print(f"ERROR configuration - {exc}", file=sys.stderr)
        print(output, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
