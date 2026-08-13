from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import sys
import uuid
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

INVOCATION_SCHEMA = "mythic_edge_issue_wave_invocation.v1"
MANIFEST_SCHEMA = "mythic_edge_issue_wave_manifest.v1"
STATE_SCHEMA = "mythic_edge_issue_wave_state.v1"
EVENT_SCHEMA = "mythic_edge_issue_wave_event.v1"
EVENT_REQUEST_SCHEMA = "mythic_edge_issue_wave_event_request.v1"
GOVERNANCE_PACKET_SCHEMA = "mythic_edge_issue_wave_governance_packet.v1"
GOVERNANCE_ROUTE_SCHEMA = "mythic_edge_issue_wave_governance_route.v1"
INSPECT_SCHEMA = "mythic_edge_issue_wave_inspect.v1"
REVIEWED_PACKAGE_SCHEMA = "mythic_edge_issue_wave_reviewed_package.v1"

RUN_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$")
TIMESTAMP_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
LANE_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
BRANCH_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._/-]{0,198}[A-Za-z0-9])?$")
ZERO_DIGEST = "0" * 64
BINARY_FLAG = getattr(os, "O_BINARY", 0)

DEFAULT_ALLOWLIST = (
    "Tahjali11/Mythic-Edge",
    "Tahjali11/Mythic-Edge-Analytics",
    "Tahjali11/Mythic-Edge-Fable-Engine",
    "Tahjali11/Mythic-Edge-Corpus",
    "Tahjali11/Mythic-Edge-Automation-Artifacts",
    "Tahjali11/Mythic-Edge-Security",
    "Tahjali11/Mythic-Edge-Feature-Expansions",
    "Tahjali11/Mythic-Edge-Research-and-Development",
    "Tahjali11/Mythic-Edge-Application-Function",
    "Tahjali11/Mythic-Edge-Governance",
)
ALLOWLIST_BY_CASEFOLD = {name.casefold(): name for name in DEFAULT_ALLOWLIST}

PROGRESS_STATES = (
    "selected",
    "a_running",
    "a_complete",
    "a_scope_verified",
    "b_running",
    "b_complete",
    "c_running",
    "c_complete",
    "e_running",
    "e_approved",
    "f_running",
    "f_complete",
    "checks_running",
    "g_consideration_ready",
)
STOP_STATES = (
    "a_ambiguous",
    "backward_route_to_a_or_b",
    "d_required",
    "unknown_agent_outcome",
    "incompatible_repository_authority",
    "checkout_unavailable_or_ambiguous",
    "unsafe_or_conflicting_scope",
    "checks_pending",
)
ALL_STATES = frozenset(PROGRESS_STATES + STOP_STATES)
RUNNING_STATES = frozenset(
    {"a_running", "b_running", "c_running", "e_running", "f_running", "checks_running"}
)
FINAL_STATES = frozenset(STOP_STATES + ("g_consideration_ready",))
PRE_ROLE_BOUNDARIES = frozenset(
    {"selected", "a_scope_verified", "b_complete", "c_complete", "e_approved", "f_complete"}
)

FORWARD_TRANSITIONS = {
    ("selected", "a_running"),
    ("a_running", "a_complete"),
    ("a_complete", "a_scope_verified"),
    ("a_scope_verified", "b_running"),
    ("b_running", "b_complete"),
    ("b_complete", "c_running"),
    ("c_running", "c_complete"),
    ("c_complete", "e_running"),
    ("e_running", "e_approved"),
    ("e_approved", "f_running"),
    ("f_running", "f_complete"),
    ("f_complete", "checks_running"),
    ("checks_running", "g_consideration_ready"),
}

AUTHORITY_BACKED_PRIORITIES = frozenset({"tracker", "roadmap", "next_role"})
ANCHOR_RELATIONSHIPS = frozenset(
    {"dependency", "child_issue", "tracker", "roadmap", "next_role"}
)
GOVERNANCE_TRIGGERS = frozenset(
    {
        "a_ambiguity",
        "authority_conflict",
        "unsafe_rule_gap",
        "repeated_inefficiency",
        "systemic_failure",
    }
)
ROLE_BY_RUNNING_STATE = {
    "a_running": "A",
    "b_running": "B",
    "c_running": "C",
    "e_running": "E",
    "f_running": "F",
}

INVOCATION_KEYS = frozenset(
    {"schema_version", "mode", "entry_role", "selectors", "permissions", "explicit_permissions"}
)
SELECTOR_KEYS = frozenset({"repositories", "anchor", "run_id"})
PERMISSION_KEYS = frozenset({"allow_main_draft", "allow_wip_exception"})
MANIFEST_KEYS = frozenset({"schema_version", "candidates"})
CANDIDATE_KEYS = frozenset(
    {"lane_id", "repository", "issue", "issue_created_at", "priority_source", "target_root", "evidence", "scope"}
)
EVIDENCE_KEYS = frozenset(
    {
        "issue_open",
        "not_deferred",
        "prerequisites_complete",
        "prerequisite_relationship_unambiguous",
        "repository_authority_compatible",
        "checkout_identity_exact",
        "active_work_clear",
        "wip_compatible",
        "wip_exception_authorized",
        "scope_known",
        "anchor_relationship",
        "summary",
    }
)
SCOPE_KEYS = frozenset(
    {"paths", "interfaces", "truth_owners", "dependencies", "shared_artifacts", "submission_lanes"}
)
STATE_KEYS = frozenset(
    {
        "schema_version",
        "run_id",
        "created_at_utc",
        "updated_at_utc",
        "revision",
        "last_event_digest",
        "invocation",
        "candidates",
        "lanes",
        "run_complete",
    }
)
LANE_KEYS = frozenset(
    {
        "lane_id",
        "repository",
        "issue",
        "issue_created_at",
        "priority_source",
        "eligibility_summary",
        "scope",
        "checkout_location",
        "worktree_location",
        "state",
        "active_role",
        "artifacts",
        "review_base_commit",
        "reviewed_package_sha256",
        "created_commit",
        "submitted_package_sha256",
        "branch",
        "draft_pr",
        "checks",
        "validation_summary",
        "stop_reason",
        "governance_packets",
    }
)
EVENT_KEYS = frozenset(
    {
        "schema_version",
        "sequence",
        "timestamp_utc",
        "lane_id",
        "from_state",
        "to_state",
        "role",
        "reason",
        "evidence_summary",
        "updates",
        "previous_event_digest",
        "event_digest",
    }
)
EVENT_REQUEST_KEYS = frozenset(
    {"schema_version", "lane_id", "from_state", "to_state", "role", "reason", "evidence_summary", "updates"}
)
UPDATE_KEYS = frozenset(
    {
        "scope",
        "worktree_location",
        "artifacts",
        "review_base_commit",
        "reviewed_package_sha256",
        "created_commit",
        "submitted_package_sha256",
        "branch",
        "draft_pr",
        "checks",
        "validation_summary",
        "governance_packets",
    }
)
CHECK_KEYS = frozenset({"status", "summary"})
REVIEWED_PACKAGE_KEYS = frozenset({"schema_version", "base_commit", "entries"})
REVIEWED_PACKAGE_ENTRY_KEYS = frozenset({"path", "status", "object"})
REVIEWED_PACKAGE_OBJECT_KEYS = frozenset({"type", "mode", "byte_length", "sha256"})
GOVERNANCE_PACKET_KEYS = frozenset(
    {
        "schema_version",
        "run_id",
        "lane_id",
        "repository",
        "issue",
        "role",
        "trigger_category",
        "evidence_summary",
        "impact",
        "repeated_pattern_count",
        "unresolved_question",
        "suggested_review_route",
    }
)


class IssueWaveError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        del message
        self.print_usage(sys.stderr)
        raise IssueWaveError("invalid_command", "command arguments are invalid")


def _exact_keys(value: object, expected: frozenset[str], *, code: str, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise IssueWaveError(code, f"{label} shape is invalid")
    return value


def _bool(value: object, *, code: str, label: str) -> bool:
    if type(value) is not bool:
        raise IssueWaveError(code, f"{label} must be boolean")
    return value


def _positive_int(value: object, *, code: str, label: str) -> int:
    if type(value) is not int or value <= 0:
        raise IssueWaveError(code, f"{label} must be a positive integer")
    return value


def _nonnegative_int(value: object, *, code: str, label: str) -> int:
    if type(value) is not int or value < 0:
        raise IssueWaveError(code, f"{label} must be a nonnegative integer")
    return value


def _timestamp(value: object, *, code: str, label: str) -> str:
    if not isinstance(value, str) or TIMESTAMP_RE.fullmatch(value) is None:
        raise IssueWaveError(code, f"{label} must be a UTC second timestamp")
    try:
        datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)
    except ValueError as error:
        raise IssueWaveError(code, f"{label} must be a UTC second timestamp") from error
    return value


def _now_timestamp(now: datetime | None = None) -> str:
    current = datetime.now(UTC) if now is None else now
    if current.tzinfo is None:
        raise IssueWaveError("invalid_time", "time source must be timezone aware")
    return current.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _canonical_package_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _reviewed_package_path(value: object) -> tuple[str, bytes]:
    if not isinstance(value, str) or not value:
        raise IssueWaveError("invalid_reviewed_package", "reviewed package path is invalid")
    try:
        encoded = value.encode("utf-8", errors="strict")
    except UnicodeEncodeError as error:
        raise IssueWaveError(
            "invalid_reviewed_package", "reviewed package path is invalid"
        ) from error
    parts = value.split("/")
    if (
        value.startswith("/")
        or value.endswith("/")
        or "\\" in value
        or "\x00" in value
        or any(part in {"", ".", ".."} for part in parts)
    ):
        raise IssueWaveError("invalid_reviewed_package", "reviewed package path is invalid")
    return value, encoded


def validate_reviewed_package(value: object) -> dict[str, Any]:
    package = _exact_keys(
        value,
        REVIEWED_PACKAGE_KEYS,
        code="invalid_reviewed_package",
        label="reviewed package",
    )
    if package["schema_version"] != REVIEWED_PACKAGE_SCHEMA:
        raise IssueWaveError(
            "invalid_reviewed_package", "reviewed package schema is unsupported"
        )
    base_commit = package["base_commit"]
    if not isinstance(base_commit, str) or COMMIT_RE.fullmatch(base_commit) is None:
        raise IssueWaveError("invalid_reviewed_package", "review base commit is invalid")
    entries_value = package["entries"]
    if not isinstance(entries_value, list) or not entries_value:
        raise IssueWaveError("invalid_reviewed_package", "reviewed package must be nonempty")

    entries: list[dict[str, Any]] = []
    encoded_paths: list[bytes] = []
    for entry_value in entries_value:
        entry = _exact_keys(
            entry_value,
            REVIEWED_PACKAGE_ENTRY_KEYS,
            code="invalid_reviewed_package",
            label="reviewed package entry",
        )
        path, encoded_path = _reviewed_package_path(entry["path"])
        status = entry["status"]
        if status not in {"added", "modified", "deleted"}:
            raise IssueWaveError("invalid_reviewed_package", "reviewed package status is unsupported")
        object_value = _exact_keys(
            entry["object"],
            REVIEWED_PACKAGE_OBJECT_KEYS,
            code="invalid_reviewed_package",
            label="reviewed package object",
        )
        if object_value["type"] != "blob":
            raise IssueWaveError("invalid_reviewed_package", "reviewed package object type is unsupported")
        if object_value["mode"] not in {"100644", "100755"}:
            raise IssueWaveError("invalid_reviewed_package", "reviewed package object mode is unsupported")
        byte_length = _nonnegative_int(
            object_value["byte_length"],
            code="invalid_reviewed_package",
            label="reviewed package byte length",
        )
        digest = object_value["sha256"]
        if not isinstance(digest, str) or DIGEST_RE.fullmatch(digest) is None:
            raise IssueWaveError("invalid_reviewed_package", "reviewed package object digest is invalid")
        entries.append(
            {
                "path": path,
                "status": status,
                "object": {
                    "type": "blob",
                    "mode": object_value["mode"],
                    "byte_length": byte_length,
                    "sha256": digest,
                },
            }
        )
        encoded_paths.append(encoded_path)

    if len(set(encoded_paths)) != len(encoded_paths):
        raise IssueWaveError("invalid_reviewed_package", "reviewed package paths must be unique")
    if encoded_paths != sorted(encoded_paths):
        raise IssueWaveError(
            "invalid_reviewed_package", "reviewed package entries are not canonically ordered"
        )
    return {
        "schema_version": REVIEWED_PACKAGE_SCHEMA,
        "base_commit": base_commit,
        "entries": entries,
    }


def bind_reviewed_package(value: object) -> dict[str, Any]:
    package = validate_reviewed_package(value)
    return {
        "schema_version": REVIEWED_PACKAGE_SCHEMA,
        "base_commit": package["base_commit"],
        "paths": [entry["path"] for entry in package["entries"]],
        "reviewed_package_sha256": hashlib.sha256(
            _canonical_package_json(package)
        ).hexdigest(),
    }


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise IssueWaveError("invalid_json", "JSON contains a duplicate key")
        result[key] = value
    return result


def strict_json_loads(raw: bytes | str) -> object:
    try:
        text = raw.decode("utf-8", errors="strict") if isinstance(raw, bytes) else raw
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
    except IssueWaveError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise IssueWaveError("invalid_json", "JSON is invalid") from error


def _canonical_repository(value: object, *, code: str) -> str:
    if not isinstance(value, str):
        raise IssueWaveError(code, "repository is invalid")
    canonical = ALLOWLIST_BY_CASEFOLD.get(value.casefold())
    if canonical is None:
        raise IssueWaveError(code, "repository is outside the allowlist")
    return canonical


def _contains_local_absolute_path(value: str) -> bool:
    if re.search(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]", value):
        return True
    if re.search(
        r"(?<![A-Za-z0-9:/])/(?:Users|home|var|tmp)/",
        value,
        flags=re.IGNORECASE,
    ):
        return True
    return re.search(r"\\\\[^\\/\s]+[\\/][^\\/\s]+", value) is not None


def _public_text(value: object, *, code: str, label: str, maximum: int = 500) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum or "\n" in value or "\r" in value:
        raise IssueWaveError(code, f"{label} is invalid")
    lowered = value.casefold()
    forbidden_markers = (
        "authorization:",
        "bearer ",
        "password=",
        "password:",
        "api_key",
        "api-key",
        "webhook url",
        "token=",
        "player.log",
        "utc_log",
    )
    if any(marker in lowered for marker in forbidden_markers):
        raise IssueWaveError(code, f"{label} contains forbidden content")
    if _contains_local_absolute_path(value):
        raise IssueWaveError(code, f"{label} contains a local absolute path")
    return value


def _public_string_list(value: object, *, code: str, label: str, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise IssueWaveError(code, f"{label} must be a list")
    result = [_public_text(item, code=code, label=label, maximum=300) for item in value]
    if len({item.casefold() for item in result}) != len(result):
        raise IssueWaveError(code, f"{label} must contain unique values")
    if result != sorted(result, key=str.casefold):
        raise IssueWaveError(code, f"{label} must be deterministically ordered")
    return result


def generate_run_id(*, now: datetime | None = None, entropy: bytes | None = None) -> str:
    suffix_bytes = secrets.token_bytes(4) if entropy is None else entropy
    if len(suffix_bytes) != 4:
        raise IssueWaveError("invalid_entropy", "run entropy must contain four bytes")
    return f"{_now_timestamp(now)}-{suffix_bytes.hex()}"


def parse_invocation(command: str) -> dict[str, Any]:
    if not isinstance(command, str):
        raise IssueWaveError("invalid_invocation", "invocation must be text")
    match = re.fullmatch(
        r"\s*\$mythic-edge-issue-wave\s+(Inspect|Dispatch)\s*\(\s*(.*?)\s*\)\s*",
        command,
    )
    if match is None:
        raise IssueWaveError(
            "invalid_invocation",
            "usage: $mythic-edge-issue-wave <Inspect|Dispatch> (A[; option ...])",
        )
    mode, body = match.groups()
    parts = [part.strip() for part in body.split(";")]
    if not parts or parts[0] != "A" or any(not part for part in parts):
        raise IssueWaveError("invalid_invocation", "entry role must be exactly A")

    values: dict[str, object] = {}
    flags: set[str] = set()
    for option in parts[1:]:
        if option in {"allow-main-draft", "allow-wip-exception"}:
            if option in flags:
                raise IssueWaveError("invalid_invocation", "an invocation option is repeated")
            flags.add(option)
            continue
        if "=" not in option or option.count("=") != 1:
            raise IssueWaveError("invalid_invocation", "an invocation option is malformed")
        key, raw_value = option.split("=", 1)
        if key not in {"repos", "anchor", "run"} or not raw_value:
            raise IssueWaveError("invalid_invocation", "an invocation option is unsupported")
        if key in values:
            raise IssueWaveError("invalid_invocation", "an invocation option is repeated")
        values[key] = raw_value

    repositories: list[str] | None = None
    if "repos" in values:
        raw_repositories = str(values["repos"]).split(",")
        if not 1 <= len(raw_repositories) <= 3 or any(not item for item in raw_repositories):
            raise IssueWaveError("invalid_invocation", "repos must contain one to three repositories")
        repositories = [
            _canonical_repository(item, code="invalid_invocation") for item in raw_repositories
        ]
        if len({item.casefold() for item in repositories}) != len(repositories):
            raise IssueWaveError("invalid_invocation", "repos must contain unique repositories")

    anchor: dict[str, object] | None = None
    if "anchor" in values:
        anchor_match = re.fullmatch(r"([^#]+)#([1-9][0-9]*)", str(values["anchor"]))
        if anchor_match is None:
            raise IssueWaveError("invalid_invocation", "anchor must identify one positive issue")
        anchor = {
            "repository": _canonical_repository(anchor_match.group(1), code="invalid_invocation"),
            "issue": int(anchor_match.group(2)),
        }

    run_id = values.get("run")
    if run_id is not None and (not isinstance(run_id, str) or RUN_ID_RE.fullmatch(run_id) is None):
        raise IssueWaveError("invalid_invocation", "run must use the required run identifier shape")
    if run_id is not None and (repositories is not None or anchor is not None):
        raise IssueWaveError("invalid_invocation", "run cannot be combined with repos or anchor")
    if mode == "Inspect" and flags:
        raise IssueWaveError("invalid_invocation", "Inspect accepts no Dispatch permissions")

    explicit_permissions = sorted(flag.replace("-", "_") for flag in flags)
    return {
        "schema_version": INVOCATION_SCHEMA,
        "mode": mode,
        "entry_role": "A",
        "selectors": {
            "repositories": repositories,
            "anchor": anchor,
            "run_id": run_id,
        },
        "permissions": {
            "allow_main_draft": "allow-main-draft" in flags,
            "allow_wip_exception": "allow-wip-exception" in flags,
        },
        "explicit_permissions": explicit_permissions,
    }


def _validate_invocation_object(value: object) -> dict[str, Any]:
    invocation = _exact_keys(value, INVOCATION_KEYS, code="invalid_invocation", label="invocation")
    if invocation["schema_version"] != INVOCATION_SCHEMA:
        raise IssueWaveError("invalid_invocation", "invocation schema is unsupported")
    if invocation["mode"] not in {"Inspect", "Dispatch"} or invocation["entry_role"] != "A":
        raise IssueWaveError("invalid_invocation", "invocation mode or entry role is invalid")
    selectors = _exact_keys(
        invocation["selectors"], SELECTOR_KEYS, code="invalid_invocation", label="selectors"
    )
    permissions = _exact_keys(
        invocation["permissions"], PERMISSION_KEYS, code="invalid_invocation", label="permissions"
    )
    for key in PERMISSION_KEYS:
        _bool(permissions[key], code="invalid_invocation", label="permission")
    explicit = invocation["explicit_permissions"]
    if not isinstance(explicit, list) or explicit != sorted(explicit) or len(set(explicit)) != len(explicit):
        raise IssueWaveError("invalid_invocation", "explicit permissions are invalid")
    if any(item not in PERMISSION_KEYS or permissions[item] is not True for item in explicit):
        raise IssueWaveError("invalid_invocation", "explicit permissions are inconsistent")
    repositories = selectors["repositories"]
    if repositories is not None:
        if not isinstance(repositories, list) or not 1 <= len(repositories) <= 3:
            raise IssueWaveError("invalid_invocation", "repository selectors are invalid")
        canonical = [_canonical_repository(item, code="invalid_invocation") for item in repositories]
        if canonical != repositories or len({item.casefold() for item in canonical}) != len(canonical):
            raise IssueWaveError("invalid_invocation", "repository selectors are invalid")
    anchor = selectors["anchor"]
    if anchor is not None:
        anchor_object = _exact_keys(
            anchor, frozenset({"repository", "issue"}), code="invalid_invocation", label="anchor"
        )
        if _canonical_repository(anchor_object["repository"], code="invalid_invocation") != anchor_object["repository"]:
            raise IssueWaveError("invalid_invocation", "anchor repository is not canonical")
        _positive_int(anchor_object["issue"], code="invalid_invocation", label="anchor issue")
    run_id = selectors["run_id"]
    if run_id is not None and (not isinstance(run_id, str) or RUN_ID_RE.fullmatch(run_id) is None):
        raise IssueWaveError("invalid_invocation", "run selector is invalid")
    if run_id is not None and (repositories is not None or anchor is not None):
        raise IssueWaveError("invalid_invocation", "run selector combination is invalid")
    if invocation["mode"] == "Inspect" and any(permissions.values()):
        raise IssueWaveError("invalid_invocation", "Inspect permissions are invalid")
    return invocation


def validate_resume_invocation(invocation: Mapping[str, Any], state: Mapping[str, Any]) -> None:
    current = _validate_invocation_object(dict(invocation))
    if current["selectors"]["run_id"] != state.get("run_id"):
        raise IssueWaveError("permission_drift", "resume run identifier does not match")
    if current["mode"] == "Dispatch":
        saved_permissions = state["invocation"]["permissions"]
        for permission in current["explicit_permissions"]:
            if current["permissions"][permission] != saved_permissions[permission]:
                raise IssueWaveError("permission_drift", "resume permissions do not match saved permissions")


def _validate_scope(value: object, *, code: str) -> dict[str, list[str]]:
    scope = _exact_keys(value, SCOPE_KEYS, code=code, label="scope")
    result = {
        key: _public_string_list(
            scope[key],
            code=code,
            label=f"scope {key}",
            allow_empty=key not in {"paths", "submission_lanes"},
        )
        for key in sorted(SCOPE_KEYS)
    }
    return result


def _resolved_directory(path_value: object, *, code: str, require_exists: bool) -> Path:
    if not isinstance(path_value, str) or not path_value:
        raise IssueWaveError(code, "target root is invalid")
    path = Path(path_value)
    if not path.is_absolute():
        raise IssueWaveError(code, "target root must be absolute")
    try:
        resolved = path.resolve(strict=require_exists)
    except OSError as error:
        raise IssueWaveError(code, "target root cannot be resolved") from error
    if require_exists and not resolved.is_dir():
        raise IssueWaveError(code, "target root must be an existing directory")
    return resolved


def _paths_overlap(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def _reject_pairwise_path_overlap(
    paths: Sequence[Path],
    *,
    code: str,
    message: str,
) -> None:
    for index, left in enumerate(paths):
        for right in paths[index + 1 :]:
            if _paths_overlap(left, right):
                raise IssueWaveError(code, message)


def _validate_state_path_isolation(
    state: Mapping[str, Any],
    run_directory: Path,
    *,
    code: str,
) -> None:
    try:
        paths = [run_directory.parent.resolve(strict=False)]
        paths.extend(
            Path(lane["checkout_location"]).resolve(strict=False) for lane in state["lanes"]
        )
        paths.extend(
            Path(lane["worktree_location"]).resolve(strict=False)
            for lane in state["lanes"]
            if lane["worktree_location"] is not None
        )
    except (KeyError, OSError, TypeError) as error:
        raise IssueWaveError(code, "recorded path isolation is invalid") from error
    _reject_pairwise_path_overlap(
        paths,
        code=code,
        message="recorded checkout, worktree, or state paths overlap",
    )


def _candidate_order_key(candidate: Mapping[str, Any]) -> tuple[int, str, str, int]:
    priority = 0 if candidate["priority_source"] in AUTHORITY_BACKED_PRIORITIES else 1
    return (priority, candidate["issue_created_at"], candidate["repository"].casefold(), candidate["issue"])


def scope_conflicts(candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, object]]:
    conflicts: list[dict[str, object]] = []
    for index, left in enumerate(candidates):
        for right in candidates[index + 1 :]:
            dimensions = [
                dimension
                for dimension in sorted(SCOPE_KEYS)
                if {
                    item.casefold() for item in left["scope"][dimension]
                }.intersection(item.casefold() for item in right["scope"][dimension])
            ]
            if dimensions:
                conflicts.append(
                    {
                        "left_lane_id": left["lane_id"],
                        "right_lane_id": right["lane_id"],
                        "dimensions": dimensions,
                    }
                )
    return conflicts


def validate_manifest(
    manifest_value: object,
    invocation_value: object,
    *,
    target_roots: Mapping[str, Path | str],
    state_root: Path,
    require_existing_roots: bool = True,
) -> dict[str, Any]:
    invocation = _validate_invocation_object(invocation_value)
    if invocation["mode"] != "Dispatch" or invocation["selectors"]["run_id"] is not None:
        raise IssueWaveError("invalid_manifest", "a new manifest requires a new Dispatch invocation")
    manifest = _exact_keys(manifest_value, MANIFEST_KEYS, code="invalid_manifest", label="manifest")
    if manifest["schema_version"] != MANIFEST_SCHEMA:
        raise IssueWaveError("invalid_manifest", "manifest schema is unsupported")
    candidates_value = manifest["candidates"]
    if not isinstance(candidates_value, list) or not 1 <= len(candidates_value) <= 3:
        raise IssueWaveError("invalid_manifest", "manifest must contain one to three candidates")

    canonical_roots: dict[str, Path] = {}
    for repository, path in target_roots.items():
        canonical_repository = _canonical_repository(repository, code="invalid_manifest")
        if canonical_repository in canonical_roots:
            raise IssueWaveError("invalid_manifest", "target roots contain a duplicate repository")
        canonical_roots[canonical_repository] = _resolved_directory(
            str(path), code="invalid_manifest", require_exists=require_existing_roots
        )

    state_root_resolved = state_root.resolve(strict=False)
    resolved_target_roots = list(canonical_roots.values())
    for target_root in resolved_target_roots:
        if _paths_overlap(state_root_resolved, target_root):
            raise IssueWaveError("unsafe_state_root", "state root overlaps a target repository")
    _reject_pairwise_path_overlap(
        resolved_target_roots,
        code="invalid_manifest",
        message="target repository roots overlap",
    )
    candidates: list[dict[str, Any]] = []
    for candidate_value in candidates_value:
        candidate = _exact_keys(
            candidate_value, CANDIDATE_KEYS, code="invalid_manifest", label="candidate"
        )
        lane_id = candidate["lane_id"]
        if not isinstance(lane_id, str) or LANE_ID_RE.fullmatch(lane_id) is None:
            raise IssueWaveError("invalid_manifest", "lane identifier is invalid")
        repository = _canonical_repository(candidate["repository"], code="invalid_manifest")
        if repository != candidate["repository"]:
            raise IssueWaveError("invalid_manifest", "candidate repository is not canonical")
        selected_repositories = invocation["selectors"]["repositories"]
        if selected_repositories is not None and repository not in selected_repositories:
            raise IssueWaveError("invalid_manifest", "candidate is outside requested repositories")
        issue = _positive_int(candidate["issue"], code="invalid_manifest", label="candidate issue")
        issue_created_at = _timestamp(
            candidate["issue_created_at"], code="invalid_manifest", label="issue creation time"
        )
        priority_source = candidate["priority_source"]
        if priority_source not in AUTHORITY_BACKED_PRIORITIES | {"other"}:
            raise IssueWaveError("invalid_manifest", "candidate priority source is invalid")
        target_root = _resolved_directory(
            candidate["target_root"], code="invalid_manifest", require_exists=require_existing_roots
        )
        if canonical_roots.get(repository) != target_root:
            raise IssueWaveError("invalid_manifest", "candidate target root does not match its repository")
        evidence = _exact_keys(
            candidate["evidence"], EVIDENCE_KEYS, code="invalid_manifest", label="candidate evidence"
        )
        required_true = (
            "issue_open",
            "not_deferred",
            "prerequisites_complete",
            "prerequisite_relationship_unambiguous",
            "repository_authority_compatible",
            "checkout_identity_exact",
            "active_work_clear",
            "scope_known",
        )
        for key in required_true:
            if not _bool(evidence[key], code="invalid_manifest", label=f"evidence {key}"):
                raise IssueWaveError("invalid_manifest", "candidate eligibility evidence is incomplete")
        wip_compatible = _bool(
            evidence["wip_compatible"], code="invalid_manifest", label="WIP compatibility"
        )
        wip_exception = _bool(
            evidence["wip_exception_authorized"], code="invalid_manifest", label="WIP exception"
        )
        if not wip_compatible and not (
            invocation["permissions"]["allow_wip_exception"] and wip_exception
        ):
            raise IssueWaveError("invalid_manifest", "candidate WIP evidence is insufficient")
        if wip_compatible and wip_exception:
            raise IssueWaveError("invalid_manifest", "candidate WIP evidence is contradictory")
        anchor_relationship = evidence["anchor_relationship"]
        if invocation["selectors"]["anchor"] is None:
            if anchor_relationship is not None:
                raise IssueWaveError("invalid_manifest", "unexpected anchor relationship")
        elif anchor_relationship not in ANCHOR_RELATIONSHIPS:
            raise IssueWaveError("invalid_manifest", "anchor relationship is not durable")
        summary = _public_text(
            evidence["summary"], code="invalid_manifest", label="eligibility summary"
        )
        scope = _validate_scope(candidate["scope"], code="invalid_manifest")
        candidates.append(
            {
                "lane_id": lane_id,
                "repository": repository,
                "issue": issue,
                "issue_created_at": issue_created_at,
                "priority_source": priority_source,
                "target_root": str(target_root),
                "evidence": {
                    **{key: evidence[key] for key in sorted(EVIDENCE_KEYS) if key != "summary"},
                    "summary": summary,
                },
                "scope": scope,
            }
        )

    if set(canonical_roots) != {candidate["repository"] for candidate in candidates}:
        raise IssueWaveError("invalid_manifest", "target roots must exactly match candidate repositories")
    if len({candidate["lane_id"] for candidate in candidates}) != len(candidates):
        raise IssueWaveError("invalid_manifest", "lane identifiers must be unique")
    if len({candidate["repository"] for candidate in candidates}) != len(candidates):
        raise IssueWaveError("invalid_manifest", "only one candidate per repository is allowed")
    if candidates != sorted(candidates, key=_candidate_order_key):
        raise IssueWaveError("invalid_manifest", "candidates are not deterministically ordered")
    if scope_conflicts(candidates):
        raise IssueWaveError("invalid_manifest", "candidate scopes mechanically overlap")
    return {"schema_version": MANIFEST_SCHEMA, "candidates": candidates}


def _state_root(workspace_root: Path | str, *, require_workspace: bool = True) -> Path:
    workspace = Path(workspace_root)
    if not workspace.is_absolute():
        raise IssueWaveError("unsafe_state_root", "workspace root must be absolute")
    try:
        resolved = workspace.resolve(strict=require_workspace)
    except OSError as error:
        raise IssueWaveError("unsafe_state_root", "workspace root cannot be resolved") from error
    if require_workspace and not resolved.is_dir():
        raise IssueWaveError("unsafe_state_root", "workspace root must be an existing directory")
    return resolved / ".codex" / "role-pool-runs"


def _initial_lane(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "lane_id": candidate["lane_id"],
        "repository": candidate["repository"],
        "issue": candidate["issue"],
        "issue_created_at": candidate["issue_created_at"],
        "priority_source": candidate["priority_source"],
        "eligibility_summary": candidate["evidence"]["summary"],
        "scope": deepcopy(candidate["scope"]),
        "checkout_location": candidate["target_root"],
        "worktree_location": None,
        "state": "selected",
        "active_role": None,
        "artifacts": [],
        "review_base_commit": None,
        "reviewed_package_sha256": None,
        "created_commit": None,
        "submitted_package_sha256": None,
        "branch": None,
        "draft_pr": None,
        "checks": None,
        "validation_summary": [],
        "stop_reason": None,
        "governance_packets": [],
    }


def _initial_state(
    run_id: str,
    timestamp: str,
    invocation: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": STATE_SCHEMA,
        "run_id": run_id,
        "created_at_utc": timestamp,
        "updated_at_utc": timestamp,
        "revision": 0,
        "last_event_digest": ZERO_DIGEST,
        "invocation": deepcopy(dict(invocation)),
        "candidates": deepcopy(manifest["candidates"]),
        "lanes": [_initial_lane(candidate) for candidate in manifest["candidates"]],
        "run_complete": False,
    }


def _atomic_write_json(path: Path, value: object) -> None:
    temporary = path.parent / f".{path.name}.{uuid.uuid4().hex}.tmp"
    payload = _canonical_json(value) + b"\n"
    descriptor: int | None = None
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | BINARY_FLAG,
            0o600,
        )
        _write_all(descriptor, payload)
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        os.replace(temporary, path)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _write_all(descriptor: int, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        written = os.write(descriptor, view)
        if written <= 0:
            raise OSError("write did not make progress")
        view = view[written:]


def _append_event(path: Path, event: Mapping[str, Any]) -> None:
    payload = _canonical_json(dict(event)) + b"\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_APPEND | BINARY_FLAG)
    try:
        _write_all(descriptor, payload)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _run_directory(workspace_root: Path | str, run_id: str) -> Path:
    if RUN_ID_RE.fullmatch(run_id) is None:
        raise IssueWaveError("state_not_found", "run identifier is invalid")
    root = _state_root(workspace_root)
    run_directory = root / run_id
    try:
        resolved = run_directory.resolve(strict=False)
        root_resolved = root.resolve(strict=False)
    except OSError as error:
        raise IssueWaveError("unsafe_state_root", "run path cannot be resolved") from error
    if resolved.parent != root_resolved:
        raise IssueWaveError("unsafe_state_root", "run path escapes the state root")
    return resolved


def _existing_run_conflict(root: Path, candidates: Sequence[Mapping[str, Any]]) -> bool:
    if not root.exists():
        return False
    requested = {(candidate["repository"], candidate["issue"]) for candidate in candidates}
    for child in root.iterdir():
        if not child.is_dir() or RUN_ID_RE.fullmatch(child.name) is None:
            continue
        state, _ = load_run_directory(child)
        existing = {(lane["repository"], lane["issue"]) for lane in state["lanes"]}
        if requested.intersection(existing):
            return True
    return False


@contextmanager
def _exclusive_admission_lock(root: Path) -> Iterator[None]:
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise IssueWaveError("state_integrity_error", "state root could not be created") from error
    lock_directory = root / ".admission.lock"
    try:
        lock_directory.mkdir()
    except FileExistsError as error:
        raise IssueWaveError("state_locked", "run admission is locked") from error
    except OSError as error:
        raise IssueWaveError("state_integrity_error", "run admission lock could not be created") from error

    owner_path = lock_directory / "owner"
    owner = secrets.token_hex(16).encode("ascii") + b"\n"
    try:
        descriptor = os.open(
            owner_path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | BINARY_FLAG,
            0o600,
        )
        try:
            _write_all(descriptor, owner)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except OSError as error:
        try:
            lock_directory.rmdir()
        except OSError:
            pass
        raise IssueWaveError("state_integrity_error", "run admission lock is invalid") from error

    try:
        yield
    finally:
        try:
            if owner_path.read_bytes() != owner:
                raise IssueWaveError("state_integrity_error", "run admission lock ownership changed")
            owner_path.unlink()
            lock_directory.rmdir()
        except IssueWaveError:
            raise
        except OSError as error:
            raise IssueWaveError("state_integrity_error", "run admission lock could not be released") from error


def _cleanup_owned_staging(staging: Path, identity: tuple[int, int] | None) -> None:
    if identity is None:
        return
    try:
        current = staging.stat()
    except OSError:
        return
    if (current.st_dev, current.st_ino) != identity:
        return
    try:
        children = list(staging.iterdir())
    except OSError:
        return
    if any(child.name not in {"events.jsonl", "run.json"} or not child.is_file() for child in children):
        return
    try:
        for child in children:
            child.unlink()
        staging.rmdir()
    except OSError:
        return


def init_run(
    workspace_root: Path | str,
    invocation_value: object,
    manifest_value: object,
    *,
    target_roots: Mapping[str, Path | str],
    run_id: str | None = None,
    now: datetime | None = None,
    entropy: bytes | None = None,
) -> tuple[Path, dict[str, Any]]:
    invocation = _validate_invocation_object(invocation_value)
    root = _state_root(workspace_root)
    manifest = validate_manifest(
        manifest_value,
        invocation,
        target_roots=target_roots,
        state_root=root,
    )
    selected_run_id = generate_run_id(now=now, entropy=entropy) if run_id is None else run_id
    if RUN_ID_RE.fullmatch(selected_run_id) is None:
        raise IssueWaveError("invalid_run_id", "run identifier is invalid")
    timestamp = _now_timestamp(now)
    state = _initial_state(selected_run_id, timestamp, invocation, manifest)
    run_directory = root / selected_run_id
    with _exclusive_admission_lock(root):
        if _existing_run_conflict(root, manifest["candidates"]):
            raise IssueWaveError("duplicate_active_lane", "a candidate already has a local run")
        if run_directory.exists():
            raise IssueWaveError("state_exists", "run already exists")
        staging = root / f".{selected_run_id}.init-{uuid.uuid4().hex}"
        staging_identity: tuple[int, int] | None = None
        try:
            staging.mkdir()
            staging_stat = staging.stat()
            staging_identity = (staging_stat.st_dev, staging_stat.st_ino)
            events_path = staging / "events.jsonl"
            descriptor = os.open(
                events_path,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | BINARY_FLAG,
                0o600,
            )
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            _atomic_write_json(staging / "run.json", state)
            os.rename(staging, run_directory)
        except OSError as error:
            _cleanup_owned_staging(staging, staging_identity)
            raise IssueWaveError("state_integrity_error", "run state could not be created") from error
    return run_directory, state


def _validate_governance_packet(
    value: object,
    *,
    run_id: str,
    lane: Mapping[str, Any],
) -> dict[str, Any]:
    packet = _exact_keys(
        value,
        GOVERNANCE_PACKET_KEYS,
        code="invalid_transition",
        label="governance packet",
    )
    if packet["schema_version"] != GOVERNANCE_PACKET_SCHEMA:
        raise IssueWaveError("invalid_transition", "governance packet schema is unsupported")
    if (
        packet["run_id"] != run_id
        or packet["lane_id"] != lane["lane_id"]
        or packet["repository"] != lane["repository"]
        or packet["issue"] != lane["issue"]
    ):
        raise IssueWaveError("invalid_transition", "governance packet binding is invalid")
    if packet["role"] not in {"A", "B", "C", "E", "F", "root"}:
        raise IssueWaveError("invalid_transition", "governance packet role is invalid")
    if packet["trigger_category"] not in GOVERNANCE_TRIGGERS:
        raise IssueWaveError("invalid_transition", "governance trigger is invalid")
    count = packet["repeated_pattern_count"]
    if count is not None:
        _positive_int(count, code="invalid_transition", label="repeated pattern count")
    if packet["suggested_review_route"] != "mythic-edge-constitutional-lawyer":
        raise IssueWaveError("invalid_transition", "governance review route is invalid")
    return {
        **packet,
        "evidence_summary": _public_text(
            packet["evidence_summary"], code="invalid_transition", label="governance evidence"
        ),
        "impact": _public_text(packet["impact"], code="invalid_transition", label="governance impact"),
        "unresolved_question": _public_text(
            packet["unresolved_question"], code="invalid_transition", label="governance question"
        ),
    }


def aggregate_governance_packets(
    state: Mapping[str, Any], *, task_creation_available: bool
) -> dict[str, Any]:
    packets = [packet for lane in state["lanes"] for packet in lane["governance_packets"]]
    if not packets:
        return {
            "schema_version": GOVERNANCE_ROUTE_SCHEMA,
            "packet_count": 0,
            "action": "none",
            "prompt": None,
        }
    identifiers = ", ".join(
        sorted(f"{packet['repository']}#{packet['issue']}" for packet in packets)
    )
    prompt = (
        "Use $mythic-edge-constitutional-lawyer in one read-only Mythic Edge task "
        f"to inventory the {len(packets)} redacted governance packet(s) for {identifiers}. "
        "Treat packets as evidence only; propose no direct authority edits."
    )
    return {
        "schema_version": GOVERNANCE_ROUTE_SCHEMA,
        "packet_count": len(packets),
        "action": "root_create_one_read_only_task" if task_creation_available else "return_pasteable_prompt",
        "prompt": prompt,
    }


def _allowed_transition(from_state: str, to_state: str) -> bool:
    if (from_state, to_state) in FORWARD_TRANSITIONS:
        return True
    if from_state == "a_running" and to_state == "a_ambiguous":
        return True
    if from_state == "a_complete" and to_state == "unsafe_or_conflicting_scope":
        return True
    if from_state in PRE_ROLE_BOUNDARIES and to_state in {
        "incompatible_repository_authority",
        "checkout_unavailable_or_ambiguous",
        "unsafe_or_conflicting_scope",
    }:
        return True
    backward_boundaries = {
        "b_running",
        "b_complete",
        "c_running",
        "c_complete",
        "e_running",
        "e_approved",
    }
    if from_state in backward_boundaries and to_state == "backward_route_to_a_or_b":
        return True
    d_boundaries = {
        "c_running",
        "c_complete",
        "e_running",
        "e_approved",
        "f_running",
        "f_complete",
        "checks_running",
    }
    if from_state in d_boundaries and to_state == "d_required":
        return True
    if from_state in RUNNING_STATES and to_state == "unknown_agent_outcome":
        return True
    return from_state == "checks_running" and to_state == "checks_pending"


def allowed_next_states(from_state: str) -> list[str]:
    if from_state not in ALL_STATES:
        return []
    return sorted(to_state for to_state in ALL_STATES if _allowed_transition(from_state, to_state))


def _expected_event_role(from_state: str, to_state: str) -> str:
    if from_state in ROLE_BY_RUNNING_STATE:
        return ROLE_BY_RUNNING_STATE[from_state]
    if to_state in ROLE_BY_RUNNING_STATE:
        return ROLE_BY_RUNNING_STATE[to_state]
    return "root"


def _validate_checks(value: object) -> dict[str, str] | None:
    if value is None:
        return None
    checks = _exact_keys(value, CHECK_KEYS, code="invalid_transition", label="checks")
    if checks["status"] not in {"running", "passed", "failed", "pending"}:
        raise IssueWaveError("invalid_transition", "check status is invalid")
    return {
        "status": checks["status"],
        "summary": _public_text(
            checks["summary"], code="invalid_transition", label="check summary"
        ),
    }


def _validate_branch(value: object) -> str | None:
    if value is None:
        return None
    if (
        not isinstance(value, str)
        or BRANCH_RE.fullmatch(value) is None
        or ".." in value
        or "//" in value
        or value.endswith(".lock")
    ):
        raise IssueWaveError("invalid_transition", "branch reference is invalid")
    return value


def _validate_updates(
    value: object,
    *,
    run_id: str,
    state: Mapping[str, Any],
    lane: Mapping[str, Any],
    run_directory: Path,
    require_existing_paths: bool,
) -> dict[str, Any]:
    if not isinstance(value, dict) or not set(value).issubset(UPDATE_KEYS):
        raise IssueWaveError("invalid_transition", "transition updates are invalid")
    updates: dict[str, Any] = {}
    if "scope" in value:
        updates["scope"] = _validate_scope(value["scope"], code="invalid_transition")
    if "worktree_location" in value:
        worktree = value["worktree_location"]
        if worktree is None:
            updates["worktree_location"] = None
        else:
            resolved = _resolved_directory(
                worktree,
                code="invalid_transition",
                require_exists=require_existing_paths,
            )
            proposed_state = deepcopy(dict(state))
            proposed_lane = next(
                item for item in proposed_state["lanes"] if item["lane_id"] == lane["lane_id"]
            )
            proposed_lane["worktree_location"] = str(resolved)
            _validate_state_path_isolation(
                proposed_state,
                run_directory,
                code="invalid_transition",
            )
            updates["worktree_location"] = str(resolved)
    if "artifacts" in value:
        updates["artifacts"] = _public_string_list(
            value["artifacts"], code="invalid_transition", label="artifact references"
        )
    for field in ("review_base_commit", "created_commit"):
        if field in value:
            commit = value[field]
            if not isinstance(commit, str) or COMMIT_RE.fullmatch(commit) is None:
                raise IssueWaveError("invalid_transition", "commit identity is invalid")
            updates[field] = commit
    for field in ("reviewed_package_sha256", "submitted_package_sha256"):
        if field in value:
            digest = value[field]
            if not isinstance(digest, str) or DIGEST_RE.fullmatch(digest) is None:
                raise IssueWaveError("invalid_transition", "package identity is invalid")
            updates[field] = digest
    if "branch" in value:
        updates["branch"] = _validate_branch(value["branch"])
    if "draft_pr" in value:
        draft_pr = value["draft_pr"]
        if draft_pr is not None:
            _positive_int(draft_pr, code="invalid_transition", label="draft PR")
        updates["draft_pr"] = draft_pr
    if "checks" in value:
        updates["checks"] = _validate_checks(value["checks"])
    if "validation_summary" in value:
        updates["validation_summary"] = _public_string_list(
            value["validation_summary"], code="invalid_transition", label="validation summary"
        )
    if "governance_packets" in value:
        packets = value["governance_packets"]
        if not isinstance(packets, list):
            raise IssueWaveError("invalid_transition", "governance packets must be a list")
        updates["governance_packets"] = [
            _validate_governance_packet(packet, run_id=run_id, lane=lane) for packet in packets
        ]
    return updates


def _validate_event_request(
    value: object,
    *,
    state: Mapping[str, Any],
    run_directory: Path,
    require_existing_paths: bool = True,
) -> dict[str, Any]:
    request = _exact_keys(
        value,
        EVENT_REQUEST_KEYS,
        code="invalid_transition",
        label="event request",
    )
    if request["schema_version"] != EVENT_REQUEST_SCHEMA:
        raise IssueWaveError("invalid_transition", "event request schema is unsupported")
    lane_id = request["lane_id"]
    lane = next((item for item in state["lanes"] if item["lane_id"] == lane_id), None)
    if lane is None:
        raise IssueWaveError("invalid_transition", "lane identifier is unknown")
    from_state = request["from_state"]
    to_state = request["to_state"]
    if from_state != lane["state"] or from_state not in ALL_STATES or to_state not in ALL_STATES:
        raise IssueWaveError("invalid_transition", "transition state binding is invalid")
    if not _allowed_transition(from_state, to_state):
        raise IssueWaveError("invalid_transition", "transition is not allowed")
    if request["role"] != _expected_event_role(from_state, to_state):
        raise IssueWaveError("invalid_transition", "transition role is invalid")
    return {
        "schema_version": EVENT_REQUEST_SCHEMA,
        "lane_id": lane_id,
        "from_state": from_state,
        "to_state": to_state,
        "role": request["role"],
        "reason": _public_text(request["reason"], code="invalid_transition", label="transition reason"),
        "evidence_summary": _public_text(
            request["evidence_summary"], code="invalid_transition", label="transition evidence"
        ),
        "updates": _validate_updates(
            request["updates"],
            run_id=state["run_id"],
            state=state,
            lane=lane,
            run_directory=run_directory,
            require_existing_paths=require_existing_paths,
        ),
    }


def _apply_event(state_value: Mapping[str, Any], event: Mapping[str, Any], run_directory: Path) -> dict[str, Any]:
    state = deepcopy(dict(state_value))
    request = {
        "schema_version": EVENT_REQUEST_SCHEMA,
        "lane_id": event["lane_id"],
        "from_state": event["from_state"],
        "to_state": event["to_state"],
        "role": event["role"],
        "reason": event["reason"],
        "evidence_summary": event["evidence_summary"],
        "updates": event["updates"],
    }
    validated = _validate_event_request(
        request,
        state=state,
        run_directory=run_directory,
        require_existing_paths=False,
    )
    lane = next(item for item in state["lanes"] if item["lane_id"] == validated["lane_id"])
    if "worktree_location" in validated["updates"] and (
        validated["from_state"] != "selected"
        or validated["to_state"] != "a_running"
        or lane["worktree_location"] is not None
        or validated["updates"]["worktree_location"] is None
    ):
        raise IssueWaveError("invalid_transition", "recorded worktree location is immutable")
    transition = (validated["from_state"], validated["to_state"])
    updates = validated["updates"]
    if transition == ("selected", "a_running"):
        if "branch" not in updates or updates["branch"] is None or lane["branch"] is not None:
            raise IssueWaveError(
                "invalid_transition", "A start requires one newly bound issue branch"
            )
    elif transition == ("f_running", "f_complete"):
        if "branch" not in updates:
            raise IssueWaveError(
                "invalid_transition", "F completion must reassert the bound issue branch"
            )
        if lane["branch"] is None or updates["branch"] != lane["branch"]:
            raise IssueWaveError(
                "invalid_transition", "F completion branch does not match the bound issue branch"
            )
    elif "branch" in updates:
        raise IssueWaveError("invalid_transition", "branch update is not allowed here")

    if transition == ("f_running", "f_complete"):
        if lane["draft_pr"] is not None:
            raise IssueWaveError("invalid_transition", "draft PR identity is immutable")
        if "draft_pr" not in updates or updates["draft_pr"] is None:
            raise IssueWaveError(
                "invalid_transition", "F completion requires a newly recorded positive draft PR"
            )
    elif "draft_pr" in updates:
        raise IssueWaveError("invalid_transition", "draft PR update is not allowed here")

    required_check_status = {
        ("f_complete", "checks_running"): "running",
        ("checks_running", "g_consideration_ready"): "passed",
        ("checks_running", "d_required"): "failed",
        ("checks_running", "checks_pending"): "pending",
    }.get(transition)
    if required_check_status is None:
        if "checks" in updates:
            raise IssueWaveError("invalid_transition", "check evidence update is not allowed here")
    elif "checks" not in updates or updates["checks"] is None:
        raise IssueWaveError(
            "invalid_transition", "this checks transition requires new check evidence"
        )
    elif updates["checks"]["status"] != required_check_status:
        raise IssueWaveError(
            "invalid_transition", "check evidence does not match the checks transition"
        )
    identity_updates = set(validated["updates"]).intersection(
        {
            "review_base_commit",
            "reviewed_package_sha256",
            "created_commit",
            "submitted_package_sha256",
        }
    )
    if validated["to_state"] == "e_approved":
        if identity_updates != {"review_base_commit", "reviewed_package_sha256"}:
            raise IssueWaveError(
                "invalid_transition", "E approval requires the complete reviewed package identity"
            )
        if any(
            lane[field] is not None
            for field in (
                "review_base_commit",
                "reviewed_package_sha256",
                "created_commit",
                "submitted_package_sha256",
            )
        ):
            raise IssueWaveError("invalid_transition", "reviewed package identity is immutable")
    elif validated["to_state"] == "f_complete":
        if identity_updates != {"created_commit", "submitted_package_sha256"}:
            raise IssueWaveError(
                "invalid_transition", "F completion requires the complete submitted package identity"
            )
        if lane["created_commit"] is not None or lane["submitted_package_sha256"] is not None:
            raise IssueWaveError("invalid_transition", "submitted package identity is immutable")
        if validated["updates"]["submitted_package_sha256"] != lane["reviewed_package_sha256"]:
            raise IssueWaveError(
                "invalid_transition", "submitted package identity does not match E approval"
            )
    elif identity_updates:
        raise IssueWaveError("invalid_transition", "package identity update is not allowed here")
    lane.update(deepcopy(validated["updates"]))
    _validate_state_path_isolation(state, run_directory, code="invalid_transition")
    lane["state"] = validated["to_state"]
    lane["active_role"] = ROLE_BY_RUNNING_STATE.get(validated["to_state"])
    lane["stop_reason"] = validated["to_state"] if validated["to_state"] in STOP_STATES else None

    if validated["to_state"] == "a_running" and lane["worktree_location"] is None:
        raise IssueWaveError("invalid_transition", "A cannot start without an isolated worktree and branch")
    if validated["to_state"] == "a_complete" and not lane["artifacts"]:
        raise IssueWaveError("invalid_transition", "A completion requires a durable artifact")
    if validated["to_state"] == "a_scope_verified":
        continuing = [item for item in state["lanes"] if item["state"] not in FINAL_STATES]
        if scope_conflicts(continuing):
            raise IssueWaveError("invalid_transition", "post-A scopes mechanically overlap")
    if validated["to_state"] in {"b_complete", "c_complete"} and not lane["artifacts"]:
        raise IssueWaveError("invalid_transition", "role completion requires durable artifacts")
    if validated["to_state"] == "c_complete" and not lane["validation_summary"]:
        raise IssueWaveError("invalid_transition", "C completion requires validation evidence")
    if validated["to_state"] == "e_approved" and (
        lane["review_base_commit"] is None
        or lane["reviewed_package_sha256"] is None
        or not lane["validation_summary"]
    ):
        raise IssueWaveError(
            "invalid_transition", "E approval requires reviewed package and validation evidence"
        )
    if validated["to_state"] == "f_complete" and (
        lane["branch"] is None
        or lane["draft_pr"] is None
        or lane["created_commit"] is None
        or lane["submitted_package_sha256"] != lane["reviewed_package_sha256"]
    ):
        raise IssueWaveError(
            "invalid_transition", "F completion requires matching submitted package evidence"
        )
    if validated["to_state"] == "checks_running" and (
        lane["checks"] is None or lane["checks"]["status"] != "running"
    ):
        raise IssueWaveError("invalid_transition", "check polling requires running check evidence")
    if validated["to_state"] == "g_consideration_ready" and (
        lane["checks"] is None or lane["checks"]["status"] != "passed"
    ):
        raise IssueWaveError("invalid_transition", "G consideration requires passing check evidence")
    if validated["to_state"] == "checks_pending" and (
        lane["checks"] is None or lane["checks"]["status"] != "pending"
    ):
        raise IssueWaveError("invalid_transition", "checks_pending requires pending check evidence")
    if validated["to_state"] == "d_required" and validated["from_state"] == "checks_running" and (
        lane["checks"] is None or lane["checks"]["status"] != "failed"
    ):
        raise IssueWaveError("invalid_transition", "CI failure requires failing check evidence")

    state["revision"] = event["sequence"]
    state["updated_at_utc"] = event["timestamp_utc"]
    state["last_event_digest"] = event["event_digest"]
    state["run_complete"] = all(item["state"] in FINAL_STATES for item in state["lanes"])
    return state


def _validate_event(value: object, *, expected_sequence: int, previous_digest: str) -> dict[str, Any]:
    event = _exact_keys(value, EVENT_KEYS, code="state_integrity_error", label="event")
    if event["schema_version"] != EVENT_SCHEMA or event["sequence"] != expected_sequence:
        raise IssueWaveError("state_integrity_error", "event sequence or schema is invalid")
    _timestamp(event["timestamp_utc"], code="state_integrity_error", label="event timestamp")
    if event["previous_event_digest"] != previous_digest:
        raise IssueWaveError("state_integrity_error", "event hash chain is broken")
    digest = event["event_digest"]
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise IssueWaveError("state_integrity_error", "event digest is invalid")
    payload = {key: event[key] for key in sorted(EVENT_KEYS) if key != "event_digest"}
    expected_digest = hashlib.sha256(_canonical_json(payload)).hexdigest()
    if digest != expected_digest:
        raise IssueWaveError("state_integrity_error", "event digest does not match")
    return event


def _read_canonical_json(path: Path, *, label: str) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise IssueWaveError("state_not_found", f"{label} is unavailable") from error
    value = strict_json_loads(raw)
    if not isinstance(value, dict) or raw != _canonical_json(value) + b"\n":
        raise IssueWaveError("state_integrity_error", f"{label} is not canonical")
    return value


def _read_events(path: Path) -> list[dict[str, Any]]:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise IssueWaveError("state_not_found", "event ledger is unavailable") from error
    if raw and not raw.endswith(b"\n"):
        raise IssueWaveError("state_integrity_error", "event ledger has an invalid tail")
    events: list[dict[str, Any]] = []
    previous_digest = ZERO_DIGEST
    for sequence, raw_line in enumerate(raw.splitlines(keepends=True), start=1):
        if not raw_line.endswith(b"\n"):
            raise IssueWaveError("state_integrity_error", "event ledger has an invalid tail")
        value = strict_json_loads(raw_line[:-1])
        event = _validate_event(value, expected_sequence=sequence, previous_digest=previous_digest)
        if raw_line != _canonical_json(event) + b"\n":
            raise IssueWaveError("state_integrity_error", "event ledger is not canonical")
        events.append(event)
        previous_digest = event["event_digest"]
    return events


def _validate_loaded_state(value: object, run_directory: Path) -> dict[str, Any]:
    state = _exact_keys(value, STATE_KEYS, code="state_integrity_error", label="run state")
    if state["schema_version"] != STATE_SCHEMA or state["run_id"] != run_directory.name:
        raise IssueWaveError("state_integrity_error", "run state binding is invalid")
    created = _timestamp(state["created_at_utc"], code="state_integrity_error", label="created time")
    _timestamp(state["updated_at_utc"], code="state_integrity_error", label="updated time")
    if type(state["revision"]) is not int or state["revision"] < 0:
        raise IssueWaveError("state_integrity_error", "run revision is invalid")
    if not isinstance(state["last_event_digest"], str) or re.fullmatch(
        r"[0-9a-f]{64}", state["last_event_digest"]
    ) is None:
        raise IssueWaveError("state_integrity_error", "run event digest is invalid")
    _bool(state["run_complete"], code="state_integrity_error", label="run completion")
    invocation = _validate_invocation_object(state["invocation"])
    if invocation["mode"] != "Dispatch" or invocation["selectors"]["run_id"] is not None:
        raise IssueWaveError("state_integrity_error", "saved invocation is invalid")
    target_roots = {
        candidate["repository"]: candidate["target_root"]
        for candidate in state["candidates"]
        if isinstance(candidate, dict) and "repository" in candidate and "target_root" in candidate
    }
    try:
        manifest = validate_manifest(
            {"schema_version": MANIFEST_SCHEMA, "candidates": state["candidates"]},
            invocation,
            target_roots=target_roots,
            state_root=run_directory.parent,
            require_existing_roots=False,
        )
    except IssueWaveError as error:
        raise IssueWaveError(
            "state_integrity_error", "saved candidate path isolation is invalid"
        ) from error
    initial = _initial_state(state["run_id"], created, invocation, manifest)
    _validate_state_path_isolation(initial, run_directory, code="state_integrity_error")
    if not isinstance(state["lanes"], list) or len(state["lanes"]) != len(initial["lanes"]):
        raise IssueWaveError("state_integrity_error", "lane projection is invalid")
    for lane in state["lanes"]:
        _exact_keys(lane, LANE_KEYS, code="state_integrity_error", label="lane projection")
    return initial


def load_run_directory(run_directory: Path) -> tuple[dict[str, Any], bool]:
    if not run_directory.exists() or not run_directory.is_dir():
        raise IssueWaveError("state_not_found", "run is unavailable")
    loaded = _read_canonical_json(run_directory / "run.json", label="run state")
    initial = _validate_loaded_state(loaded, run_directory)
    events = _read_events(run_directory / "events.jsonl")
    if loaded["revision"] > len(events) or len(events) - loaded["revision"] > 1:
        raise IssueWaveError("state_integrity_error", "run projection and event ledger disagree")

    projection = initial
    expected_at_loaded_revision = deepcopy(initial)
    for event in events:
        try:
            projection = _apply_event(projection, event, run_directory)
        except IssueWaveError as error:
            raise IssueWaveError(
                "state_integrity_error", "event replay violates run-state integrity"
            ) from error
        if event["sequence"] == loaded["revision"]:
            expected_at_loaded_revision = deepcopy(projection)
    if loaded != expected_at_loaded_revision:
        raise IssueWaveError("state_integrity_error", "run projection does not match its event ledger")
    return projection, len(events) == loaded["revision"] + 1


def load_run(workspace_root: Path | str, run_id: str) -> tuple[Path, dict[str, Any], bool]:
    run_directory = _run_directory(workspace_root, run_id)
    state, recovered = load_run_directory(run_directory)
    return run_directory, state, recovered


@contextmanager
def _exclusive_run_lock(run_directory: Path) -> Iterator[None]:
    lock_path = run_directory / ".transition.lock"
    try:
        descriptor = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise IssueWaveError("state_locked", "run state is locked") from error
    try:
        os.write(descriptor, b"locked\n")
        os.fsync(descriptor)
        os.close(descriptor)
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def transition_run(
    workspace_root: Path | str,
    run_id: str,
    *,
    expected_revision: int,
    request_value: object,
    now: datetime | None = None,
) -> dict[str, Any]:
    run_directory = _run_directory(workspace_root, run_id)
    with _exclusive_run_lock(run_directory):
        state, _ = load_run_directory(run_directory)
        if type(expected_revision) is not int or expected_revision != state["revision"]:
            raise IssueWaveError("stale_revision", "expected revision does not match current state")
        request = _validate_event_request(request_value, state=state, run_directory=run_directory)
        timestamp = _now_timestamp(now)
        if timestamp < state["updated_at_utc"]:
            raise IssueWaveError("invalid_time", "transition time precedes current state")
        event_without_digest = {
            "schema_version": EVENT_SCHEMA,
            "sequence": state["revision"] + 1,
            "timestamp_utc": timestamp,
            "lane_id": request["lane_id"],
            "from_state": request["from_state"],
            "to_state": request["to_state"],
            "role": request["role"],
            "reason": request["reason"],
            "evidence_summary": request["evidence_summary"],
            "updates": request["updates"],
            "previous_event_digest": state["last_event_digest"],
        }
        event = {
            **event_without_digest,
            "event_digest": hashlib.sha256(_canonical_json(event_without_digest)).hexdigest(),
        }
        next_state = _apply_event(state, event, run_directory)
        try:
            _append_event(run_directory / "events.jsonl", event)
        except OSError as error:
            raise IssueWaveError(
                "state_integrity_error",
                "transition event could not be recorded",
            ) from error
        try:
            _atomic_write_json(run_directory / "run.json", next_state)
        except OSError as error:
            raise IssueWaveError(
                "state_integrity_error",
                "projection update failed after the event was recorded",
            ) from error
        return next_state


def inspect_projection(state: Mapping[str, Any], *, recovered_projection: bool) -> dict[str, Any]:
    lanes = []
    for lane in state["lanes"]:
        lanes.append(
            {
                key: deepcopy(value)
                for key, value in lane.items()
                if key not in {"checkout_location", "worktree_location"}
            }
            | {
                "local_paths_redacted": True,
                "mechanically_allowed_next_states": allowed_next_states(lane["state"]),
            }
        )
    return {
        "schema_version": INSPECT_SCHEMA,
        "run_id": state["run_id"],
        "created_at_utc": state["created_at_utc"],
        "updated_at_utc": state["updated_at_utc"],
        "revision": state["revision"],
        "recovered_projection_in_memory": recovered_projection,
        "invocation": deepcopy(state["invocation"]),
        "lanes": lanes,
        "run_complete": state["run_complete"],
        "governance": aggregate_governance_packets(state, task_creation_available=False),
    }


def _read_json_argument(path_value: str) -> object:
    try:
        return strict_json_loads(Path(path_value).read_bytes())
    except OSError as error:
        raise IssueWaveError("invalid_json", "JSON input file is unavailable") from error


def _target_root_arguments(values: Sequence[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise IssueWaveError("invalid_command", "target root arguments are invalid")
        repository, path = value.split("=", 1)
        canonical = _canonical_repository(repository, code="invalid_command")
        if canonical in result or not path:
            raise IssueWaveError("invalid_command", "target root arguments are invalid")
        result[canonical] = path
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = SafeArgumentParser(description="Validate Mythic Edge issue-wave invocations and local state.")
    subparsers = parser.add_subparsers(dest="operation", required=True, parser_class=SafeArgumentParser)

    parse_parser = subparsers.add_parser("parse")
    parse_parser.add_argument("invocation")

    bind_parser = subparsers.add_parser("bind-package")
    bind_parser.add_argument("--manifest", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("invocation")
    init_parser.add_argument("--manifest", required=True)
    init_parser.add_argument("--workspace-root", required=True)
    init_parser.add_argument("--target-root", action="append", default=[], required=True)
    init_parser.add_argument("--run-id")

    transition_parser = subparsers.add_parser("transition")
    transition_parser.add_argument("--workspace-root", required=True)
    transition_parser.add_argument("--run", required=True)
    transition_parser.add_argument("--expected-revision", required=True, type=int)
    transition_parser.add_argument("--event", required=True)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--workspace-root", required=True)
    inspect_parser.add_argument("--run", required=True)
    inspect_parser.add_argument("--invocation")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(list(sys.argv[1:] if argv is None else argv))
        if args.operation == "parse":
            output = parse_invocation(args.invocation)
        elif args.operation == "bind-package":
            output = bind_reviewed_package(_read_json_argument(args.manifest))
        elif args.operation == "init":
            invocation = parse_invocation(args.invocation)
            _, state = init_run(
                args.workspace_root,
                invocation,
                _read_json_argument(args.manifest),
                target_roots=_target_root_arguments(args.target_root),
                run_id=args.run_id,
            )
            output = {"schema_version": STATE_SCHEMA, "run_id": state["run_id"], "revision": 0}
        elif args.operation == "transition":
            state = transition_run(
                args.workspace_root,
                args.run,
                expected_revision=args.expected_revision,
                request_value=_read_json_argument(args.event),
            )
            output = inspect_projection(state, recovered_projection=False)
        else:
            _, state, recovered = load_run(args.workspace_root, args.run)
            if args.invocation is not None:
                validate_resume_invocation(parse_invocation(args.invocation), state)
            output = inspect_projection(state, recovered_projection=recovered)
        print((_canonical_json(output) + b"\n").decode("utf-8"), end="")
        return 0
    except IssueWaveError as error:
        print(
            (_canonical_json({"error": {"code": error.code, "message": error.message}}) + b"\n").decode("utf-8"),
            end="",
            file=sys.stderr,
        )
        return {
            "invalid_invocation": 2,
            "invalid_command": 2,
            "invalid_json": 2,
            "invalid_reviewed_package": 3,
            "invalid_manifest": 3,
            "invalid_transition": 3,
            "permission_drift": 3,
            "stale_revision": 3,
            "duplicate_active_lane": 3,
            "unsafe_state_root": 4,
            "state_integrity_error": 4,
            "state_not_found": 4,
            "state_exists": 4,
            "state_locked": 5,
        }.get(error.code, 4)


if __name__ == "__main__":
    raise SystemExit(run())
