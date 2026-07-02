from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_coverage_floor.py"
SPEC = importlib.util.spec_from_file_location("check_coverage_floor", MODULE_PATH)
assert SPEC is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
assert SPEC.loader is not None
SPEC.loader.exec_module(checker)


def _write_xml(path: Path, *, line_rate: str = "0.8755", branch_rate: str = "0.7480") -> Path:
    path.write_text(
        f'<?xml version="1.0" ?><coverage line-rate="{line_rate}" branch-rate="{branch_rate}"></coverage>\n',
        encoding="utf-8",
    )
    return path


def _write_protected_surface_xml(
    path: Path,
    *,
    global_line_rate: str = "0.8764",
    branch_rate: str = "0.7486",
    models_line_rate: str | None = "0.9045",
    state_line_rate: str | None = "0.9296",
    models_filename: str = "src/mythic_edge_parser/app/models.py",
    state_filename: str = "src/mythic_edge_parser/app/state.py",
) -> Path:
    classes: list[str] = []
    if models_line_rate is not None:
        classes.append(
            f'<class name="models.py" filename="{models_filename}" line-rate="{models_line_rate}" '
            'branch-rate="0.7642" />'
        )
    if state_line_rate is not None:
        classes.append(
            f'<class name="state.py" filename="{state_filename}" line-rate="{state_line_rate}" '
            'branch-rate="0.7957" />'
        )
    class_xml = "\n        ".join(classes)
    path.write_text(
        f"""<?xml version="1.0" ?>
<coverage line-rate="{global_line_rate}" branch-rate="{branch_rate}">
  <packages>
    <package name="mythic_edge_parser" line-rate="{global_line_rate}" branch-rate="{branch_rate}">
      <classes>
        {class_xml}
      </classes>
    </package>
  </packages>
</coverage>
""",
        encoding="utf-8",
    )
    return path


def test_line_floor_passes_and_branch_is_advisory(tmp_path: Path) -> None:
    xml_path = _write_xml(tmp_path / "coverage.xml")

    result = checker.evaluate_coverage_floor(xml_path, line_floor=85, command_label="repo checks")

    assert result.exit_code == 0
    assert result.line_percent == 87.55
    assert result.branch_percent == 74.8
    assert "Global Python line coverage is 87.55% (floor 85.00%)." in result.message
    assert "Branch coverage is 74.80% and advisory-only; it did not affect this result." in result.message


def test_line_floor_failure_uses_contract_message(tmp_path: Path) -> None:
    xml_path = _write_xml(tmp_path / "coverage.xml", line_rate="0.8499", branch_rate="0.9900")

    result = checker.evaluate_coverage_floor(xml_path, line_floor=85, command_label="repo checks")

    assert result.exit_code == 1
    assert "below Mythic Edge's accepted 85.00% floor" in result.message
    assert "Measured line coverage: 84.99%." in result.message
    assert "Branch coverage is 99.00% and advisory-only; it did not cause this failure." in result.message
    assert "Failed command: repo checks." in result.message
    assert "Do not commit raw coverage artifacts." in result.message


def test_missing_xml_fails_without_echoing_path(tmp_path: Path) -> None:
    xml_path = tmp_path / "private" / "coverage.xml"

    result = checker.evaluate_coverage_floor(xml_path, line_floor=85)

    assert result.exit_code == 2
    assert str(xml_path) not in result.message
    assert "Coverage XML is missing." in result.message


def test_malformed_xml_fails_without_echoing_parser_details(tmp_path: Path) -> None:
    xml_path = tmp_path / "coverage.xml"
    xml_path.write_text("<coverage", encoding="utf-8")

    result = checker.evaluate_coverage_floor(xml_path, line_floor=85)

    assert result.exit_code == 2
    assert str(xml_path) not in result.message
    assert "malformed or unreadable" in result.message


def test_missing_branch_rate_remains_advisory(tmp_path: Path) -> None:
    xml_path = tmp_path / "coverage.xml"
    xml_path.write_text('<?xml version="1.0" ?><coverage line-rate="0.8500"></coverage>\n', encoding="utf-8")

    result = checker.evaluate_coverage_floor(xml_path, line_floor=85)

    assert result.exit_code == 0
    assert result.line_percent == 85.0
    assert result.branch_percent is None
    assert "Branch coverage is advisory-only and did not affect this result." in result.message


def test_protected_surface_floor_passes_when_each_required_file_is_above_floor(tmp_path: Path) -> None:
    xml_path = _write_protected_surface_xml(tmp_path / "coverage.xml")

    result = checker.evaluate_coverage_floor(
        xml_path,
        line_floor=85,
        protected_surface_group="parser_state_final_reconciliation",
        protected_surface_line_floor=88,
        command_label="repo checks",
    )

    assert result.exit_code == 0
    assert result.line_percent == 87.64
    assert "Global Python line coverage is 87.64% (floor 85.00%)." in result.message
    assert "Protected-surface line coverage for parser_state_final_reconciliation is 90.45%" in result.message
    assert "minimum required file" in result.message
    assert "src/mythic_edge_parser/app/models.py: 90.45%" in result.message
    assert "src/mythic_edge_parser/app/state.py: 92.96%" in result.message
    assert "Branch coverage is 74.86% and advisory-only; it did not affect this result." in result.message


def test_protected_surface_floor_accepts_pytest_cov_path_variants(tmp_path: Path) -> None:
    xml_path = _write_protected_surface_xml(
        tmp_path / "coverage.xml",
        models_filename="mythic_edge_parser/app/models.py",
        state_filename="app/state.py",
    )

    result = checker.evaluate_coverage_floor(
        xml_path,
        line_floor=85,
        protected_surface_group="parser_state_final_reconciliation",
        protected_surface_line_floor=88,
    )

    assert result.exit_code == 0
    assert "src/mythic_edge_parser/app/models.py: 90.45%" in result.message
    assert "src/mythic_edge_parser/app/state.py: 92.96%" in result.message


def test_protected_surface_floor_fails_when_models_file_is_below_floor(tmp_path: Path) -> None:
    xml_path = _write_protected_surface_xml(tmp_path / "coverage.xml", models_line_rate="0.8799")

    result = checker.evaluate_coverage_floor(
        xml_path,
        line_floor=85,
        protected_surface_group="parser_state_final_reconciliation",
        protected_surface_line_floor=88,
        command_label="repo checks",
    )

    assert result.exit_code == 1
    assert "below Mythic Edge's accepted 88.00% floor" in result.message
    assert "Measured minimum candidate-file line coverage: 87.99%." in result.message
    assert "src/mythic_edge_parser/app/models.py: 87.99% (below floor 88.00%)" in result.message
    assert "src/mythic_edge_parser/app/state.py: 92.96%" in result.message
    assert "Branch coverage is 74.86% and advisory-only; it did not cause this failure." in result.message
    assert "Failed command: repo checks." in result.message
    assert "Do not commit raw coverage artifacts." in result.message


def test_protected_surface_floor_fails_when_state_file_is_below_floor(tmp_path: Path) -> None:
    xml_path = _write_protected_surface_xml(tmp_path / "coverage.xml", state_line_rate="0.8700")

    result = checker.evaluate_coverage_floor(
        xml_path,
        line_floor=85,
        protected_surface_group="parser_state_final_reconciliation",
        protected_surface_line_floor=88,
    )

    assert result.exit_code == 1
    assert "Measured minimum candidate-file line coverage: 87.00%." in result.message
    assert "src/mythic_edge_parser/app/state.py: 87.00% (below floor 88.00%)" in result.message


def test_protected_surface_floor_fails_closed_when_required_file_is_missing(tmp_path: Path) -> None:
    xml_path = _write_protected_surface_xml(tmp_path / "coverage.xml", state_line_rate=None)

    result = checker.evaluate_coverage_floor(
        xml_path,
        line_floor=85,
        protected_surface_group="parser_state_final_reconciliation",
        protected_surface_line_floor=88,
    )

    assert result.exit_code == 2
    assert "missing required protected-surface file src/mythic_edge_parser/app/state.py" in result.message
    assert str(xml_path) not in result.message


def test_protected_surface_floor_fails_closed_when_required_line_rate_is_invalid(tmp_path: Path) -> None:
    xml_path = _write_protected_surface_xml(tmp_path / "coverage.xml", state_line_rate="not-a-rate")

    result = checker.evaluate_coverage_floor(
        xml_path,
        line_floor=85,
        protected_surface_group="parser_state_final_reconciliation",
        protected_surface_line_floor=88,
    )

    assert result.exit_code == 2
    assert "missing or invalid line coverage" in result.message
    assert "src/mythic_edge_parser/app/state.py" in result.message
    assert str(xml_path) not in result.message


def test_protected_surface_floor_keeps_branch_coverage_advisory_only(tmp_path: Path) -> None:
    xml_path = _write_protected_surface_xml(tmp_path / "coverage.xml", branch_rate="0.0100")

    result = checker.evaluate_coverage_floor(
        xml_path,
        line_floor=85,
        protected_surface_group="parser_state_final_reconciliation",
        protected_surface_line_floor=88,
    )

    assert result.exit_code == 0
    assert result.branch_percent == 1.0
    assert "Branch coverage is 1.00% and advisory-only; it did not affect this result." in result.message


def test_unsupported_protected_surface_group_is_rejected_without_path_echo(tmp_path: Path) -> None:
    xml_path = _write_protected_surface_xml(tmp_path / "coverage.xml")

    result = checker.evaluate_coverage_floor(
        xml_path,
        line_floor=85,
        protected_surface_group="unsafe/group",
        protected_surface_line_floor=88,
    )

    assert result.exit_code == 2
    assert "Unsupported protected-surface coverage group: <unsupported-group>." in result.message
    assert "unsafe/group" not in result.message
