# Player Log Evidence Ledger Tier 3 Timing And Duration Comparison

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/147
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/145
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/146
- Previous merge commit: `0aede4890710768c7abd2fb2a561c7ce8b10fdba`
- Base branch: `codex/parser-reliability-intelligence`
- Implementation branch: `codex/player-log-evidence-ledger-tier3-timing-duration`
- Source artifact: `docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md`
- Target artifact: `docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md`
- Risk tier: High
- Codex role: Codex C: Module Implementer

## Branch Gate Evidence

- Issue #147 is open.
- Current branch is `codex/player-log-evidence-ledger-tier3-timing-duration`.
- Current branch is even with `origin/codex/parser-reliability-intelligence`.
- Current head before implementation was `0aede48`, matching the previous #145 merge baseline.
- The contract source file was present as an untracked source artifact before implementation and was not modified by this pass.

## Confirmed Matches

- `src/mythic_edge_parser/app/evidence_ledger.py` already preserved the #128
  schema version, validators, vocabulary constants, privacy posture, and
  copy-safe build/iteration behavior.
- Existing #134 game-result, #137 participant/player-team, #139 play/draw,
  #140 mulligan, #143 opening-hand, and #145 turn-count entries were present
  and validating before the #147 slice.
- Current parser/model behavior already stores `GameSummary.first_event_time`,
  `GameSummary.last_event_time`, and derives `GameSummary.duration_seconds()`
  from those endpoints.
- Current behavior already treats game timing as parser observation-boundary
  data and serializes game-log `Game Duration` through the model; no behavior
  change was required to satisfy this metadata contract.

## Contract Mismatches Found And Fixed

- `game_level_facts.seed_fields` did not include the nine contracted
  game-level timing and duration fields.
- `game_level_facts.future_fields` still carried broad `game_timing` and
  `game_duration`, even though the #147 contract requires replacing those with
  granular seeded fields.
- The ledger did not have validating `tier3.game_timing.*` entries for
  per-game first/last observed event times.
- The ledger did not have validating `tier3.game_duration.*` entries for
  per-game duration seconds.
- Focused tests still treated timing/duration as deferred rather than seeded
  Tier 3 metadata.

## Changes Made

- Added nine Tier 3 seed fields:
  - `game1_first_event_time`, `game2_first_event_time`, `game3_first_event_time`
  - `game1_last_event_time`, `game2_last_event_time`, `game3_last_event_time`
  - `game1_duration_seconds`, `game2_duration_seconds`, `game3_duration_seconds`
- Removed broad `game_timing` and `game_duration` from Tier 3 future fields
  while preserving deferred `pre_postboard`, `sideboarding`, and `deck_state`.
- Added validating timing entries for:
  - `tier3.game_timing.game1_first_event_time`
  - `tier3.game_timing.game2_first_event_time`
  - `tier3.game_timing.game3_first_event_time`
  - `tier3.game_timing.game1_last_event_time`
  - `tier3.game_timing.game2_last_event_time`
  - `tier3.game_timing.game3_last_event_time`
- Added validating duration entries for:
  - `tier3.game_duration.game1_duration_seconds`
  - `tier3.game_duration.game2_duration_seconds`
  - `tier3.game_duration.game3_duration_seconds`
- Documented path-only timing evidence from GameState, ClientAction,
  GameResult, `EventMetadata.timestamp`, parser-state first/last endpoints,
  router timestamp-missing/parse-failure context, `_safe_iso` runtime fallback,
  and game-slot identity dependency.
- Documented duration evidence from `GameSummary.duration_seconds()`, stored
  first/last endpoint dependencies, model clamp behavior, and timestamp
  anomaly context.
- Added focused tests in `tests/test_evidence_ledger.py` for seeded fields,
  validating entries, source evidence, fallback evidence, policy vocabulary,
  invariant language, privacy posture, blank/zero/degraded semantics, remaining
  deferred scope, and preservation of prior Tier 3 slices.

## Boundaries Preserved

- No parser behavior changed.
- No timestamp parsing, duration calculation, state update behavior, GameState
  parsing, turn-info parsing, extractor behavior, parser state final
  reconciliation, or parser event classes changed.
- No workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, environment
  variables, raw logs, generated data, runtime status files, failed posts,
  workbook exports, production behavior, environment variable contracts, or
  AI/analytics truth changed.
- No pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay,
  drift, schema snapshot, invariant execution, or runtime field-evidence
  attachment behavior was added.
- No hidden cards, decklists, archetypes, gameplay advice, player mistakes,
  clock-pressure analysis, or AI truth were inferred.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - Result: passed, `55 passed`
- `python3 -m pytest -q tests/test_state.py tests/test_app_models.py tests/test_match_summary_from_match_state.py`
  - Result: passed, `42 passed`
- `python3 -m pytest -q`
  - Result: passed, `914 passed`
- `python3 -m ruff check src tests tools`
  - Result: passed, `All checks passed!`
- `git diff --check`
  - Result: passed
- `git diff --no-index --check /dev/null docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md`
  - Result: passed with no whitespace findings; command exit normalized because
    `--no-index` returns `1` for a new-file diff.
- `python3 tools/check_protected_surfaces.py --base origin/main`
  - Result: passed, `forbidden: 0`, `warnings: 12`
  - Note: warnings are from accumulated parser-reliability integration branch
    changes relative to `origin/main`; this module changed only
    `src/mythic_edge_parser/app/evidence_ledger.py`,
    `tests/test_evidence_ledger.py`, and this handoff artifact.

## Still-Unverified Layers

- Runtime field-evidence attachment is intentionally not implemented in #147.
- Drift reports, schema snapshots, diagnostics reports, replay reports,
  feature-equity reports, timing analytics, clock-pressure analytics, and
  invariant execution are intentionally deferred.
- This metadata does not prove individual live matches have clean timestamp
  evidence; it documents the parser-owned provenance contract for future
  evidence attachment.
- `_safe_iso(...)` runtime-clock fallback remains current behavior and is
  documented as degraded/review-required rather than repaired in this issue.

## Remaining Risks

- First and last observed parser events may not equal true Arena internal game
  start/end when logs are truncated, summarized, rotated, or missing early/late
  entries.
- `Game Duration` can be blank because endpoints are missing or unparseable;
  blank remains unknown/unavailable, not zero.
- `Game Duration` can be `0` when endpoints are equal or out of order and
  clamped; this is reviewable, not proof of a real zero-second game.
- Game-log row `timestamp` can fall back to match-level timing when game-level
  last-event time is absent; the ledger documents this as reviewable context.
- Protected-surface warnings remain present when comparing the full integration
  branch to `origin/main`; there are no forbidden protected-surface changes
  from this implementation slice.

## Next Recommended Role

Next role: Codex E: Module Reviewer in contract-test mode.

Codex E should verify that the #147 implementation stayed metadata/test-only,
that all nine timing/duration entries validate and preserve privacy
boundaries, and that no parser behavior or protected downstream surfaces
changed.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer in contract-test mode for issue #147, Tier 3 timing/duration provenance under issue #11.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/147
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/145
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/146
    - Previous merge commit: 0aede4890710768c7abd2fb2a561c7ce8b10fdba
    - Base branch: codex/parser-reliability-intelligence
    - Implementation branch: codex/player-log-evidence-ledger-tier3-timing-duration
    - Contract: docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
    - Implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md

  Use:
    - docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
    - docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/router.py
    - src/mythic_edge_parser/app/extractors.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/models.py

  Goal:
    Review the Codex C implementation against the #147 timing/duration provenance contract.
    Confirm it is evidence-ledger metadata/test-only and does not change parser behavior.

  Confirm:
    - The nine contracted timing/duration seed fields are present.
    - Broad `game_timing` and `game_duration` are removed from Tier 3 future fields.
    - All six `tier3.game_timing.*` entries exist and validate.
    - All three `tier3.game_duration.*` entries exist and validate.
    - Timing entries document first/latest observed parser event endpoints, not Arena internal start/end times.
    - Direct timing evidence cites GameState, ClientAction, GameResult event timestamps and parser-state first/last endpoint surfaces.
    - Timing fallback evidence cites router timestamp-missing and parse-failure counters, `_safe_iso` runtime-clock fallback, and game-slot identity dependency.
    - Duration entries document `GameSummary.duration_seconds()` and first/last endpoint dependencies.
    - Duration fallback evidence cites clamp behavior and timestamp anomaly context.
    - Blank duration is documented as unknown/unavailable, not zero.
    - Zero duration is documented as reviewable when endpoints are equal or clamped.
    - `inferred` and `legacy_enriched` are not used as timing/duration truth paths.
    - #134, #137, #139, #140, #143, and #145 entries remain present and valid.
    - All new evidence signals remain path-only and do not embed raw player values, raw logs, raw GameState payloads, raw timestamps from private logs, local artifacts, generated data, secrets, or workbook exports.
    - No parser behavior, timestamp parsing, duration calculation, state update behavior, GameState parsing, turn-info parsing, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth changed.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_state.py tests/test_app_models.py tests/test_match_summary_from_match_state.py
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
    - Close issue #11 or issue #147.
    - Change parser/runtime/workbook/webhook/App Script/output behavior or protected surfaces.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/147"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/145"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/146"
  previous_merge_commit: "0aede4890710768c7abd2fb2a561c7ce8b10fdba"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md"
  verdict: "tier3_timing_duration_provenance_metadata_implemented_ready_for_contract_review"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-timing-duration"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_app_models.py tests/test_match_summary_from_match_state.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #147."
    - "Do not change parser behavior, timestamp parsing, duration calculation, state update behavior, GameState parsing, turn-info parsing, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not rework, remove, or weaken prior Tier 3 provenance entries."
    - "Do not map pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshots, invariant execution, or runtime field-evidence attachment beyond what the #147 contract explicitly requires."
    - "Do not infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, clock-pressure analysis, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```
