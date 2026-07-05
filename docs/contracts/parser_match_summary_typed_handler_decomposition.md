# Parser Match Summary Typed Handler Decomposition Contract

## Module

Behavior-preserving decomposition of
`src/mythic_edge_parser/app/state.py::_update_match_summary(event)` into typed
match-summary transition handlers.

This is a Codex B contract artifact only. It does not implement code, move
code, change parser behavior, open a PR, change CI, read private logs, run
replay/audit recovery, or claim readiness.

## Source Issue

https://github.com/Tahjali11/Mythic-Edge/issues/461

## Tracker

Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568

Related governance:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`

## Owning Layer

Parser and state interpretation.

`state.py` owns live parser context, parser-owned `MatchSummary` /
`GameSummary` mutation, final reconciliation inputs, rank carry-forward,
mulligan/opening-hand support state, changed-field row update decisions, and
the compatibility surfaces consumed by runner/tests.

Workbook formulas, webhook transport, Apps Script, local UI, analytics, AI, and
tests remain consumers or validation surfaces. They do not become parser truth
owners through this decomposition.

## Internal Project Area

Primary internal project area: `Parser`.

Classification: `clear_owner` for `src/mythic_edge_parser/app/state.py` and
its parser-state tests.

Bridge-code status: `shared_support`.

Reason: `_update_match_summary(event)` is parser-truth code, but it is also an
internal-public compatibility surface used by `runner.py`, tests, and replay
validation. The decomposition must preserve the bridge while making event-kind
branches easier to review.

## Truth Owner

Truth owner: `src/mythic_edge_parser/app/state.py`.

The decomposition may change internal function boundaries only. It must not
change:

- which event kinds are recognized;
- which payload fields are read;
- current match ID or current game number fallback behavior;
- local player team selection;
- game winner or match winner precedence;
- final reconciliation behavior;
- row readiness;
- changed-field detection;
- posted-row snapshot behavior;
- rank carry-forward semantics;
- mulligan count or hand snapshot semantics;
- sideboarding or submit-deck flags.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_match_summary_typed_handler_decomposition.md`

Future Codex C implementation may edit only after review approval:

- `src/mythic_edge_parser/app/state.py`
- focused tests that already cover parser state behavior, especially:
  - `tests/test_state.py`
  - `tests/test_match_summary_from_match_state.py`
  - `tests/test_parser_regressions.py`
  - `tests/test_runner.py`
  - `tests/test_gre_game_result_parser.py`

Referenced but not owned by this contract:

- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `tools/google_apps_script/Code.gs`

## Observed Current Behavior

`_update_match_summary(event)` currently:

1. Reads `event.kind`.
2. Reads `event.payload`, defaulting missing payload to `{}`.
3. Uses a sequence of event-kind branches:
   - `MatchState`
   - `GameState`
   - `Rank`
   - `ClientAction`
   - `GameResult`
4. Mutates parser runtime state and `MatchSummary` / `GameSummary` objects in
   place.
5. Returns `None` for every path.
6. Ignores unknown event kinds.

Current branch responsibilities:

| Branch | Current behavior |
| --- | --- |
| `MatchState` | Resolve match ID from payload or context, create/touch summary, set event ID, infer local team, ingest sequential game results, ingest match-scope result, set game number to 1 on `match_started`. |
| `GameState` | Resolve match/game/turn from payload or context, create/touch summary, set local team from GameState, ingest game info, update current game number, touch game, record starting player, turn count, and opening-hand candidate. |
| `Rank` | Normalize rank fields, update last-posted/latest rank snapshot, apply rank to current incomplete summary only, otherwise carry forward to the next summary. |
| `ClientAction` | Require current match context, touch current game, correct local team, handle mulligan responses, submit-deck signals, sideboarding signals, generic starting-player responses, and generic mulligan responses. |
| `GameResult` | Resolve match/game/winner from payload or context, ingest game info, preserve current player team, touch game, prefer nested game-scope winner for game winner, prefer nested match-scope result for match finalization, and fall back to top-level match winner only on `MatchState_MatchComplete`. |

Unknown event kinds are complete no-ops and must remain complete no-ops.

## Problem Statement And First Bad Value

Problem: `_update_match_summary(event)` concentrates several parser-truth
state transitions in one shared-context function. The current behavior is
covered by focused tests, but the function shape increases review risk because
changes to one event kind are visually adjacent to unrelated event-kind
semantics.

First bad value:

- The first maintainability failure point is the mixed event-kind branch block
  inside `src/mythic_edge_parser/app/state.py::_update_match_summary`.
- The first runtime value that must not change is `event.kind` dispatch
  behavior.
- The first parser-truth value that must not drift is the match/game identity
  and winner reconciliation produced by the same event sequence before and
  after decomposition.

## Scope Decision

Decision: same-repo, same-package, behavior-preserving decomposition.

Codex C may split the body of `_update_match_summary(event)` into private typed
handlers while keeping `_update_match_summary(event)` as the only supported
ingestion entrypoint for callers.

Recommended first implementation shape:

```text
_update_match_summary(event)
  -> _handle_match_state_match_summary(event, payload)
  -> _handle_game_state_match_summary(event, payload)
  -> _handle_rank_match_summary(event, payload)
  -> _handle_client_action_match_summary(event, payload)
  -> _handle_game_result_match_summary(event, payload)
```

The handler names may vary if Codex C finds a clearer local naming pattern, but
the handlers must remain private, same-repo, and behavior-preserving.

First pass should keep handlers in `state.py` unless Codex C proves that a new
same-package module reduces risk without circular imports or import churn. A
new module is allowed only inside `src/mythic_edge_parser/app/`, only for these
private handlers, and only if `_update_match_summary(event)` remains the caller
entrypoint.

Cross-repo extraction is not authorized.

## Decomposition Decision Packet

| Field | Decision |
| --- | --- |
| Candidate | `_update_match_summary(event)` typed event-kind branches. |
| Current path | `src/mythic_edge_parser/app/state.py`. |
| Current behavior | Mutates parser-owned `MatchSummary` / `GameSummary` state from parsed event objects. |
| Truth owner | Parser/state layer, specifically `state.py`. |
| Upstream dependencies | Parsed event objects, event payloads, extractor helpers, context state, rank helpers, hand/mulligan helpers, `MatchSummary` methods. |
| Downstream consumers | `runner.py`, output builders, transforms, local runtime surfaces, tests, workbook/webhook transport through parser-produced rows. |
| Proposed destination | Same repository, same parser package, private typed handlers behind `_update_match_summary(event)`. |
| Why not keep as one function | Keeping all event-kind transitions in one function preserves runtime behavior but keeps review burden high and makes unrelated parser-truth edits harder to isolate. |
| Why not move to an existing sibling repo | The boundary depends on mutable in-process parser state, private helpers, and parser-owned models. It is not independently versionable or separately governed. |
| Why not create a new repo | Cross-repo extraction would add dependency/versioning/CI/branch risk while the interface is not stable or independently testable outside Mythic Edge. |
| New public interface | None. `_update_match_summary(event)` remains the caller-facing interface. |
| New private interface | One private handler per supported `event.kind`, returning `None` and preserving current side effects. |
| Behavior-preservation tests | Focused state, match-summary, runner-order, GameResult, and parser-regression tests listed below. |
| Rollback plan | Inline handler bodies back into `_update_match_summary(event)` or revert the refactor commit. No migration or data rollback should be required because behavior and public interfaces must not change. |
| Decision | `same_repo_same_package_private_handlers_first`; cross-repo extraction is rejected for this issue. |

## Typed Handler Boundary

Each handler should own one event-kind transition and no unrelated branch.

Required handler invariants:

- Input: the original event object and the normalized payload dict used today.
- Output: `None`.
- Side effects: exactly the same state mutations currently performed by that
  event-kind branch.
- No handler may call workbook, webhook, Apps Script, analytics, AI, network,
  filesystem, private log, or CI surfaces.
- No handler may change event classes, payload shape, match identity, game
  identity, deduplication, row serialization, or final reconciliation.
- No handler may catch broad exceptions to hide parser-state bugs.
- No handler may convert unknown event kinds into supported behavior.

Suggested private handler responsibilities:

| Handler | Allowed responsibility |
| --- | --- |
| MatchState handler | Existing MatchState branch only. |
| GameState handler | Existing GameState branch only. |
| Rank handler | Existing Rank branch only. |
| ClientAction handler | Existing ClientAction branch only. |
| GameResult handler | Existing GameResult branch only. |

`_update_match_summary(event)` remains the dispatch function. It should contain
only:

- event kind lookup;
- payload defaulting;
- typed handler dispatch;
- no-op handling for unknown kinds.

## Invariants

Behavior must be identical before and after Codex C implementation for:

- unknown event no-op behavior;
- missing identity no-op behavior;
- context fallback for `GameState` and `GameResult`;
- MatchState game-result indexing;
- MatchState match-scope result handling;
- GameState game info ingestion;
- GameState turn count handling;
- GameState opening-hand candidate recording;
- Rank normalization and carry-forward;
- Rank not overwriting completed summaries;
- ClientAction local-team correction;
- ClientAction mulligan count and discarded-hand recording;
- ClientAction generic starting-player handling;
- ClientAction sideboarding and submit-deck flags;
- GameResult nested game-scope winner precedence;
- GameResult nested match-scope winner precedence;
- GameResult top-level match winner fallback only for match completion;
- unknown winner handling;
- `MatchSummary.is_ready()` behavior;
- live/final match log row behavior;
- game log row finality;
- changed-field detection;
- posted-row snapshot copy behavior;
- reset and alias identity behavior.

## Public Interface

Caller-facing interface preserved:

```python
_update_match_summary(event: Any) -> None
```

Compatibility expectation:

- `runner.py` continues importing and calling `_update_match_summary(event)`.
- Tests may continue calling `_update_match_summary(event)` directly.
- No caller is required to import typed handlers.
- New handlers, if introduced, are private implementation details and should
  not be treated as durable public API.

## Inputs

Allowed inputs:

- already-parsed public-safe event objects;
- synthetic events in tests;
- committed sanitized fixtures already allowed by existing tests;
- current in-memory parser runtime state;
- existing helper outputs inside `state.py`, `extractors.py`, and `models.py`.

Forbidden inputs:

- private `Player.log` content;
- private `UTC_Log` content;
- raw log lines or raw JSON payload bodies outside existing committed tests;
- live MTGA data;
- private replay/audit artifacts;
- workbook exports;
- generated local SQLite databases;
- provider/model outputs;
- secrets, credentials, tokens, API keys, webhook URLs, or local-only paths.

## Outputs

Allowed outputs:

- same in-memory parser state mutations as current `_update_match_summary`;
- same existing row-builder outputs through existing builders;
- same test assertions and validation evidence.

Forbidden outputs:

- new persisted artifacts;
- new runtime logs or reports;
- new issue/PR artifacts;
- new workbook rows, webhook payload fields, Apps Script fields, analytics
  fields, AI summaries, fixtures, expected-output files, or corpus metadata.

## Error Behavior

The decomposition must preserve current branch error behavior.

Specific requirements:

- unknown event kinds remain no-op;
- missing match identity remains no-op for branches that currently require it;
- missing rank text remains no-op;
- unsupported ClientAction message types remain no-op after touching only the
  state currently touched today;
- malformed payload behavior must not be broadened or hidden unless a later
  contract explicitly authorizes defensive parsing changes;
- exceptions must not be swallowed through generic handler wrappers.

If Codex C discovers behavior that is unsafe to preserve, it must stop and
route back to Codex B or Codex A rather than fixing semantics inside this
decomposition.

## Side Effects

Allowed side effects for future Codex C:

- in-memory state mutations already performed by `_update_match_summary`;
- test-only assertions for behavior parity;
- implementation handoff documentation.

Forbidden side effects:

- code execution during Codex B;
- private log reads;
- replay/audit recovery;
- fixture promotion;
- corpus status mutation;
- workbook, webhook, Apps Script, analytics, AI, local app, CI, release,
  deploy, or production behavior changes.

## Dependency Order For Codex C

1. Inspect current `state.py` and focused tests.
2. Add or confirm a behavior-parity test matrix before moving code if gaps are
   found.
3. Extract one event-kind branch at a time into a private handler.
4. Keep `_update_match_summary(event)` as dispatch.
5. Run focused tests after the mechanical split.
6. Write `docs/implementation_handoffs/parser_match_summary_typed_handler_decomposition_comparison.md`.
7. Route to Codex E.

Codex C should prefer a two-pass refactor:

1. Move code into private handlers without changing behavior.
2. Defer any cleanup, semantic improvement, naming migration, or module
   extraction to a later issue if review identifies value.

## Compatibility

The following must remain compatible:

- `_update_match_summary(event)` import path and signature;
- module-level state aliases;
- `ParserRuntimeState` shape unless no code change requires it;
- `RUNTIME_STATE` singleton behavior;
- reset behavior;
- row-builder and mark-posted helper signatures;
- current tests that call private state helpers directly;
- runner event-loop ordering.

Typed handlers are not compatibility surfaces unless a future contract makes
them public.

## Behavior-Preservation Tests

Minimum Codex C validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parser_regressions.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_runner.py
python3 tools/check_agent_docs.py
printf '%s\n' src/mythic_edge_parser/app/state.py tests/test_state.py tests/test_match_summary_from_match_state.py docs/implementation_handoffs/parser_match_summary_typed_handler_decomposition_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

Add focused tests before implementation if Codex C finds a handler branch is
not pinned by existing tests.

Recommended additional validation when feasible:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_saved_event_replay.py tests/test_app_outputs.py
```

No private logs, live MTGA data, replay/audit recovery, fixture promotion, or
corpus metadata mutation are allowed for validation.

## Acceptance Criteria

This contract is satisfied when:

- the contract exists at
  `docs/contracts/parser_match_summary_typed_handler_decomposition.md`;
- the decomposition decision packet chooses same-repo/same-package private
  handlers and rejects cross-repo extraction for issue #461;
- the typed-handler boundary preserves `_update_match_summary(event)` as the
  caller-facing interface;
- behavior-preservation invariants are explicit and testable;
- Codex C implementation scope is narrow and mechanical;
- validation expectations include focused parser-state tests and protected
  surface scans;
- protected boundaries remain false;
- next role routes to Codex C after review, not directly to submitter.

## Rollback Plan

Because the future implementation must be behavior-preserving and must not
change public interfaces, rollback should be simple:

1. Revert the implementation commit, or inline each private handler body back
   into `_update_match_summary(event)`.
2. Re-run the same focused tests.
3. Confirm no fixtures, persisted artifacts, corpus metadata, workbook schema,
   webhook payloads, Apps Script code, or CI config need rollback.

If rollback requires data migration, fixture mutation, corpus mutation, or
downstream workbook/webhook changes, the implementation exceeded this contract.

## Out Of Scope And Non-Claims

This contract does not authorize:

- code implementation during Codex B;
- opening a PR;
- parser behavior changes;
- parser event class changes;
- match identity changes;
- game identity changes;
- final reconciliation changes;
- extractor behavior changes;
- workbook schema changes;
- webhook payload shape changes;
- Apps Script behavior changes;
- analytics, AI, coaching, local app, release, deploy, or production behavior;
- private log reads;
- replay/audit recovery;
- fixture promotion;
- corpus status mutation;
- CI changes;
- cross-repo extraction;
- readiness, parser truth, reliability readiness, release readiness, deploy
  readiness, or production readiness claims.

No claim is made that this decomposition is complete, that parser behavior is
ready, that reliability is ready, or that Phase 5 is complete.

## Recommended Next Role

Recommended next role: Codex E review.

After Codex E finds no blocking contract issues, route to Codex C for the
behavior-preserving implementation.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic-Edge issue #461.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/461

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source artifact:
docs/contracts/parser_match_summary_typed_handler_decomposition.md

Review the behavior-preserving decomposition contract and decomposition
decision packet for splitting
src/mythic_edge_parser/app/state.py::_update_match_summary(event) into typed
match-summary transition handlers.

Verify that the contract:
- preserves parser truth ownership;
- preserves _update_match_summary(event) as the caller-facing interface;
- chooses same-repo/same-package private handlers first;
- rejects cross-repo extraction for issue #461;
- forbids parser behavior, event class, match/game identity, final
  reconciliation, extractor, workbook, webhook, Apps Script, private log,
  replay/audit, fixture, corpus, CI, readiness, and production changes;
- gives Codex C a testable behavior-preserving implementation boundary.

Expected output:
- Findings first, ordered by severity.
- Whether the contract is ready for Codex C.
- Validation expectations.
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/461"
  completed_thread: "B"
  next_thread: "E"
  verdict: "match_summary_typed_handler_decomposition_contract_ready_for_review"
  target_artifact: "docs/contracts/parser_match_summary_typed_handler_decomposition.md"
  risk_tier: "High"
  base_branch: "origin/main"
  same_repo_decomposition_selected: true
  cross_repo_extraction_authorized: false
  implementation_authorized: false
  pr_authorized: false
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
  reliability_readiness_claimed: false
  release_readiness_claimed: false
  deploy_readiness_claimed: false
  production_readiness_claimed: false
```
