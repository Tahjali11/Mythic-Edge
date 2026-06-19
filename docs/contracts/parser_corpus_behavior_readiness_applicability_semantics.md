# Parser Corpus Behavior Readiness Applicability Semantics Contract

## Module

Parser corpus behavior-readiness applicability semantics under tracker #158.

Plain English: issue #462 made corpus readiness visible, and issue #475 sorted
the remaining not-parser-behavior-ready rows into future work classes. This
contract defines which rows should actually count toward a parser-behavior
readiness denominator, which rows are non-behavior governance/provenance or
reporting concepts, and how any future derived metric must avoid fake fixtures,
silent row promotion, or premature #388 / #381 activation.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/477
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/475
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/476
- Previous merge commit: `ad222e4bad8209a6baad631f1769ad273ff031b0`
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-behavior-readiness-applicability-477`
- Risk tier: High
- Status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- issue #388 and child issue #381, as deferred pipeline context only
- parent issue #434, as private-evidence context only

## Purpose

Define applicability semantics for parser-behavior readiness so Mythic Edge can
separate:

- all-family corpus classification completeness;
- parser-behavior readiness for rows where parser behavior is a meaningful
  target;
- governance/provenance/reporting rows that should not become parser fixtures;
- private-evidence and external-boundary rows that remain gated; and
- #388 / #381 activation evidence.

This contract recommends an additive future metric implementation. It does not
authorize code changes in Codex B, corpus status promotion, fixture creation,
private evidence execution, #388 / #381 activation, tracker closure, release
readiness, production behavior, analytics truth, AI truth, or coaching truth.

## Observed Current Behavior

Observed on `main` at
`ad222e4bad8209a6baad631f1769ad273ff031b0`:

- Issue #477 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #475 is complete after PR #476.
- The corpus parity CLI reports:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=14, report_only=19, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current readiness metrics:

```yaml
classification_complete: true
parser_behavior_ready: false
parser_behavior_ready_family_count: 19
total_scenario_families: 45
committed_parser_behavior_families: 5
synthetic_parser_behavior_families: 14
report_only_families: 19
blocked_families: 6
blocked_private_evidence_families: 2
blocked_external_boundary_families: 4
pipeline_activation_ready_for_issue_388: false
readiness_verdict: "classification_complete_not_behavior_ready"
```

The current report correctly refuses to call the corpus parser-behavior-ready.
The semantic gap is that `total_scenario_families: 45` includes rows that
should never be converted into parser-behavior fixtures, such as manifest
metadata, evidence-ledger provenance, live diagnostics report boundaries, and
analytics-readiness labels.

## Scope Decision

This contract is a semantics and future-metrics contract.

Codex B may:

- classify all 45 corpus rows by parser-behavior applicability;
- define non-behavior rows that should be excluded from an
  applicability-aware denominator;
- recommend additive derived metrics for a future Codex C implementation;
- preserve existing all-family readiness metrics and #388 / #381 gates; and
- route implementation or review with explicit stop conditions.

Codex B must not:

- implement code;
- edit the corpus manifest or session ledger;
- change readiness metric implementation;
- promote report-only, private-evidence, or external-boundary rows;
- create fixtures;
- run private/live checks;
- start #388 or #381;
- claim parser support, full corpus parity, private smoke success, release
  readiness, production behavior, analytics truth, AI truth, coaching truth, or
  tracker completion.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns only derived applicability semantics for corpus-readiness
reporting. It does not own parser behavior, parser correctness, fixture truth,
private evidence, external evidence, analytics truth, release readiness, deploy
readiness, production behavior, or tracker completion.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting: Quality / Governance for workflow sequencing, protected-surface
checks, and wording that prevents readiness overclaims.

This slice is not a Parser module, parser-evidence pipeline module,
private-evidence execution module, analytics module, AI module, coaching
module, CI gate, merge gate, deploy gate, release gate, or production module.

## Truth Owner

Truth owner for current corpus coverage rows remains:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for current all-family readiness metrics remains:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `docs/contracts/parser_corpus_readiness_metrics.md`

Truth owner for the proposed applicability semantics:

- this contract;
- a future additive implementation in
  `src/mythic_edge_parser/app/corpus_parity_report.py`, if separately
  implemented;
- focused tests in `tests/test_corpus_parity_report.py`, if separately
  implemented.

Truth boundary:

- Corpus parity may classify whether a scenario family is applicable to
  parser-behavior readiness metrics.
- Parser modules own event interpretation and parser behavior.
- Golden replay owns committed fixture execution only after a later contract
  authorizes a fixture.
- Private evidence remains local and approval-gated under #434 and related
  private-evidence contracts.
- Public external taxonomy remains category reference only.
- Analytics, workbook, Google Sheets, Apps Script, webhook transport, local app,
  Match Journal, overlay, AI/model-provider behavior, coaching, CI, merge,
  deploy, production, and tracker lifecycle remain downstream or out of scope.

## Bridge-Code Status

`not_bridge_code`

This contract creates no bridge code and authorizes no data-flow changes. A
future implementation may add derived report metrics inside the existing corpus
parity report, but it must not bridge parser truth into downstream surfaces or
move downstream truth back into parser-owned interpretation.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`

Future Codex C files authorized only if implementation is selected:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_behavior_readiness_applicability_semantics_comparison.md`
- `docs/contract_test_reports/parser_corpus_behavior_readiness_applicability_semantics.md`

Files Codex C may read but must not modify in this slice:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- recent parser-corpus contracts, handoffs, and reports
- GitHub issues #158, #388, #381, #434, #475, and #477

Not owned by this contract:

- parser modules;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- diagnostics, golden replay, feature-equity, drift, evidence-ledger, or
  analytics behavior;
- corpus manifest or session-ledger status promotion;
- fixtures or expected outputs;
- private/local artifacts;
- external corpus contents;
- workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, runtime status files, failed posts, workbook exports,
  generated data, CI gates, merge readiness, deploy readiness, production
  behavior, or tracker completion.

## Public Interface

No runtime public API is added by Codex B.

Future Codex C should add an additive derived report object under
`readiness_metrics`, preserving existing report keys and status semantics:

```yaml
readiness_metrics:
  behavior_applicability:
    schema_version: "parser_corpus_behavior_applicability.v1"
    parser_behavior_applicable_family_count: 37
    parser_behavior_applicable_ready_family_count: 19
    parser_behavior_applicable_not_ready_family_count: 18
    parser_behavior_not_applicable_family_count: 8
    parser_behavior_applicable_report_only_family_count: 13
    parser_behavior_applicable_blocked_private_evidence_family_count: 1
    parser_behavior_applicable_blocked_external_boundary_family_count: 4
    parser_behavior_applicability_ready: false
    parser_behavior_applicability_verdict: "applicable_families_not_behavior_ready"
```

Codex C may choose equivalent additive field names only if they are clearer and
fully tested. It must not remove or reinterpret current keys:

- `parser_behavior_ready`
- `parser_behavior_ready_family_count`
- `total_scenario_families`
- `pipeline_activation_ready_for_issue_388`
- `pipeline_activation_blockers`
- `readiness_verdict`

The existing all-family `parser_behavior_ready` remains a strict legacy
all-row signal unless a later issue explicitly migrates it.

## Applicability Classes

### `parser_behavior_applicable_ready`

Rows where parser-behavior evidence is applicable and already represented by
`covered_committed` or `covered_synthetic` with `parser_behavior_verified`.

Metric treatment:

- counts toward `parser_behavior_applicable_family_count`;
- counts toward `parser_behavior_applicable_ready_family_count`;
- does not imply production readiness, private smoke success, analytics truth,
  AI truth, coaching truth, full corpus parity, or tracker completion.

### `parser_behavior_applicable_not_ready`

Rows where parser-behavior evidence is meaningful, but the current row is
report-only or otherwise lacks `parser_behavior_verified`.

Metric treatment:

- counts toward `parser_behavior_applicable_family_count`;
- counts toward `parser_behavior_applicable_not_ready_family_count`;
- must not count as ready until a dedicated issue, contract, evidence source,
  and tests authorize the change.

### `parser_behavior_applicable_blocked_private`

Rows where parser-behavior evidence is meaningful but currently requires
private/live evidence approval.

Metric treatment:

- counts toward `parser_behavior_applicable_family_count`;
- counts as a not-ready private blocker;
- must remain gated by #434 and local-only private-evidence contracts.

### `parser_behavior_applicable_blocked_external`

Rows where parser-behavior evidence is meaningful but currently depends on an
external-boundary or separately generated owned evidence path.

Metric treatment:

- counts toward `parser_behavior_applicable_family_count`;
- counts as a not-ready external-boundary blocker;
- must not be promoted from public taxonomy or adjacent coverage alone.

### `non_behavior_applicability_excluded`

Rows that are corpus governance, provenance, diagnostics/reporting,
workbook-facing coverage, private-reporting, or analytics-readiness concepts.
They should not be turned into parser-behavior fixtures and should not count
toward an applicability-aware parser-behavior denominator.

Metric treatment:

- counts toward `parser_behavior_not_applicable_family_count`;
- remains visible in the report;
- must not be hidden from summary counts;
- must not be used to claim parser support, readiness, or tracker completion.

## Applicability-Class Table

Observed at `ad222e4bad8209a6baad631f1769ad273ff031b0`:

| Scenario family | Current status | Current basis | Applicability class |
| --- | --- | --- | --- |
| `manifest.metadata` | `covered_report_only` | `fixture_metadata_only` | `non_behavior_applicability_excluded` |
| `session.ledger_metadata` | `covered_committed` | `fixture_metadata_only` | `non_behavior_applicability_excluded` |
| `core_gameplay.standard_bo1` | `covered_committed` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `core_gameplay.standard_bo3` | `covered_committed` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `core_gameplay.traditional_bo3` | `covered_committed` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `core_gameplay.draft_with_games` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `core_gameplay.draft_only` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `core_gameplay.sealed_entry` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `core_gameplay.sealed_deckbuild` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `core_gameplay.sealed_matches` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `log_runtime.detailed_logs_disabled` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `log_runtime.rotation` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `log_runtime.malformed_or_headerless` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `log_runtime.timestamp_anomaly` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `log_runtime.unknown_entry` | `covered_report_only` | `diagnostics_only,evidence_ledger_only,fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `connection.reconnect` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `connection.disconnect` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `connection.firewall_or_network_drop` | `blocked_private_evidence` | `local_report_only` | `parser_behavior_applicable_blocked_private` |
| `connection.connection_error_payload` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `timer.active_player_timer` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `timer.inactivity_timeout` | `blocked_external_boundary` | `external_reference_only` | `parser_behavior_applicable_blocked_external` |
| `timer.pre_match_idle` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `deck_api.start_hook_deck_snapshot` | `covered_synthetic` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `deck_api.deck_summary` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `deck_api.deck_upsert` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `deck_api.event_set_deck` | `covered_committed` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `deck_api.store_pack_inbox_or_crafting` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `gameplay_stress.mulligan` | `covered_committed` | `fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `gameplay_stress.opponent_auto_concede` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `gameplay_stress.conjure` | `blocked_external_boundary` | `external_reference_only` | `parser_behavior_applicable_blocked_external` |
| `gameplay_stress.spellbook` | `blocked_external_boundary` | `external_reference_only` | `parser_behavior_applicable_blocked_external` |
| `gameplay_stress.companion_or_large_deck` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `gameplay_stress.action_attribution` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `gameplay_stress.event_ordering` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `drift_debug.gsm_truncation` | `covered_synthetic` | `count_ratchet_only,diagnostics_only,fixture_metadata_only,parser_behavior_verified` | `parser_behavior_applicable_ready` |
| `drift_debug.recycle_or_rollback` | `blocked_external_boundary` | `external_reference_only` | `parser_behavior_applicable_blocked_external` |
| `drift_debug.missing_message_type` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `drift_debug.rename_or_rotation_collision` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `drift_debug.phantom_or_deck_origin` | `covered_report_only` | `fixture_metadata_only` | `parser_behavior_applicable_not_ready` |
| `mythic_edge.evidence_ledger_provenance` | `covered_report_only` | `count_ratchet_only,evidence_ledger_only,fixture_metadata_only` | `non_behavior_applicability_excluded` |
| `mythic_edge.confidence_finality_degradation` | `covered_report_only` | `evidence_ledger_only,fixture_metadata_only` | `non_behavior_applicability_excluded` |
| `mythic_edge.workbook_row_coverage` | `covered_report_only` | `fixture_metadata_only` | `non_behavior_applicability_excluded` |
| `mythic_edge.live_diagnostics` | `covered_report_only` | `diagnostics_only,fixture_metadata_only` | `non_behavior_applicability_excluded` |
| `mythic_edge.private_log_report_only_drift` | `blocked_private_evidence` | `local_report_only` | `non_behavior_applicability_excluded` |
| `mythic_edge.analytics_readiness_labels` | `covered_report_only` | `fixture_metadata_only` | `non_behavior_applicability_excluded` |

## Non-Behavior Row Decisions

The following rows should be excluded from an applicability-aware
parser-behavior denominator:

- `manifest.metadata`
- `session.ledger_metadata`
- `mythic_edge.evidence_ledger_provenance`
- `mythic_edge.confidence_finality_degradation`
- `mythic_edge.workbook_row_coverage`
- `mythic_edge.live_diagnostics`
- `mythic_edge.private_log_report_only_drift`
- `mythic_edge.analytics_readiness_labels`

### `session.ledger_metadata`

`session.ledger_metadata` may remain `covered_committed` because the committed
session ledger exists and validates. It must remain outside parser-behavior
readiness unless a later contract creates a specific parser-behavior claim for
session-ledger content. Its current `fixture_metadata_only` basis is correct
for metadata completeness, not parser behavior.

### `mythic_edge.live_diagnostics`

`mythic_edge.live_diagnostics` remains a report/diagnostics boundary. It must
not become parser truth, live Player.log health truth, watcher correctness,
release readiness, production behavior, analytics truth, AI truth, or coaching
truth. A later private/local diagnostics evidence issue may add a separate
reporting metric, but that still must not count as parser-behavior readiness
unless it verifies a specific parser behavior under a new contract.

### `mythic_edge.private_log_report_only_drift`

`mythic_edge.private_log_report_only_drift` remains blocked by private evidence
and excluded from parser-behavior applicability. It is local/private drift
review evidence, not a parser-behavior fixture target. It must stay governed by
#434 and private-evidence execution contracts.

### `mythic_edge.analytics_readiness_labels`

`mythic_edge.analytics_readiness_labels` remains analytics/reporting metadata.
It must not become analytics truth, statistical validity, AI truth, coaching
truth, production readiness, or parser-behavior readiness.

## Future Metric Recommendation

Future implementation is recommended, but only as an additive derived reporting
change.

Codex C should add applicability-aware metrics in a future implementation
thread if this contract is accepted. The implementation should:

- derive applicability classes from hard-coded family sets or a deterministic
  repo-owned mapping in `corpus_parity_report.py`;
- preserve existing coverage status vocabulary;
- preserve existing manifest and session-ledger contents;
- preserve existing top-level `summary` and `readiness_metrics` keys;
- add an additive nested object such as
  `readiness_metrics.behavior_applicability`;
- keep all current all-family readiness metrics backward compatible;
- test the current observed counts at the base state:
  - `parser_behavior_applicable_family_count: 37`
  - `parser_behavior_applicable_ready_family_count: 19`
  - `parser_behavior_applicable_not_ready_family_count: 18`
  - `parser_behavior_not_applicable_family_count: 8`
  - `parser_behavior_applicable_report_only_family_count: 13`
  - `parser_behavior_applicable_blocked_private_evidence_family_count: 1`
  - `parser_behavior_applicable_blocked_external_boundary_family_count: 4`
  - `parser_behavior_applicability_ready: false`

Future implementation should not:

- use the existing `not_applicable` coverage status for these rows without a
  separate schema/status migration contract;
- remove non-behavior rows from the visible matrix;
- hide blocked or report-only rows;
- change coverage statuses;
- create fixtures;
- promote private or external rows;
- claim parser support or tracker completion.

## #388 / #381 Activation Semantics

#388 and #381 remain deferred by default.

Existing `pipeline_activation_ready_for_issue_388` must remain unchanged in the
first applicability-aware implementation. It is the legacy all-family strict
gate and is false at the observed base.

Future implementation may add a separate review-only signal such as:

```yaml
readiness_metrics:
  behavior_applicability:
    parser_behavior_applicability_ready: false
```

That signal must not activate #388 or #381 by itself.

Issue #388 / #381 may start only when at least one of these conditions is met:

1. the existing `pipeline_activation_ready_for_issue_388` becomes `true`; or
2. a later explicit issue and contract amends #388 to use applicability-aware
   semantics, and the user explicitly approves starting #388 or #381 under that
   amended gate.

At the observed base, neither condition is met. Neither
`classification_complete: true`, `missing: 0`, nor a non-behavior denominator
carve-out is enough to start #388 or #381.

## Inputs

Allowed inputs:

- committed corpus manifest metadata;
- committed session-ledger metadata;
- existing corpus parity report matrix and readiness metrics;
- existing corpus contracts and handoffs;
- GitHub issue metadata for #158, #388, #381, #434, #475, #476, and #477;
- public external taxonomy only through already committed summary/category
  references.

Forbidden inputs:

- private Player.log files;
- UTC_Log files;
- raw log lines;
- private app-data contents;
- private smoke outputs;
- live MTGA checks;
- Alchemy, Conjure, Spellbook, firewall, network, packet, OS/router, or
  private smoke checks;
- exact private paths;
- raw hashes;
- runtime logs;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs;
- decklists, card choices, private strategy notes, or private reports;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size lists, capture-date row lists, parser source,
  or external corpus contents.

## Outputs

Allowed output for this Codex B pass:

- this contract file;
- a workflow handoff to Codex C, if implementation is selected;
- optional future review report.

Future Codex C output, if separately authorized:

- additive derived metrics and tests;
- implementation handoff;
- contract-test report.

Forbidden output:

- changed parser code;
- changed parser behavior;
- changed coverage status vocabulary;
- changed corpus manifest or session-ledger status;
- new fixtures;
- private evidence artifacts;
- generated data;
- runtime artifacts;
- readiness claims;
- #388 or #381 activation;
- tracker closure.

## Required Guarantees

- Applicability-aware metrics must be derived, not independently authored.
- Existing all-family readiness metrics must remain backward compatible.
- Non-behavior rows must stay visible and separately counted.
- `session.ledger_metadata` remains committed metadata, not parser behavior.
- `covered_report_only` must not count as behavior-ready.
- Private-evidence rows must remain gated by #434 and local-only contracts.
- External-boundary rows must remain blocked until owned evidence or a reduced
  synthetic model is separately contracted.
- Applicability-aware metrics must not start #388 / #381 by themselves.
- Corpus reports must not decide parser truth, merge readiness, deploy
  readiness, tracker completion, gameplay advice, analytics truth, AI truth,
  coaching truth, release readiness, or production behavior.

## Unknowns

- Whether #388 will eventually keep the all-45-family gate or explicitly adopt
  an applicability-aware gate.
- Whether `mythic_edge.live_diagnostics` should receive a future private/local
  evidence reporting metric outside parser-behavior readiness.
- Whether future private-log drift work will remain permanently
  non-behavior-applicable or split into a parser-behavior sub-row and a
  reporting sub-row.
- Whether the applicability mapping should eventually live in manifest metadata
  instead of report code. This contract recommends code-derived mapping first
  to avoid manifest churn.

## Suspected Gaps

- The current readiness metric is safe but blunt: it prevents premature
  readiness claims, but it pressures non-behavior rows into the same denominator
  as parser-behavior rows.
- Some report-only rows are real behavior gaps, while others are permanent
  governance/reporting concepts. The current metrics do not show that
  difference.
- The pipeline activation gate should remain strict until a later issue
  deliberately amends it.

## Invariants

- `parser_behavior_ready` remains false at the observed base.
- `pipeline_activation_ready_for_issue_388` remains false at the observed base.
- `parser_behavior_applicability_ready` must be false at the observed base.
- #388 and #381 remain deferred unless their start gate is explicitly met or
  the user explicitly reorders the lane under an amended contract.
- #434 remains the parent gate for private-evidence rows.
- No raw/private/external corpus evidence is committed by this contract.
- No report-only row becomes behavior-ready without `parser_behavior_verified`
  under a dedicated contract.

## Error Behavior

If implementation needs new coverage status vocabulary, route back to Codex B.

If implementation needs manifest/session-ledger changes, route back to Codex B.

If implementation requires private/live data, stop and record the blocked
condition. Do not run private/live checks.

If a future implementation excludes private-evidence or external-boundary rows
from visibility, treat that as a blocking contract violation.

If #388 or #381 would start while both the legacy gate and any explicitly
amended gate are false, stop and route to the user.

If any proposed implementation would claim full corpus parity, release
readiness, deploy readiness, production readiness, analytics truth, AI truth,
coaching truth, or tracker completion, stop and route back to Codex B.

## Side Effects

Contract pass side effect:

- adds
  `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`

Future Codex C side effects authorized only if implementation is selected:

- updates report-derived metrics and tests;
- creates implementation handoff and contract-test report.

No runtime side effects are authorized.

## Dependency Order

1. Preserve current corpus manifest and session-ledger state.
2. Add derived applicability mapping and metrics in `corpus_parity_report.py`.
3. Update focused tests for the report object.
4. Run docs, lint, whitespace, secret, and protected-surface checks.
5. Write Codex C handoff and Codex E report artifacts.
6. Only after this lane is reviewed should the workflow return to
   `core_gameplay.draft_with_games` or another selected behavior-uplift child.

## Compatibility

Backward compatibility requirements:

- Existing `summary` keys stay unchanged.
- Existing `readiness_metrics` keys stay unchanged.
- Existing `status` values stay unchanged.
- Existing coverage matrix rows stay unchanged.
- Existing coverage status vocabulary stays unchanged.
- Existing CLI exit-code behavior stays unchanged.

Adding `readiness_metrics.behavior_applicability` is an additive report schema
extension. If Codex C decides the readiness metrics schema version must change,
it must state that in the implementation handoff and keep existing consumers
backward compatible.

## Tests Required

For this contract-only pass:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Path-scoped checks:

```bash
printf '%s\n' docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Future Codex C must run the same checks and add focused assertions for:

- 8 non-behavior-applicability excluded rows;
- 37 behavior-applicable rows;
- 19 behavior-applicable ready rows;
- 18 behavior-applicable not-ready rows;
- #388 / #381 activation remains false at the observed base;
- existing all-family readiness metrics remain unchanged.

No private/live checks are allowed.

## Acceptance Criteria

- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
  exists.
- The contract classifies all 45 corpus rows.
- The contract identifies exactly 8 non-behavior-applicability excluded rows at
  the observed base.
- The contract recommends additive applicability-aware metrics.
- The contract preserves existing all-family readiness metrics.
- The contract keeps #388 and #381 deferred by default.
- The contract does not promote report-only, private-evidence, or
  external-boundary rows.
- The contract preserves parser truth, private evidence, analytics, AI,
  coaching, readiness, and production non-claims.

## Next Workflow Action

Recommended next role: Codex C: Module Implementer, if the user wants the
additive report metrics implemented next.

If the user wants independent review before implementation, route to Codex E
with this same contract.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #477.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/477

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/475

Previous completed PR:
https://github.com/Tahjali11/Mythic-Edge/pull/476

Previous merge commit:
ad222e4bad8209a6baad631f1769ad273ff031b0

Base branch:
main

Contract:
docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md

Goal:
Implement the smallest additive corpus parity report/test change needed to expose parser-behavior readiness applicability semantics. Preserve existing all-family readiness metrics, corpus statuses, fixtures, and #388/#381 gates.

Do:
- Compare current report implementation against the contract before editing.
- Add derived applicability-aware metrics, preferably under `readiness_metrics.behavior_applicability`.
- Classify all 45 corpus rows exactly as contracted at the observed base.
- Keep existing `summary`, `readiness_metrics`, status, matrix, and CLI behavior backward compatible unless the contract explicitly allows additive wording.
- Add focused tests in `tests/test_corpus_parity_report.py`.
- Write `docs/implementation_handoffs/parser_corpus_behavior_readiness_applicability_semantics_comparison.md`.
- Write `docs/contract_test_reports/parser_corpus_behavior_readiness_applicability_semantics.md`.

Do not:
- Change corpus manifest or session-ledger statuses.
- Change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics, golden replay, feature-equity, drift, evidence-ledger, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, release readiness, production behavior, CI gates, merge readiness, deploy readiness, or final integration policy.
- Promote report-only, private-evidence, or external-boundary rows.
- Create fixtures.
- Run private Player.log, UTC_Log, app-data, live MTGA, Alchemy, network, firewall/drop, packet, OS/router, or private smoke checks.
- Activate #388 or #381.
- Claim parser support, full corpus parity, private smoke success, release readiness, production behavior, analytics truth, AI truth, coaching truth, or tracker completion.

Validation:
- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
- `python3 tools/check_agent_docs.py`
- `python3 -m ruff check src tests tools`
- `git diff --check`
- path-scoped secret/private-marker scan
- path-scoped protected-surface scan
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/477"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/475"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/476"
  previous_merge_commit: "ad222e4bad8209a6baad631f1769ad273ff031b0"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #477"
  target_artifact: "docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md"
  verdict: "parser_behavior_readiness_applicability_semantics_contract_ready"
  risk_tier: "High"
  branch: "codex/parser-corpus-behavior-readiness-applicability-477"
  base_branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  recommended_implementation: "additive_applicability_aware_readiness_metrics"
  expected_current_counts:
    total_scenario_families: 45
    parser_behavior_applicable_family_count: 37
    parser_behavior_applicable_ready_family_count: 19
    parser_behavior_applicable_not_ready_family_count: 18
    parser_behavior_not_applicable_family_count: 8
  recommended_after_implementation:
    - "Codex E review / contract test"
    - "Return to Codex A for core_gameplay.draft_with_games behavior uplift after metrics are reviewed"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close tracker #388 or parent #434."
    - "Do not promote blocked or report-only rows by default."
    - "Do not change corpus manifest or session-ledger statuses in this lane."
    - "Do not start #388 or #381 unless the legacy gate is true or a later explicit contract amends the gate and the user approves starting it."
    - "Do not claim parser support, full corpus parity, private smoke success, release readiness, production behavior, analytics truth, AI truth, coaching truth, or tracker completion."
```
