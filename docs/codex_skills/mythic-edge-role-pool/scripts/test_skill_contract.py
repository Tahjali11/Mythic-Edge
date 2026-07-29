from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

import yaml
from check_pool_plan import (
    FALLBACK_CONDITION_IDS,
    OFFLINE_SYNTHETIC_FIXTURE_VALIDATION_MODE,
)
from check_pool_plan import (
    validate_plan as validate_plan_production,
)
from check_pool_plan import (
    validate_plan_against_observations as validate_plan_against_observations_production,
)
from check_pool_plan import (
    validate_result as validate_result_production,
)
from check_pool_plan import (
    validate_result_against_plan as validate_result_against_plan_production,
)
from check_stage3_behavioral_planning import (
    build_stage3_observation,
    validate_stage3_behavioral_planning,
    validate_stage3_pair,
)
from pool_test_fixtures import (
    NOW,
    completed_result,
    discovery_for_plan,
    fallback_injection,
    inspect_plan,
    launcher_receipt_sidecars_for_document,
    offline_three_repository_completed_result,
    offline_three_repository_inspect_plan,
    offline_three_repository_preclaim_plan,
    offline_three_repository_prelaunch_plan,
    old_workflow_prompt,
    preclaim_plan,
    prelaunch_plan,
    worktrees_for_plan,
)

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_TEXT = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
SCHEMA_TEXT = (SKILL_ROOT / "references" / "pool-state-schema.md").read_text(
    encoding="utf-8"
)
SAFETY_TEXT = (SKILL_ROOT / "references" / "role-readiness-and-safety.md").read_text(
    encoding="utf-8"
)
FALLBACK_TEXT = (SKILL_ROOT / "references" / "fallback-and-recovery.md").read_text(
    encoding="utf-8"
)
MATRIX_TEXT = (SKILL_ROOT / "references" / "release-remediation-matrix.md").read_text(
    encoding="utf-8"
)
CANARY_TEXT = (
    SKILL_ROOT / "references" / "stage4-canary-exception.md"
).read_text(encoding="utf-8")
BROKER_TEXT = (
    SKILL_ROOT / "references" / "external-isolation-broker.md"
).read_text(encoding="utf-8")
STAGE3_TEXT = (
    SKILL_ROOT / "references" / "stage3-behavioral-planning.md"
).read_text(encoding="utf-8")
OLD_WORKFLOW_ROOT = SKILL_ROOT.parent / "mythic-edge-workflow"
if not OLD_WORKFLOW_ROOT.is_dir():
    OLD_WORKFLOW_ROOT = (
        Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        / "skills"
        / "mythic-edge-workflow"
    )
OLD_WORKFLOW_TEXT = (OLD_WORKFLOW_ROOT / "SKILL.md").read_text(encoding="utf-8")


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


class SkillContractTests(unittest.TestCase):
    def test_metadata_disables_implicit_invocation_and_defaults_to_inspect(self) -> None:
        metadata = yaml.safe_load(
            (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        )
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], False)
        prompt = metadata["interface"]["default_prompt"].lower()
        self.assertIn("inspect", prompt)
        self.assertNotIn("dispatch", prompt)

    def test_named_dispatch_mode_is_documented_as_intent_not_authority(self) -> None:
        selector = "Mythic-Edge-Role-Pool: Dispatch"
        self.assertIn(selector, SKILL_TEXT)
        self.assertIn(selector, SCHEMA_TEXT)
        self.assertIn(selector, SAFETY_TEXT)
        self.assertIn("bare dispatch selector selects intent only", SKILL_TEXT.lower())
        self.assertIn("permits no side effect", SCHEMA_TEXT.lower())
        self.assertIn("ambiguous_request_or_side_effect", SAFETY_TEXT)

    def test_personal_default_owner_is_documented_without_weakening_canonical_ids(self) -> None:
        for text in (SKILL_TEXT, SCHEMA_TEXT):
            self.assertIn("tahjali11", text)
            self.assertIn("ownerless", text.lower())
            self.assertIn("owner/repository", text)
        self.assertIn("request parsing", " ".join(SKILL_TEXT.lower().split()))
        self.assertIn("persisted identities", SCHEMA_TEXT.lower())

    def test_compact_grammar_has_exact_scope_and_no_automatic_repo_backfill(self) -> None:
        for text in (SKILL_TEXT, SCHEMA_TEXT):
            self.assertIn("<Inspect|Dispatch>", text)
            self.assertIn("<A|B|C|D|E|F|G>", text)
            self.assertIn("one-to-three", text)
            self.assertIn("backfill", text.lower())
        self.assertIn("C` is recognized", SCHEMA_TEXT)
        self.assertIn("No separate private-read clause", SCHEMA_TEXT)
        self.assertIn(
            "No token means no repository read authority", " ".join(SAFETY_TEXT.split())
        )

    def test_personal_repository_prefix_alias_is_documented_and_bounded(self) -> None:
        for text in (SKILL_TEXT, SCHEMA_TEXT, SAFETY_TEXT):
            self.assertIn("mythic-edge-", text)
            self.assertIn("explicit", text.lower())
        for text in (SKILL_TEXT, SCHEMA_TEXT):
            self.assertIn("fable-engine", text)
        self.assertIn("tahjali11/mythic-edge-fable-engine", SKILL_TEXT)
        self.assertIn("already-prefixed", SCHEMA_TEXT)
        self.assertIn("full canonical", SKILL_TEXT)

    def test_skill_references_every_existing_runtime_document(self) -> None:
        for name in (
            "pool-state-schema.md",
            "role-readiness-and-safety.md",
            "fallback-and-recovery.md",
            "stage3-behavioral-planning.md",
            "stage4-canary-exception.md",
            "external-isolation-broker.md",
        ):
            with self.subTest(name=name):
                self.assertIn(name, SKILL_TEXT)
                self.assertTrue((SKILL_ROOT / "references" / name).is_file())

    def test_no_stale_v1_plan_schema_or_generic_g_merge_authority_remains(self) -> None:
        all_text = "\n".join((SKILL_TEXT, SCHEMA_TEXT, SAFETY_TEXT, FALLBACK_TEXT))
        self.assertNotIn("mythic_edge_role_pool_plan.v1", all_text)
        self.assertIn("readiness-only", all_text.lower())
        self.assertIn("separate one-issue", all_text.lower())

    def test_runtime_contract_has_no_bare_gpt_56_reference(self) -> None:
        offenders = []
        pattern = re.compile(r"gpt-5\.6(?!-sol)")
        for path in SKILL_ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {
                ".md",
                ".py",
                ".yaml",
                ".yml",
                ".json",
            }:
                continue
            if pattern.search(path.read_text(encoding="utf-8")):
                offenders.append(str(path.relative_to(SKILL_ROOT)))
        self.assertEqual(offenders, [])

    def test_single_start_launcher_is_frozen_and_documented(self) -> None:
        launcher = SKILL_ROOT / "scripts" / "codex_launcher_contract.py"
        launcher_tests = SKILL_ROOT / "scripts" / "test_codex_launcher_contract.py"
        self.assertTrue(launcher.is_file())
        self.assertTrue(launcher_tests.is_file())
        for text in (SKILL_TEXT, SCHEMA_TEXT, SAFETY_TEXT, MATRIX_TEXT):
            self.assertIn("codex:exec-single-start/v2", text)
        for text in (SKILL_TEXT, SCHEMA_TEXT, SAFETY_TEXT, BROKER_TEXT):
            self.assertIn("codex:broker-single-start/v1", text)
        self.assertIn("gpt-5.6-sol", launcher.read_text(encoding="utf-8"))
        self.assertIn("build_child_environment", SKILL_TEXT)
        self.assertIn("mythic_edge_role_pool_plan.v3", SCHEMA_TEXT)
        self.assertIn("mythic_edge_role_pool_result.v3", SCHEMA_TEXT)

    def test_broker_owned_isolation_and_direct_popen_ineligibility_are_documented(self) -> None:
        combined = "\n".join(
            (SKILL_TEXT, SCHEMA_TEXT, SAFETY_TEXT, MATRIX_TEXT, CANARY_TEXT, BROKER_TEXT)
        )
        for phrase in (
            "mythic_edge_role_pool_external_isolation_broker.v1",
            "mythic_edge_role_pool_broker_launch_request.v1",
            "mythic_edge_role_pool_broker_start_reservation.v1",
            "mythic_edge_role_pool_broker_boundary_ready_receipt.v1",
            "mythic_edge_role_pool_broker_start_receipt.v1",
            "mythic_edge_role_pool_broker_terminal_receipt.v1",
            "mythic_edge_role_pool_broker_abort_receipt.v1",
            "windows_isolation_broker",
            "codex:broker-single-start/v1",
            "mythic_edge_role_pool_external_isolation.v3",
            "mythic_edge_role_pool_external_os_isolation.v2",
            "mythic_edge_role_pool_launcher_receipt_sidecars.v1",
            "direct-Popen receipt",
            "production_eligible=false",
            "verifier-constructed",
            "generic signing",
            "before reading even a length prefix",
            "non-inheritable job handle",
            "deny write and delete sharing",
            "common ancestor",
            "broker epoch",
            "verifier epoch",
            "tool subprocesses receive no network",
            "Codex service channel",
            "credential",
            "caller-profile",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), combined.lower())
        self.assertNotIn("the only production pair is\n`subprocess_popen` / `true`", combined)

    def test_contract_machine_rejects_direct_production_and_strictly_validates_broker(self) -> None:
        launcher_text = (
            SKILL_ROOT / "scripts" / "codex_launcher_contract.py"
        ).read_text(encoding="utf-8")
        plan_validator_text = (
            SKILL_ROOT / "scripts" / "check_pool_plan.py"
        ).read_text(encoding="utf-8")
        self.assertIn('DIRECT_POPEN_LAUNCH_BACKEND = "subprocess_popen"', launcher_text)
        self.assertIn('PRODUCTION_LAUNCH_BACKEND = "windows_isolation_broker"', launcher_text)
        self.assertIn('DIRECT_LAUNCH_BACKEND = "subprocess_popen"', plan_validator_text)
        self.assertIn('PRODUCTION_LAUNCH_BACKEND = "windows_isolation_broker"', plan_validator_text)
        self.assertIn("direct Popen launcher is retired", launcher_text)
        self.assertIn("broker receipt-chain validation is not implemented", launcher_text)
        self.assertIn("validate_broker_receipt_chain", launcher_text)
        self.assertIn("validate_broker_receipt_chain", plan_validator_text)
        self.assertIn("BROKER_RECEIPT_CHAIN_ATTESTATION_ALGORITHM", plan_validator_text)
        self.assertIn("ProductionVerificationContext(<unprovisioned>)", launcher_text)
        self.assertIn("public direct launcher", BROKER_TEXT)
        self.assertIn("current validators reject", SCHEMA_TEXT.lower())
        self.assertIn("all live launch and Stage-4 execution remains blocked", BROKER_TEXT)

    def test_offline_guard_is_documented_as_trusted_code_regression_only(self) -> None:
        combined = "\n".join(
            (
                SKILL_TEXT,
                SCHEMA_TEXT,
                SAFETY_TEXT,
                FALLBACK_TEXT,
                MATRIX_TEXT,
                CANARY_TEXT,
                BROKER_TEXT,
            )
        ).lower()
        for phrase in (
            "trusted-code regression guard",
            "not a security or isolation boundary",
            "external os-enforced read-only/no-network",
            "untrusted executable or script",
            "not live-ready",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

    def test_documented_fallback_ids_exactly_match_implementation(self) -> None:
        section = FALLBACK_TEXT.split("## Exact Fallback Conditions", 1)[1].split(
            "## Staged Canary", 1
        )[0]
        documented = set(
            re.findall(r"^\d+\. `([a-z0-9_]+)`", section, flags=re.MULTILINE)
        )
        self.assertEqual(documented, FALLBACK_CONDITION_IDS)
        self.assertEqual(len(documented), 19)

    def test_all_exact_packet_entries_have_release_traceability(self) -> None:
        expected = [
            ("MEPOOL-RC-001", "confirmed"),
            ("MEPOOL-RC-002", "confirmed"),
            ("MEPOOL-RC-003", "confirmed"),
            ("MEPOOL-RC-004", "confirmed"),
            ("MEPOOL-RC-005", "confirmed"),
            ("MEPOOL-RC-006", "confirmed"),
            ("MEPOOL-RC-007", "confirmed"),
            ("MEPOOL-RC-008", "duplicate"),
            ("MEPOOL-RC-009", "confirmed"),
            ("ME-RC-01", "confirmed"),
            ("ME-RC-02", "confirmed"),
            ("ME-RC-03", "duplicate"),
            ("ME-RC-04", "confirmed"),
            ("ME-RC-05", "duplicate"),
            ("ME-RC-06", "duplicate"),
            ("ME-RC-07", "confirmed"),
            ("ME-RC-08", "confirmed"),
            ("ME-RC-09", "confirmed"),
            ("ME-RC-10", "confirmed"),
            ("ME-RC-11", "confirmed"),
            ("ME-RC-12", "accepted risk"),
            ("MRP-RC-001", "accepted risk"),
            ("MRP-RC-002", "confirmed"),
            ("MRP-RC-003", "requires behavioral experiment"),
            ("MRP-RC-004", "confirmed"),
            ("MRP-RC-005", "duplicate"),
            ("MRP-RC-006", "duplicate"),
            ("MRP-RC-007", "duplicate"),
            ("MRP-RC-008", "confirmed"),
            ("MRP-RC-009", "duplicate"),
        ]
        observed = re.findall(
            r"^\| ((?:MEPOOL-RC-|ME-RC-|MRP-RC-)[0-9]+) \| "
            r"(confirmed|duplicate|unsupported|accepted risk|requires behavioral experiment) \|",
            MATRIX_TEXT,
            flags=re.MULTILINE,
        )
        self.assertEqual(observed, expected)
        counts = {classification: 0 for _, classification in expected}
        for _, classification in observed:
            counts[classification] += 1
        self.assertEqual(counts["confirmed"], 19)
        self.assertEqual(counts["duplicate"], 8)
        self.assertEqual(counts["accepted risk"], 2)
        self.assertEqual(counts["requires behavioral experiment"], 1)
        self.assertNotIn("| unsupported |", MATRIX_TEXT)

    def test_documentation_points_to_executable_canonical_fixtures(self) -> None:
        self.assertIn("scripts/pool_test_fixtures.py", SCHEMA_TEXT)
        self.assertIn("scripts\\run_release_tests.py", SCHEMA_TEXT)
        for plan in (inspect_plan(), preclaim_plan(), prelaunch_plan()):
            self.assertEqual(validate_plan(plan, NOW), [])
        for role in ("Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"):
            self.assertEqual(validate_result(completed_result(role), NOW), [])

        for plan in (
            offline_three_repository_inspect_plan(),
            offline_three_repository_preclaim_plan(),
            offline_three_repository_prelaunch_plan(),
        ):
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
        triple_result = offline_three_repository_completed_result()
        self.assertEqual(validate_result(triple_result, NOW), [])
        self.assertEqual(
            validate_result_against_plan(
                offline_three_repository_prelaunch_plan(), triple_result, NOW
            ),
            [],
        )
        self.assertIn("three-repository", SCHEMA_TEXT)
        self.assertIn("three-lane", SCHEMA_TEXT)

    def test_documentation_matches_the_release_enforcement_surface(self) -> None:
        all_text = "\n".join((SKILL_TEXT, SCHEMA_TEXT, SAFETY_TEXT))
        for phrase in (
            "authorize repository=owner/repository",
            "no separate private-read clause",
            "named public or private",
            "per-lane launch readback",
            "no_integration_mutation",
            "check waivers are not accepted",
            "changes-required E",
            "--outcome",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), all_text.lower())
        self.assertNotIn("authorize private read repository=", all_text.lower())
        self.assertNotIn("`no_mutation: true`", all_text)
        self.assertIn("## Requirement-To-Enforcement Matrix", MATRIX_TEXT)
        self.assertIn("## Missing Deterministic Tests", MATRIX_TEXT)
        self.assertIn("## Readiness Gates", MATRIX_TEXT)

    def test_exact_result_validation_command_binds_prelaunch_plan(self) -> None:
        self.assertIn("--plan <exact-prelaunch-plan.json>", SKILL_TEXT)
        self.assertIn("--plan <prelaunch-plan.json>", SCHEMA_TEXT)

    def test_fallback_actions_polling_exception_and_canary_are_documented(self) -> None:
        for phrase in (
            "stop selecting, claiming, reserving, and launching",
            "perform no new F or G action",
            "preserve healthy confirmed-running lanes",
            "release only claims proven to belong to this coordinator",
            "one old-workflow route per lane",
            "polling timeout alone does not trigger fallback",
            "Malicious-content experiment",
            "twice consecutively",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), FALLBACK_TEXT.lower())

    def test_stage4_canary_exception_is_standalone_and_fail_closed(self) -> None:
        checker = SKILL_ROOT / "scripts" / "check_stage4_canary_exception.py"
        focused_test = SKILL_ROOT / "scripts" / "test_stage4_canary_exception.py"
        self.assertTrue(checker.is_file())
        self.assertTrue(focused_test.is_file())
        combined = "\n".join(
            (SKILL_TEXT, FALLBACK_TEXT, SAFETY_TEXT, CANARY_TEXT, BROKER_TEXT)
        )
        for phrase in (
            "mythic_edge_role_pool_stage4_canary_exception.v1",
            "MRP-RC-003",
            "one fresh isolated canary agent",
            "normal pooled dispatch",
            "claim",
            "reservation",
            "repository write",
            "credential",
            "external mutation",
            "stage advancement",
            "finding resolution",
            "deny repository=",
            "mutation_scope=none",
            "broker-single-start/v1",
            "boundary-ready",
            "terminal receipt",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), combined.lower())
        self.assertIn("cannot appear in a v3 plan", FALLBACK_TEXT)
        self.assertIn("does not advance a stage", FALLBACK_TEXT)
        self.assertIn("check_stage4_canary_exception.py", MATRIX_TEXT)

    def test_stage3_behavioral_planning_contract_is_separate_and_zero_effect(self) -> None:
        checker = SKILL_ROOT / "scripts" / "check_stage3_behavioral_planning.py"
        focused_test = SKILL_ROOT / "scripts" / "test_stage3_behavioral_planning.py"
        self.assertTrue(checker.is_file())
        self.assertTrue(focused_test.is_file())
        combined = "\n".join((SKILL_TEXT, SCHEMA_TEXT, FALLBACK_TEXT, STAGE3_TEXT))
        for phrase in (
            "mythic_edge_role_pool_stage3_behavioral_planning.v1",
            "accepted Stage-2 pair",
            "three-repository/three-lane",
            "same-role",
            "fail-closed",
            "zero",
            "independent review",
            "agent behavior",
            "Stage 4",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), combined.lower())

        first = build_stage3_observation(
            "66666666-6666-4666-8666-666666666661",
            "77777777-7777-4777-8777-777777777777",
            "1_of_2",
            1,
            "2026-07-15T12:00:00Z",
        )
        second = build_stage3_observation(
            "66666666-6666-4666-8666-666666666662",
            "77777777-7777-4777-8777-777777777777",
            "2_of_2",
            2,
            "2026-07-15T12:01:00Z",
        )
        self.assertEqual(validate_stage3_behavioral_planning(first), [])
        self.assertEqual(validate_stage3_behavioral_planning(second), [])
        self.assertEqual(validate_stage3_pair(first, second), [])
        self.assertTrue(validate_plan_production(first))
        self.assertIs(first["stage_advancement_claimed"], False)
        self.assertIs(first["finding_resolution_claimed"], False)
        self.assertEqual(first["independent_review"]["status"], "pending")
        self.assertIn("check_stage3_behavioral_planning.py", MATRIX_TEXT)

    def test_independent_fallback_pickup_contract_is_executable_and_documented(self) -> None:
        producer = OLD_WORKFLOW_ROOT / "scripts" / "accept_fallback_prompt.py"
        checker = SKILL_ROOT / "scripts" / "check_fallback_pickup.py"
        regenerator = SKILL_ROOT / "scripts" / "regenerate_fallback_pickup_fixture.py"
        focused_test = SKILL_ROOT / "scripts" / "test_fallback_pickup.py"
        self.assertTrue(producer.is_file())
        self.assertTrue(checker.is_file())
        self.assertTrue(regenerator.is_file())
        self.assertTrue(focused_test.is_file())
        for schema in (
            "mythic_edge_old_workflow_prompt.v1",
            "mythic_edge_role_pool_fallback_injection.v1",
            "mythic_edge_old_workflow_pickup.v1",
        ):
            with self.subTest(schema=schema):
                self.assertIn(schema, SKILL_TEXT + FALLBACK_TEXT + SCHEMA_TEXT)
        self.assertIn("accepted_no_launch", OLD_WORKFLOW_TEXT)
        self.assertIn("scripts\\accept_fallback_prompt.py", OLD_WORKFLOW_TEXT)
        self.assertIn("scripts\\check_fallback_pickup.py", SKILL_TEXT)
        self.assertIn("regenerate_fallback_pickup_fixture.py", SCHEMA_TEXT)
        self.assertIn(
            "pickup: required after successful fallback injection",
            SKILL_TEXT + FALLBACK_TEXT + SCHEMA_TEXT,
        )
        prompt = old_workflow_prompt()
        injection = fallback_injection(prompt)
        self.assertEqual(injection["prompt_sha256"], prompt["digest"])
        self.assertIs(injection["task_created"], False)
        self.assertIs(injection["agent_launched"], False)
        self.assertIs(injection["mutation_performed"], False)

    def test_post_remediation_runner_is_present_and_documented(self) -> None:
        self.assertTrue((SKILL_ROOT / "scripts" / "run_release_tests.py").is_file())
        self.assertIn("py -B scripts\\run_release_tests.py", SKILL_TEXT)

    def test_trusted_owner_native_profile_is_windows_first_and_inert(self) -> None:
        combined = SKILL_TEXT + SCHEMA_TEXT + SAFETY_TEXT
        for marker in (
            "trusted_owner_native",
            "codex:native-task-create/v1",
            "trusted_owner_native_profile_ready",
            "trusted_owner_repository_registry.v1.json",
            "trusted_owner_native_release_state.v1.jsonl",
            "synthetic",
            "NOT LIVE-READY",
            "os.name == \"nt\"",
            "sys.platform == \"win32\"",
            "Windows-hosted execution",
            "native Mac dispatch is deferred",
            "blocked_request_or_packet_invalid",
            "no weaker fallback",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, combined)
        self.assertIn("--check --skill", SKILL_TEXT)
        self.assertIn("platform-neutral and read-only", SKILL_TEXT)
        self.assertIn("Windows-only mutation gate", SKILL_TEXT)


if __name__ == "__main__":
    unittest.main()
