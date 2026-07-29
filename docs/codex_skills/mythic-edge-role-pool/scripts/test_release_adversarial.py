from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from check_pool_plan import (
    DEFAULT_REPOSITORY_OWNER,
    DEFAULT_REPOSITORY_PREFIX,
    DEFAULT_REPOSITORY_READ_SCOPE,
    DEFAULT_ROOT_REPOSITORY,
    OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
    POOLED_ROLES,
    ROLE_ACTION_SETS,
    _canonical_request_repository,
    _request_authorized_repositories,
    _request_repository_read_grants,
    _request_repository_authorities,
    canonical_document_digest,
    choose_claim_winner,
    normalize_invocation,
    parse_compact_invocation,
    select_lanes,
    validate_plan as validate_plan_production,
    validate_plan_against_observations as validate_plan_against_observations_production,
    validate_prelaunch_against_preclaim as validate_prelaunch_against_preclaim_production,
    validate_result as validate_result_production,
    validate_result_against_plan as validate_result_against_plan_production,
    validate_result_against_outcome_observation as validate_result_against_outcome_observation_production,
)
from pool_test_fixtures import (
    CLAIM_ID,
    EXPIRES,
    LANE_ID,
    NOW,
    OBSERVED,
    REPOSITORY,
    active_inspect_plan,
    completed_result,
    discovery_observation,
    discovery_for_plan,
    inspect_plan,
    launcher_receipt_sidecars_for_document,
    outcome_observation,
    preclaim_plan,
    prelaunch_plan,
    reservation,
    result_fallback,
    runtime_preflight,
    worktree_observation,
    winning_claim,
)


def validate_plan(plan: object, now: object = None) -> list[str]:
    return validate_plan_production(
        plan,
        now,
        validation_mode=OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
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


def validate_result(result: object, now: object = None) -> list[str]:
    return validate_result_production(
        result,
        now,
        validation_mode=OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
        launcher_receipts=(
            launcher_receipt_sidecars_for_document(result)
            if isinstance(result, dict)
            else None
        ),
    )


def validate_result_against_plan(
    plan: object, result: object, now: object = None
) -> list[str]:
    return validate_result_against_plan_production(
        plan,
        result,
        now,
        validation_mode=OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
        launcher_receipts=(
            launcher_receipt_sidecars_for_document(result)
            if isinstance(result, dict)
            else None
        ),
    )


def validate_result_against_outcome_observation(
    plan: object, result: object, outcome: object, now: object = None
) -> list[str]:
    return validate_result_against_outcome_observation_production(
        plan,
        result,
        outcome,
        now,
        validation_mode=OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
        launcher_receipts=(
            launcher_receipt_sidecars_for_document(result)
            if isinstance(result, dict)
            else None
        ),
    )


SCRIPT = Path(__file__).resolve().parent / "check_pool_plan.py"


def set_request(plan: dict[str, object], text: str, mode: str | None = None) -> None:
    action = plan["action"]
    action["request_text"] = text
    action["request_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if mode is not None:
        action["mode"] = mode


def assert_fragment(test: unittest.TestCase, errors: list[str], fragment: str) -> None:
    test.assertTrue(any(fragment in error for error in errors), errors)


def two_lane_preclaim_and_prelaunch() -> tuple[dict[str, object], dict[str, object]]:
    preclaim = preclaim_plan()
    first = preclaim["proposed_wave"]["lanes"][0]
    second = copy.deepcopy(first)
    second_id = f"{REPOSITORY}#102"
    second["lane_id"] = second_id
    second["issue"] = 102
    second["worktree"].update(
        {
            "path": "C:\\ME-B-102",
            "resolved_path": "C:\\ME-B-102",
            "git_toplevel": "C:\\ME-B-102",
            "git_common_dir": "C:\\ME-B-102\\.git",
            "branch": "codex/issue-102",
        }
    )
    contract = "docs/contracts/issue-102.md"
    second["scope"]["expected_files"] = [contract]
    second["scope"]["write_paths"] = [contract]
    second["scope"]["contract_surfaces"] = [contract]
    second["role_evidence"]["issue_ref"] = "github:issue/102"
    second["role_evidence"]["contract_path"] = contract
    second["evidence_sources"][0]["ref"] = "github:issue/102"
    preclaim["inventory"]["repositories"][0]["allowed_read_only_references"].append(
        "github:issue/102"
    )
    second["wip_assignment"] = {
        "kind": "exception",
        "exception_name": "explicit_user_override",
        "repository": REPOSITORY,
        "active_issue_or_lane": LANE_ID,
        "blocked_active_issue_or_pr": "github:issue/101",
        "reason": "bounded two-lane fixture",
        "allowed_scope": second_id,
        "expiration_condition": "when issue 102 completes",
        "expires_at": EXPIRES,
        "authorized_by": "user:current-task/wip-exception",
        "recorded_in": "artifact:wip-exception/102",
    }
    request = (
        preclaim["action"]["request_text"]
        + f"; authorize WIP exception lane={second_id} owner={LANE_ID}"
    )
    set_request(preclaim, request, "dispatch")
    preclaim["proposed_wave"]["lanes"].append(second)
    preclaim["runtime_preflight"] = runtime_preflight(
        lanes=preclaim["proposed_wave"]["lanes"]
    )
    candidate = copy.deepcopy(preclaim["candidate_inventory"][0])
    candidate["lane_id"] = second_id
    preclaim["candidate_inventory"].append(candidate)
    preclaim["compatibility"] = [
        {
            "left": LANE_ID,
            "right": second_id,
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
    ]
    prelaunch = copy.deepcopy(preclaim)
    prelaunch["phase"] = "prelaunch"
    wave = prelaunch["proposed_wave"]
    wave["state"] = "reserved"
    claim = winning_claim(wave["wave_id"], canonical_document_digest(preclaim))
    claim["lane_ids"] = [LANE_ID, second_id]
    claim["competing_claims"][0]["lane_ids"] = [LANE_ID, second_id]
    wave["claim"] = claim
    for index, lane in enumerate(wave["lanes"]):
        lane["state"] = "reserved"
        lane_reservation = reservation(wave["wave_id"])
        if index == 1:
            lane_reservation["idempotency_key"] = f"reserve:{second_id}:{CLAIM_ID}"
            lane_reservation["receipt_ref"] = "github:reservation-comment/102"
            lane_reservation["server_comment_id"] = 10103
        lane["reservation"] = lane_reservation
    return preclaim, prelaunch


class InvocationAndAuthorityAdversarialTests(unittest.TestCase):
    def test_only_unambiguous_leading_imperatives_dispatch(self) -> None:
        dispatch = [
            "Dispatch Codex B for issue 101",
            "Please run Codex E for issue 101",
            "Check G readiness for issue 101",
        ]
        inspect = [
            "Do not dispatch; inspect only",
            "Never run Codex B",
            "Show me how dispatch works",
            "Would you dispatch Codex B?",
            "'Dispatch Codex B' is only an example",
            "Dispatch Codex B, then inspect the options",
        ]
        for request in dispatch:
            with self.subTest(request=request):
                self.assertEqual(normalize_invocation(request), "dispatch")
        for request in inspect:
            with self.subTest(request=request):
                self.assertEqual(normalize_invocation(request), "inspect")

    def test_named_dispatch_mode_is_leading_explicit_and_fail_closed(self) -> None:
        dispatch = [
            "Mythic-Edge-Role-Pool: Dispatch Codex B for issue 101",
            "$mythic-edge-role-pool: Dispatch Codex E for issue 101",
            "Mythic Edge Role Pool: Dispatch Codex G for PR 12",
            "Mythic-Edge-Role-Pool: Dispatch",
        ]
        inspect = [
            "Mythic-Edge-Role-Pool: Inspect Codex B candidates",
            "Use Mythic-Edge-Role-Pool: Dispatch Codex B for issue 101",
            "'Mythic-Edge-Role-Pool: Dispatch Codex B' is an example",
            "Mythic-Edge-Role-Pool: Dispatch is only an example",
            "Mythic-Edge-Role-Pool: Dispatch Codex B?",
            "Mythic-Edge-Role-Pool: Dispatch Codex B only if it is ready",
            "Mythic-Edge-Role-Pool: Dispatch Codex B, then inspect the options",
            "Mythic-Edge-Role-Pool: Dispatch no lanes",
        ]
        for request in dispatch:
            with self.subTest(request=request):
                self.assertEqual(normalize_invocation(request), "dispatch")
        for request in inspect:
            with self.subTest(request=request):
                self.assertEqual(normalize_invocation(request), "inspect")

        plan = preclaim_plan("Codex B")
        set_request(
            plan,
            plan["action"]["request_text"].replace(
                "Dispatch Codex B", "Mythic-Edge-Role-Pool: Dispatch Codex B", 1
            ),
            "dispatch",
        )
        self.assertEqual(validate_plan(plan, NOW), [])

        incomplete = preclaim_plan("Codex B")
        set_request(incomplete, "Mythic-Edge-Role-Pool: Dispatch", "dispatch")
        errors = validate_plan(incomplete, NOW)
        assert_fragment(self, errors, "exactly one unambiguous pooled target role")
        assert_fragment(self, errors, "repositories explicitly authorized in request_text")

    def test_personal_default_owner_canonicalizes_only_repository_clauses(self) -> None:
        self.assertEqual(DEFAULT_REPOSITORY_OWNER, "tahjali11")
        request = (
            "Mythic-Edge-Role-Pool: Inspect Codex B candidates; "
            "authorize repository=mythic-edge-security; "
            "authorize repository=another-owner/research; "
            "authorize private read repository=mythic-edge-security"
        )
        self.assertEqual(
            _request_authorized_repositories(request),
            {"tahjali11/mythic-edge-security", "another-owner/research"},
        )
        self.assertEqual(
            _request_repository_authorities(
                request, "authorize private read repository"
            ),
            {"tahjali11/mythic-edge-security"},
        )

        invalid = (
            'authorize repository="mythic-edge-security"; '
            "do not authorize repository=mythic-edge-security; "
            "authorize repository=mythic edge security; "
            "authorize repository=mythic-edge-security.git; "
            "authorize repository=https://github.com/tahjali11/mythic-edge-security"
        )
        self.assertEqual(_request_authorized_repositories(invalid), set())

    def test_default_owner_shorthand_grants_named_private_repository_read(self) -> None:
        plan = preclaim_plan("Codex B")
        request = plan["action"]["request_text"]
        request = request.replace(
            f"authorize repository={REPOSITORY}",
            "authorize repository=mythic-edge",
        )
        set_request(plan, request, "dispatch")
        self.assertEqual(validate_plan(plan, NOW), [])

    def test_compact_invocation_parses_mode_role_and_exact_repository_scope(self) -> None:
        request = (
            "Mythic Edge Role Pool: Inspect: B security; "
            "fable-engine; corpus"
        )
        self.assertEqual(normalize_invocation(request), "inspect")
        self.assertEqual(
            parse_compact_invocation(request),
            (
                "inspect",
                "Codex B",
                (
                    "tahjali11/mythic-edge-security",
                    "tahjali11/mythic-edge-fable-engine",
                    "tahjali11/mythic-edge-corpus",
                ),
            ),
        )
        self.assertEqual(
            _request_authorized_repositories(request),
            {
                "tahjali11/mythic-edge-security",
                "tahjali11/mythic-edge-fable-engine",
                "tahjali11/mythic-edge-corpus",
            },
        )

    def test_personal_repo_alias_adds_prefix_once_and_explicit_owner_bypasses_it(self) -> None:
        self.assertEqual(DEFAULT_REPOSITORY_PREFIX, "mythic-edge-")
        self.assertEqual(DEFAULT_ROOT_REPOSITORY, "mythic-edge")
        expected = {
            "security": "tahjali11/mythic-edge-security",
            "fable-engine": "tahjali11/mythic-edge-fable-engine",
            "corpus": "tahjali11/mythic-edge-corpus",
            "mythic-edge": "tahjali11/mythic-edge",
            "mythic-edge-security": "tahjali11/mythic-edge-security",
            "tahjali11/fable-engine": "tahjali11/fable-engine",
            "another-owner/fable-engine": "another-owner/fable-engine",
        }
        for value, canonical in expected.items():
            with self.subTest(value=value):
                self.assertEqual(_canonical_request_repository(value), canonical)
        self.assertIsNone(_canonical_request_repository("auto"))
        self.assertEqual(
            _request_repository_authorities(
                "authorize private read repository=fable-engine",
                "authorize private read repository",
            ),
            {"tahjali11/mythic-edge-fable-engine"},
        )

    def test_compact_named_private_repo_grants_read_without_extra_clause(self) -> None:
        plan = preclaim_plan("Codex B")
        request = "Mythic Edge Role Pool: Dispatch: B mythic-edge"
        set_request(plan, request, "dispatch")
        self.assertEqual(validate_plan(plan, NOW), [])

        redundant_legacy_clause = preclaim_plan("Codex B")
        set_request(
            redundant_legacy_clause,
            "Mythic Edge Role Pool: Dispatch: B mythic-edge; "
            "authorize private read repository=mythic-edge",
            "dispatch",
        )
        self.assertEqual(validate_plan(redundant_legacy_clause, NOW), [])

        scope_expanding_legacy_clause = preclaim_plan("Codex B")
        set_request(
            scope_expanding_legacy_clause,
            "Mythic Edge Role Pool: Dispatch: B mythic-edge; "
            "authorize private read repository=other-owner/unlisted",
            "dispatch",
        )
        assert_fragment(
            self,
            validate_plan(scope_expanding_legacy_clause, NOW),
            "legacy private-read clause is redundant and cannot add repository scope",
        )
        self.assertEqual(
            _request_repository_read_grants(
                scope_expanding_legacy_clause["action"]["request_text"]
            ),
            {REPOSITORY: "authorized_full"},
        )

    def test_public_and_private_named_repositories_use_the_same_read_grant(self) -> None:
        self.assertEqual(DEFAULT_REPOSITORY_READ_SCOPE, "authorized_full")
        private_plan = preclaim_plan("Codex B")
        self.assertEqual(validate_plan(private_plan, NOW), [])

        public_plan = preclaim_plan("Codex B")
        repository = public_plan["inventory"]["repositories"][0]
        repository["visibility"] = "public"
        repository["private_content_authorized"] = False
        self.assertEqual(validate_plan(public_plan, NOW), [])

    def test_named_repository_read_policy_is_modular_and_fails_closed(self) -> None:
        request = "Mythic Edge Role Pool: Inspect: B security; fable-engine"
        expected_repositories = {
            "tahjali11/mythic-edge-security",
            "tahjali11/mythic-edge-fable-engine",
        }
        self.assertEqual(
            _request_repository_read_grants(request),
            {repository: "authorized_full" for repository in expected_repositories},
        )
        self.assertEqual(
            _request_repository_read_grants(request, default_scope="metadata_only"),
            {repository: "metadata_only" for repository in expected_repositories},
        )
        self.assertEqual(
            _request_repository_read_grants(request, default_scope="unsupported"),
            {},
        )

    def test_full_read_authority_ref_is_bound_to_exact_named_repository(self) -> None:
        plan = preclaim_plan("Codex B")
        repository = plan["inventory"]["repositories"][0]
        repository["read_authority_ref"] = "user:current-task/repository/other/repo"
        assert_fragment(
            self,
            validate_plan(plan, NOW),
            "must be derived from the exact named repository",
        )

    def test_compact_repository_count_never_backfills_or_accepts_wildcards(self) -> None:
        one = parse_compact_invocation(
            "$mythic-edge-role-pool: Dispatch: E mythic-edge-security"
        )
        two = parse_compact_invocation(
            "Mythic-Edge-Role-Pool: Dispatch: E mythic-edge-security; mythic-edge-corpus"
        )
        self.assertEqual(one[2], ("tahjali11/mythic-edge-security",))
        self.assertEqual(
            two[2],
            (
                "tahjali11/mythic-edge-security",
                "tahjali11/mythic-edge-corpus",
            ),
        )
        self.assertEqual(
            parse_compact_invocation("Mythic Edge Role Pool: Inspect: B"),
            ("inspect", "Codex B", ()),
        )
        self.assertIsNone(
            parse_compact_invocation("Mythic Edge Role Pool: Inspect: B auto")
        )
        self.assertIsNone(
            parse_compact_invocation(
                "Mythic Edge Role Pool: Inspect: B one; two; three; four"
            )
        )

        incomplete = inspect_plan("Codex B")
        set_request(incomplete, "Mythic Edge Role Pool: Inspect: B", "inspect")
        assert_fragment(
            self,
            validate_plan(incomplete, NOW),
            "repositories explicitly authorized in request_text",
        )

    def test_compact_c_is_recognized_but_remains_non_poolable(self) -> None:
        parsed = parse_compact_invocation(
            "Mythic Edge Role Pool: Dispatch: C mythic-edge"
        )
        self.assertEqual(parsed[1], "Codex C")
        self.assertNotIn("Codex C", POOLED_ROLES)

    def test_plan_mode_and_request_digest_are_bound_to_exact_text(self) -> None:
        plan = preclaim_plan()
        set_request(plan, "Do not dispatch; inspect only")
        errors = validate_plan(plan, NOW)
        assert_fragment(self, errors, "normalization inspect")
        plan = preclaim_plan()
        plan["action"]["request_sha256"] = "0" * 64
        assert_fragment(self, validate_plan(plan, NOW), "bind the exact request text")

    def test_every_role_rejects_one_extra_allowed_but_unauthorized_action(self) -> None:
        extras = {
            "Codex A": "git_push",
            "Codex B": "issue_write",
            "Codex D": "issue_write",
            "Codex E": "issue_write",
            "Codex F": "issue_write",
            "Codex G": "issue_write",
        }
        for role, extra in extras.items():
            plan = preclaim_plan(role)
            self.assertNotIn(extra, ROLE_ACTION_SETS[role])
            plan["action"]["authorized_actions"].append(extra)
            with self.subTest(role=role):
                assert_fragment(self, validate_plan(plan, NOW), "must exactly equal")

    def test_role_file_boundaries_are_exact(self) -> None:
        mutators = {
            "Codex A": lambda lane: lane["scope"]["write_paths"].append("skill/file.py"),
            "Codex B": lambda lane: lane["scope"]["write_paths"].append("skill/file.py"),
            "Codex D": lambda lane: lane["scope"]["write_paths"].clear(),
            "Codex E": lambda lane: lane["scope"]["write_paths"].append("skill/file.py"),
            "Codex F": lambda lane: lane["scope"]["write_paths"].append("skill/file.py"),
            "Codex G": lambda lane: lane["scope"]["write_paths"].append("skill/file.py"),
        }
        for role, mutate in mutators.items():
            plan = preclaim_plan(role)
            mutate(plan["proposed_wave"]["lanes"][0])
            with self.subTest(role=role):
                assert_fragment(self, validate_plan(plan, NOW), "scope")

    def test_default_model_and_effort_are_frozen_and_override_is_typed(self) -> None:
        plan = preclaim_plan()
        plan["runtime_preflight"] = runtime_preflight(
            preferred_model="attacker-model"
        )
        preflight = plan["runtime_preflight"]
        preflight["effective_model"] = "attacker-model"
        assert_fragment(self, validate_plan(plan, NOW), "explicit current override")

        preflight["override_authority_ref"] = "user:current-task/runtime-override/101"
        preflight["override_request_sha256"] = plan["action"]["request_sha256"]
        preflight["override_granted_at"] = OBSERVED
        preflight["override_model"] = "attacker-model"
        preflight["override_reasoning_effort"] = "max"
        preflight["override_reason"] = "explicit test-only model override"
        set_request(
            plan,
            plan["action"]["request_text"]
            + "; authorize runtime override model=attacker-model reasoning_effort=max",
            "dispatch",
        )
        preflight["override_request_sha256"] = plan["action"]["request_sha256"]
        self.assertEqual(validate_plan(plan, NOW), [])

        preflight["override_request_sha256"] = "0" * 64
        assert_fragment(self, validate_plan(plan, NOW), "current invocation request")

    def test_main_target_needs_separate_current_approval(self) -> None:
        plan = preclaim_plan("Codex F")
        lane = plan["proposed_wave"]["lanes"][0]
        lane["target_branch"] = "main"
        lane["role_evidence"]["approved_base"] = "main"
        assert_fragment(self, validate_plan(plan, NOW), "main_target_approval_ref")
        lane["role_evidence"]["main_target_approval_ref"] = lane["role_evidence"][
            "publication_approval_ref"
        ]
        assert_fragment(self, validate_plan(plan, NOW), "distinct approval")
        lane["role_evidence"]["main_target_approval_ref"] = (
            "user:current-task/explicit-main-target-approval"
        )
        set_request(
            plan,
            plan["action"]["request_text"] + "; authorize draft PR target=main",
            "dispatch",
        )
        plan["runtime_preflight"] = runtime_preflight(
            lanes=plan["proposed_wave"]["lanes"]
        )
        self.assertEqual(validate_plan(plan, NOW), [])


class StateClaimAndObservationAdversarialTests(unittest.TestCase):
    def test_wave_lane_and_runtime_states_must_be_coherent(self) -> None:
        plan = active_inspect_plan()
        plan["active_waves"][0]["state"] = "reserved"
        assert_fragment(self, validate_plan(plan, NOW), "inconsistent with lane states")
        plan = active_inspect_plan()
        plan["active_waves"][0]["lanes"][0]["runtime"]["state"] = "running"
        assert_fragment(
            self,
            validate_plan(plan, NOW),
            "inconsistent with lane state result_received",
        )

    def test_active_slot_forces_every_new_lane_to_use_an_exception(self) -> None:
        plan = preclaim_plan()
        active = active_inspect_plan()["active_waves"][0]
        plan["active_waves"] = [active]
        repo = plan["inventory"]["repositories"][0]
        repo["active_slot_lane_id"] = LANE_ID
        repo["active_lane_ids"] = [LANE_ID]
        lane = plan["proposed_wave"]["lanes"][0]
        lane["lane_id"] = f"{REPOSITORY}#102"
        lane["issue"] = 102
        lane["worktree"].update(
            {
                "path": "C:\\ME-B-102",
                "resolved_path": "C:\\ME-B-102",
                "git_toplevel": "C:\\ME-B-102",
                "git_common_dir": "C:\\ME-B-102\\.git",
                "branch": "codex/issue-102",
            }
        )
        contract = "docs/contracts/issue-102.md"
        lane["scope"]["expected_files"] = [contract]
        lane["scope"]["write_paths"] = [contract]
        lane["scope"]["contract_surfaces"] = [contract]
        lane["role_evidence"]["issue_ref"] = "github:issue/102"
        lane["role_evidence"]["contract_path"] = contract
        lane["evidence_sources"][0]["ref"] = "github:issue/102"
        repo["allowed_read_only_references"].append("github:issue/102")
        lane["wip_assignment"] = {
            "kind": "exception",
            "exception_name": "explicit_user_override",
            "repository": REPOSITORY,
            "active_issue_or_lane": LANE_ID,
            "blocked_active_issue_or_pr": "github:issue/101",
            "reason": "bounded test exception",
            "allowed_scope": f"{REPOSITORY}#102",
            "expiration_condition": "when issue 102 completes",
            "expires_at": EXPIRES,
            "authorized_by": "user:current-task/wip-exception",
            "recorded_in": "artifact:wip-exception/102",
        }
        set_request(
            plan,
            plan["action"]["request_text"]
            + f"; authorize WIP exception lane={REPOSITORY}#102 owner={LANE_ID}",
            "dispatch",
        )
        candidate = plan["candidate_inventory"][0]
        candidate["lane_id"] = f"{REPOSITORY}#102"
        plan["compatibility"] = [
            {
                "left": f"{REPOSITORY}#102",
                "right": LANE_ID,
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
        ]
        plan["runtime_preflight"] = runtime_preflight(
            lanes=plan["proposed_wave"]["lanes"]
        )
        self.assertEqual(validate_plan(plan, NOW), [])
        lane["wip_assignment"] = {"kind": "slot_owner"}
        assert_fragment(self, validate_plan(plan, NOW), "every proposed lane needs an exception")

    def test_released_lost_and_expired_claims_cannot_win(self) -> None:
        rows = []
        for index, status in enumerate(("released", "lost", "reserved"), start=1):
            rows.append(
                {
                    "claim_id": f"00000000-0000-4000-8000-{index:012d}",
                    "server_created_at": f"2026-07-13T11:5{index}:00Z",
                    "server_comment_id": index,
                    "status": status,
                    "expires_at": "2026-07-13T11:59:59Z" if status == "reserved" else EXPIRES,
                    "wave_slot": "wave-1",
                    "lane_ids": [LANE_ID],
                }
            )
        self.assertIsNone(choose_claim_winner(rows, now=NOW, wave_slot="wave-1"))

    def test_failed_claim_observation_is_valid_and_cannot_win(self) -> None:
        plan = prelaunch_plan()
        failed = copy.deepcopy(plan["proposed_wave"]["claim"]["competing_claims"][0])
        failed.update(
            {
                "claim_id": "33333333-3333-4333-8333-333333333333",
                "coordinator_id": "33333333-3333-4333-8333-333333333334",
                "server_comment_id": 1,
                "server_created_at": "2026-07-13T11:00:00Z",
                "receipt_ref": "github:claim-comment/failed-101",
                "status": "failed",
            }
        )
        plan["proposed_wave"]["claim"]["competing_claims"].append(failed)
        self.assertEqual(validate_plan(plan, NOW), [])

    def test_active_and_proposed_claims_cannot_share_a_wave_slot(self) -> None:
        plan = prelaunch_plan()
        plan["active_waves"] = copy.deepcopy(active_inspect_plan()["active_waves"])
        assert_fragment(
            self,
            validate_plan(plan, NOW),
            "must own a unique wave slot",
        )

        plan = active_inspect_plan()
        duplicate = copy.deepcopy(plan["active_waves"][0])
        duplicate["wave_id"] = "codex-b-20260713-active-two"
        duplicate["claim"]["claim_id"] = "22222222-2222-4222-8222-222222222222"
        duplicate["claim"]["wave_id"] = duplicate["wave_id"]
        duplicate["lanes"][0]["lane_id"] = f"{REPOSITORY}#102"
        duplicate["lanes"][0]["issue"] = 102
        plan["active_waves"].append(duplicate)
        assert_fragment(
            self,
            validate_plan(plan, NOW),
            "must own a unique wave slot",
        )

    def test_claim_refresh_must_be_complete_and_cover_slot_and_lane(self) -> None:
        plan = prelaunch_plan()
        plan["proposed_wave"]["claim"]["refresh_complete"] = False
        assert_fragment(self, validate_plan(plan, NOW), "refresh_complete")
        plan = prelaunch_plan()
        plan["proposed_wave"]["claim"]["competing_claims"][0]["lane_ids"] = [
            f"{REPOSITORY}#999"
        ]
        assert_fragment(self, validate_plan(plan, NOW), "does not make this claim the winner")

    def test_prelaunch_is_bound_to_exact_preclaim_bytes_and_selection(self) -> None:
        preclaim = preclaim_plan()
        prelaunch = prelaunch_plan()
        self.assertEqual(validate_prelaunch_against_preclaim(preclaim, prelaunch, NOW), [])
        prelaunch["proposed_wave"]["lanes"][0]["scope"]["dependencies"] = [
            f"{REPOSITORY}#999"
        ]
        errors = validate_prelaunch_against_preclaim(preclaim, prelaunch, NOW)
        assert_fragment(self, errors, "selected lane identity, scope, evidence, worktree, or head changed")

    def test_prelaunch_cannot_change_active_wave_state_after_preclaim(self) -> None:
        preclaim = preclaim_plan()
        prelaunch = prelaunch_plan()
        prelaunch["active_waves"] = copy.deepcopy(active_inspect_plan()["active_waves"])
        assert_fragment(
            self,
            validate_prelaunch_against_preclaim(preclaim, prelaunch, NOW),
            "active wave identity, runtime, worktree, head, or scope changed after preclaim",
        )

    def test_independent_discovery_and_worktree_sidecars_are_mandatory_truth_bindings(self) -> None:
        plan = preclaim_plan()
        discovery = discovery_observation()
        worktrees = worktree_observation()
        self.assertEqual(
            validate_plan_against_observations(plan, discovery, worktrees, NOW), []
        )
        wrong_discovery = copy.deepcopy(discovery)
        wrong_discovery["repositories"] = []
        assert_fragment(
            self,
            validate_plan_against_observations(plan, wrong_discovery, worktrees, NOW),
            "repository set must equal",
        )
        wrong_worktrees = copy.deepcopy(worktrees)
        wrong_worktrees["entries"][0]["branch"] = "codex/wrong"
        assert_fragment(
            self,
            validate_plan_against_observations(plan, discovery, wrong_worktrees, NOW),
            "branch differs from registry",
        )
        wrong_role = copy.deepcopy(discovery)
        wrong_role["scope_observations"][0]["role"] = "Codex G"
        assert_fragment(
            self,
            validate_plan_against_observations(plan, wrong_role, worktrees, NOW),
            "role differs from independent discovery",
        )

    def test_role_evidence_must_identify_the_exact_lane_issue(self) -> None:
        for role in ("Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"):
            plan = preclaim_plan(role)
            evidence = plan["proposed_wave"]["lanes"][0]["role_evidence"]
            field = "issue_target" if role == "Codex A" else "issue_ref"
            evidence[field] = "github:issue/999"
            with self.subTest(role=role):
                assert_fragment(
                    self,
                    validate_plan(plan, NOW),
                    "must identify the lane issue",
                )


class ResultJournalAndFallbackAdversarialTests(unittest.TestCase):
    @staticmethod
    def _insert_journal_action(result: dict[str, object], operation: str) -> None:
        events = result["events"]
        insert_at = next(
            index
            for index, event in enumerate(events)
            if event["operation"] == "result" and event["stage"] == "intent"
        )
        rows = []
        for suffix, stage in ((901, "intent"), (902, "succeeded")):
            rows.append(
                {
                    "event_id": f"99999999-9999-4999-8999-{suffix:012d}",
                    "idempotency_key": f"{operation}:{LANE_ID}:forbidden",
                    "wave_id": result["wave_id"],
                    "lane_id": LANE_ID,
                    "operation": operation,
                    "stage": stage,
                    "from_state": "running",
                    "to_state": "running",
                    "attempt": 1,
                    "occurred_at": OBSERVED,
                    "receipt_ref": "receipt:forbidden/101" if stage == "succeeded" else None,
                    "failure_code": None,
                }
            )
        events[insert_at:insert_at] = rows

    def test_event_journal_rejects_every_cross_role_side_effect(self) -> None:
        for role, forbidden in {
            "Codex A": "draft_pr_write",
            "Codex B": "git_push",
            "Codex D": "git_commit",
            "Codex E": "issue_write",
            "Codex G": "git_push",
        }.items():
            result = completed_result(role)
            self._insert_journal_action(result, forbidden)
            with self.subTest(role=role, forbidden=forbidden):
                assert_fragment(
                    self,
                    validate_result(result, NOW),
                    "unauthorized journal operation",
                )

        g_result = completed_result("Codex G")
        self._insert_journal_action(g_result, "git_push")
        assert_fragment(
            self,
            validate_result_against_plan(prelaunch_plan("Codex G"), g_result, NOW),
            "unauthorized journal operation",
        )
        assert_fragment(
            self,
            validate_result_against_outcome_observation(
                prelaunch_plan("Codex G"),
                g_result,
                outcome_observation("Codex G"),
                NOW,
            ),
            "unauthorized journal operation",
        )

    def test_release_roles_honor_findings_validation_and_stop_conditions(self) -> None:
        mutators = {
            "open high finding": lambda handoff: handoff["findings"].append(
                {
                    "finding_id": "HIGH-NEW",
                    "severity": "high",
                    "blocking": False,
                    "status": "open",
                }
            ),
            "failed validation": lambda handoff: handoff["validation"][0].update(
                {"result": "failed"}
            ),
            "stop condition": lambda handoff: handoff["stop_conditions"].append(
                "owner approval missing"
            ),
        }
        for role in ("Codex E", "Codex F", "Codex G"):
            for name, mutate in mutators.items():
                result = completed_result(role)
                handoff = result["lanes"][0]["handoff"]
                mutate(handoff)
                handoff["digest"] = canonical_document_digest(
                    {key: value for key, value in handoff.items() if key != "digest"}
                )
                with self.subTest(role=role, blocker=name):
                    errors = validate_result_against_plan(
                        prelaunch_plan(role), result, NOW
                    )
                    assert_fragment(self, errors, "open high finding")
                    if role in {"Codex F", "Codex G"}:
                        assert_fragment(
                            self,
                            validate_result_against_outcome_observation(
                                prelaunch_plan(role),
                                result,
                                outcome_observation(role),
                                NOW,
                            ),
                            "open high finding" if role == "Codex F" else "G ready verdict",
                        )
    def test_every_field_of_every_role_result_is_required(self) -> None:
        for role in ("Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"):
            baseline = completed_result(role)
            for field in list(baseline["lanes"][0]["role_result"]):
                result = completed_result(role)
                del result["lanes"][0]["role_result"][field]
                with self.subTest(role=role, field=field):
                    assert_fragment(self, validate_result(result, NOW), "missing fields")

    def test_role_result_and_handoff_content_digests_are_recomputed(self) -> None:
        result = completed_result("Codex B")
        result["lanes"][0]["role_result"]["contract_ref"] = "docs/contracts/tampered.md"
        assert_fragment(self, validate_result(result, NOW), "canonical role_result content")
        result = completed_result("Codex B")
        result["lanes"][0]["handoff"]["target_artifact"] = "artifact:tampered"
        assert_fragment(self, validate_result(result, NOW), "canonical handoff content")

    def test_role_specific_outputs_bind_to_prelaunch_authority(self) -> None:
        cases = {
            "Codex A": ("problem_representation_ref", "artifact:wrong", "A problem representation"),
            "Codex B": ("contract_ref", "docs/contracts/wrong.md", "B contract target"),
            "Codex D": ("addressed_finding_ids", ["WRONG"], "D finding IDs"),
            "Codex F": ("accepted_review_ref", "review:wrong", "accepted review reference"),
            "Codex G": ("required_checks", ["wrong"], "G required_checks drifted"),
        }
        for role, (field, value, fragment) in cases.items():
            result = completed_result(role)
            result["lanes"][0]["role_result"][field] = value
            result["lanes"][0]["role_result_digest"] = canonical_document_digest(
                result["lanes"][0]["role_result"]
            )
            with self.subTest(role=role):
                assert_fragment(
                    self,
                    validate_result_against_plan(prelaunch_plan(role), result, NOW),
                    fragment,
                )

    def test_open_high_finding_blocks_e_even_when_packet_marks_nonblocking(self) -> None:
        result = completed_result("Codex E")
        result["lanes"][0]["handoff"]["findings"] = [
            {
                "finding_id": "HIGH-OPEN",
                "severity": "high",
                "blocking": False,
                "status": "open",
            }
        ]
        result["lanes"][0]["handoff"]["digest"] = canonical_document_digest(
            {k: v for k, v in result["lanes"][0]["handoff"].items() if k != "digest"}
        )
        assert_fragment(self, validate_result(result, NOW), "open blocking findings")

    def test_g_not_ready_is_valid_but_ready_requires_every_gate(self) -> None:
        result = completed_result("Codex G")
        role_result = result["lanes"][0]["role_result"]
        role_result["passing_checks"] = []
        role_result["checks_passed"] = False
        role_result["review_state"] = "pending"
        role_result["readiness_verdict"] = "not_ready"
        result["lanes"][0]["role_result_digest"] = canonical_document_digest(role_result)
        assert_fragment(
            self,
            validate_result(result, NOW),
            "g_pr_head_base_checks_approval_method_or_closeout_scope_drift",
        )
        result["status"] = "reconciliation_required"
        result["fallback"] = result_fallback(
            triggered=True,
            reason_code="g_pr_head_base_checks_approval_method_or_closeout_scope_drift",
            role="Codex G",
        )
        self.assertEqual(validate_result(result, NOW), [])
        result["status"] = "completed"
        result["fallback"] = result_fallback(role="Codex G")
        role_result["readiness_verdict"] = "ready_for_dedicated_g"
        result["lanes"][0]["role_result_digest"] = canonical_document_digest(role_result)
        assert_fragment(self, validate_result(result, NOW), "requires every readiness gate")

    def test_event_order_is_continuous_and_logical_operation_is_unique_across_keys(self) -> None:
        result = completed_result()
        result["events"][4], result["events"][5] = result["events"][5], result["events"][4]
        assert_fragment(self, validate_result(result, NOW), "outcome must follow")
        result = completed_result()
        retry = copy.deepcopy(result["events"][4])
        retry["event_id"] = "99999999-9999-4999-8999-999999999999"
        retry["idempotency_key"] = "different-key-cannot-hide-retry"
        retry["attempt"] = 2
        result["events"].append(retry)
        assert_fragment(self, validate_result(result, NOW), "logical operation")

    def test_unknown_outcome_cannot_be_retried_and_requires_exact_fallback_reason(self) -> None:
        result = completed_result()
        unknown = result["events"][5]
        unknown["stage"] = "unknown"
        unknown["receipt_ref"] = None
        retry = copy.deepcopy(result["events"][4])
        retry["event_id"] = "99999999-9999-4999-8999-999999999999"
        retry["attempt"] = 2
        result["events"].insert(6, retry)
        result["status"] = "reconciliation_required"
        result["fallback"] = result_fallback(
            triggered=True,
            reason_code="invalid_lane_result_or_handoff",
        )
        errors = validate_result(result, NOW)
        assert_fragment(self, errors, "unknown side effect cannot be retried")
        assert_fragment(
            self,
            errors,
            "observed state requires partial_transition_without_proven_idempotent_recovery",
        )

    def test_triggered_fallback_and_partial_g_always_require_human_reconciliation(self) -> None:
        result = completed_result("Codex G")
        result["status"] = "reconciliation_required"
        result["fallback"] = result_fallback(
            triggered=True,
            reason_code="partial_g_action",
            role="Codex G",
        )
        result["fallback"]["human_reconciliation_required"] = False
        assert_fragment(self, validate_result(result, NOW), "fallback requires true")


class AdditionalReleaseGapTests(unittest.TestCase):
    def test_negative_objects_and_request_role_mismatches_fail_closed(self) -> None:
        for request in (
            "Dispatch nothing",
            "Dispatch? No.",
            "Dispatch no lanes",
            "Run nothing",
            "Process no issues",
            "Publish nothing",
            "Dispatch no actions; just report status",
        ):
            with self.subTest(request=request):
                self.assertEqual(normalize_invocation(request), "inspect")
        plan = preclaim_plan("Codex B")
        set_request(plan, "Dispatch Codex E for issue 101")
        assert_fragment(self, validate_plan(plan, NOW), "must match the role")
        plan = preclaim_plan("Codex B")
        set_request(plan, "Publish Codex B for issue 101")
        assert_fragment(self, validate_plan(plan, NOW), "exactly one unambiguous")

    def test_untrusted_sources_cannot_grant_dispatch_read_publication_or_g_authority(self) -> None:
        plan = preclaim_plan()
        plan["action"]["authority_ref"] = "github:untrusted-comment/999"
        assert_fragment(self, validate_plan(plan, NOW), "current-user task authority")
        plan = preclaim_plan()
        plan["inventory"]["repositories"][0]["read_authority_ref"] = (
            "github:untrusted-comment/999"
        )
        assert_fragment(self, validate_plan(plan, NOW), "current-user task authority")
        plan = preclaim_plan("Codex F")
        plan["proposed_wave"]["lanes"][0]["role_evidence"][
            "publication_approval_ref"
        ] = "untrusted:issue-comment/999"
        assert_fragment(self, validate_plan(plan, NOW), "publication_approval_ref")
        plan = preclaim_plan("Codex G")
        plan["proposed_wave"]["lanes"][0]["role_evidence"][
            "readiness_authority_ref"
        ] = "untrusted:issue-comment/999"
        assert_fragment(self, validate_plan(plan, NOW), "readiness_authority_ref")

    def test_g_not_ready_preclaim_is_valid_and_does_not_claim_readiness(self) -> None:
        plan = preclaim_plan("Codex G")
        evidence = plan["proposed_wave"]["lanes"][0]["role_evidence"]
        evidence["passing_checks"] = []
        evidence["checks_passed"] = False
        evidence["unresolved_findings"] = ["HIGH-OPEN"]
        evidence["review_state"] = "pending"
        plan["runtime_preflight"] = runtime_preflight(
            lanes=plan["proposed_wave"]["lanes"]
        )
        self.assertEqual(validate_plan(plan, NOW), [])

    def test_scope_identifiers_are_canonical_and_overlap_is_derived(self) -> None:
        plan, _ = two_lane_preclaim_and_prelaunch()
        lanes = plan["proposed_wave"]["lanes"]
        lanes[0]["scope"]["external_state"] = ["github:tracker/1"]
        lanes[1]["scope"]["external_state"] = ["github:tracker/1"]
        assert_fragment(self, validate_plan(plan, NOW), "shared_external_state must equal")
        lanes[1]["scope"]["external_state"] = ["GitHub:Tracker/1"]
        assert_fragment(self, validate_plan(plan, NOW), "canonical lowercase identifier")
        for alias in (
            "github:tracker/1/",
            "github:tracker//1",
            "github:tracker/./1",
            "github:pr/01",
        ):
            lanes[1]["scope"]["external_state"] = [alias]
            with self.subTest(alias=alias):
                assert_fragment(
                    self,
                    validate_plan(plan, NOW),
                    "alias-free typed segments",
                )

    def test_dependency_order_and_out_of_pool_dependencies_are_enforced(self) -> None:
        plan, _ = two_lane_preclaim_and_prelaunch()
        left, right = [lane["lane_id"] for lane in plan["proposed_wave"]["lanes"]]
        plan["proposed_wave"]["lanes"][0]["scope"]["dependencies"] = [right]
        row = plan["compatibility"][0]
        row.update(
            {
                "verdict": "concurrent_until_integration_then_serialize",
                "dependency_relation": "left_depends_on_right",
                "integration_order": [left, right],
                "invalidation_triggers": ["right integration"],
                "refresh_barrier": "refresh after dependency",
                "refresh_bindings": ["git:head"],
            }
        )
        assert_fragment(self, validate_plan(plan, NOW), "dependency must integrate before")
        plan = preclaim_plan()
        plan["proposed_wave"]["lanes"][0]["scope"]["dependencies"] = [
            f"{REPOSITORY}#999"
        ]
        assert_fragment(self, validate_plan(plan, NOW), "unresolved out-of-pool")

    def test_active_wave_identity_is_bound_to_independent_discovery(self) -> None:
        plan = active_inspect_plan()
        discovery = discovery_observation()
        discovery["candidate_inventory"] = copy.deepcopy(plan["candidate_inventory"])
        discovery["repositories"][0]["active_slot_lane_id"] = LANE_ID
        discovery["repositories"][0]["active_lane_ids"] = [LANE_ID]
        wave = plan["active_waves"][0]
        claim = wave["claim"]
        lane = wave["lanes"][0]
        reserve = lane["reservation"]
        runtime = lane["runtime"]
        discovery["active_waves"] = [
            {
                "wave_id": wave["wave_id"],
                "coordinator_id": wave["coordinator_id"],
                "role": wave["role"],
                "state": wave["state"],
                "claim_id": claim["claim_id"],
                "claim_receipt_ref": claim["receipt_ref"],
                "claim_plan_digest": claim["plan_digest"],
                "refresh_snapshot_id": claim["refresh_snapshot_id"],
                "refresh_receipt_ref": claim["refresh_receipt_ref"],
                "expires_at": claim["expires_at"],
                "lanes": [
                    {
                        "lane_id": lane["lane_id"],
                        "state": lane["state"],
                        "reservation_claim_id": reserve["claim_id"],
                        "reservation_receipt_ref": reserve["receipt_ref"],
                        "reservation_idempotency_key": reserve["idempotency_key"],
                        "runtime_agent_id": runtime["agent_id"],
                        "runtime_state": runtime["state"],
                        "runtime_launch_receipt": runtime["launch_receipt"],
                        "runtime_launch_readback": copy.deepcopy(
                            runtime["launch_readback"]
                        ),
                    }
                ],
            }
        ]
        plan["inventory"]["sources"][0]["sha256"] = canonical_document_digest(discovery)
        self.assertEqual(
            validate_plan_against_observations(
                plan, discovery, worktree_observation(), NOW
            ),
            [],
        )
        plan["active_waves"][0]["claim"]["receipt_ref"] = "github:invented/claim"
        plan["active_waves"][0]["claim"]["competing_claims"][0][
            "receipt_ref"
        ] = "github:invented/claim"
        assert_fragment(
            self,
            validate_plan_against_observations(
                plan, discovery, worktree_observation(), NOW
            ),
            "active wave, claim, reservation, or runtime identity differs",
        )

    def test_candidate_completeness_is_bound_to_independent_discovery(self) -> None:
        plan = preclaim_plan()
        discovery = discovery_observation()
        older = copy.deepcopy(discovery["candidate_inventory"][0])
        older.update(
            {
                "lane_id": f"{REPOSITORY}#100",
                "ready_since": "2026-07-13T09:00:00Z",
                "selected": False,
            }
        )
        discovery["candidate_inventory"].append(older)
        plan["inventory"]["sources"][0]["sha256"] = canonical_document_digest(discovery)
        assert_fragment(
            self,
            validate_plan_against_observations(
                plan, discovery, worktree_observation(), NOW
            ),
            "candidate inventory must exactly match",
        )

    def test_handoff_changed_files_are_bound_for_all_roles(self) -> None:
        for role in ("Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"):
            result = completed_result(role)
            handoff = result["lanes"][0]["handoff"]
            handoff["files_changed"] = [".env"]
            handoff["digest"] = canonical_document_digest(
                {key: value for key, value in handoff.items() if key != "digest"}
            )
            with self.subTest(role=role):
                assert_fragment(
                    self,
                    validate_result_against_plan(prelaunch_plan(role), result, NOW),
                    "files_changed drifted from plan scope",
                )

    def test_fully_completed_lanes_cannot_be_relabelled_as_failure_states(self) -> None:
        cases = {
            "dispatch_aborted": "ambiguous_request_or_side_effect",
            "orphaned_reconciliation_required": "orphaned_or_unreconciled_agent",
            "incomplete_interrupted": "invalid_lane_result_or_handoff",
        }
        for status, reason in cases.items():
            result = completed_result()
            result["status"] = status
            result["fallback"] = result_fallback(triggered=True, reason_code=reason)
            with self.subTest(status=status):
                assert_fragment(
                    self,
                    validate_result(result, NOW),
                    "fully completed and released lanes require",
                )

    def test_completed_role_cannot_skip_the_transition_matrix(self) -> None:
        for role, invalid_next in {
            "Codex A": "Codex G",
            "Codex B": "Codex F",
            "Codex D": "Codex B",
            "Codex F": "Codex C",
            "Codex G": "Codex A",
        }.items():
            result = completed_result(role)
            result["lanes"][0]["next_role"] = invalid_next
            handoff = result["lanes"][0]["handoff"]
            handoff["next_role"] = invalid_next
            handoff["digest"] = canonical_document_digest(
                {key: value for key, value in handoff.items() if key != "digest"}
            )
            with self.subTest(role=role):
                assert_fragment(self, validate_result(result, NOW), "transition matrix")

    def test_completed_roles_require_exact_unique_external_actions(self) -> None:
        result = completed_result("Codex B")
        result["lanes"][0]["external_actions"] = []
        assert_fragment(self, validate_result(result, NOW), "exact typed action set")
        result = completed_result("Codex F")
        result["lanes"][0]["external_actions"].append(
            copy.deepcopy(result["lanes"][0]["external_actions"][0])
        )
        assert_fragment(self, validate_result(result, NOW), "duplicate logical external action")

    def test_reservation_and_release_idempotency_keys_bind_lane_claim_and_journal(self) -> None:
        plan = prelaunch_plan()
        plan["proposed_wave"]["lanes"][0]["reservation"]["idempotency_key"] = (
            "reserve:wrong"
        )
        assert_fragment(self, validate_plan(plan, NOW), "must bind lane and winning claim")
        result = completed_result()
        result["lanes"][0]["release"]["idempotency_key"] = "release:wrong"
        errors = validate_result(result, NOW)
        assert_fragment(self, errors, "must bind lane and claim")
        assert_fragment(self, errors, "idempotency key must match")

    def test_f_structured_pr_targets_and_independent_outcome_are_bound(self) -> None:
        plan = prelaunch_plan("Codex F")
        result = completed_result("Codex F")
        outcome = outcome_observation("Codex F")
        self.assertEqual(
            validate_result_against_outcome_observation(plan, result, outcome, NOW), []
        )
        result["lanes"][0]["external_actions"][2]["target"] = "github:pr/999"
        assert_fragment(self, validate_result(result, NOW), "draft_pr_write target drifted")
        result = completed_result("Codex F")
        outcome["lanes"][0]["commit_parent"] = "0" * 40
        outcome["digest"] = canonical_document_digest(
            {key: value for key, value in outcome.items() if key != "digest"}
        )
        assert_fragment(
            self,
            validate_result_against_outcome_observation(plan, result, outcome, NOW),
            "reviewed pre-publication head",
        )

    def test_g_ready_result_is_bound_to_independent_pr_state(self) -> None:
        plan = prelaunch_plan("Codex G")
        result = completed_result("Codex G")
        outcome = outcome_observation("Codex G")
        self.assertEqual(
            validate_result_against_outcome_observation(plan, result, outcome, NOW), []
        )
        outcome["lanes"][0]["review_state"] = "pending"
        outcome["digest"] = canonical_document_digest(
            {key: value for key, value in outcome.items() if key != "digest"}
        )
        assert_fragment(
            self,
            validate_result_against_outcome_observation(plan, result, outcome, NOW),
            "review_state: drifted from typed G result",
        )

    def test_prelaunch_cannot_change_compatibility_evidence_after_claim(self) -> None:
        preclaim, prelaunch = two_lane_preclaim_and_prelaunch()
        self.assertEqual(validate_prelaunch_against_preclaim(preclaim, prelaunch, NOW), [])
        prelaunch["compatibility"][0]["evidence_refs"] = ["artifact:changed-after-claim"]
        assert_fragment(
            self,
            validate_prelaunch_against_preclaim(preclaim, prelaunch, NOW),
            "compatibility evidence or sequencing changed",
        )

    def test_fairness_uses_oldest_then_canonical_lane_id_within_a_tier(self) -> None:
        candidates = []
        for issue, ready in ((103, "2026-07-13T09:00:00Z"), (102, "2026-07-13T08:00:00Z"), (101, "2026-07-13T08:00:00Z")):
            candidates.append(
                {
                    "lane_id": f"{REPOSITORY}#{issue}",
                    "status": "ready_queued",
                    "eligible": True,
                    "ready_since": ready,
                    "eligible_defer_count": 0,
                    "finding_ids": [],
                    "exclusion_reason": None,
                }
            )
        self.assertEqual(
            select_lanes(candidates, 3),
            [f"{REPOSITORY}#101", f"{REPOSITORY}#102", f"{REPOSITORY}#103"],
        )


class FinalReleaseBoundaryTests(unittest.TestCase):
    @staticmethod
    def _aborted_result(*, failed_operation: str | None = None) -> dict[str, object]:
        result = completed_result()
        lane_value = result["lanes"][0]
        result["status"] = "dispatch_aborted"
        lane_value.update(
            {
                "claim_id": None if failed_operation is None else lane_value["claim_id"],
                "launch_state": "not_started" if failed_operation is None else "launch_failed",
                "result_status": "ready_queued" if failed_operation is None else "launch_failed",
                "next_role": None,
                "result_ref": None,
                "result_digest": None,
                "role_result": None,
                "role_result_digest": None,
                "handoff": None,
                "launch_readback": None,
                "release": None,
                "external_actions": [],
            }
        )
        if failed_operation is None:
            result["events"] = []
            reason = "ambiguous_request_or_side_effect"
        else:
            succeeded_index = next(
                index
                for index, event in enumerate(result["events"])
                if event["operation"] == failed_operation and event["stage"] == "succeeded"
            )
            failed = result["events"][succeeded_index]
            failed["stage"] = "failed"
            failed["receipt_ref"] = None
            failed["failure_code"] = f"{failed_operation}_failed"
            result["events"] = result["events"][: succeeded_index + 1]
            lane_value["release"] = {
                "claim_id": lane_value["claim_id"],
                "idempotency_key": f"release:{LANE_ID}:{lane_value['claim_id']}",
                "status": "routing_failed_reconciliation_required",
                "receipt_ref": None,
                "released_at": OBSERVED,
            }
            reason = (
                "claim_acquisition_or_winner_readback_failure"
                if failed_operation == "claim"
                else "partial_transition_without_proven_idempotent_recovery"
            )
        result["fallback"] = result_fallback(
            triggered=True, reason_code=reason, role="Codex B"
        )
        return result

    def test_fallback_reason_is_derived_from_the_journaled_failure(self) -> None:
        self.assertEqual(validate_result(self._aborted_result(), NOW), [])
        for operation in ("claim", "reserve", "launch"):
            result = self._aborted_result(failed_operation=operation)
            with self.subTest(operation=operation):
                self.assertEqual(validate_result(result, NOW), [])
                result["fallback"]["reason_code"] = "ambiguous_request_or_side_effect"
                expected = (
                    "claim_acquisition_or_winner_readback_failure"
                    if operation == "claim"
                    else "partial_transition_without_proven_idempotent_recovery"
                )
                assert_fragment(self, validate_result(result, NOW), expected)

    def test_g_check_waivers_are_not_accepted_as_readiness_authority(self) -> None:
        plan = preclaim_plan("Codex G")
        evidence = plan["proposed_wave"]["lanes"][0]["role_evidence"]
        evidence.update(
            {
                "required_checks": ["ci"],
                "passing_checks": [],
                "waived_checks": ["ci"],
                "waiver_refs": ["review:pr-state/101"],
                "checks_passed": True,
            }
        )
        assert_fragment(self, validate_plan(plan, NOW), "does not accept check waivers")

    def test_exception_authority_markers_fail_closed_under_negation_or_quotation(self) -> None:
        plan = preclaim_plan()
        set_request(
            plan,
            plan["action"]["request_text"].replace(
                f"authorize repository={REPOSITORY}",
                f"do not authorize repository={REPOSITORY}",
            ),
            "dispatch",
        )
        assert_fragment(self, validate_plan(plan, NOW), "deterministic request normalization inspect")

        plan = preclaim_plan()
        set_request(
            plan,
            plan["action"]["request_text"].replace(
                f"authorize repository={REPOSITORY}",
                f'"authorize repository={REPOSITORY}"',
            ),
            "dispatch",
        )
        assert_fragment(self, validate_plan(plan, NOW), "repositories explicitly authorized")

        plan = preclaim_plan("Codex F")
        lane_value = plan["proposed_wave"]["lanes"][0]
        lane_value["target_branch"] = "main"
        lane_value["role_evidence"]["approved_base"] = "main"
        lane_value["role_evidence"]["main_target_approval_ref"] = (
            "user:current-task/main-target"
        )
        set_request(
            plan,
            plan["action"]["request_text"] + "; do not authorize draft PR target=main",
            "dispatch",
        )
        assert_fragment(self, validate_plan(plan, NOW), "deterministic request normalization inspect")

        plan = preclaim_plan()
        preflight = plan["runtime_preflight"]
        preflight.update(
            {
                "requested_model": "attacker-model",
                "effective_model": "attacker-model",
                "override_authority_ref": "user:current-task/runtime-override/101",
                "override_granted_at": OBSERVED,
                "override_model": "attacker-model",
                "override_reasoning_effort": "max",
                "override_reason": "test",
            }
        )
        set_request(
            plan,
            plan["action"]["request_text"]
            + "; do not authorize runtime override model=attacker-model reasoning_effort=max",
            "dispatch",
        )
        preflight["override_request_sha256"] = plan["action"]["request_sha256"]
        assert_fragment(self, validate_plan(plan, NOW), "deterministic request normalization inspect")

    def test_inventory_rejects_any_repository_not_named_by_current_request(self) -> None:
        plan = preclaim_plan()
        second_repo = copy.deepcopy(plan["inventory"]["repositories"][0])
        second_repo.update(
            {
                "repository_id": "other/public-repo",
                "remote_url": "https://github.com/other/public-repo",
                "visibility": "public",
                "read_scope": "metadata_only",
                "read_authority_ref": None,
                "allowed_read_only_references": [],
                "private_content_authorized": False,
                "active_slot_lane_id": None,
                "active_lane_ids": [],
            }
        )
        plan["inventory"]["repositories"].append(second_repo)
        second_source = copy.deepcopy(plan["inventory"]["sources"][0])
        second_source.update(
            {
                "ref": "core:repo-map-observation/public-extra",
                "sha256": "1" * 64,
                "repositories": ["other/public-repo"],
            }
        )
        plan["inventory"]["sources"].append(second_source)
        assert_fragment(
            self,
            validate_plan(plan, NOW),
            "repositories explicitly authorized in request_text",
        )

    def test_override_reason_and_protected_surface_rules_are_strict(self) -> None:
        plan = preclaim_plan()
        plan["runtime_preflight"]["override_reason"] = "not allowed at defaults"
        assert_fragment(self, validate_plan(plan, NOW), "default runtime must not carry")

        plan = preclaim_plan()
        lane_value = plan["proposed_wave"]["lanes"][0]
        lane_value["scope"]["protected_surfaces"] = ["parser/state"]
        lane_value["scope"]["protected_surface_contract_ref"] = "artifact:fake"
        assert_fragment(self, validate_plan(plan, NOW), "not eligible for pooled dispatch")

    def test_claim_identity_and_receipts_are_not_interchangeable(self) -> None:
        plan = prelaunch_plan()
        plan["proposed_wave"]["claim"]["competing_claims"][0][
            "coordinator_id"
        ] = "44444444-4444-4444-8444-444444444444"
        assert_fragment(self, validate_plan(plan, NOW), "own observation must match claim receipt")

        result = completed_result("Codex F")
        for action in result["lanes"][0]["external_actions"]:
            action["receipt"] = "receipt:git_commit/shared"
        for event in result["events"]:
            if event["stage"] == "succeeded" and event["operation"] in {
                "git_commit",
                "git_push",
                "draft_pr_write",
            }:
                event["receipt_ref"] = "receipt:git_commit/shared"
        assert_fragment(
            self,
            validate_result(result, NOW),
            "cannot evidence multiple logical side effects",
        )

    def test_per_lane_launch_record_is_complete_and_bound_to_preflight_and_packet(self) -> None:
        for field in list(completed_result()["lanes"][0]["launch_readback"]):
            result = completed_result()
            del result["lanes"][0]["launch_readback"][field]
            with self.subTest(field=field):
                assert_fragment(self, validate_result(result, NOW), "missing fields")

        result = completed_result()
        result["lanes"][0]["launch_readback"]["packet_digest"] = "0" * 64
        assert_fragment(
            self,
            validate_result_against_plan(prelaunch_plan(), result, NOW),
            "packet_digest drifted from exact lane packet",
        )
        for field_name, value, fragment in (
            ("launcher_preflight_digest", "1" * 64, "drifted from preflight"),
            (
                "selected_executable_sha256",
                "2" * 64,
                "drifted from selected executable",
            ),
            (
                "selected_executable_path",
                r"C:\Codex\bin\other\codex.exe",
                "drifted from selected executable",
            ),
        ):
            result = completed_result()
            result["lanes"][0]["launch_readback"][field_name] = value
            with self.subTest(field=field_name):
                assert_fragment(
                    self,
                    validate_result_against_plan(prelaunch_plan(), result, NOW),
                    fragment,
                )
        result = completed_result()
        result["lanes"][0]["launch_readback"]["effective_model"] = "platform-model"
        result["lanes"][0]["launch_readback"]["effective_reasoning_effort"] = "high"
        self.assertEqual(
            validate_result_against_plan(prelaunch_plan(), result, NOW),
            [],
        )

    def test_f_outcome_requires_every_safety_gate_and_exact_changed_files(self) -> None:
        mutators = {
            "finding": lambda lane_value: lane_value.update(
                {"unresolved_findings": ["HIGH-OPEN"]}
            ),
            "scope": lambda lane_value: lane_value.update({"diff_scope_passed": False}),
            "forbidden": lambda lane_value: lane_value.update(
                {"forbidden_files_passed": False}
            ),
            "extra file": lambda lane_value: lane_value["changed_files"].append("extra.py"),
        }
        for name, mutate in mutators.items():
            outcome = outcome_observation("Codex F")
            mutate(outcome["lanes"][0])
            outcome["digest"] = canonical_document_digest(
                {key: value for key, value in outcome.items() if key != "digest"}
            )
            with self.subTest(gate=name):
                errors = validate_result_against_outcome_observation(
                    prelaunch_plan("Codex F"),
                    completed_result("Codex F"),
                    outcome,
                    NOW,
                )
                expected = "changed_files" if name == "extra file" else "F outcome requires"
                assert_fragment(self, errors, expected)

        pending = outcome_observation("Codex F")
        pending["lanes"][0].update(
            {
                "required_checks": ["ci"],
                "passing_checks": [],
                "checks_passed": False,
                "review_state": "pending",
            }
        )
        pending["digest"] = canonical_document_digest(
            {key: value for key, value in pending.items() if key != "digest"}
        )
        self.assertEqual(
            validate_result_against_outcome_observation(
                prelaunch_plan("Codex F"),
                completed_result("Codex F"),
                pending,
                NOW,
            ),
            [],
        )

    def test_f_requires_typed_accepted_review_and_passing_head_bound_validation(self) -> None:
        plan = preclaim_plan("Codex F")
        self.assertEqual(validate_plan(plan, NOW), [])

        failed = preclaim_plan("Codex F")
        failed["proposed_wave"]["lanes"][0]["role_evidence"][
            "validation_results"
        ][0]["result"] = "failed"
        assert_fragment(self, validate_plan(failed, NOW), "validation must pass")

        for generic_ref in (
            "github:issue/101",
            "git:head/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        ):
            generic = preclaim_plan("Codex F")
            evidence = generic["proposed_wave"]["lanes"][0]["role_evidence"]
            evidence["validation_refs"] = [generic_ref]
            evidence["validation_results"][0]["evidence_ref"] = generic_ref
            with self.subTest(validation_ref=generic_ref):
                assert_fragment(
                    self,
                    validate_plan(generic, NOW),
                    "must bind one exact current evidence source",
                )

        generic_review = preclaim_plan("Codex F")
        evidence = generic_review["proposed_wave"]["lanes"][0]["role_evidence"]
        evidence["review_ref"] = "github:issue/101"
        evidence["accepted_review"]["review_ref"] = "github:issue/101"
        assert_fragment(
            self,
            validate_plan(generic_review, NOW),
            "accepted E/handoff evidence source",
        )

    def test_e_changes_required_routes_to_d_and_g_binds_all_open_findings(self) -> None:
        result = completed_result("Codex E")
        lane_value = result["lanes"][0]
        lane_value["next_role"] = "Codex D"
        lane_value["finding_ids"] = ["HIGH-REVIEW"]
        lane_value["role_result"]["review_verdict"] = "changes_required"
        lane_value["role_result"]["blocking_findings"] = 1
        lane_value["role_result_digest"] = canonical_document_digest(
            lane_value["role_result"]
        )
        lane_value["handoff"]["next_role"] = "Codex D"
        lane_value["handoff"]["findings"] = [
            {
                "finding_id": "HIGH-REVIEW",
                "severity": "high",
                "blocking": False,
                "status": "open",
            }
        ]
        lane_value["handoff"]["digest"] = canonical_document_digest(
            {
                key: value
                for key, value in lane_value["handoff"].items()
                if key != "digest"
            }
        )
        self.assertEqual(validate_result(result, NOW), [])

        result = completed_result("Codex G")
        handoff = result["lanes"][0]["handoff"]
        handoff["findings"] = [
            {
                "finding_id": "MEDIUM-OPEN",
                "severity": "medium",
                "blocking": True,
                "status": "open",
            }
        ]
        handoff["digest"] = canonical_document_digest(
            {key: value for key, value in handoff.items() if key != "digest"}
        )
        assert_fragment(
            self,
            validate_result(result, NOW),
            "unresolved_findings must exactly equal",
        )


class CommandLineGateTests(unittest.TestCase):
    def _write(self, directory: Path, name: str, value: object) -> Path:
        path = directory / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_cli_rejects_plan_without_independent_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            plan_path = self._write(directory, "plan.json", preclaim_plan())
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT),
                    str(plan_path),
                    "--offline-synthetic-fixture",
                    "--now",
                    OBSERVED,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("requires --discovery", completed.stderr)
            self.assertIn("requires --worktrees", completed.stderr)

    def test_cli_active_inspect_requires_and_accepts_physical_worktree_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            plan_value = active_inspect_plan()
            discovery_value = discovery_for_plan(plan_value)
            plan_value["inventory"]["sources"][0]["sha256"] = canonical_document_digest(
                discovery_value
            )
            plan_path = self._write(directory, "active-inspect.json", plan_value)
            discovery_path = self._write(directory, "discovery.json", discovery_value)
            worktrees_path = self._write(
                directory, "worktrees.json", worktree_observation()
            )
            receipts_path = self._write(
                directory,
                "launcher-receipts.json",
                launcher_receipt_sidecars_for_document(plan_value),
            )
            base = [
                sys.executable,
                "-B",
                str(SCRIPT),
                str(plan_path),
                "--discovery",
                str(discovery_path),
                "--offline-synthetic-fixture",
                "--now",
                OBSERVED,
            ]
            missing = subprocess.run(base, check=False, capture_output=True, text=True)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("active-wave plan validation requires --worktrees", missing.stderr)
            valid = subprocess.run(
                base
                + [
                    "--worktrees",
                    str(worktrees_path),
                    "--launcher-receipts",
                    str(receipts_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(valid.returncode, 0, valid.stderr)

    def test_cli_accepts_fully_bound_result_and_rejects_missing_preclaim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            preclaim = self._write(directory, "preclaim.json", preclaim_plan())
            prelaunch = self._write(directory, "prelaunch.json", prelaunch_plan())
            result_value = completed_result()
            result = self._write(directory, "result.json", result_value)
            receipts = self._write(
                directory,
                "launcher-receipts.json",
                launcher_receipt_sidecars_for_document(result_value),
            )
            discovery = self._write(directory, "discovery.json", discovery_observation())
            worktrees = self._write(directory, "worktrees.json", worktree_observation())
            base = [
                sys.executable,
                "-B",
                str(SCRIPT),
                str(result),
                "--plan",
                str(prelaunch),
                "--discovery",
                str(discovery),
                "--worktrees",
                str(worktrees),
                "--launcher-receipts",
                str(receipts),
                "--offline-synthetic-fixture",
                "--now",
                OBSERVED,
            ]
            missing = subprocess.run(base, check=False, capture_output=True, text=True)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("requires --plan, --preclaim, --discovery, and --worktrees", missing.stderr)
            valid = subprocess.run(
                base + ["--preclaim", str(preclaim)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(valid.returncode, 0, valid.stderr)

    def test_cli_rejects_duplicate_json_keys_before_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "duplicate.json"
            path.write_text(
                '{"schema_version":"first","schema_version":"second"}',
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, "-B", str(SCRIPT), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("duplicate JSON key: schema_version", completed.stderr)


if __name__ == "__main__":
    unittest.main()
