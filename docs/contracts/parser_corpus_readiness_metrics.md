# Parser Corpus Readiness Metrics Contract

## Module

Parser corpus readiness metrics for the corpus parity report.

Plain English: this contract separates "the corpus taxonomy has been
classified" from "Mythic Edge has committed parser-behavior evidence." Zero
missing rows are useful map-completion evidence, but they must not imply full
corpus parity, parser support, readiness, production behavior, analytics
truth, AI truth, coaching truth, or authorization to start the parser-evidence
pipeline.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/462
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/464
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/466
- Previous merge commit: `de988ffba7e960ec13d85ee13e87157be6f202e0`
- Base branch inspected: `main`
- Contract branch: `codex/parser-corpus-readiness-metrics-462`
- Risk tier: Medium-High
- Status: contract only

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
- `docs/contracts/parser_corpus_manifest_metadata_residual.md`
- `docs/contracts/parser_corpus_confidence_finality_degradation_residual.md`
- `docs/contracts/parser_corpus_workbook_row_coverage_residual.md`
- `docs/contracts/parser_corpus_analytics_readiness_labels_coverage.md`
- `docs/contracts/parser_corpus_gameplay_conjure_external_boundary.md`
- `docs/contracts/parser_corpus_gameplay_spellbook_external_boundary.md`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- issue #388 and child issue #381, as deferred pipeline context only

## Purpose

Issue #462 addresses a reporting ambiguity:

```text
Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 0 missing)
```

That headline can be misread as readiness because it highlights zero missing
rows while hiding synthetic, report-only, private-evidence, and external-boundary
counts. The current map is classified, but it is not behavior-ready:

- `covered_committed`: 6
- `covered_synthetic`: 14
- `covered_report_only`: 19
- `blocked_private_evidence`: 2
- `blocked_external_boundary`: 4
- `partial`: 0
- `missing`: 0
- `deferred`: 0
- total families: 45

This contract authorizes a narrow report/readability implementation that makes
that distinction machine-readable and visible.

## Scope Decision

Implementation should proceed as a report wording and summary-metrics change.

Codex C may update:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `docs/project_roadmap.md`, only if a small wording note is needed to avoid
  readiness overclaims
- `docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md`
- `docs/contract_test_reports/parser_corpus_readiness_metrics.md`

Codex C must not update:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- corpus coverage statuses or coverage basis values
- parser behavior or parser-owned facts
- private-evidence rows, external-boundary rows, or fixture contents
- tracker #388 or child issue #381 implementation state

If Codex C discovers that the report cannot express the required metrics
without schema/version ambiguity, it should route back to Codex B rather than
silently changing corpus vocabulary.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns derived readiness metrics and report wording for corpus
parity. It does not own parser behavior, parser correctness, coverage status,
fixture promotion, private evidence, analytics truth, release readiness,
deploy readiness, production behavior, or tracker completion.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting: Quality / Governance for contract, validation, protected-surface
checks, and wording that prevents workflow overclaims.

This slice is not a Parser module, parser-evidence pipeline module, private
evidence module, analytics module, AI module, coaching module, CI gate, merge
gate, deploy gate, release gate, or production module.

## Truth Owner

Truth owner for corpus coverage rows remains:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for the new readiness metric derivation:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- this contract

Truth boundary:

- Corpus parity may report classification completeness and evidence-strength
  metrics.
- Parser modules, router dispatch, parser events, parser state, match/game
  identity, deduplication, and final reconciliation remain parser-owned truth.
- Private Player.log checks, UTC_Log checks, firewall/drop checks, live MTGA
  checks, app-data checks, local runtime artifacts, and private smoke outputs
  remain outside this committed report.
- Public external taxonomy remains external reference context only.
- Analytics, workbook, Google Sheets, Apps Script, webhook transport, local app,
  Match Journal, overlay, AI/model-provider behavior, coaching, CI, merge,
  deploy, production, and tracker lifecycle remain downstream or out of scope.

## Bridge-Code Status

`not_bridge_code`

This contract does not authorize bridge code. It authorizes derived reporting
inside the existing corpus parity report.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_readiness_metrics.md`

Future Codex C files authorized by this contract:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md`
- `docs/contract_test_reports/parser_corpus_readiness_metrics.md`
- optional small wording change in `docs/project_roadmap.md`

Files Codex C may read but must not modify in this slice:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- recent parser-corpus contracts, handoffs, and reports
- GitHub issues #158, #388, #381, #434, #462, and #464

Not owned by this contract:

- parser modules;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- diagnostics, golden replay, feature-equity, drift, evidence-ledger, or
  analytics implementation behavior;
- corpus manifest or session-ledger status promotion;
- private/local artifacts;
- external corpus contents;
- workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, runtime status files, failed posts, workbook exports,
  generated data, CI gates, merge readiness, deploy readiness, production
  behavior, or tracker completion.

## Public Interface

Codex C may add a new top-level report section:

```text
readiness_metrics
```

The section must be deterministic and derived only from the already-built
coverage matrix and summary counts.

Required object shape:

```yaml
readiness_metrics:
  schema_version: "parser_corpus_readiness_metrics.v1"
  classification_complete: true
  parser_behavior_ready: false
  parser_behavior_ready_family_count: 20
  total_scenario_families: 45
  committed_parser_behavior_families: 6
  synthetic_parser_behavior_families: 14
  report_only_families: 19
  blocked_families: 6
  blocked_private_evidence_families: 2
  blocked_external_boundary_families: 4
  missing_families: 0
  partial_families: 0
  deferred_families: 0
  pipeline_activation_ready_for_issue_388: false
  pipeline_activation_blockers:
    - "report_only_families:19"
    - "blocked_private_evidence_families:2"
    - "blocked_external_boundary_families:4"
  readiness_verdict: "classification_complete_not_behavior_ready"
  competitive_core:
    schema_version: "parser_corpus_competitive_core.v1"
    status: "not_behavior_ready"
    total_families: 16
    parser_behavior_ready_family_count: 8
    report_only_family_count: 5
    blocked_family_count: 3
```

The exact current counts above are expected at
`de988ffba7e960ec13d85ee13e87157be6f202e0`. If upstream changes land before
Codex C runs, Codex C must calculate the live counts from the matrix and
explain any drift in its handoff.

### Classification Completeness

`classification_complete` must mean:

- `missing == 0`
- `partial == 0`
- `deferred == 0`

It must not mean parser readiness, fixture adequacy, production readiness,
analytics readiness, AI readiness, or tracker completion.

### Parser Behavior Readiness

`parser_behavior_ready` must be `true` only when all scenario families are
covered by one of:

- `covered_committed`
- `covered_synthetic`

and no family remains:

- `covered_report_only`
- `partial`
- `missing`
- `deferred`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `not_applicable`

`covered_report_only` is not parser-behavior readiness.

`covered_committed` and `covered_synthetic` count as parser-behavior-ready only
when their coverage basis includes `parser_behavior_verified`.

### Parser-Evidence Pipeline Activation

`pipeline_activation_ready_for_issue_388` must mirror issue #388's start
condition and be `true` only when all 45 parser corpus families have
`covered_synthetic` or stronger parser-behavior evidence.

Current expected value: `false`.

This metric is advisory workflow evidence. It does not open, start, implement,
close, or mutate issue #388 or child issue #381 by itself.

### Competitive Core V1

The report may include a fixed advisory `competitive_core` aggregate to help
humans see whether player-facing match/game coverage is ready. It must not be a
release gate, deploy gate, analytics gate, AI gate, coaching gate, or tracker
completion gate.

Initial `competitive_core.v1` family list:

- `core_gameplay.standard_bo1`
- `core_gameplay.standard_bo3`
- `core_gameplay.traditional_bo3`
- `core_gameplay.draft_with_games`
- `core_gameplay.sealed_matches`
- `gameplay_stress.mulligan`
- `gameplay_stress.opponent_auto_concede`
- `gameplay_stress.conjure`
- `gameplay_stress.spellbook`
- `gameplay_stress.companion_or_large_deck`
- `gameplay_stress.action_attribution`
- `gameplay_stress.event_ordering`
- `timer.active_player_timer`
- `timer.pre_match_idle`
- `timer.inactivity_timeout`
- `drift_debug.gsm_truncation`

Competitive core status values:

- `behavior_ready`: every family in the list is `covered_committed` or
  `covered_synthetic` with `parser_behavior_verified`.
- `classification_complete_not_behavior_ready`: the list has no `missing`,
  `partial`, or `deferred` families, but at least one family is report-only or
  blocked.
- `not_classified`: at least one family is `missing`, `partial`, or `deferred`.

Current expected value:

```yaml
status: "classification_complete_not_behavior_ready"
total_families: 16
parser_behavior_ready_family_count: 8
report_only_family_count: 5
blocked_family_count: 3
```

If Codex C calculates different current counts, it must explain why.

### CLI Output

Codex C should update the CLI one-line output so it no longer suggests that
zero missing rows are enough.

Required content:

- total family count
- committed count
- synthetic count
- report-only count
- blocked count, with private and external detail
- missing count
- parser-behavior-ready yes/no

Acceptable example:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=14, report_only=19, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Codex C may choose equivalent wording if tests assert the important fields.

## Inputs

Allowed inputs:

- committed corpus manifest metadata;
- committed session-ledger metadata;
- existing corpus parity report matrix;
- existing corpus parity summary counts;
- existing issue #388 start-condition text;
- existing contracts and reports listed above.

Forbidden inputs:

- private Player.log files;
- UTC_Log files;
- raw log lines;
- private app-data contents;
- private smoke outputs;
- live MTGA checks;
- firewall/drop/network/packet/OS/router checks;
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

Allowed outputs:

- a new contract file;
- a derived `readiness_metrics` object in the corpus parity report;
- clearer CLI output;
- focused tests for the metrics and wording;
- optional small roadmap wording clarification;
- Codex C/E workflow artifacts.

Forbidden outputs:

- changed parser behavior;
- changed corpus coverage status or basis;
- changed corpus manifest or session-ledger data;
- new private evidence artifacts;
- raw or private evidence;
- fixture promotion;
- generated data;
- runtime artifacts;
- readiness claims;
- issue #388 or #381 activation;
- tracker #158 completion.

## Required Guarantees

- Existing `summary` counts remain present for backward compatibility.
- Existing top-level `status` semantics remain unchanged.
- The new metrics must be derived, not independently authored.
- `covered_report_only` must never count as parser-behavior-ready.
- Blocked private-evidence rows and blocked external-boundary rows must be
  counted separately.
- The report must explicitly expose that current parser-behavior-ready coverage
  is 20 of 45 families at the observed base.
- The report must expose that issue #388 activation is not ready at the
  observed base.
- The report must preserve the statement that corpus reports do not decide
  merge readiness, deploy readiness, tracker completion, gameplay advice,
  analytics truth, AI truth, coaching truth, or production behavior.

## Unknowns

- Whether `competitive_core.v1` is the right long-term family set for future
  player-facing readiness language.
- Whether later sanitized fixture promotion will make a separate
  `covered_behavior_private_reviewed` vocabulary useful. This contract does
  not add that vocabulary.
- Whether #388 should eventually use a stricter condition than "covered
  synthetic or stronger" once private-evidence and external-boundary rows have
  evidence plans.
- Whether docs outside `docs/project_roadmap.md` need wording cleanup. Codex C
  should keep this first pass narrow.

## Suspected Gaps

- The current CLI headline can be overread because it displays missing and
  committed counts but not synthetic, report-only, or blocked counts.
- Existing `summary` counts are correct but not semantically grouped around
  readiness.
- The corpus map currently has many report-only families that are classified
  but not parser-behavior evidence.
- Issue #388 has a stricter start condition than the current report headline
  makes obvious.

## Invariants

- Coverage status vocabulary remains unchanged.
- Corpus manifest and session ledger contents remain unchanged in this slice.
- Parser behavior remains unchanged.
- Parser-evidence pipeline issues #381 through #388 remain deferred until the
  readiness metric says the start condition is met or the user explicitly
  reorders the lane.
- Private-evidence and external-boundary rows remain governed by their own
  contracts.
- Readiness metrics are review metadata, not parser truth or release truth.

## Error Behavior

If implementation needs new coverage status vocabulary, route back to Codex B.

If implementation needs manifest/session-ledger changes, route back to Codex B.

If implementation requires private/live data, stop and record the blocked
condition. Do not run private/live checks.

If `pipeline_activation_ready_for_issue_388` would be `true` while any row is
`covered_report_only`, `blocked_private_evidence`, `blocked_external_boundary`,
`partial`, `missing`, or `deferred`, treat that as a blocking bug.

If `parser_behavior_ready` would be `true` while any family lacks
`parser_behavior_verified`, treat that as a blocking bug.

If any proposed implementation would claim full corpus parity, release
readiness, deploy readiness, production readiness, analytics truth, AI truth,
coaching truth, or tracker completion, stop and route back to Codex B.

## Side Effects

Contract pass side effect:

- adds `docs/contracts/parser_corpus_readiness_metrics.md`

Future Codex C side effects authorized by this contract:

- updates report-derived metrics and CLI wording;
- updates focused tests;
- optionally updates narrow roadmap wording;
- creates implementation handoff and contract-test report.

No runtime side effects are authorized.

## Dependency Order

1. Preserve current corpus manifest and session-ledger state.
2. Add derived readiness metrics in `corpus_parity_report.py`.
3. Update focused tests for the report object and CLI output.
4. Optionally update `docs/project_roadmap.md` wording if needed.
5. Write Codex C handoff and Codex E report artifacts.

## Compatibility

Backward compatibility requirements:

- Existing `summary` keys stay unchanged.
- Existing `status` values stay unchanged.
- Existing coverage matrix rows stay unchanged.
- Existing privacy and protected-surface sections stay unchanged.
- Existing CLI exit-code behavior stays unchanged.

Adding `readiness_metrics` is an additive report schema extension under the
current report object. If Codex C decides the report schema version must change,
it must state that in the implementation handoff and keep consumers backward
compatible.

## Tests Required

Codex C must run:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Codex C should also run path-scoped checks:

```bash
printf '%s\n' docs/contracts/parser_corpus_readiness_metrics.md src/mythic_edge_parser/app/corpus_parity_report.py tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md docs/contract_test_reports/parser_corpus_readiness_metrics.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_readiness_metrics.md src/mythic_edge_parser/app/corpus_parity_report.py tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md docs/contract_test_reports/parser_corpus_readiness_metrics.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

If Codex C updates `docs/project_roadmap.md`, include it in the path-scoped
checks.

## Acceptance Criteria

- `docs/contracts/parser_corpus_readiness_metrics.md` exists.
- The contract authorizes only derived report metrics and wording changes.
- Codex C can add a `readiness_metrics` section without changing corpus
  coverage statuses.
- The report distinguishes classification completeness from parser-behavior
  readiness.
- The report distinguishes committed, synthetic, report-only, private-blocked,
  external-blocked, missing, partial, and deferred counts.
- The report exposes issue #388 pipeline activation readiness as false at the
  observed base.
- CLI output includes more than committed and missing counts.
- Tests prevent zero missing rows from implying behavior readiness.
- Protected-surface and private-artifact boundaries are preserved.

## Next Workflow Action

Recommended next role: Codex C: Module Implementer.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #462.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/462

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related parser-evidence pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/464

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/466

Previous merge commit:
de988ffba7e960ec13d85ee13e87157be6f202e0

Base branch:
main

Contract:
docs/contracts/parser_corpus_readiness_metrics.md

Goal:
Implement the smallest corpus parity report/test/docs change needed to separate classification completeness from committed/synthetic parser-behavior readiness. Do not change corpus manifest/session-ledger statuses or parser behavior.

Do:
- Add derived readiness metrics to src/mythic_edge_parser/app/corpus_parity_report.py.
- Keep existing summary and status semantics backward compatible.
- Update CLI wording so zero missing rows is not the main readiness signal.
- Add focused tests in tests/test_corpus_parity_report.py.
- Optionally add a small docs/project_roadmap.md wording note if needed.
- Write docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md.
- Write docs/contract_test_reports/parser_corpus_readiness_metrics.md.

Do not:
- Change tests/fixtures/parser_corpus/corpus_manifest.v1.json.
- Change tests/fixtures/parser_corpus/session_ledger.v1.json.
- Promote coverage statuses.
- Add fixture coverage.
- Start issue #388 or issue #381.
- Run private Player.log, UTC_Log, app-data, firewall/drop, network, live MTGA, or private smoke checks.
- Change parser behavior, parser state final reconciliation, parser event classes, router semantics, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, coaching truth, CI gates, merge readiness, deploy readiness, production behavior, or tracker completion policy.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/462"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/464"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/466"
  previous_merge_commit: "de988ffba7e960ec13d85ee13e87157be6f202e0"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #462"
  target_artifact: "docs/contracts/parser_corpus_readiness_metrics.md"
  expected_next_artifacts:
    - "docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md"
    - "docs/contract_test_reports/parser_corpus_readiness_metrics.md"
  verdict: "readiness_metrics_contract_ready_for_implementation"
  risk_tier: "Medium-High"
  branch: "codex/parser-corpus-readiness-metrics-462"
  base_branch: "main"
  implementation_scope: "derived corpus report metrics, CLI wording, focused tests, optional roadmap wording"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not change corpus manifest or session-ledger statuses in this issue."
    - "Do not change parser behavior or parser-owned truth."
    - "Do not start #388 or #381 from zero-missing evidence alone."
    - "Do not run private/live/UTC_Log/Player.log/firewall/network checks."
    - "Do not claim full corpus parity, parser support, private smoke success, release readiness, deploy readiness, production behavior, analytics truth, AI truth, coaching truth, or tracker completion."
```
