# Parser Client Actions Contract-Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/20

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_client_actions.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Implementation handoff:
`docs/implementation_handoffs/parser_client_actions_comparison.md`

Changed implementation surface reviewed:

- `tests/test_client_actions_parser.py`
- `docs/contracts/parser_client_actions.md`
- `docs/implementation_handoffs/parser_client_actions_comparison.md`

## Contract Summary

`src/mythic_edge_parser/parsers/client_actions.py` must recognize raw MTGA
`ClientToGREMessage` and `ClientToGREUIMessage` bodies, parse JSON envelopes,
extract dict or stringified dict inner payloads, preserve raw envelopes, emit
`ClientActionEvent` payloads for UI, generic, mulligan, select-N, and
submit-deck actions, return `None` for malformed or unsupported candidates,
and keep downstream parser consumers from owning raw client-to-GRE parsing.

## Checks Run

```bash
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py
python3 -m pytest -q tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check
python3 -m pytest -q
```

## Results

- `python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py`
  -> `78 passed in 0.06s`.
- `python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py`
  -> `60 passed in 0.13s`.
- `python3 -m pytest -q tests/test_grp_id_candidates.py tests/test_parser_regressions.py`
  -> `14 passed in 0.14s`.
- `python3 -m ruff check src tests` -> `All checks passed!`.
- `git diff --check` -> passed with no output.
- `python3 -m pytest -q` -> `443 passed in 0.90s`.

## Confirmed Contract Matches

- `try_parse()` returns either `ClientActionEvent` or `None` according to the
  contract.
- UI messages emit `type == "client_ui_message"` and preserve the parsed
  envelope under `raw_client_action`.
- Generic GRE messages emit `type == "generic_client_action"`, preserve
  `message_type`, tolerate missing and blank message types as `""`, and
  preserve raw envelopes, including stringified inner payloads.
- Mulligan responses emit `type == "mulligan_resp"`, normalize known decisions
  to `mulligan` and `keep`, preserve unknown truthy decisions, and default
  missing or malformed decisions to `""`.
- Select-N responses emit `type == "select_n_resp"` and normalize selected
  option/object IDs with malformed values dropped.
- Submit-deck responses emit `type == "submit_deck_resp"` with stable
  `deck_cards` and `sideboard_cards` fields, preserve direct/nested/list-valued
  source behavior, and default malformed shapes to empty lists.
- Specialized payloads include `game_state_id`, `resp_id`, `request_id`, and
  `raw_client_action`, with missing context defaulting to `0` and present
  context copied as-is.
- Marker classification remains substring-based over the body, UI marker
  priority is preserved, JSON envelope parsing matches `api_common`, inner
  payload extraction accepts dict and stringified dict values, and malformed
  GRE candidates return `None`.
- Focused tests were added for the missing parser coverage identified by the
  contract, without changing parser/runtime code.
- Downstream state, transforms, extractors, runtime surfaces, analytics,
  runner, and GRP candidate consumers continue to consume parser-produced
  client-action payloads and do not own raw client-to-GRE parsing.
- No parser state, workbook schema, webhook payload shape, Apps Script
  behavior, parser event classes, match/game identity, deduplication, final
  reconciliation, secrets, environment variables, raw logs, generated data,
  runtime status files, failed posts, or workbook exports changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

The focused parser test additions cover the contract's previously identified
gaps for metadata, marker classification, UI priority, generic fallback,
stringified payload preservation, mulligan normalization, malformed specialized
payload fallback, selected/card ID normalization, submit-deck source behavior,
request-context defaults/copying, invalid JSON, non-dict envelopes, and invalid
GRE inner payloads.

## Drift Notes

- No parser behavior drift found.
- No downstream ownership drift found; raw client-to-GRE parsing remains in
  `client_actions.py`.
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
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #20 and the parser client-actions contract audit.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/20

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_client_actions.md
- docs/implementation_handoffs/parser_client_actions_comparison.md
- docs/contract_test_reports/parser_client_actions.md
- tests/test_client_actions_parser.py

Reviewer verdict:
No blocking findings. The parser client-actions contract audit is ready for submitter work.

Submitter requirements:
- Verify current branch and changed-file scope.
- Stage only the reviewed parser client-actions audit artifacts.
- Commit and push the branch.
- Open or update a draft PR targeting codex/parser-module-audit-suite, not main.
- Do not merge, close issue #20, or mark tracker #5 complete; those are Codex G responsibilities.

Validation to run or verify:
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py
python3 -m pytest -q tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check
python3 -m pytest -q

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not merge or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/20"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_client_actions.md"
  target_artifact: "docs/contract_test_reports/parser_client_actions.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py -> 78 passed in 0.06s"
    - "python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py -> 60 passed in 0.13s"
    - "python3 -m pytest -q tests/test_grp_id_candidates.py tests/test_parser_regressions.py -> 14 passed in 0.14s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed with no output"
    - "python3 -m pytest -q -> 443 passed in 0.90s"
  stop_conditions:
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not merge, close issue #20, or mark tracker #5 complete; route deployer work to Codex G."
    - "Do not target main unless explicitly approved."
```
