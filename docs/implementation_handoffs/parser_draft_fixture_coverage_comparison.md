# Parser Draft Fixture Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/126

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

## Role Performed

Codex C: Module Implementer.

## Source Artifacts

- `docs/contracts/parser_draft_bot.md`
- `docs/contracts/parser_draft_human.md`
- `docs/contracts/parser_draft_complete.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`

## Worktree Note

The original local checkout was behind
`origin/codex/parser-reliability-intelligence` and had unrelated untracked
files from earlier modules. Codex C implemented issue #126 in a clean sibling
worktree named `Mythic-Edge-issue-126`.

That worktree is detached at `origin/codex/parser-reliability-intelligence`
commit `7540473`, the #125 DraftComplete merge commit. Submitter work should
still target `codex/parser-reliability-intelligence`, not `main`.

## Summary Of Implementation Comparison

No contract ambiguity or parser behavior mismatch was found. DraftBot,
DraftHuman, and DraftComplete parser modules already exist and focused parser
tests already cover their direct marker behavior.

The comparison found the issue #126 gap exactly as described: the committed
golden replay corpus and count-only feature-equity baseline still had zero
DraftBot, DraftHuman, and DraftComplete coverage. Codex C added a small
synthetic committed fixture that replays through the normal `LineBuffer`,
`Router`, parser modules, transforms, diagnostics, and parser state path.

No parser modules, router dispatch, event classes, parser state final
reconciliation, workbook schema, webhook payloads, Apps Script behavior,
runtime status schemas, failed-post schemas, raw logs, generated data, or
workbook exports were changed.

## Confirmed Matches

- DraftBot focused parser behavior still passes.
- DraftHuman focused parser behavior still passes.
- DraftComplete focused parser behavior still passes.
- Router and schema snapshot focused tests still pass.
- Golden replay still requires explicit committed manifests and rejects unsafe
  fixture metadata/content.
- Feature-equity corpus ratchet remains report-only and baseline-driven.
- New fixture content is synthetic and labeled as synthetic; no raw private
  `Player.log` excerpt was added.
- Golden replay over the committed manifest directory remains `pass`.
- Feature-equity corpus ratchet over the committed manifest directory remains
  `ok` against the updated count-only baseline.

## Contract Mismatches Found And Fixed

- Missing committed replay coverage for DraftBot.
  - Fixed by adding one synthetic `BotDraftDraftStatus` fixture entry.
- Missing committed replay coverage for DraftHuman.
  - Fixed by adding one synthetic `EventPlayerDraftMakePick` fixture entry.
- Missing committed replay coverage for DraftComplete.
  - Fixed by adding one synthetic `DraftCompleteDraft` fixture entry.
- Count-only feature-equity baseline still recorded zero draft-family counts.
  - Fixed by updating the baseline to the observed three-manifest corpus.
- Focused golden replay and ratchet tests still assumed two committed
  manifests and zero draft counts.
  - Fixed by updating the tests to assert the new committed draft coverage.

## Safeguards Preserved Or Added

- The new log slice is explicitly synthetic and says it is not a raw
  `Player.log` excerpt.
- The manifest uses the existing golden replay manifest schema and privacy
  fields.
- The manifest links to the golden replay contract issue as required by the
  harness and separately records issue #126 as `coverage_issue`.
- The fixture produces no unknown routed entries, timestamp anomalies,
  truncation markers, or data-loss signals.
- A tiny synthetic `GameState` anchor is included only so the existing fixture
  diagnostics profile remains `pass`; it does not introduce match completion,
  game result, hidden-card, decklist, archetype, coaching, workbook, or AI
  truth.
- The ratchet baseline update is count-only and records the extra synthetic
  GameState anchor as a coverage-shape count, not as new gameplay truth.

## Missing Or Weak Tests Found And Fixed

- Added golden replay coverage for the third committed manifest.
- Added a focused golden replay assertion that the draft parser family manifest
  passes without degradation.
- Updated the golden replay CLI directory test to expect three passing
  manifests.
- Updated the feature-equity corpus test to assert:
  - three manifests and three source files;
  - nonzero DraftBot, DraftHuman, and DraftComplete event-family counts;
  - draft payload-type counts;
  - updated routed and GameState anchor counts.
- Updated the ratchet mismatch test to keep its expected delta tied to the new
  baseline.

## Files Changed

- `tests/fixtures/draft_parser_family_slice.log`
- `tests/fixtures/golden_replay/draft_parser_family.manifest.json`
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
- `tests/test_golden_replay_harness.py`
- `tests/test_feature_equity_corpus_ratchet.py`
- `docs/implementation_handoffs/parser_draft_fixture_coverage_comparison.md`

## Validation Evidence

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py
# 13 passed

python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py
# 7 passed

python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
# 115 passed

python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py
# 23 passed

PYTHONPATH=src python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
# Golden replay: pass (3 manifests, 3 pass, 0 degraded, 0 review, 0 diff, 0 fail)

PYTHONPATH=src python3 -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests/fixtures/golden_replay --baseline tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
# Feature-equity corpus ratchet: ok (3 manifests, 3 source files)

python3 -m pytest -q tests
# 859 passed

python3 -m ruff check src tests tools
# All checks passed.

git diff --check
# passed

printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# Protected Surface Gate: passed; forbidden: 0; warnings: 0

python3 tools/check_protected_surfaces.py --base origin/main
# Protected Surface Gate: passed; forbidden: 0; warnings: 12 branch-scope
# protected parser/match-surface warnings from earlier parser reliability
# modules, not from the issue #126 changed-file set.

rg <forbidden secret/private marker patterns> tests/fixtures/draft_parser_family_slice.log tests/fixtures/golden_replay/draft_parser_family.manifest.json docs/implementation_handoffs/parser_draft_fixture_coverage_comparison.md
# no matches
```

The module CLI commands were run with `PYTHONPATH=src` in this sibling worktree
because the local desktop Python currently has an editable install pointing at
an older sibling checkout.

## Still-Unverified Layers

- Live private `Player.log` draft evidence was intentionally not used.
- The fixture proves normal parser-path coverage for synthetic draft markers;
  it does not prove that all live Arena draft variants are covered.
- CI was not run in GitHub.
- Workbook writes, webhook delivery, Apps Script, runtime status files,
  failed posts, workbook exports, AI/model-provider behavior, draft coaching,
  card ratings, deck construction analytics, hidden-card inference, and
  archetype classification were intentionally not exercised.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

## Pasteable Next-Thread Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer in contract-test mode for issue #126:
  https://github.com/Tahjali11/Mythic-Edge/issues/126

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/47

  Related evidence/resilience issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/11

  Branch:
  codex/parser-reliability-intelligence

  Use:
    - docs/contracts/parser_draft_bot.md
    - docs/contracts/parser_draft_human.md
    - docs/contracts/parser_draft_complete.md
    - docs/contracts/parser_golden_replay_harness.md
    - docs/contracts/parser_feature_equity_corpus_ratchet.md
    - docs/implementation_handoffs/parser_draft_fixture_coverage_comparison.md
    - tests/fixtures/draft_parser_family_slice.log
    - tests/fixtures/golden_replay/draft_parser_family.manifest.json
    - tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
    - tests/test_golden_replay_harness.py
    - tests/test_feature_equity_corpus_ratchet.py
    - tests/test_draft_bot_parser.py
    - tests/test_draft_human_parser.py
    - tests/test_draft_complete_parser.py
    - tests/test_router_unit.py
    - tests/test_event_schema_snapshots.py

  Goal:
    Verify the issue #126 implementation patch against the draft parser fixture
    coverage goal and the existing golden replay / feature-equity corpus
    contracts.

  Confirm:
    - The new fixture is synthetic/sanitized committed fixture coverage, not a raw private Player.log excerpt.
    - The fixture exercises DraftBot, DraftHuman, and DraftComplete through the normal LineBuffer/Router/parser path.
    - The manifest passes golden replay without review, degradation, diff, or fail status.
    - The synthetic GameState anchor is only a diagnostics anchor and does not invent match completion, game result, hidden-card, decklist, archetype, coaching, workbook, webhook, Apps Script, or AI truth.
    - The feature-equity baseline update is count-only and reflects observed replay counts.
    - Focused draft parser behavior, router behavior, schema snapshots, golden replay, and ratchet tests still pass.
    - No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, draft coaching, ratings, deck construction analytics, hidden information inference, or model-provider behavior changed.

  Validation:
    - python3 -m pytest -q tests/test_golden_replay_harness.py
    - python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py
    - python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
    - python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests/fixtures/golden_replay --baseline tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
    - python3 -m pytest -q tests
    - python3 -m ruff check src tests tools
    - git diff --check
    - python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin

  Output:
    - Findings first, if any.
    - Contract-test verdict.
    - Validation results.
    - Remaining non-blocking gaps.
    - Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
    - workflow_handoff block.

  Do not target main directly.
  Do not close tracker #47 or related issue #11.
  Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, output transport, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, draft coaching, ratings, deck construction analytics, hidden information inference, or model-provider behavior.
  Do not stage, commit, merge, or push unless explicitly asked.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/126"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  verdict: "ready_for_module_review"
  branch: "codex/parser-reliability-intelligence"
  source_artifacts:
    - "docs/contracts/parser_draft_bot.md"
    - "docs/contracts/parser_draft_human.md"
    - "docs/contracts/parser_draft_complete.md"
    - "docs/contracts/parser_golden_replay_harness.md"
    - "docs/contracts/parser_feature_equity_corpus_ratchet.md"
  target_artifact: "docs/implementation_handoffs/parser_draft_fixture_coverage_comparison.md"
  risk_tier: "Medium"
  validation:
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py"
    - "python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py"
    - "python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests/fixtures/golden_replay --baseline tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json"
    - "python3 -m pytest -q tests"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47 or related issue #11."
    - "Do not change protected parser/runtime/workbook/webhook/App Script/output surfaces."
    - "Do not infer hidden cards, complete decklists, classify archetypes, call model providers, or move parser truth downstream."
```
