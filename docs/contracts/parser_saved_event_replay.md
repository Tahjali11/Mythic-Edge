# Parser Saved Event Replay Module Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/54

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Base branch: `codex/parser-module-audit-suite`

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Adjacent contracts and reports:

- `docs/contracts/parser_runner.md`
- `docs/contracts/parser_outputs.md`
- `docs/contracts/parser_sheet_exports.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_event_lifecycle.md`
- `docs/implementation_handoffs/parser_state_comparison.md`
- `docs/contract_test_reports/parser_state.md`
- `docs/implementation_handoffs/parser_event_lifecycle_comparison.md`
- `docs/contract_test_reports/parser_event_lifecycle.md`

This is a contract artifact only. It does not implement behavior changes, open
a pull request, target `main`, or mark tracker #5 complete.

## Module

`src/mythic_edge_parser/app/saved_event_replay.py`

The module provides a local utility for replaying saved parser-event JSONL
archives. It finds selected JSONL files, reconstructs supported typed parser
event objects from saved records, skips duplicate raw event hashes during a
replay run, invokes a caller-supplied callback for reconstructed events, and
returns simple replay counters.

Plain English: this module reads generated parser evidence and turns supported
saved records back into event objects. It does not parse raw MTGA `Player.log`
text, decide match or game truth, post workbook rows, update Apps Script, or
repair downstream data.

## Owning Layer

Parser and state interpretation support / local replay QA.

Truth boundaries:

- MTGA `Player.log` remains the ultimate observable raw evidence source.
- Saved JSONL archives are generated parser evidence derived from earlier
  parser events.
- `app/transforms.py` owns the saved record shape produced by
  `to_serializable(event)`.
- `app/outputs.py` owns archive file writing through `append_local_jsonl()`.
- `app/runner.py` owns live orchestration of event filtering, serialization,
  archive writing, state updates, row building, and webhook submission.
- `events.py` owns parser event classes, event `kind` strings, metadata raw
  hash calculation, and performance classes.
- `state.py` owns parser-state interpretation when a caller passes replayed
  events into `_update_match_summary()` or any future state ingestion path.
- `saved_event_replay.py` owns only local archive selection, saved-record
  reconstruction for supported kinds, replay-local raw-hash dedupe, callback
  ordering, and replay stats.
- Workbook formulas, dashboard logic, Apps Script, webhook delivery, and
  AI-generated interpretation must not become parser truth through replay work.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/saved_event_replay.py`
- `tests/test_saved_event_replay.py`
- `docs/contracts/parser_saved_event_replay.md`

Related files referenced but not owned by this contract:

- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_parser_regressions.py`
- `tests/test_state.py`
- `tests/test_match_summary_from_match_state.py`

## Public Interfaces

### `ReplayStats`

Slotted dataclass returned by `replay_latest_saved_events()`.

Fields:

- `files_processed: int = 0`
- `events_processed: int = 0`
- `events_skipped: int = 0`

The stats object is returned only after a replay call completes without an
uncaught exception.

### `EVENT_CLASS_BY_KIND`

Mapping from saved record `kind` strings to event classes used by
`event_from_saved_record()`.

Observed supported kinds:

| Saved `kind` | Event class |
| --- | --- |
| `ClientAction` | `ClientActionEvent` |
| `DetailedLoggingStatus` | `DetailedLoggingStatusEvent` |
| `EventLifecycle` | `EventLifecycleEvent` |
| `GameResult` | `GameResultEvent` |
| `GameState` | `GameStateEvent` |
| `MatchState` | `MatchStateEvent` |
| `Rank` | `RankEvent` |

The lookup is exact and case-sensitive. Unknown, missing, differently cased, or
whitespace-padded kinds do not reconstruct an event.

### `latest_jsonl_files(root: Path) -> list[Path]`

Finds replay candidate files under `root`.

Observed behavior:

- Recursively scans `root.rglob("*.jsonl")`.
- Groups candidates by exact parent directory path.
- Extracts the first filename fragment matching `_v<number>_`.
- Treats files with no version fragment as version `-1`.
- Selects one file per parent directory: the file with the highest numeric
  version.
- Keeps the first discovered file when two files in the same parent directory
  have the same version, because replacement only happens for a strictly
  greater version.
- Returns selected files sorted by `path.parent.name`.

The code variable name is `by_day`, but the current code does not validate that
parent directories are daily archive directories.

### `event_from_saved_record(raw_line: str, payload: dict[str, Any]) -> Any | None`

Reconstructs one supported event object from a saved JSONL record dict.

Observed behavior:

- Reads `kind = payload.get("kind")`.
- Returns `None` when `kind` is not in `EVENT_CLASS_BY_KIND`.
- Parses timestamp from `payload.get("timestamp")` through `_parse_timestamp()`.
- Builds `EventMetadata` with:
  - `timestamp`: parsed timestamp or `None`
  - `raw_bytes`: `raw_line.encode("utf-8", errors="ignore")`
- Passes `payload.get("payload", {})` to the event class constructor.
- Does not use `raw_bytes_hash` from the saved record when constructing
  metadata. `EventMetadata.raw_bytes_hash` is recalculated from the saved JSONL
  line bytes.
- Does not validate that the nested `payload` field is a dict or mapping before
  event construction.

### `replay_latest_saved_events(root: Path, on_event: Callable[[Any], None]) -> ReplayStats`

Replays supported records from files selected by `latest_jsonl_files(root)`.

Observed behavior:

- Creates a fresh `ReplayStats`.
- Creates one `seen_raw_hashes` set for the whole replay call.
- Iterates selected files in `latest_jsonl_files(root)` order.
- Increments `files_processed` before opening each selected file.
- Reads files as UTF-8 text.
- Processes nonblank lines in file order.
- Parses each nonblank line with `json.loads(line)`.
- Uses nonblank `raw_bytes_hash` values for replay-local dedupe.
- Skips duplicate nonblank raw hashes before event reconstruction.
- Calls `event_from_saved_record(line, record)`.
- Skips unknown or unsupported event kinds.
- Calls `on_event(event)` synchronously for reconstructed events.
- Increments `events_processed` only after the callback returns normally.
- Returns stats after all selected files complete without uncaught exceptions.

### `_parse_timestamp(value: Any) -> datetime | None`

Internal helper with contract-covered behavior because timestamp reconstruction
is externally observable on replayed events.

Observed behavior:

- Returns `None` for falsey values.
- Converts other values with `str(value).strip()`.
- Returns `None` for a blank stripped string.
- Calls `datetime.fromisoformat(text)` for nonblank text.
- Does not catch timestamp parse errors.

New callers should use the public replay APIs rather than importing this helper.

## Replay Record Schema

The replay module consumes one JSON object per JSONL line. The current upstream
producer is `transforms.to_serializable(event)`, and archive writing is handled
by `outputs.append_local_jsonl()`.

Canonical consumed shape:

```python
{
    "kind": "MatchState",
    "timestamp": "2026-05-10T17:01:00+00:00",
    "raw_bytes_hash": "sha256-or-other-stored-hash",
    "payload": {"type": "match_started"},
}
```

Consumed fields:

| Field | Required for reconstruction | Observed handling |
| --- | --- | --- |
| `kind` | Yes | Exact lookup in `EVENT_CLASS_BY_KIND`; unknown or missing returns `None`. |
| `timestamp` | No | Missing, falsey, or blank becomes `None`; invalid nonblank values raise. |
| `raw_bytes_hash` | No | Used only by `replay_latest_saved_events()` for nonblank dedupe. |
| `payload` | No | Missing key becomes `{}`; present malformed values are not guarded. |

Additional fields are ignored by `event_from_saved_record()`. For example,
`GameState` rows may include a `derived` field from `to_serializable(event)`;
replay currently ignores that field and reconstructs only from `kind`,
`timestamp`, and nested `payload`.

Required v1 compatibility:

- Replayed records must stay compatible with the current
  `to_serializable(event)` output fields.
- The archive row shape must remain producer-owned by `transforms.py` and
  `outputs.py`; replay work must not change runtime JSONL serialization.
- The nested `payload` is expected to be dict-like for supported event classes.
  Broader malformed-payload support requires tests and a contract update.

## Latest-File Selection Semantics

Observed selection algorithm:

1. Find every `*.jsonl` path under `root`.
2. Assign a numeric version:
   - first `_v<number>_` fragment in the filename becomes that integer version
   - no matching fragment becomes `-1`
3. Group by `path.parent`, not by filename date or parsed calendar date.
4. Select the highest numeric version in each parent directory.
5. Sort selected paths by `path.parent.name`.

Required guarantees:

- The function must not read file contents.
- The function must not create, delete, rename, or rewrite archive files.
- The current grouping-by-parent-directory behavior is v1 replay compatibility.
- The current ordering by parent directory name is v1 replay compatibility.
- Any change to grouping, tie-breaking, version parsing, or ordering must be
  treated as replay behavior change and covered by focused tests.

Unknowns and suspected gaps:

- Parent directory names are not validated as dates.
- Sorting by `path.parent.name` may be ambiguous for nested directories with
  the same final name.
- Equal-version tie behavior depends on `Path.rglob()` discovery order and is
  not locked by tests.
- Unversioned files always lose to versioned files in the same parent directory
  because unversioned version is `-1`.

## Event Kind Mapping

Required v1 supported mapping:

- `ClientAction`
- `DetailedLoggingStatus`
- `EventLifecycle`
- `GameResult`
- `GameState`
- `MatchState`
- `Rank`

Observed callback implications:

- `state.py` currently interprets `MatchState`, `GameState`, `Rank`,
  `ClientAction`, and `GameResult`.
- `state.py` treats unknown event kinds as no-ops.
- `DetailedLoggingStatus` and `EventLifecycle` are reconstructable by replay
  but are not parser-state truth owners.

Suspected mapping gap:

- `transforms.include_event()` can keep additional event kinds that are not
  currently reconstructable by replay, including `Inventory`,
  `DeckCollection`, `MatchConnectionState`, `TcpConnectionClose`,
  `WebSocketClosed`, and `ConnectionError`.
- Unsupported archived kinds are skipped by replay today. Whether replay should
  reconstruct every archived kind is an implementation/comparison question for
  Codex C, not a behavior change authorized by this contract writer pass.

Required change-control rule:

- Adding, removing, or remapping event kinds changes replay behavior and must
  be compared against this contract, covered by focused tests, and kept within
  parser event class boundaries.

## Timestamp Behavior

Observed behavior:

- Missing timestamp, `None`, empty string, and whitespace-only string become
  `None`.
- Nonblank values are stringified, stripped, and parsed with
  `datetime.fromisoformat()`.
- Timezone-aware ISO strings such as `2026-05-10T17:00:00+00:00` preserve
  timezone information.
- Invalid nonblank timestamp values raise from `datetime.fromisoformat()`.
- Timestamp parse failures are not converted into skipped-event counts.

Required guarantees:

- Replay must preserve parsed timestamps in `event.metadata.timestamp`.
- Replay must not invent current-time timestamps for saved records.
- Replay must not silently replace malformed timestamps with successful
  best-effort values without a contract update.

## Raw Hash Dedupe Scope

Observed behavior:

- `replay_latest_saved_events()` creates one `seen_raw_hashes` set per replay
  call.
- Dedupe scope is global across all selected files in that call.
- Only nonblank `raw_bytes_hash` values participate.
- Missing, `None`, empty, and whitespace-only hashes do not participate in
  dedupe.
- A duplicate nonblank hash is skipped before event reconstruction and
  increments `events_skipped`.
- A first-seen nonblank hash is added before event reconstruction. If the
  record later skips because its kind is unsupported, that hash has still been
  consumed for the rest of the replay call.

Required guarantees:

- Raw-hash dedupe is local replay behavior only. It must not change live parser
  dedupe, match identity, game identity, workbook upsert keys, or webhook
  transport dedupe.
- The current global-per-call dedupe scope is v1 replay compatibility unless
  Codex C routes back with evidence that the contract is wrong.
- Blank or missing hashes must not be guessed or synthesized by the replay
  utility.

Unknown:

- It is not yet confirmed whether global dedupe across all latest files is
  preferable to per-file or per-day dedupe for all future replay workflows.

## Stats Counting Rules

Observed current rules:

| Input or outcome | `files_processed` | `events_processed` | `events_skipped` |
| --- | ---: | ---: | ---: |
| Selected file reached | +1 before open | no change | no change |
| Blank or whitespace-only line | no change | no change | no change |
| Duplicate nonblank `raw_bytes_hash` | no change | no change | +1 |
| Unknown or unsupported `kind` | no change | no change | +1 |
| Supported event and callback returns normally | no change | +1 after callback | no change |
| Callback raises | no returned stats | not incremented for that event | not incremented for that event |
| Invalid JSON | no returned stats | not incremented for that record | not incremented for that record |
| Invalid timestamp | no returned stats | not incremented for that record | not incremented for that record |
| Non-dict top-level JSON | no returned stats | not incremented for that record | not incremented for that record |
| File open/read error | no returned stats | no reliable returned count | no reliable returned count |

Required guarantees:

- `events_processed` means the callback accepted the reconstructed event without
  raising.
- `events_skipped` currently means known replay-skip cases only: duplicate
  nonblank hashes and unsupported event kinds.
- Blank lines are invisible to stats in v1.
- Broadening `events_skipped` to include malformed JSON, timestamp errors,
  callback errors, or file errors is a behavior change requiring tests and a
  contract update.

## Malformed And Unknown Record Behavior

Observed unknown-kind behavior:

- Missing or unsupported `kind` returns `None` from
  `event_from_saved_record()`.
- `replay_latest_saved_events()` converts `None` events into
  `events_skipped += 1`.

Observed malformed behavior:

- Invalid JSON raises from `json.loads()`.
- Valid JSON whose top-level value is not dict-like can raise when replay calls
  `.get()`.
- Invalid nonblank timestamps raise from `datetime.fromisoformat()`.
- Missing nested `payload` key becomes `{}`.
- Present nested `payload` values that are not mapping-like are not defended
  before event construction and may raise through `BaseEvent` payload copying.
- File open/read errors propagate.
- Callback exceptions propagate.

Required guarantees:

- Unknown supported-boundary records must not invent parser facts.
- Fail-fast malformed behavior must remain visible unless a future problem
  representation explicitly chooses a degradation policy.
- Missing payload as `{}` is current v1 compatibility for supported event
  classes.
- Any new graceful degradation path must explain how stats count the record and
  must prove invalid input does not poison parser-state replay.

## Callback Side-Effect Behavior

Observed behavior:

- `on_event` is called synchronously in replay order.
- Replay order is selected-file order from `latest_jsonl_files(root)`, then
  physical line order inside each file.
- The callback receives the reconstructed event object.
- The callback return value is ignored.
- Callback exceptions are not caught.
- `events_processed` increments after the callback returns normally.
- All parser-state mutation, diagnostics mutation, logging, or other side
  effects are owned by the callback, not by `saved_event_replay.py`.

Required guarantees:

- `saved_event_replay.py` must not directly call parser state, submit webhooks,
  write workbook rows, write runtime status, or mutate Apps Script behavior.
- Replay must remain callback-driven so callers own the replay target and side
  effects.
- Callback failures must remain visible to the caller unless a future contract
  defines a structured error/degradation mechanism.

## Required Guarantees

Future work against this module must preserve these guarantees unless this
contract is explicitly revised:

- Replay remains a local evidence and QA utility, not a parser truth owner.
- Public APIs remain import-compatible:
  - `ReplayStats`
  - `EVENT_CLASS_BY_KIND`
  - `latest_jsonl_files(root)`
  - `event_from_saved_record(raw_line, payload)`
  - `replay_latest_saved_events(root, on_event)`
- Saved record consumption remains compatible with current
  `to_serializable(event)` output.
- Latest-file selection remains recursive, per parent directory, highest
  numeric `_v<number>_`, unversioned `-1`, sorted by parent directory name.
- Supported event kind mapping includes the seven current kinds listed above.
- Unknown event kinds are skipped without event construction.
- Blank timestamps become `None`; invalid nonblank timestamps fail fast.
- `metadata.raw_bytes` for replayed events is based on the saved JSONL line
  text passed to `event_from_saved_record()`, not the original `Player.log`
  raw bytes.
- Nonblank `raw_bytes_hash` dedupe is global across one
  `replay_latest_saved_events()` call.
- Blank lines are ignored without affecting stats.
- Callback side effects remain caller-owned.
- The module does not write files, post webhooks, update workbooks, mutate
  parser state directly, or update runtime status.
- The module does not change parser event class constructors or payload
  contracts.

## Unknowns

- Whether latest-file grouping should stay per parent directory or become
  explicitly day-directory based.
- Whether ordering by `path.parent.name` is robust enough for non-date or
  duplicate-named subdirectories.
- Whether equal-version tie behavior should be deterministic beyond current
  filesystem discovery order.
- Whether replay dedupe should remain global across a replay call or be scoped
  per file/day for some workflows.
- Whether blank lines should remain invisible to stats or count as skipped
  records.
- Whether malformed records should continue to fail fast or become structured
  skipped/error counts.
- Whether missing nested payload should remain `{}` for every supported event
  kind.
- Whether replay metadata should ever prefer original `Player.log` raw bytes if
  the archive schema later stores them separately.
- Whether every archived event kind should become replayable.
- Whether at least one parser-state integration test should feed replayed
  `MatchState` / `GameResult` events into state, or whether focused replay
  utility coverage is sufficient.

## Suspected Gaps

These are comparison targets for Codex C. They are not authorization to change
behavior during this contract writer pass.

- `EVENT_CLASS_BY_KIND` does not cover every event kind that
  `transforms.include_event()` can archive.
- `latest_jsonl_files()` tie behavior for equal versions is not focused-test
  covered.
- File ordering by parent directory name can be ambiguous when multiple
  branches share the same final directory name.
- Current tests cover one selected directory and one replay file; they do not
  prove multi-file ordering or cross-file global dedupe.
- Current tests cover duplicate nonblank raw hashes but not missing or blank
  hashes.
- Current tests cover supported `Rank`, `MatchState`, and `EventLifecycle`
  reconstruction but not every supported kind.
- Current tests do not cover unknown-kind skip behavior directly.
- Current tests do not cover invalid JSON, invalid timestamp, non-dict records,
  missing payload, non-dict payload, or callback exception behavior.
- Current tests do not prove whether the replayed event can safely feed
  parser-state update paths.
- `metadata.raw_bytes_hash` on a replayed event is recalculated from the saved
  JSONL line, while replay dedupe uses the stored `raw_bytes_hash` field. That
  distinction is not directly tested.

## Protected Surfaces And Non-Goals

This contract does not authorize changes to:

- parser behavior outside `saved_event_replay.py`
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- match identity
- game identity
- production deduplication semantics outside the replay utility
- secrets, credentials, API keys, environment variables, webhook URLs, or
  external connections
- raw local logs
- generated card data or generated tier data
- runtime status files
- failed posts
- workbook exports
- `main` or production branches
- tracker #5 completion state

Out of scope for this issue:

- adding a new replay CLI or operator UI
- replaying saved events into the live workbook
- posting replay rows to webhook or Apps Script
- changing archive JSONL file shape produced by runtime code
- changing parser event class constructors or payload contracts
- changing parser-state match/game reconciliation
- changing raw `Player.log` parsing
- changing dashboard, helper formula, workbook, or AI analytics behavior
- broad cleanup of archive directories or generated local data

## Validation Requirements

Documentation-only validation for this Codex B contract:

```powershell
git diff --check
```

Focused implementation or comparison validation expected for Codex C/E if code
or tests change:

```powershell
py -m pytest -q tests\test_saved_event_replay.py
py -m pytest -q tests\test_saved_event_replay.py tests\test_parser_regressions.py
py -m ruff check src tests
git diff --check
```

If implementation touches parser-state replay integration, also consider:

```powershell
py -m pytest -q tests\test_state.py tests\test_match_summary_from_match_state.py tests\test_saved_event_replay.py
```

Before Codex F submitter work, if runtime code changed:

```powershell
py -m pytest -q
py -m ruff check src tests
git diff --check
```

## Acceptance Criteria

- `docs/contracts/parser_saved_event_replay.md` exists on
  `codex/parser-module-audit-suite`.
- The contract identifies `saved_event_replay.py` as a local replay/evidence
  utility, not a parser truth owner.
- The contract defines public interfaces, replay record schema, latest-file
  selection, event kind mapping, timestamp behavior, raw hash dedupe scope,
  stats rules, malformed behavior, callback behavior, and truth boundaries.
- The contract distinguishes observed behavior, required guarantees, unknowns,
  suspected gaps, protected surfaces, validation requirements, and acceptance
  criteria.
- No parser behavior, parser state final reconciliation, workbook schema,
  webhook payload shape, Apps Script behavior, parser event classes,
  match/game identity, deduplication outside replay, secrets, environment
  variables, raw logs, generated data, runtime status files, failed posts, or
  workbook exports changed in the contract writer pass.
- The contract routes next work to Codex C: Module Implementer / comparison
  thread.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for https://github.com/Tahjali11/Mythic-Edge/issues/54.

Module:
src/mythic_edge_parser/app/saved_event_replay.py

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Base branch:
codex/parser-module-audit-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_saved_event_replay.md
- docs/contracts/parser_runner.md
- docs/contracts/parser_outputs.md
- docs/contracts/parser_state.md
- src/mythic_edge_parser/app/saved_event_replay.py
- tests/test_saved_event_replay.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/app/outputs.py
- src/mythic_edge_parser/events.py

Goal:
Compare the current saved-event replay implementation and focused tests against docs/contracts/parser_saved_event_replay.md. Produce docs/implementation_handoffs/parser_saved_event_replay_comparison.md. Implement only the smallest scoped replay-module and focused-test changes if the contract identifies a concrete mismatch.

Before editing, briefly state:
- what the replay utility is supposed to do
- what the current code is actually doing
- whether the issue is a contract mismatch, missing test coverage, or ambiguity
- the exact minimal fix or test plan

Pay special attention to:
- public interfaces
- saved JSONL record schema
- latest-file selection semantics
- event kind mapping completeness
- timestamp behavior
- raw hash dedupe scope
- stats counting rules
- malformed and unknown record behavior
- callback side-effect behavior
- parser truth ownership boundaries

Do:
- Compare first before changing code.
- Preserve current behavior unless the contract clearly requires a change.
- Add focused tests for required replay behavior that is currently uncovered.
- Keep changes inside saved_event_replay.py and tests/test_saved_event_replay.py unless the contract explicitly requires adjacent documentation updates.
- Produce the comparison handoff with confirmed matches, mismatches, files changed, validation, remaining unknowns, forbidden-scope confirmation, and next recommended role.

Do not:
- Change parser behavior outside saved_event_replay.py.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, production deduplication semantics outside replay, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Change archive JSONL shape produced by runtime code unless routed back through a contract update.
- Open a PR, stage, commit, merge, target main, close issue #54, or mark tracker #5 complete.

Validation:
py -m pytest -q tests\test_saved_event_replay.py
py -m pytest -q tests\test_saved_event_replay.py tests\test_parser_regressions.py
py -m ruff check src tests
git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/54"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/parser_saved_event_replay.md"
  target_artifact: "docs/implementation_handoffs/parser_saved_event_replay_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior outside saved_event_replay.py."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, production deduplication semantics outside replay, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not change archive JSONL shape produced by runtime code unless routed back through a contract update."
    - "Do not target main."
    - "Do not open a PR from the comparison thread unless explicitly asked."
    - "Do not close issue #54 or mark tracker #5 complete."
```
