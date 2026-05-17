"""Select advisory validation commands for changed Mythic Edge paths."""

from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

MODE_CHANGED = "changed-files"
MODE_STDIN = "paths-from-stdin"

PRIORITY_REQUIRED = "required"
PRIORITY_RECOMMENDED = "recommended"
PRIORITY_ADVISORY = "advisory"

STATUS_OK = "ok"
STATUS_WARNING = "warning"
STATUS_ERROR = "error"

PRIORITY_ORDER = {
    PRIORITY_REQUIRED: 0,
    PRIORITY_RECOMMENDED: 1,
    PRIORITY_ADVISORY: 2,
}

PROTECTED_CATEGORY_GROUPS = {
    "parser_surface",
    "parser_state_or_model_surface",
    "extractor_surface",
    "runtime_app_surface",
    "workbook_schema_or_export_surface",
    "webhook_or_output_surface",
    "apps_script_surface",
}

FOCUSED_TEST_MAPPINGS: tuple[tuple[str, str], ...] = (
    ("tools/select_validation.py", "python3 -m pytest -q tests/test_select_validation.py"),
    ("tests/test_select_validation.py", "python3 -m pytest -q tests/test_select_validation.py"),
    ("tools/check_secret_patterns.py", "python3 -m pytest -q tests/test_check_secret_patterns.py"),
    ("tests/test_check_secret_patterns.py", "python3 -m pytest -q tests/test_check_secret_patterns.py"),
    ("tools/check_protected_surfaces.py", "python3 -m pytest -q tests/test_check_protected_surfaces.py"),
    ("tests/test_check_protected_surfaces.py", "python3 -m pytest -q tests/test_check_protected_surfaces.py"),
    ("tools/check_surface_authorization.py", "python3 -m pytest -q tests/test_check_surface_authorization.py"),
    ("tests/test_check_surface_authorization.py", "python3 -m pytest -q tests/test_check_surface_authorization.py"),
    (
        "src/mythic_edge_parser/parsers/gre/connect_resp.py",
        "python3 -m pytest -q tests/test_gre_connect_resp_parser.py",
    ),
    ("src/mythic_edge_parser/parsers/gre/game_result.py", "python3 -m pytest -q tests/test_gre_game_result_parser.py"),
    ("src/mythic_edge_parser/parsers/gre/game_state.py", "python3 -m pytest -q tests/test_gre_game_state_parser.py"),
    ("src/mythic_edge_parser/parsers/gre/turn_info.py", "python3 -m pytest -q tests/test_gre_turn_info_parser.py"),
    (
        "src/mythic_edge_parser/parsers/match_state.py",
        "python3 -m pytest -q tests/test_match_state_parser.py tests/test_match_summary_from_match_state.py",
    ),
    ("src/mythic_edge_parser/parsers/api_common.py", "python3 -m pytest -q tests/test_api_common.py"),
    ("src/mythic_edge_parser/parsers/client_actions.py", "python3 -m pytest -q tests/test_client_actions_parser.py"),
    ("src/mythic_edge_parser/app/event_identity.py", "python3 -m pytest -q tests/test_event_identity.py"),
    ("src/mythic_edge_parser/app/state.py", "python3 -m pytest -q tests/test_state.py"),
    ("src/mythic_edge_parser/app/models.py", "python3 -m pytest -q tests/test_app_models.py tests/test_events.py"),
    ("src/mythic_edge_parser/app/extractors.py", "python3 -m pytest -q tests/test_app_extractors.py"),
    ("src/mythic_edge_parser/app/runner.py", "python3 -m pytest -q tests/test_runner.py"),
    ("src/mythic_edge_parser/app/outputs.py", "python3 -m pytest -q tests/test_app_outputs.py"),
    (
        "src/mythic_edge_parser/app/sheet_schema.py",
        "python3 -m pytest -q tests/test_sheet_schema.py tests/test_event_schema_snapshots.py",
    ),
    (
        "src/mythic_edge_parser/app/sheet_exports.py",
        "python3 -m pytest -q tests/test_sheet_exports.py tests/test_event_schema_snapshots.py",
    ),
    (
        "src/mythic_edge_parser/app/transforms.py",
        "python3 -m pytest -q tests/test_transforms.py tests/test_event_schema_snapshots.py",
    ),
    ("src/mythic_edge_parser/app/runtime_surfaces.py", "python3 -m pytest -q tests/test_runtime_surfaces.py"),
    ("src/mythic_edge_parser/app/diagnostics.py", "python3 -m pytest -q tests/test_diagnostics.py"),
    ("src/mythic_edge_parser/app/log_drift_sensor.py", "python3 -m pytest -q tests/test_log_drift_sensor.py"),
    ("src/mythic_edge_parser/app/status_api.py", "python3 -m pytest -q tests/test_status_api.py"),
    (
        "src/mythic_edge_parser/stream.py",
        "python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py",
    ),
)


@dataclass(frozen=True)
class Recommendation:
    priority: str
    command_id: str
    command: str
    reason: str
    categories: tuple[str, ...]
    paths: tuple[str, ...]


@dataclass(frozen=True)
class SelectorWarning:
    category_id: str
    path: str
    reason: str


@dataclass(frozen=True)
class AdvisoryNote:
    note_id: str
    message: str


@dataclass(frozen=True)
class SelectionResult:
    mode: str
    base: str
    head: str
    changed_paths: tuple[str, ...]
    categories: tuple[str, ...]
    recommendations: tuple[Recommendation, ...]
    warnings: tuple[SelectorWarning, ...]
    notes: tuple[AdvisoryNote, ...]
    error: str = ""

    @property
    def required(self) -> tuple[Recommendation, ...]:
        return tuple(item for item in self.recommendations if item.priority == PRIORITY_REQUIRED)

    @property
    def recommended(self) -> tuple[Recommendation, ...]:
        return tuple(item for item in self.recommendations if item.priority == PRIORITY_RECOMMENDED)

    @property
    def advisory(self) -> tuple[Recommendation, ...]:
        return tuple(item for item in self.recommendations if item.priority == PRIORITY_ADVISORY)

    @property
    def selection_status(self) -> str:
        if self.error:
            return STATUS_ERROR
        if self.warnings:
            return STATUS_WARNING
        return STATUS_OK

    @property
    def exit_code(self) -> int:
        return 2 if self.error else 0


def normalize_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    text = text.lstrip("/")
    parts = [part for part in text.split("/") if part and part != "."]
    return "/".join(parts)


def _repo_relative_path(raw_path: str | Path, repo_root: Path) -> tuple[str, bool]:
    text = str(raw_path).strip()
    if not text:
        return "", False
    candidate = Path(text)
    if candidate.is_absolute():
        resolved = candidate.resolve(strict=False)
        try:
            return resolved.relative_to(repo_root).as_posix(), False
        except ValueError:
            return "", True
    return normalize_path(text), False


def normalize_paths(
    paths: Iterable[str | Path],
    *,
    repo_root: str | Path = ".",
) -> tuple[tuple[str, ...], tuple[SelectorWarning, ...]]:
    root = Path(repo_root).resolve()
    normalized: set[str] = set()
    warnings: list[SelectorWarning] = []
    for raw_path in paths:
        path, outside = _repo_relative_path(raw_path, root)
        if outside:
            warnings.append(
                SelectorWarning(
                    "outside_repo_path_ignored",
                    "<redacted-outside-repo-path>",
                    "Outside-repo stdin path was ignored.",
                ),
            )
            continue
        if path:
            normalized.add(path)
    return tuple(sorted(normalized)), tuple(warnings)


def _matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(f"{prefix}/")
    return fnmatch.fnmatchcase(path, pattern)


def categorize_path(path: str) -> tuple[str, ...]:
    categories: set[str] = set()
    if _matches(path, "src/mythic_edge_parser/parsers/**") or path == "src/mythic_edge_parser/events.py":
        categories.add("parser_surface")
    if path in {"src/mythic_edge_parser/app/state.py", "src/mythic_edge_parser/app/models.py"}:
        categories.add("parser_state_or_model_surface")
    if path == "src/mythic_edge_parser/app/extractors.py":
        categories.add("extractor_surface")
    if path in {
        "src/mythic_edge_parser/app/runner.py",
        "src/mythic_edge_parser/app/config.py",
        "src/mythic_edge_parser/stream.py",
    }:
        categories.add("runtime_app_surface")
    if path in {
        "src/mythic_edge_parser/app/sheet_schema.py",
        "src/mythic_edge_parser/app/sheet_exports.py",
        "src/mythic_edge_parser/app/transforms.py",
    } or _matches(path, "tests/fixtures/schema_snapshots/**"):
        categories.add("workbook_schema_or_export_surface")
    if path in {
        "src/mythic_edge_parser/app/outputs.py",
        "src/mythic_edge_parser/app/transforms.py",
        "src/mythic_edge_parser/app/runner.py",
    }:
        categories.add("webhook_or_output_surface")
    if _matches(path, "tools/google_apps_script/**"):
        categories.add("apps_script_surface")
    if (
        fnmatch.fnmatchcase(path, "tools/check_*.py")
        or path == "tools/select_validation.py"
        or fnmatch.fnmatchcase(path, "tests/test_check_*.py")
        or path == "tests/test_select_validation.py"
    ):
        categories.add("hardening_tool_surface")
    if (
        path == "AGENTS.md"
        or path in {"docs/agent_constitution.md", "docs/agent_rules.yml", "docs/codex_module_workflow.md"}
        or _matches(path, "docs/agent_threads/**")
        or _matches(path, "docs/templates/**")
        or _matches(path, ".github/ISSUE_TEMPLATE/**")
        or path == ".github/pull_request_template.md"
    ):
        categories.add("governance_docs_surface")
    if (
        _matches(path, "docs/contracts/**")
        or _matches(path, "docs/implementation_handoffs/**")
        or _matches(path, "docs/contract_test_reports/**")
        or _matches(path, "docs/problem_representations/**")
    ):
        categories.add("contract_or_report_docs_surface")
    if _matches(path, ".github/workflows/**") or path == "pyproject.toml":
        categories.add("ci_or_dependency_surface")
    if _matches(path, "tests/fixtures/**"):
        categories.add("fixture_surface")
    if fnmatch.fnmatchcase(path, "tests/test_*.py"):
        categories.add("test_surface")
    if path.endswith(".md") and not categories:
        categories.add("docs_only_surface")
    return tuple(sorted(categories))


def categorize_paths(paths: Iterable[str]) -> dict[str, tuple[str, ...]]:
    return {path: categorize_path(path) for path in paths}


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


def is_tracked_file(path: str, *, repo_root: str | Path = ".") -> bool:
    command = ["git", "ls-files", "--error-unmatch", path]
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError:
        return False
    return completed.returncode == 0


def _load_protected_surface_gate():
    module_path = Path(__file__).with_name("check_protected_surfaces.py")
    module_name = "check_protected_surfaces_for_selector"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def classify_protected_warnings(paths: Iterable[str]) -> tuple[SelectorWarning, ...]:
    gate = _load_protected_surface_gate()
    if gate is None:
        return ()
    warnings: list[SelectorWarning] = []
    for item in gate.classify_paths(paths):
        if item.severity == gate.SEVERITY_ALLOWED:
            continue
        prefix = (
            "Forbidden path classification"
            if item.severity == gate.SEVERITY_FORBIDDEN
            else "Protected path classification"
        )
        warnings.append(SelectorWarning(item.category_id, item.path, f"{prefix}: {item.reason}"))
    return tuple(warnings)


def _command_id_for_pytest(command: str) -> str:
    if "tests/test_select_validation.py" in command:
        return "select_validation_tests"
    if "tests/test_check_secret_patterns.py" in command:
        return "secret_pattern_tests"
    if "tests/test_check_protected_surfaces.py" in command:
        return "protected_surface_tests"
    if "tests/test_check_surface_authorization.py" in command:
        return "surface_authorization_tests"
    if "tests/test_event_schema_snapshots.py" in command:
        return "schema_snapshot_tests"
    if "tests/test_parser_regressions.py" in command:
        return "parser_regression_tests"
    if command.startswith("python3 -m pytest -q tests/test_"):
        return command.removeprefix("python3 -m pytest -q ").replace("/", "_").replace(" ", "_")
    return command.replace(" ", "_")


def _add_recommendation(
    recommendations: dict[str, Recommendation],
    *,
    priority: str,
    command_id: str,
    command: str,
    reason: str,
    categories: Iterable[str],
    paths: Iterable[str],
) -> None:
    categories_tuple = tuple(sorted(set(categories)))
    paths_tuple = tuple(sorted(set(paths)))
    existing = recommendations.get(command)
    if existing is None:
        recommendations[command] = Recommendation(
            priority,
            command_id,
            command,
            reason,
            categories_tuple,
            paths_tuple,
        )
        return
    priority_value = min(PRIORITY_ORDER[existing.priority], PRIORITY_ORDER[priority])
    merged_priority = next(key for key, value in PRIORITY_ORDER.items() if value == priority_value)
    recommendations[command] = Recommendation(
        merged_priority,
        existing.command_id,
        command,
        existing.reason,
        tuple(sorted(set(existing.categories) | set(categories_tuple))),
        tuple(sorted(set(existing.paths) | set(paths_tuple))),
    )


def _focused_test_for_path(path: str) -> str:
    for exact_path, command in FOCUSED_TEST_MAPPINGS:
        if path == exact_path:
            return command
    if fnmatch.fnmatchcase(path, "tests/fixtures/parser_regression_*"):
        return "python3 -m pytest -q tests/test_parser_regressions.py"
    if _matches(path, "tests/fixtures/schema_snapshots/**"):
        return "python3 -m pytest -q tests/test_event_schema_snapshots.py"
    if fnmatch.fnmatchcase(path, "tests/test_*.py"):
        return f"python3 -m pytest -q {path}"
    return ""


def select_recommendations(
    paths: tuple[str, ...],
    *,
    base: str,
    repo_root: str | Path = ".",
) -> tuple[tuple[Recommendation, ...], tuple[AdvisoryNote, ...], tuple[str, ...]]:
    path_categories = categorize_paths(paths)
    categories = tuple(sorted({category for items in path_categories.values() for category in items}))
    recommendations: dict[str, Recommendation] = {}
    notes: list[AdvisoryNote] = []

    if not paths:
        notes.append(
            AdvisoryNote(
                "zero_changed_paths",
                (
                    "No changed paths were selected. Baseline reporters may still run the protected-surface gate, "
                    "secret/private-marker scan, and git diff --check for explicit zero-diff evidence."
                ),
            ),
        )
        return (), tuple(notes), categories

    _add_recommendation(
        recommendations,
        priority=PRIORITY_REQUIRED,
        command_id="protected_surface_gate",
        command=f"python3 tools/check_protected_surfaces.py --base {base}",
        reason="Changed paths must be checked for forbidden and protected surfaces.",
        categories=("always_changed_paths", *categories),
        paths=paths,
    )
    _add_recommendation(
        recommendations,
        priority=PRIORITY_REQUIRED,
        command_id="secret_private_marker_scan",
        command=f"python3 tools/check_secret_patterns.py --base {base}",
        reason="Changed paths must be scanned for secrets and private markers.",
        categories=("always_changed_paths", *categories),
        paths=paths,
    )
    _add_recommendation(
        recommendations,
        priority=PRIORITY_REQUIRED,
        command_id="diff_check",
        command="git diff --check",
        reason="Changed files should be checked for whitespace and patch formatting issues.",
        categories=("always_changed_paths", *categories),
        paths=paths,
    )

    python_paths = tuple(
        path
        for path in paths
        if path.endswith(".py") and (path.startswith(("src/", "tests/", "tools/")) or path == "pyproject.toml")
    )
    if python_paths or "ci_or_dependency_surface" in categories:
        _add_recommendation(
            recommendations,
            priority=PRIORITY_REQUIRED,
            command_id="ruff",
            command="python3 -m ruff check src tests tools",
            reason="Python or dependency validation surfaces changed; Ruff should inspect source, tests, and tools.",
            categories=categories,
            paths=python_paths or paths,
        )

    pyright_paths = tuple(
        path
        for path in paths
        if path.startswith("src/") or (path.startswith("tools/") and path.endswith(".py")) or path == "pyproject.toml"
    )
    if pyright_paths:
        _add_recommendation(
            recommendations,
            priority=PRIORITY_RECOMMENDED,
            command_id="pyright_advisory",
            command="python3 -m pyright",
            reason=(
                "Source, hardening tool, or dependency configuration changed; type checking is useful before review."
            ),
            categories=categories,
            paths=pyright_paths,
        )

    source_without_mapping: list[str] = []
    for path, item_categories in path_categories.items():
        focused_command = _focused_test_for_path(path)
        if focused_command:
            _add_recommendation(
                recommendations,
                priority=PRIORITY_REQUIRED,
                command_id=_command_id_for_pytest(focused_command),
                command=focused_command,
                reason="Changed path has a focused test mapping in the validation selector contract.",
                categories=item_categories,
                paths=(path,),
            )
        elif path.startswith("src/") and path.endswith(".py"):
            source_without_mapping.append(path)

    if source_without_mapping:
        _add_recommendation(
            recommendations,
            priority=PRIORITY_RECOMMENDED,
            command_id="full_pytest",
            command="python3 -m pytest -q tests",
            reason="A source path changed without a focused selector mapping; broader tests are recommended.",
            categories=categories,
            paths=source_without_mapping,
        )

    if "ci_or_dependency_surface" in categories:
        _add_recommendation(
            recommendations,
            priority=PRIORITY_RECOMMENDED,
            command_id="full_pytest",
            command="python3 -m pytest -q tests",
            reason="CI or dependency configuration changed; full tests are recommended before review.",
            categories=("ci_or_dependency_surface",),
            paths=tuple(path for path, cats in path_categories.items() if "ci_or_dependency_surface" in cats),
        )

    touched_protected_groups = categories and (set(categories) & PROTECTED_CATEGORY_GROUPS)
    if len(touched_protected_groups) > 1:
        _add_recommendation(
            recommendations,
            priority=PRIORITY_RECOMMENDED,
            command_id="full_pytest",
            command="python3 -m pytest -q tests",
            reason=(
                "Multiple protected parser/runtime/workbook/output categories changed; broader tests are recommended."
            ),
            categories=touched_protected_groups,
            paths=paths,
        )

    protected_classifications = classify_protected_warnings(paths)
    if protected_classifications:
        _add_recommendation(
            recommendations,
            priority=PRIORITY_RECOMMENDED,
            command_id="protected_surface_authorization",
            command=(
                f"python3 tools/check_surface_authorization.py --base {base} "
                "--authorization-file issue=<issue-body-file> "
                "--authorization-file contract=<contract-file> "
                "--authorization-file pr=<pr-body-file>"
            ),
            reason=(
                "Protected or forbidden path classifications should be compared against explicit "
                "authorization evidence."
            ),
            categories=tuple(item.category_id for item in protected_classifications),
            paths=tuple(item.path for item in protected_classifications),
        )

    governance_paths = tuple(
        path for path, cats in path_categories.items() if "governance_docs_surface" in cats
    )
    contract_report_paths = tuple(
        path for path, cats in path_categories.items() if "contract_or_report_docs_surface" in cats
    )
    if governance_paths or contract_report_paths:
        if is_tracked_file("tools/check_agent_docs.py", repo_root=repo_root):
            priority = PRIORITY_REQUIRED if governance_paths else PRIORITY_RECOMMENDED
            trigger_categories = []
            if governance_paths:
                trigger_categories.append("governance_docs_surface")
            if contract_report_paths:
                trigger_categories.append("contract_or_report_docs_surface")
            _add_recommendation(
                recommendations,
                priority=priority,
                command_id="agent_docs_checker",
                command="python3 tools/check_agent_docs.py",
                reason=(
                    "Governance or contract/report docs changed and the agent-docs checker is tracked on this branch."
                ),
                categories=trigger_categories,
                paths=(*governance_paths, *contract_report_paths),
            )
        elif governance_paths:
            notes.append(
                AdvisoryNote(
                    "agent_docs_checker_unavailable",
                    "Governance docs changed, but tools/check_agent_docs.py is not tracked on this branch.",
                ),
            )

    sorted_recommendations = tuple(
        sorted(
            recommendations.values(),
            key=lambda item: (PRIORITY_ORDER[item.priority], item.command_id, item.command),
        ),
    )
    return sorted_recommendations, tuple(notes), categories


def run_selector_for_paths(
    paths: Iterable[str | Path],
    *,
    base: str,
    repo_root: str | Path = ".",
    mode: str = MODE_STDIN,
) -> SelectionResult:
    normalized_paths, path_warnings = normalize_paths(paths, repo_root=repo_root)
    recommendations, notes, categories = select_recommendations(
        normalized_paths,
        base=base,
        repo_root=repo_root,
    )
    protected_warnings = classify_protected_warnings(normalized_paths)
    warnings = tuple(
        sorted(
            path_warnings + protected_warnings,
            key=lambda item: (item.category_id, item.path, item.reason),
        ),
    )
    return SelectionResult(
        mode=mode,
        base=base,
        head="HEAD",
        changed_paths=normalized_paths,
        categories=categories,
        recommendations=recommendations,
        warnings=warnings,
        notes=notes,
    )


def run_selector(base: str, *, repo_root: str | Path = ".") -> SelectionResult:
    root = Path(repo_root).resolve()
    if not root.exists() or not root.is_dir():
        return SelectionResult(
            MODE_CHANGED,
            base,
            "HEAD",
            (),
            (),
            (),
            (),
            (),
            error=f"invalid repository root: {repo_root}",
        )
    try:
        paths = collect_changed_paths(base, repo_root=root)
    except RuntimeError as exc:
        return SelectionResult(MODE_CHANGED, base, "HEAD", (), (), (), (), (), error=str(exc))
    return run_selector_for_paths(paths, base=base, repo_root=root, mode=MODE_CHANGED)


def render_report(result: SelectionResult) -> str:
    lines = [
        "Validation Selector",
        f"mode: {result.mode}",
        f"base: {result.base}",
        f"head: {result.head}",
        f"changed_paths: {len(result.changed_paths)}",
        f"categories: {len(result.categories)}",
        f"required: {len(result.required)}",
        f"recommended: {len(result.recommended)}",
        f"advisory: {len(result.advisory) + len(result.notes)}",
        f"warnings: {len(result.warnings)}",
        "",
    ]
    if result.error:
        lines.append(f"ERROR configuration - {result.error}")
    else:
        for recommendation in result.recommendations:
            lines.extend(
                [
                    f"{recommendation.priority.upper()} {recommendation.command_id}",
                    f"command: {recommendation.command}",
                    f"reason: {recommendation.reason}",
                    f"categories: {', '.join(recommendation.categories) if recommendation.categories else '<none>'}",
                    f"paths: {', '.join(recommendation.paths) if recommendation.paths else '<none>'}",
                    "",
                ],
            )
        for note in result.notes:
            lines.append(f"ADVISORY {note.note_id} - {note.message}")
        for warning in result.warnings:
            lines.append(f"WARNING {warning.category_id} {warning.path} - {warning.reason}")
    if lines[-1] != "":
        lines.append("")
    lines.append(f"selection_status: {result.selection_status}")
    return "\n".join(lines)


def render_json(result: SelectionResult) -> str:
    return json.dumps(
        {
            "mode": result.mode,
            "base": result.base,
            "head": result.head,
            "changed_paths": list(result.changed_paths),
            "categories": list(result.categories),
            "recommendations": [asdict(item) for item in result.recommendations],
            "warnings": [asdict(item) for item in result.warnings],
            "notes": [asdict(item) for item in result.notes],
            "selection_status": result.selection_status,
        },
        indent=2,
        sort_keys=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select recommended validation commands for changed paths.")
    parser.add_argument("--base", required=True, help="Base git ref for <base>...HEAD.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--paths-from-stdin",
        action="store_true",
        help="Read newline-delimited paths from stdin instead of running git diff.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Report format.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    if args.paths_from_stdin:
        result = run_selector_for_paths(
            sys.stdin.read().splitlines(),
            base=args.base,
            repo_root=args.repo_root,
            mode=MODE_STDIN,
        )
    else:
        result = run_selector(args.base, repo_root=args.repo_root)

    output = render_json(result) if args.format == "json" else render_report(result)
    stream = sys.stderr if result.error else sys.stdout
    print(output, file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
