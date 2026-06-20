# Parser Corpus Unknown Entry Behavior Readiness Handoff

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/504
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/502
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/503
- Previous merge commit: `7fd62e893f8fd5e7e783e8a0b9e3eea374e485ae`
- Prior report-only boundary issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/377
- Branch: `codex/parser-corpus-unknown-entry-behavior-readiness-504`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_unknown_entry_behavior_readiness.md`
- Risk tier: High

## Contract Comparison

The contract authorized moving only `log_runtime.unknown_entry` beyond the
#377 report-only boundary if a reduced synthetic router, drift, diagnostics,
and evidence-ledger review packet could be proven without behavior changes.

The implementation satisfies the packet through focused tests:

- Router leg: added
  `test_route_counts_valid_timestamp_unrouted_entry_as_unknown_only`, which
  proves a valid-timestamp unrouted synthetic entry returns no events,
  increments `RouterStats.unknown`, leaves routed count at zero, and does not
  rely on timestamp-anomaly behavior.
- Drift leg: cites existing
  `test_build_player_log_drift_report_surfaces_unmatched_api_names`,
  `test_drift_report_reference_matches_manifest_fixture`, and
  `test_entry_signature_prefers_prefix_label_for_privacy`.
- Diagnostics leg: cites existing
  `test_unknown_signatures_produce_review_and_are_sanitized` and related
  diagnostics redaction coverage.
- Evidence-ledger leg: cites existing
  `test_tier6_unknown_entry_count_entry_documents_run_scoped_counts`.

No router, parser, diagnostics, drift, evidence-ledger, runtime, workbook,
webhook, Apps Script, analytics, AI, CI, deploy, production, or final
integration behavior was changed.

## Changes Made

- Added one focused router test in `tests/test_router_unit.py`.
- Added `unknown_entry_synthetic_router_drift_diagnostics_v1` to
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added `unknown_entry_synthetic_router_drift_diagnostics_v1` to
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_corpus_parity_report.py` to pin the new manifest row,
  session-ledger row, empty parser event families, status movement, readiness
  count movement, matrix row, adjacent-row non-promotion, and non-claims.
- Added this implementation handoff.
- Added
  `docs/contract_test_reports/parser_corpus_unknown_entry_behavior_readiness.md`.

The #377 `unknown_entry_drift_report_reference_v1` entry remains present and
report-only. The new synthetic entry is additive.

## Status Movement

Only one scenario family changed status:

| Scenario family | Before | After |
| --- | --- | --- |
| `log_runtime.unknown_entry` | `covered_report_only` | `covered_synthetic` |

Current corpus parity summary after the change:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 22
covered_report_only: 11
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
parser_behavior_ready_family_count: 27
pipeline_activation_ready_for_issue_388: false
pipeline_activation_blockers:
  - "report_only_families:11"
  - "blocked_private_evidence_families:2"
  - "blocked_external_boundary_families:4"
```

The corpus is still not parser-behavior ready and does not activate #388 or
#381.

## Preserved Boundaries

- `parser_event_families` remains empty for `log_runtime.unknown_entry`.
- No parser support for unknown semantic content is claimed.
- No trusted parser input, new parser event kind, automatic parser-gap issue
  creation, automatic drift issue creation, live drift health, diagnostics
  readiness, private smoke success, release readiness, deploy readiness,
  production behavior, analytics truth, AI truth, coaching truth, #388/#381
  activation, tracker completion, or full corpus parity is claimed.
- `drift_debug.missing_message_type`, `log_runtime.rotation`,
  `drift_debug.rename_or_rotation_collision`, and private-log drift evidence
  remain separate adjacent rows.
- No private Player.log, UTC_Log, live MTGA, private drift, network, private
  smoke, Manasight raw log, external corpus input, generated data, SQLite
  artifact, runtime artifact, workbook export, secret, credential, token, API
  key, webhook URL, exact private path, raw hash, or local-only artifact was
  used.

## Validation Run

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

- The evidence is synthetic and proves only reduced accounting/review behavior.
- Unknown entries still mean Mythic Edge did not classify a log entry into a
  trusted parser event.
- Drift signatures and unmatched API names remain bounded review samples, not
  parser truth.
- Remaining report-only, private-evidence, and external-boundary rows keep the
  overall corpus from parser-behavior readiness.

## Codex D Fixer Update

Finding fixed: `UNKENTRY-E-001`.

Fault category: stale adjacent-row metadata wording and focused test
expectation.

Fix produced:

- Updated the `missing_message_type_synthetic_fallback_defaults_v1` manifest
  review note so `log_runtime.unknown_entry` remains a separate adjacent row,
  not a report-only adjacent row.
- Updated the paired focused assertions in `tests/test_corpus_parity_report.py`.
- Preserved router, parser, diagnostics, drift, evidence-ledger, runtime,
  workbook, webhook, Apps Script, analytics, AI, CI, deploy, production,
  #388/#381 activation, and tracker behavior.

Codex D validation:

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

## Reviewer Focus

Codex E should verify:

- no router/parser behavior changed;
- the added router test isolates unknown-count behavior from timestamp
  anomalies;
- `parser_event_families` remains empty for `log_runtime.unknown_entry`;
- `unknown_entry_drift_report_reference_v1` remains report-only;
- drift, diagnostics, and evidence-ledger citations remain review/provenance
  evidence only;
- readiness metrics move exactly one family from report-only to synthetic;
- #388/#381 activation remains false/deferred; and
- no private/external/raw/generated artifacts are present.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #504, unknown-entry
behavior-readiness under tracker #158.

Review:
- docs/contracts/parser_corpus_unknown_entry_behavior_readiness.md
- tests/test_router_unit.py
- tests/test_log_drift_sensor.py
- tests/test_parser_diagnostics_mode.py
- tests/test_evidence_ledger.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_unknown_entry_behavior_readiness_comparison.md
- docs/contract_test_reports/parser_corpus_unknown_entry_behavior_readiness.md

Verify that log_runtime.unknown_entry is promoted only by the additive
unknown_entry_synthetic_router_drift_diagnostics_v1 metadata, that the added
valid-timestamp router test proves an unrouted synthetic entry returns no
events and increments RouterStats.unknown without timestamp-anomaly coupling,
that drift/diagnostics/evidence-ledger evidence remains review/provenance only,
and that parser_event_families remains empty.

Do not target main directly. Do not close tracker #158, #388, #434, or #504.
Do not activate #388 or #381. Do not run private/live checks. Do not claim
parser support for unknown semantic content, trusted parser input, automatic
parser-gap issue creation, live drift health, diagnostics readiness, release
readiness, production behavior, analytics truth, AI truth, coaching truth,
tracker completion, or full corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/504"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/502"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/503"
  previous_merge_commit: "7fd62e893f8fd5e7e783e8a0b9e3eea374e485ae"
  completed_thread: "D"
  next_thread: "E"
  base_branch: "main"
  selected_family: "log_runtime.unknown_entry"
  prior_status: "covered_report_only"
  target_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  source_artifact: "docs/contracts/parser_corpus_unknown_entry_behavior_readiness.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_unknown_entry_behavior_readiness_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_unknown_entry_behavior_readiness.md"
  finding_id: "UNKENTRY-E-001"
  verdict: "metadata_wording_blocker_fixed_ready_for_module_review"
  risk_tier: "High"
```
