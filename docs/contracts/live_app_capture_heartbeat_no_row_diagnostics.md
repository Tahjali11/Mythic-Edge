# Live App Capture Heartbeat, No-Row Diagnostics, And Parser Status Blurb Contract

## Module

`live_app_capture_heartbeat_no_row_diagnostics`

Plain English: this contract makes active live capture explain what it has seen so far when no SQLite rows exist yet. It should help the operator tell whether Mythic Edge is listening, seeing structured entries, routing parser events, finding match context, waiting for completed facts, or failing to write SQLite rows, without exposing raw Player.log content.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294
- Current branch: `codex/analytics-foundation`
- Risk tier: High
- Role: Codex B / Module Contract Writer

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- GitHub issue #302
- GitHub issue #294
- GitHub issue #244
- GitHub issue #246
- GitHub issue #297
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/contracts/live_app_watcher_diagnostics.md`
- `docs/contracts/live_app_explicit_start_capture_control.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`

## Owning Layer

Primary owning layer: local app live capture status.

Truth-owning layers remain unchanged:

- MTGA `Player.log` is the raw observable evidence source.
- Parser/state owns event interpretation, match identity, game identity, final reconciliation, and parser-owned match/game facts.
- Analytics ingest owns local SQLite persistence of approved parser-normalized facts.
- SQLite is downstream local analytics storage, not parser truth.
- The frontend displays backend status and does not own capture, match, result, or parser truth.

## Internal Project Area

Local App / Live Player.log Mode.

Adjacent areas:

- Analytics Foundation, because SQLite write attempts and row counts are reported.
- Parser Reliability, because parser event and match context progress are counted.
- Player.log Evidence, reference-only. This contract does not create a second parser or evidence ledger.

## Truth Owner

The new heartbeat, progress counters, no-row labels, and parser status blurb are app-owned operational metadata.

They can say what the live capture supervisor observed about its pipeline, but they do not prove game truth. They must not reinterpret raw events, invent match results, classify gameplay quality, or replace parser-owned final facts.

## Bridge-Code Status

`bridge_code`

Allowed data flow:

```text
live capture supervisor safe milestones
  -> app-owned capture state
  -> GET /api/live/capture/status
  -> frontend read-only display
```

Forbidden reverse flow:

- frontend status must not change parser behavior;
- diagnostics must not rewrite parser-owned facts;
- counters must not drive workbook, webhook, Apps Script, Sheets, AI, coaching, Line Tracer, hidden-card, archetype, or gameplay-advice behavior;
- SQLite row absence must not cause frontend-owned parser inference.

## Files Owned By This Contract

Future implementation may touch:

- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/backend.py`, only if route compatibility needs a narrow update
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- focused backend and frontend tests
- `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md`

This contract itself owns:

- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`

## Observed Current Behavior

- `GET /api/live/capture/status` exists and returns `mythic_edge_local_app_live_capture_status`.
- `POST /api/live/capture/start` and `POST /api/live/capture/stop` exist under the explicit operator control contract.
- `build_live_capture_status(...)` reports high-level capture state such as `ready_to_start`, `starting`, `capturing`, `stopped`, `blocked`, `failed`, and `stale`.
- The current active-capture warning `waiting_for_events` is broad.
- The current state can say `parser_runner_started`, `tailing_started`, and `sqlite_live_writes_enabled`.
- The current status cannot reliably explain whether capture saw log activity, structured entries, parser events, match ids, completed rows, or SQLite write attempts.
- The frontend already has a place to display a backend-led capture blurb, but the backend must own the blurb contents.
- Issue #294 is separate and should refresh analytics views after rows exist. It cannot explain why no rows exist.

## Contract Decision

Issue #302 should extend the existing `GET /api/live/capture/status` response additively.

Do not add a new route for the first slice. `docs/contracts/live_app_watcher_diagnostics.md` already owns the broader watcher diagnostics route. Issue #302 is narrower: it describes progress inside a running or recently running capture session.

Approved first-slice additions to `GET /api/live/capture/status`:

- top-level `heartbeat`;
- top-level `progress`;
- top-level `parser_status_blurb`;
- more specific no-row labels in `progress.last_no_write_reason`;
- safe warnings/errors that continue to use stable lowercase labels.

The top-level live capture status object and existing route must remain backward-compatible.

## Public Interface

### Existing Route To Extend

```text
GET /api/live/capture/status
```

The route must remain read-only. It must not create app-data directories, create SQLite files, start capture, stop capture, tail Player.log, run migrations, import facts, or write diagnostics from a GET request.

### Top-Level Response Shape

The extended response keeps the existing top-level object:

```json
{
  "object": "mythic_edge_local_app_live_capture_status",
  "schema_version": "live_app_explicit_start_capture_control.v1",
  "status": "capturing",
  "mode": "explicit_operator_control",
  "capture": {},
  "preconditions": [],
  "state": {},
  "last_result": null,
  "heartbeat": {},
  "progress": {},
  "parser_status_blurb": {},
  "warnings": [],
  "errors": []
}
```

The nested heartbeat and progress objects must each use:

```text
schema_version = live_app_capture_heartbeat_no_row_diagnostics.v1
```

This nested version avoids breaking the existing #297 capture-control schema while making the new diagnostics contract explicit.

## Heartbeat Contract

`heartbeat` is app-owned operational status for the capture supervisor.

Required shape:

```json
{
  "schema_version": "live_app_capture_heartbeat_no_row_diagnostics.v1",
  "status": "waiting",
  "heartbeat_updated_at": "2026-06-08T12:00:00Z",
  "capture_duration_seconds": 12,
  "heartbeat_age_seconds": 1,
  "stale_after_seconds": 30
}
```

Allowed `heartbeat.status` values:

- `not_started`
- `starting`
- `waiting`
- `progress`
- `rows_written`
- `blocked`
- `failed`
- `stale`
- `unknown`

Required heartbeat rules:

- While capture is `starting` or `capturing`, the supervisor should update `heartbeat_updated_at` at least every 10 seconds when the loop is alive, including while waiting for events.
- `stale_after_seconds` should default to 30 seconds unless implementation evidence proves another value safer.
- `heartbeat_age_seconds` is computed by the backend from safe timestamps.
- Healthy waiting is not stale while `heartbeat_age_seconds <= stale_after_seconds`.
- `capture_state_stale` remains the broader app-owned state/ownership stale label from #297. It is distinct from heartbeat freshness.
- Heartbeat fields must not include raw log lines, raw paths, raw hashes, process command lines, stack traces, SQL text, secrets, or environment values.

## Progress Counter Contract

`progress` is app-owned milestone evidence. It may count safe milestones observed by the local capture supervisor. It must not expose event payloads.

Required shape:

```json
{
  "schema_version": "live_app_capture_heartbeat_no_row_diagnostics.v1",
  "log_poll_count": 4,
  "log_chunks_seen": 0,
  "structured_entry_count": 2,
  "parser_event_count": 1,
  "parser_event_kinds_seen": ["game_state"],
  "match_ids_seen_count": 1,
  "current_match_detected": true,
  "current_match_game_wins": null,
  "current_match_game_losses": null,
  "last_completed_match_result": null,
  "last_completed_match_game_wins": null,
  "last_completed_match_game_losses": null,
  "completed_game_rows_seen": 0,
  "sqlite_write_attempt_count": 0,
  "sqlite_rows_written": 0,
  "last_no_write_reason": "no_completed_game_rows",
  "last_event_seen_at": "2026-06-08T12:00:00Z",
  "last_sqlite_write_at": null
}
```

Required field types:

- `log_poll_count`: non-negative integer.
- `log_chunks_seen`: non-negative integer.
- `structured_entry_count`: non-negative integer.
- `parser_event_count`: non-negative integer.
- `parser_event_kinds_seen`: list of safe lowercase labels, not raw class names when unsafe.
- `match_ids_seen_count`: non-negative integer.
- `current_match_detected`: boolean.
- `current_match_game_wins`: non-negative integer or `null`.
- `current_match_game_losses`: non-negative integer or `null`.
- `last_completed_match_result`: safe label or `null`.
- `last_completed_match_game_wins`: non-negative integer or `null`.
- `last_completed_match_game_losses`: non-negative integer or `null`.
- `completed_game_rows_seen`: non-negative integer.
- `sqlite_write_attempt_count`: non-negative integer.
- `sqlite_rows_written`: non-negative integer.
- `last_no_write_reason`: allowed no-row reason or `null`.
- `last_event_seen_at`: ISO-8601 timestamp or `null`.
- `last_sqlite_write_at`: ISO-8601 timestamp or `null`.

Required progress rules:

- Counters should be monotonic within a capture session unless the supervisor restarts and clearly starts a new app-owned session.
- `parser_event_kinds_seen` must use safe labels only. It must not include raw event payloads.
- `current_match_game_wins` and `current_match_game_losses` may be non-null only when parser/state has already supplied safe current match summary data. If unavailable, use `null`.
- `last_completed_match_result` may be non-null only after parser-owned completed match facts exist. It must not be inferred by the frontend or by elapsed time.
- `sqlite_write_attempt_count` must increment only when the live capture path calls the approved #244 SQLite ingest boundary.
- `sqlite_rows_written` must count rows reported by approved SQLite ingest results, not direct frontend or UI guesses.

## No-Row Reason Vocabulary

Allowed `last_no_write_reason` labels:

- `not_started`
- `no_log_bytes_seen`
- `no_log_chunks_seen`
- `no_structured_entries_seen`
- `no_parser_events_routed`
- `no_match_id_seen`
- `no_completed_game_rows`
- `match_row_not_ready`
- `sqlite_ingest_not_attempted`
- `sqlite_write_failed`
- `capture_stopped_before_completion`
- `capture_state_stale`
- `rows_written`
- `unknown`

Reason rules:

- `no_log_bytes_seen` or `no_log_chunks_seen` means the capture loop has not observed new log activity at the safe milestone level. It must not expose byte contents.
- `no_structured_entries_seen` means log activity did not become structured MTGA entries.
- `no_parser_events_routed` means structured entries did not become parser events routed into the state update path.
- `no_match_id_seen` means parser context has not exposed a match id to the capture loop.
- `no_completed_game_rows` means match context exists but no completed game rows are ready to write.
- `match_row_not_ready` means game rows may exist but final/reconciled match row output is not ready.
- `sqlite_ingest_not_attempted` means no approved #244 ingest call has occurred.
- `sqlite_write_failed` means an approved ingest call was attempted and failed.
- `capture_stopped_before_completion` means capture stopped before completed facts were available.
- `capture_state_stale` means app-owned capture state or heartbeat is stale.
- `rows_written` means the no-row condition has ended.

The existing broad `waiting_for_events` warning may remain for compatibility, but Codex C should add a more specific `last_no_write_reason` whenever possible.

## Brief Parser Status Blurb Contract

`parser_status_blurb` is a backend-led display hint. It lets the UI show one short line without making the frontend infer parser or match truth.

Required shape:

```json
{
  "code": "waiting_for_completed_facts",
  "text": "Capturing; waiting for completed match facts.",
  "tone": "waiting"
}
```

Allowed `code` values:

- `not_configured`
- `ready_to_start`
- `starting`
- `listening_for_events`
- `waiting_for_next_match`
- `current_match_detected`
- `waiting_for_completed_facts`
- `most_recent_match_completed`
- `needs_review_no_parser_events`
- `sqlite_write_failed`
- `capture_state_stale`
- `stopped`
- `unknown`

Allowed `tone` values:

- `neutral`
- `waiting`
- `ok`
- `warning`
- `error`

Approved text examples:

- `Configure Player.log to start capture.`
- `Ready to start capture.`
- `Listening for Player.log events.`
- `Waiting for next match.`
- `Recording current match.`
- `Capturing; waiting for completed match facts.`
- `Most recent completed match was recorded.`
- `Capture needs review. No parser events seen yet.`
- `Capture heartbeat stopped. Restart capture.`
- `SQLite write failed. Review diagnostics.`

Blurb rules:

- The backend owns `code`, `text`, and `tone`.
- The frontend may render the text, but must not derive its own score or match-result copy from counters.
- Do not say `MTGA is open` unless Mythic Edge has an explicit, safe MTGA process signal.
- Do not show fake scores or placeholders.
- Current match score text is allowed only when parser/state provides safe current match game-win/game-loss values.
- Completed match result text is allowed only when parser-owned completed match facts exist.
- Detailed counters belong in diagnostics/details, not in the main blurb.

## Backend Responsibility Boundary

The backend may:

- update app-owned heartbeat/progress metadata while the capture supervisor is alive;
- write sanitized heartbeat/progress metadata into the existing app-data-root-scoped capture state file;
- expose heartbeat, progress, and parser status blurb through `GET /api/live/capture/status`;
- count safe milestones such as polls, structured entries, parser events, match ids, completed rows, write attempts, and rows written;
- retain existing start/stop behavior from #297;
- call the approved #244 SQLite live ingest path only from the running capture supervisor, not from GET status routes.

The backend must not:

- read, copy, print, hash, store, or expose raw Player.log content;
- store raw Player.log payloads or raw log lines in SQLite;
- expose raw event payloads, raw JSONL, raw hashes, private paths, SQL text, stack traces, secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs, or environment values;
- change parser behavior, parser event classes, parser state final reconciliation, match/game identity, or deduplication;
- write analytics schema or migration changes;
- start Google Sheets, webhook, Apps Script, workbook, output transport, production, OpenAI, AI, coaching, or Line Tracer behavior;
- add destructive controls or arbitrary SQL/database browsing.

## Frontend Responsibility Boundary

The frontend may:

- validate the nested heartbeat/progress/blurb response shapes;
- render one compact backend-led parser status blurb in the Live Capture Control area;
- optionally render sanitized counters in a details area;
- distinguish active capture from rows written;
- show `Needs review`, `Waiting`, `Stale`, or `Failed` based on backend labels;
- keep existing start/stop controls governed by backend `start_allowed` and `stop_allowed`.

The frontend must not:

- infer match result truth from timers, counters, UI state, or local storage;
- generate its own current match score text;
- claim MTGA process detection without backend evidence;
- browse SQLite or run SQL;
- expose raw Player.log content, raw JSONL, private paths, raw hashes, local artifacts, secrets, or generated database contents;
- present diagnostics as gameplay advice, strategic quality, archetype inference, hidden-card inference, player-mistake labels, Line Tracer, or coaching truth.

## App-Data And State-File Boundary

This issue may extend the existing app-owned live capture state file with sanitized heartbeat/progress metadata.

Allowed app-data content:

- safe labels;
- non-negative integer counters;
- booleans;
- ISO timestamps;
- parser-status blurb code/text/tone after sanitization;
- approved warning/error labels.

Forbidden app-data content:

- raw Player.log lines;
- raw structured entries;
- raw parser event payloads;
- raw private paths;
- raw hashes derived from private content;
- SQL text;
- stack traces;
- secrets or environment values.

GET `/api/live/capture/status` must remain read-only. It may compute age and stale labels from existing safe state, but it must not create or update the state file.

## Relationship To Issue #294

Issue #294 handles frontend auto-refresh after SQLite analytics rows exist.

Issue #302 handles explaining why rows may not exist yet.

Codex C must not implement #294 polling, refresh-state endpoints, analytics auto-refresh, or dashboard refresh behavior in this slice.

## Relationship To Issue #246

Issue #246 owns the broader read-only watcher diagnostics surface.

Issue #302 owns active capture progress and no-row diagnostics for the existing `/api/live/capture/status` control surface.

Codex C should not move #302 fields into `GET /api/live/watcher/diagnostics` unless the contract is amended.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match identity;
- game identity;
- deduplication;
- analytics schema or migrations;
- #244 live capture semantics beyond additive app-owned progress metadata;
- #297 start/stop route semantics beyond additive status fields;
- #294 analytics refresh behavior;
- manual JSONL import semantics;
- replay ingest semantics;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- secrets, credentials, environment variables, API keys, tokens, webhook URLs, spreadsheet IDs, or deployment IDs.

## Unknowns

- Whether the current live capture supervisor can observe `log_chunks_seen` directly through `MtgaEventStream`, or whether it should report `0`/`unknown` until a safe upstream signal exists.
- Whether parser event kind labels should come from event classes, existing event metadata, or a small safe mapping. Raw payloads remain forbidden either way.
- Whether current match game-win/game-loss data is safely available during active capture. If not, those fields should remain `null`.
- Whether a future #302 implementation should keep all fields in the state file or derive some from in-memory supervisor state.
- Whether the existing narrow #302-shaped frontend tests reflect the final desired UI placement.

## Suspected Gaps

- Current status uses broad `waiting_for_events` rather than a precise no-row reason.
- Current state tracks `started_at` and `updated_at`, but not a distinct heartbeat object.
- Current capture loop may update state only when starting, writing rows, failing, or stopping, which can become stale during healthy waiting.
- Current status does not count structured entries, parser events, match ids, completed rows, or SQLite write attempts.
- Current frontend may accept a backend blurb, but backend does not yet produce the contracted blurb.
- Current code may not validate heartbeat/progress nested shapes as strictly as warning/error labels.

## Tests Required

Codex C should add or update focused backend tests for:

- capture status includes heartbeat/progress schema version when capture state includes safe diagnostics;
- heartbeat stays healthy while the supervisor is alive and waiting;
- stale heartbeat differs from healthy waiting;
- `last_no_write_reason` covers no-event, no-parser-event, no-match-id, no-completed-row, ingest-not-attempted, write-failed, stopped-before-completion, and state-stale cases where safely mockable;
- unsafe heartbeat/progress timestamps, labels, text, raw paths, URLs, raw hashes, SQL, stack traces, and private content are redacted or rejected;
- GET `/api/live/capture/status` remains read-only and does not create app-data files or SQLite files;
- start/stop behavior from #297 remains compatible;
- no Google Sheets/webhook/App Script/output transport behavior starts;
- raw Player.log test content is not returned.

Codex C should add or update focused frontend tests for:

- API validation accepts the contracted heartbeat/progress/blurb shape;
- API validation rejects unsafe blurb text and unsafe timestamps;
- frontend renders backend-led blurb text;
- frontend does not invent current match score or result text;
- frontend keeps start/stop visibility tied to backend control flags;
- malformed status payload fails closed.

Recommended validation commands:

```powershell
py -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_analytics_local_app_backend.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
py -m ruff check src tests tools
git diff --check
py tools/check_agent_docs.py
@'
docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md
docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md
'@ | py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md
docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md
'@ | py tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If frontend build is run and creates `frontend/dist`, Codex C must remove that generated output before handoff unless a later contract explicitly authorizes committing it.

## Acceptance Criteria

- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md` exists.
- Contract keeps #302 separate from #294 auto-refresh.
- Contract extends existing `GET /api/live/capture/status` additively.
- Heartbeat semantics are defined.
- Sanitized progress counters are defined.
- No-row reason vocabulary is defined.
- Backend-led parser status blurb is defined.
- Backend and frontend boundaries are explicit.
- Raw Player.log and private artifact boundaries are explicit.
- Validation expectations and Codex C handoff are included.
- No implementation code is changed by Codex B.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #302.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/302

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md

Goal:
Compare current live capture status/control code to the contract, then implement only the additive #302 heartbeat/progress/no-row diagnostics and backend-led parser status blurb. Keep #294 analytics auto-refresh separate.

Before editing:
- Confirm branch and git status.
- Identify unrelated dirty files and preserve them.
- Read issue #302, issue #294, the contract, live capture control/status code, watcher diagnostics, stream/tailer boundaries, analytics ingest, frontend API/types/App/tests, and focused backend tests.
- State what the #302 diagnostics are supposed to do, what current code already does, what gaps remain, and the exact minimal implementation plan.

Do:
- Extend existing GET /api/live/capture/status additively with heartbeat, progress, and parser_status_blurb.
- Keep heartbeat/progress as app-owned operational metadata, not parser truth.
- Use only sanitized counters, booleans, timestamps, and labels.
- Keep GET status read-only.
- Keep start/stop controls governed by existing backend flags.
- Add focused backend/frontend tests.
- Produce docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md.

Do not:
- Implement issue #294 analytics auto-refresh in this slice.
- Move #302 into the broader /api/live/watcher/diagnostics route unless routed back to Codex B.
- Read, copy, print, hash, store, or expose raw Player.log content.
- Store raw Player.log payloads or raw log lines in SQLite.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations, workbook/webhook/App Script/Sheets/output transport/production/OpenAI/AI/coaching behavior.
- Add arbitrary SQL, destructive controls, hidden-card inference, archetype inference, player-mistake labels, Line Tracer, or gameplay advice.
- Target main.

Validation:
py -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_analytics_local_app_backend.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
py -m ruff check src tests tools
git diff --check
py tools/check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.

Final output must include:
- role performed
- issue and contract used
- branch and git status
- comparison summary
- files changed
- tests changed
- validation run
- protected-surface status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/302"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #302"
  contract_artifact: "docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md"
  target_artifact: "docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  decision: "Extend existing /api/live/capture/status additively with app-owned heartbeat/progress diagnostics, no-row reason labels, and one backend-led parser/capture blurb. Keep #294 auto-refresh separate."
  stop_conditions:
    - "Do not implement issue #294 auto-refresh in this slice."
    - "Do not read, copy, hash, store, print, or expose raw Player.log content."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
