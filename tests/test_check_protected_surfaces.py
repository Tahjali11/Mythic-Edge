from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_protected_surfaces.py"
SPEC = importlib.util.spec_from_file_location("check_protected_surfaces", MODULE_PATH)
assert SPEC is not None
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
assert SPEC.loader is not None
SPEC.loader.exec_module(gate)


@pytest.mark.parametrize(
    ("raw_path", "expected"),
    [
        (r"data\status\runtime.json", "data/status/runtime.json"),
        ("./src/./mythic_edge_parser/app/state.py", "src/mythic_edge_parser/app/state.py"),
        ("//data//failed_posts//post.jsonl", "data/failed_posts/post.jsonl"),
        ("tests/fixtures/parser_regression_match_slice.log", "tests/fixtures/parser_regression_match_slice.log"),
    ],
)
def test_normalize_path_is_cross_platform_and_repo_relative(raw_path: str, expected: str) -> None:
    assert gate.normalize_path(raw_path) == expected


@pytest.mark.parametrize(
    ("path", "category_id"),
    [
        ("Player.log", "local_mtga_log"),
        ("data/match_logs/2026-05-14/raw.jsonl", "local_mtga_log"),
        ("data/runtime_logs/parser.runtime.log", "runtime_log"),
        ("data/status/runtime.json", "runtime_status"),
        ("data/failed_posts/post.jsonl", "failed_posts"),
        ("data/bad_events/event.json", "bad_events"),
        ("data/oracle_data/cards.json", "generated_card_data"),
        ("data/tier_sources/snapshot.json", "generated_card_data"),
        ("data/decklists/current.json", "generated_card_data"),
        ("exports/workbook/raw.xlsx", "raw_workbook_export"),
        ("client_secret_local.json", "secret_file"),
        ("api_token.txt", "webhook_api_credential"),
        ("webhook_url.local", "webhook_api_credential"),
        ("_review_tmp/report.md", "local_review_artifact"),
        (".github/Mythic-Edge/runtime.json", "local_review_artifact"),
        ("docs/fixtures/Player.log", "local_mtga_log"),
        ("sample.Player.log", "local_mtga_log"),
    ],
)
def test_forbidden_paths_fail_with_stable_categories(path: str, category_id: str) -> None:
    classification = gate.classify_path(path)

    assert classification.severity == gate.SEVERITY_FORBIDDEN
    assert classification.category_id == category_id


@pytest.mark.parametrize(
    "path",
    [
        "tests/fixtures/parser_regression_match_slice.log",
        "tests/fixtures/sample.xlsx",
        "src/mythic_edge_parser/app/token_counter.py",
        "docs/contracts/code_hardening_protected_surface_gate.md",
        "tools/check_protected_surfaces.py",
        "tests/test_check_protected_surfaces.py",
        "tests/fixtures/Player.log",
        "tests/fixtures/sample.Player.log",
        "tests/fixtures/sample.player.log",
        ".env.example",
    ],
)
def test_allowed_paths_do_not_warn_or_fail(path: str) -> None:
    classification = gate.classify_path(path)

    assert classification.severity == gate.SEVERITY_ALLOWED
    assert classification.category_id == "allowed"


def test_documented_player_log_fixture_paths_do_not_fail_gate() -> None:
    result = gate.evaluate_paths(
        [
            "tests/fixtures/Player.log",
            "tests/fixtures/sample.Player.log",
            "tests/fixtures/sample.player.log",
        ],
        base="origin/main",
    )

    assert result.exit_code == 0
    assert result.forbidden == ()
    assert result.warnings == ()


@pytest.mark.parametrize(
    ("path", "category_id"),
    [
        ("src/mythic_edge_parser/events.py", "parser_event_classes"),
        ("src/mythic_edge_parser/app/state.py", "parser_state_final_reconciliation"),
        ("src/mythic_edge_parser/app/models.py", "parser_state_final_reconciliation"),
        ("src/mythic_edge_parser/app/extractors.py", "extractor_behavior"),
        ("src/mythic_edge_parser/parsers/gre/game_state.py", "match_game_identity"),
        ("src/mythic_edge_parser/app/sheet_schema.py", "workbook_schema"),
        ("src/mythic_edge_parser/app/outputs.py", "webhook_payload_shape"),
        ("tools/google_apps_script/Code.gs", "apps_script_behavior"),
        ("src/mythic_edge_parser/app/config.py", "environment_runtime_paths"),
        (".github/workflows/repo-checks.yml", "environment_runtime_paths"),
        ("docs/agent_constitution.md", "workflow_authority_docs"),
        ("docs/agent_threads/implementation.md", "workflow_authority_docs"),
        ("docs/templates/module_contract.md", "workflow_authority_docs"),
        (".github/ISSUE_TEMPLATE/module_workflow.yml", "workflow_authority_docs"),
    ],
)
def test_protected_surfaces_warn_without_failing(path: str, category_id: str) -> None:
    classification = gate.classify_path(path)

    assert classification.severity == gate.SEVERITY_WARNING
    assert classification.category_id == category_id


def test_forbidden_precedence_beats_protected_warning() -> None:
    classification = gate.classify_path(".github/ISSUE_TEMPLATE/.env")

    assert classification.severity == gate.SEVERITY_FORBIDDEN
    assert classification.category_id == "secret_file"


def test_exit_behavior_matches_contract() -> None:
    allowed_result = gate.evaluate_paths(["docs/readme.md"], base="origin/main")
    warning_result = gate.evaluate_paths(
        ["src/mythic_edge_parser/app/state.py"],
        base="origin/main",
    )
    forbidden_result = gate.evaluate_paths(["data/status/runtime.json"], base="origin/main")
    error_result = gate.evaluate_paths((), base="origin/main", error="bad base")

    assert allowed_result.exit_code == 0
    assert warning_result.exit_code == 0
    assert forbidden_result.exit_code == 1
    assert error_result.exit_code == 2


def test_report_includes_required_summary_and_findings() -> None:
    result = gate.evaluate_paths(
        [
            "data/status/runtime.json",
            "src/mythic_edge_parser/app/state.py",
            "docs/readme.md",
        ],
        base="origin/codex/code-hardening-suite",
    )

    report = gate.render_report(result)

    assert "Protected Surface Gate" in report
    assert "base: origin/codex/code-hardening-suite" in report
    assert "head: HEAD" in report
    assert "changed_paths: 3" in report
    assert "forbidden: 1" in report
    assert "warnings: 1" in report
    assert "FORBIDDEN runtime_status data/status/runtime.json" in report
    assert "WARNING parser_state_final_reconciliation src/mythic_edge_parser/app/state.py" in report
    assert report.endswith("result: failed")


def test_collect_changed_paths_uses_base_to_head_diff_and_excludes_deletions(monkeypatch) -> None:
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, stdout="tools/check_protected_surfaces.py\n", stderr="")

    monkeypatch.setattr(gate.subprocess, "run", fake_run)

    assert gate.collect_changed_paths("origin/main", repo_root="/repo") == (
        "tools/check_protected_surfaces.py",
    )

    command, kwargs = calls[0]
    assert command == [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        "origin/main...HEAD",
    ]
    assert kwargs["cwd"] == "/repo"


def test_git_failure_returns_configuration_error(monkeypatch) -> None:
    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 128, stdout="", stderr="bad revision")

    monkeypatch.setattr(gate.subprocess, "run", fake_run)

    result = gate.run_gate("missing/ref", repo_root="/repo")

    assert result.exit_code == 2
    assert result.error == "bad revision"
    assert "result: error" in gate.render_report(result)


def test_os_error_returns_configuration_error(monkeypatch) -> None:
    def fake_run(command, **kwargs):
        raise OSError("git unavailable")

    monkeypatch.setattr(gate.subprocess, "run", fake_run)

    result = gate.run_gate("origin/main", repo_root="/repo")

    assert result.exit_code == 2
    assert result.error == "git unavailable"


def test_missing_base_is_usage_error(capsys) -> None:
    assert gate.main([]) == 2

    captured = capsys.readouterr()
    assert "--base" in captured.err


def test_paths_from_stdin_uses_test_seam(monkeypatch, capsys) -> None:
    monkeypatch.setattr(gate.sys, "stdin", io.StringIO("src/mythic_edge_parser/events.py\n"))

    assert gate.main(["--base", "origin/main", "--paths-from-stdin"]) == 0

    captured = capsys.readouterr()
    assert "warnings: 1" in captured.out
    assert "WARNING parser_event_classes src/mythic_edge_parser/events.py" in captured.out


def test_ci_workflow_runs_gate_for_pull_requests_against_base_ref() -> None:
    workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/repo-checks.yml").read_text()

    assert "fetch-depth: 0" in workflow
    assert "Run protected surface gate" in workflow
    assert "github.event_name == 'pull_request'" in workflow
    assert "py tools/check_protected_surfaces.py --base origin/${{ github.base_ref }}" in workflow
