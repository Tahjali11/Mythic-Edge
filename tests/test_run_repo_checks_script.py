from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_REPO_CHECKS = REPO_ROOT / "tools" / "run_repo_checks.ps1"
REPO_CHECKS_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "repo-checks.yml"


def test_run_repo_checks_lint_scope_matches_ci_tools_surface() -> None:
    script = RUN_REPO_CHECKS.read_text(encoding="utf-8")

    lint_lines = [line.strip() for line in script.splitlines() if "Running lint checks" in line]

    assert lint_lines == ['Invoke-Checked "Running lint checks..." py -m ruff check src tests tools']


def test_run_repo_checks_coverage_invokes_parser_state_floor() -> None:
    script = RUN_REPO_CHECKS.read_text(encoding="utf-8")

    assert '$ProtectedSurfaceCoverageGroup = "parser_state_final_reconciliation"' in script
    assert '$ProtectedSurfaceCoverageFloorPercent = "88"' in script
    assert "--protected-surface-group $ProtectedSurfaceCoverageGroup" in script
    assert "--protected-surface-line-floor $ProtectedSurfaceCoverageFloorPercent" in script
    assert "--line-floor $CoverageFloorPercent" in script


def test_repo_checks_workflow_invokes_same_parser_state_floor() -> None:
    workflow = REPO_CHECKS_WORKFLOW.read_text(encoding="utf-8")

    assert "--line-floor 85" in workflow
    assert "--protected-surface-group parser_state_final_reconciliation" in workflow
    assert "--protected-surface-line-floor 88" in workflow
    assert '--command-label "GitHub Actions repo checks"' in workflow
