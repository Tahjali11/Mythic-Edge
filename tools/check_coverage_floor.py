from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

DEFAULT_LINE_FLOOR = 85.0


@dataclass(frozen=True)
class CoverageFloorResult:
    exit_code: int
    line_percent: float | None
    branch_percent: float | None
    message: str


def _format_percent(value: float) -> str:
    return f"{value:.2f}%"


def _read_rate(root: ET.Element, name: str) -> float | None:
    raw_value = root.attrib.get(name)
    if raw_value is None:
        return None
    try:
        return float(raw_value) * 100
    except ValueError:
        return None


def evaluate_coverage_floor(
    coverage_xml: Path,
    *,
    line_floor: float = DEFAULT_LINE_FLOOR,
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

    if line_percent + 1e-9 >= line_floor:
        return CoverageFloorResult(
            exit_code=0,
            line_percent=line_percent,
            branch_percent=branch_percent,
            message=(
                f"Global Python line coverage is {_format_percent(line_percent)} "
                f"(floor {_format_percent(line_floor)}). {branch_result_message}"
            ),
        )

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check Mythic Edge aggregate Python line coverage floor.")
    parser.add_argument("--coverage-xml", required=True, type=Path, help="Coverage XML produced by pytest-cov.")
    parser.add_argument("--line-floor", default=DEFAULT_LINE_FLOOR, type=float, help="Required line coverage percent.")
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
        command_label=args.command_label,
    )
    stream = sys.stdout if result.exit_code == 0 else sys.stderr
    print(result.message, file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
