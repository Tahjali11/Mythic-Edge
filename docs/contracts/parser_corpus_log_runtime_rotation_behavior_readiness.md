# Parser Corpus Log Runtime Rotation Behavior Readiness Contract

## Module

`log_runtime.rotation` parser corpus behavior-readiness framing.

Plain English: Mythic Edge already records log-runtime rotation as report-only
boundary metadata from issue #444. This contract defines the narrowest safe
path for moving the row toward behavior readiness: reduced synthetic
tailer/stream behavior evidence only. The uplift may prove that existing
repo-owned temp-file tests cover `FileTailer` size-shrink rotation detection,
replacement-content reading from the beginning, and sanitized
`LogFileRotatedEvent` publication. It must not claim live file-system watcher
correctness, robust log-rotation resilience, file identity tracking,
duplicate/replay prevention, recycle/rollback truth, private smoke success,
parser support, release readiness, production behavior, analytics truth,
AI truth, coaching truth, tracker completion, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/502
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/500
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/501
- Previous merge commit: `28b588767c017aa2290121d2a8d21656eb49d905`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/444
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-log-runtime-rotation-behavior-readiness-502`
- Risk tier: High
- Status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`
- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_tailer.py`
- `tests/test_stream_integration.py`
- `tests/test_event_schema_snapshots.py`

## Purpose

Define the next safe behavior-readiness step for `log_runtime.rotation`.

This contract answers:

- whether the row may move from `covered_report_only` toward
  `covered_synthetic`;
- what reduced synthetic tailer/stream evidence is sufficient;
- what `parser_behavior_verified` may and may not mean for this row;
- which adjacent rotation/collision rows remain separate; and
- how #388 / #381 activation remains deferred.

This contract does not implement code, create or change runtime fixtures, edit
corpus metadata, run private/live MTGA checks, activate #388/#381, or claim
log-runtime rotation support beyond the reduced synthetic tailer/stream packet.

## Observed Current Behavior

Observed on `main` at
`28b588767c017aa2290121d2a8d21656eb49d905`:

- Issue #502 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #500 is complete after PR #501.
- The corpus parity report state recorded by issue #502 is:

```text
45 families; committed=6, synthetic=20, report_only=13,
blocked=6 [private=2, external=4], missing=0,
parser_behavior_ready=false,
pipeline_activation_ready_for_issue_388=false
```

Current `log_runtime.rotation` row:

```yaml
scenario_family: "log_runtime.rotation"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "log_runtime_rotation_boundary_report_v1"
parser_event_families: []
parser_claim_families:
  - "log_runtime_rotation_boundary_report"
  - "tailer_rotation_reference_only"
  - "stream_log_file_rotated_reference_only"
  - "live_watcher_correctness_non_claim"
  - "filesystem_rotation_truth_non_claim"
  - "duplicate_replay_prevention_non_claim"
  - "recycle_or_rollback_non_claim"
  - "private_smoke_non_claim"
  - "readiness_production_non_claim"
  - "analytics_ai_coaching_non_claim"
```

Current adjacent behavior:

- `FileTailer.poll_once(...)` sets `TailBatch.rotated=True` when current file
  size is smaller than the prior offset.
- When rotated, `FileTailer` resets its line buffer, seeks to the beginning,
  and reads replacement content from byte zero.
- `MtgaEventStream` publishes `LogFileRotatedEvent` when it observes a rotated
  tail batch.
- The stream rotation event payload is
  `{"type": "log_file_rotated", "path": "Player.log"}` for the focused test
  path, preserving only a sanitized display name.
- `tests/test_tailer.py` already exercises a temp-file replacement-content
  rotation path.
- `tests/test_stream_integration.py` already exercises sanitized
  `LogFileRotatedEvent` publication from a fake rotated tailer batch.
- `tests/test_event_schema_snapshots.py` includes `LogFileRotatedEvent` in
  parser event class and payload snapshots.

Current non-evidence:

- The #444 boundary explicitly says `TailBatch.rotated`,
  `LogFileRotatedEvent`, and focused temp-file/fake-tailer tests are not live
  watcher correctness, robust log-rotation resilience, file identity tracking,
  duplicate/replay prevention, recycle/rollback truth, private smoke success,
  release readiness, production behavior, analytics truth, AI truth, coaching
  truth, or full corpus parity by themselves.
- `drift_debug.rename_or_rotation_collision` remains a separate report-only
  family and must not be upgraded by this issue.
- `drift_debug.recycle_or_rollback` remains blocked external-boundary context
  and must not be upgraded by this issue.
- `log_runtime.unknown_entry` remains report-only drift/diagnostics context and
  must not be reinterpreted as rotation readiness.

## Scope Decision

Recommended future path: reduced synthetic tailer/stream behavior uplift.

A later Codex C implementation may move `log_runtime.rotation` from
`covered_report_only` toward `covered_synthetic` with
`parser_behavior_verified` only if it adds corpus metadata and tests tying the
row to a reduced synthetic behavior packet:

1. `FileTailer` size-shrink rotation detection.
2. Replacement-content reading from the beginning after rotation.
3. `MtgaEventStream` sanitized `LogFileRotatedEvent` publication from a
   rotated tail batch.
4. `LogFileRotatedEvent` schema snapshot compatibility.

The reduced packet must prove only repo-owned temp-file/fake-tailer behavior.
It may cite existing focused tests if they already prove the required behavior,
but the corpus manifest/session-ledger entries must make the claim explicit
and bounded.

The behavior claim is intentionally small:

- synthetic size-shrink/replacement behavior, not live rotation truth;
- sanitized stream event publication, not production stream readiness;
- current event shape compatibility, not event-class change authority;
- existing behavior, not new tailer/stream interpretation;
- local temp-file/fake-tailer evidence, not private Player.log evidence.

This contract authorizes a metadata/test/docs implementation path. It does not
authorize tailer, stream, event, parser, diagnostics, drift, golden replay,
feature-equity, evidence-ledger, runtime, workbook, webhook, Apps Script,
analytics, AI, coaching, CI, merge, deploy, production, or final integration
behavior changes. If Codex C cannot prove the reduced synthetic packet using
existing behavior, the row must remain `covered_report_only` and route back to
Codex B or Codex A.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- `src/mythic_edge_parser/log/tailer.py` owns current `FileTailer` and
  `TailBatch.rotated` behavior.
- `src/mythic_edge_parser/stream.py` owns current
  `LogFileRotatedEvent` publication.
- `src/mythic_edge_parser/events.py` owns the `LogFileRotatedEvent` class
  shape.
- Corpus parity owns status aggregation and readiness metrics.

This contract does not move truth ownership to corpus metadata, diagnostics,
drift reports, workbook formulas, dashboards, Apps Script, webhook transport,
analytics, AI, coaching, readiness, deploy, production, or tracker lifecycle
surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser / log runtime support, as the existing producer of tailer and stream
  behavior.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not a Parser behavior module, live file watcher module,
diagnostics module, drift module, analytics module, AI module, coaching
module, workbook module, release-readiness module, production module,
private-evidence execution, or parser-evidence pipeline activation.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for future reduced synthetic behavior evidence:

- `tests/test_tailer.py`;
- `tests/test_stream_integration.py`;
- `tests/test_event_schema_snapshots.py`;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- `tests/test_corpus_parity_report.py`;
- the future Codex C implementation handoff; and
- the future Codex E contract-test report.

Truth boundary:

- A synthetic tailer test may prove only that current `FileTailer` detects one
  size-shrink/replacement shape and reads replacement content from the
  beginning.
- A synthetic stream test may prove only that current `MtgaEventStream`
  publishes a sanitized `LogFileRotatedEvent` when a rotated batch is
  observed.
- A schema snapshot may prove only that the committed event class/payload shape
  remains compatible.
- Corpus parity may claim `parser_behavior_verified` only for the reduced
  tailer/stream packet described above.
- Corpus parity must not claim live file-system watcher correctness, robust
  log-rotation resilience, file identity tracking, duplicate/replay
  prevention, recycle/rollback truth, private smoke success, parser support,
  live Player.log health, analytics truth, AI truth, coaching truth, release
  readiness, production behavior, #388/#381 activation, tracker completion, or
  full corpus parity.

## Bridge-Code Status

`bridge_code`

Source project area: Parser / log runtime support.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
repo-owned synthetic tailer/stream tests
  -> focused behavior assertions
  -> corpus manifest/session-ledger behavior metadata
  -> corpus parity readiness metrics
```

Forbidden reverse flow:

- Corpus readiness must not change tailer, stream, event, parser, diagnostics,
  drift, golden replay, feature-equity, evidence-ledger, runtime, workbook,
  webhook, Apps Script, analytics, AI, coaching, CI, merge, deploy, production,
  or final integration behavior.
- Corpus metadata must not create live rotation facts absent from focused
  temp-file/fake-tailer tests.
- Corpus metadata must not turn `TailBatch.rotated`, `LogFileRotatedEvent`,
  temp-file writes, fake-tailers, schema snapshots, diagnostics, drift reports,
  unknown-entry reports, public taxonomy labels, private app-data, or local
  runtime artifacts into broad log-rotation support.
- Corpus metadata must not move file-system truth, watcher truth,
  recycle/rollback truth, duplicate/replay truth, analytics, AI, coaching,
  workbook, webhook, or Apps Script interpretation into parser truth.

Protected surfaces explicitly not touched:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- router semantics;
- tailer behavior;
- stream behavior;
- `LogFileRotatedEvent` shape;
- diagnostics report shape;
- drift report behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- runtime status files or schema;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- failed posts;
- workbook exports;
- SQLite/local app behavior;
- analytics truth;
- AI/model-provider behavior;
- coaching behavior;
- CI gates;
- merge readiness;
- deploy readiness;
- production behavior;
- final integration policy.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_log_runtime_rotation_behavior_readiness.md`

Future Codex C files authorized only if implementation is selected:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- `tests/test_corpus_parity_report.py`;
- `docs/implementation_handoffs/parser_corpus_log_runtime_rotation_behavior_readiness_comparison.md`;
- `docs/contract_test_reports/parser_corpus_log_runtime_rotation_behavior_readiness.md`.

Future Codex C may inspect and cite, but must not modify unless it routes back
for a contract loopback:

- `src/mythic_edge_parser/log/tailer.py`;
- `src/mythic_edge_parser/stream.py`;
- `src/mythic_edge_parser/events.py`;
- `tests/test_tailer.py`;
- `tests/test_stream_integration.py`;
- `tests/test_event_schema_snapshots.py`;
- adjacent corpus contracts, handoffs, and reports.

Not owned by this contract:

- tailer semantics;
- stream semantics;
- parser event class definitions;
- live watcher behavior;
- private evidence;
- external corpus contents;
- workbook/webhook/App Script/Sheets/analytics/AI/coaching surfaces.

## Public Interface

No runtime public API is added by Codex B.

Future Codex C may add corpus metadata that makes the corpus parity public
report show `log_runtime.rotation` as a reduced synthetic behavior-ready row.
The intended eventual corpus row shape is:

```yaml
scenario_family: "log_runtime.rotation"
coverage_status: "covered_synthetic"
coverage_basis:
  - "parser_behavior_verified"
  - "fixture_metadata_only"
```

The existing report-only entry `log_runtime_rotation_boundary_report_v1`
should remain as historical non-claim metadata unless Codex C has a strong
reason to route back for a replacement or migration contract. A new synthetic
evidence entry should be added rather than rewriting #444's boundary entry into
a behavior claim.

Recommended new manifest entry id:

```text
log_runtime_rotation_synthetic_tailer_stream_v1
```

Recommended new session id:

```text
log_runtime_rotation_synthetic_tailer_stream_v1
```

Recommended `parser_event_families`:

```yaml
parser_event_families:
  - "LogFileRotated"
```

Recommended manifest claim families:

```yaml
parser_claim_families:
  - "synthetic_tailer_size_shrink_rotation_flag"
  - "synthetic_tailer_replacement_content_from_start"
  - "synthetic_stream_log_file_rotated_event_publication"
  - "synthetic_stream_rotation_path_sanitization"
  - "log_file_rotated_event_schema_snapshot"
  - "log_runtime_rotation_synthetic_boundary"
  - "live_watcher_correctness_non_claim"
  - "filesystem_rotation_truth_non_claim"
  - "duplicate_replay_prevention_non_claim"
  - "recycle_or_rollback_non_claim"
  - "private_smoke_non_claim"
  - "readiness_production_non_claim"
  - "analytics_ai_coaching_non_claim"
```

Recommended manifest paths:

```yaml
paths:
  tailer_test: "tests/test_tailer.py"
  stream_integration_test: "tests/test_stream_integration.py"
  event_schema_snapshot_test: "tests/test_event_schema_snapshots.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
```

## Minimum Behavior Evidence

Future uplift requires a dedicated reduced packet. Codex C must not rely on
issue #444 report-only metadata alone.

### Tailer Leg

Required:

- repo-owned temp-file test evidence only;
- `FileTailer.open_from_end(...)` or an equivalent existing public tailer path;
- a prior offset greater than the replacement file size;
- replacement content written to the same temp path;
- `TailBatch.rotated is True`;
- replacement content is read from the beginning after rotation;
- no private Player.log, UTC_Log, live MTGA, app-data, watcher, network,
  firewall, packet, OS/router, or private smoke input.

Allowed:

- existing `tests/test_tailer.py::test_poll_reports_rotation_and_reads_replacement_content`
  may be cited if Codex C proves it still covers the required behavior;
- Codex C may add only focused corpus metadata/tests if no tailer test change
  is needed.

Not sufficient:

- file append behavior;
- open-from-start/open-from-end behavior without size-shrink rotation;
- invalid UTF-8 behavior;
- missing-file sanitized error behavior;
- private filesystem checks;
- external corpus metadata.

### Stream Leg

Required:

- repo-owned fake-tailer or temp-file test evidence only;
- a `TailBatch` with `rotated=True`;
- a published `LogFileRotatedEvent`;
- payload `type == "log_file_rotated"`;
- payload path is sanitized to a display name and does not include a private
  absolute path;
- `EventMetadata.empty()` or equivalent no-raw-log metadata for the rotation
  event;
- no live watcher, production stream, private Player.log, UTC_Log, app-data,
  network, or private smoke input.

Allowed:

- existing
  `tests/test_stream_integration.py::test_stream_emits_rotated_event_with_sanitized_log_path`
  may be cited if Codex C proves it still covers the required behavior;
- `tests/test_event_schema_snapshots.py` may be cited for event class/payload
  shape compatibility.

Not sufficient:

- generic stream entry routing;
- detailed logging status events;
- fake tailer with no rotated batch;
- runtime status or diagnostics summaries;
- production stream execution.

### Required Non-Claims

Every manifest/session-ledger entry and implementation handoff must preserve
these non-claims:

- no live file-system watcher correctness;
- no robust log-rotation resilience;
- no file identity tracking truth;
- no duplicate/replay prevention truth;
- no recycle/rollback truth;
- no private smoke success;
- no parser support;
- no live Player.log health;
- no release readiness;
- no deploy readiness;
- no production behavior;
- no analytics truth;
- no AI truth;
- no coaching truth;
- no #388/#381 activation;
- no tracker completion;
- no full corpus parity.

## Behavior-Readiness Packet

This row's reusable packet is:

```yaml
scenario_family: "log_runtime.rotation"
current_status: "covered_report_only"
current_basis:
  - "fixture_metadata_only"
target_status_if_successful: "covered_synthetic"
parser_behavior_verified_may_be_added: true
evidence_type: "synthetic"
fixture_or_test_route:
  preferred: "existing focused tailer and stream tests plus corpus metadata"
  optional: "new focused tests only if existing assertions are insufficient"
fixture_golden_replay_changes:
  allowed: []
  forbidden:
    - "private Player.log or external corpus contents"
    - "live filesystem watcher fixture"
    - "fixture that claims recycle/rollback or duplicate/replay truth"
manifest_session_ledger_changes:
  allowed:
    - "add log_runtime_rotation_synthetic_tailer_stream_v1"
    - "preserve log_runtime_rotation_boundary_report_v1 as report-only history"
  forbidden:
    - "rewrite #444 boundary entry into behavior evidence"
    - "promote drift_debug.rename_or_rotation_collision"
    - "promote drift_debug.recycle_or_rollback"
    - "promote log_runtime.unknown_entry"
    - "promote unrelated rows"
parser_behavior_changes_allowed: false
tailer_stream_behavior_changes_allowed: false
private_external_inputs_forbidden: true
required_non_claims:
  - "live_file_system_watcher_correctness"
  - "robust_log_rotation_resilience"
  - "file_identity_tracking_truth"
  - "duplicate_replay_prevention_truth"
  - "recycle_or_rollback_truth"
  - "private_smoke_success"
  - "parser_support"
  - "release_readiness"
  - "production_behavior"
  - "analytics_truth"
  - "ai_truth"
  - "coaching_truth"
focused_validation_commands:
  - "PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_event_schema_snapshots.py tests/test_corpus_parity_report.py"
  - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
stop_conditions_for_issue_388_381_activation:
  - "do not activate #388/#381"
  - "do not mark pipeline_activation_ready_for_issue_388 true"
  - "do not close tracker #158"
```

This packet is a pattern note for future behavior-readiness rows, but this
contract applies it only to `log_runtime.rotation`.

## Compatibility Expectations

- Existing #444 report-only boundary must remain readable and testable.
- Existing `drift_debug.rename_or_rotation_collision` report-only coverage
  must remain scoped to collision-boundary metadata and must not become
  rotation behavior evidence.
- Existing `drift_debug.recycle_or_rollback` blocked-external-boundary status
  must remain unchanged unless a separate contract authorizes it.
- Existing `log_runtime.unknown_entry` report-only coverage must remain scoped
  to unknown-entry drift/diagnostics metadata.
- Readiness metrics may count this row as parser-behavior-ready only after the
  family's winning status is `covered_synthetic` and its coverage basis
  includes `parser_behavior_verified`.
- `pipeline_activation_ready_for_issue_388` must remain false unless every
  separately required readiness gate is satisfied by later contracts.
- Public reports must continue to sanitize private paths, raw logs, secrets,
  runtime artifacts, failed posts, workbook exports, private reports, and
  external corpus contents.

## Validation Obligations For Codex C

Codex C must produce:

- a comparison handoff at
  `docs/implementation_handoffs/parser_corpus_log_runtime_rotation_behavior_readiness_comparison.md`;
- a contract-test report at
  `docs/contract_test_reports/parser_corpus_log_runtime_rotation_behavior_readiness.md`;
- focused evidence tying the reduced packet to existing tailer and stream
  tests;
- corpus metadata tests proving the intended manifest and session-ledger
  changes;
- explicit evidence that `drift_debug.rename_or_rotation_collision`,
  `drift_debug.recycle_or_rollback`, and `log_runtime.unknown_entry` are not
  reinterpreted; and
- clean git status with no private/generated artifacts.

Minimum validation commands:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_event_schema_snapshots.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 tools/select_validation.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Codex C may narrow or expand focused tests only if it explains why in the
handoff. Any source behavior changes require route-back before implementation.

## Acceptance Criteria

Future implementation is acceptable only if:

- `log_runtime.rotation` has a new synthetic behavior entry;
- the row's winning status becomes `covered_synthetic` only with
  `parser_behavior_verified`;
- tailer and stream reduced packet evidence is cited or added through focused
  tests;
- the old report-only boundary entry remains report-only or is migrated only
  through an explicit contract loopback;
- all required non-claims are present in metadata, handoff, and report;
- `drift_debug.rename_or_rotation_collision` remains report-only;
- `drift_debug.recycle_or_rollback` remains blocked external-boundary;
- `log_runtime.unknown_entry` remains report-only;
- #388/#381 remain inactive; and
- no protected parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  surfaces are changed.

Route back to Codex B or Codex A if:

- existing tests cannot prove the reduced packet without tailer/stream source
  changes;
- the only available evidence is #444 report-only metadata;
- a fixture would require private or external raw logs;
- the implementation would need to claim live watcher correctness,
  recycle/rollback truth, file identity tracking, duplicate/replay prevention,
  private smoke success, production behavior, or parser support; or
- validation changes would touch protected surfaces.

## Recommended Next Role

Codex C: Module Implementer.

Codex C should implement metadata/test/docs only. It should not implement
tailer, stream, event, parser, diagnostics, drift, runtime, or downstream
behavior changes.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #502.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/502

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/500

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/501

Previous merge commit:
28b588767c017aa2290121d2a8d21656eb49d905

Base branch:
main

Contract:
docs/contracts/parser_corpus_log_runtime_rotation_behavior_readiness.md

Goal:
Implement the smallest metadata/test/docs change needed to satisfy the
log-runtime rotation behavior-readiness contract for `log_runtime.rotation`.

Required implementation boundary:
- Add a dedicated reduced synthetic tailer/stream behavior packet.
- Prove or cite the tailer leg: size-shrink replacement content produces
  `TailBatch.rotated is True` and reads replacement content from the beginning.
- Prove or cite the stream leg: a rotated tail batch publishes sanitized
  `LogFileRotatedEvent` with no raw/private path.
- Cite `tests/test_event_schema_snapshots.py` for event shape compatibility if
  useful.
- Add or update corpus manifest/session-ledger metadata so the row may move
  from `covered_report_only` to `covered_synthetic` only with
  `parser_behavior_verified`.
- Preserve `log_runtime_rotation_boundary_report_v1` as report-only historical
  boundary metadata unless you route back for a contract loopback.
- Do not use `drift_debug.rename_or_rotation_collision`,
  `drift_debug.recycle_or_rollback`, or `log_runtime.unknown_entry` evidence
  as rotation behavior-readiness support.
- Do not change tailer, stream, event, parser, diagnostics, drift, runtime, or
  downstream behavior.

Expected files:
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_log_runtime_rotation_behavior_readiness_comparison.md
- docs/contract_test_reports/parser_corpus_log_runtime_rotation_behavior_readiness.md

Do not:
- Activate #388 / #381.
- Close #158, #388, #434, or #502.
- Promote blocked or unrelated report-only rows.
- Change parser behavior, tailer behavior, stream behavior, event classes,
  router semantics, diagnostics behavior, drift behavior, golden replay
  behavior, feature-equity behavior, evidence-ledger behavior, analytics
  behavior, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets sync, output transport, CI gates, merge readiness, deploy
  readiness, production behavior, or final integration policy.
- Run private Player.log, UTC_Log, live MTGA, log-rotation, filesystem
  watcher, network, or private smoke checks.
- Import, copy, mirror, summarize, or commit Manasight raw logs, compressed
  corpus files, parser source, external corpus contents, private logs,
  generated/runtime artifacts, workbook exports, secrets, tokens, API keys,
  webhook URLs, decklists, card choices, screenshots, private strategy notes,
  private reports, exact private paths, exact offsets, exact file sizes, raw
  hashes, or local-only artifacts.
- Claim live log-rotation support, watcher correctness, tailer correctness
  beyond the reduced packet, stream production readiness, file identity
  tracking, duplicate/replay prevention, recycle/rollback truth, parser
  support, release readiness, production behavior, analytics truth, AI truth,
  coaching truth, tracker completion, or full corpus parity.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_event_schema_snapshots.py tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- run path-scoped secret/protected-surface checks for changed files
- git diff --check

End with:
- files changed
- reduced log-runtime rotation evidence added or cited
- validation run
- remaining risks/open questions
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/502"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/500"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/501"
  previous_merge_commit: "28b588767c017aa2290121d2a8d21656eb49d905"
  completed_thread: "B"
  next_thread: "C"
  base_branch: "main"
  selected_family: "log_runtime.rotation"
  prior_status: "covered_report_only"
  authorized_target_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  target_contract: "docs/contracts/parser_corpus_log_runtime_rotation_behavior_readiness.md"
  expected_implementation_handoff: "docs/implementation_handoffs/parser_corpus_log_runtime_rotation_behavior_readiness_comparison.md"
  expected_contract_test_report: "docs/contract_test_reports/parser_corpus_log_runtime_rotation_behavior_readiness.md"
  verdict: "reduced_synthetic_log_runtime_rotation_behavior_readiness_authorized"
  risk_tier: "High"
  stop_conditions:
    - "Do not activate #388 / #381."
    - "Do not close #158, #388, #434, or #502."
    - "Do not promote blocked or unrelated report-only rows."
    - "Do not claim live log-rotation support, watcher correctness, duplicate/replay prevention, recycle/rollback truth, parser support, readiness, production behavior, analytics truth, AI truth, coaching truth, tracker completion, or full corpus parity."
    - "Do not change parser behavior, tailer behavior, stream behavior, event classes, diagnostics behavior, drift behavior, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, coaching truth, CI gates, deploy policy, production behavior, or final integration policy."
```
