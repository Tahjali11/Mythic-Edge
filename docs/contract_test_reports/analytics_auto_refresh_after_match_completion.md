# Analytics Auto-Refresh After Match Completion Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/294

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/302

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Contract

`docs/contracts/analytics_auto_refresh_after_match_completion.md`

## Implementation Under Test

- Branch: `codex/analytics-auto-refresh-isolation-294`
- Base branch: `origin/codex/analytics-foundation`
- Worktree: sibling checkout `MythicEdge-auto-refresh-294`
- Implementation handoff: `docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_fixer.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

This final approval is limited to the #294 contract-tested implementation package in this isolated worktree. It does not authorize merge, tracker closure, production behavior, workbook changes, or issue closure.

## Findings

No blocking findings remain.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-294-001 | P1 | `fixed_state_followup` | Fixed. Unsafe persisted SQLite timestamp metadata no longer echoes through `GET /api/analytics/refresh-state` public timestamp fields or raw revision inputs. | not_blocking | Initial Codex E review found `_string_or_none(...)` accepted any non-empty string, allowing unsafe persisted timestamp-like SQLite values to echo through `latest_completed_match_seen_at`, `latest_completed_ingest_finished_at`, and revision inputs. | `src/mythic_edge_parser/local_app/analytics_refresh_state.py` now sanitizes timestamp fields with `_safe_iso_or_none(...)`; `_max_updated_at(...)`, latest-completed helpers, and `_revision_for_metadata(...)` use sanitized timestamp values. Focused backend regression proves unsafe persisted timestamp metadata is dropped and does not alter the revision when only unsafe metadata changes. Frontend API validation now rejects unsafe refresh-state timestamp fields. | F |

## Contract Summary

The #294 contract requires a read-only, backend-owned, sanitized analytics refresh-state endpoint. The frontend may poll the opaque backend revision and refresh analytics views when it changes, but it must not infer parser truth, match completion, win/loss, or issue #302 live-capture no-row diagnostics.

## Internal Project Area Reviewed

Local app analytics backend/frontend support.

## Bridge-Code Status Reviewed

`shared_support`

## Files Reviewed

- `docs/contracts/analytics_auto_refresh_after_match_completion.md`
- `docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md`
- `docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_fixer.md`
- `docs/contract_test_reports/analytics_auto_refresh_after_match_completion.md`
- `src/mythic_edge_parser/local_app/analytics_refresh_state.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_auto_refresh_after_match_completion.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git diff --name-status
git log --oneline --name-status HEAD..origin/codex/analytics-foundation
py -m pytest -q tests\test_analytics_auto_refresh_after_match_completion.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_live_app_parser_owned_fact_capture_sqlite.py
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over #294 files
path-scoped secret/private-marker scan over #294 files
git check-ignore -v frontend/node_modules
Test-Path frontend\dist
```

## Results

CT-294-001 is confirmed fixed.

The backend now validates timestamp-like SQLite metadata before public output and before revision hashing. Unsafe strings become `null` and do not alter the revision when only unsafe timestamp metadata changes. Safe ISO timestamp strings still pass through. Frontend refresh-state validation now requires ISO timestamp strings or `null` for the two public refresh timestamp fields.

The branch is currently behind `origin/codex/analytics-foundation` by 2 commits. Inspection shows the upstream movement is the ADR-0007 governance merge and docs package, not #294 backend/frontend code. This is a Codex F submission/sync risk, not a remaining #294 contract mismatch.

## Confirmed Contract Matches

- Active checkout is the isolated #294 package, not #302 implementation work.
- `GET /api/analytics/refresh-state` remains a local-app read-only route.
- The route rejects unsupported query parameters without echoing the rejected value.
- The response object and schema remain versioned as required by the contract.
- Unsafe persisted timestamp-like SQLite metadata is dropped from `latest_completed_match_seen_at` and `latest_completed_ingest_finished_at`.
- Unsafe persisted timestamp-like SQLite metadata is sanitized before revision hashing.
- Safe ISO timestamp metadata remains visible in the public timestamp fields.
- `analytics_revision` remains opaque to the frontend and changes only from safe aggregate metadata.
- The frontend API helper validates the refresh-state response shape before use.
- Frontend refresh-state validation rejects unsafe timestamp strings.
- Frontend polling remains conservative and visibility-aware in tested paths.
- Manual refresh controls remain available.
- Issue #302 heartbeat/no-row diagnostics remain separate and were not implemented in this slice.
- No parser truth, parser final reconciliation, analytics schema/migrations, live watcher behavior, Match Journal truth ownership, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer, or production behavior changes were identified.

## Remaining Contract Mismatches

None found in this confirmation pass.

## Missing Tests Or Safeguards

No blocking missing tests remain for CT-294-001.

Confirmed coverage includes:

- backend unsafe persisted timestamp regression;
- stable revision when only unsafe timestamp-like metadata changes;
- safe ISO timestamp pass-through;
- frontend rejection of unsafe refresh-state timestamp fields;
- existing route query-parameter rejection and read-only missing/empty/completed/error cases.

## Validation Run And Result

- `git status --short --branch --untracked-files=all` -> active #294 package remains modified/untracked in the isolated worktree; branch is behind base by 2.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` -> `0 2`.
- `git log --oneline --name-status HEAD..origin/codex/analytics-foundation` -> upstream movement is ADR-0007 governance docs from PR #309.
- `py -m pytest -q tests\test_analytics_auto_refresh_after_match_completion.py tests\test_analytics_local_app_backend.py` -> 35 passed, 1 existing FastAPI/Starlette warning.
- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_live_app_parser_owned_fact_capture_sqlite.py` -> 20 passed, 1 existing FastAPI/Starlette warning.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend test -- --run` -> 3 files passed, 90 tests passed.
- `npm --prefix frontend run build` -> passed.
- `frontend/dist` cleanup -> removed generated build output.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped protected-surface scan over #294 files -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over #294 files -> passed, forbidden 0, warnings 0.

## Protected-Surface Status

Passed. Path-scoped protected-surface scan over the #294 contract, handoffs, report, backend helper/route, frontend files, and tests reported forbidden 0 and warnings 0.

## Secret/Private-Marker Status

Passed. Path-scoped secret/private-marker scan over the #294 contract, handoffs, report, backend helper/route, frontend files, and tests reported forbidden 0 and warnings 0.

## Generated/Private Artifact Status

- `frontend/dist` was generated by build validation and removed.
- `Test-Path frontend\dist` returned `False`.
- `frontend/node_modules/` is present in the isolated worktree as an ignored dependency artifact; `git check-ignore -v frontend/node_modules` confirms `.gitignore` covers it.
- No unignored generated SQLite database, runtime file, raw log, JSONL payload, workbook export, env file, secret, credential, or local-only artifact is present in the Git commit surface.

## Drift Notes

- Branch freshness drift: the isolated branch is behind `origin/codex/analytics-foundation` by 2 ADR-0007 governance commits. Codex F should sync/rebase or otherwise publish against the current base before opening a PR.
- Package lifecycle drift: the #294 package remains uncommitted/untracked, so `git diff --name-status origin/codex/analytics-foundation...HEAD` will not show the full package until Codex F stages/commits it.
- No workbook drift, deployment drift, production drift, or private app-data drift was inspected or implied.

## Recommendation

Approve for Codex F submission, with one submitter caveat: Codex F must handle the `0 2` branch-behind state before or during publication and stage only the reviewed #294 package.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #294.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/302

Branch:
codex/analytics-auto-refresh-isolation-294

Base branch:
origin/codex/analytics-foundation

Worktree:
sibling checkout MythicEdge-auto-refresh-294

Contract:
docs/contracts/analytics_auto_refresh_after_match_completion.md

Review artifact:
docs/contract_test_reports/analytics_auto_refresh_after_match_completion.md

Fixer handoff:
docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_fixer.md

Goal:
Submit the reviewed #294 analytics auto-refresh package as a narrow draft PR targeting codex/analytics-foundation. Stage only reviewed #294 files. Handle the current branch-behind state before publication if needed; upstream movement was ADR-0007 governance docs and should not be folded into the #294 staged package except through normal base sync.

Reviewed files:
- docs/contracts/analytics_auto_refresh_after_match_completion.md
- docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md
- docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_fixer.md
- docs/contract_test_reports/analytics_auto_refresh_after_match_completion.md
- src/mythic_edge_parser/local_app/analytics_refresh_state.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_auto_refresh_after_match_completion.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/api.test.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx

Do not:
- Stage unrelated files or ignored dependency/cache artifacts.
- Implement #302 no-row diagnostics.
- Change parser behavior, parser final reconciliation, analytics schema/migrations, live watcher behavior, Match Journal truth ownership, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior.
- Expose raw/private/generated/local artifacts or secrets.
- Merge, close #294, close #302, close tracker #204, or target main.

Suggested validation before commit:
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
py -m pytest -q tests\test_analytics_auto_refresh_after_match_completion.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_live_app_parser_owned_fact_capture_sqlite.py
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
Remove frontend/dist if created.
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over staged #294 files.

Final output:
- role performed
- branch and target branch
- files staged/committed
- commit hash
- draft PR URL
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/302"
  completed_thread: "E"
  next_thread: "F"
  branch: "codex/analytics-auto-refresh-isolation-294"
  base_branch: "origin/codex/analytics-foundation"
  worktree: "sibling checkout MythicEdge-auto-refresh-294"
  contract_artifact: "docs/contracts/analytics_auto_refresh_after_match_completion.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_fixer.md"
  review_artifact: "docs/contract_test_reports/analytics_auto_refresh_after_match_completion.md"
  fixed_state_verdict:
    - "CT-294-001 P1 fixed: unsafe persisted SQLite timestamp metadata no longer echoes through GET /api/analytics/refresh-state or raw revision inputs."
  validation:
    - "branch sync -> 0 2 behind origin/codex/analytics-foundation; upstream movement is ADR-0007 governance docs"
    - "backend focused tests -> 35 passed, 1 existing warning"
    - "adjacent live-capture tests -> 20 passed, 1 existing warning"
    - "frontend typecheck -> passed"
    - "frontend tests -> 90 passed"
    - "frontend build -> passed; frontend/dist removed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "agent docs -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  ignored_dependency_artifacts: "frontend/node_modules present and ignored by .gitignore"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
