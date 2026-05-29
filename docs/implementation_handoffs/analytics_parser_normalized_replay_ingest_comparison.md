# Analytics Parser-Normalized Replay Ingest Implementation Handoff

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifact Used

Codex A workflow handoff for:

```text
[analytics] Define parser-normalized replay ingest into SQLite
```

## Contract Used

`docs/contracts/analytics_parser_normalized_replay_ingest.md`

## Branch And Git Status

Branch confirmed:

```text
codex/analytics-foundation
```

Initial status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/analytics_parser_normalized_replay_ingest.md
```

The untracked contract was treated as the supplied Codex B artifact. No
unrelated modified files were present at the start of this pass.

Status after implementation, before final validation:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/analytics_parser_normalized_replay_ingest.md
?? src/mythic_edge_parser/app/analytics_ingest.py
?? tests/test_analytics_parser_normalized_replay_ingest.py
?? docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md
```

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_migration_loader.md`
- `docs/implementation_handoffs/analytics_migration_loader_comparison.md`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_migration_loader.py`
- `tests/test_app_models.py`
- `tests/test_golden_replay_harness.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`

## Current Behavior Compared To Contract

Current repo behavior already provided:

- SQLite schema v1 under
  `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`.
- Package-resource migration loading and application through
  `src/mythic_edge_parser/app/analytics_migration_loader.py`.
- In-memory schema and migration-loader tests.
- Parser-owned `MatchLogRow` and `GameLogRow` dictionaries from
  `src/mythic_edge_parser/app/models.py`.
- Gameplay action and opponent-card-observation normalized payload surfaces,
  but no SQLite ingest path for those optional payloads.

Contract gaps before this pass:

- No `src/mythic_edge_parser/app/analytics_ingest.py` module existed.
- No public API accepted parser-normalized replay bundles.
- No code wrote parser-owned match/game row dictionaries into SQLite fact
  tables.
- No deterministic `ingest_run_id` existed for replay idempotency.
- No ingest tests covered migration plus ingest, row counts, provenance labels,
  fact provenance, malformed identity rollback, or generated database artifact
  safety.

## Implementation Option Chosen

Implemented the contract's recommended first-pass option:

```text
deterministic ingest_run_id derived from source_kind, source_artifact_label,
and a canonical hash of parser-normalized input
```

Implemented only core parser-normalized row ingest:

- `MatchLogRow` to `matches`
- `MatchLogRow` to `match_results`
- `MatchLogRow` to `match_context`
- `MatchLogRow` rank fields to `rank_snapshots` when rank fields are present
- `GameLogRow` to `games`
- `GameLogRow` to `game_results`
- `GameLogRow` opening-hand fields to `opening_hands`
- `GameLogRow` semicolon-delimited opening-hand display names to
  `opening_hand_cards`
- `GameLogRow` mulligan count to `mulligan_events`
- `GameLogRow` semicolon-delimited mulliganed-away display names to
  `mulligan_bottomed_or_discarded_cards`
- focused `fact_provenance` rows for match identity/result, game result,
  opening hand, and mulligan event facts

Deferred optional payloads:

- `gameplay_action_entries`
- `opponent_card_observations`
- `field_evidence_entries`

The function accepts those optional keys, reports them in `warnings` and
`skipped`, and leaves their SQLite tables empty for a later focused ingest
slice.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md`

Source artifact present but not edited by this implementation thread:

- `docs/contracts/analytics_parser_normalized_replay_ingest.md`

## Exact Ingest, Test, And Doc Sections Changed

### `src/mythic_edge_parser/app/analytics_ingest.py`

Added public constant:

- `ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION`

Added public data/error shapes:

- `AnalyticsReplayIngestError`
- `ParserNormalizedReplayInput`
- `AnalyticsReplayIngestResult`

Added public functions:

- `normalize_parser_normalized_replay(replay)`
- `deterministic_ingest_run_id(replay)`
- `ingest_parser_normalized_replay(connection, replay, *, started_at=None, finished_at=None)`

Behavior added:

- validates `source_kind` as `sanitized_golden_replay` or `saved_event_replay`
- rejects blank or local-path/URL-like `source_artifact_label` values
- normalizes match/game row input lists without parsing raw logs
- applies analytics migrations before fact writes
- opens one ingest transaction for fact writes
- writes one deterministic `ingest_runs` row per identical replay input
- upserts deterministic fact IDs for match/game/core decision facts
- maps `game_id` as `<match_id>:g<game_number>`
- fails clearly on missing match id or invalid game number
- rolls back failed ingest transactions without partial fact rows
- splits parser-owned semicolon-delimited card display lists into child rows
- stores name-only card rows with `grp_id = NULL`
- uses `identity_hint_source='name_only_from_parser_row'`
- populates core provenance columns with safe fallback labels
- writes deterministic `fact_provenance` rows with label/path-only
  `source_payload_paths`
- reports optional gameplay/action/evidence payloads as skipped/deferred

### `tests/test_analytics_parser_normalized_replay_ingest.py`

Added focused tests for:

- public replay-ingest schema-version constant
- migration plus ingest on an empty in-memory SQLite connection
- expected rows in `ingest_runs`, `matches`, `games`, `match_results`,
  `game_results`, `match_context`, `rank_snapshots`, `opening_hands`,
  `opening_hand_cards`, `mulligan_events`,
  `mulligan_bottomed_or_discarded_cards`, and `fact_provenance`
- deterministic ingest run IDs
- replay idempotency for identical parser-normalized input
- row counts in the result and `ingest_runs.row_counts_json`
- safe core provenance fallback labels
- fact provenance path labels without raw payloads, local paths, or URLs
- empty optional decision fields not being coerced into zero/false
- name-only opening-hand cards not claiming `grp_id`
- missing match id rollback without partial fact rows
- malformed game number rollback without partial fact rows
- unsupported source kind and unsafe artifact label errors
- deferred optional payloads reported in `warnings` and `skipped`
- no generated SQLite files created under `data/analytics/`

### `docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md`

Added this handoff.

## Code Changed, Tests Changed, Docs-Only, Schema-Artifact-Only, Or Ingest-Support-Only

Code, tests, and docs changed.

This is ingest-support-only local analytics code. It is not wired into live
runtime paths and does not change parser truth, parser runtime, workbook,
webhook, Apps Script, or production behavior.

## Interface Changes

New local analytics support API:

```text
mythic_edge_parser.app.analytics_ingest
```

Public constant:

- `ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION`

Public data/error shapes:

- `AnalyticsReplayIngestError`
- `ParserNormalizedReplayInput`
- `AnalyticsReplayIngestResult`

Public functions:

- `normalize_parser_normalized_replay(replay)`
- `deterministic_ingest_run_id(replay)`
- `ingest_parser_normalized_replay(connection, replay, *, started_at=None, finished_at=None)`

No parser payloads, workbook fields, webhook payloads, Apps Script entrypoints,
environment variables, CLI commands, live runtime wiring, or production
surfaces changed.

## Contract Matches

- Ingest accepts already-normalized parser row dictionaries.
- Ingest does not parse raw `Player.log`.
- Ingest does not run saved-event replay.
- Ingest uses the existing analytics migration loader before writes.
- Ingest writes to caller-supplied SQLite connections only.
- Ingest uses deterministic `ingest_run_id` values.
- Replaying the same normalized input twice does not duplicate fact rows.
- Missing match id fails clearly and leaves no partial fact rows.
- Invalid game number fails clearly and leaves no partial fact rows.
- Empty optional decision fields are not coerced into zero or false.
- Name-only opening-hand and mulliganed-away child card rows use `grp_id = NULL`.
- Core parser fact rows receive safe provenance/status labels.
- Focused `fact_provenance` rows are written with label/path-only payload paths.
- Optional gameplay/action/evidence payloads are deferred and reported as
  skipped rather than guessed.
- No generated SQLite database files were created or committed.
- No live ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI
  runtime integration, parser behavior change, workbook schema change, webhook
  payload change, Apps Script change, or production behavior was introduced.

## Contract Mismatches

None known after this implementation.

## Missing Safeguards Or Tests

Remaining follow-up scope intentionally not implemented:

- No gameplay action SQLite ingest.
- No opponent-card-observation SQLite ingest.
- No field-evidence override handling.
- No default database opener.
- No CLI.
- No live parser ingest.
- No saved-event replay runner.
- No raw replay parser.
- No production bootstrap or runtime integration.
- No reconciliation policy for re-ingesting a different normalized payload with
  the same parser fact IDs.

## Validation Run

Completed before final safety-gate refresh:

```text
py -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py tests/test_analytics_migration_loader.py -> 40 passed
py -m pytest -q tests/test_app_models.py tests/test_golden_replay_harness.py -> 29 passed
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 26 passed
py -m ruff check src/mythic_edge_parser/app/analytics_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py -> All checks passed!
py -m ruff check src tests tools -> All checks passed!
```

Final safety gates after handoff creation:

```text
git status --short --branch -> showed intended untracked contract, ingest module, test, and handoff files only
git diff --check -> passed
py tools/check_agent_docs.py -> passed; errors 0, warnings 0
path-scoped secret/private-marker scan over touched files -> forbidden 0, warnings 1
path-scoped protected-surface check over touched files -> forbidden 0, warnings 0
generated SQLite artifact status check -> no changed or untracked SQLite DB/journal/WAL/SHM artifacts found
```

## Protected-Surface Status

Local analytics ingest-support/test/docs changes only.

Path-scoped protected-surface gate over touched files passed with forbidden 0
and warnings 0. No parser/runtime/workbook/webhook/App Script/protected
surfaces were intentionally touched.

## Secret And Private-Marker Status

Path-scoped secret/private-marker scan over touched files returned forbidden 0
and warnings 1. The warning is in the supplied contract's protected-surface
wording for failed-post payloads, not in executable code or generated data.

No secrets, raw logs, webhook URLs, workbook IDs, deployment IDs, generated
data, local runtime artifacts, workbook exports, or local source paths were
intentionally added.

The ingest code rejects local-path/URL-like `source_artifact_label` values and
generates `fact_provenance.source_payload_paths` from safe parser field labels.

## Generated SQLite Artifact Status

Tests use in-memory SQLite connections. No changed or untracked SQLite
database files, journal files, WAL files, SHM files, or DB files were found.

Focused tests compare generated SQLite artifact state before and after ingest
to prove this module does not create files under `data/analytics/`.

## Raw Player.log And Saved-Event Replay Status

No raw `Player.log` parsing was added.

No saved-event replay execution was added. `source_kind='saved_event_replay'`
is accepted only as a label for already-normalized replay bundles.

## Ingest, CLI, And Runtime Integration Status

Added local parser-normalized replay ingest support only.

No live ingest, CLI, default database opener, runtime integration, Google
Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or
production behavior was added.

## Still Unverified

- GitHub Actions were not run locally.
- Clean installed-wheel import was not tested for the new ingest module.
- Gameplay action ingest remains deferred.
- Opponent-card-observation ingest remains deferred.
- Field-evidence label override behavior remains deferred.
- Live workbook state was not checked.
- Deployed Apps Script state was not checked.
- Production behavior was not checked.

## Forbidden Scope Touched

No forbidden scope was intentionally touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for [analytics] parser-normalized replay ingest into SQLite.

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_parser_normalized_replay_ingest.md

Implementation handoff:
docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md

Expected changed files:
- src/mythic_edge_parser/app/analytics_ingest.py
- tests/test_analytics_parser_normalized_replay_ingest.py
- docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md

Source artifact present:
- docs/contracts/analytics_parser_normalized_replay_ingest.md

Task:
Review the implementation against docs/contracts/analytics_parser_normalized_replay_ingest.md. Lead with findings ordered by severity. Verify that the ingest module accepts already-normalized parser row dictionaries, writes only to caller-supplied SQLite connections, uses the existing migration loader, preserves parser truth ownership, and does not add raw Player.log parsing, saved-event replay execution, live ingest, CLI, runtime integration, workbook/webhook/App Script changes, or production behavior.

Check especially:
- deterministic ingest_run_id behavior
- replay idempotency for identical normalized input
- all-or-nothing rollback for missing match id and malformed game number
- MatchLogRow mappings to matches, match_results, match_context, and rank_snapshots
- GameLogRow mappings to games, game_results, opening_hands, opening_hand_cards, mulligan_events, and mulligan_bottomed_or_discarded_cards
- name-only card rows use grp_id = NULL and do not claim durable card identity
- row_counts and ingest_runs.row_counts_json match actual fact-table counts
- core provenance/status labels are safe fallback labels
- fact_provenance.source_payload_paths contain labels/paths only, not raw payloads, local paths, URLs, workbook IDs, webhook URLs, or secrets
- optional gameplay_action_entries, opponent_card_observations, and field_evidence_entries are explicitly deferred/skipped
- tests do not create data/analytics/mythic_edge.sqlite3 or SQLite journal/WAL/SHM files

Suggested validation:
git status --short --branch
py -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
py -m pytest -q tests/test_app_models.py tests/test_golden_replay_harness.py
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
py -m ruff check src tests tools
git diff --check
@'
src/mythic_edge_parser/app/analytics_ingest.py
tests/test_analytics_parser_normalized_replay_ingest.py
docs/contracts/analytics_parser_normalized_replay_ingest.md
docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
src/mythic_edge_parser/app/analytics_ingest.py
tests/test_analytics_parser_normalized_replay_ingest.py
docs/contracts/analytics_parser_normalized_replay_ingest.md
docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

Do not edit implementation in the review thread. Do not stage, commit, push, open a PR, merge, target main, create SQLite database files, or close issues unless explicitly asked.

Final output must include:
- role performed
- contract and handoff reviewed
- findings first
- contract matches
- contract mismatches
- missing safeguards or tests
- validation run and result
- generated SQLite artifact status
- protected-surface status
- secret/private-marker status
- remaining risks
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer / comparison thread"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "Codex A workflow handoff for [analytics] Define parser-normalized replay ingest into SQLite"
  contract_artifact: "docs/contracts/analytics_parser_normalized_replay_ingest.md"
  target_artifact: "docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "Medium"
  files_changed:
    - "src/mythic_edge_parser/app/analytics_ingest.py"
    - "tests/test_analytics_parser_normalized_replay_ingest.py"
    - "docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md"
  source_artifact_present:
    - "docs/contracts/analytics_parser_normalized_replay_ingest.md"
  code_changed: true
  tests_changed: true
  docs_changed: true
  schema_artifact_changed: false
  ingest_support_only: true
  sqlite_database_files_created_or_committed: false
  raw_player_log_or_saved_event_replay_execution_added: false
  live_ingest_or_cli_added: false
  validation:
    - "py -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py tests/test_analytics_migration_loader.py -> 40 passed"
    - "py -m pytest -q tests/test_app_models.py tests/test_golden_replay_harness.py -> 29 passed"
    - "py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 26 passed"
    - "py -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed; errors 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 1 on supplied contract protected-surface wording"
    - "path-scoped protected-surface check -> forbidden 0, warnings 0"
    - "generated SQLite artifact status check -> no changed or untracked SQLite DB/journal/WAL/SHM artifacts found"
  still_unverified:
    - "GitHub Actions"
    - "clean installed-wheel import"
    - "gameplay action SQLite ingest"
    - "opponent-card-observation SQLite ingest"
    - "field-evidence label override handling"
    - "live workbook state"
    - "deployed Apps Script state"
    - "production behavior"
  forbidden_scope_touched: false
  stop_conditions:
    - "Do not target main."
    - "Do not create or commit SQLite database files."
    - "Do not parse raw Player.log or run saved-event replay in this ingest slice."
    - "Do not implement live ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
