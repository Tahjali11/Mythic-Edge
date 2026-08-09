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
_REAL_SHA256 = hashlib.sha256
IMMUTABLE_R0_RELEASE_SHA256 = (
    "723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9"
)
IMMUTABLE_R0_RECORD_SHA256 = (
    "78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7"
)
IMMUTABLE_R0_RELEASE_LINE = (
    b'{"schema_version":"trusted_owner_native_release_record.v1"'
    b',"record_id":"r0.bootstrap.163224f847ac930a44e66aaa20f21543"'
    b',"predecessor_record_sha256":null,"from_rung":null,"to_rung":"R0"'
    b',"contract_sha256":"944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f"'
    b',"skill_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f"'
    b',"registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7"'
    b',"validator_bundle_sha256":"ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5"'
    b',"observation_receipt_sha256s":[]'
    b',"codex_e_review_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5142157228"'
    b',"codex_e_review_sha256":"d5f1aeff5ac90d0ff00fd0e43386aed2057f93729d3b98a1fc6c3fedbf70f3ee"'
    b',"owner_decision_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5142216555"'
    b',"accepted_at_utc":"2026-07-31T11:09:36Z"'
    b',"record_sha256":"78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7"}\n'
)
IMMUTABLE_R0_FIELD_ORDER = (
    "schema_version",
    "record_id",
    "predecessor_record_sha256",
    "from_rung",
    "to_rung",
    "contract_sha256",
    "skill_tree_sha256",
    "registry_sha256",
    "validator_bundle_sha256",
    "observation_receipt_sha256s",
    "codex_e_review_ref",
    "codex_e_review_sha256",
    "owner_decision_ref",
    "accepted_at_utc",
    "record_sha256",
)
SUCCESSOR_PROFILE_SHA256 = (
    "8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952"
)
SUCCESSOR_TREE_SHA256 = (
    "3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6"
)
SUCCESSOR_REGISTRY_SHA256 = (
    "93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7"
)
LIVE_IDENTITY_TOKEN = "1" * 32
LIVE_OBSERVATION_ID = (
    "r0.app_native.offline.observation.1." + LIVE_IDENTITY_TOKEN
)


class _FixedSha256:
    def __init__(self, digest: str) -> None:
        self._digest = digest

    def hexdigest(self) -> str:
        return self._digest

    def digest(self) -> bytes:
        return bytes.fromhex(self._digest)


class _PathBoundPayload(bytes):
    relative_path: Path

    def __new__(cls, payload: bytes, relative_path: Path) -> object:
        value = super().__new__(cls, payload)
        value.relative_path = relative_path
        return value


def _signed(document: dict[str, object], field: str) -> dict[str, object]:
    result = copy.deepcopy(document)
    result[field] = observation.self_digest(result, field)
    return result


def _real_checker_and_pool() -> tuple[object, object]:
    checker_spec = importlib.util.spec_from_file_location(
        "_test_r0_checker_owner",
        REPO_ROOT / observation.R0_CHECKER_RELATIVE_PATH,
    )
    assert checker_spec is not None and checker_spec.loader is not None
    checker = importlib.util.module_from_spec(checker_spec)
    sys.modules[checker_spec.name] = checker
    checker_spec.loader.exec_module(checker)
    return checker, checker._load_owner_modules(REPO_ROOT).pool


def _immutable_r0_record(pool: object) -> dict[str, object]:
    assert len(IMMUTABLE_R0_RELEASE_LINE) == 981
    assert IMMUTABLE_R0_RELEASE_LINE.endswith(b"\n")
    assert b"\r" not in IMMUTABLE_R0_RELEASE_LINE
    assert hashlib.sha256(IMMUTABLE_R0_RELEASE_LINE).hexdigest() == (
        IMMUTABLE_R0_RELEASE_SHA256
    )
    record = pool.parse_trusted_native_json(
        IMMUTABLE_R0_RELEASE_LINE.decode("utf-8")
    )
    assert tuple(record) == IMMUTABLE_R0_FIELD_ORDER
    assert record["record_sha256"] == IMMUTABLE_R0_RECORD_SHA256
    assert pool.trusted_native_self_digest(record, "record_sha256") == (
        IMMUTABLE_R0_RECORD_SHA256
    )
    assert pool.trusted_native_canonical_bytes(record) == IMMUTABLE_R0_RELEASE_LINE
    assert pool.validate_trusted_native_release_record(record) == []
    assert pool.validate_trusted_native_release_state_record(record) == []
    assert pool.validate_trusted_native_release_chain([record]) == []
    return record


def _current_validator_bundle(checker: object, pool: object) -> str:
    checker_path = REPO_ROOT / observation.R0_CHECKER_RELATIVE_PATH
    checker_test_path = REPO_ROOT / "tests/test_check_role_pool_r0_bootstrap.py"
    return checker._validator_bundle(
        hashlib.sha256(checker_path.read_bytes()).hexdigest(),
        hashlib.sha256(checker_test_path.read_bytes()).hexdigest(),
        pool,
    )


def _validated_current_release(
    checker: object,
    pool: object,
) -> tuple[bytes, list[dict[str, object]], dict[str, object]]:
    payload = (REPO_ROOT / checker.RELEASE_STATE_RELATIVE_PATH).read_bytes()
    assert payload.endswith(b"\n")
    assert b"\r" not in payload
    lines = payload.splitlines(keepends=True)
    assert len(lines) in (1, 2)
    assert b"".join(lines) == payload
    assert lines[0] == IMMUTABLE_R0_RELEASE_LINE
    records = [
        pool.parse_trusted_native_json(line.decode("utf-8")) for line in lines
    ]
    assert all(
        pool.validate_trusted_native_release_state_record(record) == []
        for record in records
    )
    assert pool.validate_trusted_native_release_chain(records) == []
    assert pool.trusted_native_current_rung(records) == "R0"
    bindings = pool.trusted_native_current_release_bindings(records)
    assert bindings is not None
    if len(records) == 1:
        assert payload == IMMUTABLE_R0_RELEASE_LINE
        assert bindings["record_sha256"] == IMMUTABLE_R0_RECORD_SHA256
    else:
        predecessor, successor = records
        assert successor["schema_version"] == (
            "trusted_owner_native_release_rebaseline_record.v1"
        )
        assert successor["predecessor_record_sha256"] == (
            predecessor["record_sha256"]
        )
        assert successor["predecessor_contract_sha256"] == (
            predecessor["contract_sha256"]
        )
        assert successor["predecessor_skill_tree_sha256"] == (
            predecessor["skill_tree_sha256"]
        )
        assert successor["predecessor_registry_sha256"] == (
            predecessor["registry_sha256"]
        )
        assert successor["predecessor_validator_bundle_sha256"] == (
            predecessor["validator_bundle_sha256"]
        )
        assert successor["contract_sha256"] == SUCCESSOR_PROFILE_SHA256
        assert successor["skill_tree_sha256"] == SUCCESSOR_TREE_SHA256
        assert successor["registry_sha256"] == SUCCESSOR_REGISTRY_SHA256
        assert successor["validator_bundle_sha256"] == (
            _current_validator_bundle(checker, pool)
        )
        assert successor["observation_receipt_sha256s"] == []
        assert bindings["record_sha256"] == successor["record_sha256"]
    return payload, records, bindings


def _assert_authority_index_semantics(payload: bytes) -> None:
    assert payload.endswith(b"\n")
    assert b"\r" not in payload
    text = payload.decode("ascii")
    lines = text.splitlines()
    assert lines[0] == "# Role Pool Current-Authority Index"
    table_heading = "## Authority And Lifecycle Inventory"
    table_header = (
        "| surface_or_artifact_family | classification | canonical_reference | "
        "observed_lifecycle_state | authority_effect_or_explicit_non_effect | "
        "refresh_trigger |"
    )
    table_separator = "| --- | --- | --- | --- | --- | --- |"
    assert lines.count(table_heading) == 1
    assert lines.count(table_header) == 1
    header_index = lines.index(table_header)
    assert lines[header_index - 2] == table_heading
    assert lines[header_index + 1] == table_separator

    rows: list[tuple[str, ...]] = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        cells = tuple(cell.strip() for cell in line[1:-1].split("|"))
        assert len(cells) == 6
        rows.append(cells)
    assert rows
    release_rows = [
        row for row in rows if row[0] == "`trusted_owner_release_state`"
    ]
    assert len(release_rows) == 1
    release_row = release_rows[0]
    assert release_row[:4] == (
        "`trusted_owner_release_state`",
        "`current_normative_authority`",
        "`docs/role_pool/trusted_owner_native_release_state.v1.jsonl`",
        "`active_r0_offline_only_release_state`",
    )
    assert "R0 permits offline validation only" in release_row[4]
    assert (
        "creates no process, task, claim, command, dispatch, R1-R8, Stage-4, "
        "or readiness authority"
    ) in release_row[4]
    assert "First release-record byte change" in release_row[5]

    no_authority_heading = "## No Authority Or Readiness Claim"
    assert lines.count(no_authority_heading) == 1
    no_authority_index = lines.index(no_authority_heading)
    assert no_authority_index > header_index
    no_authority_text = "\n".join(lines[no_authority_index + 1 :])
    assert "This index is navigational only." in no_authority_text
    assert "R1-R8 advancement" in no_authority_text
    assert "readiness" in no_authority_text


def _receipt_bytes(position: int, variant: int = 0) -> bytes:
    return observation.canonical_bytes(
        observation.EXPECTED_RECEIPTS[position - 1][variant]
    )


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
    if position != 1:
        raise ValueError("observation_position_invalid")
    packet = copy.deepcopy(observation.SYNTHETIC_CONSUMPTION_KAT)
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
    packet: dict[str, object] = {
        "schema_version": "trusted_owner_r0_offline_bootstrap_evidence.v1",
        "operation": "evaluate_r0_bootstrap_eligibility_read_only",
        "repository_id": observation.REPOSITORY_ID,
        "repository_name": "tahjali11/mythic-edge",
        "issue_url": "https://github.com/Tahjali11/Mythic-Edge/issues/761",
        "base_commit": "ad88b264a1c7947682a00b11c4a57963a43b7548",
        "profile_contract_sha256": observation.PROFILE_CONTRACT_SHA256,
        "app_server_contract_sha256": (
            "814ac91c4e099216ae4870458d7524a3d65bfba7459cbfda7de82a5fc79067e8"
        ),
        "r0_contract_sha256": (
            "ef440f1fe4ce9b0fd342057864e41cbdef93c1ac12ea85a1f9d01912eec4cd02"
        ),
        "contract_binding_status": "exact",
        "stage3_manifest_file_count": 41,
        "stage3_manifest_byte_count": 6052,
        "stage3_manifest_sha256": (
            "9109457e5897139658183595fb11c8a7bf9d66e4fb5b5fe6842b20bac43fbce2"
        ),
        "manifest_status": "exact",
        "source_tree_node_count": 43,
        "source_tree_file_count": 38,
        "source_tree_manifest_byte_count": 6840,
        "source_tree_sha256": observation.SOURCE_TREE_SHA256,
        "installed_tree_node_count": 43,
        "installed_tree_file_count": 38,
        "installed_tree_manifest_byte_count": 6840,
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
        "evidence_sha256": "",
    }
    packet["evidence_sha256"] = observation.self_digest(packet, "evidence_sha256")
    return packet


def _validation_payload() -> bytes:
    return observation.canonical_bytes(_bootstrap_packet())


def _post_exit_facts(**changes: object) -> object:
    values: dict[str, object] = {
        "top_level_process_count": 1,
        "descendant_process_count": 0,
        "process_relationships_known": True,
        "process_terminal_states_known": True,
        "surviving_process_count": 0,
        "top_level_identity_exact": None,
        "timed_out": False,
        "termination_uncertain": False,
        "cleanup_confirmed": True,
        "output_complete": True,
        "executor_network_operation_count": 0,
        "repository_write_count": 0,
        "installed_write_count": 0,
        "external_effect_count": 0,
        "generated_residue_count": 0,
    }
    values.update(changes)
    return observation.PostExitFacts(**values)


def _launcher_observation(**changes: object) -> object:
    values: dict[str, object] = {
        "exit_code": 0,
        "stdout": _validation_payload(),
        "stderr": b"",
        **_post_exit_facts().__dict__,
    }
    values.update(changes)
    return observation.LauncherObservation(**values)


class _FakePool:
    @staticmethod
    def parse_trusted_native_json(text: str) -> dict[str, object]:
        value = json.loads(text)
        assert isinstance(value, dict)
        return value

    @staticmethod
    def validate_trusted_native_release_record(value: object) -> list[str]:
        return [] if isinstance(value, dict) else ["invalid"]

    validate_trusted_native_release_state_record = validate_trusted_native_release_record

    @staticmethod
    def validate_trusted_native_release_chain(value: object) -> list[str]:
        return [] if isinstance(value, list) and len(value) == 2 else ["invalid"]

    @staticmethod
    def trusted_native_current_rung(value: object) -> str | None:
        return "R0" if isinstance(value, list) and len(value) == 2 else None

    @staticmethod
    def trusted_native_current_release_bindings(value: object) -> dict[str, object] | None:
        if not isinstance(value, list) or len(value) != 2:
            return None
        return {
            "record_sha256": observation.RELEASE_RECORD_SHA256,
            "contract_sha256": observation.PROFILE_CONTRACT_SHA256,
            "skill_tree_sha256": observation.SOURCE_TREE_SHA256,
            "registry_sha256": observation.REGISTRY_SHA256,
            "validator_bundle_sha256": observation.VALIDATOR_BUNDLE_SHA256,
        }

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
        self._checker = b"synthetic historical R0 checker fixture"
        self._tests = b"synthetic historical R0 checker-test fixture"
        real_checker, _pool = _real_checker_and_pool()
        real_owners = real_checker._load_owner_modules(REPO_ROOT)
        self._owners = SimpleNamespace(
            pool=real_owners.pool,
            stage3=object(),
            installer=object(),
            direct_adapter=real_owners.direct_adapter,
        )

    def _evaluate_roots(self, roots: object) -> tuple[dict[str, object], bytes]:
        del roots
        self.calls.append("evaluate_roots")
        packet = _bootstrap_packet()
        return packet, observation.canonical_bytes(packet)

    def _load_owner_modules(self, root: Path) -> object:
        assert root == REPO_ROOT
        self.calls.append("load_owner_modules")
        return self._owners

    def _read_stable_file(self, path: Path) -> object:
        self.calls.append(f"read:{path.name}")
        relative_path = path.relative_to(REPO_ROOT)
        payloads = {
            self.RELEASE_STATE_RELATIVE_PATH: self._release,
            self.CHECKER_RELATIVE_PATH: self._checker,
            self.CHECKER_TEST_RELATIVE_PATH: self._tests,
        }
        payload = payloads[relative_path]
        if relative_path in (
            self.CHECKER_RELATIVE_PATH,
            self.CHECKER_TEST_RELATIVE_PATH,
        ):
            payload = _PathBoundPayload(payload, relative_path)
        return SimpleNamespace(state="exact", payload=payload)

    def _binding_status(self, root: Path) -> tuple[str, dict[str, str]]:
        assert root == REPO_ROOT
        self.calls.append("binding_status")
        return "exact", {"registry_validator": observation.RELEASE_VALIDATOR_SHA256}

    def _manifest_observation(self, stage3: object, workflow_root: Path) -> object:
        del stage3, workflow_root
        self.calls.append("manifest_observation")
        return SimpleNamespace(status="exact", file_count=41)

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


def _historical_owner_hashes(checker: _FakeChecker) -> object:
    expected = {
        checker.CHECKER_RELATIVE_PATH: (
            checker._checker,
            observation.R0_CHECKER_SHA256,
        ),
        checker.CHECKER_TEST_RELATIVE_PATH: (
            checker._tests,
            observation.R0_CHECKER_TEST_SHA256,
        ),
    }

    def synthetic_sha256(payload: bytes = b"") -> object:
        binding = expected.get(getattr(payload, "relative_path", None))
        if binding is not None and bytes(payload) == binding[0]:
            return _FixedSha256(binding[1])
        return _REAL_SHA256(payload)

    return mock.patch.object(
        observation.hashlib,
        "sha256",
        side_effect=synthetic_sha256,
    )


def test_historical_owner_hashes_require_exact_path_and_payload_pairs() -> None:
    checker = _FakeChecker()
    checker_payload = _PathBoundPayload(
        checker._checker,
        checker.CHECKER_RELATIVE_PATH,
    )
    test_payload = _PathBoundPayload(
        checker._tests,
        checker.CHECKER_TEST_RELATIVE_PATH,
    )
    wrong_path = _PathBoundPayload(
        checker._checker,
        checker.CHECKER_TEST_RELATIVE_PATH,
    )
    wrong_payload = _PathBoundPayload(
        checker._checker + b"-drift",
        checker.CHECKER_RELATIVE_PATH,
    )

    with _historical_owner_hashes(checker):
        assert observation.hashlib.sha256(checker_payload).hexdigest() == (
            observation.R0_CHECKER_SHA256
        )
        assert observation.hashlib.sha256(test_payload).hexdigest() == (
            observation.R0_CHECKER_TEST_SHA256
        )
        assert observation.hashlib.sha256(wrong_path).hexdigest() == (
            _REAL_SHA256(wrong_path).hexdigest()
        )
        assert observation.hashlib.sha256(wrong_payload).hexdigest() == (
            _REAL_SHA256(wrong_payload).hexdigest()
        )
        assert observation.hashlib.sha256(checker._checker).hexdigest() == (
            _REAL_SHA256(checker._checker).hexdigest()
        )


def test_authority_index_semantics_reject_keyword_only_bytes() -> None:
    fabricated = (
        b"docs/role_pool/trusted_owner_native_release_state.v1.jsonl\n"
        b"active_r0_offline_only_release_state\n"
        b"R0 permits offline validation only\n"
        b"R1-R8\n"
        b"readiness authority\n"
    )

    with pytest.raises(AssertionError):
        _assert_authority_index_semantics(fabricated)


def _fake_roots() -> object:
    return SimpleNamespace(
        repository_root=REPO_ROOT,
        installed_skills_root=REPO_ROOT / "synthetic-installed-skills",
    )


def test_profile_is_exact_known_answer() -> None:
    payload = observation.canonical_bytes(observation.OBSERVATION_PROFILE)
    assert len(payload) == 1975
    assert hashlib.sha256(payload).hexdigest() == observation.OBSERVATION_PROFILE_SHA256
    assert observation.OBSERVATION_PROFILE["schema_version"].endswith(".v3")
    assert "direct_interpreter_binding_sha256" not in observation.OBSERVATION_PROFILE
    assert "launcher_mode" not in observation.OBSERVATION_PROFILE
    assert observation.OBSERVATION_PROFILE["fixed_command"] == [
        "python.exe",
        "-B",
        "tools/check_role_pool_r0_offline_observation.py",
        "<observation_id>",
    ]
    assert observation.OBSERVATION_PROFILE["descendant_process_limit"] == 0
    assert observation.OBSERVATION_PROFILE["surviving_process_limit"] == 0
    assert observation.OBSERVATION_PROFILE["top_level_identity_role"] == (
        "diagnostic_nonblocking"
    )
    assert observation.OBSERVATION_PROFILE["observation_count"] == 1
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
    assert observation.SEQUENCE_ID == (
        "r0.app_native.offline.sequence.1.00000000000000000000000000000000"
    )
    assert observation.OBSERVATION_IDS == (
        "r0.app_native.offline.observation.1.00000000000000000000000000000000",
    )
    assert set(observation.OBSERVATION_IDS).isdisjoint(
        observation.HISTORICAL_OBSERVATION_IDS
    )
    assert observation.SEQUENCE_ID not in observation.HISTORICAL_SEQUENCE_IDS
    assert observation.observation_identity_pair(LIVE_OBSERVATION_ID) == (
        "r0.app_native.offline.sequence.1." + LIVE_IDENTITY_TOKEN,
        LIVE_OBSERVATION_ID,
    )
    with pytest.raises(observation.ObservationFailure):
        observation.observation_identity_pair(observation.OBSERVATION_IDS[0])
    assert observation.observation_identity_pair(
        observation.OBSERVATION_IDS[0],
        allow_synthetic=True,
    ) == (observation.SEQUENCE_ID, observation.OBSERVATION_IDS[0])
    for invalid in (
        "r0.app_native.offline.observation.2." + LIVE_IDENTITY_TOKEN,
        "r0.app_native.offline.observation.1." + ("A" * 32),
        "r0.app_native.offline.observation.1.short",
    ):
        with pytest.raises(observation.ObservationFailure):
            observation.observation_identity_pair(invalid)


def test_app_native_synthetic_matrix_uses_only_fake_clients() -> None:
    checker, _pool = _real_checker_and_pool()
    owners = checker._load_owner_modules(REPO_ROOT)
    observation._validate_app_native_synthetic_matrix(
        owners.pool,
        owners.direct_adapter,
    )


@pytest.mark.parametrize(
    ("position", "variant"),
    itertools.product((1,), range(3)),
)
def test_receipt_known_answers_are_byte_exact(position: int, variant: int) -> None:
    receipt = observation.EXPECTED_RECEIPTS[position - 1][variant]
    payload = observation.canonical_bytes(receipt)
    preimage = observation.canonical_bytes(
        {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    )
    assert tuple(receipt) == observation.RECEIPT_FIELDS
    assert len(preimage) == observation.EXPECTED_RECEIPT_PREIMAGE_LENGTHS[position - 1][variant]
    assert len(payload) == observation.EXPECTED_RECEIPT_LENGTHS[position - 1][variant]
    assert receipt["receipt_sha256"] == observation.EXPECTED_RECEIPT_SHA256S[position - 1][variant]
    assert hashlib.sha256(payload).hexdigest() == observation.EXPECTED_RECEIPT_ARTIFACT_SHA256S[position - 1][variant]
    assert observation.parse_receipt(payload) == receipt
    assert all(value is False for value in receipt["authority_flags"].values())


@pytest.mark.parametrize(
    ("position", "variant", "descendant_count", "identity_exact"),
    (
        (position, variant, descendant_count, identity_exact)
        for position in (1,)
        for variant, (descendant_count, identity_exact) in enumerate(
            observation.RECEIPT_VARIANTS
        )
    ),
)
def test_pure_post_exit_sealer_reproduces_all_three_receipt_variants(
    position: int,
    variant: int,
    descendant_count: int,
    identity_exact: bool | None,
) -> None:
    result = observation.seal_proportionate_observation_receipt(
        _validation_payload(),
        _post_exit_facts(
            descendant_process_count=descendant_count,
            top_level_identity_exact=identity_exact,
        ),
        position,
    )
    assert result == _receipt_bytes(position, variant)
    assert isinstance(result, bytes)
    receipt = observation.parse_receipt(result)
    assert receipt["top_level_identity_exact"] is identity_exact
    assert all(value is False for value in receipt["authority_flags"].values())


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({"top_level_process_count": 0}, "observation_launch_unknown"),
        ({"descendant_process_count": -1}, "observation_launch_unknown"),
        ({"process_relationships_known": False}, "observation_launch_unknown"),
        ({"process_terminal_states_known": False}, "observation_timeout_unknown"),
        ({"timed_out": True}, "observation_timeout_unknown"),
        ({"termination_uncertain": True}, "observation_timeout_unknown"),
        ({"cleanup_confirmed": False}, "observation_timeout_unknown"),
        ({"descendant_process_count": 1}, "observation_safety_boundary_failed"),
        ({"surviving_process_count": 1}, "observation_safety_boundary_failed"),
        ({"executor_network_operation_count": 1}, "observation_safety_boundary_failed"),
        ({"repository_write_count": 1}, "observation_safety_boundary_failed"),
        ({"installed_write_count": 1}, "observation_safety_boundary_failed"),
        ({"external_effect_count": 1}, "observation_safety_boundary_failed"),
        ({"generated_residue_count": 1}, "observation_safety_boundary_failed"),
        ({"output_complete": False}, "observation_result_unknown"),
    ],
)
def test_post_exit_sealer_fails_at_the_first_parent_owned_boundary(
    changes: dict[str, object],
    expected: str,
) -> None:
    result = observation.seal_proportionate_observation_receipt(
        _validation_payload(),
        _post_exit_facts(**changes),
        1,
    )
    assert result == expected


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        (
            {
                "top_level_process_count": 0,
                "timed_out": True,
                "surviving_process_count": 1,
                "output_complete": False,
            },
            "observation_launch_unknown",
        ),
        (
            {
                "timed_out": True,
                "surviving_process_count": 1,
                "output_complete": False,
            },
            "observation_timeout_unknown",
        ),
        (
            {"surviving_process_count": 1, "output_complete": False},
            "observation_safety_boundary_failed",
        ),
        ({"top_level_identity_exact": 1}, "observation_launch_unknown"),
    ],
)
def test_post_exit_failure_precedence_is_deterministic(
    changes: dict[str, object],
    expected: str,
) -> None:
    assert observation.seal_proportionate_observation_receipt(
        _validation_payload(),
        _post_exit_facts(**changes),
        1,
    ) == expected


def test_stale_validation_binding_precedes_unsafe_parent_facts() -> None:
    packet = _bootstrap_packet()
    packet["validator_bundle_sha256"] = "0" * 64
    packet["evidence_sha256"] = observation.self_digest(packet, "evidence_sha256")
    assert observation.seal_proportionate_observation_receipt(
        observation.canonical_bytes(packet),
        _post_exit_facts(surviving_process_count=1),
        1,
    ) == "observation_binding_rejected"


def test_validation_payload_is_canonical_nonpublishable_and_parent_facts_are_closed() -> None:
    payload = _validation_payload()
    packet = observation.parse_validation_payload(payload)
    assert packet["schema_version"] == "trusted_owner_r0_offline_bootstrap_evidence.v1"
    assert "receipt_sha256" not in packet
    assert "descendant_process_count" not in packet

    duplicate = payload.replace(
        b'{"schema_version":',
        b'{"schema_version":"duplicate","schema_version":',
        1,
    )
    reordered_packet = {key: packet[key] for key in reversed(packet)}
    stale_packet = copy.deepcopy(packet)
    stale_packet["registry_sha256"] = "0" * 64
    stale_packet["evidence_sha256"] = observation.self_digest(
        stale_packet,
        "evidence_sha256",
    )
    for candidate, expected in (
        (duplicate, "observation_validation_failed"),
        (observation.canonical_bytes(reordered_packet), "observation_validation_failed"),
        (observation.canonical_bytes(stale_packet), "observation_binding_rejected"),
    ):
        assert observation.seal_proportionate_observation_receipt(
            candidate,
            _post_exit_facts(),
            1,
        ) == expected

    assert observation.seal_proportionate_observation_receipt(
        payload,
        _post_exit_facts().__dict__,  # type: ignore[arg-type]
        1,
    ) == "observation_launch_unknown"
    assert observation.seal_proportionate_observation_receipt(
        payload,
        _post_exit_facts(),
        3,
    ) == "observation_sequence_rejected"


def test_receipt_parser_rejects_duplicate_unknown_reordered_mistyped_and_mutated() -> None:
    original = observation.EXPECTED_RECEIPTS[0][0]
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


def test_observation_two_and_receipt_pairs_remain_unreachable() -> None:
    first = _receipt_bytes(1)
    for candidate in ((first,), (first, first), ()):
        with pytest.raises(observation.ObservationFailure) as error:
            observation.validate_receipt_pair(candidate)
        assert error.value.status == "observation_sequence_rejected"

    for identity in (
        "r0.app_native.offline.observation.2." + LIVE_IDENTITY_TOKEN,
        observation.HISTORICAL_OBSERVATION_IDS[0],
    ):
        with pytest.raises(observation.ObservationFailure) as error:
            observation.observation_identity_pair(identity)
        assert error.value.status == "observation_sequence_rejected"


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
    assert len(preimage) == 2687
    assert len(payload) == 2775
    assert packet["consumption_sha256"] == (
        "1a97a02bf48457a8af1398052ef3d467cec1c8d425ee8da347799d86051e779a"
    )
    assert hashlib.sha256(payload).hexdigest() == (
        "c9d8a85b9ec79d44aeabfa9471bd6377133a1761b1d560941040cc5fa3c22265"
    )
    assert packet["sequence_contract_review_ref"].startswith(
        "https://github.com/Tahjali11/Mythic-Edge/issues/826#"
    )
    assert packet["expected_receipt_sha256s"] == list(
        observation.EXPECTED_RECEIPT_SHA256S[0]
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


@pytest.mark.parametrize("position", [1])
def test_consumption_rejects_every_receipt_allowlist_permutation(position: int) -> None:
    packet = _consumption(position)
    allowed = list(packet["expected_receipt_sha256s"])
    assert len(allowed) == 3
    candidates = (
        list(reversed(allowed)),
        allowed[1:] + allowed[:1],
        allowed[:-1],
        allowed + [allowed[-1]],
        [*allowed[:-1], "0" * 64],
    )
    for candidate in candidates:
        changed = copy.deepcopy(packet)
        changed["expected_receipt_sha256s"] = candidate
        changed["consumption_sha256"] = observation.self_digest(
            changed,
            "consumption_sha256",
        )
        with pytest.raises(observation.ObservationFailure):
            observation.parse_consumption(observation.canonical_bytes(changed))


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


def test_sequence_preflight_binds_single_use_and_rejects_predecessors() -> None:
    first = _consumption(1)
    observation.validate_sequence_preflight(
        observation.OBSERVATION_IDS[0],
        consumption=first,
    )
    with pytest.raises(observation.ObservationFailure):
        observation.validate_sequence_preflight(
            observation.OBSERVATION_IDS[0],
            consumption=first,
            predecessor_consumption_sha256="7" * 64,
            predecessor_receipt=_receipt_bytes(1),
        )
    with pytest.raises(observation.ObservationFailure):
        observation.validate_sequence_preflight(
            LIVE_OBSERVATION_ID,
            consumption=first,
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
    observation.require_publication_issue(826)
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


def test_exact_in_process_owner_call_graph_projects_only_validation_payload() -> None:
    checker = _FakeChecker()
    roots = _fake_roots()
    audit = observation.AuditBoundary(REPO_ROOT, (Path(sys.base_prefix),))
    audit.bind_installed_root(roots.installed_skills_root)
    with _historical_owner_hashes(checker):
        payload = observation.evaluate_observation(
            observation.OBSERVATION_IDS[0],
            checker=checker,
            roots=roots,
            audit_boundary=audit,
            runtime_os_name="nt",
            runtime_sys_platform="win32",
            allow_synthetic_identity=True,
        )
    assert payload == _validation_payload()
    assert observation.parse_validation_payload(payload) == _bootstrap_packet()
    sealed = observation.seal_proportionate_observation_receipt(
        payload,
        _post_exit_facts(),
        1,
    )
    assert sealed == _receipt_bytes(1)
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
            allow_synthetic_identity=True,
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
            allow_synthetic_identity=True,
        )
    assert error.value.status == "observation_binding_rejected"


def test_current_release_uses_existing_owner_validation_and_exact_r0_ceiling() -> None:
    checker, pool = _real_checker_and_pool()
    immutable = _immutable_r0_record(pool)
    _payload, records, bindings = _validated_current_release(checker, pool)
    assert records[0] == immutable
    assert bindings["to_rung"] == "R0"
    assert records[-1]["observation_receipt_sha256s"] == []
    assert pool.validate_trusted_native_release_ceiling(
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
        ({"termination_uncertain": True}, "observation_timeout_unknown"),
        ({"cleanup_confirmed": False}, "observation_timeout_unknown"),
        ({"process_terminal_states_known": False}, "observation_timeout_unknown"),
        ({"exit_code": None}, "observation_launch_unknown"),
        ({"top_level_process_count": 0}, "observation_launch_unknown"),
        ({"process_relationships_known": False}, "observation_launch_unknown"),
        ({"descendant_process_count": 1}, "observation_safety_boundary_failed"),
        ({"descendant_process_count": 2}, "observation_safety_boundary_failed"),
        ({"surviving_process_count": 1}, "observation_safety_boundary_failed"),
        ({"top_level_identity_exact": False}, "accepted_exact_r0_offline_observation"),
        ({"top_level_identity_exact": True}, "accepted_exact_r0_offline_observation"),
        ({"repository_write_count": 1}, "observation_safety_boundary_failed"),
        ({"installed_write_count": 1}, "observation_safety_boundary_failed"),
        ({"external_effect_count": 1}, "observation_safety_boundary_failed"),
        ({"executor_network_operation_count": 1}, "observation_safety_boundary_failed"),
        ({"generated_residue_count": 1}, "observation_safety_boundary_failed"),
        ({"output_complete": False}, "observation_result_unknown"),
        ({"stdout": b"x" * 4097}, "observation_result_unknown"),
        ({"stdout": b"invalid\n"}, "observation_validation_failed"),
        ({"stderr": b"symbolic-failure\n"}, "observation_validation_failed"),
        ({"exit_code": 1}, "observation_validation_failed"),
    ],
)
def test_fake_launcher_enforces_process_timeout_output_and_cleanup_boundaries(
    changes: dict[str, object],
    expected: str,
) -> None:
    result = _launcher_observation(**changes)
    assert observation.classify_launcher_observation(result) == expected


@pytest.mark.parametrize(
    ("direct_changes", "process_changes", "expected"),
    [
        ({}, {}, "accepted_exact_r0_offline_observation"),
        ({"public_binding_exact": False}, {}, "observation_binding_rejected"),
        ({"private_binding_exact": False}, {}, "accepted_exact_r0_offline_observation"),
        ({"top_level_identity_exact": False}, {}, "accepted_exact_r0_offline_observation"),
        ({"parentage_known": False}, {}, "accepted_exact_r0_offline_observation"),
        ({}, {"top_level_process_count": 0}, "observation_launch_unknown"),
        (
            {},
            {"descendant_process_count": 1},
            "observation_safety_boundary_failed",
        ),
        ({}, {"descendant_process_count": 2}, "observation_safety_boundary_failed"),
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
    direct_values: dict[str, object] = {
        "public_binding_exact": True,
        "private_binding_exact": True,
        "top_level_identity_exact": True,
        "parentage_known": True,
        "process": _launcher_observation(**process_changes),
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


@pytest.mark.parametrize("historical_id", observation.HISTORICAL_OBSERVATION_IDS)
def test_every_historical_observation_identity_is_terminal_nonreusable(
    historical_id: str,
) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with (
        mock.patch.object(observation, "_load_checker", side_effect=AssertionError),
        mock.patch.object(observation.sys, "stdout", stdout),
        mock.patch.object(observation.sys, "stderr", stderr),
    ):
        exit_code = observation.run([historical_id])
    assert exit_code == 2
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_sequence_rejected\n"


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
    assert observation.run([LIVE_OBSERVATION_ID]) == 2
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_binding_rejected\n"


def test_cli_success_path_uses_fake_owner_and_emits_only_validation_payload(
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
    monkeypatch.setattr(observation, "_load_checker", lambda root: checker)
    monkeypatch.setattr(observation.sys, "stdout", stdout)
    monkeypatch.setattr(observation.sys, "stderr", stderr)
    with _historical_owner_hashes(checker):
        assert observation.run([LIVE_OBSERVATION_ID]) == 0
    assert stdout.getvalue().encode("utf-8") == _validation_payload()
    assert stderr.getvalue() == ""


def test_cli_does_not_use_retired_direct_interpreter_dependency(
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
        mock.Mock(side_effect=AssertionError("retired dependency must not run")),
    )
    owner = mock.Mock(return_value=checker)
    monkeypatch.setattr(observation, "_load_checker", owner)
    monkeypatch.setattr(observation.sys, "stdout", stdout)
    monkeypatch.setattr(observation.sys, "stderr", stderr)
    with _historical_owner_hashes(checker):
        assert observation.run([LIVE_OBSERVATION_ID]) == 0
    assert owner.call_count == 1
    assert stdout.getvalue().encode("utf-8") == _validation_payload()
    assert stderr.getvalue() == ""


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
    monkeypatch.setattr(observation, "_load_checker", lambda root: checker)
    monkeypatch.setattr(observation.sys, "stdout", stdout)
    monkeypatch.setattr(observation.sys, "stderr", stderr)
    assert observation.run([LIVE_OBSERVATION_ID]) == 3
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_result_unknown\n"
    assert "private" not in stderr.getvalue().lower()


def test_frozen_owner_bindings_and_current_successor_rejection_remain_exact() -> None:
    release_before = (
        REPO_ROOT / "docs/role_pool/trusted_owner_native_release_state.v1.jsonl"
    ).read_bytes()
    index_path = REPO_ROOT / "docs/role_pool_current_authority_index.md"
    index_before = index_path.read_bytes()
    checker, pool = _real_checker_and_pool()
    _validated_current_release(checker, pool)
    _assert_authority_index_semantics(index_before)
    with pytest.raises(AssertionError):
        _assert_authority_index_semantics(
            b"active_r0_offline_only_release_state\n"
        )
    assert observation.RELEASE_STATE_ARTIFACT_SHA256 == (
        "fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2"
    )
    assert hashlib.sha256(release_before).hexdigest() == (
        observation.RELEASE_STATE_ARTIFACT_SHA256
    )

    unchanged_bindings = {
        observation.SEQUENCE_CONTRACT_RELATIVE_PATH.as_posix(): observation.SEQUENCE_CONTRACT_SHA256,
        observation.RECEIPT_ORDER_CONTRACT_RELATIVE_PATH.as_posix(): observation.RECEIPT_ORDER_CONTRACT_SHA256,
        observation.RECEIPT_ORDER_REVIEW_RELATIVE_PATH.as_posix(): observation.RECEIPT_ORDER_REVIEW_SHA256,
        observation.PROPORTIONATE_CONTRACT_RELATIVE_PATH.as_posix(): observation.PROPORTIONATE_CONTRACT_SHA256,
        observation.PROPORTIONATE_REVIEW_RELATIVE_PATH.as_posix(): observation.PROPORTIONATE_REVIEW_SHA256,
        "docs/role_pool/trusted_owner_repository_registry.v1.json": observation.REGISTRY_ARTIFACT_SHA256,
    }
    assert all(
        hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest() == expected
        for path, expected in unchanged_bindings.items()
    )
    current_bindings = {
        "docs/contracts/trusted_owner_native_role_pool_profile.md": (
            observation.PROFILE_CONTRACT_SHA256,
            "8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952",
        ),
        "tools/check_role_pool_r0_bootstrap.py": (
            observation.R0_CHECKER_SHA256,
            "897790936dc0c49401177958477f839d0cecac39bd0cf2e24849fc05954e781a",
        ),
        "docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py": (
            observation.RELEASE_VALIDATOR_SHA256,
            "5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361",
        ),
    }
    for path, (frozen_constant, successor) in current_bindings.items():
        assert frozen_constant == successor
        current = hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
        assert current == successor

    assert observation.R0_CHECKER_TEST_SHA256 == (
        "55a40f12d7d161eb40fca2905f442b3b6ecd1fc029e3313c81566db89dd6ae3f"
    )
    assert hashlib.sha256(
        (REPO_ROOT / "tests/test_check_role_pool_r0_bootstrap.py").read_bytes()
    ).hexdigest() == observation.R0_CHECKER_TEST_SHA256

    assert observation._load_checker(REPO_ROOT) is not None
    assert observation.OBSERVATION_PROFILE["implementation_paths"] == [
        "tools/check_role_pool_r0_offline_observation.py",
        "tests/test_check_role_pool_r0_offline_observation.py",
        "tests/test_run_role_pool_r0_trusted_launch_observer.py",
    ]
    assert "DIRECT_INTERPRETER_CONTRACT_RELATIVE_PATH" not in (
        observation._load_checker.__code__.co_names
    )
    assert "validate_running_direct_interpreter" not in observation.run.__code__.co_names
    assert (
        REPO_ROOT / "docs/role_pool/trusted_owner_native_release_state.v1.jsonl"
    ).read_bytes() == release_before
    assert index_path.read_bytes() == index_before


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
    observation.parse_validation_payload(_validation_payload())
    assert isinstance(
        observation.seal_proportionate_observation_receipt(
            _validation_payload(),
            _post_exit_facts(),
            1,
        ),
        bytes,
    )
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
        for receipts in observation.EXPECTED_RECEIPTS
        for receipt in receipts
        for value in receipt["authority_flags"].values()
    )
