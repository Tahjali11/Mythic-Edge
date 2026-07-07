"""Git collection and CLI orchestration for the protected-surface gate."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from tools.check_protected_surfaces_classification import evaluate_paths
    from tools.check_protected_surfaces_models import GateResult
    from tools.check_protected_surfaces_report import render_report
except ModuleNotFoundError:  # pragma: no cover - script-local import fallback.
    from check_protected_surfaces_classification import evaluate_paths
    from check_protected_surfaces_models import GateResult
    from check_protected_surfaces_report import render_report


def collect_changed_paths(base: str, *, repo_root: str | Path = ".") -> tuple[str, ...]:
    command = [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        f"{base}...HEAD",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(str(exc)) from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(
            detail or f"git diff failed with exit code {completed.returncode}"
        )
    return tuple(line for line in completed.stdout.splitlines() if line.strip())


def run_gate(base: str, *, repo_root: str | Path = ".") -> GateResult:
    try:
        changed_paths = collect_changed_paths(base, repo_root=repo_root)
    except RuntimeError as exc:
        return evaluate_paths((), base=base, error=str(exc))
    return evaluate_paths(changed_paths, base=base)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check protected-surface file diffs.")
    parser.add_argument("--base", required=True, help="Base git ref for <base>...HEAD.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--paths-from-stdin",
        action="store_true",
        help="Read newline-delimited paths from stdin instead of running git diff.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    if args.paths_from_stdin:
        result = evaluate_paths(sys.stdin.read().splitlines(), base=args.base)
    else:
        result = run_gate(args.base, repo_root=args.repo_root)

    output = render_report(result)
    stream = sys.stderr if result.error else sys.stdout
    print(output, file=stream)
    return result.exit_code
