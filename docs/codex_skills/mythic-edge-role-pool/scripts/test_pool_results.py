from __future__ import annotations

import copy
import unittest

from check_pool_plan import (
    FALLBACK_CONDITION_IDS,
    OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
    evaluate_fallback,
    validate_result as validate_result_production,
    validate_result_offline_synthetic_fixture,
    validate_result_against_plan as validate_result_against_plan_production,
)
from pool_test_fixtures import (
    HEAD,
    LANE_ID,
    NOW,
    OFFLINE_THREE_LANE_IDS,
    completed_result,
    launcher_receipt_sidecars_for_document,
    offline_three_repository_completed_result,
    offline_three_repository_prelaunch_plan,
    prelaunch_plan,
    result_fallback,
)
from test_check_pool_plan import broker_sidecars_for_completed_document


def validate_result(result: object, now: object = None) -> list[str]:
    return validate_result_offline_synthetic_fixture(
        result,
        now,
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


class ResultAssertions(unittest.TestCase):
    def assert_error(self, result: dict[str, object], fragment: str) -> list[str]:
        errors = validate_result_production(
            result,
            NOW,
            launcher_receipts=launcher_receipt_sidecars_for_document(result),
        )
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )
        return errors


class LaunchEligibilityTests(unittest.TestCase):
    def test_current_broker_terminal_chain_validates_completed_result(self) -> None:
        result = completed_result()
        sidecars, context = broker_sidecars_for_completed_document(result)
        self.assertEqual(
            validate_result_production(
                result,
                NOW,
                launcher_receipts=sidecars,
                production_verification_context=context,
            ),
            [],
        )

    def test_exact_launcher_receipt_sidecar_is_mandatory(self) -> None:
        result = completed_result()
        errors = validate_result_offline_synthetic_fixture(result, NOW)
        self.assertTrue(
            any("exact launcher receipt sidecar is required" in error for error in errors),
            errors,
        )

    def test_test_result_cannot_be_relabelled_production_while_retaining_test_receipt(self) -> None:
        result = completed_result()
        sidecars = launcher_receipt_sidecars_for_document(result)
        readback = result["lanes"][0]["launch_readback"]
        readback["launch_backend"] = "subprocess_popen"
        readback["production_eligible"] = True
        errors = validate_result_offline_synthetic_fixture(
            result,
            NOW,
            launcher_receipts=sidecars,
        )
        self.assertTrue(
            any("launch_backend: must be derived from exact launcher receipt" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("production_eligible: must be derived from exact launcher receipt" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("subprocess_popen requires production_eligible false" in error for error in errors),
            errors,
        )

    def test_completed_synthetic_result_requires_explicit_offline_fixture_api(self) -> None:
        result = completed_result()
        errors = validate_result_production(
            result,
            NOW,
            launcher_receipts=launcher_receipt_sidecars_for_document(result),
        )
        self.assertTrue(
            any("production validation requires windows_isolation_broker" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("production sidecars require a broker launch receipt" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("production validation requires true" in error for error in errors),
            errors,
        )
        self.assertEqual(
            validate_result_offline_synthetic_fixture(
                result,
                NOW,
                launcher_receipts=launcher_receipt_sidecars_for_document(result),
            ),
            [],
        )

    def test_launch_readback_backend_fields_are_required(self) -> None:
        result = completed_result()
        del result["lanes"][0]["launch_readback"]["launch_backend"]
        errors = validate_result_offline_synthetic_fixture(
            result,
            NOW,
            launcher_receipts=launcher_receipt_sidecars_for_document(result),
        )
        self.assertTrue(any("launch_backend" in error for error in errors), errors)


class ValidResultAndBindingTests(ResultAssertions):
    def test_every_poolable_role_has_a_valid_typed_result(self) -> None:
        for role in ("Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"):
            with self.subTest(role=role):
                self.assertEqual(validate_result(completed_result(role), NOW), [])

    def test_every_role_result_binds_to_its_exact_prelaunch_plan(self) -> None:
        for role in ("Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"):
            with self.subTest(role=role):
                self.assertEqual(
                    validate_result_against_plan(
                        prelaunch_plan(role), completed_result(role), NOW
                    ),
                    [],
                )

    def test_result_binding_rejects_plan_wave_role_lane_claim_and_digest_drift(self) -> None:
        cases = [
            (lambda r: r.update({"plan_digest": "0" * 64}), "plan_digest"),
            (lambda r: r.update({"wave_id": "codex-b-wrong-wave"}), "wave_id"),
            (lambda r: r.update({"role": "Codex E"}), "role"),
            (
                lambda r: r["lanes"][0].update(
                    {"claim_id": "33333333-3333-4333-8333-333333333333"}
                ),
                "claim_id",
            ),
            (lambda r: r.update({"expected_lane_ids": ["tahjali11/mythic-edge#999"]}), "expected_lane_ids"),
        ]
        for mutate, fragment in cases:
            result = completed_result()
            mutate(result)
            errors = validate_result_against_plan(prelaunch_plan(), result, NOW)
            with self.subTest(fragment=fragment):
                self.assertTrue(any(fragment in error for error in errors), errors)

    def test_claim_and_reservation_journal_receipts_bind_to_prelaunch_receipts(self) -> None:
        result = completed_result()
        claim_event = next(
            event
            for event in result["events"]
            if event["operation"] == "claim" and event["stage"] == "succeeded"
        )
        claim_event["receipt_ref"] = "github:claim-comment/wrong"
        errors = validate_result_against_plan(prelaunch_plan(), result, NOW)
        self.assertTrue(any("claim journal receipt must match" in error for error in errors))

    def test_offline_three_lane_result_validates_and_binds_to_one_wave_claim(self) -> None:
        result = offline_three_repository_completed_result()
        self.assertEqual(validate_result(result, NOW), [])
        self.assertEqual(
            validate_result_against_plan(
                offline_three_repository_prelaunch_plan(), result, NOW
            ),
            [],
        )
        self.assertEqual(set(result["expected_lane_ids"]), set(OFFLINE_THREE_LANE_IDS))
        self.assertEqual(len(result["fallback"]["old_workflow_routes"]), 3)
        claim_receipts = {
            event["receipt_ref"]
            for event in result["events"]
            if event["operation"] == "claim" and event["stage"] == "succeeded"
        }
        self.assertEqual(claim_receipts, {"github:claim-comment/offline-three"})
        prohibited = {"git_commit", "git_push", "draft_pr_write", "merge_pr"}
        self.assertTrue(
            prohibited.isdisjoint({event["operation"] for event in result["events"]})
        )

    def test_shared_claim_receipt_exception_does_not_cover_lane_specific_operations(self) -> None:
        result = offline_three_repository_completed_result()
        reserve_events = [
            event
            for event in result["events"]
            if event["operation"] == "reserve" and event["stage"] == "succeeded"
        ]
        reserve_events[1]["receipt_ref"] = reserve_events[0]["receipt_ref"]
        self.assert_error(result, "cannot evidence multiple logical side effects")

        result = offline_three_repository_completed_result()
        launch_event = next(
            event
            for event in result["events"]
            if event["lane_id"] == OFFLINE_THREE_LANE_IDS[1]
            and event["operation"] == "launch"
            and event["stage"] == "succeeded"
        )
        launch_event["receipt_ref"] = "github:claim-comment/offline-three"
        self.assert_error(result, "cannot evidence multiple logical side effects")


class StrictResultContractTests(ResultAssertions):
    def test_unknown_fields_are_rejected_at_every_result_level(self) -> None:
        mutators = [
            lambda r: r.update({"surprise": True}),
            lambda r: r["lanes"][0].update({"surprise": True}),
            lambda r: r["lanes"][0]["role_result"].update({"surprise": True}),
            lambda r: r["lanes"][0]["handoff"].update({"surprise": True}),
            lambda r: r["lanes"][0]["release"].update({"surprise": True}),
            lambda r: r["events"][0].update({"surprise": True}),
            lambda r: r["fallback"].update({"surprise": True}),
            lambda r: r["fallback"]["old_workflow_routes"][0].update({"surprise": True}),
        ]
        for index, mutate in enumerate(mutators):
            result = completed_result()
            mutate(result)
            with self.subTest(index=index):
                self.assert_error(result, "unknown fields: surprise")

    def test_each_role_specific_result_rejects_an_omitted_required_field(self) -> None:
        for role in ("Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"):
            result = completed_result(role)
            role_result = result["lanes"][0]["role_result"]
            removed = next(iter(role_result))
            del role_result[removed]
            with self.subTest(role=role, removed=removed):
                self.assert_error(result, "missing fields")

    def test_exactly_one_result_and_fallback_route_are_required_per_lane(self) -> None:
        result = completed_result()
        result["lanes"].append(copy.deepcopy(result["lanes"][0]))
        self.assert_error(result, "duplicate lane result")
        result = completed_result()
        result["fallback"]["old_workflow_routes"] = []
        self.assert_error(result, "must cover every result lane exactly once")

    def test_handoff_repository_issue_role_and_next_role_must_match_lane(self) -> None:
        mutations = [
            ("issue", 999, "repository and issue must match lane_id"),
            ("completed_role", "Codex E", "must match result role"),
            ("next_role", "Codex G", "must match lane result"),
        ]
        for key, value, fragment in mutations:
            result = completed_result()
            result["lanes"][0]["handoff"][key] = value
            with self.subTest(key=key):
                self.assert_error(result, fragment)

    def test_result_and_handoff_digests_are_mandatory_sha256_values(self) -> None:
        result = completed_result()
        result["lanes"][0]["result_digest"] = "not-a-digest"
        result["lanes"][0]["handoff"]["digest"] = "not-a-digest"
        errors = validate_result(result, NOW)
        self.assertGreaterEqual(sum("must be a SHA-256 digest" in error for error in errors), 2)

    def test_release_claim_must_match_lane_claim(self) -> None:
        result = completed_result()
        result["lanes"][0]["release"]["claim_id"] = (
            "33333333-3333-4333-8333-333333333333"
        )
        self.assert_error(result, "must match lane claim_id")

    def test_typed_external_and_release_receipts_must_match_journal(self) -> None:
        result = completed_result()
        result["lanes"][0]["external_actions"][0]["receipt"] = "receipt:wrong"
        result["lanes"][0]["release"]["receipt_ref"] = "receipt:wrong-release"
        errors = validate_result(result, NOW)
        self.assertTrue(any("local_artifact receipt must match" in error for error in errors))
        self.assertTrue(any("release receipt must match" in error for error in errors))


class ReviewPublicationAndGTests(ResultAssertions):
    def test_incomplete_e_cannot_route_to_f_or_g(self) -> None:
        result = completed_result("Codex E")
        result["status"] = "incomplete_interrupted"
        result["lanes"][0]["launch_state"] = "interrupted"
        result["lanes"][0]["result_status"] = "incomplete_interrupted"
        result["fallback"] = result_fallback(
            triggered=True,
            reason_code="invalid_lane_result_or_handoff",
            role="Codex E",
        )
        self.assert_error(result, "interrupted/orphaned result cannot route to F or G")

    def test_e_with_open_blocker_or_nonaccepted_review_cannot_route_to_f(self) -> None:
        result = completed_result("Codex E")
        result["lanes"][0]["role_result"]["blocking_findings"] = 1
        result["lanes"][0]["role_result"]["review_verdict"] = "changes_required"
        result["lanes"][0]["handoff"]["findings"] = [
            {
                "finding_id": "HIGH-1",
                "severity": "high",
                "blocking": True,
                "status": "open",
            }
        ]
        errors = validate_result(result, NOW)
        self.assertTrue(any("open blocking findings" in error for error in errors))
        self.assertTrue(any("accepted review with zero blockers" in error for error in errors))

    def test_f_requires_exact_reviewed_files_staged_files_commit_push_and_draft_pr(self) -> None:
        mutations = [
            (lambda r: r["lanes"][0]["role_result"].update({"staged_files": ["other.py"]}), "must exactly match reviewed_files"),
            (lambda r: r["lanes"][0]["role_result"].update({"pushed_head": HEAD}), "must equal commit_sha"),
            (lambda r: r["lanes"][0]["external_actions"].pop(), "requires exactly commit, push, and draft PR receipts"),
        ]
        for mutate, fragment in mutations:
            result = completed_result("Codex F")
            mutate(result)
            with self.subTest(fragment=fragment):
                self.assert_error(result, fragment)

    def test_f_reviewed_head_files_and_base_are_bound_to_prelaunch_evidence(self) -> None:
        result = completed_result("Codex F")
        result["lanes"][0]["role_result"]["approved_base"] = "wrong-base"
        errors = validate_result_against_plan(prelaunch_plan("Codex F"), result, NOW)
        self.assertTrue(any("approved_base drifted" in error for error in errors), errors)

    def test_pooled_g_result_is_readiness_only_and_contains_no_mutation(self) -> None:
        result = completed_result("Codex G")
        result["lanes"][0]["role_result"]["no_integration_mutation"] = False
        result["lanes"][0]["external_actions"] = [
            {"action": "merge_pr", "target": "github:pr/101", "receipt": "github:merge/101"}
        ]
        errors = validate_result(result, NOW)
        self.assertTrue(any("no_integration_mutation: must be true" in error for error in errors))
        self.assertTrue(any("no integration action" in error for error in errors))
        self.assertTrue(any("integration actions must be empty" in error for error in errors))

    def test_g_head_base_and_no_mutation_are_bound_to_prelaunch_plan(self) -> None:
        result = completed_result("Codex G")
        result["lanes"][0]["role_result"]["current_head"] = "0" * 40
        errors = validate_result_against_plan(prelaunch_plan("Codex G"), result, NOW)
        self.assertTrue(any("G head drifted" in error for error in errors), errors)


class JournalRecoveryAndFallbackTests(ResultAssertions):
    def _event(self, result: dict[str, object], operation: str, stage: str) -> dict[str, object]:
        return next(
            event
            for event in result["events"]
            if event["operation"] == operation and event["stage"] == stage
        )

    def test_completed_result_requires_full_intent_and_receipt_journal(self) -> None:
        result = completed_result()
        result["events"] = []
        self.assert_error(result, "complete side-effect journal")

    def test_outcome_must_follow_intent_and_every_intent_requires_outcome(self) -> None:
        result = completed_result()
        result["events"].remove(self._event(result, "launch", "intent"))
        self.assert_error(result, "outcome must follow its recorded intent")
        result = completed_result()
        result["events"].remove(self._event(result, "launch", "succeeded"))
        self.assert_error(result, "every intent requires an explicit")

    def test_successful_side_effect_cannot_be_retried_or_receive_two_successes(self) -> None:
        result = completed_result()
        retry = copy.deepcopy(self._event(result, "launch", "intent"))
        retry["event_id"] = "99999999-9999-4999-8999-999999999999"
        retry["attempt"] = 2
        result["events"].append(retry)
        self.assert_error(result, "successful side effect cannot be retried")
        result = completed_result()
        duplicate = copy.deepcopy(self._event(result, "launch", "succeeded"))
        duplicate["event_id"] = "88888888-8888-4888-8888-888888888888"
        duplicate["attempt"] = 2
        result["events"].append(duplicate)
        self.assert_error(result, "logical side effect has multiple success receipts")

    def test_unknown_launch_outcome_is_valid_only_as_reconciliation_with_fallback(self) -> None:
        result = completed_result()
        unknown = self._event(result, "launch", "succeeded")
        unknown["stage"] = "unknown"
        unknown["receipt_ref"] = None
        # Once launch is unknown, no later success can be trusted. Preserve the
        # claim and route the lane to human reconciliation without pretending
        # that a result, handoff, release, or retry occurred.
        result["events"] = result["events"][:6]
        result["status"] = "reconciliation_required"
        lane = result["lanes"][0]
        lane["launch_state"] = "unknown"
        lane["result_status"] = "reconciliation_required"
        lane["next_role"] = None
        lane["result_ref"] = None
        lane["result_digest"] = None
        lane["role_result"] = None
        lane["role_result_digest"] = None
        lane["handoff"] = None
        lane["launch_readback"] = None
        lane["external_actions"] = []
        lane["release"]["status"] = "routing_failed_reconciliation_required"
        lane["release"]["receipt_ref"] = None
        result["fallback"] = result_fallback(
            triggered=True,
            reason_code="partial_transition_without_proven_idempotent_recovery",
        )
        self.assertEqual(validate_result(result, NOW), [])
        result["status"] = "completed"
        result["fallback"] = result_fallback()
        self.assert_error(result, "completed wave cannot contain an unknown")

    def test_every_exact_fallback_condition_is_implemented(self) -> None:
        self.assertEqual(len(FALLBACK_CONDITION_IDS), 19)
        for condition_id in FALLBACK_CONDITION_IDS:
            with self.subTest(condition_id=condition_id):
                self.assertTrue(evaluate_fallback(condition_id))

    def test_poll_timeout_alone_is_not_a_fallback_condition(self) -> None:
        self.assertFalse(evaluate_fallback("poll_timeout"))

    def test_fallback_policy_stops_launch_and_f_g_but_preserves_running_work(self) -> None:
        result = completed_result()
        fallback = result["fallback"]
        expected = {
            "stop_new_launches": True,
            "allow_f_or_g_actions": False,
            "preserve_running_lanes": True,
            "interrupt_only_for_proven_safety_violation": True,
            "mark_affected_lanes_reconciliation_required": True,
            "release_only_verified_owned_claims": True,
            "route_each_lane_to_old_workflow": True,
            "polling_timeout_alone_triggers_fallback": False,
            "automatic_retry": False,
        }
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertIs(fallback[key], value)

    def test_noncomplete_result_requires_stable_fallback_reason(self) -> None:
        result = completed_result()
        result["status"] = "reconciliation_required"
        self.assert_error(result, "non-complete result requires a stable fallback reason")

    def test_partial_g_action_always_falls_back_and_never_retries_automatically(self) -> None:
        self.assertTrue(evaluate_fallback("partial_g_action"))
        fallback = result_fallback(
            triggered=True, reason_code="partial_g_action", role="Codex G"
        )
        self.assertFalse(fallback["automatic_retry"])
        self.assertTrue(fallback["human_reconciliation_required"])


if __name__ == "__main__":
    unittest.main()
