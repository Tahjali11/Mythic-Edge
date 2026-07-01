# Security CWE-Mapped Local Validation Profile Contract-Test Report

## Findings

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | evidence | expected behavior | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-597-001 | P1 | `fixed_state_followup` | fixed | not_blocking | Codex D generalized Windows absolute path detection, added non-user Windows absolute path regression coverage, and Codex E confirmed with an in-memory probe that synthetic drive-root path evidence is rejected with `unsafe_report_output` without echoing raw values. | The validator now rejects Windows absolute paths generally and keeps report output symbolic. | F |

## Role Performed

Codex E: Module Reviewer / contract-test thread.

## Issue And Parent Reviewed

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/597>
- Parent security workflow: <https://github.com/Tahjali11/Mythic-Edge/issues/330>

Both issues remain open.

## Contract

- Contract used:
  `docs/contracts/security_cwe_mapped_local_validation_profile.md`
- Implementation handoff:
  `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md`

Repo workflow references reviewed:

- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

- Branch: `codex/cwe-mapped-local-validation-profile-597`
- Base ref: `origin/main`
- Branch sync: `0 0`
- Changed package files:
  - `docs/security/cwe_mapped_local_validation_profile.v1.json`
  - `tools/check_cwe_mapped_local_validation_profile.py`
  - `tests/test_cwe_mapped_local_validation_profile.py`
  - `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md`
  - `docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

Issue #597 may add advisory-only security profile tooling: a public-safe CWE
manifest, a schema/policy validator, focused tests, and handoff documentation.

It must not:

- change CI;
- enable enforcement;
- mutate CodeQL alerts;
- scan private evidence;
- claim formal CWE compliance, security assurance, privacy assurance, release
  readiness, deploy readiness, or production readiness;
- change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/
  AI/coaching/Line Tracer/production behavior;
- allow raw/private/generated/local artifacts or local absolute paths into
  manifests or reports.

## Internal Project Area Reviewed

Quality / Governance security validation.

No internal project area mismatch found.

## Bridge-Code Status Reviewed

`shared_support`

The package remains advisory support tooling and does not move parser truth,
CodeQL alert lifecycle truth, vulnerability truth, or security assurance into
the local profile.

## Files Reviewed

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`
- `docs/contracts/security_cwe_mapped_local_validation_profile.md`
- `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md`
- `docs/security/cwe_mapped_local_validation_profile.v1.json`
- `tools/check_cwe_mapped_local_validation_profile.py`
- `tests/test_cwe_mapped_local_validation_profile.py`

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
git diff --name-status
py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py
py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
py -m ruff check tools\check_cwe_mapped_local_validation_profile.py tests\test_cwe_mapped_local_validation_profile.py
git diff --check
py tools\check_agent_docs.py
```

Additional Codex E boundary probe:

- Mutated an in-memory copy of the manifest by appending synthetic non-user
  Windows absolute path shapes to family evidence.
- Called `validate_profile(...)`.
- Observed: both path shapes were rejected with `unsafe_report_output`.
- Confirmed: rendered reports did not echo the raw local path values.
- No file was written for this probe.

Path-scoped protected-surface and secret/private-marker scans were run over the
changed package files and this report.

## Validation Results

Implementation validation passed:

- Branch sync: `0 0` against `origin/main`.
- Focused pytest: `24 passed`.
- JSON syntax validation: passed.
- Profile validator against the manifest: passed with `errors: 0`, `warnings: 0`.
- Focused Ruff check: passed.
- `git diff --check`: passed.
- `py tools\check_agent_docs.py`: passed with `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan: passed, forbidden `0`, warnings `0`.
- Path-scoped secret/private-marker scan: passed, forbidden `0`, warnings `0`.

Contract-test result: passed. CT-597-001 is fixed.

## Confirmed Contract Matches

- The manifest includes exactly the seven required v1 risk families:
  - `local_path_traversal`
  - `generated_filename_id_to_path`
  - `subprocess_command_line_invocation`
  - `url_host_validation`
  - `secret_private_artifact_exposure`
  - `temporary_file_handling`
  - `workflow_permission_scope`
- Primary CWE mappings match the contract:
  - `CWE-22`
  - `CWE-73`
  - `CWE-78`
  - `CWE-187`
  - `CWE-538`
  - `CWE-377`
  - `CWE-732`
- Broad/discouraged/prohibited CWE IDs are not used as primary mappings in the
  manifest.
- Scanner provenance is separated from local profile mappings for the broad or
  prohibited scanner CWE tags.
- `profile_status` is `advisory_profile`.
- CI, enforcement, CodeQL alert mutation, parser behavior change, security
  assurance, and privacy assurance flags are false.
- No CI workflow, required status check, CodeQL alert state, parser behavior,
  analytics schema, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/
  coaching behavior, Line Tracer behavior, or production behavior changed.
- The package uses stdlib-only local validation and focused synthetic tests.

## Remaining Contract Mismatches

None.

## Fixed-State Confirmation

### CT-597-001: local absolute path rejection is complete

The contract says:

- the manifest must not contain local absolute paths;
- reports must not include local absolute paths;
- unsafe report output must fail closed.

Codex D changed the unsafe text detection to reject Windows drive-root absolute
path shapes generally. The focused test suite now covers non-user Windows
absolute path forms with both backslash and forward-slash separators.

Codex E confirmed the original failure mode no longer reproduces. An in-memory
manifest mutation with synthetic non-user Windows local path evidence now fails
validation with `unsafe_report_output`, and `render_report(...)` does not echo
the raw values.

## Missing Tests

None remaining for this issue scope.

## Advisory/No-Enforcement Status

Advisory-only status is preserved.

Review found no:

- CI change;
- enforcement activation;
- CodeQL alert mutation;
- broad scanner integration;
- private evidence inspection;
- security or privacy assurance claim.

## Protected-Surface Status

Passed: forbidden `0`, warnings `0`.

## Secret/Private-Marker Status

Passed: forbidden `0`, warnings `0`.

## Generated/Private Artifact Status

No generated/private artifacts were kept.

No raw Player.log, raw JSONL, SQLite contents, private app-data, raw SARIF,
tokens, credentials, webhook URLs, runtime logs, workbook exports, or local-only
artifacts were read, copied, committed, or exposed.

## Forbidden Scope

Forbidden scope touched: `false`.

The package did not change parser/runtime behavior, parser truth ownership,
analytics schema/ingest, workbook/webhook/App Script/Sheets behavior,
OpenAI/AI/coaching behavior, Line Tracer behavior, production behavior, CI,
or CodeQL alert lifecycle state.

## Drift Notes

- Repo drift: none found. Branch is synced with `origin/main`.
- CI drift: unverified. This local package has not been pushed for CI.
- CodeQL closure: not claimed. Local validation does not prove CodeQL closure
  or security assurance.
- Tracker drift: none blocking. Parent #330 remains open.

## Recommendation

Approve.

Route to Codex F if the user wants to publish the reviewed #597 advisory
tooling package. Do not claim CodeQL closure, security assurance, privacy
assurance, CI enforcement, or production readiness.

## Next Workflow Action

Next role: Codex F / Module Submitter, if publishing is desired.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #597.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/597

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/cwe-mapped-local-validation-profile-597

Reviewed contract:
docs/contracts/security_cwe_mapped_local_validation_profile.md

Reviewed artifacts:
docs/security/cwe_mapped_local_validation_profile.v1.json
tools/check_cwe_mapped_local_validation_profile.py
tests/test_cwe_mapped_local_validation_profile.py
docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md
docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md

Goal:
Submit the reviewed #597 advisory tooling package. Stage only the reviewed #597 files, commit, push the branch, and open a draft PR targeting main. Do not change CI, enable enforcement, mutate CodeQL alerts, run broad scanner integration, read private evidence, or claim CodeQL closure/security/privacy assurance.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py
py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
py -m ruff check tools\check_cwe_mapped_local_validation_profile.py tests\test_cwe_mapped_local_validation_profile.py
git diff --check
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over:
- docs/contracts/security_cwe_mapped_local_validation_profile.md
- docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md
- docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md
- docs/security/cwe_mapped_local_validation_profile.v1.json
- tools/check_cwe_mapped_local_validation_profile.py
- tests/test_cwe_mapped_local_validation_profile.py

Do not:
- stage unrelated files
- merge, close #597, or close #330
- change CI or enable enforcement
- mutate CodeQL alerts
- run broad scanner integration
- read private evidence or local-only artifacts
- expose raw/private/generated/local artifacts
- change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior

Final output:
- branch
- commit hash
- draft PR URL
- files staged
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- forbidden scope touched true/false
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/597"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "E"
  next_thread: "F"
  branch: "codex/cwe-mapped-local-validation-profile-597"
  contract_artifact: "docs/contracts/security_cwe_mapped_local_validation_profile.md"
  implementation_handoff: "docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md"
  review_artifact: "docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md"
  findings:
    - "CT-597-001 P1 fixed: validator rejects generic Windows local absolute path evidence without echoing raw values."
  validation:
    - "py -m pytest -q tests\\test_cwe_mapped_local_validation_profile.py -> passed, 24 tests"
    - "py -m json.tool docs\\security\\cwe_mapped_local_validation_profile.v1.json -> passed"
    - "py tools\\check_cwe_mapped_local_validation_profile.py docs\\security\\cwe_mapped_local_validation_profile.v1.json -> passed"
    - "py -m ruff check tools\\check_cwe_mapped_local_validation_profile.py tests\\test_cwe_mapped_local_validation_profile.py -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "Codex E fixed-state probe -> passed, synthetic non-user Windows absolute path evidence rejected with no raw-value echo"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  advisory_only_status: "preserved"
  enforcement_authorized: false
  ci_changed: false
  codeql_alert_mutation_authorized: false
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  recommendation: "route to Codex F if publishing; otherwise accept/no-op"
  next_recommended_role: "Codex F: Module Submitter"
```
