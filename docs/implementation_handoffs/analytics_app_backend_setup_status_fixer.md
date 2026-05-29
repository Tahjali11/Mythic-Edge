# Analytics App Backend Setup-Status Fixer Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/208>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Contract

`docs/contracts/analytics_app_backend_setup_status.md`

## Review Artifact

`docs/contract_test_reports/analytics_app_backend_setup_status.md`

## Implementation Handoff Used

`docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md`

## Role Performed

Codex D: Module Fixer.

## Branch

`codex/analytics-foundation`

Branch relation observed before and after this fixer pass:

```text
HEAD...origin/codex/analytics-foundation -> 1 1
```

This branch-sync risk was noted and not resolved.

## Finding Fixed

P1: unsafe unexpected config field names could be echoed by `GET /api/app/config`.

Fault category: implementation redaction gap in the local app config status surface.

## What Changed

Added an explicit safe-label predicate for unexpected config field names. Benign labels such as `safe_extra` remain visible in `unexpected_fields`, while URL-shaped, path-shaped, secret-like, non-string, and otherwise unsafe names are counted/redacted and are not returned in route payloads. Config values remain redacted.

## Files Changed By This Fixer Pass

- `src/mythic_edge_parser/local_app/config.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/analytics_app_backend_setup_status_fixer.md`

Existing dirty or untracked files from the broader branch package were preserved and not staged.

## Code Changed

Runtime code changed: yes, limited to `src/mythic_edge_parser/local_app/config.py`.

Behavior surface:

- added `_SAFE_UNEXPECTED_FIELD_RE`
- added `_is_safe_unexpected_field_name(...)`
- changed unexpected config field classification so only safe labels are echoed
- kept the existing `secret_like_field_count` response field as the count of redacted unsafe unexpected field names

No parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/production behavior changed.

## Tests Added Or Updated

`tests/test_analytics_local_app_config.py`:

- added helper coverage proving `safe_extra` is visible and URL-shaped, path-shaped, secret-like, unsafe-space, non-string, and `None` names are unsafe
- added config-status coverage proving unsafe unexpected names and their values are not echoed

`tests/test_analytics_local_app_backend.py`:

- added route coverage proving `/api/app/config` does not expose unsafe unexpected field names
- added route coverage proving setup-status GET routes do not create app folders, databases, migrations, runtime artifacts, or generated files

## Interface Changes

None.

No route names, payload field names, config field names, workbook columns, webhook payload fields, environment variable contracts, parser interfaces, or production entrypoints changed.

## Validation Run

```powershell
git status --short --branch
# codex/analytics-foundation...origin/codex/analytics-foundation [ahead 1, behind 1]

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
# 1 1

py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
# before fix: failed on missing safe-label predicate
# after fix: 18 passed, 1 third-party FastAPI/Starlette deprecation warning

py -m pytest -q tests\test_status_api.py tests\test_app_config.py tests\test_analytics_migration_loader.py tests\test_analytics_schema.py
# 35 passed

py -m ruff check src tests tools
# passed

git diff --check
# passed

py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, changed_paths 10, forbidden 0, warnings 0

py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, scanned_paths 10, forbidden 0, warnings 0

py tools\check_agent_docs.py
# passed, errors 0, warnings 0
```

Generated artifact check:

- no `.sqlite`, `.sqlite3`, `.db`, journal, WAL, or SHM artifacts were found
- no app-data folders or generated files were created by the new GET-route test

## Protected-Surface Status

No forbidden protected surfaces were touched.

No changes were made to parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, Match Journal behavior, OpenAI/AI behavior, production behavior, secrets, environment variables, raw logs, generated data, runtime status files, retry payloads, workbook exports, or generated SQLite files.

## Secret / Private-Marker Status

The fix prevents unsafe unexpected field names from being returned in config route payloads. Values remain redacted.

The path-scoped scan over the issue #208 package passed with forbidden `0` and warnings `0`.

## Still Unverified

- Full repository test suite was not run.
- Branch sync remains unresolved: local branch is ahead 1 and behind 1 relative to `origin/codex/analytics-foundation`.
- Codex E should confirm that reusing `secret_like_field_count` for all redacted unsafe unexpected field names is acceptable under the current payload contract.

## Reviewer Focus

Codex E should verify:

- `safe_extra` and similar safe labels remain visible in `unexpected_fields`
- URL-shaped and path-shaped unexpected names are not echoed
- secret-like names remain counted/redacted
- route payloads from `/api/app/config` do not expose unsafe field names or values
- GET routes remain read-only and do not create local app folders, databases, migrations, parser/runtime behavior, or generated artifacts
- branch-sync risk is preserved for Codex F/G rather than resolved here

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #208.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/208

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_backend_setup_status.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md

Prior review artifact:
docs/contract_test_reports/analytics_app_backend_setup_status.md

Fixer handoff:
docs/implementation_handoffs/analytics_app_backend_setup_status_fixer.md

Review only the Codex D fix for the P1 finding:
- unsafe unexpected config field names could be echoed by GET /api/app/config.

Confirm:
- benign unexpected names such as safe_extra remain visible as safe labels;
- URL-shaped, path-shaped, secret-like, non-string, and otherwise unsafe names are counted/redacted and not returned in route payloads;
- config values remain redacted;
- allowed config-field behavior is preserved;
- setup-status GET routes remain read-only and create no local app folders, databases, migrations, runtime artifacts, or generated data;
- no parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/production behavior changed;
- branch sync remains unresolved and should not be handled until submitter/integration work.

Run:
git status --short --branch
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_status_api.py tests\test_app_config.py tests\test_analytics_migration_loader.py tests\test_analytics_schema.py
py -m ruff check src tests tools
git diff --check

Also run path-scoped protected-surface and secret/private-marker checks over the issue #208 package.

Route to Codex F only if the P1 is resolved and no new blocking findings remain.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/208"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_app_backend_setup_status.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_app_backend_setup_status.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_app_backend_setup_status_fixer.md"
  finding_fixed:
    - severity: "P1"
      summary: "Unsafe unexpected config field names can be echoed by GET /api/app/config."
  validation:
    - "git status --short --branch -> codex/analytics-foundation [ahead 1, behind 1]"
    - "git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 1 1"
    - "focused local app tests -> 18 passed, 1 third-party deprecation warning"
    - "adjacent status/config/migration/schema tests -> 35 passed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "agent docs check -> errors 0, warnings 0"
    - "generated artifact check -> no SQLite DB/journal/WAL/SHM artifacts found"
  forbidden_scope_touched: false
  branch_sync_risk: "HEAD...origin/codex/analytics-foundation is 1 1; not resolved by Codex D"
  next_thread: "E"
  next_role: "Codex E confirmation thread"
```
