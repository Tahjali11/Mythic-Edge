# Parser Client Actions Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/20

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_client_actions.md`

## Role Performed

Codex C: Module Implementer.

## Summary

Compared `src/mythic_edge_parser/parsers/client_actions.py` and focused parser
tests against the parser client-actions contract.

No parser behavior mismatch was found. The implementation matches the contract
for marker classification, JSON envelope parsing, UI payload preservation,
generic fallback, specialized mulligan/select-N/submit-deck payloads, raw
envelope preservation, request-context defaults, malformed-input behavior, and
side-effect boundaries.

The comparison did find missing focused tests required by the contract. I added
focused tests in `tests/test_client_actions_parser.py` only. No runtime/parser
code was changed.

## Confirmed Matches

- `CLIENT_TO_GRE_MARKER` and `CLIENT_TO_GRE_UI_MARKER` retain the contracted
  marker strings.
- `try_parse()` returns `None` for non-client-action entries and for candidate
  bodies without a parsed dict JSON envelope.
- UI marker classification is checked before GRE marker classification, so UI
  messages remain distinguishable as `type == "client_ui_message"`.
- Marker matching remains case-sensitive and substring-based over the full raw
  body, so exact marker strings inside the JSON enum can classify messages even
  when the log prefix casing differs.
- GRE inner payload extraction accepts dict payloads and stringified JSON dict
  payloads, and rejects missing, non-dict, invalid-string, and stringified
  non-dict payloads.
- Generic fallback emits `type == "generic_client_action"`, preserves
  `message_type`, allows missing/blank type values as `""`, and preserves the
  parsed envelope under `raw_client_action`.
- Stringified inner payloads remain preserved as the original string under
  `raw_client_action["payload"]`.
- Mulligan response emits `type == "mulligan_resp"`, maps known decisions to
  `mulligan` and `keep`, passes through unknown truthy decisions, and defaults
  missing/malformed/falsey decisions to `""`.
- Select-N response emits `type == "select_n_resp"` and normalizes selected
  option/object IDs through `api_common.normalize_int_list()`, dropping
  booleans, floats, malformed strings, negative strings, dicts, nested lists,
  and `None`.
- Submit-deck response emits `type == "submit_deck_resp"` with `deck_cards`
  and `sideboard_cards`; direct truthy sources take precedence, nested deck
  sources remain supported, list-valued `deck` / `sideboard` fallbacks remain
  supported, and malformed selected sources normalize to empty lists.
- Specialized payloads include `game_state_id`, `resp_id`, `request_id`, and
  `raw_client_action`; missing request context defaults to `0`, while present
  values are copied as-is.
- `ClientActionEvent` metadata preserves the passed timestamp and raw encoded
  body, and the event performance class remains interactive dispatch.
- `router.py` still dispatches `client_actions` after `gre` for Unity and
  unknown-header entries.
- Downstream state, transform, extractor, runtime, analytics, runner, and GRP
  candidate consumers read parser-produced `ClientActionEvent.payload` fields;
  they do not own raw client-to-GRE parsing.
- `client_actions.py` remains side-effect free and does not write files, mutate
  runtime state, post webhooks, update workbook tabs, refresh status files, or
  change failed-post/generated-data surfaces.

## Contract Mismatches

None found.

No parser behavior changes were required.

## Missing Safeguards

None found in `client_actions.py`.

The contracted safeguards are present as parser-local return/default behavior:

- non-client-action bodies return `None`
- malformed or non-dict JSON envelopes return `None`
- malformed GRE inner payloads return `None`
- malformed specialized nested payloads emit neutral default fields
- malformed selected IDs and deck-list entries are dropped by normalization
- unknown well-formed GRE client actions are preserved through generic fallback
- raw envelopes are preserved for UI, generic, and specialized outputs

## Missing Or Weak Tests

The contract's suspected test gaps were confirmed in the pre-change focused
tests. They were addressed by expanding `tests/test_client_actions_parser.py`.

Tests added or strengthened:

- event metadata timestamp, raw bytes, kind, and performance class
- marker detection from JSON enum when log-prefix casing differs
- UI channel priority when both markers are present in the body
- generic fallback for missing, blank, whitespace, and `None` message types
- generic fallback preserving stringified raw payloads
- mulligan decision normalization for `MulliganOption_Mulligan`, keep,
  unknown truthy values, blank values, and `None`
- malformed/missing `mulliganResp` fallback to `decision == ""`
- malformed selected-ID filtering for booleans, malformed strings, negative
  strings, floats, dicts, nested lists, and `None`
- malformed/missing `selectNResp` fallback to empty lists
- direct submit-deck source precedence for truthy direct sources
- list-valued `deck` and `sideboard` fallbacks
- truthy malformed direct submit-deck sources normalizing to empty lists
- malformed/missing `submitDeckResp` fallback to empty lists
- missing, non-dict, invalid-stringified, and stringified non-dict GRE inner
  payloads returning `None`
- marker-present invalid JSON and parsed non-dict JSON returning `None`
- request-context defaults and as-is request-context copying for specialized
  payloads

Remaining non-blocking test notes:

- No new downstream consumer tests were added because no downstream behavior
  changed; existing router/state/transform/extractor/runtime/GRP/regression
  tests were run.
- UI subtype filtering remains out of scope and intentionally untested as a
  behavior change.
- Deep-copy isolation for `raw_client_action` remains intentionally outside
  the contract; event payload copying is shallow.

## Files Changed

- `tests/test_client_actions_parser.py`
- `docs/implementation_handoffs/parser_client_actions_comparison.md`

## Code Changed

No runtime code changed.

No parser behavior, parser state, workbook schema, webhook payload shape, Apps
Script behavior, parser event classes, match/game identity, deduplication,
final reconciliation, secrets, environment variables, raw logs, generated
data, runtime status files, failed posts, or workbook exports changed.

## Validation Evidence

Baseline checks before adding tests:

```bash
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py
# Pass: 31 passed in 0.07s.

python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py
# Pass: 60 passed in 0.23s.
```

Checks after adding focused tests:

```bash
python3 -m pytest -q tests/test_client_actions_parser.py
# Pass: 55 passed in 0.06s.

python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py
# Pass: 78 passed in 0.06s.

python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py
# Pass: 60 passed in 0.18s.

python3 -m pytest -q tests/test_grp_id_candidates.py tests/test_parser_regressions.py
# Pass: 14 passed in 0.18s.

python3 -m ruff check src tests
# Pass: All checks passed!

python3 -m pytest -q
# Pass: 443 passed in 1.08s.
```

Final documentation/worktree validation:

```bash
git diff --check
# Pass: no output.

git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
# Pass: no output.
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
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #20:
https://github.com/Tahjali11/Mythic-Edge/issues/20

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_client_actions.md
- docs/implementation_handoffs/parser_client_actions_comparison.md
- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/analytics_sidecar.py
- src/mythic_edge_parser/app/runner.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- tests/test_client_actions_parser.py
- tests/test_parsers.py
- tests/test_router_unit.py
- tests/test_state.py
- tests/test_transforms.py
- tests/test_app_extractors.py
- tests/test_runtime_surfaces.py
- tests/test_grp_id_candidates.py
- tests/test_parser_regressions.py

Goal:
Verify the Module Implementer comparison and focused test additions against the parser client-actions contract.

Confirm:
- try_parse() still returns ClientActionEvent or None according to contract.
- UI, generic, mulligan, select-N, and submit-deck payload shapes match the contract.
- marker classification, UI priority, JSON envelope parsing, inner payload extraction, raw envelope preservation, request context defaults, and malformed input behavior match the contract.
- missing focused parser tests identified by the contract were added without changing parser behavior.
- downstream consumers still consume parser-produced client-action payloads and do not own raw client-to-GRE parsing.
- no parser state, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py
python3 -m pytest -q tests/test_grp_id_candidates.py tests/test_parser_regressions.py
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/20"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_client_actions.md"
  target_artifact: "docs/implementation_handoffs/parser_client_actions_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_client_actions_parser.py"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py"
    - "python3 -m pytest -q tests/test_grp_id_candidates.py tests/test_parser_regressions.py"
    - "python3 -m ruff check src tests"
    - "python3 -m pytest -q"
    - "git diff --check"
  stop_conditions:
    - "Route to Module Contract Writer if the contract is ambiguous or inaccurate."
    - "Route to Module Fixer if reviewer finds a concrete parser behavior or focused-test mismatch."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main unless explicitly approved."
```
