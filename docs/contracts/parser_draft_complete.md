# Parser DraftComplete Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/124
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- related_tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- branch_target: codex/parser-reliability-intelligence
- source_problem_representation: GitHub issue #124
- source_feature_equity_artifact: docs/problem_representations/parser_feature_equity_with_manasight.md
- prior_draftbot_contract: docs/contracts/parser_draft_bot.md
- prior_drafthuman_contract: docs/contracts/parser_draft_human.md
- prior_integration_commit: 11ce81dde63c4a837acaaf3d42baf891590cf3dc
- target_artifact: docs/contracts/parser_draft_complete.md
- expected_next_artifact: docs/implementation_handoffs/parser_draft_complete_comparison.md
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

Mythic Edge should treat draft completion log evidence as a first-class
parser-owned event surface.

Plain English: when MTGA emits draft completion evidence, the parser should
recognize the exact completion marker, emit the existing `DraftCompleteEvent`,
preserve the raw parsed payload, and expose a small stable payload for draft
identity, event or queue context, completion status, completion source, and
bot/human draft metadata where the log provides those values.

Feature equity with the local Manasight reference means evidence coverage and
testable parser behavior. It does not mean copying Manasight source code,
matching Manasight internals, or expanding into draft coaching.

This contract does not implement code. It does not authorize workbook,
webhook, Apps Script, match/game final reconciliation, DraftBot behavior,
DraftHuman behavior, draft pick coaching, card rating, deck construction, or
AI/model-provider changes.

## Owning Layer

Owning truth layer: parser event recognition and parser payload normalization.

The parser owns:

- draft completion marker recognition
- `DraftCompleteEvent` emission
- stable DraftComplete payload `type` values
- parser-owned normalized completion evidence fields
- raw parsed draft completion payload preservation
- malformed and partial payload behavior
- false-positive separation from DraftBot and DraftHuman markers

The parser does not own in this module:

- bot draft parsing changes
- human draft parsing changes
- draft pick coaching
- card ratings
- draft advice
- deck construction analytics
- hidden-information inference
- archetype classification
- match identity or game identity
- match/game final reconciliation
- workbook row schema
- webhook payload shape
- Apps Script behavior
- AI or model-provider interpretation

Downstream systems may consume `DraftComplete` events as parser-owned draft
completion evidence. They must not turn draft helper sheets, dashboards, Apps
Script, webhooks, analytics surfaces, or AI output into the source of draft
truth.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/parser_draft_complete.md

Future implementation files owned or authorized by this contract:

- src/mythic_edge_parser/parsers/draft_complete.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/router.py
- tests/test_draft_complete_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json
- optional committed sanitized or synthetic golden replay fixture and manifest
  files under existing fixture locations, only if Codex C adds corpus coverage
  under the safety rules below
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json,
  only if a committed golden replay fixture is added and the count-only
  baseline must be updated
- docs/implementation_handoffs/parser_draft_complete_comparison.md
- docs/contract_test_reports/parser_draft_complete.md

Referenced but not silently owned:

- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/parsers/draft_bot.py
- src/mythic_edge_parser/parsers/draft_human.py
- src/mythic_edge_parser/log/entry.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- docs/contracts/parser_draft_bot.md
- docs/contracts/parser_draft_human.md
- docs/contracts/parser_draft_surface_parity_recommendation.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/player_log_evidence_ledger.md

`events.py` already defines `DraftCompleteEvent`. This contract does not
authorize a new event class or a changed event `kind` value. If Codex C
discovers that `DraftCompleteEvent` is missing or inconsistent on the active
branch, it must route back to Codex B instead of inventing a replacement event
model.

## Observed Current Behavior

Observed from `origin/codex/parser-reliability-intelligence` at
`11ce81dde63c4a837acaaf3d42baf891590cf3dc`:

- `src/mythic_edge_parser/events.py` defines `DraftCompleteEvent`.
- `DraftCompleteEvent.kind == "DraftComplete"`.
- `DraftCompleteEvent.performance_class == PerformanceClass.DURABLE_PER_EVENT`.
- `DraftCompleteEvent` is included in the public `GameEvent` union.
- `tests/fixtures/schema_snapshots/parser_event_classes.json` includes the
  `DraftCompleteEvent` class and kind.
- `src/mythic_edge_parser/parsers/draft_bot.py` exists and handles only
  `BotDraftDraftStatus` and `BotDraftDraftPick`.
- `src/mythic_edge_parser/parsers/draft_human.py` exists and handles only
  `Draft.Notify`, `EventPlayerDraftMakePick`, and qualifying
  `LogBusinessEvents` payloads with picked-card evidence.
- DraftBot and DraftHuman focused tests reject `DraftCompleteDraft` as their
  own event family.
- `src/mythic_edge_parser/parsers/__init__.py` does not import
  `draft_complete`.
- `src/mythic_edge_parser/router.py` does not dispatch to a DraftComplete
  parser.
- `src/mythic_edge_parser/parsers/` has no `draft_complete.py` module.
- `tests/test_event_schema_snapshots.py` has no `DraftComplete` payload sample.
- `tests/fixtures/schema_snapshots/parser_payload_keys.json` has no
  `DraftComplete.*` payload entries.
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
  records zero `DraftComplete` counts.
- No focused draft completion parser tests were found.

The current behavior is not a runtime bug by itself. It is a feature-equity
gap: the event class exists, but no parser path can emit it.

## Public Interface

### Parser Module

Add a dedicated parser module:

```python
src/mythic_edge_parser/parsers/draft_complete.py
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

- Return one `DraftCompleteEvent` for one recognized draft completion marker
  entry.
- Return `None` for unrelated entries.
- Never raise for malformed marker-like input in normal parser use.
- Preserve provenance with `EventMetadata(timestamp, entry.body.encode())`.
- Keep helper functions private unless a later contract makes them public.
- Do not import workbook, webhook, Apps Script, model-provider, AI, parser
  state, or downstream surfaces.

### Public Constants

The implementation should define a narrow marker constant in
`draft_complete.py`. Exact constant names may vary, but it must represent this
marker value:

```python
DRAFT_COMPLETE_DRAFT_MARKER = "DraftCompleteDraft"
```

Marker matching must be exact and case-sensitive.

### Event Kind

Required event class:

- `DraftCompleteEvent`

Required event `kind`:

- `"DraftComplete"`

Required performance class:

- `PerformanceClass.DURABLE_PER_EVENT`

The implementation must not add a new draft event class for completion
support. `DraftBotEvent` and `DraftHumanEvent` behavior must remain unchanged.

## Recognized Markers

V1 recognized draft completion markers:

| Marker | Payload `type` | Meaning |
| --- | --- | --- |
| `DraftCompleteDraft` | `draft_complete_draft` | Draft completion signal or completion metadata evidence. |

Accepted API directions:

- request marker: `==> DraftCompleteDraft`
- response marker: `<== DraftCompleteDraft`

The payload must include the observed direction:

- `"request"` when the exact marker follows `==>`
- `"response"` when the exact marker follows `<==`
- `"unknown"` only if Codex C proves with focused tests that an exact marker
  can appear without the standard API request/response prefix

If multiple recognized completion markers appear in one entry, the parser must
use a deterministic first-marker policy and emit at most one event. Since v1
has one recognized marker, this rule mainly prevents future marker broadening
without a contract update.

Unknown future draft completion markers are out of scope. The parser must not
classify `BotDraftDraftStatus`, `BotDraftDraftPick`, `Draft.Notify`,
`EventPlayerDraftMakePick`, `LogBusinessEvents`, or `PickGrpId` as
`DraftComplete`.

## Input Shapes

Primary input:

- `LogEntry` from `src/mythic_edge_parser/log/entry.py`
- expected headers: `EntryHeader.UNITY_CROSS_THREAD_LOGGER` and
  `EntryHeader.UNKNOWN`
- body text containing an exact `DraftCompleteDraft` API marker and a JSON
  object parseable by `api_common.parse_json_from_body()`

Accepted JSON payload shapes:

1. Direct object:

```json
{
  "draftId": "draft-1",
  "eventName": "PremierDraft_Example",
  "queueId": "PremierDraft",
  "completionStatus": "Complete",
  "draftType": "HumanDraft",
  "draftMode": "Premier"
}
```

2. Marker-wrapped object:

```json
{
  "DraftCompleteDraft": {
    "DraftId": "draft-1",
    "EventName": "PremierDraft_Example",
    "CompletionStatus": "Complete",
    "IsHumanDraft": true
  }
}
```

For marker-wrapped objects, normalized fields come from the nested marker
object when it is a mapping. `raw_draft_complete` still preserves the full
parsed top-level object.

If a marker is present but the first decodable JSON value is not a dictionary,
the parser returns `None`.

## Output Payload

DraftComplete payloads must use one stable key set so downstream and snapshot
tests can reason about DraftComplete uniformly.

Required payload keys, in this order:

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

### Field Contracts

| Field | Type | Required behavior |
| --- | --- | --- |
| `type` | `str` | `"draft_complete_draft"`. |
| `source_method` | `str` | Exact observed marker: `"DraftCompleteDraft"`. |
| `api_direction` | `str` | `"request"`, `"response"`, or narrowly justified `"unknown"`. |
| `draft_id` | `str` | Stripped draft id when present as a string; otherwise `""`. |
| `event_id` | `str` | Stripped event id/name when present as a string; otherwise `""`. |
| `queue_id` | `str` | Stripped queue/event queue context when present as a string; otherwise `""`. |
| `draft_status` | `str` | Stripped draft status/state when present as a string; otherwise `""`. |
| `completion_status` | `str` | Stripped completion status/result/reason when present as a string; otherwise `""`. |
| `draft_type` | `str` | Stripped draft type/category when present as a string; otherwise `""`. |
| `draft_mode` | `str` | Stripped draft mode such as Premier, Traditional, Quick, Bot, or Human when present as a string; otherwise `""`. |
| `completion_source` | `str` | Stripped payload source/completion source when present as a string; otherwise defaults to `"DraftCompleteDraft"`. |
| `is_bot_draft` | `bool | None` | Boolean bot-draft metadata when directly present; otherwise `None`. |
| `is_human_draft` | `bool | None` | Boolean human-draft metadata when directly present; otherwise `None`. |
| `raw_draft_complete` | `dict[str, Any]` | Full parsed top-level JSON object from the log entry. |

### Source Field Aliases

V1 normalized fields may use these source aliases.

| Normalized field | Accepted source aliases |
| --- | --- |
| `draft_id` | `draftId`, `DraftId`, `draftID` |
| `event_id` | `eventId`, `EventId`, `eventID`, `eventName`, `EventName` |
| `queue_id` | `queueId`, `QueueId`, `queueID`, `queueName`, `QueueName`, `eventQueueId`, `EventQueueId` |
| `draft_status` | `draftStatus`, `DraftStatus`, `status`, `state` |
| `completion_status` | `completionStatus`, `CompletionStatus`, `completeStatus`, `CompleteStatus`, `result`, `Result`, `reason`, `Reason` |
| `draft_type` | `draftType`, `DraftType`, `draftCategory`, `DraftCategory`, `type`, `Type` |
| `draft_mode` | `draftMode`, `DraftMode`, `mode`, `Mode`, `draftKind`, `DraftKind` |
| `completion_source` | `completionSource`, `CompletionSource`, `source`, `Source` |
| `is_bot_draft` | `isBotDraft`, `IsBotDraft`, `botDraft`, `BotDraft` |
| `is_human_draft` | `isHumanDraft`, `IsHumanDraft`, `humanDraft`, `HumanDraft` |

If later sanitized evidence shows different field names, Codex C must route
back to Codex B or document a contract loopback before broadening aliases.

### Normalization Rules

String fields:

- Accept only strings.
- Strip leading and trailing whitespace.
- Use `""` for missing or non-string values, except `completion_source`.
- `completion_source` defaults to `"DraftCompleteDraft"` when no accepted
  source string is present.

Boolean fields:

- Accept only real JSON/Python booleans.
- Reject strings, integers, floats, containers, and objects.
- Use `None` for missing or invalid values.
- Do not infer `is_bot_draft` or `is_human_draft` from `event_id`, `queue_id`,
  `draft_type`, `draft_mode`, or any prose-like string.

Raw evidence:

- Preserve the full parsed top-level JSON object in `raw_draft_complete`.
- Do not store full raw private log lines outside event metadata.
- Do not resolve card names, ratings, colors, archetypes, deck construction
  facts, or draft pick quality in this parser.
- If the completion payload includes decklists, picked-card arrays, or pack
  histories, preserve them only in `raw_draft_complete` in v1. Do not normalize
  them without a later contract.

## Malformed And Partial Payload Behavior

Required behavior:

- No recognized marker: return `None`.
- Recognized marker but no parseable JSON dictionary: return `None`.
- Recognized marker with parseable dictionary but missing optional normalized
  fields: emit `DraftCompleteEvent` with default `""`, `None`, or
  `"DraftCompleteDraft"` values as defined above.
- Marker-wrapped payload where the nested marker value is not a dictionary:
  normalize from the top-level dictionary and preserve the full top-level raw
  payload.
- Invalid scalar fields must not raise and must not poison normalized output.
- Malformed input must not write files, mutate parser state, post webhooks, or
  update workbook-facing rows.

False positives:

- Case variants such as `draftcompletedraft` or `DraftCompleteDraftExtra` must
  not match.
- Bot draft markers must not match `DraftComplete`.
- Human draft markers must not match `DraftComplete`.
- `LogBusinessEvents` with `PickGrpId` must not match `DraftComplete`.
- Generic prose containing `draft`, `complete`, `completed`, or
  `DraftCompleteDraft` outside the exact API marker contract must not match.

## Router And Package Expectations

Package import:

- Add `draft_complete` to `src/mythic_edge_parser/parsers/__init__.py`.
- Add `"draft_complete"` to `__all__`.

Router dispatch:

- Add `parsers.draft_complete` to `EntryHeader.UNITY_CROSS_THREAD_LOGGER`.
- Add `parsers.draft_complete` to `EntryHeader.UNKNOWN`.
- Do not add it to `EntryHeader.METADATA`, `EntryHeader.CLIENT_GRE`,
  `EntryHeader.TRUNCATION_MARKER`, `EntryHeader.CONNECTION_MANAGER`, or
  `EntryHeader.MATCHMAKING`.

Recommended ordering:

- Place `draft_complete` after `parsers.draft_human` and before
  `parsers.rank` in both the Unity and UNKNOWN dispatch tuples.

Rationale:

- Draft completion markers are durable API-style events.
- The parser must be reachable from current API log entries.
- The parser is marker-specific and should not shadow GRE, client action,
  match-state, session, lifecycle, DraftBot, DraftHuman, rank, collection, or
  inventory parsing.
- DraftBot and DraftHuman are already more specific to pack/pick evidence.
  DraftComplete should remain a separate completion surface.

If Codex C finds that real or sanitized evidence requires different routing, it
must document the reason in the implementation handoff and route back to Codex
B if the route would broaden parser behavior beyond this contract.

## Schema Snapshot Expectations

Required snapshot changes when Codex C implements the parser:

- `tests/test_event_schema_snapshots.py` must import `draft_complete`.
- `tests/test_event_schema_snapshots.py` must include a representative
  `DraftComplete` sample event for:
  - `draft_complete_draft`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json` must include:
  - `DraftComplete.draft_complete_draft`
- Snapshot entries must include only stable payload keys, not raw nested
  payload values.

Expected payload key order for the DraftComplete sample entry:

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

`parser_event_classes.json` already includes `DraftCompleteEvent` on the
current branch. If that snapshot changes during implementation, Codex C must
explain why. Adding the parser should not require changing the event class
snapshot.

Snapshot updates require the same explicit issue/contract/review approval rules
as existing schema snapshots. Do not auto-update snapshots as a way to hide an
unreviewed payload shape change.

## Corpus And Golden Evidence Expectations

The current feature-equity corpus baseline records zero `DraftComplete`
events. That zero count is accurate until a committed sanitized or synthetic
golden replay fixture exercises DraftComplete through the normal `LineBuffer`
and `Router` path.

Minimum implementation evidence:

- focused parser tests for `draft_complete.try_parse()`
- router/package reachability tests
- schema snapshot sample coverage for `draft_complete_draft`

Full reliability evidence:

- one small committed sanitized or synthetic golden replay fixture and manifest
  that emits at least one `draft_complete_draft` event through the normal
  replay path
- feature-equity corpus ratchet baseline updates that change `DraftComplete`
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

- `DraftCompleteEvent.kind` stays `"DraftComplete"`.
- `DraftCompleteEvent.performance_class` stays `DurablePerEvent`.
- `DraftBotEvent` behavior from issue #122 stays unchanged.
- `DraftHumanEvent` behavior from issue #123 stays unchanged.
- Existing parser payloads, workbook row keys, webhook payloads, Apps Script
  field maps, runtime status files, failed-post files, and generated data
  remain unchanged.
- Existing `api_common` behavior remains unchanged unless a future contract
  explicitly authorizes shared helper changes.
- `MatchSummary`, `GameSummary`, parser state, and final reconciliation ignore
  `DraftComplete` unless a later contract explicitly defines draft-to-match
  state behavior.

## Side Effects

Allowed future side effects in Codex C:

- read `LogEntry.body`
- build in-memory `DraftCompleteEvent` objects
- add source parser code
- add focused tests
- update parser payload schema snapshots for DraftComplete payload keys
- optionally add reviewed sanitized or synthetic golden replay fixture files and
  count-only corpus baseline updates if all fixture safety rules are met
- write the implementation handoff

Forbidden side effects:

- no DraftBot behavior change
- no DraftHuman behavior change
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
- no draft pick coaching, ratings, AI draft advice, hidden-card inference,
  archetype classification, gameplay advice, or deck construction analytics

## Dependency Order

Codex C should proceed in this order:

1. Confirm branch is `codex/parser-reliability-intelligence` and inspect
   `git status --short --branch`.
2. Read this contract and issue #124.
3. Compare current event/router/parser/test surfaces against this contract.
4. Add focused tests for `draft_complete.try_parse()` behavior.
5. Add `src/mythic_edge_parser/parsers/draft_complete.py`.
6. Add parser package import and router dispatch.
7. Add or update router/package reachability tests.
8. Add schema snapshot sample events and update payload-key snapshot only after
   tests define the expected DraftComplete payload shape.
9. Decide whether a safe synthetic/sanitized golden replay fixture is in scope.
   If yes, add it and update count-only corpus baseline with review notes. If
   no, record corpus coverage as remaining unverified.
10. Run validation.
11. Produce `docs/implementation_handoffs/parser_draft_complete_comparison.md`.
12. Route to Codex E for contract-test review.

Stop and route back to Codex B if:

- exact source field names from safe evidence do not fit this contract
- implementation needs a shared `api_common` behavior change
- implementation requires multi-event emission from one entry
- implementation requires a new event class or changed `kind`
- implementation requires DraftBot or DraftHuman behavior changes
- implementation requires workbook, webhook, Apps Script, state, final
  reconciliation, match/game identity, or deduplication changes
- safe fixture coverage would require committing raw private logs

## Tests Required

Focused parser tests, expected in `tests/test_draft_complete_parser.py`, must
cover:

- `DraftCompleteDraft` request or response marker emits `DraftCompleteEvent`
  with `type="draft_complete_draft"`
- event kind and performance class are correct
- metadata timestamp and raw bytes are preserved
- `source_method` and `api_direction` are populated
- direct payload shape normalizes common fields
- marker-wrapped payload shape normalizes nested fields while preserving the
  full top-level raw payload
- missing optional fields emit default values
- string fields strip whitespace and reject non-string values
- boolean fields accept only real booleans and reject strings, integers,
  floats, containers, and objects
- nested non-mapping marker payloads fall back to top-level normalization
- malformed JSON returns `None`
- unrelated entries return `None`
- marker matching is exact and case-sensitive
- marker suffix/prefix false positives do not emit `DraftComplete`
- DraftBot and DraftHuman markers do not emit `DraftComplete`
- `LogBusinessEvents` and `PickGrpId` do not emit `DraftComplete`
- generic prose does not emit `DraftComplete`

Router/package tests must cover:

- `parsers.draft_complete` is imported through
  `src/mythic_edge_parser/parsers/__init__.py`
- Unity cross-thread entries route to `DraftComplete`
- UNKNOWN header entries route to `DraftComplete`
- routed DraftComplete entries increment router routed stats, not unknown stats
- DraftBot and DraftHuman entries still route to their existing event families
- non-draft entries still route through existing parsers as before

Schema snapshot tests must cover:

- `DraftComplete.draft_complete_draft` payload keys
- no raw nested payload values are stored in schema snapshots
- `parser_event_classes.json` remains stable unless Codex C documents an
  unexpected branch mismatch

Golden/corpus tests, if Codex C adds a fixture, must cover:

- golden replay emits `DraftComplete` through the normal parser path
- the count-only corpus ratchet observes nonzero `DraftComplete` counts
- the fixture is synthetic or sanitized and contains no raw private draft log
  content

Recommended validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_draft_complete_parser.py
python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py
python3 -m pytest -q tests/test_router_unit.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests
python3 -m ruff check src tests tools
git diff --check
```

If Codex C adds fixture or corpus baseline files, it must also run the most
relevant privacy/protected-surface check available on the branch and report the
exact command and result.

## Acceptance Criteria

- `docs/contracts/parser_draft_complete.md` exists.
- The contract defines the owning layer, public parser interface, recognized
  `DraftCompleteDraft` marker, event kind, payload shape, normalized fields,
  raw evidence preservation, malformed/partial payload behavior,
  router/package expectations, schema snapshot expectations, focused tests,
  corpus/golden evidence expectations, protected boundaries, and Codex C
  handoff.
- No behavior changes are made in the contract-writing pass.
- Next workflow route is Codex C: Module Implementer on
  `codex/parser-reliability-intelligence`.

## Open Questions And Contract Risks

- Safe evidence may reveal additional completion payload field names. Codex C
  may add a narrow alias only if focused tests and implementation handoff make
  the evidence explicit; broader alias expansion should route back to Codex B.
- It is unknown whether Arena emits `DraftCompleteDraft` primarily as a request
  or response. The parser must support both standard API directions.
- It is unknown whether completion payloads contain bot/human metadata as
  booleans, strings, or queue/event IDs. V1 accepts direct booleans and
  preserves everything else raw rather than guessing.
- Draft golden replay and corpus coverage may remain unverified unless Codex C
  can safely create synthetic or sanitized fixture evidence.

## Recommended Next Role

Codex C: Module Implementer.

Codex C should compare this contract against the current parser reliability
branch, implement only the smallest coherent parser-local code and test changes
needed to satisfy the contract, produce
`docs/implementation_handoffs/parser_draft_complete_comparison.md`, and route
to Codex E for review.

## Pasteable Prompt For Codex C

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #124: DraftComplete parser module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Related evidence-ledger issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/124
- Branch/base: codex/parser-reliability-intelligence
- Contract: docs/contracts/parser_draft_complete.md
- Previous completed module: DraftHuman parser, issue #123
- Previous integration commit: 11ce81dde63c4a837acaaf3d42baf891590cf3dc

Goal:
Compare the current draft parser/event/router/test surfaces against the
DraftComplete contract. Implement only the smallest coherent parser-local code
and tests needed to satisfy the contract.

Read first:
1. AGENTS.md
2. docs/agent_constitution.md
3. docs/agent_rules.yml
4. docs/agent_threads/implementation.md
5. docs/codex_module_workflow.md
6. docs/contracts/parser_draft_complete.md
7. docs/contracts/parser_draft_bot.md
8. docs/contracts/parser_draft_human.md
9. docs/contracts/parser_draft_surface_parity_recommendation.md
10. docs/problem_representations/parser_feature_equity_with_manasight.md
11. src/mythic_edge_parser/events.py
12. src/mythic_edge_parser/router.py
13. src/mythic_edge_parser/parsers/__init__.py
14. src/mythic_edge_parser/parsers/draft_bot.py
15. src/mythic_edge_parser/parsers/draft_human.py
16. tests/test_draft_bot_parser.py
17. tests/test_draft_human_parser.py
18. tests/test_event_schema_snapshots.py
19. tests/fixtures/schema_snapshots/parser_payload_keys.json
20. tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json

Implement:
- Add src/mythic_edge_parser/parsers/draft_complete.py.
- Add tests/test_draft_complete_parser.py.
- Add parser package import and router dispatch for UNITY_CROSS_THREAD_LOGGER and UNKNOWN headers.
- Add schema snapshot sample coverage for DraftComplete.draft_complete_draft.
- Preserve DraftBot and DraftHuman behavior.
- Preserve parser event classes and DraftCompleteEvent.kind.
- Produce docs/implementation_handoffs/parser_draft_complete_comparison.md with observed comparison, changes made, validation run, open risks, files changed, and next recommended role.

Do not:
- Do not target main directly.
- Do not close tracker #47.
- Do not close related issue #11.
- Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or environment variable contracts.
- Do not change DraftBot or DraftHuman behavior except for preserving route order around the new DraftComplete parser.
- Do not create a new event class or change DraftCompleteEvent.kind.
- Do not build draft pick coaching, card ratings, AI draft advice, deck construction analytics, hidden-card inference, archetype classification, gameplay advice, or AI/analytics truth.
- Do not copy Manasight source code or commit raw private Player.log excerpts.
- Do not stage or commit unless explicitly asked.

Required validation:
- python3 -m pytest -q tests/test_draft_complete_parser.py
- python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py
- python3 -m pytest -q tests/test_router_unit.py
- python3 -m pytest -q tests/test_event_schema_snapshots.py
- python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py
- python3 -m pytest -q tests/test_golden_replay_harness.py
- python3 -m pytest -q tests
- python3 -m ruff check src tests tools
- git diff --check
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/124"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_draft_complete.md"
  target_artifact: "docs/implementation_handoffs/parser_draft_complete_comparison.md"
  verdict: "ready_for_module_implementer"
  branch: "codex/parser-reliability-intelligence"
  risk_tier: "High"
  validation:
    - "git diff --check"
    - "git diff --no-index --check /dev/null docs/contracts/parser_draft_complete.md"
    - "LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_draft_complete.md"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or environment variable contracts."
    - "Do not change DraftBot or DraftHuman behavior except for preserving route order around the new DraftComplete parser."
    - "Do not create a new event class or change DraftCompleteEvent.kind."
    - "Do not build draft pick coaching, card ratings, AI draft advice, deck construction analytics, hidden-card inference, archetype classification, gameplay advice, or AI/analytics truth."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
```
