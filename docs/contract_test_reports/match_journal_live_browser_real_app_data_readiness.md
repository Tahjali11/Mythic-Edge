# Match Journal Live-Browser Real App-Data Readiness Contract-Test Report

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/236>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Contract

`docs/contracts/match_journal_live_browser_real_app_data_readiness.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:

- `docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md`

Changed files reviewed:

- `docs/contracts/match_journal_live_browser_real_app_data_readiness.md`
- `docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `tools/dev_app/dev_app_launcher.py`
- `tests/test_analytics_dev_app_launcher.py`
- `tests/test_analytics_local_app_backend.py`

## Report Lifecycle

`report_lifecycle`: `initial_contract_test`

## Contract Summary

Issue #236 must prove the Match Journal cockpit can be safely exercised through
the real local developer app path while using disposable app-data first,
approval-gating actual app-data, preserving symbolic path/redaction behavior,
and avoiding parser/runtime/analytics/workbook/webhook/App Script/Sheets/
OpenAI/AI/coaching/production changes.

## Internal Project Area Reviewed

Local App / UI, with Generated / Local Artifacts and Quality / Governance as
supporting areas.

## Bridge-Code Status Reviewed

`stable_bridge`: browser UI -> FastAPI local app facade -> app-owned Match
Journal service/repository -> readiness evidence.

## Findings

No blocking findings remain.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-236-001 | P2 | `remaining_non_blocking` | Browser write/persistence smoke is blocked by missing safe visible context in the empty disposable app-data root. This is contract-consistent and should route to a later synthetic-context or unattached-note follow-up if desired. | non_blocking | Contract allows marking write smoke blocked when no safe visible context exists and forbids inventing parser IDs or forcing direct backend writes. Codex C handoff recorded `blocked_no_safe_context`. | Code review found no forced parser IDs or direct backend write workaround. Automated frontend/backend tests passed. | F / follow-up issue |

## Confirmed Contract Matches

- Branch is `codex/analytics-foundation`; local branch and origin are even (`0 0`).
- Issue #236 is open; tracker #202 remains open and was not marked complete.
- `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` is used as a narrow local launcher/backend bridge so Uvicorn-created backend apps can honor the launcher-selected app-data root.
- `build_local_app_paths(..., env=...)` still prefers explicit `app_data_root` and only falls back to the launcher bridge or `%LOCALAPPDATA%\MythicEdgeDev`.
- `create_app(...)` now resolves one `LocalAppPaths` object up front and uses its app-data root for manual/browser import helpers, keeping local routes on the same selected root.
- Launcher start mode passes the selected app-data root to the backend child process and removes stale bridge values when no root is available.
- Setup/status with launcher env uses symbolic Match Journal paths only and does not expose the launcher root or `%LOCALAPPDATA%` fallback root.
- Setup/status does not create the launcher root or fallback root.
- First explicit journal write creates only `<app_data>\db\match_journal.sqlite3` under the launcher-selected root and does not create analytics SQLite.
- Disposable-root live smoke evidence stayed within the contract: backend/frontend reached `200`, setup/status and cockpit rendered, no destructive/pilot-error/AI/Line Tracer controls were reported, and the write step was blocked instead of forced when no safe context existed.
- Actual-root readiness and actual-root write smoke were not run without approval.
- Direct status API global CORS remains unchanged/deferred.
- No parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest/views, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, or production behavior changed.

## Contract Mismatches

- None found.

## Missing Tests Or Safeguards

- No blocking missing tests remain.
- A future follow-up should add a safe browser-visible context seed, an unattached-note UI path, or another approved non-destructive path if the project wants the browser write/persistence smoke to complete instead of stopping at `blocked_no_safe_context`.
- The local bridge env var is currently duplicated as a string constant in launcher and backend path modules. This is acceptable for this narrow bridge, but a future cleanup could centralize it if more local-app env bridge variables appear.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# ## codex/analytics-foundation...origin/codex/analytics-foundation
# modified #236 local app/launcher/test files plus untracked #236 contract, handoff, and report

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
# 0 0

gh issue view 236 --json number,title,state,body,labels,url
# OPEN, [journal/app] Match Journal live-browser smoke and real app-data readiness

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
# 12 passed, 1 Starlette/FastAPI testclient deprecation warning

py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
# 34 passed, 1 Starlette/FastAPI testclient deprecation warning

npm --prefix frontend test -- --run src/App.test.tsx
# 1 file passed, 33 tests passed

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run build
# passed; generated frontend/dist removed afterward

py -m ruff check src tests tools
# passed

py tools\check_agent_docs.py
# passed, errors 0, warnings 0

git diff --check
# passed
```

## Disposable-Root Smoke Status

Reviewed from the Codex C handoff; not rerun by Codex E.

Status: partially passed with contract-consistent browser write blocker.

- App-data root class: `disposable`.
- Backend `/api/health`: `200` in Codex C smoke evidence.
- Frontend: `200` in Codex C smoke evidence.
- Browser opened loopback frontend in Codex C smoke evidence.
- Setup/status displayed Match Journal readiness and symbolic
  `<app_data>\db\match_journal.sqlite3`.
- Cockpit rendered without reported destructive, pilot-error, direct status
  API write, raw SQL, Sheets, OpenAI, AI/coaching, Line Tracer, hidden-card,
  player-mistake, or best-line controls.
- Browser write/persistence: `blocked_no_safe_context`; no parser IDs were
  invented and no direct backend write was forced.

## Actual-Root Readiness Approval State

Actual-root readiness was not run. Actual-root write smoke was not run.

No explicit approval was requested or granted in this review thread to inspect,
write, reset, clean, delete, move, rename, archive, sanitize, copy, or upload
actual app-data contents.

## Generated Artifact Status

`npm --prefix frontend run build` generated ignored `frontend/dist` output
during validation. The resolved path was confirmed inside the repo and removed.
`Test-Path frontend\dist -> False`.

Generated SQLite/database artifact sweep returned no files outside `.git`.
Codex C's disposable `%TEMP%` smoke root is documented as external smoke
evidence and was not staged or committed.

## Protected-Surface Status

Path-scoped protected-surface scan passed for the #236 contract, handoff,
report, and changed local app/launcher/test files: forbidden 0, warnings 0.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed for the #236 contract, handoff,
report, and changed local app/launcher/test files: forbidden 0, warnings 0.

## Drift Notes

- Local-data drift: disposable-root smoke artifacts exist outside the repo per
  handoff; actual-root state remains uninspected and unmodified.
- Production/deployment drift: not evaluated and not changed.
- Tracker drift: tracker #202 remains open as required.

## Remaining Risks

- Browser write/persistence through the UI remains blocked until a safe visible
  context, synthetic context seed, or unattached-note UI path is approved.
- Actual-root metadata readiness and actual-root write smoke remain unverified
  pending explicit user approval.
- Direct status API global CORS hardening remains intentionally deferred.
- Future cockpit/overlay clients remain unverified.
- GitHub Actions were not run locally.

## Recommendation

Approve for Codex F: Module Submitter.

Recommended follow-up: create or route a later issue under tracker #202 for a
safe browser-visible journal context seed or unattached-note UI path if the
project wants the write/persistence smoke to complete instead of stopping at
`blocked_no_safe_context`.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #236.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/236

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_live_browser_real_app_data_readiness.md

Implementation handoff:
docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md

Review artifact:
docs/contract_test_reports/match_journal_live_browser_real_app_data_readiness.md

Goal:
Stage only the reviewed #236 files, commit, push, and open or update a draft PR
targeting the approved integration branch. Do not merge, close issue #236, or
mark tracker #202 complete.

Reviewed files expected:
- docs/contracts/match_journal_live_browser_real_app_data_readiness.md
- docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md
- docs/contract_test_reports/match_journal_live_browser_real_app_data_readiness.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/paths.py
- tools/dev_app/dev_app_launcher.py
- tests/test_analytics_dev_app_launcher.py
- tests/test_analytics_local_app_backend.py

Before staging:
- Confirm branch is codex/analytics-foundation and even with origin/codex/analytics-foundation.
- Inspect git status and separate unrelated files from reviewed #236 scope.
- Confirm frontend/dist is absent.
- Confirm generated SQLite files, raw logs, runtime artifacts, failed posts, workbook exports, secrets, and local-only artifacts are not staged.

Do not:
- target main;
- run actual-root readiness or actual-root write smoke without explicit user approval;
- delete, reset, wipe, rename, move, archive, clean, sanitize, copy, upload, or commit local app-data or private/generated artifacts;
- invent parser IDs or force a browser write with direct backend calls;
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior;
- change direct status API global CORS policy;
- stage unrelated files;
- merge, close issue #236, or mark tracker #202 complete unless explicitly asked.

Validation already reviewed by Codex E:
- focused Match Journal backend pytest passed
- local app launcher/backend/config pytest passed
- focused App.test.tsx passed
- frontend typecheck/build passed
- ruff, agent docs, git diff --check, protected-surface scan, and secret/private-marker scan passed
- frontend/dist removed; no repo SQLite artifacts found

Final handoff must include branch, commit hash, PR URL, PR target branch, staged files, validation evidence, generated/private artifact status, remaining risks, issue/tracker closure status, and next role Codex G only after PR exists.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/236"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/match_journal_live_browser_real_app_data_readiness.md"
  implementation_handoff: "docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md"
  target_artifact: "docs/contract_test_reports/match_journal_live_browser_real_app_data_readiness.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  findings:
    - "No blocking findings remain."
    - "CT-236-001 non-blocking: browser write/persistence remains blocked_no_safe_context and should route to a future context/unattached-note follow-up if desired."
  validation:
    - "git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0"
    - "gh issue view 236 --json number,title,state,body,labels,url -> OPEN"
    - "py -m pytest -q tests\\test_match_journal_cockpit_ui_backend.py -> 12 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py -> 34 passed, 1 warning"
    - "npm --prefix frontend test -- --run src/App.test.tsx -> 33 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite/database artifact sweep -> no files found outside .git"
    - "Test-Path frontend\\dist -> False"
  remaining_unverified:
    - "browser journal write/persistence with safe visible context"
    - "actual-root metadata readiness"
    - "actual-root write smoke"
    - "GitHub Actions"
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
