# Parser Corpus Reconnect Coverage Contract

## Module

Reconnect corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`connection.reconnect` with repo-owned synthetic metadata and existing parser
behavior evidence for reconnect-shaped `ConnectionError` events. It proves
only that Mythic Edge has safe corpus metadata for parser-owned reconnect
result, reconnect outcome, and GRE connection-lost reconnect context handling.
It does not prove live reconnect resilience, network reliability, firewall or
network-drop behavior, private Player.log resilience, runtime health, release
readiness, analytics truth, AI truth, coaching truth, production behavior, or
full Mythic Edge corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/402
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/400
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/401
- Previous merge commit:
  `2417ba79bc3775414c21503719e4b21752d3f669`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-reconnect-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `2417ba79bc3775414c21503719e4b21752d3f669`
- target_artifact:
  `docs/contracts/parser_corpus_reconnect_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_reconnect_coverage.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/parser_corpus_connection_error_payload_coverage.md`
- `docs/contracts/parser_corpus_connection_disconnect_coverage.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_connection_parsers.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, network traces,
  reconnect traces, or external corpus contents.

## Scope Decision

Implementation may proceed as synthetic reconnect corpus metadata coverage.

Codex B considered these paths:

1. Safe synthetic reconnect coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, or blocked-private-evidence status.

Selected path: safe synthetic reconnect coverage.

Reasoning:

- Mythic Edge already has parser-owned reconnect interpretation in
  `src/mythic_edge_parser/parsers/connection_error.py`.
- Focused parser tests already cover reconnect result, reconnect success with
  attempts, reconnect failure, reconnect timeout, and GRE connection-lost
  attempting-reconnect context.
- The coverage claim can be made from metadata and focused tests without
  committing raw Player.log excerpts or adding a private live-network fixture.
- The claim is narrower than live reconnect resilience. It covers only
  parser-owned event recognition and payload metadata.
- Existing adjacent rows stay separate:
  `connection.connection_error_payload` covers generic connection error
  payload metadata, `connection.disconnect` covers close/state-transition
  metadata, and `connection.firewall_or_network_drop` remains outside this
  slice.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the `connection.reconnect`
scenario family. Parser modules and events own the underlying reconnect marker
interpretation. Corpus parity artifacts own only the coverage status claim that
Mythic Edge has safe repo-owned synthetic evidence for this narrow family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence, but it is not a Parser behavior module and is not a
runtime, diagnostics, analytics, workbook, local app, AI, coaching, release,
network-reliability, or production module.

## Truth Owner

Truth owner for `connection.reconnect` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for parser behavior referenced by this coverage:

- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`

Truth owner for adjacent connection/runtime behavior:

- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- diagnostics and runtime-health modules where explicitly contracted

Truth boundary:

- `connection_error.try_parse(...)` owns parser-owned `ConnectionError`
  emission for accepted reconnect result, reconnect outcome, and GRE
  connection-lost markers.
- `ConnectionErrorEvent` owns the event kind and metadata/payload surface.
- Router dispatch owns which log headers can reach the connection error parser.
- Corpus parity artifacts own the report-only coverage row for
  `connection.reconnect`.
- Corpus coverage status is review metadata. It is not parser truth, live
  reconnect truth, firewall truth, network reliability truth, diagnostics
  truth, runtime status truth, workbook truth, analytics truth, AI truth,
  coaching truth, merge readiness, deploy readiness, public/private release
  readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing ConnectionError reconnect parser behavior
  -> bounded synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for connection.reconnect
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change reconnect marker matching, payload shape,
  event classes, router dispatch, parser state, diagnostics behavior, runtime
  status behavior, workbook output, analytics, AI, coaching, release policy,
  or production behavior.
- Corpus metadata must not turn synthetic reconnect evidence into a claim about
  live reconnect success, network outage recovery, firewall drops, private
  Player.log resilience, launch readiness, or broad runtime health.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- match/game identity
- deduplication
- diagnostics report shape
- runtime status artifacts or schema
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- failed delivery artifacts
- workbook exports
- SQLite/local app behavior
- analytics truth
- AI truth
- coaching behavior
- OpenAI/model-provider behavior
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_reconnect_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_connection_parsers.py`
- `docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_reconnect_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- focused router and schema snapshot tests

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- parser event class changes
- router changes
- connection payload shape changes
- explicit `raw_*` field additions
- diagnostics behavior changes
- runtime status changes
- live private smoke execution
- committed raw log fixtures
- private Player.log fixture work
- Manasight corpus import
- connection error payload, disconnect, firewall, network-drop, log-rotation,
  malformed-log, detailed-logs-disabled, timestamp-anomaly, or unknown-entry
  coverage work

## Observed Current Behavior

Observed from `src/mythic_edge_parser/parsers/connection_error.py` and
`tests/test_connection_parsers.py` on the observed base commit:

- `connection_error.try_parse(...)` returns `ConnectionErrorEvent` for accepted
  reconnect-shaped markers.
- `EntryHeader.CONNECTION_MANAGER` content can include the literal
  `[ConnectionManager]` prefix, which the parser strips before matching.
- `Reconnect result : Error` emits payload:

```json
{"error_type": "reconnect_result", "result": "Error"}
```

- Accepted reconnect result values are currently `Connected`, `Error`, and
  `None`.
- `Reconnect succeeded after 3 attempts` emits payload:

```json
{"error_type": "reconnect_outcome", "outcome": "succeeded", "attempts": 3}
```

- `Reconnect failed` emits payload:

```json
{"error_type": "reconnect_outcome", "outcome": "failed", "attempts": null}
```

- `Reconnect timed out` emits payload:

```json
{"error_type": "reconnect_outcome", "outcome": "timed_out", "attempts": null}
```

- `Matchmaking: GRE connection lost, attempting reconnect` emits payload:

```json
{"error_type": "gre_connection_lost"}
```

- Unknown reconnect result values are ignored by the parser.
- Current corpus manifest state keeps `connection.reconnect` inside
  `external_reference_category_boundary` with
  `coverage_status == "blocked_external_boundary"`.
- Current corpus report status summary is:

```json
{
  "covered_synthetic": 13,
  "covered_report_only": 6,
  "partial": 3,
  "missing": 11,
  "blocked_external_boundary": 6,
  "total": 45
}
```

## First Bad Value

The first bad value is the current corpus parity treatment of
`connection.reconnect` as external-only despite existing Mythic Edge parser
behavior evidence:

```yaml
scenario_family: "connection.reconnect"
coverage_status: "blocked_external_boundary"
coverage_basis:
  - "external_reference_only"
mythic_edge_entries:
  - "external_reference_category_boundary"
```

This value is too broad because reconnect result/outcome markers are already
parser-owned. It is still correct to leave broader live reconnect resilience
and firewall/network-drop coverage outside this slice.

## Required Guarantees

Future Codex C must make only the smallest coherent corpus metadata/test
changes needed for these guarantees:

- `connection.reconnect` moves from `blocked_external_boundary` to
  `covered_synthetic`.
- The row uses only repo-owned synthetic metadata and focused parser tests.
- The row's `coverage_basis` is exactly:

```json
["fixture_metadata_only", "parser_behavior_verified"]
```

- The row's `mythic_edge_entries` includes only the new reconnect-specific
  entry.
- The coverage notes explicitly say this proves only parser-owned reconnect
  metadata and does not prove live reconnect resilience or network reliability.
- `connection.connection_error_payload` remains the generic connection error
  payload coverage row.
- `connection.disconnect` remains the close/state-transition coverage row.
- `connection.firewall_or_network_drop` remains unchanged and must not inherit
  reconnect coverage.
- No parser behavior changes are required or authorized.
- No raw logs, private Player.log excerpts, network traces, runtime artifacts,
  generated data, SQLite files, workbook exports, credentials, tokens, keys, or
  webhook URLs may be committed.

Expected status-summary impact, assuming no unrelated changes:

```json
{
  "covered_synthetic": 14,
  "covered_report_only": 6,
  "partial": 3,
  "missing": 11,
  "blocked_external_boundary": 5,
  "total": 45
}
```

## Authorized Manifest Entry

Codex C may add this manifest entry shape, adjusting only ordering and wording
needed to match existing fixture style:

```yaml
entry_id: "connection_reconnect_synthetic_v1"
entry_type: "session_ledger_entry"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/402"
authorized_by_contract: "docs/contracts/parser_corpus_reconnect_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  connection_parser_test: "tests/test_connection_parsers.py"
  router_test: "tests/test_router_unit.py"
  event_schema_snapshot_test: "tests/test_event_schema_snapshots.py"
scenario_families:
  - "connection.reconnect"
parser_event_families:
  - "ConnectionError"
parser_claim_families:
  - "reconnect_result_payload"
  - "reconnect_outcome_payload"
  - "gre_connection_lost_reconnect_context"
  - "reconnect_privacy_boundary"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
known_gaps:
  - "Synthetic reconnect metadata does not prove live reconnect success, network reliability, disconnect behavior, firewall or network-drop behavior, private Player.log resilience, runtime health, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
review_notes:
  - "Synthetic reconnect coverage proves parser-owned ConnectionError reconnect result/outcome metadata only; it does not prove live reconnect resilience, network reliability, firewall/drop behavior, private smoke, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
```

Codex C must remove `connection.reconnect` from the
`external_reference_category_boundary` entry so the report row is not
double-owned by external-reference and Mythic Edge synthetic entries.

## Authorized Session Ledger Entry

Codex C may add this session-ledger entry shape, adjusting only ordering and
wording needed to match existing fixture style:

```yaml
session_id: "connection_reconnect_synthetic_v1"
title: "Synthetic reconnect evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/402"
authorized_by_contract: "docs/contracts/parser_corpus_reconnect_coverage.md"
scenario_families:
  - "connection.reconnect"
format_family: "connection_runtime"
match_shape: "connection_reconnect_signal_only"
record_summary: "synthetic_metadata_summary_only"
parser_coverage:
  event_families:
    ConnectionError: 5
  unknown_entries: 0
  truncation_count: 0
  reconnect_result_entries: 1
  reconnect_outcome_entries: 3
  gre_connection_lost_entries: 1
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Synthetic reconnect metadata does not prove live reconnect success, network reliability, disconnect behavior, firewall or network-drop behavior, private Player.log resilience, runtime health, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
  external_logs_included: false
  decklists_included: false
```

The `ConnectionError: 5` count is metadata for the currently focused
reconnect-shaped test cases: reconnect result, reconnect succeeded, reconnect
failed, reconnect timed out, and GRE connection-lost reconnect context. If
Codex C discovers the focused tests have changed, it must either align the
metadata with current committed tests or route back to Codex B before widening
the claim.

## Required Report Row

`corpus_parity_report` must report:

```yaml
scenario_family: "connection.reconnect"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
mythic_edge_entries:
  - "connection_reconnect_synthetic_v1"
external_reference_status: "reference_category_not_checked"
notes:
  - "Synthetic reconnect coverage proves parser-owned ConnectionError reconnect result/outcome metadata only; it does not prove live reconnect resilience, network reliability, firewall/drop behavior, private smoke, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
```

## Unknowns

- Whether future private live smoke will provide safe local-only reconnect
  review evidence. This contract does not require or authorize live smoke.
- Whether MTGA emits additional reconnect variants beyond the currently
  focused parser tests. Unknown variants remain future parser/diagnostics
  work, not a corpus parity change in this slice.
- Whether `Connected` and `None` reconnect result values should receive
  distinct future fixture metadata. This contract only needs one
  `reconnect_result` metadata claim because current parser behavior and tests
  already define the accepted result vocabulary.

## Suspected Gaps

- `connection.firewall_or_network_drop` remains a separate missing family.
- Live reconnect resilience, retries under actual network interruption,
  launcher/runtime health signals, and private smoke evidence remain outside
  committed corpus parity.
- Corpus metadata cannot prove that a reconnect completed successfully in an
  actual game or preserved match/game state.

## Malformed, Private, And External Input Rules

Allowed inputs:

- Existing focused parser tests.
- Synthetic metadata stored in committed corpus manifest/session-ledger files.
- Public category-level Manasight metadata already represented by the taxonomy
  audit, used only as reference context.

Forbidden inputs:

- Raw private Player.log excerpts.
- Raw Manasight logs, compressed corpora, session payloads, hash lists,
  byte-size lists, capture-date row lists, parser source, or external corpus
  contents.
- Private live reconnect smoke outputs.
- Network traces, IP traces, firewall captures, runtime status files, failed
  posts, generated data, SQLite files, workbook exports, decklists, strategy
  notes, credentials, tokens, keys, or webhook URLs.

Malformed or unknown reconnect parser behavior must remain owned by the parser
contract and focused parser tests. Corpus metadata must not accept malformed
input as coverage evidence.

## Compatibility Expectations

- Existing corpus parity schema versions remain unchanged.
- Existing connection error payload and disconnect rows remain stable.
- Existing report status vocabulary remains unchanged.
- Existing parser event classes and payload shapes remain unchanged.
- Existing diagnostics, golden replay, feature-equity, evidence-ledger,
  analytics, workbook, runtime, local app, AI, and production behavior remain
  unchanged.

## Validation Obligations

Codex C must run, at minimum:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_corpus_reconnect_coverage.md \
  docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_reconnect_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_reconnect_coverage.md \
  docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_reconnect_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C should also run focused router/schema tests if it changes any event
coverage assertion:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py
```

Codex E must verify:

- `connection.reconnect` is no longer owned by
  `external_reference_category_boundary`.
- The report row is exactly scoped to reconnect parser metadata.
- Summary counts changed only as expected.
- No parser source, router behavior, event classes, diagnostics behavior,
  runtime behavior, workbook/webhook/App Script/Sheets behavior, analytics,
  AI, production, or private artifact behavior changed.
- No raw/private/external corpus artifacts were introduced.

Codex F/G must preserve the same protected boundaries and must not use this
coverage row as release readiness, deploy readiness, or tracker-completion
authority.

## Stop Conditions

Stop and route back to Codex B or Codex A if:

- Codex C needs to change parser source or event payload semantics.
- Existing focused reconnect tests no longer support the metadata count or
  claim families.
- The implementation would require committed raw logs, private live smoke
  artifacts, external corpus contents, network traces, generated data, runtime
  artifacts, SQLite files, workbook exports, credentials, tokens, keys, or
  webhook URLs.
- The implementation would change `connection.connection_error_payload`,
  `connection.disconnect`, or `connection.firewall_or_network_drop` beyond
  removing `connection.reconnect` from the external-reference boundary.
- The implementation would make corpus coverage into parser truth, diagnostics
  truth, runtime health truth, analytics truth, AI truth, coaching truth, merge
  readiness, deploy readiness, release readiness, or tracker-completion
  authority.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #402, reconnect corpus coverage.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/402

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_reconnect_coverage.md

Goal:
Implement the smallest metadata/test/report changes needed to mark
connection.reconnect as covered_synthetic using existing parser-owned
ConnectionError reconnect behavior evidence. Do not change parser behavior.

Required scope:
- Add the reconnect synthetic manifest/session-ledger metadata authorized by
  docs/contracts/parser_corpus_reconnect_coverage.md.
- Remove connection.reconnect from the external_reference_category_boundary
  entry.
- Update tests/test_corpus_parity_report.py to assert the new
  connection.reconnect row and expected summary-count shift.
- Inspect tests/test_connection_parsers.py and add focused parser tests only if
  the current committed tests no longer cover reconnect result, succeeded,
  failed, timed_out, and GRE connection-lost attempting-reconnect cases.
- Produce docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md.
- Produce docs/contract_test_reports/parser_corpus_reconnect_coverage.md.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- printf '%s\n' docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
- printf '%s\n' docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
- python3 -m ruff check src tests tools
- git diff --check

Do not target main.
Do not close tracker #158.
Do not claim full Mythic Edge corpus parity.
Do not claim live reconnect resilience, network reliability, firewall/drop
handling, private smoke success, release readiness, analytics truth, AI truth,
coaching truth, or production behavior.
Do not change parser behavior, parser state final reconciliation, parser event
classes, router semantics, match/game identity, deduplication, workbook schema,
webhook payload shape, Apps Script behavior, Google Sheets sync, output
transport, runtime status files, failed posts, workbook exports, analytics
truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI policy,
merge policy, deploy policy, or production behavior.
Do not import, copy, mirror, or commit Manasight raw logs or external corpus
contents.
Do not commit private Player.log excerpts, private local logs, private smoke
outputs, generated data, SQLite files, runtime artifacts, workbook exports,
credentials, tokens, API keys, webhook URLs, network traces, decklists,
strategy notes, or private reports.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/402"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/401"
  previous_merge_commit: "2417ba79bc3775414c21503719e4b21752d3f669"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_reconnect_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_reconnect_coverage.md"
  verdict: "contract_ready_for_synthetic_reconnect_parser_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-reconnect-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_synthetic_parser_metadata"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "printf '%s\\n' docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_corpus_reconnect_coverage.md docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md docs/contract_test_reports/parser_corpus_reconnect_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim live reconnect resilience, network reliability, firewall/drop handling, private smoke success, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, private smoke outputs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, network traces, decklists, strategy notes, or private reports."
```
