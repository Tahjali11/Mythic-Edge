# Core EventBus Support Decomposition Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/690>

## Tracker

Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker:
<https://github.com/Tahjali11/Mythic-Edge/issues/463>

Related ARS evidence gate:
<https://github.com/Tahjali11/Mythic-Edge/issues/664>

## Contract And Evidence

- Decision packet:
  `docs/contracts/core_event_bus_support_decomposition_decision_packet.md`
- Fresh scoped evidence issue:
  <https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/143>
- Fresh scoped evidence artifact:
  `automations/adversarial-review-scout/runs/2026/07/07/2026-07-07-codex-c-eventbus-support-scoped-evidence-summary.md`
- Evidence status: `precondition_satisfied`
- Implementation authorization: explicit owner authorization for Codex C
  behavior-preserving same-repo decomposition after scoped evidence.

## Role Performed

Codex C: Module Implementer.

## What Changed

Implemented a narrow behavior-preserving same-repo decomposition of
`src/mythic_edge_parser/event_bus.py`.

The public facade remains `mythic_edge_parser.event_bus`. Public classes and
dataclasses remain defined by that module:

- `EventBus`
- `Subscriber`
- `EventBusPublishWaitSummary`
- `EventBusEventRateSummary`
- `EventBusSubscriberPressure`
- `EventBusQueuePressureSnapshot`

The extracted helper module `src/mythic_edge_parser/event_bus_metrics.py` owns
only private/internal queue-pressure metric vocabulary and normalization
helpers:

- queue pressure schema version string;
- consumer classification source string;
- non-claim vocabulary tuple;
- known consumer classification mapping;
- `SubscriberMetrics`;
- consumer id normalization;
- publish wait bucket selection;
- event rate bucket selection.

## Files Changed

- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/event_bus_metrics.py`
- `tests/test_event_bus.py`
- `docs/implementation_handoffs/core_event_bus_support_decomposition_comparison.md`

## Behavior Preservation Evidence

Baseline before edits:

- `tests/test_event_bus.py` and
  `tests/test_event_bus_queue_pressure_metrics.py`: `13 passed`.

After implementation:

- focused EventBus and queue-pressure tests: `14 passed`;
- stream import smoke test: `1 passed`;
- direct public facade probe confirmed `EventBus`, `Subscriber`, and
  `EventBusQueuePressureSnapshot` still report
  `mythic_edge_parser.event_bus`;
- direct public-safe snapshot probe preserved:
  - schema version `event_bus_queue_pressure_metrics.v1`;
  - consumer classification source
    `event_bus_consumer_delivery_classification.v1`;
  - `event_bus_test_subscriber` classification as `test_fixture_only`.

`tests/test_event_bus.py` now includes a focused facade preservation test so a
future split cannot silently move the public classes or break the package-level
`Subscriber` export.

## Interface Changes

None intended.

Preserved:

- public module path: `mythic_edge_parser.event_bus`;
- public EventBus and Subscriber import surface;
- public queue pressure dataclass names and module identity;
- EventBus constructor and public methods;
- Subscriber `recv()` behavior;
- queue pressure snapshot field names, schema string, status strings, bucket
  strings, consumer classification source, and non-claim strings;
- close/drain behavior, blocked-publish wakeup behavior, and backpressure
  behavior.

## Contracted Area Status

Stayed inside the authorized same-repo, behavior-preserving decomposition
boundary.

Not changed:

- EventBus delivery semantics;
- queue capacity defaults;
- fanout behavior;
- close semantics;
- queue-pressure schema or vocabulary;
- consumer classification vocabulary;
- parser behavior;
- parser event classes;
- API, workbook, webhook, Apps Script, local app, analytics, AI, or coaching
  behavior;
- CI behavior.

## Validation Run

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus.py tests/test_event_bus_queue_pressure_metrics.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_stream_unit.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m py_compile src/mythic_edge_parser/event_bus.py src/mythic_edge_parser/event_bus_metrics.py tests/test_event_bus.py tests/test_event_bus_queue_pressure_metrics.py tests/test_stream_unit.py
PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check src/mythic_edge_parser/event_bus.py src/mythic_edge_parser/event_bus_metrics.py tests/test_event_bus.py tests/test_event_bus_queue_pressure_metrics.py tests/test_stream_unit.py
PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
git diff --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests
```

Observed results:

- focused EventBus tests: `14 passed`;
- focused stream import test: `1 passed`;
- `py_compile`: passed;
- Ruff on touched Python surfaces: passed;
- Ruff on `src tests tools`: passed;
- agent docs consistency check: passed with `checked_files: 36`;
- path-scoped secret/private marker scan over changed files: passed;
- path-scoped protected-surface gate over changed files: passed;
- validation selector over changed files: `selection_status: ok`;
- `git diff --check`: passed;
- full test suite: `2083 passed`.

## Still Unverified

- No GitHub CI has run for this local implementation.
- No ARS run, Refactor Scout run, probe, module sweep, replay audit,
  live-capture check, private evidence check, private log read, runtime
  artifact creation, source-repo action, or CI change was performed.

## Remaining Non-Claims

This implementation does not claim reliability readiness, parser truth,
release readiness, deploy readiness, production readiness, security assurance,
privacy assurance, analytics truth, AI truth, coaching truth, broad ARS
clearance, or Refactor Scout clearance.

## Recommended Next Role

Codex E: Module Reviewer.

Review should focus on whether the helper extraction is behavior-preserving,
whether keeping public classes in `event_bus.py` is the right compatibility
choice, and whether the facade preservation test covers the highest-risk
public import surface.

## Pasteable Codex E Prompt

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

Contract:
docs/contracts/core_event_bus_support_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_event_bus_support_decomposition_comparison.md

Review the Codex C behavior-preserving same-repo EventBus support
decomposition. Verify that `mythic_edge_parser.event_bus` remains the public
facade, public classes and dataclasses keep their import/module identity,
EventBus delivery/backpressure/close behavior is unchanged, queue pressure
schema/vocabulary is unchanged, consumer classification/no-echo behavior is
unchanged, and no parser/runtime/API/workbook/webhook/CI behavior was changed.

Protected boundaries:
Do not change EventBus behavior, parser behavior, parser event classes, queue
capacity, fanout, close semantics, queue-pressure schema, API/workbook/webhook
payloads, CI, private evidence, source-repo actions, or readiness/security/
privacy/parser-truth claims.

Expected output:
Findings first, ordered by severity. If clean, route to Codex F for reviewed
submission. If findings exist, route to Codex D with exact file/line
references, expected fixes, validation expectations, and a workflow_handoff
block.
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
  completed_thread: "C"
  next_thread: "E"
  verdict: "eventbus_support_behavior_preserving_decomposition_ready_for_review"
  source_artifact: "docs/contracts/core_event_bus_support_decomposition_decision_packet.md"
  target_artifact: "docs/implementation_handoffs/core_event_bus_support_decomposition_comparison.md"
  candidate_surface: "src/mythic_edge_parser/event_bus.py"
  candidate_id: "event_bus_support"
  evidence_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/143"
  evidence_artifact: "automations/adversarial-review-scout/runs/2026/07/07/2026-07-07-codex-c-eventbus-support-scoped-evidence-summary.md"
  evidence_status: "precondition_satisfied"
  implementation_authorized: true
  same_repo_decomposition_authorized: true
  cross_repo_extraction_authorized: false
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
  private_evidence_inspection_authorized: false
  runtime_artifact_creation_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
