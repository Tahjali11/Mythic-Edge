# Security Local Request Guard Mutating Loopback Routes Contract Test Report

## Findings

No blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-458-REFRESH-001 | P3 | `remaining_non_blocking` | Branch is behind `origin/main` by four commits, including a `pyproject.toml` quality-tooling change. | non_blocking | `git rev-list --left-right --count HEAD...origin/main` returned `0 4`; `git diff --name-status HEAD..origin/main` showed docs-only quality reports/contracts plus `pyproject.toml`. | Focused #458 validation passed on the branch, and an extra current-main Ruff logging tranche command passed: `py -m ruff check src\mythic_edge_parser\local_app tests --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015`. No local-app source overlap was observed. | F with refresh/revalidation before PR, or D/C only if the refresh surfaces conflicts. |

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/458>

## Parent Security Workflow

<https://github.com/Tahjali11/Mythic-Edge/issues/330>

## Contract

`docs/contracts/security_local_request_guard_mutating_loopback_routes.md`

## Implementation Handoff

`docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md`

## Implementation Under Test

Branch: `codex/local-request-guard-mutating-routes-458`

Worktree: sibling checkout `MythicEdge-security-next-330` (private local path redacted)

## Report Lifecycle

`report_lifecycle`: `initial_contract_test`

## Contract Summary

The #458 contract requires a process-local request guard for all current local app mutating loopback backend routes. The backend must reject missing, blank, invalid, disallowed-origin, and disallowed-host requests before route-specific behavior runs; the frontend must send the guard only in the custom header on guarded POST helpers; read-only GET routes remain unguarded in this slice; and no parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior may change.

## Internal Project Area Reviewed

Local app security boundary, backend route wiring, frontend API request wiring, and focused local app tests.

## Bridge-Code Status Reviewed

`shared_support`

The guard supports multiple local app write surfaces but does not bridge parser truth into downstream systems.

## Files Reviewed

- `docs/contracts/security_local_request_guard_mutating_loopback_routes.md`
- `docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `tests/local_app_request_guard_helpers.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `tests/test_live_app_explicit_start_capture_control.py`

## Confirmed Contract Matches

- Every current registered `/api/` POST route is listed in `GUARDED_MUTATING_API_ROUTES` and registered with the shared `require_local_request_guard` dependency.
- The route inventory test asserts that all registered `/api/` POST routes exactly match `GUARDED_MUTATING_API_ROUTES`, so a future unclassified mutating route should fail focused tests.
- Missing and blank guard headers return `401` with `local_request_guard_missing`.
- Invalid guard values return `403` with `local_request_guard_invalid`.
- Disallowed `Origin` returns `403` with `local_request_origin_not_allowed`.
- Disallowed `Host` returns `403` with `local_request_host_not_allowed`.
- Unavailable guard state is implemented as `503` with `local_request_guard_unavailable`.
- Guard comparison uses `hmac.compare_digest`.
- The guard token is generated with `secrets.token_urlsafe(32)` at backend app creation and is stored in FastAPI process state only.
- `GET /api/app/request-guard` returns the required bootstrap shape and is subject to local origin/host validation.
- CORS remains loopback-only and allows `X-Mythic-Edge-Local-Request-Guard`.
- Unsupported `POST /api/health` still returns FastAPI method handling instead of a guard failure.
- Read-only frontend GET helpers continue to omit the guard header.
- Frontend mutating helpers route through `guardedFetch`, fetch the guard once into module memory, and include the header on guarded POST requests.
- Browser JSONL upload includes the guard header without manually setting `Content-Type`.
- Existing route-specific tests were updated through a guarded TestClient helper so valid-token behavior remains covered.
- Issue #459 upload byte-limit hardening was not implemented in this slice.
- No parser truth, analytics schema/ingest, Match Journal truth ownership, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, CodeQL lifecycle, CI, or production behavior changes were observed in the reviewed diff.

## Contract Mismatches

No blocking contract mismatches found.

Non-blocking freshness note: the branch is four commits behind `origin/main`; see CT-458-REFRESH-001.

## Missing Tests Or Safeguards

No blocking missing tests found.

Remaining unverified layers:

- A live browser smoke was not run.
- GitHub CodeQL alert closure was not claimed or verified.
- The branch still needs refresh/revalidation against current `origin/main` before submitter PR routing.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
git diff --name-status
git diff --name-status HEAD..origin/main
gh issue view 458 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 330 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_match_journal_cockpit_ui_backend.py tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py tests\test_live_app_explicit_start_capture_control.py
py -m ruff check src\mythic_edge_parser\local_app tests
py -m ruff check src\mythic_edge_parser\local_app tests --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx
npm --prefix frontend run typecheck
git diff --check
py tools\check_agent_docs.py
```

Path-scoped protected-surface and secret/private-marker scans were run after this report was written over the changed #458 files and this report artifact.

## Results

- `git status --short --branch --untracked-files=all`: expected #458 implementation files modified/untracked; ignored `frontend/node_modules/` exists locally from prior npm validation and is not staged.
- Branch sync: `0 4` against `origin/main`.
- Upstream changed files: docs-only quality reports/contracts plus `pyproject.toml`.
- Issue #458: open.
- Parent issue #330: open.
- Focused backend/local-app pytest: passed, `84 passed`, with one existing Starlette/httpx deprecation warning.
- Ruff local app/tests scope: passed.
- Extra current-main Ruff logging tranche: passed.
- Focused frontend API/App tests: passed, `2 passed`, `96 passed`.
- Frontend typecheck: passed.
- `git diff --check`: passed after report creation.
- Agent docs check: passed after report creation, `errors 0`, `warnings 0`.

## Protected-Surface Status

Path-scoped protected-surface scan status: passed after report creation, `forbidden 0`, `warnings 0`.

The reviewed implementation touched only local app backend route wiring, frontend API helper wiring, focused tests, and docs artifacts. No protected parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production surfaces were changed.

## Secret And Private-Marker Status

Path-scoped secret/private-marker scan status: passed after report creation, `forbidden 0`, `warnings 0`.

The reviewed implementation does not commit a live guard token, raw Player.log content, raw JSONL payload, SQLite content, private path, raw hash, credential, endpoint secret, generated runtime artifact, workbook export, or local-only artifact.

## Generated Artifact Status

No generated build artifacts are kept in the tracked diff.

`frontend/node_modules/` exists as an ignored local validation dependency directory and must not be staged or committed.

## Forbidden Scope

Forbidden scope touched: false.

Observed changes did not implement #459 upload byte-limit hardening, cloud auth, user accounts, OAuth, durable credentials, persistent request-token storage, environment contract drift, CI changes, CodeQL alert mutation/dismissal, parser behavior changes, analytics schema changes, workbook/webhook/App Script/Sheets changes, OpenAI/AI/coaching changes, Line Tracer changes, or production behavior changes.

## Drift Notes

- Issue lifecycle: #458 and #330 remain open, as expected.
- Repo freshness: branch is behind current `origin/main` by four commits, including a `pyproject.toml` quality-tooling update. No local-app overlap was observed, and the new logging Ruff tranche passed manually, but Codex F should refresh/revalidate before PR routing.
- Generated/local artifact: ignored `frontend/node_modules/` exists locally from npm validation and is excluded from git status.

## Recommendation

Approve for Codex F submitter routing, with an explicit refresh/revalidation step against current `origin/main` before committing/pushing/opening a PR. Route to Codex D/C only if that refresh surfaces conflicts or validation failures.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #458.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/458

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/local-request-guard-mutating-routes-458

Contract:
docs/contracts/security_local_request_guard_mutating_loopback_routes.md

Implementation handoff:
docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md

Codex E review artifact:
docs/contract_test_reports/security_local_request_guard_mutating_loopback_routes.md

Goal:
Refresh the branch against current origin/main, re-run the #458 validation, then stage only the reviewed #458 files and open a draft PR if clean.

Reviewed files:
- docs/contracts/security_local_request_guard_mutating_loopback_routes.md
- docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md
- docs/contract_test_reports/security_local_request_guard_mutating_loopback_routes.md
- src/mythic_edge_parser/local_app/backend.py
- frontend/src/api.ts
- frontend/src/api.test.ts
- tests/local_app_request_guard_helpers.py
- tests/test_analytics_local_app_backend.py
- tests/test_match_journal_cockpit_ui_backend.py
- tests/test_analytics_manual_jsonl_import.py
- tests/test_analytics_browser_jsonl_upload.py
- tests/test_live_app_explicit_start_capture_control.py

Required validation before submit:
git status --short --branch --untracked-files=all
git fetch --prune origin
refresh branch against current origin/main using the repo's safe submitter workflow
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_match_journal_cockpit_ui_backend.py tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py tests\test_live_app_explicit_start_capture_control.py
py -m ruff check src\mythic_edge_parser\local_app tests
npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx
npm --prefix frontend run typecheck
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over reviewed #458 files
path-scoped secret/private-marker scan over reviewed #458 files

Do not:
- stage frontend/node_modules or any generated/private/local artifacts
- implement #459 upload byte-limit hardening
- mutate CodeQL alerts
- close #458 or #330
- change CI, parser behavior, analytics schema, Match Journal truth ownership, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior
- target main without explicit approval

Final output must include PR URL if opened, commit hash, target branch, validation results, protected/secret scan status, generated artifact status, and workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/458"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  related_follow_up: "https://github.com/Tahjali11/Mythic-Edge/issues/459"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/security_local_request_guard_mutating_loopback_routes.md"
  implementation_handoff: "docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md"
  review_artifact: "docs/contract_test_reports/security_local_request_guard_mutating_loopback_routes.md"
  branch: "codex/local-request-guard-mutating-routes-458"
  risk_tier: "High security workflow risk; medium local-app runtime risk"
  findings:
    - "No blocking findings."
    - "CT-458-REFRESH-001 P3 non-blocking: branch is 0 4 behind origin/main; Codex F should refresh/revalidate before PR routing."
  validation:
    - "focused backend/local-app pytest -> passed, 84 tests, 1 existing Starlette/httpx warning"
    - "py -m ruff check src\\mythic_edge_parser\\local_app tests -> passed"
    - "extra current-main Ruff logging tranche -> passed"
    - "frontend API/App tests -> passed, 96 tests"
    - "frontend typecheck -> passed"
    - "git diff --check -> passed after report creation"
    - "agent docs -> passed after report creation"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  generated_artifacts_kept: "No tracked generated artifacts; ignored frontend/node_modules exists locally and must not be staged."
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter with refresh/revalidation before PR"
```
