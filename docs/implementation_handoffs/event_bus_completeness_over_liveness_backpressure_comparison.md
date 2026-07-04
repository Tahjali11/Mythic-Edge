# EventBus Completeness Over Liveness Backpressure Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/460>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Contract

`docs/contracts/event_bus_completeness_over_liveness_backpressure.md`

## Role Performed

Codex C: Module Implementer.

Codex D: Module Fixer for `EVENTBUS-BACKPRESSURE-E-001`.

## Implementation Summary

`EventBus.publish()` now preserves queued parser/runtime events under
subscriber backpressure. Instead of dropping the oldest queued event when a
subscriber queue is full, publishing waits until the event is accepted into the
subscriber queue or the bus enters the explicit close path.

The close path now sets an internal close event and enqueues subscriber
sentinels only where queue capacity is immediately available. This allows a
publisher waiting on a full queue to stop waiting when the bus is closing,
while preserving already accepted queued events for the subscriber to consume
before the subscriber receives the close signal.

## Files Changed

- `src/mythic_edge_parser/event_bus.py`
- `tests/test_event_bus.py`
- `docs/implementation_handoffs/event_bus_completeness_over_liveness_backpressure_comparison.md`

Pre-existing source artifact retained:

- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`

## Behavior Change

Before:

- `publish()` used `put_nowait()`.
- On `asyncio.QueueFull`, it removed the oldest queued event with
  `get_nowait()`.
- Queue fullness could cause silent parser/runtime event loss and subscriber
  removal.

After:

- `publish()` awaits queue capacity for each subscriber.
- A full queue does not drop the oldest event.
- A full queue does not remove the subscriber as dead.
- Publishing after close still returns without delivery.
- Close still causes `Subscriber.recv()` to return `None`.

## Tests Added

`tests/test_event_bus.py` covers:

- publishing blocks when a capacity-1 subscriber queue is full;
- the first queued event is preserved and delivered before the second event;
- a slow subscriber is not removed as dead;
- close still delivers the `None` close signal;
- publishing after close does not deliver a new event;
- close unblocks a publisher waiting on a full queue after the queued event is
  consumed.
- close returns even when a subscriber queue is already full, while preserving
  the already accepted queued event before `recv()` returns `None`.

## Codex D Fixer Addendum

### Finding Fixed

`EVENTBUS-BACKPRESSURE-E-001`: `EventBus.close()` could deadlock when called
while a subscriber queue was full because close awaited insertion of a close
sentinel into the same bounded queue.

### Root Cause

The close path used the subscriber event queue itself to deliver shutdown state.
That is safe for an empty queue, but unsafe when backpressure has already filled
the bounded queue. In that state, `close()` had to wait for subscriber capacity
before it could finish.

The first D pass also exposed a race in the blocked-publisher path: a queued
`asyncio.Queue.put()` task could win capacity at the same time close started.

### Fix Applied

- `Subscriber` now receives the bus close event and returns `None` once the bus
  is closed and all already accepted queued events have been drained.
- `Subscriber.recv()` notifies the bus when it frees queue capacity.
- `EventBus.publish()` now waits for queue space through an explicit
  `asyncio.Condition`, which lets close deterministically stop blocked
  publishers without relying on cancellation of a racing queue put task.
- `EventBus.close()` sets the close event, wakes blocked publishers, preserves
  sentinel delivery for queues with available capacity, and no longer attempts
  to block on sentinel insertion into full subscriber queues.

This keeps the behavior in-memory and EventBus-owned only. It does not change
parser event classes, parser truth ownership, workbook/webhook behavior, CI, or
runtime readiness policy.

## Validation Run

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_stream_unit.py tests/test_events.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_stream_integration.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_runner.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m ruff check src/mythic_edge_parser/event_bus.py tests/test_event_bus.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
git diff --check
```

Results:

- `tests/test_event_bus.py`: 6 passed.
- `tests/test_stream_unit.py tests/test_events.py`: 3 passed.
- `tests/test_stream_integration.py`: 3 passed.
- `tests/test_runner.py`: 18 passed.
- Full repository pytest: 2074 passed.
- Ruff on touched source/test files: passed.
- Ruff on `src tests tools`: passed.
- Agent docs consistency check: passed.
- Path-scoped secret/private marker scan over changed #460 files: passed,
  forbidden 0.
- Path-scoped protected-surface gate over changed #460 files: passed,
  forbidden 0.
- `git diff --check`: passed.

Direct synthetic deadlock probe after the D fix:

- `close()` returned while the capacity-1 subscriber queue was full.
- The subscriber then received the already queued event.
- The next `recv()` returned `None`.

## Still Unverified

- Real MTGA live-capture behavior was not exercised.
- No release, deploy, production, reliability-readiness, parser-truth,
  security-assurance, privacy-assurance, analytics-truth, AI-truth, or
  coaching-truth claim is made.

## Scope Preserved

No changes were made to:

- parser event classes;
- parser state final reconciliation;
- match identity;
- game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- runtime status artifact schemas;
- CI;
- analytics behavior;
- AI/model-provider behavior.

## Reviewer Focus

Review should focus on:

- whether `_put_unless_closed()` correctly preserves completeness while allowing
  close to unblock a waiting publisher;
- whether close behavior remains acceptable for queued events and sentinels;
- whether the focused async tests sufficiently prove the new queue-full
  behavior;
- whether broader runner tests should be required before submitter handoff.

## Next Workflow Action

Next recommended role: Codex E.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #460.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/460

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/event_bus_completeness_over_liveness_backpressure.md

Implementation handoff:
docs/implementation_handoffs/event_bus_completeness_over_liveness_backpressure_comparison.md

Goal:
Review the EventBus completeness-over-liveness implementation and the Codex D
fix for `EVENTBUS-BACKPRESSURE-E-001` against the contract. Lead with findings.
Verify that full subscriber queues no longer silently drop queued events or
remove subscribers as dead, and that close behavior no longer deadlocks when a
subscriber queue is full.

Protected boundaries:
Do not implement code, open a PR, change parser event classes, change parser
state final reconciliation, change match/game identity, change workbook or
webhook schema, change CI, or claim reliability/parser/release/deploy/
production readiness.

Expected output:
Findings first, validation reviewed, residual risk, recommended next role, and
workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/460"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/event_bus_completeness_over_liveness_backpressure.md"
  target_artifact: "docs/implementation_handoffs/event_bus_completeness_over_liveness_backpressure_comparison.md"
  fixed_finding_id: "EVENTBUS-BACKPRESSURE-E-001"
  verdict: "event_bus_close_full_queue_deadlock_fix_ready_for_review"
  risk_tier: "High"
  base_branch: "origin/main"
  branch: "codex/event-bus-completeness-over-liveness-460"
  implementation_authorized: true
  eventbus_behavior_change_authorized: true
  parser_behavior_change_authorized: false
  ci_change_authorized: false
  pr_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
```
