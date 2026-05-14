# Parser API Common Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/30

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Problem-representation docs read because issue #30 is the source problem
representation:

- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

Adjacent contracts:

- `docs/contracts/parser_client_actions.md`
- `docs/contracts/parser_gre_connect_resp.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_gre_turn_info.md`
- `docs/contracts/parser_match_state.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the shared parser helper behavior in
`src/mythic_edge_parser/parsers/api_common.py`. It is a contract artifact only.
It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/parsers/api_common.py`

The module provides shared parser utilities for:

- finding the first decodable JSON value inside noisy raw Player.log text
- returning dict-only JSON payloads for parser modules
- matching MTGA API request and response markers
- normalizing list-valued integer fields used by parser payload builders

Plain English: this module is the shared raw-text helper layer under multiple
parser modules. It does not decide event-specific meaning, emit events, mutate
parser state, post workbook rows, or reconcile match/game truth.

## Owning Layer

Parser and state interpretation.

`api_common.py` owns shared helper behavior for parser input handling:

- JSON candidate scanning
- first-decodable JSON precedence
- dict-only JSON parsing for parser entrypoints
- exact request and response API marker matching
- strict integer-list normalization

Parser truth boundary:

- `api_common.py` owns shared raw-body helper behavior.
- Individual parser modules own marker prefilters, event-specific raw payload
  shapes, emitted event classes, and parser-owned payload fields.
- Parser state owns live context, match/game interpretation, and final
  reconciliation after parser events exist.
- Extractors own downstream fallback reads from parser-produced payloads.
- Workbook formulas, dashboard logic, Apps Script, webhook transport, and
  AI-generated interpretation must not redefine JSON discovery, API marker
  matching, or integer-list normalization.

This contract must not align integer normalization semantics across modules.
Local helpers such as `gre/turn_info.py` and `gre/game_state.py` local
`_maybe_int()` intentionally have different observed behavior unless a future
problem representation and contract deliberately change that boundary.

## Files Owned By This Contract

- `src/mythic_edge_parser/parsers/api_common.py`
- `tests/test_api_common.py`
- `docs/contracts/parser_api_common.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_client_actions_parser.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `tests/test_match_state_parser.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/connect_resp.py`
- `tests/test_gre_connect_resp_parser.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_game_state_parser.py`
- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `tests/test_gre_turn_info_parser.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_error.py`
- `tests/test_connection_parsers.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `src/mythic_edge_parser/parsers/rank.py`
- `src/mythic_edge_parser/parsers/session.py`
- `tests/test_parsers.py`
- `tests/test_parser_regressions.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`

## Public Interface

### JSON Helpers

`find_json_value(text: str) -> Any | None`

Public shared parser helper.

Contract status:

- Scans raw text for candidate JSON starts at every `{` and `[` character.
- Tries candidates in ascending text-offset order.
- Uses `json.JSONDecoder.raw_decode(text[idx:])`.
- Returns the first successfully decoded JSON value.
- Returns `None` when no candidate successfully decodes.
- May return any JSON value type, including `dict`, `list`, `str`, `int`,
  `float`, `bool`, or `None`, but candidate scanning only begins at `{` and
  `[`.
- Does not require the decoded JSON value to consume the entire remaining
  string. Trailing log text after the decoded value is allowed.

`parse_json_from_body(body: str, context: str = "") -> dict[str, Any] | None`

Public shared parser helper.

Contract status:

- Calls `find_json_value(body)`.
- Returns the decoded value only when it is a `dict`.
- Returns `None` for no JSON, malformed JSON, or a first decodable JSON value
  that is not a dict.
- Does not continue scanning for a later dict after the first decodable value
  is a non-dict.
- Accepts `context` for compatibility, but the current implementation does not
  use it for logging, error text, matching, or returned values.

### API Marker Helpers

`is_api_request(body: str, name: str) -> bool`

Public shared parser helper.

Contract status:

- Searches the body for a request marker matching `==>\s*(?P<name>[A-Za-z0-9_]+)`.
- Returns `True` only when the first regex match captures exactly `name`.
- Returns `False` when no request marker matches or the captured name differs.

`is_api_response(body: str, name: str) -> bool`

Public shared parser helper.

Contract status:

- Searches the body for a response marker matching `<==\s*(?P<name>[A-Za-z0-9_]+)`.
- Returns `True` only when the first regex match captures exactly `name`.
- Returns `False` when no response marker matches or the captured name differs.

### Integer-List Helper

`normalize_int_list(value: Any) -> list[int]`

Public shared parser helper.

Contract status:

- Returns a new list of normalized integers from list input.
- Returns `[]` when `value` is not a list.
- Preserves order of accepted list members.
- Preserves duplicates.
- Accepts non-bool `int` values directly, including `0` and negative integers.
- Rejects booleans even though `bool` is an `int` subclass in Python.
- Accepts string values only after `.strip()` and only when
  `.isdigit()` is true.
- Converts accepted digit strings with `int(stripped)`.
- Skips common malformed values such as empty strings, non-digit strings,
  signed integer strings, decimal strings, floats, dicts, nested lists,
  booleans, and `None`.

### Implementation Details

The following names are implementation details. Their behavior is contract
covered through the public helpers, but other modules should not import them as
public API:

- `_API_REQ_RE`
- `_API_RESP_RE`
- `_JSON_DECODER`
- `_json_candidate_offsets(text)`
- `_api_name_match(body, pattern, expected_name)`
- `_normalized_int(value)`

## Inputs

### Raw Player.log Text

Type: `str`.

Sources:

- raw `LogEntry.body`
- nested stringified client-action payloads
- parser module bodies that contain Unity, API, connection, or GRE markers

Representative input:

```text
[UnityCrossThreadLogger]greToClientEvent
{"greToClientEvent":{"greToClientMessages":[]}} trailing text
```

### API Marker Bodies

Type: `str`.

Representative request input:

```text
==> GetPlayerInventory
{"requestId": 1}
```

Representative response input:

```text
<== StartHook
{"InventoryInfo": {}}
```

### Expected API Name

Type: `str`.

Examples:

- `StartHook`
- `RankGetCombinedRankInfo`
- `AuthenticateResponse`
- `authenticateResponse`
- `EventGetCourses`

The expected name is compared exactly against the captured marker name. It is
not stripped, lowercased, normalized, or otherwise transformed.

### List-Valued Integer Payload Fields

Type: `Any`; only list input is normalized.

Representative fields:

- GRE `systemSeatIds`
- GRE `diffDeletedInstanceIds`
- GRE `diffDeletedPersistentAnnotationIds`
- connect response `deckCards`
- connect response `sideboardCards`
- client action `selectedOptionIds`
- client action `selectedObjectIds`
- client action submit-deck card ID lists

## Outputs

### `find_json_value()`

Output type: `Any | None`.

Destinations:

- `parse_json_from_body()`
- `client_actions._extract_inner_payload()` for stringified payloads
- direct focused tests

Observed examples:

| Input | Output |
| --- | --- |
| `prefix {"a": 1} suffix` | `{"a": 1}` |
| `prefix [1, 2] suffix` | `[1, 2]` |
| `prefix {bad} {"a": 1}` | `{"a": 1}` |
| `no json here` | `None` |

### `parse_json_from_body()`

Output type: `dict[str, Any] | None`.

Destinations:

- parser entrypoints that need object payloads

Observed examples:

| Input | Output |
| --- | --- |
| `prefix {"a": 1} suffix` | `{"a": 1}` |
| `prefix [1, 2] {"a": 1}` | `None` |
| `prefix {bad} {"a": 1}` | `{"a": 1}` |
| `no json here` | `None` |

The second example is intentional observed behavior: once the first decodable
JSON value is a list, `parse_json_from_body()` returns `None` and does not look
for a later object.

### `is_api_request()` And `is_api_response()`

Output type: `bool`.

Destinations:

- collection, inventory, rank, and session parsers
- focused tests

Observed examples:

| Helper | Body | Name | Output |
| --- | --- | --- | --- |
| `is_api_request` | `==> GetPlayerInventory` | `GetPlayerInventory` | `True` |
| `is_api_request` | `==> GetPlayerInventory` | `GetPlayerCards` | `False` |
| `is_api_response` | `<== EventGetCourses` | `EventGetCourses` | `True` |
| `is_api_response` | `<== EventGetCourses` | `EventGetCourse` | `False` |

### `normalize_int_list()`

Output type: `list[int]`.

Destinations:

- parser payload fields that represent card IDs, seat IDs, option IDs, object
  IDs, and diff IDs

Observed examples:

| Input | Output |
| --- | --- |
| `[1, "2", " 3 ", True, False, "x", 4]` | `[1, 2, 3, 4]` |
| `[0, "010", -2, "-3", 4.5, "4.5"]` | `[0, 10, -2]` |
| `"1"` | `[]` |
| `(1, 2)` | `[]` |
| `None` | `[]` |

## JSON Discovery And Parsing Behavior

Observed current behavior:

- Candidate offsets are every position where the raw text character is `{` or
  `[`.
- Candidates are attempted from left to right.
- Each candidate uses `json.JSONDecoder.raw_decode()` on the substring starting
  at that offset.
- `json.JSONDecodeError` is swallowed and scanning continues to the next
  candidate.
- The first candidate that decodes wins, even if a later candidate would be
  more semantically relevant to a consuming parser.
- `raw_decode()` permits trailing non-JSON text after the decoded value.
- Arrays are valid results for `find_json_value()`.
- Arrays are not valid results for `parse_json_from_body()`.
- `parse_json_from_body()` is object-only and returns `None` for first
  decodable non-dict JSON values.
- `context` is accepted by `parse_json_from_body()` but unused.

Required guarantees:

- Preserve first-decodable JSON precedence unless a new contract deliberately
  changes parser-wide raw log parsing.
- Preserve dict-only behavior in `parse_json_from_body()`.
- Preserve `None` for no decodable JSON and for first decodable non-dict JSON.
- Preserve malformed-candidate skipping for earlier bad `{` or `[` characters.
- Preserve no logging and no exception propagation for ordinary
  `json.JSONDecodeError` candidates.
- Do not silently make `parse_json_from_body()` skip earlier arrays to find a
  later object without a new contract and consumer tests.

## API Marker Matching Behavior

Observed current behavior:

- Request marker regex: `==>\s*(?P<name>[A-Za-z0-9_]+)`.
- Response marker regex: `<==\s*(?P<name>[A-Za-z0-9_]+)`.
- Matching uses `re.Pattern.search()`, so the marker may appear anywhere in the
  body.
- `\s*` allows whitespace, including newlines, between the marker and captured
  API name.
- Captured API names may contain ASCII letters, ASCII digits, and underscores.
- Matching is case-sensitive.
- The expected name is compared exactly.
- Expected names are not stripped or normalized.
- Only the first regex match is considered.
- A later matching API name does not rescue a first mismatched marker.
- Names containing punctuation are partially captured up to the first
  unsupported character. For example, `==> Start-Hook` captures `Start`, not
  `Start-Hook`.

Required guarantees:

- Preserve exact captured-name comparison.
- Preserve case-sensitive matching.
- Preserve allowed captured characters as `[A-Za-z0-9_]` unless future MTGA
  payload drift requires a new contract.
- Preserve first-match behavior until a future contract deliberately changes
  marker scanning.
- Do not move API marker interpretation into workbook formulas, dashboard
  logic, Apps Script, webhook transport, or AI interpretation.

## Integer-List Normalization Behavior

Observed current behavior:

- Non-list input returns `[]`.
- Output is a new list.
- Accepted values keep their input order.
- Duplicates are preserved.
- Non-bool integers are accepted as-is:
  - `0` is valid.
  - negative integers are valid when they are already `int` objects.
- Booleans are rejected before integer handling.
- Strings are stripped first.
- Stripped strings are accepted only if `.isdigit()` is true.
- Accepted strings are converted with `int(stripped)`.
- Whitespace-padded digit strings are accepted.
- Leading-zero digit strings are accepted and converted normally.
- Signed integer strings such as `"-1"` and `"+1"` are rejected because they
  are not `.isdigit()`.
- Float objects and float-like strings are rejected.
- Dicts, nested lists, tuples, sets, objects, empty strings, and `None` are
  skipped.

Required guarantees:

- Preserve non-list fallback to `[]`.
- Preserve order and duplicates for accepted values.
- Preserve bool rejection.
- Preserve digit-string acceptance after whitespace stripping.
- Preserve signed-string rejection.
- Preserve float and object rejection.
- Preserve stricter behavior than parser-specific local `_maybe_int()` helpers
  unless a future contract explicitly aligns those semantics.

Relationship to local parser-specific numeric helpers:

- `api_common.normalize_int_list()` is intentionally stricter for list-valued
  IDs.
- `gre/turn_info.py` local `_maybe_int()` currently accepts booleans, floats,
  signed integer strings, and whitespace-padded integer strings through Python
  `int()` behavior.
- `gre/game_state.py` local `_maybe_int()` currently has the same permissive
  Python `int()` behavior for scalar fields such as `pending_message_count`,
  `prev_game_state_id`, and `identity.game_number`.
- Do not silently align these behaviors in either direction.

Unicode digit note:

- The implementation uses `str.isdigit()` and then `int(stripped)`.
- Some non-ASCII digit strings are accepted by Python `int()`.
- Some strings for which `.isdigit()` is true can still raise `ValueError` in
  `int(stripped)`.
- MTGA Player.log ID fields are expected to be ASCII numeric values. Non-ASCII
  digit behavior is not currently a required compatibility guarantee and is
  listed as an open risk below.

## Malformed Input Behavior

JSON helpers:

- No `{` or `[` candidate returns `None`.
- Malformed candidate JSON raises `json.JSONDecodeError` internally and is
  skipped.
- If all candidates fail to decode, `find_json_value()` returns `None`.
- If the first decodable JSON value is not a dict, `parse_json_from_body()`
  returns `None`.
- Non-string direct inputs are outside the public contract.

API marker helpers:

- Missing marker returns `False`.
- Marker with no `[A-Za-z0-9_]` name after optional whitespace returns `False`.
- First captured name mismatch returns `False`.
- Punctuation after an allowed-name prefix can produce a partial captured name.

Integer-list helper:

- Non-list source returns `[]`.
- Common malformed list members are skipped rather than preserved.
- Booleans are skipped.
- Rare non-ASCII digit strings for which `.isdigit()` is true but `int()`
  rejects may currently raise. This is a suspected gap, not a required
  behavior change in this contract.

Contract ambiguity about JSON precedence, marker matching, integer-list
normalization, or consumer ownership must route back to Codex B rather than
being implemented silently.

## Side Effects

The public helpers in `api_common.py` have no project side effects.

They must not:

- mutate input text or list objects
- emit parser events
- update parser runtime state
- post webhooks
- update workbook rows
- write local logs
- write runtime status files
- write failed-post queues
- write generated card data
- export workbook files
- log diagnostics as part of normal malformed-input handling

`normalize_int_list()` returns a new output list. It does not mutate the source
list or its members.

## Downstream Consumers

### JSON Discovery Consumers

`parse_json_from_body()` is used by:

- `parsers/gre/__init__.py`
- `parsers/match_state.py`
- `parsers/client_actions.py`
- `parsers/connection_state.py`
- `parsers/connection_close.py`
- `parsers/connection_error.py`
- `parsers/collection.py`
- `parsers/inventory.py`
- `parsers/rank.py`
- `parsers/session.py`

Compatibility expectations:

- These parsers can rely on dict-or-`None` behavior.
- These parsers own their event-specific marker checks and payload-shape
  validation after a dict is returned.
- `api_common.py` must not become the owner of GRE, match-state,
  client-action, rank, inventory, collection, connection, or session payload
  semantics.

### `find_json_value()` Direct Consumers

`client_actions._extract_inner_payload()` uses `find_json_value()` for
stringified inner payloads.

Compatibility expectations:

- Stringified JSON dict payloads remain supported.
- Stringified non-dict JSON values are returned by `find_json_value()` but are
  rejected by the client-action consumer because it requires a dict.
- Client-action semantics and raw payload preservation remain owned by
  `client_actions.py`.

### API Marker Consumers

API request/response helpers are used by:

- `collection.py`
- `inventory.py`
- `rank.py`
- `session.py`

Compatibility expectations:

- Marker helpers only answer whether the first regex-captured API name matches
  the expected name.
- Consumer modules own which method names they accept and how parsed response
  bodies become parser events.
- Session parser currently checks both `AuthenticateResponse` and
  `authenticateResponse`.

### Integer-List Consumers

`normalize_int_list()` is used by:

- `client_actions.py`
  - `selected_option_ids`
  - `selected_object_ids`
  - `deck_cards`
  - `sideboard_cards`
- `gre/connect_resp.py`
  - `system_seat_ids`
  - `deck_cards`
  - `sideboard_cards`
- `gre/game_state.py`
  - `system_seat_ids`
  - `diff_deleted_instance_ids`
  - `diff_deleted_persistent_annotation_ids`

Compatibility expectations:

- These parser payload fields must remain list-of-int outputs.
- Invalid list members are dropped, not preserved as diagnostics.
- Source order and duplicates remain meaningful and are preserved.
- Consumer modules own source-field precedence and raw payload preservation.

### State, Extractor, Runtime, And Workbook-Facing Consumers

Downstream app modules consume parser-produced event payloads after individual
parser modules have used `api_common.py`.

Compatibility expectations:

- State, extractors, transforms, runtime surfaces, gameplay actions, workbook
  exports, webhook transport, and Apps Script must not reimplement generic raw
  Player.log JSON discovery or API marker matching.
- Final reconciliation remains owned by state and models.
- Workbook row shape and webhook payload shape are not changed by this
  contract.

## Observed Current Behavior

- `find_json_value()` returns the first decodable JSON value at any `{` or `[`
  candidate.
- `find_json_value()` accepts JSON arrays as valid return values.
- `parse_json_from_body()` returns only dict values.
- `parse_json_from_body()` returns `None` for non-dict first decodable values.
- `parse_json_from_body()` accepts but does not use `context`.
- API marker helpers use regex `search()` and first-match exact comparison.
- Marker helper matching is case-sensitive.
- Marker captured names allow only ASCII letters, digits, and underscores.
- `normalize_int_list()` returns `[]` for non-list input.
- `normalize_int_list()` rejects booleans.
- `normalize_int_list()` accepts non-bool integers, including `0` and negative
  integers.
- `normalize_int_list()` accepts digit-only strings after whitespace stripping.
- `normalize_int_list()` rejects signed strings, float values, float-like
  strings, objects, nested containers, `None`, and common malformed strings.
- The helpers have no project side effects.

## Required Guarantees

- Keep all five public helper names and signatures stable:
  - `find_json_value(text: str) -> Any | None`
  - `parse_json_from_body(body: str, context: str = "") -> dict[str, Any] | None`
  - `is_api_request(body: str, name: str) -> bool`
  - `is_api_response(body: str, name: str) -> bool`
  - `normalize_int_list(value: Any) -> list[int]`
- Keep `api_common` exported through `mythic_edge_parser.parsers.__all__`.
- Keep JSON candidate scanning over `{` and `[`.
- Keep first-decodable JSON precedence.
- Keep `parse_json_from_body()` object-only.
- Keep `context` as a compatibility parameter with no behavioral effect.
- Keep exact, case-sensitive first API marker matching.
- Keep integer-list normalization strict and bool-safe.
- Keep current difference between shared list normalization and parser-specific
  scalar numeric helpers.
- Keep helpers pure and side-effect free.
- Keep parser-owned truth in parser/state layers.

## Unknowns

- Whether `context` should remain permanently unused or become diagnostic-only
  in a future contract.
- Whether `find_json_value()` should continue returning arrays as successful
  values when object-consuming parser entrypoints will reject them.
- Whether `parse_json_from_body()` should continue stopping at a first
  decodable non-dict value instead of scanning for a later dict.
- Whether API marker names should remain limited to `[A-Za-z0-9_]` if future
  MTGA API names contain punctuation.
- Whether first-marker behavior is sufficient for log bodies with multiple API
  markers.
- Whether non-ASCII digit strings should be accepted, rejected, or explicitly
  guarded against in `normalize_int_list()`.
- Whether negative integer objects should remain valid while negative integer
  strings are rejected.

## Suspected Gaps

- Focused tests do not appear to lock malformed candidate skipping before a
  later valid JSON object.
- Focused tests do not appear to lock first-decodable array behavior when a
  later object exists.
- Focused tests do not appear to lock `parse_json_from_body()` leaving
  `context` unused.
- Focused tests do not appear to lock first API marker behavior when multiple
  markers are present.
- Focused tests do not appear to lock punctuation partial-capture behavior.
- Focused tests do not appear to lock whitespace and newline behavior after
  API markers.
- Focused tests do not appear to lock case-sensitive matching directly.
- Focused tests do not appear to lock non-list containers returning `[]` from
  `normalize_int_list()`.
- Focused tests do not appear to lock negative integer objects being accepted
  while negative strings are rejected.
- Focused tests do not appear to lock duplicate preservation and output list
  independence.
- Non-ASCII digit strings can expose behavior not represented in current
  tests; some are accepted, while some `.isdigit()` strings can raise.

## Error Behavior

- Ordinary malformed JSON candidates must not escape as exceptions.
- No JSON or unsupported JSON shape returns `None` from JSON parser helpers.
- Missing or mismatched API markers return `False`.
- Non-list integer-list sources return `[]`.
- Common malformed integer-list members are skipped.
- Non-string direct inputs to JSON or marker helpers are outside the current
  public contract.
- Unicode digit behavior in `normalize_int_list()` is an open risk, not a
  required implementation change in this contract.
- If a consumer needs different JSON scanning, marker matching, or numeric
  behavior, route through a new problem representation and contract.

## Dependency Order

Implementation threads should evaluate changes in this order:

1. `src/mythic_edge_parser/parsers/api_common.py`
2. `tests/test_api_common.py`
3. `src/mythic_edge_parser/parsers/client_actions.py`, only if direct
   `find_json_value()` or integer-list consumers are implicated
4. `tests/test_client_actions_parser.py`
5. `src/mythic_edge_parser/parsers/gre/connect_resp.py`, only if integer-list
   consumers are implicated
6. `tests/test_gre_connect_resp_parser.py`
7. `src/mythic_edge_parser/parsers/gre/game_state.py`, only if integer-list
   consumers are implicated
8. `tests/test_gre_game_state_parser.py`
9. `src/mythic_edge_parser/parsers/gre/__init__.py`, only if GRE JSON parsing
   compatibility is implicated
10. `src/mythic_edge_parser/parsers/match_state.py`, only if match-state JSON
    parsing compatibility is implicated
11. connection, collection, inventory, rank, and session parsers, only if
    marker or JSON parsing compatibility is implicated
12. `tests/test_connection_parsers.py`, `tests/test_parsers.py`, and
    `tests/test_parser_regressions.py`

Do not start with parser state, workbook, webhook, Apps Script, dashboard, AI
analysis, or final reconciliation changes.

## Compatibility

Compatibility surfaces that must remain stable:

- `mythic_edge_parser.parsers.api_common` import path
- `api_common` export from `mythic_edge_parser.parsers`
- five public helper names and signatures
- first-decodable JSON behavior
- dict-only `parse_json_from_body()` behavior
- unused `context` parameter compatibility
- first regex marker match behavior
- exact, case-sensitive API name matching
- `[A-Za-z0-9_]` captured-name behavior
- `normalize_int_list()` bool rejection
- `normalize_int_list()` digit-string acceptance
- `normalize_int_list()` signed-string rejection
- `normalize_int_list()` order and duplicate preservation

Breaking changes that require a new problem representation or contract:

- renaming or removing any public helper
- changing `parse_json_from_body()` to return arrays or other non-dict JSON
  values
- changing JSON search to prefer later dicts over earlier arrays
- using `context` to change return values or matching behavior
- changing marker regex allowed characters
- changing marker matching from first-match to any-match
- making marker matching case-insensitive
- changing bool, signed-string, float, duplicate, or non-list behavior in
  `normalize_int_list()`
- broadly aligning `normalize_int_list()` with local parser-specific
  `_maybe_int()` helpers
- moving raw-log parsing truth downstream

## Validation Obligations

Documentation-only checks for this contract:

```bash
git diff --check
```

Focused validation expected for later implementation or review:

```bash
python3 -m pytest -q tests/test_api_common.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py
python3 -m ruff check src tests
```

Before submitter opens or updates a module PR, run or verify:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
```

If no behavior changes are needed, the implementation handoff should still
record why existing tests are sufficient or identify the exact missing contract
tests.

## Tests Required

Focused tests expected for Module Implementer or Module Fixer:

- JSON discovery:
  - first object after noisy prefix is returned
  - malformed candidates before a later valid object are skipped
  - first decodable array is returned by `find_json_value()`
  - first decodable array causes `parse_json_from_body()` to return `None`,
    even when a later object exists
  - trailing text after decoded JSON remains accepted
  - no JSON and all malformed candidates return `None`
- Dict-only parsing:
  - object values return dicts
  - arrays and other non-dict first decodable values return `None`
  - `context` does not change output
- API marker matching:
  - exact request and response names match
  - mismatched names return `False`
  - matching is case-sensitive
  - whitespace and newline after markers are allowed
  - only `[A-Za-z0-9_]` characters are captured
  - punctuation partial-capture behavior is locked or explicitly routed
  - first-match behavior is covered when multiple markers exist
- Integer-list normalization:
  - non-list values return `[]`
  - non-bool ints are accepted, including `0` and negative integer objects
  - booleans are rejected
  - digit strings with whitespace and leading zeros are accepted
  - signed strings, decimal strings, floats, objects, nested lists, empty
    strings, and `None` are skipped
  - order and duplicates are preserved
  - output list mutation does not mutate source list
  - Unicode digit behavior is either covered as current behavior or preserved
    as an explicit open risk
- Consumer compatibility:
  - client-action stringified inner payload parsing still works
  - client-action, connect-response, and game-state integer-list fields still
    normalize through shared helper behavior
  - GRE, match-state, connection, collection, inventory, rank, session, parser
    smoke, and regression tests continue to pass without downstream truth
    movement

## Acceptance Criteria

- The contract clearly names owned files and related consumer files.
- Public helper APIs are documented.
- JSON discovery and first-decodable precedence are documented.
- `parse_json_from_body()` object-only behavior and unused `context` parameter
  are documented.
- API request/response marker matching is documented, including first-match,
  exact-name, case-sensitive, and allowed-character behavior.
- Integer-list normalization is documented, including bool rejection,
  digit-string acceptance, signed-string rejection, non-list fallback, order,
  and duplicate preservation.
- Relationship to parser-specific numeric helpers is explicit.
- Malformed input and no-side-effect expectations are documented.
- Downstream consumers and ownership boundaries are documented without moving
  parser-owned truth downstream.
- Test obligations are specific enough for Codex C or Codex D to implement or
  verify.
- Protected surfaces remain unchanged.

## Next Workflow Action

Next role: Codex C, Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for #30 and docs/contracts/parser_api_common.md.

Goal:
Compare the current shared parser API utility implementation and focused tests against the parser API common contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/30
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_api_common.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_gre_connect_resp.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_gre_turn_info.md
- docs/contracts/parser_match_state.md
- src/mythic_edge_parser/parsers/api_common.py
- tests/test_api_common.py
- src/mythic_edge_parser/parsers/client_actions.py
- tests/test_client_actions_parser.py
- src/mythic_edge_parser/parsers/gre/connect_resp.py
- tests/test_gre_connect_resp_parser.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_game_state_parser.py
- src/mythic_edge_parser/parsers/gre/__init__.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/parsers/connection_state.py
- src/mythic_edge_parser/parsers/connection_close.py
- src/mythic_edge_parser/parsers/connection_error.py
- src/mythic_edge_parser/parsers/collection.py
- src/mythic_edge_parser/parsers/inventory.py
- src/mythic_edge_parser/parsers/rank.py
- src/mythic_edge_parser/parsers/session.py
- tests/test_connection_parsers.py
- tests/test_parsers.py
- tests/test_parser_regressions.py

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned shared helper truth boundaries.
- Add focused tests for contracted api_common behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a consumer compatibility update.
- Preserve the documented distinction between api_common.normalize_int_list() and parser-specific local numeric helpers.
- Produce docs/implementation_handoffs/parser_api_common_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior unless required by the contract and covered by focused tests.
- Broadly align integer normalization semantics across parser modules unless routed through a new explicit contract.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned raw-log parsing truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/30"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_api_common.md"
  target_artifact: "docs/implementation_handoffs/parser_api_common_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior unless required by the contract and covered by focused tests."
    - "Do not broadly align integer normalization semantics across parser modules unless routed through a new explicit contract."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned raw-log parsing truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not target main for module PR work."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Source problem representation: GitHub issue #30, tracked by parser module
audit tracker #5.

Contract produced: `docs/contracts/parser_api_common.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/5

Risk tier: High.

Owning truth layer: parser and state interpretation.

Public interface:

- `find_json_value(text: str) -> Any | None`
- `parse_json_from_body(body: str, context: str = "") -> dict[str, Any] | None`
- `is_api_request(body: str, name: str) -> bool`
- `is_api_response(body: str, name: str) -> bool`
- `normalize_int_list(value: Any) -> list[int]`

Invariants:

- JSON scanning attempts `{` and `[` candidates from left to right.
- The first decodable JSON value wins.
- `parse_json_from_body()` returns only dicts or `None`.
- `context` remains behavior-neutral.
- API marker matching uses exact, case-sensitive, first regex match behavior.
- `normalize_int_list()` returns `[]` for non-list input.
- `normalize_int_list()` rejects bools, accepts non-bool ints, accepts
  stripped digit strings, preserves order and duplicates, and skips common
  malformed members.
- Shared list normalization remains distinct from parser-specific scalar
  numeric helpers.
- Helpers have no project side effects.

Required tests: focused JSON discovery, dict-only parsing, context neutrality,
marker matching, integer-list normalization, consumer compatibility, and
downstream no-truth-movement obligations listed in `Tests Required`.

Acceptance criteria: listed above.

Open questions or contract risks:

- `context` is currently unused.
- First-decodable array behavior can block a later object in
  `parse_json_from_body()`.
- Marker matching considers only the first regex match.
- Punctuation in API names is not supported beyond partial capture.
- Non-ASCII digit strings can expose behavior not currently covered by tests.
- Negative integer objects are accepted while negative integer strings are
  rejected.

Next recommended thread role: Codex C, Module Implementer.
