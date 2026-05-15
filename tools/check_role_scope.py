"""Check changed paths against the active Mythic Edge Codex role."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

STRICT_ROLE_ALLOWED_GLOBS = {
    "A": ("docs/problem_representations/**",),
    "B": ("docs/contracts/**",),
    "E": ("docs/contract_test_reports/**",),
    "CONTRACT_TEST": ("docs/contract_test_reports/**",),
    "G": (),
    "H": (
        "docs/problem_representations/agent_constitution*.md",
        "docs/contracts/agent_constitution*.md",
        "docs/templates/constitution_feedback_packet.md",
    ),
}

ROLE_DESCRIPTIONS = {
    "A": "Thinker should produce issue/problem-framing artifacts only.",
    "B": "Module Contract Writer should produce contract artifacts only.",
    "C": "Module Implementer may change scoped implementation, tests, and handoff artifacts.",
    "D": "Module Fixer may change targeted implementation, tests, and handoff artifacts.",
    "E": "Module Reviewer should report findings without mutating implementation.",
    "F": "Module Submitter stages reviewed files; use protected-surface and secret gates for actual diff safety.",
    "G": "Integration Deployer should not make local edits except explicit narrow integration fix work.",
    "H": "Constitutional Lawyer should produce synthesis/proposal artifacts without mutating authority docs.",
    "CONTRACT_TEST": "Contract-test reviewer should report mismatches without mutating implementation.",
}

ALWAYS_FORBIDDEN_GLOBS = (
    "data/match_logs/**",
    "data/runtime_logs/**",
    "data/status/**",
    "data/failed_posts/**",
    "data/bad_events/**",
    "data/oracle_data/**",
    "data/decklists/**",
    "workbook_exports/**",
    "exports/workbook/**",
    "_review_*/**",
    ".github/Mythic-Edge/**",
)


@dataclass(frozen=True)
class Finding:
    severity: str
    path: str
    message: str


def normalize_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    return text.lstrip("/")


def _matches(path: str, pattern: str) -> bool:
    pattern = normalize_path(pattern)
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(f"{prefix}/") or fnmatch.fnmatchcase(path, pattern)
    return fnmatch.fnmatchcase(path, pattern)


def collect_changed_paths(base: str, *, repo_root: Path) -> tuple[str, ...]:
    completed = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base}...HEAD"],
        cwd=repo_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"git diff failed for base {base}")
    return tuple(normalize_path(path) for path in completed.stdout.splitlines() if path.strip())


def _is_allowed(path: str, allowed_globs: tuple[str, ...]) -> bool:
    return any(_matches(path, pattern) for pattern in allowed_globs)


def check_role_scope(role: str, paths: tuple[str, ...], *, extra_allowed: tuple[str, ...] = ()) -> list[Finding]:
    normalized_role = role.upper().replace("-", "_")
    normalized_paths = tuple(normalize_path(path) for path in paths)
    findings: list[Finding] = []

    for path in normalized_paths:
        if _is_allowed(path, ALWAYS_FORBIDDEN_GLOBS):
            findings.append(Finding("error", path, "Local, generated, ignored, or private artifact is never in scope."))

    strict_allowed = STRICT_ROLE_ALLOWED_GLOBS.get(normalized_role)
    if strict_allowed is None:
        return findings

    allowed_globs = (*strict_allowed, *extra_allowed)
    for path in normalized_paths:
        if not _is_allowed(path, allowed_globs):
            findings.append(
                Finding(
                    "error",
                    path,
                    f"Path is outside role {normalized_role} scope. {ROLE_DESCRIPTIONS[normalized_role]}",
                ),
            )
    return findings


def render_report(role: str, paths: tuple[str, ...], findings: list[Finding]) -> str:
    normalized_role = role.upper().replace("-", "_")
    lines = [
        "Role Scope Check",
        f"role: {normalized_role}",
        f"changed_paths: {len(paths)}",
        f"findings: {len(findings)}",
    ]
    for finding in findings:
        lines.append(f"{finding.severity.upper()} {finding.path} - {finding.message}")
    lines.append("result: failed" if findings else "result: passed")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check changed paths against a Codex workflow role.")
    parser.add_argument("--role", required=True, help="Workflow role: A, B, C, D, E, F, G, or contract-test.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--base", default="origin/main", help="Base ref used when --changed is set.")
    parser.add_argument("--changed", action="store_true", help="Use git diff to collect changed paths.")
    parser.add_argument("--paths-from-stdin", action="store_true", help="Read paths from stdin.")
    parser.add_argument("--paths", nargs="*", default=(), help="Explicit changed paths.")
    parser.add_argument("--allow", nargs="*", default=(), help="Extra allowed glob patterns for this invocation.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    try:
        if args.paths_from_stdin:
            paths = tuple(line.strip() for line in sys.stdin if line.strip())
        elif args.changed:
            paths = collect_changed_paths(args.base, repo_root=repo_root)
        else:
            paths = tuple(args.paths)
        normalized_paths = tuple(normalize_path(path) for path in paths)
        findings = check_role_scope(args.role, normalized_paths, extra_allowed=tuple(args.allow))
    except RuntimeError as exc:
        print(f"Role Scope Check\nerror: {exc}\nresult: error")
        return 2

    print(render_report(args.role, normalized_paths, findings))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
