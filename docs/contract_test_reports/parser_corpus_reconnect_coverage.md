# Parser Corpus Reconnect Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/402
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/400
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/401
- previous_merge_commit: `2417ba79bc3775414c21503719e4b21752d3f669`
- contract: `docs/contracts/parser_corpus_reconnect_coverage.md`
- branch: `codex/parser-corpus-reconnect-coverage`
- base_branch: `codex/parser-parity`
- selected_path: `covered_synthetic_parser_metadata`
- risk_tier: High

## Source Snapshot

PR #401 is merged into `codex/parser-parity`, and the local implementation
branch starts at the required merge commit:

- local HEAD before implementation:
  `2417ba79bc3775414c21503719e4b21752d3f669`
- merge-base ancestry check: passed
- issue #402 state: open
- tracker #158 state: open

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 13
- covered_report_only: 6
- partial: 3
- missing: 11
- blocked_external_boundary: 6

Pre-change reconnect row:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `connection.reconnect` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |

## Implementation Summary

Added the single synthetic reconnect metadata path authorized by the contract:

- manifest entry: `connection_reconnect_synthetic_v1`
- session ledger entry: `connection_reconnect_synthetic_v1`
- scenario family: `connection.reconnect`
- coverage status: `covered_synthetic`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`
- parser event families:
  - `ConnectionError`
- parser claim families:
  - `reconnect_result_payload`
  - `reconnect_outcome_payload`
  - `gre_connection_lost_reconnect_context`
  - `reconnect_privacy_boundary`

Removed `connection.reconnect` from the
`external_reference_category_boundary` scenario list so the row is owned only
by the reconnect-specific synthetic metadata entry.

The session ledger records five parser-owned reconnect-shaped
`ConnectionError` examples already covered by focused parser tests:

- one reconnect result payload;
- three reconnect outcome payloads;
- one GRE connection-lost reconnect context payload.

No parser source, parser behavior, parser event class, router behavior,
diagnostics behavior, runtime behavior, workbook behavior, webhook behavior,
Apps Script behavior, analytics behavior, AI behavior, coaching behavior, CI
behavior, merge policy, deploy policy, release policy, production behavior,
raw log fixture, private smoke artifact, generated artifact, or external
corpus content was changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 6
- partial: 3
- missing: 11
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 5
- not_applicable: 0

Post-change reconnect and adjacent rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `connection.connection_error_payload` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `connection_error_payload_synthetic_v1` |
| `connection.reconnect` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `connection_reconnect_synthetic_v1` |
| `connection.disconnect` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `connection_disconnect_synthetic_v1` |
| `connection.firewall_or_network_drop` | `missing` | `external_reference_only` | none |

The reconnect row includes this non-claim note:

```text
Synthetic reconnect coverage proves parser-owned ConnectionError reconnect result/outcome metadata only; it does not prove live reconnect resilience, network reliability, firewall/drop behavior, private smoke, release readiness, analytics truth, AI truth, coaching truth, or production behavior.
```

## Privacy And Protected-Surface Assertions

- No raw Player.log excerpts were added.
- No Manasight raw logs, external corpus content, private local logs, private
  smoke outputs, IP/network traces, generated data, SQLite databases, runtime
  artifacts, failed posts, workbook exports, credentials, tokens, API keys,
  webhook URLs, decklists, strategy notes, or private reports were committed.
- The reconnect row is synthetic metadata over existing repo-owned focused
  parser tests.
- `connection.connection_error_payload` remains the generic connection error
  payload row.
- `connection.disconnect` remains the close/state-transition row.
- `connection.firewall_or_network_drop` remains missing.

## Explicit Non-Claims

- This report does not claim full Mythic Edge corpus parity.
- This report does not claim live reconnect resilience.
- This report does not claim network reliability.
- This report does not claim firewall or network-drop behavior.
- This report does not claim private smoke success.
- This report does not claim runtime health.
- This report does not claim release readiness, deploy readiness, merge
  readiness, or production readiness.
- This report does not claim analytics truth, AI truth, coaching truth,
  gameplay advice, or player-mistake labeling.
- This report does not claim issue closure or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md`

## Codex E Contract-Test Review

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The implementation moves only `connection.reconnect` from
`blocked_external_boundary` to `covered_synthetic`, with exact
`coverage_basis: ["fixture_metadata_only", "parser_behavior_verified"]`.
`connection.reconnect` is no longer owned by
`external_reference_category_boundary`, and the report row is owned only by
`connection_reconnect_synthetic_v1`.

The coverage claim remains narrowly scoped to parser-owned `ConnectionError`
reconnect result, reconnect outcome, and GRE connection-lost reconnect context
metadata. It does not claim live reconnect resilience, network reliability,
firewall/drop behavior, private smoke success, runtime health, release
readiness, analytics truth, AI truth, coaching truth, merge readiness, deploy
readiness, production behavior, issue closure, or tracker completion.

Adjacent connection rows remain separate:

- `connection.connection_error_payload`: `covered_synthetic`
- `connection.disconnect`: `covered_synthetic`
- `connection.firewall_or_network_drop`: `missing`

### Protected-Surface Status

No protected parser or downstream behavior drift was found. Reviewer inspection
found no changes under `src`, `tools`, `.github`, `main.py`,
`live_print_filtered_v11_match_summary.py`, `tests/test_connection_parsers.py`,
`tests/test_router_unit.py`, or `tests/test_event_schema_snapshots.py`.

The changed package is limited to:

- `docs/contracts/parser_corpus_reconnect_coverage.md`
- `docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_reconnect_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`

### Validation Reviewed

Codex E reran:

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py`
  - result: 32 passed
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  - result: `partial_coverage_map_ready` with 45 families, 6 committed, 11 missing
- `python3 tools/check_agent_docs.py`
  - result: passed with 0 errors and 0 warnings
- `python3 -m ruff check src tests tools`
  - result: passed
- `git diff --check`
  - result: passed
- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py`
  - result: 23 passed
- path-scoped secret/private marker scan for the changed package
  - result: passed with 0 forbidden and 0 warnings
- path-scoped protected-surface gate for the changed package
  - result: passed with 0 forbidden and 0 warnings
- path-scoped validation selector sanity check for the changed package
  - result: `selection_status: ok`
- `PYTHONPATH=src python3 -m pytest -q`
  - result: 1770 passed

Additional reviewer checks:

- Previous merge commit
  `2417ba79bc3775414c21503719e4b21752d3f669` is an ancestor of `HEAD`.
- Reviewer manifest inspection confirms only
  `connection_reconnect_synthetic_v1` owns `connection.reconnect`.
- Reviewer manifest inspection confirms `connection.reconnect` is absent from
  `external_reference_category_boundary`.
- Reviewer corpus matrix inspection confirms `connection.reconnect` is
  `covered_synthetic` with `["fixture_metadata_only",
  "parser_behavior_verified"]` and `["connection_reconnect_synthetic_v1"]`.
- Reviewer corpus matrix inspection confirms
  `connection.connection_error_payload`, `connection.disconnect`, and
  `connection.firewall_or_network_drop` remain separately scoped.
- Changed-package ASCII scan produced no findings.
- Generated SQLite/database artifact scan produced no findings.

### Remaining Non-Blocking Gaps

This remains synthetic parser metadata coverage. It does not prove live
reconnect resilience, network reliability, firewall or network-drop behavior,
private smoke success, runtime health, release readiness, deploy readiness,
merge readiness, production behavior, analytics truth, AI truth, coaching
truth, full corpus parity, issue closure, or tracker completion.
`connection.firewall_or_network_drop` remains missing and requires separate
contract authority before any future promotion.

### Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/402"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/401"
  previous_merge_commit: "2417ba79bc3775414c21503719e4b21752d3f669"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_reconnect_coverage.md"
  target_artifact: "draft PR for reconnect synthetic parser metadata coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-reconnect-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_synthetic_parser_metadata"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py"
    - "path-scoped secret/private marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector sanity check for changed files"
    - "PYTHONPATH=src python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #402 or tracker #158."
    - "Do not use reconnect corpus coverage as live reconnect resilience, network reliability, release readiness, merge readiness, deploy readiness, production behavior, or tracker-completion authority."
    - "Do not promote connection.firewall_or_network_drop or adjacent connection families without separate contract authority."
    - "Do not change parser behavior, parser event classes, router behavior, runtime behavior, workbook/webhook/App Script/output surfaces, analytics truth, AI truth, coaching truth, CI, or production behavior."
    - "Do not commit raw private Player.log excerpts, raw logs, network traces, private smoke outputs, generated/private/runtime artifacts, credentials, webhook URLs, workbook exports, or external corpus content."
```
