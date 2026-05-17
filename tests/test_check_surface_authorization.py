from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_surface_authorization.py"
SPEC = importlib.util.spec_from_file_location("check_surface_authorization", MODULE_PATH)
assert SPEC is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
assert SPEC.loader is not None
SPEC.loader.exec_module(checker)


def _write_source(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def _run_for_paths(
    tmp_path: Path,
    paths: list[str],
    *,
    source_args: list[str] | None = None,
):
    return checker.run_authorization_check(
        "origin/main",
        repo_root=tmp_path,
        paths=paths,
        authorization_file_args=source_args or [],
        mode=checker.MODE_STDIN,
    )


def test_missing_base_exits_two(capsys) -> None:
    assert checker.main([]) == 2

    captured = capsys.readouterr()
    assert "--base" in captured.err


def test_invalid_base_diff_reports_error(monkeypatch, tmp_path: Path, capsys) -> None:
    gate = checker._load_protected_surface_gate()

    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 128, stdout="", stderr="bad revision")

    monkeypatch.setattr(gate.subprocess, "run", fake_run)

    assert checker.main(["--base", "missing/ref", "--repo-root", str(tmp_path)]) == 2

    captured = capsys.readouterr()
    assert "authorization_status: error" in captured.err
    assert "bad revision" in captured.err


def test_paths_from_stdin_does_not_run_git_diff(monkeypatch, tmp_path: Path, capsys) -> None:
    gate = checker._load_protected_surface_gate()
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(gate.subprocess, "run", fake_run)
    monkeypatch.setattr(checker.sys, "stdin", io.StringIO("docs/readme.md\n"))

    assert checker.main(["--base", "origin/main", "--repo-root", str(tmp_path), "--paths-from-stdin"]) == 0

    captured = capsys.readouterr()
    assert "mode: paths-from-stdin" in captured.out
    assert calls == []


def test_changed_path_mode_uses_contract_git_diff_command(monkeypatch, tmp_path: Path) -> None:
    gate = checker._load_protected_surface_gate()
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, stdout="docs/readme.md\n", stderr="")

    monkeypatch.setattr(gate.subprocess, "run", fake_run)

    result = checker.run_authorization_check("origin/main", repo_root=tmp_path)

    assert result.changed_paths == ("docs/readme.md",)
    command, kwargs = calls[0]
    assert command == [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        "origin/main...HEAD",
    ]
    assert kwargs["cwd"] == tmp_path.resolve()


def test_checker_consumes_protected_surface_gate_classification_helpers(monkeypatch, tmp_path: Path) -> None:
    gate = checker._load_protected_surface_gate()
    calls = []

    def fake_classify_paths(paths):
        calls.append(tuple(paths))
        return (
            gate.Classification(
                "docs/readme.md",
                gate.SEVERITY_ALLOWED,
                "allowed",
                "No protected-surface classification.",
            ),
        )

    monkeypatch.setattr(gate, "classify_paths", fake_classify_paths)

    result = _run_for_paths(tmp_path, ["docs/readme.md"])

    assert calls == [("docs/readme.md",)]
    assert result.not_protected[0].category_id == "allowed"


def test_allowed_path_reports_not_protected(tmp_path: Path) -> None:
    result = _run_for_paths(tmp_path, ["docs/readme.md"])
    report = checker.render_report(result)

    assert result.authorization_status == checker.AUTHORIZATION_STATUS_OK
    assert "NOT_PROTECTED allowed docs/readme.md" in report


def test_forbidden_path_reports_forbidden_and_is_never_authorized(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "contract.md",
        "authorized_protected_surfaces: " + "runtime" + "_status",
    )

    result = _run_for_paths(
        tmp_path,
        ["data/status/runtime.json"],
        source_args=[f"contract={source}"],
    )
    report = checker.render_report(result)

    assert result.authorization_status == checker.AUTHORIZATION_STATUS_REVIEW
    assert "FORBIDDEN_PATH runtime_status data/status/runtime.json" in report
    assert "AUTHORIZED runtime_status" not in report


def test_exact_category_id_in_contract_source_authorizes_protected_path(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "contract.md",
        "authorized_protected_surfaces: workbook_schema",
    )

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"contract={source}"],
    )
    report = checker.render_report(result)

    assert result.authorization_status == checker.AUTHORIZATION_STATUS_OK
    assert "AUTHORIZED workbook_schema src/mythic_edge_parser/app/sheet_schema.py" in report
    assert "evidence: contract=contract.md - authorized_protected_surfaces: workbook_schema" in report


def test_accepted_alias_in_issue_source_authorizes_protected_path(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "issue.md",
        "Scope includes sheet schema changes to src/mythic_edge_parser/app/sheet_schema.py.",
    )

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"issue={source}"],
    )

    assert result.authorization_status == checker.AUTHORIZATION_STATUS_OK
    assert result.authorized[0].category_id == "workbook_schema"


def test_no_source_reports_unverifiable_and_missing_authorization(tmp_path: Path) -> None:
    result = _run_for_paths(tmp_path, ["src/mythic_edge_parser/app/sheet_schema.py"])
    report = checker.render_report(result)

    assert result.authorization_status == checker.AUTHORIZATION_STATUS_REVIEW
    assert "MISSING_AUTHORIZATION workbook_schema" in report
    assert "UNVERIFIABLE_SOURCE workbook_schema" in report


def test_unrelated_category_evidence_reports_scope_warning_and_missing(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "contract.md",
        "authorized_protected_surfaces: webhook_payload_shape",
    )

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"contract={source}"],
    )
    report = checker.render_report(result)

    assert "MISSING_AUTHORIZATION workbook_schema" in report
    assert "SCOPE_WARNING workbook_schema contract=contract.md" in report


def test_broad_all_protected_surfaces_text_is_scope_warning_not_authorization(tmp_path: Path) -> None:
    source = _write_source(tmp_path, "contract.md", "all protected surfaces authorized")

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"contract={source}"],
    )
    report = checker.render_report(result)

    assert "MISSING_AUTHORIZATION workbook_schema" in report
    assert "SCOPE_WARNING workbook_schema contract=contract.md" in report
    assert "AUTHORIZED workbook_schema" not in report


def test_unchanged_or_authorized_boilerplate_is_scope_warning_not_authorization(tmp_path: Path) -> None:
    source = _write_source(tmp_path, "contract.md", "workbook schema unchanged or authorized")

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"contract={source}"],
    )
    report = checker.render_report(result)

    assert "MISSING_AUTHORIZATION workbook_schema" in report
    assert "SCOPE_WARNING workbook_schema contract=contract.md" in report
    assert "AUTHORIZED workbook_schema" not in report


def test_negated_scope_text_is_scope_warning_not_authorization(tmp_path: Path) -> None:
    source = _write_source(tmp_path, "contract.md", "workbook_schema not in scope")

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"contract={source}"],
    )
    report = checker.render_report(result)

    assert "MISSING_AUTHORIZATION workbook_schema" in report
    assert "SCOPE_WARNING workbook_schema contract=contract.md" in report
    assert "AUTHORIZED workbook_schema" not in report


def test_pr_source_without_citation_does_not_authorize_category(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "pr.md",
        "Protected-surface authorization: Authorized drift - workbook_schema.",
    )

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"pr={source}"],
    )
    report = checker.render_report(result)

    assert "MISSING_AUTHORIZATION workbook_schema" in report
    assert "SCOPE_WARNING workbook_schema pr=pr.md" in report


def test_pr_source_with_category_and_citation_authorizes_category(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "pr.md",
        "Protected-surface authorization: Authorized drift - workbook_schema - #90.",
    )

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"pr={source}"],
    )

    assert result.authorization_status == checker.AUTHORIZATION_STATUS_OK
    assert result.authorized[0].evidence.source_kind == "pr"


def test_report_output_line_does_not_self_authorize_category(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "report.md",
        "AUTHORIZED workbook_schema src/mythic_edge_parser/app/sheet_schema.py",
    )

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"report={source}"],
    )

    assert result.authorization_status == checker.AUTHORIZATION_STATUS_REVIEW
    assert result.authorized == ()
    assert result.missing_authorization[0].category_id == "workbook_schema"


def test_issue_source_authorizes_without_extra_citation(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "issue.md",
        "Protected-surface authorization: Authorized drift - workbook_schema.",
    )

    result = _run_for_paths(
        tmp_path,
        ["src/mythic_edge_parser/app/sheet_schema.py"],
        source_args=[f"issue={source}"],
    )

    assert result.authorization_status == checker.AUTHORIZATION_STATUS_OK


def test_unreadable_source_exits_two(monkeypatch, tmp_path: Path, capsys) -> None:
    missing_source = tmp_path / "missing.md"
    monkeypatch.setattr(checker.sys, "stdin", io.StringIO(""))

    assert (
        checker.main(
            [
                "--base",
                "origin/main",
                "--repo-root",
                str(tmp_path),
                "--paths-from-stdin",
                "--authorization-file",
                f"contract={missing_source}",
            ],
        )
        == 2
    )

    captured = capsys.readouterr()
    assert "authorization_status: error" in captured.err
    assert "unable to read authorization source contract=missing.md" in captured.err


def test_invalid_authorization_file_syntax_exits_two(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(checker.sys, "stdin", io.StringIO(""))

    assert (
        checker.main(
            [
                "--base",
                "origin/main",
                "--repo-root",
                str(tmp_path),
                "--paths-from-stdin",
                "--authorization-file",
                "contract",
            ],
        )
        == 2
    )

    captured = capsys.readouterr()
    assert "authorization_status: error" in captured.err
    assert "invalid --authorization-file syntax" in captured.err


def test_duplicate_sources_and_paths_render_deterministically(tmp_path: Path) -> None:
    source = _write_source(
        tmp_path,
        "contract.md",
        "authorized_protected_surfaces: workbook_schema",
    )

    result = _run_for_paths(
        tmp_path,
        [
            "src/mythic_edge_parser/app/sheet_schema.py",
            "./src/mythic_edge_parser/app/sheet_schema.py",
        ],
        source_args=[f"contract={source}", f"contract={source}"],
    )

    assert result.changed_paths == ("src/mythic_edge_parser/app/sheet_schema.py",)
    assert len(result.authorization_sources) == 1
    assert len(result.authorized) == 1


def test_output_uses_authorization_status_vocabulary_without_validation_claims(tmp_path: Path) -> None:
    result = _run_for_paths(tmp_path, ["src/mythic_edge_parser/app/sheet_schema.py"])
    report = checker.render_report(result)

    assert "authorization_status: review" in report
    lowered = report.lower()
    assert "authorized to merge" not in lowered
    assert "safe" not in lowered
    assert "parser behavior passed" not in lowered
    assert "schema behavior passed" not in lowered
    assert "checks passed" not in lowered


def test_json_output_contains_contracted_fields(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(checker.sys, "stdin", io.StringIO("docs/readme.md\n"))

    assert (
        checker.main(
            [
                "--base",
                "origin/main",
                "--repo-root",
                str(tmp_path),
                "--paths-from-stdin",
                "--format",
                "json",
            ],
        )
        == 0
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert set(payload) == {
        "authorization_sources",
        "authorization_status",
        "authorized",
        "base",
        "changed_paths",
        "classifications",
        "forbidden_paths",
        "head",
        "missing_authorization",
        "mode",
        "not_protected",
        "scope_warnings",
        "unverifiable_sources",
    }
