# EventBus Consumer Delivery Classification Contract

## Module

EventBus consumer delivery classification for:

- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`

Plain English: before Mythic Edge changes EventBus delivery behavior, adds
queue-pressure metrics, or moves subscriber work into worker queues, it must
know which consumers must receive every parser event and which consumers may
receive stale, coalesced, summary, or degraded status. This contract records
that classification boundary.

This Codex B pass writes only this contract. It does not implement code, open a
PR, change EventBus behavior, collect metrics, move work to queues, change
parser facts, change parser event classes, change webhook/workbook/API payloads,
change CI, or claim reliability readiness.

## Source Context

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/471>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Prerequisite issue: <https://github.com/Tahjali11/Mythic-Edge/issues/460>
- Related open issue: <https://github.com/Tahjali11/Mythic-Edge/issues/467>
- Related open issue: <https://github.com/Tahjali11/Mythic-Edge/issues/470>
- Target artifact:
  `docs/contracts/event_bus_consumer_delivery_classification.md`
- Latest verified `origin/main`:
  `b6b865a34e52dcb1c7fb57cb8937a37d4107febb`
- Risk tier: High

Codex A findings preserved by this contract:

- #460 is complete and merged at
  `b6b865a34e52dcb1c7fb57cb8937a37d4107febb`.
- #467 and #470 remain open.
- Current runtime subscriber sites include `runner.py` and
  `live_capture_control.py`.
- `runner.py` appears truth-critical.
- `live_capture_control.py` appears mixed and needs explicit classification.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- issue #471
- issue #467
- issue #470
- issue #460
- PR #654 merge state
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/implementation_handoffs/event_bus_completeness_over_liveness_backpressure_comparison.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/live_app_explicit_start_capture_control.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- EventBus, stream, runner, and live-app tests as reference surfaces only

## Owning Layer

Primary internal project area: Parser.

Adjacent internal project area: Local app / live mode.

Truth owner: parser and state interpretation.

`event_bus.py` owns in-memory parser event fanout semantics. `stream.py` owns
the live tailer/router-to-EventBus bridge. `runner.py` owns the broad parser
runtime consumer path. `live_capture_control.py` owns an app-local capture
supervisor that consumes parser events and writes downstream local capture state
and local SQLite facts.

This contract does not move truth ownership to EventBus queues, queue metrics,
worker queues, runtime status files, local app state, SQLite rows, workbook
formulas, webhook transport, Apps Script, analytics, AI, or coaching output.

## Bridge-Code Status

`shared_support_with_bridge_consumers`

The EventBus is parser-owned shared support. Its current runtime consumers cross
two surfaces:

- parser runtime output through `runner.py`;
- local app capture orchestration through `live_capture_control.py`.

That bridge status is why consumer classification must precede future stale
delivery, queue metrics, or worker-queue changes.

## Current Behavior

`MtgaEventStream.start(log_path)` creates an `EventBus`, subscribes one
`Subscriber[GameEvent]`, starts the stream pipeline, and returns both the stream
and the subscriber.

Current runtime consumers:

- `runner.py` calls `MtgaEventStream.start(LOG_PATH)` and then awaits
  `subscriber.recv()` inside the main parser runtime loop.
- `live_capture_control.py` calls `MtgaEventStream.start(player_log_path)` and
  then awaits `subscriber.recv()` with a timeout inside the local app capture
  supervisor loop.

Current EventBus behavior after #460:

- `EventBus.publish()` waits for subscriber queue capacity instead of silently
  dropping the oldest queued event.
- A full queue does not remove the subscriber as dead.
- Close wakes blocked publishers and lets subscribers drain accepted queued
  events before returning `None`.

## Problem Statement And First Bad Values

Issue #460 fixed the first EventBus loss mode, but Mythic Edge still lacks a
consumer classification contract. Without that contract, later #467 or #470
work could accidentally treat parser-truth consumers like UI/status consumers.

First bad value:

```text
runtime EventBus subscriber
  -> unclassified delivery requirement
  -> future stale/coalesced/drop policy can be applied without truth boundary
```

Why it is bad: the parser runtime must preserve event completeness for accepted
parser events. A stale or coalesced delivery path would silently weaken parser
evidence unless the consumer has been classified and scoped.

Second bad value:

```text
live_capture_control.py
  -> one loop mixes parser event receipt, local status heartbeat, and SQLite live writes
  -> consumer can be mislabeled as either purely truth-critical or purely stale-tolerant
```

Why it is bad: the event receipt and completed-fact write path is
truth-sensitive, while progress heartbeats and waiting status can be
stale-tolerant display/control state. Future changes must split those surfaces
before applying any downgrade.

Third bad value:

```text
new subscriber site
  -> no inventory entry
  -> delivery class defaults by implementation convenience
```

Why it is bad: new EventBus consumers must not choose their own degradation
rules by local convenience. Unknown consumers must fail closed.

## Scope Decision

In scope for this contract:

- classify current runtime EventBus consumers;
- define classification vocabulary;
- define allowed and forbidden degradation behavior by class;
- define downgrade and fail-closed rules;
- define how #467 metrics and #470 worker-queue work must consume this contract;
- define validation expectations for a later implementation.

Out of scope for this contract:

- code changes;
- EventBus behavior changes;
- queue-pressure metric collection;
- worker-queue implementation;
- source `Player.log` parsing changes;
- parser event class changes;
- parser state final reconciliation changes;
- match identity, game identity, or deduplication changes;
- workbook schema changes;
- webhook payload shape changes;
- Apps Script behavior changes;
- local API/frontend behavior changes;
- runtime artifact creation;
- CI changes;
- reliability-readiness, parser-truth, release-readiness, deploy-readiness,
  production-readiness, analytics-truth, AI-truth, or coaching-truth claims.

## Classification Vocabulary

### `truth_critical`

A consumer that must receive every accepted parser event in original order.

Rules:

- delivery must remain complete for accepted events;
- per-subscriber ordering must remain first-in, first-out;
- backpressure is allowed when needed to preserve completeness;
- explicit stream close may end delivery;
- event loss, event coalescing, event sampling, stale substitutes, and summary
  substitution are forbidden;
- queue-pressure metrics may observe public-safe counts but must not weaken
  delivery.

### `stale_tolerant`

A consumer whose output is status, progress, display, or diagnostic context and
does not own parser facts.

Rules:

- status may be throttled, coalesced, summarized, or marked stale when the
  consumer contract allows it;
- degraded output must carry explicit status such as `stale`, `degraded`,
  `coalesced`, or `summary_only`;
- stale-tolerant output must not become parser truth or analytics truth;
- raw event payloads, raw logs, private paths, secrets, and source snippets must
  not be echoed.

No current runtime EventBus subscriber is classified as wholly
`stale_tolerant` by this contract.

### `mixed`

A consumer that contains both truth-critical event handling and stale-tolerant
status/control sub-surfaces.

Rules:

- truth-critical sub-surfaces keep `truth_critical` delivery rules;
- stale-tolerant sub-surfaces may degrade only after they are explicitly split,
  named, and validated;
- mixed consumers must not be downgraded as a whole;
- mixed consumers must not hide event delivery loss behind status vocabulary.

### `unknown`

A consumer that has not been classified.

Rules:

- default treatment is fail-closed;
- no stale/coalesced/drop policy may be applied;
- future implementation must either block the behavior change or require a new
  contract/update before proceeding;
- if runtime behavior must continue while classification is missing, the
  consumer must be treated as `truth_critical`.

### `test_fixture_only`

A fake or synthetic subscriber used only in tests.

Rules:

- may support focused test behavior;
- must not be used to justify runtime consumer downgrade;
- must not be counted as a runtime consumer in production inventory.

### `publisher_or_factory`

A module that creates or publishes through the EventBus but is not itself a
runtime consumer of subscriber delivery.

Rules:

- may be part of validation inventory;
- does not receive a delivery downgrade policy;
- must preserve the delivery contract required by downstream consumers.

## Consumer Inventory

| Consumer id | Runtime site | Classification | Current role | Delivery requirement |
| --- | --- | --- | --- | --- |
| `parser_runner_main_loop` | `src/mythic_edge_parser/app/runner.py` | `truth_critical` | Broad parser runtime consumes `subscriber.recv()` output and updates parser state, diagnostics, local JSONL, sheet/webhook-facing row paths, and analytics sidecar input. | Must receive every accepted event in order. No stale, sampled, coalesced, or summary substitute delivery is allowed. |
| `local_app_live_capture_supervisor` | `src/mythic_edge_parser/local_app/live_capture_control.py` | `mixed` | Local app explicit capture loop consumes parser events, updates parser match summary state, writes completed parser-owned facts to local SQLite, and writes local capture status/progress. | Event receipt and completed-fact write path are truth-sensitive and must preserve completeness. Heartbeat/progress/status display may be stale-tolerant only after a future split contract or implementation proves that no parser facts are affected. |
| `mtga_event_stream_start` | `src/mythic_edge_parser/stream.py` | `publisher_or_factory` | Creates EventBus, creates subscriber, routes parser events into the bus. | Must preserve delivery semantics required by runtime consumers. Not itself a stale-tolerant consumer. |
| `event_bus_tests` | `tests/test_event_bus.py`, `tests/test_stream_unit.py`, `tests/test_stream_integration.py`, `tests/test_runner.py`, live-app tests using fake subscribers | `test_fixture_only` | Synthetic coverage for EventBus, stream, runner, and local app behavior. | May simulate delivery, close, timeout, or fake event paths but cannot weaken runtime classification. |
| future subscriber sites | any future `bus.subscribe()`, `MtgaEventStream.start(...)` receiver, or `Subscriber.recv()` runtime path | `unknown` until classified | Unknown. | Must fail closed or be treated as `truth_critical` until this inventory is updated. |

## Allowed Delivery Behavior

For `truth_critical` consumers:

- preserve every accepted parser event;
- preserve event order;
- prefer bounded backpressure over loss;
- let explicit close terminate delivery;
- surface errors through existing scoped error handling when the consuming module
  already owns that error handling;
- keep queue-pressure observations public-safe and non-authoritative.

For `stale_tolerant` sub-surfaces:

- coalesce repeated status updates;
- throttle heartbeat or progress writes;
- emit `stale`, `degraded`, `coalesced`, or `summary_only` status;
- omit private details from display payloads;
- show explicit uncertainty instead of inventing parser facts.

For `mixed` consumers:

- apply `truth_critical` behavior to parser event receipt and parser-owned fact
  generation;
- apply stale-tolerant behavior only to named status/display sub-surfaces after
  validation proves separation;
- refuse whole-consumer downgrade.

For `unknown` consumers:

- no downgrade is allowed;
- no event drop, sample, coalescing, or stale substitute is allowed;
- future implementation must stop or classify the consumer first.

## Forbidden Degradation Behavior

The following are forbidden for every EventBus consumer class unless a future
contract explicitly narrows and authorizes the behavior:

- dropping accepted parser events;
- replacing accepted parser events with summaries for parser state consumers;
- sampling events before parser state or completed-fact generation;
- coalescing multiple parser events into one parser-truth event;
- treating queue-pressure metrics as parser truth;
- treating queue-pressure metrics as reliability readiness;
- using stale local app status to infer match identity, game identity, results,
  play/draw, mulligans, card actions, or completed parser facts;
- using worker queues to reorder parser events;
- hiding event loss behind `degraded` without a loss-specific contract;
- exposing raw `Player.log`, raw event payloads, raw local paths, secrets,
  credentials, tokens, webhook URLs, workbook exports, or generated private
  artifacts.

## Downgrade Rules

1. A `truth_critical` consumer may not be downgraded to `stale_tolerant` without
   a new Codex B contract or explicit contract update.
2. A `mixed` consumer may not be downgraded as a whole. The implementation must
   split and name sub-surfaces first.
3. A stale-tolerant sub-surface must not write parser facts, change parser
   state, trigger workbook/webhook/API truth, or serve as analytics truth.
4. An `unknown` consumer must fail closed or run under `truth_critical`
   delivery rules.
5. Metrics from #467 may inform diagnostics but must not reclassify consumers.
6. Worker queues from #470 may change work placement only after proving that
   `truth_critical` ordering and completeness remain intact.
7. Any classification change touching parser confidence, finality, runtime
   status schemas, local API/frontend behavior, or truth ownership must route
   back to Codex B.

## Relationship To Issue #467

Issue #467 may later define EventBus queue-pressure metrics. Those metrics must
consume this classification boundary.

Allowed later metric directions:

- public-safe queue depth category;
- public-safe subscriber class label;
- bounded count or status vocabulary that does not echo event payloads;
- explicit `not_authoritative` or equivalent non-claim flag.

Forbidden metric directions:

- raw event payload capture;
- raw `Player.log` capture;
- private path echo;
- per-card or per-match truth inference from queue state;
- readiness, reliability assurance, parser truth, security assurance, privacy
  assurance, release readiness, deploy readiness, or production behavior claims.

## Relationship To Issue #470

Issue #470 may later define worker queues for heavy subscriber work. That work
must consume this classification boundary.

Allowed later worker-queue directions:

- keep EventBus event receipt complete for `truth_critical` consumers;
- move non-truth work behind queues only when ordering, replay, close, and error
  behavior are explicitly defined;
- split `mixed` consumers before stale-tolerant worker behavior is applied;
- add tests that prove parser event order and completeness are preserved.

Forbidden worker-queue directions:

- reordering parser events for parser state consumers;
- skipping intermediate parser events;
- retrying events in a way that duplicates parser facts;
- turning worker queue state into parser truth;
- adding durable runtime artifacts without a separate contract;
- changing local API/frontend payloads without a separate contract.

## Public-Safe Status And Reason Vocabulary

Future validation or diagnostic artifacts may use these public-safe labels:

- `classified_truth_critical`
- `classified_stale_tolerant`
- `classified_mixed`
- `classified_unknown`
- `classification_required`
- `downgrade_blocked`
- `split_required`
- `metrics_only`
- `worker_queue_requires_order_proof`
- `not_authoritative`

Allowed public-safe reason categories:

- `parser_truth_consumer`
- `local_app_status_subsurface`
- `completed_fact_write_path`
- `display_or_diagnostic_only`
- `unknown_subscriber_site`
- `requires_contract_update`
- `requires_ordering_validation`
- `requires_no_echo_validation`

Reason text must not include raw event payloads, raw log content, private paths,
secrets, credentials, tokens, webhook URLs, workbook exports, or generated
private artifacts.

## Validation Expectations For Later Implementation

A later Codex C implementation, if separately authorized, should provide
deterministic evidence that:

- every runtime `MtgaEventStream.start(...)` receiver is listed in this
  contract or in a machine-readable inventory derived from it;
- every runtime `bus.subscribe()` or `Subscriber.recv()` site is classified;
- `runner.py` remains `truth_critical`;
- `live_capture_control.py` remains `mixed` until its truth-sensitive and
  stale-tolerant sub-surfaces are explicitly split;
- new unclassified subscriber sites fail validation;
- tests prevent silent downgrade of `truth_critical` consumers;
- any future stale-tolerant behavior has focused tests proving it does not feed
  parser state, parser facts, workbook/webhook/API truth, or analytics truth;
- public-safe validation output does not echo raw events, raw logs, private
  paths, secrets, or local-only runtime artifacts.

Recommended focused validation commands for a later implementation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_runner.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
git diff --check
```

If a future implementation adds a dedicated static inventory checker, it should
be run before EventBus, runner, and live-app tests.

## Protected Boundaries

This contract does not authorize:

- code implementation;
- PR creation;
- EventBus behavior changes;
- metric collection;
- worker-queue behavior;
- live metric collection;
- runtime artifact creation;
- parser fact changes;
- parser event class changes;
- parser confidence or finality changes;
- match identity, game identity, or deduplication changes;
- webhook, workbook, Apps Script, local API, or frontend payload changes;
- raw log ingestion beyond existing authorized runtime behavior;
- private data collection;
- CI changes;
- release, deploy, production, reliability-readiness, parser-truth,
  security-assurance, privacy-assurance, analytics-truth, AI-truth, or
  coaching-truth claims.

## Stop Conditions

Stop and route back to Codex B if later work:

- adds a new runtime EventBus subscriber that is not classified;
- attempts to downgrade `runner.py`;
- attempts to treat `live_capture_control.py` as wholly stale-tolerant;
- changes parser truth ownership;
- changes parser confidence or finality semantics;
- changes runtime status schemas;
- changes local API/frontend behavior;
- introduces durable runtime artifacts;
- requires raw log/private data collection;
- needs CI changes;
- claims reliability readiness, parser truth, release readiness, deploy
  readiness, production readiness, security assurance, privacy assurance,
  analytics truth, AI truth, or coaching truth.

## Expected Future Artifact Behavior

If this contract later routes to implementation, the expected artifact is either:

- a public-safe static inventory/check that enforces the classification table;
  or
- a narrow code/test implementation proving the classified consumers preserve
  their required delivery semantics.

The artifact must remain advisory until a separate implementation issue
authorizes behavior changes. Passing validation means only that the classification
inventory is internally consistent. It does not prove parser truth, reliability
readiness, release readiness, deploy readiness, or production behavior.

## Recommended Next Role

Recommended next role: Codex E for contract review.

After Codex E review, Codex C may implement a validation or inventory mechanism
only if that implementation is separately authorized for issue #471.

Pasteable Codex E prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for EventBus consumer delivery classification.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/471

Related issues:
https://github.com/Tahjali11/Mythic-Edge/issues/460
https://github.com/Tahjali11/Mythic-Edge/issues/467
https://github.com/Tahjali11/Mythic-Edge/issues/470

Contract:
docs/contracts/event_bus_consumer_delivery_classification.md

Goal:
Review the contract against issue #471 and the EventBus/stream/runner/live app
consumer surfaces. Confirm whether `runner.py` is correctly classified as
truth-critical, whether `live_capture_control.py` is correctly classified as
mixed, and whether the downgrade rules are strong enough before #467 metrics or
#470 worker-queue work proceeds.

Protected boundaries:
Do not implement code, open a PR, change EventBus behavior, collect metrics,
move subscriber work into queues, change parser facts, change parser event
classes, change webhook/workbook/API payloads, create runtime artifacts, change
CI, or claim reliability/readiness/truth.

Expected output:
Findings first, validation reviewed, remaining risk, recommended next role, and
workflow_handoff block.
```

Future pasteable Codex C prompt, only if separately authorized after review:

```text
Use the Mythic Edge workflow rules.

Act as Codex C: Module Implementer for EventBus consumer delivery classification.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/471

Related issues:
https://github.com/Tahjali11/Mythic-Edge/issues/460
https://github.com/Tahjali11/Mythic-Edge/issues/467
https://github.com/Tahjali11/Mythic-Edge/issues/470

Contract:
docs/contracts/event_bus_consumer_delivery_classification.md

Goal:
Implement the smallest public-safe validation or inventory mechanism needed to
prove runtime EventBus consumers are classified before any delivery behavior,
metrics, or worker-queue changes. Preserve `runner.py` as truth-critical and
`live_capture_control.py` as mixed unless a new Codex B contract changes that
boundary.

Protected boundaries:
Do not change EventBus delivery behavior, collect live metrics, move subscriber
work into worker queues, change parser facts, change parser event classes,
change webhook/workbook/API payloads, create runtime artifacts, change CI, or
claim reliability/readiness/truth.

Expected output:
Implementation handoff, files changed, validation run, remaining risks, and
workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/471"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/460"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/467"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/470"
  completed_thread: "B"
  next_thread: "E"
  verdict: "event_bus_consumer_delivery_classification_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "origin/main"
  latest_verified_origin_main: "b6b865a34e52dcb1c7fb57cb8937a37d4107febb"
  target_artifact: "docs/contracts/event_bus_consumer_delivery_classification.md"
  implementation_authorized: false
  pr_authorized: false
  eventbus_behavior_change_authorized: false
  metrics_collection_authorized: false
  worker_queue_change_authorized: false
  parser_behavior_change_authorized: false
  parser_event_class_change_authorized: false
  runtime_artifact_creation_authorized: false
  api_payload_change_authorized: false
  workbook_webhook_change_authorized: false
  ci_change_authorized: false
  private_data_collection_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
```
