# Parser Corpus Live Diagnostics Coverage Contract

## Module

Live diagnostics corpus evidence boundary for the parser corpus parity report.

Plain English: this slice lets Mythic Edge account for exactly
`mythic_edge.live_diagnostics` as report-only boundary metadata. It proves only
that committed Mythic Edge diagnostics and status contracts have a safe,
reviewed non-claim boundary for live-diagnostics coverage. It does not prove
private smoke success, live Player.log health, watcher correctness, parser
support, release readiness, production behavior, analytics truth, AI truth,
coaching truth, or full Mythic Edge corpus parity.

This contract explicitly prevents Mythic Edge from treating parser diagnostics,
local app watcher diagnostics, live-capture heartbeat/no-row diagnostics,
evidence runtime status, status API exposure, unknown-entry routing,
log-drift reports, runtime status summaries, corpus parity metadata, private
operator notes, or future browser smoke reports as live Player.log truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/420
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/418
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/419
- Previous merge commit:
  `5180de4b5900dc4bfd895d394d1a5ac74994c4b4`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-live-diagnostics-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `5180de4b5900dc4bfd895d394d1a5ac74994c4b4`
- target_artifact:
  `docs/contracts/parser_corpus_live_diagnostics_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md`
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
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contract_test_reports/parser_diagnostics_mode.md`
- `docs/implementation_handoffs/parser_diagnostics_mode_comparison.md`
- `docs/contracts/live_app_watcher_diagnostics.md`
- `docs/contract_test_reports/live_app_watcher_diagnostics.md`
- `docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md`
- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md`
- `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md`
- `docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- focused parser diagnostics, local app watcher diagnostics, drift,
  evidence-runtime-status, and status API tests when Codex C needs supporting
  behavior evidence

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, private Player.log excerpts, private local logs, private smoke
  outputs, generated/private/runtime artifacts, workbook exports, SQLite files,
  credentials, tokens, API keys, webhook URLs, IP/network traces, decklists,
  card choices, private strategy notes, or private reports.

## Observed Current Behavior

Observed on `codex/parser-parity` at merge commit
`5180de4b5900dc4bfd895d394d1a5ac74994c4b4`:

- Issue #420 is open and tracker #158 remains open.
- Issue #418 is closed after PR #419 merged phantom/deck-origin report-only
  boundary coverage.
- The current corpus parity report remains `partial_coverage_map_ready`.
- Current issue #420 report summary:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 13
  - `partial`: 3
  - `missing`: 3
  - `blocked_private_evidence`: 1
  - `blocked_external_boundary`: 5
- `mythic_edge.live_diagnostics` is `missing`, has
  `coverage_basis == ["external_reference_only"]`, and has no Mythic Edge
  entries.
- Remaining missing rows also include:
  - `mythic_edge.private_log_report_only_drift`
  - `mythic_edge.analytics_readiness_labels`
- `parser_diagnostics.py` can build a local diagnostics report from a supplied
  source log, optional runtime status, optional drift baseline, and optional
  evidence-ledger review summary. Its report separates parser health,
  event-family coverage, truncation/data-loss evidence, unknown/degradation
  evidence, final reconciliation, transport health, and workbook/App Script
  non-checks.
- `live_watcher_diagnostics.py` composes local app status into read-only
  diagnostics with explicit capability flags: it does not start or stop the
  watcher, tail Player.log, write SQLite, write diagnostics files, or allow
  external transport.
- The live-capture heartbeat/no-row diagnostics contract permits local app
  progress and heartbeat labels for a running capture session, but those labels
  are app-owned operational metadata and do not prove game truth.
- The evidence-ledger runtime status exposure contract permits only a
  summary-only local status field for evidence-ledger review health. It
  explicitly does not make runtime status parser truth, live Arena drift proof,
  merge readiness, deploy readiness, workbook truth, analytics truth, or AI
  truth.
- Unknown-entry and evidence-ledger provenance corpus rows already show that
  diagnostics or evidence-ledger coverage can be represented as report-only
  metadata without claiming parser support.
- Current code and tests do not define a committed live Player.log fixture,
  private-smoke fixture, watcher-correctness fixture, live-health assertion,
  release-readiness gate, production-readiness gate, or analytics/AI readiness
  claim for this scenario family.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Keep `mythic_edge.live_diagnostics` as `missing`.
2. Move it to `covered_report_only`.
3. Classify it as `blocked_private_evidence`, `blocked_external_boundary`, or
   `deferred`.
4. Add synthetic or committed fixture coverage.

Selected path: `covered_report_only` for `mythic_edge.live_diagnostics` only.

Reasoning:

- Mythic Edge already has committed diagnostics, watcher diagnostics,
  live-capture status, evidence-runtime-status, log-drift, and status API
  contracts and tests that define safe local review surfaces.
- Those surfaces are useful enough to record a non-claim boundary in corpus
  parity. They answer "what kind of review surface exists?" not "did a live
  private run succeed?"
- `covered_synthetic` is not appropriate because no synthetic live game,
  watcher, tailer, private Player.log, or browser smoke fixture is authorized
  here.
- `blocked_private_evidence` is too strong for this row because V1 can cover
  the repo-owned report boundary without committing private logs or private
  smoke results.
- Leaving the row `missing` hides a useful distinction: the project has
  committed live-diagnostics review surfaces, but those surfaces deliberately
  do not claim live health or production readiness.

This decision changes corpus parity metadata and tests only. It does not change
parser behavior, diagnostics behavior, watcher behavior, live-capture behavior,
status API behavior, evidence-runtime-status behavior, log-drift behavior,
golden replay behavior, feature-equity behavior, workbook/webhook/App Script
surfaces, analytics behavior, AI/coaching behavior, CI policy, merge policy,
deploy policy, or production behavior.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for
`mythic_edge.live_diagnostics`. Parser diagnostics, app diagnostics,
log-drift, status API, evidence runtime status, live watcher diagnostics, and
live capture status own their already contracted report/status behaviors.
Corpus parity artifacts own only the coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser Reliability, Local App / Live Player.log Mode, and
Player.log Evidence Ledger documentation as context, but it is not a parser
behavior module, live watcher module, diagnostics implementation, status API
implementation, local app module, analytics module, AI module, coaching module,
release-readiness module, deploy-readiness module, or production module.

## Truth Owner

Truth owner for `mythic_edge.live_diagnostics` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for adjacent behavior referenced only as non-claim context:

- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`

Truth boundary:

- Parser modules, router dispatch, parser events, parser state, and final
  reconciliation remain parser-owned truth.
- Parser diagnostics reports are local review evidence, not a second parser.
- Local app watcher diagnostics are read-only status composition, not watcher
  correctness proof.
- Live-capture heartbeat/no-row labels are operational progress metadata, not
  parser truth or game truth.
- Evidence runtime status is summary-only local review metadata, not live Arena
  drift proof.
- Corpus coverage status is review metadata. It is not parser truth,
  diagnostics readiness, private smoke success, live Player.log health,
  workbook truth, analytics truth, AI truth, coaching truth, merge readiness,
  deploy readiness, public/private release readiness, production readiness, or
  tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project areas: Parser Reliability, Local App / Live Player.log Mode,
and Player.log Evidence Ledger.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing committed diagnostics/status contracts and focused tests
  -> bounded committed report-only corpus manifest/session-ledger metadata
  -> corpus parity coverage row for mythic_edge.live_diagnostics
```

Forbidden reverse flow:

- Corpus coverage status must not change parser, diagnostics, watcher,
  live-capture, evidence runtime status, status API, log-drift, golden replay,
  feature-equity, workbook, webhook, Apps Script, local app, analytics, AI,
  coaching, release, deploy, or production behavior.
- Corpus metadata must not cause diagnostics labels to become parser facts,
  live Arena drift proof, private smoke success, watcher correctness, status
  API health, release readiness, analytics readiness, AI prompts, gameplay
  advice, or tracker-completion authority.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- match/game identity
- deduplication
- diagnostics report shape
- live watcher diagnostics behavior
- live capture status behavior
- runtime status schema
- status API behavior
- drift report behavior
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

- `docs/contracts/parser_corpus_live_diagnostics_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md`

Files Codex C may inspect but must not change unless a separate contract
explicitly authorizes it:

- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- focused diagnostics, drift, status API, evidence-runtime-status, and local
  app watcher tests

## Public Interface

This contract adds no runtime public API.

The public artifact is the corpus parity compatibility report generated from
the committed corpus manifest and session ledger.

Expected corpus report effect:

- `mythic_edge.live_diagnostics` changes from `missing` to
  `covered_report_only`.
- The row uses no parser event families.
- The row uses no private local report artifact.
- The row carries an explicit note that committed diagnostics/status surfaces
  are report-only review boundaries and do not prove live health.
- Remaining rows must stay separately scoped:
  - `mythic_edge.private_log_report_only_drift`
  - `mythic_edge.analytics_readiness_labels`

## Required Corpus Manifest Entry

Codex C should add exactly one Mythic Edge entry for
`mythic_edge.live_diagnostics`.

Recommended manifest entry values:

- `entry_id`: `live_diagnostics_boundary_report_v1`
- `entry_type`: `session_ledger_entry`
- `source_kind`: `committed_count_only_report`
- `commit_status`: `committed`
- `privacy_class`: `committed_count_only`
- `sanitization_status`: `not_applicable_count_only`
- `scenario_families`: `["mythic_edge.live_diagnostics"]`
- `coverage_status`: `covered_report_only`
- `coverage_basis`: `["diagnostics_only", "fixture_metadata_only"]`
- `parser_event_families`: `[]`
- `external_reference_status`: `reference_category_not_checked`

Required notes must state that the row is a committed report-only boundary for
diagnostics and status surfaces, not evidence of:

- private smoke success;
- live Player.log health;
- watcher correctness;
- parser support for a live run;
- status API correctness as release readiness;
- production behavior;
- analytics readiness;
- AI/coaching readiness;
- full Mythic Edge corpus parity.

## Required Session Ledger Entry

Codex C should add exactly one session-ledger entry referenced by the manifest:

- `session_id`: `live_diagnostics_boundary_report_v1`
- `source_entry_id`: `live_diagnostics_boundary_report_v1`
- `scenario_families`: `["mythic_edge.live_diagnostics"]`
- `format_family`: `mythic_edge`
- `match_shape`: `live_diagnostics_boundary_report_only`
- `record_summary`: `committed_live_diagnostics_boundary_metadata_only`
- `game_rows_count`: `0`
- `result_shape`: `not_applicable`

Recommended `parser_coverage` fields:

- `parser_diagnostics_reference_entries`: `1`
- `live_watcher_diagnostics_reference_entries`: `1`
- `live_capture_no_row_reference_entries`: `1`
- `evidence_review_status_reference_entries`: `1`
- `status_api_reference_entries`: `1`
- `log_drift_reference_entries`: `1`
- `unknown_entry_reference_entries`: `1`
- `private_smoke_success_claims`: `0`
- `live_player_log_health_claims`: `0`
- `watcher_correctness_claims`: `0`
- `parser_support_claims`: `0`
- `release_readiness_claims`: `0`
- `deploy_readiness_claims`: `0`
- `production_readiness_claims`: `0`
- `analytics_truth_claims`: `0`
- `ai_truth_claims`: `0`
- `coaching_truth_claims`: `0`

Required `known_gaps`:

- No committed private Player.log evidence is included.
- No private smoke output is included.
- No live watcher correctness proof is included.
- No live Player.log health proof is included.
- No parser support or parser correctness claim is included.
- No status API, local app, analytics, AI, coaching, release, deploy, or
  production readiness claim is included.

## Required Guarantees

The future implementation must guarantee:

- Only `mythic_edge.live_diagnostics` changes coverage status in this slice.
- `mythic_edge.live_diagnostics` becomes `covered_report_only`.
- `coverage_basis` is exactly:
  `["diagnostics_only", "fixture_metadata_only"]`.
- No `parser_behavior_verified` basis is added.
- No `local_report_only` basis is added.
- No private local report summary is added.
- No parser event families are added.
- No raw Player.log, private smoke output, generated runtime artifact, SQLite
  database, workbook export, secret, token, credential, API key, or webhook URL
  is committed.
- Existing diagnostics/status tests may be cited as supporting evidence, but
  diagnostics/status implementation must remain unchanged.
- Adjacent rows, including `mythic_edge.private_log_report_only_drift` and
  `mythic_edge.analytics_readiness_labels`, remain out of scope.

## Unknowns

- Whether a later private-local smoke workflow should emit a local-only report
  for `mythic_edge.private_log_report_only_drift` remains outside this slice.
- Whether live diagnostics should ever gain a sanitized committed fixture
  remains open and would require a separate fixture-acceptance contract.
- Whether analytics readiness labels should become report-only corpus metadata
  remains outside this slice.
- Whether future browser-assisted private-release smoke reports should feed a
  corpus row remains outside this slice.

## Suspected Gaps

- Current corpus parity metadata can show a report-only diagnostics boundary,
  but cannot prove actual live capture health without private local evidence.
- Diagnostics, watcher status, capture heartbeat, and evidence runtime status
  are intentionally separate surfaces; the corpus row should not collapse them
  into one opaque readiness label.
- The remaining missing rows likely need separate contracts because private
  log drift and analytics readiness have different evidence and privacy risks.

## Validation Expectations

Required Codex C validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_corpus_live_diagnostics_coverage.md \
  docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_live_diagnostics_coverage.md \
  docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Recommended supporting validation if Codex C cites adjacent diagnostics
behavior:

```bash
PYTHONPATH=src python3 -m pytest -q \
  tests/test_parser_diagnostics_mode.py \
  tests/test_diagnostics.py \
  tests/test_log_drift_sensor.py \
  tests/test_evidence_runtime_status.py \
  tests/test_status_api.py
```

Codex E should verify:

- The row moved only to `covered_report_only`.
- The implementation did not add `parser_behavior_verified`.
- The implementation did not add a private local report artifact or fixture.
- The implementation did not change diagnostics, watcher, status API, parser,
  runtime, workbook, webhook, Apps Script, analytics, AI, or production code.
- The report notes preserve all non-claims.

## Codex C Handoff

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #420.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/420

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_live_diagnostics_coverage.md

Goal:
Implement the report-only corpus parity metadata boundary for
mythic_edge.live_diagnostics exactly as contracted. This is corpus metadata and
test work only. It must not change parser behavior, diagnostics behavior,
watcher behavior, live-capture behavior, status API behavior, runtime status
schema, evidence-ledger behavior, workbook/webhook/App Script behavior,
analytics truth, AI truth, coaching truth, release readiness, deploy readiness,
or production behavior.

Do:
- Refresh live GitHub and local git state.
- Verify origin/codex/parser-parity includes
  5180de4b5900dc4bfd895d394d1a5ac74994c4b4.
- Compare current corpus manifest/session ledger/tests against the contract
  before editing.
- Change only the corpus manifest, session ledger, focused corpus parity tests,
  implementation handoff, and contract test report as needed.
- Move only mythic_edge.live_diagnostics from missing to covered_report_only.
- Use coverage_basis exactly ["diagnostics_only", "fixture_metadata_only"].
- Preserve private-log, live-health, watcher-correctness, parser-support,
  release-readiness, production, analytics, AI, coaching, and full-parity
  non-claims.
- Produce docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md.
- Produce docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md.

Do not:
- Target main.
- Close tracker #158.
- Claim private smoke success, live Player.log health, watcher correctness,
  parser support, release readiness, production behavior, analytics truth, AI
  truth, coaching truth, or full corpus parity.
- Add parser_behavior_verified, local_report_only, private report artifacts,
  parser event families, committed logs, runtime artifacts, generated data,
  SQLite files, workbook exports, secrets, tokens, API keys, or webhook URLs.
- Change parser behavior, parser state final reconciliation, parser event
  classes, router semantics, diagnostics behavior, live watcher diagnostics
  behavior, live capture status behavior, status API behavior, evidence runtime
  status behavior, log-drift behavior, golden replay behavior, feature-equity
  behavior, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets sync, output transport, analytics behavior, AI/model-provider
  behavior, CI policy, merge policy, deploy policy, or production behavior.

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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/420"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/418"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/419"
  previous_merge_commit: "5180de4b5900dc4bfd895d394d1a5ac74994c4b4"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_live_diagnostics_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_live_diagnostics_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_live_diagnostics_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-live-diagnostics-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only"
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
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim private smoke success, live Player.log health, watcher correctness, parser support, release readiness, production behavior, analytics truth, AI truth, or coaching truth."
    - "Do not add parser_behavior_verified, local_report_only, private report artifacts, parser event families, committed logs, generated/private/runtime artifacts, SQLite files, workbook exports, secrets, tokens, API keys, or webhook URLs."
    - "Do not change parser behavior or protected parser/runtime/diagnostics/status/local-app/workbook/webhook/App Script/analytics/AI/production surfaces."
```
