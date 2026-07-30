from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import check_stage3_behavioral_planning as stage3
from check_pool_plan import validate_plan
from check_stage3_behavioral_planning import (
    ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT,
    ALLOWED_ADDED_PATHS,
    ALLOWED_MODIFIED_PATHS,
    APP_SERVER_ADAPTER_MANIFEST_PATH,
    APP_SERVER_ADAPTER_SHA256,
    APP_SERVER_ADAPTER_SKILL_RELATIVE_PATH,
    APP_SERVER_ADAPTER_TEST_MANIFEST_PATH,
    APP_SERVER_ADAPTER_TEST_SHA256,
    APP_SERVER_ADAPTER_TEST_SKILL_RELATIVE_PATH,
    APP_SERVER_ADDED_PATHS,
    ASSERTION_FIELDS,
    EFFECT_COUNTER_FIELDS,
    EXPECTED_SCENARIO,
    FINDING_ID,
    PINNED_SUCCESSOR_DIGESTS,
    PRE_APP_SERVER_ALLOWED_ADDED_PATHS,
    PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS,
    REVIEWED_APP_SERVER_MODIFIED_DIGESTS,
    SCHEMA_VERSION,
    STAGE2_BASELINE_FILES,
    STAGE2_ENTRY_EVIDENCE,
    STAGE3_PLANNING_MANIFEST_PATH,
    SUCCESSOR_MANIFEST_PATH,
    SUCCESSOR_SHA256,
    V5_BUILD_RECONCILIATION_PREDECESSOR_STATIC_PREFLIGHT_SHA256,
    V5_BUILD_RECONCILIATION_REVIEW_EVIDENCE_SHA256,
    V5_BUILD_RECONCILIATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256,
    V5_CHARACTERIZATION_ENVELOPE_AMENDMENT_SHA256,
    V5_CHARACTERIZATION_ENVELOPE_REVIEW_EVIDENCE_SHA256,
    V5_CHARACTERIZATION_ADAPTER_SYNTHETIC_MATRIX_SHA256,
    V5_CHARACTERIZATION_PREDECESSOR_STATIC_PREFLIGHT_SHA256,
    V5_CHARACTERIZATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256,
    V5_CHARACTERIZATION_SYNTHETIC_MATRIX_SHA256,
    V5_CURRENT_RECIPE_PREDECESSOR_STATIC_PREFLIGHT_SHA256,
    V5_CURRENT_RECIPE_RECEIPT_BINDING_AMENDMENT_SHA256,
    V5_CURRENT_RECIPE_REVIEW_REF,
    V5_CURRENT_RECIPE_REVIEW_SHA256,
    V5_CURRENT_RECIPE_SHA256,
    V5_CURRENT_RECIPE_SUCCESSOR_STATIC_PREFLIGHT_SHA256,
    V5_REAL_SOURCE_ADAPTER_AMENDMENT_SHA256,
    V5_REAL_SOURCE_ADAPTER_PREDECESSOR_STATIC_PREFLIGHT_SHA256,
    V5_REAL_SOURCE_ADAPTER_REVIEW_EVIDENCE_SHA256,
    V5_REAL_SOURCE_ADAPTER_SUCCESSOR_STATIC_PREFLIGHT_SHA256,
    V4_SUCCESSOR_MANIFEST_PATH,
    V4_SUCCESSOR_SHA256,
    V5_SUCCESSOR_MANIFEST_PATH,
    V5_SUCCESSOR_SHA256,
    build_stage3_observation,
    canonical_bytes,
    canonical_self_digest,
    classify_exclusion_probe,
    current_skill_manifest,
    derive_compatibility,
    expected_contract_transition,
    expected_exclusion_probes,
    validate_stage3_pair,
    validate_stage3_behavioral_planning,
)


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER = SKILL_ROOT / "scripts" / "check_stage3_behavioral_planning.py"
ATTEMPT_SERIES_ID = "44444444-4444-4444-8444-444444444444"
LEGACY_ALLOWED_ADDED_PATHS = {
    "mythic-edge-role-pool/references/external-isolation-broker.md",
    "mythic-edge-role-pool/references/stage3-behavioral-planning.md",
    "mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py",
    "mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py",
}
LEGACY_ALLOWED_MODIFIED_PATHS = {
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
V5_REBIND_AMENDMENT = SKILL_ROOT / "references" / "stage3-behavioral-planning.md"
V5_REBIND_CONTRACT = (
    SKILL_ROOT
    / "references"
    / "external-isolation-broker-v5-corrective-successor.md"
)
V5_REBIND_AMENDMENT_SHA256 = (
    "93d0ee2ea0f3b8f9223411588cf23a3e55d20a5bfe1a869efe0ed8254cb66aee"
)
V5_REBIND_PREDECESSOR_SHA256 = (
    "0b3cc179303ddba6ece29492414b7bb942f25cc5d59d317f6c6857c93375a1ea"
)
V5_REBIND_TARGET_SHA256 = (
    "d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967"
)
V5_REBIND_RECIPE_SHA256 = (
    "4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3"
)
V5_REBIND_REVIEW_REF = "build_recipe_review_v1_ec08ac6d109ec6aab653a6b4976309a7"
V5_REBIND_RECEIPT_DIGEST = (
    "323ca61d9742da1030b4282c50a88ce9acc9417f73241dd5ba042ac49fa604cf"
)
V5_REBIND_FALSE_RECEIPT_FIELDS = {
    "build_recipe_execution_compatibility_claimed",
    "canary_authorized",
    "correctness_claimed",
    "handoff_creation_authorized",
    "historical_v4_command_tuple_verified",
    "implementation_authorized",
    "installation_authorized",
    "inventory_creation_authorized",
    "live_ready",
    "manifest_rebind_authorized",
    "package_build_authorized",
    "package_creation_authorized",
    "privacy_assurance_claimed",
    "production_readiness_claimed",
    "publication_authorized",
    "ready_for_codex_c",
    "ready_for_codex_d",
    "ready_for_codex_f",
    "release_readiness_claimed",
    "security_assurance_claimed",
    "separate_review_receipt_file_claimed",
    "service_mutation_authorized",
    "stage_advancement_authorized",
}
V5_REBIND_RECEIPT_VALUES = {
    "build_recipe_independent_review_status": (
        "accepted_exact_recipe_and_contract"
    ),
    "build_recipe_ref": "mythic_edge_role_pool_v5_build_recipe.v1",
    "build_recipe_schema": "mythic_edge_role_pool_v5_build_recipe.v1",
    "build_recipe_sha256": V5_REBIND_RECIPE_SHA256,
    "contract_review_verdict": "accepted",
    "next_role": "owner_manifest_rebind_decision",
    "receipt_digest": V5_REBIND_RECEIPT_DIGEST,
    "receipt_storage": "transcript_only",
    "recipe_definition_verdict": "conformant",
    "review_receipt_kind": "build_recipe_contract_review",
    "review_receipt_schema": (
        "mythic_edge_role_pool_v5_build_recipe_independent_review_receipt.v1"
    ),
    "review_ref": V5_REBIND_REVIEW_REF,
    "reviewed_at_utc": "2026-07-16T16:50:59Z",
    "reviewed_contract_id": (
        "mythic_edge_role_pool_external_isolation_broker_v5_corrective_successor.v1"
    ),
    "reviewed_contract_path": (
        "references/external-isolation-broker-v5-corrective-successor.md"
    ),
    "reviewed_contract_sha256": V5_REBIND_TARGET_SHA256,
    "reviewer_role": "codex_e_independent_reviewer",
}
V5_REBIND_RECEIPT_KEYS = (
    V5_REBIND_FALSE_RECEIPT_FIELDS
    | set(V5_REBIND_RECEIPT_VALUES)
    | {"finding_ids"}
)
V5_REBIND_V2_AMENDMENT_SHA256 = (
    "2186d19e752c5973497aa3506bd5b9f4ff4b20f014655b2a78bd7e67424b9dbd"
)
V5_REBIND_V2_PREDECESSOR_SHA256 = V5_REBIND_TARGET_SHA256
V5_REBIND_V2_TARGET_SHA256 = (
    "85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704"
)
V5_REBIND_V2_REVIEW_REF = (
    "build_recipe_review_v1_5dd95cd9042f9ba5be885675f8fab52d"
)
V5_REBIND_V2_RECEIPT_DIGEST = (
    "9e074c23202ecdb0f0f7d1ff8ef7c391d5e555e14897620793d84b53af3ec6ab"
)
V5_REBIND_V2_RECEIPT_VALUES = {
    **V5_REBIND_RECEIPT_VALUES,
    "receipt_digest": V5_REBIND_V2_RECEIPT_DIGEST,
    "review_ref": V5_REBIND_V2_REVIEW_REF,
    "reviewed_at_utc": "2026-07-16T21:03:30Z",
    "reviewed_contract_sha256": V5_REBIND_V2_TARGET_SHA256,
}
V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS = {
    "timestamp_floor_matrix_counts_sha256": (
        "94374945d2619fe9c7251f78f80884560b839e7b6421d3bbfa246b1c56efb792"
    ),
    "failure_matrix_counts_sha256": (
        "2212582e3af79e7c1b125d55623de2ac757912c068e3957c688aa7a78f90e2ef"
    ),
    "projection_matrix_counts_sha256": (
        "8c12cca36ce236c55264afe1b70fb464a59e9594cb976d9e2e8178c50f8bca06"
    ),
    "parent_edit_envelope_sha256": (
        "f9b27efa62cc6b7f8d6f69dbb85ba7c335daebb452eb09afe0229488768d9fa1"
    ),
    "candidate_edit_envelope_sha256": (
        "32694f48845e22fcf597b5b1b32600c905e3af0478d3ac2ef2993684a44aebed"
    ),
    "candidate_operation_matrix_sha256": (
        "f822d52edaaf32a0d8cf84288ba741d2856bcd3d56adc621e071ebd5b343552d"
    ),
    "future_activation_requirements_sha256": (
        "a22fb76fee01c5c30ada6858458632ede488e1e960ef2dbdf15a656abbd18dd1"
    ),
    "static_preflight_sha256": (
        "c15f4b6899d28628dfb7649d65147407ce640f7a1d910143ba286b5a33b22b35"
    ),
}
V5_REBIND_V2_FUTURE_ACTIVATION_REQUIREMENTS = {
    "requirements": [
        "owner_activation_ref|string|derive_from_exact_private_owner_approval_bytes",
        "owner_activation_sha256|string|sha256_exact_private_owner_approval_bytes",
        "owner_activation_status|string|literal:approved_unconsumed",
        "activation_expiry_utc|string|rfc3339_utc_whole_seconds_from_owner_approval",
        "activation_single_use|boolean|literal:true",
        (
            "contract_id|string|literal:"
            "mythic_edge_role_pool_external_isolation_broker_v5_corrective_successor.v1"
        ),
        (
            "contract_path|string|literal:references/"
            "external-isolation-broker-v5-corrective-successor.md"
        ),
        "contract_sha256|string|sha256_reviewed_contract_bytes",
        (
            "parent_contract_id|string|literal:"
            "mythic_edge_role_pool_external_isolation_broker_v4_corrective_successor.v1"
        ),
        "parent_contract_sha256|string|sha256_reviewed_parent_contract_bytes",
        (
            "accepted_candidate_revision_ordinal|integer|"
            "copy_from_accepted_candidate_review_receipt"
        ),
        (
            "accepted_candidate_revision_digest|string|"
            "recompute_from_accepted_candidate_packet"
        ),
        (
            "accepted_candidate_packet_sha256|string|"
            "sha256_accepted_candidate_packet_bytes"
        ),
        (
            "independent_candidate_review_receipt_schema|string|literal:"
            "mythic_edge_role_pool_v5_candidate_independent_review_receipt.v1"
        ),
        (
            "independent_candidate_review_ref|string|"
            "derive_from_accepted_review_receipt"
        ),
        (
            "independent_candidate_review_receipt_digest|string|"
            "recompute_from_accepted_review_receipt"
        ),
        (
            "independent_candidate_review_file_sha256|string|"
            "sha256_accepted_review_receipt_file_bytes"
        ),
        "manifest_file_count|integer|literal:37",
        (
            "manifest_v5_path|string|literal:references/"
            "external-isolation-broker-v5-corrective-successor.md"
        ),
        (
            "manifest_rebind_from_sha256|string|literal:"
            "d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967"
        ),
        "manifest_rebind_to_sha256|string|equal:contract_sha256",
        (
            "manifest_rebind_amendment_path|string|"
            "copy_from_accepted_manifest_amendment"
        ),
        (
            "manifest_rebind_amendment_sha256|string|"
            "sha256_accepted_manifest_amendment_bytes"
        ),
        "manifest_rebind_status|string|literal:accepted_implemented_current",
        (
            "candidate_edit_envelope_sha256|string|"
            "sha256_canonical_candidate_edit_envelope"
        ),
        (
            "candidate_operation_profile|string|literal:"
            "mythic_edge_role_pool_v5_candidate_operation_authority.v1"
        ),
        (
            "candidate_operation_matrix_sha256|string|"
            "sha256_canonical_candidate_operation_matrix"
        ),
        "candidate_operation_matrix_expected_pair_count|integer|literal:64",
        "candidate_operation_matrix_accepted_pair_count|integer|literal:26",
        "candidate_operation_matrix_rejected_pair_count|integer|literal:38",
        (
            "implementation_sha256|string|"
            "sha256_accepted_candidate_implementation_bytes"
        ),
        "test_sha256|string|sha256_accepted_candidate_test_bytes",
        (
            "unchanged_source_rows_root_digest|string|"
            "recompute_from_accepted_candidate_unchanged_rows"
        ),
        (
            "build_recipe_schema|string|literal:"
            "mythic_edge_role_pool_v5_build_recipe.v1"
        ),
        (
            "build_recipe_ref|string|literal:"
            "mythic_edge_role_pool_v5_build_recipe.v1"
        ),
        "build_recipe_sha256|string|sha256_canonical_accepted_build_recipe",
        "build_recipe_status|string|literal:complete",
        (
            "build_recipe_independent_review_ref|string|"
            "copy_from_accepted_recipe_review_receipt"
        ),
        (
            "build_recipe_independent_review_sha256|string|"
            "recompute_from_accepted_recipe_review_receipt"
        ),
        (
            "build_recipe_independent_review_status|string|literal:"
            "accepted_exact_recipe_and_contract"
        ),
        (
            "package_authority_profile|string|literal:"
            "mythic_edge_role_pool_external_isolation_broker_package_authority.v5"
        ),
        (
            "package_id|string|literal:"
            "mythic_edge_role_pool_windows_broker_verifier_preparation.v5"
        ),
        (
            "package_directory_name|string|literal:"
            "MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v5"
        ),
        (
            "inventory_schema|string|literal:"
            "mythic_edge_role_pool_windows_broker_verifier_package_inventory.v5"
        ),
        (
            "handoff_schema|string|literal:"
            "mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v5"
        ),
        (
            "publication_failure_schema|string|literal:"
            "mythic_edge_role_pool_package_publication_failure.v3"
        ),
        "package_creation_authorized|boolean|literal:true",
        "source_copy_authorized|boolean|literal:true",
        "local_source_copy_authorized|boolean|literal:true",
        "package_build_authorized|boolean|literal:true",
        "local_build_authorized|boolean|literal:true",
        "package_self_tests_authorized|boolean|literal:true",
        "inventory_creation_authorized|boolean|literal:true",
        "handoff_creation_authorized|boolean|literal:true",
        "handoff_publication_authorized|boolean|literal:true",
        "failure_artifact_creation_authorized|boolean|literal:true",
        "installation_authorized|boolean|literal:false",
        "service_mutation_authorized|boolean|literal:false",
        "canary_authorized|boolean|literal:false",
        "stage_advancement_authorized|boolean|literal:false",
        "external_mutation_authorized|boolean|literal:false",
        "live_ready|boolean|literal:false",
        "current_v4_reuse_authorized|boolean|literal:false",
        "correctness_claimed|boolean|literal:false",
        "security_assurance_claimed|boolean|literal:false",
        "privacy_assurance_claimed|boolean|literal:false",
        "release_readiness_claimed|boolean|literal:false",
        "production_readiness_claimed|boolean|literal:false",
    ],
    "schema": "mythic_edge_role_pool_v5_future_activation_requirements.v1",
}
V5_REBIND_V2_STATIC_PREFLIGHT_VECTOR = {
    "candidate_edit_envelope_sha256": (
        "32694f48845e22fcf597b5b1b32600c905e3af0478d3ac2ef2993684a44aebed"
    ),
    "candidate_operation_matrix_accepted_pair_count": 26,
    "candidate_operation_matrix_expected_pair_count": 64,
    "candidate_operation_matrix_rejected_pair_count": 38,
    "candidate_operation_matrix_sha256": (
        "f822d52edaaf32a0d8cf84288ba741d2856bcd3d56adc621e071ebd5b343552d"
    ),
    "candidate_operation_profile": (
        "mythic_edge_role_pool_v5_candidate_operation_authority.v1"
    ),
    "contract_path": "references/external-isolation-broker-v5-corrective-successor.md",
    "contract_sha256": "a" * 64,
    "failure_matrix_counts_sha256": (
        "2212582e3af79e7c1b125d55623de2ac757912c068e3957c688aa7a78f90e2ef"
    ),
    "future_activation_requirements_sha256": (
        "a22fb76fee01c5c30ada6858458632ede488e1e960ef2dbdf15a656abbd18dd1"
    ),
    "manifest_file_count": 37,
    "manifest_rebind_amendment_path": "references/stage3-behavioral-planning.md",
    "manifest_rebind_amendment_sha256": "b" * 64,
    "manifest_rebind_from_sha256": V5_REBIND_V2_PREDECESSOR_SHA256,
    "manifest_rebind_status": "accepted_implemented_current",
    "manifest_rebind_to_sha256": "a" * 64,
    "manifest_v5_path": (
        "references/external-isolation-broker-v5-corrective-successor.md"
    ),
    "parent_contract_path": (
        "references/external-isolation-broker-v4-corrective-successor.md"
    ),
    "parent_contract_sha256": (
        "628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487"
    ),
    "parent_edit_envelope_sha256": (
        "f9b27efa62cc6b7f8d6f69dbb85ba7c335daebb452eb09afe0229488768d9fa1"
    ),
    "projection_matrix_counts_sha256": (
        "8c12cca36ce236c55264afe1b70fb464a59e9594cb976d9e2e8178c50f8bca06"
    ),
    "static_preflight_schema": (
        "mythic_edge_role_pool_v5_static_contract_preflight.v1"
    ),
    "static_preflight_sha256": (
        "c15f4b6899d28628dfb7649d65147407ce640f7a1d910143ba286b5a33b22b35"
    ),
    "timestamp_floor_matrix_counts_sha256": (
        "94374945d2619fe9c7251f78f80884560b839e7b6421d3bbfa246b1c56efb792"
    ),
}
V5_REBIND_V3_AMENDMENT_SHA256 = (
    "eb1ddd76d10924f51b6a087fe413b24b5c00ffcb4117f31f7fe100f296519018"
)
V5_REBIND_V3_PREDECESSOR_SHA256 = V5_REBIND_V2_TARGET_SHA256
V5_REBIND_V3_TARGET_SHA256 = (
    "db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6"
)
V5_REBIND_V3_REVIEW_EVIDENCE_SHA256 = (
    "8fbd16905c63f57bc6c8320673c93b39d0c46777da853411d8695f237868ea8c"
)
V5_REBIND_V3_ORACLE_TUPLE_COUNT = 768
V5_REBIND_V3_ORACLE_OUTCOME_COUNTS = [1, 1, 45, 4, 717]
V5_REBIND_V3_ORACLE_SHA256 = (
    "19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269"
)
V5_REBIND_V3_REVIEW_EVIDENCE_VALUES = {
    "contract_review_status": "accepted_semantics_manifest_pending",
    "contract_verdict": "accepted_within_approved_scope",
    "edits_performed": False,
    "finding_id": "EIB-PKG-V5-ATOMIC-E-001",
    "finding_status": "fixed_confirmed",
    "implementation_performed": False,
    "installation_performed": False,
    "live_ready": False,
    "manifest_integration_complete": False,
    "manifest_rebind_authorized": False,
    "manifest_rebind_may_be_considered_next": True,
    "next_role": "owner_manifest_rebind_decision_then_codex_b_exact_37_to_37_amendment",
    "oracle_outcome_counts": V5_REBIND_V3_ORACLE_OUTCOME_COUNTS,
    "oracle_sha256": V5_REBIND_V3_ORACLE_SHA256,
    "oracle_tuple_count": V5_REBIND_V3_ORACLE_TUPLE_COUNT,
    "package_operations_performed": False,
    "review_evidence_schema": (
        "mythic_edge_role_pool_v5_finite_oracle_contract_confirmation.v1"
    ),
    "reviewer_role": "codex_e_independent_reviewer",
    "scope_classification": "contract_defect_within_baseline",
    "semantic_review_completed": True,
    "service_or_canary_performed": False,
    "source_sha256": V5_REBIND_V3_TARGET_SHA256,
    "stage_advancement_authorized": False,
}
V5_REBIND_V4_AMENDMENT_SHA256 = (
    V5_CURRENT_RECIPE_RECEIPT_BINDING_AMENDMENT_SHA256
)
V5_REBIND_V4_REVIEW_REF = V5_CURRENT_RECIPE_REVIEW_REF
V5_REBIND_V4_RECEIPT_DIGEST = V5_CURRENT_RECIPE_REVIEW_SHA256
V5_REBIND_V4_RECEIPT_VALUES = {
    **V5_REBIND_RECEIPT_VALUES,
    "receipt_digest": V5_REBIND_V4_RECEIPT_DIGEST,
    "review_ref": V5_REBIND_V4_REVIEW_REF,
    "reviewed_at_utc": "2026-07-17T01:41:59Z",
    "reviewed_contract_sha256": V5_REBIND_V3_TARGET_SHA256,
}
V5_REBIND_V4_FUTURE_ACTIVATION_REQUIREMENTS_SHA256 = (
    "a955b153f34f5dd861662b95ee9a1fa52b523ad666855004ec924d371b9b0bd2"
)
V5_REBIND_V4_FALSE_AUTHORITY_FIELDS = (
    "activation_consumption_authorized",
    "activation_creation_authorized",
    "candidate_preparation_authorized",
    "canary_authorized",
    "correctness_claimed",
    "external_write_authorized",
    "handoff_creation_authorized",
    "installation_authorized",
    "inventory_creation_authorized",
    "live_ready",
    "package_build_authorized",
    "privacy_assurance_claimed",
    "production_readiness_claimed",
    "publication_authorized",
    "ready_for_codex_c",
    "ready_for_codex_d",
    "ready_for_codex_f",
    "release_readiness_claimed",
    "security_assurance_claimed",
    "service_mutation_authorized",
    "source_copy_authorized",
    "stage_advancement_authorized",
)
V5_REBIND_V5_AMENDMENT_SHA256 = (
    "e2742a64463940bd47e29cfc160c6792dc10822e9df3a8e1e04565bf5758ba6d"
)
V5_REBIND_V5_PREDECESSOR_SHA256 = V5_REBIND_V3_TARGET_SHA256
V5_REBIND_V5_TARGET_SHA256 = (
    "8b8d5f1631f8d546ee7c477a7bf626f6d73f4f460827a92550e7712f3cfe35b7"
)
V5_REBIND_V5_PINNED_SUCCESSOR_DIGESTS = {
    **PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS,
    V5_SUCCESSOR_MANIFEST_PATH: V5_REBIND_V5_TARGET_SHA256,
}
V5_REBIND_V5_REVIEW_EVIDENCE_SHA256 = (
    V5_BUILD_RECONCILIATION_REVIEW_EVIDENCE_SHA256
)
V5_REBIND_V5_REVIEW_EVIDENCE_VALUES = {
    "build_environment_root_cause": "unknown",
    "canary_authorized": False,
    "characterization_status": "defined_read_only_but_unauthorized",
    "consumed_activation_reusable": False,
    "edit_envelope_status": "exact_two_paths_preserved",
    "edits_performed": False,
    "finding_ids": [],
    "generated_residue_count": 0,
    "implementation_authorized": False,
    "installation_authorized": False,
    "live_ready": False,
    "manifest_file_count": 37,
    "manifest_rebind_authorized": False,
    "manifest_status": "stale_digest_37_to_37_rebind_required",
    "next_recommended_role": (
        "owner_manifest_rebind_decision_then_codex_b_exact_37_to_37_amendment"
    ),
    "offline_gate_error_count": 54,
    "offline_gate_failure_count": 1,
    "offline_gate_root_cause": "stale_digest_only",
    "offline_gate_test_count": 338,
    "package_build_authorized": False,
    "package_creation_authorized": False,
    "protected_surface_forbidden_count": 0,
    "protected_surface_warning_count": 0,
    "receipt_storage": "transcript_only",
    "recipe_v1_status": "immutable_retired_future_execution_blocked",
    "review_evidence_schema": (
        "mythic_edge_role_pool_v5_build_reconciliation_contract_review.v1"
    ),
    "reviewer_role": "codex_e_independent_reviewer",
    "secret_private_marker_lexical_false_positive_count": 1,
    "secret_private_marker_sensitive_material_exposed": False,
    "service_mutation_authorized": False,
    "source_artifact": (
        "references/external-isolation-broker-v5-corrective-successor.md"
    ),
    "source_read_authorized": False,
    "source_sha256": V5_REBIND_V5_TARGET_SHA256,
    "source_stable_during_review": True,
    "stage_advancement_authorized": False,
    "structural_validation_passed": True,
    "unfrozen_attempt_reusable": False,
    "verdict": "accepted_semantics_manifest_pending",
}
V5_REBIND_V5_FALSE_AUTHORITY_FIELDS = (
    "activation_consumption_authorized",
    "activation_creation_authorized",
    "build_recipe_v1_future_execution_authorized",
    "candidate_preparation_authorized",
    "canary_authorized",
    "characterization_authorized",
    "correctness_claimed",
    "external_write_authorized",
    "handoff_creation_authorized",
    "installation_authorized",
    "inventory_creation_authorized",
    "live_ready",
    "package_build_authorized",
    "package_creation_authorized",
    "privacy_assurance_claimed",
    "production_readiness_claimed",
    "publication_authorized",
    "ready_for_codex_c",
    "ready_for_codex_d",
    "ready_for_codex_f",
    "release_readiness_claimed",
    "security_assurance_claimed",
    "service_mutation_authorized",
    "source_read_authorized",
    "stage_advancement_authorized",
)
V5_REBIND_V6_AMENDMENT_SHA256 = V5_CHARACTERIZATION_ENVELOPE_AMENDMENT_SHA256
V5_REBIND_V6_PREDECESSOR_SHA256 = V5_REBIND_V5_TARGET_SHA256
V5_REBIND_V6_TARGET_SHA256 = (
    "48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be"
)
V5_REBIND_V6_PINNED_SUCCESSOR_DIGESTS = {
    **PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS,
    V5_SUCCESSOR_MANIFEST_PATH: V5_REBIND_V6_TARGET_SHA256,
}
V5_REBIND_V6_REVIEW_EVIDENCE_SHA256 = (
    V5_CHARACTERIZATION_ENVELOPE_REVIEW_EVIDENCE_SHA256
)
V5_REBIND_V6_SYNTHETIC_MATRIX_SHA256 = (
    V5_CHARACTERIZATION_SYNTHETIC_MATRIX_SHA256
)
V5_REBIND_V6_REVIEW_EVIDENCE_VALUES = {
    "canary_authorized": False,
    "characterization_authorized": False,
    "contract_artifact": (
        "references/external-isolation-broker-v5-corrective-successor.md"
    ),
    "contract_sha256": V5_REBIND_V6_TARGET_SHA256,
    "contract_status": (
        "characterization_execution_envelope_review_and_manifest_rebind_blocked"
    ),
    "finding_status": {
        "EIB-PKG-V5-CHAR-E-001": "fixed_confirmed",
        "EIB-PKG-V5-CHAR-E-002": "fixed_confirmed",
        "EIB-PKG-V5-CHAR-E-003": "fixed_confirmed",
    },
    "implementation_authorized": False,
    "installation_authorized": False,
    "live_ready": False,
    "manifest_rebind_authorized": False,
    "manifest_rebind_may_be_considered_next": True,
    "next_recommended_role": (
        "Codex B: narrow 37-to-37 manifest-rebind amendment writer"
    ),
    "package_operations_authorized": False,
    "retry_activation_key_count": 54,
    "role_performed": "Codex E: Independent V5 Characterization Contract Re-reviewer",
    "service_mutation_authorized": False,
    "source_read_authorized": False,
    "stage_advancement_authorized": False,
    "synthetic_case_count": 36,
    "synthetic_matrix_sha256": V5_REBIND_V6_SYNTHETIC_MATRIX_SHA256,
    "synthetic_review_receipt_key_count": 16,
    "validation": {
        "generated_residue_count": 0,
        "offline_gate": (
            "342 tests; expected 52 errors and 1 failure from stale manifest "
            "digest only"
        ),
        "structural_validation": "passed",
    },
}
V5_REBIND_V6_FALSE_AUTHORITY_FIELDS = (
    "activation_consumption_authorized",
    "activation_creation_authorized",
    "candidate_preparation_authorized",
    "canary_authorized",
    "characterization_authorized",
    "correctness_claimed",
    "external_write_authorized",
    "handoff_creation_authorized",
    "implementation_authorized",
    "installation_authorized",
    "inventory_creation_authorized",
    "live_ready",
    "manifest_rebind_authorized",
    "package_build_authorized",
    "package_creation_authorized",
    "privacy_assurance_claimed",
    "production_readiness_claimed",
    "publication_authorized",
    "ready_for_codex_c",
    "ready_for_codex_d",
    "ready_for_codex_f",
    "release_readiness_claimed",
    "security_assurance_claimed",
    "service_mutation_authorized",
    "source_read_authorized",
    "stage_advancement_authorized",
)
V5_REBIND_V7_AMENDMENT_SHA256 = V5_REAL_SOURCE_ADAPTER_AMENDMENT_SHA256
V5_REBIND_V7_PREDECESSOR_SHA256 = V5_REBIND_V6_TARGET_SHA256
V5_REBIND_V7_TARGET_SHA256 = V5_SUCCESSOR_SHA256
V5_REBIND_V7_REVIEW_EVIDENCE_SHA256 = (
    V5_REAL_SOURCE_ADAPTER_REVIEW_EVIDENCE_SHA256
)
V5_REBIND_V7_CORE_MATRIX_SHA256 = V5_CHARACTERIZATION_SYNTHETIC_MATRIX_SHA256
V5_REBIND_V7_ADAPTER_MATRIX_SHA256 = (
    V5_CHARACTERIZATION_ADAPTER_SYNTHETIC_MATRIX_SHA256
)
V5_REBIND_V7_REVIEW_EVIDENCE_VALUES = {
    "activation_creation_authorized": False,
    "adapter_matrix": "37 unique cases; digest matched",
    "contract_sha256": V5_REBIND_V7_TARGET_SHA256,
    "contract_verdict": "accepted_semantics_manifest_rebind_required",
    "exhaustive_outer_oracle": "15360 tuples; all counts matched",
    "finding_status": {"EIB-PKG-V5-ADAPTER-E-001": "fixed_confirmed"},
    "generated_residue_count": 0,
    "implementation_authorized": False,
    "live_ready": False,
    "manifest_rebind_authorized": False,
    "manifest_rebind_eligible": True,
    "next_recommended_role": (
        "Codex B: narrow 37-to-37 manifest-rebind amendment writer, after "
        "exact owner approval"
    ),
    "offline_gate": "346 tests; 52 errors and 1 failure from stale v5 digest only",
    "package_operations_authorized": False,
    "role_performed": "Codex E: Independent V5 Real-Source Adapter Contract Re-reviewer",
    "source_access_authorized": False,
    "stage_advancement_authorized": False,
}
V5_REBIND_V7_FALSE_AUTHORITY_FIELDS = (
    "activation_consumption_authorized",
    "activation_creation_authorized",
    "candidate_preparation_authorized",
    "canary_authorized",
    "characterization_authorized",
    "correctness_claimed",
    "external_write_authorized",
    "handoff_creation_authorized",
    "implementation_authorized",
    "installation_authorized",
    "inventory_creation_authorized",
    "live_ready",
    "manifest_rebind_authorized",
    "package_build_authorized",
    "package_creation_authorized",
    "privacy_assurance_claimed",
    "production_readiness_claimed",
    "publication_authorized",
    "ready_for_codex_c",
    "ready_for_codex_d",
    "ready_for_codex_f",
    "release_readiness_claimed",
    "security_assurance_claimed",
    "service_mutation_authorized",
    "source_access_authorized",
    "source_read_authorized",
    "stage_advancement_authorized",
)
V5_REBIND_V7_OUTER_DIMENSIONS = (
    ("prevalidation_status", ("passed", "failed")),
    (
        "controller_start_status",
        ("not_invoked", "failed", "started", "unknown"),
    ),
    (
        "controller_exit_status",
        ("not_applicable", "zero", "nonzero", "unknown"),
    ),
    (
        "controller_stdout_status",
        (
            "not_applicable",
            "one_canonical_result",
            "empty",
            "malformed",
            "extra_or_overflow",
            "unknown",
        ),
    ),
    (
        "controller_stderr_status",
        ("not_applicable", "empty", "nonempty_or_overflow", "unknown"),
    ),
    (
        "controller_cleanup_status",
        ("not_applicable", "zero", "nonzero", "unknown"),
    ),
    (
        "result_candidate_status",
        (
            "not_present",
            "valid_complete",
            "valid_degraded",
            "valid_blocked",
            "invalid_or_incoherent",
        ),
    ),
)
V5_REBIND_V7_HANDOFF_COUNTS = {
    "accepted_complete": 1,
    "accepted_degraded": 1,
    "accepted_blocked": 1,
    "blocked_before_controller_start": 2,
    "blocked_after_controller_start": 157,
    "cleanup_state_unknown": 15198,
}
V5_REBIND_V7_OUTER_FAILURE_COUNTS = {
    "none": 3,
    "binding_failed_before_controller_start": 1,
    "controller_start_failed": 1,
    "controller_exit_nonzero": 5,
    "controller_stdout_empty": 10,
    "controller_stdout_malformed": 10,
    "controller_stdout_extra_or_overflow": 10,
    "controller_stderr_nonempty_or_overflow": 40,
    "controller_residue_detected": 80,
    "accepted_result_cross_field_mismatch": 2,
    "controller_state_unknown": 15198,
}


def _canonical_json_bytes(document: object) -> bytes:
    return (
        json.dumps(
            document,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _strict_json_value(payload: bytes) -> object:
    text = payload.decode("utf-8", errors="strict")

    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
        document: dict[str, object] = {}
        for key, value in pairs:
            if key in document:
                raise ValueError("duplicate receipt key")
            document[key] = value
        return document

    return json.loads(text, object_pairs_hook=reject_duplicate_keys)


def _strict_json_object(payload: bytes) -> dict[str, object]:
    document = _strict_json_value(payload)
    if not isinstance(document, dict):
        raise ValueError("receipt must be an object")
    return document


def _embedded_v5_rebind_receipt_for_contract(contract_sha256: str) -> bytes:
    prefix = '{"build_recipe_execution_compatibility_claimed"'
    matches = [
        line
        for line in V5_REBIND_AMENDMENT.read_text(encoding="utf-8").splitlines()
        if line.startswith(prefix)
        and _strict_json_object((line + "\n").encode("utf-8"))[
            "reviewed_contract_sha256"
        ]
        == contract_sha256
    ]
    if len(matches) != 1:
        raise ValueError("expected one embedded receipt for the contract")
    return (matches[0] + "\n").encode("utf-8")


def _embedded_v5_rebind_receipt() -> bytes:
    return _embedded_v5_rebind_receipt_for_contract(V5_REBIND_TARGET_SHA256)


def _embedded_v5_rebind_v2_receipt() -> bytes:
    return _embedded_v5_rebind_receipt_for_contract(V5_REBIND_V2_TARGET_SHA256)


def _embedded_v5_rebind_v4_receipt() -> bytes:
    return _embedded_v5_rebind_receipt_for_contract(V5_REBIND_V3_TARGET_SHA256)


def _validate_v5_rebind_receipt_values(
    payload: bytes, expected_values: dict[str, object]
) -> dict[str, object]:
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n") or b"\r" in payload:
        raise ValueError("receipt must end in exactly one LF")
    document = _strict_json_object(payload)
    if set(document) != V5_REBIND_RECEIPT_KEYS or len(document) != 41:
        raise ValueError("receipt key set is not exact")
    if payload != _canonical_json_bytes(document):
        raise ValueError("receipt bytes are not canonical")
    if document["finding_ids"] != []:
        raise ValueError("accepted receipt must have no findings")
    if any(document[field] is not False for field in V5_REBIND_FALSE_RECEIPT_FIELDS):
        raise ValueError("receipt authority and claim fields must be false")
    if any(document[field] != value for field, value in expected_values.items()):
        raise ValueError("receipt field binding does not match")

    reference_preimage = {
        key: value
        for key, value in document.items()
        if key not in {"review_ref", "receipt_digest"}
    }
    derived_reference = "build_recipe_review_v1_" + hashlib.sha256(
        _canonical_json_bytes(reference_preimage)
    ).hexdigest()[:32]
    if derived_reference != expected_values["review_ref"]:
        raise ValueError("review reference does not recompute")

    receipt_preimage = {
        key: value for key, value in document.items() if key != "receipt_digest"
    }
    derived_receipt_digest = hashlib.sha256(
        _canonical_json_bytes(receipt_preimage)
    ).hexdigest()
    if derived_receipt_digest != expected_values["receipt_digest"]:
        raise ValueError("receipt digest does not recompute")
    return document


def _validate_v5_rebind_receipt(payload: bytes) -> dict[str, object]:
    return _validate_v5_rebind_receipt_values(payload, V5_REBIND_RECEIPT_VALUES)


def _validate_v5_rebind_v2_receipt(payload: bytes) -> dict[str, object]:
    return _validate_v5_rebind_receipt_values(
        payload, V5_REBIND_V2_RECEIPT_VALUES
    )


def _validate_v5_rebind_v4_receipt(payload: bytes) -> dict[str, object]:
    return _validate_v5_rebind_receipt_values(
        payload, V5_REBIND_V4_RECEIPT_VALUES
    )


def _v5_rebind_binding(receipt: dict[str, object]) -> dict[str, object]:
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v1"
        ),
        "amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "contract_path": V5_SUCCESSOR_MANIFEST_PATH,
        "contract_sha256": V5_REBIND_TARGET_SHA256,
        "recipe_schema": receipt["build_recipe_schema"],
        "recipe_sha256": receipt["build_recipe_sha256"],
        "review_ref": receipt["review_ref"],
        "review_receipt_digest": receipt["receipt_digest"],
        "predecessor_sha256": V5_REBIND_PREDECESSOR_SHA256,
        "target_sha256": V5_REBIND_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "stage2_change_set_kind": "added_preserved",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT,
        "path_set_change": "none",
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "v3_sha256": SUCCESSOR_SHA256,
        "v4_sha256": V4_SUCCESSOR_SHA256,
    }


def _expected_v5_rebind_binding() -> dict[str, object]:
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v1"
        ),
        "amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "contract_path": (
            "mythic-edge-role-pool/references/"
            "external-isolation-broker-v5-corrective-successor.md"
        ),
        "contract_sha256": V5_REBIND_TARGET_SHA256,
        "recipe_schema": "mythic_edge_role_pool_v5_build_recipe.v1",
        "recipe_sha256": V5_REBIND_RECIPE_SHA256,
        "review_ref": V5_REBIND_REVIEW_REF,
        "review_receipt_digest": V5_REBIND_RECEIPT_DIGEST,
        "predecessor_sha256": V5_REBIND_PREDECESSOR_SHA256,
        "target_sha256": V5_REBIND_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "stage2_change_set_kind": "added_preserved",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": 37,
        "path_set_change": "none",
        "allowed_added_paths": tuple(
            sorted(
                LEGACY_ALLOWED_ADDED_PATHS
                | {
                    SUCCESSOR_MANIFEST_PATH,
                    V4_SUCCESSOR_MANIFEST_PATH,
                    V5_SUCCESSOR_MANIFEST_PATH,
                }
            )
        ),
        "allowed_modified_paths": tuple(sorted(LEGACY_ALLOWED_MODIFIED_PATHS)),
        "v3_sha256": (
            "44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55"
        ),
        "v4_sha256": (
            "628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487"
        ),
    }


def _validate_v5_rebind_binding(binding: dict[str, object]) -> None:
    if binding != _expected_v5_rebind_binding():
        raise ValueError("v5 manifest-rebind binding drift")


def _json_sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _drift_value(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return "drift"
    if isinstance(value, list):
        return [*value, "drift"]
    if isinstance(value, tuple):
        return (*value, "drift")
    if isinstance(value, dict):
        return {**value, "unknown": "drift"}
    raise TypeError("unsupported synthetic drift value")


def _document_json_values(path: Path) -> list[tuple[bytes, object]]:
    document = path.read_text(encoding="utf-8")
    values: list[tuple[bytes, object]] = []
    for match in re.finditer(r"```json\r?\n(.*?)\r?\n```", document, re.DOTALL):
        payload = (match.group(1) + "\n").encode("utf-8")
        try:
            value = _strict_json_value(payload)
        except json.JSONDecodeError:
            continue
        values.append((payload, value))
    return values


def _contract_json_values() -> list[tuple[bytes, object]]:
    return _document_json_values(V5_REBIND_CONTRACT)


def _amendment_json_values() -> list[tuple[bytes, object]]:
    return _document_json_values(V5_REBIND_AMENDMENT)


def _v5_candidate_operation_matrix() -> dict[str, object]:
    operations = [
        "read_parent_inventory_metadata",
        "read_parent_source_rows",
        "read_prior_candidate_revision",
        "read_prior_independent_review_receipt",
        "create_candidate_staging_root",
        "copy_candidate_source_rows",
        "edit_candidate_implementation_path",
        "edit_candidate_test_path",
        "execute_bound_build_recipe",
        "execute_bound_candidate_tests",
        "create_candidate_disposable_outputs",
        "create_candidate_preflight_packet",
        "create_candidate_review_root",
        "read_frozen_candidate_for_review",
        "create_independent_review_receipt",
        "cleanup_exact_candidate_staging_root",
    ]
    rows = [
        {
            "actor": "codex_c_candidate_preparer",
            "revision_ordinals": [0],
            "predecessor": (
                "candidate_workflow_activation_consumed_revision_zero_roots_absent"
            ),
            "allowed_operations": [
                operations[index]
                for index in (0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15)
            ],
        },
        {
            "actor": "codex_d_bounded_candidate_fixer",
            "revision_ordinals": [1, 2],
            "predecessor": (
                "prior_e_bounded_correction_receipt_unexpired_ordinal_available"
            ),
            "allowed_operations": [
                operations[index]
                for index in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15)
            ],
        },
        {
            "actor": "codex_e_independent_reviewer",
            "revision_ordinals": [0, 1, 2],
            "predecessor": "frozen_candidate_review_pending_activation_unexpired",
            "allowed_operations": [operations[13], operations[14]],
        },
        {
            "actor": "final_seal_actor_without_activation",
            "revision_ordinals": [0, 1, 2],
            "predecessor": "accepted_e_receipt_without_final_seal_activation",
            "allowed_operations": [],
        },
    ]
    return {
        "accepted_pair_count": 26,
        "expected_pair_count": 64,
        "matrix_schema": "mythic_edge_role_pool_v5_candidate_operation_matrix.v1",
        "operation_vocabulary": operations,
        "profile": "mythic_edge_role_pool_v5_candidate_operation_authority.v1",
        "rejected_pair_count": 38,
        "rows": rows,
    }


def _validate_v5_matrix_counts(matrix: dict[str, object]) -> None:
    if set(matrix) != {
        "accepted_tuple_count",
        "dimensions",
        "expected_tuple_count",
        "matrix_id",
        "rejected_tuple_count",
        "schema",
    }:
        raise ValueError("matrix-count key drift")
    dimensions = matrix["dimensions"]
    if not isinstance(dimensions, list):
        raise ValueError("matrix dimensions must be an array")
    cardinalities: list[int] = []
    for dimension in dimensions:
        if not isinstance(dimension, dict) or set(dimension) != {
            "cardinality",
            "name",
            "values",
        }:
            raise ValueError("matrix dimension shape drift")
        values = dimension["values"]
        cardinality = dimension["cardinality"]
        if (
            type(cardinality) is not int
            or not isinstance(values, list)
            or cardinality != len(values)
            or len(values) != len(set(values))
        ):
            raise ValueError("matrix dimension cardinality drift")
        cardinalities.append(cardinality)
    expected = matrix["expected_tuple_count"]
    accepted = matrix["accepted_tuple_count"]
    rejected = matrix["rejected_tuple_count"]
    if (
        type(expected) is not int
        or type(accepted) is not int
        or type(rejected) is not int
        or math.prod(cardinalities) != expected
        or accepted + rejected != expected
    ):
        raise ValueError("matrix-count total drift")


def _validate_v5_rebind_v2_static_vectors() -> dict[str, str]:
    values = _contract_json_values()
    matrix_digests = {
        "timestamp_floor": "timestamp_floor_matrix_counts_sha256",
        "failure": "failure_matrix_counts_sha256",
        "binding_projection": "projection_matrix_counts_sha256",
    }
    observed: dict[str, str] = {}
    for matrix_id, digest_name in matrix_digests.items():
        matches = [
            (payload, value)
            for payload, value in values
            if isinstance(value, dict) and value.get("matrix_id") == matrix_id
        ]
        if len(matches) != 1:
            raise ValueError("matrix-count vector is missing or duplicated")
        payload, matrix = matches[0]
        if payload != _canonical_json_bytes(matrix):
            raise ValueError("matrix-count vector is not canonical")
        _validate_v5_matrix_counts(matrix)
        observed[digest_name] = _json_sha256(matrix)

    parent_envelopes = [
        (payload, value)
        for payload, value in values
        if isinstance(value, list)
        and len(value) == 4
        and "client/windows_broker_client.py" in value
    ]
    candidate_envelopes = [
        (payload, value)
        for payload, value in values
        if value
        == [
            "tests/test_implementation_handoff.py",
            "tools/publish_implementation_candidate.py",
        ]
    ]
    if len(parent_envelopes) != 1 or len(candidate_envelopes) != 1:
        raise ValueError("edit-envelope vector is missing or duplicated")
    parent_payload, parent_envelope = parent_envelopes[0]
    candidate_payload, candidate_envelope = candidate_envelopes[0]
    if (
        parent_payload != _canonical_json_bytes(parent_envelope)
        or candidate_payload != _canonical_json_bytes(candidate_envelope)
        or parent_envelope != sorted(parent_envelope)
        or candidate_envelope != sorted(candidate_envelope)
        or not set(candidate_envelope) < set(parent_envelope)
    ):
        raise ValueError("edit-envelope relationship drift")
    observed["parent_edit_envelope_sha256"] = _json_sha256(parent_envelope)
    observed["candidate_edit_envelope_sha256"] = _json_sha256(
        candidate_envelope
    )

    future_matches = [
        value
        for _, value in values
        if isinstance(value, dict)
        and value.get("schema")
        == "mythic_edge_role_pool_v5_future_activation_requirements.v1"
    ]
    if future_matches:
        raise ValueError(
            "legacy future-activation vector must not be adopted from current bytes"
        )
    future_requirements = copy.deepcopy(
        V5_REBIND_V2_FUTURE_ACTIVATION_REQUIREMENTS
    )
    requirements = future_requirements["requirements"]
    if (
        not isinstance(requirements, list)
        or len(requirements) != 68
        or len(requirements) != len(set(requirements))
    ):
        raise ValueError("future-activation requirements drift")
    observed["future_activation_requirements_sha256"] = _json_sha256(
        future_requirements
    )

    operation_matrix = _v5_candidate_operation_matrix()
    operations = operation_matrix["operation_vocabulary"]
    rows = operation_matrix["rows"]
    if not isinstance(operations, list) or not isinstance(rows, list):
        raise ValueError("candidate-operation matrix shape drift")
    actors = [row["actor"] for row in rows]
    pairs = list(itertools.product(actors, operations))
    accepted_pairs = {
        (row["actor"], operation)
        for row in rows
        for operation in row["allowed_operations"]
    }
    if (
        len(operations) != 16
        or len(operations) != len(set(operations))
        or len(actors) != 4
        or len(actors) != len(set(actors))
        or len(pairs) != operation_matrix["expected_pair_count"]
        or len(accepted_pairs) != operation_matrix["accepted_pair_count"]
        or len(pairs) - len(accepted_pairs)
        != operation_matrix["rejected_pair_count"]
    ):
        raise ValueError("candidate-operation matrix count drift")
    observed["candidate_operation_matrix_sha256"] = _json_sha256(
        operation_matrix
    )

    static_preflight = copy.deepcopy(V5_REBIND_V2_STATIC_PREFLIGHT_VECTOR)
    static_payload = _canonical_json_bytes(static_preflight)
    static_preimage = {
        key: value
        for key, value in static_preflight.items()
        if key != "static_preflight_sha256"
    }
    if (
        static_payload != _canonical_json_bytes(static_preflight)
        or len(static_preflight) != 24
        or static_preflight["contract_sha256"] != "a" * 64
        or static_preflight["manifest_rebind_to_sha256"] != "a" * 64
        or static_preflight["manifest_rebind_amendment_sha256"] != "b" * 64
    ):
        raise ValueError("static-preflight fixture drift")
    observed["static_preflight_sha256"] = _json_sha256(static_preimage)
    for digest_name, expected_digest in observed.items():
        if static_preflight.get(digest_name) not in {None, expected_digest}:
            raise ValueError("static-preflight cross-binding drift")
    if observed != V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS:
        raise ValueError("static-preflight digest drift")
    return observed


def _v5_rebind_v2_binding(receipt: dict[str, object]) -> dict[str, object]:
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v2"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v1"
        ),
        "predecessor_amendment_lifecycle_status": "complete",
        "amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V2_TARGET_SHA256,
        "predecessor_sha256": V5_REBIND_V2_PREDECESSOR_SHA256,
        "target_sha256": V5_REBIND_V2_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "stage2_change_set_kind": "added_preserved",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT,
        "path_set_change": "none",
        "recipe_schema": receipt["build_recipe_schema"],
        "recipe_sha256": receipt["build_recipe_sha256"],
        "review_ref": receipt["review_ref"],
        "review_receipt_digest": receipt["receipt_digest"],
        "reviewed_at_utc": receipt["reviewed_at_utc"],
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v1_predecessor_sha256": V5_REBIND_PREDECESSOR_SHA256,
        "v1_target_sha256": V5_REBIND_TARGET_SHA256,
        "v1_review_ref": V5_REBIND_REVIEW_REF,
        "v1_receipt_digest": V5_REBIND_RECEIPT_DIGEST,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "v3_sha256": SUCCESSOR_SHA256,
        "v4_sha256": V4_SUCCESSOR_SHA256,
        "static_preflight": _validate_v5_rebind_v2_static_vectors(),
    }


def _expected_v5_rebind_v2_binding() -> dict[str, object]:
    expected = _expected_v5_rebind_binding()
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v2"
        ),
        "predecessor_amendment_id": expected["amendment_id"],
        "predecessor_amendment_lifecycle_status": "complete",
        "amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V2_TARGET_SHA256,
        "predecessor_sha256": V5_REBIND_V2_PREDECESSOR_SHA256,
        "target_sha256": V5_REBIND_V2_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "stage2_change_set_kind": "added_preserved",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": 37,
        "path_set_change": "none",
        "recipe_schema": "mythic_edge_role_pool_v5_build_recipe.v1",
        "recipe_sha256": V5_REBIND_RECIPE_SHA256,
        "review_ref": V5_REBIND_V2_REVIEW_REF,
        "review_receipt_digest": V5_REBIND_V2_RECEIPT_DIGEST,
        "reviewed_at_utc": "2026-07-16T21:03:30Z",
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v1_predecessor_sha256": V5_REBIND_PREDECESSOR_SHA256,
        "v1_target_sha256": V5_REBIND_TARGET_SHA256,
        "v1_review_ref": V5_REBIND_REVIEW_REF,
        "v1_receipt_digest": V5_REBIND_RECEIPT_DIGEST,
        "allowed_added_paths": expected["allowed_added_paths"],
        "allowed_modified_paths": expected["allowed_modified_paths"],
        "v3_sha256": expected["v3_sha256"],
        "v4_sha256": expected["v4_sha256"],
        "static_preflight": V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS,
    }


def _validate_v5_rebind_v2_binding(binding: dict[str, object]) -> None:
    if binding != _expected_v5_rebind_v2_binding():
        raise ValueError("v5 manifest-rebind v2 binding drift")


def _embedded_v5_rebind_v3_review_evidence() -> bytes:
    matches = [
        (payload, value)
        for payload, value in _amendment_json_values()
        if isinstance(value, dict)
        and value.get("review_evidence_schema")
        == "mythic_edge_role_pool_v5_finite_oracle_contract_confirmation.v1"
    ]
    if len(matches) != 1:
        raise ValueError("v3 review evidence is missing or duplicated")
    return matches[0][0]


def _validate_v5_rebind_v3_review_evidence(payload: bytes) -> dict[str, object]:
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n") or b"\r" in payload:
        raise ValueError("v3 review evidence must end in exactly one LF")
    document = _strict_json_object(payload)
    if payload != _canonical_json_bytes(document):
        raise ValueError("v3 review evidence is not canonical")
    if document != V5_REBIND_V3_REVIEW_EVIDENCE_VALUES:
        raise ValueError("v3 review evidence binding drift")
    if hashlib.sha256(payload).hexdigest() != V5_REBIND_V3_REVIEW_EVIDENCE_SHA256:
        raise ValueError("v3 review evidence digest drift")
    return document


def _v5_rebind_v3_binding(evidence: dict[str, object]) -> dict[str, object]:
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v3"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v2"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "predecessor_binding_preserved_as_history": True,
        "amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V3_TARGET_SHA256,
        "predecessor_sha256": V5_REBIND_V3_PREDECESSOR_SHA256,
        "target_sha256": V5_REBIND_V3_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "stage2_change_set_kind": "added_preserved",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT,
        "path_set_change": "none",
        "review_evidence_schema": evidence["review_evidence_schema"],
        "review_evidence_sha256": hashlib.sha256(
            _canonical_json_bytes(evidence)
        ).hexdigest(),
        "oracle_tuple_count": evidence["oracle_tuple_count"],
        "oracle_outcome_counts": tuple(evidence["oracle_outcome_counts"]),
        "oracle_sha256": evidence["oracle_sha256"],
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v1_predecessor_sha256": V5_REBIND_PREDECESSOR_SHA256,
        "v1_target_sha256": V5_REBIND_TARGET_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v2_predecessor_sha256": V5_REBIND_V2_PREDECESSOR_SHA256,
        "v2_target_sha256": V5_REBIND_V2_TARGET_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "v3_sha256": SUCCESSOR_SHA256,
        "v4_sha256": V4_SUCCESSOR_SHA256,
    }


def _expected_v5_rebind_v3_binding() -> dict[str, object]:
    expected_v2 = _expected_v5_rebind_v2_binding()
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v3"
        ),
        "predecessor_amendment_id": expected_v2["amendment_id"],
        "predecessor_manifest_binding_status": "implemented_current",
        "predecessor_binding_preserved_as_history": True,
        "amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V3_TARGET_SHA256,
        "predecessor_sha256": V5_REBIND_V3_PREDECESSOR_SHA256,
        "target_sha256": V5_REBIND_V3_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "stage2_change_set_kind": "added_preserved",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": 37,
        "path_set_change": "none",
        "review_evidence_schema": (
            "mythic_edge_role_pool_v5_finite_oracle_contract_confirmation.v1"
        ),
        "review_evidence_sha256": V5_REBIND_V3_REVIEW_EVIDENCE_SHA256,
        "oracle_tuple_count": V5_REBIND_V3_ORACLE_TUPLE_COUNT,
        "oracle_outcome_counts": tuple(V5_REBIND_V3_ORACLE_OUTCOME_COUNTS),
        "oracle_sha256": V5_REBIND_V3_ORACLE_SHA256,
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v1_predecessor_sha256": V5_REBIND_PREDECESSOR_SHA256,
        "v1_target_sha256": V5_REBIND_TARGET_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v2_predecessor_sha256": V5_REBIND_V2_PREDECESSOR_SHA256,
        "v2_target_sha256": V5_REBIND_V2_TARGET_SHA256,
        "allowed_added_paths": expected_v2["allowed_added_paths"],
        "allowed_modified_paths": expected_v2["allowed_modified_paths"],
        "v3_sha256": expected_v2["v3_sha256"],
        "v4_sha256": expected_v2["v4_sha256"],
    }


def _validate_v5_rebind_v3_binding(binding: dict[str, object]) -> None:
    if binding != _expected_v5_rebind_v3_binding():
        raise ValueError("v5 manifest-rebind v3 binding drift")


def _v5_rebind_v4_static_preflight(
    amendment_sha256: str,
) -> dict[str, object]:
    future_matches = [
        value
        for _, value in _contract_json_values()
        if isinstance(value, dict)
        and value.get("schema")
        == "mythic_edge_role_pool_v5_future_activation_requirements.v2"
    ]
    if len(future_matches) != 1:
        raise ValueError("current future-activation vector is missing or duplicated")
    future_requirements = future_matches[0]
    requirements = future_requirements.get("requirements")
    if (
        not isinstance(requirements, list)
        or len(requirements) != 75
        or len(requirements) != len(set(requirements))
        or _json_sha256(future_requirements)
        != V5_REBIND_V4_FUTURE_ACTIVATION_REQUIREMENTS_SHA256
    ):
        raise ValueError("current future-activation vector drift")

    preimage = {
        "atomic_observation_oracle_sha256": V5_REBIND_V3_ORACLE_SHA256,
        "candidate_edit_envelope_sha256": (
            "32694f48845e22fcf597b5b1b32600c905e3af0478d3ac2ef2993684a44aebed"
        ),
        "candidate_operation_matrix_accepted_pair_count": 26,
        "candidate_operation_matrix_expected_pair_count": 64,
        "candidate_operation_matrix_rejected_pair_count": 38,
        "candidate_operation_matrix_sha256": (
            "f822d52edaaf32a0d8cf84288ba741d2856bcd3d56adc621e071ebd5b343552d"
        ),
        "candidate_operation_profile": (
            "mythic_edge_role_pool_v5_candidate_operation_authority.v1"
        ),
        "contract_path": (
            "references/external-isolation-broker-v5-corrective-successor.md"
        ),
        "contract_sha256": V5_REBIND_V3_TARGET_SHA256,
        "failure_matrix_counts_sha256": (
            "2212582e3af79e7c1b125d55623de2ac757912c068e3957c688aa7a78f90e2ef"
        ),
        "future_activation_requirements_sha256": (
            V5_REBIND_V4_FUTURE_ACTIVATION_REQUIREMENTS_SHA256
        ),
        "manifest_file_count": 37,
        "manifest_rebind_amendment_path": (
            "references/stage3-behavioral-planning.md"
        ),
        "manifest_rebind_amendment_sha256": amendment_sha256,
        "manifest_rebind_from_sha256": V5_REBIND_V2_TARGET_SHA256,
        "manifest_rebind_status": "accepted_implemented_current",
        "manifest_rebind_to_sha256": V5_REBIND_V3_TARGET_SHA256,
        "manifest_v5_path": (
            "references/external-isolation-broker-v5-corrective-successor.md"
        ),
        "parent_contract_path": (
            "references/external-isolation-broker-v4-corrective-successor.md"
        ),
        "parent_contract_sha256": V4_SUCCESSOR_SHA256,
        "parent_edit_envelope_sha256": (
            "f9b27efa62cc6b7f8d6f69dbb85ba7c335daebb452eb09afe0229488768d9fa1"
        ),
        "projection_matrix_counts_sha256": (
            "8c12cca36ce236c55264afe1b70fb464a59e9594cb976d9e2e8178c50f8bca06"
        ),
        "static_preflight_schema": (
            "mythic_edge_role_pool_v5_static_contract_preflight.v1"
        ),
        "timestamp_floor_matrix_counts_sha256": (
            "94374945d2619fe9c7251f78f80884560b839e7b6421d3bbfa246b1c56efb792"
        ),
    }
    if len(preimage) != 24:
        raise ValueError("current static-preflight field-set drift")
    return {
        **preimage,
        "static_preflight_sha256": _json_sha256(preimage),
    }


def _v5_rebind_v4_binding(receipt: dict[str, object]) -> dict[str, object]:
    amendment_sha256 = V5_REBIND_V4_AMENDMENT_SHA256
    contract_sha256 = V5_REBIND_V3_TARGET_SHA256
    predecessor = _v5_rebind_v4_static_preflight(V5_REBIND_V3_AMENDMENT_SHA256)
    successor = _v5_rebind_v4_static_preflight(amendment_sha256)
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v4"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v3"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "amendment_sha256": amendment_sha256,
        "contract_sha256": contract_sha256,
        "transition_kind": "37_to_37_review_receipt_binding",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT,
        "path_set_change": "none",
        "v5_contract_sha256_before": V5_REBIND_V3_TARGET_SHA256,
        "v5_contract_sha256_after": V5_REBIND_V3_TARGET_SHA256,
        "v5_contract_digest_change": "none",
        "recipe_schema": receipt["build_recipe_schema"],
        "recipe_sha256": receipt["build_recipe_sha256"],
        "review_ref": receipt["review_ref"],
        "review_receipt_digest": receipt["receipt_digest"],
        "review_status": receipt["build_recipe_independent_review_status"],
        "reviewed_at_utc": receipt["reviewed_at_utc"],
        "receipt_storage": receipt["receipt_storage"],
        "receipt_key_count": len(receipt),
        "predecessor_static_preflight_sha256": predecessor[
            "static_preflight_sha256"
        ],
        "successor_static_preflight_sha256": successor[
            "static_preflight_sha256"
        ],
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v3_amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "pinned_successor_digests": tuple(
            sorted(PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS.items())
        ),
        "current_recipe_review_receipt_bound_for_execution": True,
        "false_authority": {
            field: False for field in V5_REBIND_V4_FALSE_AUTHORITY_FIELDS
        },
    }


def _expected_v5_rebind_v4_binding() -> dict[str, object]:
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v4"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v3"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "amendment_sha256": V5_REBIND_V4_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V3_TARGET_SHA256,
        "transition_kind": "37_to_37_review_receipt_binding",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": 37,
        "path_set_change": "none",
        "v5_contract_sha256_before": V5_REBIND_V3_TARGET_SHA256,
        "v5_contract_sha256_after": V5_REBIND_V3_TARGET_SHA256,
        "v5_contract_digest_change": "none",
        "recipe_schema": "mythic_edge_role_pool_v5_build_recipe.v1",
        "recipe_sha256": V5_CURRENT_RECIPE_SHA256,
        "review_ref": V5_REBIND_V4_REVIEW_REF,
        "review_receipt_digest": V5_REBIND_V4_RECEIPT_DIGEST,
        "review_status": "accepted_exact_recipe_and_contract",
        "reviewed_at_utc": "2026-07-17T01:41:59Z",
        "receipt_storage": "transcript_only",
        "receipt_key_count": 41,
        "predecessor_static_preflight_sha256": (
            V5_CURRENT_RECIPE_PREDECESSOR_STATIC_PREFLIGHT_SHA256
        ),
        "successor_static_preflight_sha256": (
            V5_CURRENT_RECIPE_SUCCESSOR_STATIC_PREFLIGHT_SHA256
        ),
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v3_amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "pinned_successor_digests": tuple(
            sorted(PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS.items())
        ),
        "current_recipe_review_receipt_bound_for_execution": True,
        "false_authority": {
            field: False for field in V5_REBIND_V4_FALSE_AUTHORITY_FIELDS
        },
    }


def _validate_v5_rebind_v4_binding(binding: dict[str, object]) -> None:
    if binding != _expected_v5_rebind_v4_binding():
        raise ValueError("v5 manifest-rebind v4 binding drift")


def _embedded_v5_rebind_v5_review_evidence() -> bytes:
    matches = [
        (payload, value)
        for payload, value in _amendment_json_values()
        if isinstance(value, dict)
        and value.get("review_evidence_schema")
        == "mythic_edge_role_pool_v5_build_reconciliation_contract_review.v1"
    ]
    if len(matches) != 1:
        raise ValueError("v5 review evidence is missing or duplicated")
    return matches[0][0]


def _validate_v5_rebind_v5_review_evidence(
    payload: bytes,
) -> dict[str, object]:
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n") or b"\r" in payload:
        raise ValueError("v5 review evidence must end in exactly one LF")
    document = _strict_json_object(payload)
    if len(document) != 38 or set(document) != set(
        V5_REBIND_V5_REVIEW_EVIDENCE_VALUES
    ):
        raise ValueError("v5 review evidence key set drift")
    if payload != _canonical_json_bytes(document):
        raise ValueError("v5 review evidence is not canonical")
    if document != V5_REBIND_V5_REVIEW_EVIDENCE_VALUES:
        raise ValueError("v5 review evidence binding drift")
    if hashlib.sha256(payload).hexdigest() != V5_REBIND_V5_REVIEW_EVIDENCE_SHA256:
        raise ValueError("v5 review evidence digest drift")
    return document


def _v5_rebind_v5_static_preflight(
    contract_sha256: str,
    amendment_sha256: str,
) -> dict[str, object]:
    historical = _v5_rebind_v4_static_preflight(V5_REBIND_V4_AMENDMENT_SHA256)
    preimage = {
        key: value
        for key, value in historical.items()
        if key != "static_preflight_sha256"
    }
    preimage["contract_sha256"] = contract_sha256
    preimage["manifest_rebind_amendment_sha256"] = amendment_sha256
    preimage["manifest_rebind_to_sha256"] = contract_sha256
    return {
        **preimage,
        "static_preflight_sha256": _json_sha256(preimage),
    }


def _v5_rebind_v5_binding(evidence: dict[str, object]) -> dict[str, object]:
    predecessor = _v5_rebind_v5_static_preflight(
        V5_REBIND_V5_PREDECESSOR_SHA256,
        V5_REBIND_V4_AMENDMENT_SHA256,
    )
    successor = _v5_rebind_v5_static_preflight(
        V5_REBIND_V5_TARGET_SHA256,
        V5_REBIND_V5_AMENDMENT_SHA256,
    )
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v5"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v4"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "amendment_sha256": V5_REBIND_V5_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V5_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT,
        "path_set_change": "none",
        "v5_contract_sha256_before": V5_REBIND_V5_PREDECESSOR_SHA256,
        "v5_contract_sha256_after": V5_REBIND_V5_TARGET_SHA256,
        "v5_contract_digest_change": (
            "exact_predecessor_to_reviewed_successor"
        ),
        "recipe_v1_sha256": V5_CURRENT_RECIPE_SHA256,
        "recipe_v1_status": evidence["recipe_v1_status"],
        "recipe_v2_defined": False,
        "review_evidence_schema": evidence["review_evidence_schema"],
        "review_evidence_key_count": len(evidence),
        "review_evidence_sha256": hashlib.sha256(
            _canonical_json_bytes(evidence)
        ).hexdigest(),
        "predecessor_static_preflight_sha256": predecessor[
            "static_preflight_sha256"
        ],
        "successor_static_preflight_sha256": successor[
            "static_preflight_sha256"
        ],
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v3_amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "v4_amendment_sha256": V5_REBIND_V4_AMENDMENT_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "pinned_successor_digests": tuple(
            sorted(V5_REBIND_V5_PINNED_SUCCESSOR_DIGESTS.items())
        ),
        "false_authority": {
            field: False for field in V5_REBIND_V5_FALSE_AUTHORITY_FIELDS
        },
    }


def _expected_v5_rebind_v5_binding() -> dict[str, object]:
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v5"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v4"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "amendment_sha256": V5_REBIND_V5_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V5_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": 37,
        "path_set_change": "none",
        "v5_contract_sha256_before": V5_REBIND_V5_PREDECESSOR_SHA256,
        "v5_contract_sha256_after": V5_REBIND_V5_TARGET_SHA256,
        "v5_contract_digest_change": (
            "exact_predecessor_to_reviewed_successor"
        ),
        "recipe_v1_sha256": V5_CURRENT_RECIPE_SHA256,
        "recipe_v1_status": "immutable_retired_future_execution_blocked",
        "recipe_v2_defined": False,
        "review_evidence_schema": (
            "mythic_edge_role_pool_v5_build_reconciliation_contract_review.v1"
        ),
        "review_evidence_key_count": 38,
        "review_evidence_sha256": V5_REBIND_V5_REVIEW_EVIDENCE_SHA256,
        "predecessor_static_preflight_sha256": (
            V5_BUILD_RECONCILIATION_PREDECESSOR_STATIC_PREFLIGHT_SHA256
        ),
        "successor_static_preflight_sha256": (
            V5_BUILD_RECONCILIATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256
        ),
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v3_amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "v4_amendment_sha256": V5_REBIND_V4_AMENDMENT_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "pinned_successor_digests": tuple(
            sorted(V5_REBIND_V5_PINNED_SUCCESSOR_DIGESTS.items())
        ),
        "false_authority": {
            field: False for field in V5_REBIND_V5_FALSE_AUTHORITY_FIELDS
        },
    }


def _validate_v5_rebind_v5_binding(binding: dict[str, object]) -> None:
    if binding != _expected_v5_rebind_v5_binding():
        raise ValueError("v5 manifest-rebind v5 binding drift")


def _embedded_v5_rebind_v6_review_evidence() -> bytes:
    matches = [
        (payload, value)
        for payload, value in _amendment_json_values()
        if isinstance(value, dict)
        and value.get("contract_status")
        == "characterization_execution_envelope_review_and_manifest_rebind_blocked"
    ]
    if len(matches) != 1:
        raise ValueError("v6 review evidence is missing or duplicated")
    return matches[0][0]


def _validate_v5_rebind_v6_review_evidence(
    payload: bytes,
) -> dict[str, object]:
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n") or b"\r" in payload:
        raise ValueError("v6 review evidence must end in exactly one LF")
    document = _strict_json_object(payload)
    if len(document) != 22 or set(document) != set(
        V5_REBIND_V6_REVIEW_EVIDENCE_VALUES
    ):
        raise ValueError("v6 review evidence key set drift")
    finding_status = document.get("finding_status")
    validation = document.get("validation")
    if not isinstance(finding_status, dict) or len(finding_status) != 3:
        raise ValueError("v6 finding-status shape drift")
    if not isinstance(validation, dict) or len(validation) != 3:
        raise ValueError("v6 validation shape drift")
    if payload != _canonical_json_bytes(document):
        raise ValueError("v6 review evidence is not canonical")
    if document != V5_REBIND_V6_REVIEW_EVIDENCE_VALUES:
        raise ValueError("v6 review evidence binding drift")
    if hashlib.sha256(payload).hexdigest() != V5_REBIND_V6_REVIEW_EVIDENCE_SHA256:
        raise ValueError("v6 review evidence digest drift")
    return document


def _embedded_v5_characterization_synthetic_matrix() -> bytes:
    matches = [
        (payload, value)
        for payload, value in _contract_json_values()
        if isinstance(value, dict)
        and value.get("schema")
        == "mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1"
    ]
    if len(matches) != 1:
        raise ValueError("characterization matrix is missing or duplicated")
    return matches[0][0]


def _validate_v5_characterization_synthetic_matrix(
    payload: bytes,
) -> dict[str, object]:
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n") or b"\r" in payload:
        raise ValueError("characterization matrix must end in exactly one LF")
    document = _strict_json_object(payload)
    if set(document) != {"case_count", "category_counts", "rows", "schema"}:
        raise ValueError("characterization matrix key set drift")
    if document.get("schema") != (
        "mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1"
    ):
        raise ValueError("characterization matrix schema drift")
    if document.get("case_count") != 36:
        raise ValueError("characterization matrix case-count drift")
    if document.get("category_counts") != {"ast": 14, "host": 6, "lifecycle": 16}:
        raise ValueError("characterization matrix category-count drift")
    rows = document.get("rows")
    if not isinstance(rows, list) or len(rows) != 36:
        raise ValueError("characterization matrix row-count drift")
    if any(not isinstance(row, list) or len(row) != 3 for row in rows):
        raise ValueError("characterization matrix row shape drift")
    row_ids = [row[0] for row in rows]
    if any(not isinstance(row_id, str) for row_id in row_ids):
        raise ValueError("characterization matrix row-id type drift")
    if len(set(row_ids)) != 36:
        raise ValueError("characterization matrix row-id collision")
    if payload != _canonical_json_bytes(document):
        raise ValueError("characterization matrix is not canonical")
    if hashlib.sha256(payload).hexdigest() != V5_REBIND_V6_SYNTHETIC_MATRIX_SHA256:
        raise ValueError("characterization matrix digest drift")
    return document


def _v5_rebind_v6_static_preflight(
    contract_sha256: str,
    amendment_sha256: str,
) -> dict[str, object]:
    historical = _v5_rebind_v5_static_preflight(
        V5_REBIND_V5_TARGET_SHA256,
        V5_REBIND_V5_AMENDMENT_SHA256,
    )
    preimage = {
        key: value
        for key, value in historical.items()
        if key != "static_preflight_sha256"
    }
    preimage["contract_sha256"] = contract_sha256
    preimage["manifest_rebind_amendment_sha256"] = amendment_sha256
    preimage["manifest_rebind_to_sha256"] = contract_sha256
    return {
        **preimage,
        "static_preflight_sha256": _json_sha256(preimage),
    }


def _v5_rebind_v6_binding(
    evidence: dict[str, object],
    matrix: dict[str, object],
) -> dict[str, object]:
    predecessor = _v5_rebind_v6_static_preflight(
        V5_REBIND_V6_PREDECESSOR_SHA256,
        V5_REBIND_V5_AMENDMENT_SHA256,
    )
    successor = _v5_rebind_v6_static_preflight(
        V5_REBIND_V6_TARGET_SHA256,
        V5_REBIND_V6_AMENDMENT_SHA256,
    )
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v6"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v5"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "amendment_sha256": V5_REBIND_V6_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V6_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT,
        "path_set_change": "none",
        "v5_contract_sha256_before": V5_REBIND_V6_PREDECESSOR_SHA256,
        "v5_contract_sha256_after": V5_REBIND_V6_TARGET_SHA256,
        "v5_contract_digest_change": (
            "exact_predecessor_to_reviewed_successor"
        ),
        "accepted_review_evidence_schema": (
            "mythic_edge_role_pool_v5_characterization_execution_envelope_"
            "contract_review.v1"
        ),
        "accepted_review_evidence_root_key_count": len(evidence),
        "accepted_review_evidence_finding_key_count": len(
            evidence["finding_status"]
        ),
        "accepted_review_evidence_validation_key_count": len(
            evidence["validation"]
        ),
        "accepted_review_evidence_sha256": hashlib.sha256(
            _canonical_json_bytes(evidence)
        ).hexdigest(),
        "accepted_review_evidence_storage": (
            "transcript_only_no_separate_receipt_asserted"
        ),
        "characterization_parser_profile": (
            "mythic_edge_role_pool_v5_powershell_ast_characterizer.v2"
        ),
        "characterization_result_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_result.v2"
        ),
        "characterization_retry_activation_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_"
            "activation.v4"
        ),
        "characterization_synthetic_matrix_schema": matrix["schema"],
        "characterization_synthetic_matrix_sha256": hashlib.sha256(
            _canonical_json_bytes(matrix)
        ).hexdigest(),
        "characterization_synthetic_case_count": matrix["case_count"],
        "characterization_retry_activation_key_count": evidence[
            "retry_activation_key_count"
        ],
        "characterization_synthetic_review_receipt_schema": (
            "mythic_edge_role_pool_v5_characterization_synthetic_review_receipt.v1"
        ),
        "characterization_synthetic_review_receipt_key_count": evidence[
            "synthetic_review_receipt_key_count"
        ],
        "predecessor_static_preflight_sha256": predecessor[
            "static_preflight_sha256"
        ],
        "successor_static_preflight_sha256": successor[
            "static_preflight_sha256"
        ],
        "predecessor_manifest_sha256": (
            "6e6a2d08c3fe3dbcb00c03a9918851dd4478e3daf3f8ba8d17859d60fa1a072c"
        ),
        "validator_preimplementation_sha256": (
            "6101f1a1d7a24c0b2dc6faa0e378e93aaff845729e56368baff03815e91188bc"
        ),
        "test_preimplementation_sha256": (
            "4de1f059934b193d80362aff51029aa342097400b9d0aa2bcd04c85b6fff8c74"
        ),
        "build_recipe_sha256": V5_CURRENT_RECIPE_SHA256,
        "candidate_edit_envelope_sha256": (
            V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS["candidate_edit_envelope_sha256"]
        ),
        "atomic_oracle_tuple_count": V5_REBIND_V3_ORACLE_TUPLE_COUNT,
        "atomic_oracle_outcome_counts": V5_REBIND_V3_ORACLE_OUTCOME_COUNTS,
        "atomic_oracle_sha256": V5_REBIND_V3_ORACLE_SHA256,
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v3_amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "v4_amendment_sha256": V5_REBIND_V4_AMENDMENT_SHA256,
        "v5_amendment_sha256": V5_REBIND_V5_AMENDMENT_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "pinned_successor_digests": tuple(
            sorted(V5_REBIND_V6_PINNED_SUCCESSOR_DIGESTS.items())
        ),
        "false_authority": {
            field: False for field in V5_REBIND_V6_FALSE_AUTHORITY_FIELDS
        },
    }


def _expected_v5_rebind_v6_binding() -> dict[str, object]:
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v6"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v5"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "amendment_sha256": V5_REBIND_V6_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V6_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": 37,
        "path_set_change": "none",
        "v5_contract_sha256_before": V5_REBIND_V6_PREDECESSOR_SHA256,
        "v5_contract_sha256_after": V5_REBIND_V6_TARGET_SHA256,
        "v5_contract_digest_change": (
            "exact_predecessor_to_reviewed_successor"
        ),
        "accepted_review_evidence_schema": (
            "mythic_edge_role_pool_v5_characterization_execution_envelope_"
            "contract_review.v1"
        ),
        "accepted_review_evidence_root_key_count": 22,
        "accepted_review_evidence_finding_key_count": 3,
        "accepted_review_evidence_validation_key_count": 3,
        "accepted_review_evidence_sha256": V5_REBIND_V6_REVIEW_EVIDENCE_SHA256,
        "accepted_review_evidence_storage": (
            "transcript_only_no_separate_receipt_asserted"
        ),
        "characterization_parser_profile": (
            "mythic_edge_role_pool_v5_powershell_ast_characterizer.v2"
        ),
        "characterization_result_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_result.v2"
        ),
        "characterization_retry_activation_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_"
            "activation.v4"
        ),
        "characterization_synthetic_matrix_schema": (
            "mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1"
        ),
        "characterization_synthetic_matrix_sha256": (
            V5_REBIND_V6_SYNTHETIC_MATRIX_SHA256
        ),
        "characterization_synthetic_case_count": 36,
        "characterization_retry_activation_key_count": 54,
        "characterization_synthetic_review_receipt_schema": (
            "mythic_edge_role_pool_v5_characterization_synthetic_review_receipt.v1"
        ),
        "characterization_synthetic_review_receipt_key_count": 16,
        "predecessor_static_preflight_sha256": (
            V5_CHARACTERIZATION_PREDECESSOR_STATIC_PREFLIGHT_SHA256
        ),
        "successor_static_preflight_sha256": (
            V5_CHARACTERIZATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256
        ),
        "predecessor_manifest_sha256": (
            "6e6a2d08c3fe3dbcb00c03a9918851dd4478e3daf3f8ba8d17859d60fa1a072c"
        ),
        "validator_preimplementation_sha256": (
            "6101f1a1d7a24c0b2dc6faa0e378e93aaff845729e56368baff03815e91188bc"
        ),
        "test_preimplementation_sha256": (
            "4de1f059934b193d80362aff51029aa342097400b9d0aa2bcd04c85b6fff8c74"
        ),
        "build_recipe_sha256": V5_CURRENT_RECIPE_SHA256,
        "candidate_edit_envelope_sha256": (
            "32694f48845e22fcf597b5b1b32600c905e3af0478d3ac2ef2993684a44aebed"
        ),
        "atomic_oracle_tuple_count": 768,
        "atomic_oracle_outcome_counts": [1, 1, 45, 4, 717],
        "atomic_oracle_sha256": (
            "19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269"
        ),
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v3_amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "v4_amendment_sha256": V5_REBIND_V4_AMENDMENT_SHA256,
        "v5_amendment_sha256": V5_REBIND_V5_AMENDMENT_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "pinned_successor_digests": tuple(
            sorted(V5_REBIND_V6_PINNED_SUCCESSOR_DIGESTS.items())
        ),
        "false_authority": {
            field: False for field in V5_REBIND_V6_FALSE_AUTHORITY_FIELDS
        },
    }


def _validate_v5_rebind_v6_binding(binding: dict[str, object]) -> None:
    if binding != _expected_v5_rebind_v6_binding():
        raise ValueError("v5 manifest-rebind v6 binding drift")


def _embedded_v5_rebind_v7_review_evidence() -> bytes:
    matches = [
        (payload, value)
        for payload, value in _amendment_json_values()
        if isinstance(value, dict)
        and value.get("role_performed")
        == "Codex E: Independent V5 Real-Source Adapter Contract Re-reviewer"
    ]
    if len(matches) != 1:
        raise ValueError("v7 review evidence is missing or duplicated")
    return matches[0][0]


def _validate_v5_rebind_v7_review_evidence(
    payload: bytes,
) -> dict[str, object]:
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n") or b"\r" in payload:
        raise ValueError("v7 review evidence must end in exactly one LF")
    document = _strict_json_object(payload)
    if len(document) != 17 or set(document) != set(
        V5_REBIND_V7_REVIEW_EVIDENCE_VALUES
    ):
        raise ValueError("v7 review evidence key set drift")
    finding_status = document.get("finding_status")
    if not isinstance(finding_status, dict) or len(finding_status) != 1:
        raise ValueError("v7 finding-status shape drift")
    if payload != _canonical_json_bytes(document):
        raise ValueError("v7 review evidence is not canonical")
    if document != V5_REBIND_V7_REVIEW_EVIDENCE_VALUES:
        raise ValueError("v7 review evidence binding drift")
    if hashlib.sha256(payload).hexdigest() != V5_REBIND_V7_REVIEW_EVIDENCE_SHA256:
        raise ValueError("v7 review evidence digest drift")
    return document


def _embedded_v5_characterization_adapter_matrix() -> bytes:
    matches = [
        (payload, value)
        for payload, value in _contract_json_values()
        if isinstance(value, dict)
        and value.get("schema")
        == "mythic_edge_role_pool_v5_characterization_adapter_synthetic_matrix.v2"
    ]
    if len(matches) != 1:
        raise ValueError("adapter matrix is missing or duplicated")
    return matches[0][0]


def _validate_v5_characterization_adapter_matrix(
    payload: bytes,
) -> dict[str, object]:
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n") or b"\r" in payload:
        raise ValueError("adapter matrix must end in exactly one LF")
    document = _strict_json_object(payload)
    if set(document) != {"case_count", "category_counts", "rows", "schema"}:
        raise ValueError("adapter matrix key set drift")
    if document.get("schema") != (
        "mythic_edge_role_pool_v5_characterization_adapter_synthetic_matrix.v2"
    ):
        raise ValueError("adapter matrix schema drift")
    if document.get("case_count") != 37:
        raise ValueError("adapter matrix case-count drift")
    if document.get("category_counts") != {
        "binding": 2,
        "child": 10,
        "controller": 7,
        "determinism": 1,
        "outer_launcher": 17,
    }:
        raise ValueError("adapter matrix category-count drift")
    rows = document.get("rows")
    if not isinstance(rows, list) or len(rows) != 37:
        raise ValueError("adapter matrix row-count drift")
    if any(not isinstance(row, list) or len(row) != 3 for row in rows):
        raise ValueError("adapter matrix row shape drift")
    row_ids = [row[0] for row in rows]
    expected_row_ids = [f"I{index:02d}" for index in range(1, 21)] + [
        f"O{index:02d}" for index in range(1, 18)
    ]
    if row_ids != expected_row_ids or len(set(row_ids)) != 37:
        raise ValueError("adapter matrix row-id or order drift")
    if payload != _canonical_json_bytes(document):
        raise ValueError("adapter matrix is not canonical")
    if hashlib.sha256(payload).hexdigest() != V5_REBIND_V7_ADAPTER_MATRIX_SHA256:
        raise ValueError("adapter matrix digest drift")
    return document


def _classify_v5_rebind_v7_outer_tuple(
    observations: tuple[str, ...],
) -> tuple[str, str]:
    (
        prevalidation,
        start,
        exit_status,
        stdout,
        stderr,
        cleanup,
        result_candidate,
    ) = observations
    not_applicable_tail = (
        exit_status == "not_applicable"
        and stdout == "not_applicable"
        and stderr == "not_applicable"
        and cleanup == "not_applicable"
        and result_candidate == "not_present"
    )
    if prevalidation == "failed" and start == "not_invoked" and not_applicable_tail:
        return (
            "blocked_before_controller_start",
            "binding_failed_before_controller_start",
        )
    if prevalidation == "passed" and start == "failed" and not_applicable_tail:
        return "blocked_before_controller_start", "controller_start_failed"

    coherent_started = (
        prevalidation == "passed"
        and start == "started"
        and exit_status in {"zero", "nonzero"}
        and stdout
        in {"one_canonical_result", "empty", "malformed", "extra_or_overflow"}
        and stderr in {"empty", "nonempty_or_overflow"}
        and cleanup in {"zero", "nonzero"}
        and result_candidate
        in {
            "not_present",
            "valid_complete",
            "valid_degraded",
            "valid_blocked",
            "invalid_or_incoherent",
        }
    )
    if not coherent_started:
        return "cleanup_state_unknown", "controller_state_unknown"
    if cleanup == "nonzero":
        return "blocked_after_controller_start", "controller_residue_detected"
    if stderr == "nonempty_or_overflow":
        return (
            "blocked_after_controller_start",
            "controller_stderr_nonempty_or_overflow",
        )
    if stdout == "extra_or_overflow":
        return (
            "blocked_after_controller_start",
            "controller_stdout_extra_or_overflow",
        )
    if stdout == "malformed":
        return "blocked_after_controller_start", "controller_stdout_malformed"
    if stdout == "empty":
        return "blocked_after_controller_start", "controller_stdout_empty"
    if exit_status == "nonzero":
        return "blocked_after_controller_start", "controller_exit_nonzero"
    accepted_status = {
        "valid_complete": "accepted_complete",
        "valid_degraded": "accepted_degraded",
        "valid_blocked": "accepted_blocked",
    }.get(result_candidate)
    if accepted_status is not None:
        return accepted_status, "none"
    return (
        "blocked_after_controller_start",
        "accepted_result_cross_field_mismatch",
    )


def _v5_rebind_v7_outer_oracle_rows(
    dimensions: tuple[tuple[str, tuple[str, ...]], ...] = (
        V5_REBIND_V7_OUTER_DIMENSIONS
    ),
) -> list[dict[str, object]]:
    if dimensions != V5_REBIND_V7_OUTER_DIMENSIONS:
        raise ValueError("outer-oracle dimension order or vocabulary drift")
    rows: list[dict[str, object]] = []
    for observations in itertools.product(*(values for _, values in dimensions)):
        handoff, failure = _classify_v5_rebind_v7_outer_tuple(observations)
        rows.append(
            {
                "observations": observations,
                "handoff_statuses": (handoff,),
                "outer_failure_codes": (failure,),
            }
        )
    return rows


def _validate_v5_rebind_v7_outer_oracle(
    rows: list[dict[str, object]],
    dimensions: tuple[tuple[str, tuple[str, ...]], ...] = (
        V5_REBIND_V7_OUTER_DIMENSIONS
    ),
) -> dict[str, object]:
    if dimensions != V5_REBIND_V7_OUTER_DIMENSIONS:
        raise ValueError("outer-oracle dimension order or vocabulary drift")
    expected_tuples = list(itertools.product(*(values for _, values in dimensions)))
    if len(rows) != 15360 or len(expected_tuples) != 15360:
        raise ValueError("outer-oracle tuple-count drift")
    observed_tuples: set[tuple[str, ...]] = set()
    handoff_counts: dict[str, int] = {}
    failure_counts: dict[str, int] = {}
    for index, (row, expected_tuple) in enumerate(zip(rows, expected_tuples)):
        if set(row) != {
            "observations",
            "handoff_statuses",
            "outer_failure_codes",
        }:
            raise ValueError("outer-oracle row shape drift")
        observations = row["observations"]
        if observations != expected_tuple or not isinstance(observations, tuple):
            raise ValueError(f"outer-oracle tuple order drift at {index}")
        if observations in observed_tuples:
            raise ValueError("outer-oracle tuple collision")
        observed_tuples.add(observations)
        handoffs = row["handoff_statuses"]
        failures = row["outer_failure_codes"]
        if not isinstance(handoffs, tuple) or len(handoffs) != 1:
            raise ValueError("outer-oracle tuple must have exactly one handoff")
        if not isinstance(failures, tuple) or len(failures) != 1:
            raise ValueError("outer-oracle tuple must have exactly one failure")
        expected_handoff, expected_failure = _classify_v5_rebind_v7_outer_tuple(
            observations
        )
        if handoffs[0] != expected_handoff or failures[0] != expected_failure:
            raise ValueError("outer-oracle tuple classification drift")
        handoff_counts[handoffs[0]] = handoff_counts.get(handoffs[0], 0) + 1
        failure_counts[failures[0]] = failure_counts.get(failures[0], 0) + 1
    if handoff_counts != V5_REBIND_V7_HANDOFF_COUNTS:
        raise ValueError("outer-oracle handoff-count drift")
    if failure_counts != V5_REBIND_V7_OUTER_FAILURE_COUNTS:
        raise ValueError("outer-oracle failure-count drift")
    return {
        "tuple_count": len(rows),
        "handoff_counts": handoff_counts,
        "outer_failure_counts": failure_counts,
    }


def _v5_rebind_v7_static_preflight(
    contract_sha256: str,
    amendment_sha256: str,
) -> dict[str, object]:
    return _v5_rebind_v6_static_preflight(contract_sha256, amendment_sha256)


def _v5_rebind_v7_binding(
    evidence: dict[str, object],
    core_matrix: dict[str, object],
    adapter_matrix: dict[str, object],
    oracle: dict[str, object],
) -> dict[str, object]:
    predecessor = _v5_rebind_v7_static_preflight(
        V5_REBIND_V7_PREDECESSOR_SHA256,
        V5_REBIND_V6_AMENDMENT_SHA256,
    )
    successor = _v5_rebind_v7_static_preflight(
        V5_REBIND_V7_TARGET_SHA256,
        V5_REBIND_V7_AMENDMENT_SHA256,
    )
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v7"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v6"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "amendment_sha256": hashlib.sha256(
            V5_REBIND_AMENDMENT.read_bytes()
        ).hexdigest(),
        "contract_sha256": hashlib.sha256(
            V5_REBIND_CONTRACT.read_bytes()
        ).hexdigest(),
        "transition_kind": "37_to_37_digest_rebind",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT,
        "path_set_change": "none",
        "v5_contract_sha256_before": V5_REBIND_V7_PREDECESSOR_SHA256,
        "v5_contract_sha256_after": V5_REBIND_V7_TARGET_SHA256,
        "v5_contract_digest_change": "exact_predecessor_to_reviewed_successor",
        "v5_contract_status": (
            "outer_launcher_contract_review_and_manifest_rebind_blocked"
        ),
        "accepted_review_evidence_schema": (
            "mythic_edge_role_pool_v5_real_source_adapter_contract_review.v1"
        ),
        "accepted_review_evidence_root_key_count": len(evidence),
        "accepted_review_evidence_finding_key_count": len(
            evidence["finding_status"]
        ),
        "accepted_review_evidence_sha256": hashlib.sha256(
            _canonical_json_bytes(evidence)
        ).hexdigest(),
        "accepted_review_evidence_storage": (
            "transcript_only_no_separate_receipt_asserted"
        ),
        "characterization_activation_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_"
            "activation.v5"
        ),
        "characterization_activation_key_count": 64,
        "characterization_controller_profile": (
            "mythic_edge_role_pool_v5_characterization_controller.v1"
        ),
        "characterization_controller_request_schema": (
            "mythic_edge_role_pool_v5_characterization_controller_request.v1"
        ),
        "characterization_controller_request_key_count": 10,
        "characterization_parser_profile": (
            "mythic_edge_role_pool_v5_powershell_ast_characterizer.v3"
        ),
        "characterization_child_result_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_child_"
            "result.v1"
        ),
        "characterization_child_result_key_count": 13,
        "characterization_result_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_result.v3"
        ),
        "characterization_result_key_count": 20,
        "characterization_attempt_handoff_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_attempt_"
            "handoff.v1"
        ),
        "characterization_attempt_handoff_key_count": 27,
        "characterization_program_bundle_schema": (
            "mythic_edge_role_pool_v5_characterization_program_bundle.v2"
        ),
        "characterization_program_bundle_key_count": 18,
        "characterization_core_matrix_schema": core_matrix["schema"],
        "characterization_core_matrix_sha256": hashlib.sha256(
            _canonical_json_bytes(core_matrix)
        ).hexdigest(),
        "characterization_core_case_count": core_matrix["case_count"],
        "characterization_adapter_matrix_schema": adapter_matrix["schema"],
        "characterization_adapter_matrix_sha256": hashlib.sha256(
            _canonical_json_bytes(adapter_matrix)
        ).hexdigest(),
        "characterization_adapter_case_count": adapter_matrix["case_count"],
        "characterization_outer_oracle_tuple_count": oracle["tuple_count"],
        "characterization_outer_oracle_accepted_count": sum(
            oracle["handoff_counts"][status]
            for status in (
                "accepted_complete",
                "accepted_degraded",
                "accepted_blocked",
            )
        ),
        "characterization_outer_oracle_blocked_before_start_count": oracle[
            "handoff_counts"
        ]["blocked_before_controller_start"],
        "characterization_outer_oracle_blocked_after_start_count": oracle[
            "handoff_counts"
        ]["blocked_after_controller_start"],
        "characterization_outer_oracle_cleanup_unknown_count": oracle[
            "handoff_counts"
        ]["cleanup_state_unknown"],
        "characterization_bundle_review_schema": (
            "mythic_edge_role_pool_v5_characterization_bundle_review_receipt.v3"
        ),
        "characterization_bundle_review_key_count": 29,
        "predecessor_static_preflight_sha256": predecessor[
            "static_preflight_sha256"
        ],
        "successor_static_preflight_sha256": successor["static_preflight_sha256"],
        "predecessor_manifest_sha256": (
            "5f95acc7c29be1d332f893ce518f8e1bfe0900e38394821d70d51ff637f5f8fc"
        ),
        "validator_preimplementation_sha256": (
            "1333f9e1fd176fa4a8e19ea3f09b9632134d5bfbbd63cb77aa2ea664372912f9"
        ),
        "test_preimplementation_sha256": (
            "fc9224f36028f95b62836e4a3d5a125b5c0dfefee558b33ba77f4089d0675cf4"
        ),
        "build_recipe_sha256": V5_CURRENT_RECIPE_SHA256,
        "candidate_edit_envelope_sha256": (
            V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS["candidate_edit_envelope_sha256"]
        ),
        "atomic_oracle_tuple_count": V5_REBIND_V3_ORACLE_TUPLE_COUNT,
        "atomic_oracle_outcome_counts": V5_REBIND_V3_ORACLE_OUTCOME_COUNTS,
        "atomic_oracle_sha256": V5_REBIND_V3_ORACLE_SHA256,
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v3_amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "v4_amendment_sha256": V5_REBIND_V4_AMENDMENT_SHA256,
        "v5_amendment_sha256": V5_REBIND_V5_AMENDMENT_SHA256,
        "v6_amendment_sha256": V5_REBIND_V6_AMENDMENT_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "pinned_successor_digests": tuple(
            sorted(PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS.items())
        ),
        "false_authority": {
            field: False for field in V5_REBIND_V7_FALSE_AUTHORITY_FIELDS
        },
    }


def _expected_v5_rebind_v7_binding() -> dict[str, object]:
    return {
        "amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v7"
        ),
        "predecessor_amendment_id": (
            "mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_"
            "amendment.v6"
        ),
        "predecessor_manifest_binding_status": "implemented_current",
        "amendment_sha256": V5_REBIND_V7_AMENDMENT_SHA256,
        "contract_sha256": V5_REBIND_V7_TARGET_SHA256,
        "transition_kind": "37_to_37_digest_rebind",
        "manifest_file_count_before": 37,
        "manifest_file_count_after": 37,
        "path_set_change": "none",
        "v5_contract_sha256_before": V5_REBIND_V7_PREDECESSOR_SHA256,
        "v5_contract_sha256_after": V5_REBIND_V7_TARGET_SHA256,
        "v5_contract_digest_change": "exact_predecessor_to_reviewed_successor",
        "v5_contract_status": (
            "outer_launcher_contract_review_and_manifest_rebind_blocked"
        ),
        "accepted_review_evidence_schema": (
            "mythic_edge_role_pool_v5_real_source_adapter_contract_review.v1"
        ),
        "accepted_review_evidence_root_key_count": 17,
        "accepted_review_evidence_finding_key_count": 1,
        "accepted_review_evidence_sha256": V5_REBIND_V7_REVIEW_EVIDENCE_SHA256,
        "accepted_review_evidence_storage": (
            "transcript_only_no_separate_receipt_asserted"
        ),
        "characterization_activation_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_"
            "activation.v5"
        ),
        "characterization_activation_key_count": 64,
        "characterization_controller_profile": (
            "mythic_edge_role_pool_v5_characterization_controller.v1"
        ),
        "characterization_controller_request_schema": (
            "mythic_edge_role_pool_v5_characterization_controller_request.v1"
        ),
        "characterization_controller_request_key_count": 10,
        "characterization_parser_profile": (
            "mythic_edge_role_pool_v5_powershell_ast_characterizer.v3"
        ),
        "characterization_child_result_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_child_"
            "result.v1"
        ),
        "characterization_child_result_key_count": 13,
        "characterization_result_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_result.v3"
        ),
        "characterization_result_key_count": 20,
        "characterization_attempt_handoff_schema": (
            "mythic_edge_role_pool_v5_build_dependency_characterization_attempt_"
            "handoff.v1"
        ),
        "characterization_attempt_handoff_key_count": 27,
        "characterization_program_bundle_schema": (
            "mythic_edge_role_pool_v5_characterization_program_bundle.v2"
        ),
        "characterization_program_bundle_key_count": 18,
        "characterization_core_matrix_schema": (
            "mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1"
        ),
        "characterization_core_matrix_sha256": V5_REBIND_V7_CORE_MATRIX_SHA256,
        "characterization_core_case_count": 36,
        "characterization_adapter_matrix_schema": (
            "mythic_edge_role_pool_v5_characterization_adapter_synthetic_matrix.v2"
        ),
        "characterization_adapter_matrix_sha256": (
            V5_REBIND_V7_ADAPTER_MATRIX_SHA256
        ),
        "characterization_adapter_case_count": 37,
        "characterization_outer_oracle_tuple_count": 15360,
        "characterization_outer_oracle_accepted_count": 3,
        "characterization_outer_oracle_blocked_before_start_count": 2,
        "characterization_outer_oracle_blocked_after_start_count": 157,
        "characterization_outer_oracle_cleanup_unknown_count": 15198,
        "characterization_bundle_review_schema": (
            "mythic_edge_role_pool_v5_characterization_bundle_review_receipt.v3"
        ),
        "characterization_bundle_review_key_count": 29,
        "predecessor_static_preflight_sha256": (
            V5_REAL_SOURCE_ADAPTER_PREDECESSOR_STATIC_PREFLIGHT_SHA256
        ),
        "successor_static_preflight_sha256": (
            V5_REAL_SOURCE_ADAPTER_SUCCESSOR_STATIC_PREFLIGHT_SHA256
        ),
        "predecessor_manifest_sha256": (
            "5f95acc7c29be1d332f893ce518f8e1bfe0900e38394821d70d51ff637f5f8fc"
        ),
        "validator_preimplementation_sha256": (
            "1333f9e1fd176fa4a8e19ea3f09b9632134d5bfbbd63cb77aa2ea664372912f9"
        ),
        "test_preimplementation_sha256": (
            "fc9224f36028f95b62836e4a3d5a125b5c0dfefee558b33ba77f4089d0675cf4"
        ),
        "build_recipe_sha256": V5_CURRENT_RECIPE_SHA256,
        "candidate_edit_envelope_sha256": (
            "32694f48845e22fcf597b5b1b32600c905e3af0478d3ac2ef2993684a44aebed"
        ),
        "atomic_oracle_tuple_count": 768,
        "atomic_oracle_outcome_counts": [1, 1, 45, 4, 717],
        "atomic_oracle_sha256": (
            "19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269"
        ),
        "v1_amendment_sha256": V5_REBIND_AMENDMENT_SHA256,
        "v2_amendment_sha256": V5_REBIND_V2_AMENDMENT_SHA256,
        "v3_amendment_sha256": V5_REBIND_V3_AMENDMENT_SHA256,
        "v4_amendment_sha256": V5_REBIND_V4_AMENDMENT_SHA256,
        "v5_amendment_sha256": V5_REBIND_V5_AMENDMENT_SHA256,
        "v6_amendment_sha256": V5_REBIND_V6_AMENDMENT_SHA256,
        "allowed_added_paths": tuple(sorted(PRE_APP_SERVER_ALLOWED_ADDED_PATHS)),
        "allowed_modified_paths": tuple(sorted(ALLOWED_MODIFIED_PATHS)),
        "pinned_successor_digests": tuple(
            sorted(PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS.items())
        ),
        "false_authority": {
            field: False for field in V5_REBIND_V7_FALSE_AUTHORITY_FIELDS
        },
    }


def _validate_v5_rebind_v7_binding(binding: dict[str, object]) -> None:
    if binding != _expected_v5_rebind_v7_binding():
        raise ValueError("v5 manifest-rebind v7 binding drift")


def observation(attempt: str = "1_of_2") -> dict[str, object]:
    identifier = (
        "33333333-3333-4333-8333-333333333331"
        if attempt == "1_of_2"
        else "33333333-3333-4333-8333-333333333332"
    )
    created_at = (
        "2026-07-15T12:00:00Z"
        if attempt == "1_of_2"
        else "2026-07-15T12:01:00Z"
    )
    return build_stage3_observation(
        identifier,
        ATTEMPT_SERIES_ID,
        attempt,
        1 if attempt == "1_of_2" else 2,
        created_at,
    )


def rehash(document: dict[str, object]) -> dict[str, object]:
    result = copy.deepcopy(document)
    result["digest"] = canonical_self_digest(result)
    return result


class Stage3BehavioralPlanningTests(unittest.TestCase):
    def assert_manifest_rows_rejected(
        self, rows: list[dict[str, str]], expected_error: str
    ) -> None:
        document = observation()
        with mock.patch.object(stage3, "current_skill_manifest", return_value=rows):
            errors = validate_stage3_behavioral_planning(document)
        self.assertTrue(
            any(expected_error in error for error in errors),
            f"expected {expected_error!r} in {errors!r}",
        )

    def assert_pinned_metadata_rejected_before_target_access(
        self,
        skill_relative_path: str,
        metadata: object,
        expected_error: str,
    ) -> None:
        successor_path = SKILL_ROOT / skill_relative_path
        original_lstat = Path.lstat

        def synthetic_lstat(path: Path) -> object:
            if path == successor_path:
                if isinstance(metadata, BaseException):
                    raise metadata
                return metadata
            return original_lstat(path)

        with (
            mock.patch.object(Path, "lstat", autospec=True, side_effect=synthetic_lstat),
            mock.patch.object(
                stage3,
                "_manifest_row",
                side_effect=AssertionError("pinned target must not be hashed"),
            ),
            mock.patch.object(
                Path,
                "resolve",
                side_effect=AssertionError("pinned target must not be followed"),
            ),
            mock.patch.object(
                Path,
                "open",
                side_effect=AssertionError("pinned target must not be opened"),
            ),
            mock.patch.object(
                Path,
                "read_bytes",
                side_effect=AssertionError("pinned target must not be read"),
            ),
            mock.patch.object(
                Path,
                "replace",
                side_effect=AssertionError("pinned target must not be replaced"),
            ),
            mock.patch.object(
                stage3.hashlib,
                "sha256",
                side_effect=AssertionError("pinned target must not be hashed"),
            ),
        ):
            with self.assertRaisesRegex(stage3.ManifestTransitionError, expected_error):
                expected_contract_transition()

    def assert_v5_metadata_rejected_before_target_access(
        self, metadata: object, expected_error: str
    ) -> None:
        self.assert_pinned_metadata_rejected_before_target_access(
            stage3.V5_SUCCESSOR_SKILL_RELATIVE_PATH,
            metadata,
            expected_error,
        )

    def assert_pinned_case_representation_rejected(
        self,
        skill_relative_path: str,
        *,
        duplicate: bool,
        expected_error: str,
    ) -> None:
        target_path = SKILL_ROOT / skill_relative_path
        parent = target_path.parent
        entries = list(parent.iterdir())
        if not duplicate:
            entries = [item for item in entries if item.name != target_path.name]
        case_variant = parent / target_path.name.swapcase()
        original_iterdir = Path.iterdir

        def synthetic_iterdir(path: Path) -> object:
            if path == parent:
                return iter([*entries, case_variant])
            return original_iterdir(path)

        with (
            mock.patch.object(
                Path, "iterdir", autospec=True, side_effect=synthetic_iterdir
            ),
            mock.patch.object(
                stage3,
                "_manifest_row",
                side_effect=AssertionError("case-varied target must not be hashed"),
            ),
            mock.patch.object(
                Path,
                "read_bytes",
                side_effect=AssertionError("case-varied target must not be read"),
            ),
            mock.patch.object(
                stage3.hashlib,
                "sha256",
                side_effect=AssertionError("case-varied target must not be hashed"),
            ),
        ):
            with self.assertRaisesRegex(stage3.ManifestTransitionError, expected_error):
                expected_contract_transition()

    def test_both_observation_attempts_validate_with_distinct_identities(self) -> None:
        first = observation("1_of_2")
        second = observation("2_of_2")
        self.assertEqual(validate_stage3_behavioral_planning(first), [])
        self.assertEqual(validate_stage3_behavioral_planning(second), [])
        self.assertNotEqual(first["observation_id"], second["observation_id"])
        self.assertNotEqual(first["digest"], second["digest"])

    def test_stage2_entry_binding_is_exact_and_does_not_invent_review_receipt(self) -> None:
        document = observation()
        self.assertEqual(document["stage2_entry_evidence"], STAGE2_ENTRY_EVIDENCE)
        self.assertIs(
            document["stage2_entry_evidence"]["separate_review_receipt_file_claimed"],
            False,
        )
        self.assertEqual(
            document["stage2_entry_evidence"]["subsequent_review_receipt_digest"],
            "8bd72f917f5b7782121571a6c9dc23964151e66d352c5d1751ad66f59a103f8e",
        )
        document["stage2_entry_evidence"]["pair_digest"] = "0" * 64
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("stage2_entry_evidence" in error for error in errors))

    def test_contract_transition_is_exact_and_fail_closes_v3_validator(self) -> None:
        transition = expected_contract_transition()
        self.assertEqual(transition["entry_manifest_file_count"], 30)
        self.assertEqual(transition["current_manifest_file_count"], 39)
        self.assertEqual(transition["removed_paths"], [])
        self.assertIs(transition["production_plan_validator_unchanged"], False)
        plan_path = "mythic-edge-role-pool/scripts/check_pool_plan.py"
        current = {row["path"]: row["sha256"] for row in current_skill_manifest()}
        self.assertEqual(len(STAGE2_BASELINE_FILES), 30)
        self.assertIn("mythic-edge-workflow/agents/openai.yaml", STAGE2_BASELINE_FILES)
        self.assertNotEqual(current[plan_path], STAGE2_BASELINE_FILES[plan_path])
        self.assertEqual(transition["production_plan_validator_sha256"], current[plan_path])
        changed_paths = {row["path"] for row in transition["change_set"]}
        self.assertEqual(
            changed_paths, ALLOWED_MODIFIED_PATHS | ALLOWED_ADDED_PATHS
        )
        successor_rows = [
            row
            for row in transition["change_set"]
            if row["path"] == SUCCESSOR_MANIFEST_PATH
        ]
        self.assertEqual(
            successor_rows,
            [
                {
                    "path": SUCCESSOR_MANIFEST_PATH,
                    "change_kind": "added",
                    "before_sha256": None,
                    "after_sha256": SUCCESSOR_SHA256,
                }
            ],
        )
        v4_successor_rows = [
            row
            for row in transition["change_set"]
            if row["path"] == V4_SUCCESSOR_MANIFEST_PATH
        ]
        self.assertEqual(
            v4_successor_rows,
            [
                {
                    "path": V4_SUCCESSOR_MANIFEST_PATH,
                    "change_kind": "added",
                    "before_sha256": None,
                    "after_sha256": V4_SUCCESSOR_SHA256,
                }
            ],
        )
        v5_successor_rows = [
            row
            for row in transition["change_set"]
            if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
        ]
        self.assertEqual(
            v5_successor_rows,
            [
                {
                    "path": V5_SUCCESSOR_MANIFEST_PATH,
                    "change_kind": "added",
                    "before_sha256": None,
                    "after_sha256": V5_SUCCESSOR_SHA256,
                }
            ],
        )
        for path, digest in {
            APP_SERVER_ADAPTER_MANIFEST_PATH: APP_SERVER_ADAPTER_SHA256,
            APP_SERVER_ADAPTER_TEST_MANIFEST_PATH: APP_SERVER_ADAPTER_TEST_SHA256,
        }.items():
            with self.subTest(path=path):
                self.assertEqual(
                    [
                        row
                        for row in transition["change_set"]
                        if row["path"] == path
                    ],
                    [
                        {
                            "path": path,
                            "change_kind": "added",
                            "before_sha256": None,
                            "after_sha256": digest,
                        }
                    ],
                )
        transition_paths = [row["path"] for row in transition["change_set"]]
        self.assertEqual(transition_paths, sorted(transition_paths))
        self.assertEqual(len(ALLOWED_ADDED_PATHS), 9)
        self.assertEqual(len(ALLOWED_MODIFIED_PATHS), 13)
        self.assertEqual(
            PINNED_SUCCESSOR_DIGESTS,
            {
                SUCCESSOR_MANIFEST_PATH: SUCCESSOR_SHA256,
                V4_SUCCESSOR_MANIFEST_PATH: V4_SUCCESSOR_SHA256,
                V5_SUCCESSOR_MANIFEST_PATH: V5_SUCCESSOR_SHA256,
                APP_SERVER_ADAPTER_MANIFEST_PATH: APP_SERVER_ADAPTER_SHA256,
                APP_SERVER_ADAPTER_TEST_MANIFEST_PATH: (
                    APP_SERVER_ADAPTER_TEST_SHA256
                ),
            },
        )

    def test_app_server_predecessor_and_reviewed_candidate_manifests_are_exact(
        self,
    ) -> None:
        rows = current_skill_manifest()
        self.assertEqual(len(rows), 39)
        self.assertEqual(
            [row["path"] for row in rows],
            sorted(row["path"] for row in rows),
        )

        reviewed_candidate = copy.deepcopy(rows)
        reviewed_candidate_by_path = {
            row["path"]: row for row in reviewed_candidate
        }
        stage3_pre_edit_digests = {
            (
                "mythic-edge-role-pool/scripts/"
                "check_stage3_behavioral_planning.py"
            ): "0c82bab47e45d87d66cd317027a2a7c63b11341bb734d75f5f780c7c7ac72b2e",
            (
                "mythic-edge-role-pool/scripts/"
                "test_stage3_behavioral_planning.py"
            ): "f334ebbe67d5fff8f68797e0709770d00cb254215e710d59e9fb331daca7ab08",
        }
        for path, digest in stage3_pre_edit_digests.items():
            reviewed_candidate_by_path[path]["sha256"] = digest
        reviewed_candidate = sorted(reviewed_candidate, key=lambda row: row["path"])
        self.assertEqual(len(stage3.canonical_bytes(reviewed_candidate)), 5729)
        self.assertEqual(
            stage3.canonical_digest(reviewed_candidate),
            "b0a0dfeae17aa4c56e3b9abe8e3104e3f8893f38387a31c577cf3b54401de2a4",
        )

        predecessor = [
            copy.deepcopy(row)
            for row in reviewed_candidate
            if row["path"] not in APP_SERVER_ADDED_PATHS
        ]
        predecessor_by_path = {row["path"]: row for row in predecessor}
        predecessor_by_path[
            "mythic-edge-role-pool/scripts/check_pool_plan.py"
        ]["sha256"] = (
            "cd85d9a33fbd92d8b29d8ec092a03492d7e05915a973796c5218a6eaf903fae0"
        )
        predecessor_by_path[
            "mythic-edge-role-pool/scripts/test_check_pool_plan.py"
        ]["sha256"] = (
            "8ca31a9276d5bb092686010968dce8d7e98715a15d4a581616ec60c06a2b4243"
        )
        predecessor = sorted(predecessor, key=lambda row: row["path"])
        self.assertEqual(len(predecessor), ACCEPTED_PRE_APP_SERVER_MANIFEST_FILE_COUNT)
        self.assertEqual(len(stage3.canonical_bytes(predecessor)), 5416)
        self.assertEqual(
            stage3.canonical_digest(predecessor),
            "2c6e3772fcfbd2eb68618486520d2d309b0594f8a1a7dafd2d3f32fd6ee76bcb",
        )

        predecessor_digests = {row["path"]: row["sha256"] for row in predecessor}
        candidate_digests = {
            row["path"]: row["sha256"] for row in reviewed_candidate
        }
        self.assertEqual(
            set(candidate_digests) - set(predecessor_digests),
            APP_SERVER_ADDED_PATHS,
        )
        self.assertEqual(
            {
                path
                for path in set(candidate_digests) & set(predecessor_digests)
                if candidate_digests[path] != predecessor_digests[path]
            },
            set(REVIEWED_APP_SERVER_MODIFIED_DIGESTS),
        )
        self.assertEqual(
            set(predecessor_digests) - set(candidate_digests),
            set(),
        )
        self.assertEqual(
            {
                path
                for path, digest in reviewed_candidate_by_path.items()
                if digest["sha256"]
                != {row["path"]: row["sha256"] for row in rows}[path]
            },
            set(stage3_pre_edit_digests),
        )

    def test_v5_rebind_v1_lineage_recipe_and_receipt_remain_exact(self) -> None:
        receipt = _validate_v5_rebind_receipt(_embedded_v5_rebind_receipt())
        binding = _v5_rebind_binding(receipt)
        _validate_v5_rebind_binding(binding)

        self.assertEqual(
            V5_REBIND_TARGET_SHA256, V5_REBIND_V2_PREDECESSOR_SHA256
        )
        self.assertNotEqual(
            V5_REBIND_TARGET_SHA256, V5_REBIND_PREDECESSOR_SHA256
        )
        amendment = V5_REBIND_AMENDMENT.read_text(encoding="utf-8")
        self.assertIn(
            "before_sha256=0b3cc179303ddba6ece29492414b7bb942f25cc5d59d317f6c6857c93375a1ea",
            amendment,
        )
        self.assertIn(
            "after_sha256=d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967",
            amendment,
        )

    def test_v5_rebind_receipt_rejects_every_field_and_shape_drift(self) -> None:
        payload = _embedded_v5_rebind_receipt()
        receipt = _validate_v5_rebind_receipt(payload)

        for field in sorted(receipt):
            with self.subTest(field=field):
                changed = copy.deepcopy(receipt)
                if field == "finding_ids":
                    changed[field] = ["EIB-PKG-V5-SYNTHETIC"]
                elif isinstance(changed[field], bool):
                    changed[field] = True
                else:
                    changed[field] = "drift"
                with self.assertRaises(ValueError):
                    _validate_v5_rebind_receipt(_canonical_json_bytes(changed))

        missing = copy.deepcopy(receipt)
        missing.pop("reviewed_at_utc")
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_receipt(_canonical_json_bytes(missing))

        unknown = copy.deepcopy(receipt)
        unknown["unknown"] = False
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_receipt(_canonical_json_bytes(unknown))

        duplicate = (
            b'{"build_recipe_execution_compatibility_claimed":false,' + payload[1:]
        )
        with self.assertRaisesRegex(ValueError, "duplicate receipt key"):
            _validate_v5_rebind_receipt(duplicate)

        reordered = dict(reversed(list(receipt.items())))
        reordered_payload = (
            json.dumps(reordered, ensure_ascii=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "not canonical"):
            _validate_v5_rebind_receipt(reordered_payload)

        malformed_payloads = {
            "missing_final_lf": payload[:-1],
            "extra_final_lf": payload + b"\n",
            "crlf": payload[:-1] + b"\r\n",
            "invalid_utf8": b"\xff\n",
            "invalid_json": b"{\n",
        }
        for label, malformed_payload in malformed_payloads.items():
            with self.subTest(label=label), self.assertRaises(ValueError):
                _validate_v5_rebind_receipt(malformed_payload)

    def test_v5_rebind_rejects_each_closed_binding_drift(self) -> None:
        receipt = _validate_v5_rebind_receipt(_embedded_v5_rebind_receipt())
        binding = _v5_rebind_binding(receipt)
        _validate_v5_rebind_binding(binding)

        for field in sorted(binding):
            with self.subTest(field=field):
                changed = copy.deepcopy(binding)
                value = changed[field]
                if isinstance(value, int):
                    changed[field] = value + 1
                elif isinstance(value, tuple):
                    changed[field] = (*value, "drift")
                else:
                    changed[field] = "drift"
                with self.assertRaisesRegex(ValueError, "binding drift"):
                    _validate_v5_rebind_binding(changed)

    def test_v5_rebind_v2_receipt_static_preflight_and_lineage_are_exact(
        self,
    ) -> None:
        v1_receipt = _validate_v5_rebind_receipt(_embedded_v5_rebind_receipt())
        v2_receipt = _validate_v5_rebind_v2_receipt(
            _embedded_v5_rebind_v2_receipt()
        )
        _validate_v5_rebind_binding(_v5_rebind_binding(v1_receipt))
        v2_binding = _v5_rebind_v2_binding(v2_receipt)
        _validate_v5_rebind_v2_binding(v2_binding)

        self.assertEqual(
            V5_REBIND_V2_TARGET_SHA256, V5_REBIND_V3_PREDECESSOR_SHA256
        )
        self.assertNotEqual(V5_SUCCESSOR_SHA256, V5_REBIND_V2_TARGET_SHA256)
        self.assertEqual(
            v2_binding["target_sha256"],
            V5_REBIND_V2_TARGET_SHA256,
        )
        self.assertEqual(len(PRE_APP_SERVER_ALLOWED_ADDED_PATHS), 7)
        self.assertEqual(len(ALLOWED_MODIFIED_PATHS), 13)
        self.assertEqual(len(PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS), 3)

    def test_v5_rebind_v2_receipt_rejects_every_field_and_shape_drift(
        self,
    ) -> None:
        payload = _embedded_v5_rebind_v2_receipt()
        receipt = _validate_v5_rebind_v2_receipt(payload)
        for field in sorted(receipt):
            with self.subTest(field=field):
                changed = copy.deepcopy(receipt)
                changed[field] = _drift_value(changed[field])
                with self.assertRaises(ValueError):
                    _validate_v5_rebind_v2_receipt(
                        _canonical_json_bytes(changed)
                    )

        missing = copy.deepcopy(receipt)
        missing.pop("reviewed_at_utc")
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v2_receipt(_canonical_json_bytes(missing))
        unknown = copy.deepcopy(receipt)
        unknown["unknown"] = False
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v2_receipt(_canonical_json_bytes(unknown))
        duplicate = (
            b'{"build_recipe_execution_compatibility_claimed":false,' + payload[1:]
        )
        with self.assertRaisesRegex(ValueError, "duplicate receipt key"):
            _validate_v5_rebind_v2_receipt(duplicate)
        reordered = dict(reversed(list(receipt.items())))
        reordered_payload = (
            json.dumps(reordered, ensure_ascii=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "not canonical"):
            _validate_v5_rebind_v2_receipt(reordered_payload)

        malformed_payloads = {
            "missing_final_lf": payload[:-1],
            "extra_final_lf": payload + b"\n",
            "crlf": payload[:-1] + b"\r\n",
            "invalid_utf8": b"\xff\n",
            "invalid_json": b"{\n",
        }
        for label, malformed_payload in malformed_payloads.items():
            with self.subTest(label=label), self.assertRaises(ValueError):
                _validate_v5_rebind_v2_receipt(malformed_payload)

    def test_v5_rebind_v2_rejects_each_closed_binding_drift(self) -> None:
        receipt = _validate_v5_rebind_v2_receipt(
            _embedded_v5_rebind_v2_receipt()
        )
        binding = _v5_rebind_v2_binding(receipt)
        _validate_v5_rebind_v2_binding(binding)

        for field in sorted(binding):
            with self.subTest(field=field):
                changed = copy.deepcopy(binding)
                changed[field] = _drift_value(changed[field])
                with self.assertRaisesRegex(ValueError, "v2 binding drift"):
                    _validate_v5_rebind_v2_binding(changed)
        static_preflight = binding["static_preflight"]
        self.assertIsInstance(static_preflight, dict)
        for field in sorted(static_preflight):
            with self.subTest(static_preflight_field=field):
                changed = copy.deepcopy(binding)
                changed_static = changed["static_preflight"]
                self.assertIsInstance(changed_static, dict)
                changed_static[field] = "drift"
                with self.assertRaisesRegex(ValueError, "v2 binding drift"):
                    _validate_v5_rebind_v2_binding(changed)

    def test_v5_rebind_v2_static_vectors_reject_digest_and_shape_drift(
        self,
    ) -> None:
        self.assertEqual(
            _validate_v5_rebind_v2_static_vectors(),
            V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS,
        )
        values = _contract_json_values()
        matrix_names = {
            "timestamp_floor": "timestamp_floor_matrix_counts_sha256",
            "failure": "failure_matrix_counts_sha256",
            "binding_projection": "projection_matrix_counts_sha256",
        }
        for matrix_id, digest_name in matrix_names.items():
            matrix = next(
                value
                for _, value in values
                if isinstance(value, dict) and value.get("matrix_id") == matrix_id
            )
            _validate_v5_matrix_counts(matrix)
            for field in sorted(matrix):
                with self.subTest(matrix=matrix_id, field=field):
                    changed = copy.deepcopy(matrix)
                    changed[field] = _drift_value(changed[field])
                    self.assertNotEqual(
                        _json_sha256(changed),
                        V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS[digest_name],
                    )

        operation_matrix = _v5_candidate_operation_matrix()
        self.assertEqual(
            _json_sha256(operation_matrix),
            V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS[
                "candidate_operation_matrix_sha256"
            ],
        )
        for field in sorted(operation_matrix):
            with self.subTest(operation_matrix_field=field):
                changed = copy.deepcopy(operation_matrix)
                changed[field] = _drift_value(changed[field])
                self.assertNotEqual(
                    _json_sha256(changed),
                    V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS[
                        "candidate_operation_matrix_sha256"
                    ],
                )

    def test_v5_rebind_v2_future_activation_vector_is_immutable_evidence(
        self,
    ) -> None:
        vector = copy.deepcopy(V5_REBIND_V2_FUTURE_ACTIVATION_REQUIREMENTS)
        self.assertEqual(len(vector["requirements"]), 68)
        self.assertEqual(
            _json_sha256(vector),
            V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS[
                "future_activation_requirements_sha256"
            ],
        )
        self.assertFalse(
            any(
                isinstance(value, dict)
                and value.get("schema") == vector["schema"]
                for _, value in _contract_json_values()
            )
        )
        mutations = {
            "missing": vector["requirements"][:-1],
            "extra": [*vector["requirements"], "unknown|string|literal:drift"],
            "reordered": list(reversed(vector["requirements"])),
            "changed": ["drift", *vector["requirements"][1:]],
        }
        for label, requirements in mutations.items():
            with self.subTest(label=label):
                changed = copy.deepcopy(vector)
                changed["requirements"] = requirements
                self.assertNotEqual(
                    _json_sha256(changed),
                    V5_REBIND_V2_STATIC_PREFLIGHT_DIGESTS[
                        "future_activation_requirements_sha256"
                    ],
                )

    def test_v5_rebind_v3_review_oracle_and_history_are_exact(self) -> None:
        evidence = _validate_v5_rebind_v3_review_evidence(
            _embedded_v5_rebind_v3_review_evidence()
        )
        binding = _v5_rebind_v3_binding(evidence)
        _validate_v5_rebind_v3_binding(binding)
        self.assertEqual(binding["target_sha256"], V5_REBIND_V3_TARGET_SHA256)
        self.assertNotEqual(V5_SUCCESSOR_SHA256, V5_REBIND_V3_TARGET_SHA256)
        self.assertNotEqual(
            V5_REBIND_V3_TARGET_SHA256,
            V5_REBIND_V3_PREDECESSOR_SHA256,
        )
        self.assertEqual(evidence["oracle_tuple_count"], 768)
        self.assertEqual(evidence["oracle_outcome_counts"], [1, 1, 45, 4, 717])
        self.assertEqual(evidence["oracle_sha256"], V5_REBIND_V3_ORACLE_SHA256)
        self.assertIs(evidence["live_ready"], False)
        self.assertIs(evidence["manifest_rebind_authorized"], False)
        self.assertIs(evidence["stage_advancement_authorized"], False)

    def test_v5_rebind_v3_review_evidence_rejects_every_drift(self) -> None:
        payload = _embedded_v5_rebind_v3_review_evidence()
        evidence = _validate_v5_rebind_v3_review_evidence(payload)
        for field in sorted(evidence):
            with self.subTest(field=field):
                changed = copy.deepcopy(evidence)
                changed[field] = _drift_value(changed[field])
                with self.assertRaisesRegex(ValueError, "binding drift"):
                    _validate_v5_rebind_v3_review_evidence(
                        _canonical_json_bytes(changed)
                    )
        malformed = {
            "missing_lf": payload[:-1],
            "extra_lf": payload + b"\n",
            "crlf": payload[:-1] + b"\r\n",
            "duplicate_key": b'{"contract_review_status":"drift",' + payload[1:],
        }
        for label, changed_payload in malformed.items():
            with self.subTest(label=label), self.assertRaises(ValueError):
                _validate_v5_rebind_v3_review_evidence(changed_payload)

    def test_v5_rebind_v3_rejects_each_closed_binding_drift(self) -> None:
        evidence = _validate_v5_rebind_v3_review_evidence(
            _embedded_v5_rebind_v3_review_evidence()
        )
        binding = _v5_rebind_v3_binding(evidence)
        _validate_v5_rebind_v3_binding(binding)
        for field in sorted(binding):
            with self.subTest(field=field):
                changed = copy.deepcopy(binding)
                changed[field] = _drift_value(changed[field])
                with self.assertRaisesRegex(ValueError, "v3 binding drift"):
                    _validate_v5_rebind_v3_binding(changed)

    def test_v5_rebind_v3_failure_paths_restore_synthetic_predecessor(self) -> None:
        evidence = _validate_v5_rebind_v3_review_evidence(
            _embedded_v5_rebind_v3_review_evidence()
        )
        binding = _v5_rebind_v3_binding(evidence)
        predecessor_state = {
            **PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS,
            V5_SUCCESSOR_MANIFEST_PATH: V5_REBIND_V3_PREDECESSOR_SHA256,
        }

        prewrite_state = copy.deepcopy(predecessor_state)
        invalid_binding = copy.deepcopy(binding)
        invalid_binding["oracle_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "v3 binding drift"):
            _validate_v5_rebind_v3_binding(invalid_binding)
        self.assertEqual(prewrite_state, predecessor_state)

        postwrite_state = copy.deepcopy(predecessor_state)
        original_state = copy.deepcopy(postwrite_state)
        _validate_v5_rebind_v3_binding(binding)
        try:
            postwrite_state[V5_SUCCESSOR_MANIFEST_PATH] = V5_REBIND_V3_TARGET_SHA256
            raise ValueError("synthetic post-write validation failure")
        except ValueError:
            postwrite_state = original_state
        self.assertEqual(postwrite_state, predecessor_state)

    def test_v5_rebind_v4_historical_receipt_and_static_preflight_are_exact(
        self,
    ) -> None:
        evidence = _validate_v5_rebind_v3_review_evidence(
            _embedded_v5_rebind_v3_review_evidence()
        )
        _validate_v5_rebind_v3_binding(_v5_rebind_v3_binding(evidence))

        receipt = _validate_v5_rebind_v4_receipt(
            _embedded_v5_rebind_v4_receipt()
        )
        _validate_v5_rebind_v4_binding(_v5_rebind_v4_binding(receipt))

        predecessor = _v5_rebind_v4_static_preflight(
            V5_REBIND_V3_AMENDMENT_SHA256
        )
        successor = _v5_rebind_v4_static_preflight(
            V5_REBIND_V4_AMENDMENT_SHA256
        )
        self.assertEqual(
            predecessor["static_preflight_sha256"],
            V5_CURRENT_RECIPE_PREDECESSOR_STATIC_PREFLIGHT_SHA256,
        )
        self.assertEqual(
            successor["static_preflight_sha256"],
            V5_CURRENT_RECIPE_SUCCESSOR_STATIC_PREFLIGHT_SHA256,
        )
        for field in sorted(predecessor):
            if field not in {
                "manifest_rebind_amendment_sha256",
                "static_preflight_sha256",
            }:
                self.assertEqual(predecessor[field], successor[field], field)

        self.assertEqual(
            _v5_rebind_v4_binding(receipt)["v5_contract_sha256_after"],
            V5_REBIND_V3_TARGET_SHA256,
        )

    def test_v5_rebind_v4_receipt_rejects_every_field_and_shape_drift(
        self,
    ) -> None:
        payload = _embedded_v5_rebind_v4_receipt()
        receipt = _validate_v5_rebind_v4_receipt(payload)
        for field in sorted(receipt):
            with self.subTest(field=field):
                changed = copy.deepcopy(receipt)
                changed[field] = _drift_value(changed[field])
                with self.assertRaises(ValueError):
                    _validate_v5_rebind_v4_receipt(
                        _canonical_json_bytes(changed)
                    )

        for label, historical in {
            "v1": _embedded_v5_rebind_receipt(),
            "v2": _embedded_v5_rebind_v2_receipt(),
        }.items():
            with self.subTest(historical=label), self.assertRaises(ValueError):
                _validate_v5_rebind_v4_receipt(historical)

        missing = copy.deepcopy(receipt)
        missing.pop("reviewed_at_utc")
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v4_receipt(_canonical_json_bytes(missing))
        unknown = copy.deepcopy(receipt)
        unknown["unknown"] = False
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v4_receipt(_canonical_json_bytes(unknown))
        duplicate = (
            b'{"build_recipe_execution_compatibility_claimed":false,' + payload[1:]
        )
        with self.assertRaisesRegex(ValueError, "duplicate receipt key"):
            _validate_v5_rebind_v4_receipt(duplicate)
        reordered = dict(reversed(list(receipt.items())))
        reordered_payload = (
            json.dumps(reordered, ensure_ascii=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "not canonical"):
            _validate_v5_rebind_v4_receipt(reordered_payload)
        for label, malformed in {
            "missing_final_lf": payload[:-1],
            "extra_final_lf": payload + b"\n",
            "crlf": payload[:-1] + b"\r\n",
            "invalid_utf8": b"\xff\n",
            "invalid_json": b"{\n",
        }.items():
            with self.subTest(malformed=label), self.assertRaises(ValueError):
                _validate_v5_rebind_v4_receipt(malformed)

    def test_v5_rebind_v4_rejects_each_closed_binding_drift(self) -> None:
        receipt = _validate_v5_rebind_v4_receipt(
            _embedded_v5_rebind_v4_receipt()
        )
        binding = _v5_rebind_v4_binding(receipt)
        _validate_v5_rebind_v4_binding(binding)
        for field in sorted(binding):
            with self.subTest(field=field):
                changed = copy.deepcopy(binding)
                changed[field] = _drift_value(changed[field])
                with self.assertRaisesRegex(ValueError, "v4 binding drift"):
                    _validate_v5_rebind_v4_binding(changed)

    def test_v5_rebind_v4_failure_preserves_manifest_and_authority(self) -> None:
        rows = current_skill_manifest()
        changed_rows = copy.deepcopy(rows)
        amendment_row = next(
            row
            for row in changed_rows
            if row["path"] == STAGE3_PLANNING_MANIFEST_PATH
        )
        amendment_row["sha256"] = "0" * 64
        with mock.patch.object(
            stage3,
            "current_skill_manifest",
            return_value=changed_rows,
        ), self.assertRaisesRegex(
            stage3.ManifestTransitionError,
            "amendment digest",
        ):
            stage3.expected_contract_transition()

        receipt = _validate_v5_rebind_v4_receipt(
            _embedded_v5_rebind_v4_receipt()
        )
        binding = _v5_rebind_v4_binding(receipt)
        predecessor = {
            "manifest_file_count": 37,
            "manifest_v5_sha256": V5_REBIND_V3_TARGET_SHA256,
            "candidate_preparation_authorized": False,
            "live_ready": False,
        }
        observed = copy.deepcopy(predecessor)
        invalid = copy.deepcopy(binding)
        invalid["review_receipt_digest"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "v4 binding drift"):
            _validate_v5_rebind_v4_binding(invalid)
        self.assertEqual(observed, predecessor)

    def test_v5_rebind_v5_review_static_preflight_and_manifest_are_exact(
        self,
    ) -> None:
        evidence = _validate_v5_rebind_v5_review_evidence(
            _embedded_v5_rebind_v5_review_evidence()
        )
        binding = _v5_rebind_v5_binding(evidence)
        _validate_v5_rebind_v5_binding(binding)

        predecessor = _v5_rebind_v5_static_preflight(
            V5_REBIND_V5_PREDECESSOR_SHA256,
            V5_REBIND_V4_AMENDMENT_SHA256,
        )
        successor = _v5_rebind_v5_static_preflight(
            V5_REBIND_V5_TARGET_SHA256,
            V5_REBIND_V5_AMENDMENT_SHA256,
        )
        self.assertEqual(
            predecessor["static_preflight_sha256"],
            V5_BUILD_RECONCILIATION_PREDECESSOR_STATIC_PREFLIGHT_SHA256,
        )
        self.assertEqual(
            successor["static_preflight_sha256"],
            V5_BUILD_RECONCILIATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256,
        )
        changed_fields = {
            "contract_sha256",
            "manifest_rebind_amendment_sha256",
            "manifest_rebind_to_sha256",
            "static_preflight_sha256",
        }
        for field in sorted(set(predecessor) - changed_fields):
            self.assertEqual(predecessor[field], successor[field], field)

        self.assertEqual(
            binding["amendment_sha256"],
            V5_REBIND_V5_AMENDMENT_SHA256,
        )
        self.assertEqual(
            binding["contract_sha256"],
            V5_REBIND_V5_TARGET_SHA256,
        )
        self.assertEqual(
            dict(binding["pinned_successor_digests"])[V5_SUCCESSOR_MANIFEST_PATH],
            V5_REBIND_V5_TARGET_SHA256,
        )
        self.assertTrue(all(value is False for value in binding["false_authority"].values()))
        self.assertEqual(binding["recipe_v1_status"], "immutable_retired_future_execution_blocked")
        self.assertIs(binding["recipe_v2_defined"], False)

    def test_v5_rebind_v5_review_evidence_rejects_every_drift(self) -> None:
        payload = _embedded_v5_rebind_v5_review_evidence()
        evidence = _validate_v5_rebind_v5_review_evidence(payload)
        for field in sorted(evidence):
            with self.subTest(field=field):
                changed = copy.deepcopy(evidence)
                changed[field] = _drift_value(changed[field])
                with self.assertRaises(ValueError):
                    _validate_v5_rebind_v5_review_evidence(
                        _canonical_json_bytes(changed)
                    )

        missing = copy.deepcopy(evidence)
        missing.pop("source_sha256")
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v5_review_evidence(
                _canonical_json_bytes(missing)
            )
        unknown = copy.deepcopy(evidence)
        unknown["unknown"] = False
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v5_review_evidence(
                _canonical_json_bytes(unknown)
            )
        duplicate = b'{"build_environment_root_cause":"drift",' + payload[1:]
        with self.assertRaisesRegex(ValueError, "duplicate receipt key"):
            _validate_v5_rebind_v5_review_evidence(duplicate)
        reordered = dict(reversed(list(evidence.items())))
        reordered_payload = (
            json.dumps(reordered, ensure_ascii=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "not canonical"):
            _validate_v5_rebind_v5_review_evidence(reordered_payload)
        for label, malformed in {
            "missing_final_lf": payload[:-1],
            "extra_final_lf": payload + b"\n",
            "crlf": payload[:-1] + b"\r\n",
            "invalid_utf8": b"\xff\n",
            "invalid_json": b"{\n",
        }.items():
            with self.subTest(malformed=label), self.assertRaises(ValueError):
                _validate_v5_rebind_v5_review_evidence(malformed)

    def test_v5_rebind_v5_rejects_each_closed_binding_drift(self) -> None:
        evidence = _validate_v5_rebind_v5_review_evidence(
            _embedded_v5_rebind_v5_review_evidence()
        )
        binding = _v5_rebind_v5_binding(evidence)
        _validate_v5_rebind_v5_binding(binding)
        for field in sorted(binding):
            with self.subTest(field=field):
                changed = copy.deepcopy(binding)
                changed[field] = _drift_value(changed[field])
                with self.assertRaisesRegex(ValueError, "v5 binding drift"):
                    _validate_v5_rebind_v5_binding(changed)

    def test_v5_rebind_v5_failure_rolls_back_and_retains_no_authority(self) -> None:
        rows = current_skill_manifest()
        before = copy.deepcopy(rows)
        for label, digest in {
            "predecessor": V5_REBIND_V5_PREDECESSOR_SHA256,
            "wrong_target": "0" * 64,
        }.items():
            with self.subTest(label=label):
                changed_rows = copy.deepcopy(rows)
                next(
                    row
                    for row in changed_rows
                    if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
                )["sha256"] = digest
                self.assert_manifest_rows_rejected(
                    changed_rows,
                    "v5 successor digest",
                )
                self.assertEqual(current_skill_manifest(), before)

        evidence = _validate_v5_rebind_v5_review_evidence(
            _embedded_v5_rebind_v5_review_evidence()
        )
        invalid = _v5_rebind_v5_binding(evidence)
        invalid["recipe_v1_status"] = "complete"
        with self.assertRaisesRegex(ValueError, "v5 binding drift"):
            _validate_v5_rebind_v5_binding(invalid)
        self.assertEqual(current_skill_manifest(), before)

    def test_v5_rebind_v6_review_static_preflight_and_manifest_are_exact(
        self,
    ) -> None:
        historical_evidence = _validate_v5_rebind_v5_review_evidence(
            _embedded_v5_rebind_v5_review_evidence()
        )
        _validate_v5_rebind_v5_binding(
            _v5_rebind_v5_binding(historical_evidence)
        )

        evidence = _validate_v5_rebind_v6_review_evidence(
            _embedded_v5_rebind_v6_review_evidence()
        )
        matrix = _validate_v5_characterization_synthetic_matrix(
            _embedded_v5_characterization_synthetic_matrix()
        )
        binding = _v5_rebind_v6_binding(evidence, matrix)
        _validate_v5_rebind_v6_binding(binding)

        predecessor = _v5_rebind_v6_static_preflight(
            V5_REBIND_V6_PREDECESSOR_SHA256,
            V5_REBIND_V5_AMENDMENT_SHA256,
        )
        successor = _v5_rebind_v6_static_preflight(
            V5_REBIND_V6_TARGET_SHA256,
            V5_REBIND_V6_AMENDMENT_SHA256,
        )
        self.assertEqual(
            predecessor["static_preflight_sha256"],
            V5_CHARACTERIZATION_PREDECESSOR_STATIC_PREFLIGHT_SHA256,
        )
        self.assertEqual(
            successor["static_preflight_sha256"],
            V5_CHARACTERIZATION_SUCCESSOR_STATIC_PREFLIGHT_SHA256,
        )
        changed_fields = {
            "contract_sha256",
            "manifest_rebind_amendment_sha256",
            "manifest_rebind_to_sha256",
            "static_preflight_sha256",
        }
        for field in sorted(set(predecessor) - changed_fields):
            self.assertEqual(predecessor[field], successor[field], field)

        self.assertEqual(
            dict(binding["pinned_successor_digests"])[V5_SUCCESSOR_MANIFEST_PATH],
            V5_REBIND_V6_TARGET_SHA256,
        )
        self.assertNotEqual(V5_REBIND_V6_TARGET_SHA256, V5_SUCCESSOR_SHA256)
        self.assertEqual(binding["characterization_synthetic_case_count"], 36)
        self.assertEqual(binding["characterization_retry_activation_key_count"], 54)
        self.assertEqual(
            binding["characterization_synthetic_review_receipt_key_count"], 16
        )
        self.assertTrue(
            all(value is False for value in binding["false_authority"].values())
        )

    def test_v5_rebind_v6_review_evidence_rejects_every_drift(self) -> None:
        payload = _embedded_v5_rebind_v6_review_evidence()
        evidence = _validate_v5_rebind_v6_review_evidence(payload)
        for field in sorted(evidence):
            with self.subTest(field=field):
                changed = copy.deepcopy(evidence)
                changed[field] = _drift_value(changed[field])
                with self.assertRaises(ValueError):
                    _validate_v5_rebind_v6_review_evidence(
                        _canonical_json_bytes(changed)
                    )

        for parent in ("finding_status", "validation"):
            nested = evidence[parent]
            assert isinstance(nested, dict)
            for field in sorted(nested):
                with self.subTest(parent=parent, field=field):
                    changed = copy.deepcopy(evidence)
                    changed[parent][field] = _drift_value(changed[parent][field])
                    with self.assertRaises(ValueError):
                        _validate_v5_rebind_v6_review_evidence(
                            _canonical_json_bytes(changed)
                        )

        missing = copy.deepcopy(evidence)
        missing.pop("contract_sha256")
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v6_review_evidence(_canonical_json_bytes(missing))
        unknown = copy.deepcopy(evidence)
        unknown["unknown"] = False
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v6_review_evidence(_canonical_json_bytes(unknown))
        duplicate = b'{"canary_authorized":true,' + payload[1:]
        with self.assertRaisesRegex(ValueError, "duplicate receipt key"):
            _validate_v5_rebind_v6_review_evidence(duplicate)
        reordered = dict(reversed(list(evidence.items())))
        reordered_payload = (
            json.dumps(reordered, ensure_ascii=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "not canonical"):
            _validate_v5_rebind_v6_review_evidence(reordered_payload)
        for label, malformed in {
            "missing_final_lf": payload[:-1],
            "extra_final_lf": payload + b"\n",
            "crlf": payload[:-1] + b"\r\n",
            "invalid_utf8": b"\xff\n",
            "invalid_json": b"{\n",
        }.items():
            with self.subTest(malformed=label), self.assertRaises(ValueError):
                _validate_v5_rebind_v6_review_evidence(malformed)

    def test_v5_rebind_v6_synthetic_matrix_rejects_every_drift(self) -> None:
        payload = _embedded_v5_characterization_synthetic_matrix()
        matrix = _validate_v5_characterization_synthetic_matrix(payload)
        for field in sorted(matrix):
            with self.subTest(field=field):
                changed = copy.deepcopy(matrix)
                changed[field] = _drift_value(changed[field])
                with self.assertRaises(ValueError):
                    _validate_v5_characterization_synthetic_matrix(
                        _canonical_json_bytes(changed)
                    )

        changed = copy.deepcopy(matrix)
        changed["rows"][0][2] = "drift"
        with self.assertRaisesRegex(ValueError, "digest drift"):
            _validate_v5_characterization_synthetic_matrix(
                _canonical_json_bytes(changed)
            )
        duplicate = b'{"case_count":36,' + payload[1:]
        with self.assertRaisesRegex(ValueError, "duplicate receipt key"):
            _validate_v5_characterization_synthetic_matrix(duplicate)
        reordered = dict(reversed(list(matrix.items())))
        reordered_payload = (
            json.dumps(reordered, ensure_ascii=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "not canonical"):
            _validate_v5_characterization_synthetic_matrix(reordered_payload)

    def test_v5_rebind_v6_binding_drift_rolls_back_without_authority(self) -> None:
        evidence = _validate_v5_rebind_v6_review_evidence(
            _embedded_v5_rebind_v6_review_evidence()
        )
        matrix = _validate_v5_characterization_synthetic_matrix(
            _embedded_v5_characterization_synthetic_matrix()
        )
        binding = _v5_rebind_v6_binding(evidence, matrix)
        _validate_v5_rebind_v6_binding(binding)
        for field in sorted(binding):
            with self.subTest(field=field):
                changed = copy.deepcopy(binding)
                changed[field] = _drift_value(changed[field])
                with self.assertRaisesRegex(ValueError, "v6 binding drift"):
                    _validate_v5_rebind_v6_binding(changed)

        rows = current_skill_manifest()
        before = copy.deepcopy(rows)
        for label, digest in {
            "predecessor": V5_REBIND_V6_PREDECESSOR_SHA256,
            "wrong_target": "0" * 64,
        }.items():
            with self.subTest(label=label):
                changed_rows = copy.deepcopy(rows)
                next(
                    row
                    for row in changed_rows
                    if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
                )["sha256"] = digest
                self.assert_manifest_rows_rejected(
                    changed_rows,
                    "v5 successor digest",
                )
                self.assertEqual(current_skill_manifest(), before)

        changed_rows = copy.deepcopy(rows)
        next(
            row
            for row in changed_rows
            if row["path"] == STAGE3_PLANNING_MANIFEST_PATH
        )["sha256"] = V5_REBIND_V5_AMENDMENT_SHA256
        self.assert_manifest_rows_rejected(
            changed_rows,
            "amendment digest",
        )
        self.assertEqual(current_skill_manifest(), before)
        self.assertTrue(
            all(value is False for value in binding["false_authority"].values())
        )

    def test_v5_rebind_v7_review_matrices_oracle_and_manifest_are_exact(
        self,
    ) -> None:
        historical_evidence = _validate_v5_rebind_v6_review_evidence(
            _embedded_v5_rebind_v6_review_evidence()
        )
        historical_matrix = _validate_v5_characterization_synthetic_matrix(
            _embedded_v5_characterization_synthetic_matrix()
        )
        _validate_v5_rebind_v6_binding(
            _v5_rebind_v6_binding(historical_evidence, historical_matrix)
        )

        evidence = _validate_v5_rebind_v7_review_evidence(
            _embedded_v5_rebind_v7_review_evidence()
        )
        core_matrix = _validate_v5_characterization_synthetic_matrix(
            _embedded_v5_characterization_synthetic_matrix()
        )
        adapter_matrix = _validate_v5_characterization_adapter_matrix(
            _embedded_v5_characterization_adapter_matrix()
        )
        oracle = _validate_v5_rebind_v7_outer_oracle(
            _v5_rebind_v7_outer_oracle_rows()
        )
        binding = _v5_rebind_v7_binding(
            evidence,
            core_matrix,
            adapter_matrix,
            oracle,
        )
        _validate_v5_rebind_v7_binding(binding)

        predecessor = _v5_rebind_v7_static_preflight(
            V5_REBIND_V7_PREDECESSOR_SHA256,
            V5_REBIND_V6_AMENDMENT_SHA256,
        )
        successor = _v5_rebind_v7_static_preflight(
            V5_REBIND_V7_TARGET_SHA256,
            V5_REBIND_V7_AMENDMENT_SHA256,
        )
        self.assertEqual(
            predecessor["static_preflight_sha256"],
            V5_REAL_SOURCE_ADAPTER_PREDECESSOR_STATIC_PREFLIGHT_SHA256,
        )
        self.assertEqual(
            successor["static_preflight_sha256"],
            V5_REAL_SOURCE_ADAPTER_SUCCESSOR_STATIC_PREFLIGHT_SHA256,
        )
        changed_fields = {
            "contract_sha256",
            "manifest_rebind_amendment_sha256",
            "manifest_rebind_to_sha256",
            "static_preflight_sha256",
        }
        for field in sorted(set(predecessor) - changed_fields):
            self.assertEqual(predecessor[field], successor[field], field)

        rows = current_skill_manifest()
        self.assertEqual(len(rows), 39)
        self.assertEqual(len({row["path"] for row in rows}), 39)
        current_by_path = {row["path"]: row["sha256"] for row in rows}
        self.assertEqual(
            current_by_path[STAGE3_PLANNING_MANIFEST_PATH],
            V5_REBIND_V7_AMENDMENT_SHA256,
        )
        self.assertEqual(
            current_by_path[V5_SUCCESSOR_MANIFEST_PATH],
            V5_REBIND_V7_TARGET_SHA256,
        )
        transition = expected_contract_transition()
        self.assertEqual(transition["current_manifest_file_count"], 39)
        self.assertEqual(
            [
                row
                for row in transition["change_set"]
                if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
            ],
            [
                {
                    "path": V5_SUCCESSOR_MANIFEST_PATH,
                    "change_kind": "added",
                    "before_sha256": None,
                    "after_sha256": V5_REBIND_V7_TARGET_SHA256,
                }
            ],
        )
        self.assertEqual(binding["characterization_activation_key_count"], 64)
        self.assertEqual(
            binding["characterization_controller_request_key_count"], 10
        )
        self.assertEqual(binding["characterization_child_result_key_count"], 13)
        self.assertEqual(binding["characterization_result_key_count"], 20)
        self.assertEqual(binding["characterization_attempt_handoff_key_count"], 27)
        self.assertEqual(binding["characterization_program_bundle_key_count"], 18)
        self.assertEqual(binding["characterization_core_case_count"], 36)
        self.assertEqual(binding["characterization_adapter_case_count"], 37)
        self.assertEqual(binding["characterization_outer_oracle_tuple_count"], 15360)
        self.assertEqual(binding["characterization_outer_oracle_accepted_count"], 3)
        self.assertEqual(
            binding["characterization_outer_oracle_blocked_before_start_count"],
            2,
        )
        self.assertEqual(
            binding["characterization_outer_oracle_blocked_after_start_count"],
            157,
        )
        self.assertEqual(
            binding["characterization_outer_oracle_cleanup_unknown_count"],
            15198,
        )
        self.assertEqual(binding["characterization_bundle_review_key_count"], 29)
        self.assertTrue(
            all(value is False for value in binding["false_authority"].values())
        )

    def test_v5_rebind_v7_review_and_adapter_matrix_reject_every_drift(
        self,
    ) -> None:
        review_payload = _embedded_v5_rebind_v7_review_evidence()
        evidence = _validate_v5_rebind_v7_review_evidence(review_payload)
        for field in sorted(evidence):
            with self.subTest(review_field=field):
                changed = copy.deepcopy(evidence)
                changed[field] = _drift_value(changed[field])
                with self.assertRaises(ValueError):
                    _validate_v5_rebind_v7_review_evidence(
                        _canonical_json_bytes(changed)
                    )
        changed = copy.deepcopy(evidence)
        changed["finding_status"]["EIB-PKG-V5-ADAPTER-E-001"] = "drift"
        with self.assertRaisesRegex(ValueError, "binding drift"):
            _validate_v5_rebind_v7_review_evidence(_canonical_json_bytes(changed))
        missing = copy.deepcopy(evidence)
        missing.pop("contract_sha256")
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v7_review_evidence(_canonical_json_bytes(missing))
        extra = copy.deepcopy(evidence)
        extra["unknown"] = False
        with self.assertRaisesRegex(ValueError, "key set"):
            _validate_v5_rebind_v7_review_evidence(_canonical_json_bytes(extra))
        duplicate = b'{"activation_creation_authorized":true,' + review_payload[1:]
        with self.assertRaisesRegex(ValueError, "duplicate receipt key"):
            _validate_v5_rebind_v7_review_evidence(duplicate)
        reordered = dict(reversed(list(evidence.items())))
        reordered_payload = (
            json.dumps(reordered, ensure_ascii=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "not canonical"):
            _validate_v5_rebind_v7_review_evidence(reordered_payload)

        matrix_payload = _embedded_v5_characterization_adapter_matrix()
        matrix = _validate_v5_characterization_adapter_matrix(matrix_payload)
        for field in sorted(matrix):
            with self.subTest(matrix_field=field):
                changed = copy.deepcopy(matrix)
                changed[field] = _drift_value(changed[field])
                with self.assertRaises(ValueError):
                    _validate_v5_characterization_adapter_matrix(
                        _canonical_json_bytes(changed)
                    )
        changed = copy.deepcopy(matrix)
        changed["rows"][0][2] = "drift"
        with self.assertRaisesRegex(ValueError, "digest drift"):
            _validate_v5_characterization_adapter_matrix(
                _canonical_json_bytes(changed)
            )
        changed = copy.deepcopy(matrix)
        changed["rows"][0], changed["rows"][1] = (
            changed["rows"][1],
            changed["rows"][0],
        )
        with self.assertRaisesRegex(ValueError, "row-id or order drift"):
            _validate_v5_characterization_adapter_matrix(
                _canonical_json_bytes(changed)
            )
        duplicate = b'{"case_count":37,' + matrix_payload[1:]
        with self.assertRaisesRegex(ValueError, "duplicate receipt key"):
            _validate_v5_characterization_adapter_matrix(duplicate)

    def test_v5_rebind_v7_outer_oracle_is_exhaustive_and_fail_closed(
        self,
    ) -> None:
        rows = _v5_rebind_v7_outer_oracle_rows()
        summary = _validate_v5_rebind_v7_outer_oracle(rows)
        self.assertEqual(summary["tuple_count"], 15360)
        self.assertEqual(summary["handoff_counts"], V5_REBIND_V7_HANDOFF_COUNTS)
        self.assertEqual(
            summary["outer_failure_counts"],
            V5_REBIND_V7_OUTER_FAILURE_COUNTS,
        )
        self.assertEqual(
            sum(V5_REBIND_V7_HANDOFF_COUNTS.values()),
            15360,
        )
        self.assertEqual(
            sum(V5_REBIND_V7_OUTER_FAILURE_COUNTS.values()),
            15360,
        )
        self.assertEqual(
            len({row["observations"] for row in rows}),
            15360,
        )

        with self.assertRaisesRegex(ValueError, "tuple-count drift"):
            _validate_v5_rebind_v7_outer_oracle(rows[:-1])
        duplicate = list(rows)
        duplicate[-1] = copy.deepcopy(duplicate[0])
        with self.assertRaisesRegex(ValueError, "tuple order drift"):
            _validate_v5_rebind_v7_outer_oracle(duplicate)
        multiply_classified = list(rows)
        multiply_classified[0] = copy.deepcopy(multiply_classified[0])
        multiply_classified[0]["handoff_statuses"] = (
            "blocked_before_controller_start",
            "cleanup_state_unknown",
        )
        with self.assertRaisesRegex(ValueError, "exactly one handoff"):
            _validate_v5_rebind_v7_outer_oracle(multiply_classified)
        unclassified = list(rows)
        unclassified[0] = copy.deepcopy(unclassified[0])
        unclassified[0]["outer_failure_codes"] = ()
        with self.assertRaisesRegex(ValueError, "exactly one failure"):
            _validate_v5_rebind_v7_outer_oracle(unclassified)
        changed_classification = list(rows)
        changed_classification[0] = copy.deepcopy(changed_classification[0])
        changed_classification[0]["outer_failure_codes"] = (
            "controller_start_failed",
        )
        with self.assertRaisesRegex(ValueError, "classification drift"):
            _validate_v5_rebind_v7_outer_oracle(changed_classification)
        reordered_dimensions = (
            V5_REBIND_V7_OUTER_DIMENSIONS[1],
            V5_REBIND_V7_OUTER_DIMENSIONS[0],
            *V5_REBIND_V7_OUTER_DIMENSIONS[2:],
        )
        with self.assertRaisesRegex(ValueError, "dimension order"):
            _v5_rebind_v7_outer_oracle_rows(reordered_dimensions)
        with self.assertRaisesRegex(ValueError, "dimension order"):
            _validate_v5_rebind_v7_outer_oracle(rows, reordered_dimensions)

    def test_v5_rebind_v7_binding_drift_rolls_back_without_authority(self) -> None:
        evidence = _validate_v5_rebind_v7_review_evidence(
            _embedded_v5_rebind_v7_review_evidence()
        )
        core_matrix = _validate_v5_characterization_synthetic_matrix(
            _embedded_v5_characterization_synthetic_matrix()
        )
        adapter_matrix = _validate_v5_characterization_adapter_matrix(
            _embedded_v5_characterization_adapter_matrix()
        )
        oracle = _validate_v5_rebind_v7_outer_oracle(
            _v5_rebind_v7_outer_oracle_rows()
        )
        binding = _v5_rebind_v7_binding(
            evidence,
            core_matrix,
            adapter_matrix,
            oracle,
        )
        _validate_v5_rebind_v7_binding(binding)
        for field in sorted(binding):
            with self.subTest(field=field):
                changed = copy.deepcopy(binding)
                changed[field] = _drift_value(changed[field])
                with self.assertRaisesRegex(ValueError, "v7 binding drift"):
                    _validate_v5_rebind_v7_binding(changed)

        rows = current_skill_manifest()
        before = copy.deepcopy(rows)
        for label, digest in {
            "predecessor": V5_REBIND_V7_PREDECESSOR_SHA256,
            "wrong_target": "0" * 64,
        }.items():
            with self.subTest(label=label):
                changed_rows = copy.deepcopy(rows)
                next(
                    row
                    for row in changed_rows
                    if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
                )["sha256"] = digest
                self.assert_manifest_rows_rejected(
                    changed_rows,
                    "v5 successor digest",
                )
                self.assertEqual(current_skill_manifest(), before)

        changed_rows = copy.deepcopy(rows)
        next(
            row
            for row in changed_rows
            if row["path"] == STAGE3_PLANNING_MANIFEST_PATH
        )["sha256"] = V5_REBIND_V6_AMENDMENT_SHA256
        self.assert_manifest_rows_rejected(changed_rows, "amendment digest")
        self.assertEqual(current_skill_manifest(), before)
        self.assertEqual(len(PRE_APP_SERVER_ALLOWED_ADDED_PATHS), 7)
        self.assertEqual(len(ALLOWED_MODIFIED_PATHS), 13)
        self.assertEqual(len(PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS), 3)
        self.assertEqual(
            dict(binding["pinned_successor_digests"])[V5_SUCCESSOR_MANIFEST_PATH],
            V5_REBIND_V7_TARGET_SHA256,
        )
        self.assertTrue(
            all(value is False for value in binding["false_authority"].values())
        )

    def test_manifest_transition_preserves_legacy_sets(self) -> None:
        self.assertEqual(
            PRE_APP_SERVER_ALLOWED_ADDED_PATHS
            - {
                SUCCESSOR_MANIFEST_PATH,
                V4_SUCCESSOR_MANIFEST_PATH,
                V5_SUCCESSOR_MANIFEST_PATH,
            },
            LEGACY_ALLOWED_ADDED_PATHS,
        )
        self.assertEqual(
            PRE_APP_SERVER_ALLOWED_ADDED_PATHS - {V5_SUCCESSOR_MANIFEST_PATH},
            LEGACY_ALLOWED_ADDED_PATHS
            | {SUCCESSOR_MANIFEST_PATH, V4_SUCCESSOR_MANIFEST_PATH},
        )
        self.assertEqual(
            ALLOWED_ADDED_PATHS,
            PRE_APP_SERVER_ALLOWED_ADDED_PATHS | APP_SERVER_ADDED_PATHS,
        )
        self.assertEqual(
            PINNED_SUCCESSOR_DIGESTS,
            {
                **PRE_APP_SERVER_PINNED_SUCCESSOR_DIGESTS,
                APP_SERVER_ADAPTER_MANIFEST_PATH: APP_SERVER_ADAPTER_SHA256,
                APP_SERVER_ADAPTER_TEST_MANIFEST_PATH: (
                    APP_SERVER_ADAPTER_TEST_SHA256
                ),
            },
        )
        self.assertEqual(ALLOWED_MODIFIED_PATHS, LEGACY_ALLOWED_MODIFIED_PATHS)
        self.assertEqual(len(STAGE2_BASELINE_FILES), 30)

    def test_app_server_added_rows_reject_each_membership_and_digest_drift(
        self,
    ) -> None:
        for path in sorted(APP_SERVER_ADDED_PATHS):
            with self.subTest(path=path, drift="missing"):
                rows = [
                    row
                    for row in current_skill_manifest()
                    if row["path"] != path
                ]
                self.assertEqual(len(rows), 38)
                self.assert_manifest_rows_rejected(rows, "file count")

            with self.subTest(path=path, drift="renamed"):
                rows = copy.deepcopy(current_skill_manifest())
                row = next(row for row in rows if row["path"] == path)
                row["path"] = path.replace(".py", "-renamed.py")
                self.assert_manifest_rows_rejected(
                    rows, "unexpected or missing added paths"
                )

            with self.subTest(path=path, drift="case_varied"):
                rows = copy.deepcopy(current_skill_manifest())
                row = next(row for row in rows if row["path"] == path)
                row["path"] = path.replace("trusted_native", "Trusted_Native")
                self.assert_manifest_rows_rejected(
                    rows, "unexpected or missing added paths"
                )

            with self.subTest(path=path, drift="duplicate_exact"):
                rows = copy.deepcopy(current_skill_manifest())
                rows.append(next(row for row in rows if row["path"] == path).copy())
                self.assert_manifest_rows_rejected(rows, "duplicate manifest paths")

            with self.subTest(path=path, drift="duplicate_case_insensitive"):
                rows = copy.deepcopy(current_skill_manifest())
                duplicate = next(row for row in rows if row["path"] == path).copy()
                duplicate["path"] = duplicate["path"].swapcase()
                rows.append(duplicate)
                self.assert_manifest_rows_rejected(rows, "duplicate manifest paths")

            with self.subTest(path=path, drift="digest"):
                rows = copy.deepcopy(current_skill_manifest())
                next(row for row in rows if row["path"] == path)["sha256"] = "0" * 64
                self.assert_manifest_rows_rejected(rows, "app-server adapter digest")

    def test_reviewed_app_server_modified_rows_reject_each_digest_drift(self) -> None:
        for path in sorted(REVIEWED_APP_SERVER_MODIFIED_DIGESTS):
            with self.subTest(path=path):
                rows = copy.deepcopy(current_skill_manifest())
                next(row for row in rows if row["path"] == path)["sha256"] = "0" * 64
                self.assert_manifest_rows_rejected(
                    rows, "reviewed app-server modified digest"
                )

    def test_current_manifest_rows_must_remain_in_ordinal_path_order(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        rows[0], rows[1] = rows[1], rows[0]
        self.assert_manifest_rows_rejected(rows, "ordinal path order")

    def test_app_server_added_paths_reject_case_insensitive_filesystem_duplicates(
        self,
    ) -> None:
        for relative_path in (
            APP_SERVER_ADAPTER_SKILL_RELATIVE_PATH,
            APP_SERVER_ADAPTER_TEST_SKILL_RELATIVE_PATH,
        ):
            with self.subTest(relative_path=relative_path):
                self.assert_pinned_case_representation_rejected(
                    relative_path,
                    duplicate=True,
                    expected_error="duplicate representations",
                )

    def test_app_server_added_paths_reject_case_varied_filesystem_representations(
        self,
    ) -> None:
        for relative_path in (
            APP_SERVER_ADAPTER_SKILL_RELATIVE_PATH,
            APP_SERVER_ADAPTER_TEST_SKILL_RELATIVE_PATH,
        ):
            with self.subTest(relative_path=relative_path):
                self.assert_pinned_case_representation_rejected(
                    relative_path,
                    duplicate=False,
                    expected_error="casing does not match",
                )

    def test_app_server_added_paths_reject_unsafe_metadata_before_target_access(
        self,
    ) -> None:
        unsafe_metadata = {
            "directory": (
                SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0),
                "not an ordinary file",
            ),
            "reparse": (
                SimpleNamespace(
                    st_mode=stat.S_IFREG,
                    st_file_attributes=getattr(
                        stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400
                    ),
                ),
                "reparse point",
            ),
            "symlink": (
                SimpleNamespace(st_mode=stat.S_IFLNK, st_file_attributes=0),
                "reparse point",
            ),
        }
        for relative_path in (
            APP_SERVER_ADAPTER_SKILL_RELATIVE_PATH,
            APP_SERVER_ADAPTER_TEST_SKILL_RELATIVE_PATH,
        ):
            for label, (metadata, expected_error) in unsafe_metadata.items():
                with self.subTest(relative_path=relative_path, label=label):
                    self.assert_pinned_metadata_rejected_before_target_access(
                        relative_path,
                        metadata,
                        expected_error,
                    )

    def test_manifest_transition_rejects_successor_digest_mismatch(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(row for row in rows if row["path"] == SUCCESSOR_MANIFEST_PATH)
        successor["sha256"] = "0" * 64
        self.assert_manifest_rows_rejected(rows, "successor digest")

    def test_manifest_transition_rejects_missing_successor(self) -> None:
        rows = [
            row
            for row in current_skill_manifest()
            if row["path"] != SUCCESSOR_MANIFEST_PATH
        ]
        self.assert_manifest_rows_rejected(rows, "file count")

    def test_manifest_transition_rejects_renamed_successor(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(row for row in rows if row["path"] == SUCCESSOR_MANIFEST_PATH)
        successor["path"] = SUCCESSOR_MANIFEST_PATH.replace(
            ".md", "-renamed.md"
        )
        self.assert_manifest_rows_rejected(rows, "unexpected or missing added paths")

    def test_manifest_transition_rejects_case_varied_successor(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(row for row in rows if row["path"] == SUCCESSOR_MANIFEST_PATH)
        successor["path"] = SUCCESSOR_MANIFEST_PATH.replace(
            "external-isolation", "External-Isolation"
        )
        self.assert_manifest_rows_rejected(rows, "unexpected or missing added paths")

    def test_manifest_transition_rejects_extra_path(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        rows.append(
            {
                "path": "mythic-edge-role-pool/references/unexpected.md",
                "sha256": "0" * 64,
            }
        )
        self.assert_manifest_rows_rejected(rows, "file count")

    def test_manifest_transition_rejects_duplicate_path(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        rows.append(
            next(row for row in rows if row["path"] == SUCCESSOR_MANIFEST_PATH).copy()
        )
        self.assert_manifest_rows_rejected(rows, "duplicate manifest paths")

    def test_reparse_successor_is_rejected_before_target_access(self) -> None:
        document = observation()
        successor_path = SKILL_ROOT / stage3.SUCCESSOR_SKILL_RELATIVE_PATH
        original_lstat = Path.lstat

        def synthetic_lstat(path: Path) -> object:
            if path == successor_path:
                return SimpleNamespace(
                    st_mode=stat.S_IFLNK,
                    st_file_attributes=getattr(
                        stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400
                    ),
                )
            return original_lstat(path)

        with (
            mock.patch.object(Path, "lstat", autospec=True, side_effect=synthetic_lstat),
            mock.patch.object(
                stage3,
                "_manifest_row",
                side_effect=AssertionError("reparse target must not be hashed"),
            ),
            mock.patch.object(
                Path,
                "resolve",
                side_effect=AssertionError("reparse target must not be followed"),
            ),
            mock.patch.object(
                Path,
                "read_bytes",
                side_effect=AssertionError("reparse target must not be opened"),
            ),
            mock.patch.object(
                Path,
                "replace",
                side_effect=AssertionError("reparse target must not be replaced"),
            ),
        ):
            errors = validate_stage3_behavioral_planning(document)

        self.assertTrue(any("reparse point" in error for error in errors), errors)
        successor_rows = [
            row
            for row in document["contract_transition"]["change_set"]
            if row["path"] == SUCCESSOR_MANIFEST_PATH
        ]
        self.assertEqual(successor_rows[0]["after_sha256"], SUCCESSOR_SHA256)

    def test_v4_successor_digest_mismatch_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(
            row for row in rows if row["path"] == V4_SUCCESSOR_MANIFEST_PATH
        )
        successor["sha256"] = "0" * 64
        self.assert_manifest_rows_rejected(rows, "v4 successor digest")

    def test_missing_v4_successor_rejects_count_38(self) -> None:
        rows = [
            row
            for row in current_skill_manifest()
            if row["path"] != V4_SUCCESSOR_MANIFEST_PATH
        ]
        self.assertEqual(len(rows), 38)
        self.assert_manifest_rows_rejected(rows, "file count")

    def test_renamed_v4_successor_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(
            row for row in rows if row["path"] == V4_SUCCESSOR_MANIFEST_PATH
        )
        successor["path"] = V4_SUCCESSOR_MANIFEST_PATH.replace(
            ".md", "-renamed.md"
        )
        self.assert_manifest_rows_rejected(rows, "unexpected or missing added paths")

    def test_case_varied_v4_successor_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(
            row for row in rows if row["path"] == V4_SUCCESSOR_MANIFEST_PATH
        )
        successor["path"] = V4_SUCCESSOR_MANIFEST_PATH.replace(
            "external-isolation", "External-Isolation"
        )
        self.assert_manifest_rows_rejected(rows, "unexpected or missing added paths")

    def test_duplicate_v4_successor_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        rows.append(
            next(
                row for row in rows if row["path"] == V4_SUCCESSOR_MANIFEST_PATH
            ).copy()
        )
        self.assert_manifest_rows_rejected(rows, "duplicate manifest paths")

    def test_extra_path_rejects_count_40(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        rows.append(
            {
                "path": "mythic-edge-role-pool/references/unexpected-v4.md",
                "sha256": "0" * 64,
            }
        )
        self.assertEqual(len(rows), 40)
        self.assert_manifest_rows_rejected(rows, "file count")

    def test_unexpected_modified_path_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        unchanged_path = (
            "mythic-edge-role-pool/references/"
            "fallback-pickup-fixture/injection.json"
        )
        row = next(row for row in rows if row["path"] == unchanged_path)
        row["sha256"] = "0" * 64
        self.assert_manifest_rows_rejected(rows, "unexpected or missing modified paths")

    def test_changed_legacy_added_path_set_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        legacy_path = "mythic-edge-role-pool/references/external-isolation-broker.md"
        row = next(row for row in rows if row["path"] == legacy_path)
        row["path"] = legacy_path.replace(".md", "-changed.md")
        self.assert_manifest_rows_rejected(rows, "unexpected or missing added paths")

    def test_v4_reparse_successor_is_rejected_before_target_access(self) -> None:
        document = observation()
        successor_path = SKILL_ROOT / stage3.V4_SUCCESSOR_SKILL_RELATIVE_PATH
        original_lstat = Path.lstat

        def synthetic_lstat(path: Path) -> object:
            if path == successor_path:
                return SimpleNamespace(
                    st_mode=stat.S_IFLNK,
                    st_file_attributes=getattr(
                        stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400
                    ),
                )
            return original_lstat(path)

        with (
            mock.patch.object(Path, "lstat", autospec=True, side_effect=synthetic_lstat),
            mock.patch.object(
                stage3,
                "_manifest_row",
                side_effect=AssertionError("reparse target must not be hashed"),
            ),
            mock.patch.object(
                Path,
                "resolve",
                side_effect=AssertionError("reparse target must not be followed"),
            ),
            mock.patch.object(
                Path,
                "read_bytes",
                side_effect=AssertionError("reparse target must not be opened"),
            ),
            mock.patch.object(
                Path,
                "replace",
                side_effect=AssertionError("reparse target must not be replaced"),
            ),
        ):
            errors = validate_stage3_behavioral_planning(document)

        self.assertTrue(any("reparse point" in error for error in errors), errors)
        successor_rows = [
            row
            for row in document["contract_transition"]["change_set"]
            if row["path"] == V4_SUCCESSOR_MANIFEST_PATH
        ]
        self.assertEqual(successor_rows[0]["after_sha256"], V4_SUCCESSOR_SHA256)

    def test_v5_successor_digest_mismatch_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(
            row for row in rows if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
        )
        successor["sha256"] = "0" * 64
        self.assert_manifest_rows_rejected(rows, "v5 successor digest")

    def test_missing_v5_successor_rejects_count_38(self) -> None:
        rows = [
            row
            for row in current_skill_manifest()
            if row["path"] != V5_SUCCESSOR_MANIFEST_PATH
        ]
        self.assertEqual(len(rows), 38)
        self.assert_manifest_rows_rejected(rows, "file count")

    def test_renamed_v5_successor_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(
            row for row in rows if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
        )
        successor["path"] = V5_SUCCESSOR_MANIFEST_PATH.replace(
            ".md", "-renamed.md"
        )
        self.assert_manifest_rows_rejected(rows, "unexpected or missing added paths")

    def test_case_varied_v5_successor_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(
            row for row in rows if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
        )
        successor["path"] = V5_SUCCESSOR_MANIFEST_PATH.replace(
            "external-isolation", "External-Isolation"
        )
        self.assert_manifest_rows_rejected(rows, "unexpected or missing added paths")

    def test_duplicate_v5_successor_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        rows.append(
            next(
                row for row in rows if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
            ).copy()
        )
        self.assert_manifest_rows_rejected(rows, "duplicate manifest paths")

    def test_v5_case_insensitive_duplicate_representation_is_rejected(self) -> None:
        successor_path = SKILL_ROOT / stage3.V5_SUCCESSOR_SKILL_RELATIVE_PATH
        parent = successor_path.parent
        entries = list(parent.iterdir())
        case_variant = parent / "External-Isolation-Broker-v5-corrective-successor.md"
        original_iterdir = Path.iterdir

        def synthetic_iterdir(path: Path) -> object:
            if path == parent:
                return iter([*entries, case_variant])
            return original_iterdir(path)

        with (
            mock.patch.object(
                Path, "iterdir", autospec=True, side_effect=synthetic_iterdir
            ),
            mock.patch.object(
                stage3,
                "_manifest_row",
                side_effect=AssertionError("duplicate target must not be hashed"),
            ),
            mock.patch.object(
                Path,
                "read_bytes",
                side_effect=AssertionError("duplicate target must not be read"),
            ),
            mock.patch.object(
                stage3.hashlib,
                "sha256",
                side_effect=AssertionError("duplicate target must not be hashed"),
            ),
        ):
            with self.assertRaisesRegex(
                stage3.ManifestTransitionError, "duplicate representations"
            ):
                expected_contract_transition()

    def test_v5_case_varied_filesystem_representation_is_rejected(self) -> None:
        successor_path = SKILL_ROOT / stage3.V5_SUCCESSOR_SKILL_RELATIVE_PATH
        parent = successor_path.parent
        entries = [item for item in parent.iterdir() if item.name != successor_path.name]
        case_variant = parent / "External-Isolation-Broker-v5-corrective-successor.md"
        original_iterdir = Path.iterdir

        def synthetic_iterdir(path: Path) -> object:
            if path == parent:
                return iter([*entries, case_variant])
            return original_iterdir(path)

        with mock.patch.object(
            Path, "iterdir", autospec=True, side_effect=synthetic_iterdir
        ):
            with self.assertRaisesRegex(
                stage3.ManifestTransitionError, "casing does not match"
            ):
                expected_contract_transition()

    def test_v5_nonordinary_metadata_is_rejected_before_target_access(self) -> None:
        nonordinary_modes = {
            "directory": stat.S_IFDIR,
            "block_device": stat.S_IFBLK,
            "character_device": stat.S_IFCHR,
            "fifo": stat.S_IFIFO,
            "socket": stat.S_IFSOCK,
        }
        for label, mode in nonordinary_modes.items():
            with self.subTest(label=label):
                self.assert_v5_metadata_rejected_before_target_access(
                    SimpleNamespace(st_mode=mode, st_file_attributes=0),
                    "not an ordinary file",
                )

    def test_v5_metadata_failure_is_rejected_before_target_access(self) -> None:
        self.assert_v5_metadata_rejected_before_target_access(
            OSError("synthetic metadata failure"), "metadata is unavailable"
        )

    def test_v5_reparse_successor_is_rejected_before_target_access(self) -> None:
        self.assert_v5_metadata_rejected_before_target_access(
            SimpleNamespace(
                st_mode=stat.S_IFREG,
                st_file_attributes=getattr(
                    stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400
                ),
            ),
            "reparse point",
        )

    def test_v5_symlink_identity_is_rejected_before_target_access(self) -> None:
        self.assert_v5_metadata_rejected_before_target_access(
            SimpleNamespace(st_mode=stat.S_IFLNK, st_file_attributes=0),
            "reparse point",
        )

    def test_count_39_substitution_with_wrong_path_set_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        successor = next(
            row for row in rows if row["path"] == V5_SUCCESSOR_MANIFEST_PATH
        )
        successor["path"] = "mythic-edge-role-pool/references/substitution.md"
        self.assertEqual(len(rows), 39)
        self.assert_manifest_rows_rejected(rows, "unexpected or missing added paths")

    def test_missing_modified_path_membership_is_rejected(self) -> None:
        rows = copy.deepcopy(current_skill_manifest())
        modified_path = "mythic-edge-role-pool/scripts/check_pool_plan.py"
        row = next(row for row in rows if row["path"] == modified_path)
        row["sha256"] = STAGE2_BASELINE_FILES[modified_path]
        self.assert_manifest_rows_rejected(rows, "unexpected or missing modified paths")

    def test_removed_stage2_baseline_path_is_rejected(self) -> None:
        baseline_path = (
            "mythic-edge-role-pool/references/fallback-pickup-fixture/injection.json"
        )
        rows = [
            row for row in current_skill_manifest() if row["path"] != baseline_path
        ]
        self.assertEqual(len(rows), 38)
        self.assert_manifest_rows_rejected(rows, "file count")

    def test_legacy_transition_rules_cannot_be_weakened(self) -> None:
        mutations = {
            "production_plan_validator_unchanged": True,
            "stage2_evidence_historical_immutable": False,
            "stage2_revalidated_under_current_manifest": True,
            "authority_expansion": True,
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                document = observation()
                document["contract_transition"][field] = value
                errors = validate_stage3_behavioral_planning(rehash(document))
                self.assertTrue(
                    any("contract_transition" in error for error in errors), errors
                )

    def test_scenario_is_explicitly_synthetic_three_repo_three_lane_same_role(self) -> None:
        scenario = observation()["scenario"]
        self.assertEqual(scenario, EXPECTED_SCENARIO)
        self.assertIs(scenario["synthetic"], True)
        self.assertEqual(scenario["repository_count"], 3)
        self.assertEqual(scenario["lane_count"], 3)
        self.assertEqual({lane["role"] for lane in scenario["lanes"]}, {"Codex B"})
        self.assertTrue(
            all(repo.startswith("synthetic/") for repo in scenario["repositories"])
        )

    def test_positive_compatibility_covers_all_three_pairs(self) -> None:
        compatibility = observation()["compatibility"]
        self.assertEqual(compatibility["observed_pair_count"], 3)
        self.assertIs(compatibility["all_pairs_covered"], True)
        self.assertEqual(
            compatibility["overall_verdict"], "safe_to_run_concurrently"
        )
        self.assertTrue(
            all(
                row["verdict"] == "safe_to_run_concurrently"
                for row in compatibility["rows"]
            )
        )

    def test_same_repository_relative_path_is_safe_only_across_distinct_repos(self) -> None:
        scenario = copy.deepcopy(EXPECTED_SCENARIO)
        positive = derive_compatibility(scenario)
        self.assertEqual(positive["overall_verdict"], "safe_to_run_concurrently")
        scenario["lanes"][1]["repository_id"] = scenario["lanes"][0][
            "repository_id"
        ]
        negative = derive_compatibility(scenario)
        self.assertEqual(negative["overall_verdict"], "excluded_fail_closed")
        self.assertTrue(negative["rows"][0]["shared_write_paths"])

    def test_malformed_nested_compatibility_input_fails_without_exception(self) -> None:
        scenario = copy.deepcopy(EXPECTED_SCENARIO)
        scenario["lanes"][0]["dependencies"] = [["not-a-string"]]
        self.assertIsNone(derive_compatibility(scenario))

        document = observation()
        document["scenario"] = scenario
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("scenario" in error for error in errors))
        self.assertTrue(any("cannot be derived" in error for error in errors))

    def test_fail_closed_probe_set_is_complete_and_mechanically_derived(self) -> None:
        probes = expected_exclusion_probes()
        self.assertEqual(len(probes), 7)
        self.assertEqual(
            {probe["probe_id"] for probe in probes},
            {
                "missing_compatibility_evidence",
                "unlisted_repository",
                "dependency_cycle",
                "overlapping_write_path",
                "shared_contract_surface",
                "protected_surface",
                "external_effect_required",
            },
        )
        for probe in probes:
            with self.subTest(probe=probe["probe_id"]):
                result, fallback, reason = classify_exclusion_probe(probe)
                self.assertEqual(result, "excluded_fail_closed")
                self.assertEqual(probe["observed_result"], result)
                self.assertEqual(probe["fallback_condition"], fallback)
                self.assertEqual(probe["reason_code"], reason)

    def test_probe_claim_cannot_disagree_with_classifier(self) -> None:
        document = observation()
        document["exclusion_probes"][0]["observed_result"] = "eligible"
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("exclusion_probes" in error for error in errors))

    def test_every_operational_counter_is_required_and_zero(self) -> None:
        document = observation()
        self.assertEqual(
            document["effect_counters"],
            {field: 0 for field in EFFECT_COUNTER_FIELDS},
        )
        for field in EFFECT_COUNTER_FIELDS:
            with self.subTest(field=field):
                changed = observation()
                changed["effect_counters"][field] = 1
                errors = validate_stage3_behavioral_planning(rehash(changed))
                self.assertTrue(any("effect_counters" in error for error in errors))

    def test_every_required_assertion_is_true(self) -> None:
        document = observation()
        self.assertEqual(
            document["assertions"], {field: True for field in ASSERTION_FIELDS}
        )
        for field in ASSERTION_FIELDS:
            with self.subTest(field=field):
                changed = observation()
                changed["assertions"][field] = False
                errors = validate_stage3_behavioral_planning(rehash(changed))
                self.assertTrue(any("assertions" in error for error in errors))

    def test_json_boolean_and_integer_types_are_not_interchangeable(self) -> None:
        document = observation()
        document["effect_counters"] = {
            field: False for field in EFFECT_COUNTER_FIELDS
        }
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("effect_counters" in error for error in errors))

        document = observation()
        document["assertions"] = {field: 1 for field in ASSERTION_FIELDS}
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("assertions" in error for error in errors))

        document = observation()
        document["scenario"]["synthetic"] = 1
        document["scenario"]["source_repository_read_performed"] = 0
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("scenario" in error for error in errors))

        document = observation()
        document["sequence_index"] = True
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("sequence_index" in error for error in errors))

        document = observation()
        document["stage"] = True
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("stage" in error for error in errors))

    def test_planning_projection_never_becomes_v3_plan_or_live_transition(self) -> None:
        projection = observation()["planning_projection"]
        self.assertEqual(
            projection["mode"], "synthetic_parallel_compatibility_assessment"
        )
        self.assertIs(projection["projection_only"], True)
        self.assertIs(projection["v3_plan_emitted"], False)
        self.assertIs(projection["live_transition_authorized"], False)
        self.assertEqual(projection["selected_for_dispatch_lane_ids"], [])
        for field in ("claim_count", "lease_count", "reservation_count", "launch_count"):
            self.assertEqual(projection[field], 0)

    def test_pair_validator_makes_pair_review_ready_without_accepting_it(self) -> None:
        first = observation("1_of_2")
        second = observation("2_of_2")
        self.assertEqual(validate_stage3_pair(first, second), [])
        self.assertEqual(first["independent_review"]["status"], "pending")
        self.assertEqual(second["independent_review"]["status"], "pending")

        changed = copy.deepcopy(second)
        changed["attempt_series_id"] = "55555555-5555-4555-8555-555555555555"
        changed = rehash(changed)
        errors = validate_stage3_pair(first, changed)
        self.assertTrue(any("attempt_series_id" in error for error in errors))

    def test_pair_requires_order_distinct_identity_and_increasing_time(self) -> None:
        first = observation("1_of_2")
        second = observation("2_of_2")
        second["observation_id"] = first["observation_id"]
        second["created_at"] = first["created_at"]
        second = rehash(second)
        errors = validate_stage3_pair(first, second)
        self.assertTrue(any("IDs must be distinct" in error for error in errors))
        self.assertTrue(any("later than first" in error for error in errors))

    def test_agent_behavior_and_finding_resolution_remain_for_stage4_review(self) -> None:
        document = observation()
        self.assertIs(document["scenario"]["agent_behavior_tested"], False)
        self.assertIs(document["finding_resolution_claimed"], False)
        self.assertIs(document["stage_advancement_claimed"], False)
        self.assertEqual(
            document["release_findings"],
            [
                {
                    "finding_id": FINDING_ID,
                    "status": "unresolved",
                    "resolution_claimed": False,
                }
            ],
        )
        self.assertIs(
            document["independent_review"]["agent_behavior_review_in_scope"],
            False,
        )

    def test_stage3_document_is_rejected_as_a_v3_pool_plan(self) -> None:
        errors = validate_plan(observation())
        self.assertTrue(errors)
        self.assertTrue(any("schema_version" in error for error in errors))

    def test_missing_unknown_and_invalid_identity_fields_fail_closed(self) -> None:
        document = observation()
        del document["effect_counters"]
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("missing fields" in error for error in errors))

        document = observation()
        document["claim_receipt"] = "invented"
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("unknown fields" in error for error in errors))

        document = observation()
        document["observation_id"] = "not-a-uuid"
        errors = validate_stage3_behavioral_planning(rehash(document))
        self.assertTrue(any("observation_id" in error for error in errors))

    def test_canonical_self_digest_is_recomputed(self) -> None:
        document = observation()
        document["digest"] = "0" * 64
        errors = validate_stage3_behavioral_planning(document)
        self.assertTrue(any("digest" in error for error in errors))

    def test_cli_accepts_canonical_json_and_rejects_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "stage3-observation.json"
            document = observation()
            path.write_bytes(canonical_bytes(document))
            completed = subprocess.run(
                [sys.executable, "-B", str(CHECKER), str(path)],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

            second_path = Path(temporary) / "stage3-observation-2.json"
            second_path.write_bytes(canonical_bytes(observation("2_of_2")))
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(CHECKER),
                    str(path),
                    "--pair-with",
                    str(second_path),
                ],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("independent_review=pending", completed.stdout)

            rendered = canonical_bytes(document).decode("ascii")
            needle = '"stage":3'
            path.write_text(
                rendered.replace(needle, needle + ',"stage":3', 1),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, "-B", str(CHECKER), str(path)],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("duplicate JSON key", completed.stderr)

            path.write_text(
                rendered.replace('"stage":3', '"stage":NaN', 1),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, "-B", str(CHECKER), str(path)],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("unable to read strict JSON document", completed.stderr)

    def test_schema_name_is_the_separate_stage3_contract(self) -> None:
        self.assertEqual(
            SCHEMA_VERSION,
            "mythic_edge_role_pool_stage3_behavioral_planning.v1",
        )
        self.assertEqual(observation()["schema_version"], SCHEMA_VERSION)


if __name__ == "__main__":
    unittest.main()
