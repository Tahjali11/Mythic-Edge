# Parser Outputs Module Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/40

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Problem-representation docs read because issue #40 is the source problem
representation:

- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

Adjacent contracts:

- `docs/contracts/parser_runner.md`
- `docs/contracts/parser_state.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the runtime output transport and local archive boundary
in `src/mythic_edge_parser/app/outputs.py`. It is a contract artifact only. It
does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/app/outputs.py`

The module moves already-produced parser/workbook-facing rows to output sinks:

- synchronous Google Sheets webhook POSTs
- asynchronous webhook dispatch through a background queue
- dispatch success/failure callback delivery
- failed-post diagnostic capture through `diagnostics.py`
- local JSONL archive writing under the current daily match-log path
- runtime status updates for webhook dispatcher activity and webhook outcomes
- runtime-state caching for daily archive paths

Plain English: `outputs.py` transports and archives rows. It must not decide
parser truth, workbook schema, webhook payload shape, event interpretation,
match identity, game identity, deduplication meaning, or final reconciliation.

## Owning Layer

Webhook / transport layer.

`outputs.py` owns runtime mechanics for output delivery after upstream parser,
state, transform, export, analytics, or sync code has already constructed a
row.

Parser truth boundary:

- `app/state.py` owns live parser state, match/game summaries, final
  reconciliation, and runtime state fields that cache the current local archive
  path.
- `app/transforms.py`, `app/sheet_exports.py`, `app/runtime_surfaces.py`,
  `app/analytics_sidecar.py`, and `app/tier_sync.py` own row construction and
  row meaning before handing rows to `outputs.py`.
- `app/runner.py` owns orchestration: when parsing starts, when rows are
  submitted, when callbacks are attached, when webhook results are drained, and
  when shutdown drains the dispatcher.
- `app/diagnostics.py` owns runtime-status and failed-post artifact schemas,
  URL redaction, and sensitive text sanitization.
- `app/config.py` owns environment variable interpretation for webhook URL,
  match-log root, output filename prefix, and related runtime settings.
- `outputs.py` must treat rows as already serialized or already
  workbook-facing data. It may copy, enqueue, post, archive, and report
  delivery status, but it must not reinterpret parser facts or rewrite row
  schema.
- Workbook formulas, dashboard logic, Apps Script, webhook delivery, and
  AI-generated interpretation must not become sources of parser-owned truth.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/outputs.py`
- `tests/test_app_outputs.py`
- `docs/contracts/parser_outputs.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/app/runner.py`
- `tests/test_runner.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `tests/test_diagnostics.py`
- `src/mythic_edge_parser/app/status_api.py`
- `tests/test_status_api.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `tests/test_transforms.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_runtime_surfaces.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `src/mythic_edge_parser/app/tier_sync.py`
- `.github/pull_request_template.md`

## Public Interface

### Dataclasses

`WebhookDispatchJob`

- Public async-dispatch job value stored in the dispatcher queue.
- Fields:
  - `row: dict[str, Any]`
  - `row_key: str`
  - `on_success: Callable[[], None] | None = None`
  - `on_failure: Callable[[], None] | None = None`
- Observed current behavior: `submit_row_to_google_sheets()` creates jobs with
  a shallow `dict(row)` copy, not a deep copy.

`WebhookDispatchResult`

- Public async-dispatch result value stored in the result queue.
- Fields:
  - `job: WebhookDispatchJob`
  - `success: bool`
- Observed current behavior: callbacks are not executed when a result is
  created. Callbacks are executed only when the result is drained through
  `drain_webhook_results()` or shutdown paths that call it.

### Functions

`reset_outputs_runtime_state() -> None`

- Stops the dispatcher without waiting for the queue first.
- Drains queued jobs without processing callbacks.
- Drains completed results without callbacks.
- Clears pending row keys.
- Clears the dispatcher thread reference.
- Updates runtime status with `webhook_dispatcher_active=False`.

`webhook_target_display(url: str | None = None) -> str`

- Returns the diagnostics-owned redacted display form for an explicit URL or
  for configured `WEBHOOK_URL` when `url is None`.
- Must not reveal the configured webhook secret in logs, status output, docs, or
  tests.

`post_row_to_google_sheets(row: dict[str, Any]) -> bool`

- Performs a synchronous HTTP POST to the configured Google Sheets webhook.
- Returns `True` only after a successful POST and diagnostics success update.
- Returns `False` for missing webhook URL or terminal POST failure.
- Does not mutate the row intentionally and does not validate row schema.

`start_webhook_dispatcher() -> None`

- Starts the background webhook dispatcher thread when no live dispatcher thread
  exists.
- Updates runtime status with `webhook_dispatcher_active=True`.
- Is idempotent while the existing dispatcher thread is alive.

`submit_row_to_google_sheets(row: dict[str, Any], on_success: Callable[[], None] | None = None, on_failure: Callable[[], None] | None = None) -> bool`

- Computes a stable pending-row key from the submitted row.
- Enqueues a shallow copied row for async webhook dispatch when that key is not
  already pending.
- Returns `True` when a job is enqueued.
- Returns `False` when an equivalent row is already pending.
- Does not call callbacks directly.

`drain_webhook_results(max_items: int = 200) -> int`

- Drains up to `max_items` completed dispatch results.
- Removes each drained result's row key from the pending-key set.
- Invokes the success callback only for successful dispatch results.
- Invokes the failure callback only for failed dispatch results.
- Returns the number of drained results.

`stop_webhook_dispatcher(wait_for_queue: bool = True) -> None`

- Stops the dispatcher thread using a queue sentinel.
- Optionally waits for queued work to finish before sending the sentinel.
- Drains completed results through callback-capable result draining when the
  dispatcher is fully stopped or when no dispatcher thread exists.
- Updates runtime status for dispatcher activity.

`daily_log_label(event_dt: datetime) -> str`

- Returns the daily archive label in `"%m_%d_%y"` format.

`append_local_jsonl(local_row: str, event_dt: datetime) -> None`

- Appends an already serialized JSONL row string plus a newline to the current
  daily archive file.
- Uses `event_dt` to choose the daily folder and filename.
- Updates or reuses parser runtime-state cache fields for the current daily log
  path.

### Implementation Details With Contract-Covered Behavior

These names are not public import targets for new callers, but their behavior is
covered by this contract because tests or lifecycle paths can observe their
effects:

- `_WEBHOOK_MAX_ATTEMPTS`
- `_WEBHOOK_RETRYABLE_STATUS_CODES`
- `_WEBHOOK_BACKOFF_SECONDS`
- `_QUIET_SUCCESS_EVENT_FAMILIES`
- `_DISPATCH_QUEUE`
- `_DISPATCH_RESULTS`
- `_DISPATCH_THREAD`
- `_DISPATCH_LOCK`
- `_PENDING_ROW_KEYS`
- `_row_dispatch_key(row)`
- `_dispatch_loop()`
- `_drain_all_webhook_results()`
- `_drain_queue_without_processing()`
- `_drain_results_without_callbacks()`
- `_ensure_daily_log_path(event_dt)`

New production code should call the public functions instead of importing
underscored helpers or globals.

## Inputs

### Row Input

Rows are dictionaries produced upstream by parser/runtime/export code.

Required guarantees:

- `outputs.py` must remain schema agnostic.
- `outputs.py` must not add, remove, rename, reinterpret, or validate workbook
  row fields.
- `outputs.py` must not change webhook payload shape.
- Row identity for pending async dispatch is based on a stable JSON rendering of
  the row, not on parser-specific IDs.
- Synchronous posting uses the caller-provided row object.
- Async posting uses a shallow copy of the caller-provided row.

Observed current behavior:

- `_row_dispatch_key(row)` uses `json.dumps(row, sort_keys=True,
  ensure_ascii=False, default=str)`.
- Key generation can stringify values that are not directly JSON serializable,
  but it is not a general validation layer.
- Circular or otherwise unsupported row structures may raise during key
  generation before enqueue.
- Async shallow copying protects against top-level key mutation after submit,
  but nested mutable values remain shared.

### Webhook Configuration Input

`outputs.py` reads configured values from `app/config.py`:

- `WEBHOOK_URL`
- `MATCH_LOGS_ROOT`
- `OUT_FILENAME_PREFIX`

Required guarantees:

- This contract does not authorize changing environment variable names,
  defaults, secret handling, or configuration loading.
- Webhook URL display must go through diagnostics redaction.
- The raw webhook URL must not be written to docs, logs, runtime status,
  failed-post artifacts, local archives, or tests.

### Callback Input

Callbacks are zero-argument callables supplied by orchestrating code.

Observed current behavior:

- Success callbacks are stored on the async job and invoked after a successful
  webhook result is drained.
- Failure callbacks are stored on the async job and invoked after a failed
  webhook result is drained.
- Duplicate pending submissions are not enqueued and their callbacks are not
  registered.
- Reset and no-callback drain helpers discard queued or completed results
  without invoking callbacks.
- Callback exceptions are not caught by `drain_webhook_results()` and can
  propagate to the caller.

Required guarantees:

- Callback invocation must remain tied to drained dispatch results, not to row
  submission or to the dispatcher worker thread.
- Runner-owned state transitions that depend on webhook success must continue
  to happen through success callbacks after dispatch results are drained.

### Local Archive Input

`append_local_jsonl(local_row, event_dt)` accepts:

- `local_row`: an already serialized JSON string for one JSONL row
- `event_dt`: the timestamp used to select the daily archive folder and file

Required guarantees:

- `outputs.py` must not parse, enrich, validate, or rewrite `local_row`.
- Local JSONL archive writing must remain local artifact writing and must not
  become a parser truth source.
- Local raw logs and generated local archives must not be committed.

## Observed Current Behavior

### Webhook Target Display

- `webhook_target_display()` returns `redact_url(WEBHOOK_URL or "")`.
- `webhook_target_display(url)` returns `redact_url(url)` for explicit `url`
  values, including blank or invalid values.
- Redaction and placeholder vocabulary are diagnostics-owned.

### Synchronous Webhook Posting

- When `WEBHOOK_URL` is empty, posting is skipped, a warning is logged, and
  `False` is returned.
- Missing webhook URL does not currently record a failed-post artifact and does
  not mark a webhook failure in runtime diagnostics.
- When `WEBHOOK_URL` is set, `requests.post(WEBHOOK_URL, json=row, timeout=10)`
  is called.
- A successful POST calls `mark_webhook_success(row, attempts=attempt)` and
  returns `True`.
- Success logging is less noisy for these event families:
  - `ActionLogRow`
  - `ParserStatusRow`
  - `DeckSnapshotRow`
  - `CollectionSnapshotRow`
  - `CardPerformanceRow`
- Retryable HTTP status codes are:
  - `408`
  - `425`
  - `429`
  - `500`
  - `502`
  - `503`
  - `504`
- Retryable HTTP failures and `requests.RequestException` failures retry up to
  three total attempts.
- Backoff before retry uses `0.5` seconds before attempt 2 and `1.5` seconds
  before attempt 3.
- Terminal HTTP failure records a failed post with up to the first 500
  characters of response text, marks webhook failure diagnostics, logs the
  failure, and returns `False`.
- Terminal request failure records a failed post, marks webhook failure
  diagnostics, logs the failure, and returns `False`.

### Failed-Post Boundary

- Failed-post artifact writing is delegated to `diagnostics.record_failed_post()`.
- Failed-post record shape, sanitization, traceback capture, and destination
  path are diagnostics-owned.
- `outputs.py` decides when a terminal webhook failure should be reported to
  diagnostics.
- This contract does not authorize changing failed-post schema or committing
  failed-post artifacts.

### Async Dispatcher Lifecycle

- `start_webhook_dispatcher()` starts one daemon thread named
  `manasight-webhook-dispatcher` when no existing dispatcher thread is alive.
- The dispatcher thread reads jobs from `_DISPATCH_QUEUE`.
- A `None` queue item is the stop sentinel.
- For each job, the dispatcher calls `post_row_to_google_sheets(job.row)` and
  puts `WebhookDispatchResult(job=job, success=success)` into
  `_DISPATCH_RESULTS`.
- Queue `task_done()` is called for jobs and sentinels.
- `start_webhook_dispatcher()` updates runtime status as active after starting
  a thread.

### Pending-Row Dedupe

- `submit_row_to_google_sheets()` computes `row_key` before taking the pending
  set lock.
- If `row_key` is already present in `_PENDING_ROW_KEYS`, the function returns
  `False` and does not enqueue a second job.
- If `row_key` is new, the key is added to `_PENDING_ROW_KEYS`, the copied job
  is enqueued, and the function returns `True`.
- Pending keys are removed when completed results are drained, when queued jobs
  are drained without processing, when completed results are drained without
  callbacks, or when runtime state is reset.
- This dedupe is transport pending-work dedupe only. It must not be confused
  with parser match/game identity or workbook row deduplication.

### Result Draining And Callbacks

- `drain_webhook_results(max_items=200)` processes at most `max_items` results.
- It returns the number of results processed.
- It removes each row key from the pending set before invoking that result's
  callback.
- Success callbacks are invoked only for `success=True`.
- Failure callbacks are invoked only for `success=False`.
- No callback is invoked when the matching callback field is `None`.
- Callback exceptions currently propagate to the caller.
- If a callback exception occurs, later queued results may remain undrained
  until a later drain call.

### Stop And Reset

- `stop_webhook_dispatcher(wait_for_queue=True)` waits for the dispatch queue
  to finish before sending the sentinel.
- After a clean stop, it drains all completed results through
  callback-capable draining and marks the dispatcher inactive.
- If no dispatcher thread exists, it still drains completed results and marks
  the dispatcher inactive.
- If the dispatcher thread remains alive after the stop timeout, a warning is
  logged, runtime status remains active, and completed results are not fully
  drained by that call.
- `stop_webhook_dispatcher(wait_for_queue=False)` does not wait for queued work
  before sending the sentinel. FIFO queue order can still allow already queued
  jobs before the sentinel to run.
- `reset_outputs_runtime_state()` calls stop with `wait_for_queue=False`,
  drains queued jobs without processing, drains completed results without
  callbacks, clears pending keys, clears the dispatcher thread reference, and
  marks the dispatcher inactive.

### Local JSONL Archive

- `daily_log_label(event_dt)` formats dates as `"%m_%d_%y"`.
- `_ensure_daily_log_path(event_dt)` creates a daily folder named by that label
  under `MATCH_LOGS_ROOT`.
- The archive filename is
  `f"{OUT_FILENAME_PREFIX}_{daily_log_label(event_dt)}.jsonl"`.
- Runtime state fields `current_log_date` and `current_log_path` cache the
  selected daily path.
- The cached path is reused when the requested daily label matches
  `current_log_date` and `current_log_path` is set.
- `append_local_jsonl()` appends the provided `local_row` string plus a newline,
  using UTF-8 and `ensure_ascii=False` semantics already present in the row
  producer rather than reserializing here.
- File-system errors from local archive writes are not handled inside
  `outputs.py` and may propagate to callers.

## Required Guarantees

### Transport Boundary

- `outputs.py` must remain a transport and local archive module.
- It must not become a parser, extractor, reconciler, workbook-schema owner, or
  Apps Script compatibility layer.
- It must not change parser behavior, parser state final reconciliation,
  parser event classes, match identity, game identity, extractor behavior, or
  deduplication semantics.
- It must not move parser-owned truth into output transport, workbook formulas,
  dashboard logic, Apps Script, webhook delivery, or AI-generated
  interpretation.

### Row Shape Compatibility

- The module must preserve caller-provided row field names and values.
- It must not add transport-only fields to webhook payload rows.
- It must not drop fields before webhook posting.
- It must not normalize event-family, match ID, game ID, winner, deck, card, or
  runtime row values.
- Local JSONL archive input remains caller-serialized; this module must not
  silently rewrite archive row shape.

### Webhook Dispatch Compatibility

- Synchronous `post_row_to_google_sheets()` must continue returning a boolean
  success indicator.
- Terminal webhook failure must continue reporting to diagnostics through
  failed-post capture and failure status updates.
- Retry behavior must be explicit and test-covered if changed.
- A missing webhook URL must remain distinguishable from a terminal HTTP or
  network failure.
- Webhook URL handling must remain secret-safe and redacted in displays.

### Async Dispatch Compatibility

- Async submission must continue to dedupe only currently pending equivalent
  rows.
- Equivalent pending-row detection must remain deterministic for dicts with the
  same keys and values in different insertion orders.
- Callback execution must remain outside the dispatcher thread and tied to
  result draining.
- Queue reset paths must not accidentally mark rows posted, call success
  callbacks, or record parser-state changes.
- Dispatcher lifecycle status must remain visible through runtime diagnostics.

### Local Archive Compatibility

- Daily archive labels must remain stable unless a future contract explicitly
  changes local archive layout.
- Runtime-state path caching must stay compatible with
  `ParserRuntimeState.current_log_date` and `ParserRuntimeState.current_log_path`.
- Local archives remain generated local artifacts and must not be committed.

## Unknowns And Suspected Gaps

- Current focused tests do not appear to cover the missing-webhook-url path.
- Current focused tests do not appear to cover nonretryable HTTP status
  behavior separately from retryable network failures.
- Current focused tests do not appear to cover retryable HTTP failures that
  eventually succeed.
- Current focused tests do not appear to cover response-text truncation for
  failed-post capture.
- Current focused tests do not appear to cover failure callback invocation
  timing.
- Current focused tests do not appear to cover callback exception propagation.
- Current focused tests do not appear to cover nested mutation after async
  shallow copy.
- Current focused tests do not appear to cover duplicate pending submission
  callback registration behavior.
- Current focused tests do not appear to cover dispatcher timeout behavior when
  a thread remains alive after stop.
- Current focused tests do not appear to cover daily archive rollover and
  runtime-state cache reuse in isolation.
- Current reset semantics around `wait_for_queue=False` and FIFO sentinel order
  are subtle. If future work changes reset, tests should distinguish discarding
  queued work from letting already-running work finish.

These gaps are test obligations or review targets. They are not authorization to
change behavior during the contract-writing pass.

## Malformed Input And Error Behavior

- Missing `WEBHOOK_URL` returns `False` from synchronous posting and logs a
  skip warning.
- `requests.HTTPError` is classified by response status code when available.
- `requests.RequestException` is treated as retryable until attempts are
  exhausted.
- Unexpected exceptions from callbacks are not caught by result draining.
- Unexpected exceptions from local archive writes are not caught by
  `append_local_jsonl()`.
- Invalid row structures that cannot be rendered by `_row_dispatch_key()` may
  raise before async enqueue.
- Invalid row structures passed to `requests.post(json=row)` may raise through
  the requests/json stack and should be treated as webhook dispatch failures
  only if current exception handling catches them. Current handling catches
  `requests.RequestException`, not arbitrary serialization exceptions.

Required guarantee:

- Do not silently broaden or hide error behavior without focused tests and an
  updated contract.

## Downstream Consumers

Known direct consumers:

- `app/runner.py`
  - Starts and stops dispatcher lifecycle.
  - Submits match log, match summary, and game log rows.
  - Drains webhook results during runtime and shutdown.
  - Attaches callbacks that mark rows posted only after successful dispatch.
- `app/analytics_sidecar.py`
  - Submits runtime export rows through async dispatch.
- `app/tier_sync.py`
  - Uses synchronous posting for startup snapshot sync when webhook posting is
    enabled.
- Tests
  - `tests/test_app_outputs.py` covers focused output behavior.
  - `tests/test_runner.py` covers runner-owned integration ordering around
    output submission, callbacks, and shutdown.

Compatibility expectation:

- New callers may submit already-built rows, but must not expect `outputs.py`
  to validate schema, infer parser identity, transform rows, or own parser
  truth.

## Protected Surfaces And Non-Goals

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- extractor behavior
- match identity
- game identity
- deduplication semantics
- secrets
- environment variables
- raw logs
- generated data
- runtime status file schema
- failed-post schema
- workbook exports
- issue tracker completion
- pull request targeting to `main`

This contract also does not authorize moving parser-owned truth into output
transport, workbook formulas, dashboard logic, Apps Script, webhook delivery, or
AI-generated interpretation.

## Test Obligations For Module Implementer

Codex C should compare current code and focused tests against this contract
before editing. If behavior already satisfies a requirement, prefer adding only
missing focused tests or documenting the comparison in the implementation
handoff.

Minimum focused validation to consider:

- `webhook_target_display()` redacts configured and explicit webhook URLs.
- Missing webhook URL returns `False` and does not create failed-post artifacts.
- Successful synchronous POST marks webhook success with attempt count.
- Retryable network failures retry and eventually mark success.
- Retryable HTTP failures retry and eventually mark success or terminal
  failure.
- Nonretryable HTTP failures do not retry, record failed posts, mark failure,
  and return `False`.
- Terminal retryable HTTP failure records failed posts with response text
  bounded to the current limit.
- Async submit uses deterministic pending-row dedupe for reordered dict keys.
- Duplicate pending submit returns `False` and does not register duplicate
  callbacks.
- Drained success results clear pending keys and invoke only success callbacks.
- Drained failure results clear pending keys and invoke only failure callbacks.
- Callback invocation occurs only from drain/shutdown result-drain paths.
- Reset clears queues, results, and pending keys without invoking callbacks.
- Stop with `wait_for_queue=True` drains queued work and completed results.
- Daily archive path creation, label formatting, cache reuse, rollover, and
  newline append behavior are covered without committing generated artifacts.
- Dispatcher runtime status flags are updated on start, clean stop, reset, and
  stop timeout paths where feasible.

Suggested commands after implementation:

```bash
python3 -m pytest -q tests/test_app_outputs.py tests/test_runner.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m ruff check src tests
git diff --check
```

## Acceptance Criteria

- The durable contract exists at `docs/contracts/parser_outputs.md`.
- The contract names `outputs.py` as transport/local archive boundary, not a
  truth owner.
- The contract lists public interfaces and observable lifecycle behavior.
- The contract separates observed current behavior from required guarantees.
- The contract protects downstream parser, workbook, webhook payload, Apps
  Script, secrets, environment, raw-log, generated-data, runtime-status,
  failed-post, and workbook-export surfaces.
- The contract names unknowns and suspected coverage gaps without implementing
  behavior changes.
- The contract routes next work to Codex C on
  `codex/parser-module-audit-suite`.

## Next Workflow Action

Next role: Codex C: Module Implementer

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for issue #40 and docs/contracts/parser_outputs.md.

Goal:
Compare the current outputs.py runtime/output transport implementation and focused tests against the parser outputs module contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/40
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_outputs.md
- docs/contracts/parser_runner.md
- docs/contracts/parser_state.md
- src/mythic_edge_parser/app/outputs.py
- src/mythic_edge_parser/app/runner.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/config.py
- src/mythic_edge_parser/app/state.py
- tests/test_app_outputs.py
- tests/test_runner.py
- tests/test_diagnostics.py
- tests/test_status_api.py

Do:
- Compare observed code behavior against the contract before editing.
- Preserve outputs.py as runtime/output transport and local archive plumbing, not parser truth.
- Add focused tests for contracted behavior not currently covered.
- Keep behavior changes minimal and outputs-local unless the contract explicitly requires a downstream integration update.
- Produce docs/implementation_handoffs/parser_outputs_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication semantics, secrets, environment variables, raw logs, generated data, runtime status file schema, failed-post schema, or workbook exports.
- Move parser-owned truth into output transport, workbook formulas, dashboard logic, Apps Script, webhook delivery, or AI-generated interpretation.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/40"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_outputs.md"
  target_artifact: "docs/implementation_handoffs/parser_outputs_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_app_outputs.py tests/test_runner.py tests/test_diagnostics.py tests/test_status_api.py"
    - "python3 -m ruff check src tests"
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication semantics, secrets, environment variables, raw logs, generated data, runtime status file schema, failed-post schema, or workbook exports."
    - "Do not move parser-owned truth into output transport, workbook formulas, dashboard logic, Apps Script, webhook delivery, or AI-generated interpretation."
    - "Do not target main for module PR work."
    - "Do not mark tracker #5 complete."
```
