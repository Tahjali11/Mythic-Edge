# Parser Corpus Reconnect Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/402

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_reconnect_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`reconnect_synthetic_parser_metadata_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `connection_reconnect_synthetic_v1`.
  - Removed `connection.reconnect` from `external_reference_category_boundary`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching synthetic reconnect metadata.
- `tests/test_corpus_parity_report.py`
  - Updated summary-count expectations.
  - Added focused manifest, session-ledger, and matrix-row assertions for
    `connection.reconnect`.
  - Preserved exact adjacent row assertions for
    `connection.connection_error_payload`, `connection.disconnect`, and
    `connection.firewall_or_network_drop`.
- `docs/contract_test_reports/parser_corpus_reconnect_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_reconnect_coverage.md`

No parser source, parser behavior, parser event class, router behavior,
diagnostics source, runtime source, workbook export, webhook surface, Apps
Script surface, analytics source, AI/coaching behavior, generated/private
artifact, raw fixture, private log, network trace, runtime status file, failed
post, workbook export, or external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 13
- covered_report_only: 6
- partial: 3
- missing: 11
- blocked_external_boundary: 6
- `connection.reconnect`: `blocked_external_boundary`
- `connection.connection_error_payload`: `covered_synthetic`
- `connection.disconnect`: `covered_synthetic`
- `connection.firewall_or_network_drop`: `missing`

Repo inspection confirmed `tests/test_connection_parsers.py` already covers
the contract-required reconnect-shaped `ConnectionError` cases:

- `Reconnect result : Error`;
- `Reconnect succeeded after 3 attempts`;
- `Reconnect failed`;
- `Reconnect timed out`;
- `Matchmaking: GRE connection lost, attempting reconnect`.

Because those tests were already present, no parser tests or parser source
changes were needed.

## Contract Changes Implemented

Implemented exactly one authorized coverage movement:

| Scenario family | Before | After |
| --- | --- | --- |
| `connection.reconnect` | `blocked_external_boundary` | `covered_synthetic` |

Added the required reconnect metadata:

- entry id: `connection_reconnect_synthetic_v1`
- session id: `connection_reconnect_synthetic_v1`
- source kind: `synthetic_committed_fixture`
- privacy class: `synthetic_committable`
- sanitization status: `synthetic`
- parser event families:
  - `ConnectionError`
- parser claim families:
  - `reconnect_result_payload`
  - `reconnect_outcome_payload`
  - `gre_connection_lost_reconnect_context`
  - `reconnect_privacy_boundary`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`

The coverage row intentionally does not claim live reconnect resilience,
network reliability, firewall/drop behavior, private smoke, release readiness,
analytics truth, AI truth, coaching truth, or production behavior.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- the `connection_reconnect_synthetic_v1` manifest entry shape;
- `parser_event_families: ["ConnectionError"]`;
- exact `covered_synthetic` status and
  `["fixture_metadata_only", "parser_behavior_verified"]` basis;
- reconnect claim families;
- known-gap and review-note non-claims;
- session-ledger parser coverage counts:
  - `ConnectionError: 5`
  - `reconnect_result_entries: 1`
  - `reconnect_outcome_entries: 3`
  - `gre_connection_lost_entries: 1`
  - `unknown_entries: 0`
  - `truncation_count: 0`
- game-row non-applicability;
- redaction flags;
- report summary movement from 13 to 14 synthetic families and 6 to 5
  external-boundary families;
- the exact `connection.reconnect` matrix row;
- adjacent connection rows remain separate.

## Contract Mismatches

No blocking mismatches were found.

The selected `covered_synthetic_parser_metadata` path was viable without
parser behavior, parser test, router, event schema, runtime, diagnostics, or
private smoke changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future coverage for live reconnect resilience, firewall/network-drop behavior,
private smoke, runtime health, release readiness, analytics truth, AI truth,
coaching truth, or production behavior needs separate contract authority.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata and
boundary assertions.

No new `tests/test_connection_parsers.py` cases were added because the existing
committed tests already cover the five reconnect-shaped parser evidence cases
named by the contract.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py
```

- passed: 32 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 11 missing)`

```bash
python3 tools/check_agent_docs.py
```

- passed: checked_files 32, errors 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
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
printf '%s\n' docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py
```

- passed: 23 passed

```bash
for f in docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md; do git diff --no-index --check /dev/null "$f"; rc=$?; if [ "$rc" -eq 1 ]; then true; elif [ "$rc" -ne 0 ]; then exit "$rc"; fi; done
```

- passed

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py
```

- passed: no matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

```bash
git diff --name-only -- src tests/test_connection_parsers.py tests/test_router_unit.py tests/test_event_schema_snapshots.py tools main.py live_print_filtered_v11_match_summary.py .github
```

- passed: no parser/source, focused connection parser test, router test,
  event schema test, tools, app entrypoint, or CI paths changed

## Open Risks

- `connection.reconnect` is now covered only as synthetic parser metadata.
- The coverage row does not prove live reconnect success, network reliability,
  firewall/drop handling, private smoke success, runtime health, release
  readiness, analytics truth, AI truth, coaching truth, or production
  behavior.
- `connection.firewall_or_network_drop` remains missing.
- Tracker #158 remains open.

## Next Recommended Role

Codex E: Module Reviewer / Contract-Test Reviewer.

Codex E should verify that the implementation is metadata/test/report-only,
that `connection.reconnect` is no longer owned by
`external_reference_category_boundary`, that adjacent connection rows remain
separate, and that no parser/runtime/downstream behavior changed.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer / Contract-Test Reviewer for issue #402,
  parser corpus reconnect synthetic metadata coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/402
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/400
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/401
    - Previous merge commit: 2417ba79bc3775414c21503719e4b21752d3f669
    - Branch: codex/parser-corpus-reconnect-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_reconnect_coverage.md
    - Handoff: docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_reconnect_coverage.md

  Goal:
    Review the Codex C implementation against the contract. Confirm whether the
    package is ready for Codex F submission without overclaiming reconnect
    resilience or changing protected behavior.

  Review:
    - Confirm `connection.reconnect` moved from `blocked_external_boundary` to
      `covered_synthetic` only.
    - Confirm `coverage_basis` is exactly
      `["fixture_metadata_only", "parser_behavior_verified"]`.
    - Confirm `connection.reconnect` is no longer owned by
      `external_reference_category_boundary`.
    - Confirm `mythic_edge_entries` is exactly
      `["connection_reconnect_synthetic_v1"]`.
    - Confirm the row proves only parser-owned `ConnectionError`
      reconnect-result/outcome metadata.
    - Confirm `connection.connection_error_payload`,
      `connection.disconnect`, and `connection.firewall_or_network_drop`
      remain separate and unchanged in meaning.
    - Confirm no parser behavior, parser event classes, router behavior,
      runtime, diagnostics, workbook, webhook, Apps Script, analytics,
      AI/coaching, CI, generated/private artifacts, raw logs, network traces,
      private smoke, or external corpus content changed.
    - Rerun focused validation and record the verdict.

  Suggested validation:
    - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 tools/check_agent_docs.py
    - python3 -m ruff check src tests tools
    - git diff --check
    - path-scoped secret/private marker scan for changed files
    - path-scoped protected-surface check for changed files
    - path-scoped selector sanity check for changed files

  Do not:
    - Target main directly.
    - Close #402 or tracker #158 unless separately authorized.
    - Claim full corpus parity, live reconnect resilience, network reliability,
      firewall/drop behavior, private smoke success, runtime health, release
      readiness, analytics truth, AI truth, coaching truth, production
      behavior, merge readiness, deploy readiness, or tracker completion.
    - Add parser behavior, parser event classes, runtime behavior, workbook,
      webhook, Apps Script, analytics, AI/coaching, CI, generated/private
      artifacts, raw logs, network traces, private smoke, or external corpus
      content.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/402"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/401"
  previous_merge_commit: "2417ba79bc3775414c21503719e4b21752d3f669"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_reconnect_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_reconnect_coverage.md"
  verdict: "reconnect_synthetic_parser_metadata_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-reconnect-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_synthetic_parser_metadata"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/402"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/401"
  previous_merge_commit: "2417ba79bc3775414c21503719e4b21752d3f669"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_reconnect_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_reconnect_coverage.md"
  verdict: "reconnect_synthetic_parser_metadata_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-reconnect-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_synthetic_parser_metadata"
```
