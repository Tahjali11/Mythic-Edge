# Parser Match State Contract Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/16

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_match_state.md`

## Implementation Under Test

- `src/mythic_edge_parser/parsers/match_state.py`
- `tests/test_match_state_parser.py`
- `tests/test_parsers.py`
- `docs/contracts/parser_match_state.md`
- `docs/implementation_handoffs/parser_match_state_comparison.md`

Related consumers inspected:

- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_transforms.py`
- `tests/test_runtime_surfaces.py`

## Contract-Test Verdict

Approved for Module Submitter.

The current match-state parser implementation and Module Implementer test-only
changes satisfy the parser match-state contract. No parser behavior changes
were found beyond focused test coverage and contract/comparison artifacts.

## Confirmed Matches

- `try_parse()` remains marker-gated on `matchGameRoomStateChangedEvent`.
- Non-candidate bodies, malformed marker-present JSON, and parsed payloads with
  no supported state-event dict return `None`.
- Wrapped payloads and bare `gameRoomInfo` payloads remain compatible.
- Non-dict wrapper values fall through to bare `gameRoomInfo` validation when
  that supported bare shape is present.
- Successful parses emit `MatchStateEvent` with the provided timestamp,
  encoded raw body, `kind == "MatchState"`, and
  `PerformanceClass.INTERACTIVE_DISPATCH`.
- `build_payload()` always emits the contracted base fields:
  `type`, `state_type`, `match_id`, `event_id`, `players`, and
  `raw_match_state`.
- State-type mapping matches the contract:
  `MatchGameRoomStateType_Playing` -> `match_started`,
  `MatchGameRoomStateType_MatchCompleted` -> `match_completed`, and unknown or
  missing state types -> `state_changed`.
- Player normalization matches the contract: non-list containers become `[]`,
  non-dict entries are skipped, selected-source order is preserved, and missing
  scalar fields use `""` or `0` defaults.
- Player source precedence is preserved: non-empty
  `gameRoomConfig.reservedPlayers` wins, otherwise `gameRoomInfo.players` is
  used.
- Event ID precedence is preserved: trimmed config `eventId`, then first
  selected-player `eventId`, then `""`.
- Final result extraction is parser-local and shape-safe: non-empty dict
  `finalMatchResult` adds `match_completed_reason` and `game_results`;
  malformed or missing final-result payloads omit those fields.
- `resultList` normalization preserves game-scope and match-scope entries,
  skips non-dict entries, keeps result order, and uses contracted defaults,
  including missing `winning_team_id == 0`.
- `raw_match_state` remains present on successful payloads for parser/debug
  inspection and is not promoted into workbook schema.
- Parser truth boundaries are preserved: `match_state.py` normalizes parser
  facts, while `state.py` owns summary mutation and final reconciliation.
- No workbook schema, webhook payload shape, Apps Script behavior, parser state
  final reconciliation, extractor behavior, match identity, game identity,
  deduplication, secrets, raw logs, generated data, runtime status files,
  failed posts, or workbook exports changed.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests remain for the Issue #16 contract.

The Module Implementer test-only changes cover:

- successful parse metadata and raw payload preservation
- no-marker and malformed JSON `None` paths
- unsupported parsed payload `None` paths
- non-dict wrapper fallback to bare `gameRoomInfo`
- unknown state type fallback to `state_changed`
- mixed player-list filtering, defaults, and ordering
- config and selected-player event ID precedence
- empty `reservedPlayers` fallback to `gameRoomInfo.players`
- malformed and mixed final result lists
- result scope/order/default preservation

## Drift Classification

- Parser behavior drift: none found. `src/mythic_edge_parser/parsers/match_state.py`
  was reviewed unchanged in behavior.
- Parser truth ownership drift: none found. Match-state parsing remains in
  `match_state.py`; runtime state mutation and final reconciliation remain in
  `state.py`.
- Workbook/webhook/schema drift: none found.
- Runtime/transform drift: none found. Consumers continue to use
  parser-produced payload fields and do not parse raw match-state JSON.
- Test/docs drift: intended contract/comparison artifacts and focused parser
  tests are present for Issue #16.

## Validation Results

```text
python3 -m pytest -q tests/test_match_state_parser.py tests/test_parsers.py
24 passed in 0.03s
```

```text
python3 -m pytest -q tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py
22 passed in 0.10s
```

```text
python3 -m ruff check src tests
All checks passed!
```

Full repo validation:

```text
python3 -m pytest -q
396 passed in 0.88s
```

Additional whitespace check:

```text
git diff --check
passed
```

## Remaining Non-Blocking Gaps

- Future MTGA match-room payload-shape drift remains a normal parser audit
  risk.
- `match_state.py` still does not infer explicit game numbers from
  `finalMatchResult.resultList`; the contract leaves that outside the current
  payload truth because no such source field is contracted.
- `raw_match_state` remains shallow raw payload data and should be treated as
  read-only by consumers, as documented by the contract.

## Recommendation

Next recommended role: Module Submitter.

No blocking contract-test findings remain for Issue #16.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/16"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_match_state.md"
  target_artifact: "module PR targeting codex/parser-module-audit-suite"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  verdict: "approved_for_submitter"
  validation:
    - "python3 -m pytest -q tests/test_match_state_parser.py tests/test_parsers.py -> 24 passed"
    - "python3 -m pytest -q tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py -> 22 passed"
    - "python3 -m ruff check src tests -> All checks passed"
    - "python3 -m pytest -q -> 396 passed"
    - "git diff --check -> passed"
  stop_conditions:
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned match-state truth into workbook formulas, dashboard logic, Apps Script, or AI-generated interpretation."
```
