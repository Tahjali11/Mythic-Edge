# Parser Corpus Detailed Logs Disabled Coverage Contract

## Module

Detailed logs disabled corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`log_runtime.detailed_logs_disabled` with repo-owned synthetic metadata and
existing parser behavior evidence for explicit Arena detailed-logging status
markers. It proves only that Mythic Edge has safe corpus metadata for parser-
owned `DETAILED LOGS: DISABLED` handling. It does not prove live MTGA settings,
private Player.log resilience, log rotation, malformed/headerless log handling,
timestamp anomaly handling, unknown-entry handling, diagnostics readiness,
release readiness, full runtime health, or full Mythic Edge corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/368
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/366
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/367
- Previous merge commit:
  `d3a98f01d2fe048340489009ad703149e1fc30ef`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-detailed-logs-disabled-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `d3a98f01d2fe048340489009ad703149e1fc30ef`
- target_artifact:
  `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md`
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
- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- `docs/contracts/parser_corpus_connection_error_payload_coverage.md`
- `docs/contracts/parser_corpus_connection_disconnect_coverage.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/contracts/parser_saved_event_replay.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/metadata.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_parser_small_modules.py`
- `tests/test_parsers.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_tailer_router_integration.py`
- `tests/test_stream_integration.py`

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
`log_runtime.detailed_logs_disabled` scenario family. Parser modules and events
own the underlying detailed-logging status interpretation. Corpus parity
artifacts own only the coverage status claim that Mythic Edge has safe
repo-owned evidence for this narrow family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence, but it is not a Parser behavior module and is not a
runtime, diagnostics, analytics, workbook, local app, AI, coaching, release,
or production module.

## Truth Owner

Truth owner for `log_runtime.detailed_logs_disabled` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for parser behavior referenced by this coverage:

- `src/mythic_edge_parser/parsers/metadata.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`

Truth owner for stream/tailer operational behavior:

- `src/mythic_edge_parser/stream.py`
- tailer/router integration modules and their focused tests
- diagnostics modules where explicitly contracted

Truth boundary:

- `log.entry` owns classifying `DETAILED LOGS:` lines as metadata entries.
- `metadata.try_parse(...)` owns parser-owned `DetailedLoggingStatus`
  emission for explicit `DETAILED LOGS: ENABLED` and
  `DETAILED LOGS: DISABLED` metadata entries.
- `DetailedLoggingStatusEvent` owns the event kind and payload contract.
- Router dispatch owns which metadata entries can reach `metadata.try_parse`.
- Stream/tailer code may observe or infer detailed-logging status, but this
  issue's corpus claim must be grounded in explicit metadata-line evidence.
- Corpus parity artifacts own the report-only coverage row for
  `log_runtime.detailed_logs_disabled`.
- Corpus coverage status is review metadata. It is not parser truth, runtime
  health truth, live MTGA settings truth, diagnostics truth, workbook truth,
  analytics truth, AI truth, coaching truth, merge readiness, deploy readiness,
  public/private release readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing DetailedLoggingStatus parser behavior for explicit metadata markers
  -> bounded synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for log_runtime.detailed_logs_disabled
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change metadata marker matching, line-buffer
  classification, event classes, router dispatch, stream/tailer behavior,
  parser state, diagnostics behavior, runtime status behavior, workbook output,
  analytics, AI, coaching, release policy, or production behavior.
- Corpus metadata must not turn synthetic detailed-logging evidence into a
  claim about actual MTGA settings, private Player.log resilience, runtime
  health, live diagnostics readiness, launcher readiness, or broad log-runtime
  parity.

Protected surfaces explicitly not touched:

- parser behavior
- metadata parser marker matching
- line-buffer/header classification behavior
- stream/tailer operational behavior
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

- `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_parser_small_modules.py`
- `tests/test_parsers.py`
- `docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/metadata.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_tailer_router_integration.py`
- `tests/test_stream_integration.py`

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- line-buffer/header classification changes
- stream/tailer behavior changes
- parser event class changes
- router changes
- diagnostics behavior changes
- runtime status changes
- live private smoke execution
- committed raw log fixtures
- private Player.log fixture work
- actual MTGA settings inspection
- local app-data inspection
- Manasight corpus import
- log rotation, malformed/headerless log, timestamp anomaly, unknown-entry,
  reconnect, firewall/network-drop, or private resilience coverage work
- connection coverage work already owned by issues #364 and #366
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
`d3a98f01d2fe048340489009ad703149e1fc30ef`:

- Tracker #158 is open.
- Issue #368 is open as the detailed logs disabled corpus coverage child.
- Issue #366 was merged through PR #367 into `codex/parser-parity` at
  `d3a98f01d2fe048340489009ad703149e1fc30ef`.
- The current corpus parity report returns
  `partial_coverage_map_ready (45 families, 6 committed, 23 missing)`.
- `log_runtime.detailed_logs_disabled` exists in the corpus taxonomy.
- No committed manifest entry currently owns
  `log_runtime.detailed_logs_disabled`.
- No session-ledger entry currently owns
  `log_runtime.detailed_logs_disabled`.
- `log_runtime.rotation` is represented only by
  `external_reference_category_boundary` and is
  `blocked_external_boundary`.
- `log_runtime.malformed_or_headerless`, `log_runtime.timestamp_anomaly`, and
  `log_runtime.unknown_entry` are taxonomy families but have no Mythic
  Edge-owned coverage entries.

Observed parser behavior:

- `src/mythic_edge_parser/log/entry.py` classifies lines beginning with
  `DETAILED LOGS:` as metadata entries.
- `src/mythic_edge_parser/parsers/metadata.py` emits
  `DetailedLoggingStatus` for metadata entries whose stripped body is exactly
  `DETAILED LOGS: ENABLED` or `DETAILED LOGS: DISABLED`.
- `DETAILED LOGS: ENABLED` produces payload `{"enabled": True}`.
- `DETAILED LOGS: DISABLED` produces payload `{"enabled": False}`.
- Whitespace around the recognized marker is stripped before lookup.
- Unknown metadata bodies, non-metadata entries, and unrecognized
  detailed-logging values return no parser event.
- `DetailedLoggingStatusEvent` owns event kind `DetailedLoggingStatus`.
- Router and integration tests exercise metadata dispatch for
  `DetailedLoggingStatus`.

Observed adjacent runtime behavior:

- Stream/tailer code can emit or infer `DetailedLoggingStatus` in operational
  contexts.
- Diagnostics mode expects `DetailedLoggingStatus` as one runtime event family.
- Those behaviors may be regression-tested, but they are not this issue's
  primary coverage basis and must not be recast as live settings truth.

## Required Guarantees

### In-Scope Scenario Family

Only this scenario family is in scope:

```text
log_runtime.detailed_logs_disabled
```

Codex C may move this family from `missing` to `covered_synthetic` only if it
adds safe repo-owned synthetic metadata and focused tests that keep all
non-claims explicit.

### Required Manifest Entry

If Codex C implements coverage, it should add exactly one manifest entry:

```text
detailed_logs_disabled_synthetic_v1
```

Required shape:

- `entry_type`: `session_ledger_entry`
- `source_kind`: `synthetic_committed_fixture`
- `commit_status`: `committed`
- `privacy_class`: `synthetic_committable`
- `sanitization_status`: `synthetic`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/368`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`
- `scenario_families`: `["log_runtime.detailed_logs_disabled"]`
- `parser_event_families`: `["DetailedLoggingStatus"]`
- `coverage_status`: `covered_synthetic`
- `coverage_basis`: `["fixture_metadata_only", "parser_behavior_verified"]`

Suggested `parser_claim_families`:

- `detailed_logging_status_event`
- `detailed_logs_disabled_marker`
- `detailed_logging_metadata_parser`
- `detailed_logging_privacy_boundary`

The manifest entry may reference focused parser tests and schema snapshots as
evidence paths. It must not include raw log lines, private local paths, MTGA
settings paths, private report paths, external corpus paths, compressed log
paths, local app-data paths, or raw payload dumps.

### Required Session-Ledger Entry

If Codex C implements coverage, it should add exactly one session-ledger entry:

```text
detailed_logs_disabled_synthetic_v1
```

Required behavior:

- `source_kind`: `synthetic_committed_fixture`
- `commit_status`: `committed`
- `privacy_class`: `synthetic_committable`
- `sanitization_status`: `synthetic`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/368`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`
- `scenario_families`: `["log_runtime.detailed_logs_disabled"]`
- `format_family`: `log_runtime`
- `match_shape`: `detailed_logging_status_signal_only`
- `record_summary`: `synthetic_metadata_summary_only`
- `parser_coverage.event_families`: `{"DetailedLoggingStatus": 1}` unless
  Codex C adds a reasoned contract-test note explaining a different safe count.
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
It must not contain a copied Player.log line, copied Manasight row, live MTGA
settings dump, local app-data path, private report path, raw metadata payload,
decklist, strategy note, or private machine identifier.

### Allowed Evidence Model

Allowed committed evidence:

- existing parser source and focused parser tests for
  `DetailedLoggingStatus`;
- existing log-entry/header tests for `DETAILED LOGS:` classification;
- existing router, schema snapshot, and integration tests that exercise
  `DetailedLoggingStatus`;
- synthetic manifest/session-ledger metadata;
- generic parser claim labels and counts;
- public Manasight category labels only through existing taxonomy context;
- contract-test and implementation-handoff Markdown that summarizes evidence
  without reproducing raw/private log lines.

Allowed synthetic payload concepts:

- a generic explicit detailed-logging disabled marker;
- optional paired reference to the already-tested enabled marker, only as
  parser behavior context;
- generic missing-game-row statement because detailed-logging status coverage
  is not a match/game fact;
- generic redaction statement that raw log text, local settings paths, private
  reports, and local app-data contents are not committed corpus evidence.

Forbidden committed evidence:

- raw/private Player.log excerpts;
- raw local logs;
- private smoke outputs;
- actual MTGA settings dumps or screenshots;
- local app-data contents;
- local runtime artifacts;
- generated data;
- SQLite files;
- workbook exports;
- failed post artifacts;
- credentials, tokens, API keys, webhook URLs, or secrets;
- private machine identifiers, account identifiers, local user paths, or
  private report locations;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size row lists, capture-date row lists, parser
  source, or external corpus contents;
- decklists, deck names, card choices, card pools, strategy notes, or private
  reports.

### Explicit Metadata-Line Boundary

Coverage must be grounded in explicit metadata parser evidence:

```text
DETAILED LOGS: DISABLED
```

Codex C may mention stream/tailer behavior as adjacent regression context, but
stream/tailer inference must not be the sole coverage basis. This protects the
distinction between:

- parser-owned interpretation of an explicit metadata marker; and
- operational inference that detailed logs may be unavailable or delayed.

If Codex C cannot demonstrate explicit metadata-line support with existing
tests, it must route back to Codex B/E for contract clarification. It must not
patch parser behavior under this corpus-only issue.

### Adjacent Family Non-Claims

The implementation must not change or imply coverage for:

- `log_runtime.rotation`
- `log_runtime.malformed_or_headerless`
- `log_runtime.timestamp_anomaly`
- `log_runtime.unknown_entry`
- `connection.reconnect`
- `connection.disconnect` beyond preserving the already-covered #366 status
- `connection.connection_error_payload` beyond preserving the already-covered
  #364 status
- `connection.firewall_or_network_drop`
- timer/inactivity runtime families
- private live-log smoke
- release readiness or runtime resilience

Specific status expectations:

- `log_runtime.detailed_logs_disabled` may become `covered_synthetic`.
- `log_runtime.rotation` must remain `blocked_external_boundary` unless a
  later issue and contract authorize Mythic Edge-owned rotation evidence.
- `log_runtime.malformed_or_headerless`, `log_runtime.timestamp_anomaly`, and
  `log_runtime.unknown_entry` must remain `missing` unless later issues and
  contracts authorize coverage.
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

The expected report row for `log_runtime.detailed_logs_disabled` should show:

- `coverage_status`: `covered_synthetic`
- `coverage_basis`: `["fixture_metadata_only", "parser_behavior_verified"]`
- `mythic_edge_entries`: `["detailed_logs_disabled_synthetic_v1"]`
- notes stating that this proves synthetic parser-owned detailed-logging
  metadata only and does not prove live MTGA settings, log rotation,
  malformed/headerless log handling, timestamp anomaly handling,
  unknown-entry routing, private smoke, release readiness, analytics truth, AI
  truth, coaching truth, or production behavior.

The report summary may change by exactly one family moving from `missing` to
`covered_synthetic`. If counts differ because the base branch changed, Codex C
must explain the current base in its implementation handoff.

## Inputs

Primary inputs:

- corpus manifest:
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- session ledger:
  `tests/fixtures/parser_corpus/session_ledger.v1.json`
- parser source:
  `src/mythic_edge_parser/parsers/metadata.py`
- log-entry classification source:
  `src/mythic_edge_parser/log/entry.py`
- event source:
  `src/mythic_edge_parser/events.py`
- focused tests:
  `tests/test_parser_small_modules.py`, `tests/test_parsers.py`,
  `tests/test_log_entry_headers.py`, `tests/test_event_schema_snapshots.py`,
  `tests/test_tailer_router_integration.py`

Optional context inputs:

- `src/mythic_edge_parser/stream.py`
- `tests/test_stream_integration.py`
- `docs/contracts/parser_diagnostics_mode.md`

Forbidden inputs:

- raw/private Player.log files;
- private local MTGA settings state;
- private smoke reports;
- local app-data contents;
- generated runtime artifacts;
- Manasight raw corpus contents;
- external compressed logs;
- credentials, secrets, tokens, API keys, or webhook URLs.

## Outputs

Required Codex B output:

- `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`

Expected Codex C outputs if implementation proceeds:

- manifest entry for `detailed_logs_disabled_synthetic_v1`
- session-ledger entry for `detailed_logs_disabled_synthetic_v1`
- focused corpus parity tests proving the new family status
- focused parser evidence tests if current disabled-marker evidence is not
  already asserted strongly enough
- implementation handoff:
  `docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md`
- contract test report:
  `docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md`

No output may include raw/private log text, private paths, raw payload dumps,
runtime artifacts, generated databases, workbook exports, credentials, tokens,
API keys, webhook URLs, or local app-data contents.

## Invariants

- `log_runtime.detailed_logs_disabled` coverage is metadata/report-only.
- `DetailedLoggingStatus` remains parser-owned truth.
- `DetailedLoggingStatus` payload shape remains owned by parser/event code.
- Corpus coverage does not authorize parser behavior changes.
- Corpus coverage does not authorize stream/tailer, diagnostics, runtime
  status, workbook, webhook, Apps Script, Google Sheets, local app, analytics,
  AI, coaching, CI, release, or production changes.
- Corpus metadata must not contain raw/private Player.log excerpts.
- Corpus metadata must not contain raw Manasight corpus contents.
- Corpus metadata must not contain private local paths or settings dumps.
- `log_runtime.detailed_logs_disabled` must not be used to claim full log-
  runtime parity.
- `DetailedLoggingStatus` evidence must not become live MTGA settings truth.

## Error Behavior

If the current parser tests do not show explicit
`DETAILED LOGS: DISABLED -> {"enabled": False}` behavior, Codex C must add a
focused test only if the existing implementation already supports it. If a
test would require behavior changes, Codex C must stop and route back to Codex
B/E.

If the corpus report cannot represent the new coverage row using existing
schemas, Codex C must stop and route back for a schema contract. This issue
does not authorize new corpus schema fields.

If private evidence seems necessary to prove coverage, Codex C must stop. This
issue authorizes only synthetic committed metadata and existing parser tests.

If the base branch has changed and report counts no longer match this
contract's observed counts, Codex C may proceed only if the in-scope family,
coverage status, and non-claims remain intact. The implementation handoff must
record the updated counts and base commit.

## Side Effects

Codex B side effects:

- writes this contract file only.

Codex C side effects authorized later:

- edits committed corpus manifest/session-ledger metadata;
- edits focused tests;
- writes implementation handoff and contract test report.

Codex C side effects forbidden:

- parser behavior changes;
- runtime behavior changes;
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
   `log_runtime.detailed_logs_disabled` status.
3. Verify focused parser tests for explicit disabled-marker behavior.
4. Add the manifest entry.
5. Add the session-ledger entry.
6. Add or update focused corpus parity tests for
   `log_runtime.detailed_logs_disabled`.
7. Add focused disabled-marker parser tests only if current coverage is
   insufficient and no behavior change is required.
8. Run validation.
9. Write implementation handoff and contract test report.

## Compatibility

Compatibility expectations:

- Preserve existing corpus manifest object and schema version.
- Preserve existing session-ledger object and schema version.
- Preserve existing coverage status vocabulary.
- Preserve existing report summary shape.
- Preserve existing parser event kind `DetailedLoggingStatus`.
- Preserve existing `enabled` boolean payload semantics.
- Preserve existing treatment of `DETAILED LOGS: ENABLED`.
- Preserve existing stream/tailer and diagnostics behavior.
- Preserve existing external-reference boundary entries.

This issue must not introduce compatibility shims, migration code, alternate
schema versions, new CLI flags, new environment variables, or new runtime
artifact shapes.

## Tests Required

Codex C should run, at minimum:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json

python3 -m pytest -q \
  tests/test_corpus_parity_report.py \
  tests/test_parser_small_modules.py \
  tests/test_parsers.py

python3 -m pytest -q \
  tests/test_log_entry_headers.py \
  tests/test_entry_buffer_edges.py \
  tests/test_router_unit.py \
  tests/test_event_schema_snapshots.py \
  tests/test_tailer_router_integration.py

python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
```

Recommended if stream/tailer evidence is mentioned in the handoff:

```bash
python3 -m pytest -q tests/test_stream_integration.py
```

Recommended path-scoped governance checks:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_parser_small_modules.py \
  tests/test_parsers.py \
  docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_parser_small_modules.py \
  tests/test_parsers.py \
  docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_parser_small_modules.py \
  tests/test_parsers.py \
  docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md \
  | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

Codex C may add more focused checks if it edits tests adjacent to router,
event schema snapshots, stream/tailer integration, or diagnostics context.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`.
- The contract names the owned module, issue, tracker, branch, and base commit.
- The contract authorizes only metadata/report-only corpus coverage for
  `log_runtime.detailed_logs_disabled`.
- The contract defines the exact manifest and session-ledger entry ID
  `detailed_logs_disabled_synthetic_v1`.
- The contract distinguishes explicit metadata-line parser evidence from
  stream/tailer operational inference.
- The contract preserves parser behavior and protected surfaces.
- The contract forbids raw/private Player.log excerpts, raw external corpus
  contents, local settings dumps, generated artifacts, and secrets.
- The contract lists adjacent non-claims and status expectations.
- The contract defines validation expectations for Codex C/E/F/G.
- The contract ends with a clear Codex C handoff.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #368, detailed logs disabled
corpus coverage under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/368

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Previous completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/366

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/367

Previous merge commit:
d3a98f01d2fe048340489009ad703149e1fc30ef

Base branch:
codex/parser-parity

Implementation branch:
codex/parser-corpus-detailed-logs-disabled-coverage

Contract:
docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md

Goal:
Implement the smallest metadata/report-only corpus parity change that moves
`log_runtime.detailed_logs_disabled` to safe Mythic Edge-owned synthetic
coverage, grounded in existing explicit `DETAILED LOGS: DISABLED` parser
behavior.

Do:
- Compare current corpus manifest, session ledger, parser tests, and corpus
  parity report against the contract before editing.
- Add exactly one manifest entry and one session-ledger entry for
  `detailed_logs_disabled_synthetic_v1` unless a contract-test note explains a
  necessary schema-preserving deviation.
- Keep coverage grounded in explicit metadata-line parser evidence, not live
  MTGA settings or private Player.log checks.
- Add or update focused tests for the corpus parity row and disabled-marker
  parser evidence only as needed.
- Produce
  `docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md`.
- Produce
  `docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md`.

Do not:
- Change parser behavior, line-buffer/header classification behavior, stream
  behavior, router semantics, parser event classes, parser state final
  reconciliation, match/game identity, deduplication, diagnostics behavior,
  runtime status behavior, workbook schema, webhook payload shape, Apps Script
  behavior, Google Sheets sync, output transport, analytics truth, AI truth,
  coaching behavior, CI gates, merge policy, deploy policy, production
  behavior, or final integration policy.
- Commit raw/private Player.log excerpts, raw local logs, MTGA settings dumps,
  private local app-data contents, generated artifacts, SQLite files, failed
  posts, runtime status files, workbook exports, secrets, credentials, tokens,
  API keys, webhook URLs, Manasight raw logs, external compressed corpus files,
  or external raw corpus contents.
- Claim full Mythic Edge corpus parity, full log-runtime parity, live settings
  truth, private smoke readiness, release readiness, merge readiness, deploy
  readiness, analytics truth, AI truth, gameplay advice, hidden-card inference,
  archetype classification, or coaching truth.
- Close tracker #158.
- Target main directly.
- Stage or commit unless explicitly asked.

Validation:
- Run the corpus parity report command from the contract.
- Run the focused pytest, ruff, agent-docs, diff-check, and path-scoped
  governance checks listed in the contract.
- Run `tests/test_stream_integration.py` only if you rely on stream/tailer
  evidence in the handoff; stream/tailer inference must not be the primary
  corpus coverage basis.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/368"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/366"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/367"
  previous_merge_commit: "d3a98f01d2fe048340489009ad703149e1fc30ef"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md"
  verdict: "contract_ready_for_synthetic_detailed_logs_disabled_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-detailed-logs-disabled-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_parser_small_modules.py tests/test_parsers.py"
    - "python3 -m pytest -q tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_event_schema_snapshots.py tests/test_tailer_router_integration.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
  stop_conditions:
    - "Do not implement parser behavior changes in this corpus coverage slice."
    - "Do not use stream/tailer inference as the sole coverage basis; coverage must be grounded in explicit metadata-line parser evidence."
    - "Do not commit raw/private Player.log excerpts, raw local logs, MTGA settings dumps, private app-data contents, generated artifacts, SQLite files, workbook exports, failed posts, runtime artifacts, credentials, tokens, API keys, webhook URLs, Manasight raw logs, or external raw corpus contents."
    - "Do not claim full Mythic Edge corpus parity, full log-runtime parity, live settings truth, private smoke readiness, release readiness, merge readiness, deploy readiness, analytics truth, AI truth, gameplay advice, hidden-card inference, archetype classification, or coaching truth."
    - "Do not target main directly or close tracker #158."
```
