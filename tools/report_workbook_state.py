"""Read-only workbook/App Script state probe for Mythic Edge."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class WorkbookProbeReport:
    code_gs_path: str
    code_gs_sha256: str
    deployed_state: str
    workbook_state: str
    findings: tuple[str, ...]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _load_state(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _expected_headers(repo_root: Path) -> dict[str, list[str]]:
    sys.path.insert(0, str(repo_root / "src"))
    from mythic_edge_parser.app import sheet_schema

    return {
        "Match Log": list(sheet_schema.MATCH_LOG_SYNC_FIELDS),
        "Game Log": list(sheet_schema.GAME_LOG_SYNC_FIELDS),
    }


def build_report(repo_root: Path, *, state_json: Path | None = None) -> WorkbookProbeReport:
    code_gs_path = repo_root / "tools" / "google_apps_script" / "Code.gs"
    code_hash = _sha256(code_gs_path)
    state = _load_state(state_json)
    findings: list[str] = []

    deployed = state.get("deployed_apps_script") or {}
    deployed_hash = deployed.get("code_gs_sha256")
    if deployed_hash:
        deployed_state = "matches repo" if deployed_hash == code_hash else "differs from repo"
        if deployed_hash != code_hash:
            findings.append("Deployed Apps Script hash differs from repo Code.gs hash.")
    else:
        deployed_state = "unverified; no state JSON hash supplied"

    workbook_headers = state.get("workbook_headers") or {}
    if workbook_headers:
        expected = _expected_headers(repo_root)
        for sheet_name, expected_headers in expected.items():
            actual_headers = workbook_headers.get(sheet_name)
            if actual_headers is None:
                findings.append(f"Workbook state JSON does not include headers for {sheet_name}.")
                continue
            missing = [header for header in expected_headers if header not in actual_headers]
            if missing:
                findings.append(f"{sheet_name} is missing expected parser sync fields: {', '.join(missing)}")
        workbook_state = "checked against supplied state JSON"
    else:
        workbook_state = "unverified; no workbook headers supplied"

    return WorkbookProbeReport(
        code_gs_path=str(code_gs_path),
        code_gs_sha256=code_hash,
        deployed_state=deployed_state,
        workbook_state=workbook_state,
        findings=tuple(findings),
    )


def render_report(report: WorkbookProbeReport) -> str:
    lines = [
        "Workbook State Probe",
        f"repo_code_gs: {report.code_gs_path}",
        f"repo_code_gs_sha256: {report.code_gs_sha256}",
        f"deployed_apps_script: {report.deployed_state}",
        f"live_workbook_headers: {report.workbook_state}",
        f"findings: {len(report.findings)}",
    ]
    for finding in report.findings:
        lines.append(f"WARNING {finding}")
    lines.append("result: passed")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report repo/deployed/workbook state without mutating anything.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--state-json", default="", help="Optional local JSON export of deployed/workbook state.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    state_path = Path(args.state_json).resolve() if args.state_json else None
    try:
        report = build_report(repo_root, state_json=state_path)
    except (OSError, json.JSONDecodeError, ImportError) as exc:
        print(f"Workbook State Probe\nerror: {exc}\nresult: error")
        return 2

    print(render_report(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
