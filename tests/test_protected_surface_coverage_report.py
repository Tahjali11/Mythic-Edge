from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "generate_protected_surface_coverage_report.py"
SPEC = importlib.util.spec_from_file_location("generate_protected_surface_coverage_report", MODULE_PATH)
assert SPEC is not None
reporter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reporter
assert SPEC.loader is not None
SPEC.loader.exec_module(reporter)


def _write(repo_root: Path, path: str) -> None:
    target = repo_root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# placeholder\n", encoding="utf-8")


def _write_xml(repo_root: Path, text: str) -> Path:
    path = repo_root / "coverage.xml"
    path.write_text(text, encoding="utf-8")
    return path


def _minimal_repo(repo_root: Path) -> None:
    for path in (
        "src/mythic_edge_parser/events.py",
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/extractors.py",
        "src/mythic_edge_parser/app/gameplay_actions.py",
        "src/mythic_edge_parser/app/transforms.py",
        "src/mythic_edge_parser/app/sheet_schema.py",
        "src/mythic_edge_parser/app/sheet_exports.py",
        "src/mythic_edge_parser/app/outputs.py",
        "src/mythic_edge_parser/app/runner.py",
        "src/mythic_edge_parser/app/config.py",
        "src/mythic_edge_parser/app/analytics_ingest.py",
        "src/mythic_edge_parser/local_app/backend.py",
        "src/mythic_edge_parser/parsers/gre/game_state.py",
        "tools/google_apps_script/Code.gs",
        "tools/check_protected_surfaces.py",
        ".github/workflows/repo-checks.yml",
        "AGENTS.md",
        "docs/agent_constitution.md",
    ):
        _write(repo_root, path)


def _coverage_xml() -> str:
    classes = "\n".join(
        (
            '<class name="events.py" filename="events.py" line-rate="1.0000" branch-rate="1.0000" />',
            '<class name="state.py" filename="app/state.py" '
            'line-rate="0.9000" branch-rate="0.5000" />',
            '<class name="models.py" filename="src/mythic_edge_parser/app/models.py" '
            'line-rate="0.8000" branch-rate="0.4000" />',
            '<class name="extractors.py" filename="mythic_edge_parser/app/extractors.py" '
            'line-rate="1.0000" branch-rate="1.0000" />',
            '<class name="game_state.py" filename="mythic_edge_parser/parsers/gre/game_state.py" '
            'line-rate="0.7500" branch-rate="0.2500" />',
            '<class name="backend.py" filename="mythic_edge_parser/local_app/backend.py" '
            'line-rate="0.6000" branch-rate="0.2000" />',
        ),
    )
    return f"""<?xml version="1.0" ?>
<coverage line-rate="0.8755" branch-rate="0.7480">
  <packages>
    <package name="mythic_edge_parser" line-rate="0.8755" branch-rate="0.7480">
      <classes>
        {classes}
      </classes>
    </package>
  </packages>
</coverage>
"""


def _report(repo_root: Path, coverage_xml: Path) -> dict:
    return reporter.build_report(
        coverage_xml=coverage_xml,
        repo_root=repo_root,
        metadata=reporter.RepoMetadata(
            measured_ref="unit-test-ref",
            measured_commit="024eda7d9408c0bb72d645af4d41d604539291ba",
        ),
    )


def _group(report: dict, group_id: str) -> dict:
    return next(item for item in report["groups"] if item["group_id"] == group_id)


def _file(group: dict, path: str) -> dict:
    return next(item for item in group["files"] if item["path"] == path)


def test_report_is_advisory_and_preserves_global_floor_boundary(tmp_path: Path) -> None:
    _minimal_repo(tmp_path)
    report = _report(tmp_path, _write_xml(tmp_path, _coverage_xml()))

    assert report["object"] == "mythic_edge_quality_protected_surface_coverage_advisory"
    assert report["schema_version"] == "protected_surface_coverage_advisory.v1"
    assert report["overall_status"] == "passed_advisory"
    assert report["global_line_coverage_percent"] == 87.55
    assert report["global_branch_coverage_percent"] == 74.8
    assert report["global_line_floor_status"] == "passed"
    assert report["branch_coverage_status"] == "advisory_only"
    assert report["protected_surface_floor_status"] == "not_authorized"
    assert report["protected_surface_floor_authorized"] is False
    assert report["ci_change_authorized"] is False
    assert report["advisory_only"] is True
    assert "not CI enforcement" in report["non_claims"]


def test_measured_groups_use_repo_relative_paths_and_file_rates(tmp_path: Path) -> None:
    _minimal_repo(tmp_path)
    report = _report(tmp_path, _write_xml(tmp_path, _coverage_xml()))

    state_group = _group(report, "parser_state_final_reconciliation")
    assert state_group["coverage_scope_status"] == "measured"
    state_file = _file(state_group, "src/mythic_edge_parser/app/state.py")
    assert state_file["coverage_status"] == "measured"
    assert state_file["line_coverage_percent"] == 90.0
    assert state_file["branch_coverage_percent"] == 50.0
    assert state_file["branch_coverage_status"] == "advisory_only"


def test_missing_measurable_file_is_symbolic_without_fake_percentage(tmp_path: Path) -> None:
    _minimal_repo(tmp_path)
    report = _report(tmp_path, _write_xml(tmp_path, _coverage_xml()))

    workbook_group = _group(report, "workbook_schema_and_exports")
    sheet_schema = _file(workbook_group, "src/mythic_edge_parser/app/sheet_schema.py")
    assert sheet_schema["coverage_status"] == "missing_from_coverage_xml"
    assert sheet_schema["line_coverage_percent"] is None
    assert sheet_schema["branch_coverage_percent"] is None


def test_non_python_groups_are_not_applicable_without_fake_percentages(tmp_path: Path) -> None:
    _minimal_repo(tmp_path)
    report = _report(tmp_path, _write_xml(tmp_path, _coverage_xml()))

    apps_script = _group(report, "apps_script_behavior")
    assert apps_script["coverage_scope_status"] == "not_applicable_current_coverage_scope"
    code_gs = _file(apps_script, "tools/google_apps_script/Code.gs")
    assert code_gs["coverage_status"] == "not_applicable_current_coverage_scope"
    assert code_gs["line_coverage_percent"] is None
    assert "outside the current Python coverage source" in code_gs["notes"][0]


def test_missing_coverage_xml_fails_closed_without_path_echo(tmp_path: Path) -> None:
    _minimal_repo(tmp_path)
    missing = tmp_path / "private" / "coverage.xml"

    report = _report(tmp_path, missing)

    rendered = json.dumps(report)
    assert report["overall_status"] == "failed_advisory"
    assert report["coverage_xml_status"] == "coverage_xml_missing"
    assert report["global_line_floor_status"] == "not_run"
    assert str(missing) not in rendered


def test_malformed_coverage_xml_fails_closed_without_parser_detail(tmp_path: Path) -> None:
    _minimal_repo(tmp_path)
    coverage_xml = _write_xml(tmp_path, "<coverage")

    report = _report(tmp_path, coverage_xml)

    assert report["overall_status"] == "failed_advisory"
    assert report["coverage_xml_status"] == "coverage_xml_malformed_or_unreadable"


def test_default_report_path_uses_date_and_short_commit() -> None:
    path = reporter.default_report_path("2026-07-01", "024eda7d9408c0bb72d645af4d41d604539291ba")

    assert path.as_posix() == (
        "docs/quality_reports/coverage/protected_surface/"
        "2026-07-01-024eda7-protected-surface-coverage-advisory.json"
    )


def test_output_path_must_stay_in_approved_report_directory(tmp_path: Path) -> None:
    rejected = tmp_path / "data" / "status" / "report.json"

    try:
        reporter.validate_output_path(tmp_path, rejected)
    except reporter.ConfigError as exc:
        assert "docs/quality_reports/coverage/protected_surface" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("Expected output path validation to fail")
