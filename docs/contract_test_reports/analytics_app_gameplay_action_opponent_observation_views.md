# Analytics App Gameplay Action And Opponent Observation Views Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/228

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:
`docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md`

Changed implementation surfaces reviewed:

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `tests/test_analytics_app_gameplay_action_opponent_observation_views.py`
- `tests/test_analytics_local_app_backend.py`
- `docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md`
- `docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

This report began as `initial_contract_test` and found CT-228-001. After Codex
D fixed the finding, Codex E reran the focused reproduction and validation
checks. No blocking findings remain.

## Contract Summary

Issue #228 adds read-only local app review views over stored SQLite gameplay-action
and opponent-card-observation facts. The slice may expose only fixed,
parameterized, read-only endpoints and curated frontend display. It must not add
opening-lines, arbitrary SQL, destructive controls, parser behavior changes,
schema/migration/ingest changes, workbook/webhook/App Script/Sheets changes,
Line Tracer, AI/coaching behavior, hidden-card inference, best-line labels, or
private artifact leakage.

## Internal Project Area Reviewed

Primary area: Local App / UI.

Supporting area: Analytics.

Truth owner preserved: parser/state remains the truth owner for gameplay-action
facts, opponent-card-observation facts, event interpretation, match/game
identity, deduplication, and final reconciliation.

## Bridge-Code Status Reviewed

Reviewed as `bridge_code` from Analytics SQLite storage to Local App / UI.

## Findings

No blocking findings remain.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-228-001 | P1 | `fixed_state_followup` | verified fixed | not_blocking | `src/mythic_edge_parser/local_app/analytics_history.py:893` originally mapped `degradation_flags` through `_degradation_flags()`, and `_degradation_flags()` at `src/mythic_edge_parser/local_app/analytics_history.py:993` accepted any valid JSON array of strings. The contract requires a safe string-array at `docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md:500` and says no private paths may appear in endpoint responses at `docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md:850`. The initial focused test covered a malformed raw path string, but not a valid JSON array containing a private marker. | D added `_safe_degradation_flags()` and `_is_safe_degradation_flag()` in `src/mythic_edge_parser/local_app/analytics_history.py` and added `test_opponent_observation_review_redacts_valid_degradation_flag_private_markers()` in `tests/test_analytics_app_gameplay_action_opponent_observation_views.py`. Codex E replayed the original probe with `["missing_expected_evidence", "C:\\secret\\Player.log", "https://example.invalid/local-artifact"]`; the endpoint returned `["missing_expected_evidence", "opponent_observation_degradation_flag_redacted"]`, `review_required_row_count` was 1, and the encoded response contained none of `Player.log`, `C:`, `secret`, `https://`, or `local-artifact`. Focused #228 pytest passed, 23 tests. | F |

### CT-228-001 Detail

The malformed-degradation-flag guard is good, but it only protects invalid JSON
or non-string entries. A syntactically valid JSON array containing a private
path is considered safe by `_degradation_flags()` and is returned in the backend
JSON response. The frontend `SafeCell` layer can redact display, but the
contract explicitly covers endpoint responses too.

Fixed-state confirmation:

- unsafe parsed degradation flag entries are replaced by the stable
  `opponent_observation_degradation_flag_redacted` marker;
- safe documented flags such as `missing_expected_evidence` are preserved;
- the endpoint no longer echoes the raw private path or URL from a valid JSON
  array;
- the regression test covers valid JSON list private path and URL markers.

## Checks Run

```powershell
git status --short --branch
git fetch --prune
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
gh issue view 228 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
py -m pytest -q tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
py tools\check_agent_docs.py
npm --prefix frontend ci
npm --prefix frontend install
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
@'
docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md
docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md
src/mythic_edge_parser/local_app/analytics_history.py
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_app_gameplay_action_opponent_observation_views.py
tests/test_analytics_local_app_backend.py
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/App.test.tsx
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md
docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md
src/mythic_edge_parser/local_app/analytics_history.py
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_app_gameplay_action_opponent_observation_views.py
tests/test_analytics_local_app_backend.py
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/App.test.tsx
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Additional direct reproduction probe:

```text
Inserted a temp opponent observation with degradation_flags ["C:\\secret\\Player.log"].
GET /api/analytics/opponent-card-observations returned the raw flag value.
Encoded response contained Player.log=True, C:=True, secret=True.
```

## Results

- Branch sync: `HEAD...origin/codex/analytics-foundation -> 0 0`.
- Issue #228 is open.
- Direct fixed-state probe: passed; unsafe valid JSON degradation flag entries
  were redacted before backend response serialization.
- Focused #228 pytest: `23 passed`, with one existing FastAPI/Starlette
  deprecation warning.
- Focused backend/local app slice: `70 passed`, with one existing
  FastAPI/Starlette deprecation warning.
- Adjacent analytics ingest/schema/view/replay slice: `70 passed`.
- Ruff: passed.
- Agent docs check: passed.
- Frontend typecheck: passed.
- Frontend tests: `3 files passed`, `47 tests passed`.
- Frontend build: passed; generated `frontend/dist` removed afterward.
- `git diff --check`: passed.
- Path-scoped protected-surface scan including the report: passed, forbidden 0,
  warnings 0.
- Path-scoped secret/private-marker scan including the report: passed,
  forbidden 0, warnings 0.

## Confirmed Contract Matches

- Added exactly the contracted backend endpoints:
  `GET /api/analytics/gameplay-actions` and
  `GET /api/analytics/opponent-card-observations`.
- Endpoint object names and schema version match the contract.
- Existing sanitized `limit` and `offset` query parsing is reused; unapproved,
  duplicate, malformed, and out-of-range query parameters are rejected without
  raw echo.
- Backend queries are fixed SQL over allowed analytics tables and joined context
  tables; no arbitrary SQL, database browser, or destructive route was added.
- Parent-row pagination is used, with child-card rows fetched by fixed
  parameterized parent-id queries.
- Gameplay-action rows preserve zero-child groups and child cards.
- Opponent-card-observation rows preserve zero-child groups, linked action
  context only when stored, child cards, visibility/evidence/review labels, and
  malformed-degradation warning behavior.
- Missing, empty, schema-degraded, query-error, and malformed-query states are
  covered by focused backend tests.
- Frontend adds a read-only Action Review section with response validation,
  safe display cells, summary counts, loading/empty/degraded/error states, and a
  refresh-only control.
- `GET /api/analytics/opening-lines` remains unexposed.
- No parser, analytics schema/migration/ingest, workbook, webhook, Apps Script,
  Sheets, Line Tracer, AI/OpenAI, coaching, production, or CI gate changes were
  observed in the #228 diff.

## Contract Mismatches

- None remaining.

## Missing Tests Or Safeguards

- None blocking. The D fix added the missing backend regression for valid JSON
  degradation flag arrays containing private path and URL markers.

## Drift Notes

- No branch drift: local HEAD is even with `origin/codex/analytics-foundation`.
- No workbook, deployed Apps Script, parser/runtime, schema/migration, ingest,
  production, or live-data drift was verified or changed in this pass.
- Ignored local data directories exist under `data/`, but they are outside the
  #228 diff and were not touched by this review.
- Frontend build output was generated by validation and removed.

## Protected-Surface Status

Path-scoped protected-surface gate passed with forbidden 0 and warnings 0.

Forbidden scope touched: no implementation diff evidence found for parser
behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migration/ingest,
workbook schema, webhook payload shape, Apps Script behavior, Google Sheets,
Line Tracer, AI/OpenAI, coaching, production behavior, secrets, credentials,
raw logs, private JSONL artifacts, generated SQLite databases, runtime status
files, failed posts, workbook exports, or local-only runtime artifacts.

## Secret / Private-Marker Status

Path-scoped scanner passed with forbidden 0 and warnings 0.

Review-only direct runtime probe confirmed the unsafe-but-valid
`degradation_flags` leak is fixed. Runtime SQLite data containing a private path
or URL is now returned as a stable redaction marker instead of raw text.

## Generated Artifact Status

- `frontend/dist` was created by `npm --prefix frontend run build` and removed.
- No tracked or untracked generated SQLite DB/WAL/SHM/journal artifacts were
  observed in `git status --short`.
- Existing ignored local `data/` directories were visible in ignored status but
  were not part of this review package.

## Recommendation

Approve for submitter.

Next role: Codex F: Module Submitter.

## Next Workflow Action

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #228.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/228

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md

Review artifact:
docs/contract_test_reports/analytics_app_gameplay_action_opponent_observation_views.md

Goal:
Submit the reviewed #228 package. Stage only the intended files for the gameplay-action and opponent-card-observation review views, commit, push, and open or update a draft PR targeting the correct integration branch. Do not target main.

Before staging:
- confirm branch is codex/analytics-foundation;
- inspect git status and identify unrelated or generated files;
- confirm CT-228-001 is marked verified fixed in the review artifact;
- stage only the reviewed #228 contract, handoff, report, backend, frontend, and focused test files.

Expected reviewed files:
- docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md
- docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md
- docs/contract_test_reports/analytics_app_gameplay_action_opponent_observation_views.md
- src/mythic_edge_parser/local_app/analytics_history.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_app_gameplay_action_opponent_observation_views.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/api.test.ts
- frontend/src/App.test.tsx

Validation to rerun or cite from Codex E:
- focused #228 pytest -> 23 passed
- adjacent local app history/backend pytest -> 70 passed
- analytics ingest/schema/replay pytest -> 70 passed
- ruff -> passed
- frontend typecheck -> passed
- frontend vitest -> 47 passed
- frontend build -> passed, generated dist removed
- git diff --check -> passed
- agent docs check -> passed
- path-scoped protected-surface scan -> passed
- path-scoped secret/private-marker scan -> passed

Do not:
- target main;
- stage unrelated or generated files;
- change implementation during submitter work unless a concrete submitter blocker appears;
- change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior;
- create or commit generated SQLite files, raw logs, private JSONL artifacts, frontend build output, runtime artifacts, failed posts, workbook exports, secrets, credentials, API keys, tokens, webhook URLs, or local-only artifacts;
- merge, deploy, close issue #228, or mark tracker #204/umbrella #207 complete unless explicitly asked.

Final handoff must include:
- branch
- commit hash
- draft PR URL and target branch
- files staged/committed
- validation cited or rerun
- protected-surface and generated/private artifact status
- remaining risk
- next role: Codex G or Codex E if submitter blockers appear
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/228"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_app_gameplay_action_opponent_observation_views.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  findings:
    - "No blocking findings remain."
    - "CT-228-001 P1 verified fixed: valid JSON-array degradation_flags private markers are redacted before backend response serialization."
  validation:
    - "branch sync -> 0 0"
    - "direct fixed-state probe -> passed; private path and URL were redacted to opponent_observation_degradation_flag_redacted"
    - "focused #228 pytest -> 23 passed, 1 existing FastAPI/Starlette warning"
    - "focused backend/local app slice -> 70 passed, 1 existing FastAPI/Starlette warning"
    - "adjacent analytics ingest/schema/view/replay slice -> 70 passed"
    - "ruff -> passed"
    - "agent docs check -> passed"
    - "frontend typecheck -> passed"
    - "frontend tests -> 47 passed"
    - "frontend build -> passed; frontend/dist removed afterward"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex F: Module Submitter"
```
