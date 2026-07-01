from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_REPO_CHECKS = REPO_ROOT / "tools" / "run_repo_checks.ps1"


def test_run_repo_checks_lint_scope_matches_ci_tools_surface() -> None:
    script = RUN_REPO_CHECKS.read_text(encoding="utf-8")

    lint_lines = [line.strip() for line in script.splitlines() if "Running lint checks" in line]

    assert lint_lines == ['Invoke-Checked "Running lint checks..." py -m ruff check src tests tools']
