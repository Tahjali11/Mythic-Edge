# Parser Corpus Private Log Report-Only Drift Coverage Contract

## Module

Private log report-only drift corpus evidence boundary for the parser corpus
parity report.

Plain English: this slice lets Mythic Edge account for exactly
`mythic_edge.private_log_report_only_drift` as a private-evidence-blocked
corpus boundary. It records that private/local Player.log drift coverage
requires future user-approved local evidence and must remain report-only. It
does not prove private smoke success, live Player.log health, parser support,
drift health, release readiness, deploy readiness, production behavior,
analytics readiness, analytics truth, AI truth, coaching truth, or full Mythic
Edge corpus parity.

This contract explicitly prevents Mythic Edge from treating parser diagnostics,
log-drift machinery, unknown-entry report references, live diagnostics boundary
coverage, evidence-ledger runtime health, private-local readiness docs, browser
smoke plans, golden replay reports, feature-equity reports, public Manasight
taxonomy metadata, or corpus parity metadata as proof that a private Player.log
drift review was run or passed.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/422
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/420
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/421
- Previous merge commit:
  `9a0a3538eab11dc4db5bc474c793f186d8c21ea5`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-private-log-report-only-drift-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `9a0a3538eab11dc4db5bc474c793f186d8c21ea5`
- target_artifact:
  `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md`
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
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/parser_corpus_live_diagnostics_coverage.md`
- `docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md`
- `docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md`
- `docs/contracts/private_release_e2e_browser_integration_readiness.md`
- `docs/contracts/private_local_v1_package_footprint_release_ref.md`
- `docs/contracts/private_local_v1_scanner_readiness_reconciliation.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/fixtures/player_log_drift_flush_timing_expected.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_diagnostics.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, private Player.log excerpts, private local logs, private smoke
  outputs, private drift reports, generated/private/runtime artifacts, workbook
  exports, SQLite files, credentials, tokens, API keys, webhook URLs,
  IP/network traces, decklists, card choices, private strategy notes, or local
  absolute paths.

## Observed Current Behavior

Observed on `codex/parser-parity` at merge commit
`9a0a3538eab11dc4db5bc474c793f186d8c21ea5`:

- Issue #422 is open and tracker #158 remains open.
- Issue #420 is closed after PR #421 merged live-diagnostics report-only
  boundary coverage.
- The current corpus parity report remains `partial_coverage_map_ready`.
- Current issue #422 report summary:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 14
  - `partial`: 3
  - `missing`: 2
  - `blocked_private_evidence`: 1
  - `blocked_external_boundary`: 5
- `mythic_edge.private_log_report_only_drift` is `missing`, has
  `coverage_basis == ["external_reference_only"]`, and has no Mythic Edge
  entries.
- The remaining missing row is `mythic_edge.analytics_readiness_labels`.
- `mythic_edge.live_diagnostics` is now `covered_report_only`, but that row
  explicitly does not prove private smoke success, live Player.log health,
  watcher correctness, parser support for a live run, release readiness,
  production behavior, analytics readiness, AI/coaching readiness, or full
  corpus parity.
- `log_runtime.unknown_entry` is `covered_report_only` by a committed
  normalized drift report reference. It proves review visibility for unknown
  entries and drift samples, not live private drift health.
- `tests/fixtures/player_log_drift_flush_timing_expected.json` is a committed
  normalized drift report reference for a sanitized fixture path. It is not a
  private local report and does not prove private Player.log drift health.
- `log_drift_sensor.py` can build local drift reports from a supplied log path
  and optional baseline, but this contract does not authorize running it
  against private data.
- Private-local-v1 contracts describe release/scanner/readiness boundaries, but
  they do not supply committed private drift evidence and do not authorize
  corpus parity to publish private reports.
- Current code and tests do not define a committed private drift report
  summary, a user-approved local drift run, private smoke success evidence,
  drift-health assertion, release-readiness gate, deploy-readiness gate,
  production-readiness gate, or analytics/AI readiness claim for this scenario
  family.

## Scope Decision

Implementation may proceed as private-evidence-blocked boundary metadata.

Codex B considered these paths:

1. Keep `mythic_edge.private_log_report_only_drift` as `missing`.
2. Move it to `covered_report_only`.
3. Classify it as `blocked_private_evidence`.
4. Classify it as `deferred`.

Selected path: `blocked_private_evidence` for
`mythic_edge.private_log_report_only_drift` only.

Reasoning:

- The row name and issue scope are specifically about private/local Player.log
  drift review. An honest positive coverage claim would require
  user-approved private-local report evidence that is not committed here.
- Existing repo-owned diagnostics, drift, unknown-entry, live-diagnostics,
  evidence-ledger, golden replay, and feature-equity surfaces prove that Mythic
  Edge has review machinery. They do not prove private drift health or private
  smoke success.
- `covered_report_only` would be too strong unless a later contract authorizes
  a sanitized, non-private, committed summary artifact or a local-private
  evidence ledger that can be referenced without publishing private data.
- `deferred` would be less precise than `blocked_private_evidence`; the blocker
  is not general sequencing, it is the need for approved private/local evidence
  and a publish-safe summary policy.
- Leaving the row `missing` hides an important inspected boundary: Mythic Edge
  has reviewed adjacent drift surfaces and determined they are non-claims for
  private log drift coverage.

This decision changes corpus parity metadata and tests only. It does not change
parser behavior, diagnostics behavior, log-drift behavior, status API behavior,
live app behavior, evidence-ledger behavior, golden replay behavior,
feature-equity behavior, workbook/webhook/App Script surfaces, analytics
behavior, AI/coaching behavior, CI policy, merge policy, deploy policy, or
production behavior.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for
`mythic_edge.private_log_report_only_drift`. Parser diagnostics, log drift,
unknown-entry reports, live diagnostics, evidence-ledger runtime-health
metadata, private-local readiness docs, golden replay, and feature-equity
surfaces own their already contracted behavior. Corpus parity artifacts own
only the coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser Reliability, Local App / Live Player.log Mode,
Player.log Evidence Ledger, and Quality / Governance documentation as context,
but it is not a parser behavior module, diagnostics implementation, drift
detector implementation, private smoke runner, local app module, release gate,
deploy gate, analytics module, AI module, coaching module, or production
module.

## Truth Owner

Truth owner for `mythic_edge.private_log_report_only_drift` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for adjacent behavior referenced only as non-claim context:

- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `docs/contracts/parser_corpus_live_diagnostics_coverage.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `docs/contracts/private_release_e2e_browser_integration_readiness.md`

Truth boundary:

- Parser modules, router dispatch, parser events, parser state, and final
  reconciliation remain parser-owned truth.
- Log-drift reports are local review evidence for one analyzed input, not
  global drift truth.
- Unknown-entry drift references are committed sanitized report references, not
  private Player.log health.
- Live diagnostics coverage is report-only boundary metadata, not live health
  proof.
- Private-local readiness contracts are release/readiness governance, not
  private drift corpus evidence.
- Corpus coverage status is review metadata. It is not parser truth, private
  smoke success, live Player.log health, parser support, drift health,
  workbook truth, analytics truth, AI truth, coaching truth, merge readiness,
  deploy readiness, public/private release readiness, production readiness, or
  tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project areas: Parser Reliability, Local App / Live Player.log Mode,
Player.log Evidence Ledger, and Quality / Governance.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing committed diagnostics/drift/readiness contracts and focused tests
  -> local-private evidence-required corpus manifest metadata
  -> corpus parity coverage row for mythic_edge.private_log_report_only_drift
```

Forbidden reverse flow:

- Corpus coverage status must not change parser, diagnostics, log-drift,
  status API, live app, evidence-ledger, golden replay, feature-equity,
  workbook, webhook, Apps Script, analytics, AI, coaching, release, deploy, or
  production behavior.
- Corpus metadata must not cause local drift labels to become parser facts,
  private smoke success, live Player.log health, parser support, drift health,
  release readiness, deploy readiness, production readiness, analytics
  readiness, AI prompts, gameplay advice, or tracker-completion authority.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- match/game identity
- deduplication
- diagnostics report shape
- drift report behavior
- status API behavior
- live app watcher behavior
- live capture behavior
- runtime status schema
- evidence-ledger behavior
- golden replay behavior
- feature-equity behavior
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- delivery retry artifacts
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

- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md`

Files Codex C may inspect but must not change unless a separate contract
explicitly authorizes it:

- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/fixtures/player_log_drift_flush_timing_expected.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- focused parser diagnostics, drift, and diagnostics-runtime tests

## Public Interface

This contract adds no runtime public API.

The public artifact is the corpus parity compatibility report generated from
the committed corpus manifest.

Expected corpus report effect:

- `mythic_edge.private_log_report_only_drift` changes from `missing` to
  `blocked_private_evidence`.
- The row uses no parser event families.
- The row uses no committed private report artifact.
- The row carries an explicit note that private-log drift coverage requires
  future approved private/local report evidence.
- The row does not add a session-ledger entry in this slice because no
  committed session or private report summary exists.
- Remaining rows must stay separately scoped:
  - `mythic_edge.analytics_readiness_labels`
  - `mythic_edge.live_diagnostics`
  - `mythic_edge.confidence_finality_degradation`
  - `mythic_edge.workbook_row_coverage`

## Required Corpus Manifest Entry

Codex C should add exactly one Mythic Edge entry for
`mythic_edge.private_log_report_only_drift`.

Recommended manifest entry values:

- `entry_id`: `private_log_report_only_drift_private_evidence_boundary_v1`
- `entry_type`: `local_private_report_summary`
- `source_kind`: `local_private_report_only`
- `commit_status`: `local_report_only`
- `privacy_class`: `local_private_not_committed`
- `sanitization_status`: `requires_review`
- `scenario_families`: `["mythic_edge.private_log_report_only_drift"]`
- `coverage_status`: `blocked_private_evidence`
- `coverage_basis`: `["local_report_only"]`
- `parser_event_families`: `[]`
- `external_reference_status`: `reference_category_not_checked`
- `paths`: `{}`

Required `parser_claim_families`:

- `private_log_drift_private_evidence_required`
- `committed_drift_references_non_claim`
- `live_diagnostics_non_claim`
- `private_local_readiness_non_claim`
- `analytics_readiness_non_claim`
- `private_artifact_boundary`

Required notes must state that the row is blocked by future approved
private/local evidence and is not evidence of:

- private smoke success;
- live Player.log health;
- parser support;
- drift health;
- release readiness;
- deploy readiness;
- production behavior;
- analytics readiness;
- analytics truth;
- AI/coaching readiness or truth;
- full Mythic Edge corpus parity.

## Required Session Ledger Policy

Codex C must not add a session-ledger entry for this slice.

Reasoning:

- A session-ledger entry would imply a committed reviewed session or report
  summary.
- This contract does not authorize running private local checks, reading
  private Player.log data, or committing private report summaries.
- The manifest boundary entry is enough to move the row from uninspected
  `missing` to inspected `blocked_private_evidence`.

A later contract may authorize a local-only report summary or sanitized
non-private session reference after user approval and privacy review.

## Required Guarantees

The future implementation must guarantee:

- Only `mythic_edge.private_log_report_only_drift` changes coverage status in
  this slice.
- `mythic_edge.private_log_report_only_drift` becomes
  `blocked_private_evidence`.
- `coverage_basis` is exactly `["local_report_only"]`.
- No `covered_report_only`, `covered_synthetic`, or `covered_committed` status
  is used for this row.
- No `parser_behavior_verified`, `diagnostics_only`, `fixture_metadata_only`,
  or `evidence_ledger_only` basis is added for this row.
- No session-ledger entry is added.
- No private local report, raw Player.log, private smoke output, generated
  runtime artifact, SQLite database, workbook export, secret, token,
  credential, API key, webhook URL, IP/network trace, decklist, private
  strategy note, or local absolute path is committed.
- Existing diagnostics/drift tests may be cited as adjacent non-claim evidence,
  but diagnostics and drift implementation must remain unchanged.
- Adjacent rows, including `mythic_edge.analytics_readiness_labels` and
  `mythic_edge.live_diagnostics`, remain out of scope.

## Unknowns

- Whether a later private-local workflow should produce a user-approved
  local-only drift report summary remains outside this slice.
- Whether a future report summary can be sanitized enough for committed
  metadata requires a separate privacy and fixture-acceptance contract.
- Whether analytics readiness labels should become report-only corpus metadata
  remains outside this slice.
- Whether private browser smoke evidence should feed corpus parity remains
  outside this slice.

## Suspected Gaps

- Current corpus parity metadata can identify the private evidence requirement,
  but cannot prove actual private drift health.
- Existing drift reports include useful local report machinery, but they write
  local-only report artifacts and include source-path information before
  normalization; those artifacts must not be committed as evidence here.
- A future safe private report flow likely needs a redacted summary shape,
  explicit retention rules, and user approval before it can support stronger
  coverage.

## Validation Expectations

Required Codex C validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md \
  docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md \
  docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Recommended supporting validation if Codex C cites adjacent diagnostics or
drift behavior:

```bash
PYTHONPATH=src python3 -m pytest -q \
  tests/test_parser_diagnostics_mode.py \
  tests/test_log_drift_sensor.py \
  tests/test_diagnostics.py
```

Codex E should verify:

- The row moved only to `blocked_private_evidence`.
- The implementation did not add `covered_report_only` or
  `parser_behavior_verified`.
- The implementation did not add a session-ledger entry.
- The implementation did not add a private local report artifact or fixture.
- The implementation did not change diagnostics, drift, status API, parser,
  runtime, workbook, webhook, Apps Script, analytics, AI, or production code.
- The report notes preserve all non-claims.

## Codex C Handoff

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #422.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/422

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md

Goal:
Implement the private-evidence-blocked corpus parity metadata boundary for
mythic_edge.private_log_report_only_drift exactly as contracted. This is corpus
metadata and test work only. It must not change parser behavior, diagnostics
behavior, log-drift behavior, status API behavior, live app behavior,
evidence-ledger behavior, workbook/webhook/App Script behavior, analytics
truth, AI truth, coaching truth, release readiness, deploy readiness, or
production behavior.

Do:
- Refresh live GitHub and local git state.
- Verify origin/codex/parser-parity includes
  9a0a3538eab11dc4db5bc474c793f186d8c21ea5.
- Compare current corpus manifest/tests against the contract before editing.
- Change only the corpus manifest, focused corpus parity tests,
  implementation handoff, and contract test report as needed.
- Move only mythic_edge.private_log_report_only_drift from missing to
  blocked_private_evidence.
- Use coverage_basis exactly ["local_report_only"].
- Do not add a session-ledger entry.
- Preserve private-smoke, live Player.log health, parser-support,
  drift-health, release-readiness, deploy-readiness, production, analytics, AI,
  coaching, and full-parity non-claims.
- Produce docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md.
- Produce docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md.

Do not:
- Target main.
- Close tracker #158.
- Run actual private app-data checks or Player.log checks.
- Claim private smoke success, live Player.log health, parser support, drift
  health, release readiness, deploy readiness, production behavior, analytics
  readiness, analytics truth, AI truth, coaching truth, or full corpus parity.
- Add covered_report_only, parser_behavior_verified, diagnostics_only,
  fixture_metadata_only, evidence_ledger_only, private report artifacts,
  session-ledger entries, parser event families, committed logs, generated
  artifacts, SQLite files, workbook exports, secrets, tokens, API keys, webhook
  URLs, private report contents, IP/network traces, decklists, private strategy
  notes, or local absolute paths.
- Change parser behavior, parser state final reconciliation, parser event
  classes, router semantics, diagnostics behavior, log-drift behavior, status
  API behavior, live app behavior, evidence-ledger behavior, golden replay
  behavior, feature-equity behavior, workbook schema, webhook payload shape,
  Apps Script behavior, Google Sheets sync, output transport, analytics
  behavior, AI/model-provider behavior, CI policy, merge policy, deploy policy,
  or production behavior.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- python3 tools/check_secret_patterns.py with changed paths
- python3 tools/check_protected_surfaces.py with changed paths
- python3 -m ruff check src tests tools
- git diff --check
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/422"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/420"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/421"
  previous_merge_commit: "9a0a3538eab11dc4db5bc474c793f186d8c21ea5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md"
  verdict: "contract_ready_for_private_evidence_blocked_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-private-log-report-only-drift-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "blocked_private_evidence"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 tools/check_secret_patterns.py with changed paths"
    - "python3 tools/check_protected_surfaces.py with changed paths"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not run actual private app-data checks or Player.log checks."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim private smoke success, live Player.log health, parser support, drift health, release readiness, deploy readiness, production behavior, analytics readiness, analytics truth, AI truth, or coaching truth."
    - "Do not add covered_report_only, parser_behavior_verified, diagnostics_only, fixture_metadata_only, evidence_ledger_only, private report artifacts, session-ledger entries, parser event families, committed logs, generated/private/runtime artifacts, SQLite files, workbook exports, secrets, tokens, API keys, webhook URLs, private report contents, IP/network traces, decklists, private strategy notes, or local absolute paths."
    - "Do not change parser behavior or protected parser/runtime/diagnostics/drift/status/local-app/workbook/webhook/App Script/analytics/AI/production surfaces."
```
