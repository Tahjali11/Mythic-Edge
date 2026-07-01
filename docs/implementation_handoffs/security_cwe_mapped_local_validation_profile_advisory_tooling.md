# Security CWE-Mapped Local Validation Profile Advisory Tooling Handoff

## Role Performed

Codex C: Module Implementer.

## Issue And Parent

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/597
- Parent security workflow: https://github.com/Tahjali11/Mythic-Edge/issues/330

## Contract Used

- `docs/contracts/security_cwe_mapped_local_validation_profile.md`

## Branch And Status

- Branch: `codex/cwe-mapped-local-validation-profile-597`
- Base: `origin/main`
- Branch sync before implementation: `0 0`
- Git status at handoff creation: new untracked #597 package files only.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/security_cwe_mapped_local_validation_profile.md`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_protected_surfaces.py`
- `tests/test_github_workflow_permissions.py`
- GitHub issue #597
- GitHub issue #330

## Current Behavior Compared To Contract

The repository already had secret/private-marker scanning, protected-surface
path classification, and a workflow-permission posture test. It did not have a
single public-safe manifest that maps local preventive security validation
families to exact CWE IDs, and it did not have a focused validator for that
profile.

The contract authorizes advisory-only local tooling. It does not authorize CI
changes, enforcement, CodeQL alert mutation, scanner integration, private
artifact inspection, or security/privacy assurance claims.

## Implementation Option Chosen

Implemented the smallest advisory tooling package:

- one deterministic public-safe JSON manifest;
- one stdlib-only validator;
- one focused validator test module;
- this implementation handoff.

No CI workflow, CodeQL alert state, broad scanner run, parser behavior, local
app behavior, analytics schema, workbook/webhook/App Script behavior, OpenAI/AI
behavior, production behavior, or private artifact boundary changed.

## Files Changed

- `docs/security/cwe_mapped_local_validation_profile.v1.json`
- `tools/check_cwe_mapped_local_validation_profile.py`
- `tests/test_cwe_mapped_local_validation_profile.py`
- `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md`

## Exact Sections Changed

### Manifest

Added `docs/security/cwe_mapped_local_validation_profile.v1.json` with:

- required envelope fields from the contract;
- `profile_status: advisory_profile`;
- explicit false flags for CI, enforcement, CodeQL mutation, parser behavior
  changes, security assurance, and privacy assurance;
- `profile_manifest_implementation_authorized: true` for this #597 slice;
- the seven v1 families:
  - `local_path_traversal`;
  - `generated_filename_id_to_path`;
  - `subprocess_command_line_invocation`;
  - `url_host_validation`;
  - `secret_private_artifact_exposure`;
  - `temporary_file_handling`;
  - `workflow_permission_scope`.

### Validator

Added `tools/check_cwe_mapped_local_validation_profile.py` with checks for:

- required envelope and family fields;
- exact v1 family set;
- expected primary CWE per family;
- required related CWE IDs;
- rejected broad, discouraged, prohibited, placeholder, or invented mappings;
- advisory-only status boundaries;
- false enforcement, CodeQL mutation, parser behavior, and assurance flags;
- separate scanner provenance for discouraged or prohibited scanner CWE tags;
- public-safe output that avoids local absolute path echo.

### Tests

Added `tests/test_cwe_mapped_local_validation_profile.py` with focused coverage
for:

- manifest success path;
- CLI success report;
- exact family set;
- missing family rejection;
- enforcement and assurance flag rejection;
- blocking profile or rollout status rejection;
- URL, secret/private-artifact, and workflow broad/prohibited primary CWE
  rejection;
- required discouraged scanner provenance separation;
- placeholder/invented rejected mapping rejection;
- local absolute path and live webhook URL non-echo behavior.

## Change Type

- Code changed: yes, local advisory tooling only.
- Tests changed: yes, focused validator tests only.
- Docs changed: yes, implementation handoff and public-safe profile manifest.
- CI changed: no.
- Enforcement changed: no.
- Scanner integration changed: no.

## Validation Run

- `git status --short --branch --untracked-files=all`
  - passed; only #597 package files are untracked.
- `git rev-list --left-right --count HEAD...origin/main`
  - passed: `0 0`.
- `py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py`
  - passed: `22 passed`.
- `py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json`
  - passed.
- `py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json`
  - passed: `errors: 0`, `warnings: 0`, `result: passed`.
- `py -m ruff check tools\check_cwe_mapped_local_validation_profile.py tests\test_cwe_mapped_local_validation_profile.py`
  - passed.
- `git diff --check`
  - passed.
- direct whitespace/final-newline check over the four untracked package files
  - passed.
- `py tools\check_agent_docs.py`
  - passed: `errors: 0`, `warnings: 0`, `result: passed`.
- path-scoped protected-surface scan over the four touched paths with
  `--base origin/main --paths-from-stdin`
  - passed: `forbidden: 0`, `warnings: 0`, `result: passed`.
- path-scoped secret/private-marker scan over the four touched paths with
  `--base origin/main --paths-from-stdin`
  - passed: `forbidden: 0`, `warnings: 0`, `result: passed`.

## Protected-Surface Status

Path-scoped protected-surface status: passed with no forbidden findings and no
warnings. This package touches Quality/Governance docs and local advisory
tooling only.

## Secret/Private-Marker Status

Path-scoped secret/private-marker status: passed with no forbidden findings and
no warnings. No private values, raw logs, local absolute paths, generated local
artifacts, CodeQL alert mutation metadata, or private evidence are included.

## Generated/Private Artifact Status

No raw coverage, private logs, private paths, generated local artifacts,
workbook exports, app-data files, failed posts, runtime files, private reports,
or local-only scanner outputs were created or committed by this slice.

## Remaining Risk

- The manifest is advisory vocabulary, not proof that all repo security checks
  are complete.
- The validator checks profile shape and safety, not actual source-code
  vulnerabilities.
- CodeQL alert closure or dismissal remains outside this package.
- CI enforcement remains unauthorized.

## Codex D Fixer Addendum

### Source Finding

- Review artifact:
  `docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md`
- Finding fixed:
  `CT-597-001 P1`: the validator accepted generic local absolute path evidence
  despite the contract forbidding local absolute paths.

### Fault Category

Implementation gap in public-safe text detection. The validator recognized
Windows user-profile paths, but not non-user drive-root absolute path shapes.

### Fix Produced

- Expanded the unsafe text detector to reject generic Windows drive-root
  absolute paths.
- Kept validator output symbolic; the raw local path value is not echoed in the
  rendered report.
- Added focused regression coverage for non-user Windows absolute path evidence
  using both backslash and forward-slash separators.

### Codex D Files Changed

- `tools/check_cwe_mapped_local_validation_profile.py`
- `tests/test_cwe_mapped_local_validation_profile.py`
- `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md`

### Codex D Validation Run

- `py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py`
  - passed: `24 passed`.
- `py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json`
  - passed.
- `py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json`
  - passed: `errors: 0`, `warnings: 0`, `result: passed`.
- `py -m ruff check tools\check_cwe_mapped_local_validation_profile.py tests\test_cwe_mapped_local_validation_profile.py`
  - passed.
- `git diff --check`
  - passed.
- `py tools\check_agent_docs.py`
  - passed: `errors: 0`, `warnings: 0`, `result: passed`.

### Remaining Review Focus

- Confirm `CT-597-001` is fixed by the generalized Windows absolute path
  detector.
- Confirm the validator still does not echo raw local path values in reports.
- Confirm advisory-only status, no-enforcement flags, and CodeQL
  non-mutation boundaries remain preserved.

## Forbidden Scope

Forbidden scope was not touched:

- no CI changes;
- no enforcement activation;
- no CodeQL alert mutation;
- no broad scanner run;
- no private evidence inspection;
- no parser behavior or parser truth change;
- no workbook, webhook, Apps Script, production, OpenAI/model-provider, or
  AI/coaching behavior change.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #597.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/597

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/cwe-mapped-local-validation-profile-597

Contract:
docs/contracts/security_cwe_mapped_local_validation_profile.md

Implementation handoff:
docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md

Review scope:
Review the advisory-only CWE-mapped local validation profile package against the contract. Verify that the implementation adds only public-safe profile manifest, focused validator, focused tests, and handoff documentation. Confirm no CI enforcement, CodeQL alert mutation, scanner integration, private evidence inspection, parser behavior change, workbook/webhook/App Script change, production behavior change, OpenAI/model-provider change, or AI/coaching behavior change occurred.

Files expected in scope:
- docs/security/cwe_mapped_local_validation_profile.v1.json
- tools/check_cwe_mapped_local_validation_profile.py
- tests/test_cwe_mapped_local_validation_profile.py
- docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md

Validation to run:
- git status --short --branch --untracked-files=all
- py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py
- py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
- py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
- py -m ruff check tools\check_cwe_mapped_local_validation_profile.py tests\test_cwe_mapped_local_validation_profile.py
- git diff --check
- path-scoped protected-surface scan over changed files with base origin/main
- path-scoped secret/private-marker scan over changed files with base origin/main

Review questions:
- Does the profile include exactly the seven required v1 risk families?
- Are primary CWE mappings exact and contract-aligned?
- Are broad/discouraged/prohibited CWE IDs kept out of primary finding IDs?
- Are scanner provenance CWEs separated from local profile CWE mappings?
- Are enforcement, CI, CodeQL mutation, parser behavior, and assurance flags false?
- Does the validator fail closed without echoing local absolute paths or live private URLs?
- Does the implementation avoid all forbidden private/generated artifacts and product behavior changes?

Final report must include:
- role performed
- issue/parent reviewed
- contract used
- branch and git status
- files reviewed
- findings first, ordered by severity
- validation run and results
- protected-surface status
- secret/private-marker status
- advisory/no-enforcement status
- generated/private artifact status
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/597"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "D"
  next_thread: "E"
  branch: "codex/cwe-mapped-local-validation-profile-597"
  contract_artifact: "docs/contracts/security_cwe_mapped_local_validation_profile.md"
  implementation_handoff: "docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md"
  review_artifact: "docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md"
  manifest: "docs/security/cwe_mapped_local_validation_profile.v1.json"
  validator: "tools/check_cwe_mapped_local_validation_profile.py"
  tests: "tests/test_cwe_mapped_local_validation_profile.py"
  finding_fixed:
    - "CT-597-001 P1: validator now rejects generic Windows local absolute path evidence without echoing raw values."
  verdict: "ct_597_001_fixed_ready_for_confirmation"
  validation:
    - "py -m pytest -q tests\\test_cwe_mapped_local_validation_profile.py -> 24 passed"
    - "py -m json.tool docs\\security\\cwe_mapped_local_validation_profile.v1.json -> passed"
    - "py tools\\check_cwe_mapped_local_validation_profile.py docs\\security\\cwe_mapped_local_validation_profile.v1.json -> passed"
    - "py -m ruff check tools\\check_cwe_mapped_local_validation_profile.py tests\\test_cwe_mapped_local_validation_profile.py -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  enforcement_authorized: false
  ci_changed: false
  codeql_alert_mutation_authorized: false
  forbidden_scope_touched: false
  generated_private_artifacts_kept: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
