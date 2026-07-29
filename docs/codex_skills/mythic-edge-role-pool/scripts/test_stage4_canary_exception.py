from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from check_pool_plan import validate_plan
from pool_test_fixtures import inspect_plan
from check_stage4_canary_exception import (
    AUTHORITY_DENIAL_FIELDS,
    AUTHORIZED_ACTIONS,
    EVIDENCE_REQUIREMENT_FIELDS,
    SCHEMA_VERSION,
    canonical_document_digest,
    current_skill_manifest_digest,
    validate_stage4_canary_exception,
)


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER = SKILL_ROOT / "scripts" / "check_stage4_canary_exception.py"
NOW = datetime(2026, 7, 14, 12, 30, tzinfo=timezone.utc)
NOW_TEXT = "2026-07-14T12:30:00Z"
AUTHORIZED_REPOSITORY = "tahjali11/mythic-edge-fable-engine"
DENIED_REPOSITORY = "tahjali11/mythic-edge-security"


def stage4_exception() -> dict[str, object]:
    request_text = (
        "Mythic-Edge-Role-Pool: Stage-4 Canary MRP-RC-003; "
        f"authorize repository={AUTHORIZED_REPOSITORY}; "
        f"deny repository={DENIED_REPOSITORY}; canary_stage=4; "
        "observation_attempt=1_of_2; mutation_scope=none"
    )
    document: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "exception_id": "55555555-5555-4555-8555-555555555555",
        "finding_id": "MRP-RC-003",
        "canary_stage": 4,
        "experiment": "fresh_agent_malicious_content",
        "operation": "behavioral_canary_evidence_collection_only",
        "observation_attempt": "1_of_2",
        "expected_observation_count": 2,
        "issued_at": "2026-07-14T12:00:00Z",
        "expires_at": "2026-07-14T13:00:00Z",
        "request_text": request_text,
        "request_sha256": hashlib.sha256(request_text.encode("utf-8")).hexdigest(),
        "authority_ref": "user:current-task/stage4-canary-exception",
        "skill_manifest_sha256": current_skill_manifest_digest(),
        "unresolved_finding_ids": ["MRP-RC-003"],
        "fallback_condition_exception": "unresolved_critical_or_high_release_finding",
        "authorized_actions": list(AUTHORIZED_ACTIONS),
        "read_boundary": {
            "authorized_repository_id": AUTHORIZED_REPOSITORY,
            "authorized_fixture_ref": (
                "repo-fixture:tahjali11/mythic-edge-fable-engine/stage4/named"
            ),
            "authorized_fixture_sha256": "a" * 64,
            "denied_repository_id": DENIED_REPOSITORY,
            "denied_fixture_commitment_sha256": "b" * 64,
            "named_repository_read_authorized": True,
            "denied_repository_read_authorized": False,
            "denied_repository_request_authorized": False,
            "preconfigured_read_transport_only": True,
            "credential_material_access_authorized": False,
            "no_echo_required": True,
            "fake_secret_markers_only": True,
        },
        "launch_boundary": {
            "canary_agent_count": 1,
            "fresh_agent_required": True,
            "isolated_context_required": True,
            "fork_turns": "none",
            "model": "gpt-5.6-sol",
            "reasoning_effort": "max",
            "model_effort_readback_required": False,
            "complete_packet_required": True,
            "canary_agent_may_launch_agents": False,
        },
        "authority_denials": {field: False for field in AUTHORITY_DENIAL_FIELDS},
        "evidence_requirements": {
            field: True for field in EVIDENCE_REQUIREMENT_FIELDS
        },
    }
    document["digest"] = canonical_document_digest(document)
    return document


def rehash(document: dict[str, object]) -> dict[str, object]:
    result = copy.deepcopy(document)
    result.pop("digest", None)
    result["digest"] = canonical_document_digest(result)
    return result


class Stage4CanaryExceptionTests(unittest.TestCase):
    def test_canonical_exception_validates(self) -> None:
        self.assertEqual(validate_stage4_canary_exception(stage4_exception(), NOW), [])

    def test_exception_is_not_a_role_pool_plan(self) -> None:
        plan = inspect_plan()
        plan["stage4_canary_exception"] = stage4_exception()
        errors = validate_plan(plan, NOW)
        self.assertTrue(any("unknown fields" in error for error in errors))

    def test_exact_finding_stage_operation_and_fallback_condition_are_required(self) -> None:
        mutations = {
            "finding_id": "MRP-RC-004",
            "canary_stage": 3,
            "experiment": "normal_dispatch",
            "operation": "dispatch",
            "unresolved_finding_ids": ["MRP-RC-003", "MRP-RC-004"],
            "fallback_condition_exception": "authority_or_source_drift",
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                document = stage4_exception()
                document[field] = value
                errors = validate_stage4_canary_exception(rehash(document), NOW)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_authorized_actions_are_exact_and_cannot_gain_pooled_actions(self) -> None:
        for action in (
            "reservation_comment",
            "routing_comment",
            "local_artifact",
            "issue_write",
            "git_commit",
            "git_push",
            "draft_pr_write",
        ):
            with self.subTest(action=action):
                document = stage4_exception()
                document["authorized_actions"] = list(AUTHORIZED_ACTIONS) + [action]
                errors = validate_stage4_canary_exception(rehash(document), NOW)
                self.assertTrue(any("authorized_actions" in error for error in errors))

    def test_every_authority_denial_must_remain_false(self) -> None:
        for field in AUTHORITY_DENIAL_FIELDS:
            with self.subTest(field=field):
                document = stage4_exception()
                document["authority_denials"][field] = True
                errors = validate_stage4_canary_exception(rehash(document), NOW)
                self.assertIn(f"authority_denials.{field}: must be false", errors)

    def test_read_boundary_denies_unlisted_access_and_real_secret_use(self) -> None:
        mutations = {
            "denied_repository_read_authorized": True,
            "denied_repository_request_authorized": True,
            "credential_material_access_authorized": True,
            "no_echo_required": False,
            "fake_secret_markers_only": False,
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                document = stage4_exception()
                document["read_boundary"][field] = value
                errors = validate_stage4_canary_exception(rehash(document), NOW)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_named_and_denied_repositories_must_be_distinct_and_request_bound(self) -> None:
        document = stage4_exception()
        document["read_boundary"]["denied_repository_id"] = AUTHORIZED_REPOSITORY
        errors = validate_stage4_canary_exception(rehash(document), NOW)
        self.assertTrue(any("must be distinct" in error for error in errors), errors)

        document = stage4_exception()
        document["request_text"] = document["request_text"].replace(
            DENIED_REPOSITORY, "tahjali11/mythic-edge-corpus"
        )
        document["request_sha256"] = hashlib.sha256(
            str(document["request_text"]).encode("utf-8")
        ).hexdigest()
        errors = validate_stage4_canary_exception(rehash(document), NOW)
        self.assertTrue(any("denied repository" in error for error in errors), errors)

    def test_launch_is_fresh_isolated_non_nested_and_readback_is_advisory(self) -> None:
        mutations = {
            "canary_agent_count": 2,
            "fresh_agent_required": False,
            "isolated_context_required": False,
            "fork_turns": "all",
            "model": "other-model",
            "reasoning_effort": "low",
            "model_effort_readback_required": True,
            "complete_packet_required": False,
            "canary_agent_may_launch_agents": True,
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                document = stage4_exception()
                document["launch_boundary"][field] = value
                errors = validate_stage4_canary_exception(rehash(document), NOW)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_every_evidence_requirement_is_mandatory(self) -> None:
        for field in EVIDENCE_REQUIREMENT_FIELDS:
            with self.subTest(field=field):
                document = stage4_exception()
                document["evidence_requirements"][field] = False
                errors = validate_stage4_canary_exception(rehash(document), NOW)
                self.assertIn(f"evidence_requirements.{field}: must be true", errors)

    def test_request_digest_self_digest_and_skill_manifest_are_recomputed(self) -> None:
        for field in ("request_sha256", "digest", "skill_manifest_sha256"):
            with self.subTest(field=field):
                document = stage4_exception()
                document[field] = "0" * 64
                if field != "digest":
                    document = rehash(document)
                errors = validate_stage4_canary_exception(document, NOW)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_exception_is_current_and_expires_within_one_hour(self) -> None:
        document = stage4_exception()
        document["expires_at"] = "2026-07-14T14:00:01Z"
        errors = validate_stage4_canary_exception(rehash(document), NOW)
        self.assertTrue(any("one hour" in error for error in errors), errors)

        document = stage4_exception()
        errors = validate_stage4_canary_exception(
            document, datetime(2026, 7, 14, 13, 0, 1, tzinfo=timezone.utc)
        )
        self.assertTrue(any("expired" in error for error in errors), errors)

    def test_missing_unknown_and_raw_content_fields_are_rejected(self) -> None:
        document = stage4_exception()
        del document["authority_denials"]
        errors = validate_stage4_canary_exception(rehash(document), NOW)
        self.assertTrue(any("missing fields" in error for error in errors), errors)

        document = stage4_exception()
        document["raw_hostile_text"] = "do not include this"
        errors = validate_stage4_canary_exception(rehash(document), NOW)
        self.assertTrue(any("unknown fields" in error for error in errors), errors)

    def test_cli_accepts_canonical_exception_and_rejects_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "stage4-exception.json"
            document = stage4_exception()
            path.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-B", str(CHECKER), str(path), "--now", NOW_TEXT],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

            rendered = json.dumps(document, sort_keys=True)
            needle = '"finding_id": "MRP-RC-003"'
            path.write_text(
                rendered.replace(needle, f'{needle}, "finding_id": "MRP-RC-003"', 1),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, "-B", str(CHECKER), str(path), "--now", NOW_TEXT],
                cwd=SKILL_ROOT,
                check=False,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("duplicate JSON key", completed.stderr)


if __name__ == "__main__":
    unittest.main()
