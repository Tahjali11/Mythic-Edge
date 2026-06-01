# Analytics App Opening Hand And Mulligan Views Contract-Test Report

## Findings

No blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- |
| CT-226-000 | none | `original_finding` | no_findings | not_blocking | Reviewed the implementation against `docs/contracts/analytics_app_opening_hand_mulligan_views.md`; focused backend/frontend validation passed; no contract mismatch or unsafe behavior was found in the reviewed scope. | F |

## Issue / Tracker / Umbrella

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/226
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/225

## Contract And Handoff Reviewed

- Contract: `docs/contracts/analytics_app_opening_hand_mulligan_views.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md`
- Role guidance: `docs/agent_threads/contract_test.md`, `docs/agent_threads/review.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed files reviewed:

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_app_opening_hand_mulligan_views.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `docs/contracts/analytics_app_opening_hand_mulligan_views.md`
- `docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md`
- `docs/contract_test_reports/analytics_app_opening_hand_mulligan_views.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

No remaining blocker findings exist. This approval routes the module to Codex F only; it does not authorize merge, deployment, issue closure, tracker closure, live workbook changes, or production behavior changes.

## Contract Summary

The contract requires a fixed, read-only local app early-game history slice:

- `GET /api/analytics/opening-hands`
- `GET /api/analytics/mulligans`

Both endpoints must use only `limit` and `offset`, return typed grouped parent rows with child card arrays, query only allowed analytics tables/views, preserve missing child rows as empty arrays, handle missing/degraded/error states safely, and avoid parser/runtime/workbook/webhook/App Script/Sheets/Line Tracer/AI/coaching/production changes.

## Checks Run

```powershell
git status --short --branch
git fetch --prune
gh issue view 226 --repo Tahjali11/Mythic-Edge --json number,title,state,body,url,comments
gh issue view 204 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 207 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 225 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m pytest -q tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over touched #226 files
path-scoped secret/private-marker scan over touched #226 files
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
    for endpoint in ['/api/analytics/opening-hands', '/api/analytics/mulligans']:
        for query in queries:
            response = client.get(endpoint + '?' + query)
            body = json.dumps(response.json(), sort_keys=True)
            print(endpoint, query, response.status_code, body)
            if 'Player.log' in body or 'C:' in body or 'secret' in body:
                raise SystemExit(f'private marker leaked for {endpoint}?{query}: {body}')
'@ | py -
```

## Results

- Branch state: `codex/analytics-foundation`.
- Issue state: #226 open, #204 open, #207 open, prerequisite #225 closed.
- Direct malformed-query probe -> passed; both early-game endpoints returned stable sanitized 422 codes without private-marker echo.
- `py -m pytest -q tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py` -> passed, 47 tests, 1 existing FastAPI/Starlette warning.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py` -> passed, 25 tests, 1 existing FastAPI/Starlette warning.
- `py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py` -> passed, 22 tests.
- `py -m ruff check src tests tools` -> passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> passed, 3 files / 42 tests.
- `npm --prefix frontend run build` -> passed.
- Frontend build artifact cleanup -> removed generated `frontend/dist/`.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0.
- New/untracked artifact whitespace, ASCII, and final-newline check -> passed.
- Path-scoped protected-surface scan -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0.

## Confirmed Contract Matches

- `GET /api/analytics/opening-hands` and `GET /api/analytics/mulligans` are present in `src/mythic_edge_parser/local_app/backend.py`.
- The routes reuse the sanitized `limit` / `offset` pagination guard from #225 and reject unapproved params without raw input echo.
- Backend parent queries paginate grouped parent rows first, then fetch child rows by selected parent ids using fixed parameterized child queries.
- Opening hand rows preserve zero-card parent groups as `cards: []`.
- Mulligan rows preserve zero-card parent groups as `cards: []`.
- Child card status objects participate in degraded/unavailable/conflict summary counts through recursive status traversal.
- Backend queries are read-only and limited to the contract-approved early-game, game/result, match-result, and match-context tables.
- Missing database, empty current database, unknown schema/degraded database, fixed-query failure, malformed query params, duplicate query params, and out-of-range query params are covered.
- Frontend API validation checks the early-game schema/object names, required shape, child card arrays, and allowed mulligan `card_action` labels before display.
- The frontend adds a read-only Early Game History section adjacent to Analytics History and preserves setup, import, upload, folder upload, match history, and game history behavior.
- No arbitrary SQL, generic DB browsing, destructive controls, Line Tracer behavior, coaching labels, best-keep recommendations, mulligan mistake labels, or strategic advice were found.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocking missing tests found.

Non-blocking: no live browser/manual visual check against a real operator database was run in this review thread.

## Protected-Surface Status

Forbidden protected surfaces touched: no.

The implementation is scoped to local app backend/frontend, focused tests, contract, and implementation handoff. No parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations, analytics ingest, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, Match Journal, Line Tracer, OpenAI/model-provider, AI/coaching, production behavior, or CI gate change was detected.

## Secret / Private-Marker Status

The direct malformed-query probe found no private-marker echo for the new early-game endpoints.

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.

## Generated Artifact Status

No generated artifacts are tracked or staged.

The frontend build generated `frontend/dist/`; it was removed before final status checks.

## Remaining Risks

- Remote CI has not run in this thread.
- Live local app browser rendering against a real operator database was not checked.
- Live workbook state, deployed Apps Script state, and production behavior remain unverified and out of scope.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #226.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/226

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Completed prerequisite:
https://github.com/Tahjali11/Mythic-Edge/issues/225

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_opening_hand_mulligan_views.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md

Review artifact:
docs/contract_test_reports/analytics_app_opening_hand_mulligan_views.md

Goal:
Stage only the reviewed issue #226 files, commit them, push the branch, and open or update a draft PR targeting the approved integration branch. Do not target main. Preserve unrelated local dirt and generated artifacts.

Before staging:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated dirty/untracked files.
- Confirm the contract-test report has no remaining blocking findings.
- Confirm frontend/dist, SQLite DB/WAL/SHM/journal files, raw logs, raw JSONL artifacts, runtime artifacts, failed posts, workbook exports, secrets, credentials, and local-only artifacts are not staged.

Intended issue #226 paths:
- docs/contracts/analytics_app_opening_hand_mulligan_views.md
- docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md
- docs/contract_test_reports/analytics_app_opening_hand_mulligan_views.md
- src/mythic_edge_parser/local_app/analytics_history.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_app_opening_hand_mulligan_views.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/api.test.ts
- frontend/src/App.test.tsx

Suggested validation before commit:
py -m pytest -q tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
path-scoped protected-surface scan over intended issue #226 paths
path-scoped secret/private-marker scan over intended issue #226 paths

Do not:
- stage unrelated files or generated artifacts
- target main
- close issue #226, tracker #204, or umbrella issue #207
- merge or deploy
- change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/Line Tracer/OpenAI/AI/coaching/production behavior
- change analytics schema, migrations, ingest behavior, fixtures, snapshots, raw logs, runtime artifacts, or local-only artifacts

Final handoff must include branch, commit hash, PR URL, target branch, files staged, validation run, checks status if available, protected-surface status, generated/private artifact status, remaining risk, and next recommended role.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / contract-test thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/226"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_prerequisite: "https://github.com/Tahjali11/Mythic-Edge/issues/225"
  branch: "codex/analytics-foundation"
  contract: "docs/contracts/analytics_app_opening_hand_mulligan_views.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md"
  artifact_produced: "docs/contract_test_reports/analytics_app_opening_hand_mulligan_views.md"
  findings:
    - "No blocking findings."
  validation:
    - "direct malformed-query probe -> passed"
    - "backend focused and compatibility tests -> 47 passed, 1 existing third-party warning"
    - "adjacent import/upload tests -> 25 passed, 1 existing third-party warning"
    - "schema/derived/replay tests -> 22 passed"
    - "ruff -> passed"
    - "frontend typecheck/test/build -> passed"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "new/untracked artifact whitespace/ascii/final-newline check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "No forbidden protected surfaces touched."
  generated_artifact_status: "frontend/dist generated by validation build and removed."
  forbidden_scope_touched: false
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
```
