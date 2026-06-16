# Parser Corpus Evidence-Ledger Provenance Coverage Contract

## Module

Evidence-ledger provenance corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`mythic_edge.evidence_ledger_provenance` with committed report-only metadata.
It proves that the repository contains a deterministic, reviewed
evidence-ledger provenance scaffold with schema snapshot, drift review,
invariant execution, runtime field-evidence mapping, validation-report wiring,
runtime health summary, and focused tests. It does not prove that every parser
field is semantically correct, that every consumer attaches field evidence, or
that Mythic Edge is ready for release, analytics, AI, coaching, or production.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/379
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/377
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/378
- Previous merge commit:
  `bb266a3d848bc9e0bec8d69be80828b1b8a12598`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-evidence-ledger-provenance-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `bb266a3d848bc9e0bec8d69be80828b1b8a12598`
- target_artifact:
  `docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_evidence_ledger_provenance_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_evidence_ledger_provenance_coverage.md`
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
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`
- `docs/contracts/player_log_evidence_ledger_schema_drift_report.md`
- `docs/contracts/player_log_evidence_ledger_invariant_execution.md`
- `docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md`
- `docs/contracts/player_log_evidence_ledger_validation_report_wiring.md`
- the player-log evidence-ledger runtime-health exposure contract
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
- `src/mythic_edge_parser/app/evidence_schema_drift_report.py`
- `src/mythic_edge_parser/app/evidence_invariant_execution.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- the evidence-ledger runtime-health summary module
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_evidence_ledger.py`
- `tests/test_evidence_schema_snapshot.py`
- `tests/test_evidence_schema_drift_report.py`
- `tests/test_evidence_invariant_execution.py`
- `tests/test_runtime_field_evidence.py`
- `tests/test_evidence_validation_report_wiring.py`
- the focused runtime-health summary tests

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, or external
  corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns only the corpus coverage metadata for the
`mythic_edge.evidence_ledger_provenance` scenario family. Evidence-ledger
modules own their existing provenance reports and validators. Parser modules
and parser state own parser facts. The corpus parity report owns only the
coverage-row statement that Mythic Edge has committed evidence-ledger
provenance scaffolding.

## Internal Project Area

Corpus / Provenance.

This slice consumes Quality / Governance validation evidence and Parser-owned
field names as references, but it is not a parser behavior module, not a
runtime behavior module, not an analytics module, not a workbook or transport
module, and not a Future AI Integration module.

## Truth Owner

Truth owner for `mythic_edge.evidence_ledger_provenance` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for evidence-ledger schema and vocabulary:

- `docs/contracts/player_log_evidence_ledger_schema.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`

Truth owner for evidence-ledger review surfaces:

- `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
- `src/mythic_edge_parser/app/evidence_schema_drift_report.py`
- `src/mythic_edge_parser/app/evidence_invariant_execution.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- the evidence-ledger runtime-health summary module

Truth boundary:

- The parser remains the source of parser-owned facts.
- The evidence ledger explains evidence, value-source policy, confidence,
  finality, degradation, drift flags, and review obligations.
- Schema snapshots, schema drift reports, invariant execution, runtime
  field-evidence reports, validation-review sections, and runtime health
  summaries are review evidence only.
- Corpus parity owns only the scenario-family coverage label and its supporting
  metadata.
- A coverage label must not become parser truth, evidence-ledger lifecycle
  completion authority, diagnostics readiness, live private-log health, release
  readiness, analytics truth, AI truth, coaching truth, merge readiness, deploy
  readiness, production behavior, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Corpus / Provenance evidence-ledger modules.

Consuming project area: Corpus / Provenance corpus parity report.

Allowed data flow:

```text
existing evidence-ledger objects, schema snapshots, drift reports,
invariant execution, runtime field-evidence, validation-review wiring,
and runtime-health summary evidence
  -> bounded committed count/report metadata in corpus manifest/session ledger
  -> corpus parity coverage row for mythic_edge.evidence_ledger_provenance
```

Forbidden reverse flow:

- Corpus coverage metadata must not change evidence-ledger schemas,
  vocabulary, entries, validators, snapshots, drift reports, invariant
  execution, runtime field-evidence behavior, validation report wiring, runtime
  health summary behavior, parser behavior, or downstream surfaces.
- Corpus coverage metadata must not cause evidence-ledger reports to be
  generated, written, consumed, or embedded in runtime products by default.
- Corpus coverage metadata must not imply every parser output field has a
  runtime-attached evidence record.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- match/game identity
- deduplication
- evidence-ledger vocabulary, schema, entries, validators, or report behavior
- diagnostics, golden replay, feature-equity, and drift report behavior
- runtime artifact shape or write behavior
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
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

- `docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_evidence_ledger_provenance_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_evidence_ledger_provenance_coverage.md`

Files Codex C may inspect, import, or exercise in focused tests but must not
change unless the contract is routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
- `src/mythic_edge_parser/app/evidence_schema_drift_report.py`
- `src/mythic_edge_parser/app/evidence_invariant_execution.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- the evidence-ledger runtime-health summary module
- `tests/test_evidence_ledger.py`
- `tests/test_evidence_schema_snapshot.py`
- `tests/test_evidence_schema_drift_report.py`
- `tests/test_evidence_invariant_execution.py`
- `tests/test_runtime_field_evidence.py`
- `tests/test_evidence_validation_report_wiring.py`
- the focused runtime-health summary tests
- `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- evidence-ledger source changes
- evidence-ledger schema snapshot updates
- new evidence-ledger entries or output families
- evidence-ledger vocabulary changes
- runtime field-evidence behavior changes
- diagnostics, golden replay, feature-equity, drift, or runtime health wiring
  changes
- generated report commits
- private live-log smoke output
- external corpus import
- `timer.pre_match_idle` coverage
- `mythic_edge.live_diagnostics`
- `mythic_edge.private_log_report_only_drift`
- `mythic_edge.analytics_readiness_labels`
- `mythic_edge.workbook_row_coverage`
- `mythic_edge.confidence_finality_degradation`
- any AI, coaching, workbook, transport, CI, production, merge, deploy, or
  tracker lifecycle behavior

## Public Interface

Existing corpus parity public interface referenced by this contract:

```text
build_corpus_parity_report(
    manifest_path,
    *,
    session_ledger_path=None,
    feature_equity_report=None,
    external_reference=None,
) -> dict

validate_corpus_manifest(payload) -> list[str]
validate_session_ledger(payload) -> list[str]
python3 -m mythic_edge_parser.app.corpus_parity_report <manifest> --session-ledger <ledger>
```

Existing evidence-ledger public interfaces used as evidence:

```text
build_player_log_evidence_ledger() -> dict
iter_ledger_entries() -> tuple[dict, ...]
validate_player_log_evidence_ledger(payload=None) -> list[str]
validate_ledger_entry(entry) -> list[str]
validate_field_evidence(payload) -> list[str]

build_evidence_schema_snapshot(...) -> dict
compare_evidence_schema_snapshot(current, expected) -> dict
load_expected_evidence_schema_snapshot(...) -> dict
build_current_evidence_schema_drift_report(...) -> dict
build_current_evidence_invariant_execution_report(...) -> dict
build_runtime_field_evidence_report(...) -> dict
build_evidence_ledger_review_section(...) -> dict
build_evidence_ledger_health_status(...) -> dict
```

No new public parser, evidence-ledger, runtime, diagnostics, drift, golden
replay, feature-equity, workbook, webhook, Apps Script, analytics, AI, or
production interface is authorized by this contract.

## Observed Current Behavior

Observed on `codex/parser-parity` at
`bb266a3d848bc9e0bec8d69be80828b1b8a12598`:

- Issue #379 is open under tracker #158.
- Tracker #158 is open.
- PR #378 is merged into `codex/parser-parity`.
- Corpus parity report status is:

```text
partial_coverage_map_ready (45 families, 6 committed, 18 missing)
```

- `log_runtime.unknown_entry` is now `covered_report_only`.
- `timer.pre_match_idle` remains `missing`.
- `mythic_edge.evidence_ledger_provenance` remains:

```text
missing / external_reference_only / no Mythic Edge entries
```

Current evidence-ledger observations:

- `build_player_log_evidence_ledger()` returns object
  `mythic_edge_player_log_evidence_ledger`.
- Current ledger schema version is `player_log_evidence_ledger_schema.v1`.
- Current ledger version is `player_log_evidence_ledger.v1`.
- Current ledger has 7 output families and 71 entries.
- Current ledger validation returns no errors.
- Current evidence schema snapshot has:
  - 7 output families
  - 71 entries
  - 448 evidence signals
  - 204 direct evidence signals
  - 244 fallback evidence signals
  - deferred output field `tier3.game_level_facts.deck_state`
- Current committed schema snapshot comparison status is `pass`.
- Current schema drift report status is `pass`.
- Current invariant execution report status is `pass`.
- Current invariant execution report has 11 executable invariants, 425 declared
  invariant references, and 394 unique declared invariant names.
- An empty runtime field-evidence report currently returns `pass` with zero
  attachments.
- An empty validation-review section currently returns `fail` because no source
  reports are supplied.
- An empty runtime health summary currently returns `unavailable` because no
  source reports are supplied.

Observed gap:

- The corpus parity matrix does not yet represent the committed
  evidence-ledger provenance scaffold as Mythic Edge coverage.
- The current `missing / external_reference_only` row under-describes the
  branch because the ledger, snapshot, drift, invariant, runtime field-evidence,
  validation wiring, runtime health summary, and focused tests exist in the
  repository.

## Required Guarantees

### Coverage Decision

Codex C may move `mythic_edge.evidence_ledger_provenance` from `missing` to
`covered_report_only`.

Codex C must not use `covered_committed` or `covered_synthetic` for this
family in issue #379.

Rationale:

- The coverage is committed, deterministic, and test-backed.
- The evidence is a provenance/report scaffold, not a parser behavior fixture.
- It does not execute a new gameplay parser scenario.
- It does not prove semantic correctness for every field or every future
  consumer.

### Coverage Basis

The required basis values are:

- `evidence_ledger_only`
- `fixture_metadata_only`
- `count_ratchet_only`

Interpretation:

- `evidence_ledger_only`: the claim is grounded in the committed
  evidence-ledger schema, entries, vocabulary, validators, snapshots, drift,
  invariant, and review/health support.
- `fixture_metadata_only`: the corpus row is a metadata coverage entry, not a
  new parser fixture.
- `count_ratchet_only`: the coverage records counts and report status evidence
  only; it does not embed or regenerate full report payloads.

Codex C must not add `parser_behavior_verified`, because this issue is not a
parser behavior fixture and does not exercise parser interpretation.

### Manifest Entry

Codex C should add exactly one corpus manifest entry for this family unless it
discovers that the existing manifest schema requires a smaller split.

Recommended entry id:

```text
evidence_ledger_provenance_report_reference_v1
```

Recommended logical shape:

```yaml
entry_id: "evidence_ledger_provenance_report_reference_v1"
entry_type: "session_ledger_entry"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/379"
authorized_by_contract: "docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  evidence_schema_snapshot: "tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json"
  evidence_ledger_test: "tests/test_evidence_ledger.py"
  evidence_schema_snapshot_test: "tests/test_evidence_schema_snapshot.py"
  evidence_schema_drift_report_test: "tests/test_evidence_schema_drift_report.py"
  evidence_invariant_execution_test: "tests/test_evidence_invariant_execution.py"
  runtime_field_evidence_test: "tests/test_runtime_field_evidence.py"
  evidence_validation_report_wiring_test: "tests/test_evidence_validation_report_wiring.py"
  runtime_health_summary_test: "focused runtime-health summary tests"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
scenario_families:
  - "mythic_edge.evidence_ledger_provenance"
parser_event_families: []
parser_claim_families:
  - "evidence_ledger_schema"
  - "evidence_ledger_entries"
  - "evidence_schema_snapshot"
  - "evidence_schema_drift_report"
  - "evidence_invariant_execution"
  - "runtime_field_evidence_mapping"
  - "validation_report_wiring"
  - "runtime_health_summary_boundary"
  - "evidence_ledger_privacy_boundary"
coverage_status: "covered_report_only"
coverage_basis:
  - "evidence_ledger_only"
  - "fixture_metadata_only"
  - "count_ratchet_only"
```

Required known gaps:

- The row does not prove semantic parser correctness for every ledger entry.
- The row does not prove every parser output field has runtime-attached field
  evidence in every consumer.
- The row does not prove live private-log health, diagnostics readiness,
  release readiness, analytics truth, AI truth, coaching truth, production
  behavior, or tracker completion.
- The row does not cover `timer.pre_match_idle`,
  `mythic_edge.live_diagnostics`,
  `mythic_edge.private_log_report_only_drift`,
  `mythic_edge.analytics_readiness_labels`,
  `mythic_edge.workbook_row_coverage`, or
  `mythic_edge.confidence_finality_degradation`.

Required review note:

```text
Evidence-ledger provenance coverage proves that Mythic Edge has committed,
deterministic provenance metadata and review scaffolding for parser-owned fact
evidence; it does not prove parser correctness for every field or runtime
attachment in every consumer.
```

### Session Ledger Entry

Codex C should add a matching session ledger row.

Recommended logical shape:

```yaml
session_id: "evidence_ledger_provenance_report_reference_v1"
title: "Report-only evidence-ledger provenance scaffold"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/379"
authorized_by_contract: "docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md"
scenario_families:
  - "mythic_edge.evidence_ledger_provenance"
format_family: "mythic_edge_provenance"
match_shape: "evidence_ledger_report_reference_only"
record_summary: "committed_provenance_metadata_summary_only"
parser_coverage:
  event_families: {}
  unknown_entries: 0
  truncation_count: 0
  evidence_ledger_output_families: 7
  evidence_ledger_entries: 71
  evidence_ledger_evidence_signals: 448
  evidence_schema_snapshot_status: "pass"
  evidence_schema_drift_status: "pass"
  evidence_invariant_execution_status: "pass"
  executable_invariants: 11
  declared_invariants: 425
  declared_unique_invariants: 394
  runtime_field_evidence_surface: "available_review_sidecar"
  validation_report_wiring_surface: "available_report_only"
  runtime_health_surface: "available_summary_only"
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Evidence-ledger provenance metadata does not prove semantic parser correctness, universal field-evidence attachment, live private-log health, release readiness, analytics truth, AI truth, coaching truth, production behavior, or tracker completion."
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
  external_logs_included: false
  decklists_included: false
```

Codex C may adjust count field names to match existing session-ledger style,
but must preserve the meaning and the privacy boundary.

### Count Freshness Policy

The recommended counts above are observed at the base commit. Codex C must
refresh them from the current branch during implementation.

If counts change because the base branch has advanced, Codex C must:

- inspect why the counts changed;
- update the contract-test report or implementation handoff with the observed
  current counts;
- avoid changing evidence-ledger behavior in this issue;
- route back to Codex B if the change alters coverage meaning, vocabulary,
  schema, privacy posture, or protected-surface scope.

### Non-Claims

This coverage row must explicitly not claim:

- full Mythic Edge corpus parity;
- parser support from corpus metadata alone;
- parser correctness for every evidence-ledger entry;
- evidence-ledger lifecycle completion;
- universal runtime field-evidence attachment;
- diagnostics readiness;
- live private-log health;
- release readiness;
- analytics truth;
- AI truth;
- coaching or gameplay advice;
- hidden-card inference;
- archetype classification;
- player-mistake labels;
- merge readiness;
- deploy readiness;
- production behavior;
- tracker #158 completion.

### Deferred Candidate

`timer.pre_match_idle` remains deferred. It needs dedicated pre-match
timer-state evidence or approval-gated private smoke planning before coverage.
Codex C must not cover it in issue #379.

## Inputs

Allowed inputs:

- Current repo docs and contracts named by this contract.
- Existing corpus parity manifest and session ledger.
- Existing committed evidence-ledger code and focused tests.
- Existing committed schema snapshot fixture.
- Current report output from the corpus parity CLI.
- Current report output from evidence-ledger builders when generated locally
  during validation and not committed as generated artifacts.
- Public Manasight metadata only through category-level taxonomy context
  already represented by prior corpus parity artifacts.

Forbidden inputs:

- Manasight raw logs, compressed corpus files, raw session payloads, hash lists,
  byte-size lists, capture-date row lists, parser source, or external corpus
  contents.
- Private Player.log excerpts, private local logs, private smoke outputs,
  generated data, SQLite files, runtime artifacts, workbook exports,
  credentials, tokens, API keys, webhook endpoints, IP/network traces,
  decklists, deck names, card choices, strategy notes, or private reports.
- Newly generated evidence report JSON or Markdown committed as source
  artifacts, unless a later contract authorizes exact report artifact storage.

## Outputs

Authorized output changes for Codex C:

- One new corpus manifest entry for
  `mythic_edge.evidence_ledger_provenance`.
- One new session ledger entry for
  `mythic_edge.evidence_ledger_provenance`.
- Focused corpus parity tests that assert:
  - the new entry validates;
  - the new session validates;
  - the coverage row is `covered_report_only`;
  - the coverage basis contains exactly the required bounded basis values;
  - no parser event families are claimed;
  - non-claims are present in known gaps or review notes;
  - the report summary shifts by one from missing to covered-report-only.
- Implementation handoff and contract-test report documents.

Expected report summary after implementation, assuming no other branch changes:

```text
partial_coverage_map_ready (45 families, 6 committed, 17 missing)
```

Expected summary count changes:

- `covered_report_only`: 1 -> 2
- `missing`: 18 -> 17
- `covered_committed`: unchanged
- `covered_synthetic`: unchanged
- `partial`: unchanged
- `blocked_external_boundary`: unchanged

## Invariants

- `mythic_edge.evidence_ledger_provenance` coverage must remain
  `covered_report_only` for issue #379.
- `parser_event_families` must be empty for the new manifest entry.
- The new entry must not use `parser_behavior_verified`.
- The new entry must not reference private paths, raw local log content,
  external corpus files, generated report outputs, SQLite files, or workbook
  exports.
- The new entry must not reference `timer.pre_match_idle`.
- The new entry must not change the scenario-family taxonomy list.
- The new entry must not change allowed coverage vocabulary.
- The new entry must not mutate evidence-ledger source, validators, reports, or
  snapshots.
- The corpus parity report status may remain `partial_coverage_map_ready`.
  Issue #379 must not try to make it fully ready.
- Protected-surface assertions in evidence-ledger review outputs must remain
  review evidence only.

## Error Behavior

Contract ambiguity:

- If Codex C cannot represent this slice using the existing manifest/session
  schema and allowed status/basis vocabulary, it must route back to Codex B.

Evidence-ledger drift:

- If focused evidence-ledger tests fail on the current base before Codex C
  edits behavior, Codex C must stop and report the base failure rather than
  patching evidence-ledger behavior inside this issue.

Count drift:

- If counts differ from the observed base but reports still pass, Codex C may
  update metadata counts and explain the difference in the handoff.
- If counts differ because schema, vocabulary, privacy, or report semantics
  changed, Codex C must route back for contract clarification.

Privacy or protected-surface warnings:

- If secret/private-marker or protected-surface checks warn on the new docs,
  Codex C must reword or narrow the metadata. It must not suppress the checks
  or add broad allowlists.

Generated artifact temptation:

- If implementation would require committing generated reports, private smoke
  output, or runtime artifacts, stop and route back. Issue #379 authorizes
  metadata references and tests, not generated report storage.

## Side Effects

Codex B side effects:

- Create only this contract.

Codex C authorized side effects:

- Edit corpus manifest JSON.
- Edit session ledger JSON.
- Edit focused corpus parity tests.
- Write implementation handoff.
- Write contract-test report.

No runtime side effects, local external writes, GitHub issue closure, PR
creation, tracker completion, generated artifact commits, workbook changes,
webhook changes, Apps Script changes, analytics changes, AI/model-provider
calls, or production behavior changes are authorized.

## Dependency Order

Codex C should proceed in this order:

1. Verify branch state against `origin/codex/parser-parity`.
2. Run the current corpus parity report and capture the existing row for
   `mythic_edge.evidence_ledger_provenance`.
3. Run focused evidence-ledger checks or builders needed to refresh counts.
4. Add the manifest entry.
5. Add the session ledger entry.
6. Add focused corpus parity assertions.
7. Run validation.
8. Write the implementation handoff and contract-test report.

## Compatibility

This contract preserves:

- corpus manifest schema version `parser_corpus_manifest.v1`;
- session ledger schema version `parser_corpus_session_ledger.v1`;
- scenario family id `mythic_edge.evidence_ledger_provenance`;
- coverage status vocabulary;
- coverage basis vocabulary;
- evidence-ledger object and schema versions;
- evidence-ledger report object names;
- parser behavior and downstream surface shapes.

No migration is authorized.

## Tests Required

Focused validation for Codex C:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_evidence_ledger.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py tests/test_evidence_invariant_execution.py tests/test_runtime_field_evidence.py tests/test_evidence_validation_report_wiring.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_evidence_ledger_provenance_coverage_comparison.md docs/contract_test_reports/parser_corpus_evidence_ledger_provenance_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_evidence_ledger_provenance_coverage_comparison.md docs/contract_test_reports/parser_corpus_evidence_ledger_provenance_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_evidence_ledger_provenance_coverage_comparison.md docs/contract_test_reports/parser_corpus_evidence_ledger_provenance_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

Recommended broader validation if the environment is ready:

```bash
PYTHONPATH=src python3 -m ruff check src tests
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_evidence_ledger.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py tests/test_evidence_invariant_execution.py tests/test_runtime_field_evidence.py tests/test_evidence_validation_report_wiring.py
```

Codex C must record any skipped validation and why.

## Acceptance Criteria

- `docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md`
  exists.
- Codex C updates exactly the corpus metadata/test surfaces authorized by this
  contract, unless it routes back.
- The corpus manifest validates cleanly.
- The session ledger validates cleanly.
- The corpus parity report still returns `partial_coverage_map_ready`.
- `mythic_edge.evidence_ledger_provenance` reports:
  - `coverage_status: covered_report_only`
  - `coverage_basis: ["evidence_ledger_only", "fixture_metadata_only", "count_ratchet_only"]`
  - one Mythic Edge entry,
    `evidence_ledger_provenance_report_reference_v1`
- The entry has no parser event families.
- Tests assert the non-claims and the deferred `timer.pre_match_idle` boundary.
- No raw/private/external/generated artifacts are committed.
- No protected parser/runtime/workbook/webhook/App Script/diagnostics/golden
  replay/feature-equity/evidence-ledger/analytics/AI/production behavior
  changes are made.
- The implementation handoff and contract-test report name remaining gaps.

## Open Questions And Suspected Gaps

- The exact evidence-ledger counts may change if `codex/parser-parity` advances
  before Codex C starts. This is acceptable only if the meaning and privacy
  posture remain unchanged.
- `mythic_edge.confidence_finality_degradation` and
  `mythic_edge.workbook_row_coverage` are adjacent Mythic Edge families but are
  not covered by this issue.
- The validation-review and runtime-health helpers can report `fail` or
  `unavailable` when no source reports are supplied. That is not a blocker for
  `covered_report_only`, because the coverage claim is existence and
  boundary-oriented, not "all review surfaces are passing in every empty-input
  mode."
- This contract does not decide whether future local runtime products should
  expose evidence-ledger health. That remains governed by the existing runtime
  status exposure contract and future implementation/review work.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #379.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/379

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md

Goal:
Implement the smallest metadata/test/report-only change needed to satisfy the
evidence-ledger provenance corpus coverage contract. Move only
`mythic_edge.evidence_ledger_provenance` from missing to `covered_report_only`
using committed count/report metadata. Do not change parser behavior or
evidence-ledger behavior.

Before editing:
1. Fetch and verify `origin/codex/parser-parity`.
2. Create or use a clean implementation branch from `codex/parser-parity`.
3. Confirm PR #378 merged at
   `bb266a3d848bc9e0bec8d69be80828b1b8a12598` or record the newer base.
4. Inspect `git status --short --branch`.
5. Leave unrelated or untracked local artifacts alone.

Read:
- docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md
- docs/contracts/parser_corpus_parity_expansion.md
- docs/contracts/parser_corpus_unknown_entry_coverage.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- src/mythic_edge_parser/app/evidence_schema_drift_report.py
- src/mythic_edge_parser/app/evidence_invariant_execution.py
- src/mythic_edge_parser/app/runtime_field_evidence.py
- src/mythic_edge_parser/app/evidence_validation_report_wiring.py
- the evidence-ledger runtime-health summary module
- focused evidence-ledger tests named by the contract

Do:
- Compare the current corpus parity report against the contract before editing.
- Refresh evidence-ledger counts from the current branch.
- Add exactly one manifest entry for
  `evidence_ledger_provenance_report_reference_v1`.
- Add the matching session ledger entry.
- Add focused tests proving `mythic_edge.evidence_ledger_provenance` is
  `covered_report_only` with bounded basis values and non-claims.
- Preserve `timer.pre_match_idle` as missing/deferred.
- Produce
  `docs/implementation_handoffs/parser_corpus_evidence_ledger_provenance_coverage_comparison.md`.
- Produce
  `docs/contract_test_reports/parser_corpus_evidence_ledger_provenance_coverage.md`.

Do not:
- Change parser behavior.
- Change evidence-ledger vocabulary, schema, entries, validators, snapshots,
  drift reports, invariant execution, runtime field-evidence behavior,
  validation report wiring, runtime health summary behavior, diagnostics,
  golden replay, feature-equity, router semantics, parser state final
  reconciliation, parser event classes, match/game identity, workbook/webhook
  or Apps Script behavior, analytics truth, AI truth, production behavior, CI
  gates, merge readiness, deploy readiness, or tracker lifecycle behavior.
- Cover `timer.pre_match_idle` or any other scenario family in issue #379.
- Claim full Mythic Edge corpus parity or parser support from corpus metadata
  alone.
- Import, copy, mirror, or commit external corpus contents or forbidden
  private/generated/local artifacts named by the contract.
- Target main directly.
- Close issue #379 or tracker #158.
- Stage or commit unless explicitly asked.

Validation:
- Run the focused validation commands from the contract.
- Run changed-file secret/private and protected-surface checks.
- Record skipped validation with reasons.

Expected output:
- Updated corpus manifest/session ledger/tests.
- Implementation handoff.
- Contract-test report.
- Validation summary.
- workflow_handoff block to Codex E.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/379"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/377"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/378"
  previous_merge_commit: "bb266a3d848bc9e0bec8d69be80828b1b8a12598"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_evidence_ledger_provenance_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_evidence_ledger_provenance_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_evidence_ledger_provenance_coverage.md"
  verdict: "contract_ready_for_report_only_evidence_ledger_provenance_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-evidence-ledger-provenance-coverage"
  base_branch: "codex/parser-parity"
  deferred_candidate: "timer.pre_match_idle needs dedicated pre-match timer-state evidence or approval-gated private smoke planning before coverage."
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_evidence_ledger.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py tests/test_evidence_invariant_execution.py tests/test_runtime_field_evidence.py tests/test_evidence_validation_report_wiring.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "changed-file secret/private marker scan"
    - "changed-file protected-surface gate"
    - "changed-file validation selector"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not close issue #379."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim parser support from corpus metadata alone."
    - "Do not cover timer.pre_match_idle or any other scenario family in issue #379."
    - "Do not import, copy, mirror, or commit external corpus contents or forbidden private/generated/local artifacts named by the contract."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```
