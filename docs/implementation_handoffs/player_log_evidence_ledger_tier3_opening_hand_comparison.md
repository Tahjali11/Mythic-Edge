# Player Log Evidence Ledger Tier 3 Opening-Hand Comparison

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/142
- Previous merge commit: `33a8bc2cba188389fe885b2446da51ac48c8555e`
- Base branch: `codex/parser-reliability-intelligence`
- Implementation branch: `codex/player-log-evidence-ledger-tier3-opening-hand`
- Source artifact: `docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md`
- Target artifact: `docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md`
- Risk tier: High
- Codex role: Codex C: Module Implementer; Codex D: Module Fixer follow-up

## Branch Gate Evidence

- PR #142 is merged into `codex/parser-reliability-intelligence`.
- Merge commit `33a8bc2cba188389fe885b2446da51ac48c8555e` is an ancestor of
  `origin/codex/parser-reliability-intelligence`.
- Current branch is even with `origin/codex/parser-reliability-intelligence` before
  the issue #143 implementation changes.
- The contract source file was present as an untracked source artifact before
  implementation and was not modified by this pass.

## Confirmed Matches

- `src/mythic_edge_parser/app/evidence_ledger.py` already preserved the #128
  schema version, validators, vocabulary constants, privacy posture, and
  copy-safe build/iteration behavior.
- Existing #134 game-result entries, #139 play/draw entries, and #140 mulligan
  entries were present and validating before the #143 slice.
- Current parser/model behavior already exposes opening-hand surfaces through
  `GameSummary.opening_hand_size()`, `GameSummary.opening_hand`,
  `GameSummary.mulliganed_away`, `MatchSummary.set_game_opening_hand()`, and
  `MatchSummary.add_game_mulliganed_away()`.
- Current parser state already records local private-hand snapshots, applies
  turn-one and expected-size checks, resolves instance-to-GRP/card names, and
  records discarded/bottomed mulliganed-away evidence. No behavior change was
  required to satisfy the metadata contract.
- Codex D follow-up fixed the Codex E blocking display-name finding: all nine
  `tier3.opening_hand.*` entries now use the contracted row-facing display
  names `Opening Hand Size`, `Opening Hand`, and `Mulliganed Away`, and focused
  tests lock those names.

## Contract Mismatches Found And Fixed

- `game_level_facts.seed_fields` did not include the nine granular opening-hand
  fields required by the #143 contract.
- `game_level_facts.future_fields` still carried broad `opening_hand`, even
  though the #143 contract requires replacing that broad future field with
  granular seeded fields.
- The ledger did not have validating `tier3.opening_hand.*` entries for:
  `gameN_opening_hand_size`, `gameN_opening_hand`, and
  `gameN_mulliganed_away`.
- Focused tests still asserted that opening-hand provenance was deferred after
  #140 and that no opening-hand/mulliganed-away Tier 3 entries existed.
- Codex E found a display-name mismatch after implementation: opening-hand
  entries used game-prefixed labels instead of the contracted row-facing
  aliases.

## Changes Made

- Added nine Tier 3 opening-hand seed fields:
  `game1_opening_hand_size`, `game2_opening_hand_size`,
  `game3_opening_hand_size`, `game1_opening_hand`, `game2_opening_hand`,
  `game3_opening_hand`, `game1_mulliganed_away`, `game2_mulliganed_away`, and
  `game3_mulliganed_away`.
- Removed broad `opening_hand` from Tier 3 future fields while preserving
  deferred `turn_count`, `game_timing`, `game_duration`, `pre_postboard`,
  `sideboarding`, and `deck_state`.
- Added validating entries for all nine `tier3.opening_hand.*` fields.
- Documented path-only evidence for local private-hand zones, hand instance-id
  paths, instance-to-GRP lookup, card-name resolution, snapshot history,
  opening-hand size fallback, and mulliganed-away discarded/bottomed evidence.
- Made #137 participant/local-seat dependencies, #134 game slot dependencies,
  and #140 mulligan dependencies explicit in the new metadata.
- Updated #140 mulligan notes to identify opening-hand fields as downstream
  consumers documented by #143, not count evidence.
- Added focused tests in `tests/test_evidence_ledger.py` for seeded fields,
  validating entries, fallback/dependency language, placeholder/blank behavior,
  privacy posture, remaining deferred scope, and preservation of #139/#140
  entries.
- Updated the nine opening-hand `display_name` values to match the contract:
  `Opening Hand Size`, `Opening Hand`, and `Mulliganed Away`.
- Updated focused tests to assert the contracted display names.

## Missing Safeguards Addressed

- Added metadata language that malformed owner-seat evidence cannot support
  high-confidence local ownership.
- Added metadata language that placeholder-containing exact lists are degraded
  and may serialize blank.
- Added metadata language that opening-hand size fallback is derived from #140
  mulligan provenance and is not exact-card-list evidence.
- Added metadata language that mulliganed-away cards are not evidence for
  mulligan count and must not rewrite #140.
- Added path-only privacy assertions in focused tests for every new evidence
  signal.

## Boundaries Preserved

- No parser behavior changed.
- No local private-hand extraction behavior changed.
- No opening-hand selection behavior changed.
- No mulligan counting or ClientAction parsing behavior changed.
- No mulliganed-away capture behavior changed.
- No card-name resolution, GRP catalog behavior, or generated card data changed.
- No parser state final reconciliation, parser event classes, workbook schema,
  webhook payload shape, Apps Script behavior, output transport, match/game
  identity, deduplication, secrets, raw logs, runtime status files, failed posts,
  workbook exports, production behavior, environment variable contracts, or
  AI/analytics truth changed.
- No raw card names, raw hand lists, raw player values, raw object-instance
  values, raw GRP values, or raw private Player.log excerpts were added.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - Result: passed, `47 passed in 0.22s`
- `python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py`
  - Result: passed, `107 passed in 0.13s`
- `python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py`
  - Result: passed, `35 passed in 0.11s`
- `python3 -m pytest -q tests/test_golden_replay_harness.py`
  - Result: passed, `13 passed in 0.15s`
- `python3 -m pytest -q`
  - Result: passed, `906 passed in 1.22s`
- `python3 -m ruff check src tests tools`
  - Result: passed, `All checks passed!`
- `git diff --check`
  - Result: passed
- Path-scoped protected-surface check for reviewed files
  - Result: passed, `5 changed paths`, `forbidden: 0`, `warnings: 0`
- `python3 tools/check_protected_surfaces.py --base origin/main`
  - Result: passed, `forbidden: 0`, `warnings: 12`
  - Note: warnings are from accumulated parser-reliability integration branch
    changes relative to `origin/main`; this module changed only
    `src/mythic_edge_parser/app/evidence_ledger.py`,
    `tests/test_evidence_ledger.py`, and this handoff artifact.

## Still-Unverified Layers

- Runtime field-evidence attachment is intentionally not implemented in #143.
- Drift reports, schema snapshots, diagnostics reports, replay reports,
  feature-equity reports, and invariant execution are intentionally deferred.
- This metadata does not prove individual live matches have clean opening-hand
  evidence; it documents the parser-owned provenance contract for future
  evidence attachment.

## Remaining Risks

- Existing parser extraction can accept malformed or missing owner-seat evidence
  in some cases; #143 documents that as degraded/review-required metadata but
  does not change extraction behavior.
- Placeholder-containing exact lists may exist in parser state while row
  serialization is blank. The metadata now distinguishes blank display from
  evidence absence, but runtime field-evidence is deferred.
- Protected-surface warnings remain present when comparing the full integration
  branch to `origin/main`; there are no forbidden protected-surface changes from
  this implementation slice.

## Next Recommended Role

Next role: Codex E: Module Reviewer in contract-test mode.

Codex E should verify that the #143 implementation stayed metadata/test-only,
that all nine opening-hand entries validate and preserve privacy boundaries,
and that no parser behavior or protected downstream surfaces changed.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer in contract-test mode for issue #143, Tier 3 opening-hand provenance under issue #11.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/142
    - Previous merge commit: 33a8bc2cba188389fe885b2446da51ac48c8555e
    - Base branch: codex/parser-reliability-intelligence
    - Implementation branch: codex/player-log-evidence-ledger-tier3-opening-hand
    - Contract: docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
    - Implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md

  Use:
    - docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
    - docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/app/extractors.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/models.py
    - src/mythic_edge_parser/app/grp_id_catalog.py

  Goal:
    Review the Codex C implementation and Codex D display-name fixer pass against the #143 opening-hand provenance contract.
    Confirm it is evidence-ledger metadata/test-only and does not change parser behavior.

  Confirm:
    - PR #142 merge commit is present in the base branch.
    - The nine contracted opening-hand seed fields are present.
    - Broad `opening_hand` is removed from Tier 3 future fields.
    - All nine `tier3.opening_hand.*` entries exist and validate.
    - All nine `tier3.opening_hand.*` entries use the contracted display names: `Opening Hand Size`, `Opening Hand`, and `Mulliganed Away`.
    - Opening-hand size entries distinguish observed exact length from derived #140 mulligan fallback.
    - Exact opening-hand entries cite local private-hand zone, instance-id, instance-to-GRP, card-name resolution, and #137 participant/local-seat dependencies.
    - Mulliganed-away entries cite discarded/latest snapshot and bottomed-card difference evidence while not claiming to determine mulligan counts.
    - Placeholder-containing lists, unplayed-slot blanks, malformed owner-seat evidence, and missing private-hand evidence are documented as degraded or expected behavior.
    - All new evidence signals remain path-only and do not embed raw hand contents, raw card lists, raw instance id values, raw GRP values, raw logs, generated data, or local artifacts.
    - #134, #139, and #140 entries remain present and valid.
    - No parser behavior, local private-hand extraction behavior, opening-hand selection behavior, mulligan counting behavior, ClientAction parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth changed.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py
    - python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py
    - python3 -m pytest -q tests/test_golden_replay_harness.py
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
    - Close issue #11 or issue #143.
    - Change parser/runtime/workbook/webhook/App Script/output behavior or protected surfaces.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/143"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/142"
  previous_merge_commit: "33a8bc2cba188389fe885b2446da51ac48c8555e"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md"
  target_artifact: "src/mythic_edge_parser/app/evidence_ledger.py; tests/test_evidence_ledger.py"
  verdict: "fixer_pass_ready_for_module_reviewer"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-opening-hand"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py -> 47 passed in 0.22s"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py -> 107 passed in 0.13s"
    - "python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py -> 35 passed in 0.11s"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 13 passed in 0.15s"
    - "python3 -m pytest -q -> 906 passed in 1.22s"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, 5 changed paths, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #143."
    - "Do not change parser behavior, local private-hand extraction behavior, opening-hand selection behavior, mulligan counting behavior, ClientAction parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move parser truth into AI/analytics truth."
```
