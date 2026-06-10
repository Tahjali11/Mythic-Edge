"""Report-only freshness guard for Mythic Edge workflow handoffs."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

VERDICT_FRESH = "fresh"
VERDICT_FRESH_WITH_WARNINGS = "fresh_with_warnings"
VERDICT_CLOSED_ISSUE_REENTRY = "closed_issue_reentry"
VERDICT_BRANCH_MISMATCH = "branch_mismatch"
VERDICT_WORKTREE_MISMATCH = "worktree_mismatch"
VERDICT_ARTIFACT_UNTRACKED = "artifact_untracked"
VERDICT_ARTIFACT_MISSING = "artifact_missing"
VERDICT_GITHUB_STATE_UNKNOWN = "github_state_unknown"
VERDICT_BLOCKED_NEEDS_USER_DECISION = "blocked_needs_user_decision"

ROUTE_CONTINUE_CURRENT_ROLE = "continue_current_role"
ROUTE_CODEX_B = "route_to_codex_b"
ROUTE_CODEX_C = "route_to_codex_c"
ROUTE_ASK_USER = "ask_user"
ROUTE_CLEANUP_CLASSIFICATION_ONLY = "cleanup_classification_only"


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class BranchReport:
    current: str
    intended: str
    upstream: str
    ahead: int | None
    behind: int | None


@dataclass(frozen=True)
class IssueReport:
    number: int | None
    state: str
    url: str
    title: str
    closed_at: str
    error: str = ""


@dataclass(frozen=True)
class ArtifactReport:
    path: str
    status: str
    git_status: str
    recommended_route: str


@dataclass(frozen=True)
class WorktreeReport:
    path: str
    branch: str
    classification: str


@dataclass(frozen=True)
class FreshnessReport:
    result: str
    recommended_route: str
    verified_at: str
    branch: BranchReport
    issue: IssueReport
    tracker: IssueReport
    artifacts: tuple[ArtifactReport, ...]
    worktrees: tuple[WorktreeReport, ...]
    dirty_paths: tuple[str, ...]
    untracked_artifacts: tuple[str, ...]
    warnings: tuple[str, ...]
    stop_conditions: tuple[str, ...]


def _run(args: list[str], repo_root: Path) -> CommandResult:
    completed = subprocess.run(
        args,
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def _git(args: list[str], repo_root: Path) -> CommandResult:
    return _run(["git", *args], repo_root)


def _current_branch(repo_root: Path) -> str:
    result = _git(["rev-parse", "--abbrev-ref", "HEAD"], repo_root)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def _upstream_branch(repo_root: Path) -> str:
    result = _git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], repo_root)
    return result.stdout.strip() if result.returncode == 0 else ""


def _ahead_behind(repo_root: Path, upstream: str) -> tuple[int | None, int | None]:
    if not upstream:
        return None, None
    result = _git(["rev-list", "--left-right", "--count", f"HEAD...{upstream}"], repo_root)
    if result.returncode != 0:
        return None, None
    parts = result.stdout.strip().split()
    if len(parts) != 2:
        return None, None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None, None


def _branch_report(repo_root: Path, intended_branch: str) -> BranchReport:
    current = _current_branch(repo_root)
    upstream = _upstream_branch(repo_root)
    ahead, behind = _ahead_behind(repo_root, upstream)
    return BranchReport(
        current=current,
        intended=intended_branch or current,
        upstream=upstream,
        ahead=ahead,
        behind=behind,
    )


def _parse_status(stdout: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    dirty: list[str] = []
    untracked: list[str] = []
    for line in stdout.splitlines():
        if not line or line.startswith("## "):
            continue
        path = line[3:] if len(line) > 3 else line
        if line.startswith("?? "):
            untracked.append(path)
        else:
            dirty.append(path)
    return tuple(dirty), tuple(untracked)


def _dirty_state(repo_root: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
    result = _git(["status", "--short", "--untracked-files=all"], repo_root)
    if result.returncode != 0:
        return (), ()
    return _parse_status(result.stdout)


def _git_status_for_path(repo_root: Path, artifact_path: str) -> str:
    result = _git(["status", "--short", "--untracked-files=all", "--", artifact_path], repo_root)
    return result.stdout.splitlines()[0] if result.returncode == 0 and result.stdout.strip() else ""


def _is_tracked(repo_root: Path, artifact_path: str) -> bool:
    result = _git(["ls-files", "--error-unmatch", artifact_path], repo_root)
    return result.returncode == 0


def _artifact_report(repo_root: Path, artifact_path: str) -> ArtifactReport:
    path = artifact_path.replace("\\", "/").strip()
    if not path:
        return ArtifactReport("", "not_requested", "", ROUTE_CONTINUE_CURRENT_ROLE)
    exists = (repo_root / path).exists()
    git_status = _git_status_for_path(repo_root, path)
    if not exists:
        return ArtifactReport(path, "missing_expected_artifact", git_status, ROUTE_CODEX_B)
    if git_status.startswith("?? "):
        return ArtifactReport(path, "untracked_candidate_artifact", git_status, ROUTE_CODEX_C)
    if git_status and git_status[0] != " ":
        return ArtifactReport(path, "staged_pending_submission", git_status, ROUTE_CONTINUE_CURRENT_ROLE)
    if _is_tracked(repo_root, path):
        return ArtifactReport(path, "tracked_official_artifact", git_status, ROUTE_CONTINUE_CURRENT_ROLE)
    return ArtifactReport(path, "unknown_requires_user_or_role_review", git_status, ROUTE_ASK_USER)


def _load_issue(number: int | None, repo_root: Path, *, no_gh: bool) -> IssueReport:
    if number is None:
        return IssueReport(None, "not_requested", "", "", "")
    if no_gh:
        return IssueReport(number, "unknown", "", "", "", error="GitHub lookup disabled by --no-gh.")
    result = _run(
        ["gh", "issue", "view", str(number), "--json", "number,title,state,url,closedAt"],
        repo_root,
    )
    if result.returncode != 0:
        error = result.stderr or result.stdout or "GitHub issue lookup failed."
        return IssueReport(number, "unknown", "", "", "", error=error)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return IssueReport(number, "unknown", "", "", "", error=f"GitHub issue JSON decode failed: {exc}")
    return IssueReport(
        number=int(data.get("number") or number),
        state=str(data.get("state") or "unknown"),
        url=str(data.get("url") or ""),
        title=str(data.get("title") or ""),
        closed_at=str(data.get("closedAt") or ""),
    )


def _parse_worktrees(stdout: str, repo_root: Path, issue: int | None, issue_state: str) -> tuple[WorktreeReport, ...]:
    reports: list[WorktreeReport] = []
    current_path = repo_root.resolve()
    current: dict[str, str] = {}
    entries: list[dict[str, str]] = []
    for line in stdout.splitlines():
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        entries.append(current)

    for entry in entries:
        path = entry.get("worktree", "")
        branch_ref = entry.get("branch", "")
        branch = branch_ref.removeprefix("refs/heads/")
        normalized_path = Path(path).resolve()
        if normalized_path == current_path:
            classification = "primary_current_worktree"
        elif issue is not None and str(issue) in f"{path} {branch}":
            classification = (
                "closed_issue_worktree_candidate" if issue_state.upper() == "CLOSED" else "active_issue_worktree"
            )
        else:
            classification = "unknown_or_unlinked_worktree"
        reports.append(WorktreeReport(path=path, branch=branch, classification=classification))
    return tuple(reports)


def _worktree_reports(
    repo_root: Path,
    issue: int | None,
    issue_state: str,
    include_worktrees: bool,
) -> tuple[WorktreeReport, ...]:
    if not include_worktrees:
        return ()
    result = _git(["worktree", "list", "--porcelain"], repo_root)
    if result.returncode != 0:
        return ()
    return _parse_worktrees(result.stdout, repo_root, issue, issue_state)


def _matches_expected_worktree(repo_root: Path, expected_worktree: str) -> bool:
    expected = expected_worktree.strip()
    if not expected:
        return True
    current = repo_root.resolve()
    expected_path = Path(expected)
    if expected_path.is_absolute():
        return current == expected_path.resolve()
    return current.name == expected or current == (current.parent / expected).resolve()


def _choose_result(
    branch: BranchReport,
    issue: IssueReport,
    artifacts: tuple[ArtifactReport, ...],
    dirty_paths: tuple[str, ...],
    untracked_paths: tuple[str, ...],
    worktree_matches_expected: bool,
) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    warnings: list[str] = []
    stop_conditions: list[str] = []
    if branch.current != "unknown" and branch.intended and branch.current != branch.intended:
        stop_conditions.append(
            "Current branch differs from intended branch; do not edit until branch/worktree is reconciled."
        )
        return VERDICT_BRANCH_MISMATCH, ROUTE_ASK_USER, tuple(warnings), tuple(stop_conditions)
    if not worktree_matches_expected:
        stop_conditions.append(
            "Current worktree differs from expected worktree; do not edit until worktree routing is reconciled."
        )
        return VERDICT_WORKTREE_MISMATCH, ROUTE_ASK_USER, tuple(warnings), tuple(stop_conditions)
    if issue.state.upper() == "CLOSED":
        stop_conditions.append(
            "Source issue is closed; continue only with an explicit reentry or reconciliation reason."
        )
        return VERDICT_CLOSED_ISSUE_REENTRY, ROUTE_ASK_USER, tuple(warnings), tuple(stop_conditions)
    if issue.state == "unknown" and issue.number is not None:
        warnings.append("GitHub issue state is unknown; live verification or user confirmation may be needed.")
        stop_conditions.append(
            "GitHub issue state is unknown; do not route implementation/submission work without confirmation."
        )
        return VERDICT_GITHUB_STATE_UNKNOWN, ROUTE_ASK_USER, tuple(warnings), tuple(stop_conditions)
    if any(artifact.status == "missing_expected_artifact" for artifact in artifacts):
        stop_conditions.append("Expected source or target artifact is missing.")
        return VERDICT_ARTIFACT_MISSING, ROUTE_CODEX_B, tuple(warnings), tuple(stop_conditions)
    if any(artifact.status == "untracked_candidate_artifact" for artifact in artifacts):
        warnings.append("One or more workflow artifacts are untracked candidate artifacts.")
        return VERDICT_ARTIFACT_UNTRACKED, ROUTE_CODEX_C, tuple(warnings), tuple(stop_conditions)
    if dirty_paths or untracked_paths:
        warnings.append(
            "Local checkout has dirty or untracked paths that need classification before staging or submission."
        )
        return VERDICT_FRESH_WITH_WARNINGS, ROUTE_CONTINUE_CURRENT_ROLE, tuple(warnings), tuple(stop_conditions)
    return VERDICT_FRESH, ROUTE_CONTINUE_CURRENT_ROLE, tuple(warnings), tuple(stop_conditions)


def run_check(
    repo_root: str | Path = ".",
    *,
    issue: int | None = None,
    tracker: int | None = None,
    source_artifact: str = "",
    target_artifact: str = "",
    expected_branch: str = "",
    expected_worktree: str = "",
    include_worktrees: bool = True,
    no_gh: bool = False,
) -> FreshnessReport:
    root = Path(repo_root).resolve()
    branch = _branch_report(root, expected_branch)
    dirty_paths, untracked_paths = _dirty_state(root)
    issue_report = _load_issue(issue, root, no_gh=no_gh)
    tracker_report = (
        _load_issue(tracker, root, no_gh=no_gh)
        if tracker is not None
        else IssueReport(None, "not_requested", "", "", "")
    )
    artifacts = tuple(
        report
        for report in (
            _artifact_report(root, source_artifact),
            _artifact_report(root, target_artifact),
        )
        if report.status != "not_requested"
    )
    worktrees = _worktree_reports(root, issue, issue_report.state, include_worktrees)
    result, route, warnings, stop_conditions = _choose_result(
        branch,
        issue_report,
        artifacts,
        dirty_paths,
        untracked_paths,
        _matches_expected_worktree(root, expected_worktree),
    )
    return FreshnessReport(
        result=result,
        recommended_route=route,
        verified_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
        branch=branch,
        issue=issue_report,
        tracker=tracker_report,
        artifacts=artifacts,
        worktrees=worktrees,
        dirty_paths=dirty_paths,
        untracked_artifacts=untracked_paths,
        warnings=warnings,
        stop_conditions=stop_conditions,
    )


def render_json(report: FreshnessReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True)


def _ahead_behind_text(branch: BranchReport) -> str:
    if branch.ahead is None or branch.behind is None:
        return "unknown"
    return f"{branch.ahead} {branch.behind}"


def render_text(report: FreshnessReport) -> str:
    lines = [
        "Workflow Freshness Guard",
        f"result: {report.result}",
        f"recommended_route: {report.recommended_route}",
        f"verified_at: {report.verified_at}",
        "",
        "Branch",
        f"  current: {report.branch.current}",
        f"  intended: {report.branch.intended}",
        f"  upstream: {report.branch.upstream or 'unknown'}",
        f"  ahead_behind: {_ahead_behind_text(report.branch)}",
        "",
        "Issue",
        f"  number: {report.issue.number if report.issue.number is not None else 'not_requested'}",
        f"  state: {report.issue.state}",
    ]
    if report.issue.error:
        lines.append(f"  error: {report.issue.error}")
    if report.artifacts:
        lines.extend(["", "Artifacts"])
        for artifact in report.artifacts:
            lines.append(f"  - {artifact.path}: {artifact.status} -> {artifact.recommended_route}")
    if report.dirty_paths or report.untracked_artifacts:
        lines.extend(["", "Local State"])
        for path in report.dirty_paths:
            lines.append(f"  dirty: {path}")
        for path in report.untracked_artifacts:
            lines.append(f"  untracked: {path}")
    if report.worktrees:
        lines.extend(["", "Worktrees"])
        for worktree in report.worktrees:
            lines.append(f"  - {worktree.branch or 'unknown'}: {worktree.classification} ({worktree.path})")
    if report.warnings:
        lines.extend(["", "Warnings"])
        lines.extend(f"  - {warning}" for warning in report.warnings)
    if report.stop_conditions:
        lines.extend(["", "Stop Conditions"])
        lines.extend(f"  - {condition}" for condition in report.stop_conditions)
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report Mythic Edge workflow freshness without mutating state.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument("--issue", type=int, help="Source issue number.")
    parser.add_argument("--parent-issue", type=int, help="Parent issue number. Recorded as context only.")
    parser.add_argument("--tracker", type=int, help="Tracker issue number.")
    parser.add_argument("--source-artifact", default="", help="Expected source artifact path.")
    parser.add_argument("--target-artifact", default="", help="Expected target artifact path.")
    parser.add_argument("--expected-branch", "--branch", dest="expected_branch", default="", help="Intended branch.")
    parser.add_argument("--expected-worktree", default="", help="Expected current worktree path or directory name.")
    parser.add_argument("--include-worktrees", action="store_true", help="Include git worktree list classification.")
    parser.add_argument("--no-gh", action="store_true", help="Do not call GitHub CLI; report issue state as unknown.")
    parser.add_argument("--json", action="store_true", help="Emit deterministic JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    report = run_check(
        args.repo_root,
        issue=args.issue,
        tracker=args.tracker or args.parent_issue,
        source_artifact=args.source_artifact,
        target_artifact=args.target_artifact,
        expected_branch=args.expected_branch,
        expected_worktree=args.expected_worktree,
        include_worktrees=args.include_worktrees,
        no_gh=args.no_gh,
    )
    output = render_json(report) if args.json else render_text(report)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
