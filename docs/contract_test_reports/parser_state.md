# Parser State Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/6

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_state.md`

Required role and workflow references:

- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`
- `docs/codex_module_workflow.md`

## Implementation Under Test

Current branch: `codex/parser-module-audit-suite`

Implementation file reviewed: `src/mythic_edge_parser/app/state.py`

Comparison artifact reviewed: `docs/implementation_handoffs/parser_state_comparison.md`

Focused tests reviewed:

- `tests/test_state.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_parser_regressions.py`
- `tests/test_saved_event_replay.py`
- related row-shape checks in `tests/test_app_models.py` and `tests/test_sheet_schema.py`

## Contract Summary

`state.py` must remain the parser-owned runtime state and event-ingestion layer. It owns current match/game/player context, rank carry-forward, match/game summary mutation, mulligan and hand capture, live/final row readiness, changed-field detection, and posted-row dedupe snapshots. It must preserve parser truth ownership and must not move workbook/webhook/schema/final-reconciliation behavior downstream.

## Checks Run

```powershell
gh issue view 6 --json number,title,body,state,author,url,labels,comments
git status --short
python -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_parser_regressions.py tests/test_saved_event_replay.py
python -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py
ruff check src tests
PYTHONPATH=src python - <<'PY'
from datetime import UTC, datetime
from mythic_edge_parser.app import state
from mythic_edge_parser.events import EventMetadata, MatchStateEvent

class UnknownEvent:
    kind = 'UnknownKind'
    payload = {'match_id': 'ghost'}
    metadata = EventMetadata(datetime(2026, 5, 12, tzinfo=UTC), b'raw')

state.reset_runtime_state()
state._update_match_summary(UnknownEvent())
print('unknown_summaries', dict(state._MATCH_SUMMARIES))

state.reset_runtime_state()
missing = MatchStateEvent(EventMetadata(datetime(2026, 5, 12, tzinfo=UTC), b'raw'), {'type': 'match_started'})
state._update_match_summary(missing)
print('missing_matchstate_summaries', dict(state._MATCH_SUMMARIES))

state.reset_runtime_state()
started = MatchStateEvent(
    EventMetadata(datetime(2026, 5, 12, tzinfo=UTC), b'raw'),
    {'type': 'match_started','match_id':'m_copy','players':[{'player_name':'Local','team_id':1},{'player_name':'Opp','team_id':2}]},
)
state._update_match_summary(started)
row, _, _ = state.build_match_log_update('m_copy')
state.mark_match_log_posted('m_copy', row)
row['MTGA Match ID'] = 'mutated'
print('posted_match_id_copy', state._LAST_POSTED_MATCH_LOG_ROWS['m_copy']['MTGA Match ID'])
PY
python -m pytest -q
```

## Results

Module Fixer follow-up completed for the revised GameResult final
reconciliation contract.

Focused GameResult reconciliation validation passed:

```text
32 passed in 0.10s
```

Focused parser-state validation passed:

```text
30 passed in 0.12s
```

Related model/schema validation passed:

```text
12 passed in 0.04s
```

Ruff passed:

```text
All checks passed!
```

Additional probes confirmed representative required behavior:

```text
unknown_summaries {}
missing_matchstate_summaries {}
posted_match_id_copy m_copy
```

Full repo validation found one known unrelated failure:

```text
1 failed, 324 passed
```

The failing test was the known unrelated
`tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook`
local path-sanitization failure. Runner changes are not part of this
parser-state GameResult contract PR.

## Confirmed Contract Matches

- `ParserRuntimeState` owns the containers and scalar state named by the contract, and `RUNTIME_STATE` remains the live singleton in `src/mythic_edge_parser/app/state.py:33`.
- Mutable compatibility aliases point at `RUNTIME_STATE` containers in `src/mythic_edge_parser/app/state.py:70`, including context, summaries, posted snapshots, mulligan counts, gameplay card state, and hand snapshot state.
- `reset_runtime_state()` clears mutable containers in place, restores default context, resets rank/card/log scalar state, and preserves `RUNTIME_STATE` object ownership in `src/mythic_edge_parser/app/state.py:414`.
- Direct focused tests now cover alias identity and scalar reset behavior for `reset_runtime_state()`.
- Rank events normalize and store latest rank state, seed the next created summary, and avoid overwriting completed ready summaries through `set_last_posted_rank()`, `_store_latest_rank_snapshot()`, `_seed_summary_with_latest_rank()`, and the Rank branch in `src/mythic_edge_parser/app/state.py:127`, `src/mythic_edge_parser/app/state.py:154`, `src/mythic_edge_parser/app/state.py:198`, and `src/mythic_edge_parser/app/state.py:529`.
- Unknown event kinds are no-ops because `_update_match_summary()` only mutates inside known-kind branches; a probe left `_MATCH_SUMMARIES` empty.
- Direct focused tests now cover unknown event kinds as complete no-ops.
- MatchState, GameState, ClientAction, and GameResult identity gates are present where the contract requires them, including early returns for missing match identity in `src/mythic_edge_parser/app/state.py:468`, `src/mythic_edge_parser/app/state.py:506`, `src/mythic_edge_parser/app/state.py:551`, and `src/mythic_edge_parser/app/state.py:601`.
- Direct focused tests now cover missing-identity no-op behavior for MatchState, GameState, ClientAction, and GameResult.
- MatchState handling creates summaries on demand, updates context, touches timestamps, preserves/updates event ID, infers local team, assigns game-scope winners by order, and separates match-scope winner fields in `src/mythic_edge_parser/app/state.py:468`.
- GameState handling uses payload plus context fallback, touches match/game state, allows local-team correction, ingests game info, infers starting player, advances turn count, and records opening-hand candidates in `src/mythic_edge_parser/app/state.py:506`.
- ClientAction handling requires current match context, touches summaries, corrects local team, updates mulligan counts, captures discarded mulligan hands before non-keep increments, and handles submit-deck/sideboarding/starting-player actions in `src/mythic_edge_parser/app/state.py:551`.
- GameResult handling keeps game winner and match winner distinct, uses context fallback, ingests game info, touches game state, and marks match completion only when completion markers or match-scope results exist in `src/mythic_edge_parser/app/state.py:601`.
- GameResult final reconciliation now uses the latest known nested `MatchScope_Game` winner for game winners.
- GameResult final reconciliation now prefers the latest known nested `MatchScope_Match` winner, result type, and reason for match finalization.
- Top-level match winner fallback now occurs only when no nested match-scope winner exists and `match_state == "MatchState_MatchComplete"`.
- Winner values `None`, `""`, `0`, and `"0"` are treated as unknown and do not set or overwrite game or match winners.
- Hand and mulligan capture preserve placeholders internally, suppress duplicate consecutive hand snapshots, infer bottomed cards from a longer prior snapshot once per game key, and rely on model serialization to hide unresolved exact-card workbook fields in `src/mythic_edge_parser/app/state.py:259`, `src/mythic_edge_parser/app/state.py:284`, and `src/mythic_edge_parser/app/state.py:306`.
- Direct focused tests now cover consecutive duplicate hand snapshot suppression and once-only bottomed-card capture.
- Live/final readiness is distinct: final match summary and match log rows require `summary.is_ready()`, live match log rows can emit earlier, match updates switch from live to final at readiness, and game finality is per row based on non-empty `Game Result` in `src/mythic_edge_parser/app/state.py:663`, `src/mythic_edge_parser/app/state.py:689`, `src/mythic_edge_parser/app/state.py:696`, `src/mythic_edge_parser/app/state.py:703`, and `src/mythic_edge_parser/app/state.py:722`.
- Direct focused tests now cover live/final row builder readiness and withholding behavior.
- Changed-field detection compares only schema sync fields, ignores blank first-post values, and rounds floats before comparison in `src/mythic_edge_parser/app/state.py:634`.
- Direct focused tests now cover non-sync-field changes being ignored and float rounding suppressing insignificant churn.
- `mark_match_log_posted()` and `mark_game_log_posted()` store row copies with `dict(row)`, and the probe confirmed caller mutation does not alter the stored match row snapshot in `src/mythic_edge_parser/app/state.py:718` and `src/mythic_edge_parser/app/state.py:745`.
- Direct focused tests now cover copy semantics for both match-log and game-log posted-row snapshots.
- Observation APIs expose live summary lookup, list snapshots, the runtime singleton, and context copies in `src/mythic_edge_parser/app/state.py:752`.
- Direct focused tests now cover `iter_match_summaries()` list snapshots and `get_context_snapshot()` shallow-copy behavior.

## Contract Mismatches

Resolved by Module Fixer follow-up:

- The prior implementation used top-level `winning_team_id` for match
  finalization once `_has_match_scope_result(payload)` indicated a match result
  existed. The revised contract requires nested match-scope winner precedence,
  and the implementation now follows that rule.
- `build_game_result_payload()` no longer promotes a match-scope result into
  top-level game-winner fields when no valid game-scope result exists.

## Missing Tests

Resolved by Module Fixer follow-up:

- Unknown event kinds are tested as complete no-ops.
- MatchState, GameState, ClientAction, and GameResult missing-identity branches are directly tested to prove they do not create anonymous summaries.
- `reset_runtime_state()` asserts alias object identity before/after reset and confirms `RUNTIME_STATE` itself is not replaced.
- Reset coverage directly asserts `RUNTIME_STATE.current_log_date`, `RUNTIME_STATE.current_log_path`, latest rank fields, and lookup-readiness scalar fields.
- `mark_match_log_posted()` and `mark_game_log_posted()` each have copy-semantics tests that mutate the caller row after marking posted.
- Changed-field detection directly tests non-sync-field changes are ignored and float normalization suppresses insignificant churn.
- Invalid `mark_game_log_posted()` keys and invalid game numbers in game-log update paths are directly tested as no-ops/skips.
- `build_live_match_log_row()` and `build_match_summary_row()` have direct readiness/withholding tests.
- `iter_match_summaries()` is tested as a list snapshot and `get_context_snapshot()` as a shallow copy.
- Context fallback has narrow GameState and GameResult tests where identity fields are omitted after context is established.
- Hand snapshot history has a narrow test for consecutive duplicate suppression and once-only bottomed-card capture.

Resolved by Module Fixer follow-up after contract revision:

- GameResult nested match-scope variants now have focused parser and state
  coverage.

## Drift Notes

- Repo drift: Module Fixer changed parser-owned code for the contracted
  GameResult winner precedence rule, added focused tests, and updated
  parser-state handoff/report docs.
- Workbook schema drift: not inspected; no workbook schema files changed in this review.
- Webhook payload shape drift: not inspected live; no webhook transport files changed in this review.
- Apps Script deployment drift: deployed Apps Script was not inspected; `tools/google_apps_script/Code.gs` was not changed.
- Local environment drift: the known unrelated runner path-sanitization failure
  reproduced in full-suite validation and remains outside this parser-state PR
  scope.

## Prohibited-Surface Confirmation

No workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, deduplication behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports were changed by this Module Fixer follow-up. Final reconciliation changed only within the contracted parser-owned GameResult winner precedence rule.

Files changed by the Module Fixer follow-up:

- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `tests/test_gre_game_result_parser.py`
- `tests/test_state.py`
- `docs/implementation_handoffs/parser_state_comparison.md`
- `docs/contract_test_reports/parser_state.md`

## Recommendation

Route to Module Submitter.

The revised GameResult final reconciliation rule has been implemented and
reviewed with focused parser and state tests. No blocking contract-test findings
remain for the reviewed parser-state scope.

## Next Workflow Action

Next role: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Submitter thread for https://github.com/Tahjali11/Mythic-Edge/issues/6, docs/contracts/parser_state.md, docs/implementation_handoffs/parser_state_comparison.md, and docs/contract_test_reports/parser_state.md.

Submit the reviewed parser-state GameResult contract-audit work to a draft PR targeting codex/parser-module-audit-suite. Stage only intended parser-state GameResult contract files, tests, and docs. Do not target main. Do not stage unrelated runner.py or test_runner.py changes. Do not stage local secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/6"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_state.md"
  target_artifact: "draft PR/update on codex/parser-module-audit-suite"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_match_summary_from_match_state.py -> 32 passed"
    - "python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_parser_regressions.py tests/test_saved_event_replay.py -> 30 passed"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py -> 12 passed"
    - "python3 -m ruff check src tests -> All checks passed"
    - "python3 -m pytest -q -> 1 failed, 324 passed; known unrelated runner path-sanitization failure"
  stop_conditions:
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Stage only intended parser-state GameResult contract files, tests, and docs."
    - "Do not stage unrelated runner.py or test_runner.py changes with this parser-state PR."
    - "Do not stage local secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
```
