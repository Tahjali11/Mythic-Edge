# Parser Corpus Workbook Row Coverage Residual Handoff

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/432

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

- `docs/contracts/parser_corpus_workbook_row_coverage_residual.md`

## Internal Project Area

Corpus / Provenance, with Workbook / Transport as referenced supporting
evidence only.

## Truth Owner

Truth owner for the corpus coverage row:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Supporting workbook-facing contracts and tests remain the authority for their
own surfaces. This slice only records the report-only corpus metadata boundary.

## Bridge-Code Status

`not_bridge_code`

This implementation adds committed corpus metadata and focused tests. It does
not add source-code behavior, move runtime data between project areas, or
authorize downstream workbook/webhook/App Script behavior.

## Role Performed

Codex C: Module Implementer.

## Comparison Summary

The contract selected a metadata-only promotion for only
`mythic_edge.workbook_row_coverage`:

- before: `partial`, basis `count_ratchet_only`, entry
  `feature_equity_corpus_baseline_v1`
- after: `covered_report_only`, basis `["fixture_metadata_only"]`, entry
  `workbook_row_coverage_boundary_report_v1`

The implementation follows that path using existing corpus manifest and
session-ledger vocabulary. No corpus report source-code changes were needed.

The generated corpus parity report now has the contracted count change:

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
- overall status: `partial_coverage_map_ready`

Rows explicitly required to remain unchanged stayed unchanged:

- `mythic_edge.confidence_finality_degradation`: `covered_report_only`
- `manifest.metadata`: `covered_report_only`
- `connection.firewall_or_network_drop`: `blocked_private_evidence`
- `mythic_edge.private_log_report_only_drift`: `blocked_private_evidence`
- `log_runtime.rotation`: `blocked_external_boundary`
- `timer.inactivity_timeout`: `blocked_external_boundary`
- `gameplay_stress.conjure`: `blocked_external_boundary`
- `gameplay_stress.spellbook`: `blocked_external_boundary`
- `drift_debug.recycle_or_rollback`: `blocked_external_boundary`

Zero partial rows and zero missing rows are not readiness claims while blocked
private-evidence and blocked-external rows remain.

## What Changed

- Added manifest entry `workbook_row_coverage_boundary_report_v1`.
- Added matching session-ledger entry
  `workbook_row_coverage_boundary_report_v1`.
- Removed only `mythic_edge.workbook_row_coverage` from
  `feature_equity_corpus_baseline_v1` scenario-family ownership.
- Updated focused corpus parity tests to pin the manifest entry, session-ledger
  entry, generated report row, summary count movement, absence of a target-row
  gap, and unchanged blocked rows.
- Added this implementation handoff.
- Added the contract-test report artifact for Codex E review.

## Files Changed

- `docs/contracts/parser_corpus_workbook_row_coverage_residual.md`
  - Source contract artifact from Codex B, present in the worktree.
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md`
- `docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md`

## Code Changed

No runtime source code changed.

The corpus report code already supported the required entry type, coverage
status, coverage basis, source kind, privacy class, sanitization status, and
session-ledger metadata shape.

## Tests Added Or Updated

- Updated `tests/test_corpus_parity_report.py`.

Focused assertions now cover:

- the new manifest entry shape and existing vocabulary;
- parser event families remaining empty;
- `fixture_metadata_only` as the only basis;
- absence of `parser_behavior_verified` and `count_ratchet_only`;
- the matching session-ledger entry, availability fields, and zero-claim fields;
- privacy redactions for no raw logs, payloads, live workbook contents, deployed
  Apps Script output, Google Sheets contents, webhook payload captures, runtime
  artifacts, workbook exports, private evidence, decklists, card choices,
  strategy notes, credentials, tokens, keys, or webhooks;
- `feature_equity_corpus_baseline_v1` no longer owning the target row;
- the target row no longer producing a gap record;
- private-evidence and external-boundary rows remaining unchanged.

## Interface Changes

Corpus metadata changed for one scenario-family row:

- `mythic_edge.workbook_row_coverage` now reports:
  - `coverage_status`: `covered_report_only`
  - `coverage_basis`: `["fixture_metadata_only"]`
  - `mythic_edge_entries`: `["workbook_row_coverage_boundary_report_v1"]`

No function signatures, parser events, parser behavior, workbook columns,
webhook payloads, Apps Script behavior, runtime status schema, environment
variables, CLI arguments, CI gates, issue lifecycle rules, or PR lifecycle
rules changed.

## Contracted Area Status

The implementation stayed within the authorized Corpus / Provenance metadata
area. No parser, router, diagnostics, drift, golden replay, feature-equity,
evidence-ledger behavior, analytics, workbook, webhook, Apps Script, Google
Sheets, local app, Match Journal, overlay, AI/model-provider, coaching, CI,
merge, deploy, production, private-artifact, external-corpus, or tracker
lifecycle surface was touched.

## Validation Run

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_sheet_schema.py tests/test_sheet_exports.py tests/test_event_schema_snapshots.py tests/test_app_models.py tests/test_webhook_payload_schema.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  docs/contracts/parser_corpus_workbook_row_coverage_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_workbook_row_coverage_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_workbook_row_coverage_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md \
  | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
LC_ALL=C rg -n '[^[:ascii:]]' \
  docs/contracts/parser_corpus_workbook_row_coverage_residual.md \
  docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py
LC_ALL=C rg -n '[[:blank:]]$' \
  docs/contracts/parser_corpus_workbook_row_coverage_residual.md \
  docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py
find . -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm'
```

Results:

- manifest JSON parse: passed.
- session-ledger JSON parse: passed.
- focused corpus parity tests: 7 passed.
- corpus parity CLI: `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
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

## Open Risks

- The report status remains `partial_coverage_map_ready` because blocked
  private-evidence and blocked-external rows remain.
- This implementation does not prove live workbook behavior, deployed Apps
  Script behavior, Google Sheets sync, webhook delivery success, workbook
  formulas, dashboard truth, analytics truth, AI truth, coaching truth, release
  readiness, production readiness, tracker completion, or full corpus parity.
- Future rows that require private or external evidence still need separate
  issue/contract paths.

## Next Recommended Role

Codex E: Module Reviewer.

Suggested review focus:

- confirm `feature_equity_corpus_baseline_v1` no longer owns
  `mythic_edge.workbook_row_coverage`;
- confirm the new target row is `covered_report_only` with only
  `fixture_metadata_only`;
- confirm blocked-private and blocked-external rows are unchanged;
- confirm no runtime code, workbook schema, webhook, Apps Script, Google Sheets,
  analytics, AI, coaching, CI, merge, deploy, production, or tracker lifecycle
  surface changed;
- confirm validation evidence.

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
