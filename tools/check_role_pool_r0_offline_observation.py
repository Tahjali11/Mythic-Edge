#!/usr/bin/env python3
"""Project one contracted R0 offline observation without persistent effects.

The live CLI is intentionally narrow: it accepts one predeclared observation
identity and emits either that identity's exact receipt or one symbolic failure
status. Authority consumption and GitHub publication remain executor-owned.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Mapping, Sequence, TextIO

SEQUENCE_CONTRACT_RELATIVE_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_offline_observation_sequence.md"
)
SEQUENCE_CONTRACT_SHA256 = (
    "df6cce588e6d64ba5ba24b5d8d7f267c9c9a7e769c9a254527a9e7fd3d68e2b8"
)
R0_CHECKER_RELATIVE_PATH = Path("tools/check_role_pool_r0_bootstrap.py")
R0_CHECKER_SHA256 = (
    "34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914"
)

REPOSITORY_ID = 1235264383
ISSUE_NUMBER = 776
PROTECTED_ISSUE_NUMBER = 769
CURRENT_RUNG = "R0"
SEQUENCE_ID = "r0.offline.sequence.1d11e7476ab400a39d222d0feab38eba"
OBSERVATION_IDS = (
    "r0.offline.observation.1.094221964ddd0af9c3b2034a35347971",
    "r0.offline.observation.2.45b674178dd44c9b6723f42e75f3b04f",
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
    "0d97f23b96dfab5b6b459bea92df63a8bc6675c50632ace60a36f7e1cbea2124"
)
EXPECTED_RECEIPT_SHA256S = (
    "3bbc18f5af98ac88f9d2b38bac8c1ebc24d828129517368b68f420ae8988f60a",
    "d059de10976d0652c60dc29f0e55c18393cbf337b870befd85875359adf4d769",
)
EXPECTED_RECEIPT_ARTIFACT_SHA256S = (
    "f01466254996a3332d1406ab0dfbfe73bce3c99ecf279ba8d5fd46014dd5654f",
    "8994ad1d631f6163613cd24fb6baba3a7603e23b805d6c6837835b272b25c5d1",
)
EXPECTED_RECEIPT_PREIMAGE_LENGTHS = (2333, 2388)
EXPECTED_RECEIPT_LENGTHS = (2417, 2472)

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
    "expected_receipt_sha256",
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


OBSERVATION_PROFILE: dict[str, object] = {
    "schema_version": "trusted_owner_r0_offline_observation_profile.v1",
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
    "host_os_name": "nt",
    "host_sys_platform": "win32",
    "top_level_process_limit": 1,
    "descendant_process_limit": 0,
    "process_launch_attempt_limit": 0,
    "network_operation_limit": 0,
    "external_effect_limit": 0,
    "observation_count": 2,
    "timeout_seconds": 120,
    "retry_limit": 0,
}


def _build_receipt(position: int) -> dict[str, object]:
    if position not in (1, 2):
        raise ObservationFailure("observation_sequence_rejected")
    receipt: dict[str, object] = {
        "schema_version": "trusted_owner_r0_offline_observation_receipt.v1",
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
        "process_topology": "single_top_level_process_zero_descendants",
        "top_level_process_count": 1,
        "descendant_process_count": 0,
        "process_launch_attempt_count": 0,
        "network_operation_count": 0,
        "repository_write_count": 0,
        "installed_write_count": 0,
        "external_effect_count": 0,
        "retry_count": 0,
        "unknown_outcome_count": 0,
        "cleanup_status": "no_attempt_owned_artifacts",
        "accepted_for_independent_review": True,
        "authority_flags": _authority_flags(),
        "receipt_sha256": "",
    }
    receipt["receipt_sha256"] = self_digest(receipt, "receipt_sha256")
    return receipt


EXPECTED_RECEIPTS = (_build_receipt(1), _build_receipt(2))


def parse_receipt(payload: bytes) -> dict[str, object]:
    if len(payload) > MAX_STDOUT_BYTES:
        raise ObservationFailure("observation_result_unknown")
    receipt = _parse_canonical_object(payload, RECEIPT_FIELDS)
    position = receipt.get("sequence_position")
    if type(position) is not int or position not in (1, 2):
        raise ObservationFailure("observation_validation_failed")
    expected = EXPECTED_RECEIPTS[position - 1]
    if not _json_values_are_exact(receipt, expected):
        raise ObservationFailure("observation_validation_failed")
    if receipt["receipt_sha256"] != self_digest(receipt, "receipt_sha256"):
        raise ObservationFailure("observation_validation_failed")
    return receipt


def validate_receipt_pair(payloads: Sequence[bytes]) -> tuple[dict[str, object], ...]:
    if len(payloads) != 2:
        raise ObservationFailure("observation_sequence_rejected")
    receipts = tuple(parse_receipt(payload) for payload in payloads)
    if tuple(receipt["sequence_position"] for receipt in receipts) != (1, 2):
        raise ObservationFailure("observation_sequence_rejected")
    digests = tuple(str(receipt["receipt_sha256"]) for receipt in receipts)
    if digests != EXPECTED_RECEIPT_SHA256S or list(digests) != sorted(digests):
        raise ObservationFailure("observation_sequence_rejected")
    if receipts[1]["predecessor_observation_id"] != receipts[0]["observation_id"]:
        raise ObservationFailure("observation_sequence_rejected")
    return receipts


SYNTHETIC_CONSUMPTION_KAT: dict[str, object] = {
    "schema_version": "trusted_owner_r0_offline_observation_consumption.v1",
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
    "expected_receipt_sha256": EXPECTED_RECEIPT_SHA256S[0],
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
        "schema_version": "trusted_owner_r0_offline_observation_consumption.v1",
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
    if consumption["expected_receipt_sha256"] != EXPECTED_RECEIPT_SHA256S[position - 1]:
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
    if predecessor_receipt is None or parse_receipt(predecessor_receipt) != EXPECTED_RECEIPTS[0]:
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
    contract_payload = _stable_payload(repository_root / SEQUENCE_CONTRACT_RELATIVE_PATH)
    if hashlib.sha256(contract_payload).hexdigest() != SEQUENCE_CONTRACT_SHA256:
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
        "contract_binding_status": "exact",
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
        raise ObservationFailure("observation_validation_failed")
    effects = packet.get("effect_counts")
    authority = packet.get("authority_flags")
    if not isinstance(effects, dict) or any(
        type(value) is not int or value != 0 for value in effects.values()
    ):
        raise ObservationFailure("observation_safety_boundary_failed")
    if (
        not isinstance(authority, dict)
        or tuple(authority) != AUTHORITY_FIELDS
        or any(type(value) is not bool or value for value in authority.values())
    ):
        raise ObservationFailure("observation_safety_boundary_failed")


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
    _validate_release_and_reobserve(checker, roots)
    if audit_boundary.forbidden_attempt_count != 0:
        raise SafetyBoundaryViolation
    position = OBSERVATION_IDS.index(observation_id) + 1
    receipt = _build_receipt(position)
    payload = canonical_bytes(receipt)
    try:
        sealed = parse_receipt(payload)
    except ObservationFailure as exc:
        raise ObservationFailure("observation_receipt_sealing_failed") from exc
    if sealed != receipt or len(payload) > MAX_STDOUT_BYTES:
        raise ObservationFailure("observation_receipt_sealing_failed")
    return payload


@dataclass(frozen=True)
class LauncherObservation:
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

    if observation.timed_out or not observation.cleanup_confirmed:
        return "observation_timeout_unknown"
    if observation.exit_code is None or observation.top_level_process_count != 1:
        return "observation_launch_unknown"
    if observation.descendant_process_count != 0:
        return "observation_safety_boundary_failed"
    if not observation.output_complete:
        return "observation_result_unknown"
    if len(observation.stdout) > MAX_STDOUT_BYTES or len(observation.stderr) > MAX_FAILURE_STDERR_BYTES:
        return "observation_result_unknown"
    if observation.exit_code == 0:
        if observation.stderr:
            return "observation_result_unknown"
        try:
            parse_receipt(observation.stdout)
        except ObservationFailure:
            return "observation_validation_failed"
        return "accepted_exact_r0_offline_observation"
    if observation.exit_code == 4:
        return "observation_safety_boundary_failed"
    if observation.exit_code == 3:
        return "observation_result_unknown"
    return "observation_validation_failed"


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
    profile = canonical_bytes(OBSERVATION_PROFILE)
    if len(profile) != 1616 or hashlib.sha256(profile).hexdigest() != OBSERVATION_PROFILE_SHA256:
        raise RuntimeError("observation_profile_kat_invalid")
    for index, receipt in enumerate(EXPECTED_RECEIPTS):
        preimage = canonical_bytes(
            {key: value for key, value in receipt.items() if key != "receipt_sha256"}
        )
        payload = canonical_bytes(receipt)
        if (
            len(preimage) != EXPECTED_RECEIPT_PREIMAGE_LENGTHS[index]
            or len(payload) != EXPECTED_RECEIPT_LENGTHS[index]
            or receipt["receipt_sha256"] != EXPECTED_RECEIPT_SHA256S[index]
            or hashlib.sha256(payload).hexdigest()
            != EXPECTED_RECEIPT_ARTIFACT_SHA256S[index]
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
        len(consumption_preimage) != 2526
        or len(consumption) != 2614
        or SYNTHETIC_CONSUMPTION_KAT["consumption_sha256"]
        != "6d0e6a9aeb895c75a43cc013cf895016570574e836fdca67a0ea2071bc441ab1"
        or hashlib.sha256(consumption).hexdigest()
        != "5fdd20f34258315199dc15ab416e9243eb68190171f514ad2c037f1afde0b4f2"
    ):
        raise RuntimeError("observation_consumption_kat_invalid")


_validate_known_answers()


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
