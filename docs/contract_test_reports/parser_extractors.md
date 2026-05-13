# Parser Extractors Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/9

Issue #9 is open and describes this as a high-risk parser extractor contract audit, not a known bug report.

## Contract

`docs/contracts/parser_extractors.md`

Supporting workflow docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Implementation files reviewed:

- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/arena_id_validation.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `src/mythic_edge_parser/app/runner.py`
- `tests/test_app_extractors.py`
- `tests/test_state.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_transforms.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_gre_game_result_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_parser_regressions.py`
- `docs/implementation_handoffs/parser_extractors_comparison.md`

No working-tree code diff was present for `extractors.py` or the focused test files during this review. The implementation handoff under review is docs-only.

## Contract Summary

`extractors.py` must remain a parser-owned helper module. It reads already-parsed event payload dictionaries and preserved raw subpayloads, then returns primitive facts for state, transforms, runtime surfaces, gameplay-action tracking, and diagnostics.

It must not parse raw log text, post webhooks, mutate workbook state, mutate parser runtime state, change model row field names, or own final match/game truth.

## Checks Run

```powershell
py -m pytest -q tests/test_app_extractors.py
py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py
```

Results:

```text
11 passed in 0.11s
50 passed in 0.92s
```

Additional read-only probes were run to verify the review focus areas:

```text
_safe_local_player("ab") -> "a"
_safe_local_player({"team_id": 1}) -> KeyError: 0
_maybe_int(True) -> 1
_maybe_int(1.5) -> 1
_extract_game_result_identity({"game_info": "bad"}, context) -> AttributeError
_extract_game_result_identity({}, {}) -> KeyError
_has_match_scope_result({"results": ["bad", {"scope": "MatchScope_Match"}]}) -> AttributeError
_extract_starting_player_from_client_action({"systemSeatId": "2"}) -> "2"
_extract_starting_player_from_game_state(mapped active seat 2 to team 9) -> 9
_extract_starting_player_from_game_state(unmapped active seat 2) -> 2
_extract_local_private_hand_instance_ids(malformed owner seat with local seat 2) -> [1, 2]
_game_state_actions() queued fallback filters non-dict entries
_game_state_annotations() queued fallback filters non-dict entries
_event_datetime(object()) -> datetime
```

## Results

The implementation broadly matches the current contract and no forbidden scope was touched.

However, the contract and implementation handoff both identify malformed-input and mixed-return-shape risks that are not yet locked by tests. Some of those risks are concrete crash paths when helpers are called with malformed parsed payload sections. Because this is a high-risk parser boundary, this report recommends Module Fixer before Module Submitter.

Post-fix note: this report is preserved as the historical contract-test artifact. The Module Fixer follow-up addressed the P2 malformed-input findings and added focused tests for the documented current behaviors; see `docs/implementation_handoffs/parser_extractors_fixer.md`.

## Review Findings Ordered By Severity

- P2: `_safe_local_player()` can return a non-dictionary or raise for malformed player-list inputs, while direct call sites immediately use `.get()`. With a string input, `_safe_local_player("ab")` returns `"a"`; with a dict input, it raises `KeyError: 0`. `state.py` and `transforms.py` pass `payload.get("players") or []` into this helper and then call `.get()` on the result. The contract marks malformed input tolerance as a reviewer focus, so this needs a focused test and likely a small guard if malformed player lists are considered valid parsed-input tolerance.
- P2: `_extract_game_result_identity()` and `_has_match_scope_result()` can crash on malformed optional sections. `_extract_game_result_identity({"game_info": "bad"}, context)` raises `AttributeError`, `_extract_game_result_identity({}, {})` raises `KeyError`, and `_has_match_scope_result({"results": ["bad"]})` raises `AttributeError`. This conflicts with the broader extractor guarantee that malformed optional sections should degrade to neutral values, although the contract also documents these as observed limitations. This should route to Module Fixer for tests and either implementation guards or contract clarification.
- P3: `_maybe_int()` accepts booleans and truncates fractional values. `_maybe_int(True)` returns `1`, and `_maybe_int(1.5)` returns `1`. The contract explicitly lists this as unknown rather than a mismatch, but these values flow into identity, team, seat, instance, and GRP paths, so the behavior needs direct tests before submit.
- P3: Starting-player return shape remains mixed. `_extract_starting_player_from_client_action({"systemSeatId": "2"})` returns raw string `"2"`, while `_extract_starting_player_from_game_state()` returns a team ID when player mapping exists and an active seat ID when it does not. Current call sites tolerate this, but direct tests should lock the intended bridge behavior.
- P3: Local private hand extraction accepts a malformed owner seat as local when a local seat is known. This is documented current behavior, not a mismatch, but it is sensitive because a bad owner value can allow a private hand zone through the local-hand path.
- P3: `_event_datetime()` falls back to nondeterministic local `datetime.now()` when metadata timestamp is missing or invalid. This is documented current behavior, but it remains untested and can affect local JSONL partitioning in runner paths.

## Confirmed Contract Matches

- All compatibility-surface helpers listed in the contract are present and importable.
- Extractor helpers are return-value helpers only; they do not write files, post webhooks, mutate workbook tabs, mutate `state.RUNTIME_STATE`, or own final match/game truth.
- Top-level normalized game-state fields take precedence over current raw `gameStateMessage` fields, and current raw fields take precedence over queued raw fallback.
- `_game_state_actions()` and `_game_state_annotations()` use the same top-level/current-raw/queued-raw fallback as other game-state list sections and filter non-dictionary list items.
- `_hydrate_game_state_identity()` returns the contracted identity keys and supports context fallback for partial GameState payloads.
- `_extract_turn_info()` returns the contracted seven-item tuple consumed by state, transforms, runtime surfaces, validation, and diagnostic tools.
- Client-action helpers support top-level, raw payload, and nested response shapes for current local team and starting-player extraction.
- Game-state local team extraction maps local system seat to player team when player mapping exists.
- Game-state starting-player extraction is limited to turn one and returns team ID when mapping exists, otherwise active seat ID.
- Local private hand extraction normalizes returned object instance IDs to integers.
- Instance-to-GRP lookup normalizes instance and GRP IDs to integers and preserves overlay GRP fallback behavior.
- `_extract_game_result_scope_result()` skips non-dictionary result entries, filters by scope, and can require a known winner.
- `_is_known_winner()` rejects blank, boolean, and zero winners.
- `_event_datetime()` returns a `datetime`, and `_safe_iso()` returns ISO text.
- No workbook schema, webhook payload shape, deployed Apps Script behavior, model row field names, state ownership, raw parser modules, secrets, environment variables, live workbook state, debug/archive/helper/runtime layer, or observability layer was changed.

## Contract Mismatches

No strict mismatch was found against the contract's explicitly documented observed behavior.

There is contract tension around malformed-input tolerance: the required guarantees say malformed optional sections should degrade to neutral values, while the error-behavior and suspected-gap sections explicitly document that `_safe_local_player()`, `_extract_game_result_identity()`, and `_has_match_scope_result()` do not fully guard malformed inputs today. This should be resolved by Module Fixer tests and, if needed, Module Contract Writer clarification.

## Missing Safeguards

- `_safe_local_player()` lacks an input-type guard that guarantees it returns a dictionary for malformed player-list inputs.
- `_extract_game_result_identity()` lacks safe dictionary coercion for truthy non-dict `game_info`.
- `_extract_game_result_identity()` assumes context contains `current_match_id` and `current_game_number`.
- `_has_match_scope_result()` lacks non-dictionary result-item filtering.
- `_maybe_int()` has permissive bool and fractional behavior that is not explicitly accepted or rejected by tests.
- `_extract_starting_player_from_client_action()` has raw return shape while other identity helpers generally normalize integers.
- `_extract_starting_player_from_game_state()` mixes team-ID and seat-ID return semantics.
- `_extract_local_private_hand_instance_ids()` accepts malformed owner-seat values as local when a local seat exists.
- `_event_datetime()` has nondeterministic fallback behavior without direct tests.

## Missing Tests

Recommended next tests for Module Fixer:

- `_safe_local_player()` empty list, configured index, out-of-range configured index, string input, dict input, and non-dict list entries.
- `_first_present()`, `_safe_dict()`, and `_safe_list()` edge cases for `0`, `False`, `{}`, `[]`, non-dict, and non-list values.
- `_maybe_int()` explicit behavior for `True`, `False`, `1.5`, `"1.5"`, `"2"`, and invalid strings.
- `_extract_game_result_identity()` malformed `game_info` and missing context keys.
- `_has_match_scope_result()` with non-dictionary `results` entries.
- `_extract_starting_player_from_client_action()` raw string versus integer return shape.
- `_extract_starting_player_from_game_state()` mapped team-ID return and unmapped seat-ID fallback.
- `_extract_local_private_hand_instance_ids()` malformed owner-seat behavior and multiple private hand zones.
- `_extract_instance_grp_lookup()` behavior for GRP ID `0`, if the project needs to decide whether zero is valid.
- `_event_datetime()` and `_safe_iso()` valid timestamp and missing timestamp fallback.
- `_game_state_actions()` and `_game_state_annotations()` top-level, current-raw, queued-raw, and non-dict filtering behavior.

## Stale Or Bridge-Code Areas

- Underscore-prefixed extractor helpers are private-style names but currently act as shared parser compatibility surfaces.
- Extractors still support preserved raw MTGA subpayloads under `raw_game_state` and `raw_client_action` while parser modules also provide normalized top-level views.
- Queue fallback is bridge-like compatibility for partial current `gameStateMessage` payloads.
- Starting-player helpers bridge mixed seat/team and raw/normalized return shapes.
- Timestamp fallback to current local time is useful for runtime continuity but nondeterministic for replay strictness.

## Drift Notes

- Repo state: no code/test implementation diff was present for the reviewed extractor files; this report adds a docs-only contract-test artifact.
- Workbook state: not inspected.
- Deployed Apps Script state: not inspected.
- Live workbook state: not inspected.
- Local data: no raw logs, generated card data, runtime status files, failed posts, debug/archive/helper layers, or observability layers were changed.

## Forbidden Scope

Forbidden scope was not touched.

This report did not change workbook schema, webhook payload shape, deployed Apps Script behavior, row field names in `models.py`, state ownership in `state.py`, raw parser modules, secrets, environment variables, live workbook state, debug/archive/helper/runtime layers, or observability layers.

## Recommendation

Request implementation fix, focused first on tests.

Next role: Module Fixer (D).

Rationale: no production code mismatch is proven under the current documented behavior, but the malformed-input crash probes and untested mixed semantics are high-risk parser-boundary issues. Module Fixer should add focused tests, then apply small guards only where the tests confirm behavior should degrade neutrally instead of raising.

## Next Workflow Action

Next role: Module Fixer (D)

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Fixer thread for https://github.com/Tahjali11/Mythic-Edge/issues/9.

Source artifacts:
- docs/agent_constitution.md
- docs/agent_threads/module_fixer.md
- docs/contracts/parser_extractors.md
- docs/implementation_handoffs/parser_extractors_comparison.md
- docs/contract_test_reports/parser_extractors.md

Task:
Address the contract-test report findings for parser extractors. Prefer focused tests first. Do not change production code unless a focused test confirms the current behavior violates the intended parser-extractor contract.

Targets:
- Add tests for _safe_local_player() malformed player-list input and configured-index behavior.
- Add tests for _first_present(), _maybe_int(), _safe_dict(), and _safe_list() edge cases.
- Add tests for _extract_game_result_identity() malformed game_info and missing context keys. If the intended contract is neutral fallback, add the smallest implementation guard.
- Add tests for _has_match_scope_result() with non-dictionary results entries. If the intended contract is neutral fallback, add the smallest implementation guard.
- Add tests clarifying bool and float behavior in _maybe_int().
- Add tests clarifying raw value versus normalized integer return shape for _extract_starting_player_from_client_action().
- Add tests clarifying team-ID versus seat-ID semantics in _extract_starting_player_from_game_state().
- Add tests clarifying local private hand owner-seat behavior when owner seat is malformed and when multiple private hand zones exist.
- Add tests for _game_state_actions() and _game_state_annotations() fallback behavior used by gameplay_actions.py.
- Add tests for _event_datetime() and _safe_iso() valid timestamp and missing timestamp fallback.

Do not change workbook schema, webhook payload shape, deployed Apps Script behavior, row field names in models.py, state ownership in state.py, raw parser modules, secrets, environment variables, live workbook state, debug/archive/helper/runtime layers, or observability layers.

Run:
py -m pytest -q tests/test_app_extractors.py
py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py

Final handoff must include:
- role performed
- issue and report used
- files changed
- code changed or tests-only
- findings fixed
- validation result
- still-unverified layers
- whether forbidden scope was touched
- next recommended thread role
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/9"
  completed_thread: "E"
  next_thread: "D"
  source_artifact: "docs/contract_test_reports/parser_extractors.md"
  target_artifact: "tests/test_app_extractors.py"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "py -m pytest -q tests/test_app_extractors.py (11 passed)"
    - "py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py (50 passed)"
  stop_conditions:
    - "Do not change production code unless focused tests confirm current behavior violates the intended contract."
    - "Do not change workbook schema, webhook payload shape, Apps Script deployment behavior, model row field names, state ownership, raw parser modules, or parser truth ownership."
    - "Route back to Module Contract Writer if tests reveal ambiguity rather than a clear expected behavior."
```
