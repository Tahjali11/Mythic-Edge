#!/usr/bin/env python3
"""Validate the non-authoritative Stage-3 behavioral-planning observation."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "mythic_edge_role_pool_stage3_behavioral_planning.v1"
STAGE = 3
OPERATION = "deterministic_synthetic_behavioral_planning_only"
PRODUCER = "mythic-edge-role-pool-stage3-harness"
EXPECTED_OBSERVATION_COUNT = 2
SHARED_ROLE = "Codex B"
SCENARIO_ID = "stage3-synthetic-three-repository-three-lane-same-role-v1"
FINDING_ID = "MRP-RC-003"

STAGE2_ATTEMPT_SERIES_ID = "71753f13-17a3-490c-9ea1-217e7b955779"
STAGE2_ENTRY_EVIDENCE: dict[str, object] = {
    "attempt_series_id": STAGE2_ATTEMPT_SERIES_ID,
    "portable_wrapper_length_bytes": 55835,
    "portable_wrapper_sha256": (
        "306af1db3e6229202c274e41498d1284ec693a51419a2b970501b7b910bd351a"
    ),
    "portable_wrapper_digest": (
        "abb16b21f2318bac7283cdef8190d32a418c6267a37c5190c22f0f86a2954a99"
    ),
    "pair_payload_length_bytes": 116597,
    "pair_payload_sha256": (
        "e9392d046266da3b3229503e8df383832d7bb34b576d1dbb30e46bfab2a00525"
    ),
    "pair_digest": (
        "017598959f999511b4bb7dc96e498a8803415e15325e6389922aad0cdfa7c02a"
    ),
    "observations": [
        {
            "observation_attempt": "1_of_2",
            "canonical_length_bytes": 56905,
            "canonical_sha256": (
                "841598189ca69e8ac1e18980627f6ac0d0e62479589d3bbda07afae655dd28a9"
            ),
            "digest": (
                "564cdea29209e90788366578a7775e009f76278249a530b7af73c3f41ccd9717"
            ),
            "evidence_index_digest": (
                "ed400a26f53f4753b314aa96a7d924faa70434f0a892acf7ccb8c8711fa21fe4"
            ),
        },
        {
            "observation_attempt": "2_of_2",
            "canonical_length_bytes": 56904,
            "canonical_sha256": (
                "b76c83fbd100f0deb3be25e20b73da1262004d7ad2c22126724cdd8976d18293"
            ),
            "digest": (
                "7dd07f8a7110ec6b407b3bdae44422ee64c43f2cbbde5b1a49fce5b64dbe1397"
            ),
            "evidence_index_digest": (
                "425c9d477e0c437b1db38621b1a63f05d711ddc552d10da91f987cbdf5b9382b"
            ),
        },
    ],
    "entry_manifest_file_count": 30,
    "entry_manifest_digest": (
        "2b713c831de0cefc9f488699ce163eba904467260cfcbdc134d932f2b24c8b39"
    ),
    "entry_manifest_canonical_length_bytes": 5070,
    "entry_manifest_canonical_sha256": (
        "3eabb2633eaecbd734a3345af9a035061b71e352020494779ad8bfd03846b545"
    ),
    "pair_embedded_review_status": "pending_at_pair_creation",
    "subsequent_independent_review_status": "accepted",
    "subsequent_review_receipt_schema": (
        "mythic_edge_role_pool_stage2_independent_review_receipt.v1"
    ),
    "subsequent_review_receipt_digest": (
        "8bd72f917f5b7782121571a6c9dc23964151e66d352c5d1751ad66f59a103f8e"
    ),
    "subsequent_review_receipt_canonical_length_bytes": 2520,
    "subsequent_review_receipt_canonical_sha256": (
        "fcfdee84941ba1e30765cee56652aabf09a12cf1b6f212b4bd375224a1717bb2"
    ),
    "subsequent_review_receipt_storage": "transcript_only",
    "accepted_for_stage3_entry": True,
    "acceptance_authority_ref": (
        "user:stage3-contract/accepted-stage2-pair/"
        + STAGE2_ATTEMPT_SERIES_ID
    ),
    "separate_review_receipt_file_claimed": False,
    "stage2_advancement_claimed": False,
}

SKILL_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_ROOT = SKILL_ROOT.parent / "mythic-edge-workflow"
WORKFLOW_SNAPSHOT_FILES = (
    WORKFLOW_ROOT / "SKILL.md",
    WORKFLOW_ROOT / "agents" / "openai.yaml",
    WORKFLOW_ROOT / "scripts" / "accept_fallback_prompt.py",
)

# This is the exact accepted Stage-2 30-file snapshot. It is intentionally
# historical: the additive Stage-3 contract changes are recorded separately.
STAGE2_BASELINE_FILES = {
    "mythic-edge-role-pool/SKILL.md": "90cbe6c798ae7209c47f5f134f30185aba4f13fe4c60eccb7d204fc133365056",
    "mythic-edge-role-pool/agents/openai.yaml": "34bf1fb42a79f2765d88b3c46ec728e69975759ed4839577aba5e559e6ffe2f9",
    "mythic-edge-role-pool/references/fallback-and-recovery.md": "fac1f4ea306f1b371e188416ae30f74a864997b0ac466281de421ce98eb76dad",
    "mythic-edge-role-pool/references/fallback-pickup-fixture/injection.json": "5322c32f5e252f9b74eec3264b34c4a0e04c32440d1b2a7f07ac0810cf672e3e",
    "mythic-edge-role-pool/references/fallback-pickup-fixture/pickup.json": "1b11d1f74d379e8f6b75ea2ae921e1c4ac11685b5d5f11ada39c68e7df8d7a32",
    "mythic-edge-role-pool/references/fallback-pickup-fixture/prompt.json": "d3d0c5b84dfaa99745a8446b7fffa54783b5e6629cb5e5d9aa9a984aa1861f0f",
    "mythic-edge-role-pool/references/pool-state-schema.md": "8321e9850aa1d3b044031427b1f188047281fc9df090b2f06e13dca5d2a505e2",
    "mythic-edge-role-pool/references/release-remediation-matrix.md": "531107d3e35154757b303b0663b2e6938d151cbff3c27b8226e390b666a5a7c6",
    "mythic-edge-role-pool/references/role-readiness-and-safety.md": "1013a0430c178f8dc0b09c58745ac52389f8234c8fded83aa770253430a16a6c",
    "mythic-edge-role-pool/references/stage4-canary-exception.md": "ab21df4d290d4b010ead37111f520b9cb92154d14c742ca914ab2799a5c79047",
    "mythic-edge-role-pool/scripts/check_fallback_pickup.py": "c38191547694387f27af0614edf2566b80a1adc5b31f840bb81cd3dc6f9cf406",
    "mythic-edge-role-pool/scripts/check_pool_plan.py": "0cff4b949703de29abb598d1284db298c1b9fa86d95a7335162b13d4b5f309ee",
    "mythic-edge-role-pool/scripts/check_stage4_canary_exception.py": "5fc41cee93396979d2689eea43b7a82fd869b64bbe8123b50b34c91fb51d01d9",
    "mythic-edge-role-pool/scripts/codex_launcher_contract.py": "400fe0e8858e485a8066aa686ea111f5f3c300a5760169274d1a43eca7dbcafd",
    "mythic-edge-role-pool/scripts/offline_gate_guard/offline_guard.py": "e508217276391b327119a16f8c21bbaa845c525868b4b3977bfd8f5e6d052fd9",
    "mythic-edge-role-pool/scripts/offline_gate_guard/sitecustomize.py": "ffa0a190b3617033825a9d284fb7e612cacef079fb551cdc950f8d3c401ca80c",
    "mythic-edge-role-pool/scripts/pool_test_fixtures.py": "3a2a6cf0c712f773de03a4c4928ed68879811a76e95f188018f1d3ced7440dab",
    "mythic-edge-role-pool/scripts/regenerate_fallback_pickup_fixture.py": "ac871a4dfcfb1a3cf517c6517af06699357b83d734e2084abd63300a3f0ae331",
    "mythic-edge-role-pool/scripts/run_release_tests.py": "43cc3835ec60fc92c5be1b7cecf9ebe084c06c14b8c2cef0ab3e39d1bb45d8b8",
    "mythic-edge-role-pool/scripts/test_check_pool_plan.py": "23f40b17ca2a8ba1bf98b82315c4cfb955ed3414af52d867e7b7a3350ce1ff50",
    "mythic-edge-role-pool/scripts/test_codex_launcher_contract.py": "988df3825f79080cacbed0e8af19008057373782b51d9980df09479403d35c67",
    "mythic-edge-role-pool/scripts/test_fallback_pickup.py": "9a7e244a3ee66fb1f02e335c3967bb3b836d8347202918a24695daf23510c4de",
    "mythic-edge-role-pool/scripts/test_offline_gate_guard.py": "f5f1f964e4b8a107a88de3c24ba340e91a9c0a4d6541bafbdcd6bf6f46e4274c",
    "mythic-edge-role-pool/scripts/test_pool_results.py": "6636a4b10f561e0df7f1770174e472669902c4efebc84aa32b96ee7b052fdb67",
    "mythic-edge-role-pool/scripts/test_release_adversarial.py": "717f3f5f769bbd9c6eedba998da75a85192912b0085fa98847a59f2095a7779c",
    "mythic-edge-role-pool/scripts/test_skill_contract.py": "73f16fae0fb044cd873b66ef7d9551bd5a0d954394232a41accb01d60bbb7778",
    "mythic-edge-role-pool/scripts/test_stage4_canary_exception.py": "84a3272f1ad2380206e7ef9dd4ceaa1ae71ed500b6be26a36cd3090b1bd06612",
    "mythic-edge-workflow/SKILL.md": "04c229e2604ec965391d0044947d5a985049fc69508b79c88aec09e3732f14bb",
    "mythic-edge-workflow/agents/openai.yaml": "0dc1f6b8acfac33f9f7a2628e093bc7fddbc2cb52a8bb41f9c22e56a57aa0c2f",
    "mythic-edge-workflow/scripts/accept_fallback_prompt.py": "47aa25f3da14bfade71ed2862e4b7d85248c8356b1c90bdfd61222133b0a875d",
}

ALLOWED_MODIFIED_PATHS = {
    "mythic-edge-role-pool/SKILL.md",
    "mythic-edge-role-pool/references/fallback-and-recovery.md",
    "mythic-edge-role-pool/references/pool-state-schema.md",
    "mythic-edge-role-pool/references/release-remediation-matrix.md",
    "mythic-edge-role-pool/references/role-readiness-and-safety.md",
    "mythic-edge-role-pool/references/stage4-canary-exception.md",
    "mythic-edge-role-pool/scripts/check_pool_plan.py",
    "mythic-edge-role-pool/scripts/codex_launcher_contract.py",
    "mythic-edge-role-pool/scripts/run_release_tests.py",
    "mythic-edge-role-pool/scripts/test_check_pool_plan.py",
    "mythic-edge-role-pool/scripts/test_codex_launcher_contract.py",
    "mythic-edge-role-pool/scripts/test_pool_results.py",
    "mythic-edge-role-pool/scripts/test_skill_contract.py",
}
PRE_APP_SERVER_ALLOWED_ADDED_PATHS = {
    "mythic-edge-role-pool/references/external-isolation-broker.md",
    (
        "mythic-edge-role-pool/references/"
        "external-isolation-broker-v3-corrective-successor.md"
    ),
    (
        "mythic-edge-role-pool/references/"
        "external-isolation-broker-v4-corrective-successor.md"
    ),
    (
        "mythic-edge-role-pool/references/"
        "external-isolation-broker-v5-corrective-successor.md"
    ),
    "mythic-edge-role-pool/references/stage3-behavioral-planning.md",
    "mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py",
    "mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py",
}

ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT = 37
ACCEPTED_APP_SERVER_MANIFEST_FILE_COUNT = 39
EXPECTED_CURRENT_MANIFEST_FILE_COUNT = 41
SUCCESSOR_SKILL_RELATIVE_PATH = (
    "references/external-isolation-broker-v3-corrective-successor.md"
)
SUCCESSOR_MANIFEST_PATH = "mythic-edge-role-pool/" + SUCCESSOR_SKILL_RELATIVE_PATH
SUCCESSOR_SHA256 = (
    "44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55"
)
V4_SUCCESSOR_SKILL_RELATIVE_PATH = (
    "references/external-isolation-broker-v4-corrective-successor.md"
)
V4_SUCCESSOR_MANIFEST_PATH = (
    "mythic-edge-role-pool/" + V4_SUCCESSOR_SKILL_RELATIVE_PATH
)
V4_SUCCESSOR_SHA256 = (
    "628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487"
)
V5_SUCCESSOR_SKILL_RELATIVE_PATH = (
    "references/external-isolation-broker-v5-corrective-successor.md"
)
V5_SUCCESSOR_MANIFEST_PATH = (
    "mythic-edge-role-pool/" + V5_SUCCESSOR_SKILL_RELATIVE_PATH
)
V5_SUCCESSOR_SHA256 = (
    "81aa7400268c0c23d8a2d14633c19cebdb64d464add7650cec53468f63f0b5d4"
)
STAGE3_PLANNING_SKILL_RELATIVE_PATH = "references/stage3-behavioral-planning.md"
STAGE3_PLANNING_MANIFEST_PATH = (
    "mythic-edge-role-pool/" + STAGE3_PLANNING_SKILL_RELATIVE_PATH
)
V5_CURRENT_RECIPE_RECEIPT_BINDING_AMENDMENT_SHA256 = (
    "6991beb7bdc50005216236b78daa348d5921b86f3e31a9228d072ed6310678e3"
)
V5_CURRENT_RECIPE_SHA256 = (
    "4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3"
)
V5_CURRENT_RECIPE_REVIEW_REF = (
    "build_recipe_review_v1_6128230418da966dd28bdc271edbf6d9"
)
V5_CURRENT_RECIPE_REVIEW_SHA256 = (
    "b0db654fce1316984c7e0380b85e77caadac580a256313bc2f41bb872c32667f"
)
V5_CURRENT_RECIPE_PREDECESSOR_STATIC_PREFLIGHT_SHA256 = (
    "7bd7855164cfd0b70f3f51b0b4c97b82ca1237b32a0cea0bef8960f90bea5fcd"
)
V5_CURRENT_RECIPE_SUCCESSOR_STATIC_PREFLIGHT_SHA256 = (
    "ad32aa287651e721c08d1cf900f5809fdc708b3c232c3a5b9ca5e54d5b86d065"
)
V5_BUILD_RECONCILIATION_AMENDMENT_SHA256 = (
    "e2742a64463940bd47e29cfc160c6792dc10822e9df3a8e1e04565bf5758ba6d"
)
V5_BUILD_RECONCILIATION_REVIEW_EVIDENCE_SHA256 = (
    "c2aeac32cf5e6b93f4d6cd0dbda547dc57ef959190d402ae572de2e12c399565"
)
V5_BUILD_RECONCILIATION_PREDECESSOR_STATIC_PREFLIGHT_SHA256 = (
    V5_CURRENT_RECIPE_SUCCESSOR_STATIC_PREFLIGHT_SHA256
)
V5_BUILD_RECONCILIATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256 = (
    "b0c44a82bccc95333b9340834c0b9dbbbf7fd5dace9788958dda3f9216f8e984"
)
V5_CHARACTERIZATION_ENVELOPE_AMENDMENT_SHA256 = (
    "9d84e547d7b71b06c3f04f6bfdd114763eb6ca3134fa627429e1f906d945ad5d"
)
V5_CHARACTERIZATION_ENVELOPE_REVIEW_EVIDENCE_SHA256 = (
    "5f6a6dcc5e0ad1150aeb302e049ef0ec50900aa31dd93ef1ea5c03195057db53"
)
V5_CHARACTERIZATION_SYNTHETIC_MATRIX_SHA256 = (
    "9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526"
)
V5_CHARACTERIZATION_PREDECESSOR_STATIC_PREFLIGHT_SHA256 = (
    V5_BUILD_RECONCILIATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256
)
V5_CHARACTERIZATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256 = (
    "95599612548ba08beff8c4c10377815d0aa80b203fe0e3115ccf0ea7d911e6af"
)
V5_REAL_SOURCE_ADAPTER_AMENDMENT_SHA256 = (
    "9b29d4546da706a8ceae8f106cb4e4acd7851587700089920898781005627c34"
)
V5_REAL_SOURCE_ADAPTER_REVIEW_EVIDENCE_SHA256 = (
    "bdef51e12ae9de10670c09076349e84ff23e5b543f67838b320bbb892a1e2be4"
)
V5_CHARACTERIZATION_ADAPTER_SYNTHETIC_MATRIX_SHA256 = (
    "2d6cee277836948115925f3629e4f0babe23e975dd3eac96c97a3429d776c8f7"
)
V5_REAL_SOURCE_ADAPTER_PREDECESSOR_STATIC_PREFLIGHT_SHA256 = (
    V5_CHARACTERIZATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256
)
V5_REAL_SOURCE_ADAPTER_SUCCESSOR_STATIC_PREFLIGHT_SHA256 = (
    "e9a10d67ddc359d4b7275c49a5187727d9be02c59e852a7b3183a2a357b224f0"
)
APP_SERVER_ADAPTER_SKILL_RELATIVE_PATH = (
    "scripts/trusted_native_app_server_adapter.py"
)
APP_SERVER_ADAPTER_MANIFEST_PATH = (
    "mythic-edge-role-pool/" + APP_SERVER_ADAPTER_SKILL_RELATIVE_PATH
)
APP_SERVER_ADAPTER_SHA256 = (
    "9a24c6b2f39a327aa6ad0728ba54263f0da134165e9c1bacf9414f50729f9a18"
)
APP_SERVER_ADAPTER_TEST_SKILL_RELATIVE_PATH = (
    "scripts/test_trusted_native_app_server_adapter.py"
)
APP_SERVER_ADAPTER_TEST_MANIFEST_PATH = (
    "mythic-edge-role-pool/" + APP_SERVER_ADAPTER_TEST_SKILL_RELATIVE_PATH
)
APP_SERVER_ADAPTER_TEST_SHA256 = (
    "42e1d4d2e1edbf3c80b9d85e1b256afdc5f4475e18f0d662f7414c23af7a33be"
)
APP_SERVER_ADDED_PATHS = {
    APP_SERVER_ADAPTER_MANIFEST_PATH,
    APP_SERVER_ADAPTER_TEST_MANIFEST_PATH,
}
PRE_APP_NATIVE_ALLOWED_ADDED_PATHS = (
    PRE_APP_SERVER_ALLOWED_ADDED_PATHS | APP_SERVER_ADDED_PATHS
)
APP_NATIVE_ADAPTER_SKILL_RELATIVE_PATH = (
    "scripts/trusted_native_app_direct_task_adapter.py"
)
APP_NATIVE_ADAPTER_MANIFEST_PATH = (
    "mythic-edge-role-pool/" + APP_NATIVE_ADAPTER_SKILL_RELATIVE_PATH
)
APP_NATIVE_ADAPTER_SHA256 = (
    "b0eb739e960a342d95f148f6d2c57b121a2bed48c972907bc379cdbd2042d831"
)
APP_NATIVE_ADAPTER_TEST_SKILL_RELATIVE_PATH = (
    "scripts/test_trusted_native_app_direct_task_adapter.py"
)
APP_NATIVE_ADAPTER_TEST_MANIFEST_PATH = (
    "mythic-edge-role-pool/" + APP_NATIVE_ADAPTER_TEST_SKILL_RELATIVE_PATH
)
APP_NATIVE_ADAPTER_TEST_SHA256 = (
    "98bdec5936129946cc95a6cebce2645a3da50c81894e6c018e2b42739af50375"
)
APP_NATIVE_ADDED_PATHS = {
    APP_NATIVE_ADAPTER_MANIFEST_PATH,
    APP_NATIVE_ADAPTER_TEST_MANIFEST_PATH,
}
ALLOWED_ADDED_PATHS = PRE_APP_NATIVE_ALLOWED_ADDED_PATHS | APP_NATIVE_ADDED_PATHS
PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS = {
    SUCCESSOR_MANIFEST_PATH: SUCCESSOR_SHA256,
    V4_SUCCESSOR_MANIFEST_PATH: V4_SUCCESSOR_SHA256,
    V5_SUCCESSOR_MANIFEST_PATH: V5_SUCCESSOR_SHA256,
}
PRE_APP_NATIVE_PINNED_SUCCESSOR_DIGESTS = {
    **PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS,
    APP_SERVER_ADAPTER_MANIFEST_PATH: APP_SERVER_ADAPTER_SHA256,
    APP_SERVER_ADAPTER_TEST_MANIFEST_PATH: APP_SERVER_ADAPTER_TEST_SHA256,
}
PINNED_SUCCESSOR_DIGESTS = {
    **PRE_APP_NATIVE_PINNED_SUCCESSOR_DIGESTS,
    APP_NATIVE_ADAPTER_MANIFEST_PATH: APP_NATIVE_ADAPTER_SHA256,
    APP_NATIVE_ADAPTER_TEST_MANIFEST_PATH: APP_NATIVE_ADAPTER_TEST_SHA256,
}
REVIEWED_APP_SERVER_MODIFIED_DIGESTS = {
    (
        "mythic-edge-role-pool/scripts/check_pool_plan.py"
    ): "af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d",
    (
        "mythic-edge-role-pool/scripts/test_check_pool_plan.py"
    ): "60201804ed1700d5d75b615a39fc06ad0585b7073ca0a48d07e4fc99579f7b49",
}
REVIEWED_APP_NATIVE_MODIFIED_DIGESTS = {
    (
        "mythic-edge-role-pool/scripts/check_pool_plan.py"
    ): "5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361",
    (
        "mythic-edge-role-pool/scripts/test_check_pool_plan.py"
    ): "a4b7a74925f16f12dc7c3b1de71a234bff832ea1aa645d884424466bad1fb93d",
}


class ManifestTransitionError(ValueError):
    """Signal that the current filesystem cannot produce the pinned transition."""

SYNTHETIC_REPOSITORIES = [
    "synthetic/mythic-edge-analytics",
    "synthetic/mythic-edge-corpus",
    "synthetic/mythic-edge-fable-engine",
]
SYNTHETIC_LANES: list[dict[str, object]] = [
    {
        "lane_id": "stage3-synthetic-b-analytics",
        "repository_id": SYNTHETIC_REPOSITORIES[0],
        "synthetic_issue_number": 3001,
        "role": SHARED_ROLE,
        "dependencies": [],
        "modeled_write_paths": ["docs/contracts/stage3-synthetic-contract.md"],
        "global_contract_surfaces": ["synthetic.analytics.contract.v1"],
        "protected_surfaces": [],
        "external_state_ids": [],
        "invalidation_risks": [],
        "repository_read_authorized": False,
        "dispatch_authorized": False,
        "selected_for_launch": False,
    },
    {
        "lane_id": "stage3-synthetic-b-corpus",
        "repository_id": SYNTHETIC_REPOSITORIES[1],
        "synthetic_issue_number": 3002,
        "role": SHARED_ROLE,
        "dependencies": [],
        "modeled_write_paths": ["docs/contracts/stage3-synthetic-contract.md"],
        "global_contract_surfaces": ["synthetic.corpus.contract.v1"],
        "protected_surfaces": [],
        "external_state_ids": [],
        "invalidation_risks": [],
        "repository_read_authorized": False,
        "dispatch_authorized": False,
        "selected_for_launch": False,
    },
    {
        "lane_id": "stage3-synthetic-b-fable-engine",
        "repository_id": SYNTHETIC_REPOSITORIES[2],
        "synthetic_issue_number": 3003,
        "role": SHARED_ROLE,
        "dependencies": [],
        "modeled_write_paths": ["docs/contracts/stage3-synthetic-contract.md"],
        "global_contract_surfaces": ["synthetic.fable.contract.v1"],
        "protected_surfaces": [],
        "external_state_ids": [],
        "invalidation_risks": [],
        "repository_read_authorized": False,
        "dispatch_authorized": False,
        "selected_for_launch": False,
    },
]

EXPECTED_SCENARIO: dict[str, object] = {
    "scenario_id": SCENARIO_ID,
    "synthetic": True,
    "repository_count": 3,
    "lane_count": 3,
    "shared_role": SHARED_ROLE,
    "repositories": SYNTHETIC_REPOSITORIES,
    "lanes": SYNTHETIC_LANES,
    "source_repository_read_performed": False,
    "repository_authority_created": False,
    "dispatch_authority_created": False,
    "v3_plan_document_emitted": False,
    "agent_behavior_tested": False,
}

EFFECT_COUNTER_FIELDS = (
    "repository_read_count",
    "git_request_count",
    "github_request_count",
    "connector_request_count",
    "browser_request_count",
    "api_request_count",
    "claim_count",
    "lease_count",
    "reservation_count",
    "pooled_launch_count",
    "nested_agent_launch_count",
    "role_task_creation_count",
    "v3_plan_document_count",
    "role_artifact_write_count",
    "repository_write_count",
    "persistent_local_write_count",
    "github_write_count",
    "issue_write_count",
    "commit_count",
    "push_count",
    "pull_request_write_count",
    "integration_action_count",
    "credential_access_count",
    "external_mutation_count",
    "deployment_count",
    "production_effect_count",
    "stage_advancement_count",
    "finding_resolution_count",
)

ASSERTION_FIELDS = (
    "stage2_entry_evidence_bound",
    "explicit_contract_transition_bound",
    "synthetic_only",
    "three_repositories_three_lanes",
    "same_role_across_all_lanes",
    "complete_pairwise_coverage",
    "positive_compatibility_passed",
    "fail_closed_exclusions_passed",
    "no_authority_created",
    "no_repository_access_performed",
    "no_claim_lease_reservation_or_launch",
    "no_write_or_external_effect",
    "agent_behavior_not_tested",
    "agent_behavior_reserved_for_stage4",
    "effect_absence_requires_independent_audit",
    "independent_review_required",
    "release_finding_remains_unresolved",
    "no_mutation",
)

TOP_LEVEL_FIELDS = {
    "schema_version",
    "observation_id",
    "attempt_series_id",
    "sequence_index",
    "observation_attempt",
    "expected_observation_count",
    "stage",
    "operation",
    "created_at",
    "producer",
    "stage2_entry_evidence",
    "contract_transition",
    "scenario",
    "planning_projection",
    "compatibility",
    "exclusion_probes",
    "effect_counters",
    "evidence_boundary",
    "assertions",
    "verdict",
    "stage3_observation_complete",
    "independent_review",
    "finding_resolution_claimed",
    "stage_advancement_claimed",
    "live_ready_claimed",
    "no_mutation",
    "blockers",
    "release_findings",
    "digest",
}

PROBE_INPUTS = [
    {
        "probe_id": "missing_compatibility_evidence",
        "evidence_complete": False,
        "repository_in_synthetic_scope": True,
        "dependency_cycle": False,
        "shared_write_paths": [],
        "shared_contract_surfaces": [],
        "protected_surfaces": [],
        "external_effects": [],
    },
    {
        "probe_id": "unlisted_repository",
        "evidence_complete": True,
        "repository_in_synthetic_scope": False,
        "dependency_cycle": False,
        "shared_write_paths": [],
        "shared_contract_surfaces": [],
        "protected_surfaces": [],
        "external_effects": [],
    },
    {
        "probe_id": "dependency_cycle",
        "evidence_complete": True,
        "repository_in_synthetic_scope": True,
        "dependency_cycle": True,
        "shared_write_paths": [],
        "shared_contract_surfaces": [],
        "protected_surfaces": [],
        "external_effects": [],
    },
    {
        "probe_id": "overlapping_write_path",
        "evidence_complete": True,
        "repository_in_synthetic_scope": True,
        "dependency_cycle": False,
        "shared_write_paths": ["global/shared-output"],
        "shared_contract_surfaces": [],
        "protected_surfaces": [],
        "external_effects": [],
    },
    {
        "probe_id": "shared_contract_surface",
        "evidence_complete": True,
        "repository_in_synthetic_scope": True,
        "dependency_cycle": False,
        "shared_write_paths": [],
        "shared_contract_surfaces": ["global.schema.v1"],
        "protected_surfaces": [],
        "external_effects": [],
    },
    {
        "probe_id": "protected_surface",
        "evidence_complete": True,
        "repository_in_synthetic_scope": True,
        "dependency_cycle": False,
        "shared_write_paths": [],
        "shared_contract_surfaces": [],
        "protected_surfaces": ["parser_state"],
        "external_effects": [],
    },
    {
        "probe_id": "external_effect_required",
        "evidence_complete": True,
        "repository_in_synthetic_scope": True,
        "dependency_cycle": False,
        "shared_write_paths": [],
        "shared_contract_surfaces": [],
        "protected_surfaces": [],
        "external_effects": ["github_issue_write"],
    },
]

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


class DuplicateKeyError(ValueError):
    """Raised when strict JSON parsing observes a duplicate object key."""


class NonFiniteJSONConstantError(ValueError):
    """Raised when parsing encounters NaN or Infinity."""


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_nonfinite_constant(value: str) -> object:
    raise NonFiniteJSONConstantError(f"non-finite JSON constant: {value}")


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def canonical_self_digest(document: dict[str, object]) -> str:
    payload = dict(document)
    payload.pop("digest", None)
    return canonical_digest(payload)


def _skill_relative_path(path: Path) -> str | None:
    try:
        return path.relative_to(SKILL_ROOT).as_posix()
    except ValueError:
        return None


def _require_ordinary_non_reparse_successor(path: Path) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise ManifestTransitionError("successor path metadata is unavailable") from exc
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    file_attributes = getattr(metadata, "st_file_attributes", 0)
    if stat.S_ISLNK(metadata.st_mode) or file_attributes & reparse_flag:
        raise ManifestTransitionError("successor path is a reparse point")
    if not stat.S_ISREG(metadata.st_mode):
        raise ManifestTransitionError("successor path is not an ordinary file")


def _exact_successor_path(skill_relative_path: str) -> Path:
    expected = SKILL_ROOT / skill_relative_path
    try:
        representations = [
            path
            for path in expected.parent.iterdir()
            if path.name.casefold() == expected.name.casefold()
        ]
    except OSError as exc:
        raise ManifestTransitionError("successor path cannot be enumerated") from exc
    if len(representations) != 1:
        raise ManifestTransitionError(
            "successor path is missing or has duplicate representations"
        )
    successor = representations[0]
    if successor.name != expected.name:
        raise ManifestTransitionError("successor path casing does not match")
    _require_ordinary_non_reparse_successor(successor)
    return successor


def _manifest_row(path: Path) -> dict[str, str]:
    skill_relative = _skill_relative_path(path)
    if skill_relative is not None:
        relative = "mythic-edge-role-pool/" + skill_relative
    else:
        try:
            workflow_relative = path.relative_to(WORKFLOW_ROOT).as_posix()
        except ValueError as exc:
            raise ManifestTransitionError(
                "manifest path is outside the closed roots"
            ) from exc
        relative = "mythic-edge-workflow/" + workflow_relative
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise ManifestTransitionError("manifest file cannot be read") from exc
    return {"path": relative, "sha256": hashlib.sha256(payload).hexdigest()}


def current_skill_manifest() -> list[dict[str, str]]:
    pinned_paths = tuple(
        _exact_successor_path(relative_path)
        for relative_path in (
            SUCCESSOR_SKILL_RELATIVE_PATH,
            V4_SUCCESSOR_SKILL_RELATIVE_PATH,
            V5_SUCCESSOR_SKILL_RELATIVE_PATH,
            APP_SERVER_ADAPTER_SKILL_RELATIVE_PATH,
            APP_SERVER_ADAPTER_TEST_SKILL_RELATIVE_PATH,
            APP_NATIVE_ADAPTER_SKILL_RELATIVE_PATH,
            APP_NATIVE_ADAPTER_TEST_SKILL_RELATIVE_PATH,
        )
    )
    pinned_paths_casefolded = {
        SUCCESSOR_SKILL_RELATIVE_PATH.casefold(),
        V4_SUCCESSOR_SKILL_RELATIVE_PATH.casefold(),
        V5_SUCCESSOR_SKILL_RELATIVE_PATH.casefold(),
        APP_SERVER_ADAPTER_SKILL_RELATIVE_PATH.casefold(),
        APP_SERVER_ADAPTER_TEST_SKILL_RELATIVE_PATH.casefold(),
        APP_NATIVE_ADAPTER_SKILL_RELATIVE_PATH.casefold(),
        APP_NATIVE_ADAPTER_TEST_SKILL_RELATIVE_PATH.casefold(),
    }
    files: list[Path] = []
    for path in SKILL_ROOT.rglob("*", recurse_symlinks=False):
        relative = _skill_relative_path(path)
        if (
            relative is not None
            and relative.casefold() in pinned_paths_casefolded
        ):
            continue
        if (
            path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix.lower() not in {".pyc", ".pyo"}
        ):
            files.append(path)
    for pinned_path in pinned_paths:
        _require_ordinary_non_reparse_successor(pinned_path)
        files.append(pinned_path)
    files.extend(WORKFLOW_SNAPSHOT_FILES)
    return sorted((_manifest_row(path) for path in files), key=lambda row: row["path"])


def _manifest_state() -> tuple[
    list[dict[str, str]],
    dict[str, str],
    set[str],
    set[str],
    set[str],
    set[str],
]:
    rows = current_skill_manifest()
    current: dict[str, str] = {}
    duplicates: set[str] = set()
    casefolded_paths: dict[str, str] = {}
    for row in rows:
        path = row["path"]
        if path in current:
            duplicates.add(path)
        folded_path = path.casefold()
        if folded_path in casefolded_paths:
            duplicates.add(path)
            duplicates.add(casefolded_paths[folded_path])
        else:
            casefolded_paths[folded_path] = path
        current[path] = row["sha256"]
    baseline_paths = set(STAGE2_BASELINE_FILES)
    current_paths = set(current)
    added = current_paths - baseline_paths
    removed = baseline_paths - current_paths
    modified = {
        path
        for path in baseline_paths & current_paths
        if STAGE2_BASELINE_FILES[path] != current[path]
    }
    return rows, current, added, removed, modified, duplicates


def _validated_manifest_state() -> tuple[
    list[dict[str, str]], dict[str, str], set[str]
]:
    rows, current, added, removed, modified, duplicates = _manifest_state()
    if duplicates:
        raise ManifestTransitionError("duplicate manifest paths")
    if len(rows) != EXPECTED_CURRENT_MANIFEST_FILE_COUNT:
        raise ManifestTransitionError("current manifest file count is not 41")
    if added != ALLOWED_ADDED_PATHS:
        raise ManifestTransitionError("unexpected or missing added paths")
    if modified != ALLOWED_MODIFIED_PATHS:
        raise ManifestTransitionError("unexpected or missing modified paths")
    if removed:
        raise ManifestTransitionError("Stage-2 baseline paths were removed")
    manifest_paths = [row["path"] for row in rows]
    if manifest_paths != sorted(manifest_paths):
        raise ManifestTransitionError("manifest rows are not in ordinal path order")
    if current.get(SUCCESSOR_MANIFEST_PATH) != SUCCESSOR_SHA256:
        raise ManifestTransitionError("successor digest does not match the pinned digest")
    if current.get(V4_SUCCESSOR_MANIFEST_PATH) != V4_SUCCESSOR_SHA256:
        raise ManifestTransitionError(
            "v4 successor digest does not match the pinned digest"
        )
    if current.get(V5_SUCCESSOR_MANIFEST_PATH) != V5_SUCCESSOR_SHA256:
        raise ManifestTransitionError(
            "v5 successor digest does not match the pinned digest"
        )
    if (
        current.get(STAGE3_PLANNING_MANIFEST_PATH)
        != V5_REAL_SOURCE_ADAPTER_AMENDMENT_SHA256
    ):
        raise ManifestTransitionError(
            "v5 real-source-adapter amendment digest does not match"
        )
    for path in sorted(APP_SERVER_ADDED_PATHS):
        if current.get(path) != PINNED_SUCCESSOR_DIGESTS[path]:
            raise ManifestTransitionError(
                "app-server adapter digest does not match the reviewed digest"
            )
    for path in sorted(APP_NATIVE_ADDED_PATHS):
        if current.get(path) != PINNED_SUCCESSOR_DIGESTS[path]:
            raise ManifestTransitionError(
                "app-native adapter digest does not match the reviewed digest"
            )
    for path, digest in sorted(REVIEWED_APP_NATIVE_MODIFIED_DIGESTS.items()):
        if current.get(path) != digest:
            raise ManifestTransitionError(
                "reviewed app-native modified digest does not match"
            )
    plan_path = "mythic-edge-role-pool/scripts/check_pool_plan.py"
    if current.get(plan_path) == STAGE2_BASELINE_FILES[plan_path]:
        raise ManifestTransitionError(
            "production plan validator was not fail-closed"
        )
    return rows, current, removed


def expected_contract_transition() -> dict[str, object]:
    rows, current, removed = _validated_manifest_state()
    change_set: list[dict[str, object]] = []
    for path in sorted(ALLOWED_MODIFIED_PATHS):
        change_set.append(
            {
                "path": path,
                "change_kind": "modified",
                "before_sha256": STAGE2_BASELINE_FILES[path],
                "after_sha256": current.get(path),
            }
        )
    for path in sorted(ALLOWED_ADDED_PATHS):
        change_set.append(
            {
                "path": path,
                "change_kind": "added",
                "before_sha256": None,
                "after_sha256": PINNED_SUCCESSOR_DIGESTS.get(path, current.get(path)),
            }
        )
    return {
        "transition_kind": "explicit_additive_stage3_stage4_contract_upgrade",
        "entry_manifest_file_count": 30,
        "entry_manifest_digest": STAGE2_ENTRY_EVIDENCE["entry_manifest_digest"],
        "entry_manifest_canonical_length_bytes": 5070,
        "entry_manifest_canonical_sha256": STAGE2_ENTRY_EVIDENCE[
            "entry_manifest_canonical_sha256"
        ],
        "current_manifest_file_count": EXPECTED_CURRENT_MANIFEST_FILE_COUNT,
        "current_manifest_sha256": canonical_digest(rows),
        "change_set": sorted(change_set, key=lambda row: str(row["path"])),
        "removed_paths": sorted(removed),
        "production_plan_validator_path": (
            "mythic-edge-role-pool/scripts/check_pool_plan.py"
        ),
        "production_plan_validator_sha256": current.get(
            "mythic-edge-role-pool/scripts/check_pool_plan.py"
        ),
        "production_plan_validator_unchanged": False,
        "stage2_evidence_historical_immutable": True,
        "stage2_revalidated_under_current_manifest": False,
        "entry_snapshot_equals_current_snapshot": False,
        "authority_expansion": False,
    }


def expected_planning_projection() -> dict[str, object]:
    lane_ids = [str(lane["lane_id"]) for lane in SYNTHETIC_LANES]
    return {
        "mode": "synthetic_parallel_compatibility_assessment",
        "projection_only": True,
        "candidate_lane_ids": lane_ids,
        "modeled_compatible_lane_ids": lane_ids,
        "selected_for_dispatch_lane_ids": [],
        "claim_count": 0,
        "lease_count": 0,
        "reservation_count": 0,
        "launch_count": 0,
        "v3_plan_emitted": False,
        "live_transition_authorized": False,
        "live_block_reason": "stage3_synthetic_zero_effect_contract",
        "validator_process_is_not_a_pooled_agent_launch": True,
    }


def derive_compatibility(scenario: object) -> dict[str, object] | None:
    if not isinstance(scenario, dict) or not isinstance(scenario.get("lanes"), list):
        return None
    lanes = scenario["lanes"]
    if not all(isinstance(lane, dict) for lane in lanes):
        return None
    list_fields = (
        "dependencies",
        "modeled_write_paths",
        "global_contract_surfaces",
        "protected_surfaces",
        "external_state_ids",
        "invalidation_risks",
    )
    for lane in lanes:
        if not isinstance(lane.get("lane_id"), str) or not isinstance(
            lane.get("repository_id"), str
        ):
            return None
        for field in list_fields:
            value = lane.get(field)
            if not isinstance(value, list) or not all(
                isinstance(item, str) for item in value
            ):
                return None
    rows: list[dict[str, object]] = []
    for index, left in enumerate(lanes):
        for right in lanes[index + 1 :]:
            left_id = left.get("lane_id")
            right_id = right.get("lane_id")
            left_dependencies = set(left.get("dependencies", []))
            right_dependencies = set(right.get("dependencies", []))
            dependency_edges: list[str] = []
            if right_id in left_dependencies:
                dependency_edges.append(f"{left_id}->{right_id}")
            if left_id in right_dependencies:
                dependency_edges.append(f"{right_id}->{left_id}")
            shared_write_paths: list[str] = []
            if left.get("repository_id") == right.get("repository_id"):
                shared_write_paths = sorted(
                    set(left.get("modeled_write_paths", []))
                    & set(right.get("modeled_write_paths", []))
                )
            shared_contracts = sorted(
                set(left.get("global_contract_surfaces", []))
                & set(right.get("global_contract_surfaces", []))
            )
            protected = sorted(
                set(left.get("protected_surfaces", []))
                | set(right.get("protected_surfaces", []))
            )
            external_state = sorted(
                set(left.get("external_state_ids", []))
                | set(right.get("external_state_ids", []))
            )
            invalidation = sorted(
                set(left.get("invalidation_risks", []))
                | set(right.get("invalidation_risks", []))
            )
            risks = (
                dependency_edges
                + shared_write_paths
                + shared_contracts
                + protected
                + external_state
                + invalidation
            )
            rows.append(
                {
                    "left_lane_id": left_id,
                    "right_lane_id": right_id,
                    "dependency_edges": dependency_edges,
                    "shared_write_paths": shared_write_paths,
                    "shared_contract_surfaces": shared_contracts,
                    "protected_surfaces": protected,
                    "external_state": external_state,
                    "invalidation_risks": invalidation,
                    "verdict": (
                        "safe_to_run_concurrently"
                        if not risks
                        else "excluded_fail_closed"
                    ),
                }
            )
    return {
        "required_pair_count": 3,
        "observed_pair_count": len(rows),
        "all_pairs_covered": len(rows) == 3,
        "overall_verdict": (
            "safe_to_run_concurrently"
            if len(rows) == 3
            and all(row["verdict"] == "safe_to_run_concurrently" for row in rows)
            else "excluded_fail_closed"
        ),
        "rows": rows,
    }


def classify_exclusion_probe(probe: dict[str, object]) -> tuple[str, str, str]:
    if probe.get("evidence_complete") is not True:
        return (
            "excluded_fail_closed",
            "dependency_write_scope_protected_surface_or_integration_order_unknown",
            "missing_compatibility_evidence",
        )
    if probe.get("repository_in_synthetic_scope") is not True:
        return (
            "excluded_fail_closed",
            "repository_access_or_no_echo_authority_missing",
            "unlisted_repository",
        )
    if probe.get("dependency_cycle") is True:
        return (
            "excluded_fail_closed",
            "dependency_write_scope_protected_surface_or_integration_order_unknown",
            "dependency_cycle",
        )
    if probe.get("shared_write_paths"):
        return (
            "excluded_fail_closed",
            "dependency_write_scope_protected_surface_or_integration_order_unknown",
            "overlapping_write_path",
        )
    if probe.get("shared_contract_surfaces"):
        return (
            "excluded_fail_closed",
            "dependency_write_scope_protected_surface_or_integration_order_unknown",
            "shared_contract_surface",
        )
    if probe.get("protected_surfaces"):
        return (
            "excluded_fail_closed",
            "dependency_write_scope_protected_surface_or_integration_order_unknown",
            "protected_surface",
        )
    if probe.get("external_effects"):
        return (
            "excluded_fail_closed",
            "unexpected_write_scope_expansion_secret_exposure_or_external_effect",
            "external_effect_required",
        )
    return "eligible", "none", "none"


def expected_exclusion_probes() -> list[dict[str, object]]:
    probes: list[dict[str, object]] = []
    for item in PROBE_INPUTS:
        probe = copy.deepcopy(item)
        result, fallback, reason = classify_exclusion_probe(probe)
        probe["observed_result"] = result
        probe["fallback_condition"] = fallback
        probe["reason_code"] = reason
        probes.append(probe)
    return probes


def build_stage3_observation(
    observation_id: str,
    attempt_series_id: str,
    observation_attempt: str,
    sequence_index: int,
    created_at: str,
) -> dict[str, object]:
    scenario = copy.deepcopy(EXPECTED_SCENARIO)
    document: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "observation_id": observation_id,
        "attempt_series_id": attempt_series_id,
        "sequence_index": sequence_index,
        "observation_attempt": observation_attempt,
        "expected_observation_count": EXPECTED_OBSERVATION_COUNT,
        "stage": STAGE,
        "operation": OPERATION,
        "created_at": created_at,
        "producer": PRODUCER,
        "stage2_entry_evidence": copy.deepcopy(STAGE2_ENTRY_EVIDENCE),
        "contract_transition": expected_contract_transition(),
        "scenario": scenario,
        "planning_projection": expected_planning_projection(),
        "compatibility": derive_compatibility(scenario),
        "exclusion_probes": expected_exclusion_probes(),
        "effect_counters": {field: 0 for field in EFFECT_COUNTER_FIELDS},
        "evidence_boundary": {
            "evidence_class": "deterministic_structure_and_derivation",
            "effect_counters_are_assertions": True,
            "checker_exit_zero_proves_runtime_effect_absence": False,
            "offline_release_gate_required": True,
            "validator_command_transcript_required": True,
            "before_after_persistent_projection_required": True,
            "independent_operation_audit_required": True,
            "independent_review_must_verify_zero_effects": True,
        },
        "assertions": {field: True for field in ASSERTION_FIELDS},
        "verdict": "complete",
        "stage3_observation_complete": True,
        "independent_review": {
            "required": True,
            "status": "pending",
            "required_attempts": ["1_of_2", "2_of_2"],
            "pair_acceptance_separate_from_stage_advancement": True,
            "agent_behavior_review_in_scope": False,
        },
        "finding_resolution_claimed": False,
        "stage_advancement_claimed": False,
        "live_ready_claimed": False,
        "no_mutation": True,
        "blockers": [],
        "release_findings": [
            {
                "finding_id": FINDING_ID,
                "status": "unresolved",
                "resolution_claimed": False,
            }
        ],
    }
    document["digest"] = canonical_self_digest(document)
    return document


def _check_keys(
    value: object,
    expected: set[str],
    errors: list[str],
    context: str,
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{context}: must be an object")
        return None
    missing = sorted(expected - value.keys())
    unknown = sorted(value.keys() - expected)
    if missing:
        errors.append(f"{context}: missing fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"{context}: unknown fields: {', '.join(unknown)}")
    return value


def _require_exact(
    value: object,
    expected: object,
    errors: list[str],
    context: str,
) -> None:
    try:
        equal = canonical_bytes(value) == canonical_bytes(expected)
    except (TypeError, ValueError):
        equal = False
    if not equal:
        errors.append(f"{context}: does not match the Stage-3 contract")


def _validate_created_at(value: object, errors: list[str]) -> None:
    if not isinstance(value, str) or not TIMESTAMP_RE.fullmatch(value):
        errors.append("created_at: must use whole-second UTC Z form")
        return
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        errors.append("created_at: must be a valid UTC timestamp")


def _validate_current_transition(
    errors: list[str],
) -> dict[str, object] | None:
    try:
        return expected_contract_transition()
    except ManifestTransitionError as exc:
        errors.append(f"contract_transition: {exc}")
        return None


def validate_stage3_behavioral_planning(document: object) -> list[str]:
    errors: list[str] = []
    root = _check_keys(document, TOP_LEVEL_FIELDS, errors, "observation")
    if root is None:
        return errors

    _require_exact(root.get("schema_version"), SCHEMA_VERSION, errors, "schema_version")
    observation_id = root.get("observation_id")
    if not isinstance(observation_id, str) or not UUID_RE.fullmatch(observation_id):
        errors.append("observation_id: must be a lowercase UUID")
    attempt_series_id = root.get("attempt_series_id")
    if (
        not isinstance(attempt_series_id, str)
        or not UUID_RE.fullmatch(attempt_series_id)
    ):
        errors.append("attempt_series_id: must be a lowercase UUID")
    elif attempt_series_id == STAGE2_ATTEMPT_SERIES_ID:
        errors.append("attempt_series_id: must be fresh for Stage 3")
    if observation_id == attempt_series_id:
        errors.append("observation_id: must be distinct from attempt_series_id")
    attempt = root.get("observation_attempt")
    if attempt not in {"1_of_2", "2_of_2"}:
        errors.append("observation_attempt: must be '1_of_2' or '2_of_2'")
    expected_sequence = {"1_of_2": 1, "2_of_2": 2}.get(attempt)
    sequence_index = root.get("sequence_index")
    if type(sequence_index) is not int or sequence_index != expected_sequence:
        errors.append("sequence_index: must match observation_attempt")
    _require_exact(
        root.get("expected_observation_count"),
        EXPECTED_OBSERVATION_COUNT,
        errors,
        "expected_observation_count",
    )
    _require_exact(root.get("stage"), STAGE, errors, "stage")
    _require_exact(root.get("operation"), OPERATION, errors, "operation")
    _require_exact(root.get("producer"), PRODUCER, errors, "producer")
    _validate_created_at(root.get("created_at"), errors)

    _require_exact(
        root.get("stage2_entry_evidence"),
        STAGE2_ENTRY_EVIDENCE,
        errors,
        "stage2_entry_evidence",
    )
    expected_transition = _validate_current_transition(errors)
    if expected_transition is not None:
        _require_exact(
            root.get("contract_transition"),
            expected_transition,
            errors,
            "contract_transition",
        )
    _require_exact(root.get("scenario"), EXPECTED_SCENARIO, errors, "scenario")

    _require_exact(
        root.get("planning_projection"),
        expected_planning_projection(),
        errors,
        "planning_projection",
    )
    derived_compatibility = derive_compatibility(root.get("scenario"))
    if derived_compatibility is None:
        errors.append("compatibility: scenario lanes cannot be derived")
    else:
        _require_exact(
            root.get("compatibility"),
            derived_compatibility,
            errors,
            "compatibility",
        )
        if derived_compatibility.get("overall_verdict") != (
            "safe_to_run_concurrently"
        ):
            errors.append("compatibility: positive scenario must be concurrency-safe")
        if derived_compatibility.get("observed_pair_count") != 3:
            errors.append("compatibility: exactly three pair rows are required")

    probes = root.get("exclusion_probes")
    _require_exact(probes, expected_exclusion_probes(), errors, "exclusion_probes")
    if isinstance(probes, list):
        for index, probe in enumerate(probes):
            if not isinstance(probe, dict):
                errors.append(f"exclusion_probes[{index}]: must be an object")
                continue
            result, fallback, reason = classify_exclusion_probe(probe)
            if probe.get("observed_result") != result:
                errors.append(f"exclusion_probes[{index}]: result is not derived")
            if probe.get("fallback_condition") != fallback:
                errors.append(f"exclusion_probes[{index}]: fallback is not derived")
            if probe.get("reason_code") != reason:
                errors.append(f"exclusion_probes[{index}]: reason is not derived")
            if result != "excluded_fail_closed":
                errors.append(f"exclusion_probes[{index}]: must fail closed")

    _require_exact(
        root.get("effect_counters"),
        {field: 0 for field in EFFECT_COUNTER_FIELDS},
        errors,
        "effect_counters",
    )
    _require_exact(
        root.get("evidence_boundary"),
        {
            "evidence_class": "deterministic_structure_and_derivation",
            "effect_counters_are_assertions": True,
            "checker_exit_zero_proves_runtime_effect_absence": False,
            "offline_release_gate_required": True,
            "validator_command_transcript_required": True,
            "before_after_persistent_projection_required": True,
            "independent_operation_audit_required": True,
            "independent_review_must_verify_zero_effects": True,
        },
        errors,
        "evidence_boundary",
    )
    _require_exact(
        root.get("assertions"),
        {field: True for field in ASSERTION_FIELDS},
        errors,
        "assertions",
    )
    exact_values = {
        "verdict": "complete",
        "stage3_observation_complete": True,
        "independent_review": {
            "required": True,
            "status": "pending",
            "required_attempts": ["1_of_2", "2_of_2"],
            "pair_acceptance_separate_from_stage_advancement": True,
            "agent_behavior_review_in_scope": False,
        },
        "finding_resolution_claimed": False,
        "stage_advancement_claimed": False,
        "live_ready_claimed": False,
        "no_mutation": True,
        "blockers": [],
        "release_findings": [
            {
                "finding_id": FINDING_ID,
                "status": "unresolved",
                "resolution_claimed": False,
            }
        ],
    }
    for field, expected in exact_values.items():
        _require_exact(root.get(field), expected, errors, field)

    digest = root.get("digest")
    if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
        errors.append("digest: must be a lowercase SHA-256 digest")
    elif digest != canonical_self_digest(root):
        errors.append("digest: does not match the canonical observation")
    return errors


def validate_stage3_pair(first: object, second: object) -> list[str]:
    """Validate that two passing observations are ready for independent review."""

    errors: list[str] = []
    for label, document in (("first", first), ("second", second)):
        for error in validate_stage3_behavioral_planning(document):
            errors.append(f"{label}: {error}")
    if not isinstance(first, dict) or not isinstance(second, dict):
        return errors

    if first.get("observation_attempt") != "1_of_2":
        errors.append("pair: first observation must be 1_of_2")
    if second.get("observation_attempt") != "2_of_2":
        errors.append("pair: second observation must be 2_of_2")
    if (
        type(first.get("sequence_index")) is not int
        or type(second.get("sequence_index")) is not int
        or first.get("sequence_index") != 1
        or second.get("sequence_index") != 2
    ):
        errors.append("pair: sequence indexes must be 1 then 2")
    if first.get("attempt_series_id") != second.get("attempt_series_id"):
        errors.append("pair: attempt_series_id must match")
    if first.get("observation_id") == second.get("observation_id"):
        errors.append("pair: observation IDs must be distinct")
    if first.get("digest") == second.get("digest"):
        errors.append("pair: observation digests must be distinct")

    variable_fields = {
        "observation_id",
        "observation_attempt",
        "sequence_index",
        "created_at",
        "digest",
    }
    first_stable = {
        key: value for key, value in first.items() if key not in variable_fields
    }
    second_stable = {
        key: value for key, value in second.items() if key not in variable_fields
    }
    try:
        stable_equal = canonical_bytes(first_stable) == canonical_bytes(second_stable)
    except (TypeError, ValueError):
        stable_equal = False
    if not stable_equal:
        errors.append("pair: stable evidence and scenario bindings must be identical")

    try:
        first_time = datetime.strptime(
            str(first.get("created_at")), "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=timezone.utc)
        second_time = datetime.strptime(
            str(second.get("created_at")), "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=timezone.utc)
        if second_time <= first_time:
            errors.append("pair: second observation must be later than first")
    except ValueError:
        # Individual validation already emits the precise timestamp error.
        pass
    return errors


def _load_document(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(
            handle,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_nonfinite_constant,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate one zero-effect Stage-3 synthetic behavioral-planning "
            "observation. Validation performs no repository access or launch."
        )
    )
    parser.add_argument("document", type=Path)
    parser.add_argument(
        "--pair-with",
        type=Path,
        help=(
            "Validate document as 1_of_2 with this 2_of_2 observation. "
            "Success means review-ready, not independently accepted."
        ),
    )
    args = parser.parse_args(argv)
    try:
        document = _load_document(args.document)
    except DuplicateKeyError as exc:
        print(f"stage3 behavioral planning invalid: {exc}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError, NonFiniteJSONConstantError):
        print(
            "stage3 behavioral planning invalid: unable to read strict JSON document",
            file=sys.stderr,
        )
        return 2
    if args.pair_with is not None:
        try:
            second_document = _load_document(args.pair_with)
        except DuplicateKeyError as exc:
            print(f"stage3 behavioral planning invalid: {exc}", file=sys.stderr)
            return 2
        except (OSError, json.JSONDecodeError, NonFiniteJSONConstantError):
            print(
                "stage3 behavioral planning invalid: unable to read strict pair document",
                file=sys.stderr,
            )
            return 2
        errors = validate_stage3_pair(document, second_document)
    else:
        errors = validate_stage3_behavioral_planning(document)
    if errors:
        print("stage3 behavioral planning invalid:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if args.pair_with is not None:
        print(
            "stage3 behavioral planning pair review-ready: "
            f"schema={SCHEMA_VERSION}; independent_review=pending"
        )
    else:
        print(f"stage3 behavioral planning valid: schema={SCHEMA_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
