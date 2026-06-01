"""Report Mythic Edge local artifact readiness without reading private payloads."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPORT_OBJECT = "mythic_edge_local_environment_report"
REPORT_SCHEMA_VERSION = "local_artifact_manifest_environment_profiles.v1"
MANIFEST_SCHEMA_VERSION = "local_artifacts_manifest.v1"
MANIFEST_OBJECT = "mythic_edge_local_artifacts_manifest"
DEFAULT_MANIFEST = "docs/local_artifacts_manifest.json"
LOCAL_APP_DIR_NAME = "MythicEdgeDev"

SEVERITY_OK = "ok"
SEVERITY_INFO = "info"
SEVERITY_WARNING = "warning"
SEVERITY_BLOCKED = "blocked"
SEVERITY_ERROR = "error"
SEVERITIES = (SEVERITY_OK, SEVERITY_INFO, SEVERITY_WARNING, SEVERITY_BLOCKED, SEVERITY_ERROR)

PATH_SCOPES = {
    "repo_relative",
    "app_data_relative",
    "env_relative",
    "user_selected",
    "external_only",
    "git_metadata",
}
GIT_POLICIES = {"tracked_allowed", "ignored_required", "never_commit", "external_only"}
PRIVACY_VALUES = {
    "public_repo_source",
    "generated_nonprivate",
    "private_local",
    "secret_or_credential",
    "unknown_private",
}
PRIVATE_PRIVACY = {"private_local", "secret_or_credential", "unknown_private"}
REQUIRED_ARTIFACT_CLASSES = {
    "Repo-Owned Source Files",
    "Generated Local App State",
    "Private Local Inputs",
    "Private Local Outputs",
    "Generated Nonprivate Support Data",
    "Secret And Credential Surfaces",
}


class UsageError(Exception):
    """Configuration or invocation error that should exit 2."""


@dataclass(frozen=True)
class CheckOptions:
    repo_root: Path
    profile: str
    requested_profile: str
    app_data_root: Path | None
    player_log_path: str | None
    source_path: str | None
    source_folder: str | None


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise UsageError(f"invalid manifest JSON: {exc.msg}") from exc
    except OSError as exc:
        raise UsageError(f"unable to read manifest: {exc.strerror or exc}") from exc
    if not isinstance(loaded, dict):
        raise UsageError("manifest must be a JSON object")
    validate_manifest(loaded)
    return loaded


def validate_manifest(manifest: dict[str, Any]) -> None:
    required_top_level = {
        "schema_version",
        "object",
        "description",
        "profiles",
        "artifact_classes",
        "artifacts",
    }
    missing = sorted(required_top_level - set(manifest))
    if missing:
        raise UsageError(f"manifest missing required fields: {', '.join(missing)}")
    if manifest["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise UsageError(f"unsupported manifest schema_version: {manifest['schema_version']!r}")
    if manifest["object"] != MANIFEST_OBJECT:
        raise UsageError(f"unsupported manifest object: {manifest['object']!r}")
    profiles = _require_mapping(manifest, "profiles")
    artifact_classes = _require_mapping(manifest, "artifact_classes")
    artifacts = _require_list(manifest, "artifacts")
    missing_classes = sorted(REQUIRED_ARTIFACT_CLASSES - set(artifact_classes))
    if missing_classes:
        raise UsageError(f"manifest missing artifact classes: {', '.join(missing_classes)}")

    artifact_ids: set[str] = set()
    for raw_artifact in artifacts:
        if not isinstance(raw_artifact, dict):
            raise UsageError("each artifact must be an object")
        _validate_artifact(raw_artifact, profiles, artifact_classes)
        artifact_id = str(raw_artifact["id"])
        if artifact_id in artifact_ids:
            raise UsageError(f"duplicate artifact id: {artifact_id}")
        artifact_ids.add(artifact_id)

    for profile_name, raw_profile in profiles.items():
        if not isinstance(raw_profile, dict):
            raise UsageError(f"profile {profile_name!r} must be an object")
        referenced = raw_profile.get("artifacts")
        if not isinstance(referenced, list) or not referenced:
            raise UsageError(f"profile {profile_name!r} must reference artifact ids")
        unknown = sorted(str(artifact_id) for artifact_id in referenced if str(artifact_id) not in artifact_ids)
        if unknown:
            raise UsageError(f"profile {profile_name!r} references unknown artifacts: {', '.join(unknown)}")

    aliases = manifest.get("profile_aliases", {})
    if aliases is not None:
        if not isinstance(aliases, dict):
            raise UsageError("profile_aliases must be an object when present")
        unknown_alias_targets = sorted(str(target) for target in aliases.values() if str(target) not in profiles)
        if unknown_alias_targets:
            raise UsageError(f"profile aliases target unknown profiles: {', '.join(unknown_alias_targets)}")


def _validate_artifact(
    artifact: dict[str, Any],
    profiles: dict[str, Any],
    artifact_classes: dict[str, Any],
) -> None:
    required_fields = {
        "id",
        "label",
        "classification",
        "path_scope",
        "path_pattern",
        "git_policy",
        "privacy",
        "profiles",
        "safe_checks",
        "forbidden_checks",
        "notes",
    }
    missing = sorted(required_fields - set(artifact))
    if missing:
        artifact_id = artifact.get("id", "<unknown>")
        raise UsageError(f"artifact {artifact_id!r} missing required fields: {', '.join(missing)}")
    artifact_id = str(artifact["id"])
    if not artifact_id.replace("_", "").isalnum():
        raise UsageError(f"artifact id must be snake_case-like: {artifact_id}")
    if artifact["classification"] not in artifact_classes:
        raise UsageError(f"artifact {artifact_id!r} uses unknown classification")
    if artifact["path_scope"] not in PATH_SCOPES:
        raise UsageError(f"artifact {artifact_id!r} uses unsupported path_scope")
    if artifact["git_policy"] not in GIT_POLICIES:
        raise UsageError(f"artifact {artifact_id!r} uses unsupported git_policy")
    if artifact["privacy"] not in PRIVACY_VALUES:
        raise UsageError(f"artifact {artifact_id!r} uses unsupported privacy")
    artifact_profiles = _require_mapping(artifact, "profiles")
    unknown_profiles = sorted(str(profile) for profile in artifact_profiles if str(profile) not in profiles)
    if unknown_profiles:
        raise UsageError(f"artifact {artifact_id!r} references unknown profiles: {', '.join(unknown_profiles)}")
    for profile_name, settings in artifact_profiles.items():
        if not isinstance(settings, dict):
            raise UsageError(f"artifact {artifact_id!r} profile {profile_name!r} must be an object")
        for key in ("missing_severity", "present_severity"):
            if key in settings and settings[key] not in SEVERITIES:
                raise UsageError(f"artifact {artifact_id!r} profile {profile_name!r} has bad {key}")
    if not isinstance(artifact["safe_checks"], list) or not isinstance(artifact["forbidden_checks"], list):
        raise UsageError(f"artifact {artifact_id!r} safe_checks and forbidden_checks must be lists")


def _require_mapping(value: dict[str, Any], key: str) -> dict[str, Any]:
    item = value.get(key)
    if not isinstance(item, dict):
        raise UsageError(f"manifest field {key!r} must be an object")
    return item


def _require_list(value: dict[str, Any], key: str) -> list[Any]:
    item = value.get(key)
    if not isinstance(item, list):
        raise UsageError(f"manifest field {key!r} must be a list")
    return item


def build_report(manifest: dict[str, Any], options: CheckOptions) -> dict[str, Any]:
    profile = _resolve_profile(manifest, options.requested_profile)
    profile_data = manifest["profiles"][profile]
    artifact_by_id = {artifact["id"]: artifact for artifact in manifest["artifacts"]}
    findings = [
        evaluate_artifact(artifact_by_id[artifact_id], profile=profile, options=options)
        for artifact_id in profile_data["artifacts"]
    ]
    summary = {
        "checks": len(findings),
        "ok": sum(1 for item in findings if item["severity"] == SEVERITY_OK),
        "info": sum(1 for item in findings if item["severity"] == SEVERITY_INFO),
        "warnings": sum(1 for item in findings if item["severity"] == SEVERITY_WARNING),
        "blocked": sum(1 for item in findings if item["severity"] == SEVERITY_BLOCKED),
        "errors": sum(1 for item in findings if item["severity"] == SEVERITY_ERROR),
    }
    status = _status_from_summary(summary)
    return {
        "object": REPORT_OBJECT,
        "schema_version": REPORT_SCHEMA_VERSION,
        "profile": profile,
        "requested_profile": options.requested_profile,
        "status": status,
        "summary": summary,
        "privacy": {
            "raw_paths_echoed": False,
            "private_contents_read": False,
            "files_modified": False,
        },
        "findings": findings,
    }


def _resolve_profile(manifest: dict[str, Any], requested_profile: str) -> str:
    profiles = manifest["profiles"]
    aliases = manifest.get("profile_aliases", {})
    profile = aliases.get(requested_profile, requested_profile)
    if profile not in profiles:
        known = ", ".join(sorted([*profiles, *aliases]))
        raise UsageError(f"unsupported profile {requested_profile!r}; known profiles: {known}")
    return str(profile)


def _status_from_summary(summary: dict[str, int]) -> str:
    if summary["errors"]:
        return SEVERITY_ERROR
    if summary["blocked"]:
        return SEVERITY_BLOCKED
    if summary["warnings"]:
        return "warning"
    return SEVERITY_OK


def evaluate_artifact(artifact: dict[str, Any], *, profile: str, options: CheckOptions) -> dict[str, Any]:
    scope = artifact["path_scope"]
    if scope == "repo_relative":
        severity, observed, message, remediation = _evaluate_repo_artifact(artifact, profile=profile, options=options)
    elif scope == "app_data_relative":
        severity, observed, message, remediation = _evaluate_app_data_artifact(
            artifact,
            profile=profile,
            options=options,
        )
    elif scope == "user_selected":
        severity, observed, message, remediation = _evaluate_user_selected_artifact(
            artifact,
            profile=profile,
            options=options,
        )
    elif scope == "env_relative":
        severity, observed, message, remediation = _evaluate_env_artifact(artifact, profile=profile)
    else:
        severity, observed, message, remediation = (
            _missing_severity(artifact, profile),
            "not_checked",
            "This artifact is documented but has no metadata check in v1.",
            "Use a scoped follow-up contract before adding behavior.",
        )

    return {
        "check_id": f"{profile}:{artifact['id']}",
        "artifact_id": artifact["id"],
        "classification": artifact["classification"],
        "severity": severity,
        "display_path": _display_path(artifact),
        "expected": _expected_text(artifact, profile),
        "observed": observed,
        "message": message,
        "remediation": remediation,
        "contents_read": False,
        "path_echoed": False,
    }


def _evaluate_repo_artifact(
    artifact: dict[str, Any],
    *,
    profile: str,
    options: CheckOptions,
) -> tuple[str, str, str, str]:
    settings = _profile_settings(artifact, profile)
    matched_relatives = _matching_repo_path_patterns(options.repo_root, str(artifact["path_pattern"]))
    if matched_relatives:
        return _evaluate_present_repo_artifact(
            artifact,
            profile=profile,
            options=options,
            relatives=matched_relatives,
            settings=settings,
        )

    relative = _concrete_repo_path_pattern(str(artifact["path_pattern"]))
    if relative is None:
        return (
            _missing_severity(artifact, profile),
            "symbolic_pattern_only",
            "No concrete repo path is checked for this symbolic artifact pattern.",
            "Keep this artifact local and use dedicated secret/private scanners for content checks.",
        )

    path = options.repo_root / relative
    exists = _path_exists(path)
    git_policy = artifact["git_policy"]
    if not exists:
        if git_policy in {"ignored_required", "never_commit"}:
            ignored, git_error = _is_git_ignored(options.repo_root, relative)
            if git_error:
                return (SEVERITY_ERROR, "git_metadata_unavailable", git_error, "Verify Git is available locally.")
            if artifact.get("gitignore_expectation") == "report_if_missing" and not ignored:
                return (
                    SEVERITY_WARNING,
                    "missing_not_ignored",
                    "No local artifact is present, but ignore coverage is not confirmed.",
                    "Record as a suspected ignore-policy gap before any follow-up edit.",
                )
            return (
                _missing_severity(artifact, profile),
                "missing_ignored" if ignored else "missing",
                "Optional local/generated artifact is not present.",
                "No action required unless this profile needs the artifact on this machine.",
            )
        return _missing_required_or_optional(artifact, profile)

    return _evaluate_present_repo_artifact(
        artifact,
        profile=profile,
        options=options,
        relatives=(relative,),
        settings=settings,
    )


def _evaluate_present_repo_artifact(
    artifact: dict[str, Any],
    *,
    profile: str,
    options: CheckOptions,
    relatives: tuple[str, ...],
    settings: dict[str, Any],
) -> tuple[str, str, str, str]:
    for relative in relatives:
        kind_error = _kind_error(options.repo_root / relative, artifact)
        if kind_error:
            return (
                SEVERITY_WARNING if not settings.get("required") else SEVERITY_BLOCKED,
                kind_error,
                "Path exists but does not match the expected file or directory kind.",
                "Inspect the local path manually without committing generated/private content.",
            )

    git_policy = artifact["git_policy"]
    if git_policy == "tracked_allowed":
        for relative in relatives:
            tracked, git_error = _is_git_tracked(options.repo_root, relative)
            if git_error:
                return (SEVERITY_ERROR, "git_metadata_unavailable", git_error, "Verify Git is available locally.")
            if not tracked:
                return (
                    SEVERITY_WARNING,
                    "present_untracked",
                    "Repo-owned source path exists but is not currently tracked by Git.",
                    "Review whether this path should be staged in the scoped submitter thread.",
                )
        return (
            SEVERITY_OK,
            "present_tracked",
            "Repo-owned source path is present and tracked.",
            "No action required.",
        )

    all_ignored = True
    for relative in relatives:
        ignored, git_error = _is_git_ignored(options.repo_root, relative)
        if git_error:
            return (SEVERITY_ERROR, "git_metadata_unavailable", git_error, "Verify Git is available locally.")
        if not ignored:
            all_ignored = False

    if all_ignored:
        return (
            _present_severity(artifact, profile),
            "present_ignored",
            "Local/generated artifact family is present and appears ignored.",
            "Do not read or commit private/generated contents.",
        )
    return (
        SEVERITY_BLOCKED,
        "present_not_ignored",
        "Local/generated artifact family is present without confirmed ignore coverage.",
        "Stop and route a narrow ignore-policy follow-up before submitter work.",
    )


def _matching_repo_path_patterns(repo_root: Path, pattern: str) -> tuple[str, ...]:
    clean = _repo_path_pattern_text(pattern)
    if clean != ".env*":
        return ()
    try:
        return tuple(sorted(path.name for path in repo_root.glob(".env*") if _path_exists(path)))
    except OSError:
        return ()


def _repo_path_pattern_text(pattern: str) -> str | None:
    clean = pattern.replace("\\", "/").strip()
    for prefix in ("<placeholder_repo>/", "<repo>/"):
        if clean.startswith(prefix):
            clean = clean[len(prefix) :]
    if clean.startswith("<"):
        return None
    return clean


def _concrete_repo_path_pattern(pattern: str) -> str | None:
    clean = _repo_path_pattern_text(pattern)
    if clean is None:
        return None
    if "*" in clean:
        clean = clean.split("*", 1)[0].rstrip("/")
    return clean or None


def _path_exists(path: Path) -> bool:
    try:
        return path.exists()
    except OSError:
        return False


def _evaluate_app_data_artifact(
    artifact: dict[str, Any],
    *,
    profile: str,
    options: CheckOptions,
) -> tuple[str, str, str, str]:
    if options.app_data_root is None:
        return (
            _missing_severity(artifact, profile),
            "app_data_root_unavailable",
            "No app data root was supplied and LOCALAPPDATA is unavailable.",
            "Supply --app-data-root for a local readiness check when needed.",
        )

    relative = str(artifact["path_pattern"]).replace("\\", "/").strip("/")
    if artifact["id"] == "sqlite_sidecar_files":
        sidecar_paths = [
            options.app_data_root / "db" / "mythic_edge.sqlite3-wal",
            options.app_data_root / "db" / "mythic_edge.sqlite3-shm",
            options.app_data_root / "db" / "mythic_edge.sqlite3-journal",
        ]
        exists = any(_path_exists(path) for path in sidecar_paths)
    else:
        path = options.app_data_root if not relative else options.app_data_root / relative
        exists = _path_exists(path)
        kind_error = _kind_error(path, artifact) if exists else ""
        if kind_error:
            return (
                SEVERITY_WARNING,
                kind_error,
                "App-data path exists but does not match the expected kind.",
                "Inspect the local app setup manually; the checker did not modify it.",
            )

    if exists:
        return (
            _present_severity(artifact, profile),
            "present",
            "Local app artifact is present using symbolic app-data reporting.",
            "No automatic cleanup or migration is performed by this checker.",
        )
    return (
        _missing_severity(artifact, profile),
        "missing",
        "Local app artifact is missing.",
        "No action required unless this profile needs initialized local app state.",
    )


def _evaluate_user_selected_artifact(
    artifact: dict[str, Any],
    *,
    profile: str,
    options: CheckOptions,
) -> tuple[str, str, str, str]:
    raw_path = _selected_path_for_artifact(artifact, options)
    if not raw_path:
        return (
            _missing_severity(artifact, profile),
            "not_supplied",
            "No local path was supplied for this private input.",
            "Pass the relevant CLI option only when checking this machine's readiness.",
        )
    path = Path(raw_path)
    try:
        exists = path.exists()
        is_file = path.is_file()
        is_dir = path.is_dir()
    except OSError:
        return (
            SEVERITY_BLOCKED if _profile_settings(artifact, profile).get("required") else SEVERITY_WARNING,
            "uninspectable",
            "The supplied private path could not be inspected safely.",
            "Inspect the local path manually; the checker did not read or print it.",
        )

    if not exists:
        return (
            SEVERITY_BLOCKED if _profile_settings(artifact, profile).get("required") else SEVERITY_WARNING,
            "supplied_missing",
            "A private path was supplied but does not exist.",
            "Correct the local selection without committing private paths.",
        )
    if "file_kind" in artifact["safe_checks"] and not is_file:
        return (
            SEVERITY_BLOCKED,
            "supplied_not_file",
            "A private path was supplied but is not a file.",
            "Choose a file path for this profile input.",
        )
    if "directory_kind" in artifact["safe_checks"] and not is_dir:
        return (
            SEVERITY_BLOCKED,
            "supplied_not_directory",
            "A private path was supplied but is not a directory.",
            "Choose a folder path for this profile input.",
        )
    if "extension" in artifact["safe_checks"] and path.suffix.lower() != ".jsonl":
        return (
            SEVERITY_BLOCKED,
            "supplied_wrong_extension",
            "A private path was supplied but does not have the expected .jsonl extension.",
            "Choose an approved JSONL source without committing or copying it.",
        )
    return (
        _present_severity(artifact, profile),
        "supplied_present",
        "Private input is present. Contents were not read and the raw path was not echoed.",
        "Run the approved import/parser flow separately only when explicitly authorized.",
    )


def _evaluate_env_artifact(artifact: dict[str, Any], *, profile: str) -> tuple[str, str, str, str]:
    env_var = str(artifact.get("env_var") or "")
    if not env_var:
        return (
            _missing_severity(artifact, profile),
            "not_configured",
            "No environment variable name is defined for this artifact.",
            "Keep secret material out of committed files.",
        )
    if env_var in os.environ:
        return (
            _present_severity(artifact, profile),
            "env_var_present",
            "Environment variable name is present; value was not printed.",
            "Verify the value manually if this machine needs the integration.",
        )
    return (
        _missing_severity(artifact, profile),
        "env_var_missing",
        "Environment variable name is not present.",
        "No action required unless this profile needs the integration on this machine.",
    )


def _selected_path_for_artifact(artifact: dict[str, Any], options: CheckOptions) -> str | None:
    artifact_id = artifact["id"]
    if artifact_id == "private_input_player_log":
        return options.player_log_path or _env_value_if_present(str(artifact.get("env_var") or ""))
    if artifact_id == "private_input_historical_jsonl_file":
        return options.source_path
    if artifact_id == "private_input_historical_jsonl_folder":
        return options.source_folder
    return None


def _env_value_if_present(name: str) -> str | None:
    if not name or name not in os.environ:
        return None
    return os.environ.get(name)


def _profile_settings(artifact: dict[str, Any], profile: str) -> dict[str, Any]:
    return artifact["profiles"].get(profile, {"required": False, "missing_severity": SEVERITY_INFO})


def _missing_severity(artifact: dict[str, Any], profile: str) -> str:
    settings = _profile_settings(artifact, profile)
    if "missing_severity" in settings:
        return str(settings["missing_severity"])
    return SEVERITY_BLOCKED if settings.get("required") else SEVERITY_INFO


def _present_severity(artifact: dict[str, Any], profile: str) -> str:
    settings = _profile_settings(artifact, profile)
    if "present_severity" in settings:
        return str(settings["present_severity"])
    return SEVERITY_OK


def _missing_required_or_optional(
    artifact: dict[str, Any],
    profile: str,
) -> tuple[str, str, str, str]:
    severity = _missing_severity(artifact, profile)
    if severity == SEVERITY_BLOCKED:
        return (
            SEVERITY_BLOCKED,
            "missing_required",
            "Required profile artifact is missing.",
            "Install or restore repo-owned source through normal Git workflow.",
        )
    return (
        severity,
        "missing_optional",
        "Optional artifact is missing.",
        "No action required unless this profile needs the artifact on this machine.",
    )


def _expected_text(artifact: dict[str, Any], profile: str) -> str:
    settings = _profile_settings(artifact, profile)
    requirement = "required" if settings.get("required") else "optional"
    return f"{requirement}; git_policy={artifact['git_policy']}; privacy={artifact['privacy']}"


def _display_path(artifact: dict[str, Any]) -> str:
    explicit = artifact.get("example_display_path")
    if explicit:
        return str(explicit)
    scope = artifact["path_scope"]
    pattern = str(artifact["path_pattern"])
    if scope == "repo_relative":
        if _repo_path_pattern_text(pattern) == ".env*":
            return "<repo>\\.env*"
        clean = _concrete_repo_path_pattern(pattern) or pattern
        return "<repo>" if not clean else "<repo>\\" + clean.replace("/", "\\")
    if scope == "app_data_relative":
        clean = pattern.replace("/", "\\").strip("\\")
        return "<app_data>" if not clean else "<app_data>\\" + clean
    if scope == "user_selected":
        return pattern
    if scope == "env_relative":
        return str(artifact.get("example_display_path") or "<configured_secret>")
    return "<external>"


def _kind_error(path: Path, artifact: dict[str, Any]) -> str:
    try:
        if "file_kind" in artifact["safe_checks"] and not path.is_file():
            return "wrong_kind"
        if "directory_kind" in artifact["safe_checks"] and not path.is_dir():
            return "wrong_kind"
    except OSError:
        return "uninspectable"
    return ""


def _is_git_tracked(repo_root: Path, relative: str) -> tuple[bool, str]:
    path = relative.replace("\\", "/").rstrip("/")
    if not path:
        return False, ""
    try:
        command = ["git", "ls-files", "--", path]
        result = subprocess.run(command, cwd=repo_root, capture_output=True, text=True, check=False)
    except OSError as exc:
        return False, str(exc)
    if result.returncode not in (0,):
        return False, result.stderr.strip() or "git ls-files failed"
    return bool(result.stdout.strip()), ""


def _is_git_ignored(repo_root: Path, relative: str) -> tuple[bool, str]:
    candidates = _ignore_candidates(relative)
    try:
        for candidate in candidates:
            result = subprocess.run(
                ["git", "check-ignore", "-q", "--", candidate],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return True, ""
            if result.returncode not in (1,):
                return False, result.stderr.strip() or "git check-ignore failed"
    except OSError as exc:
        return False, str(exc)
    return False, ""


def _ignore_candidates(relative: str) -> tuple[str, ...]:
    clean = relative.replace("\\", "/").rstrip("/")
    if not clean:
        return ()
    candidates = [clean]
    name = clean.rsplit("/", 1)[-1]
    if "." not in name:
        candidates.append(f"{clean}/.local-environment-check")
    return tuple(candidates)


def build_options(args: argparse.Namespace, manifest: dict[str, Any]) -> CheckOptions:
    repo_root = Path(args.repo_root).resolve()
    requested_profile = str(args.profile)
    profile = _resolve_profile(manifest, requested_profile)
    return CheckOptions(
        repo_root=repo_root,
        profile=profile,
        requested_profile=requested_profile,
        app_data_root=_resolve_app_data_root(args.app_data_root),
        player_log_path=args.player_log_path,
        source_path=args.source_path,
        source_folder=args.source_folder,
    )


def _resolve_app_data_root(raw_app_data_root: str | None) -> Path | None:
    if raw_app_data_root:
        return Path(raw_app_data_root)
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        return None
    return Path(local_app_data) / LOCAL_APP_DIR_NAME


def render_text(report: dict[str, Any]) -> str:
    lines = [
        "Local Environment Report",
        f"schema_version: {report['schema_version']}",
        f"profile: {report['profile']}",
        f"requested_profile: {report['requested_profile']}",
        f"status: {report['status']}",
        (
            "summary: "
            f"checks={report['summary']['checks']} "
            f"ok={report['summary']['ok']} "
            f"info={report['summary']['info']} "
            f"warnings={report['summary']['warnings']} "
            f"blocked={report['summary']['blocked']} "
            f"errors={report['summary']['errors']}"
        ),
        "privacy: raw_paths_echoed=false private_contents_read=false files_modified=false",
        "",
        "Findings:",
    ]
    for finding in report["findings"]:
        lines.append(
            f"- {finding['severity'].upper()} {finding['artifact_id']} "
            f"{finding['display_path']} observed={finding['observed']}"
        )
        lines.append(f"  expected: {finding['expected']}")
        lines.append(f"  message: {finding['message']}")
        lines.append(f"  remediation: {finding['remediation']}")
    lines.append(f"result: {report['status']}")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report Mythic Edge local environment readiness by profile.")
    parser.add_argument("--repo-root", default=str(default_repo_root()), help="Repository root.")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, help="Manifest path, absolute or repo-relative.")
    parser.add_argument("--profile", required=True, help="Environment profile from the manifest.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Report format.")
    parser.add_argument("--app-data-root", help="Optional local app data root for metadata-only checks.")
    parser.add_argument("--player-log-path", help="Optional private Player.log path. Contents are never read.")
    parser.add_argument("--source-path", help="Optional private JSONL source file. Contents are never read.")
    parser.add_argument("--source-folder", help="Optional private JSONL source folder. Contents are not enumerated.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = repo_root / manifest_path
    try:
        manifest = load_manifest(manifest_path)
        options = build_options(args, manifest)
        report = build_report(manifest, options)
    except UsageError as exc:
        print(f"Local Environment Report\nerror: {exc}\nresult: error", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
