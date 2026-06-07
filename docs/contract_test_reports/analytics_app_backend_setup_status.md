# Analytics App Backend Setup-Status Contract-Test Report

report_lifecycle: followup_after_fixer
finding_lifecycle: fixed_state_followup

## Findings

No blocking findings remain after the Codex D fixer pass.

### issue-208-p1-unsafe-config-field-names

- severity: P1
- finding_lifecycle: fixed_state_followup
- finding_status: fixed
- blocking_status: not_blocking
- original_evidence: unsafe unexpected config field names could be echoed by `GET /api/app/config`.
- verification_evidence: `src/mythic_edge_parser/local_app/config.py:148` now defines `_is_safe_unexpected_field_name(...)`; focused tests pass; a direct route probe confirmed safe labels are retained while URL-shaped, path-shaped, secret-like names and unsafe values are absent from the response.
- next_route: F

Original context preserved: `docs/contracts/analytics_app_backend_setup_status.md:647` allows unexpected config fields to be reported by name only when the names are safe labels, and `docs/contracts/analytics_app_backend_setup_status.md:914` requires route responses to avoid temp roots, real home paths, raw log text, secrets, and webhook-like strings. The initial review found that `src/mythic_edge_parser/local_app/config.py` treated every non-allowed, non-secret-like string key as safe and exposed that through `src/mythic_edge_parser/local_app/backend.py`.

Codex D added a safe-label predicate and coverage in `tests/test_analytics_local_app_config.py:86` to `tests/test_analytics_local_app_config.py:135` and `tests/test_analytics_local_app_backend.py:106` to `tests/test_analytics_local_app_backend.py:137`. Benign names such as `safe_extra` remain visible. URL-shaped, path-shaped, secret-like, non-string, and otherwise unsafe unexpected names are counted/redacted and are not returned in route payloads. Config values remain redacted.

### issue-208-p2-branch-sync-risk

- severity: P2
- finding_lifecycle: remaining_non_blocking
- finding_status: unresolved
- blocking_status: non_blocking_for_review
- original_evidence: branch was ahead 1 and behind 1 relative to `origin/codex/analytics-foundation`.
- verification_evidence: rechecked during confirmation; branch still reports `1 1`.
- next_route: F

This is not an implementation mismatch, but it is a submitter/integration risk. Codex F should not stage, push, or open/update a PR until the branch state is reconciled or explicitly reported as blocked.

## Issue And Scope

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/208>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Branch: `codex/analytics-foundation`
- Contract: `docs/contracts/analytics_app_backend_setup_status.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/analytics_app_backend_setup_status_fixer.md`

## Contract Matches

- The implementation remains limited to the local app backend setup-status package, tests, dependency metadata, and handoff/report artifacts.
- FastAPI remains an optional `app` dependency rather than a core parser runtime dependency.
- `httpx` remains dev/test support for FastAPI test-client coverage.
- The implemented endpoints are GET-only setup/status surfaces.
- The reviewed GET endpoints do not start parser/runtime behavior.
- Benign unexpected config field names remain visible as safe labels.
- URL-shaped, path-shaped, secret-like, non-string, and otherwise unsafe unexpected config field names are not returned in route payloads.
- Config values remain redacted.
- Missing database status does not create a SQLite database file.
- Existing database status opens the database read-only for metadata inspection.
- Migration status uses source-controlled migration discovery and does not apply migrations.
- Runtime-control-like behavior is reported as deferred.
- Wildcard CORS was not introduced.
- Referenced parser/runtime/workbook/webhook/App Script modules were not edited in this package.
- Path-scoped protected-surface and secret/private-marker checks over the reviewed package passed.
- No generated SQLite database, journal, WAL, SHM, runtime, retry-payload, or workbook-export artifact was detected as changed or untracked.

## Contract Mismatches

None remaining after the Codex D fixer pass.

## Missing Tests Or Safeguards

None remaining for the original P1. The fixer added helper-level and route-level coverage for unsafe unexpected config field names.

Residual note: `secret_like_field_count` now conservatively counts all redacted unsafe unexpected field names, not only secret-pattern names. This is acceptable for this first setup-status slice because the contract has no separate `redacted_unexpected_field_count` response field and the safer behavior is to redact without expanding the payload contract. A future contract may split those counts if UI copy needs sharper semantics.

## Validation Run

- `git fetch --prune` -> passed.
- `git status --short --branch` -> branch is `codex/analytics-foundation`, with unrelated dirty/untracked work present and branch relation `[ahead 1, behind 1]`.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` -> `1 1`.
- FastAPI/httpx import check -> `fastapi 0.136.3`, `httpx 0.28.1`.
- `py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py` -> 18 passed, 1 third-party deprecation warning.
- `py -m pytest -q tests\test_status_api.py tests\test_app_config.py tests\test_analytics_migration_loader.py tests\test_analytics_schema.py` -> 35 passed.
- `py -m ruff check src tests tools` -> passed.
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0.
- `git diff --check` -> passed.
- Path-scoped protected-surface check over the reviewed package and this report -> forbidden 0, warnings 0, passed.
- Path-scoped secret/private-marker check over the reviewed package and this report -> forbidden 0, warnings 0, passed.
- Generated SQLite/runtime artifact status check -> no changed or untracked database or runtime artifacts found.
- Direct route probe for `/api/app/config` -> `safe_extra` remained visible; unsafe URL-shaped, path-shaped, and secret-like names were absent; unsafe values were absent.

## FastAPI And Httpx Environment Status

FastAPI and httpx are installed in the local environment and import successfully at the versions recorded above. The dependency decision matches the contract: FastAPI is optional app support, and httpx is dev/test support.

## Branch Sync Risk

The branch is ahead 1 and behind 1 relative to `origin/codex/analytics-foundation`. This should be handled before Codex F submitter work.

## Protected-Surface Status

No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal behavior, OpenAI/AI runtime behavior, or production behavior change was found in the reviewed package.

## Secret And Private-Marker Status

The path-scoped scanner passed for the reviewed package. The follow-up manual route probe confirms the application-level redaction bug is fixed. No actual private value is recorded in this report.

## Generated Artifact Status

No generated SQLite database file, journal, WAL, SHM, runtime artifact, retry payload, workbook export, raw log, or generated data file was detected as changed or untracked in the reviewed artifact status check.

## Forbidden Scope

Forbidden scope was not touched.

## Verdict

Ready for Codex F with branch-sync caution. Codex F should stage only the issue #208 package, preserve unrelated dirty/untracked files, and handle or explicitly report the ahead/behind branch state before any push or PR work.

## Next Recommended Role

Codex F: Module Submitter.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #208 on branch codex/analytics-foundation.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/208

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Contract:
docs/contracts/analytics_app_backend_setup_status.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md

Fixer handoff:
docs/implementation_handoffs/analytics_app_backend_setup_status_fixer.md

Review artifact:
docs/contract_test_reports/analytics_app_backend_setup_status.md

Goal:
Submit the reviewed issue #208 local app backend setup-status package only if branch sync and intended-file staging are safe.

Before staging:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated dirty/untracked files.
- Recheck HEAD...origin/codex/analytics-foundation. The last Codex E review saw 1 1.
- Do not stage unrelated quality Pyright evidence-ledger files or unrelated contracts/handoffs.
- Do not target main unless explicitly approved.

Intended issue #208 files include:
- pyproject.toml
- docs/contracts/analytics_app_backend_setup_status.md
- docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md
- docs/implementation_handoffs/analytics_app_backend_setup_status_fixer.md
- docs/contract_test_reports/analytics_app_backend_setup_status.md
- src/mythic_edge_parser/local_app/__init__.py
- src/mythic_edge_parser/local_app/paths.py
- src/mythic_edge_parser/local_app/config.py
- src/mythic_edge_parser/local_app/setup_status.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_local_app_config.py
- tests/test_analytics_local_app_backend.py

Also inspect whether docs/contracts/analytics_local_developer_app_shell.md belongs to this same issue package or should remain unstaged as a source/umbrella artifact.

Run:
git status --short --branch
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_status_api.py tests\test_app_config.py tests\test_analytics_migration_loader.py tests\test_analytics_schema.py
py -m ruff check src tests tools
git diff --check

Also rerun path-scoped protected-surface and secret/private-marker checks over the issue #208 package.

If safe, stage only reviewed issue #208 files, commit, push, and open or update the appropriate draft PR against the approved integration target. If branch sync blocks safe submission, stop and report the exact branch-sync state rather than forcing a push.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/208"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_app_backend_setup_status.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_app_backend_setup_status_fixer.md"
  review_artifact: "docs/contract_test_reports/analytics_app_backend_setup_status.md"
  findings:
    - severity: "P1"
      status: "fixed_state_followup"
      summary: "Unsafe unexpected config field names are no longer echoed by GET /api/app/config."
    - severity: "P2"
      status: "remaining_non_blocking"
      summary: "Branch is ahead 1 and behind 1 relative to origin/codex/analytics-foundation."
  validation:
    - "FastAPI/httpx import check -> fastapi 0.136.3, httpx 0.28.1"
    - "focused local app backend tests -> 18 passed, 1 third-party deprecation warning"
    - "adjacent status/config/migration/schema tests -> 35 passed"
    - "ruff -> passed"
    - "agent docs check -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "direct route probe -> safe label retained; unsafe keys and values redacted"
    - "generated SQLite/runtime artifact status -> clean"
  forbidden_scope_touched: false
  branch_sync_risk: "HEAD...origin/codex/analytics-foundation is 1 1"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
```
