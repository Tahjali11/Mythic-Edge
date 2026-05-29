# Analytics Opponent-Card-Observation Ingest Fixer Handoff

## Issue

Analytics foundation child work for opponent-card-observation ingest into local SQLite.

## Tracker

Analytics foundation tracker, branch `codex/analytics-foundation`.

## Contract

`docs/contracts/analytics_opponent_card_observation_ingest.md`

## Review Artifact

`docs/contract_test_reports/analytics_opponent_card_observation_ingest.md`

## Implementation Handoff Used

`docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md`

## Role Performed

Codex D: Module Fixer.

## Finding Fixed

P1: `degradation_flags` could persist local paths, URLs, raw-log/private markers, or secret-like text into durable observation rows and `fact_provenance` drift/degraded fields.

## What Changed

Added a focused safe-label guard at the opponent-card-observation ingest boundary. Parser-normalized degradation labels such as `missing_card_identity` remain accepted, but path-like, URL-like, raw-log, payload, and secret-marker values are rejected before SQLite rows or provenance records are written.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `docs/implementation_handoffs/analytics_opponent_card_observation_ingest_fixer.md`

Existing in-scope package files from the prior implementation/review loop remain present in the working tree:

- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`
- `docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md`
- `docs/contract_test_reports/analytics_opponent_card_observation_ingest.md`

## Code Changed

Runtime code changed: yes, limited to `src/mythic_edge_parser/app/analytics_ingest.py`.

Behavior surface:

- `_required_string_list(...)` now strips and validates observation `degradation_flags` values as durable-safe labels.
- `_validate_safe_degradation_flag(...)` rejects local paths, absolute paths, URLs, whitespace/punctuation-heavy strings, raw-log/private artifact markers, payload markers, and secret-like labels.
- No schema, migration, parser classification, gameplay-action classification, workbook, webhook, Apps Script, production, or AI/model-provider behavior changed.

## Tests Added Or Updated

- Added `test_unsafe_degradation_flags_fail_without_persisting_private_text` in `tests/test_analytics_opponent_card_observation_ingest.py`.
- The test exercises path-like, URL-like, raw payload marker, secret-like, and private artifact marker degradation flags.
- Each unsafe input must raise `AnalyticsReplayIngestError` and leave no partial fact rows.

## Interface Changes

None.

No function signatures, payload fields, workbook columns, environment variables, script entrypoints, docs schemas, issue lifecycle rules, or PR lifecycle rules changed.

## Contract Matches Confirmed

- Valid parser-normalized degradation labels remain accepted.
- Unsafe `degradation_flags` values are rejected before durable observation or provenance persistence.
- Missing/malformed unsafe values do not leave partial analytics fact rows.
- Fact provenance payload paths remain parser-owned safe labels.
- Existing opponent-card-observation ingest behavior stays intact.

## Validation Run

```powershell
py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py
# 29 passed

py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py
# 99 passed

py -m pytest -q tests\test_opponent_card_observations.py tests\test_gameplay_actions.py
# 26 passed

py -m ruff check src tests tools
# passed

git diff --check
# passed

py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# forbidden 0, warnings 1 on existing contract protected-artifact wording

py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# forbidden 0, warnings 0
```

Generated artifact check:

- No `.sqlite`, `.sqlite3`, `.db`, journal, WAL, or SHM files were found under `data`.

## Still Unverified

- Full repository test suite was not run in this fixer pass.
- Codex E should re-review the safe-label vocabulary to confirm it is neither too loose for durable provenance nor too strict for expected parser-normalized degradation labels.
- Branch has not been staged, committed, pushed, or submitted by this fixer thread.

## Reviewer Focus

Ask Codex E to verify:

- unsafe degradation values cannot reach `opponent_card_observations.degradation_flags`;
- unsafe degradation values cannot reach `fact_provenance.drift_flags` or `fact_provenance.degraded_reason`;
- valid parser-normalized labels still persist as expected;
- no forbidden parser/runtime/workbook/webhook/App Script surfaces were touched.

## Forbidden Scope Status

Forbidden scope was not touched.

No changes were made to parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, production behavior, AI truth, model-provider behavior, secrets, environment variables, raw logs, generated data, runtime status files, retry-queue payloads, workbook exports, generated SQLite files, or local runtime artifacts.

## Next Workflow Action

Next role: Codex E: Module Reviewer / confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for [analytics] Opponent-card-observation ingest into SQLite.

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_opponent_card_observation_ingest.md

Original implementation handoff:
docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md

Prior review artifact:
docs/contract_test_reports/analytics_opponent_card_observation_ingest.md

Fixer handoff:
docs/implementation_handoffs/analytics_opponent_card_observation_ingest_fixer.md

Review only the Codex D fix for the P1 finding:
- unsafe `degradation_flags` values could persist local paths, URLs, raw/private markers, or secret-like text into `opponent_card_observations.degradation_flags`, `fact_provenance.drift_flags`, and `fact_provenance.degraded_reason`.

Confirm:
- valid parser-normalized degradation labels are still accepted;
- unsafe path-like, URL-like, raw-log, payload, private artifact, and secret-marker labels fail before durable persistence;
- no partial analytics fact rows are written after rejection;
- no parser/runtime/workbook/webhook/App Script/protected production behavior changed.

Run focused validation:
py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py
py -m pytest -q tests\test_opponent_card_observations.py tests\test_gameplay_actions.py
py -m ruff check src tests tools
git diff --check

Also run path-scoped secret/private-marker and protected-surface checks over the changed files if available.

Produce or update the contract-test report and route to Codex F only if the P1 is resolved.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_opponent_card_observation_ingest.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_opponent_card_observation_ingest.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_opponent_card_observation_ingest_fixer.md"
  finding_fixed:
    - "P1: degradation_flags can persist local paths or URLs into durable observation rows and fact_provenance drift/degraded fields."
  validation:
    - "py -m pytest -q tests\\test_analytics_opponent_card_observation_ingest.py -> 29 passed"
    - "py -m pytest -q tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_schema.py tests\\test_analytics_migration_loader.py -> 99 passed"
    - "py -m pytest -q tests\\test_opponent_card_observations.py tests\\test_gameplay_actions.py -> 26 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 1 on existing contract protected-artifact wording"
    - "path-scoped protected-surface check -> forbidden 0, warnings 0"
    - "generated SQLite artifact check -> no data SQLite DB/journal/WAL/SHM artifacts found"
  forbidden_scope_touched: false
  route: "Codex E confirmation before Codex F"
```
