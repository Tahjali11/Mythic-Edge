from __future__ import annotations

import copy
import hashlib
import importlib.util
import io
import itertools
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "tools/check_role_pool_r0_bootstrap.py"
SPEC = importlib.util.spec_from_file_location(
    "check_role_pool_r0_bootstrap",
    MODULE_PATH,
)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)

WORKFLOW_FIXTURE_ROOT = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "role_pool_r0_workflow"
)
WORKFLOW_ROOT_PLACEHOLDER = b"{{MYTHIC_EDGE_WORKSPACE_ROOT}}"
WORKFLOW_ROOT_BYTES = "\\".join(
    ("C:", "Users", "Tahj " + "Blow", "Desktop", "MTG Resources")
).encode("ascii")
WORKFLOW_BINDINGS = {
    Path("SKILL.md"): (
        "04c229e2604ec965391d0044947d5a985049fc69508b79c88aec09e3732f14bb"
    ),
    Path("agents/openai.yaml"): (
        "0dc1f6b8acfac33f9f7a2628e093bc7fddbc2cb52a8bb41f9c22e56a57aa0c2f"
    ),
    Path("scripts/accept_fallback_prompt.py"): (
        "47aa25f3da14bfade71ed2862e4b7d85248c8356b1c90bdfd61222133b0a875d"
    ),
}


@dataclass(frozen=True)
class SyntheticFixture:
    root: Path
    repository_root: Path
    installed_skills_root: Path
    roots: object
    owners: object


def _copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _signed(pool: object, document: dict[str, object], field: str) -> dict[str, object]:
    result = copy.deepcopy(document)
    result[field] = pool.trusted_native_self_digest(result, field)
    return result


def _valid_registry(pool: object) -> dict[str, object]:
    entry = _signed(
        pool,
        {
            "schema_version": "trusted_owner_repository_entry.v1",
            "repository_id": checker.REPOSITORY_ID,
            "canonical_name": checker.REPOSITORY_NAME,
            "status": "active",
            "trust_basis_refs": [checker.ISSUE_URL],
            "eligible_roles": ["A"],
            "permitted_operations": ["offline_validation"],
            "permitted_read_scope": ["docs"],
            "maximum_mutation_scope": [],
            "repository_code_execution_policy": "forbidden",
            "approved_commands": [],
            "protected_surface_restrictions": ["parser_truth"],
            "external_effect_restrictions": [
                "credentials",
                "network",
                "service",
            ],
            "approving_authority_ref": checker.ISSUE_URL,
            "approved_at_utc": "2026-07-30T00:00:00Z",
            "review_triggers": [
                "authority_widening",
                "identity_drift",
                "protected_surface_change",
                "transfer",
            ],
            "review_due_at_utc": None,
            "entry_sha256": "",
        },
        "entry_sha256",
    )
    return _signed(
        pool,
        {
            "schema_version": "trusted_owner_repository_registry.v1",
            "profile_id": "trusted_owner_native",
            "coordination_repository_id": checker.REPOSITORY_ID,
            "coordination_repository_name": checker.REPOSITORY_NAME,
            "coordination_issue_number": 761,
            "authorized_claim_actor_ids": [1],
            "release_state_path": (
                "docs/role_pool/trusted_owner_native_release_state.v1.jsonl"
            ),
            "entries": [entry],
            "registry_sha256": "",
        },
        "registry_sha256",
    )


def _release_record(
    pool: object,
    rung: str = "R0",
    *,
    predecessor: dict[str, object] | None = None,
    registry_sha256: str = "c" * 64,
) -> dict[str, object]:
    bootstrap = predecessor is None
    rung_index = int(rung.removeprefix("R"))
    receipts = (
        []
        if bootstrap
        else [
            f"{2 * rung_index:064x}",
            f"{2 * rung_index + 1:064x}",
        ]
    )
    return _signed(
        pool,
        {
            "schema_version": "trusted_owner_native_release_record.v1",
            "record_id": f"release.{rung.lower()}",
            "predecessor_record_sha256": (
                None if bootstrap else predecessor["record_sha256"]
            ),
            "from_rung": None if bootstrap else predecessor["to_rung"],
            "to_rung": rung,
            "contract_sha256": "a" * 64,
            "skill_tree_sha256": "b" * 64,
            "registry_sha256": registry_sha256,
            "validator_bundle_sha256": "d" * 64,
            "observation_receipt_sha256s": receipts,
            "codex_e_review_ref": "review:codex-e",
            "codex_e_review_sha256": "e" * 64,
            "owner_decision_ref": "owner:decision",
            "accepted_at_utc": f"2026-07-30T00:00:{rung_index:02d}Z",
            "record_sha256": "",
        },
        "record_sha256",
    )


def _release_rebaseline(
    pool: object,
    predecessor: dict[str, object],
    *,
    contract_sha256: str = "9" * 64,
) -> dict[str, object]:
    return _signed(
        pool,
        {
            "schema_version": (
                "trusted_owner_native_release_rebaseline_record.v1"
            ),
            "record_id": "r0.rebaseline.synthetic",
            "predecessor_record_sha256": predecessor["record_sha256"],
            "from_rung": "R0",
            "to_rung": "R0",
            "predecessor_contract_sha256": predecessor["contract_sha256"],
            "contract_sha256": contract_sha256,
            "predecessor_skill_tree_sha256": predecessor["skill_tree_sha256"],
            "skill_tree_sha256": predecessor["skill_tree_sha256"],
            "predecessor_registry_sha256": predecessor["registry_sha256"],
            "registry_sha256": predecessor["registry_sha256"],
            "predecessor_validator_bundle_sha256": predecessor[
                "validator_bundle_sha256"
            ],
            "validator_bundle_sha256": predecessor[
                "validator_bundle_sha256"
            ],
            "observation_receipt_sha256s": [],
            "codex_e_review_ref": "review:codex-e-rebaseline",
            "codex_e_review_sha256": "1" * 64,
            "owner_decision_ref": "owner:rebaseline-decision",
            "accepted_at_utc": "2026-07-30T00:00:01Z",
            "record_sha256": "",
        },
        "record_sha256",
    )


def _write_registry(fixture: SyntheticFixture, registry: dict[str, object]) -> None:
    path = fixture.repository_root / checker.REGISTRY_RELATIVE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(fixture.owners.pool.trusted_native_canonical_bytes(registry))


def _copy_workflow(target_root: Path) -> None:
    for relative_path, expected_sha256 in WORKFLOW_BINDINGS.items():
        fixture_relative_path = {
            Path("SKILL.md"): Path("SKILL.md.template"),
            Path("scripts/accept_fallback_prompt.py"): Path(
                "scripts/accept_fallback_prompt.py.fixture"
            ),
        }.get(relative_path, relative_path)
        source = WORKFLOW_FIXTURE_ROOT / fixture_relative_path
        payload = source.read_bytes()
        if relative_path == Path("SKILL.md"):
            assert payload.count(WORKFLOW_ROOT_PLACEHOLDER) == 2
            payload = payload.replace(
                WORKFLOW_ROOT_PLACEHOLDER,
                WORKFLOW_ROOT_BYTES,
            )
        assert hashlib.sha256(payload).hexdigest() == expected_sha256
        target = target_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)


@contextmanager
def _exact_fixture(
    *,
    with_registry: bool = True,
    bind_current_source_tree: bool = True,
    bind_current_manifest: bool = True,
) -> SyntheticFixture:
    temporary = tempfile.TemporaryDirectory(prefix="mythic-edge-r0-bootstrap-")
    root = Path(temporary.name)
    repository_root = root / "repository"
    installed_skills_root = root / "user-home" / ".codex" / "skills"
    previous_source_binding = (
        checker.SOURCE_TREE_NODE_COUNT,
        checker.SOURCE_TREE_FILE_COUNT,
        checker.SOURCE_TREE_MANIFEST_BYTE_COUNT,
        checker.SOURCE_TREE_SHA256,
    )
    previous_manifest_binding = (
        checker.STAGE3_MANIFEST_FILE_COUNT,
        checker.STAGE3_MANIFEST_BYTE_COUNT,
        checker.STAGE3_MANIFEST_SHA256,
    )
    try:
        for _, relative_path, _ in checker.FILE_BINDINGS:
            source = REPO_ROOT / relative_path
            target = repository_root / relative_path
            if checker.SOURCE_SKILL_RELATIVE_PATH in (
                relative_path,
                *relative_path.parents,
            ):
                continue
            _copy_file(source, target)
        _copy_file(MODULE_PATH, repository_root / checker.CHECKER_RELATIVE_PATH)
        _copy_file(
            Path(__file__),
            repository_root / checker.CHECKER_TEST_RELATIVE_PATH,
        )
        source_skill = REPO_ROOT / checker.SOURCE_SKILL_RELATIVE_PATH
        copied_source_skill = (
            repository_root / checker.SOURCE_SKILL_RELATIVE_PATH
        )
        shutil.copytree(source_skill, copied_source_skill)
        shutil.copytree(
            source_skill,
            installed_skills_root / "mythic-edge-role-pool",
        )
        _copy_workflow(installed_skills_root / "mythic-edge-workflow")
        roots = checker.EvaluationRoots(repository_root, installed_skills_root)
        owners = checker._load_owner_modules(repository_root)
        if bind_current_manifest:
            workflow_root = installed_skills_root / "mythic-edge-workflow"
            owners.stage3.WORKFLOW_ROOT = workflow_root
            owners.stage3.WORKFLOW_SNAPSHOT_FILES = tuple(
                workflow_root / relative_path
                for relative_path in checker.WORKFLOW_SNAPSHOT_RELATIVE_PATHS
            )
            rows = owners.stage3.current_skill_manifest()
            current = {row["path"]: row["sha256"] for row in rows}
            baseline = owners.stage3.STAGE2_BASELINE_FILES
            owners.stage3.EXPECTED_CURRENT_MANIFEST_FILE_COUNT = len(rows)
            owners.stage3.ALLOWED_ADDED_PATHS = set(current) - set(baseline)
            owners.stage3.ALLOWED_MODIFIED_PATHS = {
                path
                for path in set(current) & set(baseline)
                if current[path] != baseline[path]
            }
            owners.stage3.REVIEWED_APP_SERVER_MODIFIED_DIGESTS = {
                path: current[path]
                for path in owners.stage3.REVIEWED_APP_SERVER_MODIFIED_DIGESTS
            }
            encoded_manifest = owners.stage3.canonical_bytes(rows)
            checker.STAGE3_MANIFEST_FILE_COUNT = len(rows)
            checker.STAGE3_MANIFEST_BYTE_COUNT = len(encoded_manifest)
            checker.STAGE3_MANIFEST_SHA256 = hashlib.sha256(
                encoded_manifest
            ).hexdigest()
        if bind_current_source_tree:
            snapshot = owners.installer._tree_snapshot(copied_source_skill)
            assert snapshot is not None
            (
                checker.SOURCE_TREE_NODE_COUNT,
                checker.SOURCE_TREE_FILE_COUNT,
                checker.SOURCE_TREE_MANIFEST_BYTE_COUNT,
                checker.SOURCE_TREE_SHA256,
            ) = checker._tree_manifest(snapshot, owners.pool)
        fixture = SyntheticFixture(
            root=root,
            repository_root=repository_root,
            installed_skills_root=installed_skills_root,
            roots=roots,
            owners=owners,
        )
        if with_registry:
            _write_registry(fixture, _valid_registry(owners.pool))
        if bind_current_manifest:
            with mock.patch.object(
                checker,
                "_load_owner_modules",
                return_value=owners,
            ):
                yield fixture
        else:
            yield fixture
    finally:
        (
            checker.SOURCE_TREE_NODE_COUNT,
            checker.SOURCE_TREE_FILE_COUNT,
            checker.SOURCE_TREE_MANIFEST_BYTE_COUNT,
            checker.SOURCE_TREE_SHA256,
        ) = previous_source_binding
        (
            checker.STAGE3_MANIFEST_FILE_COUNT,
            checker.STAGE3_MANIFEST_BYTE_COUNT,
            checker.STAGE3_MANIFEST_SHA256,
        ) = previous_manifest_binding
        temporary.cleanup()
        assert not root.exists()


def _run_raw_cli(
    fixture: SyntheticFixture,
    *arguments: str,
) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment.pop("CODEX_HOME", None)
    user_home = fixture.installed_skills_root.parents[1]
    environment["HOME"] = str(user_home)
    environment["USERPROFILE"] = str(user_home)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(
                fixture.repository_root
                / checker.CHECKER_RELATIVE_PATH
            ),
            *arguments,
        ],
        cwd=fixture.repository_root,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=60,
    )


def _exact_observations() -> object:
    source = checker.TreeObservation(
        checker.SOURCE_TREE_NODE_COUNT,
        checker.SOURCE_TREE_FILE_COUNT,
        checker.SOURCE_TREE_MANIFEST_BYTE_COUNT,
        checker.SOURCE_TREE_SHA256,
        "observed",
    )
    return checker.ComponentObservations(
        contract_binding_status="exact",
        manifest=checker.ManifestObservation(
            checker.STAGE3_MANIFEST_FILE_COUNT,
            checker.STAGE3_MANIFEST_BYTE_COUNT,
            checker.STAGE3_MANIFEST_SHA256,
            "exact",
        ),
        source_tree=source,
        installed_tree=source,
        source_install_status="identical",
        registry_status="valid_exact",
        registry_sha256="a" * 64,
        release_state_status="absent_bootstrap_candidate",
        release_state_sha256=None,
        checker_sha256="b" * 64,
        checker_test_sha256="c" * 64,
        validator_bundle_sha256="d" * 64,
        validator_bundle_status="exact",
        offline_validation_status="passed",
    )


def _replace_observations(observations: object, **changes: object) -> object:
    values = dict(observations.__dict__)
    values.update(changes)
    return checker.ComponentObservations(**values)


def test_exact_synthetic_roots_are_eligible_and_owner_backed() -> None:
    with _exact_fixture() as fixture:
        packet, encoded = checker._evaluate_for_tests(fixture.roots)
        assert packet["terminal_status"] == "eligible_for_independent_review"
        assert packet["eligible_for_independent_review"] is True
        assert packet["manifest_status"] == "exact"
        assert packet["source_install_status"] == "identical"
        assert packet["registry_status"] == "valid_exact"
        assert packet["release_state_status"] == "absent_bootstrap_candidate"
        assert packet["offline_validation_status"] == "passed"
        assert encoded == fixture.owners.pool.trusted_native_canonical_bytes(packet)
        assert fixture.owners.pool.validate_trusted_native_registry(
            fixture.owners.pool.parse_trusted_native_json(
                (
                    fixture.repository_root
                    / checker.REGISTRY_RELATIVE_PATH
                ).read_text(encoding="utf-8")
            )
        ) == []


def test_successor_contract_and_profile_bindings_are_exact() -> None:
    binding_by_name = {
        name: (relative_path, digest)
        for name, relative_path, digest in checker.FILE_BINDINGS
    }

    assert checker.PROFILE_CONTRACT_SHA256 == (
        "8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952"
    )
    assert checker.APP_NATIVE_CONTRACT_SHA256 == (
        "00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4"
    )
    assert checker.R0_CONTRACT_SHA256 == (
        "07ab1c7153ba1312533bdc27d984789127fb7fc02190d26853ffae1849c2ac82"
    )
    assert binding_by_name["profile_contract"] == (
        Path("docs/contracts/trusted_owner_native_role_pool_profile.md"),
        checker.PROFILE_CONTRACT_SHA256,
    )
    assert binding_by_name["app_native_contract"] == (
        Path(
            "docs/contracts/role_pool_codex_app_native_direct_task_adapter.md"
        ),
        checker.APP_NATIVE_CONTRACT_SHA256,
    )
    assert binding_by_name["direct_fake_transport"] == (
        checker.SOURCE_SKILL_RELATIVE_PATH
        / "scripts/trusted_native_app_direct_task_adapter.py",
        (
            "fae7aa4aec168d02de0dbdd34ab6a181b9f545b85aba39110e8d741e8094dd98"
        ),
    )
    assert binding_by_name["r0_contract"] == (
        Path(
            "docs/contracts/"
            "role_pool_trusted_owner_r0_post_sync_evidence_binding_successor.md"
        ),
        checker.R0_CONTRACT_SHA256,
    )
    assert binding_by_name["installer"] == (
        Path("tools/install_codex_skills.py"),
        checker.INSTALLER_SHA256,
    )


def test_current_successor_tree_waits_for_separate_manifest_transition() -> None:
    with _exact_fixture(
        bind_current_source_tree=False,
        bind_current_manifest=False,
    ) as fixture:
        packet, _ = checker._evaluate_for_tests(fixture.roots)

    assert packet["contract_binding_status"] == "exact"
    assert packet["validator_bundle_status"] == "exact"
    assert packet["manifest_status"] == "known_invalid"
    assert packet["source_install_status"] == "installed_drift"
    assert packet["registry_status"] == "valid_exact"
    assert packet["release_state_status"] == "absent_bootstrap_candidate"
    assert packet["offline_validation_status"] == "passed"
    assert packet["terminal_status"] == "blocked_manifest_invalid"
    assert packet["eligible_for_independent_review"] is False
    assert set(packet["effect_counts"].values()) == {0}
    assert set(packet["authority_flags"].values()) == {False}


def test_successor_pre_sync_projection_retains_source_drift_as_first_blocker() -> None:
    with _exact_fixture(with_registry=False) as fixture:
        installed = (
            fixture.installed_skills_root
            / "mythic-edge-role-pool"
            / "SKILL.md"
        )
        installed.write_text("synthetic predecessor drift\n", encoding="utf-8")

        packet, _ = checker._evaluate_for_tests(fixture.roots)

    assert packet["contract_binding_status"] == "exact"
    assert packet["validator_bundle_status"] == "exact"
    assert packet["manifest_status"] == "exact"
    assert packet["source_install_status"] == "installed_drift"
    assert packet["registry_status"] == "absent"
    assert packet["release_state_status"] == "absent_bootstrap_candidate"
    assert packet["offline_validation_status"] == "passed"
    assert packet["terminal_status"] == "blocked_skill_source_drift"
    assert packet["eligible_for_independent_review"] is False
    assert set(packet["effect_counts"].values()) == {0}
    assert set(packet["authority_flags"].values()) == {False}


def test_successor_post_sync_projection_advances_only_to_registry_blocker() -> None:
    with _exact_fixture(with_registry=False) as fixture:
        packet, _ = checker._evaluate_for_tests(fixture.roots)
        expected_tree = (
            checker.SOURCE_TREE_NODE_COUNT,
            checker.SOURCE_TREE_FILE_COUNT,
            checker.SOURCE_TREE_MANIFEST_BYTE_COUNT,
            checker.SOURCE_TREE_SHA256,
        )

    assert packet["contract_binding_status"] == "exact"
    assert packet["validator_bundle_status"] == "exact"
    assert packet["manifest_status"] == "exact"
    assert packet["source_install_status"] == "identical"
    assert (
        packet["installed_tree_node_count"],
        packet["installed_tree_file_count"],
        packet["installed_tree_manifest_byte_count"],
        packet["installed_tree_sha256"],
    ) == expected_tree
    assert packet["registry_status"] == "absent"
    assert packet["release_state_status"] == "absent_bootstrap_candidate"
    assert packet["terminal_status"] == "blocked_registry_missing_or_invalid"
    assert packet["eligible_for_independent_review"] is False
    assert set(packet["effect_counts"].values()) == {0}
    assert set(packet["authority_flags"].values()) == {False}


def test_exact_fixture_does_not_require_ambient_installed_workflow() -> None:
    with mock.patch.object(
        Path,
        "home",
        side_effect=AssertionError("ambient home must not be read"),
    ):
        with _exact_fixture() as fixture:
            packet, encoded = checker._evaluate_for_tests(fixture.roots)
    assert packet["terminal_status"] == "eligible_for_independent_review"
    assert WORKFLOW_ROOT_BYTES not in encoded


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        (
            "contract_binding_status",
            "known_invalid",
            "blocked_contract_binding_invalid",
        ),
        (
            "validator_bundle_status",
            "known_invalid",
            "blocked_validator_bundle_invalid",
        ),
        ("manifest", "known_invalid", "blocked_manifest_invalid"),
        ("source_install_status", "installed_drift", "blocked_skill_source_drift"),
        (
            "registry_status",
            "absent",
            "blocked_registry_missing_or_invalid",
        ),
        (
            "release_state_status",
            "present_valid_chain",
            "blocked_release_state_conflict",
        ),
        (
            "offline_validation_status",
            "failed",
            "blocked_offline_validation_failed",
        ),
        (
            "contract_binding_status",
            "unknown",
            "unknown_outcome_reconciliation_required",
        ),
        (
            "contract_binding_status",
            "exact",
            "eligible_for_independent_review",
        ),
    ],
)
def test_each_terminal_status_is_reachable(
    field: str,
    value: str,
    expected: str,
) -> None:
    observations = _exact_observations()
    if field == "manifest":
        observations = _replace_observations(
            observations,
            manifest=checker.ManifestObservation(
                38,
                1,
                "f" * 64,
                value,
            ),
        )
    else:
        observations = _replace_observations(observations, **{field: value})
    terminal = checker._select_terminal_status(
        observations.contract_binding_status,
        observations.validator_bundle_status,
        observations.manifest.status,
        observations.source_install_status,
        observations.registry_status,
        observations.release_state_status,
        observations.offline_validation_status,
    )
    assert terminal == expected


def test_selector_exhaustively_covers_6480_vectors_without_overlap() -> None:
    audit = checker._selector_audit()
    assert audit == {
        "tuple_count": 6480,
        "overlap_count": 0,
        "uncovered_count": 0,
        "unreachable_count": 0,
    }
    reached = {
        checker._select_terminal_status(*values)
        for values in itertools.product(
            checker.CONTRACT_BINDING_STATUSES,
            checker.VALIDATOR_BUNDLE_STATUSES,
            checker.MANIFEST_STATUSES,
            checker.SOURCE_INSTALL_STATUSES,
            checker.REGISTRY_STATUSES,
            checker.RELEASE_STATE_STATUSES,
            checker.OFFLINE_VALIDATION_STATUSES,
        )
    }
    assert reached == set(checker.TERMINAL_STATUSES)


@pytest.mark.parametrize(
    ("earlier_field", "earlier_value", "expected"),
    [
        (
            "contract_binding_status",
            "known_invalid",
            "blocked_contract_binding_invalid",
        ),
        (
            "validator_bundle_status",
            "known_invalid",
            "blocked_validator_bundle_invalid",
        ),
        ("manifest_status", "known_invalid", "blocked_manifest_invalid"),
        ("source_install_status", "installed_drift", "blocked_skill_source_drift"),
        (
            "registry_status",
            "invalid",
            "blocked_registry_missing_or_invalid",
        ),
        (
            "release_state_status",
            "present_invalid_or_forked",
            "blocked_release_state_conflict",
        ),
    ],
)
def test_first_failure_precedence_ignores_all_later_failures(
    earlier_field: str,
    earlier_value: str,
    expected: str,
) -> None:
    values = {
        "contract_binding_status": "exact",
        "validator_bundle_status": "exact",
        "manifest_status": "exact",
        "source_install_status": "identical",
        "registry_status": "valid_exact",
        "release_state_status": "absent_bootstrap_candidate",
        "offline_validation_status": "passed",
    }
    ordered = list(values)
    index = ordered.index(earlier_field)
    values[earlier_field] = earlier_value
    later_failures = {
        "validator_bundle_status": "known_invalid",
        "manifest_status": "known_invalid",
        "source_install_status": "installed_drift",
        "registry_status": "invalid",
        "release_state_status": "present_invalid_or_forked",
        "offline_validation_status": "failed",
    }
    for field in ordered[index + 1 :]:
        values[field] = later_failures[field]
    assert checker._select_terminal_status(*values.values()) == expected


@pytest.mark.parametrize(
    "mutation",
    [
        "missing",
        "extra",
        "duplicate",
        "reordered",
        "case_varied",
        "digest_mismatch",
    ],
)
def test_stage3_manifest_row_mutations_fail_in_owner_validator(
    mutation: str,
) -> None:
    with _exact_fixture() as fixture:
        stage3 = fixture.owners.stage3
        workflow_root = fixture.installed_skills_root / "mythic-edge-workflow"
        stage3.WORKFLOW_ROOT = workflow_root
        stage3.WORKFLOW_SNAPSHOT_FILES = tuple(
            workflow_root / relative
            for relative in checker.WORKFLOW_SNAPSHOT_RELATIVE_PATHS
        )
        rows = stage3.current_skill_manifest()
        changed = copy.deepcopy(rows)
        if mutation == "missing":
            changed.pop()
        elif mutation == "extra":
            changed.append({"path": "unexpected.txt", "sha256": "0" * 64})
        elif mutation == "duplicate":
            changed.append(copy.deepcopy(changed[-1]))
        elif mutation == "reordered":
            changed[0], changed[1] = changed[1], changed[0]
        elif mutation == "case_varied":
            changed[0]["path"] = changed[0]["path"].swapcase()
        else:
            changed[0]["sha256"] = "0" * 64
        with mock.patch.object(
            stage3,
            "current_skill_manifest",
            return_value=changed,
        ):
            observation = checker._manifest_observation(stage3, workflow_root)
        assert observation.status == "known_invalid"


@pytest.mark.parametrize(
    "mutation",
    ["missing", "extra", "renamed", "content_drift"],
)
def test_installed_tree_drift_is_detected_by_installer_owner(
    mutation: str,
) -> None:
    with _exact_fixture() as fixture:
        installed = (
            fixture.installed_skills_root / "mythic-edge-role-pool"
        )
        if mutation == "missing":
            shutil.rmtree(installed)
        elif mutation == "extra":
            (installed / "unexpected.txt").write_text("synthetic", encoding="utf-8")
        elif mutation == "renamed":
            source = installed / "SKILL.md"
            source.rename(installed / "SKILL-renamed.md")
        else:
            (installed / "SKILL.md").write_text("synthetic", encoding="utf-8")
        source, target, status = checker._tree_observations(
            fixture.roots,
            fixture.owners,
        )
        assert source.status == "observed"
        if mutation == "missing":
            assert target.status == "installed_missing"
            assert status == "installed_missing"
        else:
            assert target.status == "observed"
            assert status == "installed_drift"


def test_nonordinary_and_reparse_tree_results_fail_closed_without_skip() -> None:
    with _exact_fixture() as fixture:
        target = fixture.installed_skills_root / "mythic-edge-role-pool"
        with mock.patch.object(
            fixture.owners.installer,
            "_target_tree_unsafe_reason",
            return_value="target_reparse_point",
        ):
            _, installed, status = checker._tree_observations(
                fixture.roots,
                fixture.owners,
            )
        assert installed.status == "unsafe_or_unreadable"
        assert status == "unsafe_or_unreadable"
        assert target.is_dir()


def test_identically_drifted_source_and_install_still_block() -> None:
    with _exact_fixture() as fixture:
        for root in (
            fixture.repository_root / checker.SOURCE_SKILL_RELATIVE_PATH,
            fixture.installed_skills_root / "mythic-edge-role-pool",
        ):
            cache = root / "__pycache__"
            cache.mkdir()
            (cache / "synthetic.pyc").write_bytes(b"synthetic")
        source, installed, status = checker._tree_observations(
            fixture.roots,
            fixture.owners,
        )
        assert source.sha256 == installed.sha256
        assert source.sha256 != checker.SOURCE_TREE_SHA256
        assert status == "installed_drift"


def test_absent_fixed_parent_proves_both_inputs_without_enumeration() -> None:
    with _exact_fixture(with_registry=False) as fixture:
        role_pool = fixture.repository_root / "docs/role_pool"
        assert not role_pool.exists()
        with mock.patch.object(
            Path,
            "iterdir",
            side_effect=AssertionError("enumeration forbidden"),
        ):
            result = checker._fixed_inputs(
                fixture.repository_root,
                fixture.owners.pool,
            )
        assert result == checker.FixedInputObservation(
            "absent",
            None,
            "absent_bootstrap_candidate",
            None,
        )
        assert not role_pool.exists()


def test_present_ordinary_parent_with_absent_release_is_candidate() -> None:
    with _exact_fixture() as fixture:
        result = checker._fixed_inputs(
            fixture.repository_root,
            fixture.owners.pool,
        )
        assert result.registry_status == "valid_exact"
        assert result.release_state_status == "absent_bootstrap_candidate"
        assert result.release_state_sha256 is None


@pytest.mark.parametrize(
    "parent_shape",
    ["nonordinary", "case_ambiguous", "unreadable", "identity_unstable"],
)
def test_fixed_parent_unsafe_or_ambiguous_projects_unknown(
    parent_shape: str,
) -> None:
    with _exact_fixture(with_registry=False) as fixture:
        role_pool = fixture.repository_root / "docs/role_pool"
        if parent_shape == "nonordinary":
            role_pool.write_text("synthetic", encoding="utf-8")
            result = checker._fixed_inputs(
                fixture.repository_root,
                fixture.owners.pool,
            )
        elif parent_shape == "case_ambiguous":
            role_pool.with_name("Role_Pool").mkdir()
            result = checker._fixed_inputs(
                fixture.repository_root,
                fixture.owners.pool,
            )
        else:
            original = checker._observe_component

            def unstable(path: Path, kind: str) -> object:
                if path == role_pool:
                    state = (
                        "unknown"
                        if parent_shape == "unreadable"
                        else "identity_unstable"
                    )
                    return checker.FileObservation(state)
                return original(path, kind)

            with mock.patch.object(checker, "_observe_component", side_effect=unstable):
                result = checker._fixed_inputs(
                    fixture.repository_root,
                    fixture.owners.pool,
                )
        assert result.registry_status == "unknown"
        assert result.release_state_status == "unknown"


@pytest.mark.parametrize(
    "mutation",
    [
        "malformed",
        "duplicate_key",
        "unknown_field",
        "wrong_self_digest",
        "wrong_repository",
        "inactive_entry",
        "missing_offline_operation",
    ],
)
def test_registry_invalid_matrix_uses_strict_owner_parser(
    mutation: str,
) -> None:
    with _exact_fixture() as fixture:
        pool = fixture.owners.pool
        registry = _valid_registry(pool)
        if mutation == "malformed":
            payload = b"{not-json}\n"
        elif mutation == "duplicate_key":
            payload = b'{"schema_version":"a","schema_version":"b"}\n'
        else:
            if mutation == "unknown_field":
                registry["unexpected"] = False
            elif mutation == "wrong_self_digest":
                registry["registry_sha256"] = "0" * 64
            else:
                entry = copy.deepcopy(registry["entries"][0])
                if mutation == "wrong_repository":
                    entry["canonical_name"] = "tahjali11/not-mythic-edge"
                elif mutation == "inactive_entry":
                    entry["status"] = "retired"
                else:
                    entry["permitted_operations"] = ["inspect"]
                entry = _signed(pool, entry, "entry_sha256")
                registry["entries"] = [entry]
                registry = _signed(pool, registry, "registry_sha256")
            payload = pool.trusted_native_canonical_bytes(registry)
        status, digest = checker._parse_registry(
            checker.FileObservation("exact", payload),
            pool,
        )
        assert status == "invalid"
        assert digest is None


def test_registry_missing_and_unreadable_are_distinct() -> None:
    with _exact_fixture() as fixture:
        pool = fixture.owners.pool
        assert checker._parse_registry(
            checker.FileObservation("absent"),
            pool,
        ) == ("absent", None)
        assert checker._parse_registry(
            checker.FileObservation("unknown"),
            pool,
        ) == ("unknown", None)


def test_release_state_valid_r0_and_later_chains_are_conflicts() -> None:
    with _exact_fixture() as fixture:
        pool = fixture.owners.pool
        r0 = _release_record(pool)
        r1 = _release_record(pool, "R1", predecessor=r0)
        rebaseline = _release_rebaseline(pool, r0)
        rebased_r1 = _release_record(pool, "R1", predecessor=rebaseline)
        for field in (
            "contract_sha256",
            "skill_tree_sha256",
            "registry_sha256",
            "validator_bundle_sha256",
        ):
            rebased_r1[field] = rebaseline[field]
        rebased_r1["accepted_at_utc"] = "2026-07-30T00:00:02Z"
        rebased_r1 = _signed(pool, rebased_r1, "record_sha256")
        for records in (
            [r0],
            [r0, r1],
            [r0, rebaseline],
            [r0, rebaseline, rebased_r1],
        ):
            payload = b"".join(
                pool.trusted_native_canonical_bytes(record)
                for record in records
            )
            status, digest = checker._parse_release_state(
                checker.FileObservation("exact", payload),
                pool,
            )
            assert status == "present_valid_chain"
            assert digest == hashlib.sha256(payload).hexdigest()


def test_release_state_selects_rebaseline_tip_and_rejects_invalid_forms() -> None:
    with _exact_fixture() as fixture:
        pool = fixture.owners.pool
        r0 = _release_record(pool)
        rebaseline = _release_rebaseline(pool, r0)
        valid_payload = b"".join(
            pool.trusted_native_canonical_bytes(record)
            for record in (r0, rebaseline)
        )
        assert checker._parse_release_state(
            checker.FileObservation("exact", valid_payload),
            pool,
        ) == ("present_valid_chain", hashlib.sha256(valid_payload).hexdigest())
        assert pool.trusted_native_current_rung([r0, rebaseline]) == "R0"
        bindings = pool.trusted_native_current_release_bindings(
            [r0, rebaseline]
        )
        assert bindings is not None
        assert bindings["record_sha256"] == rebaseline["record_sha256"]
        assert bindings["contract_sha256"] == "9" * 64

        stale = copy.deepcopy(rebaseline)
        stale["predecessor_record_sha256"] = "0" * 64
        stale = _signed(pool, stale, "record_sha256")

        duplicate = copy.deepcopy(rebaseline)
        duplicate["record_id"] = "r0.rebaseline.duplicate"
        duplicate["predecessor_record_sha256"] = rebaseline["record_sha256"]
        duplicate["accepted_at_utc"] = "2026-07-30T00:00:02Z"
        duplicate = _signed(pool, duplicate, "record_sha256")

        non_r0 = copy.deepcopy(rebaseline)
        non_r0["to_rung"] = "R1"
        non_r0 = _signed(pool, non_r0, "record_sha256")

        wrong_binding = copy.deepcopy(rebaseline)
        wrong_binding["predecessor_registry_sha256"] = "0" * 64
        wrong_binding = _signed(pool, wrong_binding, "record_sha256")

        unchanged = _release_rebaseline(
            pool,
            r0,
            contract_sha256=str(r0["contract_sha256"]),
        )

        observed_r0 = copy.deepcopy(r0)
        observed_r0["observation_receipt_sha256s"] = ["1" * 64, "2" * 64]
        observed_r0 = _signed(pool, observed_r0, "record_sha256")

        for records in (
            [r0, stale],
            [r0, rebaseline, duplicate],
            [r0, non_r0],
            [r0, wrong_binding],
            [r0, unchanged],
            [observed_r0, _release_rebaseline(pool, observed_r0)],
        ):
            payload = b"".join(
                pool.trusted_native_canonical_bytes(record)
                for record in records
            )
            status, digest = checker._parse_release_state(
                checker.FileObservation("exact", payload),
                pool,
            )
            assert status == "present_invalid_or_forked"
            assert digest == hashlib.sha256(payload).hexdigest()


@pytest.mark.parametrize(
    "mutation",
    [
        "invalid_line",
        "fork",
        "duplicate",
        "empty",
        "partial_final_line",
    ],
)
def test_release_state_invalid_matrix_remains_conflict(
    mutation: str,
) -> None:
    with _exact_fixture() as fixture:
        pool = fixture.owners.pool
        r0 = _release_record(pool)
        r1 = _release_record(pool, "R1", predecessor=r0)
        if mutation == "invalid_line":
            payload = b"{invalid}\n"
        elif mutation == "fork":
            fork = copy.deepcopy(r1)
            fork["predecessor_record_sha256"] = "0" * 64
            fork = _signed(pool, fork, "record_sha256")
            payload = (
                pool.trusted_native_canonical_bytes(r0)
                + pool.trusted_native_canonical_bytes(fork)
            )
        elif mutation == "duplicate":
            payload = (
                pool.trusted_native_canonical_bytes(r0)
                + pool.trusted_native_canonical_bytes(r0)
            )
        elif mutation == "empty":
            payload = b""
        else:
            payload = pool.trusted_native_canonical_bytes(r0).rstrip(b"\n")
        status, digest = checker._parse_release_state(
            checker.FileObservation("exact", payload),
            pool,
        )
        assert status == "present_invalid_or_forked"
        assert digest == hashlib.sha256(payload).hexdigest()


def test_release_state_absent_and_unreadable_are_distinct() -> None:
    with _exact_fixture() as fixture:
        pool = fixture.owners.pool
        assert checker._parse_release_state(
            checker.FileObservation("absent"),
            pool,
        ) == ("absent_bootstrap_candidate", None)
        assert checker._parse_release_state(
            checker.FileObservation("unknown"),
            pool,
        ) == ("unknown", None)


def test_contract_and_owner_drift_block_before_lower_components() -> None:
    with _exact_fixture() as fixture:
        profile = (
            fixture.repository_root
            / "docs/contracts/trusted_owner_native_role_pool_profile.md"
        )
        profile.write_bytes(profile.read_bytes() + b"\n")
        packet, _ = checker._evaluate_for_tests(fixture.roots)
        assert packet["contract_binding_status"] == "known_invalid"
        assert packet["validator_bundle_status"] == "known_invalid"
        assert packet["terminal_status"] == "blocked_contract_binding_invalid"


def test_packet_is_deterministic_self_digested_and_final_lf_exact() -> None:
    with _exact_fixture() as fixture:
        first_packet, first = checker._evaluate_for_tests(fixture.roots)
        second_packet, second = checker._evaluate_for_tests(fixture.roots)
        assert first == second
        assert first_packet == second_packet
        assert first.endswith(b"\n")
        assert not first.endswith(b"\n\n")
        assert not first.startswith(b"\xef\xbb\xbf")
        preimage = dict(first_packet)
        preimage.pop("evidence_sha256")
        expected = hashlib.sha256(
            fixture.owners.pool.trusted_native_canonical_bytes(preimage)
        ).hexdigest()
        assert first_packet["evidence_sha256"] == expected
        assert checker._parse_packet(
            first.decode("utf-8"),
            fixture.owners.pool,
        ) == first_packet


def test_cli_emits_canonical_packet_as_exact_binary_bytes() -> None:
    with _exact_fixture(
        bind_current_source_tree=False,
        bind_current_manifest=False,
    ) as fixture:
        packet, encoded = checker._evaluate_for_tests(fixture.roots)
        completed = _run_raw_cli(fixture)

        assert completed.returncode == checker._exit_code(
            str(packet["terminal_status"])
        )
        assert completed.stdout == encoded
        assert completed.stdout.endswith(b"\n")
        assert b"\r\n" not in completed.stdout
        assert completed.stderr == b""


def test_cli_emits_packet_unavailable_as_exact_ascii_bytes() -> None:
    with _exact_fixture() as fixture:
        completed = _run_raw_cli(fixture, "unexpected-argument")

        assert completed.returncode == 3
        assert completed.stdout == b""
        assert completed.stderr == (
            checker.PACKET_UNAVAILABLE.encode("ascii") + b"\n"
        )
        assert b"\r\n" not in completed.stderr


def test_packet_rejects_duplicate_unknown_reordered_and_cross_field_drift() -> None:
    with _exact_fixture() as fixture:
        packet, encoded = checker._evaluate_for_tests(fixture.roots)
        pool = fixture.owners.pool
        duplicate = encoded.decode("utf-8").replace(
            "{",
            '{"schema_version":"duplicate",',
            1,
        )
        with pytest.raises(Exception):
            checker._parse_packet(duplicate, pool)

        unknown = dict(packet)
        unknown["unexpected"] = False
        assert checker._validate_packet(unknown, pool) == [
            "packet_fields_invalid"
        ]

        reordered = {"operation": packet["operation"]}
        reordered.update(packet)
        assert checker._validate_packet(reordered, pool) == [
            "packet_fields_invalid"
        ]

        inconsistent = copy.deepcopy(packet)
        inconsistent["eligible_for_independent_review"] = False
        inconsistent["evidence_sha256"] = pool.trusted_native_self_digest(
            inconsistent,
            "evidence_sha256",
        )
        assert "eligibility_inconsistent" in checker._validate_packet(
            inconsistent,
            pool,
        )


@pytest.mark.parametrize(
    "mutation",
    [
        "manifest_count",
        "source_digest",
        "partial_source",
        "installed_missing_counts",
        "absent_registry_digest",
        "absent_release_digest",
        "terminal",
        "effect_type",
        "effect",
        "authority_type",
        "authority",
    ],
)
def test_packet_cross_field_and_false_authority_rules(
    mutation: str,
) -> None:
    with _exact_fixture() as fixture:
        packet, _ = checker._evaluate_for_tests(fixture.roots)
        pool = fixture.owners.pool
        changed = copy.deepcopy(packet)
        if mutation == "manifest_count":
            changed["stage3_manifest_file_count"] = 38
        elif mutation == "source_digest":
            changed["source_tree_sha256"] = "0" * 64
        elif mutation == "partial_source":
            changed["source_tree_file_count"] = None
        elif mutation == "installed_missing_counts":
            changed["source_install_status"] = "installed_missing"
        elif mutation == "absent_registry_digest":
            changed["registry_status"] = "absent"
        elif mutation == "absent_release_digest":
            changed["release_state_sha256"] = "f" * 64
        elif mutation == "terminal":
            changed["terminal_status"] = "blocked_manifest_invalid"
        elif mutation == "effect_type":
            changed["effect_counts"] = []
        elif mutation == "effect":
            changed["effect_counts"]["task_creation_count"] = 1
        elif mutation == "authority_type":
            changed["authority_flags"] = []
        else:
            changed["authority_flags"]["live_ready"] = True
        changed["evidence_sha256"] = pool.trusted_native_self_digest(
            changed,
            "evidence_sha256",
        )
        assert checker._validate_packet(changed, pool)


def test_packet_and_cli_fallback_do_not_echo_private_values() -> None:
    with _exact_fixture() as fixture:
        packet, encoded = checker._evaluate_for_tests(fixture.roots)
        text = encoded.decode("utf-8")
        forbidden = (
            str(fixture.root),
            str(Path.home()),
            os.environ.get("USERNAME", ""),
            "Traceback",
            "FileNotFoundError",
        )
        assert all(not value or value not in text for value in forbidden)
        assert all(value == 0 for value in packet["effect_counts"].values())
        assert not any(packet["authority_flags"].values())

    stdout = io.StringIO()
    stderr = io.StringIO()
    private_argument = r"C:\private\do-not-echo"
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = checker.run([private_argument])
    assert exit_code == 3
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == checker.PACKET_UNAVAILABLE + "\n"
    assert private_argument not in stderr.getvalue()


def test_codex_home_override_is_rejected_before_installed_root_derivation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CODEX_HOME", r"C:\private\override")
    with mock.patch.object(
        Path,
        "home",
        side_effect=AssertionError("installed root must not be derived"),
    ):
        roots = checker._production_roots()
    assert roots.installed_skills_root is None


def test_missing_installed_root_never_calls_target_owner_functions() -> None:
    with _exact_fixture() as fixture:
        roots = checker.EvaluationRoots(fixture.repository_root, None)
        owners = fixture.owners
        manifest = checker._manifest_observation(owners.stage3, None)
        assert manifest.status == "unknown"
        with (
            mock.patch.object(
                owners.installer,
                "_target_tree_unsafe_reason",
                side_effect=AssertionError("installed target access forbidden"),
            ),
            mock.patch.object(
                owners.installer,
                "_directories_match",
                side_effect=AssertionError("installed target access forbidden"),
            ),
        ):
            source, installed, status = checker._tree_observations(roots, owners)
        assert source.status == "observed"
        assert installed.status == "unknown"
        assert status == "unknown"


def test_production_root_derivation_uses_installer_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CODEX_HOME", raising=False)
    installer = checker._load_module(
        "_r0_test_installer_derivation",
        REPO_ROOT / "tools/install_codex_skills.py",
    )
    roots = checker._production_roots()
    assert roots.installed_skills_root == installer._codex_home(None) / "skills"


def test_evaluation_performs_no_persistent_mutation_or_forbidden_calls() -> None:
    with _exact_fixture() as fixture:
        before = tuple(
            sorted(
                (
                    path.relative_to(fixture.root).as_posix(),
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
                for path in fixture.root.rglob("*")
                if path.is_file()
            )
        )
        with (
            mock.patch.object(
                Path,
                "write_bytes",
                side_effect=AssertionError("write forbidden"),
            ),
            mock.patch.object(
                Path,
                "write_text",
                side_effect=AssertionError("write forbidden"),
            ),
            mock.patch.object(
                Path,
                "mkdir",
                side_effect=AssertionError("mkdir forbidden"),
            ),
            mock.patch.object(
                Path,
                "unlink",
                side_effect=AssertionError("unlink forbidden"),
            ),
            mock.patch.object(
                Path,
                "rename",
                side_effect=AssertionError("rename forbidden"),
            ),
        ):
            packet, _ = checker._evaluate_for_tests(fixture.roots)
        after = tuple(
            sorted(
                (
                    path.relative_to(fixture.root).as_posix(),
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
                for path in fixture.root.rglob("*")
                if path.is_file()
            )
        )
        assert before == after
        assert all(value == 0 for value in packet["effect_counts"].values())


def test_cleanup_runs_after_success_and_failure() -> None:
    success_root: Path
    with _exact_fixture() as fixture:
        success_root = fixture.root
        checker._evaluate_for_tests(fixture.roots)
    assert not success_root.exists()

    failure_root: Path
    with pytest.raises(RuntimeError), _exact_fixture() as fixture:
        failure_root = fixture.root
        raise RuntimeError("synthetic failure")
    assert not failure_root.exists()
