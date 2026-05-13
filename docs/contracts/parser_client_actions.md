# Parser Client Actions Module Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/20

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Adjacent contracts:

- `docs/contracts/parser_state.md`
- `docs/contracts/parser_extractors.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the parser-owned client-action parser in
`src/mythic_edge_parser/parsers/client_actions.py`. It is a contract artifact
only. It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/parsers/client_actions.py`

The module recognizes raw MTGA `ClientToGREMessage` and
`ClientToGREUIMessage` log bodies and normalizes them into `ClientActionEvent`
payloads.

## Owning Layer

Parser and state interpretation.

`client_actions.py` owns raw client-to-GRE marker recognition, channel
classification, inner client payload extraction, normalized client-action
payload fields, specialized client-action payload builders, and preservation of
raw client-action envelopes for downstream parser consumers.

It does not own live match/game summary mutation, mulligan count state,
submit-deck row deduplication, starting-player reconciliation, local team
correction, workbook row shape, webhook transport, Apps Script behavior,
dashboard interpretation, match/game identity, deduplication, or final
reconciliation.

Parser truth boundary:

- `client_actions.py` owns conversion from raw MTGA client-action log entry to
  `ClientActionEvent.payload`.
- `src/mythic_edge_parser/app/state.py` owns applying client-action facts to
  live `MatchSummary` / `GameSummary` state.
- `src/mythic_edge_parser/app/transforms.py` owns turning parser events into
  raw sheet rows and dedupe gates.
- `src/mythic_edge_parser/app/extractors.py` owns fallback extraction from
  preserved raw payloads.
- Runtime surfaces, analytics sidecar, diagnostics, GRP candidate tooling,
  workbook formulas, webhook transport, Apps Script, dashboard logic, and AI
  analysis must consume parser-produced client-action facts rather than parse
  raw MTGA client-action logs as their own source of truth.

## Files Owned By This Contract

- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_client_actions_parser.py`
- `docs/contracts/parser_client_actions.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `src/mythic_edge_parser/app/config.py`
- `tests/test_parsers.py`
- `tests/test_router_unit.py`
- `tests/test_state.py`
- `tests/test_transforms.py`
- `tests/test_app_extractors.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_grp_id_candidates.py`
- `tests/test_parser_regressions.py`

## Public Interface

### Constants

`CLIENT_TO_GRE_MARKER`

- Value: `"ClientToGREMessage"`.
- Contract status: public parser marker for non-UI client-to-GRE messages.

`CLIENT_TO_GRE_UI_MARKER`

- Value: `"ClientToGREUIMessage"`.
- Contract status: public parser marker for client-to-GRE UI messages.

`MULLIGAN_DECISION_MAP`

- Maps `MulliganOption_Mulligan` to `mulligan`.
- Maps `MulliganOption_AcceptHand` to `keep`.
- Contract status: parser normalization map for known mulligan decisions.

### Function

`try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None`

- Public parser entrypoint.
- Returns a `ClientActionEvent` for recognized, parseable client-action log
  entries.
- Returns `None` for non-client-action entries, unparseable JSON, unsupported
  non-UI payload shapes, or malformed GRE inner payloads that cannot become a
  dict.

Underscored helpers and `_CLIENT_ACTION_PAYLOAD_BUILDERS` are implementation
details. Their behavior is contract-covered through `try_parse()`, but callers
should not import them as public API.

### Event Type

Successful parses emit `ClientActionEvent` from
`src/mythic_edge_parser/events.py`.

Observed event properties:

- `kind == "ClientAction"`.
- `performance_class == PerformanceClass.INTERACTIVE_DISPATCH`.
- `metadata.timestamp` is the timestamp passed to `try_parse()`.
- `metadata.raw_bytes` is `entry.body.encode()`.
- `metadata.raw_bytes_hash` is derived from the raw bytes by `EventMetadata`.

## Inputs

### Raw Log Input

| Input | Type | Source | Required |
| --- | --- | --- | --- |
| `entry.body` | `str` | MTGA log `LogEntry` | Yes |
| `timestamp` | `datetime | None` | router timestamp extraction | No |

Current marker classification is substring-based over the entire raw body:

- If `CLIENT_TO_GRE_UI_MARKER` appears anywhere in the body, the message
  channel is `ui`.
- Else, if `CLIENT_TO_GRE_MARKER` appears anywhere in the body, the message
  channel is `gre`.
- Else, the entry is not a client-action candidate.

Observed implication:

- Marker detection can succeed because the JSON field
  `clientToMatchServiceMessageType` contains
  `ClientToMatchServiceMessageType_ClientToGREMessage` or
  `ClientToMatchServiceMessageType_ClientToGREUIMessage`, even when the log
  prefix casing differs.

Required guarantee:

- Do not narrow marker recognition to only the log prefix, only parsed JSON, or
  only one casing without a new contract and compatibility tests.

### JSON Envelope Input

`api_common.parse_json_from_body()` extracts the first dict JSON value from the
raw body. This module does not own generic JSON scanning, but it depends on the
current behavior that non-dict JSON values produce `None`.

Common envelope fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `requestId` | object/int | Client request identifier. |
| `clientToMatchServiceMessageType` | object/string | Raw MTGA client message channel enum. |
| `payload` | dict or stringified JSON dict | Inner client-action payload for GRE messages. |

UI messages do not require a valid inner payload; the whole parsed envelope is
preserved.

GRE messages require an inner payload dict, either directly as
`envelope["payload"]` or parsed from stringified JSON stored in that field.

### Recognized Inner GRE Payload Fields

| Field | Type | Meaning |
| --- | --- | --- |
| `type` | object/string | Raw MTGA client message type. |
| `gameStateId` | object/int | Request context game-state ID. |
| `respId` | object/int | Request context response ID. |
| `mulliganResp` | dict | Mulligan response body. |
| `selectNResp` | dict | Select-N response body. |
| `submitDeckResp` | dict | Submit-deck response body. |

## Outputs

### Non-Parse Output

`try_parse()` returns `None` when:

- neither client-action marker appears in `entry.body`
- marker detection succeeds but no dict JSON envelope can be parsed
- the message channel is `gre` and `payload` is missing
- the message channel is `gre` and `payload` is neither a dict nor a string
  containing a dict JSON value
- the message channel is `gre` and stringified `payload` contains no parseable
  dict

### UI Message Output

For channel `ui`, successful payloads have this shape:

| Field | Type | Meaning |
| --- | --- | --- |
| `type` | `str` | Always `client_ui_message`. |
| `raw_client_action` | `dict` | Parsed JSON envelope. |

Observed behavior:

- UI messages are emitted whenever the UI marker is present and the raw body
  contains a parseable dict JSON envelope.
- UI messages do not normalize request context fields.
- UI messages do not require or inspect `envelope["payload"]`.
- The raw envelope is preserved under `raw_client_action`.

Required guarantees:

- UI messages must remain distinguishable from GRE messages by
  `type == "client_ui_message"`.
- UI raw payload preservation must remain available for diagnostics and future
  parser consumers.
- Filtering high-volume UI message subtypes is out of scope for this contract.

### Generic GRE Client Action Output

For unrecognized inner `type` values, successful payloads have this shape:

| Field | Type | Meaning |
| --- | --- | --- |
| `type` | `str` | Always `generic_client_action`. |
| `message_type` | `str` | Trimmed string form of `inner["type"]`, or `""`. |
| `raw_client_action` | `dict` | Parsed JSON envelope. |

Observed behavior:

- Unknown, missing, blank, or future inner message types are emitted as
  `generic_client_action` when the inner payload is a dict.
- Generic payloads preserve the original envelope under `raw_client_action`.
- Generic payloads do not currently include normalized `game_state_id`,
  `resp_id`, or `request_id` fields.
- If the inner payload was stringified JSON, `raw_client_action["payload"]`
  remains the original stringified payload because the envelope is preserved.

Required guarantees:

- Generic fallback must not discard future MTGA client message types that have
  a valid inner dict payload.
- Generic fallback must preserve `message_type` so state and transforms can
  consume `ClientMessageType_ChooseStartingPlayerResp`,
  `ClientMessageType_EnterSideboardingReq`,
  `ClientMessageType_SubmitDeckResp`, and
  `ClientMessageType_MulliganResp` compatibility paths.
- Generic fallback must preserve `raw_client_action` because extractor helpers
  read nested starting-player and local-team fields from it.

### Specialized GRE Payload Outputs

Specialized builders emit normalized payloads for currently supported message
types.

All specialized payloads include request context:

| Field | Source | Missing default |
| --- | --- | --- |
| `game_state_id` | `inner.gameStateId` | `0` |
| `resp_id` | `inner.respId` | `0` |
| `request_id` | `envelope.requestId` | `0` |
| `raw_client_action` | parsed envelope | envelope dict |

The request context values are copied as-is from source fields when present.
They are not integer-normalized by this parser.

#### Mulligan Response

Recognized when `inner["type"] == "ClientMessageType_MulliganResp"`.

Payload fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `type` | `str` | Always `mulligan_resp`. |
| `decision` | object/string | Normalized or raw mulligan decision. |
| `game_state_id` | object/int | Request context. |
| `resp_id` | object/int | Request context. |
| `request_id` | object/int | Request context. |
| `raw_client_action` | `dict` | Parsed envelope. |

Decision normalization:

- `MulliganOption_Mulligan` becomes `mulligan`.
- `MulliganOption_AcceptHand` becomes `keep`.
- Unknown truthy values pass through unchanged.
- Missing, malformed, or falsey decision values become `""`.

Observed behavior:

- Malformed or missing `mulliganResp` normalizes to `decision == ""`.
- The raw decision string is not preserved in a separate field.

Required guarantees:

- Known mulligan decision normalization must remain stable because `state.py`
  uses `keep` to avoid incrementing mulligan counts and treats non-keep
  decisions as mulligans.
- Unknown decision values must remain explicit rather than being coerced to
  `keep`.

#### Select-N Response

Recognized when `inner["type"] == "ClientMessageType_SelectNResp"`.

Payload fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `type` | `str` | Always `select_n_resp`. |
| `selected_option_ids` | `list[int]` | Normalized selected option IDs. |
| `selected_object_ids` | `list[int]` | Normalized selected object IDs. |
| `game_state_id` | object/int | Request context. |
| `resp_id` | object/int | Request context. |
| `request_id` | object/int | Request context. |
| `raw_client_action` | `dict` | Parsed envelope. |

Integer list normalization is delegated to `api_common.normalize_int_list()`:

- non-list containers normalize to `[]`
- `int` values are kept, except booleans are rejected
- digit-only strings after trimming become integers
- malformed strings, negative strings, floats, booleans, dicts, lists, and
  `None` entries are skipped
- valid order is preserved

Observed behavior:

- Missing or malformed `selectNResp` normalizes both selected ID lists to `[]`.

Required guarantees:

- Malformed selected IDs must not leak into parser-owned selected ID lists.
- The parser currently drops malformed selected IDs rather than preserving them
  for diagnostics.

#### Submit Deck Response

Recognized when `inner["type"] == "ClientMessageType_SubmitDeckResp"`.

Payload fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `type` | `str` | Always `submit_deck_resp`. |
| `deck_cards` | `list[int]` | Normalized submitted main-deck card IDs. |
| `sideboard_cards` | `list[int]` | Normalized submitted sideboard card IDs. |
| `game_state_id` | object/int | Request context. |
| `resp_id` | object/int | Request context. |
| `request_id` | object/int | Request context. |
| `raw_client_action` | `dict` | Parsed envelope. |

Deck list source precedence:

Main deck:

1. `submitDeckResp.deckCards`
2. `submitDeckResp.deck.deckCards`
3. `submitDeckResp.deck`
4. `[]`

Sideboard:

1. `submitDeckResp.sideboardCards`
2. `submitDeckResp.deck.sideboardCards`
3. `submitDeckResp.sideboard`
4. `[]`

Observed behavior:

- Source selection uses Python truthiness. An empty direct list can fall
  through to a later source. A truthy malformed direct source can be selected
  and then normalize to `[]`.
- Missing or malformed `submitDeckResp` normalizes both lists to `[]`.
- If `submitDeckResp.deck` is a dict, nested deck fields can be read.
- If `submitDeckResp.deck` is a list, it can be used as the main-deck card
  list when higher-priority deck-card sources are falsey.
- Normalization uses `api_common.normalize_int_list()`.

Required guarantees:

- Direct `deckCards` / `sideboardCards` and nested
  `deck.deckCards` / `deck.sideboardCards` must remain supported.
- Deck-list output field names must remain `deck_cards` and
  `sideboard_cards` because runtime surfaces, diagnostics, GRP candidate tools,
  and tests consume them.
- The parser must not infer match ID, game number, deck name, collection
  ownership, or workbook row shape from submit-deck payloads.

## Raw Payload Preservation

`raw_client_action` is the parsed JSON envelope, not only the inner payload.

Required guarantees:

- UI, generic, and specialized outputs must preserve `raw_client_action`.
- Downstream extractors must be able to inspect
  `raw_client_action.payload`, including nested `chooseStartingPlayerResp`,
  `mulliganResp`, and `submitDeckResp`.
- If `payload` was stringified JSON in the raw envelope, raw preservation keeps
  that original string under `raw_client_action["payload"]`.
- Callers must treat `raw_client_action` as read-only. Event payload copying is
  shallow, so this contract does not guarantee deep-copy isolation of nested
  raw objects.

## Observed Behavior

- UI marker wins over GRE marker because channel classification checks the UI
  marker first.
- Marker matching is case-sensitive and substring-based over the whole body.
- JSON parsing accepts the first dict JSON value in the raw body.
- GRE inner payload accepts dict payloads and stringified JSON dict payloads.
- Unknown GRE inner message types become `generic_client_action`.
- Supported specialized message types are:
  `ClientMessageType_MulliganResp`, `ClientMessageType_SelectNResp`, and
  `ClientMessageType_SubmitDeckResp`.
- Specialized payloads include request context; generic and UI payloads do not.
- No workbook rows, runtime state, status files, failed posts, or generated
  data are written by this parser.

## Required Guarantees

- Keep `try_parse()` side-effect free.
- Keep `ClientActionEvent.payload` field names stable unless a future contract
  updates all consumers.
- Do not discard unknown but well-formed GRE client actions.
- Do not remove `raw_client_action`.
- Do not move client-action parsing truth into state, transforms, extractors,
  workbook formulas, dashboard logic, Apps Script, webhook transport, or AI
  interpretation.
- Do not change parser event classes, parser state, workbook schema, webhook
  payload shape, Apps Script behavior, match/game identity, final
  reconciliation, deduplication, secrets, raw logs, generated data, runtime
  status files, failed posts, or workbook exports from this module.

## Downstream Consumers

Observed consumers:

- `router.py`
  - dispatches `client_actions` after `gre` for Unity and unknown-header log
    entries.
  - wraps a successful `ClientActionEvent` in a list.
- `events.py`
  - defines `ClientActionEvent` kind and performance class.
- `state.py`
  - ignores `ClientAction` when no current match ID exists.
  - uses `mulligan_resp` and generic `ClientMessageType_MulliganResp` for
    mulligan counts.
  - uses `submit_deck_resp` and generic `ClientMessageType_SubmitDeckResp` for
    `submit_deck_seen`.
  - uses generic `ClientMessageType_ChooseStartingPlayerResp` for starting
    player.
  - uses generic `ClientMessageType_EnterSideboardingReq` for sideboarding.
  - uses extractor helpers to correct local team from raw payloads.
- `transforms.py`
  - includes `mulligan_resp`, `submit_deck_resp`, and selected generic message
    types in raw row output.
  - uses request and context information only downstream; this parser does not
    own row dedupe.
- `extractors.py`
  - reads top-level client-action fields and nested
    `raw_client_action.payload` fields for starting player and local team.
- `runtime_surfaces.py`, `runner.py`, `diagnostics.py`,
  `analytics_sidecar.py`, and `grp_id_candidates.py`
  - consume `submit_deck_resp`, `deck_cards`, `sideboard_cards`,
    `game_state_id`, `resp_id`, `request_id`, and raw fallback payloads for
    runtime deck profiles, submitted-deck recording, status exports, and GRP
    candidate workflows.

These consumers do not own raw client-to-GRE parsing.

## Invariants

- `try_parse()` returns either `None` or a `ClientActionEvent`.
- Every successful event has `kind == "ClientAction"`.
- Every successful event preserves the encoded raw body in metadata.
- Every successful payload includes a top-level `type`.
- Every successful payload includes `raw_client_action`.
- UI payload type is `client_ui_message`.
- Generic payload type is `generic_client_action`.
- Specialized payload types are `mulligan_resp`, `select_n_resp`, and
  `submit_deck_resp`.
- Specialized payloads include `game_state_id`, `resp_id`, and `request_id`.
- `selected_option_ids`, `selected_object_ids`, `deck_cards`, and
  `sideboard_cards` are always lists when their payload type is emitted.
- Specialized selected-ID and card-list outputs contain only integers.
- The parser does not mutate runtime state or submit rows.

## Unknowns

- Whether future MTGA logs will keep the same marker strings or casing.
- Whether marker matching should eventually depend on parsed
  `clientToMatchServiceMessageType` instead of substring detection.
- Whether high-volume UI message subtypes should remain emitted or be filtered
  before downstream surfaces.
- Whether `generic_client_action` should eventually include request context
  fields.
- Whether `mulligan_resp` should preserve the raw decision value separately
  from normalized `decision`.
- Whether malformed selected IDs should be preserved for diagnostics instead
  of dropped.
- Whether additional submit-deck shapes exist beyond direct deck/sideboard
  lists, nested `deck` dicts, and list-valued `deck` / `sideboard` fallbacks.

## Suspected Gaps

- Focused tests do not yet directly assert `ClientActionEvent` metadata raw
  bytes, timestamp, or performance class.
- Focused tests do not yet directly cover marker detection from the JSON enum
  when log-prefix casing differs as an explicit contract rule.
- Focused tests do not yet cover marker-present invalid JSON returning `None`.
- Focused tests do not yet cover parsed non-dict JSON returning `None`.
- Focused tests do not yet cover GRE payload missing, non-dict, invalid
  stringified, or stringified non-dict payload returning `None`.
- Focused tests do not yet cover generic fallback with missing or blank
  `type`.
- Focused tests do not yet assert that generic fallback preserves a stringified
  raw `payload` under `raw_client_action`.
- Focused tests do not yet cover all request-context defaults on each
  specialized payload.
- Focused tests do not yet cover unknown mulligan decision pass-through and
  malformed mulligan payload fallback.
- Focused tests do not yet cover `MulliganOption_Mulligan` mapping to
  `mulligan`.
- Focused tests do not yet cover boolean, malformed string, negative string,
  float, dict, or nested-list rejection in selected ID lists and deck lists.
- Focused tests do not yet cover direct submit-deck source precedence versus
  nested fallback and list-valued `deck` / `sideboard` fallback.

## Error Behavior

- Non-client-action bodies return `None`.
- Candidate bodies with no parseable dict JSON return `None`.
- UI candidates with a parseable dict envelope emit `client_ui_message`, even
  if the envelope payload is missing or malformed.
- GRE candidates with no dict inner payload return `None`.
- Unknown GRE inner message types emit `generic_client_action`.
- Malformed specialized nested payloads emit neutral default fields rather than
  raising.
- Malformed selected ID and card-list entries are dropped.
- Missing request context fields default to `0` for specialized payloads.

## Side Effects

None.

This module must not mutate parser runtime state, write files, post webhooks,
update workbook tabs, refresh status files, alter failed-post queues, modify
generated data, or change environment/secrets.

## Dependency Order

For future implementation work, inspect and update in this order:

1. `docs/contracts/parser_client_actions.md`
2. `src/mythic_edge_parser/parsers/client_actions.py`
3. `tests/test_client_actions_parser.py`
4. `tests/test_parsers.py`
5. `tests/test_router_unit.py`
6. `src/mythic_edge_parser/events.py`, only if event class behavior is in
   scope under a new contract
7. `src/mythic_edge_parser/app/state.py`, only if downstream state behavior is
   explicitly in scope under a new/revised contract
8. `src/mythic_edge_parser/app/transforms.py`,
   `src/mythic_edge_parser/app/extractors.py`, runtime surfaces, analytics, and
   diagnostics only if the client-action payload contract changes
9. Adjacent contracts if public payload fields or ownership boundaries change

## Compatibility

Must remain compatible with:

- marker substring detection for `ClientToGREMessage` and
  `ClientToGREUIMessage`
- UI channel priority
- dict and stringified JSON inner GRE payload shapes
- payload type strings:
  - `client_ui_message`
  - `generic_client_action`
  - `mulligan_resp`
  - `select_n_resp`
  - `submit_deck_resp`
- generic `message_type`
- request context field names: `game_state_id`, `resp_id`, `request_id`
- raw envelope preservation under `raw_client_action`
- mulligan normalized values `mulligan` and `keep`
- selected ID list fields: `selected_option_ids`, `selected_object_ids`
- submit-deck list fields: `deck_cards`, `sideboard_cards`
- existing downstream generic message handling for
  `ClientMessageType_ChooseStartingPlayerResp`,
  `ClientMessageType_EnterSideboardingReq`,
  `ClientMessageType_SubmitDeckResp`, and
  `ClientMessageType_MulliganResp`

Changing any of these compatibility surfaces requires a revised contract and
focused downstream tests.

## Tests Required

Focused parser tests should cover:

- UI message payload shape and raw payload preservation.
- Generic message fallback and `message_type`.
- Mulligan response decision normalization for keep and mulligan.
- Unknown mulligan decision pass-through.
- Malformed/missing `mulliganResp` fallback to `decision == ""`.
- Select-N response normalization and malformed selected ID filtering.
- Submit-deck response extraction from direct `deckCards` /
  `sideboardCards`.
- Submit-deck response extraction from nested `deck.deckCards` /
  `deck.sideboardCards`.
- Submit-deck response extraction from list-valued `deck` and `sideboard`
  fallbacks.
- Malformed submit-deck nested shapes returning empty lists.
- Stringified inner payload support.
- Stringified inner payload invalid/non-dict fallback to `None`.
- Marker-present invalid JSON returning `None`.
- Parsed non-dict JSON returning `None`.
- Missing/non-dict GRE inner payload returning `None`.
- Entries without a client marker returning `None`.
- Specialized request context fields and defaults.
- Metadata timestamp, raw bytes, and `ClientActionEvent` performance class.
- UI channel priority when both markers appear.
- Raw envelope preservation for UI, generic, and specialized payloads.

Related consumer tests should continue to cover:

- Router dispatch order with `client_actions` after `gre`.
- State handling for mulligan, submit deck, sideboarding, starting player, and
  local team extraction.
- Transform row inclusion/dedupe for kept client-action types.
- Extractor raw payload fallback for starting player and local team.
- Runtime submitted deck surfaces and diagnostics.
- GRP candidate submitted-deck and mulligan consumers.
- Parser regression coverage for saved event payload compatibility.

Recommended validation commands:

```bash
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py tests/test_router_unit.py
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_app_extractors.py tests/test_runtime_surfaces.py
python3 -m pytest -q tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m ruff check src tests
```

Before submitter work:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
```

Documentation-only contract edits may use:

```bash
git diff --check
```

## Acceptance Criteria

- The contract names `client_actions.py` as owner of client-action log parsing
  and normalized `ClientActionEvent` payloads.
- Public API, markers, channel behavior, accepted payload shapes, and payload
  type strings are explicit.
- UI, generic, mulligan, select-N, and submit-deck behavior are explicit.
- Request context fields and defaults are explicit.
- Normalization rules for mulligan decisions, selected IDs, and deck lists are
  explicit.
- Malformed input behavior is explicit.
- Raw payload preservation requirements are explicit.
- Downstream consumers and ownership boundaries are listed.
- Compatibility expectations and test obligations are concrete enough for
  Module Implementer and Module Reviewer to verify.
- No parser behavior, parser state, workbook schema, webhook payload shape, App
  Script behavior, parser event classes, match/game identity, final
  reconciliation, deduplication, secrets, raw logs, generated data, runtime
  status files, failed posts, or workbook exports are changed by this contract
  thread.

## Next Workflow Action

Next role: Module Implementer (Codex C)

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for issue #20 and docs/contracts/parser_client_actions.md.

Goal:
Compare the current client-actions parser implementation and focused tests against the parser client-actions module contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/20
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_client_actions.md
- src/mythic_edge_parser/parsers/client_actions.py
- tests/test_client_actions_parser.py
- tests/test_parsers.py
- tests/test_router_unit.py
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/analytics_sidecar.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- docs/contracts/parser_state.md
- docs/contracts/parser_extractors.md

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned truth boundaries.
- Add focused tests for contracted parser behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a downstream update.
- Produce docs/implementation_handoffs/parser_client_actions_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser state, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, final reconciliation, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned client-action truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/20"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_client_actions.md"
  target_artifact: "docs/implementation_handoffs/parser_client_actions_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser state, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, final reconciliation, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned client-action truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not target main for module PR work."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Source problem representation: GitHub issue #20, tracked by parser module audit
tracker #5.

Contract produced: `docs/contracts/parser_client_actions.md`

Risk tier: High.

Owning truth layer: parser and state interpretation.

Public interface:

- `CLIENT_TO_GRE_MARKER`
- `CLIENT_TO_GRE_UI_MARKER`
- `MULLIGAN_DECISION_MAP`
- `try_parse(entry, timestamp)`
- `ClientActionEvent.payload` fields documented above

Key invariants:

- Successful parses emit `ClientActionEvent`.
- UI/generic/specialized payload types remain stable.
- Raw client-action envelope preservation remains available.
- Specialized payloads include request context.
- Client-action parser has no side effects.

Required tests: focused parser and related consumer obligations listed in
`Tests Required`.

Acceptance criteria: listed above.

Open questions or contract risks:

- Marker detection is currently substring-based over the whole body.
- Generic payloads do not currently include request context.
- Raw mulligan decision is not preserved separately from normalized decision.
- Malformed selected IDs are dropped rather than preserved for diagnostics.
- Additional future MTGA submit-deck shapes may require a revised contract.

Next recommended thread role: Codex C, Module Implementer.
