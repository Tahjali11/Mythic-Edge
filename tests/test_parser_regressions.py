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


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.fixture_name)
def test_parser_regression_fixture_matches_expected_snapshot(case: ParserRegressionCase) -> None:
    expected_path = FIXTURES_ROOT / case.expected_name
    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    assert _replay_fixture_snapshot(case) == expected
