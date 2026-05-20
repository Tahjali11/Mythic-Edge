# Player.log Evidence Ledger Tier 1 Match Lifecycle Comparison

## Metadata

- role: Codex C / Module Implementer; Codex D / Module Fixer follow-up
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/130
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/128
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/129
- source_artifact: docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- existing_schema_contract: docs/contracts/player_log_evidence_ledger_schema.md
- implementation_branch: codex/player-log-evidence-ledger-tier1-match-lifecycle
- base_branch: codex/parser-reliability-intelligence
- risk_tier: High

## Summary

The pre-implementation ledger matched the issue #128 schema contract and had one
valid Tier 1 anchor entry for `tier1.match_identity.match_id`. It did not yet
map the issue #130 Tier 1 lifecycle/result fields. This implementation expands
the registry metadata only: no parser behavior, parser state reconciliation,
event classes, workbook schema, webhook payloads, Apps Script behavior, output
transport, runtime artifacts, raw logs, or downstream truth surfaces were
changed.

Codex D follow-up fixed the Codex E blocking metadata-provenance finding: the
GameResult direct match-scope winner evidence now points at the parser-produced
raw source shape under `greToClientMessages[].gameStateMessage.gameInfo.results[]`
instead of `gameStateMessage.results[]`.

## Confirmed Matches Before Editing

- The issue #128 public constants, schema version, ledger version, validators,
  and vocabulary constants were present and preserved.
- The top-level ledger object still uses issue #128 as `source_issue`, as the
  issue #130 contract allows because #128 remains the schema origin.
- The `tier1.match_identity.match_id` entry was present and valid.
- The `match_id` entry preserved direct evidence from `MatchState`,
  `GameState`, and `GameResult`, plus the parser-context fallback.
- Existing parser state/model surfaces already own the current lifecycle fields:
  `MatchSummary.first_event_time`, `last_event_time`, `match_winner_team`,
  `match_wl`, `is_ready()`, and `to_match_log_row(final=...)`.
- Existing state tests already cover live/final sync status, nested match-scope
  winner precedence, top-level winner fallback gating, and unknown winner
  preservation.

## Contract Mismatches Found

- Tier 1 family metadata listed only `match_id` as a seed field and kept
  `match_started_at`, `match_finished_at`, `match_winner_team`, `match_result`,
  and `match_sync_status` in `future_fields`.
- The ledger had no entries for:
  - `tier1.match_lifecycle.match_started_at`
  - `tier1.match_lifecycle.match_finished_at`
  - `tier1.match_result.match_winner_team`
  - `tier1.match_result.match_result`
  - `tier1.match_lifecycle.match_sync_status`
- Focused tests still assumed the ledger contained exactly one entry.
- Focused tests did not verify derived aggregate deferral, the legacy `MGTA
  Start Time` spelling, result/sync derived-source policy, or match-winner
  precedence metadata.
- Codex E found one blocking metadata mismatch after implementation:
  `game_result.results.match_scope_winner` used the wrong raw payload path for
  GameResult result evidence.

## Changes Made

- Updated `src/mythic_edge_parser/app/evidence_ledger.py` so Tier 1
  `match_identity_and_lifecycle` seed fields now include the six contracted
  fields:
  - `match_id`
  - `match_started_at`
  - `match_finished_at`
  - `match_winner_team`
  - `match_result`
  - `match_sync_status`
- Kept derived aggregate fields deferred in Tier 1 `future_fields`:
  - `games_won`
  - `games_lost`
  - `total_games`
  - `match_win_flag`
  - `game_win_rate`
- Preserved the #128 `match_id` anchor entry and updated only its notes.
- Added metadata-only ledger entries for the five issue #130 fields:
  - `match_started_at`: explicit match-start timestamp plus
    `MatchSummary.first_event_time` fallback.
  - `match_finished_at`: final result or match-complete timestamp plus
    `MatchSummary.last_event_time` fallback.
  - `match_winner_team`: nested match-scope winner precedence, top-level
    match-complete fallback, unknown winner semantics, and no game aggregation.
  - `match_result`: derived from `match_winner_team` and `player_team`, not
    directly observed as win/loss.
  - `match_sync_status`: derived from parser-state readiness/live-row
    construction, not raw log evidence or transport state.
- Updated `tests/test_evidence_ledger.py` with focused coverage for expanded
  Tier 1 entries, source policies, aggregate deferral, copy safety, privacy, and
  deterministic serialization.
- Corrected the GameResult direct match-scope winner `raw_payload_path` to
  `greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId`.
- Added focused regression coverage asserting both GameResult winner evidence
  paths use the parser-produced `gameInfo.results[]` raw shape.

## Missing Safeguards

No missing safeguards remain for the issue #130 registry-only scope. The ledger
still rejects absolute paths and raw-log-like/private text through existing
privacy validation, and the new entries use repo-relative or symbolic paths.

## Missing Or Weak Tests

- Fixed: focused tests now assert the six Tier 1 entries, required signal IDs,
  aliases, derived policies, and deferred aggregate fields.
- Fixed by Codex D: focused tests now assert GameResult direct and fallback
  winner evidence raw paths.
- Existing adjacent state tests remain the behavioral proof for winner
  precedence, unknown winner handling, and sync status behavior.
- Still intentionally absent: runtime field-evidence attachment tests, drift
  report tests, schema snapshot tests, diagnostics report tests, replay report
  tests, and feature-equity report tests. These are explicitly out of scope for
  issue #130.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - passed: 20 tests in 0.08s
- `python3 -m pytest -q tests/test_state.py`
  - passed: 18 tests in 0.29s
- `python3 -m ruff check src tests tools`
  - passed
- `git diff --check`
  - passed
- Path-scoped protected-surface check for reviewed files
  - passed: 5 changed paths, forbidden 0, warnings 0
- `python3 -m pytest -q`
  - passed: 879 tests in 3.12s

## Still-Unverified Layers

- Runtime field-evidence attachment remains unimplemented by design.
- Drift reports, invariant execution, schema snapshots, diagnostics reports,
  replay reports, and feature-equity reports remain out of scope.
- Participant/player-team provenance remains referenced as a dependency for
  `match_result`, but full participant provenance mapping is not part of this
  Tier 1 lifecycle slice.
- Game-derived aggregate field provenance remains deferred to a later
  game-result or aggregate provenance issue.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #130, Tier 1
match lifecycle evidence ledger expansion under tracker #11.

Use:
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_state.py

Goal:
Verify the Codex C implementation and Codex D metadata-provenance fixer pass
against the Tier 1 match lifecycle evidence ledger contract. Confirm the
registry expands only metadata and tests, preserves the #128
schema/vocabulary/match_id anchor, adds the five issue #130 entries, keeps
aggregate fields deferred, and does not change parser/runtime/workbook
behavior.

Confirm:
- The six contracted Tier 1 fields are mapped in the output-family metadata.
- The #128 `tier1.match_identity.match_id` entry is preserved.
- Entries exist for `match_started_at`, `match_finished_at`,
  `match_winner_team`, `match_result`, and `match_sync_status`.
- All new entries use only existing value-source, confidence, finality,
  invariant-status, and drift-flag vocabulary.
- `MGTA Start Time` keeps the legacy workbook spelling.
- `MTGA End Time` documents live-row blank behavior.
- `match_winner_team` documents nested match-scope precedence, top-level
  match-complete fallback, and unknown winner values.
- GameResult match-winner direct and fallback raw payload paths both point at
  `greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId`.
- `match_result` is documented as derived from winner plus local player team.
- `match_sync_status` is documented as parser-state derived.
- Derived aggregate fields are not represented as fully mapped entries.
- Existing validators, privacy checks, copy safety, and deterministic
  serialization still pass.
- No parser behavior, parser state final reconciliation, parser event classes,
  workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, raw logs, generated
  data, runtime status files, failed posts, workbook exports, or AI/analytics
  truth changed.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_state.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped protected-surface check for reviewed files
- python3 -m pytest -q

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F if no blocking findings, otherwise Codex D or
  Codex B.
- workflow_handoff block.

Do not target main directly.
Do not close issue #11.
Do not stage, commit, push, or open a PR unless explicitly asked.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/130"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/129"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_tier1_match_lifecycle.md"
  target_artifact: "src/mythic_edge_parser/app/evidence_ledger.py; tests/test_evidence_ledger.py; docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md"
  verdict: "fixer_pass_ready_for_module_reviewer"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier1-match-lifecycle"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py -> 20 passed in 0.08s"
    - "python3 -m pytest -q tests/test_state.py -> 18 passed in 0.29s"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, 5 changed paths, forbidden 0, warnings 0"
    - "python3 -m pytest -q -> 879 passed in 3.12s"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth."
    - "Do not reconstruct missing GameState data or infer facts that the Player.log did not provide."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes."
    - "Do not commit raw private Player.log excerpts."
```
