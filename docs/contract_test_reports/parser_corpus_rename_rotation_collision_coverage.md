# Parser Corpus Rename Rotation Collision Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/416
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/414
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/415
- previous_merge_commit: `c0691fa4e53198179a76efdd5f05b33390f817ff`
- contract: `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- branch: `codex/parser-corpus-rename-rotation-collision-coverage`
- base_branch: `codex/parser-parity`
- selected_path: `covered_report_only_boundary`
- risk_tier: High

## Source Snapshot

PR #415 is merged into `codex/parser-parity`, and the local implementation
branch starts at the required merge commit:

- local HEAD before implementation:
  `c0691fa4e53198179a76efdd5f05b33390f817ff`
- merge-base ancestry check: passed
- issue #416 state: open
- tracker #158 state: open

Pre-change corpus parity summary:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 11
- partial: 3
- missing: 5
- blocked_private_evidence: 1
- blocked_external_boundary: 5

Pre-change rename/rotation collision row:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `drift_debug.rename_or_rotation_collision` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single report-only boundary metadata path authorized by the
contract:

- manifest entry: `rename_rotation_collision_boundary_report_v1`
- session ledger entry: `rename_rotation_collision_boundary_report_v1`
- entry type: `session_ledger_entry`
- source kind: `committed_count_only_report`
- commit status: `committed`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- scenario family: `drift_debug.rename_or_rotation_collision`
- coverage status: `covered_report_only`
- coverage basis:
  - `fixture_metadata_only`
- parser event families: none
- parser claim families:
  - `rename_rotation_collision_boundary_report`
  - `tailer_rotation_not_collision_truth`
  - `log_runtime_rotation_not_collision_truth`
  - `recycle_or_rollback_not_collision_truth`
  - `unknown_entry_not_collision_truth`
  - `timestamp_anomaly_not_collision_truth`
  - `missing_message_type_not_collision_truth`
  - `file_system_truth_non_claim`
  - `duplicate_replay_prevention_non_claim`

The committed metadata is a boundary report only. It is not a file-system
fixture, not a parser behavior claim, not a watcher behavior claim, and not
evidence of rename/rotation collision support, log-rotation truth, live
file-system truth, file identity tracking truth, rename/recycle collision
handling, duplicate/replay prevention, parser drift recovery truth, private
smoke success, live watcher correctness, release readiness, production
behavior, analytics truth, AI truth, coaching truth, or full corpus parity.

No parser source, parser behavior, file tailer/watcher behavior, log discovery
behavior, stream behavior, router behavior, diagnostics behavior, log-drift
behavior, golden replay behavior, feature-equity behavior, evidence-ledger
behavior, runtime behavior, analytics behavior, workbook behavior, webhook
behavior, Apps Script behavior, AI/coaching behavior, CI behavior, merge
policy, deploy policy, release policy, production behavior, raw log fixture,
private smoke artifact, generated artifact, file-system fixture, decklist,
card-choice artifact, strategy note, or external corpus content was changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 12
- partial: 3
- missing: 4
- blocked_private_evidence: 1
- blocked_external_boundary: 5

Post-change row:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `drift_debug.rename_or_rotation_collision` | `covered_report_only` | `fixture_metadata_only` | `rename_rotation_collision_boundary_report_v1` |

Adjacent rows preserved:

| scenario_family | status |
| --- | --- |
| `log_runtime.rotation` | `blocked_external_boundary` |
| `drift_debug.recycle_or_rollback` | `blocked_external_boundary` |
| `drift_debug.missing_message_type` | `covered_report_only` |
| `drift_debug.phantom_or_deck_origin` | `missing` |
| `mythic_edge.private_log_report_only_drift` | `missing` |

## Privacy And Protected-Surface Assertions

- No raw Player.log excerpts were added.
- No Manasight raw logs, external corpus content, private local logs, private
  smoke outputs, generated data, SQLite databases, runtime artifacts, failed
  posts, workbook exports, credentials, tokens, API keys, webhook URLs,
  decklists, deck names, card choices, sideboard choices, strategy notes, or
  private reports were committed.
- No parser source, parser event schema, file tailer/watcher behavior, log
  discovery behavior, stream behavior, diagnostics, log-drift, golden replay,
  feature-equity, evidence-ledger, workbook, webhook, Apps Script, analytics,
  AI, coaching, runtime, CI, merge, deploy, release, or production surface was
  changed.

## Explicit Non-Claims

- This report does not claim full Mythic Edge corpus parity.
- This report does not claim rename/rotation collision support.
- This report does not claim log-rotation truth or live file-system truth.
- This report does not claim file identity tracking truth.
- This report does not claim rename/recycle collision handling.
- This report does not claim duplicate/replay prevention.
- This report does not claim private smoke success or production watcher
  support.
- This report does not claim support from tailer/stream rotation signals,
  log-runtime rotation boundaries, recycle/rollback boundaries, unknown-entry
  reporting, timestamp anomaly reporting, missing-message-type coverage,
  diagnostics, log-drift reports, golden replay, feature-equity, corpus parity
  metadata, or public taxonomy metadata alone.
- This report does not claim release readiness, deploy readiness, merge
  readiness, production behavior, analytics truth, AI truth, or coaching truth.
- This report does not claim issue closure or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md`

## Codex E Contract-Test Review

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The package moves only
`drift_debug.rename_or_rotation_collision` from `missing` to
`covered_report_only` with `coverage_basis` exactly
`["fixture_metadata_only"]`, one Mythic Edge entry
`rename_rotation_collision_boundary_report_v1`, and no parser event families.

The manifest and session ledger preserve the required report-only boundary:
the session ledger records zero dedicated rename/rotation collision fixtures,
zero file identity tracking claims, zero rename collision detection claims,
zero recycle collision detection claims, zero duplicate/replay prevention
claims, zero private smoke success claims, and zero production watcher support
claims. The reference counts for tailer rotation, stream rotation events,
log-drift, diagnostics, golden replay, and feature-equity are documented only as
adjacent context and do not become parser or file-system truth.

Adjacent rows remain separate and unchanged in meaning:

| scenario_family | status |
| --- | --- |
| `log_runtime.rotation` | `blocked_external_boundary` |
| `drift_debug.recycle_or_rollback` | `blocked_external_boundary` |
| `drift_debug.missing_message_type` | `covered_report_only` |
| `drift_debug.phantom_or_deck_origin` | `missing` |
| `mythic_edge.private_log_report_only_drift` | `missing` |

### Validation Results

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
  - passed, 7 tests
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  - passed, `partial_coverage_map_ready` with 45 families, 6 committed, 4 missing
- `python3 tools/check_agent_docs.py`
  - passed, 32 checked files, 0 errors, 0 warnings
- `python3 -m ruff check src tests tools`
  - passed
- `git diff --check`
  - passed
- `PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_tailer_router_integration.py`
  - passed, 12 tests
- Path-scoped changed-file secret/private marker scan
  - passed, 6 scanned paths, 0 forbidden, 0 warnings
- Path-scoped changed-file protected-surface gate
  - passed, 6 changed paths, 0 forbidden, 0 warnings
- Path-scoped validation selector sanity check
  - passed, `selection_status: ok`

### Protected-Surface Status

No protected downstream behavior changed. The changed package is limited to:

- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- `docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`

There are no changes under parser source, tools, CI, tailer/stream tests,
diagnostics, log-drift, golden replay, feature-equity, runtime, workbook,
webhook, Apps Script, analytics, AI/coaching, generated data, raw logs,
runtime status files, failed posts, workbook exports, or production surfaces.

### Remaining Risks

This remains report-only boundary coverage. It does not prove rename/rotation
collision support, live file-system truth, file identity tracking, rename or
recycle collision detection, duplicate/replay prevention, private smoke
success, watcher correctness, release readiness, production behavior, analytics
truth, AI truth, coaching truth, or full corpus parity.

### Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/416"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/414"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/415"
  previous_merge_commit: "c0691fa4e53198179a76efdd5f05b33390f817ff"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md"
  target_artifact: "draft PR for rename/rotation collision report-only boundary"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-rename-rotation-collision-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_tailer_router_integration.py"
    - "path-scoped secret/private marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector sanity check for changed files"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #416 or tracker #158 unless separately authorized."
    - "Do not use report-only coverage as parser, file-system, tailer, watcher, log-rotation, rename collision, recycle collision, duplicate/replay prevention, private smoke, release, production, analytics, AI, coaching, or full-parity authority."
    - "Do not promote this family beyond report-only boundary metadata without a new contract."
    - "Do not reinterpret tailer rotation, stream rotation events, log_runtime.rotation, recycle_or_rollback, missing_message_type, timestamp anomaly, unknown-entry, diagnostics, log-drift, golden replay, feature-equity, corpus metadata, or public taxonomy metadata as dedicated rename/rotation collision support without a new contract."
    - "Do not change parser behavior, parser event classes, tailer/watcher behavior, log discovery, stream behavior, LogFileRotatedEvent shape, diagnostics report shape, drift report behavior, golden replay behavior, feature-equity behavior, evidence-ledger behavior, runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, CI, merge/deploy policy, release policy, production behavior, analytics truth, AI truth, or coaching truth."
    - "Do not commit raw private logs, local logs, file path identities, file hashes, byte-size lists, capture-date rows, private smoke outputs, generated/runtime artifacts, SQLite files, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, card choices, strategy notes, or external corpus content."
```
