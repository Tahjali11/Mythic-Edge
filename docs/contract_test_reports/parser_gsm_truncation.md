# GSM Truncation Parser Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/107

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/parser_gsm_truncation.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Changed files reviewed:

- `src/mythic_edge_parser/__init__.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/parsers/truncation.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/transforms.py`
- `tests/test_gsm_truncation_parser.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`
- `tests/test_saved_event_replay.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_log_drift_sensor.py`
- `tests/fixtures/schema_snapshots/parser_event_classes.json`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `docs/implementation_handoffs/parser_gsm_truncation_comparison.md`

## Findings

No blocking findings.

## Contract Summary

GSM truncation/summarization markers must become parser-owned data-loss
evidence. A marker must emit a first-class `TruncationEvent` without
reconstructing omitted GameState payloads, changing workbook/webhook/App Script
surfaces, mutating parser state final reconciliation, or inferring match/game
facts. Header buffering, router dispatch, saved replay, transform inclusion,
schema snapshots, and drift reports must understand the new event while
preserving existing parser truth boundaries.

## Checks Run

```bash
python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py
python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py
python3 -m ruff check src tests
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
{ git diff --name-only; printf '%s\n' docs/contracts/parser_gsm_truncation.md docs/implementation_handoffs/parser_gsm_truncation_comparison.md src/mythic_edge_parser/parsers/truncation.py tests/test_gsm_truncation_parser.py; } | sort -u | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m pytest -q
python3 tools/select_validation.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
```

## Results

- Focused contract suite: `88 passed in 0.14s`.
- Regression/touched-surface suite: `4 passed in 0.10s`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- Protected-surface gate against committed branch diff: `changed_paths: 1`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- Explicit local changed-path protected-surface gate: `changed_paths: 19`, `forbidden: 0`, `warnings: 4`, `result: passed`.
- Full local test suite: `685 passed in 0.97s`.
- `tools/select_validation.py`: unavailable on this branch.
- `tools/check_secret_patterns.py`: unavailable on this branch.

The four explicit local protected-surface warnings are for contract-authorized
parser/event/module surfaces: `src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`, and
`src/mythic_edge_parser/parsers/truncation.py`.

## Confirmed Contract Matches

- `TruncationEvent` exists with kind `"Truncation"` and
  `PerformanceClass.INTERACTIVE_DISPATCH`.
- `GameEvent` and package exports include `TruncationEvent`.
- `src/mythic_edge_parser/parsers/truncation.py` exposes `try_parse()` and
  emits exactly one `TruncationEvent` for the sanitized explicit
  `"[Message summarized"` marker family.
- The payload includes the required data-loss evidence fields:
  `type`, `marker_family`, `affected_event_family`,
  `affected_message_type`, `data_loss`, `recoverable`,
  `parser_confidence`, `value_source`, `confidence`, `finality`,
  `drift_flag`, `source_header`, `game_object_count`,
  `annotation_count`, and `raw_marker_summary`.
- The payload does not include reconstructed game objects, annotations, raw
  GameState payloads, match/game identity, result, winner, webhook URL,
  secret, or environment-value fields.
- Count normalization is conservative: missing and malformed counts produce
  `None`, explicit zero counts produce `0`, negative counts are ignored, and
  one count is not inferred from the other.
- Event metadata raw bytes and hash are derived from `entry.body.encode()`.
- Header classification adds `EntryHeader.TRUNCATION_MARKER` with value
  `"TruncationMarker"` and multiline buffering.
- Count-only text, nearby summary prose, unrelated unknown headers, normal GRE
  parsing, and non-truncation dispatch paths are not routed as truncation.
- Router dispatch sends `EntryHeader.TRUNCATION_MARKER` only to the truncation
  parser, counts marker entries as routed, and preserves timestamp
  present/missing/malformed stats.
- GRE parsing remains sibling behavior and does not receive fabricated
  `gameStateMessage` dictionaries from truncation markers.
- Saved-event replay reconstructs `"Truncation"` records.
- Parser event class and payload snapshots include `TruncationEvent` and the
  contracted payload keys.
- `include_event()` keeps `Truncation`, `to_sheet_rows()` returns `[]`, and
  `summarize()` uses normalized payload fields only.
- Drift reports count routed `Truncation` events and no longer list the
  synthetic marker as an unknown signature.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

The focused tests cover event-class registration, parser payload shape,
metadata hashing, missing/zero/malformed count behavior, false-positive
boundaries, GRE non-promotion, header classification, multiline buffering,
router dispatch/stats/timestamps, saved replay, schema snapshots, transform
behavior, and drift-report routing.

## Drift Notes

- Repo drift: expected parser event/schema snapshot drift only, limited to the
  new `TruncationEvent` and payload keys.
- Workbook drift: none found.
- Webhook payload drift: none found.
- Apps Script drift: none found.
- Runtime status schema drift: none found.
- Failed-post schema drift: none found.
- Local-data drift: none found; tests use sanitized synthetic marker text.
- Parser truth drift: intentional and contract-authorized addition of a
  parser-owned data-loss signal. No reconstructed GameState, match identity,
  game identity, winner, or final reconciliation facts were introduced.

## Remaining Non-Blocking Gaps

- Remote CI has not run in this local Codex E pass.
- Live Arena marker variants beyond the contracted sanitized
  `"[Message summarized"` family remain unknown, as documented in the
  contract and handoff.
- `tools/select_validation.py` and `tools/check_secret_patterns.py` are absent
  from this branch and were recorded as unavailable.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for parser reliability issue #107.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Use:
- docs/contracts/parser_gsm_truncation.md
- docs/implementation_handoffs/parser_gsm_truncation_comparison.md
- docs/contract_test_reports/parser_gsm_truncation.md

Goal:
Stage only the reviewed GSM truncation parser/event/replay/test/report files, commit, push, and open or update a draft PR against codex/parser-reliability-intelligence. Do not target main.

Confirm before staging:
- No raw private Player.log excerpts, Manasight source code, secrets, webhook URLs, generated runtime artifacts, runtime status files, failed posts, or workbook exports are included.
- Workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, extractor behavior, match/game identity, deduplication, runtime status schema, failed-post schema, and workbook exports are unchanged.

Validation evidence to include:
- python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py -> 88 passed
- python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py -> 4 passed
- python3 -m ruff check src tests -> All checks passed!
- python3 -m pytest -q -> 685 passed
- python3 tools/check_protected_surfaces.py --base origin/main -> passed
- explicit local changed-path protected-surface stdin check -> passed with contract-authorized parser/event warnings only
- git diff --check -> passed

Do not stage unrelated files. Do not merge, close issue #107, mark tracker #47 complete, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/107"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_gsm_truncation.md"
  target_artifact: "docs/contract_test_reports/parser_gsm_truncation.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  verdict: "No blocking findings. Ready for Codex F."
  validation:
    - "python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py -> 88 passed"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py -> 4 passed"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "python3 -m pytest -q -> 685 passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed"
    - "explicit local changed-path protected-surface stdin check -> passed with contract-authorized warnings only"
    - "git diff --check -> passed"
    - "not run - tools/select_validation.py unavailable on this branch"
    - "not run - tools/check_secret_patterns.py unavailable on this branch"
  stop_conditions:
    - "Do not copy Manasight source code."
    - "Do not paste raw private Player.log excerpts into repo files."
    - "Do not reconstruct omitted GameState payload data."
    - "Do not infer match winner, game winner, match identity, game identity, or final reconciliation facts from truncation alone."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts committed to the repo, runtime status file schema, failed-post schema, or workbook exports."
    - "Do not target main directly; parser reliability work belongs on codex/parser-reliability-intelligence."
    - "Do not mark tracker #47 complete."
```
