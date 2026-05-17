from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "select_validation.py"
SPEC = importlib.util.spec_from_file_location("select_validation", MODULE_PATH)
assert SPEC is not None
selector = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = selector
assert SPEC.loader is not None
SPEC.loader.exec_module(selector)


def _commands(result) -> dict[str, str]:
    return {item.command_id: item.command for item in result.recommendations}


def test_missing_base_exits_two(capsys) -> None:
    assert selector.main([]) == 2

    captured = capsys.readouterr()
    assert "--base" in captured.err


def test_invalid_base_diff_reports_error(monkeypatch, capsys) -> None:
    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 128, stdout="", stderr="bad revision")

    monkeypatch.setattr(selector.subprocess, "run", fake_run)

    assert selector.main(["--base", "missing/ref"]) == 2

    captured = capsys.readouterr()
    assert "selection_status: error" in captured.err
    assert "bad revision" in captured.err


def test_changed_path_mode_uses_contract_git_diff_command(monkeypatch, tmp_path: Path) -> None:
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, stdout="tools/select_validation.py\n", stderr="")

    monkeypatch.setattr(selector.subprocess, "run", fake_run)

    result = selector.run_selector("origin/main", repo_root=tmp_path)

    assert result.changed_paths == ("tools/select_validation.py",)
    command, kwargs = calls[0]
    assert command == [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        "origin/main...HEAD",
    ]
    assert kwargs["cwd"] == tmp_path.resolve()


def test_stdin_mode_does_not_run_git_diff(monkeypatch, capsys) -> None:
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(selector.subprocess, "run", fake_run)
    monkeypatch.setattr(selector.sys, "stdin", io.StringIO("tools/select_validation.py\n"))

    assert selector.main(["--base", "origin/main", "--paths-from-stdin"]) == 0

    captured = capsys.readouterr()
    assert "mode: paths-from-stdin" in captured.out
    assert all("diff" not in command for command in calls)


def test_path_normalization_deduplicates_sorts_and_redacts_outside_paths(tmp_path: Path) -> None:
    outside = tmp_path.parent / "private" / "secret.txt"
    paths, warnings = selector.normalize_paths(
        ["./b.md", "a.md", "b.md", str(outside)],
        repo_root=tmp_path,
    )

    assert paths == ("a.md", "b.md")
    assert warnings == (
        selector.SelectorWarning(
            "outside_repo_path_ignored",
            "<redacted-outside-repo-path>",
            "Outside-repo stdin path was ignored.",
        ),
    )


def test_zero_changed_paths_emit_no_required_commands_and_baseline_advisory() -> None:
    result = selector.run_selector_for_paths((), base="origin/main")

    assert result.required == ()
    assert result.selection_status == selector.STATUS_OK
    assert result.notes[0].note_id == "zero_changed_paths"


def test_docs_only_change_uses_docs_safe_checks_without_full_parser_suite() -> None:
    result = selector.run_selector_for_paths(["README.md"], base="origin/main")
    commands = _commands(result)

    assert commands["protected_surface_gate"] == "python3 tools/check_protected_surfaces.py --base origin/main"
    assert commands["secret_private_marker_scan"] == "python3 tools/check_secret_patterns.py --base origin/main"
    assert commands["diff_check"] == "git diff --check"
    assert "full_pytest" not in commands


def test_governance_docs_do_not_select_agent_docs_checker_when_untracked(monkeypatch) -> None:
    monkeypatch.setattr(selector, "is_tracked_file", lambda path, *, repo_root=".": False)

    result = selector.run_selector_for_paths(["AGENTS.md"], base="origin/main")
    commands = _commands(result)

    assert "agent_docs_checker" not in commands
    assert result.notes == (
        selector.AdvisoryNote(
            "agent_docs_checker_unavailable",
            "Governance docs changed, but tools/check_agent_docs.py is not tracked on this branch.",
        ),
    )


def test_governance_docs_select_agent_docs_checker_when_tracked(monkeypatch) -> None:
    monkeypatch.setattr(selector, "is_tracked_file", lambda path, *, repo_root=".": True)

    result = selector.run_selector_for_paths(["docs/agent_constitution.md"], base="origin/main")
    commands = _commands(result)

    assert commands["agent_docs_checker"] == "python3 tools/check_agent_docs.py"
    agent_docs = next(item for item in result.recommendations if item.command_id == "agent_docs_checker")
    assert agent_docs.priority == "required"
    assert agent_docs.categories == ("governance_docs_surface",)
    assert agent_docs.paths == ("docs/agent_constitution.md",)


def test_contract_docs_select_recommended_agent_docs_checker_with_accurate_metadata(monkeypatch) -> None:
    monkeypatch.setattr(selector, "is_tracked_file", lambda path, *, repo_root=".": True)

    result = selector.run_selector_for_paths(
        ["docs/contracts/repo_wide_validation_selector.md"],
        base="origin/main",
    )

    agent_docs = next(item for item in result.recommendations if item.command_id == "agent_docs_checker")
    assert agent_docs.priority == "recommended"
    assert agent_docs.categories == ("contract_or_report_docs_surface",)
    assert agent_docs.paths == ("docs/contracts/repo_wide_validation_selector.md",)


def test_agent_docs_checker_metadata_aggregates_mixed_governance_and_contract_paths(monkeypatch) -> None:
    monkeypatch.setattr(selector, "is_tracked_file", lambda path, *, repo_root=".": True)

    result = selector.run_selector_for_paths(
        ["AGENTS.md", "docs/contracts/repo_wide_validation_selector.md"],
        base="origin/main",
    )

    agent_docs = next(item for item in result.recommendations if item.command_id == "agent_docs_checker")
    assert agent_docs.priority == "required"
    assert agent_docs.categories == ("contract_or_report_docs_surface", "governance_docs_surface")
    assert agent_docs.paths == ("AGENTS.md", "docs/contracts/repo_wide_validation_selector.md")


def test_hardening_tool_changes_select_matching_focused_tests() -> None:
    result = selector.run_selector_for_paths(["tools/check_secret_patterns.py"], base="origin/main")
    commands = _commands(result)

    assert commands["secret_pattern_tests"] == "python3 -m pytest -q tests/test_check_secret_patterns.py"
    assert commands["ruff"] == "python3 -m ruff check src tests tools"


def test_selector_changes_select_selector_tests() -> None:
    result = selector.run_selector_for_paths(["tests/test_select_validation.py"], base="origin/main")
    commands = _commands(result)

    assert commands["select_validation_tests"] == "python3 -m pytest -q tests/test_select_validation.py"


def test_parser_module_change_selects_focused_tests_ruff_and_pyright() -> None:
    result = selector.run_selector_for_paths(
        ["src/mythic_edge_parser/parsers/match_state.py"],
        base="origin/main",
    )
    command_values = set(_commands(result).values())

    expected = "python3 -m pytest -q tests/test_match_state_parser.py tests/test_match_summary_from_match_state.py"
    assert expected in command_values
    assert "python3 -m ruff check src tests tools" in command_values
    assert "python3 -m pyright" in command_values


def test_workbook_schema_export_change_selects_schema_snapshot_tests() -> None:
    result = selector.run_selector_for_paths(["src/mythic_edge_parser/app/sheet_schema.py"], base="origin/main")
    command_values = set(_commands(result).values())

    assert "python3 -m pytest -q tests/test_sheet_schema.py tests/test_event_schema_snapshots.py" in command_values


def test_webhook_output_change_selects_output_tests() -> None:
    result = selector.run_selector_for_paths(["src/mythic_edge_parser/app/outputs.py"], base="origin/main")
    command_values = set(_commands(result).values())

    assert "python3 -m pytest -q tests/test_app_outputs.py" in command_values


def test_fixture_changes_select_regression_or_snapshot_tests() -> None:
    result = selector.run_selector_for_paths(
        [
            "tests/fixtures/parser_regression_match_slice.log",
            "tests/fixtures/schema_snapshots/workbook_row_keys.json",
        ],
        base="origin/main",
    )
    command_values = set(_commands(result).values())

    assert "python3 -m pytest -q tests/test_parser_regressions.py" in command_values
    assert "python3 -m pytest -q tests/test_event_schema_snapshots.py" in command_values


def test_ci_or_dependency_change_recommends_broader_tests_and_pyright() -> None:
    result = selector.run_selector_for_paths(["pyproject.toml"], base="origin/main")
    commands = _commands(result)

    assert commands["full_pytest"] == "python3 -m pytest -q tests"
    assert commands["pyright_advisory"] == "python3 -m pyright"
    assert commands["ruff"] == "python3 -m ruff check src tests tools"


def test_protected_and_forbidden_path_classifications_are_warnings() -> None:
    result = selector.run_selector_for_paths(
        ["src/mythic_edge_parser/app/state.py", "data/status/runtime.json"],
        base="origin/main",
    )
    warning_categories = {warning.category_id for warning in result.warnings}

    assert "parser_state_final_reconciliation" in warning_categories
    assert "runtime_status" in warning_categories
    assert result.selection_status == selector.STATUS_WARNING


def test_duplicate_commands_are_emitted_once_with_aggregated_paths() -> None:
    result = selector.run_selector_for_paths(
        ["tools/check_secret_patterns.py", "tests/test_check_secret_patterns.py"],
        base="origin/main",
    )
    matching = [
        item
        for item in result.recommendations
        if item.command == "python3 -m pytest -q tests/test_check_secret_patterns.py"
    ]

    assert len(matching) == 1
    assert matching[0].paths == ("tests/test_check_secret_patterns.py", "tools/check_secret_patterns.py")


def test_report_uses_selection_vocabulary_not_validation_results() -> None:
    result = selector.run_selector_for_paths(["README.md"], base="origin/main")
    report = selector.render_report(result)

    assert "Validation Selector" in report
    assert "selection_status: ok" in report
    assert "validation passed" not in report.lower()
    assert "checks passed" not in report.lower()
    assert "ready to merge" not in report.lower()


def test_json_output_contains_contracted_fields(monkeypatch, capsys) -> None:
    monkeypatch.setattr(selector.sys, "stdin", io.StringIO(""))

    assert selector.main(["--base", "origin/main", "--paths-from-stdin", "--format", "json"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert set(payload) == {
        "base",
        "categories",
        "changed_paths",
        "head",
        "mode",
        "notes",
        "recommendations",
        "selection_status",
        "warnings",
    }
