"""Inert direct-task adapter for the trusted-owner Role Pool.

The module owns only deterministic protocol construction and an injected
synthetic-client state machine.  It does not import or expose a real Codex app
connector and cannot create a real task, worktree, process, or durable record.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
import unicodedata
from datetime import datetime, timezone
from typing import Mapping, Protocol

PROFILE_CONTRACT_SHA256 = "8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952"
COMPANION_CONTRACT_SHA256 = "00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4"
PUBLIC_LAUNCHER_ID = "codex:native-task-create/v1"
APP_NATIVE_DIRECT_ADAPTER_ID = "codex:app-native-task-direct/v1"

OPERATION_BINDING_SCHEMA = "trusted_owner_app_native_operation_binding.v1"
TARGET_READBACK_SCHEMA = "trusted_owner_app_native_target_readback.v1"
TERMINAL_READBACK_SCHEMA = "trusted_owner_app_native_terminal_readback.v1"
PLATFORM_RECEIPT_SCHEMA = "trusted_owner_app_native_direct_platform_receipt.v1"
DEFAULT_OBSERVATION_DEADLINE_SECONDS = 5400

TASK_REQUEST_FIELDS = (
    "schema_version",
    "request_sha256",
    "claim_observation_sha256",
    "lane_packet_sha256",
    "repository_id",
    "issue_url",
    "role",
    "base_sha",
    "worktree_observation_sha256",
    "context_mode",
    "fork_turns",
    "issued_at_utc",
    "task_request_sha256",
)
LANE_PACKET_FIELDS = (
    "lane_id",
    "repository_id",
    "canonical_name",
    "issue_url",
    "role",
    "operation_id",
    "base_ref",
    "base_sha",
    "predecessor_packet_sha256",
    "command_ids",
    "read_scope",
    "mutation_scope",
    "protected_surfaces",
    "validation_command_ids",
    "expected_artifact_paths",
    "stop_conditions",
    "lane_packet_sha256",
)
OPERATION_BINDING_FIELDS = (
    "schema_version",
    "task_request_sha256",
    "request_sha256",
    "claim_observation_sha256",
    "lane_packet_sha256",
    "repository_id",
    "issue_url",
    "role",
    "lane_operation_id",
    "base_sha",
    "project_identity_sha256",
    "pre_worktree_observation_sha256",
)
TARGET_READBACK_FIELDS = (
    "schema_version",
    "task_identity_sha256",
    "project_identity_sha256",
    "repository_id",
    "worktree_observation_sha256",
    "base_sha",
    "app_task_operation_id",
)
TERMINAL_READBACK_FIELDS = (
    "schema_version",
    "app_task_operation_id",
    "task_identity_sha256",
    "terminal_status",
    "task_target_readback_sha256",
    "read_at_utc",
)
PLATFORM_RECEIPT_FIELDS = (
    "schema_version",
    "app_task_operation_id",
    "task_request_sha256",
    "claim_observation_sha256",
    "lane_packet_sha256",
    "canonical_prompt_sha256",
    "create_call_count",
    "returned_identifier_kind",
    "task_identity_sha256",
    "project_identity_sha256",
    "repository_id",
    "pre_worktree_observation_sha256",
    "task_target_readback_sha256",
    "accepted_at_utc",
    "terminal_status",
    "terminal_readback_sha256",
    "typed_handoff_sha256",
    "post_worktree_observation_sha256",
    "automatic_retry_count",
    "replacement_task_count",
    "follow_up_message_count",
    "observation_deadline_seconds",
    "reconciliation_status",
    "platform_receipt_sha256",
)
TASK_RECEIPT_FIELDS = (
    "schema_version",
    "task_request_sha256",
    "task_id",
    "accepted_at_utc",
    "platform_receipt_ref",
    "platform_receipt_sha256",
    "task_receipt_sha256",
)
HANDOFF_FIELDS = (
    "status",
    "next_role",
    "source_artifact_paths",
    "finding_ids",
    "stop_reason",
    "handoff_sha256",
)
THREAD_LIST_FIELDS = ("threads",)
THREAD_LIST_ENTRY_FIELDS = (
    "threadId",
    "clientThreadId",
    "projectId",
    "operationId",
)
THREAD_READBACK_FIELDS = (
    "threadId",
    "projectId",
    "repositoryId",
    "worktreeObservationSha256",
    "branchRef",
    "baseSha",
    "operationId",
    "status",
    "handoffs",
    "postWorktreeObservationSha256",
    "effectCounts",
)
EFFECT_COUNT_FIELDS = (
    "tracked_modification_count",
    "staged_modification_count",
    "untracked_file_count",
    "new_commit_count",
    "push_count",
    "issue_write_count",
    "pr_write_count",
    "registry_mutation_count",
    "release_mutation_count",
    "installation_mutation_count",
    "external_mutation_count",
)

TERMINAL_STATUSES = {"completed", "failed", "interrupted"}
NONTERMINAL_STATUSES = {"running", "queued", "inProgress", "pending"}
PUBLIC_STATUS_VALUES = TERMINAL_STATUSES | {
    "running",
    "unavailable",
    "conflicting",
    "unknown",
}
RETURNED_IDENTIFIER_KINDS = {
    "thread_id",
    "client_thread_id_resolved",
    "ambiguous_submission_reconciled",
}
RECONCILIATION_STATUSES = {
    "not_required",
    "required_same_task",
    "resolved_same_task_terminal",
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._:-]{0,127}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
DEADLINE_RE = re.compile(r"^app_native_observation_deadline_seconds:([1-9][0-9]*)$")

TERMINAL_READBACK_KAT_SHA256 = (
    "09a3d716d4f14baf67ebc5b4914b7e4daea24d8fd4c5376924859b5885a76e45"
)
PLATFORM_RECEIPT_KAT_SELF_SHA256 = (
    "c0af9c0be3cd43c4a1db80e1b525749d6c91cb2c8dc057e193c3badf17327918"
)
PLATFORM_RECEIPT_KAT_ARTIFACT_SHA256 = (
    "5df194e378dad42d515879fff05c671da3c4852394c2cbb87a3564ef9c33b0e4"
)


class AppNativeDirectAdapterError(ValueError):
    """Symbolic, no-echo direct-adapter refusal."""

    def __init__(self, code: str, *, profile_projection: str | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.profile_projection = profile_projection


class AmbiguousCreateOutcome(AppNativeDirectAdapterError):
    """Synthetic signal that submission may have occurred without a response."""


class KnownCreateRejection(AppNativeDirectAdapterError):
    """Synthetic signal for a directly known rejected create call."""


class InertAppNativeClient(Protocol):
    """Closed fake-client interface. Real connector implementations are rejected."""

    synthetic_only: bool

    def create_thread(self, *, target: Mapping[str, object], prompt: str) -> object: ...

    def list_threads(self) -> object: ...

    def read_thread(self, thread_id: str) -> object: ...


class _CallGuard:
    def __init__(self) -> None:
        self.state = "not_entered"

    def enter(self) -> None:
        if self.state != "not_entered":
            raise AppNativeDirectAdapterError("create_call_already_entered")
        self.state = "entered_once"


def _reject_duplicate_key(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AppNativeDirectAdapterError("duplicate_json_key")
        result[key] = value
    return result


def _is_nfc(value: object) -> bool:
    if isinstance(value, str):
        return value == unicodedata.normalize("NFC", value)
    if isinstance(value, Mapping):
        return all(_is_nfc(key) and _is_nfc(item) for key, item in value.items())
    if isinstance(value, list):
        return all(_is_nfc(item) for item in value)
    return True


def canonical_json_bytes(value: object, *, final_lf: bool = True) -> bytes:
    if not _is_nfc(value):
        raise AppNativeDirectAdapterError("non_nfc_value")
    encoded = json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return encoded + (b"\n" if final_lf else b"")


def canonical_sha256(value: object, *, final_lf: bool = True) -> str:
    return hashlib.sha256(canonical_json_bytes(value, final_lf=final_lf)).hexdigest()


def _self_digest(value: Mapping[str, object], digest_field: str) -> str:
    return canonical_sha256(
        {key: item for key, item in value.items() if key != digest_field}
    )


def with_self_digest(
    value: Mapping[str, object],
    digest_field: str,
) -> dict[str, object]:
    result = dict(value)
    result[digest_field] = _self_digest(result, digest_field)
    return result


def parse_canonical_json_line(
    value: object,
    *,
    fields: tuple[str, ...] | None = None,
) -> dict[str, object]:
    if not isinstance(value, (bytes, bytearray)):
        raise AppNativeDirectAdapterError("canonical_bytes_required")
    raw = bytes(value)
    if (
        raw.startswith(b"\xef\xbb\xbf")
        or not raw.endswith(b"\n")
        or raw.endswith(b"\n\n")
        or b"\r" in raw
        or b"\n" in raw[:-1]
    ):
        raise AppNativeDirectAdapterError("canonical_framing_invalid")
    try:
        document = json.loads(
            raw[:-1].decode("utf-8", errors="strict"),
            object_pairs_hook=_reject_duplicate_key,
        )
    except AppNativeDirectAdapterError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AppNativeDirectAdapterError("canonical_json_invalid") from exc
    if not isinstance(document, dict):
        raise AppNativeDirectAdapterError("canonical_object_required")
    if fields is not None and tuple(document) != fields:
        raise AppNativeDirectAdapterError("canonical_fields_invalid")
    if canonical_json_bytes(document) != raw:
        raise AppNativeDirectAdapterError("canonical_bytes_invalid")
    return document


def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _is_git_sha(value: object) -> bool:
    return isinstance(value, str) and GIT_SHA_RE.fullmatch(value) is not None


def _is_id(value: object) -> bool:
    return isinstance(value, str) and ID_RE.fullmatch(value) is not None


def _is_nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value) and "\x00" not in value and _is_nfc(value)


def _is_positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_nonnegative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_utc_second(value: object) -> bool:
    if not isinstance(value, str) or UTC_RE.fullmatch(value) is None:
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def _utc_now(clock: object = None) -> str:
    now = clock() if callable(clock) else datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise AppNativeDirectAdapterError("clock_invalid")
    return now.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _monotonic_now(clock: object = None) -> float:
    if clock is None:
        value = time.monotonic()
    elif callable(clock):
        value = clock()
    else:
        raise AppNativeDirectAdapterError("monotonic_clock_invalid")
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
    ):
        raise AppNativeDirectAdapterError("monotonic_clock_invalid")
    return float(value)


def _strict_mapping(
    value: object,
    fields: tuple[str, ...],
    code: str,
) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or tuple(value) != fields:
        raise AppNativeDirectAdapterError(code)
    return value


def _domain_digest(domain: str, value: str) -> str:
    return hashlib.sha256(domain.encode("ascii") + b"\x00" + value.encode("utf-8")).hexdigest()


def project_identity_sha256(project_id: object) -> str:
    if not _is_nonempty_text(project_id):
        raise AppNativeDirectAdapterError("project_identity_invalid")
    return _domain_digest("app_native_project", str(project_id))


def task_identity_sha256(thread_id: object) -> str:
    if not _is_id(thread_id):
        raise AppNativeDirectAdapterError("task_identity_invalid")
    return _domain_digest("app_native_thread", str(thread_id))


def _validate_task_request(value: object) -> Mapping[str, object]:
    request = _strict_mapping(value, TASK_REQUEST_FIELDS, "task_request_fields_invalid")
    if request["schema_version"] != "trusted_owner_native_task_request.v1":
        raise AppNativeDirectAdapterError("task_request_schema_invalid")
    for field in (
        "request_sha256",
        "claim_observation_sha256",
        "lane_packet_sha256",
        "worktree_observation_sha256",
        "task_request_sha256",
    ):
        if not _is_sha256(request[field]):
            raise AppNativeDirectAdapterError(f"{field}_invalid")
    if request["task_request_sha256"] != _self_digest(request, "task_request_sha256"):
        raise AppNativeDirectAdapterError("task_request_digest_invalid")
    if not _is_positive_int(request["repository_id"]):
        raise AppNativeDirectAdapterError("repository_id_invalid")
    if not _is_nonempty_text(request["issue_url"]):
        raise AppNativeDirectAdapterError("issue_url_invalid")
    if request["role"] not in {"B", "E"}:
        raise AppNativeDirectAdapterError("role_not_admitted")
    if not _is_git_sha(request["base_sha"]):
        raise AppNativeDirectAdapterError("base_sha_invalid")
    if request["context_mode"] != "isolated_packet_only" or request["fork_turns"] != "none":
        raise AppNativeDirectAdapterError("context_boundary_invalid")
    if not _is_utc_second(request["issued_at_utc"]):
        raise AppNativeDirectAdapterError("issued_at_utc_invalid")
    return request


def _validate_lane(value: object) -> Mapping[str, object]:
    lane = _strict_mapping(value, LANE_PACKET_FIELDS, "lane_packet_fields_invalid")
    for field in ("lane_id", "canonical_name", "issue_url", "base_ref"):
        if not _is_nonempty_text(lane[field]):
            raise AppNativeDirectAdapterError(f"lane_{field}_invalid")
    if not _is_positive_int(lane["repository_id"]):
        raise AppNativeDirectAdapterError("lane_repository_id_invalid")
    if lane["role"] not in {"B", "E"}:
        raise AppNativeDirectAdapterError("lane_role_not_admitted")
    if lane["operation_id"] != "inspect":
        raise AppNativeDirectAdapterError("lane_operation_invalid")
    if not _is_git_sha(lane["base_sha"]):
        raise AppNativeDirectAdapterError("lane_base_sha_invalid")
    predecessor = lane["predecessor_packet_sha256"]
    if predecessor is not None and not _is_sha256(predecessor):
        raise AppNativeDirectAdapterError("lane_predecessor_invalid")
    for field in (
        "command_ids",
        "read_scope",
        "mutation_scope",
        "protected_surfaces",
        "validation_command_ids",
        "expected_artifact_paths",
        "stop_conditions",
    ):
        if not isinstance(lane[field], list) or not all(
            _is_nonempty_text(item) for item in lane[field]
        ):
            raise AppNativeDirectAdapterError(f"lane_{field}_invalid")
    for field in (
        "command_ids",
        "validation_command_ids",
        "mutation_scope",
        "expected_artifact_paths",
    ):
        if lane[field] != []:
            raise AppNativeDirectAdapterError(f"lane_{field}_must_be_empty")
    if not lane["read_scope"]:
        raise AppNativeDirectAdapterError("lane_read_scope_required")
    if lane["lane_packet_sha256"] != _self_digest(lane, "lane_packet_sha256"):
        raise AppNativeDirectAdapterError("lane_packet_digest_invalid")
    return lane


def _scope_is_within(requested: list[object], permitted: list[object]) -> bool:
    return all(
        isinstance(path, str)
        and any(path == root or path.startswith(f"{root}/") for root in permitted)
        for path in requested
    )


def validate_direct_request_boundary(
    *,
    task_request: object,
    lane_packet: object,
    registry_entry: object,
) -> list[str]:
    try:
        request = _validate_task_request(task_request)
        lane = _validate_lane(lane_packet)
        if not isinstance(registry_entry, Mapping):
            raise AppNativeDirectAdapterError("registry_entry_invalid")
        for field in ("repository_id", "repository_code_execution_policy"):
            if field not in registry_entry:
                raise AppNativeDirectAdapterError("registry_entry_invalid")
        if registry_entry["repository_id"] != request["repository_id"]:
            raise AppNativeDirectAdapterError("registry_repository_mismatch")
        if registry_entry["repository_code_execution_policy"] != "forbidden":
            raise AppNativeDirectAdapterError("registry_execution_policy_invalid")
        if registry_entry.get("maximum_mutation_scope") != []:
            raise AppNativeDirectAdapterError("registry_mutation_scope_invalid")
        if registry_entry.get("approved_commands") != []:
            raise AppNativeDirectAdapterError("registry_commands_invalid")
        if request["role"] not in registry_entry.get("eligible_roles", []):
            raise AppNativeDirectAdapterError("registry_role_invalid")
        if lane["operation_id"] not in registry_entry.get("permitted_operations", []):
            raise AppNativeDirectAdapterError("registry_operation_invalid")
        permitted_scope = registry_entry.get("permitted_read_scope")
        if not isinstance(permitted_scope, list) or not _scope_is_within(
            list(lane["read_scope"]), permitted_scope
        ):
            raise AppNativeDirectAdapterError("registry_read_scope_invalid")
        bindings = (
            "lane_packet_sha256",
            "repository_id",
            "issue_url",
            "role",
            "base_sha",
        )
        if any(request[field] != lane[field] for field in bindings):
            raise AppNativeDirectAdapterError("request_lane_binding_mismatch")
    except AppNativeDirectAdapterError as exc:
        return [exc.code]
    return []


def validate_first_r2_request(
    *,
    task_request: object,
    lane_packet: object,
    registry_entry: object,
) -> list[str]:
    errors = validate_direct_request_boundary(
        task_request=task_request,
        lane_packet=lane_packet,
        registry_entry=registry_entry,
    )
    if errors:
        return errors
    assert isinstance(task_request, Mapping)
    return [] if task_request["role"] == "E" else ["first_r2_role_not_admitted"]


def observation_deadline_seconds(lane_packet: object) -> int:
    lane = _validate_lane(lane_packet)
    candidates = [
        item
        for item in lane["stop_conditions"]
        if isinstance(item, str) and item.startswith("app_native_observation_deadline_seconds")
    ]
    if not candidates:
        return DEFAULT_OBSERVATION_DEADLINE_SECONDS
    if len(candidates) != 1:
        raise AppNativeDirectAdapterError("observation_deadline_invalid")
    match = DEADLINE_RE.fullmatch(candidates[0])
    if match is None:
        raise AppNativeDirectAdapterError("observation_deadline_invalid")
    return int(match.group(1))


def build_operation_binding(
    *,
    task_request: Mapping[str, object],
    lane_packet: Mapping[str, object],
    project_id: str,
) -> tuple[dict[str, object], str, str]:
    errors = validate_direct_request_boundary(
        task_request=task_request,
        lane_packet=lane_packet,
        registry_entry={
            "repository_id": task_request.get("repository_id"),
            "eligible_roles": [task_request.get("role")],
            "permitted_operations": [lane_packet.get("operation_id")],
            "permitted_read_scope": list(lane_packet.get("read_scope", [])),
            "maximum_mutation_scope": [],
            "repository_code_execution_policy": "forbidden",
            "approved_commands": [],
        },
    )
    if errors:
        raise AppNativeDirectAdapterError(errors[0])
    binding = {
        "schema_version": OPERATION_BINDING_SCHEMA,
        "task_request_sha256": task_request["task_request_sha256"],
        "request_sha256": task_request["request_sha256"],
        "claim_observation_sha256": task_request["claim_observation_sha256"],
        "lane_packet_sha256": task_request["lane_packet_sha256"],
        "repository_id": task_request["repository_id"],
        "issue_url": task_request["issue_url"],
        "role": task_request["role"],
        "lane_operation_id": lane_packet["operation_id"],
        "base_sha": task_request["base_sha"],
        "project_identity_sha256": project_identity_sha256(project_id),
        "pre_worktree_observation_sha256": task_request[
            "worktree_observation_sha256"
        ],
    }
    digest = canonical_sha256(binding)
    return binding, digest, f"app_native_{digest[:32]}"


def build_create_target(*, project_id: str, base_ref: str) -> dict[str, object]:
    if not _is_nonempty_text(project_id) or not _is_nonempty_text(base_ref):
        raise AppNativeDirectAdapterError("create_target_invalid")
    return {
        "type": "project",
        "projectId": project_id,
        "environment": {
            "type": "worktree",
            "startingState": {
                "type": "branch",
                "branchName": base_ref,
            },
        },
    }


def build_canonical_prompt(
    *,
    task_request: Mapping[str, object],
    lane_packet: Mapping[str, object],
    predecessor_packet: Mapping[str, object] | None,
    app_task_operation_id: str,
) -> str:
    if not _is_id(app_task_operation_id):
        raise AppNativeDirectAdapterError("app_task_operation_id_invalid")
    lane_json = canonical_json_bytes(lane_packet, final_lf=False).decode("utf-8")
    predecessor_json = (
        "null"
        if predecessor_packet is None
        else canonical_json_bytes(predecessor_packet, final_lf=False).decode("utf-8")
    )
    lines = (
        "Use the Mythic Edge agent constitution and $mythic-edge-workflow.",
        f"mythic_edge_operation_id: {app_task_operation_id}",
        f"mythic_edge_task_request_sha256: {task_request['task_request_sha256']}",
        f"mythic_edge_lane_packet_sha256: {lane_packet['lane_packet_sha256']}",
        f"Act as Codex {task_request['role']} for {task_request['issue_url']}.",
        "Use only the exact lane packet and predecessor packet below. Do not inherit or infer authority from ambient conversation.",
        f"lane_packet: {lane_json}",
        f"predecessor_packet: {predecessor_json}",
        "This is a read-only task. Make no repository, GitHub, registry, release, installation, dispatch, or external mutation.",
        "Return exactly one canonical object matching the existing trusted-owner native handoff object and no other prose.",
    )
    return "\n".join(lines) + "\n"


def normalize_task_status(value: object) -> str:
    if value is None:
        return "unavailable"
    observations = value if isinstance(value, list) else [value]
    if not observations:
        return "unavailable"
    if not all(isinstance(item, str) for item in observations):
        return "unknown"
    if any(
        item not in TERMINAL_STATUSES and item not in NONTERMINAL_STATUSES
        for item in observations
    ):
        return "unknown"
    normalized = {
        item if item in TERMINAL_STATUSES else "running"
        for item in observations
    }
    if len(normalized) > 1:
        return "conflicting"
    if len(normalized) == 1:
        return next(iter(normalized))
    return "unknown"


def _validate_handoff(value: object, role: str) -> Mapping[str, object]:
    handoff = _strict_mapping(value, HANDOFF_FIELDS, "handoff_fields_invalid")
    if handoff["status"] not in {
        "blocked",
        "changes_required",
        "complete",
        "no_next_role",
    }:
        raise AppNativeDirectAdapterError("handoff_status_invalid")
    if handoff["next_role"] not in {*"ABCDEFGH", None}:
        raise AppNativeDirectAdapterError("handoff_next_role_invalid")
    if handoff["status"] == "no_next_role" and handoff["next_role"] is not None:
        raise AppNativeDirectAdapterError("handoff_next_role_invalid")
    if role == "B" and handoff["next_role"] != "E":
        raise AppNativeDirectAdapterError("handoff_transition_invalid")
    if role == "E" and handoff["next_role"] not in {"D", "F", None}:
        raise AppNativeDirectAdapterError("handoff_transition_invalid")
    for field in ("source_artifact_paths", "finding_ids"):
        if not isinstance(handoff[field], list) or not all(
            _is_nonempty_text(item) for item in handoff[field]
        ):
            raise AppNativeDirectAdapterError(f"handoff_{field}_invalid")
    if handoff["stop_reason"] is not None and not _is_nonempty_text(
        handoff["stop_reason"]
    ):
        raise AppNativeDirectAdapterError("handoff_stop_reason_invalid")
    if not _is_sha256(handoff["handoff_sha256"]) or handoff[
        "handoff_sha256"
    ] != _self_digest(handoff, "handoff_sha256"):
        raise AppNativeDirectAdapterError("handoff_digest_invalid")
    return handoff


def _effect_counts_exact_zero(value: object) -> bool:
    return (
        isinstance(value, Mapping)
        and tuple(value) == EFFECT_COUNT_FIELDS
        and all(value[field] == 0 for field in EFFECT_COUNT_FIELDS)
    )


def _target_readback(
    *,
    readback: Mapping[str, object],
    expected_thread_id: str,
    project_id: str,
    task_request: Mapping[str, object],
    lane_packet: Mapping[str, object],
    app_task_operation_id: str,
) -> tuple[dict[str, object], str]:
    if readback["threadId"] != expected_thread_id:
        raise AppNativeDirectAdapterError("task_identity_changed")
    expected = {
        "projectId": project_id,
        "repositoryId": task_request["repository_id"],
        "worktreeObservationSha256": task_request["worktree_observation_sha256"],
        "branchRef": lane_packet["base_ref"],
        "baseSha": lane_packet["base_sha"],
        "operationId": app_task_operation_id,
    }
    if any(readback[field] != expected_value for field, expected_value in expected.items()):
        raise AppNativeDirectAdapterError("task_target_readback_mismatch")
    target = {
        "schema_version": TARGET_READBACK_SCHEMA,
        "task_identity_sha256": task_identity_sha256(expected_thread_id),
        "project_identity_sha256": project_identity_sha256(project_id),
        "repository_id": task_request["repository_id"],
        "worktree_observation_sha256": task_request["worktree_observation_sha256"],
        "base_sha": task_request["base_sha"],
        "app_task_operation_id": app_task_operation_id,
    }
    return target, canonical_sha256(target)


def seal_terminal_readback(value: Mapping[str, object]) -> tuple[dict[str, object], str]:
    terminal = dict(value)
    errors = validate_terminal_readback(terminal)
    if errors:
        raise AppNativeDirectAdapterError(errors[0])
    return terminal, canonical_sha256(terminal)


def validate_terminal_readback(
    value: object,
    *,
    app_task_operation_id: object = None,
    task_identity_digest: object = None,
    task_target_readback_sha256: object = None,
) -> list[str]:
    if not isinstance(value, Mapping) or tuple(value) != TERMINAL_READBACK_FIELDS:
        return ["terminal_readback_fields_invalid"]
    errors: list[str] = []
    if value["schema_version"] != TERMINAL_READBACK_SCHEMA:
        errors.append("terminal_readback_schema_invalid")
    if not _is_id(value["app_task_operation_id"]):
        errors.append("terminal_readback_operation_invalid")
    for field in ("task_identity_sha256", "task_target_readback_sha256"):
        if not _is_sha256(value[field]):
            errors.append(f"terminal_readback_{field}_invalid")
    if value["terminal_status"] not in TERMINAL_STATUSES:
        errors.append("terminal_readback_status_invalid")
    if not _is_utc_second(value["read_at_utc"]):
        errors.append("terminal_readback_time_invalid")
    expected = {
        "app_task_operation_id": app_task_operation_id,
        "task_identity_sha256": task_identity_digest,
        "task_target_readback_sha256": task_target_readback_sha256,
    }
    for field, expected_value in expected.items():
        if expected_value is not None and value[field] != expected_value:
            errors.append(f"terminal_readback_{field}_mismatch")
    return errors


def seal_platform_receipt(value: Mapping[str, object]) -> dict[str, object]:
    if tuple(value) not in {PLATFORM_RECEIPT_FIELDS[:-1], PLATFORM_RECEIPT_FIELDS}:
        raise AppNativeDirectAdapterError("platform_receipt_fields_invalid")
    receipt = dict(value)
    receipt.setdefault("platform_receipt_sha256", "")
    receipt["platform_receipt_sha256"] = _self_digest(
        receipt, "platform_receipt_sha256"
    )
    return receipt


def validate_platform_receipt(
    value: object,
    *,
    terminal_readback: object = None,
) -> list[str]:
    if not isinstance(value, Mapping) or tuple(value) != PLATFORM_RECEIPT_FIELDS:
        return ["platform_receipt_fields_invalid"]
    errors: list[str] = []
    if value["schema_version"] != PLATFORM_RECEIPT_SCHEMA:
        errors.append("platform_receipt_schema_invalid")
    if not _is_id(value["app_task_operation_id"]):
        errors.append("app_task_operation_id_invalid")
    for field in (
        "task_request_sha256",
        "claim_observation_sha256",
        "lane_packet_sha256",
        "canonical_prompt_sha256",
        "task_identity_sha256",
        "project_identity_sha256",
        "pre_worktree_observation_sha256",
        "task_target_readback_sha256",
    ):
        if not _is_sha256(value[field]):
            errors.append(f"{field}_invalid")
    if value["create_call_count"] != 1:
        errors.append("create_call_count_invalid")
    if value["returned_identifier_kind"] not in RETURNED_IDENTIFIER_KINDS:
        errors.append("returned_identifier_kind_invalid")
    if not _is_positive_int(value["repository_id"]):
        errors.append("repository_id_invalid")
    if not _is_utc_second(value["accepted_at_utc"]):
        errors.append("accepted_at_utc_invalid")
    status = value["terminal_status"]
    if status not in PUBLIC_STATUS_VALUES:
        errors.append("terminal_status_invalid")
    for field in (
        "automatic_retry_count",
        "replacement_task_count",
        "follow_up_message_count",
    ):
        if value[field] != 0:
            errors.append(f"{field}_invalid")
    if not _is_positive_int(value["observation_deadline_seconds"]):
        errors.append("observation_deadline_seconds_invalid")
    reconciliation = value["reconciliation_status"]
    if reconciliation not in RECONCILIATION_STATUSES:
        errors.append("reconciliation_status_invalid")
    if status in TERMINAL_STATUSES:
        if not _is_sha256(value["terminal_readback_sha256"]):
            errors.append("terminal_readback_sha256_invalid")
        if terminal_readback is None:
            errors.append("terminal_readback_object_required")
        else:
            terminal_errors = validate_terminal_readback(
                terminal_readback,
                app_task_operation_id=value["app_task_operation_id"],
                task_identity_digest=value["task_identity_sha256"],
                task_target_readback_sha256=value["task_target_readback_sha256"],
            )
            errors.extend(terminal_errors)
            if not terminal_errors and canonical_sha256(terminal_readback) != value[
                "terminal_readback_sha256"
            ]:
                errors.append("terminal_readback_digest_mismatch")
        if reconciliation not in {"not_required", "resolved_same_task_terminal"}:
            errors.append("terminal_reconciliation_invalid")
    else:
        if value["terminal_readback_sha256"] is not None:
            errors.append("terminal_readback_must_be_null")
        if reconciliation != "required_same_task":
            errors.append("nonterminal_reconciliation_invalid")
    handoff_digest = value["typed_handoff_sha256"]
    if status == "completed":
        if not _is_sha256(handoff_digest):
            errors.append("typed_handoff_sha256_required")
    elif handoff_digest is not None:
        errors.append("typed_handoff_sha256_forbidden")
    post_digest = value["post_worktree_observation_sha256"]
    if status == "completed" and post_digest is None:
        errors.append("post_worktree_observation_sha256_required")
    elif post_digest is not None and not _is_sha256(post_digest):
        errors.append("post_worktree_observation_sha256_invalid")
    if value["platform_receipt_sha256"] != _self_digest(
        value, "platform_receipt_sha256"
    ):
        errors.append("platform_receipt_digest_invalid")
    return errors


def _task_receipt(
    *,
    task_request_sha256: str,
    thread_id: str,
    accepted_at_utc: str,
    platform_receipt: Mapping[str, object],
) -> dict[str, object]:
    platform_digest = str(platform_receipt["platform_receipt_sha256"])
    return with_self_digest(
        {
            "schema_version": "trusted_owner_native_task_receipt.v1",
            "task_request_sha256": task_request_sha256,
            "task_id": thread_id,
            "accepted_at_utc": accepted_at_utc,
            "platform_receipt_ref": (
                f"role_pool:app_native_direct:{platform_digest[:32]}"
            ),
            "platform_receipt_sha256": platform_digest,
            "task_receipt_sha256": "",
        },
        "task_receipt_sha256",
    )


def validate_task_receipt(
    value: object,
    *,
    task_request: object = None,
    platform_receipt: object = None,
) -> list[str]:
    if not isinstance(value, Mapping) or tuple(value) != TASK_RECEIPT_FIELDS:
        return ["task_receipt_fields_invalid"]
    errors: list[str] = []
    if value["schema_version"] != "trusted_owner_native_task_receipt.v1":
        errors.append("task_receipt_schema_invalid")
    if not _is_sha256(value["task_request_sha256"]):
        errors.append("task_request_sha256_invalid")
    if not _is_id(value["task_id"]):
        errors.append("task_id_invalid")
    if not _is_utc_second(value["accepted_at_utc"]):
        errors.append("task_receipt_time_invalid")
    if not _is_sha256(value["platform_receipt_sha256"]):
        errors.append("platform_receipt_sha256_invalid")
    expected_ref = f"role_pool:app_native_direct:{str(value['platform_receipt_sha256'])[:32]}"
    if value["platform_receipt_ref"] != expected_ref:
        errors.append("platform_receipt_ref_invalid")
    if value["task_receipt_sha256"] != _self_digest(value, "task_receipt_sha256"):
        errors.append("task_receipt_digest_invalid")
    if isinstance(task_request, Mapping) and value["task_request_sha256"] != task_request.get(
        "task_request_sha256"
    ):
        errors.append("task_request_binding_mismatch")
    if isinstance(platform_receipt, Mapping):
        if value["platform_receipt_sha256"] != platform_receipt.get(
            "platform_receipt_sha256"
        ):
            errors.append("platform_receipt_binding_mismatch")
        if value["accepted_at_utc"] != platform_receipt.get("accepted_at_utc"):
            errors.append("accepted_at_binding_mismatch")
        if task_identity_sha256(value["task_id"]) != platform_receipt.get(
            "task_identity_sha256"
        ):
            errors.append("task_identity_binding_mismatch")
    return errors


def _terminal_readback_kat() -> dict[str, object]:
    return {
        "schema_version": TERMINAL_READBACK_SCHEMA,
        "app_task_operation_id": "app_native_0123456789abcdef0123456789abcdef",
        "task_identity_sha256": "5" * 64,
        "terminal_status": "completed",
        "task_target_readback_sha256": "8" * 64,
        "read_at_utc": "2026-08-04T12:05:00Z",
    }


def _platform_receipt_kat() -> dict[str, object]:
    return {
        "schema_version": PLATFORM_RECEIPT_SCHEMA,
        "app_task_operation_id": "app_native_0123456789abcdef0123456789abcdef",
        "task_request_sha256": "1" * 64,
        "claim_observation_sha256": "2" * 64,
        "lane_packet_sha256": "3" * 64,
        "canonical_prompt_sha256": "4" * 64,
        "create_call_count": 1,
        "returned_identifier_kind": "thread_id",
        "task_identity_sha256": "5" * 64,
        "project_identity_sha256": "6" * 64,
        "repository_id": 1235264383,
        "pre_worktree_observation_sha256": "7" * 64,
        "task_target_readback_sha256": "8" * 64,
        "accepted_at_utc": "2026-08-04T12:00:00Z",
        "terminal_status": "completed",
        "terminal_readback_sha256": TERMINAL_READBACK_KAT_SHA256,
        "typed_handoff_sha256": "a" * 64,
        "post_worktree_observation_sha256": "b" * 64,
        "automatic_retry_count": 0,
        "replacement_task_count": 0,
        "follow_up_message_count": 0,
        "observation_deadline_seconds": 5400,
        "reconciliation_status": "not_required",
        "platform_receipt_sha256": PLATFORM_RECEIPT_KAT_SELF_SHA256,
    }


def validate_fixed_contract_bytes() -> dict[str, object]:
    terminal = _terminal_readback_kat()
    terminal_bytes = canonical_json_bytes(terminal)
    platform = _platform_receipt_kat()
    platform_preimage = canonical_json_bytes(
        {
            key: value
            for key, value in platform.items()
            if key != "platform_receipt_sha256"
        }
    )
    platform_bytes = canonical_json_bytes(platform)
    checks = {
        "terminal_byte_count": len(terminal_bytes),
        "terminal_sha256": hashlib.sha256(terminal_bytes).hexdigest(),
        "platform_preimage_byte_count": len(platform_preimage),
        "platform_self_sha256": hashlib.sha256(platform_preimage).hexdigest(),
        "platform_artifact_byte_count": len(platform_bytes),
        "platform_artifact_sha256": hashlib.sha256(platform_bytes).hexdigest(),
    }
    expected = {
        "terminal_byte_count": 391,
        "terminal_sha256": TERMINAL_READBACK_KAT_SHA256,
        "platform_preimage_byte_count": 1489,
        "platform_self_sha256": PLATFORM_RECEIPT_KAT_SELF_SHA256,
        "platform_artifact_byte_count": 1582,
        "platform_artifact_sha256": PLATFORM_RECEIPT_KAT_ARTIFACT_SHA256,
    }
    if checks != expected:
        raise AppNativeDirectAdapterError("fixed_contract_bytes_invalid")
    if validate_platform_receipt(platform, terminal_readback=terminal):
        raise AppNativeDirectAdapterError("fixed_contract_receipt_invalid")
    return checks


def _contains_private_value(value: object, private_values: tuple[str, ...]) -> bool:
    if isinstance(value, str):
        return any(item and item in value for item in private_values)
    if isinstance(value, Mapping):
        return any(
            _contains_private_value(key, private_values)
            or _contains_private_value(item, private_values)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_contains_private_value(item, private_values) for item in value)
    return False


class TrustedNativeAppDirectTaskAdapter:
    """One-attempt, fake-client-only realization of the direct app contract."""

    synthetic_only = True
    adapter_identity = APP_NATIVE_DIRECT_ADAPTER_ID
    public_launcher_identity = PUBLIC_LAUNCHER_ID

    def __init__(
        self,
        *,
        task_request: Mapping[str, object],
        lane_packet: Mapping[str, object],
        registry_entry: Mapping[str, object],
        project_id: str,
        client: InertAppNativeClient,
        predecessor_packet: Mapping[str, object] | None = None,
        clock: object = None,
        monotonic_clock: object = None,
        first_r2: bool = True,
    ) -> None:
        self._task_request = dict(task_request)
        self._lane_packet = dict(lane_packet)
        self._registry_entry = dict(registry_entry)
        self._project_id = project_id
        self._client = client
        self._predecessor_packet = (
            None if predecessor_packet is None else dict(predecessor_packet)
        )
        self._clock = clock
        self._monotonic_clock = monotonic_clock
        self._first_r2 = first_r2
        self._guard = _CallGuard()
        self._attempted = False
        self._thread_id: str | None = None
        self._returned_identifier_kind: str | None = None
        self._accepted_at_utc: str | None = None
        self._operation_id: str | None = None
        self._prompt_sha256: str | None = None
        self._target_readback_sha256: str | None = None
        self._create_started_monotonic: float | None = None
        self._create_call_count = 0
        self.last_result: dict[str, object] | None = None

    @property
    def call_guard_state(self) -> str:
        return self._guard.state

    def _preflight(self) -> tuple[str, str, int]:
        if getattr(self._client, "synthetic_only", False) is not True:
            raise AppNativeDirectAdapterError("fake_client_required")
        errors = (
            validate_first_r2_request(
                task_request=self._task_request,
                lane_packet=self._lane_packet,
                registry_entry=self._registry_entry,
            )
            if self._first_r2
            else validate_direct_request_boundary(
                task_request=self._task_request,
                lane_packet=self._lane_packet,
                registry_entry=self._registry_entry,
            )
        )
        if errors:
            raise AppNativeDirectAdapterError(errors[0])
        _, _, operation_id = build_operation_binding(
            task_request=self._task_request,
            lane_packet=self._lane_packet,
            project_id=self._project_id,
        )
        prompt = build_canonical_prompt(
            task_request=self._task_request,
            lane_packet=self._lane_packet,
            predecessor_packet=self._predecessor_packet,
            app_task_operation_id=operation_id,
        )
        if self._project_id in prompt:
            raise AppNativeDirectAdapterError("private_project_identity_exposed")
        return operation_id, prompt, observation_deadline_seconds(self._lane_packet)

    def _list_matches(
        self,
        *,
        client_thread_id: str | None,
        operation_id: str,
    ) -> list[str]:
        try:
            response = self._client.list_threads()
        except Exception:
            return []
        if not isinstance(response, Mapping) or tuple(response) != THREAD_LIST_FIELDS:
            return []
        threads = response["threads"]
        if not isinstance(threads, list):
            return []
        matches: list[str] = []
        for item in threads:
            if not isinstance(item, Mapping) or tuple(item) != THREAD_LIST_ENTRY_FIELDS:
                return []
            if (
                _is_id(item["threadId"])
                and (item["clientThreadId"] is None or _is_id(item["clientThreadId"]))
                and item["projectId"] == self._project_id
                and item["operationId"] == operation_id
                and (client_thread_id is None or item["clientThreadId"] == client_thread_id)
            ):
                matches.append(str(item["threadId"]))
        return matches

    def _resolve_create_response(
        self,
        response: object,
        *,
        operation_id: str,
    ) -> tuple[str | None, str]:
        if isinstance(response, Mapping) and tuple(response) == ("threadId",):
            return (
                (str(response["threadId"]), "thread_id")
                if _is_id(response["threadId"])
                else (None, "identity_unknown")
            )
        if isinstance(response, Mapping) and tuple(response) == ("clientThreadId",):
            client_id = response["clientThreadId"]
            if not _is_id(client_id):
                return None, "identity_unknown"
            matches = self._list_matches(
                client_thread_id=str(client_id),
                operation_id=operation_id,
            )
            return (
                (matches[0], "client_thread_id_resolved")
                if len(matches) == 1
                else (None, "identity_pending" if not matches else "identity_unknown")
            )
        return None, "identity_unknown"

    def _read(self, thread_id: str) -> Mapping[str, object] | None:
        try:
            value = self._client.read_thread(thread_id)
        except Exception:
            return None
        if not isinstance(value, Mapping) or tuple(value) != THREAD_READBACK_FIELDS:
            return None
        return value

    def _deadline_elapsed(self, deadline: int) -> bool:
        if self._create_started_monotonic is None:
            raise AppNativeDirectAdapterError("monotonic_start_missing")
        current = _monotonic_now(self._monotonic_clock)
        if current < self._create_started_monotonic:
            raise AppNativeDirectAdapterError("monotonic_clock_regressed")
        return current - self._create_started_monotonic >= deadline

    def _public_result(
        self,
        *,
        status: str,
        platform_receipt: Mapping[str, object] | None,
        task_receipt: Mapping[str, object] | None,
    ) -> dict[str, object]:
        result: dict[str, object] = {
            "status": status,
            "platform_receipt": (
                None if platform_receipt is None else dict(platform_receipt)
            ),
            "task_receipt": None if task_receipt is None else dict(task_receipt),
            "create_call_count": self._create_call_count,
            "automatic_retry_count": 0,
            "replacement_task_count": 0,
            "follow_up_message_count": 0,
            "call_guard_state": self._guard.state,
            "synthetic_only": True,
            "live_ready": False,
        }
        private_values = (self._project_id,)
        if _contains_private_value(result, private_values):
            raise AppNativeDirectAdapterError("private_value_exposed")
        return result

    def _seal_observation(
        self,
        *,
        readback: Mapping[str, object] | None,
        reconciliation_status: str,
        deadline: int,
    ) -> dict[str, object]:
        assert self._thread_id is not None
        assert self._returned_identifier_kind is not None
        assert self._accepted_at_utc is not None
        assert self._operation_id is not None
        assert self._prompt_sha256 is not None
        if readback is None:
            if self._target_readback_sha256 is None:
                return self._public_result(
                    status="unknown_outcome_reconciliation_required",
                    platform_receipt=None,
                    task_receipt=None,
                )
            status = "unavailable"
            post_digest = None
            handoff_digest = None
            terminal = None
            terminal_digest = None
        else:
            target, target_digest = _target_readback(
                readback=readback,
                expected_thread_id=self._thread_id,
                project_id=self._project_id,
                task_request=self._task_request,
                lane_packet=self._lane_packet,
                app_task_operation_id=self._operation_id,
            )
            del target
            if self._target_readback_sha256 is not None and target_digest != self._target_readback_sha256:
                raise AppNativeDirectAdapterError("task_target_identity_changed")
            self._target_readback_sha256 = target_digest
            status = normalize_task_status(readback["status"])
            post_digest = readback["postWorktreeObservationSha256"]
            if post_digest is not None and not _is_sha256(post_digest):
                raise AppNativeDirectAdapterError("post_worktree_observation_invalid")
            if (
                post_digest is not None
                and post_digest != self._task_request["worktree_observation_sha256"]
            ):
                raise AppNativeDirectAdapterError(
                    "post_worktree_observation_mismatch"
                )
            if status == "completed" and post_digest is None:
                raise AppNativeDirectAdapterError(
                    "post_worktree_observation_required"
                )
            if not _effect_counts_exact_zero(readback["effectCounts"]):
                raise AppNativeDirectAdapterError("unexpected_state_change")
            handoff_digest = None
            terminal = None
            terminal_digest = None
            handoffs = readback["handoffs"]
            if not isinstance(handoffs, list):
                raise AppNativeDirectAdapterError("handoff_collection_invalid")
            if status == "completed":
                if len(handoffs) != 1:
                    raise AppNativeDirectAdapterError("handoff_cardinality_invalid")
                handoff = _validate_handoff(handoffs[0], str(self._task_request["role"]))
                handoff_digest = handoff["handoff_sha256"]
            elif handoffs:
                raise AppNativeDirectAdapterError("handoff_forbidden_for_status")
            if status in TERMINAL_STATUSES:
                terminal, terminal_digest = seal_terminal_readback(
                    {
                        "schema_version": TERMINAL_READBACK_SCHEMA,
                        "app_task_operation_id": self._operation_id,
                        "task_identity_sha256": task_identity_sha256(self._thread_id),
                        "terminal_status": status,
                        "task_target_readback_sha256": target_digest,
                        "read_at_utc": _utc_now(self._clock),
                    }
                )

        if self._target_readback_sha256 is None:
            return self._public_result(
                status="unknown_outcome_reconciliation_required",
                platform_receipt=None,
                task_receipt=None,
            )
        if status not in TERMINAL_STATUSES:
            reconciliation_status = "required_same_task"
        receipt = seal_platform_receipt(
            {
                "schema_version": PLATFORM_RECEIPT_SCHEMA,
                "app_task_operation_id": self._operation_id,
                "task_request_sha256": self._task_request["task_request_sha256"],
                "claim_observation_sha256": self._task_request[
                    "claim_observation_sha256"
                ],
                "lane_packet_sha256": self._task_request["lane_packet_sha256"],
                "canonical_prompt_sha256": self._prompt_sha256,
                "create_call_count": 1,
                "returned_identifier_kind": self._returned_identifier_kind,
                "task_identity_sha256": task_identity_sha256(self._thread_id),
                "project_identity_sha256": project_identity_sha256(self._project_id),
                "repository_id": self._task_request["repository_id"],
                "pre_worktree_observation_sha256": self._task_request[
                    "worktree_observation_sha256"
                ],
                "task_target_readback_sha256": self._target_readback_sha256,
                "accepted_at_utc": self._accepted_at_utc,
                "terminal_status": status,
                "terminal_readback_sha256": terminal_digest,
                "typed_handoff_sha256": handoff_digest,
                "post_worktree_observation_sha256": post_digest,
                "automatic_retry_count": 0,
                "replacement_task_count": 0,
                "follow_up_message_count": 0,
                "observation_deadline_seconds": deadline,
                "reconciliation_status": reconciliation_status,
            }
        )
        receipt_errors = validate_platform_receipt(
            receipt,
            terminal_readback=terminal,
        )
        if receipt_errors:
            raise AppNativeDirectAdapterError("platform_receipt_invalid")
        task_receipt = _task_receipt(
            task_request_sha256=str(self._task_request["task_request_sha256"]),
            thread_id=self._thread_id,
            accepted_at_utc=self._accepted_at_utc,
            platform_receipt=receipt,
        )
        if validate_task_receipt(
            task_receipt,
            task_request=self._task_request,
            platform_receipt=receipt,
        ):
            raise AppNativeDirectAdapterError("task_receipt_invalid")
        public_status = (
            "synthetic_app_native_receipt_accepted_non_live"
            if status == "completed"
            else (
                "failed_lane_known"
                if status in {"failed", "interrupted"}
                else "unknown_outcome_reconciliation_required"
            )
        )
        return self._public_result(
            status=public_status,
            platform_receipt=receipt,
            task_receipt=task_receipt,
        )

    def create_once(self, request: Mapping[str, object]) -> object:
        if self._attempted:
            raise AppNativeDirectAdapterError("app_native_adapter_already_used")
        self._attempted = True
        if dict(request) != self._task_request:
            raise AppNativeDirectAdapterError("task_request_binding_mismatch")
        operation_id, prompt, deadline = self._preflight()
        self._operation_id = operation_id
        self._prompt_sha256 = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        target = build_create_target(
            project_id=self._project_id,
            base_ref=str(self._lane_packet["base_ref"]),
        )
        self._guard.enter()
        self._create_call_count = 1
        self._accepted_at_utc = _utc_now(self._clock)
        self._create_started_monotonic = _monotonic_now(self._monotonic_clock)
        try:
            response = self._client.create_thread(target=target, prompt=prompt)
            thread_id, kind = self._resolve_create_response(
                response,
                operation_id=operation_id,
            )
        except KnownCreateRejection as exc:
            self.last_result = self._public_result(
                status="failed_lane_known",
                platform_receipt=None,
                task_receipt=None,
            )
            raise AppNativeDirectAdapterError(
                "failed_lane_known", profile_projection="failed_lane_known"
            ) from exc
        except AmbiguousCreateOutcome:
            matches = self._list_matches(
                client_thread_id=None,
                operation_id=operation_id,
            )
            thread_id, kind = (
                (matches[0], "ambiguous_submission_reconciled")
                if len(matches) == 1
                else (None, "identity_unknown")
            )
        except Exception:
            thread_id, kind = None, "identity_unknown"
        if thread_id is None:
            self.last_result = self._public_result(
                status="unknown_outcome_reconciliation_required",
                platform_receipt=None,
                task_receipt=None,
            )
            raise AppNativeDirectAdapterError(
                "identity_pending" if kind == "identity_pending" else "identity_unknown",
                profile_projection="unknown_outcome_reconciliation_required",
            )
        self._thread_id = thread_id
        self._returned_identifier_kind = kind
        try:
            initial = self._read(thread_id)
            initial_status = (
                "unavailable"
                if initial is None
                else normalize_task_status(initial["status"])
            )
            if initial is not None and initial_status not in TERMINAL_STATUSES:
                _, initial_target_digest = _target_readback(
                    readback=initial,
                    expected_thread_id=thread_id,
                    project_id=self._project_id,
                    task_request=self._task_request,
                    lane_packet=self._lane_packet,
                    app_task_operation_id=operation_id,
                )
                if not _effect_counts_exact_zero(initial["effectCounts"]):
                    raise AppNativeDirectAdapterError("unexpected_state_change")
                if initial["handoffs"] != []:
                    raise AppNativeDirectAdapterError(
                        "handoff_forbidden_for_status"
                    )
                self._target_readback_sha256 = initial_target_digest
            if initial_status in TERMINAL_STATUSES:
                final_readback = initial
            else:
                if not self._deadline_elapsed(deadline):
                    raise AppNativeDirectAdapterError(
                        "observation_deadline_not_elapsed"
                    )
                final_readback = self._read(thread_id)
            self.last_result = self._seal_observation(
                readback=final_readback,
                reconciliation_status="not_required",
                deadline=deadline,
            )
        except AppNativeDirectAdapterError as exc:
            if exc.code == "observation_deadline_not_elapsed":
                self.last_result = None
                raise AppNativeDirectAdapterError(exc.code) from exc
            projection = (
                "unknown_outcome_reconciliation_required"
                if exc.code in {
                    "task_identity_changed",
                    "task_target_identity_changed",
                    "post_worktree_observation_invalid",
                    "post_worktree_observation_mismatch",
                    "post_worktree_observation_required",
                }
                else "failed_lane_known"
            )
            self.last_result = self._public_result(
                status=projection,
                platform_receipt=None,
                task_receipt=None,
            )
            raise AppNativeDirectAdapterError(
                exc.code,
                profile_projection=projection,
            ) from exc
        if self.last_result["status"] != "synthetic_app_native_receipt_accepted_non_live":
            raise AppNativeDirectAdapterError(
                str(self.last_result["status"]),
                profile_projection=str(self.last_result["status"]),
            )
        return self.last_result["task_receipt"]

    def reconcile_same_task(self) -> dict[str, object]:
        if self._guard.state != "entered_once" or self._thread_id is None:
            raise AppNativeDirectAdapterError("same_task_reconciliation_unavailable")
        deadline = observation_deadline_seconds(self._lane_packet)
        if not self._deadline_elapsed(deadline):
            raise AppNativeDirectAdapterError("observation_deadline_not_elapsed")
        self.last_result = self._seal_observation(
            readback=self._read(self._thread_id),
            reconciliation_status="resolved_same_task_terminal",
            deadline=deadline,
        )
        return self.last_result


def real_app_task_create_once(*args: object, **kwargs: object) -> None:
    """Fail closed: the accepted R0 implementation has no real connector."""

    del args, kwargs
    raise AppNativeDirectAdapterError("real_task_operation_not_authorized")
