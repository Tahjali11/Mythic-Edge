# Player Log Evidence Ledger Tier 3 Turn-Count Comparison

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/145
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/144
- Previous merge commit: `af6d5f554720b159975e8fecfcf008298fd8ca76`
- Base branch: `codex/parser-reliability-intelligence`
- Implementation branch: `codex/player-log-evidence-ledger-tier3-turn-count`
- Source artifact: `docs/contracts/player_log_evidence_ledger_tier3_turn_count.md`
- Target artifact: `docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md`
- Risk tier: High
- Codex role: Codex C: Module Implementer

## Branch Gate Evidence

- Issue #145 is open.
- Current branch is `codex/player-log-evidence-ledger-tier3-turn-count`.
- Current branch is even with `origin/codex/parser-reliability-intelligence`.
- The previous #143 merge commit `af6d5f554720b159975e8fecfcf008298fd8ca76`
  is the current integration baseline.
- The contract source file was present as an untracked source artifact before
  implementation and was not modified by this pass.

## Confirmed Matches

- `src/mythic_edge_parser/app/evidence_ledger.py` already preserved the #128
  schema version, validators, vocabulary constants, privacy posture, and
  copy-safe build/iteration behavior.
- Existing #134 game-result, #139 play/draw, #140 mulligan, and #143
  opening-hand entries were present and validating before the #145 slice.
- Current parser behavior already exposes turn-number surfaces through
  `build_turn_info(...)`, `build_game_state_payload(...)`,
  `_extract_turn_info(...)`, `GameSummary.set_turn_count(...)`,
  `MatchSummary.set_game_turn_count(...)`, match-log `G1/G2/G3 Turn Count`, and
  game-log `Turn Count`.
- Current model behavior already stores the maximum observed integer turn
  number for a game slot and serializes zero/unobserved counts as blank. No
  behavior change was required to satisfy the metadata contract.

## Contract Mismatches Found And Fixed

- `game_level_facts.seed_fields` did not include `game1_turn_count`,
  `game2_turn_count`, or `game3_turn_count`.
- `game_level_facts.future_fields` still carried broad `turn_count`, even
  though the #145 contract requires replacing that broad future field with
  granular seeded fields.
- The ledger did not have validating `tier3.turn_count.gameN_turn_count`
  entries.
- Focused tests still asserted that turn-count provenance was deferred and that
  no `tier3.turn_count.*` entries existed.

## Changes Made

- Added three Tier 3 turn-count seed fields:
  `game1_turn_count`, `game2_turn_count`, and `game3_turn_count`.
- Removed broad `turn_count` from Tier 3 future fields while preserving
  deferred `game_timing`, `game_duration`, `pre_postboard`, `sideboarding`, and
  `deck_state`.
- Added validating entries for:
  - `tier3.turn_count.game1_turn_count`
  - `tier3.turn_count.game2_turn_count`
  - `tier3.turn_count.game3_turn_count`
- Documented path-only evidence for current GameState turn info, identity turn
  number, top-level payload turn number, extractor output, parser-state/model
  output, queued GameState fallback, game-slot dependency, and prior
  max-observed observation.
- Documented turn count as maximum observed valid positive turn number, not a
  reconstructed full turn timeline.
- Documented blank-vs-zero semantics, invalid negative/zero evidence,
  boolean/float coercion degradation, queued fallback reviewability,
  conflicting evidence, lower later observations, and truncation/data-loss
  degradation.
- Added focused tests in `tests/test_evidence_ledger.py` for seeded fields,
  validating entries, source evidence, fallback evidence, policy vocabulary,
  invariant language, privacy posture, remaining deferred scope, and
  preservation of prior Tier 3 slices.

## Boundaries Preserved

- No parser behavior changed.
- No turn-count update behavior changed.
- No GameState parsing, turn-info normalization, or extractor behavior changed.
- No parser state final reconciliation or parser event classes changed.
- No workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, environment
  variables, raw logs, generated data, runtime status files, failed posts,
  workbook exports, production behavior, or analytics truth changed.
- No missing turns, skipped phases, hidden actions, or absent Player.log facts
  were reconstructed.
- No parser-owned truth was moved into workbook formulas, dashboard logic, Apps
  Script, webhook delivery, diagnostics reports, golden replay manifests,
  analytics, or AI output.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - Result: passed, `51 passed`
- `python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py`
  - Result: passed, `82 passed`
- `python3 -m pytest -q`
  - Result: passed, `910 passed`
- `python3 -m ruff check src tests tools`
  - Result: passed, `All checks passed!`
- `git diff --check`
  - Result: passed
- `python3 tools/check_protected_surfaces.py --base origin/main`
  - Result: passed, `forbidden: 0`, `warnings: 12`
  - Note: warnings are from accumulated parser-reliability integration branch
    changes relative to `origin/main`; this module changed only
    `src/mythic_edge_parser/app/evidence_ledger.py`,
    `tests/test_evidence_ledger.py`, and this handoff artifact.

## Still-Unverified Layers

- Runtime field-evidence attachment is intentionally not implemented in #145.
- Drift reports, schema snapshots, diagnostics reports, replay reports,
  feature-equity reports, timing/duration provenance, and invariant execution
  are intentionally deferred.
- This metadata does not prove individual live matches have clean turn-count
  evidence; it documents the parser-owned provenance contract for future
  evidence attachment.

## Remaining Risks

- Current parser normalization can expose boolean-like, float-like, and
  negative turn values in some normalized payload surfaces. The ledger now
  documents these as degraded/review-required, but #145 does not change parser
  normalization or model update behavior.
- Blank output remains ambiguous between unplayed slots, no observed positive
  count, and degraded/missing evidence until a later runtime field-evidence
  issue attaches per-row provenance.
- Protected-surface warnings remain present when comparing the full integration
  branch to `origin/main`; there are no forbidden protected-surface changes from
  this implementation slice.

## Next Recommended Role

Next role: Codex E: Module Reviewer in contract-test mode.

Codex E should verify that the #145 implementation stayed metadata/test-only,
that all three turn-count entries validate and preserve privacy boundaries, and
that no parser behavior or protected downstream surfaces changed.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer in contract-test mode for issue #145, Tier 3 turn-count provenance under issue #11.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/145
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/144
    - Previous merge commit: af6d5f554720b159975e8fecfcf008298fd8ca76
    - Base branch: codex/parser-reliability-intelligence
    - Implementation branch: codex/player-log-evidence-ledger-tier3-turn-count
    - Contract: docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
    - Implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md

  Use:
    - docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
    - docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/parsers/gre/turn_info.py
    - src/mythic_edge_parser/parsers/gre/game_state.py
    - src/mythic_edge_parser/app/extractors.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/models.py

  Goal:
    Review the Codex C implementation against the #145 turn-count provenance contract.
    Confirm it is evidence-ledger metadata/test-only and does not change parser behavior.

  Confirm:
    - The three contracted turn-count seed fields are present.
    - Broad `turn_count` is removed from Tier 3 future fields.
    - All three `tier3.turn_count.*` entries exist and validate.
    - Turn count is documented as maximum observed valid positive turn number, not reconstructed total turns.
    - Direct evidence cites GameState turn-info, identity turn number, payload turn number, extractor output, and parser state/model output.
    - Fallback evidence cites queued GameState fallback, game-slot dependency, and prior max-observed observation.
    - Blank-vs-zero, malformed values, non-integral values, boolean/float coercion, negative values, queued fallback, conflicts, lower later observations, and truncation/data-loss degradation are documented.
    - `inferred` and `legacy_enriched` are not used as turn-count truth paths.
    - #134, #139, #140, and #143 entries remain present and valid.
    - All new evidence signals remain path-only and do not embed raw logs, raw GameState payloads, raw turn payloads, local artifacts, generated data, secrets, or workbook exports.
    - No parser behavior, turn-count update behavior, GameState parsing, turn-info normalization, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or analytics truth changed.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py
    - python3 -m pytest -q
    - python3 -m ruff check src tests tools
    - git diff --check
    - python3 tools/check_protected_surfaces.py --base origin/main

  Output:
    - Findings first, if any.
    - Contract-test verdict.
    - Validation results.
    - Remaining non-blocking gaps.
    - Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
    - workflow_handoff block.

  Do not:
    - Change code.
    - Stage, commit, merge, or target main.
    - Close issue #11 or issue #145.
    - Change parser/runtime/workbook/webhook/App Script/output behavior or protected surfaces.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/145"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/143"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/144"
  previous_merge_commit: "af6d5f554720b159975e8fecfcf008298fd8ca76"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_turn_count.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md"
  verdict: "tier3_turn_count_provenance_metadata_implemented_ready_for_contract_review"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-turn-count"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #145."
    - "Do not change parser behavior, turn-count update behavior, GameState parsing, turn-info normalization, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or analytics truth."
    - "Do not reconstruct missing turns, skipped phases, hidden actions, or facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```
