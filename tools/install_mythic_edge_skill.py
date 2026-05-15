"""Install repo-owned Mythic Edge Codex skills into the local Codex skills folder."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

DEFAULT_SKILL_NAME = "mythic-edge-workflow"


def default_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured)
    return Path.home() / ".codex"


def available_skills(repo_root: Path) -> tuple[str, ...]:
    skills_root = repo_root / "docs" / "codex_skills"
    if not skills_root.exists():
        return ()
    return tuple(sorted(path.name for path in skills_root.iterdir() if path.joinpath("SKILL.md").exists()))


def install_skill(repo_root: Path, *, skill_name: str = DEFAULT_SKILL_NAME, codex_home: Path | None = None) -> Path:
    source = repo_root / "docs" / "codex_skills" / skill_name
    if not source.exists():
        raise FileNotFoundError(source)
    target_root = (codex_home or default_codex_home()) / "skills"
    target = target_root / skill_name
    target_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, dirs_exist_ok=True)
    return target


def install_all_skills(repo_root: Path, *, codex_home: Path | None = None) -> tuple[Path, ...]:
    skill_names = available_skills(repo_root)
    if not skill_names:
        raise FileNotFoundError(repo_root / "docs" / "codex_skills")
    return tuple(install_skill(repo_root, skill_name=skill_name, codex_home=codex_home) for skill_name in skill_names)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install repo-owned Mythic Edge Codex skills.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--codex-home", default="", help="Override CODEX_HOME for testing or custom installs.")
    parser.add_argument("--skill", default=DEFAULT_SKILL_NAME, help="Skill folder name to install.")
    parser.add_argument("--all", action="store_true", help="Install every skill under docs/codex_skills.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    codex_home = Path(args.codex_home).resolve() if args.codex_home else None
    try:
        targets = install_all_skills(repo_root, codex_home=codex_home) if args.all else (
            install_skill(repo_root, skill_name=args.skill, codex_home=codex_home),
        )
    except OSError as exc:
        print(f"Mythic Edge Skill Install\nerror: {exc}\nresult: error")
        return 2

    print("Mythic Edge Skill Install")
    for target in targets:
        print(f"installed: {target}")
    print("result: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
