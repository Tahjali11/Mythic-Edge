# Analytics App Match And Game History Views Contract-Test Report

## Findings

No remaining blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-225-001 | P1 | `fixed_state_followup` | fixed | not_blocking | The initial review found malformed `limit` and `offset` query values could echo raw private input through FastAPI's default 422 response. | `src/mythic_edge_parser/local_app/backend.py:159` now rejects unknown params and validates `limit` / `offset` manually with stable error codes only. `tests/test_analytics_app_match_game_history_views.py:229` covers malformed private-marker values, duplicate values, and out-of-range values. A direct runtime probe of private-marker `limit`, `offset`, duplicate, negative, out-of-range, and unknown query params returned stable `analytics_history_query_parameter_*` codes without echoing `Player.log`, `C:`, or `secret`. | F |
| CT-225-002 | P2 | `fixed_state_followup` | fixed | not_blocking | The initial review found frontend history response validation accepted arbitrary top-level `status` labels later displayed by `StatusPill`. | `frontend/src/api.ts:361` now requires `payload.status` to match the contract's allowed history status labels before returning a typed response. `frontend/src/api.test.ts:125` covers private-marker and unsupported status rejection and verifies the thrown error text does not echo the private marker. | F |

## Issue / Tracker / Umbrella

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/225
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract And Handoff Reviewed

- Contract: `docs/contracts/analytics_app_match_game_history_views.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md`
- Codex D handoff: supplied in-thread for CT-225-001 and CT-225-002 confirmation.

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed files reviewed:

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_app_match_game_history_views.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `docs/contracts/analytics_app_match_game_history_views.md`
- `docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md`
- `docs/contract_test_reports/analytics_app_match_game_history_views.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

This report is a Codex E follow-up after Codex D. The original findings are preserved above and marked as fixed after verification evidence.

## Contract Summary

The implementation adds fixed, read-only local app history endpoints and a curated read-only frontend history view over local analytics SQLite facts. It must not add arbitrary SQL, generic database browsing, destructive controls, schema/migration changes, parser/runtime/workbook/App Script/Sheets/AI/production behavior changes, or raw/private data exposure.

## Internal Project Area Reviewed

Local App / UI, with Analytics as the downstream storage/query support layer.

The parser remains truth owner for match/game facts and identity. SQLite and the local app remain downstream storage/display surfaces.

## Bridge-Code Status Reviewed

`bridge_code`

Allowed flow reviewed: analytics SQLite fact tables -> fixed read-only local backend responses -> frontend display.

## Checks Run

```powershell
git status --short --branch
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
py -m pytest -q tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over touched #225 files
path-scoped secret/private-marker scan over touched #225 files
git status --short --ignored frontend\dist data\analytics data\status data\runtime_logs data\failed_posts
```

Additional focused reviewer probe:

```powershell
@'
from fastapi.testclient import TestClient
from mythic_edge_parser.local_app.backend import create_app
from pathlib import Path
import tempfile, json
queries = [
    'limit=C:%5Csecret%5CPlayer.log',
    'offset=C:%5Csecret%5CPlayer.log',
    'limit=1&limit=2',
    'limit=0',
    'limit=101',
    'offset=-1',
    'table=C:%5Csecret%5CPlayer.log',
]
with tempfile.TemporaryDirectory() as d:
    client = TestClient(create_app(app_data_root=Path(d) / 'app-data'))
    for query in queries:
        response = client.get('/api/analytics/matches?' + query)
        body = json.dumps(response.json(), sort_keys=True)
        print(query, response.status_code, body)
        if 'Player.log' in body or 'C:\\secret' in body:
            raise SystemExit(f'private marker leaked for {query}: {body}')
'@ | py -
```

## Results

- Branch sync: `HEAD...origin/codex/analytics-foundation` -> `0 0`.
- Direct malformed-query probe -> all probed malformed/private query cases returned stable 422 error codes without private-marker echo.
- `py -m pytest -q tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py` -> passed, 26 tests, 1 existing FastAPI/Starlette dependency warning.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py` -> passed, 25 tests, 1 existing FastAPI/Starlette dependency warning.
- `py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py` -> passed, 22 tests.
- `py -m ruff check src tests tools` -> passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> passed, 3 files / 37 tests.
- `npm --prefix frontend run build` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0.
- Path-scoped protected-surface scan -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0.
- Generated artifact cleanup -> `frontend/dist/` produced by the frontend build was removed after validation.

## Confirmed Contract Matches

- `GET /api/analytics/matches` and `GET /api/analytics/games` exist.
- Happy-path response object names and schema version match the contract.
- Backend SQL projections are fixed and parameterized.
- Backend queries are limited to the contracted tables: `matches`, `games`, `match_results`, `game_results`, and `match_context`.
- Missing database, empty current database, schema-degraded database, invalid database, fixed-query failure states, malformed query params, duplicate query params, and out-of-range query params are covered by focused backend tests.
- Malformed numeric query parameters return stable codes without echoing raw private input.
- The frontend replaces the deferred Analytics Views panel with a read-only Analytics History section.
- Frontend history response validation rejects unsupported top-level `status` labels before display.
- Existing setup-status, manual import, browser upload, and folder upload tests still pass.
- No destructive database, import, job, launcher, or UI controls were found.
- No parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed in the reviewed scope.

## Contract Mismatches

None after Codex D follow-up.

## Missing Tests Or Safeguards

No blocking gaps found after Codex D follow-up.

Non-blocking: no live browser check against a real operator database was run in this confirmation thread.

## Protected-Surface Status

Forbidden protected surfaces touched: no.

The implementation changes are local app backend/frontend plus tests and docs. No parser, analytics schema/migration/ingest, workbook, webhook, Apps Script, Sheets, OpenAI/model-provider, AI/coaching, production, or CI gate changes were detected.

## Secret / Private-Marker Status

The direct malformed-query probe found no remaining private-marker echo for the fixed query paths.

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.

## Generated Artifact Status

No generated artifacts are tracked or staged.

The frontend build generated `frontend/dist/`; it was removed before final status checks.

## Remaining Risks

- Remote CI has not run in this thread.
- No live local browser check against a real operator database was run.
- Live workbook state, deployed Apps Script state, and production behavior remain unverified and out of scope.

## Recommendation

Route to Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #225.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/225

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_match_game_history_views.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md

Review artifact:
docs/contract_test_reports/analytics_app_match_game_history_views.md

Goal:
Stage only the reviewed issue #225 files, commit them, push the branch, and open or update a draft PR targeting the approved integration branch. Do not target main. Preserve unrelated local dirt and generated artifacts.

Before staging:
- Confirm branch is codex/analytics-foundation and is even with origin/codex/analytics-foundation.
- Inspect git status and identify unrelated dirty/untracked files.
- Confirm the contract-test report has no remaining blocking findings.
- Confirm frontend/dist, SQLite DB/WAL/SHM/journal files, raw logs, raw JSONL artifacts, runtime artifacts, failed posts, workbook exports, secrets, credentials, and local-only artifacts are not staged.

Intended issue #225 paths:
- docs/contracts/analytics_app_match_game_history_views.md
- docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md
- docs/contract_test_reports/analytics_app_match_game_history_views.md
- src/mythic_edge_parser/local_app/analytics_history.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_app_match_game_history_views.py
- tests/test_analytics_local_app_backend.py
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/status.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/api.test.ts
- frontend/src/App.test.tsx

Suggested validation before commit:
py -m pytest -q tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
path-scoped protected-surface scan over intended issue #225 paths
path-scoped secret/private-marker scan over intended issue #225 paths

Do not:
- stage unrelated files or generated artifacts
- target main
- close issue #225, tracker #204, or umbrella issue #207
- merge or deploy
- change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior
- change analytics schema, migrations, ingest behavior, fixtures, snapshots, raw logs, runtime artifacts, or local-only artifacts

Final handoff must include branch, commit hash, PR URL, target branch, files staged, validation run, checks status if available, protected-surface status, generated/private artifact status, remaining risk, and next recommended role.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/225"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-foundation"
  contract: "docs/contracts/analytics_app_match_game_history_views.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md"
  artifact_updated: "docs/contract_test_reports/analytics_app_match_game_history_views.md"
  findings:
    - "No remaining blocking findings."
    - "CT-225-001 fixed: malformed limit/offset query values now return stable sanitized 422 codes without raw private input echo."
    - "CT-225-002 fixed: frontend history status validation now rejects unsupported/private-marker labels before display."
  validation:
    - "branch sync -> 0 0"
    - "direct malformed-query probe -> passed"
    - "backend focused tests -> 26 passed, 1 existing third-party warning"
    - "adjacent import tests -> 25 passed, 1 existing third-party warning"
    - "schema/derived/replay tests -> 22 passed"
    - "ruff -> passed"
    - "frontend typecheck/test/build -> passed"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "No forbidden protected surfaces touched."
  generated_artifact_status: "frontend/dist generated by validation build and removed."
  forbidden_scope_touched: false
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
```
