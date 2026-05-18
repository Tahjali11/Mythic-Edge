from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "run_hardening_orchestrator.py"
SPEC = importlib.util.spec_from_file_location("run_hardening_orchestrator", MODULE_PATH)
assert SPEC is not None
orchestrator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = orchestrator
assert SPEC.loader is not None
SPEC.loader.exec_module(orchestrator)


def _completed(command, returncode: int = 0, stdout: str = "result: passed\n", stderr: str = ""):
    return subprocess.CompletedProcess(list(command), returncode, stdout=stdout, stderr=stderr)


def _command_contains(command, needle: str) -> bool:
    return any(needle in part for part in command)


def test_missing_base_exits_two(capsys) -> None:
    assert orchestrator.main([]) == 2

    captured = capsys.readouterr()
    assert "--base" in captured.err


def test_default_profile_is_plan_only_and_executes_no_subprocesses(tmp_path: Path) -> None:
    calls = []

    def runner(command, cwd, stdin_text):
        calls.append(command)
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_PLAN,
        base="origin/main",
        repo_root=tmp_path,
        runner=runner,
    )

    assert calls == []
    assert result.run_mode == "plan"
    assert result.orchestrator_status == "plan_only"
    assert {item.status for item in result.commands} == {"planned"}


def test_plan_profile_renders_stable_quick_command_rows(tmp_path: Path) -> None:
    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_PLAN,
        base="origin/main",
        repo_root=tmp_path,
    )
    command_ids = [item.command_id for item in result.commands]

    assert command_ids == [
        "protected_surface_gate",
        "secret_private_marker_scan",
        "validation_selector",
        "agent_docs_checker",
        "diff_check",
    ]
    report = orchestrator.render_text(result)
    assert "Hardening Orchestrator" in report
    assert "orchestrator_status: plan_only" in report
    assert "merge_readiness: not_decided_by_orchestrator" in report
    assert "deploy_readiness: not_decided_by_orchestrator" in report
    assert "tracker_completion: not_decided_by_orchestrator" in report


def test_quick_without_run_executes_no_commands_and_skips_missing_authorization(tmp_path: Path) -> None:
    calls = []

    def runner(command, cwd, stdin_text):
        calls.append(command)
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_QUICK,
        base="origin/main",
        repo_root=tmp_path,
        runner=runner,
    )
    by_id = {item.command_id: item for item in result.commands}

    assert calls == []
    assert by_id["surface_authorization"].status == "skipped"
    assert by_id["surface_authorization"].skip_reason == "authorization_files_not_supplied"
    assert by_id["surface_authorization"].status != "passed"
    assert result.orchestrator_status == "plan_only"


def test_quick_run_executes_fake_commands_in_stable_order(tmp_path: Path) -> None:
    calls = []

    def runner(command, cwd, stdin_text):
        calls.append(list(command))
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_QUICK,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        authorization_files=["contract=docs/contracts/example.md"],
        runner=runner,
    )

    assert [item.command_id for item in result.commands] == [
        "protected_surface_gate",
        "secret_private_marker_scan",
        "validation_selector",
        "surface_authorization",
        "agent_docs_checker",
        "diff_check",
    ]
    assert calls == [
        ["python3", "tools/check_protected_surfaces.py", "--base", "origin/main"],
        ["python3", "tools/check_secret_patterns.py", "--base", "origin/main"],
        ["python3", "tools/select_validation.py", "--base", "origin/main"],
        [
            "python3",
            "tools/check_surface_authorization.py",
            "--base",
            "origin/main",
            "--authorization-file",
            "contract=docs/contracts/example.md",
        ],
        ["python3", "tools/check_agent_docs.py"],
        ["git", "diff", "--check"],
    ]


def test_paths_from_stdin_are_forwarded_once_to_compatible_tools(tmp_path: Path) -> None:
    calls = []

    def runner(command, cwd, stdin_text):
        calls.append((list(command), stdin_text))
        return _completed(command)

    orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_QUICK,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        paths_from_stdin=True,
        stdin_text="./b.md\na.md\nb.md\n",
        authorization_files=["contract=docs/contracts/example.md"],
        runner=runner,
    )

    stdin_by_command = {tuple(command): stdin_text for command, stdin_text in calls}
    protected_command = ("python3", "tools/check_protected_surfaces.py", "--base", "origin/main", "--paths-from-stdin")
    secret_command = ("python3", "tools/check_secret_patterns.py", "--base", "origin/main", "--paths-from-stdin")
    selector_command = ("python3", "tools/select_validation.py", "--base", "origin/main", "--paths-from-stdin")
    assert stdin_by_command[protected_command] == "a.md\nb.md\n"
    assert stdin_by_command[secret_command] == "a.md\nb.md\n"
    assert stdin_by_command[selector_command] == "a.md\nb.md\n"
    assert stdin_by_command[
        (
            "python3",
            "tools/check_surface_authorization.py",
            "--base",
            "origin/main",
            "--paths-from-stdin",
            "--authorization-file",
            "contract=docs/contracts/example.md",
        )
    ] == "a.md\nb.md\n"
    assert stdin_by_command[("python3", "tools/check_agent_docs.py")] == ""
    assert stdin_by_command[("git", "diff", "--check")] == ""


def test_outside_repo_stdin_path_is_configuration_error(tmp_path: Path) -> None:
    outside = tmp_path.parent / "private.txt"

    try:
        orchestrator.run_orchestrator(
            profile=orchestrator.PROFILE_QUICK,
            base="origin/main",
            repo_root=tmp_path,
            run=True,
            paths_from_stdin=True,
            stdin_text=str(outside),
        )
    except orchestrator.ConfigError as exc:
        assert "<redacted-outside-repo-path>" in str(exc)
    else:
        raise AssertionError("expected ConfigError")


def test_scanner_warning_output_is_classified_as_warning(tmp_path: Path) -> None:
    def runner(command, cwd, stdin_text):
        if _command_contains(command, "check_secret_patterns.py"):
            return _completed(command, stdout="warnings: 1\nresult: warning\n")
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_QUICK,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        runner=runner,
    )
    by_id = {item.command_id: item for item in result.commands}

    assert by_id["secret_private_marker_scan"].status == "warning"
    assert result.orchestrator_status == "warning"
    assert result.exit_code == 0


def test_protected_surface_forbidden_output_is_classified_as_failed(tmp_path: Path) -> None:
    def runner(command, cwd, stdin_text):
        if _command_contains(command, "check_protected_surfaces.py"):
            return _completed(command, returncode=1, stdout="forbidden: 1\nresult: failed\n")
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_QUICK,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        runner=runner,
    )
    by_id = {item.command_id: item for item in result.commands}

    assert by_id["protected_surface_gate"].status == "failed"
    assert result.orchestrator_status == "failed"
    assert result.exit_code == 1


def test_surface_authorization_review_output_is_warning(tmp_path: Path) -> None:
    def runner(command, cwd, stdin_text):
        if _command_contains(command, "check_surface_authorization.py"):
            return _completed(command, stdout="authorization_status: review\n")
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_QUICK,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        authorization_files=["contract=docs/contracts/example.md"],
        runner=runner,
    )
    by_id = {item.command_id: item for item in result.commands}

    assert by_id["surface_authorization"].status == "warning"
    assert result.orchestrator_status == "warning"


def test_pyright_advisory_findings_remain_advisory(tmp_path: Path) -> None:
    def runner(command, cwd, stdin_text):
        if _command_contains(command, "run_pyright_advisory_report.py"):
            return _completed(command, stdout="status: advisory_findings\n")
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_FULL,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        runner=runner,
    )
    by_id = {item.command_id: item for item in result.commands}

    assert by_id["pyright_advisory"].status == "advisory"
    assert result.orchestrator_status == "advisory"
    assert result.exit_code == 0


def test_subprocess_execution_error_makes_orchestrator_error(tmp_path: Path) -> None:
    def runner(command, cwd, stdin_text):
        if _command_contains(command, "check_agent_docs.py"):
            return _completed(command, returncode=2, stderr="tool unavailable")
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_QUICK,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        runner=runner,
    )
    by_id = {item.command_id: item for item in result.commands}

    assert by_id["agent_docs_checker"].status == "error"
    assert result.orchestrator_status == "error"
    assert result.exit_code == 2


def test_stdout_and_stderr_summaries_are_sanitized_and_bounded() -> None:
    secret_text = f"{Path.home()}/private api_key={'A' * 32} " + ("x" * 500)

    summary = orchestrator.summarize_output(secret_text, "")

    assert str(Path.home()) not in summary
    assert "A" * 32 not in summary
    assert "<redacted-local-path>" in summary
    assert "<redacted-secret>" in summary
    assert len(summary) <= orchestrator.MAX_SUMMARY_CHARS


def test_json_output_preserves_command_statuses_and_exit_codes(tmp_path: Path) -> None:
    def runner(command, cwd, stdin_text):
        if _command_contains(command, "check_protected_surfaces.py"):
            return _completed(command, returncode=1, stdout="result: failed\n")
        return _completed(command)

    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_QUICK,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        runner=runner,
    )
    payload = json.loads(orchestrator.render_json(result))
    by_id = {item["command_id"]: item for item in payload["commands"]}

    assert payload["object"] == "mythic_edge_hardening_orchestrator"
    assert payload["orchestrator_status"] == "failed"
    assert by_id["protected_surface_gate"]["status"] == "failed"
    assert by_id["protected_surface_gate"]["exit_code"] == 1
    assert payload["merge_readiness"] == "not_decided_by_orchestrator"


def test_output_paths_outside_contract_reports_are_rejected(tmp_path: Path) -> None:
    try:
        orchestrator.run_orchestrator(
            profile=orchestrator.PROFILE_POST_HARDENING,
            base="origin/main",
            repo_root=tmp_path,
            run=True,
            hardening_report_output="data/status/report.md",
        )
    except orchestrator.ConfigError as exc:
        assert "docs/contract_test_reports" in str(exc)
    else:
        raise AssertionError("expected ConfigError")


def test_post_hardening_profile_forwards_report_generator_inputs(tmp_path: Path) -> None:
    result = orchestrator.run_orchestrator(
        profile=orchestrator.PROFILE_POST_HARDENING,
        base="origin/main",
        repo_root=tmp_path,
        run=True,
        evidence_manifest="docs/contract_test_reports/evidence.json",
        hardening_report_output="docs/contract_test_reports/status.md",
        runner=lambda command, cwd, stdin_text: _completed(command),
    )
    by_id = {item.command_id: item for item in result.commands}

    assert by_id["hardening_report_generator"].command == (
        "python3 tools/generate_hardening_report.py "
        "--evidence-manifest docs/contract_test_reports/evidence.json "
        "--output docs/contract_test_reports/status.md"
    )


def test_summary_output_writes_only_approved_markdown_path(tmp_path: Path) -> None:
    target = "docs/contract_test_reports/orchestrator.md"

    orchestrator.write_summary_output(target, "summary\n", repo_root=tmp_path)

    assert (tmp_path / target).read_text(encoding="utf-8") == "summary\n"


def test_cli_summary_output_writes_text_even_when_stdout_is_json(capsys, tmp_path: Path) -> None:
    target = "docs/contract_test_reports/orchestrator.md"

    assert (
        orchestrator.main(
            [
                "--base",
                "origin/main",
                "--repo-root",
                str(tmp_path),
                "--format",
                "json",
                "--summary-output",
                target,
            ],
        )
        == 0
    )

    captured = capsys.readouterr()
    assert json.loads(captured.out)["object"] == "mythic_edge_hardening_orchestrator"
    assert (tmp_path / target).read_text(encoding="utf-8").startswith("Hardening Orchestrator")


def test_no_openai_model_provider_or_github_commands_are_planned() -> None:
    for profile in orchestrator.PROFILES:
        commands = orchestrator.build_command_plan(profile=profile, base="origin/main")
        command_text = "\n".join(spec.command_string.lower() for spec in commands)
        assert "openai" not in command_text
        assert "model" not in command_text
        assert "gh " not in command_text
        assert "github" not in command_text
