# Parser DraftHuman Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/123
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- related_tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- branch_target: codex/parser-reliability-intelligence
- source_problem_representation: GitHub issue #123
- source_feature_equity_artifact: docs/problem_representations/parser_feature_equity_with_manasight.md
- draft_surface_reconciliation: docs/contracts/parser_draft_surface_parity_recommendation.md
- prior_draftbot_contract: docs/contracts/parser_draft_bot.md
- prior_draftbot_commit: 02df882538d607d32e43a5544422035ae8c25db1
- prior_scope_reconciliation_commit: fa126f281417702e5e66b6e046e7bb4e22745f0c
- target_artifact: docs/contracts/parser_draft_human.md
- expected_next_artifact: docs/implementation_handoffs/parser_draft_human_comparison.md
- risk_tier: High
- status: contract only

Required agent docs:

- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

## Purpose

Mythic Edge should treat Premier and Traditional human draft log evidence as a
first-class parser-owned event surface.

Plain English: when MTGA emits human draft pack, pick, or business-event pick
evidence, the parser should recognize the exact human draft markers, emit the
existing `DraftHumanEvent`, preserve the raw parsed payload, and expose a small
stable payload for draft identity, pack/pick position, available pack cards,
and picked-card evidence where the log provides those values.

Feature equity with the local Manasight reference means evidence coverage and
testable parser behavior. It does not mean copying Manasight source code,
matching Manasight internals, or expanding into draft advice.

This contract does not implement code. It does not authorize workbook,
webhook, Apps Script, match/game final reconciliation, DraftComplete behavior,
coaching, card rating, or deck construction changes.

## Owning Layer

Owning truth layer: parser event recognition and parser payload normalization.

The parser owns:

- human draft marker recognition
- `DraftHumanEvent` emission
- stable DraftHuman payload `type` values
- parser-owned normalized draft evidence fields
- raw parsed draft payload preservation
- malformed and partial payload degradation behavior
- false-positive separation from DraftBot and DraftComplete markers

The parser does not own in this module:

- draft completion parsing
- bot draft parsing changes
- draft pick coaching
- card ratings
- draft advice
- deck construction analytics
- hidden-information inference
- match identity or game identity
- match/game final reconciliation
- workbook row schema
- webhook payload shape
- Apps Script behavior
- AI or model-provider interpretation

Downstream systems may consume `DraftHuman` events as parser-owned draft
evidence. They must not turn draft helper sheets, dashboards, Apps Script,
webhooks, or AI output into the source of draft truth.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/parser_draft_human.md

Future implementation files owned or authorized by this contract:

- src/mythic_edge_parser/parsers/draft_human.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/router.py
- tests/test_draft_human_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json
- optional committed sanitized or synthetic golden replay fixture and manifest
  files under existing fixture locations, only if Codex C adds corpus coverage
  under the safety rules below
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json,
  only if a committed golden replay fixture is added and the count-only
  baseline must be updated
- docs/implementation_handoffs/parser_draft_human_comparison.md
- docs/contract_test_reports/parser_draft_human.md

Referenced but not silently owned:

- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/parsers/draft_bot.py
- src/mythic_edge_parser/log/entry.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- docs/contracts/parser_draft_bot.md
- docs/contracts/parser_draft_surface_parity_recommendation.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/player_log_evidence_ledger.md

`events.py` already defines `DraftHumanEvent`. This contract does not
authorize a new event class or a changed event `kind` value. If Codex C
discovers that `DraftHumanEvent` is missing or inconsistent on the active
branch, it must route back to Codex B instead of inventing a replacement event
model.

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence`:

- `src/mythic_edge_parser/events.py` defines `DraftHumanEvent`.
- `DraftHumanEvent.kind == "DraftHuman"`.
- `DraftHumanEvent.performance_class == PerformanceClass.DURABLE_PER_EVENT`.
- `DraftHumanEvent` is included in the public `GameEvent` union.
- `tests/fixtures/schema_snapshots/parser_event_classes.json` includes the
  `DraftHumanEvent` class and kind.
- `src/mythic_edge_parser/parsers/draft_bot.py` exists and handles only
  `BotDraftDraftStatus` and `BotDraftDraftPick`.
- DraftBot focused tests reject `Draft.Notify`, `EventPlayerDraftMakePick`,
  `LogBusinessEvents`, `PickGrpId`, and `DraftCompleteDraft` as DraftBot.
- `src/mythic_edge_parser/parsers/__init__.py` does not import `draft_human`.
- `src/mythic_edge_parser/router.py` does not dispatch to a human draft parser.
- `src/mythic_edge_parser/parsers/` has no `draft_human.py` module.
- `tests/test_event_schema_snapshots.py` has no `DraftHuman` payload sample.
- `tests/fixtures/schema_snapshots/parser_payload_keys.json` has no
  `DraftHuman.*` payload entries.
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
  records zero `DraftHuman` counts.
- No focused human draft parser tests were found.

The current behavior is not a runtime bug by itself. It is a feature-equity
gap: the event class exists, but no parser path can emit it.

## Public Interface

### Parser Module

Add a dedicated parser module:

```python
src/mythic_edge_parser/parsers/draft_human.py
```

Required public parser hook:

```python
from datetime import datetime

from mythic_edge_parser.events import GameEvent
from mythic_edge_parser.log.entry import LogEntry


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    ...
```

Required behavior:

- Return one `DraftHumanEvent` for one recognized human draft marker entry.
- Return `None` for unrelated entries.
- Never raise for malformed marker-like input in normal parser use.
- Preserve provenance with `EventMetadata(timestamp, entry.body.encode())`.
- Keep helper functions private unless a later contract makes them public.
- Do not import workbook, webhook, Apps Script, model-provider, AI, parser
  state, or downstream surfaces.

### Public Constants

The implementation should define narrow marker constants in `draft_human.py`.
Exact constant names may vary, but they must represent these marker values:

```python
DRAFT_NOTIFY_MARKER = "Draft.Notify"
EVENT_PLAYER_DRAFT_MAKE_PICK_MARKER = "EventPlayerDraftMakePick"
LOG_BUSINESS_EVENTS_MARKER = "LogBusinessEvents"
```

Marker matching must be exact and case-sensitive. Because `Draft.Notify`
contains a dot, Codex C must not rely on an unescaped generic API-name regex
that treats `.` as any character or that cannot match dotted names.

### Event Kind

Required event class:

- `DraftHumanEvent`

Required event `kind`:

- `"DraftHuman"`

Required performance class:

- `PerformanceClass.DURABLE_PER_EVENT`

The implementation must not add a new draft event class for human draft
support. `DraftBotEvent` behavior is already complete for issue #122.
`DraftCompleteEvent` remains out of scope for issue #123.

## Recognized Markers

V1 recognized human draft markers:

| Marker | Payload `type` | Meaning |
| --- | --- | --- |
| `Draft.Notify` | `human_draft_notify` | Human draft notification or pack presentation evidence. |
| `EventPlayerDraftMakePick` | `human_draft_make_pick` | Human draft pick submission or picked-card confirmation evidence. |
| `LogBusinessEvents` with `PickGrpId` | `human_draft_business_pick` | Business-event pick evidence for a human draft pick. |

Accepted API directions:

- request marker: `==> Draft.Notify`
- response marker: `<== Draft.Notify`
- request marker: `==> EventPlayerDraftMakePick`
- response marker: `<== EventPlayerDraftMakePick`
- request marker: `==> LogBusinessEvents`
- response marker: `<== LogBusinessEvents`

The payload must include the observed direction:

- `"request"` when the exact marker follows `==>`
- `"response"` when the exact marker follows `<==`
- `"unknown"` only if Codex C proves with focused tests that an exact marker
  can appear without the standard API request/response prefix

`LogBusinessEvents` recognition is narrower than ordinary marker detection:

- A `LogBusinessEvents` entry must emit `DraftHumanEvent` only when the parsed
  payload contains a recognized `PickGrpId` alias in the top-level object,
  marker-wrapped object, or first matching business-event object.
- A `LogBusinessEvents` entry without pick-card evidence must return `None`.
- The parser must not classify all business events as draft evidence.

If multiple recognized human draft markers appear in one entry, the parser must
use a deterministic first-marker policy and emit at most one event. If later
safe evidence proves that one `LogBusinessEvents` payload contains multiple
separate draft picks that must be preserved, Codex C must route back to Codex B
before implementing multi-event emission.

Unknown future draft markers are out of scope. The parser must not classify
`BotDraftDraftStatus`, `BotDraftDraftPick`, or `DraftCompleteDraft` as
`DraftHuman`.

## Input Shapes

Primary input:

- `LogEntry` from `src/mythic_edge_parser/log/entry.py`
- expected headers: `EntryHeader.UNITY_CROSS_THREAD_LOGGER` and
  `EntryHeader.UNKNOWN`
- body text containing an exact recognized human draft API marker and a JSON
  object parseable by `api_common.parse_json_from_body()`

Accepted JSON payload shapes:

1. Direct object:

```json
{
  "draftId": "draft-1",
  "eventId": "PremierDraft_Example",
  "packNumber": 1,
  "pickNumber": 2,
  "packCards": [1001, 1002],
  "PickGrpId": 1001
}
```

2. Marker-wrapped object:

```json
{
  "EventPlayerDraftMakePick": {
    "draftId": "draft-1",
    "pickNumber": 2,
    "PickGrpId": 1001
  }
}
```

3. Business-event object:

```json
{
  "LogBusinessEvents": [
    {
      "EventName": "DraftPick",
      "PickGrpId": 1001,
      "PackNumber": 1,
      "PickNumber": 2
    }
  ]
}
```

For marker-wrapped objects, normalized fields come from the nested marker
object when it is a mapping. For `LogBusinessEvents`, normalized fields may
come from the first mapping that contains a recognized picked-card alias.
`raw_draft_human` still preserves the full parsed top-level object.

If a marker is present but the first decodable JSON value is not a dictionary,
the parser returns `None`.

## Output Payload

All DraftHuman payload types must share one stable key set so downstream and
snapshot tests can reason about DraftHuman uniformly.

Required payload keys, in this order:

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

### Field Contracts

| Field | Type | Required behavior |
| --- | --- | --- |
| `type` | `str` | `"human_draft_notify"`, `"human_draft_make_pick"`, or `"human_draft_business_pick"`. |
| `source_method` | `str` | Exact observed marker: `"Draft.Notify"`, `"EventPlayerDraftMakePick"`, or `"LogBusinessEvents"`. |
| `api_direction` | `str` | `"request"`, `"response"`, or narrowly justified `"unknown"`. |
| `draft_id` | `str` | Stripped draft id when present as a string; otherwise `""`. |
| `event_id` | `str` | Stripped event id/name when present as a string; otherwise `""`. |
| `draft_status` | `str` | Stripped draft status/state when present as a string; otherwise `""`. |
| `pack_number` | `int | None` | Non-bool integer or integer-like string when present; otherwise `None`. |
| `pick_number` | `int | None` | Non-bool integer or integer-like string when present; otherwise `None`. |
| `pack_card_ids` | `list[int]` | Normalized nonnegative Arena card/grp IDs from the offered pack list; otherwise `[]`. |
| `picked_card_id` | `int | None` | Normalized nonnegative picked card/grp ID when present; otherwise `None`. |
| `picked_card_ids` | `list[int]` | Normalized nonnegative picked card/grp IDs when a list is present; may contain `picked_card_id`; otherwise `[]`. |
| `business_event_type` | `str` | Stripped business-event type/name when present as a string; otherwise `""`. |
| `raw_draft_human` | `dict[str, Any]` | Full parsed top-level JSON object from the log entry. |

### Source Field Aliases

V1 normalized fields may use these source aliases.

| Normalized field | Accepted source aliases |
| --- | --- |
| `draft_id` | `draftId`, `DraftId`, `draftID` |
| `event_id` | `eventId`, `EventId`, `eventID`, `eventName`, `EventName` |
| `draft_status` | `draftStatus`, `DraftStatus`, `status`, `state` |
| `pack_number` | `packNumber`, `PackNumber`, `pack`, `Pack` |
| `pick_number` | `pickNumber`, `PickNumber`, `pick`, `Pick` |
| `pack_card_ids` | `packCardIds`, `packCards`, `PackCards`, `cards`, `Cards`, `draftPack`, `DraftPack` |
| `picked_card_id` | `pickedCardId`, `PickedCardId`, `pickGrpId`, `PickGrpId`, `cardId`, `grpId` |
| `picked_card_ids` | `pickedCardIds`, `pickedCards`, `pickedGrpIds`, `PickedGrpIds` |
| `business_event_type` | `businessEventType`, `BusinessEventType`, `eventType`, `EventType`, `eventName`, `EventName` |

If later sanitized evidence shows different field names, Codex C must route
back to Codex B or document a contract loopback before broadening aliases.

### Normalization Rules

String fields:

- Accept only strings.
- Strip leading and trailing whitespace.
- Use `""` for missing or non-string values.

Integer fields:

- Accept `int` values except `bool`.
- Accept stripped digit-only strings such as `"2"` or `"003"`.
- Reject booleans, floats, negative numbers, negative strings, signed strings,
  blank strings, containers, and arbitrary objects.
- Use `None` for invalid scalar integers.
- Preserve the observed index number. Do not infer whether Arena used zero-based
  or one-based indexing.

Card ID lists:

- Accept only list values.
- Normalize each element with the nonnegative integer policy above.
- Preserve source order and duplicates.
- Reject booleans, floats, negative values, malformed strings, nested lists,
  mappings, and objects.
- Use `[]` for missing or non-list values.

`picked_card_id` relationship:

- When a scalar picked card id is present, use it for `picked_card_id`.
- When only `picked_card_ids` is present and nonempty, `picked_card_id` may be
  the first normalized list value.
- Do not infer a picked card from `pack_card_ids` when no picked field exists.

Business-event source selection:

- For `LogBusinessEvents`, inspect the top-level object, a nested
  `LogBusinessEvents` mapping, or entries inside a nested `LogBusinessEvents`
  list.
- Use the first mapping that contains a valid picked-card alias as the
  normalization source.
- If no such mapping exists, return `None`.
- Do not emit multiple events from one `LogBusinessEvents` entry in V1.

Raw evidence:

- Preserve the full parsed top-level JSON object in `raw_draft_human`.
- Do not store full raw private log lines outside event metadata.
- Do not resolve card names, ratings, colors, archetypes, pick quality, or deck
  construction facts in this parser.

## Malformed And Partial Payload Behavior

Required behavior:

- No recognized marker: return `None`.
- Recognized marker but no parseable JSON dictionary: return `None`.
- Recognized `LogBusinessEvents` marker without pick-card evidence: return
  `None`.
- Recognized non-business marker with parseable dictionary but missing optional
  normalized fields: emit `DraftHumanEvent` with default `""`, `None`, or `[]`
  values.
- Marker-wrapped payload where the nested marker value is not a dictionary:
  normalize from the top-level dictionary and preserve the full top-level raw
  payload.
- Invalid scalar fields must not raise and must not poison normalized output.
- Invalid list members must be skipped, not surfaced as card IDs.
- Malformed input must not write files, mutate parser state, post webhooks, or
  update workbook-facing rows.

False positives:

- Case variants such as `draft.notify` or `eventplayerdraftmakepick` must not
  match.
- Bot draft markers must not match `DraftHuman`.
- Draft completion markers must not match `DraftHuman`.
- `LogBusinessEvents` without `PickGrpId` or an accepted picked-card alias must
  not match.
- Generic prose containing `draft`, `pack`, `pick`, `human`, or `PickGrpId`
  must not match unless the exact marker and payload contract are satisfied.

## Router And Package Expectations

Package import:

- Add `draft_human` to `src/mythic_edge_parser/parsers/__init__.py`.
- Add `"draft_human"` to `__all__`.

Router dispatch:

- Add `parsers.draft_human` to `EntryHeader.UNITY_CROSS_THREAD_LOGGER`.
- Add `parsers.draft_human` to `EntryHeader.UNKNOWN`.
- Do not add it to `EntryHeader.METADATA`, `EntryHeader.CLIENT_GRE`,
  `EntryHeader.TRUNCATION_MARKER`, `EntryHeader.CONNECTION_MANAGER`, or
  `EntryHeader.MATCHMAKING`.

Recommended ordering:

- Place `draft_human` after `parsers.draft_bot` and before `parsers.rank` in
  both the Unity and UNKNOWN dispatch tuples.
- When issue #124 later adds `draft_complete`, route order should be revisited
  by that contract instead of changed preemptively here.

Rationale:

- Human draft markers are durable API-style events.
- The parser must be reachable from current API log entries.
- The parser is marker-specific and should not shadow GRE, client action,
  match-state, session, lifecycle, DraftBot, rank, collection, or inventory
  parsing.

If Codex C finds that real or sanitized evidence requires different routing, it
must document the reason in the implementation handoff and route back to Codex
B if the route would broaden parser behavior beyond this contract.

## Schema Snapshot Expectations

Required snapshot changes when Codex C implements the parser:

- `tests/test_event_schema_snapshots.py` must import `draft_human`.
- `tests/test_event_schema_snapshots.py` must include representative
  `DraftHuman` sample events for:
  - `human_draft_notify`
  - `human_draft_make_pick`
  - `human_draft_business_pick`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json` must include:
  - `DraftHuman.human_draft_notify`
  - `DraftHuman.human_draft_make_pick`
  - `DraftHuman.human_draft_business_pick`
- Snapshot entries must include only stable payload keys, not raw nested payload
  values.

Expected payload key order for all DraftHuman sample entries:

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

`parser_event_classes.json` already includes `DraftHumanEvent` on the current
branch. If that snapshot changes during implementation, Codex C must explain
why. Adding the parser should not require changing the event class snapshot.

Snapshot updates require the same explicit issue/contract/review approval rules
as existing schema snapshots. Do not auto-update snapshots as a way to hide an
unreviewed payload shape change.

## Corpus And Golden Evidence Expectations

The current feature-equity corpus baseline records zero `DraftHuman` events.
That zero count is accurate until a committed sanitized or synthetic golden
replay fixture exercises DraftHuman through the normal `LineBuffer` and
`Router` path.

Minimum implementation evidence:

- focused parser tests for `draft_human.try_parse()`
- router/package reachability tests
- schema snapshot sample coverage for all three payload types

Full reliability evidence:

- one small committed sanitized or synthetic golden replay fixture and manifest
  that emits at least one `human_draft_notify`, one
  `human_draft_make_pick`, and one `human_draft_business_pick` event through
  the normal replay path
- feature-equity corpus ratchet baseline updates that change `DraftHuman`
  counts from zero only when the committed fixture is added

Golden/corpus safety rules:

- Do not commit raw private `Player.log` data.
- Do not copy private draft logs into tests or docs.
- Prefer synthetic draft-only fixture lines when possible.
- Any committed fixture must satisfy `docs/contracts/parser_golden_replay_harness.md`.
- Any count-only baseline update must explain whether the count changed because
  parser support was added, fixture coverage was added, or both.
- If Codex C cannot add a safe committed fixture in the implementation pass, it
  must leave corpus coverage as a remaining unverified layer and should not
  claim full corpus feature equity.

## Compatibility

Existing compatibility requirements:

- `DraftHumanEvent.kind` stays `"DraftHuman"`.
- `DraftHumanEvent.performance_class` stays `DurablePerEvent`.
- `DraftBotEvent` behavior from issue #122 stays unchanged.
- `DraftCompleteEvent` remains a separate event family for issue #124.
- Existing parser payloads, workbook row keys, webhook payloads, Apps Script
  field maps, runtime status files, failed-post files, and generated data
  remain unchanged.
- Existing `api_common` behavior remains unchanged unless a future contract
  explicitly authorizes shared helper changes.
- `MatchSummary`, `GameSummary`, parser state, and final reconciliation ignore
  `DraftHuman` unless a later contract explicitly defines draft-to-match state
  behavior.

## Side Effects

Allowed future side effects in Codex C:

- read `LogEntry.body`
- build in-memory `DraftHumanEvent` objects
- add source parser code
- add focused tests
- update parser payload schema snapshots for DraftHuman payload keys
- optionally add reviewed sanitized or synthetic golden replay fixture files and
  count-only corpus baseline updates if all fixture safety rules are met
- write the implementation handoff

Forbidden side effects:

- no DraftComplete behavior
- no DraftBot behavior change
- no parser state final reconciliation changes
- no workbook schema changes
- no webhook payload shape changes
- no Apps Script changes
- no match/game identity changes
- no deduplication changes
- no event class or event kind changes
- no raw private log commits
- no runtime status file changes
- no failed-post changes
- no workbook export changes
- no generated card/tier/oracle data changes
- no secrets, credentials, tokens, API keys, webhook URLs, or environment
  variable contract changes
- no CI gate changes
- no production behavior changes
- no draft pick coaching, ratings, AI draft advice, or deck construction
  analytics

## Dependency Order

Codex C should proceed in this order:

1. Confirm branch is `codex/parser-reliability-intelligence` and inspect
   `git status --short --branch`.
2. Read this contract and issue #123.
3. Compare current event/router/parser/test surfaces against this contract.
4. Add focused tests for `draft_human.try_parse()` behavior.
5. Add `src/mythic_edge_parser/parsers/draft_human.py`.
6. Add parser package import and router dispatch.
7. Add or update router/package reachability tests.
8. Add schema snapshot sample events and update payload-key snapshot only after
   tests define the expected DraftHuman payload shape.
9. Decide whether a safe synthetic/sanitized golden replay fixture is in scope.
   If yes, add it and update count-only corpus baseline with review notes. If
   no, record corpus coverage as remaining unverified.
10. Run validation.
11. Produce `docs/implementation_handoffs/parser_draft_human_comparison.md`.
12. Route to Codex E for contract-test review.

Stop and route back to Codex B if:

- exact source field names from safe evidence do not fit this contract
- implementation needs a shared `api_common` behavior change
- implementation requires multi-event emission from one `LogBusinessEvents`
  entry
- implementation requires a new event class or changed `kind`
- implementation requires DraftComplete behavior
- implementation requires workbook, webhook, Apps Script, state, final
  reconciliation, match/game identity, or deduplication changes
- safe fixture coverage would require committing raw private logs

## Tests Required

Focused parser tests, expected in `tests/test_draft_human_parser.py`, must
cover:

- `Draft.Notify` request or response marker emits `DraftHumanEvent` with
  `type="human_draft_notify"`
- `EventPlayerDraftMakePick` request or response marker emits
  `DraftHumanEvent` with `type="human_draft_make_pick"`
- `LogBusinessEvents` with `PickGrpId` or an accepted picked-card alias emits
  `DraftHumanEvent` with `type="human_draft_business_pick"`
- `LogBusinessEvents` without picked-card evidence returns `None`
- event kind and performance class are correct
- metadata timestamp and raw bytes are preserved
- `source_method` and `api_direction` are populated
- direct payload shape normalizes common fields
- marker-wrapped payload shape normalizes nested fields while preserving the
  full top-level raw payload
- business-event list shape uses the first mapping with picked-card evidence
  and preserves the full top-level raw payload
- missing optional fields emit default values for non-business markers
- integer-like strings are accepted for indexes and card IDs
- booleans, floats, negative values, signed strings, blank strings, containers,
  and arbitrary objects are rejected for numeric fields
- non-list card containers produce empty lists
- invalid list members are skipped without raising
- malformed JSON returns `None`
- unrelated entries return `None`
- marker matching is exact and case-sensitive, including dotted
  `Draft.Notify`
- DraftBot and DraftComplete markers do not emit `DraftHuman`
- false-positive prose does not emit `DraftHuman`

Router/package tests must cover:

- `parsers.draft_human` is imported through
  `src/mythic_edge_parser/parsers/__init__.py`
- Unity cross-thread entries route to `DraftHuman`
- UNKNOWN header entries route to `DraftHuman`
- routed DraftHuman entries increment router routed stats, not unknown stats
- non-draft entries still route through existing parsers as before
- DraftBot routing still works and stays before DraftHuman in the dispatch order

Schema snapshot tests must cover:

- `DraftHuman.human_draft_notify` payload keys
- `DraftHuman.human_draft_make_pick` payload keys
- `DraftHuman.human_draft_business_pick` payload keys
- no raw nested payload values are stored in schema snapshots

Golden/corpus tests, if Codex C adds a fixture, must cover:

- golden replay emits `DraftHuman` through the normal parser path
- the count-only corpus ratchet observes nonzero `DraftHuman` counts
- no private raw log content, local paths, secrets, workbook IDs, webhook URLs,
  generated data, runtime status files, failed posts, or workbook exports appear
  in the fixture, manifest, baseline, or report

## Validation Requirements

### Contract Writer Validation

For this Codex B pass:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/parser_draft_human.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

Because this contract is a new untracked file during the B pass, Codex B should
also run a new-file whitespace check such as:

```powershell
Select-String -Path docs\contracts\parser_draft_human.md -Pattern '[ \t]+$'
```

### Codex C Implementation Validation

Focused first:

```powershell
py -m pytest -q tests\test_draft_human_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
```

Related parser reliability checks:

```powershell
py -m pytest -q tests\test_draft_bot_parser.py tests\test_router_unit.py tests\test_parsers.py
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
```

If Codex C adds golden/corpus coverage:

```powershell
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
```

Repo-level and protected-surface validation:

```powershell
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence
```

If a repo-approved secret/private-content scanner exists on the active branch,
run it against any new fixture, manifest, snapshot, baseline, and report
fixture paths before submitter work.

## Acceptance Criteria

This contract is complete when:

- `docs/contracts/parser_draft_human.md` exists.
- The contract links issue #123, tracker #47, related tracker #11, the agent
  constitution, the Module Contract Writer rules, and the module contract
  template.
- The parser truth-owning layer is named.
- Observed current behavior is distinguished from required guarantees.
- Recognized human draft markers are exact and case-sensitive.
- `DraftHuman` event kind and payload `type` values are defined.
- Parser-owned normalized fields are defined with type and default behavior.
- Raw evidence preservation is defined.
- `LogBusinessEvents` recognition is narrowed to picked-card evidence.
- Malformed and partial payload behavior is defined.
- Router and parser package expectations are defined.
- False-positive separation from DraftBot and DraftComplete is required.
- Schema snapshot expectations are defined.
- Focused tests and optional golden/corpus evidence expectations are defined.
- Protected surfaces and out-of-scope behavior are explicit.
- The next role is Codex C for implementation/comparison.
- No code, test, snapshot, fixture, baseline, parser behavior, workbook,
  webhook, Apps Script, secret, generated-data, runtime, CI, or production
  changes are implemented by this contract thread.

## Unknowns

- Exact live MTGA human draft payload field names are not present in committed
  repo fixtures.
- It is unknown whether the log emits `Draft.Notify`,
  `EventPlayerDraftMakePick`, and `LogBusinessEvents` as requests, responses,
  or both for all client versions.
- It is unknown whether `LogBusinessEvents` carries one pick event or can carry
  multiple pick events in one entry. V1 must emit at most one event and route
  back to Codex B if multi-event preservation is required.
- It is unknown whether pack/pick indexes are zero-based or one-based. V1 must
  preserve observed values without conversion.
- It is unknown whether `draft_id` and `event_id` are always present in human
  draft payloads.
- It is unknown whether card IDs appear as `PickGrpId`, `grpId`, `cardId`, or
  another field in all client versions.
- It is unknown whether a safe synthetic golden replay fixture can be added
  without expanding the implementation pass.

## Suspected Implementation Gaps

- No DraftHuman parser module exists.
- Router dispatch cannot currently emit `DraftHuman`.
- Payload schema snapshots do not include DraftHuman payload keys.
- Focused tests do not protect human draft marker recognition, false positives,
  malformed input, business-event narrowing, or normalization rules.
- The feature-equity corpus ratchet currently records DraftHuman zero counts.
- There is no committed golden replay fixture for human draft evidence.

These are contract findings, not authorization for Codex B to change behavior.

## Next Workflow Action

Recommended next role: Codex C / Module Implementer.

Codex C should compare current code to this contract, implement the smallest
coherent parser/test/snapshot changes required, and produce
`docs/implementation_handoffs/parser_draft_human_comparison.md`.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #123:
https://github.com/Tahjali11/Mythic-Edge/issues/123

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/parser_draft_human.md

Goal:
Compare the current parser/event/router/tests/snapshots/corpus surfaces against docs/contracts/parser_draft_human.md, then implement the smallest coherent first-class Premier/Traditional human draft parser support required by the contract. Produce docs/implementation_handoffs/parser_draft_human_comparison.md.

Context:
- Issue #122 DraftBot parser scope is complete and closed.
- DraftBot implementation commit: 02df882538d607d32e43a5544422035ae8c25db1
- Scope reconciliation commit: fa126f281417702e5e66b6e046e7bb4e22745f0c
- Issue #124 remains open for DraftComplete and must stay separate.

Before editing:
- Confirm the branch is codex/parser-reliability-intelligence and inspect git status.
- State what DraftHuman parsing is supposed to do, what the repo currently does, what gap remains, why it exists, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/parser_draft_human.md
- docs/contracts/parser_draft_bot.md
- docs/contracts/parser_draft_surface_parity_recommendation.md
- docs/problem_representations/parser_feature_equity_with_manasight.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/player_log_evidence_ledger.md
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/parsers/draft_bot.py
- tests/test_draft_bot_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/test_feature_equity_corpus_ratchet.py
- tests/test_golden_replay_harness.py

Implement only if the contract is implementable as written:
- src/mythic_edge_parser/parsers/draft_human.py
- parser package import and router dispatch for Unity and UNKNOWN headers
- focused tests, expected in tests/test_draft_human_parser.py
- DraftHuman parser payload schema snapshot samples
- optional safe synthetic/sanitized golden replay and corpus baseline update only if it can be done without private raw logs or scope expansion

Do not:
- Copy Manasight code.
- Paste or commit raw private Player.log excerpts.
- Add DraftComplete behavior.
- Change DraftBot behavior.
- Add draft coaching, card ratings, AI draft advice, pick-quality evaluation, or deck construction analytics.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates.
- Target main.
- Mark #47 or #11 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
py -m pytest -q tests\test_draft_human_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_draft_bot_parser.py tests\test_router_unit.py tests\test_parsers.py
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence

If golden/corpus coverage is added, also run:
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json

Final handoff must include:
- role performed
- issue and trackers used
- contract used
- files changed
- code changed
- tests/snapshots/fixtures/baselines changed
- exact parser payload fields implemented
- validation run and result
- protected-surface status
- corpus/golden coverage status
- remaining unverified layers
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/123"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer"
  source_artifact: "GitHub issue #123; docs/problem_representations/parser_feature_equity_with_manasight.md; docs/contracts/parser_draft_surface_parity_recommendation.md"
  contract_artifact: "docs/contracts/parser_draft_human.md"
  target_artifact: "docs/implementation_handoffs/parser_draft_human_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "new-file trailing-whitespace scan for docs/contracts/parser_draft_human.md"
    - "path-scoped protected-surface check for docs/contracts/parser_draft_human.md"
  stop_conditions:
    - "Do not copy Manasight code."
    - "Do not paste or commit raw private Player.log excerpts."
    - "Do not add DraftComplete behavior."
    - "Do not change DraftBot behavior."
    - "Do not add draft coaching, card ratings, AI draft advice, pick-quality evaluation, or deck construction analytics."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates."
    - "Do not target main."
    - "Do not mark tracker #47 or related tracker #11 complete."
```
