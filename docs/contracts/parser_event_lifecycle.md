# Parser Event Lifecycle Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/32

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Problem-representation docs read because issue #32 is the source problem
representation:

- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

Adjacent contracts:

- `docs/contracts/parser_api_common.md`
- `docs/contracts/parser_client_actions.md`
- `docs/contracts/parser_match_state.md`
- `docs/contracts/parser_state.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the parser-owned event-lifecycle marker parser in
`src/mythic_edge_parser/parsers/event_lifecycle.py`. It is a contract artifact
only. It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/parsers/event_lifecycle.py`

The module recognizes a narrow set of raw MTGA API request lifecycle markers in
Player.log text and emits `EventLifecycleEvent` evidence for event-queue
milestones.

Plain English: this module does not parse lifecycle JSON payload details,
infer match or game identity, mutate parser state, post workbook rows, or own
event analytics. It maps known raw request markers to a small set of stable
parser event types and preserves the raw body as evidence.

## Owning Layer

Parser and state interpretation.

`event_lifecycle.py` owns:

- lifecycle request marker recognition
- known marker-to-type mapping
- non-match fallback behavior
- construction of `EventLifecycleEvent` payloads
- raw lifecycle body preservation at `payload["raw_event_lifecycle"]`

Parser truth boundary:

- `event_lifecycle.py` owns raw lifecycle-marker recognition and emitted
  lifecycle payload shape.
- `events.py` owns `EventLifecycleEvent`, its `kind`, and its performance
  class.
- `router.py` owns dispatch order, header buckets, and unknown-entry
  accounting.
- `app/config.py` owns the configured set of lifecycle event types that
  `app/transforms.py` should keep.
- `app/transforms.py` owns inclusion, serialization, and summaries after an
  `EventLifecycleEvent` exists.
- `app/saved_event_replay.py` owns reconstructing saved lifecycle events from
  archived JSONL records.
- Parser state, workbook formulas, dashboard logic, Apps Script, webhook
  transport, and AI notes must not reinterpret raw lifecycle markers as parser
  truth.

## Files Owned By This Contract

- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `tests/test_parser_small_modules.py`, for event-lifecycle focused tests
- `docs/contracts/parser_event_lifecycle.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/events.py`
- `tests/test_events.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_router_unit.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/transforms.py`
- `tests/test_transforms.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `tests/test_saved_event_replay.py`
- `tests/test_parser_regressions.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `docs/contracts/parser_api_common.md`

## Public Interface

### Function

`try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None`

Public parser entrypoint.

Contract status:

- Reads `entry.body`.
- Returns an `EventLifecycleEvent` for recognized lifecycle request markers.
- Returns `None` for non-matching bodies.
- Does not inspect `entry.header` directly.
- Does not parse JSON from the body.
- Does not call `api_common.is_api_request()`.
- Does not mutate the `LogEntry`, parser state, runtime state, files, or
  workbook surfaces.

### Known Marker Mapping

Current mapping and precedence:

| Event type | Pattern | Precedence |
| --- | --- | --- |
| `event_join` | `==>\s*EventJoin` | 1 |
| `event_claim_prize` | `==>\s*EventClaimPrize` | 2 |
| `event_enter_pairing` | `==>\s*EventEnterPairing` | 3 |

Precedence is tuple order in `_EVENT_LIFECYCLE_PATTERNS`, not raw-text
position. If more than one known lifecycle marker appears in the same body,
the first matching tuple entry wins.

### Implementation Details

The following names are implementation details. Their behavior is
contract-covered through `try_parse()`, but other modules should not import
them as public API:

- `_EVENT_LIFECYCLE_PATTERNS`
- `_matched_event_lifecycle_type(body)`
- `_event_lifecycle_event(timestamp, body, event_type)`

## Inputs

### Raw Log Entry

| Input | Type | Source | Required |
| --- | --- | --- | --- |
| `entry.body` | `str` | MTGA `LogEntry` | Yes |
| `entry.header` | `EntryHeader` | log line classifier | Ignored by this parser |
| `timestamp` | `datetime | None` | router timestamp extraction | No |

Representative matching inputs:

```text
[UnityCrossThreadLogger]==> EventJoin {"id":"event-1"}
```

```text
[UnityCrossThreadLogger]==> EventEnterPairing {"id":"event-2"}
```

```text
[UnityCrossThreadLogger]==> EventClaimPrize {"id":"event-3"}
```

Representative non-matching input:

```text
[UnityCrossThreadLogger]==> EventSomethingElse
```

## Outputs

### Non-Parse Output

`try_parse()` returns `None` when no known lifecycle marker pattern matches
`entry.body`.

Non-match behavior is important because router dispatch then continues to
later parser modules in the same header bucket. Lifecycle parser false
positives can shadow later parsers.

### `EventLifecycleEvent`

Successful parses return an `EventLifecycleEvent` from `events.py`.

Observed event properties:

- `kind == "EventLifecycle"`.
- `performance_class == PerformanceClass.DURABLE_PER_EVENT`.
- `metadata.timestamp` is the timestamp passed to `try_parse()`.
- `metadata.raw_bytes == entry.body.encode()`.
- `metadata.raw_bytes_hash` is derived by `EventMetadata`.
- `payload["type"]` is one of:
  - `event_join`
  - `event_claim_prize`
  - `event_enter_pairing`
- `payload["raw_event_lifecycle"]` is the original `entry.body` string.

Payload shape:

```json
{
  "type": "event_join",
  "raw_event_lifecycle": "[UnityCrossThreadLogger]==> EventJoin {\"id\":\"event-1\"}"
}
```

The parser does not extract event IDs, queue IDs, match IDs, game numbers,
rank, prize content, pairing metadata, or JSON payload fields from lifecycle
bodies.

## Marker Recognition Behavior

Observed current behavior:

- Matching uses local compiled regex patterns.
- Regex matching uses `pattern.search(body)`, so a marker may appear anywhere
  in the body.
- `==>` must appear before the lifecycle method name.
- `\s*` means zero or more whitespace characters, including spaces, tabs, and
  newlines, may appear between `==>` and the method name.
- Matching is case-sensitive.
- There is no API-name boundary after the method name.
- Known markers can match as prefixes of longer names. For example,
  `==> EventJoinSomethingElse` currently matches `event_join`.
- The parser does not require valid JSON after the marker.
- The parser does not require the marker to be on the first line.
- The parser does not require a specific `EntryHeader` in direct calls.

Multiple-marker precedence:

- `event_join` wins whenever its pattern appears anywhere in the body.
- If no join pattern appears, `event_claim_prize` wins when present.
- If neither join nor claim-prize appears, `event_enter_pairing` wins when
  present.
- Raw-text order does not decide the emitted type.

Examples:

| Body | Output |
| --- | --- |
| `==> EventJoin` | `event_join` |
| `==> EventClaimPrize` | `event_claim_prize` |
| `==> EventEnterPairing` | `event_enter_pairing` |
| `==>\nEventJoin` | `event_join` |
| `==> eventjoin` | `None` |
| `==> EventJoinSomethingElse` | `event_join` |
| `==> EventEnterPairing ... ==> EventJoin` | `event_join` |
| `==> EventClaimPrize ... ==> EventJoin` | `event_join` |

Required guarantees:

- Preserve the current known marker set until a future contract explicitly
  expands it.
- Preserve current tuple precedence unless a future contract explicitly changes
  multi-marker behavior.
- Preserve case-sensitive matching.
- Preserve raw body preservation.
- Do not parse lifecycle JSON into new first-class fields without a new
  contract.
- Do not replace local regex behavior with `api_common.is_api_request()`
  without explicitly handling the behavior differences around prefix matching,
  allowed method-name characters, and first-match semantics.

## Router Dispatch Relationship

`router.py` owns dispatch order. `event_lifecycle.py` is included in these
router buckets:

- `EntryHeader.UNITY_CROSS_THREAD_LOGGER`
- `EntryHeader.UNKNOWN`

It is not included in these buckets:

- `EntryHeader.METADATA`
- `EntryHeader.CLIENT_GRE`
- `EntryHeader.CONNECTION_MANAGER`
- `EntryHeader.MATCHMAKING`

Current `UNITY_CROSS_THREAD_LOGGER` dispatch order places lifecycle parsing
after:

- GRE
- client actions
- match state
- session

and before:

- rank
- collection
- inventory
- connection state
- connection close
- connection error

Current `UNKNOWN` dispatch order places lifecycle parsing after:

- GRE
- client actions
- match state
- session

and before:

- rank
- collection
- inventory

Router implications:

- `dispatch_to_parsers()` stops at the first parser module that returns a
  truthy result.
- If `event_lifecycle.try_parse()` returns an event, later parser modules do
  not inspect that entry.
- False positives can shadow rank, collection, inventory, and connection
  parsers for the same body.
- False negatives let later parsers or router unknown tracking handle the
  entry.

Required compatibility:

- Do not change router dispatch order as part of this module contract unless a
  future problem representation and contract explicitly authorize it.
- Do not broaden lifecycle marker recognition without considering parser
  shadowing risk.

## Transform And Config Boundaries

`app/config.py` defines `KEEP_EVENT_LIFECYCLE_TYPES`:

- `event_join`
- `event_enter_pairing`
- `event_claim_prize`

`app/transforms.py` consumes lifecycle events as follows:

- `include_event(event)` returns `True` only when
  `event.kind == "EventLifecycle"` and `payload["type"]` is in
  `KEEP_EVENT_LIFECYCLE_TYPES`.
- `to_serializable(event)` serializes lifecycle events with the standard
  `kind`, `timestamp`, `raw_bytes_hash`, and `payload` keys.
- `summarize(event)` returns `EventLifecycle type=<payload type>`.
- `to_sheet_rows(event)` does not create normalized workbook rows for
  lifecycle events.

Runner implications:

- Kept lifecycle events can be archived to local JSONL through
  `to_serializable()`.
- The raw/archive row written by `to_serializable()` includes
  `raw_event_lifecycle` in the payload.
- Lifecycle parsing does not directly post workbook rows.

Required compatibility:

- Parser marker mapping and `KEEP_EVENT_LIFECYCLE_TYPES` must remain
  synchronized for emitted lifecycle event types that should be retained.
- Adding a new lifecycle event type requires a contract decision covering both
  parser recognition and transform inclusion.
- Workbook schema, webhook payload shape, Apps Script behavior, and dashboard
  formulas must not become lifecycle marker truth owners.

## Saved Event Replay

`app/saved_event_replay.py` maps saved records with
`kind == "EventLifecycle"` back to `EventLifecycleEvent`.

Compatibility expectations:

- `EventLifecycleEvent.kind` must remain `"EventLifecycle"`.
- The payload must remain JSON-serializable.
- Saved lifecycle records should remain reconstructable through
  `EVENT_CLASS_BY_KIND`.

## Observed Current Behavior

- `==> EventJoin` emits `event_join`.
- `==> EventClaimPrize` emits `event_claim_prize`.
- `==> EventEnterPairing` emits `event_enter_pairing`.
- Unknown lifecycle-like markers return `None`.
- Matching is regex-based, case-sensitive, and not API-boundary exact.
- Whitespace and newlines between `==>` and the method name are accepted.
- Prefix matches such as `EventJoinSomethingElse` currently match.
- Multiple known markers use tuple precedence, not raw-text order.
- The parser preserves the raw body string in `raw_event_lifecycle`.
- The parser stores `entry.body.encode()` in event metadata raw bytes.
- The parser has no project side effects.

## Required Guarantees

- Keep `try_parse(entry, timestamp)` as the public parser entrypoint.
- Keep the current three event types and marker mapping.
- Keep non-matching entries returning `None`.
- Keep emitted event class as `EventLifecycleEvent`.
- Keep `EventLifecycleEvent.performance_class == DurablePerEvent`.
- Keep metadata timestamp and raw bytes derived from the router timestamp and
  raw body.
- Keep `payload["raw_event_lifecycle"]` as the original raw body string.
- Keep the parser narrow: no JSON lifecycle field extraction, no match/game
  identity inference, no state mutation, and no direct workbook posting.
- Keep transform/config inclusion synchronized with emitted lifecycle types.
- Keep parser-owned lifecycle truth inside parser/state layers.

## Unknowns

- Whether marker matching should require an API-name boundary so
  `EventJoinSomethingElse` does not match `EventJoin`.
- Whether matching should remain local-regex based or use
  `api_common.is_api_request()` in the future.
- Whether multi-marker bodies should follow tuple precedence, raw-text order,
  or be treated as unsupported.
- Whether lifecycle JSON payload content should remain raw-only forever.
- Whether future lifecycle markers should be added, and if so, how they should
  synchronize with `KEEP_EVENT_LIFECYCLE_TYPES`.
- Whether lifecycle parsing should continue to apply to both
  `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN` router headers.

## Suspected Gaps

- Focused tests do not appear to lock prefix-match behavior for longer method
  names such as `EventJoinSomethingElse`.
- Focused tests do not appear to lock case sensitivity.
- Focused tests do not appear to lock whitespace and newline behavior after
  `==>`.
- Focused tests do not appear to lock tuple precedence when multiple known
  lifecycle markers appear in one body.
- Focused tests do not appear to assert metadata timestamp, raw bytes, raw
  hash, or performance class.
- Focused tests do not appear to lock router shadowing implications around
  lifecycle parser position before rank, collection, and inventory.
- Transform tests do not appear to cover
  `KEEP_EVENT_LIFECYCLE_TYPES` inclusion for lifecycle events.
- Saved-event replay tests do not appear to cover `EventLifecycle` records.

## Error Behavior

- Non-matching bodies return `None`.
- Bodies with known markers but malformed or absent JSON still emit a lifecycle
  event because the parser does not parse JSON.
- Missing or non-string `entry.body` is outside the current public contract.
- Direct calls with any `LogEntry.header` can emit an event if the body
  matches; router header buckets decide normal runtime reachability.
- Contract ambiguity about marker exactness, router shadowing, transform
  inclusion, or downstream ownership must route back to Codex B rather than
  being implemented silently.

## Side Effects

`try_parse()` has no project side effects.

It must not:

- mutate `LogEntry`
- mutate parser runtime state
- infer match or game identity
- parse lifecycle JSON into new payload fields
- post webhooks
- update workbook rows
- write local logs
- write runtime status files
- write failed-post queues
- write generated data
- export workbook files

Any local JSONL archive writes, runtime status updates, analytics submission,
or workbook posting decisions happen downstream in runner, transforms, outputs,
or runtime surfaces.

## Dependency Order

Implementation threads should evaluate changes in this order:

1. `src/mythic_edge_parser/parsers/event_lifecycle.py`
2. `tests/test_parser_small_modules.py`
3. `src/mythic_edge_parser/events.py`, only if event class metadata or
   performance-class compatibility is implicated
4. `src/mythic_edge_parser/router.py`, only if dispatch implications are
   explicitly in scope
5. `tests/test_router_unit.py`
6. `src/mythic_edge_parser/app/config.py`, only if emitted lifecycle types or
   inclusion policy changes are explicitly in scope
7. `src/mythic_edge_parser/app/transforms.py`
8. `tests/test_transforms.py`
9. `src/mythic_edge_parser/app/saved_event_replay.py`
10. `tests/test_saved_event_replay.py`
11. `tests/test_parser_regressions.py`

Do not start with parser state, workbook, webhook, Apps Script, dashboard,
AI-layer, or final reconciliation changes.

## Compatibility

Compatibility surfaces that must remain stable:

- `event_lifecycle.try_parse()` import path and signature
- `EventLifecycleEvent.kind == "EventLifecycle"`
- `EventLifecycleEvent.performance_class == PerformanceClass.DURABLE_PER_EVENT`
- payload field names:
  - `type`
  - `raw_event_lifecycle`
- current event type strings:
  - `event_join`
  - `event_claim_prize`
  - `event_enter_pairing`
- raw body string preservation
- metadata raw bytes from `entry.body.encode()`
- non-match fallback to `None`
- router bucket reachability through `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN`
- transform inclusion through `KEEP_EVENT_LIFECYCLE_TYPES`
- saved-event replay mapping for `EventLifecycle`

Breaking changes that require a new problem representation or contract:

- adding, removing, or renaming lifecycle event types
- parsing lifecycle JSON into first-class payload fields
- changing regex matching to require API-name boundaries
- changing case sensitivity
- changing whitespace behavior after `==>`
- changing multi-marker precedence
- switching to `api_common.is_api_request()` without documenting behavior
  differences
- changing router dispatch order
- making lifecycle events directly produce workbook rows
- changing event class, performance class, or payload field names
- moving lifecycle marker interpretation downstream

## Validation Obligations

Documentation-only checks for this contract:

```bash
git diff --check
```

Focused validation expected for later implementation or review:

```bash
python3 -m pytest -q tests/test_parser_small_modules.py
python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py
python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py
python3 -m ruff check src tests
```

Before submitter opens or updates a module PR, run or verify:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
```

If no behavior changes are needed, the implementation handoff should still
record why existing tests are sufficient or identify the exact missing contract
tests.

## Tests Required

Focused tests expected for Module Implementer or Module Fixer:

- Known marker mapping:
  - `EventJoin` emits `event_join`
  - `EventClaimPrize` emits `event_claim_prize`
  - `EventEnterPairing` emits `event_enter_pairing`
- Fallback:
  - unknown `Event...` request markers return `None`
  - unrelated bodies return `None`
- Regex behavior:
  - matching is case-sensitive
  - whitespace and newline after `==>` are accepted
  - prefix-match behavior for longer method names is locked as current
    behavior or routed back to B if changed
  - multiple known markers follow tuple precedence
- Event shape:
  - `kind == "EventLifecycle"`
  - `performance_class == DurablePerEvent`
  - metadata timestamp is passed through
  - metadata raw bytes equal `entry.body.encode()`
  - raw bytes hash is populated
  - payload contains exactly the expected public fields unless a new contract
    changes payload shape
  - `raw_event_lifecycle` preserves the full raw body string
- Parser scope:
  - malformed JSON after a known marker still emits lifecycle evidence
  - lifecycle JSON fields are not extracted into first-class payload fields
- Router compatibility:
  - lifecycle parser remains after session and before rank/collection/inventory
    in `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN` buckets
  - dispatch stops after lifecycle event emission
- Transform/config compatibility:
  - all emitted lifecycle types are present in `KEEP_EVENT_LIFECYCLE_TYPES`
  - `include_event()` keeps known lifecycle events
  - `summarize()` produces lifecycle summaries
  - `to_serializable()` preserves lifecycle payloads
  - `to_sheet_rows()` continues not producing normalized workbook rows unless
    a future contract explicitly changes row behavior
- Saved replay:
  - saved `EventLifecycle` records reconstruct as `EventLifecycleEvent`

## Acceptance Criteria

- The contract clearly names owned files and related consumer files.
- The public parser entrypoint is documented.
- Known marker-to-type mapping and precedence are documented.
- Non-match fallback behavior is documented.
- Regex matching behavior is documented, including prefix behavior, case
  sensitivity, whitespace, and multi-marker precedence.
- Emitted event metadata, performance class, and payload shape are documented.
- Raw-body preservation expectations are documented.
- Router dispatch implications and shadowing risk are documented.
- Transform/config inclusion boundaries are documented.
- Side-effect and no-mutation expectations are documented.
- Test obligations are specific enough for Codex C or Codex D to implement or
  verify.
- Protected surfaces remain unchanged.

## Next Workflow Action

Next role: Codex C, Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for #32 and docs/contracts/parser_event_lifecycle.md.

Goal:
Compare the current event lifecycle parser implementation and focused tests against the parser event lifecycle contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/32
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_event_lifecycle.md
- docs/contracts/parser_api_common.md
- src/mythic_edge_parser/parsers/event_lifecycle.py
- tests/test_parser_small_modules.py
- src/mythic_edge_parser/router.py
- tests/test_router_unit.py
- src/mythic_edge_parser/events.py
- tests/test_events.py
- src/mythic_edge_parser/app/config.py
- src/mythic_edge_parser/app/transforms.py
- tests/test_transforms.py
- src/mythic_edge_parser/app/saved_event_replay.py
- tests/test_saved_event_replay.py
- tests/test_parser_regressions.py

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned lifecycle marker truth boundaries.
- Add focused tests for contracted event-lifecycle behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a downstream compatibility update.
- Preserve the current marker set unless the contract explicitly routes a change.
- Produce docs/implementation_handoffs/parser_event_lifecycle_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior unless required by the contract and covered by focused tests.
- Expand the marker set, parse lifecycle JSON into new fields, or change router dispatch order unless routed through an explicit contract decision.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned lifecycle marker truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/32"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_event_lifecycle.md"
  target_artifact: "docs/implementation_handoffs/parser_event_lifecycle_comparison.md"
  risk_tier: "Medium"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior unless required by the contract and covered by focused tests."
    - "Do not expand the marker set, parse lifecycle JSON into new fields, or change router dispatch order unless routed through an explicit contract decision."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned lifecycle marker truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not target main for module PR work."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Source problem representation: GitHub issue #32, tracked by parser module
audit tracker #5.

Contract produced: `docs/contracts/parser_event_lifecycle.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/5

Risk tier: Medium.

Owning truth layer: parser and state interpretation.

Public interface:

- `try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None`

Invariants:

- Known markers map to `event_join`, `event_claim_prize`, and
  `event_enter_pairing`.
- Non-matching bodies return `None`.
- Regex matching is case-sensitive, local, and tuple-precedence based.
- Prefix matches such as `EventJoinSomethingElse` currently match.
- Emitted events are `EventLifecycleEvent` with `DurablePerEvent` performance
  class.
- Metadata raw bytes are `entry.body.encode()`.
- `raw_event_lifecycle` preserves the full raw body string.
- The parser has no project side effects and does not parse lifecycle JSON
  fields into first-class payload data.

Required tests: focused marker mapping, fallback, regex behavior, event shape,
router compatibility, transform/config inclusion, saved replay, and downstream
no-truth-movement obligations listed in `Tests Required`.

Acceptance criteria: listed above.

Open questions or contract risks:

- Current regexes match known markers as prefixes of longer method names.
- Multiple markers use tuple precedence rather than raw-text order.
- The parser uses local regexes rather than `api_common.is_api_request()`.
- Lifecycle JSON content is raw-only today.
- Parser marker mapping and `KEEP_EVENT_LIFECYCLE_TYPES` must stay
  synchronized if future lifecycle types are added.

Next recommended thread role: Codex C, Module Implementer.
