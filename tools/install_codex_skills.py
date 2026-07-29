from __future__ import annotations

import argparse
import os
import shutil
import stat
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

PACKAGE_NAME = "mythic-edge-repo-owned-codex-skills"
SKILL_SOURCE_ROOT = Path("docs/codex_skills")
SKILL_NAME_PREFIX = "name:"
TRUSTED_WINDOWS_SKILL_NAME = "mythic-edge-role-pool"

EXIT_SUCCESS = 0
EXIT_USAGE_ERROR = 1
EXIT_SOURCE_MISSING = 2
EXIT_TARGET_DIFFERS = 3
EXIT_UNSAFE_PATH = 4
EXIT_INSTALL_FAILURE = 5
UNSAFE_TARGET_REASONS = {
    "target_reparse_point",
    "target_symlink_escape",
}


@dataclass(frozen=True)
class SkillSource:
    name: str
    source_dir: Path
    unsafe_reason: str | None = None


@dataclass(frozen=True)
class DiscoveryResult:
    source_root: Path
    skills: tuple[SkillSource, ...]
    missing: bool = False
    unsafe_reason: str | None = None


@dataclass(frozen=True)
class InstallAction:
    skill_name: str
    action: str
    source_dir: Path
    target_dir: Path
    reason: str


class SkillInstallArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE_ERROR, f"{self.prog}: error: {message}\n")


def discover_skills(repo_root: Path) -> DiscoveryResult:
    source_root = repo_root.resolve() / SKILL_SOURCE_ROOT
    if not source_root.exists() or not source_root.is_dir():
        return DiscoveryResult(source_root=source_root, skills=(), missing=True)
    if source_root.is_symlink() or _is_reparse_point(source_root):
        return DiscoveryResult(
            source_root=source_root,
            skills=(),
            unsafe_reason="source_reparse_point",
        )

    skills: list[SkillSource] = []
    for child in sorted(source_root.iterdir(), key=lambda path: path.name):
        if child.name.startswith(".") or not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.exists() or not skill_md.is_file():
            continue
        unsafe_reason = _source_tree_unsafe_reason(child, source_root)
        name = child.name if unsafe_reason else _read_skill_name(skill_md)
        if unsafe_reason is None and name != child.name:
            unsafe_reason = "skill_name_mismatch"
        skills.append(SkillSource(name=name, source_dir=child, unsafe_reason=unsafe_reason))
    return DiscoveryResult(source_root=source_root, skills=tuple(skills))


def build_parser() -> argparse.ArgumentParser:
    parser = SkillInstallArgumentParser(
        description="Install Mythic Edge repo-owned Codex skills for the local user.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true", help="List installable skills.")
    mode.add_argument("--all", action="store_true", help="Install or dry-run all skills.")
    mode.add_argument("--skill", help="Install or dry-run one skill by name.")
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument(
        "--check",
        action="store_true",
        help="Check one source and installed skill without writing.",
    )
    operation.add_argument(
        "--sync",
        action="store_true",
        help="Synchronize one reviewed existing skill using staging and rollback.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions only.")
    parser.add_argument("--repo-root", type=Path, default=_default_repo_root())
    parser.add_argument("--codex-home", type=Path, default=None)
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if (args.check or args.sync) and args.skill is None:
        parser.error("--check and --sync require --skill")
    if (args.check or args.sync) and args.dry_run:
        parser.error("--check and --sync cannot be combined with --dry-run")
    result = execute(args)
    for line in result[1]:
        print(line)
    return result[0]


def execute(args: argparse.Namespace) -> tuple[int, list[str]]:
    repo_root = args.repo_root.resolve()
    codex_home = _codex_home(args.codex_home)
    target_root = codex_home / "skills"
    discovery = discover_skills(repo_root)
    lines = [
        f"package: {PACKAGE_NAME}",
        f"mode: {_mode_label(args)}",
        f"source_repo_root: {repo_root}",
        f"target_codex_home: {codex_home}",
        f"target_skills_root: {target_root}",
    ]
    if discovery.missing:
        result = "missing" if args.check else "failed"
        return (
            EXIT_SOURCE_MISSING,
            lines
            + [
                f"result: {result}",
                "reason: source_package_missing",
            ],
        )
    if discovery.unsafe_reason is not None:
        result = "unsafe" if args.check else "failed"
        return (
            EXIT_UNSAFE_PATH,
            lines
            + [
                f"result: {result}",
                f"reason: {discovery.unsafe_reason}",
            ],
        )
    if any(skill.unsafe_reason for skill in discovery.skills):
        lines.extend(_skill_lines(discovery.skills, target_root, unsafe_only=True))
        result = "unsafe" if args.check else "failed"
        return (
            EXIT_UNSAFE_PATH,
            lines
            + [
                f"result: {result}",
                "reason: unsafe_source_skill",
            ],
        )
    if args.list:
        return (
            EXIT_SUCCESS,
            lines + _skill_lines(discovery.skills, target_root) + ["result: passed"],
        )

    selected = _selected_skills(discovery.skills, args)
    if not selected:
        result = "missing" if args.check else "failed"
        return (
            EXIT_SOURCE_MISSING,
            lines
            + [
                f"skill {args.skill}: action=missing",
                f"result: {result}",
                "reason: selected_skill_missing",
            ],
        )

    target_root_unsafe_reason = _target_root_unsafe_reason(target_root, codex_home)
    if target_root_unsafe_reason is not None:
        result = "unsafe" if args.check else "failed"
        return (
            EXIT_UNSAFE_PATH,
            lines
            + [
                f"result: {result}",
                f"reason: {target_root_unsafe_reason}",
            ],
        )

    actions = [_plan_action(skill, target_root) for skill in selected]
    if args.check:
        return _check_actions(lines, actions)
    if args.sync:
        return _sync_action(lines, actions[0])
    if args.dry_run:
        dry_run_lines = [
            _format_action(
                InstallAction(
                    skill_name=action.skill_name,
                    action=_dry_run_action(action.action),
                    source_dir=action.source_dir,
                    target_dir=action.target_dir,
                    reason=action.reason,
                )
            )
            for action in actions
        ]
        exit_code = _refusal_exit_code(actions)
        result = "refused" if exit_code != EXIT_SUCCESS else "passed"
        return exit_code, lines + dry_run_lines + [f"result: {result}"]

    role_pool_installs = [
        action
        for action in actions
        if action.skill_name == TRUSTED_WINDOWS_SKILL_NAME
        and action.action == "install"
    ]
    role_pool_preflight_reason = (
        _role_pool_mutation_preflight_failure_reason()
        if role_pool_installs
        else None
    )
    if role_pool_preflight_reason is not None:
        return (
            EXIT_INSTALL_FAILURE,
            lines
            + [
                _format_action(_replace_action(action, "refused"))
                for action in actions
            ]
            + ["result: refused", f"reason: {role_pool_preflight_reason}"],
        )

    unsafe_exit_code = _unsafe_refusal_exit_code(actions)
    if unsafe_exit_code is not None:
        return (
            unsafe_exit_code,
            lines + [_format_action(action) for action in actions] + ["result: refused"],
        )

    installed_lines: list[str] = []
    for action in actions:
        if action.action == "install":
            try:
                action.target_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(action.source_dir, action.target_dir)
                installed_lines.append(_format_action(_replace_action(action, "installed")))
            except OSError:
                installed_lines.append(_format_action(_replace_action(action, "failed")))
                return EXIT_INSTALL_FAILURE, lines + installed_lines + ["result: failed"]
        else:
            installed_lines.append(_format_action(action))
    if any(action.action == "refused" for action in actions):
        return _refusal_exit_code(actions), lines + installed_lines + ["result: refused"]
    return EXIT_SUCCESS, lines + installed_lines + ["result: passed"]


def _selected_skills(
    skills: Sequence[SkillSource],
    args: argparse.Namespace,
) -> tuple[SkillSource, ...]:
    if args.all:
        return tuple(skills)
    return tuple(skill for skill in skills if skill.name == args.skill)


def _plan_action(skill: SkillSource, target_root: Path) -> InstallAction:
    target_dir = target_root / skill.name
    target_unsafe_reason = _target_tree_unsafe_reason(target_dir, target_root)
    if target_unsafe_reason is not None:
        return InstallAction(
            skill.name,
            "refused",
            skill.source_dir,
            target_dir,
            target_unsafe_reason,
        )
    if not target_dir.exists():
        return InstallAction(skill.name, "install", skill.source_dir, target_dir, "target_missing")
    if not target_dir.is_dir():
        return InstallAction(skill.name, "refused", skill.source_dir, target_dir, "target_not_dir")
    if _directories_match(skill.source_dir, target_dir):
        return InstallAction(skill.name, "unchanged", skill.source_dir, target_dir, "identical")
    return InstallAction(skill.name, "refused", skill.source_dir, target_dir, "target_differs")


def _check_actions(
    prefix_lines: list[str],
    actions: Sequence[InstallAction],
) -> tuple[int, list[str]]:
    status_by_action = {
        "install": ("missing", EXIT_SOURCE_MISSING),
        "unchanged": ("identical", EXIT_SUCCESS),
    }
    statuses: list[str] = []
    exit_code = EXIT_SUCCESS
    for action in actions:
        if action.action in status_by_action:
            status, action_exit_code = status_by_action[action.action]
        elif action.reason in UNSAFE_TARGET_REASONS or action.reason == "target_not_dir":
            status, action_exit_code = "unsafe", EXIT_UNSAFE_PATH
        else:
            status, action_exit_code = "drift", EXIT_TARGET_DIFFERS
        statuses.append(status)
        exit_code = max(exit_code, action_exit_code)
    result = statuses[0] if len(statuses) == 1 else (
        "identical" if all(status == "identical" for status in statuses) else "drift"
    )
    return (
        exit_code,
        prefix_lines
        + [_format_action(action) for action in actions]
        + [f"result: {result}"],
    )


def _sync_action(
    prefix_lines: list[str],
    action: InstallAction,
) -> tuple[int, list[str]]:
    if action.action == "unchanged":
        return (
            EXIT_SUCCESS,
            prefix_lines + [_format_action(action), "result: identical"],
        )
    if action.action == "install":
        refusal = _replace_action(action, "refused")
        return (
            EXIT_SOURCE_MISSING,
            prefix_lines
            + [_format_action(refusal), "result: refused", "reason: target_missing"],
        )
    if action.reason != "target_differs":
        exit_code = (
            EXIT_UNSAFE_PATH
            if action.reason in UNSAFE_TARGET_REASONS
            or action.reason == "target_not_dir"
            else EXIT_TARGET_DIFFERS
        )
        return (
            exit_code,
            prefix_lines + [_format_action(action), "result: refused"],
        )
    role_pool_preflight_reason = (
        _role_pool_mutation_preflight_failure_reason()
        if action.skill_name == TRUSTED_WINDOWS_SKILL_NAME
        else None
    )
    if role_pool_preflight_reason is not None:
        refused = _replace_action(action, "refused")
        return (
            EXIT_INSTALL_FAILURE,
            prefix_lines
            + [
                _format_action(refused),
                "result: refused",
                f"reason: {role_pool_preflight_reason}",
            ],
        )
    if _synchronize_existing_skill(action.source_dir, action.target_dir):
        synchronized = _replace_action(action, "synchronized")
        return (
            EXIT_SUCCESS,
            prefix_lines + [_format_action(synchronized), "result: passed"],
        )
    failed = _replace_action(action, "failed")
    return (
        EXIT_INSTALL_FAILURE,
        prefix_lines + [_format_action(failed), "result: failed"],
    )


def _synchronize_existing_skill(source_dir: Path, target_dir: Path) -> bool:
    target_root = target_dir.parent
    if (
        (
            target_dir.name == TRUSTED_WINDOWS_SKILL_NAME
            and _role_pool_mutation_preflight_failure_reason() is not None
        )
        or
        not target_dir.exists()
        or not target_dir.is_dir()
        or _source_tree_unsafe_reason(source_dir, source_dir.parent) is not None
        or _target_tree_unsafe_reason(target_dir, target_root) is not None
    ):
        return False

    original_snapshot = _tree_snapshot(target_dir)
    if original_snapshot is None:
        return False
    staging_dir = Path(
        tempfile.mkdtemp(
            prefix=f".{target_dir.name}.sync-",
            dir=target_root,
        )
    )
    backup_dir = target_root / f".{target_dir.name}.backup-{uuid.uuid4().hex}"
    target_moved = False
    replacement_moved = False
    replacement_validated = False
    try:
        shutil.copytree(source_dir, staging_dir, dirs_exist_ok=True)
        if (
            _target_tree_unsafe_reason(staging_dir, target_root) is not None
            or not _directories_match(source_dir, staging_dir)
        ):
            return False
        os.replace(target_dir, backup_dir)
        target_moved = True
        os.replace(staging_dir, target_dir)
        replacement_moved = True
        if (
            _target_tree_unsafe_reason(target_dir, target_root) is not None
            or not _directories_match(source_dir, target_dir)
        ):
            raise OSError("synchronized tree failed final validation")
        replacement_validated = True
        shutil.rmtree(backup_dir)
        target_moved = False
        return True
    except OSError:
        if replacement_validated:
            return False
        if replacement_moved and target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        if target_moved and backup_dir.exists() and not target_dir.exists():
            try:
                os.replace(backup_dir, target_dir)
                target_moved = False
            except OSError:
                return False
        if _tree_snapshot(target_dir) != original_snapshot:
            return False
        return False
    finally:
        if staging_dir.exists():
            shutil.rmtree(staging_dir, ignore_errors=True)
        if backup_dir.exists() and not target_moved:
            shutil.rmtree(backup_dir, ignore_errors=True)


def _dry_run_action(action: str) -> str:
    if action == "install":
        return "would_install"
    if action == "refused":
        return "refused"
    return action


def _trusted_windows_host_observed() -> bool:
    return os.name == "nt" and sys.platform == "win32"


def _exact_native_task_capability_observed() -> bool:
    # No exact production capability evidence is currently bound.
    return False


def _role_pool_mutation_preflight_failure_reason() -> str | None:
    if not _trusted_windows_host_observed():
        return "unsupported_execution_host"
    if not _exact_native_task_capability_observed():
        return "native_task_capability_unavailable"
    return None


def _replace_action(action: InstallAction, new_action: str) -> InstallAction:
    return InstallAction(
        skill_name=action.skill_name,
        action=new_action,
        source_dir=action.source_dir,
        target_dir=action.target_dir,
        reason=action.reason,
    )


def _refusal_exit_code(actions: Sequence[InstallAction]) -> int:
    unsafe_exit_code = _unsafe_refusal_exit_code(actions)
    if unsafe_exit_code is not None:
        return unsafe_exit_code
    if any(action.action == "refused" for action in actions):
        return EXIT_TARGET_DIFFERS
    return EXIT_SUCCESS


def _unsafe_refusal_exit_code(actions: Sequence[InstallAction]) -> int | None:
    if any(
        action.action == "refused" and action.reason in UNSAFE_TARGET_REASONS
        for action in actions
    ):
        return EXIT_UNSAFE_PATH
    return None


def _skill_lines(
    skills: Sequence[SkillSource],
    target_root: Path,
    *,
    unsafe_only: bool = False,
) -> list[str]:
    lines: list[str] = []
    for skill in skills:
        if unsafe_only and skill.unsafe_reason is None:
            continue
        action = "unsafe" if skill.unsafe_reason else "available"
        reason = f" reason={skill.unsafe_reason}" if skill.unsafe_reason else ""
        lines.append(
            f"skill {skill.name}: action={action} "
            f"source={skill.source_dir} target={target_root / skill.name}{reason}"
        )
    return lines


def _format_action(action: InstallAction) -> str:
    return (
        f"skill {action.skill_name}: action={action.action} "
        f"source={action.source_dir} target={action.target_dir} reason={action.reason}"
    )


def _source_tree_unsafe_reason(source_dir: Path, source_root: Path) -> str | None:
    if source_dir.is_symlink():
        return "source_symlink_escape"
    if _is_reparse_point(source_dir):
        return "source_reparse_point"
    if not _path_inside(source_dir.resolve(), source_root):
        return "source_symlink_escape"
    if _tree_contains_reparse_point(source_dir):
        return "source_reparse_point"
    return None


def _path_inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _target_root_unsafe_reason(target_root: Path, codex_home: Path) -> str | None:
    if target_root.is_symlink():
        return "target_symlink_escape"
    if target_root.exists() and _is_reparse_point(target_root):
        return "target_reparse_point"
    if target_root.exists() and not _path_inside(target_root.resolve(), codex_home):
        return "target_symlink_escape"
    return None


def _target_tree_unsafe_reason(target_dir: Path, target_root: Path) -> str | None:
    if target_dir.is_symlink():
        return "target_symlink_escape"
    if target_dir.exists() and _is_reparse_point(target_dir):
        return "target_reparse_point"
    if not target_dir.exists():
        return None
    if not _path_inside(target_dir.resolve(), target_root):
        return "target_symlink_escape"
    if _tree_contains_reparse_point(target_dir):
        return "target_reparse_point"
    return None


def _is_reparse_point(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    attributes = getattr(info, "st_file_attributes", 0)
    marker = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attributes & marker)


def _tree_contains_reparse_point(root: Path) -> bool:
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            entries = list(os.scandir(directory))
        except OSError:
            return True
        for entry in entries:
            try:
                info = entry.stat(follow_symlinks=False)
            except OSError:
                return True
            attributes = getattr(info, "st_file_attributes", 0)
            marker = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
            if entry.is_symlink() or attributes & marker:
                return True
            if stat.S_ISDIR(info.st_mode):
                pending.append(Path(entry.path))
    return False


def _read_skill_name(skill_md: Path) -> str:
    for line in skill_md.read_text(encoding="utf-8").splitlines()[:20]:
        stripped = line.strip()
        if stripped.startswith(SKILL_NAME_PREFIX):
            return stripped.removeprefix(SKILL_NAME_PREFIX).strip().strip('"').strip("'")
    return skill_md.parent.name


def _directories_match(source_dir: Path, target_dir: Path) -> bool:
    source_paths = _relative_paths(source_dir)
    target_paths = _relative_paths(target_dir)
    if source_paths != target_paths:
        return False
    for relative_path in sorted(source_paths):
        source_path = source_dir / relative_path
        target_path = target_dir / relative_path
        if source_path.is_dir() and target_path.is_dir():
            continue
        if source_path.is_file() and target_path.is_file():
            if not _files_match_bytes(source_path, target_path):
                return False
            continue
        return False
    return True


def _tree_snapshot(root: Path) -> tuple[tuple[str, str, bytes], ...] | None:
    if not root.exists() or not root.is_dir() or _tree_contains_reparse_point(root):
        return None
    rows: list[tuple[str, str, bytes]] = []
    try:
        for path in sorted(
            root.rglob("*"),
            key=lambda item: item.relative_to(root).as_posix(),
        ):
            relative = path.relative_to(root).as_posix()
            if path.is_dir():
                rows.append((relative, "directory", b""))
            elif path.is_file():
                rows.append((relative, "file", path.read_bytes()))
            else:
                return None
    except OSError:
        return None
    return tuple(rows)


def _relative_paths(root: Path) -> set[Path]:
    return {path.relative_to(root) for path in root.rglob("*")}


def _files_match_bytes(source_file: Path, target_file: Path) -> bool:
    with source_file.open("rb") as source, target_file.open("rb") as target:
        while True:
            source_chunk = source.read(1024 * 1024)
            target_chunk = target.read(1024 * 1024)
            if source_chunk != target_chunk:
                return False
            if not source_chunk:
                return True


def _mode_label(args: argparse.Namespace) -> str:
    if args.list:
        return "list"
    if args.check:
        return "check"
    if args.sync:
        return "sync"
    if args.dry_run:
        return "dry-run"
    return "install"


def _codex_home(arg_value: Path | None) -> Path:
    if arg_value is not None:
        return arg_value.expanduser().resolve()
    env_value = os.environ.get("CODEX_HOME")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
