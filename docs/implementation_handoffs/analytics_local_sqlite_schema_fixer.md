# Analytics Local SQLite Schema Fixer Handoff

## Role Performed

Codex D: Module Fixer.

## Source Finding

Codex E requested an implementation fix:

- P1: parser fact tables accepted `human_annotation` / `human` labels despite
  the contract restricting those labels to annotation tables.

## Source Artifacts

- Contract: `docs/contracts/analytics_local_sqlite_schema.md`
- Implementation handoff:
  `docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md`
- Branch: `codex/analytics-foundation`

No stored analytics SQLite schema review artifact was found under
`docs/contract_test_reports/`; this fixer used the supplied workflow handoff as
the source finding.

## Fault Category

Implementation mismatch against the approved schema contract.

The SQL migration used one broad value-source/confidence vocabulary for parser
fact tables and annotation tables. The contract permits
`value_source='human_annotation'` and `confidence='human'` only for downstream
annotation tables.

## Fix Produced

Updated the migration so parser fact tables before the annotation-table section
exclude:

- `value_source='human_annotation'`
- `confidence='human'`

The annotation tables still require:

- `value_source='human_annotation'`
- `confidence='human'`

`fact_provenance` remains a separate detailed provenance table family and was
not changed by this P1 parser-fact-table fix.

## Files Changed

- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_schema.py`
- `docs/implementation_handoffs/analytics_local_sqlite_schema_fixer.md`

Existing C-thread files remain present in the working tree:

- `.gitignore`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md`

## Tests Added Or Updated

Updated `tests/test_analytics_schema.py` with focused regression coverage:

- parser fact table definitions must not include `human_annotation` or `human`
- parser fact rows reject `human_annotation` and `human`
- annotation tables still accept `human_annotation` and `human`

Focused test result before the migration fix:

```text
py -m pytest -q tests\test_analytics_schema.py
2 failed, 10 passed
```

Focused test result after the migration fix:

```text
py -m pytest -q tests\test_analytics_schema.py
12 passed
```

## Validation Evidence

```text
py -m pytest -q tests\test_analytics_schema.py
12 passed
```

```text
py -m pytest -q tests\test_analytics_sidecar.py tests\test_saved_event_replay.py
31 passed
```

```text
py -m pytest -q tests\test_app_models.py tests\test_gameplay_actions.py tests\test_opponent_card_observations.py
42 passed
```

```text
py -m pytest -q tests\test_evidence_ledger.py tests\test_runtime_field_evidence.py
128 passed
```

```text
py -m ruff check src tests tools
All checks passed!
```

```text
git diff --check
passed
```

```text
path-scoped secret/private-marker scan over .gitignore, migration, schema tests, and C handoff
result: passed; forbidden: 0; warnings: 0
```

```text
py tools\check_protected_surfaces.py --base origin/main
result: passed; forbidden: 0; warnings: 0
```

```text
path-scoped protected-surface check over .gitignore, migration, schema tests, and C handoff
result: passed; forbidden: 0; warnings: 0
```

`git fetch --prune origin main` succeeded before the origin/main protected
surface checks.

## Generated Artifact Status

No `data/analytics/` directory exists after validation. No SQLite database,
journal, WAL, SHM, raw log, failed-post, runtime status, generated data, or
workbook export artifacts were created or committed.

## Forbidden Scope Status

No parser/runtime/workbook/webhook/Apps Script behavior changed. No live ingest,
replay ingest, production migration runner, Google Sheets sync, Line Tracer, AI
coaching, OpenAI runtime integration, environment-variable contract, or
production behavior was added.

## Remaining Review Focus

- Confirm parser fact tables now exclude the human-only labels.
- Confirm annotation tables still require the human-only labels.
- Decide whether `fact_provenance` should remain separate for this P1 or needs
  a follow-up contract clarification.

## Still Unverified

- GitHub Actions.
- PR diff after staging/submission.
- Future production migration runner behavior.
- Future ingest/replay-to-SQLite behavior.
- Installed package-data loading for SQL migrations.
- Live workbook and deployed Apps Script state.

## Next Recommended Role

Codex E: Module Reviewer / confirmation thread.

```yaml
workflow_handoff:
  branch: "codex/analytics-foundation"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  source_artifact: "docs/contracts/analytics_local_sqlite_schema.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_local_sqlite_schema_fixer.md"
  finding_fixed:
    - "P1: parser fact tables no longer accept human_annotation/human labels."
  validation:
    - "py -m pytest -q tests\\test_analytics_schema.py -> 12 passed"
    - "py -m pytest -q tests\\test_analytics_sidecar.py tests\\test_saved_event_replay.py -> 31 passed"
    - "py -m pytest -q tests\\test_app_models.py tests\\test_gameplay_actions.py tests\\test_opponent_card_observations.py -> 42 passed"
    - "py -m pytest -q tests\\test_evidence_ledger.py tests\\test_runtime_field_evidence.py -> 128 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private-marker scan -> passed"
    - "py tools\\check_protected_surfaces.py --base origin/main -> passed"
    - "path-scoped protected-surface check -> passed"
  forbidden_scope_touched: false
  remaining_review_focus:
    - "Confirm the fact_provenance table-family treatment is acceptable or route to Codex B for clarification."
```
