"""Inert, fake-transport App Server adapter for the trusted-native Role Pool.

This module implements the contract-owned protocol and validation boundary for
R0 tests. It cannot start Codex, create a process, use a network endpoint, or
publish durable state. A real process transport remains a separately
authorized R2 concern.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Mapping, Protocol

PROFILE_CONTRACT_SHA256 = "4a0ba9efe5c987735c09df66f94f42924a92a40ca68fd15a84ffb2c41842c94d"
COMPANION_CONTRACT_SHA256 = "814ac91c4e099216ae4870458d7524a3d65bfba7459cbfda7de82a5fc79067e8"
PUBLIC_LAUNCHER_ID = "codex:native-task-create/v1"
APP_SERVER_ADAPTER_ID = "codex:app-server-stdio-direct/v1"
PINNED_CODEX_VERSION = "0.146.0"
PINNED_EXECUTABLE_SHA256 = "bc343ba420dc2e2e9f59e6fc5e5bf0aae1cd8c771fc319665241fc9c0271fddb"
PINNED_PROTOCOL_SCHEMA_SHA256 = "08cc0c836bf0caca1e65b92956c3d57fd59c6be9b66277f77afe1cf65aefa592"

EXECUTION_BINDING_SCHEMA = "trusted_owner_app_server_execution_binding.v1"
INSTRUCTION_PACKET_SCHEMA = "trusted_owner_app_server_instruction_packet.v1"
PLATFORM_RECEIPT_SCHEMA = "trusted_owner_app_server_platform_receipt.v1"
ROLE_OUTPUT_SCHEMA_VERSION = "trusted_owner_app_server_role_output.v1"
LIFECYCLE_REGISTRY_SCHEMA = "trusted_owner_app_server_lifecycle_registry.v1"

DEVELOPER_INSTRUCTION = (
    "Execute exactly one Mythic Edge trusted-owner lane from the supplied "
    "canonical instruction packet. Follow the loaded AGENTS.md, the role "
    "contract, and the exact repository-owned Role Pool skill. Do not infer "
    "or widen authority. Return only one JSON object matching the supplied "
    "output schema."
)
DEVELOPER_INSTRUCTION_SHA256 = "2d084e88397914bb97e1bae60be44ffeb3d29c2577f984db966937c1c91beffa"

ROLE_OUTPUT_SCHEMA_JSON = (
    '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
    '"additionalProperties":false,"properties":{"files_changed":{"items":'
    '{"additionalProperties":false,"properties":{"after_sha256":{"pattern":'
    '"^[0-9a-f]{64}$","type":["string","null"]},"before_sha256":{"pattern":'
    '"^[0-9a-f]{64}$","type":["string","null"]},"change_kind":{"enum":'
    '["added","deleted","modified"],"type":"string"},"path":{"minLength":1,'
    '"type":"string"}},"required":["path","change_kind","before_sha256",'
    '"after_sha256"],"type":"object"},"type":"array"},"handoff":'
    '{"additionalProperties":false,"properties":{"finding_ids":{"items":'
    '{"minLength":1,"type":"string"},"type":"array"},"next_role":{"enum":'
    '["A","B","C","D","E","F","G","H",null]},"source_artifact_paths":'
    '{"items":{"minLength":1,"type":"string"},"type":"array"},"status":'
    '{"enum":["blocked","changes_required","complete","no_next_role"],'
    '"type":"string"},"stop_reason":{"type":["string","null"]}},'
    '"required":["status","next_role","source_artifact_paths","finding_ids",'
    '"stop_reason"],"type":"object"},"result":{"enum":["blocked","completed",'
    '"finding"],"type":"string"},"schema_version":{"const":'
    '"trusted_owner_app_server_role_output.v1","type":"string"},'
    '"validation":{"items":{"additionalProperties":false,"properties":'
    '{"command_id":{"minLength":1,"type":"string"},"evidence_sha256":'
    '{"pattern":"^[0-9a-f]{64}$","type":["string","null"]},"exit_code":'
    '{"type":["integer","null"]},"status":{"enum":["blocked","failed",'
    '"not_run","passed"],"type":"string"}},"required":["command_id","status",'
    '"exit_code","evidence_sha256"],"type":"object"},"type":"array"}},'
    '"required":["schema_version","result","files_changed","validation",'
    '"handoff"],"type":"object"}'
)
ROLE_OUTPUT_SCHEMA_SHA256 = "fc0ade6cf9664b32b3b3e83935f69f01418356897f16e937ed597aedfdd5b247"

INSPECT_ONLY_CONFIG = """[features]
apps = false
artifact = false
auth_elicitation = false
browser_use = false
browser_use_external = false
browser_use_full_cdp_access = false
code_mode = false
code_mode_host = false
code_mode_only = false
computer_use = false
default_mode_request_user_input = false
enable_mcp_apps = false
goals = false
hooks = false
image_generation = false
in_app_browser = false
multi_agent = false
multi_agent_v2 = false
plugin_sharing = false
plugins = false
remote_plugin = false
request_permissions_tool = false
shell_tool = false
skill_mcp_dependency_install = false
skill_search = false
standalone_web_search = false
tool_call_mcp_elicitation = false
tool_suggest = false
unified_exec = false
web_search_cached = false
web_search_request = false
workspace_dependencies = false
"""
INSPECT_ONLY_CONFIG_SHA256 = "fae8d0a1992225d30d2275c247629b31f39b3b9ee4578963fb121e1093510412"

EXECUTION_BINDING_FIELDS = (
    "schema_version",
    "profile_contract_sha256",
    "companion_contract_sha256",
    "task_request_sha256",
    "request_sha256",
    "claim_observation_sha256",
    "lane_packet_sha256",
    "worktree_observation_sha256",
    "registry_sha256",
    "release_state_record_sha256",
    "skill_tree_sha256",
    "repository_id",
    "issue_url",
    "role",
    "operation_id",
    "predecessor_packet_sha256",
    "cwd_identity_sha256",
    "model_request_mode",
    "requested_model",
    "requested_effort",
    "sandbox_binding_sha256",
    "approval_policy",
    "role_instruction_sha256",
    "instruction_packet_sha256",
    "role_pool_skill_sha256",
    "output_schema_sha256",
    "installation_receipt_sha256",
    "executable_sha256",
    "protocol_schema_sha256",
    "runtime_config_manifest_sha256",
    "environment_binding_sha256",
    "turn_timeout_seconds",
    "execution_binding_sha256",
)

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

INSTRUCTION_PACKET_FIELDS = (
    "schema_version",
    "task_request_sha256",
    "lane_packet_sha256",
    "role",
    "operation_id",
    "issue_url",
    "predecessor_packet_sha256",
    "role_contract_path",
    "role_contract_sha256",
    "role_pool_skill_sha256",
    "output_schema_sha256",
    "lane_packet_json",
    "predecessor_packet_json",
    "instruction_packet_sha256",
)

INSPECT_REGISTRY_PROJECTION_FIELDS = (
    "repository_id",
    "repository_code_execution_policy",
    "maximum_mutation_scope",
    "approved_commands",
)

ROLE_CONTRACT_PATHS = {
    "B": "docs/agent_threads/module_contract.md",
    "E": "docs/agent_threads/review.md",
}

PLATFORM_RECEIPT_FIELDS = (
    "schema_version",
    "task_request_sha256",
    "execution_binding_sha256",
    "installation_receipt_sha256",
    "executable_sha256",
    "protocol_schema_sha256",
    "initialize_request_id",
    "thread_start_request_id",
    "turn_start_request_id",
    "interrupt_request_id",
    "thread_id_sha256",
    "turn_id_sha256",
    "effective_model_sha256",
    "effective_effort_sha256",
    "instruction_sources_sha256",
    "process_start_count",
    "initialize_count",
    "initialized_count",
    "thread_start_count",
    "turn_start_count",
    "interrupt_count",
    "command_approval_count",
    "file_change_approval_count",
    "terminal_notification_sha256",
    "role_output_sha256",
    "lifecycle_case",
    "profile_terminal_projection",
    "process_exit_class",
    "cleanup_status",
    "started_at_utc",
    "terminal_at_utc",
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

ROLE_OUTPUT_FIELDS = (
    "schema_version",
    "result",
    "files_changed",
    "validation",
    "handoff",
)
HANDOFF_FIELDS = (
    "status",
    "next_role",
    "source_artifact_paths",
    "finding_ids",
    "stop_reason",
)

LIFECYCLE_FIELDS = (
    "ordinal",
    "phase",
    "raw_observation",
    "consumption_state",
    "lifecycle_case",
    "profile_projection",
)

LIFECYCLE_ROWS = (
    (
        1,
        "preflight",
        "profile_priority_01_request_or_packet_invalid",
        "not_consumed",
        "AS-BLK-001",
        "blocked_request_or_packet_invalid",
    ),
    (2, "preflight", "profile_priority_02_no_wip_authority", "not_consumed", "AS-BLK-001", "blocked_no_wip_authority"),
    (
        3,
        "preflight",
        "profile_priority_03_skill_source_drift",
        "not_consumed",
        "AS-BLK-001",
        "blocked_skill_source_drift",
    ),
    (
        4,
        "preflight",
        "profile_priority_04_registry_invalid",
        "not_consumed",
        "AS-BLK-001",
        "blocked_registry_missing_or_invalid",
    ),
    (
        5,
        "preflight",
        "profile_priority_05_release_state_invalid",
        "not_consumed",
        "AS-BLK-001",
        "blocked_release_state_invalid",
    ),
    (
        6,
        "preflight",
        "profile_priority_06_repository_inactive",
        "not_consumed",
        "AS-BLK-001",
        "blocked_repository_inactive",
    ),
    (
        7,
        "preflight",
        "profile_priority_07_repository_identity_mismatch",
        "not_consumed",
        "AS-BLK-001",
        "blocked_repository_identity_mismatch",
    ),
    (
        8,
        "preflight",
        "profile_priority_08_role_or_operation_not_allowed",
        "not_consumed",
        "AS-BLK-001",
        "blocked_role_or_operation_not_allowed",
    ),
    (
        9,
        "preflight",
        "profile_priority_09_command_not_approved",
        "not_consumed",
        "AS-BLK-001",
        "blocked_command_not_approved",
    ),
    (
        10,
        "preflight",
        "profile_priority_10_external_isolation_required",
        "not_consumed",
        "AS-BLK-001",
        "blocked_external_isolation_required",
    ),
    (
        11,
        "preflight",
        "profile_priority_11_mixed_profile_wave",
        "not_consumed",
        "AS-BLK-001",
        "blocked_mixed_profile_wave",
    ),
    (
        12,
        "preflight",
        "profile_priority_12_predecessor_invalid",
        "not_consumed",
        "AS-BLK-001",
        "blocked_predecessor_packet_invalid",
    ),
    (
        13,
        "preflight",
        "profile_priority_13_cross_lane_overlap",
        "not_consumed",
        "AS-BLK-001",
        "blocked_cross_lane_overlap",
    ),
    (
        14,
        "preflight",
        "profile_priority_14_capacity_exceeded",
        "not_consumed",
        "AS-BLK-001",
        "blocked_capacity_exceeded",
    ),
    (15, "preflight", "profile_priority_15_f_boundary", "not_consumed", "AS-BLK-001", "blocked_f_boundary"),
    (
        16,
        "consumption",
        "record_prior_or_collision",
        "not_consumed",
        "AS-CNS-REUSE-001",
        "blocked_request_or_packet_invalid",
    ),
    (
        17,
        "consumption",
        "record_state_or_commit_unknown",
        "unknown",
        "AS-CNS-UNK-001",
        "unknown_outcome_reconciliation_required",
    ),
    (18, "process_start", "start_known_not_started", "consumed", "AS-START-001", "failed_lane_known"),
    (
        19,
        "process_start",
        "start_observation_unknown",
        "consumed",
        "AS-START-UNK-001",
        "unknown_outcome_reconciliation_required",
    ),
    (20, "handshake", "handshake_known_invalid", "consumed", "AS-HSK-001", "failed_lane_known"),
    (21, "thread_start", "thread_start_known_invalid", "consumed", "AS-THR-001", "failed_lane_known"),
    (22, "pre_turn", "pre_turn_binding_known_invalid", "consumed", "AS-INS-001", "failed_lane_known"),
    (23, "turn_start", "turn_start_known_invalid", "consumed", "AS-TURN-001", "failed_lane_known"),
    (24, "execution", "policy_breach_known", "consumed", "AS-POL-001", "failed_lane_known"),
    (25, "execution", "timeout_terminal_interrupted_known", "consumed", "AS-TMO-001", "failed_lane_known"),
    (
        26,
        "execution",
        "timeout_or_interrupt_terminal_unknown",
        "consumed",
        "AS-TMO-UNK-001",
        "unknown_outcome_reconciliation_required",
    ),
    (27, "role_output", "role_output_known_invalid", "consumed", "AS-OUT-001", "failed_lane_known"),
    (28, "execution", "process_exit_before_terminal_known", "consumed", "AS-EXIT-001", "failed_lane_known"),
    (29, "receipt_sealing", "receipt_sealing_known_failure", "consumed", "AS-SEAL-001", "failed_lane_known"),
    (30, "receipt_staging", "staging_failure_cleanup_complete", "consumed", "AS-STG-001", "failed_lane_known"),
    (
        31,
        "receipt_publication",
        "final_collision_known",
        "consumed",
        "AS-COL-001",
        "unknown_outcome_reconciliation_required",
    ),
    (
        32,
        "receipt_publication",
        "commit_state_unknown",
        "consumed",
        "AS-CMT-UNK-001",
        "unknown_outcome_reconciliation_required",
    ),
    (33, "receipt_readback", "final_readback_known_invalid", "consumed", "AS-RDB-INV-001", "failed_lane_known"),
    (
        34,
        "receipt_readback",
        "final_readback_unknown",
        "consumed",
        "AS-RDB-UNK-001",
        "unknown_outcome_reconciliation_required",
    ),
    (35, "cleanup", "cleanup_known_incomplete", "consumed", "AS-CLN-FAIL-001", "failed_lane_known"),
    (36, "cleanup", "cleanup_unknown", "consumed", "AS-CLN-UNK-001", "unknown_outcome_reconciliation_required"),
    (
        37,
        "terminal",
        "required_fact_unknown_no_specific_case",
        "consumed",
        "AS-UNK-001",
        "unknown_outcome_reconciliation_required",
    ),
    (
        38,
        "terminal",
        "required_fact_known_invalid_no_specific_case",
        "consumed",
        "AS-KNOWN-FAIL-001",
        "failed_lane_known",
    ),
    (39, "terminal", "all_required_facts_valid", "consumed", "AS-ACC-001", None),
)

LIFECYCLE_CASE_COUNTS = (
    ("AS-BLK-001", 15),
    ("AS-CNS-REUSE-001", 1),
    ("AS-CNS-UNK-001", 1),
    ("AS-START-001", 1),
    ("AS-START-UNK-001", 1),
    ("AS-HSK-001", 1),
    ("AS-THR-001", 1),
    ("AS-INS-001", 1),
    ("AS-TURN-001", 1),
    ("AS-POL-001", 1),
    ("AS-TMO-001", 1),
    ("AS-TMO-UNK-001", 1),
    ("AS-OUT-001", 1),
    ("AS-EXIT-001", 1),
    ("AS-SEAL-001", 1),
    ("AS-STG-001", 1),
    ("AS-COL-001", 1),
    ("AS-CMT-UNK-001", 1),
    ("AS-RDB-INV-001", 1),
    ("AS-RDB-UNK-001", 1),
    ("AS-CLN-FAIL-001", 1),
    ("AS-CLN-UNK-001", 1),
    ("AS-UNK-001", 1),
    ("AS-KNOWN-FAIL-001", 1),
    ("AS-ACC-001", 1),
)

PROFILE_PROJECTION_COUNTS = (
    ("blocked_request_or_packet_invalid", 2),
    ("blocked_no_wip_authority", 1),
    ("blocked_skill_source_drift", 1),
    ("blocked_registry_missing_or_invalid", 1),
    ("blocked_release_state_invalid", 1),
    ("blocked_repository_inactive", 1),
    ("blocked_repository_identity_mismatch", 1),
    ("blocked_role_or_operation_not_allowed", 1),
    ("blocked_command_not_approved", 1),
    ("blocked_external_isolation_required", 1),
    ("blocked_mixed_profile_wave", 1),
    ("blocked_predecessor_packet_invalid", 1),
    ("blocked_cross_lane_overlap", 1),
    ("blocked_capacity_exceeded", 1),
    ("blocked_f_boundary", 1),
    ("failed_lane_known", 14),
    ("unknown_outcome_reconciliation_required", 8),
    (None, 1),
)

LIFECYCLE_REGISTRY_SHA256 = "0d50774b0b8cb4f47a11b2cde2919f73ac887dacced761dfa4ebd7ea95e4f517"

ALLOWED_NOTIFICATION_METHODS = {
    "thread/started",
    "thread/status/changed",
    "thread/tokenUsage/updated",
    "turn/started",
    "turn/completed",
    "turn/plan/updated",
    "item/started",
    "item/completed",
    "item/agentMessage/delta",
    "item/plan/delta",
    "item/reasoning/summaryPartAdded",
    "item/reasoning/summaryTextDelta",
    "item/reasoning/textDelta",
}
APPROVAL_REQUEST_METHODS = {
    "item/commandExecution/requestApproval",
    "item/fileChange/requestApproval",
}
ALLOWED_ITEM_TYPES = {"agentMessage", "reasoning", "plan"}
FORBIDDEN_VALUE_MARKERS = (
    "authorization:",
    "bearer ",
    "api_key",
    "credential",
    "password",
    "secret",
    "token",
)

MAX_JSON_LINE_BYTES = 1_048_576
MAX_STDOUT_BYTES = 67_108_864
MAX_MESSAGE_COUNT = 256
MAX_MESSAGE_QUEUE_BYTES = 8_388_608
TURN_TIMEOUT_SECONDS = 120

SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
REQUEST_ID_PATTERN = re.compile(r"^rp-(?:init|thread|turn|interrupt)-[0-9a-f]{32}$")


def lifecycle_case_projection(lifecycle_case: object) -> str | None:
    if not isinstance(lifecycle_case, str):
        return None
    projections = {
        row[5] for row in LIFECYCLE_ROWS if row[4] == lifecycle_case
    }
    if len(projections) != 1:
        return None
    projection = next(iter(projections))
    return projection if isinstance(projection, str) else None


class AppServerAdapterError(ValueError):
    """Symbolic, no-echo adapter failure."""

    def __init__(
        self,
        code: str,
        *,
        profile_projection: str | None = None,
    ) -> None:
        super().__init__(code)
        self.code = code
        self.profile_projection = (
            profile_projection
            if profile_projection is not None
            else lifecycle_case_projection(code)
        )


class FakeTransportTimeout(AppServerAdapterError):
    """Synthetic timeout emitted by an inert transport."""


class FakeTransportProcessExit(AppServerAdapterError):
    """Synthetic pre-terminal process exit emitted by an inert transport."""


class InertAppServerTransport(Protocol):
    """Closed test transport; production transports are not accepted in R0."""

    synthetic_only: bool
    process_start_count: int
    cleanup_status: str

    def request(self, message: Mapping[str, object]) -> object: ...

    def notify(self, message: Mapping[str, object]) -> None: ...

    def messages(self) -> Iterable[object]: ...

    def respond(self, message: Mapping[str, object]) -> None: ...


@dataclass(frozen=True)
class SyntheticPrivateContext:
    """Invented private values used only by fake-transport tests."""

    cwd: str
    codex_home: str
    skill_path: str
    agents_path: str
    agents_sha256: str


def _reject_duplicate_key(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AppServerAdapterError("duplicate_json_key")
        result[key] = value
    return result


def canonical_json_bytes(value: object, *, final_lf: bool) -> bytes:
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return encoded + (b"\n" if final_lf else b"")


def canonical_sha256(value: object, *, final_lf: bool) -> str:
    return hashlib.sha256(canonical_json_bytes(value, final_lf=final_lf)).hexdigest()


def _self_digest(value: Mapping[str, object], digest_field: str) -> str:
    preimage = {key: item for key, item in value.items() if key != digest_field}
    return canonical_sha256(preimage, final_lf=True)


def with_self_digest(
    value: Mapping[str, object],
    digest_field: str,
) -> dict[str, object]:
    result = dict(value)
    result[digest_field] = _self_digest(result, digest_field)
    return result


def decode_json_line(value: object) -> dict[str, object]:
    if not isinstance(value, (bytes, bytearray)):
        raise AppServerAdapterError("wire_bytes_required")
    raw = bytes(value)
    if len(raw) > MAX_JSON_LINE_BYTES:
        raise AppServerAdapterError("wire_line_limit_exceeded")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AppServerAdapterError("wire_bom_forbidden")
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n") or b"\r" in raw:
        raise AppServerAdapterError("wire_framing_invalid")
    if b"\n" in raw[:-1]:
        raise AppServerAdapterError("wire_framing_invalid")
    try:
        decoded = raw[:-1].decode("utf-8", errors="strict")
        document = json.loads(decoded, object_pairs_hook=_reject_duplicate_key)
    except AppServerAdapterError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AppServerAdapterError("wire_json_invalid") from exc
    if not isinstance(document, dict):
        raise AppServerAdapterError("wire_object_required")
    return document


def encode_json_line(value: Mapping[str, object]) -> bytes:
    return canonical_json_bytes(dict(value), final_lf=True)


def _strict_keys(
    value: object,
    fields: tuple[str, ...],
    code: str,
) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or tuple(value) != fields:
        raise AppServerAdapterError(code)
    return value


def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and SHA256_PATTERN.fullmatch(value) is not None


def _is_git_sha(value: object) -> bool:
    return isinstance(value, str) and GIT_SHA_PATTERN.fullmatch(value) is not None


def _is_nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value) and "\x00" not in value


def _whole_second_utc(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith("Z") or "." in value:
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def _decode_canonical_object(
    value: object,
    *,
    fields: tuple[str, ...] | None,
    code: str,
) -> Mapping[str, object]:
    if (
        not isinstance(value, str)
        or not value.endswith("\n")
        or value.endswith("\n\n")
        or "\r" in value
        or "\n" in value[:-1]
    ):
        raise AppServerAdapterError(code)
    try:
        decoded = json.loads(
            value[:-1],
            object_pairs_hook=_reject_duplicate_key,
        )
    except AppServerAdapterError:
        raise
    except json.JSONDecodeError as exc:
        raise AppServerAdapterError(code) from exc
    if not isinstance(decoded, Mapping):
        raise AppServerAdapterError(code)
    if fields is not None:
        _strict_keys(decoded, fields, code)
    if canonical_json_bytes(decoded, final_lf=True).decode("utf-8") != value:
        raise AppServerAdapterError(code)
    return decoded


def _validate_task_request(value: object) -> Mapping[str, object]:
    request = _strict_keys(
        value,
        TASK_REQUEST_FIELDS,
        "task_request_fields_invalid",
    )
    if request["schema_version"] != "trusted_owner_native_task_request.v1":
        raise AppServerAdapterError("task_request_schema_invalid")
    for field in (
        "request_sha256",
        "claim_observation_sha256",
        "lane_packet_sha256",
        "worktree_observation_sha256",
    ):
        if not _is_sha256(request[field]):
            raise AppServerAdapterError(f"{field}_invalid")
    if (
        not isinstance(request["repository_id"], int)
        or isinstance(request["repository_id"], bool)
        or request["repository_id"] <= 0
    ):
        raise AppServerAdapterError("repository_id_invalid")
    if not _is_nonempty_text(request["issue_url"]):
        raise AppServerAdapterError("issue_url_invalid")
    if request["role"] not in ROLE_CONTRACT_PATHS:
        raise AppServerAdapterError("task_request_role_invalid")
    if not _is_git_sha(request["base_sha"]):
        raise AppServerAdapterError("base_sha_invalid")
    if request["context_mode"] != "isolated_packet_only":
        raise AppServerAdapterError("context_mode_invalid")
    if request["fork_turns"] != "none":
        raise AppServerAdapterError("fork_turns_invalid")
    if not _whole_second_utc(request["issued_at_utc"]):
        raise AppServerAdapterError("issued_at_utc_invalid")
    if (
        not _is_sha256(request["task_request_sha256"])
        or request["task_request_sha256"]
        != _self_digest(request, "task_request_sha256")
    ):
        raise AppServerAdapterError("task_request_digest_invalid")
    return request


def _validate_lane_packet_json(value: object) -> Mapping[str, object]:
    lane = _decode_canonical_object(
        value,
        fields=LANE_PACKET_FIELDS,
        code="lane_packet_json_invalid",
    )
    if not _is_nonempty_text(lane["lane_id"]):
        raise AppServerAdapterError("lane_id_invalid")
    if (
        not isinstance(lane["repository_id"], int)
        or isinstance(lane["repository_id"], bool)
        or lane["repository_id"] <= 0
    ):
        raise AppServerAdapterError("lane_repository_id_invalid")
    for field in (
        "canonical_name",
        "issue_url",
        "base_ref",
    ):
        if not _is_nonempty_text(lane[field]):
            raise AppServerAdapterError(f"lane_{field}_invalid")
    if lane["role"] not in ROLE_CONTRACT_PATHS:
        raise AppServerAdapterError("lane_role_invalid")
    if lane["operation_id"] != "inspect":
        raise AppServerAdapterError("lane_operation_invalid")
    if not _is_git_sha(lane["base_sha"]):
        raise AppServerAdapterError("lane_base_sha_invalid")
    predecessor = lane["predecessor_packet_sha256"]
    if predecessor is not None and not _is_sha256(predecessor):
        raise AppServerAdapterError("lane_predecessor_invalid")
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
            raise AppServerAdapterError(f"lane_{field}_invalid")
    if (
        not _is_sha256(lane["lane_packet_sha256"])
        or lane["lane_packet_sha256"]
        != _self_digest(lane, "lane_packet_sha256")
    ):
        raise AppServerAdapterError("lane_packet_digest_invalid")
    return lane


def seal_instruction_packet(
    value: Mapping[str, object],
) -> dict[str, object]:
    if tuple(value) not in {
        INSTRUCTION_PACKET_FIELDS[:-1],
        INSTRUCTION_PACKET_FIELDS,
    }:
        raise AppServerAdapterError("instruction_packet_fields_invalid")
    result = dict(value)
    result.setdefault("instruction_packet_sha256", "")
    _strict_keys(
        result,
        INSTRUCTION_PACKET_FIELDS,
        "instruction_packet_fields_invalid",
    )
    if result["schema_version"] != INSTRUCTION_PACKET_SCHEMA:
        raise AppServerAdapterError("instruction_packet_schema_invalid")
    for field in (
        "task_request_sha256",
        "lane_packet_sha256",
        "role_contract_sha256",
        "role_pool_skill_sha256",
        "output_schema_sha256",
    ):
        if not _is_sha256(result[field]):
            raise AppServerAdapterError(f"{field}_invalid")
    role = result["role"]
    if role not in ROLE_CONTRACT_PATHS:
        raise AppServerAdapterError("instruction_packet_role_invalid")
    if result["operation_id"] != "inspect":
        raise AppServerAdapterError("instruction_packet_operation_invalid")
    if not _is_nonempty_text(result["issue_url"]):
        raise AppServerAdapterError("instruction_packet_issue_invalid")
    predecessor = result["predecessor_packet_sha256"]
    if predecessor is not None and not _is_sha256(predecessor):
        raise AppServerAdapterError("instruction_packet_predecessor_invalid")
    if result["role_contract_path"] != ROLE_CONTRACT_PATHS[str(role)]:
        raise AppServerAdapterError("role_contract_path_invalid")
    _validate_lane_packet_json(result["lane_packet_json"])
    predecessor_json = result["predecessor_packet_json"]
    if predecessor is None:
        if predecessor_json is not None:
            raise AppServerAdapterError("predecessor_packet_json_invalid")
    else:
        _decode_canonical_object(
            predecessor_json,
            fields=None,
            code="predecessor_packet_json_invalid",
        )
    result["instruction_packet_sha256"] = _self_digest(
        result,
        "instruction_packet_sha256",
    )
    return result


def validate_accepted_input_boundary(
    *,
    task_request: object,
    execution_binding: object,
    registry_entry: object,
    instruction_packet: object,
) -> list[str]:
    try:
        request = _validate_task_request(task_request)
        binding = _strict_keys(
            execution_binding,
            EXECUTION_BINDING_FIELDS,
            "execution_binding_fields_invalid",
        )
        if validate_execution_binding(binding):
            raise AppServerAdapterError("execution_binding_invalid")
        packet = _decode_canonical_object(
            instruction_packet,
            fields=INSTRUCTION_PACKET_FIELDS,
            code="instruction_packet_invalid",
        )
        expected_packet = seal_instruction_packet(packet)
        if (
            packet["instruction_packet_sha256"]
            != expected_packet["instruction_packet_sha256"]
        ):
            raise AppServerAdapterError("instruction_packet_digest_invalid")
        lane = _validate_lane_packet_json(packet["lane_packet_json"])
    except AppServerAdapterError as exc:
        return [exc.code]

    errors: list[str] = []
    for field in (
        "task_request_sha256",
        "request_sha256",
        "claim_observation_sha256",
        "lane_packet_sha256",
        "worktree_observation_sha256",
        "repository_id",
        "issue_url",
        "role",
    ):
        if request[field] != binding[field]:
            errors.append(f"{field}_binding_mismatch")
    for field in (
        "lane_packet_sha256",
        "repository_id",
        "issue_url",
        "role",
        "base_sha",
    ):
        if request[field] != lane[field]:
            errors.append(f"lane_{field}_binding_mismatch")
    if lane["operation_id"] != binding["operation_id"]:
        errors.append("operation_id_binding_mismatch")
    if (
        lane["predecessor_packet_sha256"]
        != binding["predecessor_packet_sha256"]
    ):
        errors.append("predecessor_packet_binding_mismatch")
    packet_bindings = {
        "task_request_sha256": request["task_request_sha256"],
        "lane_packet_sha256": lane["lane_packet_sha256"],
        "role": request["role"],
        "operation_id": lane["operation_id"],
        "issue_url": request["issue_url"],
        "predecessor_packet_sha256": lane["predecessor_packet_sha256"],
        "role_pool_skill_sha256": binding["role_pool_skill_sha256"],
        "output_schema_sha256": binding["output_schema_sha256"],
        "instruction_packet_sha256": binding["instruction_packet_sha256"],
    }
    for field, expected in packet_bindings.items():
        if packet[field] != expected:
            errors.append(f"instruction_packet_{field}_binding_mismatch")
    errors.extend(
        validate_inspect_only_effect_boundary(
            request,
            lane,
            registry_entry,
            turn_timeout_seconds=binding["turn_timeout_seconds"],
        )
    )
    return errors


def _utc_now(clock: object = None) -> str:
    now = clock() if callable(clock) else datetime.now(timezone.utc)
    if not isinstance(now, datetime):
        raise AppServerAdapterError("clock_invalid")
    if now.tzinfo is None:
        raise AppServerAdapterError("clock_invalid")
    normalized = now.astimezone(timezone.utc).replace(microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")


def _domain_digest(domain: str, value: str) -> str:
    return hashlib.sha256(domain.encode("ascii") + b"\x00" + value.encode("utf-8")).hexdigest()


def lifecycle_registry_document() -> dict[str, object]:
    return {
        "schema_version": LIFECYCLE_REGISTRY_SCHEMA,
        "fields": list(LIFECYCLE_FIELDS),
        "rows": [list(row) for row in LIFECYCLE_ROWS],
        "lifecycle_case_counts": [list(row) for row in LIFECYCLE_CASE_COUNTS],
        "profile_projection_counts": [list(row) for row in PROFILE_PROJECTION_COUNTS],
    }


def validate_lifecycle_registry() -> dict[str, object]:
    document = lifecycle_registry_document()
    encoded = canonical_json_bytes(document, final_lf=True)
    if len(encoded) != 5_614:
        raise AppServerAdapterError("lifecycle_registry_byte_count_invalid")
    if hashlib.sha256(encoded).hexdigest() != LIFECYCLE_REGISTRY_SHA256:
        raise AppServerAdapterError("lifecycle_registry_digest_invalid")
    if len(LIFECYCLE_ROWS) != 39:
        raise AppServerAdapterError("lifecycle_registry_row_count_invalid")
    if tuple(row[0] for row in LIFECYCLE_ROWS) != tuple(range(1, 40)):
        raise AppServerAdapterError("lifecycle_registry_ordinal_invalid")
    if len(set((row[1], row[2], row[3]) for row in LIFECYCLE_ROWS)) != 39:
        raise AppServerAdapterError("lifecycle_registry_overlap")
    reached = {select_lifecycle_case(row[1], row[2], row[3])["ordinal"] for row in LIFECYCLE_ROWS}
    if reached != set(range(1, 40)):
        raise AppServerAdapterError("lifecycle_registry_unreachable")
    return {
        "tuple_count": 39,
        "overlap_count": 0,
        "uncovered_count": 0,
        "unreachable_row_count": 0,
        "sha256": LIFECYCLE_REGISTRY_SHA256,
    }


def select_lifecycle_case(
    phase: object,
    raw_observation: object,
    consumption_state: object,
) -> dict[str, object]:
    if not all(isinstance(value, str) for value in (phase, raw_observation, consumption_state)):
        raise AppServerAdapterError("lifecycle_tuple_type_invalid")
    matches = [
        row for row in LIFECYCLE_ROWS if row[1] == phase and row[2] == raw_observation and row[3] == consumption_state
    ]
    if len(matches) == 1:
        row = matches[0]
    elif consumption_state == "not_consumed":
        row = LIFECYCLE_ROWS[0]
    elif consumption_state in {"consumed", "unknown"}:
        row = LIFECYCLE_ROWS[36]
    else:
        raise AppServerAdapterError("lifecycle_tuple_invalid")
    return {
        "ordinal": row[0],
        "lifecycle_case": row[4],
        "profile_projection": row[5],
    }


def validate_fixed_contract_bytes() -> dict[str, object]:
    instruction = DEVELOPER_INSTRUCTION.encode("utf-8")
    schema = ROLE_OUTPUT_SCHEMA_JSON.encode("utf-8")
    config = INSPECT_ONLY_CONFIG.encode("utf-8")
    if len(instruction) != 292 or hashlib.sha256(instruction).hexdigest() != DEVELOPER_INSTRUCTION_SHA256:
        raise AppServerAdapterError("developer_instruction_binding_invalid")
    if len(schema) != 1_663 or hashlib.sha256(schema).hexdigest() != ROLE_OUTPUT_SCHEMA_SHA256:
        raise AppServerAdapterError("role_output_schema_binding_invalid")
    if len(config) != 780 or hashlib.sha256(config).hexdigest() != INSPECT_ONLY_CONFIG_SHA256:
        raise AppServerAdapterError("inspect_config_binding_invalid")
    if config.count(b" = false\n") != 32:
        raise AppServerAdapterError("inspect_config_feature_count_invalid")
    return {
        "developer_instruction_sha256": DEVELOPER_INSTRUCTION_SHA256,
        "role_output_schema_sha256": ROLE_OUTPUT_SCHEMA_SHA256,
        "inspect_config_sha256": INSPECT_ONLY_CONFIG_SHA256,
    }


def validate_inspect_only_effect_boundary(
    task_request: object,
    lane: object,
    registry_entry: object,
    *,
    turn_timeout_seconds: object,
) -> list[str]:
    errors: list[str] = []
    if (
        not isinstance(task_request, Mapping)
        or tuple(task_request) != TASK_REQUEST_FIELDS
    ):
        return ["task_request_invalid"]
    if not isinstance(lane, Mapping) or tuple(lane) != LANE_PACKET_FIELDS:
        return ["lane_invalid"]
    if (
        not isinstance(registry_entry, Mapping)
        or tuple(registry_entry) != INSPECT_REGISTRY_PROJECTION_FIELDS
    ):
        return ["registry_entry_invalid"]
    if task_request.get("role") not in {"B", "E"}:
        errors.append("role_not_inspect_only")
    if lane.get("role") != task_request.get("role"):
        errors.append("role_binding_mismatch")
    if lane.get("operation_id") != "inspect":
        errors.append("operation_not_inspect")
    if lane.get("lane_packet_sha256") != task_request.get("lane_packet_sha256"):
        errors.append("lane_packet_binding_mismatch")
    if lane.get("repository_id") != task_request.get("repository_id"):
        errors.append("repository_id_binding_mismatch")
    if registry_entry.get("repository_id") != task_request.get("repository_id"):
        errors.append("registry_repository_id_binding_mismatch")
    if registry_entry.get("repository_code_execution_policy") != "forbidden":
        errors.append("repository_code_execution_policy_invalid")
    for field in (
        "command_ids",
        "validation_command_ids",
        "mutation_scope",
        "expected_artifact_paths",
    ):
        if lane.get(field) != []:
            errors.append(f"{field}_not_empty")
    for field in ("maximum_mutation_scope", "approved_commands"):
        if registry_entry.get(field) != []:
            errors.append(f"{field}_not_empty")
    if turn_timeout_seconds != TURN_TIMEOUT_SECONDS:
        errors.append("turn_timeout_invalid")
    return errors


def seal_execution_binding(value: Mapping[str, object]) -> dict[str, object]:
    if tuple(value) not in {EXECUTION_BINDING_FIELDS[:-1], EXECUTION_BINDING_FIELDS}:
        raise AppServerAdapterError("execution_binding_fields_invalid")
    result = dict(value)
    result.setdefault("execution_binding_sha256", "")
    _strict_keys(result, EXECUTION_BINDING_FIELDS, "execution_binding_fields_invalid")
    if result["schema_version"] != EXECUTION_BINDING_SCHEMA:
        raise AppServerAdapterError("execution_binding_schema_invalid")
    fixed = {
        "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
        "companion_contract_sha256": COMPANION_CONTRACT_SHA256,
        "executable_sha256": PINNED_EXECUTABLE_SHA256,
        "protocol_schema_sha256": PINNED_PROTOCOL_SCHEMA_SHA256,
        "role_instruction_sha256": DEVELOPER_INSTRUCTION_SHA256,
        "output_schema_sha256": ROLE_OUTPUT_SCHEMA_SHA256,
    }
    for field, expected in fixed.items():
        if result[field] != expected:
            raise AppServerAdapterError(f"{field}_invalid")
    for field in (
        "profile_contract_sha256",
        "companion_contract_sha256",
        "task_request_sha256",
        "request_sha256",
        "claim_observation_sha256",
        "lane_packet_sha256",
        "worktree_observation_sha256",
        "registry_sha256",
        "release_state_record_sha256",
        "skill_tree_sha256",
        "cwd_identity_sha256",
        "sandbox_binding_sha256",
        "role_instruction_sha256",
        "instruction_packet_sha256",
        "role_pool_skill_sha256",
        "output_schema_sha256",
        "installation_receipt_sha256",
        "executable_sha256",
        "protocol_schema_sha256",
        "runtime_config_manifest_sha256",
        "environment_binding_sha256",
    ):
        if not _is_sha256(result[field]):
            raise AppServerAdapterError(f"{field}_invalid")
    if result["role"] not in {"B", "E"} or result["operation_id"] != "inspect":
        raise AppServerAdapterError("execution_binding_role_or_operation_invalid")
    if result["model_request_mode"] != "platform_default_then_bind_thread_response":
        raise AppServerAdapterError("model_request_mode_invalid")
    if result["requested_model"] is not None or result["requested_effort"] is not None:
        raise AppServerAdapterError("requested_model_or_effort_invalid")
    if result["approval_policy"] != "untrusted":
        raise AppServerAdapterError("approval_policy_invalid")
    if result["turn_timeout_seconds"] != TURN_TIMEOUT_SECONDS:
        raise AppServerAdapterError("turn_timeout_invalid")
    if (
        not isinstance(result["repository_id"], int)
        or isinstance(result["repository_id"], bool)
        or result["repository_id"] <= 0
    ):
        raise AppServerAdapterError("repository_id_invalid")
    if not _is_nonempty_text(result["issue_url"]):
        raise AppServerAdapterError("issue_url_invalid")
    predecessor = result["predecessor_packet_sha256"]
    if predecessor is not None and not _is_sha256(predecessor):
        raise AppServerAdapterError("predecessor_packet_sha256_invalid")
    result["execution_binding_sha256"] = _self_digest(result, "execution_binding_sha256")
    return result


def validate_execution_binding(value: object) -> list[str]:
    try:
        binding = _strict_keys(value, EXECUTION_BINDING_FIELDS, "execution_binding_fields_invalid")
        expected = seal_execution_binding(binding)
        if binding["execution_binding_sha256"] != expected["execution_binding_sha256"]:
            raise AppServerAdapterError("execution_binding_digest_invalid")
    except AppServerAdapterError as exc:
        return [exc.code]
    return []


def request_ids(task_request_sha256: object) -> dict[str, str]:
    if not _is_sha256(task_request_sha256):
        raise AppServerAdapterError("task_request_sha256_invalid")
    prefix = str(task_request_sha256)[:32]
    return {
        "initialize": f"rp-init-{prefix}",
        "thread_start": f"rp-thread-{prefix}",
        "turn_start": f"rp-turn-{prefix}",
        "interrupt": f"rp-interrupt-{prefix}",
        "client_message": f"rp-message-{prefix}",
    }


def _contains_private_value(value: object, private_values: tuple[str, ...]) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(item.lower() in lowered for item in private_values if item)
    if isinstance(value, Mapping):
        return any(_contains_private_value(item, private_values) for item in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains_private_value(item, private_values) for item in value)
    return False


def validate_role_output(
    value: object,
    *,
    private_values: Iterable[str] = (),
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, Mapping) or tuple(value) != ROLE_OUTPUT_FIELDS:
        return ["role_output_fields_invalid"]
    if value["schema_version"] != ROLE_OUTPUT_SCHEMA_VERSION:
        errors.append("role_output_schema_invalid")
    if value["result"] not in {"completed", "blocked", "finding"}:
        errors.append("role_output_result_invalid")
    if value["files_changed"] != []:
        errors.append("role_output_files_changed_not_empty")
    if value["validation"] != []:
        errors.append("role_output_validation_not_empty")
    handoff = value["handoff"]
    if not isinstance(handoff, Mapping) or tuple(handoff) != HANDOFF_FIELDS:
        errors.append("role_output_handoff_invalid")
    else:
        if handoff["status"] not in {"blocked", "changes_required", "complete", "no_next_role"}:
            errors.append("role_output_handoff_status_invalid")
        if handoff["next_role"] not in {"A", "B", "C", "D", "E", "F", "G", "H", None}:
            errors.append("role_output_handoff_next_role_invalid")
        for field in ("source_artifact_paths", "finding_ids"):
            values = handoff[field]
            if (
                not isinstance(values, list)
                or any(not _is_nonempty_text(item) for item in values)
                or values != sorted(set(values))
            ):
                errors.append(f"role_output_handoff_{field}_invalid")
        if handoff["stop_reason"] is not None and not _is_nonempty_text(handoff["stop_reason"]):
            errors.append("role_output_handoff_stop_reason_invalid")
        if value["result"] == "blocked" and handoff["status"] != "blocked":
            errors.append("role_output_handoff_result_mismatch")
        if value["result"] == "finding" and handoff["status"] != "changes_required":
            errors.append("role_output_handoff_result_mismatch")
        if value["result"] == "completed" and handoff["status"] not in {"complete", "no_next_role"}:
            errors.append("role_output_handoff_result_mismatch")
    private_tuple = tuple(private_values)
    if _contains_private_value(value, private_tuple):
        errors.append("role_output_private_value_echo")
    projection = json.dumps(value, ensure_ascii=True, separators=(",", ":")).lower()
    if any(marker in projection for marker in FORBIDDEN_VALUE_MARKERS):
        errors.append("role_output_private_marker")
    return errors


def _coerce_wire_message(value: object) -> tuple[dict[str, object], int]:
    if isinstance(value, Mapping):
        encoded = encode_json_line(value)
        return dict(value), len(encoded)
    document = decode_json_line(value)
    assert isinstance(value, (bytes, bytearray))
    return document, len(value)


def _validate_response(value: object, request_id: str, phase: str) -> Mapping[str, object]:
    response, _ = _coerce_wire_message(value)
    response = _strict_keys(response, ("id", "result"), f"{phase}_response_fields_invalid")
    if response["id"] != request_id:
        raise AppServerAdapterError(f"{phase}_response_id_invalid")
    if not isinstance(response["result"], Mapping):
        raise AppServerAdapterError(f"{phase}_response_result_invalid")
    return response["result"]


def _initialize_params() -> dict[str, object]:
    return {
        "clientInfo": {
            "name": "mythic-edge-role-pool",
            "title": "Mythic Edge Role Pool",
            "version": "1",
        },
        "capabilities": {
            "experimentalApi": False,
            "mcpServerOpenaiFormElicitation": False,
            "optOutNotificationMethods": None,
            "requestAttestation": False,
        },
    }


def _instruction_sources_digest(agents_sha256: str) -> str:
    return canonical_sha256(
        [{"relative_path": "AGENTS.md", "sha256": agents_sha256}],
        final_lf=True,
    )


def _terminal_projection(
    *,
    method: str,
    thread_id_sha256: str,
    turn_id_sha256: str,
    terminal_status: str,
    received_at_utc: str,
) -> str:
    return canonical_sha256(
        {
            "method": method,
            "thread_id_sha256": thread_id_sha256,
            "turn_id_sha256": turn_id_sha256,
            "terminal_status": terminal_status,
            "received_at_utc": received_at_utc,
        },
        final_lf=True,
    )


def _validate_thread_result(
    result: Mapping[str, object],
    context: SyntheticPrivateContext,
) -> tuple[str, str, str]:
    thread = result.get("thread")
    if not isinstance(thread, Mapping):
        raise AppServerAdapterError("thread_start_result_invalid")
    expected_fields = (
        "id",
        "ephemeral",
        "turns",
        "parentThreadId",
        "forkedFromThreadId",
        "cwd",
        "approvalPolicy",
        "approvalsReviewer",
        "sandbox",
        "model",
        "reasoningEffort",
        "instructionSources",
    )
    _strict_keys(thread, expected_fields, "thread_start_result_fields_invalid")
    if not _is_nonempty_text(thread["id"]):
        raise AppServerAdapterError("thread_id_invalid")
    if (
        thread["ephemeral"] is not True
        or thread["turns"] != []
        or thread["parentThreadId"] is not None
        or thread["forkedFromThreadId"] is not None
        or thread["cwd"] != context.cwd
        or thread["approvalPolicy"] != "untrusted"
        or thread["approvalsReviewer"] != "user"
        or thread["sandbox"] != "read-only"
    ):
        raise AppServerAdapterError("thread_binding_invalid")
    if not _is_nonempty_text(thread["model"]) or not _is_nonempty_text(thread["reasoningEffort"]):
        raise AppServerAdapterError("thread_model_or_effort_invalid")
    if thread["instructionSources"] != [context.agents_path]:
        raise AppServerAdapterError("instruction_sources_invalid")
    return str(thread["id"]), str(thread["model"]), str(thread["reasoningEffort"])


def _validate_turn_result(result: Mapping[str, object]) -> str:
    turn = result.get("turn")
    if not isinstance(turn, Mapping) or tuple(turn) != ("id", "status"):
        raise AppServerAdapterError("turn_start_result_invalid")
    if not _is_nonempty_text(turn["id"]) or turn["status"] != "inProgress":
        raise AppServerAdapterError("turn_start_binding_invalid")
    return str(turn["id"])


def _make_outbound_request(
    request_id: str,
    method: str,
    params: Mapping[str, object],
) -> dict[str, object]:
    if REQUEST_ID_PATTERN.fullmatch(request_id) is None:
        raise AppServerAdapterError("request_id_invalid")
    return {"id": request_id, "method": method, "params": dict(params)}


def _failure_result(
    phase: str,
    raw_observation: str,
    consumption_state: str,
    *,
    process_start_calls: int,
    automatic_retry_count: int = 0,
    fallback_attempt_count: int = 0,
) -> dict[str, object]:
    selected = select_lifecycle_case(phase, raw_observation, consumption_state)
    return {
        "status": selected["profile_projection"],
        "lifecycle_case": selected["lifecycle_case"],
        "profile_projection": selected["profile_projection"],
        "platform_receipt": None,
        "task_receipt": None,
        "actual_process_start_count": process_start_calls,
        "automatic_retry_count": automatic_retry_count,
        "fallback_attempt_count": fallback_attempt_count,
        "durable_write_count": 0,
        "synthetic_only": True,
        "live_ready": False,
    }


def _platform_receipt(
    *,
    binding: Mapping[str, object],
    ids: Mapping[str, str],
    thread_id: str,
    turn_id: str,
    model: str,
    effort: str,
    instruction_sources_sha256: str,
    terminal_notification_sha256: str,
    role_output_sha256: str,
    started_at_utc: str,
    terminal_at_utc: str,
) -> dict[str, object]:
    receipt = {
        "schema_version": PLATFORM_RECEIPT_SCHEMA,
        "task_request_sha256": binding["task_request_sha256"],
        "execution_binding_sha256": binding["execution_binding_sha256"],
        "installation_receipt_sha256": binding["installation_receipt_sha256"],
        "executable_sha256": binding["executable_sha256"],
        "protocol_schema_sha256": binding["protocol_schema_sha256"],
        "initialize_request_id": ids["initialize"],
        "thread_start_request_id": ids["thread_start"],
        "turn_start_request_id": ids["turn_start"],
        "interrupt_request_id": None,
        "thread_id_sha256": _domain_digest("app_server_thread_id", thread_id),
        "turn_id_sha256": _domain_digest("app_server_turn_id", turn_id),
        "effective_model_sha256": _domain_digest("app_server_effective_model", model),
        "effective_effort_sha256": _domain_digest("app_server_effective_effort", effort),
        "instruction_sources_sha256": instruction_sources_sha256,
        "process_start_count": 1,
        "initialize_count": 1,
        "initialized_count": 1,
        "thread_start_count": 1,
        "turn_start_count": 1,
        "interrupt_count": 0,
        "command_approval_count": 0,
        "file_change_approval_count": 0,
        "terminal_notification_sha256": terminal_notification_sha256,
        "role_output_sha256": role_output_sha256,
        "lifecycle_case": "AS-ACC-001",
        "profile_terminal_projection": None,
        "process_exit_class": "exited_zero",
        "cleanup_status": "complete",
        "started_at_utc": started_at_utc,
        "terminal_at_utc": terminal_at_utc,
        "platform_receipt_sha256": "",
    }
    return with_self_digest(receipt, "platform_receipt_sha256")


def validate_platform_receipt(value: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, Mapping) or tuple(value) != PLATFORM_RECEIPT_FIELDS:
        return ["platform_receipt_fields_invalid"]
    if value["schema_version"] != PLATFORM_RECEIPT_SCHEMA:
        errors.append("platform_receipt_schema_invalid")
    for field in (
        "task_request_sha256",
        "execution_binding_sha256",
        "installation_receipt_sha256",
        "executable_sha256",
        "protocol_schema_sha256",
        "thread_id_sha256",
        "turn_id_sha256",
        "effective_model_sha256",
        "effective_effort_sha256",
        "instruction_sources_sha256",
        "terminal_notification_sha256",
        "role_output_sha256",
    ):
        if not _is_sha256(value[field]):
            errors.append(f"{field}_invalid")
    for field in ("initialize_request_id", "thread_start_request_id", "turn_start_request_id"):
        if not isinstance(value[field], str) or REQUEST_ID_PATTERN.fullmatch(value[field]) is None:
            errors.append(f"{field}_invalid")
    if value["interrupt_request_id"] is not None:
        errors.append("interrupt_request_id_invalid")
    expected_counts = {
        "process_start_count": 1,
        "initialize_count": 1,
        "initialized_count": 1,
        "thread_start_count": 1,
        "turn_start_count": 1,
        "interrupt_count": 0,
        "command_approval_count": 0,
        "file_change_approval_count": 0,
    }
    for field, expected in expected_counts.items():
        if value[field] != expected:
            errors.append(f"{field}_invalid")
    if (
        value["lifecycle_case"] != "AS-ACC-001"
        or value["profile_terminal_projection"] is not None
        or value["process_exit_class"] != "exited_zero"
        or value["cleanup_status"] != "complete"
    ):
        errors.append("platform_receipt_terminal_invalid")
    if not _whole_second_utc(value["started_at_utc"]) or not _whole_second_utc(value["terminal_at_utc"]):
        errors.append("platform_receipt_timestamp_invalid")
    if value["platform_receipt_sha256"] != _self_digest(value, "platform_receipt_sha256"):
        errors.append("platform_receipt_digest_invalid")
    return errors


def _task_receipt(
    task_request_sha256: str,
    platform_receipt: Mapping[str, object],
    accepted_at_utc: str,
) -> dict[str, object]:
    thread_digest = str(platform_receipt["thread_id_sha256"])
    platform_digest = str(platform_receipt["platform_receipt_sha256"])
    receipt = {
        "schema_version": "trusted_owner_native_task_receipt.v1",
        "task_request_sha256": task_request_sha256,
        "task_id": f"app_server_{thread_digest[:32]}",
        "accepted_at_utc": accepted_at_utc,
        "platform_receipt_ref": f"role_pool:app_server:{platform_digest[:32]}",
        "platform_receipt_sha256": platform_digest,
        "task_receipt_sha256": "",
    }
    return with_self_digest(receipt, "task_receipt_sha256")


def _validate_initialize_result(
    result: Mapping[str, object],
    context: SyntheticPrivateContext,
) -> None:
    expected = ("platformFamily", "platformOs", "userAgent", "codexHome")
    _strict_keys(result, expected, "initialize_result_fields_invalid")
    if result["platformFamily"] != "windows" or result["platformOs"] != "windows":
        raise AppServerAdapterError("initialize_platform_invalid")
    if result["userAgent"] != f"codex-cli/{PINNED_CODEX_VERSION}":
        raise AppServerAdapterError("initialize_version_invalid")
    if result["codexHome"] != context.codex_home:
        raise AppServerAdapterError("initialize_codex_home_invalid")


def _turn_params(
    *,
    ids: Mapping[str, str],
    thread_id: str,
    model: str,
    effort: str,
    context: SyntheticPrivateContext,
    instruction_packet: str,
) -> dict[str, object]:
    return {
        "approvalPolicy": "untrusted",
        "approvalsReviewer": "user",
        "clientUserMessageId": ids["client_message"],
        "cwd": context.cwd,
        "effort": effort,
        "input": [
            {
                "type": "text",
                "text": instruction_packet,
                "text_elements": [],
            },
            {
                "type": "skill",
                "name": "mythic-edge-role-pool",
                "path": context.skill_path,
            },
        ],
        "model": model,
        "outputSchema": json.loads(ROLE_OUTPUT_SCHEMA_JSON),
        "personality": None,
        "sandboxPolicy": {"networkAccess": False, "type": "readOnly"},
        "serviceTier": None,
        "summary": None,
        "threadId": thread_id,
    }


def _thread_params(context: SyntheticPrivateContext) -> dict[str, object]:
    return {
        "approvalPolicy": "untrusted",
        "approvalsReviewer": "user",
        "baseInstructions": None,
        "config": None,
        "cwd": context.cwd,
        "developerInstructions": DEVELOPER_INSTRUCTION,
        "ephemeral": True,
        "model": None,
        "modelProvider": None,
        "personality": None,
        "sandbox": "read-only",
        "serviceName": "mythic-edge-role-pool",
        "serviceTier": None,
        "sessionStartSource": None,
        "threadSource": None,
    }


def _validate_event_identity(
    params: Mapping[str, object],
    thread_id: str,
    turn_id: str | None,
) -> None:
    if params.get("threadId") != thread_id:
        raise AppServerAdapterError("event_thread_id_invalid")
    if turn_id is not None and "turnId" in params and params.get("turnId") != turn_id:
        raise AppServerAdapterError("event_turn_id_invalid")


def _process_events(
    transport: InertAppServerTransport,
    *,
    thread_id: str,
    turn_id: str,
    context: SyntheticPrivateContext,
    clock: object,
) -> tuple[Mapping[str, object], str, str]:
    total_bytes = 0
    count = 0
    terminal_output: Mapping[str, object] | None = None
    terminal_status: str | None = None
    terminal_time: str | None = None
    for raw_message in transport.messages():
        message, byte_count = _coerce_wire_message(raw_message)
        count += 1
        total_bytes += byte_count
        if count > MAX_MESSAGE_COUNT or total_bytes > MAX_MESSAGE_QUEUE_BYTES or total_bytes > MAX_STDOUT_BYTES:
            raise AppServerAdapterError("message_queue_limit_exceeded")
        if "id" in message:
            request = _strict_keys(message, ("id", "method", "params"), "server_request_fields_invalid")
            if request["method"] in APPROVAL_REQUEST_METHODS:
                params = request["params"]
                if not isinstance(params, Mapping):
                    raise AppServerAdapterError("server_request_params_invalid")
                _validate_event_identity(params, thread_id, turn_id)
                transport.respond(
                    {
                        "id": request["id"],
                        "result": {"decision": "decline"},
                    }
                )
                raise AppServerAdapterError("policy_breach_known")
            raise AppServerAdapterError("policy_breach_known")
        notification = _strict_keys(message, ("method", "params"), "notification_fields_invalid")
        method = notification["method"]
        params = notification["params"]
        if method not in ALLOWED_NOTIFICATION_METHODS or not isinstance(params, Mapping):
            raise AppServerAdapterError("policy_breach_known")
        _validate_event_identity(params, thread_id, turn_id)
        if method == "model/rerouted":
            raise AppServerAdapterError("policy_breach_known")
        if method in {"item/started", "item/completed"}:
            item = params.get("item")
            if not isinstance(item, Mapping) or item.get("type") not in ALLOWED_ITEM_TYPES:
                raise AppServerAdapterError("policy_breach_known")
        if method == "turn/completed":
            if terminal_output is not None:
                raise AppServerAdapterError("policy_breach_known")
            if params.get("turnId") != turn_id or params.get("status") != "completed":
                raise AppServerAdapterError("role_output_known_invalid")
            output = params.get("output")
            errors = validate_role_output(
                output,
                private_values=(
                    context.cwd,
                    context.codex_home,
                    context.skill_path,
                    context.agents_path,
                ),
            )
            if errors:
                raise AppServerAdapterError("role_output_known_invalid")
            assert isinstance(output, Mapping)
            terminal_output = output
            terminal_status = "completed"
            terminal_time = _utc_now(clock)
    if terminal_output is None or terminal_status is None or terminal_time is None:
        raise AppServerAdapterError("required_fact_unknown_no_specific_case")
    return terminal_output, terminal_status, terminal_time


def run_inert_app_server_once(
    *,
    task_request: Mapping[str, object],
    execution_binding: Mapping[str, object],
    registry_entry: Mapping[str, object],
    private_context: SyntheticPrivateContext,
    instruction_packet: str,
    transport: InertAppServerTransport,
    clock: object = None,
) -> dict[str, object]:
    """Exercise one fake App Server lifecycle without process or durable effects."""

    try:
        validate_fixed_contract_bytes()
        validate_lifecycle_registry()
        if validate_accepted_input_boundary(
            task_request=task_request,
            execution_binding=execution_binding,
            registry_entry=registry_entry,
            instruction_packet=instruction_packet,
        ):
            raise AppServerAdapterError("accepted_input_boundary_invalid")
        if not _is_sha256(private_context.agents_sha256):
            raise AppServerAdapterError("agents_binding_invalid")
        if (
            getattr(transport, "synthetic_only", False) is not True
            or getattr(transport, "process_start_count", None) != 0
        ):
            raise AppServerAdapterError("fake_transport_required")
    except AppServerAdapterError:
        return _failure_result(
            "preflight",
            "profile_priority_01_request_or_packet_invalid",
            "not_consumed",
            process_start_calls=0,
        )

    ids = request_ids(str(task_request["task_request_sha256"]))
    started_at = _utc_now(clock)
    try:
        initialize_result = _validate_response(
            transport.request(
                _make_outbound_request(
                    ids["initialize"],
                    "initialize",
                    _initialize_params(),
                )
            ),
            ids["initialize"],
            "initialize",
        )
        _validate_initialize_result(initialize_result, private_context)
        transport.notify({"method": "initialized", "params": {}})

        thread_result = _validate_response(
            transport.request(
                _make_outbound_request(
                    ids["thread_start"],
                    "thread/start",
                    _thread_params(private_context),
                )
            ),
            ids["thread_start"],
            "thread_start",
        )
        thread_id, model, effort = _validate_thread_result(thread_result, private_context)

        turn_result = _validate_response(
            transport.request(
                _make_outbound_request(
                    ids["turn_start"],
                    "turn/start",
                    _turn_params(
                        ids=ids,
                        thread_id=thread_id,
                        model=model,
                        effort=effort,
                        context=private_context,
                        instruction_packet=instruction_packet,
                    ),
                )
            ),
            ids["turn_start"],
            "turn_start",
        )
        turn_id = _validate_turn_result(turn_result)
        role_output, terminal_status, terminal_time = _process_events(
            transport,
            thread_id=thread_id,
            turn_id=turn_id,
            context=private_context,
            clock=clock,
        )
    except FakeTransportTimeout:
        return _failure_result(
            "execution",
            "timeout_or_interrupt_terminal_unknown",
            "consumed",
            process_start_calls=getattr(transport, "process_start_count", 0),
        )
    except FakeTransportProcessExit:
        return _failure_result(
            "execution",
            "process_exit_before_terminal_known",
            "consumed",
            process_start_calls=getattr(transport, "process_start_count", 0),
        )
    except AppServerAdapterError as exc:
        mapping = {
            "policy_breach_known": ("execution", "policy_breach_known"),
            "role_output_known_invalid": ("role_output", "role_output_known_invalid"),
            "required_fact_unknown_no_specific_case": (
                "terminal",
                "required_fact_unknown_no_specific_case",
            ),
        }
        phase, observation = mapping.get(exc.code, ("terminal", "required_fact_known_invalid_no_specific_case"))
        return _failure_result(
            phase,
            observation,
            "consumed",
            process_start_calls=getattr(transport, "process_start_count", 0),
        )

    if getattr(transport, "process_start_count", None) != 0:
        return _failure_result(
            "execution",
            "policy_breach_known",
            "consumed",
            process_start_calls=getattr(transport, "process_start_count", 0),
        )
    if getattr(transport, "cleanup_status", None) != "complete":
        observation = (
            "cleanup_known_incomplete"
            if getattr(transport, "cleanup_status", None) == "known_incomplete"
            else "cleanup_unknown"
        )
        return _failure_result(
            "cleanup",
            observation,
            "consumed",
            process_start_calls=0,
        )

    thread_digest = _domain_digest("app_server_thread_id", thread_id)
    turn_digest = _domain_digest("app_server_turn_id", turn_id)
    terminal_digest = _terminal_projection(
        method="turn/completed",
        thread_id_sha256=thread_digest,
        turn_id_sha256=turn_digest,
        terminal_status=terminal_status,
        received_at_utc=terminal_time,
    )
    role_output_digest = canonical_sha256(role_output, final_lf=True)
    platform_receipt = _platform_receipt(
        binding=execution_binding,
        ids=ids,
        thread_id=thread_id,
        turn_id=turn_id,
        model=model,
        effort=effort,
        instruction_sources_sha256=_instruction_sources_digest(private_context.agents_sha256),
        terminal_notification_sha256=terminal_digest,
        role_output_sha256=role_output_digest,
        started_at_utc=started_at,
        terminal_at_utc=terminal_time,
    )
    if validate_platform_receipt(platform_receipt):
        return _failure_result(
            "receipt_sealing",
            "receipt_sealing_known_failure",
            "consumed",
            process_start_calls=0,
        )
    task_receipt = _task_receipt(
        str(task_request["task_request_sha256"]),
        platform_receipt,
        terminal_time,
    )
    return {
        "status": "synthetic_app_server_receipt_accepted_non_live",
        "lifecycle_case": "AS-ACC-001",
        "profile_projection": None,
        "platform_receipt": platform_receipt,
        "task_receipt": task_receipt,
        "actual_process_start_count": 0,
        "automatic_retry_count": 0,
        "fallback_attempt_count": 0,
        "durable_write_count": 0,
        "synthetic_only": True,
        "live_ready": False,
    }


class TrustedNativeAppServerAdapter:
    """Single-use inert adapter accepted only by the fake-transport R0 path."""

    synthetic_only = True
    adapter_identity = APP_SERVER_ADAPTER_ID
    public_launcher_identity = PUBLIC_LAUNCHER_ID

    def __init__(
        self,
        *,
        execution_binding: Mapping[str, object],
        registry_entry: Mapping[str, object],
        private_context: SyntheticPrivateContext,
        instruction_packet: str,
        transport: InertAppServerTransport,
        clock: object = None,
    ) -> None:
        self._execution_binding = dict(execution_binding)
        self._registry_entry = dict(registry_entry)
        self._private_context = private_context
        self._instruction_packet = instruction_packet
        self._transport = transport
        self._clock = clock
        self._used = False
        self.last_result: dict[str, object] | None = None

    def create_once(self, request: Mapping[str, object]) -> object:
        if self._used:
            raise AppServerAdapterError("app_server_adapter_already_used")
        boundary_errors = validate_accepted_input_boundary(
            task_request=request,
            execution_binding=self._execution_binding,
            registry_entry=self._registry_entry,
            instruction_packet=self._instruction_packet,
        )
        if boundary_errors:
            self.last_result = _failure_result(
                "preflight",
                "profile_priority_01_request_or_packet_invalid",
                "not_consumed",
                process_start_calls=0,
            )
            raise AppServerAdapterError(
                str(self.last_result["lifecycle_case"]),
                profile_projection=str(self.last_result["profile_projection"]),
            )
        self._used = True
        self.last_result = run_inert_app_server_once(
            task_request=request,
            execution_binding=self._execution_binding,
            registry_entry=self._registry_entry,
            private_context=self._private_context,
            instruction_packet=self._instruction_packet,
            transport=self._transport,
            clock=self._clock,
        )
        if self.last_result["status"] != "synthetic_app_server_receipt_accepted_non_live":
            raise AppServerAdapterError(
                str(self.last_result["lifecycle_case"]),
                profile_projection=(
                    str(self.last_result["profile_projection"])
                    if self.last_result["profile_projection"] is not None
                    else None
                ),
            )
        return self.last_result["task_receipt"]


def start_pinned_app_server_once(
    validated_binding: object,
    private_installation: object,
) -> None:
    """Fail closed until a separately authorized R2 process transport exists."""

    del validated_binding, private_installation
    raise AppServerAdapterError("real_process_start_not_authorized")
