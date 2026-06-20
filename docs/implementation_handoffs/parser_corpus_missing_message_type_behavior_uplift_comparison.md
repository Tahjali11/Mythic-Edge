# Parser Corpus Missing Message Type Behavior Uplift Handoff

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/500
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/498
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/499
- Previous merge commit: `b3d8dfc1527bfef7d0828d41c7fce6128a745883`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/414
- Adjacent report-only family: `log_runtime.unknown_entry`
- Branch: `codex/parser-corpus-missing-message-type-behavior-uplift-500`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_missing_message_type_behavior_uplift.md`
- Risk tier: High

## Contract Comparison

The contract authorized moving only `drift_debug.missing_message_type` beyond
the #414 report-only boundary if a reduced two-leg synthetic packet could be
proven through existing parser behavior:

- client-action missing/blank inner `type` generic fallback; and
- GRE GameState missing top-level message `type` default preservation.

The implementation satisfies both legs with focused tests:

- `test_client_actions_missing_message_type_behavior_packet_preserves_raw_fallbacks`
  proves one missing inner `type` payload and one whitespace inner `type`
  payload both emit `ClientActionEvent` with `type == "generic_client_action"`,
  `message_type == ""`, and preserved `raw_client_action`.
- `test_gre_missing_message_type_behavior_packet_uses_default_and_preserves_raw`
  proves a parseable public GRE dispatch input whose selected
  `gameStateMessage` lacks a top-level message `type` emits a `GameStateEvent`
  with `type == "game_state_message"`,
  `message_type == "GREMessageType_GameStateMessage"`, and preserved
  `raw_game_state`.

No parser source, router behavior, GRE parser behavior, client-action parser
behavior, diagnostics, drift, golden replay, feature-equity, evidence-ledger,
analytics, workbook, webhook, Apps Script, or output behavior was changed.

The committed corpus metadata uses `GameState source preservation` wording
instead of the literal parser field name so the corpus artifact remains clean
under the report validator's raw-log marker checks. The focused GRE dispatch
test still asserts the actual parser-owned `raw_game_state` field.

## Changes Made

- Added a dedicated missing-message-type client-action fallback test in
  `tests/test_client_actions_parser.py`.
- Added a dedicated GRE GameState missing-type default-preservation dispatch
  test in `tests/test_client_actions_parser.py`. This keeps the test in a
  synthetic marker-safe file; `tests/test_gre_game_state_parser.py` was run
  for validation but left unchanged because path-scanning that existing file
  reports historical raw-marker fixtures outside this contract.
- Added `missing_message_type_synthetic_fallback_defaults_v1` to
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added `missing_message_type_synthetic_fallback_defaults_v1` to
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_corpus_parity_report.py` to pin the new manifest row,
  session-ledger row, status movement, readiness count movement, matrix row,
  and non-claims.
- Added this handoff.
- Added
  `docs/contract_test_reports/parser_corpus_missing_message_type_behavior_uplift.md`.

The contract source artifact was present in the worktree and used as input; it
was not modified by this implementation pass.

## Status Movement

Only one scenario family changed status:

| Scenario family | Before | After |
| --- | --- | --- |
| `drift_debug.missing_message_type` | `covered_report_only` | `covered_synthetic` |

The resulting corpus parity summary is:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 20
covered_report_only: 13
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
parser_behavior_ready_family_count: 25
pipeline_activation_ready_for_issue_388: false
pipeline_activation_blockers:
  - "report_only_families:13"
  - "blocked_private_evidence_families:2"
  - "blocked_external_boundary_families:4"
```

The corpus is still not parser-behavior ready and does not activate #388 or
#381.

## Preserved Boundaries

- No parser behavior, router behavior, GRE parser behavior, client-action
  parser behavior, parser event classes, diagnostics, drift, golden replay,
  feature-equity, evidence-ledger, analytics behavior, workbook schema,
  webhook payload shape, Apps Script behavior, Google Sheets sync, output
  transport, CI gates, merge readiness, deploy readiness, production behavior,
  or final integration policy changed.
- No private Player.log, UTC_Log, live MTGA, private malformed payload,
  private smoke output, Manasight raw log, external corpus input, generated
  data, SQLite artifact, runtime artifact, workbook export, secret,
  credential, token, API key, or webhook URL was used.
- The #414 `missing_message_type_boundary_report_v1` row remains report-only
  non-claim metadata.
- The `log_runtime.unknown_entry` row remains report-only adjacent context and
  is not used as missing-message-type support.
- The #498 event-ordering evidence remains unchanged.
- The new evidence does not claim parser message recovery, hidden payload
  truth, GameState reconstruction, unknown future MTGA message support,
  generic unknown-entry support, parser resilience truth, live private
  Player.log drift health, diagnostics readiness, analytics truth, AI truth,
  coaching truth, private smoke success, release readiness, production
  behavior, #388/#381 activation, tracker completion, or full corpus parity.

## Validation Run

- `PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py::test_client_actions_missing_message_type_behavior_packet_preserves_raw_fallbacks tests/test_client_actions_parser.py::test_gre_missing_message_type_behavior_packet_uses_default_and_preserves_raw`
  passed: 2 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_game_state_parser.py tests/test_corpus_parity_report.py`
  passed: 70 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=20, report_only=13, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  completed with `selection_status: ok`.
- Path-scoped secret/private-marker scan completed with warnings only:
  scanned paths 7, forbidden 0, warnings 11. The warnings were ambiguous
  marker references in policy/docs and synthetic test-marker constants.
- Path-scoped protected-surface scan passed: changed paths 7, forbidden 0,
  warnings 0.
- `git diff --check` passed.

## Residual Risks

- The new evidence is synthetic and proves only selected fallback/default
  preservation for owned parseable payloads.
- It does not prove parser message recovery, hidden payload truth, GameState
  reconstruction, malformed JSON recovery, unknown future MTGA message
  support, generic unknown-entry support, parser resilience truth, private
  drift health, analytics truth, AI truth, coaching truth, release readiness,
  production behavior, or full corpus parity.
- Remaining report-only, private-evidence, and external-boundary rows keep the
  overall corpus from parser-behavior readiness.

## Reviewer Focus

Codex E should verify:

- no parser source files changed;
- both reduced legs are proved through existing public parser behavior;
- `missing_message_type_boundary_report_v1` remains report-only;
- `log_runtime.unknown_entry` remains report-only adjacent context;
- #498 event-ordering evidence remains unchanged;
- readiness metrics move exactly one family from report-only to synthetic;
- #388/#381 activation remains false/deferred; and
- no private/external/raw/generated artifacts are present.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #500, missing-message-type behavior
uplift under tracker #158.

Review:
- docs/contracts/parser_corpus_missing_message_type_behavior_uplift.md
- tests/test_client_actions_parser.py
- tests/test_gre_game_state_parser.py (validation-only; unchanged)
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_missing_message_type_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_missing_message_type_behavior_uplift.md

Verify that drift_debug.missing_message_type is promoted only by the new
focused synthetic client-action and GRE GameState parser-behavior tests, that
missing_message_type_boundary_report_v1 remains report-only non-claim
metadata, that log_runtime.unknown_entry remains adjacent report-only context,
and that #498 event-ordering evidence remains unchanged.

Do not target main directly. Do not close tracker #158, #388, #434, or #500.
Do not activate #388 or #381. Do not run private/live checks. Do not claim
parser message recovery, hidden payload truth, GameState reconstruction,
unknown future MTGA message support, generic unknown-entry support, parser
resilience truth, diagnostics readiness, analytics truth, AI truth, coaching
truth, readiness, production behavior, full corpus parity, or tracker
completion.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/500"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/498"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/499"
  previous_merge_commit: "b3d8dfc1527bfef7d0828d41c7fce6128a745883"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/414"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_missing_message_type_behavior_uplift.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_missing_message_type_behavior_uplift_comparison.md"
  report_artifact: "docs/contract_test_reports/parser_corpus_missing_message_type_behavior_uplift.md"
  verdict: "missing_message_type_behavior_uplift_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-missing-message-type-behavior-uplift-500"
  base_branch: "main"
  selected_family: "drift_debug.missing_message_type"
  prior_status: "covered_report_only"
  current_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
```
