# Parser DraftComplete Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/124

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence-ledger issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/parser_draft_complete.md`

## Role Performed

Codex C: Module Implementer.

## Worktree Note

The original checkout at `/Users/tahjblow/Documents/New project/Mythic-Edge`
was five commits behind `origin/codex/parser-reliability-intelligence` and had
unrelated untracked files from earlier modules. Codex C implemented this module
in a clean sibling worktree at:

`/Users/tahjblow/Documents/New project/Mythic-Edge-issue-124`

That worktree is detached at `origin/codex/parser-reliability-intelligence`
commit `11ce81d`, with the `docs/contracts/parser_draft_complete.md` source
artifact copied in from the original checkout.

## Summary Of Implementation Comparison

No blocking contract ambiguity was found. The current integration branch
already defined `DraftCompleteEvent`, had DraftBot and DraftHuman parser
modules, and had schema snapshot coverage for the event class. It lacked the
parser module, router/package wiring, focused tests, and payload-key snapshot
coverage needed to emit `DraftComplete` events.

Codex C implemented the smallest parser-local `DraftCompleteDraft` parser
surface, preserving DraftBot and DraftHuman behavior and leaving golden/corpus
coverage as an explicit remaining layer because no safe committed replay
fixture was required for minimum acceptance.

## Confirmed Matches

- `DraftCompleteEvent` already exists in `src/mythic_edge_parser/events.py`.
- `DraftCompleteEvent.kind` remains `"DraftComplete"`.
- `DraftCompleteEvent.performance_class` remains `DurablePerEvent`.
- `parser_event_classes.json` was unchanged.
- DraftBot and DraftHuman parser behavior was not modified.
- Existing DraftBot and DraftHuman focused tests still pass.
- Parser state, final reconciliation, workbook schema, webhook payload shape,
  Apps Script behavior, match/game identity, deduplication, runtime status
  files, failed posts, workbook exports, secrets, environment variables,
  generated data, and production behavior were not changed.

## Contract Mismatches Found And Fixed

- Missing `src/mythic_edge_parser/parsers/draft_complete.py`.
  - Fixed with a dedicated parser module for the exact
    `DraftCompleteDraft` marker.
- Missing package import and public `__all__` entry.
  - Fixed in `src/mythic_edge_parser/parsers/__init__.py`.
- Missing router dispatch from `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN`
  headers.
  - Fixed in `src/mythic_edge_parser/router.py`, ordered after DraftHuman and
    before Rank.
- Missing focused parser/router/package tests.
  - Fixed with `tests/test_draft_complete_parser.py` and small router unit
    order updates.
- Missing DraftComplete payload-key snapshot coverage.
  - Fixed by adding a `DraftComplete.draft_complete_draft` sample in
    `tests/test_event_schema_snapshots.py` and the authorized payload key entry
    in `tests/fixtures/schema_snapshots/parser_payload_keys.json`.

## Missing Safeguards Found And Added

- Marker matching is exact and case-sensitive.
- `DraftCompleteDraftExtra`, dotted suffixes, case variants, generic prose, and
  DraftBot/DraftHuman markers return `None`.
- Both request and response markers are recognized and preserve
  `api_direction`.
- Malformed marker-like input returns `None` instead of raising.
- Non-dictionary JSON payloads return `None`.
- Marker-wrapped payloads use nested marker fields only when the nested value
  is a mapping.
- Nested non-mapping marker payloads fall back to top-level normalization.
- Missing optional fields emit contract defaults.
- String fields accept only strings and strip whitespace.
- Boolean metadata accepts only real booleans; strings, integers, floats,
  containers, and objects remain `None`.
- Raw parsed top-level JSON is preserved in `raw_draft_complete` without
  normalizing card ratings, decklists, archetypes, advice, or hidden facts.

## Missing Or Weak Tests Found And Fixed

- Added focused direct payload coverage.
- Added marker-wrapped payload coverage.
- Added default value coverage.
- Added nested non-mapping fallback coverage.
- Added string and boolean normalization boundary tests.
- Added malformed JSON and non-dict JSON coverage.
- Added exact-marker false-positive coverage.
- Added first-marker deterministic policy coverage.
- Added package import coverage.
- Added Unity and UNKNOWN router reachability coverage.
- Added DraftBot/DraftHuman route-preservation coverage.
- Updated router dispatch-order tests.
- Updated schema snapshot sample coverage.

## Files Changed

- `docs/contracts/parser_draft_complete.md`
- `src/mythic_edge_parser/parsers/draft_complete.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_draft_complete_parser.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `docs/implementation_handoffs/parser_draft_complete_comparison.md`

## Interface Changes

Added parser-local module:

- `src/mythic_edge_parser/parsers/draft_complete.py`
- `DRAFT_COMPLETE_DRAFT_MARKER`
- `try_parse(entry, timestamp)`

Added emitted payload:

- `DraftComplete.draft_complete_draft`

Stable payload keys:

```text
type
source_method
api_direction
draft_id
event_id
queue_id
draft_status
completion_status
draft_type
draft_mode
completion_source
is_bot_draft
is_human_draft
raw_draft_complete
```

No new event class was added. No event kind changed.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_draft_complete_parser.py
# 39 passed

python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py
# 76 passed

python3 -m pytest -q tests/test_router_unit.py
# 17 passed

python3 -m pytest -q tests/test_event_schema_snapshots.py
# 6 passed

python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py
# 7 passed

python3 -m pytest -q tests/test_golden_replay_harness.py
# 12 passed

python3 -m pytest -q tests
# 858 passed

python3 -m ruff check src tests tools
# All checks passed.

git diff --check
# passed

git diff --no-index --check /dev/null docs/contracts/parser_draft_complete.md
git diff --no-index --check /dev/null src/mythic_edge_parser/parsers/draft_complete.py
git diff --no-index --check /dev/null tests/test_draft_complete_parser.py
# passed for new untracked files; no whitespace errors

python3 tools/check_protected_surfaces.py --base origin/main
# result: passed
# warnings: 11 branch-scope protected parser/match-surface warnings from the
# parser reliability branch; no forbidden paths.
```

## Still-Unverified Layers

- No safe committed golden replay fixture or feature-equity corpus fixture was
  added in this implementation pass.
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
  still records zero `DraftComplete` counts because no corpus fixture exercises
  DraftComplete through the replay path.
- Live private `Player.log` evidence, workbook writes, webhook delivery, Apps
  Script, runtime status files, failed posts, workbook exports, CI in GitHub,
  and production behavior were intentionally not exercised.
- Draft pick coaching, card ratings, deck construction analytics, hidden-card
  inference, archetype classification, gameplay advice, and AI/model-provider
  behavior remain out of scope.

## Reviewer Focus

Please verify that:

- `DraftCompleteDraft` marker matching is exact and case-sensitive.
- DraftComplete recognizes request and response markers.
- The emitted event is the existing `DraftCompleteEvent`.
- The stable payload keys and order match the contract.
- Raw parsed evidence is preserved only as `raw_draft_complete`.
- Malformed, partial, non-dict, and false-positive inputs do not raise or emit
  incorrect events.
- DraftBot and DraftHuman behavior is unchanged.
- Router dispatch is limited to Unity and UNKNOWN headers and is ordered after
  DraftHuman and before Rank.
- The schema snapshot update is limited to
  `DraftComplete.draft_complete_draft`.
- No protected downstream surfaces changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #124: DraftComplete parser module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Related evidence-ledger issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/124
- Branch/base: codex/parser-reliability-intelligence
- Contract: docs/contracts/parser_draft_complete.md
- Implementation handoff: docs/implementation_handoffs/parser_draft_complete_comparison.md
- Previous completed module: DraftHuman parser, issue #123
- Previous integration commit: 11ce81dde63c4a837acaaf3d42baf891590cf3dc

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/contracts/parser_draft_complete.md
- docs/contracts/parser_draft_bot.md
- docs/contracts/parser_draft_human.md
- docs/problem_representations/parser_feature_equity_with_manasight.md
- docs/implementation_handoffs/parser_draft_complete_comparison.md
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/parsers/draft_complete.py
- src/mythic_edge_parser/parsers/draft_bot.py
- src/mythic_edge_parser/parsers/draft_human.py
- tests/test_draft_complete_parser.py
- tests/test_draft_bot_parser.py
- tests/test_draft_human_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Goal:
Verify the Module Implementer patch against the DraftComplete parser contract.

Confirm:
- `DraftCompleteDraft` request and response markers emit the existing `DraftCompleteEvent`.
- `DraftCompleteEvent.kind` remains `"DraftComplete"` and no new event class was added.
- Metadata timestamp and raw bytes are preserved.
- Stable payload keys and key order match the contract.
- Direct and marker-wrapped payloads normalize from the correct source.
- Missing optional fields use `""`, `None`, or `"DraftCompleteDraft"` defaults as contracted.
- String fields accept only strings and strip whitespace.
- Boolean fields accept only real booleans and reject strings, numbers, containers, and objects.
- Marker-wrapped non-mapping payloads fall back to top-level normalization.
- Malformed JSON and non-dict JSON return `None`.
- Marker matching is exact and case-sensitive.
- DraftBot, DraftHuman, `LogBusinessEvents`, `PickGrpId`, suffix/prefix variants, and generic prose do not emit DraftComplete.
- Router/package wiring imports `draft_complete`, dispatches Unity and UNKNOWN headers only, and places DraftComplete after DraftHuman and before Rank.
- Existing DraftBot and DraftHuman behavior is preserved.
- `parser_payload_keys.json` changed only for `DraftComplete.draft_complete_draft`.
- `parser_event_classes.json` did not change.
- No parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, draft coaching, ratings, AI advice, or analytics truth changed.

Validation:
Run:
python3 -m pytest -q tests/test_draft_complete_parser.py
python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py
python3 -m pytest -q tests/test_router_unit.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not target main directly.
Do not close tracker #47.
Do not close related issue #11.
Do not stage, commit, merge, or open a PR.
Do not change DraftBot or DraftHuman behavior.
Do not create a new event class or change DraftCompleteEvent.kind.
Do not change protected parser/runtime/workbook/webhook/App Script surfaces.
Do not commit raw private Player.log excerpts.
Do not build draft coaching, ratings, AI advice, deck construction analytics, hidden-card inference, archetype classification, gameplay advice, or AI/analytics truth.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/124"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_draft_complete.md"
  target_artifact: "docs/implementation_handoffs/parser_draft_complete_comparison.md"
  verdict: "ready_for_module_reviewer"
  branch: "codex/parser-reliability-intelligence"
  worktree: "/Users/tahjblow/Documents/New project/Mythic-Edge-issue-124"
  risk_tier: "High"
  validation:
    - "python3 -m pytest -q tests/test_draft_complete_parser.py"
    - "python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py"
    - "python3 -m pytest -q tests/test_router_unit.py"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py"
    - "python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  files_changed:
    - "docs/contracts/parser_draft_complete.md"
    - "src/mythic_edge_parser/parsers/draft_complete.py"
    - "src/mythic_edge_parser/parsers/__init__.py"
    - "src/mythic_edge_parser/router.py"
    - "tests/test_draft_complete_parser.py"
    - "tests/test_router_unit.py"
    - "tests/test_event_schema_snapshots.py"
    - "tests/fixtures/schema_snapshots/parser_payload_keys.json"
    - "docs/implementation_handoffs/parser_draft_complete_comparison.md"
  remaining_gaps:
    - "No golden replay fixture or feature-equity corpus baseline update was added; DraftComplete corpus count remains zero until safe fixture coverage is added."
    - "Live private Player.log evidence and downstream workbook/webhook/App Script surfaces were not exercised."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change DraftBot or DraftHuman behavior."
    - "Do not create a new event class or change DraftCompleteEvent.kind."
    - "Do not change protected parser/runtime/workbook/webhook/App Script surfaces."
    - "Do not commit raw private Player.log excerpts."
    - "Do not build draft coaching, ratings, AI advice, deck construction analytics, hidden-card inference, archetype classification, gameplay advice, or AI/analytics truth."
```
