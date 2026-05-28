from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from ..log.entry import LineBuffer
from ..router import Router
from . import evidence_validation_report_wiring, parser_diagnostics, state
from .config import PROJECT_ROOT
from .diagnostics import sanitize_sensitive_text
from .transforms import include_event, to_sheet_rows

MANIFEST_OBJECT = "mythic_edge_golden_replay_manifest"
MANIFEST_SCHEMA_VERSION = "parser_golden_replay_manifest.v1"
REPORT_OBJECT = "mythic_edge_golden_replay_report"
REPORT_SCHEMA_VERSION = "parser_golden_replay_report.v1"

STATUS_PASS = "pass"
STATUS_DEGRADED = "degraded"
STATUS_REVIEW = "review"
STATUS_DIFF = "diff"
STATUS_FAIL = "fail"
STATUS_PRECEDENCE = (STATUS_FAIL, STATUS_DIFF, STATUS_REVIEW, STATUS_DEGRADED, STATUS_PASS)
CLI_FAILURE_STATUSES = {STATUS_FAIL, STATUS_DIFF, STATUS_REVIEW}

ALLOWED_SOURCE_KINDS = {"sanitized_player_log_slice", "synthetic_player_log_slice"}
ALLOWED_SANITIZATION_STATUSES = {"sanitized", "synthetic", "legacy_unclassified", "requires_review"}
REVIEW_SANITIZATION_STATUSES = {"legacy_unclassified", "requires_review"}
REQUIRED_EXPECTED_SECTIONS = (
    "router_stats",
    "event_family_counts",
    "event_kind_sequence",
    "diagnostics_summary",
    "truncation_and_data_loss",
    "unknowns_and_degradation",
    "parser_state",
    "final_reconciliation",
    "parser_owned_rows",
)

FORBIDDEN_FIXTURE_PATTERNS = (
    ("local_user_path", re.compile(r"(?i)(/Users/|C:\\Users\\)[^\s,;]+")),
    ("bearer_token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}")),
    ("apps_script_url", re.compile(r"https?://script\.google\.com/[^\s)>\]}\"]+", re.IGNORECASE)),
    ("webhook_url", re.compile(r"https?://hooks\.[^\s)>\]}\"]+", re.IGNORECASE)),
    ("api_key_assignment", re.compile(r"(?i)\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,}")),
)

MATCH_LOG_KEYS = (
    "MTGA Match ID",
    "MTGA Event ID",
    "MTGA Format",
    "MTGA Queue Type",
    "MTGA Rank Raw",
    "MTGA Submit Deck Seen",
    "MTGA Sideboard Entered",
    "Match Win?",
    "Match Win Flag",
    "Total Games",
    "Games Won",
    "Games Lost",
    "Game Win %",
    "Game 1 Result",
    "Game 2 Result",
    "Game 3 Result",
    "G1 Mulligans",
    "G2 Mulligans",
    "G3 Mulligans",
    "G1 Play / Draw",
    "G2 Play / Draw",
    "G3 Play / Draw",
    "G1 Turn Count",
    "G2 Turn Count",
    "G3 Turn Count",
)

GAME_LOG_KEYS = (
    "MTGA Match ID",
    "MTGA Event ID",
    "MTGA Format",
    "MTGA Queue Type",
    "Game Number",
    "Game Result",
    "Turn Count",
    "Mulligans",
    "Play / Draw",
    "Pre / Postboard",
    "Opening Hand Size",
    "Opening Hand",
)


@dataclass(slots=True)
class GoldenReplayFixtureResult:
    fixture_id: str
    status: str
    manifest_path: Path
    fixture_path: Path | None = None
    privacy: dict[str, Any] = field(default_factory=dict)
    comparisons: dict[str, str] = field(default_factory=dict)
    diffs: list[dict[str, Any]] = field(default_factory=list)
    degradation: list[str] = field(default_factory=list)
    review_notes: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    truncation_count: int = 0
    data_loss_count: int = 0

    def to_report_result(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "fixture_id": self.fixture_id,
            "status": self.status,
            "manifest_path": _safe_repo_path(self.manifest_path),
            "fixture_path": _safe_repo_path(self.fixture_path) if self.fixture_path is not None else "",
            "privacy": self.privacy,
            "comparisons": dict(self.comparisons),
            "diffs": list(self.diffs),
            "degradation": list(self.degradation),
            "review_notes": list(self.review_notes),
        }
        if self.failures:
            payload["failures"] = list(self.failures)
        return _sanitize_report_value(payload)


def build_golden_replay_report(
    manifest_paths: Sequence[Path],
    *,
    evidence_ledger_review: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    results = [run_golden_replay(Path(manifest_path)) for manifest_path in manifest_paths]
    status = _suite_status(results)
    summary = {
        "manifests_total": len(results),
        STATUS_PASS: sum(result.status == STATUS_PASS for result in results),
        STATUS_DEGRADED: sum(result.status == STATUS_DEGRADED for result in results),
        STATUS_REVIEW: sum(result.status == STATUS_REVIEW for result in results),
        STATUS_DIFF: sum(result.status == STATUS_DIFF for result in results),
        STATUS_FAIL: sum(result.status == STATUS_FAIL for result in results),
        "fixtures_with_truncation": sum(result.truncation_count > 0 for result in results),
        "fixtures_with_data_loss": sum(result.data_loss_count > 0 for result in results),
    }
    return _sanitize_report_value(
        {
            "object": REPORT_OBJECT,
            "schema_version": REPORT_SCHEMA_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "suite_status": status,
            "summary": summary,
            "results": [result.to_report_result() for result in results],
            "metadata": {
                "degraded_cli_exit_code": 0,
                "evidence_ledger_review_status_affects_suite": False,
                "explicit_inputs_required": True,
                "normal_parser_path": ["LineBuffer", "Router", "parser modules", "transforms", "parser state"],
                "truth_boundary": "Golden replay compares parser-owned outputs; it does not infer missing facts.",
            },
            "evidence_ledger_review": evidence_validation_report_wiring.evidence_review_section_from_inputs(
                evidence_ledger_review,
                report_context="golden_replay",
            ),
        }
    )


def run_golden_replay(manifest_path: Path) -> GoldenReplayFixtureResult:
    manifest_display = _safe_repo_path(manifest_path)
    manifest = _load_manifest(manifest_path)
    if not isinstance(manifest, dict):
        return _fail_result(
            manifest_path,
            fixture_id="",
            failures=[f"malformed_manifest_json:{manifest_display}"],
        )

    fixture_id = str(manifest.get("fixture_id") or "").strip()
    validation_failures = _manifest_validation_failures(manifest)
    validation_failures.extend(_content_validation_failures(manifest_path, failure_prefix="forbidden_manifest_content"))
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    fixture_path = _resolve_fixture_path(source.get("log_path") if isinstance(source, dict) else None)
    privacy = _privacy_payload(source if isinstance(source, dict) else {})
    review_notes = _manifest_review_notes(manifest)
    degradation = _manifest_degradation(manifest)

    if validation_failures:
        return _fail_result(
            manifest_path,
            fixture_id=fixture_id,
            fixture_path=fixture_path,
            privacy=privacy,
            failures=validation_failures,
            review_notes=review_notes,
            degradation=degradation,
        )

    assert fixture_path is not None
    fixture_failures = _fixture_validation_failures(fixture_path)
    if fixture_failures:
        return _fail_result(
            manifest_path,
            fixture_id=fixture_id,
            fixture_path=fixture_path,
            privacy=privacy,
            failures=fixture_failures,
            review_notes=review_notes,
            degradation=degradation,
        )

    try:
        observed = _build_observed_parser_output(fixture_path)
    except Exception as exc:  # pragma: no cover - focused tests monkeypatch this path.
        return _fail_result(
            manifest_path,
            fixture_id=fixture_id,
            fixture_path=fixture_path,
            privacy=privacy,
            failures=[f"parser_replay_exception:{type(exc).__name__}:{sanitize_sensitive_text(exc)}"],
            review_notes=review_notes,
            degradation=degradation,
        )

    expected = manifest.get("expected") if isinstance(manifest.get("expected"), dict) else {}
    comparisons: dict[str, str] = {}
    diffs: list[dict[str, Any]] = []
    for section in REQUIRED_EXPECTED_SECTIONS:
        section_diffs = _compare_expected_section(
            manifest_path=manifest_path,
            fixture_id=fixture_id,
            section=section,
            expected=expected.get(section),
            observed=observed.get(section),
        )
        comparisons[section] = STATUS_DIFF if section_diffs else STATUS_PASS
        diffs.extend(section_diffs)

    unexpected_notes = _unexpected_evidence_notes(manifest, observed)
    review_notes.extend(unexpected_notes)

    status = STATUS_PASS
    if diffs:
        status = STATUS_DIFF
    elif review_notes:
        status = STATUS_REVIEW
    elif degradation:
        status = STATUS_DEGRADED

    return GoldenReplayFixtureResult(
        fixture_id=fixture_id,
        status=status,
        manifest_path=manifest_path,
        fixture_path=fixture_path,
        privacy={**privacy, "review_required": bool(review_notes)},
        comparisons=comparisons,
        diffs=diffs,
        degradation=degradation,
        review_notes=review_notes,
        truncation_count=_safe_int(observed["truncation_and_data_loss"].get("truncation_count")),
        data_loss_count=len(observed["truncation_and_data_loss"].get("data_loss_events") or []),
    )


def _load_manifest(manifest_path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _manifest_validation_failures(manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if manifest.get("object") != MANIFEST_OBJECT:
        failures.append("invalid_manifest_object")
    if manifest.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        failures.append("invalid_manifest_schema_version")
    if not str(manifest.get("fixture_id") or "").strip():
        failures.append("missing_fixture_id")
    if manifest.get("linked_issue") != "https://github.com/Tahjali11/Mythic-Edge/issues/48":
        failures.append("missing_or_invalid_linked_issue")
    if manifest.get("authorized_by_contract") != "docs/contracts/parser_golden_replay_harness.md":
        failures.append("missing_or_invalid_contract_authorization")

    source = manifest.get("source")
    if not isinstance(source, dict):
        failures.append("missing_source")
        source = {}
    source_kind = source.get("source_kind")
    sanitization_status = source.get("sanitization_status")
    if source_kind not in ALLOWED_SOURCE_KINDS:
        failures.append("invalid_source_kind")
    if sanitization_status not in ALLOWED_SANITIZATION_STATUSES:
        failures.append("invalid_sanitization_status")
    if source.get("source_privacy_class") != "sanitized_committable":
        failures.append("invalid_source_privacy_class")
    if source.get("raw_private_log_committed") is not False:
        failures.append("raw_private_log_committed_must_be_false")
    if _resolve_fixture_path(source.get("log_path")) is None:
        failures.append("missing_or_invalid_fixture_path")

    coverage = manifest.get("coverage")
    if not isinstance(coverage, dict):
        failures.append("missing_coverage")
        coverage = {}
    for key in ("covered_event_families", "known_gaps", "expected_degradation", "expected_truncation_signals"):
        if not isinstance(coverage.get(key), list):
            failures.append(f"missing_or_invalid_coverage:{key}")

    expected = manifest.get("expected")
    if not isinstance(expected, dict):
        failures.append("missing_expected")
        expected = {}
    for section in REQUIRED_EXPECTED_SECTIONS:
        if section not in expected:
            failures.append(f"missing_expected_section:{section}")
    return failures


def _resolve_fixture_path(raw_path: Any) -> Path | None:
    text = str(raw_path or "").strip()
    if not text:
        return None
    path = Path(text)
    if path.is_absolute() or ".." in path.parts:
        return None
    root = PROJECT_ROOT.resolve(strict=False)
    resolved = (root / path).resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError:
        return None
    return resolved


def _fixture_validation_failures(fixture_path: Path) -> list[str]:
    if not fixture_path.is_file():
        return [f"fixture_unreadable:{_safe_repo_path(fixture_path)}"]
    return _content_validation_failures(fixture_path, failure_prefix="forbidden_fixture_content")


def _content_validation_failures(path: Path, *, failure_prefix: str) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return [f"fixture_unreadable:{_safe_repo_path(path)}:{type(exc).__name__}"]

    failures: list[str] = []
    for label, pattern in FORBIDDEN_FIXTURE_PATTERNS:
        if pattern.search(text):
            failures.append(f"{failure_prefix}:{label}")
    return failures


def _privacy_payload(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "sanitization_status": source.get("sanitization_status", ""),
        "source_kind": source.get("source_kind", ""),
        "source_privacy_class": source.get("source_privacy_class", ""),
        "raw_private_log_committed": bool(source.get("raw_private_log_committed")),
        "review_required": source.get("sanitization_status") in REVIEW_SANITIZATION_STATUSES,
    }


def _manifest_review_notes(manifest: dict[str, Any]) -> list[str]:
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    status = source.get("sanitization_status")
    notes: list[str] = []
    if status == "legacy_unclassified":
        notes.append("legacy_unclassified_fixture_metadata")
    elif status == "requires_review":
        notes.append("fixture_sanitization_requires_review")
    return notes


def _manifest_degradation(manifest: dict[str, Any]) -> list[str]:
    coverage = manifest.get("coverage") if isinstance(manifest.get("coverage"), dict) else {}
    degradation: list[str] = []
    for key in ("known_gaps", "expected_degradation", "expected_truncation_signals"):
        for item in coverage.get(key) or []:
            text = str(item or "").strip()
            if text:
                degradation.append(f"{key}:{text}")
    return degradation


def _build_observed_parser_output(fixture_path: Path) -> dict[str, Any]:
    state.reset_runtime_state()
    _seed_empty_fixture_card_lookup()
    router = Router()
    event_family_counts: Counter[str] = Counter()
    event_kind_sequence: list[str] = []

    try:
        _replay_fixture_lines(fixture_path, router, event_family_counts, event_kind_sequence)
        diagnostics_report = parser_diagnostics.build_parser_diagnostics_report(fixture_path, profile="fixture")
        context = state.get_context_snapshot()
        match_id = str(context.get("current_match_id") or "").strip()
        summary = state.get_match_summary(match_id) if match_id else None
        if summary is None:
            summaries = state.iter_match_summaries()
            summary = summaries[0] if len(summaries) == 1 else None
            match_id = summary.match_id if summary is not None else match_id
        summary_debug = summary.to_debug_dict() if summary is not None else {}
        match_log_row = state.build_match_log_row(match_id) if match_id else None
        game_log_rows = state.build_game_summary_rows(match_id) if match_id else []
        stats = router.stats
        return {
            "router_stats": {
                "routed": stats.routed,
                "unknown": stats.unknown,
                "timestamp_missing": stats.timestamp_missing,
                "timestamp_parse_failure": stats.timestamp_parse_failure,
            },
            "event_family_counts": dict(sorted(event_family_counts.items())),
            "event_kind_sequence": event_kind_sequence,
            "diagnostics_summary": _diagnostics_summary(diagnostics_report),
            "truncation_and_data_loss": _truncation_summary(diagnostics_report),
            "unknowns_and_degradation": _unknowns_summary(diagnostics_report),
            "parser_state": _parser_state_summary(context, summary_debug),
            "final_reconciliation": _final_reconciliation_summary(summary_debug),
            "parser_owned_rows": _parser_owned_rows_summary(match_log_row, game_log_rows),
        }
    finally:
        state.reset_runtime_state()


def _seed_empty_fixture_card_lookup() -> None:
    lookup: dict[str, dict[str, Any]] = {}
    state._ARENA_CARD_LOOKUP = lookup
    state.RUNTIME_STATE.arena_card_lookup = lookup
    state._ARENA_CARD_LOOKUP_READY = True
    state.RUNTIME_STATE.arena_card_lookup_ready = True
    state._GAMEPLAY_CARD_LOOKUP_READY = True
    state.RUNTIME_STATE.gameplay_card_lookup_ready = True


def _replay_fixture_lines(
    fixture_path: Path,
    router: Router,
    event_family_counts: Counter[str],
    event_kind_sequence: list[str],
) -> None:
    buffer = LineBuffer()
    with fixture_path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            if raw_line.startswith("#"):
                continue
            _route_entries(buffer.feed(raw_line), router, event_family_counts, event_kind_sequence)
    _route_entries(buffer.flush(), router, event_family_counts, event_kind_sequence)


def _route_entries(
    entries: list[Any],
    router: Router,
    event_family_counts: Counter[str],
    event_kind_sequence: list[str],
) -> None:
    for entry in entries:
        for event in router.route(entry):
            state._update_match_summary(event)
            if include_event(event):
                to_sheet_rows(event)
            kind = str(getattr(event, "kind", type(event).__name__) or "").strip()
            if kind:
                event_family_counts[kind] += 1
                event_kind_sequence.append(kind)


def _diagnostics_summary(report: dict[str, Any]) -> dict[str, Any]:
    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    return {
        "overall_status": report.get("overall_status", ""),
        "parser_status": summary.get("parser_status", ""),
        "routed_entries": _safe_int(summary.get("routed_entries")),
        "unknown_entries": _safe_int(summary.get("unknown_entries")),
        "truncation_events": _safe_int(summary.get("truncation_events")),
        "parser_failures": _safe_int(summary.get("parser_failures")),
    }


def _truncation_summary(report: dict[str, Any]) -> dict[str, Any]:
    section = report.get("truncation_and_data_loss") if isinstance(report.get("truncation_and_data_loss"), dict) else {}
    data_loss_events = section.get("data_loss_events")
    return {
        "truncation_count": _safe_int(section.get("truncation_count")),
        "data_loss_events": data_loss_events if isinstance(data_loss_events, list) else [],
    }


def _unknowns_summary(report: dict[str, Any]) -> dict[str, Any]:
    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    section = report.get("unknowns_and_degradation") if isinstance(report.get("unknowns_and_degradation"), dict) else {}
    return {
        "unknown_entry_count": _safe_int(summary.get("unknown_entries")),
        "degraded_outputs": section.get("drift_flags") if isinstance(section.get("drift_flags"), list) else [],
        "unknown_signatures": section.get("unknown_signatures")
        if isinstance(section.get("unknown_signatures"), list)
        else [],
    }


def _parser_state_summary(context: dict[str, Any], summary_debug: dict[str, Any]) -> dict[str, Any]:
    return {
        "match_id": summary_debug.get("match_id") or context.get("current_match_id", ""),
        "current_game_number": context.get("current_game_number", ""),
        "player_team": summary_debug.get("player_team") or context.get("current_player_team", ""),
        "constructed_rank": summary_debug.get("constructed_rank", ""),
        "event_id": summary_debug.get("event_id", ""),
        "match_win_condition": summary_debug.get("match_win_condition", ""),
        "submit_deck_seen": bool(summary_debug.get("submit_deck_seen")),
        "sideboarding_entered": bool(summary_debug.get("sideboarding_entered")),
        "total_games": summary_debug.get("total_games", ""),
        "game_wins": summary_debug.get("game_wins", ""),
        "game_losses": summary_debug.get("game_losses", ""),
        "games": [_game_summary(game) for game in _meaningful_games(summary_debug.get("games"))],
    }


def _meaningful_games(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    games = [game for game in value if isinstance(game, dict)]
    return [
        game
        for game in games
        if game.get("winner_team") not in (None, "")
        or game.get("result") not in (None, "")
        or _safe_int(game.get("turn_count")) > 0
        or bool(game.get("opening_hand"))
    ]


def _game_summary(game: dict[str, Any]) -> dict[str, Any]:
    opening_hand = game.get("opening_hand") if isinstance(game.get("opening_hand"), list) else []
    return {
        "game_number": game.get("game_number", ""),
        "winner_team": game.get("winner_team", ""),
        "result": game.get("result", ""),
        "starting_player": game.get("starting_player", ""),
        "play_draw": game.get("play_draw", ""),
        "mulligans": game.get("mulligans", ""),
        "turn_count": game.get("turn_count", ""),
        "opening_hand_size": len(opening_hand),
        "opening_hand": opening_hand,
    }


def _final_reconciliation_summary(summary_debug: dict[str, Any]) -> dict[str, Any]:
    return {
        "match_winner_team": summary_debug.get("match_winner_team", ""),
        "match_result_type": summary_debug.get("match_result_type", ""),
        "match_result_reason": summary_debug.get("match_result_reason", ""),
        "game_results": [
            {
                "game_number": game.get("game_number", ""),
                "winner_team": game.get("winner_team", ""),
                "result": game.get("result", ""),
            }
            for game in _meaningful_games(summary_debug.get("games"))
        ],
    }


def _parser_owned_rows_summary(
    match_log_row: dict[str, Any] | None,
    game_log_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "match_log_row": _select_keys(match_log_row or {}, MATCH_LOG_KEYS),
        "game_log_rows": [_select_keys(row, GAME_LOG_KEYS) for row in game_log_rows],
    }


def _select_keys(row: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    return {key: row.get(key, "") for key in keys}


def _compare_expected_section(
    *,
    manifest_path: Path,
    fixture_id: str,
    section: str,
    expected: Any,
    observed: Any,
) -> list[dict[str, Any]]:
    if expected is None:
        return [
            _diff_payload(
                manifest_path=manifest_path,
                fixture_id=fixture_id,
                section=section,
                pointer=f"/expected/{section}",
                expected="[section present]",
                observed="[missing]",
            )
        ]
    diffs: list[dict[str, Any]] = []
    _compare_values(
        manifest_path=manifest_path,
        fixture_id=fixture_id,
        section=section,
        pointer=f"/expected/{section}",
        expected=expected,
        observed=observed,
        diffs=diffs,
    )
    return diffs


def _compare_values(
    *,
    manifest_path: Path,
    fixture_id: str,
    section: str,
    pointer: str,
    expected: Any,
    observed: Any,
    diffs: list[dict[str, Any]],
) -> None:
    if isinstance(expected, dict):
        if not isinstance(observed, dict):
            diffs.append(_diff_payload(manifest_path, fixture_id, section, pointer, expected, observed))
            return
        for key, expected_value in expected.items():
            key_pointer = f"{pointer}/{_json_pointer_token(str(key))}"
            if key not in observed:
                diffs.append(
                    _diff_payload(manifest_path, fixture_id, section, key_pointer, expected_value, "[missing]")
                )
                continue
            _compare_values(
                manifest_path=manifest_path,
                fixture_id=fixture_id,
                section=section,
                pointer=key_pointer,
                expected=expected_value,
                observed=observed.get(key),
                diffs=diffs,
            )
        return

    if isinstance(expected, list):
        if not isinstance(observed, list):
            diffs.append(_diff_payload(manifest_path, fixture_id, section, pointer, expected, observed))
            return
        if len(expected) != len(observed):
            diffs.append(_diff_payload(manifest_path, fixture_id, section, pointer, expected, observed))
            return
        for index, expected_value in enumerate(expected):
            _compare_values(
                manifest_path=manifest_path,
                fixture_id=fixture_id,
                section=section,
                pointer=f"{pointer}/{index}",
                expected=expected_value,
                observed=observed[index],
                diffs=diffs,
            )
        return

    if expected != observed:
        diffs.append(_diff_payload(manifest_path, fixture_id, section, pointer, expected, observed))


def _diff_payload(
    manifest_path: Path,
    fixture_id: str,
    section: str,
    pointer: str,
    expected: Any,
    observed: Any,
) -> dict[str, Any]:
    return _sanitize_report_value(
        {
            "manifest_path": _safe_repo_path(manifest_path),
            "fixture_id": fixture_id,
            "section": section,
            "json_pointer": pointer,
            "expected": expected,
            "observed": observed,
            "truth_layer": _truth_layer_for_section(section),
        }
    )


def _truth_layer_for_section(section: str) -> str:
    if section in {
        "router_stats",
        "event_family_counts",
        "event_kind_sequence",
        "parser_state",
        "final_reconciliation",
    }:
        return "parser_owned_truth"
    if section in {"diagnostics_summary", "truncation_and_data_loss", "unknowns_and_degradation"}:
        return "diagnostics_evidence"
    if section == "parser_owned_rows":
        return "parser_owned_transform_output"
    return "privacy_metadata"


def _unexpected_evidence_notes(manifest: dict[str, Any], observed: dict[str, Any]) -> list[str]:
    coverage = manifest.get("coverage") if isinstance(manifest.get("coverage"), dict) else {}
    expected_degradation = bool(coverage.get("expected_degradation") or coverage.get("expected_truncation_signals"))
    notes: list[str] = []
    unknown_count = _safe_int(observed["unknowns_and_degradation"].get("unknown_entry_count"))
    degraded_outputs = observed["unknowns_and_degradation"].get("degraded_outputs") or []
    truncation_count = _safe_int(observed["truncation_and_data_loss"].get("truncation_count"))

    if unknown_count > 0 and not expected_degradation:
        notes.append("unexpected_unknown_entries_present")
    if degraded_outputs and not expected_degradation:
        notes.append("unexpected_degraded_outputs_present")
    if truncation_count > 0 and not coverage.get("expected_truncation_signals"):
        notes.append("unexpected_truncation_or_data_loss_present")
    return notes


def _fail_result(
    manifest_path: Path,
    *,
    fixture_id: str,
    fixture_path: Path | None = None,
    privacy: dict[str, Any] | None = None,
    failures: list[str],
    review_notes: list[str] | None = None,
    degradation: list[str] | None = None,
) -> GoldenReplayFixtureResult:
    return GoldenReplayFixtureResult(
        fixture_id=fixture_id,
        status=STATUS_FAIL,
        manifest_path=manifest_path,
        fixture_path=fixture_path,
        privacy=privacy or {},
        failures=failures,
        review_notes=review_notes or [],
        degradation=degradation or [],
    )


def _suite_status(results: list[GoldenReplayFixtureResult]) -> str:
    if not results:
        return STATUS_PASS
    statuses = {result.status for result in results}
    for status in STATUS_PRECEDENCE:
        if status in statuses:
            return status
    return STATUS_FAIL


def _json_pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _safe_int(value: Any) -> int:
    try:
        if isinstance(value, bool):
            return int(value)
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _sanitize_report_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _sanitize_report_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_report_value(item) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_report_value(item) for item in value]
    if isinstance(value, Path):
        return _safe_repo_path(value)
    if isinstance(value, str):
        return sanitize_sensitive_text(value)
    return value


def _safe_repo_path(path: Path | None) -> str:
    if path is None:
        return ""
    target = Path(path)
    try:
        return str(target.resolve(strict=False).relative_to(PROJECT_ROOT.resolve(strict=False)))
    except Exception:
        return target.name or "[redacted-path]"


def _expand_manifest_paths(paths: Sequence[Path]) -> list[Path]:
    manifests: list[Path] = []
    for path in paths:
        target = Path(path)
        if target.is_dir():
            manifests.extend(sorted(target.glob("*.manifest.json")))
        else:
            manifests.append(target)
    return manifests


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Replay sanitized Player.log golden fixtures through the normal parser path."
    )
    parser.add_argument(
        "manifests",
        nargs="+",
        help="Manifest file paths, or directories containing *.manifest.json files.",
    )
    parser.add_argument("--out", dest="report_path", default="", help="Optional local JSON report output path.")
    evidence_validation_report_wiring.evidence_review_cli_arguments(parser)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    manifest_paths = _expand_manifest_paths([Path(path) for path in args.manifests])
    report = build_golden_replay_report(
        manifest_paths,
        evidence_ledger_review=evidence_validation_report_wiring.evidence_review_inputs_from_args(args),
    )
    summary = report["summary"]
    print(
        "Golden replay: "
        f"{report['suite_status']} "
        f"({summary['manifests_total']} manifests, "
        f"{summary[STATUS_PASS]} pass, "
        f"{summary[STATUS_DEGRADED]} degraded, "
        f"{summary[STATUS_REVIEW]} review, "
        f"{summary[STATUS_DIFF]} diff, "
        f"{summary[STATUS_FAIL]} fail)"
    )
    if args.report_path:
        report_path = Path(args.report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Report written: {_safe_repo_path(report_path)}")
    return 1 if report["suite_status"] in CLI_FAILURE_STATUSES else 0


if __name__ == "__main__":
    raise SystemExit(main())
