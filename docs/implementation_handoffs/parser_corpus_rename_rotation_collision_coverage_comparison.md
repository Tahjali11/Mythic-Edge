# Parser Corpus Rename Rotation Collision Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/416

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`rename_rotation_collision_report_only_boundary_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `rename_rotation_collision_boundary_report_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added count-only/report-only session metadata for
    `rename_rotation_collision_boundary_report_v1`.
- `tests/test_corpus_parity_report.py`
  - Updated summary-count expectations.
  - Added focused manifest and session-ledger assertions for
    `drift_debug.rename_or_rotation_collision`.
  - Added exact matrix-row assertions for
    `drift_debug.rename_or_rotation_collision`.
  - Preserved adjacent log-runtime rotation, recycle/rollback,
    missing-message-type, phantom/deck-origin, and private-log-drift
    boundaries.
- `docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`

No parser source, parser behavior, file tailer/watcher behavior, log discovery
behavior, stream behavior, router behavior, diagnostics source, log-drift
source, golden replay source, feature-equity source, evidence-ledger source,
runtime source, analytics source, workbook export, webhook surface, Apps
Script surface, AI/coaching behavior, generated/private artifact, raw fixture,
private log, private smoke output, file-system fixture, decklist, card-choice
artifact, strategy note, runtime status file, failed post, workbook export, or
external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 11
- partial: 3
- missing: 5
- blocked_private_evidence: 1
- blocked_external_boundary: 5
- `drift_debug.rename_or_rotation_collision`: `missing`
- `log_runtime.rotation`: `blocked_external_boundary`
- `drift_debug.recycle_or_rollback`: `blocked_external_boundary`
- `drift_debug.missing_message_type`: `covered_report_only`
- `drift_debug.phantom_or_deck_origin`: `missing`
- `mythic_edge.private_log_report_only_drift`: `missing`

Repo inspection confirmed adjacent tailer/stream rotation, log-drift,
diagnostics, golden replay, feature-equity, timestamp anomaly, unknown-entry,
missing-message-type, and corpus parity context, but no committed
parser-owned or file-system-owned rename/rotation collision fixture and no
contract authority to infer live file-system truth, log-rotation truth, file
identity tracking truth, rename/recycle collision handling, duplicate/replay
prevention, parser drift recovery truth, private smoke success, live watcher
correctness, release readiness, production behavior, analytics truth, AI
truth, coaching truth, or full corpus parity from those surfaces.

## Contract Changes Implemented

Implemented exactly one authorized coverage movement:

| Scenario family | Before | After |
| --- | --- | --- |
| `drift_debug.rename_or_rotation_collision` | `missing` | `covered_report_only` |

Preserved adjacent families:

| Scenario family | Status |
| --- | --- |
| `log_runtime.rotation` | `blocked_external_boundary` |
| `drift_debug.recycle_or_rollback` | `blocked_external_boundary` |
| `drift_debug.missing_message_type` | `covered_report_only` |
| `drift_debug.phantom_or_deck_origin` | `missing` |
| `mythic_edge.private_log_report_only_drift` | `missing` |

Added the required boundary metadata:

- entry id: `rename_rotation_collision_boundary_report_v1`
- entry type: `session_ledger_entry`
- source kind: `committed_count_only_report`
- commit status: `committed`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
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
- coverage basis:
  - `fixture_metadata_only`

The coverage row intentionally does not claim parser support,
parser-behavior verification, file-system fixture support, watcher support,
log-rotation truth, live file-system truth, file identity tracking truth,
rename/recycle collision handling, duplicate/replay prevention, parser drift
recovery truth, private smoke success, live watcher correctness, release
readiness, merge readiness, deploy readiness, production behavior, analytics
truth, AI truth, coaching truth, or full corpus parity.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- the `rename_rotation_collision_boundary_report_v1` manifest entry shape;
- `parser_event_families: []`;
- exact `covered_report_only` status and `["fixture_metadata_only"]` basis;
- non-claim parser claim families;
- known-gap and review-note non-claims;
- the session-ledger entry shape;
- count-only parser coverage fields, including one reference entry for tailer
  rotation, stream rotation event, log drift, diagnostics, golden replay, and
  feature-equity;
- zero dedicated rename/rotation collision fixtures, zero file-identity
  tracking claims, zero rename/recycle collision detection claims, zero
  duplicate/replay prevention claims, zero private-smoke success claims, and
  zero production watcher support claims;
- report-only redaction flags for file path identities, file hashes,
  byte-size lists, capture-date rows, private smoke outputs,
  generated/private/runtime artifacts, SQLite files, workbook exports,
  decklists, card choices, and credentials/tokens/keys/webhooks;
- report summary movement from 5 to 4 missing families and 11 to 12
  covered-report-only families;
- the exact `drift_debug.rename_or_rotation_collision` matrix row;
- adjacent family status preservation.

## Contract Mismatches

No blocking mismatches were found.

The selected `covered_report_only_boundary` path was viable without parser
behavior, parser source, tailer/watcher changes, log discovery changes, stream
changes, diagnostics, log-drift, golden replay, feature-equity,
evidence-ledger, runtime, analytics, workbook, webhook, Apps Script,
AI/coaching, private smoke, generated artifact, raw fixture, file-system
fixture, or decklist changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future rename/rotation collision support, file-system fixture evidence,
reduced expected-behavior models, private evidence collection, or movement
beyond report-only boundary metadata needs separate contract authority.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata,
session-ledger metadata, summary movement, adjacent-row preservation, and
boundary assertions.

No new parser, tailer, stream, or analytics tests were added because the
contract explicitly does not authorize parser behavior, file tailer/watcher
behavior, log discovery behavior, stream behavior, diagnostics behavior,
log-drift behavior, or dedicated file-system collision fixture claims.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 4 missing)`

```bash
python3 tools/check_agent_docs.py
```

- passed: checked_files 32, errors 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_rename_rotation_collision_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_rename_rotation_collision_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 6, forbidden 0, warnings 0

```bash
python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
git diff --check
```

- passed

```bash
printf '%s\n' docs/contracts/parser_corpus_rename_rotation_collision_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok

```bash
for docfile in docs/contracts/parser_corpus_rename_rotation_collision_coverage.md docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md; do git diff --no-index --check /dev/null "$docfile"; rc=$?; if [ "$rc" -eq 1 ]; then true; elif [ "$rc" -ne 0 ]; then exit "$rc"; fi; done
```

- passed

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_rename_rotation_collision_coverage.md docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py
```

- passed: no matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

```bash
git diff --name-only -- src tests/test_tailer.py tests/test_stream_integration.py tests/test_tailer_router_integration.py tests/fixtures/golden_replay tools main.py live_print_filtered_v11_match_summary.py .github
```

- passed: no protected parser/source, tailer/stream, golden replay, tool,
  app entrypoint, or CI paths changed

Recommended tailer/stream confidence check:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_tailer_router_integration.py
```

- passed: 12 passed

## Residual Risks

- `drift_debug.rename_or_rotation_collision` is covered only as report-only
  boundary metadata. It is not parser support, watcher support, or a dedicated
  file-system fixture.
- Tailer/stream rotation signals, log-runtime rotation boundaries,
  recycle/rollback boundaries, unknown-entry reporting, timestamp anomaly
  reporting, missing-message-type coverage, diagnostics, log-drift reports,
  golden replay, feature-equity, corpus parity metadata, and public taxonomy
  metadata remain reference context only.
- Live file-system truth, log-rotation truth, file identity tracking truth,
  rename/recycle collision handling, duplicate/replay prevention, private
  smoke success, parser drift recovery truth, live watcher correctness,
  release readiness, deploy readiness, merge readiness, production behavior,
  analytics truth, AI truth, coaching truth, and full corpus parity remain out
  of scope.
- Tracker #158 and issue #416 remain open until an authorized later workflow
  role handles lifecycle updates.

## Next Recommended Role

Codex E: Module Reviewer.

Review against issue #416, the contract, this handoff, the changed corpus
metadata, focused test assertions, and validation evidence. The reviewer
should verify that `drift_debug.rename_or_rotation_collision` moved only to
`covered_report_only`, `coverage_basis` remains exactly
`["fixture_metadata_only"]`, `parser_event_families` remains empty, and
adjacent log-runtime rotation, recycle/rollback, missing-message-type,
phantom/deck-origin, and private-log-drift boundaries were not reinterpreted.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer for issue #416, rename/rotation collision corpus coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/416
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/414
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/415
    - Previous merge commit: c0691fa4e53198179a76efdd5f05b33390f817ff
    - Branch: codex/parser-corpus-rename-rotation-collision-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_rename_rotation_collision_coverage.md
    - Handoff: docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md

  Goal:
    Review the implementation against the contract and repo boundaries. Lead with findings.

  Check:
    - drift_debug.rename_or_rotation_collision moved only from missing to covered_report_only.
    - coverage_basis is exactly ["fixture_metadata_only"].
    - parser_event_families remains empty.
    - parser_claim_families are non-claim boundary labels only.
    - session ledger counters are count-only/report-only and include zero dedicated collision fixtures, zero file-identity claims, zero duplicate/replay prevention claims, zero private-smoke success claims, and zero production watcher support claims.
    - log_runtime.rotation, drift_debug.recycle_or_rollback, drift_debug.missing_message_type, drift_debug.phantom_or_deck_origin, and mythic_edge.private_log_report_only_drift remain unchanged and are not reinterpreted as collision support.
    - No parser/tailer/stream/diagnostics/log-drift/runtime/analytics/workbook/webhook/App Script/AI/coaching/CI behavior changed.
    - No raw/private/external corpus data or generated/local artifacts were added.

  Suggested validation:
    - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_tailer_router_integration.py
    - python3 tools/check_agent_docs.py
    - python3 -m ruff check src tests tools
    - git diff --check
    - path-scoped secret/private-marker and protected-surface checks for changed files

  Do not:
    - Implement code.
    - Target main directly.
    - Close issue #416 or tracker #158.
    - Claim rename/rotation collision support, log-rotation truth, live file-system truth, duplicate/replay prevention, private smoke success, parser drift recovery truth, release readiness, deploy readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/416"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/414"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/415"
  previous_merge_commit: "c0691fa4e53198179a76efdd5f05b33390f817ff"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_rename_rotation_collision_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md"
  verdict: "rename_rotation_collision_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-rename-rotation-collision-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/416"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/414"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/415"
  previous_merge_commit: "c0691fa4e53198179a76efdd5f05b33390f817ff"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_rename_rotation_collision_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md"
  verdict: "rename_rotation_collision_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-rename-rotation-collision-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```
