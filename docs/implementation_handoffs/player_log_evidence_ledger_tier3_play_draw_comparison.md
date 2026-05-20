# Player.log Evidence Ledger Tier 3 Play/Draw Implementation Handoff

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/139
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Parallel issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/137
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/138
- Previous merge commit: 869491a7999ebf2510c19925f1f671d1f37f2113
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier3-play-draw
- Risk tier: High

## Contract

- Source artifact: docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
- Expected artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md

## Role Performed

Codex C: Module Implementer.

## Summary

Implemented the Tier 3 starting-player and play/draw evidence-ledger metadata
slice required by the #139 contract. The implementation is ledger metadata,
focused tests, and this handoff only.

No parser behavior, starting-player extraction behavior, later-game inference
behavior, parser state final reconciliation, parser event classes, workbook
schema, webhook payload shape, Apps Script behavior, output transport,
match/game identity, deduplication, runtime surfaces, failed-post artifacts,
workbook exports, or AI/analytics truth changed.

## Confirmed Matches Before Editing

- Current parser behavior already exposes explicit ClientAction starting-player
  evidence through `_extract_starting_player_from_client_action(...)`.
- Current GameState extraction already uses turn-one active-player evidence and
  maps active seat to team id when player mapping is available.
- Current model behavior already derives `Play` / `Draw` from effective
  starting player plus local `player_team`.
- Current later-game behavior already infers game 2 and game 3 starters from
  previous game winner and participant context when explicit starting-player
  evidence is absent.
- Current evidence-ledger schema, validators, vocabulary constants, and copy
  safety already support the required metadata-only expansion.

## Contract Mismatches Fixed

- `game_level_facts.seed_fields` did not include the six granular #139 fields:
  `game1_starting_player`, `game2_starting_player`,
  `game3_starting_player`, `game1_play_draw`, `game2_play_draw`, and
  `game3_play_draw`.
- `game_level_facts.future_fields` still listed broad `play_draw` and
  `starting_player` after the granular slice was ready to seed.
- Six required `tier3.play_draw.*` entries were missing.
- Focused tests did not assert ClientAction evidence, turn-one GameState
  evidence, later-game inferred provenance, participant dependencies,
  prior-game winner dependencies, blank/degraded behavior, or #140 deferral for
  play/draw provenance.

## Changes Made

- Added six Tier 3 seed fields to `game_level_facts`.
- Removed broad `play_draw` and `starting_player` from Tier 3 future fields.
- Added validating entries:
  - `tier3.play_draw.game1_starting_player`
  - `tier3.play_draw.game2_starting_player`
  - `tier3.play_draw.game3_starting_player`
  - `tier3.play_draw.game1_play_draw`
  - `tier3.play_draw.game2_play_draw`
  - `tier3.play_draw.game3_play_draw`
- Documented explicit `ClientMessageType_ChooseStartingPlayerResp` evidence,
  turn-one GameState active-player team evidence, and degraded seat-only
  evidence.
- Labeled game 2 and game 3 model fallback as `inferred`, not observed.
- Added dependencies on #137 participant entries and #134 game-result entries
  where required.
- Kept #140 mulligan provenance and all other Tier 3/Tier 4 work deferred.

## Files Changed

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md`

Untracked source artifact present in this worktree:

- `docs/contracts/player_log_evidence_ledger_tier3_play_draw.md`

## Code Changed

Runtime parser behavior did not change.

The only Python implementation change is evidence-ledger metadata in
`src/mythic_edge_parser/app/evidence_ledger.py`. This does not add parser APIs,
state mutation, workbook fields, webhook fields, Apps Script mappings, runtime
field-evidence attachment, diagnostics behavior, replay behavior, or analytics
truth.

## Tests Added Or Updated

Updated `tests/test_evidence_ledger.py` to assert:

- Tier 3 seed fields include the #134 game-result fields plus the six #139
  starting-player/play-draw fields.
- Tier 3 future fields no longer list broad `play_draw` or `starting_player`.
- All six `tier3.play_draw.*` entries exist and validate.
- Starting-player entries cite explicit ClientAction evidence.
- Starting-player entries cite turn-one GameState active-player team and seat
  evidence.
- Game 1 starting-player metadata does not claim later-game inference.
- Game 2 starting-player metadata cites game 1 winner dependency and labels
  model fallback as inferred.
- Game 3 starting-player metadata cites game 2 winner dependency and labels
  model fallback as inferred.
- Play/draw entries cite their starting-player dependency and
  `tier1.participants.player_team`.
- Later-game play/draw entries cite opponent-team and previous-game winner
  context.
- Blank expected behavior and degraded played-game behavior are documented.
- #140 mulligan provenance and remaining game facts stay deferred.
- New evidence remains path-only and built-in entries validate cleanly.

## Interface Changes

No public parser API, parser event class, workbook schema, webhook payload,
Apps Script mapping, environment variable contract, runtime status schema,
failed-post schema, generated data shape, or output transport shape changed.

The ledger registry now exposes additional metadata entries and seed-field
names through the existing `build_player_log_evidence_ledger()` and
`iter_ledger_entries()` functions.

## Validation Run

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
# 38 passed in 0.17s

python3 -m pytest -q tests/test_app_extractors.py tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_state.py
# 70 passed in 0.16s

python3 -m pytest -q tests/test_golden_replay_harness.py
# 13 passed in 0.16s

python3 -m pytest -q
# 897 passed in 1.88s

python3 -m ruff check src tests tools
# All checks passed!

git diff --check
# passed with no output

python3 tools/check_protected_surfaces.py --base origin/main
# result: passed; forbidden: 0; warnings: 12

printf '%s\n' 'docs/contracts/player_log_evidence_ledger_tier3_play_draw.md' \
  'docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md' \
  'src/mythic_edge_parser/app/evidence_ledger.py' \
  'tests/test_evidence_ledger.py' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# result: passed; forbidden: 0; warnings: 0
```

Note: the broad protected-surface run compares the whole branch against
`origin/main`, so its 12 warnings come from prior parser-reliability branch
history. The focused stdin run over this #139 package reported no warnings.

## Still Unverified

- Codex E should independently verify the diff against the #139 contract.
- No live workbook, webhook, Apps Script, runtime, diagnostics, replay report,
  feature-equity report, or AI/analytics behavior was exercised or changed.
- Issue #140 mulligan provenance remains open and intentionally unimplemented.
- This worktree has not staged, committed, pushed, or opened a PR.

## Reviewer Focus

Codex E should pay special attention to:

- The #139 scope stays metadata/test-only.
- No starting-player extraction, inference, parser state, or model behavior
  changed.
- Game 1 does not claim later-game inference.
- Game 2 and game 3 inferred starting-player provenance is labeled `inferred`.
- Play/draw entries depend on starting-player plus `player_team`.
- Later-game inference cites prior-game winner and participant dependencies.
- Broad `play_draw` and `starting_player` are removed from future fields only
  after granular fields are seeded.
- #140 mulligans and remaining game-level facts stay deferred.
- The source contract is currently an untracked source artifact in this
  worktree and should be considered part of the reviewed package if it is not
  already present on the target base.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #139, Tier 3 play/draw provenance under issue #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/139
- Parallel issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/137
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/138
- Previous merge commit: 869491a7999ebf2510c19925f1f671d1f37f2113
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier3-play-draw
- Contract: docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
- Implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md

Use:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_participant_player_team.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- tests/test_app_extractors.py
- tests/test_app_models.py
- tests/test_match_summary_from_match_state.py
- tests/test_state.py

Goal:
Verify the Codex C implementation against the #139 play/draw provenance contract.

Confirm:
- game_level_facts.seed_fields includes the existing #134 fields plus game1_starting_player, game2_starting_player, game3_starting_player, game1_play_draw, game2_play_draw, and game3_play_draw.
- game_level_facts.future_fields no longer lists broad play_draw or starting_player.
- all six tier3.play_draw.* entries exist and validate.
- starting-player entries cite explicit ClientAction ChooseStartingPlayer evidence.
- starting-player entries cite turn-one GameState active-player team and degraded seat evidence.
- game 1 starting-player metadata does not claim later-game inference.
- game 2 starting-player metadata cites game 1 winner dependency and labels fallback inference as inferred.
- game 3 starting-player metadata cites game 2 winner dependency and labels fallback inference as inferred.
- play/draw entries cite their starting-player dependency and tier1.participants.player_team.
- later-game play/draw entries cite participant/opponent-team and previous-game winner dependencies where needed.
- blank unplayed game behavior and degraded played-game missing-evidence behavior are documented.
- #140 mulligans and opening-hand, turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshots, invariant execution, and runtime field-evidence attachment remain deferred.
- no parser behavior, starting-player extraction/inference behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth changed.

Validation:
Run:
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_app_extractors.py tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_state.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change code in review-only mode.
Do not stage, commit, push, merge, target main, close issue #11, close issue #139, or absorb #140 work.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/139"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  parallel_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/137"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/138"
  previous_merge_commit: "869491a7999ebf2510c19925f1f671d1f37f2113"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_play_draw.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md"
  verdict: "ready_for_module_reviewer_contract_test"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-play-draw"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_app_extractors.py tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_state.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #139."
    - "Do not change parser behavior, starting-player extraction behavior, later-game starting-player inference behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not map mulligan, opening-hand, turn-count, timing/duration, pre/postboard, sideboarding, or deck-state provenance."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```
