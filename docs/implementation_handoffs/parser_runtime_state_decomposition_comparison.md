# Parser Runtime State Decomposition Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/307

## Tracker

N/A

## Contract

`docs/contracts/parser_runtime_state_decomposition.md`

## Internal Project Area

Parser.

`src/mythic_edge_parser/app/state.py` is mapped as Parser-owned in
`docs/internal_project_map.md`. This slice also touches Quality / Governance
test evidence and a Quality / Governance implementation handoff.

## Truth Owner

Parser/state remains the truth owner for event interpretation, normalized
match/game facts, final reconciliation, identity, and deduplication.

`PostingState` owns downstream posting/delivery bookkeeping only. It is not
parser truth.

## Bridge-Code Status

`bridge_code`

`state.py` remains the compatibility bridge for existing module-level aliases
and helper APIs. The first pilot extracts the posting cluster without removing
legacy names.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifacts Used

- GitHub issue #307
- `docs/contracts/parser_runtime_state_decomposition.md`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/internal_project_map.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

## Files Inspected

- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/outputs.py`
- `tests/test_state.py`
- `tests/test_runner.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_parser_regressions.py`
- `tests/test_app_outputs.py`

## Current Behavior Compared To Contract

Current behavior before this slice:

- `ParserRuntimeState` already centralized runtime state, but posting and
  delivery bookkeeping lived as direct fields beside parser context, summary,
  mulligan, opening-hand, rank, card lookup, and local output state.
- Legacy module-level aliases such as `_POSTED_SUBMIT_DECK_KEYS`,
  `_GAME_ROWS_POSTED`, `_POSTED_MATCH_SUMMARIES`, and
  `_LAST_POSTED_MATCH_LOG_ROWS` pointed directly at mutable runtime-state
  containers.
- `reset_runtime_state()` cleared each posting container directly and preserved
  alias identity.
- `build_match_log_update()`, `build_game_log_updates()`,
  `mark_match_log_posted()`, and `mark_game_log_posted()` used those posting
  containers to compare prior posted rows and store copied posted snapshots.

Contract requirements:

- Extract or introduce only the `PostingState` downstream bookkeeping cluster.
- Preserve `ParserRuntimeState`, `RUNTIME_STATE`, `state.py` aliases, helper
  names, helper signatures, return shapes, changed-field behavior, and copied
  snapshot semantics.
- Preserve mutable alias object identity across reset.
- Avoid parser behavior, final reconciliation, event class, identity,
  deduplication, workbook, webhook, analytics, local app, and AI changes.

Gap closed:

- The posting/delivery bookkeeping cluster now has a named `PostingState`
  object while `state.py` keeps the compatibility bridge intact.

Remaining deferred clusters:

- Parser context, match summaries, mulligan state, opening-hand state, rank
  state, card lookup state, local output path state, and transform emission
  guard state remain in `state.py`.

## Implementation Option Chosen

Used a nested `ParserRuntimeState.posting: PostingState` field plus
compatibility properties on `ParserRuntimeState`.

This is the smallest behavior-preserving option because it:

- names the posting cluster;
- keeps `RUNTIME_STATE.posted_*` attribute access working;
- keeps existing module-level aliases pointing to the same mutable containers;
- avoids broad caller import migration;
- avoids touching parser fact clusters.

## What Changed

- Added `src/mythic_edge_parser/app/posting_state.py` with a narrow
  `PostingState` dataclass.
- Nested `PostingState` under `ParserRuntimeState`.
- Replaced direct posting fields on `ParserRuntimeState` with compatibility
  properties that return the nested posting containers.
- Pointed legacy `state.py` posting aliases at `RUNTIME_STATE.posting`.
- Delegated posting reset through `PostingState.reset()`.
- Delegated posted match/game row snapshot writes through `PostingState`
  methods while preserving copy semantics.
- Added focused state tests that prove the nested posting bridge and legacy
  aliases stay identity-stable.

## Files Changed

- `src/mythic_edge_parser/app/posting_state.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_state.py`
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`

The contract file `docs/contracts/parser_runtime_state_decomposition.md`
remains an untracked Codex B artifact and was preserved.

Unrelated untracked file preserved:

- `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`

## Exact Code/Test/Doc Sections Changed

Code:

- `posting_state.py`
  - Added `PostingState`.
  - Added `reset()`.
  - Added `mark_match_log_posted()`.
  - Added `mark_game_log_posted()`.
- `state.py`
  - Imported `PostingState`.
  - Added `ParserRuntimeState.posting`.
  - Added compatibility properties for the eight contracted posting fields.
  - Added `_POSTING_STATE` bridge alias.
  - Updated existing posting aliases to point at `_POSTING_STATE`.
  - Updated `reset_runtime_state()` to call `_POSTING_STATE.reset()`.
  - Updated match/game log update and mark-posted helpers to use
    `_POSTING_STATE`.

Tests:

- `tests/test_state.py`
  - Extended alias-identity reset coverage for all contracted posting aliases.
  - Added `test_posting_state_bridge_aliases_point_to_nested_state()`.

Docs:

- Added this implementation handoff.

## Code Changed

Yes. Parser-runtime bridge code changed, but the change is decomposition-only
and keeps parser behavior/output behavior unchanged.

## Tests Added Or Updated

Yes. Focused `tests/test_state.py` coverage was updated.

## Interface Changes

Existing public/bridge interfaces preserved:

- `ParserRuntimeState`
- `RUNTIME_STATE`
- `get_runtime_state()`
- `reset_runtime_state()`
- `_POSTED_SUBMIT_DECK_KEYS`
- `_POSTED_SIDEBOARD_KEYS`
- `_GAME_ROWS_POSTED`
- `_MATCH_ROWS_POSTED`
- `_POSTED_MATCH_SUMMARIES`
- `_POSTED_MATCH_LOG_ROWS`
- `_LAST_POSTED_MATCH_LOG_ROWS`
- `_LAST_POSTED_GAME_LOG_ROWS`
- `build_match_log_update()`
- `mark_match_log_posted()`
- `build_game_log_updates()`
- `mark_game_log_posted()`

New internal support interface:

- `mythic_edge_parser.app.posting_state.PostingState`
- `ParserRuntimeState.posting`

No parser event classes, event kind values, workbook columns, webhook payload
fields, analytics schema fields, environment variables, or production entry
points changed.

## Contracted Area Status

Stayed inside the contracted first pilot:

- Extracted only the posting/delivery bookkeeping cluster.
- Did not extract parser context, match summaries, mulligan state,
  opening-hand state, rank state, card lookup state, transform emission guards,
  analytics state, local app state, or live capture state.

## Behavior Preserved

Confirmed by tests:

- `reset_runtime_state()` preserves runtime singleton identity.
- `reset_runtime_state()` preserves posting alias object identity.
- Posting containers are cleared on reset.
- Posted match/game row snapshots are stored as copies.
- Match log changed-field detection remains unchanged.
- Game log changed-field detection remains unchanged.
- Runner success callbacks still mark posted rows through the existing helper
  APIs.
- Representative parser regression and output tests remain unchanged.

## Validation Run

```text
git status --short --branch --untracked-files=all -> branch codex/analytics-foundation; modified state.py/test_state.py; untracked #304 contract, #307 contract, posting_state.py
gh issue view 307 --repo Tahjali11/Mythic-Edge --json number,title,state,body,comments -> issue open, no comments
py -m pytest -q tests\test_state.py -> 19 passed in 0.53s
py -m ruff check src\mythic_edge_parser\app\state.py src\mythic_edge_parser\app\posting_state.py tests\test_state.py -> All checks passed!
py -m pytest -q tests\test_state.py tests\test_runner.py tests\test_match_summary_from_match_state.py -> 45 passed in 0.86s
py -m pytest -q tests\test_parser_regressions.py -> 3 passed in 0.49s
py -m pytest -q tests\test_app_outputs.py -> 19 passed in 0.65s
py -m ruff check src tests -> All checks passed!
git diff --check -> passed
py tools\check_agent_docs.py -> passed, 0 errors, 0 warnings
```

Final path-scoped protected-surface and secret/private-marker scans are listed
below.

## Protected-Surface Status

Path-scoped protected-surface scan over touched files passed with one expected
contract-authorized warning for `state.py`:

```text
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin -> forbidden 0, warnings 1
```

Protected parser surfaces were touched by path, but the contract explicitly
authorized a behavior-preserving `PostingState` pilot in `state.py`. No
forbidden semantic protected-surface change was made.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over touched files passed:

```text
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin -> forbidden 0, warnings 0
```

No raw logs, secrets, credentials, generated data, runtime status files, failed
posts, workbook exports, private JSONL artifacts, generated SQLite files, or
local-only artifacts were added.

## Generated/Private Artifact Status

No generated/private/runtime artifacts were created or committed.

## Still Unverified

- Full repository pytest was not run; validation stayed focused to the
  contract-required parser/runtime surfaces.
- Live parser runtime against a real Player.log was not run.
- No workbook, webhook, Apps Script, Sheets, analytics, local app, AI, or
  production behavior was exercised because those surfaces were out of scope.

## Whether Forbidden Scope Was Touched

Forbidden scope was not touched.

Specifically unchanged:

- parser behavior
- parser final reconciliation
- parser event classes
- event kind values
- parser payload shapes
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets behavior
- analytics schema/migrations
- local app behavior
- live capture behavior
- production behavior
- AI/OpenAI/coaching/Line Tracer behavior

## Reviewer Focus

Codex E should focus on:

- Whether `PostingState` extraction is truly limited to downstream posting and
  delivery bookkeeping.
- Whether the `ParserRuntimeState` compatibility properties are acceptable as
  the bridge surface.
- Whether aliases still point at nested containers and remain identity-stable
  across reset.
- Whether row snapshot copy semantics and changed-field detection are unchanged.
- Whether any protected parser behavior changed accidentally despite focused
  tests passing.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #307.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/307

Branch:
codex/analytics-foundation

Contract:
docs/contracts/parser_runtime_state_decomposition.md

Implementation handoff:
docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md

Risk tier:
High

Goal:
Review the PostingState decomposition pilot against the contract. Lead with blocking findings, if any. Verify that the implementation is behavior-preserving, keeps state.py compatibility aliases stable, and does not change parser truth ownership.

Before reviewing:
- Confirm branch and git status.
- Identify unrelated dirty/untracked files and exclude them from findings unless they affect this scope.
- Read the contract and implementation handoff.
- Inspect the diff for:
  - src/mythic_edge_parser/app/posting_state.py
  - src/mythic_edge_parser/app/state.py
  - tests/test_state.py
  - docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md

Review focus:
- Is only the PostingState downstream bookkeeping cluster extracted?
- Do ParserRuntimeState, RUNTIME_STATE, reset_runtime_state(), state.py aliases, and helper APIs remain import-compatible?
- Are mutable alias objects identity-stable across reset?
- Are posted match/game row snapshots still copied before storage?
- Are build_match_log_update() and build_game_log_updates() changed-field semantics unchanged?
- Did runner callback behavior remain unchanged?
- Did parser behavior, final reconciliation, event classes, match/game identity, deduplication, workbook/webhook/App Script/Sheets/analytics/local app/live capture/AI/production behavior stay untouched?
- Are tests sufficient for the contract?

Validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_state.py tests\test_runner.py tests\test_match_summary_from_match_state.py
py -m pytest -q tests\test_parser_regressions.py
py -m pytest -q tests\test_app_outputs.py
py -m ruff check src tests
git diff --check
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over touched files.

Final report must include:
- findings first, ordered by severity
- contract match/mismatch summary
- validation results
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- whether forbidden scope was touched
- remaining risk/unverified layers
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/307"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_runtime_state_decomposition.md"
  target_artifact: "docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  decision: "Introduced PostingState as the first behavior-preserving decomposition pilot while preserving state.py compatibility aliases and parser truth boundaries."
  validation:
    - "py -m pytest -q tests\\test_state.py -> 19 passed"
    - "py -m pytest -q tests\\test_state.py tests\\test_runner.py tests\\test_match_summary_from_match_state.py -> 45 passed"
    - "py -m pytest -q tests\\test_parser_regressions.py -> 3 passed"
    - "py -m pytest -q tests\\test_app_outputs.py -> 19 passed"
    - "py -m ruff check src tests -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 1 expected parser state warning"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not remove compatibility aliases or change helper signatures."
    - "Do not broaden extraction beyond PostingState without a contract amendment."
    - "Do not change parser behavior, final reconciliation, event classes, match/game identity, workbook/webhook/App Script/Sheets behavior, analytics schema, local app behavior, production behavior, or AI/model-provider behavior."
    - "Do not target main."
```
