# Parser Runner Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/36

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Problem-representation docs read because issue #36 is the source problem
representation:

- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

Adjacent contracts:

- `docs/contracts/parser_state.md`
- `docs/contracts/parser_extractors.md`
- `docs/contracts/parser_client_actions.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_event_lifecycle.md`
- `docs/contracts/parser_api_common.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes `src/mythic_edge_parser/app/runner.py` as the live
parser/runtime bridge. It is a contract artifact only. It does not implement
code or change parser behavior.

## Module

`src/mythic_edge_parser/app/runner.py`

The module starts the live MTGA event stream, receives parser-produced events,
updates parser-owned state, records diagnostics/status, writes kept events to
the local JSONL archive, coordinates output sidecars, and submits
workbook-facing rows through existing transport helpers.

Plain English: the runner owns orchestration and side-effect ordering. It does
not parse raw Player.log bodies, define parser event classes, invent match or
game truth, reconcile final results, define workbook row schemas, define
webhook payload shapes, or own Apps Script behavior.

## Owning Layer

Primary layer: parser and state interpretation, with an explicit
runtime/transport boundary.

Truth boundary:

- Parser modules and `app/state.py` own event interpretation, live parser
  context, match identity, game identity, final reconciliation, and normalized
  match/game facts.
- `runner.py` owns when parser-produced events are sent to state, diagnostics,
  local JSONL archive, gameplay-action observation, analytics sidecar,
  webhook row dispatch, console logging, and shutdown cleanup.
- `app/transforms.py` owns event inclusion, serializable archive rows, raw
  debug sheet rows, and summary strings.
- `app/outputs.py` owns local JSONL file path caching and webhook dispatch
  mechanics.
- `app/diagnostics.py` owns runtime logs, runtime status files, failed event
  records, failed post records, submitted-deck diagnostics, and URL redaction.
- `app/analytics_sidecar.py`, `app/runtime_surfaces.py`,
  `app/gameplay_actions.py`, and row/export helpers own analytics and runtime
  artifact construction after the runner submits events.
- Workbook formulas, dashboard logic, Apps Script, webhook transport, and AI
  notes must not become parser truth owners through runner work.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/runner.py`
- `tests/test_runner.py`
- `docs/contracts/parser_runner.md`

Related files whose behavior is referenced but not owned by this contract:

- `main.py`
- `src/mythic_edge_parser/app/__init__.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `tests/test_app_outputs.py`
- `tests/test_diagnostics.py`
- `tests/test_status_api.py`
- `tests/test_stream_unit.py`
- `tests/test_stream_integration.py`
- `tests/test_state.py`
- `tests/test_transforms.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_sheet_exports.py`
- `tests/test_parser_regressions.py`

## Public Interface

### Runtime Entrypoint

`async def main() -> None`

Primary live runtime entrypoint. `main.py` imports this function and executes it
with `asyncio.run(run_parser())`. `src/mythic_edge_parser/app/__init__.py`
also exposes a lazy `main()` wrapper that returns the coroutine from
`runner.main()`.

Contract status:

- Starts runtime logging, startup checks, the MTGA event stream, optional
  webhook dispatcher, analytics sidecar, and optional status API.
- Consumes parser events from the `MtgaEventStream` subscriber until the
  subscriber returns `None`.
- Applies the event-loop ordering defined in this contract.
- Records runner-stage event failures and continues to the next event.
- Performs shutdown cleanup in the defined order once the live loop exits after
  a successfully created stream.

### Internal-Public Helpers

These names are underscore-prefixed, but they are contract-covered because
focused tests and sibling modules depend on their current behavior.

| Interface | Current signature | Contract status |
| --- | --- | --- |
| `_display_path(path)` | `(Path | None) -> str` | Display-safe path normalization for logs/status. |
| `_sheet_posting_enabled()` | `() -> bool` | Aggregates all runner-visible webhook/output flags. |
| `_startup_status_fields()` | `() -> dict[str, object]` | Startup status payload builder. |
| `_startup_issues()` | `() -> tuple[list[str], list[str]]` | Startup warning/error collector. |
| `_should_post_sheet_debug_rows(event)` | `(object) -> bool` | Raw/GameState debug row gate. |
| `_post_sheet_debug_rows(event)` | `(object) -> int` | Queues debug rows built by `to_sheet_rows()`. |
| `_maybe_record_submitted_deck(event, logger)` | `(object, object) -> None` | Records kept submitted-deck client actions. |
| `_post_game_log_rows(logger)` | `(object) -> None` | Queues changed Game Log rows for the current match. |
| `_post_match_summary_row()` | `() -> None` | Queues one ready MatchSummary row per match. |
| `_post_match_log_row(logger)` | `(object) -> None` | Queues changed Match Log rows for the current match. |
| `_game_log_success_callback(...)` | returns callable | Snapshots Game Log row and changed fields before async dispatch. |
| `_match_log_success_callback(...)` | returns callable | Snapshots Match Log row and changed fields before async dispatch. |

## Inputs

### Configuration Inputs

`runner.py` reads these imported configuration values at module runtime:

- Paths:
  - `LOG_PATH`
  - `MATCH_LOGS_ROOT`
  - `PROJECT_ROOT`
  - `TIER_NORMALIZATION_PATH`
- Webhook:
  - `WEBHOOK_URL`
- Posting and sync flags:
  - `POST_RAW_EVENT_ROWS`
  - `POST_GAMESTATE_ROWS`
  - `POST_GAME_LOG_ROWS`
  - `POST_MATCH_SUMMARY_ROWS`
  - `POST_MATCH_LOG_ROWS`
  - `POST_ACTION_LOG_ROWS`
  - `POST_DECK_SNAPSHOT_ROWS`
  - `POST_COLLECTION_SNAPSHOT_ROWS`
  - `POST_PARSER_STATUS_ROWS`
  - `POST_CARD_PERFORMANCE_ROWS`
  - `SYNC_TIER_BUCKETS`

`app/config.py` owns environment variable names, defaults, legacy environment
fallbacks, and parsing rules. Runner work must not change environment variable
names or default values without a separate contract.

### Event Stream Input

`main()` receives events through:

- `stream, subscriber = await MtgaEventStream.start(LOG_PATH)`
- `event = await subscriber.recv()`

`stream.py`, `event_bus.py`, and `router.py` own log tailing, parser dispatch,
event bus capacity, subscriber sentinel behavior, and router failure handling.
`runner.py` consumes typed `GameEvent` objects after those modules emit them.

Accepted event surface:

| Field | Type | Required by runner | Notes |
| --- | --- | --- | --- |
| `event.kind` | string-like | No, but expected | Used for gates and logging. |
| `event.payload` | dict-like | No, defaults through helpers | Passed to state, transforms, diagnostics, and analytics. |
| `event.metadata.timestamp` | datetime-like or absent | No | Used by `_event_datetime()` and submitted-deck diagnostics. |
| `event.metadata.raw_bytes_hash` | string-like or absent | No | Preserved in failure diagnostics. |

Malformed event objects are not rejected at the top of the loop. They are
allowed to flow into helper calls, and runner-stage exceptions are handled by
`record_event_failure(event, exc, stage="runner")`.

### Parser State Input

Runner reads parser context and row readiness through `app/state.py`:

- `_CONTEXT["current_match_id"]`
- `_CONTEXT["current_game_number"]`
- `_CONTEXT["current_player_team"]`
- `_POSTED_MATCH_SUMMARIES`
- `_update_match_summary(event)`
- `build_game_log_updates(match_id)`
- `build_match_summary_row(match_id)`
- `build_match_log_update(match_id)`
- `mark_game_log_posted(match_id, game_number, row)`
- `mark_match_log_posted(match_id, row)`

State owns what these facts mean. Runner owns only when it calls them and which
callbacks fire after webhook success.

## Outputs

### Runtime Status Output

Runner writes runtime status through `diagnostics.update_runtime_status()`.

Startup status fields currently include:

| Field | Source | Notes |
| --- | --- | --- |
| `status` | literal `"starting"` | Later changed to `"running"` and `"stopped"` by runner. |
| `log_path` | `_display_path(LOG_PATH)` | Must be display-safe. |
| `match_logs_root` | `_display_path(MATCH_LOGS_ROOT)` | Must be display-safe. |
| `webhook_enabled` | `bool(WEBHOOK_URL)` | Does not validate URL by itself. |
| `webhook_target` | `webhook_target_display(WEBHOOK_URL)` | Must be redacted/display-safe. |
| `post_match_log_rows` | `POST_MATCH_LOG_ROWS` | Transport flag. |
| `post_game_log_rows` | `POST_GAME_LOG_ROWS` | Transport flag. |
| `post_match_summaries` | `POST_MATCH_SUMMARY_ROWS` | Historical field name. |
| `post_raw_event_rows` | `POST_RAW_EVENT_ROWS` | Transport/debug flag. |
| `post_gamestate_rows` | `POST_GAMESTATE_ROWS` | Transport/debug flag. |
| `post_action_log_rows` | `POST_ACTION_LOG_ROWS` | Sidecar/export flag. |
| `post_deck_snapshot_rows` | `POST_DECK_SNAPSHOT_ROWS` | Sidecar/export flag. |
| `post_collection_snapshot_rows` | `POST_COLLECTION_SNAPSHOT_ROWS` | Sidecar/export flag. |
| `post_parser_status_rows` | `POST_PARSER_STATUS_ROWS` | Sidecar/export flag. |
| `post_card_performance_rows` | `POST_CARD_PERFORMANCE_ROWS` | Sidecar/export flag. |
| `status_file_path` | `_display_path(current_status_path())` | Must be display-safe. |

If the status API starts successfully, runner adds:

- `local_status_api_url`
- `local_status_api_host`
- `local_status_api_port`
- `local_status_api_enabled=True`

If status API startup raises, runner writes:

- `local_status_api_enabled=False`
- `local_status_api_error=<exception text>`

### Local JSONL Archive Output

For kept events only, runner:

1. Builds `local_row = to_serializable(event)`.
2. Gets `event_dt = _event_datetime(event)`.
3. Calls `append_local_jsonl(local_row, event_dt)`.

`outputs.py` owns the daily folder/file naming and write mechanics. Runner must
not alter local JSONL row shape; that belongs to `transforms.py`.

### Workbook-Facing Row Dispatch Output

Runner queues rows with `submit_row_to_google_sheets()`. `outputs.py` owns
deduplicating pending row payloads, HTTP retries, failed post recording, and
success/failure callback dispatch.

Runner-owned posting paths:

| Posting path | Gate | Row builder owner | Success callback |
| --- | --- | --- | --- |
| Raw/debug rows | `_should_post_sheet_debug_rows(event)` | `transforms.to_sheet_rows()` | none |
| Game Log rows | `POST_GAME_LOG_ROWS` and current match ID | `state.build_game_log_updates()` | `mark_game_log_posted()` |
| MatchSummary row | `POST_MATCH_SUMMARY_ROWS`, current match ID, not posted | `state.build_match_summary_row()` | add match ID to `_POSTED_MATCH_SUMMARIES` |
| Match Log row | `POST_MATCH_LOG_ROWS` and current match ID | `state.build_match_log_update()` | `mark_match_log_posted()` |

Runner must not change workbook row schemas, field names, Apps Script behavior,
webhook payload shape, or row construction semantics in this audit.

### Diagnostics And Runtime Artifacts

Runner may cause these local runtime artifacts to be written through owned
helper modules:

- runtime log file under `RUNTIME_LOGS_ROOT`
- runtime status JSON under `STATUS_ROOT`
- local match JSONL archive under `MATCH_LOGS_ROOT`
- bad event JSONL records under `BAD_EVENTS_ROOT`
- failed webhook post JSONL records under `FAILED_POSTS_ROOT`
- active submitted deck JSON under `ACTIVE_SUBMITTED_DECK_PATH`
- gameplay-action status artifacts through `gameplay_actions.py`
- runtime surface, timeline, history, deck, collection, parser-status, and
  card-performance artifacts through the analytics sidecar

These are runtime/generated artifacts. They must not be committed as part of a
runner audit unless a separate issue explicitly approves a fixture or sample.

## Observed Current Behavior

### Display Path Behavior

- `_display_path(None)` returns `""`.
- Project-relative paths are displayed relative to `PROJECT_ROOT`.
- External POSIX paths display as the basename.
- Windows-style paths seen on POSIX display as the Windows basename when the
  text contains backslashes and a Windows drive or root.
- Fallback behavior returns `path.name`, the Windows basename, or the original
  path text.

### Startup Behavior

Observed `main()` startup order:

1. `setup_runtime_logging()`.
2. `logger = get_logger("runner")`.
3. `MATCH_LOGS_ROOT.mkdir(parents=True, exist_ok=True)`.
4. Log the runtime log file path.
5. `update_runtime_status(**_startup_status_fields())`.
6. Collect warnings and errors through `_startup_issues()`.
7. Log all startup warnings and errors.
8. Raise `RuntimeError("Startup checks failed. See runtime log for details.")`
   if any startup errors exist.
9. `bootstrap_gameplay_actions()`.
10. `stream, subscriber = await MtgaEventStream.start(LOG_PATH)`.
11. Log watched path, output roots, posting flags, and redacted webhook target.
12. `update_runtime_status(status="running")`.
13. Start webhook dispatcher only when `_sheet_posting_enabled()` is true.
14. Start analytics sidecar unconditionally.
15. Try to start the status API; status API startup failure is logged as a
   warning and is not fatal.

`_startup_issues()` currently returns:

- Error when `LOG_PATH` does not exist.
- Warning when any sheet/sidecar posting flag is enabled and `WEBHOOK_URL` is
  blank.
- Error when posting is enabled and `WEBHOOK_URL` is not an `http` or `https`
  URL with a network location.
- Warning when `SYNC_TIER_BUCKETS` is true and
  `TIER_NORMALIZATION_PATH` is missing.
- Warning when `SYNC_TIER_BUCKETS` is true and the tier normalization file
  cannot be read as JSON.

### Event Loop Behavior

Observed per-iteration order inside `main()`:

1. `drain_webhook_results()`.
2. `event = await subscriber.recv()`.
3. Break the loop when `event is None`.
4. `_update_match_summary(event)`.
5. `mark_event_seen(event, match_id=..., game_number=..., player_team=...)`.
6. `observe_gameplay_event(event)`.
7. `keep_event = include_event(event)`.
8. `submit_analytics_event(event, include_in_timeline=keep_event)`.
9. If `keep_event` is false, continue to the next loop iteration.
10. `to_serializable(event)`.
11. `_event_datetime(event)`.
12. `append_local_jsonl(local_row, event_dt)`.
13. `_maybe_record_submitted_deck(event, logger)`.
14. `_post_sheet_debug_rows(event)`.
15. `_post_game_log_rows(logger)`.
16. `_post_match_summary_row()`.
17. `_post_match_log_row(logger)`.
18. `summarize(event)`.
19. Log GameState summaries at debug level and other kept summaries at info
    level.

Every non-`None` event currently reaches parser state, diagnostics
`mark_event_seen()`, gameplay-action observation, and analytics sidecar
submission before the keep/drop branch. Dropped events do not reach local JSONL
archive writing, submitted-deck diagnostics, debug row posting, Game Log row
posting, MatchSummary row posting, Match Log row posting, or console summary
logging.

### Keep/Drop Decisions

Runner does not own keep/drop interpretation. It calls
`transforms.include_event(event)`.

Required runner boundary:

- Do not move `_update_match_summary(event)`, `mark_event_seen()`,
  `observe_gameplay_event()`, or `submit_analytics_event()` behind the
  `include_event(event)` keep gate without a new contract.
- Do not make dropped events appear in local JSONL or workbook-facing runner
  rows without a new contract.
- Preserve the observed analytics behavior that all events are submitted to
  the sidecar with `include_in_timeline` reflecting the keep/drop decision.

### Submitted Deck Behavior

`_maybe_record_submitted_deck(event, logger)` currently:

- Runs only after the event has been kept and archived.
- Ignores non-`ClientAction` events.
- Ignores client actions whose payload `type` is not `submit_deck_resp`.
- Calls `diagnostics.record_submitted_deck()` with the event payload, current
  match ID, current game number, and event timestamp.
- Logs the active submitted deck path only when an artifact path is returned.

Runtime surfaces may also observe submitted-deck events through the analytics
sidecar. Runner must not merge those responsibilities.

### Webhook Dispatcher And Callback Behavior

Observed callback guarantees:

- Game Log and Match Log success callbacks snapshot `row` and
  `changed_fields` with shallow copies when the callback is created.
- The callbacks mark posted state only after `outputs.drain_webhook_results()`
  receives a successful dispatch result and invokes `on_success`.
- Runner does not provide `on_failure` callbacks for Game Log, MatchSummary,
  or Match Log rows.
- MatchSummary rows are marked posted by adding the match ID to
  `_POSTED_MATCH_SUMMARIES` only after webhook success.

Required guarantee:

- Do not mark parser-state rows as posted before asynchronous webhook success.
- Do not let later mutation of a row dict or changed-fields list alter what a
  queued success callback records.

### Shutdown Behavior

After a stream has been created, `main()` currently performs this `finally`
cleanup when the live loop exits or an uncaught loop-level exception leaves the
outer try:

1. `drain_webhook_results(max_items=5000)`.
2. `stop_webhook_dispatcher(wait_for_queue=True)`.
3. `drain_webhook_results(max_items=5000)`.
4. `stop_analytics_sidecar(wait_for_queue=False)`.
5. `update_runtime_status(status="stopped")`.
6. `stop_status_api_server()`.
7. `await stream.shutdown()`.

The runner does not currently wrap shutdown calls in independent best-effort
error handlers. A failure during cleanup may propagate after earlier cleanup
steps have already run.

## Required Guarantees

- `runner.py` must remain an orchestration module, not a parser truth owner.
- Startup status must use display-safe local paths and redacted webhook target
  text.
- Startup validation must distinguish warnings from fatal errors as documented.
- A missing `LOG_PATH` remains a fatal startup error unless a new contract
  changes live-tail behavior.
- Blank webhook URL with posting enabled remains a warning, not a fatal error.
- Invalid webhook URL with posting enabled remains a fatal error.
- Missing or unreadable tier normalization data remains a warning while
  `SYNC_TIER_BUCKETS` is enabled.
- `MtgaEventStream.start(LOG_PATH)` remains the source of subscriber events.
- Parser state must see every non-`None` event before runner keep/drop
  decisions.
- Diagnostics `mark_event_seen()` must run before the keep/drop branch.
- Gameplay-action observation must run before the keep/drop branch.
- Analytics sidecar submission must receive every event with
  `include_in_timeline=keep_event`.
- Kept events only are archived locally and posted through runner-owned
  workbook row paths.
- Raw/debug row posting remains gated by `POST_RAW_EVENT_ROWS` or
  `POST_GAMESTATE_ROWS` for `GameState` events.
- Game Log and Match Log posted-state markers must be success-callback driven.
- MatchSummary once-only posting must remain success-callback driven.
- Runner-stage event failures must be recorded through
  `record_event_failure(..., stage="runner")` and must not stop the subscriber
  loop for a single bad event.
- Shutdown must drain webhook results around dispatcher shutdown, stop the
  analytics sidecar, mark runtime status stopped, stop the status API, and
  shut down the stream.
- Runner changes must not change workbook schema, webhook payload shape, Apps
  Script behavior, parser event classes, parser state final reconciliation,
  extractor behavior, match identity, game identity, deduplication, secrets,
  environment variables, raw logs, generated data, runtime status files, failed
  posts, or workbook exports without a separate issue and contract.

## Unknowns And Suspected Gaps

- Focused tests currently cover display path normalization, startup status
  sanitization, posting-flag aggregation, and raw/GameState debug row gating.
- There is no focused test that drives the full `main()` event loop with fake
  stream/subscriber objects and asserts the complete side-effect order.
- There is no focused test proving dropped events update parser state,
  diagnostics, gameplay observation, and analytics while skipping archive and
  workbook row paths.
- There is no focused test for runner-stage failure handling and continuation
  after `record_event_failure()`.
- There is no focused test for `_startup_issues()` warning/error combinations.
- There is no focused runner test for status API startup success/failure
  status fields.
- There is no focused runner test proving Game Log and Match Log success
  callbacks snapshot row data and changed-field lists before async dispatch.
- There is no focused runner test for shutdown ordering.
- The observed shutdown call `stop_analytics_sidecar(wait_for_queue=False)` may
  leave queued analytics work unprocessed on stop. This contract records the
  current behavior and does not change it.
- When the status API is disabled by configuration, `start_status_api_server()`
  returns `None` and runner currently does not write an explicit disabled
  status field in that branch. This contract records current behavior and
  leaves any change to a future problem representation.

## Error Behavior

- Fatal startup errors from `_startup_issues()` raise `RuntimeError` after
  startup status has been written and errors have been logged.
- Exceptions from `MtgaEventStream.start(LOG_PATH)` are logged and re-raised;
  the shutdown `finally` block is not entered because no stream exists yet.
- Status API startup exceptions are logged as warnings and recorded in runtime
  status; they do not stop the parser runtime.
- Per-event runner exceptions are caught, recorded with
  `record_event_failure(event, exc, stage="runner")`, logged with the saved
  failure path, and then the loop continues.
- Webhook HTTP/network failures are owned by `outputs.py`, which records failed
  posts and updates webhook failure status.
- Router failures before events reach runner are owned by `stream.py` and
  `diagnostics.record_router_failure()`, not by runner.

## Side Effects

Allowed runner-triggered side effects:

- Creates `MATCH_LOGS_ROOT`.
- Writes runtime logs and status through `diagnostics.py`.
- Starts and stops the MTGA event stream.
- Starts and stops the webhook dispatcher when posting is enabled.
- Starts and stops the analytics sidecar.
- Starts and stops the local status API when enabled and available.
- Mutates parser runtime state by calling `state._update_match_summary(event)`.
- Mutates diagnostics status by calling `mark_event_seen()`.
- Mutates gameplay-action runtime state by calling `observe_gameplay_event()`.
- Queues analytics sidecar jobs.
- Writes kept events to local JSONL through `append_local_jsonl()`.
- Records active submitted-deck diagnostics for kept submit-deck actions.
- Queues workbook-facing rows through `submit_row_to_google_sheets()`.
- Marks Game Log, MatchSummary, and Match Log rows as posted only through
  webhook success callbacks.
- Writes bad-event diagnostics for runner-stage event processing failures.

Forbidden side effects for this audit:

- Do not alter committed raw logs, generated data, runtime status snapshots,
  failed posts, workbook exports, or local output artifacts.
- Do not change workbook schema or Apps Script files.
- Do not change parser event classes, parser payload shapes, extractor
  behavior, state final reconciliation, match/game identity, or dedupe
  semantics.
- Do not commit secrets, webhook URLs, tokens, local MTGA logs, failed posts,
  runtime status files, generated card data, or raw workbook exports.

## Dependency Order

Future implementation work should follow this order:

1. Compare `runner.py` and focused tests against this contract.
2. Add focused tests for missing contracted behavior before changing behavior.
3. Keep code changes runner-local unless a test exposes a collaborator bug that
   already belongs to that collaborator's contract.
4. If a required fix would change parser truth, workbook row shape, webhook
   payload shape, runtime artifact shape, environment variables, or downstream
   behavior, stop and route back to Codex B or Codex A before editing.
5. Produce `docs/implementation_handoffs/parser_runner_comparison.md` with the
   comparison, changes, validation, and remaining risks.

## Compatibility

- Preserve `main()` as the async runtime entrypoint imported by `main.py`.
- Preserve the lazy `src/mythic_edge_parser/app/__init__.py` wrapper unless a
  separate entrypoint contract changes it.
- Preserve `_display_path()` behavior for Windows-style paths on POSIX; this
  is completed context from issue #7 and should not regress.
- Preserve internal-public helper names until a migration contract updates
  tests and call sites together.
- Preserve imported config flag names and their runner semantics.
- Preserve startup status field names, especially the existing
  `post_match_summaries` field, unless a diagnostics/status contract changes
  the status schema.
- Preserve success-callback based posted-state updates.
- Preserve the branch target `codex/parser-module-audit-suite` for module PR
  work.

## Tests Required

Focused runner checks:

```bash
python3 -m pytest -q tests/test_runner.py
```

Adjacent behavior checks for implementation or fixer roles:

```bash
python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m ruff check src tests
```

Before submitter opens or updates a module PR:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
```

Test obligations for Codex C or Codex D:

- Add a focused async runner-loop test with fake stream/subscriber objects that
  proves the per-event side-effect order.
- Add a focused dropped-event test proving state, diagnostics, gameplay
  observation, and analytics run while archive and row posting do not.
- Add a focused event-failure test proving `record_event_failure()` is called
  with `stage="runner"` and the loop continues.
- Add `_startup_issues()` tests for missing log path, blank webhook warning,
  invalid webhook error, missing tier normalization warning, and unreadable
  tier JSON warning.
- Add status API startup success/failure tests if not already covered through a
  runner-level fake.
- Add success-callback copy-semantics tests for Game Log and Match Log rows.
- Add shutdown-order coverage if fake stream/dispatcher/sidecar hooks make it
  practical without flaky live threads.

## Acceptance Criteria

- The runner contract exists at `docs/contracts/parser_runner.md`.
- The contract names the parser/runtime bridge ownership boundary clearly.
- Public and internal-public runner interfaces are listed with their current
  signatures and contract status.
- Event-loop ordering distinguishes all-event side effects from kept-event-only
  side effects.
- Startup, shutdown, status, archive, webhook, callback, and failure behavior
  are documented.
- Protected parser, workbook, webhook, Apps Script, raw log, generated data,
  runtime status, failed post, and workbook export surfaces remain unchanged.
- Implementation/fixer roles have concrete test obligations.
- Module PR work targets `codex/parser-module-audit-suite`, not `main`.

## Handoff Packet

Role performed: Codex B: Module Contract Writer

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/36

Contract produced: `docs/contracts/parser_runner.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/5

Risk tier: High

Owning truth layer: parser and state interpretation with explicit
runtime/transport boundary

Public interface:

- `async def main() -> None`
- `_display_path(path)`
- `_sheet_posting_enabled()`
- `_startup_status_fields()`
- `_startup_issues()`
- `_should_post_sheet_debug_rows(event)`
- `_post_sheet_debug_rows(event)`
- `_maybe_record_submitted_deck(event, logger)`
- `_post_game_log_rows(logger)`
- `_post_match_summary_row()`
- `_post_match_log_row(logger)`
- `_game_log_success_callback(...)`
- `_match_log_success_callback(...)`

Invariants:

- Parser state sees every event before keep/drop decisions.
- Diagnostics, gameplay observation, and analytics submission run before the
  keep/drop branch.
- Local JSONL archive and runner-owned workbook row posting are kept-event only.
- Posted-state markers are success-callback driven.
- Runner does not own parser truth, workbook schema, webhook payload shape, or
  Apps Script behavior.

Required tests:

- `python3 -m pytest -q tests/test_runner.py`
- `python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py`
- `python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py`
- `python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py`
- `python3 -m pytest -q tests/test_parser_regressions.py`
- `python3 -m ruff check src tests`

Acceptance criteria:

- Compare current runner implementation and focused tests against this
  contract.
- Add focused tests for missing contracted behavior.
- Keep any implementation changes minimal and runner-local unless the contract
  explicitly requires a collaborator change.
- Preserve all protected surfaces and branch policy.

Open questions or contract risks:

- Current test coverage does not lock down full main-loop side-effect order.
- Current test coverage does not lock down dropped-event behavior.
- Current test coverage does not lock down event-failure continuation.
- Current test coverage does not lock down shutdown order.
- The observed analytics sidecar shutdown uses `wait_for_queue=False`; this
  contract records but does not change that behavior.

Next recommended thread role: Codex C: Module Implementer

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for issue #36 and docs/contracts/parser_runner.md.

Goal:
Compare the current runner implementation and focused tests against the parser runner contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/36
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_runner.md
- src/mythic_edge_parser/app/runner.py
- tests/test_runner.py
- src/mythic_edge_parser/stream.py
- src/mythic_edge_parser/event_bus.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/app/config.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/app/outputs.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/analytics_sidecar.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/gameplay_actions.py

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned truth boundaries.
- Add focused tests for contracted runner behavior not currently covered.
- Keep behavior changes minimal and runner-local unless the contract explicitly requires a collaborator update.
- Produce docs/implementation_handoffs/parser_runner_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned truth into runner orchestration, workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/36"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_runner.md"
  target_artifact: "docs/implementation_handoffs/parser_runner_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
    - "python3 -m pytest -q tests/test_runner.py"
    - "not run - python3 -m ruff check src tests (implementation/submission gate)"
  stop_conditions:
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned truth into runner orchestration, workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Do not mark tracker #5 complete."
```
