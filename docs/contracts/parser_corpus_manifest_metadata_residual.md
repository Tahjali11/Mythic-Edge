# Parser Corpus Manifest Metadata Residual Contract

## Module

Manifest metadata residual coverage boundary for the parser corpus parity
report.

Plain English: this slice lets Mythic Edge resolve the `manifest.metadata`
residual by proving only that the committed corpus manifest has an explicit,
validated, privacy-safe metadata boundary. It does not prove parser behavior,
fixture adequacy, session-ledger completeness, full corpus parity, tracker
completion, release readiness, analytics truth, AI truth, or coaching truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/428
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/426
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/427
- Previous merge commit:
  `376e95bdc5647a7ac5bd14af2c15e543cfd180c6`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-manifest-metadata-residual`
- base_branch: `codex/parser-parity`
- observed_base_commit: `376e95bdc5647a7ac5bd14af2c15e543cfd180c6`
- target_artifact:
  `docs/contracts/parser_corpus_manifest_metadata_residual.md`
- issue_body_alternate_artifact:
  `docs/contracts/parser_corpus_manifest_metadata_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md`
- risk_tier: High
- status: contract only

Naming decision: the current user prompt names
`docs/contracts/parser_corpus_manifest_metadata_residual.md`, while the issue
body names `docs/contracts/parser_corpus_manifest_metadata_coverage.md`. This
contract follows the current user prompt. Codex C should use the `residual`
prefix for its handoff and report unless the user explicitly redirects.

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md`
- `docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

## Observed Current Behavior

Observed on `codex/parser-parity` at merge commit
`376e95bdc5647a7ac5bd14af2c15e543cfd180c6`:

- Issue #428 is open and tracker #158 remains open.
- PR #427 completed the residual-gap readiness review for issue #426.
- The current report remains `partial_coverage_map_ready`.
- The report summary is:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 15
  - `partial`: 3
  - `missing`: 0
  - `blocked_private_evidence`: 2
  - `blocked_external_boundary`: 5
- `manifest.metadata` is currently:
  - `coverage_status`: `partial`
  - `coverage_basis`: `count_ratchet_only`
  - `mythic_edge_entries`: `feature_equity_corpus_baseline_v1`
- `feature_equity_corpus_baseline_v1` also covers:
  - `mythic_edge.confidence_finality_degradation`
  - `mythic_edge.workbook_row_coverage`
  - `drift_debug.gsm_truncation`
- `session.ledger_metadata` is already `covered_committed` by
  `parser_corpus_session_ledger_v1` with basis `fixture_metadata_only`.
- The corpus manifest validates the current manifest object, schema version,
  corpus id, source privacy flags, taxonomy family list, entry identifiers,
  entry vocabulary, coverage basis values, and forbidden private/raw/external
  content markers.
- The session ledger validates separately. It does not by itself prove the
  `manifest.metadata` row.

## Scope Decision

Selected path: promote only `manifest.metadata` from `partial` to
`covered_report_only`.

Reasoning:

- `manifest.metadata` is a repo-owned corpus/provenance metadata row, not a
  parser behavior row and not a private-evidence row.
- The committed manifest already has machine-readable object, schema,
  taxonomy, entry, vocabulary, source-privacy, and forbidden-content checks.
- A dedicated manifest metadata boundary entry can safely prove that Mythic
  Edge has an explicit committed manifest metadata model.
- `covered_committed` would overstate the result because this row proves a
  metadata boundary, not committed parser behavior or fixture adequacy.
- Keeping `partial` would preserve a residual that this slice can safely
  resolve without private evidence, external corpus imports, or behavior
  changes.

Codex C may update:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md`
- `docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md`

Codex C must not update:

- `tests/fixtures/parser_corpus/session_ledger.v1.json`, unless a reviewer
  later requires a contract loopback for session-ledger symmetry;
- `src/mythic_edge_parser/app/corpus_parity_report.py`, unless current code
  cannot represent the contracted manifest entry without a new vocabulary
  value;
- any parser, runtime, workbook, webhook, Apps Script, analytics, AI, coaching,
  CI, merge, deploy, production, private-artifact, or external-corpus surface.

If current corpus parity code cannot express the selected path using existing
vocabulary, Codex C must route back to Codex B instead of adding a new enum or
schema field.

## Owning Layer

Owning layer: Corpus / Provenance / Governance.

This contract owns only the `manifest.metadata` corpus coverage boundary. It
does not own parser truth, parser behavior, parser correctness, live MTGA
behavior, private evidence, external corpus contents, analytics truth, AI
truth, coaching truth, release readiness, deploy readiness, production
readiness, or tracker completion.

## Internal Project Area

Corpus / Provenance.

Quality / Governance owns the contract, handoff, and contract-test report
artifacts. This slice is not bridge code.

## Truth Owner

Truth owner for the corpus manifest metadata row:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Supporting reference only:

- `tests/fixtures/parser_corpus/session_ledger.v1.json`

Truth boundary:

- The corpus manifest owns corpus metadata about scenario families, entries,
  source privacy, coverage status, coverage basis, known gaps, review notes,
  linked issues, contracts, and safe repo paths.
- Parser modules, router dispatch, parser events, parser state, match/game
  identity, deduplication, and final reconciliation remain parser-owned truth.
- Workbook, webhook, Apps Script, Google Sheets, output transport, local app,
  Match Journal, overlay, analytics, AI/model-provider behavior, coaching,
  CI, merge, deploy, production, and tracker lifecycle remain downstream or
  out of scope.
- Public Manasight metadata remains external reference context only.

## Bridge-Code Status

`not_bridge_code`

This is a committed corpus metadata boundary. It does not move data between
internal project areas and does not authorize bridge code.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_manifest_metadata_residual.md`

Future implementation artifacts authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md`
- `docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md`

Read-only context:

- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- recent parser-corpus contracts, handoffs, and reports

Not owned by this contract:

- parser modules;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- diagnostics, drift, golden replay, feature-equity, evidence-ledger, or
  analytics behavior;
- session-ledger semantics;
- private/local artifacts;
- external corpus contents;
- workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, runtime status files, failed posts, workbook exports,
  CI gates, merge readiness, deploy readiness, production behavior, or tracker
  lifecycle.

## Public Interface

The public interface is the corpus parity row for `manifest.metadata`.

After implementation, the generated corpus parity report must show:

```text
scenario_family: manifest.metadata
coverage_status: covered_report_only
coverage_basis: ["fixture_metadata_only"]
mythic_edge_entries: ["parser_corpus_manifest_metadata_boundary_v1"]
```

The entry id must be:

```text
parser_corpus_manifest_metadata_boundary_v1
```

The entry should use only existing corpus manifest vocabulary:

- `entry_type`: `session_ledger_entry`
- `source_kind`: `committed_count_only_report`
- `commit_status`: `committed`
- `privacy_class`: `committed_count_only`
- `sanitization_status`: `not_applicable_count_only`
- `coverage_status`: `covered_report_only`
- `coverage_basis`: `["fixture_metadata_only"]`
- `parser_event_families`: `[]`
- `scenario_families`: `["manifest.metadata"]`

The `entry_type` value `session_ledger_entry` is reused here only because it is
the existing non-parser metadata entry vocabulary. It does not mean the session
ledger owns manifest metadata truth.

Recommended `parser_claim_families`:

- `corpus_manifest_metadata_boundary`
- `manifest_schema_v1`
- `taxonomy_family_inventory`
- `source_privacy_flags`
- `manifest_entry_vocabulary`
- `private_artifact_non_claim`

Required `known_gaps` and `review_notes` must state that this row does not
prove:

- parser behavior;
- parser support;
- complete fixture adequacy;
- session-ledger completeness;
- full corpus parity;
- tracker completion;
- readiness;
- private smoke success;
- analytics truth;
- AI truth;
- coaching truth.

## Inputs

Allowed inputs:

- Issue #428 problem representation.
- Tracker #158 public GitHub state.
- Current `origin/codex/parser-parity` branch state.
- Existing committed corpus manifest and session ledger.
- Existing corpus parity report code and focused tests.
- Existing issue #426 contract, handoff, and report.
- Existing parser-corpus contracts, handoffs, and reports.

Forbidden inputs:

- private app-data;
- private Player.log files or excerpts;
- private smoke outputs;
- firewall/drop, network, live MTGA, or private smoke checks;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size lists, capture-date row lists, parser source,
  or external corpus contents;
- generated SQLite databases;
- runtime status files;
- failed posts;
- workbook exports;
- private reports;
- secrets, credentials, tokens, API keys, webhook URLs, IP/network traces,
  decklists, card choices, or private strategy notes.

## Outputs

Expected Codex C implementation handoff:

- path:
  `docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md`
- purpose: compare current `manifest.metadata` behavior to this contract,
  describe the manifest/test changes made, record validation, and route to
  Codex E.

Expected Codex E-ready report:

- path:
  `docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md`
- purpose: record row status, matrix counts, non-claims, validation, and
  protected-surface status.

Expected report-count change after Codex C:

- `covered_report_only`: increases from 15 to 16
- `partial`: decreases from 3 to 2
- `missing`: remains 0
- `blocked_private_evidence`: remains 2
- `blocked_external_boundary`: remains 5
- `covered_committed`: remains 6
- `covered_synthetic`: remains 14
- overall report status remains `partial_coverage_map_ready`

Rows that must remain unchanged:

- `mythic_edge.confidence_finality_degradation`
- `mythic_edge.workbook_row_coverage`
- `connection.firewall_or_network_drop`
- `mythic_edge.private_log_report_only_drift`
- `log_runtime.rotation`
- `timer.inactivity_timeout`
- `gameplay_stress.conjure`
- `gameplay_stress.spellbook`
- `drift_debug.recycle_or_rollback`

## Invariants

- Only `manifest.metadata` may change status in this slice.
- `manifest.metadata` must move only to `covered_report_only`, not
  `covered_committed` or `covered_synthetic`.
- `manifest.metadata` must use `fixture_metadata_only` only.
- `manifest.metadata` must not use `parser_behavior_verified`,
  `count_ratchet_only`, `diagnostics_only`, `evidence_ledger_only`,
  `local_report_only`, or `external_reference_only` after implementation.
- `feature_equity_corpus_baseline_v1` must no longer be the entry that gives
  `manifest.metadata` its family coverage status. It may continue to cover
  other rows under its existing contract.
- No private, generated, raw, runtime, external, or secret artifact may be
  added.
- No private or live checks may be run.
- Tracker #158 must remain open.
- The implementation branch must not target `main`.

## Error Behavior

If Codex C cannot represent the selected path using existing vocabulary, it
must route back to Codex B. It must not add new enum values, schema fields,
or code behavior silently.

If changing `manifest.metadata` would require changing session-ledger semantics,
Codex C must route back to Codex B.

If the generated report does not show the expected count change, Codex C must
record the mismatch and stop before widening scope.

If validation requires private/live/external corpus inputs, Codex C must stop
and record the blocked condition.

## Side Effects

Allowed side effects for Codex C:

- edit the corpus manifest entry metadata for `manifest.metadata`;
- update focused corpus parity tests;
- write the implementation handoff;
- write the contract-test report;
- run safe local validation commands.

Forbidden side effects:

- parser behavior changes;
- source parser code changes;
- session-ledger edits unless routed through a contract loopback;
- private/live checks;
- generated/private/runtime artifact commits;
- external corpus imports;
- issue closure;
- tracker completion;
- PR creation unless separately requested in Codex F;
- CI, merge, deploy, production, workbook, webhook, Apps Script, Google
  Sheets, analytics, AI, or coaching changes.

## Dependency Order

1. Verify `origin/codex/parser-parity` contains
   `376e95bdc5647a7ac5bd14af2c15e543cfd180c6`.
2. Verify issue #428 and tracker #158 are open.
3. Generate the current corpus parity report.
4. Add the dedicated `parser_corpus_manifest_metadata_boundary_v1` manifest
   entry using existing vocabulary.
5. Remove `manifest.metadata` from the `feature_equity_corpus_baseline_v1`
   scenario-family list so the new entry owns that row's status.
6. Update focused corpus parity tests for the row status, basis, entry id,
   counts, and non-claims.
7. Generate the updated corpus parity report.
8. Write the implementation handoff and contract-test report.
9. Run validation and route to Codex E.

## Compatibility

This contract preserves:

- `parser_corpus_manifest.v1`
- `parser_corpus_session_ledger.v1`
- `parser_corpus_compatibility_report.v1`
- current coverage status vocabulary
- current coverage basis vocabulary
- current privacy and protected-surface report sections
- current report status `partial_coverage_map_ready`

This contract does not rename the scenario family `manifest.metadata`.

## Tests Required

Codex C validation should include:

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Path-scoped private-marker and protected-surface checks should be run against
the files changed by Codex C.

## Acceptance Criteria

- The contract exists at
  `docs/contracts/parser_corpus_manifest_metadata_residual.md`.
- `manifest.metadata` is contracted to move from `partial` to
  `covered_report_only`.
- The selected coverage basis is exactly `["fixture_metadata_only"]`.
- The selected entry id is exactly
  `parser_corpus_manifest_metadata_boundary_v1`.
- No other residual row changes status in this slice.
- The updated report remains `partial_coverage_map_ready`.
- The updated report has 45 total families, 6 committed, 14 synthetic, 16
  report-only, 2 partial, 2 blocked-private, 5 blocked-external, and 0
  missing rows.
- The implementation records non-claims around full corpus parity, tracker
  completion, parser support, readiness, private smoke, analytics truth, AI
  truth, and coaching truth.
- No protected surfaces or forbidden artifacts are changed.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #428.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/428

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/426

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/427

Previous merge commit:
376e95bdc5647a7ac5bd14af2c15e543cfd180c6

Base branch:
codex/parser-parity

Implementation branch:
codex/parser-corpus-manifest-metadata-residual

Contract:
docs/contracts/parser_corpus_manifest_metadata_residual.md

Goal:
Implement the narrow manifest.metadata residual coverage boundary. Promote only
manifest.metadata from partial to covered_report_only by adding a dedicated
manifest metadata boundary entry and focused tests. Do not change parser
behavior, session-ledger semantics, private evidence, external corpus inputs,
or protected surfaces.

Required work:
1. Verify origin/codex/parser-parity contains
   376e95bdc5647a7ac5bd14af2c15e543cfd180c6.
2. Verify issue #428 and tracker #158 are open.
3. Inspect the contract and current corpus report.
4. Add manifest entry parser_corpus_manifest_metadata_boundary_v1 using
   existing corpus manifest vocabulary.
5. Move manifest.metadata coverage ownership off
   feature_equity_corpus_baseline_v1 so the row reports:
   - coverage_status: covered_report_only
   - coverage_basis: ["fixture_metadata_only"]
   - mythic_edge_entries: ["parser_corpus_manifest_metadata_boundary_v1"]
6. Preserve all other residual rows and statuses.
7. Update focused corpus parity tests.
8. Write:
   - docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md
   - docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md
9. Run validation from the contract and record results.
10. Route to Codex E.

Do not:
- target main;
- close tracker #158;
- mark tracker #158 complete;
- claim full corpus parity, readiness, parser support, analytics truth, AI
  truth, or coaching truth;
- run private Player.log, app-data, firewall/drop, network, live MTGA, or
  private smoke checks;
- import or commit external corpus contents or Manasight raw logs;
- commit private/generated/runtime artifacts, secrets, workbook exports,
  decklists, card choices, or private reports;
- change parser behavior, parser state final reconciliation, parser event
  classes, router semantics, diagnostics behavior, drift behavior, golden
  replay behavior, feature-equity behavior, evidence-ledger behavior,
  match/game identity, deduplication, workbook schema, webhook payload shape,
  Apps Script behavior, Google Sheets sync, output transport, analytics truth,
  AI/model-provider behavior, coaching behavior, CI gates, merge readiness,
  deploy readiness, production behavior, or final integration policy.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/428"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/426"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/427"
  previous_merge_commit: "376e95bdc5647a7ac5bd14af2c15e543cfd180c6"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_manifest_metadata_residual.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_manifest_metadata_residual_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_manifest_metadata_residual.md"
  verdict: "contract_ready_for_manifest_metadata_report_only_promotion"
  risk_tier: "High"
  branch: "codex/parser-corpus-manifest-metadata-residual"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null"
    - "python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not mark tracker #158 complete."
    - "Do not claim full corpus parity, readiness, parser support, analytics truth, AI truth, or coaching truth."
    - "Do not run private Player.log, app-data, firewall/drop, network, live MTGA, or private smoke checks."
    - "Do not import or commit Manasight raw logs, compressed corpus files, parser source, external corpus contents, private logs, generated/runtime artifacts, workbook exports, secrets, tokens, API keys, webhook URLs, decklists, card choices, or private reports."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics behavior, drift behavior, golden replay behavior, feature-equity behavior, evidence-ledger behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy."
```
