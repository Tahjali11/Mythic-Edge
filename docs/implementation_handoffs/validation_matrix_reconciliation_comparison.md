# Validation Matrix Reconciliation Implementation Handoff

## Role Performed

Codex C: Module Implementer.

## Source Issue And Contract

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/152>
- Contract: `docs/contracts/validation_matrix_reconciliation.md`
- Branch: `codex/analytics-foundation`
- Risk tier: Medium-High

## Comparison Summary

The current repo already had the correct authority split:

- `tools/select_validation.py` is the executable changed-path selector.
- `tools/run_hardening_orchestrator.py` is the local bundle planner/runner.
- `.github/workflows/repo-checks.yml` does not run selector, orchestrator,
  secret scan, frontend checks, local-environment checks, or Pyright as CI
  gates.

The stale PR #65 `docs/validation_matrix.json` was useful as source material
only. It included baseline safety checks and surface-oriented command mapping,
but it predated the current local app, frontend, analytics SQLite, local
artifact manifest, clean-install transition, internal project map, and current
selector/orchestrator tools.

## Confirmed Matches

- Selector still requires explicit `--base`.
- Selector still supports `--paths-from-stdin`.
- Selector still recommends protected-surface gate, secret/private-marker scan,
  and `git diff --check` for non-empty path sets.
- Selector still reports recommendations and does not run validation commands.
- Orchestrator remains plan/run bundle authority and was not changed.
- No CI workflow changes were made.
- No `docs/validation_matrix.json` runtime config was added.
- No parser, analytics, local app, workbook, webhook, Apps Script, Sheets,
  OpenAI, AI, coaching, or production behavior was changed.

## Contract Mismatches Fixed

- Added selector categories and focused mappings for:
  - `frontend/**`;
  - `src/mythic_edge_parser/local_app/**`;
  - `tools/dev_app/**`;
  - analytics migration/schema/ingest/view/import surfaces;
  - `docs/local_artifacts_manifest.json` and local-environment checker
    surfaces;
  - validation reference docs and internal project boundary docs.
- Changed selector Pyright recommendation priority from `recommended` to
  `advisory`.
- Added focused selector tests pinning the modern surface mappings and Pyright
  advisory behavior.
- Added `docs/validation_matrix.md` as a human-facing,
  non-authoritative selector-backed reference.

## Files Changed

- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `docs/validation_matrix.md`
- `docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md`

Existing untracked source artifact from Codex B:

- `docs/contracts/validation_matrix_reconciliation.md`

## Tests Added Or Updated

Updated `tests/test_select_validation.py` with focused coverage for:

- Pyright advisory/non-required priority for parser and dependency/source
  changes;
- frontend typecheck/test/build recommendations;
- local app backend/history focused test routing;
- developer launcher focused test routing;
- analytics migration/schema/view routing;
- analytics ingest focused routing;
- local artifact manifest/checker/profile-report routing;
- validation matrix and internal project map governance/reference routing.

## Validation Run

- `python3 -m pytest -q tests/test_select_validation.py`
  - passed: 34 passed
- `python3 -m pytest -q tests/test_hardening_orchestrator.py`
  - passed: 19 passed
- `python3 -m pytest -q tests/test_check_local_environment.py tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py`
  - passed: 97 passed
- `python3 -m ruff check tools tests src`
  - passed
- `python3 tools/check_agent_docs.py`
  - passed: errors 0, warnings 0
- `git diff --check`
  - passed for tracked changes
- `git diff --no-index --check /dev/null docs/contracts/validation_matrix_reconciliation.md`
  - no whitespace findings; wrapper normalized expected no-index diff exit
- `git diff --no-index --check /dev/null docs/validation_matrix.md`
  - no whitespace findings; wrapper normalized expected no-index diff exit
- `printf '%s\n' docs/contracts/validation_matrix_reconciliation.md docs/validation_matrix.md tools/select_validation.py tests/test_select_validation.py | python3 tools/select_validation.py --base origin/codex/analytics-foundation --paths-from-stdin`
  - passed: selection_status ok, required 6, recommended 0, advisory 1
- `printf '%s\n' docs/contracts/validation_matrix_reconciliation.md docs/validation_matrix.md tools/select_validation.py tests/test_select_validation.py | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin`
  - passed: forbidden 0, warnings 0
- `printf '%s\n' docs/contracts/validation_matrix_reconciliation.md docs/validation_matrix.md tools/select_validation.py tests/test_select_validation.py | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin`
  - passed: forbidden 0, warnings 0
- `find . -path './.git' -prune -o \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name '*.sqlite-journal' \) -print`
  - passed: no generated SQLite artifacts found
- `python3 tools/run_pyright_advisory_report.py`
  - advisory non-blocking: status `advisory_findings`, pyright exit_code 1,
    errors 148, type_findings 138, local_resolver_noise 10,
    tooling_config_blockers 0

## Validation Not Run

- Frontend `npm --prefix frontend run typecheck`, `npm --prefix frontend run
  test -- --run`, and `npm --prefix frontend run build` were not run because
  no frontend implementation changed. Frontend routing is covered by focused
  selector tests.
- Analytics focused suites beyond selector routing were not run because no
  analytics implementation, SQL, ingest, or view code changed.
- Local environment profile reports were not run because
  `docs/local_artifacts_manifest.json` and `tools/check_local_environment.py`
  were not changed in this implementation. Their routing is covered by focused
  selector tests, and the local-environment focused test suite passed.

## Remaining Risks And Unverified Layers

- `docs/validation_matrix.md` is manually synchronized with selector behavior;
  a future generator could reduce drift, but that is out of scope for #152.
- CT-227-001 remains adjacent scanner coverage debt and was not solved here.
- Pyright continues to report existing advisory findings; this implementation
  preserves advisory/non-blocking behavior.
- No CI evidence was produced because CI changes are out of scope.
- No frontend runtime validation was run because no frontend code changed.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #152, validation matrix reconciliation.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/152

Branch:
codex/analytics-foundation

Contract:
docs/contracts/validation_matrix_reconciliation.md

Implementation handoff:
docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md

Review scope:
- Verify the implementation against the contract, issue #152, stale PR #65 source-material decision, selector authority, orchestrator authority, and validation evidence.
- Review these intended files:
  - docs/contracts/validation_matrix_reconciliation.md
  - docs/validation_matrix.md
  - tools/select_validation.py
  - tests/test_select_validation.py
  - docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md

Check specifically:
- selector remains the executable changed-path recommendation authority;
- orchestrator remains the local bundle planner/runner and was not changed;
- docs/validation_matrix.md is non-authoritative and not runtime config;
- docs/validation_matrix.json was not revived as canonical executable config;
- no CI gates were added;
- Pyright is advisory and non-blocking;
- frontend, local app, developer launcher, analytics, local artifact, clean-install, and validation-reference surfaces route to focused recommendations;
- selector output still never claims validation passed;
- CT-227-001 remains adjacent scanner coverage debt, not silently solved;
- no parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed;
- no generated/private/local artifacts or secrets were introduced.

Suggested validation:
- python3 -m pytest -q tests/test_select_validation.py
- python3 -m pytest -q tests/test_hardening_orchestrator.py
- python3 -m pytest -q tests/test_check_local_environment.py tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py
- python3 -m ruff check tools tests src
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker and protected-surface checks over the reviewed files
- generated SQLite artifact scan

Do not:
- target main;
- stage or commit unless explicitly asked;
- add CI gates;
- make Pyright required/failing;
- revive PR #65 directly;
- add docs/validation_matrix.json as executable selector config;
- change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

Output:
- findings first, if any;
- validation reviewed or rerun;
- remaining risks;
- recommendation for Codex F if clean, otherwise Codex D or B;
- workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/152"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/validation_matrix_reconciliation.md"
  target_artifact: "docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "python3 -m pytest -q tests/test_select_validation.py"
    - "python3 -m pytest -q tests/test_hardening_orchestrator.py"
    - "python3 -m pytest -q tests/test_check_local_environment.py tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py"
    - "python3 -m ruff check tools tests src"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped selector run over intended files"
    - "path-scoped secret/private-marker scan over intended files"
    - "path-scoped protected-surface gate over intended files"
    - "generated SQLite artifact scan"
    - "python3 tools/run_pyright_advisory_report.py"
  stop_conditions:
    - "Do not target main."
    - "Do not revive stale PR #65 directly."
    - "Do not add CI gates or make Pyright required/failing."
    - "Do not create docs/validation_matrix.json as canonical executable config."
    - "Do not create a second unsynchronized validation authority."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create, delete, move, copy, sanitize, archive, or commit generated/private/local artifacts or secrets."
```
