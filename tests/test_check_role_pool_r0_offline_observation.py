from __future__ import annotations

import copy
import hashlib
import importlib.util
import io
import itertools
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "tools/check_role_pool_r0_offline_observation.py"
SPEC = importlib.util.spec_from_file_location(
    "check_role_pool_r0_offline_observation",
    MODULE_PATH,
)
assert SPEC is not None and SPEC.loader is not None
observation = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = observation
SPEC.loader.exec_module(observation)


def _signed(document: dict[str, object], field: str) -> dict[str, object]:
    result = copy.deepcopy(document)
    result[field] = observation.self_digest(result, field)
    return result


def _receipt_bytes(position: int) -> bytes:
    return observation.canonical_bytes(observation.EXPECTED_RECEIPTS[position - 1])


def _direct_metadata(**changes: object) -> object:
    values: dict[str, object] = {
        "runtime_implementation": "CPython",
        "executable_basename": "python.exe",
        "file_version": "3.13.14",
        "product_version": "3.13.14",
        "byte_length": 105696,
        "file_sha256": (
            "ef8f51028ac5329641985112f8efb1c2d4c47c86b8011ddf7e6fae21e2b4e5a1"
        ),
        "stable_identity_sha256": (
            "570754cbc03fb52f4e846c3611e48e18334f08e621babfa2e8eb76f4a0e5c953"
        ),
        "ordinary_file": True,
        "reparse_point": False,
    }
    values.update(changes)
    return observation.DirectInterpreterMetadata(**values)


def _consumption(position: int = 1) -> dict[str, object]:
    packet = copy.deepcopy(observation.SYNTHETIC_CONSUMPTION_KAT)
    if position == 2:
        packet["observation_id"] = observation.OBSERVATION_IDS[1]
        packet["sequence_position"] = 2
        packet["predecessor_consumption_sha256"] = "7" * 64
        packet["expected_receipt_sha256"] = observation.EXPECTED_RECEIPT_SHA256S[1]
    packet["consumption_sha256"] = observation.self_digest(
        packet,
        "consumption_sha256",
    )
    return packet


def _lifecycle_state(**changes: object) -> dict[str, object]:
    state: dict[str, object] = {
        "public_binding_exact": True,
        "authority_exact": True,
        "sequence_exact": True,
        "consumption_status": "consumed_exact_nonreusable",
        "host_exact": True,
        "launch_status": "exact",
        "safety_boundary_exact": True,
        "timeout_status": "within_limit",
        "result_status": "exact",
        "sealing_exact": True,
        "publication_status": "exact",
        "readback_exact": True,
    }
    state.update(changes)
    return state


def _bootstrap_packet() -> dict[str, object]:
    return {
        "contract_binding_status": "exact",
        "manifest_status": "exact",
        "source_tree_node_count": 41,
        "source_tree_file_count": 36,
        "source_tree_manifest_byte_count": 6495,
        "source_tree_sha256": observation.SOURCE_TREE_SHA256,
        "installed_tree_node_count": 41,
        "installed_tree_file_count": 36,
        "installed_tree_manifest_byte_count": 6495,
        "installed_tree_sha256": observation.SOURCE_TREE_SHA256,
        "source_install_status": "identical",
        "registry_status": "valid_exact",
        "registry_sha256": observation.REGISTRY_SHA256,
        "release_state_status": "present_valid_chain",
        "release_state_sha256": observation.RELEASE_STATE_ARTIFACT_SHA256,
        "checker_sha256": observation.R0_CHECKER_SHA256,
        "checker_test_sha256": observation.R0_CHECKER_TEST_SHA256,
        "validator_bundle_sha256": observation.VALIDATOR_BUNDLE_SHA256,
        "validator_bundle_status": "exact",
        "offline_validation_status": "passed",
        "terminal_status": "blocked_release_state_conflict",
        "eligible_for_independent_review": False,
        "effect_counts": {
            "app_server_process_start_count": 0,
            "task_creation_count": 0,
            "network_operation_count": 0,
            "repository_command_count": 0,
            "persistent_mutation_count": 0,
        },
        "authority_flags": {
            field: False for field in observation.AUTHORITY_FIELDS
        },
    }


class _FakePool:
    @staticmethod
    def parse_trusted_native_json(text: str) -> dict[str, object]:
        value = json.loads(text)
        assert isinstance(value, dict)
        return value

    @staticmethod
    def validate_trusted_native_release_record(value: object) -> list[str]:
        return [] if isinstance(value, dict) else ["invalid"]

    @staticmethod
    def validate_trusted_native_release_chain(value: object) -> list[str]:
        return [] if isinstance(value, list) and len(value) == 1 else ["invalid"]

    @staticmethod
    def trusted_native_current_rung(value: object) -> str | None:
        return "R0" if isinstance(value, list) and len(value) == 1 else None

    @staticmethod
    def validate_trusted_native_release_ceiling(
        rung: object,
        **values: object,
    ) -> list[str]:
        expected = {
            "mode": "offline",
            "role": None,
            "lane_count": 0,
            "wave_count": 0,
            "operation_id": "offline_validation",
            "claim_creation": False,
            "task_creation": False,
            "f_publication": False,
        }
        return [] if rung == "R0" and values == expected else ["invalid"]


class _FakeChecker:
    RELEASE_STATE_RELATIVE_PATH = Path(
        "docs/role_pool/trusted_owner_native_release_state.v1.jsonl"
    )
    CHECKER_RELATIVE_PATH = Path("tools/check_role_pool_r0_bootstrap.py")
    CHECKER_TEST_RELATIVE_PATH = Path("tests/test_check_role_pool_r0_bootstrap.py")

    def __init__(self) -> None:
        self.calls: list[str] = []
        self._release = (
            REPO_ROOT / self.RELEASE_STATE_RELATIVE_PATH
        ).read_bytes()
        self._checker = (REPO_ROOT / self.CHECKER_RELATIVE_PATH).read_bytes()
        self._tests = (REPO_ROOT / self.CHECKER_TEST_RELATIVE_PATH).read_bytes()
        self._owners = SimpleNamespace(
            pool=_FakePool(),
            stage3=object(),
            installer=object(),
        )

    def _evaluate_roots(self, roots: object) -> tuple[dict[str, object], bytes]:
        del roots
        self.calls.append("evaluate_roots")
        return _bootstrap_packet(), b"synthetic-owner-packet\n"

    def _load_owner_modules(self, root: Path) -> object:
        assert root == REPO_ROOT
        self.calls.append("load_owner_modules")
        return self._owners

    def _read_stable_file(self, path: Path) -> object:
        self.calls.append(f"read:{path.name}")
        payloads = {
            self.RELEASE_STATE_RELATIVE_PATH.name: self._release,
            self.CHECKER_RELATIVE_PATH.name: self._checker,
            self.CHECKER_TEST_RELATIVE_PATH.name: self._tests,
        }
        return SimpleNamespace(state="exact", payload=payloads[path.name])

    def _binding_status(self, root: Path) -> tuple[str, dict[str, str]]:
        assert root == REPO_ROOT
        self.calls.append("binding_status")
        return "exact", {"registry_validator": observation.RELEASE_VALIDATOR_SHA256}

    def _manifest_observation(self, stage3: object, workflow_root: Path) -> object:
        del stage3, workflow_root
        self.calls.append("manifest_observation")
        return SimpleNamespace(status="exact", file_count=39)

    def _tree_observations(self, roots: object, owners: object) -> tuple[object, object, str]:
        del roots, owners
        self.calls.append("tree_observations")
        tree = SimpleNamespace(status="observed", sha256=observation.SOURCE_TREE_SHA256)
        return tree, tree, "identical"

    def _fixed_inputs(self, root: Path, pool: object) -> object:
        del root, pool
        self.calls.append("fixed_inputs")
        return SimpleNamespace(
            registry_status="valid_exact",
            registry_sha256=observation.REGISTRY_SHA256,
            release_state_status="present_valid_chain",
            release_state_sha256=observation.RELEASE_STATE_ARTIFACT_SHA256,
        )

    def _validator_bundle(self, checker: str, tests: str, pool: object) -> str:
        del checker, tests, pool
        self.calls.append("validator_bundle")
        return observation.VALIDATOR_BUNDLE_SHA256

    def _offline_validation_status(self, owners: object) -> str:
        del owners
        self.calls.append("offline_validation")
        return "passed"


def _fake_roots() -> object:
    return SimpleNamespace(
        repository_root=REPO_ROOT,
        installed_skills_root=REPO_ROOT / "synthetic-installed-skills",
    )


def test_profile_is_exact_known_answer() -> None:
    payload = observation.canonical_bytes(observation.OBSERVATION_PROFILE)
    assert len(payload) == 1776
    assert hashlib.sha256(payload).hexdigest() == observation.OBSERVATION_PROFILE_SHA256
    assert observation.OBSERVATION_PROFILE["schema_version"].endswith(".v2")
    assert observation.OBSERVATION_PROFILE["direct_interpreter_binding_sha256"] == (
        observation.DIRECT_INTERPRETER_BINDING_SHA256
    )
    assert observation.OBSERVATION_PROFILE["launcher_mode"] == (
        "exact_direct_absolute_cpython_no_shell"
    )
    assert observation.OBSERVATION_PROFILE["observation_count"] == 2
    assert observation.OBSERVATION_PROFILE["retry_limit"] == 0


def test_direct_interpreter_binding_is_exact_known_answer() -> None:
    binding = observation.DIRECT_INTERPRETER_BINDING
    payload = observation.canonical_bytes(binding)
    preimage = observation.canonical_bytes(
        {key: value for key, value in binding.items() if key != "binding_sha256"}
    )
    assert tuple(binding) == observation.DIRECT_INTERPRETER_BINDING_FIELDS
    assert len(preimage) == 694
    assert len(payload) == 778
    assert binding["binding_sha256"] == observation.DIRECT_INTERPRETER_BINDING_SHA256
    assert hashlib.sha256(payload).hexdigest() == (
        observation.DIRECT_INTERPRETER_BINDING_ARTIFACT_SHA256
    )
    assert observation.parse_direct_interpreter_binding(payload) == binding
    assert binding["private_path_publication_authorized"] is False
    assert b"C:\\" not in payload
    assert b"C:/" not in payload
    assert b"Users" not in payload


def test_direct_interpreter_binding_rejects_shape_type_and_digest_drift() -> None:
    binding = observation.DIRECT_INTERPRETER_BINDING
    payload = observation.canonical_bytes(binding)
    duplicate = payload.replace(
        b'{"schema_version":',
        b'{"schema_version":"duplicate","schema_version":',
        1,
    )
    reordered = {key: binding[key] for key in reversed(binding)}
    missing = {
        key: value for key, value in binding.items() if key != "repository_id"
    }
    extra = copy.deepcopy(binding)
    extra["unexpected"] = False
    wrong_type = copy.deepcopy(binding)
    wrong_type["byte_length"] = True
    wrong_type["binding_sha256"] = observation.self_digest(
        wrong_type,
        "binding_sha256",
    )
    wrong_digest = copy.deepcopy(binding)
    wrong_digest["binding_sha256"] = "0" * 64
    for candidate in (
        duplicate,
        observation.canonical_bytes(reordered),
        observation.canonical_bytes(missing),
        observation.canonical_bytes(extra),
        observation.canonical_bytes(wrong_type),
        observation.canonical_bytes(wrong_digest),
    ):
        with pytest.raises(observation.ObservationFailure) as error:
            observation.parse_direct_interpreter_binding(candidate)
        assert error.value.status == "observation_binding_rejected"


@pytest.mark.parametrize(
    "changes",
    [
        {"runtime_implementation": "PyPy"},
        {"executable_basename": "py.exe"},
        {"file_version": "3.13.13"},
        {"product_version": "3.13.13"},
        {"byte_length": 105697},
        {"file_sha256": "0" * 64},
        {"stable_identity_sha256": "0" * 64},
        {"ordinary_file": False},
        {"reparse_point": True},
    ],
)
def test_direct_interpreter_metadata_rejects_every_binding_drift(
    changes: dict[str, object],
) -> None:
    with pytest.raises(observation.ObservationFailure) as error:
        observation.validate_direct_interpreter_metadata(_direct_metadata(**changes))
    assert error.value.status == "observation_binding_rejected"


def test_running_direct_interpreter_requires_two_stable_reads_without_echo() -> None:
    private_path = Path("C:/private/python.exe")
    calls: list[Path] = []

    def observer(path: Path) -> object:
        calls.append(path)
        return _direct_metadata()

    result = observation.validate_running_direct_interpreter(
        private_path,
        observer=observer,
    )
    assert result == _direct_metadata()
    assert calls == [private_path, private_path]

    unstable = iter((_direct_metadata(), _direct_metadata(file_sha256="0" * 64)))
    with pytest.raises(observation.ObservationFailure) as error:
        observation.validate_running_direct_interpreter(
            private_path,
            observer=lambda path: next(unstable),
        )
    assert str(error.value) == "observation_binding_rejected"
    assert "private" not in str(error.value).lower()


@pytest.mark.parametrize(
    "candidate",
    [
        "python.exe",
        "py.exe",
        "C:/private/py.exe",
        "C:/private/python.cmd",
        "C:/private/python.bat",
        "C:/private/powershell.exe",
        "C:/private/cmd.exe",
    ],
)
def test_running_direct_interpreter_rejects_relative_alias_wrapper_and_shell(
    candidate: str,
) -> None:
    reader = mock.Mock(side_effect=AssertionError("must not inspect"))
    with pytest.raises(observation.ObservationFailure) as error:
        observation.validate_running_direct_interpreter(candidate, observer=reader)
    assert error.value.status == "observation_binding_rejected"
    assert reader.call_count == 0
    assert candidate not in str(error.value)


def test_running_direct_interpreter_rejects_reparse_and_raw_reader_failure() -> None:
    private_path = Path("C:/private/python.exe")
    with pytest.raises(observation.ObservationFailure) as error:
        observation.validate_running_direct_interpreter(
            private_path,
            observer=lambda path: _direct_metadata(reparse_point=True),
        )
    assert error.value.status == "observation_binding_rejected"
    with pytest.raises(observation.ObservationFailure) as error:
        observation.validate_running_direct_interpreter(
            private_path,
            observer=mock.Mock(
                side_effect=OSError("C:/private/raw-identity-value")
            ),
        )
    assert str(error.value) == "observation_binding_rejected"
    assert "private" not in str(error.value).lower()


def test_stable_file_identity_digest_uses_closed_synthetic_preimage() -> None:
    expected = hashlib.sha256(
        b"trusted_owner_direct_cpython_file_identity.v1|"
        b"volume_serial_number=1234abcd|file_index=0123456789abcdef"
    ).hexdigest()
    assert observation._stable_file_identity_sha256(
        0x1234ABCD,
        0x0123456789ABCDEF,
    ) == expected


def test_direct_interpreter_preflight_selector_covers_all_32_tuples() -> None:
    row_counts: Counter[int] = Counter()
    overlap_count = 0
    uncovered_count = 0
    for historical, public, private, state in itertools.product(
        (False, True),
        (False, True),
        (False, True),
        observation.DIRECT_INTERPRETER_PREFLIGHT_STATES,
    ):
        row_matches = (
            historical,
            not historical and (not public or not private),
            not historical and public and private and state == "not_run",
            not historical and public and private and state == "descendant",
            not historical and public and private and state == "unknown",
            not historical and public and private and state == "passed",
        )
        matched = tuple(index for index, value in enumerate(row_matches) if value)
        overlap_count += len(matched) > 1
        uncovered_count += not matched
        if len(matched) == 1:
            row_counts[matched[0]] += 1
        expected = observation.DIRECT_INTERPRETER_PREFLIGHT_OUTCOMES[matched[0]]
        assert observation.select_direct_interpreter_preflight_outcome(
            historical,
            public,
            private,
            state,
        ) == expected

    assert [row_counts[index] for index in range(6)] == [16, 12, 1, 1, 1, 1]
    assert overlap_count == 0
    assert uncovered_count == 0
    assert all(row_counts[index] > 0 for index in range(6))
    with pytest.raises(ValueError, match="boolean_invalid"):
        observation.select_direct_interpreter_preflight_outcome(1, True, True, "passed")
    with pytest.raises(ValueError, match="state_invalid"):
        observation.select_direct_interpreter_preflight_outcome(
            False,
            True,
            True,
            "retry",
        )


def test_predeclared_identities_derive_from_exact_preimages() -> None:
    preimages = (
        "trusted_owner_r0_offline_direct_interpreter_sequence.v1|"
        "1235264383|776|780|"
        + observation.RELEASE_RECORD_SHA256
        + "|"
        + observation.HISTORICAL_SEQUENCE_ID
        + "|"
        + observation.HISTORICAL_CONSUMPTION_SHA256
        + "|"
        + observation.DIRECT_INTERPRETER_BINDING_SHA256,
        "trusted_owner_r0_offline_direct_interpreter_observation.v1|"
        "1235264383|776|780|"
        + observation.SEQUENCE_ID
        + "|1",
        "trusted_owner_r0_offline_direct_interpreter_observation.v1|"
        "1235264383|776|780|"
        + observation.SEQUENCE_ID
        + "|2",
    )
    derived = tuple(hashlib.sha256(value.encode("ascii")).hexdigest()[:32] for value in preimages)
    assert observation.SEQUENCE_ID.endswith(derived[0])
    assert observation.OBSERVATION_IDS[0].endswith(derived[1])
    assert observation.OBSERVATION_IDS[1].endswith(derived[2])


@pytest.mark.parametrize("position", [1, 2])
def test_receipt_known_answers_are_byte_exact(position: int) -> None:
    receipt = observation.EXPECTED_RECEIPTS[position - 1]
    payload = observation.canonical_bytes(receipt)
    preimage = observation.canonical_bytes(
        {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    )
    assert tuple(receipt) == observation.RECEIPT_FIELDS
    assert len(preimage) == observation.EXPECTED_RECEIPT_PREIMAGE_LENGTHS[position - 1]
    assert len(payload) == observation.EXPECTED_RECEIPT_LENGTHS[position - 1]
    assert receipt["receipt_sha256"] == observation.EXPECTED_RECEIPT_SHA256S[position - 1]
    assert hashlib.sha256(payload).hexdigest() == observation.EXPECTED_RECEIPT_ARTIFACT_SHA256S[position - 1]
    assert observation.parse_receipt(payload) == receipt
    assert all(value is False for value in receipt["authority_flags"].values())


def test_receipt_parser_rejects_duplicate_unknown_reordered_mistyped_and_mutated() -> None:
    original = observation.EXPECTED_RECEIPTS[0]
    payload = observation.canonical_bytes(original)
    duplicate = payload.replace(
        b'{"schema_version":',
        b'{"schema_version":"duplicate","schema_version":',
        1,
    )
    unknown = copy.deepcopy(original)
    unknown["unexpected"] = False
    reordered = {key: original[key] for key in reversed(original)}
    mistyped = copy.deepcopy(original)
    mistyped["sequence_position"] = True
    mutated = copy.deepcopy(original)
    mutated["network_operation_count"] = 1
    for candidate in (
        duplicate,
        observation.canonical_bytes(unknown),
        observation.canonical_bytes(reordered),
        observation.canonical_bytes(mistyped),
        observation.canonical_bytes(mutated),
    ):
        with pytest.raises(observation.ObservationFailure):
            observation.parse_receipt(candidate)


def test_receipt_pair_requires_exact_chronology_independent_of_digest_order() -> None:
    first, second = _receipt_bytes(1), _receipt_bytes(2)
    receipts = observation.validate_receipt_pair((first, second))
    assert tuple(item["receipt_sha256"] for item in receipts) == (
        observation.EXPECTED_RECEIPT_SHA256S
    )
    assert observation.EXPECTED_RECEIPT_SHA256S == tuple(
        sorted(observation.EXPECTED_RECEIPT_SHA256S)
    )
    bytewise_sorted = tuple(
        sorted(
            (first, second),
            key=lambda payload: json.loads(payload)["receipt_sha256"],
        )
    )
    assert bytewise_sorted == (first, second)

    def mutated(position: int, **updates: object) -> bytes:
        receipt = copy.deepcopy(observation.EXPECTED_RECEIPTS[position - 1])
        receipt.update(updates)
        receipt["receipt_sha256"] = observation.self_digest(
            receipt,
            "receipt_sha256",
        )
        return observation.canonical_bytes(receipt)

    candidates = (
        (second, first),
        (first, first),
        (second, second),
        (first,),
        (mutated(1, current_rung="R1"), second),
        (mutated(1, sequence_position=2), second),
        (mutated(1, sequence_id=observation.HISTORICAL_SEQUENCE_ID), second),
        (mutated(1, observation_id="r0.offline.observation.substituted"), second),
        (mutated(1, observation_profile_sha256="0" * 64), second),
        (first, mutated(2, predecessor_observation_id=None)),
    )
    for candidate in candidates:
        with pytest.raises(observation.ObservationFailure):
            observation.validate_receipt_pair(candidate)

    old_first = copy.deepcopy(observation.EXPECTED_RECEIPTS[0])
    old_first["sequence_id"] = observation.HISTORICAL_SEQUENCE_ID
    old_first["observation_id"] = observation.HISTORICAL_OBSERVATION_IDS[0]
    old_first["observation_profile_sha256"] = (
        "0d97f23b96dfab5b6b459bea92df63a8bc6675c50632ace60a36f7e1cbea2124"
    )
    old_first["receipt_sha256"] = observation.self_digest(
        old_first,
        "receipt_sha256",
    )
    with pytest.raises(observation.ObservationFailure):
        observation.validate_receipt_pair(
            (observation.canonical_bytes(old_first), second)
        )


def test_receipt_pair_selector_covers_all_64_tuples_without_lexical_authority() -> None:
    row_counts: Counter[int] = Counter()
    overlap_count = 0
    uncovered_count = 0
    for values in itertools.product((False, True), repeat=6):
        row_matches = (
            not values[0],
            values[0] and not values[1],
            all(values[:2]) and not values[2],
            all(values[:3]) and not values[3],
            all(values[:4]) and not values[4],
            all(values[:5]),
        )
        matched_rows = tuple(
            index for index, matched in enumerate(row_matches) if matched
        )
        overlap_count += len(matched_rows) > 1
        uncovered_count += not matched_rows
        if len(matched_rows) == 1:
            row_counts[matched_rows[0]] += 1
        expected = (
            "accepted_exact_chronological_receipt_pair"
            if all(values[:5])
            else "observation_sequence_rejected"
        )
        assert observation.select_receipt_pair_outcome(*values) == expected

    assert [row_counts[index] for index in range(6)] == [32, 16, 8, 4, 2, 2]
    assert overlap_count == 0
    assert uncovered_count == 0
    assert all(row_counts[index] > 0 for index in range(6))
    assert observation.select_receipt_pair_outcome(True, True, True, True, True, False) == (
        "accepted_exact_chronological_receipt_pair"
    )
    assert observation.select_receipt_pair_outcome(True, True, True, True, True, True) == (
        "accepted_exact_chronological_receipt_pair"
    )
    with pytest.raises(observation.ObservationFailure):
        observation.select_receipt_pair_outcome(True, True, True, True, True, 1)


def test_consumption_known_answer_is_exact_and_nonpublishable() -> None:
    packet = observation.SYNTHETIC_CONSUMPTION_KAT
    payload = observation.canonical_bytes(packet)
    preimage = observation.canonical_bytes(
        {key: value for key, value in packet.items() if key != "consumption_sha256"}
    )
    assert tuple(packet) == observation.CONSUMPTION_FIELDS
    assert len(preimage) == 2531
    assert len(payload) == 2619
    assert packet["consumption_sha256"] == (
        "b49572e1faad02c68270c0832dc86158da3b24d2eff5772669521a7e53955efa"
    )
    assert hashlib.sha256(payload).hexdigest() == (
        "d3e1f80d0c755c65c8c9cb905275cff09ca92c38f2bb662ddcd553de08d1e360"
    )
    assert packet["sequence_contract_review_ref"].startswith(
        "https://github.com/Tahjali11/Mythic-Edge/issues/780#"
    )
    assert observation.parse_consumption(payload, expected=packet) == packet
    with pytest.raises(observation.ObservationFailure) as error:
        observation.parse_consumption(payload, expected={**packet, "harness_sha256": "8" * 64})
    assert error.value.status == "observation_binding_rejected"


def test_consumption_parser_rejects_duplicate_reordered_wrong_type_and_digest() -> None:
    packet = _consumption()
    payload = observation.canonical_bytes(packet)
    duplicate = payload.replace(
        b'{"schema_version":',
        b'{"schema_version":"duplicate","schema_version":',
        1,
    )
    reordered = {key: packet[key] for key in reversed(packet)}
    wrong_type = copy.deepcopy(packet)
    wrong_type["attempt_limit"] = True
    wrong_type["consumption_sha256"] = observation.self_digest(
        wrong_type,
        "consumption_sha256",
    )
    wrong_digest = copy.deepcopy(packet)
    wrong_digest["consumption_sha256"] = "0" * 64
    for candidate in (
        duplicate,
        observation.canonical_bytes(reordered),
        observation.canonical_bytes(wrong_type),
        observation.canonical_bytes(wrong_digest),
    ):
        with pytest.raises(observation.ObservationFailure):
            observation.parse_consumption(candidate)


def test_consumption_selector_exhaustively_covers_fifteen_tuples() -> None:
    outputs = Counter(
        observation.select_consumption_outcome(call, state)
        for call, state in itertools.product(
            observation.CONSUMPTION_CALL_RESULTS,
            observation.CONSUMPTION_COMMENT_STATES,
        )
    )
    assert sum(outputs.values()) == 15
    assert [outputs[name] for name in observation.CONSUMPTION_TERMINALS] == [2, 1, 5, 4, 3]
    assert set(outputs) == set(observation.CONSUMPTION_TERMINALS)


@pytest.mark.parametrize(
    ("call_result", "comment_state", "expected"),
    [
        ("reported_success", "exact_one", "consumed_exact_nonreusable"),
        ("known_failure", "none", "consumption_failed_nonreusable"),
        ("reported_success", "none", "consumption_collision_nonreusable"),
        ("reported_success", "unique_invalid", "consumption_readback_failed_nonreusable"),
        ("unknown", "none", "consumption_ambiguous_nonreusable"),
    ],
)
def test_fake_consumption_transport_is_single_post_single_read(
    call_result: str,
    comment_state: str,
    expected: str,
) -> None:
    class FakeTransport:
        def __init__(self) -> None:
            self.posts = 0
            self.reads = 0

        def post_once(self) -> str:
            self.posts += 1
            return call_result

        def enumerate_once(self) -> str:
            self.reads += 1
            return comment_state

    transport = FakeTransport()
    result = observation.select_consumption_outcome(
        transport.post_once(),
        transport.enumerate_once(),
    )
    assert result == expected
    assert (transport.posts, transport.reads) == (1, 1)


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ({"exact_receipt": True}, "completed_no_relaunch"),
        ({"exact_consumption": True}, "consumed_without_accepted_receipt_nonreusable"),
        ({"collision": True}, "consumption_collision_nonreusable"),
        (
            {"prior_post_entry": True, "state_available": True},
            "consumption_absent_after_attempt_nonreusable",
        ),
        ({}, "consumption_ambiguous_nonreusable"),
    ],
)
def test_fresh_task_reconciliation_is_terminal_and_never_relaunches(
    values: dict[str, bool],
    expected: str,
) -> None:
    inputs = {
        "exact_receipt": False,
        "exact_consumption": False,
        "collision": False,
        "prior_post_entry": False,
        "state_available": False,
    }
    inputs.update(values)
    assert observation.reconcile_consumption(**inputs) == expected
    assert "relaunch" not in expected or expected == "completed_no_relaunch"


def test_sequence_preflight_binds_single_use_and_observation_two_predecessors() -> None:
    first = _consumption(1)
    second = _consumption(2)
    observation.validate_sequence_preflight(
        observation.OBSERVATION_IDS[0],
        consumption=first,
    )
    observation.validate_sequence_preflight(
        observation.OBSERVATION_IDS[1],
        consumption=second,
        predecessor_consumption_sha256="7" * 64,
        predecessor_receipt=_receipt_bytes(1),
    )
    with pytest.raises(observation.ObservationFailure):
        observation.validate_sequence_preflight(
            observation.OBSERVATION_IDS[1],
            consumption=second,
            predecessor_consumption_sha256="8" * 64,
            predecessor_receipt=_receipt_bytes(1),
        )
    with pytest.raises(observation.ObservationFailure):
        observation.validate_sequence_preflight(
            observation.OBSERVATION_IDS[1],
            consumption=second,
            predecessor_consumption_sha256="7" * 64,
            predecessor_receipt=_receipt_bytes(2),
        )


@pytest.mark.parametrize(
    ("call_result", "comment_state", "expected"),
    [
        ("reported_success", "exact_one", "accepted_exact_r0_offline_observation"),
        ("unknown", "exact_one", "accepted_exact_r0_offline_observation"),
        ("reported_success", "none", "observation_receipt_readback_failed"),
        ("unknown", "none", "observation_publication_unknown"),
        ("known_failure", "none", "observation_publication_unknown"),
        ("reported_success", "multiple_or_conflicting", "observation_receipt_collision"),
    ],
)
def test_fake_receipt_publication_is_bounded_and_fail_closed(
    call_result: str,
    comment_state: str,
    expected: str,
) -> None:
    assert observation.classify_publication(call_result, comment_state) == expected
    observation.require_publication_issue(776)
    with pytest.raises(observation.ObservationFailure):
        observation.require_publication_issue(769)


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({"public_binding_exact": False}, "observation_binding_rejected"),
        ({"authority_exact": False}, "observation_authority_rejected"),
        ({"sequence_exact": False}, "observation_sequence_rejected"),
        ({"consumption_status": "consumption_collision_nonreusable"}, "consumption_collision_nonreusable"),
        ({"consumption_status": "consumption_failed_nonreusable"}, "consumption_failed_nonreusable"),
        ({"consumption_status": "consumption_ambiguous_nonreusable"}, "consumption_ambiguous_nonreusable"),
        ({"consumption_status": "consumption_readback_failed_nonreusable"}, "consumption_readback_failed_nonreusable"),
        ({"host_exact": False}, "observation_host_rejected"),
        ({"launch_status": "unknown"}, "observation_launch_unknown"),
        ({"safety_boundary_exact": False}, "observation_safety_boundary_failed"),
        ({"timeout_status": "expired"}, "observation_timeout_unknown"),
        ({"result_status": "unknown"}, "observation_result_unknown"),
        ({"result_status": "invalid"}, "observation_validation_failed"),
        ({"sealing_exact": False}, "observation_receipt_sealing_failed"),
        ({"publication_status": "collision"}, "observation_receipt_collision"),
        ({"publication_status": "unknown"}, "observation_publication_unknown"),
        ({"readback_exact": False}, "observation_receipt_readback_failed"),
        ({}, "accepted_exact_r0_offline_observation"),
    ],
)
def test_every_lifecycle_status_is_reachable_with_first_failure_precedence(
    changes: dict[str, object],
    expected: str,
) -> None:
    assert observation.select_lifecycle_status(_lifecycle_state(**changes)) == expected


def test_lifecycle_first_failure_and_closed_fields_are_deterministic() -> None:
    state = _lifecycle_state(
        public_binding_exact=False,
        authority_exact=False,
        sequence_exact=False,
        consumption_status="consumption_collision_nonreusable",
        host_exact=False,
    )
    assert observation.select_lifecycle_status(state) == "observation_binding_rejected"
    state["unexpected"] = False
    with pytest.raises(ValueError, match="lifecycle_fields_invalid"):
        observation.select_lifecycle_status(state)


@pytest.mark.parametrize(
    ("event", "args", "counter"),
    [
        ("subprocess.Popen", ("private-command",), "process_launch_attempt_count"),
        ("os.spawnv", (0, "private-command", ()), "process_launch_attempt_count"),
        ("os.startfile", ("private-command",), "process_launch_attempt_count"),
        ("os.startfile/2", ("private-command", None), "process_launch_attempt_count"),
        ("socket.connect", (object(), ("private-host", 443)), "network_operation_count"),
        ("os.putenv", ("PRIVATE", "private-value"), "external_effect_count"),
    ],
)
def test_audit_boundary_rejects_process_network_and_environment_without_echo(
    event: str,
    args: tuple[object, ...],
    counter: str,
) -> None:
    audit = observation.AuditBoundary(REPO_ROOT, (Path(sys.base_prefix),))
    with pytest.raises(observation.SafetyBoundaryViolation) as error:
        audit(event, args)
    assert str(error.value) == "observation_safety_boundary_failed"
    assert getattr(audit, counter) == 1
    assert "private" not in str(error.value).lower()


def test_audit_boundary_rejects_writes_and_out_of_scope_expansion() -> None:
    audit = observation.AuditBoundary(REPO_ROOT, (Path(sys.base_prefix),))
    with pytest.raises(observation.SafetyBoundaryViolation):
        audit("open", (REPO_ROOT / "forbidden.txt", "w", os.O_WRONLY))
    assert audit.repository_write_count == 1
    installed_root = REPO_ROOT.parent / "synthetic-installed"
    audit.bind_installed_root(installed_root)
    with pytest.raises(observation.SafetyBoundaryViolation):
        audit("os.remove", (installed_root / "forbidden",))
    assert audit.installed_write_count == 1
    with pytest.raises(observation.SafetyBoundaryViolation):
        audit("os.scandir", (REPO_ROOT.parent,))
    assert audit.external_effect_count == 1
    audit("open", (MODULE_PATH, "r", os.O_RDONLY))
    audit("os.scandir", (REPO_ROOT,))


def test_stable_payload_refuses_reparse_before_opening() -> None:
    fake_stat = SimpleNamespace(
        st_mode=stat.S_IFREG,
        st_file_attributes=getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400),
        st_dev=1,
        st_ino=1,
        st_size=1,
        st_mtime_ns=1,
    )
    with (
        mock.patch.object(Path, "lstat", return_value=fake_stat),
        mock.patch.object(Path, "open", side_effect=AssertionError("must not open")),
        pytest.raises(observation.ObservationFailure) as error,
    ):
        observation._stable_payload(MODULE_PATH)
    assert error.value.status == "observation_binding_rejected"


def test_exact_in_process_owner_call_graph_projects_only_expected_receipt() -> None:
    checker = _FakeChecker()
    roots = _fake_roots()
    audit = observation.AuditBoundary(REPO_ROOT, (Path(sys.base_prefix),))
    audit.bind_installed_root(roots.installed_skills_root)
    payload = observation.evaluate_observation(
        observation.OBSERVATION_IDS[0],
        checker=checker,
        roots=roots,
        audit_boundary=audit,
        runtime_os_name="nt",
        runtime_sys_platform="win32",
    )
    assert payload == _receipt_bytes(1)
    assert checker.calls[0] == "evaluate_roots"
    assert "load_owner_modules" in checker.calls
    assert checker.calls[-1] == "offline_validation"
    assert audit.forbidden_attempt_count == 0


@pytest.mark.parametrize(("os_name", "platform"), [("posix", "win32"), ("nt", "linux")])
def test_trusted_runtime_rejects_non_windows_before_owner_evaluation(
    os_name: str,
    platform: str,
) -> None:
    checker = _FakeChecker()
    audit = observation.AuditBoundary(REPO_ROOT, (Path(sys.base_prefix),))
    with pytest.raises(observation.ObservationFailure) as error:
        observation.evaluate_observation(
            observation.OBSERVATION_IDS[0],
            checker=checker,
            roots=_fake_roots(),
            audit_boundary=audit,
            runtime_os_name=os_name,
            runtime_sys_platform=platform,
        )
    assert error.value.status == "observation_host_rejected"
    assert checker.calls == []


def test_owner_projection_drift_fails_without_receipt() -> None:
    checker = _FakeChecker()
    original = checker._evaluate_roots

    def drifted(roots: object) -> tuple[dict[str, object], bytes]:
        packet, encoded = original(roots)
        packet["registry_sha256"] = "0" * 64
        return packet, encoded

    checker._evaluate_roots = drifted  # type: ignore[method-assign]
    with pytest.raises(observation.ObservationFailure) as error:
        observation.evaluate_observation(
            observation.OBSERVATION_IDS[0],
            checker=checker,
            roots=_fake_roots(),
            audit_boundary=observation.AuditBoundary(
                REPO_ROOT,
                (Path(sys.base_prefix),),
            ),
            runtime_os_name="nt",
            runtime_sys_platform="win32",
        )
    assert error.value.status == "observation_validation_failed"


def test_current_release_uses_existing_owner_validation_and_exact_r0_ceiling() -> None:
    checker_spec = importlib.util.spec_from_file_location(
        "_test_r0_checker_owner",
        REPO_ROOT / observation.R0_CHECKER_RELATIVE_PATH,
    )
    assert checker_spec is not None and checker_spec.loader is not None
    checker = importlib.util.module_from_spec(checker_spec)
    sys.modules[checker_spec.name] = checker
    checker_spec.loader.exec_module(checker)
    owners = checker._load_owner_modules(REPO_ROOT)
    release = (REPO_ROOT / checker.RELEASE_STATE_RELATIVE_PATH).read_bytes()
    records = [
        owners.pool.parse_trusted_native_json(line.decode("utf-8"))
        for line in release.splitlines(keepends=True)
    ]
    assert all(not owners.pool.validate_trusted_native_release_record(item) for item in records)
    assert owners.pool.validate_trusted_native_release_chain(records) == []
    assert owners.pool.trusted_native_current_rung(records) == "R0"
    assert owners.pool.validate_trusted_native_release_ceiling(
        "R0",
        mode="offline",
        role=None,
        lane_count=0,
        wave_count=0,
        operation_id="offline_validation",
        claim_creation=False,
        task_creation=False,
        f_publication=False,
    ) == []


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({}, "accepted_exact_r0_offline_observation"),
        ({"timed_out": True}, "observation_timeout_unknown"),
        ({"cleanup_confirmed": False}, "observation_timeout_unknown"),
        ({"exit_code": None}, "observation_launch_unknown"),
        ({"top_level_process_count": 0}, "observation_launch_unknown"),
        ({"descendant_process_count": 1}, "observation_safety_boundary_failed"),
        ({"output_complete": False}, "observation_result_unknown"),
        ({"stdout": b"x" * 4097}, "observation_result_unknown"),
        ({"stdout": b"invalid\n"}, "observation_validation_failed"),
    ],
)
def test_fake_launcher_enforces_process_timeout_output_and_cleanup_boundaries(
    changes: dict[str, object],
    expected: str,
) -> None:
    values: dict[str, object] = {
        "exit_code": 0,
        "stdout": _receipt_bytes(1),
        "stderr": b"",
        "top_level_process_count": 1,
        "descendant_process_count": 0,
        "timed_out": False,
        "cleanup_confirmed": True,
        "output_complete": True,
    }
    values.update(changes)
    result = observation.LauncherObservation(**values)
    assert observation.classify_launcher_observation(result) == expected


@pytest.mark.parametrize(
    ("direct_changes", "process_changes", "expected"),
    [
        ({}, {}, "accepted_exact_r0_offline_observation"),
        ({"public_binding_exact": False}, {}, "observation_binding_rejected"),
        ({"private_binding_exact": False}, {}, "observation_binding_rejected"),
        ({"top_level_identity_exact": False}, {}, "observation_launch_unknown"),
        ({"parentage_known": False}, {}, "observation_launch_unknown"),
        ({}, {"top_level_process_count": 0}, "observation_launch_unknown"),
        (
            {},
            {"descendant_process_count": 1},
            "observation_safety_boundary_failed",
        ),
        ({}, {"timed_out": True}, "observation_timeout_unknown"),
        ({}, {"cleanup_confirmed": False}, "observation_timeout_unknown"),
        ({}, {"output_complete": False}, "observation_result_unknown"),
    ],
)
def test_fake_direct_launcher_binds_identity_parentage_timeout_and_cleanup(
    direct_changes: dict[str, object],
    process_changes: dict[str, object],
    expected: str,
) -> None:
    process_values: dict[str, object] = {
        "exit_code": 0,
        "stdout": _receipt_bytes(1),
        "stderr": b"",
        "top_level_process_count": 1,
        "descendant_process_count": 0,
        "timed_out": False,
        "cleanup_confirmed": True,
        "output_complete": True,
    }
    process_values.update(process_changes)
    direct_values: dict[str, object] = {
        "public_binding_exact": True,
        "private_binding_exact": True,
        "top_level_identity_exact": True,
        "parentage_known": True,
        "process": observation.LauncherObservation(**process_values),
    }
    direct_values.update(direct_changes)
    result = observation.DirectLauncherObservation(**direct_values)
    assert observation.classify_direct_launcher_observation(result) == expected


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({}, "direct_interpreter_preflight_passed"),
        ({"public_binding_exact": False}, "observation_binding_rejected"),
        ({"private_binding_exact": False}, "observation_binding_rejected"),
        (
            {"top_level_identity_exact": False},
            "direct_interpreter_preflight_unknown",
        ),
        ({"parentage_known": False}, "direct_interpreter_preflight_unknown"),
        ({"exit_code": None}, "direct_interpreter_preflight_unknown"),
        ({"exit_code": 1}, "direct_interpreter_preflight_unknown"),
        ({"top_level_process_count": 0}, "direct_interpreter_preflight_unknown"),
        (
            {"descendant_process_count": 1},
            "direct_interpreter_preflight_descendant_observed",
        ),
        ({"timed_out": True}, "direct_interpreter_preflight_unknown"),
        ({"cleanup_confirmed": False}, "direct_interpreter_preflight_unknown"),
        ({"output_complete": False}, "direct_interpreter_preflight_unknown"),
        ({"stdout": b"unexpected"}, "direct_interpreter_preflight_unknown"),
        ({"stderr": b"unexpected"}, "direct_interpreter_preflight_unknown"),
    ],
)
def test_fake_direct_preflight_is_one_process_zero_output_no_retry(
    changes: dict[str, object],
    expected: str,
) -> None:
    values: dict[str, object] = {
        "public_binding_exact": True,
        "private_binding_exact": True,
        "top_level_identity_exact": True,
        "parentage_known": True,
        "exit_code": 0,
        "stdout": b"",
        "stderr": b"",
        "top_level_process_count": 1,
        "descendant_process_count": 0,
        "timed_out": False,
        "cleanup_confirmed": True,
        "output_complete": True,
    }
    values.update(changes)
    result = observation.DirectPreflightObservation(**values)
    assert observation.classify_direct_preflight_observation(result) == expected


def test_cli_invalid_identity_is_symbolic_no_echo_and_does_not_load_owner() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with (
        mock.patch.object(observation, "_load_checker", side_effect=AssertionError),
        mock.patch.object(observation.sys, "stdout", stdout),
        mock.patch.object(observation.sys, "stderr", stderr),
    ):
        exit_code = observation.run(["C:\\private\\identity"])
    assert exit_code == 2
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_sequence_rejected\n"
    assert "private" not in stderr.getvalue().lower()


def test_cli_rejects_wrong_working_directory_before_owner_load(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    monkeypatch.setattr(observation.os, "name", "nt")
    monkeypatch.setattr(observation.sys, "platform", "win32")
    monkeypatch.setattr(observation.sys, "dont_write_bytecode", True)
    monkeypatch.setattr(observation.os, "getcwd", lambda: str(REPO_ROOT.parent))
    monkeypatch.setattr(
        observation,
        "_load_checker",
        mock.Mock(side_effect=AssertionError("must not load")),
    )
    monkeypatch.setattr(
        observation,
        "validate_running_direct_interpreter",
        mock.Mock(side_effect=AssertionError("must not inspect")),
    )
    monkeypatch.setattr(observation.sys, "stdout", stdout)
    monkeypatch.setattr(observation.sys, "stderr", stderr)
    assert observation.run([observation.OBSERVATION_IDS[0]]) == 2
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_binding_rejected\n"


def test_cli_success_path_uses_fake_owner_and_emits_only_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    checker = _FakeChecker()
    roots = _fake_roots()
    checker._production_roots = lambda: roots  # type: ignore[attr-defined]
    stdout = io.StringIO()
    stderr = io.StringIO()
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    monkeypatch.setattr(observation.os, "name", "nt")
    monkeypatch.setattr(observation.sys, "platform", "win32")
    monkeypatch.setattr(observation.sys, "dont_write_bytecode", True)
    monkeypatch.setattr(observation.sys, "addaudithook", lambda hook: None)
    monkeypatch.setattr(
        observation,
        "validate_running_direct_interpreter",
        lambda: _direct_metadata(),
    )
    monkeypatch.setattr(observation, "_load_checker", lambda root: checker)
    monkeypatch.setattr(observation.sys, "stdout", stdout)
    monkeypatch.setattr(observation.sys, "stderr", stderr)
    assert observation.run([observation.OBSERVATION_IDS[0]]) == 0
    assert stdout.getvalue().encode("utf-8") == _receipt_bytes(1)
    assert stderr.getvalue() == ""


def test_cli_direct_interpreter_failure_precedes_owner_load_without_echo(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    monkeypatch.setattr(observation.os, "name", "nt")
    monkeypatch.setattr(observation.sys, "platform", "win32")
    monkeypatch.setattr(observation.sys, "dont_write_bytecode", True)
    monkeypatch.setattr(
        observation,
        "validate_running_direct_interpreter",
        mock.Mock(
            side_effect=observation.ObservationFailure(
                "observation_binding_rejected"
            )
        ),
    )
    owner = mock.Mock(side_effect=AssertionError("must not load"))
    monkeypatch.setattr(observation, "_load_checker", owner)
    monkeypatch.setattr(observation.sys, "stdout", stdout)
    monkeypatch.setattr(observation.sys, "stderr", stderr)
    assert observation.run([observation.OBSERVATION_IDS[0]]) == 2
    assert owner.call_count == 0
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_binding_rejected\n"


def test_cli_unknown_owner_failure_never_echoes_raw_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    checker = _FakeChecker()
    roots = _fake_roots()
    checker._production_roots = lambda: roots  # type: ignore[attr-defined]
    checker._evaluate_roots = mock.Mock(  # type: ignore[method-assign]
        side_effect=RuntimeError("C:\\private\\secret-value")
    )
    stdout = io.StringIO()
    stderr = io.StringIO()
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    monkeypatch.setattr(observation.os, "name", "nt")
    monkeypatch.setattr(observation.sys, "platform", "win32")
    monkeypatch.setattr(observation.sys, "dont_write_bytecode", True)
    monkeypatch.setattr(observation.sys, "addaudithook", lambda hook: None)
    monkeypatch.setattr(
        observation,
        "validate_running_direct_interpreter",
        lambda: _direct_metadata(),
    )
    monkeypatch.setattr(observation, "_load_checker", lambda root: checker)
    monkeypatch.setattr(observation.sys, "stdout", stdout)
    monkeypatch.setattr(observation.sys, "stderr", stderr)
    assert observation.run([observation.OBSERVATION_IDS[0]]) == 3
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_result_unknown\n"
    assert "private" not in stderr.getvalue().lower()


def test_fixed_owner_bindings_and_two_file_scope_remain_exact() -> None:
    bindings = {
        observation.SEQUENCE_CONTRACT_RELATIVE_PATH.as_posix(): observation.SEQUENCE_CONTRACT_SHA256,
        observation.RECEIPT_ORDER_CONTRACT_RELATIVE_PATH.as_posix(): observation.RECEIPT_ORDER_CONTRACT_SHA256,
        observation.RECEIPT_ORDER_REVIEW_RELATIVE_PATH.as_posix(): observation.RECEIPT_ORDER_REVIEW_SHA256,
        observation.DIRECT_INTERPRETER_CONTRACT_RELATIVE_PATH.as_posix(): (
            observation.DIRECT_INTERPRETER_CONTRACT_SHA256
        ),
        "docs/contracts/trusted_owner_native_role_pool_profile.md": observation.PROFILE_CONTRACT_SHA256,
        "docs/role_pool/trusted_owner_native_release_state.v1.jsonl": observation.RELEASE_STATE_ARTIFACT_SHA256,
        "docs/role_pool/trusted_owner_repository_registry.v1.json": observation.REGISTRY_ARTIFACT_SHA256,
        "tools/check_role_pool_r0_bootstrap.py": observation.R0_CHECKER_SHA256,
        "tests/test_check_role_pool_r0_bootstrap.py": observation.R0_CHECKER_TEST_SHA256,
        "docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py": observation.RELEASE_VALIDATOR_SHA256,
        "docs/role_pool_current_authority_index.md": observation.AUTHORITY_INDEX_SHA256,
    }
    assert all(
        hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest() == expected
        for path, expected in bindings.items()
    )
    assert observation.OBSERVATION_PROFILE["implementation_paths"] == [
        "tools/check_role_pool_r0_offline_observation.py",
        "tests/test_check_role_pool_r0_offline_observation.py",
    ]
    assert observation.DIRECT_INTERPRETER_REVIEWED_CONTRACT_SHA256 == (
        observation.DIRECT_INTERPRETER_CONTRACT_SHA256
    )


def test_no_runtime_function_mutates_repository_or_grants_authority() -> None:
    before = {
        path: hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
        for path in (
            "docs/contracts/trusted_owner_native_role_pool_profile.md",
            "docs/role_pool/trusted_owner_native_release_state.v1.jsonl",
            "docs/role_pool/trusted_owner_repository_registry.v1.json",
            "docs/role_pool_current_authority_index.md",
        )
    }
    observation.parse_receipt(_receipt_bytes(1))
    observation.parse_direct_interpreter_binding(
        observation.canonical_bytes(observation.DIRECT_INTERPRETER_BINDING)
    )
    observation.parse_consumption(observation.canonical_bytes(_consumption()))
    observation.select_direct_interpreter_preflight_outcome(
        False,
        True,
        True,
        "not_run",
    )
    observation.select_consumption_outcome("unknown", "none")
    observation.classify_publication("unknown", "none")
    after = {
        path: hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
        for path in before
    }
    assert before == after
    assert all(
        value is False
        for receipt in observation.EXPECTED_RECEIPTS
        for value in receipt["authority_flags"].values()
    )
