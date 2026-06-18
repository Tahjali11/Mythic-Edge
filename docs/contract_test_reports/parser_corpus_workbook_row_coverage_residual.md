# Parser Corpus Workbook Row Coverage Residual Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/432
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- contract:
  `docs/contracts/parser_corpus_workbook_row_coverage_residual.md`
- base_branch: `codex/parser-parity`
- implementation_branch:
  `codex/parser-corpus-workbook-row-coverage-residual`
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/430
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/431
- previous_merge_commit:
  `4c080d5820e34cb5bdd1f4df86350e45ee5b6874`
- generated_by: Codex C / Module Implementer

Live state checked during implementation:

- Issue #432 is open.
- Tracker #158 is open.
- PR #431 is merged into `codex/parser-parity` with merge commit
  `4c080d5820e34cb5bdd1f4df86350e45ee5b6874`.
- The current implementation branch contains that merge commit as an ancestor.

## Contract Decision

The contract selected the safe metadata-only promotion path:

- promote only `mythic_edge.workbook_row_coverage`;
- move it from `partial` to `covered_report_only`;
- use existing corpus manifest and session-ledger vocabulary;
- use basis `["fixture_metadata_only"]`;
- use entry id `workbook_row_coverage_boundary_report_v1`;
- keep parser event families empty;
- stop using `feature_equity_corpus_baseline_v1` for this row;
- preserve confidence/finality/degradation, manifest metadata,
  private-evidence rows, external-boundary rows, and protected surfaces.

This report records the post-implementation state. It does not decide full
corpus parity, tracker completion, parser support, workbook truth, release
readiness, deploy readiness, production readiness, analytics truth, AI truth,
coaching truth, gameplay advice, merge readiness, or CI authority.

## Corpus Report Status

After implementation:

- status: `partial_coverage_map_ready`
- total scenario families: 45
- covered committed: 6
- covered synthetic: 14
- covered report-only: 18
- partial: 0
- missing: 0
- deferred: 0
- blocked private evidence: 2
- blocked external boundary: 5
- not applicable: 0

Expected count movement from the contract was observed:

- `covered_report_only`: 17 -> 18
- `partial`: 1 -> 0
- `missing`: remains 0
- `blocked_private_evidence`: remains 2
- `blocked_external_boundary`: remains 5
- `covered_committed`: remains 6
- `covered_synthetic`: remains 14

The overall status remains `partial_coverage_map_ready` because blocked rows
remain.

## Promoted Row

| Scenario family | Status | Basis | Entry | Review |
| --- | --- | --- | --- | --- |
| `mythic_edge.workbook_row_coverage` | `covered_report_only` | `fixture_metadata_only` | `workbook_row_coverage_boundary_report_v1` | Proves committed parser-side workbook-facing contracts, tests, snapshots, and row-shape guardrails exist. It does not prove live workbook behavior or downstream truth. |

The row no longer uses:

- `feature_equity_corpus_baseline_v1`
- `count_ratchet_only`
- `partial`

The new manifest entry records these parser claim families:

- `match_log_row_keys`
- `game_log_row_keys`
- `sync_field_registry`
- `runtime_sheet_headers`
- `runtime_export_row_keys`
- `repo_side_apps_script_mapping_parity`
- `webhook_top_level_row_shape`
- `live_workbook_non_claim`
- `downstream_truth_non_claim`

The matching session-ledger entry records availability signals for parser-side
workbook-facing row/schema evidence and zero claims for:

- live workbook behavior;
- deployed Apps Script behavior;
- Google Sheets sync;
- webhook delivery;
- dashboard truth;
- analytics truth;
- AI truth;
- coaching truth.

## Rows Preserved

| Scenario family | Status | Basis | Entry |
| --- | --- | --- | --- |
| `mythic_edge.confidence_finality_degradation` | `covered_report_only` | `evidence_ledger_only`, `fixture_metadata_only` | `confidence_finality_degradation_boundary_report_v1` |
| `manifest.metadata` | `covered_report_only` | `fixture_metadata_only` | `parser_corpus_manifest_metadata_boundary_v1` |
| `connection.firewall_or_network_drop` | `blocked_private_evidence` | `local_report_only` | `firewall_network_drop_private_evidence_boundary_v1` |
| `mythic_edge.private_log_report_only_drift` | `blocked_private_evidence` | `local_report_only` | `private_log_report_only_drift_private_evidence_boundary_v1` |
| `log_runtime.rotation` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `timer.inactivity_timeout` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `gameplay_stress.conjure` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `gameplay_stress.spellbook` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `drift_debug.recycle_or_rollback` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |

`feature_equity_corpus_baseline_v1` still contributes to:

- `drift_debug.gsm_truncation`

It no longer contributes to `mythic_edge.workbook_row_coverage`.

## Truth Boundary

Corpus parity metadata owns scenario-family coverage status and review notes.
This implementation proves only a committed metadata boundary for parser-side
workbook-facing row coverage.

Workbook-facing contracts and tests remain the authority for workbook schema,
runtime row construction, row-key snapshots, repo-side Apps Script parity
checks, and webhook row-shape guardrails. They do not prove deployed or live
behavior.

Private Player.log checks, private smoke outputs, live workbook checks, live
Google Sheets checks, deployed Apps Script execution, webhook delivery checks,
runtime artifacts, and workbook exports remain outside this committed package.

## Non-Claims

This report does not claim:

- full Mythic Edge corpus parity
- tracker #158 completion
- parser behavior
- parser support
- workbook truth
- live workbook tab correctness
- deployed Apps Script behavior
- Google Sheets sync success
- webhook delivery success
- workbook formula truth
- dashboard truth
- private smoke success
- live Player.log health
- release readiness
- deploy readiness
- production readiness
- analytics truth or statistical validity
- AI truth
- coaching truth
- gameplay advice
- hidden-card inference
- archetype classification
- player-mistake labels
- merge readiness
- CI gate status beyond commands actually run

## Protected Surface Status

Changed:

- corpus manifest metadata for one scenario-family row;
- session-ledger metadata for the matching report-only row;
- focused corpus parity tests;
- Codex C handoff and report artifacts.

Not changed:

- parser behavior;
- source parser code;
- evidence-ledger behavior;
- runtime field-evidence behavior;
- corpus report code;
- router semantics;
- diagnostics, drift, golden replay, feature-equity, or analytics behavior;
- match/game identity or deduplication;
- workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, runtime status files, failed posts, workbook exports;
- AI/model-provider behavior, coaching behavior, CI gates, merge readiness,
  deploy readiness, production behavior, or tracker lifecycle.

No private Player.log files, private app-data, private smoke outputs, live
MTGA checks, live workbook checks, Google Sheets reads or writes, Apps Script
execution, webhook calls, generated SQLite databases, runtime status files,
failed posts, workbook exports, private reports, Manasight raw logs,
compressed corpus files, raw session payloads, external corpus contents,
secrets, credentials, tokens, API keys, webhook URLs, decklists, card choices,
private strategy notes, or local absolute paths were added.

## Validation

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_sheet_schema.py tests/test_sheet_exports.py tests/test_event_schema_snapshots.py tests/test_app_models.py tests/test_webhook_payload_schema.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
LC_ALL=C rg -n '[^[:ascii:]]' <changed files>
LC_ALL=C rg -n '[[:blank:]]$' <changed files>
find . -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm'
```

Results:

- manifest JSON parse: passed.
- session-ledger JSON parse: passed.
- focused corpus parity tests: 7 passed.
- corpus parity CLI:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- direct row inspection:
  - target row promoted to `covered_report_only`;
  - `feature_equity_corpus_baseline_v1` no longer owns the target row;
  - #430 confidence/finality/degradation row unchanged;
  - private-evidence rows unchanged;
  - external-boundary rows unchanged.
- workbook-facing regression tests: 66 passed.
- agent docs check: passed.
- Ruff: passed.
- diff whitespace check: passed.
- path-scoped secret/private-marker scan: passed.
- path-scoped protected-surface gate: passed.
- validation selector: `selection_status: ok`.
- ASCII scan: passed.
- trailing-whitespace scan: passed.
- generated SQLite artifact scan: clean.

## Residual Risks

- The corpus report status is still `partial_coverage_map_ready` while blocked
  private-evidence and blocked-external rows remain.
- This metadata row does not prove any live workbook, deployed Apps Script,
  Google Sheets sync, webhook delivery, dashboard, analytics, AI, coaching,
  release, deploy, production, tracker-completion, or full-parity claim.
- Future private/external evidence rows need separate issue and contract paths.

## Next Recommended Role

Codex E: Module Reviewer.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/432"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/430"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/431"
  previous_merge_commit: "4c080d5820e34cb5bdd1f4df86350e45ee5b6874"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_workbook_row_coverage_residual.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md"
  verdict: "workbook_row_coverage_metadata_promotion_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-workbook-row-coverage-residual"
  base_branch: "codex/parser-parity"
  selected_family: "mythic_edge.workbook_row_coverage"
```

## Codex E Contract-Test Review - 2026-06-18

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The implementation matches the #432 contract's narrow report-only
promotion: only `mythic_edge.workbook_row_coverage` moved from
`partial` / `count_ratchet_only` /
`feature_equity_corpus_baseline_v1` to `covered_report_only` with basis
`["fixture_metadata_only"]` and entry
`workbook_row_coverage_boundary_report_v1`.

The reviewer base-vs-head matrix comparison found exactly one changed row:

| Scenario family | Before | After |
| --- | --- | --- |
| `mythic_edge.workbook_row_coverage` | `partial`, `count_ratchet_only`, `feature_equity_corpus_baseline_v1` | `covered_report_only`, `fixture_metadata_only`, `workbook_row_coverage_boundary_report_v1` |

The generated report summary remains contract-aligned:

- status: `partial_coverage_map_ready`
- total scenario families: 45
- covered committed: 6
- covered synthetic: 14
- covered report-only: 18
- partial: 0
- missing: 0
- deferred: 0
- blocked private evidence: 2
- blocked external boundary: 5
- not applicable: 0

### Contract Matches

- `feature_equity_corpus_baseline_v1` no longer owns
  `mythic_edge.workbook_row_coverage`.
- `feature_equity_corpus_baseline_v1` still owns exactly
  `drift_debug.gsm_truncation`.
- `mythic_edge.workbook_row_coverage` no longer appears in the generated gaps.
- `mythic_edge.confidence_finality_degradation` remains `covered_report_only`
  with basis `["evidence_ledger_only", "fixture_metadata_only"]`.
- `manifest.metadata` remains `covered_report_only` with
  `fixture_metadata_only`.
- Private-evidence rows remain `blocked_private_evidence`.
- External-boundary rows remain `blocked_external_boundary`.
- The new manifest entry has no parser event families and does not use
  `parser_behavior_verified`, `count_ratchet_only`, `diagnostics_only`,
  `evidence_ledger_only`, `local_report_only`, or `external_reference_only`.
- The matching session-ledger entry records zero live workbook, deployed Apps
  Script, Google Sheets sync, webhook delivery, dashboard truth, analytics
  truth, AI truth, and coaching truth claims.
- Issue #432 and tracker #158 are open; PR #431 is merged into
  `codex/parser-parity`, and merge commit
  `4c080d5820e34cb5bdd1f4df86350e45ee5b6874` is an ancestor of this branch.

### Contract Mismatches

None found.

### Validation Run

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_sheet_schema.py tests/test_sheet_exports.py tests/test_event_schema_snapshots.py tests/test_app_models.py tests/test_webhook_payload_schema.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' <changed files> | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' <changed files> | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' <changed files> | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
LC_ALL=C rg -n '[^[:ascii:]]' <changed files>
LC_ALL=C rg -n '[[:blank:]]$' <changed files>
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name 'Player.log' -o -name '*.Player.log' -o -name '*.player.log' -o -name '*.log.gz' \) -print
gh issue view 432 --repo Tahjali11/Mythic-Edge --json state,number,title,url
gh issue view 158 --repo Tahjali11/Mythic-Edge --json state,number,title,url
gh pr view 431 --repo Tahjali11/Mythic-Edge --json state,mergedAt,mergeCommit,baseRefName,headRefName,url
git merge-base --is-ancestor 4c080d5820e34cb5bdd1f4df86350e45ee5b6874 HEAD
```

Results:

- manifest JSON parse: passed.
- session-ledger JSON parse: passed.
- focused corpus parity tests: 7 passed.
- corpus parity CLI:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- workbook-facing regression tests: 66 passed.
- direct row assertions: passed.
- base-vs-head matrix comparison: passed with exactly one changed row.
- agent docs check: passed.
- Ruff: passed.
- diff whitespace check: passed.
- path-scoped secret/private-marker scan: passed with 0 forbidden and 0 warnings.
- path-scoped protected-surface gate: passed with 0 forbidden and 0 warnings.
- path-scoped validation selector: `selection_status: ok`.
- ASCII scan: passed.
- trailing-whitespace scan: passed.
- generated SQLite/raw-log artifact scan: clean.
- GitHub state refresh: issue #432 open, tracker #158 open, PR #431 merged.
- previous merge commit ancestry check: passed.

### Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
router semantics, diagnostics behavior, drift behavior, golden replay behavior,
feature-equity behavior, evidence-ledger behavior, runtime field-evidence
behavior, match/game identity, deduplication, workbook schema, webhook payload
shape, Apps Script behavior, Google Sheets sync, output transport, analytics
truth, AI/model-provider behavior, coaching behavior, CI gates, merge
readiness, deploy readiness, production behavior, tracker lifecycle, or final
integration policy changed.

The changed package is limited to the six expected files:

- `docs/contracts/parser_corpus_workbook_row_coverage_residual.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md`
- `docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md`

### Remaining Risks

- The report status remains `partial_coverage_map_ready` while two
  private-evidence and five external-boundary rows remain intentionally
  unresolved.
- This review did not run private Player.log, app-data, live MTGA, Google
  Sheets, deployed Apps Script, webhook delivery, private smoke, or full pytest
  checks.
- This review does not claim full corpus parity, parser behavior correctness,
  workbook truth, live workbook correctness, deployed Apps Script behavior,
  Google Sheets sync success, webhook delivery success, dashboard truth,
  analytics truth, AI truth, coaching truth, release readiness, merge
  readiness, deploy readiness, production readiness, tracker completion, or CI
  authority beyond commands run.

### Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/432"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/430"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/431"
  previous_merge_commit: "4c080d5820e34cb5bdd1f4df86350e45ee5b6874"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md"
  target_artifact: "draft PR for workbook row coverage residual report-only promotion"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-workbook-row-coverage-residual"
  base_branch: "codex/parser-parity"
  selected_family: "mythic_edge.workbook_row_coverage"
  validation:
    - "python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null"
    - "python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_sheet_schema.py tests/test_sheet_exports.py tests/test_event_schema_snapshots.py tests/test_app_models.py tests/test_webhook_payload_schema.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector sanity check for changed files"
    - "GitHub issue/tracker/previous PR state refreshed with gh"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #432 or tracker #158 unless separately authorized."
    - "Do not mark tracker #158 complete."
    - "Do not claim full corpus parity, parser behavior correctness, workbook truth, live workbook correctness, deployed Apps Script behavior, Google Sheets sync success, webhook delivery success, dashboard truth, analytics truth, AI truth, coaching truth, release readiness, merge readiness, deploy readiness, production readiness, tracker completion, or CI authority beyond commands run."
    - "Do not run private Player.log, app-data, live MTGA, Google Sheets, deployed Apps Script, webhook delivery, or private smoke checks."
    - "Do not import or commit Manasight raw logs, compressed corpus files, parser source, external corpus contents, private logs, generated/runtime artifacts, workbook exports, secrets, tokens, API keys, webhook URLs, decklists, card choices, private reports, private strategy notes, or local absolute paths."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics behavior, drift behavior, golden replay behavior, feature-equity behavior, evidence-ledger behavior, runtime field-evidence behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI/model-provider behavior, coaching behavior, CI gates, merge readiness, deploy readiness, production behavior, tracker lifecycle, or final integration policy."
```
