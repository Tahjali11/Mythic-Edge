# Parser DraftBot Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/122

## Tracker

- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- related tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/parser_draft_bot.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed:

```text
## codex/parser-reliability-intelligence...origin/codex/parser-reliability-intelligence
```

Initial status before editing showed only the untracked DraftBot contract:

```text
?? docs/contracts/parser_draft_bot.md
```

Final status before handoff validation:

```text
 M src/mythic_edge_parser/parsers/__init__.py
 M src/mythic_edge_parser/router.py
 M tests/fixtures/schema_snapshots/parser_payload_keys.json
 M tests/test_event_schema_snapshots.py
 M tests/test_router_unit.py
?? docs/contracts/parser_draft_bot.md
?? src/mythic_edge_parser/parsers/draft_bot.py
?? tests/test_draft_bot_parser.py
```

The untracked contract is the source artifact from Codex B. No unrelated
worktree files were absorbed.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- GitHub issue #122
- `docs/problem_representations/parser_feature_equity_with_manasight.md`
- `docs/contracts/parser_draft_bot.md`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- durable parser patterns in `event_lifecycle.py`, `rank.py`, `session.py`,
  `collection.py`, and `inventory.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_feature_equity_corpus_ratchet.py`
- `tests/test_golden_replay_harness.py`
- `tests/test_router_unit.py`
- `tests/test_parsers.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`

## Current Behavior Compared To Contract

Expected behavior from the contract:

- Recognize exact, case-sensitive Quick Draft / bot draft API markers:
  - `BotDraftDraftStatus`
  - `BotDraftDraftPick`
- Emit `DraftBotEvent` with `kind == "DraftBot"` and
  `PerformanceClass.DURABLE_PER_EVENT`.
- Preserve event metadata raw bytes.
- Normalize stable draft evidence fields for draft identity, event identity,
  status, pack/pick position, offered card IDs, and picked card evidence.
- Preserve the full parsed top-level JSON object under `raw_draft_bot`.
- Route from `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN` headers only.
- Keep DraftHuman and DraftComplete out of scope.

Observed pre-change behavior:

- `DraftBotEvent` already existed with the correct kind and performance class.
- The public `GameEvent` union already included `DraftBotEvent`.
- No `src/mythic_edge_parser/parsers/draft_bot.py` module existed.
- `parsers.__init__` did not expose `draft_bot`.
- `router.py` did not dispatch to a DraftBot parser.
- `tests/test_event_schema_snapshots.py` had no DraftBot payload samples.
- `parser_payload_keys.json` had no `DraftBot.*` payload key entries.
- The feature-equity corpus baseline still recorded zero `DraftBot` counts.

Gap:

The event class existed, but no parser path could emit it. That meant Mythic
Edge had an event model placeholder, not first-class bot draft parser feature
equity.

## Implementation Option Chosen

Implemented the minimum parser/test/snapshot scope required by the contract.

Not implemented in this pass:

- No DraftHuman or DraftComplete behavior.
- No golden replay fixture.
- No feature-equity corpus baseline update.
- No parser state, workbook, webhook, Apps Script, runtime, or production
  behavior changes.

Reason:

The contract makes focused parser tests, router/package reachability, and
schema snapshot samples the minimum implementation evidence. Golden/corpus
coverage is optional only if safe committed draft fixture evidence can be added
without scope expansion. No safe committed draft fixture source was present, so
corpus coverage remains explicitly unverified.

## What Changed

Added first-class DraftBot parser support:

- New parser module `src/mythic_edge_parser/parsers/draft_bot.py`.
- Parser package import and `__all__` exposure for `draft_bot`.
- Router dispatch for `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN` headers.
- Focused parser and router tests in `tests/test_draft_bot_parser.py`.
- Router order expectations updated in `tests/test_router_unit.py`.
- Schema snapshot sample coverage for `bot_draft_status` and `bot_draft_pick`.
- Payload key snapshot entries for:
  - `DraftBot.bot_draft_status`
  - `DraftBot.bot_draft_pick`

## Files Changed

- `src/mythic_edge_parser/parsers/draft_bot.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_draft_bot_parser.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `docs/implementation_handoffs/parser_draft_bot_comparison.md`

Source artifact present but not edited by Codex C:

- `docs/contracts/parser_draft_bot.md`

## Code Changed

Yes.

Runtime parser code changed only in the contract-authorized DraftBot parser
surface:

- `draft_bot.try_parse()` now recognizes exact bot draft request/response
  markers.
- It emits one `DraftBotEvent` per recognized marker-like entry.
- It returns `None` for unrelated or malformed marker-like input.
- It preserves metadata raw bytes via `EventMetadata(timestamp, entry.body.encode())`.
- It does not import workbook, webhook, Apps Script, model-provider, AI,
  parser state, or downstream surfaces.

## Tests Added Or Updated

Added:

- `tests/test_draft_bot_parser.py`

Updated:

- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`

## Exact Parser Payload Fields Implemented

Both `bot_draft_status` and `bot_draft_pick` payloads use this stable key set:

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
raw_draft_bot
```

Normalization behavior:

- String fields accept only strings, strip whitespace, and default to `""`.
- Scalar integer fields accept non-bool nonnegative integers and digit-only
  strings, and default to `None`.
- Card ID lists accept only list containers, preserve order and duplicates, and
  skip invalid members.
- `picked_card_id` uses the scalar picked-card field when present; otherwise it
  falls back to the first normalized picked-card list value when available.
- Marker-wrapped payloads normalize from the nested marker object when it is a
  mapping.
- `raw_draft_bot` preserves the full parsed top-level JSON dictionary.

## Interface Changes

Parser-only interface changes:

- New module: `mythic_edge_parser.parsers.draft_bot`
- New public package export: `parsers.draft_bot`
- Router can now emit existing `DraftBotEvent` from Unity and UNKNOWN entries.

No changes to:

- parser event classes
- event kind values
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- match identity
- game identity
- deduplication
- runtime status file shape
- failed-post shape
- generated data
- secrets or environment variables

## Validation Run

Focused checks:

```text
py -m pytest -q tests\test_draft_bot_parser.py -> 35 passed in 0.52s
py -m pytest -q tests\test_router_unit.py -> 17 passed in 0.52s
```

Schema snapshot:

```text
py -m pytest -q tests\test_event_schema_snapshots.py -> initially failed on parser_payload_keys.json mismatch, as expected before the authorized DraftBot payload-key snapshot update
$env:MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS='1'; py -m pytest -q tests\test_event_schema_snapshots.py -> 6 passed in 0.51s
py -m pytest -q tests\test_event_schema_snapshots.py -> 6 passed in 0.56s
```

Related parser reliability checks:

```text
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py -> 45 passed in 0.91s
py -m pytest -q tests\test_router_unit.py tests\test_parsers.py -> 35 passed in 0.51s
```

Style and diff checks:

```text
py -m ruff check src tests tools -> All checks passed!
git diff --check -> passed
```

Protected-surface checks:

```text
py tools\check_protected_surfaces.py --base origin/main -> passed; 9 warnings from branch-wide parser-reliability differences against origin/main
```

Path-scoped touched-file check:

```text
@'
docs/contracts/parser_draft_bot.md
docs/implementation_handoffs/parser_draft_bot_comparison.md
src/mythic_edge_parser/parsers/draft_bot.py
src/mythic_edge_parser/parsers/__init__.py
src/mythic_edge_parser/router.py
tests/test_draft_bot_parser.py
tests/test_router_unit.py
tests/test_event_schema_snapshots.py
tests/fixtures/schema_snapshots/parser_payload_keys.json
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result:

```text
changed_paths: 9
forbidden: 0
warnings: 2
result: passed
```

The two path-scoped warnings were for parser surfaces touched by this
contract-authorized implementation:

- `src/mythic_edge_parser/parsers/draft_bot.py`
- `src/mythic_edge_parser/parsers/__init__.py`

Secret/private-content scanner:

```text
Test-Path tools\check_secret_patterns.py -> False
```

No repo-approved secret/private-content scanner was present on this branch.

Whitespace scan:

```text
rg -n "[ \t]+$" docs\contracts\parser_draft_bot.md docs\implementation_handoffs\parser_draft_bot_comparison.md src\mythic_edge_parser\parsers\draft_bot.py tests\test_draft_bot_parser.py -> no matches
```

## Corpus And Golden Coverage Status

Not changed.

The feature-equity corpus baseline still records zero `DraftBot` counts. This
is intentional for this pass because no safe committed synthetic or sanitized
draft replay fixture was added.

Remaining corpus/golden gap:

- no committed golden replay fixture emits `DraftBot`;
- no corpus baseline update proves nonzero DraftBot counts;
- full reliability evidence should be a future scoped issue or a reviewer
  decision if a safe synthetic fixture is desired now.

## Protected-Surface Status

No forbidden surface was touched.

Contract-authorized parser surfaces touched:

- parser module package export
- router dispatch
- parser payload schema snapshot

Forbidden surfaces not touched:

- DraftHuman behavior
- DraftComplete behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- match identity
- game identity
- deduplication
- secrets or environment variables
- raw private logs
- generated card/tier/oracle data
- runtime status files
- failed posts
- workbook exports
- production behavior
- CI gates

## Still Unverified

- Live MTGA bot draft payload field names.
- Whether MTGA emits status and pick as requests, responses, or both in every
  client version.
- Whether pack/pick indexes are zero-based or one-based. The parser preserves
  observed values without conversion.
- Golden replay coverage for DraftBot.
- Feature-equity corpus nonzero `DraftBot` coverage.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.

## Reviewer Focus

Codex E should pay special attention to:

- exact marker matching and false-positive behavior;
- first-marker policy when multiple bot draft markers appear in one entry;
- integer normalization rejecting booleans, floats, negative values, signed
  strings, containers, and blank strings;
- marker-wrapped payload behavior and `raw_draft_bot` preservation;
- router dispatch order after `event_lifecycle` and before `rank`;
- schema snapshot payload-key order;
- whether leaving golden/corpus coverage unimplemented is acceptable for this
  first pass.

## Next Workflow Action

Next role: Codex E / Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #122:
https://github.com/Tahjali11/Mythic-Edge/issues/122

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/parser_draft_bot.md

Implementation handoff:
docs/implementation_handoffs/parser_draft_bot_comparison.md

Review the implementation against the contract and lead with findings ordered by severity.

Inspect:
- git status and diff
- docs/contracts/parser_draft_bot.md
- docs/implementation_handoffs/parser_draft_bot_comparison.md
- src/mythic_edge_parser/parsers/draft_bot.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/router.py
- tests/test_draft_bot_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Review for:
- exact, case-sensitive marker matching for BotDraftDraftStatus and BotDraftDraftPick
- no DraftHuman or DraftComplete behavior
- stable payload key set and normalization defaults
- raw_draft_bot preserving the full parsed top-level object
- malformed/partial payload behavior
- router/package reachability from Unity and UNKNOWN headers only
- schema snapshot key order and snapshot safety
- whether focused tests fully cover the contract-required behavior
- whether the unimplemented golden/corpus fixture coverage is acceptable as a documented remaining gap
- whether protected surfaces stayed within contract-authorized scope

Suggested validation:
py -m pytest -q tests\test_draft_bot_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
py -m pytest -q tests\test_router_unit.py tests\test_parsers.py
py -m ruff check src tests tools
git diff --check
@'
docs/contracts/parser_draft_bot.md
docs/implementation_handoffs/parser_draft_bot_comparison.md
src/mythic_edge_parser/parsers/draft_bot.py
src/mythic_edge_parser/parsers/__init__.py
src/mythic_edge_parser/router.py
tests/test_draft_bot_parser.py
tests/test_router_unit.py
tests/test_event_schema_snapshots.py
tests/fixtures/schema_snapshots/parser_payload_keys.json
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin

Do not:
- Change parser behavior during review.
- Add DraftHuman or DraftComplete behavior.
- Add raw private Player.log excerpts.
- Update golden fixtures or corpus baselines unless the user explicitly routes you to a fixer/implementation pass.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates.
- Stage, commit, open a PR, merge, close issue #122, or mark trackers complete.

Final review must include:
- role performed
- issue and trackers
- contract reviewed
- implementation handoff reviewed
- files inspected
- findings
- validation run and result
- protected-surface status
- remaining unverified layers
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/122"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "GitHub issue #122 and docs/contracts/parser_draft_bot.md"
  target_artifact: "docs/implementation_handoffs/parser_draft_bot_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "py -m pytest -q tests\\test_draft_bot_parser.py -> 35 passed"
    - "py -m pytest -q tests\\test_event_schema_snapshots.py -> 6 passed"
    - "py -m pytest -q tests\\test_parser_small_modules.py tests\\test_feature_equity_corpus_ratchet.py tests\\test_golden_replay_harness.py -> 45 passed"
    - "py -m pytest -q tests\\test_router_unit.py tests\\test_parsers.py -> 35 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_protected_surfaces.py --base origin/main -> passed with branch-wide warnings"
    - "path-scoped protected-surface check over touched files -> passed with 2 contract-authorized parser warnings"
  remaining_unverified:
    - "Live MTGA bot draft payload field names"
    - "Golden replay DraftBot fixture coverage"
    - "Feature-equity corpus nonzero DraftBot coverage"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
  stop_conditions:
    - "Do not copy Manasight code."
    - "Do not paste or commit raw private Player.log excerpts."
    - "Do not add DraftHuman or DraftComplete behavior."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates."
    - "Do not target main."
    - "Do not mark tracker #47 or related tracker #11 complete."
```
