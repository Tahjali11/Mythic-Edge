# Parser Runtime State Decomposition Contract

## Metadata

- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/307
- Role: Codex B / Module Contract Writer
- Intended base branch: `codex/analytics-foundation`
- Risk tier: High
- Contract artifact: `docs/contracts/parser_runtime_state_decomposition.md`
- Bridge-code status: `bridge_code`

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `tests/test_state.py`
- `tests/test_runner.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_parser_regressions.py`
- `tests/test_app_outputs.py`

## Observed Current Behavior

`src/mythic_edge_parser/app/state.py` currently exposes one broad `ParserRuntimeState` dataclass, a singleton `RUNTIME_STATE`, module-level mutable aliases, scalar alias helpers, row-builder helpers, reset helpers, and downstream posting bookkeeping.

The file mixes several conceptual state clusters:

- parser context and current match/game association
- parser-owned match and game summary state
- mulligan and opening-hand state
- rank carry-forward state
- card lookup readiness and runtime caches
- local output path bookkeeping
- downstream row-posting and delivery bookkeeping
- compatibility aliases used by tests and adjacent modules

Existing tests intentionally pin important compatibility behavior. In particular, `tests/test_state.py` verifies that `reset_runtime_state()` clears shared containers without replacing them, preserves alias object identity, resets scalar values, and stores copies of posted row snapshots.

The current design is functional but increasingly hard to reason about because parser truth, runtime support, and downstream delivery bookkeeping live in the same object and module surface.

## Required Guarantees

Parser runtime state decomposition must be behavior-preserving. It may make state ownership easier to read and safer to evolve, but it must not change parser interpretation, final reconciliation, event classification, row identity, deduplication, output payloads, workbook schemas, webhook payload shape, analytics schema, or local app behavior.

The decomposition strategy must guarantee:

- `ParserRuntimeState` and `RUNTIME_STATE` remain import-compatible unless a later contract explicitly authorizes removal or replacement.
- `reset_runtime_state()` keeps existing reset semantics.
- Existing mutable alias object identity remains stable across reset.
- Existing scalar alias helpers remain synchronized with runtime state.
- Existing row builders and mark-posted helpers keep their public names and behavior.
- Posted row snapshots continue to be copied before storage.
- Changed-field detection remains unchanged.
- Parser-owned state remains parser-owned after decomposition.
- Downstream bookkeeping remains downstream bookkeeping and must not become parser truth.
- No raw `Player.log` content, private artifacts, runtime logs, generated data, secrets, or local-only artifacts may be introduced.

## State Cluster Map

| Cluster | Current examples | Truth ownership | First-pass action |
| --- | --- | --- | --- |
| Parser context state | `_CONTEXT`, current match id, game number, player team | Parser truth context | Name only; do not extract first |
| Match summary state | `_MATCH_SUMMARIES`, `_update_match_summary`, match/game row builders | Parser-owned normalized facts | Name only; do not extract first |
| Mulligan state | `_MULLIGAN_COUNTS` | Parser-owned match/game fact support | Name only; defer |
| Opening-hand state | `_GAME_INSTANCE_GRP_IDS`, `_HAND_SNAPSHOT_HISTORY`, `_LATEST_HAND_SNAPSHOT`, `_BOTTOMED_CARDS_CAPTURED`, local hand snapshot keys | Parser-owned evidence support | Name only; defer |
| Rank state | latest rank text/class/level/percentile, last posted rank | Parser-managed context plus delivery guard | Name only; defer |
| Card lookup runtime state | `arena_card_lookup`, lookup readiness flags | Parser support/cache, not external truth | Name only; defer |
| Local output path state | current log date/path | Runtime bookkeeping | Name only; defer |
| Transform emission guard state | local/sheets turn keys and related dedupe sets | Downstream emission bookkeeping with parser-adjacent risk | Defer until after pilot |
| PostingState | posted submit-deck keys, sideboard keys, game/match rows posted, posted summaries, posted row snapshots | Downstream delivery bookkeeping, not parser truth | Approved first pilot |

## Approved First Pilot: PostingState

`PostingState` is the safest first pilot extraction because it primarily tracks which downstream rows or payloads have already been posted or snapshotted. It is not the source of match result truth, game result truth, play/draw truth, mulligan truth, opening-hand truth, card identity truth, or gameplay-action truth.

The first pilot may extract only this downstream bookkeeping cluster:

- `posted_submit_deck_keys`
- `posted_sideboard_keys`
- `game_rows_posted`
- `match_rows_posted`
- `posted_match_summaries`
- `posted_match_log_rows`
- `last_posted_match_log_rows`
- `last_posted_game_log_rows`

The pilot may introduce a small `PostingState` dataclass or equivalent narrow object under `src/mythic_edge_parser/app/`, but it must keep current import paths and helper APIs working from `state.py`.

The pilot must not extract parser context, match summaries, mulligan state, opening-hand state, rank state, card lookup readiness, gameplay actions, opponent-card observations, analytics ingest state, or local app state.

## Compatibility Bridge Rules

The current state module is a bridge surface. Codex C must preserve the bridge while extracting the pilot cluster.

Required bridge rules:

- Existing aliases such as `_POSTED_SUBMIT_DECK_KEYS`, `_POSTED_SIDEBOARD_KEYS`, `_GAME_ROWS_POSTED`, `_MATCH_ROWS_POSTED`, `_POSTED_MATCH_SUMMARIES`, `_POSTED_MATCH_LOG_ROWS`, `_LAST_POSTED_MATCH_LOG_ROWS`, and `_LAST_POSTED_GAME_LOG_ROWS` must remain available from `src/mythic_edge_parser/app/state.py`.
- Mutable alias objects must not be replaced during `reset_runtime_state()`.
- If `ParserRuntimeState` gains a nested `posting` field, the legacy aliases must point at the nested containers and remain identity-stable.
- Existing helpers including `build_match_log_update()`, `mark_match_log_posted()`, `build_game_log_updates()`, and `mark_game_log_posted()` must keep their names, signatures, return shapes, and copy semantics.
- Callers may be internally delegated to the new object, but broad import migration is out of scope for the first pilot.
- Any new compatibility comments should be brief and should identify bridge behavior without promising alias removal.
- Alias removal, deprecation warnings, broad caller rewrites, or import-path churn require a later contract.

## Parser Truth Boundary

This contract does not authorize a new parser truth source. Parser/state remains the owner of event interpretation and normalized match/game facts under ADR-0001.

`PostingState` must be treated as downstream delivery bookkeeping. It may remember what has already been emitted or posted; it must not decide what a match, game, action, mulligan, opening hand, rank, deck, or card means.

Downstream workbook, webhook, analytics, local app, and AI surfaces remain consumers or displays of parser-owned facts. They do not gain truth ownership through this decomposition.

## Protected Surfaces

The first pilot must not change:

- parser behavior
- parser state final reconciliation
- parser event classes
- event kind values
- parser payload shapes
- match/game identity or deduplication
- match summary or game summary semantics
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets behavior
- analytics schema or migrations
- local app behavior
- live capture behavior
- output transport or production behavior
- OpenAI/model-provider behavior
- AI/coaching/Line Tracer behavior
- raw logs, generated data, runtime status files, failed posts, workbook exports, secrets, credentials, or local-only artifacts

ADR-0004 protected-surface warnings are review signals, not automatic authorization.

## Unknowns

- Whether a nested `ParserRuntimeState.posting` field is the cleanest implementation shape, or whether a separate module-level `POSTING_STATE` with legacy aliases is lower risk.
- Whether `posted_match_log_rows` and `posted_match_summaries` should remain separate long term.
- Whether turn-key and transform emission guard state belongs with `PostingState` in a later pass or should become its own cluster.
- Whether rank carry-forward should eventually split into parser context and downstream posting memory.
- Whether repeated successful cluster extraction should become ADR-0007.

## Suspected Gaps

- The current module does not name state ownership boundaries, which makes future edits more likely to touch parser truth while intending to adjust downstream bookkeeping.
- Existing alias compatibility is implicit and mostly protected by tests rather than documentation.
- The current reset path relies on careful clearing of mutable containers; an extraction could accidentally replace containers and break alias consumers.
- Broad refactors would be high risk because `state.py` is imported across parser, transforms, runner, outputs, gameplay surfaces, golden replay, analytics legacy adapter, and tests.

## Out Of Scope

This contract does not authorize:

- implementation during Codex B
- a full `state.py` rewrite
- extracting more than the PostingState pilot cluster
- removing aliases
- changing helper signatures
- changing parser facts or final reconciliation
- changing workbook/webhook/Apps Script/Sheets behavior
- changing analytics or local app behavior
- adding CI gates
- creating ADR-0007 immediately
- targeting `main`

## Behavior-Preserving Test Expectations

Codex C must preserve and, if needed, extend tests that prove:

- `reset_runtime_state()` preserves alias object identity.
- `reset_runtime_state()` clears PostingState containers.
- posted match and game row snapshots are stored as copies.
- match log update detection remains unchanged.
- game log update detection remains unchanged.
- runner success callbacks still mark posted rows through the existing helper APIs.
- match summary live/final readiness behavior remains unchanged.
- parser regression behavior is unchanged for representative fixtures.

Minimum focused validation for Codex C:

```powershell
py -m pytest -q tests\test_state.py tests\test_runner.py tests\test_match_summary_from_match_state.py
py -m pytest -q tests\test_parser_regressions.py
py -m pytest -q tests\test_app_outputs.py
ruff check src tests
git diff --check
```

If Codex C touches transform emission guard state, it must also run the focused transform tests. If Codex C touches context, gameplay, or runtime surface state, it must add the relevant focused tests before review.

## ADR-0007 Recommendation

Do not create ADR-0007 before the first pilot extraction.

ADR-0007 should be considered only if:

- the `PostingState` pilot lands with preserved behavior,
- Codex E confirms the compatibility bridge is stable,
- at least one later contract needs the same state-cluster pattern, and
- the project needs a durable architectural rule rather than a one-off implementation contract.

ADR-0007, if created later, should document the decomposition strategy and ownership model. It must not retroactively authorize parser behavior changes, protected-surface changes, alias removal, or broad module moves.

## Branch And Worktree Preconditions

Codex A observed branch drift during problem framing: local checkout was on `codex/live-capture-heartbeat-no-row-fixer-302`, while the intended base for this work is `codex/analytics-foundation`.

Before implementation, Codex C must:

- confirm the active branch is `codex/analytics-foundation`;
- inspect `git status --short --branch --untracked-files=all`;
- preserve unrelated #302 WIP or any other local changes;
- avoid staging, overwriting, or absorbing unrelated frontend/live-capture work;
- stop and ask for routing if the branch is not `codex/analytics-foundation` and the worktree is dirty.

## Acceptance Criteria

This contract is satisfied when a future implementation:

- extracts or introduces the `PostingState` pilot cluster only;
- preserves all existing public helper names and alias surfaces;
- preserves mutable alias identity across reset;
- preserves row snapshot copy semantics;
- preserves parser output behavior;
- adds or maintains focused tests for reset, alias identity, update detection, and posting callbacks;
- passes focused parser/runtime validation;
- avoids protected-surface changes;
- documents any remaining state clusters as deferred rather than partially extracting them.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #307.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/307

Branch:
codex/analytics-foundation

Contract:
docs/contracts/parser_runtime_state_decomposition.md

Goal:
Implement only the first behavior-preserving parser runtime state decomposition pilot: extract or introduce PostingState for downstream posting/delivery bookkeeping while preserving all existing state.py helper APIs and compatibility aliases.

Before editing:
- Confirm the active branch is codex/analytics-foundation.
- Inspect git status with untracked files.
- Preserve unrelated #302 WIP or frontend/live-capture changes.
- Read the contract, state.py, runner.py, transforms.py, and focused tests.

Do:
- Keep ParserRuntimeState, RUNTIME_STATE, reset_runtime_state(), get_runtime_state(), posting aliases, and mark/build helper APIs import-compatible.
- Preserve mutable alias object identity across reset.
- Preserve posted row snapshot copy semantics.
- Keep this as a narrow PostingState pilot only.
- Add or adjust focused behavior-preserving tests if needed.
- Produce docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md.

Do not:
- Rewrite state.py broadly.
- Extract parser context, match summaries, mulligan state, opening-hand state, rank state, card lookup state, analytics state, live app state, or transform emission guard state unless the contract is amended.
- Remove aliases or change helper signatures.
- Change parser behavior, final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script/Sheets behavior, analytics schema, local app behavior, production behavior, AI/model-provider behavior, raw logs, generated data, secrets, or local-only artifacts.
- Target main, stage, commit, push, open a PR, or close issue #307 unless explicitly asked.

Validation:
py -m pytest -q tests\test_state.py tests\test_runner.py tests\test_match_summary_from_match_state.py
py -m pytest -q tests\test_parser_regressions.py
py -m pytest -q tests\test_app_outputs.py
ruff check src tests
git diff --check
path-scoped protected-surface and secret/private-marker scans for changed files

Final handoff must include:
- role performed
- branch and git status
- contract used
- implementation handoff artifact
- files changed
- behavior preserved
- validation run and results
- protected-surface status
- remaining risks
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/307"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #307"
  contract_artifact: "docs/contracts/parser_runtime_state_decomposition.md"
  target_artifact: "docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  decision: "Use PostingState as the first behavior-preserving decomposition pilot; preserve state.py compatibility aliases and parser truth boundaries."
  stop_conditions:
    - "Do not implement more than the PostingState pilot without a contract amendment."
    - "Do not remove compatibility aliases or change helper signatures."
    - "Do not change parser behavior, final reconciliation, event classes, match/game identity, workbook/webhook/App Script/Sheets behavior, analytics schema, local app behavior, production behavior, or AI/model-provider behavior."
    - "Do not absorb unrelated #302 WIP or frontend/live-capture changes."
    - "Do not target main."
```
