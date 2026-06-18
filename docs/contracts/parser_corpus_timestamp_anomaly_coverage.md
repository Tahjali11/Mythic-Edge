# Parser Corpus Timestamp Anomaly Coverage Contract

## Module

Timestamp anomaly corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`log_runtime.timestamp_anomaly` with repo-owned synthetic metadata and existing
router behavior evidence for timestamp-missing and timestamp-parse-failure
signals. It proves only that Mythic Edge has safe corpus metadata for
router-owned timestamp anomaly accounting. It does not prove malformed or
headerless log recovery, unknown-entry drift handling, log rotation support,
real local Player.log timestamp drift, diagnostics readiness, release
readiness, full runtime health, or full Mythic Edge corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/370
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/368
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/369
- Previous merge commit:
  `c7dfefc1e1c00f521ace4243f974d12c17596994`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-timestamp-anomaly-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `c7dfefc1e1c00f521ace4243f974d12c17596994`
- target_artifact:
  `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md`
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
- `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`
- `docs/contracts/parser_corpus_connection_error_payload_coverage.md`
- `docs/contracts/parser_corpus_connection_disconnect_coverage.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `tests/test_router_unit.py`
- `tests/test_parser_regressions.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, or external
  corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`log_runtime.timestamp_anomaly` scenario family. Router/parser modules own the
underlying timestamp extraction and timestamp-anomaly accounting. Corpus parity
artifacts own only the coverage status claim that Mythic Edge has safe
repo-owned evidence for this narrow family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence, but it is not a Parser behavior module and is not a
runtime, diagnostics, analytics, workbook, local app, AI, coaching, release,
or production module.

## Truth Owner

Truth owner for `log_runtime.timestamp_anomaly` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for timestamp behavior referenced by this coverage:

- `src/mythic_edge_parser/router.py`
- `RouterStats.timestamp_missing`
- `RouterStats.timestamp_parse_failure`
- `RouterStats.timestamp_anomalies`
- focused router tests in `tests/test_router_unit.py`

Truth owner for downstream observation of timestamp counts:

- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- their focused tests, where already contracted

Truth boundary:

- `router.extract_timestamp(...)` owns the public timestamp extraction helper.
- `Router.route(...)` owns incrementing router stats for timestamp-missing and
  timestamp-parse-failure cases.
- `RouterStats.timestamp_anomalies` owns the aggregate count equal to
  `timestamp_missing + timestamp_parse_failure`.
- Diagnostics, drift sensor, golden replay, and feature-equity reports may
  observe timestamp counts but do not become timestamp truth.
- Corpus parity artifacts own the report-only coverage row for
  `log_runtime.timestamp_anomaly`.
- Corpus coverage status is review metadata. It is not parser truth, runtime
  health truth, private Player.log drift proof, diagnostics truth, workbook
  truth, analytics truth, AI truth, coaching truth, merge readiness, deploy
  readiness, public/private release readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing RouterStats timestamp_missing / timestamp_parse_failure behavior
  -> bounded synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for log_runtime.timestamp_anomaly
```

Forbidden reverse flow:

- Corpus coverage status must not change timestamp parsing behavior.
- Corpus metadata must not change router semantics, timestamp regexes,
  timestamp parsing formats, parser event classes, parser state, diagnostics
  behavior, drift report behavior, golden replay behavior, feature-equity
  behavior, runtime status behavior, workbook output, analytics, AI, coaching,
  release policy, or production behavior.
- Corpus metadata must not turn synthetic timestamp evidence into a claim about
  real local Player.log drift, live MTGA runtime behavior, diagnostics
  readiness, private smoke readiness, or broad log-runtime parity.

Protected surfaces explicitly not touched:

- parser behavior
- timestamp parsing behavior
- router semantics
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- diagnostics report shape
- log drift sensor behavior
- golden replay behavior
- feature-equity behavior
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

- `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_router_unit.py`
- `docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `tests/test_parser_regressions.py`
- relevant diagnostics, drift, golden replay, and feature-equity tests

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- timestamp regex or parse-format changes
- router stats semantics changes
- parser event class changes
- new timestamp anomaly event kinds
- diagnostics report shape changes
- drift sensor behavior changes
- golden replay behavior changes
- feature-equity behavior changes
- runtime status changes
- live private smoke execution
- committed raw log fixtures
- private Player.log fixture work
- actual local MTGA runtime timestamp drift verification
- Manasight corpus import
- malformed/headerless log, unknown-entry, log-rotation, reconnect,
  firewall/network-drop, or private resilience coverage work
- detailed-logs-disabled work already owned by issue #368
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, final integration, and production surfaces

## Public Interface

The public parser/router interface referenced by this contract is:

```python
router.extract_timestamp(body: str) -> datetime | None
router.Router().route(entry: LogEntry) -> list[GameEvent]
router.Router().stats -> RouterStats
RouterStats.timestamp_missing: int
RouterStats.timestamp_parse_failure: int
RouterStats.timestamp_anomalies: int
```

The public corpus parity report API remains:

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
`c7dfefc1e1c00f521ace4243f974d12c17596994`:

- Tracker #158 is open.
- Issue #370 is open as the timestamp anomaly corpus coverage child.
- Issue #368 was merged through PR #369 into `codex/parser-parity` at
  `c7dfefc1e1c00f521ace4243f974d12c17596994`.
- The current corpus parity report returns
  `partial_coverage_map_ready (45 families, 6 committed, 22 missing)`.
- `log_runtime.timestamp_anomaly` exists in the corpus taxonomy.
- No committed manifest entry currently owns `log_runtime.timestamp_anomaly`.
- No session-ledger entry currently owns `log_runtime.timestamp_anomaly`.
- `log_runtime.detailed_logs_disabled` is already `covered_synthetic` through
  issue #368 and `detailed_logs_disabled_synthetic_v1`.
- `log_runtime.rotation` is represented only by
  `external_reference_category_boundary` and is
  `blocked_external_boundary`.
- `log_runtime.malformed_or_headerless` and `log_runtime.unknown_entry` are
  taxonomy families but have no Mythic Edge-owned coverage entries.

Observed router behavior:

- `router.extract_timestamp(...)` reads only the first line of a log-entry
  body when looking for a timestamp.
- A valid first-line timestamp returns a UTC `datetime`.
- A body with no first-line timestamp returns `None`.
- An invalid timestamp value returns `None`.
- `Router.route(...)` increments `timestamp_missing` when timestamp extraction
  finds no timestamp marker.
- `Router.route(...)` increments `timestamp_parse_failure` when timestamp
  extraction finds a marker with invalid timestamp values.
- `RouterStats.timestamp_anomalies` returns the sum of missing and parse-failed
  timestamp counts.
- Focused router tests cover valid extraction, first-line-only extraction,
  invalid timestamp values, missing timestamp stats, parse-failure stats, and
  truncation markers that route while still counting timestamp anomalies.

Observed downstream consumers:

- Golden replay reports include `timestamp_missing` and
  `timestamp_parse_failure` in router stats.
- Log drift sensor reports include `timestamp_missing` and
  `timestamp_parse_failure` in entry counts.
- Parser diagnostics reports include timestamp anomaly counts under parser
  health.
- Feature-equity corpus ratchet records timestamp missing and parse-failure
  counts.
- These consumers observe router-owned counts. They do not own timestamp
  interpretation, corpus coverage status, or parser truth.

## Required Guarantees

### In-Scope Scenario Family

Only this scenario family is in scope:

```text
log_runtime.timestamp_anomaly
```

Codex C may move this family from `missing` to `covered_synthetic` only if it
adds safe repo-owned synthetic metadata and focused tests that keep all
non-claims explicit.

### Required Manifest Entry

If Codex C implements coverage, it should add exactly one manifest entry:

```text
timestamp_anomaly_synthetic_v1
```

Required shape:

- `entry_type`: `session_ledger_entry`
- `source_kind`: `synthetic_committed_fixture`
- `commit_status`: `committed`
- `privacy_class`: `synthetic_committable`
- `sanitization_status`: `synthetic`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/370`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- `scenario_families`: `["log_runtime.timestamp_anomaly"]`
- `parser_event_families`: `[]`
- `coverage_status`: `covered_synthetic`
- `coverage_basis`: `["fixture_metadata_only", "parser_behavior_verified"]`

Suggested `parser_claim_families`:

- `router_timestamp_missing_stat`
- `router_timestamp_parse_failure_stat`
- `router_timestamp_anomalies_aggregate`
- `timestamp_anomaly_privacy_boundary`

The empty `parser_event_families` list is intentional. Timestamp anomaly
coverage is router-stat evidence, not a parser event-family coverage claim.
Codex C must not invent a `TimestampAnomaly` event family or event class to
make the corpus row look like event coverage.

The manifest entry may reference focused router tests and corpus parity tests
as evidence paths. It must not include raw log lines, private local paths,
private runtime report paths, external corpus paths, compressed log paths,
local app-data paths, IP/network traces, or raw payload dumps.

### Required Session-Ledger Entry

If Codex C implements coverage, it should add exactly one session-ledger entry:

```text
timestamp_anomaly_synthetic_v1
```

Required behavior:

- `source_kind`: `synthetic_committed_fixture`
- `commit_status`: `committed`
- `privacy_class`: `synthetic_committable`
- `sanitization_status`: `synthetic`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/370`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- `scenario_families`: `["log_runtime.timestamp_anomaly"]`
- `format_family`: `log_runtime`
- `match_shape`: `timestamp_anomaly_signal_only`
- `record_summary`: `synthetic_router_stats_summary_only`
- `parser_coverage.event_families`: `{}`
- `parser_coverage.unknown_entries`: `0`
- `parser_coverage.truncation_count`: `0`
- `parser_coverage.timestamp_missing`: `1`
- `parser_coverage.timestamp_parse_failure`: `1`
- `parser_coverage.timestamp_anomalies`: `2`
- `game_rows`: `{"count": 0, "result_shape": "not_applicable"}`

Required redaction flags:

- `raw_log_lines_included`: `false`
- `private_paths_included`: `false`
- `raw_payloads_included`: `false`
- `external_logs_included`: `false`
- `decklists_included`: `false`

The session entry must say clearly that it is synthetic router-stats summary
only. It must not contain a copied Player.log line, copied Manasight row, live
runtime report, private report path, raw timestamp string, raw metadata
payload, IP/network trace, decklist, strategy note, or private machine
identifier.

If Codex C finds that the session-ledger validator or tests reject timestamp
count keys under `parser_coverage`, it must route back to Codex B/E for a
schema clarification. It must not silently encode timestamp counts in a less
machine-readable field or change schema validation behavior under this
contract-only coverage slice.

### Allowed Evidence Model

Allowed committed evidence:

- existing router source and focused router tests for `timestamp_missing`,
  `timestamp_parse_failure`, and `timestamp_anomalies`;
- existing diagnostics, drift, golden replay, and feature-equity code/tests as
  read-only context showing downstream observation of router counts;
- synthetic manifest/session-ledger metadata;
- generic parser/router claim labels and counts;
- public Manasight category labels only through existing taxonomy context;
- contract-test and implementation-handoff Markdown that summarizes evidence
  without reproducing raw/private log lines.

Allowed synthetic payload concepts:

- a generic missing first-line timestamp case;
- a generic invalid timestamp value case;
- generic counts for missing, parse-failed, and aggregate timestamp anomalies;
- generic missing-game-row statement because timestamp anomaly coverage is not
  a match/game fact;
- generic redaction statement that raw log text, private reports, local
  runtime paths, and local app-data contents are not committed corpus evidence.

Forbidden committed evidence:

- raw/private Player.log excerpts;
- raw local logs;
- private smoke outputs;
- actual local MTGA runtime timestamp drift reports;
- local app-data contents;
- local runtime artifacts;
- generated data;
- SQLite files;
- workbook exports;
- failed post artifacts;
- credentials, tokens, API keys, webhook URLs, or secrets;
- private machine identifiers, account identifiers, local user paths, IP
  addresses, network traces, or private report locations;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size row lists, capture-date row lists, parser
  source, or external corpus contents;
- decklists, deck names, card choices, card pools, strategy notes, or private
  reports.

### Router-Stats Boundary

Coverage must be grounded in existing router-owned timestamp stats:

```text
RouterStats.timestamp_missing
RouterStats.timestamp_parse_failure
RouterStats.timestamp_anomalies
```

Codex C may mention diagnostics, drift sensor, golden replay, or feature-equity
behavior as adjacent consumer context, but those report layers must not be the
sole coverage basis. This protects the distinction between:

- router-owned accounting that a timestamp is missing or parse-failed; and
- downstream review reports that surface the count.

If Codex C cannot demonstrate the router-stat behavior with existing tests, it
must add focused tests only if the existing implementation already supports
the contract. If a test would require behavior changes, Codex C must stop and
route back to Codex B/E.

### Adjacent Family Non-Claims

The implementation must not change or imply coverage for:

- `log_runtime.malformed_or_headerless`
- `log_runtime.unknown_entry`
- `log_runtime.rotation`
- `log_runtime.detailed_logs_disabled` beyond preserving the already-covered
  #368 status
- `connection.reconnect`
- `connection.disconnect`
- `connection.connection_error_payload`
- `connection.firewall_or_network_drop`
- timer/inactivity runtime families
- private live-log smoke
- release readiness or runtime resilience

Specific status expectations:

- `log_runtime.timestamp_anomaly` may become `covered_synthetic`.
- `log_runtime.detailed_logs_disabled` must remain `covered_synthetic` from
  issue #368.
- `log_runtime.rotation` must remain `blocked_external_boundary` unless a
  later issue and contract authorize Mythic Edge-owned rotation evidence.
- `log_runtime.malformed_or_headerless` and `log_runtime.unknown_entry` must
  remain `missing` unless later issues and contracts authorize coverage.
- `connection.connection_error_payload` must remain `covered_synthetic` from
  issue #364.
- `connection.disconnect` must remain `covered_synthetic` from issue #366.
- `connection.reconnect` must remain `blocked_external_boundary` unless a
  later issue and contract authorize Mythic Edge-owned reconnect evidence.
- `connection.firewall_or_network_drop` must remain `missing` unless a later
  issue and contract authorize private/local report-only or synthetic
  coverage.

### Report Expectations

After Codex C implementation, the corpus parity report should still be
`partial_coverage_map_ready`.

The expected report row for `log_runtime.timestamp_anomaly` should show:

- `coverage_status`: `covered_synthetic`
- `coverage_basis`: `["fixture_metadata_only", "parser_behavior_verified"]`
- `mythic_edge_entries`: `["timestamp_anomaly_synthetic_v1"]`
- notes stating that this proves synthetic router-owned timestamp anomaly
  stats only and does not prove malformed/headerless log handling,
  unknown-entry routing, log rotation, real local Player.log timestamp drift,
  private smoke, release readiness, analytics truth, AI truth, coaching truth,
  or production behavior.

The report summary may change by exactly one family moving from `missing` to
`covered_synthetic`. Expected current-base movement is:

- before: `partial_coverage_map_ready (45 families, 6 committed, 22 missing)`
- after: `partial_coverage_map_ready (45 families, 6 committed, 21 missing)`

If counts differ because the base branch changed, Codex C must explain the
current base in its implementation handoff.

## Inputs

Primary inputs:

- corpus manifest:
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- session ledger:
  `tests/fixtures/parser_corpus/session_ledger.v1.json`
- router source:
  `src/mythic_edge_parser/router.py`
- focused router tests:
  `tests/test_router_unit.py`
- corpus parity report tests:
  `tests/test_corpus_parity_report.py`

Optional context inputs:

- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `tests/test_parser_regressions.py`
- relevant diagnostics, drift, golden replay, and feature-equity tests

Forbidden inputs:

- raw/private Player.log files;
- actual local MTGA runtime timestamp drift reports;
- private local MTGA settings state;
- private smoke reports;
- local app-data contents;
- generated runtime artifacts;
- Manasight raw corpus contents;
- external compressed logs;
- credentials, secrets, tokens, API keys, or webhook URLs.

## Outputs

Required Codex B output:

- `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`

Expected Codex C outputs if implementation proceeds:

- manifest entry for `timestamp_anomaly_synthetic_v1`
- session-ledger entry for `timestamp_anomaly_synthetic_v1`
- focused corpus parity tests proving the new family status
- focused router-stat tests if current timestamp anomaly evidence is not
  already asserted strongly enough
- implementation handoff:
  `docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md`
- contract test report:
  `docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md`

No output may include raw/private log text, private paths, raw payload dumps,
runtime artifacts, generated databases, workbook exports, credentials, tokens,
API keys, webhook URLs, local app-data contents, or external raw corpus
contents.

## Invariants

- `log_runtime.timestamp_anomaly` coverage is metadata/report-only.
- Router stats remain parser-owned timestamp-anomaly truth.
- Corpus coverage does not authorize parser behavior changes.
- Corpus coverage does not authorize new parser event classes.
- Corpus coverage does not authorize diagnostics, drift sensor, golden replay,
  feature-equity, runtime status, workbook, webhook, Apps Script, Google
  Sheets, local app, analytics, AI, coaching, CI, release, or production
  changes.
- Corpus metadata must not contain raw/private Player.log excerpts.
- Corpus metadata must not contain raw Manasight corpus contents.
- Corpus metadata must not contain private local paths, settings dumps, or
  runtime reports.
- `log_runtime.timestamp_anomaly` must not be used to claim full log-runtime
  parity.
- Synthetic timestamp anomaly evidence must not become private live-log drift
  proof.

## Error Behavior

If the current router tests do not show `timestamp_missing`,
`timestamp_parse_failure`, and `timestamp_anomalies` behavior, Codex C must add
focused tests only if the existing implementation already supports it. If a
test would require behavior changes, Codex C must stop and route back to Codex
B/E.

If the corpus report cannot represent the new coverage row using existing
schemas, Codex C must stop and route back for a schema contract. This issue
does not authorize corpus report schema changes.

If the session-ledger validator rejects the preferred
`parser_coverage.timestamp_*` fields, Codex C must stop and route back for a
schema clarification. This issue does not authorize weakening validation or
silently dropping the machine-readable timestamp counts.

If private evidence seems necessary to prove coverage, Codex C must stop. This
issue authorizes only synthetic committed metadata and existing router tests.

If the base branch has changed and report counts no longer match this
contract's observed counts, Codex C may proceed only if the in-scope family,
coverage status, and non-claims remain intact. The implementation handoff must
record the updated counts and base commit.

## Side Effects

Codex B side effects:

- writes this contract file only.

Codex C side effects authorized later:

- edits committed corpus manifest/session-ledger metadata;
- edits focused corpus parity and router tests;
- writes implementation handoff and contract test report.

Codex C side effects forbidden:

- parser behavior changes;
- timestamp parsing behavior changes;
- router semantic changes;
- diagnostics/drift/golden-replay/feature-equity behavior changes;
- private/local artifact generation committed to the repo;
- issue closure;
- tracker closure;
- PR opening unless separately asked;
- CI gate changes;
- generated SQLite/runtime/workbook artifacts;
- workbook/webhook/App Script/Sheets changes;
- OpenAI/model-provider integration.

## Dependency Order

Codex C should work in this order:

1. Verify branch and base commit against `codex/parser-parity`.
2. Re-run the corpus parity report before editing and record the current
   `log_runtime.timestamp_anomaly` status.
3. Verify focused router tests for timestamp missing, parse failure, and
   aggregate anomaly counts.
4. Add the manifest entry.
5. Add the session-ledger entry.
6. Add or update focused corpus parity tests for
   `log_runtime.timestamp_anomaly`.
7. Add focused router-stat tests only if current coverage is insufficient and
   no behavior change is required.
8. Run validation.
9. Write implementation handoff and contract test report.

## Compatibility

Compatibility expectations:

- Preserve existing corpus manifest object and schema version.
- Preserve existing session-ledger object and schema version.
- Preserve existing coverage status vocabulary.
- Preserve existing report summary shape.
- Preserve existing router public helpers and `RouterStats` field names.
- Preserve existing timestamp extraction behavior.
- Preserve existing downstream consumers of timestamp stats.
- Preserve existing external-reference boundary entries.

This issue must not introduce compatibility shims, migration code, alternate
schema versions, new CLI flags, new environment variables, new runtime
artifact shapes, or new parser events.

## Tests Required

Codex C should run, at minimum:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json

python3 -m pytest -q \
  tests/test_corpus_parity_report.py \
  tests/test_router_unit.py \
  tests/test_parser_regressions.py

python3 -m pytest -q \
  tests/test_parser_diagnostics_mode.py \
  tests/test_log_drift_sensor.py \
  tests/test_golden_replay_harness.py \
  tests/test_feature_equity_corpus_ratchet.py

python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
```

Recommended path-scoped governance checks:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_timestamp_anomaly_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_router_unit.py \
  docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_timestamp_anomaly_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_router_unit.py \
  docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_timestamp_anomaly_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_router_unit.py \
  docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md \
  | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

Codex C may add more focused checks if it edits tests adjacent to diagnostics,
drift sensor, golden replay, feature-equity, or router-stat consumers.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`.
- The contract names the owned module, issue, tracker, branch, and base commit.
- The contract authorizes only metadata/report-only corpus coverage for
  `log_runtime.timestamp_anomaly`.
- The contract defines the exact manifest and session-ledger entry ID
  `timestamp_anomaly_synthetic_v1`.
- The contract explicitly defines `parser_event_families` as empty for this
  corpus row because the evidence is router stats, not a parser event.
- The contract preserves parser behavior and protected surfaces.
- The contract forbids raw/private Player.log excerpts, raw external corpus
  contents, local runtime reports, generated artifacts, and secrets.
- The contract lists adjacent non-claims and status expectations.
- The contract defines validation expectations for Codex C/E/F/G.
- The contract ends with a clear Codex C handoff.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #370, timestamp anomaly corpus
coverage under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/370

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Previous completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/368

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/369

Previous merge commit:
c7dfefc1e1c00f521ace4243f974d12c17596994

Base branch:
codex/parser-parity

Implementation branch:
codex/parser-corpus-timestamp-anomaly-coverage

Contract:
docs/contracts/parser_corpus_timestamp_anomaly_coverage.md

Goal:
Implement the smallest metadata/report-only corpus parity change that moves
`log_runtime.timestamp_anomaly` to safe Mythic Edge-owned synthetic coverage,
grounded in existing router-owned `timestamp_missing`,
`timestamp_parse_failure`, and `timestamp_anomalies` behavior.

Do:
- Compare current corpus manifest, session ledger, router tests, and corpus
  parity report against the contract before editing.
- Add exactly one manifest entry and one session-ledger entry for
  `timestamp_anomaly_synthetic_v1` unless a contract-test note identifies a
  contract mismatch that must be routed back.
- Keep coverage grounded in router-owned timestamp stats, not diagnostics,
  drift report summaries, private Player.log checks, or live MTGA runtime
  reports.
- Keep `parser_event_families` empty for this coverage row; do not invent a
  timestamp anomaly event family.
- Add or update focused tests for the corpus parity row and router-stat
  evidence only as needed.
- Produce
  `docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md`.
- Produce
  `docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md`.

Do not:
- Change parser behavior, timestamp parsing behavior, router semantics,
  parser event classes, parser state final reconciliation, match/game
  identity, deduplication, diagnostics behavior, drift sensor behavior, golden
  replay behavior, feature-equity behavior, runtime status behavior, workbook
  schema, webhook payload shape, Apps Script behavior, Google Sheets sync,
  output transport, analytics truth, AI truth, coaching behavior, CI gates,
  merge policy, deploy policy, production behavior, or final integration
  policy.
- Commit raw/private Player.log excerpts, raw local logs, actual runtime
  timestamp drift reports, private local app-data contents, generated
  artifacts, SQLite files, failed posts, runtime status files, workbook
  exports, secrets, credentials, tokens, API keys, webhook URLs, Manasight raw
  logs, external compressed corpus files, or external raw corpus contents.
- Claim full Mythic Edge corpus parity, full log-runtime parity, malformed or
  headerless log handling, unknown-entry routing, log rotation support,
  private smoke readiness, release readiness, merge readiness, deploy
  readiness, analytics truth, AI truth, gameplay advice, hidden-card
  inference, archetype classification, or coaching truth.
- Close tracker #158 or issue #370.
- Target main directly.
- Stage or commit unless explicitly asked.

Validation:
- Run the corpus parity report command from the contract.
- Run the focused pytest, ruff, agent-docs, diff-check, and path-scoped
  governance checks listed in the contract.
- Run adjacent diagnostics, drift, golden replay, and feature-equity tests only
  as consumer-regression evidence; those consumers must not be the primary
  corpus coverage basis.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/370"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/368"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/369"
  previous_merge_commit: "c7dfefc1e1c00f521ace4243f974d12c17596994"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_timestamp_anomaly_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md"
  verdict: "contract_ready_for_synthetic_timestamp_anomaly_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-timestamp-anomaly-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_router_unit.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
  stop_conditions:
    - "Do not implement parser behavior, timestamp parsing, or router semantic changes in this corpus coverage slice."
    - "Do not invent a timestamp anomaly parser event or event family; this coverage is router-stat evidence."
    - "Do not use diagnostics, drift reports, golden replay, feature-equity reports, private Player.log checks, or live runtime reports as the sole coverage basis."
    - "Do not commit raw/private Player.log excerpts, raw local logs, runtime timestamp drift reports, private app-data contents, generated artifacts, SQLite files, workbook exports, failed posts, runtime artifacts, credentials, tokens, API keys, webhook URLs, Manasight raw logs, or external raw corpus contents."
    - "Do not claim full Mythic Edge corpus parity, full log-runtime parity, malformed/headerless log handling, unknown-entry routing, log rotation support, private smoke readiness, release readiness, merge readiness, deploy readiness, analytics truth, AI truth, gameplay advice, hidden-card inference, archetype classification, or coaching truth."
    - "Do not target main directly or close tracker #158 or issue #370."
```
