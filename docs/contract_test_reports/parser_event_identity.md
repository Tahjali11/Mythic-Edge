# Parser Event Identity Contract Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/14

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_event_identity.md`

## Implementation Under Test

- `src/mythic_edge_parser/app/event_identity.py`
- `tests/test_event_identity.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_app_models.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_parser_regressions.py`

Comparison artifact reviewed:

- `docs/implementation_handoffs/parser_event_identity_comparison.md`

## Contract-Test Verdict

Approved for Module Submitter.

The current implementation and test-only Module Implementer changes satisfy the
parser event identity contract. No parser behavior changes were found beyond
focused test coverage and contract/comparison artifacts.

## Confirmed Matches

- Special-event keyword checks remain ahead of draft, sealed, ladder, play, and
  broad constructed fallback rules.
- Rankedness rules match the contract: ranked ladder, quick draft, and premier
  draft are ranked; play queues, constructed queue, traditional draft, sealed,
  jump in, and non-competitive special events are unranked; generic draft and
  unknown queues remain unknown.
- Competitive special events, including qualifier, arena open, play-in, and
  generic special challenge cases, remain `rank_match_type == "unknown"`.
- Missing, blank, falsey, numeric, and novel descriptors return unknown
  classifications without raising or inventing certainty.
- Normalization is punctuation-, case-, space-, hyphen-, and
  separator-insensitive.
- Boolean invariants hold, including
  `rank_eligible == (rank_match_type == "ranked")`.
- `EventIdentity.to_dict()` retains the stable field and boolean key shape.
- `MatchSummary.event_identity()` delegates to
  `classify_event_identity()` using parser-produced `event_id`,
  `super_format`, and `match_win_condition`.
- `MatchSummary.to_debug_dict()` embeds `event_identity.to_dict()` and
  `MatchSummary.to_history_item()` exposes the parser-produced classification
  fields and booleans.
- `runtime_surfaces.filter_match_history_payload()` and history filter building
  consume parser-produced classification fields without reclassifying raw MTGA
  descriptors.
- No workbook schema, webhook payload shape, Apps Script behavior, parser
  state, match identity, game identity, final reconciliation, secrets, raw
  logs, generated data, runtime status files, failed posts, or workbook exports
  changed.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests remain for the Issue #14 contract.

The Module Implementer test-only changes cover:

- premier draft ranked limited classification
- generic draft unknown-rankedness fallback
- best-of-one ranked ladder
- constructed queue fallback
- every currently contracted special-event keyword subtype
- competitive special event unknown rankedness
- missing, falsey, numeric, and novel descriptor unknown fallback
- normalization across punctuation, case, and separators
- boolean invariants
- `EventIdentity.to_dict()` key shape
- model history item boolean exposure
- runtime history filtering by parser-produced classification fields

## Drift Classification

- Parser behavior drift: none found. `src/mythic_edge_parser/app/event_identity.py`
  was reviewed unchanged in behavior.
- Parser truth ownership drift: none found. Event classification remains owned by
  `event_identity.py`; model and runtime surfaces consume those outputs.
- Workbook/webhook/schema drift: none found.
- Runtime surface drift: no reclassification drift found; runtime filters
  compare existing parser-produced fields directly.
- Test/docs drift: intended contract/comparison artifacts and focused tests are
  present for Issue #14.

## Validation Results

```text
python3 -m pytest -q tests/test_event_identity.py
36 passed in 0.04s
```

```text
python3 -m pytest -q tests/test_app_models.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
24 passed in 0.11s
```

```text
python3 -m ruff check src tests
All checks passed!
```

Full repo validation:

```text
python3 -m pytest -q
389 passed in 0.88s
```

## Remaining Non-Blocking Gaps

- Future MTGA event-name drift remains a normal contract maintenance risk.
- Parser regression fixtures cover current replay slices, not every queue
  subtype.
- There is no direct immutability mutation assertion for the frozen
  `EventIdentity` dataclass; static inspection confirms `frozen=True` and
  `slots=True`.

## Recommendation

Next recommended role: Module Submitter.

No blocking contract-test findings remain for Issue #14.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/14"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_event_identity.md"
  target_artifact: "module PR targeting codex/parser-module-audit-suite"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  verdict: "approved_for_submitter"
  validation:
    - "python3 -m pytest -q tests/test_event_identity.py -> 36 passed"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py -> 24 passed"
    - "python3 -m ruff check src tests -> All checks passed"
    - "python3 -m pytest -q -> 389 passed"
  stop_conditions:
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Route back to Module Contract Writer if event identity classification precedence changes or becomes ambiguous."
```
