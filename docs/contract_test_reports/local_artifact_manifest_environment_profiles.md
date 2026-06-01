# Contract Test Report: Local Artifact Manifest And Environment Profiles

## Findings

No blocking findings remain.

### CT-153-001 P1: `.env*` secret-surface checks only inspected `.env.local`, so real `.env` files could be missed

Status: fixed.

Original evidence: `docs/local_artifacts_manifest.json` declares `env_files`
as `path_pattern: ".env*"` with `present_severity: "blocked"`, but the first
review found that `tools/check_local_environment.py` checked only `.env.local`.
A temporary Git repo containing `.env` was reported as `missing_not_ignored`
with "No local artifact is present."

Verification evidence: after the Codex D fix, the checker handles `.env*` as a
narrow repo-root metadata-only glob. A direct probe with a temporary Git repo
containing `.env` now reports:

```json
{
  "artifact_id": "env_files",
  "display_path": "<repo>\\.env*",
  "observed": "present_not_ignored",
  "severity": "blocked",
  "contents_read": false,
  "path_echoed": false
}
```

Focused tests now cover `.env`, `.env.local`, and `.env.production` without
printing values.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/153

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/227

## Tracker

N/A

## Contract

`docs/contracts/local_artifact_manifest_environment_profiles.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed files reviewed:

- `docs/contracts/local_artifact_manifest_environment_profiles.md`
- `docs/local_artifacts_manifest.json`
- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- `docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md`
- `docs/contract_test_reports/local_artifact_manifest_environment_profiles.md`

Governance artifacts used:

- `AGENTS.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

## Contract Summary

The implementation must add a source-controlled local artifact manifest and a
report-only local environment checker. The checker must classify repo-owned,
generated, private, local-only, and secret-adjacent artifacts across required
profiles without reading private payloads, printing raw paths or values,
creating local state, becoming a CI gate, implementing issue #227 checkout
retirement behavior, or changing parser/runtime/analytics/local app/workbook/
webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

## Internal Project Area Reviewed

Quality / Governance, with shared-support relevance to Generated / Local
Artifacts, Local App / UI, Analytics, and parser runtime readiness.

## Bridge-Code Status Reviewed

`shared_support`. The checker is a reporting surface only. It does not own
parser truth, analytics truth, local app runtime behavior, setup authority,
cleanup authority, or deployment readiness.

## Checks Run

```bash
git status --short --branch
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
py -m pytest -q tests\test_check_local_environment.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_manual_jsonl_import.py
py -m ruff check tools tests src
git diff --check
py tools\check_agent_docs.py
```

Path-scoped protected-surface and secret/private-marker scans were run over the
contract, manifest, checker, focused tests, handoff, and this report.

Additional verification probe:

- Created a temporary Git repo containing `.env`.
- Loaded the real manifest and built a `clean_clone` report.
- Verified `env_files` reports `present_not_ignored`, `severity: blocked`,
  symbolic display path `<repo>\.env*`, `contents_read: false`, and
  `path_echoed: false`.

## Results

Approve for Codex F.

Validation results:

- `py -m pytest -q tests\test_check_local_environment.py` -> 15 passed
- `py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py` -> 76 passed, 1 skipped
- `py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_manual_jsonl_import.py` -> 35 passed, 1 third-party warning
- `py -m ruff check tools tests src` -> passed
- `git diff --check` -> passed
- `py tools\check_agent_docs.py` -> passed
- Path-scoped protected-surface scan -> passed, forbidden 0, warnings 0
- Path-scoped secret/private-marker scan -> warning result, forbidden 0,
  warnings from manifest placeholder artifact references
- Generated/private artifact status check -> no SQLite DB/WAL/SHM/journal,
  local artifact, frontend build, raw log, runtime, failed-post, or workbook-
  export artifacts were created or changed

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-153-001 | P1 | `fixed_state_followup` | fixed | not_blocking | Manifest declares `env_files` as `.env*` and blocked when present; first review found the checker only inspected `.env.local`, so `.env` could be missed. | Temporary Git repo probe with `.env` now returns `observed: present_not_ignored`, `severity: blocked`, symbolic `<repo>\.env*`, `contents_read: false`, and `path_echoed: false`; focused tests cover `.env`, `.env.local`, and `.env.production`. | F |

## Confirmed Contract Matches

- The manifest exists at `docs/local_artifacts_manifest.json` and uses
  `schema_version: local_artifacts_manifest.v1`.
- Required profiles are present: `clean_clone`, `local_developer_app`,
  `analytics_development`, `live_parser_readiness`, and
  `historical_import_readiness`.
- PR #65 compatibility aliases map `live_parser` to
  `live_parser_readiness` and `analytics_dev` to `analytics_development`.
- Required artifact classifications are present.
- The checker supports the contracted report-only CLI profiles and optional
  path arguments.
- Unknown profile and malformed manifest return exit code `2`.
- Generated reports, including blocked readiness reports, return exit code `0`.
- Repo-local `.env*` secret-adjacent files are detected as present local state
  without reading or printing values.
- User-supplied private file paths are inspected only by metadata and are not
  echoed in JSON or text output.
- Environment variable values are not printed.
- Private file contents are not read in the covered tests.
- The checker does not create app-data folders or SQLite files in the covered
  tests.
- Existing protected-surface and secret/private-marker tooling behavior was not
  modified.
- Existing local app setup/status/import behavior was not modified.
- Issue #227 clean-install and checkout-retirement behavior was not
  implemented.
- No parser/runtime/analytics schema or ingest/local app runtime/workbook/
  webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changes were
  found.

## Contract Mismatches

- None remaining.

## Missing Tests

- No blocking missing tests found.
- Remaining non-blocking gap: live operator machines with real local artifact
  layouts were not tested; tests use synthetic temp directories only.

## Drift Notes

- Branch drift: `HEAD...origin/codex/analytics-foundation` was `0 0` during
  review.
- Issue lifecycle drift: issue #153 and related issue #227 remain open. This
  report does not authorize closure.
- Local-data drift: no generated/private/local artifacts were created or
  changed by validation.
- Repo drift: all-repo secret/private-marker advisory findings remain
  pre-existing outside this module.
- No workbook, deployment, parser behavior, analytics schema, local-app runtime,
  CI-gate, or production drift was identified.

## Recommendation

approve

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #153.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/153

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/227

Branch:
codex/analytics-foundation

Contract:
docs/contracts/local_artifact_manifest_environment_profiles.md

Implementation handoff:
docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md

Review artifact:
docs/contract_test_reports/local_artifact_manifest_environment_profiles.md

Task:
Submit the reviewed #153 local artifact manifest and environment profile checker package. Inspect git status, confirm branch sync, stage only the intended #153 files, commit with a concise message, push codex/analytics-foundation, and open or update the draft PR toward the correct non-production integration target. Do not target main, merge, close issue #153, close issue #227, or change production behavior unless explicitly approved.

Reviewed files expected:
- docs/contracts/local_artifact_manifest_environment_profiles.md
- docs/local_artifacts_manifest.json
- tools/check_local_environment.py
- tests/test_check_local_environment.py
- docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md
- docs/contract_test_reports/local_artifact_manifest_environment_profiles.md

Validation already confirmed by Codex E:
- focused checker tests passed
- secret/protected checker tests passed with one platform skip
- adjacent local app/import tests passed with one existing third-party warning
- Ruff passed
- git diff --check passed
- agent docs check passed
- path-scoped protected-surface scan passed
- path-scoped secret/private-marker scan had no forbidden findings and only expected manifest placeholder warnings
- generated/private artifact status check found no generated/private/local artifacts created or changed

Stop conditions:
- Do not stage unrelated files.
- Do not target main.
- Do not implement #227 clean-install or checkout-retirement behavior.
- Do not merge or revive stale PR #65.
- Do not edit .gitignore or CI gates unless explicitly authorized by a separate contract.
- Do not create, mutate, read, copy, sanitize, upload, move, delete, hash, import, archive, or commit generated/private/local artifacts.
- Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
- Do not close issue #153/#227 unless explicitly approved.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/153"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/227"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/local_artifact_manifest_environment_profiles.md"
  implementation_handoff: "docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md"
  target_artifact: "docs/contract_test_reports/local_artifact_manifest_environment_profiles.md"
  branch: "codex/analytics-foundation"
  risk_tier: "Medium-High"
  findings:
    - "CT-153-001 fixed: `.env*` secret-surface checks now detect `.env`, `.env.local`, and `.env.production` as present local state without reading or printing values."
  validation:
    - "py -m pytest -q tests\\test_check_local_environment.py -> 15 passed"
    - "py -m pytest -q tests\\test_check_secret_patterns.py tests\\test_check_protected_surfaces.py -> 76 passed, 1 skipped"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_manual_jsonl_import.py -> 35 passed, 1 third-party warning"
    - "py -m ruff check tools tests src -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, manifest placeholder warnings"
    - "generated/private artifact status check -> no generated/private/local artifacts created or changed"
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
  stop_conditions:
    - "Do not implement #227 clean-install or checkout-retirement behavior."
    - "Do not merge or revive stale PR #65."
    - "Do not edit .gitignore or CI gates unless explicitly authorized by a separate contract."
    - "Do not create, mutate, read, copy, sanitize, upload, move, delete, hash, import, archive, or commit generated/private/local artifacts."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not target main or close issue #153/#227."
```
