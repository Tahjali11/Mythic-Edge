# Player.log Evidence Ledger Tier 3 Mulligans Implementation Handoff

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/139
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/141
- Previous merge commit: 734c7c7f587e0951073b0c01b834e38cd7c60de1
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier3-mulligans
- Risk tier: High

## Contract

- Source artifact: docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
- Expected artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md

## Role Performed

Codex C: Module Implementer.

## Gate Check

The #139 gate passed before editing.

- `gh pr view 141` reported PR #141 merged into
  `codex/parser-reliability-intelligence` with merge commit
  `734c7c7f587e0951073b0c01b834e38cd7c60de1`.
- `git merge-base --is-ancestor 734c7c7f587e0951073b0c01b834e38cd7c60de1 origin/codex/parser-reliability-intelligence`
  exited successfully.
- `git rev-list --left-right --count HEAD...origin/codex/parser-reliability-intelligence`
  returned `0 0`.

## Summary

Implemented the Tier 3 mulligan provenance metadata slice required by the #140
contract. The implementation is evidence-ledger metadata, focused tests, and
this handoff only.

No parser behavior, mulligan counting behavior, ClientAction parsing behavior,
parser state final reconciliation, parser event classes, workbook schema,
webhook payload shape, Apps Script behavior, output transport, match/game
identity, deduplication, runtime surfaces, failed-post artifacts, workbook
exports, or AI/analytics truth changed.

## Confirmed Matches Before Editing

- #139 play/draw seed fields and `tier3.play_draw.*` entries were present on
  the branch and validated through existing tests.
- Current ClientAction parsing already specializes
  `ClientMessageType_MulliganResp` as `mulligan_resp` and preserves normalized
  decision values plus raw action metadata.
- Current parser state already owns `_MULLIGAN_COUNTS`,
  `_next_mulligan_count(...)`, and current match/game context handling.
- Current model behavior already exposes per-game mulligan counts,
  `MatchSummary.total_mulligans`, game-log `Mulligans`, match-log
  `G1/G2/G3 Mulligans`, and `MTGA Mulligans`.
- Current evidence-ledger schema, validators, vocabulary constants, privacy
  posture, deterministic serialization, and copy safety already support the
  required metadata-only expansion.

## Contract Mismatches Fixed

- `game_level_facts.seed_fields` did not include
  `game1_mulligans`, `game2_mulligans`, `game3_mulligans`, or
  `total_mulligans`.
- `game_level_facts.future_fields` still listed broad `mulligans`.
- Four required `tier3.mulligans.*` entries were missing.
- Focused tests did not yet assert mulligan ClientAction evidence, parser
  state counter/model dependencies, game-number/current-context dependencies,
  total-mulligan derivation, zero/blank semantics, unknown-decision
  degradation, or opening-hand/mulliganed-away deferral.

## Changes Made

- Added four Tier 3 seed fields:
  - `game1_mulligans`
  - `game2_mulligans`
  - `game3_mulligans`
  - `total_mulligans`
- Removed broad `mulligans` from Tier 3 future fields.
- Added validating entries:
  - `tier3.mulligans.game1_mulligans`
  - `tier3.mulligans.game2_mulligans`
  - `tier3.mulligans.game3_mulligans`
  - `tier3.mulligans.total_mulligans`
- Documented direct ClientAction `mulligan_resp` evidence and parser-state
  derived count surfaces.
- Documented missing context, unknown/blank/malformed/future decisions,
  duplicate/replayed action risk, contextless fallback zero, unplayed-slot
  blank behavior, played-slot degraded behavior, and live/final total display
  semantics.
- Preserved #139 play/draw seed fields, entries, notes, and tests while
  updating only stale "mulligans still future" assertions.
- Kept opening-hand, opening-hand size, exact hand, mulliganed-away,
  turn-count, timing/duration, pre/postboard, sideboarding, deck-state,
  analytics, diagnostics, replay, drift, schema snapshots, invariant
  execution, and runtime field-evidence attachment deferred.

## Files Changed

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md`

Untracked source artifact present in this worktree:

- `docs/contracts/player_log_evidence_ledger_tier3_mulligans.md`

Unrelated local artifact present before and after this pass:

- `docs/contracts/.player_log_evidence_ledger_tier3_mulligans.md.swp`

The swap file is not part of this implementation package and was not edited.

## Code Changed

Runtime parser behavior did not change.

The only Python implementation change is evidence-ledger metadata in
`src/mythic_edge_parser/app/evidence_ledger.py`. This does not add parser APIs,
state mutation, ClientAction parsing behavior, workbook fields, webhook fields,
Apps Script mappings, runtime field-evidence attachment, diagnostics behavior,
replay behavior, or analytics truth.

## Tests Added Or Updated

Updated `tests/test_evidence_ledger.py` to assert:

- Tier 3 seed fields include the #134 game-result fields, #139 play/draw
  fields, and the four #140 mulligan fields.
- Tier 3 future fields no longer list broad `mulligans`.
- #139 play/draw entries remain present and independent from mulligan entries.
- All four `tier3.mulligans.*` entries exist and validate.
- Per-game mulligan entries cite direct ClientAction `mulligan_resp` evidence.
- Per-game mulligan entries cite parser state counter and model dependencies.
- Per-game mulligan entries cite game-number and current match/game context
  dependencies.
- Total mulligans is derived from the three per-game mulligan entries and
  `MatchSummary.total_mulligans`.
- Unknown, blank, malformed, or future decision values are degraded and
  review-required.
- Contextless fallback zero is not a clean high-confidence zero.
- Zero/blank semantics are documented for game-log and match-log outputs.
- Opening-hand, exact-hand, and mulliganed-away provenance remain deferred.
- New evidence remains path-only and built-in entries validate cleanly.

## Interface Changes

No public parser API, parser event class, workbook schema, webhook payload,
Apps Script mapping, environment variable contract, runtime status schema,
failed-post schema, generated data shape, output transport shape, or analytics
surface changed.

The ledger registry now exposes additional metadata entries and seed-field
names through the existing `build_player_log_evidence_ledger()` and
`iter_ledger_entries()` functions.

## Validation Run

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
# 42 passed in 0.22s

python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py
# 107 passed in 0.18s

python3 -m pytest -q tests/test_golden_replay_harness.py
# 13 passed in 0.16s

python3 -m pytest -q
# 901 passed in 1.72s

python3 -m ruff check src tests tools
# All checks passed!

git diff --check
# passed with no output

python3 tools/check_protected_surfaces.py --base origin/main
# result: passed; forbidden: 0; warnings: 12

printf '%s\n' 'docs/contracts/player_log_evidence_ledger_tier3_mulligans.md' \
  'docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md' \
  'src/mythic_edge_parser/app/evidence_ledger.py' \
  'tests/test_evidence_ledger.py' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# result: passed; forbidden: 0; warnings: 0
```

Note: the broad protected-surface run compares the full parser-reliability
branch against `origin/main`, so its 12 warnings come from prior branch
history. The focused stdin run over this #140 package reported no warnings.

## Still Unverified

- Codex E should independently verify the diff against the #140 contract.
- No live workbook, webhook, Apps Script, runtime, diagnostics, replay report,
  feature-equity report, analytics, or AI behavior was exercised or changed.
- Opening-hand, exact-hand, mulliganed-away, turn-count, timing/duration,
  pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay,
  drift, schema snapshots, invariant execution, and runtime field-evidence
  attachment remain deferred.
- This worktree has not staged, committed, pushed, or opened a PR.

## Reviewer Focus

Codex E should pay special attention to:

- The #140 scope stays metadata/test-only.
- No ClientAction parsing, mulligan counting, parser state, or model behavior
  changed.
- #139 play/draw seed fields and entries remain present and valid.
- Per-game mulligan entries cite ClientAction evidence, parser-state count
  evidence, model surfaces, and current match/game context.
- Total mulligans is derived from per-game counts, not observed raw-log truth.
- Unknown/blank/malformed/future decision values are degraded/review-required.
- Contextless fallback `0` is not described as a clean high-confidence zero.
- Final total `0` and live blank total semantics are documented distinctly.
- Opening-hand, exact-hand, and mulliganed-away provenance remain deferred.
- The source contract is currently an untracked source artifact in this
  worktree and should be considered part of the reviewed package if it is not
  already present on the target base.
- The unrelated `.swp` file should remain out of the package.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #140, Tier 3 mulligan provenance under issue #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/139
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/141
- Previous merge commit: 734c7c7f587e0951073b0c01b834e38cd7c60de1
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier3-mulligans
- Contract: docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
- Implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md

Use:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_participant_player_team.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- tests/test_client_actions_parser.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_transforms.py
- tests/test_match_summary_from_match_state.py

Goal:
Verify the Codex C implementation against the #140 mulligan provenance contract.

Confirm:
- branch contains PR #141 / merge commit 734c7c7f587e0951073b0c01b834e38cd7c60de1 before the #140 changes.
- #139 play/draw seed fields and tier3.play_draw.* entries remain present and valid.
- game_level_facts.seed_fields includes game1_mulligans, game2_mulligans, game3_mulligans, and total_mulligans.
- game_level_facts.future_fields no longer lists broad mulligans.
- all four tier3.mulligans.* entries exist and validate.
- per-game mulligan entries cite direct ClientAction mulligan_resp evidence.
- per-game mulligan entries cite parser state count/model dependencies.
- per-game mulligan entries cite game-number or current-game context dependencies.
- total_mulligans cites all three per-game mulligan dependencies.
- total_mulligans is documented as derived, not observed.
- unknown, blank, malformed, or future decision values are documented as degraded/review-required.
- zero/blank semantics are documented for game-log and match-log outputs.
- opening-hand, exact-hand, and mulliganed-away fields remain deferred.
- no parser behavior, mulligan counting behavior, ClientAction parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth changed.

Validation:
Run:
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py
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
Do not stage, commit, push, merge, target main, close issue #11, close issue #140, or absorb deferred opening-hand/analytics work.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/139"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/141"
  previous_merge_commit: "734c7c7f587e0951073b0c01b834e38cd7c60de1"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_mulligans.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md"
  verdict: "ready_for_module_reviewer_contract_test"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-mulligans"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #140."
    - "Do not rework, remove, or weaken #139 play/draw provenance."
    - "Do not change parser behavior, mulligan counting behavior, ClientAction parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not map play/draw, opening-hand, opening-hand size, exact hand, mulliganed-away, turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior beyond this contract."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```
