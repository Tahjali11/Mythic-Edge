# Analytics Opponent Card Observation Ingest Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifact Used

- Codex A workflow handoff for `[analytics] Opponent-card-observation ingest into SQLite`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`

## Contract Used

`docs/contracts/analytics_opponent_card_observation_ingest.md`

## Branch And Git Status

- Branch target: `codex/analytics-foundation`
- Verified context commit: `39948ed0f8b5f876371548357672dabdcb07debc`
- Branch check: current branch was `codex/analytics-foundation`
- Ancestor check: `39948ed0f8b5f876371548357672dabdcb07debc` is an ancestor of `HEAD`
- Initial worktree status before implementation:
  - `?? docs/contracts/analytics_opponent_card_observation_ingest.md`
- The contract file was present as an untracked source artifact from the prior workflow thread and was inspected, not edited by this pass.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/parser_opponent_card_observations.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_migration_loader.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_gameplay_actions.py`

## Current Behavior Compared To Contract

### Contract Matches Before Implementation

- SQLite schema v1 already defined `opponent_card_observations` and `opponent_card_observation_cards`.
- `ParserNormalizedReplayInput` already accepted `replay["opponent_card_observations"]`.
- Gameplay-action ingest was already implemented, including deterministic IDs, child-card rows, idempotent upserts, and provenance using `tier5.gameplay_action.gameplay_action`.
- `opponent_card_observations.py` already owned parser-normalized observation facts and emitted `object = mythic_edge_opponent_card_observation` plus `schema_version = parser_opponent_card_observations.v1`.
- Existing parser helper tests covered clean visible observations, degraded observations, suppression boundaries, and collection payload behavior.

### Contract Mismatches Before Implementation

- `analytics_ingest.py` still reported `opponent_card_observations` as deferred optional input.
- Valid opponent observations were added to `result.skipped["opponent_card_observations"]`.
- The ingest result emitted the deferred warning `opponent_card_observations are accepted but deferred by the first ingest pass`.
- `_TOUCHED_TABLES` did not include the opponent observation parent and child tables.
- No opponent-observation ingest helper, deterministic observation ID helper, gameplay-action link resolver, child-card row builder, or observation provenance writer existed.
- Existing analytics tests asserted the old deferred behavior.

### Missing Safeguards Or Missing Tests Before Implementation

- No focused tests verified insertion into `opponent_card_observations`.
- No focused tests verified insertion into `opponent_card_observation_cards`.
- No test verified row counts and `ingest_runs.row_counts_json` included the opponent observation tables.
- No test verified idempotent replay for opponent observation parent, child, and provenance rows.
- No test verified deterministic link resolution to an already-ingested gameplay action.
- No test verified null-link behavior when no gameplay action exists.
- No test verified explicit unknown `gameplay_action_id` warning behavior.
- No test verified degraded missing-card observations avoid fabricated child-card identity.
- No test verified malformed opponent observations fail and roll back without partial fact rows.
- No test verified Tier 5 opponent-observation provenance uses safe payload-path labels instead of raw payloads or local paths.

## Implementation Option Chosen

Implemented the smallest local analytics ingest slice authorized by the contract:

- Keep `opponent_card_observations.py` as the parser-normalized truth owner.
- Treat `replay["opponent_card_observations"]` as the input boundary.
- Store parser-produced observation facts in existing SQLite schema v1 tables.
- Link to a stored gameplay action only when an explicit or deterministic candidate row exists.
- Store `NULL` for missing gameplay-action links without synthesizing actions.
- Preserve parser-supplied value source, confidence, evidence status, visibility, degradation flags, review-required, finality, and drift labels.
- Keep `field_evidence_entries` deferred.
- Do not add migrations, schema columns, CLI, database files, raw-log readers, saved-event replay execution, live ingest, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime behavior, or production behavior.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md`

Related source artifact present but not edited by Codex C:

- `docs/contracts/analytics_opponent_card_observation_ingest.md`

## Exact Code, Test, Doc, And Schema Sections Changed

### `src/mythic_edge_parser/app/analytics_ingest.py`

- Added parser observation constants imported from `opponent_card_observations.py`.
- Added `opponent_card_observations` and `opponent_card_observation_cards` to `_TOUCHED_TABLES`.
- Added Tier 5 opponent-observation ledger constant and enum allowlists for value source, confidence, evidence status, visibility, finality, and drift status.
- Extended `ingest_parser_normalized_replay(...)` to call `_ingest_opponent_card_observations(...)` after gameplay-action ingest.
- Added private opponent-observation helpers:
  - `_ingest_opponent_card_observations(...)`
  - `_normalize_opponent_card_observation(...)`
  - `_opponent_card_observation_id(...)`
  - `_resolve_opponent_observation_gameplay_action_id(...)`
  - `_opponent_observation_card_row(...)`
  - `_has_opponent_observation_card_identity(...)`
  - `_has_opponent_observation_numeric_identity(...)`
  - `_observation_core_columns(...)`
  - `_upsert_opponent_observation_provenance(...)`
  - `_gameplay_action_exists(...)`
  - `_required_enum(...)`
  - `_optional_enum(...)`
  - `_required_bool_int(...)`
  - `_required_string_list(...)`
  - `_default_observation_drift_status(...)`
  - `_observation_degraded_reason(...)`
- Extended `_upsert_fact_provenance(...)` with optional row-specific `value_source`, `confidence`, `drift_flags`, `degraded_reason`, and `review_required` parameters while preserving existing defaults for earlier callers.
- Removed opponent observation deferred warning and skipped-count behavior from `_deferred_optional_warnings(...)` and `_deferred_optional_skips(...)`.

### `tests/test_analytics_opponent_card_observation_ingest.py`

Added focused coverage for:

- parent and child table writes;
- row counts and `ingest_runs.row_counts_json`;
- no deferred warning or skipped count for valid observations;
- deterministic gameplay-action link storage;
- null-link storage when no matching gameplay action exists;
- explicit unknown gameplay-action ID warning plus null link;
- idempotent repeated replay for parent, child, and provenance rows;
- preservation/defaulting of parser labels;
- degraded missing-card identity without fabricated child rows;
- malformed enum, marker, boolean, list, numeric, and actor-relation inputs;
- unknown parent game rejection and transaction rollback;
- safe fact-provenance payload paths and Tier 5 ledger entry.

### `tests/test_analytics_gameplay_action_ingest.py`

- Replaced the old opponent-observation deferred assertion with a `field_evidence_entries` deferred assertion.
- Preserved the check that no opponent observation rows are written when no observation payload is provided.

### `tests/test_analytics_parser_normalized_replay_ingest.py`

- Updated deferred optional payload coverage so only `field_evidence_entries` remains skipped/deferred.

### Schema And Migration Files

- No schema or migration files were changed.

## Change Type

- Code changed: yes, local analytics ingest support only.
- Tests changed: yes, focused analytics ingest tests.
- Docs changed: yes, implementation handoff only.
- Schema-artifact-only: no.
- Ingest-support-only: yes.

## Validation Run And Result

Validation completed:

- `git status --short --branch`
  - branch: `codex/analytics-foundation...origin/codex/analytics-foundation`
  - modified: `src/mythic_edge_parser/app/analytics_ingest.py`
  - modified: `tests/test_analytics_gameplay_action_ingest.py`
  - modified: `tests/test_analytics_parser_normalized_replay_ingest.py`
  - untracked source artifact: `docs/contracts/analytics_opponent_card_observation_ingest.md`
  - untracked handoff: `docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md`
  - untracked test: `tests/test_analytics_opponent_card_observation_ingest.py`
- `py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py`
  - passed: `98 passed`
- `py -m pytest -q tests\test_opponent_card_observations.py tests\test_gameplay_actions.py`
  - passed: `26 passed`
- `py -m ruff check src tests tools`
  - passed
- `git diff --check`
  - passed
- `py tools\check_agent_docs.py`
  - passed: `errors: 0`, `warnings: 0`
- path-scoped secret/private-marker scan over touched/source paths
  - result: warning
  - forbidden: `0`
  - warnings: `1`
  - warning source: `docs/contracts/analytics_opponent_card_observation_ingest.md`, the unedited source contract, from forbidden-artifact wording
- path-scoped protected-surface check over touched/source paths
  - passed: `forbidden: 0`, `warnings: 0`
- generated SQLite artifact status check
  - passed: no `.sqlite`, `.sqlite3`, `.db`, `.db-journal`, `.db-wal`, or `.db-shm` files listed by `git status --short --untracked-files=all`

## Protected-Surface Status

No protected parser/runtime/workbook/webhook/App Script behavior was intentionally changed.

Touched implementation scope was limited to:

- local analytics replay ingest storage behavior in `analytics_ingest.py`;
- focused tests for that local analytics ingest behavior;
- this implementation handoff.

No changes were made to:

- parser behavior;
- opponent-card-observation parser classification behavior;
- gameplay-action extraction/classification behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- output transport;
- production behavior.

## Secret And Private-Marker Status

No secrets, credentials, webhook URLs, workbook IDs, raw Player.log payloads, local absolute artifact paths, runtime status payloads, retry-queue payloads, generated data, or workbook exports were added intentionally.

Fact-provenance source payload paths for this slice are label-only paths such as:

```text
/opponent_card_observations/0/visibility
```

## Generated SQLite Artifact Status

No SQLite database files were intentionally created or committed. Tests use in-memory SQLite connections.

## Raw Player.log And Saved-Event Replay Status

No raw `Player.log` parsing was added.

No saved-event replay execution was added.

This slice consumes parser-normalized replay dictionaries only.

## Runtime Integration Status

No live ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior was added.

## What Remains Unverified

- Full repository test suite beyond the focused analytics/parser helper tests.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.
- Future field-evidence ingest.
- Future multi-card opponent observation input.
- Future dedicated storage for `layout`, `card_faces`, `raw_action_types`, `annotation_types`, and `annotation_categories`.

## Forbidden Scope Status

No forbidden scope was intentionally touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for [analytics] Opponent-card-observation ingest into SQLite.

Branch:
codex/analytics-foundation

Source implementation handoff:
docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md

Contract:
docs/contracts/analytics_opponent_card_observation_ingest.md

Risk tier:
Medium

Goal:
Review the Codex C implementation against docs/contracts/analytics_opponent_card_observation_ingest.md. Lead with findings ordered by severity. Verify that the implementation stores parser-normalized opponent-card observations in SQLite without changing parser truth ownership or protected surfaces.

Before reviewing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and identify unrelated or untracked files.
- Read the contract and implementation handoff before inspecting code.
- Inspect:
  - src/mythic_edge_parser/app/analytics_ingest.py
  - tests/test_analytics_opponent_card_observation_ingest.py
  - tests/test_analytics_gameplay_action_ingest.py
  - tests/test_analytics_parser_normalized_replay_ingest.py
  - src/mythic_edge_parser/app/opponent_card_observations.py
  - src/mythic_edge_parser/app/gameplay_actions.py
  - src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql

Review for:
- contract matches;
- contract mismatches;
- missing safeguards;
- missing tests;
- unintended parser/gameplay/opponent-observation behavior changes;
- schema or migration drift;
- unsafe provenance paths, raw payloads, local paths, secrets, or private markers;
- generated SQLite artifacts;
- correct row-count, skipped, warning, idempotency, null-link, degraded-observation, malformed-input, and provenance behavior.

Do not:
- implement fixes unless explicitly asked after the review;
- change parser behavior;
- change opponent-card-observation classification behavior;
- change gameplay-action extraction/classification behavior;
- change parser state final reconciliation;
- change parser event classes;
- change match/game identity or deduplication;
- change workbook schema, webhook payload shape, Apps Script behavior, output transport, production behavior, AI truth, model-provider behavior, secrets, environment variables, raw logs, generated data, runtime status files, retry-queue payloads, workbook exports, generated SQLite files, or local runtime artifacts;
- create migration files or alter schema;
- rebuild observations from raw gameplay actions;
- implement live ingest, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime behavior, or production behavior;
- target main, stage, commit, push, open a PR, merge, or close issues unless explicitly asked.

Validation:
git status --short --branch
py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py
py -m pytest -q tests\test_opponent_card_observations.py tests\test_gameplay_actions.py
py -m ruff check src tests tools
git diff --check

Also run path-scoped secret/private-marker and protected-surface checks over the contract, implementation handoff, analytics_ingest.py, and focused tests if available.

Produce:
docs/contract_test_reports/analytics_opponent_card_observation_ingest.md

Final review report must include:
- role performed
- contract and handoff reviewed
- files reviewed
- findings first, ordered by severity
- contract matches
- contract mismatches
- missing tests or safeguards
- validation run and result
- protected-surface status
- secret/private-marker status
- generated SQLite artifact status
- whether forbidden scope was touched
- whether this should route to Codex D, Codex B, or Codex F
- pasteable next-thread prompt
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer / comparison thread"
  source_artifact: "Codex A workflow handoff for [analytics] Opponent-card-observation ingest into SQLite"
  contract_artifact: "docs/contracts/analytics_opponent_card_observation_ingest.md"
  target_artifact: "docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md"
  branch: "codex/analytics-foundation"
  base_branch: "codex/analytics-foundation"
  verified_context_commit: "39948ed0f8b5f876371548357672dabdcb07debc"
  risk_tier: "Medium"
  code_changed: true
  tests_changed: true
  docs_changed: true
  schema_changed: false
  next_thread: "E"
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
  validation:
    - "py -m pytest -q tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_schema.py tests\\test_analytics_migration_loader.py -> passed, 98 passed"
    - "py -m pytest -q tests\\test_opponent_card_observations.py tests\\test_gameplay_actions.py -> passed, 26 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, errors 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 1 from unedited source contract forbidden-artifact wording"
    - "path-scoped protected-surface check -> forbidden 0, warnings 0"
    - "generated SQLite artifact status check -> no tracked or untracked SQLite DB artifacts listed"
  remaining_unverified:
    - "Full repository test suite"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
    - "Future field-evidence ingest"
    - "Future multi-card opponent observation input"
  stop_conditions:
    - "Do not target main."
    - "Do not create or commit SQLite database files."
    - "Do not parse raw Player.log."
    - "Do not run saved-event replay."
    - "Do not implement live ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
