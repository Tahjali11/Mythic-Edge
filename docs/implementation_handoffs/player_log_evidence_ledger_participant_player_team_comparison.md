# Player Log Evidence Ledger Participant Player-Team Comparison

Codex C: Module Implementer

## Summary

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/137
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
Source contract: `docs/contracts/player_log_evidence_ledger_participant_player_team.md`
Implementation branch: `codex/player-log-evidence-ledger-participant-player-team`
Base branch: `codex/parser-reliability-intelligence`
Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/134
Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/135
Previous merge commit: `9697a666f60fc60a8c13892b9815fd692056e298`

This pass compared the current evidence-ledger registry and focused tests against the participant/player-team provenance contract. The contract required metadata and focused-test changes only. No parser behavior, local player selection behavior, `LOCAL_PLAYER_INDEX` semantics, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, opponent-card observation behavior, gameplay actor-relation behavior, runtime schemas, failed-post artifacts, workbook exports, production behavior, or AI/analytics truth were changed.

## Confirmed Matches

- The #128 evidence-ledger schema, vocabulary constants, validators, privacy posture, deterministic serialization, and `match_id` anchor entry were preserved.
- The #130 match lifecycle/result/sync entries were preserved.
- The #132 game aggregate entries were preserved.
- The #134 Tier 3 game-result entries were preserved.
- Current parser behavior already exposes the referenced participant surfaces:
  - MatchState selected local player data.
  - GameState `system_seat_ids` and player records.
  - ClientAction team fields.
  - parser context carry-forward through `_CONTEXT["current_player_team"]`.
  - `MatchSummary.player_team` and `MatchSummary.opponent_team()`.
  - gameplay local-seat tracking and opponent-card missing-seat degradation.
- The contract did not require parser logic changes.

## Contract Mismatches Found And Fixed

- `match_identity_and_lifecycle.seed_fields` did not include participant dependency fields.
  - Added `player_team`, `opponent_team`, `local_system_seat_id`, and `participant_team_mapping`.
- Participant provenance entries were missing.
  - Added `tier1.participants.player_team`.
  - Added `tier1.participants.opponent_team`.
  - Added `tier1.participants.local_system_seat_id`.
  - Added `tier1.participants.participant_team_mapping`.
- Existing match result, aggregate, and game result entries only referenced generic `MatchSummary.player_team`.
  - Added explicit `ledger.tier1.participants.player_team_dependency` signals and #137 notes to the dependent entries.

## Missing Safeguards Addressed

- Participant entries now document unknown-like values for provenance: `None`, blank strings, whitespace-only strings, zero, string zero, and booleans.
- `player_team` metadata now states that known match or game winners do not repair missing participant evidence.
- `opponent_team` metadata now documents derivation only from known local `player_team` and no inference when local team is unknown.
- `local_system_seat_id` metadata now documents GameState, MatchState, and gameplay carry-forward sources plus missing/conflicting seat degradation.
- `participant_team_mapping` metadata now documents MatchState, GameState, ClientAction, parser context, and opponent-card missing-seat-mapping dependencies without inferring hidden information.

## Tests Added Or Strengthened

- Updated Tier 1 seed-field and entry-id tests for participant fields.
- Added focused tests for all four new participant entries validating:
  - entry existence and validator compatibility.
  - source signal IDs.
  - path-only privacy posture.
  - unknown/degraded participant values.
  - opponent-team derivation from player-team provenance.
  - local-seat raw-path coverage and degradation language.
  - participant/team mapping dependencies across MatchState, GameState, ClientAction, parser context, gameplay, and opponent-card observations.
- Updated existing dependency tests so match result, games won/lost, match win flag, game win rate, and game result entries explicitly cite `tier1.participants.player_team`.

## Still-Unverified Layers

- Runtime field-evidence attachment remains deferred.
- Drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, and feature-equity report changes remain deferred.
- Play/draw, opening-hand ownership, opponent-card observation ledger entries, and analytics consumer rules remain future work.
- Protected-surface gate reported warning-only historical branch changes outside this issue's touched files; `forbidden` was `0`.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - Passed: 34 tests.
- `python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py`
  - Passed: 72 tests.
- `python3 -m pytest -q`
  - Passed: 893 tests.
- `python3 -m ruff check src tests tools`
  - Passed.
- `python3 tools/check_protected_surfaces.py --base origin/main`
  - Passed with `forbidden: 0`, `warnings: 12`.
- `git diff --check`
  - Passed after this handoff file was written.

## Open Risks

- The source contract `docs/contracts/player_log_evidence_ledger_participant_player_team.md` is currently an untracked artifact in this worktree and should be included intentionally by reviewer/submitter workflow if it is part of the PR package.
- The ledger remains metadata-only and does not emit runtime field evidence.
- This implementation does not decide merge readiness, deploy readiness, issue closure, tracker completion, or downstream workbook correctness.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #137, participant/player-team provenance under issue #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/137
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/134
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/135
- Previous merge commit: 9697a666f60fc60a8c13892b9815fd692056e298
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-participant-player-team
- Contract: docs/contracts/player_log_evidence_ledger_participant_player_team.md
- Handoff: docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md

Use:
- docs/contracts/player_log_evidence_ledger_participant_player_team.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_state.py
- tests/test_app_extractors.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py

Goal:
Verify the Codex C implementation against the participant/player-team evidence-ledger contract.

Confirm:
- The #128 schema, validators, vocabulary constants, privacy posture, and match_id anchor entry are preserved.
- The #130, #132, and #134 ledger entries are preserved.
- `match_identity_and_lifecycle.seed_fields` includes `player_team`, `opponent_team`, `local_system_seat_id`, and `participant_team_mapping`.
- New entries exist and validate for:
  - `tier1.participants.player_team`
  - `tier1.participants.opponent_team`
  - `tier1.participants.local_system_seat_id`
  - `tier1.participants.participant_team_mapping`
- Participant entries use existing vocabulary only and remain path-only with no raw player values.
- `player_team` documents MatchState, GameState, ClientAction, parser context, unknown-like values, and stale/context limits.
- `opponent_team` is derived from player_team only and does not infer hidden information.
- `local_system_seat_id` documents GameState `systemSeatIds[0]`, MatchState selected local player seat, gameplay carry-forward, and missing/conflicting seat degradation.
- `participant_team_mapping` documents MatchState, GameState, ClientAction, parser context, and opponent-card missing-seat-mapping dependencies.
- Existing match result, aggregate, and game result entries explicitly cite `tier1.participants.player_team`.
- No parser behavior, local player selection behavior, `LOCAL_PLAYER_INDEX` semantics, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, opponent-card observation behavior, gameplay actor-relation behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or AI/analytics truth changed.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
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
- A workflow_handoff block.

Do not target main directly.
Do not close issue #11.
Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth.
Do not change local player selection behavior or LOCAL_PLAYER_INDEX semantics.
Do not change opponent-card observation behavior or gameplay actor-relation behavior.
Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth.
Do not commit raw private Player.log excerpts or local diagnostics artifacts.
Do not stage, commit, merge, or push unless explicitly asked.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/137"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/134"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/135"
  previous_merge_commit: "9697a666f60fc60a8c13892b9815fd692056e298"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_participant_player_team.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md"
  verdict: "ready_for_module_reviewer"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-participant-player-team"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not change local player selection behavior or LOCAL_PLAYER_INDEX semantics."
    - "Do not change opponent-card observation behavior or gameplay actor-relation behavior."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```
