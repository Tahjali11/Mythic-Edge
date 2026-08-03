#!/usr/bin/env python3
"""Project one contracted R0 offline observation without persistent effects.

The live CLI is intentionally narrow: it accepts one predeclared observation
identity and emits either that identity's exact receipt or one symbolic failure
status. Authority consumption and GitHub publication remain executor-owned.
"""

from __future__ import annotations

import ctypes
import hashlib
import importlib.util
import json
import os
import stat
import sys
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Callable, Mapping, Sequence, TextIO

SEQUENCE_CONTRACT_RELATIVE_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_offline_observation_sequence.md"
)
SEQUENCE_CONTRACT_SHA256 = (
    "df6cce588e6d64ba5ba24b5d8d7f267c9c9a7e769c9a254527a9e7fd3d68e2b8"
)
RECEIPT_ORDER_CONTRACT_RELATIVE_PATH = Path(
    "docs/contracts/"
    "role_pool_trusted_owner_r0_offline_observation_receipt_order_"
    "reconciliation_successor.md"
)
RECEIPT_ORDER_CONTRACT_SHA256 = (
    "8cbd996f729d77eff3bd954fd054aa2012926e1d9c06f7e43e7e7d0a08a939a7"
)
RECEIPT_ORDER_REVIEW_RELATIVE_PATH = Path(
    "docs/contract_test_reports/"
    "role_pool_trusted_owner_r0_offline_observation_receipt_order_"
    "reconciliation_successor.md"
)
RECEIPT_ORDER_REVIEW_SHA256 = (
    "9a54ffd8de7ace8092316de7637f76db2de2d8ede6e0163b8c33d22e68930ff2"
)
DIRECT_INTERPRETER_CONTRACT_RELATIVE_PATH = Path(
    "docs/contracts/"
    "role_pool_trusted_owner_r0_offline_observation_direct_interpreter_"
    "successor.md"
)
DIRECT_INTERPRETER_CONTRACT_SHA256 = (
    "17d0d2f5fe965643888ea70c71a278afdb7797033c311252bce1dde56486ea84"
)
DIRECT_INTERPRETER_REVIEWED_CONTRACT_SHA256 = (
    "17d0d2f5fe965643888ea70c71a278afdb7797033c311252bce1dde56486ea84"
)
PROPORTIONATE_CONTRACT_RELATIVE_PATH = Path(
    "docs/contracts/"
    "role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md"
)
PROPORTIONATE_CONTRACT_SHA256 = (
    "129ceb8f2bb21f4773e8258ad04238784d986c14168179e1d009b30c584588ae"
)
PROPORTIONATE_REVIEW_RELATIVE_PATH = Path(
    "docs/contract_test_reports/"
    "role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md"
)
PROPORTIONATE_REVIEW_SHA256 = (
    "465af80ae12e10f7e7417dcf93a902807d9155041e8b1f781da8babca46b7b32"
)
R0_CHECKER_RELATIVE_PATH = Path("tools/check_role_pool_r0_bootstrap.py")
R0_CHECKER_SHA256 = (
    "34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914"
)

REPOSITORY_ID = 1235264383
ISSUE_NUMBER = 776
PROTECTED_ISSUE_NUMBER = 769
CURRENT_RUNG = "R0"
HISTORICAL_FAILED_CONSUMPTION_ARTIFACT_SHA256 = (
    "00908b1692bd09f980cb2ef9e97b697667564f8388cd9070da59421e97348d7c"
)
HISTORICAL_SEQUENCE_IDS = (
    "r0.offline.sequence.1d11e7476ab400a39d222d0feab38eba",
    "r0.offline.sequence.2.45c8f6d057ddc04aa60650b0c09090f0",
    "r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa",
)
HISTORICAL_OBSERVATION_IDS = (
    "r0.offline.observation.1.094221964ddd0af9c3b2034a35347971",
    "r0.offline.observation.2.45b674178dd44c9b6723f42e75f3b04f",
    "r0.offline.observation.1.v2.f6b5effa4a357e784cbbf1dd39efff2c",
    "r0.offline.observation.2.v2.7b491e38edb350b7a9b6864c1d60cb39",
    "r0.offline.observation.1.v3.b40fa2727a0f8006ceb93945cf1b1461",
    "r0.offline.observation.2.v3.7269e523cea1b426a7ecedb3ef6e7fb1",
)
HISTORICAL_CONSUMPTION_SHA256 = (
    "3c3537c680b9d413b10d32f9444d5667a1348f54afe39ade24912154ce2949c3"
)
DIRECT_INTERPRETER_BINDING_SHA256 = (
    "2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333"
)
DIRECT_INTERPRETER_BINDING_ARTIFACT_SHA256 = (
    "235e21a04acb454adb5471f2136b53547c35a279a63b8e09d8c6a10926d3bb9b"
)
SEQUENCE_ID = "r0.offline.sequence.4.ff3d34eee94243a6a031d3334430bfca"
OBSERVATION_IDS = (
    "r0.offline.observation.1.v4.209f443bcbf144d99bbb5cecf8aa8bf3",
    "r0.offline.observation.2.v4.b0dacd7eeb56422f9107c0775d972be4",
)
PROFILE_CONTRACT_SHA256 = (
    "944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f"
)
RELEASE_STATE_ARTIFACT_SHA256 = (
    "723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9"
)
RELEASE_RECORD_SHA256 = (
    "78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7"
)
SOURCE_TREE_SHA256 = (
    "18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f"
)
REGISTRY_ARTIFACT_SHA256 = (
    "4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb"
)
REGISTRY_SHA256 = (
    "93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7"
)
VALIDATOR_BUNDLE_SHA256 = (
    "ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5"
)
R0_CHECKER_TEST_SHA256 = (
    "976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34"
)
RELEASE_VALIDATOR_SHA256 = (
    "af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d"
)
AUTHORITY_INDEX_SHA256 = (
    "2a4b4629c2faaa77f1c8f65d0f8f2c6c42aef8f34fc57ab4164fbb84d5579de0"
)
OBSERVATION_PROFILE_SHA256 = (
    "8fee508faddd873413cf655d8435e21121d9f713ede471ceaf768cfa65dd0c81"
)
EXPECTED_RECEIPT_SHA256S = (
    (
        "1ee18ff073a8d998e6370fb6762b80aedaf9c656c4b4d15c1c54d216cb2b150c",
        "54c362c1831668c8ab8130aa68541106f89536a754b212035c3a81610ef53d63",
        "cc93c09eedcdeeb802ddafdb84abbf34be9ba9f96eccc5261e621d47fab7a6ed",
        "0c416f9a97151f14f5210feeebf13188b7d0bdb03035237e5bebebf7238deb61",
        "8f1cadbb03d0c4b630e48e2b52e1bc97cd4f0d31ace194e34d4b881580b98e40",
        "61a25cea3056cd0a4cfe8efd9072ad4a1a0dce0f6eeccb28033571da89a76cef",
    ),
    (
        "1c6182fb3bfb6ec8cb069d141af4110a03bcce45fc928707451cd8281f6095a3",
        "ff39330edf11c3142641f2d6031d7dc540a4b65b6137fa3539a75a6ae4359ea3",
        "4294c180d32116c06c0036fa70a4826f5e15a4ae91d7761151de30605b4e8364",
        "a641437ccceeeb0919a615981e02cb726cbc19137b5441e26656416906043c2b",
        "201e5cf48a49c4d286f7d3e6a325e5137280bec346bf18946a6e7d56fbc817b2",
        "5c3e971c57aa34028a3ff9abdc480ab57eb5d9a456f0e0238f1db17a79f57052",
    ),
)
EXPECTED_RECEIPT_ARTIFACT_SHA256S = (
    (
        "2922a69cc5972f5b6a9901202f8749c0d3df519b9698a260f5c62e708d5a892b",
        "1e97d25b92c9ce92d594a2f33dfce5519383764d58b86f3a0a8e97d552932463",
        "f0ff509832a167eb4a42c51630b9683de5c4ba35fd734ad2e3aefc02444ee2ca",
        "f553e2d0ac110d988490f20122e5a6e1f92c8792bcb069d6e8d6119b9db1a9ea",
        "7fc75ccca246364c3b74d35bade5f5ec0dd893bbb532f8caf877ebb6c2500d1e",
        "4ba512c8b2057223d47cec9a81604074f8598d737fc3d984ba7b0bf5cdbf0a67",
    ),
    (
        "90705e6fac3ba7aefeeba3938647d23117a7a2ce193f2a1154524e32f58ec25b",
        "dd1bc38ed2140fefc874d58db854f99382793f72fec65f5378a820f4e334bc2f",
        "564e7a42ddaf4ba04c96ce1b93562bb6ea943a474d528a0128eae3a1ba555ef6",
        "e2351f414d40ba0022764048a850e2fa868718e0054a0fe1edc5422c3e1c193c",
        "0ca85017b89062073b4764a23bc43164088d9eea19248c614772141672e83652",
        "52795d6fa8e94bfa6700c89aa0393d058bd7ca5558e254ed6a76c9816817d638",
    ),
)
EXPECTED_RECEIPT_PREIMAGE_LENGTHS = (
    (2477, 2478, 2477, 2485, 2486, 2485),
    (2535, 2536, 2535, 2543, 2544, 2543),
)
EXPECTED_RECEIPT_LENGTHS = (
    (2561, 2562, 2561, 2569, 2570, 2569),
    (2619, 2620, 2619, 2627, 2628, 2627),
)

AUTHORITY_FIELDS = (
    "repository_mutation_authorized",
    "implementation_authorized",
    "publication_authorized",
    "merge_authorized",
    "deployment_authorized",
    "installation_authorized",
    "package_operations_authorized",
    "network_authorized",
    "secrets_authorized",
    "external_isolation_authorized",
    "canary_authorized",
    "stage4_authorized",
    "stage_advancement_authorized",
    "dispatch_authorized",
    "live_ready",
    "trusted_owner_native_profile_ready",
)

VALIDATION_PAYLOAD_FIELDS = (
    "schema_version",
    "operation",
    "repository_id",
    "repository_name",
    "issue_url",
    "base_commit",
    "profile_contract_sha256",
    "app_server_contract_sha256",
    "r0_contract_sha256",
    "contract_binding_status",
    "stage3_manifest_file_count",
    "stage3_manifest_byte_count",
    "stage3_manifest_sha256",
    "manifest_status",
    "source_tree_node_count",
    "source_tree_file_count",
    "source_tree_manifest_byte_count",
    "source_tree_sha256",
    "installed_tree_node_count",
    "installed_tree_file_count",
    "installed_tree_manifest_byte_count",
    "installed_tree_sha256",
    "source_install_status",
    "registry_status",
    "registry_sha256",
    "release_state_status",
    "release_state_sha256",
    "checker_sha256",
    "checker_test_sha256",
    "validator_bundle_sha256",
    "validator_bundle_status",
    "offline_validation_status",
    "terminal_status",
    "eligible_for_independent_review",
    "effect_counts",
    "authority_flags",
    "evidence_sha256",
)

VALIDATION_EFFECT_FIELDS = (
    "app_server_process_start_count",
    "task_creation_count",
    "network_operation_count",
    "repository_command_count",
    "persistent_mutation_count",
)

RECEIPT_FIELDS = (
    "schema_version",
    "sequence_id",
    "observation_id",
    "sequence_position",
    "predecessor_observation_id",
    "repository_id",
    "issue_number",
    "current_rung",
    "profile_contract_sha256",
    "release_state_artifact_sha256",
    "release_record_sha256",
    "source_tree_sha256",
    "installed_tree_sha256",
    "registry_artifact_sha256",
    "registry_sha256",
    "validator_bundle_sha256",
    "observation_profile_sha256",
    "host_os_name",
    "host_sys_platform",
    "validation_status",
    "release_state_status",
    "bootstrap_checker_terminal_status",
    "derived_current_rung",
    "process_topology",
    "top_level_process_count",
    "descendant_process_count",
    "process_relationships_known",
    "process_terminal_states_known",
    "surviving_process_count",
    "top_level_identity_exact",
    "process_launch_attempt_count",
    "network_operation_count",
    "repository_write_count",
    "installed_write_count",
    "external_effect_count",
    "retry_count",
    "unknown_outcome_count",
    "cleanup_status",
    "accepted_for_independent_review",
    "authority_flags",
    "receipt_sha256",
)

CONSUMPTION_FIELDS = (
    "schema_version",
    "sequence_id",
    "observation_id",
    "sequence_position",
    "predecessor_consumption_sha256",
    "repository_id",
    "issue_number",
    "owner_decision_ref",
    "owner_decision_sha256",
    "owner_decision_created_at_utc",
    "owner_decision_expires_at_utc",
    "sequence_contract_sha256",
    "sequence_contract_review_ref",
    "sequence_contract_review_sha256",
    "harness_sha256",
    "harness_test_sha256",
    "implementation_review_ref",
    "implementation_review_sha256",
    "profile_contract_sha256",
    "release_state_artifact_sha256",
    "release_record_sha256",
    "source_tree_sha256",
    "installed_tree_sha256",
    "registry_artifact_sha256",
    "registry_sha256",
    "validator_bundle_sha256",
    "observation_profile_sha256",
    "expected_receipt_sha256s",
    "decision",
    "transition",
    "attempt_limit",
    "retry_authorized",
    "reuse_authorized",
    "launch_authorized_after_exact_readback",
    "status",
    "consumption_sha256",
)

CONSUMPTION_CALL_RESULTS = ("reported_success", "known_failure", "unknown")
CONSUMPTION_COMMENT_STATES = (
    "exact_one",
    "none",
    "unique_invalid",
    "multiple_or_conflicting",
    "unreadable",
)
CONSUMPTION_TERMINALS = (
    "consumed_exact_nonreusable",
    "consumption_failed_nonreusable",
    "consumption_collision_nonreusable",
    "consumption_readback_failed_nonreusable",
    "consumption_ambiguous_nonreusable",
)

LIFECYCLE_FIELDS = (
    "public_binding_exact",
    "authority_exact",
    "sequence_exact",
    "consumption_status",
    "host_exact",
    "launch_status",
    "safety_boundary_exact",
    "timeout_status",
    "result_status",
    "sealing_exact",
    "publication_status",
    "readback_exact",
)

TERMINAL_STATUSES = (
    "observation_binding_rejected",
    "observation_authority_rejected",
    "observation_sequence_rejected",
    "consumption_collision_nonreusable",
    "consumption_failed_nonreusable",
    "consumption_ambiguous_nonreusable",
    "consumption_readback_failed_nonreusable",
    "observation_host_rejected",
    "observation_launch_unknown",
    "observation_safety_boundary_failed",
    "observation_timeout_unknown",
    "observation_result_unknown",
    "observation_validation_failed",
    "observation_receipt_sealing_failed",
    "observation_receipt_collision",
    "observation_publication_unknown",
    "observation_receipt_readback_failed",
    "accepted_exact_r0_offline_observation",
)

MAX_STDOUT_BYTES = 4096
MAX_FAILURE_STDERR_BYTES = 128

DIRECT_INTERPRETER_BINDING_FIELDS = (
    "schema_version",
    "repository_id",
    "issue_number",
    "host_os_name",
    "host_sys_platform",
    "runtime_implementation",
    "executable_basename",
    "file_version",
    "product_version",
    "byte_length",
    "file_sha256",
    "stable_identity_schema",
    "stable_identity_sha256",
    "ordinary_file",
    "reparse_point",
    "private_path_source",
    "private_path_publication_authorized",
    "binding_sha256",
)

DIRECT_INTERPRETER_PREFLIGHT_STATES = (
    "not_run",
    "passed",
    "descendant",
    "unknown",
)

DIRECT_INTERPRETER_PREFLIGHT_OUTCOMES = (
    "direct_interpreter_hypothesis_rejected",
    "observation_binding_rejected",
    "direct_interpreter_preflight_required",
    "direct_interpreter_preflight_descendant_observed",
    "direct_interpreter_preflight_unknown",
    "direct_interpreter_preflight_passed",
)


class DuplicateJsonKeyError(ValueError):
    """Reject duplicate keys before a packet can be interpreted."""


class ObservationFailure(RuntimeError):
    """A public-safe, known terminal observation failure."""

    def __init__(self, status: str) -> None:
        if status not in TERMINAL_STATUSES:
            raise ValueError("terminal_status_invalid")
        super().__init__(status)
        self.status = status


class ObservationUnknown(ObservationFailure):
    """An outcome that cannot safely be resolved in this process."""


class SafetyBoundaryViolation(ObservationFailure):
    """A forbidden process, network, write, or target-expansion attempt."""

    def __init__(self) -> None:
        super().__init__("observation_safety_boundary_failed")


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError
        result[key] = value
    return result


def canonical_bytes(document: Mapping[str, object]) -> bytes:
    """Encode ordered canonical JSON used by all contracted packets."""

    return (
        json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def self_digest(document: Mapping[str, object], digest_field: str) -> str:
    preimage = {key: value for key, value in document.items() if key != digest_field}
    return hashlib.sha256(canonical_bytes(preimage)).hexdigest()


def _json_values_are_exact(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        assert isinstance(right, dict)
        return tuple(left) == tuple(right) and all(
            _json_values_are_exact(left[key], right[key]) for key in left
        )
    if isinstance(left, list):
        assert isinstance(right, list)
        return len(left) == len(right) and all(
            _json_values_are_exact(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def _parse_canonical_object(payload: bytes, fields: tuple[str, ...]) -> dict[str, object]:
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n"):
        raise ObservationFailure("observation_validation_failed")
    try:
        text = payload.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        raise ObservationFailure("observation_validation_failed") from exc
    if not isinstance(value, dict) or tuple(value) != fields:
        raise ObservationFailure("observation_validation_failed")
    if canonical_bytes(value) != payload:
        raise ObservationFailure("observation_validation_failed")
    return value


def _authority_flags() -> dict[str, bool]:
    return {field: False for field in AUTHORITY_FIELDS}


DIRECT_INTERPRETER_BINDING: dict[str, object] = {
    "schema_version": "trusted_owner_r0_direct_cpython_binding.v1",
    "repository_id": REPOSITORY_ID,
    "issue_number": 780,
    "host_os_name": "nt",
    "host_sys_platform": "win32",
    "runtime_implementation": "CPython",
    "executable_basename": "python.exe",
    "file_version": "3.13.14",
    "product_version": "3.13.14",
    "byte_length": 105696,
    "file_sha256": (
        "ef8f51028ac5329641985112f8efb1c2d4c47c86b8011ddf7e6fae21e2b4e5a1"
    ),
    "stable_identity_schema": "trusted_owner_direct_cpython_file_identity.v1",
    "stable_identity_sha256": (
        "570754cbc03fb52f4e846c3611e48e18334f08e621babfa2e8eb76f4a0e5c953"
    ),
    "ordinary_file": True,
    "reparse_point": False,
    "private_path_source": "owner_supplied_local_absolute_path",
    "private_path_publication_authorized": False,
    "binding_sha256": DIRECT_INTERPRETER_BINDING_SHA256,
}


@dataclass(frozen=True)
class DirectInterpreterMetadata:
    runtime_implementation: str
    executable_basename: str
    file_version: str
    product_version: str
    byte_length: int
    file_sha256: str
    stable_identity_sha256: str
    ordinary_file: bool
    reparse_point: bool


def parse_direct_interpreter_binding(payload: bytes) -> dict[str, object]:
    try:
        binding = _parse_canonical_object(
            payload,
            DIRECT_INTERPRETER_BINDING_FIELDS,
        )
    except ObservationFailure as exc:
        raise ObservationFailure("observation_binding_rejected") from exc
    if (
        not _json_values_are_exact(binding, DIRECT_INTERPRETER_BINDING)
        or binding["binding_sha256"]
        != self_digest(binding, "binding_sha256")
    ):
        raise ObservationFailure("observation_binding_rejected")
    return binding


def validate_direct_interpreter_metadata(
    metadata: DirectInterpreterMetadata,
) -> None:
    expected = DirectInterpreterMetadata(
        runtime_implementation=str(
            DIRECT_INTERPRETER_BINDING["runtime_implementation"]
        ),
        executable_basename=str(
            DIRECT_INTERPRETER_BINDING["executable_basename"]
        ),
        file_version=str(DIRECT_INTERPRETER_BINDING["file_version"]),
        product_version=str(DIRECT_INTERPRETER_BINDING["product_version"]),
        byte_length=int(DIRECT_INTERPRETER_BINDING["byte_length"]),
        file_sha256=str(DIRECT_INTERPRETER_BINDING["file_sha256"]),
        stable_identity_sha256=str(
            DIRECT_INTERPRETER_BINDING["stable_identity_sha256"]
        ),
        ordinary_file=True,
        reparse_point=False,
    )
    if metadata != expected:
        raise ObservationFailure("observation_binding_rejected")


def select_direct_interpreter_preflight_outcome(
    historical_direct_use_proven: bool,
    public_bindings_exact: bool,
    private_binding_exact: bool,
    preflight_state: str,
) -> str:
    values = (
        historical_direct_use_proven,
        public_bindings_exact,
        private_binding_exact,
    )
    if any(type(value) is not bool for value in values):
        raise ValueError("direct_interpreter_preflight_boolean_invalid")
    if preflight_state not in DIRECT_INTERPRETER_PREFLIGHT_STATES:
        raise ValueError("direct_interpreter_preflight_state_invalid")
    if historical_direct_use_proven:
        return "direct_interpreter_hypothesis_rejected"
    if not public_bindings_exact or not private_binding_exact:
        return "observation_binding_rejected"
    outcomes = {
        "not_run": "direct_interpreter_preflight_required",
        "descendant": "direct_interpreter_preflight_descendant_observed",
        "unknown": "direct_interpreter_preflight_unknown",
        "passed": "direct_interpreter_preflight_passed",
    }
    return outcomes[preflight_state]


OBSERVATION_PROFILE: dict[str, object] = {
    "schema_version": "trusted_owner_r0_offline_observation_profile.v3",
    "repository_id": REPOSITORY_ID,
    "issue_number": ISSUE_NUMBER,
    "current_rung": CURRENT_RUNG,
    "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
    "release_state_artifact_sha256": RELEASE_STATE_ARTIFACT_SHA256,
    "release_record_sha256": RELEASE_RECORD_SHA256,
    "source_tree_sha256": SOURCE_TREE_SHA256,
    "installed_tree_sha256": SOURCE_TREE_SHA256,
    "registry_artifact_sha256": REGISTRY_ARTIFACT_SHA256,
    "registry_sha256": REGISTRY_SHA256,
    "validator_bundle_sha256": VALIDATOR_BUNDLE_SHA256,
    "r0_checker_sha256": R0_CHECKER_SHA256,
    "r0_checker_test_sha256": R0_CHECKER_TEST_SHA256,
    "release_validator_sha256": RELEASE_VALIDATOR_SHA256,
    "authority_index_sha256": AUTHORITY_INDEX_SHA256,
    "implementation_paths": [
        "tools/check_role_pool_r0_offline_observation.py",
        "tests/test_check_role_pool_r0_offline_observation.py",
    ],
    "fixed_command": [
        "py",
        "-3.13",
        "-B",
        "tools/check_role_pool_r0_offline_observation.py",
        "<observation_id>",
    ],
    "host_os_name": "nt",
    "host_sys_platform": "win32",
    "top_level_operation_limit": 1,
    "descendant_process_limit": 1,
    "surviving_process_limit": 0,
    "process_relationships_known_required": True,
    "process_terminal_states_known_required": True,
    "top_level_identity_role": "diagnostic_nonblocking",
    "network_observation_scope": "executor_owned_observed_only",
    "network_operation_limit": 0,
    "external_effect_limit": 0,
    "observation_count": 2,
    "timeout_seconds": 120,
    "retry_limit": 0,
}


RECEIPT_VARIANTS = (
    (0, None),
    (0, False),
    (0, True),
    (1, None),
    (1, False),
    (1, True),
)


def _build_receipt(
    position: int,
    descendant_process_count: int,
    top_level_identity_exact: bool | None,
) -> dict[str, object]:
    if position not in (1, 2):
        raise ObservationFailure("observation_sequence_rejected")
    if (descendant_process_count, top_level_identity_exact) not in RECEIPT_VARIANTS:
        raise ObservationFailure("observation_validation_failed")
    receipt: dict[str, object] = {
        "schema_version": "trusted_owner_r0_offline_observation_receipt.v2",
        "sequence_id": SEQUENCE_ID,
        "observation_id": OBSERVATION_IDS[position - 1],
        "sequence_position": position,
        "predecessor_observation_id": None if position == 1 else OBSERVATION_IDS[0],
        "repository_id": REPOSITORY_ID,
        "issue_number": ISSUE_NUMBER,
        "current_rung": CURRENT_RUNG,
        "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
        "release_state_artifact_sha256": RELEASE_STATE_ARTIFACT_SHA256,
        "release_record_sha256": RELEASE_RECORD_SHA256,
        "source_tree_sha256": SOURCE_TREE_SHA256,
        "installed_tree_sha256": SOURCE_TREE_SHA256,
        "registry_artifact_sha256": REGISTRY_ARTIFACT_SHA256,
        "registry_sha256": REGISTRY_SHA256,
        "validator_bundle_sha256": VALIDATOR_BUNDLE_SHA256,
        "observation_profile_sha256": OBSERVATION_PROFILE_SHA256,
        "host_os_name": "nt",
        "host_sys_platform": "win32",
        "validation_status": "accepted_exact_r0_offline_observation",
        "release_state_status": "present_valid_chain",
        "bootstrap_checker_terminal_status": (
            "blocked_release_state_conflict_expected"
        ),
        "derived_current_rung": "R0",
        "process_topology": (
            "single_top_level_zero_descendants_terminal"
            if descendant_process_count == 0
            else "single_top_level_one_transient_descendant_terminal"
        ),
        "top_level_process_count": 1,
        "descendant_process_count": descendant_process_count,
        "process_relationships_known": True,
        "process_terminal_states_known": True,
        "surviving_process_count": 0,
        "top_level_identity_exact": top_level_identity_exact,
        "process_launch_attempt_count": 0,
        "network_operation_count": 0,
        "repository_write_count": 0,
        "installed_write_count": 0,
        "external_effect_count": 0,
        "retry_count": 0,
        "unknown_outcome_count": 0,
        "cleanup_status": "complete_no_survivors_no_residue",
        "accepted_for_independent_review": True,
        "authority_flags": _authority_flags(),
        "receipt_sha256": "",
    }
    receipt["receipt_sha256"] = self_digest(receipt, "receipt_sha256")
    return receipt


EXPECTED_RECEIPTS = tuple(
    tuple(
        _build_receipt(position, descendant_count, identity_exact)
        for descendant_count, identity_exact in RECEIPT_VARIANTS
    )
    for position in (1, 2)
)


def parse_receipt(payload: bytes) -> dict[str, object]:
    if len(payload) > MAX_STDOUT_BYTES:
        raise ObservationFailure("observation_result_unknown")
    receipt = _parse_canonical_object(payload, RECEIPT_FIELDS)
    position = receipt.get("sequence_position")
    if type(position) is not int or position not in (1, 2):
        raise ObservationFailure("observation_validation_failed")
    allowed = EXPECTED_RECEIPTS[position - 1]
    if not any(_json_values_are_exact(receipt, expected) for expected in allowed):
        raise ObservationFailure("observation_validation_failed")
    if receipt["receipt_sha256"] != self_digest(receipt, "receipt_sha256"):
        raise ObservationFailure("observation_validation_failed")
    return receipt


def select_receipt_pair_outcome(
    canonical_pair_exact: bool,
    position_order_exact: bool,
    identity_order_exact: bool,
    predecessor_link_exact: bool,
    expected_digest_tuple_exact: bool,
    digest_tuple_lexically_ascending: bool,
) -> str:
    values = (
        canonical_pair_exact,
        position_order_exact,
        identity_order_exact,
        predecessor_link_exact,
        expected_digest_tuple_exact,
        digest_tuple_lexically_ascending,
    )
    if any(type(value) is not bool for value in values):
        raise ObservationFailure("observation_sequence_rejected")
    if all(values[:5]):
        return "accepted_exact_chronological_receipt_pair"
    return "observation_sequence_rejected"


def validate_receipt_pair(payloads: Sequence[bytes]) -> tuple[dict[str, object], ...]:
    if len(payloads) != 2:
        raise ObservationFailure("observation_sequence_rejected")
    try:
        receipts = tuple(parse_receipt(payload) for payload in payloads)
    except ObservationFailure as exc:
        raise ObservationFailure("observation_sequence_rejected") from exc
    position_order_exact = tuple(
        receipt["sequence_position"] for receipt in receipts
    ) == (1, 2)
    identity_order_exact = (
        tuple(receipt["sequence_id"] for receipt in receipts)
        == (SEQUENCE_ID, SEQUENCE_ID)
        and tuple(receipt["observation_id"] for receipt in receipts)
        == OBSERVATION_IDS
    )
    predecessor_link_exact = (
        receipts[0]["predecessor_observation_id"] is None
        and receipts[1]["predecessor_observation_id"]
        == receipts[0]["observation_id"]
    )
    digests = tuple(str(receipt["receipt_sha256"]) for receipt in receipts)
    outcome = select_receipt_pair_outcome(
        True,
        position_order_exact,
        identity_order_exact,
        predecessor_link_exact,
        all(
            digest in EXPECTED_RECEIPT_SHA256S[index]
            for index, digest in enumerate(digests)
        ),
        False,
    )
    if outcome != "accepted_exact_chronological_receipt_pair":
        raise ObservationFailure("observation_sequence_rejected")
    return receipts


SYNTHETIC_CONSUMPTION_KAT: dict[str, object] = {
    "schema_version": "trusted_owner_r0_offline_observation_consumption.v2",
    "sequence_id": SEQUENCE_ID,
    "observation_id": OBSERVATION_IDS[0],
    "sequence_position": 1,
    "predecessor_consumption_sha256": None,
    "repository_id": REPOSITORY_ID,
    "issue_number": ISSUE_NUMBER,
    "owner_decision_ref": (
        "https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-kat-owner"
    ),
    "owner_decision_sha256": "1" * 64,
    "owner_decision_created_at_utc": "2026-08-01T00:00:00Z",
    "owner_decision_expires_at_utc": "2026-08-01T12:00:00Z",
    "sequence_contract_sha256": "2" * 64,
    "sequence_contract_review_ref": (
        "https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-kat-contract-review"
    ),
    "sequence_contract_review_sha256": "3" * 64,
    "harness_sha256": "4" * 64,
    "harness_test_sha256": "5" * 64,
    "implementation_review_ref": (
        "https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-kat-implementation-review"
    ),
    "implementation_review_sha256": "6" * 64,
    "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
    "release_state_artifact_sha256": RELEASE_STATE_ARTIFACT_SHA256,
    "release_record_sha256": RELEASE_RECORD_SHA256,
    "source_tree_sha256": SOURCE_TREE_SHA256,
    "installed_tree_sha256": SOURCE_TREE_SHA256,
    "registry_artifact_sha256": REGISTRY_ARTIFACT_SHA256,
    "registry_sha256": REGISTRY_SHA256,
    "validator_bundle_sha256": VALIDATOR_BUNDLE_SHA256,
    "observation_profile_sha256": OBSERVATION_PROFILE_SHA256,
    "expected_receipt_sha256s": list(EXPECTED_RECEIPT_SHA256S[0]),
    "decision": "consume_one_r0_offline_observation_identity",
    "transition": "approved_unconsumed_to_consumed_exact_nonreusable",
    "attempt_limit": 1,
    "retry_authorized": False,
    "reuse_authorized": False,
    "launch_authorized_after_exact_readback": True,
    "status": "consumed_exact_nonreusable",
    "consumption_sha256": "",
}
SYNTHETIC_CONSUMPTION_KAT["consumption_sha256"] = self_digest(
    SYNTHETIC_CONSUMPTION_KAT,
    "consumption_sha256",
)


def parse_consumption(
    payload: bytes,
    *,
    expected: Mapping[str, object] | None = None,
) -> dict[str, object]:
    consumption = _parse_canonical_object(payload, CONSUMPTION_FIELDS)
    digest = consumption.get("consumption_sha256")
    if not isinstance(digest, str) or digest != self_digest(
        consumption,
        "consumption_sha256",
    ):
        raise ObservationFailure("observation_validation_failed")
    fixed = {
        "schema_version": "trusted_owner_r0_offline_observation_consumption.v2",
        "sequence_id": SEQUENCE_ID,
        "repository_id": REPOSITORY_ID,
        "issue_number": ISSUE_NUMBER,
        "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
        "release_state_artifact_sha256": RELEASE_STATE_ARTIFACT_SHA256,
        "release_record_sha256": RELEASE_RECORD_SHA256,
        "source_tree_sha256": SOURCE_TREE_SHA256,
        "installed_tree_sha256": SOURCE_TREE_SHA256,
        "registry_artifact_sha256": REGISTRY_ARTIFACT_SHA256,
        "registry_sha256": REGISTRY_SHA256,
        "validator_bundle_sha256": VALIDATOR_BUNDLE_SHA256,
        "observation_profile_sha256": OBSERVATION_PROFILE_SHA256,
        "decision": "consume_one_r0_offline_observation_identity",
        "transition": "approved_unconsumed_to_consumed_exact_nonreusable",
        "attempt_limit": 1,
        "retry_authorized": False,
        "reuse_authorized": False,
        "launch_authorized_after_exact_readback": True,
        "status": "consumed_exact_nonreusable",
    }
    for field, value in fixed.items():
        if not _json_values_are_exact(consumption[field], value):
            raise ObservationFailure("observation_validation_failed")
    position = consumption["sequence_position"]
    if type(position) is not int or position not in (1, 2):
        raise ObservationFailure("observation_sequence_rejected")
    if consumption["observation_id"] != OBSERVATION_IDS[position - 1]:
        raise ObservationFailure("observation_sequence_rejected")
    if not _json_values_are_exact(
        consumption["expected_receipt_sha256s"],
        list(EXPECTED_RECEIPT_SHA256S[position - 1]),
    ):
        raise ObservationFailure("observation_sequence_rejected")
    predecessor = consumption["predecessor_consumption_sha256"]
    if position == 1 and predecessor is not None:
        raise ObservationFailure("observation_sequence_rejected")
    if position == 2 and not _is_sha256(predecessor):
        raise ObservationFailure("observation_sequence_rejected")
    dynamic_digest_fields = (
        "owner_decision_sha256",
        "sequence_contract_sha256",
        "sequence_contract_review_sha256",
        "harness_sha256",
        "harness_test_sha256",
        "implementation_review_sha256",
    )
    if any(not _is_sha256(consumption[field]) for field in dynamic_digest_fields):
        raise ObservationFailure("observation_validation_failed")
    dynamic_string_fields = (
        "owner_decision_ref",
        "owner_decision_created_at_utc",
        "owner_decision_expires_at_utc",
        "sequence_contract_review_ref",
        "implementation_review_ref",
    )
    if any(
        not isinstance(consumption[field], str) or not consumption[field]
        for field in dynamic_string_fields
    ):
        raise ObservationFailure("observation_validation_failed")
    if expected is not None and not _json_values_are_exact(consumption, dict(expected)):
        raise ObservationFailure("observation_binding_rejected")
    return consumption


def select_consumption_outcome(call_result: str, comment_state: str) -> str:
    if call_result not in CONSUMPTION_CALL_RESULTS:
        raise ValueError("call_result_invalid")
    if comment_state not in CONSUMPTION_COMMENT_STATES:
        raise ValueError("comment_state_invalid")
    if comment_state == "exact_one" and call_result in {"reported_success", "unknown"}:
        return "consumed_exact_nonreusable"
    if comment_state == "none" and call_result == "known_failure":
        return "consumption_failed_nonreusable"
    if (
        comment_state == "multiple_or_conflicting"
        or (comment_state == "exact_one" and call_result == "known_failure")
        or (comment_state == "none" and call_result == "reported_success")
    ):
        return "consumption_collision_nonreusable"
    if comment_state == "unique_invalid" or (
        comment_state == "unreadable" and call_result == "reported_success"
    ):
        return "consumption_readback_failed_nonreusable"
    return "consumption_ambiguous_nonreusable"


def reconcile_consumption(
    *,
    exact_receipt: bool,
    exact_consumption: bool,
    collision: bool,
    prior_post_entry: bool,
    state_available: bool,
) -> str:
    if exact_receipt:
        return "completed_no_relaunch"
    if exact_consumption:
        return "consumed_without_accepted_receipt_nonreusable"
    if collision:
        return "consumption_collision_nonreusable"
    if prior_post_entry and state_available:
        return "consumption_absent_after_attempt_nonreusable"
    return "consumption_ambiguous_nonreusable"


def validate_sequence_preflight(
    observation_id: str,
    *,
    consumption: Mapping[str, object],
    predecessor_consumption_sha256: str | None = None,
    predecessor_receipt: bytes | None = None,
) -> None:
    if observation_id not in OBSERVATION_IDS:
        raise ObservationFailure("observation_sequence_rejected")
    position = OBSERVATION_IDS.index(observation_id) + 1
    if consumption.get("observation_id") != observation_id:
        raise ObservationFailure("observation_sequence_rejected")
    if consumption.get("status") != "consumed_exact_nonreusable":
        raise ObservationFailure("observation_sequence_rejected")
    if position == 1:
        if predecessor_consumption_sha256 is not None or predecessor_receipt is not None:
            raise ObservationFailure("observation_sequence_rejected")
        return
    if not _is_sha256(predecessor_consumption_sha256):
        raise ObservationFailure("observation_sequence_rejected")
    if consumption.get("predecessor_consumption_sha256") != predecessor_consumption_sha256:
        raise ObservationFailure("observation_sequence_rejected")
    if predecessor_receipt is None:
        raise ObservationFailure("observation_sequence_rejected")
    parsed_predecessor = parse_receipt(predecessor_receipt)
    if (
        parsed_predecessor["sequence_position"] != 1
        or parsed_predecessor["receipt_sha256"] not in EXPECTED_RECEIPT_SHA256S[0]
    ):
        raise ObservationFailure("observation_sequence_rejected")


def classify_publication(call_result: str, comment_state: str) -> str:
    if call_result not in CONSUMPTION_CALL_RESULTS:
        raise ValueError("call_result_invalid")
    if comment_state not in CONSUMPTION_COMMENT_STATES:
        raise ValueError("comment_state_invalid")
    if comment_state == "exact_one" and call_result in {"reported_success", "unknown"}:
        return "accepted_exact_r0_offline_observation"
    if comment_state == "multiple_or_conflicting":
        return "observation_receipt_collision"
    if call_result == "reported_success":
        return "observation_receipt_readback_failed"
    return "observation_publication_unknown"


def require_publication_issue(issue_number: int) -> None:
    if type(issue_number) is not int or issue_number != ISSUE_NUMBER:
        raise ObservationFailure("observation_binding_rejected")


def select_lifecycle_status(state: Mapping[str, object]) -> str:
    if tuple(state) != LIFECYCLE_FIELDS:
        raise ValueError("lifecycle_fields_invalid")
    if state["public_binding_exact"] is not True:
        return "observation_binding_rejected"
    if state["authority_exact"] is not True:
        return "observation_authority_rejected"
    if state["sequence_exact"] is not True:
        return "observation_sequence_rejected"
    consumption_status = state["consumption_status"]
    if consumption_status == "consumption_collision_nonreusable":
        return consumption_status
    if consumption_status == "consumption_failed_nonreusable":
        return consumption_status
    if consumption_status == "consumption_ambiguous_nonreusable":
        return consumption_status
    if consumption_status == "consumption_readback_failed_nonreusable":
        return consumption_status
    if consumption_status != "consumed_exact_nonreusable":
        raise ValueError("consumption_status_invalid")
    if state["host_exact"] is not True:
        return "observation_host_rejected"
    if state["launch_status"] != "exact":
        return "observation_launch_unknown"
    if state["safety_boundary_exact"] is not True:
        return "observation_safety_boundary_failed"
    if state["timeout_status"] != "within_limit":
        return "observation_timeout_unknown"
    if state["result_status"] == "unknown":
        return "observation_result_unknown"
    if state["result_status"] != "exact":
        return "observation_validation_failed"
    if state["sealing_exact"] is not True:
        return "observation_receipt_sealing_failed"
    publication_status = state["publication_status"]
    if publication_status == "collision":
        return "observation_receipt_collision"
    if publication_status == "unknown":
        return "observation_publication_unknown"
    if publication_status != "exact":
        raise ValueError("publication_status_invalid")
    if state["readback_exact"] is not True:
        return "observation_receipt_readback_failed"
    return "accepted_exact_r0_offline_observation"


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _path_is_within(path: object, roots: Sequence[str]) -> bool:
    if isinstance(path, int):
        return True
    try:
        candidate = os.path.normcase(os.path.abspath(os.fsdecode(path)))
    except (TypeError, ValueError):
        return False
    for root in roots:
        try:
            if os.path.commonpath((candidate, root)) == root:
                return True
        except ValueError:
            continue
    return False


def _paths_are_lexically_equal(left: Path, right: Path) -> bool:
    return os.path.normcase(os.path.abspath(left)) == os.path.normcase(
        os.path.abspath(right)
    )


class _ByHandleFileInformation(ctypes.Structure):
    _fields_ = (
        ("dwFileAttributes", wintypes.DWORD),
        ("ftCreationTime", wintypes.FILETIME),
        ("ftLastAccessTime", wintypes.FILETIME),
        ("ftLastWriteTime", wintypes.FILETIME),
        ("dwVolumeSerialNumber", wintypes.DWORD),
        ("nFileSizeHigh", wintypes.DWORD),
        ("nFileSizeLow", wintypes.DWORD),
        ("nNumberOfLinks", wintypes.DWORD),
        ("nFileIndexHigh", wintypes.DWORD),
        ("nFileIndexLow", wintypes.DWORD),
    )


def _stable_file_identity_sha256(volume_serial: int, file_index: int) -> str:
    preimage = (
        "trusted_owner_direct_cpython_file_identity.v1|"
        f"volume_serial_number={volume_serial:08x}|"
        f"file_index={file_index:016x}"
    ).encode("ascii")
    return hashlib.sha256(preimage).hexdigest()


def _windows_file_versions(path_text: str, version_dll: object) -> tuple[str, str]:
    version_dll.GetFileVersionInfoSizeW.argtypes = (
        wintypes.LPCWSTR,
        ctypes.POINTER(wintypes.DWORD),
    )
    version_dll.GetFileVersionInfoSizeW.restype = wintypes.DWORD
    version_dll.GetFileVersionInfoW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.c_void_p,
    )
    version_dll.GetFileVersionInfoW.restype = wintypes.BOOL
    version_dll.VerQueryValueW.argtypes = (
        ctypes.c_void_p,
        wintypes.LPCWSTR,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(wintypes.UINT),
    )
    version_dll.VerQueryValueW.restype = wintypes.BOOL

    ignored = wintypes.DWORD()
    size = version_dll.GetFileVersionInfoSizeW(path_text, ctypes.byref(ignored))
    if not size:
        raise ObservationFailure("observation_binding_rejected")
    buffer = ctypes.create_string_buffer(size)
    if not version_dll.GetFileVersionInfoW(path_text, 0, size, buffer):
        raise ObservationFailure("observation_binding_rejected")

    translation_pointer = ctypes.c_void_p()
    translation_length = wintypes.UINT()
    if not version_dll.VerQueryValueW(
        buffer,
        r"\VarFileInfo\Translation",
        ctypes.byref(translation_pointer),
        ctypes.byref(translation_length),
    ):
        raise ObservationFailure("observation_binding_rejected")
    if translation_pointer.value is None or translation_length.value < 4:
        raise ObservationFailure("observation_binding_rejected")
    translations = ctypes.cast(
        translation_pointer,
        ctypes.POINTER(ctypes.c_ushort),
    )

    for index in range(0, translation_length.value // 2, 2):
        language = translations[index]
        code_page = translations[index + 1]
        values: list[str] = []
        for field in ("FileVersion", "ProductVersion"):
            value_pointer = ctypes.c_void_p()
            value_length = wintypes.UINT()
            query = f"\\StringFileInfo\\{language:04x}{code_page:04x}\\{field}"
            if not version_dll.VerQueryValueW(
                buffer,
                query,
                ctypes.byref(value_pointer),
                ctypes.byref(value_length),
            ):
                values = []
                break
            if value_pointer.value is None or value_length.value == 0:
                values = []
                break
            value = ctypes.wstring_at(
                value_pointer.value,
                value_length.value,
            ).rstrip("\x00").strip()
            if not value:
                values = []
                break
            values.append(value)
        if len(values) == 2:
            return values[0], values[1]
    raise ObservationFailure("observation_binding_rejected")


def _observe_windows_direct_interpreter(path: Path) -> DirectInterpreterMetadata:
    if os.name != "nt" or sys.platform != "win32":
        raise ObservationFailure("observation_host_rejected")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    version = ctypes.WinDLL("version", use_last_error=True)
    kernel32.CreateFileW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    kernel32.CreateFileW.restype = wintypes.HANDLE
    kernel32.GetFileInformationByHandle.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(_ByHandleFileInformation),
    )
    kernel32.GetFileInformationByHandle.restype = wintypes.BOOL
    kernel32.GetFileType.argtypes = (wintypes.HANDLE,)
    kernel32.GetFileType.restype = wintypes.DWORD
    kernel32.ReadFile.argtypes = (
        wintypes.HANDLE,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.c_void_p,
    )
    kernel32.ReadFile.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL

    generic_read = 0x80000000
    share_all = 0x00000001 | 0x00000002 | 0x00000004
    open_existing = 3
    open_reparse_point = 0x00200000
    invalid_handle = ctypes.c_void_p(-1).value
    handle = kernel32.CreateFileW(
        os.fspath(path),
        generic_read,
        share_all,
        None,
        open_existing,
        open_reparse_point,
        None,
    )
    if handle in (None, invalid_handle):
        raise ObservationFailure("observation_binding_rejected")

    close_failed = False
    metadata: DirectInterpreterMetadata | None = None
    try:
        before = _ByHandleFileInformation()
        if not kernel32.GetFileInformationByHandle(handle, ctypes.byref(before)):
            raise ObservationFailure("observation_binding_rejected")
        file_type = kernel32.GetFileType(handle)
        directory = bool(before.dwFileAttributes & 0x00000010)
        reparse_point = bool(before.dwFileAttributes & 0x00000400)
        ordinary_file = file_type == 0x0001 and not directory and not reparse_point
        if not ordinary_file:
            raise ObservationFailure("observation_binding_rejected")

        digest = hashlib.sha256()
        buffer = ctypes.create_string_buffer(65536)
        while True:
            bytes_read = wintypes.DWORD()
            if not kernel32.ReadFile(
                handle,
                buffer,
                len(buffer),
                ctypes.byref(bytes_read),
                None,
            ):
                raise ObservationFailure("observation_binding_rejected")
            if bytes_read.value == 0:
                break
            digest.update(buffer.raw[: bytes_read.value])

        after = _ByHandleFileInformation()
        if not kernel32.GetFileInformationByHandle(handle, ctypes.byref(after)):
            raise ObservationFailure("observation_binding_rejected")
        before_identity = (
            before.dwVolumeSerialNumber,
            before.nFileIndexHigh,
            before.nFileIndexLow,
            before.nFileSizeHigh,
            before.nFileSizeLow,
            before.dwFileAttributes,
        )
        after_identity = (
            after.dwVolumeSerialNumber,
            after.nFileIndexHigh,
            after.nFileIndexLow,
            after.nFileSizeHigh,
            after.nFileSizeLow,
            after.dwFileAttributes,
        )
        if before_identity != after_identity:
            raise ObservationFailure("observation_binding_rejected")
        file_index = (before.nFileIndexHigh << 32) | before.nFileIndexLow
        byte_length = (before.nFileSizeHigh << 32) | before.nFileSizeLow
        file_version, product_version = _windows_file_versions(
            os.fspath(path),
            version,
        )
        metadata = DirectInterpreterMetadata(
            runtime_implementation=(
                "CPython" if sys.implementation.name == "cpython" else ""
            ),
            executable_basename=path.name,
            file_version=file_version,
            product_version=product_version,
            byte_length=byte_length,
            file_sha256=digest.hexdigest(),
            stable_identity_sha256=_stable_file_identity_sha256(
                before.dwVolumeSerialNumber,
                file_index,
            ),
            ordinary_file=ordinary_file,
            reparse_point=reparse_point,
        )
    except ObservationFailure:
        raise
    except Exception as exc:
        raise ObservationFailure("observation_binding_rejected") from exc
    finally:
        close_failed = not bool(kernel32.CloseHandle(handle))
    if close_failed or metadata is None:
        raise ObservationFailure("observation_binding_rejected")
    return metadata


def validate_running_direct_interpreter(
    executable_path: str | os.PathLike[str] | None = None,
    *,
    observer: Callable[[Path], DirectInterpreterMetadata] | None = None,
) -> DirectInterpreterMetadata:
    try:
        path = Path(sys.executable if executable_path is None else executable_path)
    except (TypeError, ValueError) as exc:
        raise ObservationFailure("observation_binding_rejected") from exc
    if not path.is_absolute() or path.name != "python.exe":
        raise ObservationFailure("observation_binding_rejected")
    reader = _observe_windows_direct_interpreter if observer is None else observer
    try:
        first = reader(path)
        second = reader(path)
    except ObservationFailure:
        raise
    except Exception as exc:
        raise ObservationFailure("observation_binding_rejected") from exc
    if first != second:
        raise ObservationFailure("observation_binding_rejected")
    validate_direct_interpreter_metadata(first)
    return first


class AuditBoundary:
    """Fail closed on side effects or reads outside the fixed owner roots."""

    _PROCESS_EVENTS = {
        "subprocess.Popen",
        "os.system",
        "os.posix_spawn",
        "os.posix_spawnp",
        "os.startfile",
        "os.startfile/2",
    }
    _MUTATION_EVENTS = {
        "os.remove",
        "os.rename",
        "os.renames",
        "os.replace",
        "os.rmdir",
        "os.mkdir",
        "os.link",
        "os.symlink",
        "os.truncate",
        "os.chmod",
        "os.chown",
        "os.utime",
        "os.chdir",
        "shutil.copyfile",
        "shutil.copymode",
        "shutil.copystat",
        "shutil.rmtree",
        "shutil.move",
    }
    _ENVIRONMENT_EVENTS = {"os.putenv", "os.unsetenv"}
    _EXPANSION_EVENTS = {"os.listdir", "os.scandir", "glob.glob", "glob.glob/2"}

    def __init__(self, repository_root: Path, read_roots: Sequence[Path]) -> None:
        self._repository_root = os.path.normcase(os.path.abspath(repository_root))
        self._installed_root: str | None = None
        roots = (repository_root, *read_roots)
        self._read_roots = [os.path.normcase(os.path.abspath(root)) for root in roots]
        self.process_launch_attempt_count = 0
        self.network_operation_count = 0
        self.repository_write_count = 0
        self.installed_write_count = 0
        self.external_effect_count = 0

    def bind_installed_root(self, path: Path) -> None:
        root = os.path.normcase(os.path.abspath(path))
        self._installed_root = root
        if root not in self._read_roots:
            self._read_roots.append(root)

    @property
    def forbidden_attempt_count(self) -> int:
        return (
            self.process_launch_attempt_count
            + self.network_operation_count
            + self.repository_write_count
            + self.installed_write_count
            + self.external_effect_count
        )

    def _record_write(self, path: object) -> None:
        if _path_is_within(path, (self._repository_root,)):
            self.repository_write_count += 1
        elif self._installed_root is not None and _path_is_within(
            path,
            (self._installed_root,),
        ):
            self.installed_write_count += 1
        else:
            self.external_effect_count += 1

    @staticmethod
    def _open_is_write(args: tuple[object, ...]) -> bool:
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else 0
        if isinstance(mode, str) and any(marker in mode for marker in "wax+"):
            return True
        write_flags = (
            os.O_WRONLY
            | os.O_RDWR
            | os.O_APPEND
            | os.O_CREAT
            | os.O_TRUNC
            | os.O_EXCL
        )
        return isinstance(flags, int) and bool(flags & write_flags)

    def __call__(self, event: str, args: tuple[object, ...]) -> None:
        if event in self._PROCESS_EVENTS or event.startswith("os.spawn"):
            self.process_launch_attempt_count += 1
            raise SafetyBoundaryViolation
        if event.startswith("socket."):
            self.network_operation_count += 1
            raise SafetyBoundaryViolation
        if event in self._ENVIRONMENT_EVENTS:
            self.external_effect_count += 1
            raise SafetyBoundaryViolation
        if event == "open":
            path = args[0] if args else None
            if self._open_is_write(args):
                self._record_write(path)
                raise SafetyBoundaryViolation
            if not _path_is_within(path, self._read_roots):
                self.external_effect_count += 1
                raise SafetyBoundaryViolation
            return
        if event in self._MUTATION_EVENTS:
            self._record_write(args[0] if args else None)
            raise SafetyBoundaryViolation
        if event in self._EXPANSION_EVENTS:
            path = args[0] if args and args[0] is not None else os.getcwd()
            if not _path_is_within(path, self._read_roots):
                self.external_effect_count += 1
                raise SafetyBoundaryViolation


def _stable_payload(path: Path) -> bytes:
    try:
        before = path.lstat()
        marker = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_ISLNK(before.st_mode)
            or bool(getattr(before, "st_file_attributes", 0) & marker)
        ):
            raise ObservationFailure("observation_binding_rejected")
        with path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            payload = handle.read()
            after_read = os.fstat(handle.fileno())
        after = path.lstat()
    except ObservationFailure:
        raise
    except OSError as exc:
        raise ObservationUnknown("observation_result_unknown") from exc
    identity = lambda item: (  # noqa: E731 - compact immutable identity projection
        item.st_dev,
        item.st_ino,
        item.st_mode,
        item.st_size,
        item.st_mtime_ns,
    )
    if identity(before) != identity(opened) or identity(before) != identity(after_read):
        raise ObservationUnknown("observation_result_unknown")
    if identity(before) != identity(after):
        raise ObservationUnknown("observation_result_unknown")
    return payload


def _load_checker(repository_root: Path) -> ModuleType:
    for relative_path, expected_sha256 in (
        (SEQUENCE_CONTRACT_RELATIVE_PATH, SEQUENCE_CONTRACT_SHA256),
        (RECEIPT_ORDER_CONTRACT_RELATIVE_PATH, RECEIPT_ORDER_CONTRACT_SHA256),
        (RECEIPT_ORDER_REVIEW_RELATIVE_PATH, RECEIPT_ORDER_REVIEW_SHA256),
        (PROPORTIONATE_CONTRACT_RELATIVE_PATH, PROPORTIONATE_CONTRACT_SHA256),
        (PROPORTIONATE_REVIEW_RELATIVE_PATH, PROPORTIONATE_REVIEW_SHA256),
    ):
        payload = _stable_payload(repository_root / relative_path)
        if hashlib.sha256(payload).hexdigest() != expected_sha256:
            raise ObservationFailure("observation_binding_rejected")
    checker_path = repository_root / R0_CHECKER_RELATIVE_PATH
    checker_payload = _stable_payload(checker_path)
    if hashlib.sha256(checker_payload).hexdigest() != R0_CHECKER_SHA256:
        raise ObservationFailure("observation_binding_rejected")
    specification = importlib.util.spec_from_file_location(
        "_role_pool_r0_offline_observation_owner",
        checker_path,
    )
    if specification is None or specification.loader is None:
        raise ObservationUnknown("observation_result_unknown")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    try:
        specification.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(specification.name, None)
        raise ObservationUnknown("observation_result_unknown") from exc
    return module


def _validate_bootstrap_packet(packet: object) -> None:
    if not isinstance(packet, dict):
        raise ObservationFailure("observation_validation_failed")
    expected = {
        "schema_version": "trusted_owner_r0_offline_bootstrap_evidence.v1",
        "operation": "evaluate_r0_bootstrap_eligibility_read_only",
        "repository_id": REPOSITORY_ID,
        "repository_name": "tahjali11/mythic-edge",
        "issue_url": "https://github.com/Tahjali11/Mythic-Edge/issues/761",
        "base_commit": "10d4a4a79053fe33297a612599667d9b58bb4296",
        "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
        "app_server_contract_sha256": (
            "814ac91c4e099216ae4870458d7524a3d65bfba7459cbfda7de82a5fc79067e8"
        ),
        "r0_contract_sha256": (
            "07ab1c7153ba1312533bdc27d984789127fb7fc02190d26853ffae1849c2ac82"
        ),
        "contract_binding_status": "exact",
        "stage3_manifest_file_count": 39,
        "stage3_manifest_byte_count": 5729,
        "stage3_manifest_sha256": (
            "cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06"
        ),
        "manifest_status": "exact",
        "source_tree_node_count": 41,
        "source_tree_file_count": 36,
        "source_tree_manifest_byte_count": 6495,
        "source_tree_sha256": SOURCE_TREE_SHA256,
        "installed_tree_node_count": 41,
        "installed_tree_file_count": 36,
        "installed_tree_manifest_byte_count": 6495,
        "installed_tree_sha256": SOURCE_TREE_SHA256,
        "source_install_status": "identical",
        "registry_status": "valid_exact",
        "registry_sha256": REGISTRY_SHA256,
        "release_state_status": "present_valid_chain",
        "release_state_sha256": RELEASE_STATE_ARTIFACT_SHA256,
        "checker_sha256": R0_CHECKER_SHA256,
        "checker_test_sha256": R0_CHECKER_TEST_SHA256,
        "validator_bundle_sha256": VALIDATOR_BUNDLE_SHA256,
        "validator_bundle_status": "exact",
        "offline_validation_status": "passed",
        "terminal_status": "blocked_release_state_conflict",
        "eligible_for_independent_review": False,
    }
    if any(
        field not in packet or not _json_values_are_exact(packet[field], value)
        for field, value in expected.items()
    ):
        raise ObservationFailure("observation_binding_rejected")
    effects = packet.get("effect_counts")
    authority = packet.get("authority_flags")
    if (
        not isinstance(effects, dict)
        or tuple(effects) != VALIDATION_EFFECT_FIELDS
        or any(type(value) is not int or value != 0 for value in effects.values())
    ):
        raise ObservationFailure("observation_safety_boundary_failed")
    if (
        not isinstance(authority, dict)
        or tuple(authority) != AUTHORITY_FIELDS
        or any(type(value) is not bool or value for value in authority.values())
    ):
        raise ObservationFailure("observation_safety_boundary_failed")
    evidence_sha256 = packet.get("evidence_sha256")
    if (
        not _is_sha256(evidence_sha256)
        or evidence_sha256 != self_digest(packet, "evidence_sha256")
    ):
        raise ObservationFailure("observation_validation_failed")


def parse_validation_payload(payload: bytes) -> dict[str, object]:
    """Parse the nonpublishable child validation payload exactly."""

    if len(payload) > MAX_STDOUT_BYTES:
        raise ObservationFailure("observation_result_unknown")
    packet = _parse_canonical_object(payload, VALIDATION_PAYLOAD_FIELDS)
    _validate_bootstrap_packet(packet)
    return packet


@dataclass(frozen=True)
class PostExitFacts:
    """Closed parent-owned facts observed only after process-tree termination."""

    top_level_process_count: int
    descendant_process_count: int
    process_relationships_known: bool
    process_terminal_states_known: bool
    surviving_process_count: int
    top_level_identity_exact: bool | None
    timed_out: bool
    termination_uncertain: bool
    cleanup_confirmed: bool
    output_complete: bool
    executor_network_operation_count: int
    repository_write_count: int
    installed_write_count: int
    external_effect_count: int
    generated_residue_count: int


def _post_exit_status(facts: PostExitFacts) -> str:
    integer_fields = (
        facts.top_level_process_count,
        facts.descendant_process_count,
        facts.surviving_process_count,
        facts.executor_network_operation_count,
        facts.repository_write_count,
        facts.installed_write_count,
        facts.external_effect_count,
        facts.generated_residue_count,
    )
    boolean_fields = (
        facts.process_relationships_known,
        facts.process_terminal_states_known,
        facts.timed_out,
        facts.termination_uncertain,
        facts.cleanup_confirmed,
        facts.output_complete,
    )
    identity_valid = facts.top_level_identity_exact is None or type(
        facts.top_level_identity_exact
    ) is bool
    if (
        any(type(value) is not int or value < 0 for value in integer_fields)
        or any(type(value) is not bool for value in boolean_fields)
        or not identity_valid
        or facts.top_level_process_count != 1
        or not facts.process_relationships_known
    ):
        return "observation_launch_unknown"
    if (
        facts.timed_out
        or facts.termination_uncertain
        or not facts.process_terminal_states_known
        or not facts.cleanup_confirmed
    ):
        return "observation_timeout_unknown"
    if (
        facts.descendant_process_count > 1
        or facts.surviving_process_count != 0
        or facts.executor_network_operation_count != 0
        or facts.repository_write_count != 0
        or facts.installed_write_count != 0
        or facts.external_effect_count != 0
        or facts.generated_residue_count != 0
    ):
        return "observation_safety_boundary_failed"
    if not facts.output_complete:
        return "observation_result_unknown"
    return "accepted_exact_r0_offline_observation"


def seal_proportionate_observation_receipt(
    validation_payload: bytes,
    post_exit_facts: PostExitFacts,
    sequence_position: int,
) -> bytes | str:
    """Seal one receipt from exact validation and parent-owned terminal facts."""

    try:
        parse_validation_payload(validation_payload)
        if type(post_exit_facts) is not PostExitFacts:
            return "observation_launch_unknown"
        if type(sequence_position) is not int or sequence_position not in (1, 2):
            return "observation_sequence_rejected"
        status = _post_exit_status(post_exit_facts)
        if status != "accepted_exact_r0_offline_observation":
            return status
        receipt = _build_receipt(
            sequence_position,
            post_exit_facts.descendant_process_count,
            post_exit_facts.top_level_identity_exact,
        )
        payload = canonical_bytes(receipt)
        if parse_receipt(payload) != receipt:
            return "observation_receipt_sealing_failed"
        return payload
    except ObservationFailure as exc:
        return exc.status
    except Exception:
        return "observation_result_unknown"


def _validate_release_and_reobserve(checker: ModuleType, roots: object) -> None:
    repository_root = roots.repository_root
    owners = checker._load_owner_modules(repository_root)
    release = checker._read_stable_file(
        repository_root / checker.RELEASE_STATE_RELATIVE_PATH
    )
    if release.state != "exact" or release.payload is None:
        raise ObservationFailure("observation_validation_failed")
    if hashlib.sha256(release.payload).hexdigest() != RELEASE_STATE_ARTIFACT_SHA256:
        raise ObservationFailure("observation_binding_rejected")
    records: list[dict[str, object]] = []
    try:
        for line in release.payload.splitlines(keepends=True):
            record = owners.pool.parse_trusted_native_json(line.decode("utf-8"))
            if owners.pool.validate_trusted_native_release_record(record):
                raise ObservationFailure("observation_validation_failed")
            records.append(record)
    except ObservationFailure:
        raise
    except Exception as exc:
        raise ObservationFailure("observation_validation_failed") from exc
    if (
        len(records) != 1
        or records[0].get("record_sha256") != RELEASE_RECORD_SHA256
        or owners.pool.validate_trusted_native_release_chain(records)
        or owners.pool.trusted_native_current_rung(records) != "R0"
    ):
        raise ObservationFailure("observation_validation_failed")
    ceiling_errors = owners.pool.validate_trusted_native_release_ceiling(
        "R0",
        mode="offline",
        role=None,
        lane_count=0,
        wave_count=0,
        operation_id="offline_validation",
        claim_creation=False,
        task_creation=False,
        f_publication=False,
    )
    if ceiling_errors:
        raise ObservationFailure("observation_validation_failed")

    binding_status, observed_bindings = checker._binding_status(repository_root)
    workflow_root = roots.installed_skills_root / "mythic-edge-workflow"
    manifest = checker._manifest_observation(owners.stage3, workflow_root)
    source, installed, source_install = checker._tree_observations(roots, owners)
    fixed = checker._fixed_inputs(repository_root, owners.pool)
    checker_payload = checker._read_stable_file(
        repository_root / checker.CHECKER_RELATIVE_PATH
    )
    test_payload = checker._read_stable_file(
        repository_root / checker.CHECKER_TEST_RELATIVE_PATH
    )
    if checker_payload.payload is None or test_payload.payload is None:
        raise ObservationUnknown("observation_result_unknown")
    checker_sha = hashlib.sha256(checker_payload.payload).hexdigest()
    test_sha = hashlib.sha256(test_payload.payload).hexdigest()
    bundle = checker._validator_bundle(checker_sha, test_sha, owners.pool)
    exact = (
        binding_status == "exact"
        and observed_bindings.get("registry_validator") == RELEASE_VALIDATOR_SHA256
        and manifest.status == "exact"
        and manifest.file_count == 39
        and source.status == "observed"
        and installed.status == "observed"
        and source.sha256 == SOURCE_TREE_SHA256
        and installed.sha256 == SOURCE_TREE_SHA256
        and source_install == "identical"
        and fixed.registry_status == "valid_exact"
        and fixed.registry_sha256 == REGISTRY_SHA256
        and fixed.release_state_status == "present_valid_chain"
        and fixed.release_state_sha256 == RELEASE_STATE_ARTIFACT_SHA256
        and checker_sha == R0_CHECKER_SHA256
        and test_sha == R0_CHECKER_TEST_SHA256
        and bundle == VALIDATOR_BUNDLE_SHA256
        and checker._offline_validation_status(owners) == "passed"
    )
    if not exact:
        raise ObservationFailure("observation_validation_failed")


def evaluate_observation(
    observation_id: str,
    *,
    checker: ModuleType,
    roots: object,
    audit_boundary: AuditBoundary,
    runtime_os_name: str,
    runtime_sys_platform: str,
) -> bytes:
    """Evaluate one identity; injection points exist only for synthetic tests."""

    if runtime_os_name != "nt" or runtime_sys_platform != "win32":
        raise ObservationFailure("observation_host_rejected")
    if observation_id not in OBSERVATION_IDS:
        raise ObservationFailure("observation_sequence_rejected")
    try:
        packet, encoded = checker._evaluate_roots(roots)
    except SafetyBoundaryViolation:
        raise
    except Exception as exc:
        raise ObservationUnknown("observation_result_unknown") from exc
    _validate_bootstrap_packet(packet)
    if not isinstance(encoded, bytes):
        raise ObservationFailure("observation_validation_failed")
    if parse_validation_payload(encoded) != packet:
        raise ObservationFailure("observation_validation_failed")
    _validate_release_and_reobserve(checker, roots)
    if audit_boundary.forbidden_attempt_count != 0:
        raise SafetyBoundaryViolation
    return encoded


@dataclass(frozen=True)
class LauncherObservation:
    exit_code: int | None
    stdout: bytes
    stderr: bytes
    top_level_process_count: int
    descendant_process_count: int
    process_relationships_known: bool
    process_terminal_states_known: bool
    surviving_process_count: int
    top_level_identity_exact: bool | None
    timed_out: bool
    termination_uncertain: bool
    cleanup_confirmed: bool
    output_complete: bool
    executor_network_operation_count: int
    repository_write_count: int
    installed_write_count: int
    external_effect_count: int
    generated_residue_count: int

    def post_exit_facts(self) -> PostExitFacts:
        return PostExitFacts(
            top_level_process_count=self.top_level_process_count,
            descendant_process_count=self.descendant_process_count,
            process_relationships_known=self.process_relationships_known,
            process_terminal_states_known=self.process_terminal_states_known,
            surviving_process_count=self.surviving_process_count,
            top_level_identity_exact=self.top_level_identity_exact,
            timed_out=self.timed_out,
            termination_uncertain=self.termination_uncertain,
            cleanup_confirmed=self.cleanup_confirmed,
            output_complete=self.output_complete,
            executor_network_operation_count=self.executor_network_operation_count,
            repository_write_count=self.repository_write_count,
            installed_write_count=self.installed_write_count,
            external_effect_count=self.external_effect_count,
            generated_residue_count=self.generated_residue_count,
        )


@dataclass(frozen=True)
class DirectLauncherObservation:
    public_binding_exact: bool
    private_binding_exact: bool
    top_level_identity_exact: bool
    parentage_known: bool
    process: LauncherObservation


@dataclass(frozen=True)
class DirectPreflightObservation:
    public_binding_exact: bool
    private_binding_exact: bool
    top_level_identity_exact: bool
    parentage_known: bool
    exit_code: int | None
    stdout: bytes
    stderr: bytes
    top_level_process_count: int
    descendant_process_count: int
    timed_out: bool
    cleanup_confirmed: bool
    output_complete: bool


def classify_launcher_observation(observation: LauncherObservation) -> str:
    """Classify fake launcher evidence without launching a process."""

    if observation.exit_code is None:
        return "observation_launch_unknown"
    status = _post_exit_status(observation.post_exit_facts())
    if status != "accepted_exact_r0_offline_observation":
        return status
    if len(observation.stdout) > MAX_STDOUT_BYTES or len(observation.stderr) > MAX_FAILURE_STDERR_BYTES:
        return "observation_result_unknown"
    if observation.exit_code == 0:
        if observation.stderr:
            return "observation_validation_failed"
        try:
            parse_validation_payload(observation.stdout)
        except ObservationFailure:
            return "observation_validation_failed"
        return "accepted_exact_r0_offline_observation"
    if observation.exit_code == 4:
        return "observation_safety_boundary_failed"
    if observation.exit_code == 3:
        return "observation_result_unknown"
    return "observation_validation_failed"


def classify_direct_launcher_observation(
    observation: DirectLauncherObservation,
) -> str:
    if not observation.public_binding_exact:
        return "observation_binding_rejected"
    return classify_launcher_observation(observation.process)


def classify_direct_preflight_observation(
    observation: DirectPreflightObservation,
) -> str:
    if not observation.public_binding_exact or not observation.private_binding_exact:
        return "observation_binding_rejected"
    if observation.timed_out or not observation.cleanup_confirmed:
        return "direct_interpreter_preflight_unknown"
    if (
        observation.exit_code is None
        or observation.top_level_process_count != 1
        or not observation.top_level_identity_exact
        or not observation.parentage_known
    ):
        return "direct_interpreter_preflight_unknown"
    if observation.descendant_process_count != 0:
        return "direct_interpreter_preflight_descendant_observed"
    if (
        not observation.output_complete
        or observation.stdout
        or observation.stderr
        or observation.exit_code != 0
    ):
        return "direct_interpreter_preflight_unknown"
    return "direct_interpreter_preflight_passed"


def _write_exact_bytes(stream: TextIO, payload: bytes) -> None:
    binary = getattr(stream, "buffer", None)
    if binary is None:
        stream.write(payload.decode("utf-8"))
    else:
        binary.write(payload)


def _emit_failure(status: str) -> None:
    payload = status.encode("ascii") + b"\n"
    if len(payload) > MAX_FAILURE_STDERR_BYTES:
        payload = b"observation_result_unknown\n"
    _write_exact_bytes(sys.stderr, payload)


def run(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 1 or arguments[0] not in OBSERVATION_IDS:
        _emit_failure("observation_sequence_rejected")
        return 2
    if os.name != "nt" or sys.platform != "win32":
        _emit_failure("observation_host_rejected")
        return 2
    if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1" or not sys.dont_write_bytecode:
        _emit_failure("observation_safety_boundary_failed")
        return 4
    repository_root = Path(__file__).absolute().parent.parent
    if not _paths_are_lexically_equal(Path.cwd(), repository_root):
        _emit_failure("observation_binding_rejected")
        return 2
    runtime_roots = tuple({Path(sys.base_prefix), Path(sys.prefix)})
    audit = AuditBoundary(repository_root, runtime_roots)
    sys.addaudithook(audit)
    try:
        checker = _load_checker(repository_root)
        roots = checker._production_roots()
        if roots.installed_skills_root is None:
            raise ObservationFailure("observation_binding_rejected")
        audit.bind_installed_root(roots.installed_skills_root)
        payload = evaluate_observation(
            arguments[0],
            checker=checker,
            roots=roots,
            audit_boundary=audit,
            runtime_os_name=os.name,
            runtime_sys_platform=sys.platform,
        )
    except SafetyBoundaryViolation as exc:
        _emit_failure(exc.status)
        return 4
    except ObservationUnknown as exc:
        _emit_failure(exc.status)
        return 3
    except ObservationFailure as exc:
        _emit_failure(exc.status)
        return 2
    except Exception:
        _emit_failure("observation_result_unknown")
        return 3
    _write_exact_bytes(sys.stdout, payload)
    return 0


def _validate_known_answers() -> None:
    binding = canonical_bytes(DIRECT_INTERPRETER_BINDING)
    binding_preimage = canonical_bytes(
        {
            key: value
            for key, value in DIRECT_INTERPRETER_BINDING.items()
            if key != "binding_sha256"
        }
    )
    if (
        len(binding_preimage) != 694
        or len(binding) != 778
        or self_digest(DIRECT_INTERPRETER_BINDING, "binding_sha256")
        != DIRECT_INTERPRETER_BINDING_SHA256
        or hashlib.sha256(binding).hexdigest()
        != DIRECT_INTERPRETER_BINDING_ARTIFACT_SHA256
        or parse_direct_interpreter_binding(binding) != DIRECT_INTERPRETER_BINDING
    ):
        raise RuntimeError("direct_interpreter_binding_kat_invalid")
    profile = canonical_bytes(OBSERVATION_PROFILE)
    if (
        len(profile) != 1918
        or hashlib.sha256(profile).hexdigest() != OBSERVATION_PROFILE_SHA256
    ):
        raise RuntimeError("observation_profile_kat_invalid")
    for position_index, receipts in enumerate(EXPECTED_RECEIPTS):
        for variant_index, receipt in enumerate(receipts):
            preimage = canonical_bytes(
                {
                    key: value
                    for key, value in receipt.items()
                    if key != "receipt_sha256"
                }
            )
            payload = canonical_bytes(receipt)
            if (
                len(preimage)
                != EXPECTED_RECEIPT_PREIMAGE_LENGTHS[position_index][variant_index]
                or len(payload)
                != EXPECTED_RECEIPT_LENGTHS[position_index][variant_index]
                or receipt["receipt_sha256"]
                != EXPECTED_RECEIPT_SHA256S[position_index][variant_index]
                or hashlib.sha256(payload).hexdigest()
                != EXPECTED_RECEIPT_ARTIFACT_SHA256S[position_index][variant_index]
            ):
                raise RuntimeError("observation_receipt_kat_invalid")
    consumption = canonical_bytes(SYNTHETIC_CONSUMPTION_KAT)
    consumption_preimage = canonical_bytes(
        {
            key: value
            for key, value in SYNTHETIC_CONSUMPTION_KAT.items()
            if key != "consumption_sha256"
        }
    )
    if (
        len(consumption_preimage) != 2869
        or len(consumption) != 2957
        or SYNTHETIC_CONSUMPTION_KAT["consumption_sha256"]
        != "4f54d1df7627e9ac544822d4b140ed87ba47dea682137a6bbc3654910f5b29ca"
        or hashlib.sha256(consumption).hexdigest()
        != "eab4d6326ee187d641ed0a3b63e958229e66e4aea4cc3d2573a27916d79a57e1"
    ):
        raise RuntimeError("observation_consumption_kat_invalid")


_validate_known_answers()


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
