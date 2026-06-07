# Live App Parser-Owned Fact Capture Into SQLite Contract

## Module

`live_app_parser_owned_fact_capture_sqlite`

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/244
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
- GitHub issue `#244`
- GitHub tracker `#204`
- GitHub umbrella issue `#207`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_migration_loader.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`
- `docs/contracts/analytics_field_evidence_ingest.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`

## Owning Layer

- Parser/state owns event interpretation and parser-managed match/game truth.
- Analytics ingest owns local SQLite persistence of parser-normalized facts.
- Local app owns local-only status surfaces and user-visible readiness state.
- SQLite is a local storage surface, not a truth owner.
- The browser UI is a display/control surface, not a truth owner.

## Truth Owner

Parser-owned facts remain owned by `src/mythic_edge_parser/app/state.py`,
`src/mythic_edge_parser/app/models.py`, and their existing final-reconciliation
logic. This contract must not move truth ownership into analytics, SQLite, the
local app, frontend views, Google Sheets, AI, or any watcher process.

## Bridge-Code Status

This is bridge code between:

- parser/state final outputs,
- local app live-mode orchestration,
- local SQLite analytics storage.

The bridge may copy parser-normalized facts into SQLite. It must not reinterpret
raw Player.log content, compute match/game truth, infer hidden state, or create
new parser-managed identities.

## Observed Current Behavior

### Live App And Watcher Status

- `#240` added read-only Player.log path and watcher status surfaces.
- `#242` added process-control safeguards through
  `src/mythic_edge_parser/local_app/live_watcher_process.py`.
- `GET /api/live/watcher/process` reports safeguards and readiness metadata.
- Current watcher process-control flags intentionally remain false, including:
  - `start_allowed`
  - `stop_allowed`
  - `parser_runner_started`
  - `tailing_started`
  - `sqlite_live_writes_enabled`
  - `external_transport_allowed`
- `live_sqlite_ingest_contract_present` is currently deferred in the process
  preconditions.
- The local app does not start, stop, tail, or run the parser watcher.
- The local app does not write live parser-owned facts into SQLite.

### Analytics Ingest

- `src/mythic_edge_parser/app/analytics_ingest.py` provides
  `ingest_parser_normalized_replay(...)` for parser-normalized replay-shaped
  input.
- Existing replay ingest accepts `source_kind` values:
  - `sanitized_golden_replay`
  - `saved_event_replay`
- Existing replay ingest rejects `live_parser`, even though the SQLite schema
  already permits `live_parser` in `ingest_runs.source_kind`.
- Existing replay ingest writes parser-normalized match/game rows, gameplay
  actions, opponent-card observations, and field evidence when those arrays are
  supplied in replay-shaped input.
- Existing replay ingest creates deterministic ingest run IDs from the full
  normalized replay payload.
- Existing replay ingest rejects unsafe source labels that look like local paths,
  URLs, or private filenames.
- Existing manual JSONL import uses the replay ingest path and the local app
  analytics database.

### SQLite Schema

- The initial analytics SQLite schema already permits:
  - `source_kind = 'live_parser'`
  - `finality` values including `live`, `provisional`, `final`, and
    `reconciled`
- The schema supports existing match/game fact families and provenance rows.
- The schema is not a raw Player.log storage surface.

### Parser Final Outputs

- `MatchState.build_match_summary_row()` returns final match rows only when the
  match summary is ready.
- `MatchState.build_live_match_log_row()` returns live/provisional match rows.
- `MatchState.build_match_log_update()` can return either final or live-shaped
  match updates.
- `MatchState.build_game_log_updates()` emits game rows and marks rows final
  when game result evidence exists.

### Runner And Tailer Boundaries

- The existing parser runner can initialize runtime logging, status API,
  analytics sidecar behavior, webhook dispatch, and Sheets/output transport
  depending on configuration.
- The existing stream/tailer path reads Player.log bytes.
- The current local app process-control safeguards intentionally do not call the
  runner, stream, or tailer.
- A live SQLite write path must not accidentally enable workbook, webhook, Apps
  Script, Sheets, production transport, raw log storage, or broad runner side
  effects.

## Contract Decision

Issue `#244` should define and implement the narrow SQLite capture boundary for
completed parser-owned facts supplied by an approved live-mode caller.

The first implementation must focus on a reusable live SQLite ingest adapter and
read-only status reporting. It must not expose routine watcher start/stop UI,
must not start tailing Player.log, and must not invoke the existing parser runner
unless a later issue/contract proves a no-transport local-app runner mode is safe.

The first live-capture slice should write only final or reconciled match/game
facts. It should defer provisional live facts, gameplay actions, opponent-card
observations, field evidence, diagnostics for log rotation/truncation, actual
private Player.log smoke, and frontend live controls.

## Public Interfaces

### Required Analytics Interface

Codex C should add a narrow live ingest interface rather than overloading manual
import semantics. The exact function name may vary, but the public behavior must
be equivalent to:

```python
ingest_live_parser_owned_facts(
    connection,
    payload,
    *,
    started_at=None,
    finished_at=None,
)
```

Required payload fields:

- `source_kind`: must be `live_parser`
- `source_artifact_label`: sanitized label such as `live_parser_session`
- `session_id`: deterministic live-session or capture-session identifier
- `match_log_rows`: parser-normalized final/reconciled match rows
- `game_log_rows`: parser-normalized final game rows

Optional payload fields:

- `parser_version`
- `capture_started_at`
- `capture_finished_at`
- `warnings`

Forbidden payload fields:

- raw Player.log lines
- raw saved-event lines
- raw webhook payloads
- raw local file paths
- local Player.log paths
- private JSONL source paths
- raw log hashes derived from private content unless a later contract explicitly
  authorizes hash handling

### Existing Replay Interface Compatibility

Codex C may reuse existing analytics ingest helpers, but must preserve existing
manual import and replay behavior.

Acceptable implementation strategies:

- Add `live_parser` to the existing normalized replay source-kind validator and
  create a separate live wrapper that only accepts final/reconciled match/game
  rows.
- Keep replay ingest source-kind validation unchanged and add a separate live
  ingest path that shares lower-level row-upsert helpers.

Required compatibility either way:

- Existing `sanitized_golden_replay` ingest tests must continue to pass.
- Existing `saved_event_replay` ingest tests must continue to pass.
- Existing unsafe source-label rejection must remain active.
- Existing manual import semantics must remain unchanged.
- Existing replay ingest must not start accepting raw log content.

### Required Local App Status Interface

Codex C may add a read-only local app status route equivalent to:

```text
GET /api/live/ingest/status
```

Required response shape:

```json
{
  "object": "mythic_edge_local_app_live_parser_sqlite_capture_status",
  "schema_version": "live_app_parser_owned_fact_capture_sqlite.v1",
  "status": "disabled",
  "mode": "status_only",
  "source_kind": "live_parser",
  "database": {
    "configured": true,
    "display_path": "<app_data>\\db\\mythic_edge.sqlite3"
  },
  "capabilities": {
    "live_sqlite_capture_contract_present": true,
    "final_match_game_fact_capture_supported": true,
    "provisional_fact_capture_supported": false,
    "gameplay_action_live_capture_supported": false,
    "opponent_observation_live_capture_supported": false,
    "field_evidence_live_capture_supported": false,
    "raw_player_log_storage_supported": false,
    "external_transport_allowed": false
  },
  "last_result": null,
  "warnings": []
}
```

Allowed `status` values:

- `disabled`
- `not_configured`
- `blocked`
- `ready`
- `idle`
- `writing`
- `degraded`
- `failed`
- `stale`
- `unknown`

The route must be loopback/local-app only under the existing local backend
boundary. It must not expose raw local paths, raw Player.log content, arbitrary
SQL, database browsing, destructive actions, or process-control buttons.

### Process-Control Status Integration

Codex C may update `live_watcher_process` readiness metadata to recognize that a
live SQLite ingest contract or adapter exists.

Required boundaries:

- `sqlite_live_writes_enabled` must remain false unless the implementation also
  introduces an explicitly approved caller that supplies final parser-owned rows.
- `start_allowed` and `stop_allowed` must remain governed by the process-control
  safeguards contract.
- `parser_runner_started` and `tailing_started` must remain false for read-only
  status calls.
- External transport flags must remain false.

## Inputs

### Match Rows

Allowed match rows:

- Rows generated from existing parser/state `MatchSummary` row surfaces.
- Rows equivalent to `MatchSummary.to_match_log_row(final=True)`.
- Rows that are final or reconciled.

Forbidden match rows:

- Rows generated only from `build_live_match_log_row(...)`.
- Rows whose sync status clearly indicates live/provisional state.
- Rows missing required match identity.
- Rows carrying raw Player.log snippets, raw source paths, or raw event payloads.

### Game Rows

Allowed game rows:

- Rows generated from existing parser/state `GameSummary` row surfaces.
- Rows equivalent to `GameSummary.to_game_log_row()` or the existing final game
  sheet row output.
- Rows with parser-owned game identity and game result evidence.

Forbidden game rows:

- In-progress rows without game result evidence.
- Rows that require analytics to infer game result, play/draw, or game identity.
- Rows carrying raw Player.log snippets, raw source paths, or raw event payloads.

### Deferred Inputs

The first implementation must not ingest these from live mode:

- gameplay actions
- opponent-card observations
- field evidence rows
- partial opening-hand fragments not already represented in final parser rows
- raw event replay records
- raw tailer lines
- raw Player.log bytes
- drift diagnostics derived from log rotation/truncation

These may remain supported by replay/manual import paths where already
implemented, but live-mode writes for these families require later contracts.

## Outputs

Allowed SQLite output tables for the first implementation:

- `ingest_runs`
- `matches`
- `games`
- `match_results`
- `game_results`
- `match_context`
- `rank_snapshots`
- `opening_hands`
- `opening_hand_cards`
- `mulligan_events`
- `mulligan_bottomed_or_discarded_cards`
- `fact_provenance`

Forbidden SQLite output tables for the first implementation:

- `gameplay_actions`
- `gameplay_action_cards`
- `opponent_card_observations`
- `opponent_card_observation_cards`
- new raw-log tables
- new raw-event tables
- new arbitrary diagnostics tables
- new coaching, Line Tracer, archetype, hidden-card, player-mistake, or best-line
  tables

Required result object behavior:

- report touched table counts;
- report skipped row counts;
- report sanitized warnings;
- never include raw Player.log content;
- never include private absolute paths;
- distinguish malformed input from valid-but-skipped deferred facts.

## Deterministic IDs And Idempotency

The live ingest path must be idempotent. Idempotent means repeated writes of the
same parser-owned facts update the same logical rows instead of creating
duplicates.

Required guarantees:

- Repeating the same final match row must not create duplicate `matches` or
  `match_results` rows.
- Repeating the same final game row must not create duplicate `games` or
  `game_results` rows.
- Replaying a live session after watcher restart must not duplicate facts when
  match/game IDs are unchanged.
- Facts imported manually from replay/JSONL and later seen by live capture must
  converge on the same parser-owned logical identity where the existing schema
  already uses stable primary keys.
- `ingest_runs` may record distinct source runs, but fact tables must remain
  deduplicated by their existing deterministic keys.
- The implementation must not redefine match ID, game ID, or deduplication
  semantics.

Recommended live run identity:

- `source_kind`: `live_parser`
- `source_artifact_label`: `live_parser_session`
- `session_id`: sanitized identifier that does not reveal a local path, username,
  raw log hash, or private filename.

If Codex C cannot define a safe deterministic `session_id` without path or raw
content leakage, the implementation must use an explicit non-private app-session
identifier and record the limitation as an unknown, not hash private log content.

## Finality Policy

The first implementation must be final/reconciled only.

Allowed finality values for live writes in this slice:

- `final`
- `reconciled`

Disallowed finality values for live writes in this slice:

- `live`
- `provisional`

Required behavior:

- Provisional/live rows must be rejected or skipped with a sanitized warning.
- Provisional/live rows must not overwrite final/reconciled facts.
- A later contract is required before live/provisional facts can be written to
  SQLite.

## Source, Confidence, And Provenance

Required provenance behavior:

- Every written fact family must retain the existing parser-normalized lineage
  columns required by the analytics schema contract.
- `fact_provenance` rows must identify `source_kind = live_parser`.
- Provenance must describe parser-normalized rows, not raw Player.log evidence.
- The live capture path must preserve existing parser-provided value source,
  confidence, finality, drift, and evidence-status fields when those fields are
  already present in the parser-normalized row surface.
- The implementation must not synthesize confidence labels that the parser/state
  layer did not provide.

Unknown:

- Current final match/game row surfaces may not expose every ledger-style
  source/confidence/finality field. Codex C should preserve what exists and
  report missing lineage fields instead of inventing them.

## Error Behavior

### Malformed Input

Malformed live payloads must fail closed.

Required behavior:

- Reject missing `source_kind`.
- Reject non-`live_parser` source kind for the live-specific interface.
- Reject unsafe source labels that look like paths, URLs, private filenames, or
  raw log artifacts.
- Reject or skip non-final match/game rows.
- Reject rows that lack required parser-owned identity fields.
- Return sanitized error messages.
- Roll back partial writes on transaction failure.

### SQLite Errors

Required behavior:

- Preserve transaction integrity.
- Report sanitized failure status.
- Do not include raw filesystem paths unless passed through an approved display
  path helper such as `<app_data>\...`.
- Do not delete, move, archive, or repair database files automatically.

### Duplicate Or Previously Imported Facts

Required behavior:

- Treat duplicate final facts as idempotent upserts.
- Do not create duplicate match/game facts because a row was also imported
  manually from JSONL.
- Do not delete existing facts from another source kind.
- Do not downgrade final/reconciled facts to provisional/live.

### Watcher Restart, Crash, Stale State, Rotation, And Truncation

The first implementation is not required to solve log restart, crash, rotation,
or truncation diagnostics.

Required behavior:

- Do not read raw Player.log to detect these states.
- Do not hash raw Player.log to dedupe these states.
- If status needs to mention these states, report them as deferred or unknown.
- Route detailed diagnostics to a later issue.

## Side Effects

Allowed future Codex C side effects:

- Create or update Python source for a local/live SQLite ingest adapter.
- Add focused tests using in-memory or temporary SQLite databases.
- Update local app read-only status route metadata.
- Update process-control readiness metadata to recognize the new ingest adapter
  while keeping process start/stop and external transport disabled.

Forbidden side effects:

- Start or stop a live watcher.
- Tail, read, copy, hash, or store raw Player.log content.
- Store raw Player.log lines, raw saved-event lines, raw JSONL artifacts, or raw
  webhook payloads in SQLite.
- Create or commit SQLite database files, WAL/SHM/journal files, runtime logs,
  app-data files, raw logs, private JSONL artifacts, failed posts, workbook
  exports, secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs,
  environment values, or local-only artifacts.
- Trigger Google Sheets, webhook, Apps Script, workbook, production transport, AI,
  OpenAI runtime, Line Tracer, coaching, hidden-card inference, archetype
  inference, player-mistake labels, or gameplay advice.
- Expose arbitrary SQL, database browsing, destructive UI controls, or routine
  watcher start/stop browser controls.

## Backend Responsibility Boundary

Allowed backend responsibilities:

- Provide a local-only read-only status route for live SQLite capture readiness.
- Open the existing local analytics database only when an explicitly approved
  ingest call is made.
- Use existing analytics migration loader behavior.
- Call the live ingest adapter with parser-normalized final match/game rows.
- Return sanitized warnings and row counts.

Forbidden backend responsibilities:

- Read raw Player.log content.
- Start the existing parser runner.
- Start the tailer.
- Enable Sheets/webhook/App Script transport.
- Persist raw paths in API responses.
- Expose direct SQL execution or database browsing.
- Expose destructive controls.

## Frontend Responsibility Boundary

Allowed frontend responsibilities:

- Display read-only live SQLite capture status.
- Display whether final match/game live capture is supported, disabled, ready, or
  degraded.
- Display sanitized warnings.
- Use existing status-tone helpers where appropriate.

Forbidden frontend responsibilities:

- Start or stop the watcher.
- Trigger live capture directly from arbitrary user-provided data.
- Browse SQLite tables.
- Execute SQL.
- Display raw Player.log content.
- Display private absolute paths.
- Present parser-owned facts as coaching, Line Tracer, archetype, hidden-card,
  player-mistake, or best-line truth.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication semantics;
- analytics schema or migration files, unless Codex C finds the existing schema
  cannot represent the contracted first slice and routes back to Codex B;
- manual JSONL import semantics;
- replay ingest semantics beyond narrowly allowing or sharing code with
  `live_parser` as specified here;
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
- secrets, credentials, environment variables, API keys, tokens, webhook URLs, or
  spreadsheet IDs.

## Unknowns

- Whether the safest implementation is a separate live ingest module or an
  extension of `analytics_ingest.py`.
- Whether current parser final row surfaces expose enough provenance metadata for
  all desired analytics lineage fields.
- Whether a safe non-private live session identifier already exists in local app
  state.
- Whether actual watcher-to-ingest wiring should be authorized by this issue or a
  later issue after the adapter/status path is implemented and reviewed.
- Whether frontend status display is necessary in this slice or should remain
  backend-only.
- Whether manual JSONL imports and future live capture need explicit
  cross-source provenance conflict reporting after identical match/game facts are
  upserted.

## Suspected Gaps

- The SQLite schema permits `source_kind = live_parser`, but current ingest code
  rejects it.
- `live_watcher_process` currently marks live SQLite ingest contract presence as
  deferred.
- Existing analytics ingest hashes the full normalized replay payload for ingest
  run identity, which may not be ideal for incremental live writes.
- Existing parser runner is too broad to be a safe local-app live writer without
  additional no-transport guarantees.
- Current local app status surfaces do not show live SQLite capture readiness.
- Current tests assert `live_parser` is unsupported in the replay ingest path;
  these tests will need careful update if Codex C chooses to allow `live_parser`
  through shared normalization.

## Tests Required

Codex C should add focused tests before or with implementation.

Required test coverage:

- `live_parser` source kind is accepted by the approved live ingest path.
- Unsafe source labels remain rejected.
- Final/reconciled match rows are written to existing match-family tables.
- Final game rows are written to existing game-family tables.
- Repeating the same payload is idempotent and does not duplicate facts.
- A fact imported through manual/replay ingest and then seen by live capture does
  not create duplicate logical fact rows.
- Provisional/live match rows are rejected or skipped and do not overwrite final
  rows.
- Gameplay action, opponent-card observation, and field evidence live payloads
  are skipped or rejected with warnings in the first slice.
- The local status route, if added, returns sanitized metadata only.
- GET status calls do not create databases, generated files, logs, or app-data
  artifacts unless existing backend behavior already requires directory checks.
- Existing replay ingest and manual import tests still pass.
- Existing watcher process-control safeguard tests still pass and continue to
  report start/stop controls disabled.
- Existing runner/stream/tailer behavior is not invoked by local app status
  calls.
- Frontend tests pass if frontend status display is changed.

Recommended focused commands:

```powershell
py -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py
py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
py -m pytest -q tests/test_analytics_local_app_backend.py
py -m pytest -q tests/test_live_app_player_log_watcher_process_control_safeguards.py
py -m ruff check src tests
git diff --check
```

If Codex C changes frontend files:

```powershell
npm --prefix frontend test -- --run
npm --prefix frontend run build
```

If Codex C adds or changes local/private artifact boundaries:

```powershell
py tools\check_secret_patterns.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
```

## Validation Expectations

Codex C validation must prove:

- local SQLite live capture writes only parser-normalized final match/game facts;
- no raw Player.log content is stored or exposed;
- no private local path is returned in API payloads;
- existing replay/manual import behavior remains intact;
- existing process-control safeguards remain conservative;
- the implementation is idempotent;
- generated/private artifacts are not committed.

Codex E review must explicitly check:

- no parser truth moved into analytics or UI;
- no hidden raw log storage or hashing;
- no unintended runner/tailer/webhook/Sheets/App Script behavior;
- no accidental `main` target or production-facing behavior;
- all warnings/errors are sanitized.

## Acceptance Criteria

The issue is ready for Codex C when:

- this contract exists at
  `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`;
- the contract distinguishes observed behavior, required guarantees, unknowns,
  suspected gaps, and protected surfaces;
- the contract defines the first live-capture slice as final/reconciled
  match/game facts only;
- the contract preserves parser truth ownership;
- the contract forbids raw Player.log storage;
- the contract keeps watcher start/stop controls and actual tailing out of scope;
- the contract includes validation expectations and a pasteable Codex C handoff.

The Codex C implementation is acceptable only if:

- it keeps the change narrow;
- it produces an implementation comparison handoff;
- it validates the focused tests and hygiene checks listed above;
- it does not touch forbidden surfaces;
- it routes back to Codex B if schema changes, runner wiring, provisional facts,
  or live gameplay/opponent/field-evidence writes become necessary.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #244.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/244

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_parser_owned_fact_capture_sqlite.md

Goal:
Compare the current local app, watcher process safeguards, analytics ingest, and parser final row surfaces against the contract. Implement only the narrow approved first slice: a live SQLite capture boundary for parser-normalized final/reconciled match and game facts, plus read-only sanitized status reporting if needed.

Before editing:
- Confirm branch and git status.
- State what live parser-owned fact capture is supposed to do.
- State what current code is actually doing.
- State why live SQLite capture is currently blocked.
- State the exact minimal implementation plan.

Do:
- Preserve parser/state truth ownership.
- Use parser-normalized final/reconciled match and game rows only.
- Reuse existing analytics migration/upsert helpers where safe.
- Use source_kind = live_parser only through the approved live ingest boundary.
- Keep deterministic upserts/idempotency.
- Keep raw Player.log content out of SQLite and API payloads.
- Keep watcher start/stop controls disabled.
- Keep Google Sheets/webhook/App Script/output transport disabled.
- Add focused tests for final rows, duplicate writes, manual-import coexistence, provisional-row rejection/skipping, deferred gameplay/opponent/field-evidence live payloads, and status sanitization if status changes.
- Produce docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md.

Do not:
- Start or stop a live watcher.
- Tail, read, copy, hash, or store raw Player.log content.
- Invoke the broad parser runner unless a no-transport local-app runner mode is already proven and explicitly within the contract.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations, manual JSONL import semantics, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, AI/OpenAI/model-provider behavior, Line Tracer, coaching, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice.
- Create or commit SQLite database files, WAL/SHM/journal files, raw logs, private JSONL artifacts, runtime logs, app-data files, failed posts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, environment values, or local-only artifacts.
- Target main.
- Close #204 or #207.

Validation:
py -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py
py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
py -m pytest -q tests/test_analytics_local_app_backend.py
py -m pytest -q tests/test_live_app_player_log_watcher_process_control_safeguards.py
py -m ruff check src tests
git diff --check
py tools\check_secret_patterns.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation

If frontend files change, also run:
npm --prefix frontend test -- --run
npm --prefix frontend run build

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- files changed
- exact implementation sections changed
- comparison against contract
- validation run
- protected-surface status
- remaining risks/unknowns
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/244"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue problem representation for live parser-owned fact capture into SQLite"
  target_artifact: "docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md"
  contract_artifact: "docs/contracts/live_app_parser_owned_fact_capture_sqlite.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  contract_decision: "First slice is final/reconciled parser-owned match/game fact capture only; provisional facts, gameplay actions, opponent observations, field evidence, actual watcher start/stop, raw Player.log reads, and external transport remain out of scope."
  validation:
    - "Codex B should run git diff --check."
    - "Codex B should run protected-surface scan for the new contract path."
    - "Codex C should run focused analytics, local app, watcher process-control, ruff, secret, and protected-surface validation."
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not start or stop a live watcher unless a later contract explicitly authorizes it."
    - "Do not read, copy, hash, tail, or store raw Player.log contents."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime/local artifacts or secrets."
```
