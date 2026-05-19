from __future__ import annotations

import builtins
import copy
import importlib
import json

from mythic_edge_parser.app import evidence_ledger


def test_vocabulary_constants_match_contract_slice() -> None:
    assert evidence_ledger.VALUE_SOURCES == (
        "observed",
        "derived",
        "inferred",
        "unknown",
        "conflict",
        "legacy_enriched",
    )
    assert evidence_ledger.CONFIDENCE_LEVELS == ("high", "medium", "low", "unknown")
    assert evidence_ledger.FINALITY_LABELS == ("live", "provisional", "final", "reconciled")
    assert evidence_ledger.INVARIANT_STATUSES == (
        "passed",
        "failed",
        "not_applicable",
        "not_checked",
        "degraded",
    )
    assert evidence_ledger.DRIFT_FLAGS == (
        "missing_expected_event_family",
        "missing_expected_payload_path",
        "changed_signal_type",
        "new_unknown_event_family",
        "new_unknown_payload_path",
        "fallback_used",
        "weak_fallback_used",
        "conflicting_evidence",
        "invariant_failed",
        "schema_snapshot_missing",
        "fixture_gap",
        "parser_exception",
        "transport_failure",
        "workbook_drift",
        "deployment_drift",
        "sensitive_evidence_redacted",
    )


def test_build_ledger_returns_stable_top_level_shape() -> None:
    ledger = evidence_ledger.build_player_log_evidence_ledger()

    assert ledger["object"] == evidence_ledger.LEDGER_OBJECT
    assert ledger["schema_version"] == evidence_ledger.LEDGER_SCHEMA_VERSION
    assert ledger["ledger_version"] == evidence_ledger.LEDGER_VERSION
    assert ledger["source_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/128"
    assert ledger["parent_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/11"
    assert ledger["related_adrs"] == ["docs/decisions/ADR-0003-player-log-drift-policy.md"]
    assert ledger["branch_target"] == "codex/parser-reliability-intelligence"
    assert ledger["privacy"] == {
        "raw_private_logs_included": False,
        "raw_payload_values_included": False,
        "source_paths_are_repo_relative_or_symbolic": True,
    }
    assert ledger["vocabulary"] == {
        "value_sources": list(evidence_ledger.VALUE_SOURCES),
        "confidence_levels": list(evidence_ledger.CONFIDENCE_LEVELS),
        "finality_labels": list(evidence_ledger.FINALITY_LABELS),
        "drift_flags": list(evidence_ledger.DRIFT_FLAGS),
        "invariant_statuses": list(evidence_ledger.INVARIANT_STATUSES),
    }
    assert "generated_at" not in ledger


def test_output_family_registry_contains_required_seven_families() -> None:
    families = evidence_ledger.build_player_log_evidence_ledger()["output_families"]

    assert [(family["tier"], family["output_family"], family["status"]) for family in families] == [
        (1, "match_identity_and_lifecycle", "seeded_sample"),
        (2, "queue_format_rank_event_context", "registered_future"),
        (3, "game_level_facts", "registered_future"),
        (4, "sideboarding_and_deck_state", "registered_future"),
        (5, "card_identity_and_gameplay_actions", "registered_future"),
        (6, "runtime_health_and_drift_detection", "registered_future"),
        (7, "derived_analytics_outputs", "registered_future"),
    ]
    assert [family for family in families if family["status"] == "seeded_sample"][0]["seed_fields"] == ["match_id"]


def test_seed_entry_maps_match_id_evidence_signals() -> None:
    entries = evidence_ledger.iter_ledger_entries()

    assert len(entries) == 1
    entry = entries[0]
    assert entry["entry_id"] == "tier1.match_identity.match_id"
    assert entry["tier"] == 1
    assert entry["output_family"] == "match_identity_and_lifecycle"
    assert entry["output_field"] == "match_id"
    assert entry["display_name"] == "MTGA Match ID"
    assert entry["parser_owner"] == "src/mythic_edge_parser/app/state.py"
    assert entry["model_surface"] == "MatchSummary.to_match_log_row"
    assert entry["downstream_surfaces"] == ["MatchLogRow", "GameLogRow", "match_history"]
    assert entry["parser_managed_truth"] is True
    assert entry["coverage_status"] == "seeded_sample"
    assert entry["recommended_review_modules"] == [
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/parsers/match_state.py",
        "src/mythic_edge_parser/parsers/gre/game_state.py",
        "src/mythic_edge_parser/parsers/gre/game_result.py",
    ]
    assert {signal["signal_id"] for signal in entry["direct_evidence"]} == {
        "match_state.match_id",
        "game_state.identity.match_id",
        "game_result.identity.match_id",
    }
    assert entry["fallback_evidence"][0]["signal_id"] == "parser_context.current_match_id"
    assert entry["fallback_evidence"][0]["value_source_when_used"] == "derived"


def test_builtin_ledger_and_entries_validate_cleanly() -> None:
    ledger = evidence_ledger.build_player_log_evidence_ledger()

    assert evidence_ledger.validate_player_log_evidence_ledger() == []
    assert evidence_ledger.validate_player_log_evidence_ledger(ledger) == []
    for entry in ledger["entries"]:
        assert evidence_ledger.validate_ledger_entry(entry) == []


def test_iter_ledger_entries_is_copy_safe() -> None:
    first_entry = evidence_ledger.iter_ledger_entries()[0]
    first_entry["entry_id"] = "tier1.mutated"
    first_entry["direct_evidence"][0]["signal_id"] = "mutated.signal"

    fresh_entry = evidence_ledger.iter_ledger_entries()[0]

    assert fresh_entry["entry_id"] == "tier1.match_identity.match_id"
    assert fresh_entry["direct_evidence"][0]["signal_id"] == "match_state.match_id"


def test_built_ledger_is_json_serializable_and_deterministic() -> None:
    first = evidence_ledger.build_player_log_evidence_ledger()
    second = evidence_ledger.build_player_log_evidence_ledger()

    assert first == second
    encoded = json.dumps(first, indent=2, sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded) == first


def test_validator_reports_missing_required_fields_without_raising() -> None:
    errors = evidence_ledger.validate_player_log_evidence_ledger({})

    assert "ledger:missing:object" in errors
    assert "ledger:missing:entries" in errors
    assert "ledger:entries_not_list" in errors
    assert evidence_ledger.validate_player_log_evidence_ledger("not-a-mapping") == ["ledger:not_mapping"]


def test_validator_reports_unknown_policy_vocabularies() -> None:
    entry = copy.deepcopy(evidence_ledger.iter_ledger_entries()[0])
    entry["value_source_policy"]["direct"] = "guessed"
    entry["confidence_policy"]["direct"] = "certain"
    entry["finality_policy"]["live"] = "done"
    entry["drift_flags"].append("mystery_drift")
    entry["direct_evidence"][0]["value_source_when_used"] = "guessed"
    entry["direct_evidence"][0]["confidence_when_used"] = "certain"
    entry["direct_evidence"][0]["finality_when_used"] = "done"

    errors = evidence_ledger.validate_ledger_entry(entry)

    assert "entry:value_source_policy:unknown:direct:guessed" in errors
    assert "entry:confidence_policy:unknown:direct:certain" in errors
    assert "entry:finality_policy:unknown:live:done" in errors
    assert "drift_flags:unknown:mystery_drift" in errors
    assert "entry:direct_evidence[0]:evidence:value_source_when_used:unknown:guessed" in errors
    assert "entry:direct_evidence[0]:evidence:confidence_when_used:unknown:certain" in errors
    assert "entry:direct_evidence[0]:evidence:finality_when_used:unknown:done" in errors


def test_validator_reports_duplicate_entry_and_signal_ids() -> None:
    ledger = evidence_ledger.build_player_log_evidence_ledger()
    ledger["entries"].append(copy.deepcopy(ledger["entries"][0]))
    entry = copy.deepcopy(evidence_ledger.iter_ledger_entries()[0])
    entry["fallback_evidence"][0]["signal_id"] = entry["direct_evidence"][0]["signal_id"]

    ledger_errors = evidence_ledger.validate_player_log_evidence_ledger(ledger)
    entry_errors = evidence_ledger.validate_ledger_entry(entry)

    assert "duplicate_entry_id:tier1.match_identity.match_id" in ledger_errors
    assert "duplicate_signal_id:match_state.match_id" in entry_errors


def test_validator_reports_absolute_paths_and_raw_log_like_text() -> None:
    entry = copy.deepcopy(evidence_ledger.iter_ledger_entries()[0])
    entry["parser_owner"] = "/private/example/state.py"
    entry["notes"].append("[UnityCrossThreadLogger]5/19/2026 12:00:00 PM")

    errors = evidence_ledger.validate_ledger_entry(entry)

    assert "privacy:absolute_path:entry.parser_owner" in errors
    assert "privacy:forbidden_text:entry.notes[1]" in errors


def test_field_evidence_validator_enforces_vocabularies_and_review_rules() -> None:
    payload = {
        "object": evidence_ledger.FIELD_EVIDENCE_OBJECT,
        "schema_version": evidence_ledger.FIELD_EVIDENCE_SCHEMA_VERSION,
        "ledger_version": evidence_ledger.LEDGER_VERSION,
        "entry_id": "tier1.match_identity.match_id",
        "output_family": "match_identity_and_lifecycle",
        "output_field": "match_id",
        "value_source": "observed",
        "confidence": "high",
        "finality": "live",
        "source_event_kind": "MatchState",
        "source_event_type": "match_started",
        "source_payload_paths": ["payload.match_id"],
        "source_event_timestamp": "",
        "drift_flags": [],
        "invariant_status": "not_checked",
        "degraded_reason": "",
        "review_required": False,
    }

    assert evidence_ledger.validate_field_evidence(payload) == []

    invalid = dict(payload)
    invalid.update(
        {
            "value_source": "guessed",
            "confidence": "certain",
            "finality": "done",
            "drift_flags": ["mystery_drift"],
            "invariant_status": "mystery",
        }
    )

    errors = evidence_ledger.validate_field_evidence(invalid)

    assert "field_evidence:value_source:unknown:guessed" in errors
    assert "field_evidence:confidence:unknown:certain" in errors
    assert "field_evidence:finality:unknown:done" in errors
    assert "field_evidence:drift_flags:unknown:mystery_drift" in errors
    assert "field_evidence:invariant_status:unknown:mystery" in errors


def test_field_evidence_review_required_policy_is_validated() -> None:
    payload = {
        "object": evidence_ledger.FIELD_EVIDENCE_OBJECT,
        "schema_version": evidence_ledger.FIELD_EVIDENCE_SCHEMA_VERSION,
        "ledger_version": evidence_ledger.LEDGER_VERSION,
        "entry_id": "tier1.match_identity.match_id",
        "output_family": "match_identity_and_lifecycle",
        "output_field": "match_id",
        "value_source": "conflict",
        "confidence": "low",
        "finality": "final",
        "source_event_kind": "MatchState",
        "source_event_type": "match_started",
        "source_payload_paths": ["payload.match_id"],
        "source_event_timestamp": "",
        "drift_flags": [],
        "invariant_status": "not_checked",
        "degraded_reason": "conflicting evidence",
        "review_required": False,
    }

    assert "field_evidence:invalid_review_required" in evidence_ledger.validate_field_evidence(payload)
    payload["review_required"] = True
    assert evidence_ledger.validate_field_evidence(payload) == []


def test_ledger_data_omits_private_values_and_local_artifact_markers() -> None:
    encoded = json.dumps(evidence_ledger.build_player_log_evidence_ledger(), sort_keys=True)

    for forbidden in (
        "[UnityCrossThreadLogger]",
        "[Client GRE]",
        "https://" + "hooks.",
        "script.google.com",
        "failed_posts",
        "runtime_status",
        "workbook_exports",
        "/" + "Users/",
        "C:" + "\\Users\\",
    ):
        assert forbidden not in encoded


def test_module_reload_has_no_filesystem_dependency(monkeypatch) -> None:
    def forbidden_open(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("evidence_ledger import must not read files")

    monkeypatch.setattr(builtins, "open", forbidden_open)

    reloaded = importlib.reload(evidence_ledger)

    assert reloaded.build_player_log_evidence_ledger()["object"] == evidence_ledger.LEDGER_OBJECT
