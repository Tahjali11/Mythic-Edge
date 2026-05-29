# Analytics Gameplay Action Ingest Implementation Handoff

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifact Used

Codex A workflow handoff for:

```text
[analytics] Define gameplay-action ingest into SQLite
```

## Contract Used

`docs/contracts/analytics_gameplay_action_ingest.md`

## Branch And Git Status

Branch confirmed:

```text
codex/analytics-foundation
```

Initial status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/analytics_gameplay_action_ingest.md
```

The untracked gameplay-action ingest contract was treated as the supplied Codex
B artifact. No unrelated modified files were present at the start of this pass.

Status after implementation, before final safety-gate refresh:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
 M src/mythic_edge_parser/app/analytics_ingest.py
 M tests/test_analytics_parser_normalized_replay_ingest.py
?? docs/contracts/analytics_gameplay_action_ingest.md
?? tests/test_analytics_gameplay_action_ingest.py
```

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_migration_loader.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`

## Current Behavior Compared To Contract

Current repo behavior already matched these contract areas:

- The analytics schema already had `gameplay_actions` and
  `gameplay_action_cards` tables.
- Parser-normalized replay ingest already accepted `gameplay_action_entries` as
  optional input.
- Core match/game ingest already used caller-supplied SQLite connections,
  migration-loader bootstrap, deterministic ingest IDs, transaction rollback,
  row counts, and label-only `fact_provenance`.
- Parser action interpretation remained owned by `gameplay_actions.py`.
- Opponent-card observations were already a separate parser-normalized surface.

Contract gaps before this pass:

- `gameplay_action_entries` were still treated as deferred/skipped payloads.
- `_TOUCHED_TABLES` did not include `gameplay_actions` or
  `gameplay_action_cards`.
- No helper normalized gameplay action rows into SQLite-safe primitive values.
- No deterministic gameplay-action or child-card SQLite ID existed.
- No gameplay-action fact provenance rows existed.
- Existing optional-payload tests expected gameplay actions to remain skipped.
- No focused gameplay-action ingest tests covered idempotency, malformed
  action fields, parent-game integrity, no-card parent rows, or provenance
  boundaries.

## Implementation Option Chosen

Implemented the narrow contract-authorized slice inside the existing
`mythic_edge_parser.app.analytics_ingest` module. No schema migration, parser
change, CLI, live ingest, saved-event replay execution, or runtime integration
was added.

Chosen ID policy:

- `gameplay_action_id` is `gameplay_action:<sha256>` over canonical JSON of
  parser-normalized identity fields.
- ID inputs include match id, game number, game state id, turn number, action
  type, cast mode, actor relation, instance/card ids, parent id, zone movement,
  raw action labels, and annotation labels.
- `gameplay_action_card_id` is `gameplay_action_card:<sha256>` over the parent
  action ID and stable card ordinal.

Chosen storage policy:

- Accepted gameplay actions now write parent rows to `gameplay_actions`.
- Card identity evidence writes child rows to `gameplay_action_cards`.
- Actions without card identity still write the parent action row and do not
  fabricate a child card row.
- Opponent-card observations and field evidence remain deferred/skipped.
- Core provenance uses conservative labels:
  `value_source='derived'`, `confidence='unknown'`,
  `finality='reconciled'`, `drift_status='not_checked'`, and
  `availability_status='available'`.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md`

Source artifact present but not edited by this implementation thread:

- `docs/contracts/analytics_gameplay_action_ingest.md`

## Exact Code, Test, Doc, And Schema Sections Changed

### `src/mythic_edge_parser/app/analytics_ingest.py`

- Added `gameplay_actions` and `gameplay_action_cards` to `_TOUCHED_TABLES`.
- Changed `ingest_parser_normalized_replay(...)` to call gameplay-action ingest
  after core game rows are written.
- Changed `_ingest_game_log_rows(...)` to return deterministic game IDs written
  during the current ingest transaction.
- Added private gameplay-action helpers for:
  - action-entry validation and primitive normalization;
  - deterministic parent action IDs;
  - deterministic child card IDs;
  - associated-card list support for future parser-normalized inputs;
  - card identity/enrichment status classification;
  - actor-relation validation;
  - label-list storage;
  - visibility conversion to SQLite `1`, `0`, or `NULL`;
  - parent-game existence checks;
  - gameplay parent/card fact provenance.
- Expanded `_upsert_fact_provenance(...)` with optional ledger/event/payload
  path parameters while preserving existing callers.
- Removed gameplay actions from deferred optional warnings/skips.

### `tests/test_analytics_gameplay_action_ingest.py`

Added focused tests for:

- in-memory ingest writing `gameplay_actions` and `gameplay_action_cards`;
- `_TOUCHED_TABLES`, result row counts, and `ingest_runs.row_counts_json`
  including gameplay tables;
- deterministic replay idempotency for parent rows, child rows, and gameplay
  provenance rows;
- actions without card identity writing parent rows only;
- accepted actor relations: `local`, `opponent`, `unknown`, and blank;
- rejected actor relations failing without partial fact rows;
- malformed numeric action fields failing without partial fact rows;
- malformed `card_ordinal` failing without partial fact rows;
- missing parent game identity failing without orphan action rows;
- label-only gameplay fact provenance with no raw payload copies;
- opponent-card observations remaining deferred/skipped.

### `tests/test_analytics_parser_normalized_replay_ingest.py`

- Updated the optional-payload skip test so gameplay actions are no longer
  expected to be deferred.
- Left opponent-card observations and field evidence as deferred/skipped.

### Schema Artifacts

No schema migration or SQLite schema artifact changed.

### `docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md`

Added this handoff.

## Code Changed, Tests Changed, Docs-Only, Schema-Artifact-Only, Or Ingest-Support-Only

Code, tests, and docs changed.

This is local analytics ingest-support code only. It is not wired into live
runtime paths and does not change parser truth, parser runtime, workbook,
webhook, Apps Script, or production behavior.

## Contract Matches

- Gameplay action interpretation remains parser-owned.
- Analytics ingest only stores already-normalized parser action facts.
- `gameplay_action_entries` are no longer reported as skipped when accepted.
- `opponent_card_observations` remain deferred/skipped.
- `field_evidence_entries` remain deferred/skipped.
- `gameplay_actions` and `gameplay_action_cards` are included in row counts.
- Parent action rows map the contract-required columns.
- Child card rows map the contract-required identity/name columns.
- Actions with no card identity write no fabricated child row.
- Deterministic IDs are based on canonical JSON and do not use Python
  process-local `hash()`.
- Replaying the same normalized input is idempotent for action rows, child rows,
  and gameplay provenance rows.
- Malformed action fields fail clearly and roll back the ingest transaction.
- Unknown parent game identity fails without orphan action rows.
- Gameplay provenance uses labels and JSON-pointer-like paths, not raw payloads.
- No raw `Player.log`, saved-event JSONL, runtime status, failed-post payloads,
  workbook exports, local paths, secrets, webhook URLs, workbook IDs, or
  deployment IDs are stored.
- No parser behavior, gameplay-action parsing behavior, workbook schema,
  webhook payload shape, Apps Script behavior, live workbook state, or
  production behavior changed.

## Contract Mismatches

None known after this implementation.

## Missing Safeguards Or Tests

Remaining follow-up scope intentionally not implemented:

- No opponent-card-observation ingest.
- No field-evidence override handling.
- No migration for a dedicated `cast_mode` column.
- No live parser ingest.
- No saved-event replay runner.
- No CLI or default database opener.
- No Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration,
  or production wiring.

Remaining test gaps:

- Future multi-card associated-action inputs are minimally supported but not
  exhaustively tested beyond malformed `card_ordinal`.
- Existing-database parent-game acceptance was not separately tested; current
  tests cover same-replay parent integrity.
- Installed-wheel package import was not tested.

## Validation Run

Completed before final safety-gate refresh:

```text
py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py -> 55 passed
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 26 passed
py -m ruff check src/mythic_edge_parser/app/analytics_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py -> All checks passed!
py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py tests/test_analytics_migration_loader.py -> 70 passed
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 26 passed
py -m ruff check src tests tools -> All checks passed!
```

Final safety-gate results:

```text
git status --short --branch -> intended analytics ingest/test changes, untracked supplied contract, untracked handoff, and untracked focused gameplay-action ingest test
git diff --check -> passed
py tools/check_agent_docs.py -> passed; errors 0, warnings 0
py -m ruff check src tests tools -> All checks passed!
path-scoped secret/private-marker scan over touched files -> forbidden 0, warnings 3 on supplied contract protected-surface/raw-event wording
path-scoped protected-surface check over touched files -> forbidden 0, warnings 0
generated SQLite artifact status check -> no changed or untracked SQLite DB/journal/WAL/SHM artifacts found
```

## Protected-Surface Status

Local analytics ingest-support/test/docs changes only.

Path-scoped protected-surface gate over touched files passed with forbidden 0
and warnings 0. No parser/runtime/workbook/webhook/App Script/protected
surfaces were intentionally touched.

## Secret And Private-Marker Status

No secrets, raw logs, webhook URLs, workbook IDs, deployment IDs, generated
data, local runtime artifacts, workbook exports, or local source paths were
intentionally added.

An initial path-scoped scan flagged the raw MTGA event-type string from the
contract example in new code/tests. The implementation now leaves
`fact_provenance.source_event_type` null because parser-normalized gameplay
action entries do not carry a safe, durable event-type label in this slice.

Final path-scoped secret/private-marker scan passed with forbidden 0 and
warnings 3. The remaining warnings are in the supplied contract's
protected-surface/raw-event wording, not executable code, tests, generated data,
or this handoff.

## Generated SQLite Artifact Status

Tests use in-memory SQLite connections. Final generated SQLite artifact status
check found no changed or untracked SQLite DB, journal, WAL, SHM, or DB files.

## Raw Player.log And Saved-Event Replay Status

No raw `Player.log` parsing was added.

No saved-event replay execution was added. `source_kind='saved_event_replay'`
remains accepted only as a label for already-normalized replay bundles.

## Ingest, CLI, And Runtime Integration Status

Added local parser-normalized gameplay-action ingest support only.

No live ingest, CLI, default database opener, runtime integration, Google
Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or
production behavior was added.

## Still Unverified

- GitHub Actions.
- Installed-wheel package import.
- Future multi-card associated-action ingest coverage beyond malformed ordinal.
- Existing-database parent-game acceptance.
- Opponent-card-observation ingest.
- Field-evidence label override handling.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.

## Forbidden Scope Touched

No forbidden scope was intentionally touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for [analytics] gameplay-action ingest into SQLite.

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_gameplay_action_ingest.md

Implementation handoff:
docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md

Expected changed files:
- src/mythic_edge_parser/app/analytics_ingest.py
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_gameplay_action_ingest.py
- docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md

Source artifact present:
- docs/contracts/analytics_gameplay_action_ingest.md

Task:
Review the implementation against docs/contracts/analytics_gameplay_action_ingest.md. Lead with findings ordered by severity. Verify that gameplay-action ingest stores only already-normalized parser gameplay-action entries, preserves parser truth ownership, writes deterministic SQLite parent/card rows and label-only provenance, keeps opponent-card-observation ingest deferred, and does not change parser behavior or runtime/workbook/webhook/App Script/production behavior.

Check especially:
- gameplay_action_entries are no longer skipped when valid
- _TOUCHED_TABLES, result row_counts, and ingest_runs.row_counts_json include gameplay_actions and gameplay_action_cards
- deterministic gameplay_action_id and gameplay_action_card_id inputs are stable and specific enough
- repeated ingest is idempotent for action rows, card rows, and gameplay provenance rows
- action rows without card identity do not fabricate child cards
- actor_relation accepts only local, opponent, unknown, or blank
- malformed numeric action fields fail without partial fact rows
- missing parent game identity fails without orphan action rows
- fact_provenance rows use source labels and payload paths only, not raw payloads, local paths, URLs, workbook IDs, webhook URLs, or secrets
- opponent_card_observations and field_evidence_entries still remain deferred/skipped
- no schema migration, parser behavior change, saved-event replay execution, live ingest, CLI, runtime integration, generated SQLite DB, or production behavior was introduced

Suggested validation:
git status --short --branch
py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
py -m ruff check src tests tools
git diff --check
@'
src/mythic_edge_parser/app/analytics_ingest.py
tests/test_analytics_gameplay_action_ingest.py
tests/test_analytics_parser_normalized_replay_ingest.py
docs/contracts/analytics_gameplay_action_ingest.md
docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
src/mythic_edge_parser/app/analytics_ingest.py
tests/test_analytics_gameplay_action_ingest.py
tests/test_analytics_parser_normalized_replay_ingest.py
docs/contracts/analytics_gameplay_action_ingest.md
docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md
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
  source_artifact: "Codex A workflow handoff for [analytics] Define gameplay-action ingest into SQLite"
  contract_artifact: "docs/contracts/analytics_gameplay_action_ingest.md"
  target_artifact: "docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "Medium"
  files_changed:
    - "src/mythic_edge_parser/app/analytics_ingest.py"
    - "tests/test_analytics_parser_normalized_replay_ingest.py"
    - "tests/test_analytics_gameplay_action_ingest.py"
    - "docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md"
  source_artifact_present:
    - "docs/contracts/analytics_gameplay_action_ingest.md"
  code_changed: true
  tests_changed: true
  docs_changed: true
  schema_artifact_changed: false
  ingest_support_only: true
  sqlite_database_files_created_or_committed: false
  raw_player_log_or_saved_event_replay_execution_added: false
  live_ingest_or_cli_added: false
  validation:
    - "py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py -> 55 passed"
    - "py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py tests/test_analytics_migration_loader.py -> 70 passed"
    - "py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 26 passed"
    - "py -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed; errors 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 3 on supplied contract protected-surface/raw-event wording"
    - "path-scoped protected-surface check -> forbidden 0, warnings 0"
    - "generated SQLite artifact status check -> no changed or untracked SQLite DB/journal/WAL/SHM artifacts found"
  still_unverified:
    - "GitHub Actions"
    - "installed-wheel package import"
    - "future multi-card associated-action ingest coverage beyond malformed ordinal"
    - "existing-database parent-game acceptance"
    - "opponent-card-observation ingest"
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
