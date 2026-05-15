"""Select focused validation commands for changed Mythic Edge paths."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MatchedSurface:
    surface_id: str
    risk: str
    reason: str
    paths: tuple[str, ...]
    commands: tuple[str, ...]


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


def load_matrix(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_validation(
    matrix: dict[str, Any],
    paths: tuple[str, ...],
    *,
    base: str,
) -> tuple[tuple[str, str], tuple[MatchedSurface, ...]]:
    normalized_paths = tuple(normalize_path(path) for path in paths)
    baseline = tuple(
        (
            str(item["command"]).format(base=base),
            str(item.get("reason", "")),
        )
        for item in matrix.get("baseline_commands", [])
    )
    matched: list[MatchedSurface] = []
    for surface in matrix.get("surfaces", []):
        globs = tuple(str(pattern) for pattern in surface.get("path_globs", []))
        surface_paths = tuple(path for path in normalized_paths if any(_matches(path, pattern) for pattern in globs))
        if not surface_paths:
            continue
        commands = tuple(str(command).format(base=base) for command in surface.get("commands", []))
        matched.append(
            MatchedSurface(
                surface_id=str(surface.get("id", "unknown")),
                risk=str(surface.get("risk", "unknown")),
                reason=str(surface.get("reason", "")),
                paths=surface_paths,
                commands=commands,
            ),
        )
    return baseline, tuple(matched)


def _dedupe_commands(baseline: tuple[tuple[str, str], ...], matched: tuple[MatchedSurface, ...]) -> tuple[str, ...]:
    commands: list[str] = []
    for command, _reason in baseline:
        if command not in commands:
            commands.append(command)
    for surface in matched:
        for command in surface.commands:
            if command not in commands:
                commands.append(command)
    return tuple(commands)


def render_report(
    paths: tuple[str, ...],
    baseline: tuple[tuple[str, str], ...],
    matched: tuple[MatchedSurface, ...],
) -> str:
    lines = ["Validation Selector", f"changed_paths: {len(paths)}", f"matched_surfaces: {len(matched)}"]
    if paths:
        lines.append("")
        lines.append("Changed paths:")
        lines.extend(f"- {path}" for path in paths)
    if matched:
        lines.append("")
        lines.append("Matched surfaces:")
        for surface in matched:
            lines.append(f"- {surface.surface_id} ({surface.risk}): {surface.reason}")
            for path in surface.paths:
                lines.append(f"  path: {path}")
    lines.append("")
    lines.append("Recommended commands:")
    for command in _dedupe_commands(baseline, matched):
        lines.append(f"- {command}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Select validation commands for changed paths.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--matrix", default="docs/validation_matrix.json", help="Validation matrix JSON path.")
    parser.add_argument("--base", default="origin/main", help="Base ref used for changed path detection.")
    parser.add_argument("--changed", action="store_true", help="Use git diff to collect changed paths.")
    parser.add_argument("--paths", nargs="*", default=(), help="Explicit changed paths.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    matrix_path = repo_root.joinpath(args.matrix)
    try:
        paths = collect_changed_paths(args.base, repo_root=repo_root) if args.changed else tuple(args.paths)
        matrix = load_matrix(matrix_path)
        baseline, matched = select_validation(matrix, paths, base=args.base)
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Validation Selector\nerror: {exc}\nresult: error")
        return 2

    print(render_report(tuple(normalize_path(path) for path in paths), baseline, matched))
    return 0


if __name__ == "__main__":
    sys.exit(main())
