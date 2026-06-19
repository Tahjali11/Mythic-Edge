# Parser Corpus Companion / Large-Deck Behavior Uplift Handoff

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/494
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/492
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/493
- Previous merge commit: `8d1e48c9c6bd0a20926829c2d7de1d516a24ac20`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/408
- Branch: `codex/parser-corpus-companion-large-deck-behavior-uplift-494`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md`
- Risk tier: High

## Contract Comparison

The contract authorized moving only
`gameplay_stress.companion_or_large_deck` beyond the #408 report-only boundary
if two reduced synthetic deck-shape evidence legs could be proven by existing
parser behavior:

- StartHook / `DeckCollection` preserves a companion-shaped deck payload field.
- SubmitDeckResp / `ClientAction` preserves and normalizes a large-deck-like
  `deck_cards` list with count greater than 60.

Both evidence legs are satisfied by focused parser tests. No parser source or
parser behavior was changed.

The contract suggested `focused_parser_tests` as the manifest entry type, but
the current corpus manifest validator does not include that vocabulary. To stay
inside the expected file set and avoid a report schema change, the new entry
uses the existing `session_ledger_entry` type while preserving the contracted
title, paths, event families, claim families, coverage status, basis, and
non-claims.

## Changes Made

- Added a focused collection parser test proving a synthetic `Companions`
  field is preserved inside the correlated `DeckCollection` payload and
  `raw_start_hook`.
- Added a focused client-action parser test proving a synthetic 80-card
  `SubmitDeckResp` `deck_cards` list is preserved and normalized, with
  sideboard and request context still intact.
- Refactored synthetic Player.log-style marker literals in
  `tests/test_client_actions_parser.py` into explicit test-marker constants so
  the changed file remains scanner-safe without changing runtime test inputs.
- Added `companion_large_deck_synthetic_deck_shape_v1` to
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added `companion_large_deck_synthetic_deck_shape_v1` to
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_corpus_parity_report.py` to pin the new manifest row,
  session-ledger row, status movement, readiness count movement, matrix row,
  and non-claims.
- Added this handoff.
- Added
  `docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md`.

The contract source artifact was present in the worktree and used as input; it
was not modified by this implementation pass.

## Status Movement

Only one scenario family changed status:

| Scenario family | Before | After |
| --- | --- | --- |
| `gameplay_stress.companion_or_large_deck` | `covered_report_only` | `covered_synthetic` |

The resulting corpus parity summary is:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 17
covered_report_only: 16
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
parser_behavior_ready_family_count: 22
pipeline_activation_ready_for_issue_388: false
pipeline_activation_blockers:
  - "report_only_families:16"
  - "blocked_private_evidence_families:2"
  - "blocked_external_boundary_families:4"
```

The corpus is still not parser-behavior ready and does not activate #388 or
#381.

## Preserved Boundaries

- No parser behavior, parser event classes, parser state final reconciliation,
  router semantics, match/game identity, diagnostics, drift, golden replay,
  feature-equity, evidence-ledger, workbook schema, webhook payload shape, Apps
  Script behavior, Google Sheets sync, output transport, analytics truth,
  AI/model-provider behavior, coaching behavior, CI gates, merge readiness,
  deploy readiness, production behavior, or final integration policy was
  changed.
- No private Player.log, UTC_Log, live MTGA, private deck, Manasight raw log,
  external corpus, generated data, SQLite, runtime artifact, workbook export,
  secret, credential, token, API key, or webhook URL was used.
- The #408 `companion_large_deck_boundary_report_v1` row remains report-only
  non-claim metadata.
- The new evidence does not claim companion presence, companion legality,
  companion castability, in-game companion availability, large-deck legality,
  complete decklist truth, deck identity, deck ownership, sideboard choice
  truth, hidden-card truth, archetype classification, gameplay advice,
  analytics truth, AI truth, coaching truth, private smoke success, release
  readiness, production behavior, #388/#381 activation, tracker completion, or
  full corpus parity.

## Validation Run

- `PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py`
  passed: 65 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_corpus_parity_report.py`
  passed: 72 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=17, report_only=16, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed: checked files 34, errors 0,
  warnings 0.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- Path-scoped secret/private-marker scan completed with exit code 0,
  forbidden 0, warnings 3. Warnings were explicit synthetic test-marker
  constants in `tests/test_client_actions_parser.py`; no secret or private
  artifact was committed.
- Path-scoped protected-surface scan passed: forbidden 0, warnings 0.
- ASCII scan over changed files passed.
- Trailing-whitespace scan over changed files passed.
- Generated SQLite/local DB artifact scan returned no files.

## Residual Risks

- The new evidence is synthetic and proves only reduced deck-shape preservation
  through existing parser outputs.
- It does not prove real companion behavior, large-deck legality, complete
  decklists, exact deck identity, hidden-card truth, private MTGA behavior,
  analytics truth, AI truth, coaching truth, release readiness, production
  behavior, or full corpus parity.
- Remaining report-only, private-evidence, and external-boundary rows keep the
  overall corpus from parser-behavior readiness.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #494, companion / large-deck
behavior uplift under tracker #158.

Review:
- docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md
- tests/test_collection_parser.py
- tests/test_client_actions_parser.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md

Verify that gameplay_stress.companion_or_large_deck is promoted only by the two
new focused synthetic parser tests, that companion_large_deck_boundary_report_v1
remains report-only non-claim metadata, and that no parser behavior or protected
downstream surface changed. Note that the implementation used the existing
session_ledger_entry manifest entry type because focused_parser_tests is not in
the current manifest vocabulary.

Do not target main directly. Do not close tracker #158, #388, #434, or #494.
Do not activate #388 or #381. Do not run private/live checks. Do not claim
companion presence, companion legality, companion castability, large-deck
legality, complete decklist truth, deck identity truth, readiness, analytics
truth, AI truth, coaching truth, full corpus parity, or tracker completion.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/494"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/492"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/493"
  previous_merge_commit: "8d1e48c9c6bd0a20926829c2d7de1d516a24ac20"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/408"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md"
  report_artifact: "docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md"
  verdict: "companion_large_deck_behavior_uplift_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-companion-large-deck-behavior-uplift-494"
  base_branch: "main"
  selected_family: "gameplay_stress.companion_or_large_deck"
  prior_status: "covered_report_only"
  current_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  recommended_next_role: "Codex E: Module Reviewer"
```
