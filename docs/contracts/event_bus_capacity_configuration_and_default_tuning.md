# EventBus Capacity Configuration And Default Tuning Contract

Status: contract only
Codex role: B, Module Contract Writer
Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/468
Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
Latest verified `origin/main`: `cf1960a13b52500e1de1d394e3abd0025f2f7015`

## Purpose

This contract defines how Mythic Edge may later make EventBus subscriber queue
capacity configurable and how a future default capacity may be tuned from
evidence.

Plain English behavior:

- EventBus must preserve completeness before liveness.
- A full subscriber queue must apply backpressure instead of silently dropping
  events.
- Queue capacity is a bounded buffering setting, not a truth rule and not a data
  loss budget.
- Queue pressure metrics may show diagnostic pressure, but they do not authorize
  changing capacity by themselves.
- This issue does not implement a capacity change.

## Source Context

Prerequisites:

- Issue #460 / PR #654 established completeness-preserving EventBus
  backpressure.
- Issue #471 / PR #655 established EventBus consumer delivery classifications.
- Issue #467 / PR #658 established privacy-safe queue pressure metrics.
- Issue #470 / PR #657 established heavy-subscriber worker-queue planning
  boundaries.

Related future issues:

- Issue #469: concurrent fanout.
- Issue #472: sequence IDs and gap detection.
- Issue #473: post-session replay audit.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- GitHub issue #468
- GitHub issues #469, #472, and #473
- GitHub PR #657
- GitHub PR #658
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/contracts/event_bus_consumer_delivery_classification.md`
- `docs/contracts/event_bus_queue_pressure_metrics.md`
- `docs/contracts/event_bus_heavy_subscriber_worker_queues.md`
- `src/mythic_edge_parser/event_bus.py`
- `tests/test_event_bus.py`
- `tests/test_event_bus_queue_pressure_metrics.py`

## Observed Current Behavior

Current EventBus behavior on `origin/main`:

- `EventBus.__init__(capacity: int = 1024, ...)` accepts a constructor capacity.
- `EventBus.with_default_capacity()` returns `EventBus(capacity=1024)`.
- Each subscriber receives an `asyncio.Queue(maxsize=self._capacity)`.
- `EventBus.publish()` waits when a subscriber queue is full.
- `queue_pressure_snapshot()` reports `queue_capacity` and diagnostic pressure
  counters.
- Existing tests use small explicit capacities such as `1` and `2` to prove
  bounded backpressure behavior.

The current default of `1024` is an implicit implementation default. It is not
currently tied to a named policy, default-tuning evidence packet, or documented
configuration boundary.

## First Bad Values

The first bad values are planning and authority gaps, not a proven runtime
failure:

| First bad value | Why it is bad |
| --- | --- |
| `capacity=1024` as an implicit default | The default is not named, versioned, or tied to evidence. |
| `EventBus.with_default_capacity() -> EventBus(capacity=1024)` | Default selection is duplicated as a literal instead of a policy surface. |
| `queue_pressure_snapshot()` treated as authority | Metrics are diagnostic-only and cannot authorize capacity changes. |
| `capacity <= 0` if accepted later through config | `asyncio.Queue(maxsize=0)` is unbounded and would violate bounded backpressure. |
| external config requests without contract | Environment variables, local-app settings, APIs, and persisted config are separate surfaces. |

## Scope Decision

In scope for a later Codex C only if separately authorized:

- name the EventBus default capacity as an EventBus-owned constant or policy
  value;
- preserve `EventBus(capacity=...)` as the explicit constructor override surface;
- preserve `EventBus.with_default_capacity()` as the default-construction helper;
- add fail-closed validation for invalid capacity values;
- keep `queue_pressure_snapshot().queue_capacity` aligned with the effective
  queue capacity;
- add focused tests for default, explicit override, invalid values, and
  backpressure preservation.

Out of scope for this issue and any later implementation unless separately
contracted:

- changing the default capacity;
- adopting a candidate default such as `8192`;
- adding environment variable configuration;
- adding local-app settings persistence;
- adding public API, status API, workbook, webhook, or frontend config fields;
- collecting live metrics;
- writing runtime artifacts;
- changing fanout;
- moving subscriber work into worker queues;
- changing parser facts or parser event classes;
- changing CI;
- claiming reliability readiness, parser truth, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching truth.

## Owning Layer And Truth Boundary

The owning layer is the EventBus support layer inside the parser runtime.

Truth boundary:

- EventBus capacity controls buffering and backpressure only.
- EventBus capacity does not create parser facts.
- EventBus capacity does not change parser event classes.
- EventBus capacity does not prove event correctness.
- EventBus metrics do not prove parser truth.
- Workbook, webhook, API, dashboard, analytics, and AI layers must not treat
  EventBus capacity as a truth signal.

## Capacity Vocabulary

| Term | Meaning |
| --- | --- |
| `repo_default_capacity` | The repository-owned default used by `EventBus.with_default_capacity()`. |
| `explicit_capacity` | A caller-provided constructor capacity, usually in tests or a future contracted runtime construction path. |
| `effective_capacity` | The actual per-subscriber queue `maxsize` used by each `asyncio.Queue`. |
| `candidate_default_capacity` | A proposed replacement default under review. It is not active. |
| `capacity_floor` | The minimum allowed bounded capacity. It must exclude unbounded queue behavior. |
| `capacity_ceiling` | The maximum allowed bounded capacity, if a later implementation defines one. |
| `invalid_capacity` | A capacity value that must fail closed before queue construction. |
| `unbounded_capacity` | Any value or config path that creates an unbounded queue. This is forbidden. |
| `capacity_tuning_evidence` | Public-safe evidence used to justify reviewing a candidate default. |

Allowed capacity statuses:

- `default_unchanged`
- `explicit_capacity_accepted`
- `candidate_default_under_review`
- `candidate_default_blocked`
- `invalid_capacity_rejected`
- `external_config_not_authorized`
- `review_required`
- `unknown_fail_closed`

Forbidden capacity statuses:

- `default_safe_for_production`
- `reliability_ready`
- `parser_truth_confirmed`
- `pressure_resolved`
- `lossless_guaranteed`
- `unbounded_allowed`

## Configuration Boundary

Allowed future configuration surfaces, if separately authorized:

- EventBus-owned constant for the repository default.
- Constructor-level explicit capacity for tests and scoped internal construction.
- Public-safe metadata in queue-pressure snapshots that reports the effective
  capacity.

Forbidden or blocked configuration surfaces in this contract:

- environment variables;
- command-line flags;
- local-app settings files;
- status API fields;
- workbook or webhook payload fields;
- Apps Script configuration;
- user-facing UI controls;
- persisted runtime config files;
- external service configuration.

If any later implementation needs one of the blocked surfaces, stop and route
back to Codex B for a dedicated contract.

## Fail-Closed Capacity Rules

A later implementation should fail closed before queue construction when
capacity is:

- missing from a required configuration path;
- not an integer;
- a boolean value;
- less than or equal to zero;
- unbounded by meaning or by `asyncio.Queue(maxsize=0)` behavior;
- larger than a separately contracted ceiling;
- sourced from an unauthorized config surface;
- ambiguous because multiple sources disagree.

Failure output must be public-safe and symbolic. It must not echo local paths,
private runtime values, raw event payloads, secrets, tokens, or raw log content.

## Default-Tuning Evidence Requirements

A future default-capacity change requires a separate implementation issue and
evidence packet. Evidence must be public-safe and should include:

- the current `repo_default_capacity`;
- the proposed `candidate_default_capacity`;
- why the current default is insufficient;
- whether evidence came from synthetic tests, authorized public-safe metrics, or
  another contracted source;
- #471 consumer classes represented in the evidence;
- #467 queue-pressure fields used, such as `queue_capacity`,
  `max_subscriber_depth`, `publish_wait_count`, and symbolic wait buckets;
- whether pressure came from `truth_critical`, `mixed`, `stale_tolerant`, or
  `unknown` consumers;
- whether #470 worker-queue planning indicates heavy work rather than a capacity
  issue;
- validation that #460 backpressure still preserves completeness;
- explicit non-claims.

Default tuning must not rely on:

- raw `Player.log` or `UTC_Log` content;
- raw event payloads;
- raw diffs or source snippets;
- private paths;
- live metric collection unless separately authorized;
- one-off local observations that cannot be reproduced or summarized safely;
- a desire to avoid backpressure without proving completeness.

## Relationship To #467 Metrics

#467 queue pressure metrics are diagnostic-only.

Allowed uses:

- identify that pressure was observed;
- identify which public-safe consumer class showed pressure;
- compare `queue_capacity` against symbolic depth and wait summaries;
- motivate a candidate review issue.

Forbidden uses:

- automatically changing capacity;
- automatically selecting a default;
- treating pressure metrics as reliability readiness;
- treating pressure metrics as parser truth;
- treating pressure metrics as permission to collect live runtime data;
- treating pressure metrics as permission to change fanout, worker queues,
  sequence IDs, replay, API payloads, workbook payloads, webhook payloads, or CI.

## Relationship To #470 Worker Queues

Capacity tuning must not hide heavy subscriber work.

If pressure is primarily caused by known heavy work:

- keep #467 metrics diagnostic-only;
- use #470 vocabulary to classify the work;
- do not raise capacity as a substitute for worker-queue analysis;
- do not move truth-critical work without separate ordering, flush, failure, and
  gap-detection proof.

Worker queues remain unauthorized by this contract.

## Relationship To Future Reliability Issues

Issue #469, concurrent fanout:

- capacity configuration does not authorize fanout changes;
- issue #469 should wait until capacity boundaries are reviewed or until a
  separate tracker decision selects it.

Issue #472, sequence IDs and gap detection:

- capacity configuration does not authorize event envelope changes, sequence IDs,
  or gap detection;
- capacity evidence may later motivate sequence/gap review, but it is not
  authority.

Issue #473, post-session replay audit:

- capacity pressure may later motivate replay-audit review;
- this contract does not authorize reading private logs, replay execution,
  fixture promotion, corpus status changes, or recovery claims.

## Public-Safe Output Boundary

Allowed public-safe fields for later evidence:

- symbolic capacity source;
- numeric capacity values only when they are repository defaults, explicit test
  inputs, or public-safe candidate values;
- consumer class labels from #471;
- queue-pressure counters and buckets from #467;
- validation command names and pass/fail status;
- symbolic reason categories;
- explicit non-claims.

Forbidden output:

- raw event payloads;
- event content;
- raw logs;
- private local paths;
- secrets, tokens, API keys, webhook URLs, or credentials;
- runtime artifact paths;
- raw source snippets from private evidence;
- readiness, truth, assurance, release, deploy, or production claims.

## Expected Future Artifact Behavior

A later implementation, if authorized, should produce behavior that is small and
testable:

- `EventBus.with_default_capacity()` uses one named default value.
- `EventBus(capacity=...)` preserves explicit capacity construction.
- every subscriber queue receives the same validated effective capacity.
- pressure snapshots continue to report the effective capacity.
- invalid capacity values fail closed before queue creation.
- existing backpressure tests keep proving no silent event drop.
- existing #467 metric tests keep proving public-safe diagnostic output.

The implementation must not change event ordering, event classes, subscriber
close signaling, parser facts, workbook/webhook/API payloads, or CI.

## Validation Expectations For Later Implementation

Focused tests should prove:

- the repository default is named once and used by `with_default_capacity()`;
- explicit constructor capacity overrides the default;
- `queue_pressure_snapshot().queue_capacity` equals the effective capacity;
- a full queue still blocks publish until capacity is available;
- `capacity <= 0` is rejected or otherwise fail-closed before unbounded queue
  behavior can occur;
- non-integer and boolean capacity values are rejected;
- unauthorized external config surfaces are not read;
- #471 consumer classifications are unchanged;
- #467 metrics remain diagnostic-only;
- no raw payloads, raw logs, private paths, secrets, or runtime artifacts appear
  in public output.

Suggested validation commands for a later implementation:

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

If a later implementation adds a dedicated capacity test file, run it before the
broader EventBus and stream tests.

## Acceptance Criteria

- Contract defines capacity vocabulary.
- Contract identifies the current implicit default of `1024`.
- Contract keeps the default unchanged.
- Contract defines fail-closed invalid-capacity expectations.
- Contract treats #467 queue-pressure metrics as diagnostic-only.
- Contract consumes #471 consumer classes without changing them.
- Contract preserves #460 completeness-over-liveness behavior.
- Contract keeps #470 worker-queue planning separate from capacity tuning.
- Contract forbids fanout, worker-queue, sequence/gap, replay, payload, CI,
  parser behavior, and readiness/truth changes.
- Contract defines validation evidence required before any later implementation.

## Stop Conditions

Stop and route back to Codex B if later work requires:

- changing the default capacity without an evidence packet;
- adding environment variable configuration;
- adding local-app settings persistence;
- changing public API or status API payloads;
- changing workbook or webhook payloads;
- collecting live metrics;
- writing runtime artifacts;
- adding worker queues;
- changing fanout;
- adding sequence IDs or event envelopes;
- reading private logs;
- changing parser facts or parser event classes;
- changing CI;
- making reliability readiness, parser truth, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching truth
  claims.

## Recommended Next Role

Recommended next role: Codex E.

Codex E should review this contract against issue #468, the #460/#471/#467/#470
contracts, and the current EventBus code. Codex E should route back to Codex B if
the capacity vocabulary, invalid-capacity rules, or default-tuning evidence
requirements are ambiguous. Codex E should not route to Codex F until the
contract is reviewed and no blocker remains.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic-Edge issue #468.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/468

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source artifact:
docs/contracts/event_bus_capacity_configuration_and_default_tuning.md

Review the EventBus capacity configuration and default tuning contract against
the completed #460 completeness-over-liveness contract, #471 consumer delivery
classification contract, #467 queue pressure metrics contract, #470
heavy-subscriber worker-queue contract, and current EventBus code.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not change EventBus capacity, fanout, worker queues, parser facts, parser
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/468"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  verdict: "event_bus_capacity_configuration_contract_ready_for_review"
  risk_tier: "High"
  target_artifact: "docs/contracts/event_bus_capacity_configuration_and_default_tuning.md"
  latest_verified_main: "cf1960a13b52500e1de1d394e3abd0025f2f7015"
  prerequisite_issue_460_complete: true
  prerequisite_issue_471_complete: true
  prerequisite_issue_467_complete: true
  prerequisite_issue_470_complete: true
  issue_469_should_wait: true
  implementation_authorized: false
  capacity_change_authorized: false
  fanout_change_authorized: false
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
