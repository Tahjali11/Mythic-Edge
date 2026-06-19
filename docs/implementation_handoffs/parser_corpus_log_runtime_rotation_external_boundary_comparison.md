# Parser Corpus Log Runtime Rotation External Boundary Comparison

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/444
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Parent/private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/442
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/443
- Previous merge commit: `32b11c3238b1d572213c5953708f19aa359a2c2f`
- Branch: `codex/parser-corpus-log-runtime-rotation-boundary-444`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`
- Selected family: `log_runtime.rotation`
- Deferred family: `drift_debug.recycle_or_rollback`
- Risk tier: High

## Contract Comparison

Before this pass, `log_runtime.rotation` was covered only through the broad
`external_reference_category_boundary` entry with
`blocked_external_boundary` status. The contract selected a narrow
report-only metadata path for that single family, based on committed tailer
and stream rotation reference surfaces, without treating those surfaces as
runtime correctness or readiness evidence.

The implementation now gives `log_runtime.rotation` a dedicated
`log_runtime_rotation_boundary_report_v1` manifest and session-ledger entry.
It removes only `log_runtime.rotation` from
`external_reference_category_boundary`. The broad external-reference entry
still covers `timer.inactivity_timeout`, `gameplay_stress.conjure`,
`gameplay_stress.spellbook`, and `drift_debug.recycle_or_rollback`.

## Files Changed

- Updated `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Updated `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_corpus_parity_report.py`.
- Added
  `docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md`.
- Added
  `docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md`.

The Codex B contract is present at
`docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`.

## Behavior Boundaries

No parser, tailer, stream, event, diagnostics, drift, golden replay,
feature-equity, evidence-ledger, workbook, webhook, Apps Script, Sheets,
analytics, AI, coaching, CI, merge, deploy, production, or final integration
behavior changed.

No private logs, live MTGA checks, file-system rotation checks, watcher
checks, drift checks, diagnostics checks, or private smoke checks were run.

## Validation Run

- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed: `partial_coverage_map_ready` with 45 families, 6 committed, 0
  missing.
- Row query confirmed:
  - `log_runtime.rotation`: `covered_report_only`,
    `["fixture_metadata_only"]`, `["log_runtime_rotation_boundary_report_v1"]`
  - `drift_debug.recycle_or_rollback`: `blocked_external_boundary`
  - `timer.inactivity_timeout`: `blocked_external_boundary`
  - `connection.firewall_or_network_drop`: `blocked_private_evidence`
  - `mythic_edge.private_log_report_only_drift`:
    `blocked_private_evidence`
- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_tailer.py tests/test_stream_integration.py tests/test_stream_unit.py tests/test_event_schema_snapshots.py`
  passed: 25 tests.
- `python3 tools/check_agent_docs.py` passed: 34 checked files, 0 errors,
  0 warnings.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- New-file whitespace checks for the contract, handoff, and report passed.
- Path-scoped secret/private marker scan passed: 6 scanned paths, 0
  forbidden, 0 warnings.
- Path-scoped protected-surface gate passed: 6 changed paths, 0 forbidden,
  0 warnings.
- ASCII scan returned no matches for the changed files.
- Trailing-whitespace scan returned no matches for the changed files.
- Generated SQLite artifact scan returned no matches.

## Residual Risks

- `log_runtime.rotation` is only `covered_report_only`; it is not parser
  support, live watcher correctness, file-system rotation truth,
  duplicate/replay prevention, recycle/rollback truth, private smoke success,
  release readiness, production behavior, analytics truth, AI truth, coaching
  truth, or full corpus parity.
- `drift_debug.recycle_or_rollback` remains `blocked_external_boundary`.
- `connection.firewall_or_network_drop` and
  `mythic_edge.private_log_report_only_drift` remain
  `blocked_private_evidence`.
- Future live or private evidence still requires a separate approved issue,
  contract, and review.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #444, log_runtime.rotation
external-boundary metadata, under tracker #158.

Review:
- docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md
- docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md

Verify that only log_runtime.rotation moved to dedicated covered_report_only
metadata, drift_debug.recycle_or_rollback remains blocked_external_boundary,
private-evidence rows remain blocked_private_evidence, no runtime behavior
changed, no private/live/file-system checks were run, and the non-claims are
preserved.

Lead with findings. If no issues are found, say so and record residual risks.

Do not target main directly. Do not close #158, #434, or #444. Do not run
private/live/file-system rotation checks. Do not claim parser support, watcher
correctness, log-rotation resilience, recycle/rollback truth, private smoke
success, readiness, production behavior, analytics truth, AI truth, coaching
truth, or full corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/444"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/442"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/443"
  previous_merge_commit: "32b11c3238b1d572213c5953708f19aa359a2c2f"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md"
  report_artifact: "docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md"
  verdict: "log_runtime_rotation_report_only_metadata_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-log-runtime-rotation-boundary-444"
  base_branch: "main"
  selected_family: "log_runtime.rotation"
  deferred_family: "drift_debug.recycle_or_rollback"
  status_decision: "covered_report_only_boundary_metadata"
  tracker_status: "open"
  parent_issue_status: "open"
```
