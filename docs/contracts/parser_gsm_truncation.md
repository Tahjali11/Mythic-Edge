# GSM Truncation Parser Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/107

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Source artifact:

- `docs/problem_representations/parser_feature_equity_with_manasight.md`

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Branch target: `codex/parser-reliability-intelligence`

This is a contract artifact only. It does not implement code, copy Manasight
source code, paste raw private log excerpts, or change parser behavior by
itself.

## Purpose

Mythic Edge must treat Arena GameStateMessage truncation or summarization
markers as first-class parser-owned data-loss evidence.

The parser should be able to say, deterministically:

- Arena emitted a GameStateMessage truncation marker.
- The marker means expected GameState evidence was omitted or summarized.
- Any available counts are evidence about the omitted payload shape, not
  recovered game objects or annotations.
- Match, game, workbook, webhook, Apps Script, dashboard, and AI layers must
  not invent missing facts from the marker.

Feature equity with the local Manasight reference means behavior and evidence
coverage parity, not source-code parity. Codex threads must not copy Manasight
source code or commit raw private Player.log excerpts.

## Owned Files

Implementation files this contract is expected to own or authorize:

- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/parsers/truncation.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/transforms.py`, only for event inclusion and
  summary behavior explicitly described below
- focused tests listed in this contract
- `docs/contracts/parser_gsm_truncation.md`

Related files whose behavior is referenced but not owned except through the
specific compatibility requirements below:

- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_parsers.py`
- `tests/test_parser_regressions.py`
- `tests/test_saved_event_replay.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`
- `tests/test_router_smoke.py`
- `tests/test_tailer_router_integration.py`

## Parser Truth Boundary

Parser-owned truth:

- detection that an Arena GameStateMessage truncation or summarization marker
  occurred
- normalized marker category
- normalized count fields when they are explicitly present and safely parsed
- parser confidence that the marker was detected by an explicit marker shape
- event metadata and raw-bytes hash through existing `EventMetadata`
- evidence labels that the affected GameState evidence is incomplete
- routing, replay, and local diagnostic behavior for the truncation signal

Not parser-owned by this feature:

- reconstruction of omitted GameState payload contents
- invented game objects, annotations, zones, actions, timers, or card facts
- inferred match result, game result, winner, game identity, or match identity
  from truncation alone
- workbook schema, webhook payload shape, Apps Script behavior, dashboard
  formulas, or AI-generated truth
- raw log retention beyond existing in-memory `EventMetadata.raw_bytes` and
  derived `raw_bytes_hash`

Downstream systems may consume the truncation event as data-loss evidence. They
must not promote the marker into recovered game facts.

## Protected Surfaces

This contract authorizes only the minimum parser/event/replay/test changes
needed for GSM truncation evidence. It does not authorize changes to:

- parser state final reconciliation
- workbook schema or row fields
- webhook payload shape or delivery semantics
- Apps Script behavior
- extractor behavior
- match identity or game identity
- deduplication semantics
- secrets or environment variables
- raw logs
- generated runtime artifacts committed to the repo
- runtime status file schema
- failed-post schema
- workbook exports

Schema snapshot updates are allowed only for parser event schema and payload
snapshot files that must change because `TruncationEvent` becomes a supported
parser event.

## Observed Current Behavior

Observed from the current code:

- `src/mythic_edge_parser/events.py` has no `TruncationEvent`, and the
  `GameEvent` union does not include truncation/data-loss events.
- `src/mythic_edge_parser/log/entry.py` has no truncation-specific
  `EntryHeader` or header policy. Unknown bracket headers become
  `EntryHeader.UNKNOWN`.
- `src/mythic_edge_parser/router.py` has no truncation parser dispatch path.
  Unknown entries are routed through existing GRE, client-action, match-state,
  session, event-lifecycle, rank, collection, and inventory parsers.
- `src/mythic_edge_parser/parsers/gre/__init__.py` only emits
  `GameStateEvent` and optional paired `GameResultEvent` for GRE game-state
  messages. It does not emit a data-loss event for summarized or truncated GSM
  markers.
- `src/mythic_edge_parser/app/saved_event_replay.py` does not list
  `Truncation` in `EVENT_CLASS_BY_KIND`; saved records with that kind would be
  skipped under current behavior.
- `src/mythic_edge_parser/app/transforms.py` does not include or summarize a
  truncation event kind.
- Current tests cover parser routing, GRE game states, header buffering,
  saved-event replay, and event schema snapshots, but they do not cover GSM
  truncation marker detection or false-positive avoidance.

## Required Guarantees

### First-Class Event

Add a parser event class:

`TruncationEvent(BaseEvent)`

Required class constants:

- `kind = "Truncation"`
- `performance_class = PerformanceClass.INTERACTIVE_DISPATCH`

`TruncationEvent` must be included in the public `GameEvent` union.

The event is data-loss evidence. It is not a replacement `GameStateEvent` and
must not be paired with a `GameResultEvent`.

### Public Parser Module

Add a dedicated parser module:

`src/mythic_edge_parser/parsers/truncation.py`

Public API:

`try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None`

Required behavior:

- Return a single `TruncationEvent` when the entry is an explicit GSM
  truncation marker.
- Return `None` for non-marker entries.
- Never raise for malformed marker-like input.
- Never parse or fabricate the omitted GameState payload.
- Never emit `GameStateEvent`, `GameResultEvent`, `MatchStateEvent`, or
  `ClientActionEvent`.
- Preserve provenance with `EventMetadata(timestamp, entry.body.encode())`.
- Keep helper functions private unless future contracts make them public.

### Event Payload

The normalized event payload must be stable and JSON-serializable.

Required fields:

| Field | Value contract |
| --- | --- |
| `type` | `"game_state_message_truncation"` |
| `marker_family` | `"game_state_message_truncation"` |
| `affected_event_family` | `"GameState"` |
| `affected_message_type` | `"GREMessageType_GameStateMessage"` |
| `data_loss` | `True` |
| `recoverable` | `False` |
| `parser_confidence` | `"explicit_marker"` for an exact marker match |
| `value_source` | `"observed"` |
| `confidence` | `"high"` for an exact marker match |
| `finality` | `"live"` |
| `drift_flag` | `"missing_expected_payload_path"` |
| `source_header` | `entry.header.value` |
| `game_object_count` | `int | None` |
| `annotation_count` | `int | None` |

Optional field:

| Field | Value contract |
| --- | --- |
| `raw_marker_summary` | A bounded sanitized summary of recognized marker labels and parsed counts; never a pasted raw log excerpt. |

The payload must not contain reconstructed game objects, annotations, zones,
actions, timers, raw JSON GameState payloads, raw private log paths, webhook
URLs, secrets, or environment variable values.

### Count Semantics

`game_object_count` and `annotation_count` are evidence about the shape of the
omitted payload.

Required normalization:

- Parse a count only when an explicit recognized count line is present.
- Store parsed counts as nonnegative integers.
- Treat `0` as a valid explicit count.
- Treat missing, blank, negative, non-integer, or ambiguous values as `None`.
- Do not infer one count from the other.
- Do not treat counts as recovered objects or annotations.

### Header And Buffering Strategy

Add first-class header recognition for truncation marker blocks.

Required header behavior:

- Add an `EntryHeader` value dedicated to truncation markers. Recommended enum
  member: `TRUNCATION_MARKER`; recommended value: `"TruncationMarker"`.
- A line whose first non-timestamp content begins with the explicit Arena GSM
  summarization marker prefix must start a truncation marker entry. The
  contracted marker-family prefix is the issue-described sanitized prefix
  `"[Message summarized"`; do not paste a private full log line into code or
  tests.
- Truncation marker entries are multiline entries so related marker/count lines
  can be collected until the next recognized header or end-of-file flush.
- Existing known-header behavior must remain unchanged.
- Unknown bracketed headers that are not explicit GSM truncation markers must
  continue to be treated as `EntryHeader.UNKNOWN`.

False-positive requirements:

- Do not classify arbitrary prose containing words such as "summary",
  "summarized", "truncated", `GameObject Count`, or `Annotation Count` unless
  the entry begins with the explicit GSM truncation marker shape.
- Do not classify normal GRE JSON, client actions, match state events,
  metadata, connection messages, or unrelated unknown headers as truncation.
- Synthetic tests must use sanitized marker text, not raw private log excerpts.

### Router Dispatch

Required router behavior:

- Dispatch `EntryHeader.TRUNCATION_MARKER` entries to `parsers.truncation`.
- Add the truncation parser to UNKNOWN fallback dispatch only if needed to
  preserve detection for marker entries that the header layer cannot safely
  classify. If added to UNKNOWN, it must run before broad parsers and must
  still use exact marker detection.
- Do not add truncation dispatch to metadata, connection, matchmaking, or
  client-GRE header paths unless a later contract authorizes that expansion.
- A routed truncation event increments routed-entry stats and must not also be
  counted as unknown.
- Timestamp behavior follows existing router rules: use the first-line
  timestamp when present and parseable; otherwise emit with `timestamp=None`
  while preserving existing timestamp-missing or timestamp-parse-failure stats.
- Emit exactly one `TruncationEvent` per marker entry.

### GRE Parser Relationship

The truncation parser is sibling evidence to GRE game-state parsing, not a
replacement for it.

Required relationship:

- `parsers/gre/__init__.py` continues to own JSON GRE message parsing,
  `GameStateEvent` emission, connect-response emission, and game-result pairing.
- The truncation parser owns explicit marker-block parsing.
- Truncation events must not cause GRE game-state builders to receive
  fabricated `gameStateMessage` dictionaries.
- A truncation marker must not be interpreted as game-over, match-complete, or
  winner evidence.

### Saved Replay And Schema Snapshots

Required compatibility:

- Add `Truncation` support to saved-event replay so saved records for this
  event kind round-trip instead of being skipped.
- Update parser event class and payload snapshot fixtures to include
  `TruncationEvent` and its payload keys.
- Snapshot updates must be limited to parser event/schema evidence required by
  the new event. Workbook, webhook, Apps Script, runtime status, failed-post,
  and export schemas must not change.

### Transform And Runtime Handling

Required behavior:

- `include_event()` must include `Truncation` so the event can be archived and
  replayed by the existing local event pipeline.
- `to_sheet_rows()` must return `[]` for `Truncation` unless a later workbook
  contract explicitly authorizes a row shape.
- `summarize()` must provide a concise sanitized `Truncation` summary using
  normalized fields only.
- Runtime status may naturally report `last_event_kind = "Truncation"` through
  existing status fields, but this contract does not authorize new runtime
  status fields.
- Runtime surfaces may include the event in existing local timelines if
  `include_event()` marks it keepable, but this contract does not authorize new
  timeline schema fields.
- `app/state.py` must ignore `Truncation` for match/game summary mutation.

### Diagnostics And Drift

Required behavior:

- Log drift reports should count routed `Truncation` events by kind through the
  existing routed-event-kind mechanism.
- The marker should stop appearing as an unknown signature once routed.
- No raw private log text should be committed to drift baselines, test
  fixtures, docs, or reports.

## Accepted Input Shapes

The implementation should support sanitized/synthetic versions of the Arena GSM
marker block shape described by issue #107 and the source problem
representation:

- an explicit summarization marker line beginning with the sanitized marker
  family prefix `"[Message summarized"`
- optional recognized count lines for omitted game objects using the
  issue-described label family `GameObject Count`
- optional recognized count lines for omitted annotations using the
  issue-described label family `Annotation Count`

The exact marker prefix and count labels must be encoded as narrow parser
constants in `parsers/truncation.py` or `log/entry.py`, with tests documenting
them through synthetic examples.

Unknown future marker families are out of scope unless they share the explicit
GSM truncation marker shape. Future expansion should come through a new
contract or contract amendment.

## Malformed Input

Malformed marker-like input must be safe:

- Marker line present but counts missing: emit `TruncationEvent` with count
  fields set to `None`.
- Marker line present with malformed counts: emit `TruncationEvent` with only
  safely parsed counts populated.
- Count lines present without the explicit marker line: return `None`.
- Non-string, empty, or whitespace-only bodies routed through direct tests:
  return `None` or emit no event without raising.
- Multiple count lines for the same field: use the first safely parsed value,
  or document and test a deterministic last-value policy before implementing.

No malformed input path may write files, post webhooks, mutate parser state, or
invent recovered GameState facts.

## Public Interfaces

### `TruncationEvent`

Owned by `src/mythic_edge_parser/events.py`.

Public event class used by router, stream, saved replay, schema snapshots, and
local event serialization.

### `parsers.truncation.try_parse()`

Owned by `src/mythic_edge_parser/parsers/truncation.py`.

Public parser hook called by router dispatch. It should be directly covered by
focused unit tests.

### `EntryHeader.TRUNCATION_MARKER`

Owned by `src/mythic_edge_parser/log/entry.py`.

Public header enum member used by the line buffer and router. It should be
covered by header/buffer tests proving exact marker recognition and no
regression for existing known and unknown headers.

## Unknowns

- The committed repo does not contain raw private Arena marker examples, and
  this contract intentionally does not add them.
- The exact full Arena marker text may vary by MTGA client version. The first
  implementation should start with the explicit marker family described in
  issue #107 and sanitized tests.
- It is unknown whether future marker families will summarize non-GSM payloads.
  This contract only covers GameStateMessage truncation/summarization markers.
- It is unknown whether count labels can appear with localized text, commas, or
  alternate casing. The first implementation should be exact and conservative;
  broaden only with new evidence and tests.

## Suspected Gaps

- Current router unknown-signature reports likely hide truncation markers among
  generic unknown entries instead of preserving a parser-owned data-loss
  signal.
- Current saved-event replay would skip a future saved `Truncation` record
  unless explicitly updated.
- Current event schema snapshots will fail once the event class is added until
  snapshots are intentionally refreshed.
- Current transform inclusion rules would drop the event from the existing
  archive/replay path unless `include_event()` is updated.

## Test Obligations

Module Implementer/Fixer must add or update focused tests proving:

- `TruncationEvent` exists with kind `Truncation` and
  `PerformanceClass.INTERACTIVE_DISPATCH`.
- `GameEvent` includes `TruncationEvent`.
- `parsers.truncation.try_parse()` emits one event for a sanitized explicit GSM
  marker block.
- Parsed payload contains all required fields and no reconstructed GameState
  content.
- Metadata raw-bytes hash is stable and derived from the marker entry body.
- Missing counts produce `None`.
- Explicit zero counts produce `0`.
- Malformed counts produce `None` without raising.
- Count-only lines without the explicit marker do not emit events.
- Non-marker unknown entries remain unknown/non-routed as before.
- Existing known headers retain their current buffering behavior.
- Truncation marker headers are multiline and collect related count lines.
- Router emits exactly one `TruncationEvent` for a marker entry.
- Router stats count the marker as routed, not unknown.
- Timestamp present, missing, and malformed paths follow existing router
  timestamp behavior.
- GRE GameState and GameResult parser tests remain unchanged in meaning.
- Saved-event replay supports `Truncation`.
- Parser event schema and payload snapshots include `Truncation` and only the
  expected payload keys.
- `include_event()` includes `Truncation`.
- `to_sheet_rows()` returns no workbook rows for `Truncation`.
- `summarize()` returns a sanitized summary for `Truncation`.
- Drift reports count routed `Truncation` events and no longer list the
  synthetic marker as an unknown signature.
- No tests commit raw private log excerpts.

Recommended test files:

- `tests/test_gsm_truncation_parser.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`
- `tests/test_parsers.py`
- `tests/test_saved_event_replay.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_log_drift_sensor.py`

Optional regression tests, if they can remain synthetic and small:

- `tests/test_parser_regressions.py`
- `tests/test_router_smoke.py`
- `tests/test_tailer_router_integration.py`

## Validation Obligations

For the implementation pass, run the focused suite first:

```bash
python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py
```

Then run regression coverage appropriate to touched surfaces:

```bash
python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py
python3 -m ruff check src tests
python3 tools/check_protected_surfaces.py --base origin/main
```

If branch-local hardening tools such as validation selector or secret-pattern
scanner are unavailable, record them as unavailable instead of inventing a
replacement requirement. If they are available, run them with the same base
branch discipline:

```bash
python3 tools/select_validation.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
```

## Acceptance Criteria

The contract is satisfied when:

- GSM truncation/summarization markers produce a first-class
  `TruncationEvent`.
- The event preserves parser-owned data-loss evidence without reconstructing
  missing game facts.
- The marker is routed deterministically and stops being an unknown entry.
- Saved replay and parser event schema snapshots understand the new event.
- Local archive/summarization can retain the event without changing workbook,
  webhook, Apps Script, runtime status schema, or failed-post schema.
- Synthetic tests cover detection, false positives, counts, metadata, routing,
  replay, and schema behavior.
- Raw private log excerpts and Manasight source code are not copied into the
  repo.

## Next Workflow Route

Recommended next role: Codex C, Module Implementer.

Codex D should only be used if Codex C returns a concrete blocker or reviewer
findings require a fixer loop.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for parser reliability issue #107 and docs/contracts/parser_gsm_truncation.md.

  Goal:
  Implement the smallest coherent parser/event/replay/test changes needed to satisfy the GSM truncation marker contract. Treat Arena GameStateMessage truncation/summarization markers as parser-owned data-loss evidence, not recovered game truth.

  Use:
    - https://github.com/Tahjali11/Mythic-Edge/issues/107
    - https://github.com/Tahjali11/Mythic-Edge/issues/47
    - https://github.com/Tahjali11/Mythic-Edge/issues/11
    - docs/contracts/parser_gsm_truncation.md
    - docs/problem_representations/parser_feature_equity_with_manasight.md
    - docs/contracts/player_log_evidence_ledger.md
    - docs/agent_constitution.md
    - docs/agent_rules.yml
    - docs/codex_module_workflow.md
    - src/mythic_edge_parser/events.py
    - src/mythic_edge_parser/log/entry.py
    - src/mythic_edge_parser/router.py
    - src/mythic_edge_parser/parsers/__init__.py
    - src/mythic_edge_parser/parsers/gre/__init__.py
    - src/mythic_edge_parser/app/saved_event_replay.py
    - src/mythic_edge_parser/app/transforms.py
    - tests/test_log_entry_headers.py
    - tests/test_entry_buffer_edges.py
    - tests/test_router_unit.py
    - tests/test_parsers.py
    - tests/test_saved_event_replay.py
    - tests/test_event_schema_snapshots.py
    - tests/test_log_drift_sensor.py

  Do:
    - Compare current behavior against the contract before editing.
    - Add a first-class TruncationEvent with kind "Truncation" and InteractiveDispatch performance class.
    - Add a dedicated parser module for explicit GSM truncation markers.
    - Add first-class header/buffer and router handling if required by the contract.
    - Preserve exact false-positive boundaries with synthetic/sanitized tests.
    - Preserve EventMetadata raw-bytes hash behavior.
    - Add saved replay and parser schema snapshot support for the new event.
    - Keep workbook/webhook/App Script/runtime status schema/failed-post schemas unchanged.
    - Produce docs/implementation_handoffs/parser_gsm_truncation_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

  Do not:
    - Copy Manasight source code.
    - Paste raw private Player.log excerpts into repo files.
    - Reconstruct omitted GameState payload data.
    - Infer match winner, game winner, match identity, game identity, or final reconciliation facts from truncation alone.
    - Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts committed to the repo, runtime status file schema, failed-post schema, or workbook exports.
    - Target main directly; parser reliability work belongs on codex/parser-reliability-intelligence.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/107"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_gsm_truncation.md"
  target_artifact: "docs/implementation_handoffs/parser_gsm_truncation_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py"
    - "python3 -m ruff check src tests"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not copy Manasight source code."
    - "Do not paste raw private Player.log excerpts into repo files."
    - "Do not reconstruct omitted GameState payload data."
    - "Do not infer match winner, game winner, match identity, game identity, or final reconciliation facts from truncation alone."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts committed to the repo, runtime status file schema, failed-post schema, or workbook exports."
    - "Do not target main directly; parser reliability work belongs on codex/parser-reliability-intelligence."
    - "Do not mark tracker #47 complete."
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/107"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_gsm_truncation.md"
  target_artifact: "docs/implementation_handoffs/parser_gsm_truncation_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py"
    - "python3 -m ruff check src tests"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not copy Manasight source code."
    - "Do not paste raw private Player.log excerpts into repo files."
    - "Do not reconstruct omitted GameState payload data."
    - "Do not infer match winner, game winner, match identity, game identity, or final reconciliation facts from truncation alone."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts committed to the repo, runtime status file schema, failed-post schema, or workbook exports."
    - "Do not target main directly; parser reliability work belongs on codex/parser-reliability-intelligence."
    - "Do not mark tracker #47 complete."
