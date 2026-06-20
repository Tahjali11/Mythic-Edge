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


def _recommendation(result, command_id: str):
    return next(item for item in result.recommendations if item.command_id == command_id)


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


def test_mapping_constants_are_loaded_through_selector_entrypoint() -> None:
    assert (
        "tools/select_validation.py",
        "python3 -m pytest -q tests/test_select_validation.py",
    ) in selector.FOCUSED_TEST_MAPPINGS
    assert "parser_surface" in selector.PROTECTED_CATEGORY_GROUPS


def test_hardening_report_generator_changes_select_focused_tests() -> None:
    result = selector.run_selector_for_paths(
        ["tools/generate_hardening_report.py", "tests/test_hardening_report_generator.py"],
        base="origin/main",
    )
    commands = _commands(result)

    assert (
        commands["hardening_report_generator_tests"]
        == "python3 -m pytest -q tests/test_hardening_report_generator.py"
    )
    recommendation = next(
        item for item in result.recommendations if item.command_id == "hardening_report_generator_tests"
    )
    assert recommendation.categories == ("hardening_tool_surface", "test_surface")


def test_hardening_orchestrator_changes_select_focused_tests() -> None:
    result = selector.run_selector_for_paths(
        ["tools/run_hardening_orchestrator.py", "tests/test_hardening_orchestrator.py"],
        base="origin/main",
    )
    commands = _commands(result)

    assert (
        commands["hardening_orchestrator_tests"]
        == "python3 -m pytest -q tests/test_hardening_orchestrator.py"
    )
    recommendation = next(
        item for item in result.recommendations if item.command_id == "hardening_orchestrator_tests"
    )
    assert recommendation.categories == ("hardening_tool_surface", "test_surface")


def test_parser_module_change_selects_focused_tests_ruff_and_pyright() -> None:
    result = selector.run_selector_for_paths(
        ["src/mythic_edge_parser/parsers/match_state.py"],
        base="origin/main",
    )
    command_values = set(_commands(result).values())

    expected = "python3 -m pytest -q tests/test_match_state_parser.py tests/test_match_summary_from_match_state.py"
    assert expected in command_values
    assert "python3 -m ruff check src tests tools" in command_values
    assert "python3 tools/run_pyright_advisory_report.py" in command_values
    assert _recommendation(result, "pyright_advisory").priority == "advisory"


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
    assert commands["pyright_advisory"] == "python3 tools/run_pyright_advisory_report.py"
    assert commands["ruff"] == "python3 -m ruff check src tests tools"
    assert _recommendation(result, "pyright_advisory").priority == "advisory"


def test_frontend_paths_select_frontend_checks_without_claiming_results() -> None:
    result = selector.run_selector_for_paths(
        ["frontend/src/App.tsx", "frontend/package.json"],
        base="origin/main",
    )
    commands = _commands(result)

    assert commands["frontend_typecheck"] == "npm --prefix frontend run typecheck"
    assert commands["frontend_tests"] == "npm --prefix frontend run test -- --run"
    assert commands["frontend_build"] == "npm --prefix frontend run build"
    assert _recommendation(result, "frontend_typecheck").priority == "required"
    assert "frontend_surface" in result.categories
    assert "full_pytest" not in commands


def test_local_app_backend_paths_select_focused_backend_and_history_tests() -> None:
    result = selector.run_selector_for_paths(
        ["src/mythic_edge_parser/local_app/backend.py"],
        base="origin/main",
    )
    commands = _commands(result)

    expected = (
        "python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_manual_jsonl_import.py "
        "tests/test_analytics_app_match_game_history_views.py tests/test_analytics_app_opening_hand_mulligan_views.py "
        "tests/test_analytics_app_play_draw_postboard_split_views.py "
        "tests/test_analytics_app_gameplay_action_opponent_observation_views.py"
    )
    assert commands["local_app_backend_tests"] == expected
    assert commands["ruff"] == "python3 -m ruff check src tests tools"
    assert _recommendation(result, "pyright_advisory").priority == "advisory"
    assert "local_app_surface" in result.categories
    assert "full_pytest" not in commands


def test_developer_launcher_paths_select_launcher_tests() -> None:
    result = selector.run_selector_for_paths(
        ["tools/dev_app/dev_app_launcher.py", "tools/dev_app/start_mythic_edge_dev_app.ps1"],
        base="origin/main",
    )
    commands = _commands(result)

    assert commands["dev_app_launcher_tests"] == "python3 -m pytest -q tests/test_analytics_dev_app_launcher.py"
    recommendation = _recommendation(result, "dev_app_launcher_tests")
    assert recommendation.categories == ("developer_launcher_surface",)
    assert recommendation.paths == (
        "tools/dev_app/dev_app_launcher.py",
        "tools/dev_app/start_mythic_edge_dev_app.ps1",
    )


def test_analytics_migration_paths_select_schema_loader_and_view_tests() -> None:
    result = selector.run_selector_for_paths(
        ["src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql"],
        base="origin/main",
    )
    commands = _commands(result)

    assert (
        commands["analytics_migration_tests"]
        == "python3 -m pytest -q tests/test_analytics_migration_loader.py tests/test_analytics_schema.py "
        "tests/test_analytics_derived_views.py"
    )
    assert "analytics_schema_surface" in result.categories
    assert "full_pytest" not in commands


def test_analytics_ingest_paths_select_all_focused_ingest_tests() -> None:
    result = selector.run_selector_for_paths(
        ["src/mythic_edge_parser/app/analytics_ingest.py"],
        base="origin/main",
    )
    commands = _commands(result)

    assert commands["analytics_ingest_tests"] == (
        "python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py "
        "tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py "
        "tests/test_analytics_field_evidence_ingest.py"
    )
    assert "analytics_ingest_surface" in result.categories
    assert _recommendation(result, "pyright_advisory").priority == "advisory"


def test_local_artifact_policy_paths_select_checker_tests_and_profile_reports() -> None:
    result = selector.run_selector_for_paths(
        ["docs/local_artifacts_manifest.json"],
        base="origin/main",
    )
    commands = _commands(result)

    assert commands["local_environment_tests"] == "python3 -m pytest -q tests/test_check_local_environment.py"
    assert (
        commands["local_environment_clean_clone"]
        == "python3 tools/check_local_environment.py --profile clean_clone --format json"
    )
    assert (
        commands["local_environment_clean_install_transition"]
        == "python3 tools/check_local_environment.py --profile clean_install_transition_audit --format json"
    )
    assert _recommendation(result, "local_environment_clean_clone").priority == "recommended"
    assert "local_artifact_policy_surface" in result.categories


def test_validation_reference_docs_select_agent_docs_checker_when_tracked(monkeypatch) -> None:
    monkeypatch.setattr(selector, "is_tracked_file", lambda path, *, repo_root=".": True)

    result = selector.run_selector_for_paths(
        ["docs/validation_matrix.md", "docs/internal_project_map.md"],
        base="origin/main",
    )

    agent_docs = _recommendation(result, "agent_docs_checker")
    assert agent_docs.priority == "required"
    assert agent_docs.categories == ("governance_docs_surface",)
    assert agent_docs.paths == ("docs/internal_project_map.md", "docs/validation_matrix.md")
    assert "validation_reference_surface" in result.categories


def test_protected_and_forbidden_path_classifications_are_warnings() -> None:
    result = selector.run_selector_for_paths(
        ["src/mythic_edge_parser/app/state.py", "data/status/runtime.json"],
        base="origin/main",
    )
    warning_categories = {warning.category_id for warning in result.warnings}

    assert "parser_state_final_reconciliation" in warning_categories
    assert "runtime_status" in warning_categories
    assert result.selection_status == selector.STATUS_WARNING


def test_protected_warning_path_recommends_surface_authorization_checker() -> None:
    result = selector.run_selector_for_paths(
        ["src/mythic_edge_parser/app/state.py"],
        base="origin/main",
    )
    commands = _commands(result)

    command = commands["protected_surface_authorization"]
    assert command.startswith("python3 tools/check_surface_authorization.py --base origin/main")
    assert "--authorization-file issue=<issue-body-file>" in command
    assert "--authorization-file contract=<contract-file>" in command
    assert "--authorization-file pr=<pr-body-file>" in command
    recommendation = next(
        item
        for item in result.recommendations
        if item.command_id == "protected_surface_authorization"
    )
    assert recommendation.priority == "recommended"
    assert recommendation.categories == ("parser_state_final_reconciliation",)
    assert recommendation.paths == ("src/mythic_edge_parser/app/state.py",)


def test_forbidden_path_recommends_surface_authorization_checker() -> None:
    result = selector.run_selector_for_paths(["data/status/runtime.json"], base="origin/main")
    recommendation = next(
        item
        for item in result.recommendations
        if item.command_id == "protected_surface_authorization"
    )

    assert recommendation.priority == "recommended"
    assert recommendation.categories == ("runtime_status",)
    assert recommendation.paths == ("data/status/runtime.json",)


def test_allowed_docs_only_path_does_not_recommend_surface_authorization_checker() -> None:
    result = selector.run_selector_for_paths(["README.md"], base="origin/main")
    commands = _commands(result)

    assert "protected_surface_authorization" not in commands


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
