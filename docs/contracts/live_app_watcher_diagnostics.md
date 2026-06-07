# Live App Watcher Diagnostics Contract

## Module

`live_app_watcher_diagnostics`

Plain English: this contract defines a safe local-app diagnostics surface that
answers, "Can I trust live capture right now, and what should I review?" It
does this with sanitized labels and counters, not raw Player.log content.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/246
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Branch: `codex/analytics-foundation`
- Risk tier: High

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- GitHub issue `#246`
- GitHub tracker `#204`
- GitHub umbrella issue `#207`
- GitHub issue `#240` / PR `#241`
- GitHub issue `#242` / PR `#243`
- GitHub issue `#244` / PR `#245`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`
- `tests/test_tailer.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_evidence_runtime_status.py`

## Owning Layer

Primary owning layer: local app live-mode status and diagnostics.

Truth-owning layers remain unchanged:

- MTGA `Player.log` is the raw observable evidence source.
- Parser/state owns event interpretation and parser-managed facts.
- Evidence-ledger and parser diagnostics modules own evidence/provenance and
  drift-health reports when those reports already exist.
- Local app diagnostics owns only safe composition and display of status labels.

## Internal Project Area

Local App / Live Player.log Mode.

Adjacent areas:

- Parser Reliability / Diagnostics, reference-only for this contract.
- Player.log Evidence Ledger, reference-only unless sanitized health objects are
  already available.
- Analytics Foundation, read-only status consumer of #244 live capture metadata.

## Truth Owner

The diagnostics response does not own parser truth, evidence truth, analytics
truth, workbook truth, or AI truth. It is a local status summary composed from
already-authorized surfaces.

The diagnostics response may say that a signal is `observed`, `metadata_only`,
`deferred`, `unsupported`, `expected_but_unavailable`, `not_checked`, or
`unknown`. It must not promote one of those labels into game truth.

## Bridge-Code Status

`bridge_code`

Allowed data flow:

```text
local app metadata/status surfaces
  -> live diagnostics response
  -> frontend read-only display
```

Allowed reference flow:

```text
already-sanitized parser/evidence diagnostics
  -> live diagnostics response
```

Forbidden reverse flow:

- frontend diagnostics must not change parser behavior;
- diagnostics must not rewrite parser-owned facts;
- diagnostics must not trigger watcher start/stop;
- diagnostics must not trigger raw Player.log reads;
- diagnostics must not write analytics rows, runtime files, workbook rows, or
  webhook payloads.

## Files Owned By This Contract

Future implementation may touch:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- a new local-app diagnostics helper, if Codex C chooses one;
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.tsx`
- `frontend/src/status.ts`
- focused local app/frontend tests.

This contract itself owns:

- `docs/contracts/live_app_watcher_diagnostics.md`

## Observed Current Behavior

### Live Player.log Metadata Status

`build_live_player_log_status(paths)` currently returns sanitized metadata-only
status for a configured or default Player.log candidate.

Observed safe labels include:

- `readability_not_probed`
- `rotation_detection_deferred`
- `truncation_detection_deferred`
- `permission_denied`
- `metadata_unavailable`
- `not_file`
- `stale`

Observed guarantees:

- Player.log contents are not read.
- `contents_read` is false.
- `tailing_started` is false.
- Display paths are symbolic, such as `<configured_player_log>` or
  `<detected_mtga_player_log>`.

### Watcher Readiness Status

`build_live_watcher_status(paths)` composes Player.log readiness into a
readiness-only watcher status.

Observed guarantees:

- `mode = "readiness_only"`
- `running = false`
- `start_allowed = false`
- `stop_allowed = false`
- `parser_runner_started = false`
- `tailing_started = false`
- `sqlite_live_writes_enabled = false`

### Watcher Process-Control Safeguards

`build_live_watcher_process_status(paths)` reports process-control safeguards
through `GET /api/live/watcher/process`.

Observed safe inputs:

- sanitized Player.log status;
- synthetic or app-owned watcher state file metadata when present;
- app-data path availability;
- process-control precondition labels.

Observed guarantees:

- start/stop controls remain disabled;
- parser runner is not started;
- tailer is not started;
- external transport remains disabled;
- app-owned process state is reported, not cleaned or repaired.

### Live SQLite Capture Status

`GET /api/live/ingest/status` currently reports live SQLite capture readiness
and capability metadata.

Observed guarantees:

- status route is read-only;
- source kind is `live_parser`;
- final match/game fact capture is supported;
- provisional/gameplay/opponent-observation/field-evidence live capture remains
  unsupported or deferred;
- raw Player.log storage is unsupported;
- external transport is not allowed.

`analytics_ingest.ingest_live_parser_owned_facts(...)` now accepts final or
reconciled parser-owned match/game rows and reports sanitized warnings/skipped
counts for deferred live fact families.

### Tailer, Stream, Parser Diagnostics, And Evidence Runtime Status

`FileTailer` can detect rotation after polling a file, and `MtgaEventStream` can
publish `LogFileRotatedEvent` when a running stream observes rotation.

`parser_diagnostics.py`, `log_drift_sensor.py`, and
`evidence_runtime_status.py` can produce useful parser/evidence health reports,
but some of those functions read logs or write reports when directly invoked.

Therefore the local app diagnostics route must not call those raw-log/report
generation paths from a GET request. It may reference already-sanitized reports
only when they are already available from an authorized upstream surface.

## Contract Decision

Issue `#246` should define a read-only live diagnostics/status layer.

Approved first slice:

- add or define `GET /api/live/watcher/diagnostics`;
- compose existing sanitized live Player.log status, watcher readiness, watcher
  process safeguards, and live ingest status;
- optionally include already-sanitized parser/evidence diagnostics summaries
  when they are already available without reading raw logs or creating files;
- render a frontend read-only diagnostics summary;
- keep all diagnostics as labels, counters, and booleans;
- preserve #244 live capture semantics.

Not approved for issue `#246`:

- tailing, reading, copying, hashing, or storing raw Player.log content;
- starting, stopping, restarting, killing, repairing, or clearing a watcher;
- creating diagnostics files, runtime status files, logs, SQLite files, or
  app-data artifacts from GET routes;
- adding analytics schema/migration changes;
- changing parser behavior or final reconciliation;
- adding remediation/destructive UI controls.

## Public Interface

### Backend Route

Codex C should add exactly one read-only backend route:

```text
GET /api/live/watcher/diagnostics
```

The route must use the existing local app FastAPI loopback/CORS boundary.

The route must not add:

```text
POST /api/live/watcher/*
PUT /api/live/watcher/*
PATCH /api/live/watcher/*
DELETE /api/live/watcher/*
```

### Backend Helper

Codex C may add a helper equivalent to:

```python
build_live_watcher_diagnostics_status(paths) -> dict[str, object]
```

Allowed composed inputs:

- `build_live_player_log_status(paths)`
- `build_live_watcher_status(paths)`
- `build_live_watcher_process_status(paths)`
- `build_live_sqlite_capture_status(paths)`
- already-sanitized parser/evidence health objects, only if supplied by an
  authorized existing source without reading raw logs or writing report files

Forbidden helper calls from this route:

- `runner.main(...)`
- `MtgaEventStream.start(...)`
- `FileTailer.open_from_start(...)`
- `FileTailer.open_from_end(...)`
- `FileTailer.poll(...)`
- `FileTailer.poll_once(...)`
- `parser_diagnostics.build_parser_diagnostics_report(...)` against a live or
  private log path
- `parser_diagnostics.write_parser_diagnostics_report(...)`
- `log_drift_sensor.build_player_log_drift_report(...)` against a live or
  private log path
- `log_drift_sensor.write_player_log_drift_report(...)`

### Response Shape

`GET /api/live/watcher/diagnostics` must return a JSON object with:

```json
{
  "object": "mythic_edge_local_app_live_watcher_diagnostics",
  "schema_version": "live_app_watcher_diagnostics.v1",
  "status": "degraded",
  "mode": "read_only_composition",
  "summary": {
    "info_count": 0,
    "warning_count": 0,
    "degraded_count": 0,
    "error_count": 0,
    "blocked_count": 0,
    "unknown_count": 0
  },
  "diagnostics": [],
  "sources": {},
  "privacy": {
    "raw_player_log_content_included": false,
    "raw_player_log_path_included": false,
    "raw_hashes_included": false,
    "raw_sql_included": false,
    "stack_traces_included": false,
    "secrets_or_environment_values_included": false
  },
  "capabilities": {
    "read_only": true,
    "starts_watcher": false,
    "stops_watcher": false,
    "tails_player_log": false,
    "writes_sqlite": false,
    "writes_diagnostics_files": false,
    "external_transport_allowed": false
  },
  "warnings": [],
  "errors": []
}
```

Required top-level fields:

- `object`
- `schema_version`
- `status`
- `mode`
- `summary`
- `diagnostics`
- `sources`
- `privacy`
- `capabilities`
- `warnings`
- `errors`

The route may include `generated_at` if it is useful, but `generated_at` must not
be treated as proof of live watcher activity.

## Status And Severity Vocabulary

Approved top-level statuses:

- `ok`: no warning, degraded, error, blocked, or unknown diagnostics were found.
- `degraded`: at least one warning/degraded diagnostic exists, but the app can
  still report useful status.
- `blocked`: a required precondition prevents safe live capture or reliable
  diagnostics.
- `unavailable`: required local app state is unavailable.
- `unknown`: diagnostics cannot be classified safely.

Approved per-diagnostic severity values:

- `info`
- `warning`
- `degraded`
- `error`
- `blocked`

Approved evidence availability labels:

- `observed`
- `metadata_only`
- `deferred`
- `unsupported`
- `expected_but_unavailable`
- `not_checked`
- `unknown`

Top-level status rules:

- Any `blocked` diagnostic should make top-level status `blocked`.
- Any `error` diagnostic should make top-level status `blocked` unless it is
  explicitly non-blocking.
- Any `warning` or `degraded` diagnostic should make top-level status
  `degraded` unless a blocking diagnostic is present.
- If required source payloads are missing or malformed, top-level status should
  be `unknown` or `unavailable`.
- `info` diagnostics alone should not degrade the top-level status.

## Diagnostic Entry Shape

Each diagnostic entry must have:

- `category`: approved category string;
- `key`: stable safe diagnostic key;
- `severity`: approved severity;
- `status`: safe status label;
- `evidence_availability`: approved evidence-availability label;
- `source`: source surface key;
- `message`: short safe user-facing explanation;
- `count`: non-negative integer or `null`;
- `review_required`: boolean.

Each diagnostic entry must not include:

- raw Player.log lines;
- raw saved-event lines;
- raw hashes derived from private content;
- private absolute paths;
- local usernames;
- command lines;
- SQL text;
- stack traces;
- secrets;
- environment values;
- generated artifact paths beyond approved symbolic display values.

## Diagnostic Categories

### `player_log_metadata`

Allowed source:

- `build_live_player_log_status(paths)`

Allowed labels:

- `player_log_missing`
- `player_log_stale`
- `player_log_not_file`
- `player_log_unreadable`
- `player_log_metadata_unavailable`
- `player_log_metadata_denied`
- `readability_not_probed`
- `rotation_detection_deferred`
- `truncation_detection_deferred`

Required behavior:

- Confirmed metadata-only labels must use `evidence_availability =
  "metadata_only"`.
- Deferred rotation/truncation/readability checks must use
  `evidence_availability = "deferred"` or `not_checked`.
- The route must not convert deferred detection into confirmed `rotated` or
  `truncated`.

### `watcher_readiness`

Allowed source:

- `build_live_watcher_status(paths)`

Allowed labels:

- `watcher_ready`
- `watcher_not_configured`
- `watcher_blocked_missing_log`
- `watcher_blocked_unreadable_log`
- `watcher_blocked_invalid_config`
- `watcher_deferred`
- `watcher_unavailable`

Required behavior:

- Readiness must not imply live capture is running.
- `running` must remain false unless a later contract authorizes a supervised
  running watcher.

### `watcher_process`

Allowed source:

- `build_live_watcher_process_status(paths)`

Allowed labels:

- `watcher_state_missing`
- `watcher_state_malformed`
- `watcher_state_stale`
- `watcher_state_not_file`
- `single_instance_guard_deferred`
- `supervisor_target_deferred`
- `frontend_controls_not_authorized`
- `watcher_process_control_deferred`

Required behavior:

- Stale/malformed process state must be reported, not repaired.
- A PID in state must not be treated as process ownership proof.
- No process may be started, stopped, inspected, killed, or signaled.

### `live_capture`

Allowed source:

- `build_live_sqlite_capture_status(paths)`
- result metadata from `ingest_live_parser_owned_facts(...)` only when already
  supplied by an authorized caller and already sanitized

Allowed labels:

- `live_sqlite_capture_status_only`
- `final_match_game_fact_capture_supported`
- `provisional_fact_capture_unsupported`
- `gameplay_action_live_capture_deferred`
- `opponent_observation_live_capture_deferred`
- `field_evidence_live_capture_deferred`
- `live_capture_warning`
- `live_capture_skipped_rows`

Required behavior:

- Diagnostics may report warnings/skipped counts from #244 live capture results.
- Diagnostics must not write SQLite from a GET request.
- Diagnostics must not reinterpret skipped rows as parser failures unless #244
  result metadata says the write failed.
- Diagnostics must preserve the #244 boundary: final/reconciled match/game facts
  only.

### `tailer_event_bridge`

Allowed source:

- already-authorized watcher/tailer event summaries, if a future caller supplies
  them in sanitized form

Allowed labels:

- `rotation_detection_deferred`
- `truncation_detection_deferred`
- `duplication_detection_deferred`
- `rotation_observed`
- `truncation_observed`
- `duplication_suspected`

Required behavior for issue `#246`:

- The diagnostics route must normally report rotation/truncation/duplication as
  deferred or unavailable.
- It must not call the tailer or stream to confirm those states.
- `rotation_observed`, `truncation_observed`, and `duplication_suspected` may
  appear only if already supplied by an authorized sanitized upstream surface.

### `parser_evidence`

Allowed source:

- already-sanitized parser diagnostics report summaries;
- already-sanitized evidence-ledger runtime health summaries;
- already-sanitized runtime field evidence summaries.

Allowed labels:

- `parser_diagnostics_unavailable`
- `evidence_ledger_health_unavailable`
- `unknown_entries`
- `truncation_count`
- `drift_flags`
- `degraded_evidence`
- `review_required`

Required behavior:

- The route must not generate parser diagnostics against a live/private
  Player.log path.
- The route must not expose raw hashes from data-loss events.
- Parser/evidence health must remain advisory diagnostics and must not change
  local app live capture state.

### `privacy_boundary`

Required labels:

- `raw_player_log_content_excluded`
- `raw_player_log_path_excluded`
- `raw_hashes_excluded`
- `external_transport_disabled`
- `destructive_controls_absent`

Required behavior:

- The response should explicitly expose privacy/capability booleans so reviewers
  can assert the boundary.
- If any privacy boolean would be true, the route must fail closed and return a
  sanitized `privacy_boundary_failed` error rather than returning unsafe data.

## Sources Object

The `sources` object must summarize which source surfaces were used. It should
use stable keys:

- `player_log_status`
- `watcher_status`
- `watcher_process_status`
- `live_ingest_status`
- `tailer_event_bridge`
- `parser_diagnostics`
- `evidence_runtime_health`

Each source summary should include:

- `supplied`: boolean;
- `status`: safe status string;
- `schema_version`: string or `null`;
- `evidence_availability`: approved evidence label;
- `limitations`: list of safe labels.

The `sources` object must not inline full raw source payloads if that would
include private paths, raw hashes, stack traces, SQL text, or local artifacts.

## Backend Contract

The backend may:

- add `GET /api/live/watcher/diagnostics`;
- compose existing sanitized local app status builders;
- classify safe labels into category/severity/status;
- include symbolic display paths already allowed by previous contracts;
- include sanitized warning/error codes;
- include counts from already-sanitized live ingest result metadata if supplied;
- include already-sanitized parser/evidence summaries if already available.

The backend must not:

- call runner, stream, or tailer startup;
- read, copy, hash, tail, or store raw Player.log content;
- call parser diagnostics builders against live/private logs from GET routes;
- create diagnostics files, runtime status files, logs, SQLite files, WAL/SHM
  files, journal files, app-data state files, or generated artifacts from GET
  routes;
- mutate local app config;
- repair/delete/clear stale watcher state;
- expose raw PIDs as ownership proof;
- expose raw absolute paths, command lines, environment values, secrets, SQL
  text, stack traces, raw hashes, or private artifact names;
- enable external transport.

## Frontend Contract

The frontend may:

- add a typed API reader for `GET /api/live/watcher/diagnostics`;
- add TypeScript types for the diagnostics response;
- render a read-only Live Diagnostics panel;
- group diagnostics by category and severity;
- render safe messages and review-required flags;
- use existing `statusTone(...)` and `safeDisplayValue(...)` protections;
- fail closed on malformed or unsupported response shapes.

The frontend must not:

- add start, stop, restart, clear, delete, repair, reset, or force controls;
- expose arbitrary SQL or database browsing;
- display raw Player.log lines, raw hashes, raw paths, local usernames, stack
  traces, secrets, environment values, generated artifact names, or local-only
  file paths;
- present diagnostics as coaching, Line Tracer, archetype inference, hidden-card
  inference, player-mistake labels, or best-line truth.

## SQLite, App-Data, And Runtime-Status Boundary

The first implementation must be API-only/read-only composition.

It must not:

- add SQLite schema tables;
- add migrations;
- write diagnostics into SQLite;
- create app-data diagnostics files;
- create runtime status files;
- create logs;
- create watcher state files;
- create import jobs;
- create generated frontend build output as a committed artifact.

If Codex C finds persistence is required, stop and route back to Codex B for a
separate storage/schema contract.

## Error Behavior

Malformed composed source payload:

- fail closed with top-level `status = "unknown"` or `blocked`;
- include a sanitized error code such as `source_payload_malformed`;
- do not return unsafe source payload content.

Missing source payload:

- report `expected_but_unavailable` or `not_checked`;
- do not synthesize evidence;
- do not call raw-log readers to fill the gap.

Privacy boundary failure:

- return sanitized `privacy_boundary_failed`;
- do not include the unsafe value;
- classify top-level status as `blocked`.

Unsupported schema version:

- return sanitized `source_schema_unsupported`;
- keep the frontend fail-closed behavior.

## Compatibility

Existing routes must remain compatible:

- `GET /api/live/player-log/status`
- `GET /api/live/watcher/status`
- `GET /api/live/watcher/process`
- `GET /api/live/ingest/status`
- `GET /api/app/setup-status`

Existing frontend status panels must remain compatible. Adding a diagnostics
panel must not remove or rename existing live panels.

Existing #244 behavior must remain compatible:

- final/reconciled match/game capture only;
- no provisional live fact writes;
- no gameplay/opponent-observation/field-evidence live writes;
- no raw Player.log storage.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- analytics schema or migrations;
- #244 live capture semantics;
- manual JSONL import semantics;
- replay ingest semantics;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- AI/OpenAI/model-provider behavior;
- Line Tracer behavior;
- coaching behavior;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- secrets, credentials, environment variables, API keys, tokens, webhook URLs,
  spreadsheet IDs, or deployment IDs.

## Unknowns

- Whether Codex C should implement diagnostics in `setup_status.py` or a new
  local-app diagnostics module.
- Whether live ingest result metadata is available anywhere outside direct test
  calls yet.
- Whether existing evidence-ledger runtime health is available through a safe
  local app status source, or should remain `expected_but_unavailable`.
- Whether the frontend should show the diagnostics panel inside the setup status
  surface or a separate live-mode section.
- Whether future actual watcher operation will supply sanitized rotation,
  truncation, and duplication summaries.

## Suspected Gaps

- No current `GET /api/live/watcher/diagnostics` route exists.
- Existing live status surfaces are separate, so users must mentally combine
  Player.log readiness, watcher process status, and live ingest status.
- Existing diagnostics labels can say rotation/truncation detection is deferred,
  but there is no consolidated user-facing quality explanation.
- Parser diagnostics can produce useful health reports, but invoking that code
  from a local app GET route would overreach if it reads a live/private log.
- Frontend types currently cover Player.log, watcher, and process status, but
  not a consolidated diagnostics response.

## Tests Required

Codex C should add focused backend tests covering:

- `GET /api/live/watcher/diagnostics` returns the required object and schema
  version;
- player log metadata labels map to diagnostics entries;
- stale Player.log metadata produces a safe warning/degraded diagnostic;
- missing/unreadable/not-file Player.log metadata produces safe blocked or
  unavailable diagnostics;
- missing watcher state is reported, not repaired;
- malformed watcher state is reported without echoing file content;
- stale watcher state is reported, not cleaned;
- live ingest status is included as a source summary;
- deferred live fact families are represented as diagnostics when supplied by
  sanitized live ingest metadata;
- privacy/capability booleans are present and false for unsafe exposure;
- GET calls do not create SQLite files, WAL/SHM/journal files, logs,
  diagnostics files, runtime status files, watcher state files, or app-data
  artifacts beyond any pre-existing test fixture root;
- no start/stop/restart/clear/delete routes are added.

Codex C should add focused frontend tests covering:

- typed API validation for the diagnostics response;
- fail-closed handling for malformed/unsupported response shapes;
- safe rendering of category/severity/status labels;
- redaction of unsafe display values;
- absence of destructive/remediation controls.

Recommended validation commands:

```powershell
py -m pytest -q tests/test_analytics_local_app_backend.py
py -m pytest -q tests/test_live_app_parser_owned_fact_capture_sqlite.py tests/test_tailer.py tests/test_parser_diagnostics_mode.py tests/test_evidence_runtime_status.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
py -m ruff check src tests
git diff --check
py tools\check_agent_docs.py
py tools\check_secret_patterns.py --all
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
```

If `npm --prefix frontend run build` is used, Codex C must remove generated
`frontend/dist` output afterward unless it is already ignored and absent from
the final diff.

## Acceptance Criteria

- `docs/contracts/live_app_watcher_diagnostics.md` exists.
- Contract defines route, response shape, status/severity vocabulary, diagnostic
  categories, source summaries, privacy booleans, backend/frontend boundaries,
  protected surfaces, tests, and handoff.
- The approved first slice is read-only composition.
- The contract explicitly forbids raw Player.log reads/storage, watcher control,
  remediation controls, new persistence, schema changes, and external transport.
- Parser truth ownership and #244 live capture semantics remain unchanged.
- Codex C handoff is included.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #246.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/246

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_watcher_diagnostics.md

Goal:
Compare the current local app live Player.log status, watcher process safeguards, live SQLite capture status, parser diagnostics, evidence runtime health, and frontend live panels against the contract. Implement only the approved first slice: a read-only sanitized diagnostics/status surface, likely `GET /api/live/watcher/diagnostics`, plus frontend display if needed.

Before editing:
- Confirm branch and git status.
- State what the live watcher diagnostics surface is supposed to do.
- State what current code already does.
- State why the current surfaces are insufficient.
- State the exact minimal implementation plan.

Do:
- Compose existing sanitized status surfaces.
- Keep diagnostics as labels, counts, booleans, and safe messages.
- Preserve parser truth ownership and #244 live capture semantics.
- Add focused backend tests for route shape, category/severity mapping, stale/malformed watcher state, live ingest source inclusion, privacy booleans, and no GET-created artifacts.
- Add frontend API/types/display/tests if frontend display changes.
- Produce docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md.

Do not:
- Start, stop, restart, kill, inspect, or control a watcher process.
- Call runner, stream, or tailer startup/polling.
- Read, copy, hash, tail, store, or expose raw Player.log content.
- Generate parser diagnostics reports from a live/private log in a GET route.
- Create SQLite files, WAL/SHM/journal files, diagnostics files, runtime status files, logs, watcher state files, generated artifacts, secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs, environment values, or local-only artifacts.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations, #244 live capture semantics, manual import semantics, replay ingest semantics, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, AI/OpenAI/model-provider behavior, Line Tracer, coaching, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice.
- Add destructive/remediation UI controls.
- Target main.

Validation:
py -m pytest -q tests/test_analytics_local_app_backend.py
py -m pytest -q tests/test_live_app_parser_owned_fact_capture_sqlite.py tests/test_tailer.py tests/test_parser_diagnostics_mode.py tests/test_evidence_runtime_status.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
py -m ruff check src tests
git diff --check
py tools\check_agent_docs.py
py tools\check_secret_patterns.py --all
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- files changed
- exact implementation sections changed
- comparison against contract
- validation run
- generated/private artifact status
- protected-surface status
- remaining risks/unknowns
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/246"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue problem representation for live watcher diagnostics"
  contract_artifact: "docs/contracts/live_app_watcher_diagnostics.md"
  target_artifact: "docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B should run git diff --check or an equivalent new-file-safe whitespace check."
    - "Codex B should run a path-scoped protected-surface scan."
    - "Codex B should run a path-scoped secret/private-marker scan."
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not start, stop, restart, tail, read, copy, hash, store, or expose raw Player.log."
    - "Do not create local/generated/private/runtime artifacts from diagnostics GET routes."
    - "Do not change parser/runtime/analytics schema/#244 capture/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose destructive/remediation controls."
```
