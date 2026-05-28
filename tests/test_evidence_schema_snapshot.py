from __future__ import annotations

import copy
import hashlib
import json

import pytest

from mythic_edge_parser.app import evidence_ledger
from mythic_edge_parser.app import evidence_schema_snapshot as snapshot_builder


def test_build_evidence_schema_snapshot_returns_contract_shape() -> None:
    snapshot = snapshot_builder.build_evidence_schema_snapshot()
    ledger = evidence_ledger.build_player_log_evidence_ledger()
    direct_count = sum(len(entry["direct_evidence"]) for entry in ledger["entries"])
    fallback_count = sum(len(entry["fallback_evidence"]) for entry in ledger["entries"])

    assert snapshot["object"] == snapshot_builder.EVIDENCE_SCHEMA_SNAPSHOT_OBJECT
    assert snapshot["schema_version"] == snapshot_builder.EVIDENCE_SCHEMA_SNAPSHOT_VERSION
    assert snapshot["snapshot_version"] == 1
    assert snapshot["source_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/175"
    assert snapshot["parent_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/11"
    assert snapshot["ledger"] == {
        "object": ledger["object"],
        "schema_version": ledger["schema_version"],
        "ledger_version": ledger["ledger_version"],
        "source_issue": ledger["source_issue"],
        "parent_issue": ledger["parent_issue"],
        "branch_target": ledger["branch_target"],
        "related_adrs": ledger["related_adrs"],
    }
    assert snapshot["privacy"] == {
        "raw_private_logs_included": False,
        "raw_payload_values_included": False,
        "local_absolute_paths_included": False,
        "runtime_artifacts_included": False,
        "generated_data_included": False,
        "source_paths_are_repo_relative_or_symbolic": True,
    }
    assert snapshot["summary"] == {
        "output_family_count": len(ledger["output_families"]),
        "entry_count": len(ledger["entries"]),
        "evidence_signal_count": direct_count + fallback_count,
        "direct_evidence_signal_count": direct_count,
        "fallback_evidence_signal_count": fallback_count,
        "deferred_output_fields": ["tier3.game_level_facts.deck_state"],
    }
    assert snapshot["vocabulary"] == ledger["vocabulary"]
    assert snapshot["snapshot_policy"] == {
        "deterministic": True,
        "update_mode_default": "disabled",
        "update_env_var": snapshot_builder.UPDATE_ENV_VAR,
        "auto_update_allowed": False,
        "comparison_authority": "review_signal_only",
    }


def test_snapshot_projects_only_stable_schema_surfaces() -> None:
    snapshot = snapshot_builder.build_evidence_schema_snapshot()
    first_entry = snapshot["entries"][0]
    first_signal = snapshot["evidence_signals"][0]

    assert set(snapshot) == {
        "object",
        "schema_version",
        "snapshot_version",
        "snapshot_id",
        "source_issue",
        "parent_issue",
        "ledger",
        "privacy",
        "summary",
        "vocabulary",
        "output_families",
        "entries",
        "evidence_signals",
        "snapshot_policy",
        "limitations",
    }
    assert set(first_entry) == {
        "entry_id",
        "tier",
        "output_family",
        "output_field",
        "display_name",
        "parser_owner",
        "model_surface",
        "downstream_surfaces",
        "parser_managed_truth",
        "coverage_status",
        "direct_signal_ids",
        "fallback_signal_ids",
        "value_source_policy",
        "confidence_policy",
        "finality_policy",
        "invariant_checks",
        "drift_flags",
        "recommended_review_modules",
        "tests",
        "fixture_refs",
    }
    assert set(first_signal) == {
        "entry_id",
        "evidence_kind",
        "signal_id",
        "parser_event_kind",
        "parser_event_type",
        "raw_event_family",
        "raw_message_type",
        "normalized_payload_path",
        "raw_payload_path",
        "required_for_final",
        "value_source_when_used",
        "confidence_when_used",
        "finality_when_used",
        "allowed_types",
        "privacy_class",
    }
    assert "notes" not in first_entry
    assert "degradation_behavior" not in first_entry
    assert "missing_behavior" not in first_signal


def test_snapshot_generation_is_deterministic_and_does_not_mutate_ledger() -> None:
    ledger = evidence_ledger.build_player_log_evidence_ledger()
    original = copy.deepcopy(ledger)

    first = snapshot_builder.build_evidence_schema_snapshot(ledger)
    second = snapshot_builder.build_evidence_schema_snapshot(ledger)

    assert first == second
    assert ledger == original


def test_snapshot_id_is_hash_of_canonical_content_without_snapshot_id() -> None:
    snapshot = snapshot_builder.build_evidence_schema_snapshot()
    content = dict(snapshot)
    content["snapshot_id"] = ""
    expected_digest = hashlib.sha256(
        json.dumps(content, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8"),
    ).hexdigest()

    assert snapshot["snapshot_id"] == f"sha256:{expected_digest}"


def test_committed_expected_snapshot_matches_generated_current_snapshot() -> None:
    current = snapshot_builder.build_evidence_schema_snapshot()
    expected = snapshot_builder.load_expected_evidence_schema_snapshot()

    assert snapshot_builder.compare_evidence_schema_snapshot(current, expected)["status"] == "pass"
    assert current == expected


def test_builder_validates_current_ledger_before_projection(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        snapshot_builder.evidence_ledger,
        "validate_player_log_evidence_ledger",
        lambda payload: ["ledger:synthetic_error"],
    )

    with pytest.raises(ValueError, match="invalid evidence ledger: ledger:synthetic_error"):
        snapshot_builder.build_evidence_schema_snapshot()


def test_missing_expected_snapshot_check_fails_with_policy_message(
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    missing_path = tmp_path / "missing.json"

    assert snapshot_builder.main(["--check", "--expected", str(missing_path)]) == 1
    captured = capsys.readouterr()

    assert snapshot_builder.SNAPSHOT_POLICY_MESSAGE in captured.err
    assert '"status": "fail"' in captured.out
    assert not missing_path.exists()


def test_snapshot_mismatch_check_fails_without_updating(
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    expected = snapshot_builder.build_evidence_schema_snapshot()
    expected["summary"]["entry_count"] += 1
    expected_path = tmp_path / "expected.json"
    snapshot_builder.write_evidence_schema_snapshot(expected_path, expected)

    assert snapshot_builder.main(["--check", "--expected", str(expected_path)]) == 1
    captured = capsys.readouterr()

    assert snapshot_builder.SNAPSHOT_POLICY_MESSAGE in captured.err
    assert '"status": "diff"' in captured.out
    assert snapshot_builder.load_expected_evidence_schema_snapshot(expected_path)["summary"]["entry_count"] != (
        snapshot_builder.build_evidence_schema_snapshot()["summary"]["entry_count"]
    )


def test_update_mode_requires_explicit_environment_variable(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    expected_path = tmp_path / "expected.json"

    monkeypatch.delenv(snapshot_builder.UPDATE_ENV_VAR, raising=False)
    assert snapshot_builder.main(["--update", "--expected", str(expected_path)]) == 2
    assert not expected_path.exists()
    assert snapshot_builder.SNAPSHOT_POLICY_MESSAGE in capsys.readouterr().err

    monkeypatch.setenv(snapshot_builder.UPDATE_ENV_VAR, "1")
    assert snapshot_builder.main(["--update", "--expected", str(expected_path)]) == 0
    assert snapshot_builder.load_expected_evidence_schema_snapshot(expected_path) == (
        snapshot_builder.build_evidence_schema_snapshot()
    )


def test_snapshot_excludes_private_volatile_and_generated_content() -> None:
    snapshot = snapshot_builder.build_evidence_schema_snapshot()
    encoded = json.dumps(snapshot, ensure_ascii=False, sort_keys=True)

    for forbidden in (
        "generated_at",
        "updated_at",
        "raw_bytes_hash",
        "EventMetadata.raw_bytes",
        "[UnityCrossThreadLogger]",
        "[Client GRE]",
        "DETAILED LOGS:",
        "script.google.com/macros/",
        "Bearer ",
        "api_key",
        "secret=",
        "token=",
        "/Users/",
        "C:\\Users\\",
        "data/runtime_logs/",
        "data/failed_posts/",
        "data/status/",
        "data/generated/",
    ):
        assert forbidden not in encoded


def test_forbidden_snapshot_content_is_rejected() -> None:
    snapshot = snapshot_builder.build_evidence_schema_snapshot()
    snapshot["entries"][0]["parser_owner"] = "/Users/example/private.py"

    with pytest.raises(ValueError, match="forbidden evidence schema snapshot content"):
        snapshot_builder.write_evidence_schema_snapshot(
            snapshot_builder.EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH,
        snapshot,
    )


@pytest.mark.parametrize(
    "private_path",
    [
        "repo note /Users/example/private.py",
        "prefix C:\\Users\\Example Name\\private.py",
    ],
)
def test_embedded_local_path_markers_are_rejected_without_dumping_values(private_path: str) -> None:
    snapshot = snapshot_builder.build_evidence_schema_snapshot()
    snapshot["entries"][0]["parser_owner"] = private_path

    with pytest.raises(ValueError) as exc_info:
        snapshot_builder.write_evidence_schema_snapshot(
            snapshot_builder.EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH,
            snapshot,
        )

    message = str(exc_info.value)
    assert "forbidden evidence schema snapshot content" in message
    assert "snapshot.entries[0].parser_owner" in message
    assert private_path not in message


def test_comparison_reports_schema_surface_changes_without_raw_values() -> None:
    current = snapshot_builder.build_evidence_schema_snapshot()
    expected = copy.deepcopy(current)
    expected["output_families"][0]["status"] = "registered_future"
    expected["entries"][0]["output_field"] = "changed_output_field"
    expected["entries"][0]["value_source_policy"]["direct"] = "unknown"
    expected["evidence_signals"][0]["normalized_payload_path"] = "payload.private_value"
    expected["vocabulary"]["value_sources"] = ["observed"]

    comparison = snapshot_builder.compare_evidence_schema_snapshot(current, expected)
    encoded = json.dumps(comparison, sort_keys=True)

    assert comparison["status"] == "diff"
    assert comparison["review_required"] is True
    assert comparison["diff"]["changed_output_families"] == ["match_identity_and_lifecycle"]
    assert comparison["diff"]["changed_entries"] == ["tier1.match_identity.match_id"]
    assert comparison["diff"]["changed_evidence_signals"] == [
        "tier1.match_identity.match_id:direct:match_state.match_id",
    ]
    assert comparison["diff"]["changed_vocabulary"] == ["value_sources"]
    assert comparison["diff"]["changed_policies"] == ["tier1.match_identity.match_id.value_source_policy"]
    assert "payload.private_value" not in encoded


def test_comparison_fails_for_private_or_volatile_expected_snapshot_content() -> None:
    current = snapshot_builder.build_evidence_schema_snapshot()
    expected = copy.deepcopy(current)
    expected["entries"][0]["parser_owner"] = "/Users/example/private.py"

    comparison = snapshot_builder.compare_evidence_schema_snapshot(current, expected)

    assert comparison["status"] == "fail"
    assert comparison["summary"]["privacy_findings"] == 1
    assert comparison["privacy"]["local_absolute_paths_found"] == ["expected.entries[0].parser_owner"]


@pytest.mark.parametrize(
    ("side", "private_path", "expected_finding"),
    [
        ("current", "repo note /Users/example/private.py", "current.entries[0].parser_owner"),
        ("expected", "prefix C:\\Users\\Example Name\\private.py", "expected.entries[0].parser_owner"),
    ],
)
def test_comparison_fails_for_embedded_local_path_markers_without_raw_values(
    side: str,
    private_path: str,
    expected_finding: str,
) -> None:
    current = snapshot_builder.build_evidence_schema_snapshot()
    expected = copy.deepcopy(current)
    target = current if side == "current" else expected
    target["entries"][0]["parser_owner"] = private_path

    comparison = snapshot_builder.compare_evidence_schema_snapshot(current, expected)
    encoded = json.dumps(comparison, sort_keys=True)

    assert comparison["status"] == "fail"
    assert comparison["summary"]["privacy_findings"] == 1
    assert comparison["privacy"]["local_absolute_paths_found"] == [expected_finding]
    assert private_path not in encoded


def test_snapshot_preserves_deferred_and_report_only_boundaries() -> None:
    snapshot = snapshot_builder.build_evidence_schema_snapshot()
    families = {family["output_family"]: family for family in snapshot["output_families"]}
    entries = {entry["entry_id"]: entry for entry in snapshot["entries"]}

    assert families["game_level_facts"]["future_fields"] == ["deck_state"]
    assert "tier3.game_level_facts.deck_state" in snapshot["summary"]["deferred_output_fields"]
    assert not any(entry_id.startswith("tier3.deck_state.") for entry_id in entries)
    assert families["runtime_health_and_drift_detection"]["seed_fields"] == [
        "diagnostics_status",
        "unknown_entry_count",
        "truncation_count",
    ]
    assert families["derived_analytics_outputs"]["seed_fields"] == [
        "card_performance",
        "feature_equity_counts",
    ]
    assert "tier7.derived_analytics_outputs.card_performance" in entries
    assert "tier7.derived_analytics_outputs.feature_equity_counts" in entries


def test_write_mode_writes_explicit_path_only(tmp_path) -> None:
    output_path = tmp_path / "review" / "snapshot.json"

    assert snapshot_builder.main(["--write", str(output_path)]) == 0

    written = output_path.read_text(encoding="utf-8")
    assert written.endswith("\n")
    assert json.loads(written) == snapshot_builder.build_evidence_schema_snapshot()
