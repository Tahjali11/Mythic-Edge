#!/usr/bin/env python3
"""Resolve Codex safely and provide a direct one-process-start test contract.

The command-line entry point is preflight-only.  It reads local executable
metadata, help text, and the bundled model catalog; it never calls
``codex exec``. Runtime harnesses may import ``build_codex_exec_args`` for exact
argument preparation. The public direct ``launch_once`` entry point is retired
and fails closed before process creation.

``launch_once`` is retained as fail-closed migration code.  The production and
Stage-4 contract in ``references/external-isolation-broker.md`` requires the
external broker, not this module or ``subprocess.Popen``, to own process
creation and lifecycle.  Do not provision the placeholder production context
or treat a direct-Popen receipt as live evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import ntpath
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Mapping, Sequence


PREFLIGHT_SCHEMA_VERSION = "mythic_edge_role_pool_launcher_preflight.v1"
LAUNCH_RECEIPT_SCHEMA_VERSION = "mythic_edge_role_pool_single_start_receipt.v2"
BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION = "mythic_edge_role_pool_single_start_receipt.v3"
BROKER_RECEIPT_CHAIN_SCHEMA_VERSION = "mythic_edge_role_pool_broker_receipt_chain.v1"
BROKER_LAUNCH_REQUEST_SCHEMA_VERSION = "mythic_edge_role_pool_broker_launch_request.v1"
BROKER_RESERVATION_SCHEMA_VERSION = "mythic_edge_role_pool_broker_start_reservation.v1"
BROKER_BOUNDARY_SCHEMA_VERSION = "mythic_edge_role_pool_broker_boundary_ready_receipt.v1"
BROKER_START_SCHEMA_VERSION = "mythic_edge_role_pool_broker_start_receipt.v1"
BROKER_TERMINAL_SCHEMA_VERSION = "mythic_edge_role_pool_broker_terminal_receipt.v1"
BROKER_ABORT_SCHEMA_VERSION = "mythic_edge_role_pool_broker_abort_receipt.v1"
BROKER_RECEIPT_DOMAINS = {
    BROKER_RESERVATION_SCHEMA_VERSION: (
        "mythic_edge_role_pool_broker_start_reservation.v1"
    ),
    BROKER_BOUNDARY_SCHEMA_VERSION: (
        "mythic_edge_role_pool.broker_boundary_ready_receipt.v1"
    ),
    BROKER_START_SCHEMA_VERSION: "mythic_edge_role_pool.broker_start_receipt.v1",
    BROKER_TERMINAL_SCHEMA_VERSION: (
        "mythic_edge_role_pool.broker_terminal_receipt.v1"
    ),
    BROKER_ABORT_SCHEMA_VERSION: "mythic_edge_role_pool.broker_abort_receipt.v1",
}
CHILD_ENVIRONMENT_POLICY = "mythic_edge_role_pool_child_environment.v1"
AMBIENT_ENVIRONMENT_PROVENANCE = "ambient_process_environment"
_TEST_ENVIRONMENT_PROVENANCE = "internal_test_fixture"
EXTERNAL_ISOLATION_SCHEMA_VERSION = "mythic_edge_role_pool_external_isolation.v3"
ATTESTATION_ALGORITHM = "hmac-sha256"
EXTERNAL_ISOLATION_ATTESTATION_DOMAIN = (
    "mythic_edge_role_pool.external_isolation_receipt.v3"
)
LAUNCHER_SIDECAR_ATTESTATION_DOMAIN = (
    "mythic_edge_role_pool.launcher_receipt_sidecars.v1"
)
EXTERNAL_ISOLATION_MAX_TTL_SECONDS = 300
CODEX_CONTROL_PLANE_NETWORK_SCOPE = "codex_service_only"
# Direct execution remains available only through the private deterministic test
# seam. The broker identity is reserved for a future distinct receipt chain.
DIRECT_POPEN_LAUNCH_BACKEND = "subprocess_popen"
PRODUCTION_LAUNCH_BACKEND = "windows_isolation_broker"
TEST_LAUNCH_BACKEND = "internal_test_backend"
BROKER_RECEIPT_CHAIN_UNAVAILABLE_ERROR = (
    "broker receipt-chain validation is not implemented"
)
PREFERRED_MODEL = "gpt-5.6-sol"
PREFERRED_REASONING_EFFORT = "max"
REQUIRED_EXEC_FLAGS = (
    "--ephemeral",
    "--json",
    "--ignore-user-config",
    "--skip-git-repo-check",
    "--model",
    "-c",
    "--sandbox",
    "--cd",
    "--add-dir",
    "--output-schema",
)
CANDIDATE_FIELDS = {
    "path",
    "sha256",
    "length_bytes",
    "cli_version",
    "version_key",
    "supported_exec_flags",
    "missing_exec_flags",
    "bundled_model_catalog_available",
    "preferred_model_available",
    "usable",
    "sanitized_error_code",
    "probe_command_kinds",
    "probe_process_count",
}
SELECTED_EXECUTABLE_FIELDS = {
    "path",
    "sha256",
    "length_bytes",
    "cli_version",
    "supported_exec_flags",
    "bundled_model_catalog_available",
    "preferred_model_available",
}
SAFE_OS_ENVIRONMENT_KEYS = {
    "APPDATA",
    "COMSPEC",
    "HOMEDRIVE",
    "HOMEPATH",
    "LOCALAPPDATA",
    "NUMBER_OF_PROCESSORS",
    "PATH",
    "PATHEXT",
    "PROCESSOR_ARCHITECTURE",
    "PROGRAMDATA",
    "PROGRAMFILES",
    "PROGRAMFILES(X86)",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "USERPROFILE",
    "WINDIR",
}
ROLE_POOL_ENVIRONMENT_BINDING_KEYS = {
    "MYTHIC_EDGE_ROLE_POOL_ATTEMPT_SERIES_ID",
    "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_PATH",
    "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_SHA256",
    "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES",
    "MYTHIC_EDGE_ROLE_POOL_PACKET_PATH",
    "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256",
    "MYTHIC_EDGE_ROLE_POOL_SEQUENCE_INDEX",
}
ROLE_POOL_SHA256_BINDING_KEYS = {
    "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_SHA256",
    "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256",
}
ROLE_POOL_PATH_BINDING_KEYS = {
    "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_PATH",
    "MYTHIC_EDGE_ROLE_POOL_PACKET_PATH",
}
ROLE_POOL_POSITIVE_INTEGER_BINDING_KEYS = {
    "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES",
    "MYTHIC_EDGE_ROLE_POOL_SEQUENCE_INDEX",
}
UUID_TEXT_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
SENSITIVE_ENVIRONMENT_KEY_RE = re.compile(
    r"(?:API[_-]?KEY|AUTH|CREDENTIAL|PASSWORD|SECRET|TOKEN)", re.IGNORECASE
)
LAUNCH_RECEIPT_FIELDS = {
    "schema_version",
    "status",
    "first_failed_stage",
    "sanitized_error_code",
    "preflight_digest",
    "exact_argument_array",
    "executable_path",
    "executable_sha256",
    "executable_length_bytes",
    "payload_sha256",
    "payload_length_bytes",
    "environment_policy",
    "environment_source_provenance",
    "environment_safe_os_source_digest",
    "environment_digest",
    "environment_keys",
    "environment_source_key_count",
    "environment_retained_source_key_count",
    "environment_dropped_source_key_count",
    "environment_sensitive_source_key_count",
    "environment_binding_key_count",
    "launch_backend",
    "production_eligible",
    "external_isolation_receipt_digest",
    "pid",
    "process_start_count",
    "started_at",
    "completed_at",
    "exit_code",
    "timed_out",
    "stdout_sha256",
    "stdout_length_bytes",
    "stderr_sha256",
    "stderr_length_bytes",
    "relaunch_attempted",
    "stdout_content_included",
    "stderr_content_included",
    "single_start_guard_consumed_before_call",
    "single_start_guard_consume_attempted",
    "single_start_guard_consumed",
    "digest",
}
BROKER_LAUNCH_RECEIPT_FIELDS = LAUNCH_RECEIPT_FIELDS | {"broker_receipt_chain"}
BROKER_RECEIPT_CHAIN_FIELDS = {
    "schema_version",
    "launch_request",
    "reservation_receipt",
    "boundary_ready_receipt",
    "start_receipt",
    "terminal_receipt",
    "abort_receipt",
}
BROKER_BASE_RECEIPT_FIELDS = {
    "schema_version",
    "attestation_domain",
    "attestation_algorithm",
    "attestation_key_id",
    "verifier_identity",
    "evidence_source",
    "attestation",
    "digest",
}
BROKER_RESERVATION_FIELDS = BROKER_BASE_RECEIPT_FIELDS | {
    "launch_id",
    "launch_request_digest",
    "authority_digest",
    "attempt_series_id",
    "sequence_index",
    "idempotency_key",
    "broker_epoch",
    "verifier_epoch",
    "reservation_id",
    "reservation_status",
    "observed_at",
    "expires_at",
}
BROKER_BOUNDARY_FIELDS = BROKER_BASE_RECEIPT_FIELDS | {
    "launch_id",
    "launch_request_digest",
    "start_reservation_digest",
    "boundary_receipt_id",
    "broker_identity",
    "verifier_service_sid",
    "verifier_installation_id",
    "verifier_epoch",
    "process_identity",
    "bindings_digest",
    "observed_boundary",
    "observed_at",
    "expires_at",
}
BROKER_START_FIELDS = BROKER_BASE_RECEIPT_FIELDS | {
    "launch_id",
    "launch_request_digest",
    "start_reservation_digest",
    "boundary_ready_receipt_digest",
    "process_identity",
    "process_created_count",
    "process_resumed_count",
    "relaunch_attempted",
    "start_time",
    "post_resume_observation_digest",
    "observed_at",
}
BROKER_TERMINAL_FIELDS = BROKER_BASE_RECEIPT_FIELDS | {
    "launch_id",
    "launch_request_digest",
    "start_receipt_digest",
    "process_identity",
    "terminal_status",
    "terminal_reason",
    "completed_at",
    "exit_code",
    "timed_out",
    "cancelled",
    "stdout_sha256",
    "stdout_length_bytes",
    "stderr_sha256",
    "stderr_length_bytes",
    "job_termination_result",
    "cleanup_result",
    "process_created_count",
    "process_resumed_count",
    "relaunch_attempted",
    "final_process_count",
    "remaining_tracked_process_count",
    "remaining_temporary_file_count",
    "observed_at",
}
BROKER_ABORT_FIELDS = BROKER_BASE_RECEIPT_FIELDS | {
    "launch_id",
    "launch_request_digest",
    "start_reservation_digest",
    "latest_receipt_digest",
    "process_identity",
    "abort_state",
    "first_failed_stage",
    "sanitized_reason",
    "process_created_count",
    "process_resumed_count",
    "relaunch_attempted",
    "termination_observed",
    "zero_survivors_observed",
    "cleanup_result",
    "observed_at",
}
BROKER_LAUNCH_REQUEST_FIELDS = {
    "schema_version",
    "launch_id",
    "attempt_series_id",
    "sequence_index",
    "idempotency_key",
    "current_request_digest",
    "authority_digest",
    "canary_exception_digest",
    "expires_at",
    "broker_epoch",
    "verifier_epoch",
    "launcher_identity",
    "broker_identity",
    "verifier_identity",
    "launcher_preflight_digest",
    "executable",
    "cli_version",
    "arguments",
    "arguments_digest",
    "packet",
    "packet_bytes_equal_stdin",
    "output_schema",
    "child_script",
    "working_directory",
    "allowed_namespace_root",
    "read_only_roots",
    "writable_temp_root",
    "writable_cleanup_required",
    "denied_repository_policy",
    "appcontainer_sid",
    "child_environment",
    "policies",
    "root_workload_count",
    "allowed_tool_descendant_count",
    "nested_agent_allowed",
    "relaunch_allowed",
    "shell_mediation",
    "intended_use",
    "digest",
}
BROKER_FILE_BINDING_FIELDS = {"path", "sha256", "length_bytes"}
BROKER_POLICY_BINDING_FIELDS = {"policy_id", "digest"}
BROKER_POLICY_NAMES = {
    "token",
    "appcontainer",
    "job",
    "handle",
    "filesystem",
    "network",
    "process_count",
    "timeout",
    "control_plane",
}
BROKER_CHILD_ENVIRONMENT_FIELDS = {
    "keys",
    "entries",
    "digest",
    "credential_like_values_present",
    "user_profile_access",
}
BROKER_IDENTITY_FIELDS = {
    "service_sid",
    "scm_process_id",
    "pipe_server_process_id",
    "process_creation_time_utc_ticks",
    "binary_path",
    "binary_sha256",
    "binary_length_bytes",
    "signer_sha256",
    "installation_id",
    "provider_id",
    "broker_epoch",
    "restricted_service_configuration",
}
BROKER_OBSERVED_BOUNDARY_FIELDS = {
    "executable_path",
    "executable_sha256",
    "executable_length_bytes",
    "primary_thread_suspended",
    "process_created_count",
    "process_resumed_count",
    "final_job_membership",
    "restricted_token",
    "appcontainer_token",
    "appcontainer_identity_exact",
    "network_capabilities_absent",
    "namespace_no_reparse",
    "namespace_acl_read_only",
    "writable_root_scoped",
    "writable_acl_scoped",
    "job_no_breakaway",
    "job_kill_on_close",
    "explicit_inherited_handle_set",
    "process_limit_enforced",
}
VERSION_RE = re.compile(
    r"\bcodex-cli\s+(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?\b"
)

CommandRunner = Callable[[Sequence[str]], subprocess.CompletedProcess[str]]


class DuplicateKeyError(ValueError):
    """Raised when supposedly typed JSON contains a duplicate object key."""


class SingleStartGuard:
    """Thread-safe, process-local guard that permits one Popen attempt."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._consumed = False

    def consume(self) -> bool:
        with self._lock:
            if self._consumed:
                return False
            self._consumed = True
            return True

    @property
    def consumed(self) -> bool:
        with self._lock:
            return self._consumed


@dataclass(frozen=True)
class LaunchOutcome:
    """In-memory child bytes plus the separately serializable safe receipt."""

    receipt: dict[str, Any]
    stdout_bytes: bytes = field(repr=False)
    stderr_bytes: bytes = field(repr=False)
    broker_verification_context: object | None = field(default=None, repr=False)


class ProductionVerificationContext:
    """Opaque production trust capability placeholder.

    Step 1 deliberately provisions no live verifier.  The earlier key-bearing
    dataclass was caller-constructible and serializable, so it could not prove
    independent provenance. This direct-launch capability is permanently
    retired; never provision it or connect it to a verifier. A later live stage
    must introduce a distinct pinned broker client and receipt chain. No instance
    can be created and every legacy production attestation fails closed.
    """

    __slots__ = ()

    def __new__(cls, *args: object, **kwargs: object) -> "ProductionVerificationContext":
        del args, kwargs
        raise RuntimeError(
            "production verifier capability is not provisioned; "
            "caller-supplied keys are never accepted"
        )

    def __repr__(self) -> str:
        return "ProductionVerificationContext(<unprovisioned>)"

    @property
    def key_id(self) -> str:
        return "unprovisioned"

    @property
    def expected_provider(self) -> str:
        return "unprovisioned"

    @property
    def expected_evidence_source(self) -> str:
        return "unprovisioned"

    @property
    def expected_verifier_identity(self) -> str:
        return "unprovisioned"

    def __copy__(self) -> "ProductionVerificationContext":
        raise TypeError("production verifier capability cannot be copied")

    def __deepcopy__(self, memo: object) -> "ProductionVerificationContext":
        del memo
        raise TypeError("production verifier capability cannot be deep-copied")

    def __reduce__(self) -> object:
        raise TypeError("production verifier capability cannot be serialized")

    def __reduce_ex__(self, protocol: int) -> object:
        del protocol
        raise TypeError("production verifier capability cannot be serialized")

    def verify(
        self,
        domain: str,
        payload: Mapping[str, Any],
        attestation: object,
    ) -> bool:
        del domain, payload, attestation
        return False


_BROKER_CONTEXT_FACTORY_TOKEN = object()


class BrokerVerificationContext:
    """Opaque current-service receipt-chain verification capability.

    This context never carries a verifier key or process handle. It can only ask
    the fixed broker client for a read-only reconciliation of one exact chain.
    """

    __slots__ = ("_client", "_chain_object", "_chain_digest")

    def __new__(
        cls,
        token: object = None,
        client: object = None,
        chain_object: object = None,
        chain_digest: str | None = None,
    ) -> "BrokerVerificationContext":
        if (
            token is not _BROKER_CONTEXT_FACTORY_TOKEN
            or client is None
            or chain_object is None
            or not isinstance(chain_digest, str)
        ):
            raise RuntimeError("broker verification context is not caller-constructible")
        instance = super().__new__(cls)
        instance._client = client
        instance._chain_object = chain_object
        instance._chain_digest = chain_digest
        return instance

    def verify_current_chain(self, chain: Mapping[str, Any]) -> bool:
        if not isinstance(chain, Mapping) or canonical_digest(dict(chain)) != self._chain_digest:
            return False
        method = getattr(self._client, "verify_current_chain", None)
        if not callable(method):
            return False
        try:
            return method(self._chain_object) is True
        except Exception:
            return False

    def __copy__(self) -> "BrokerVerificationContext":
        raise TypeError("broker verification context cannot be copied")

    def __deepcopy__(self, memo: object) -> "BrokerVerificationContext":
        del memo
        raise TypeError("broker verification context cannot be deep-copied")

    def __reduce__(self) -> object:
        raise TypeError("broker verification context cannot be serialized")


def _broker_verification_context_for_client(
    client: object,
    chain_object: object,
    chain: Mapping[str, Any],
) -> BrokerVerificationContext:
    return BrokerVerificationContext(
        _BROKER_CONTEXT_FACTORY_TOKEN,
        client,
        chain_object,
        canonical_digest(dict(chain)),
    )


@dataclass(frozen=True)
class ExternalIsolationReceipt:
    """Legacy pre-creation policy evidence; never an active child boundary."""

    schema_version: str
    provider: str
    evidence_source: str
    provider_production_eligible: bool
    evidence_source_production_eligible: bool
    independently_verified: bool
    isolation_id: str
    selected_executable_path: str
    selected_executable_sha256: str
    selected_executable_length_bytes: int
    packet_path: str
    packet_sha256: str
    packet_length_bytes: int
    workspace_path: str
    writable_directory_path: str
    reviewed_read_only_roots: tuple[str, ...]
    writable_temp_scopes: tuple[str, ...]
    tool_subprocess_network_denied: bool
    codex_control_plane_network_separately_scoped: bool
    codex_control_plane_network_scope: str
    writable_directory_exclusive: bool
    process_creation_controlled: bool
    launcher_process_start_limit: int
    tool_subprocess_start_limit: int
    credential_access_denied: bool
    user_profile_access_denied: bool
    observed_at: str
    expires_at: str
    attestation_algorithm: str
    attestation_key_id: str
    attestation_hmac_sha256: str
    digest: str


@dataclass(frozen=True)
class ChildEnvironment:
    """Credential-minimized, deterministic environment for one child process."""

    policy_id: str
    source_provenance: str
    safe_os_source_digest: str
    entries: tuple[tuple[str, str], ...] = field(repr=False)
    digest: str
    source_key_count: int
    retained_source_key_count: int
    dropped_source_key_count: int
    sensitive_source_key_count: int
    binding_key_count: int

    @property
    def keys(self) -> tuple[str, ...]:
        return tuple(key for key, _ in self.entries)

    def as_dict(self) -> dict[str, str]:
        return dict(self.entries)


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def with_self_digest(document: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(document)
    result.pop("digest", None)
    result["digest"] = canonical_digest(result)
    return result


def _external_isolation_attestation_payload(
    value: ExternalIsolationReceipt,
) -> dict[str, Any]:
    return {
        "schema_version": value.schema_version,
        "provider": value.provider,
        "evidence_source": value.evidence_source,
        "provider_production_eligible": value.provider_production_eligible,
        "evidence_source_production_eligible": value.evidence_source_production_eligible,
        "independently_verified": value.independently_verified,
        "isolation_id": value.isolation_id,
        "selected_executable_path": value.selected_executable_path,
        "selected_executable_sha256": value.selected_executable_sha256,
        "selected_executable_length_bytes": value.selected_executable_length_bytes,
        "packet_path": value.packet_path,
        "packet_sha256": value.packet_sha256,
        "packet_length_bytes": value.packet_length_bytes,
        "workspace_path": value.workspace_path,
        "writable_directory_path": value.writable_directory_path,
        "reviewed_read_only_roots": list(value.reviewed_read_only_roots),
        "writable_temp_scopes": list(value.writable_temp_scopes),
        "tool_subprocess_network_denied": value.tool_subprocess_network_denied,
        "codex_control_plane_network_separately_scoped": value.codex_control_plane_network_separately_scoped,
        "codex_control_plane_network_scope": value.codex_control_plane_network_scope,
        "writable_directory_exclusive": value.writable_directory_exclusive,
        "process_creation_controlled": value.process_creation_controlled,
        "launcher_process_start_limit": value.launcher_process_start_limit,
        "tool_subprocess_start_limit": value.tool_subprocess_start_limit,
        "credential_access_denied": value.credential_access_denied,
        "user_profile_access_denied": value.user_profile_access_denied,
        "observed_at": value.observed_at,
        "expires_at": value.expires_at,
        "attestation_algorithm": value.attestation_algorithm,
        "attestation_key_id": value.attestation_key_id,
    }


def _external_isolation_unsigned(value: ExternalIsolationReceipt) -> dict[str, Any]:
    result = _external_isolation_attestation_payload(value)
    result["attestation_hmac_sha256"] = value.attestation_hmac_sha256
    return result


def validate_external_isolation_receipt(
    value: object,
    *,
    preflight: Mapping[str, Any],
    packet_bytes: bytes,
    packet_path: Path,
    cwd: Path,
    additional_directory: Path,
    verification_context: ProductionVerificationContext | None,
    now: datetime | None = None,
) -> list[str]:
    """Validate the legacy pre-creation isolation shape; never live evidence."""

    if type(value) is not ExternalIsolationReceipt:
        return ["external isolation receipt must use the frozen typed contract"]
    errors: list[str] = []
    if type(verification_context) is not ProductionVerificationContext:
        errors.append(
            "production verification context must use the frozen out-of-band typed contract"
        )
    if value.schema_version != EXTERNAL_ISOLATION_SCHEMA_VERSION:
        errors.append(f"schema_version must be {EXTERNAL_ISOLATION_SCHEMA_VERSION}")
    if not isinstance(value.provider, str) or not value.provider.strip():
        errors.append("provider must be a non-empty string")
    if not isinstance(value.evidence_source, str) or not value.evidence_source.strip():
        errors.append("evidence_source must be a non-empty string")
    if value.provider == value.evidence_source:
        errors.append("evidence_source must be independent from provider")
    if type(verification_context) is ProductionVerificationContext:
        if value.provider != verification_context.expected_provider:
            errors.append("provider must match the out-of-band verification context")
        if value.evidence_source != verification_context.expected_evidence_source:
            errors.append(
                "evidence_source must match the out-of-band verification context"
            )
    for field_name in (
        "provider_production_eligible",
        "evidence_source_production_eligible",
        "independently_verified",
    ):
        if getattr(value, field_name) is not True:
            errors.append(f"{field_name} must be true")
    if not isinstance(value.isolation_id, str) or UUID_TEXT_RE.fullmatch(
        value.isolation_id
    ) is None:
        errors.append("isolation_id must be a canonical lowercase UUID")
    selected = preflight.get("selected_executable")
    if not isinstance(selected, dict):
        errors.append("preflight must provide a selected executable binding")
    else:
        for receipt_field, selected_field in (
            ("selected_executable_path", "path"),
            ("selected_executable_sha256", "sha256"),
            ("selected_executable_length_bytes", "length_bytes"),
        ):
            if getattr(value, receipt_field) != selected.get(selected_field):
                errors.append(
                    f"{receipt_field} must bind the exact selected executable"
                )
    if not isinstance(value.selected_executable_sha256, str) or re.fullmatch(
        r"[0-9a-f]{64}", value.selected_executable_sha256
    ) is None:
        errors.append("selected_executable_sha256 must be lowercase SHA-256")
    if (
        not isinstance(value.selected_executable_length_bytes, int)
        or isinstance(value.selected_executable_length_bytes, bool)
        or value.selected_executable_length_bytes <= 0
    ):
        errors.append("selected_executable_length_bytes must be positive")
    if type(packet_bytes) is not bytes or not packet_bytes:
        errors.append("packet_bytes must be non-empty exact immutable bytes")
    else:
        if value.packet_sha256 != hashlib.sha256(packet_bytes).hexdigest():
            errors.append("packet_sha256 must bind exact stdin packet bytes")
        if value.packet_length_bytes != len(packet_bytes):
            errors.append("packet_length_bytes must bind exact stdin packet bytes")
    if value.packet_path != str(packet_path):
        errors.append("packet_path must bind the exact packet file")
    if value.workspace_path != str(cwd):
        errors.append("workspace_path must bind the exact launch cwd")
    if value.writable_directory_path != str(additional_directory):
        errors.append("writable_directory_path must bind the exact additional directory")
    if value.reviewed_read_only_roots != (str(cwd),):
        errors.append("reviewed_read_only_roots must bind exactly the workspace root")
    if value.writable_temp_scopes != (str(additional_directory),):
        errors.append("writable_temp_scopes must contain exactly the additional directory")
    try:
        resolved_temp_root = Path(tempfile.gettempdir()).resolve(strict=True)
        resolved_writable = additional_directory.resolve(strict=True)
        resolved_packet = packet_path.resolve(strict=True)
        if not resolved_writable.is_relative_to(resolved_temp_root):
            errors.append("writable_directory_path must be inside the OS temporary root")
        if not resolved_packet.is_relative_to(resolved_writable):
            errors.append("packet_path must be inside the sole writable temp scope")
    except (OSError, RuntimeError, ValueError):
        errors.append("writable temp scope and packet path must exist for attestation")
    for field_name in (
        "tool_subprocess_network_denied",
        "codex_control_plane_network_separately_scoped",
        "writable_directory_exclusive",
        "process_creation_controlled",
        "credential_access_denied",
        "user_profile_access_denied",
    ):
        if getattr(value, field_name) is not True:
            errors.append(f"{field_name} must be true")
    if value.codex_control_plane_network_scope != CODEX_CONTROL_PLANE_NETWORK_SCOPE:
        errors.append(
            f"codex_control_plane_network_scope must be {CODEX_CONTROL_PLANE_NETWORK_SCOPE}"
        )
    for field_name in (
        "launcher_process_start_limit",
        "tool_subprocess_start_limit",
    ):
        field_value = getattr(value, field_name)
        if field_value != 1 or isinstance(field_value, bool):
            errors.append(f"{field_name} must be exactly one")
    parsed_times: dict[str, datetime] = {}
    for field_name in ("observed_at", "expires_at"):
        field_value = getattr(value, field_name)
        if not isinstance(field_value, str) or re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
            field_value,
        ) is None:
            errors.append(f"{field_name} must be canonical UTC seconds")
            continue
        try:
            parsed_times[field_name] = datetime.fromisoformat(
                field_value.replace("Z", "+00:00")
            )
        except ValueError:
            errors.append(f"{field_name} must be a valid timestamp")
    if len(parsed_times) == 2:
        observed_at = parsed_times["observed_at"]
        expires_at = parsed_times["expires_at"]
        current_time = now or datetime.now(timezone.utc).replace(microsecond=0)
        if current_time.tzinfo is None:
            errors.append("current validation time must be timezone-aware")
        else:
            current_time = current_time.astimezone(timezone.utc).replace(microsecond=0)
            if observed_at > current_time:
                errors.append("observed_at cannot be in the future")
            if expires_at <= current_time:
                errors.append("external isolation receipt is stale")
            if expires_at <= observed_at:
                errors.append("expires_at must follow observed_at")
            if (expires_at - observed_at).total_seconds() > EXTERNAL_ISOLATION_MAX_TTL_SECONDS:
                errors.append("external isolation receipt TTL exceeds the frozen maximum")
            if (current_time - observed_at).total_seconds() > EXTERNAL_ISOLATION_MAX_TTL_SECONDS:
                errors.append("external isolation observation is not fresh")
    if value.attestation_algorithm != ATTESTATION_ALGORITHM:
        errors.append(f"attestation_algorithm must be {ATTESTATION_ALGORITHM}")
    if type(verification_context) is ProductionVerificationContext:
        if value.attestation_key_id != verification_context.key_id:
            errors.append("attestation_key_id must match verification context")
        if not verification_context.verify(
            EXTERNAL_ISOLATION_ATTESTATION_DOMAIN,
            _external_isolation_attestation_payload(value),
            value.attestation_hmac_sha256,
        ):
            errors.append("attestation_hmac_sha256 failed authenticated verification")
    if value.digest != canonical_digest(_external_isolation_unsigned(value)):
        errors.append("digest must bind the exact external isolation receipt")
    return errors


def _normalized_environment_items(
    values: Mapping[str, str], *, context: str
) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for raw_key, raw_value in values.items():
        if not isinstance(raw_key, str) or not raw_key or "=" in raw_key or "\x00" in raw_key:
            raise ValueError(f"{context} contains an invalid environment key")
        if not isinstance(raw_value, str) or "\x00" in raw_value:
            raise ValueError(f"{context}[{raw_key}] must be a NUL-free string")
        key = raw_key.upper()
        if key in normalized:
            raise ValueError(f"{context} contains a case-insensitive duplicate key: {key}")
        normalized[key] = raw_value
    return normalized


def _build_child_environment_from_source(
    source: Mapping[str, str],
    *,
    bindings: Mapping[str, str] | None = None,
    source_provenance: str,
) -> ChildEnvironment:
    normalized_source = _normalized_environment_items(source, context="source")
    normalized_bindings = _normalized_environment_items(
        bindings or {}, context="bindings"
    )
    unknown_bindings = sorted(
        set(normalized_bindings) - ROLE_POOL_ENVIRONMENT_BINDING_KEYS
    )
    if unknown_bindings:
        raise ValueError(
            "bindings contain keys outside the frozen role-pool allowlist: "
            + ", ".join(unknown_bindings)
        )
    retained = {
        key: value
        for key, value in normalized_source.items()
        if key in SAFE_OS_ENVIRONMENT_KEYS
        and SENSITIVE_ENVIRONMENT_KEY_RE.search(key) is None
    }
    sensitive_count = sum(
        1
        for key in normalized_source
        if SENSITIVE_ENVIRONMENT_KEY_RE.search(key) is not None
    )
    collision = set(retained) & set(normalized_bindings)
    if collision:
        raise ValueError(
            "bindings collide with retained source keys: " + ", ".join(sorted(collision))
        )
    combined = {**retained, **normalized_bindings}
    entries = tuple(sorted(combined.items()))
    safe_os_source_digest = canonical_digest(
        {
            "source_provenance": source_provenance,
            "safe_os_values": retained,
        }
    )
    digest = canonical_digest(
        {
            "policy_id": CHILD_ENVIRONMENT_POLICY,
            "source_provenance": source_provenance,
            "safe_os_source_digest": safe_os_source_digest,
            "values": dict(entries),
        }
    )
    environment = ChildEnvironment(
        policy_id=CHILD_ENVIRONMENT_POLICY,
        source_provenance=source_provenance,
        safe_os_source_digest=safe_os_source_digest,
        entries=entries,
        digest=digest,
        source_key_count=len(normalized_source),
        retained_source_key_count=len(retained),
        dropped_source_key_count=len(normalized_source) - len(retained),
        sensitive_source_key_count=sensitive_count,
        binding_key_count=len(normalized_bindings),
    )
    validation_errors = validate_child_environment(environment)
    if validation_errors:
        raise ValueError("constructed child environment failed validation")
    return environment


def build_child_environment(
    *,
    packet_path: Path,
    packet_bytes: bytes,
    child_script_path: Path,
    child_script_bytes: bytes,
    attempt_series_id: str,
    sequence_index: int,
) -> ChildEnvironment:
    """Build exact broker-request environment inputs from this process only.

    OS values are captured from the launcher's ambient environment.  Every
    role-pool binding is derived here from exact bytes and typed inputs, so a
    caller cannot omit a binding group or substitute a caller-made
    digest or byte length.
    """

    if type(packet_bytes) is not bytes or not packet_bytes:
        raise ValueError("packet_bytes must be non-empty exact immutable bytes")
    if type(child_script_bytes) is not bytes or not child_script_bytes:
        raise ValueError("child_script_bytes must be non-empty exact immutable bytes")
    if not isinstance(packet_path, Path) or not packet_path.is_absolute():
        raise ValueError("packet_path must be an absolute Path")
    if not isinstance(child_script_path, Path) or not child_script_path.is_absolute():
        raise ValueError("child_script_path must be an absolute Path")
    if not isinstance(attempt_series_id, str) or UUID_TEXT_RE.fullmatch(
        attempt_series_id
    ) is None:
        raise ValueError("attempt_series_id must be a canonical lowercase UUID")
    if (
        not isinstance(sequence_index, int)
        or isinstance(sequence_index, bool)
        or sequence_index <= 0
    ):
        raise ValueError("sequence_index must be a positive integer")
    bindings = {
        "MYTHIC_EDGE_ROLE_POOL_PACKET_PATH": str(packet_path),
        "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256": hashlib.sha256(packet_bytes).hexdigest(),
        "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES": str(len(packet_bytes)),
        "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_PATH": str(child_script_path),
        "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_SHA256": hashlib.sha256(
            child_script_bytes
        ).hexdigest(),
        "MYTHIC_EDGE_ROLE_POOL_ATTEMPT_SERIES_ID": attempt_series_id,
        "MYTHIC_EDGE_ROLE_POOL_SEQUENCE_INDEX": str(sequence_index),
    }

    return _build_child_environment_from_source(
        os.environ,
        bindings=bindings,
        source_provenance=AMBIENT_ENVIRONMENT_PROVENANCE,
    )


def _build_child_environment_for_test(
    source: Mapping[str, str],
    *,
    bindings: Mapping[str, str] | None = None,
) -> ChildEnvironment:
    """Build an explicitly non-production environment for focused unit tests."""

    return _build_child_environment_from_source(
        source,
        bindings=bindings,
        source_provenance=_TEST_ENVIRONMENT_PROVENANCE,
    )


def validate_child_environment(
    value: object,
    *,
    require_ambient_provenance: bool = False,
) -> list[str]:
    """Validate even manually constructed environments before any process start."""

    errors: list[str] = []
    if type(value) is not ChildEnvironment:
        return ["child environment must use the frozen typed contract"]
    if value.policy_id != CHILD_ENVIRONMENT_POLICY:
        errors.append(f"policy_id must be {CHILD_ENVIRONMENT_POLICY}")
    if value.source_provenance not in {
        AMBIENT_ENVIRONMENT_PROVENANCE,
        _TEST_ENVIRONMENT_PROVENANCE,
    }:
        errors.append("source_provenance must identify a frozen environment source")
    if not isinstance(value.entries, tuple):
        errors.append("entries must be an immutable tuple")
        entries: tuple[tuple[str, str], ...] = ()
    else:
        entries = value.entries
    parsed_entries: list[tuple[str, str]] = []
    for index, entry in enumerate(entries):
        if (
            not isinstance(entry, tuple)
            or len(entry) != 2
            or not isinstance(entry[0], str)
            or not isinstance(entry[1], str)
        ):
            errors.append(f"entries[{index}] must be a string pair")
            continue
        key, item_value = entry
        if not key or key != key.upper() or "=" in key or "\x00" in key:
            errors.append(f"entries[{index}] key must be canonical uppercase")
        if "\x00" in item_value:
            errors.append(f"entries[{index}] value must be NUL-free")
        if key not in SAFE_OS_ENVIRONMENT_KEYS | ROLE_POOL_ENVIRONMENT_BINDING_KEYS:
            errors.append(f"entries[{index}] key is outside the frozen allowlist")
        if SENSITIVE_ENVIRONMENT_KEY_RE.search(key) is not None:
            errors.append(f"entries[{index}] key is credential-like")
        parsed_entries.append((key, item_value))
    if parsed_entries != sorted(parsed_entries) or len(
        {key for key, _ in parsed_entries}
    ) != len(parsed_entries):
        errors.append("entries must be sorted and case-insensitively unique")
    entry_map = dict(parsed_entries)
    safe_os_values = {
        key: item_value
        for key, item_value in parsed_entries
        if key in SAFE_OS_ENVIRONMENT_KEYS
    }
    expected_safe_os_source_digest = canonical_digest(
        {
            "source_provenance": value.source_provenance,
            "safe_os_values": safe_os_values,
        }
    )
    if value.safe_os_source_digest != expected_safe_os_source_digest:
        errors.append("safe_os_source_digest must bind retained safe OS values")
    for key in ROLE_POOL_SHA256_BINDING_KEYS & set(entry_map):
        if re.fullmatch(r"[0-9a-f]{64}", entry_map[key]) is None:
            errors.append(f"{key} must be lowercase SHA-256")
    for key in ROLE_POOL_POSITIVE_INTEGER_BINDING_KEYS & set(entry_map):
        text = entry_map[key]
        if not text.isdigit() or int(text) <= 0 or str(int(text)) != text:
            errors.append(f"{key} must be a canonical positive integer")
    for key in ROLE_POOL_PATH_BINDING_KEYS & set(entry_map):
        try:
            path = Path(entry_map[key])
            if not path.is_absolute():
                raise ValueError
        except (OSError, RuntimeError, ValueError):
            errors.append(f"{key} must be an absolute path")
    attempt_id = entry_map.get("MYTHIC_EDGE_ROLE_POOL_ATTEMPT_SERIES_ID")
    if attempt_id is not None and UUID_TEXT_RE.fullmatch(attempt_id) is None:
        errors.append("MYTHIC_EDGE_ROLE_POOL_ATTEMPT_SERIES_ID must be a lowercase UUID")
    for group in (
        {
            "MYTHIC_EDGE_ROLE_POOL_PACKET_PATH",
            "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256",
            "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES",
        },
        {
            "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_PATH",
            "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_SHA256",
        },
        {
            "MYTHIC_EDGE_ROLE_POOL_ATTEMPT_SERIES_ID",
            "MYTHIC_EDGE_ROLE_POOL_SEQUENCE_INDEX",
        },
    ):
        present = group & set(entry_map)
        if present and present != group:
            errors.append("role-pool environment binding groups must be complete")
    integer_fields = {
        "source_key_count": value.source_key_count,
        "retained_source_key_count": value.retained_source_key_count,
        "dropped_source_key_count": value.dropped_source_key_count,
        "sensitive_source_key_count": value.sensitive_source_key_count,
        "binding_key_count": value.binding_key_count,
    }
    counts_are_valid = True
    for field_name, field_value in integer_fields.items():
        if (
            not isinstance(field_value, int)
            or isinstance(field_value, bool)
            or field_value < 0
        ):
            errors.append(f"{field_name} must be a nonnegative integer")
            counts_are_valid = False
    os_entry_count = len(set(entry_map) & SAFE_OS_ENVIRONMENT_KEYS)
    binding_entry_count = len(set(entry_map) & ROLE_POOL_ENVIRONMENT_BINDING_KEYS)
    if value.retained_source_key_count != os_entry_count:
        errors.append("retained_source_key_count must equal retained OS entries")
    if value.binding_key_count != binding_entry_count:
        errors.append("binding_key_count must equal role-pool binding entries")
    if counts_are_valid:
        if value.source_key_count != (
            value.retained_source_key_count + value.dropped_source_key_count
        ):
            errors.append("source_key_count must equal retained plus dropped counts")
        if value.sensitive_source_key_count > value.dropped_source_key_count:
            errors.append("sensitive_source_key_count cannot exceed dropped count")
    expected_digest = canonical_digest(
        {
            "policy_id": value.policy_id,
            "source_provenance": value.source_provenance,
            "safe_os_source_digest": value.safe_os_source_digest,
            "values": entry_map,
        }
    )
    if value.digest != expected_digest:
        errors.append("digest must match the exact canonical environment")
    if require_ambient_provenance:
        if value.source_provenance != AMBIENT_ENVIRONMENT_PROVENANCE:
            errors.append("production launch requires ambient environment provenance")
        else:
            normalized_ambient = _normalized_environment_items(
                os.environ,
                context="ambient environment",
            )
            expected_ambient_values = {
                key: item_value
                for key, item_value in normalized_ambient.items()
                if key in SAFE_OS_ENVIRONMENT_KEYS
                and SENSITIVE_ENVIRONMENT_KEY_RE.search(key) is None
            }
            if safe_os_values != expected_ambient_values:
                errors.append(
                    "retained safe OS values must match the current ambient environment"
                )
            expected_ambient_digest = canonical_digest(
                {
                    "source_provenance": AMBIENT_ENVIRONMENT_PROVENANCE,
                    "safe_os_values": expected_ambient_values,
                }
            )
            if value.safe_os_source_digest != expected_ambient_digest:
                errors.append(
                    "safe_os_source_digest must bind the current ambient environment"
                )
            expected_sensitive_count = sum(
                1
                for key in normalized_ambient
                if SENSITIVE_ENVIRONMENT_KEY_RE.search(key) is not None
            )
            expected_counts = {
                "source_key_count": len(normalized_ambient),
                "retained_source_key_count": len(expected_ambient_values),
                "dropped_source_key_count": len(normalized_ambient)
                - len(expected_ambient_values),
                "sensitive_source_key_count": expected_sensitive_count,
            }
            for field_name, expected_value in expected_counts.items():
                if getattr(value, field_name) != expected_value:
                    errors.append(
                        f"{field_name} must bind the current ambient environment"
                    )
    return errors


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def default_codex_bin_root() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "OpenAI" / "Codex" / "bin"
    return Path.home() / "AppData" / "Local" / "OpenAI" / "Codex" / "bin"


def discover_codex_executables(bin_root: Path) -> list[Path]:
    """Return unique local codex.exe candidates contained by ``bin_root``."""

    try:
        resolved_root = bin_root.resolve(strict=True)
    except OSError:
        return []
    candidates: dict[str, Path] = {}
    for candidate in [resolved_root / "codex.exe", *resolved_root.rglob("codex.exe")]:
        try:
            resolved = candidate.resolve(strict=True)
            if not resolved.is_file() or not resolved.is_relative_to(resolved_root):
                continue
        except OSError:
            continue
        candidates[str(resolved).lower()] = resolved
    return sorted(candidates.values(), key=lambda item: str(item).lower())


def _run_local_command(args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=20,
        shell=False,
    )


def _parse_version(text: str) -> tuple[tuple[int, int, int, int, str], str] | None:
    match = VERSION_RE.search(text.strip())
    if not match:
        return None
    major, minor, patch = (int(match.group(index)) for index in range(1, 4))
    prerelease = match.group(4)
    version_text = f"codex-cli {major}.{minor}.{patch}"
    if prerelease:
        version_text += f"-{prerelease}"
    return (major, minor, patch, 1 if prerelease is None else 0, prerelease or ""), version_text


def _collect_model_slugs(value: object) -> set[str]:
    slugs: set[str] = set()
    if isinstance(value, dict):
        slug = value.get("slug")
        if isinstance(slug, str) and slug:
            slugs.add(slug)
        for child in value.values():
            slugs.update(_collect_model_slugs(child))
    elif isinstance(value, list):
        for child in value:
            slugs.update(_collect_model_slugs(child))
    return slugs


def _help_has_flag(help_text: str, flag: str) -> bool:
    return re.search(
        rf"(?<![0-9A-Za-z_-]){re.escape(flag)}(?![0-9A-Za-z_-])",
        help_text,
    ) is not None


def inspect_candidate(
    executable: Path,
    *,
    preferred_model: str = PREFERRED_MODEL,
    runner: CommandRunner = _run_local_command,
) -> dict[str, Any]:
    """Inspect one executable without invoking ``codex exec``."""

    observation: dict[str, Any] = {
        "path": str(executable),
        "sha256": _sha256_file(executable),
        "length_bytes": executable.stat().st_size,
        "cli_version": None,
        "version_key": None,
        "supported_exec_flags": [],
        "missing_exec_flags": list(REQUIRED_EXEC_FLAGS),
        "bundled_model_catalog_available": False,
        "preferred_model_available": False,
        "usable": False,
        "sanitized_error_code": "candidate_inspection_failed",
        "probe_command_kinds": [],
        "probe_process_count": 0,
    }
    def probe(kind: str, args: Sequence[str]) -> subprocess.CompletedProcess[str]:
        observation["probe_command_kinds"].append(kind)
        observation["probe_process_count"] += 1
        return runner(args)

    try:
        version_result = probe("version", [str(executable), "--version"])
        if version_result.returncode != 0:
            observation["sanitized_error_code"] = "version_command_failed"
            return observation
        parsed_version = _parse_version(version_result.stdout)
        if parsed_version is None:
            observation["sanitized_error_code"] = "version_output_invalid"
            return observation
        version_key, version_text = parsed_version
        observation["cli_version"] = version_text
        observation["version_key"] = list(version_key)

        help_result = probe("exec_help", [str(executable), "exec", "--help"])
        if help_result.returncode != 0:
            observation["sanitized_error_code"] = "exec_help_failed"
            return observation
        help_text = help_result.stdout + "\n" + help_result.stderr
        supported = [flag for flag in REQUIRED_EXEC_FLAGS if _help_has_flag(help_text, flag)]
        missing = [flag for flag in REQUIRED_EXEC_FLAGS if not _help_has_flag(help_text, flag)]
        observation["supported_exec_flags"] = supported
        observation["missing_exec_flags"] = missing
        if missing:
            observation["sanitized_error_code"] = "required_exec_flag_missing"
            return observation

        model_result = probe(
            "bundled_model_catalog",
            [str(executable), "debug", "models", "--bundled"],
        )
        if model_result.returncode == 0:
            try:
                catalog = json.loads(
                    model_result.stdout,
                    object_pairs_hook=_strict_object,
                )
                model_slugs = _collect_model_slugs(catalog)
                observation["bundled_model_catalog_available"] = True
                observation["preferred_model_available"] = preferred_model in model_slugs
            except (DuplicateKeyError, json.JSONDecodeError, TypeError):
                observation["bundled_model_catalog_available"] = False

        observation["usable"] = True
        observation["sanitized_error_code"] = "none"
        return observation
    except (OSError, subprocess.SubprocessError, ValueError):
        return observation


def resolve_launcher_preflight(
    bin_root: Path | None = None,
    *,
    preferred_model: str = PREFERRED_MODEL,
    preferred_reasoning_effort: str = PREFERRED_REASONING_EFFORT,
    runner: CommandRunner = _run_local_command,
    observed_at: str | None = None,
) -> dict[str, Any]:
    """Select the newest compatible CLI and bind the advisory model request."""

    root = (bin_root or default_codex_bin_root()).resolve()
    candidates = [
        inspect_candidate(path, preferred_model=preferred_model, runner=runner)
        for path in discover_codex_executables(root)
    ]
    usable = [candidate for candidate in candidates if candidate["usable"] is True]
    selected = max(
        usable,
        key=lambda candidate: (
            tuple(candidate["version_key"] or []),
            str(candidate["path"]).lower(),
        ),
        default=None,
    )
    if selected is None:
        status = "blocked"
        first_failed_stage = "launcher_resolution"
        error_code = "compatible_codex_executable_unavailable"
        selected_projection = None
        model_argument_enabled = False
        reasoning_effort_argument_enabled = False
        preference_status = "not_evaluated"
    else:
        status = "ready"
        first_failed_stage = "none"
        error_code = "none"
        selected_projection = {
            key: selected[key]
            for key in (
                "path",
                "sha256",
                "length_bytes",
                "cli_version",
                "supported_exec_flags",
                "bundled_model_catalog_available",
                "preferred_model_available",
            )
        }
        model_argument_enabled = selected["preferred_model_available"] is True
        reasoning_effort_argument_enabled = model_argument_enabled
        preference_status = (
            "available_and_will_request"
            if model_argument_enabled
            else "unavailable_use_platform_default"
        )
    document = {
        "schema_version": PREFLIGHT_SCHEMA_VERSION,
        "observed_at": observed_at or _utc_now_text(),
        "status": status,
        "first_failed_stage": first_failed_stage,
        "sanitized_error_code": error_code,
        "bin_root": str(root),
        "preferred_model": preferred_model,
        "preferred_reasoning_effort": preferred_reasoning_effort,
        "model_preference_advisory": True,
        "model_preference_status": preference_status,
        "model_argument_enabled": model_argument_enabled,
        "reasoning_effort_argument_enabled": reasoning_effort_argument_enabled,
        "required_exec_flags": list(REQUIRED_EXEC_FLAGS),
        "candidate_count": len(candidates),
        "selected_executable": selected_projection,
        "inspected_candidates": candidates,
        "network_access_authorized": False,
        "credential_access_authorized": False,
        "codex_exec_started": False,
        "probe_process_count": sum(
            int(candidate["probe_process_count"]) for candidate in candidates
        ),
        "codex_exec_process_start_count": 0,
    }
    return with_self_digest(document)


def validate_preflight(
    document: object,
    *,
    expected_preferred_model: str | None = None,
    expected_preferred_reasoning_effort: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["preflight must be an object"]
    required = {
        "schema_version",
        "observed_at",
        "status",
        "first_failed_stage",
        "sanitized_error_code",
        "bin_root",
        "preferred_model",
        "preferred_reasoning_effort",
        "model_preference_advisory",
        "model_preference_status",
        "model_argument_enabled",
        "reasoning_effort_argument_enabled",
        "required_exec_flags",
        "candidate_count",
        "selected_executable",
        "inspected_candidates",
        "network_access_authorized",
        "credential_access_authorized",
        "codex_exec_started",
        "probe_process_count",
        "codex_exec_process_start_count",
        "digest",
    }
    if set(document) != required:
        missing = sorted(required - set(document))
        unknown = sorted(set(document) - required)
        if missing:
            errors.append("missing fields: " + ", ".join(missing))
        if unknown:
            errors.append("unknown fields: " + ", ".join(unknown))
    if document.get("schema_version") != PREFLIGHT_SCHEMA_VERSION:
        errors.append(f"schema_version must be {PREFLIGHT_SCHEMA_VERSION}")
    preferred_model = document.get("preferred_model")
    preferred_effort = document.get("preferred_reasoning_effort")
    if not isinstance(preferred_model, str) or not preferred_model:
        errors.append("preferred_model must be a non-empty string")
    if not isinstance(preferred_effort, str) or not preferred_effort:
        errors.append("preferred_reasoning_effort must be a non-empty string")
    if (
        expected_preferred_model is not None
        and preferred_model != expected_preferred_model
    ):
        errors.append(
            f"preferred_model must match expected preference {expected_preferred_model}"
        )
    if (
        expected_preferred_reasoning_effort is not None
        and preferred_effort != expected_preferred_reasoning_effort
    ):
        errors.append(
            "preferred_reasoning_effort must match expected preference "
            f"{expected_preferred_reasoning_effort}"
        )
    if document.get("model_preference_advisory") is not True:
        errors.append("model_preference_advisory must be true")
    if document.get("network_access_authorized") is not False:
        errors.append("network_access_authorized must be false during preflight")
    if document.get("credential_access_authorized") is not False:
        errors.append("credential_access_authorized must be false during preflight")
    if document.get("codex_exec_process_start_count") != 0:
        errors.append("codex_exec_process_start_count must be zero during preflight")
    if document.get("codex_exec_started") is not False:
        errors.append("codex_exec_started must be false during preflight")
    if document.get("required_exec_flags") != list(REQUIRED_EXEC_FLAGS):
        errors.append("required_exec_flags must match the frozen launcher contract")
    for boolean_field in (
        "model_argument_enabled",
        "reasoning_effort_argument_enabled",
    ):
        if not isinstance(document.get(boolean_field), bool):
            errors.append(f"{boolean_field} must be boolean")
    inspected = document.get("inspected_candidates")
    if not isinstance(inspected, list):
        errors.append("inspected_candidates must be an array")
        inspected = []
    if document.get("candidate_count") != len(inspected):
        errors.append("candidate_count must equal inspected_candidates length")
    bin_root = document.get("bin_root")
    try:
        if not isinstance(bin_root, str) or not bin_root:
            raise ValueError
        root = Path(bin_root).resolve(strict=False)
    except (OSError, RuntimeError, ValueError):
        root = None
        errors.append("bin_root must be a resolvable path")
    candidate_paths: set[str] = set()
    for index, candidate in enumerate(inspected):
        context = f"inspected_candidates[{index}]"
        if not isinstance(candidate, dict):
            errors.append(f"{context} must be an object")
            continue
        if set(candidate) != CANDIDATE_FIELDS:
            errors.append(f"{context} fields must match the frozen candidate schema")
        candidate_path = candidate.get("path")
        try:
            resolved_path = Path(str(candidate_path)).resolve(strict=False)
            if root is not None and not resolved_path.is_relative_to(root):
                errors.append(f"{context}.path must be contained by bin_root")
            path_key = str(resolved_path).lower()
            if path_key in candidate_paths:
                errors.append(f"{context}.path must be unique")
            candidate_paths.add(path_key)
        except (OSError, RuntimeError, ValueError):
            errors.append(f"{context}.path must be resolvable")
        if not isinstance(candidate.get("sha256"), str) or not re.fullmatch(
            r"[0-9a-f]{64}", str(candidate.get("sha256"))
        ):
            errors.append(f"{context}.sha256 must be lowercase SHA-256")
        if not isinstance(candidate.get("length_bytes"), int) or isinstance(
            candidate.get("length_bytes"), bool
        ) or candidate.get("length_bytes", 0) < 0:
            errors.append(f"{context}.length_bytes must be a nonnegative integer")
        for boolean_field in (
            "bundled_model_catalog_available",
            "preferred_model_available",
            "usable",
        ):
            if not isinstance(candidate.get(boolean_field), bool):
                errors.append(f"{context}.{boolean_field} must be boolean")
        if (
            candidate.get("preferred_model_available") is True
            and candidate.get("bundled_model_catalog_available") is not True
        ):
            errors.append(
                f"{context}.preferred_model_available requires bundled catalog evidence"
            )
        if not isinstance(candidate.get("supported_exec_flags"), list) or not all(
            isinstance(flag, str) for flag in candidate.get("supported_exec_flags", [])
        ):
            errors.append(f"{context}.supported_exec_flags must be a string array")
        if not isinstance(candidate.get("missing_exec_flags"), list) or not all(
            isinstance(flag, str) for flag in candidate.get("missing_exec_flags", [])
        ):
            errors.append(f"{context}.missing_exec_flags must be a string array")
        if not isinstance(candidate.get("probe_command_kinds"), list) or not all(
            kind in {"version", "exec_help", "bundled_model_catalog"}
            for kind in candidate.get("probe_command_kinds", [])
        ):
            errors.append(f"{context}.probe_command_kinds must use known local probes")
        if candidate.get("probe_process_count") != len(
            candidate.get("probe_command_kinds", [])
        ):
            errors.append(f"{context}.probe_process_count must equal recorded probes")
        version_key = candidate.get("version_key")
        cli_version = candidate.get("cli_version")
        if candidate.get("usable") is True and (
            not isinstance(cli_version, str)
            or not isinstance(version_key, list)
            or len(version_key) != 5
            or not all(isinstance(item, int) for item in version_key[:4])
            or not isinstance(version_key[4], str)
        ):
            errors.append(f"{context} must contain a typed usable CLI version")
        if candidate.get("usable") is True:
            if candidate.get("missing_exec_flags") != []:
                errors.append(f"{context}.missing_exec_flags must be empty when usable")
            if candidate.get("supported_exec_flags") != list(REQUIRED_EXEC_FLAGS):
                errors.append(f"{context}.supported_exec_flags must match the contract")
            if candidate.get("sanitized_error_code") != "none":
                errors.append(f"{context}.sanitized_error_code must be none when usable")
            if candidate.get("probe_command_kinds") != [
                "version",
                "exec_help",
                "bundled_model_catalog",
            ]:
                errors.append(f"{context} usable candidate must complete all local probes")
    if document.get("probe_process_count") != sum(
        candidate.get("probe_process_count", 0)
        for candidate in inspected
        if isinstance(candidate, dict)
        and isinstance(candidate.get("probe_process_count"), int)
    ):
        errors.append("probe_process_count must equal inspected candidate probe counts")
    digest = document.get("digest")
    unsigned = dict(document)
    unsigned.pop("digest", None)
    if digest != canonical_digest(unsigned):
        errors.append("digest must match canonical preflight content")
    status = document.get("status")
    selected = document.get("selected_executable")
    if status == "ready":
        if not isinstance(selected, dict):
            errors.append("ready preflight requires selected_executable")
        else:
            if set(selected) != SELECTED_EXECUTABLE_FIELDS:
                errors.append(
                    "selected_executable fields must match the frozen selected schema"
                )
            matching = []
            for candidate in inspected:
                if not isinstance(candidate, dict) or candidate.get("usable") is not True:
                    continue
                projection = {
                    key: candidate.get(key) for key in SELECTED_EXECUTABLE_FIELDS
                }
                if projection == selected:
                    matching.append(candidate)
            if len(matching) != 1:
                errors.append(
                    "selected_executable must exactly project one usable inspected candidate"
                )
            if (
                selected.get("preferred_model_available") is True
                and selected.get("bundled_model_catalog_available") is not True
            ):
                errors.append(
                    "selected_executable preferred-model availability requires bundled catalog evidence"
                )
            usable_candidates = [
                candidate
                for candidate in inspected
                if isinstance(candidate, dict)
                and candidate.get("usable") is True
                and isinstance(candidate.get("version_key"), list)
            ]
            if usable_candidates:
                newest = max(
                    usable_candidates,
                    key=lambda candidate: (
                        tuple(candidate["version_key"]),
                        str(candidate.get("path", "")).lower(),
                    ),
                )
                newest_projection = {
                    key: newest.get(key) for key in SELECTED_EXECUTABLE_FIELDS
                }
                if selected != newest_projection:
                    errors.append("selected_executable must be the newest usable candidate")
        if document.get("first_failed_stage") != "none":
            errors.append("ready preflight first_failed_stage must be none")
        if document.get("sanitized_error_code") != "none":
            errors.append("ready preflight sanitized_error_code must be none")
    elif status == "blocked":
        if selected is not None:
            errors.append("blocked preflight must not select an executable")
        if document.get("model_argument_enabled") is not False:
            errors.append("blocked preflight cannot enable the model argument")
        if document.get("reasoning_effort_argument_enabled") is not False:
            errors.append("blocked preflight cannot enable the reasoning effort argument")
    else:
        errors.append("status must be ready or blocked")
    if document.get("model_argument_enabled") is True:
        if (
            not isinstance(selected, dict)
            or selected.get("preferred_model_available") is not True
            or selected.get("bundled_model_catalog_available") is not True
        ):
            errors.append("model argument requires observed preferred-model availability")
        if document.get("model_preference_status") != "available_and_will_request":
            errors.append("enabled model argument requires available_and_will_request status")
        if document.get("reasoning_effort_argument_enabled") is not True:
            errors.append("enabled model argument requires enabled reasoning effort argument")
    elif status == "ready":
        if not isinstance(selected, dict) or selected.get("preferred_model_available") is not False:
            errors.append("disabled model argument requires observed model unavailability")
        if document.get("model_preference_status") != "unavailable_use_platform_default":
            errors.append(
                "disabled model argument requires unavailable_use_platform_default status"
            )
        if document.get("reasoning_effort_argument_enabled") is not False:
            errors.append("platform-default fallback must omit reasoning effort argument")
    return errors


def build_codex_exec_args(
    preflight: Mapping[str, Any],
    *,
    cwd: Path,
    additional_directory: Path,
    output_schema_path: Path,
) -> list[str]:
    """Build the isolated stdin-driven command from a validated preflight."""

    errors = validate_preflight(dict(preflight))
    if errors or preflight.get("status") != "ready":
        raise ValueError("launcher preflight is not ready")
    selected = preflight["selected_executable"]
    if not isinstance(selected, dict) or not isinstance(selected.get("path"), str):
        raise ValueError("launcher preflight selected executable is invalid")
    args = [
        selected["path"],
        "exec",
        "--ephemeral",
        "--json",
        "--ignore-user-config",
        "--skip-git-repo-check",
    ]
    if preflight.get("model_argument_enabled") is True:
        args.extend(["--model", str(preflight["preferred_model"])])
    if preflight.get("reasoning_effort_argument_enabled") is True:
        args.extend(
            [
                "-c",
                f'model_reasoning_effort="{preflight["preferred_reasoning_effort"]}"',
            ]
        )
    args.extend(
        [
            "--sandbox",
            "read-only",
            "--cd",
            str(cwd),
            "--add-dir",
            str(additional_directory),
            "--output-schema",
            str(output_schema_path),
            "-",
        ]
    )
    return args


def _validate_broker_receipt(
    value: object,
    *,
    schema: str,
    fields: set[str],
    context: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"{context} must be an object"]
    if set(value) != fields:
        errors.append(f"{context} fields must match the exact broker schema")
    if value.get("schema_version") != schema:
        errors.append(f"{context}.schema_version must be {schema}")
    if value.get("attestation_domain") != BROKER_RECEIPT_DOMAINS[schema]:
        errors.append(f"{context}.attestation_domain is not pinned")
    unsigned = {key: item for key, item in value.items() if key != "digest"}
    if value.get("digest") != canonical_digest(unsigned):
        errors.append(f"{context}.digest must match canonical content")
    if value.get("attestation_algorithm") != ATTESTATION_ALGORITHM:
        errors.append(f"{context}.attestation_algorithm must be {ATTESTATION_ALGORITHM}")
    for field_name in ("attestation", "attestation_key_id"):
        if not isinstance(value.get(field_name), str) or not re.fullmatch(
            r"[0-9a-f]{64}", str(value.get(field_name))
        ):
            errors.append(f"{context}.{field_name} must be lowercase SHA-256")
    if value.get("verifier_identity") != (
        "mythic_edge_role_pool_windows_isolation_verifier_service.v1"
    ):
        errors.append(f"{context}.verifier_identity is not pinned")
    if value.get("evidence_source") != (
        "windows_kernel_appcontainer_job_acl_network_state.v1"
    ):
        errors.append(f"{context}.evidence_source is not pinned")
    return errors


def _broker_is_sha256(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _validate_broker_launch_request(request: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if set(request) != BROKER_LAUNCH_REQUEST_FIELDS:
        errors.append("broker launch request fields must match the exact schema")
    if request.get("schema_version") != BROKER_LAUNCH_REQUEST_SCHEMA_VERSION:
        errors.append("broker launch request schema is not recognized")
    unsigned = {key: item for key, item in request.items() if key != "digest"}
    if request.get("digest") != canonical_digest(unsigned):
        errors.append("broker launch request digest must match canonical content")
    if request.get("launcher_identity") != "codex:broker-single-start/v1":
        errors.append("broker launch request launcher identity is not pinned")
    if request.get("broker_identity") != (
        "mythic_edge_role_pool_windows_isolation_broker.v1"
    ):
        errors.append("broker launch request broker identity is not pinned")
    if request.get("verifier_identity") != (
        "mythic_edge_role_pool_windows_isolation_verifier_service.v1"
    ):
        errors.append("broker launch request verifier identity is not pinned")
    for field_name in (
        "current_request_digest",
        "authority_digest",
        "canary_exception_digest",
        "launcher_preflight_digest",
        "arguments_digest",
    ):
        if not _broker_is_sha256(request.get(field_name)):
            errors.append(f"broker launch request {field_name} is invalid")
    if type(request.get("sequence_index")) is not int or request.get(
        "sequence_index", 0
    ) <= 0:
        errors.append("broker launch request sequence_index is invalid")
    for field_name in ("nested_agent_allowed", "relaunch_allowed", "shell_mediation"):
        if request.get(field_name) is not False:
            errors.append(f"broker launch request {field_name} must be false")
    for field_name in ("packet_bytes_equal_stdin", "writable_cleanup_required"):
        if request.get(field_name) is not True:
            errors.append(f"broker launch request {field_name} must be true")
    if request.get("root_workload_count") != 1:
        errors.append("broker launch request root_workload_count must be one")
    descendant_count = request.get("allowed_tool_descendant_count")
    if type(descendant_count) is not int or not 0 <= descendant_count <= 63:
        errors.append("broker launch request descendant count is invalid")
    for field_name in ("executable", "packet", "output_schema", "child_script"):
        binding = request.get(field_name)
        if not isinstance(binding, dict) or set(binding) != BROKER_FILE_BINDING_FIELDS:
            errors.append(f"broker launch request {field_name} binding is invalid")
            continue
        if not isinstance(binding.get("path"), str) or not ntpath.isabs(
            binding["path"]
        ):
            errors.append(f"broker launch request {field_name} path is invalid")
        if not _broker_is_sha256(binding.get("sha256")):
            errors.append(f"broker launch request {field_name} digest is invalid")
        if type(binding.get("length_bytes")) is not int or binding.get(
            "length_bytes", -1
        ) < 0:
            errors.append(f"broker launch request {field_name} length is invalid")
    arguments = request.get("arguments")
    if not isinstance(arguments, list) or len(arguments) > 4096 or any(
        not isinstance(argument, str) or "\0" in argument
        for argument in arguments or []
    ):
        errors.append("broker launch request arguments are invalid")
    elif request.get("arguments_digest") != canonical_digest(arguments):
        errors.append("broker launch request arguments digest does not match")
    for field_name in (
        "working_directory",
        "allowed_namespace_root",
        "writable_temp_root",
    ):
        path = request.get(field_name)
        if not isinstance(path, str) or not ntpath.isabs(path):
            errors.append(f"broker launch request {field_name} is invalid")
    roots = request.get("read_only_roots")
    if (
        not isinstance(roots, list)
        or not roots
        or any(not isinstance(root, str) or not ntpath.isabs(root) for root in roots)
        or len(roots) != len({str(root).casefold() for root in roots})
    ):
        errors.append("broker launch request read_only_roots are invalid")
    denied = request.get("denied_repository_policy")
    if (
        not isinstance(denied, dict)
        or set(denied) != BROKER_POLICY_BINDING_FIELDS
        or not isinstance(denied.get("policy_id"), str)
        or not _broker_is_sha256(denied.get("digest"))
    ):
        errors.append("broker launch request denied repository policy is invalid")
    policies = request.get("policies")
    if not isinstance(policies, dict) or set(policies) != BROKER_POLICY_NAMES:
        errors.append("broker launch request policies are invalid")
    else:
        for name, policy in policies.items():
            if (
                not isinstance(policy, dict)
                or set(policy) != BROKER_POLICY_BINDING_FIELDS
                or not isinstance(policy.get("policy_id"), str)
                or not _broker_is_sha256(policy.get("digest"))
            ):
                errors.append(f"broker launch request {name} policy is invalid")
    environment = request.get("child_environment")
    if (
        not isinstance(environment, dict)
        or set(environment) != BROKER_CHILD_ENVIRONMENT_FIELDS
    ):
        errors.append("broker launch request child environment is invalid")
    else:
        keys = environment.get("keys")
        entries = environment.get("entries")
        keys_valid = isinstance(keys, list) and all(
            isinstance(key, str) for key in keys
        )
        if (
            environment.get("credential_like_values_present") is not False
            or environment.get("user_profile_access") is not False
            or not keys_valid
            or not isinstance(entries, dict)
            or (keys_valid and keys != sorted(keys))
            or (keys_valid and set(keys) != set(entries))
            or any(not isinstance(item, str) for item in entries.values())
            or environment.get("digest") != canonical_digest(entries)
        ):
            errors.append("broker launch request child environment binding is invalid")
    appcontainer_sid = request.get("appcontainer_sid")
    if not isinstance(appcontainer_sid, str) or not appcontainer_sid.startswith(
        "S-1-15-2-"
    ):
        errors.append("broker launch request AppContainer SID is invalid")
    if request.get("intended_use") != "stage4_evidence_only":
        errors.append("broker launch request intended use is invalid")
    return errors


def validate_broker_receipt_chain(value: object) -> list[str]:
    """Strict-validate broker lifecycle ordering and exact cross-bindings."""

    errors: list[str] = []
    if not isinstance(value, dict):
        return ["broker receipt chain must be an object"]
    if set(value) != BROKER_RECEIPT_CHAIN_FIELDS:
        errors.append("broker receipt chain fields must match the exact schema")
    if value.get("schema_version") != BROKER_RECEIPT_CHAIN_SCHEMA_VERSION:
        errors.append(
            f"broker receipt chain schema_version must be {BROKER_RECEIPT_CHAIN_SCHEMA_VERSION}"
        )
    request = value.get("launch_request")
    if not isinstance(request, dict):
        errors.append("broker launch request must be an object")
        return errors
    errors.extend(_validate_broker_launch_request(request))
    request_digest = request.get("digest")
    reservation = value.get("reservation_receipt")
    boundary = value.get("boundary_ready_receipt")
    start = value.get("start_receipt")
    terminal = value.get("terminal_receipt")
    abort = value.get("abort_receipt")
    errors.extend(
        _validate_broker_receipt(
            reservation,
            schema=BROKER_RESERVATION_SCHEMA_VERSION,
            fields=BROKER_RESERVATION_FIELDS,
            context="broker reservation receipt",
        )
    )
    if boundary is not None:
        errors.extend(
            _validate_broker_receipt(
                boundary,
                schema=BROKER_BOUNDARY_SCHEMA_VERSION,
                fields=BROKER_BOUNDARY_FIELDS,
                context="broker boundary-ready receipt",
            )
        )
    if start is not None:
        errors.extend(
            _validate_broker_receipt(
                start,
                schema=BROKER_START_SCHEMA_VERSION,
                fields=BROKER_START_FIELDS,
                context="broker start receipt",
            )
        )
    if terminal is not None:
        errors.extend(
            _validate_broker_receipt(
                terminal,
                schema=BROKER_TERMINAL_SCHEMA_VERSION,
                fields=BROKER_TERMINAL_FIELDS,
                context="broker terminal receipt",
            )
        )
    if abort is not None:
        errors.extend(
            _validate_broker_receipt(
                abort,
                schema=BROKER_ABORT_SCHEMA_VERSION,
                fields=BROKER_ABORT_FIELDS,
                context="broker abort receipt",
            )
        )
    if terminal is not None and abort is not None:
        errors.append("broker chain cannot contain both terminal and abort receipts")
    if terminal is None and abort is None and not isinstance(start, dict):
        errors.append(
            "broker chain without terminal or abort evidence requires a start receipt"
        )
    if isinstance(start, dict) and not isinstance(boundary, dict):
        errors.append("broker start receipt requires a boundary-ready receipt")
    documents = [
        ("reservation", reservation),
        ("boundary", boundary),
        ("start", start),
        ("terminal", terminal),
        ("abort", abort),
    ]
    launch_id = request.get("launch_id")
    for name, document in documents:
        if not isinstance(document, dict):
            continue
        if document.get("launch_id") != launch_id:
            errors.append(f"broker {name} receipt launch_id must bind the request")
        if document.get("launch_request_digest") != request_digest:
            errors.append(
                f"broker {name} receipt launch_request_digest must bind the request"
            )
    if isinstance(reservation, dict) and isinstance(boundary, dict):
        if boundary.get("start_reservation_digest") != reservation.get("digest"):
            errors.append("broker boundary receipt must bind the reservation")
    if isinstance(boundary, dict):
        broker_identity = boundary.get("broker_identity")
        if not isinstance(broker_identity, dict) or set(
            broker_identity
        ) != BROKER_IDENTITY_FIELDS:
            errors.append("broker boundary identity must match the exact schema")
        else:
            scm_pid = broker_identity.get("scm_process_id")
            if (
                broker_identity.get("provider_id")
                != "mythic_edge_role_pool_windows_isolation_broker.v1"
                or broker_identity.get("broker_epoch") != request.get("broker_epoch")
                or broker_identity.get("restricted_service_configuration") is not True
                or type(scm_pid) is not int
                or scm_pid <= 0
                or broker_identity.get("pipe_server_process_id") != scm_pid
                or type(broker_identity.get("process_creation_time_utc_ticks"))
                is not int
                or broker_identity.get("process_creation_time_utc_ticks", 0) <= 0
                or not isinstance(broker_identity.get("binary_path"), str)
                or not ntpath.isabs(broker_identity["binary_path"])
                or not _broker_is_sha256(broker_identity.get("binary_sha256"))
                or not _broker_is_sha256(broker_identity.get("signer_sha256"))
                or type(broker_identity.get("binary_length_bytes")) is not int
                or broker_identity.get("binary_length_bytes", 0) <= 0
                or not isinstance(broker_identity.get("service_sid"), str)
                or not isinstance(broker_identity.get("installation_id"), str)
            ):
                errors.append("broker boundary identity binding is invalid")
        observed = boundary.get("observed_boundary")
        if not isinstance(observed, dict) or set(
            observed
        ) != BROKER_OBSERVED_BOUNDARY_FIELDS:
            errors.append("broker boundary observation must match the exact schema")
        else:
            executable = request.get("executable", {})
            if (
                observed.get("executable_path") != executable.get("path")
                or observed.get("executable_sha256") != executable.get("sha256")
                or observed.get("executable_length_bytes")
                != executable.get("length_bytes")
                or observed.get("process_created_count") != 1
                or observed.get("process_resumed_count") != 0
            ):
                errors.append("broker boundary executable binding is invalid")
            for field_name in BROKER_OBSERVED_BOUNDARY_FIELDS - {
                "executable_path",
                "executable_sha256",
                "executable_length_bytes",
                "process_created_count",
                "process_resumed_count",
            }:
                if observed.get(field_name) is not True:
                    errors.append(f"broker boundary {field_name} must be true")
        process_identity = boundary.get("process_identity")
        if not isinstance(process_identity, str) or re.fullmatch(
            r"[1-9][0-9]*:[1-9][0-9]*", process_identity
        ) is None:
            errors.append("broker boundary process identity is invalid")
        if not _broker_is_sha256(boundary.get("bindings_digest")):
            errors.append("broker boundary bindings digest is invalid")
    if isinstance(reservation, dict) and isinstance(start, dict):
        if start.get("start_reservation_digest") != reservation.get("digest"):
            errors.append("broker start receipt must bind the reservation")
    if isinstance(boundary, dict) and isinstance(start, dict):
        if start.get("boundary_ready_receipt_digest") != boundary.get("digest"):
            errors.append("broker start receipt must bind the boundary-ready receipt")
        if start.get("process_identity") != boundary.get("process_identity"):
            errors.append("broker start receipt must bind the same process identity")
    if isinstance(start, dict):
        if start.get("process_created_count") != 1:
            errors.append("broker start receipt must report one created process")
        if start.get("process_resumed_count") != 1:
            errors.append("broker start receipt must report one resumed process")
        if start.get("relaunch_attempted") is not False:
            errors.append("broker start receipt must deny relaunch")
    if isinstance(terminal, dict):
        if not isinstance(start, dict):
            errors.append("broker terminal receipt requires a start receipt")
        elif terminal.get("start_receipt_digest") != start.get("digest"):
            errors.append("broker terminal receipt must bind the start receipt")
        if isinstance(boundary, dict) and terminal.get("process_identity") != boundary.get(
            "process_identity"
        ):
            errors.append("broker terminal receipt must bind the same process identity")
        for field_name in (
            "final_process_count",
            "remaining_tracked_process_count",
            "remaining_temporary_file_count",
        ):
            if terminal.get(field_name) != 0:
                errors.append(f"broker terminal {field_name} must be zero")
        if terminal.get("relaunch_attempted") is not False:
            errors.append("broker terminal receipt must deny relaunch")
    if isinstance(abort, dict):
        latest = (
            start.get("digest")
            if isinstance(start, dict)
            else boundary.get("digest")
            if isinstance(boundary, dict)
            else reservation.get("digest")
            if isinstance(reservation, dict)
            else None
        )
        if abort.get("latest_receipt_digest") != latest:
            errors.append("broker abort receipt must bind the latest valid receipt")
        if abort.get("zero_survivors_observed") is not True:
            errors.append("broker abort receipt must prove zero survivors")
        if abort.get("relaunch_attempted") is not False:
            errors.append("broker abort receipt must deny relaunch")
    return errors


def _require_opaque_broker_client(client: object) -> None:
    client_type = type(client)
    if (
        client_type.__name__ != "WindowsBrokerClient"
        or not client_type.__module__.endswith("windows_broker_client")
        or not callable(getattr(client, "start_once", None))
        or not callable(getattr(client, "verify_current_chain", None))
    ):
        raise TypeError("broker_client must be the pinned opaque Windows broker client")
    for forbidden in ("kill", "terminate", "retry", "launch"):
        if hasattr(client, forbidden):
            raise TypeError("broker_client exposes forbidden lifecycle authority")


def broker_launch_once(
    launch_request: Mapping[str, Any],
    *,
    broker_client: object,
) -> LaunchOutcome:
    """Use the opaque broker once; this function never creates a process."""

    _require_opaque_broker_client(broker_client)
    return _broker_launch_once_impl(launch_request, broker_client)


def _broker_launch_once_for_test(
    launch_request: Mapping[str, Any],
    *,
    broker_client: object,
) -> LaunchOutcome:
    """Private deterministic seam for the receipt-chain integration tests."""

    return _broker_launch_once_impl(launch_request, broker_client)


def _broker_launch_once_impl(
    launch_request: Mapping[str, Any],
    broker_client: object,
) -> LaunchOutcome:
    if not isinstance(launch_request, Mapping):
        raise TypeError("launch_request must be a mapping")
    request = dict(launch_request)
    if request.get("schema_version") != BROKER_LAUNCH_REQUEST_SCHEMA_VERSION:
        raise ValueError("broker launch request schema is not recognized")
    request_unsigned = {key: item for key, item in request.items() if key != "digest"}
    if request.get("digest") != canonical_digest(request_unsigned):
        raise ValueError("broker launch request digest is invalid")
    start_once_method = getattr(broker_client, "start_once", None)
    verify_method = getattr(broker_client, "verify_current_chain", None)
    if not callable(start_once_method) or not callable(verify_method):
        raise TypeError("broker_client does not implement the fixed broker protocol")
    chain_object = start_once_method(request)
    as_document = getattr(chain_object, "as_document", None)
    if callable(as_document):
        chain = as_document()
    elif isinstance(chain_object, Mapping):
        chain = dict(chain_object)
    else:
        raise TypeError("broker client returned an unsupported receipt-chain object")
    chain_errors = validate_broker_receipt_chain(chain)
    if chain_errors:
        raise RuntimeError("broker receipt chain failed validation: " + chain_errors[0])
    if verify_method(chain_object) is not True:
        raise RuntimeError("broker receipt chain failed current-service reconciliation")
    stdout_bytes = getattr(chain_object, "stdout_bytes", b"")
    stderr_bytes = getattr(chain_object, "stderr_bytes", b"")
    if type(stdout_bytes) is not bytes or type(stderr_bytes) is not bytes:
        raise TypeError("broker output channels must be immutable bytes")
    terminal = chain.get("terminal_receipt")
    abort = chain.get("abort_receipt")
    reservation = chain["reservation_receipt"]
    boundary = chain.get("boundary_ready_receipt")
    start = chain.get("start_receipt")
    executable = request.get("executable", {})
    packet = request.get("packet", {})
    environment = request.get("child_environment", {})
    environment_keys = environment.get("keys", []) if isinstance(environment, dict) else []
    binding_count = len(
        [
            key
            for key in environment_keys
            if isinstance(key, str) and key.startswith("MYTHIC_EDGE_ROLE_POOL_")
        ]
    )
    retained_count = len(environment_keys) - binding_count
    process_identity = (
        boundary.get("process_identity") if isinstance(boundary, dict) else None
    )
    pid: int | None = None
    if isinstance(process_identity, str):
        try:
            parsed_pid = int(process_identity.split(":", 1)[0])
        except (TypeError, ValueError):
            parsed_pid = 0
        if parsed_pid > 0:
            pid = parsed_pid
    status = (
        "complete"
        if isinstance(terminal, dict) and terminal.get("exit_code") == 0
        else "started"
        if terminal is None and abort is None and isinstance(start, dict)
        else "failed"
    )
    first_failed_stage = "none" if status in {"complete", "started"} else (
        abort.get("first_failed_stage") if isinstance(abort, dict) else "terminal"
    )
    error_code = "none" if status in {"complete", "started"} else (
        abort.get("sanitized_reason") if isinstance(abort, dict) else "broker_terminal_failure"
    )
    exact_arguments = [executable.get("path"), *request.get("arguments", [])]

    def broker_timestamp(value: object) -> object:
        if isinstance(value, str) and value.endswith(".000Z"):
            return value[:-5] + "Z"
        return value

    receipt = with_self_digest(
        {
            "schema_version": BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION,
            "status": status,
            "first_failed_stage": first_failed_stage,
            "sanitized_error_code": error_code,
            "preflight_digest": request.get("launcher_preflight_digest"),
            "exact_argument_array": exact_arguments,
            "executable_path": executable.get("path"),
            "executable_sha256": executable.get("sha256"),
            "executable_length_bytes": executable.get("length_bytes"),
            "payload_sha256": packet.get("sha256"),
            "payload_length_bytes": packet.get("length_bytes"),
            "environment_policy": CHILD_ENVIRONMENT_POLICY,
            "environment_source_provenance": AMBIENT_ENVIRONMENT_PROVENANCE,
            "environment_safe_os_source_digest": environment.get("digest"),
            "environment_digest": environment.get("digest"),
            "environment_keys": environment_keys,
            "environment_source_key_count": retained_count,
            "environment_retained_source_key_count": retained_count,
            "environment_dropped_source_key_count": 0,
            "environment_sensitive_source_key_count": 0,
            "environment_binding_key_count": binding_count,
            "launch_backend": PRODUCTION_LAUNCH_BACKEND,
            "production_eligible": True,
            "external_isolation_receipt_digest": None,
            "pid": pid,
            "process_start_count": (
                1
                if isinstance(start, dict)
                or isinstance(abort, dict)
                and abort.get("process_created_count") == 1
                else 0
            ),
            "started_at": (
                broker_timestamp(start.get("start_time"))
                if isinstance(start, dict)
                else None
            ),
            "completed_at": (
                broker_timestamp(terminal.get("completed_at"))
                if isinstance(terminal, dict)
                else broker_timestamp(abort.get("observed_at"))
                if isinstance(abort, dict)
                else None
            ),
            "exit_code": terminal.get("exit_code") if isinstance(terminal, dict) else None,
            "timed_out": terminal.get("timed_out") if isinstance(terminal, dict) else False,
            "stdout_sha256": hashlib.sha256(stdout_bytes).hexdigest(),
            "stdout_length_bytes": len(stdout_bytes),
            "stderr_sha256": hashlib.sha256(stderr_bytes).hexdigest(),
            "stderr_length_bytes": len(stderr_bytes),
            "relaunch_attempted": False,
            "stdout_content_included": False,
            "stderr_content_included": False,
            "single_start_guard_consumed_before_call": False,
            "single_start_guard_consume_attempted": True,
            "single_start_guard_consumed": True,
            "broker_receipt_chain": chain,
        }
    )
    context = _broker_verification_context_for_client(
        broker_client, chain_object, chain
    )
    return LaunchOutcome(
        receipt=receipt,
        stdout_bytes=stdout_bytes,
        stderr_bytes=stderr_bytes,
        broker_verification_context=context,
    )


def launch_once(
    preflight: Mapping[str, Any],
    args: Sequence[str],
    packet_bytes: bytes,
    *,
    cwd: Path,
    additional_directory: Path,
    output_schema_path: Path,
    environment: ChildEnvironment,
    attempt_guard: SingleStartGuard,
    external_isolation_receipt: ExternalIsolationReceipt | None = None,
    verification_context: ProductionVerificationContext | None = None,
    timeout_seconds: int = 300,
) -> LaunchOutcome:
    """Validate legacy inputs, then refuse the retired direct-Popen path.

    Tests use the explicitly private helper below. Broker contract v1 prohibits
    production or Stage-4 process creation here; the distinct broker client owns
    the production path and this retired direct path never creates a process.
    """

    environment_errors = validate_child_environment(
        environment,
        require_ambient_provenance=True,
    )
    if environment_errors:
        raise ValueError("child environment failed the frozen validation contract")
    environment_values = environment.as_dict()
    missing_launch_bindings = sorted(
        ROLE_POOL_ENVIRONMENT_BINDING_KEYS - set(environment_values)
    )
    if missing_launch_bindings:
        raise ValueError(
            "production binding set is incomplete: "
            + ", ".join(missing_launch_bindings)
        )
    packet_path = Path(environment_values["MYTHIC_EDGE_ROLE_POOL_PACKET_PATH"])
    isolation_errors = validate_external_isolation_receipt(
        external_isolation_receipt,
        preflight=preflight,
        packet_bytes=packet_bytes,
        packet_path=packet_path,
        cwd=cwd,
        additional_directory=additional_directory,
        verification_context=verification_context,
    )
    if isolation_errors:
        raise ValueError("external OS isolation evidence failed validation")
    raise RuntimeError(
        "direct Popen launcher is retired; "
        + BROKER_RECEIPT_CHAIN_UNAVAILABLE_ERROR
    )


def _launch_once_for_test(
    preflight: Mapping[str, Any],
    args: Sequence[str],
    packet_bytes: bytes,
    *,
    cwd: Path,
    additional_directory: Path,
    output_schema_path: Path,
    environment: ChildEnvironment,
    attempt_guard: SingleStartGuard,
    timeout_seconds: int = 300,
    popen_factory: Callable[..., Any],
    clock: Callable[[], str] = _utc_now_text,
) -> LaunchOutcome:
    """Internal-only deterministic seam for focused launcher unit tests."""

    return _launch_once_impl(
        preflight,
        args,
        packet_bytes,
        cwd=cwd,
        additional_directory=additional_directory,
        output_schema_path=output_schema_path,
        environment=environment,
        attempt_guard=attempt_guard,
        timeout_seconds=timeout_seconds,
        popen_factory=popen_factory,
        clock=clock,
        require_ambient_provenance=False,
        launch_backend=TEST_LAUNCH_BACKEND,
        production_eligible=False,
        external_isolation_receipt_digest=None,
    )


def _launch_once_impl(
    preflight: Mapping[str, Any],
    args: Sequence[str],
    packet_bytes: bytes,
    *,
    cwd: Path,
    additional_directory: Path,
    output_schema_path: Path,
    environment: ChildEnvironment,
    attempt_guard: SingleStartGuard,
    timeout_seconds: int,
    popen_factory: Callable[..., Any],
    clock: Callable[[], str],
    require_ambient_provenance: bool,
    launch_backend: str,
    production_eligible: bool,
    external_isolation_receipt_digest: str | None,
) -> LaunchOutcome:
    """Shared single-start implementation; never call outside this module."""

    environment_errors = validate_child_environment(
        environment,
        require_ambient_provenance=require_ambient_provenance,
    )
    if environment_errors:
        raise ValueError("child environment failed the frozen validation contract")
    if type(packet_bytes) is not bytes:
        raise TypeError("packet_bytes must be exact immutable bytes")
    if not isinstance(args, (list, tuple)) or not all(
        type(item) is str for item in args
    ):
        raise TypeError("args must be a sequence of strings")
    if type(attempt_guard) is not SingleStartGuard:
        raise TypeError("attempt_guard must use the frozen SingleStartGuard contract")
    if not isinstance(timeout_seconds, int) or isinstance(timeout_seconds, bool) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be a positive integer")
    environment_values = environment.as_dict()
    packet_sha_binding = environment_values.get(
        "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256"
    )
    packet_length_binding = environment_values.get(
        "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES"
    )
    missing_launch_bindings = sorted(
        ROLE_POOL_ENVIRONMENT_BINDING_KEYS - set(environment_values)
    )
    if require_ambient_provenance and missing_launch_bindings:
        raise ValueError(
            "production binding set is incomplete: "
            + ", ".join(missing_launch_bindings)
        )
    if packet_sha_binding is not None and packet_sha_binding != hashlib.sha256(
        packet_bytes
    ).hexdigest():
        raise ValueError("child environment packet SHA-256 binding does not match")
    if packet_length_binding is not None and int(packet_length_binding) != len(packet_bytes):
        raise ValueError("child environment packet length binding does not match")
    if require_ambient_provenance:
        packet_path = Path(
            environment_values["MYTHIC_EDGE_ROLE_POOL_PACKET_PATH"]
        )
        try:
            packet_file_bytes = packet_path.read_bytes()
        except (OSError, RuntimeError, ValueError) as error:
            raise ValueError("bound packet file is unavailable") from error
        if packet_file_bytes != packet_bytes:
            raise ValueError("bound packet file bytes do not match stdin packet bytes")
        child_script_path = Path(
            environment_values["MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_PATH"]
        )
        try:
            observed_child_script_sha256 = _sha256_file(child_script_path)
        except (OSError, RuntimeError, ValueError) as error:
            raise ValueError("bound child script is unavailable") from error
        if observed_child_script_sha256 != environment_values[
            "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_SHA256"
        ]:
            raise ValueError("child script SHA-256 binding does not match")

    validation_errors = validate_preflight(dict(preflight))
    process_start_count = 0
    started_at = clock()
    stdout_bytes = b""
    stderr_bytes = b""
    pid: int | None = None
    exit_code: int | None = None
    timed_out = False
    first_failed_stage = "none"
    error_code = "none"
    executable_path: str | None = None
    executable_sha256: str | None = None
    executable_length_bytes: int | None = None
    guard_consumed_before_call = attempt_guard.consumed
    guard_consume_attempted = False
    payload_sha256 = hashlib.sha256(packet_bytes).hexdigest()
    payload_length_bytes = len(packet_bytes)
    if validation_errors or preflight.get("status") != "ready":
        first_failed_stage = "launcher_preflight"
        error_code = "launcher_preflight_not_ready"
    else:
        selected = preflight.get("selected_executable")
        selected_path = selected.get("path") if isinstance(selected, dict) else None
        expected_args = build_codex_exec_args(
            preflight,
            cwd=cwd,
            additional_directory=additional_directory,
            output_schema_path=output_schema_path,
        )
        if list(args) != expected_args:
            first_failed_stage = "argument_binding"
            error_code = "exact_argument_array_mismatch"
        else:
            try:
                executable = Path(str(selected_path)).resolve(strict=True)
                observed_executable_path = str(executable)
                observed_executable_length = executable.stat().st_size
                observed_executable_sha256 = _sha256_file(executable)
                executable_path = observed_executable_path
                executable_length_bytes = observed_executable_length
                executable_sha256 = observed_executable_sha256
            except (OSError, RuntimeError, ValueError):
                executable_path = None
                executable_length_bytes = None
                executable_sha256 = None
                first_failed_stage = "executable_revalidation"
                error_code = "executable_unavailable"
            if error_code == "none" and (
                executable_path != selected_path
                or executable_length_bytes != selected.get("length_bytes")
                or executable_sha256 != selected.get("sha256")
            ):
                first_failed_stage = "executable_revalidation"
                error_code = "executable_binding_changed"
            if error_code == "none":
                guard_consume_attempted = True
                if not attempt_guard.consume():
                    first_failed_stage = "single_start_guard"
                    error_code = "process_start_already_attempted"
                else:
                    try:
                        process = popen_factory(
                            list(args),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=str(cwd),
                            env=environment_values,
                            shell=False,
                        )
                    except (OSError, subprocess.SubprocessError, TypeError, ValueError):
                        first_failed_stage = "process_start"
                        error_code = "process_start_failed"
                    else:
                        process_start_count = 1
                        try:
                            pid = int(process.pid)
                            if isinstance(process.pid, bool) or pid <= 0:
                                raise ValueError("invalid pid")
                            stdout_bytes, stderr_bytes = process.communicate(
                                input=packet_bytes,
                                timeout=timeout_seconds,
                            )
                            if not isinstance(stdout_bytes, bytes) or not isinstance(
                                stderr_bytes, bytes
                            ):
                                raise ValueError("child streams were not bytes")
                            if isinstance(process.returncode, bool) or not isinstance(
                                process.returncode, int
                            ):
                                raise ValueError("invalid return code")
                            exit_code = process.returncode
                            if exit_code != 0:
                                first_failed_stage = "child_process"
                                error_code = "child_exit_nonzero"
                        except subprocess.TimeoutExpired:
                            timed_out = True
                            first_failed_stage = "child_process"
                            error_code = "child_timeout"
                            try:
                                process.kill()
                                stdout_bytes, stderr_bytes = process.communicate()
                                if not isinstance(stdout_bytes, bytes) or not isinstance(
                                    stderr_bytes, bytes
                                ):
                                    raise ValueError("child streams were not bytes")
                                if isinstance(process.returncode, bool) or not isinstance(
                                    process.returncode, int
                                ):
                                    raise ValueError("invalid return code")
                                exit_code = process.returncode
                            except (
                                OSError,
                                subprocess.SubprocessError,
                                TypeError,
                                ValueError,
                                AttributeError,
                            ):
                                first_failed_stage = "child_process"
                                error_code = "child_cleanup_failed"
                        except (OSError, subprocess.SubprocessError):
                            first_failed_stage = "child_process"
                            error_code = "child_io_failed"
                            try:
                                process.kill()
                                cleanup_stdout, cleanup_stderr = process.communicate()
                                if isinstance(cleanup_stdout, bytes):
                                    stdout_bytes = cleanup_stdout
                                if isinstance(cleanup_stderr, bytes):
                                    stderr_bytes = cleanup_stderr
                                if isinstance(process.returncode, int) and not isinstance(
                                    process.returncode, bool
                                ):
                                    exit_code = process.returncode
                            except (
                                OSError,
                                subprocess.SubprocessError,
                                TypeError,
                                ValueError,
                                AttributeError,
                            ):
                                error_code = "child_cleanup_failed"
                        except (TypeError, ValueError, AttributeError):
                            first_failed_stage = "child_process"
                            error_code = "child_process_state_invalid"
                            try:
                                process.kill()
                                cleanup_stdout, cleanup_stderr = process.communicate()
                                if not isinstance(cleanup_stdout, bytes) or not isinstance(
                                    cleanup_stderr, bytes
                                ):
                                    raise ValueError("cleanup streams were not bytes")
                                stdout_bytes = cleanup_stdout
                                stderr_bytes = cleanup_stderr
                                if isinstance(process.returncode, int) and not isinstance(
                                    process.returncode, bool
                                ):
                                    exit_code = process.returncode
                            except (
                                OSError,
                                subprocess.SubprocessError,
                                TypeError,
                                ValueError,
                                AttributeError,
                            ):
                                error_code = "child_cleanup_failed"
    completed_at = clock()
    document = {
        "schema_version": LAUNCH_RECEIPT_SCHEMA_VERSION,
        "status": "complete" if error_code == "none" else "failed",
        "first_failed_stage": first_failed_stage,
        "sanitized_error_code": error_code,
        "preflight_digest": preflight.get("digest"),
        "exact_argument_array": list(args),
        "executable_path": executable_path,
        "executable_sha256": executable_sha256,
        "executable_length_bytes": executable_length_bytes,
        "payload_sha256": payload_sha256,
        "payload_length_bytes": payload_length_bytes,
        "environment_policy": environment.policy_id,
        "environment_source_provenance": environment.source_provenance,
        "environment_safe_os_source_digest": environment.safe_os_source_digest,
        "environment_digest": environment.digest,
        "environment_keys": list(environment.keys),
        "environment_source_key_count": environment.source_key_count,
        "environment_retained_source_key_count": environment.retained_source_key_count,
        "environment_dropped_source_key_count": environment.dropped_source_key_count,
        "environment_sensitive_source_key_count": environment.sensitive_source_key_count,
        "environment_binding_key_count": environment.binding_key_count,
        "launch_backend": launch_backend,
        "production_eligible": production_eligible,
        "external_isolation_receipt_digest": external_isolation_receipt_digest,
        "pid": pid,
        "process_start_count": process_start_count,
        "started_at": started_at,
        "completed_at": completed_at,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "stdout_sha256": hashlib.sha256(stdout_bytes).hexdigest(),
        "stdout_length_bytes": len(stdout_bytes),
        "stderr_sha256": hashlib.sha256(stderr_bytes).hexdigest(),
        "stderr_length_bytes": len(stderr_bytes),
        "relaunch_attempted": False,
        "stdout_content_included": False,
        "stderr_content_included": False,
        "single_start_guard_consumed_before_call": guard_consumed_before_call,
        "single_start_guard_consume_attempted": guard_consume_attempted,
        "single_start_guard_consumed": attempt_guard.consumed,
    }
    return LaunchOutcome(
        receipt=with_self_digest(document),
        stdout_bytes=stdout_bytes,
        stderr_bytes=stderr_bytes,
    )


def validate_launch_receipt(document: object) -> list[str]:
    """Validate direct/test v2 or broker-backed v3 content-free receipts."""

    errors: list[str] = []
    if not isinstance(document, dict):
        return ["launch receipt must be an object"]
    schema_version = document.get("schema_version")
    expected_fields = (
        BROKER_LAUNCH_RECEIPT_FIELDS
        if schema_version == BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION
        else LAUNCH_RECEIPT_FIELDS
    )
    if set(document) != expected_fields:
        errors.append("launch receipt fields must match the frozen receipt schema")
    if schema_version not in {
        LAUNCH_RECEIPT_SCHEMA_VERSION,
        BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION,
    }:
        errors.append(
            "schema_version must be a recognized direct/test or broker receipt schema"
        )
    unsigned = dict(document)
    digest = unsigned.pop("digest", None)
    if digest != canonical_digest(unsigned):
        errors.append("digest must match canonical launch receipt content")
    for field in (
        "preflight_digest",
        "payload_sha256",
        "environment_safe_os_source_digest",
        "environment_digest",
        "stdout_sha256",
        "stderr_sha256",
    ):
        if not isinstance(document.get(field), str) or not re.fullmatch(
            r"[0-9a-f]{64}", str(document.get(field))
        ):
            errors.append(f"{field} must be lowercase SHA-256")
    exact_args = document.get("exact_argument_array")
    if not isinstance(exact_args, list) or not all(
        isinstance(item, str) for item in exact_args
    ):
        errors.append("exact_argument_array must be a string array")
    if document.get("environment_policy") != CHILD_ENVIRONMENT_POLICY:
        errors.append(f"environment_policy must be {CHILD_ENVIRONMENT_POLICY}")
    if document.get("environment_source_provenance") not in {
        AMBIENT_ENVIRONMENT_PROVENANCE,
        _TEST_ENVIRONMENT_PROVENANCE,
    }:
        errors.append("environment_source_provenance is not recognized")
    launch_backend = document.get("launch_backend")
    production_eligible = document.get("production_eligible")
    isolation_digest = document.get("external_isolation_receipt_digest")
    if launch_backend == DIRECT_POPEN_LAUNCH_BACKEND:
        if production_eligible is not False:
            errors.append("direct Popen backend must be production ineligible")
        if isolation_digest is not None:
            errors.append("direct Popen backend cannot claim live isolation evidence")
    elif launch_backend == PRODUCTION_LAUNCH_BACKEND:
        if schema_version != BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION:
            errors.append(BROKER_RECEIPT_CHAIN_UNAVAILABLE_ERROR)
            errors.append("broker backend requires the broker launch receipt schema")
        if production_eligible is not True:
            errors.append("broker backend receipt must be production eligible")
        if isolation_digest is not None:
            errors.append("broker backend cannot reuse legacy isolation evidence")
        errors.extend(
            f"broker_receipt_chain: {error}"
            for error in validate_broker_receipt_chain(
                document.get("broker_receipt_chain")
            )
        )
    elif launch_backend == TEST_LAUNCH_BACKEND:
        if production_eligible is not False:
            errors.append("test backend receipt must be production ineligible")
        if isolation_digest is not None:
            errors.append("test backend cannot claim external isolation evidence")
    else:
        errors.append("launch_backend is not recognized")
    environment_keys = document.get("environment_keys")
    if (
        not isinstance(environment_keys, list)
        or not all(isinstance(item, str) for item in environment_keys)
        or environment_keys != sorted(set(environment_keys))
    ):
        errors.append("environment_keys must be a sorted unique string array")
    for field in (
        "payload_length_bytes",
        "environment_source_key_count",
        "environment_retained_source_key_count",
        "environment_dropped_source_key_count",
        "environment_sensitive_source_key_count",
        "environment_binding_key_count",
        "stdout_length_bytes",
        "stderr_length_bytes",
    ):
        value = document.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{field} must be a nonnegative integer")
    source_count = document.get("environment_source_key_count")
    retained_count = document.get("environment_retained_source_key_count")
    dropped_count = document.get("environment_dropped_source_key_count")
    binding_count = document.get("environment_binding_key_count")
    if all(
        isinstance(item, int) and not isinstance(item, bool)
        for item in (source_count, retained_count, dropped_count, binding_count)
    ):
        if source_count != retained_count + dropped_count:
            errors.append("environment source count must equal retained plus dropped")
        if isinstance(environment_keys, list) and len(environment_keys) != (
            retained_count + binding_count
        ):
            errors.append("environment_keys length must equal retained plus binding counts")
    if document.get("process_start_count") not in {0, 1} or isinstance(
        document.get("process_start_count"), bool
    ):
        errors.append("process_start_count must be zero or one")
    for field in (
        "timed_out",
        "relaunch_attempted",
        "stdout_content_included",
        "stderr_content_included",
        "single_start_guard_consumed_before_call",
        "single_start_guard_consume_attempted",
        "single_start_guard_consumed",
    ):
        if not isinstance(document.get(field), bool):
            errors.append(f"{field} must be boolean")
    if document.get("relaunch_attempted") is not False:
        errors.append("relaunch_attempted must be false")
    if document.get("stdout_content_included") is not False:
        errors.append("stdout_content_included must be false")
    if document.get("stderr_content_included") is not False:
        errors.append("stderr_content_included must be false")
    timestamp_values: dict[str, datetime] = {}
    for field_name in ("started_at", "completed_at"):
        value = document.get(field_name)
        if (
            field_name == "completed_at"
            and document.get("schema_version") == BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION
            and document.get("status") == "started"
            and value is None
        ):
            continue
        if (
            field_name == "started_at"
            and document.get("schema_version") == BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION
            and document.get("status") == "failed"
            and value is None
            and isinstance(document.get("broker_receipt_chain"), dict)
            and document["broker_receipt_chain"].get("start_receipt") is None
        ):
            continue
        if not isinstance(value, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value
        ):
            errors.append(f"{field_name} must be canonical UTC seconds")
            continue
        try:
            timestamp_values[field_name] = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError:
            errors.append(f"{field_name} must be a valid timestamp")
    if (
        "started_at" in timestamp_values
        and "completed_at" in timestamp_values
        and timestamp_values["completed_at"] < timestamp_values["started_at"]
    ):
        errors.append("completed_at must not precede started_at")

    executable_fields = (
        document.get("executable_path"),
        document.get("executable_sha256"),
        document.get("executable_length_bytes"),
    )
    executable_bound = all(item is not None for item in executable_fields)
    if any(item is not None for item in executable_fields) and not executable_bound:
        errors.append("executable binding fields must be all null or all present")
    if executable_bound:
        if not isinstance(document.get("executable_path"), str) or not document.get(
            "executable_path"
        ):
            errors.append("executable_path must be a non-empty string")
        if not isinstance(document.get("executable_sha256"), str) or not re.fullmatch(
            r"[0-9a-f]{64}", str(document.get("executable_sha256"))
        ):
            errors.append("executable_sha256 must be lowercase SHA-256")
        if not isinstance(document.get("executable_length_bytes"), int) or isinstance(
            document.get("executable_length_bytes"), bool
        ) or document.get("executable_length_bytes", -1) < 0:
            errors.append("executable_length_bytes must be a nonnegative integer")

    started = document.get("process_start_count") == 1
    if started:
        if document.get("sanitized_error_code") not in {
            "child_process_state_invalid",
            "child_cleanup_failed",
        } and (
            not isinstance(document.get("pid"), int)
            or isinstance(document.get("pid"), bool)
            or document.get("pid", 0) <= 0
        ):
            errors.append("a started process requires a positive integer pid")
        if not executable_bound:
            errors.append("a started process requires an executable binding")
    elif document.get("pid") is not None or document.get("exit_code") is not None:
        errors.append("an unstarted process cannot report pid or exit_code")
    exit_code = document.get("exit_code")
    if exit_code is not None and (
        not isinstance(exit_code, int) or isinstance(exit_code, bool)
    ):
        errors.append("exit_code must be an integer or null")

    error_pairs = {
        "none": "none",
        "launcher_preflight_not_ready": "launcher_preflight",
        "exact_argument_array_mismatch": "argument_binding",
        "executable_unavailable": "executable_revalidation",
        "executable_binding_changed": "executable_revalidation",
        "process_start_already_attempted": "single_start_guard",
        "process_start_failed": "process_start",
        "child_exit_nonzero": "child_process",
        "child_timeout": "child_process",
        "child_io_failed": "child_process",
        "child_cleanup_failed": "child_process",
        "child_process_state_invalid": "child_process",
    }
    error_code = document.get("sanitized_error_code")
    first_failed_stage = document.get("first_failed_stage")
    broker_abort = (
        document.get("broker_receipt_chain", {}).get("abort_receipt")
        if document.get("schema_version") == BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION
        and isinstance(document.get("broker_receipt_chain"), dict)
        else None
    )
    if isinstance(broker_abort, dict) and document.get("status") == "failed":
        if error_code != broker_abort.get("sanitized_reason"):
            errors.append("sanitized_error_code must match the broker abort receipt")
        if first_failed_stage != broker_abort.get("first_failed_stage"):
            errors.append("first_failed_stage must match the broker abort receipt")
        if not isinstance(error_code, str) or re.fullmatch(
            r"[a-z][a-z0-9_]{0,127}", error_code
        ) is None:
            errors.append("broker sanitized_error_code must be symbolic lowercase text")
    elif error_code not in error_pairs:
        errors.append("sanitized_error_code is not recognized")
    elif first_failed_stage != error_pairs[error_code]:
        errors.append("first_failed_stage must match sanitized_error_code")

    guard_before = document.get("single_start_guard_consumed_before_call")
    guard_attempted = document.get("single_start_guard_consume_attempted")
    guard_after = document.get("single_start_guard_consumed")
    if guard_before is True and guard_after is not True:
        errors.append("a consumed guard cannot become unconsumed")
    if guard_attempted is True and guard_after is not True:
        errors.append("a guard consume attempt must leave the guard consumed")
    if started and not (guard_before is False and guard_attempted is True and guard_after is True):
        errors.append("a started process requires this call to consume a fresh guard")
    if error_code == "process_start_already_attempted" and not (
        guard_before is True and guard_attempted is True and guard_after is True
    ):
        errors.append("guard-blocked receipt requires a previously consumed guard")
    if error_code == "process_start_failed" and not (
        guard_before is False and guard_attempted is True and guard_after is True
    ):
        errors.append("process-start failure requires this call to consume the guard")
    if error_code in {
        "launcher_preflight_not_ready",
        "exact_argument_array_mismatch",
        "executable_unavailable",
        "executable_binding_changed",
    } and guard_attempted is not False:
        errors.append("pre-start validation failure cannot attempt guard consumption")
    if error_code in {
        "launcher_preflight_not_ready",
        "exact_argument_array_mismatch",
        "executable_unavailable",
    } and executable_bound:
        errors.append("this pre-start failure cannot claim an executable binding")
    if error_code in {
        "process_start_already_attempted",
        "process_start_failed",
        "none",
        "child_exit_nonzero",
        "child_timeout",
        "child_io_failed",
        "child_cleanup_failed",
        "child_process_state_invalid",
    } and not executable_bound:
        errors.append("this launch stage requires a revalidated executable binding")
    if error_code in {
        "none",
        "child_exit_nonzero",
        "child_timeout",
        "child_io_failed",
        "child_cleanup_failed",
        "child_process_state_invalid",
    } and not started:
        errors.append("child-process outcome requires exactly one process start")
    if document.get("timed_out") is True and error_code not in {
        "child_timeout",
        "child_cleanup_failed",
    }:
        errors.append("timed_out may only accompany timeout or timeout cleanup failure")
    if error_code == "child_timeout" and document.get("timed_out") is not True:
        errors.append("child_timeout requires timed_out true")
    if error_code == "child_exit_nonzero" and (
        not isinstance(exit_code, int)
        or isinstance(exit_code, bool)
        or exit_code == 0
    ):
        errors.append("child_exit_nonzero requires a nonzero integer exit_code")
    if error_code == "none" and exit_code != 0 and not (
        document.get("schema_version") == BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION
        and document.get("status") == "started"
        and exit_code is None
    ):
        errors.append("a successful child requires exit_code zero")
    if error_code in {
        "launcher_preflight_not_ready",
        "exact_argument_array_mismatch",
        "executable_unavailable",
        "executable_binding_changed",
        "process_start_already_attempted",
        "process_start_failed",
    } and exit_code is not None:
        errors.append("a pre-start outcome cannot report an exit_code")
    if document.get("status") == "complete":
        if document.get("first_failed_stage") != "none":
            errors.append("complete receipt first_failed_stage must be none")
        if document.get("sanitized_error_code") != "none":
            errors.append("complete receipt sanitized_error_code must be none")
        if not started or document.get("exit_code") != 0 or document.get("timed_out") is not False:
            errors.append("complete receipt requires one successful non-timeout process")
    elif (
        document.get("schema_version") == BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION
        and document.get("status") == "started"
    ):
        if document.get("first_failed_stage") != "none":
            errors.append("started receipt first_failed_stage must be none")
        if document.get("sanitized_error_code") != "none":
            errors.append("started receipt sanitized_error_code must be none")
        if (
            not started
            or document.get("exit_code") is not None
            or document.get("completed_at") is not None
            or document.get("timed_out") is not False
        ):
            errors.append(
                "started receipt requires one started, nonterminal, non-timeout process"
            )
    elif document.get("status") == "failed":
        if document.get("first_failed_stage") == "none":
            errors.append("failed receipt must identify first_failed_stage")
        if document.get("sanitized_error_code") == "none":
            errors.append("failed receipt must identify sanitized_error_code")
    else:
        errors.append("status must be complete, failed, or broker-v3 started")
    return errors


def validate_launch_receipt_against_context(
    document: object,
    *,
    preflight: Mapping[str, Any],
    cwd: Path,
    additional_directory: Path,
    output_schema_path: Path,
    packet_bytes: bytes,
    child_environment: ChildEnvironment,
    external_isolation_receipt: ExternalIsolationReceipt | None = None,
    verification_context: ProductionVerificationContext | None = None,
    broker_verification_context: BrokerVerificationContext | None = None,
    stdout_bytes: bytes | None = None,
    stderr_bytes: bytes | None = None,
) -> list[str]:
    """Bind a receipt to the exact preflight, command, payload, and environment."""

    errors = validate_launch_receipt(document)
    if not isinstance(document, dict):
        return errors
    preflight_errors = validate_preflight(dict(preflight))
    errors.extend(f"preflight: {error}" for error in preflight_errors)
    if document.get("preflight_digest") != preflight.get("digest"):
        errors.append("preflight_digest must bind the exact launcher preflight")
    try:
        derived_args = build_codex_exec_args(
            preflight,
            cwd=cwd,
            additional_directory=additional_directory,
            output_schema_path=output_schema_path,
        )
    except (TypeError, ValueError):
        errors.append("exact command could not be derived from launcher preflight")
    else:
        if document.get("exact_argument_array") != derived_args:
            errors.append("exact_argument_array must match the independently derived command")
    if not isinstance(packet_bytes, bytes):
        errors.append("packet_bytes must be exact immutable bytes")
    else:
        if document.get("payload_sha256") != hashlib.sha256(packet_bytes).hexdigest():
            errors.append("payload_sha256 must bind the exact packet bytes")
        if document.get("payload_length_bytes") != len(packet_bytes):
            errors.append("payload_length_bytes must bind the exact packet bytes")
    child_environment_errors = validate_child_environment(child_environment)
    errors.extend(
        f"child_environment: {error}" for error in child_environment_errors
    )
    if isinstance(child_environment, ChildEnvironment) and not child_environment_errors:
        environment_bindings = {
            "environment_policy": child_environment.policy_id,
            "environment_source_provenance": child_environment.source_provenance,
            "environment_safe_os_source_digest": child_environment.safe_os_source_digest,
            "environment_digest": child_environment.digest,
            "environment_keys": list(child_environment.keys),
            "environment_source_key_count": child_environment.source_key_count,
            "environment_retained_source_key_count": child_environment.retained_source_key_count,
            "environment_dropped_source_key_count": child_environment.dropped_source_key_count,
            "environment_sensitive_source_key_count": child_environment.sensitive_source_key_count,
            "environment_binding_key_count": child_environment.binding_key_count,
        }
        for field_name, expected_value in environment_bindings.items():
            if document.get(field_name) != expected_value:
                errors.append(f"{field_name} must bind the exact child environment")
        if isinstance(packet_bytes, bytes):
            environment_values = child_environment.as_dict()
            missing_launch_bindings = sorted(
                ROLE_POOL_ENVIRONMENT_BINDING_KEYS - set(environment_values)
            )
            if missing_launch_bindings:
                errors.append("child environment must contain every production binding")
            packet_sha_binding = environment_values.get(
                "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256"
            )
            packet_length_binding = environment_values.get(
                "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES"
            )
            if packet_sha_binding != hashlib.sha256(
                packet_bytes
            ).hexdigest():
                errors.append("child environment packet SHA-256 must bind packet bytes")
            if packet_length_binding is None or int(packet_length_binding) != len(packet_bytes):
                errors.append("child environment packet length must bind packet bytes")
    launch_backend = document.get("launch_backend")
    if launch_backend == PRODUCTION_LAUNCH_BACKEND:
        if external_isolation_receipt is not None:
            errors.append("broker backend cannot include legacy isolation evidence")
        if type(broker_verification_context) is not BrokerVerificationContext:
            errors.append("broker backend requires an opaque verification context")
        elif not broker_verification_context.verify_current_chain(
            document.get("broker_receipt_chain", {})
        ):
            errors.append("broker receipt chain failed current-service reconciliation")
    elif launch_backend in {DIRECT_POPEN_LAUNCH_BACKEND, TEST_LAUNCH_BACKEND}:
        if external_isolation_receipt is not None:
            errors.append("direct/test backend context cannot include live isolation evidence")
    selected = preflight.get("selected_executable")
    error_code = document.get("sanitized_error_code")
    if isinstance(selected, dict) and error_code not in {
        "launcher_preflight_not_ready",
        "exact_argument_array_mismatch",
        "executable_unavailable",
        "executable_binding_changed",
    }:
        for receipt_field, selected_field in (
            ("executable_path", "path"),
            ("executable_sha256", "sha256"),
            ("executable_length_bytes", "length_bytes"),
        ):
            if document.get(receipt_field) != selected.get(selected_field):
                errors.append(
                    f"{receipt_field} must bind the selected launcher executable"
                )
    for stream_name, stream_bytes in (
        ("stdout", stdout_bytes),
        ("stderr", stderr_bytes),
    ):
        if stream_bytes is None:
            continue
        if not isinstance(stream_bytes, bytes):
            errors.append(f"{stream_name}_bytes must be bytes when supplied")
            continue
        if document.get(f"{stream_name}_sha256") != hashlib.sha256(
            stream_bytes
        ).hexdigest():
            errors.append(f"{stream_name}_sha256 must bind returned bytes")
        if document.get(f"{stream_name}_length_bytes") != len(stream_bytes):
            errors.append(f"{stream_name}_length_bytes must bind returned bytes")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect local Codex launcher capability without network access, "
            "credential access, or codex exec."
        )
    )
    parser.add_argument("--bin-root", type=Path, default=default_codex_bin_root())
    args = parser.parse_args(argv)
    document = resolve_launcher_preflight(args.bin_root)
    print(canonical_bytes(document).decode("ascii"))
    return 0 if document["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
