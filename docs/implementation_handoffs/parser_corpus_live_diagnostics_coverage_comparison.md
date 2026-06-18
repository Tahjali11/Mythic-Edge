# Parser Corpus Live Diagnostics Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/420

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_live_diagnostics_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`live_diagnostics_report_only_boundary_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `live_diagnostics_boundary_report_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added count-only/report-only session metadata for
    `live_diagnostics_boundary_report_v1`.
- `tests/test_corpus_parity_report.py`
  - Updated summary-count expectations.
  - Added focused manifest and session-ledger assertions for
    `mythic_edge.live_diagnostics`.
  - Added exact matrix-row assertion for `mythic_edge.live_diagnostics`.
  - Preserved adjacent private-log drift, analytics-readiness, unknown-entry,
    and evidence-ledger provenance boundaries.
- `docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_live_diagnostics_coverage.md`

No parser source, parser behavior, diagnostics behavior, watcher behavior,
live-capture behavior, status API behavior, evidence review status behavior,
log-drift behavior, golden replay behavior, feature-equity behavior, runtime
status schema, analytics behavior, workbook export, webhook surface, Apps
Script surface, AI/coaching behavior, generated/private artifact, raw fixture,
private log, private smoke output, runtime artifact, SQLite file, workbook
export, operator note, browser smoke report, secret, token, API key,
credential, or webhook URL was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 13
- partial: 3
- missing: 3
- blocked_private_evidence: 1
- blocked_external_boundary: 5
- `mythic_edge.live_diagnostics`: `missing`
- `mythic_edge.private_log_report_only_drift`: `missing`
- `mythic_edge.analytics_readiness_labels`: `missing`
- `log_runtime.unknown_entry`: `covered_report_only`
- `mythic_edge.evidence_ledger_provenance`: `covered_report_only`

Repo inspection confirmed committed parser diagnostics, local app watcher
diagnostics, live-capture heartbeat/no-row diagnostics, evidence runtime
status, status API exposure, unknown-entry routing, log-drift, local status,
and corpus parity context, but no committed live Player.log fixture,
private-smoke fixture, watcher-correctness fixture, live-health assertion,
release-readiness gate, production-readiness gate, analytics-readiness claim,
AI/coaching claim, or contract authority to infer live truth from those
surfaces.

## Contract Changes Implemented

Implemented exactly one authorized coverage movement:

| Scenario family | Before | After |
| --- | --- | --- |
| `mythic_edge.live_diagnostics` | `missing` | `covered_report_only` |

Preserved adjacent families:

| Scenario family | Status |
| --- | --- |
| `mythic_edge.private_log_report_only_drift` | `missing` |
| `mythic_edge.analytics_readiness_labels` | `missing` |
| `log_runtime.unknown_entry` | `covered_report_only` |
| `mythic_edge.evidence_ledger_provenance` | `covered_report_only` |

Added the required boundary metadata:

- entry id: `live_diagnostics_boundary_report_v1`
- entry type: `session_ledger_entry`
- source kind: `committed_count_only_report`
- commit status: `committed`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
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
- coverage basis:
  - `diagnostics_only`
  - `fixture_metadata_only`

The coverage row intentionally does not include `parser_behavior_verified`,
`local_report_only`, private report artifacts, parser event families, committed
logs, runtime artifacts, generated data, SQLite files, workbook exports,
secrets, tokens, API keys, or webhook URLs.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- the `live_diagnostics_boundary_report_v1` manifest entry shape;
- `parser_event_families: []`;
- exact `covered_report_only` status and
  `["diagnostics_only", "fixture_metadata_only"]` basis;
- absence of `parser_behavior_verified` and `local_report_only`;
- non-claim parser claim families;
- known-gap and review-note non-claims;
- the session-ledger entry shape and `source_entry_id`;
- count-only parser coverage fields, including one reference entry for parser
  diagnostics, live watcher diagnostics, live-capture no-row diagnostics,
  evidence review status, status API, log drift, and unknown entry;
- zero private-smoke success, live Player.log health, watcher correctness,
  parser support, release readiness, deploy readiness, production readiness,
  analytics truth, AI truth, and coaching truth claims;
- report-only redaction flags for raw logs, private paths, raw payloads,
  external logs, private Player.log evidence, private smoke outputs,
  generated/private/runtime artifacts, local status artifacts, SQLite files,
  workbook exports, operator notes, browser smoke reports, decklists, card
  choices, and credentials/tokens/keys/webhooks;
- report summary movement from 3 to 2 missing families and 13 to 14
  covered-report-only families;
- the exact `mythic_edge.live_diagnostics` matrix row;
- adjacent family status preservation.

## Contract Mismatches

No blocking mismatches were found.

The selected `covered_report_only` path was viable without parser behavior,
diagnostics behavior, watcher behavior, live-capture behavior, status API
behavior, evidence review status behavior, log-drift behavior, golden replay,
feature-equity, local status schema, analytics, workbook, webhook, Apps
Script, AI/coaching, private smoke, generated artifact, raw fixture, runtime
artifact, SQLite file, workbook export, operator note, or browser smoke report
changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future private-log drift, analytics-readiness labels, private smoke evidence,
browser smoke evidence, live Player.log health proof, watcher correctness
proof, release-readiness gates, or movement beyond report-only boundary
metadata needs separate contract authority.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata,
session-ledger metadata, summary movement, adjacent-row preservation, and
boundary assertions.

No new parser, diagnostics, status API, watcher, live-capture, evidence runtime
status, log-drift, golden replay, feature-equity, analytics, or AI tests were
added because the contract explicitly does not authorize behavior changes or
live health/support claims.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 2 missing)`

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_diagnostics.py tests/test_log_drift_sensor.py tests/test_evidence_runtime_status.py tests/test_status_api.py
```

- passed: 39 passed

```bash
python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
git diff --check
```

- passed

```bash
python3 tools/check_agent_docs.py
```

- passed: checked_files 32, errors 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_live_diagnostics_coverage.md docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_live_diagnostics_coverage.md docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_live_diagnostics_coverage.md docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
```

- passed

```bash
for docfile in docs/contracts/parser_corpus_live_diagnostics_coverage.md docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md; do git diff --no-index --check /dev/null "$docfile"; check_rc=$?; if [ "$check_rc" -eq 1 ]; then true; elif [ "$check_rc" -ne 0 ]; then exit "$check_rc"; fi; done
```

- passed

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_live_diagnostics_coverage.md docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py
```

- passed: no matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

```bash
git diff --name-only -- src tests/test_parser_diagnostics_mode.py tests/test_diagnostics.py tests/test_log_drift_sensor.py tests/test_evidence_runtime_status.py tests/test_status_api.py tests/fixtures/golden_replay tools main.py live_print_filtered_v11_match_summary.py .github
```

- passed: no protected parser/source, adjacent behavior, golden replay, tool,
  app entrypoint, or CI paths changed

## Residual Risks

- `mythic_edge.live_diagnostics` is covered only as report-only boundary
  metadata. It is not private smoke success, live Player.log health, watcher
  correctness, parser support for a live run, release readiness, deploy
  readiness, production behavior, analytics readiness, AI truth, coaching
  truth, or full corpus parity.
- Parser diagnostics, local app watcher diagnostics, live-capture
  heartbeat/no-row diagnostics, evidence review status, status API exposure,
  unknown-entry routing, log-drift reports, local status summaries, corpus
  parity metadata, private operator notes, and future browser smoke reports
  remain reference context only.
- Tracker #158 and issue #420 remain open until an authorized later workflow
  role handles lifecycle updates.

## Next Recommended Role

Codex E: Module Reviewer.

Review against issue #420, the contract, this handoff, the changed corpus
metadata, focused test assertions, and validation evidence. The reviewer
should verify that `mythic_edge.live_diagnostics` moved only to
`covered_report_only`, `coverage_basis` remains exactly
`["diagnostics_only", "fixture_metadata_only"]`, `parser_event_families`
remains empty, no `parser_behavior_verified` or `local_report_only` basis was
added, and adjacent private-log drift and analytics-readiness rows remain
missing.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer for issue #420, live diagnostics corpus coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/420
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/418
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/419
    - Previous merge commit: 5180de4b5900dc4bfd895d394d1a5ac74994c4b4
    - Branch: codex/parser-corpus-live-diagnostics-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_live_diagnostics_coverage.md
    - Handoff: docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md

  Goal:
    Review the implementation against the contract and repo boundaries. Lead with findings.

  Check:
    - mythic_edge.live_diagnostics moved only from missing to covered_report_only.
    - coverage_basis is exactly ["diagnostics_only", "fixture_metadata_only"].
    - parser_event_families remains empty.
    - parser_behavior_verified and local_report_only were not added.
    - No private local report artifact, committed logs, runtime artifacts, generated data, SQLite files, workbook exports, secrets, tokens, API keys, or webhook URLs were added.
    - session ledger counters are count-only/report-only and include zero private-smoke success, live Player.log health, watcher correctness, parser support, release readiness, deploy readiness, production readiness, analytics truth, AI truth, and coaching truth claims.
    - mythic_edge.private_log_report_only_drift and mythic_edge.analytics_readiness_labels remain missing.
    - No parser/diagnostics/watcher/live-capture/status API/evidence-runtime-status/log-drift/runtime/workbook/webhook/App Script/analytics/AI/coaching/CI behavior changed.

  Suggested validation:
    - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - PYTHONPATH=src python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_diagnostics.py tests/test_log_drift_sensor.py tests/test_evidence_runtime_status.py tests/test_status_api.py
    - python3 tools/check_agent_docs.py
    - python3 -m ruff check src tests tools
    - git diff --check
    - path-scoped secret/private-marker and protected-surface checks for changed files

  Do not:
    - Implement code.
    - Target main directly.
    - Close issue #420 or tracker #158.
    - Claim private smoke success, live Player.log health, watcher correctness, parser support, release readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/420"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/418"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/419"
  previous_merge_commit: "5180de4b5900dc4bfd895d394d1a5ac74994c4b4"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_live_diagnostics_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md"
  verdict: "live_diagnostics_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-live-diagnostics-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/420"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/418"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/419"
  previous_merge_commit: "5180de4b5900dc4bfd895d394d1a5ac74994c4b4"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_live_diagnostics_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md"
  verdict: "live_diagnostics_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-live-diagnostics-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only"
```
