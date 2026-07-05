# EventBus Sequence IDs And Subscriber Gap Detection Contract

Status: contract only
Codex role: B, Module Contract Writer
Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/472
Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
Latest verified `origin/main`: `d56a26062b2683a6e8682996145a56850ed74d16`

## Purpose

This contract defines how Mythic Edge may later add EventBus-owned sequence IDs
and subscriber gap detection without changing parser event classes or claiming
parser truth.

Plain English behavior:

- EventBus should eventually be able to prove that each subscriber saw a
  contiguous sequence of EventBus deliveries.
- A sequence ID is an EventBus delivery counter, not a game fact.
- A gap signal is an in-memory diagnostic signal, not proof of MTGA truth or
  parser truth.
- This pass does not implement sequence IDs, gap detection, replay audit, or
  parser behavior changes.

## Source Context

Prerequisites:

- Issue #460 / PR #654 established completeness-preserving EventBus
  backpressure.
- Issue #471 / PR #655 established EventBus consumer delivery classifications.
- Issue #467 / PR #658 established privacy-safe queue pressure metrics.
- Issue #470 / PR #657 established heavy-subscriber worker-queue planning.
- Issue #468 / PR #659 established EventBus capacity configuration boundaries.
- Issue #469 / PR #660 established the concurrent fanout completeness contract.

Related future issue:

- Issue #473: post-session Player.log and UTC_Log replay audit.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- GitHub issue #472
- GitHub issue #473
- GitHub PR #660
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/contracts/event_bus_consumer_delivery_classification.md`
- `docs/contracts/event_bus_queue_pressure_metrics.md`
- `docs/contracts/event_bus_heavy_subscriber_worker_queues.md`
- `docs/contracts/event_bus_capacity_configuration_and_default_tuning.md`
- `docs/contracts/event_bus_concurrent_fanout_completeness.md`
- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_event_bus.py`
- `tests/test_event_bus_queue_pressure_metrics.py`

No private `Player.log`, `UTC_Log`, app-data, live MTGA data, runtime status
files, local-only artifacts, workbook exports, raw diffs, source patches,
secrets, credentials, tokens, API keys, or webhook URLs were read.

## Owning Layer

Primary internal project area: Parser.

Truth owner: parser and state interpretation.

`event_bus.py` may own in-memory delivery sequence and subscriber continuity
diagnostics for its own queue mechanics. It does not own parser event truth,
MTGA raw log truth, match identity, game identity, final reconciliation,
workbook truth, webhook truth, API truth, analytics truth, AI truth, coaching
truth, or production reliability truth.

## Bridge-Code Status

`shared_support`

The EventBus is parser-owned shared support used by stream/runtime code,
`runner.py`, local app capture control, and tests. Sequence and gap diagnostics
may describe EventBus delivery continuity, but must not become parser event
metadata, parser state truth, a replay engine, or a downstream correction layer
without a later contract.

## Files Owned By This Contract

- `docs/contracts/event_bus_sequence_ids_and_subscriber_gap_detection.md`

Likely files for a later implementation, if separately authorized:

- `src/mythic_edge_parser/event_bus.py`
- focused EventBus tests, likely `tests/test_event_bus.py` or a new dedicated
  `tests/test_event_bus_sequence_gap_detection.py`
- possibly `tests/test_event_bus_queue_pressure_metrics.py` if the in-memory
  snapshot is extended

Referenced but not owned by this contract:

- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- all existing EventBus contracts listed above

## Observed Current Behavior

Current EventBus behavior on `origin/main`:

- `EventBus.publish(event)` delivers a parser event to subscriber queues with
  completeness-preserving backpressure.
- The current implementation still uses a sequential fanout loop; issue #469
  produced a contract for future concurrent fanout but did not implement it.
- `Subscriber.recv()` returns the parser event value or `None` on close.
- `queue_pressure_snapshot()` reports aggregate queue pressure but does not
  report per-delivery sequence continuity.
- Subscriber queues carry raw parser event values or the internal close sentinel.
- There is no EventBus-owned delivery envelope, sequence ID, or subscriber gap
  tracker.

## Problem Statement And First Bad Values

First bad value:

```text
EventBus publish succeeds
  -> subscriber receives next GameEvent
  -> subscriber cannot prove whether an EventBus delivery number was skipped
```

Why it is bad: #460 and #469 are designed to avoid loss, but current subscribers
have no independent in-memory continuity signal if a future bug, cancellation
path, or worker-queue design creates a discontinuity.

Second bad value:

```text
subscriber starts after earlier publishes
  -> first observed event has no baseline sequence
  -> late join can be mistaken for a gap
```

Why it is bad: gap detection must distinguish real discontinuity from a
subscriber that legitimately started after earlier EventBus publishes.

Third bad value:

```text
gap concern
  -> raw Player.log or UTC_Log replay
```

Why it is bad: #473 replay audit should wait. EventBus sequence/gap diagnostics
must be in-memory and public-safe before any replay or private log workflow is
considered.

Fourth bad value:

```text
sequence_id
  -> parser event metadata or workbook/webhook/API payload field
```

Why it is bad: sequence IDs are EventBus delivery diagnostics. They must not
change parser event classes, parser facts, workbook schema, webhook payloads, or
API payloads unless a later contract explicitly authorizes those surfaces.

## Scope Decision

In scope for a later Codex C implementation only if separately authorized:

- EventBus-owned monotonic delivery sequence counter;
- EventBus-owned internal delivery envelope or equivalent internal metadata;
- subscriber-owned expected-next-sequence tracking;
- in-memory gap, duplicate, and out-of-order detection;
- public-safe in-memory continuity snapshot vocabulary;
- focused tests for contiguous delivery and simulated gaps.

Out of scope:

- implementing code in this Codex B pass;
- changing parser event classes;
- changing `GameEvent` payloads or parser event metadata;
- changing `Subscriber.recv()` return type unless a later contract explicitly
  authorizes that interface change;
- changing EventBus capacity;
- changing EventBus fanout;
- collecting live metrics;
- writing runtime artifacts;
- adding worker queues;
- changing parser facts, parser state final reconciliation, match identity, game
  identity, or deduplication;
- changing stream, runner, local app, API, workbook, webhook, Apps Script, or CI
  behavior;
- running replay audit;
- reading raw logs or private app-data;
- claiming reliability readiness, parser truth, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching truth.

## Design Decision

Preferred future boundary:

```text
EventBus-owned internal delivery envelope
  -> subscriber queue
  -> Subscriber.recv() unwraps parser event
  -> subscriber-owned in-memory gap tracker updates diagnostics
```

This is preferred because it gives EventBus an internal continuity surface while
preserving parser event classes and the existing `Subscriber.recv()` public
return behavior.

Rejected by default:

- parser event metadata sequence fields;
- workbook/webhook/API payload sequence fields;
- raw-log offset sequence fields;
- durable runtime sequence ledgers;
- global process-wide or cross-session sequence IDs.

If a later implementation cannot meet the contract without changing parser event
classes, `Subscriber.recv()` return type, API payloads, workbook/webhook
payloads, or durable artifact shape, stop and route back to Codex B.

## Public Interface Boundary

Existing public interfaces must remain compatible unless a later contract
explicitly authorizes an interface change:

- `EventBus(capacity=...)`
- `EventBus.with_default_capacity()`
- `EventBus.subscribe(consumer_id=...)`
- `await EventBus.publish(event)`
- `await EventBus.close()`
- `await Subscriber.recv() -> GameEvent | None`
- `EventBus.queue_pressure_snapshot()`
- `EventBus.reset_queue_pressure_metrics()`

Allowed future in-memory diagnostic interface shapes:

- `EventBus.delivery_continuity_snapshot() -> EventBusDeliveryContinuitySnapshot`
- `Subscriber.delivery_continuity_snapshot() -> SubscriberDeliveryContinuitySnapshot`
- an equivalent EventBus-owned read-only dataclass or dictionary shape

Any future snapshot must be:

- read-only from the caller perspective;
- in-memory only;
- public-safe;
- symbolic for subscriber references;
- free of raw parser event payloads;
- explicit that it is not parser truth or readiness evidence.

This contract does not authorize:

- local API endpoint fields;
- runtime status file fields;
- workbook or webhook fields;
- Apps Script changes;
- frontend diagnostics;
- CI gates.

## Sequence And Gap Vocabulary

| Term | Meaning |
| --- | --- |
| `delivery_sequence_id` | EventBus-owned monotonic integer assigned to a publish delivery record in one EventBus instance. |
| `delivery_envelope` | Internal EventBus wrapper that pairs a parser event with delivery metadata. |
| `sequence_origin` | The first sequence value generated by a new EventBus instance. |
| `publish_sequence_counter` | EventBus-owned in-memory counter used to assign `delivery_sequence_id`. |
| `subscriber_sequence_baseline` | First sequence observed by a subscriber after subscription or reset. |
| `expected_next_sequence_id` | The next sequence a subscriber expects after its latest accepted delivery. |
| `gap_detected` | Subscriber observed a sequence greater than expected. |
| `duplicate_detected` | Subscriber observed a sequence already seen. |
| `out_of_order_detected` | Subscriber observed a sequence lower than expected but not accepted as normal duplicate handling. |
| `continuity_snapshot` | Public-safe in-memory diagnostic view of subscriber continuity state. |

Allowed continuity statuses:

- `sequence_not_implemented`
- `sequence_available_in_memory`
- `baseline_pending`
- `baseline_established`
- `contiguous`
- `gap_detected`
- `duplicate_detected`
- `out_of_order_detected`
- `closed`
- `unknown_fail_closed`
- `review_required`

Allowed reason categories:

- `normal_contiguous_delivery`
- `subscriber_joined_after_publish`
- `missing_sequence`
- `duplicate_sequence`
- `out_of_order_sequence`
- `closed_bus_path`
- `external_cancellation`
- `test_gap_injection`
- `unsupported_interface_change`
- `protected_surface_blocked`

Required non-claim labels:

- `not_parser_truth`
- `not_runtime_reliability_readiness`
- `not_release_readiness`
- `not_deploy_readiness`
- `not_production_readiness`
- `not_replay_audit_authorization`
- `not_private_log_read_authorization`
- `not_parser_event_class_change`
- `not_workbook_truth`
- `not_webhook_truth`
- `not_api_contract`
- `not_ci_gate`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`

Forbidden labels:

- `delivery_loss_proven_absent`
- `parser_truth_confirmed`
- `reliability_ready`
- `production_safe`
- `replay_authorized`
- `raw_log_verified`

## Internal Envelope Expectations

A future internal delivery envelope should contain only EventBus-owned metadata:

- `delivery_sequence_id`;
- public-safe `schema_version`;
- parser event object reference for in-memory delivery only;
- optional public-safe fanout status;
- optional public-safe non-claim labels.

The envelope must not:

- mutate the parser event;
- copy parser event payloads into public output;
- add fields to parser event dataclasses;
- add workbook, webhook, API, or Apps Script fields;
- persist to disk;
- include raw log offsets, local paths, wall-clock timestamps, secrets, or private
  values.

`Subscriber.recv()` should keep returning the parser event value or `None` unless
a later contract authorizes an interface change. If an internal envelope reaches
external callers, that is a contract failure.

## Gap Detection Rules

Baseline:

- A subscriber with no prior sequence starts in `baseline_pending`.
- The first delivered sequence establishes `subscriber_sequence_baseline`.
- A subscriber that joins after earlier publishes must not report a gap for the
  missed pre-subscription sequences.

Contiguous delivery:

- After baseline, a subscriber expects the next sequence to be previous sequence
  plus one.
- Receiving the expected next sequence yields `contiguous`.

Gap:

- Receiving a sequence greater than expected yields `gap_detected` with reason
  `missing_sequence`.
- Gap detection must identify the expected and observed sequence values in
  in-memory tests, but public artifacts should use symbolic or synthetic values
  only.

Duplicate and out-of-order:

- Receiving a sequence already seen yields `duplicate_detected` or
  `out_of_order_detected`.
- Duplicate/out-of-order diagnostics must not auto-replay, skip, synthesize, or
  rewrite parser events.

Close and cancellation:

- Close may move a subscriber to `closed`.
- Close must not turn missing post-close deliveries into parser truth claims.
- External cancellation must not be reported as normal contiguous delivery.
- If cancellation semantics require a runtime degradation policy, stop and route
  back to Codex B.

## Relationship To #460 Completeness

#460 backpressure remains the primary delivery invariant:

- full queues apply backpressure;
- accepted queued events are not silently dropped;
- close must avoid deadlock;
- per-subscriber order remains stable.

Sequence/gap detection observes continuity. It does not replace #460
completeness behavior and does not authorize lossy delivery.

## Relationship To #471 Consumer Classification

Sequence/gap diagnostics must consume #471 classifications:

- `truth_critical` consumers must treat gaps as review-required diagnostics;
- `mixed` consumers must preserve truth-sensitive event receipt rules;
- `unknown` consumers fail closed or are treated as `truth_critical`;
- `test_fixture_only` consumers may simulate gaps in tests but cannot weaken
  runtime requirements.

Sequence/gap diagnostics must not reclassify consumers or authorize stale,
coalesced, sampled, or summary substitute delivery.

## Relationship To #467 Metrics

Sequence/gap diagnostics may be adjacent to queue pressure metrics, but they are
not queue pressure metrics.

Allowed relationship:

- continuity snapshots may share public-safe `subscriber_ref` vocabulary;
- continuity snapshots may include non-claims matching #467;
- tests may assert that queue pressure metrics still avoid raw payloads.

Forbidden relationship:

- queue pressure metrics must not become parser truth;
- sequence IDs must not be added to public metrics unless this contract or a later
  implementation explicitly keeps them public-safe and in-memory;
- gap detection must not trigger live metrics collection or runtime artifact
  creation.

## Relationship To #468 Capacity

Sequence/gap detection does not authorize capacity changes.

Capacity remains bounded, explicit, and separate from sequence continuity.
Increasing capacity to hide a gap or pressure signal is forbidden.

## Relationship To #469 Fanout

Sequence IDs must be compatible with future concurrent fanout:

- one publish call should assign one `delivery_sequence_id` shared by all selected
  subscriber delivery attempts;
- fanout task completion order must not change sequence order;
- partial delivery must not be reported as normal contiguous delivery;
- fanout cancellation must not leak tasks or hide missing deliveries.

If a later fanout implementation needs a different sequence model, route back to
Codex B before implementation.

## Relationship To #470 Worker Queues

Worker queues remain unauthorized.

If future worker-queue work needs gap detection, it must consume this contract
and still prove:

- parser event receipt stays complete and ordered;
- truth-sensitive work is not moved without order, flush, failure, and gap proof;
- no durable retry queue or runtime artifact is created without a separate
  contract.

## Relationship To #473 Replay Audit

Issue #473 must wait.

This contract may produce future in-memory reason categories that make replay
audit worth considering, such as `gap_detected` or `external_cancellation`.
Those categories are not replay authorization.

This contract forbids:

- reading private `Player.log`;
- reading `UTC_Log`;
- running replay audit;
- promoting fixtures;
- changing corpus status;
- claiming private smoke success;
- claiming parser behavior readiness.

## Allowed Inputs

Allowed future inputs:

- EventBus-owned publish counter;
- EventBus-owned subscriber queues;
- EventBus-generated subscriber refs;
- EventBus-owned closed state;
- #471 public-safe consumer ids and classes;
- synthetic public-safe test events;
- process-local in-memory counters.

Forbidden inputs:

- raw `Player.log`;
- raw `UTC_Log`;
- app-data contents;
- live MTGA state;
- workbook exports;
- webhook payloads;
- Apps Script state;
- raw event payloads in public output;
- raw log offsets;
- local paths;
- runtime artifact files;
- generated private artifacts;
- secrets, credentials, tokens, API keys, or webhook URLs;
- provider or model outputs.

## Outputs

Allowed future outputs:

- in-memory `delivery_sequence_id` values;
- in-memory subscriber expected-next-sequence state;
- in-memory continuity snapshots;
- focused test assertions using synthetic values;
- public-safe handoff reason categories and non-claims.

Forbidden outputs:

- parser event class fields;
- parser event payload changes;
- workbook or webhook fields;
- API payload fields;
- runtime status files;
- durable sequence ledgers;
- replay artifacts;
- raw logs or private paths;
- readiness, truth, assurance, release, deploy, production, analytics, AI, or
  coaching claims.

## Validation Expectations For Later Implementation

A later Codex C implementation, if separately authorized, should provide
deterministic evidence that:

- sequence IDs start from a documented in-memory origin for a new EventBus;
- sequential awaited publishes produce contiguous sequence IDs;
- every active subscriber sees contiguous sequence state under normal delivery;
- a late subscriber establishes a baseline without false gap reporting;
- a synthetic test-only gap produces `gap_detected`;
- synthetic duplicate or out-of-order delivery produces the correct diagnostic;
- gap diagnostics do not mutate parser events;
- `Subscriber.recv()` still returns `GameEvent | None`;
- queue pressure metrics remain public-safe;
- #460 backpressure tests still pass;
- #469 fanout expectations are not weakened;
- #473 replay audit remains unauthorized.

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

If a dedicated sequence/gap test file is added, run it before broader EventBus,
stream, runner, and live-app tests.

## Acceptance Criteria

- Contract defines where sequence data should live.
- Contract preserves parser event classes and parser event payloads.
- Contract defines EventBus-owned sequence and gap vocabulary.
- Contract defines late-subscriber baseline behavior.
- Contract defines gap, duplicate, and out-of-order statuses.
- Contract keeps #473 replay audit blocked.
- Contract preserves #460, #471, #467, #468, #469, and #470 boundaries.
- Contract forbids private log reads, runtime artifacts, payload changes, CI
  changes, parser behavior changes, and readiness/truth claims.
- Contract defines validation evidence required before any later implementation.

## Stop Conditions

Stop and route back to Codex B if later work requires:

- changing parser event classes;
- changing parser event payloads;
- changing `Subscriber.recv()` return type;
- adding API, workbook, webhook, Apps Script, or frontend fields;
- writing runtime artifacts;
- creating durable sequence ledgers;
- reading private logs or live MTGA data;
- running replay audit;
- changing EventBus capacity;
- changing EventBus fanout outside the #469 boundary;
- adding worker queues;
- changing parser facts, final reconciliation, match identity, game identity, or
  deduplication;
- changing CI;
- making reliability readiness, parser truth, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching truth
  claims.

## Recommended Next Role

Recommended next role: Codex E.

Codex E should review this contract against issue #472, issue #473, the completed
EventBus contract chain, and current EventBus code. Codex E should route back to
Codex B if the sequence location, `Subscriber.recv()` compatibility,
late-subscriber baseline rule, or replay-audit boundary is ambiguous.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic-Edge issue #472.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/472

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source artifact:
docs/contracts/event_bus_sequence_ids_and_subscriber_gap_detection.md

Review the EventBus sequence IDs and subscriber gap detection contract against
#460, #471, #467, #468, #469, #470, #473, and current EventBus code.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not implement sequence IDs or gap detection.
- Do not change EventBus behavior, parser behavior, parser event classes,
  API payloads, workbook/webhook payloads, or CI.
- Do not read private logs, run replay audit, collect live metrics, or create
  runtime artifacts.
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
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/469"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/660"
  latest_merge_commit: "d56a26062b2683a6e8682996145a56850ed74d16"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/472"
  next_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/473"
  completed_thread: "B"
  next_thread: "E"
  verdict: "event_bus_sequence_gap_contract_ready_for_review"
  target_artifact: "docs/contracts/event_bus_sequence_ids_and_subscriber_gap_detection.md"
  issue_473_should_wait: true
  risk_tier: "High"
  implementation_authorized: false
  sequence_id_implementation_authorized: false
  gap_detection_implementation_authorized: false
  eventbus_behavior_change_authorized: false
  parser_behavior_change_authorized: false
  parser_event_class_change_authorized: false
  api_payload_change_authorized: false
  workbook_webhook_change_authorized: false
  private_log_read_authorized: false
  replay_audit_authorized: false
  ci_change_authorized: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
```
