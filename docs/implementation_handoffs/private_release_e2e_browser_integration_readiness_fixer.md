# Private Release E2E Browser Integration Readiness Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/285

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Related Match Journal tracker: https://github.com/Tahjali11/Mythic-Edge/issues/202

## Contract

`docs/contracts/private_release_e2e_browser_integration_readiness.md`

## Source Finding

Codex E confirmed a privacy blocker in
`docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md`:
error-report preview Markdown did not redact a reproduced private local temp
path shape, and the focused backend test failed at
`tests/test_analytics_local_app_backend.py::test_error_report_preview_returns_sanitized_markdown_without_writes`.

Fault category: implementation gap in local path redaction coverage.

## Required Governance

- `docs/agent_constitution.md`
- `docs/agent_threads/module_fixer.md`

## Internal Project Area

Private release readiness evidence for the local app, limited to sanitized
error-report preview behavior.

## Truth Owner

The local app error-report preview owns sanitized triage Markdown composition.
Parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching
and production layers remain unchanged and retain their existing truth
boundaries.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex D: Module Fixer.

## What Changed

Expanded the existing private-path redaction pattern to treat common local
temporary roots as private paths:

- `/private/var/...`
- `/var/folders/...`
- `/tmp/...`
- `/private/tmp/...`
- `/var/tmp/...`

The existing Windows-drive and user-home directory behavior is preserved.
No error-report response schema, route, payload field, diagnostic category,
external submission behavior, app-data read behavior, or file-write behavior was
changed.

## Files Changed

- `src/mythic_edge_parser/local_app/error_reports.py`
- `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/private_release_e2e_browser_integration_readiness_fixer.md`
- `docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md`

Existing Codex B/C artifacts remain in the working tree and were preserved:

- `docs/contracts/private_release_e2e_browser_integration_readiness.md`
- `docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md`

## Code Changed

Yes. Local app support code changed only in
`src/mythic_edge_parser/local_app/error_reports.py`.

## Tests Added Or Updated

Updated `tests/test_analytics_local_app_backend.py`:

- the previously failing sanitized-preview test now passes on the local
  disposable temp root;
- added a focused route-level regression for the macOS `/private/var/folders`
  path shape cited by the blocker.

## Interface Changes

None.

No workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior,
parser behavior, runtime status schema, environment variable contract, route
schema, route path, response payload field, frontend contract, or private-release
readiness vocabulary was changed.

## Contracted Area Status

The fix stayed inside the contracted local-app error-report preview privacy
boundary. It does not claim private release readiness. Actual private app-data
and actual private log checks remain unrun because explicit approval was not
given.

## Validation Run

```bash
python3 -m pytest -q tests/test_analytics_local_app_backend.py::test_error_report_preview_returns_sanitized_markdown_without_writes tests/test_analytics_local_app_backend.py::test_error_report_preview_redacts_macos_private_temp_path_shape
python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py
python3 -m pytest -q tests/test_private_local_v1_setup.py
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
find . -path ./.git -prune -o -name '*.sqlite' -print -o -name '*.sqlite3' -print -o -name '*.db' -print -o -name '*.sqlite-wal' -print -o -name '*.sqlite-shm' -print -o -name '*.sqlite-journal' -print
```

Results:

- Focused redaction tests: `2 passed`.
- Backend/config tests: `41 passed`.
- Private local setup adjacency: `10 passed`.
- Ruff: passed.
- `git diff --check`: passed.
- Path-scoped secret/private marker scan for the current five-file artifact set:
  passed.
- Path-scoped protected-surface scan for the current five-file artifact set:
  passed.
- Generated SQLite/local database artifact sweep: empty.

## Still Unverified

- Actual private app-data root checks were not run.
- Actual private log checks were not run.
- Browser smoke was not rerun after the code fix.
- Full private-release readiness is not claimed.

## Reviewer Focus

Codex E should verify:

- the new redaction roots are appropriate for disposable/local temp private
  path shapes;
- no raw local path can remain in the sanitized preview for the reproduced
  blocker;
- no payload shape, route, diagnostics category, external submission behavior,
  parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching,
  or production behavior changed;
- private-release readiness remains blocked pending review and any explicitly
  approved private-root smoke.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test confirmation.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #285, private-release end-to-end browser integration readiness.

Review the Codex D fixer pass for the confirmed privacy blocker:
- docs/contracts/private_release_e2e_browser_integration_readiness.md
- docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md
- docs/implementation_handoffs/private_release_e2e_browser_integration_readiness_fixer.md
- src/mythic_edge_parser/local_app/error_reports.py
- tests/test_analytics_local_app_backend.py

Branch:
codex/private-release-e2e-browser-contract

Base:
codex/analytics-foundation

Finding under review:
Error-report preview Markdown previously retained a reproduced private local temp path shape and omitted <redacted_local_path>.

Confirm:
- the focused redaction blocker is fixed;
- no raw local path remains in preview JSON/Markdown for the reproduced shape;
- no error-report payload shape, route, diagnostics category, external submission behavior, file-write behavior, or private-root read behavior changed;
- no parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed;
- private-release readiness is not claimed before review and any explicitly approved private-root smoke.

Suggested validation:
- python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py
- python3 -m pytest -q tests/test_private_local_v1_setup.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped secret/private marker scan for the changed files
- path-scoped protected-surface scan for the changed files

Do not:
- run actual private app-data or private log checks without explicit user approval;
- target main directly;
- close tracker #204, umbrella #207, tracker #202, or issue #285;
- claim private release readiness before the redaction fix is reviewed.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/285"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_match_journal_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md"
  target_artifact: "docs/implementation_handoffs/private_release_e2e_browser_integration_readiness_fixer.md"
  verdict: "redaction_blocker_fixed_pending_module_review"
  risk_tier: "High"
  branch: "codex/private-release-e2e-browser-contract"
  base_branch: "codex/analytics-foundation"
  validation:
    - "python3 -m pytest -q tests/test_analytics_local_app_backend.py::test_error_report_preview_returns_sanitized_markdown_without_writes tests/test_analytics_local_app_backend.py::test_error_report_preview_redacts_macos_private_temp_path_shape - 2 passed"
    - "python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py - 41 passed"
    - "python3 -m pytest -q tests/test_private_local_v1_setup.py - 10 passed"
    - "python3 -m ruff check src tests tools - passed"
    - "git diff --check - passed"
    - "path-scoped secret/private marker scan for current five-file artifact set - passed"
    - "path-scoped protected-surface scan for current five-file artifact set - passed"
    - "generated SQLite/local database artifact sweep - empty"
  stop_conditions:
    - "Do not claim private release readiness until the redaction gap is fixed and reviewed."
    - "Do not run actual private app-data or private log checks without explicit user approval."
    - "Do not target main directly."
    - "Do not close tracker #204, umbrella #207, tracker #202, or issue #285."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
