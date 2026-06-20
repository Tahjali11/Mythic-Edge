# Parser Corpus Unknown Entry Behavior Readiness Contract

## Module

`log_runtime.unknown_entry` parser corpus behavior-readiness framing.

Plain English: Mythic Edge already records unknown-entry coverage as
report-only drift/diagnostics/evidence-ledger metadata from issue #377. This
contract defines the narrowest safe path for moving the row toward behavior
readiness: reduced synthetic router, drift, diagnostics, and evidence-ledger
review evidence only. The uplift may prove that existing repo-owned behavior
tracks and reports unknown entries without treating them as parser-understood
facts. It must not claim parser support for unknown semantic content,
automatic parser-gap issue creation, trusted parser input, live drift health,
diagnostics readiness, release readiness, production behavior, analytics
truth, AI truth, coaching truth, tracker completion, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/504
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/502
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/503
- Previous merge commit: `7fd62e893f8fd5e7e783e8a0b9e3eea374e485ae`
- Prior report-only boundary issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/377
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-unknown-entry-behavior-readiness-504`
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
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_corpus_missing_message_type_behavior_uplift.md`
- `docs/contracts/parser_corpus_log_runtime_rotation_behavior_readiness.md`
- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_router_unit.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_evidence_ledger.py`

## Purpose

Define the next safe behavior-readiness step for
`log_runtime.unknown_entry`.

This contract answers:

- whether the row may move from `covered_report_only` toward
  `covered_synthetic`;
- what reduced synthetic unknown-entry behavior evidence is sufficient;
- what `parser_behavior_verified` may and may not mean for this row;
- why `parser_event_families` must remain empty; and
- how issue #388 / issue #381 activation remains deferred.

This contract does not implement code, create or change runtime fixtures, edit
corpus metadata, run private/live MTGA checks, activate the parser-evidence
pipeline, or claim unknown-entry support beyond the reduced synthetic review
packet for router, drift, diagnostics, and evidence-ledger behavior.

## Observed Current Behavior

Observed on `main` at
`7fd62e893f8fd5e7e783e8a0b9e3eea374e485ae`:

- Issue #504 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #502 is complete after PR #503.
- The current corpus parity report prints:

```text
Corpus parity report: partial_coverage_map_ready
(45 families; committed=6, synthetic=21, report_only=12,
blocked=6 [private=2, external=4], missing=0,
parser_behavior_ready=no)
```

Current `log_runtime.unknown_entry` row:

```yaml
scenario_family: "log_runtime.unknown_entry"
coverage_status: "covered_report_only"
coverage_basis:
  - "diagnostics_only"
  - "fixture_metadata_only"
  - "evidence_ledger_only"
mythic_edge_entries:
  - "unknown_entry_drift_report_reference_v1"
parser_event_families: []
parser_claim_families:
  - "router_unknown_entry_count"
  - "drift_unknown_signature_review_samples"
  - "drift_unmatched_api_name_review_samples"
  - "diagnostics_unknown_entries_review_status"
  - "evidence_ledger_unknown_entry_count_boundary"
  - "unknown_entry_privacy_boundary"
```

Current repo behavior:

- `Router.route(...)` increments `RouterStats.unknown` when parser dispatch
  returns no events.
- `tests/test_router_unit.py` already exercises unrouted-entry unknown-count
  behavior.
- `build_player_log_drift_report(...)` counts unknown entries, records unknown
  signatures and unmatched API names, computes unknown rate, and returns
  `status == "review"` when unknown evidence is present.
- `tests/test_log_drift_sensor.py` already exercises drift report unknown
  counts, unmatched API-name samples, baseline deltas, reference fixture
  normalization, and privacy-oriented signature behavior.
- `build_parser_diagnostics_report(...)` surfaces unknown/degraded evidence as
  `review`, copies bounded unknown signatures/API-name review samples, and
  summarizes `summary.unknown_entries`.
- `tests/test_parser_diagnostics_mode.py` already exercises review status and
  redaction for an unknown signature containing sensitive-looking data.
- `evidence_ledger.py` seeds Tier 6
  `tier6.runtime_health_and_drift_detection.unknown_entry_count`, documenting
  router/drift/diagnostics sources as run-scoped review evidence.
- `tests/test_evidence_ledger.py` already verifies the Tier 6 unknown-entry
  count signals and invariants.

Current non-evidence:

- The issue #377 boundary explicitly says unknown-entry coverage is report
  evidence, not parser support for unknown semantic content.
- Unknown entries do not emit trusted parser events.
- Unknown signatures and unmatched API names are review samples, not trusted
  parser inputs.
- A nonzero unknown count is not live drift health, and a zero unknown count is
  not global no-drift proof.
- `drift_debug.missing_message_type` remains separate and was uplifted only
  through missing/blank type fallback and GameState default-preservation
  evidence in issue #500.
- `log_runtime.rotation` remains separate and was uplifted only through tailer
  and stream rotation behavior evidence in issue #502.
- `drift_debug.rename_or_rotation_collision`,
  `mythic_edge.private_log_report_only_drift`, private-evidence rows, and
  external-boundary rows must not be reinterpreted by this issue.

## Scope Decision

Recommended future path: reduced synthetic unknown-entry behavior uplift.

A later Codex C implementation may move `log_runtime.unknown_entry` from
`covered_report_only` toward `covered_synthetic` with
`parser_behavior_verified` only if it adds corpus metadata and tests tying the
row to a reduced synthetic review-behavior packet:

1. Router unknown-count behavior for an unrouted synthetic entry.
2. Drift report unknown-count and sanitized review-sample behavior.
3. Diagnostics unknown/degraded review status and redaction behavior.
4. Evidence-ledger Tier 6 unknown-entry-count provenance invariants.

The reduced packet proves only that Mythic Edge has deterministic, repo-owned
behavior for accounting for and reviewing unknown entries. It must not claim
that unknown entries are understood, safe to ignore, parser-supported, or
semantically classified.

The behavior claim is intentionally small:

- unknown accounting and review behavior, not unknown semantic parsing;
- bounded report samples, not raw log evidence;
- diagnostics review status, not diagnostics readiness;
- evidence-ledger provenance, not runtime truth;
- existing repo-owned tests and metadata, not live/private evidence.

This contract authorizes a metadata/test/docs implementation path. It does not
authorize router, parser, diagnostics, drift, evidence-ledger, golden replay,
feature-equity, runtime, workbook, webhook, Apps Script, analytics, AI,
coaching, CI, merge, deploy, production, or final integration behavior
changes. If Codex C cannot prove the reduced packet without behavior changes,
the row must remain `covered_report_only` and route back to Codex B or Codex
A.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- `src/mythic_edge_parser/router.py` owns current `RouterStats.unknown`
  behavior.
- `src/mythic_edge_parser/app/log_drift_sensor.py` owns current drift report
  unknown counts, unknown signatures, unmatched API names, and baseline delta
  review evidence.
- `src/mythic_edge_parser/app/parser_diagnostics.py` owns current diagnostics
  unknown/degraded review status.
- `src/mythic_edge_parser/app/evidence_ledger.py` owns current Tier 6
  unknown-entry-count provenance vocabulary.
- Corpus parity owns status aggregation and readiness metrics.

This contract does not move truth ownership to corpus metadata, diagnostics
summaries, drift samples, workbook formulas, dashboards, Apps Script, webhook
transport, analytics, AI, coaching, readiness, deploy, production, or tracker
lifecycle surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser / Router, as the existing producer of routed/unknown entry counts.
- Parser Diagnostics / Drift, as existing review-report consumers of router
  counts.
- Evidence Ledger / Provenance, as existing provenance vocabulary for
  run-scoped unknown-entry-count evidence.

This contract is not a parser behavior module in the sense of adding
understanding for unknown entries. It is a corpus-readiness contract for
existing unknown accounting and review behavior.

## Truth Owner

Truth owner for corpus coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for the reduced behavior evidence:

- Router unknown behavior:
  - `src/mythic_edge_parser/router.py`
  - `tests/test_router_unit.py`
- Drift unknown review behavior:
  - `src/mythic_edge_parser/app/log_drift_sensor.py`
  - `tests/test_log_drift_sensor.py`
- Diagnostics unknown review behavior:
  - `src/mythic_edge_parser/app/parser_diagnostics.py`
  - `tests/test_parser_diagnostics_mode.py`
- Evidence-ledger unknown-count provenance:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `tests/test_evidence_ledger.py`

Truth boundary:

- `RouterStats.unknown` is a count of entries that produced no parser events
  in one router pass.
- Drift unknown signatures and unmatched API names are bounded review samples.
- Diagnostics unknown/degraded status is a review classifier for one analyzed
  source/report.
- Evidence-ledger `unknown_entry_count` is run-scoped provenance.
- Corpus parity may claim behavior-readiness only for the reduced accounting
  and review packet.
- Corpus parity must not claim parser-understood semantic content, trusted
  parser input, automatic parser-gap issue creation, live drift health,
  diagnostics readiness, release readiness, production behavior, analytics
  truth, AI truth, coaching truth, tracker completion, or full corpus parity.

## Bridge-Code Status

`bridge_code`

Source project area: Parser / Router and Diagnostics / Drift.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing router unknown-count behavior
  + existing drift unknown review samples
  + existing diagnostics unknown/degraded review status
  + existing evidence-ledger Tier 6 provenance vocabulary
  -> bounded committed corpus metadata
  -> corpus parity coverage row for log_runtime.unknown_entry
```

Forbidden reverse flow:

- Corpus metadata must not change router, parser, diagnostics, drift,
  evidence-ledger, runtime, workbook, webhook, Apps Script, analytics, AI,
  coaching, CI, merge, deploy, production, or final integration behavior.
- Corpus metadata must not turn unknown signatures or unmatched API names into
  parser facts, gameplay facts, automatic parser-gap issues, trusted parser
  inputs, analytics labels, AI prompts, coaching advice, or live health claims.

Protected surfaces explicitly not touched:

- parser behavior
- router semantics
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- diagnostics report shape
- drift report behavior
- evidence-ledger schema or vocabulary
- golden replay behavior
- feature-equity behavior
- runtime status artifacts or schema
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- local app / SQLite behavior
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

- `docs/contracts/parser_corpus_unknown_entry_behavior_readiness.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_router_unit.py`, only for a focused synthetic router evidence
  test if existing coverage is too coupled to timestamp anomalies
- `docs/implementation_handoffs/parser_corpus_unknown_entry_behavior_readiness_comparison.md`
- `docs/contract_test_reports/parser_corpus_unknown_entry_behavior_readiness.md`

Future Codex C may cite but should not need to edit:

- `tests/test_log_drift_sensor.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_evidence_ledger.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- router dispatch or `RouterStats` semantic changes
- parser event class changes
- new unknown-entry parser event kinds
- automatic parser-gap issue creation
- diagnostics report shape changes
- drift report shape changes
- evidence-ledger schema/vocabulary changes
- golden replay behavior changes
- feature-equity behavior changes
- runtime status changes
- live/private smoke execution
- committed raw log fixtures
- Manasight corpus import
- local private evidence
- issue #388 or issue #381 activation

## Public Interface

No runtime public API is added by Codex B.

Future Codex C may add corpus metadata that makes the corpus parity public
report show `log_runtime.unknown_entry` as a reduced synthetic
behavior-ready row. The intended eventual corpus row shape is:

```yaml
scenario_family: "log_runtime.unknown_entry"
coverage_status: "covered_synthetic"
coverage_basis:
  - "parser_behavior_verified"
  - "diagnostics_only"
  - "evidence_ledger_only"
  - "fixture_metadata_only"
parser_event_families: []
```

The existing report-only entry `unknown_entry_drift_report_reference_v1`
should remain as historical non-claim metadata. A new synthetic evidence entry
should be added rather than rewriting issue #377's boundary entry into a
behavior claim.

Recommended new manifest entry id:

```text
unknown_entry_synthetic_router_drift_diagnostics_v1
```

Recommended new session id:

```text
unknown_entry_synthetic_router_drift_diagnostics_v1
```

Recommended `parser_event_families`:

```yaml
parser_event_families: []
```

Rationale: unknown entries produce no trusted parser events. The verified
behavior is accounting and review behavior, not event emission.

Recommended manifest claim families:

```yaml
parser_claim_families:
  - "synthetic_router_unknown_count"
  - "synthetic_router_no_event_for_unknown_entry"
  - "synthetic_drift_unknown_count_review"
  - "synthetic_drift_unknown_signature_review_samples"
  - "synthetic_drift_unmatched_api_review_samples"
  - "synthetic_diagnostics_unknown_entries_review_status"
  - "synthetic_diagnostics_unknown_redaction_boundary"
  - "evidence_ledger_tier6_unknown_entry_count_boundary"
  - "unknown_entry_synthetic_boundary"
  - "unknown_semantic_content_non_claim"
  - "automatic_parser_gap_creation_non_claim"
  - "trusted_parser_input_non_claim"
  - "live_drift_health_non_claim"
  - "readiness_production_non_claim"
  - "analytics_ai_coaching_non_claim"
```

Recommended manifest paths:

```yaml
paths:
  router_test: "tests/test_router_unit.py"
  drift_sensor_test: "tests/test_log_drift_sensor.py"
  diagnostics_test: "tests/test_parser_diagnostics_mode.py"
  evidence_ledger_test: "tests/test_evidence_ledger.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
```

## Minimum Behavior Evidence

Future uplift requires a dedicated reduced packet. Codex C must not rely on
issue #377 report-only metadata alone.

### Router Leg

Required:

- repo-owned synthetic `LogEntry` or equivalent existing focused test only;
- parser dispatch returns no events;
- `Router.route(...)` returns `[]`;
- `RouterStats.unknown` increments by one;
- routed count does not increment;
- no parser event is emitted;
- no private Player.log, UTC_Log, live MTGA, app-data, network, packet,
  OS/router, private smoke, or external corpus input.

Preferred:

- a focused router test with a valid timestamp and no parser match, so
  unknown-count behavior is not conflated with timestamp-missing behavior.

Allowed:

- existing
  `tests/test_router_unit.py::test_route_updates_unknown_and_timestamp_missing_for_unrouted_entry`
  may be cited as partial evidence if Codex C also documents the timestamp
  anomaly coupling and either adds a narrower valid-timestamp test or explains
  why the existing test is sufficient for the reduced packet.

Not sufficient:

- parser dispatch order tests that eventually produce an event;
- truncation marker routing;
- timestamp-anomaly behavior alone;
- missing-message-type fallback behavior;
- log-runtime rotation behavior;
- private or external log evidence.

### Drift Leg

Required:

- repo-owned synthetic or already committed sanitized/count-only reference
  evidence only;
- `build_player_log_drift_report(...)` reports `entry_counts.unknown > 0`
  for unknown evidence;
- report status becomes `review` when unknown evidence is present;
- unknown signatures and unmatched API-name samples are bounded review
  samples;
- privacy-oriented normalization excludes raw private paths and raw log lines.

Allowed:

- existing
  `tests/test_log_drift_sensor.py::test_build_player_log_drift_report_surfaces_unmatched_api_names`
  may be cited for drift unknown review behavior;
- existing
  `tests/test_log_drift_sensor.py::test_drift_report_reference_matches_manifest_fixture`
  may be cited for normalized report-reference and privacy boundary behavior;
- existing
  `tests/test_log_drift_sensor.py::test_entry_signature_prefers_prefix_label_for_privacy`
  may be cited for bounded signature behavior.

Not sufficient:

- drift report shape alone with zero unknowns;
- baseline delta behavior without unknown counts or review samples;
- raw private signatures;
- public Manasight taxonomy metadata.

### Diagnostics Leg

Required:

- repo-owned synthetic or committed sanitized/count-only evidence only;
- diagnostics `unknowns_and_degradation.status == "review"` when unknown
  evidence is present;
- diagnostics `summary.unknown_entries` reflects the unknown count;
- sensitive-looking values in unknown input are not emitted in the report;
- diagnostics remains review/report behavior, not parser truth.

Allowed:

- existing
  `tests/test_parser_diagnostics_mode.py::test_unknown_signatures_produce_review_and_are_sanitized`
  may be cited if Codex C proves it still covers the required behavior.

Not sufficient:

- missing optional runtime status;
- expected-family missing behavior alone;
- diagnostics pass output;
- runtime status or transport health summaries.

### Evidence-Ledger Leg

Required:

- Tier 6 `unknown_entry_count` remains seeded and run-scoped;
- direct/fallback signals include diagnostics, drift report, router stats, and
  validation consumers as already documented;
- invariants include
  `tier6_unknown_entry_count_is_run_scoped` and
  `tier6_unknown_entries_are_review_samples_not_parser_truth`;
- unknown signatures and unmatched API names remain review samples, not
  trusted parser inputs.

Allowed:

- existing
  `tests/test_evidence_ledger.py::test_tier6_unknown_entry_count_entry_documents_run_scoped_counts`
  may be cited if Codex C proves it still covers the required behavior.

Not sufficient:

- evidence-ledger row existence without the unknown-entry invariants;
- non-Tier 6 confidence/finality/degradation rows;
- runtime field evidence or validation report wiring.

### Required Non-Claims

Every manifest/session-ledger entry and implementation handoff must preserve
these non-claims:

- no parser support for unknown semantic content;
- no parser-understood unknown future MTGA message support;
- no trusted parser input;
- no new parser event kind;
- no automatic parser-gap issue creation;
- no automatic drift issue creation;
- no live private Player.log drift health;
- no diagnostics readiness;
- no private smoke success;
- no release readiness;
- no deploy readiness;
- no production behavior;
- no analytics truth;
- no AI truth;
- no coaching truth;
- no issue #388 or issue #381 activation;
- no tracker completion;
- no full corpus parity.

## Behavior-Readiness Packet

This row's reusable packet is:

```yaml
scenario_family: "log_runtime.unknown_entry"
current_status: "covered_report_only"
current_basis:
  - "diagnostics_only"
  - "fixture_metadata_only"
  - "evidence_ledger_only"
target_status_if_successful: "covered_synthetic"
parser_behavior_verified_may_be_added: true
evidence_type: "synthetic"
fixture_or_test_route:
  preferred: "existing focused router, drift, diagnostics, and evidence-ledger tests plus corpus metadata"
  allowed_new_tests:
    - "focused router valid-timestamp unrouted-entry test if needed"
  forbidden_new_tests:
    - "private Player.log checks"
    - "live MTGA checks"
    - "network, firewall, packet, OS/router, or private smoke checks"
    - "tests that require parser behavior changes"
manifest_session_ledger_changes_allowed: true
parser_behavior_changes_allowed: false
parser_event_families: []
private_external_inputs_forbidden: true
required_non_claims:
  - "unknown semantic content"
  - "trusted parser input"
  - "new parser event kind"
  - "automatic parser-gap issue creation"
  - "live drift health"
  - "diagnostics readiness"
  - "release/deploy/production readiness"
  - "analytics/AI/coaching truth"
  - "#388/#381 activation"
focused_validation:
  - "PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py tests/test_evidence_ledger.py tests/test_corpus_parity_report.py"
  - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
  - "python3 tools/check_agent_docs.py"
  - "path-scoped secret/protected-surface checks for changed files"
  - "git diff --check"
stop_conditions:
  - "implementation would change router, parser, diagnostics, drift, evidence-ledger, runtime, workbook, analytics, AI, coaching, CI, deploy, production, or final integration behavior"
  - "metadata would claim parser support for unknown semantic content"
  - "metadata would add parser_event_families for unknown entries"
  - "evidence would require private or external raw logs"
  - "implementation would activate issue #388 or issue #381"
```

## Compatibility Expectations

- Existing `unknown_entry_drift_report_reference_v1` report-only coverage must
  remain scoped to unknown-entry drift/diagnostics/evidence-ledger metadata.
- Existing `drift_debug.missing_message_type` coverage must remain scoped to
  its issue #500 missing/blank type fallback and GameState default-preservation
  packet.
- Existing `log_runtime.rotation` coverage must remain scoped to its issue
  #502 tailer/stream packet.
- `parser_event_families` for `log_runtime.unknown_entry` must remain empty.
- Existing readiness semantics must remain false unless all applicable rows
  satisfy the readiness contract.
- Existing issue #388 / issue #381 activation semantics must remain deferred.

## Validation Obligations For Codex C

If implementation proceeds, Codex C should run:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py tests/test_evidence_ledger.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
git diff --check
```

Codex C should also run path-scoped secret and protected-surface checks for all
changed files, for example:

```bash
printf '%s\n' <changed-files> | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' <changed-files> | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Validation is not complete unless the report still keeps:

- `parser_behavior_ready=false`, unless every applicable readiness row has
  independently satisfied its contract;
- `pipeline_activation_ready_for_issue_388=false`;
- no promoted blocked/private/external rows;
- no parser event families for `log_runtime.unknown_entry`;
- no private/raw/external artifacts in the diff.

## Acceptance Criteria

For Codex B:

- This contract exists at
  `docs/contracts/parser_corpus_unknown_entry_behavior_readiness.md`.
- It clearly selects reduced synthetic behavior uplift as the next path.
- It separates router/drift/diagnostics/evidence-ledger review behavior from
  parser-understood unknown semantic content.
- It preserves issue #388 and issue #381 as inactive.
- It provides a Codex C handoff and workflow block.

For future Codex C:

- Adds or updates corpus manifest/session-ledger metadata for
  `unknown_entry_synthetic_router_drift_diagnostics_v1`.
- Keeps `unknown_entry_drift_report_reference_v1` as report-only historical
  metadata.
- Adds focused router test coverage only if needed to isolate unknown-count
  behavior from timestamp anomalies.
- Does not change router, parser, diagnostics, drift, evidence-ledger, or
  downstream behavior.
- Keeps `parser_event_families` empty for `log_runtime.unknown_entry`.
- Preserves all non-claims.
- Produces the expected implementation handoff and contract-test report.

## Open Questions And Risks

- Existing router unknown-count test coverage is coupled to timestamp-missing
  behavior. Codex C should either add a narrower valid-timestamp unrouted-entry
  test or explicitly justify why the existing test is sufficient.
- Existing drift/diagnostics evidence uses committed sanitized/count-only
  references and generated temp files. Codex C must keep raw/private log
  content out of corpus metadata.
- `parser_behavior_verified` is unusually delicate for this row because no
  parser event should be emitted. The metadata must explain that the verified
  behavior is accounting/review behavior only.

## Recommended Next Role

Codex C: Module Implementer.

Codex C should implement metadata/test/docs only. It should not implement
router, parser, diagnostics, drift, evidence-ledger, runtime, or downstream
behavior changes.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #504.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/504

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/502

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/503

Previous merge commit:
7fd62e893f8fd5e7e783e8a0b9e3eea374e485ae

Base branch:
main

Contract:
docs/contracts/parser_corpus_unknown_entry_behavior_readiness.md

Goal:
Implement the smallest metadata/test/docs change needed to satisfy the
unknown-entry behavior-readiness contract for `log_runtime.unknown_entry`.

Required implementation boundary:
- Add a dedicated reduced synthetic router/drift/diagnostics/evidence-ledger
  behavior packet.
- Keep `unknown_entry_drift_report_reference_v1` as report-only historical
  non-claim metadata.
- Add or update corpus manifest/session-ledger metadata so the row may move
  from `covered_report_only` to `covered_synthetic` only with
  `parser_behavior_verified`.
- Keep `parser_event_families` empty for `log_runtime.unknown_entry`.
- Prove or cite the router leg: an unrouted synthetic entry returns no events
  and increments `RouterStats.unknown`.
- Prefer a valid-timestamp router test if the existing test is too coupled to
  timestamp-missing behavior.
- Prove or cite the drift leg: unknown counts, review status, bounded unknown
  signatures/API-name samples, and privacy normalization.
- Prove or cite the diagnostics leg: unknown evidence produces review status
  and sensitive-looking values are redacted.
- Prove or cite the evidence-ledger leg: Tier 6 unknown-entry-count provenance
  is run-scoped and review-only.
- Do not use `drift_debug.missing_message_type`, `log_runtime.rotation`,
  `drift_debug.rename_or_rotation_collision`, or private-log drift evidence as
  unknown-entry behavior-readiness support.
- Do not change router, parser, diagnostics, drift, evidence-ledger, runtime,
  or downstream behavior.

Expected files:
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- tests/test_router_unit.py, only if a narrow router test is needed
- docs/implementation_handoffs/parser_corpus_unknown_entry_behavior_readiness_comparison.md
- docs/contract_test_reports/parser_corpus_unknown_entry_behavior_readiness.md

Do not:
- Activate #388 / #381.
- Close #158, #388, #434, or #504.
- Promote blocked or unrelated report-only rows.
- Add parser event families for unknown entries.
- Change parser behavior, router behavior, parser event classes, diagnostics
  report shape, drift report behavior, evidence-ledger schema/vocabulary,
  golden replay behavior, feature-equity behavior, analytics behavior,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, CI gates, merge readiness, deploy readiness,
  production behavior, or final integration policy.
- Run private Player.log, UTC_Log, live MTGA, private drift, network, or
  private smoke checks.
- Import, copy, mirror, summarize, or commit Manasight raw logs, compressed
  corpus files, parser source, external corpus contents, private logs,
  generated/runtime artifacts, workbook exports, secrets, tokens, API keys,
  webhook URLs, decklists, card choices, screenshots, private strategy notes,
  private reports, exact private paths, raw hashes, or local-only artifacts.
- Claim parser support for unknown semantic content, unknown future MTGA
  messages, trusted parser input, automatic parser-gap issue creation,
  automatic drift issue creation, live drift health, diagnostics readiness,
  release readiness, production behavior, analytics truth, AI truth, coaching
  truth, tracker completion, or full corpus parity.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py tests/test_evidence_ledger.py tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- run path-scoped secret/protected-surface checks for changed files
- git diff --check

End with:
- files changed
- reduced unknown-entry evidence added or cited
- validation run
- remaining risks/open questions
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/504"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/502"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/503"
  previous_merge_commit: "7fd62e893f8fd5e7e783e8a0b9e3eea374e485ae"
  completed_thread: "B"
  next_thread: "C"
  base_branch: "main"
  selected_family: "log_runtime.unknown_entry"
  prior_status: "covered_report_only"
  authorized_target_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  target_contract: "docs/contracts/parser_corpus_unknown_entry_behavior_readiness.md"
  expected_implementation_handoff: "docs/implementation_handoffs/parser_corpus_unknown_entry_behavior_readiness_comparison.md"
  expected_contract_test_report: "docs/contract_test_reports/parser_corpus_unknown_entry_behavior_readiness.md"
  verdict: "reduced_synthetic_unknown_entry_behavior_readiness_authorized"
  risk_tier: "High"
  stop_conditions:
    - "Do not activate #388 / #381."
    - "Do not close #158, #388, #434, or #504."
    - "Do not promote blocked or unrelated report-only rows."
    - "Do not add parser event families for unknown entries."
    - "Do not claim parser support for unknown semantic content, trusted parser input, automatic parser-gap issue creation, live drift health, diagnostics readiness, release readiness, production behavior, analytics truth, AI truth, coaching truth, tracker completion, or full corpus parity."
    - "Do not change parser behavior, router behavior, parser event classes, diagnostics report shape, drift report behavior, evidence-ledger schema/vocabulary, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, coaching truth, CI gates, deploy policy, production behavior, or final integration policy."
```
