# Parser Corpus Unknown Entry Behavior Readiness Report

## Verdict

`log_runtime.unknown_entry` has one reduced synthetic behavior-readiness uplift
ready for Codex E review.

The evidence is intentionally narrow. It proves that existing repo-owned
router, drift, diagnostics, and evidence-ledger behavior can account for and
surface unknown entries as review evidence without treating them as
parser-understood facts.

This report does not claim parser support for unknown semantic content,
trusted parser input, unknown future MTGA message support, a new parser event
kind, automatic parser-gap issue creation, automatic drift issue creation,
live drift health, diagnostics readiness, release readiness, deploy readiness,
production behavior, analytics truth, AI truth, coaching truth, tracker
completion, #388/#381 activation, or full corpus parity.

## Evidence Added

- Router test:
  `test_route_counts_valid_timestamp_unrouted_entry_as_unknown_only`
- Corpus manifest entry:
  `unknown_entry_synthetic_router_drift_diagnostics_v1`
- Session-ledger entry:
  `unknown_entry_synthetic_router_drift_diagnostics_v1`
- Corpus parity assertions pinning:
  - status movement to `covered_synthetic`;
  - `parser_behavior_verified` basis;
  - empty `parser_event_families`;
  - readiness metric count movement;
  - adjacent-row non-promotion; and
  - required non-claims.

The #377 entry `unknown_entry_drift_report_reference_v1` remains present and
report-only.

## Parser-Owned Evidence

The router leg verifies:

- one valid-timestamp synthetic entry;
- parser dispatch returns no events;
- `Router.route(...)` returns `[]`;
- `RouterStats.unknown == 1`;
- routed count remains zero; and
- timestamp anomaly counters remain zero.

The drift leg is existing committed behavior that verifies unknown counts,
review status, bounded unmatched API-name samples, normalized reference output,
and privacy-oriented signature behavior.

The diagnostics leg is existing committed behavior that verifies unknown
evidence produces review status and sensitive-looking unknown signature values
are not emitted raw.

The evidence-ledger leg is existing committed behavior that verifies Tier 6
`unknown_entry_count` is run-scoped and that unknown signatures / unmatched API
names remain review samples rather than trusted parser inputs.

## Corpus Status Effect

Before issue #504:

```yaml
log_runtime.unknown_entry:
  coverage_status: "covered_report_only"
  coverage_basis:
    - "diagnostics_only"
    - "evidence_ledger_only"
    - "fixture_metadata_only"
  mythic_edge_entries:
    - "unknown_entry_drift_report_reference_v1"
  parser_event_families: []
```

After issue #504:

```yaml
log_runtime.unknown_entry:
  coverage_status: "covered_synthetic"
  coverage_basis:
    - "diagnostics_only"
    - "evidence_ledger_only"
    - "fixture_metadata_only"
    - "parser_behavior_verified"
  mythic_edge_entries:
    - "unknown_entry_drift_report_reference_v1"
    - "unknown_entry_synthetic_router_drift_diagnostics_v1"
  parser_event_families: []
```

Current overall corpus summary:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 22
covered_report_only: 11
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
```

## Privacy And Protected Boundaries

- No private Player.log, UTC_Log, live MTGA, private drift, private smoke,
  network, Manasight raw log, external corpus input, generated data, SQLite
  artifact, runtime artifact, workbook export, secret, credential, token, API
  key, webhook URL, exact private path, raw hash, or local-only artifact was
  used.
- No parser behavior, router behavior, parser event classes, diagnostics
  report shape, drift report behavior, evidence-ledger schema or vocabulary,
  golden replay behavior, feature-equity behavior, analytics behavior,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, CI gates, merge readiness, deploy readiness,
  production behavior, or final integration policy changed.
- `drift_debug.missing_message_type` remains scoped to #500.
- `log_runtime.rotation` remains scoped to #502.
- `drift_debug.rename_or_rotation_collision` remains report-only.
- Private-log drift evidence remains separate.

## Non-Claims

This report does not claim:

- parser support for unknown semantic content;
- parser-understood unknown future MTGA message support;
- trusted parser input;
- new parser event kind;
- automatic parser-gap issue creation;
- automatic drift issue creation;
- live private Player.log drift health;
- diagnostics readiness;
- private smoke success;
- release readiness;
- deploy readiness;
- production behavior;
- analytics truth;
- AI truth;
- coaching truth;
- tracker completion;
- #388 or #381 activation;
- full corpus parity.

## Validation

- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_corpus_parity_report.py`
  passed: 25 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py tests/test_evidence_ledger.py tests/test_corpus_parity_report.py`
  passed: 141 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=22, report_only=11, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  completed with `selection_status: ok`: changed paths 7, required 6,
  recommended 1, warnings 0.
- Path-scoped secret/private-marker scan passed: scanned paths 7, forbidden 0,
  warnings 0.
- Path-scoped protected-surface scan passed: changed paths 7, forbidden 0,
  warnings 0.
- `git diff --check` passed.

## Residual Risks

- The evidence is synthetic and proves only reduced unknown-entry
  accounting/review behavior.
- Unknown entries remain evidence of unclassified log entries, not parser
  facts.
- Bounded unknown signatures and unmatched API names remain review samples, not
  trusted parser inputs.
- Overall corpus readiness remains blocked by report-only, private-evidence,
  and external-boundary rows.

## Codex E Review Target

Codex E should confirm that this is a safe additive metadata/test/docs uplift
and that the new `covered_synthetic` status is bounded to the reduced
unknown-entry accounting/review packet only.

## Codex E Contract-Test Review

Initial review result: route to Codex D for one metadata wording fix.

Finding `UNKENTRY-E-001` is blocking for Codex F submission:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json` still says the
  `log_runtime.unknown_entry` row remains "report-only adjacent context" in
  the `missing_message_type_synthetic_fallback_defaults_v1` review note.
- `tests/test_corpus_parity_report.py` pins the same stale wording in the
  expected `drift_debug.missing_message_type` matrix row.
- This conflicts with the issue #504 status transition, where
  `log_runtime.unknown_entry` now moves to `covered_synthetic`.

The implementation otherwise matches the reduced synthetic packet:

- `unknown_entry_synthetic_router_drift_diagnostics_v1` is additive.
- `unknown_entry_drift_report_reference_v1` remains report-only historical
  metadata.
- `parser_event_families` remains empty for `log_runtime.unknown_entry`.
- The new router test isolates valid-timestamp unrouted-entry unknown-count
  behavior from timestamp anomalies.
- `parser_behavior_ready=false` and
  `pipeline_activation_ready_for_issue_388=false` remain intact.

Validation rerun by Codex E:

- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_corpus_parity_report.py`
  passed: 25 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py tests/test_evidence_ledger.py tests/test_corpus_parity_report.py`
  passed: 141 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed `parser_behavior_ready=no`.
- Path-scoped secret/private-marker scan passed: scanned paths 7, forbidden 0,
  warnings 0.
- Path-scoped protected-surface scan passed: changed paths 7, forbidden 0,
  warnings 0.
- Path-scoped validation selector completed with `selection_status: ok`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.

Recommended fix route: Codex D should update only the stale
`missing_message_type_synthetic_fallback_defaults_v1` adjacent-row wording and
the matching focused assertion so the note says `log_runtime.unknown_entry`
remains a separate adjacent row, not a report-only adjacent row. Do not change
router, parser, diagnostics, drift, evidence-ledger, runtime, workbook,
webhook, Apps Script, analytics, AI, CI, deploy, production, #388/#381
activation, or tracker behavior.

## Codex D Fixer Follow-Up

Status: `UNKENTRY-E-001` fixed.

Codex D updated only the stale
`missing_message_type_synthetic_fallback_defaults_v1` adjacent-row wording and
the paired focused assertions. The wording now says
`log_runtime.unknown_entry` remains separate adjacent context instead of
report-only adjacent context.

Validation rerun by Codex D:

- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_corpus_parity_report.py`
  passed: 25 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py tests/test_evidence_ledger.py tests/test_corpus_parity_report.py`
  passed: 141 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json --out /tmp/mythic_edge_issue_504_corpus_report_d_verify.json`
  passed and printed `parser_behavior_ready=no`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- Explicit 7-path secret/private-marker scan passed: forbidden 0,
  warnings 0.
- Explicit 7-path protected-surface scan passed: forbidden 0, warnings 0.
- Explicit 7-path validation selector completed with `selection_status: ok`.
- `PYTHONPATH=src python3 -m pytest -q` passed: 1779 tests.

Next route: Codex E Module Reviewer / Contract Tester should confirm the
fixed wording and re-check the reduced synthetic packet boundary.

## Codex E Follow-Up Final Approval

Report lifecycle: `final_approval`.

Final review result: approved for Codex F submission.

Finding `UNKENTRY-E-001` is verified fixed. The active corpus manifest and
focused corpus parity assertion now state that `log_runtime.unknown_entry`
remains separate adjacent context, not report-only adjacent context. The
historical #500 report/handoff text still reflects the older pre-#504 state,
but the current #504 metadata, tests, handoff, and report are internally
consistent.

Codex E confirmed that:

- `unknown_entry_synthetic_router_drift_diagnostics_v1` is additive and
  bounded to reduced unknown-entry accounting/review behavior.
- `unknown_entry_drift_report_reference_v1` remains report-only historical
  metadata.
- `parser_event_families` remains empty for `log_runtime.unknown_entry`.
- `drift_debug.missing_message_type`, `log_runtime.rotation`,
  `drift_debug.rename_or_rotation_collision`, and private-log drift evidence
  remain separate adjacent rows.
- `parser_behavior_ready=false` and
  `pipeline_activation_ready_for_issue_388=false` remain intact.

Validation rerun by Codex E after the fixer pass:

- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_corpus_parity_report.py`
  passed: 25 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_router_unit.py tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py tests/test_evidence_ledger.py tests/test_corpus_parity_report.py`
  passed: 141 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed `parser_behavior_ready=no`.
- Path-scoped secret/private-marker scan passed: scanned paths 7, forbidden 0,
  warnings 0.
- Path-scoped protected-surface scan passed: changed paths 7, forbidden 0,
  warnings 0.
- Path-scoped validation selector completed with `selection_status: ok`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- `PYTHONPATH=src python3 -m pytest -q` passed: 1779 tests.

Remaining risk is intentionally scoped: this is synthetic accounting/review
evidence only. It does not prove parser support for unknown semantic content,
trusted parser input, new parser event kinds, automatic parser-gap issue
creation, live drift health, diagnostics readiness, release readiness, deploy
readiness, production behavior, analytics truth, AI truth, coaching truth,
tracker completion, #388/#381 activation, or full corpus parity.

Next recommended role: Codex F: Module Submitter.
