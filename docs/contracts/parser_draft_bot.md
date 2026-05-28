# Parser DraftBot Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/122
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- related_tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- branch_target: codex/parser-reliability-intelligence
- source_problem_representation: GitHub issue #122
- source_feature_equity_artifact: docs/problem_representations/parser_feature_equity_with_manasight.md
- target_artifact: docs/contracts/parser_draft_bot.md
- expected_next_artifact: docs/implementation_handoffs/parser_draft_bot_comparison.md
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

Mythic Edge should treat Quick Draft / bot draft log evidence as a first-class
parser-owned event surface.

Plain English: when MTGA emits bot draft status or pick evidence, the parser
should recognize the exact draft markers, emit `DraftBotEvent`, preserve the raw
parsed payload, and expose a small stable payload for draft identity, pack/pick
position, available pack cards, and picked-card evidence where the log provides
those values.

Feature equity with the local Manasight reference means evidence coverage and
testable parser behavior. It does not mean copying Manasight source code or
matching Manasight internals.

This contract does not implement code. It does not authorize workbook,
webhook, Apps Script, match/game final reconciliation, coaching, card rating,
or deck construction changes.

## Owning Layer

Owning truth layer: parser event recognition and parser payload normalization.

The parser owns:

- bot draft marker recognition
- `DraftBotEvent` emission
- stable DraftBot payload `type` values
- parser-owned normalized draft evidence fields
- raw parsed draft payload preservation
- malformed and partial payload degradation behavior

The parser does not own in this module:

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

Downstream systems may consume `DraftBot` events as parser-owned draft evidence.
They must not turn draft helper sheets, dashboards, Apps Script, webhooks, or AI
output into the source of draft truth.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/parser_draft_bot.md

Future implementation files owned or authorized by this contract:

- src/mythic_edge_parser/parsers/draft_bot.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/router.py
- tests/test_draft_bot_parser.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json
- optional committed sanitized or synthetic golden replay fixture and manifest
  files under existing fixture locations, only if Codex C adds corpus coverage
  under the safety rules below
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json,
  only if a committed golden replay fixture is added and the count-only
  baseline must be updated
- docs/implementation_handoffs/parser_draft_bot_comparison.md
- docs/contract_test_reports/parser_draft_bot.md

Referenced but not silently owned:

- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/log/entry.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/player_log_evidence_ledger.md

`events.py` already defines `DraftBotEvent`. This contract does not authorize a
new event class or a changed event `kind` value. If Codex C discovers that
`DraftBotEvent` is missing or inconsistent on the active branch, it must route
back to Codex B instead of inventing a replacement event model.

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence`:

- `src/mythic_edge_parser/events.py` defines `DraftBotEvent`.
- `DraftBotEvent.kind == "DraftBot"`.
- `DraftBotEvent.performance_class == PerformanceClass.DURABLE_PER_EVENT`.
- `DraftBotEvent` is included in the public `GameEvent` union.
- `tests/fixtures/schema_snapshots/parser_event_classes.json` includes the
  `DraftBotEvent` class and kind.
- `src/mythic_edge_parser/parsers/__init__.py` does not import `draft_bot`.
- `src/mythic_edge_parser/router.py` does not dispatch to a draft bot parser.
- `src/mythic_edge_parser/parsers/` has no `draft_bot.py` module.
- `tests/test_event_schema_snapshots.py` has no `DraftBot` payload sample.
- `tests/fixtures/schema_snapshots/parser_payload_keys.json` has no
  `DraftBot.*` payload entries.
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
  records zero `DraftBot` counts.
- No focused bot draft parser tests were found.

The current behavior is not a runtime bug by itself. It is a feature-equity gap:
the event class exists, but no parser path can emit it.

## Public Interface

### Parser Module

Add a dedicated parser module:

```python
src/mythic_edge_parser/parsers/draft_bot.py
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

- Return one `DraftBotEvent` for one recognized bot draft marker entry.
- Return `None` for unrelated entries.
- Never raise for malformed marker-like input in normal parser use.
- Preserve provenance with `EventMetadata(timestamp, entry.body.encode())`.
- Keep helper functions private unless a later contract makes them public.
- Do not import workbook, webhook, Apps Script, model-provider, or AI surfaces.

### Public Constants

The implementation should define narrow marker constants in `draft_bot.py`.
Exact constant names may vary, but they must represent these marker values:

```python
BOT_DRAFT_STATUS_MARKER = "BotDraftDraftStatus"
BOT_DRAFT_PICK_MARKER = "BotDraftDraftPick"
```

Marker matching must be exact and case-sensitive.

### Event Kind

Required event class:

- `DraftBotEvent`

Required event `kind`:

- `"DraftBot"`

Required performance class:

- `PerformanceClass.DURABLE_PER_EVENT`

The implementation must not add a new draft event class for bot draft support.
`DraftHumanEvent` and `DraftCompleteEvent` remain out of scope.

## Recognized Markers

V1 recognized bot draft markers:

| Marker | Payload `type` | Meaning |
| --- | --- | --- |
| `BotDraftDraftStatus` | `bot_draft_status` | Bot draft status or pack presentation evidence. |
| `BotDraftDraftPick` | `bot_draft_pick` | Bot draft pick submission or picked-card confirmation evidence. |

Accepted API directions:

- request marker: `==> BotDraftDraftStatus`
- response marker: `<== BotDraftDraftStatus`
- request marker: `==> BotDraftDraftPick`
- response marker: `<== BotDraftDraftPick`

The payload must include the observed direction:

- `"request"` when `api_common.is_api_request(body, marker)` matches
- `"response"` when `api_common.is_api_response(body, marker)` matches
- `"unknown"` only if Codex C proves with focused tests that an exact marker
  can appear without the standard API request/response prefix

If both request and response markers appear in one entry, the parser must use a
deterministic first-marker policy and emit at most one event. It must not emit
multiple events from one entry unless a later contract amends this behavior.

Unknown future draft markers are out of scope. The parser must not classify
`Draft.Notify`, `EventPlayerDraftMakePick`, `LogBusinessEvents`, `PickGrpId`, or
`DraftCompleteDraft` as `DraftBot`; those belong to future `DraftHuman` and
`DraftComplete` contracts.

## Input Shapes

Primary input:

- `LogEntry` from `src/mythic_edge_parser/log/entry.py`
- expected headers: `EntryHeader.UNITY_CROSS_THREAD_LOGGER` and
  `EntryHeader.UNKNOWN`
- body text containing an exact recognized bot draft API marker and a JSON
  object parseable by `api_common.parse_json_from_body()`

Accepted JSON payload shapes:

1. Direct object:

```json
{
  "draftId": "draft-1",
  "eventId": "QuickDraft_Example",
  "packNumber": 1,
  "pickNumber": 2,
  "packCards": [1001, 1002],
  "pickedCardId": 1001
}
```

2. Marker-wrapped object:

```json
{
  "BotDraftDraftPick": {
    "draftId": "draft-1",
    "pickNumber": 2,
    "pickedCardId": 1001
  }
}
```

For marker-wrapped objects, normalized fields come from the nested marker
object when it is a mapping. `raw_draft_bot` still preserves the full parsed
top-level object.

If a marker is present but the first decodable JSON value is not a dictionary,
the parser returns `None`.

## Output Payload

Both payload types must share one stable key set so downstream and snapshot
tests can reason about DraftBot uniformly.

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
raw_draft_bot
```

### Field Contracts

| Field | Type | Required behavior |
| --- | --- | --- |
| `type` | `str` | `"bot_draft_status"` or `"bot_draft_pick"`. |
| `source_method` | `str` | Exact observed marker: `"BotDraftDraftStatus"` or `"BotDraftDraftPick"`. |
| `api_direction` | `str` | `"request"`, `"response"`, or narrowly justified `"unknown"`. |
| `draft_id` | `str` | Stripped draft id when present as a string; otherwise `""`. |
| `event_id` | `str` | Stripped event id/name when present as a string; otherwise `""`. |
| `draft_status` | `str` | Stripped draft status/state when present as a string; otherwise `""`. |
| `pack_number` | `int | None` | Non-bool integer or integer-like string when present; otherwise `None`. |
| `pick_number` | `int | None` | Non-bool integer or integer-like string when present; otherwise `None`. |
| `pack_card_ids` | `list[int]` | Normalized nonnegative Arena card/grp IDs from the offered pack list; otherwise `[]`. |
| `picked_card_id` | `int | None` | Normalized nonnegative picked card/grp ID when present; otherwise `None`. |
| `picked_card_ids` | `list[int]` | Normalized nonnegative picked card/grp IDs when a list is present; may contain `picked_card_id`; otherwise `[]`. |
| `raw_draft_bot` | `dict[str, Any]` | Full parsed top-level JSON object from the log entry. |

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

Raw evidence:

- Preserve the full parsed top-level JSON object in `raw_draft_bot`.
- Do not store full raw private log lines outside event metadata.
- Do not resolve card names, ratings, colors, archetypes, or deck construction
  facts in this parser.

## Malformed And Partial Payload Behavior

Required behavior:

- No recognized marker: return `None`.
- Recognized marker but no parseable JSON dictionary: return `None`.
- Recognized marker with parseable dictionary but missing optional normalized
  fields: emit `DraftBotEvent` with default `""`, `None`, or `[]` values.
- Marker-wrapped payload where the nested marker value is not a dictionary:
  normalize from the top-level dictionary and preserve the full top-level raw
  payload.
- Invalid scalar fields must not raise and must not poison normalized output.
- Invalid list members must be skipped, not surfaced as card IDs.
- Malformed input must not write files, mutate parser state, post webhooks, or
  update workbook-facing rows.

False positives:

- Case variants such as `botdraftdraftpick` must not match.
- Human draft markers must not match `DraftBot`.
- Draft completion markers must not match `DraftBot`.
- Generic prose containing `draft`, `pack`, `pick`, or `bot` must not match.

## Router And Package Expectations

Package import:

- Add `draft_bot` to `src/mythic_edge_parser/parsers/__init__.py`.
- Add `"draft_bot"` to `__all__`.

Router dispatch:

- Add `parsers.draft_bot` to `EntryHeader.UNITY_CROSS_THREAD_LOGGER`.
- Add `parsers.draft_bot` to `EntryHeader.UNKNOWN`.
- Do not add it to `EntryHeader.METADATA`, `EntryHeader.CLIENT_GRE`,
  `EntryHeader.TRUNCATION_MARKER`, `EntryHeader.CONNECTION_MANAGER`, or
  `EntryHeader.MATCHMAKING`.

Recommended ordering:

- Place `draft_bot` after `parsers.event_lifecycle` and before `parsers.rank`
  in both the Unity and UNKNOWN dispatch tuples.

Rationale:

- Bot draft markers are durable API-style events.
- The parser must be reachable from current API log entries.
- The parser is marker-specific and should not shadow GRE, client action,
  match-state, session, lifecycle, rank, collection, or inventory parsing.

If Codex C finds that real or sanitized evidence requires different routing,
it must document the reason in the implementation handoff and route back to
Codex B if the route would broaden parser behavior beyond this contract.

## Schema Snapshot Expectations

Required snapshot changes when Codex C implements the parser:

- `tests/test_event_schema_snapshots.py` must include representative
  `DraftBot` sample events for:
  - `bot_draft_status`
  - `bot_draft_pick`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json` must include:
  - `DraftBot.bot_draft_status`
  - `DraftBot.bot_draft_pick`
- Snapshot entries must include only stable payload keys, not raw nested payload
  values.

Expected payload key order for both DraftBot sample entries:

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

`parser_event_classes.json` already includes `DraftBotEvent` on the current
branch. If that snapshot changes during implementation, Codex C must explain
why. Adding the parser should not require changing the event class snapshot.

Snapshot updates require the same explicit issue/contract/review approval rules
as existing schema snapshots. Do not auto-update snapshots as a way to hide an
unreviewed payload shape change.

## Corpus And Golden Evidence Expectations

The current feature-equity corpus baseline records zero `DraftBot` events. That
zero count is accurate until a committed sanitized or synthetic golden replay
fixture exercises DraftBot through the normal `LineBuffer` and `Router` path.

Minimum implementation evidence:

- focused parser tests for `draft_bot.try_parse()`
- router/package reachability tests
- schema snapshot sample coverage for both payload types

Full reliability evidence:

- one small committed sanitized or synthetic golden replay fixture and manifest
  that emits at least one `bot_draft_status` and one `bot_draft_pick` event
  through the normal replay path
- feature-equity corpus ratchet baseline updates that change `DraftBot` counts
  from zero only when the committed fixture is added

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

- `DraftBotEvent.kind` stays `"DraftBot"`.
- `DraftBotEvent.performance_class` stays `DurablePerEvent`.
- `DraftHumanEvent` and `DraftCompleteEvent` remain separate event families.
- Existing parser payloads, workbook row keys, webhook payloads, Apps Script
  field maps, runtime status files, failed-post files, and generated data remain
  unchanged.
- Existing `api_common` behavior remains unchanged unless a future contract
  explicitly authorizes shared helper changes.
- `MatchSummary`, `GameSummary`, parser state, and final reconciliation ignore
  `DraftBot` unless a later contract explicitly defines draft-to-match state
  behavior.

## Side Effects

Allowed future side effects in Codex C:

- read `LogEntry.body`
- build in-memory `DraftBotEvent` objects
- add source parser code
- add focused tests
- update parser payload schema snapshots for DraftBot payload keys
- optionally add reviewed sanitized or synthetic golden replay fixture files and
  count-only corpus baseline updates if all fixture safety rules are met
- write the implementation handoff

Forbidden side effects:

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
- no production behavior changes
- no draft pick coaching, ratings, AI draft advice, or deck construction
  analytics

## Dependency Order

Codex C should proceed in this order:

1. Confirm branch is `codex/parser-reliability-intelligence` and inspect
   `git status --short --branch`.
2. Read this contract and issue #122.
3. Compare current event/router/parser/test surfaces against this contract.
4. Add focused tests for `draft_bot.try_parse()` behavior.
5. Add `src/mythic_edge_parser/parsers/draft_bot.py`.
6. Add parser package import and router dispatch.
7. Add router/package reachability tests.
8. Add schema snapshot sample events and update payload-key snapshot only after
   tests define the expected DraftBot payload shape.
9. Decide whether a safe synthetic/sanitized golden replay fixture is in scope.
   If yes, add it and update count-only corpus baseline with review notes. If
   no, record corpus coverage as remaining unverified.
10. Run validation.
11. Produce `docs/implementation_handoffs/parser_draft_bot_comparison.md`.
12. Route to Codex E for contract-test review.

Stop and route back to Codex B if:

- exact source field names from safe evidence do not fit this contract
- implementation needs a shared `api_common` behavior change
- implementation requires a new event class or changed `kind`
- implementation requires workbook, webhook, Apps Script, state, final
  reconciliation, match/game identity, or deduplication changes
- safe fixture coverage would require committing raw private logs

## Tests Required

Focused parser tests, expected in `tests/test_draft_bot_parser.py`, must cover:

- status response marker emits `DraftBotEvent` with `type="bot_draft_status"`
- pick request or response marker emits `DraftBotEvent` with
  `type="bot_draft_pick"`
- event kind and performance class are correct
- metadata timestamp and raw bytes are preserved
- `source_method` and `api_direction` are populated
- direct payload shape normalizes common fields
- marker-wrapped payload shape normalizes nested fields while preserving the
  full top-level raw payload
- missing optional fields emit default values
- integer-like strings are accepted for indexes and card IDs
- booleans, floats, negative values, signed strings, blank strings, containers,
  and arbitrary objects are rejected for numeric fields
- non-list card containers produce empty lists
- invalid list members are skipped without raising
- malformed JSON returns `None`
- unrelated entries return `None`
- marker matching is case-sensitive
- human draft and draft completion markers do not emit `DraftBot`
- false-positive prose does not emit `DraftBot`

Router/package tests must cover:

- `parsers.draft_bot` is imported through `src/mythic_edge_parser/parsers/__init__.py`
- Unity cross-thread entries route to `DraftBot`
- UNKNOWN header entries route to `DraftBot`
- routed DraftBot entries increment router routed stats, not unknown stats
- non-draft entries still route through existing parsers as before

Schema snapshot tests must cover:

- `DraftBot.bot_draft_status` payload keys
- `DraftBot.bot_draft_pick` payload keys
- no raw nested payload values are stored in schema snapshots

Golden/corpus tests, if Codex C adds a fixture, must cover:

- golden replay emits `DraftBot` through the normal parser path
- the count-only corpus ratchet observes nonzero `DraftBot` counts
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
docs/contracts/parser_draft_bot.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Because this contract is a new untracked file during the B pass, Codex B should
also run a new-file whitespace check such as:

```powershell
Select-String -Path docs\contracts\parser_draft_bot.md -Pattern '[ \t]+$'
```

### Codex C Implementation Validation

Focused first:

```powershell
py -m pytest -q tests\test_draft_bot_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
```

Related parser reliability checks:

```powershell
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
py -m pytest -q tests\test_router_unit.py tests\test_parsers.py
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
py tools\check_protected_surfaces.py --base origin/main
```

If a repo-approved secret/private-content scanner exists on the active branch,
run it against any new fixture, manifest, snapshot, baseline, and report
fixture paths before submitter work.

## Acceptance Criteria

This contract is complete when:

- `docs/contracts/parser_draft_bot.md` exists.
- The contract links issue #122, tracker #47, related tracker #11, the agent
  constitution, the Module Contract Writer rules, and the module contract
  template.
- The parser truth-owning layer is named.
- Observed current behavior is distinguished from required guarantees.
- Recognized bot draft markers are exact and case-sensitive.
- `DraftBot` event kind and payload `type` values are defined.
- Parser-owned normalized fields are defined with type and default behavior.
- Raw evidence preservation is defined.
- Malformed and partial payload behavior is defined.
- Router and parser package expectations are defined.
- Schema snapshot expectations are defined.
- Focused tests and optional golden/corpus evidence expectations are defined.
- Protected surfaces and out-of-scope behavior are explicit.
- The next role is Codex C for implementation/comparison.
- No code, test, snapshot, fixture, baseline, parser behavior, workbook,
  webhook, Apps Script, secret, generated-data, runtime, or production changes
  are implemented by this contract thread.

## Unknowns

- Exact live MTGA bot draft payload field names are not present in committed
  repo fixtures.
- It is unknown whether the log emits status and pick evidence as requests,
  responses, or both for all client versions.
- It is unknown whether pack/pick indexes are zero-based or one-based. V1 must
  preserve observed values without conversion.
- It is unknown whether `draft_id` and `event_id` are always present in bot
  draft payloads.
- It is unknown whether card IDs appear as `grpId`, `cardId`, or another field
  in all client versions.
- It is unknown whether a safe synthetic golden replay fixture can be added
  without expanding the implementation pass.

## Suspected Implementation Gaps

- No DraftBot parser module exists.
- Router dispatch cannot currently emit `DraftBot`.
- Payload schema snapshots do not include DraftBot payload keys.
- Focused tests do not protect bot draft marker recognition, false positives,
  malformed input, or normalization rules.
- The feature-equity corpus ratchet currently records DraftBot zero counts.
- There is no committed golden replay fixture for draft evidence.

These are contract findings, not authorization for Codex B to change behavior.

## Next Workflow Action

Recommended next role: Codex C / Module Implementer.

Codex C should compare current code to this contract, implement the smallest
coherent parser/test/snapshot changes required, and produce
`docs/implementation_handoffs/parser_draft_bot_comparison.md`.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #122:
https://github.com/Tahjali11/Mythic-Edge/issues/122

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/parser_draft_bot.md

Goal:
Compare the current parser/event/router/tests/snapshots/corpus surfaces against docs/contracts/parser_draft_bot.md, then implement the smallest coherent first-class Quick Draft / bot draft parser support required by the contract. Produce docs/implementation_handoffs/parser_draft_bot_comparison.md.

Before editing:
- Confirm the branch is codex/parser-reliability-intelligence and inspect git status.
- State what DraftBot parsing is supposed to do, what the repo currently does, what gap remains, why it exists, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/parser_draft_bot.md
- docs/problem_representations/parser_feature_equity_with_manasight.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/player_log_evidence_ledger.md
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/parsers/api_common.py
- durable parser patterns in event_lifecycle.py, rank.py, session.py, collection.py, and inventory.py
- tests/test_event_schema_snapshots.py
- tests/test_feature_equity_corpus_ratchet.py
- tests/test_golden_replay_harness.py

Implement only if the contract is implementable as written:
- src/mythic_edge_parser/parsers/draft_bot.py
- parser package import and router dispatch for Unity and UNKNOWN headers
- focused tests, expected in tests/test_draft_bot_parser.py
- DraftBot parser payload schema snapshot samples
- optional safe synthetic/sanitized golden replay and corpus baseline update only if it can be done without private raw logs or scope expansion

Do not:
- Copy Manasight code.
- Paste or commit raw private Player.log excerpts.
- Add DraftHuman or DraftComplete behavior.
- Add draft coaching, card ratings, AI draft advice, or deck construction analytics.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates.
- Target main.
- Mark #47 or #11 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
py -m pytest -q tests\test_draft_bot_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
py -m pytest -q tests\test_router_unit.py tests\test_parsers.py
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/main

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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/122"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer"
  source_artifact: "GitHub issue #122 and docs/problem_representations/parser_feature_equity_with_manasight.md"
  contract_artifact: "docs/contracts/parser_draft_bot.md"
  target_artifact: "docs/implementation_handoffs/parser_draft_bot_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "new-file trailing-whitespace scan for docs/contracts/parser_draft_bot.md"
    - "path-scoped protected-surface check for docs/contracts/parser_draft_bot.md"
  stop_conditions:
    - "Do not copy Manasight code."
    - "Do not paste or commit raw private Player.log excerpts."
    - "Do not add DraftHuman or DraftComplete behavior."
    - "Do not add draft coaching, card ratings, AI draft advice, or deck construction analytics."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates."
    - "Do not target main."
    - "Do not mark tracker #47 or related tracker #11 complete."
```
