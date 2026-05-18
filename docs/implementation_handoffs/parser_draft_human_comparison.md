# Parser DraftHuman Implementation Comparison

## Role Performed

Codex C / Module Implementer / comparison thread.

## Issue And Trackers

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/123
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Related tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Branch: `codex/parser-reliability-intelligence`

## Contract Used

- Source contract: `docs/contracts/parser_draft_human.md`
- Target artifact: `docs/implementation_handoffs/parser_draft_human_comparison.md`
- Risk tier: High

## Branch And Git Status

Initial status before editing:

```text
## codex/parser-reliability-intelligence...origin/codex/parser-reliability-intelligence
?? docs/contracts/parser_draft_human.md
```

The contract file was present as an untracked source artifact before this pass.
It was inspected but not modified.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/parser_draft_human.md`
- `docs/contracts/parser_draft_bot.md`
- `docs/contracts/parser_draft_surface_parity_recommendation.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/parsers/draft_bot.py`
- `tests/test_draft_bot_parser.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_feature_equity_corpus_ratchet.py`
- `tests/test_golden_replay_harness.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`

## Current Behavior Compared To Contract

### Contract Matches Before Implementation

- `DraftHumanEvent` already existed in `events.py`.
- `DraftHumanEvent.kind` was already `"DraftHuman"`.
- `DraftHumanEvent.performance_class` was already `DurablePerEvent`.
- `DraftHumanEvent` was already part of the public `GameEvent` union.
- `parser_event_classes.json` already covered the DraftHuman event class and
  kind.
- `DraftBot` support already existed separately and was routed before the new
  DraftHuman surface.

### Contract Mismatches Before Implementation

- No `src/mythic_edge_parser/parsers/draft_human.py` module existed.
- `parsers.__init__` did not export `draft_human`.
- `router.py` did not dispatch to a DraftHuman parser for Unity or UNKNOWN log
  entries.
- No focused DraftHuman parser tests existed.
- `tests/test_event_schema_snapshots.py` had no DraftHuman payload samples.
- `parser_payload_keys.json` had no `DraftHuman.*` payload-key entries.
- Feature-equity corpus baseline correctly recorded zero DraftHuman counts
  because no committed golden replay fixture exercised DraftHuman.

## Implementation Option Chosen

Implemented the minimum parser/test/snapshot package authorized by the contract.

This pass did not add golden replay or corpus fixture coverage. The contract
classifies that as full reliability evidence rather than the minimum first
implementation evidence, and no safe committed DraftHuman fixture was in scope.

## Files Changed

- `src/mythic_edge_parser/parsers/draft_human.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_draft_human_parser.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `docs/implementation_handoffs/parser_draft_human_comparison.md`

Inspected but not modified:

- `docs/contracts/parser_draft_human.md`

## Exact Sections Changed

### Parser Code

Added `src/mythic_edge_parser/parsers/draft_human.py` with:

- exact, case-sensitive marker constants:
  - `Draft.Notify`
  - `EventPlayerDraftMakePick`
  - `LogBusinessEvents`
- a dedicated API marker regex that escapes the dotted `Draft.Notify` marker
  and does not use the shared non-dotted API-name regex
- `try_parse(entry, timestamp)` returning the existing `DraftHumanEvent`
- raw parsed top-level payload preservation under `raw_draft_human`
- `LogBusinessEvents` narrowing to valid picked-card evidence
- private helpers for string, scalar integer, list-of-card-id, and first-marker
  normalization

Implemented stable DraftHuman payload fields:

```text
type
source_method
api_direction
draft_id
event_id
draft_status
pack_number
pick_number
pack_card_ids
picked_card_id
picked_card_ids
business_event_type
raw_draft_human
```

### Parser Package

Updated `src/mythic_edge_parser/parsers/__init__.py`:

- imported `draft_human`
- added `"draft_human"` to `__all__`

### Router

Updated `src/mythic_edge_parser/router.py`:

- added `parsers.draft_human` to `EntryHeader.UNITY_CROSS_THREAD_LOGGER`
- added `parsers.draft_human` to `EntryHeader.UNKNOWN`
- placed it after `parsers.draft_bot` and before `parsers.rank`
- did not add it to metadata, GRE, truncation, connection, or matchmaking
  buckets

### Tests

Added `tests/test_draft_human_parser.py` covering:

- `Draft.Notify` emits `human_draft_notify`
- `EventPlayerDraftMakePick` emits `human_draft_make_pick`
- `LogBusinessEvents` with valid picked-card evidence emits
  `human_draft_business_pick`
- `LogBusinessEvents` without valid picked-card evidence returns `None`
- event kind, performance class, timestamp, and raw bytes
- source method and API direction
- direct, marker-wrapped, and business-event list payload shapes
- missing optional field defaults
- integer-like string normalization
- invalid scalar and list-member rejection
- malformed JSON and non-dictionary JSON rejection
- exact/case-sensitive marker matching, including dotted `Draft.Notify`
- false positives against DraftBot, DraftComplete, and generic prose
- public package import
- Unity and UNKNOWN router reachability
- DraftBot precedence still routes DraftBot before DraftHuman

Updated `tests/test_router_unit.py`:

- added `draft_human` to dispatch-order monkeypatch coverage
- updated Unity and UNKNOWN dispatch-order expectations

Updated `tests/test_event_schema_snapshots.py`:

- imported `draft_human`
- added representative samples for all three DraftHuman payload types

### Snapshot Fixture

Updated `tests/fixtures/schema_snapshots/parser_payload_keys.json` with:

- `DraftHuman.human_draft_notify`
- `DraftHuman.human_draft_make_pick`
- `DraftHuman.human_draft_business_pick`

The snapshot contains payload keys only. It does not store raw nested payload
values, private log content, workbook IDs, webhook URLs, runtime paths, failed
posts, generated data, or local machine paths.

## Code/Test/Fixture/Docs Status

- Code changed: yes
- Tests changed: yes
- Snapshot changed: yes, payload-key schema snapshot only
- Fixtures changed: yes, schema snapshot fixture only
- Golden replay fixtures changed: no
- Corpus baseline changed: no
- Docs changed: yes, this handoff only

## Contract Matches After Implementation

- The existing `DraftHumanEvent` is used; no new event class or kind value was
  added.
- `DraftHumanEvent.kind` remains `"DraftHuman"`.
- `DraftHumanEvent.performance_class` remains durable per-event.
- The parser emits at most one event per entry.
- Marker matching is exact and case-sensitive.
- `Draft.Notify` is handled with an escaped dotted marker, not a generic
  unescaped API-name regex.
- `api_direction` is `"request"` for `==>` and `"response"` for `<==`.
- Non-business markers with parseable dictionaries emit defaults for missing
  optional normalized fields.
- `LogBusinessEvents` emits only when a valid picked-card alias is present.
- `LogBusinessEvents` without valid picked-card evidence returns `None`.
- Direct object, marker-wrapped object, and business-event list shapes are
  covered by tests.
- Invalid numeric values do not raise and do not enter normalized output.
- Invalid list members are skipped.
- DraftBot and DraftComplete markers do not emit DraftHuman.
- Router dispatch is limited to Unity and UNKNOWN headers.
- DraftBot remains before DraftHuman in router dispatch.
- DraftHuman payload-key schema snapshot coverage exists for all three payload
  types.

## Contract Mismatches After Implementation

No known mismatch remains for the minimum implementation evidence required by
the contract.

The remaining gaps are reliability evidence gaps, not contradictions with the
implemented minimum scope.

## Missing Safeguards Or Missing Tests

- No committed sanitized or synthetic golden replay fixture exercises
  DraftHuman through `LineBuffer` and `Router`.
- Feature-equity corpus baseline still records zero DraftHuman counts by design.
- Exact live MTGA human draft payload field names remain unverified.
- It remains unknown whether `LogBusinessEvents` can contain multiple separate
  draft picks that should eventually require multi-event emission.
- It remains unknown whether pack and pick indexes are always zero-based or
  one-based; this implementation preserves observed values without conversion.
- Repo-approved secret/private-content scanner was not run because
  `tools/check_secret_patterns.py` is not present on this branch.

## Validation Run And Result

Focused first:

```text
py -m pytest -q tests\test_draft_human_parser.py
41 passed in 0.54s
```

Snapshot check before the approved snapshot update:

```text
py -m pytest -q tests\test_event_schema_snapshots.py
1 failed, 5 passed
```

The failure was the expected `parser_payload_keys.json` mismatch after adding
DraftHuman sample events. The contract explicitly authorized adding the three
DraftHuman payload-key snapshot entries.

Focused after snapshot update:

```text
py -m pytest -q tests\test_draft_human_parser.py tests\test_event_schema_snapshots.py
47 passed in 0.67s
```

Adjacent parser/router checks:

```text
py -m pytest -q tests\test_draft_bot_parser.py tests\test_router_unit.py tests\test_parsers.py
70 passed in 0.62s
```

Related reliability checks:

```text
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
45 passed in 1.06s
```

Ruff:

```text
py -m ruff check src tests tools
All checks passed!
```

Whitespace:

```text
git diff --check
passed

Select-String -Path docs\contracts\parser_draft_human.md,docs\implementation_handoffs\parser_draft_human_comparison.md,src\mythic_edge_parser\parsers\draft_human.py,tests\test_draft_human_parser.py -Pattern '[ \t]+$'
no matches
```

Protected surface gate:

```text
py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence
forbidden: 0
warnings: 0
result: passed
```

Path-scoped protected surface gate over touched paths:

```text
py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
forbidden: 0
warnings: 2
result: passed
```

Warnings:

- `match_game_identity src/mythic_edge_parser/parsers/draft_human.py`
- `match_game_identity src/mythic_edge_parser/parsers/__init__.py`

Interpretation: these warnings are expected parser-surface warnings and are
authorized by `docs/contracts/parser_draft_human.md`.

## Protected-Surface Status

Forbidden protected surfaces touched: none known.

Authorized parser surfaces touched:

- `src/mythic_edge_parser/parsers/draft_human.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/router.py`

Protected surfaces not touched:

- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event kind values
- match identity
- game identity
- deduplication
- secrets or environment variables
- raw local logs
- generated card data
- runtime status files
- failed posts
- workbook exports
- live workbook state
- deployed Apps Script state
- production behavior

## Fixture And Corpus Drift-Budget Interpretation

No new `.log` fixture was added.

No golden replay manifest was added.

No feature-equity corpus baseline was changed.

The zero DraftHuman count in
`tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
remains accurate because no committed golden replay fixture exercises the new
DraftHuman parser through the normal replay path.

## What Remains Unverified

- Live MTGA human draft log payload field names.
- Real Premier/Traditional draft request/response direction distribution.
- Multi-pick `LogBusinessEvents` behavior, if Arena emits it.
- Golden replay DraftHuman fixture coverage.
- Nonzero feature-equity corpus DraftHuman coverage.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.

## Forbidden Scope

No forbidden scope was intentionally touched.

This pass did not:

- copy Manasight code
- commit raw private Player.log excerpts
- add DraftComplete behavior
- change DraftBot parser behavior
- change parser state final reconciliation
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change event classes or event kind values
- change match/game identity or deduplication
- stage, commit, open a PR, close issues, or mark trackers complete

## Next Recommended Role

Recommended next role: Codex E / Module Reviewer / contract-test thread.

Codex E should review the implementation against
`docs/contracts/parser_draft_human.md`, verify the diff and validation evidence,
and decide whether it routes forward to Codex F or back to Codex D/B.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #123: parser DraftHuman support.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/123

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Related tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/parser_draft_human.md

Implementation handoff:
docs/implementation_handoffs/parser_draft_human_comparison.md

Review scope:
Review the DraftHuman implementation against the contract. Lead with findings ordered by severity. Do not assume there is a known bug; verify whether the implementation satisfies the contract and whether any behavior exceeds scope.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_reviewer.md
- docs/contracts/parser_draft_human.md
- docs/implementation_handoffs/parser_draft_human_comparison.md
- src/mythic_edge_parser/parsers/draft_human.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/events.py
- tests/test_draft_human_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Focus areas:
- Exact and case-sensitive marker matching, especially dotted Draft.Notify.
- LogBusinessEvents only emits DraftHuman when picked-card evidence is valid.
- Payload key order and field normalization match the contract.
- Raw parsed top-level payload is preserved without committing private raw log data.
- DraftBot behavior and precedence are preserved.
- DraftComplete remains out of scope.
- Router dispatch is limited to Unity and UNKNOWN headers.
- Schema snapshot changes are limited to DraftHuman payload keys.
- Corpus/golden replay coverage remains correctly documented as unverified.
- No protected workbook/webhook/App Script/state/final reconciliation surfaces changed.

Validation to run:
py -m pytest -q tests\test_draft_human_parser.py tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_draft_bot_parser.py tests\test_router_unit.py tests\test_parsers.py
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
py -m ruff check src tests tools
git diff --check
@'
docs/contracts/parser_draft_human.md
docs/implementation_handoffs/parser_draft_human_comparison.md
src/mythic_edge_parser/parsers/draft_human.py
src/mythic_edge_parser/parsers/__init__.py
src/mythic_edge_parser/router.py
tests/test_draft_human_parser.py
tests/test_router_unit.py
tests/test_event_schema_snapshots.py
tests/fixtures/schema_snapshots/parser_payload_keys.json
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin

Do not:
- Copy Manasight code.
- Add DraftComplete behavior.
- Change DraftBot behavior beyond reviewing that it remains preserved.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates.
- Stage, commit, open a PR, close issues, or mark trackers complete unless explicitly asked.

Final review report must include:
- findings first, ordered by severity
- contract matches
- contract mismatches, if any
- missing tests or safeguards
- validation run and result
- protected-surface status
- remaining unverified layers
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/123"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  contract_artifact: "docs/contracts/parser_draft_human.md"
  implementation_artifact: "docs/implementation_handoffs/parser_draft_human_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  files_changed:
    - "src/mythic_edge_parser/parsers/draft_human.py"
    - "src/mythic_edge_parser/parsers/__init__.py"
    - "src/mythic_edge_parser/router.py"
    - "tests/test_draft_human_parser.py"
    - "tests/test_router_unit.py"
    - "tests/test_event_schema_snapshots.py"
    - "tests/fixtures/schema_snapshots/parser_payload_keys.json"
    - "docs/implementation_handoffs/parser_draft_human_comparison.md"
  validation:
    - "py -m pytest -q tests\\test_draft_human_parser.py tests\\test_event_schema_snapshots.py -> 47 passed"
    - "py -m pytest -q tests\\test_draft_bot_parser.py tests\\test_router_unit.py tests\\test_parsers.py -> 70 passed"
    - "py -m pytest -q tests\\test_parser_small_modules.py tests\\test_feature_equity_corpus_ratchet.py tests\\test_golden_replay_harness.py -> 45 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "new/untracked file trailing-whitespace scan -> no matches"
    - "protected-surface gate -> passed"
    - "path-scoped protected-surface gate -> passed with 0 forbidden, 2 authorized parser-surface warnings"
  remaining_unverified:
    - "Live MTGA human draft payload field names"
    - "Golden replay DraftHuman fixture coverage"
    - "Feature-equity corpus nonzero DraftHuman coverage"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
  stop_conditions:
    - "Do not copy Manasight code."
    - "Do not add DraftComplete behavior."
    - "Do not change DraftBot behavior."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates."
    - "Do not target main."
    - "Do not mark tracker #47 or related tracker #11 complete."
```
