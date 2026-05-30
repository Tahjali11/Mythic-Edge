# Implementation Handoff: Analytics Legacy JSONL Batch Import Fixer

## Role

Codex D: Module Fixer

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/213
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Branch: `codex/analytics-foundation`

## Source Artifacts

- Contract: `docs/contracts/analytics_legacy_jsonl_batch_import.md`
- Review artifact: `docs/contract_test_reports/analytics_legacy_jsonl_batch_import.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md`

## Fix Summary

This pass addressed only the Codex E review findings for executable safeguards:

- CT-213-001: added backend coverage for non-string entries inside `source_paths`.
- CT-213-002: added adapter coverage for a malformed selected file inside an explicit batch.
- CT-213-003: added frontend coverage for rejected, failed, and degraded batch import states.

No production code was changed in this fixer pass.

## Files Changed

- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_fixer.md`

## Contract Safeguards Added

- Backend batch validation now has tests proving integer and object entries in `source_paths` return `source_path_invalid` before app-data or database creation.
- Adapter batch validation now has a malformed selected-file test proving `adapt_legacy_jsonl_file_batch(...)` fails without leaving parser replay summaries and without exposing raw JSONL line text, payload marker, raw hash, or full local path in the exception.
- Frontend batch UI tests now cover terminal `rejected`, `failed`, and `degraded` job states and confirm raw submitted batch paths are cleared and not displayed.

## Forbidden Scope

Not touched:

- parser/runtime behavior
- saved-event replay semantics
- SQLite schema or migrations
- workbook schema
- webhook payload shape
- Apps Script or Sheets behavior
- Match Journal behavior
- OpenAI/AI/coaching behavior
- production behavior
- secrets, raw logs, generated data, runtime artifacts, retry payloads, workbook exports

## Validation

```powershell
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
```

Results:

- `py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_manual_jsonl_import.py` -> 26 passed, 1 third-party Starlette deprecation warning.
- `py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py` -> 35 passed, 1 third-party Starlette deprecation warning.
- `npm --prefix frontend ci` -> passed, 113 packages audited, 0 vulnerabilities.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 24 tests passed.
- `npm --prefix frontend run build` -> passed; generated `frontend/dist` was removed after validation.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Path-scoped protected-surface check over the touched fixer paths -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over the touched fixer paths -> passed, forbidden 0, warnings 0.

Note: a mistaken exploratory `py -m ruff check ... frontend/src/App.test.tsx` invocation failed because Ruff parses `.tsx` as Python. The intended repo Ruff command above passed.

## Working Tree Notes

The working tree already contained the broader #213 implementation files plus unrelated launcher dirt before this fixer pass. This pass intentionally did not stage, commit, push, or clean unrelated files.

## Next Role

Codex E: Module Reviewer / confirmation thread.
