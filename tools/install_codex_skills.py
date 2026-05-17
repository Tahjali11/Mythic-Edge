from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MANIFEST_RELATIVE_PATH = Path("docs") / "codex_skills" / "manifest.json"


@dataclass(frozen=True)
class SkillEntry:
    name: str
    path: Path


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def default_skills_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def load_manifest(repo_root: Path) -> dict[str, Any]:
    manifest_path = repo_root / MANIFEST_RELATIVE_PATH
    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("object") != "mythic_edge_codex_skill_bundle":
        raise ValueError(f"Unexpected manifest object in {manifest_path}")
    return manifest


def skill_entries(repo_root: Path) -> dict[str, SkillEntry]:
    manifest = load_manifest(repo_root)
    entries: dict[str, SkillEntry] = {}
    for raw_entry in manifest.get("included_skills", []):
        name = str(raw_entry.get("name", "")).strip()
        relative_path = Path(str(raw_entry.get("path", "")).strip())
        if not name or not relative_path.parts:
            raise ValueError("Skill manifest contains an incomplete entry")
        if any(part in {"..", ""} for part in relative_path.parts):
            raise ValueError(f"Unsafe skill path for {name}: {relative_path}")
        source_path = repo_root / relative_path
        skill_file = source_path / "SKILL.md"
        if not skill_file.exists():
            raise FileNotFoundError(f"Missing SKILL.md for {name}: {skill_file}")
        entries[name] = SkillEntry(name=name, path=source_path)
    return entries


def selected_entries(entries: dict[str, SkillEntry], names: list[str], install_all: bool) -> list[SkillEntry]:
    if install_all:
        return [entries[name] for name in sorted(entries)]
    if not names:
        raise ValueError("Choose --all, --list, or one or more --skill values")
    missing = sorted(set(names) - set(entries))
    if missing:
        known = ", ".join(sorted(entries))
        raise ValueError(f"Unknown skill(s): {', '.join(missing)}. Known skills: {known}")
    return [entries[name] for name in names]


def copy_skill(entry: SkillEntry, destination_root: Path, *, mode: str, dry_run: bool) -> Path:
    destination = destination_root / entry.name
    if dry_run:
        return destination

    destination_root.mkdir(parents=True, exist_ok=True)
    if mode == "exact" and destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(entry.path, destination, dirs_exist_ok=(mode == "merge"))
    return destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install repo-owned Codex skills for Mythic Edge.")
    parser.add_argument("--repo-root", default=None, help="Repo root. Defaults to this script's repo.")
    parser.add_argument(
        "--destination",
        default=None,
        help="Skills destination. Defaults to CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Skill name to install. May be supplied more than once.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Install all repo-owned skills in docs/codex_skills/manifest.json.",
    )
    parser.add_argument("--list", action="store_true", help="List bundled skills and exit.")
    parser.add_argument(
        "--mode",
        choices=("exact", "merge"),
        default="exact",
        help="exact replaces the destination skill directory; merge overlays files.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be installed without copying files.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else repo_root_from_script()
    destination_root = (
        Path(args.destination).expanduser().resolve() if args.destination else default_skills_destination()
    )
    entries = skill_entries(repo_root)

    if args.list:
        for name in sorted(entries):
            print(name)
        return 0

    to_install = selected_entries(entries, args.skill, bool(args.all))
    action = "Would install" if args.dry_run else "Installed"
    for entry in to_install:
        destination = copy_skill(entry, destination_root, mode=args.mode, dry_run=bool(args.dry_run))
        print(f"{action} {entry.name} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
