# Parser Match Summary Typed Handler Decomposition Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/461>

## Tracker

Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Contract

`docs/contracts/parser_match_summary_typed_handler_decomposition.md`

## Internal Project Area

Parser.

## Truth Owner

`src/mythic_edge_parser/app/state.py` remains the parser/state truth owner for
live `MatchSummary` / `GameSummary` mutation, parser context, rank
carry-forward, mulligan/opening-hand state, and final row-builder inputs.

## Bridge-Code Status

`shared_support`

`_update_match_summary(event)` remains the caller-facing compatibility
entrypoint used by runner and tests. The new typed handlers are private
same-file implementation details only.

## Role Performed

Codex C: Module Implementer.

## What The Code Is Supposed To Do

The parser should update match and game summaries from supported parsed event
kinds while preserving parser-owned truth, match identity, game identity,
winner reconciliation, rank carry-forward, mulligan/opening-hand state, and
changed-row behavior.

## What It Was Actually Doing

Before this implementation, `_update_match_summary(event)` handled `MatchState`,
`GameState`, `Rank`, `ClientAction`, and `GameResult` in one large shared
function. Behavior was covered by focused tests, but unrelated parser-truth
branches were visually coupled.

## Why This Was Risky

The first maintainability risk was branch adjacency: a small edit for one event
kind could accidentally affect another event kind during review. The first
runtime value that had to stay unchanged was `event.kind` dispatch behavior.

## Exact Fix

Kept `_update_match_summary(event)` as the only caller-facing dispatch function
and moved each existing branch body into a private same-file handler:

- `_handle_match_state_match_summary(event, payload)`
- `_handle_game_state_match_summary(event, payload)`
- `_handle_rank_match_summary(event, payload)`
- `_handle_client_action_match_summary(event, payload)`
- `_handle_game_result_match_summary(event, payload)`

The handlers return `None` and preserve the existing side effects. No semantic
cleanup, defensive parsing, module extraction, or caller migration was added.

## Files Changed

- `docs/contracts/parser_match_summary_typed_handler_decomposition.md`
- `src/mythic_edge_parser/app/state.py`
- `docs/implementation_handoffs/parser_match_summary_typed_handler_decomposition_comparison.md`

## Code Changed

Runtime code changed only in `src/mythic_edge_parser/app/state.py`.

No parser behavior, parser event class, match identity, game identity, final
reconciliation, extractor behavior, workbook schema, webhook payload, Apps
Script behavior, fixture, corpus metadata, CI, replay/audit, or private log
surface changed.

## Tests Added Or Updated

No tests were added or edited.

The existing focused test matrix already covered the required behavior
preservation points from the contract:

- unknown event-kind no-op behavior;
- missing identity no-op behavior;
- MatchState game and match result ingestion;
- GameState play/draw, turn count, and opening-hand handling;
- Rank alias/carry-forward and completed-summary behavior;
- ClientAction local-team correction, mulligan, submit-deck, and sideboarding
  signals;
- GameResult nested game/match result precedence and top-level fallback rules;
- live/final row update behavior;
- parser regression replay snapshots;
- runner event-loop side-effect ordering.

## Interface Changes

Caller-facing interface unchanged:

```python
_update_match_summary(event: Any) -> None
```

Private implementation helpers were added inside `state.py`. They are not a
public API and should not be imported by callers.

## Contracted Area Status

The implementation stayed inside the contracted parser/state area. No
downstream consumers or bridge-code boundaries were changed.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: not applicable; no new public data surface or
  serializer was added.
- Vocabulary and example coherence: satisfied; handler names follow the
  contract's typed-handler intent.
- Authority/readiness semantics: satisfied; no readiness, parser truth,
  reliability, release, deploy, or production claims were made.
- Fail-closed schema or validator checks: not applicable; this was a
  behavior-preserving refactor, not a validator.
- Protected-surface rollout phase: satisfied; protected runtime behavior was
  not changed, path-scoped scans were run, and the protected-surface
  authorization checker found the `state.py` change authorized by the contract.

## Validation Run

Baseline before implementation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parser_regressions.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_runner.py
```

Post-implementation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parser_regressions.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_runner.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m ruff check src/mythic_edge_parser/app/state.py tests/test_state.py tests/test_match_summary_from_match_state.py
```

Post-handoff validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_saved_event_replay.py tests/test_app_outputs.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests
PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_surface_authorization.py --base origin/main --paths-from-stdin --authorization-file contract=docs/contracts/parser_match_summary_typed_handler_decomposition.md --authorization-file handoff=docs/implementation_handoffs/parser_match_summary_typed_handler_decomposition_comparison.md
python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
git diff --check
```

## Still Unverified

- No private Player.log, UTC_Log, live MTGA, replay/audit, fixture promotion,
  or corpus status mutation was run or attempted.
- No workbook, webhook, Apps Script, local app, API, analytics, AI, release,
  deploy, or production surface was exercised.
- The new private handlers are intentionally not a durable public interface.

## Reviewer Focus

Codex E should verify:

- each moved handler body is behavior-preserving;
- `_update_match_summary(event)` still no-ops for unknown event kinds;
- missing identity behavior remains unchanged;
- no handler changes parser event classes, match/game identity, final
  reconciliation, extractor behavior, or downstream row shape;
- tests and scans are sufficient without adding new fixture or corpus changes.

## Next Workflow Action

Next role: Codex E.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #461.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/461

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source contract:
docs/contracts/parser_match_summary_typed_handler_decomposition.md

Implementation handoff:
docs/implementation_handoffs/parser_match_summary_typed_handler_decomposition_comparison.md

Review the behavior-preserving same-file decomposition of
src/mythic_edge_parser/app/state.py::_update_match_summary(event) into private
typed handlers. Verify that _update_match_summary remains the caller-facing
entrypoint, unknown events remain no-ops, match/game identity and final
reconciliation semantics do not change, and no parser event class, extractor,
workbook, webhook, Apps Script, private log, replay/audit, fixture, corpus, CI,
readiness, or parser-truth claim was introduced.

Expected output:
Findings first, validation reviewed, remaining risks, recommended next role,
and workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/461"
  completed_thread: "C"
  next_thread: "E"
  verdict: "match_summary_typed_handler_decomposition_ready_for_review"
  source_artifact: "docs/contracts/parser_match_summary_typed_handler_decomposition.md"
  target_artifact: "docs/implementation_handoffs/parser_match_summary_typed_handler_decomposition_comparison.md"
  risk_tier: "High"
  base_branch: "origin/main"
  branch: "codex/parser-match-summary-typed-handler-decomposition-461"
  same_repo_decomposition_selected: true
  cross_repo_extraction_authorized: false
  parser_behavior_change_authorized: false
  parser_event_class_change_authorized: false
  match_identity_change_authorized: false
  game_identity_change_authorized: false
  final_reconciliation_change_authorized: false
  extractor_behavior_change_authorized: false
  workbook_schema_change_authorized: false
  webhook_payload_change_authorized: false
  apps_script_behavior_change_authorized: false
  private_log_read_authorized: false
  replay_audit_authorized: false
  fixture_promotion_authorized: false
  corpus_status_mutation_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
```
