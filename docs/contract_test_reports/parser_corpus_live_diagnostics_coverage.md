# Parser Corpus Live Diagnostics Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/420
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/418
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/419
- previous_merge_commit: `5180de4b5900dc4bfd895d394d1a5ac74994c4b4`
- contract: `docs/contracts/parser_corpus_live_diagnostics_coverage.md`
- branch: `codex/parser-corpus-live-diagnostics-coverage`
- base_branch: `codex/parser-parity`
- selected_path: `covered_report_only`
- risk_tier: High

## Source Snapshot

PR #419 is merged into `codex/parser-parity`, and the local implementation
branch starts at the required merge commit:

- local HEAD before implementation:
  `5180de4b5900dc4bfd895d394d1a5ac74994c4b4`
- merge-base ancestry check: passed
- issue #420 state: open
- tracker #158 state: open

Pre-change corpus parity summary:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 13
- partial: 3
- missing: 3
- blocked_private_evidence: 1
- blocked_external_boundary: 5

Pre-change live-diagnostics row:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `mythic_edge.live_diagnostics` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single report-only boundary metadata path authorized by the contract:

- manifest entry: `live_diagnostics_boundary_report_v1`
- session ledger entry: `live_diagnostics_boundary_report_v1`
- entry type: `session_ledger_entry`
- source kind: `committed_count_only_report`
- commit status: `committed`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- scenario family: `mythic_edge.live_diagnostics`
- coverage status: `covered_report_only`
- coverage basis:
  - `diagnostics_only`
  - `fixture_metadata_only`
- parser event families: none
- parser claim families:
  - `live_diagnostics_boundary_report`
  - `parser_diagnostics_not_live_health_truth`
  - `live_watcher_diagnostics_not_watcher_correctness_truth`
  - `live_capture_status_not_game_truth`
  - `evidence_review_status_not_live_arena_truth`
  - `status_api_not_release_readiness`
  - `log_drift_not_private_smoke_truth`
  - `analytics_ai_coaching_non_claim`

The committed metadata is a boundary report only. It is not private smoke
evidence, live Player.log health proof, watcher correctness proof, parser
support for a live run, status API correctness as release readiness,
production behavior, analytics readiness, AI/coaching readiness, or full
corpus parity.

No parser source, parser behavior, diagnostics behavior, watcher behavior,
live-capture behavior, status API behavior, evidence review status behavior,
log-drift behavior, golden replay behavior, feature-equity behavior, runtime
status schema, analytics behavior, workbook behavior, webhook behavior, Apps
Script behavior, AI/coaching behavior, CI behavior, merge policy, deploy
policy, release policy, production behavior, raw log fixture, private smoke
artifact, generated artifact, runtime artifact, SQLite file, workbook export,
operator note, browser smoke report, secret, token, API key, credential, or
webhook URL was added or changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 14
- partial: 3
- missing: 2
- blocked_private_evidence: 1
- blocked_external_boundary: 5

Post-change row:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `mythic_edge.live_diagnostics` | `covered_report_only` | `diagnostics_only`, `fixture_metadata_only` | `live_diagnostics_boundary_report_v1` |

Adjacent rows preserved:

| scenario_family | status |
| --- | --- |
| `mythic_edge.private_log_report_only_drift` | `missing` |
| `mythic_edge.analytics_readiness_labels` | `missing` |
| `log_runtime.unknown_entry` | `covered_report_only` |
| `mythic_edge.evidence_ledger_provenance` | `covered_report_only` |

## Privacy And Protected-Surface Assertions

- No raw Player.log excerpts were added.
- No Manasight raw logs, external corpus content, private local logs, private
  smoke outputs, generated data, SQLite databases, runtime artifacts, runtime
  status files, failed posts, workbook exports, credentials, tokens, API keys,
  webhook URLs, decklists, card choices, strategy notes, operator notes,
  browser smoke reports, or private reports were committed.
- No parser source, parser event schema, diagnostics behavior, watcher
  behavior, live-capture behavior, status API behavior, evidence runtime
  status behavior, log-drift behavior, golden replay, feature-equity,
  workbook, webhook, Apps Script, analytics, AI, coaching, CI, merge, deploy,
  release, or production surface was changed.

## Explicit Non-Claims

- This report does not claim full Mythic Edge corpus parity.
- This report does not claim private smoke success.
- This report does not claim live Player.log health.
- This report does not claim watcher correctness.
- This report does not claim parser support for a live run.
- This report does not claim status API correctness as release readiness.
- This report does not claim production behavior, analytics readiness, AI
  truth, coaching truth, issue closure, or tracker completion.
- This report does not claim support from parser diagnostics, local app
  watcher diagnostics, live-capture heartbeat/no-row diagnostics, evidence
  local status, status API exposure, unknown-entry routing, log-drift
  reports, local status summaries, corpus parity metadata, private operator
  notes, or future browser smoke reports alone.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md`

## Codex E Contract-Test Review

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The package moves only `mythic_edge.live_diagnostics` from `missing` to
`covered_report_only`, with `coverage_basis` exactly
`["diagnostics_only", "fixture_metadata_only"]`, one Mythic Edge entry
`live_diagnostics_boundary_report_v1`, and no parser event families.

The implementation does not add `parser_behavior_verified`, `local_report_only`,
a private local report artifact, committed logs, runtime artifacts, generated
data, SQLite files, workbook exports, secrets, tokens, API keys, or webhook
URLs.

The manifest and session ledger preserve the required report-only boundary:
the session ledger records zero private-smoke success claims, zero live
Player.log health claims, zero watcher-correctness claims, zero parser-support
claims, zero release-readiness claims, zero deploy-readiness claims, zero
production-readiness claims, zero analytics-truth claims, zero AI-truth claims,
and zero coaching-truth claims.

Adjacent rows remain separate and unchanged in meaning:

| scenario_family | status |
| --- | --- |
| `mythic_edge.private_log_report_only_drift` | `missing` |
| `mythic_edge.analytics_readiness_labels` | `missing` |
| `log_runtime.unknown_entry` | `covered_report_only` |
| `mythic_edge.evidence_ledger_provenance` | `covered_report_only` |

### Validation Results

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
  - passed, 7 tests
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  - passed, `partial_coverage_map_ready` with 45 families, 6 committed, 2 missing
- `PYTHONPATH=src python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_diagnostics.py tests/test_log_drift_sensor.py tests/test_evidence_runtime_status.py tests/test_status_api.py`
  - passed, 39 tests
- `python3 tools/check_agent_docs.py`
  - passed, 32 checked files, 0 errors, 0 warnings
- `python3 -m ruff check src tests tools`
  - passed
- `git diff --check`
  - passed
- Path-scoped changed-file secret/private marker scan
  - passed, 6 scanned paths, 0 forbidden, 0 warnings
- Path-scoped changed-file protected-surface gate
  - passed, 6 changed paths, 0 forbidden, 0 warnings
- Path-scoped validation selector sanity check
  - passed, `selection_status: ok`
- Trailing-whitespace scan over changed and untracked package files
  - passed, no matches

### Protected-Surface Status

No protected downstream behavior changed. The changed package is limited to:

- `docs/contracts/parser_corpus_live_diagnostics_coverage.md`
- `docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`

There are no changes under parser source, tools, CI, diagnostics behavior,
watcher behavior, live-capture behavior, status API behavior, evidence runtime
status behavior, log-drift behavior, golden replay, feature-equity, runtime
status schema, workbook, webhook, Apps Script, analytics, AI/coaching,
generated data, raw logs, runtime status files, failed posts, workbook exports,
or production surfaces.

### Remaining Risks

This remains report-only boundary coverage. It does not prove private smoke
success, live Player.log health, watcher correctness, parser support for a live
run, status API correctness as release readiness, production behavior,
analytics readiness, AI truth, coaching truth, issue closure, tracker
completion, or full corpus parity.

### Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/420"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/418"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/419"
  previous_merge_commit: "5180de4b5900dc4bfd895d394d1a5ac74994c4b4"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md"
  target_artifact: "draft PR for live diagnostics report-only boundary"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-live-diagnostics-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_diagnostics.py tests/test_log_drift_sensor.py tests/test_evidence_runtime_status.py tests/test_status_api.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector sanity check for changed files"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #420 or tracker #158 unless separately authorized."
    - "Do not use report-only coverage as private smoke success, live Player.log health, watcher correctness, parser support, release readiness, deploy readiness, production behavior, analytics readiness, AI truth, coaching truth, or full-parity authority."
    - "Do not promote this family beyond report-only boundary metadata without a new contract."
    - "Do not reinterpret parser diagnostics, local app watcher diagnostics, live-capture heartbeat/no-row diagnostics, evidence local status, status API exposure, unknown-entry routing, log-drift reports, local status summaries, corpus metadata, private operator notes, or future browser smoke reports as dedicated live Player.log health or readiness support without a new contract."
    - "Do not add parser_behavior_verified, local_report_only, private report artifacts, parser event families, committed logs, generated/private/runtime artifacts, SQLite files, workbook exports, secrets, tokens, API keys, or webhook URLs."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics behavior, live watcher diagnostics behavior, live capture status behavior, status API behavior, evidence runtime status behavior, log-drift behavior, golden replay behavior, feature-equity behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics behavior, AI/model-provider behavior, CI policy, merge policy, deploy policy, release policy, or production behavior."
```
