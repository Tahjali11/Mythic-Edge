# EventBus Completeness Over Liveness Backpressure Contract

## Module

`src/mythic_edge_parser/event_bus.py`

Plain English: the EventBus is the in-memory async delivery path between the
MTGA log stream/router and subscribers that consume parser events. This
contract defines the future behavior expected when a subscriber queue is full:
preserve parser/runtime event completeness by applying backpressure, rather
than silently dropping queued events to keep publishing live.

This Codex B pass writes only this contract. It does not implement EventBus
behavior changes, change parser behavior, add parser event classes, change
runtime status artifacts, change CI, open a PR, or claim readiness.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/460>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source problem: GitHub issue #460 Codex A problem representation
- Base branch inspected: `origin/main`
- Latest verified `origin/main`: `99ac62103d38ff68f526fd3c010d9a6004462ff1`
- Target artifact:
  `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- Risk tier: High

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- issue #460
- tracker #568
- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_events.py`
- `tests/test_stream_unit.py`
- `tests/test_runner.py`
- `docs/contracts/parser_runner.md`
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py` as
  adjacent backpressure vocabulary reference only

## Owning Layer

Primary internal project area: Parser.

Truth owner: parser and state interpretation.

`event_bus.py` owns in-memory parser event fanout semantics. It does not own
MTGA raw log truth, parser event-class definitions, match identity, game
identity, final reconciliation, workbook schema, webhook payload shape, Apps
Script behavior, runtime status artifact schemas, analytics truth, AI truth, or
coaching truth.

## Bridge-Code Status

`shared_support`

The EventBus is parser-owned shared support used by `stream.py`, the parser
runner path, and tests. It supports event transport inside the parser runtime,
but must not become a downstream correction layer or a status-artifact owner by
accident.

## Files Owned By This Contract

- `src/mythic_edge_parser/event_bus.py`
- future focused EventBus tests, expected path:
  `tests/test_event_bus.py`
- this contract:
  `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`

Related files referenced but not owned:

- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_stream_unit.py`
- `tests/test_runner.py`

## Current Behavior And First Bad Value

Current behavior in `EventBus.publish(event)`:

1. If the bus is closed, it returns.
2. For each subscriber queue, it calls `q.put_nowait(event)`.
3. If the subscriber queue is full, it catches `asyncio.QueueFull`.
4. It removes the oldest queued event with `q.get_nowait()`.
5. It retries `q.put_nowait(event)`.
6. If that fails, it removes the subscriber as dead.

First bad value:

```text
asyncio.QueueFull
  -> q.get_nowait()
  -> oldest queued GameEvent silently removed
```

Why it is bad: parser/runtime evidence can be lost without a visible
degradation marker, data-loss status, exception, diagnostic, or backpressure.
That favors liveness over completeness.

Second bad value:

```text
QueueFull
  -> remove subscriber as dead
```

Why it is bad: a slow subscriber and a broken subscriber are different
conditions. Full queues should not be treated as dead subscribers unless a
future contract defines explicit timeout, cancellation, or subscriber-health
semantics.

## Scope Decision

In scope for a later Codex C implementation:

- make default EventBus delivery completeness-preserving under backpressure;
- preserve per-subscriber event order;
- preserve current public constructor and method names;
- add focused async tests for full subscriber queues;
- keep close/sentinel behavior coherent with blocked publishers;
- document any timeout/cancellation behavior used by tests.

Out of scope for this issue:

- parser event class changes;
- new data-loss event classes;
- runtime status artifact schema changes;
- diagnostics artifact schema changes;
- source `Player.log` parsing changes;
- router behavior changes;
- stream polling behavior changes except what is necessary to await the
  EventBus contract;
- runner state/final reconciliation changes;
- match identity changes;
- game identity changes;
- deduplication changes;
- workbook schema changes;
- webhook payload shape changes;
- Apps Script behavior changes;
- analytics behavior;
- AI/model-provider behavior;
- CI changes;
- readiness, reliability-readiness, parser-truth, release-readiness,
  deploy-readiness, production-readiness, analytics-truth, AI-truth, or
  coaching-truth claims.

## Public Interface

### `Subscriber[T].recv() -> T | None`

Receives the next item from the subscriber queue.

Contract:

- returns a `GameEvent` subtype while the stream is active;
- returns `None` only when it receives the close sentinel;
- must not synthesize missing events;
- must not expose internal queue sentinels or queue objects;
- must not turn backpressure into parser truth or analytics truth.

### `EventBus.__init__(capacity: int = 1024) -> None`

Creates an EventBus with bounded per-subscriber queues.

Contract:

- `capacity` is the max queue size for each subscriber queue;
- the default capacity remains `1024`;
- invalid capacity handling is implementation-defined today and should remain
  unchanged unless Codex C finds a concrete bug that requires focused tests;
- capacity is not a completeness guarantee by itself.

### `EventBus.with_default_capacity() -> EventBus`

Creates a bus with the current default capacity.

Contract:

- preserves the existing convenience constructor;
- does not introduce environment-variable configuration, runtime status
  artifacts, or CI policy.

### `EventBus.subscribe() -> Subscriber[GameEvent]`

Creates a subscriber queue and returns a `Subscriber`.

Contract:

- each subscriber receives events independently;
- one subscriber's queue pressure must not reorder another subscriber's events;
- subscribing does not replay historical events;
- subscriber creation does not create files, logs, status artifacts, workbook
  rows, webhook payloads, or analytics outputs.

### `EventBus.publish(event: GameEvent) -> None`

Publishes one parser event to each active subscriber.

Future contract behavior:

- default behavior must preserve delivery completeness by awaiting queue
  capacity for each active subscriber;
- default behavior must not silently remove the oldest queued event;
- default behavior must not silently drop the newest event;
- default behavior must not remove a subscriber solely because its queue is
  full;
- per-subscriber order must remain first-in, first-out;
- if the bus is already closed, publish may keep returning without delivery, as
  it does today.

Allowed implementation shape:

```text
for each active subscriber queue:
    await queue.put(event)
```

The exact code does not need to match this pseudocode. The observable behavior
does.

Forbidden implementation shapes:

```text
QueueFull -> get_nowait() -> put_nowait(event)
QueueFull -> drop oldest event silently
QueueFull -> drop newest event silently
QueueFull -> remove subscriber as dead solely because the queue is full
QueueFull -> record only a comment without observable behavior
```

### `EventBus.close() -> None`

Closes the bus and sends the sentinel to subscribers.

Contract:

- close still eventually causes `Subscriber.recv()` to return `None`;
- close must not silently discard already accepted queued parser events unless
  a later shutdown-specific contract explicitly changes drain semantics;
- if close is called while a publisher is blocked by backpressure, the
  implementation must avoid deadlock;
- close behavior must remain in-memory only and must not create runtime
  artifacts or workbook/webhook output.

## Inputs

| Input | Type | Source | Contract |
| --- | --- | --- | --- |
| `event` | `GameEvent` union | `stream.py` after router output | Already parser-produced event; EventBus must not reinterpret payload. |
| subscriber queue | `asyncio.Queue[object]` | `EventBus.subscribe()` | Bounded per-subscriber queue. |
| `capacity` | `int` | EventBus constructor | Queue capacity, not a loss policy. |
| close sentinel | private object | EventBus module | Internal shutdown marker only. |

Forbidden inputs for this contract:

- raw `Player.log` or `UTC_Log` contents;
- app-data, live MTGA state, private smoke data, or private logs;
- workbook exports;
- webhook payloads;
- Apps Script state;
- analytics outputs;
- AI/model-provider outputs;
- runtime status files as input authority;
- local generated artifacts as input authority.

## Outputs

| Output | Destination | Contract |
| --- | --- | --- |
| delivered `GameEvent` | each subscriber queue | Preserved in publish order unless the bus was already closed. |
| `None` sentinel result | subscriber receiving after close | Close signal only. |
| async backpressure | publishing coroutine | Expected when a subscriber queue is full. |

This contract does not define any durable output artifact, runtime status file,
new parser event class, data-loss marker schema, workbook row, webhook payload,
or analytics output.

## Completeness And Backpressure Vocabulary

`completeness_preserving_delivery`: publish does not return for a subscriber
until the event has been accepted into that subscriber's queue or the bus has
entered an explicitly handled close/cancellation path.

`backpressure_wait`: publish awaits space in a full subscriber queue.

`silent_drop`: an event is removed, skipped, overwritten, or lost without a
visible error, status, or explicit data-loss artifact. Silent drop is forbidden
for default EventBus behavior.

`slow_subscriber`: a subscriber whose queue is full because it is not consuming
events fast enough. A slow subscriber is not automatically a dead subscriber.

`dead_subscriber`: a subscriber that is explicitly closed, cancelled, or
otherwise proven unusable by a future contract. Queue fullness alone is not
proof.

`lossy_delivery_mode`: any mode that drops or coalesces events. This contract
does not authorize lossy delivery mode.

## Invariants

- Parser-produced events must remain parser events; EventBus must not mutate
  event payloads.
- Default queue-full behavior must apply backpressure rather than silent loss.
- Event order must remain stable per subscriber.
- One subscriber's backpressure must not reorder another subscriber's delivered
  event sequence.
- Queue capacity must not become a hidden data-loss budget.
- `Subscriber.recv()` must continue to return `None` for close.
- The EventBus must not claim reliability readiness, parser truth, or
  production readiness from unit tests alone.

## Error Behavior

Malformed or unsupported event values are outside this contract. Codex C should
not add broad runtime type validation unless a focused test proves a current
bug.

Backpressure behavior:

- A full queue should block the publisher until capacity is available.
- Tests may use `asyncio.wait_for()` or equivalent bounded waits to prove the
  publisher is waiting.
- Cancellation or timeout in tests must not be mistaken for an EventBus data
  loss policy.

Close behavior:

- Closing an idle bus should deliver sentinels as it does today.
- Closing with queued events should not silently imply those events were
  processed.
- If Codex C cannot make close and blocked publish semantics safe without
  defining new shutdown policy, it must stop and route back to Codex B.

Unsupported lossy behavior:

- Any future need to drop, coalesce, summarize, or mark data loss requires a
  separate problem representation and contract for the status/degradation
  surface.
- This issue does not authorize data-loss schemas or parser event-class
  additions.

## Side Effects

Allowed future implementation side effects:

- in-memory queue operations only;
- async waiting on subscriber queues;
- focused tests.

Forbidden side effects:

- writing files;
- creating runtime status artifacts;
- creating failed-post records;
- posting webhooks;
- updating workbook rows;
- changing Apps Script;
- changing CI;
- reading private logs or app-data;
- changing parser event classes;
- changing parser state final reconciliation;
- changing match/game identity or deduplication;
- adding analytics or AI/model-provider behavior.

## Dependency Order For Later Implementation

1. Add focused EventBus tests that reproduce the full-queue behavior with a
   small capacity.
2. Change `EventBus.publish()` to use completeness-preserving backpressure.
3. Verify `stream.py` still awaits `publish()` without interface changes.
4. Verify close/sentinel behavior still works.
5. Run focused stream/EventBus tests.
6. Run broader parser tests only if the focused change affects stream or
   runner behavior beyond `event_bus.py`.

## Compatibility

Must remain compatible:

- `EventBus(capacity=...)`
- `EventBus.with_default_capacity()`
- `EventBus.subscribe()`
- `await EventBus.publish(event)`
- `await EventBus.close()`
- `await Subscriber.recv()`
- `None` as the subscriber close signal
- current `GameEvent` classes in `src/mythic_edge_parser/events.py`
- `MtgaEventStream.start()` creating a default EventBus and one subscriber

The contract does not require legacy compatibility for silent dropping. Silent
dropping is the behavior being retired.

## Tests Required For Later Codex C

Focused tests should prove:

- with capacity `1`, publishing a second event blocks while the first event is
  still queued;
- once the subscriber consumes the first event, the blocked publish completes
  and the second event is delivered;
- the first event is not replaced by the second event;
- per-subscriber order is preserved;
- a full queue does not remove the subscriber as dead;
- `close()` still causes `recv()` to return `None`;
- publishing after close does not deliver new events;
- `MtgaEventStream` still routes events through the EventBus using the same
  public interface.

Suggested validation commands:

```bash
python3 -m pytest -q tests/test_event_bus.py
python3 -m pytest -q tests/test_stream_unit.py
python3 -m pytest -q tests/test_events.py
git diff --check
```

If Codex C changes stream or runner behavior, also run:

```bash
python3 -m pytest -q tests/test_runner.py
```

## Acceptance Criteria

- The default EventBus path no longer silently drops the oldest queued event
  when a subscriber queue is full.
- `publish()` applies observable backpressure under full-queue conditions.
- Event order and event completeness are proven by focused async tests.
- Subscriber close behavior is still tested.
- No parser event classes, runtime status schemas, workbook schemas, webhook
  payloads, Apps Script behavior, analytics behavior, CI gates, private data
  reads, or readiness claims are introduced.

## Stop Conditions

Stop and route back to Codex B or Codex A if implementation needs:

- new parser event classes;
- data-loss marker schemas;
- runtime status artifact changes;
- diagnostics artifact schema changes;
- subscriber-health policy beyond queue fullness;
- cross-thread or cross-process delivery redesign;
- stream/tailer/router redesign;
- parser state final reconciliation changes;
- match identity, game identity, or deduplication changes;
- workbook/webhook/App Script changes;
- private log reads or live MTGA evidence;
- CI gate changes;
- readiness, reliability-readiness, parser-truth, security/privacy assurance,
  release-readiness, deploy-readiness, production-readiness, analytics-truth,
  AI-truth, or coaching-truth claims.

## Next Workflow Action

Next recommended role: Codex C Module Implementer.

Codex C should implement the smallest EventBus-only behavior change that
satisfies this contract, with focused async tests first. It should not add
data-loss schemas, parser event classes, runtime artifacts, or downstream
behavior.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex C: Module Implementer for issue #460.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/460

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/event_bus_completeness_over_liveness_backpressure.md

Goal:
Implement the smallest EventBus-only change so `EventBus.publish()` preserves
completeness under subscriber backpressure. Add focused async tests proving a
full subscriber queue blocks publishing until the queued event is consumed,
without dropping the oldest event or removing the subscriber as dead.

Protected boundaries:
Do not change parser event classes, parser behavior outside EventBus delivery,
parser state final reconciliation, match/game identity, deduplication, workbook
schema, webhook payload shape, Apps Script behavior, runtime status artifacts,
CI, analytics, AI/model-provider behavior, or readiness/truth/assurance claims.

Expected output:
Implementation, focused tests, validation run, implementation handoff, and
workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/460"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  verdict: "event_bus_completeness_over_liveness_backpressure_contract_ready_for_implementation"
  target_artifact: "docs/contracts/event_bus_completeness_over_liveness_backpressure.md"
  risk_tier: "High"
  base_branch: "origin/main"
  latest_verified_origin_main: "99ac62103d38ff68f526fd3c010d9a6004462ff1"
  implementation_authorized: false
  pr_authorized: false
  eventbus_behavior_change_authorized: false
  parser_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
```
