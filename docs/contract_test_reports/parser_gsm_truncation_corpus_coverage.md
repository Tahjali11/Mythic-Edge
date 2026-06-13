# Parser GSM Truncation Corpus Coverage Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/351

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_gsm_truncation_corpus_coverage.md`

## Required Workflow References

- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/gsm-truncation-corpus-coverage`

Changed-file package reviewed:

- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- `docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Findings

No blocking findings.

No non-blocking findings requiring follow-up were identified in this contract
slice.

## Contract Summary

Issue #351 adds narrow GSM truncation/data-loss corpus coverage to the parser
corpus parity report. The implementation must keep the work metadata/test-only,
move only the `drift_debug.gsm_truncation` corpus row to honest
`covered_synthetic` coverage, preserve the existing parser-owned truncation
truth boundary, and avoid claiming recovered GameState data or readiness.

## Internal Project Area Reviewed

Corpus / Provenance.

## Bridge-Code Status Reviewed

`bridge_code`: existing parser-owned `TruncationEvent` and adjacent parser /
diagnostics / drift tests are consumed as evidence by corpus metadata and report
tests. No reverse flow from corpus metadata into parser behavior was found.

## Checks Run

```bash
gh issue view 351 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body,labels,comments
gh issue view 158 --repo Tahjali11/Mythic-Edge --json number,title,state,url
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from mythic_edge_parser.app.corpus_parity_report import build_corpus_parity_report
report = build_corpus_parity_report(Path("tests/fixtures/parser_corpus/corpus_manifest.v1.json"), session_ledger_path=Path("tests/fixtures/parser_corpus/session_ledger.v1.json"))
row = next(r for r in report["coverage_matrix"] if r["scenario_family"] == "drift_debug.gsm_truncation")
print("summary", report["summary"])
print("gsm_row", row)
print("status", report["status"])
PY
python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py
python3 -m pytest -q tests
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
git diff --no-index --check /dev/null docs/contracts/parser_gsm_truncation_corpus_coverage.md
git diff --no-index --check /dev/null docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md
printf '%s\n' docs/contracts/parser_gsm_truncation_corpus_coverage.md docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_gsm_truncation_corpus_coverage.md docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_gsm_truncation_corpus_coverage.md docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

## Results

Passed:

- Issue #351 and tracker #158 are open.
- Corpus parity CLI: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 28 missing)`.
- Row inspection:
  - report status remains `partial_coverage_map_ready`;
  - summary is `covered_synthetic: 2`, `partial: 3`, `missing: 28`;
  - `drift_debug.gsm_truncation` row is `covered_synthetic`;
  - GSM row entries are `feature_equity_corpus_baseline_v1` and
    `gsm_truncation_marker_synthetic_v1`;
  - GSM row basis is `count_ratchet_only`, `diagnostics_only`,
    `fixture_metadata_only`, and `parser_behavior_verified`.
- `python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py` -> `14 passed`.
- `python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py` -> `38 passed`.
- `python3 -m pytest -q tests` -> `1765 passed`.
- `python3 -m ruff check src tests tools` -> passed.
- `python3 tools/check_agent_docs.py` -> passed.
- `git diff --check` -> passed.
- `git diff --no-index --check` for the untracked contract and handoff printed
  no whitespace errors. Exit code `1` is expected because the files differ from
  `/dev/null`.
- Path-scoped secret/private-marker scan -> passed, `forbidden: 0`,
  `warnings: 0`.
- Path-scoped protected-surface gate -> passed, `forbidden: 0`, `warnings: 0`.
- Path-scoped validation selector -> `selection_status: ok`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GSMCOV-E-001 | N/A | `not_reproduced` | No blocking contract mismatch found | not_blocking | Codex E review obligation for issue #351 | Focused tests, full pytest, row inspection, secret/private scan, protected-surface gate, and selector all passed | F |

## Confirmed Contract Matches

- The new corpus manifest entry
  `gsm_truncation_marker_synthetic_v1` is present and uses
  `coverage_status: covered_synthetic`.
- The new session-ledger entry records one `Truncation` event, zero unknown
  entries, one truncation count, and zero game rows.
- The GSM corpus row combines the existing feature-equity baseline with the new
  synthetic GSM truncation marker entry.
- The GSM corpus row is not `covered_committed`.
- The report notes preserve the boundary that GSM truncation is data-loss
  evidence, not recovered GameState truth.
- Summary counts move from the contracted baseline to `covered_synthetic: 2`
  and `partial: 3` while the overall report remains partial.
- Tests cover manifest/session validation, summary delta, row status, basis,
  entries, and the no-`covered_committed` guard.
- No parser behavior, `TruncationEvent` shape, router behavior, diagnostics
  behavior, replay behavior, workbook schema, webhook payload shape, Apps
  Script behavior, output transport, analytics truth, AI truth, or production
  behavior changed.
- No raw/private logs, external corpus files, generated artifacts, SQLite
  files, workbook exports, credentials, tokens, keys, or webhook URLs were
  added.

## Contract Mismatches

None.

## Missing Tests

None blocking. Focused tests cover the required corpus metadata and report row
semantics, and adjacent truncation / diagnostics / drift / router tests pass.

## Drift Notes

- Local worktree drift: the contract and handoff are untracked, while the
  fixture and test updates are tracked modifications. Codex F should stage only
  the reviewed package files.
- Issue lifecycle drift: issue #351 and tracker #158 remain open, as expected.
- Tracker scope drift: tracker #158 remains incomplete; this issue must not be
  treated as corpus parity completion.
- No workbook, deployment, runtime, parser behavior, or local-data drift was
  found in the reviewed package.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #351 under tracker #158.

Review:
- docs/contracts/parser_gsm_truncation_corpus_coverage.md
- docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md
- docs/contract_test_reports/parser_gsm_truncation_corpus_coverage.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py

Goal:
Stage only the reviewed GSM truncation corpus coverage package, commit, push,
and open or update a draft PR. Do not target main directly and do not close
tracker #158.

Validation to preserve:
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py
- python3 -m pytest -q tests
- python3 -m ruff check src tests tools
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker and protected-surface checks for reviewed files

Do not change parser behavior, TruncationEvent shape, router behavior,
diagnostics behavior, replay behavior, workbook schema, webhook payload shape,
Apps Script behavior, analytics truth, AI truth, production behavior, or any
raw/private/external/generated/local artifacts.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/351"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_gsm_truncation_corpus_coverage.md"
  target_artifact: "draft PR for GSM truncation corpus coverage package"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/gsm-truncation-corpus-coverage"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json -> partial_coverage_map_ready"
    - "row inspection -> drift_debug.gsm_truncation covered_synthetic, not covered_committed"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py -> 14 passed"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py -> 38 passed"
    - "python3 -m pytest -q tests -> 1765 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "python3 tools/check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private-marker scan -> passed"
    - "path-scoped protected-surface gate -> passed"
    - "path-scoped validation selector -> selection_status ok"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158."
    - "Do not change parser behavior, TruncationEvent shape, router behavior, diagnostics behavior, replay behavior, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, or production behavior."
    - "Do not commit raw/private Player.log excerpts, external raw corpora, local logs, generated data, runtime artifacts, SQLite files, workbook exports, credentials, tokens, keys, or webhook URLs."
    - "Do not reconstruct missing GameState data from truncation markers."
```
