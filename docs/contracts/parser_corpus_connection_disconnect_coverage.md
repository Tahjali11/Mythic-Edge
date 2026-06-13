# Parser Corpus Connection Disconnect Coverage Contract

## Module

Connection disconnect corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`connection.disconnect` with repo-owned synthetic metadata and existing parser
behavior evidence for disconnect-style parser events. It proves only that
Mythic Edge has safe corpus metadata for parser-owned connection close and
connection state-transition handling. It does not prove live reconnect
behavior, firewall or network-drop behavior, private Player.log resilience,
release readiness, full runtime health, full connection parity, or full
Mythic Edge corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/366
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/364
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/365
- Previous merge commit:
  `5513f406f227fe53bea87de73bf6e86f4b58d30a`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-connection-disconnect-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `5513f406f227fe53bea87de73bf6e86f4b58d30a`
- target_artifact:
  `docs/contracts/parser_corpus_connection_disconnect_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_connection_disconnect_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_connection_disconnect_coverage.md`
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
- `docs/contracts/parser_field_level_parity_audit.md`
- `docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/parsers/connection_error.py`
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
  byte-size row lists, capture-date row lists, parser source, or external
  corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the `connection.disconnect`
scenario family. Parser modules and events own the underlying connection
state-transition and connection-close interpretation. Corpus parity artifacts
own only the coverage status claim that Mythic Edge has safe repo-owned
evidence for this narrow family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence, but it is not a Parser behavior module and is not a
runtime, diagnostics, analytics, workbook, local app, AI, coaching, release,
or production module.

## Truth Owner

Truth owner for `connection.disconnect` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for parser behavior referenced by this coverage:

- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`

Truth owner for adjacent connection/runtime behavior:

- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/router.py`
- diagnostics and runtime-health modules where explicitly contracted

Truth boundary:

- `connection_state.try_parse(...)` owns parser-owned
  `MatchConnectionState` emission for accepted `STATE CHANGED` Unity lines.
- `connection_close.try_parse(...)` owns parser-owned
  `TcpConnectionClose` and `WebSocketClosed` emission for accepted Unity JSON
  close markers.
- `MatchConnectionStateEvent`, `TcpConnectionCloseEvent`, and
  `WebSocketClosedEvent` own the event kinds and interactive-dispatch event
  identities.
- Router dispatch owns which log headers can reach these parsers.
- Corpus parity artifacts own the report-only coverage row for
  `connection.disconnect`.
- Corpus coverage status is review metadata. It is not parser truth, runtime
  health truth, reconnect truth, firewall truth, network reliability truth,
  diagnostics truth, workbook truth, analytics truth, AI truth, coaching
  truth, merge readiness, deploy readiness, public/private release readiness,
  or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing MatchConnectionState / TcpConnectionClose / WebSocketClosed parser behavior
  -> bounded synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for connection.disconnect
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change connection parser marker matching, payload
  shape, event classes, router dispatch, parser state, diagnostics behavior,
  runtime status behavior, workbook output, analytics, AI, coaching, release
  policy, or production behavior.
- Corpus metadata must not turn synthetic disconnect/close/state-transition
  evidence into a claim about live reconnects, firewall drops, network outage
  handling, private Player.log resilience, launch readiness, or broad runtime
  health.

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

- `docs/contracts/parser_corpus_connection_disconnect_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_connection_parsers.py`
- `docs/implementation_handoffs/parser_corpus_connection_disconnect_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_connection_disconnect_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/parsers/connection_error.py`
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
- reconnect, firewall, network-drop, log-rotation, malformed-log,
  detailed-logs-disabled, timestamp-anomaly, or unknown-entry coverage work
- additional connection error payload work already owned by issue #364
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, final integration, and production surfaces

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

The command-line interface also remains:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Codex C may use the existing manifest and session-ledger schemas. This
contract does not authorize a new Python API, CLI flag, environment variable,
runtime route, workbook column, webhook field, Apps Script mapping, SQLite
schema, AI/model-provider behavior, or production integration.

## Observed Current Behavior

Observed from `origin/codex/parser-parity` at
`5513f406f227fe53bea87de73bf6e86f4b58d30a`:

- Tracker #158 is open.
- Issue #366 is open as the connection disconnect corpus coverage child.
- The current corpus parity report returns
  `partial_coverage_map_ready (45 families, 6 committed, 24 missing)`.
- `connection.disconnect` exists in the corpus taxonomy.
- No committed manifest entry currently owns `connection.disconnect`.
- No session-ledger entry currently owns `connection.disconnect`.
- `connection.connection_error_payload` is already `covered_synthetic` through
  issue #364 and `connection_error_payload_synthetic_v1`.
- `connection.reconnect` is represented only by
  `external_reference_category_boundary` and is
  `blocked_external_boundary`.
- `connection.firewall_or_network_drop` is a taxonomy family but has no Mythic
  Edge-owned coverage entry.

Observed parser behavior:

- `src/mythic_edge_parser/parsers/connection_state.py` emits
  `MatchConnectionState` for accepted Unity `STATE CHANGED` JSON payloads.
- `MatchConnectionState` payload currently contains parser-owned `old` and
  `new` string transition values.
- `connection_state.py` rejects non-Unity headers, malformed JSON,
  non-mapping JSON, and non-string transition values.
- `src/mythic_edge_parser/parsers/connection_close.py` emits
  `TcpConnectionClose` for accepted `Client.TcpConnection.Close` Unity JSON
  markers.
- `connection_close.py` emits `WebSocketClosed` for accepted
  `GREConnection.HandleWebSocketClosed` Unity JSON markers.
- `TcpConnectionClose` and `WebSocketClosed` payloads are the parsed JSON
  payloads emitted directly; stable normalized fields are not separated from
  raw payload content.
- `connection_close.py` rejects non-Unity headers, malformed JSON,
  non-mapping JSON, and unrelated Unity lines.
- `MatchConnectionStateEvent`, `TcpConnectionCloseEvent`, and
  `WebSocketClosedEvent` are interactive-dispatch parser event kinds.
- Router dispatch sends `UNITY_CROSS_THREAD_LOGGER` entries to
  `connection_state`, then `connection_close`, then `connection_error` after
  more specific parsers.

Observed prior audit guidance:

- The field-level parity audit classified `MatchConnectionState` as
  `documented_partial`.
- The same audit classified `TcpConnectionClose` and `WebSocketClosed` as
  `raw_preserved_only`.
- `MatchConnectionState` has no explicit `type` field and no explicit
  `raw_connection_state` field.
- `TcpConnectionClose` has no explicit `type` field and no explicit
  `raw_tcp_connection_close` field.
- `WebSocketClosed` has no explicit `type` field and no explicit
  `raw_websocket_closed` field.
- These are observed payload-shape gaps, not authorized behavior changes in
  this issue.

## Required Guarantees

### In-Scope Scenario Family

Only this scenario family is in scope:

```text
connection.disconnect
```

Codex C may move this family from `missing` to `covered_synthetic` only if it
adds safe repo-owned synthetic metadata and focused tests that keep all
non-claims explicit.

### Required Manifest Entry

If Codex C implements coverage, it should add exactly one manifest entry:

```text
connection_disconnect_synthetic_v1
```

Required shape:

- `entry_type`: `session_ledger_entry`
- `source_kind`: `synthetic_committed_fixture`
- `commit_status`: `committed`
- `privacy_class`: `synthetic_committable`
- `sanitization_status`: `synthetic`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/366`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_connection_disconnect_coverage.md`
- `scenario_families`: `["connection.disconnect"]`
- `parser_event_families`:
  `["MatchConnectionState", "TcpConnectionClose", "WebSocketClosed"]`
- `coverage_status`: `covered_synthetic`
- `coverage_basis`: `["fixture_metadata_only", "parser_behavior_verified"]`

Suggested `parser_claim_families`:

- `connection_state_transition`
- `tcp_connection_close_payload`
- `websocket_closed_payload`
- `disconnect_privacy_boundary`

The manifest entry may reference focused parser tests and schema snapshots as
evidence paths. It must not include raw log lines, private local paths,
network traces, private report paths, external corpus paths, compressed log
paths, host names, IP addresses, port values, or raw payload dumps.

### Required Session-Ledger Entry

If Codex C implements coverage, it should add exactly one session-ledger entry:

```text
connection_disconnect_synthetic_v1
```

Required behavior:

- `source_kind`: `synthetic_committed_fixture`
- `commit_status`: `committed`
- `privacy_class`: `synthetic_committable`
- `sanitization_status`: `synthetic`
- `scenario_families`: `["connection.disconnect"]`
- `format_family`: `connection_runtime`
- `match_shape`: `connection_disconnect_signal_only`
- `record_summary`: `synthetic_metadata_summary_only`
- `parser_coverage.event_families`:
  `{"MatchConnectionState": 1, "TcpConnectionClose": 1, "WebSocketClosed": 1}`
  unless Codex C adds a reasoned contract-test note explaining a different
  safe count.
- `parser_coverage.unknown_entries`: `0`
- `parser_coverage.truncation_count`: `0`
- `game_rows`: `{"count": 0, "result_shape": "not_applicable"}`

Required redaction flags:

- `raw_log_lines_included`: `false`
- `private_paths_included`: `false`
- `raw_payloads_included`: `false`
- `external_logs_included`: `false`
- `decklists_included`: `false`

The session entry must say clearly that it is synthetic metadata summary only.
It must not contain a copied Player.log line, copied Manasight row, live
network trace, raw connection payload dump, host name, IP address, port value,
local path, credential-like text, decklist, strategy note, or private report
location.

### Allowed Evidence Model

Allowed committed evidence:

- existing parser source and focused parser tests for `MatchConnectionState`,
  `TcpConnectionClose`, and `WebSocketClosed`;
- existing event/schema snapshot evidence for those event kinds;
- synthetic manifest/session-ledger metadata;
- generic parser claim labels and counts;
- public Manasight category labels only through existing taxonomy context;
- contract-test and implementation-handoff Markdown that summarizes evidence
  without reproducing raw/private log lines.

Allowed synthetic payload concepts:

- generic state transition from a playing-like state to a disconnected-like
  state;
- generic TCP connection close payload handling;
- generic websocket closed payload handling;
- generic missing-game-row statement because disconnect coverage is not a
  match/game fact;
- generic redaction statement that any host, port, IP, network trace, or local
  path values are not committed corpus evidence.

Forbidden committed evidence:

- raw/private Player.log excerpts;
- raw local logs;
- private smoke outputs;
- local runtime artifacts;
- generated data;
- SQLite files;
- workbook exports;
- failed post artifacts;
- credentials, tokens, API keys, webhook URLs, or secrets;
- IP addresses, hostnames, network traces, firewall logs, Wi-Fi logs, pfctl
  logs, or private machine/network identifiers;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size row lists, capture-date row lists, parser
  source, or external corpus contents;
- decklists, deck names, card choices, card pools, strategy notes, or private
  reports.

### Adjacent Family Non-Claims

The implementation must not change or imply coverage for:

- `connection.reconnect`
- `connection.firewall_or_network_drop`
- `connection.connection_error_payload` beyond preserving the already-covered
  #364 status
- `log_runtime.detailed_logs_disabled`
- `log_runtime.rotation`
- `log_runtime.malformed_or_headerless`
- `log_runtime.timestamp_anomaly`
- `log_runtime.unknown_entry`
- timer/inactivity runtime families
- private live-log smoke
- release readiness or runtime resilience

Specific status expectations:

- `connection.disconnect` may become `covered_synthetic`.
- `connection.connection_error_payload` must remain `covered_synthetic` from
  issue #364.
- `connection.reconnect` must remain `blocked_external_boundary` unless a
  later issue and contract authorize Mythic Edge-owned reconnect evidence.
- `connection.firewall_or_network_drop` must remain `missing` unless a later
  issue and contract authorize private/local report-only or synthetic
  coverage.

Because `connection_error.py` currently parses some reconnect text and close
exception markers under the `ConnectionError` event kind, Codex C must keep
wording sharp: connection-error parser tests may be run as regression
coverage, but this corpus slice must not use those tests to claim
`connection.disconnect` or `connection.reconnect` scenario coverage. This
slice's primary parser evidence is `connection_state.py` and
`connection_close.py`.

### Report Expectations

After Codex C implementation, the corpus parity report should still be
`partial_coverage_map_ready`.

The expected report row for `connection.disconnect` should show:

- `coverage_status`: `covered_synthetic`
- `coverage_basis`: `["fixture_metadata_only", "parser_behavior_verified"]`
- `mythic_edge_entries`: `["connection_disconnect_synthetic_v1"]`
- notes stating that this proves synthetic parser-owned connection
  state/close metadata only and does not prove reconnect, firewall/drop,
  network reliability, private smoke, release readiness, analytics truth, AI
  truth, coaching truth, or production behavior.

The report summary may change by exactly one family moving from `missing` to
`covered_synthetic`. If counts differ because the base branch changed, Codex C
must explain the current base in its implementation handoff.

## Inputs

### Corpus Manifest

Type: JSON object.

Source:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`

Required current schema values:

- `object`: `mythic_edge_parser_corpus_manifest`
- `schema_version`: `parser_corpus_manifest.v1`
- `corpus_id`: `mythic_edge_parser_reliability_corpus_v1`

Relevant fields:

- `entries`
- `taxonomy.families`
- `source_privacy`

### Session Ledger

Type: JSON object.

Source:

- `tests/fixtures/parser_corpus/session_ledger.v1.json`

Required current schema values:

- `object`: `mythic_edge_parser_corpus_session_ledger`
- `schema_version`: `parser_corpus_session_ledger.v1`

Relevant fields:

- `sessions`
- `report_only_redactions`
- `parser_coverage`
- `known_gaps`

### Parser Behavior Evidence

Type: source files and focused tests.

Sources:

- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_connection_parsers.py`
- `tests/test_event_schema_snapshots.py`

Allowed evidence:

- event kind `MatchConnectionState`;
- event kind `TcpConnectionClose`;
- event kind `WebSocketClosed`;
- state transition string validation;
- parsed close payload preservation;
- parsed websocket closed payload preservation;
- malformed and unrelated input rejection.

Forbidden evidence use:

- using `ConnectionError` coverage from issue #364 as this issue's disconnect
  coverage;
- using reconnect text behavior as coverage for `connection.reconnect`;
- using parser tests as live runtime resilience evidence;
- adding private/live-network logs to make the corpus row look more realistic.

## Outputs

### Contract Artifact

Type: Markdown.

Destination:

- `docs/contracts/parser_corpus_connection_disconnect_coverage.md`

Status:

- contract only

### Future Manifest And Ledger Rows

Type: JSON metadata entries.

Destinations:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`

Status:

- committed synthetic metadata
- report-only coverage evidence
- not parser truth

### Future Report And Handoff

Type: Markdown.

Destinations:

- `docs/contract_test_reports/parser_corpus_connection_disconnect_coverage.md`
- `docs/implementation_handoffs/parser_corpus_connection_disconnect_coverage_comparison.md`

Status:

- implementation/review evidence
- not parser truth
- not merge/deploy readiness by itself

## Invariants

- Exactly one in-scope family is authorized: `connection.disconnect`.
- The coverage row must remain synthetic metadata, not raw log evidence.
- The implementation must not add committed raw log fixtures.
- The implementation must not import external corpus material.
- The implementation must not change parser source behavior.
- `connection.reconnect` must not become covered from this issue.
- `connection.firewall_or_network_drop` must not become covered from this
  issue.
- `connection.connection_error_payload` must remain covered only by the #364
  entry and must not be redefined here.
- The report must keep private and external artifact flags safe.
- All report-only redaction flags for the new session must be false.
- No new artifact may contain raw/private Player.log text, local absolute
  paths, credentials, webhook URLs, IP/network traces, hostnames, port values,
  decklists, strategy notes, generated data, SQLite files, runtime artifacts,
  or workbook exports.
- The contract and implementation must keep corpus reports downstream of
  parser behavior.

## Error Behavior

Codex C must stop and route back to Codex B if:

- the manifest/schema cannot represent a safe synthetic disconnect entry
  without schema changes;
- the focused parser evidence is insufficient to justify
  `covered_synthetic`;
- implementation would require changing parser source, router behavior, event
  classes, diagnostics behavior, runtime status behavior, or report schemas;
- coverage for reconnect, firewall/network-drop, or runtime interruption
  appears necessary to satisfy the issue;
- private/live log evidence appears necessary;
- current branch state differs materially from
  `5513f406f227fe53bea87de73bf6e86f4b58d30a` and changes the coverage counts
  or family statuses in a way this contract does not anticipate.

Malformed manifest or session-ledger metadata must continue to be handled by
the existing corpus parity validation behavior. This contract does not
authorize changing validation behavior to accept unsafe or ambiguous entries.

## Side Effects

Codex B side effects:

- writes this contract only.

Future Codex C side effects authorized by this contract:

- may update the committed corpus manifest;
- may update the committed session ledger;
- may update focused corpus parity tests;
- may update focused connection parser tests only to document existing
  behavior, not to change behavior;
- must write the implementation handoff;
- should write the contract-test report if following the established parser
  parity child pattern.

Explicitly forbidden side effects:

- no parser behavior changes;
- no router behavior changes;
- no event class changes;
- no diagnostics/runtime status changes;
- no workbook, webhook, Apps Script, Sheets, output transport, analytics, AI,
  coaching, CI, merge, deploy, release, or production changes;
- no issue closure, tracker closure, PR creation, staging, commit, or push
  unless a later role/user instruction explicitly requests it.

## Dependency Order

Future Codex C should work in this order:

1. Re-verify branch and base commit against `origin/codex/parser-parity`.
2. Compare `connection.disconnect` current corpus status to this contract.
3. Confirm focused connection parser tests still pass without source changes.
4. Add the manifest entry for `connection_disconnect_synthetic_v1`.
5. Add the session-ledger entry for `connection_disconnect_synthetic_v1`.
6. Update `tests/test_corpus_parity_report.py` for the new row, summary counts,
   redaction flags, and adjacent family statuses.
7. Add or adjust focused connection parser tests only if needed to document
   already-observed behavior.
8. Run the required validation.
9. Write the implementation handoff and contract-test report.

## Compatibility

Compatibility requirements:

- The corpus manifest schema remains `parser_corpus_manifest.v1`.
- The session-ledger schema remains `parser_corpus_session_ledger.v1`.
- The corpus report schema remains `parser_corpus_compatibility_report.v1`.
- The existing report CLI and API remain unchanged.
- Existing sealed lifecycle coverage entries remain unchanged.
- Existing connection error payload coverage remains unchanged.
- Existing status vocabulary remains unchanged.
- Existing `MatchConnectionState`, `TcpConnectionClose`, and
  `WebSocketClosed` payload behavior remains unchanged.
- Existing parser tests and event schema snapshots remain compatible.

This issue must not introduce new coverage-status vocabulary, new scenario
families, new report API fields, new event payload fields, or new runtime
surfaces.

## Unknowns And Suspected Gaps

Unknowns:

- Whether a later connection-payload policy issue should add explicit `raw_*`
  fields for connection-state and connection-close event payloads.
- Whether future private/local smoke can safely produce report-only evidence
  for reconnect or firewall/network-drop families.
- Whether diagnostics should later summarize connection close and disconnect
  signals more richly.

Suspected gaps:

- `MatchConnectionState` does not expose an explicit `type` field.
- `MatchConnectionState` does not expose an explicit `raw_connection_state`
  field.
- `TcpConnectionClose` does not expose an explicit `type` field.
- `TcpConnectionClose` does not expose an explicit `raw_tcp_connection_close`
  field.
- `WebSocketClosed` does not expose an explicit `type` field.
- `WebSocketClosed` does not expose an explicit `raw_websocket_closed` field.
- Current corpus coverage has no live-runtime network interruption evidence.
- Public taxonomy mapping alone cannot prove Mythic Edge support for any
  connection/runtime family.

These are not blockers for this contract. They are boundaries for future
issues.

## Tests Required

Codex C validation should include:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json

python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py
python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
```

Path-scoped safety checks should include the changed contract, report, handoff,
manifest, ledger, and tests:

```bash
git diff --name-only origin/codex/parser-parity...HEAD \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

git diff --name-only origin/codex/parser-parity...HEAD \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin

git diff --name-only origin/codex/parser-parity...HEAD \
  | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

If Codex C only has untracked files, it must use explicit path lists instead
of relying on triple-dot diff output.

Optional broader validation:

```bash
python3 -m pytest -q tests
```

## Acceptance Criteria

- `docs/contracts/parser_corpus_connection_disconnect_coverage.md` exists and
  names the owning layer, truth boundary, allowed evidence, forbidden
  evidence, protected surfaces, and validation plan.
- Codex C has a clear path to add one safe synthetic corpus entry:
  `connection_disconnect_synthetic_v1`.
- Only `connection.disconnect` is authorized for status movement.
- Adjacent connection/runtime families remain explicitly out of scope.
- Parser behavior changes are explicitly forbidden.
- Raw/private logs, external corpus content, live network traces, generated
  artifacts, SQLite files, workbook exports, secrets, and credentials remain
  forbidden.
- The contract routes implementation to Codex C and preserves tracker #158 as
  open.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #366, Connection disconnect
corpus coverage path, under tracker #158.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/366
- Previous completed child issue: https://github.com/Tahjali11/Mythic-Edge/issues/364
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/365
- Previous merge commit on codex/parser-parity: 5513f406f227fe53bea87de73bf6e86f4b58d30a
- Base branch: codex/parser-parity
- Contract: docs/contracts/parser_corpus_connection_disconnect_coverage.md
- Expected handoff: docs/implementation_handoffs/parser_corpus_connection_disconnect_coverage_comparison.md
- Expected report: docs/contract_test_reports/parser_corpus_connection_disconnect_coverage.md

Goal:
Compare the current parser corpus parity artifacts and focused connection parser
tests against the contract. Implement only the smallest metadata/test changes
needed to move `connection.disconnect` to safe synthetic corpus coverage
without changing parser behavior or claiming adjacent connection runtime
coverage.

Do:
- Verify the branch is based on current `origin/codex/parser-parity`.
- Compare observed current behavior against the contract before editing.
- Add one safe synthetic manifest entry named
  `connection_disconnect_synthetic_v1`.
- Add one safe synthetic session-ledger entry named
  `connection_disconnect_synthetic_v1`.
- Update focused corpus parity tests for the new report row, summary counts,
  redaction flags, and adjacent family non-claims.
- Run the focused connection parser tests as evidence of existing parser-owned
  behavior.
- Write `docs/implementation_handoffs/parser_corpus_connection_disconnect_coverage_comparison.md`.
- Write `docs/contract_test_reports/parser_corpus_connection_disconnect_coverage.md`.

Do not:
- Change parser behavior, router behavior, parser event classes, parser state
  final reconciliation, diagnostics behavior, runtime status behavior, workbook
  schema, webhook payload shape, Apps Script behavior, Google Sheets sync,
  output transport, analytics truth, AI truth, coaching behavior, CI policy,
  merge policy, deploy policy, production behavior, match/game identity, or
  deduplication.
- Move `connection.reconnect` or `connection.firewall_or_network_drop` to
  covered status.
- Redefine `connection.connection_error_payload` coverage from issue #364.
- Claim live reconnect, firewall/network-drop, runtime interruption, private
  smoke, release readiness, full connection parity, or full Mythic Edge corpus
  parity.
- Import, copy, mirror, or commit Manasight raw logs, `.log.gz` files, raw
  session payloads, compressed corpus files, hash lists, byte-size row lists,
  capture-date row lists, parser source, or external corpus contents.
- Commit private Player.log excerpts, private local logs, generated data,
  SQLite files, runtime artifacts, workbook exports, credentials, tokens, API
  keys, webhook URLs, IP/network traces, hostnames, port values, decklists,
  strategy notes, or private reports.
- Stage or commit unless explicitly asked.

Validation:
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
- `python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py`
- `python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py`
- `python3 -m ruff check src tests tools`
- `python3 tools/check_agent_docs.py`
- `git diff --check`
- path-scoped secret/private-marker, protected-surface, and validation-selector checks against `origin/codex/parser-parity`

Expected output:
- Implementation summary
- Files changed
- Validation run
- Remaining risks/open questions
- Clear handoff to Codex E
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/366"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/364"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/365"
  previous_merge_commit: "5513f406f227fe53bea87de73bf6e86f4b58d30a"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_connection_disconnect_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_connection_disconnect_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_connection_disconnect_coverage.md"
  verdict: "contract_ready_for_synthetic_connection_disconnect_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-connection-disconnect-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py"
    - "python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface gate"
    - "path-scoped validation selector"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not close issue #366."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not change parser behavior, router semantics, parser event classes, diagnostics behavior, runtime status behavior, workbook/webhook/App Script/Sheets/output/analytics/AI/coaching/production surfaces, match/game identity, deduplication, CI policy, merge policy, or deploy policy."
    - "Do not move connection.reconnect or connection.firewall_or_network_drop to covered status."
    - "Do not redefine connection.connection_error_payload coverage from issue #364."
    - "Do not claim live reconnect, firewall/network-drop, runtime interruption, private smoke, release readiness, or full connection parity."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, IP/network traces, hostnames, port values, decklists, strategy notes, or private reports."
```
