# Player Log Evidence Ledger Tier 3 Pre/Postboard Comparison

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/149
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/147
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/148
- Previous merge commit: `14c69c47a953387b0a4151aeff4b46a17aadae64`
- Base branch: `codex/parser-reliability-intelligence`
- Implementation branch: `codex/player-log-evidence-ledger-tier3-pre-postboard`
- Source artifact: `docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md`
- Target artifact: `docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md`
- Related ADRs: `docs/decisions/ADR-0003-player-log-drift-policy.md`
- Risk tier: High
- Codex role: Codex C: Module Implementer

## Branch Gate Evidence

- Issue #149 is open.
- Current branch is `codex/player-log-evidence-ledger-tier3-pre-postboard`.
- Current branch is even with `origin/codex/parser-reliability-intelligence`.
- Current head before implementation was `14c69c4`, matching the previous #147/#148 integration baseline.
- The contract source file was present as an untracked source artifact before implementation and was not modified by this pass.

## Confirmed Matches

- `src/mythic_edge_parser/app/evidence_ledger.py` already preserved the #128
  schema version, validators, vocabulary constants, privacy posture, and
  copy-safe build/iteration behavior.
- Existing #134 game-result, #137 participant/player-team, #139 play/draw,
  #140 mulligan, #143 opening-hand, #145 turn-count, and #147 timing/duration
  entries were present and validating before the #149 slice.
- Current model behavior already serializes `Pre / Postboard` as `Preboard`
  for game 1 and `Postboard` for games 2 and 3 through
  `GameSummary.to_game_log_row(...)`.
- Current state/model behavior already emits game-log rows only for game slots
  with summary data. No behavior change was required to satisfy this metadata
  contract.

## Contract Mismatches Found And Fixed

- `game_level_facts.seed_fields` did not include `game1_pre_postboard`,
  `game2_pre_postboard`, or `game3_pre_postboard`.
- `game_level_facts.future_fields` still carried broad `pre_postboard`, even
  though the #149 contract requires replacing it with granular seeded fields.
- The ledger did not have validating `tier3.pre_postboard.gameN_pre_postboard`
  entries.
- Focused tests still treated pre/postboard provenance as deferred rather than
  seeded Tier 3 metadata.

## Changes Made

- Added three Tier 3 pre/postboard seed fields:
  `game1_pre_postboard`, `game2_pre_postboard`, and `game3_pre_postboard`.
- Removed broad `pre_postboard` from Tier 3 future fields while preserving
  deferred `sideboarding` and `deck_state`.
- Added validating entries for:
  - `tier3.pre_postboard.game1_pre_postboard`
  - `tier3.pre_postboard.game2_pre_postboard`
  - `tier3.pre_postboard.game3_pre_postboard`
- Documented path-only direct evidence for game-slot model state,
  `GameSummary.to_game_log_row()["Pre / Postboard"]`, and game-log row
  serialization.
- Documented path-only fallback evidence for game-number dependency, parser
  context game-number fallback, and row-emission context through
  `GameSummary.has_summary_data()`.
- Documented `Preboard`/`Postboard` as game-slot-derived labels, not observed
  sideboarding, submitted-deck, deck-state, format, queue, analytics, or AI
  truth.
- Added focused tests in `tests/test_evidence_ledger.py` for seeded fields,
  validating entries, source evidence, fallback evidence, value-source policy,
  confidence/finality policy, invariant language, privacy posture, remaining
  deferred scope, and preservation of prior Tier 3 slices.

## Boundaries Preserved

- No parser behavior changed.
- No game-number assignment, `GameSummary.to_game_log_row(...)`, literal
  `Pre / Postboard`, `Preboard`, or `Postboard` behavior changed.
- No sideboarding behavior, submitted-deck behavior, deck-state behavior,
  timestamp parsing, duration calculation, state update behavior, GameState
  parsing, turn-info parsing, extractor behavior, parser state final
  reconciliation, or parser event classes changed.
- No workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, environment
  variables, raw logs, generated data, runtime status files, failed posts,
  workbook exports, production behavior, environment variable contracts, or
  AI/analytics truth changed.
- No sideboarding, deck-state, analytics, diagnostics, replay, drift, schema
  snapshot, invariant execution, or runtime field-evidence attachment behavior
  was added.
- No hidden cards, decklists, archetypes, gameplay advice, player mistakes,
  matchup plans, or AI truth were inferred.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - Result: passed, `59 passed`
- `python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py`
  - Result: passed, `61 passed`
- `python3 -m pytest -q`
  - Result: passed, `918 passed`
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

- Runtime field-evidence attachment is intentionally not implemented in #149.
- Sideboarding and deck-state provenance remain deferred to later modules.
- Drift reports, schema snapshots, diagnostics reports, replay reports,
  feature-equity reports, sideboarding analytics, deck-state analytics, and
  invariant execution are intentionally deferred.
- This metadata does not prove that sideboarding happened or that deck
  contents changed; it documents only the parser-owned slot-derived label.

## Remaining Risks

- `Postboard` can still be misread by downstream humans or future analytics as
  proof of sideboarding. The ledger now documents this boundary, but runtime
  consumers are not changed by #149.
- Context-only or weak game-number assignment can still make the label
  review-worthy. The ledger documents this as degraded rather than changing
  parser behavior.
- Unplayed game slots remain row-omitted by model behavior; #149 documents
  that they should not become standalone pre/postboard truth.
- Protected-surface warnings remain present when comparing the full integration
  branch to `origin/main`; there are no forbidden protected-surface changes
  from this implementation slice.

## Next Recommended Role

Next role: Codex E: Module Reviewer in contract-test mode.

Codex E should verify that the #149 implementation stayed metadata/test-only,
that all three pre/postboard entries validate and preserve privacy boundaries,
and that no parser behavior or protected downstream surfaces changed.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer in contract-test mode for issue #149, Tier 3 pre/postboard provenance under issue #11.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/149
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/147
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/148
    - Previous merge commit: 14c69c47a953387b0a4151aeff4b46a17aadae64
    - Base branch: codex/parser-reliability-intelligence
    - Implementation branch: codex/player-log-evidence-ledger-tier3-pre-postboard
    - Contract: docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
    - Implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md

  Use:
    - docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
    - docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/app/models.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/extractors.py
    - src/mythic_edge_parser/app/sheet_schema.py

  Goal:
    Review the Codex C implementation against the #149 pre/postboard provenance contract.
    Confirm it is evidence-ledger metadata/test-only and does not change parser behavior.

  Confirm:
    - The three contracted pre/postboard seed fields are present.
    - Broad `pre_postboard` is removed from Tier 3 future fields.
    - Remaining deferred fields still include `sideboarding` and `deck_state`.
    - All three `tier3.pre_postboard.*` entries exist and validate.
    - Entries document game 1 as `Preboard` and games 2/3 as `Postboard`.
    - Entries document `Pre / Postboard` as derived from `GameSummary.game_number` and `GameSummary.to_game_log_row(...)`.
    - Direct evidence cites game-slot model state and game-log row serialization.
    - Fallback evidence cites game-number dependency, parser context fallback, and row-emission context.
    - Value-source policy uses `derived`, `unknown`, and `conflict` and excludes observed/inferred/legacy-enriched pre/postboard truth.
    - Degradation behavior documents missing/invalid game numbers, context-only fallback, conflicting slot evidence, missing row emission, `Postboard` without sideboarding-entered evidence, `Postboard` without submit-deck evidence, Best-of-One/unknown-format behavior, and truncated/partial log degradation.
    - #134, #137, #139, #140, #143, #145, and #147 entries remain present and valid.
    - All new evidence signals remain path-only and do not embed raw player values, raw logs, raw GameState payloads, raw timestamps from private logs, deck contents, sideboard contents, local artifacts, generated data, secrets, or workbook exports.
    - No parser behavior, game-number assignment, `GameSummary.to_game_log_row(...)`, literal `Pre / Postboard` values, sideboarding behavior, submitted-deck behavior, deck-state behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, feature-equity reports, runtime field-evidence attachment, or analytics truth changed.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py
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
    - Close issue #11 or issue #149.
    - Change parser/runtime/workbook/webhook/App Script/output behavior or protected surfaces.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/149"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/147"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/148"
  previous_merge_commit: "14c69c47a953387b0a4151aeff4b46a17aadae64"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md"
  verdict: "tier3_pre_postboard_provenance_metadata_implemented_ready_for_contract_review"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-pre-postboard"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #149."
    - "Do not change parser behavior, game-number assignment, GameSummary.to_game_log_row behavior, literal Pre / Postboard values, sideboarding behavior, submitted-deck behavior, deck-state behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, feature-equity reports, runtime field-evidence attachment, or analytics truth."
    - "Do not reconstruct missing sideboarding, submitted-deck, deck-state, game-slot, hidden-card, or match-format facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```
