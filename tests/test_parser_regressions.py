from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from mythic_edge_parser.app import state
from mythic_edge_parser.app.transforms import include_event, summarize, to_sheet_rows
from mythic_edge_parser.log.entry import LineBuffer
from mythic_edge_parser.router import Router

FIXTURES_ROOT = Path(__file__).resolve().parent / "fixtures"
ARENA_LOOKUP = {
    "1001": {"name": "Plains", "resolved_name": "Plains"},
    "1002": {"name": "Island", "resolved_name": "Island"},
    "1003": {"name": "Swamp", "resolved_name": "Swamp"},
    "1004": {"name": "Mountain", "resolved_name": "Mountain"},
    "1005": {"name": "Forest", "resolved_name": "Forest"},
    "1006": {"name": "Opt", "resolved_name": "Opt"},
    "1007": {"name": "Lightning Strike", "resolved_name": "Lightning Strike"},
    "3001": {"name": "Plains", "resolved_name": "Plains"},
    "3002": {"name": "Swamp", "resolved_name": "Swamp"},
    "3003": {"name": "Concealed Courtyard", "resolved_name": "Concealed Courtyard"},
    "3004": {"name": "Cut Down", "resolved_name": "Cut Down"},
    "3005": {"name": "Go for the Throat", "resolved_name": "Go for the Throat"},
    "3006": {"name": "Sheoldred's Edict", "resolved_name": "Sheoldred's Edict"},
    "4001": {"name": "Plains", "resolved_name": "Plains"},
    "4002": {"name": "Island", "resolved_name": "Island"},
    "4003": {"name": "Seachrome Coast", "resolved_name": "Seachrome Coast"},
    "4004": {"name": "No More Lies", "resolved_name": "No More Lies"},
    "4005": {"name": "Sunfall", "resolved_name": "Sunfall"},
    "4006": {"name": "Memory Deluge", "resolved_name": "Memory Deluge"},
    "4007": {"name": "Farewell", "resolved_name": "Farewell"},
}


@dataclass(frozen=True, slots=True)
class ParserRegressionCase:
    fixture_name: str
    expected_name: str
    match_id: str


CASES = (
    ParserRegressionCase(
        fixture_name="parser_regression_match_slice.log",
        expected_name="parser_regression_match_expected.json",
        match_id="match-regression-1",
    ),
    ParserRegressionCase(
        fixture_name="parser_regression_bo3_slice.log",
        expected_name="parser_regression_bo3_expected.json",
        match_id="match-regression-bo3",
    ),
)

GOLDEN_FIXTURE_ID = "parser_regression_match_bo1_v1"
GOLDEN_MANIFEST_NAME = "golden_fixture_manifest.json"
GOLDEN_INPUT_PATH = "tests/fixtures/parser_regression_match_slice.log"
GOLDEN_EXPECTED_PATH = "tests/fixtures/parser_regression_match_golden_expected.json"
GOLDEN_REQUIRED_ENTRY_FIELDS = {
    "fixture_id",
    "fixture_classes",
    "input_path",
    "expected_output_path",
    "expected_output_kind",
    "source_issue",
    "tracker_issue",
    "source_contract",
    "policy_contract",
    "related_adrs",
    "source_type",
    "source_privacy_class",
    "redaction_status",
    "redaction_method",
    "redaction_categories",
    "minimum_evidence_preserved",
    "parser_surfaces_under_test",
    "expected_output_fields",
    "evidence_ledger_tiers",
    "tier_scope_notes",
    "value_source_labels_expected",
    "confidence_labels_expected",
    "finality_labels_expected",
    "drift_flags_expected",
    "invariants_expected",
    "update_approval_required",
    "update_policy",
    "known_limitations",
    "not_applicable",
}
GOLDEN_REQUIRED_NOT_APPLICABLE_FIELDS = {
    "raw_log_source_path",
    "source_log_session_id",
    "source_schema_snapshot_id",
    "sanitizer_tool_version",
    "evidence_ledger_fixture_id",
    "drift_baseline_id",
    "drift_report_expected_output_path",
    "live_workbook_id",
    "deployed_apps_script_version",
    "webhook_url",
    "generated_card_data_version",
    "external_api_source",
    "runtime_status_artifact",
    "failed_post_artifact",
    "workbook_export_artifact",
}
FORBIDDEN_GOLDEN_OUTPUT_KEYS = {
    "context",
    "event_traces",
    "match_summary_debug",
    "match_summary_row",
    "raw_json",
    "router_stats",
}
FORBIDDEN_GOLDEN_OUTPUT_SNIPPETS = (
    "script.google.com/macros",
    "hooks.slack.com/services",
    "discord.com/api/webhooks",
    "C:\\Users\\",
    "/Users/",
    "/home/",
    "data/runtime_logs",
    "data/status",
    "data/failed_posts",
    "data/oracle_data",
    "data/tier_sources",
)


def _seed_arena_lookup() -> None:
    lookup = {grp_id: dict(payload) for grp_id, payload in ARENA_LOOKUP.items()}
    state._ARENA_CARD_LOOKUP = lookup
    state.RUNTIME_STATE.arena_card_lookup = lookup
    state._ARENA_CARD_LOOKUP_READY = True
    state.RUNTIME_STATE.arena_card_lookup_ready = True
    state._GAMEPLAY_CARD_LOOKUP_READY = True
    state.RUNTIME_STATE.gameplay_card_lookup_ready = True


def _normalized_sheet_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(row)
    normalized.pop("raw_json", None)
    return normalized


def _event_trace(event: Any) -> dict[str, Any]:
    state._update_match_summary(event)
    included = include_event(event)
    rows = [_normalized_sheet_row(row) for row in to_sheet_rows(event)] if included else []
    payload = getattr(event, "payload", {}) or {}
    return {
        "kind": getattr(event, "kind", type(event).__name__),
        "payload_type": payload.get("type", ""),
        "included": included,
        "summary": summarize(event),
        "sheet_rows": rows,
    }


def _replay_fixture_snapshot(case: ParserRegressionCase) -> dict[str, Any]:
    state.reset_runtime_state()
    _seed_arena_lookup()

    buffer = LineBuffer()
    router = Router()
    traces: list[dict[str, Any]] = []
    fixture_path = FIXTURES_ROOT / case.fixture_name

    try:
        for line in fixture_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                continue
            for entry in buffer.feed(f"{line}\n"):
                for event in router.route(entry):
                    traces.append(_event_trace(event))
        for entry in buffer.flush():
            for event in router.route(entry):
                traces.append(_event_trace(event))

        summary = state.get_match_summary(case.match_id)
        assert summary is not None

        return {
            "fixture": fixture_path.name,
            "router_stats": {
                "routed": router.stats.routed,
                "unknown": router.stats.unknown,
                "timestamp_missing": router.stats.timestamp_missing,
                "timestamp_parse_failure": router.stats.timestamp_parse_failure,
            },
            "event_traces": traces,
            "context": state.get_context_snapshot(),
            "match_summary_debug": summary.to_debug_dict(),
            "match_summary_row": _normalized_sheet_row(summary.to_sheet_row()),
            "match_log_row": state.build_match_log_row(case.match_id),
            "game_log_rows": state.build_game_summary_rows(case.match_id),
        }
    finally:
        state.reset_runtime_state()


def _repo_fixture_path(repo_relative_path: str) -> Path:
    prefix = "tests/fixtures/"
    assert repo_relative_path.startswith(prefix)
    return FIXTURES_ROOT / repo_relative_path.removeprefix(prefix)


def _collect_json_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_collect_json_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_collect_json_keys(item))
        return keys
    return set()


def _load_golden_fixture_entry(fixture_id: str) -> dict[str, Any]:
    manifest_path = FIXTURES_ROOT / GOLDEN_MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["object"] == "mythic_edge_golden_fixture_manifest"
    assert manifest["schema_version"] == 1

    matching = [entry for entry in manifest["fixtures"] if entry.get("fixture_id") == fixture_id]
    assert len(matching) == 1, f"expected one golden fixture entry for {fixture_id}"
    return matching[0]


def _reduced_parser_owned_output(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "match_log_row": snapshot["match_log_row"],
        "game_log_rows": snapshot["game_log_rows"],
    }


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.fixture_name)
def test_parser_regression_fixture_matches_expected_snapshot(case: ParserRegressionCase) -> None:
    expected_path = FIXTURES_ROOT / case.expected_name
    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    assert _replay_fixture_snapshot(case) == expected


def test_golden_fixture_manifest_replays_to_reduced_parser_owned_expected_output() -> None:
    entry = _load_golden_fixture_entry(GOLDEN_FIXTURE_ID)

    assert GOLDEN_REQUIRED_ENTRY_FIELDS <= set(entry)
    assert GOLDEN_REQUIRED_NOT_APPLICABLE_FIELDS <= set(entry["not_applicable"])
    assert entry["fixture_id"] == GOLDEN_FIXTURE_ID
    assert entry["fixture_classes"] == ["sanitized_player_log_excerpt", "parser_replay_fixture"]
    assert entry["input_path"] == GOLDEN_INPUT_PATH
    assert entry["expected_output_path"] == GOLDEN_EXPECTED_PATH
    assert entry["expected_output_kind"] == "reduced_parser_owned_output"
    assert entry["expected_output_fields"] == ["match_log_row", "game_log_rows"]
    assert entry["value_source_labels_expected"] == "not_applicable"
    assert entry["confidence_labels_expected"] == "not_applicable"
    assert entry["finality_labels_expected"] == "not_applicable"
    assert entry["drift_flags_expected"] == "not_applicable"
    assert entry["update_approval_required"] is True

    expected_path = _repo_fixture_path(entry["expected_output_path"])
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    assert list(expected) == ["match_log_row", "game_log_rows"]
    assert not (FORBIDDEN_GOLDEN_OUTPUT_KEYS & _collect_json_keys(expected))
    expected_text = json.dumps(expected, sort_keys=True)
    assert not any(snippet in expected_text for snippet in FORBIDDEN_GOLDEN_OUTPUT_SNIPPETS)

    snapshot = _replay_fixture_snapshot(
        ParserRegressionCase(
            fixture_name=_repo_fixture_path(entry["input_path"]).name,
            expected_name=expected_path.name,
            match_id="match-regression-1",
        ),
    )

    assert _reduced_parser_owned_output(snapshot) == expected
