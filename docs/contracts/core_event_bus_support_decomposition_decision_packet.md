# Core EventBus Support Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/690>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Related ARS evidence gate: <https://github.com/Tahjali11/Mythic-Edge/issues/664>

Latest completed protected-surface decomposition issue:
<https://github.com/Tahjali11/Mythic-Edge/issues/687>

Latest completed protected-surface decomposition PR:
<https://github.com/Tahjali11/Mythic-Edge/pull/689>

Latest merge commit: `3c20909d42d8818697533150f79e717d605ac7e5`

Target candidate: `src/mythic_edge_parser/event_bus.py`

Candidate id: `event_bus_support`

Candidate class: `mixed_governance_runtime_surface`

## Module

`core_event_bus_support_decomposition_decision_packet`

This contract is the Phase 5 decomposition decision packet for the EventBus
support surface.

Plain English: `src/mythic_edge_parser/event_bus.py` is the in-memory async
delivery support module that lets parser events move from publishers to
subscribers. It also owns subscriber close behavior, backpressure behavior,
queue pressure snapshots, consumer classification metadata, and diagnostic
bucket vocabulary. This packet decides whether that surface may later be split
into smaller same-repo modules while preserving behavior. It does not implement
that split.

This contract is planning-only. It does not implement code, move files, open a
PR, change EventBus delivery behavior, change queue capacity, change fanout,
change close semantics, change queue pressure schema, change consumer
classification vocabulary, change parser behavior, change parser event
classes, change API/workbook/webhook payloads, change CI, run ARS, run
Refactor Scout, read private evidence, or claim reliability readiness, parser
truth, security assurance, privacy assurance, release readiness, deploy
readiness, or production readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/690>
- Project roadmap / tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Broad decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Related ARS evidence gate: <https://github.com/Tahjali11/Mythic-Edge/issues/664>
- Target artifact:
  `docs/contracts/core_event_bus_support_decomposition_decision_packet.md`

## Source Artifacts Inspected

- GitHub issue #690
- GitHub issue #568
- GitHub issue #463
- GitHub issue #664
- GitHub issue #687 and PR #689 as the immediate predecessor lane
- `AGENTS.md`
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md`
- `docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md`
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/contracts/event_bus_consumer_delivery_classification.md`
- `docs/contracts/event_bus_queue_pressure_metrics.md`
- `docs/contracts/event_bus_heavy_subscriber_worker_queues.md`
- `docs/contracts/event_bus_capacity_configuration_and_default_tuning.md`
- `docs/contracts/event_bus_concurrent_fanout_completeness.md`
- `docs/contracts/event_bus_sequence_ids_and_subscriber_gap_detection.md`
- `docs/contracts/event_bus_post_session_replay_audit_recovery.md`
- `src/mythic_edge_parser/event_bus.py`
- `tests/test_event_bus.py`
- `tests/test_event_bus_queue_pressure_metrics.py`

No private `Player.log`, `UTC_Log`, app-data, live MTGA data, runtime status
files, generated local artifacts, workbook exports, raw diffs, source patches,
secrets, credentials, tokens, API keys, webhook URLs, ARS run artifacts,
Refactor Scout artifacts, or private evidence were read, created, imported, or
modified.

## Owning Layer

Primary layer: Parser shared support / EventBus runtime support.

`src/mythic_edge_parser/event_bus.py` owns in-memory parser event delivery
mechanics. It does not own MTGA raw log truth, parser event-class definitions,
match identity, game identity, parser state final reconciliation, workbook
schema, webhook payload shape, Apps Script behavior, API payload shape,
analytics truth, AI truth, coaching truth, security assurance, privacy
assurance, release readiness, deploy readiness, or production readiness.

## Internal Project Area

Parser shared support, with local app bridge consumers.

The EventBus is not a downstream correction layer and not a persistence layer.
It supports event delivery inside the runtime. Queue pressure metrics and
delivery diagnostics are diagnostic only; they are not parser truth and do not
authorize behavior changes.

## Truth Owner

- `src/mythic_edge_parser/event_bus.py` owns the current `EventBus` and
  `Subscriber` public import surface, in-memory delivery behavior, queue
  pressure snapshot schema, consumer metadata lookup, pressure status
  vocabulary, wait bucket vocabulary, event-rate bucket vocabulary, and
  non-claim vocabulary.
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md` owns
  the completeness-over-liveness backpressure boundary.
- `docs/contracts/event_bus_consumer_delivery_classification.md` owns the
  consumer classification vocabulary and current consumer inventory boundary.
- `docs/contracts/event_bus_queue_pressure_metrics.md` owns the public-safe
  diagnostic metric boundary.
- Repo governance docs, active issues, accepted contracts, and human owner
  decisions remain authoritative for workflow routing.

## Bridge-Code Status

`shared_support_with_bridge_consumers`

The EventBus is parser-owned shared support, but current consumers include both
the parser runtime path and local app capture control. That bridge status makes
decomposition higher risk than a local advisory helper: a careless split could
change ordering, close behavior, blocked-publish wakeups, queue pressure
snapshots, consumer metadata, or no-echo boundaries even if no product feature
was intended.

## Files Owned By This Contract

- `docs/contracts/core_event_bus_support_decomposition_decision_packet.md`

Files referenced but not owned:

- `src/mythic_edge_parser/event_bus.py`
- `tests/test_event_bus.py`
- `tests/test_event_bus_queue_pressure_metrics.py`
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/contracts/event_bus_consumer_delivery_classification.md`
- `docs/contracts/event_bus_queue_pressure_metrics.md`
- `docs/contracts/event_bus_heavy_subscriber_worker_queues.md`
- `docs/contracts/event_bus_capacity_configuration_and_default_tuning.md`
- `docs/contracts/event_bus_concurrent_fanout_completeness.md`
- `docs/contracts/event_bus_sequence_ids_and_subscriber_gap_detection.md`
- `docs/contracts/event_bus_post_session_replay_audit_recovery.md`

## Authorization State

The following flags are false for this contract:

```yaml
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
eventbus_behavior_change_authorized: false
queue_capacity_change_authorized: false
fanout_change_authorized: false
close_semantics_change_authorized: false
backpressure_behavior_change_authorized: false
queue_pressure_schema_change_authorized: false
queue_pressure_metric_collection_authorized: false
consumer_classification_change_authorized: false
sequence_id_implementation_authorized: false
gap_detection_implementation_authorized: false
post_session_replay_audit_authorized: false
parser_behavior_change_authorized: false
parser_event_class_change_authorized: false
api_payload_change_authorized: false
workbook_webhook_change_authorized: false
apps_script_change_authorized: false
ci_change_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
private_evidence_inspection_authorized: false
runtime_artifact_creation_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
truth_or_assurance_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
release_readiness_claimed: false
deploy_readiness_claimed: false
production_readiness_claimed: false
```

Any future handoff, evidence packet, review, or implementation plan that flips
one of these flags without a separate reviewed issue and explicit owner
approval must fail closed.

## Codex E Schema And Vocabulary Reconciliation

This section resolves:

- `EVENTBUS-DECOMP-E-001`
- `EVENTBUS-DECOMP-E-002`

The packet must consume the #665 Phase 5 decision-packet schema literally when
it uses the #665 packet envelope. It must not invent parallel schema values
that look equivalent to #665 terms but are not accepted by the source
contract.

Canonical corrections:

- the schema `candidate_surface_class` is
  `mixed_governance_runtime_surface`, the closest accepted #665 class for an
  EventBus runtime-support candidate that is intentionally outside the earlier
  governance/report/helper lane;
- the descriptive phrase `core_runtime_eventbus_support_surface` may appear
  only as explanatory prose and must not be treated as schema vocabulary;
- the schema `final_decision` is `review_required`, one of the exact #665
  decision values;
- the phrase `same_repo_decomposition_candidate_review_required` is not schema
  vocabulary and must not appear in the packet envelope, candidate row, refusal
  vocabulary, or handoff as a decision value;
- same-repo decomposition remains the preferred direction in prose only:
  EventBus support may later become a `same_repo_decomposition_candidate` only
  after Codex E review, explicit owner routing, and a separate implementation
  authorization;
- cross-repo extraction remains rejected;
- all false-authority fields from #665 remain literal, including
  `source_mutation_authorized: false` and
  `truth_or_assurance_claimed: false`.
- the ARS/refactor evidence block uses the exact #665 required fields and
  allowed values;
- `prior_ars_evidence_found` and `prior_refactor_scout_evidence_found` use
  `no`, not a custom value such as `not_claimed`;
- `evidence_status` uses
  `fresh_scoped_evidence_required_before_implementation`, not a custom value
  such as `contract_only_no_implementation_authority`;
- `fresh_scoped_evidence_needed` uses `yes`, not a custom
  `fresh_scoped_evidence_needed_before_implementation` field;
- `relevant_changes_since_review` and `ars_version_contract_bundle` are present
  because #665 requires them.

Because EventBus support is a runtime protected surface, `review_required` is
the safest canonical decision for this Codex B packet. It records that the
contract is ready for Codex E review, not that implementation, file movement,
or behavior-preserving extraction is approved.

Because EventBus support owns runtime delivery mechanics, fresh scoped ARS or
Refactor Scout evidence is required before any later implementation unless a
future owner decision creates a separate, explicit, issue-scoped exception.
That exception must be recorded outside the schema block and must not be
represented as an alternate schema value.

## Packet Envelope

```yaml
packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/690"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
source_contract: "docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md"
previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/687"
previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/689"
previous_merge_commit: "3c20909d42d8818697533150f79e717d605ac7e5"
target_commit: "3c20909d42d8818697533150f79e717d605ac7e5"
candidate_scope: "eventbus_support_only"
candidate_id: "event_bus_support"
candidate_surface_class: "mixed_governance_runtime_surface"
current_path: "src/mythic_edge_parser/event_bus.py"
target_artifact: "docs/contracts/core_event_bus_support_decomposition_decision_packet.md"
phase_5_order_preserved: true
governance_report_helper_phase_complete: true
eventbus_support_active: true
api_frontend_live_capture_deferred: true
parser_state_deferred: true
final_decision: "review_required"
implementation_authorized: false
file_move_authorized: false
cross_repo_extraction_authorized: false
eventbus_behavior_change_authorized: false
parser_behavior_change_authorized: false
parser_event_class_change_authorized: false
ci_change_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
truth_or_assurance_claimed: false
```

## Observed Current Behavior

`src/mythic_edge_parser/event_bus.py` currently contains these related
concerns:

- `Subscriber.recv()` returns queued parser events and returns `None` after
  close;
- `Subscriber.recv()` wakes blocked publishers by notifying the shared
  `asyncio.Condition` after an item leaves a subscriber queue;
- `EventBus.__init__(capacity=1024, time_source=None)` initializes bounded
  subscriber queues, close state, queue pressure counters, subscriber metrics,
  active waiters, and a metrics time window;
- `EventBus.with_default_capacity()` constructs the current default capacity;
- `EventBus.subscribe(consumer_id="unknown_subscriber")` creates a bounded
  subscriber queue and records normalized consumer metadata;
- `EventBus.publish(event)` sends the same accepted parser event to each
  active subscriber queue and waits for capacity instead of silently dropping
  events;
- `EventBus.close()` sets the closed flag, wakes subscribers and blocked
  publishers, tries to place a sentinel, clears active queue registries, and
  lets accepted queued events drain;
- `queue_pressure_snapshot()` returns an in-memory public-safe diagnostic
  snapshot without echoing event payloads;
- `reset_queue_pressure_metrics()` resets diagnostic counters without clearing
  queued events or changing delivery behavior;
- private helpers own waiter decrementing, depth recording, subscriber
  pressure, pressure status, metrics status, classification status, event-rate
  buckets, publish-wait buckets, and consumer metadata normalization.

Current focused tests cover:

- publish waits when a subscriber queue is full;
- full queues do not remove slow subscribers as dead;
- close delivers a close signal;
- close returns when a subscriber queue is full;
- publish after close does not deliver new events;
- close unblocks publish waiting on a full queue;
- queue pressure snapshots are public-safe and schema-versioned;
- queue pressure metrics track depth, wait, reset, closed-bus, and consumer
  classification behavior;
- unknown consumer ids fail closed without echoing unsafe input;
- queue pressure snapshots do not expose event payloads or event kind.

## Problem Statement And First Bad Values

The intended workflow is:

1. use this packet to decide the future decomposition boundary for
   `src/mythic_edge_parser/event_bus.py`;
2. preserve current EventBus behavior and public import/API surface;
3. require Codex E review before any submitter or implementation route;
4. require explicit user routing before any later Codex C implementation;
5. keep any future decomposition same-repo-first unless a later contract
   proves a stronger boundary.

The first bad value is treating this contract as implementation authority.

The second bad value is changing EventBus behavior while calling the change
behavior-preserving.

The third bad value is moving the public import path away from
`mythic_edge_parser.event_bus` or changing the `EventBus` / `Subscriber`
surface without a separate public-interface contract.

The fourth bad value is changing completeness-over-liveness behavior,
close/drain behavior, blocked-publish wakeups, sequential fanout behavior,
queue pressure schema, pressure/status vocabulary, consumer classification
vocabulary, no-echo behavior, or non-claim vocabulary during a decomposition.

The fifth bad value is treating EventBus metrics or sequence/gap planning as
proof of reliability readiness, parser truth, release readiness, deploy
readiness, production readiness, security assurance, or privacy assurance.

The sixth bad value is treating same-repo decomposition eligibility as
permission for cross-repo extraction.

## Public Interface To Preserve

This contract does not change the EventBus public interface. A later
behavior-preserving implementation must preserve at least:

- module import path: `mythic_edge_parser.event_bus`;
- public class: `EventBus`;
- public class: `Subscriber`;
- public dataclass: `EventBusPublishWaitSummary`;
- public dataclass: `EventBusEventRateSummary`;
- public dataclass: `EventBusSubscriberPressure`;
- public dataclass: `EventBusQueuePressureSnapshot`;
- `EventBus.__init__(capacity: int = 1024, *, time_source: Callable[[], float] | None = None)`;
- `EventBus.with_default_capacity()`;
- `EventBus.subscribe(*, consumer_id: str = "unknown_subscriber")`;
- `EventBus.publish(event: GameEvent)`;
- `EventBus.close()`;
- `EventBus.queue_pressure_snapshot()`;
- `EventBus.reset_queue_pressure_metrics()`;
- `Subscriber.recv()`;
- current return values, async behavior, accepted-event object delivery,
  sentinel handling, and closed-bus behavior;
- current queue pressure snapshot field names and schema version;
- current consumer classification source and public-safe non-claims.

Any proposed change to these items is outside this decision packet and must
route back to Codex B.

## Decomposition Decision

Decision: `review_required`

Same-repo decomposition is eligible for later consideration, but it is not
authorized by this contract. The preferred direction is to keep
`src/mythic_edge_parser/event_bus.py` as the stable public facade and, only
after explicit implementation routing, consider extracting private same-repo
helpers behind that facade.

Cross-repo extraction is rejected. EventBus behavior is tightly coupled to the
parser runtime, parser event types, focused tests, and prior EventBus
contracts. A separate repository would introduce versioning, ownership, and
governance ambiguity around a core runtime support surface.

Keeping the current monolithic file also remains an acceptable outcome. A
future implementer must prove that a split reduces review burden without
changing behavior. If that proof is weak, the correct decision is
`same_repo_keep_current_path`.

## Candidate Row

| Field | Value |
| --- | --- |
| `candidate_id` | `event_bus_support` |
| `candidate_surface_class` | `mixed_governance_runtime_surface` |
| `current_path` | `src/mythic_edge_parser/event_bus.py` |
| `current_behavior` | In-memory async EventBus delivery, bounded subscriber queues, completeness-preserving backpressure, close/drain signaling, queue pressure snapshots, consumer metadata, diagnostic buckets, and public-safe non-claims |
| `truth_or_authority_owner` | EventBus owns in-memory delivery mechanics only; parser/state remains parser truth owner; repo contracts and human owner decisions own workflow authority |
| `upstream_dependencies` | `asyncio.Queue`, `asyncio.Event`, `asyncio.Condition`, `GameEvent`, caller-provided `consumer_id`, optional `time_source`, existing EventBus contracts |
| `downstream_consumers` | Parser stream/runtime, `runner.py`, local app capture control, EventBus tests, queue pressure metric consumers, future diagnostic/replay planning contracts |
| `protected_surface_contact` | `read_only_reference`; this packet reads source and tests as reference only and does not mutate EventBus behavior |
| `proposed_destination` | Same repository, same public facade at `src/mythic_edge_parser/event_bus.py`, optional private same-repo helper modules only after explicit implementation authorization |
| `why_not_keep_local` | The current file combines public API, subscriber receive logic, publish/backpressure logic, close behavior, metrics dataclasses, metric counters, consumer metadata, pressure status, and bucket helpers. A later split may reduce review fatigue if behavior can be proven identical. |
| `why_not_move_to_existing_repo` | Adjacent repos do not own parser runtime EventBus behavior or its current tests and contracts. |
| `why_not_create_new_repo` | A new repo would add dependency/version skew around a core parser runtime support surface. |
| `new_public_interface_needed` | `none` |
| `new_public_interface_description` | Not applicable; any later implementation must preserve `mythic_edge_parser.event_bus`, public class names, dataclass fields, method signatures, async behavior, queue pressure schema, non-claim vocabulary, and test-visible semantics. |
| `behavior_preservation_tests` | Focused EventBus tests for publish backpressure, ordering, slow subscriber retention, close behavior, publish-after-close behavior, blocked-publish wakeup, queue pressure schema, public-safe no-echo behavior, reset behavior, closed-bus metrics, and consumer classification behavior |
| `rollback_plan` | Revert implementation commit; restore all EventBus logic to `src/mythic_edge_parser/event_bus.py`; remove any same-repo helper modules introduced by the implementation; do not alter parser, EventBus behavior, API, workbook/webhook, CI, runtime artifacts, or private evidence. |
| `ars_refactor_evidence_status` | `fresh_scoped_evidence_required_before_implementation`; not required for this contract-only packet, required before any later implementation |
| `non_claims` | No reliability readiness, parser truth, release readiness, deploy readiness, production readiness, security assurance, privacy assurance, ARS clearance, Refactor Scout clearance, EventBus behavior approval, or CI enforcement authority |
| `final_decision` | `review_required` |

## Same-Repo Module Boundaries

A later implementation may split internal code only if these boundaries
preserve behavior exactly:

- Public facade:
  `src/mythic_edge_parser/event_bus.py` remains the public import path for
  `EventBus`, `Subscriber`, queue pressure dataclasses, and public methods.
- Type and schema layer:
  queue pressure dataclass names, field names, field meanings, schema version,
  consumer classification source, and non-claim vocabulary remain stable.
- Subscriber receive layer:
  `Subscriber.recv()` preserves queue-first behavior, close-event wakeup,
  pending-task cancellation, space-available notification, sentinel handling,
  and `None` return on close.
- Publish/backpressure layer:
  `EventBus.publish()` preserves completeness-over-liveness behavior, waits on
  full queues, does not drop accepted events silently, does not remove slow
  subscribers as dead, and returns without delivery after close.
- Close layer:
  `EventBus.close()` remains idempotent, wakes blocked publishers and
  subscribers, does not deadlock on full queues, and allows already accepted
  queued events to drain before `Subscriber.recv()` returns `None`.
- Metrics layer:
  queue pressure counters, reset behavior, closed-bus behavior, pressure
  status values, wait bucket values, event-rate bucket values, and no-echo
  behavior remain stable.
- Consumer classification layer:
  known consumer ids, fallback behavior, fail-closed unknown-consumer handling,
  and unsafe-consumer-id no-echo behavior remain stable.
- Test surface:
  existing tests that import `EventBus` from `mythic_edge_parser.event_bus`
  continue to pass without import-path changes.

Candidate helper names are intentionally not fixed by this contract. A later
Codex C must inspect current imports and choose the smallest same-repo helper
shape that preserves behavior. If helper extraction would require a public
interface change, the route must return to Codex B.

## ARS And Refactor Scout Evidence Status

No fresh scoped ARS or Refactor Scout evidence is claimed by this packet.

```yaml
prior_ars_evidence_found: "no"
prior_refactor_scout_evidence_found: "no"
reviewed_repo: "none"
reviewed_scope: "none"
reviewed_commit: "none"
ars_version_contract_bundle: "none"
current_target_commit: "3c20909d42d8818697533150f79e717d605ac7e5"
relevant_changes_since_review: "not_applicable"
evidence_status: "fresh_scoped_evidence_required_before_implementation"
fresh_scoped_evidence_needed: "yes"
reason: "The candidate is same-repo, but it owns core runtime delivery behavior. Fresh scoped ARS or Refactor Scout evidence is required before any later implementation."
```

Fresh scoped ARS or Refactor Scout evidence is not required for this
contract-only packet because no implementation, file move, runtime behavior
change, private evidence read, source mutation, or readiness claim is
authorized here.

Fresh scoped ARS or Refactor Scout evidence is required before a later Codex C
implementation because the candidate:

- owns runtime delivery completeness and close behavior;
- owns diagnostic public-safe snapshot schema;
- bridges parser runtime and local app consumers;
- has prior EventBus reliability contracts that must remain coherent;
- can create false reliability authority if decomposed carelessly.

A future owner exception, if granted separately, must name this issue,
candidate id, current path, target commit or branch, allowed next role, and
preserved boundaries. It must not be encoded as custom schema vocabulary and
must not become general ARS clearance, reliability readiness, parser truth,
security assurance, privacy assurance, or CI authority.

## Allowed Later Implementation Boundary

After Codex E review and explicit user routing, a later Codex C implementation
may proceed only inside a behavior-preserving same-repo boundary.

If authorized, the later implementation may:

- keep `src/mythic_edge_parser/event_bus.py` as the public facade;
- extract private same-repo helper modules only if current imports and tests
  remain stable;
- preserve existing public class names, dataclasses, method signatures, schema
  strings, status strings, bucket strings, and non-claim strings;
- add focused behavior-preservation tests;
- compare before/after queue pressure snapshot output using public-safe
  synthetic events;
- write only the implementation handoff required by the workflow.

That later implementation must not:

- move the public import path;
- change EventBus delivery semantics;
- change queue capacity defaults;
- change close/drain behavior;
- change sequential versus concurrent fanout behavior;
- add sequence IDs or gap detection;
- run replay audit;
- change parser event classes or parser facts;
- change API, workbook, webhook, Apps Script, local app, analytics, AI, or
  coaching behavior;
- collect live metrics or write runtime artifacts;
- run ARS, Refactor Scout, probes, module sweeps, replay audits, private
  evidence checks, or live-capture checks unless separately authorized;
- read private logs, app-data, workbook exports, source patches, raw diffs,
  local paths, secrets, credentials, tokens, API keys, or webhook URLs;
- change CI or claim readiness.

## Behavior-Preservation Validation Expectations

A later implementation must collect baseline evidence before editing and
compare it after the change. Minimum expected validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus_queue_pressure_metrics.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m py_compile src/mythic_edge_parser/event_bus.py
python3 tools/check_secret_patterns.py docs/contracts/core_event_bus_support_decomposition_decision_packet.md
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

If helper modules are added, include those helper modules,
`src/mythic_edge_parser/event_bus.py`, EventBus tests, and the implementation
handoff artifact in path-scoped secret/private-marker and protected-surface
validation.

Behavior-preservation evidence must include:

- before/after test results for `tests/test_event_bus.py`;
- before/after test results for `tests/test_event_bus_queue_pressure_metrics.py`;
- proof that `from mythic_edge_parser.event_bus import EventBus` still works;
- before/after queue pressure snapshot comparison for public-safe synthetic
  events;
- proof that unknown consumer ids still fail closed without echoing input;
- proof that event payloads and event kinds are not echoed in queue pressure
  snapshots;
- proof that accepted queued events still drain across close;
- proof that blocked publishes are still woken by close;
- proof that no runtime artifacts, private logs, raw diffs, source patches,
  source snippets, secrets, local paths, workbook exports, generated data, or
  failed posts were committed.

Validation must not:

- run private evidence;
- run ARS, Refactor Scout, probes, module sweeps, replay audits, or live
  capture unless separately authorized;
- change CI;
- create durable runtime artifacts;
- claim readiness, parser truth, reliability readiness, security assurance, or
  privacy assurance.

## Rollback Plan

Rollback must be simple:

- revert the decomposition implementation commit;
- restore all EventBus public facade and internal logic to
  `src/mythic_edge_parser/event_bus.py`;
- remove any same-repo helper modules introduced by the implementation commit;
- preserve the public import path and current tests;
- do not update parser behavior, EventBus behavior, API, workbook, webhook,
  Apps Script, CI, runtime artifacts, source repos, private artifacts, raw logs,
  generated data, failed posts, workbook exports, or private evidence as part
  of rollback unless a later issue explicitly authorizes that separate scope.

## Refusal And Downgrade Vocabulary

Future roles must fail closed using these statuses:

- `same_repo_decomposition_candidate`: internal same-repo extraction may be
  considered only after review and explicit implementation routing.
- `same_repo_keep_current_path`: keep the current file intact because
  behavior-preservation risk is higher than maintenance benefit.
- `request_fresh_ars_refactor_evidence`: scoped ARS or Refactor Scout evidence
  or explicit owner acceptance is needed before implementation.
- `request_scope_split_child`: proposed work combines decomposition with
  EventBus behavior, parser behavior, queue capacity, fanout, metrics,
  sequence IDs, replay audit, API, workbook, webhook, CI, private evidence, or
  production changes and needs a new issue.
- `reject_cross_repo_extraction`: moving EventBus support outside this repo is
  not allowed by this packet.
- `unsupported`: requested action lacks authority or evidence.
- `review_required`: Codex E or the human owner must resolve the route before
  implementation.

Forbidden statuses:

- `implementation_approved`
- `file_move_approved`
- `cross_repo_extraction_approved`
- `eventbus_behavior_change_approved`
- `parser_truth_confirmed`
- `reliability_readiness_confirmed`
- `security_assured`
- `privacy_assured`
- `ready_for_release`
- `ready_for_deploy`
- `ready_for_production`

## Codex C Implementation Boundary

Codex C is not authorized by this contract.

If a later user instruction routes to Codex C after review, the implementation
must be a two-pass behavior-preserving refactor:

1. Preserve behavior and public API while adding focused tests or baseline
   evidence if missing.
2. Extract only the smallest same-repo private helpers needed to reduce review
   burden.

No behavior improvement, capacity tuning, fanout change, metrics expansion,
sequence/gap detection, replay audit, parser fact change, public interface
change, or CI change may be bundled into that implementation.

## Next Recommended Role

Codex E - Module Reviewer.

Codex E should review this contract against issue #690, the EventBus reliability
contracts, and the current `event_bus.py` / EventBus tests. Review should focus
on whether the decision vocabulary is compatible with the #665 packet
vocabulary, whether the EventBus public interface is fully protected, and
whether the same-repo-first / cross-repo-refusal boundary is clear.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #690.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/690

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Target artifact:
docs/contracts/core_event_bus_support_decomposition_decision_packet.md

Review the Codex B contract for the EventBus support Phase 5 decomposition
decision packet. Verify that it preserves EventBus behavior, public import/API
surface, queue pressure schema, consumer classification vocabulary,
backpressure and close semantics, no-echo boundaries, and non-claim language.

Protected boundaries:
Do not implement code, move files, open a PR, change EventBus behavior, change
parser behavior, change parser event classes, change API/workbook/webhook
payloads, change CI, run ARS or Refactor Scout, read private evidence, or claim
readiness, reliability readiness, parser truth, security assurance, or privacy
assurance.

Expected output:
Findings first, ordered by severity. If the contract is ready, say so and route
to Codex F only if docs-only submission is appropriate. If blocked, route back
to Codex B with exact finding ids, contract sections, expected correction, and
a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/690"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/687"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/689"
  previous_merge_commit: "3c20909d42d8818697533150f79e717d605ac7e5"
  completed_thread: "B"
  next_thread: "E"
  verdict: "eventbus_support_decomposition_decision_packet_ready_for_review"
  target_artifact: "docs/contracts/core_event_bus_support_decomposition_decision_packet.md"
  candidate_surface: "src/mythic_edge_parser/event_bus.py"
  candidate_id: "event_bus_support"
  candidate_surface_class: "mixed_governance_runtime_surface"
  risk_tier: "High"
  final_decision: "review_required"
  same_repo_decomposition_preferred: true
  cross_repo_extraction_authorized: false
  implementation_authorized: false
  file_move_authorized: false
  eventbus_behavior_change_authorized: false
  queue_capacity_change_authorized: false
  fanout_change_authorized: false
  close_semantics_change_authorized: false
  queue_pressure_schema_change_authorized: false
  consumer_classification_change_authorized: false
  parser_behavior_change_authorized: false
  parser_event_class_change_authorized: false
  api_payload_change_authorized: false
  workbook_webhook_change_authorized: false
  ci_change_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  private_evidence_inspection_authorized: false
  runtime_artifact_creation_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
