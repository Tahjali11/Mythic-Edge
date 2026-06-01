# Match Journal Local SQLite Schema Contract Test Report

## Findings

No blocking findings.

### Resolved By Codex D

#### MJSQL-001: Match Journal SQL migration package-data behavior was missing

- Severity: high
- Finding lifecycle: `fixed_state_followup`
- Finding status: verified fixed
- Blocking status: not_blocking
- Route: Codex F: Module Submitter

Original evidence:

- The contract authorizes a public migration loader with `load_match_journal_migration_sql(...)` and `apply_match_journal_migrations(...)`, and says the loader may match the analytics migration-loader pattern.
- The implementation reads SQL resources with `importlib.resources.files(MATCH_JOURNAL_MIGRATIONS_PACKAGE)` from `mythic_edge_parser.app.match_journal_migrations`.
- Before the Codex D fix, `pyproject.toml` declared package data only for `mythic_edge_parser.app.analytics_migrations = ["*.sql"]`; there was no package-data entry for `mythic_edge_parser.app.match_journal_migrations`.
- Existing analytics migration-loader tests explicitly protected the analytics package-data rule. The new Match Journal tests covered source-tree resource loading but did not cover package-data configuration.
- The implementation handoff also called this out as unverified because `pyproject.toml` was not in the original contract-owned file list.

Fix evidence:

- Codex B clarified that package-data behavior is required.
- Codex D added `mythic_edge_parser.app.match_journal_migrations = ["*.sql"]` under `[tool.setuptools.package-data]`.
- Codex D added focused coverage in `tests/test_match_journal_schema.py` proving the package-data declaration exists.

Why this is no longer blocking:

- The public `importlib.resources` migration loader now has matching package-data metadata for installed package contexts.
- The Match Journal package-data assertion mirrors the existing analytics migration-loader protection.
- Codex E verified a wheel built with the workspace Python includes both the Match Journal SQL migration and the analytics SQL migration.

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/196>

## Contract

`docs/contracts/match_journal_local_sqlite_schema.md`

## Implementation Under Test

Branch: `codex/match-journal-foundation`

Base branch: `main`

Changed files reviewed:

- `.gitignore`
- `pyproject.toml`
- `docs/contracts/match_journal_local_sqlite_schema.md`
- `docs/contract_test_reports/match_journal_local_sqlite_schema.md`
- `docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md`
- `src/mythic_edge_parser/app/match_journal_migration_loader.py`
- `src/mythic_edge_parser/app/match_journal_migrations/__init__.py`
- `src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql`
- `tests/test_match_journal_schema.py`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The implementation must add a local-only Match Journal SQLite schema and migration loader for human-entered notes, labels, review flags, experiment metadata, reference values, and display-only correction proposals. It must preserve parser truth boundaries, keep unattached notes representable without parser IDs, avoid generated/private artifacts, and avoid overlay, Google Sheets, workbook, webhook, Apps Script, runtime, parser, AI/model-provider, merge, or deploy behavior changes.

## Checks Run

```bash
python3 -m pytest -q tests/test_match_journal_schema.py
python3 -m pytest -q tests/test_analytics_migration_loader.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  .gitignore \
  pyproject.toml \
  docs/contracts/match_journal_local_sqlite_schema.md \
  docs/contract_test_reports/match_journal_local_sqlite_schema.md \
  docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md \
  src/mythic_edge_parser/app/match_journal_migration_loader.py \
  src/mythic_edge_parser/app/match_journal_migrations/__init__.py \
  src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql \
  tests/test_match_journal_schema.py \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  .gitignore \
  pyproject.toml \
  docs/contracts/match_journal_local_sqlite_schema.md \
  docs/contract_test_reports/match_journal_local_sqlite_schema.md \
  docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md \
  src/mythic_edge_parser/app/match_journal_migration_loader.py \
  src/mythic_edge_parser/app/match_journal_migrations/__init__.py \
  src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql \
  tests/test_match_journal_schema.py \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
find data -type f \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*-wal' -o -name '*-shm' -o -name '*-journal' \) -print
python3 -m pytest -q
```

Additional investigation:

```bash
python3 - <<'PY'
import tomllib
from pathlib import Path
pyproject = tomllib.loads(Path("pyproject.toml").read_text())
package_data = pyproject.get("tool", {}).get("setuptools", {}).get("package-data", {})
print(package_data)
print("match_journal package data:", package_data.get("mythic_edge_parser.app.match_journal_migrations"))
PY
python3 -m build --wheel --outdir <temp>
<workspace-python> -m pip wheel . --no-deps --no-build-isolation -w <temp>
```

## Results

- `tests/test_match_journal_schema.py`: 23 passed after Codex D added package-data coverage.
- `tests/test_analytics_migration_loader.py`: 15 passed.
- `tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py`: 14 passed.
- `python3 -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- Path-scoped secret/private marker scan: warning-only result, 9 scanned paths, 0 forbidden and 2 warnings from contract stop-condition prose mentioning failed-post/payload artifacts.
- Path-scoped protected-surface gate: passed, 9 changed paths, 0 forbidden, 0 warnings.
- SQLite artifact scan: passed with no output.
- Full pytest: 1373 passed.
- Package-data probe: `pyproject.toml` now lists both `mythic_edge_parser.app.analytics_migrations = ["*.sql"]` and `mythic_edge_parser.app.match_journal_migrations = ["*.sql"]`.
- System-Python wheel-build probes could not run because the local Python environment lacks `build`, `setuptools`, and `wheel`.
- Workspace-Python wheel check: passed; built 1 wheel and verified `mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql` and `mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql` are both included.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MJSQL-001 | high | `fixed_state_followup` | verified fixed | not_blocking | Match Journal loader reads SQL through `importlib.resources`, but `pyproject.toml` declared SQL package data only for analytics migrations. | `pyproject.toml` now declares `mythic_edge_parser.app.match_journal_migrations = ["*.sql"]`; `tests/test_match_journal_schema.py::test_pyproject_includes_match_journal_sql_package_data` covers it; workspace-Python wheel check verified the Match Journal SQL migration is included in the built wheel. | F |

## Confirmed Contract Matches

- The implementation stays scoped to `.gitignore`, a Match Journal migration loader, a source-controlled SQL migration, focused tests, and handoff documentation.
- `pyproject.toml` includes `mythic_edge_parser.app.match_journal_migrations = ["*.sql"]` under `[tool.setuptools.package-data]`.
- `data/match_journal/` is ignored.
- The default local database path is `data/match_journal/mythic_edge_journal.sqlite3`.
- The schema version is `match_journal_local_sqlite_schema.v1`.
- Journal-owned metadata tables exist: `journal_schema_migrations` and `journal_schema_versions`.
- Required table families exist: `journal_matches`, `journal_games`, `journal_notes`, `journal_labels`, `journal_review_flags`, and `journal_reference_values`.
- `journal_field_overrides` exists and constrains `effect_scope` to `journal_display_only`.
- `journal_sheet_sync_queue` remains deferred, which is acceptable for this first schema slice because the contract made it conditional.
- Tests prove migration discovery, SQL loading, idempotency, checksum mismatch rejection, open-transaction rejection, required tables/columns, bounded vocabulary enforcement, unattached note preservation, attached parser ID references without parser-table dependencies, display-only field override proposals, `.gitignore` coverage, and analytics-schema coexistence in the same in-memory SQLite connection.
- No parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics ingest, runtime status, status API, workbook schema, webhook payload shape, Apps Script behavior, overlay behavior, Google Sheets sync, OpenAI/model-provider behavior, merge policy, deploy policy, generated SQLite artifact, raw log, failed-post artifact, workbook export, or secret change was observed.

## Contract Mismatches

- None open for MJSQL-001. Package-data behavior is now specified in the clarified contract and implemented in `pyproject.toml`.

## Missing Tests

- None blocking.

## Drift Notes

- Worktree is on `codex/match-journal-foundation` and is based on `origin/main`.
- Changed/untracked files match the expected implementation slice plus this Codex E report.
- Secret/private marker warnings are warning-only prose matches in the contract, not live secrets or local artifacts.
- No repo drift, workbook drift, deployment drift, local-data drift, issue lifecycle drift, PR lifecycle drift, or tracker drift was found. The original package-data gap is verified fixed.

## Recommendation

Approve for Codex F submission.

## Next Workflow Action

Next role: Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/196"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/match_journal_local_sqlite_schema.md"
  target_artifact: "Codex F submission package for issue #196"
  verdict: "no_blocking_findings_ready_for_codex_f"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-foundation"
  validation:
    - "python3 -m pytest -q tests/test_match_journal_schema.py -> 23 passed"
    - "python3 -m pytest -q tests/test_analytics_migration_loader.py -> 15 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py -> 14 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private marker scan -> warning only: scanned paths 9, forbidden 0, warnings 2 in contract stop-condition prose"
    - "path-scoped protected-surface gate -> passed, changed paths 9"
    - "SQLite artifact scan -> passed with no output"
    - "python3 -m pytest -q -> 1373 passed"
    - "pyproject package-data probe -> analytics SQL package data present, Match Journal SQL package data present"
    - "system python wheel build probes -> not run; build/setuptools/wheel unavailable"
    - "workspace python pip wheel check -> built 1 wheel; analytics and Match Journal SQL migrations both included"
  fixed_findings:
    - "MJSQL-001 verified fixed: Match Journal SQL migration package-data behavior is specified, implemented, covered by focused test, and verified in a built wheel."
  stop_conditions:
    - "Do not target main directly."
    - "Do not implement overlay behavior, Google Sheets sync, workbook export, webhook delivery, Apps Script behavior, OpenAI/model-provider behavior, analytics ingest changes, runtime status changes, status API routes, parser behavior changes, parser state final reconciliation changes, parser event changes, match/game identity changes, or deduplication changes."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not let Match Journal notes or human annotations become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```
