# EventBus Queue Pressure Metrics Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/467>

## Project Roadmap

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Contract

`docs/contracts/event_bus_queue_pressure_metrics.md`

## Prerequisites

- #460 / PR #654: EventBus completeness-over-liveness behavior
- #471 / PR #655: EventBus consumer delivery classification
- #467 / PR #656: EventBus queue pressure metrics contract
- #470 / PR #657: heavy subscriber worker-queue planning

## Internal Project Area

Parser.

## Truth Owner

Parser and state interpretation. `src/mythic_edge_parser/event_bus.py` owns the
in-memory parser event fanout and the new in-memory queue-pressure snapshot.
The snapshot is diagnostic-only and does not own parser truth, delivery policy
authorization, runtime reliability readiness, workbook truth, webhook truth,
API truth, analytics truth, AI truth, coaching truth, or production reliability
truth.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer.

## What Changed

Implemented an additive, in-memory EventBus queue-pressure metrics snapshot.

The patch adds:

- frozen public-safe snapshot dataclasses in `event_bus.py`;
- `EventBus.queue_pressure_snapshot()`;
- `EventBus.reset_queue_pressure_metrics()`;
- optional public-safe `consumer_id` metadata on `EventBus.subscribe()`;
- EventBus-owned counters for publish calls, publish waits, queue depth
  high-water marks, wait summaries, and event-rate buckets;
- symbolic subscriber refs such as `subscriber_1`;
- fail-closed handling for unknown or unsafe consumer ids;
- #471 consumer class/status vocabulary in metrics output;
- clearing of queue-keyed metrics state on close so metrics do not retain
  queued `GameEvent` objects beyond the existing subscriber delivery path.

## Files Changed

- `src/mythic_edge_parser/event_bus.py`
- `tests/test_event_bus_queue_pressure_metrics.py`
- `docs/implementation_handoffs/event_bus_queue_pressure_metrics_comparison.md`

## Code Changed

Runtime code changed only in `src/mythic_edge_parser/event_bus.py`.

The EventBus delivery contract remains the same:

- no capacity tuning;
- no fanout changes;
- no worker queues;
- no live metric collection;
- no runtime artifacts;
- no API/workbook/webhook/App Script payloads;
- no parser event class changes;
- no parser fact changes.

`subscribe()` remains backward-compatible. Existing callers may still call
`bus.subscribe()` without arguments. The default subscriber classification is
`unknown_subscriber` / `unknown` / `classification_required`, which is
fail-closed for runtime metrics review.

## Tests Added Or Updated

Added `tests/test_event_bus_queue_pressure_metrics.py`.

Focused coverage proves:

- metrics start empty and public-safe;
- publishing increments counters and queue depths;
- max depth preserves the observed high-water mark;
- full-queue backpressure records publish wait metrics without changing
  delivery order;
- symbolic subscriber refs and #471 consumer class labels appear in summaries;
- unknown/unsafe consumer ids fail closed without echoing input;
- raw event payloads, event kind labels, raw bytes, hashes, path markers, and
  secret-like markers do not appear in snapshot output;
- metrics reset does not clear queues or change delivery;
- closed bus snapshots drop subscriber summaries and keep only aggregate
  counters.

Existing `tests/test_event_bus.py` continues to cover #460 backpressure
behavior.

## Interface Changes

Additive only:

- `EventBus(capacity: int = 1024, *, time_source: Callable[[], float] | None = None)`
- `EventBus.subscribe(*, consumer_id: str = "unknown_subscriber")`
- `EventBus.queue_pressure_snapshot() -> EventBusQueuePressureSnapshot`
- `EventBus.reset_queue_pressure_metrics() -> None`
- public frozen dataclasses:
  - `EventBusQueuePressureSnapshot`
  - `EventBusSubscriberPressure`
  - `EventBusEventRateSummary`
  - `EventBusPublishWaitSummary`

No existing call sites needed to change.

## Contracted Area Status

The implementation stayed inside the contracted Parser / shared-support area.
No downstream bridge surfaces were touched. The snapshot copies #471 consumer
classification vocabulary but does not change classification, delivery
requirements, degradation rules, or consumer behavior.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: satisfied by aggregate-only metrics,
  EventBus-generated subscriber refs, fail-closed unknown consumer handling,
  and focused no-echo tests.
- Vocabulary and example coherence: uses the contract vocabulary for
  `metrics_status`, `pressure_status`, `classification_status`,
  `consumer_class`, wait buckets, rate buckets, and non-claims.
- Authority/readiness semantics: satisfied; metrics are diagnostic-only and
  include non-claims.
- Fail-closed schema or validator checks: satisfied for unknown/unsafe
  consumer ids.
- Protected-surface rollout phase: no protected downstream surface changed.

## Validation Run

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus_queue_pressure_metrics.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_stream_unit.py tests/test_events.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m ruff check src/mythic_edge_parser/event_bus.py tests/test_event_bus.py tests/test_event_bus_queue_pressure_metrics.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_runner.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests
PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
git diff --check
```

## Still Unverified

- No live metrics were collected.
- No runtime artifact, status API, local app view, workbook, webhook, Apps
  Script, frontend, or CI surface exposes the snapshot.
- No capacity tuning, concurrent fanout, worker queues, sequence-gap behavior,
  replay audit behavior, or readiness gate was attempted.
- Existing runtime subscribers still use the default unknown classification
  until a later authorized integration names public-safe consumer ids at call
  sites.

## Reviewer Focus

Review should focus on:

- whether metrics change EventBus delivery semantics in any edge case;
- whether queue-keyed metrics state is fully cleared on close;
- whether public snapshot output can echo raw payload, path, secret, event kind,
  hash, or private marker data;
- whether default unknown classification is the right fail-closed behavior for
  current runtime subscribers until a later call-site integration is
  authorized;
- whether the additive `time_source` and `consumer_id` parameters are acceptable
  for deterministic tests and future public-safe classification wiring.

## Next Workflow Action

Next role: Codex E.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for EventBus queue pressure metrics snapshot.

Repository:
Tahjali11/Mythic-Edge

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source contract:
docs/contracts/event_bus_queue_pressure_metrics.md

Implementation handoff:
docs/implementation_handoffs/event_bus_queue_pressure_metrics_comparison.md

Review scope:
Review the additive in-memory EventBus queue-pressure metrics snapshot. Verify
that the implementation preserves #460 delivery behavior, preserves #471
consumer classification boundaries, remains public-safe/no-echo, and does not
introduce runtime artifacts, API/workbook/webhook/App Script payloads, capacity
tuning, fanout changes, worker queues, live metric collection, parser event
class changes, parser behavior changes, CI changes, or readiness/truth claims.

Expected output:
Findings first, validation reviewed, remaining risks, recommended next role,
and workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/event_bus_queue_pressure_metrics.md"
  target_artifact: "docs/implementation_handoffs/event_bus_queue_pressure_metrics_comparison.md"
  verdict: "event_bus_queue_pressure_metrics_snapshot_ready_for_review"
  risk_tier: "High"
  base_branch: "origin/main"
  branch: "codex/event-bus-queue-pressure-metrics-snapshot"
  runtime_artifact_creation_authorized: false
  live_metric_collection_authorized: false
  capacity_change_authorized: false
  fanout_change_authorized: false
  worker_queue_change_authorized: false
  parser_behavior_change_authorized: false
  parser_event_class_change_authorized: false
  api_payload_change_authorized: false
  workbook_webhook_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
```
