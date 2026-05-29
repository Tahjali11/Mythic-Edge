# Analytics Field Evidence Ingest Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifact Used

Codex A handoff for `analytics_field_evidence_ingest`.

## Contract Used

`docs/contracts/analytics_field_evidence_ingest.md`

## Branch And Git Status

- Branch target: `codex/analytics-foundation`
- Current branch confirmed: `codex/analytics-foundation`
- Starting `HEAD`: `8cdfcaeae5e561d73056eeeda6ca0e3597564701`
- Initial worktree status:
  - `?? docs/contracts/analytics_field_evidence_ingest.md`

The untracked contract file was treated as the source artifact for this pass.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_field_evidence_ingest.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_migration_loader.py`
- `tests/test_evidence_ledger.py`
- `tests/test_runtime_field_evidence.py`

## Current Behavior Compared To Contract

### Contract Matches Before Implementation

- `ParserNormalizedReplayInput` already accepted `field_evidence_entries`.
- `normalize_parser_normalized_replay()` already normalized `field_evidence_entries` as a list of mappings.
- `deterministic_ingest_run_id()` already included field evidence entries in the replay hash.
- SQLite schema v1 already contained `fact_provenance`.
- `fact_provenance` already supported multiple rows for the same `fact_table`, `fact_id`, and `fact_field` when the IDs are distinct.
- `evidence_ledger.validate_field_evidence()` already enforced canonical field-evidence object/schema/ledger values, vocabulary labels, drift flags, invariant status, review-required policy, and privacy checks.

### Contract Mismatches Before Implementation

- `analytics_ingest.py` still treated `field_evidence_entries` as deferred optional input.
- Valid field-evidence entries were reported in `result.skipped`.
- Valid field-evidence entries emitted the deferred warning.
- No field-evidence ingest helper wrote replay field-evidence entries into `fact_provenance`.
- `_upsert_fact_provenance()` used the default ID shape `{fact_table}:{fact_id}:{fact_field}:provenance`, which collapses multiple field-evidence rows for the same fact field.
- `_upsert_fact_provenance()` did not preserve `invariant_status`.
- Existing analytics tests still asserted field evidence remained deferred.

### Missing Safeguards Or Missing Tests Before Implementation

- No focused tests proved valid field-evidence entries write `fact_provenance`.
- No test proved multiple field-evidence rows can attach to the same fact field without collapsing.
- No test proved idempotent replay for field-evidence provenance rows.
- No test proved malformed canonical field evidence rolls back without partial fact rows.
- No test proved malformed analytics attachment fields roll back without partial fact rows.
- No test proved missing target fact rows are rejected.
- No test proved private/local/raw path-like evidence labels are rejected.
- No test proved fact rows themselves are not mutated by field-evidence ingest.

## Implementation Option Chosen

Implemented the smallest local analytics ingest slice authorized by the contract:

- Field-evidence ingest remains private to `analytics_ingest.py`.
- `replay["field_evidence_entries"]` is treated as the input boundary.
- Canonical evidence fields are validated with `evidence_ledger.validate_field_evidence()`, with one compatibility filter for JSON-pointer-like `source_payload_paths` because this contract explicitly allows paths such as `/match_log_rows/0/match_id`.
- Analytics attachment fields are validated separately.
- Target fact rows must already exist in a known analytics fact table before provenance is written.
- Field evidence writes only `fact_provenance` rows.
- Deterministic `field_evidence:{sha256(...)}` provenance IDs allow multiple records for the same fact field.
- Existing automatic provenance rows are preserved.
- Valid field evidence is no longer reported as deferred or skipped.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_field_evidence_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md`

Related source artifact present but not edited by this pass:

- `docs/contracts/analytics_field_evidence_ingest.md`

## Exact Code, Test, Doc, And Schema Sections Changed

### `src/mythic_edge_parser/app/analytics_ingest.py`

- Imported `evidence_ledger`.
- Added `_FIELD_EVIDENCE_FACT_TABLE_PRIMARY_KEYS` allowlist for target fact-row existence checks.
- Added safe-label and private-marker validation constants for analytics field-evidence attachments.
- Called `_ingest_field_evidence_entries(...)` after parser-normalized fact ingest and before row counts are stored.
- Added private helpers:
  - `_ingest_field_evidence_entries(...)`
  - `_normalize_field_evidence_entry(...)`
  - `_field_evidence_provenance_id(...)`
  - `_require_target_fact_row(...)`
  - `_required_field_evidence_label(...)`
  - `_optional_field_evidence_label(...)`
  - `_required_safe_string_list(...)`
  - `_validate_safe_field_evidence_label(...)`
- Extended `_upsert_fact_provenance(...)` with optional `fact_provenance_id` and `invariant_status` parameters while preserving defaults for existing callers.
- Removed deferred warning and skipped-count behavior for `field_evidence_entries`.

### `tests/test_analytics_field_evidence_ingest.py`

Added focused coverage for:

- valid field evidence writing `fact_provenance`;
- preserved ledger entry, source labels, payload path labels, timestamp, value source, confidence, finality, drift flags, invariant status, degraded reason, and review-required values;
- row counts and `ingest_runs.row_counts_json`;
- valid field evidence not appearing in warnings or skipped counts;
- multiple rows for the same `fact_table`, `fact_id`, and `fact_field`;
- idempotent repeated replay;
- existing automatic provenance rows not being deleted;
- fact rows not being mutated by field-evidence ingest;
- malformed canonical evidence rollback;
- malformed analytics attachment rollback;
- missing target fact row rollback;
- private/local/raw path-like label rejection.

### Existing Analytics Tests

- Updated stale deferred-field-evidence assertions in:
  - `tests/test_analytics_gameplay_action_ingest.py`
  - `tests/test_analytics_opponent_card_observation_ingest.py`
  - `tests/test_analytics_parser_normalized_replay_ingest.py`

### Schema And Migration Files

- No schema or migration files were changed.

## Change Type

- Code changed: yes, local analytics ingest support only.
- Tests changed: yes, focused and stale deferred assertions.
- Docs changed: yes, implementation handoff only.
- Schema-artifact-only: no.
- Ingest-support-only: yes.

## Validation Run And Result

Validation completed:

- `git status --short --branch`
  - branch: `codex/analytics-foundation...origin/codex/analytics-foundation`
  - initial only-untracked source artifact: `docs/contracts/analytics_field_evidence_ingest.md`
- `py -m pytest -q tests\test_analytics_field_evidence_ingest.py`
  - passed: `24 passed`
- `py -m pytest -q tests\test_analytics_field_evidence_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py`
  - passed: `108 passed`
- `py -m pytest -q tests\test_evidence_ledger.py tests\test_runtime_field_evidence.py`
  - passed: `128 passed`
- `py -m pytest -q tests\test_analytics_field_evidence_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py`
  - passed: `123 passed`
- `py -m ruff check src tests`
  - passed
- `py -m ruff check src tests tools`
  - passed
- generated SQLite artifact status check
  - passed: no `.sqlite`, `.sqlite3`, `.db`, `.db-journal`, `.db-wal`, or `.db-shm` files listed by `git status --short --untracked-files=all`
- `git diff --check`
  - passed
- `py tools\check_agent_docs.py`
  - passed: `errors: 0`, `warnings: 0`
- path-scoped secret/private-marker scan over touched/source paths
  - passed: `forbidden: 0`, `warnings: 0`
- path-scoped protected-surface scan over touched/source paths
  - passed: `forbidden: 0`, `warnings: 0`

## Protected-Surface Status

No protected parser/runtime/workbook/webhook/App Script behavior was intentionally changed.

Touched implementation scope was limited to:

- local analytics replay ingest storage behavior in `analytics_ingest.py`;
- focused tests for that local analytics ingest behavior;
- this implementation handoff.

No changes were made to:

- parser behavior;
- parser state final reconciliation;
- parser event classes or payload shapes;
- match/game identity or deduplication;
- SQLite schema or migrations;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- Line Tracer;
- AI/OpenAI runtime behavior;
- production behavior.

## Secret And Private-Marker Status

No secrets, credentials, webhook URLs, workbook IDs, raw Player.log payloads, local absolute artifact paths, runtime status payloads, retry-queue payloads, generated data, or workbook exports were added intentionally.

Field-evidence provenance source paths are stored as safe labels or JSON-pointer-like labels only, such as:

```text
/match_log_rows/0/match_id
payload.match_id
```

## Generated SQLite Artifact Status

No SQLite database files were intentionally created or committed. Tests use in-memory SQLite connections.

## Raw Player.log Status

No raw `Player.log` data was stored.

No raw `Player.log` parsing was added.

## Runtime Integration Status

No live ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior was added.

## What Remains Unverified

- Full repository test suite beyond focused analytics/evidence checks.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.
- Durable producer of replay-ready field-evidence entries.
- Broader output-family coverage beyond representative existing analytics fact targets.

## Forbidden Scope Status

No forbidden scope was intentionally touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for analytics_field_evidence_ingest.

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_field_evidence_ingest.md

Implementation handoff:
docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md

Risk tier:
Medium

Goal:
Review the Codex C implementation against docs/contracts/analytics_field_evidence_ingest.md. Lead with findings ordered by severity. Verify that field-evidence ingest stores parser-normalized field evidence as local SQLite fact_provenance rows without changing parser truth ownership, SQLite schema, workbook/webhook/App Script behavior, raw log handling, or production behavior.

Before reviewing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and identify unrelated or untracked files.
- Read the contract and implementation handoff before inspecting code.
- Inspect:
  - src/mythic_edge_parser/app/analytics_ingest.py
  - tests/test_analytics_field_evidence_ingest.py
  - tests/test_analytics_gameplay_action_ingest.py
  - tests/test_analytics_opponent_card_observation_ingest.py
  - tests/test_analytics_parser_normalized_replay_ingest.py
  - src/mythic_edge_parser/app/evidence_ledger.py
  - src/mythic_edge_parser/app/runtime_field_evidence.py
  - src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql

Review for:
- contract matches;
- contract mismatches;
- missing safeguards;
- missing tests;
- unintended parser/runtime/workbook/webhook/App Script behavior changes;
- unintended SQLite schema or migration drift;
- unsafe provenance paths, raw payloads, local paths, secrets, or private markers;
- generated SQLite artifacts;
- deterministic field-evidence provenance IDs that allow multiple rows for one fact field;
- canonical evidence-ledger validation and review-required policy;
- target fact-row existence checks;
- rollback behavior for malformed/private/missing-target entries;
- whether the JSON-pointer compatibility filter around evidence_ledger.validate_field_evidence is acceptable under the contract.

Do not:
- implement fixes unless explicitly asked after the review;
- target main;
- change parser/runtime/workbook/webhook/App Script behavior;
- alter SQLite schema or create database files;
- store raw Player.log data;
- parse raw Player.log;
- run saved-event replay;
- implement live ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior;
- touch secrets, credentials, generated data, runtime artifacts, retry-queue payloads, workbook exports, or local-only artifacts;
- stage, commit, push, open a PR, merge, or close issues unless explicitly asked.

Validation:
git status --short --branch
py -m pytest -q tests\test_analytics_field_evidence_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py
py -m pytest -q tests\test_evidence_ledger.py tests\test_runtime_field_evidence.py
py -m ruff check src tests tools
git diff --check

Also run path-scoped secret/private-marker and protected-surface checks over the contract, implementation handoff, analytics_ingest.py, and focused tests if available.

Produce:
docs/contract_test_reports/analytics_field_evidence_ingest.md

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
  completed_thread: "C"
  next_thread: "E"
  branch: "codex/analytics-foundation"
  source_artifact: "Codex A handoff for analytics_field_evidence_ingest"
  contract_artifact: "docs/contracts/analytics_field_evidence_ingest.md"
  target_artifact: "docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md"
  risk_tier: "Medium"
  code_changed: true
  tests_changed: true
  docs_changed: true
  schema_changed: false
  validation:
    - "py -m pytest -q tests\\test_analytics_field_evidence_ingest.py -> passed, 24 passed"
    - "py -m pytest -q tests\\test_analytics_field_evidence_ingest.py tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_schema.py -> passed, 108 passed"
    - "py -m pytest -q tests\\test_evidence_ledger.py tests\\test_runtime_field_evidence.py -> passed, 128 passed"
    - "py -m pytest -q tests\\test_analytics_field_evidence_ingest.py tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_schema.py tests\\test_analytics_migration_loader.py -> passed, 123 passed"
    - "py -m ruff check src tests -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "generated SQLite artifact status check -> no tracked or untracked SQLite DB artifacts listed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, errors 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
  remaining_unverified:
    - "Full repository test suite"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
    - "Durable producer of replay-ready field-evidence entries"
    - "Broader output-family coverage beyond representative existing analytics fact targets"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
    - "Do not alter SQLite schema or create database files in this slice."
    - "Do not store raw Player.log data or touch secrets/generated/runtime artifacts."
```
