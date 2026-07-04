# EventBus Queue Pressure Metrics Contract

## Module

`src/mythic_edge_parser/event_bus.py`

Plain English: this contract defines privacy-safe, local-first metrics for
observing EventBus queue pressure after issue #460 changed EventBus delivery to
preserve completeness under backpressure and issue #471 classified current
EventBus consumers by delivery sensitivity. The goal is to make queue pressure
measurable without changing EventBus delivery semantics, changing consumer
classification, collecting live metrics in this Codex B pass, writing runtime
artifacts, exposing raw event payloads, or claiming runtime reliability
readiness.

This Codex B pass writes only this contract. It does not implement code, open a
PR, change EventBus behavior, collect live metrics, create runtime artifacts,
change parser behavior, change parser event classes, change workbook/webhook
or API payloads, change CI, expose raw logs/private paths/secrets, or claim
reliability, readiness, parser truth, release readiness, deploy readiness, or
production readiness.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/467>
- Prerequisite issue: <https://github.com/Tahjali11/Mythic-Edge/issues/460>
- Prerequisite PR: <https://github.com/Tahjali11/Mythic-Edge/pull/654>
- Prerequisite issue: <https://github.com/Tahjali11/Mythic-Edge/issues/471>
- Prerequisite PR: <https://github.com/Tahjali11/Mythic-Edge/pull/655>
- Related future issue: <https://github.com/Tahjali11/Mythic-Edge/issues/468>
- Related future issue: <https://github.com/Tahjali11/Mythic-Edge/issues/469>
- Related future issue: <https://github.com/Tahjali11/Mythic-Edge/issues/470>
- Related future issue: <https://github.com/Tahjali11/Mythic-Edge/issues/472>
- Related future issue: <https://github.com/Tahjali11/Mythic-Edge/issues/473>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source problem: GitHub issue #467 problem representation
- Prerequisite merge commit:
  `b6b865a34e52dcb1c7fb57cb8937a37d4107febb`
- Prerequisite merge commit:
  `09857723c38b4424d585659c8aa21f123af50519`
- Base branch inspected: `origin/main`
- Latest verified `origin/main`:
  `09857723c38b4424d585659c8aa21f123af50519`
- Target artifact:
  `docs/contracts/event_bus_queue_pressure_metrics.md`
- Risk tier: High

Live state observed during this Codex B pass:

- Issue #467 is open and still carries a deferred label in GitHub.
- The current user instruction activates contract-only Codex B work for #467.
- Issue #460 is closed.
- PR #654 is merged at
  `b6b865a34e52dcb1c7fb57cb8937a37d4107febb`.
- Issue #471 is closed.
- PR #655 is merged at
  `09857723c38b4424d585659c8aa21f123af50519`.
- Issues #468, #469, #470, #472, and #473 remain future reliability work and
  are not authorized by this contract.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- issue #467
- issue #460
- issue #471
- issues #468, #469, #470, #472, and #473 as related future work
- PR #654
- PR #655
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/implementation_handoffs/event_bus_completeness_over_liveness_backpressure_comparison.md`
- `docs/contracts/event_bus_consumer_delivery_classification.md`
- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `tests/test_event_bus.py`
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py` as
  adjacent backpressure vocabulary reference only
- current runtime/diagnostics references as boundary context only

No private Player.log, UTC_Log, app-data, live MTGA, runtime status files,
generated local artifacts, workbook exports, source patches, raw diffs,
secrets, credentials, tokens, API keys, or webhook URLs were read.

## Owning Layer

Primary internal project area: Parser.

Truth owner: parser and state interpretation.

`event_bus.py` may own in-memory metrics about its own queue pressure and
publish waits. It does not own parser event truth, runtime readiness, workbook
truth, webhook truth, API truth, analytics truth, AI truth, coaching truth, or
production reliability truth.

`docs/contracts/event_bus_consumer_delivery_classification.md` owns the current
consumer classification vocabulary and inventory. Queue pressure metrics may
refer to that classification, but must not change it.

## Bridge-Code Status

`shared_support`

The EventBus is parser-owned shared support used by stream/runtime code,
`runner.py`, local app capture control, and tests. Metrics may describe EventBus
delivery mechanics and consumer-class pressure, but must not become a downstream
correction layer, a hidden source of parser truth, or an implementation shortcut
for changing consumer delivery behavior.

## Files Owned By This Contract

- `src/mythic_edge_parser/event_bus.py`
- future focused tests, expected path:
  `tests/test_event_bus_queue_pressure_metrics.py`
- this contract:
  `docs/contracts/event_bus_queue_pressure_metrics.md`

Related files referenced but not owned:

- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/status_api.py`
- `tests/test_event_bus.py`
- `tests/test_stream_unit.py`
- `docs/contracts/event_bus_consumer_delivery_classification.md`

## Current Behavior And First Bad Value

Current behavior after #460/#654:

- `EventBus.publish()` waits for subscriber queue capacity.
- A full subscriber queue no longer silently drops the oldest event.
- A full subscriber queue no longer removes the subscriber as dead.
- `EventBus.close()` wakes blocked publishers and preserves already accepted
  queued events before subscriber close.
- Focused tests prove full-queue blocking, order preservation, and close
  behavior.

Current consumer classification after #471/#655:

- `parser_runner_main_loop` is `truth_critical`.
- `local_app_live_capture_supervisor` is `mixed`.
- `mtga_event_stream_start` is `publisher_or_factory`.
- EventBus test subscribers are `test_fixture_only`.
- Future runtime subscriber sites are `unknown` until classified and must fail
  closed or be treated as `truth_critical`.

Current missing behavior:

- EventBus does not expose a dedicated pressure summary.
- There is no in-memory counter for how often publish had to wait.
- There is no queue-depth/max-depth snapshot.
- There is no public-safe subscriber lag summary.
- There is no local-only event-rate summary.
- There is no metrics vocabulary tying pressure summaries to #471 consumer
  classes.

First bad value:

```text
backpressure_wait_happened
  -> no metric or review signal
```

Why it is bad: after completeness-preserving backpressure is correct, the next
reliability question is whether slow subscribers or burst patterns are causing
pressure. Without metrics, capacity, fanout, subscriber design, and recovery
policy decisions would be based on guesses.

Second bad value:

```text
pressure_metrics
  -> raw event payloads or runtime artifacts
```

Why it is bad: pressure metrics must stay aggregate and public-safe. They must
not expose raw parser payloads, private paths, secrets, local logs, or runtime
artifacts.

## Scope Decision

In scope for a later implementation, if separately authorized:

- in-memory EventBus pressure counters;
- queue depth and max observed queue depth;
- publish call counts;
- count of publish calls that had to wait;
- aggregate publish wait duration summaries;
- subscriber lag summaries based on queue depth and capacity;
- consumer-class pressure summaries tied to the #471 classification vocabulary;
- aggregate event-rate summaries using monotonic process-local time;
- public-safe snapshot vocabulary;
- reset semantics for in-memory metrics;
- focused tests proving metrics do not change delivery behavior.

Out of scope:

- changing EventBus delivery semantics from #460;
- changing EventBus consumer classification from #471;
- collecting live metrics in Codex B;
- writing runtime artifacts;
- adding runtime status file fields;
- changing local API payloads;
- changing frontend diagnostics surfaces;
- changing workbook/webhook/App Script behavior;
- changing parser event classes;
- changing parser state final reconciliation;
- changing match identity, game identity, or deduplication;
- reading raw logs, app-data, live MTGA, private decks, local artifacts,
  secrets, credentials, tokens, keys, webhook URLs, provider outputs, or model
  outputs;
- changing CI;
- claiming runtime reliability readiness, release readiness, deploy readiness,
  production readiness, parser truth, security assurance, privacy assurance,
  analytics truth, AI truth, or coaching truth.

## Relationship To Consumer Delivery Classification

Metrics must be joined to the #471 consumer classification boundary before any
later capacity, fanout, worker-queue, sequence-gap, replay, audit, readiness, or
diagnostic decision uses them.

Allowed class labels in queue-pressure metrics:

- `truth_critical`
- `stale_tolerant`
- `mixed`
- `unknown`
- `test_fixture_only`
- `publisher_or_factory`

Required current mappings:

| Consumer id | Class | Metric rule |
| --- | --- | --- |
| `parser_runner_main_loop` | `truth_critical` | Metrics may report pressure but must not authorize dropping, sampling, coalescing, stale substitution, or worker-queue downgrade. |
| `local_app_live_capture_supervisor` | `mixed` | Metrics may report pressure for the whole consumer, but must not treat the whole loop as stale-tolerant. Any status-only split requires a later contract or implementation authorization. |
| `mtga_event_stream_start` | `publisher_or_factory` | Metrics may identify stream publishing/factory context, but this is not a delivery consumer downgrade target. |
| EventBus tests | `test_fixture_only` | Metrics may be asserted in tests, but test fixtures must not be counted as runtime pressure evidence. |
| future runtime subscriber | `unknown` | Metrics must fail closed or treat the subscriber as `truth_critical` until classification is updated. |

Metric snapshots must not create a new classification. They may only copy a
classification from the current contract/inventory or report
`classification_required`.

Metric pressure on a `truth_critical`, `mixed`, or `unknown` consumer is a
diagnostic signal only. It does not authorize lossy delivery, stale substitution,
fanout restructuring, worker queues, replay recovery, capacity tuning, or
readiness claims.

## Public Interface Boundary

A later implementation may add one EventBus-owned in-memory snapshot interface.
The exact name is left to Codex C, but the intended shape is:

```text
EventBus.queue_pressure_snapshot() -> EventBusQueuePressureSnapshot
```

or an equivalent plain dictionary/dataclass return value.

Interface constraints:

- must be read-only from the caller's perspective;
- must not return internal queue objects;
- must not return raw `GameEvent` objects;
- must not return event payloads;
- must not return raw bytes or hashes from event metadata;
- must not return local paths, process command lines, thread names, task names,
  or subscriber labels supplied by downstream callers;
- must use EventBus-generated public-safe subscriber ids if per-subscriber
  summaries are exposed;
- must be usable in unit tests without live MTGA, private logs, runtime status
  files, or external services.

This contract does not authorize:

- a local API endpoint;
- a runtime status file schema change;
- a diagnostic report schema change;
- a workbook/webhook/App Script field;
- a frontend view;
- a CI gate.

Those surfaces require separate contracts if later needed.

## Metric Vocabulary

Allowed metric fields for an in-memory snapshot:

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | string | Static snapshot schema label, e.g. `event_bus_queue_pressure_metrics.v1`. |
| `metrics_status` | string | One of the allowed status values below. |
| `subscriber_count` | integer | Number of current subscriber queues. |
| `queue_capacity` | integer | Configured per-subscriber queue capacity. |
| `total_publish_calls` | integer | Count of publish calls accepted by the bus before close. |
| `publish_wait_count` | integer | Count of publish calls that observed at least one full subscriber queue and waited. |
| `current_total_queue_depth` | integer | Sum of current queue sizes across subscribers. |
| `max_total_queue_depth` | integer | Max observed total queue depth since metrics reset. |
| `current_max_subscriber_depth` | integer | Current largest queue depth among subscribers. |
| `max_subscriber_depth` | integer | Largest observed single-subscriber depth since metrics reset. |
| `subscriber_pressure` | list | Public-safe per-subscriber aggregate summaries. |
| `consumer_classification_source` | string | Static reference to the classification source, expected `event_bus_consumer_delivery_classification.v1`. |
| `classification_status` | string | Whether all runtime subscribers were mapped to allowed #471 classes. |
| `event_rate_summary` | object | Aggregate event rate summary from process-local monotonic time. |
| `publish_wait_summary` | object | Aggregate wait count and duration summary. |
| `non_claims` | list[string] | Required non-claim labels. |

Allowed per-subscriber fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `subscriber_ref` | string | EventBus-generated symbolic id, such as `subscriber_1`. |
| `consumer_id` | string | Public-safe consumer id from the #471 contract, or `unknown_subscriber`. |
| `consumer_class` | string | One of the allowed #471 class labels. |
| `classification_status` | string | `classified`, `classification_required`, or `test_fixture_only`. |
| `current_queue_depth` | integer | Current queue size. |
| `max_queue_depth` | integer | Max observed queue size for that subscriber. |
| `queue_capacity` | integer | Queue capacity for that subscriber. |
| `pressure_status` | string | Status vocabulary value. |
| `publish_wait_count` | integer | Count of publishes that waited on this subscriber. |

Allowed wait summary fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `wait_observed` | boolean | Whether any publish wait occurred. |
| `publish_wait_count` | integer | Count of publish calls that waited. |
| `total_wait_seconds` | float | Process-local monotonic duration; in-memory only unless a later public artifact buckets it. |
| `max_wait_seconds` | float | Process-local monotonic duration; in-memory only unless a later public artifact buckets it. |
| `wait_bucket` | string | Public-safe bucket for reporting outside memory. |

Allowed event rate fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `window_publish_calls` | integer | Publish calls observed in the current metrics window. |
| `window_elapsed_seconds` | float | Monotonic elapsed seconds, not wall-clock time. |
| `events_per_second_bucket` | string | Public-safe event-rate bucket. |

## Status Vocabulary

Allowed `metrics_status` values:

- `metrics_not_implemented`
- `metrics_disabled`
- `metrics_available_in_memory`
- `metrics_unavailable_closed_bus`
- `metrics_reset`
- `metrics_review_required`

Allowed `pressure_status` values:

- `pressure_ok`
- `pressure_observed`
- `pressure_near_capacity`
- `pressure_waiting`
- `pressure_closed`
- `pressure_unknown`
- `pressure_review_required`

Allowed `classification_status` values:

- `classified`
- `classification_required`
- `classification_unknown_fail_closed`
- `test_fixture_only`
- `publisher_or_factory`
- `classification_review_required`

Allowed `consumer_class` values are inherited from #471:

- `truth_critical`
- `stale_tolerant`
- `mixed`
- `unknown`
- `test_fixture_only`
- `publisher_or_factory`

Allowed `wait_bucket` values:

- `wait_none`
- `wait_observed_short`
- `wait_observed_moderate`
- `wait_observed_long`
- `wait_unknown`

Allowed `events_per_second_bucket` values:

- `rate_not_observed`
- `rate_low`
- `rate_moderate`
- `rate_high`
- `rate_burst`
- `rate_unknown`

Exact thresholds for bucket assignment are implementation details and must be
tested deterministically. Thresholds must not be used to claim readiness or
production reliability.

## Allowed Inputs

Allowed inputs for a later implementation:

- EventBus-owned queue size/capacity metadata;
- EventBus-owned subscriber list length;
- EventBus-generated subscriber ids;
- public-safe consumer ids from the #471 contract;
- public-safe consumer class labels from the #471 contract;
- monotonic process-local timestamps;
- publish/close lifecycle state already owned by EventBus.

This contract does not need event-kind bucketing. Queue pressure should be
measured from queue mechanics, consumer class, and process-local counters, not
from event payload or gameplay semantics.

## Forbidden Inputs And Fields

Forbidden:

- raw event payloads;
- event payload keys or values;
- event kind buckets or event class labels in public metrics;
- raw bytes;
- raw byte hashes;
- raw `Player.log` or `UTC_Log` contents;
- app-data contents;
- live MTGA state;
- private decklists;
- workbook exports;
- webhook payloads;
- Apps Script state;
- local paths;
- process command lines;
- raw task names;
- source file contents;
- raw diffs or patches;
- generated local artifact contents;
- secrets, credentials, tokens, keys, API keys, or webhook URLs;
- provider outputs;
- OpenAI/model-provider outputs.

Unknown or unsafe fields must fail closed in any future public-safe serializer
or test helper. Unsafe values must not be echoed in failure output.

## Public-Safe And No-Echo Boundary

In-memory metrics may hold exact monotonic counters and durations because they
are process-local and do not expose raw payloads by themselves.

Any public-safe report, handoff, test fixture, or future diagnostic surface
must:

- use symbolic subscriber refs;
- use only #471 public-safe consumer ids and class labels;
- use bucketed wait and rate labels instead of exact timing when persisted or
  copied outside the process;
- avoid wall-clock timestamps unless a later contract authorizes them;
- include non-claims;
- omit raw payloads and local/private values;
- use generic failure categories instead of echoing unsafe input.

Required non-claim labels:

- `not_runtime_reliability_readiness`
- `not_release_readiness`
- `not_deploy_readiness`
- `not_production_readiness`
- `not_parser_truth`
- `not_delivery_policy_authorization`
- `not_consumer_classification_change`
- `not_workbook_truth`
- `not_webhook_truth`
- `not_api_contract`
- `not_ci_gate`
- `not_security_assurance`
- `not_privacy_assurance`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`

## Invariants

- Metrics must not change EventBus delivery order.
- Metrics must not change EventBus backpressure behavior.
- Metrics must not mutate parser events.
- Metrics must not keep references to raw `GameEvent` objects beyond the
  existing delivery path.
- Metrics must not expose payloads, raw bytes, hashes, private paths, secrets,
  or local artifacts.
- Metrics are observational and advisory only.
- Metrics are not readiness evidence by themselves.
- Metrics are not source truth for parser facts.
- Metrics are not authorization to change #471 consumer delivery class.
- Metrics are not authorization to change EventBus capacity, fanout, worker
  queues, sequence envelopes, or replay/audit behavior.

## Error Behavior

Malformed metrics state:

- return `metrics_review_required` or fail closed in tests;
- do not infer missing values;
- do not echo unsafe values.

Closed bus:

- snapshot may report `metrics_unavailable_closed_bus` or the last in-memory
  counters, if Codex C documents that choice in tests;
- closed-bus metrics must not imply all queued events were processed.

Reset behavior:

- if a reset method is added, it must reset only EventBus-owned metrics;
- reset must not clear subscriber queues;
- reset must not change publish/close behavior.

## Side Effects

Allowed future side effects:

- updating in-memory counters on EventBus-owned objects;
- reading in-memory counters through a snapshot method;
- focused tests.

Forbidden side effects:

- creating runtime artifacts;
- writing files;
- adding local API payload fields;
- changing frontend diagnostics;
- posting webhooks;
- updating workbook rows;
- changing Apps Script;
- reading private logs;
- changing parser event classes;
- changing parser facts;
- changing EventBus delivery semantics from #460;
- changing EventBus consumer classifications from #471;
- changing CI;
- creating release/deploy/production readiness gates.

## Relationship To Future Reliability Issues

Metrics from this contract may be used as diagnostic evidence for later
contracted work, but they do not authorize that work.

Issue #468, capacity configuration and default tuning:

- metrics may identify pressure categories that justify investigation;
- metrics do not authorize changing default capacity or adding configuration;
- any capacity change must have its own contract and tests.

Issue #469, concurrent fanout:

- metrics may identify a slow-subscriber pressure pattern;
- metrics do not authorize changing fanout order, concurrency, cancellation, or
  shutdown behavior;
- any fanout change must preserve per-subscriber order and completeness.

Issue #470, worker queues:

- metrics may identify expensive consumer work as a candidate for separation;
- metrics do not authorize worker queues, durable retry queues, runtime
  artifacts, local API changes, SQLite writes, or frontend behavior changes;
- `truth_critical` and `mixed` consumers must keep their #471 delivery
  requirements unless a later contract changes them.

Issue #472, sequence IDs and gap detection:

- metrics may motivate sequence/gap work;
- metrics do not authorize event envelopes, parser event metadata changes, or
  runtime diagnostic shape changes.

Issue #473, post-session Player.log and UTC_Log replay audit:

- metrics may mark a session as needing review;
- metrics do not authorize reading private logs, replay execution, fixture
  promotion, recovery claims, or corpus status changes.

## Dependency Order For Later Implementation

1. Add focused tests for the snapshot interface with synthetic events only.
2. Add EventBus-owned in-memory counters without changing delivery semantics.
3. Bind subscriber summaries to #471 public-safe consumer class vocabulary.
4. Add public-safe serializer/snapshot vocabulary if needed by tests.
5. Prove full-queue backpressure behavior from #460 still passes.
6. Prove no raw payload, event kind, path, secret, or local artifact appears in
   metrics.
7. Stop before any runtime artifact, API, UI, workbook, webhook, or CI surface.

## Compatibility

Must remain compatible:

- `EventBus(capacity=...)`
- `EventBus.with_default_capacity()`
- `EventBus.subscribe()`
- `await EventBus.publish(event)`
- `await EventBus.close()`
- `await Subscriber.recv()`
- `None` as the subscriber close signal
- all current `GameEvent` classes
- existing #460 backpressure tests
- existing #471 consumer classification contract and class vocabulary

Adding a snapshot interface must be additive only.

## Tests Required For Later Codex C

Focused tests should prove:

- metrics start at zero/empty for a new bus;
- publishing increments `total_publish_calls`;
- queue depth updates after publish and after `recv()`;
- max depth records the observed high-water mark;
- full-queue backpressure increments `publish_wait_count`;
- per-subscriber pressure summaries use symbolic refs only;
- per-subscriber pressure summaries use #471 consumer ids and class labels only;
- unknown runtime consumers report `classification_required` or fail closed;
- metrics do not include raw event payloads;
- metrics do not include event-kind buckets or event class labels in public
  output;
- metrics do not include local paths, raw bytes, hashes, secrets, or tokens;
- metrics reset, if implemented, does not clear queues or change delivery;
- existing #460 EventBus behavior tests still pass.
- #471 `truth_critical`, `mixed`, and `unknown` classification rules are not
  weakened by metric output.

Suggested validation commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus_queue_pressure_metrics.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_stream_unit.py tests/test_events.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m ruff check src/mythic_edge_parser/event_bus.py tests/test_event_bus.py tests/test_event_bus_queue_pressure_metrics.py
git diff --check
```

If Codex C touches diagnostics, status API, runtime surfaces, local app, or any
durable output surface, stop and route back to Codex B before implementation.

## Acceptance Criteria

- Contract-defined metrics are in-memory and public-safe.
- Metrics are aggregate counters, depths, rates, durations, buckets, and
  symbolic subscriber/classification summaries only.
- Metrics do not alter #460 EventBus backpressure behavior.
- Metrics do not alter #471 consumer classification or downgrade rules.
- No raw event payloads, raw bytes, hashes, logs, private paths, secrets,
  event-kind buckets, local artifacts, workbook exports, provider outputs, or
  model outputs are exposed.
- No runtime artifact, API payload, workbook/webhook/App Script, frontend, or
  CI change is introduced.
- Validation proves both metric behavior and protected-boundary preservation.

## Stop Conditions

Stop immediately if implementation requires:

- changing EventBus delivery semantics;
- changing EventBus consumer classification or downgrade rules;
- using metrics as delivery-policy authorization;
- changing EventBus capacity, fanout, worker queues, sequence/gap behavior, or
  replay/audit behavior;
- changing parser event classes;
- changing parser behavior outside metrics counters;
- runtime status file changes;
- diagnostics report schema changes;
- local API payload changes;
- frontend diagnostics changes;
- workbook/webhook/App Script changes;
- CI changes;
- raw log reads;
- private/local artifact reads;
- live MTGA data;
- exact wall-clock session timeline reporting;
- source-repo or production readiness claims;
- reliability readiness claims;
- parser truth, analytics truth, AI truth, or coaching truth claims.

## Next Workflow Action

Next recommended role: Codex E for contract review.

After Codex E review, Codex C may implement in-memory queue pressure metrics
only if implementation is separately authorized. Codex C must not collect live
metrics, create runtime artifacts, change EventBus delivery semantics, change
#471 consumer classifications, or expose metrics through API/workbook/webhook/UI
surfaces.

Pasteable Codex E prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for EventBus queue pressure metrics.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/467

Prerequisite:
https://github.com/Tahjali11/Mythic-Edge/issues/460
https://github.com/Tahjali11/Mythic-Edge/issues/471

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/event_bus_queue_pressure_metrics.md

Goal:
Review the contract for privacy-safe EventBus queue pressure metrics. Confirm
that metrics remain diagnostic-only, public-safe, tied to #471 consumer classes,
and non-authoritative before any capacity, fanout, worker-queue, sequence/gap,
replay/audit, runtime artifact, API, UI, workbook, webhook, CI, readiness, or
parser-truth work proceeds.

Protected boundaries:
Do not implement code, open a PR, collect live metrics, write runtime artifacts,
change EventBus behavior, change #471 consumer classification, change parser
behavior, change parser event classes, change workbook/webhook/API payloads,
change CI, read raw logs/private paths/secrets/local artifacts, or claim
reliability/readiness/parser truth.

Expected output:
Findings first, validation reviewed, remaining risks, recommended next role, and
workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/467"
  prerequisite_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/460"
  prerequisite_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/654"
  prerequisite_issue_2: "https://github.com/Tahjali11/Mythic-Edge/issues/471"
  prerequisite_pr_2: "https://github.com/Tahjali11/Mythic-Edge/pull/655"
  related_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/468"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/469"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/470"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/472"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/473"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  verdict: "event_bus_queue_pressure_metrics_contract_ready_for_review"
  target_artifact: "docs/contracts/event_bus_queue_pressure_metrics.md"
  prerequisite_merge_commit: "b6b865a34e52dcb1c7fb57cb8937a37d4107febb"
  prerequisite_merge_commit_2: "09857723c38b4424d585659c8aa21f123af50519"
  risk_tier: "High"
  base_branch: "origin/main"
  latest_verified_origin_main: "09857723c38b4424d585659c8aa21f123af50519"
  implementation_authorized: false
  pr_authorized: false
  eventbus_behavior_change_authorized: false
  consumer_classification_change_authorized: false
  metrics_collection_authorized: false
  capacity_change_authorized: false
  fanout_change_authorized: false
  worker_queue_change_authorized: false
  sequence_gap_behavior_authorized: false
  replay_audit_behavior_authorized: false
  parser_behavior_change_authorized: false
  parser_event_class_change_authorized: false
  runtime_artifact_creation_authorized: false
  api_payload_change_authorized: false
  workbook_webhook_change_authorized: false
  ci_change_authorized: false
  live_metric_collection_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
```
