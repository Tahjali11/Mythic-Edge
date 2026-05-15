# Parser Event Identity Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/14

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Issue #14 is a no-known-bug parser module audit for
`src/mythic_edge_parser/app/event_identity.py`. It classifies the work as
high-risk because parser-owned event classification fields feed match history,
runtime filters, debug payloads, and downstream analytics.

## Contract

`docs/contracts/parser_event_identity.md`

## Role Performed

Module Implementer / comparison thread.

This pass compared the current event identity implementation, focused tests,
model integration, runtime-history consumers, and parser regression fixtures
against the parser event identity contract.

## Current Behavior Summary

`event_identity.py` is broadly aligned with the contract. It normalizes raw
descriptors with string trimming, lowercasing, and non-alphanumeric collapse;
classifies queue subtype before deriving event family and rankedness; returns
an immutable `EventIdentity`; and exposes stable dictionary keys and boolean
properties.

The comparison found no parser behavior mismatch. It did find missing focused
tests required by the contract, so this thread added test-only coverage in the
owned and referenced consumer tests.

## Confirmed Matches

- Public API matches the contract: `EventIdentity` is a frozen, slotted
  dataclass and `classify_event_identity(event_id, super_format,
  match_win_condition)` remains the public classifier.
- Input normalization matches the contract: values are normalized with
  `str(value or "").strip()`, lowercased, and collapsed with
  `re.sub(r"[^a-z0-9]+", "", text)`.
- Missing, falsey, numeric, and novel descriptors degrade to explicit
  `"unknown"` fields without raising.
- Play mode family precedence matches the contract: limited keywords beat
  constructed keywords.
- Queue subtype precedence matches the contract: special-event keywords are
  checked before draft/sealed, ladder, play, constructed-event, and broad
  constructed fallback rules.
- Rankedness matches the contract: ranked ladder, quick draft, and premier
  draft are ranked; play queues, constructed queue, traditional draft, sealed,
  jump in, and non-competitive special events are unranked; competitive special
  events remain unknown.
- `rank_eligible` is derived only from `rank_match_type == "ranked"`.
- Boolean properties match their contracted field predicates.
- `EventIdentity.to_dict()` returns the five constructor fields plus all
  contracted boolean property keys.
- `MatchSummary.event_identity()` delegates classification to
  `classify_event_identity()` and does not own classification rules.
- `MatchSummary.to_debug_dict()` embeds `event_identity.to_dict()` under
  `"event_identity"`, and parser regression fixtures include those values.
- `MatchSummary.to_history_item()` exposes parser-produced event identity
  fields and boolean properties.
- `runtime_surfaces.filter_match_history_payload()` consumes exact
  parser-produced classification strings and does not reclassify raw MTGA
  descriptors.
- `_build_history_filters()` builds available filter values from parser-produced
  history-item classification fields.
- `event_identity.py` has no file I/O, webhook submission, workbook mutation,
  Apps Script mutation, parser-state mutation, environment access, raw-log
  access, generated-data refresh, runtime status writes, failed-post access, or
  workbook export access.

## Contract Mismatches

No contract mismatches were found.

No parser behavior was changed. No workbook schema, webhook payload shape, Apps
Script behavior, parser state, match/game identity, final reconciliation,
secrets, raw logs, generated data, runtime status files, failed posts, or
workbook exports changed.

## Missing Or Weak Tests

Resolved in this implementation pass:

- Added focused coverage for premier draft as ranked limited draft.
- Added focused coverage for generic draft fallback.
- Added focused coverage for best-of-one ranked ladder.
- Added focused coverage for broad constructed fallback to
  `constructed_queue`.
- Added focused coverage for every currently contracted special keyword subtype
  and generic `special_event` fallback.
- Added focused coverage that competitive special events keep rankedness
  `"unknown"`.
- Added focused coverage for `None`, blank, numeric, falsey, and novel
  descriptors returning unknown classifications.
- Added focused coverage for case, punctuation, space, hyphen, and underscore
  insensitive normalization.
- Added focused coverage for all contracted boolean invariants.
- Added focused coverage for `EventIdentity.to_dict()` key shape.
- Strengthened model history-item coverage to assert all event-identity boolean
  fields are exposed by `MatchSummary.to_history_item()`.
- Strengthened runtime surface filtering coverage to filter by
  `rank_match_type`, `play_mode_family`, `event_family`, and `queue_subtype`.

Remaining non-blocking gaps:

- There is no direct test that `EventIdentity` assignment raises because the
  dataclass is frozen; the implementation is visibly frozen and slotted.
- Parser regression fixtures cover event identity in debug payloads for current
  replay slices, but they do not enumerate every queue subtype.
- MTGA event-name drift cannot be exhaustively protected by static tests; new
  descriptors should continue to get contract/test updates before downstream
  consumers rely on new strings.

## Files Changed

- `docs/implementation_handoffs/parser_event_identity_comparison.md`
- `tests/test_event_identity.py`
- `tests/test_app_models.py`
- `tests/test_runtime_surfaces.py`

## Code Changed

None.

## Tests Changed

Focused tests were added or strengthened only to cover contract-required
behavior. No parser behavior changed.

## Interface Changes

None.

No function signatures, event classes, payload fields, workbook columns,
environment variables, Apps Script entrypoints, match identity rules, game
identity rules, final reconciliation behavior, or runtime artifact shapes
changed.

## Validation Evidence

Static inspection:

- Read `docs/agent_constitution.md`.
- Read `docs/agent_threads/implementation.md`.
- Read `docs/codex_module_workflow.md`.
- Read `docs/contracts/parser_event_identity.md`.
- Reviewed GitHub issue #14.
- Compared `src/mythic_edge_parser/app/event_identity.py`.
- Compared `tests/test_event_identity.py`.
- Compared `src/mythic_edge_parser/app/models.py`.
- Compared `src/mythic_edge_parser/app/runtime_surfaces.py`.
- Compared `tests/test_app_models.py`.
- Compared `tests/test_runtime_surfaces.py`.
- Compared `tests/test_parser_regressions.py`.
- Checked parser regression expected fixtures for embedded `event_identity`
  payloads.

Focused event identity validation:

```bash
python3 -m pytest -q tests/test_event_identity.py
```

Result:

```text
36 passed in 0.04s
```

Related consumer validation:

```bash
python3 -m pytest -q tests/test_app_models.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
```

Result:

```text
24 passed in 0.15s
```

Lint:

```bash
python3 -m ruff check src tests
```

Result:

```text
All checks passed!
```

Full repo validation:

```bash
python3 -m pytest -q
```

Result:

```text
389 passed in 0.88s
```

## Still Unverified

- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Webhook dispatch was not exercised.
- Runtime dashboard/UI behavior was not manually inspected.
- Unknown future MTGA event IDs remain an expected drift risk.

## Reviewer Focus

Ask the Module Reviewer to verify:

- Special-event keyword precedence remains ahead of draft and constructed
  fallback rules.
- Competitive special events remain rankedness `"unknown"`.
- Unknown and falsey descriptors do not invent classification certainty.
- `rank_eligible` remains equivalent to rankedness.
- `MatchSummary` and runtime surfaces consume parser-produced classifications
  without owning classification truth.
- No downstream surface or parser-state behavior changed.

## Next Recommended Role

Module Reviewer in contract-test mode.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for https://github.com/Tahjali11/Mythic-Edge/issues/14, docs/contracts/parser_event_identity.md, and docs/implementation_handoffs/parser_event_identity_comparison.md.

Review the event identity implementation and test-only Module Implementer changes in:
- src/mythic_edge_parser/app/event_identity.py
- tests/test_event_identity.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_app_models.py
- tests/test_runtime_surfaces.py
- tests/test_parser_regressions.py

Verify the implementation against the parser event identity contract. Confirm special-event keyword precedence, rankedness rules, unknown fallback behavior, boolean invariants, EventIdentity.to_dict() shape, MatchSummary history/debug exposure, and runtime filtering by parser-produced classification fields. Confirm no workbook schema, webhook payload shape, Apps Script behavior, parser state, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Produce docs/contract_test_reports/parser_event_identity.md with findings first if any, contract-test verdict, validation evidence, remaining gaps, next recommended role, and a workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/14"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/parser_event_identity_comparison.md"
  target_artifact: "docs/contract_test_reports/parser_event_identity.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_event_identity.py -> 36 passed in 0.04s"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py -> 24 passed in 0.15s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "python3 -m pytest -q -> 389 passed in 0.88s"
  stop_conditions:
    - "Stop and route back to Module Contract Writer if event identity classification precedence is ambiguous."
    - "Stop and route back to Thinker if review discovers scope outside issue #14."
    - "Do not move parser-owned classification truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI interpretation."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main until the parser module audit suite is complete."
```
