# Live App Player.log Path And Watcher Status Contract

## Module

Local app live Player.log path and watcher readiness status.

This contract defines the first Live Player.log Mode local-app slice: a
read-only status surface that tells the user whether Mythic Edge can locate a
candidate MTGA `Player.log` file and whether a future live watcher would be
ready, blocked, unavailable, or deferred.

This slice does not start a watcher, tail `Player.log`, start the parser
runner, write parser facts to SQLite, write config, alter parser behavior, or
change production behavior.

Plain English: show the user the live-mode dashboard lights before wiring any
live-mode controls.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/240>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Related Match Journal tracker:
  <https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Branch

Intended branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
0 0
```

This contract does not target `main`.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- issue #240
- tracker #204
- umbrella issue #207
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contracts/match_journal_live_browser_real_app_data_readiness.md`
- `docs/contracts/match_journal_safe_context_browser_write_smoke.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/stream.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/status.ts`
- `frontend/src/types.ts`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_runner.py`
- `tests/test_tailer.py`
- `frontend/src/App.test.tsx`

## Risk Tier

High.

Reasons:

- introduces browser-visible live-mode status vocabulary;
- adds local API routes that reference a private local file path;
- can accidentally expose full paths, file contents, or private metadata;
- can blur readiness status with actual parser runtime behavior;
- can accidentally grow into live watcher process control;
- can accidentally create generated artifacts from GET routes;
- is the first local-app step toward live Player.log capture.

## Internal Project Area

Primary area: local app / UI.

Adjacent areas:

- parser runtime and stream tailing, reference-only in this slice;
- local app config and setup-status;
- frontend setup/status display;
- future live watcher lifecycle.

## Bridge-Code Status

bridge_code

This module is a bridge from local app config/path metadata into browser-visible
status. It must not become parser truth, analytics truth, workbook truth,
deployment truth, or AI truth.

## Ownership And Truth Boundaries

Truth owners:

- MTGA `Player.log` remains the observable raw evidence source.
- `src/mythic_edge_parser/app/runner.py` and
  `src/mythic_edge_parser/stream.py` own actual live parser/tailer behavior.
- Parser/state modules own event interpretation, match/game identity, final
  reconciliation, and parser-managed facts.
- The local app owns only local readiness/status reporting and sanitized
  browser display.
- SQLite analytics remains downstream storage and is not used by this slice.
- The frontend displays status only.

This contract must not move truth ownership to:

- local app status payloads;
- browser UI state;
- analytics rows;
- workbook formulas;
- webhook or Apps Script transport;
- AI or model-provider output.

## Observed Current Behavior

Backend:

- `src/mythic_edge_parser/local_app/setup_status.py` already exposes
  `build_player_log_path_status(paths)`.
- The current Player.log setup status checks:
  - invalid local app config;
  - configured `player_log_path`;
  - default MTGA Player.log path from `app.config.DEFAULT_MTGA_PLAYER_LOG`;
  - unavailable app-data root;
  - missing detected path.
- The current Player.log setup status returns symbolic display values such as
  `<configured_player_log>` and `<detected_mtga_player_log>`.
- Existing tests assert the configured Player.log body is not read and the
  absolute configured path is not returned.
- `build_runtime_state()` currently returns parser runner and live watcher
  status as `deferred`.
- `GET /api/runtime/status` exposes that non-controlling runtime payload.
- Existing setup-status GET routes are tested not to create local app
  artifacts.

Frontend:

- `frontend/src/App.tsx` renders setup-status panels from
  `GET /api/app/setup-status`.
- The Player Log panel currently displays symbolic path and coarse state.
- The Runtime panel displays backend, parser runner, and live watcher status.
- A separate deferred "Live Watcher" panel is currently hardcoded.
- `frontend/src/status.ts` redacts unsafe display strings, including raw
  absolute paths and non-symbolic `Player.log` values.

Parser runtime:

- `runner.py` checks whether `LOG_PATH` exists during startup and raises on a
  missing Player.log.
- `runner.py` starts runtime logging, runtime status updates, status API,
  analytics sidecar, webhook dispatching, and the MTGA event stream when
  `main()` runs.
- `stream.py` starts live tailing by opening `FileTailer.open_from_end(log_path)`.
- `FileTailer` owns actual polling, rotation detection, content reads, and
  structured log entry parsing.

## Required Contract Decisions

### Read-Only Status First

Issue #240 is a read-only status slice.

Codex C may add helper functions, backend GET routes, frontend types, frontend
API readers, frontend display panels, and tests needed to report live readiness.

Codex C must not add:

- POST, PUT, PATCH, or DELETE routes;
- watcher start/stop controls;
- parser runner control;
- live tailing;
- raw Player.log reads;
- SQLite ingest from live Player.log;
- config write behavior;
- runtime-status file reads or writes;
- destructive local app actions.

### Backend Endpoint Contract

Codex C should add these local loopback-only read-only endpoints:

```text
GET /api/live/player-log/status
GET /api/live/watcher/status
```

The endpoints must be mounted on the existing FastAPI local app only. They must
use the same loopback and CORS boundaries as the existing local app backend and
must not start or call the legacy parser status API.

Allowed aggregate compatibility change:

- `GET /api/app/setup-status` may include a new `live` or
  `live_player_log` summary section if doing so improves frontend ergonomics.
- This addition must be backward-compatible with the existing required
  setup-status fields.
- Existing setup-status response fields must not be removed or renamed.

### Player.log Status Response Shape

`GET /api/live/player-log/status` must return a JSON object with:

- `object = "mythic_edge_local_app_live_player_log_status"`
- `schema_version = "live_app_player_log_path_watcher_status.v1"`
- `status`: top-level status string
- `player_log`: object
- `diagnostics`: object or list of sanitized diagnostic labels
- `warnings`: list of sanitized codes
- `errors`: list of sanitized codes

The `player_log` object must include:

- `status`: one of the approved Player.log path/config statuses;
- `source`: `configured`, `detected_default`, `none`, or `unavailable`;
- `display_path`: symbolic only;
- `path_kind`: `file`, `missing`, `directory`, `unknown`, or `unavailable`;
- `metadata_access`: `accessible`, `denied`, `not_checked`, or `unavailable`;
- `exists`: boolean;
- `contents_read`: always `false` for this slice;
- `tailing_started`: always `false` for this slice.

Optional metadata fields are allowed only when they are obtained without
reading file contents:

- `size_bytes`: non-negative integer or `null`;
- `last_modified_at`: ISO-like timestamp string or `null`;
- `last_modified_age_seconds`: non-negative number or `null`;
- `activity_hint`: `recent`, `stale`, `unknown`, or `not_applicable`.

The response must not include:

- raw absolute local paths;
- raw Player.log content;
- raw log lines;
- hashes of raw log content;
- snippets, headers, usernames, machine-specific paths, or environment values.

### Watcher Readiness Response Shape

`GET /api/live/watcher/status` must return a JSON object with:

- `object = "mythic_edge_local_app_live_watcher_status"`
- `schema_version = "live_app_player_log_path_watcher_status.v1"`
- `status`: top-level status string
- `watcher`: object
- `player_log`: sanitized nested summary or reference status
- `warnings`: list of sanitized codes
- `errors`: list of sanitized codes

The `watcher` object must include:

- `status`: one of the approved watcher statuses;
- `mode = "readiness_only"`;
- `running`: `false` for this slice;
- `start_allowed`: `false` for this slice;
- `stop_allowed`: `false` for this slice;
- `parser_runner_started`: `false`;
- `tailing_started`: `false`;
- `sqlite_live_writes_enabled`: `false`;
- `reason`: sanitized code or `null`.

`running` is reserved for future process-control work. This slice must not
return `running` unless Codex C routes back to Codex B because an already
existing, separately owned watcher process is discovered and needs a narrower
contract.

### Status Vocabulary

Approved Player.log path/config statuses:

- `configured_exists`: config supplied a path and metadata confirms it is a
  file.
- `configured_missing`: config supplied a path that is missing.
- `configured_not_file`: config supplied a path that exists but is not a file.
- `detected_exists`: default MTGA Player.log path exists and is a file.
- `detected_missing`: default MTGA Player.log path was checked and missing.
- `missing`: no configured path exists and no default path exists.
- `invalid_config`: config was malformed or `player_log_path` had an invalid
  shape.
- `unreadable`: metadata access failed because of permissions or an OS error.
- `not_file`: selected path exists but is not a file.
- `unavailable`: app-data root, local platform, or environment did not allow a
  meaningful path check.

Approved watcher statuses:

- `not_configured`: no usable Player.log path is configured or detected.
- `ready`: metadata says a candidate Player.log file exists and no blocker was
  found.
- `blocked_missing_log`: the selected/detected file is missing.
- `blocked_unreadable_log`: metadata access failed.
- `blocked_invalid_config`: local app config prevents a reliable path check.
- `stopped`: future status for an implemented watcher that is not running.
- `running`: future status only; not expected for #240 implementation.
- `deferred`: watcher implementation is intentionally not present yet.
- `unavailable`: local app environment cannot determine watcher readiness.
- `degraded`: readiness can be partially reported but has warnings.

Approved diagnostic labels:

- `stale`
- `unknown_last_modified`
- `permission_denied`
- `not_file`
- `metadata_unavailable`
- `readability_not_probed`
- `rotation_detection_deferred`
- `truncation_detection_deferred`

`rotated` and `truncated` must not be reported as confirmed in this first
slice unless the implementation has direct evidence that does not require
tailing or reading Player.log contents. Otherwise use deferred diagnostics.

## Config And Path Boundary

Allowed:

- Read existing local app config with `read_local_app_config(paths)`.
- Use configured `player_log_path` as a path candidate.
- Use `DEFAULT_MTGA_PLAYER_LOG` as the default Windows path candidate.
- Use `Path.exists()`, `Path.is_file()`, and `Path.stat()` or equivalent
  metadata-only checks.
- Return symbolic display paths only:
  - `<configured_player_log>`
  - `<detected_mtga_player_log>`
  - `<player_log_unavailable>`
- Return safe labels and codes.

Forbidden:

- Return raw configured or default absolute path strings.
- Return `MTGA_PLAYER_LOG` or other environment values.
- Read or copy Player.log contents.
- Tail the file.
- Open a persistent file handle.
- Store path snapshots in SQLite.
- Write local app config.
- Create missing app-data folders from status GET routes.
- Create generated databases, WAL/SHM files, logs, diagnostics, failed posts,
  or runtime status files from status GET routes.

If Codex C needs a readability check beyond metadata access, it must keep it
non-content-reading and explain the exact operating-system call used. If that
cannot be done safely, readability must remain `not_checked` or `unknown`.

## Watcher Readiness Boundary

Watcher readiness may be derived only from:

- sanitized Player.log path/config status;
- metadata-only file existence/kind/access results;
- local app environment availability;
- explicit current implementation status that live watcher process control is
  deferred.

Watcher readiness must not:

- start `runner.main()`;
- call `MtgaEventStream.start(...)`;
- call `FileTailer.open_from_end(...)`;
- poll Player.log;
- parse log entries;
- route events;
- update parser runtime state;
- write parser facts into SQLite;
- update workbook/webhook/App Script output;
- imply live capture is active.

## Frontend Display Contract

Allowed frontend changes:

- Add frontend API helpers for the two new GET routes.
- Add typed response shapes for live Player.log and watcher status.
- Add a visible "Live Player.log" or "Live Mode Readiness" panel.
- Replace the hardcoded deferred "Live Watcher" panel with status from the new
  read-only endpoint.
- Continue showing setup-status Player Log and Runtime sections.
- Display symbolic paths, status values, safe diagnostics, and warnings.
- Show that watcher controls are disabled/deferred.

Required frontend safety:

- Reuse `safeDisplayValue(...)` or equivalent redaction before rendering
  backend-provided status detail strings.
- Do not render raw absolute paths or non-symbolic `Player.log` values.
- Do not add file picker/config write controls.
- Do not add watcher start/stop buttons.
- Do not add arbitrary SQL, database browsing, or generated-artifact controls.
- Do not present `ready` as "currently capturing". The UI must distinguish
  readiness from active live capture.

## Tests Required For Codex C

Backend tests:

- configured existing Player.log reports `configured_exists`, symbolic path,
  `contents_read = false`, and no raw path/body leakage;
- configured missing Player.log reports `configured_missing` and blocks watcher
  readiness;
- configured directory reports `configured_not_file` or `not_file`;
- invalid config maps to `invalid_config` and
  `blocked_invalid_config`;
- detected default path can be monkeypatched to report `detected_exists`;
- app-data root unavailable reports `unavailable` without throwing;
- status GET routes do not create app-data folders, databases, WAL/SHM files,
  runtime status files, logs, or failed posts;
- watcher status remains readiness-only and returns `start_allowed = false`,
  `stop_allowed = false`, `tailing_started = false`, and
  `sqlite_live_writes_enabled = false`.

Frontend tests:

- live status panel renders sanitized symbolic Player.log status;
- unsafe backend strings containing raw paths or `Player.log` are redacted;
- watcher readiness displays `ready`, `blocked_*`, or `deferred` without
  implying active capture;
- no start/stop controls are rendered;
- malformed or incompatible live-status responses fail safely.

Regression boundaries:

- existing setup-status tests must continue to pass;
- existing Match Journal, manual import, analytics view, runner, tailer, and
  frontend tests must not require behavior changes outside this contract.

## Validation Plan

Codex C should run the smallest relevant checks first:

```powershell
py -m pytest -q tests/test_analytics_local_app_config.py tests/test_analytics_local_app_backend.py
```

Frontend focused checks:

```powershell
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
```

Adjacent parser/runtime checks:

```powershell
py -m pytest -q tests/test_runner.py tests/test_tailer.py
```

Hygiene checks:

```powershell
py -m ruff check src tests
git diff --check
@'
docs/contracts/live_app_player_log_path_watcher_status.md
docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/setup_status.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
py tools\check_secret_patterns.py docs/contracts/live_app_player_log_path_watcher_status.md
```

Codex C/E must report if frontend dependency installation or Node validation is
unavailable.

## Acceptance Criteria

- Contract comparison/handoff is produced at
  `docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md`.
- New backend live status routes are read-only and loopback-local.
- Player.log path status is metadata-only and symbolic-path-only.
- Watcher status is readiness-only and explicitly non-controlling.
- Frontend displays live readiness safely and does not expose controls.
- No raw paths, raw Player.log content, secrets, environment values, generated
  database files, runtime artifacts, failed posts, or workbook exports are
  committed.
- No parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/
  production behavior changes occur.
- Required focused validation passes or failures are explained with cause.

## Unknowns

- Whether metadata-only `Path.stat()` is enough to distinguish all practical
  Windows permission failures.
- Whether stale thresholds should be time-based, size-based, user-configurable,
  or omitted until watcher process-control exists.
- Whether future live watcher status should read process state from an
  app-owned job table, a runtime status file, or an in-memory launcher process.
- Whether the default MTGA Player.log path should remain hardcoded in
  `app.config` or move to a local-app path helper in a later contract.
- Whether actual-root readiness should be user-approved before or after the
  first live watcher process-control issue.

## Suspected Gaps

- Current setup status is too coarse for live mode because it does not expose
  metadata, path kind, or readiness reason.
- Current runtime status has `live_watcher = deferred` only and does not map
  Player.log path state into readiness blockers.
- Frontend has a hardcoded deferred Live Watcher panel instead of using a live
  readiness endpoint.
- Current code has no local app endpoint dedicated to live Player.log status.
- Rotation/truncation detection exists in the tailer, but using it here would
  require tailing or reading Player.log and is out of scope.

## Protected Surfaces

Do not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- extractor behavior;
- gameplay-action or opponent-observation behavior;
- analytics schema, migrations, ingest semantics, or curated views;
- Match Journal write semantics;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- CI gate behavior.

Do not create, inspect, commit, print, or modify:

- secrets;
- credentials;
- tokens;
- API keys;
- webhook URLs;
- spreadsheet IDs;
- environment values;
- raw Player.log files;
- private JSONL artifacts;
- generated SQLite databases;
- WAL/SHM/journal files;
- runtime logs;
- runtime status files;
- failed posts;
- workbook exports;
- local-only artifacts.

## Out Of Scope

- Live watcher process-control safeguards.
- Watcher start/stop/restart routes or buttons.
- Parser runner process control.
- Live parser-owned fact writes to SQLite.
- Live Player.log tailing.
- Live drift/truncation/rotation diagnostics that require tailing or content
  reads.
- Config write or Player.log path picker UI.
- Actual app-data root writes.
- Direct legacy status API browser integration.
- Google Sheets sync.
- OpenAI runtime integration.
- AI coaching, Line Tracer, or strategic advice.
- Production deployment behavior.

## Expected Codex C Implementation Scope

Codex C should:

1. Compare the current local app backend/frontend to this contract.
2. Implement only read-only live Player.log and watcher readiness status.
3. Produce
   `docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md`.
4. Add focused backend and frontend tests.
5. Keep all generated/private artifacts out of git.
6. Route back to Codex B if the contract is insufficient for metadata-only
   readability or if process-control behavior is needed.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #240.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/240

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_player_log_path_watcher_status.md

Goal:
Compare the current local app backend/frontend to the contract and implement only the read-only Player.log path and watcher readiness status surface. Produce docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md.

Before editing:
- Confirm branch and git status.
- Inspect AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, issue #240, and docs/contracts/live_app_player_log_path_watcher_status.md.
- State what the live status surface is supposed to do, what the repo currently does, why the gap exists, and the exact minimal implementation plan.

Allowed:
- Add metadata-only backend helpers for Player.log path status.
- Add GET /api/live/player-log/status.
- Add GET /api/live/watcher/status.
- Optionally add a backward-compatible setup-status live summary.
- Add frontend API/types/display for sanitized live readiness status.
- Add focused backend/frontend tests.

Do not:
- start or stop a watcher;
- call runner.main(), MtgaEventStream.start(), or FileTailer.open_from_end();
- tail, parse, read, copy, hash, or store Player.log contents;
- expose raw absolute paths, environment values, secrets, or private data;
- write local app config;
- create SQLite databases or generated artifacts from GET status routes;
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest/views, Match Journal write semantics, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- target main;
- close #204 or #207.

Validation:
py -m pytest -q tests/test_analytics_local_app_config.py tests/test_analytics_local_app_backend.py
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
py -m pytest -q tests/test_runner.py tests/test_tailer.py
py -m ruff check src tests
git diff --check
Path-scoped protected-surface scan for the contract, comparison handoff, and changed backend/frontend files.
Secret/private-marker scan for changed docs/backend/frontend files.

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract artifact used
- files changed
- exact backend/frontend/test sections changed
- what was verified
- what remains unverified
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block routing to Codex E
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/240"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #240"
  target_artifact: "docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md"
  contract_artifact: "docs/contracts/live_app_player_log_path_watcher_status.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch -> clean/even before contract edit"
    - "git diff --check"
    - "path-scoped protected-surface scan for docs/contracts/live_app_player_log_path_watcher_status.md"
    - "secret/private-marker scan for docs/contracts/live_app_player_log_path_watcher_status.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not start or stop a live watcher."
    - "Do not tail, read, copy, hash, or store raw Player.log contents."
    - "Do not expose raw absolute paths, secrets, environment values, or private artifacts."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
