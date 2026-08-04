from __future__ import annotations

import copy
import hashlib
import io
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from unittest import mock

import check_pool_plan as native
import codex_launcher_contract as launcher_contract
import trusted_native_app_direct_task_adapter as app_direct
import trusted_native_app_server_adapter as app_server
from check_pool_plan import (
    BROKER_LAUNCHER_RECEIPT_SIDECARS_SCHEMA_VERSION,
    OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
    canonical_document_digest,
    render_untrusted_evidence,
    select_lanes,
    validate_launcher_receipt_sidecars,
    validate_plan_offline_synthetic_fixture,
)
from check_pool_plan import (
    validate_plan as validate_plan_production,
)
from check_pool_plan import (
    validate_plan_against_observations as validate_plan_against_observations_production,
)
from check_pool_plan import (
    validate_prelaunch_against_preclaim as validate_prelaunch_against_preclaim_production,
)
from codex_launcher_contract import (
    ProductionVerificationContext,
    with_self_digest,
)
from pool_test_fixtures import (
    ARTIFACT_DIGEST,
    EXPIRES,
    LANE_ID,
    MALICIOUS_EXTERNAL_TEXT,
    NOW,
    OBSERVED,
    OFFLINE_THREE_LANE_IDS,
    OFFLINE_THREE_REPOSITORIES,
    READY,
    REPOSITORY,
    active_inspect_plan,
    completed_result,
    discovery_for_plan,
    inspect_plan,
    launcher_receipt_sidecars_for_document,
    offline_three_repository_inspect_plan,
    offline_three_repository_preclaim_plan,
    offline_three_repository_prelaunch_plan,
    preclaim_plan,
    prelaunch_plan,
    runtime_preflight,
    worktrees_for_plan,
)
from test_codex_launcher_contract import (
    _synthetic_broker_chain,
    _SyntheticBrokerClient,
)


def validate_plan(plan: object, now: object = None) -> list[str]:
    return validate_plan_offline_synthetic_fixture(
        plan,
        now,
        launcher_receipts=(
            launcher_receipt_sidecars_for_document(plan)
            if isinstance(plan, dict)
            else None
        ),
    )


def validate_plan_against_observations(
    plan: object, discovery: object, worktrees: object, now: object = None
) -> list[str]:
    return validate_plan_against_observations_production(
        plan,
        discovery,
        worktrees,
        now,
        validation_mode=OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
        launcher_receipts=(
            launcher_receipt_sidecars_for_document(plan)
            if isinstance(plan, dict)
            else None
        ),
    )


def validate_prelaunch_against_preclaim(
    preclaim: object, prelaunch: object, now: object = None
) -> list[str]:
    return validate_prelaunch_against_preclaim_production(
        preclaim,
        prelaunch,
        now,
        validation_mode=OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
    )


def valid_exception(lane_id: str) -> dict[str, object]:
    return {
        "kind": "exception",
        "exception_name": "explicit_user_override",
        "repository": REPOSITORY,
        "active_issue_or_lane": LANE_ID,
        "blocked_active_issue_or_pr": "github:issue/101",
        "reason": "bounded test exception",
        "allowed_scope": lane_id,
        "expiration_condition": "when the test lane completes",
        "expires_at": EXPIRES,
        "authorized_by": "user:current-task/wip-exception",
        "recorded_in": "artifact:wip-exception/101",
    }


def compatibility_row(left: str, right: str) -> dict[str, object]:
    return {
        "left": left,
        "right": right,
        "verdict": "safe_to_run_concurrently",
        "observed_at": OBSERVED,
        "evidence_refs": ["artifact:compatibility/101-102"],
        "dependency_relation": "none",
        "shared_write_paths": [],
        "shared_contracts": [],
        "shared_protected_surfaces": [],
        "shared_external_state": [],
        "invalidation_risk": "none",
        "integration_order": [],
        "invalidation_triggers": [],
        "refresh_barrier": None,
        "refresh_bindings": [],
    }


class _StartedSyntheticBrokerClient(_SyntheticBrokerClient):
    def start_once(self, launch_request: dict[str, object]) -> object:
        chain = super().start_once(launch_request)
        chain.document["terminal_receipt"] = None
        return chain


def broker_sidecars_for_completed_document(
    document: dict[str, object],
    *,
    terminal: bool = True,
) -> tuple[dict[str, object], launcher_contract.BrokerVerificationContext]:
    """Project one synthetic broker terminal chain into a plan or result fixture."""

    if document.get("schema_version") == "mythic_edge_role_pool_plan.v3":
        readback = document["active_waves"][0]["lanes"][0]["runtime"][
            "launch_readback"
        ]
    else:
        readback = document["lanes"][0]["launch_readback"]
    chain, _stdout, _stderr = _synthetic_broker_chain()
    request = chain["launch_request"]
    request.update(
        {
            "launcher_preflight_digest": readback["launcher_preflight_digest"],
            "executable": {
                "path": readback["selected_executable_path"],
                "sha256": readback["selected_executable_sha256"],
                "length_bytes": readback["selected_executable_length_bytes"],
            },
            "packet": {
                "path": "C:\\synthetic\\packet.json",
                "sha256": readback["packet_digest"],
                "length_bytes": readback["packet_length_bytes"],
            },
        }
    )
    request.pop("digest", None)
    request = with_self_digest(request)
    outcome = launcher_contract._broker_launch_once_for_test(
        request,
        broker_client=(
            _SyntheticBrokerClient()
            if terminal
            else _StartedSyntheticBrokerClient()
        ),
    )
    readback.update(
        {
            "launcher": "codex:broker-single-start/v1",
            "launcher_receipt_digest": outcome.receipt["digest"],
            "launch_backend": "windows_isolation_broker",
            "production_eligible": True,
            "external_os_isolation": None,
            "external_os_isolation_live_launch_eligible": True,
        }
    )
    sidecars = with_self_digest(
        {
            "schema_version": BROKER_LAUNCHER_RECEIPT_SIDECARS_SCHEMA_VERSION,
            "receipts": {readback["launch_receipt"]: outcome.receipt},
            "attestation_algorithm": "broker_receipt_chain",
            "attestation_key_id": None,
            "attestation_hmac_sha256": None,
        }
    )
    assert outcome.broker_verification_context is not None
    return sidecars, outcome.broker_verification_context


class AuthenticatedBoundaryTests(unittest.TestCase):
    def test_caller_cannot_construct_a_production_verifier_context(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "not provisioned"):
            ProductionVerificationContext(
                key_id="attacker-key",
                expected_provider="attacker-provider",
                expected_evidence_source="attacker-source",
                expected_verifier_identity="attacker-verifier",
                verification_key=b"a" * 32,
            )

    def test_live_envelope_relabel_and_redigest_fails_without_pinned_verifier(self) -> None:
        plan = preclaim_plan()
        preflight = plan["runtime_preflight"]
        for index, binding in enumerate(preflight["external_os_isolation_bindings"]):
            evidence = binding["evidence"]
            issue = evidence["lane_id"].rsplit("#", 1)[1]
            evidence.update(
                {
                    "evidence_kind": "independent_os_boundary_receipt",
                    "boundary_status": "verified",
                    "live_boundary_claimed": True,
                    "live_launch_eligible": True,
                    "independently_verified": True,
                    "verifier_identity": "caller-selected-verifier",
                    "receipt_ref": f"receipt:external-os-isolation/{issue}",
                    "codex_control_plane_channel_ref": (
                        f"receipt:codex-control-plane-channel/{issue}"
                    ),
                    "launcher_external_isolation_receipt_digest": "9" * 64,
                    "attestation_algorithm": "hmac-sha256",
                    "attestation_key_id": "caller-selected-key",
                    "attestation_hmac_sha256": "8" * 64,
                }
            )
            binding["evidence_ref"] = evidence["receipt_ref"]
            binding["evidence_digest"] = canonical_document_digest(evidence)
        preflight["external_os_isolation_live_launch_eligible"] = True
        errors = validate_plan_production(
            plan,
            NOW,
        )
        self.assertTrue(
            any("out-of-band production verification context" in error for error in errors),
            errors,
        )
        opaque = object.__new__(ProductionVerificationContext)
        opaque_errors = validate_plan_production(
            plan,
            NOW,
            production_verification_context=opaque,
        )
        self.assertTrue(
            any("authenticated verification failed" in error for error in opaque_errors),
            opaque_errors,
        )

    def test_launcher_sidecar_relabel_and_redigest_fails_without_pinned_verifier(self) -> None:
        result = completed_result()
        sidecars = launcher_receipt_sidecars_for_document(result)
        sidecars["attestation_algorithm"] = "hmac-sha256"
        sidecars["attestation_key_id"] = "caller-selected-key"
        sidecars["attestation_hmac_sha256"] = "7" * 64
        sidecars = with_self_digest(sidecars)
        errors = validate_launcher_receipt_sidecars(
            sidecars,
        )
        self.assertTrue(
            any("opaque current-service verification context" in error for error in errors),
            errors,
        )
        opaque = object.__new__(ProductionVerificationContext)
        opaque_errors = validate_launcher_receipt_sidecars(
            sidecars,
            production_verification_context=opaque,
        )
        self.assertTrue(
            any("production broker sidecars require" in error for error in opaque_errors),
            opaque_errors,
        )

    def test_current_broker_chain_validates_without_generic_mapping_mac(self) -> None:
        plan = active_inspect_plan()
        sidecars, context = broker_sidecars_for_completed_document(plan)
        self.assertEqual(
            validate_plan_production(
                plan,
                NOW,
                launcher_receipts=sidecars,
                production_verification_context=context,
            ),
            [],
        )
        self.assertIsNone(sidecars["attestation_key_id"])
        self.assertIsNone(sidecars["attestation_hmac_sha256"])

    def test_running_requires_current_start_chain_not_terminal_receipt(self) -> None:
        plan = active_inspect_plan()
        lane = plan["active_waves"][0]["lanes"][0]
        lane["state"] = "running"
        lane["runtime"]["state"] = "running"
        terminal_sidecars, terminal_context = broker_sidecars_for_completed_document(
            plan
        )
        terminal_errors = validate_plan_production(
            plan,
            NOW,
            launcher_receipts=terminal_sidecars,
            production_verification_context=terminal_context,
        )
        self.assertTrue(
            any("running requires a current start receipt" in error for error in terminal_errors),
            terminal_errors,
        )

        plan = active_inspect_plan()
        lane = plan["active_waves"][0]["lanes"][0]
        lane["state"] = "running"
        lane["runtime"]["state"] = "running"
        started_sidecars, started_context = broker_sidecars_for_completed_document(
            plan,
            terminal=False,
        )
        self.assertEqual(
            validate_plan_production(
                plan,
                NOW,
                launcher_receipts=started_sidecars,
                production_verification_context=started_context,
            ),
            [],
        )


def add_second_proposed_lane(plan: dict[str, object]) -> str:
    second = copy.deepcopy(plan["proposed_wave"]["lanes"][0])
    second_id = f"{REPOSITORY}#102"
    second["lane_id"] = second_id
    second["issue"] = 102
    second["worktree"]["path"] = "C:\\ME-B-102"
    second["worktree"]["resolved_path"] = "C:\\ME-B-102"
    second["worktree"]["git_toplevel"] = "C:\\ME-B-102"
    second["worktree"]["git_common_dir"] = "C:\\ME-B-102\\.git"
    second["worktree"]["branch"] = "codex/issue-102"
    second_contract = "docs/contracts/issue-102.md"
    second["scope"]["expected_files"] = [second_contract]
    second["scope"]["write_paths"] = [second_contract]
    second["scope"]["contract_surfaces"] = [second_contract]
    second["role_evidence"]["issue_ref"] = "github:issue/102"
    second["role_evidence"]["contract_path"] = second_contract
    second["evidence_sources"][0]["ref"] = "github:issue/102"
    plan["inventory"]["repositories"][0]["allowed_read_only_references"].append(
        "github:issue/102"
    )
    second["wip_assignment"] = valid_exception(second_id)
    request_text = (
        plan["action"]["request_text"]
        + f"; authorize WIP exception lane={second_id} owner={LANE_ID}"
    )
    plan["action"]["request_text"] = request_text
    plan["action"]["request_sha256"] = hashlib.sha256(
        request_text.encode("utf-8")
    ).hexdigest()
    plan["proposed_wave"]["lanes"].append(second)
    plan["runtime_preflight"] = runtime_preflight(
        lanes=plan["proposed_wave"]["lanes"]
    )
    candidate = copy.deepcopy(plan["candidate_inventory"][0])
    candidate["lane_id"] = second_id
    plan["candidate_inventory"].append(candidate)
    plan["compatibility"] = [compatibility_row(LANE_ID, second_id)]
    return second_id


class PlanAssertions(unittest.TestCase):
    def assert_error(self, plan: dict[str, object], fragment: str) -> list[str]:
        errors = validate_plan(plan, NOW)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )
        return errors


class ValidPlanTests(PlanAssertions):
    def test_canonical_inspect_preclaim_and_prelaunch_plans_validate(self) -> None:
        for plan in (inspect_plan(), preclaim_plan(), prelaunch_plan(), active_inspect_plan()):
            with self.subTest(phase=plan["phase"], active=bool(plan["active_waves"])):
                self.assertEqual(validate_plan(plan, NOW), [])

    def test_every_poolable_role_has_a_valid_preclaim_plan(self) -> None:
        for role in ("Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"):
            with self.subTest(role=role):
                self.assertEqual(validate_plan(preclaim_plan(role), NOW), [])

    def test_valid_two_lane_plan_uses_one_slot_and_one_exception(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        self.assertEqual(validate_plan(plan, NOW), [])

    def test_offline_three_repository_plans_validate_and_bind_to_observations(self) -> None:
        plans = (
            offline_three_repository_inspect_plan(),
            offline_three_repository_preclaim_plan(),
            offline_three_repository_prelaunch_plan(),
        )
        for plan in plans:
            with self.subTest(phase=plan["phase"]):
                self.assertEqual(validate_plan(plan, NOW), [])
                self.assertEqual(
                    validate_plan_against_observations(
                        plan,
                        discovery_for_plan(plan),
                        worktrees_for_plan(plan),
                        NOW,
                    ),
                    [],
                )

    def test_offline_three_lane_wave_uses_one_role_and_only_local_role_artifacts(self) -> None:
        plan = offline_three_repository_preclaim_plan()
        wave = plan["proposed_wave"]
        self.assertEqual(wave["role"], "Codex B")
        self.assertEqual({lane["next_role"] for lane in wave["lanes"]}, {"Codex B"})
        self.assertEqual(
            {lane["repository_id"] for lane in wave["lanes"]},
            set(OFFLINE_THREE_REPOSITORIES),
        )
        self.assertEqual(
            [lane["lane_id"] for lane in wave["lanes"]],
            list(OFFLINE_THREE_LANE_IDS),
        )
        self.assertEqual(len(plan["compatibility"]), 3)
        for lane in wave["lanes"]:
            self.assertEqual(lane["wip_assignment"], {"kind": "slot_owner"})
            self.assertEqual(lane["scope"]["external_writes"], ["local_artifact"])
        forbidden = {"git_commit", "git_push", "draft_pr_write", "merge_pr"}
        self.assertTrue(forbidden.isdisjoint(plan["action"]["authorized_actions"]))

    def test_offline_three_lane_prelaunch_freezes_claim_and_unique_reservations(self) -> None:
        preclaim = offline_three_repository_preclaim_plan()
        prelaunch = offline_three_repository_prelaunch_plan()
        self.assertEqual(
            validate_prelaunch_against_preclaim(preclaim, prelaunch, NOW), []
        )
        wave = prelaunch["proposed_wave"]
        self.assertEqual(set(wave["claim"]["lane_ids"]), set(OFFLINE_THREE_LANE_IDS))
        receipts = {lane["reservation"]["receipt_ref"] for lane in wave["lanes"]}
        keys = {lane["reservation"]["idempotency_key"] for lane in wave["lanes"]}
        self.assertEqual(len(receipts), 3)
        self.assertEqual(len(keys), 3)

    def test_offline_inspect_candidates_bind_exactly_to_independent_discovery(self) -> None:
        plan = offline_three_repository_inspect_plan()
        discovery = discovery_for_plan(plan)
        discovery["candidate_inventory"].pop()
        errors = validate_plan_against_observations(
            plan, discovery, worktrees_for_plan(plan), NOW
        )
        self.assertTrue(
            any("candidate inventory must exactly match" in error for error in errors),
            errors,
        )


class StrictSchemaAndIntentTests(PlanAssertions):
    def test_v1_schema_is_rejected(self) -> None:
        plan = preclaim_plan()
        plan["schema_version"] = "mythic_edge_role_pool_plan.v1"
        self.assert_error(plan, "must be mythic_edge_role_pool_plan.v3")

    def test_missing_and_unknown_top_level_fields_are_rejected(self) -> None:
        plan = preclaim_plan()
        del plan["fallback"]
        plan["surprise"] = True
        errors = validate_plan(plan, NOW)
        self.assertTrue(any("missing fields: fallback" in error for error in errors))
        self.assertTrue(any("unknown fields: surprise" in error for error in errors))

    def test_unknown_fields_are_rejected_at_nested_schema_levels(self) -> None:
        mutators = [
            lambda p: p["action"].update({"surprise": True}),
            lambda p: p["inventory"]["sources"][0].update({"surprise": True}),
            lambda p: p["inventory"]["repositories"][0].update({"surprise": True}),
            lambda p: p["runtime_preflight"].update({"surprise": True}),
            lambda p: p["proposed_wave"].update({"surprise": True}),
            lambda p: p["proposed_wave"]["lanes"][0].update({"surprise": True}),
            lambda p: p["proposed_wave"]["lanes"][0]["scope"].update({"surprise": True}),
            lambda p: p["proposed_wave"]["lanes"][0]["role_evidence"].update({"surprise": True}),
            lambda p: p["candidate_inventory"][0].update({"surprise": True}),
            lambda p: p["fallback"].update({"surprise": True}),
            lambda p: p["proposed_wave"]["claim"].update({"surprise": True}),
            lambda p: p["proposed_wave"]["lanes"][0]["reservation"].update({"surprise": True}),
        ]
        for index, mutate in enumerate(mutators):
            plan = prelaunch_plan() if index >= 10 else preclaim_plan()
            mutate(plan)
            with self.subTest(index=index):
                self.assert_error(plan, "unknown fields: surprise")

    def test_bare_or_role_only_invocation_normalizes_to_non_mutating_inspect(self) -> None:
        self.assertEqual(validate_plan(inspect_plan(explicit=False), NOW), [])

    def test_dispatch_requires_explicit_current_user_action(self) -> None:
        plan = preclaim_plan()
        plan["action"]["explicit"] = False
        self.assert_error(plan, "dispatch requires explicit current-user action")

    def test_inspect_cannot_carry_dispatch_state(self) -> None:
        plan = inspect_plan()
        plan["proposed_wave"] = preclaim_plan()["proposed_wave"]
        self.assert_error(plan, "inspect phase must not carry a dispatch wave")

    def test_unknown_or_merge_action_fails_closed(self) -> None:
        plan = preclaim_plan("Codex G")
        plan["action"]["authorized_actions"].append("merge_pr")
        self.assert_error(plan, "unknown or prohibited actions: merge_pr")

    def test_pooled_g_is_readiness_only(self) -> None:
        plan = preclaim_plan("Codex G")
        self.assertEqual(plan["action"]["operation"], "g_readiness_only")
        plan["action"]["operation"] = "merge_pr"
        self.assert_error(plan, "requires g_readiness_only")

    def test_codex_c_cannot_be_pooled(self) -> None:
        plan = preclaim_plan()
        plan["action"]["target_role"] = "Codex C"
        plan["proposed_wave"]["role"] = "Codex C"
        plan["proposed_wave"]["lanes"][0]["next_role"] = "Codex C"
        self.assert_error(plan, "must be a pooled A, B, D, E, F, or G role")


class InventoryReadScopeAndWipTests(PlanAssertions):
    def test_incomplete_stale_or_unresolved_inventory_is_rejected(self) -> None:
        cases = [
            ("complete", False, "must be complete"),
            ("observed_at", "2026-07-13T10:00:00Z", "is stale"),
            ("unresolved_sources", ["github"], "must be empty"),
        ]
        for key, value, fragment in cases:
            plan = preclaim_plan()
            plan["inventory"][key] = value
            with self.subTest(key=key):
                self.assert_error(plan, fragment)

    def test_discovery_union_must_equal_repository_inventory(self) -> None:
        plan = preclaim_plan()
        plan["inventory"]["sources"][0]["repositories"] = []
        self.assert_error(plan, "source repository union must equal")

    def test_repository_identity_must_be_canonical_owner_repository(self) -> None:
        for invalid in ("Tahjali11/Mythic-Edge", "mythic-edge", "tahjali11/mythic-edge.git"):
            plan = preclaim_plan()
            plan["inventory"]["repositories"][0]["repository_id"] = invalid
            with self.subTest(repository=invalid):
                self.assert_error(plan, "canonical lowercase owner/repository")

    def test_private_full_read_requires_derived_marker_and_no_echo(self) -> None:
        plan = preclaim_plan()
        repo = plan["inventory"]["repositories"][0]
        repo["private_content_authorized"] = False
        repo["no_echo_required"] = False
        errors = validate_plan(plan, NOW)
        self.assertTrue(any("derived private-content handling marker" in error for error in errors))
        self.assertTrue(any("no_echo_required: must be true" in error for error in errors))

    def test_private_content_marker_is_not_independent_read_authority(self) -> None:
        private_metadata = preclaim_plan()
        private_repo = private_metadata["inventory"]["repositories"][0]
        private_repo["read_scope"] = "metadata_only"
        private_repo["read_authority_ref"] = None
        private_repo["allowed_read_only_references"] = []
        private_repo["private_content_authorized"] = True
        self.assert_error(private_metadata, "derived private-content handling marker")

        public_full = preclaim_plan()
        public_repo = public_full["inventory"]["repositories"][0]
        public_repo["visibility"] = "public"
        public_repo["private_content_authorized"] = True
        self.assert_error(public_full, "derived private-content handling marker")

    def test_metadata_only_scope_cannot_supply_issue_or_handoff_content(self) -> None:
        plan = preclaim_plan()
        repo = plan["inventory"]["repositories"][0]
        repo["read_scope"] = "metadata_only"
        repo["read_authority_ref"] = None
        repo["allowed_read_only_references"] = []
        repo["private_content_authorized"] = False
        self.assert_error(plan, "content evidence requires authorized_full")

    def test_evidence_reference_must_be_in_exact_allowlist(self) -> None:
        plan = preclaim_plan()
        plan["proposed_wave"]["lanes"][0]["evidence_sources"][0]["ref"] = "github:issue/999"
        self.assert_error(plan, "outside allowed_read_only_references")

    def test_private_protected_credential_production_and_destructive_scopes_fail_closed(self) -> None:
        for key in ("private_evidence", "credentials", "production", "destructive"):
            plan = preclaim_plan()
            plan["proposed_wave"]["lanes"][0]["scope"][key] = True
            with self.subTest(key=key):
                self.assert_error(plan, f"{key}: cannot be pooled")

    def test_second_same_repository_lane_requires_canonical_exception(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        plan["proposed_wave"]["lanes"][1]["wip_assignment"] = {"kind": "slot_owner"}
        errors = validate_plan(plan, NOW)
        self.assertTrue(any("requires exactly one proposed slot owner" in error for error in errors))
        self.assertTrue(any("needs a WIP exception" in error for error in errors))

    def test_every_exception_field_and_canonical_name_is_required(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        plan["proposed_wave"]["lanes"][1]["wip_assignment"] = {
            "kind": "exception",
            "exception_name": "because_i_said_so",
        }
        errors = validate_plan(plan, NOW)
        self.assertTrue(any("missing fields" in error for error in errors))
        self.assertTrue(any("canonical ADR-0008 exception" in error for error in errors))

    def test_more_than_three_lanes_in_one_wave_is_rejected(self) -> None:
        plan = preclaim_plan()
        for issue in (102, 103, 104):
            extra = copy.deepcopy(plan["proposed_wave"]["lanes"][0])
            extra["lane_id"] = f"{REPOSITORY}#{issue}"
            extra["issue"] = issue
            plan["proposed_wave"]["lanes"].append(extra)
        self.assert_error(plan, "maximum is three")


class ClaimsIdentityAndLeaseTests(PlanAssertions):
    def test_refreshed_server_order_must_make_claim_the_winner(self) -> None:
        plan = prelaunch_plan()
        plan["proposed_wave"]["claim"]["competing_claims"].append(
            {
                "claim_id": "33333333-3333-4333-8333-333333333333",
                "coordinator_id": "44444444-4444-4444-8444-444444444444",
                "server_comment_id": 1,
                "server_created_at": "2026-07-13T11:49:00Z",
                "wave_slot": "wave-1",
                "lane_ids": [LANE_ID],
                "expires_at": EXPIRES,
                "receipt_ref": "github:claim-comment/earlier",
                "refresh_snapshot_id": "claim-refresh-20260713-1159",
                "status": "reserved",
            }
        )
        self.assert_error(plan, "does not make this claim the winner")

    def test_claim_and_reservation_identity_must_match(self) -> None:
        plan = prelaunch_plan()
        plan["proposed_wave"]["lanes"][0]["reservation"]["claim_id"] = (
            "33333333-3333-4333-8333-333333333333"
        )
        self.assert_error(plan, "must match the winning claim")

    def test_launch_requires_at_least_fifteen_minutes_remaining(self) -> None:
        plan = prelaunch_plan()
        expires = "2026-07-13T12:00:01Z"
        plan["proposed_wave"]["claim"]["expires_at"] = expires
        plan["proposed_wave"]["lanes"][0]["reservation"]["expires_at"] = expires
        self.assert_error(plan, "fewer than 15 minutes remain before launch")

    def test_claim_and_reservation_duration_cannot_exceed_twenty_four_hours(self) -> None:
        plan = prelaunch_plan()
        plan["proposed_wave"]["claim"]["expires_at"] = "2026-07-14T11:51:00Z"
        plan["proposed_wave"]["lanes"][0]["reservation"]["expires_at"] = (
            "2026-07-14T11:51:00Z"
        )
        errors = validate_plan(plan, NOW)
        self.assertTrue(any("claim exceeds 24 hours" in error for error in errors))
        self.assertTrue(any("reservation exceeds 24 hours" in error for error in errors))

    def test_scheduling_reservation_never_grants_execution_or_release_authority(self) -> None:
        for key in (
            "implementation_authorized",
            "execution_authorized",
            "publication_authorized",
            "merge_authorized",
        ):
            plan = prelaunch_plan()
            plan["proposed_wave"]["lanes"][0]["reservation"][key] = True
            with self.subTest(key=key):
                self.assert_error(plan, f"{key}: must be false")

    def test_expired_scheduling_lease_does_not_erase_observed_running_runtime(self) -> None:
        plan = active_inspect_plan()
        plan["active_waves"][0]["claim"]["expires_at"] = "2026-07-13T11:55:00Z"
        plan["active_waves"][0]["claim"]["competing_claims"][0]["expires_at"] = (
            "2026-07-13T11:55:00Z"
        )
        plan["active_waves"][0]["lanes"][0]["reservation"]["expires_at"] = (
            "2026-07-13T11:55:00Z"
        )
        self.assertEqual(validate_plan(plan, NOW), [])

    def test_running_lane_requires_fresh_runtime_and_launch_receipt(self) -> None:
        plan = active_inspect_plan()
        plan["active_waves"][0]["lanes"][0]["runtime"]["launch_receipt"] = ""
        self.assert_error(plan, "launch_receipt: must be a non-empty string")

    def test_device_prefix_and_duplicate_physical_worktree_are_rejected(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        second = plan["proposed_wave"]["lanes"][1]["worktree"]
        second["path"] = "\\\\?\\C:\\ME-B-101"
        second["resolved_path"] = "C:\\ME-B-101"
        second["git_toplevel"] = "C:\\ME-B-101"
        errors = validate_plan(plan, NOW)
        self.assertTrue(any("canonical absolute non-device path" in error for error in errors))
        self.assertTrue(any("shares physical worktree" in error for error in errors))

    def test_duplicate_branch_and_lane_id_are_rejected(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        plan["proposed_wave"]["lanes"][1]["worktree"]["branch"] = "codex/issue-101"
        self.assert_error(plan, "shares branch")
        plan = preclaim_plan()
        plan["queued_lanes"] = [copy.deepcopy(plan["proposed_wave"]["lanes"][0])]
        plan["queued_lanes"][0]["wip_assignment"] = {"kind": "queued"}
        self.assert_error(plan, "lane IDs must be unique")


class RuntimeCompatibilityAndFairnessTests(PlanAssertions):
    def test_model_effort_readback_is_advisory(self) -> None:
        plan = preclaim_plan()
        preflight = plan["runtime_preflight"]
        preflight["effective_model"] = "platform-selected-model"
        preflight["effective_reasoning_effort"] = "platform-selected-effort"
        preflight["readback_receipt"] = None
        self.assertEqual(validate_plan(plan, NOW), [])

    def test_platform_default_records_no_requested_cli_preferences(self) -> None:
        plan = preclaim_plan()
        plan["runtime_preflight"] = runtime_preflight(model_available=False)
        self.assertEqual(validate_plan(plan, NOW), [])
        self.assertIsNone(plan["runtime_preflight"]["requested_model"])
        self.assertIsNone(
            plan["runtime_preflight"]["requested_reasoning_effort"]
        )

    def test_launcher_preflight_digest_and_argument_mode_are_derived(self) -> None:
        plan = preclaim_plan()
        preflight = plan["runtime_preflight"]
        preflight["launcher_preflight_digest"] = "0" * 64
        self.assert_error(plan, "must bind the exact launcher preflight")

        plan = preclaim_plan()
        preflight = plan["runtime_preflight"]
        preflight["requested_model"] = None
        self.assert_error(plan, "requested values must equal preferred values")

        plan = preclaim_plan()
        preflight = plan["runtime_preflight"]
        preflight["launcher_preference_mode"] = "platform_default"
        self.assert_error(plan, "must match launcher preflight argument mode")

    def test_prelaunch_freezes_the_entire_runtime_preflight(self) -> None:
        preclaim = preclaim_plan()
        prelaunch = prelaunch_plan()
        prelaunch["runtime_preflight"]["effective_model"] = "advisory-readback"
        self.assertEqual(validate_plan(prelaunch, NOW), [])
        errors = validate_prelaunch_against_preclaim(preclaim, prelaunch, NOW)
        self.assertTrue(
            any("exact launcher" in error for error in errors),
            errors,
        )

    def test_context_isolation_remains_required(self) -> None:
        cases = [
            ("fork_turns", "all", "must be none"),
            ("context_mode", "inherited", "must be isolated"),
        ]
        for key, value, fragment in cases:
            plan = preclaim_plan()
            plan["runtime_preflight"][key] = value
            with self.subTest(key=key):
                self.assert_error(plan, fragment)

    def test_external_os_isolation_is_required_and_fresh(self) -> None:
        plan = preclaim_plan()
        del plan["runtime_preflight"]["external_os_isolation_bindings"]
        self.assert_error(plan, "external_os_isolation_bindings")

        plan = preclaim_plan()
        binding = plan["runtime_preflight"]["external_os_isolation_bindings"][0]
        binding["evidence"]["verified_at"] = "2026-07-13T10:00:00Z"
        binding["evidence_digest"] = canonical_document_digest(binding["evidence"])
        self.assert_error(plan, "verified_at: is stale")

    def test_external_os_isolation_rejects_policy_and_packet_drift(self) -> None:
        plan = preclaim_plan()
        binding = plan["runtime_preflight"]["external_os_isolation_bindings"][0]
        binding["evidence"]["tool_subprocess_network_policy"] = "allow"
        binding["evidence_digest"] = canonical_document_digest(binding["evidence"])
        self.assert_error(plan, "tool_subprocess_network_policy")

        plan = preclaim_plan()
        binding = plan["runtime_preflight"]["external_os_isolation_bindings"][0]
        binding["evidence"]["packet_digest"] = "0" * 64
        binding["evidence_digest"] = canonical_document_digest(binding["evidence"])
        self.assert_error(plan, "must bind the exact lane packet")

    def test_synthetic_isolation_evidence_is_explicitly_live_ineligible(self) -> None:
        plan = preclaim_plan()
        preflight = plan["runtime_preflight"]
        binding = preflight["external_os_isolation_bindings"][0]
        self.assertEqual(binding["evidence"]["evidence_kind"], "synthetic_contract_fixture")
        self.assertFalse(binding["evidence"]["live_launch_eligible"])
        self.assertFalse(preflight["external_os_isolation_live_launch_eligible"])
        production_errors = validate_plan_production(plan, NOW)
        self.assertTrue(
            any(
                "production validation requires codex:broker-single-start/v1" in error
                for error in production_errors
            ),
            production_errors,
        )
        self.assertEqual(
            validate_plan_offline_synthetic_fixture(
                plan,
                NOW,
                launcher_receipts=launcher_receipt_sidecars_for_document(plan),
            ),
            [],
        )

        preflight["external_os_isolation_live_launch_eligible"] = True
        errors = validate_plan_offline_synthetic_fixture(
            plan,
            NOW,
            launcher_receipts=launcher_receipt_sidecars_for_document(plan),
        )
        self.assertTrue(
            any("must equal all bound receipt eligibility markers" in error for error in errors),
            errors,
        )

    def test_active_synthetic_launch_requires_explicit_offline_fixture_api(self) -> None:
        plan = active_inspect_plan()
        errors = validate_plan_production(plan, NOW)
        self.assertTrue(
            any("production validation requires windows_isolation_broker" in error for error in errors),
            errors,
        )
        self.assertTrue(any("launcher_receipts: must be an object" in error for error in errors), errors)
        self.assertTrue(
            any("production validation requires true" in error for error in errors),
            errors,
        )
        self.assertEqual(
            validate_plan_offline_synthetic_fixture(
                plan,
                NOW,
                launcher_receipts=launcher_receipt_sidecars_for_document(plan),
            ),
            [],
        )

    def test_launch_readback_requires_exact_backend_eligibility_pair(self) -> None:
        plan = active_inspect_plan()
        readback = plan["active_waves"][0]["lanes"][0]["runtime"]["launch_readback"]
        readback["launch_backend"] = "subprocess_popen"
        readback["production_eligible"] = True
        errors = validate_plan_offline_synthetic_fixture(
            plan,
            NOW,
            launcher_receipts=launcher_receipt_sidecars_for_document(plan),
        )
        self.assertTrue(
            any("subprocess_popen requires production_eligible false" in error for error in errors),
            errors,
        )

        plan = active_inspect_plan()
        readback = plan["active_waves"][0]["lanes"][0]["runtime"]["launch_readback"]
        readback["launch_backend"] = "windows_isolation_broker"
        readback["launcher"] = "codex:broker-single-start/v1"
        readback["production_eligible"] = True
        readback["external_os_isolation_live_launch_eligible"] = True
        errors = validate_plan_production(
            plan,
            NOW,
            launcher_receipts=launcher_receipt_sidecars_for_document(plan),
        )
        self.assertTrue(
            any("production sidecars require a broker launch receipt" in error for error in errors),
            errors,
        )

    def test_preclaim_requires_preflight_before_any_claim(self) -> None:
        plan = preclaim_plan()
        plan["runtime_preflight"] = None
        self.assert_error(plan, "plan.runtime_preflight: must be an object")

    def test_every_proposed_pair_requires_exact_compatibility_evidence(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        plan["compatibility"] = []
        self.assert_error(plan, "missing 1 required pair")

    def test_three_lane_plan_requires_all_three_unique_pair_rows(self) -> None:
        plan = offline_three_repository_preclaim_plan()
        plan["compatibility"].pop()
        self.assert_error(plan, "missing 1 required pair")

        plan = offline_three_repository_preclaim_plan()
        plan["compatibility"][2] = copy.deepcopy(plan["compatibility"][0])
        errors = validate_plan(plan, NOW)
        self.assertTrue(
            any("duplicate pair" in error or "missing 1 required pair" in error for error in errors),
            errors,
        )

    def test_three_lane_plan_rejects_shared_worktree_and_out_of_pool_dependency(self) -> None:
        plan = offline_three_repository_preclaim_plan()
        first = plan["proposed_wave"]["lanes"][0]["worktree"]
        second = plan["proposed_wave"]["lanes"][1]["worktree"]
        for field in ("path", "resolved_path", "git_toplevel", "git_common_dir"):
            second[field] = first[field]
        self.assert_error(plan, "shares physical worktree")

        plan = offline_three_repository_preclaim_plan()
        plan["proposed_wave"]["lanes"][0]["scope"]["dependencies"] = [
            f"{OFFLINE_THREE_REPOSITORIES[0]}#999"
        ]
        self.assert_error(plan, "unresolved out-of-pool dependencies")

    def test_cross_repository_identical_local_contract_path_is_safe(self) -> None:
        plan = offline_three_repository_preclaim_plan()
        lanes = plan["proposed_wave"]["lanes"]
        shared_path = lanes[0]["scope"]["write_paths"][0]
        lanes[1]["scope"]["expected_files"] = [shared_path]
        lanes[1]["scope"]["write_paths"] = [shared_path]
        lanes[1]["scope"]["contract_surfaces"] = [shared_path]
        lanes[1]["role_evidence"]["contract_path"] = shared_path
        plan["runtime_preflight"] = runtime_preflight(lanes=lanes)
        self.assertEqual(validate_plan(plan, NOW), [])

    def test_cross_repository_namespaced_contract_remains_shared(self) -> None:
        plan = offline_three_repository_preclaim_plan()
        lanes = plan["proposed_wave"]["lanes"]
        for lane_value in lanes[:2]:
            lane_value["scope"]["contract_surfaces"] = ["schema:match-event/v1"]
        self.assert_error(plan, "shared_contracts must equal derived overlap")
        plan["compatibility"][0]["shared_contracts"] = ["schema:match-event/v1"]
        self.assert_error(plan, "safe verdict has shared or invalidating state")

    def test_cross_repository_one_sided_local_contract_remains_shared(self) -> None:
        plan = offline_three_repository_preclaim_plan()
        lanes = plan["proposed_wave"]["lanes"]
        shared_surface = "docs/contracts/shared.md"
        lanes[0]["scope"]["expected_files"] = [shared_surface]
        lanes[0]["scope"]["write_paths"] = [shared_surface]
        lanes[0]["scope"]["contract_surfaces"] = [shared_surface]
        lanes[0]["role_evidence"]["contract_path"] = shared_surface
        lanes[1]["scope"]["contract_surfaces"] = [shared_surface]
        self.assert_error(plan, "shared_contracts must equal derived overlap")

    def test_safe_verdict_rejects_dependency_or_shared_state(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        plan["compatibility"][0]["dependency_relation"] = "left_depends_on_right"
        self.assert_error(plan, "safe verdict has shared or invalidating state")

    def test_actual_write_overlap_must_be_recorded_and_serialized(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        first_contract = plan["proposed_wave"]["lanes"][0]["role_evidence"]["contract_path"]
        second = plan["proposed_wave"]["lanes"][1]
        second["role_evidence"]["contract_path"] = first_contract
        second["scope"]["expected_files"] = [first_contract]
        second["scope"]["write_paths"] = [first_contract]
        second["scope"]["contract_surfaces"] = [first_contract]
        self.assert_error(plan, "shared_write_paths must equal derived overlap")

    def test_serialized_verdict_requires_order_trigger_barrier_and_bindings(self) -> None:
        plan = preclaim_plan()
        add_second_proposed_lane(plan)
        plan["compatibility"][0]["verdict"] = "concurrent_until_integration_then_serialize"
        self.assert_error(plan, "needs exact integration order")
        self.assert_error(plan, "needs triggers, refresh barrier, and bindings")

    def test_selection_prioritizes_twice_deferred_then_returned_then_oldest(self) -> None:
        candidates = [
            {
                "lane_id": f"{REPOSITORY}#103",
                "status": "ready_queued",
                "eligible": True,
                "ready_since": "2026-07-13T08:00:00Z",
                "eligible_defer_count": 0,
                "finding_ids": [],
                "exclusion_reason": None,
            },
            {
                "lane_id": f"{REPOSITORY}#102",
                "status": "returned",
                "eligible": True,
                "ready_since": "2026-07-13T09:00:00Z",
                "eligible_defer_count": 0,
                "finding_ids": ["F-102"],
                "exclusion_reason": None,
            },
            {
                "lane_id": f"{REPOSITORY}#101",
                "status": "ready_queued",
                "eligible": True,
                "ready_since": "2026-07-13T10:00:00Z",
                "eligible_defer_count": 2,
                "finding_ids": [],
                "exclusion_reason": None,
            },
        ]
        self.assertEqual(
            select_lanes(candidates, 3),
            [f"{REPOSITORY}#101", f"{REPOSITORY}#102", f"{REPOSITORY}#103"],
        )

    def test_skipped_returned_lane_requires_substantive_exclusion_and_correct_selection(self) -> None:
        plan = preclaim_plan()
        queued = copy.deepcopy(plan["proposed_wave"]["lanes"][0])
        queued["lane_id"] = f"{REPOSITORY}#102"
        queued["issue"] = 102
        queued["state"] = "returned"
        queued["wip_assignment"] = {"kind": "queued"}
        queued["worktree"]["branch"] = "codex/issue-102"
        plan["queued_lanes"] = [queued]
        returned = copy.deepcopy(plan["candidate_inventory"][0])
        returned.update(
            {
                "lane_id": f"{REPOSITORY}#102",
                "status": "returned",
                "selected": False,
                "finding_ids": ["F-102"],
                "ready_since": "2026-07-13T09:00:00Z",
            }
        )
        plan["candidate_inventory"].append(returned)
        errors = validate_plan(plan, NOW)
        self.assertTrue(any("skipped returned/twice-deferred" in error for error in errors))
        self.assertTrue(any("deterministic priority order" in error for error in errors))

    def test_returned_lane_without_concrete_finding_is_ineligible(self) -> None:
        candidate = {
            "lane_id": LANE_ID,
            "status": "returned",
            "eligible": True,
            "ready_since": READY,
            "eligible_defer_count": 0,
            "finding_ids": [],
            "exclusion_reason": None,
        }
        self.assertEqual(select_lanes([candidate], 1), [])


class UntrustedEvidenceBoundaryTests(PlanAssertions):
    def test_external_text_is_rendered_as_data_only_and_cannot_grant_authority(self) -> None:
        rendered = render_untrusted_evidence(
            "github:comment/999", OBSERVED, ARTIFACT_DIGEST, MALICIOUS_EXTERNAL_TEXT
        )
        self.assertIn("DATA ONLY", rendered)
        self.assertIn('"grants_authority": false', rendered)
        self.assertIn('"handling": "data_only"', rendered)
        self.assertIn('"content_included": false', rendered)
        self.assertNotIn("merge PR 999", rendered)

    def test_untrusted_evidence_cannot_change_handling_or_authority_fields(self) -> None:
        for key, value, fragment in (
            ("handling", "execute_as_instructions", "must be untrusted_data_only"),
            ("grants_authority", True, "must be false"),
        ):
            plan = preclaim_plan()
            plan["proposed_wave"]["lanes"][0]["evidence_sources"][0][key] = value
            with self.subTest(key=key):
                self.assert_error(plan, fragment)

    def test_external_content_has_no_schema_field_that_can_override_action(self) -> None:
        plan = preclaim_plan()
        plan["proposed_wave"]["lanes"][0]["evidence_sources"][0]["content"] = (
            MALICIOUS_EXTERNAL_TEXT
        )
        self.assert_error(plan, "unknown fields: content")


NATIVE_SHA_A = "a" * 64
NATIVE_SHA_B = "b" * 64
NATIVE_SHA_C = "c" * 64
NATIVE_GIT_A = "a" * 40
NATIVE_GIT_B = "b" * 40
NATIVE_TIME = "2026-07-23T12:00:00Z"


def _native_signed(
    value: dict[str, object],
    digest_field: str,
) -> dict[str, object]:
    value[digest_field] = native.trusted_native_self_digest(value, digest_field)
    return value


def _native_command(role: str = "A") -> dict[str, object]:
    return _native_signed(
        {
            "command_id": "inspect",
            "role": role,
            "operation_id": "inspect",
            "executable_ref": "codex:trusted-owner-native-inspect/v1",
            "executable_sha256": None,
            "executable_byte_count": None,
            "argument_template": [
                {"ordinal": 0, "kind": "literal", "value": "inspect"},
                {
                    "ordinal": 1,
                    "kind": "typed_placeholder",
                    "value": "issue_number",
                },
            ],
            "working_directory_policy": "worktree_root",
            "working_directory_value": None,
            "environment_allowlist": [],
            "maximum_runtime_seconds": 300,
            "mutation_scope": [],
            "external_effects": [],
            "command_sha256": "",
        },
        "command_sha256",
    )


def _native_entry(
    repository_id: int,
    *,
    role: str = "A",
    status: str = "active",
    code_policy: str = "reviewed_command_set_only",
) -> dict[str, object]:
    commands = [] if code_policy == "forbidden" else [_native_command(role)]
    return _native_signed(
        {
            "schema_version": "trusted_owner_repository_entry.v1",
            "repository_id": repository_id,
            "canonical_name": f"tahjali11/repository-{repository_id}",
            "status": status,
            "trust_basis_refs": [
                f"https://github.com/Tahjali11/Mythic-Edge/issues/{743 + repository_id}"
            ],
            "eligible_roles": [role],
            "permitted_operations": ["inspect"],
            "permitted_read_scope": ["docs"],
            "maximum_mutation_scope": [],
            "repository_code_execution_policy": code_policy,
            "approved_commands": commands,
            "protected_surface_restrictions": ["parser_truth"],
            "external_effect_restrictions": [
                "credentials",
                "network",
                "service",
            ],
            "approving_authority_ref": (
                "https://github.com/Tahjali11/Mythic-Edge/issues/744"
            ),
            "approved_at_utc": NATIVE_TIME,
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


def _native_registry(
    entry_count: int = 1,
    *,
    role: str = "A",
    status: str = "active",
    code_policy: str = "reviewed_command_set_only",
) -> dict[str, object]:
    return _native_signed(
        {
            "schema_version": "trusted_owner_repository_registry.v1",
            "profile_id": "trusted_owner_native",
            "coordination_repository_id": 1,
            "coordination_repository_name": "tahjali11/mythic-edge",
            "coordination_issue_number": 744,
            "authorized_claim_actor_ids": [1001],
            "release_state_path": (
                "docs/role_pool/trusted_owner_native_release_state.v1.jsonl"
            ),
            "entries": [
                _native_entry(
                    index,
                    role=role,
                    status=status,
                    code_policy=code_policy,
                )
                for index in range(1, entry_count + 1)
            ],
            "registry_sha256": "",
        },
        "registry_sha256",
    )


def _native_release_record(
    rung: str = "R0",
    *,
    predecessor: dict[str, object] | None = None,
    registry_sha256: str = NATIVE_SHA_C,
) -> dict[str, object]:
    bootstrap = predecessor is None
    rung_number = int(rung.removeprefix("R"))
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_release_record.v1",
            "record_id": f"release.{rung.lower()}",
            "predecessor_record_sha256": (
                None if bootstrap else predecessor["record_sha256"]
            ),
            "from_rung": None if bootstrap else predecessor["to_rung"],
            "to_rung": rung,
            "contract_sha256": NATIVE_SHA_A,
            "skill_tree_sha256": NATIVE_SHA_B,
            "registry_sha256": registry_sha256,
            "validator_bundle_sha256": "d" * 64,
            "observation_receipt_sha256s": (
                [] if bootstrap else ["e" * 64, "f" * 64]
            ),
            "codex_e_review_ref": "review:codex-e",
            "codex_e_review_sha256": "1" * 64,
            "owner_decision_ref": "owner:decision",
            "accepted_at_utc": f"2026-07-23T12:00:{rung_number:02d}Z",
            "record_sha256": "",
        },
        "record_sha256",
    )


def _native_release_rebaseline(
    predecessor: dict[str, object],
    *,
    contract_sha256: str = "9" * 64,
    skill_tree_sha256: str | None = None,
    registry_sha256: str | None = None,
    validator_bundle_sha256: str | None = None,
) -> dict[str, object]:
    return _native_signed(
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
            "skill_tree_sha256": (
                skill_tree_sha256 or str(predecessor["skill_tree_sha256"])
            ),
            "predecessor_registry_sha256": predecessor["registry_sha256"],
            "registry_sha256": (
                registry_sha256 or str(predecessor["registry_sha256"])
            ),
            "predecessor_validator_bundle_sha256": predecessor[
                "validator_bundle_sha256"
            ],
            "validator_bundle_sha256": (
                validator_bundle_sha256
                or str(predecessor["validator_bundle_sha256"])
            ),
            "observation_receipt_sha256s": [],
            "codex_e_review_ref": "review:codex-e-rebaseline",
            "codex_e_review_sha256": "2" * 64,
            "owner_decision_ref": "owner:rebaseline-decision",
            "accepted_at_utc": "2026-07-23T12:00:01Z",
            "record_sha256": "",
        },
        "record_sha256",
    )


def _native_lane(
    repository_id: int,
    role: str = "A",
    *,
    inspect_only: bool = False,
) -> dict[str, object]:
    return _native_signed(
        {
            "lane_id": f"lane.{repository_id}",
            "repository_id": repository_id,
            "canonical_name": f"tahjali11/repository-{repository_id}",
            "issue_url": (
                f"https://github.com/tahjali11/repository-{repository_id}/issues/"
                f"{743 + repository_id}"
            ),
            "role": role,
            "operation_id": "inspect",
            "base_ref": "refs/heads/main",
            "base_sha": NATIVE_GIT_A,
            "predecessor_packet_sha256": None,
            "command_ids": [] if inspect_only else ["inspect"],
            "read_scope": ["docs"],
            "mutation_scope": [],
            "protected_surfaces": ["parser_truth"],
            "validation_command_ids": [] if inspect_only else ["inspect"],
            "expected_artifact_paths": [],
            "stop_conditions": ["Stop on authority drift."],
            "lane_packet_sha256": "",
        },
        "lane_packet_sha256",
    )


def _native_request(
    registry: dict[str, object],
    *,
    lane_count: int = 1,
    release_record: dict[str, object] | None = None,
    role: str = "A",
    inspect_only: bool = False,
) -> dict[str, object]:
    release_record = release_record or _native_release_record(
        registry_sha256=registry["registry_sha256"],
    )
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_request.v1",
            "request_id": f"request.{lane_count}",
            "mode": "safe",
            "automation_series_id": None,
            "predecessor_request_sha256": None,
            "requested_role": role,
            "skill_tree_sha256": NATIVE_SHA_B,
            "registry_sha256": registry["registry_sha256"],
            "release_state_record_sha256": release_record["record_sha256"],
            "requested_at_utc": NATIVE_TIME,
            "lanes": [
                _native_lane(
                    index,
                    role,
                    inspect_only=inspect_only,
                )
                for index in range(1, lane_count + 1)
            ],
            "request_sha256": "",
        },
        "request_sha256",
    )


def _native_handoff() -> dict[str, object]:
    return _native_signed(
        {
            "status": "complete",
            "next_role": "E",
            "source_artifact_paths": ["docs/result.md"],
            "finding_ids": [],
            "stop_reason": None,
            "handoff_sha256": "",
        },
        "handoff_sha256",
    )


def _native_result(request: dict[str, object]) -> dict[str, object]:
    lane = request["lanes"][0]
    assert isinstance(lane, dict)
    handoff = _native_handoff()
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_result.v1",
            "request_sha256": request["request_sha256"],
            "claim_observation_sha256": "2" * 64,
            "wave_id": "wave.1",
            "lane_id": lane["lane_id"],
            "worktree_observation_sha256": "3" * 64,
            "task_receipt_sha256": "4" * 64,
            "task_id": "task.1",
            "repository_id": lane["repository_id"],
            "issue_url": lane["issue_url"],
            "role": lane["role"],
            "operation_id": lane["operation_id"],
            "base_sha": lane["base_sha"],
            "head_sha": NATIVE_GIT_B,
            "result": "completed",
            "files_changed": [],
            "validation": [
                {
                    "command_id": "inspect",
                    "status": "passed",
                    "exit_code": 0,
                    "evidence_sha256": "5" * 64,
                }
            ],
            "handoff": handoff,
            "authority_flags": {
                field: False for field in native.TRUSTED_NATIVE_AUTHORITY_FIELDS
            },
            "result_packet_sha256": "",
        },
        "result_packet_sha256",
    )


def _native_worktree() -> dict[str, object]:
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_worktree_observation.v1",
            "repository_id": 1,
            "canonical_name": "tahjali11/repository-1",
            "base_sha": NATIVE_GIT_A,
            "branch_ref": "refs/heads/codex/inspect",
            "branch_head_sha": NATIVE_GIT_A,
            "registered_top_level_sha256": "6" * 64,
            "common_directory_sha256": "7" * 64,
            "remote_identity_sha256": "8" * 64,
            "ordinary_nonreparse": True,
            "observed_at_utc": NATIVE_TIME,
            "worktree_observation_sha256": "",
        },
        "worktree_observation_sha256",
    )


def _native_task_request(
    request: dict[str, object],
    worktree: dict[str, object],
) -> dict[str, object]:
    lane = request["lanes"][0]
    assert isinstance(lane, dict)
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_task_request.v1",
            "request_sha256": request["request_sha256"],
            "claim_observation_sha256": "2" * 64,
            "lane_packet_sha256": lane["lane_packet_sha256"],
            "repository_id": lane["repository_id"],
            "issue_url": lane["issue_url"],
            "role": lane["role"],
            "base_sha": lane["base_sha"],
            "worktree_observation_sha256": worktree[
                "worktree_observation_sha256"
            ],
            "context_mode": "isolated_packet_only",
            "fork_turns": "none",
            "issued_at_utc": NATIVE_TIME,
            "task_request_sha256": "",
        },
        "task_request_sha256",
    )


def _native_task_receipt(
    request: dict[str, object],
) -> dict[str, object]:
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_task_receipt.v1",
            "task_request_sha256": request["task_request_sha256"],
            "task_id": "task.1",
            "accepted_at_utc": NATIVE_TIME,
            "platform_receipt_ref": "synthetic:receipt",
            "platform_receipt_sha256": "9" * 64,
            "task_receipt_sha256": "",
        },
        "task_receipt_sha256",
    )


def _native_windows_preflight(
    *,
    os_name: str | None = "nt",
    sys_platform: str | None = "win32",
    host_observed: bool = True,
    capability_available: bool = True,
    capability_compatible: bool = True,
) -> dict[str, object]:
    host = native.TrustedNativeRuntimeHostObservation(
        os_name=os_name,
        sys_platform=sys_platform,
        observation_succeeded=host_observed,
        source="synthetic_test_double",
    )
    capability = native.TrustedNativeTaskCapabilityObservation(
        launcher_identity="codex:native-task-create/v1",
        available=capability_available,
        compatible=capability_compatible,
        request_binding=True,
        one_task_only=True,
        receipt_binding=True,
        timeout_enforced=True,
        unknown_outcome_fail_closed=True,
        automatic_retry_forbidden=True,
        fallback_forbidden=True,
        source="synthetic_test_double",
    )
    return native.evaluate_trusted_native_execution_preflight(
        "dispatch",
        host,
        capability,
    )


def _native_claim_event(
    request: dict[str, object],
    *,
    claim_id: str = "claim.1",
    event_id: str = "event.1",
    wave_ordinal: int = 1,
    state: str = "reserved",
    predecessor: str | None = None,
    issued_at: str = NATIVE_TIME,
    expires_at: str = "2026-07-23T13:00:00Z",
    terminal_binding: dict[str, object] | None = None,
    device_sha256: str = "a" * 64,
    coordinator_sha256: str = "b" * 64,
) -> dict[str, object]:
    lanes = request["lanes"]
    assert isinstance(lanes, list)
    resources = {
        "project:trusted_owner_native:v1",
        f"wave_slot:{wave_ordinal}",
    }
    for lane in lanes:
        assert isinstance(lane, dict)
        issue_number = lane["issue_url"].rsplit("/", 1)[1]
        resources.update(
            {
                f"repository:{lane['repository_id']}",
                f"issue:{lane['repository_id']}:{issue_number}",
                f"lane:{lane['lane_id']}",
            }
        )
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_claim_event.v1",
            "event_id": event_id,
            "claim_id": claim_id,
            "predecessor_observation_sha256": predecessor,
            "request_sha256": request["request_sha256"],
            "wave_id": f"wave.{wave_ordinal}",
            "wave_ordinal": wave_ordinal,
            "coordinator_id_sha256": coordinator_sha256,
            "device_id_sha256": device_sha256,
            "lane_ids": [lane["lane_id"] for lane in lanes],
            "resource_keys": sorted(resources, key=lambda item: item.encode()),
            "state": state,
            "issued_at_utc": issued_at,
            "expires_at_utc": expires_at,
            "terminal_binding": terminal_binding,
            "event_sha256": "",
        },
        "event_sha256",
    )


def _native_observation(
    event: dict[str, object],
    *,
    comment_id: int,
    author_id: int = 1001,
    observed_at: str = NATIVE_TIME,
) -> dict[str, object]:
    body = native.trusted_native_canonical_bytes(event)
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_claim_observation.v1",
            "coordination_repository_id": 1,
            "coordination_issue_number": 744,
            "server_comment_id": comment_id,
            "server_author_id": author_id,
            "server_author_type": "User",
            "server_created_at": observed_at,
            "server_updated_at": observed_at,
            "event_schema_version": event["schema_version"],
            "event_sha256": event["event_sha256"],
            "comment_body_byte_count": len(body),
            "comment_body_sha256": hashlib.sha256(body).hexdigest(),
            "claim_observation_sha256": "",
        },
        "claim_observation_sha256",
    )


def _native_snapshot(
    observations: list[dict[str, object]],
    *,
    page_count: int = 1,
) -> dict[str, object]:
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_claim_snapshot.v1",
            "coordination_repository_id": 1,
            "coordination_issue_number": 744,
            "server_high_water_comment_id": max(
                observation["server_comment_id"] for observation in observations
            ),
            "page_count": page_count,
            "observation_sha256s": [
                observation["claim_observation_sha256"]
                for observation in observations
            ],
            "pagination_complete": True,
            "snapshot_sha256": "",
        },
        "snapshot_sha256",
    )


def _native_release_binding(
    worktree: dict[str, object],
    task_receipt: dict[str, object],
    result: dict[str, object],
    *,
    released_at: str,
) -> dict[str, object]:
    handoff = result["handoff"]
    assert isinstance(handoff, dict)
    return _native_signed(
        {
            "schema_version": "trusted_owner_native_claim_release_binding.v1",
            "worktree_observation_sha256": worktree[
                "worktree_observation_sha256"
            ],
            "task_receipt_sha256": task_receipt["task_receipt_sha256"],
            "result_packet_sha256": result["result_packet_sha256"],
            "handoff_sha256": handoff["handoff_sha256"],
            "released_at_utc": released_at,
            "release_binding_sha256": "",
        },
        "release_binding_sha256",
    )


def _native_automatic_predecessor_chain() -> tuple[dict[str, object], ...]:
    registry = _native_registry()
    predecessor = _native_request(registry)
    predecessor["mode"] = "automatic"
    predecessor["automation_series_id"] = "series.1"
    predecessor["request_sha256"] = native.trusted_native_self_digest(
        predecessor,
        "request_sha256",
    )

    reservation = _native_claim_event(predecessor)
    reservation_observation = _native_observation(reservation, comment_id=100)
    winning_event = _native_claim_event(
        predecessor,
        event_id="event.predecessor.running",
        state="confirmed_running",
        predecessor=reservation_observation["claim_observation_sha256"],
        issued_at="2026-07-23T12:00:10Z",
    )
    winning_observation = _native_observation(
        winning_event,
        comment_id=101,
        observed_at="2026-07-23T12:00:10Z",
    )

    result = _native_result(predecessor)
    handoff = result["handoff"]
    assert isinstance(handoff, dict)
    handoff["next_role"] = "B"
    handoff["handoff_sha256"] = native.trusted_native_self_digest(
        handoff,
        "handoff_sha256",
    )
    worktree = _native_worktree()
    task_request = _native_task_request(predecessor, worktree)
    task_request["claim_observation_sha256"] = winning_observation[
        "claim_observation_sha256"
    ]
    task_request["task_request_sha256"] = native.trusted_native_self_digest(
        task_request,
        "task_request_sha256",
    )
    task_receipt = _native_task_receipt(task_request)
    result["claim_observation_sha256"] = winning_observation[
        "claim_observation_sha256"
    ]
    result["wave_id"] = winning_event["wave_id"]
    result["worktree_observation_sha256"] = worktree[
        "worktree_observation_sha256"
    ]
    result["task_receipt_sha256"] = task_receipt["task_receipt_sha256"]
    result["task_id"] = task_receipt["task_id"]
    result["result_packet_sha256"] = native.trusted_native_self_digest(
        result,
        "result_packet_sha256",
    )

    released_at = "2026-07-23T12:00:20Z"
    release = _native_claim_event(
        predecessor,
        event_id="event.predecessor.release",
        state="released",
        predecessor=winning_observation["claim_observation_sha256"],
        issued_at=released_at,
        terminal_binding=_native_release_binding(
            worktree,
            task_receipt,
            result,
            released_at=released_at,
        ),
    )

    successor = _native_request(registry)
    successor["request_id"] = "request.successor"
    successor["mode"] = "automatic"
    successor["automation_series_id"] = "series.1"
    successor["predecessor_request_sha256"] = predecessor["request_sha256"]
    successor["requested_role"] = "B"
    successor_lane = successor["lanes"][0]
    assert isinstance(successor_lane, dict)
    successor_lane["role"] = "B"
    successor_lane["predecessor_packet_sha256"] = result["result_packet_sha256"]
    successor_lane["lane_packet_sha256"] = native.trusted_native_self_digest(
        successor_lane,
        "lane_packet_sha256",
    )
    successor["request_sha256"] = native.trusted_native_self_digest(
        successor,
        "request_sha256",
    )
    return (
        predecessor,
        result,
        winning_event,
        winning_observation,
        release,
        successor,
        worktree,
        task_receipt,
    )


def _native_resolution_event(
    claim_id: str,
    trigger_observation_sha256: str,
    trigger_snapshot_sha256: str,
) -> dict[str, object]:
    return _native_signed(
        {
            "schema_version": (
                "trusted_owner_native_claim_resolution_event.v1"
            ),
            "event_id": "resolution.1",
            "claim_id": claim_id,
            "trigger_observation_sha256": trigger_observation_sha256,
            "trigger_snapshot_sha256": trigger_snapshot_sha256,
            "resolution": "known_no_task_created",
            "worktree_observation_sha256": None,
            "task_receipt_sha256": None,
            "result_packet_sha256": None,
            "handoff_sha256": None,
            "cleanup_evidence_sha256": None,
            "review_ref": "review:reconciliation",
            "review_receipt_sha256": "3" * 64,
            "issued_at_utc": "2026-07-23T12:00:20Z",
            "event_sha256": "",
        },
        "event_sha256",
    )


class TrustedOwnerNativeProfileTests(unittest.TestCase):
    def test_cli_emits_only_fixed_guidance_for_plan_validation_errors(self) -> None:
        private_detail = "invented_" + "secret_" + "material"
        document = inspect_plan()
        document[private_detail] = False
        self.assertTrue(
            any(private_detail in error for error in validate_plan(document, NOW))
        )

        with tempfile.TemporaryDirectory() as directory:
            document_path = Path(directory) / "plan.json"
            document_path.write_text(json.dumps(document), encoding="utf-8")
            stderr = io.StringIO()
            with mock.patch.object(native.sys, "stderr", stderr):
                exit_code = native.main(
                    [
                        str(document_path),
                        "--offline-synthetic-fixture",
                        "--now",
                        OBSERVED,
                    ]
                )

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "role-pool document invalid:\n"
            "- cli: plan validation requires --discovery\n",
        )
        self.assertNotIn(private_detail, stderr.getvalue())

    def test_cli_does_not_echo_trusted_native_validation_details(self) -> None:
        private_detail = "invented_" + "secret_" + "material"
        document = _native_request(_native_registry())
        document["unexpected_detail"] = private_detail

        with tempfile.TemporaryDirectory() as directory:
            document_path = Path(directory) / "request.json"
            document_path.write_text(json.dumps(document), encoding="utf-8")
            stderr = io.StringIO()
            with (
                mock.patch.object(
                    native,
                    "validate_trusted_native_document",
                    side_effect=lambda value: [str(value["unexpected_detail"])],
                ),
                mock.patch.object(native.sys, "stderr", stderr),
            ):
                exit_code = native.main([str(document_path)])

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "role-pool document invalid:\n- validation details withheld\n",
        )
        self.assertNotIn(private_detail, stderr.getvalue())

    def test_canonical_json_and_closed_schema_fail_closed(self) -> None:
        registry = _native_registry()
        text = native.trusted_native_canonical_bytes(registry).decode("utf-8")

        self.assertEqual(native.parse_trusted_native_json(text), registry)
        with self.assertRaisesRegex(
            native.TrustedNativePacketError,
            "duplicate_json_key",
        ):
            native.parse_trusted_native_json('{"a":1,"a":2}\n')
        with self.assertRaisesRegex(
            native.TrustedNativePacketError,
            "canonical_bytes_invalid",
        ):
            native.parse_trusted_native_json(json.dumps(registry) + "\n")

        unknown = copy.deepcopy(registry)
        unknown["unexpected"] = False
        self.assertIn(
            "registry:fields_or_order_invalid",
            native.validate_trusted_native_registry(unknown),
        )
        wrong_type = copy.deepcopy(registry)
        wrong_type["coordination_repository_id"] = True
        wrong_type["registry_sha256"] = native.trusted_native_self_digest(
            wrong_type,
            "registry_sha256",
        )
        self.assertIn(
            "registry.coordination_repository_id:value_invalid",
            native.validate_trusted_native_registry(wrong_type),
        )

    def test_registry_identity_transitions_and_request_lane_limits(self) -> None:
        for lane_count in (1, 2, 3):
            registry = _native_registry(lane_count)
            release = _native_release_record(
                registry_sha256=registry["registry_sha256"],
            )
            request = _native_request(
                registry,
                lane_count=lane_count,
                release_record=release,
            )
            self.assertEqual(native.validate_trusted_native_registry(registry), [])
            self.assertEqual(
                native.validate_trusted_native_request(
                    request,
                    registry=registry,
                    release_record=release,
                ),
                [],
            )

        registry = _native_registry(4)
        too_many = _native_request(registry, lane_count=4)
        self.assertIn(
            "request.lanes:lane_count_invalid",
            native.validate_trusted_native_request(too_many),
        )
        empty = _native_request(_native_registry(), lane_count=1)
        empty["lanes"] = []
        empty["request_sha256"] = native.trusted_native_self_digest(
            empty,
            "request_sha256",
        )
        self.assertIn(
            "request.lanes:lane_count_invalid",
            native.validate_trusted_native_request(empty),
        )

        duplicate = _native_registry(2)
        duplicate["entries"][1]["repository_id"] = 1
        duplicate["entries"][1]["entry_sha256"] = native.trusted_native_self_digest(
            duplicate["entries"][1],
            "entry_sha256",
        )
        duplicate["registry_sha256"] = native.trusted_native_self_digest(
            duplicate,
            "registry_sha256",
        )
        self.assertIn(
            "registry.entries:duplicate_repository_id",
            native.validate_trusted_native_registry(duplicate),
        )

        before = _native_registry()
        suspended = copy.deepcopy(before)
        suspended["entries"][0]["status"] = "suspended"
        suspended["entries"][0]["entry_sha256"] = native.trusted_native_self_digest(
            suspended["entries"][0],
            "entry_sha256",
        )
        suspended["registry_sha256"] = native.trusted_native_self_digest(
            suspended,
            "registry_sha256",
        )
        self.assertEqual(
            native.validate_trusted_native_registry_transition(before, suspended),
            [],
        )
        renamed = copy.deepcopy(before)
        renamed["entries"][0]["canonical_name"] = "tahjali11/renamed"
        renamed["entries"][0]["entry_sha256"] = native.trusted_native_self_digest(
            renamed["entries"][0],
            "entry_sha256",
        )
        renamed["registry_sha256"] = native.trusted_native_self_digest(
            renamed,
            "registry_sha256",
        )
        self.assertIn(
            "registry_transition:rename_requires_review",
            native.validate_trusted_native_registry_transition(before, renamed),
        )
        transferred = copy.deepcopy(before)
        transferred["authorized_claim_actor_ids"] = [2002]
        transferred["registry_sha256"] = native.trusted_native_self_digest(
            transferred,
            "registry_sha256",
        )
        self.assertIn(
            "registry_transition:authorized_claim_actors_changed",
            native.validate_trusted_native_registry_transition(before, transferred),
        )

    def test_request_authority_and_release_bindings_fail_closed(self) -> None:
        registry = _native_registry()
        release = _native_release_record(
            registry_sha256=registry["registry_sha256"],
        )

        inactive_registry = _native_registry(status="suspended")
        inactive_release = _native_release_record(
            registry_sha256=inactive_registry["registry_sha256"],
        )
        inactive_request = _native_request(
            inactive_registry,
            release_record=inactive_release,
        )
        self.assertIn(
            "request:repository_inactive",
            native.validate_trusted_native_request(
                inactive_request,
                registry=inactive_registry,
                release_record=inactive_release,
            ),
        )

        mutations = (
            ("role_not_allowed", "role", "D"),
            ("operation_not_allowed", "operation_id", "unreviewed"),
            ("command_not_approved", "validation_command_ids", ["unreviewed"]),
            (
                "protected_surface_classification_mismatch",
                "protected_surfaces",
                ["workbook_schema"],
            ),
        )
        for expected_code, field, value in mutations:
            request = _native_request(registry, release_record=release)
            lane = request["lanes"][0]
            assert isinstance(lane, dict)
            if field == "role":
                request["requested_role"] = value
            lane[field] = value
            lane["lane_packet_sha256"] = native.trusted_native_self_digest(
                lane,
                "lane_packet_sha256",
            )
            request["request_sha256"] = native.trusted_native_self_digest(
                request,
                "request_sha256",
            )
            self.assertIn(
                f"request:{expected_code}",
                native.validate_trusted_native_request(
                    request,
                    registry=registry,
                    release_record=release,
                ),
            )

        stale_skill_release = copy.deepcopy(release)
        stale_skill_release["skill_tree_sha256"] = NATIVE_SHA_A
        stale_skill_release["record_sha256"] = native.trusted_native_self_digest(
            stale_skill_release,
            "record_sha256",
        )
        stale_skill_request = _native_request(
            registry,
            release_record=stale_skill_release,
        )
        self.assertIn(
            "request:skill_tree_digest_mismatch",
            native.validate_trusted_native_request(
                stale_skill_request,
                registry=registry,
                release_record=stale_skill_release,
            ),
        )

        stale_registry_release = _native_release_record(
            registry_sha256=NATIVE_SHA_A,
        )
        stale_registry_request = _native_request(
            registry,
            release_record=stale_registry_release,
        )
        self.assertIn(
            "request:release_registry_digest_mismatch",
            native.validate_trusted_native_request(
                stale_registry_request,
                registry=registry,
                release_record=stale_registry_release,
            ),
        )

    def test_request_binds_issue_repository_to_registry_identity(self) -> None:
        registry = _native_registry()
        release = _native_release_record(
            registry_sha256=registry["registry_sha256"],
        )
        request = _native_request(registry, release_record=release)
        lane = request["lanes"][0]
        assert isinstance(lane, dict)
        lane["issue_url"] = "https://github.com/tahjali11/mythic-edge/issues/744"
        lane["lane_packet_sha256"] = native.trusted_native_self_digest(
            lane,
            "lane_packet_sha256",
        )
        request["request_sha256"] = native.trusted_native_self_digest(
            request,
            "request_sha256",
        )

        self.assertIn(
            "request:repository_identity_mismatch",
            native.validate_trusted_native_request(
                request,
                registry=registry,
                release_record=release,
            ),
        )

    def test_automatic_successor_requires_exact_released_predecessor(self) -> None:
        (
            predecessor,
            predecessor_result,
            winning_event,
            winning_observation,
            predecessor_release,
            successor,
            _worktree,
            _task_receipt,
        ) = _native_automatic_predecessor_chain()

        self.assertEqual(
            native.validate_trusted_native_request(
                successor,
                predecessor_request=predecessor,
                predecessor_claim_events=[winning_event],
                predecessor_claim_observations=[winning_observation],
                predecessor_results=[predecessor_result],
                predecessor_release_events=[predecessor_release],
            ),
            [],
        )
        self.assertIn(
            "request:automatic_predecessor_evidence_required",
            native.validate_trusted_native_request(successor),
        )

        stale_request = copy.deepcopy(predecessor)
        stale_request["requested_at_utc"] = "2026-07-23T12:00:01Z"
        stale_request["request_sha256"] = native.trusted_native_self_digest(
            stale_request,
            "request_sha256",
        )
        self.assertIn(
            "request:predecessor_request_mismatch",
            native.validate_trusted_native_request(
                successor,
                predecessor_request=stale_request,
                predecessor_claim_events=[winning_event],
                predecessor_claim_observations=[winning_observation],
                predecessor_results=[predecessor_result],
                predecessor_release_events=[predecessor_release],
            ),
        )

        stale_result = copy.deepcopy(predecessor_result)
        stale_result["head_sha"] = NATIVE_GIT_A
        stale_result["result_packet_sha256"] = native.trusted_native_self_digest(
            stale_result,
            "result_packet_sha256",
        )
        self.assertIn(
            "request:predecessor_packet_mismatch",
            native.validate_trusted_native_request(
                successor,
                predecessor_request=predecessor,
                predecessor_claim_events=[winning_event],
                predecessor_claim_observations=[winning_observation],
                predecessor_results=[stale_result],
                predecessor_release_events=[predecessor_release],
            ),
        )

        cross_series = copy.deepcopy(predecessor)
        cross_series["automation_series_id"] = "series.other"
        cross_series["request_sha256"] = native.trusted_native_self_digest(
            cross_series,
            "request_sha256",
        )
        cross_series_successor = copy.deepcopy(successor)
        cross_series_successor["predecessor_request_sha256"] = cross_series[
            "request_sha256"
        ]
        cross_series_successor["request_sha256"] = native.trusted_native_self_digest(
            cross_series_successor,
            "request_sha256",
        )
        self.assertIn(
            "request:predecessor_series_mismatch",
            native.validate_trusted_native_request(
                cross_series_successor,
                predecessor_request=cross_series,
                predecessor_claim_events=[winning_event],
                predecessor_claim_observations=[winning_observation],
                predecessor_results=[predecessor_result],
                predecessor_release_events=[predecessor_release],
            ),
        )

        self.assertIn(
            "request:predecessor_result_count_mismatch",
            native.validate_trusted_native_request(
                successor,
                predecessor_request=predecessor,
                predecessor_claim_events=[winning_event],
                predecessor_claim_observations=[winning_observation],
                predecessor_results=[predecessor_result, predecessor_result],
                predecessor_release_events=[
                    predecessor_release,
                    predecessor_release,
                ],
            ),
        )
        self.assertIn(
            "request:predecessor_evidence_forbidden",
            native.validate_trusted_native_request(
                predecessor,
                predecessor_request=predecessor,
                predecessor_claim_events=[winning_event],
                predecessor_claim_observations=[winning_observation],
                predecessor_results=[predecessor_result],
                predecessor_release_events=[predecessor_release],
            ),
        )

        self.assertIn(
            "request:automatic_predecessor_evidence_required",
            native.validate_trusted_native_request(
                successor,
                predecessor_request=predecessor,
                predecessor_claim_events=[winning_event],
                predecessor_claim_observations=[winning_observation],
                predecessor_results=[predecessor_result],
            ),
        )

    def test_automatic_successor_rejects_redigested_unowned_fields(self) -> None:
        for case in (
            "result_request",
            "result_wave",
            "claim_observation",
            "validation_plan",
            "release_wave",
        ):
            with self.subTest(case=case):
                (
                    predecessor,
                    result,
                    winning_event,
                    winning_observation,
                    release,
                    successor,
                    worktree,
                    task_receipt,
                ) = _native_automatic_predecessor_chain()

                if case == "result_request":
                    result["request_sha256"] = NATIVE_SHA_C
                elif case == "result_wave":
                    result["wave_id"] = "wave.other"
                elif case == "claim_observation":
                    result["claim_observation_sha256"] = NATIVE_SHA_C
                elif case == "validation_plan":
                    result["validation"][0]["command_id"] = "other"
                else:
                    release["wave_id"] = "wave.other"

                if case != "release_wave":
                    result["result_packet_sha256"] = (
                        native.trusted_native_self_digest(
                            result,
                            "result_packet_sha256",
                        )
                    )
                    release["terminal_binding"] = _native_release_binding(
                        worktree,
                        task_receipt,
                        result,
                        released_at=release["issued_at_utc"],
                    )
                    successor_lane = successor["lanes"][0]
                    assert isinstance(successor_lane, dict)
                    successor_lane["predecessor_packet_sha256"] = result[
                        "result_packet_sha256"
                    ]
                    successor_lane["lane_packet_sha256"] = (
                        native.trusted_native_self_digest(
                            successor_lane,
                            "lane_packet_sha256",
                        )
                    )
                    successor["request_sha256"] = native.trusted_native_self_digest(
                        successor,
                        "request_sha256",
                    )
                release["event_sha256"] = native.trusted_native_self_digest(
                    release,
                    "event_sha256",
                )

                expected_error = {
                    "result_request": "request:predecessor_result_invalid",
                    "result_wave": "request:predecessor_release_mismatch",
                    "claim_observation": "request:predecessor_claim_mismatch",
                    "validation_plan": "request:predecessor_result_invalid",
                    "release_wave": "request:predecessor_release_mismatch",
                }[case]
                self.assertIn(
                    expected_error,
                    native.validate_trusted_native_request(
                        successor,
                        predecessor_request=predecessor,
                        predecessor_claim_events=[winning_event],
                        predecessor_claim_observations=[winning_observation],
                        predecessor_results=[result],
                        predecessor_release_events=[release],
                    ),
                )

    def test_relative_paths_reject_supported_wildcard_forms(self) -> None:
        for path in (
            "src/*.py",
            "src/file?.py",
            "src/[ab].py",
            "src/[!a].py",
        ):
            with self.subTest(path=path):
                self.assertFalse(native._native_is_relative_path(path))

    def test_command_resolution_is_nonexecuting_and_has_no_fallback(self) -> None:
        registry = _native_registry()
        lane = _native_lane(1)
        resolved = native.resolve_trusted_native_command(
            registry,
            lane,
            "inspect",
            {"issue_number": "744"},
        )
        self.assertEqual(resolved["status"], "approved_command_resolved_nonexecuting")
        self.assertIs(resolved["execution_performed"], False)
        self.assertEqual(
            resolved["launcher_identity"],
            "codex:native-task-create/v1",
        )
        self.assertNotIn("shell", resolved)

        self.assertEqual(
            native.resolve_trusted_native_command(
                registry,
                lane,
                "unapproved",
                {},
            ),
            {"status": "blocked_command_not_approved"},
        )
        self.assertEqual(
            native.resolve_trusted_native_command(
                registry,
                lane,
                "inspect",
                {"issue_number": "744", "output_path": "docs/out"},
            ),
            {"status": "blocked_command_not_approved"},
        )
        environment = native.resolve_trusted_native_command(
            registry,
            lane,
            "inspect",
            {"issue_number": "744"},
            environment_names=["PATH"],
        )
        self.assertEqual(environment, {"status": "blocked_command_not_approved"})
        for unsafe_value in ("744;whoami", "*", "@response-file"):
            self.assertEqual(
                native.resolve_trusted_native_command(
                    registry,
                    lane,
                    "inspect",
                    {"issue_number": unsafe_value},
                ),
                {"status": "blocked_command_not_approved"},
            )

        ambient = _native_registry()
        ambient["entries"][0]["approved_commands"][0]["executable_ref"] = "python"
        ambient["entries"][0]["approved_commands"][0][
            "command_sha256"
        ] = native.trusted_native_self_digest(
            ambient["entries"][0]["approved_commands"][0],
            "command_sha256",
        )
        ambient["entries"][0]["entry_sha256"] = native.trusted_native_self_digest(
            ambient["entries"][0],
            "entry_sha256",
        )
        ambient["registry_sha256"] = native.trusted_native_self_digest(
            ambient,
            "registry_sha256",
        )
        self.assertIn(
            "registry.entries[0].approved_commands[0].executable_ref:"
            "ambient_path_forbidden",
            native.validate_trusted_native_registry(ambient),
        )

        shell_literal = _native_registry()
        shell_literal["entries"][0]["approved_commands"][0][
            "argument_template"
        ][0]["value"] = "inspect&&hook"
        shell_literal["entries"][0]["approved_commands"][0][
            "command_sha256"
        ] = native.trusted_native_self_digest(
            shell_literal["entries"][0]["approved_commands"][0],
            "command_sha256",
        )
        shell_literal["entries"][0][
            "entry_sha256"
        ] = native.trusted_native_self_digest(
            shell_literal["entries"][0],
            "entry_sha256",
        )
        shell_literal["registry_sha256"] = native.trusted_native_self_digest(
            shell_literal,
            "registry_sha256",
        )
        self.assertIn(
            "registry.entries[0].approved_commands[0].argument_template[0]:"
            "literal_forbidden_syntax",
            native.validate_trusted_native_registry(shell_literal),
        )

    def test_synthetic_native_adapter_is_single_use_and_never_live(self) -> None:
        registry = _native_registry()
        request = _native_request(registry)
        worktree = _native_worktree()
        task_request = _native_task_request(request, worktree)

        self.assertEqual(native.validate_trusted_native_worktree_observation(worktree), [])
        self.assertEqual(native.validate_trusted_native_task_request(task_request), [])
        blocked = native.trusted_native_task_create_once(task_request)
        self.assertEqual(
            blocked,
            {
                "status": "blocked_request_or_packet_invalid",
                "receipt": None,
            },
        )

        adapter = native.TrustedNativeSyntheticTaskAdapter(_native_task_receipt)
        accepted = native.trusted_native_task_create_once(
            task_request,
            synthetic_adapter=adapter,
        )
        self.assertEqual(
            accepted["status"],
            "synthetic_task_receipt_accepted_non_live",
        )
        self.assertEqual(
            native.validate_trusted_native_task_receipt(
                accepted["receipt"],
                request=task_request,
            ),
            [],
        )
        retry = native.trusted_native_task_create_once(
            task_request,
            synthetic_adapter=adapter,
        )
        self.assertEqual(retry, {"status": "failed_lane_known", "receipt": None})

    def test_direct_app_adapter_is_selected_only_with_exact_cross_bindings(
        self,
    ) -> None:
        registry = _native_registry(role="E", code_policy="forbidden")
        request = _native_request(
            registry,
            role="E",
            inspect_only=True,
        )
        lane = request["lanes"][0]
        self.assertIsInstance(lane, dict)
        assert isinstance(lane, dict)
        task_request = _native_task_request(request, _native_worktree())
        project_id = "synthetic-private-project"
        operation_id = app_direct.build_operation_binding(
            task_request=task_request,
            lane_packet=lane,
            project_id=project_id,
        )[2]
        handoff = _native_signed(
            {
                "status": "complete",
                "next_role": "F",
                "source_artifact_paths": ["docs/result.md"],
                "finding_ids": [],
                "stop_reason": None,
                "handoff_sha256": "",
            },
            "handoff_sha256",
        )

        class FakeDirectClient:
            synthetic_only = True

            def __init__(self) -> None:
                self.create_call_count = 0
                self.follow_up_message_count = 0
                self.replacement_task_count = 0
                self.real_operation_call_count = 0

            def create_thread(
                self,
                *,
                target: Mapping[str, object],
                prompt: str,
            ) -> object:
                self.create_call_count += 1
                self.target = dict(target)
                self.prompt = prompt
                return {"threadId": "thread.synthetic.direct"}

            def list_threads(self) -> object:
                return {"threads": []}

            def read_thread(self, thread_id: str) -> object:
                return {
                    "threadId": thread_id,
                    "projectId": project_id,
                    "repositoryId": task_request["repository_id"],
                    "worktreeObservationSha256": task_request[
                        "worktree_observation_sha256"
                    ],
                    "branchRef": lane["base_ref"],
                    "baseSha": lane["base_sha"],
                    "operationId": operation_id,
                    "status": "completed",
                    "handoffs": [handoff],
                    "postWorktreeObservationSha256": "9" * 64,
                    "effectCounts": {
                        field: 0 for field in app_direct.EFFECT_COUNT_FIELDS
                    },
                }

        moments = iter(
            (
                datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc),
                datetime(2026, 8, 4, 12, 5, tzinfo=timezone.utc),
            )
        )
        client = FakeDirectClient()
        adapter = app_direct.TrustedNativeAppDirectTaskAdapter(
            task_request=task_request,
            lane_packet=lane,
            registry_entry=registry["entries"][0],
            project_id=project_id,
            client=client,
            clock=lambda: next(moments),
        )
        accepted = native.trusted_native_app_direct_task_create_once(
            task_request,
            adapter=adapter,
        )
        self.assertEqual(
            accepted["status"],
            "synthetic_app_native_receipt_accepted_non_live",
        )
        self.assertEqual(client.create_call_count, 1)
        self.assertEqual(client.follow_up_message_count, 0)
        self.assertEqual(client.replacement_task_count, 0)
        self.assertEqual(client.real_operation_call_count, 0)
        self.assertNotIn(project_id, repr(accepted))
        self.assertEqual(
            native.validate_trusted_native_task_receipt(
                accepted["receipt"],
                request=task_request,
            ),
            [],
        )

        self.assertEqual(
            native.trusted_native_app_direct_task_create_once(
                task_request,
                adapter=native.TrustedNativeSyntheticTaskAdapter(
                    _native_task_receipt
                ),
            ),
            {"status": "blocked_request_or_packet_invalid", "receipt": None},
        )

    def test_direct_app_adapter_rejects_tampered_private_receipt_binding(
        self,
    ) -> None:
        task_request = _native_task_request(
            _native_request(
                _native_registry(role="E", code_policy="forbidden"),
                role="E",
                inspect_only=True,
            ),
            _native_worktree(),
        )
        receipt = _native_task_receipt(task_request)

        class MissingDirectResult:
            synthetic_only = True
            adapter_identity = app_direct.APP_NATIVE_DIRECT_ADAPTER_ID
            last_result = None

            def create_once(self, value: Mapping[str, object]) -> object:
                del value
                return receipt

        self.assertEqual(
            native.trusted_native_app_direct_task_create_once(
                task_request,
                adapter=MissingDirectResult(),
            ),
            {"status": "failed_lane_known", "receipt": None},
        )

        class TamperedDirectAdapter:
            synthetic_only = True
            adapter_identity = app_direct.APP_NATIVE_DIRECT_ADAPTER_ID
            last_result = {"platform_receipt": {"repository_id": 999}}

            def create_once(self, value: Mapping[str, object]) -> object:
                self.last_result["platform_receipt"].update(
                    {
                        "platform_receipt_sha256": receipt[
                            "platform_receipt_sha256"
                        ],
                        "accepted_at_utc": receipt["accepted_at_utc"],
                        "task_request_sha256": value["task_request_sha256"],
                        "claim_observation_sha256": value[
                            "claim_observation_sha256"
                        ],
                        "lane_packet_sha256": value["lane_packet_sha256"],
                        "pre_worktree_observation_sha256": value[
                            "worktree_observation_sha256"
                        ],
                        "task_identity_sha256": app_direct.task_identity_sha256(
                            str(receipt["task_id"])
                        ),
                        "terminal_status": "completed",
                        "terminal_readback_sha256": "1" * 64,
                        "typed_handoff_sha256": "2" * 64,
                        "post_worktree_observation_sha256": "3" * 64,
                        "automatic_retry_count": 0,
                        "replacement_task_count": 0,
                        "follow_up_message_count": 0,
                    }
                )
                return receipt

        self.assertEqual(
            native.trusted_native_app_direct_task_create_once(
                task_request,
                adapter=TamperedDirectAdapter(),
            ),
            {"status": "failed_lane_known", "receipt": None},
        )

    def test_release_rebaseline_kat_and_current_binding_selection(self) -> None:
        kat = _native_signed(
            {
                "schema_version": (
                    "trusted_owner_native_release_rebaseline_record.v1"
                ),
                "record_id": "r0.rebaseline.0123456789abcdef0123456789abcdef",
                "predecessor_record_sha256": "1" * 64,
                "from_rung": "R0",
                "to_rung": "R0",
                "predecessor_contract_sha256": "2" * 64,
                "contract_sha256": "3" * 64,
                "predecessor_skill_tree_sha256": "4" * 64,
                "skill_tree_sha256": "5" * 64,
                "predecessor_registry_sha256": "6" * 64,
                "registry_sha256": "7" * 64,
                "predecessor_validator_bundle_sha256": "8" * 64,
                "validator_bundle_sha256": "9" * 64,
                "observation_receipt_sha256s": [],
                "codex_e_review_ref": (
                    "https://github.com/Tahjali11/Mythic-Edge/issues/"
                    "813#issuecomment-1"
                ),
                "codex_e_review_sha256": "a" * 64,
                "owner_decision_ref": (
                    "https://github.com/Tahjali11/Mythic-Edge/issues/"
                    "813#issuecomment-2"
                ),
                "accepted_at_utc": "2026-08-04T12:00:00Z",
                "record_sha256": "",
            },
            "record_sha256",
        )
        preimage = native.trusted_native_canonical_bytes(
            {
                key: value
                for key, value in kat.items()
                if key != "record_sha256"
            }
        )
        artifact = native.trusted_native_canonical_bytes(kat)
        self.assertEqual(len(preimage), 1352)
        self.assertEqual(
            hashlib.sha256(preimage).hexdigest(),
            "50e60de91339280e4afe6b2e588c8d6be801e825405eae675703ff01451af32f",
        )
        self.assertEqual(len(artifact), 1435)
        self.assertEqual(
            hashlib.sha256(artifact).hexdigest(),
            "5ba515bcf5023803d8233672459940c504b7158337a8e6ede575b8a926e0e5ff",
        )
        self.assertEqual(
            native.validate_trusted_native_release_rebaseline_record(kat),
            [],
        )

        registry = _native_registry()
        r0 = _native_release_record(
            registry_sha256=registry["registry_sha256"],
        )
        historical = native.trusted_native_current_release_bindings([r0])
        self.assertIsNotNone(historical)
        assert historical is not None
        self.assertEqual(historical["contract_sha256"], NATIVE_SHA_A)

        rebaseline = _native_release_rebaseline(r0)
        chain = [r0, rebaseline]
        self.assertEqual(native.validate_trusted_native_release_chain(chain), [])
        self.assertEqual(native.trusted_native_current_rung(chain), "R0")
        current = native.trusted_native_current_release_bindings(chain)
        self.assertIsNotNone(current)
        assert current is not None
        self.assertEqual(current["record_sha256"], rebaseline["record_sha256"])
        self.assertEqual(current["contract_sha256"], "9" * 64)

        request = _native_request(
            registry,
            release_record=rebaseline,
        )
        self.assertEqual(
            native.validate_trusted_native_request(
                request,
                registry=registry,
                release_record=rebaseline,
            ),
            [],
        )

        r1 = _native_release_record("R1", predecessor=rebaseline)
        for field in (
            "contract_sha256",
            "skill_tree_sha256",
            "registry_sha256",
            "validator_bundle_sha256",
        ):
            r1[field] = rebaseline[field]
        r1["accepted_at_utc"] = "2026-07-23T12:00:02Z"
        r1["record_sha256"] = native.trusted_native_self_digest(
            r1,
            "record_sha256",
        )
        self.assertEqual(
            native.validate_trusted_native_release_chain([*chain, r1]),
            [],
        )

    def test_release_rebaseline_refusal_matrix_is_fail_closed(self) -> None:
        r0 = _native_release_record()
        valid = _native_release_rebaseline(r0)
        cases: dict[str, list[dict[str, object]]] = {}

        stale = copy.deepcopy(valid)
        stale["predecessor_record_sha256"] = "0" * 64
        stale["record_sha256"] = native.trusted_native_self_digest(
            stale,
            "record_sha256",
        )
        cases["stale"] = [r0, stale]

        wrong_binding = copy.deepcopy(valid)
        wrong_binding["predecessor_registry_sha256"] = "0" * 64
        wrong_binding["record_sha256"] = native.trusted_native_self_digest(
            wrong_binding,
            "record_sha256",
        )
        cases["wrong_binding"] = [r0, wrong_binding]

        unchanged = _native_release_rebaseline(
            r0,
            contract_sha256=str(r0["contract_sha256"]),
        )
        cases["unchanged_contract"] = [r0, unchanged]

        non_r0 = copy.deepcopy(valid)
        non_r0["to_rung"] = "R1"
        non_r0["record_sha256"] = native.trusted_native_self_digest(
            non_r0,
            "record_sha256",
        )
        cases["non_r0"] = [r0, non_r0]

        observed_r0 = copy.deepcopy(r0)
        observed_r0["observation_receipt_sha256s"] = ["1" * 64, "2" * 64]
        observed_r0["record_sha256"] = native.trusted_native_self_digest(
            observed_r0,
            "record_sha256",
        )
        cases["post_observation"] = [
            observed_r0,
            _native_release_rebaseline(observed_r0),
        ]

        duplicate = copy.deepcopy(valid)
        duplicate["predecessor_record_sha256"] = valid["record_sha256"]
        duplicate["record_id"] = "r0.rebaseline.duplicate"
        duplicate["accepted_at_utc"] = "2026-07-23T12:00:02Z"
        duplicate["record_sha256"] = native.trusted_native_self_digest(
            duplicate,
            "record_sha256",
        )
        cases["second_rebaseline"] = [r0, valid, duplicate]

        fork = _native_release_record("R1", predecessor=r0)
        cases["forked_ordinary_successor"] = [r0, fork, valid]

        for name, chain in cases.items():
            with self.subTest(name=name):
                self.assertTrue(native.validate_trusted_native_release_chain(chain))
                self.assertIsNone(
                    native.trusted_native_current_release_bindings(chain)
                )

    def test_app_server_observer_remains_inert_until_real_evidence(self) -> None:
        capability = native.unavailable_trusted_native_app_server_capability()
        self.assertEqual(
            capability.launcher_identity,
            "codex:native-task-create/v1",
        )
        self.assertIs(capability.available, False)
        self.assertIs(capability.compatible, False)
        self.assertIs(capability.fallback_forbidden, True)
        self.assertEqual(
            capability.source,
            "inert_app_server_r0_fake_transport_only",
        )

    def test_dedicated_app_server_integration_accepts_only_its_inert_adapter(
        self,
    ) -> None:
        registry = _native_registry()
        request = _native_request(registry)
        worktree = _native_worktree()
        task_request = _native_task_request(request, worktree)

        self.assertEqual(
            native.trusted_native_app_server_task_create_once(
                task_request,
                adapter=native.TrustedNativeSyntheticTaskAdapter(
                    _native_task_receipt
                ),
            ),
            {
                "status": "blocked_request_or_packet_invalid",
                "receipt": None,
            },
        )

        class InertAppServerReceiptAdapter:
            synthetic_only = True
            adapter_identity = app_server.APP_SERVER_ADAPTER_ID

            def __init__(self) -> None:
                self.used = False

            def create_once(
                self,
                value: Mapping[str, object],
            ) -> object:
                if self.used:
                    raise app_server.AppServerAdapterError(
                        "app_server_adapter_already_used"
                    )
                self.used = True
                return _native_task_receipt(dict(value))

        rejected_adapter = InertAppServerReceiptAdapter()
        self.assertEqual(
            native.trusted_native_app_server_task_create_once(
                task_request,
                adapter=rejected_adapter,
            ),
            {
                "status": "blocked_request_or_packet_invalid",
                "receipt": None,
            },
        )
        self.assertIs(rejected_adapter.used, False)

        inspect_registry = _native_registry(
            role="B",
            code_policy="forbidden",
        )
        inspect_request = _native_request(
            inspect_registry,
            role="B",
            inspect_only=True,
        )
        inspect_task_request = _native_task_request(inspect_request, worktree)
        adapter = InertAppServerReceiptAdapter()
        accepted = native.trusted_native_app_server_task_create_once(
            inspect_task_request,
            adapter=adapter,
        )
        self.assertEqual(
            native.validate_trusted_native_task_request(
                inspect_task_request,
                request=inspect_request,
            ),
            [],
        )
        self.assertEqual(
            native.validate_trusted_native_task_receipt(
                accepted["receipt"],
                request=inspect_task_request,
            ),
            [],
        )
        self.assertEqual(
            accepted["status"],
            "synthetic_app_server_receipt_accepted_non_live",
        )
        self.assertEqual(
            native.trusted_native_app_server_task_create_once(
                inspect_task_request,
                adapter=adapter,
            ),
            {"status": "failed_lane_known", "receipt": None},
        )

    def test_app_server_integration_preserves_known_and_unknown_projection(
        self,
    ) -> None:
        registry = _native_registry(
            role="B",
            code_policy="forbidden",
        )
        request = _native_request(
            registry,
            role="B",
            inspect_only=True,
        )
        task_request = _native_task_request(request, _native_worktree())

        class FailingAppServerAdapter:
            synthetic_only = True
            adapter_identity = app_server.APP_SERVER_ADAPTER_ID

            def __init__(self, lifecycle_case: str) -> None:
                self.lifecycle_case = lifecycle_case

            def create_once(self, value: Mapping[str, object]) -> object:
                del value
                raise app_server.AppServerAdapterError(self.lifecycle_case)

        for lifecycle_case, expected_status in (
            ("AS-POL-001", "failed_lane_known"),
            (
                "AS-TMO-UNK-001",
                "unknown_outcome_reconciliation_required",
            ),
        ):
            with self.subTest(lifecycle_case=lifecycle_case):
                self.assertEqual(
                    native.trusted_native_app_server_task_create_once(
                        task_request,
                        adapter=FailingAppServerAdapter(lifecycle_case),
                    ),
                    {
                        "status": expected_status,
                        "receipt": None,
                    },
                )

    def test_windows_preflight_accepts_only_exact_host_and_primitive(self) -> None:
        decision = _native_windows_preflight()
        self.assertEqual(
            decision["status"],
            "windows_preflight_satisfied_non_authorizing",
        )
        self.assertEqual(
            decision["host_classification"],
            "windows_hosted_execution",
        )
        self.assertIs(decision["task_capability_compatible"], True)
        self.assertIs(decision["preflight_satisfied"], True)
        self.assertIs(decision["authority_granted"], False)
        self.assertIs(decision["persistent_effect_performed"], False)
        self.assertIs(decision["fallback_attempted"], False)
        self.assertIsNone(decision["fallback_launcher"])

        for field, replacement in (
            ("available", False),
            ("compatible", False),
            ("request_binding", False),
            ("one_task_only", False),
            ("receipt_binding", False),
            ("timeout_enforced", False),
            ("unknown_outcome_fail_closed", False),
            ("automatic_retry_forbidden", False),
            ("fallback_forbidden", False),
        ):
            capability = native.TrustedNativeTaskCapabilityObservation(
                launcher_identity="codex:native-task-create/v1",
                available=True,
                compatible=True,
                request_binding=True,
                one_task_only=True,
                receipt_binding=True,
                timeout_enforced=True,
                unknown_outcome_fail_closed=True,
                automatic_retry_forbidden=True,
                fallback_forbidden=True,
                source="synthetic_test_double",
            )._replace(**{field: replacement})
            blocked = native.evaluate_trusted_native_execution_preflight(
                "dispatch",
                native.TrustedNativeRuntimeHostObservation(
                    "nt",
                    "win32",
                    True,
                    "synthetic_test_double",
                ),
                capability,
            )
            with self.subTest(field=field):
                self.assertEqual(
                    blocked["status"],
                    "blocked_request_or_packet_invalid",
                )
                self.assertIs(blocked["preflight_satisfied"], False)

        wrong_identity = native.TrustedNativeTaskCapabilityObservation(
            launcher_identity="codex:other/v1",
            available=True,
            compatible=True,
            request_binding=True,
            one_task_only=True,
            receipt_binding=True,
            timeout_enforced=True,
            unknown_outcome_fail_closed=True,
            automatic_retry_forbidden=True,
            fallback_forbidden=True,
            source="synthetic_test_double",
        )
        self.assertEqual(
            native.evaluate_trusted_native_execution_preflight(
                "dispatch",
                native.TrustedNativeRuntimeHostObservation(
                    "nt",
                    "win32",
                    True,
                    "synthetic_test_double",
                ),
                wrong_identity,
            )["status"],
            "blocked_request_or_packet_invalid",
        )

    def test_unsupported_host_is_priority_one_and_has_no_fallback(self) -> None:
        blocked_decisions = (
            _native_windows_preflight(os_name="posix", sys_platform="darwin"),
            _native_windows_preflight(os_name="nt", sys_platform="darwin"),
            _native_windows_preflight(os_name=None, sys_platform=None),
            _native_windows_preflight(host_observed=False),
        )
        for decision in blocked_decisions:
            with self.subTest(decision=decision):
                self.assertEqual(
                    decision["status"],
                    "blocked_request_or_packet_invalid",
                )
                self.assertEqual(
                    decision["terminal_outcome"],
                    "blocked_request_or_packet_invalid",
                )
                self.assertEqual(
                    decision["route"],
                    "codex_a_or_b_reconciliation",
                )
                self.assertIs(decision["persistent_effect_performed"], False)
                self.assertIs(decision["fallback_attempted"], False)
                self.assertIsNone(decision["fallback_launcher"])
                self.assertEqual(
                    native.select_trusted_native_terminal_outcome(
                        {"blocked_command_not_approved"},
                        execution_preflight=decision,
                    ),
                    "blocked_request_or_packet_invalid",
                )

        registry = _native_registry()
        request = _native_request(registry)
        request["platform"] = "win32"
        self.assertIn(
            "request:fields_or_order_invalid",
            native.validate_trusted_native_request(request),
        )

        invalid_operation = native.evaluate_trusted_native_execution_preflight(
            "private operation text",
            native.TrustedNativeRuntimeHostObservation(
                "nt",
                "win32",
                True,
                "synthetic_test_double",
            ),
            native.unavailable_trusted_native_task_capability(),
        )
        self.assertEqual(
            invalid_operation["operation"],
            "unsupported_operation",
        )
        self.assertNotIn("private operation text", repr(invalid_operation))

    def test_remote_mac_client_does_not_change_windows_execution_host(self) -> None:
        remote_client_platform = "macos"
        self.assertEqual(remote_client_platform, "macos")
        decision = _native_windows_preflight()
        self.assertEqual(
            decision["host_classification"],
            "windows_hosted_execution",
        )
        self.assertNotIn("remote_client_platform", decision)

    def test_offline_validation_is_platform_neutral_and_non_authorizing(self) -> None:
        decision = native.evaluate_trusted_native_execution_preflight(
            "offline_validation",
            native.TrustedNativeRuntimeHostObservation(
                "posix",
                "darwin",
                True,
                "synthetic_test_double",
            ),
            None,
        )
        self.assertEqual(
            decision["status"],
            "offline_validation_allowed_non_authorizing",
        )
        self.assertEqual(
            decision["host_classification"],
            "offline_host_not_required",
        )
        self.assertIs(decision["preflight_satisfied"], True)
        self.assertIs(decision["authority_granted"], False)
        self.assertIs(decision["persistent_effect_performed"], False)
        self.assertIs(decision["fallback_attempted"], False)

    def test_independent_windows_coordinators_contend_across_request_ids(
        self,
    ) -> None:
        registry = _native_registry()
        first_request = _native_request(registry)
        second_request = _native_request(registry)
        second_request["request_id"] = "request.second"
        second_request["request_sha256"] = native.trusted_native_self_digest(
            second_request,
            "request_sha256",
        )
        self.assertIs(_native_windows_preflight()["preflight_satisfied"], True)
        self.assertIs(_native_windows_preflight()["preflight_satisfied"], True)

        first = _native_claim_event(
            first_request,
            claim_id="claim.1",
            event_id="event.1",
            coordinator_sha256="b" * 64,
        )
        second = _native_claim_event(
            second_request,
            claim_id="claim.2",
            event_id="event.2",
            coordinator_sha256="c" * 64,
            device_sha256="d" * 64,
        )
        first_observation = _native_observation(first, comment_id=10)
        second_observation = _native_observation(
            second,
            comment_id=11,
            observed_at="2026-07-23T12:00:10Z",
        )
        snapshot = _native_snapshot([first_observation, second_observation])
        replay = native.replay_trusted_native_claims(
            [
                {"event": first, "observation": first_observation},
                {"event": second, "observation": second_observation},
            ],
            snapshot,
            registry=registry,
            now=datetime(2026, 7, 23, 12, 5, tzinfo=timezone.utc),
        )
        self.assertEqual(replay["status"], "claim_snapshot_replayed")
        self.assertEqual(replay["winning_claim_ids"], ["claim.1"])
        self.assertEqual(replay["active_claim_ids"], ["claim.1"])

    def test_task_result_and_terminal_evidence_cross_bind_one_lane(self) -> None:
        registry = _native_registry()
        request = _native_request(registry)
        lane = request["lanes"][0]
        assert isinstance(lane, dict)
        reservation = _native_claim_event(request)
        reservation_observation = _native_observation(reservation, comment_id=10)
        running = _native_claim_event(
            request,
            event_id="event.2",
            state="confirmed_running",
            predecessor=reservation_observation["claim_observation_sha256"],
            issued_at="2026-07-23T12:00:10Z",
        )
        running_observation = _native_observation(
            running,
            comment_id=11,
            observed_at="2026-07-23T12:00:10Z",
        )
        worktree = _native_worktree()
        task_request = _native_task_request(request, worktree)
        task_request["claim_observation_sha256"] = running_observation[
            "claim_observation_sha256"
        ]
        task_request["task_request_sha256"] = native.trusted_native_self_digest(
            task_request,
            "task_request_sha256",
        )
        task_receipt = _native_task_receipt(task_request)
        result = _native_result(request)
        result["claim_observation_sha256"] = running_observation[
            "claim_observation_sha256"
        ]
        result["worktree_observation_sha256"] = worktree[
            "worktree_observation_sha256"
        ]
        result["task_receipt_sha256"] = task_receipt["task_receipt_sha256"]
        result["task_id"] = task_receipt["task_id"]
        result["result_packet_sha256"] = native.trusted_native_self_digest(
            result,
            "result_packet_sha256",
        )

        self.assertEqual(
            native.validate_trusted_native_worktree_observation(
                worktree,
                lane=lane,
            ),
            [],
        )
        self.assertEqual(
            native.validate_trusted_native_task_request(
                task_request,
                request=request,
                claim_observation=running_observation,
                worktree=worktree,
            ),
            [],
        )
        self.assertEqual(
            native.validate_trusted_native_result(
                result,
                expected_request=request,
                claim_observation=running_observation,
                worktree=worktree,
                task_receipt=task_receipt,
                release_rung="R0",
            ),
            [],
        )

        released_at = "2026-07-23T12:00:20Z"
        release_binding = _native_release_binding(
            worktree,
            task_receipt,
            result,
            released_at=released_at,
        )
        released = _native_claim_event(
            request,
            event_id="event.3",
            state="released",
            predecessor=running_observation["claim_observation_sha256"],
            issued_at=released_at,
            terminal_binding=release_binding,
        )
        self.assertEqual(
            native.validate_trusted_native_terminal_evidence(
                released,
                expected_request=request,
                worktree=worktree,
                task_receipt=task_receipt,
                result=result,
            ),
            [],
        )
        unauthorized_result = copy.deepcopy(result)
        unauthorized_result["files_changed"] = [
            {
                "path": "src/unplanned.py",
                "change_kind": "added",
                "before_sha256": None,
                "after_sha256": NATIVE_SHA_A,
            }
        ]
        unauthorized_result["result_packet_sha256"] = (
            native.trusted_native_self_digest(
                unauthorized_result,
                "result_packet_sha256",
            )
        )
        unauthorized_binding = _native_release_binding(
            worktree,
            task_receipt,
            unauthorized_result,
            released_at=released_at,
        )
        unauthorized_release = _native_claim_event(
            request,
            event_id="event.unauthorized.release",
            state="released",
            predecessor=running_observation["claim_observation_sha256"],
            issued_at=released_at,
            terminal_binding=unauthorized_binding,
        )
        self.assertEqual(
            native.validate_trusted_native_terminal_evidence(
                unauthorized_release,
                expected_request=request,
                worktree=worktree,
                task_receipt=task_receipt,
                result=unauthorized_result,
            ),
            ["terminal_evidence:result_invalid"],
        )
        self.assertIn(
            "terminal_evidence:request_required",
            native.validate_trusted_native_terminal_evidence(
                released,
                worktree=worktree,
                task_receipt=task_receipt,
                result=result,
            ),
        )
        mixed = copy.deepcopy(result)
        mixed["task_id"] = "task.other"
        mixed["result_packet_sha256"] = native.trusted_native_self_digest(
            mixed,
            "result_packet_sha256",
        )
        self.assertIn(
            "result:task_id_mismatch",
            native.validate_trusted_native_result(
                mixed,
                task_receipt=task_receipt,
            ),
        )

    def test_completed_result_requires_passed_validation_and_authorized_outputs(
        self,
    ) -> None:
        request = _native_request(_native_registry())
        lane = request["lanes"][0]
        assert isinstance(lane, dict)
        lane["mutation_scope"] = ["docs"]
        lane["expected_artifact_paths"] = ["docs/result.md"]
        lane["lane_packet_sha256"] = native.trusted_native_self_digest(
            lane,
            "lane_packet_sha256",
        )
        request["request_sha256"] = native.trusted_native_self_digest(
            request,
            "request_sha256",
        )

        valid = _native_result(request)
        valid["files_changed"] = [
            {
                "path": "docs/result.md",
                "change_kind": "added",
                "before_sha256": None,
                "after_sha256": NATIVE_SHA_A,
            }
        ]
        valid["result_packet_sha256"] = native.trusted_native_self_digest(
            valid,
            "result_packet_sha256",
        )
        self.assertEqual(
            native.validate_trusted_native_result(
                valid,
                expected_request=request,
            ),
            [],
        )

        failed_validation = copy.deepcopy(valid)
        failed_validation["validation"][0].update(
            {
                "status": "failed",
                "exit_code": 1,
                "evidence_sha256": NATIVE_SHA_B,
            }
        )
        failed_validation["result_packet_sha256"] = (
            native.trusted_native_self_digest(
                failed_validation,
                "result_packet_sha256",
            )
        )
        self.assertIn(
            "result.validation:completed_requires_passed_validation",
            native.validate_trusted_native_result(
                failed_validation,
                expected_request=request,
            ),
        )

        out_of_scope = copy.deepcopy(valid)
        out_of_scope["files_changed"][0]["path"] = "src/result.py"
        out_of_scope["result_packet_sha256"] = native.trusted_native_self_digest(
            out_of_scope,
            "result_packet_sha256",
        )
        out_of_scope_errors = native.validate_trusted_native_result(
            out_of_scope,
            expected_request=request,
        )
        self.assertIn(
            "result.files_changed:mutation_scope_exceeded",
            out_of_scope_errors,
        )
        self.assertIn(
            "result.files_changed:expected_artifacts_mismatch",
            out_of_scope_errors,
        )

    def test_claim_authorship_transitions_and_project_contention(self) -> None:
        registry = _native_registry()
        request = _native_request(registry)
        reservation = _native_claim_event(request)
        observation = _native_observation(reservation, comment_id=10)
        self.assertEqual(
            native.validate_trusted_native_claim_event(
                reservation,
                request=request,
            ),
            [],
        )
        self.assertEqual(
            native.validate_trusted_native_claim_observation(
                observation,
                event=reservation,
                registry=registry,
            ),
            [],
        )

        unauthorized = _native_observation(
            reservation,
            comment_id=11,
            author_id=2002,
        )
        self.assertIn(
            "claim_observation:author_not_authorized",
            native.validate_trusted_native_claim_observation(
                unauthorized,
                event=reservation,
                registry=registry,
            ),
        )
        server_field = copy.deepcopy(reservation)
        server_field["server_comment_id"] = 10
        self.assertIn(
            "claim_event:fields_or_order_invalid",
            native.validate_trusted_native_claim_event(server_field),
        )

        running = _native_claim_event(
            request,
            event_id="event.2",
            state="confirmed_running",
            predecessor=observation["claim_observation_sha256"],
            issued_at="2026-07-23T12:00:10Z",
        )
        running_observation = _native_observation(
            running,
            comment_id=11,
            observed_at="2026-07-23T12:00:10Z",
        )
        self.assertEqual(
            native.validate_trusted_native_claim_transition(
                reservation,
                observation,
                running,
                running_observation,
                registry=registry,
            ),
            [],
        )

        second = _native_claim_event(
            request,
            claim_id="claim.2",
            event_id="event.3",
            device_sha256="c" * 64,
        )
        second_observation = _native_observation(
            second,
            comment_id=12,
            observed_at="2026-07-23T12:00:20Z",
        )
        snapshot = _native_snapshot([observation, second_observation])
        replay = native.replay_trusted_native_claims(
            [
                {"event": reservation, "observation": observation},
                {"event": second, "observation": second_observation},
            ],
            snapshot,
            registry=registry,
            now=datetime(2026, 7, 23, 12, 5, tzinfo=timezone.utc),
        )
        self.assertEqual(replay["status"], "claim_snapshot_replayed")
        self.assertEqual(replay["winning_claim_ids"], ["claim.1"])
        self.assertEqual(replay["active_claim_ids"], ["claim.1"])

    def test_project_replay_allows_two_disjoint_waves_and_rejects_duplicate_ids(
        self,
    ) -> None:
        registry = _native_registry(6)
        request_one = _native_request(registry, lane_count=3)
        request_two = _native_request(registry, lane_count=3)
        request_two["request_id"] = "request.second"
        request_two["lanes"] = [_native_lane(index) for index in range(4, 7)]
        request_two["request_sha256"] = native.trusted_native_self_digest(
            request_two,
            "request_sha256",
        )

        first = _native_claim_event(
            request_one,
            claim_id="claim.1",
            event_id="event.1",
            wave_ordinal=1,
        )
        second = _native_claim_event(
            request_two,
            claim_id="claim.2",
            event_id="event.2",
            wave_ordinal=2,
            issued_at="2026-07-23T12:00:10Z",
            device_sha256="c" * 64,
        )
        first_observation = _native_observation(first, comment_id=10)
        second_observation = _native_observation(
            second,
            comment_id=11,
            observed_at="2026-07-23T12:00:10Z",
        )
        records = [
            {"event": first, "observation": first_observation},
            {"event": second, "observation": second_observation},
        ]
        replay = native.replay_trusted_native_claims(
            records,
            _native_snapshot([first_observation, second_observation]),
            registry=registry,
            now=datetime(2026, 7, 23, 12, 5, tzinfo=timezone.utc),
        )
        self.assertEqual(replay["status"], "claim_snapshot_replayed")
        self.assertEqual(replay["winning_claim_ids"], ["claim.1", "claim.2"])
        self.assertEqual(replay["active_claim_ids"], ["claim.1", "claim.2"])

        duplicate_observation = copy.deepcopy(second_observation)
        duplicate_observation["server_comment_id"] = 10
        duplicate_observation[
            "claim_observation_sha256"
        ] = native.trusted_native_self_digest(
            duplicate_observation,
            "claim_observation_sha256",
        )
        duplicate_replay = native.replay_trusted_native_claims(
            [
                {"event": first, "observation": first_observation},
                {"event": second, "observation": duplicate_observation},
            ],
            _native_snapshot([first_observation, duplicate_observation]),
            registry=registry,
            now=datetime(2026, 7, 23, 12, 5, tzinfo=timezone.utc),
        )
        self.assertEqual(
            duplicate_replay["status"],
            "unknown_outcome_reconciliation_required",
        )
        self.assertIn(
            "duplicate_server_comment_id",
            duplicate_replay["errors"],
        )

    def test_claim_fork_and_incomplete_snapshot_remain_unknown(self) -> None:
        registry = _native_registry()
        request = _native_request(registry)
        reservation = _native_claim_event(request)
        observation = _native_observation(reservation, comment_id=10)
        running_a = _native_claim_event(
            request,
            event_id="event.2",
            state="confirmed_running",
            predecessor=observation["claim_observation_sha256"],
            issued_at="2026-07-23T12:00:10Z",
        )
        running_b = _native_claim_event(
            request,
            event_id="event.3",
            state="confirmed_running",
            predecessor=observation["claim_observation_sha256"],
            issued_at="2026-07-23T12:00:20Z",
        )
        observations = [
            observation,
            _native_observation(
                running_a,
                comment_id=11,
                observed_at="2026-07-23T12:00:10Z",
            ),
            _native_observation(
                running_b,
                comment_id=12,
                observed_at="2026-07-23T12:00:20Z",
            ),
        ]
        snapshot = _native_snapshot(observations)
        replay = native.replay_trusted_native_claims(
            [
                {"event": reservation, "observation": observations[0]},
                {"event": running_a, "observation": observations[1]},
                {"event": running_b, "observation": observations[2]},
            ],
            snapshot,
            registry=registry,
            now=datetime(2026, 7, 23, 12, 5, tzinfo=timezone.utc),
        )
        self.assertEqual(
            replay["status"],
            "unknown_outcome_reconciliation_required",
        )
        self.assertIn("claim_chain_fork_or_gap", replay["errors"])

        incomplete = copy.deepcopy(snapshot)
        incomplete["pagination_complete"] = False
        incomplete["snapshot_sha256"] = native.trusted_native_self_digest(
            incomplete,
            "snapshot_sha256",
        )
        self.assertEqual(
            native.replay_trusted_native_claims(
                [],
                incomplete,
                registry=registry,
                now=datetime(2026, 7, 23, 12, 5, tzinfo=timezone.utc),
            )["status"],
            "unknown_outcome_reconciliation_required",
        )

    def test_running_survives_expiry_and_reviewed_resolution_releases_capacity(
        self,
    ) -> None:
        registry = _native_registry()
        request = _native_request(registry)
        reservation = _native_claim_event(request)
        reservation_observation = _native_observation(reservation, comment_id=10)
        running = _native_claim_event(
            request,
            event_id="event.2",
            state="confirmed_running",
            predecessor=reservation_observation["claim_observation_sha256"],
            issued_at="2026-07-23T12:00:10Z",
        )
        running_observation = _native_observation(
            running,
            comment_id=11,
            observed_at="2026-07-23T12:00:10Z",
        )
        running_snapshot = _native_snapshot(
            [reservation_observation, running_observation]
        )
        running_replay = native.replay_trusted_native_claims(
            [
                {"event": reservation, "observation": reservation_observation},
                {"event": running, "observation": running_observation},
            ],
            running_snapshot,
            registry=registry,
            now=datetime(2026, 7, 23, 14, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(running_replay["active_claim_ids"], ["claim.1"])

        reconciliation = _native_claim_event(
            request,
            event_id="event.3",
            state="reconciliation_required",
            predecessor=reservation_observation["claim_observation_sha256"],
            issued_at="2026-07-23T12:00:10Z",
        )
        reconciliation_observation = _native_observation(
            reconciliation,
            comment_id=11,
            observed_at="2026-07-23T12:00:10Z",
        )
        trigger_snapshot = _native_snapshot(
            [reservation_observation, reconciliation_observation]
        )
        resolution = _native_resolution_event(
            "claim.1",
            reconciliation_observation["claim_observation_sha256"],
            trigger_snapshot["snapshot_sha256"],
        )
        resolution_observation = _native_observation(
            resolution,
            comment_id=12,
            observed_at="2026-07-23T12:00:20Z",
        )
        final_snapshot = _native_snapshot(
            [
                reservation_observation,
                reconciliation_observation,
                resolution_observation,
            ]
        )
        records = [
            {"event": reservation, "observation": reservation_observation},
            {
                "event": reconciliation,
                "observation": reconciliation_observation,
            },
            {"event": resolution, "observation": resolution_observation},
        ]
        unresolved = native.replay_trusted_native_claims(
            records,
            final_snapshot,
            registry=registry,
            now=datetime(2026, 7, 23, 12, 5, tzinfo=timezone.utc),
            resolution_snapshots={
                trigger_snapshot["snapshot_sha256"]: trigger_snapshot
            },
        )
        self.assertEqual(
            unresolved["status"],
            "unknown_outcome_reconciliation_required",
        )
        self.assertEqual(unresolved["active_claim_ids"], ["claim.1"])

        resolved = native.replay_trusted_native_claims(
            records,
            final_snapshot,
            registry=registry,
            now=datetime(2026, 7, 23, 12, 5, tzinfo=timezone.utc),
            resolution_snapshots={
                trigger_snapshot["snapshot_sha256"]: trigger_snapshot
            },
            accepted_resolution_review_receipts=[
                resolution["review_receipt_sha256"]
            ],
        )
        self.assertEqual(resolved["status"], "claim_snapshot_replayed")
        self.assertEqual(resolved["active_claim_ids"], [])

    def test_state_routes_terminal_selector_and_f_boundary_are_closed(self) -> None:
        windows_preflight = _native_windows_preflight()
        states = set(native.TRUSTED_NATIVE_SAFE_TRANSITIONS)
        for current, allowed in native.TRUSTED_NATIVE_SAFE_TRANSITIONS.items():
            for candidate in states:
                kwargs = (
                    {"execution_preflight": windows_preflight}
                    if current == "request_received" and candidate == "validated"
                    else {}
                )
                errors = native.validate_trusted_native_state_transition(
                    "safe",
                    current,
                    candidate,
                    **kwargs,
                )
                self.assertEqual(errors == [], candidate in allowed)
        self.assertIn(
            "state_transition:windows_preflight_required",
            native.validate_trusted_native_state_transition(
                "safe",
                "request_received",
                "validated",
            ),
        )

        self.assertEqual(
            native.route_trusted_native_automatic(
                "A",
                result_status="completed",
                handoff_status="complete",
                next_role="B",
            ),
            "fresh_b_task_eligible",
        )
        self.assertEqual(
            native.route_trusted_native_automatic(
                "B",
                result_status="completed",
                handoff_status="complete",
                next_role="C",
            ),
            "manual_implementation_required",
        )
        self.assertEqual(
            native.route_trusted_native_automatic(
                "D",
                result_status="completed",
                handoff_status="complete",
                next_role="E",
            ),
            "later_fresh_e_invocation_required",
        )
        self.assertEqual(
            native.route_trusted_native_automatic(
                "F",
                result_status="completed",
                handoff_status="no_next_role",
                next_role=None,
            ),
            "stop_before_g",
        )
        self.assertEqual(
            native.route_trusted_native_automatic(
                "A",
                result_status="unknown",
                handoff_status="complete",
                next_role="B",
            ),
            "reconcile_and_stop",
        )
        self.assertEqual(
            native.route_trusted_native_automatic(
                "A",
                result_status="failed",
                handoff_status="complete",
                next_role="B",
            ),
            "reconcile_and_stop",
        )

        for outcome in native.TRUSTED_NATIVE_TERMINAL_OUTCOMES[:-1]:
            self.assertEqual(
                native.select_trusted_native_terminal_outcome({outcome}),
                outcome,
            )
        self.assertEqual(
            native.select_trusted_native_terminal_outcome(set()),
            "accepted_wave_complete",
        )
        self.assertEqual(
            native.select_trusted_native_terminal_outcome(
                set(native.TRUSTED_NATIVE_TERMINAL_OUTCOMES)
            ),
            native.TRUSTED_NATIVE_TERMINAL_OUTCOMES[0],
        )
        self.assertEqual(
            len(native.TRUSTED_NATIVE_TERMINAL_OUTCOMES),
            len(set(native.TRUSTED_NATIVE_TERMINAL_OUTCOMES)),
        )

        boundary = {
            field: True
            for field in (
                "independent_review_accepted",
                "exact_head_files_scope",
                "validation_passed",
                "repository_authority_refreshed",
                "wip_authority_refreshed",
                "base_branch_authorized",
                "publication_authority_exact",
                "reviewed_files_only",
                "secret_scan_passed",
                "protected_surface_check_passed",
                "repository_checks_passed",
                "draft_pr_only",
            )
        }
        self.assertEqual(native.validate_trusted_native_f_boundary(boundary), [])
        boundary["draft_pr_only"] = False
        self.assertIn(
            "f_boundary:draft_pr_only_required",
            native.validate_trusted_native_f_boundary(boundary),
        )

    def test_external_isolation_classification_and_release_ladder(self) -> None:
        self.assertEqual(
            native.classify_trusted_native_profile(
                [{"external_isolation_triggers": []}]
            ),
            "trusted_owner_native_eligible",
        )
        self.assertEqual(
            native.classify_trusted_native_profile(
                [{"external_isolation_triggers": ["untrusted_contributor"]}]
            ),
            "blocked_external_isolation_required",
        )
        self.assertEqual(
            native.classify_trusted_native_profile(
                [
                    {"external_isolation_triggers": []},
                    {
                        "external_isolation_triggers": [
                            "malicious_content_containment"
                        ]
                    },
                ]
            ),
            "blocked_mixed_profile_wave",
        )

        bootstrap = _native_release_record()
        r1 = _native_release_record("R1", predecessor=bootstrap)
        self.assertEqual(
            native.validate_trusted_native_release_chain([bootstrap, r1]),
            [],
        )
        self.assertEqual(native.trusted_native_current_rung([bootstrap, r1]), "R1")
        skip = _native_release_record("R2", predecessor=bootstrap)
        self.assertIn(
            "release_chain:rung_skip_or_duplicate",
            native.validate_trusted_native_release_chain([bootstrap, skip]),
        )
        stale = copy.deepcopy(r1)
        stale["registry_sha256"] = "0" * 64
        stale["record_sha256"] = native.trusted_native_self_digest(
            stale,
            "record_sha256",
        )
        self.assertIn(
            "release_chain:registry_sha256_drift",
            native.validate_trusted_native_release_chain([bootstrap, stale]),
        )

    def test_release_rungs_block_three_lane_and_f_canaries_until_available(
        self,
    ) -> None:
        common = {
            "operation_id": "inspect",
            "claim_creation": True,
            "task_creation": True,
            "f_publication": False,
            "execution_preflight": _native_windows_preflight(),
        }
        self.assertIn(
            "release_ceiling:r2_single_lane",
            native.validate_trusted_native_release_ceiling(
                "R2",
                mode="safe",
                role="B",
                lane_count=3,
                wave_count=1,
                **common,
            ),
        )
        self.assertEqual(
            native.validate_trusted_native_release_ceiling(
                "R3",
                mode="safe",
                role="B",
                lane_count=3,
                wave_count=1,
                **common,
            ),
            [],
        )
        self.assertIn(
            "release_ceiling:f_publication_not_available",
            native.validate_trusted_native_release_ceiling(
                "R3",
                mode="safe",
                role="F",
                lane_count=1,
                wave_count=1,
                operation_id="draft_pr",
                claim_creation=True,
                task_creation=True,
                f_publication=True,
            ),
        )
        self.assertEqual(
            native.validate_trusted_native_release_ceiling(
                "R4",
                mode="safe",
                role="F",
                lane_count=1,
                wave_count=1,
                operation_id="draft_pr",
                claim_creation=True,
                task_creation=True,
                f_publication=True,
                execution_preflight=_native_windows_preflight(),
            ),
            [],
        )
        self.assertIn(
            "release_ceiling:windows_preflight_required",
            native.validate_trusted_native_release_ceiling(
                "R1",
                mode="safe",
                role="B",
                lane_count=1,
                wave_count=1,
                operation_id="inspect",
                claim_creation=False,
                task_creation=False,
                f_publication=False,
                execution_preflight=_native_windows_preflight(
                    os_name="posix",
                    sys_platform="darwin",
                ),
            ),
        )
        self.assertIn(
            "release_ceiling:r0_offline_only",
            native.validate_trusted_native_release_ceiling(
                "R0",
                mode="safe",
                role="B",
                lane_count=1,
                wave_count=1,
                **common,
            ),
        )

    def test_result_and_handoff_preserve_false_authority(self) -> None:
        registry = _native_registry()
        request = _native_request(registry)
        result = _native_result(request)
        self.assertEqual(
            native.validate_trusted_native_result(
                result,
                expected_request=request,
                release_rung="R0",
            ),
            [],
        )
        live = copy.deepcopy(result)
        live["authority_flags"]["live_ready"] = True
        live["result_packet_sha256"] = native.trusted_native_self_digest(
            live,
            "result_packet_sha256",
        )
        self.assertIn(
            "result.authority_flags:live_ready_forbidden",
            native.validate_trusted_native_result(live, release_rung="R8"),
        )
        premature = copy.deepcopy(result)
        premature["authority_flags"]["trusted_owner_native_profile_ready"] = True
        premature["result_packet_sha256"] = native.trusted_native_self_digest(
            premature,
            "result_packet_sha256",
        )
        self.assertIn(
            "result.authority_flags:profile_ready_requires_r8",
            native.validate_trusted_native_result(premature, release_rung="R7"),
        )
        unknown = copy.deepcopy(result)
        unknown["result"] = "unknown"
        unknown["authority_flags"]["implementation_authorized"] = True
        unknown["result_packet_sha256"] = native.trusted_native_self_digest(
            unknown,
            "result_packet_sha256",
        )
        self.assertIn(
            "result.authority_flags:unknown_result_authority_forbidden",
            native.validate_trusted_native_result(unknown, release_rung="R0"),
        )

    def test_migration_inventory_and_reparse_refusal_are_deterministic(self) -> None:
        self.assertEqual(native.validate_trusted_native_migration_constants(), [])
        self.assertEqual(len(native.TRUSTED_NATIVE_MIGRATION_MANAGED_ROWS), 34)
        self.assertEqual(len(native.TRUSTED_NATIVE_MIGRATION_GENERATED_ROWS), 16)
        self.assertTrue(
            all(
                "__pycache__" not in row[0] and not row[0].endswith(".pyc")
                for row in native.TRUSTED_NATIVE_MIGRATION_MANAGED_ROWS
            )
        )
        self.assertTrue(
            all(
                "__pycache__" in row[0] or row[0].endswith(".pyc")
                for row in native.TRUSTED_NATIVE_MIGRATION_GENERATED_ROWS
            )
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (
                mock.patch.object(native, "_native_is_reparse_stat", return_value=True),
                mock.patch.object(Path, "read_bytes") as read_bytes,
            ):
                manifest, errors = native.build_trusted_native_managed_manifest(root)
            self.assertIsNone(manifest)
            self.assertIn("managed_tree:root_unsafe", errors)
            read_bytes.assert_not_called()


if __name__ == "__main__":
    unittest.main()
