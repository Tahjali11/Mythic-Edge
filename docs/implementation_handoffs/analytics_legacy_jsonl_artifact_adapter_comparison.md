# Analytics Legacy JSONL Artifact Adapter Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue And Tracker

- Issue: No new issue opened by Codex B.
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Source Artifact Used

Chat problem representation for legacy JSONL artifact adapter.

## Contract Used

`docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`

## Branch And Git Status

- Branch target: `codex/analytics-foundation`
- Current branch confirmed: `codex/analytics-foundation`
- Starting `HEAD`: `be86be8e533604c79aa0000a0f1b11a564cd5d14`
- `git fetch --prune`: completed
- Branch sync check: `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` returned `0 0`
- Tracker check: issue #204 is open
- Prior CLI problem representation check: issue #205 is closed
- Initial worktree status:
  - `?? docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`

The untracked contract file was treated as the source artifact for this pass.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_saved_event_replay.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_replay_view_harness.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_parser_regressions.py`
- `tests/test_match_summary_from_match_state.py`

## Current Behavior Compared To Contract

### Contract Matches Before Implementation

- `saved_event_replay.py` already reconstructs supported generated JSONL records into event objects through `EVENT_CLASS_BY_KIND`.
- `saved_event_replay.latest_jsonl_files(...)` already preserves highest-version-per-day file selection semantics for folders.
- `saved_event_replay.replay_latest_saved_events(...)` already dedupes nonblank `raw_bytes_hash` values during one replay.
- `state.py` already exposes reset, event-update, match-row, game-row, and summary iteration helpers.
- `analytics_ingest.py` already accepts parser-normalized replay mappings with `source_kind = "saved_event_replay"`.
- `analytics_ingest.py` already rejects unsafe source artifact labels that look like local paths or URLs.
- Existing analytics ingest tests already prove in-memory SQLite compatibility for parser-normalized replay inputs.

### Contract Mismatches Before Implementation

- No `analytics_legacy_jsonl_adapter.py` module existed.
- No public adapter schema-version constant existed.
- No adapter function converted generated legacy JSONL artifacts into parser-normalized replay mappings.
- No result object exposed adapter stats such as records seen, processed events, skipped events, unsupported kinds, or warnings.
- No focused tests proved legacy `derived` fields are ignored as parser truth.
- No focused tests proved unsupported event kinds are skipped and counted safely.
- No focused tests proved duplicate `raw_bytes_hash` values are deduped in adapter output.
- No focused tests proved adapter output can be ingested into in-memory SQLite without storing raw saved-event lines.

### Missing Safeguards Or Missing Tests Before Implementation

- No source-label validation owned by the adapter.
- No adapter-level clear errors for missing sources, non-JSONL files, invalid JSON, non-object records, malformed supported event records, or no ingestable match/game rows.
- No adapter-level state-isolation test coverage.
- No test checked that adapter tests avoid creating runtime status/action-log/generated SQLite artifacts.
- No test checked folder input through existing latest-file selection semantics.

## Implementation Option Chosen

Implemented the smallest local adapter slice authorized by the contract:

- Added a new app module, `analytics_legacy_jsonl_adapter.py`.
- Reused `saved_event_replay.EVENT_CLASS_BY_KIND`, `event_from_saved_record(...)`, and `latest_jsonl_files(...)`.
- Reused current parser/state behavior via `state._update_match_summary(...)`, `state.build_match_log_row(...)`, and `state.build_game_summary_rows(...)`.
- Reset parser runtime state before and after every adapter call.
- Seeded an empty in-memory card lookup to avoid card-catalog bootstrap side effects during replay.
- Supported both single `.jsonl` file input and folder input using existing latest-file selection semantics.
- Counted unsupported event kinds and duplicate hashes without failing the whole adapter.
- Ignored legacy `derived` values as facts, with a safe mismatch warning when a safe derived match id disagrees with produced match rows.
- Returned a parser-normalized replay mapping with empty first-pass lists for gameplay actions, opponent-card observations, and field evidence.
- Kept SQLite writes out of the adapter; compatibility is tested only with `sqlite3.connect(":memory:")`.

## Files Changed

- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `docs/implementation_handoffs/analytics_legacy_jsonl_artifact_adapter_comparison.md`

Related source artifact present but not edited by this pass:

- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`

## Exact Code, Test, Doc, And Schema Sections Changed

### `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`

Added:

- `ANALYTICS_LEGACY_JSONL_ADAPTER_SCHEMA_VERSION`
- `LegacyJsonlAdapterError`
- `LegacyJsonlAdapterResult`
- `adapt_legacy_jsonl_artifacts(...)`
- JSONL source selection, source-label validation, safe path labels, unsupported-kind counting, duplicate hash dedupe, parser state reset, replay bundle construction, and safe warning helpers.

### `tests/test_analytics_legacy_jsonl_artifact_adapter.py`

Added focused coverage for:

- public schema-version constant;
- synthetic generated JSONL adapting to `source_kind = "saved_event_replay"`;
- safe `source_artifact_label` behavior;
- match/game rows produced from current parser state;
- deliberately wrong legacy `derived.match_id` not affecting produced rows;
- unsupported event kinds counted/skipped;
- duplicate `raw_bytes_hash` values deduped;
- adapter output accepted by `normalize_parser_normalized_replay(...)`;
- adapter output ingested into in-memory SQLite through `ingest_parser_normalized_replay(...)`;
- folder input preserving latest-file selection semantics;
- unsafe source label rejection;
- invalid JSON failure without raw-line echo;
- non-object record failure;
- malformed supported event-record failure without payload dump;
- no ingestable rows failure;
- no generated SQLite, runtime status, runtime log, or failed-post artifacts created by adapter tests.

### Handoff Document

Added this implementation comparison artifact.

### Schema And Migration Files

No SQLite schema, migration, workbook schema, webhook payload, or Apps Script files were changed.

## Change Type

- Code changed: yes, local analytics adapter support only.
- Tests changed: yes, focused synthetic adapter tests.
- Docs changed: yes, implementation handoff only.
- Schema-artifact-only: no.
- Adapter-support-only: yes.

## Validation Run And Result

Validation completed:

- `git status --short --branch`
  - branch: `codex/analytics-foundation...origin/codex/analytics-foundation`
  - initial only-untracked source artifact: `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- `git fetch --prune`
  - passed
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation`
  - passed: `0 0`
- `gh issue view 204 --json number,state,title,url`
  - passed: issue #204 is `OPEN`
- `gh issue view 205 --json number,state,title,url`
  - passed: issue #205 is `CLOSED`
- `py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py`
  - passed: `8 passed`
- `py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_saved_event_replay.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_replay_view_harness.py`
  - passed: `60 passed`
- `py -m ruff check src\mythic_edge_parser\app\analytics_legacy_jsonl_adapter.py tests\test_analytics_legacy_jsonl_artifact_adapter.py`
  - passed
- `py -m ruff check src tests`
  - passed
- `git diff --check`
  - passed
- path-scoped protected-surface check over the contract, adapter module, adapter tests, and handoff
  - passed: `forbidden: 0`, `warnings: 0`
- path-scoped secret/private-marker scan over the contract, adapter module, adapter tests, and handoff
  - passed: `forbidden: 0`, `warnings: 0`
- generated SQLite artifact status check
  - passed: no `.sqlite`, `.sqlite3`, `.db`, `.db-journal`, `.db-wal`, or `.db-shm` files were found under `data`

## Protected-Surface Status

No protected parser/runtime/workbook/webhook/App Script behavior was intentionally changed.

Touched implementation scope was limited to:

- local analytics legacy JSONL adapter support;
- focused synthetic tests for that adapter;
- this implementation handoff.

No changes were made to:

- parser behavior;
- parser state final reconciliation behavior;
- parser event classes;
- match/game identity or deduplication behavior;
- SQLite schema or migrations;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- AI/OpenAI runtime behavior;
- production behavior;
- CI gates or merge policy.

## Secret And Private-Marker Status

No secrets, credentials, webhook URLs, workbook IDs, raw `Player.log` payloads, raw saved-event lines, local JSONL artifacts, local absolute artifact paths, runtime status payloads, retry-queue payloads, generated data, workbook exports, or SQLite database files were intentionally added.

The adapter tests use only synthetic temporary JSONL content created inside pytest `tmp_path`.

## Generated SQLite Artifact Status

No SQLite database files were intentionally created or committed. Compatibility tests use in-memory SQLite only.

## Local JSONL Artifact Status

No local JSONL artifact was committed, copied, sanitized, fixtured, or raw-dumped.

Synthetic JSONL test records are generated inside pytest temporary directories only.

## Raw Player.log And Saved-Event Storage Status

No raw `Player.log` payloads are stored in SQLite.

No raw saved-event lines are stored in SQLite.

The adapter output contains parser-normalized match/game rows and empty first-pass optional analytics lists only.

## Runtime, Sheets, And AI Integration Status

No CLI, live ingest, runtime integration, Google Sheets sync, workbook behavior, Apps Script behavior, AI coaching, or OpenAI runtime integration was added.

## What Remains Unverified

- Full repository test suite.
- Real private local legacy JSONL artifact behavior.
- Whether every local legacy JSONL day has final match evidence sufficient for match/game row output.
- Future pure in-memory gameplay-action extraction.
- Future field-evidence emission from replayed legacy JSONL.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.

## Forbidden Scope Status

No forbidden scope was intentionally touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for the analytics legacy JSONL artifact adapter.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_legacy_jsonl_artifact_adapter.md

Implementation handoff:
docs/implementation_handoffs/analytics_legacy_jsonl_artifact_adapter_comparison.md

Risk tier:
Medium-High

Goal:
Review the Codex C implementation against docs/contracts/analytics_legacy_jsonl_artifact_adapter.md. Lead with findings ordered by severity. Verify that the adapter converts generated legacy JSONL event archives into parser-normalized replay mappings accepted by analytics ingest without trusting legacy derived fields, storing raw payloads, creating database files, adding a CLI, or changing parser/runtime/workbook/webhook/App Script/Sheets/AI behavior.

Before reviewing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and identify unrelated or untracked files.
- Confirm docs/contracts/analytics_legacy_jsonl_artifact_adapter.md is the source contract.
- Read the contract and implementation handoff before inspecting code.
- Inspect:
  - src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
  - tests/test_analytics_legacy_jsonl_artifact_adapter.py
  - src/mythic_edge_parser/app/saved_event_replay.py
  - src/mythic_edge_parser/app/analytics_ingest.py
  - src/mythic_edge_parser/app/state.py
  - src/mythic_edge_parser/app/models.py
  - tests/test_saved_event_replay.py
  - tests/test_analytics_parser_normalized_replay_ingest.py
  - tests/test_analytics_replay_view_harness.py

Review for:
- contract matches;
- contract mismatches;
- missing safeguards;
- missing tests;
- unintended parser/runtime/workbook/webhook/App Script/Sheets/AI behavior changes;
- unsafe source labels, warnings, or error messages;
- raw payload, raw Player.log, raw saved-event, local path, webhook URL, workbook ID, secret, or credential leakage;
- generated SQLite or runtime artifact creation;
- state isolation before and after adapter calls;
- folder input preserving saved_event_replay.latest_jsonl_files(...) semantics;
- unsupported event kind counting and duplicate raw_bytes_hash dedupe;
- whether empty gameplay_action_entries, opponent_card_observations, and field_evidence_entries are acceptable for this first pass.

Do not:
- implement fixes unless explicitly asked after the review;
- target main unless explicitly approved;
- commit, copy, sanitize, fixture, or raw-dump local JSONL artifacts;
- store raw Player.log payloads or raw saved-event lines in SQLite;
- treat legacy derived fields as parser truth;
- add a CLI in this adapter slice;
- change parser behavior, runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, AI/OpenAI runtime behavior, production behavior, or SQLite schema;
- create SQLite database files;
- touch secrets, credentials, generated data, runtime artifacts, retry-queue payloads, workbook exports, raw logs, or local-only artifacts;
- stage, commit, push, open a PR, merge, or close issues unless explicitly asked.

Validation:
git status --short --branch
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_saved_event_replay.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests
git diff --check

Also run path-scoped secret/private-marker and protected-surface checks over:
- docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- docs/implementation_handoffs/analytics_legacy_jsonl_artifact_adapter_comparison.md

Produce:
docs/contract_test_reports/analytics_legacy_jsonl_artifact_adapter.md

Final review report must include:
- role performed
- tracker and contract reviewed
- implementation handoff reviewed
- files reviewed
- findings first, ordered by severity
- contract matches
- contract mismatches
- missing tests or safeguards
- validation run and result
- protected-surface status
- secret/private-marker status
- generated SQLite artifact status
- local JSONL artifact status
- whether forbidden scope was touched
- whether this should route to Codex D, Codex B, or Codex F
- pasteable next-thread prompt
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "No new issue opened by Codex B"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  role_performed: "Codex C: Module Implementer / comparison thread"
  completed_thread: "C"
  next_thread: "E"
  branch: "codex/analytics-foundation"
  source_artifact: "chat problem representation for legacy JSONL artifact adapter"
  contract_artifact: "docs/contracts/analytics_legacy_jsonl_artifact_adapter.md"
  target_artifact: "docs/implementation_handoffs/analytics_legacy_jsonl_artifact_adapter_comparison.md"
  risk_tier: "Medium-High"
  code_changed: true
  tests_changed: true
  docs_changed: true
  schema_changed: false
  validation:
    - "git fetch --prune -> passed"
    - "git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0"
    - "gh issue view 204 -> OPEN tracker"
    - "gh issue view 205 -> CLOSED prior CLI problem representation"
    - "py -m pytest -q tests\\test_analytics_legacy_jsonl_artifact_adapter.py -> passed, 8 passed"
    - "py -m pytest -q tests\\test_analytics_legacy_jsonl_artifact_adapter.py tests\\test_saved_event_replay.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_replay_view_harness.py -> passed, 60 passed"
    - "py -m ruff check src\\mythic_edge_parser\\app\\analytics_legacy_jsonl_adapter.py tests\\test_analytics_legacy_jsonl_artifact_adapter.py -> passed"
    - "py -m ruff check src tests -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "generated SQLite artifact status check -> no SQLite DB artifacts found under data"
  remaining_unverified:
    - "Full repository test suite"
    - "Real private local legacy JSONL artifact behavior"
    - "Whether every local legacy JSONL day has final match evidence sufficient for match/game row output"
    - "Future pure in-memory gameplay-action extraction"
    - "Future field-evidence emission from replayed legacy JSONL"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
  stop_conditions:
    - "Do not target main unless explicitly approved."
    - "Do not commit, copy, sanitize, fixture, or raw-dump local JSONL artifacts."
    - "Do not store raw Player.log payloads or raw saved-event lines in SQLite."
    - "Do not treat legacy derived fields as parser truth."
    - "Do not add a CLI in this adapter slice."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/AI behavior."
```
