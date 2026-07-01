"""Generate an advisory protected-surface coverage report."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPORT_OBJECT = "mythic_edge_quality_protected_surface_coverage_advisory"
REPORT_SCHEMA_VERSION = "protected_surface_coverage_advisory.v1"
REPOSITORY = "Tahjali11/Mythic-Edge"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge"
ISSUE_URL = "https://github.com/Tahjali11/Mythic-Edge/issues/605"
TRACKER_URL = "https://github.com/Tahjali11/Mythic-Edge/issues/566"
CONTRACT_REF = "docs/contracts/quality_protected_surface_coverage_floor_readiness.md"
REPORT_DIR = Path("docs/quality_reports/coverage/protected_surface")
DEFAULT_COVERAGE_SOURCE = "src/mythic_edge_parser"
DEFAULT_COVERAGE_COMMAND = (
    "py -m pytest -q tests --cov=src/mythic_edge_parser "
    "--cov-report=term-missing --cov-report=xml:<local-ignored-coverage-xml>"
)
GLOBAL_LINE_FLOOR_PERCENT = 85.0
DEFAULT_NEXT_ROLE = "Codex E: Module Reviewer / contract-test thread"

NON_CLAIMS = (
    "advisory measurement only",
    "not a protected-surface coverage gate",
    "not CI enforcement",
    "not branch coverage enforcement",
    "not parser truth",
    "not parser correctness proof",
    "not protected-surface authorization",
    "not security assurance",
    "not privacy assurance",
    "not release readiness",
    "not deploy readiness",
    "not production readiness",
    "not analytics truth",
    "not AI truth",
    "not coaching truth",
)


@dataclass(frozen=True)
class RepoMetadata:
    measured_ref: str
    measured_commit: str


@dataclass(frozen=True)
class CoverageFile:
    path: str
    line_coverage_percent: float | None
    branch_coverage_percent: float | None


@dataclass(frozen=True)
class CoverageData:
    global_line_coverage_percent: float | None
    global_branch_coverage_percent: float | None
    files: dict[str, CoverageFile]
    error: str = ""

    @property
    def parsed(self) -> bool:
        return not self.error


@dataclass(frozen=True)
class GroupSpec:
    group_id: str
    protected_category_id: str
    internal_project_area: str
    paths: tuple[str, ...] = ()
    path_globs: tuple[str, ...] = ()
    not_applicable_reason: str = ""

    @property
    def measurable(self) -> bool:
        return not self.not_applicable_reason


MEASURABLE_GROUPS: tuple[GroupSpec, ...] = (
    GroupSpec(
        group_id="parser_event_classes",
        protected_category_id="parser_event_classes",
        internal_project_area="Parser",
        paths=("src/mythic_edge_parser/events.py",),
    ),
    GroupSpec(
        group_id="parser_state_final_reconciliation",
        protected_category_id="parser_state_final_reconciliation",
        internal_project_area="Parser",
        paths=("src/mythic_edge_parser/app/state.py", "src/mythic_edge_parser/app/models.py"),
    ),
    GroupSpec(
        group_id="extractor_behavior",
        protected_category_id="extractor_behavior",
        internal_project_area="Parser",
        paths=("src/mythic_edge_parser/app/extractors.py",),
    ),
    GroupSpec(
        group_id="match_game_identity",
        protected_category_id="match_game_identity",
        internal_project_area="Parser",
        paths=(
            "src/mythic_edge_parser/app/gameplay_actions.py",
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/transforms.py",
        ),
        path_globs=("src/mythic_edge_parser/parsers/**/*.py",),
    ),
    GroupSpec(
        group_id="workbook_schema_and_exports",
        protected_category_id="workbook_schema",
        internal_project_area="Workbook / Transport",
        paths=(
            "src/mythic_edge_parser/app/sheet_schema.py",
            "src/mythic_edge_parser/app/sheet_exports.py",
            "src/mythic_edge_parser/app/transforms.py",
        ),
    ),
    GroupSpec(
        group_id="webhook_payload_and_transport",
        protected_category_id="webhook_payload_shape",
        internal_project_area="Workbook / Transport",
        paths=(
            "src/mythic_edge_parser/app/outputs.py",
            "src/mythic_edge_parser/app/runner.py",
            "src/mythic_edge_parser/app/transforms.py",
        ),
    ),
    GroupSpec(
        group_id="environment_runtime_python_paths",
        protected_category_id="environment_runtime_paths",
        internal_project_area="Parser",
        paths=("src/mythic_edge_parser/app/config.py",),
    ),
    GroupSpec(
        group_id="analytics_schema_and_ingest",
        protected_category_id="protected_adjacent_analytics_area",
        internal_project_area="Analytics",
        path_globs=("src/mythic_edge_parser/app/analytics_*.py",),
    ),
    GroupSpec(
        group_id="local_app_security_and_artifact_safety",
        protected_category_id="protected_adjacent_local_app_area",
        internal_project_area="Local App / UI",
        path_globs=("src/mythic_edge_parser/local_app/**/*.py",),
    ),
)

NON_MEASURABLE_GROUPS: tuple[GroupSpec, ...] = (
    GroupSpec(
        group_id="apps_script_behavior",
        protected_category_id="apps_script_behavior",
        internal_project_area="Workbook / Transport",
        paths=("tools/google_apps_script/Code.gs",),
        not_applicable_reason="Apps Script is outside the current Python coverage source.",
    ),
    GroupSpec(
        group_id="workflow_authority_docs",
        protected_category_id="workflow_authority_docs",
        internal_project_area="Quality / Governance",
        paths=("AGENTS.md", "docs/agent_constitution.md", "docs/agent_rules.yml", "docs/codex_module_workflow.md"),
        not_applicable_reason="Governance docs are not executable Python coverage targets.",
    ),
    GroupSpec(
        group_id="workflow_ci_yaml",
        protected_category_id="environment_runtime_paths",
        internal_project_area="Quality / Governance",
        paths=(".github/workflows/repo-checks.yml",),
        not_applicable_reason="GitHub workflow YAML is outside the current Python coverage source.",
    ),
    GroupSpec(
        group_id="local_artifact_checker_tools",
        protected_category_id="local_artifact_safety_tooling",
        internal_project_area="Quality / Governance",
        paths=("tools/check_protected_surfaces.py", "tools/check_secret_patterns.py"),
        not_applicable_reason="Quality tools are outside the current coverage source.",
    ),
    GroupSpec(
        group_id="forbidden_local_artifact_paths",
        protected_category_id="local_artifact_surfaces",
        internal_project_area="Generated / Local Artifacts",
        paths=("data/", "_review_/", "frontend/dist/"),
        not_applicable_reason="Local/generated/private artifacts are not coverage targets.",
    ),
)


class ConfigError(Exception):
    """Configuration error that should fail closed without echoing private paths."""


def normalize_repo_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    text = text.lstrip("/")
    parts = [part for part in text.split("/") if part and part != "."]
    return "/".join(parts)


def _short_commit(commit: str) -> str:
    return commit[:7] if commit else "unknown"


def _rate_to_percent(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value) * 100, 2)
    except ValueError:
        return None


def _coverage_filename_to_repo_path(filename: str) -> str:
    path = normalize_repo_path(filename)
    source_marker = f"{DEFAULT_COVERAGE_SOURCE}/"
    if source_marker in path:
        return path[path.index(source_marker) :]
    if path.startswith("mythic_edge_parser/"):
        return f"src/{path}"
    if not path.startswith("src/"):
        return f"{DEFAULT_COVERAGE_SOURCE}/{path}"
    return path


def read_coverage_xml(coverage_xml: str | Path) -> CoverageData:
    path = Path(coverage_xml)
    if not path.is_file():
        return CoverageData(None, None, {}, error="coverage_xml_missing")
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        return CoverageData(None, None, {}, error="coverage_xml_malformed_or_unreadable")

    files: dict[str, CoverageFile] = {}
    for item in root.findall(".//class"):
        filename = item.attrib.get("filename")
        if not filename:
            continue
        repo_path = _coverage_filename_to_repo_path(filename)
        if not repo_path.startswith(f"{DEFAULT_COVERAGE_SOURCE}/"):
            continue
        files[repo_path] = CoverageFile(
            path=repo_path,
            line_coverage_percent=_rate_to_percent(item.attrib.get("line-rate")),
            branch_coverage_percent=_rate_to_percent(item.attrib.get("branch-rate")),
        )

    return CoverageData(
        global_line_coverage_percent=_rate_to_percent(root.attrib.get("line-rate")),
        global_branch_coverage_percent=_rate_to_percent(root.attrib.get("branch-rate")),
        files=dict(sorted(files.items())),
    )


def read_repo_metadata(repo_root: str | Path = ".") -> RepoMetadata:
    root = Path(repo_root)

    def run_git(args: list[str], fallback: str) -> str:
        try:
            completed = subprocess.run(
                ["git", *args],
                cwd=root,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except OSError:
            return fallback
        if completed.returncode != 0:
            return fallback
        return completed.stdout.strip() or fallback

    return RepoMetadata(
        measured_ref=run_git(["rev-parse", "--abbrev-ref", "HEAD"], "unknown"),
        measured_commit=run_git(["rev-parse", "HEAD"], "unknown"),
    )


def _matches_pattern(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(f"{prefix}/")
    return fnmatch.fnmatchcase(path, pattern)


def _expand_group_paths(spec: GroupSpec, repo_root: str | Path) -> tuple[str, ...]:
    root = Path(repo_root)
    paths = {normalize_repo_path(path) for path in spec.paths}
    for pattern in spec.path_globs:
        for item in root.glob(pattern):
            if item.is_file():
                paths.add(normalize_repo_path(item.relative_to(root)))
    return tuple(sorted(paths))


def _file_entry(path: str, coverage: CoverageData, *, measurable: bool, reason: str = "") -> dict[str, Any]:
    if not measurable:
        return {
            "path": path,
            "line_coverage_percent": None,
            "branch_coverage_percent": None,
            "branch_coverage_status": "advisory_unavailable",
            "coverage_status": "not_applicable_current_coverage_scope",
            "notes": [reason],
        }

    item = coverage.files.get(path)
    if item is None:
        status = "missing_from_coverage_xml" if coverage.parsed else coverage.error
        return {
            "path": path,
            "line_coverage_percent": None,
            "branch_coverage_percent": None,
            "branch_coverage_status": "advisory_unavailable",
            "coverage_status": status,
            "notes": ["Measured coverage data was not available for this repo-relative path."],
        }

    return {
        "path": path,
        "line_coverage_percent": item.line_coverage_percent,
        "branch_coverage_percent": item.branch_coverage_percent,
        "branch_coverage_status": "advisory_only",
        "coverage_status": "measured",
        "notes": ["Branch coverage is advisory-only and has no threshold."],
    }


def _group_scope_status(files: list[dict[str, Any]]) -> str:
    statuses = {item["coverage_status"] for item in files}
    if statuses == {"not_applicable_current_coverage_scope"}:
        return "not_applicable_current_coverage_scope"
    if "measured" in statuses:
        return "measured"
    if statuses <= {"missing_from_coverage_xml"}:
        return "missing_from_coverage_xml"
    if statuses <= {"coverage_xml_missing", "coverage_xml_malformed_or_unreadable"}:
        return next(iter(statuses))
    return "unmapped"


def _build_group(spec: GroupSpec, coverage: CoverageData, repo_root: str | Path) -> dict[str, Any]:
    paths = _expand_group_paths(spec, repo_root)
    files = [
        _file_entry(path, coverage, measurable=spec.measurable, reason=spec.not_applicable_reason)
        for path in paths
    ]
    return {
        "group_id": spec.group_id,
        "protected_category_id": spec.protected_category_id,
        "internal_project_area": spec.internal_project_area,
        "coverage_scope_status": _group_scope_status(files),
        "files": files,
    }


def _global_line_floor_status(coverage: CoverageData) -> str:
    if not coverage.parsed or coverage.global_line_coverage_percent is None:
        return "not_run"
    if coverage.global_line_coverage_percent + 1e-9 >= GLOBAL_LINE_FLOOR_PERCENT:
        return "passed"
    return "failed"


def build_report(
    *,
    coverage_xml: str | Path,
    repo_root: str | Path = ".",
    metadata: RepoMetadata | None = None,
    coverage_command: str = DEFAULT_COVERAGE_COMMAND,
    coverage_source: str = DEFAULT_COVERAGE_SOURCE,
) -> dict[str, Any]:
    metadata = metadata or read_repo_metadata(repo_root)
    coverage = read_coverage_xml(coverage_xml)
    groups = [
        _build_group(spec, coverage, repo_root)
        for spec in (*MEASURABLE_GROUPS, *NON_MEASURABLE_GROUPS)
    ]
    overall_status = "passed_advisory" if coverage.parsed else "failed_advisory"
    return {
        "object": REPORT_OBJECT,
        "schema_version": REPORT_SCHEMA_VERSION,
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "issue": ISSUE_URL,
        "tracker": TRACKER_URL,
        "contract_ref": CONTRACT_REF,
        "measured_ref": metadata.measured_ref,
        "measured_commit": metadata.measured_commit,
        "coverage_command": coverage_command,
        "coverage_source": coverage_source,
        "overall_status": overall_status,
        "coverage_xml_status": "parsed" if coverage.parsed else coverage.error,
        "global_line_coverage_percent": coverage.global_line_coverage_percent,
        "global_branch_coverage_percent": coverage.global_branch_coverage_percent,
        "global_line_floor_percent": GLOBAL_LINE_FLOOR_PERCENT,
        "global_line_floor_status": _global_line_floor_status(coverage),
        "branch_coverage_status": "advisory_only",
        "protected_surface_floor_status": "not_authorized",
        "protected_surface_floor_authorized": False,
        "ci_change_authorized": False,
        "global_line_floor_increase_authorized": False,
        "branch_coverage_enforcement_authorized": False,
        "raw_artifacts_committed": False,
        "advisory_only": True,
        "groups": groups,
        "non_claims": list(NON_CLAIMS),
        "next_recommended_role": DEFAULT_NEXT_ROLE,
    }


def default_report_path(report_date: str, commit: str) -> Path:
    return REPORT_DIR / f"{report_date}-{_short_commit(commit)}-protected-surface-coverage-advisory.json"


def validate_output_path(repo_root: str | Path, output: str | Path) -> Path:
    root = Path(repo_root).resolve()
    target = Path(output)
    if not target.is_absolute():
        target = root / target
    try:
        relative = normalize_repo_path(target.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except ValueError as exc:
        raise ConfigError("output path must stay inside the repository") from exc
    if not relative.startswith(f"{REPORT_DIR.as_posix()}/") or not relative.endswith(".json"):
        raise ConfigError("output path must be a JSON file under docs/quality_reports/coverage/protected_surface/")
    return target


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an advisory protected-surface coverage report.")
    parser.add_argument("--coverage-xml", required=True, type=Path, help="Ignored local coverage XML to read.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--coverage-command", default=DEFAULT_COVERAGE_COMMAND, help="Public-safe command label.")
    parser.add_argument("--coverage-source", default=DEFAULT_COVERAGE_SOURCE, help="Coverage source label.")
    parser.add_argument("--measured-ref", help="Measured branch or ref label.")
    parser.add_argument("--measured-commit", help="Measured commit hash.")
    parser.add_argument(
        "--report-date",
        default=datetime.now(UTC).date().isoformat(),
        help="Report date used for the default report path.",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON output path under the approved report directory.")
    parser.add_argument("--write-report", action="store_true", help="Write the default report path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    metadata = None
    if args.measured_ref or args.measured_commit:
        metadata = RepoMetadata(
            measured_ref=args.measured_ref or "unknown",
            measured_commit=args.measured_commit or "unknown",
        )

    try:
        report = build_report(
            coverage_xml=args.coverage_xml,
            repo_root=args.repo_root,
            metadata=metadata,
            coverage_command=args.coverage_command,
            coverage_source=args.coverage_source,
        )
        output_path = args.output
        if args.write_report:
            output_path = default_report_path(args.report_date, report["measured_commit"])
        if output_path is not None:
            target = validate_output_path(args.repo_root, output_path)
            write_report(target, report)
            print(normalize_repo_path(target.relative_to(Path(args.repo_root).resolve())))
        else:
            print(json.dumps(report, indent=2, sort_keys=True))
    except ConfigError as exc:
        print(f"ERROR configuration - {exc}", file=sys.stderr)
        return 2
    except OSError:
        print("ERROR filesystem - unable to write protected-surface coverage report", file=sys.stderr)
        return 2

    return 0 if report["overall_status"] == "passed_advisory" else 2


if __name__ == "__main__":
    raise SystemExit(main())
