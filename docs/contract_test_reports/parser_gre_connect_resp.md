# GRE Connect Response Parser Contract-Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/22

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_gre_connect_resp.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Implementation handoff:
`docs/implementation_handoffs/parser_gre_connect_resp_comparison.md`

Changed implementation surface reviewed:

- `tests/test_gre_connect_resp_parser.py`
- `tests/test_parsers.py`
- `tests/test_runtime_surfaces.py`
- `docs/contracts/parser_gre_connect_resp.md`
- `docs/implementation_handoffs/parser_gre_connect_resp_comparison.md`

## Contract Summary

`src/mythic_edge_parser/parsers/gre/connect_resp.py` must normalize GRE
connect-response message dictionaries into stable parser-owned `connect_resp`
payloads. GRE dispatch must emit those payloads as `GameStateEvent` objects
only for dictionary `connectResp` messages, while preserving game-state
precedence, raw-body metadata, normalized list fields, settings shallow-copy
behavior, and raw message preservation. Downstream consumers may consume
parser-produced fields but must not own raw GRE connect-response parsing or
promote connect-response deck evidence to active submitted-deck truth.

## Checks Run

```bash
python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check
python3 -m pytest -q
```

## Results

- `python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py`
  -> `22 passed in 0.04s`.
- `python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py`
  -> `64 passed in 0.15s`.
- `python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py`
  -> `21 passed in 0.16s`.
- `python3 -m ruff check src tests` -> `All checks passed!`.
- `git diff --check` -> passed with no output.
- `python3 -m pytest -q` -> `452 passed in 0.90s`.

## Confirmed Contract Matches

- `build_connect_resp_payload()` returns the contracted payload fields:
  `type`, `message_type`, `msg_id`, `game_state_id`, `system_seat_ids`,
  `deck_cards`, `sideboard_cards`, `settings`, and `raw_connect_resp`.
- `message_type`, `msg_id`, and `game_state_id` remain pass-through/default
  scalar fields and are not coerced.
- `system_seat_ids`, `deck_cards`, and `sideboard_cards` use the contracted
  integer-list normalization: valid ints and digit strings are kept, malformed
  members are skipped, accepted order is preserved, and duplicates are
  preserved.
- `settings` is a shallow top-level copy, and nested settings aliasing remains
  documented and covered as current behavior.
- `raw_connect_resp` preserves the original message object.
- Direct helper calls tolerate missing or malformed optional nested sections
  with neutral defaults.
- GRE dispatch emits connect-response `GameStateEvent` payloads only for
  dictionary `connectResp` messages.
- GRE dispatch returns no connect-response event for missing or non-dict
  `connectResp`.
- GRE game-state handling takes precedence over connect-response handling for
  the same message.
- Emitted connect-response events preserve `GameStateEvent` kind, interactive
  performance class, timestamp, and raw body bytes.
- Focused tests cover the contract-required normalization, malformed-input,
  direct-helper, dispatch, event-metadata, game-state-precedence, and runtime
  guard behavior.
- Connect-response deck evidence is not treated as `ClientAction`
  `submit_deck_resp` active submitted-deck truth.
- Downstream state, extractors, gameplay actions, diagnostics, runtime
  surfaces, analytics, transforms, and GRP candidate tooling continue to
  consume parser-produced fields and do not own raw GRE connect-response
  parsing.
- No parser state, workbook schema, webhook payload shape, Apps Script
  behavior, parser event classes, extractor behavior, match/game identity,
  deduplication, final reconciliation, secrets, environment variables, raw
  logs, generated data, runtime status files, failed posts, or workbook exports
  changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

The focused additions cover the contract's prior suspected gaps for nested
settings aliasing, integer-list edge cases, non-list source defaults,
missing/non-dict `connectResp` dispatch no-events, direct-helper versus dispatch
distinction, game-state precedence, emitted event metadata, and the runtime
guard that connect-response deck evidence does not update active submitted-deck
artifacts.

## Drift Notes

- No parser behavior drift found.
- No downstream ownership drift found; raw GRE connect-response parsing remains
  in the parser layer.
- No active submitted-deck drift found; connect-response deck fields remain
  separate parser evidence.
- No workbook/webhook/App Script/runtime artifact drift found in the reviewed
  surface.

## Recommendation

Approve for submitter work.

Next recommended role: Codex F: Module Submitter.

## Remaining Non-Blocking Gaps

- GitHub Actions were not checked because no PR exists yet.
- Live workbook and deployed Apps Script behavior were not checked; no workbook
  schema or Apps Script changes are in scope.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #22 and the GRE connect-response parser contract audit.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/22

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_gre_connect_resp.md
- docs/implementation_handoffs/parser_gre_connect_resp_comparison.md
- docs/contract_test_reports/parser_gre_connect_resp.md
- tests/test_gre_connect_resp_parser.py
- tests/test_parsers.py
- tests/test_runtime_surfaces.py

Reviewer verdict:
No blocking findings. The GRE connect-response parser contract audit is ready for submitter work.

Submitter requirements:
- Verify current branch and changed-file scope.
- Stage only the reviewed GRE connect-response parser audit artifacts.
- Commit and push the branch.
- Open or update a draft PR targeting codex/parser-module-audit-suite, not main.
- Do not merge, close issue #22, or mark tracker #5 complete; those are Codex G responsibilities.

Validation to run or verify:
python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check
python3 -m pytest -q

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not merge or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/22"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_gre_connect_resp.md"
  target_artifact: "docs/contract_test_reports/parser_gre_connect_resp.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py -> 22 passed in 0.04s"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py -> 64 passed in 0.15s"
    - "python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py -> 21 passed in 0.16s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed with no output"
    - "python3 -m pytest -q -> 452 passed in 0.90s"
  stop_conditions:
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not treat GRE connect-response deck evidence as active submitted-deck truth unless a future contract explicitly requires it."
    - "Do not merge, close issue #22, or mark tracker #5 complete; route deployer work to Codex G."
    - "Do not target main unless explicitly approved."
```
