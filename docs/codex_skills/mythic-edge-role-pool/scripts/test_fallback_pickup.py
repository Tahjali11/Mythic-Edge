from __future__ import annotations

import copy
import hashlib
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path

from check_fallback_pickup import validate_fallback_pickup_bundle, with_digest
from check_pool_plan import FALLBACK_CONDITION_IDS
from pool_test_fixtures import (
    NOW,
    NOW_TEXT,
    FALLBACK_SOURCE_ARTIFACT,
    OLD_WORKFLOW_INGRESS,
    OLD_WORKFLOW_SKILL,
    fallback_injection,
    old_workflow_prompt,
)


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER = SKILL_ROOT / "scripts" / "check_fallback_pickup.py"
STATIC_FIXTURE = SKILL_ROOT / "references" / "fallback-pickup-fixture"


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


class FallbackPickupReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prompt = old_workflow_prompt()
        self.injection = fallback_injection(self.prompt)

    def _producer_command(
        self,
        injection_path: Path,
        prompt_path: Path,
        output_path: Path,
        *,
        now_text: str = NOW_TEXT,
    ) -> list[str]:
        return [
            sys.executable,
            "-B",
            str(OLD_WORKFLOW_INGRESS),
            str(injection_path),
            "--prompt",
            str(prompt_path),
            "--source-artifact",
            str(FALLBACK_SOURCE_ARTIFACT),
            "--output",
            str(output_path),
            "--now",
            now_text,
        ]

    def _emit_pickup(
        self,
        directory: Path,
        *,
        prompt: dict[str, object] | None = None,
        injection: dict[str, object] | None = None,
        name: str = "pickup.json",
        now_text: str = NOW_TEXT,
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        prompt_path = directory / f"{name}.prompt.json"
        injection_path = directory / f"{name}.injection.json"
        output_path = directory / name
        _write_json(prompt_path, prompt or self.prompt)
        _write_json(injection_path, injection or self.injection)
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            self._producer_command(
                injection_path, prompt_path, output_path, now_text=now_text
            ),
            cwd=SKILL_ROOT,
            env=environment,
            check=False,
            text=True,
            capture_output=True,
            timeout=30,
        )
        return completed, output_path

    def test_successful_injection_without_pickup_fails_closed(self) -> None:
        errors = validate_fallback_pickup_bundle(
            prompt=self.prompt,
            injection=self.injection,
            pickup=None,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn(
            "pickup: required after successful fallback injection",
            errors,
        )

    def test_independent_old_workflow_ingress_emits_fully_bound_pickup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(Path(temporary))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            pickup = json.loads(pickup_path.read_text(encoding="utf-8"))

        errors = validate_fallback_pickup_bundle(
            prompt=self.prompt,
            injection=self.injection,
            pickup=pickup,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertEqual(errors, [])
        self.assertEqual(pickup["pickup_status"], "accepted_no_launch")
        self.assertIs(pickup["task_created"], False)
        self.assertIs(pickup["agent_launched"], False)
        self.assertIs(pickup["mutation_performed"], False)

    def test_static_offline_pickup_receipt_remains_independently_verifiable(self) -> None:
        prompt = json.loads((STATIC_FIXTURE / "prompt.json").read_text(encoding="utf-8"))
        injection = json.loads(
            (STATIC_FIXTURE / "injection.json").read_text(encoding="utf-8")
        )
        pickup = json.loads((STATIC_FIXTURE / "pickup.json").read_text(encoding="utf-8"))
        errors = validate_fallback_pickup_bundle(
            prompt=prompt,
            injection=injection,
            pickup=pickup,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertEqual(errors, [])
        self.assertEqual(
            pickup["digest"],
            "cb49d6251c8a89e552a4601eddb22f718e38d097930d5b9525275978b8bc658a",
        )

    def test_static_receipt_exactly_matches_old_workflow_cli_output(self) -> None:
        prompt_path = STATIC_FIXTURE / "prompt.json"
        injection_path = STATIC_FIXTURE / "injection.json"
        expected = json.loads(
            (STATIC_FIXTURE / "pickup.json").read_text(encoding="utf-8")
        )
        with tempfile.TemporaryDirectory() as temporary:
            output_path = Path(temporary) / "pickup.json"
            completed = subprocess.run(
                self._producer_command(injection_path, prompt_path, output_path),
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            observed = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(observed, expected)

    def test_checker_cli_returns_one_when_successful_injection_has_no_pickup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            prompt_path = directory / "prompt.json"
            injection_path = directory / "injection.json"
            _write_json(prompt_path, self.prompt)
            _write_json(injection_path, self.injection)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(CHECKER),
                    str(injection_path),
                    "--prompt",
                    str(prompt_path),
                    "--workflow-skill",
                    str(OLD_WORKFLOW_SKILL),
                    "--pickup-producer",
                    str(OLD_WORKFLOW_INGRESS),
                    "--source-artifact",
                    str(FALLBACK_SOURCE_ARTIFACT),
                    "--now",
                    NOW_TEXT,
                ],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
        self.assertEqual(completed.returncode, 1)
        self.assertIn(
            "pickup: required after successful fallback injection",
            completed.stdout,
        )

    def test_unknown_pickup_field_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(Path(temporary))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            pickup = json.loads(pickup_path.read_text(encoding="utf-8"))
        marker = "RAW-PRIVATE-CONTENT"
        pickup[marker] = True
        pickup = with_digest(pickup)
        errors = validate_fallback_pickup_bundle(
            prompt=self.prompt,
            injection=self.injection,
            pickup=pickup,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn("pickup: unknown fields are not permitted", errors)
        self.assertNotIn(marker, "\n".join(errors))

    def test_pickup_injection_digest_drift_is_rejected_after_rehash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(Path(temporary))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            pickup = json.loads(pickup_path.read_text(encoding="utf-8"))
        pickup["injection_sha256"] = "0" * 64
        pickup = with_digest(pickup)
        errors = validate_fallback_pickup_bundle(
            prompt=self.prompt,
            injection=self.injection,
            pickup=pickup,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn(
            "binding.injection_sha256: pickup must equal injection.digest",
            errors,
        )

    def test_pickup_cannot_claim_a_task_launch_or_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(Path(temporary))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            base_pickup = json.loads(pickup_path.read_text(encoding="utf-8"))
        for field in ("task_created", "agent_launched", "mutation_performed"):
            with self.subTest(field=field):
                pickup = copy.deepcopy(base_pickup)
                pickup[field] = True
                pickup = with_digest(pickup)
                errors = validate_fallback_pickup_bundle(
                    prompt=self.prompt,
                    injection=self.injection,
                    pickup=pickup,
                    workflow_skill=OLD_WORKFLOW_SKILL,
                    pickup_producer=OLD_WORKFLOW_INGRESS,
                    source_artifact=FALLBACK_SOURCE_ARTIFACT,
                    now=NOW,
                )
                self.assertIn(f"pickup.{field}: must equal False", errors)

    def test_old_workflow_rejects_prompt_binding_drift_before_emitting_pickup(self) -> None:
        injection = copy.deepcopy(self.injection)
        injection["prompt_sha256"] = "0" * 64
        injection = with_digest(injection)
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(
                Path(temporary), injection=injection
            )
            self.assertEqual(completed.returncode, 1)
            self.assertFalse(pickup_path.exists())
        self.assertIn(
            "binding.prompt_sha256: must equal prompt.digest",
            completed.stderr,
        )

    def test_pickup_binds_current_old_workflow_contract_and_ingress_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(Path(temporary))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            pickup = json.loads(pickup_path.read_text(encoding="utf-8"))
        expected_contract = hashlib.sha256(OLD_WORKFLOW_SKILL.read_bytes()).hexdigest()
        expected_ingress = hashlib.sha256(OLD_WORKFLOW_INGRESS.read_bytes()).hexdigest()
        self.assertEqual(pickup["consumer_contract_sha256"], expected_contract)
        self.assertEqual(pickup["consumer_ingress_sha256"], expected_ingress)

    def test_same_injection_and_timestamp_produce_same_canonical_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            first, first_path = self._emit_pickup(directory, name="first.json")
            second, second_path = self._emit_pickup(directory, name="second.json")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            first_receipt = json.loads(first_path.read_text(encoding="utf-8"))
            second_receipt = json.loads(second_path.read_text(encoding="utf-8"))
        self.assertEqual(first_receipt, second_receipt)

    def test_distinct_pickup_times_have_distinct_receipt_identities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            first, first_path = self._emit_pickup(
                directory, name="first.json", now_text="2026-07-13T11:59:00Z"
            )
            second, second_path = self._emit_pickup(
                directory, name="second.json", now_text="2026-07-13T12:00:00Z"
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            first_receipt = json.loads(first_path.read_text(encoding="utf-8"))
            second_receipt = json.loads(second_path.read_text(encoding="utf-8"))
        self.assertNotEqual(first_receipt["pickup_id"], second_receipt["pickup_id"])
        self.assertNotEqual(first_receipt["receipt_ref"], second_receipt["receipt_ref"])

    def test_surrounding_whitespace_in_route_identity_fails_closed(self) -> None:
        prompt = copy.deepcopy(self.prompt)
        prompt["route_id"] = f" {prompt['route_id']} "
        prompt = with_digest(prompt)
        injection = copy.deepcopy(self.injection)
        injection["route_id"] = prompt["route_id"]
        injection["prompt_sha256"] = prompt["digest"]
        injection = with_digest(injection)
        errors = validate_fallback_pickup_bundle(
            prompt=prompt,
            injection=injection,
            pickup=None,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn("prompt.route_id: surrounding whitespace is not permitted", errors)
        self.assertIn("injection.route_id: surrounding whitespace is not permitted", errors)

    def test_noncanonical_pickup_timestamp_fails_after_rehash_and_id_rebinding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(Path(temporary))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            pickup = json.loads(pickup_path.read_text(encoding="utf-8"))
        pickup["picked_up_at"] = " 2026-07-13T12:00:00Z "
        pickup["pickup_id"] = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                "mythic-edge-old-workflow-pickup:"
                f"{self.injection['digest']}:{pickup['picked_up_at']}",
            )
        )
        pickup["receipt_ref"] = f"receipt:old-workflow-pickup/{pickup['pickup_id']}"
        pickup = with_digest(pickup)
        errors = validate_fallback_pickup_bundle(
            prompt=self.prompt,
            injection=self.injection,
            pickup=pickup,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn(
            "pickup.picked_up_at: must use canonical UTC whole-second Z format",
            errors,
        )

    def test_reference_fields_reject_embedded_private_content_without_echo(self) -> None:
        marker = "RAW-PRIVATE-CONTENT"
        prompt = copy.deepcopy(self.prompt)
        prompt["prompt_ref"] = f"{prompt['prompt_ref']}\n{marker}"
        prompt = with_digest(prompt)
        injection = copy.deepcopy(self.injection)
        injection["prompt_ref"] = prompt["prompt_ref"]
        injection["prompt_sha256"] = prompt["digest"]
        injection = with_digest(injection)
        errors = validate_fallback_pickup_bundle(
            prompt=prompt,
            injection=injection,
            pickup=None,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn("prompt.prompt_ref: must be a canonical typed reference", errors)
        self.assertIn("injection.prompt_ref: must be a canonical typed reference", errors)
        self.assertNotIn(marker, "\n".join(errors))
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(
                Path(temporary), prompt=prompt, injection=injection
            )
            self.assertEqual(completed.returncode, 1)
            self.assertFalse(pickup_path.exists())
        self.assertNotIn(marker, completed.stderr)

    def test_duplicate_json_keys_are_rejected_by_both_clis(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            prompt_path = directory / "prompt.json"
            injection_path = directory / "injection.json"
            pickup_path = directory / "pickup.json"
            _write_json(prompt_path, self.prompt)
            rendered = json.dumps(self.injection, sort_keys=True)
            needle = '"mutation_performed": false'
            self.assertIn(needle, rendered)
            injection_path.write_text(
                rendered.replace(
                    needle,
                    f'{needle}, "mutation_performed": false',
                    1,
                ),
                encoding="utf-8",
            )
            producer = subprocess.run(
                self._producer_command(injection_path, prompt_path, pickup_path),
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            checker = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(CHECKER),
                    str(injection_path),
                    "--prompt",
                    str(prompt_path),
                    "--workflow-skill",
                    str(OLD_WORKFLOW_SKILL),
                    "--pickup-producer",
                    str(OLD_WORKFLOW_INGRESS),
                    "--source-artifact",
                    str(FALLBACK_SOURCE_ARTIFACT),
                    "--now",
                    NOW_TEXT,
                ],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
        self.assertEqual(producer.returncode, 2)
        self.assertEqual(checker.returncode, 2)
        self.assertIn("input is unreadable, malformed, or ambiguous", producer.stderr)
        self.assertIn("input is unreadable, malformed, or ambiguous", checker.stderr)

    def test_unreadable_verification_file_returns_cli_exit_two_without_echo(self) -> None:
        marker = "RAW-PRIVATE-CONTENT"
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            prompt_path = directory / "prompt.json"
            injection_path = directory / "injection.json"
            pickup_path = directory / "pickup.json"
            missing_source = directory / marker
            _write_json(prompt_path, self.prompt)
            _write_json(injection_path, self.injection)
            producer_command = self._producer_command(
                injection_path, prompt_path, pickup_path
            )
            source_index = producer_command.index("--source-artifact") + 1
            producer_command[source_index] = str(missing_source)
            producer = subprocess.run(
                producer_command,
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            checker = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(CHECKER),
                    str(injection_path),
                    "--prompt",
                    str(prompt_path),
                    "--workflow-skill",
                    str(OLD_WORKFLOW_SKILL),
                    "--pickup-producer",
                    str(OLD_WORKFLOW_INGRESS),
                    "--source-artifact",
                    str(missing_source),
                    "--now",
                    NOW_TEXT,
                ],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
        self.assertEqual(producer.returncode, 2)
        self.assertEqual(checker.returncode, 2)
        combined = producer.stderr + checker.stderr
        self.assertIn("input is unreadable, malformed, or ambiguous", combined)
        self.assertNotIn(marker, combined)

    def test_source_artifact_digest_must_be_independently_reproducible(self) -> None:
        errors = validate_fallback_pickup_bundle(
            prompt=self.prompt,
            injection=self.injection,
            pickup=None,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=OLD_WORKFLOW_SKILL,
            now=NOW,
        )
        self.assertIn(
            "binding.source_artifact_sha256: prompt does not match supplied source artifact",
            errors,
        )

    def test_source_artifact_reference_must_match_its_resolved_path(self) -> None:
        prompt = copy.deepcopy(self.prompt)
        prompt["source_artifact_ref"] = "github:issue/999"
        prompt = with_digest(prompt)
        injection = copy.deepcopy(self.injection)
        injection["prompt_sha256"] = prompt["digest"]
        injection = with_digest(injection)
        errors = validate_fallback_pickup_bundle(
            prompt=prompt,
            injection=injection,
            pickup=None,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn(
            "binding.source_artifact_ref: prompt does not identify the supplied "
            "canonical Role Pool source artifact",
            errors,
        )
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(
                Path(temporary), prompt=prompt, injection=injection
            )
            self.assertEqual(completed.returncode, 1)
            self.assertFalse(pickup_path.exists())
        self.assertIn(
            "prompt.source_artifact_ref: must identify the supplied canonical "
            "Role Pool source artifact",
            completed.stderr,
        )

    def test_copied_consumer_files_cannot_impersonate_installed_old_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fake_root = Path(temporary) / "mythic-edge-workflow"
            fake_scripts = fake_root / "scripts"
            fake_scripts.mkdir(parents=True)
            fake_skill = fake_root / "SKILL.md"
            fake_producer = fake_scripts / "accept_fallback_prompt.py"
            shutil.copyfile(OLD_WORKFLOW_SKILL, fake_skill)
            shutil.copyfile(OLD_WORKFLOW_INGRESS, fake_producer)
            errors = validate_fallback_pickup_bundle(
                prompt=self.prompt,
                injection=self.injection,
                pickup=None,
                workflow_skill=fake_skill,
                pickup_producer=fake_producer,
                source_artifact=FALLBACK_SOURCE_ARTIFACT,
                now=NOW,
            )
        self.assertIn(
            "workflow_skill: must be the canonical installed sibling "
            "mythic-edge-workflow/SKILL.md",
            errors,
        )
        self.assertIn(
            "pickup_producer: must be the canonical installed sibling "
            "mythic-edge-workflow/scripts/accept_fallback_prompt.py",
            errors,
        )

    def test_route_receipt_must_bind_the_exact_issue(self) -> None:
        injection = copy.deepcopy(self.injection)
        injection["route_receipt_ref"] = "receipt:route/999"
        injection = with_digest(injection)
        errors = validate_fallback_pickup_bundle(
            prompt=self.prompt,
            injection=injection,
            pickup=None,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn(
            "injection.route_receipt_ref: must equal 'receipt:route/101'",
            errors,
        )

    def test_repository_identity_rejects_traversal_only_segments(self) -> None:
        prompt = copy.deepcopy(self.prompt)
        prompt["repository_id"] = "../.."
        prompt["lane_id"] = "../..#101"
        prompt = with_digest(prompt)
        injection = copy.deepcopy(self.injection)
        injection["repository_id"] = prompt["repository_id"]
        injection["lane_id"] = prompt["lane_id"]
        injection["prompt_sha256"] = prompt["digest"]
        injection = with_digest(injection)
        errors = validate_fallback_pickup_bundle(
            prompt=prompt,
            injection=injection,
            pickup=None,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertIn(
            "prompt.repository_id: must be canonical lowercase owner/repository",
            errors,
        )
        self.assertIn(
            "injection.repository_id: must be canonical lowercase owner/repository",
            errors,
        )
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(
                Path(temporary), prompt=prompt, injection=injection
            )
            self.assertEqual(completed.returncode, 1)
            self.assertFalse(pickup_path.exists())

    def test_invalid_repository_content_is_never_echoed_in_errors(self) -> None:
        marker = "RAW-PRIVATE-CONTENT"
        prompt = copy.deepcopy(self.prompt)
        prompt["repository_id"] = marker
        prompt["lane_id"] = f"{marker}#101"
        prompt = with_digest(prompt)
        injection = copy.deepcopy(self.injection)
        injection["repository_id"] = prompt["repository_id"]
        injection["lane_id"] = prompt["lane_id"]
        injection["prompt_sha256"] = prompt["digest"]
        injection = with_digest(injection)
        errors = validate_fallback_pickup_bundle(
            prompt=prompt,
            injection=injection,
            pickup=None,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        self.assertTrue(errors)
        self.assertNotIn(marker, "\n".join(errors))
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(
                Path(temporary), prompt=prompt, injection=injection
            )
            self.assertEqual(completed.returncode, 1)
            self.assertFalse(pickup_path.exists())
        self.assertNotIn(marker, completed.stderr)

    def test_old_workflow_refuses_to_emit_a_late_pickup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(
                Path(temporary), now_text="2026-07-13T12:04:00Z"
            )
            self.assertEqual(completed.returncode, 1)
            self.assertFalse(pickup_path.exists())
        self.assertIn(
            "binding.timestamps: pickup must occur within five minutes of injection",
            completed.stderr,
        )

    def test_old_workflow_never_overwrites_a_frozen_pickup_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            prompt_path = directory / "prompt.json"
            injection_path = directory / "injection.json"
            pickup_path = directory / "pickup.json"
            _write_json(prompt_path, self.prompt)
            _write_json(injection_path, self.injection)
            pickup_path.write_text("frozen-evidence\n", encoding="utf-8")
            completed = subprocess.run(
                self._producer_command(injection_path, prompt_path, pickup_path),
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(
                pickup_path.read_text(encoding="utf-8"), "frozen-evidence\n"
            )
        self.assertIn("old-workflow pickup output error", completed.stderr)

    def test_pickup_more_than_five_minutes_after_injection_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed, pickup_path = self._emit_pickup(Path(temporary))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            pickup = json.loads(pickup_path.read_text(encoding="utf-8"))
        pickup["picked_up_at"] = "2026-07-13T12:04:00Z"
        pickup = with_digest(pickup)
        errors = validate_fallback_pickup_bundle(
            prompt=self.prompt,
            injection=self.injection,
            pickup=pickup,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=datetime(2026, 7, 13, 12, 5, tzinfo=timezone.utc),
        )
        self.assertIn(
            "binding.timestamps: pickup must occur within five minutes of injection",
            errors,
        )

    def test_old_workflow_accepts_exact_role_pool_fallback_condition_set(self) -> None:
        producer_namespace = runpy.run_path(str(OLD_WORKFLOW_INGRESS))
        self.assertEqual(
            producer_namespace["FALLBACK_CONDITIONS"],
            FALLBACK_CONDITION_IDS,
        )


if __name__ == "__main__":
    unittest.main()
