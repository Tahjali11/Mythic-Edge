# Parser Event Identity Module Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/14

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Adjacent contract:

- `docs/contracts/parser_models.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the parser-owned event identity classifier in
`src/mythic_edge_parser/app/event_identity.py`. It is a contract artifact only.
It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/app/event_identity.py`

The module converts raw or missing MTGA event descriptors into stable,
normalized match classification facts.

## Owning Layer

Parser and state interpretation.

`event_identity.py` owns parser classification truth for:

- ranked / unranked / unknown match type
- constructed / limited / unknown play mode family
- ladder / queue / draft / sealed / special event / unknown event family
- queue subtype
- rank eligibility
- boolean classification convenience fields

Workbook formulas, dashboard filters, webhook transport, Apps Script, and AI
analysis must consume these parser-produced classifications rather than
reclassifying MTGA event descriptors downstream.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/event_identity.py`
- `tests/test_event_identity.py`
- `docs/contracts/parser_event_identity.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `docs/contracts/parser_models.md`
- `tests/test_app_models.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_parser_regressions.py`
- `tests/fixtures/parser_regression_match_expected.json`
- `tests/fixtures/parser_regression_bo3_expected.json`

## Public Interface

### `EventIdentity`

`EventIdentity` is a frozen, slotted dataclass with these constructor fields:

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `rank_match_type` | `str` | `"unknown"` | Rankedness classification. |
| `play_mode_family` | `str` | `"unknown"` | Constructed/limited family classification. |
| `event_family` | `str` | `"unknown"` | Match classification family, distinct from sheet row `event_family`. |
| `queue_subtype` | `str` | `"unknown"` | Specific queue/event subtype classification. |
| `rank_eligible` | `bool` | `False` | Whether this match should be treated as ranked for parser analytics. |

`EventIdentity` exposes these boolean properties:

- `is_ranked_match`
- `is_unranked_match`
- `is_constructed_match`
- `is_limited_match`
- `is_draft_match`
- `is_sealed_match`
- `is_ladder_match`
- `is_special_event_match`
- `is_event_match`

`EventIdentity.to_dict() -> dict[str, object]` returns the five constructor
fields plus all boolean property values.

### `classify_event_identity()`

Signature:

```python
classify_event_identity(
    event_id: object,
    super_format: object,
    match_win_condition: object,
) -> EventIdentity
```

The function is the public classifier. It must remain callable with ordinary
Python objects, including `None`, blank strings, numeric values, and MTGA raw
descriptor strings.

## Inputs

### Raw Descriptor Inputs

| Input | Current source | Meaning |
| --- | --- | --- |
| `event_id` | `MatchSummary.event_id` | Raw MTGA event identifier such as `Traditional_Ladder`, `Play`, `QuickDraft_BLOOMBURROW`, or `Event_Constructed_BestOfThree`. |
| `super_format` | `MatchSummary.super_format` | Raw MTGA super-format descriptor such as `SuperFormat_Constructed`, `SuperFormat_Limited`, or `SuperFormat_Standard`. |
| `match_win_condition` | `MatchSummary.match_win_condition` | Raw MTGA win-condition descriptor such as `MatchWinCondition_BestOfOne`, `MatchWinCondition_Best2of3`, or `MatchWinCondition_BestOfThree`. |

### Input Normalization

Observed normalization:

- Each input is first normalized with `str(value or "").strip()`.
- Falsey values such as `None`, `""`, `0`, and `False` normalize to an empty
  string before classification.
- The classifier then lowercases the text and removes every non-alphanumeric
  character with `re.sub(r"[^a-z0-9]+", "", text)`.
- Keyword matching is therefore case-insensitive and ignores spaces,
  underscores, hyphens, punctuation, and MTGA enum separators.

Required guarantees:

- Missing, falsey, malformed, or novel descriptor values must degrade to
  `"unknown"` classifications rather than raising or inventing certainty.
- Normalization must not require callers to pre-normalize MTGA enum strings.
- Classification must not depend on workbook formulas, webhook payload shape,
  Apps Script behavior, dashboard filters, or AI interpretation.

## Outputs

### Allowed `rank_match_type` Values

| Value | Meaning |
| --- | --- |
| `"ranked"` | Parser has classified the match as ranked. |
| `"unranked"` | Parser has classified the match as unranked. |
| `"unknown"` | Parser does not have enough contracted evidence to classify rankedness. |

Observed `rank_match_type` rules:

- `"ranked"` for `ranked_ladder`, `traditional_ranked_ladder`, `quick_draft`,
  and `premier_draft`.
- `"unranked"` for `play_queue`, `traditional_play_queue`,
  `constructed_queue`, `traditional_draft`, `sealed`, `jump_in`,
  `midweek_magic`, `festival`, `decathlon`, `cube_event`, `momir_event`, and
  `omniscience_event`.
- Special events with competitive keywords `qualifier`, `arenaopen`, `playin`,
  or `challenge` remain `"unknown"` when they classify as `special_event`.
- Other recognized non-competitive special events classify as `"unranked"`.
- Any remaining case is `"unknown"`.

Required guarantees:

- `rank_eligible` must be `True` if and only if `rank_match_type == "ranked"`.
- Unknown rankedness must not be converted to unranked downstream.
- Competitive special events should remain `"unknown"` unless a future contract
  names direct evidence for their rankedness.

### Allowed `play_mode_family` Values

| Value | Meaning |
| --- | --- |
| `"constructed"` | Event descriptors look constructed. |
| `"limited"` | Event descriptors look draft, sealed, or limited. |
| `"unknown"` | Parser does not have enough evidence. |

Observed `play_mode_family` rules:

- The classifier combines normalized `event_id` and `super_format`.
- If the combined text contains `draft`, `sealed`, or `limited`, the result is
  `"limited"`.
- Otherwise, if the combined text contains `constructed`, `standard`,
  `alchemy`, `historic`, `explorer`, `timeless`, `brawl`, `play`, or `ladder`,
  the result is `"constructed"`.
- Limited keywords take precedence over constructed keywords.
- Otherwise, the result is `"unknown"`.

### Allowed `event_family` Values

| Value | Meaning |
| --- | --- |
| `"draft"` | Draft event family. |
| `"sealed"` | Sealed event family. |
| `"ladder"` | Ranked ladder family. |
| `"special_event"` | Special event family. |
| `"queue"` | Play/constructed queue family. |
| `"unknown"` | Parser does not have enough evidence. |

Important naming rule:

- This `event_family` is an event identity classification field. It is distinct
  from row/sheet `event_family` values such as `MatchLogRow`, `GameLogRow`,
  `MatchSummary`, `GameState`, or `ParserStatusRow`.

Observed `event_family` rules:

- Draft queue subtypes become `"draft"`.
- `sealed` becomes `"sealed"`.
- Ranked ladder queue subtypes become `"ladder"`.
- Special-event queue subtypes and subtypes ending in `_event` become
  `"special_event"`.
- `Play`, `play_queue`, `traditional_play_queue`, and `constructed_queue`
  become `"queue"`.
- Otherwise, the result is `"unknown"`.

### Allowed `queue_subtype` Values

Currently allowed values:

- `"quick_draft"`
- `"premier_draft"`
- `"traditional_draft"`
- `"draft"`
- `"sealed"`
- `"ranked_ladder"`
- `"traditional_ranked_ladder"`
- `"play_queue"`
- `"traditional_play_queue"`
- `"constructed_queue"`
- `"midweek_magic"`
- `"festival"`
- `"qualifier"`
- `"arena_open"`
- `"play_in"`
- `"decathlon"`
- `"jump_in"`
- `"cube_event"`
- `"momir_event"`
- `"omniscience_event"`
- `"special_event"`
- `"unknown"`

Observed `queue_subtype` precedence:

1. Special event keywords in `event_id` are checked first:
   - `midweekmagic -> midweek_magic`
   - `festival -> festival`
   - `qualifier -> qualifier`
   - `arenaopen -> arena_open`
   - `playin -> play_in`
   - `decathlon -> decathlon`
   - `jumpin -> jump_in`
   - `cube -> cube_event`
   - `momir -> momir_event`
   - `omniscience -> omniscience_event`
2. If no specific special keyword matches but `event_id` contains `special`,
   queue subtype is `"special_event"`.
3. Draft and sealed keywords are checked next:
   - `quickdraft -> quick_draft`
   - `premierdraft -> premier_draft`
   - `traditionaldraft -> traditional_draft`
   - other `draft -> draft`
   - `sealed -> sealed`
4. Ladder keywords classify as `"traditional_ranked_ladder"` when
   `event_id` or `match_win_condition` looks best-of-three/traditional;
   otherwise they classify as `"ranked_ladder"`.
5. Exact normalized `event_id == "play"` classifies as
   `"traditional_play_queue"` when best-of-three/traditional; otherwise
   `"play_queue"`.
6. Constructed event identifiers classify as play queues:
   - `eventconstructedbestofthree` or `constructedbestofthree` ->
     `"traditional_play_queue"`
   - `eventconstructedbestofone` or `constructedbestofone` -> `"play_queue"`
7. If play mode is constructed but no specific subtype matched, queue subtype is
   `"constructed_queue"`.
8. Otherwise, queue subtype is `"unknown"`.

Required guarantees:

- Specific queue/event keywords must take precedence over broad constructed
  fallback.
- Special-event keyword classification must happen before broad draft,
  constructed, or queue fallback.
- New queue subtype strings require a contract/test update before downstream
  consumers rely on them.

## Boolean Invariants

Required invariants:

- `is_ranked_match == (rank_match_type == "ranked")`
- `is_unranked_match == (rank_match_type == "unranked")`
- `is_constructed_match == (play_mode_family == "constructed")`
- `is_limited_match == (play_mode_family == "limited")`
- `is_draft_match == (event_family == "draft")`
- `is_sealed_match == (event_family == "sealed")`
- `is_ladder_match == (event_family == "ladder")`
- `is_special_event_match == (event_family == "special_event")`
- `is_event_match == (event_family in {"draft", "sealed", "special_event"})`
- `rank_eligible == is_ranked_match`

Derived implications:

- `is_ranked_match` and `is_unranked_match` may both be `False` when
  `rank_match_type == "unknown"`.
- `is_constructed_match` and `is_limited_match` may both be `False` when
  `play_mode_family == "unknown"`.
- At most one of `is_draft_match`, `is_sealed_match`, `is_ladder_match`, and
  `is_special_event_match` should be true for a single `EventIdentity`.
- `is_event_match` is false for `"ladder"`, `"queue"`, and `"unknown"` event
  families.

## Downstream Consumers

### `MatchSummary.event_identity()`

`src/mythic_edge_parser/app/models.py` calls:

```python
classify_event_identity(
    self.event_id,
    self.super_format,
    self.match_win_condition,
)
```

The model delegates classification to `event_identity.py`. It does not own the
classification rules.

### `MatchSummary.to_debug_dict()`

`to_debug_dict()` embeds `event_identity.to_dict()` under the
`"event_identity"` key. Parser regression fixtures currently include these
values inside debug payloads.

### `MatchSummary.to_history_item()`

`to_history_item()` exposes these parser-produced classification fields:

- `rank_match_type`
- `play_mode_family`
- `event_family`
- `queue_subtype`
- `rank_eligible`
- all boolean convenience fields from `EventIdentity`

These values are used by runtime match history surfaces and filters.

### `runtime_surfaces.py`

`filter_match_history_payload()` filters history items by exact string equality
for `rank_match_type`, `play_mode_family`, `event_family`, and `queue_subtype`.

`_build_history_filters()` builds available filter values from those same
history-item fields.

Runtime surfaces consume parser-produced classifications. They must not
reclassify raw MTGA descriptors or become classification truth owners.

## Invariants

- Event identity classification must be pure and deterministic for the same
  inputs.
- `classify_event_identity()` must not mutate parser state, model objects,
  runtime surface state, files, workbook state, webhook state, or environment
  variables.
- `EventIdentity` instances should remain immutable value objects.
- Output strings are lower-case snake-case vocabulary except `"unknown"`,
  `"ranked"`, and `"unranked"`.
- Missing or unknown raw descriptor values must remain explicit `"unknown"`
  output values.
- Exact output strings are compatibility surface for parser regression fixtures,
  runtime filters, and analytics consumers.

## Error Behavior

Observed behavior:

- `None`, blank strings, `0`, and `False` normalize to empty input keys.
- Missing or empty descriptors classify as:
  - `rank_match_type == "unknown"`
  - `play_mode_family == "unknown"`
  - `event_family == "unknown"`
  - `queue_subtype == "unknown"`
  - `rank_eligible is False`
- Unknown but truthy descriptor objects are converted through `str()` before
  normalization.
- No external data is read and no exception is intentionally raised for ordinary
  missing or novel MTGA descriptor values.

Not guaranteed:

- Objects whose `__str__` implementation raises are outside the current
  supported input contract.
- The classifier does not validate that raw descriptors came from MTGA.

## Side Effects

`event_identity.py` has no intended side effects.

The module must not:

- write files
- post webhooks
- mutate workbook state
- mutate Apps Script behavior
- mutate parser runtime state
- read secrets
- read environment variables
- inspect raw logs directly
- refresh generated data
- write runtime status files
- read failed posts or workbook exports

## Dependency Order

If future work changes this contract, update and validate in this order:

1. Update `docs/contracts/parser_event_identity.md` to define the intended
   classification behavior.
2. Update `src/mythic_edge_parser/app/event_identity.py`.
3. Update `tests/test_event_identity.py`.
4. Update `src/mythic_edge_parser/app/models.py` only if the
   `MatchSummary.event_identity()` integration changes.
5. Update `src/mythic_edge_parser/app/runtime_surfaces.py` only if history
   filter consumption changes.
6. Update parser regression fixtures if debug/history identity payloads
   intentionally change.
7. Update adjacent contracts such as `docs/contracts/parser_models.md` if model
   or history item obligations change.

## Compatibility

Compatibility requirements:

- Preserve the public `EventIdentity` field names.
- Preserve `to_dict()` keys for all five fields and all boolean properties.
- Preserve `classify_event_identity(event_id, super_format, match_win_condition)`
  as the public classifier signature.
- Preserve existing allowed output strings unless a future contract explicitly
  changes them.
- Preserve `"unknown"` fallback behavior for missing and novel descriptors.
- Preserve `rank_eligible == (rank_match_type == "ranked")`.
- Do not rename classification `event_family` without a broader model/runtime
  contract update because `event_family` is already consumed by history filters
  and parser regression fixtures.

## Unknowns And Contract Risks

- Competitive special events such as qualifier, arena open, play-in, and
  challenge currently remain rankedness `"unknown"`. This is deliberate until
  there is direct evidence.
- The current queue subtype vocabulary is code-owned and keyword-based, not
  data-driven.
- Bare `challenge` is a competitive special-event rankedness keyword only when
  the event already classifies as `special_event`; no current queue subtype maps
  a bare challenge event by itself.
- Keyword ordering is high risk: broad fallback such as constructed queue can
  hide missed specific event IDs if tests do not cover them.
- MTGA event IDs may drift, producing `"unknown"` or overly broad fallback
  categories.
- `event_family` naming is overloaded across the repo. This contract covers
  only the event identity classification field, not row/sheet family fields.

## Tests Required

Focused contract validation:

```powershell
py -m pytest -q tests/test_event_identity.py
```

Related consumer validation:

```powershell
py -m pytest -q tests/test_app_models.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
```

Lint before submitter work:

```powershell
py -m ruff check src tests
```

On non-Windows shells, use the equivalent Python invocation:

```bash
python3 -m pytest -q tests/test_event_identity.py
python3 -m pytest -q tests/test_app_models.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
python3 -m ruff check src tests
```

Required focused coverage for the next implementation/comparison thread:

- Existing known cases must stay covered:
  - traditional ranked ladder
  - play queue
  - constructed best-of-one event
  - constructed best-of-three event
  - quick draft
  - traditional draft
  - sealed
  - midweek magic
- Add or confirm coverage for:
  - premier draft as ranked limited draft
  - generic draft fallback
  - ranked ladder best-of-one
  - constructed fallback to `constructed_queue`
  - all special keyword subtypes
  - competitive special events remaining rankedness `"unknown"`
  - missing, `None`, numeric, and novel descriptors returning unknowns
  - punctuation/case/underscore-insensitive normalization
  - every boolean invariant listed above
  - `EventIdentity.to_dict()` key shape
  - model history item exposure through `MatchSummary.to_history_item()`
  - runtime history filtering by classification fields

## Acceptance Criteria

- `docs/contracts/parser_event_identity.md` exists on
  `codex/parser-module-audit-suite`.
- The contract names parser and state interpretation as the truth-owning layer.
- The public API is defined.
- Input normalization is defined.
- Allowed output values are enumerated.
- Fallback behavior is explicit.
- Boolean invariants are testable.
- Downstream consumers are listed without moving truth downstream.
- Compatibility expectations and test obligations are listed.
- No parser behavior, workbook schema, webhook payload, Apps Script behavior,
  parser state, match/game identity, final reconciliation, secrets, raw logs,
  generated data, runtime status files, failed posts, or workbook exports are
  changed by this contract thread.

## Next Workflow Action

Next role: Module Implementer (C).

The next thread should compare the current implementation and focused tests to
this contract, then produce
`docs/implementation_handoffs/parser_event_identity_comparison.md`. Because
issue #14 is a no-known-bug audit, it should not change behavior unless the
comparison finds a clear contract mismatch or missing focused tests required by
this contract.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Implementer thread for https://github.com/Tahjali11/Mythic-Edge/issues/14 and docs/contracts/parser_event_identity.md.

Compare src/mythic_edge_parser/app/event_identity.py, tests/test_event_identity.py, src/mythic_edge_parser/app/models.py, src/mythic_edge_parser/app/runtime_surfaces.py, and parser regression fixtures against the event identity contract. Produce docs/implementation_handoffs/parser_event_identity_comparison.md with confirmed matches, contract mismatches, missing tests, validation evidence, and a handoff to Module Reviewer.

Do not change parser behavior unless the comparison finds a clear contract mismatch or missing focused test required by the contract. Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports. Do not target main; module PR work belongs on codex/parser-module-audit-suite.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/14"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_event_identity.md"
  target_artifact: "docs/implementation_handoffs/parser_event_identity_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "documentation-only contract creation; no tests required in Module Contract Writer thread"
  stop_conditions:
    - "Stop and route back to Module Contract Writer if event identity classification precedence is ambiguous."
    - "Stop and route back to Thinker if comparison discovers scope outside issue #14."
    - "Do not move parser-owned classification truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI interpretation."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main until the parser module audit suite is complete."
```

## Handoff Packet

- Role performed: Module Contract Writer.
- Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/14
- Audit tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5
- Contract produced: `docs/contracts/parser_event_identity.md`
- Risk tier: High.
- Owning truth layer: parser and state interpretation.
- Public interface: `EventIdentity`, `EventIdentity.to_dict()`, and
  `classify_event_identity(event_id, super_format, match_win_condition)`.
- Invariants: output vocabulary remains explicit; unknown inputs degrade to
  unknown; `rank_eligible` equals rankedness; booleans reflect normalized
  string fields; downstream consumers do not own classification truth.
- Required tests: focused event identity tests, model history-item integration,
  runtime history filters, parser regression fixture checks, and ruff before
  submitter work.
- Acceptance criteria: contract exists, allowed values and fallbacks are
  documented, downstream consumers are named, and no prohibited behavior or
  downstream surface changes occur in this contract thread.
- Open questions or contract risks: competitive special-event rankedness,
  keyword ordering, MTGA event-name drift, and overloaded `event_family` naming.
- Next recommended thread role: Module Implementer (C).
