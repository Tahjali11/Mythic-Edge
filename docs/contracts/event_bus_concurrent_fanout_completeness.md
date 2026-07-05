# EventBus Concurrent Fanout Completeness Contract

Status: contract only
Codex role: B, Module Contract Writer
Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/469
Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
Latest verified `origin/main`: `c2acc9d7ef3d31e1f5f8eb6f0690dbf059c7940e`

## Purpose

This contract defines how Mythic Edge may later fan out one EventBus publish to
multiple subscribers concurrently while preserving completeness.

Plain English behavior:

- EventBus must still deliver every accepted parser event to every active
  subscriber selected for that publish.
- One slow subscriber should not prevent delivery attempts to other subscribers
  that already have queue capacity.
- Per-subscriber event order must remain stable.
- Concurrent fanout is not permission to drop, sample, coalesce, reorder, or
  summarize parser events.
- This pass does not implement fanout changes.

## Source Context

Prerequisites:

- Issue #460 / PR #654 established completeness-preserving EventBus
  backpressure.
- Issue #471 / PR #655 established EventBus consumer delivery classifications.
- Issue #467 / PR #658 established privacy-safe queue pressure metrics.
- Issue #470 / PR #657 established heavy-subscriber worker-queue planning.
- Issue #468 / PR #659 established EventBus capacity configuration and default
  tuning boundaries.

Related future issues:

- Issue #472: sequence IDs and gap detection.
- Issue #473: post-session replay audit.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- GitHub issue #469
- GitHub PR #659
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/contracts/event_bus_consumer_delivery_classification.md`
- `docs/contracts/event_bus_queue_pressure_metrics.md`
- `docs/contracts/event_bus_heavy_subscriber_worker_queues.md`
- `docs/contracts/event_bus_capacity_configuration_and_default_tuning.md`
- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_event_bus.py`
- `tests/test_event_bus_queue_pressure_metrics.py`
- `pyproject.toml`

No private `Player.log`, `UTC_Log`, app-data, live MTGA data, runtime status
files, local-only artifacts, workbook exports, raw diffs, source patches,
secrets, credentials, tokens, API keys, or webhook URLs were read.

## Owning Layer

Primary internal project area: Parser.

Truth owner: parser and state interpretation.

`event_bus.py` owns in-memory parser event delivery mechanics. It does not own
parser event truth, parser event-class definitions, match identity, game
identity, final reconciliation, workbook schema, webhook payload shape, Apps
Script behavior, runtime artifacts, analytics truth, AI truth, coaching truth,
or production reliability truth.

## Bridge-Code Status

`shared_support`

The EventBus is parser-owned shared support used by stream/runtime code,
`runner.py`, local app capture control, and tests. Concurrent fanout may change
in-memory delivery scheduling only after a later implementation is authorized.
It must not become a downstream correction layer, retry system, runtime artifact
owner, or truth owner.

## Files Owned By This Contract

- `docs/contracts/event_bus_concurrent_fanout_completeness.md`

Likely files for a later Codex C implementation, if separately authorized:

- `src/mythic_edge_parser/event_bus.py`
- `tests/test_event_bus.py`
- possibly `tests/test_event_bus_queue_pressure_metrics.py`

Referenced but not owned by this contract:

- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/contracts/event_bus_consumer_delivery_classification.md`
- `docs/contracts/event_bus_queue_pressure_metrics.md`
- `docs/contracts/event_bus_heavy_subscriber_worker_queues.md`
- `docs/contracts/event_bus_capacity_configuration_and_default_tuning.md`

## Observed Current Behavior

Current `EventBus.publish(event)` behavior on `origin/main`:

1. If the bus is closed, publish returns without delivery.
2. It iterates over `list(self._queues)` sequentially.
3. For each subscriber queue, it awaits `_put_unless_closed(q, event)`.
4. If a subscriber queue is full, `_put_unless_closed()` waits for capacity.
5. Later subscriber queues are not attempted until earlier subscriber queue
   waits finish.
6. A successful publish increments in-memory queue pressure metrics after the
   sequential loop finishes.

This preserves completeness after #460, but the fanout loop still couples all
later subscribers to the first slow subscriber in iteration order.

## Problem Statement And First Bad Values

First bad value:

```text
subscriber_1 queue full
  -> EventBus.publish waits on subscriber_1
  -> subscriber_2 delivery attempt is delayed even if subscriber_2 has capacity
```

Why it is bad: completeness is preserved, but liveness is unnecessarily coupled.
Liveness means the system keeps making progress where it safely can. A slow
subscriber should not delay independent delivery attempts to other subscribers.

Second bad value:

```text
concurrent fanout implementation
  -> returns after some subscriber tasks finish
  -> unfinished subscriber tasks continue or fail silently
```

Why it is bad: that would create false success, task leaks, or partial delivery.
Concurrent fanout must have an explicit publish completion barrier.

Third bad value:

```text
publish is cancelled or close happens during fanout
  -> some subscriber tasks accepted event
  -> other subscriber tasks are abandoned without cleanup or status
```

Why it is bad: cancellation and shutdown are the risky parts of concurrent
fanout. A later implementation must prove no task leaks, no deadlock, and no
silent policy change.

Fourth bad value:

```text
#467 pressure metrics or #468 capacity evidence
  -> treated as authority to change fanout behavior
```

Why it is bad: prior metrics and capacity contracts are diagnostic or planning
evidence only. This contract is the fanout boundary, not implementation
authorization.

## Scope Decision

In scope for a later Codex C implementation only if separately authorized:

- change the internal fanout scheduling inside `EventBus.publish()`;
- attempt delivery to subscriber queues from one publish concurrently;
- preserve completeness and per-subscriber order;
- define and test publish completion barrier behavior;
- define and test close and cancellation behavior for fanout tasks;
- keep #467 queue pressure metrics coherent after fanout;
- add focused async tests with slow and fast subscribers.

Out of scope:

- implementing code in this Codex B pass;
- changing EventBus capacity or default capacity;
- collecting live metrics;
- writing runtime artifacts;
- adding worker queues;
- changing parser facts or parser event classes;
- changing match identity, game identity, deduplication, or final reconciliation;
- changing stream, runner, local app, API, workbook, webhook, Apps Script, or CI
  behavior beyond what a later scoped EventBus implementation requires;
- adding sequence IDs, event envelopes, replay, or audit behavior;
- reading raw logs, private app-data, live MTGA data, workbook exports, private
  paths, generated local artifacts, secrets, credentials, tokens, API keys, or
  webhook URLs;
- claiming reliability readiness, parser truth, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching truth.

## Public Interface Boundary

The public EventBus interface must remain compatible:

- `EventBus(capacity=...)`
- `EventBus.with_default_capacity()`
- `EventBus.subscribe(consumer_id=...)`
- `await EventBus.publish(event)`
- `await EventBus.close()`
- `await Subscriber.recv()`
- `EventBus.queue_pressure_snapshot()`
- `EventBus.reset_queue_pressure_metrics()`
- `None` as the subscriber close result

The intended change is internal scheduling only. A later implementation must not
require caller changes in `stream.py`, `runner.py`, local app capture control,
workbook/webhook payloads, API payloads, or parser event classes.

## Fanout Vocabulary

| Term | Meaning |
| --- | --- |
| `publish_call` | One call to `EventBus.publish(event)`. |
| `publish_snapshot` | The list of subscriber queues selected at the start of a publish call. |
| `subscriber_delivery_attempt` | One attempt to place the event into one subscriber queue. |
| `concurrent_fanout` | Scheduling subscriber delivery attempts for the same publish call so independent subscribers can progress while another subscriber waits. |
| `publish_completion_barrier` | The rule that publish may return normally only after all selected subscriber delivery attempts finish or an explicitly handled close path occurs. |
| `per_subscriber_order` | Each subscriber receives events in the same order accepted by publish calls. |
| `partial_delivery` | Some selected subscribers receive an event while others do not. It is forbidden as normal success. |
| `task_leak` | A fanout task continues after publish returns, close completes, or cancellation cleanup should have finished. |
| `external_cancellation` | Cancellation of the publish coroutine by an outside caller. |
| `closed_bus_path` | The explicit behavior when the bus is closed before or during publish. |

Allowed fanout statuses for future tests or handoffs:

- `fanout_not_authorized`
- `fanout_contract_only`
- `fanout_candidate_under_review`
- `fanout_complete`
- `fanout_waiting_on_subscriber`
- `fanout_closed_bus_path`
- `fanout_cancelled_cleanup_required`
- `fanout_blocked_by_shutdown_policy`
- `fanout_review_required`
- `fanout_unknown_fail_closed`

Required non-claim labels:

- `not_fanout_change_authorization`
- `not_capacity_change`
- `not_live_metrics_collection`
- `not_runtime_artifact_authorization`
- `not_worker_queue_authorization`
- `not_parser_truth`
- `not_reliability_readiness`
- `not_release_readiness`
- `not_deploy_readiness`
- `not_production_readiness`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`

Forbidden status labels:

- `lossless_guaranteed`
- `reliability_ready`
- `parser_truth_confirmed`
- `production_safe`
- `partial_delivery_ok`
- `drop_allowed`
- `coalescing_allowed`

## Future Fanout Behavior Requirements

A later implementation may use `asyncio.gather()`, `asyncio.TaskGroup`, or an
equivalent Python 3.11-compatible task grouping approach. The exact code shape
is not the contract. The observable behavior is the contract.

Required behavior:

- each publish call selects a stable `publish_snapshot` of current subscriber
  queues;
- delivery to each selected subscriber is attempted without waiting for unrelated
  subscribers to free capacity first;
- publish returns normally only after every selected subscriber accepts the event;
- if the bus closes during publish, publish follows an explicit tested
  `closed_bus_path`;
- child fanout tasks are awaited, cancelled, or otherwise joined before publish
  returns or propagates cancellation;
- per-subscriber event order remains first-in, first-out for sequential awaited
  publish calls;
- a full queue remains backpressure, not event loss;
- one slow subscriber must not cause event loss for fast subscribers;
- fast-subscriber delivery may complete while a slow subscriber is still waiting;
- queue pressure metrics remain public-safe and diagnostic-only.

Forbidden behavior:

- dropping accepted parser events;
- overwriting queued events;
- removing subscribers solely because a queue is full;
- returning from publish while fanout tasks are still running;
- swallowing fanout task exceptions without a tested policy;
- treating partial delivery as success;
- adding retries or replay;
- changing capacity to mask fanout pressure;
- moving subscriber work into worker queues;
- adding event sequence IDs or gap-detection envelopes;
- exposing raw event payloads, local paths, private data, or secrets.

## Ordering Rules

For one publish call:

- every selected subscriber must receive the same event object or equivalent
  parser event value already accepted by EventBus;
- fanout may complete per-subscriber delivery in different wall-clock order;
- wall-clock completion order must not become parser truth.

For sequential awaited publish calls:

- if caller code does `await publish(first)` and then `await publish(second)`,
  every subscriber that receives both events must receive `first` before
  `second`;
- tests must prove this with at least one slow subscriber and one fast subscriber.

For externally concurrent publish calls:

- this contract does not broaden guarantees beyond existing caller behavior;
- if a later implementation needs deterministic ordering across concurrently
  scheduled publish calls, stop and route back to Codex B or a new issue.

## Close, Cancellation, And Failure Rules

Close behavior:

- `EventBus.close()` must still wake blocked publishers.
- `Subscriber.recv()` must still eventually return `None`.
- Already accepted queued parser events must not be silently discarded by the
  fanout change.
- Close must not hang because a fanout task is waiting on queue capacity.

External cancellation behavior:

- fanout tasks must not leak after the publish coroutine is cancelled;
- cancellation cleanup must be deterministic in tests;
- partial delivery caused by external cancellation must not be reported as normal
  fanout success;
- if exact cancellation semantics cannot be specified without a broader runtime
  degradation policy, stop and route back to Codex B.

Failure behavior:

- unexpected fanout task exceptions must not be hidden;
- future implementation should prefer propagating the exception after child task
  cleanup unless a later contract defines another behavior;
- queue-full alone is not an exception path after #460, it is backpressure.

## Relationship To Consumer Delivery Classification

This contract consumes #471 classifications:

- `truth_critical` consumers keep complete ordered delivery.
- `mixed` consumers keep complete ordered event receipt for their truth-sensitive
  path.
- `unknown` consumers fail closed or are treated as `truth_critical`.
- `test_fixture_only` subscribers may simulate slow and fast behavior in tests,
  but must not weaken runtime rules.

Concurrent fanout must not reclassify consumers. Queue pressure on a consumer
class is diagnostic only and must not become a delivery downgrade.

## Relationship To #467 Metrics

Queue pressure metrics may be used in tests to observe fanout behavior:

- `publish_wait_count`
- `queue_capacity`
- `current_total_queue_depth`
- `max_total_queue_depth`
- per-subscriber `pressure_status`
- public-safe wait buckets

Metrics remain non-authoritative:

- metrics do not authorize fanout changes;
- metrics do not authorize capacity changes;
- metrics do not authorize worker queues;
- metrics do not prove reliability readiness;
- metrics do not prove parser truth.

A later implementation must keep metrics public-safe:

- no raw event payloads;
- no event-kind buckets;
- no raw logs;
- no private paths;
- no secrets;
- no runtime artifacts.

## Relationship To #468 Capacity Configuration

Concurrent fanout must preserve the current capacity boundary:

- no default capacity change;
- no new capacity source;
- no environment variable config;
- no local-app settings config;
- no status API, workbook, webhook, or UI config;
- no unbounded queue behavior.

If a later implementation needs capacity tuning to make concurrent fanout pass
tests, stop and route back to Codex B. Capacity changes are not authorized here.

## Relationship To #470 Worker Queues

Concurrent fanout is not worker-queue implementation.

Allowed:

- fan out the EventBus placement of one event into subscriber queues;
- keep subscriber downstream work exactly where it is today;
- use tests to prove fast subscribers are not blocked by slow subscriber queue
  capacity during the fanout attempt.

Forbidden:

- moving parser state work;
- moving side effects behind worker queues;
- introducing durable retry queues;
- changing SQLite, local app, API, workbook, webhook, or Apps Script behavior;
- treating fanout as proof that heavy subscriber work is fixed.

## Relationship To Future #472 And #473

Issue #472, sequence IDs and gap detection:

- concurrent fanout does not authorize event envelopes, sequence IDs, gap
  detection, or parser event metadata changes;
- if a fanout implementation needs sequence IDs to prove correctness, stop and
  route back to Codex B.

Issue #473, replay audit:

- concurrent fanout does not authorize replay, private log reads, fixture
  promotion, recovery claims, or corpus status changes;
- fanout tests must use synthetic public-safe events only.

## Allowed Inputs

Allowed inputs for later implementation and tests:

- EventBus-owned subscriber queues from `publish_snapshot`;
- EventBus-owned capacity and closed state;
- EventBus-owned condition used for backpressure wakeups;
- synthetic public-safe `GameEvent` values in tests;
- #471 public-safe consumer ids and classifications;
- #467 in-memory queue pressure counters and snapshots;
- process-local monotonic timing already used by queue pressure metrics.

Forbidden inputs:

- raw `Player.log`;
- raw `UTC_Log`;
- private app-data;
- live MTGA state;
- workbook exports;
- webhook payloads;
- Apps Script state;
- raw event payloads in public output;
- private paths;
- generated local artifacts;
- secrets, credentials, tokens, API keys, or webhook URLs;
- provider or model outputs.

## Side Effects

Allowed future side effects, if implementation is separately authorized:

- in-memory task scheduling inside `EventBus.publish()`;
- in-memory queue operations;
- in-memory metrics updates;
- focused tests.

Forbidden side effects:

- writing files;
- creating runtime artifacts;
- collecting live metrics;
- posting webhooks;
- updating workbook rows;
- changing Apps Script;
- changing local API or frontend payloads;
- changing parser event classes;
- changing parser facts;
- changing EventBus capacity;
- adding worker queues;
- changing CI.

## Validation Expectations For Later Implementation

A later Codex C implementation, if separately authorized, should provide
deterministic evidence that:

- a slow first subscriber does not prevent an independent fast later subscriber
  from receiving the event;
- the same slow subscriber eventually receives the event when capacity becomes
  available;
- per-subscriber order remains stable across sequential awaited publishes;
- publish does not return normally before all selected subscriber delivery
  attempts are complete;
- close wakes fanout tasks and does not deadlock;
- external cancellation does not leak fanout tasks;
- queue pressure metrics still expose only public-safe aggregate values;
- #460 backpressure tests still pass;
- #471 consumer classification output is unchanged;
- #468 capacity default and explicit capacity behavior are unchanged;
- #470 worker-queue boundaries are not weakened.

Suggested validation commands for later implementation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus_queue_pressure_metrics.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_runner.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
git diff --check
```

If a future implementation adds a dedicated fanout test file, run it before the
broader EventBus, stream, runner, and live-app tests.

## Acceptance Criteria

- Contract defines concurrent fanout vocabulary.
- Contract identifies the current sequential publish loop as the first bad value.
- Contract preserves #460 completeness and backpressure semantics.
- Contract consumes #471 consumer classifications without changing them.
- Contract treats #467 metrics as diagnostic-only.
- Contract preserves #468 capacity boundaries.
- Contract keeps #470 worker queues out of scope.
- Contract defines close, cancellation, task cleanup, and partial-delivery rules.
- Contract forbids parser behavior changes, parser event class changes, payload
  changes, runtime artifacts, CI changes, private-data reads, and readiness/truth
  claims.
- Contract defines validation evidence required before any later implementation.

## Stop Conditions

Stop and route back to Codex B if later work requires:

- changing EventBus capacity;
- collecting live metrics;
- adding runtime artifacts;
- moving subscriber work into worker queues;
- changing consumer classification;
- adding sequence IDs or event envelopes;
- adding replay or audit behavior;
- changing parser facts, parser event classes, final reconciliation, match
  identity, game identity, or deduplication;
- changing stream, runner, local app, API, workbook, webhook, Apps Script, or CI
  behavior beyond a scoped EventBus implementation;
- defining lossy delivery, stale substitution, sampling, coalescing, retries, or
  data-loss artifacts;
- reading private logs or live MTGA data;
- making reliability readiness, parser truth, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching truth
  claims.

## Recommended Next Role

Recommended next role: Codex E.

Codex E should review this contract against issue #469, #460, #471, #467, #468,
#470, and current EventBus code. Codex E should route back to Codex B if the
completion barrier, close/cancellation behavior, partial-delivery rule, or
ordering expectations are ambiguous.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic-Edge issue #469.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/469

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source artifact:
docs/contracts/event_bus_concurrent_fanout_completeness.md

Review the EventBus concurrent fanout completeness contract against the completed
#460 completeness-over-liveness contract, #471 consumer classification contract,
#467 queue pressure metrics contract, #468 capacity configuration contract, #470
worker-queue planning contract, and current EventBus code.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not change EventBus fanout, capacity, worker queues, parser facts, parser
  event classes, API payloads, workbook/webhook payloads, or CI.
- Do not collect live metrics or create runtime artifacts.
- Do not claim reliability readiness, parser truth, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching truth.

Expected output:
- Findings first, ordered by severity.
- Whether the contract is ready for Codex F or must return to Codex B.
- Validation expectations.
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/469"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/468"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/659"
  latest_merge_commit: "c2acc9d7ef3d31e1f5f8eb6f0690dbf059c7940e"
  completed_thread: "B"
  next_thread: "E"
  verdict: "event_bus_concurrent_fanout_contract_ready_for_review"
  risk_tier: "High"
  target_artifact: "docs/contracts/event_bus_concurrent_fanout_completeness.md"
  fanout_change_authorized: false
  capacity_change_authorized: false
  live_metrics_collection_authorized: false
  runtime_artifact_creation_authorized: false
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
