# GRE ConnectResp Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/22

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_gre_connect_resp.md`

## Role Performed

Codex C: Module Implementer.

## Summary

Compared `src/mythic_edge_parser/parsers/gre/connect_resp.py`,
`src/mythic_edge_parser/parsers/gre/__init__.py`, and focused tests against the
GRE connect-response parser contract.

No parser behavior mismatch was found. The implementation matches the contract
for helper output fields, scalar pass-through/default behavior, list
normalization, settings shallow copy, raw message identity preservation,
direct-helper malformed-section tolerance, GRE dispatch gating, game-state
precedence, and side-effect boundaries.

The comparison did find missing focused tests required by the contract. I added
focused tests only. No runtime/parser implementation code changed.

## Confirmed Matches

- `build_connect_resp_payload(message)` returns `type == "connect_resp"` and
  keeps the public helper API parser-local.
- `message_type`, `msg_id`, and `game_state_id` are pass-through/default
  fields and are not coerced.
- `system_seat_ids`, `deck_cards`, and `sideboard_cards` use
  `api_common.normalize_int_list()`, which accepts ints and digit strings,
  skips bools/malformed values, preserves accepted order, and preserves
  duplicates.
- Missing or malformed direct-helper optional sections degrade to neutral
  defaults rather than raising.
- `settings` is a top-level shallow copy when `connectResp.settings` is a dict.
- Nested `settings` values intentionally remain shallow aliases under the
  current contract.
- `raw_connect_resp` preserves the original GRE message object by identity.
- GRE dispatch in `parsers/gre/__init__.py` includes the
  `GREMessageType_ConnectResp` marker and extracts direct or batched GRE
  message dicts.
- GRE dispatch ignores non-dict batch members and invalid
  `greToClientMessages` shapes.
- GRE dispatch emits a connect-response `GameStateEvent` only when
  `message.get("connectResp")` is a dict.
- GRE game-state handling takes precedence over connect-response handling for
  the same message.
- Emitted connect-response events remain `GameStateEvent` with metadata based
  on the full raw body.
- Downstream runtime behavior still treats connect-response deck evidence as
  separate parser evidence, not as `ClientAction submit_deck_resp` active
  submitted-deck truth.
- No workbook rows, runtime status files, failed posts, generated data,
  webhooks, Apps Script, or parser state are written by the helper.

## Contract Mismatches

None found.

No parser behavior changes were required.

## Missing Safeguards

None found in `connect_resp.py` or GRE dispatch.

The contracted safeguards are present:

- malformed optional nested sections use neutral defaults in the direct helper
- GRE dispatch requires dictionary `connectResp` before event emission
- game-state emission takes precedence over connect-response emission
- connect-response deck evidence is not promoted to active submitted-deck
  runtime behavior
- malformed list members are filtered before downstream consumers receive
  normalized lists

## Missing Or Weak Tests

The contract's suspected test gaps were confirmed in the pre-change tests. They
were addressed by focused additions to:

- `tests/test_gre_connect_resp_parser.py`
- `tests/test_parsers.py`
- `tests/test_runtime_surfaces.py`

Tests added or strengthened:

- helper happy path field shape, including payload type, scalar pass-through,
  normalized lists, shallow settings copy, and raw message identity
- nested settings aliasing to document current shallow-copy behavior
- defaults for missing `type`, `msgId`, `gameStateId`, `systemSeatIds`,
  deck-list fields, and sideboard-list fields
- malformed integer-list members for `system_seat_ids`, `deck_cards`, and
  `sideboard_cards`
- non-list source values normalizing to empty lists
- direct top-level GRE connect-response dispatch
- emitted event metadata raw bytes, timestamp, kind, and performance class
- missing and non-dict `connectResp` producing no dispatch event
- game-state payload precedence when the same message also has `connectResp`
- runtime surface guard that connect-response deck evidence does not write
  active submitted deck or deck profile artifacts

Remaining non-blocking test notes:

- No new `state.py`, `extractors.py`, or `gameplay_actions.py` tests were
  added because existing focused suites were already passing and no downstream
  behavior changed.
- Future use of connect-response deck evidence as fallback submitted-deck
  evidence remains out of scope and should receive a new contract.
- Future deep-copy isolation for nested settings remains out of scope and would
  be a behavior change.

## Files Changed

- `tests/test_gre_connect_resp_parser.py`
- `tests/test_parsers.py`
- `tests/test_runtime_surfaces.py`
- `docs/implementation_handoffs/parser_gre_connect_resp_comparison.md`

## Code Changed

No runtime code changed.

No parser behavior, parser state, workbook schema, webhook payload shape, Apps
Script behavior, parser event classes, extractor behavior, match/game identity,
deduplication, final reconciliation, secrets, environment variables, raw logs,
generated data, runtime status files, failed posts, or workbook exports
changed.

## Validation Evidence

Baseline checks before adding tests:

```bash
python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py
# Pass: 14 passed in 0.04s.

python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
# Pass: 64 passed in 0.15s.

python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
# Pass: 20 passed in 0.15s.
```

Checks after adding focused tests:

```bash
python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py
# Pass: 22 passed in 0.05s.

python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
# Pass: 64 passed in 0.15s.

python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
# Pass: 21 passed in 0.16s.

python3 -m ruff check src tests
# Pass: All checks passed!
```

Final documentation/worktree validation:

```bash
git diff --check
# Pass: no output.

git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
# Pass: no output.

python3 -m pytest -q
# Pass: 452 passed in 0.96s.
```

## Still-Unverified Layers

- Live workbook behavior was not checked; no workbook schema or workbook export
  behavior was in scope.
- Deployed Apps Script behavior was not checked; no Apps Script behavior was in
  scope.
- GitHub Actions were not checked because no PR exists for this module yet.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

No Codex D fixer pass is recommended because no behavior mismatch or failing
validation remains after the focused test additions.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #22:
https://github.com/Tahjali11/Mythic-Edge/issues/22

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_gre_connect_resp.md
- docs/implementation_handoffs/parser_gre_connect_resp_comparison.md
- src/mythic_edge_parser/parsers/gre/connect_resp.py
- src/mythic_edge_parser/parsers/gre/__init__.py
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/app/analytics_sidecar.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- tests/test_gre_connect_resp_parser.py
- tests/test_parsers.py
- tests/test_gre_game_state_parser.py
- tests/test_state.py
- tests/test_app_extractors.py
- tests/test_gameplay_actions.py
- tests/test_runtime_surfaces.py
- tests/test_grp_id_candidates.py
- tests/test_parser_regressions.py

Goal:
Verify the Module Implementer comparison and focused test additions against the GRE connect-response parser contract.

Confirm:
- build_connect_resp_payload() returns the contracted payload fields, defaults, raw preservation, settings shallow copy, and normalized list behavior.
- GRE dispatch emits connect-response GameStateEvent payloads only for dictionary connectResp messages.
- GRE dispatch returns no connect-response event for missing or non-dict connectResp.
- GRE game-state handling takes precedence over connect-response handling on the same message.
- emitted connect-response events preserve GameStateEvent kind, interactive performance class, timestamp, and raw body bytes.
- focused tests cover the contract-required normalization, malformed-input, direct-helper, dispatch, and runtime guard behavior.
- connect-response deck evidence is not treated as ClientAction submit_deck_resp active submitted-deck truth.
- downstream consumers still consume parser-produced fields and do not own raw GRE connect-response parsing.
- no parser state, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not stage, commit, merge, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/22"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_gre_connect_resp.md"
  target_artifact: "docs/implementation_handoffs/parser_gre_connect_resp_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py"
    - "python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py"
    - "python3 -m ruff check src tests"
    - "python3 -m pytest -q"
    - "git diff --check"
  stop_conditions:
    - "Route to Module Contract Writer if the contract is ambiguous or inaccurate."
    - "Route to Module Fixer if reviewer finds a concrete parser behavior or focused-test mismatch."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not treat GRE connect-response deck evidence as active submitted-deck truth unless a future contract explicitly requires it."
    - "Do not target main unless explicitly approved."
```
