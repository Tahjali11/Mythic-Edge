# Contract Test Report: Pre-v1 Clean-install Transition

## Findings

No blocking findings.

### CT-227-001 P3: `.env.example` scanner behavior is manually verified, but not pinned by a dedicated focused test

The contract requires `.env.example` with live-looking secret material to be
caught by the secret/private-marker scanner, not silently accepted by the local
environment checker. The implementation correctly keeps the checker
metadata-only and does not read `.env.example` values. Existing scanner behavior
was manually verified with a temporary tracked `.env.example` containing a
live-looking Apps Script URL; `tools/check_secret_patterns.py --all` reported
`FORBIDDEN live_webhook_url`.

This is not blocking because the behavior exists and the checker did not weaken
scanner behavior. A future narrow test in `tests/test_check_secret_patterns.py`
would make this cross-tool guarantee more durable.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/227

Related completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/153

## Tracker

N/A

## Contract

`docs/contracts/pre_v1_clean_install_transition.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed files reviewed:

- `docs/contracts/pre_v1_clean_install_transition.md`
- `docs/local_artifacts_manifest.json`
- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- `docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md`
- `docs/contract_test_reports/pre_v1_clean_install_transition.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The implementation must add report-only pre-v1 clean-install transition support
using the completed #153 manifest/checker. It must allow exact tracked
`.env.example` as a repo-owned template, keep real `.env*` local secret files
blocked, add a `clean_install_transition_audit` profile, and avoid cleanup,
clone creation, app startup, parser startup, import execution, artifact
migration, `.gitignore`, CI, runtime, workbook, webhook, Apps Script, Sheets,
AI, coaching, or production changes.

## Internal Project Area Reviewed

Quality / Governance, with shared-support relevance to Generated / Local
Artifacts, Local App / UI, Analytics, and parser runtime readiness.

## Bridge-Code Status Reviewed

`shared_support`. The audit report is advisory and report-only; it does not own
parser truth, analytics truth, local app runtime behavior, checkout retirement
authority, cleanup authority, or deployment readiness.

## Checks Run

```bash
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
gh issue view 227 --json number,title,state,body,url,labels
gh issue view 153 --json number,title,state,url
py -m pytest -q tests\test_check_local_environment.py
py tools\check_local_environment.py --profile clean_clone --format json
py tools\check_local_environment.py --profile clean_install_transition_audit --format json
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
py -m ruff check tools tests src
py tools\check_agent_docs.py
git diff --check
```

Path-scoped protected-surface and secret/private-marker scans were run over the
contract, manifest, checker, focused tests, handoff, and this report.

Additional scanner probe:

- Created a temporary Git repo with tracked `.env.example`.
- Wrote a synthetic live-looking Apps Script webhook URL into that file.
- Ran `py tools\check_secret_patterns.py --repo-root <temp> --all`.
- Verified scanner output reported `FORBIDDEN live_webhook_url`.

## Results

Approve for Codex F.

Validation results:

- `py -m pytest -q tests\test_check_local_environment.py` -> 20 passed
- `py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py` -> 76 passed, 1 skipped
- `py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py` -> 31 passed, 1 third-party warning
- `py -m ruff check tools tests src` -> passed
- `py tools\check_agent_docs.py` -> passed
- `git diff --check` -> passed
- `py tools\check_local_environment.py --profile clean_clone --format json` -> exited 0, `blocked: 0`, tracked `.env.example` accepted
- `py tools\check_local_environment.py --profile clean_install_transition_audit --format json` -> exited 0, `blocked: 0`, count-only Git/local artifact summary
- Path-scoped protected-surface scan -> passed, forbidden 0, warnings 0
- Path-scoped secret/private-marker scan -> warning result, forbidden 0,
  warnings from expected manifest placeholder artifact references
- Generated/private artifact status check -> no SQLite DB/WAL/SHM/journal,
  local artifact, frontend build, raw log, runtime, failed-post, workbook
  export, archive, copied app-data, or clone artifacts were created or changed

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-227-001 | P3 | `remaining_non_blocking` | scanner behavior manually verified but not pinned by a dedicated focused test | non_blocking | Contract requires `.env.example` with live-looking secret material to be caught by scanner behavior. | Temporary tracked `.env.example` with synthetic Apps Script URL was reported as `FORBIDDEN live_webhook_url`; existing scanner tests passed. | F / follow-up issue optional |

## Confirmed Contract Matches

- Exact tracked `.env.example` is accepted as repo-owned template source in
  `clean_clone` and `clean_install_transition_audit`.
- `.env`, `.env.local`, `.env.production`, and other non-example `.env*`
  variants remain blocked by focused tests.
- The checker does not read or print `.env.example` values.
- Untracked `.env.example` and modified tracked `.env.example` require manual
  review in focused tests.
- `clean_install_transition_audit` exists and returns report-only exit `0`.
- Git metadata output is count-only; changed paths, untracked filenames, stash
  text, and private payloads are not printed.
- Generated/private artifact families remain symbolic/report-only.
- No cleanup, clone creation, checkout rename, app startup, parser startup,
  import execution, artifact migration, `.gitignore`, or CI-gate behavior was
  added.
- Existing #153 profiles and `live_parser` / `analytics_dev` aliases remain
  compatible.
- Existing local app setup/status/import behavior remains unchanged.
- Existing protected-surface and secret/private-marker tools remain
  authoritative.
- Issue #227 remains open; the implementation does not decide checkout
  retirement or authorize deletion.

## Contract Mismatches

- None blocking.

## Missing Tests

- Non-blocking: a dedicated scanner test for live-looking secret material in
  `.env.example` would pin the contract more directly. The scanner behavior was
  manually verified during review.

## Drift Notes

- Branch drift: `HEAD...origin/codex/analytics-foundation` was `0 0` during
  review.
- Issue lifecycle: issue #153 is closed; issue #227 remains open.
- Local-data drift: validation observed existing ignored/generated local
  artifact families symbolically, but no generated/private/local artifacts were
  created or changed.
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

Act as Codex F: Module Submitter for issue #227.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/227

Related completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/153

Branch:
codex/analytics-foundation

Contract:
docs/contracts/pre_v1_clean_install_transition.md

Implementation handoff:
docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md

Review artifact:
docs/contract_test_reports/pre_v1_clean_install_transition.md

Task:
Submit the reviewed #227 pre-v1 clean-install transition package. Inspect git status, confirm branch sync, stage only the intended #227 files plus the related #153 manifest/checker/test updates authorized by this contract, commit with a concise message, push codex/analytics-foundation, and open or update the draft PR toward the correct non-production integration target. Do not target main, merge, close issue #227, or change production behavior unless explicitly approved.

Reviewed files expected:
- docs/contracts/pre_v1_clean_install_transition.md
- docs/local_artifacts_manifest.json
- tools/check_local_environment.py
- tests/test_check_local_environment.py
- docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md
- docs/contract_test_reports/pre_v1_clean_install_transition.md

Validation already confirmed by Codex E:
- focused checker tests passed
- clean_clone and clean_install_transition_audit reports exited 0 with blocked 0
- secret/protected checker tests passed with one platform skip
- adjacent local app/launcher tests passed with one existing third-party warning
- Ruff passed
- agent docs check passed
- git diff --check passed
- path-scoped protected-surface scan passed
- path-scoped secret/private-marker scan had no forbidden findings and only expected manifest placeholder warnings
- generated/private artifact status check found no generated/private/local artifacts created or changed

Stop conditions:
- Do not stage unrelated files.
- Do not target main.
- Do not delete, move, rename, archive, copy, sanitize, upload, import, hash, clean, or commit local/private/generated artifacts.
- Do not create a fresh clone, rename the current checkout, run destructive cleanup commands, or start local app/parser/import workflows.
- Do not inspect secret values or private payload contents.
- Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
- Do not edit .gitignore or CI gates unless explicitly rerouted by the user.
- Do not close #227 unless explicitly approved.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/227"
  related_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/153"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/pre_v1_clean_install_transition.md"
  implementation_handoff: "docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md"
  target_artifact: "docs/contract_test_reports/pre_v1_clean_install_transition.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  findings:
    - "No blocking findings."
    - "CT-227-001 P3 non-blocking: `.env.example` scanner behavior manually verified but not pinned by a dedicated focused test."
  validation:
    - "py -m pytest -q tests\\test_check_local_environment.py -> 20 passed"
    - "py tools\\check_local_environment.py --profile clean_clone --format json -> exited 0, blocked 0"
    - "py tools\\check_local_environment.py --profile clean_install_transition_audit --format json -> exited 0, blocked 0"
    - "py -m pytest -q tests\\test_check_secret_patterns.py tests\\test_check_protected_surfaces.py -> 76 passed, 1 skipped"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_dev_app_launcher.py -> 31 passed, 1 third-party warning"
    - "py -m ruff check tools tests src -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, expected manifest placeholder warnings"
    - "generated/private artifact status check -> no generated/private/local artifacts created or changed"
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
  stop_conditions:
    - "Do not delete, move, rename, archive, copy, sanitize, upload, import, hash, clean, or commit local/private/generated artifacts."
    - "Do not create a fresh clone, rename the current checkout, run destructive cleanup commands, or start local app/parser/import workflows."
    - "Do not inspect secret values or private payload contents."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not edit .gitignore or CI gates unless explicitly rerouted by the user."
    - "Do not target main or close #227."
```
