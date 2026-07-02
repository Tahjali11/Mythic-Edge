from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

DEFAULT_LINE_FLOOR = 85.0
DEFAULT_PROTECTED_SURFACE_LINE_FLOOR = 88.0
SUPPORTED_PROTECTED_SURFACE_GROUPS = {
    "parser_state_final_reconciliation": (
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/state.py",
    ),
}
_SAFE_SYMBOL_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


@dataclass(frozen=True)
class CoverageFloorResult:
    exit_code: int
    line_percent: float | None
    branch_percent: float | None
    message: str


@dataclass(frozen=True)
class _ProtectedFileMeasurement:
    path: str
    line_percent: float


def _format_percent(value: float) -> str:
    return f"{value:.2f}%"


def _safe_symbol(value: str) -> str:
    if _SAFE_SYMBOL_RE.fullmatch(value):
        return value
    return "<unsupported-group>"


def _read_rate(root: ET.Element, name: str) -> float | None:
    raw_value = root.attrib.get(name)
    if raw_value is None:
        return None
    try:
        return float(raw_value) * 100
    except ValueError:
        return None


def _read_class_line_rate(class_element: ET.Element) -> float | None:
    raw_value = class_element.attrib.get("line-rate")
    if raw_value is None:
        return None
    try:
        return float(raw_value) * 100
    except ValueError:
        return None


def _coverage_filename_candidates(filename: str) -> set[str]:
    normalized = filename.replace("\\", "/").lstrip("./")
    candidates = {normalized}
    if "mythic_edge_parser/" in normalized:
        package_relative = normalized.split("mythic_edge_parser/", 1)[1]
        candidates.add(f"src/mythic_edge_parser/{package_relative}")
    if normalized.startswith("app/"):
        candidates.add(f"src/mythic_edge_parser/{normalized}")
    return candidates


def _class_elements_by_repo_path(root: ET.Element) -> dict[str, ET.Element]:
    class_elements: dict[str, ET.Element] = {}
    for class_element in root.iter("class"):
        filename = class_element.attrib.get("filename", "")
        for candidate in _coverage_filename_candidates(filename):
            class_elements.setdefault(candidate, class_element)
    return class_elements


def _branch_success_message(branch_percent: float | None) -> str:
    if branch_percent is None:
        return "Branch coverage is advisory-only and did not affect this result."
    return f"Branch coverage is {_format_percent(branch_percent)} and advisory-only; it did not affect this result."


def _branch_failure_message(branch_percent: float | None) -> str:
    if branch_percent is None:
        return "Branch coverage is advisory-only and did not cause this failure."
    return f"Branch coverage is {_format_percent(branch_percent)} and advisory-only; it did not cause this failure."


def _evaluate_protected_surface_floor(
    root: ET.Element,
    *,
    group_id: str,
    line_floor: float,
    branch_percent: float | None,
    command_label: str,
) -> CoverageFloorResult:
    required_paths = SUPPORTED_PROTECTED_SURFACE_GROUPS.get(group_id)
    if required_paths is None:
        return CoverageFloorResult(
            exit_code=2,
            line_percent=None,
            branch_percent=branch_percent,
            message=f"Unsupported protected-surface coverage group: {_safe_symbol(group_id)}.",
        )

    class_elements = _class_elements_by_repo_path(root)
    measurements: list[_ProtectedFileMeasurement] = []
    for required_path in required_paths:
        class_element = class_elements.get(required_path)
        if class_element is None:
            return CoverageFloorResult(
                exit_code=2,
                line_percent=None,
                branch_percent=branch_percent,
                message=(
                    "Coverage XML is missing required protected-surface file "
                    f"{required_path} for group {group_id}."
                ),
            )
        line_percent = _read_class_line_rate(class_element)
        if line_percent is None:
            return CoverageFloorResult(
                exit_code=2,
                line_percent=None,
                branch_percent=branch_percent,
                message=(
                    "Coverage XML has missing or invalid line coverage for required protected-surface file "
                    f"{required_path} in group {group_id}."
                ),
            )
        measurements.append(_ProtectedFileMeasurement(path=required_path, line_percent=line_percent))

    minimum_line_percent = min(item.line_percent for item in measurements)
    measurement_lines = [
        f"{item.path}: {_format_percent(item.line_percent)}"
        + (f" (below floor {_format_percent(line_floor)})" if item.line_percent + 1e-9 < line_floor else "")
        for item in measurements
    ]
    measurement_message = " ".join(measurement_lines)

    if minimum_line_percent + 1e-9 >= line_floor:
        return CoverageFloorResult(
            exit_code=0,
            line_percent=minimum_line_percent,
            branch_percent=branch_percent,
            message=(
                f"Protected-surface line coverage for {group_id} is {_format_percent(minimum_line_percent)} "
                f"(floor {_format_percent(line_floor)}; minimum required file). "
                f"{_branch_success_message(branch_percent)} {measurement_message}"
            ),
        )

    return CoverageFloorResult(
        exit_code=1,
        line_percent=minimum_line_percent,
        branch_percent=branch_percent,
        message=(
            f"Protected-surface line coverage for {group_id} is below Mythic Edge's accepted "
            f"{_format_percent(line_floor)} floor. Measured minimum candidate-file line coverage: "
            f"{_format_percent(minimum_line_percent)}. {_branch_failure_message(branch_percent)} "
            f"Failed command: {command_label}. {measurement_message} "
            "Add focused behavior-preserving tests, rerun the approved coverage command on the current base, "
            "or route back to Codex B if the floor or scope is stale. Do not commit raw coverage artifacts."
        ),
    )


def evaluate_coverage_floor(
    coverage_xml: Path,
    *,
    line_floor: float = DEFAULT_LINE_FLOOR,
    protected_surface_group: str | None = None,
    protected_surface_line_floor: float = DEFAULT_PROTECTED_SURFACE_LINE_FLOOR,
    command_label: str = "coverage command",
) -> CoverageFloorResult:
    if not coverage_xml.is_file():
        return CoverageFloorResult(
            exit_code=2,
            line_percent=None,
            branch_percent=None,
            message=(
                "Coverage XML is missing. Rerun the approved coverage command before enforcing "
                "Mythic Edge's global Python line coverage floor."
            ),
        )

    try:
        root = ET.parse(coverage_xml).getroot()
    except (ET.ParseError, OSError):
        return CoverageFloorResult(
            exit_code=2,
            line_percent=None,
            branch_percent=None,
            message=(
                "Coverage XML is malformed or unreadable. Rerun the approved coverage command before enforcing "
                "Mythic Edge's global Python line coverage floor."
            ),
        )

    line_percent = _read_rate(root, "line-rate")
    branch_percent = _read_rate(root, "branch-rate")
    if line_percent is None:
        return CoverageFloorResult(
            exit_code=2,
            line_percent=None,
            branch_percent=branch_percent,
            message=(
                "Coverage XML is missing aggregate line coverage. Rerun the approved coverage command before "
                "enforcing Mythic Edge's global Python line coverage floor."
            ),
        )

    branch_result_message = "Branch coverage is advisory-only and did not affect this result."
    branch_failure_message = "Branch coverage is advisory-only and did not cause this failure."
    if branch_percent is not None:
        branch_result_message = (
            f"Branch coverage is {_format_percent(branch_percent)} and advisory-only; it did not affect this result."
        )
        branch_failure_message = (
            f"Branch coverage is {_format_percent(branch_percent)} and advisory-only; it did not cause this failure."
        )

    if line_percent + 1e-9 < line_floor:
        return CoverageFloorResult(
            exit_code=1,
            line_percent=line_percent,
            branch_percent=branch_percent,
            message=(
                f"Global Python line coverage is below Mythic Edge's accepted {_format_percent(line_floor)} floor. "
                f"Measured line coverage: {_format_percent(line_percent)}. {branch_failure_message} "
                f"Failed command: {command_label}. "
                "Rerun the approved coverage command on the current base, add focused tests for changed behavior, "
                "or route back to Codex B if the floor or scope is stale. Do not commit raw coverage artifacts."
            ),
        )

    if protected_surface_group is None:
        return CoverageFloorResult(
            exit_code=0,
            line_percent=line_percent,
            branch_percent=branch_percent,
            message=(
                f"Global Python line coverage is {_format_percent(line_percent)} "
                f"(floor {_format_percent(line_floor)}). {branch_result_message}"
            ),
        )

    protected_result = _evaluate_protected_surface_floor(
        root,
        group_id=protected_surface_group,
        line_floor=protected_surface_line_floor,
        branch_percent=branch_percent,
        command_label=command_label,
    )
    if protected_result.exit_code != 0:
        return protected_result
    return CoverageFloorResult(
        exit_code=0,
        line_percent=line_percent,
        branch_percent=branch_percent,
        message=(
            f"Global Python line coverage is {_format_percent(line_percent)} "
            f"(floor {_format_percent(line_floor)}). {protected_result.message}"
        ),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check Mythic Edge aggregate Python line coverage floor.")
    parser.add_argument("--coverage-xml", required=True, type=Path, help="Coverage XML produced by pytest-cov.")
    parser.add_argument("--line-floor", default=DEFAULT_LINE_FLOOR, type=float, help="Required line coverage percent.")
    parser.add_argument(
        "--protected-surface-group",
        help="Allow-listed protected-surface group to enforce after the global line floor passes.",
    )
    parser.add_argument(
        "--protected-surface-line-floor",
        default=DEFAULT_PROTECTED_SURFACE_LINE_FLOOR,
        type=float,
        help="Required line coverage percent for each required file in the protected-surface group.",
    )
    parser.add_argument(
        "--command-label",
        default="coverage command",
        help="Short label for the command or workflow being checked.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = evaluate_coverage_floor(
        args.coverage_xml,
        line_floor=args.line_floor,
        protected_surface_group=args.protected_surface_group,
        protected_surface_line_floor=args.protected_surface_line_floor,
        command_label=args.command_label,
    )
    stream = sys.stdout if result.exit_code == 0 else sys.stderr
    print(result.message, file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
