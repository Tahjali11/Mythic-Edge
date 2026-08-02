"""Characterize one bounded direct-interpreter identity operation.

The module is inert when executed directly.  A separately authorized executor
must first consume its owner decision, then call
``run_consumed_characterization`` with the predeclared public characterization
identifier and the dedicated private-path stdin pipe.  Synthetic tests use the
pure selector and an injected fake adapter; importing this module performs no
filesystem, process, registry, or network operation.
"""

from __future__ import annotations

import ctypes
import hashlib
import importlib.util
import itertools
import json
import ntpath
import os
import re
import stat
import sys
import time
from collections import Counter
from collections.abc import Mapping, Sequence
from ctypes import wintypes
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import BinaryIO, Protocol, cast

REPOSITORY_ID = 1235264383
ISSUE_NUMBER = 795
PARENT_ISSUE_NUMBER = 780

RESULT_SCHEMA = "trusted_owner_r0_direct_interpreter_identity_characterization.v1"
CHARACTERIZER_CONTRACT_SHA256 = (
    "42661d3f445c7d93e6253105c09d27454a96607b9acb2f7b2499290abcfda904"
)
CHARACTERIZER_CONTRACT_REVIEW_SHA256 = (
    "89ee9144a2dee459a819259f05db7b659c6dc589fc8ef635234333f0e03a2127"
)
DIRECT_INTERPRETER_BINDING_SHA256 = (
    "2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333"
)

CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_"
    "identity_characterizer.md"
)
CONTRACT_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_"
    "interpreter_identity_characterizer.md"
)
PARENT_API_PATH = Path("tools/check_role_pool_r0_offline_observation.py")
CHARACTERIZER_PATH = Path(
    "tools/run_role_pool_r0_direct_interpreter_identity_characterizer.py"
)
CHARACTERIZER_TEST_PATH = Path(
    "tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer.py"
)

FROZEN_PUBLIC_ARTIFACTS = {
    CONTRACT_PATH: CHARACTERIZER_CONTRACT_SHA256,
    CONTRACT_REVIEW_PATH: CHARACTERIZER_CONTRACT_REVIEW_SHA256,
    Path(
        "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_"
        "preflight_executor.md"
    ): "cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4",
    Path(
        "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_"
        "interpreter_preflight_terminal_fallback.md"
    ): "8fa95ada34171e0e040acea13de52a87d72138995bbcc8b6dc982fb0ecca3880",
    Path(
        "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_"
        "interpreter_preflight_terminal_fallback_implementation.md"
    ): "1e44189d09664c86539bc8e9441bfb2ef8b51199f04b7087333908d1035ac81b",
    Path(
        "tools/run_role_pool_r0_direct_interpreter_preflight.py"
    ): "429021301e9aad9958dfafae22fa98665ed75d0f80b241963cc4ecfb97ce97ed",
    Path(
        "tests/test_run_role_pool_r0_direct_interpreter_preflight.py"
    ): "435aedabf5d73e02df1cede397f937da6c44b2cecd4ee3ae21b0645bf44e490b",
    PARENT_API_PATH: "001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6",
}

FIXED_ARGUMENTS = ("-B", "-c", "pass")
MAX_PRIVATE_PATH_BYTES = 4096
MAX_OUTPUT_BYTES = 4096
PROCESS_TIMEOUT_SECONDS = 30.0
TERMINATION_GRACE_SECONDS = 5.0

LIFECYCLE_STATES = ("exact", "ambiguous")
PRELAUNCH_METADATA_STATES = ("exact", "mismatch", "unavailable", "ambiguous")
IMAGE_STATES = ("not_reached", "exact", "mismatch", "unavailable", "ambiguous")
POSTLAUNCH_METADATA_STATES = ("not_reached", "available", "unavailable", "ambiguous")
METADATA_EQUALITY_STATES = ("not_reached", "exact", "mismatch", "unavailable", "ambiguous")

AMBIGUOUS_CATEGORY = "direct_interpreter_identity_evidence_ambiguous"
PRELAUNCH_UNAVAILABLE_CATEGORY = (
    "direct_interpreter_identity_prelaunch_metadata_unavailable"
)
PRELAUNCH_MISMATCH_CATEGORY = "direct_interpreter_identity_prelaunch_metadata_mismatch"
PRE_RESUME_UNAVAILABLE_CATEGORY = (
    "direct_interpreter_identity_pre_resume_image_unavailable"
)
PRE_RESUME_MISMATCH_CATEGORY = "direct_interpreter_identity_pre_resume_image_mismatch"
POST_EXIT_UNAVAILABLE_CATEGORY = (
    "direct_interpreter_identity_post_exit_image_unavailable"
)
POST_EXIT_MISMATCH_CATEGORY = "direct_interpreter_identity_post_exit_image_mismatch"
POSTLAUNCH_UNAVAILABLE_CATEGORY = (
    "direct_interpreter_identity_postlaunch_metadata_unavailable"
)
EQUALITY_UNAVAILABLE_CATEGORY = (
    "direct_interpreter_identity_metadata_equality_unavailable"
)
EQUALITY_MISMATCH_CATEGORY = "direct_interpreter_identity_metadata_equality_mismatch"
EXACT_CATEGORY = "direct_interpreter_identity_exact"

CATEGORIES = (
    AMBIGUOUS_CATEGORY,
    PRELAUNCH_UNAVAILABLE_CATEGORY,
    PRELAUNCH_MISMATCH_CATEGORY,
    PRE_RESUME_UNAVAILABLE_CATEGORY,
    PRE_RESUME_MISMATCH_CATEGORY,
    POST_EXIT_UNAVAILABLE_CATEGORY,
    POST_EXIT_MISMATCH_CATEGORY,
    POSTLAUNCH_UNAVAILABLE_CATEGORY,
    EQUALITY_UNAVAILABLE_CATEGORY,
    EQUALITY_MISMATCH_CATEGORY,
    EXACT_CATEGORY,
)

KNOWN_FAILURE_CATEGORIES = CATEGORIES[1:-1]

RESULT_FIELDS = (
    "schema_version",
    "repository_id",
    "issue_number",
    "parent_issue_number",
    "characterizer_contract_sha256",
    "characterizer_contract_review_sha256",
    "characterizer_sha256",
    "characterizer_test_sha256",
    "direct_interpreter_binding_sha256",
    "characterization_id",
    "observed_at_utc",
    "characterization_authority_consumed",
    "lifecycle_evidence_state",
    "prelaunch_metadata_state",
    "pre_resume_image_state",
    "post_exit_image_state",
    "postlaunch_metadata_state",
    "metadata_equality_state",
    "category",
    "process_launch_count",
    "top_level_process_count",
    "descendant_process_count",
    "exit_state",
    "stdout_byte_count",
    "stderr_byte_count",
    "timed_out",
    "streams_drained",
    "cleanup_confirmed",
    "surviving_process_count",
    "private_value_emitted",
    "eligible_for_independent_review",
    "authority_flags",
    "result_sha256",
)

AUTHORITY_FIELDS = (
    "characterizer_authorized",
    "implementation_authorized",
    "private_path_access_authorized",
    "preflight_authorized",
    "observation_authorized",
    "receipt_publication_authorized",
    "release_state_mutation_authorized",
    "installation_authorized",
    "package_operations_authorized",
    "network_authorized",
    "dispatch_authorized",
    "r1_r8_authorized",
    "stage4_authorized",
    "submission_authorized",
    "merge_authorized",
    "deployment_authorized",
    "live_ready",
    "security_assurance_claimed",
)

_SAFE_CHARACTERIZATION_ID = re.compile(r"[a-z0-9][a-z0-9._-]{0,127}\Z")
_ZERO_DIGEST = "0" * 64


class CharacterizerError(RuntimeError):
    """A symbolic failure that must not carry private detail."""


class ResultValidationError(CharacterizerError):
    """A result does not satisfy the closed public schema."""


class DuplicateJsonKeyError(ResultValidationError):
    """A JSON object repeated a key."""


@dataclass(frozen=True)
class MetadataObservation:
    state: str
    value: object | None = None


@dataclass(frozen=True)
class ImageObservation:
    state: str
    value: str | None = None


@dataclass(frozen=True)
class PreResumeBoundary:
    job_assigned: bool | None
    active_process_count: int | None
    parentage_known: bool | None


@dataclass(frozen=True)
class TerminalObservation:
    exit_state: str
    stdout_byte_count: int
    stderr_byte_count: int
    timed_out: bool
    streams_drained: bool
    descendant_process_count: int
    process_stopped: bool


@dataclass(frozen=True)
class CleanupObservation:
    cleanup_confirmed: bool
    surviving_process_count: int


@dataclass(frozen=True)
class CreateSuspendedResult:
    state: str
    session: object | None
    cleanup: CleanupObservation


@dataclass(frozen=True)
class FixedLaunchRequest:
    application_path: str
    arguments: tuple[str, str, str]
    repository_root: Path
    environment: tuple[tuple[str, str], ...]
    creation_flags: int
    timeout_seconds: float
    termination_grace_seconds: float


@dataclass(frozen=True)
class PublicBindingSnapshot:
    exact: bool
    characterizer_sha256: str
    characterizer_test_sha256: str
    parent_api: ModuleType | object


@dataclass(frozen=True)
class CharacterizationRecord:
    lifecycle_evidence_state: str
    prelaunch_metadata_state: str
    pre_resume_image_state: str
    post_exit_image_state: str
    postlaunch_metadata_state: str
    metadata_equality_state: str
    process_launch_count: int
    top_level_process_count: int
    descendant_process_count: int
    exit_state: str
    stdout_byte_count: int
    stderr_byte_count: int
    timed_out: bool
    streams_drained: bool
    cleanup_confirmed: bool
    surviving_process_count: int
    private_value_emitted: bool = False


@dataclass(frozen=True)
class SelectorAudit:
    tuple_count: int
    outcome_counts: Mapping[str, int]
    overlap_count: int
    uncovered_count: int
    unreachable_category_count: int


class NativeIdentityAdapter(Protocol):
    """Closed native boundary used by one separately authorized operation."""

    def observe_metadata(
        self,
        path: str,
        parent_api: ModuleType | object,
    ) -> MetadataObservation:
        ...

    def create_suspended(self, request: FixedLaunchRequest) -> CreateSuspendedResult:
        ...

    def observe_image(self, session: object) -> ImageObservation:
        ...

    def observe_pre_resume_boundary(self, session: object) -> PreResumeBoundary:
        ...

    def resume_once(self, session: object) -> bool:
        ...

    def terminate_once(self, session: object) -> bool:
        ...

    def wait_terminal(self, session: object) -> TerminalObservation:
        ...

    def cleanup(self, session: object) -> CleanupObservation:
        ...

    def observed_at_utc(self) -> str:
        ...


_VALID_TRACES = {
    (
        "exact",
        "unavailable",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
    ): PRELAUNCH_UNAVAILABLE_CATEGORY,
    (
        "exact",
        "mismatch",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
    ): PRELAUNCH_MISMATCH_CATEGORY,
    (
        "exact",
        "exact",
        "unavailable",
        "not_reached",
        "not_reached",
        "not_reached",
    ): PRE_RESUME_UNAVAILABLE_CATEGORY,
    (
        "exact",
        "exact",
        "mismatch",
        "not_reached",
        "not_reached",
        "not_reached",
    ): PRE_RESUME_MISMATCH_CATEGORY,
    (
        "exact",
        "exact",
        "exact",
        "unavailable",
        "not_reached",
        "not_reached",
    ): POST_EXIT_UNAVAILABLE_CATEGORY,
    (
        "exact",
        "exact",
        "exact",
        "mismatch",
        "not_reached",
        "not_reached",
    ): POST_EXIT_MISMATCH_CATEGORY,
    (
        "exact",
        "exact",
        "exact",
        "exact",
        "unavailable",
        "not_reached",
    ): POSTLAUNCH_UNAVAILABLE_CATEGORY,
    (
        "exact",
        "exact",
        "exact",
        "exact",
        "available",
        "unavailable",
    ): EQUALITY_UNAVAILABLE_CATEGORY,
    (
        "exact",
        "exact",
        "exact",
        "exact",
        "available",
        "mismatch",
    ): EQUALITY_MISMATCH_CATEGORY,
    (
        "exact",
        "exact",
        "exact",
        "exact",
        "available",
        "exact",
    ): EXACT_CATEGORY,
}


def select_identity_category(
    lifecycle_evidence_state: str,
    prelaunch_metadata_state: str,
    pre_resume_image_state: str,
    post_exit_image_state: str,
    postlaunch_metadata_state: str,
    metadata_equality_state: str,
) -> str:
    """Select one category from the closed six-field raw state domain."""

    values = (
        lifecycle_evidence_state,
        prelaunch_metadata_state,
        pre_resume_image_state,
        post_exit_image_state,
        postlaunch_metadata_state,
        metadata_equality_state,
    )
    domains = (
        LIFECYCLE_STATES,
        PRELAUNCH_METADATA_STATES,
        IMAGE_STATES,
        IMAGE_STATES,
        POSTLAUNCH_METADATA_STATES,
        METADATA_EQUALITY_STATES,
    )
    if any(type(value) is not str or value not in domain for value, domain in zip(values, domains, strict=True)):
        raise ResultValidationError
    return _VALID_TRACES.get(values, AMBIGUOUS_CATEGORY)


def audit_selector() -> SelectorAudit:
    """Exhaust the exact 4000-tuple selector domain."""

    counts: Counter[str] = Counter()
    overlap = 0
    uncovered = 0
    tuple_count = 0
    for values in itertools.product(
        LIFECYCLE_STATES,
        PRELAUNCH_METADATA_STATES,
        IMAGE_STATES,
        IMAGE_STATES,
        POSTLAUNCH_METADATA_STATES,
        METADATA_EQUALITY_STATES,
    ):
        tuple_count += 1
        try:
            category = select_identity_category(*values)
        except ResultValidationError:
            uncovered += 1
            continue
        if category not in CATEGORIES:
            overlap += 1
            continue
        counts[category] += 1
    unreachable = sum(counts[category] == 0 for category in CATEGORIES)
    return SelectorAudit(tuple_count, dict(counts), overlap, uncovered, unreachable)


def _authority_flags() -> dict[str, bool]:
    return {field: False for field in AUTHORITY_FIELDS}


def _json_object_bytes(document: Mapping[str, object]) -> bytes:
    return json.dumps(document, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


def canonical_bytes(document: Mapping[str, object]) -> bytes:
    return _json_object_bytes(document) + b"\n"


def self_digest(document: Mapping[str, object]) -> str:
    if tuple(document) != RESULT_FIELDS:
        raise ResultValidationError
    preimage = dict(document)
    preimage["result_sha256"] = _ZERO_DIGEST
    return hashlib.sha256(_json_object_bytes(preimage)).hexdigest()


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
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ") == value


def _valid_characterization_id(value: object) -> bool:
    return type(value) is str and _SAFE_CHARACTERIZATION_ID.fullmatch(value) is not None


def _profile_kind(category: str) -> str:
    if category in {PRELAUNCH_UNAVAILABLE_CATEGORY, PRELAUNCH_MISMATCH_CATEGORY}:
        return "not_started"
    if category in {PRE_RESUME_UNAVAILABLE_CATEGORY, PRE_RESUME_MISMATCH_CATEGORY}:
        return "terminated_suspended"
    if category == AMBIGUOUS_CATEGORY:
        return "ambiguous"
    return "completed"


def _nonambiguous_profile_exact(document: Mapping[str, object], category: str) -> bool:
    common = (
        document["descendant_process_count"] == 0
        and document["stdout_byte_count"] == 0
        and document["stderr_byte_count"] == 0
        and document["timed_out"] is False
        and document["streams_drained"] is True
        and document["cleanup_confirmed"] is True
        and document["surviving_process_count"] == 0
    )
    if not common:
        return False
    profile = _profile_kind(category)
    if profile == "not_started":
        return (
            document["process_launch_count"] == 0
            and document["top_level_process_count"] == 0
            and document["exit_state"] == "not_started"
        )
    if profile == "terminated_suspended":
        return (
            document["process_launch_count"] == 1
            and document["top_level_process_count"] == 1
            and document["exit_state"] == "nonzero"
        )
    return (
        document["process_launch_count"] == 1
        and document["top_level_process_count"] == 1
        and document["exit_state"] == "zero"
    )


def _validate_result_semantics(document: Mapping[str, object]) -> None:
    if tuple(document) != RESULT_FIELDS:
        raise ResultValidationError
    fixed = {
        "schema_version": RESULT_SCHEMA,
        "repository_id": REPOSITORY_ID,
        "issue_number": ISSUE_NUMBER,
        "parent_issue_number": PARENT_ISSUE_NUMBER,
        "characterizer_contract_sha256": CHARACTERIZER_CONTRACT_SHA256,
        "characterizer_contract_review_sha256": CHARACTERIZER_CONTRACT_REVIEW_SHA256,
        "direct_interpreter_binding_sha256": DIRECT_INTERPRETER_BINDING_SHA256,
        "characterization_authority_consumed": True,
        "private_value_emitted": False,
    }
    if any(document[field] != value for field, value in fixed.items()):
        raise ResultValidationError
    for field in (
        "repository_id",
        "issue_number",
        "parent_issue_number",
        "process_launch_count",
        "top_level_process_count",
        "descendant_process_count",
        "stdout_byte_count",
        "stderr_byte_count",
        "surviving_process_count",
    ):
        if type(document[field]) is not int:
            raise ResultValidationError
    for field in (
        "characterization_authority_consumed",
        "timed_out",
        "streams_drained",
        "cleanup_confirmed",
        "private_value_emitted",
        "eligible_for_independent_review",
    ):
        if type(document[field]) is not bool:
            raise ResultValidationError
    for field in (
        "characterizer_contract_sha256",
        "characterizer_contract_review_sha256",
        "characterizer_sha256",
        "characterizer_test_sha256",
        "direct_interpreter_binding_sha256",
        "result_sha256",
    ):
        if not _is_sha256(document[field]):
            raise ResultValidationError
    if not _valid_characterization_id(document["characterization_id"]):
        raise ResultValidationError
    if not _whole_second_utc(document["observed_at_utc"]):
        raise ResultValidationError
    category = select_identity_category(
        cast(str, document["lifecycle_evidence_state"]),
        cast(str, document["prelaunch_metadata_state"]),
        cast(str, document["pre_resume_image_state"]),
        cast(str, document["post_exit_image_state"]),
        cast(str, document["postlaunch_metadata_state"]),
        cast(str, document["metadata_equality_state"]),
    )
    if document["category"] != category:
        raise ResultValidationError
    if document["process_launch_count"] not in {0, 1}:
        raise ResultValidationError
    if document["top_level_process_count"] not in {0, 1}:
        raise ResultValidationError
    for field in ("descendant_process_count", "surviving_process_count"):
        if cast(int, document[field]) < 0:
            raise ResultValidationError
    for field in ("stdout_byte_count", "stderr_byte_count"):
        if not 0 <= cast(int, document[field]) <= MAX_OUTPUT_BYTES:
            raise ResultValidationError
    if document["exit_state"] not in {"not_started", "zero", "nonzero", "unknown"}:
        raise ResultValidationError
    authority = document["authority_flags"]
    if type(authority) is not dict or tuple(authority) != AUTHORITY_FIELDS:
        raise ResultValidationError
    if any(type(value) is not bool or value for value in cast(dict[str, object], authority).values()):
        raise ResultValidationError
    if category != AMBIGUOUS_CATEGORY and not _nonambiguous_profile_exact(document, category):
        raise ResultValidationError
    reviewable = (
        document["streams_drained"] is True
        and document["cleanup_confirmed"] is True
        and document["surviving_process_count"] == 0
        and document["private_value_emitted"] is False
    )
    if document["eligible_for_independent_review"] is not reviewable:
        raise ResultValidationError
    if document["result_sha256"] != self_digest(document):
        raise ResultValidationError


def seal_result(
    record: CharacterizationRecord,
    bindings: PublicBindingSnapshot,
    characterization_id: str,
    observed_at_utc: str,
) -> dict[str, object]:
    if not bindings.exact:
        raise ResultValidationError
    category = select_identity_category(
        record.lifecycle_evidence_state,
        record.prelaunch_metadata_state,
        record.pre_resume_image_state,
        record.post_exit_image_state,
        record.postlaunch_metadata_state,
        record.metadata_equality_state,
    )
    reviewable = (
        record.streams_drained
        and record.cleanup_confirmed
        and record.surviving_process_count == 0
        and not record.private_value_emitted
    )
    result: dict[str, object] = {
        "schema_version": RESULT_SCHEMA,
        "repository_id": REPOSITORY_ID,
        "issue_number": ISSUE_NUMBER,
        "parent_issue_number": PARENT_ISSUE_NUMBER,
        "characterizer_contract_sha256": CHARACTERIZER_CONTRACT_SHA256,
        "characterizer_contract_review_sha256": CHARACTERIZER_CONTRACT_REVIEW_SHA256,
        "characterizer_sha256": bindings.characterizer_sha256,
        "characterizer_test_sha256": bindings.characterizer_test_sha256,
        "direct_interpreter_binding_sha256": DIRECT_INTERPRETER_BINDING_SHA256,
        "characterization_id": characterization_id,
        "observed_at_utc": observed_at_utc,
        "characterization_authority_consumed": True,
        "lifecycle_evidence_state": record.lifecycle_evidence_state,
        "prelaunch_metadata_state": record.prelaunch_metadata_state,
        "pre_resume_image_state": record.pre_resume_image_state,
        "post_exit_image_state": record.post_exit_image_state,
        "postlaunch_metadata_state": record.postlaunch_metadata_state,
        "metadata_equality_state": record.metadata_equality_state,
        "category": category,
        "process_launch_count": record.process_launch_count,
        "top_level_process_count": record.top_level_process_count,
        "descendant_process_count": record.descendant_process_count,
        "exit_state": record.exit_state,
        "stdout_byte_count": record.stdout_byte_count,
        "stderr_byte_count": record.stderr_byte_count,
        "timed_out": record.timed_out,
        "streams_drained": record.streams_drained,
        "cleanup_confirmed": record.cleanup_confirmed,
        "surviving_process_count": record.surviving_process_count,
        "private_value_emitted": False,
        "eligible_for_independent_review": reviewable,
        "authority_flags": _authority_flags(),
        "result_sha256": _ZERO_DIGEST,
    }
    result["result_sha256"] = self_digest(result)
    _validate_result_semantics(result)
    if len(canonical_bytes(result)) > MAX_OUTPUT_BYTES:
        raise ResultValidationError
    return result


def parse_result(payload: bytes) -> dict[str, object]:
    if (
        not payload
        or len(payload) > MAX_OUTPUT_BYTES
        or not payload.endswith(b"\n")
        or payload.endswith(b"\n\n")
    ):
        raise ResultValidationError
    try:
        result = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=lambda _value: (_ for _ in ()).throw(ResultValidationError()),
        )
    except (UnicodeError, json.JSONDecodeError, DuplicateJsonKeyError, ResultValidationError) as exc:
        raise ResultValidationError from exc
    if type(result) is not dict or canonical_bytes(result) != payload:
        raise ResultValidationError
    _validate_result_semantics(result)
    return cast(dict[str, object], result)


def _metadata_prelaunch_state(
    observation: MetadataObservation,
    parent_api: ModuleType | object,
) -> tuple[str, object | None]:
    if observation.state in {"unavailable", "ambiguous"}:
        if observation.value is not None:
            return "ambiguous", None
        return observation.state, None
    if observation.state != "available" or observation.value is None:
        return "ambiguous", None
    metadata_type = getattr(parent_api, "DirectInterpreterMetadata", None)
    validator = getattr(parent_api, "validate_direct_interpreter_metadata", None)
    if metadata_type is None or not callable(validator) or type(observation.value) is not metadata_type:
        return "ambiguous", None
    try:
        validator(observation.value)
    except Exception:
        return "mismatch", observation.value
    return "exact", observation.value


def _metadata_postlaunch_state(
    observation: MetadataObservation,
    parent_api: ModuleType | object,
) -> tuple[str, object | None]:
    if observation.state in {"unavailable", "ambiguous"}:
        if observation.value is not None:
            return "ambiguous", None
        return observation.state, None
    metadata_type = getattr(parent_api, "DirectInterpreterMetadata", None)
    if (
        observation.state != "available"
        or metadata_type is None
        or type(observation.value) is not metadata_type
    ):
        return "ambiguous", None
    return "available", observation.value


def _image_state(observation: ImageObservation, bound_path: str) -> str:
    if observation.state in {"unavailable", "ambiguous"}:
        if observation.value is not None:
            return "ambiguous"
        return observation.state
    value = observation.value
    if observation.state != "available" or type(value) is not str:
        return "ambiguous"
    if not 1 <= len(value) <= 32767 or "\x00" in value:
        return "unavailable"
    try:
        observed_normalized = ntpath.normcase(value)
        bound_normalized = ntpath.normcase(bound_path)
    except Exception:
        return "ambiguous"
    return "exact" if observed_normalized == bound_normalized else "mismatch"


def _metadata_equality_state(left: object, right: object) -> str:
    try:
        equal = left == right
    except Exception:
        return "unavailable"
    if type(equal) is not bool:
        return "unavailable"
    return "exact" if equal else "mismatch"


def _vacuous_terminal() -> TerminalObservation:
    return TerminalObservation("not_started", 0, 0, False, True, 0, True)


def _vacuous_cleanup() -> CleanupObservation:
    return CleanupObservation(True, 0)


def _pre_resume_boundary_exact(boundary: PreResumeBoundary) -> bool:
    return (
        boundary.job_assigned is True
        and type(boundary.active_process_count) is int
        and boundary.active_process_count == 1
        and boundary.parentage_known is True
    )


def _terminal_profile_exact(
    terminal: TerminalObservation,
    cleanup: CleanupObservation,
    *,
    expected_exit: str,
) -> bool:
    return (
        terminal.exit_state == expected_exit
        and terminal.stdout_byte_count == 0
        and terminal.stderr_byte_count == 0
        and terminal.timed_out is False
        and terminal.streams_drained is True
        and terminal.descendant_process_count == 0
        and terminal.process_stopped is True
        and cleanup.cleanup_confirmed is True
        and cleanup.surviving_process_count == 0
    )


def _record(
    *,
    lifecycle_exact: bool,
    prelaunch: str,
    pre_resume: str,
    post_exit: str,
    postlaunch: str,
    equality: str,
    launch_count: int,
    top_level_count: int,
    terminal: TerminalObservation,
    cleanup: CleanupObservation,
) -> CharacterizationRecord:
    return CharacterizationRecord(
        lifecycle_evidence_state="exact" if lifecycle_exact else "ambiguous",
        prelaunch_metadata_state=prelaunch,
        pre_resume_image_state=pre_resume,
        post_exit_image_state=post_exit,
        postlaunch_metadata_state=postlaunch,
        metadata_equality_state=equality,
        process_launch_count=launch_count,
        top_level_process_count=top_level_count,
        descendant_process_count=terminal.descendant_process_count,
        exit_state=terminal.exit_state,
        stdout_byte_count=terminal.stdout_byte_count,
        stderr_byte_count=terminal.stderr_byte_count,
        timed_out=terminal.timed_out,
        streams_drained=terminal.streams_drained,
        cleanup_confirmed=cleanup.cleanup_confirmed,
        surviving_process_count=cleanup.surviving_process_count,
    )


def _validate_private_path_text(value: str) -> None:
    if type(value) is not str or not value or "\x00" in value:
        raise CharacterizerError
    if not ntpath.isabs(value) or ntpath.basename(value) != "python.exe":
        raise CharacterizerError
    drive, tail = ntpath.splitdrive(value)
    components = tuple(
        component.casefold()
        for component in value.replace("/", "\\").split("\\")
        if component
    )
    if (
        len(drive) != 2
        or drive[1] != ":"
        or not drive[0].isalpha()
        or not tail.startswith(("\\", "/"))
        or "windowsapps" in components
    ):
        raise CharacterizerError


def _fixed_environment() -> tuple[tuple[str, str], ...]:
    selected: list[tuple[str, str]] = []
    seen: set[str] = set()
    for name in ("SystemRoot", "WINDIR"):
        matches = [
            (key, value)
            for key, value in os.environ.items()
            if key.casefold() == name.casefold()
        ]
        if len(matches) != 1 or not matches[0][1]:
            raise CharacterizerError
        if name.casefold() in seen:
            raise CharacterizerError
        seen.add(name.casefold())
        selected.append((name, matches[0][1]))
    selected.extend(
        (
            ("PYTHONDONTWRITEBYTECODE", "1"),
            ("PYTHONNOUSERSITE", "1"),
            ("PYTHONUTF8", "1"),
        )
    )
    return tuple(selected)


def _build_request(path: str, repository_root: Path) -> FixedLaunchRequest:
    _validate_private_path_text(path)
    return FixedLaunchRequest(
        application_path=path,
        arguments=FIXED_ARGUMENTS,
        repository_root=repository_root,
        environment=_fixed_environment(),
        creation_flags=(
            CREATE_SUSPENDED
            | CREATE_NO_WINDOW
            | CREATE_UNICODE_ENVIRONMENT
            | EXTENDED_STARTUPINFO_PRESENT
        ),
        timeout_seconds=PROCESS_TIMEOUT_SECONDS,
        termination_grace_seconds=TERMINATION_GRACE_SECONDS,
    )


def characterize_with_adapter(
    private_path: str,
    *,
    characterization_id: str,
    adapter: NativeIdentityAdapter,
    bindings: PublicBindingSnapshot,
    repository_root: Path,
) -> dict[str, object]:
    """Run the closed coordinator through an already selected adapter.

    This injection boundary exists only for the operation-free synthetic tests.
    The production wrapper below always constructs ``CtypesIdentityAdapter``.
    """

    if not bindings.exact or not _valid_characterization_id(characterization_id):
        raise CharacterizerError
    _validate_private_path_text(private_path)
    observed_at = adapter.observed_at_utc()
    try:
        pre_observation = adapter.observe_metadata(private_path, bindings.parent_api)
    except Exception:
        pre_observation = MetadataObservation("ambiguous", None)
    prelaunch_state, prelaunch_metadata = _metadata_prelaunch_state(
        pre_observation,
        bindings.parent_api,
    )
    if prelaunch_state != "exact":
        record = _record(
            lifecycle_exact=True,
            prelaunch=prelaunch_state,
            pre_resume="not_reached",
            post_exit="not_reached",
            postlaunch="not_reached",
            equality="not_reached",
            launch_count=0,
            top_level_count=0,
            terminal=_vacuous_terminal(),
            cleanup=_vacuous_cleanup(),
        )
        return seal_result(record, bindings, characterization_id, observed_at)

    request = _build_request(private_path, repository_root)
    creation = adapter.create_suspended(request)
    if creation.state != "created" or creation.session is None:
        terminal = _vacuous_terminal()
        record = _record(
            lifecycle_exact=False,
            prelaunch="exact",
            pre_resume="not_reached",
            post_exit="not_reached",
            postlaunch="not_reached",
            equality="not_reached",
            launch_count=0,
            top_level_count=0,
            terminal=terminal,
            cleanup=creation.cleanup,
        )
        return seal_result(record, bindings, characterization_id, observed_at)

    session = creation.session
    pre_resume_state = "ambiguous"
    post_exit_state = "not_reached"
    postlaunch_state = "not_reached"
    equality_state = "not_reached"
    terminal: TerminalObservation | None = None
    cleanup: CleanupObservation | None = None
    boundary_exact = False
    resume_exact = False
    termination_exact = False
    operation_ambiguous = False
    termination_attempted = False
    wait_attempted = False
    try:
        pre_resume_state = _image_state(
            adapter.observe_image(session),
            private_path,
        )
        boundary_exact = _pre_resume_boundary_exact(
            adapter.observe_pre_resume_boundary(session)
        )
        if pre_resume_state != "exact" or not boundary_exact:
            termination_attempted = True
            termination_exact = adapter.terminate_once(session)
            wait_attempted = True
            terminal = adapter.wait_terminal(session)
        else:
            resume_exact = adapter.resume_once(session)
            if not resume_exact:
                termination_attempted = True
                termination_exact = adapter.terminate_once(session)
                wait_attempted = True
                terminal = adapter.wait_terminal(session)
            else:
                wait_attempted = True
                terminal = adapter.wait_terminal(session)
                process_exact = (
                    terminal.exit_state == "zero"
                    and terminal.stdout_byte_count == 0
                    and terminal.stderr_byte_count == 0
                    and terminal.timed_out is False
                    and terminal.streams_drained is True
                    and terminal.descendant_process_count == 0
                    and terminal.process_stopped is True
                )
                if process_exact:
                    post_exit_state = _image_state(
                        adapter.observe_image(session),
                        private_path,
                    )
                    if post_exit_state == "exact":
                        post_observation = adapter.observe_metadata(
                            private_path,
                            bindings.parent_api,
                        )
                        postlaunch_state, postlaunch_metadata = (
                            _metadata_postlaunch_state(
                                post_observation,
                                bindings.parent_api,
                            )
                        )
                        if postlaunch_state == "available":
                            equality_state = _metadata_equality_state(
                                prelaunch_metadata,
                                postlaunch_metadata,
                            )
    except Exception:
        operation_ambiguous = True
        if terminal is None:
            if not termination_attempted:
                termination_attempted = True
                try:
                    termination_exact = adapter.terminate_once(session)
                except Exception:
                    termination_exact = False
            if not wait_attempted:
                wait_attempted = True
                try:
                    terminal = adapter.wait_terminal(session)
                except Exception:
                    terminal = None
            if terminal is None:
                terminal = TerminalObservation(
                    "unknown",
                    0,
                    0,
                    False,
                    False,
                    0,
                    False,
                )
    finally:
        try:
            cleanup = adapter.cleanup(session)
        except Exception:
            cleanup = CleanupObservation(False, 1)

    if terminal is None or cleanup is None:
        raise CharacterizerError
    if pre_resume_state in {"mismatch", "unavailable"} and boundary_exact:
        lifecycle_exact = termination_exact and _terminal_profile_exact(
            terminal,
            cleanup,
            expected_exit="nonzero",
        )
    elif resume_exact:
        lifecycle_exact = _terminal_profile_exact(
            terminal,
            cleanup,
            expected_exit="zero",
        )
    else:
        lifecycle_exact = False
    lifecycle_exact = lifecycle_exact and not operation_ambiguous
    record = _record(
        lifecycle_exact=lifecycle_exact,
        prelaunch="exact",
        pre_resume=pre_resume_state,
        post_exit=post_exit_state,
        postlaunch=postlaunch_state,
        equality=equality_state,
        launch_count=1,
        top_level_count=1,
        terminal=terminal,
        cleanup=cleanup,
    )
    return seal_result(record, bindings, characterization_id, observed_at)


def _stable_file_sha256(path: Path) -> str:
    before = path.lstat()
    attributes = getattr(before, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    if not stat.S_ISREG(before.st_mode) or attributes & reparse:
        raise CharacterizerError
    digest = hashlib.sha256()
    with path.open("rb", buffering=0) as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino, opened.st_size) != (
            before.st_dev,
            before.st_ino,
            before.st_size,
        ):
            raise CharacterizerError
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    final = path.lstat()
    identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    if identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise CharacterizerError
    if identity != (final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns):
        raise CharacterizerError
    return digest.hexdigest()


def _load_parent_api(repository_root: Path) -> ModuleType:
    path = repository_root / PARENT_API_PATH
    spec = importlib.util.spec_from_file_location("_r0_identity_characterizer_parent", path)
    if spec is None or spec.loader is None:
        raise CharacterizerError
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(spec.name, None)
        raise CharacterizerError from exc
    return module


def _public_bindings(repository_root: Path) -> PublicBindingSnapshot:
    try:
        for relative_path, expected_digest in FROZEN_PUBLIC_ARTIFACTS.items():
            if _stable_file_sha256(repository_root / relative_path) != expected_digest:
                raise CharacterizerError
        characterizer_sha = _stable_file_sha256(repository_root / CHARACTERIZER_PATH)
        test_sha = _stable_file_sha256(repository_root / CHARACTERIZER_TEST_PATH)
        parent_api = _load_parent_api(repository_root)
    except (OSError, CharacterizerError):
        return PublicBindingSnapshot(
            False,
            _ZERO_DIGEST,
            _ZERO_DIGEST,
            ModuleType("_unloaded_r0_identity_characterizer_parent"),
        )
    return PublicBindingSnapshot(True, characterizer_sha, test_sha, parent_api)


class _BoundPrivatePath:
    __slots__ = ("_buffer",)

    def __init__(self, value: str) -> None:
        self._buffer = ctypes.create_unicode_buffer(value, len(value) + 1)

    def value(self) -> str:
        return self._buffer.value

    def clear(self) -> None:
        for index in range(len(self._buffer)):
            self._buffer[index] = "\x00"


def parse_private_path_stdin(stream: BinaryIO) -> _BoundPrivatePath:
    payload = bytearray(stream.read(MAX_PRIVATE_PATH_BYTES + 1))
    decoded = ""
    try:
        if (
            not payload
            or len(payload) > MAX_PRIVATE_PATH_BYTES
            or payload.startswith(b"\xef\xbb\xbf")
            or not payload.endswith(b"\n")
            or payload.endswith(b"\n\n")
            or payload.count(b"\n") != 1
            or b"\r" in payload
            or b"\x00" in payload
        ):
            raise CharacterizerError
        decoded = bytes(payload[:-1]).decode("utf-8", errors="strict")
        _validate_private_path_text(decoded)
        return _BoundPrivatePath(decoded)
    except (UnicodeError, CharacterizerError) as exc:
        raise CharacterizerError from exc
    finally:
        for index in range(len(payload)):
            payload[index] = 0
        decoded = ""


def run_consumed_characterization(
    *,
    characterization_id: str,
    stdin: BinaryIO,
    stdout: BinaryIO,
) -> int:
    """Run only after an external executor proves exact atomic consumption."""

    repository_root = Path(__file__).absolute().parent.parent
    private_path: _BoundPrivatePath | None = None
    try:
        if not _valid_characterization_id(characterization_id):
            return 2
        bindings = _public_bindings(repository_root)
        if not bindings.exact:
            return 2
        private_path = parse_private_path_stdin(stdin)
        result = characterize_with_adapter(
            private_path.value(),
            characterization_id=characterization_id,
            adapter=CtypesIdentityAdapter(),
            bindings=bindings,
            repository_root=repository_root,
        )
        payload = canonical_bytes(result)
        stdout.write(payload)
        stdout.flush()
        return 0
    except Exception:
        return 2
    finally:
        if private_path is not None:
            private_path.clear()


# The Win32 adapter is declared below the pure kernel so imports and synthetic
# tests do not instantiate native APIs or create a process.

HANDLE_FLAG_INHERIT = 0x00000001
STARTF_USESTDHANDLES = 0x00000100
PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002
CREATE_SUSPENDED = 0x00000004
CREATE_NO_WINDOW = 0x08000000
CREATE_UNICODE_ENVIRONMENT = 0x00000400
EXTENDED_STARTUPINFO_PRESENT = 0x00080000
JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 0x00000008
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT = 3
JOB_OBJECT_MSG_NEW_PROCESS = 6
JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO = 4
JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION_CLASS = 1
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
    _fields_ = (("StartupInfo", _StartupInfoW), ("lpAttributeList", wintypes.LPVOID))


class _ProcessInformation(ctypes.Structure):
    _fields_ = (
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    )


class _IoCounters(ctypes.Structure):
    _fields_ = tuple(
        (name, ctypes.c_ulonglong)
        for name in (
            "ReadOperationCount",
            "WriteOperationCount",
            "OtherOperationCount",
            "ReadTransferCount",
            "WriteTransferCount",
            "OtherTransferCount",
        )
    )


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
    _fields_ = (("CompletionKey", wintypes.LPVOID), ("CompletionPort", wintypes.HANDLE))


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
    def __init__(self, kernel32: object, value: int | None) -> None:
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
        try:
            self.close_ok = bool(self._kernel32.CloseHandle(wintypes.HANDLE(value)))
        except Exception:
            self.close_ok = False
        return self.close_ok


class _OwnedAttributeList:
    def __init__(self, kernel32: object) -> None:
        self._kernel32 = kernel32
        self.buffer: ctypes.Array[ctypes.c_char] | None = None
        self.pointer: wintypes.LPVOID | None = None
        self.initialized = False
        self.close_ok = True

    def initialize(self) -> wintypes.LPVOID:
        if self.buffer is not None or self.pointer is not None or self.initialized:
            raise CharacterizerError
        size = ctypes.c_size_t()
        self._kernel32.InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(size))
        if size.value == 0:
            raise CharacterizerError
        self.buffer = ctypes.create_string_buffer(size.value)
        pointer = ctypes.cast(self.buffer, wintypes.LPVOID)
        if not self._kernel32.InitializeProcThreadAttributeList(
            pointer,
            1,
            0,
            ctypes.byref(size),
        ):
            raise CharacterizerError
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


@dataclass
class _NativeSession:
    kernel32: object
    handles: dict[str, _OwnedHandle]
    process_information: _ProcessInformation
    attribute_owner: _OwnedAttributeList
    job_assigned: bool
    timeout_seconds: float
    termination_grace_seconds: float
    resume_attempted: bool = False
    resumed: bool = False
    termination_attempted: bool = False
    stdout_byte_count: int = 0
    stderr_byte_count: int = 0
    stdout_overflow: bool = False
    stderr_overflow: bool = False
    descendant_process_ids: set[int] = dataclass_field(default_factory=set)
    active_limit_seen: bool = False
    accounting_violation_seen: bool = False


def _kernel32() -> object:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
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
    kernel32.QueryInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
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
    kernel32.GetExitCodeProcess.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.DWORD),
    )
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


def _create_pipe_pair(
    kernel32: object,
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
        raise CharacterizerError
    return (
        _OwnedHandle(kernel32, cast(int, read_handle.value)),
        _OwnedHandle(kernel32, cast(int, write_handle.value)),
    )


def _set_and_verify_pipe_inheritance(
    kernel32: object,
    handles: Mapping[str, _OwnedHandle],
) -> None:
    for name in ("stdin_write", "stdout_read", "stderr_read"):
        handle = handles[name]
        if not kernel32.SetHandleInformation(
            wintypes.HANDLE(handle.value),
            HANDLE_FLAG_INHERIT,
            0,
        ):
            raise CharacterizerError
    inheritable = {"stdin_read", "stdout_write", "stderr_write"}
    for name, handle in handles.items():
        flags = wintypes.DWORD()
        if not handle.open or not kernel32.GetHandleInformation(
            wintypes.HANDLE(handle.value),
            ctypes.byref(flags),
        ):
            raise CharacterizerError
        if bool(flags.value & HANDLE_FLAG_INHERIT) != (name in inheritable):
            raise CharacterizerError


def _query_job_active_processes(kernel32: object, job: _OwnedHandle) -> int:
    accounting = _JobBasicAccountingInformation()
    returned = wintypes.DWORD()
    if not kernel32.QueryInformationJobObject(
        wintypes.HANDLE(job.value),
        JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION_CLASS,
        ctypes.byref(accounting),
        ctypes.sizeof(accounting),
        ctypes.byref(returned),
    ) or returned.value != ctypes.sizeof(accounting):
        raise CharacterizerError
    return int(accounting.ActiveProcesses)


def _query_process_image(kernel32: object, process: _OwnedHandle) -> str:
    capacity = 32768
    buffer = ctypes.create_unicode_buffer(capacity)
    size = wintypes.DWORD(capacity)
    if not kernel32.QueryFullProcessImageNameW(
        wintypes.HANDLE(process.value),
        0,
        buffer,
        ctypes.byref(size),
    ):
        raise CharacterizerError
    if not 1 <= size.value < capacity:
        raise CharacterizerError
    value = "".join(buffer[index] for index in range(size.value))
    if "\x00" in value:
        raise CharacterizerError
    return value


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
        raise CharacterizerError
    return int(information.InheritedFromUniqueProcessId)


def _environment_block(
    environment: Sequence[tuple[str, str]],
) -> ctypes.Array[ctypes.c_wchar]:
    if len({name.casefold() for name, _value in environment}) != len(environment):
        raise CharacterizerError
    text = "\x00".join(
        f"{name}={value}"
        for name, value in sorted(environment, key=lambda item: item[0].casefold())
    ) + "\x00\x00"
    return ctypes.create_unicode_buffer(text)


def _windows_quote_argument(argument: str) -> str:
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


def _fixed_command_line(request: FixedLaunchRequest) -> str:
    return " ".join(
        _windows_quote_argument(value)
        for value in (request.application_path, *request.arguments)
    )


def _close_all(handles: Mapping[str, _OwnedHandle]) -> bool:
    all_closed = True
    for handle in reversed(tuple(handles.values())):
        all_closed = handle.close() and all_closed
    return all_closed


def _read_pipe_available(
    session: _NativeSession,
    name: str,
) -> bool:
    handle = session.handles[name]
    available = wintypes.DWORD()
    kernel32 = session.kernel32
    if not kernel32.PeekNamedPipe(
        wintypes.HANDLE(handle.value),
        None,
        0,
        None,
        ctypes.byref(available),
        None,
    ):
        return ctypes.get_last_error() == ERROR_BROKEN_PIPE
    while available.value:
        requested = min(int(available.value), 4096)
        buffer = ctypes.create_string_buffer(requested)
        received = wintypes.DWORD()
        if not kernel32.ReadFile(
            wintypes.HANDLE(handle.value),
            buffer,
            requested,
            ctypes.byref(received),
            None,
        ):
            return ctypes.get_last_error() == ERROR_BROKEN_PIPE
        field_name = "stdout_byte_count" if name == "stdout_read" else "stderr_byte_count"
        overflow_name = "stdout_overflow" if name == "stdout_read" else "stderr_overflow"
        updated = getattr(session, field_name) + int(received.value)
        if updated > MAX_OUTPUT_BYTES:
            setattr(session, overflow_name, True)
        setattr(session, field_name, min(updated, MAX_OUTPUT_BYTES))
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


def _drain_completion_port(session: _NativeSession) -> None:
    kernel32 = session.kernel32
    port = session.handles["completion_port"]
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
                return
            raise CharacterizerError
        process_id = ctypes.cast(overlapped, ctypes.c_void_p).value or 0
        if (
            message.value == JOB_OBJECT_MSG_NEW_PROCESS
            and process_id != int(session.process_information.dwProcessId)
        ):
            session.descendant_process_ids.add(process_id)
        elif message.value == JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT:
            session.active_limit_seen = True


def _descendant_count(session: _NativeSession) -> int:
    return (
        len(session.descendant_process_ids)
        + int(session.active_limit_seen)
        + int(session.accounting_violation_seen)
    )


class CtypesIdentityAdapter:
    """Direct Win32 adapter selected only by the consumed production wrapper."""

    def __init__(self) -> None:
        if os.name != "nt" or sys.platform != "win32":
            raise CharacterizerError

    def observe_metadata(
        self,
        path: str,
        parent_api: ModuleType | object,
    ) -> MetadataObservation:
        observer = getattr(parent_api, "_observe_windows_direct_interpreter", None)
        if not callable(observer):
            return MetadataObservation("ambiguous")
        try:
            return MetadataObservation("available", observer(Path(path)))
        except Exception:
            return MetadataObservation("unavailable")

    def create_suspended(self, request: FixedLaunchRequest) -> CreateSuspendedResult:
        if (
            request.arguments != FIXED_ARGUMENTS
            or request.creation_flags
            != (
                CREATE_SUSPENDED
                | CREATE_NO_WINDOW
                | CREATE_UNICODE_ENVIRONMENT
                | EXTENDED_STARTUPINFO_PRESENT
            )
            or request.timeout_seconds != PROCESS_TIMEOUT_SECONDS
            or request.termination_grace_seconds != TERMINATION_GRACE_SECONDS
        ):
            return CreateSuspendedResult("ambiguous", None, CleanupObservation(False, 1))
        kernel32 = _kernel32()
        handles: dict[str, _OwnedHandle] = {}
        attributes = _OwnedAttributeList(kernel32)
        information = _ProcessInformation()
        created = False
        job_assigned = False
        try:
            security = _SecurityAttributes(ctypes.sizeof(_SecurityAttributes), None, True)
            handles["stdin_read"], handles["stdin_write"] = _create_pipe_pair(
                kernel32,
                security,
            )
            handles["stdout_read"], handles["stdout_write"] = _create_pipe_pair(
                kernel32,
                security,
            )
            handles["stderr_read"], handles["stderr_write"] = _create_pipe_pair(
                kernel32,
                security,
            )
            _set_and_verify_pipe_inheritance(kernel32, handles)
            handles["job"] = _OwnedHandle(
                kernel32,
                cast(int, kernel32.CreateJobObjectW(None, None)),
            )
            if not handles["job"].open:
                raise CharacterizerError
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
                raise CharacterizerError
            invalid_handle = wintypes.HANDLE(ctypes.c_void_p(-1).value)
            handles["completion_port"] = _OwnedHandle(
                kernel32,
                cast(int, kernel32.CreateIoCompletionPort(invalid_handle, None, 0, 1)),
            )
            if not handles["completion_port"].open:
                raise CharacterizerError
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
                raise CharacterizerError
            attribute_list = attributes.initialize()
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
                raise CharacterizerError
            startup = _StartupInfoExW()
            startup.StartupInfo.cb = ctypes.sizeof(startup)
            startup.StartupInfo.dwFlags = STARTF_USESTDHANDLES
            startup.StartupInfo.hStdInput = wintypes.HANDLE(handles["stdin_read"].value)
            startup.StartupInfo.hStdOutput = wintypes.HANDLE(handles["stdout_write"].value)
            startup.StartupInfo.hStdError = wintypes.HANDLE(handles["stderr_write"].value)
            startup.lpAttributeList = attribute_list
            if not handles["stdin_write"].close():
                raise CharacterizerError
            command_line = ctypes.create_unicode_buffer(_fixed_command_line(request))
            environment = _environment_block(request.environment)
            created = bool(
                kernel32.CreateProcessW(
                    request.application_path,
                    command_line,
                    None,
                    None,
                    True,
                    request.creation_flags,
                    ctypes.cast(environment, wintypes.LPVOID),
                    os.fspath(request.repository_root),
                    ctypes.cast(ctypes.byref(startup), ctypes.POINTER(_StartupInfoW)),
                    ctypes.byref(information),
                )
            )
            if created:
                handles["process"] = _OwnedHandle(
                    kernel32,
                    cast(int, information.hProcess),
                )
                handles["thread"] = _OwnedHandle(
                    kernel32,
                    cast(int, information.hThread),
                )
                if not handles["process"].open or not handles["thread"].open:
                    raise CharacterizerError
            if not attributes.close():
                raise CharacterizerError
            if not created:
                cleanup = CleanupObservation(_close_all(handles), 0)
                return CreateSuspendedResult("failed", None, cleanup)
            for inherited_name in ("stdin_read", "stdout_write", "stderr_write"):
                if not handles[inherited_name].close():
                    raise CharacterizerError
            job_assigned = bool(
                kernel32.AssignProcessToJobObject(
                    wintypes.HANDLE(handles["job"].value),
                    wintypes.HANDLE(handles["process"].value),
                )
            )
            session = _NativeSession(
                kernel32,
                handles,
                information,
                attributes,
                job_assigned,
                request.timeout_seconds,
                request.termination_grace_seconds,
            )
            return CreateSuspendedResult(
                "created",
                session,
                CleanupObservation(False, 1),
            )
        except Exception:
            attribute_ok = attributes.close()
            process_stopped = not created
            if created and "process" in handles and handles["process"].open:
                try:
                    if job_assigned and "job" in handles and handles["job"].open:
                        kernel32.TerminateJobObject(wintypes.HANDLE(handles["job"].value), 1)
                    else:
                        kernel32.TerminateProcess(
                            wintypes.HANDLE(handles["process"].value),
                            1,
                        )
                    process_stopped = (
                        kernel32.WaitForSingleObject(
                            wintypes.HANDLE(handles["process"].value),
                            int(TERMINATION_GRACE_SECONDS * 1000),
                        )
                        == WAIT_OBJECT_0
                    )
                except Exception:
                    process_stopped = False
            close_ok = _close_all(handles)
            cleanup_ok = attribute_ok and close_ok and process_stopped
            return CreateSuspendedResult(
                "ambiguous",
                None,
                CleanupObservation(cleanup_ok, 0 if cleanup_ok else 1),
            )

    def _session(self, session: object) -> _NativeSession:
        if type(session) is not _NativeSession:
            raise CharacterizerError
        return session

    def observe_image(self, session: object) -> ImageObservation:
        native = self._session(session)
        try:
            return ImageObservation(
                "available",
                _query_process_image(native.kernel32, native.handles["process"]),
            )
        except Exception:
            return ImageObservation("unavailable")

    def observe_pre_resume_boundary(self, session: object) -> PreResumeBoundary:
        native = self._session(session)
        active: int | None
        parentage: bool | None
        try:
            active = _query_job_active_processes(native.kernel32, native.handles["job"])
        except Exception:
            active = None
        try:
            parentage = _query_parent_process_id(native.handles["process"]) == os.getpid()
        except Exception:
            parentage = None
        return PreResumeBoundary(native.job_assigned, active, parentage)

    def resume_once(self, session: object) -> bool:
        native = self._session(session)
        if native.resume_attempted:
            return False
        native.resume_attempted = True
        try:
            previous_count = native.kernel32.ResumeThread(
                wintypes.HANDLE(native.handles["thread"].value)
            )
        except Exception:
            return False
        native.resumed = previous_count == 1
        return native.resumed

    def terminate_once(self, session: object) -> bool:
        native = self._session(session)
        if native.termination_attempted:
            return False
        native.termination_attempted = True
        try:
            if native.job_assigned:
                return bool(
                    native.kernel32.TerminateJobObject(
                        wintypes.HANDLE(native.handles["job"].value),
                        1,
                    )
                )
            return bool(
                native.kernel32.TerminateProcess(
                    wintypes.HANDLE(native.handles["process"].value),
                    1,
                )
            )
        except Exception:
            return False

    def wait_terminal(self, session: object) -> TerminalObservation:
        native = self._session(session)
        deadline = time.monotonic() + (
            native.timeout_seconds if native.resumed else native.termination_grace_seconds
        )
        timed_out = False
        streams_ok = True
        process_stopped = False
        while True:
            wait = native.kernel32.WaitForSingleObject(
                wintypes.HANDLE(native.handles["process"].value),
                10,
            )
            if wait == WAIT_OBJECT_0:
                process_stopped = True
            elif wait != WAIT_TIMEOUT:
                streams_ok = False
                break
            streams_ok = (
                _read_pipe_available(native, "stdout_read")
                and _read_pipe_available(native, "stderr_read")
                and streams_ok
            )
            try:
                _drain_completion_port(native)
                active = _query_job_active_processes(
                    native.kernel32,
                    native.handles["job"],
                )
                if active > 1:
                    native.accounting_violation_seen = True
            except Exception:
                streams_ok = False
            fault = (
                native.stdout_overflow
                or native.stderr_overflow
                or _descendant_count(native) > 0
                or not streams_ok
            )
            now = time.monotonic()
            if native.resumed and now >= deadline and not process_stopped:
                timed_out = True
                fault = True
            if fault and not native.termination_attempted:
                self.terminate_once(native)
                deadline = now + native.termination_grace_seconds
            if process_stopped:
                break
            if now >= deadline and native.termination_attempted:
                break
        streams_ok = (
            _read_pipe_available(native, "stdout_read")
            and _read_pipe_available(native, "stderr_read")
            and streams_ok
        )
        try:
            _drain_completion_port(native)
        except Exception:
            streams_ok = False
        exit_code = wintypes.DWORD(STILL_ACTIVE)
        exit_known = bool(
            native.kernel32.GetExitCodeProcess(
                wintypes.HANDLE(native.handles["process"].value),
                ctypes.byref(exit_code),
            )
        ) and exit_code.value != STILL_ACTIVE
        exit_state = (
            "unknown"
            if not exit_known
            else ("zero" if exit_code.value == 0 else "nonzero")
        )
        return TerminalObservation(
            exit_state,
            native.stdout_byte_count,
            native.stderr_byte_count,
            timed_out,
            streams_ok and not native.stdout_overflow and not native.stderr_overflow,
            _descendant_count(native),
            process_stopped,
        )

    def cleanup(self, session: object) -> CleanupObservation:
        native = self._session(session)
        process_stopped = False
        active: int | None = None
        try:
            process_stopped = (
                native.kernel32.WaitForSingleObject(
                    wintypes.HANDLE(native.handles["process"].value),
                    0,
                )
                == WAIT_OBJECT_0
            )
            if not process_stopped and not native.termination_attempted:
                self.terminate_once(native)
                process_stopped = (
                    native.kernel32.WaitForSingleObject(
                        wintypes.HANDLE(native.handles["process"].value),
                        int(native.termination_grace_seconds * 1000),
                    )
                    == WAIT_OBJECT_0
                )
            active = _query_job_active_processes(native.kernel32, native.handles["job"])
        except Exception:
            process_stopped = False
            active = None
        attribute_ok = native.attribute_owner.close()
        close_ok = _close_all(native.handles)
        cleanup_ok = process_stopped and active == 0 and attribute_ok and close_ok
        survivor_count = 0 if cleanup_ok else max(1, 0 if active is None else active)
        return CleanupObservation(cleanup_ok, survivor_count)

    def observed_at_utc(self) -> str:
        return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    # Direct execution has no consumed owner decision or bound public ID.
    raise SystemExit(2)
