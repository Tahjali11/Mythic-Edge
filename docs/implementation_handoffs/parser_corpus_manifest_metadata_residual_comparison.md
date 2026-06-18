# Parser Corpus Manifest Metadata Residual Handoff

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/428

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

- `docs/contracts/parser_corpus_manifest_metadata_residual.md`

## Internal Project Area

Corpus / Provenance, with Quality / Governance as the workflow artifact owner.

## Truth Owner

Truth owner for the `manifest.metadata` corpus coverage row:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Supporting reference only:

- `tests/fixtures/parser_corpus/session_ledger.v1.json`

## Bridge-Code Status

`not_bridge_code`

This slice is committed corpus metadata plus focused test coverage. It does
not move data between project areas and does not authorize bridge code.

## Role Performed

Codex C: Module Implementer.

## Comparison Summary

The contract selected a narrow promotion for only `manifest.metadata`:

- before: `partial`, basis `count_ratchet_only`, entry
  `feature_equity_corpus_baseline_v1`
- after: `covered_report_only`, basis `fixture_metadata_only`, entry
  `parser_corpus_manifest_metadata_boundary_v1`

The implementation follows that selected path using existing corpus manifest
vocabulary. No corpus report code changes were needed.

The generated corpus parity report now has the contracted count change:

- total scenario families: 45
- covered committed: 6
- covered synthetic: 14
- covered report-only: 16
- partial: 2
- missing: 0
- deferred: 0
- blocked private evidence: 2
- blocked external boundary: 5
- not applicable: 0
- overall status: `partial_coverage_map_ready`

Rows explicitly required to remain unchanged stayed unchanged:

- `mythic_edge.confidence_finality_degradation`: `partial`
- `mythic_edge.workbook_row_coverage`: `partial`
- `connection.firewall_or_network_drop`: `blocked_private_evidence`
- `mythic_edge.private_log_report_only_drift`: `blocked_private_evidence`
- `log_runtime.rotation`: `blocked_external_boundary`
- `timer.inactivity_timeout`: `blocked_external_boundary`
- `gameplay_stress.conjure`: `blocked_external_boundary`
- `gameplay_stress.spellbook`: `blocked_external_boundary`
- `drift_debug.recycle_or_rollback`: `blocked_external_boundary`

## What Changed

- Added `parser_corpus_manifest_metadata_boundary_v1` to the corpus manifest.
- Removed only `manifest.metadata` from
  `feature_equity_corpus_baseline_v1` scenario-family ownership.
- Updated focused corpus parity tests to pin the new manifest boundary entry,
  the count change, the generated report row, and unchanged residual ownership.
- Added this implementation handoff.
- Added the contract-test report artifact for Codex E review.

## Files Changed

- `docs/contracts/parser_corpus_manifest_metadata_residual.md`
  - Source contract artifact from Codex B, present in the worktree.
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md`
- `docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md`

## Code Changed

No runtime source code changed.

The corpus report code already supported the required entry type, coverage
status, coverage basis, source kind, privacy class, and sanitization status.

## Tests Added Or Updated

- Updated `tests/test_corpus_parity_report.py`.

Focused assertions now cover:

- the new `parser_corpus_manifest_metadata_boundary_v1` entry shape;
- existing vocabulary only;
- `manifest.metadata` removed from `feature_equity_corpus_baseline_v1`;
- `manifest.metadata` generated report status, basis, entry, and notes;
- report summary counts changing from 15 report-only / 3 partial to 16
  report-only / 2 partial;
- remaining partial, private-evidence, and external-boundary rows unchanged.

## Interface Changes

Corpus manifest metadata changed for one scenario-family row:

- `manifest.metadata` now reports:
  - `coverage_status`: `covered_report_only`
  - `coverage_basis`: `["fixture_metadata_only"]`
  - `mythic_edge_entries`:
    `["parser_corpus_manifest_metadata_boundary_v1"]`

No function signatures, parser event classes, parser state behavior, CLI
arguments, workbook columns, webhook payloads, Apps Script behavior, runtime
status schema, environment variables, CI gates, issue lifecycle rules, or PR
lifecycle rules changed.

## Contracted Area Status

The implementation stayed within the authorized Corpus / Provenance metadata
area. No parser, router, diagnostics, drift, golden replay, feature-equity,
evidence-ledger, analytics, workbook, webhook, Apps Script, Google Sheets,
local app, Match Journal, overlay, AI/model-provider, coaching, CI, merge,
deploy, production, private-artifact, external-corpus, or tracker lifecycle
surface was touched.

## Validation Run

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  docs/contracts/parser_corpus_manifest_metadata_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_manifest_metadata_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_manifest_metadata_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md \
  | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
LC_ALL=C rg -n '[^[:ascii:]]' \
  docs/contracts/parser_corpus_manifest_metadata_residual.md \
  docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py
LC_ALL=C rg -n '[[:blank:]]$' \
  docs/contracts/parser_corpus_manifest_metadata_residual.md \
  docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py
find . -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm'
```

Results:

- manifest JSON parse: passed.
- session-ledger JSON parse: passed.
- focused corpus parity tests: 7 passed.
- corpus parity CLI: `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- agent docs check: passed.
- Ruff: passed.
- diff whitespace check: passed.
- path-scoped secret/private-marker scan: passed.
- path-scoped protected-surface gate: passed.
- validation selector: `selection_status: ok`.
- ASCII scan: passed.
- trailing-whitespace scan: passed.
- generated SQLite artifact scan: clean.

## Still Unverified

- No private Player.log, app-data, firewall/drop, network, live MTGA, or
  private smoke checks were run or authorized.
- This does not prove parser behavior, parser support, complete fixture
  adequacy, session-ledger completeness, full corpus parity, tracker
  completion, private smoke success, release readiness, deploy readiness,
  production readiness, analytics truth, AI truth, coaching truth, gameplay
  advice, merge readiness, or CI authority beyond commands actually run.

## Reviewer Focus

Codex E should verify:

- only `manifest.metadata` changed status;
- `manifest.metadata` is `covered_report_only`, not `covered_committed` or
  `covered_synthetic`;
- the basis is exactly `["fixture_metadata_only"]`;
- the row is owned only by
  `parser_corpus_manifest_metadata_boundary_v1`;
- `feature_equity_corpus_baseline_v1` no longer owns `manifest.metadata` but
  still owns the two remaining partial rows and GSM truncation;
- private-evidence and external-boundary rows remain unchanged;
- no session-ledger semantics, parser behavior, source parser code, private
  evidence, external corpus content, or protected surface changed;
- the non-claims are strong enough for report-only promotion.

## Next Workflow Action

Next role: Codex E: Module Reviewer / Contract Tester.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #428.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/428

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/426

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/427

Previous merge commit:
376e95bdc5647a7ac5bd14af2c15e543cfd180c6

Branch:
codex/parser-corpus-manifest-metadata-residual

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_manifest_metadata_residual.md

Implementation handoff:
docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md

Expected report:
docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md

Goal:
Review the narrow manifest.metadata residual promotion against the contract.
Verify that only manifest.metadata moved from partial/count_ratchet_only to
covered_report_only/fixture_metadata_only via
parser_corpus_manifest_metadata_boundary_v1, with no parser behavior,
session-ledger semantics, private evidence, external corpus inputs, or
protected-surface changes.

Reviewer focus:
- Confirm issue #428 and tracker #158 remain open.
- Confirm PR #427 merge commit 376e95bdc5647a7ac5bd14af2c15e543cfd180c6 is an ancestor.
- Confirm manifest.metadata now reports covered_report_only with basis
  ["fixture_metadata_only"] and entry
  ["parser_corpus_manifest_metadata_boundary_v1"].
- Confirm feature_equity_corpus_baseline_v1 no longer owns
  manifest.metadata but still owns mythic_edge.confidence_finality_degradation,
  mythic_edge.workbook_row_coverage, and drift_debug.gsm_truncation.
- Confirm report counts are 45 total, 6 committed, 14 synthetic, 16
  report-only, 2 partial, 0 missing, 2 blocked-private, and 5
  blocked-external, while status remains partial_coverage_map_ready.
- Confirm no private Player.log, app-data, firewall/drop, network, live MTGA,
  private smoke, external corpus, generated/runtime artifact, parser behavior,
  session-ledger semantic, workbook/webhook/App Script/Sheets, analytics,
  AI, coaching, CI, merge/deploy, production, or tracker lifecycle surface
  changed.
- Lead with findings if any; otherwise produce a pass verdict and route to
  Codex F.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/428"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/426"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/427"
  previous_merge_commit: "376e95bdc5647a7ac5bd14af2c15e543cfd180c6"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_manifest_metadata_residual.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md"
  verdict: "manifest_metadata_report_only_promotion_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-manifest-metadata-residual"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
}
```
