# Parser Corpus Parity Residual-Gap Readiness Review Contract

## Module

Corpus parity residual-gap/readiness review under tracker #158.

Plain English: this slice lets Mythic Edge review the corpus parity map after
the last `missing` row was removed. It explains the remaining `partial`,
`blocked_private_evidence`, and `blocked_external_boundary` rows without
promoting them, changing parser behavior, running private checks, importing
external corpora, or claiming readiness.

Zero missing rows are useful map-completion evidence. They are not full corpus
parity, tracker completion, parser support, private smoke success, release
readiness, deploy readiness, production readiness, analytics truth, AI truth,
coaching truth, or gameplay advice.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/426
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/424
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/425
- Previous merge commit:
  `b4fcb673a9190740a99efe8260311d3eff5368b9`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-residual-gap-readiness-review`
- base_branch: `codex/parser-parity`
- observed_base_commit: `b4fcb673a9190740a99efe8260311d3eff5368b9`
- target_artifact:
  `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md`
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
- `docs/contracts/parser_corpus_analytics_readiness_labels_coverage.md`
- `docs/contract_test_reports/parser_corpus_analytics_readiness_labels_coverage.md`
- recent parser-corpus contracts, implementation handoffs, and contract-test
  reports under `docs/contracts/`, `docs/implementation_handoffs/`, and
  `docs/contract_test_reports/`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

## Observed Current Behavior

Observed on `codex/parser-parity` at merge commit
`b4fcb673a9190740a99efe8260311d3eff5368b9`:

- Issue #426 is open and tracker #158 remains open.
- Issue #424 / PR #425 moved
  `mythic_edge.analytics_readiness_labels` to `covered_report_only`.
- The corpus parity report returns:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- The report summary is:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 15
  - `partial`: 3
  - `missing`: 0
  - `deferred`: 0
  - `blocked_private_evidence`: 2
  - `blocked_external_boundary`: 5
  - `not_applicable`: 0
- The remaining residual rows are:
  - `manifest.metadata`: `partial`, entry
    `feature_equity_corpus_baseline_v1`, basis `count_ratchet_only`
  - `mythic_edge.confidence_finality_degradation`: `partial`, entry
    `feature_equity_corpus_baseline_v1`, basis `count_ratchet_only`
  - `mythic_edge.workbook_row_coverage`: `partial`, entry
    `feature_equity_corpus_baseline_v1`, basis `count_ratchet_only`
  - `connection.firewall_or_network_drop`: `blocked_private_evidence`,
    entry `firewall_network_drop_private_evidence_boundary_v1`, basis
    `local_report_only`
  - `mythic_edge.private_log_report_only_drift`:
    `blocked_private_evidence`, entry
    `private_log_report_only_drift_private_evidence_boundary_v1`, basis
    `local_report_only`
  - `log_runtime.rotation`: `blocked_external_boundary`, entry
    `external_reference_category_boundary`, basis `external_reference_only`
  - `timer.inactivity_timeout`: `blocked_external_boundary`, entry
    `external_reference_category_boundary`, basis `external_reference_only`
  - `gameplay_stress.conjure`: `blocked_external_boundary`, entry
    `external_reference_category_boundary`, basis `external_reference_only`
  - `gameplay_stress.spellbook`: `blocked_external_boundary`, entry
    `external_reference_category_boundary`, basis `external_reference_only`
  - `drift_debug.recycle_or_rollback`: `blocked_external_boundary`, entry
    `external_reference_category_boundary`, basis `external_reference_only`

## Scope Decision

Implementation may proceed as a docs/report-only residual review.

The review must use this resolution order:

1. Reconcile the non-blocked `partial` rows first. These are committed
   count-ratchet residuals and should be treated as documentation/reporting
   gaps, not private-evidence blockers.
2. Separately plan the `blocked_private_evidence` rows. These require future
   explicit user approval, private-evidence contracts, privacy/redaction
   rules, and local artifact retention rules before promotion.
3. Defer `blocked_external_boundary` rows to a later evidence-generation
   workflow. Public external taxonomy may name these families, but it must not
   be used as Mythic Edge support evidence.

Codex C may create:

- `docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md`
- `docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md`

Codex C must not change:

- corpus manifest statuses;
- session-ledger entries;
- corpus report code;
- parser behavior;
- diagnostics, golden replay, feature-equity, or evidence-ledger behavior;
- workbook, webhook, Apps Script, Google Sheets, output transport, analytics,
  AI, coaching, CI, merge, deploy, production, or tracker lifecycle behavior.

If Codex C finds that the current report differs from this contract, it should
record the mismatch and route back to Codex B or Codex A. It should not repair
the mismatch by silently editing metadata, code, or tests.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns only the review boundary for residual corpus parity statuses.
It consumes the current corpus parity report and produces report-only review
evidence.

## Internal Project Area

Corpus / Provenance, with Quality / Governance as the workflow artifact owner.

This slice is not a parser module, analytics module, release module, deployment
gate, AI module, coaching module, production module, or private smoke run.

## Truth Owner

Truth owner for the current corpus coverage matrix:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for this review package:

- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md`
- `docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md`

Truth boundary:

- Corpus parity metadata owns scenario-family coverage status and review notes.
- Parser modules, router dispatch, parser events, parser state, and final
  reconciliation remain parser-owned truth.
- Private Player.log checks, private smoke outputs, firewall/drop tests, live
  MTGA behavior, app-data checks, network diagnostics, and local runtime
  artifacts remain outside this committed review package.
- Public Manasight metadata remains external reference context only.
- Analytics, workbook, Google Sheets, Apps Script, webhook transport, local app,
  Match Journal, overlay, AI/model-provider behavior, coaching, CI, merge,
  deploy, production, and tracker lifecycle remain downstream or out of scope.

## Bridge-Code Status

`not_bridge_code`

This contract does not authorize bridge code. It authorizes a docs/report-only
review of already committed corpus parity metadata.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`

Codex C artifacts authorized by this contract:

- `docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md`
- `docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md`

Files Codex C may read but must not modify in this slice:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- recent parser-corpus contracts, handoffs, and reports

Not owned by this contract:

- parser modules;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- diagnostics, golden replay, feature-equity, drift, evidence-ledger, or
  analytics implementation behavior;
- corpus manifest or session-ledger status promotions;
- workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, runtime status files, failed posts, workbook exports,
  generated data, or private/local artifacts;
- GitHub Actions, CI policy, merge policy, deploy policy, or tracker
  completion.

## Public Interface

The public interface is the review artifact shape that Codex C must produce.

The review report must include:

- `issue`
- `tracker`
- `contract`
- `base_branch`
- `observed_commit`
- `generated_by`
- `corpus_report_status`
- `summary_counts`
- `resolution_order`
- `residual_rows`
- `truth_boundary`
- `non_claims`
- `recommended_next_action`
- `validation`
- `protected_surface_status`
- `remaining_risks`
- `workflow_handoff`

The report may be a Markdown document. If it embeds structured snippets, they
must be summaries only and must not include raw Player.log data, private local
paths, external corpus contents, private report output, generated database
contents, secrets, tokens, credentials, API keys, webhook URLs, IP/network
traces, decklists, card choices, or private strategy notes.

## Inputs

Allowed inputs:

- Issue #426 problem representation.
- Tracker #158 public GitHub state.
- Current `origin/codex/parser-parity` branch state.
- Committed corpus manifest and session ledger.
- Committed corpus parity report code and tests.
- Committed parser-corpus contracts, implementation handoffs, and contract-test
  reports.
- Generated corpus parity report output from committed safe inputs only.

Forbidden inputs:

- Private Player.log files or excerpts.
- Private app-data.
- Private smoke outputs.
- Firewall/drop, network, or live MTGA checks.
- Generated SQLite databases.
- Runtime status files.
- Failed posts.
- Workbook exports.
- Private reports.
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size lists, capture-date row lists, parser source, or
  external corpus contents.
- Secrets, credentials, tokens, API keys, webhook URLs, IP/network traces,
  decklists, card choices, and private strategy notes.

## Outputs

Expected Codex C implementation handoff:

- path:
  `docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md`
- purpose: compare current branch behavior against this contract, record
  whether the report-only review can be produced without metadata or behavior
  changes, and route the next role.

Expected Codex E-ready review report:

- path:
  `docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md`
- purpose: record report output, residual row reconciliation, validation
  results, protected-surface checks, non-claims, and remaining risks.

These outputs are final review artifacts for the residual-gap slice, not final
parser, release, deploy, production, tracker, analytics, AI, or coaching
authority.

## Residual Row Requirements

The review must preserve each current status unless a future scoped contract
explicitly authorizes a status change.

### Partial Rows

`manifest.metadata`

- Current status: `partial`
- Current basis: `count_ratchet_only`
- Required interpretation: Count-ratchet metadata proves that committed
  corpus counting exists. It does not prove a complete manifest metadata model,
  full corpus parity, or readiness.
- Promotion requirement: a separate manifest metadata enrichment contract with
  explicit schema, fixtures, tests, privacy rules, and non-claims.
- Recommended action in this slice: document as an acceptable residual unless
  the user wants a future metadata-enrichment child issue.

`mythic_edge.confidence_finality_degradation`

- Current status: `partial`
- Current basis: `count_ratchet_only`
- Required interpretation: Count-ratchet evidence notes that Mythic Edge has
  confidence/finality/degradation vocabulary in adjacent contracts. It does not
  prove representative corpus coverage across all parser families.
- Promotion requirement: a separate cross-family confidence/finality/
  degradation corpus contract with committed safe evidence and tests.
- Recommended action in this slice: document as an acceptable residual or
  future optional child issue, not a blocker to the residual review.

`mythic_edge.workbook_row_coverage`

- Current status: `partial`
- Current basis: `count_ratchet_only`
- Required interpretation: Count-ratchet coverage does not prove workbook row
  shape completeness, workbook schema parity, Apps Script behavior, or Google
  Sheets readiness.
- Promotion requirement: a separate workbook-row coverage contract that keeps
  workbook and Apps Script surfaces protected.
- Recommended action in this slice: document as an acceptable residual unless
  a later workbook/transport issue is explicitly opened.

### Blocked Private Evidence Rows

`connection.firewall_or_network_drop`

- Current status: `blocked_private_evidence`
- Current basis: `local_report_only`
- Required interpretation: Adjacent connection error, disconnect, reconnect,
  diagnostics, and synthetic corpus rows do not prove firewall behavior,
  Wi-Fi/drop behavior, network reliability, private smoke success, release
  readiness, analytics truth, AI truth, coaching truth, or production behavior.
- Promotion requirement: explicit user-approved private/live evidence contract,
  privacy/redaction policy, local artifact retention rules, and report-only
  promotion criteria.
- Recommended action in this slice: remain blocked.

`mythic_edge.private_log_report_only_drift`

- Current status: `blocked_private_evidence`
- Current basis: `local_report_only`
- Required interpretation: Committed diagnostics, drift machinery, private-local
  readiness docs, browser smoke plans, evidence-ledger context, golden replay,
  feature-equity, public taxonomy, and corpus metadata do not prove private
  Player.log drift health or private smoke success.
- Promotion requirement: explicit user-approved private drift-report contract
  with redaction, retention, and report-only publication rules.
- Recommended action in this slice: remain blocked.

### Blocked External Boundary Rows

`log_runtime.rotation`

- Current status: `blocked_external_boundary`
- Current basis: `external_reference_only`
- Required interpretation: Public external taxonomy can name log rotation as a
  scenario family. It does not prove Mythic Edge support.
- Promotion requirement: Mythic Edge-owned synthetic or sanitized committed
  evidence, or an approved report-only boundary contract.
- Recommended action in this slice: remain blocked.

`timer.inactivity_timeout`

- Current status: `blocked_external_boundary`
- Current basis: `external_reference_only`
- Required interpretation: Public external taxonomy can name inactivity
  timeout as a scenario family. It does not prove parser, timer, live-client, or
  gameplay behavior.
- Promotion requirement: Mythic Edge-owned safe evidence or a separate
  approval-gated private evidence plan.
- Recommended action in this slice: remain blocked.

`gameplay_stress.conjure`

- Current status: `blocked_external_boundary`
- Current basis: `external_reference_only`
- Required interpretation: Public taxonomy can name conjure as a gameplay
  stress category. It does not prove card creation, hidden-card, decklist,
  analytics, gameplay advice, AI, or parser support.
- Promotion requirement: Mythic Edge-owned sanitized or synthetic evidence that
  preserves hidden-information boundaries.
- Recommended action in this slice: remain blocked.

`gameplay_stress.spellbook`

- Current status: `blocked_external_boundary`
- Current basis: `external_reference_only`
- Required interpretation: Public taxonomy can name spellbook as a gameplay
  stress category. It does not prove option generation, hidden-card, decklist,
  analytics, gameplay advice, AI, or parser support.
- Promotion requirement: Mythic Edge-owned sanitized or synthetic evidence that
  preserves hidden-information boundaries.
- Recommended action in this slice: remain blocked.

`drift_debug.recycle_or_rollback`

- Current status: `blocked_external_boundary`
- Current basis: `external_reference_only`
- Required interpretation: Public taxonomy can name recycle/rollback as a drift
  category. It does not prove Mythic Edge parser support, drift health, private
  log behavior, production behavior, or readiness.
- Promotion requirement: a Mythic Edge-owned evidence model or a safe
  synthetic/fixture plan under a new scoped contract.
- Recommended action in this slice: remain blocked.

## Non-Claims

The residual-gap/readiness review must explicitly state that it does not claim:

- full Mythic Edge corpus parity;
- tracker #158 completion;
- parser support for residual rows;
- parser behavior verification for report-only, private-blocked, or
  external-boundary rows;
- private smoke success;
- live Player.log health;
- firewall/drop, network, or live MTGA behavior;
- release readiness;
- deploy readiness;
- production readiness;
- analytics truth or statistical validity;
- AI truth;
- coaching truth;
- gameplay advice;
- hidden-card inference;
- archetype classification;
- player-mistake labels;
- merge readiness;
- CI gate status beyond commands actually run.

## Invariants

- `missing == 0` must always be described with the residual statuses beside it.
- `partial_coverage_map_ready` must not be shortened to `coverage_map_ready`.
- `partial`, `blocked_private_evidence`, and `blocked_external_boundary` rows
  must remain meaningful residual gaps.
- This slice must not change corpus statuses.
- This slice must not add or commit private, generated, raw, runtime, external,
  or secret artifacts.
- This slice must not run private Player.log, app-data, firewall/drop, network,
  or live MTGA checks.
- This slice must not infer hidden cards, complete decklists, archetypes,
  gameplay advice, player mistakes, AI truth, analytics truth, or coaching
  truth.
- This slice must not close tracker #158 or mark it complete.
- This slice must not target `main`.

## Error Behavior

If Codex C observes a different corpus summary than this contract, it must:

1. record the exact observed summary;
2. record the expected summary from this contract;
3. stop before editing corpus metadata, code, or tests;
4. route to Codex B if the contract needs clarification, or Codex A if the
   problem representation is stale.

If a residual row is missing, renamed, promoted, demoted, or split without a
corresponding contract, Codex C must treat that as review evidence, not as
authorization to adjust the matrix.

If validation requires private/live data, Codex C must stop and record the
blocked condition. It must not run private checks as a workaround.

## Side Effects

Allowed side effects for Codex C:

- write the implementation handoff;
- write the contract-test report;
- run safe local validation commands against committed repo artifacts.

Forbidden side effects:

- source-code edits;
- manifest or session-ledger edits;
- issue closure;
- tracker completion;
- PR creation unless separately requested in a later Codex F pass;
- private/live MTGA checks;
- generated/private/runtime artifact commits;
- external corpus imports;
- CI, merge, deploy, production, workbook, webhook, Apps Script, Google Sheets,
  analytics, AI, or coaching changes.

## Dependency Order

1. Verify `origin/codex/parser-parity` contains
   `b4fcb673a9190740a99efe8260311d3eff5368b9`.
2. Verify issue #426 and tracker #158 are open.
3. Regenerate the corpus parity report from committed manifest and session
   ledger.
4. Compare the current summary and residual rows against this contract.
5. Produce the comparison handoff and contract-test report.
6. Run safe validation.
7. Route to Codex E for review unless a mismatch requires Codex A/B loopback.

## Compatibility

This contract preserves current corpus parity vocabulary:

- `covered_committed`
- `covered_synthetic`
- `covered_report_only`
- `partial`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `missing`
- `deferred`
- `not_applicable`

This contract does not rename or replace existing report status
`partial_coverage_map_ready`.

## Tests Required

Codex C validation should include:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Path-scoped private-marker and protected-surface checks should be run against
the files changed by Codex C:

```bash
printf '%s\n' \
  docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md \
  docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md \
  docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

If Codex C changes only docs, broader parser, analytics, workbook, runtime,
frontend, or CI tests are not required unless local selector output or reviewer
findings justify them.

## Acceptance Criteria

- The contract exists at
  `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`.
- Codex C produces the expected handoff and report artifacts only.
- The report records `partial_coverage_map_ready` with 45 families, 6 committed,
  0 missing, 3 partial, 2 blocked-private, and 5 blocked-external rows.
- The report reconciles all ten residual scenario families named in issue #426.
- The report preserves non-claims around full parity, tracker completion,
  parser support, private smoke, release, deploy, production, analytics, AI,
  and coaching.
- No corpus status, code behavior, protected surface, private artifact, or
  external corpus content changes in this slice.
- Validation evidence is recorded.
- The next role is Codex C unless live repo evidence invalidates the contract.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Codex C should implement the docs/report-only residual review, not code or
metadata behavior changes.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #426.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/426

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Implementation branch:
codex/parser-corpus-residual-gap-readiness-review

Contract:
docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md

Goal:
Produce the docs/report-only residual-gap readiness review artifacts for the
current corpus parity map. Do not change parser behavior, corpus statuses,
corpus manifest entries, session-ledger entries, report code, tests, protected
surfaces, private artifacts, external corpus inputs, or tracker lifecycle.

Expected artifacts:
- docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md
- docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md

Required work:
1. Verify origin/codex/parser-parity contains
   b4fcb673a9190740a99efe8260311d3eff5368b9.
2. Verify issue #426 and tracker #158 are open.
3. Regenerate the corpus parity report from committed manifest and session
   ledger.
4. Confirm the report is partial_coverage_map_ready with 45 families, 6
   committed, 0 missing, 3 partial, 2 blocked-private, and 5 blocked-external
   rows.
5. Reconcile the residual rows in this order without changing their status:
   first partial rows, then approval-gated private-evidence rows, then
   externally-blocked rows deferred to later evidence-generation work.
6. Partial rows:
   - manifest.metadata
   - mythic_edge.confidence_finality_degradation
   - mythic_edge.workbook_row_coverage
7. Blocked private-evidence rows:
   - connection.firewall_or_network_drop
   - mythic_edge.private_log_report_only_drift
8. Blocked external-boundary rows:
   - log_runtime.rotation
   - timer.inactivity_timeout
   - gameplay_stress.conjure
   - gameplay_stress.spellbook
   - drift_debug.recycle_or_rollback
9. State clearly that zero missing rows do not mean full corpus parity, tracker
   completion, parser support, private smoke success, release readiness, deploy
   readiness, production readiness, analytics truth, AI truth, coaching truth,
   gameplay advice, or merge readiness.
10. Run the validation commands from the contract and record results.
11. Route to Codex E for review, or loop back to Codex B/A if the live repo state
   no longer matches the contract.

Do not:
- implement code;
- modify tests;
- edit corpus manifest or session ledger statuses;
- open a PR unless separately asked;
- close issue #426 or tracker #158;
- target main;
- run private Player.log, app-data, firewall/drop, network, or live MTGA checks;
- import or commit Manasight raw logs, compressed corpus files, raw session
  payloads, parser source, or external corpus contents;
- commit private logs, private smoke outputs, generated/runtime artifacts,
  SQLite files, workbook exports, secrets, tokens, credentials, API keys,
  webhook URLs, decklists, card choices, private strategy notes, or private
  reports;
- claim full corpus parity, parser support, private smoke success, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  coaching truth, or tracker completion.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/426"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/424"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/425"
  previous_merge_commit: "b4fcb673a9190740a99efe8260311d3eff5368b9"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_parity_residual_gap_readiness_review_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_parity_residual_gap_readiness_review.md"
  verdict: "contract_ready_for_report_only_residual_gap_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-residual-gap-readiness-review"
  base_branch: "codex/parser-parity"
  selected_path: "report_only_residual_gap_review"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private marker scan for Codex C changed files"
    - "path-scoped protected-surface gate for Codex C changed files"
  stop_conditions:
    - "Do not target main."
    - "Do not close issue #426 or tracker #158."
    - "Do not mark tracker #158 complete."
    - "Do not run private Player.log, app-data, firewall/drop, network, or live MTGA checks."
    - "Do not edit corpus manifest statuses, session-ledger entries, report code, parser behavior, tests, protected surfaces, or tracker lifecycle."
    - "Do not import or commit Manasight raw logs, compressed corpus files, raw session payloads, hash lists, parser source, or external corpus contents."
    - "Do not commit private logs, private smoke outputs, generated/runtime artifacts, SQLite files, workbook exports, secrets, tokens, credentials, API keys, webhook URLs, decklists, card choices, private strategy notes, or private reports."
    - "Do not claim full corpus parity, parser support, private smoke success, release readiness, deploy readiness, production readiness, analytics truth, AI truth, coaching truth, gameplay advice, merge readiness, or tracker completion."
```
