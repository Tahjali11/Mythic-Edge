# Live App Parser-Owned Fact Capture SQLite Comparison

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/244
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

- Contract: `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- Risk tier: High
- Branch: `codex/analytics-foundation`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Internal Project Area

Local analytics SQLite ingest and local app live-status surfaces.

## Truth Owner

Parser/state remains the truth owner for match and game facts. Analytics SQLite
stores parser-normalized facts as local support data only. The local app status
route reports readiness only and does not own parser truth, analytics truth,
workbook truth, or AI truth.

## Bridge-Code Status

`bridge_code`: the implemented adapter bridges parser-owned final/reconciled
match and game rows into local SQLite. It does not parse raw Player.log content,
run the parser, start tailing, invoke transport, or infer match/game identity.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`

## Current Behavior Compared To Contract

Before this pass, `analytics_ingest.py` accepted only
`sanitized_golden_replay` and `saved_event_replay` through the parser-normalized
replay path. The SQLite schema already permitted `source_kind = live_parser`,
but the public ingest API rejected it. Existing replay ingest could write
match/game rows and optional gameplay/opponent/field-evidence rows when supplied.

The local app already exposed read-only Player.log path, watcher readiness, and
watcher process safeguard status. It did not expose
`GET /api/live/ingest/status`, and process preconditions still reported
`live_sqlite_ingest_contract_present` as deferred.

The remaining contract gap was a live-only adapter that accepts parser-owned
final/reconciled match/game rows, rejects private/raw inputs, preserves replay
semantics, and reports status without creating app-data or enabling watcher
process controls.

## Implementation Option Chosen

Implemented the contract's separate live-wrapper strategy:

- direct replay normalization still rejects `live_parser`;
- `ingest_live_parser_owned_facts(...)` is the only approved live entrypoint;
- shared lower-level ingest code writes the existing match/game fact families;
- optional gameplay, opponent-observation, and field-evidence live payloads are
  skipped with explicit warnings rather than written;
- local status remains disabled/status-only.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md`

The contract file remains untracked from Codex B:

- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`

## Exact Code And Test Sections Changed

### `src/mythic_edge_parser/app/analytics_ingest.py`

- Added `LIVE_PARSER_OWNED_FACT_CAPTURE_SCHEMA_VERSION`.
- Added live-only constants for `live_parser`, allowed finalities, deferred fact
  families, and forbidden raw/private payload fields.
- Added `normalize_live_parser_owned_facts(...)`.
- Added `ingest_live_parser_owned_facts(...)`.
- Split replay execution into `_ingest_normalized_replay(...)` so replay and live
  wrappers share existing match/game upsert helpers while preserving public
  replay validation.
- Added live safety helpers:
  - `_validate_safe_source_artifact_label(...)`
  - `_required_live_safe_label(...)`
  - `_reject_live_forbidden_payload_fields(...)`
  - `_require_live_final_rows(...)`
  - `_live_row_finality(...)`
  - `_live_payload_warnings(...)`
  - `_live_payload_skips(...)`
- Preserved direct replay `source_kind` validation, so
  `normalize_parser_normalized_replay({"source_kind": "live_parser", ...})`
  still fails.

### `src/mythic_edge_parser/local_app/setup_status.py`

- Added `LIVE_SQLITE_CAPTURE_SCHEMA_VERSION`.
- Added `LIVE_SQLITE_CAPTURE_STATUS_OBJECT`.
- Added `build_live_sqlite_capture_status(...)`.
- Added `live_sqlite_capture` section to setup status.

### `src/mythic_edge_parser/local_app/backend.py`

- Added read-only `GET /api/live/ingest/status`.

### `src/mythic_edge_parser/local_app/live_watcher_process.py`

- Updated `live_sqlite_ingest_contract_present` precondition from deferred to
  pass.
- Left `start_allowed`, `stop_allowed`, `parser_runner_started`,
  `tailing_started`, `sqlite_live_writes_enabled`, and
  `external_transport_allowed` false.

### Tests

- Added `tests/test_live_app_parser_owned_fact_capture_sqlite.py`.
- Updated `tests/test_analytics_local_app_backend.py` to include the new route in
  read-only no-artifact GET coverage and status-shape assertions.
- Updated `tests/test_analytics_local_app_config.py` to assert the process
  precondition is now present while process control remains disabled.

## Code Changed

Yes. Runtime code changed only in local analytics ingest and local app
status/safeguard metadata.

No parser/state behavior, parser final reconciliation, event classes,
match/game identity, deduplication rules, workbook schema, webhook payload,
Apps Script, Google Sheets, OpenAI/AI, or production behavior was changed.

## Tests Added Or Updated

Added focused live ingest tests for:

- public live schema-version constant;
- `live_parser` accepted only by `ingest_live_parser_owned_facts(...)`;
- final match/game rows written to existing match/game fact tables;
- idempotent repeat live payloads;
- replay then live for the same logical facts does not duplicate fact rows;
- unsafe live labels and forbidden raw/private payload fields rejected;
- live/provisional rows rejected without overwriting final facts;
- gameplay/opponent/field-evidence live payloads skipped with warnings;
- no generated SQLite files created by in-memory tests.

Updated local app tests for:

- `GET /api/live/ingest/status`;
- no app-data creation from read-only GET status calls;
- sanitized symbolic status payload;
- disabled/status-only capability flags;
- process-control safeguards remaining false.

## Interface Changes

Added public Python interface:

```python
ingest_live_parser_owned_facts(connection, payload, *, started_at=None, finished_at=None)
```

Added public normalizer:

```python
normalize_live_parser_owned_facts(payload)
```

Added local app route:

```text
GET /api/live/ingest/status
```

Added status object:

```text
mythic_edge_local_app_live_parser_sqlite_capture_status
```

Added schema version:

```text
live_app_parser_owned_fact_capture_sqlite.v1
```

No workbook columns, webhook payload fields, Apps Script entrypoints, external
connectors, environment variables, CI gates, or production routes were added.

## Contracted Area Status

Implementation stayed inside the contracted local analytics/local app bridge
area. The adapter writes only existing parser-normalized match/game fact
families. The status route is read-only and does not create directories,
databases, generated artifacts, local app runtime files, or private payloads.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
git diff --check
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
py -m ruff check src tests tools
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
<touched paths> | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
<touched paths> | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Results:

- `git status --short --branch --untracked-files=all` -> branch
  `codex/analytics-foundation`, modified implementation/test files and
  untracked Codex B contract, handoff, and new focused test.
- `git diff --check` -> passed.
- `tests\test_live_app_parser_owned_fact_capture_sqlite.py` -> passed, 8 passed
- `tests\test_analytics_parser_normalized_replay_ingest.py` -> passed, 24 passed
- `tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py` -> passed, 34 passed, 1 existing FastAPI/Starlette deprecation warning
- `tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py` -> passed, 77 passed
- `py -m ruff check src tests tools` -> passed.
- `py tools\check_agent_docs.py` -> passed, 46 checked files, 0 errors, 0 warnings.
- `py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation` -> passed, 0 changed paths reported because worktree edits are uncommitted.
- `py tools\check_secret_patterns.py --base origin/codex/analytics-foundation` -> passed, 0 changed paths reported because worktree edits are uncommitted.
- Path-scoped protected-surface scan over 9 touched/untracked paths -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over 9 touched/untracked paths -> passed, forbidden 0, warnings 0.

## Protected-Surface Status

No protected parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI or
production behavior was intentionally touched.

Touched runtime surfaces are limited to:

- analytics SQLite ingest support;
- local app read-only status;
- local app watcher process safeguard metadata.

## Secret And Private Marker Status

The new live ingest wrapper rejects raw/private fields including Player.log
lines, saved-event lines, webhook payloads, raw local paths, Player.log paths,
private source paths, and raw log hashes. The local status route returns
symbolic `<app_data>` display paths only.

Path-scoped scanner status over touched/untracked files: forbidden 0,
warnings 0.

## Generated Artifact Status

Focused tests use in-memory SQLite or temporary app-data roots. The read-only
status route does not create app-data, job state, or database files.

No SQLite database files, raw Player.log data, raw saved-event lines, runtime
status files, failed posts, workbook exports, local JSONL artifacts, or
generated/private local artifacts were created or committed.

## Still Unverified

- Live browser smoke for the new status route.
- Actual approved live-mode caller wiring.
- Actual private Player.log smoke.
- Real app-data database write path outside synthetic/in-memory tests.
- Deployed Apps Script state.
- Live workbook state.
- Production behavior.

## Reviewer Focus

Codex E should pay special attention to:

- whether `session_id` validation without writing the `sessions` table is the
  right scope for this contract;
- whether live payload deferred-family behavior should remain warning/skip or be
  fail-closed;
- whether `GET /api/live/ingest/status` exposes only symbolic, non-private
  status data;
- whether direct replay import remains unchanged for `sanitized_golden_replay`
  and `saved_event_replay`;
- whether the adapter writes only allowed fact families and does not enable
  watcher process controls.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #244.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/244

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_parser_owned_fact_capture_sqlite.md

Implementation handoff:
docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md

Risk tier:
High

Goal:
Review the Codex C implementation against the live app parser-owned fact capture SQLite contract. Lead with findings ordered by severity. Verify that only the narrow live parser-owned final/reconciled match/game SQLite capture boundary and read-only status route were implemented.

Review focus:
- Confirm direct replay ingest still rejects live_parser except through the new live adapter.
- Confirm ingest_live_parser_owned_facts accepts only source_kind live_parser, safe source_artifact_label, safe session_id, and final/reconciled match/game rows.
- Confirm raw Player.log lines, saved-event lines, webhook payloads, raw/local paths, Player.log paths, private source paths, and raw log hashes are rejected.
- Confirm gameplay-action, opponent-card-observation, and field-evidence live payloads are not written in this slice.
- Confirm repeated live ingest and replay-then-live ingest do not duplicate logical fact rows.
- Confirm GET /api/live/ingest/status is disabled/status-only, symbolic, and does not create app-data or databases.
- Confirm watcher process controls remain disabled and no runner/tailer calls are introduced.
- Confirm parser/state behavior, final reconciliation, event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script, Sheets, AI/OpenAI, and production behavior were not changed.

Required validation:
git status --short --branch
git diff --check
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
py -m ruff check src tests tools
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation

Do not:
- Target main.
- Stage, commit, push, open a PR, merge, close issues, or mark tracker #204 complete.
- Change parser/runtime/workbook/webhook/App Script/Sheets/analytics truth/OpenAI/AI/coaching/production behavior.
- Create or commit SQLite/generated/private/runtime artifacts or secrets.
- Start the parser runner, tail Player.log, inspect private Player.log contents, or write to actual app-data root unless explicitly approved.

Final review report must include:
- role performed
- issue/tracker/umbrella issue
- contract and handoff reviewed
- branch and git status
- findings ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- whether implementation is ready for Codex F or needs Codex D fixes
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/244"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/live_app_parser_owned_fact_capture_sqlite.md"
  target_artifact: "docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check -> passed"
    - "focused live adapter tests -> passed"
    - "focused replay ingest tests -> passed"
    - "focused local app backend/config tests -> passed"
    - "adjacent gameplay/opponent/field-evidence ingest tests -> passed"
    - "ruff -> passed"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main."
    - "Do not start parser runner or tail Player.log."
    - "Do not inspect private Player.log contents or write actual app-data root without explicit approval."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
