"""Report local Mythic Edge artifacts required by a workflow profile."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ArtifactStatus:
    artifact_id: str
    label: str
    path: str
    required: bool
    exists: bool
    env_var: str
    note: str


def _expand_path(template: str | None, *, repo_root: Path) -> str:
    if not template:
        return ""
    home = str(Path.home()).replace("\\", "/")
    userprofile = os.environ.get("USERPROFILE", str(Path.home())).replace("\\", "/")
    expanded = template.format(repo_root=str(repo_root).replace("\\", "/"), home=home, userprofile=userprofile)
    return os.path.expandvars(expanded)


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def inspect_artifacts(manifest: dict[str, Any], *, repo_root: Path, profile: str) -> tuple[ArtifactStatus, ...]:
    profiles = manifest.get("profiles", {})
    if profile not in profiles:
        raise ValueError(f"Unknown profile {profile!r}. Known profiles: {', '.join(sorted(profiles))}")
    required_ids = set(profiles[profile].get("required_artifact_ids", []))
    statuses: list[ArtifactStatus] = []
    for artifact in manifest.get("artifacts", []):
        artifact_id = str(artifact["id"])
        env_var = str(artifact.get("env_var") or "")
        env_value = os.environ.get(env_var) if env_var else None
        path_text = env_value or _expand_path(artifact.get("default_path"), repo_root=repo_root)
        exists = bool(path_text) and Path(path_text).exists()
        statuses.append(
            ArtifactStatus(
                artifact_id=artifact_id,
                label=str(artifact.get("label", artifact_id)),
                path=path_text,
                required=artifact_id in required_ids,
                exists=exists,
                env_var=env_var,
                note=str(artifact.get("notes", "")),
            ),
        )
    return tuple(statuses)


def render_report(profile: str, statuses: tuple[ArtifactStatus, ...]) -> str:
    missing_required = [status for status in statuses if status.required and not status.exists]
    lines = [
        "Local Environment Check",
        f"profile: {profile}",
        f"artifacts: {len(statuses)}",
        f"missing_required: {len(missing_required)}",
    ]
    for status in statuses:
        state = "present" if status.exists else "missing"
        requirement = "required" if status.required else "optional"
        path = status.path or "<env-only>"
        lines.append(f"{state.upper()} {requirement} {status.artifact_id} - {path}")
        if status.env_var:
            lines.append(f"  env: {status.env_var}")
        if status.note:
            lines.append(f"  note: {status.note}")
    lines.append("result: failed" if missing_required else "result: passed")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report missing local/generated artifacts for a workflow profile.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--manifest", default="docs/local_artifacts_manifest.json", help="Manifest JSON path.")
    parser.add_argument("--profile", default="clean_clone", help="Profile name from the manifest.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    try:
        manifest = load_manifest(repo_root.joinpath(args.manifest))
        statuses = inspect_artifacts(manifest, repo_root=repo_root, profile=args.profile)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Local Environment Check\nerror: {exc}\nresult: error")
        return 2

    print(render_report(args.profile, statuses))
    return 1 if any(status.required and not status.exists for status in statuses) else 0


if __name__ == "__main__":
    sys.exit(main())
