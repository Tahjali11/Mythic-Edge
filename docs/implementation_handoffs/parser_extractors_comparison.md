# Parser Extractors Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/9

Issue #9 is open and describes this as a high-risk parser extractor contract audit, not a known bug report.

## Contract

`docs/contracts/parser_extractors.md`

## Role Performed

Module Implementer thread (C).

This pass compared the current `src/mythic_edge_parser/app/extractors.py` implementation, direct call sites, and focused tests against the parser extractors contract. It did not assume a known bug.

## What The Code Is Supposed To Do

`extractors.py` is supposed to provide safe, deterministic helper functions that read already-parsed MTGA event payload dictionaries and return primitive parser facts for state, transforms, runtime surfaces, gameplay-action tracking, and local diagnostic tools.

Plain English: this module reads facts from payloads. It should not parse raw log text, mutate parser runtime state, post webhooks, edit workbook tabs, or own final match/game truth.

## Current Behavior Summary

The implementation is broadly aligned with the contract:

- Safe primitive helpers normalize first-present values, integer-like values, dictionaries, and lists.
- Game-state helpers preserve the fallback order from normalized top-level fields to current raw `gameStateMessage` and then queued raw `queuedGameStateMessage.gameStateMessage`.
- Game-state identity hydration uses payload identity and game info first, then optional context fallback.
- Local team and starting-player helpers support current client-action and game-state payload shapes.
- Local private hand extraction filters for private hand zones and local seat ownership when seat data is available.
- Instance-to-GRP lookup extraction supports `grpId`, `grp_id`, `overlayGrpId`, and `overlay_grp_id`.
- Game-result helpers distinguish game-scope and match-scope results and expose latest matching scope results.
- Timestamp helpers return a `datetime` and ISO string for runner/state consumers.
- Extractor functions return values only; they do not perform project I/O or mutate runtime state.

## Call Sites Inspected

- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/arena_id_validation.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `src/mythic_edge_parser/app/runner.py`

The call sites match the contract's compatibility-surface story: underscore-prefixed helpers are private-style names, but they are currently shared parser interfaces and must not be renamed or shape-changed without a coordinated migration.

## Contract Matches

- Public compatibility surface: all helpers listed by the contract are present and importable.
- Purity boundary: extractor helpers do not write files, post webhooks, update workbook tabs, or mutate `state.RUNTIME_STATE`.
- Safe sections: non-dict and non-list optional game-state sections generally degrade through `_safe_dict()`, `_safe_list()`, `_game_state_dict_section()`, and `_game_state_list_section()`.
- Fallback order: normalized top-level game-state fields win before raw current message fields, which win before queued message fallback fields.
- Identity hydration: `_hydrate_game_state_identity()` returns the contracted keys and supports context fallback for partial GameState payloads.
- Turn tuple: `_extract_turn_info()` returns the contracted seven-item tuple used by state, transforms, runtime surfaces, validation, and GRP candidate tools.
- Local team and starting player: helpers support top-level, raw client-action, nested choose-starting-player, system-seat, and turn-one active-player paths.
- Hand extraction: local private hand instance IDs are normalized to integers and queued-zone fallback is tested.
- GRP lookup: instance and GRP identifiers are normalized to integers, including overlay GRP fallback.
- Game-result scopes: `_extract_game_result_scope_result()` skips malformed result entries, filters by normalized scope, and can require a known winner.
- Winner handling: `_is_known_winner()` rejects blank, boolean, and zero winners; state integration tests cover unknown winners not overwriting existing parser facts.
- Timestamp shape: `_event_datetime()` returns a `datetime` object for runner JSONL partitioning and `_safe_iso()` returns ISO text for state/model timing.

## Contract Mismatches

No clear implementation mismatch was found against the current contract.

Because no mismatch was found, no extractor code, parser state ownership, model row field names, workbook schema, webhook payload shape, Apps Script behavior, raw parser modules, secrets, environment variables, live workbook state, debug/archive/helper/runtime layers, or observability layers were changed.

## Missing Safeguards

These are not proven bugs from this comparison, but they remain useful guardrails for Module Reviewer / contract-test mode:

- `_safe_local_player()` assumes a list-like input and is not directly tested with malformed player-list values.
- `_maybe_int()` accepts booleans and truncates floats through Python `int()` behavior; the contract marks this as unresolved for identity, team, seat, instance, and GRP values.
- `_extract_game_result_identity()` assumes truthy `game_info` is a dictionary and assumes context contains `current_match_id` and `current_game_number`.
- `_has_match_scope_result()` assumes every `results` item supports `.get()`, unlike `_extract_game_result_scope_result()`, which skips non-dict entries.
- `_extract_starting_player_from_client_action()` returns raw values, while game-state starting-player extraction usually returns normalized integers.
- `_extract_starting_player_from_game_state()` can return team ID when player mapping exists and active seat ID when it does not.
- Local private hand extraction accepts malformed owner-seat values as local when a local system seat is known.
- Local private hand extraction returns the first matching zone and does not merge multiple valid local private hand zones.
- `_extract_instance_grp_lookup()` preserves GRP ID `0` if present; there is no direct test deciding whether zero is a valid GRP value.
- `_event_datetime()` falls back to nondeterministic local `datetime.now()` when timestamp metadata is missing or invalid.

## Missing Tests

Recommended for the next Module Reviewer / contract-test thread:

- Direct safe primitive tests for `_first_present()`, `_maybe_int()`, `_safe_dict()`, and `_safe_list()`.
- `_safe_local_player()` tests for empty lists, configured index, out-of-range configured index, and malformed input if that behavior should be guaranteed.
- `_extract_game_result_identity()` tests for malformed `game_info` and missing context keys, or explicit documentation that callers must sanitize those values.
- `_has_match_scope_result()` tests with non-dictionary `results` entries.
- `_event_datetime()` and `_safe_iso()` tests for valid timestamps and missing timestamp fallback.
- `_game_state_actions()` and `_game_state_annotations()` fallback tests because `gameplay_actions.py` imports them directly.
- Tests clarifying whether bool and fractional values are valid IDs for `_maybe_int()` callers.
- Tests clarifying local private hand owner-seat behavior for malformed owner IDs and multiple private hand zones.

## Stale Or Bridge-Code Areas

- Underscore-prefixed helper names act as public compatibility surfaces because app modules import them directly.
- Extractors still support preserved raw MTGA subpayloads under `raw_game_state` and `raw_client_action` while parser modules also provide normalized top-level views.
- Queue fallback is bridge-like compatibility for partial current `gameStateMessage` payloads.
- Timestamp fallback to local current time is convenient for runtime continuity but nondeterministic for strict replay semantics.

## Files Changed

- `docs/implementation_handoffs/parser_extractors_comparison.md`

## Code Changed

Docs-only. No Python code or tests changed.

## Interface Changes

None.

No function signatures, payload fields, workbook columns, environment variables, Apps Script entrypoints, model row field names, state ownership, parser event classes, raw parser behavior, extractor return shapes, match identity rules, game identity rules, or reconciliation behavior changed.

## Tests Added Or Updated

None.

This was a comparison pass. Missing tests are listed above for the next role.

## Validation Run

Focused extractor check:

```powershell
py -m pytest -q tests/test_app_extractors.py
```

Result:

```text
11 passed in 0.11s
```

Dependent parser/state/transform/runtime checks:

```powershell
py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py
```

Result:

```text
50 passed in 0.89s
```

## Forbidden Scope

Forbidden scope was not touched.

Specifically, this pass did not change workbook schema, webhook payload shape, deployed Apps Script behavior, row field names in `models.py`, state ownership in `state.py`, raw parser modules, secrets, environment variables, live workbook state, debug/archive/helper/runtime layers, or observability layers.

## Still Unverified

- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Full repo checks were not run because no code or test behavior changed.
- Diagnostic tool behavior outside the inspected call sites was not exhaustively tested.
- Rare malformed payload cases remain unverified unless already covered by parser payload tests.

## Reviewer Focus

Ask the Module Reviewer in contract-test mode to pay special attention to:

- malformed input tolerance for `_safe_local_player()`, `_extract_game_result_identity()`, and `_has_match_scope_result()`
- bool and float behavior in `_maybe_int()`
- raw value versus normalized integer return shape for client-action starting-player extraction
- mixed team-ID and seat-ID semantics in game-state starting-player extraction
- local private hand owner-seat behavior when owner seat is malformed
- `actions` and `annotations` fallback behavior used by `gameplay_actions.py`
- nondeterministic timestamp fallback in `_event_datetime()`

## Next Workflow Action

Next role: Module Reviewer (E) in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Reviewer thread in contract-test mode for https://github.com/Tahjali11/Mythic-Edge/issues/9.

Source artifacts:
- docs/agent_constitution.md
- docs/agent_threads/review.md
- docs/agent_threads/contract_test.md
- docs/contracts/parser_extractors.md
- docs/implementation_handoffs/parser_extractors_comparison.md

Task:
Review src/mythic_edge_parser/app/extractors.py, direct call sites, and focused tests against docs/contracts/parser_extractors.md and docs/implementation_handoffs/parser_extractors_comparison.md. Produce docs/contract_test_reports/parser_extractors.md.

Do not assume there is a known bug. Verify contract matches, mismatches, missing tests, and remaining risks. Do not change workbook schema, webhook payload shape, deployed Apps Script behavior, row field names in models.py, state ownership in state.py, raw parser modules, secrets, environment variables, live workbook state, debug/archive/helper/runtime layers, or observability layers.

Run:
py -m pytest -q tests/test_app_extractors.py
py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py

Final handoff must include findings, contract matches, contract mismatches, missing tests, validation result, still-unverified layers, whether forbidden scope was touched, and whether the next role is Module Fixer or Module Submitter.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/9"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/parser_extractors_comparison.md"
  target_artifact: "docs/contract_test_reports/parser_extractors.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "py -m pytest -q tests/test_app_extractors.py (11 passed)"
    - "py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py (50 passed)"
  stop_conditions:
    - "Do not implement code changes during review unless explicitly redirected to Module Fixer."
    - "Stop if a proposed fix would change workbook schema, webhook payload shape, Apps Script deployment behavior, state ownership, raw parser modules, or move parser-owned truth downstream."
```
