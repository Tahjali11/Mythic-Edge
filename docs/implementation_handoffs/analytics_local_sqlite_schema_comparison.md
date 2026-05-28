# Analytics Local SQLite Schema Implementation Handoff

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed:

```text
codex/analytics-foundation
```

Initial worktree status:

```text
## codex/analytics-foundation
?? docs/contracts/analytics_local_sqlite_schema.md
```

The untracked contract was treated as the supplied Codex B artifact. No
unrelated modified files were present at the start of this pass.

## Source Artifacts Used

- `docs/problem_representations/analytics_schema_contract.md`
- `docs/problem_representations/local_analytics_foundation.md`
- `docs/contracts/analytics_local_sqlite_schema.md`

## Contract Used

`docs/contracts/analytics_local_sqlite_schema.md`

## Artifact Produced

`docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md`

## Risk Tier

Medium-High.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/problem_representations/analytics_schema_contract.md`
- `docs/problem_representations/local_analytics_foundation.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `.gitignore`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `tests/test_app_models.py`
- `tests/test_analytics_sidecar.py`
- `tests/test_saved_event_replay.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_evidence_ledger.py`
- `tests/test_runtime_field_evidence.py`

## Current Behavior Compared To Contract

Current repo behavior already provides parser-normalized facts and adjacent
evidence surfaces:

- `models.py` emits normalized match and game row dictionaries.
- `state.py` owns live parser state, match/game identity, opening hand,
  mulligan, sideboarding, submitted-deck signals, and final reconciliation.
- `gameplay_actions.py` builds local gameplay action artifacts.
- `opponent_card_observations.py` builds visible/degraded opponent-card
  observation payloads.
- `evidence_ledger.py` and `runtime_field_evidence.py` define provenance,
  confidence, finality, drift, degradation, and runtime evidence vocabulary.
- `analytics_sidecar.py` currently manages optional runtime artifact and
  Google Sheets export work; it does not own a SQLite store.

Current repo gaps before this pass:

- `.gitignore` did not ignore `data/analytics/`.
- No analytics migration directory existed.
- No `0001_initial_analytics_schema.sql` migration existed.
- No focused SQLite schema tests existed.
- No `schema_migrations`, `fact_provenance`, required local analytics tables,
  required views, or schema-level idempotency evidence existed.

## Implementation Option Chosen

Implemented the smallest schema-first contract path:

- Add Git ignore coverage for generated local analytics database artifacts.
- Add one source-controlled plain SQL migration for schema v1.
- Add focused tests that apply the migration to an in-memory SQLite database.
- Keep migration application in test-only helpers, not production code.
- Do not implement ingest, live runtime wiring, replay ingest, a production
  migration runner, environment-variable contracts, Google Sheets sync, Line
  Tracer, AI coaching, or OpenAI runtime integration.

The migration files are repo-local source artifacts in this first pass. Package
data loading for installed-wheel execution is not implemented.

## Files Changed

- `.gitignore`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_schema.py`
- `docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md`

Source artifact present but not edited by this implementation thread:

- `docs/contracts/analytics_local_sqlite_schema.md`

## Exact Code, Test, Doc, And Schema Sections Changed

### `.gitignore`

Added:

```text
data/analytics/
```

This covers generated local SQLite database files and adjacent generated
SQLite artifacts under the contract default path.

### `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`

Added the first plain SQL migration.

Schema sections added:

- metadata tables: `schema_migrations`, `ingest_runs`,
  `parser_schema_versions`
- identity tables: `matches`, `games`, `game_players`, `sessions`,
  `deck_labels`
- result/context tables: `match_results`, `game_results`, `match_context`,
  `rank_snapshots`
- decision snapshot tables: `opening_hands`, `opening_hand_cards`,
  `mulligan_events`, `mulligan_bottomed_or_discarded_cards`,
  `sideboarding_states`, `submitted_deck_snapshots`,
  `submitted_deck_cards`
- gameplay/action/observation tables: `turns`, `gameplay_actions`,
  `gameplay_action_cards`, `card_movements`, `life_totals`,
  `public_zone_observations`, `opponent_card_observations`,
  `opponent_card_observation_cards`
- human annotation tables: `matchup_labels`, `archetype_labels`,
  `game_notes`
- detailed provenance table: `fact_provenance`
- indexes for common match/game/ingest/provenance joins
- initial views: `v_opening_hand_cards`, `v_opening_lines`,
  `v_mulligan_outcomes`, `v_game1_vs_postboard`,
  `v_play_draw_splits`, `v_sample_size_warnings`,
  `v_matchup_label_performance`

The migration includes core provenance columns on parser fact and annotation
tables, deterministic text primary keys where source identity is stable,
vocabulary constraints for source/confidence/finality/drift/availability
labels, one-card-per-row child tables for card-list surfaces, and a
non-materialized view note.

### `tests/test_analytics_schema.py`

Added focused schema tests that:

- apply the migration to an in-memory SQLite database
- record migration identity and SHA-256 checksum in `schema_migrations`
- assert the local generated database path is ignored by Git
- assert required tables, views, and key indexes exist
- assert core provenance columns exist on fact and annotation tables
- assert required label vocabularies are constrained
- assert `fact_provenance` supports multiple field-level rows per fact/field
- assert canonical card lists are modeled in child rows
- assert expected-unavailable and not-observed statuses are distinct
- assert repeated normalized fact inserts converge by deterministic IDs

### `docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md`

Added this handoff.

## Code Changed, Tests Changed, Docs-Only, Or Schema-Artifact-Only

Schema-artifact plus tests and docs:

- No runtime Python code changed.
- New test code was added.
- New SQL schema source artifact was added.
- `.gitignore` was updated.
- No production migration runner or ingest code was added.

## Contract Matches

- `data/analytics/` is ignored by Git.
- The default database path remains documented as
  `data/analytics/mythic_edge.sqlite3`; no database file was created.
- Plain SQL migration path exists at
  `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`.
- The logical schema version `analytics_local_sqlite_schema.v1` is recorded in
  schema metadata.
- Required table families exist.
- Required initial view families exist with `v_` names.
- Parser fact and annotation tables include core provenance columns.
- `fact_provenance` exists and supports multiple rows per fact/field.
- Canonical card-list surfaces use child rows.
- Expected-unavailable status is distinct from not-observed status.
- Deterministic-ID idempotency is covered by focused schema-level insert tests.
- SQLite remains a local analytics support layer and does not own parser truth.
- No raw Player.log payloads are stored in SQLite.
- No parser, state, workbook, webhook, Apps Script, runtime, AI, or production
  behavior changed.

## Contract Mismatches

None known after this implementation.

## Missing Safeguards Or Tests

Remaining follow-up scope intentionally not implemented:

- No production migration runner.
- No package-data loading for installed-wheel execution.
- No live parser ingest.
- No saved-event or replay ingest into SQLite.
- No environment-variable path override.
- No generated database artifact under `data/analytics/`.
- No broad query validation against real multi-match analytics data.

## Validation Run

Completed before this handoff was finalized:

```text
git status --short --branch -> branch confirmed; source contract untracked; implementation files modified/untracked
py -m pytest -q tests/test_analytics_schema.py -> 9 passed
PowerShell-expanded tests/test_analytics_schema*.py selector -> 9 passed
py -m pytest -q tests/test_analytics_schema.py tests/test_analytics_sidecar.py tests/test_saved_event_replay.py -> 40 passed
py -m pytest -q tests/test_app_models.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 42 passed
py -m pytest -q tests/test_evidence_ledger.py tests/test_runtime_field_evidence.py -> 128 passed
py -m ruff check src tests tools -> passed after import-order fix in tests/test_analytics_schema.py
git diff --check -> passed
py tools\check_agent_docs.py -> passed; checked 46 files, 0 errors, 0 warnings
path-scoped secret/private marker scan over touched files -> passed; forbidden 0, warnings 0
path-scoped protected-surface check over touched files with --base HEAD -> passed; forbidden 0, warnings 0
path-scoped protected-surface check over touched files with --base origin/main -> passed; forbidden 0, warnings 0
targeted trailing-whitespace scan -> no matches
```

Blocked validation:

```text
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation -> blocked; origin/codex/analytics-foundation does not exist locally or on origin
```

## Protected-Surface Status

Schema/test/docs-only. No forbidden parser/runtime/workbook/webhook/App
Script/protected surfaces were intentionally touched. The requested broad gate
using `origin/codex/analytics-foundation` was blocked because that remote ref
does not exist; path-scoped fallback gates passed with 0 forbidden changes and
0 warnings.

## Secret And Private-Marker Status

No secrets, raw logs, webhook URLs, workbook IDs, deployment IDs, generated
data, local runtime artifacts, workbook exports, or local source paths were
intentionally added. The path-scoped secret/private marker scan passed with 0
forbidden findings and 0 warnings.

## SQLite Database Artifact Status

No SQLite database files, journal files, WAL files, SHM files, or DB files were
created or found under `data/`.

Schema tests use an in-memory SQLite database.

## Raw Player.log Storage Status

No raw Player.log payloads, raw saved-event lines, raw local log paths, or raw
private log excerpts are stored in SQLite schema artifacts or tests.

## Still Unverified

- GitHub Actions were not run locally.
- Production migration runner behavior does not exist and was not tested.
- Installed package-data loading for SQL migrations was not implemented or
  tested.
- Live parser ingest was not implemented or tested.
- Saved-event replay ingest into SQLite was not implemented or tested.
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

Act as Codex E: Module Reviewer / contract-test thread for the local analytics SQLite schema implementation.

Branch:
codex/analytics-foundation

Source artifacts:
- docs/problem_representations/analytics_schema_contract.md
- docs/problem_representations/local_analytics_foundation.md

Contract:
docs/contracts/analytics_local_sqlite_schema.md

Implementation handoff:
docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md

Expected changed files:
- .gitignore
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- tests/test_analytics_schema.py
- docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md

Task:
Review the implementation against the analytics local SQLite schema contract. Lead with findings ordered by severity. Verify that the pass is schema/test/docs-only, that SQLite remains a local analytics support layer rather than parser truth, and that no parser/runtime/workbook/webhook/App Script behavior changed.

Check especially:
- data/analytics/ is ignored by Git.
- The migration is plain SQL under src/mythic_edge_parser/app/analytics_migrations/.
- No SQLite database files, WAL/SHM/journal files, raw Player.log payloads,
  raw saved-event lines, secrets, local paths, local runtime artifacts,
  workbook exports, generated data, or local-only artifacts were added.
- Required metadata, identity, result/context, decision snapshot, gameplay/action/observation, annotation, and provenance tables exist.
- Required initial views exist with v_ names.
- Parser fact and annotation tables include the core provenance columns.
- fact_provenance supports field-level provenance and multiple rows per fact/field.
- Label vocabularies for value_source, confidence, finality, drift_status, and availability_status are constrained or tested.
- Canonical card-list surfaces use child rows rather than delimited text or JSON as canonical truth.
- Expected-unavailable facts remain distinct from not-observed facts.
- Deterministic-ID idempotency is tested without implementing live or replay ingest.
- No production migration runner, ingest module, runtime wiring, environment-variable contract, Google Sheets sync, Line Tracer, AI coaching, or OpenAI runtime integration was added.

Suggested validation:
git status --short --branch
py -m pytest -q tests/test_analytics_schema.py
py -m pytest -q tests/test_analytics_sidecar.py tests/test_saved_event_replay.py
py -m pytest -q tests/test_app_models.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
py -m pytest -q tests/test_evidence_ledger.py tests/test_runtime_field_evidence.py
py -m ruff check src tests tools
git diff --check
@'
.gitignore
src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
tests/test_analytics_schema.py
docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md
'@ | py tools\check_secret_patterns.py --base HEAD --paths-from-stdin
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation

Do not edit implementation in the review thread. Do not stage, commit, push, open a PR, merge, target main, create SQLite database files, or close issues unless explicitly asked.

Final output must include:
- role performed
- contract and handoff reviewed
- findings first
- contract matches
- contract mismatches
- missing safeguards or tests
- validation run and result
- protected-surface status
- secret/private-marker status
- generated SQLite artifact status
- remaining risks
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/problem_representations/analytics_schema_contract.md"
  parent_artifact: "docs/problem_representations/local_analytics_foundation.md"
  contract_artifact: "docs/contracts/analytics_local_sqlite_schema.md"
  target_artifact: "docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md"
  branch: "codex/analytics-foundation"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  risk_tier: "Medium-High"
  files_changed:
    - ".gitignore"
    - "src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql"
    - "tests/test_analytics_schema.py"
    - "docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md"
  source_artifact_present:
    - "docs/contracts/analytics_local_sqlite_schema.md"
  code_changed: false
  tests_changed: true
  schema_artifact_changed: true
  docs_changed: true
  sqlite_database_files_created_or_committed: false
  raw_player_log_payloads_stored: false
  validation:
    - "py -m pytest -q tests/test_analytics_schema.py -> 9 passed"
    - "py -m pytest -q tests/test_analytics_schema.py tests/test_analytics_sidecar.py tests/test_saved_event_replay.py -> 40 passed"
    - "py -m pytest -q tests/test_app_models.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 42 passed"
    - "py -m pytest -q tests/test_evidence_ledger.py tests/test_runtime_field_evidence.py -> 128 passed"
    - "py -m ruff check src tests tools -> passed"
    - "PowerShell-expanded tests/test_analytics_schema*.py selector -> 9 passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, checked 46 files, errors 0, warnings 0"
    - "path-scoped secret/private marker scan over touched files -> passed, forbidden 0, warnings 0"
    - "path-scoped protected-surface check over touched files with --base HEAD -> passed, forbidden 0, warnings 0"
    - "path-scoped protected-surface check over touched files with --base origin/main -> passed, forbidden 0, warnings 0"
    - "py tools\\check_protected_surfaces.py --base origin/codex/analytics-foundation -> blocked, remote ref does not exist"
    - "targeted trailing-whitespace scan -> no matches"
  still_unverified:
    - "GitHub Actions"
    - "production migration runner"
    - "installed package-data loading for SQL migrations"
    - "live parser ingest"
    - "saved-event replay ingest into SQLite"
    - "live workbook state"
    - "deployed Apps Script state"
    - "production behavior"
  forbidden_scope_touched: false
  stop_conditions:
    - "Do not create or commit SQLite database files."
    - "Do not store raw Player.log payloads in SQLite."
    - "Do not implement ingest or a production migration runner without follow-up authorization."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
    - "Do not target main without explicit approval."
```
