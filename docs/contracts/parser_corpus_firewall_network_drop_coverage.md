# Parser Corpus Firewall / Network-Drop Coverage Contract

## Module

Firewall and network-drop corpus evidence boundary for the parser corpus parity
report.

Plain English: this slice lets Mythic Edge classify exactly
`connection.firewall_or_network_drop` as a blocked private-evidence boundary.
It does not add parser support, committed fixtures, synthetic fixtures, raw
logs, live smoke evidence, network traces, or production-runtime claims.

This contract explicitly prevents Mythic Edge from inheriting
firewall/network-drop coverage from adjacent connection rows:

- `connection.connection_error_payload`
- `connection.reconnect`
- `connection.disconnect`

Those rows prove only their own parser-owned metadata. They do not prove
firewall behavior, Wi-Fi/drop behavior, operating-system networking behavior,
live reconnect resilience, private smoke success, runtime health, release
readiness, analytics truth, AI truth, coaching truth, production behavior, or
full Mythic Edge corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/404
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/402
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/403
- Previous merge commit:
  `8245be1ce8d3bc4f9bfeb090f9e66633768c88ea`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-firewall-network-drop-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `8245be1ce8d3bc4f9bfeb090f9e66633768c88ea`
- target_artifact:
  `docs/contracts/parser_corpus_firewall_network_drop_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md`
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
- `docs/contracts/parser_corpus_reconnect_coverage.md`
- `docs/contract_test_reports/parser_corpus_reconnect_coverage.md`
- `docs/implementation_handoffs/parser_corpus_reconnect_coverage_comparison.md`
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
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, firewall logs, Wi-Fi logs, host diagnostics, router diagnostics, IP
  traces, packet captures, or network traces.

## Scope Decision

Implementation may proceed as a blocked private-evidence boundary.

Codex B considered these paths:

1. `covered_synthetic`.
2. `covered_report_only`.
3. `blocked_private_evidence` / evidence-prerequisite boundary.
4. Leave the family plain `missing` with no manifest entry.

Selected path: `blocked_private_evidence`.

Reasoning:

- Current parser behavior recognizes generic connection-error payloads,
  reconnect result/outcome markers, connection-close payloads, and connection
  state transitions.
- None of those current parser-owned signals proves that Arena was affected by
  a firewall rule, Wi-Fi interruption, ISP/network outage, OS networking
  failure, router behavior, packet loss, or an intentional local network drop.
- A synthetic fixture would overclaim the scenario because synthetic reconnect,
  close, or socket-error text cannot prove a real firewall/network-drop cause.
- A `covered_report_only` row would also overclaim because there is no current
  safe local report proving this family.
- Leaving the row as plain `missing` hides a useful risk distinction: this
  family is not merely unmodeled; honest coverage likely requires either
  approved private/live evidence or a future, narrower parser-owned signal.
- A committed metadata-only `blocked_private_evidence` entry can explain the
  boundary without committing private artifacts or changing parser behavior.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`connection.firewall_or_network_drop` scenario family. Parser modules own
connection marker interpretation. Runtime/diagnostics modules own their own
health or drift reports only when separately contracted. Corpus parity owns
only the coverage-status boundary and its non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance evidence
for context, but it is not a Parser behavior module, diagnostics module,
runtime module, network-reliability module, release-readiness module, local app
module, analytics module, AI module, coaching module, or production module.

## Truth Owner

Truth owner for `connection.firewall_or_network_drop` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for adjacent parser behavior referenced only as non-claim context:

- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`

Truth boundary:

- Corpus parity may say that firewall/network-drop coverage is blocked by
  private/live evidence needs.
- Corpus parity must not say that Mythic Edge has parser support for proving
  firewall or network-drop causes.
- Corpus parity must not infer firewall/network-drop truth from
  `ConnectionError`, `MatchConnectionState`, `TcpConnectionClose`,
  `WebSocketClosed`, reconnect result/outcome markers, GRE connection-lost
  text, socket-error fields, close reasons, or public taxonomy metadata alone.
- Coverage status is review metadata. It is not parser truth, runtime health
  truth, diagnostics truth, network reliability truth, firewall truth, workbook
  truth, analytics truth, AI truth, coaching truth, merge readiness, deploy
  readiness, public/private release readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing adjacent connection parser behavior and report rows
  -> explicit non-claim boundary metadata
  -> corpus parity row for connection.firewall_or_network_drop
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change marker matching, payload shape, event
  classes, router dispatch, parser state, diagnostics behavior, runtime status
  behavior, workbook output, analytics, AI, coaching, release policy, or
  production behavior.
- Corpus metadata must not turn generic connection errors, reconnect events,
  connection closes, connection-state transitions, or socket payload fields
  into proof of firewall/network-drop behavior.

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

- `docs/contracts/parser_corpus_firewall_network_drop_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_connection_parsers.py`
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
- network trace collection
- OS/router/firewall/Wi-Fi diagnostics collection
- synthetic fixture claims for firewall or network-drop causes
- connection error payload, disconnect, reconnect, log-rotation,
  inactivity-timeout, timestamp-anomaly, malformed-log, or unknown-entry
  coverage work

## Public Interface

The public interface remains the existing corpus parity report API:

```python
build_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]
```

The command-line interface remains:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

No new parser function, parser event, router dispatch behavior, runtime status
field, diagnostics section, workbook field, webhook field, Apps Script field,
analytics field, AI field, or production behavior is authorized.

## Observed Current Behavior

Observed on `origin/codex/parser-parity` at
`8245be1ce8d3bc4f9bfeb090f9e66633768c88ea`:

- `connection.firewall_or_network_drop` is present in the corpus taxonomy.
- The corpus parity report currently shows:

```yaml
scenario_family: "connection.firewall_or_network_drop"
coverage_status: "missing"
coverage_basis:
  - "external_reference_only"
mythic_edge_entries: []
external_reference_status: "reference_category_not_checked"
notes: []
```

- The current corpus summary is:

```json
{
  "covered_committed": 6,
  "covered_synthetic": 14,
  "covered_report_only": 6,
  "partial": 3,
  "missing": 11,
  "deferred": 0,
  "blocked_private_evidence": 0,
  "blocked_external_boundary": 5,
  "not_applicable": 0
}
```

- `connection.connection_error_payload` is `covered_synthetic` and proves only
  parser-owned `ConnectionError` payload metadata.
- `connection.reconnect` is `covered_synthetic` and proves only parser-owned
  reconnect result/outcome metadata.
- `connection.disconnect` is `covered_synthetic` and proves only parser-owned
  connection close and connection state-transition metadata.
- The focused connection tests include socket-error-like payloads, reconnect
  markers, close payloads, and state transitions, but they do not prove actual
  firewall or network-drop cause.

## First Bad Value

The first bad value is any row, note, fixture, or test assertion that marks
`connection.firewall_or_network_drop` as covered because another connection
family is covered.

Examples of bad values:

```yaml
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
parser_claim_families:
  - "reconnect_outcome_payload"
```

```yaml
coverage_status: "covered_report_only"
coverage_basis:
  - "local_report_only"
notes:
  - "Reconnect and disconnect coverage prove firewall/network-drop handling."
```

The current plain `missing` row is not unsafe, but it is under-specified. The
required improvement is to make the evidence prerequisite explicit without
claiming coverage.

## Required Guarantees

Future Codex C must make only the smallest coherent corpus metadata/test
changes needed for these guarantees:

- `connection.firewall_or_network_drop` moves from plain `missing` to
  `blocked_private_evidence`.
- The row uses a committed metadata boundary only; it does not add a committed
  raw log, committed synthetic log fixture, local private artifact, or session
  ledger entry.
- The row's `coverage_basis` is exactly:

```json
["local_report_only"]
```

- The row's `mythic_edge_entries` includes only:

```json
["firewall_network_drop_private_evidence_boundary_v1"]
```

- The row's notes state that firewall/network-drop coverage requires future
  approved private/live evidence or a narrower parser-owned signal, and that
  adjacent connection rows do not prove it.
- `connection.connection_error_payload`, `connection.reconnect`, and
  `connection.disconnect` remain unchanged.
- `log_runtime.rotation`, `timer.inactivity_timeout`, and other
  external-boundary rows remain unchanged.
- No parser behavior changes are required or authorized.
- No raw logs, private Player.log excerpts, private smoke outputs, IP/network
  traces, firewall logs, Wi-Fi logs, OS/router diagnostics, generated data,
  SQLite files, workbook exports, credentials, tokens, keys, or webhook URLs
  may be committed.

Expected status-summary impact, assuming no unrelated changes:

```json
{
  "covered_committed": 6,
  "covered_synthetic": 14,
  "covered_report_only": 6,
  "partial": 3,
  "missing": 10,
  "deferred": 0,
  "blocked_private_evidence": 1,
  "blocked_external_boundary": 5,
  "not_applicable": 0
}
```

The overall report status remains `partial_coverage_map_ready`.

## Authorized Manifest Entry

Codex C may add this manifest entry shape, adjusting only ordering and wording
needed to match existing fixture style:

```yaml
entry_id: "firewall_network_drop_private_evidence_boundary_v1"
entry_type: "local_private_report_summary"
source_kind: "local_private_report_only"
commit_status: "local_report_only"
privacy_class: "local_private_not_committed"
sanitization_status: "requires_review"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/404"
authorized_by_contract: "docs/contracts/parser_corpus_firewall_network_drop_coverage.md"
paths: {}
scenario_families:
  - "connection.firewall_or_network_drop"
parser_event_families: []
parser_claim_families:
  - "firewall_network_drop_private_evidence_required"
  - "connection_adjacent_rows_non_claim"
  - "network_reliability_non_claim"
  - "private_artifact_boundary"
coverage_status: "blocked_private_evidence"
coverage_basis:
  - "local_report_only"
known_gaps:
  - "Firewall/network-drop corpus coverage requires future approved private/live evidence or a narrower parser-owned signal; generic connection errors, reconnect metadata, disconnect metadata, public taxonomy, and synthetic text do not prove firewall behavior, Wi-Fi/drop behavior, OS/router/network diagnostics, runtime health, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
review_notes:
  - "Firewall/network-drop coverage is blocked by private/live evidence requirements; adjacent connection error, reconnect, and disconnect corpus rows do not prove firewall/drop behavior, network reliability, private smoke success, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
```

No session-ledger entry is authorized in this slice. The committed manifest row
is a boundary marker, not a committed fixture and not a local private report.

## Required Report Row

`corpus_parity_report` must report:

```yaml
scenario_family: "connection.firewall_or_network_drop"
coverage_status: "blocked_private_evidence"
coverage_basis:
  - "local_report_only"
mythic_edge_entries:
  - "firewall_network_drop_private_evidence_boundary_v1"
external_reference_status: "reference_category_not_checked"
notes:
  - "Firewall/network-drop coverage is blocked by private/live evidence requirements; adjacent connection error, reconnect, and disconnect corpus rows do not prove firewall/drop behavior, network reliability, private smoke success, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
```

The report `gaps` entry for this family must include
`private_evidence_required` in `blocked_by`.

## Unknowns

- Whether a future private live smoke can safely produce a local-only report
  that supports this family without committing raw logs or traces.
- Whether MTGA exposes a future parser-owned marker that clearly distinguishes
  firewall/network-drop cause from generic connection errors.
- Whether a safe, synthetic-only fixture could ever prove this family. This
  contract says no for the current repo because synthetic text cannot prove
  external network cause.

## Suspected Gaps

- Current parser behavior has no first-class firewall/network-drop event.
- Current diagnostics and runtime status reports do not own firewall/network
  reliability truth in this contract.
- Current corpus metadata can explain the blocker but cannot prove support.
- Public Manasight taxonomy can identify the scenario family but cannot prove
  Mythic Edge support.

## Malformed, Private, And External Input Rules

Allowed inputs:

- Existing Mythic Edge docs, contracts, handoffs, reports, source files, and
  focused tests on `codex/parser-parity`.
- Existing corpus manifest and session ledger metadata.
- Public category-level Manasight metadata already represented by the taxonomy
  audit, used only as reference context.

Forbidden inputs:

- Raw private Player.log excerpts.
- Private local logs or private smoke outputs.
- IP/network traces, firewall logs, Wi-Fi logs, hostnames, router logs, OS
  network diagnostics, pfctl output, packet captures, or similar local network
  evidence.
- Raw Manasight logs, compressed corpora, session payloads, hash lists,
  byte-size lists, capture-date row lists, parser source, or external corpus
  contents.
- Runtime status files, failed delivery artifacts, generated data, SQLite files, workbook
  exports, decklists, strategy notes, credentials, tokens, keys, or webhook
  URLs.

Malformed or unknown connection parser behavior remains owned by parser
contracts and focused parser tests. Corpus metadata must not accept malformed
input as firewall/network-drop coverage evidence.

## Compatibility Expectations

- Existing corpus parity schema versions remain unchanged.
- Existing report status vocabulary remains unchanged.
- Existing adjacent connection rows remain unchanged.
- Existing parser event classes and payload shapes remain unchanged.
- Existing session ledger shape remains unchanged.
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
  docs/contracts/parser_corpus_firewall_network_drop_coverage.md \
  docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_firewall_network_drop_coverage.md \
  docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C should also run focused router/schema tests if it changes any event or
schema assertion:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py
```

Codex E must verify:

- `connection.firewall_or_network_drop` is `blocked_private_evidence`, not
  `covered_synthetic` or `covered_report_only`.
- The row is exactly scoped to a private/live evidence prerequisite.
- `gaps[].blocked_by` includes `private_evidence_required`.
- Summary counts changed only as expected: `missing` decreases by one and
  `blocked_private_evidence` increases by one.
- Adjacent connection rows remain unchanged.
- No session ledger entry was added for firewall/network-drop.
- No parser source, router behavior, event classes, diagnostics behavior,
  runtime behavior, workbook/webhook/App Script/Sheets behavior, analytics,
  AI, production, or private artifact behavior changed.
- No raw/private/external corpus artifacts or network traces were introduced.

Codex F/G must preserve the same protected boundaries and must not use this
boundary row as release readiness, deploy readiness, or tracker-completion
authority.

## Stop Conditions

Stop and route back to Codex B or Codex A if:

- Codex C needs to change parser source or event payload semantics.
- Codex C finds an existing parser-owned firewall/network-drop signal that
  might justify synthetic coverage instead of a blocked boundary.
- The implementation would require a committed raw log, private live smoke
  artifact, external corpus content, network trace, OS/router/firewall/Wi-Fi
  diagnostic, generated data, runtime artifact, SQLite file, workbook export,
  credential, token, key, or webhook URL.
- The implementation would change adjacent connection rows beyond preserving
  their current non-claim language.
- The implementation would make corpus coverage into parser truth, diagnostics
  truth, runtime health truth, network reliability truth, analytics truth, AI
  truth, coaching truth, merge readiness, deploy readiness, release readiness,
  or tracker-completion authority.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #404, firewall/network-drop corpus evidence boundary.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/404

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_firewall_network_drop_coverage.md

Goal:
Implement the smallest metadata/test/report changes needed to move
connection.firewall_or_network_drop from plain missing to a
blocked_private_evidence boundary. Do not change parser behavior.

Required scope:
- Add only the committed metadata boundary entry authorized by
  docs/contracts/parser_corpus_firewall_network_drop_coverage.md.
- Do not add a session-ledger entry for firewall/network-drop.
- Update tests/test_corpus_parity_report.py to assert the new row, expected
  gap blocked_by value, and expected summary-count shift.
- Preserve connection.connection_error_payload, connection.reconnect, and
  connection.disconnect rows unchanged.
- Produce docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md.
- Produce docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- printf '%s\n' docs/contracts/parser_corpus_firewall_network_drop_coverage.md docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
- printf '%s\n' docs/contracts/parser_corpus_firewall_network_drop_coverage.md docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
- python3 -m ruff check src tests tools
- git diff --check

Do not target main.
Do not close tracker #158.
Do not claim full Mythic Edge corpus parity.
Do not claim parser support from public taxonomy metadata alone.
Do not claim firewall/network-drop behavior, network reliability, private smoke success, runtime health, release readiness, analytics truth, AI truth, coaching truth, production behavior, or full connection parity.
Do not reopen or broaden existing connection error payload, disconnect, reconnect, log-rotation, or inactivity-timeout boundaries.
Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents.
Do not commit private Player.log excerpts, private local logs, private smoke outputs, IP/network traces, firewall logs, Wi-Fi logs, OS/router diagnostics, generated/private/runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, card choices, or private strategy notes.
Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, drift report behavior, golden replay behavior, feature-equity behavior, evidence-ledger behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, runtime status files, failed delivery artifacts, workbook exports, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy without a new explicit contract.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/404"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/402"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/403"
  previous_merge_commit: "8245be1ce8d3bc4f9bfeb090f9e66633768c88ea"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_firewall_network_drop_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md"
  verdict: "contract_ready_for_blocked_private_evidence_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-firewall-network-drop-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "blocked_private_evidence_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "printf '%s\\n' docs/contracts/parser_corpus_firewall_network_drop_coverage.md docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_corpus_firewall_network_drop_coverage.md docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim parser support from public taxonomy metadata alone."
    - "Do not claim firewall/network-drop behavior, network reliability, private smoke success, runtime health, release readiness, analytics truth, AI truth, coaching truth, production behavior, or full connection parity."
    - "Do not reopen or broaden existing connection error payload, disconnect, reconnect, log-rotation, or inactivity-timeout boundaries."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, private smoke outputs, IP/network traces, firewall logs, Wi-Fi logs, OS/router diagnostics, generated/private/runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, card choices, or private strategy notes."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```
