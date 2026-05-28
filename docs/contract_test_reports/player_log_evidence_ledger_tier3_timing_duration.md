# Player.log Evidence Ledger Tier 3 Timing And Duration Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/147

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

- Branch: `codex/player-log-evidence-ledger-tier3-timing-duration`
- Base branch: `codex/parser-reliability-intelligence`
- Previous merge commit: `0aede4890710768c7abd2fb2a561c7ce8b10fdba`
- Changed implementation files:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `tests/test_evidence_ledger.py`
  - `docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md`
  - `docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md`

## Findings

No blocking findings.

## Contract Summary

Issue #147 maps Tier 3 game timing and duration provenance in the Player.log
evidence ledger. The implementation must add metadata and focused tests for
six game timing entries and three game duration entries, define timing as
parser observation-boundary endpoints rather than Arena internal start/end
times, define duration as `GameSummary.duration_seconds()` derived from those
endpoints, remove broad `game_timing` and `game_duration` future placeholders,
preserve prior #134, #137, #139, #140, #143, and #145 entries, and avoid
parser/runtime/workbook/webhook or Apps Script behavior changes.

## Checks Run

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_state.py tests/test_app_models.py tests/test_match_summary_from_match_state.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
printf 'docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md\nsrc/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
PYTHONPATH=src python3 - <<'PY'
from mythic_edge_parser.app import evidence_ledger
ledger = evidence_ledger.build_player_log_evidence_ledger()
families = {f["output_family"]: f for f in ledger["output_families"]}
entries = {e["entry_id"]: e for e in evidence_ledger.iter_ledger_entries()}
ids = [
    *(f"tier3.game_timing.game{i}_first_event_time" for i in (1, 2, 3)),
    *(f"tier3.game_timing.game{i}_last_event_time" for i in (1, 2, 3)),
    *(f"tier3.game_duration.game{i}_duration_seconds" for i in (1, 2, 3)),
]
print("future_game_timing:", "game_timing" in families["game_level_facts"]["future_fields"])
print("future_game_duration:", "game_duration" in families["game_level_facts"]["future_fields"])
for entry_id in ids:
    entry = entries[entry_id]
    print(entry_id, "errors=", evidence_ledger.validate_ledger_entry(entry))
print("ledger_errors=", evidence_ledger.validate_player_log_evidence_ledger())
PY
```

## Results

- `tests/test_evidence_ledger.py`: passed, `55 passed in 0.21s`
- Adjacent state/model/match-summary tests: passed, `42 passed in 0.10s`
- Full pytest: passed, `914 passed in 1.31s`
- Ruff: passed, `All checks passed!`
- `git diff --check`: passed with no output
- Full protected-surface gate against `origin/main`: passed, `forbidden: 0`, `warnings: 12`
- #147 path-scoped protected-surface gate: passed, `forbidden: 0`, `warnings: 0`
- Ledger introspection: broad `game_timing` and `game_duration` are absent
  from Tier 3 future fields, all nine timing/duration entries validate
  cleanly, and the full ledger validates cleanly.

## Confirmed Contract Matches

- `game_level_facts.seed_fields` includes all nine contracted fields:
  `game1_first_event_time`, `game2_first_event_time`,
  `game3_first_event_time`, `game1_last_event_time`,
  `game2_last_event_time`, `game3_last_event_time`,
  `game1_duration_seconds`, `game2_duration_seconds`, and
  `game3_duration_seconds`.
- Broad `game_timing` and `game_duration` are removed from
  `game_level_facts.future_fields`, while `pre_postboard`, `sideboarding`,
  and `deck_state` remain deferred.
- All six `tier3.game_timing.*` entries exist and validate.
- All three `tier3.game_duration.*` entries exist and validate.
- Timing entries document first/latest observed parser event endpoints as
  parser observation boundaries, not Arena internal start/end times.
- Direct timing evidence cites GameState, ClientAction, GameResult event
  timestamps, and parser-state first/last endpoint surfaces.
- Timing fallback evidence cites router timestamp-missing counters, router
  timestamp-parse-failure counters, `_safe_iso(...)` runtime-clock fallback,
  and game-slot identity dependency.
- Duration entries document `GameSummary.duration_seconds()` and first/last
  endpoint dependencies.
- Duration fallback evidence cites clamp behavior and timestamp anomaly
  context.
- Blank duration is documented as unknown/unavailable, not zero.
- Zero duration is documented as reviewable when endpoints are equal or
  out-of-order and clamped.
- Timing/duration value-source policy uses observed, derived, unknown, and
  conflict; `inferred` and `legacy_enriched` are not used as timing/duration
  truth paths.
- #134 game-result, #137 participant/player-team, #139 play/draw, #140
  mulligan, #143 opening-hand, and #145 turn-count entries remain present and
  covered by focused tests.
- All new evidence signals are path-only and do not embed raw player values,
  raw logs, raw GameState payloads, raw timestamps from private logs, local
  artifacts, generated data, secrets, or workbook exports.
- No parser behavior, timestamp parsing, duration calculation, state update
  behavior, GameState parsing, turn-info parsing, extractor behavior, parser
  state final reconciliation, parser event classes, workbook schema, webhook
  payload shape, Apps Script behavior, output transport, match/game identity,
  deduplication, secrets, environment variables, raw logs, generated data,
  runtime status files, failed posts, workbook exports, production behavior,
  environment variable contracts, or AI/analytics truth changed in this slice.

## Contract Mismatches

None found.

## Missing Tests

None found for the #147 contract. Focused tests cover entry existence,
validation, seed/future field movement, direct and fallback evidence signals,
runtime-clock fallback degradation, row timestamp fallback reviewability,
duration endpoint dependencies, clamp behavior, blank-versus-zero semantics,
no inferred or legacy-enriched timing/duration truth path, prior entry
preservation, privacy class, and remaining deferred scope.

## Drift Notes

- Repo drift: none found in the #147 slice.
- Workbook schema drift: none found.
- Webhook payload drift: none found.
- Apps Script drift: none found.
- Parser/runtime behavior drift: none found.
- Local-data drift: none found.
- Protected-surface note: the full branch comparison to `origin/main` reports
  12 warnings from accumulated parser-reliability integration branch changes,
  but the path-scoped #147 gate reports `forbidden: 0`, `warnings: 0`.

## Recommendation

Approve for Codex F: Module Submitter.

## Remaining Non-Blocking Gaps

- Runtime field-evidence attachment remains intentionally deferred.
- Drift reports, schema snapshots, diagnostics reports, replay reports,
  feature-equity reports, timing analytics, clock-pressure analytics, and
  invariant execution remain intentionally deferred.
- `_safe_iso(...)` runtime-clock fallback remains current behavior and is
  documented as degraded/review-required rather than repaired in this issue.
- This metadata does not prove individual live matches have clean timestamp
  evidence; it documents the parser-owned provenance contract for future
  evidence attachment.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #147, Tier 3 timing/duration provenance under issue #11.

Submit the reviewed metadata/test-only package from branch codex/player-log-evidence-ledger-tier3-timing-duration into base branch codex/parser-reliability-intelligence.

Use:
- docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier3_timing_duration.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py

Codex E found no blocking findings. Validation passed:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_state.py tests/test_app_models.py tests/test_match_summary_from_match_state.py
- python3 -m pytest -q
- python3 -m ruff check src tests tools
- git diff --check
- python3 tools/check_protected_surfaces.py --base origin/main
- path-scoped protected-surface gate for #147 files

Stage only the reviewed #147 files, commit, push, and open or update a draft PR to codex/parser-reliability-intelligence. Do not target main. Do not merge. Do not close issue #11 or issue #147. Do not include unrelated local files or protected artifacts.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/147"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/145"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/146"
  previous_merge_commit: "0aede4890710768c7abd2fb2a561c7ce8b10fdba"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md"
  target_artifact: "draft PR to codex/parser-reliability-intelligence"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-timing-duration"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_app_models.py tests/test_match_summary_from_match_state.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "path-scoped protected-surface gate for #147 files -> forbidden: 0, warnings: 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #147."
    - "Do not change parser behavior, timestamp parsing, duration calculation, state update behavior, GameState parsing, turn-info parsing, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not rework, remove, or weaken prior Tier 3 provenance entries."
    - "Do not map pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshots, invariant execution, or runtime field-evidence attachment beyond what the #147 contract explicitly requires."
    - "Do not infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, clock-pressure analysis, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```
