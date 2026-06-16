# Parser Corpus Malformed Headerless Coverage Contract

## Module

Malformed/headerless log corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`log_runtime.malformed_or_headerless` with repo-owned synthetic metadata and
existing line-buffer/header-boundary evidence. It proves only that Mythic Edge
has safe corpus metadata for entry-boundary behavior such as orphan/headerless
noise, partial-line handling, multiline entry boundaries, unknown-looking
headers, and clean `LogEntry` emission. It does not prove unknown-entry drift
handling, semantic recovery from arbitrary malformed Player.log payloads, log
rotation support, private Player.log smoke success, release readiness, full
runtime health, or full Mythic Edge corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/372
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/370
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/371
- Previous merge commit:
  `4dac867bd22fbb8465c9c8c44b250d129f653121`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-malformed-headerless-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `4dac867bd22fbb8465c9c8c44b250d129f653121`
- target_artifact:
  `docs/contracts/parser_corpus_malformed_headerless_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md`
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
- `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_line_buffer_corpus.py`
- `tests/test_tailer_router_integration.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- Existing committed Mythic Edge line-buffer fixtures may be cited as
  repo-owned test evidence.
- This contract does not authorize importing, copying, mirroring, or committing
  new Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, or external
  corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`log_runtime.malformed_or_headerless` scenario family. The log entry layer owns
the underlying line-buffer/header-boundary behavior. Corpus parity artifacts
own only the coverage status claim that Mythic Edge has safe repo-owned
evidence for this narrow family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence, but it is not a Parser behavior module and is not a
runtime, diagnostics, analytics, workbook, local app, AI, coaching, release,
or production module.

## Truth Owner

Truth owner for `log_runtime.malformed_or_headerless` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for entry-boundary behavior referenced by this coverage:

- `src/mythic_edge_parser/log/entry.py`
- `LineBuffer`
- `LogEntry`
- `EntryHeader`
- `classify_line_header(...)`
- `is_single_line_header(...)`
- focused line-buffer/header tests

Truth owner for downstream consumption of emitted entries:

- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/router.py`
- parser modules and diagnostics where separately contracted

Truth boundary:

- `LineBuffer.feed(...)` owns converting complete text lines into zero or more
  `LogEntry` objects.
- `LineBuffer.flush(...)` owns finalizing pending fragments and buffered
  multiline entries.
- `resolve_header_policy(...)` and `classify_line_header(...)` own header
  classification.
- `EntryHeader.UNKNOWN` owns unknown bracketed header classification at the
  entry-boundary layer.
- Router unknown-entry stats are downstream routing outcomes and are not owned
  by this corpus slice.
- Diagnostics, drift sensor, golden replay, and feature-equity reports may
  observe entries or router stats but do not become entry-boundary truth.
- Corpus parity artifacts own the report-only coverage row for
  `log_runtime.malformed_or_headerless`.
- Corpus coverage status is review metadata. It is not parser truth, runtime
  health truth, private Player.log malformed-log proof, unknown-entry drift
  proof, diagnostics truth, workbook truth, analytics truth, AI truth,
  coaching truth, merge readiness, deploy readiness, public/private release
  readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing LineBuffer / EntryHeader entry-boundary behavior
  -> bounded synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for log_runtime.malformed_or_headerless
```

Forbidden reverse flow:

- Corpus coverage status must not change line-buffer behavior.
- Corpus metadata must not change header recognition, pending-fragment
  handling, multiline-entry buffering, orphan/headerless-noise handling,
  router semantics, parser behavior, parser event classes, parser state,
  diagnostics behavior, drift report behavior, golden replay behavior,
  feature-equity behavior, runtime status behavior, workbook output, analytics,
  AI, coaching, release policy, or production behavior.
- Corpus metadata must not turn synthetic line-buffer evidence into a claim
  about semantic recovery from arbitrary malformed Player.log payloads, real
  local Player.log drift, live MTGA runtime behavior, diagnostics readiness,
  private smoke readiness, or broad log-runtime parity.

Protected surfaces explicitly not touched:

- `LineBuffer` behavior
- header classification behavior
- tailer behavior
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

- `docs/contracts/parser_corpus_malformed_headerless_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_line_buffer_corpus.py`
- `docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_tailer_router_integration.py`
- relevant diagnostics, drift, golden replay, and feature-equity tests

Out of scope unless a later contract explicitly authorizes it:

- line-buffer behavior changes
- header classification behavior changes
- tailer behavior changes
- router semantic changes
- parser source changes
- parser event class changes
- new malformed/headerless parser events
- diagnostics report shape changes
- drift sensor behavior changes
- golden replay behavior changes
- feature-equity behavior changes
- runtime status changes
- live private smoke execution
- committed raw log fixtures
- private Player.log fixture work
- actual local MTGA malformed-log verification
- Manasight corpus import
- unknown-entry, log-rotation, reconnect, firewall/network-drop, or private
  resilience coverage work
- timestamp anomaly work already owned by issue #370
- detailed-logs-disabled work already owned by issue #368
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, final integration, and production surfaces

## Public Interface

The public entry-boundary interface referenced by this contract is:

```python
LineBuffer.feed(text: str) -> list[LogEntry]
LineBuffer.flush() -> list[LogEntry]
classify_line_header(line: str) -> EntryHeader | None
is_single_line_header(line: str, header: EntryHeader | None = None) -> bool
LogEntry.header: EntryHeader
LogEntry.body: str
EntryHeader.UNKNOWN
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
`4dac867bd22fbb8465c9c8c44b250d129f653121`:

- Tracker #158 is open.
- Issue #372 is open as the malformed/headerless log corpus coverage child.
- Issue #370 was merged through PR #371 into `codex/parser-parity` at
  `4dac867bd22fbb8465c9c8c44b250d129f653121`.
- The current corpus parity report returns
  `partial_coverage_map_ready (45 families, 6 committed, 21 missing)`.
- `log_runtime.malformed_or_headerless` exists in the corpus taxonomy.
- No committed manifest entry currently owns
  `log_runtime.malformed_or_headerless`.
- No session-ledger entry currently owns
  `log_runtime.malformed_or_headerless`.
- `log_runtime.detailed_logs_disabled` is already `covered_synthetic` through
  issue #368 and `detailed_logs_disabled_synthetic_v1`.
- `log_runtime.timestamp_anomaly` is already `covered_synthetic` through issue
  #370 and `timestamp_anomaly_synthetic_v1`.
- `log_runtime.rotation` is represented only by
  `external_reference_category_boundary` and is
  `blocked_external_boundary`.
- `log_runtime.unknown_entry` is a taxonomy family but has no Mythic
  Edge-owned coverage entry.

Observed line-buffer behavior:

- `classify_line_header(...)` recognizes known bracketed headers and explicit
  metadata, matchmaking, and truncation-marker prefixes.
- Lines with unknown bracketed headers classify as `EntryHeader.UNKNOWN`.
- Non-header lines classify as `None`.
- Single-line headers emit immediately after a complete line is available.
- Partial single-line headers wait for the trailing newline or for `flush()`.
- `flush()` finalizes a pending fragment if it is a recognized header.
- Multiline headers collect continuation lines until the next recognized
  header or `flush()`.
- Unknown bracketed headers collect continuation lines until the next
  recognized header or `flush()`.
- Headerless/orphan non-header lines are ignored when no current entry is open.
- Non-header lines inside an open multiline or unknown-header entry are
  appended to that entry.
- Existing line-buffer corpus tests assert that known header lines produce one
  emitted entry per header line and that orphan noise does not pollute
  single-line entry bodies.

Observed downstream behavior:

- `FileTailer` consumes bytes, decodes text, and delegates entry construction
  to `LineBuffer`.
- Router consumes emitted `LogEntry` objects.
- Router unknown-entry stats are a downstream routing concept and are not the
  same thing as line-buffer malformed/headerless boundary coverage.
- Tailer/router integration tests may be used as adjacent context, but this
  contract's coverage basis is the entry-boundary layer.

## Required Guarantees

### In-Scope Scenario Family

Only this scenario family is in scope:

```text
log_runtime.malformed_or_headerless
```

Codex C may move this family from `missing` to `covered_synthetic` only if it
adds safe repo-owned synthetic metadata and focused tests that keep all
non-claims explicit.

### Required Manifest Entry

If Codex C implements coverage, it should add exactly one manifest entry:

```text
malformed_headerless_synthetic_v1
```

Required shape:

- `entry_type`: `session_ledger_entry`
- `source_kind`: `synthetic_committed_fixture`
- `commit_status`: `committed`
- `privacy_class`: `synthetic_committable`
- `sanitization_status`: `synthetic`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/372`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_malformed_headerless_coverage.md`
- `scenario_families`: `["log_runtime.malformed_or_headerless"]`
- `parser_event_families`: `[]`
- `coverage_status`: `covered_synthetic`
- `coverage_basis`: `["fixture_metadata_only", "parser_behavior_verified"]`

Suggested `parser_claim_families`:

- `line_buffer_header_classification`
- `line_buffer_headerless_orphan_noise_ignored`
- `line_buffer_unknown_header_boundary`
- `line_buffer_partial_line_boundary`
- `line_buffer_multiline_boundary`
- `malformed_headerless_privacy_boundary`

The empty `parser_event_families` list is intentional. Malformed/headerless
coverage is entry-boundary evidence, not parser event-family coverage. Codex C
must not invent a malformed/headerless event family or event class to make the
corpus row look like event coverage.

The manifest entry may reference focused line-buffer tests and corpus parity
tests as evidence paths. It must not include raw log lines, private local
paths, private runtime report paths, external corpus paths, compressed log
paths, local app-data paths, IP/network traces, or raw payload dumps.

### Required Session-Ledger Entry

If Codex C implements coverage, it should add exactly one session-ledger entry:

```text
malformed_headerless_synthetic_v1
```

Required behavior:

- `source_kind`: `synthetic_committed_fixture`
- `commit_status`: `committed`
- `privacy_class`: `synthetic_committable`
- `sanitization_status`: `synthetic`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/372`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_malformed_headerless_coverage.md`
- `scenario_families`: `["log_runtime.malformed_or_headerless"]`
- `format_family`: `log_runtime`
- `match_shape`: `line_buffer_boundary_signal_only`
- `record_summary`: `synthetic_line_buffer_summary_only`
- `parser_coverage.event_families`: `{}`
- `parser_coverage.unknown_entries`: `0`
- `parser_coverage.truncation_count`: `0`
- `parser_coverage.line_buffer_headerless_orphan_lines_ignored`: `1`
- `parser_coverage.line_buffer_unknown_header_entries`: `1`
- `parser_coverage.line_buffer_partial_fragments_joined`: `1`
- `parser_coverage.line_buffer_multiline_entries_finalized`: `1`
- `parser_coverage.line_buffer_single_line_headers_emitted`: `1`
- `game_rows`: `{"count": 0, "result_shape": "not_applicable"}`

Required redaction flags:

- `raw_log_lines_included`: `false`
- `private_paths_included`: `false`
- `raw_payloads_included`: `false`
- `external_logs_included`: `false`
- `decklists_included`: `false`

The session entry must say clearly that it is synthetic line-buffer summary
only. It must not contain a copied Player.log line, copied Manasight row, live
runtime report, private report path, raw line-buffer text, raw entry body, IP
or network trace, decklist, strategy note, or private machine identifier.

If Codex C finds that the session-ledger validator or tests reject
line-buffer-specific count keys under `parser_coverage`, it must route back to
Codex B/E for a schema clarification. It must not silently encode the counts
in a less machine-readable field or change schema validation behavior under
this contract-only coverage slice.

### Allowed Evidence Model

Allowed committed evidence:

- existing `LineBuffer`, `EntryHeader`, `LogEntry`, `classify_line_header(...)`,
  and `is_single_line_header(...)` source and focused tests;
- existing committed Mythic Edge line-buffer corpus fixtures and tests;
- existing tailer/router integration tests as read-only adjacent context;
- synthetic manifest/session-ledger metadata;
- generic entry-boundary claim labels and counts;
- public Manasight category labels only through existing taxonomy context;
- contract-test and implementation-handoff Markdown that summarizes evidence
  without reproducing raw/private log lines.

Allowed synthetic payload concepts:

- a generic orphan/headerless noise line ignored with no open entry;
- a generic unknown bracketed header becoming an `EntryHeader.UNKNOWN` entry;
- a generic partial header fragment joined before emission;
- a generic multiline entry finalized before the next header;
- a generic single-line header emitted cleanly;
- generic missing-game-row statement because malformed/headerless entry
  boundary coverage is not a match/game fact;
- generic redaction statement that raw log text, private reports, local
  runtime paths, and local app-data contents are not committed corpus evidence.

Forbidden committed evidence:

- raw/private Player.log excerpts;
- raw local logs;
- private smoke outputs;
- actual local MTGA malformed-log verification reports;
- local app-data contents;
- local runtime artifacts;
- generated data;
- SQLite files;
- workbook exports;
- failed post artifacts;
- credentials, tokens, API keys, webhook URLs, or secrets;
- private machine identifiers, account identifiers, local user paths, IP
  addresses, network traces, or private report locations;
- new Manasight raw logs, `.log.gz` files, raw session payloads, compressed
  corpus files, hash lists, byte-size row lists, capture-date row lists,
  parser source, or external corpus contents;
- decklists, deck names, card choices, card pools, strategy notes, or private
  reports.

### Entry-Boundary Boundary

Coverage must be grounded in existing line-buffer/header-boundary behavior:

```text
LineBuffer.feed(...)
LineBuffer.flush()
EntryHeader.UNKNOWN
classify_line_header(...)
is_single_line_header(...)
```

Codex C may mention tailer/router behavior as adjacent consumer context, but
tailer/router outcomes must not be the sole coverage basis. This protects the
distinction between:

- line-buffer ownership of entry boundaries and header classification; and
- downstream parser/router ownership of whether emitted entries route to
  parser events or become unknown entries.

If Codex C cannot demonstrate the entry-boundary behavior with existing tests,
it must add focused tests only if the existing implementation already supports
the contract. If a test would require behavior changes, Codex C must stop and
route back to Codex B/E.

### Adjacent Family Non-Claims

The implementation must not change or imply coverage for:

- `log_runtime.unknown_entry`
- `log_runtime.rotation`
- `log_runtime.timestamp_anomaly` beyond preserving the already-covered #370
  status
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

- `log_runtime.malformed_or_headerless` may become `covered_synthetic`.
- `log_runtime.timestamp_anomaly` must remain `covered_synthetic` from issue
  #370.
- `log_runtime.detailed_logs_disabled` must remain `covered_synthetic` from
  issue #368.
- `log_runtime.rotation` must remain `blocked_external_boundary` unless a
  later issue and contract authorize Mythic Edge-owned rotation evidence.
- `log_runtime.unknown_entry` must remain `missing` unless a later issue and
  contract authorize unknown-entry coverage.
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

The expected report row for `log_runtime.malformed_or_headerless` should show:

- `coverage_status`: `covered_synthetic`
- `coverage_basis`: `["fixture_metadata_only", "parser_behavior_verified"]`
- `mythic_edge_entries`: `["malformed_headerless_synthetic_v1"]`
- notes stating that this proves synthetic line-buffer/header-boundary
  metadata only and does not prove unknown-entry routing, log drift detection,
  log rotation, semantic recovery from arbitrary malformed Player.log payloads,
  private smoke, release readiness, analytics truth, AI truth, coaching truth,
  or production behavior.

The report summary may change by exactly one family moving from `missing` to
`covered_synthetic`. Expected current-base movement is:

- before: `partial_coverage_map_ready (45 families, 6 committed, 21 missing)`
- after: `partial_coverage_map_ready (45 families, 6 committed, 20 missing)`

If counts differ because the base branch changed, Codex C must explain the
current base in its implementation handoff.

## Inputs

Primary inputs:

- corpus manifest:
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- session ledger:
  `tests/fixtures/parser_corpus/session_ledger.v1.json`
- entry-boundary source:
  `src/mythic_edge_parser/log/entry.py`
- focused line-buffer/header tests:
  `tests/test_log_entry_headers.py`
- focused edge tests:
  `tests/test_entry_buffer_edges.py`
- line-buffer corpus tests:
  `tests/test_line_buffer_corpus.py`
- corpus parity report tests:
  `tests/test_corpus_parity_report.py`

Optional context inputs:

- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_tailer_router_integration.py`
- relevant diagnostics, drift, golden replay, and feature-equity tests

Forbidden inputs:

- raw/private Player.log files;
- actual local MTGA malformed-log verification reports;
- private local MTGA settings state;
- private smoke reports;
- local app-data contents;
- generated runtime artifacts;
- new Manasight raw corpus contents;
- external compressed logs;
- credentials, secrets, tokens, API keys, or webhook URLs.

## Outputs

Required Codex B output:

- `docs/contracts/parser_corpus_malformed_headerless_coverage.md`

Expected Codex C outputs if implementation proceeds:

- manifest entry for `malformed_headerless_synthetic_v1`
- session-ledger entry for `malformed_headerless_synthetic_v1`
- focused corpus parity tests proving the new family status
- focused line-buffer/header-boundary tests if current evidence is not already
  asserted strongly enough
- implementation handoff:
  `docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md`
- contract test report:
  `docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md`

No output may include raw/private log text, private paths, raw payload dumps,
runtime artifacts, generated databases, workbook exports, credentials, tokens,
API keys, webhook URLs, local app-data contents, or external raw corpus
contents.

## Invariants

- `log_runtime.malformed_or_headerless` coverage is metadata/report-only.
- `LineBuffer` remains parser-owned entry-boundary truth.
- Corpus coverage does not authorize line-buffer behavior changes.
- Corpus coverage does not authorize parser behavior changes.
- Corpus coverage does not authorize new parser event classes.
- Corpus coverage does not authorize unknown-entry coverage.
- Corpus coverage does not authorize diagnostics, drift sensor, golden replay,
  feature-equity, runtime status, workbook, webhook, Apps Script, Google
  Sheets, local app, analytics, AI, coaching, CI, release, or production
  changes.
- Corpus metadata must not contain raw/private Player.log excerpts.
- Corpus metadata must not contain new raw Manasight corpus contents.
- Corpus metadata must not contain private local paths, settings dumps, or
  runtime reports.
- `log_runtime.malformed_or_headerless` must not be used to claim full
  log-runtime parity.
- Synthetic malformed/headerless evidence must not become private live-log
  drift proof.

## Error Behavior

If the current line-buffer tests do not show orphan/headerless noise handling,
unknown bracketed header boundaries, partial-line handling, multiline entry
boundaries, and clean single-line emission, Codex C must add focused tests
only if the existing implementation already supports them. If a test would
require behavior changes, Codex C must stop and route back to Codex B/E.

If the corpus report cannot represent the new coverage row using existing
schemas, Codex C must stop and route back for a schema contract. This issue
does not authorize corpus report schema changes.

If the session-ledger validator rejects the preferred
`parser_coverage.line_buffer_*` fields, Codex C must stop and route back for a
schema clarification. This issue does not authorize weakening validation or
silently dropping the machine-readable line-buffer counts.

If private evidence seems necessary to prove coverage, Codex C must stop. This
issue authorizes only synthetic committed metadata and existing line-buffer
tests.

If the base branch has changed and report counts no longer match this
contract's observed counts, Codex C may proceed only if the in-scope family,
coverage status, and non-claims remain intact. The implementation handoff must
record the updated counts and base commit.

## Side Effects

Codex B side effects:

- writes this contract file only.

Codex C side effects authorized later:

- edits committed corpus manifest/session-ledger metadata;
- edits focused corpus parity and line-buffer tests;
- writes implementation handoff and contract test report.

Codex C side effects forbidden:

- line-buffer behavior changes;
- header classification behavior changes;
- tailer behavior changes;
- router semantic changes;
- parser behavior changes;
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
   `log_runtime.malformed_or_headerless` status.
3. Verify focused line-buffer/header tests for orphan/headerless noise,
   unknown bracketed headers, partial fragments, multiline boundaries, and
   clean single-line emission.
4. Add the manifest entry.
5. Add the session-ledger entry.
6. Add or update focused corpus parity tests for
   `log_runtime.malformed_or_headerless`.
7. Add focused line-buffer/header-boundary tests only if current coverage is
   insufficient and no behavior change is required.
8. Run validation.
9. Write implementation handoff and contract test report.

## Compatibility

Compatibility expectations:

- Preserve existing corpus manifest object and schema version.
- Preserve existing session-ledger object and schema version.
- Preserve existing coverage status vocabulary.
- Preserve existing report summary shape.
- Preserve existing `LineBuffer`, `LogEntry`, and `EntryHeader` public names.
- Preserve existing header classification behavior.
- Preserve existing tailer/router consumers of `LogEntry`.
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
  tests/test_log_entry_headers.py \
  tests/test_entry_buffer_edges.py \
  tests/test_line_buffer_corpus.py

python3 -m pytest -q tests/test_tailer_router_integration.py

python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
```

Recommended path-scoped governance checks:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_malformed_headerless_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_log_entry_headers.py \
  tests/test_entry_buffer_edges.py \
  tests/test_line_buffer_corpus.py \
  docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_malformed_headerless_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_log_entry_headers.py \
  tests/test_entry_buffer_edges.py \
  tests/test_line_buffer_corpus.py \
  docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_malformed_headerless_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_log_entry_headers.py \
  tests/test_entry_buffer_edges.py \
  tests/test_line_buffer_corpus.py \
  docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md \
  | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

Codex C may add more focused checks if it edits tests adjacent to tailer,
router, diagnostics, drift sensor, golden replay, or feature-equity consumers.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_corpus_malformed_headerless_coverage.md`.
- The contract names the owned module, issue, tracker, branch, and base commit.
- The contract authorizes only metadata/report-only corpus coverage for
  `log_runtime.malformed_or_headerless`.
- The contract defines the exact manifest and session-ledger entry ID
  `malformed_headerless_synthetic_v1`.
- The contract explicitly defines `parser_event_families` as empty for this
  corpus row because the evidence is entry-boundary behavior, not a parser
  event.
- The contract preserves line-buffer behavior, parser behavior, and protected
  surfaces.
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

Act as Codex C: Module Implementer for issue #372, malformed/headerless log
corpus coverage under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/372

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Previous completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/370

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/371

Previous merge commit:
4dac867bd22fbb8465c9c8c44b250d129f653121

Base branch:
codex/parser-parity

Implementation branch:
codex/parser-corpus-malformed-headerless-coverage

Contract:
docs/contracts/parser_corpus_malformed_headerless_coverage.md

Goal:
Implement the smallest metadata/report-only corpus parity change that moves
`log_runtime.malformed_or_headerless` to safe Mythic Edge-owned synthetic
coverage, grounded in existing `LineBuffer`, `EntryHeader`, and header-boundary
behavior.

Do:
- Compare current corpus manifest, session ledger, line-buffer tests, and
  corpus parity report against the contract before editing.
- Add exactly one manifest entry and one session-ledger entry for
  `malformed_headerless_synthetic_v1` unless a contract-test note identifies a
  contract mismatch that must be routed back.
- Keep coverage grounded in line-buffer/header-boundary evidence, not router
  unknown-entry stats, diagnostics summaries, drift reports, private
  Player.log checks, or live MTGA runtime reports.
- Keep `parser_event_families` empty for this coverage row; do not invent a
  malformed/headerless parser event family.
- Add or update focused tests for the corpus parity row and line-buffer
  evidence only as needed.
- Produce
  `docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md`.
- Produce
  `docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md`.

Do not:
- Change LineBuffer behavior, header classification behavior, tailer behavior,
  parser behavior, timestamp parsing behavior, router semantics, parser event
  classes, parser state final reconciliation, match/game identity,
  deduplication, diagnostics behavior, drift sensor behavior, golden replay
  behavior, feature-equity behavior, runtime status behavior, workbook schema,
  webhook payload shape, Apps Script behavior, Google Sheets sync, output
  transport, analytics truth, AI truth, coaching behavior, CI gates, merge
  policy, deploy policy, production behavior, or final integration policy.
- Commit raw/private Player.log excerpts, raw local logs, actual malformed-log
  runtime reports, private local app-data contents, generated artifacts,
  SQLite files, failed posts, runtime status files, workbook exports, secrets,
  credentials, tokens, API keys, webhook URLs, Manasight raw logs, external
  compressed corpus files, or external raw corpus contents.
- Claim full Mythic Edge corpus parity, full log-runtime parity, unknown-entry
  routing, log drift detection, log rotation support, semantic recovery from
  arbitrary malformed Player.log payloads, private smoke readiness, release
  readiness, merge readiness, deploy readiness, analytics truth, AI truth,
  gameplay advice, hidden-card inference, archetype classification, or coaching
  truth.
- Close tracker #158 or issue #372.
- Target main directly.
- Stage or commit unless explicitly asked.

Validation:
- Run the corpus parity report command from the contract.
- Run the focused pytest, ruff, agent-docs, diff-check, and path-scoped
  governance checks listed in the contract.
- Run tailer/router integration only as adjacent consumer-regression evidence;
  downstream router outcomes must not be the primary corpus coverage basis.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/372"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/370"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/371"
  previous_merge_commit: "4dac867bd22fbb8465c9c8c44b250d129f653121"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_malformed_headerless_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md"
  verdict: "contract_ready_for_synthetic_malformed_headerless_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-malformed-headerless-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_line_buffer_corpus.py"
    - "python3 -m pytest -q tests/test_tailer_router_integration.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
  stop_conditions:
    - "Do not implement LineBuffer behavior, header classification, tailer behavior, parser behavior, or router semantic changes in this corpus coverage slice."
    - "Do not invent a malformed/headerless parser event or event family; this coverage is entry-boundary evidence."
    - "Do not use router unknown-entry stats, diagnostics, drift reports, golden replay, feature-equity reports, private Player.log checks, or live runtime reports as the sole coverage basis."
    - "Do not commit raw/private Player.log excerpts, raw local logs, malformed-log runtime reports, private app-data contents, generated artifacts, SQLite files, workbook exports, failed posts, runtime artifacts, credentials, tokens, API keys, webhook URLs, Manasight raw logs, or external raw corpus contents."
    - "Do not claim full Mythic Edge corpus parity, full log-runtime parity, unknown-entry routing, log drift detection, log rotation support, semantic recovery from arbitrary malformed Player.log payloads, private smoke readiness, release readiness, merge readiness, deploy readiness, analytics truth, AI truth, gameplay advice, hidden-card inference, archetype classification, or coaching truth."
    - "Do not target main directly or close tracker #158 or issue #372."
```
