from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_workflow_freshness.py"
SPEC = importlib.util.spec_from_file_location("check_workflow_freshness", MODULE_PATH)
assert SPEC is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
assert SPEC.loader is not None
SPEC.loader.exec_module(checker)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


def _init_repo(tmp_path: Path, branch: str = "codex/analytics-foundation") -> Path:
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", branch)
    (repo / "README.md").write_text("# test repo\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "init"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return repo


def test_untracked_source_artifact_preserves_github_unknown_route_without_github(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    contract = repo / "docs" / "contracts" / "codeql_code_scanning_alert_triage.md"
    contract.parent.mkdir(parents=True)
    contract.write_text("# contract\n", encoding="utf-8")

    report = checker.run_check(
        repo,
        issue=331,
        source_artifact="docs/contracts/codeql_code_scanning_alert_triage.md",
        expected_branch="codex/analytics-foundation",
        include_worktrees=False,
        no_gh=True,
    )

    assert report.result == checker.VERDICT_GITHUB_STATE_UNKNOWN
    assert report.recommended_route == checker.ROUTE_ASK_USER
    assert report.issue.state == "unknown"
    assert report.artifacts[0].status == "untracked_candidate_artifact"
    assert "GitHub issue state is unknown" in report.stop_conditions[0]


def test_branch_mismatch_stops_before_editing(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, branch="codex/observed")

    report = checker.run_check(
        repo,
        issue=331,
        expected_branch="codex/expected",
        include_worktrees=False,
        no_gh=True,
    )

    assert report.result == checker.VERDICT_BRANCH_MISMATCH
    assert report.recommended_route == checker.ROUTE_ASK_USER
    assert "Current branch differs" in report.stop_conditions[0]


def test_expected_worktree_mismatch_stops_before_editing(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "current-worktree")

    report = checker.run_check(
        repo,
        expected_branch="codex/analytics-foundation",
        expected_worktree="different-worktree",
        include_worktrees=False,
        no_gh=True,
    )

    assert report.result == checker.VERDICT_WORKTREE_MISMATCH
    assert report.recommended_route == checker.ROUTE_ASK_USER
    assert "Current worktree differs" in report.stop_conditions[0]


def test_expected_worktree_name_match_allows_fresh_result(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "expected-worktree")

    report = checker.run_check(
        repo,
        expected_branch="codex/analytics-foundation",
        expected_worktree="repo",
        include_worktrees=False,
        no_gh=True,
    )

    assert report.result == checker.VERDICT_FRESH
    assert report.recommended_route == checker.ROUTE_CONTINUE_CURRENT_ROLE


def test_missing_expected_artifact_routes_to_codex_b(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)

    report = checker.run_check(
        repo,
        source_artifact="docs/contracts/missing.md",
        expected_branch="codex/analytics-foundation",
        include_worktrees=False,
        no_gh=True,
    )

    assert report.result == checker.VERDICT_ARTIFACT_MISSING
    assert report.recommended_route == checker.ROUTE_CODEX_B
    assert report.artifacts[0].status == "missing_expected_artifact"


def test_closed_issue_reentry_requires_user_route(tmp_path: Path, monkeypatch) -> None:
    repo = _init_repo(tmp_path)

    def fake_load_issue(number, repo_root, *, no_gh):
        return checker.IssueReport(number, "CLOSED", "https://example.invalid/issue", "closed", "2026-01-01T00:00:00Z")

    monkeypatch.setattr(checker, "_load_issue", fake_load_issue)

    report = checker.run_check(
        repo,
        issue=302,
        expected_branch="codex/analytics-foundation",
        include_worktrees=False,
    )

    assert report.result == checker.VERDICT_CLOSED_ISSUE_REENTRY
    assert report.recommended_route == checker.ROUTE_ASK_USER


def test_json_output_is_deterministic_shape(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    report = checker.run_check(
        repo,
        issue=331,
        expected_branch="codex/analytics-foundation",
        include_worktrees=False,
        no_gh=True,
    )

    payload = json.loads(checker.render_json(report))

    assert payload["branch"]["current"] == "codex/analytics-foundation"
    assert payload["issue"]["number"] == 331
    assert payload["result"] == checker.VERDICT_GITHUB_STATE_UNKNOWN


def test_text_output_lists_verdict_and_route(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    report = checker.run_check(
        repo,
        issue=331,
        expected_branch="codex/analytics-foundation",
        include_worktrees=False,
        no_gh=True,
    )

    text = checker.render_text(report)

    assert "Workflow Freshness Guard" in text
    assert f"result: {checker.VERDICT_GITHUB_STATE_UNKNOWN}" in text
    assert f"recommended_route: {checker.ROUTE_ASK_USER}" in text


def test_worktree_porcelain_parser_preserves_paths_with_spaces(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "root with spaces")
    output = f"""worktree {repo}
HEAD abc123
branch refs/heads/codex/analytics-foundation

worktree {tmp_path / "other worktree 331"}
HEAD def456
branch refs/heads/codex/example-331
"""

    reports = checker._parse_worktrees(output, repo, 331, "OPEN")

    assert reports[0].path == str(repo)
    assert reports[0].classification == "primary_current_worktree"
    assert reports[1].path.endswith("other worktree 331")
    assert reports[1].classification == "active_issue_worktree"
