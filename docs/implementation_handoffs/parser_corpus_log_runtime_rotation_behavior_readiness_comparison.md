# Parser Corpus Log Runtime Rotation Behavior Readiness Handoff

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/502
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/500
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/501
- Previous merge commit: `28b588767c017aa2290121d2a8d21656eb49d905`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/444
- Branch: `codex/parser-corpus-log-runtime-rotation-behavior-readiness-502`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_log_runtime_rotation_behavior_readiness.md`
- Risk tier: High

## Contract Comparison

The contract authorized a metadata/test/docs-only uplift for
`log_runtime.rotation` if a reduced synthetic tailer/stream packet could be
proved through existing behavior. The implementation satisfies that narrow
packet by citing existing focused tests:

- `tests/test_tailer.py::test_poll_reports_rotation_and_reads_replacement_content`
  proves size-shrink rotation detection and replacement-content reading from
  the beginning for a repo-owned temp file.
- `tests/test_stream_integration.py::test_stream_emits_rotated_event_with_sanitized_log_path`
  proves a rotated tail batch publishes `LogFileRotatedEvent` with a sanitized
  display path and empty raw metadata.
- `tests/test_event_schema_snapshots.py` keeps the `LogFileRotatedEvent`
  sample payload shape pinned.

No tailer, stream, event, parser, diagnostics, drift, golden replay,
feature-equity, evidence-ledger, analytics, workbook, webhook, Apps Script,
or output behavior was changed.

## Changes Made

- Added `log_runtime_rotation_synthetic_tailer_stream_v1` to
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added `log_runtime_rotation_synthetic_tailer_stream_v1` to
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_corpus_parity_report.py` to pin the new manifest row,
  session-ledger row, status movement, readiness count movement, matrix row,
  adjacent-row non-promotion, and non-claims.
- Added this implementation handoff.
- Added
  `docs/contract_test_reports/parser_corpus_log_runtime_rotation_behavior_readiness.md`.

The #444 `log_runtime_rotation_boundary_report_v1` entry remains present and
report-only. The new synthetic entry is additive.

## Status Movement

Only one scenario family changed status:

| Scenario family | Before | After |
| --- | --- | --- |
| `log_runtime.rotation` | `covered_report_only` | `covered_synthetic` |

Current corpus parity summary after the change:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 21
covered_report_only: 12
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
parser_behavior_ready_family_count: 26
pipeline_activation_ready_for_issue_388: false
pipeline_activation_blockers:
  - "report_only_families:12"
  - "blocked_private_evidence_families:2"
  - "blocked_external_boundary_families:4"
```

The corpus is still not parser-behavior ready and does not activate #388 or
#381.

## Preserved Boundaries

- No parser behavior, tailer behavior, stream behavior, event classes, router
  semantics, diagnostics, drift, golden replay, feature-equity,
  evidence-ledger, analytics behavior, workbook schema, webhook payload shape,
  Apps Script behavior, Google Sheets sync, output transport, CI gates, merge
  readiness, deploy readiness, production behavior, or final integration
  policy changed.
- No private Player.log, UTC_Log, live MTGA, live log-rotation check,
  filesystem watcher check, network check, private smoke output, Manasight raw
  log, external corpus input, generated data, SQLite artifact, runtime
  artifact, workbook export, secret, credential, token, API key, webhook URL,
  exact private path, exact private offset, exact private file size, or raw hash
  was used.
- `drift_debug.rename_or_rotation_collision` remains report-only.
- `drift_debug.recycle_or_rollback` remains blocked external-boundary.
- `log_runtime.unknown_entry` remains report-only.
- The new evidence does not claim live log-rotation support, watcher
  correctness, tailer correctness beyond the reduced packet, stream production
  readiness, file identity tracking, duplicate/replay prevention,
  recycle/rollback truth, parser support, release readiness, production
  behavior, analytics truth, AI truth, coaching truth, tracker completion, or
  full corpus parity.

## Validation Run

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
  passed: 7 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_event_schema_snapshots.py tests/test_corpus_parity_report.py`
  passed: 24 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=21, report_only=12, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  completed with `selection_status: ok`: changed paths 6, required 5,
  recommended 1, warnings 0.
- Path-scoped secret/private-marker scan passed: scanned paths 6, forbidden 0,
  warnings 0.
- Path-scoped protected-surface scan passed: changed paths 6, forbidden 0,
  warnings 0.
- `git diff --check` passed.

## Residual Risks

- The evidence is synthetic and proves only one reduced tailer/stream packet.
- It does not prove live file-system watcher correctness, robust
  log-rotation resilience, file identity tracking, duplicate/replay
  prevention, recycle/rollback truth, private smoke success, live Player.log
  health, parser support, release readiness, deploy readiness, production
  behavior, analytics truth, AI truth, coaching truth, tracker completion, or
  full corpus parity.
- Remaining report-only, private-evidence, and external-boundary rows keep the
  overall corpus from parser-behavior readiness.

## Reviewer Focus

Codex E should verify:

- no tailer, stream, event, or parser source files changed;
- the existing focused tests truly cover the reduced packet;
- `log_runtime_rotation_boundary_report_v1` remains report-only;
- `drift_debug.rename_or_rotation_collision`, `drift_debug.recycle_or_rollback`,
  and `log_runtime.unknown_entry` are not promoted or reinterpreted;
- readiness metrics move exactly one family from report-only to synthetic;
- #388/#381 activation remains false/deferred; and
- no private/external/raw/generated artifacts are present.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #502, log-runtime rotation
behavior-readiness under tracker #158.

Review:
- docs/contracts/parser_corpus_log_runtime_rotation_behavior_readiness.md
- tests/test_tailer.py
- tests/test_stream_integration.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_log_runtime_rotation_behavior_readiness_comparison.md
- docs/contract_test_reports/parser_corpus_log_runtime_rotation_behavior_readiness.md

Verify that log_runtime.rotation is promoted only by the additive
log_runtime_rotation_synthetic_tailer_stream_v1 metadata, that the existing
tailer, stream, and event schema tests prove only the reduced synthetic packet,
that log_runtime_rotation_boundary_report_v1 remains report-only non-claim
metadata, and that drift_debug.rename_or_rotation_collision,
drift_debug.recycle_or_rollback, and log_runtime.unknown_entry remain separate
adjacent rows.

Do not target main directly. Do not close tracker #158, #388, #434, or #502.
Do not activate #388 or #381. Do not run private/live checks. Do not claim live
log-rotation support, watcher correctness, tailer correctness beyond the
reduced packet, stream production readiness, file identity tracking,
duplicate/replay prevention, recycle/rollback truth, parser support, release
readiness, production behavior, analytics truth, AI truth, coaching truth,
tracker completion, or full corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/502"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/500"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/501"
  previous_merge_commit: "28b588767c017aa2290121d2a8d21656eb49d905"
  completed_thread: "C"
  next_thread: "E"
  base_branch: "main"
  selected_family: "log_runtime.rotation"
  prior_status: "covered_report_only"
  target_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  source_artifact: "docs/contracts/parser_corpus_log_runtime_rotation_behavior_readiness.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_log_runtime_rotation_behavior_readiness_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_log_runtime_rotation_behavior_readiness.md"
  verdict: "reduced_synthetic_log_runtime_rotation_behavior_readiness_ready_for_review"
  risk_tier: "High"
```
