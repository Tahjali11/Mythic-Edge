# Player.log Evidence Ledger Tier 4 Sideboarding / Submit-Deck Signal Comparison

## Metadata

- role: Codex C / Module Implementer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/151
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- source_artifact: docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- target_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier4-sideboarding-submit-deck
- risk_tier: High
- branch_check: `HEAD 1b26490`, `HEAD...origin/codex/parser-reliability-intelligence` = `0 0`

## Summary

The implementation matched the existing parser/runtime behavior described by the contract:
`ClientAction` parsing, parser state updates, `MatchSummary` booleans, and row serialization already supported
`sideboarding_entered` and `submit_deck_seen`.

The evidence ledger metadata and focused tests did not yet map those two fields as Tier 4 seeded provenance.
This pass updates only the evidence-ledger registry and focused ledger tests.

## Confirmed Matches

- `src/mythic_edge_parser/parsers/client_actions.py` already recognizes `ClientMessageType_SubmitDeckResp`
  as `submit_deck_resp` and preserves generic GRE client-action message types.
- `src/mythic_edge_parser/app/state.py` already ignores ClientAction events without current match context.
- `state.py` already sets `MatchSummary.sideboarding_entered` from generic
  `ClientMessageType_EnterSideboardingReq`.
- `state.py` already sets `MatchSummary.submit_deck_seen` from `submit_deck_resp` or generic
  `ClientMessageType_SubmitDeckResp`.
- `src/mythic_edge_parser/app/models.py` already serializes final false booleans as `No` and live false
  booleans as blank for `MTGA Sideboard Entered` and `MTGA Submit Deck Seen`.
- `src/mythic_edge_parser/app/sheet_schema.py` already contains the workbook-facing sync field names.
- Prior Tier 1 and Tier 3 evidence-ledger entries remain present and validate cleanly.

## Contract Mismatches Fixed

- Tier 4 `sideboarding_and_deck_state` was still `registered_future`; it is now `seeded_sample`.
- Tier 4 `seed_fields` was empty; it now includes only:
  - `sideboarding_entered`
  - `submit_deck_seen`
- Tier 4 `future_fields` still listed `sideboarding_entered` and `submit_deck_seen`; those moved to seeds.
- Tier 4 now keeps only `submitted_deck_cards` deferred.
- Tier 3 `game_level_facts.future_fields` still listed broad `sideboarding`; it now keeps only `deck_state`.
- The validator expected Tier 4 to remain `registered_future`; it now expects `seeded_sample`.
- The ledger lacked entries for:
  - `tier4.sideboarding_submit_deck.sideboarding_entered`
  - `tier4.sideboarding_submit_deck.submit_deck_seen`

## Changes Made

- Updated `src/mythic_edge_parser/app/evidence_ledger.py`.
  - Added Tier 4 sideboarding/submit-deck family seed metadata.
  - Added two validating Tier 4 entries with direct/fallback evidence, value-source policy, confidence/finality policy,
    invariants, degradation behavior, drift flags, review modules, tests, and notes.
  - Documented final `No` as derived parser-state absence, not absolute source-log absence proof.
  - Documented live blank as provisional absence.
  - Kept submitted deck card contents and broader deck-state provenance deferred.
- Updated `tests/test_evidence_ledger.py`.
  - Added Tier 4 constants and focused coverage for family status, seed/future fields, entry existence, validation,
    evidence signals, privacy, value-source policy, final `No`, and downstream truth boundaries.
  - Updated prior Tier 3 scope tests to expect broad `sideboarding` to be removed from Tier 3 future fields.

## Boundaries Preserved

- No parser behavior changed.
- No ClientAction parsing behavior changed.
- No parser state final reconciliation changed.
- No parser event classes changed.
- No workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication,
  secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports,
  production behavior, or AI/analytics truth changed.
- No submitted deck card contents, sideboard deltas, deck signatures, deck-state snapshots, archetypes, sideboard plans,
  gameplay advice, or AI interpretation were mapped as parser truth.
- Pre/postboard remains Tier 3 game-slot-derived metadata and is not treated as sideboarding proof.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - result: passed, `64 passed`
- `python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py`
  - result: passed, `61 passed`
- `python3 -m pytest -q tests/test_client_actions_parser.py tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py`
  - result: passed, `116 passed`
- `python3 -m pytest -q`
  - result: passed, `923 passed`
- `python3 -m ruff check src tests tools`
  - result: passed
- `git diff --check`
  - result: passed
- `python3 tools/check_protected_surfaces.py --base origin/main`
  - result: passed, `forbidden: 0`, `warnings: 12`
  - note: warnings are integration-branch protected-surface warnings from prior parser-reliability changes relative to
    `origin/main`; this #151 pass touched only `evidence_ledger.py`, `test_evidence_ledger.py`, and this handoff.

## Still-Unverified Layers

- CI was not run in this local Codex C pass.
- No live/private Player.log excerpts were used or committed.
- Runtime field-evidence attachment remains out of scope.
- Submitted deck card contents and broader deck-state provenance remain deferred.
- GitHub issue/PR closure, tracker updates, staging, committing, pushing, and PR creation remain out of scope for Codex C.

## Worktree Notes

- Pre-existing untracked source artifact remains present:
  - `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- New implementation handoff artifact:
  - `docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md`
- No files were staged or committed.

## Next Recommended Role

Next role: Codex E / Module Reviewer in contract-test mode.

Use Codex D only if Codex E finds a concrete blocker. Use Codex F only after review passes.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #151, Tier 4 sideboarding / submit-deck signal provenance under issue #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/151
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier4-sideboarding-submit-deck
- Contract: docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- Handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md

Use:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_client_actions_parser.py
- tests/test_app_models.py
- tests/test_state.py
- tests/test_sheet_schema.py

Goal:
Verify the Codex C implementation against the Tier 4 sideboarding / submit-deck signal provenance contract.

Confirm:
- Tier 4 sideboarding_and_deck_state is seeded_sample.
- Tier 4 seed_fields include exactly sideboarding_entered and submit_deck_seen.
- Tier 4 future_fields no longer include sideboarding_entered or submit_deck_seen.
- Tier 4 future_fields still include submitted_deck_cards.
- Tier 3 future_fields no longer include broad sideboarding and still include deck_state.
- Existing Tier 1 and Tier 3 seed fields and entries remain present.
- Entries tier4.sideboarding_submit_deck.sideboarding_entered and tier4.sideboarding_submit_deck.submit_deck_seen exist and validate.
- Direct evidence documents ClientMessageType_EnterSideboardingReq, submit_deck_resp, ClientMessageType_SubmitDeckResp, MatchSummary booleans, and workbook-facing row fields.
- Both entries use direct observed, fallback derived, missing unknown, and contradiction conflict.
- Both entries document final No as derived row value, not absolute source-log absence proof.
- Both entries keep all evidence privacy path_only_no_values.
- Entries reject submitted deck contents, sideboard deltas, pre/postboard labels, queue type, workbook formulas, Apps Script, analytics, and AI truth as evidence.
- submitted_deck_cards and broader deck-state provenance remain deferred.
- No parser behavior, ClientAction parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or AI/analytics truth changed.

Validation:
Run:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_client_actions_parser.py tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py
- python3 -m pytest -q
- python3 -m ruff check src tests tools
- git diff --check
- python3 tools/check_protected_surfaces.py --base origin/main

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
- workflow_handoff block.

Do not:
- Change parser behavior.
- Change sideboarding detection behavior.
- Change submit-deck detection behavior.
- Change ClientAction parsing behavior.
- Change deck-state behavior.
- Change parser state final reconciliation or parser event classes.
- Change workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth.
- Stage, commit, push, merge, close issue #11, close issue #151, or target main.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/151"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md"
  verdict: "tier4_sideboarding_submit_deck_signal_metadata_ready_for_contract_review"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier4-sideboarding-submit-deck"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py - passed, 64 passed"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py - passed, 61 passed"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py - passed, 116 passed"
    - "python3 -m pytest -q - passed, 923 passed"
    - "python3 -m ruff check src tests tools - passed"
    - "git diff --check - passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main - passed, forbidden 0, warnings 12"
  changed_files:
    - "src/mythic_edge_parser/app/evidence_ledger.py"
    - "tests/test_evidence_ledger.py"
    - "docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #151."
    - "Do not change parser behavior, sideboarding detection behavior, submit-deck detection behavior, ClientAction parsing behavior, deck-state behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not map submitted deck contents, deck-state, card changes, analytics, diagnostics, replay, drift, schema snapshots, invariant execution, feature-equity reports, or runtime field-evidence attachment beyond what the #151 contract explicitly requires."
    - "Do not infer hidden cards, decklists, archetypes, sideboard plans, gameplay advice, player mistakes, matchup plans, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```
