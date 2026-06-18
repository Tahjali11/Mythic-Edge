# Parser Corpus Workbook Row Coverage Residual Contract

## Module

Parser corpus parity residual coverage for
`mythic_edge.workbook_row_coverage`.

Plain English: this slice lets Mythic Edge move the final non-blocked partial
corpus row off a broad count-ratchet baseline and onto an explicit
parser-side workbook-facing report-only boundary. It proves committed metadata
and tests exist for Python row shapes, schema vocabulary, runtime export rows,
repo-side Apps Script parity, and webhook row-shape guardrails. It does not
prove live workbook behavior, deployed Apps Script behavior, Google Sheets
sync, webhook delivery success, dashboard truth, release readiness, production
readiness, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/432
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/430
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/431
- Previous merge commit:
  `4c080d5820e34cb5bdd1f4df86350e45ee5b6874`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-workbook-row-coverage-residual`
- base_branch: `codex/parser-parity`
- observed_base_commit: `4c080d5820e34cb5bdd1f4df86350e45ee5b6874`
- target_artifact:
  `docs/contracts/parser_corpus_workbook_row_coverage_residual.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority inspected:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/contracts/parser_corpus_manifest_metadata_residual.md`
- `docs/contracts/parser_corpus_confidence_finality_degradation_residual.md`
- `docs/implementation_handoffs/parser_corpus_confidence_finality_degradation_residual_comparison.md`
- `docs/contract_test_reports/parser_corpus_confidence_finality_degradation_residual.md`
- `docs/contracts/parser_sheet_schema.md`
- `docs/contracts/parser_sheet_exports.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/parser_outputs.md`
- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`
- `docs/contract_test_reports/parser_sheet_schema.md`
- `docs/contract_test_reports/parser_sheet_exports.md`
- `docs/contract_test_reports/parser_runner.md`
- `docs/contract_test_reports/parser_outputs.md`
- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/outputs.py`
- `tests/test_sheet_schema.py`
- `tests/test_sheet_exports.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_app_models.py`
- `tests/test_app_outputs.py`
- `tests/test_webhook_payload_schema.py`

## Observed Current Behavior

Observed on `origin/codex/parser-parity` at merge commit
`4c080d5820e34cb5bdd1f4df86350e45ee5b6874`:

- Issue #432 is open and tracker #158 remains open.
- Issue #430 / PR #431 moved
  `mythic_edge.confidence_finality_degradation` to `covered_report_only`.
- The corpus parity report returns:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- The report summary is:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 17
  - `partial`: 1
  - `missing`: 0
  - `deferred`: 0
  - `blocked_private_evidence`: 2
  - `blocked_external_boundary`: 5
  - `not_applicable`: 0
- The only remaining non-blocked partial row is:
  - `mythic_edge.workbook_row_coverage`: `partial`, entry
    `feature_equity_corpus_baseline_v1`, basis `count_ratchet_only`

Current target row:

| scenario_family | coverage_status | coverage_basis | entry | note |
| --- | --- | --- | --- | --- |
| `mythic_edge.workbook_row_coverage` | `partial` | `count_ratchet_only` | `feature_equity_corpus_baseline_v1` | `Committed count-only baseline summarizes existing golden replay manifests.` |

The count-ratchet baseline proves a committed baseline exists. It does not
prove workbook schema parity, live workbook correctness, deployed Apps Script
behavior, Google Sheets sync, webhook delivery, runtime export behavior in live
operation, dashboard correctness, release readiness, production behavior,
tracker completion, or full corpus parity.

Observed parser-side workbook-facing evidence:

- `parser_sheet_schema.md` and `tests/test_sheet_schema.py` define and test
  Python-side Match Log/Game Log sync fields, runtime landing headers,
  runtime row families, Apps Script field-map order, Apps Script landing-header
  order, and the legacy `MGTA Start Time` compatibility spelling.
- `parser_sheet_exports.md` and `tests/test_sheet_exports.py` define and test
  runtime export row construction for Action Log, Deck Snapshot, Collection
  Snapshot, Parser Status, and Card Performance rows, including metadata
  fields and Apps Script-consumed snake_case keys.
- `repo_wide_workbook_webhook_schema_snapshots.md` and
  `tests/test_event_schema_snapshots.py` document and test committed
  repo-side schema snapshots for workbook row keys, sheet schema surfaces,
  runtime export row keys, and repo-side Apps Script parity.
- `parser_outputs.md` and `tests/test_webhook_payload_schema.py` document and
  test that webhook transport sends already-produced row dictionaries as the
  top-level JSON payload, without a wrapper.
- `parser_runner.md` documents runner orchestration, but runner behavior is not
  a source of workbook schema truth.

## Scope Decision

`mythic_edge.workbook_row_coverage` is approved to move from `partial` to
`covered_report_only` if Codex C adds a dedicated committed metadata-only
corpus entry and matching session-ledger entry for parser-side workbook-facing
row coverage.

The approved status is not `covered_committed` or `covered_synthetic`.

The approved basis is:

- `fixture_metadata_only`

`count_ratchet_only` is not sufficient for the target row after this contract.
Codex C should stop using `feature_equity_corpus_baseline_v1` as the source of
coverage for `mythic_edge.workbook_row_coverage`.

The new row may cite committed contracts, focused tests, and schema snapshot
surfaces as report-only evidence. It must not claim live workbook/App Script/
Google Sheets/webhook behavior.

If Codex C discovers that the current manifest/session-ledger vocabulary cannot
represent this boundary without source-code changes, Codex C must stop and
route back to Codex B or Codex A. Codex C must not add new coverage-basis
vocabulary, corpus report behavior, schema snapshot behavior, or workbook
behavior in this slice.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns the corpus metadata boundary for a workbook-facing coverage
row. It does not own workbook schema, row construction, output transport, Apps
Script behavior, Google Sheets sync, or live workbook state.

Supporting truth owners:

- `sheet_schema.py` owns Python-side workbook schema vocabulary and runtime
  landing header tuples.
- `models.py` owns parser-normalized Match Log and Game Log row construction.
- `sheet_exports.py` owns Python-side runtime workbook export row construction.
- `outputs.py` owns webhook transport mechanics after rows already exist.
- `runner.py` owns orchestration and side-effect ordering.
- `tools/google_apps_script/Code.gs` is repo-side Apps Script source and a
  downstream transport/upsert surface. It is not proof of deployed Apps Script
  or live workbook state.
- Corpus parity metadata owns scenario-family coverage status and review notes.

## Internal Project Area

Primary: Corpus / Provenance.

Adjacent supporting area: Workbook / Transport.

Quality / Governance owns the workflow artifacts, contract, implementation
handoff, and contract-test report.

This slice is not a parser behavior module, workbook migration, Apps Script
deployment, Google Sheets sync workflow, webhook delivery test, analytics
module, AI module, coaching module, release-readiness review, or tracker
completion issue.

## Truth Owner

Truth owner for the target corpus row:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for supporting workbook-facing row/schema evidence:

- `docs/contracts/parser_sheet_schema.md`
- `docs/contracts/parser_sheet_exports.md`
- `docs/contracts/parser_outputs.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`
- `tests/test_sheet_schema.py`
- `tests/test_sheet_exports.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_app_models.py`
- `tests/test_app_outputs.py`
- `tests/test_webhook_payload_schema.py`

Truth boundary:

- Corpus parity may report that committed parser-side workbook-facing metadata,
  contracts, and tests exist.
- Corpus parity must not report that live workbook tabs, deployed Apps Script,
  Google Sheets sync, webhook delivery, dashboard formulas, or production
  runtime behavior are validated.

## Bridge-Code Status

`deferred_future_boundary`

This contract references Workbook / Transport surfaces from Corpus /
Provenance metadata. It does not add bridge code or change allowed data flow.

Allowed data flow:

- committed workbook-facing contracts/tests/snapshots -> corpus metadata
  review row

Forbidden reverse-flow:

- corpus metadata must not modify parser row construction, workbook schema,
  Apps Script mappings, webhook transport, runtime behavior, workbook formulas,
  Google Sheets sync, dashboard logic, analytics truth, AI truth, or coaching
  truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_workbook_row_coverage_residual.md`

Codex C artifacts authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md`
- `docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md`

Files Codex C may read but must not modify in this slice:

- `docs/contracts/parser_sheet_schema.md`
- `docs/contracts/parser_sheet_exports.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/parser_outputs.md`
- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`
- `docs/contract_test_reports/parser_sheet_schema.md`
- `docs/contract_test_reports/parser_sheet_exports.md`
- `docs/contract_test_reports/parser_runner.md`
- `docs/contract_test_reports/parser_outputs.md`
- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/models.py`
- `tools/google_apps_script/Code.gs`
- focused workbook-facing tests named above

Not owned by this contract:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- router semantics;
- diagnostics, drift, golden replay, feature-equity, or evidence-ledger
  behavior;
- Match Log/Game Log/runtime row construction behavior;
- workbook schema or migrations;
- webhook payload shape;
- Apps Script behavior or deployment;
- Google Sheets sync;
- output transport behavior;
- runtime status files;
- failed posts;
- workbook exports;
- analytics truth;
- AI truth;
- coaching behavior;
- CI gates, merge readiness, deploy readiness, production readiness, or
  tracker lifecycle.

## Public Interface

Codex C is authorized to update only corpus metadata, focused corpus parity
tests, and handoff/report docs needed to satisfy this contract.

### Manifest Entry

Codex C should add a dedicated manifest entry with this identity unless a
focused implementation comparison shows an existing equivalent entry is safer:

```text
workbook_row_coverage_boundary_report_v1
```

Required manifest properties:

- `scenario_families`: exactly `["mythic_edge.workbook_row_coverage"]`
- `status`: `covered_report_only`
- `coverage_basis`: exactly `["fixture_metadata_only"]`
- `entry_type`: `session_ledger_entry`
- `source_kind`: `committed_count_only_report`
- `commit_status`: `committed`
- `privacy_class`: `committed_count_only`
- `sanitization_status`: `not_applicable_count_only`
- `parser_event_families`: empty

Recommended `parser_claim_families`:

- `match_log_row_keys`
- `game_log_row_keys`
- `sync_field_registry`
- `runtime_sheet_headers`
- `runtime_export_row_keys`
- `repo_side_apps_script_mapping_parity`
- `webhook_top_level_row_shape`
- `live_workbook_non_claim`
- `downstream_truth_non_claim`

Required known-gap language:

- parser-side workbook-facing metadata does not prove live workbook behavior;
- repo-side Apps Script parity does not prove deployed Apps Script behavior;
- webhook row-shape tests do not prove webhook delivery success;
- schema snapshots do not authorize schema migration;
- workbook formulas, dashboards, analytics, AI, coaching, release readiness,
  production readiness, and tracker completion remain non-claims.

Recommended path references:

- `docs/contracts/parser_sheet_schema.md`
- `docs/contracts/parser_sheet_exports.md`
- `docs/contracts/parser_outputs.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`
- `docs/contract_test_reports/parser_sheet_schema.md`
- `docs/contract_test_reports/parser_sheet_exports.md`
- `docs/contract_test_reports/parser_outputs.md`
- `docs/contract_test_reports/parser_runner.md`
- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`
- `tests/test_sheet_schema.py`
- `tests/test_sheet_exports.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_app_models.py`
- `tests/test_app_outputs.py`
- `tests/test_webhook_payload_schema.py`
- `tests/test_corpus_parity_report.py`

### Session Ledger Entry

Codex C should add a matching session-ledger entry with the same ID:

```text
workbook_row_coverage_boundary_report_v1
```

The session entry should summarize committed metadata and test-backed
parser-side workbook-facing coverage without embedding raw workbook exports,
runtime artifacts, webhook payload captures, private logs, or live Sheets data.

It may include count-like or availability-like fields under `parser_coverage`,
such as:

- `match_log_sync_fields`: `available`
- `game_log_sync_fields`: `available`
- `match_log_row_key_snapshot`: `available`
- `game_log_row_key_snapshot`: `available`
- `runtime_sheet_schema_snapshot`: `available`
- `runtime_export_row_key_snapshot`: `available`
- `repo_side_apps_script_parity_snapshot`: `available`
- `webhook_top_level_row_shape_test`: `available`
- `live_workbook_claims`: 0
- `deployed_apps_script_claims`: 0
- `google_sheets_sync_claims`: 0
- `webhook_delivery_claims`: 0
- `dashboard_truth_claims`: 0
- `analytics_truth_claims`: 0
- `ai_truth_claims`: 0
- `coaching_truth_claims`: 0

The session ledger must not include:

- raw Player.log lines;
- private local logs;
- private smoke outputs;
- generated/runtime artifacts;
- runtime status files;
- failed posts;
- workbook exports;
- live workbook tab contents;
- deployed Apps Script output;
- webhook URLs or payload captures;
- Google Sheets contents;
- SQLite databases;
- secrets, credentials, tokens, API keys, or webhook URLs;
- Manasight raw logs or external corpus contents.

### Existing Feature-Equity Baseline Entry

Codex C should stop using `feature_equity_corpus_baseline_v1` as the source of
coverage for `mythic_edge.workbook_row_coverage`.

After implementation, `feature_equity_corpus_baseline_v1` may continue covering
only already-authorized count-ratchet families such as `drift_debug.gsm_truncation`
if the current manifest still requires it. It must not own the workbook row
coverage residual.

## Inputs

Allowed committed inputs:

- corpus manifest metadata;
- session ledger metadata;
- corpus parity report output generated from committed metadata;
- parser-side workbook-facing contracts;
- parser-side workbook-facing tests;
- repo-side schema snapshot tests and fixtures;
- repo-side Apps Script source as committed text;
- local test output from focused commands.

Forbidden inputs:

- private Player.log files;
- private app-data;
- live MTGA output;
- live Google Sheets contents;
- deployed Apps Script execution;
- webhook POST captures;
- private smoke reports;
- workbook exports;
- runtime status artifacts;
- failed post artifacts;
- generated data;
- SQLite databases;
- Manasight raw logs, compressed corpus files, parser source, hash lists,
  byte-size lists, capture-date row lists, or external corpus contents;
- OpenAI/model-provider output.

## Outputs

Expected Codex C output:

- a dedicated corpus manifest entry for
  `workbook_row_coverage_boundary_report_v1`;
- a matching session-ledger entry;
- focused corpus parity test updates pinning the manifest/session row, report
  row, count movement, and unchanged blocked rows;
- implementation handoff:
  `docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md`;
- contract-test report:
  `docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md`.

Expected report summary after the narrow implementation:

- `total_scenario_families`: 45
- `covered_committed`: 6
- `covered_synthetic`: 14
- `covered_report_only`: 18
- `partial`: 0
- `missing`: 0
- `blocked_private_evidence`: 2
- `blocked_external_boundary`: 5

The overall report status should remain `partial_coverage_map_ready` while
blocked-private and blocked-external rows remain.

If exact counts differ because upstream work has already changed the corpus
matrix, Codex C must explain the drift and prove the target row behavior
directly.

## Invariants

- `mythic_edge.workbook_row_coverage` may move only to `covered_report_only`,
  not `covered_committed` or `covered_synthetic`.
- The target row must not use `parser_behavior_verified`.
- The target row must not use `diagnostics_only`, `evidence_ledger_only`,
  `local_report_only`, or `external_reference_only`.
- `parser_event_families` for the target row must remain empty.
- `feature_equity_corpus_baseline_v1` must no longer own
  `mythic_edge.workbook_row_coverage` after implementation.
- Blocked-private and blocked-external rows must remain unchanged.
- Zero `partial` rows and zero `missing` rows must not be treated as full
  corpus parity, tracker completion, parser support, workbook truth, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  or coaching truth.
- Repo-side Apps Script parity is not deployed Apps Script behavior.
- Parser-side workbook-facing row coverage is not live workbook behavior.
- Webhook row-shape coverage is not webhook delivery success.
- Schema snapshot coverage is not schema migration approval.

## Error Behavior

If focused corpus validation fails, Codex C must fix only metadata/test issues
inside this contract or route back to Codex B.

If the manifest/session-ledger vocabulary cannot express the approved boundary,
Codex C must stop and route back to Codex B or Codex A.

If implementation would require source-code changes, workbook schema changes,
Apps Script changes, webhook payload changes, live Google Sheets checks, private
evidence, or new coverage vocabulary, Codex C must stop and route back.

If current report rows differ from this contract because upstream work changed
the matrix, Codex C must record the drift explicitly and avoid silent
promotion/demotion of unrelated rows.

## Side Effects

Allowed side effects:

- write the contract artifact;
- later Codex C may write corpus manifest/session-ledger metadata;
- later Codex C may update focused corpus parity tests;
- later Codex C may write implementation handoff and contract-test report docs.

Forbidden side effects:

- code behavior changes;
- source schema changes;
- Apps Script edits;
- live workbook reads or writes;
- webhook calls;
- private smoke runs;
- raw/private artifact creation or commits;
- issue closure;
- tracker completion;
- PR opening in Codex B.

## Dependency Order

Codex C should proceed in this order:

1. Verify live issue, tracker, PR #431, and branch state.
2. Regenerate and inspect the current corpus parity report.
3. Add the dedicated manifest entry.
4. Add the matching session-ledger entry.
5. Remove `mythic_edge.workbook_row_coverage` from
   `feature_equity_corpus_baseline_v1` ownership.
6. Update focused corpus parity tests for the new row, session entry, count
   movement, and unchanged blocked rows.
7. Run validation.
8. Write implementation handoff and contract-test report.

## Compatibility

The implementation must preserve:

- existing manifest schema version;
- existing session ledger schema version;
- existing coverage status vocabulary;
- existing coverage basis vocabulary;
- existing source-kind, privacy-class, and sanitization vocabulary;
- existing corpus report CLI shape;
- existing scenario-family inventory;
- existing parser-side workbook-facing contracts and tests;
- existing repo-side Apps Script parity tests;
- existing `MGTA Start Time` legacy spelling compatibility.

No migration is authorized.

## Tests Required

Minimum Codex C validation:

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_sheet_schema.py tests/test_sheet_exports.py tests/test_event_schema_snapshots.py tests/test_app_models.py tests/test_webhook_payload_schema.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Codex C should also run path-scoped secret and protected-surface checks over
the changed files:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_workbook_row_coverage_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_workbook_row_coverage_residual.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md \
  docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

Focused row inspection must confirm:

- `mythic_edge.workbook_row_coverage`: `covered_report_only`
- `mythic_edge.confidence_finality_degradation`: unchanged
- `manifest.metadata`: unchanged
- private-evidence rows: unchanged
- external-boundary rows: unchanged
- `partial`: 0, if no upstream drift
- overall status: `partial_coverage_map_ready`

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_corpus_workbook_row_coverage_residual.md`.
- The contract identifies the Corpus / Provenance owner and Workbook /
  Transport support boundary.
- The contract authorizes only metadata/test/report implementation.
- The contract defines the exact target row status, entry ID, basis, non-claims,
  and validation evidence.
- The contract keeps live workbook, deployed Apps Script, Google Sheets sync,
  webhook delivery, dashboard truth, analytics truth, AI truth, coaching truth,
  readiness, production behavior, tracker completion, and full corpus parity
  out of scope.
- The contract routes to Codex C.

## Next Workflow Action

Next role: Codex C: Module Implementer

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #432.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/432

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Previous issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/430

  Previous PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/431

  Previous merge commit:
  4c080d5820e34cb5bdd1f4df86350e45ee5b6874

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_workbook_row_coverage_residual.md

  Goal:
  Implement the narrow metadata-only corpus parity residual update for
  mythic_edge.workbook_row_coverage. Promote only this row from count-ratchet
  partial coverage to a dedicated covered_report_only parser-side workbook-row
  boundary entry, if the current repo still matches the contract.

  Expected implementation artifacts:
  - tests/fixtures/parser_corpus/corpus_manifest.v1.json
  - tests/fixtures/parser_corpus/session_ledger.v1.json
  - tests/test_corpus_parity_report.py
  - docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md
  - docs/contract_test_reports/parser_corpus_workbook_row_coverage_residual.md

  Required behavior:
  - Add a dedicated report-only manifest/session-ledger entry for
    mythic_edge.workbook_row_coverage.
  - Use coverage_status covered_report_only.
  - Use coverage_basis fixture_metadata_only.
  - Keep parser_event_families empty for the new row.
  - Do not add parser_behavior_verified.
  - Stop using feature_equity_corpus_baseline_v1 for this target row.
  - Leave confidence/finality/degradation, manifest metadata, private-evidence
    rows, and external-boundary rows unchanged.
  - Keep the report status partial_coverage_map_ready while blocked rows remain.

  Validation:
  - python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
  - python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
  - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
  - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
  - PYTHONPATH=src python3 -m pytest -q tests/test_sheet_schema.py tests/test_sheet_exports.py tests/test_event_schema_snapshots.py tests/test_app_models.py tests/test_webhook_payload_schema.py
  - python3 tools/check_agent_docs.py
  - python3 -m ruff check src tests tools
  - git diff --check

  Do not:
  - Implement parser behavior changes.
  - Change workbook schema, webhook payload shape, Apps Script behavior, Google
    Sheets sync, output transport, parser state final reconciliation, parser
    event classes, router semantics, diagnostics behavior, drift behavior,
    golden replay behavior, feature-equity behavior, evidence-ledger behavior,
    analytics truth, AI truth, coaching behavior, CI gates, merge readiness,
    deploy readiness, production behavior, or final integration policy.
  - Run private app-data, Player.log, live MTGA, Google Sheets, Apps Script,
    webhook, or private smoke checks.
  - Commit private logs, workbook exports, runtime artifacts, generated data,
    SQLite files, secrets, credentials, tokens, API keys, webhook URLs, or
    private reports.
  - Claim full corpus parity, parser support, workbook truth, release
    readiness, production readiness, analytics truth, AI truth, coaching truth,
    tracker completion, or readiness.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/432"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/430"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/431"
  previous_merge_commit: "4c080d5820e34cb5bdd1f4df86350e45ee5b6874"
  completed_thread: "B"
  next_thread: "C"
  verdict: "contract_ready_for_metadata_only_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-parity"
  selected_family: "mythic_edge.workbook_row_coverage"
  contract: "docs/contracts/parser_corpus_workbook_row_coverage_residual.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not mark tracker #158 complete."
    - "Do not claim full corpus parity, parser support, workbook truth, release readiness, production readiness, analytics truth, AI truth, coaching truth, tracker completion, or readiness."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, evidence-ledger behavior, analytics truth, AI truth, coaching behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy."
    - "Do not run or commit private app-data, Player.log, live MTGA, Google Sheets, Apps Script, webhook, or private smoke evidence."
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/432"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/430"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/431"
  previous_merge_commit: "4c080d5820e34cb5bdd1f4df86350e45ee5b6874"
  completed_thread: "B"
  next_thread: "C"
  verdict: "contract_ready_for_metadata_only_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-parity"
  selected_family: "mythic_edge.workbook_row_coverage"
  contract: "docs/contracts/parser_corpus_workbook_row_coverage_residual.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_workbook_row_coverage_residual_comparison.md"
  validation:
    - "Contract writer verified issue #432 open, tracker #158 open, and PR #431 merged into codex/parser-parity at 4c080d5820e34cb5bdd1f4df86350e45ee5b6874."
    - "Contract writer inspected current corpus report, manifest/session ledger, corpus parity implementation/tests, workbook-facing contracts/tests, schema snapshot tests, and adjacent handoff/report artifacts."
    - "Documentation-only contract pass; no behavior validation expected beyond contract file checks."
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not mark tracker #158 complete."
    - "Do not claim full corpus parity, parser support, workbook truth, release readiness, production readiness, analytics truth, AI truth, coaching truth, tracker completion, or readiness."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, evidence-ledger behavior, analytics truth, AI truth, coaching behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy."
    - "Do not run or commit private app-data, Player.log, live MTGA, Google Sheets, Apps Script, webhook, or private smoke evidence."
```
