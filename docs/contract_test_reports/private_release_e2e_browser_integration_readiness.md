# Private Release E2E Browser Integration Readiness Report

```text
schema_version: private_release_e2e_browser_integration_readiness.v1
issue: https://github.com/Tahjali11/Mythic-Edge/issues/287
previous_readiness_issue: https://github.com/Tahjali11/Mythic-Edge/issues/285
previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/286
tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
umbrella_issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
related_match_journal_tracker: https://github.com/Tahjali11/Mythic-Edge/issues/202
branch_under_test: origin/codex/analytics-foundation
commit_under_test: f0b9cc94808dc09961be0e396e84b7a4ffdbaa6c
platform: Darwin 24.6.0 arm64
smoke_mode: disposable_app_data_browser_smoke
app_data_root_mode: disposable_outside_repo_removed_after_smoke
backend_url: http://127.0.0.1:8765
frontend_url: http://127.0.0.1:5178
verdict: ready_with_acceptable_degradation
```

## Post-Fix Rerun Addendum

Status: post-fix disposable-root browser smoke passed with acceptable
degradation.

Codex C reran the contracted smoke for issue #287 after PR #286 merged the
error-report redaction fix into `codex/analytics-foundation`.

- PR #286 state: merged.
- Merge commit under test:
  `f0b9cc94808dc09961be0e396e84b7a4ffdbaa6c`.
- `origin/codex/analytics-foundation` resolved to that merge commit.
- Issue #287 was open at rerun time.
- Previous issue #285 was closed at rerun time.
- The primary `Mythic-Edge-analytics-foundation` worktree remained dirty/stale
  with unrelated #203 files, so the rerun used a clean detached sibling
  worktree at the remote branch head.

Current verdict: `ready_with_acceptable_degradation`.

The previous `not_ready_privacy_blocked` history remains below. It is
superseded by the post-fix rerun for the current branch head, but preserved as
the historical evidence that led to PR #286.

### Post-Fix Validation Matrix

| Command | Result | Evidence |
| --- | --- | --- |
| `python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py` | Passed | `41 passed`. |
| `python3 -m pytest -q tests/test_private_local_v1_setup.py` | Passed | `10 passed`. |
| `python3 -m pytest -q tests/test_match_journal_cockpit_ui_backend.py tests/test_match_journal_status_api.py` | Passed | `35 passed`. |
| `python3 -m pytest -q tests/test_analytics_browser_jsonl_upload.py tests/test_analytics_manual_jsonl_import.py` | Passed | `25 passed`. |
| `python3 -m pytest -q tests/test_analytics_dynamic_decision_support_dashboard.py` | Passed | `8 passed`. |
| `npm --prefix frontend ci` | Passed | 114 packages installed; 0 vulnerabilities reported. |
| `npm --prefix frontend run typecheck` | Passed | TypeScript completed without reported errors. |
| `npm --prefix frontend run test -- --run` | Passed | 3 test files passed; 75 tests passed. |
| `npm --prefix frontend run build` | Passed | Vite build completed; `frontend/dist` was removed afterward. |
| `python3 -m ruff check src tests tools` | Passed | Ruff reported no issues. |
| `git diff --check` | Passed | No whitespace errors after report edit. |
| `python3 tools/check_agent_docs.py` | Passed | 30 files checked; 0 errors; 0 warnings. |
| `printf '%s\n' docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md \| python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin` | Passed | 1 path scanned; forbidden 0; warnings 0. |
| `printf '%s\n' docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md \| python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin` | Passed | 1 changed path; forbidden 0; warnings 0. |
| Generated/private artifact sweep | Passed | No repo-local SQLite database, SQLite sidecar, or `frontend/dist` artifact found. |

Environment notes:

- Platform: Darwin 24.6.0 arm64.
- Python: 3.14.3.
- FastAPI: 0.136.3.
- Uvicorn: 0.49.0.
- `python-multipart`: 0.0.30.
- Node: v24.14.0.
- npm: 11.9.0.

### Post-Fix Backend Route Matrix

All routes were exercised against the disposable loopback backend.

| Route | HTTP | Status | Schema/Object |
| --- | ---: | --- | --- |
| `GET /api/health` | 200 | `ok` | `mythic_edge_local_app_health` |
| `GET /api/app/setup-status` | 200 | `degraded` | `mythic_edge_local_app_setup_status` |
| `GET /api/app/config` | 200 | `missing` | `mythic_edge_local_app_config_status` |
| `GET /api/app/paths` | 200 | `degraded` | `mythic_edge_local_app_paths_status` |
| `GET /api/analytics/database/status` | 200 | `missing` | `mythic_edge_local_app_analytics_database_status` |
| `GET /api/analytics/dashboard/modules` | 200 | `missing` | `mythic_edge_local_app_analytics_dashboard_modules` |
| `GET /api/live/player-log/status` | 200 | `missing` | `mythic_edge_local_app_live_player_log_status` |
| `GET /api/live/watcher/status` | 200 | `blocked_missing_log` | `mythic_edge_local_app_live_watcher_status` |
| `GET /api/live/watcher/process` | 200 | `blocked_missing_log` | `mythic_edge_local_app_live_watcher_process_status` |
| `GET /api/live/watcher/diagnostics` | 200 | `blocked` | `mythic_edge_local_app_live_watcher_diagnostics` |
| `GET /api/live/ingest/status` | 200 | `disabled` | `mythic_edge_local_app_live_parser_sqlite_capture_status` |
| `GET /api/runtime/status` | 200 | `ok` | `mythic_edge_local_app_runtime_status` |

### Post-Fix Browser Smoke Matrix

The in-app Browser and Chrome extension surfaces were unavailable in this
session, so the rerun used a temporary `puppeteer-core` harness under `/tmp`
against the existing local Google Chrome binary. The temporary harness and
Chrome profile were deleted after the smoke. No repo files were added by the
browser fallback.

| Browser observation | Result |
| --- | --- |
| Main page HTTP status | 200 |
| Page title | `Mythic Edge Local Status` |
| `Mythic Edge Cockpit` heading | Present |
| Dashboard section | Present |
| Decision Support section | Present |
| Analytics / Review area | Present |
| Import section | Present |
| Match Journal section | Present |
| Setup/status content | Present |
| Live Player.log content | Present |
| Diagnostics content | Present |
| Runtime/app connection status content | Present |
| Error report surface | Present |
| Contracted dashboard module titles | Present |
| Loopback API calls | Observed successful calls to `http://127.0.0.1:8765/...` routes. |
| OpenAI/model-provider controls | Not observed. |
| Deploy/Google Sheets controls | Not observed. |
| Console/runtime errors | One non-blocking `favicon.ico` 404; no page errors and no failed app API requests. |

No screenshots were committed.

### Post-Fix Import/Data Recognition Evidence

The safer minimum import path was used.

- Manual import controls rendered in browser smoke.
- `POST /api/imports/jsonl` with an empty request returned sanitized rejected
  status with `source_path_required`.
- No analytics SQLite database was created by this import recognition smoke.
- No private JSON/JSONL file was read or copied.

### Post-Fix Analytics Dashboard Evidence

`GET /api/analytics/dashboard/modules` returned the contracted module family:

- `play_draw_win_rate`
- `game1_postboard`
- `mulligan_opening_hand_outcomes`

With no analytics database in the disposable root, the modules honestly
reported missing/setup-needed state. This is acceptable degradation for
disposable empty-data smoke.

### Post-Fix Match Journal Evidence

The disposable-root Match Journal smoke used the contracted unattached note
path.

- `POST /api/journal/notes` returned HTTP 200.
- Request used `note_scope = "unattached"`.
- The synthetic note text began with
  `MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW`.
- Readback used `GET /api/journal/notes` by exact journal-owned note ID.
- Readback returned safe metadata only and did not return `note_text`.
- Disposable app-data artifacts were limited to `db/match_journal.sqlite3`.
- Analytics SQLite was not created by the Match Journal smoke.

### Post-Fix Live Player.log Evidence

Disposable-root Live Player.log status routes were exercised without reading a
real Player.log:

- `GET /api/live/player-log/status`: `missing`
- `GET /api/live/watcher/status`: `blocked_missing_log`
- `GET /api/live/watcher/process`: `blocked_missing_log`
- `GET /api/live/watcher/diagnostics`: `blocked`
- `GET /api/live/ingest/status`: `disabled`

The frontend rendered Live Player.log and diagnostics labels safely. This
report does not claim final Live Player.log supported readiness; the #275
private smoke requirement remains approval-gated and unrun.

### Post-Fix Error Report Preview Evidence

Synthetic safe preview request:

- `POST /api/feedback/error-report/preview` returned HTTP 200.
- Response status: `preview_ready`.
- `external_submission_enabled`: `false`.
- Diagnostic category count: 9.

Synthetic redaction probe:

- `POST /api/feedback/error-report/preview` returned HTTP 200.
- Response status: `preview_ready`.
- Raw synthetic private local path was absent from generated Markdown.
- `<redacted_local_path>` was present.
- Redaction summary reported one private path marker redacted from
  `actual_behavior`.

The previous privacy blocker was not reproduced at the current branch head.

### Post-Fix Optional Actual-Private-Root Evidence

Not run.

- `approval_scope: actual_app_data_readiness_status_only`: not approved.
- `approval_scope: actual_player_log_metadata_status_only`: not approved.
- `approval_scope: actual_match_journal_unattached_smoke_write`: not approved.

This remains acceptable degradation for the current disposable-root private
release smoke; it prevents stronger real-operator and Live Player.log supported
claims.

### Post-Fix Generated And Private Artifact Sweep

Cleanup evidence:

- Backend process stopped.
- Frontend dev process stopped.
- Backend port `8765` clear after cleanup.
- Frontend port `5178` clear after cleanup.
- Disposable app-data root removed.
- Temporary browser harness and temporary Chrome profile removed from `/tmp`.
- `frontend/dist` removed after build.
- Repo-local SQLite artifact sweep found no SQLite database or sidecar files.
- No generated/private/runtime repo artifact was produced by the rerun.

### Post-Fix Acceptable Degradation

The following degraded states were expected and acceptable:

- analytics database missing in disposable empty-data mode;
- local app config missing;
- Live Player.log path missing;
- watcher/process routes blocked because no configured Player.log was supplied;
- live SQLite capture disabled;
- dashboard modules rendering setup-needed / missing state;
- actual private app-data and Player.log checks unrun because approval was not
  granted;
- macOS smoke platform rather than Windows private-local-v1 operator platform;
- in-app Browser unavailable, with real browser fallback supplied by headless
  local Chrome.

### Post-Fix Residual Risks

- Actual private app-data readiness was not checked.
- Actual private Player.log metadata/status smoke was not checked.
- Windows private-local-v1 launch proof was not rerun in this pass.
- Browser smoke used headless local Chrome instead of the in-app Browser
  because the in-app Browser and Chrome extension surfaces were unavailable.
- A non-blocking favicon 404 remains visible in browser console output.

### Post-Fix Next Recommended Role

Codex E: Module Reviewer.

Review should verify the post-fix `ready_with_acceptable_degradation` verdict,
with special attention to the redaction probe, the fallback browser evidence,
the unrun actual-private scopes, and the preserved historical #285 blocker
record.

Pasteable Codex E prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer for issue #287, post-fix private-release end-to-end browser smoke rerun.

  Review:
  - docs/contracts/private_release_e2e_browser_integration_readiness.md
  - docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md

  Context:
  - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/285
  - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/286
  - Commit under test: f0b9cc94808dc09961be0e396e84b7a4ffdbaa6c
  - Target branch: codex/analytics-foundation

  Focus:
  - Verify the current `ready_with_acceptable_degradation` verdict.
  - Confirm the #286 redaction fix is reflected by focused tests and route-level probe evidence.
  - Confirm disposable-root backend/frontend/Match Journal/import/dashboard/Live Player.log smoke evidence is accurately summarized.
  - Confirm fallback headless Chrome browser evidence is acceptable given Browser/iab unavailability.
  - Confirm actual private app-data and actual Player.log scopes remain unrun and approval-gated.
  - Confirm no raw private paths, logs, payloads, SQLite contents, secrets, or generated/private artifacts are included.

  Do not:
  - Target main directly.
  - Close tracker #204, umbrella #207, tracker #202, or issue #287.
  - Read actual private app-data or Player.log without explicit approval.
  - Change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
  - Stage or commit unless explicitly asked.
```

### Post-Fix Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/287"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/285"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/286"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_match_journal_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_release_e2e_browser_integration_readiness.md"
  target_artifact: "docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md"
  verdict: "ready_with_acceptable_degradation"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  commit_under_test: "f0b9cc94808dc09961be0e396e84b7a4ffdbaa6c"
  validation:
    - "python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py - passed"
    - "python3 -m pytest -q tests/test_private_local_v1_setup.py - passed"
    - "python3 -m pytest -q tests/test_match_journal_cockpit_ui_backend.py tests/test_match_journal_status_api.py - passed"
    - "python3 -m pytest -q tests/test_analytics_browser_jsonl_upload.py tests/test_analytics_manual_jsonl_import.py - passed"
    - "python3 -m pytest -q tests/test_analytics_dynamic_decision_support_dashboard.py - passed"
    - "npm --prefix frontend ci - passed"
    - "npm --prefix frontend run typecheck - passed"
    - "npm --prefix frontend run test -- --run - passed"
    - "npm --prefix frontend run build - passed; frontend/dist removed"
    - "python3 -m ruff check src tests tools - passed"
    - "git diff --check - passed after report edit"
    - "python3 tools/check_agent_docs.py - passed"
    - "path-scoped secret/private marker scan - passed"
    - "path-scoped protected-surface gate - passed"
    - "generated/private artifact sweep - passed"
    - "disposable loopback backend/frontend browser smoke - completed with headless local Chrome fallback"
  stop_conditions:
    - "Do not claim production, public release, main, deploy, merge, parser truth, analytics truth, Live Player.log supported, AI, or coaching readiness."
    - "Do not run actual private app-data or Player.log checks without explicit user approval."
    - "Do not target main directly."
    - "Do not close tracker #204, umbrella #207, tracker #202, or issue #287."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```

## Codex D Fixer Addendum

Status: redaction blocker fixed in this branch pending Codex E module review.

Codex D reproduced the failing backend test, expanded the error-report preview
private-path redaction coverage for local temporary path roots, and added a
focused route-level regression for the macOS `/private/var/folders` path shape
cited by the blocker.

This addendum does not claim private release readiness. Actual private app-data
and actual private log checks remain unrun without explicit user approval. The
original Codex C report below remains historical evidence for the readiness pass
at commit `400b19a90169bf52f6ca5bc5af9566419f5fe3a6`.

Codex D validation:

- `python3 -m pytest -q tests/test_analytics_local_app_backend.py::test_error_report_preview_returns_sanitized_markdown_without_writes tests/test_analytics_local_app_backend.py::test_error_report_preview_redacts_macos_private_temp_path_shape`
  -> `2 passed`
- `python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py`
  -> `41 passed`
- `python3 -m pytest -q tests/test_private_local_v1_setup.py`
  -> `10 passed`
- `python3 -m ruff check src tests tools`
  -> passed
- `git diff --check`
  -> passed
- path-scoped secret/private marker scan for the current five-file artifact set
  -> passed
- path-scoped protected-surface scan for the current five-file artifact set
  -> passed
- generated SQLite/local database artifact sweep
  -> empty

Next recommended role: Codex E: Module Reviewer / contract-test confirmation.

## Role Performed

Codex C: Module Implementer / Readiness Executor.

This was a report-first readiness pass. No product code, parser code, analytics
schema, Match Journal semantics, CI, workbook, webhook, Apps Script, Google
Sheets, OpenAI/model-provider, or production behavior was changed.

## Source Issue And Trackers

- Issue #285 was verified open.
- Tracker #204 was verified open.
- Umbrella #207 was verified open.
- Match Journal tracker #202 was verified open and remains context only.

## Branch And Commit

The primary analytics worktree was dirty and stale with unrelated #203 files, so
this pass used a clean sibling worktree based on `origin/codex/analytics-foundation`.

- Head under test: `400b19a90169bf52f6ca5bc5af9566419f5fe3a6`
- `HEAD` matched `origin/codex/analytics-foundation`.
- Worktree branch used for the report pass:
  `codex/private-release-e2e-browser-contract`
- No staged files were created.

## Contract Used

- Source artifact:
  `docs/contracts/private_release_e2e_browser_integration_readiness.md`
- Target artifact:
  `docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md`

## Smoke Mode

Disposable local smoke only.

- Actual private app-data root checks: not run; no explicit approval was given.
- Actual private Player.log checks: not run; no explicit approval was given.
- Browser smoke: run with the Codex in-app browser against a loopback frontend.
- Backend and frontend were started on loopback only.
- Disposable app-data root was outside the repository and was removed after the
  smoke.

## Validation Matrix

| Command | Result | Evidence |
| --- | --- | --- |
| `python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py` | Failed | `39 passed, 1 failed`; failing test: `test_error_report_preview_returns_sanitized_markdown_without_writes`. |
| `python3 -m pytest -q tests/test_private_local_v1_setup.py` | Passed | `10 passed`. |
| `python3 -m pytest -q tests/test_match_journal_cockpit_ui_backend.py tests/test_match_journal_status_api.py` | Passed | `35 passed`. |
| `python3 -m pytest -q tests/test_analytics_browser_jsonl_upload.py tests/test_analytics_manual_jsonl_import.py` | Passed | `25 passed`. |
| `python3 -m pytest -q tests/test_analytics_dynamic_decision_support_dashboard.py` | Passed | `8 passed`. |
| `npm --prefix frontend ci` | Passed | 114 packages installed; 0 vulnerabilities reported. |
| `npm --prefix frontend run typecheck` | Passed | TypeScript completed without reported errors. |
| `npm --prefix frontend run test -- --run` | Passed | 3 test files passed; 75 tests passed. |
| `npm --prefix frontend run build` | Passed | Vite build completed; `frontend/dist` was removed afterward. |
| `python3 -m ruff check src tests tools` | Passed | Ruff reported no issues. |
| `git diff --check` | Passed | No whitespace errors in tracked diffs. |
| `git diff --no-index --check /dev/null docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md` | Passed | No whitespace warnings in the new untracked report artifact. |
| `python3 tools/check_agent_docs.py` | Passed | 30 files checked; 0 errors; 0 warnings. |

Dependency notes:

- Environment packages present for this smoke: FastAPI `0.136.3`, Uvicorn
  `0.49.0`, `python-multipart` `0.0.30`.
- Node `v24.14.0` and npm `11.9.0` were used for frontend commands.

Blocking validation detail:

- A focused redaction probe confirmed that the error-report preview Markdown
  can retain a user-supplied private local path value and does not include
  `<redacted_local_path>` for that input. The raw path value is intentionally
  omitted from this report.

## Backend Route Matrix

All routes below were exercised against the disposable loopback backend.

| Route | HTTP | Status | Schema/Object |
| --- | ---: | --- | --- |
| `GET /api/health` | 200 | `ok` | `mythic_edge_local_app_health` |
| `GET /api/app/setup-status` | 200 | `degraded` | `mythic_edge_local_app_setup_status` |
| `GET /api/app/config` | 200 | `missing` | `mythic_edge_local_app_config_status` |
| `GET /api/app/paths` | 200 | `degraded` | `mythic_edge_local_app_paths_status` |
| `GET /api/analytics/database/status` | 200 | `missing` | `mythic_edge_local_app_analytics_database_status` |
| `GET /api/analytics/dashboard/modules` | 200 | `missing` | `mythic_edge_local_app_analytics_dashboard_modules` |
| `GET /api/live/player-log/status` | 200 | `missing` | `mythic_edge_local_app_live_player_log_status` |
| `GET /api/live/watcher/status` | 200 | `blocked_missing_log` | `mythic_edge_local_app_live_watcher_status` |
| `GET /api/live/watcher/process` | 200 | `blocked_missing_log` | `mythic_edge_local_app_live_watcher_process_status` |
| `GET /api/live/watcher/diagnostics` | 200 | `blocked` | `mythic_edge_local_app_live_watcher_diagnostics` |
| `GET /api/live/ingest/status` | 200 | `disabled` | `mythic_edge_local_app_live_parser_sqlite_capture_status` |
| `GET /api/runtime/status` | 200 | `ok` | `mythic_edge_local_app_runtime_status` |

## Browser Smoke Matrix

The Codex in-app browser loaded the frontend at `http://127.0.0.1:5178/`
against the loopback backend.

| Browser observation | Result |
| --- | --- |
| Page title | `Mythic Edge Local Status` |
| `Mythic Edge Cockpit` heading | Present |
| Dashboard section | Present |
| Analytics / Review area | Present |
| Import section | Present |
| Match Journal section | Present |
| Setup/status content | Present |
| Live Player.log content | Present |
| Diagnostics content | Present |
| Error report surface | Present |
| Loopback API base evidence | Present |
| Console/runtime errors | No blocking app errors observed; Vite and React informational messages only. |

No screenshots were committed.

## Import/Data Recognition Evidence

The safer minimum import path was used.

- Manual import controls rendered in the browser smoke.
- `POST /api/imports/jsonl` with an empty request returned a sanitized
  rejected status with `source_path_required`.
- No analytics SQLite database was created by this import recognition smoke.
- No private JSON/JSONL file was read or copied.

## Analytics Dashboard Evidence

`GET /api/analytics/dashboard/modules` returned the contracted dashboard module
family:

- `play_draw_win_rate`
- `game1_postboard`
- `mulligan_opening_hand_outcomes`

With no analytics database in the disposable root, each module honestly reported
`missing` / setup-needed style state. The browser displayed descriptive local
analytics labels and did not present SQL text, hidden-card inference, best-line
ranking, player-mistake labels, archetype truth, Line Tracer truth, or
AI/coaching conclusions.

## Match Journal Evidence

The disposable-root Match Journal smoke used the contracted unattached note
path.

- `POST /api/journal/notes` returned HTTP 200.
- Request used `note_scope = "unattached"`.
- The synthetic note text began with
  `MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW`.
- Readback used `GET /api/journal/notes` by exact journal-owned note ID.
- Readback returned safe metadata only:
  `journal_note_id`, `note_scope`, author/source/privacy labels, timestamps,
  `smoke_marker_present`, and `attachment_status`.
- Readback did not return the note body.
- Disposable app-data artifacts were limited to `db/match_journal.sqlite3`.
- Analytics SQLite was not created by the Match Journal smoke.

Actual app-data-root Match Journal smoke was not run because no approval was
given for actual private app-data checks.

## Live Player.log Evidence

Disposable-root Live Player.log status routes were exercised without reading a
real Player.log:

- `GET /api/live/player-log/status`: `missing`
- `GET /api/live/watcher/status`: `blocked_missing_log`
- `GET /api/live/watcher/process`: `blocked_missing_log`
- `GET /api/live/watcher/diagnostics`: `blocked`
- `GET /api/live/ingest/status`: `disabled`

The frontend rendered Live Player.log and diagnostics labels safely. This report
does not claim final Live Player.log supported readiness; the #275 private smoke
requirement remains approval-gated and unrun.

## Error Report Preview Evidence

Synthetic safe preview request:

- `POST /api/feedback/error-report/preview` returned HTTP 200.
- Response status: `preview_ready`.
- `external_submission_enabled`: `false`.
- Diagnostic category count: 9.

Blocking privacy finding:

- Required backend validation failed in
  `test_error_report_preview_returns_sanitized_markdown_without_writes`.
- A direct sanitized probe confirmed that a user-entered private local path can
  remain in the generated Markdown preview and that the expected
  `<redacted_local_path>` marker is absent.
- The raw path value is intentionally omitted from this report.

This finding prevents a private-release-ready verdict.

## Optional Actual-Private-Root Evidence

Not run.

- `approval_scope: actual_app_data_readiness_status_only`: not approved.
- `approval_scope: actual_player_log_metadata_status_only`: not approved.
- `approval_scope: actual_match_journal_unattached_smoke_write`: not approved.

Because the disposable-root smoke found a privacy blocker, actual private-root
checks should remain deferred until the error-report preview redaction bug is
fixed and reviewed.

## Generated And Private Artifact Sweep

Cleanup evidence:

- Backend process stopped.
- Frontend dev process stopped.
- Backend port `8765` clear after cleanup.
- Frontend port `5178` clear after cleanup.
- Disposable app-data root removed.
- `frontend/dist` removed after build.
- Repo-local SQLite artifact sweep found no SQLite database or sidecar files.
- Git status before writing this report listed only the expected untracked
  contract artifact.

## Secret / Private Marker Status

Base changed-file secret/private marker scan before writing this report:

- Command: `python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation`
- Result: passed.
- Scanned paths: 0 tracked changed paths at that point.

Path-scoped scans for the final report and contract should be run after this
artifact is written; final path-scoped scan evidence is listed below.

Final path-scoped scan:

- Command:
  `printf '%s\n' docs/contracts/private_release_e2e_browser_integration_readiness.md docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin`
- Result: passed.
- Scanned paths: 2.
- Forbidden: 0.
- Warnings: 0.

## Protected-Surface Status

Base protected-surface scan before writing this report:

- Command: `python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation`
- Result: passed.
- Changed paths: 0 tracked changed paths at that point.

Path-scoped scans for the final report and contract should be run after this
artifact is written; final path-scoped scan evidence is listed below.

Final path-scoped scan:

- Command:
  `printf '%s\n' docs/contracts/private_release_e2e_browser_integration_readiness.md docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin`
- Result: passed.
- Changed paths: 2.
- Forbidden: 0.
- Warnings: 0.

## Acceptable Degradation

The following degraded states were expected and acceptable under disposable
empty-data smoke mode:

- analytics database missing;
- local app config missing;
- Live Player.log path missing;
- watcher/process routes blocked because no configured Player.log was supplied;
- live SQLite capture disabled;
- dashboard modules rendering setup-needed / missing state;
- no actual private app-data or Player.log checks because approval was not
  requested or granted.

These degradations are not the blocker.

## Residual Risks

- Privacy blocker: error-report preview redaction is unsafe for private release
  until fixed and reviewed.
- Required backend/local app validation does not fully pass.
- This smoke ran on Darwin, not the Windows private-local-v1 operator platform.
- Actual private app-data and actual Player.log metadata smokes were not run.
- Browser evidence was from a disposable empty-data mode, not a real operator
  app-data root.
- Path-scoped safety scans for this final report and contract passed after the
  file was written.

## Explicit Non-Claims

This report does not claim:

- production readiness;
- public release readiness;
- main branch readiness;
- merge readiness;
- deploy readiness;
- parser truth verification;
- analytics truth verification;
- Match Journal truth verification;
- Live Player.log supported readiness;
- hidden-card inference;
- archetype classification;
- gameplay advice;
- player-mistake labels;
- AI readiness or coaching readiness.

## Next Recommended Role

Codex E: Module Reviewer.

Review should focus first on the privacy blocker in
`test_error_report_preview_returns_sanitized_markdown_without_writes` and the
direct probe result that a private local path can remain in generated preview
Markdown. If Codex E confirms the finding, route to a narrow Codex C/D fix for
error-report path redaction before any private-root smoke or private-release
readiness claim.

Pasteable Codex E prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer for issue #285, private-release end-to-end browser smoke and integration readiness.

  Review:
  - docs/contracts/private_release_e2e_browser_integration_readiness.md
  - docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md

  Branch/context:
  - Target branch: codex/analytics-foundation
  - Commit under test: 400b19a90169bf52f6ca5bc5af9566419f5fe3a6
  - Clean sibling worktree was used because the primary analytics worktree had unrelated #203 changes.

  Focus:
  - Verify the report's `not_ready_privacy_blocked` verdict.
  - Review the failed backend validation:
    `python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py`
  - Confirm whether the error-report preview path-redaction finding should route to a narrow fix before any private-root smoke.
  - Confirm browser/backend/Match Journal/import/dashboard/Live Player.log disposable-root evidence is accurately summarized.
  - Confirm no raw private paths, logs, payloads, SQLite contents, secrets, or generated/private artifacts are included.

  Do not:
  - Target main directly.
  - Close tracker #204, umbrella #207, tracker #202, or issue #285.
  - Claim private release readiness while the privacy blocker remains.
  - Read actual private app-data or Player.log without explicit approval.
  - Change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
  - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/285"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_match_journal_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_release_e2e_browser_integration_readiness.md"
  target_artifact: "docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md"
  verdict: "not_ready_privacy_blocked"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/285"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_match_journal_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_release_e2e_browser_integration_readiness.md"
  target_artifact: "docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md"
  verdict: "not_ready_privacy_blocked"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  commit_under_test: "400b19a90169bf52f6ca5bc5af9566419f5fe3a6"
  validation:
    - "python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py - failed: error-report preview path redaction"
    - "python3 -m pytest -q tests/test_private_local_v1_setup.py - passed"
    - "python3 -m pytest -q tests/test_match_journal_cockpit_ui_backend.py tests/test_match_journal_status_api.py - passed"
    - "python3 -m pytest -q tests/test_analytics_browser_jsonl_upload.py tests/test_analytics_manual_jsonl_import.py - passed"
    - "python3 -m pytest -q tests/test_analytics_dynamic_decision_support_dashboard.py - passed"
    - "npm --prefix frontend ci - passed"
    - "npm --prefix frontend run typecheck - passed"
    - "npm --prefix frontend run test -- --run - passed"
    - "npm --prefix frontend run build - passed; frontend/dist removed"
    - "python3 -m ruff check src tests tools - passed"
    - "git diff --check - passed"
    - "git diff --no-index --check /dev/null docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md - passed"
    - "python3 tools/check_agent_docs.py - passed"
    - "path-scoped secret/private marker scan - passed"
    - "path-scoped protected-surface gate - passed"
    - "disposable loopback backend/frontend browser smoke - completed"
  stop_conditions:
    - "Do not claim private release readiness until error-report preview redaction is fixed and reviewed."
    - "Do not run actual private app-data or Player.log checks without explicit user approval."
    - "Do not target main directly."
    - "Do not close tracker #204, umbrella #207, tracker #202, or issue #285."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
