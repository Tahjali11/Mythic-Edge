"""Run the single-use R0 direct-interpreter preflight.

The module deliberately exposes one fixed operation.  Its pure selectors and
projector are testable without creating a process; the production adapter uses
Win32 APIs directly and is selected only when no adapter is injected.
"""

from __future__ import annotations

import ctypes
import hashlib
import importlib.util
import itertools
import json
import os
import stat
import sys
import time
from collections.abc import Mapping, Sequence
from ctypes import wintypes
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import BinaryIO, Protocol, TextIO, cast

REPOSITORY_ID = 1235264383
ISSUE_NUMBER = 780
RESULT_SCHEMA = "trusted_owner_r0_direct_interpreter_preflight_result.v1"
EXECUTOR_CONTRACT_SHA256 = (
    "cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4"
)
EXECUTOR_CONTRACT_REVIEW_SHA256 = (
    "8fa95ada34171e0e040acea13de52a87d72138995bbcc8b6dc982fb0ecca3880"
)
EXECUTOR_LOCAL_EFFECT_REVIEW_SHA256 = (
    "5977226c70449601e09d04328a9a0522cefcb15dbaea13aead494bfb64fa753a"
)
EXECUTOR_PREDECESSOR_REVIEW_SHA256 = (
    "97adebc7fc8033125ac19dddb861361c7b4d40babdee338ca73b239394fa8038"
)
EXECUTOR_IMPLEMENTATION_REVIEW_SHA256 = (
    "49d66f9ce38f0fab01bbeebf02deba4451f87f45600a21552b47a3e9292e0dac"
)
EXECUTOR_TEST_SHA256 = (
    "435aedabf5d73e02df1cede397f937da6c44b2cecd4ee3ae21b0645bf44e490b"
)
PARENT_CONTRACT_SHA256 = (
    "17d0d2f5fe965643888ea70c71a278afdb7797033c311252bce1dde56486ea84"
)
PARENT_REVIEW_SHA256 = (
    "0fd7d921a92fbd58576f053a0e8938d3ae4a0266e9a023b762f933e65aee450f"
)
HARNESS_SHA256 = (
    "001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6"
)
HARNESS_TEST_SHA256 = (
    "3d9c0403c93ad0db14a51adfe905e7e3be33af13f8787b5b0276380e39ab67c3"
)
DIRECT_INTERPRETER_BINDING_SHA256 = (
    "2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333"
)

PARENT_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_offline_observation_"
    "direct_interpreter_successor.md"
)
EXECUTOR_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md"
)
EXECUTOR_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_"
    "preflight_terminal_fallback.md"
)
EXECUTOR_LOCAL_EFFECT_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_"
    "preflight_executor_local_effect_reconciliation.md"
)
EXECUTOR_PREDECESSOR_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_"
    "preflight_executor.md"
)
EXECUTOR_IMPLEMENTATION_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_"
    "preflight_executor_implementation.md"
)
PARENT_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_offline_observation_"
    "direct_interpreter_successor.md"
)
HARNESS_PATH = Path("tools/check_role_pool_r0_offline_observation.py")
HARNESS_TEST_PATH = Path("tests/test_check_role_pool_r0_offline_observation.py")
EXECUTOR_PATH = Path("tools/run_role_pool_r0_direct_interpreter_preflight.py")
EXECUTOR_TEST_PATH = Path("tests/test_run_role_pool_r0_direct_interpreter_preflight.py")

MAX_PRIVATE_PATH_BYTES = 4096
MAX_OUTPUT_BYTES = 4096
TIMEOUT_SECONDS = 30.0
INVENTORY_TIMEOUT_SECONDS = 30.0
MAX_INVENTORY_ROWS = 4096
MAX_INVENTORY_TOTAL_BYTES = 256 * 1024 * 1024
MAX_INVENTORY_FILE_BYTES = 64 * 1024 * 1024
MAX_RELATIVE_PATH_BYTES = 1024
MAX_EFFECT_COUNT = (1 << 63) - 1
UNAVAILABLE = "unavailable"
ROLE_POOL_SOURCE_PREFIX = "docs/codex_skills/mythic-edge-role-pool"
ROLE_POOL_TREE_NODE_COUNT = 41
ROLE_POOL_TREE_FILE_COUNT = 36
ROLE_POOL_TREE_MANIFEST_BYTE_COUNT = 6495
ROLE_POOL_TREE_SHA256 = (
    "18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f"
)
DIRECTORY_READ_ATTRIBUTES = 0x00000080
DIRECTORY_LIST_DIRECTORY = 0x00000001
DIRECTORY_SHARE_READ = 0x00000001
DIRECTORY_SHARE_WRITE = 0x00000002
DIRECTORY_SHARE_DELETE = 0x00000004
DIRECTORY_OPEN_EXISTING = 3
DIRECTORY_OPEN_REPARSE_POINT = 0x00200000
DIRECTORY_BACKUP_SEMANTICS = 0x02000000
DIRECTORY_ATTRIBUTE = 0x00000010
REPARSE_POINT_ATTRIBUTE = 0x00000400
FILE_ID_BOTH_DIRECTORY_INFO = 10
FILE_ID_BOTH_DIRECTORY_RESTART_INFO = 11
ERROR_NO_MORE_FILES = 18
DIRECTORY_ENUMERATION_BUFFER_BYTES = 64 * 1024
UNKNOWN_SENTINEL = b"direct_interpreter_preflight_unknown\n"
UNKNOWN_PRECREATE_UNCONSUMED = (
    b"direct_interpreter_preflight_unknown_precreate_unconsumed\n"
)
UNKNOWN_CREATE_ENTERED_CONSUMED = (
    b"direct_interpreter_preflight_unknown_create_entered_consumed\n"
)
UNKNOWN_STAGE_AMBIGUOUS_CONSUMED = (
    b"direct_interpreter_preflight_unknown_stage_ambiguous_consumed\n"
)
FIXED_ARGUMENTS = ("-B", "-c", "pass")

CREATE_SUSPENDED = 0x00000004
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
CREATE_NO_WINDOW = 0x08000000
CREATE_UNICODE_ENVIRONMENT = 0x00000400
EXTENDED_STARTUPINFO_PRESENT = 0x00080000
BASE_CREATION_FLAGS = (
    CREATE_SUSPENDED
    | CREATE_NO_WINDOW
    | CREATE_UNICODE_ENVIRONMENT
    | EXTENDED_STARTUPINFO_PRESENT
)

RESULT_FIELDS = (
    "schema_version",
    "repository_id",
    "issue_number",
    "executor_contract_sha256",
    "executor_contract_review_sha256",
    "parent_contract_sha256",
    "parent_review_sha256",
    "harness_sha256",
    "harness_test_sha256",
    "executor_sha256",
    "executor_test_sha256",
    "direct_interpreter_binding_sha256",
    "observed_at_utc",
    "preflight_authority_consumed",
    "public_bindings_exact",
    "private_binding_exact",
    "top_level_identity_exact",
    "parentage_known",
    "exit_status",
    "stdout_byte_count",
    "stderr_byte_count",
    "top_level_process_count",
    "descendant_process_count",
    "descendant_attempt_detected",
    "timed_out",
    "cleanup_confirmed",
    "output_complete",
    "process_launch_count",
    "retry_count",
    "repository_write_count",
    "installed_write_count",
    "network_operation_count",
    "external_effect_count",
    "private_value_emitted",
    "result_status",
    "eligible_for_independent_review",
    "authority_flags",
    "result_sha256",
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

RESULT_STATUSES = (
    "direct_interpreter_hypothesis_rejected",
    "observation_binding_rejected",
    "direct_interpreter_preflight_required",
    "direct_interpreter_preflight_descendant_observed",
    "direct_interpreter_preflight_unknown",
    "direct_interpreter_preflight_passed",
)

SUCCESS_LIFECYCLE_EVENTS = (
    "stdin_pipe_created",
    "stdout_pipe_created",
    "stderr_pipe_created",
    "six_handles_validated",
    "job_created",
    "job_limits_set",
    "completion_port_attached",
    "handle_list_set",
    "stdin_writer_closed",
    "create_entered",
    "create_succeeded",
    "parent_inherited_handles_closed",
    "job_assigned",
    "one_process_readback",
    "image_validated",
    "parentage_validated",
    "resumed_once",
    "terminal_observed",
    "streams_drained",
    "post_exit_identity_validated",
    "active_zero",
    "all_handles_closed",
)

SOURCE_FIELDS = (
    "historical_direct_use_proven",
    "public_binding_state",
    "owner_decision_state",
    "private_binding_state",
    "ambient_job_state",
    "precreate_setup_state",
    "create_call_entered",
    "create_return_state",
    "top_level_identity_exact",
    "parentage_known",
    "exit_status",
    "stdout_byte_count",
    "stderr_byte_count",
    "top_level_process_count",
    "descendant_process_count",
    "descendant_attempt_detected",
    "timed_out",
    "effect_derivation_state",
    "repository_write_count",
    "installed_write_count",
    "generated_residue_delta_count",
    "executor_network_operation_count",
    "cleanup_confirmed",
    "output_complete",
)


class PreflightFailure(Exception):
    """A symbolic, no-echo preflight failure."""


class DuplicateJsonKeyError(ValueError):
    """A JSON object repeated a key."""


class ResultProjectionError(PreflightFailure):
    """Normalized facts cannot produce exactly one contracted result."""


class LocalEffectEvidenceError(ResultProjectionError):
    """Local-effect evidence cannot support a canonical zero-effect result."""


@dataclass(frozen=True)
class AmbientJobObservation:
    membership_api_exact: bool
    in_job: bool | None
    extended_query_exact: bool = False
    ui_query_exact: bool = False
    version_query_exact: bool = False
    silent_breakaway: bool = False
    breakaway: bool = False
    nested_jobs_supported: bool = False
    ui_restrictions_class: int | None = None


@dataclass(frozen=True)
class AmbientJobSelection:
    row_id: str
    admitted: bool
    creation_flags: int
    post_create_action: str


@dataclass(frozen=True)
class ProcessRecord:
    historical_direct_use_proven: bool
    public_binding_state: str
    owner_decision_state: str
    private_binding_state: str
    ambient_job_state: str
    precreate_setup_state: str
    create_call_entered: bool
    create_return_state: str
    top_level_identity_exact: bool
    parentage_known: bool
    exit_status: str
    stdout_byte_count: int
    stderr_byte_count: int
    top_level_process_count: int
    descendant_process_count: int
    descendant_attempt_detected: bool
    timed_out: bool
    cleanup_confirmed: bool
    output_complete: bool


@dataclass(frozen=True)
class SourceRecord:
    historical_direct_use_proven: bool
    public_binding_state: str
    owner_decision_state: str
    private_binding_state: str
    ambient_job_state: str
    precreate_setup_state: str
    create_call_entered: bool
    create_return_state: str
    top_level_identity_exact: bool
    parentage_known: bool
    exit_status: str
    stdout_byte_count: int
    stderr_byte_count: int
    top_level_process_count: int
    descendant_process_count: int
    descendant_attempt_detected: bool
    timed_out: bool
    effect_derivation_state: str
    repository_write_count: int
    installed_write_count: int
    generated_residue_delta_count: int
    executor_network_operation_count: int
    cleanup_confirmed: bool
    output_complete: bool


@dataclass(frozen=True)
class LocalEffectObservation:
    effect_boundary_state: str
    pre_inventory_state: str
    post_inventory_state: str
    executor_audit_state: str
    repository_write_attempt_count: int | str
    installed_write_attempt_count: int | str
    executor_network_operation_count: int | str
    repository_row_delta_count: int | str
    installed_row_delta_count: int | str
    residue_row_delta_count: int | str


@dataclass(frozen=True)
class LocalEffectDerivation:
    effect_derivation_state: str
    repository_write_count: int
    installed_write_count: int
    generated_residue_delta_count: int
    executor_network_operation_count: int
    external_effect_count: int


@dataclass(frozen=True)
class InventoryRow:
    relative_path: str
    kind: str
    byte_count: int
    sha256: str


@dataclass(frozen=True)
class TreeInventory:
    root_identity: tuple[int, int]
    rows: tuple[InventoryRow, ...]


@dataclass(frozen=True)
class _NativeDirectoryEntry:
    name: str
    file_index: int
    attributes: int
    byte_count: int


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


class _FileIdBothDirectoryInfo(ctypes.Structure):
    _fields_ = (
        ("NextEntryOffset", wintypes.DWORD),
        ("FileIndex", wintypes.DWORD),
        ("CreationTime", ctypes.c_longlong),
        ("LastAccessTime", ctypes.c_longlong),
        ("LastWriteTime", ctypes.c_longlong),
        ("ChangeTime", ctypes.c_longlong),
        ("EndOfFile", ctypes.c_longlong),
        ("AllocationSize", ctypes.c_longlong),
        ("FileAttributes", wintypes.DWORD),
        ("FileNameLength", wintypes.DWORD),
        ("EaSize", wintypes.DWORD),
        ("ShortNameLength", ctypes.c_byte),
        ("ShortName", wintypes.WCHAR * 12),
        ("FileId", ctypes.c_ulonglong),
    )


class _OwnedDirectoryGuard:
    def __init__(
        self,
        kernel32: object,
        value: int,
        identity: tuple[int, int],
    ) -> None:
        self._kernel32 = kernel32
        self.value: int | None = value
        self.identity = identity
        self.close_ok = True

    def enumerate(self) -> tuple[_NativeDirectoryEntry, ...]:
        if self.value is None:
            raise PreflightFailure
        return _enumerate_windows_directory(self._kernel32, self.value)

    def close(self) -> bool:
        if self.value is None:
            return self.close_ok
        value = self.value
        self.value = None
        try:
            self.close_ok = bool(self._kernel32.CloseHandle(value))
        except Exception:
            self.close_ok = False
        return self.close_ok


@dataclass(frozen=True)
class _EffectSnapshot:
    repository: TreeInventory
    installed: TreeInventory
    residue: tuple[InventoryRow, ...]


@dataclass(frozen=True)
class PublicBindingSnapshot:
    exact: bool
    executor_sha256: str
    executor_test_sha256: str
    parent_api: ModuleType


@dataclass(frozen=True)
class FixedLaunchRequest:
    application_path: Path
    arguments: tuple[str, str, str]
    repository_root: Path
    environment: tuple[tuple[str, str], ...]
    creation_flags: int
    timeout_seconds: float
    inherited_streams: tuple[str, str, str] = (
        "stdin_read",
        "stdout_write",
        "stderr_write",
    )


class _TerminalBoundaryTracker:
    """Track whether the invocation entered its sole process-creation call."""

    __slots__ = ("_state", "_transition_count")

    def __init__(self) -> None:
        self._state = "precreate"
        self._transition_count = 0

    def mark_create_entered(self) -> None:
        if (
            type(self._state) is not str
            or type(self._transition_count) is not int
            or self._state != "precreate"
            or self._transition_count != 0
        ):
            self._state = "ambiguous"
            self._transition_count = -1
            raise PreflightFailure
        self._state = "create_entered"
        self._transition_count = 1

    def diagnostic(self) -> bytes:
        if type(self._state) is not str or type(self._transition_count) is not int:
            return UNKNOWN_STAGE_AMBIGUOUS_CONSUMED
        if self._state == "precreate" and self._transition_count == 0:
            return UNKNOWN_PRECREATE_UNCONSUMED
        if self._state == "create_entered" and self._transition_count == 1:
            return UNKNOWN_CREATE_ENTERED_CONSUMED
        return UNKNOWN_STAGE_AMBIGUOUS_CONSUMED


def _terminal_fallback_diagnostic(tracker: object | None) -> bytes:
    if type(tracker) is not _TerminalBoundaryTracker:
        return UNKNOWN_STAGE_AMBIGUOUS_CONSUMED
    try:
        diagnostic = getattr(tracker, "diagnostic")()
    except Exception:
        return UNKNOWN_STAGE_AMBIGUOUS_CONSUMED
    if diagnostic not in {
        UNKNOWN_PRECREATE_UNCONSUMED,
        UNKNOWN_CREATE_ENTERED_CONSUMED,
        UNKNOWN_STAGE_AMBIGUOUS_CONSUMED,
    }:
        return UNKNOWN_STAGE_AMBIGUOUS_CONSUMED
    return diagnostic


class LocalEffectMonitor(Protocol):
    def observe_pre(self, parent_api: ModuleType) -> str:
        ...

    def observe_early_terminal(self) -> LocalEffectObservation:
        ...

    def enter_effect_boundary(self) -> None:
        ...

    def observe_post_terminal(self) -> LocalEffectObservation:
        ...


class DirectWindowsPreflightAdapter(Protocol):
    """The closed adapter boundary used by the single public operation."""

    def validate_public_bindings(self, repository_root: Path) -> PublicBindingSnapshot:
        ...

    def begin_local_effect_observation(
        self,
        repository_root: Path,
    ) -> LocalEffectMonitor:
        ...

    def validate_private_binding(self, path: Path, parent_api: ModuleType) -> None:
        ...

    def revalidate_private_binding(self, path: Path, parent_api: ModuleType) -> None:
        ...

    def observe_ambient_job(self) -> AmbientJobObservation:
        ...

    def execute_once(
        self,
        request: FixedLaunchRequest,
        selection: AmbientJobSelection,
        parent_api: ModuleType,
        terminal_tracker: _TerminalBoundaryTracker | None = None,
    ) -> ProcessRecord:
        ...

    def observed_at_utc(self) -> str:
        ...


def _authority_flags() -> dict[str, bool]:
    return {field: False for field in AUTHORITY_FIELDS}


def canonical_bytes(document: Mapping[str, object]) -> bytes:
    return (
        json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def self_digest(document: Mapping[str, object], digest_field: str) -> str:
    preimage = {key: value for key, value in document.items() if key != digest_field}
    return hashlib.sha256(canonical_bytes(preimage)).hexdigest()


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError
        result[key] = value
    return result


def _is_sha256(value: object) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _whole_second_utc(value: object) -> bool:
    if type(value) is not str or not value.endswith("Z") or "." in value:
        return False
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError:
        return False
    return parsed.tzinfo is UTC


def local_effect_predicate_rows(
    observation: LocalEffectObservation,
) -> tuple[str, ...]:
    """Return every literal LE row matched by the raw four-state record."""

    boundary = observation.effect_boundary_state
    pre = observation.pre_inventory_state
    post = observation.post_inventory_state
    audit = observation.executor_audit_state
    if boundary not in {"not_entered", "entered"}:
        raise LocalEffectEvidenceError
    if pre not in {"not_started", "failed_or_ambiguous", "exact"}:
        raise LocalEffectEvidenceError
    if post not in {
        "not_required",
        "failed_or_ambiguous",
        "exact_equal",
        "exact_drift",
    }:
        raise LocalEffectEvidenceError
    if audit not in {"exact_zero", "nonzero", "unreadable_or_ambiguous"}:
        raise LocalEffectEvidenceError

    matches: list[str] = []
    if boundary == "not_entered" and post == "not_required" and audit == "exact_zero":
        matches.append("LE-01")
    if (
        boundary == "entered"
        and pre == "exact"
        and post == "exact_equal"
        and audit == "exact_zero"
    ):
        matches.append("LE-02")
    if (
        (boundary == "not_entered" and post == "not_required" and audit == "nonzero")
        or (
            boundary == "entered"
            and pre == "exact"
            and post == "exact_equal"
            and audit == "nonzero"
        )
        or (
            boundary == "entered"
            and pre == "exact"
            and post == "exact_drift"
            and audit in {"exact_zero", "nonzero"}
        )
    ):
        matches.append("LE-03")
    if (
        (
            boundary == "not_entered"
            and post == "not_required"
            and audit == "unreadable_or_ambiguous"
        )
        or (
            boundary == "entered"
            and pre == "exact"
            and post == "failed_or_ambiguous"
        )
        or (
            boundary == "entered"
            and pre == "exact"
            and post in {"exact_equal", "exact_drift"}
            and audit == "unreadable_or_ambiguous"
        )
    ):
        matches.append("LE-04")
    if not matches:
        matches.append("LE-05")
    return tuple(matches)


def select_local_effect_outcome(observation: LocalEffectObservation) -> str:
    matches = local_effect_predicate_rows(observation)
    if len(matches) != 1:
        raise LocalEffectEvidenceError
    return {
        "LE-01": "early_terminal_structural_zero",
        "LE-02": "sampled_exact_zero",
        "LE-03": "effect_observed_nonzero",
        "LE-04": "effect_evidence_unavailable",
        "LE-05": "invalid_effect_source_state",
    }[matches[0]]


def _checked_effect_count(value: object) -> int:
    if type(value) is not int or not 0 <= cast(int, value) <= MAX_EFFECT_COUNT:
        raise LocalEffectEvidenceError
    return cast(int, value)


def _checked_effect_sum(*values: int) -> int:
    total = 0
    for value in values:
        total += _checked_effect_count(value)
        if total > MAX_EFFECT_COUNT:
            raise LocalEffectEvidenceError
    return total


def calculate_sampled_effect_counts(
    observation: LocalEffectObservation,
) -> LocalEffectDerivation:
    repository_attempts = _checked_effect_count(
        observation.repository_write_attempt_count
    )
    installed_attempts = _checked_effect_count(
        observation.installed_write_attempt_count
    )
    network = _checked_effect_count(observation.executor_network_operation_count)
    repository_delta = _checked_effect_count(observation.repository_row_delta_count)
    installed_delta = _checked_effect_count(observation.installed_row_delta_count)
    residue_delta = _checked_effect_count(observation.residue_row_delta_count)
    repository = _checked_effect_sum(repository_attempts, repository_delta)
    installed = _checked_effect_sum(installed_attempts, installed_delta)
    external = _checked_effect_sum(repository, installed, residue_delta, network)
    return LocalEffectDerivation(
        "sampled_exact_zero",
        repository,
        installed,
        residue_delta,
        network,
        external,
    )


def derive_local_effects(
    observation: LocalEffectObservation,
) -> LocalEffectDerivation:
    outcome = select_local_effect_outcome(observation)
    if outcome == "early_terminal_structural_zero":
        for value in (
            observation.repository_write_attempt_count,
            observation.installed_write_attempt_count,
            observation.executor_network_operation_count,
        ):
            if _checked_effect_count(value) != 0:
                raise LocalEffectEvidenceError
        if (
            observation.repository_row_delta_count != UNAVAILABLE
            or observation.installed_row_delta_count != UNAVAILABLE
            or observation.residue_row_delta_count != UNAVAILABLE
        ):
            raise LocalEffectEvidenceError
        return LocalEffectDerivation(
            "early_terminal_structural_zero",
            0,
            0,
            0,
            0,
            0,
        )
    if outcome != "sampled_exact_zero":
        raise LocalEffectEvidenceError
    result = calculate_sampled_effect_counts(observation)
    if any(
        (
            result.repository_write_count,
            result.installed_write_count,
            result.generated_residue_delta_count,
            result.executor_network_operation_count,
            result.external_effect_count,
        )
    ):
        raise LocalEffectEvidenceError
    return result


def source_record_from_process(
    record: ProcessRecord,
    observation: LocalEffectObservation,
) -> SourceRecord:
    effects = derive_local_effects(observation)
    return SourceRecord(
        historical_direct_use_proven=record.historical_direct_use_proven,
        public_binding_state=record.public_binding_state,
        owner_decision_state=record.owner_decision_state,
        private_binding_state=record.private_binding_state,
        ambient_job_state=record.ambient_job_state,
        precreate_setup_state=record.precreate_setup_state,
        create_call_entered=record.create_call_entered,
        create_return_state=record.create_return_state,
        top_level_identity_exact=record.top_level_identity_exact,
        parentage_known=record.parentage_known,
        exit_status=record.exit_status,
        stdout_byte_count=record.stdout_byte_count,
        stderr_byte_count=record.stderr_byte_count,
        top_level_process_count=record.top_level_process_count,
        descendant_process_count=record.descendant_process_count,
        descendant_attempt_detected=record.descendant_attempt_detected,
        timed_out=record.timed_out,
        effect_derivation_state=effects.effect_derivation_state,
        repository_write_count=effects.repository_write_count,
        installed_write_count=effects.installed_write_count,
        generated_residue_delta_count=effects.generated_residue_delta_count,
        executor_network_operation_count=effects.executor_network_operation_count,
        cleanup_confirmed=record.cleanup_confirmed,
        output_complete=record.output_complete,
    )


def _all_exact_types(record: SourceRecord) -> bool:
    values = tuple(getattr(record, field) for field in SOURCE_FIELDS)
    expected = (
        bool,
        str,
        str,
        str,
        str,
        str,
        bool,
        str,
        bool,
        bool,
        str,
        int,
        int,
        int,
        int,
        bool,
        bool,
        str,
        int,
        int,
        int,
        int,
        bool,
        bool,
    )
    return all(type(value) is kind for value, kind in zip(values, expected, strict=True))


def _validated_source_route(record: SourceRecord, route: str) -> str:
    expected_mode = (
        "early_terminal_structural_zero"
        if route in {"PR-01", "PR-02", "PR-03", "PR-04", "PR-05"}
        else "sampled_exact_zero"
    )
    if record.effect_derivation_state != expected_mode:
        raise ResultProjectionError
    for value in (
        record.repository_write_count,
        record.installed_write_count,
        record.generated_residue_delta_count,
        record.executor_network_operation_count,
    ):
        if _checked_effect_count(value) != 0:
            raise ResultProjectionError
    return route


def source_route(record: SourceRecord) -> str:
    """Return the sole valid sequential route or reject the source record."""

    if not _all_exact_types(record):
        raise ResultProjectionError
    later = (
        record.public_binding_state,
        record.owner_decision_state,
        record.private_binding_state,
        record.ambient_job_state,
        record.precreate_setup_state,
        record.create_return_state,
    )
    if record.historical_direct_use_proven:
        if later == ("not_observed",) * 5 + ("not_entered",) and not record.create_call_entered:
            return _validated_source_route(record, "PR-01")
        raise ResultProjectionError
    if record.public_binding_state == "rejected":
        if later[1:] == ("not_observed",) * 4 + ("not_entered",) and not record.create_call_entered:
            return _validated_source_route(record, "PR-02")
        raise ResultProjectionError
    if record.public_binding_state != "exact":
        raise ResultProjectionError
    if record.owner_decision_state == "rejected":
        if later[2:] == ("not_observed",) * 3 + ("not_entered",) and not record.create_call_entered:
            return _validated_source_route(record, "PR-03")
        raise ResultProjectionError
    if record.owner_decision_state != "exact":
        raise ResultProjectionError
    if record.private_binding_state == "rejected":
        if later[3:] == ("not_observed",) * 2 + ("not_entered",) and not record.create_call_entered:
            return _validated_source_route(record, "PR-04")
        raise ResultProjectionError
    if record.private_binding_state != "exact":
        raise ResultProjectionError
    if record.ambient_job_state == "rejected":
        if later[4:] == ("not_observed", "not_entered") and not record.create_call_entered:
            return _validated_source_route(record, "PR-05")
        raise ResultProjectionError
    if record.ambient_job_state != "admitted":
        raise ResultProjectionError
    if record.precreate_setup_state == "failed_no_process":
        if not record.create_call_entered and record.create_return_state == "not_entered":
            return _validated_source_route(record, "PR-05A")
        raise ResultProjectionError
    if record.precreate_setup_state != "complete" or not record.create_call_entered:
        raise ResultProjectionError
    if record.create_return_state == "failed_no_process":
        return _validated_source_route(record, "PR-06")
    if record.create_return_state == "succeeded_one_process":
        return _validated_source_route(record, "POST-CREATE")
    raise ResultProjectionError


def audit_source_state_domain() -> tuple[int, int]:
    """Mechanically audit the closed 2 * 3^6 * 2 * 2 stage grammar."""

    states = ("not_observed", "rejected", "exact")
    ambient = ("not_observed", "rejected", "admitted")
    setup = ("not_observed", "failed_no_process", "complete")
    returned = ("not_entered", "failed_no_process", "succeeded_one_process")
    admitted = 0
    rejected = 0
    for values in itertools.product(
        (False, True),
        states,
        states,
        states,
        ambient,
        setup,
        returned,
        (False, True),
        ("early_terminal_structural_zero", "sampled_exact_zero"),
    ):
        (
            history,
            public,
            owner,
            private,
            ambient_state,
            setup_state,
            return_state,
            entered,
            effect_mode,
        ) = values
        record = SourceRecord(
            historical_direct_use_proven=cast(bool, history),
            public_binding_state=cast(str, public),
            owner_decision_state=cast(str, owner),
            private_binding_state=cast(str, private),
            ambient_job_state=cast(str, ambient_state),
            precreate_setup_state=cast(str, setup_state),
            create_call_entered=cast(bool, entered),
            create_return_state=cast(str, return_state),
            top_level_identity_exact=False,
            parentage_known=False,
            exit_status="not_started",
            stdout_byte_count=0,
            stderr_byte_count=0,
            top_level_process_count=0,
            descendant_process_count=0,
            descendant_attempt_detected=False,
            timed_out=False,
            effect_derivation_state=cast(str, effect_mode),
            repository_write_count=0,
            installed_write_count=0,
            generated_residue_delta_count=0,
            executor_network_operation_count=0,
            cleanup_confirmed=True,
            output_complete=True,
        )
        try:
            source_route(record)
        except ResultProjectionError:
            rejected += 1
        else:
            admitted += 1
    return admitted, rejected


def select_ambient_job(observation: AmbientJobObservation) -> AmbientJobSelection:
    """Apply the eight-row ambient-job selector in precedence order."""

    if type(observation.membership_api_exact) is not bool:
        raise ValueError("ambient_job_observation_invalid")
    if not observation.membership_api_exact or type(observation.in_job) is not bool:
        return AmbientJobSelection("AJ-01", False, 0, "none")
    if not observation.in_job:
        return AmbientJobSelection("AJ-02", True, BASE_CREATION_FLAGS, "assign_once")
    exact_query_values = (
        observation.extended_query_exact,
        observation.ui_query_exact,
        observation.version_query_exact,
    )
    if any(type(value) is not bool for value in exact_query_values):
        raise ValueError("ambient_job_observation_invalid")
    ui_value_exact = (
        type(observation.ui_restrictions_class) is int
        and 0 <= observation.ui_restrictions_class <= 0xFFFFFFFF
    )
    flag_values_exact = all(
        type(value) is bool
        for value in (
            observation.silent_breakaway,
            observation.breakaway,
            observation.nested_jobs_supported,
        )
    )
    if not all(exact_query_values) or not ui_value_exact or not flag_values_exact:
        return AmbientJobSelection("AJ-03", False, 0, "none")
    if observation.silent_breakaway:
        return AmbientJobSelection("AJ-04", True, BASE_CREATION_FLAGS, "assign_once")
    if observation.breakaway:
        return AmbientJobSelection(
            "AJ-05",
            True,
            BASE_CREATION_FLAGS | CREATE_BREAKAWAY_FROM_JOB,
            "assign_once",
        )
    if observation.nested_jobs_supported and observation.ui_restrictions_class == 0:
        return AmbientJobSelection("AJ-06", True, BASE_CREATION_FLAGS, "assign_once")
    if not observation.nested_jobs_supported:
        return AmbientJobSelection("AJ-07", False, 0, "none")
    return AmbientJobSelection("AJ-08", False, 0, "none")


def select_parent_outcome(
    historical_direct_use_proven: bool,
    public_bindings_exact: bool,
    owner_decision_exact: bool,
    private_binding_exact: bool,
    parent_state: str,
) -> str:
    values = (
        historical_direct_use_proven,
        public_bindings_exact,
        owner_decision_exact,
        private_binding_exact,
    )
    if any(type(value) is not bool for value in values):
        raise ValueError("parent_selector_boolean_invalid")
    if parent_state not in {"not_run", "descendant", "unknown", "passed"}:
        raise ValueError("parent_selector_state_invalid")
    if historical_direct_use_proven:
        return "direct_interpreter_hypothesis_rejected"
    if not public_bindings_exact:
        return "observation_binding_rejected"
    if not owner_decision_exact:
        return "direct_interpreter_preflight_required"
    if not private_binding_exact:
        return "observation_binding_rejected"
    return {
        "not_run": "direct_interpreter_preflight_required",
        "descendant": "direct_interpreter_preflight_descendant_observed",
        "unknown": "direct_interpreter_preflight_unknown",
        "passed": "direct_interpreter_preflight_passed",
    }[parent_state]


def validate_success_lifecycle_trace(events: Sequence[str]) -> None:
    """Require the exact resume-once and close-once successful lifecycle."""

    if tuple(events) != SUCCESS_LIFECYCLE_EVENTS:
        raise ResultProjectionError


def _prelaunch_facts_are_exact(record: SourceRecord, *, cleanup_any: bool = False) -> bool:
    return (
        not record.top_level_identity_exact
        and not record.parentage_known
        and record.exit_status == "not_started"
        and record.stdout_byte_count == 0
        and record.stderr_byte_count == 0
        and record.top_level_process_count == 0
        and record.descendant_process_count == 0
        and not record.descendant_attempt_detected
        and not record.timed_out
        and (cleanup_any or record.cleanup_confirmed)
        and record.output_complete
    )


def _project_status(record: SourceRecord, parent_api: ModuleType) -> str:
    route = source_route(record)
    if not (0 <= record.stdout_byte_count <= MAX_OUTPUT_BYTES):
        raise ResultProjectionError
    if not (0 <= record.stderr_byte_count <= MAX_OUTPUT_BYTES):
        raise ResultProjectionError
    if record.top_level_process_count not in {0, 1}:
        raise ResultProjectionError
    if record.descendant_process_count < 0:
        raise ResultProjectionError
    if record.descendant_attempt_detected != (record.descendant_process_count > 0):
        raise ResultProjectionError
    if route in {"PR-01", "PR-02", "PR-03", "PR-04", "PR-05"}:
        if not _prelaunch_facts_are_exact(record):
            raise ResultProjectionError
        return {
            "PR-01": "direct_interpreter_hypothesis_rejected",
            "PR-02": "observation_binding_rejected",
            "PR-03": "direct_interpreter_preflight_required",
            "PR-04": "observation_binding_rejected",
            "PR-05": "observation_binding_rejected",
        }[route]
    if route == "PR-05A":
        if not _prelaunch_facts_are_exact(record, cleanup_any=True):
            raise ResultProjectionError
        return "direct_interpreter_preflight_unknown"
    if route == "PR-06":
        if not _prelaunch_facts_are_exact(record):
            raise ResultProjectionError
        return "direct_interpreter_preflight_unknown"
    if record.top_level_process_count != 1 or record.exit_status == "not_started":
        raise ResultProjectionError
    if record.exit_status not in {"zero", "nonzero", "unknown"}:
        raise ResultProjectionError
    exit_code = {"zero": 0, "nonzero": 1, "unknown": None}[record.exit_status]
    observation = parent_api.DirectPreflightObservation(
        public_binding_exact=True,
        private_binding_exact=True,
        top_level_identity_exact=record.top_level_identity_exact,
        parentage_known=record.parentage_known,
        exit_code=exit_code,
        stdout=b"x" * record.stdout_byte_count,
        stderr=b"x" * record.stderr_byte_count,
        top_level_process_count=record.top_level_process_count,
        descendant_process_count=record.descendant_process_count,
        timed_out=record.timed_out,
        cleanup_confirmed=record.cleanup_confirmed,
        output_complete=record.output_complete,
    )
    status = parent_api.classify_direct_preflight_observation(observation)
    if status not in RESULT_STATUSES:
        raise ResultProjectionError
    return cast(str, status)


def _validate_result_semantics(document: Mapping[str, object]) -> None:
    if tuple(document) != RESULT_FIELDS:
        raise ResultProjectionError
    if document["schema_version"] != RESULT_SCHEMA:
        raise ResultProjectionError
    if document["repository_id"] != REPOSITORY_ID or type(document["repository_id"]) is not int:
        raise ResultProjectionError
    if document["issue_number"] != ISSUE_NUMBER or type(document["issue_number"]) is not int:
        raise ResultProjectionError
    for field in (
        "executor_contract_sha256",
        "executor_contract_review_sha256",
        "parent_contract_sha256",
        "parent_review_sha256",
        "harness_sha256",
        "harness_test_sha256",
        "executor_sha256",
        "executor_test_sha256",
        "direct_interpreter_binding_sha256",
        "result_sha256",
    ):
        if not _is_sha256(document[field]):
            raise ResultProjectionError
    if not _whole_second_utc(document["observed_at_utc"]):
        raise ResultProjectionError
    boolean_fields = (
        "preflight_authority_consumed",
        "public_bindings_exact",
        "private_binding_exact",
        "top_level_identity_exact",
        "parentage_known",
        "descendant_attempt_detected",
        "timed_out",
        "cleanup_confirmed",
        "output_complete",
        "private_value_emitted",
        "eligible_for_independent_review",
    )
    if any(type(document[field]) is not bool for field in boolean_fields):
        raise ResultProjectionError
    if document["exit_status"] not in {"not_started", "zero", "nonzero", "unknown"}:
        raise ResultProjectionError
    integer_fields = (
        "stdout_byte_count",
        "stderr_byte_count",
        "top_level_process_count",
        "descendant_process_count",
        "process_launch_count",
        "retry_count",
        "repository_write_count",
        "installed_write_count",
        "network_operation_count",
        "external_effect_count",
    )
    if any(type(document[field]) is not int for field in integer_fields):
        raise ResultProjectionError
    if not 0 <= cast(int, document["stdout_byte_count"]) <= MAX_OUTPUT_BYTES:
        raise ResultProjectionError
    if not 0 <= cast(int, document["stderr_byte_count"]) <= MAX_OUTPUT_BYTES:
        raise ResultProjectionError
    if document["top_level_process_count"] not in {0, 1}:
        raise ResultProjectionError
    if document["process_launch_count"] not in {0, 1}:
        raise ResultProjectionError
    if cast(int, document["descendant_process_count"]) < 0:
        raise ResultProjectionError
    if document["descendant_attempt_detected"] != (
        cast(int, document["descendant_process_count"]) > 0
    ):
        raise ResultProjectionError
    for field in (
        "retry_count",
        "repository_write_count",
        "installed_write_count",
        "network_operation_count",
        "external_effect_count",
    ):
        if document[field] != 0:
            raise ResultProjectionError
    if document["private_value_emitted"] is not False:
        raise ResultProjectionError
    if document["eligible_for_independent_review"] is not True:
        raise ResultProjectionError
    authority = document["authority_flags"]
    if type(authority) is not dict or tuple(authority) != AUTHORITY_FIELDS:
        raise ResultProjectionError
    if any(type(value) is not bool or value for value in cast(dict[str, object], authority).values()):
        raise ResultProjectionError
    status = document["result_status"]
    if status not in RESULT_STATUSES:
        raise ResultProjectionError
    consumed = cast(bool, document["preflight_authority_consumed"])
    public = cast(bool, document["public_bindings_exact"])
    private = cast(bool, document["private_binding_exact"])
    top = cast(int, document["top_level_process_count"])
    launch = cast(int, document["process_launch_count"])
    exit_status = cast(str, document["exit_status"])
    stdout_count = cast(int, document["stdout_byte_count"])
    stderr_count = cast(int, document["stderr_byte_count"])
    descendant = cast(int, document["descendant_process_count"])
    early_unknown = (
        cast(bool, document["timed_out"])
        or not cast(bool, document["cleanup_confirmed"])
        or not cast(bool, document["top_level_identity_exact"])
        or not cast(bool, document["parentage_known"])
        or exit_status == "unknown"
    )
    late_unknown = (
        exit_status == "nonzero"
        or stdout_count != 0
        or stderr_count != 0
        or not cast(bool, document["output_complete"])
    )
    prelaunch_shape = (
        not consumed
        and top == 0
        and launch == 0
        and exit_status == "not_started"
        and stdout_count == 0
        and stderr_count == 0
        and descendant == 0
        and not cast(bool, document["timed_out"])
        and cast(bool, document["output_complete"])
        and not cast(bool, document["top_level_identity_exact"])
        and not cast(bool, document["parentage_known"])
    )
    if status == "direct_interpreter_hypothesis_rejected":
        valid = prelaunch_shape and not public and not private and document["cleanup_confirmed"] is True
    elif status == "observation_binding_rejected":
        valid = prelaunch_shape and document["cleanup_confirmed"] is True and not (not public and private)
    elif status == "direct_interpreter_preflight_required":
        valid = prelaunch_shape and public and not private and document["cleanup_confirmed"] is True
    elif status == "direct_interpreter_preflight_passed":
        valid = (
            consumed
            and public
            and private
            and top == launch == 1
            and not early_unknown
            and descendant == 0
            and not late_unknown
            and exit_status == "zero"
        )
    elif status == "direct_interpreter_preflight_descendant_observed":
        valid = (
            consumed
            and public
            and private
            and top == launch == 1
            and not early_unknown
            and descendant > 0
        )
    else:
        precreate_unknown = prelaunch_shape and public and private
        create_failed = (
            consumed
            and public
            and private
            and top == launch == 0
            and exit_status == "not_started"
            and stdout_count == stderr_count == descendant == 0
            and not cast(bool, document["timed_out"])
            and cast(bool, document["cleanup_confirmed"])
            and cast(bool, document["output_complete"])
        )
        postcreate_unknown = (
            consumed
            and public
            and private
            and top == launch == 1
            and (early_unknown or (descendant == 0 and late_unknown))
        )
        valid = precreate_unknown or create_failed or postcreate_unknown
    if not valid:
        raise ResultProjectionError
    if document["result_sha256"] != self_digest(document, "result_sha256"):
        raise ResultProjectionError


def seal_result(
    record: SourceRecord,
    bindings: PublicBindingSnapshot,
    observed_at_utc: str,
) -> dict[str, object]:
    status = _project_status(record, bindings.parent_api)
    route = source_route(record)
    consumed = record.create_call_entered
    public_exact = record.public_binding_state == "exact"
    private_exact = record.private_binding_state == "exact"
    process_launch_count = 1 if record.create_return_state == "succeeded_one_process" else 0
    external_effect_count = _checked_effect_sum(
        record.repository_write_count,
        record.installed_write_count,
        record.generated_residue_delta_count,
        record.executor_network_operation_count,
    )
    result: dict[str, object] = {
        "schema_version": RESULT_SCHEMA,
        "repository_id": REPOSITORY_ID,
        "issue_number": ISSUE_NUMBER,
        "executor_contract_sha256": EXECUTOR_CONTRACT_SHA256,
        "executor_contract_review_sha256": EXECUTOR_CONTRACT_REVIEW_SHA256,
        "parent_contract_sha256": PARENT_CONTRACT_SHA256,
        "parent_review_sha256": PARENT_REVIEW_SHA256,
        "harness_sha256": HARNESS_SHA256,
        "harness_test_sha256": HARNESS_TEST_SHA256,
        "executor_sha256": bindings.executor_sha256,
        "executor_test_sha256": bindings.executor_test_sha256,
        "direct_interpreter_binding_sha256": DIRECT_INTERPRETER_BINDING_SHA256,
        "observed_at_utc": observed_at_utc,
        "preflight_authority_consumed": consumed,
        "public_bindings_exact": public_exact,
        "private_binding_exact": private_exact,
        "top_level_identity_exact": record.top_level_identity_exact,
        "parentage_known": record.parentage_known,
        "exit_status": record.exit_status,
        "stdout_byte_count": record.stdout_byte_count,
        "stderr_byte_count": record.stderr_byte_count,
        "top_level_process_count": record.top_level_process_count,
        "descendant_process_count": record.descendant_process_count,
        "descendant_attempt_detected": record.descendant_attempt_detected,
        "timed_out": record.timed_out,
        "cleanup_confirmed": record.cleanup_confirmed,
        "output_complete": record.output_complete,
        "process_launch_count": process_launch_count,
        "retry_count": 0,
        "repository_write_count": record.repository_write_count,
        "installed_write_count": record.installed_write_count,
        "network_operation_count": record.executor_network_operation_count,
        "external_effect_count": external_effect_count,
        "private_value_emitted": False,
        "result_status": status,
        "eligible_for_independent_review": True,
        "authority_flags": _authority_flags(),
    }
    if route == "PR-01":
        result["public_bindings_exact"] = False
        result["private_binding_exact"] = False
    validate_result_source_binding(result, record, bindings.parent_api)
    result["result_sha256"] = self_digest(result, "result_sha256")
    _validate_result_semantics(result)
    if len(canonical_bytes(result)) > MAX_OUTPUT_BYTES:
        raise ResultProjectionError
    return result


def validate_result_source_binding(
    document: Mapping[str, object],
    record: SourceRecord,
    parent_api: ModuleType,
) -> None:
    """Bind a projected result to its non-serialized normalized source facts."""

    expected_status = _project_status(record, parent_api)
    expected = {
        "preflight_authority_consumed": record.create_call_entered,
        "public_bindings_exact": record.public_binding_state == "exact",
        "private_binding_exact": record.private_binding_state == "exact",
        "top_level_identity_exact": record.top_level_identity_exact,
        "parentage_known": record.parentage_known,
        "exit_status": record.exit_status,
        "stdout_byte_count": record.stdout_byte_count,
        "stderr_byte_count": record.stderr_byte_count,
        "top_level_process_count": record.top_level_process_count,
        "descendant_process_count": record.descendant_process_count,
        "descendant_attempt_detected": record.descendant_attempt_detected,
        "timed_out": record.timed_out,
        "cleanup_confirmed": record.cleanup_confirmed,
        "output_complete": record.output_complete,
        "process_launch_count": (
            1 if record.create_return_state == "succeeded_one_process" else 0
        ),
        "repository_write_count": record.repository_write_count,
        "installed_write_count": record.installed_write_count,
        "network_operation_count": record.executor_network_operation_count,
        "external_effect_count": _checked_effect_sum(
            record.repository_write_count,
            record.installed_write_count,
            record.generated_residue_delta_count,
            record.executor_network_operation_count,
        ),
        "result_status": expected_status,
    }
    if source_route(record) == "PR-01":
        expected["public_bindings_exact"] = False
        expected["private_binding_exact"] = False
    if any(document.get(field) != value for field, value in expected.items()):
        raise ResultProjectionError


def parse_result(payload: bytes) -> dict[str, object]:
    if len(payload) > MAX_OUTPUT_BYTES or not payload.endswith(b"\n") or payload.endswith(b"\n\n"):
        raise ResultProjectionError
    try:
        result = json.loads(payload.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        raise ResultProjectionError from exc
    if type(result) is not dict or canonical_bytes(result) != payload:
        raise ResultProjectionError
    _validate_result_semantics(result)
    return cast(dict[str, object], result)


def _empty_record(
    *,
    public: str,
    owner: str,
    private: str,
    ambient: str,
    setup: str = "not_observed",
    cleanup_confirmed: bool = True,
) -> ProcessRecord:
    return ProcessRecord(
        historical_direct_use_proven=False,
        public_binding_state=public,
        owner_decision_state=owner,
        private_binding_state=private,
        ambient_job_state=ambient,
        precreate_setup_state=setup,
        create_call_entered=False,
        create_return_state="not_entered",
        top_level_identity_exact=False,
        parentage_known=False,
        exit_status="not_started",
        stdout_byte_count=0,
        stderr_byte_count=0,
        top_level_process_count=0,
        descendant_process_count=0,
        descendant_attempt_detected=False,
        timed_out=False,
        cleanup_confirmed=cleanup_confirmed,
        output_complete=True,
    )


def _stable_file_sha256(path: Path) -> str:
    before = path.lstat()
    attributes = getattr(before, "st_file_attributes", 0)
    if not stat.S_ISREG(before.st_mode) or attributes & 0x400:
        raise PreflightFailure
    digest = hashlib.sha256()
    with path.open("rb", buffering=0) as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino, opened.st_size) != (
            before.st_dev,
            before.st_ino,
            before.st_size,
        ):
            raise PreflightFailure
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    final = path.lstat()
    identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    if identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise PreflightFailure
    if identity != (final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns):
        raise PreflightFailure
    return digest.hexdigest()


def _is_reparse_metadata(metadata: os.stat_result) -> bool:
    marker = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(metadata.st_mode) or bool(
        getattr(metadata, "st_file_attributes", 0) & marker
    )


def _directory_identity(metadata: os.stat_result) -> tuple[int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        stat.S_IFMT(metadata.st_mode),
        getattr(metadata, "st_file_attributes", 0),
    )


def _file_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        stat.S_IFMT(metadata.st_mode),
        metadata.st_size,
        metadata.st_mtime_ns,
        getattr(metadata, "st_file_attributes", 0),
    )


def _validate_relative_path(relative_path: str) -> None:
    parts = relative_path.split("/")
    if (
        not relative_path
        or "\x00" in relative_path
        or relative_path.startswith("/")
        or any(part in {"", ".", ".."} for part in parts)
        or (len(parts[0]) >= 2 and parts[0][1] == ":")
        or len(relative_path.encode("utf-8")) > MAX_RELATIVE_PATH_BYTES
    ):
        raise PreflightFailure


def _register_inventory_path(
    relative_path: str,
    seen: set[str],
    folded: set[str],
) -> None:
    _validate_relative_path(relative_path)
    folded_path = relative_path.casefold()
    if relative_path in seen or folded_path in folded:
        raise PreflightFailure
    seen.add(relative_path)
    folded.add(folded_path)


def _inventory_deadline_ok(deadline: float) -> None:
    if time.monotonic() > deadline:
        raise PreflightFailure


def _directory_kernel32() -> ctypes.WinDLL:
    if os.name != "nt" or sys.platform != "win32":
        raise PreflightFailure
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
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
    kernel32.GetFileInformationByHandleEx.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
    )
    kernel32.GetFileInformationByHandleEx.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


def _open_windows_directory_guard(
    path: Path,
    kernel32: object,
) -> _OwnedDirectoryGuard:
    handle = kernel32.CreateFileW(
        os.fspath(path),
        DIRECTORY_LIST_DIRECTORY | DIRECTORY_READ_ATTRIBUTES,
        DIRECTORY_SHARE_READ | DIRECTORY_SHARE_WRITE | DIRECTORY_SHARE_DELETE,
        None,
        DIRECTORY_OPEN_EXISTING,
        DIRECTORY_OPEN_REPARSE_POINT | DIRECTORY_BACKUP_SEMANTICS,
        None,
    )
    invalid_handle = ctypes.c_void_p(-1).value
    if handle in (None, invalid_handle):
        raise PreflightFailure
    try:
        information = _ByHandleFileInformation()
        if not kernel32.GetFileInformationByHandle(
            handle,
            ctypes.byref(information),
        ):
            raise PreflightFailure
        attributes = int(information.dwFileAttributes)
        if not attributes & DIRECTORY_ATTRIBUTE or attributes & REPARSE_POINT_ATTRIBUTE:
            raise PreflightFailure
        file_index = (
            int(information.nFileIndexHigh) << 32
        ) | int(information.nFileIndexLow)
        return _OwnedDirectoryGuard(
            kernel32,
            cast(int, handle),
            (int(information.dwVolumeSerialNumber), file_index),
        )
    except Exception:
        try:
            kernel32.CloseHandle(handle)
        except Exception:
            pass
        raise PreflightFailure from None


def _enumerate_windows_directory(
    kernel32: object,
    handle: int,
) -> tuple[_NativeDirectoryEntry, ...]:
    buffer = ctypes.create_string_buffer(DIRECTORY_ENUMERATION_BUFFER_BYTES)
    information_class = FILE_ID_BOTH_DIRECTORY_RESTART_INFO
    entries: list[_NativeDirectoryEntry] = []
    while True:
        if not kernel32.GetFileInformationByHandleEx(
            handle,
            information_class,
            buffer,
            len(buffer),
        ):
            if ctypes.get_last_error() == ERROR_NO_MORE_FILES:
                break
            raise PreflightFailure
        information_class = FILE_ID_BOTH_DIRECTORY_INFO
        offset = 0
        while True:
            if offset % 8 or offset + ctypes.sizeof(_FileIdBothDirectoryInfo) > len(buffer):
                raise PreflightFailure
            record = _FileIdBothDirectoryInfo.from_buffer(buffer, offset)
            name_bytes = int(record.FileNameLength)
            if not name_bytes or name_bytes % 2:
                raise PreflightFailure
            record_end = (
                offset + int(record.NextEntryOffset)
                if record.NextEntryOffset
                else len(buffer)
            )
            name_offset = offset + ctypes.sizeof(_FileIdBothDirectoryInfo)
            if name_offset + name_bytes > record_end:
                raise PreflightFailure
            name = ctypes.wstring_at(
                ctypes.addressof(buffer) + name_offset,
                name_bytes // 2,
            )
            if name not in {".", ".."}:
                byte_count = int(record.EndOfFile)
                if byte_count < 0:
                    raise PreflightFailure
                entries.append(
                    _NativeDirectoryEntry(
                        name,
                        int(record.FileId),
                        int(record.FileAttributes),
                        byte_count,
                    )
                )
            next_offset = int(record.NextEntryOffset)
            if next_offset == 0:
                break
            if next_offset < ctypes.sizeof(_FileIdBothDirectoryInfo) or next_offset % 8:
                raise PreflightFailure
            offset += next_offset
    return tuple(sorted(entries, key=lambda entry: entry.name.encode("utf-8")))


def _open_directory_guard(path: Path) -> _OwnedDirectoryGuard:
    return _open_windows_directory_guard(path, _directory_kernel32())


def _close_directory_guards(guards: Sequence[_OwnedDirectoryGuard]) -> bool:
    all_closed = True
    for guard in reversed(guards):
        try:
            closed = guard.close()
        except Exception:
            closed = False
        all_closed = bool(closed) and all_closed
    return all_closed


def _enumerate_kind_map(
    root: Path,
    *,
    exclude_top_level_git: bool,
    deadline: float,
    expected_kinds: Mapping[str, str],
    guarded_directories: Mapping[Path, _OwnedDirectoryGuard],
) -> dict[str, str]:
    pending = [root]
    rows: dict[str, str] = {}
    seen: set[str] = set()
    folded: set[str] = set()
    while pending:
        _inventory_deadline_ok(deadline)
        directory = pending.pop()
        guard = guarded_directories.get(directory)
        if guard is None:
            raise PreflightFailure
        entries = guard.enumerate()
        children: list[Path] = []
        for entry in entries:
            if exclude_top_level_git and directory == root and entry.name == ".git":
                continue
            _inventory_deadline_ok(deadline)
            if not entry.name or any(marker in entry.name for marker in ("\x00", "/", "\\")):
                raise PreflightFailure
            path = directory / entry.name
            try:
                relative = path.relative_to(root).as_posix()
            except ValueError as exc:
                raise PreflightFailure from exc
            _register_inventory_path(relative, seen, folded)
            if entry.attributes & REPARSE_POINT_ATTRIBUTE:
                raise PreflightFailure
            if entry.attributes & DIRECTORY_ATTRIBUTE:
                kind = "directory"
                if expected_kinds.get(relative) != kind or path not in guarded_directories:
                    raise PreflightFailure
                children.append(path)
            else:
                kind = "file"
            if expected_kinds.get(relative) != kind:
                raise PreflightFailure
            rows[relative] = kind
            if len(rows) > MAX_INVENTORY_ROWS:
                raise PreflightFailure
        pending.extend(reversed(children))
    return rows


def _observe_tree_inventory_guarded(
    root: Path,
    *,
    exclude_top_level_git: bool,
    guards: list[_OwnedDirectoryGuard],
) -> TreeInventory:
    """Build one bounded, stable, read-only in-memory tree inventory."""

    root = root.absolute()
    deadline = time.monotonic() + INVENTORY_TIMEOUT_SECONDS
    root_guard = _open_directory_guard(root)
    guards.append(root_guard)
    root_before = root.lstat()
    if (
        not stat.S_ISDIR(root_before.st_mode)
        or _is_reparse_metadata(root_before)
        or root_before.st_ino != root_guard.identity[1]
    ):
        raise PreflightFailure
    root_identity = root_guard.identity
    pending = [root]
    rows: list[InventoryRow] = []
    seen: set[str] = set()
    folded: set[str] = set()
    directory_identities: dict[Path, tuple[int, int, int, int]] = {
        root: _directory_identity(root_before)
    }
    directory_guards = {root: root_guard}
    total_bytes = 0
    while pending:
        _inventory_deadline_ok(deadline)
        directory = pending.pop()
        guard = directory_guards.get(directory)
        if guard is None:
            raise PreflightFailure
        entries = guard.enumerate()
        children: list[Path] = []
        for entry in entries:
            if exclude_top_level_git and directory == root and entry.name == ".git":
                continue
            _inventory_deadline_ok(deadline)
            if not entry.name or any(marker in entry.name for marker in ("\x00", "/", "\\")):
                raise PreflightFailure
            path = directory / entry.name
            try:
                relative = path.relative_to(root).as_posix()
            except ValueError as exc:
                raise PreflightFailure from exc
            if not _path_is_within(path, root):
                raise PreflightFailure
            _register_inventory_path(relative, seen, folded)
            if len(seen) > MAX_INVENTORY_ROWS:
                raise PreflightFailure
            if entry.attributes & REPARSE_POINT_ATTRIBUTE:
                raise PreflightFailure
            path_before = path.lstat()
            if path_before.st_ino != entry.file_index:
                raise PreflightFailure
            before = path_before
            if entry.attributes & DIRECTORY_ATTRIBUTE:
                if not stat.S_ISDIR(before.st_mode) or _is_reparse_metadata(before):
                    raise PreflightFailure
                child_guard = _open_directory_guard(path)
                guards.append(child_guard)
                if (
                    child_guard.identity[0] != root_identity[0]
                    or child_guard.identity[1] != entry.file_index
                    or child_guard.identity[1] != before.st_ino
                ):
                    raise PreflightFailure
                directory_identities[path] = _directory_identity(before)
                directory_guards[path] = child_guard
                rows.append(
                    InventoryRow(
                        relative,
                        "directory",
                        0,
                        hashlib.sha256(b"").hexdigest(),
                    )
                )
                children.append(path)
                continue
            if not stat.S_ISREG(before.st_mode):
                raise PreflightFailure
            if before.st_size != entry.byte_count or before.st_size > MAX_INVENTORY_FILE_BYTES:
                raise PreflightFailure
            total_bytes += before.st_size
            if total_bytes > MAX_INVENTORY_TOTAL_BYTES:
                raise PreflightFailure
            digest = hashlib.sha256()
            retained = 0
            with path.open("rb", buffering=0) as stream:
                opened = os.fstat(stream.fileno())
                if (
                    _is_reparse_metadata(opened)
                    or _file_identity(opened) != _file_identity(before)
                ):
                    raise PreflightFailure
                while retained < before.st_size:
                    _inventory_deadline_ok(deadline)
                    chunk = stream.read(min(1024 * 1024, before.st_size - retained))
                    if not chunk:
                        raise PreflightFailure
                    retained += len(chunk)
                    digest.update(chunk)
                if stream.read(1):
                    raise PreflightFailure
                after_read = os.fstat(stream.fileno())
                if _file_identity(after_read) != _file_identity(before):
                    raise PreflightFailure
            after_close = path.lstat()
            if (
                not _path_is_within(path, root)
                or _is_reparse_metadata(after_close)
                or _file_identity(after_close) != _file_identity(before)
            ):
                raise PreflightFailure
            rows.append(InventoryRow(relative, "file", retained, digest.hexdigest()))
        pending.extend(reversed(children))
    for directory, identity in directory_identities.items():
        metadata = directory.lstat()
        if (
            _is_reparse_metadata(metadata)
            or _directory_identity(metadata) != identity
            or metadata.st_ino != directory_guards[directory].identity[1]
        ):
            raise PreflightFailure
    root_after = root.lstat()
    if (
        _directory_identity(root_after) != directory_identities[root]
        or root_after.st_ino != root_identity[1]
        or _is_reparse_metadata(root_after)
    ):
        raise PreflightFailure
    first_kinds = {row.relative_path: row.kind for row in rows}
    if first_kinds != _enumerate_kind_map(
        root,
        exclude_top_level_git=exclude_top_level_git,
        deadline=deadline,
        expected_kinds=first_kinds,
        guarded_directories=directory_guards,
    ):
        raise PreflightFailure
    ordered = tuple(sorted(rows, key=lambda row: row.relative_path.encode("utf-8")))
    return TreeInventory(root_identity, ordered)


def observe_tree_inventory(
    root: Path,
    *,
    exclude_top_level_git: bool,
) -> TreeInventory:
    guards: list[_OwnedDirectoryGuard] = []
    try:
        inventory = _observe_tree_inventory_guarded(
            root,
            exclude_top_level_git=exclude_top_level_git,
            guards=guards,
        )
    except Exception:
        _close_directory_guards(guards)
        raise
    if not _close_directory_guards(guards):
        raise PreflightFailure
    return inventory


def _residue_projection(rows: Sequence[InventoryRow]) -> tuple[InventoryRow, ...]:
    selected = []
    for row in rows:
        components = row.relative_path.split("/")
        if (
            any(component in {"__pycache__", ".pytest_cache", ".ruff_cache"} for component in components)
            or components[-1].endswith((".pyc", ".pyo"))
        ):
            selected.append(row)
    return tuple(selected)


def inventory_row_delta_count(
    before: Sequence[InventoryRow],
    after: Sequence[InventoryRow],
) -> int:
    before_rows = {row.relative_path: row for row in before}
    after_rows = {row.relative_path: row for row in after}
    paths = before_rows.keys() | after_rows.keys()
    return sum(before_rows.get(path) != after_rows.get(path) for path in paths)


def _tree_manifest_binding(rows: Sequence[InventoryRow]) -> tuple[int, int, int, str]:
    document = {
        "schema_version": "trusted_owner_role_pool_install_tree.v1",
        "rows": [
            {
                "path": row.relative_path,
                "kind": row.kind,
                "byte_count": row.byte_count,
                "sha256": row.sha256,
            }
            for row in rows
        ],
    }
    encoded = json.dumps(
        document,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    return (
        len(rows),
        sum(row.kind == "file" for row in rows),
        len(encoded),
        hashlib.sha256(encoded).hexdigest(),
    )


def _validate_role_pool_projection(
    repository: TreeInventory,
    installed: TreeInventory,
) -> None:
    prefix = ROLE_POOL_SOURCE_PREFIX + "/"
    source_rows = tuple(
        replace(row, relative_path=row.relative_path[len(prefix) :])
        for row in repository.rows
        if row.relative_path.startswith(prefix)
    )
    expected = (
        ROLE_POOL_TREE_NODE_COUNT,
        ROLE_POOL_TREE_FILE_COUNT,
        ROLE_POOL_TREE_MANIFEST_BYTE_COUNT,
        ROLE_POOL_TREE_SHA256,
    )
    if _tree_manifest_binding(source_rows) != expected:
        raise PreflightFailure
    if _tree_manifest_binding(installed.rows) != expected:
        raise PreflightFailure


def _lexically_equal(left: Path, right: Path) -> bool:
    return os.path.normcase(os.path.abspath(left)) == os.path.normcase(
        os.path.abspath(right)
    )


def _path_is_within(path: object, root: Path) -> bool:
    try:
        candidate = os.path.normcase(os.path.abspath(os.fspath(path)))
        expected = os.path.normcase(os.path.abspath(root))
        return os.path.commonpath((candidate, expected)) == expected
    except (OSError, TypeError, ValueError):
        return False


class _ExecutorAuditOwner:
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
    _PROCESS_EVENTS = {
        "subprocess.Popen",
        "os.system",
        "os.posix_spawn",
        "os.posix_spawnp",
        "os.startfile",
        "os.startfile/2",
    }

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.installed_root: Path | None = None
        self.repository_write_attempt_count = 0
        self.installed_write_attempt_count = 0
        self.executor_network_operation_count = 0
        self.invalid = False

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

    def bind_installed_root(self, path: Path) -> None:
        if self.installed_root is not None or not path.is_absolute():
            self.invalid = True
            raise LocalEffectEvidenceError
        self.installed_root = path

    def _increment(self, field: str) -> None:
        value = getattr(self, field)
        if type(value) is not int or value >= MAX_EFFECT_COUNT:
            self.invalid = True
            raise LocalEffectEvidenceError
        setattr(self, field, value + 1)

    def _record_write(self, path: object) -> None:
        if _path_is_within(path, self.repository_root):
            self._increment("repository_write_attempt_count")
        elif self.installed_root is not None and _path_is_within(path, self.installed_root):
            self._increment("installed_write_attempt_count")
        else:
            self.invalid = True
        raise LocalEffectEvidenceError

    def __call__(self, event: str, args: tuple[object, ...]) -> None:
        if event.startswith("socket."):
            self._increment("executor_network_operation_count")
            raise LocalEffectEvidenceError
        if event in self._ENVIRONMENT_EVENTS or event in self._PROCESS_EVENTS or event.startswith(
            "os.spawn"
        ):
            self.invalid = True
            raise LocalEffectEvidenceError
        if event == "open" and self._open_is_write(args):
            self._record_write(args[0] if args else None)
        if event in self._MUTATION_EVENTS:
            self._record_write(args[0] if args else None)

    def values(self) -> tuple[str, int | str, int | str, int | str]:
        if self.invalid:
            return (
                "unreadable_or_ambiguous",
                UNAVAILABLE,
                UNAVAILABLE,
                UNAVAILABLE,
            )
        values = (
            self.repository_write_attempt_count,
            self.installed_write_attempt_count,
            self.executor_network_operation_count,
        )
        state = "nonzero" if any(values) else "exact_zero"
        return state, *values


_production_audit_owner: _ExecutorAuditOwner | None = None


def _derive_installed_role_pool_root(
    repository_root: Path,
    parent_api: ModuleType,
) -> Path:
    checker = parent_api._load_checker(repository_root)
    roots = checker._production_roots()
    if (
        roots.installed_skills_root is None
        or not _lexically_equal(roots.repository_root, repository_root)
    ):
        raise PreflightFailure
    return roots.installed_skills_root / "mythic-edge-role-pool"


class _ProductionLocalEffectMonitor:
    def __init__(self, repository_root: Path) -> None:
        global _production_audit_owner
        if _production_audit_owner is not None:
            raise LocalEffectEvidenceError
        self.repository_root = repository_root
        self.audit = _ExecutorAuditOwner(repository_root)
        _production_audit_owner = self.audit
        sys.addaudithook(self.audit)
        self.pre_inventory_state = "not_started"
        self.effect_boundary_state = "not_entered"
        self.pre_snapshot: _EffectSnapshot | None = None
        self.installed_root: Path | None = None

    def observe_pre(self, parent_api: ModuleType) -> str:
        if self.pre_inventory_state != "not_started" or self.effect_boundary_state != "not_entered":
            raise LocalEffectEvidenceError
        try:
            self.installed_root = _derive_installed_role_pool_root(
                self.repository_root,
                parent_api,
            )
            self.audit.bind_installed_root(self.installed_root)
            repository = observe_tree_inventory(
                self.repository_root,
                exclude_top_level_git=True,
            )
            installed = observe_tree_inventory(
                self.installed_root,
                exclude_top_level_git=False,
            )
            _validate_role_pool_projection(repository, installed)
            self.pre_snapshot = _EffectSnapshot(
                repository,
                installed,
                _residue_projection((*repository.rows, *installed.rows)),
            )
        except Exception:
            self.pre_inventory_state = "failed_or_ambiguous"
        else:
            self.pre_inventory_state = "exact"
        return self.pre_inventory_state

    def _raw_observation(
        self,
        *,
        post_state: str,
        repository_delta: int | str,
        installed_delta: int | str,
        residue_delta: int | str,
    ) -> LocalEffectObservation:
        audit_state, repository_attempts, installed_attempts, network = self.audit.values()
        return LocalEffectObservation(
            self.effect_boundary_state,
            self.pre_inventory_state,
            post_state,
            audit_state,
            repository_attempts,
            installed_attempts,
            network,
            repository_delta,
            installed_delta,
            residue_delta,
        )

    def observe_early_terminal(self) -> LocalEffectObservation:
        if self.effect_boundary_state != "not_entered":
            raise LocalEffectEvidenceError
        return self._raw_observation(
            post_state="not_required",
            repository_delta=UNAVAILABLE,
            installed_delta=UNAVAILABLE,
            residue_delta=UNAVAILABLE,
        )

    def enter_effect_boundary(self) -> None:
        if self.pre_inventory_state != "exact" or self.effect_boundary_state != "not_entered":
            raise LocalEffectEvidenceError
        self.effect_boundary_state = "entered"

    def observe_post_terminal(self) -> LocalEffectObservation:
        if (
            self.effect_boundary_state != "entered"
            or self.pre_snapshot is None
            or self.installed_root is None
        ):
            raise LocalEffectEvidenceError
        repository: TreeInventory | None = None
        installed: TreeInventory | None = None
        try:
            repository = observe_tree_inventory(
                self.repository_root,
                exclude_top_level_git=True,
            )
        except Exception:
            pass
        try:
            installed = observe_tree_inventory(
                self.installed_root,
                exclude_top_level_git=False,
            )
        except Exception:
            pass
        if repository is None or installed is None:
            return self._raw_observation(
                post_state="failed_or_ambiguous",
                repository_delta=UNAVAILABLE,
                installed_delta=UNAVAILABLE,
                residue_delta=UNAVAILABLE,
            )
        residue = _residue_projection((*repository.rows, *installed.rows))
        repository_delta = inventory_row_delta_count(
            self.pre_snapshot.repository.rows,
            repository.rows,
        )
        installed_delta = inventory_row_delta_count(
            self.pre_snapshot.installed.rows,
            installed.rows,
        )
        residue_delta = inventory_row_delta_count(self.pre_snapshot.residue, residue)
        post_state = (
            "exact_equal"
            if repository_delta == installed_delta == residue_delta == 0
            else "exact_drift"
        )
        return self._raw_observation(
            post_state=post_state,
            repository_delta=repository_delta,
            installed_delta=installed_delta,
            residue_delta=residue_delta,
        )


def _load_parent_api(repository_root: Path) -> ModuleType:
    path = repository_root / HARNESS_PATH
    spec = importlib.util.spec_from_file_location("_r0_direct_preflight_parent", path)
    if spec is None or spec.loader is None:
        raise PreflightFailure
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(spec.name, None)
        raise PreflightFailure from exc
    return module


def _public_bindings(repository_root: Path) -> PublicBindingSnapshot:
    expected = {
        EXECUTOR_CONTRACT_PATH: EXECUTOR_CONTRACT_SHA256,
        EXECUTOR_REVIEW_PATH: EXECUTOR_CONTRACT_REVIEW_SHA256,
        EXECUTOR_LOCAL_EFFECT_REVIEW_PATH: EXECUTOR_LOCAL_EFFECT_REVIEW_SHA256,
        EXECUTOR_PREDECESSOR_REVIEW_PATH: EXECUTOR_PREDECESSOR_REVIEW_SHA256,
        EXECUTOR_IMPLEMENTATION_REVIEW_PATH: EXECUTOR_IMPLEMENTATION_REVIEW_SHA256,
        PARENT_CONTRACT_PATH: PARENT_CONTRACT_SHA256,
        PARENT_REVIEW_PATH: PARENT_REVIEW_SHA256,
        HARNESS_PATH: HARNESS_SHA256,
        HARNESS_TEST_PATH: HARNESS_TEST_SHA256,
        EXECUTOR_TEST_PATH: EXECUTOR_TEST_SHA256,
    }
    exact = True
    for relative_path, digest in expected.items():
        try:
            exact = _stable_file_sha256(repository_root / relative_path) == digest and exact
        except (OSError, PreflightFailure):
            exact = False
    executor_sha = _stable_file_sha256(repository_root / EXECUTOR_PATH)
    executor_test_sha = _stable_file_sha256(repository_root / EXECUTOR_TEST_PATH)
    parent_api = (
        _load_parent_api(repository_root)
        if exact
        else ModuleType("_unloaded_r0_direct_preflight_parent")
    )
    return PublicBindingSnapshot(exact, executor_sha, executor_test_sha, parent_api)


def _fixed_environment() -> tuple[tuple[str, str], ...]:
    selected: list[tuple[str, str]] = []
    seen: set[str] = set()
    for name in ("SystemRoot", "WINDIR"):
        matches = [(key, value) for key, value in os.environ.items() if key.casefold() == name.casefold()]
        if len(matches) != 1 or not matches[0][1]:
            raise PreflightFailure
        canonical = name
        if canonical.casefold() in seen:
            raise PreflightFailure
        seen.add(canonical.casefold())
        selected.append((canonical, matches[0][1]))
    selected.extend(
        (
            ("PYTHONDONTWRITEBYTECODE", "1"),
            ("PYTHONNOUSERSITE", "1"),
            ("PYTHONUTF8", "1"),
        )
    )
    if len({name.casefold() for name, _ in selected}) != len(selected):
        raise PreflightFailure
    return tuple(selected)


def windows_quote_argument(argument: str) -> str:
    """Quote one argument according to CommandLineToArgvW-compatible rules."""

    if argument and not any(character in " \t\n\v\"" for character in argument):
        return argument
    output = ['"']
    backslashes = 0
    for character in argument:
        if character == "\\":
            backslashes += 1
            continue
        if character == '"':
            output.append("\\" * (backslashes * 2 + 1))
            output.append('"')
            backslashes = 0
            continue
        output.append("\\" * backslashes)
        backslashes = 0
        output.append(character)
    output.append("\\" * (backslashes * 2))
    output.append('"')
    return "".join(output)


def fixed_command_line(path: Path) -> str:
    return " ".join(windows_quote_argument(value) for value in (os.fspath(path), *FIXED_ARGUMENTS))


def _build_request(
    path: Path,
    repository_root: Path,
    selection: AmbientJobSelection,
) -> FixedLaunchRequest:
    if not path.is_absolute() or path.name != "python.exe":
        raise PreflightFailure
    return FixedLaunchRequest(
        application_path=path,
        arguments=FIXED_ARGUMENTS,
        repository_root=repository_root,
        environment=_fixed_environment(),
        creation_flags=selection.creation_flags,
        timeout_seconds=TIMEOUT_SECONDS,
    )


def execute_preflight(
    private_interpreter_path: Path,
    *,
    adapter: DirectWindowsPreflightAdapter | None = None,
) -> Mapping[str, object]:
    """Execute the one fixed preflight through production or a fake adapter."""

    repository_root = Path(__file__).absolute().parent.parent
    runtime: DirectWindowsPreflightAdapter = (
        CtypesDirectWindowsPreflightAdapter() if adapter is None else adapter
    )
    effects = runtime.begin_local_effect_observation(repository_root)
    bindings = runtime.validate_public_bindings(repository_root)
    return _execute_with_validated_bindings(
        private_interpreter_path,
        runtime,
        bindings,
        repository_root,
        effects,
    )


def _execute_with_validated_bindings(
    private_interpreter_path: Path,
    runtime: DirectWindowsPreflightAdapter,
    bindings: PublicBindingSnapshot,
    repository_root: Path,
    effects: LocalEffectMonitor,
    terminal_tracker: _TerminalBoundaryTracker | None = None,
) -> Mapping[str, object]:
    observed_at = runtime.observed_at_utc()
    if not bindings.exact:
        record = _empty_record(
            public="rejected",
            owner="not_observed",
            private="not_observed",
            ambient="not_observed",
        )
        observation = effects.observe_early_terminal()
        if observation.pre_inventory_state != "not_started":
            raise LocalEffectEvidenceError
        return seal_result(source_record_from_process(record, observation), bindings, observed_at)
    if effects.observe_pre(bindings.parent_api) != "exact":
        raise LocalEffectEvidenceError
    try:
        if not isinstance(private_interpreter_path, Path):
            raise PreflightFailure
        runtime.validate_private_binding(private_interpreter_path, bindings.parent_api)
        runtime.revalidate_private_binding(private_interpreter_path, bindings.parent_api)
    except Exception:
        record = _empty_record(
            public="exact",
            owner="exact",
            private="rejected",
            ambient="not_observed",
        )
        observation = effects.observe_early_terminal()
        if observation.pre_inventory_state != "exact":
            raise LocalEffectEvidenceError from None
        return seal_result(source_record_from_process(record, observation), bindings, observed_at)
    selection = select_ambient_job(runtime.observe_ambient_job())
    if not selection.admitted:
        record = _empty_record(
            public="exact",
            owner="exact",
            private="exact",
            ambient="rejected",
        )
        observation = effects.observe_early_terminal()
        if observation.pre_inventory_state != "exact":
            raise LocalEffectEvidenceError
        return seal_result(source_record_from_process(record, observation), bindings, observed_at)
    try:
        request = _build_request(private_interpreter_path, repository_root, selection)
        effects.enter_effect_boundary()
        if terminal_tracker is None:
            process_record = runtime.execute_once(request, selection, bindings.parent_api)
        else:
            process_record = runtime.execute_once(
                request,
                selection,
                bindings.parent_api,
                terminal_tracker,
            )
    except Exception as exc:
        try:
            derive_local_effects(effects.observe_post_terminal())
        except Exception:
            pass
        raise ResultProjectionError from exc
    observation = effects.observe_post_terminal()
    record = source_record_from_process(process_record, observation)
    if (
        record.public_binding_state != "exact"
        or record.owner_decision_state != "exact"
        or record.private_binding_state != "exact"
        or record.ambient_job_state != "admitted"
    ):
        raise ResultProjectionError
    return seal_result(record, bindings, observed_at)


def parse_private_path_stdin(stream: BinaryIO) -> Path:
    buffer = bytearray(stream.read(MAX_PRIVATE_PATH_BYTES + 1))
    try:
        if (
            not buffer
            or len(buffer) > MAX_PRIVATE_PATH_BYTES
            or buffer[:3] == b"\xef\xbb\xbf"
            or b"\x00" in buffer
            or b"\r" in buffer
            or buffer.count(b"\n") != 1
            or buffer[-1:] != b"\n"
        ):
            raise PreflightFailure
        raw = bytes(buffer[:-1])
        if not raw:
            raise PreflightFailure
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise PreflightFailure from exc
        path = Path(text)
        if not path.is_absolute() or path.name != "python.exe":
            raise PreflightFailure
        return path
    finally:
        for index in range(len(buffer)):
            buffer[index] = 0


def _write_bytes(stream: TextIO, payload: bytes) -> None:
    binary = getattr(stream, "buffer", None)
    if binary is None:
        stream.write(payload.decode("utf-8"))
    else:
        binary.write(payload)


def _exit_code(status: str) -> int:
    if status == "direct_interpreter_preflight_passed":
        return 0
    if status == "direct_interpreter_preflight_unknown":
        return 3
    if status == "direct_interpreter_preflight_descendant_observed":
        return 4
    return 2


def run(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments != ["--private-path-stdin"]:
        _write_bytes(sys.stderr, UNKNOWN_SENTINEL)
        return 3
    try:
        terminal_tracker = _TerminalBoundaryTracker()
    except Exception:
        _write_bytes(sys.stderr, UNKNOWN_SENTINEL)
        return 3
    try:
        repository_root = Path(__file__).absolute().parent.parent
        runtime = CtypesDirectWindowsPreflightAdapter()
        effects = runtime.begin_local_effect_observation(repository_root)
        bindings = runtime.validate_public_bindings(repository_root)
        if not bindings.exact:
            result = _execute_with_validated_bindings(
                Path(),
                runtime,
                bindings,
                repository_root,
                effects,
            )
            payload = canonical_bytes(result)
            parse_result(payload)
            _write_bytes(sys.stdout, payload)
            return _exit_code(cast(str, result["result_status"]))
        path = parse_private_path_stdin(sys.stdin.buffer)
        result = _execute_with_validated_bindings(
            path,
            runtime,
            bindings,
            repository_root,
            effects,
            terminal_tracker,
        )
        payload = canonical_bytes(result)
        parse_result(payload)
    except Exception:
        _write_bytes(sys.stderr, _terminal_fallback_diagnostic(terminal_tracker))
        return 3
    _write_bytes(sys.stdout, payload)
    return _exit_code(cast(str, result["result_status"]))


# The Win32 implementation is below the pure contract kernel so importing this
# module for synthetic tests performs no process or operating-system action.


class CtypesDirectWindowsPreflightAdapter:
    """Production adapter.  It is instantiated only for the real CLI path."""

    def __init__(self, kernel: _Win32Kernel | None = None) -> None:
        self._kernel = _Win32Kernel() if kernel is None else kernel

    def validate_public_bindings(self, repository_root: Path) -> PublicBindingSnapshot:
        return _public_bindings(repository_root)

    def begin_local_effect_observation(
        self,
        repository_root: Path,
    ) -> LocalEffectMonitor:
        return _ProductionLocalEffectMonitor(repository_root)

    def validate_private_binding(self, path: Path, parent_api: ModuleType) -> None:
        parent_api.validate_running_direct_interpreter(path)

    def revalidate_private_binding(self, path: Path, parent_api: ModuleType) -> None:
        metadata = parent_api._observe_windows_direct_interpreter(path)
        parent_api.validate_direct_interpreter_metadata(metadata)

    def observe_ambient_job(self) -> AmbientJobObservation:
        return self._kernel.observe_ambient_job()

    def execute_once(
        self,
        request: FixedLaunchRequest,
        selection: AmbientJobSelection,
        parent_api: ModuleType,
        terminal_tracker: _TerminalBoundaryTracker | None = None,
    ) -> ProcessRecord:
        return self._kernel.execute_once(
            request,
            selection,
            parent_api,
            terminal_tracker,
        )

    def observed_at_utc(self) -> str:
        return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


HANDLE_FLAG_INHERIT = 0x00000001
STARTF_USESTDHANDLES = 0x00000100
PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002
JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 0x00000008
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
JOB_OBJECT_LIMIT_BREAKAWAY_OK = 0x00000800
JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK = 0x00001000
JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT = 3
JOB_OBJECT_MSG_NEW_PROCESS = 6
JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO = 4
JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION_CLASS = 1
JOB_OBJECT_BASIC_UI_RESTRICTIONS_CLASS = 4
JOB_OBJECT_ASSOCIATE_COMPLETION_PORT_INFORMATION_CLASS = 7
JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS = 9
WAIT_OBJECT_0 = 0
WAIT_TIMEOUT = 258
ERROR_BROKEN_PIPE = 109
STILL_ACTIVE = 259


class _SecurityAttributes(ctypes.Structure):
    _fields_ = (
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", wintypes.LPVOID),
        ("bInheritHandle", wintypes.BOOL),
    )


class _StartupInfoW(ctypes.Structure):
    _fields_ = (
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_ubyte)),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    )


class _StartupInfoExW(ctypes.Structure):
    _fields_ = (
        ("StartupInfo", _StartupInfoW),
        ("lpAttributeList", wintypes.LPVOID),
    )


class _ProcessInformation(ctypes.Structure):
    _fields_ = (
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    )


class _IoCounters(ctypes.Structure):
    _fields_ = tuple((name, ctypes.c_ulonglong) for name in (
        "ReadOperationCount",
        "WriteOperationCount",
        "OtherOperationCount",
        "ReadTransferCount",
        "WriteTransferCount",
        "OtherTransferCount",
    ))


class _JobBasicLimitInformation(ctypes.Structure):
    _fields_ = (
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    )


class _JobExtendedLimitInformation(ctypes.Structure):
    _fields_ = (
        ("BasicLimitInformation", _JobBasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    )


class _JobAssociateCompletionPort(ctypes.Structure):
    _fields_ = (
        ("CompletionKey", wintypes.LPVOID),
        ("CompletionPort", wintypes.HANDLE),
    )


class _JobBasicUiRestrictions(ctypes.Structure):
    _fields_ = (("UIRestrictionsClass", wintypes.DWORD),)


class _JobBasicAccountingInformation(ctypes.Structure):
    _fields_ = (
        ("TotalUserTime", ctypes.c_longlong),
        ("TotalKernelTime", ctypes.c_longlong),
        ("ThisPeriodTotalUserTime", ctypes.c_longlong),
        ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
        ("TotalPageFaultCount", wintypes.DWORD),
        ("TotalProcesses", wintypes.DWORD),
        ("ActiveProcesses", wintypes.DWORD),
        ("TotalTerminatedProcesses", wintypes.DWORD),
    )


class _ProcessBasicInformation(ctypes.Structure):
    _fields_ = (
        ("Reserved1", wintypes.LPVOID),
        ("PebBaseAddress", wintypes.LPVOID),
        ("Reserved2_0", wintypes.LPVOID),
        ("Reserved2_1", wintypes.LPVOID),
        ("UniqueProcessId", ctypes.c_size_t),
        ("InheritedFromUniqueProcessId", ctypes.c_size_t),
    )


class _OwnedHandle:
    def __init__(self, kernel32: ctypes.WinDLL, value: int | None) -> None:
        self._kernel32 = kernel32
        self.value = value
        self.close_ok = True

    @property
    def open(self) -> bool:
        return self.value not in (None, 0, -1, ctypes.c_void_p(-1).value)

    def close(self) -> bool:
        if not self.open:
            return self.close_ok
        value = self.value
        self.value = None
        self.close_ok = bool(self._kernel32.CloseHandle(wintypes.HANDLE(value)))
        return self.close_ok


class _OwnedAttributeList:
    def __init__(self, kernel32: ctypes.WinDLL) -> None:
        self._kernel32 = kernel32
        self.buffer: ctypes.Array[ctypes.c_char] | None = None
        self.pointer: wintypes.LPVOID | None = None
        self.initialized = False
        self.close_ok = True

    def initialize(self) -> wintypes.LPVOID:
        if self.buffer is not None or self.pointer is not None or self.initialized:
            raise PreflightFailure
        size = ctypes.c_size_t()
        self._kernel32.InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(size))
        if size.value == 0:
            raise PreflightFailure
        self.buffer = ctypes.create_string_buffer(size.value)
        pointer = ctypes.cast(self.buffer, wintypes.LPVOID)
        if not self._kernel32.InitializeProcThreadAttributeList(
            pointer,
            1,
            0,
            ctypes.byref(size),
        ):
            raise PreflightFailure
        self.pointer = pointer
        self.initialized = True
        return pointer

    def close(self) -> bool:
        if not self.initialized:
            return self.close_ok
        pointer = self.pointer
        self.initialized = False
        self.pointer = None
        try:
            self._kernel32.DeleteProcThreadAttributeList(pointer)
        except Exception:
            self.close_ok = False
        return self.close_ok


def _kernel32() -> ctypes.WinDLL:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.IsProcessInJob.argtypes = (
        wintypes.HANDLE,
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.BOOL),
    )
    kernel32.IsProcessInJob.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.CreatePipe.argtypes = (
        ctypes.POINTER(wintypes.HANDLE),
        ctypes.POINTER(wintypes.HANDLE),
        ctypes.POINTER(_SecurityAttributes),
        wintypes.DWORD,
    )
    kernel32.CreatePipe.restype = wintypes.BOOL
    kernel32.SetHandleInformation.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.DWORD,
    )
    kernel32.SetHandleInformation.restype = wintypes.BOOL
    kernel32.GetHandleInformation.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.GetHandleInformation.restype = wintypes.BOOL
    kernel32.CreateJobObjectW.argtypes = (ctypes.POINTER(_SecurityAttributes), wintypes.LPCWSTR)
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
    )
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.CreateIoCompletionPort.argtypes = (
        wintypes.HANDLE,
        wintypes.HANDLE,
        ctypes.c_size_t,
        wintypes.DWORD,
    )
    kernel32.CreateIoCompletionPort.restype = wintypes.HANDLE
    kernel32.InitializeProcThreadAttributeList.argtypes = (
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.c_size_t),
    )
    kernel32.InitializeProcThreadAttributeList.restype = wintypes.BOOL
    kernel32.UpdateProcThreadAttribute.argtypes = (
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.c_size_t,
        wintypes.LPVOID,
        ctypes.c_size_t,
        wintypes.LPVOID,
        ctypes.POINTER(ctypes.c_size_t),
    )
    kernel32.UpdateProcThreadAttribute.restype = wintypes.BOOL
    kernel32.DeleteProcThreadAttributeList.argtypes = (wintypes.LPVOID,)
    kernel32.CreateProcessW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        ctypes.POINTER(_SecurityAttributes),
        ctypes.POINTER(_SecurityAttributes),
        wintypes.BOOL,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.LPCWSTR,
        ctypes.POINTER(_StartupInfoW),
        ctypes.POINTER(_ProcessInformation),
    )
    kernel32.CreateProcessW.restype = wintypes.BOOL
    kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.QueryFullProcessImageNameW.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
    kernel32.ResumeThread.argtypes = (wintypes.HANDLE,)
    kernel32.ResumeThread.restype = wintypes.DWORD
    kernel32.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.TerminateProcess.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateProcess.restype = wintypes.BOOL
    kernel32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.PeekNamedPipe.argtypes = (
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.POINTER(wintypes.DWORD),
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.PeekNamedPipe.restype = wintypes.BOOL
    kernel32.ReadFile.argtypes = (
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    )
    kernel32.ReadFile.restype = wintypes.BOOL
    kernel32.GetQueuedCompletionStatus.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.POINTER(wintypes.LPVOID),
        wintypes.DWORD,
    )
    kernel32.GetQueuedCompletionStatus.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


def _observe_ambient_job_ctypes() -> AmbientJobObservation:
    kernel32 = _kernel32()
    in_job = wintypes.BOOL()
    if not kernel32.IsProcessInJob(kernel32.GetCurrentProcess(), None, ctypes.byref(in_job)):
        return AmbientJobObservation(False, None)
    if not bool(in_job.value):
        return AmbientJobObservation(True, False)
    limits = _JobExtendedLimitInformation()
    limit_length = wintypes.DWORD()
    limit_ok = bool(
        kernel32.QueryInformationJobObject(
            None,
            JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
            ctypes.byref(limit_length),
        )
    ) and limit_length.value == ctypes.sizeof(limits)
    ui = _JobBasicUiRestrictions()
    ui_length = wintypes.DWORD()
    ui_ok = bool(
        kernel32.QueryInformationJobObject(
            None,
            JOB_OBJECT_BASIC_UI_RESTRICTIONS_CLASS,
            ctypes.byref(ui),
            ctypes.sizeof(ui),
            ctypes.byref(ui_length),
        )
    ) and ui_length.value == ctypes.sizeof(ui)
    try:
        version = sys.getwindowsversion()
        nested = (version.major, version.minor) >= (6, 2)
        version_exact = True
    except Exception:
        nested = False
        version_exact = False
    flags = int(limits.BasicLimitInformation.LimitFlags) if limit_ok else 0
    return AmbientJobObservation(
        membership_api_exact=True,
        in_job=True,
        extended_query_exact=limit_ok,
        ui_query_exact=ui_ok,
        version_query_exact=version_exact,
        silent_breakaway=bool(flags & JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK),
        breakaway=bool(flags & JOB_OBJECT_LIMIT_BREAKAWAY_OK),
        nested_jobs_supported=nested,
        ui_restrictions_class=int(ui.UIRestrictionsClass) if ui_ok else None,
    )


def _create_pipe_pair(
    kernel32: ctypes.WinDLL,
    security: _SecurityAttributes,
) -> tuple[_OwnedHandle, _OwnedHandle]:
    read_handle = wintypes.HANDLE()
    write_handle = wintypes.HANDLE()
    if not kernel32.CreatePipe(
        ctypes.byref(read_handle),
        ctypes.byref(write_handle),
        ctypes.byref(security),
        0,
    ):
        raise PreflightFailure
    return (
        _OwnedHandle(kernel32, cast(int, read_handle.value)),
        _OwnedHandle(kernel32, cast(int, write_handle.value)),
    )


def _set_and_verify_pipe_inheritance(
    kernel32: ctypes.WinDLL,
    handles: Mapping[str, _OwnedHandle],
) -> None:
    for name in ("stdin_write", "stdout_read", "stderr_read"):
        handle = handles[name]
        if not kernel32.SetHandleInformation(
            wintypes.HANDLE(handle.value),
            HANDLE_FLAG_INHERIT,
            0,
        ):
            raise PreflightFailure
    inheritable = {"stdin_read", "stdout_write", "stderr_write"}
    for name, handle in handles.items():
        flags = wintypes.DWORD()
        if not handle.open or not kernel32.GetHandleInformation(
            wintypes.HANDLE(handle.value), ctypes.byref(flags)
        ):
            raise PreflightFailure
        if bool(flags.value & HANDLE_FLAG_INHERIT) != (name in inheritable):
            raise PreflightFailure


def _query_job_active_processes(kernel32: ctypes.WinDLL, job: _OwnedHandle) -> int:
    accounting = _JobBasicAccountingInformation()
    returned = wintypes.DWORD()
    if not kernel32.QueryInformationJobObject(
        wintypes.HANDLE(job.value),
        JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION_CLASS,
        ctypes.byref(accounting),
        ctypes.sizeof(accounting),
        ctypes.byref(returned),
    ) or returned.value != ctypes.sizeof(accounting):
        raise PreflightFailure
    return int(accounting.ActiveProcesses)


def _query_process_image(kernel32: ctypes.WinDLL, process: _OwnedHandle) -> str:
    capacity = 32768
    buffer = ctypes.create_unicode_buffer(capacity)
    size = wintypes.DWORD(capacity)
    if not kernel32.QueryFullProcessImageNameW(
        wintypes.HANDLE(process.value), 0, buffer, ctypes.byref(size)
    ):
        raise PreflightFailure
    return buffer.value[: size.value]


def _query_parent_process_id(process: _OwnedHandle) -> int:
    ntdll = ctypes.WinDLL("ntdll", use_last_error=True)
    ntdll.NtQueryInformationProcess.argtypes = (
        wintypes.HANDLE,
        wintypes.ULONG,
        wintypes.LPVOID,
        wintypes.ULONG,
        ctypes.POINTER(wintypes.ULONG),
    )
    ntdll.NtQueryInformationProcess.restype = ctypes.c_long
    information = _ProcessBasicInformation()
    returned = wintypes.ULONG()
    status = ntdll.NtQueryInformationProcess(
        wintypes.HANDLE(process.value),
        0,
        ctypes.byref(information),
        ctypes.sizeof(information),
        ctypes.byref(returned),
    )
    if status != 0 or returned.value != ctypes.sizeof(information):
        raise PreflightFailure
    return int(information.InheritedFromUniqueProcessId)


def _read_available(
    kernel32: ctypes.WinDLL,
    handle: _OwnedHandle,
    retained: bytearray,
) -> bool:
    available = wintypes.DWORD()
    if not kernel32.PeekNamedPipe(
        wintypes.HANDLE(handle.value),
        None,
        0,
        None,
        ctypes.byref(available),
        None,
    ):
        if ctypes.get_last_error() == ERROR_BROKEN_PIPE:
            return True
        return False
    while available.value:
        requested = min(int(available.value), MAX_OUTPUT_BYTES + 1 - len(retained), 4096)
        if requested <= 0:
            return False
        buffer = ctypes.create_string_buffer(requested)
        received = wintypes.DWORD()
        if not kernel32.ReadFile(
            wintypes.HANDLE(handle.value),
            buffer,
            requested,
            ctypes.byref(received),
            None,
        ):
            if ctypes.get_last_error() == ERROR_BROKEN_PIPE:
                return True
            return False
        retained.extend(buffer.raw[: received.value])
        if len(retained) > MAX_OUTPUT_BYTES:
            del retained[MAX_OUTPUT_BYTES:]
            return False
        available = wintypes.DWORD()
        if not kernel32.PeekNamedPipe(
            wintypes.HANDLE(handle.value),
            None,
            0,
            None,
            ctypes.byref(available),
            None,
        ):
            return ctypes.get_last_error() == ERROR_BROKEN_PIPE
    return True


def _drain_completion_port(
    kernel32: ctypes.WinDLL,
    port: _OwnedHandle,
    target_pid: int,
    descendant_process_ids: set[int],
    active_limit_seen: bool,
) -> tuple[bool, bool]:
    zero_seen = False
    while True:
        message = wintypes.DWORD()
        key = ctypes.c_size_t()
        overlapped = wintypes.LPVOID()
        ok = kernel32.GetQueuedCompletionStatus(
            wintypes.HANDLE(port.value),
            ctypes.byref(message),
            ctypes.byref(key),
            ctypes.byref(overlapped),
            0,
        )
        if not ok:
            if ctypes.get_last_error() == WAIT_TIMEOUT:
                break
            raise PreflightFailure
        process_id = ctypes.cast(overlapped, ctypes.c_void_p).value or 0
        if message.value == JOB_OBJECT_MSG_NEW_PROCESS and process_id != target_pid:
            descendant_process_ids.add(process_id)
        elif message.value == JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT:
            active_limit_seen = True
        elif message.value == JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO:
            zero_seen = True
    return active_limit_seen, zero_seen


def _environment_block(environment: Sequence[tuple[str, str]]) -> ctypes.Array[ctypes.c_wchar]:
    if len({name.casefold() for name, _ in environment}) != len(environment):
        raise PreflightFailure
    text = "\0".join(
        f"{name}={value}" for name, value in sorted(environment, key=lambda item: item[0].casefold())
    ) + "\0\0"
    return ctypes.create_unicode_buffer(text)


def _close_all(handles: Mapping[str, _OwnedHandle]) -> bool:
    all_closed = True
    for handle in reversed(tuple(handles.values())):
        try:
            closed = handle.close()
        except Exception:
            closed = False
        all_closed = bool(closed) and all_closed
    return all_closed


def _setup_failure_record(cleanup_confirmed: bool) -> ProcessRecord:
    return _empty_record(
        public="exact",
        owner="exact",
        private="exact",
        ambient="admitted",
        setup="failed_no_process",
        cleanup_confirmed=cleanup_confirmed,
    )


def _create_failure_record() -> ProcessRecord:
    return ProcessRecord(
        historical_direct_use_proven=False,
        public_binding_state="exact",
        owner_decision_state="exact",
        private_binding_state="exact",
        ambient_job_state="admitted",
        precreate_setup_state="complete",
        create_call_entered=True,
        create_return_state="failed_no_process",
        top_level_identity_exact=False,
        parentage_known=False,
        exit_status="not_started",
        stdout_byte_count=0,
        stderr_byte_count=0,
        top_level_process_count=0,
        descendant_process_count=0,
        descendant_attempt_detected=False,
        timed_out=False,
        cleanup_confirmed=True,
        output_complete=True,
    )


def _execute_win32_once(
    request: FixedLaunchRequest,
    selection: AmbientJobSelection,
    parent_api: ModuleType,
    terminal_tracker: _TerminalBoundaryTracker | None = None,
) -> ProcessRecord:
    if selection.creation_flags != request.creation_flags or not selection.admitted:
        raise PreflightFailure
    if request.arguments != FIXED_ARGUMENTS or request.inherited_streams != (
        "stdin_read",
        "stdout_write",
        "stderr_write",
    ):
        raise PreflightFailure
    kernel32 = _kernel32()
    handles: dict[str, _OwnedHandle] = {}
    attribute_owner = _OwnedAttributeList(kernel32)
    process_information = _ProcessInformation()
    events: list[str] = []
    create_entered = False
    create_return_known = False
    created = False
    assigned = False
    resumed = False
    identity_exact = False
    parentage_known = False
    try:
        security = _SecurityAttributes(
            ctypes.sizeof(_SecurityAttributes),
            None,
            True,
        )
        handles["stdin_read"], handles["stdin_write"] = _create_pipe_pair(kernel32, security)
        events.append("stdin_pipe_created")
        handles["stdout_read"], handles["stdout_write"] = _create_pipe_pair(kernel32, security)
        events.append("stdout_pipe_created")
        handles["stderr_read"], handles["stderr_write"] = _create_pipe_pair(kernel32, security)
        events.append("stderr_pipe_created")
        _set_and_verify_pipe_inheritance(kernel32, handles)
        events.append("six_handles_validated")

        handles["job"] = _OwnedHandle(kernel32, cast(int, kernel32.CreateJobObjectW(None, None)))
        if not handles["job"].open:
            raise PreflightFailure
        events.append("job_created")
        limits = _JobExtendedLimitInformation()
        limits.BasicLimitInformation.LimitFlags = (
            JOB_OBJECT_LIMIT_ACTIVE_PROCESS | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        )
        limits.BasicLimitInformation.ActiveProcessLimit = 1
        if not kernel32.SetInformationJobObject(
            wintypes.HANDLE(handles["job"].value),
            JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            raise PreflightFailure
        events.append("job_limits_set")

        invalid_handle = wintypes.HANDLE(ctypes.c_void_p(-1).value)
        handles["completion_port"] = _OwnedHandle(
            kernel32,
            cast(int, kernel32.CreateIoCompletionPort(invalid_handle, None, 0, 1)),
        )
        if not handles["completion_port"].open:
            raise PreflightFailure
        association = _JobAssociateCompletionPort(
            None,
            wintypes.HANDLE(handles["completion_port"].value),
        )
        if not kernel32.SetInformationJobObject(
            wintypes.HANDLE(handles["job"].value),
            JOB_OBJECT_ASSOCIATE_COMPLETION_PORT_INFORMATION_CLASS,
            ctypes.byref(association),
            ctypes.sizeof(association),
        ):
            raise PreflightFailure
        events.append("completion_port_attached")

        attribute_list = attribute_owner.initialize()
        events.append("handle_list_set")
        inherited_values = (wintypes.HANDLE * 3)(
            wintypes.HANDLE(handles["stdin_read"].value),
            wintypes.HANDLE(handles["stdout_write"].value),
            wintypes.HANDLE(handles["stderr_write"].value),
        )
        if not kernel32.UpdateProcThreadAttribute(
            attribute_list,
            0,
            PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
            ctypes.byref(inherited_values),
            ctypes.sizeof(inherited_values),
            None,
            None,
        ):
            raise PreflightFailure

        startup = _StartupInfoExW()
        startup.StartupInfo.cb = ctypes.sizeof(startup)
        startup.StartupInfo.dwFlags = STARTF_USESTDHANDLES
        startup.StartupInfo.hStdInput = wintypes.HANDLE(handles["stdin_read"].value)
        startup.StartupInfo.hStdOutput = wintypes.HANDLE(handles["stdout_write"].value)
        startup.StartupInfo.hStdError = wintypes.HANDLE(handles["stderr_write"].value)
        startup.lpAttributeList = attribute_list
        if not handles["stdin_write"].close():
            raise PreflightFailure
        events.append("stdin_writer_closed")

        command_line = ctypes.create_unicode_buffer(fixed_command_line(request.application_path))
        environment = _environment_block(request.environment)
        create_entered = True
        events.append("create_entered")
        if terminal_tracker is not None:
            terminal_tracker.mark_create_entered()
        create_result = kernel32.CreateProcessW(
                os.fspath(request.application_path),
                command_line,
                None,
                None,
                True,
                request.creation_flags,
                ctypes.cast(environment, wintypes.LPVOID),
                os.fspath(request.repository_root),
                ctypes.cast(ctypes.byref(startup), ctypes.POINTER(_StartupInfoW)),
                ctypes.byref(process_information),
            )
        create_return_known = True
        created = bool(create_result)
        if created:
            handles["process"] = _OwnedHandle(kernel32, cast(int, process_information.hProcess))
            handles["thread"] = _OwnedHandle(kernel32, cast(int, process_information.hThread))
        if not attribute_owner.close():
            raise PreflightFailure
        if not created:
            if not _close_all(handles):
                raise ResultProjectionError
            return _create_failure_record()
        events.append("create_succeeded")
        for inherited_name in ("stdin_read", "stdout_write", "stderr_write"):
            if not handles[inherited_name].close():
                raise PreflightFailure
        events.append("parent_inherited_handles_closed")

        assigned = bool(
            kernel32.AssignProcessToJobObject(
                wintypes.HANDLE(handles["job"].value),
                wintypes.HANDLE(handles["process"].value),
            )
        )
        if assigned:
            events.append("job_assigned")
        active_before_resume = _query_job_active_processes(kernel32, handles["job"])
        if active_before_resume == 1:
            events.append("one_process_readback")
        image_before = _query_process_image(kernel32, handles["process"])
        image_exact_before = os.path.normcase(image_before) == os.path.normcase(
            os.fspath(request.application_path)
        )
        if image_exact_before:
            events.append("image_validated")
        parentage_known = _query_parent_process_id(handles["process"]) == os.getpid()
        if parentage_known:
            events.append("parentage_validated")
        prelaunch_identity = parent_api._observe_windows_direct_interpreter(
            request.application_path
        )
        parent_api.validate_direct_interpreter_metadata(prelaunch_identity)
        if not assigned or active_before_resume != 1 or not image_exact_before or not parentage_known:
            raise PreflightFailure
        if kernel32.ResumeThread(wintypes.HANDLE(handles["thread"].value)) == 0xFFFFFFFF:
            raise PreflightFailure
        resumed = True
        events.append("resumed_once")

        stdout = bytearray()
        stderr = bytearray()
        output_complete = True
        descendant_process_ids: set[int] = set()
        active_limit_seen = False
        accounting_violation_seen = False
        timed_out = False
        deadline = time.monotonic() + request.timeout_seconds
        termination_deadline: float | None = None
        termination_requested = False
        process_exited = False
        while not process_exited:
            wait = kernel32.WaitForSingleObject(wintypes.HANDLE(handles["process"].value), 10)
            if wait == WAIT_OBJECT_0:
                process_exited = True
            elif wait != WAIT_TIMEOUT:
                raise PreflightFailure
            output_complete = (
                _read_available(kernel32, handles["stdout_read"], stdout)
                and _read_available(kernel32, handles["stderr_read"], stderr)
                and output_complete
            )
            active_limit_seen, _ = _drain_completion_port(
                kernel32,
                handles["completion_port"],
                int(process_information.dwProcessId),
                descendant_process_ids,
                active_limit_seen,
            )
            active = _query_job_active_processes(kernel32, handles["job"])
            if active > 1:
                accounting_violation_seen = True
            descendant_count = (
                len(descendant_process_ids)
                + int(active_limit_seen)
                + int(accounting_violation_seen)
            )
            now = time.monotonic()
            if not output_complete or descendant_count or now >= deadline:
                timed_out = now >= deadline
                if not termination_requested:
                    termination_requested = True
                    termination_deadline = now + 5
                    kernel32.TerminateJobObject(wintypes.HANDLE(handles["job"].value), 1)
            if termination_deadline is not None and now >= termination_deadline:
                break
        events.append("terminal_observed")

        output_complete = (
            _read_available(kernel32, handles["stdout_read"], stdout)
            and _read_available(kernel32, handles["stderr_read"], stderr)
            and output_complete
        )
        events.append("streams_drained")
        active_limit_seen, _ = _drain_completion_port(
            kernel32,
            handles["completion_port"],
            int(process_information.dwProcessId),
            descendant_process_ids,
            active_limit_seen,
        )
        descendant_count = (
            len(descendant_process_ids)
            + int(active_limit_seen)
            + int(accounting_violation_seen)
        )
        exit_code = wintypes.DWORD(STILL_ACTIVE)
        exit_known = bool(
            kernel32.GetExitCodeProcess(
                wintypes.HANDLE(handles["process"].value), ctypes.byref(exit_code)
            )
        ) and exit_code.value != STILL_ACTIVE
        try:
            image_after = _query_process_image(kernel32, handles["process"])
            postlaunch_identity = parent_api._observe_windows_direct_interpreter(
                request.application_path
            )
            parent_api.validate_direct_interpreter_metadata(postlaunch_identity)
            identity_exact = (
                image_exact_before
                and os.path.normcase(image_after) == os.path.normcase(os.fspath(request.application_path))
                and prelaunch_identity == postlaunch_identity
            )
            if identity_exact:
                events.append("post_exit_identity_validated")
        except Exception:
            identity_exact = False
        active_zero = _query_job_active_processes(kernel32, handles["job"]) == 0
        if active_zero:
            events.append("active_zero")
        process_stopped = (
            kernel32.WaitForSingleObject(wintypes.HANDLE(handles["process"].value), 0)
            == WAIT_OBJECT_0
        )
        close_ok = _close_all(handles)
        if close_ok:
            events.append("all_handles_closed")
        cleanup_confirmed = active_zero and process_stopped and close_ok
        if cleanup_confirmed and identity_exact and parentage_known:
            validate_success_lifecycle_trace(events)
        return ProcessRecord(
            historical_direct_use_proven=False,
            public_binding_state="exact",
            owner_decision_state="exact",
            private_binding_state="exact",
            ambient_job_state="admitted",
            precreate_setup_state="complete",
            create_call_entered=True,
            create_return_state="succeeded_one_process",
            top_level_identity_exact=identity_exact,
            parentage_known=parentage_known,
            exit_status=(
                "unknown" if not exit_known else ("zero" if exit_code.value == 0 else "nonzero")
            ),
            stdout_byte_count=len(stdout),
            stderr_byte_count=len(stderr),
            top_level_process_count=1,
            descendant_process_count=descendant_count,
            descendant_attempt_detected=descendant_count > 0,
            timed_out=timed_out,
            cleanup_confirmed=cleanup_confirmed,
            output_complete=output_complete,
        )
    except Exception as exc:
        attribute_cleanup = attribute_owner.close()
        if created and "process" in handles and handles["process"].open:
            if assigned and "job" in handles and handles["job"].open:
                kernel32.TerminateJobObject(wintypes.HANDLE(handles["job"].value), 1)
            else:
                kernel32.TerminateProcess(wintypes.HANDLE(handles["process"].value), 1)
            kernel32.WaitForSingleObject(wintypes.HANDLE(handles["process"].value), 5000)
        process_stopped = (
            created
            and "process" in handles
            and handles["process"].open
            and kernel32.WaitForSingleObject(wintypes.HANDLE(handles["process"].value), 0)
            == WAIT_OBJECT_0
        )
        try:
            active_zero = (
                not assigned
                or "job" not in handles
                or not handles["job"].open
                or _query_job_active_processes(kernel32, handles["job"]) == 0
            )
        except Exception:
            active_zero = False
        cleanup = _close_all(handles) and attribute_cleanup
        if not create_entered:
            return _setup_failure_record(cleanup)
        if create_return_known and not created and cleanup:
            return _create_failure_record()
        if created and not resumed:
            return ProcessRecord(
                historical_direct_use_proven=False,
                public_binding_state="exact",
                owner_decision_state="exact",
                private_binding_state="exact",
                ambient_job_state="admitted",
                precreate_setup_state="complete",
                create_call_entered=True,
                create_return_state="succeeded_one_process",
                top_level_identity_exact=identity_exact,
                parentage_known=parentage_known,
                exit_status="unknown",
                stdout_byte_count=0,
                stderr_byte_count=0,
                top_level_process_count=1,
                descendant_process_count=0,
                descendant_attempt_detected=False,
                timed_out=False,
                cleanup_confirmed=cleanup and process_stopped and active_zero,
                output_complete=True,
            )
        raise ResultProjectionError from exc
    finally:
        attribute_owner.close()


class _Win32Kernel:
    """Direct ctypes kernel; detailed Win32 lifecycle is defined below."""

    def __init__(self) -> None:
        if os.name != "nt" or sys.platform != "win32":
            raise PreflightFailure

    def observe_ambient_job(self) -> AmbientJobObservation:
        return _observe_ambient_job_ctypes()

    def execute_once(
        self,
        request: FixedLaunchRequest,
        selection: AmbientJobSelection,
        parent_api: ModuleType,
        terminal_tracker: _TerminalBoundaryTracker | None = None,
    ) -> ProcessRecord:
        return _execute_win32_once(
            request,
            selection,
            parent_api,
            terminal_tracker,
        )


if __name__ == "__main__":
    raise SystemExit(run())
