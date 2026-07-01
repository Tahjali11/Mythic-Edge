# Security CWE-Mapped Local Validation Profile Advisory Report Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/603
- Parent security workflow: https://github.com/Tahjali11/Mythic-Edge/issues/330

## Contract Used

`docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md`

## Branch And Git Status

- Worktree: issue-scoped #603 worktree
- Branch: `codex/cwe-profile-advisory-report-603`
- Base branch: `main`
- Base ref: `origin/main`
- Initial implementation base: `3948e5204ae3372b6418c456297467fa8ca788bf`
- Refreshed base before final validation: `024eda7d9408c0bb72d645af4d41d604539291ba`
- Branch sync after refresh: `0 0` with `origin/main`
- Initial dirty state: one untracked contract artifact.

The branch was refreshed after `origin/main` advanced by the coverage-floor
merge. The only overlapping file was `tools/select_validation_mappings.py`; the
upstream coverage-floor mappings were preserved and the #603 mapping was added.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- GitHub issue #603
- `docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md`
- `docs/security/cwe_mapped_local_validation_profile.v1.json`
- `tools/check_cwe_mapped_local_validation_profile.py`
- `tests/test_cwe_mapped_local_validation_profile.py`
- `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md`
- `docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md`
- `tools/select_validation_mappings.py`
- nearby report helpers including `tools/generate_ruff_advisory_report.py` and
  `tools/generate_hardening_report.py`

## Current Behavior Compared To Contract

The repo already had the #597 advisory CWE profile manifest, manifest
validator, validator tests, implementation handoff, and contract-test report.
It did not have a durable JSON report helper that turns the profile manifest
and validator result into a public-safe advisory report.

The #603 contract authorizes only the first manifest-validator advisory report
slice. It explicitly defers scanner summaries and forbids CodeQL API reads, raw
SARIF reads, private artifact reads, CI changes, enforcement, CodeQL alert
mutation, security/privacy assurance claims, release/deploy readiness claims,
and parser/runtime/analytics/workbook/App Script/OpenAI/AI/coaching/Line Tracer
behavior changes.

## Implementation Option Chosen

Implemented the smallest report-only package:

1. Added a stdlib-only report helper that imports and reuses the existing CWE
   profile validator.
2. Added focused tests for report schema, advisory-only flags, warning/error
   preservation, unsupported-mode blocking, non-default profile path blocking,
   public-safe output, and deterministic report path naming.
3. Generated one intentional public-safe advisory JSON report under the
   contract-specified report directory.
4. Added the new helper/test mapping to validation selection metadata.
5. Produced this implementation handoff.

The helper consumes only:

- `docs/security/cwe_mapped_local_validation_profile.v1.json`
- the in-process result from `tools/check_cwe_mapped_local_validation_profile.py`
- public Git metadata for branch/ref and commit
- static public issue/path metadata from the contract

## Files Changed

- `docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md`
- `tools/generate_cwe_profile_advisory_report.py`
- `tests/test_cwe_profile_advisory_report.py`
- `tools/select_validation_mappings.py`
- `docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json`
- `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md`

## Exact Sections Changed

`tools/generate_cwe_profile_advisory_report.py`

- Added report constants for schema, source issue, parent issue, contract,
  manifest, validator, report directory, non-claims, blocked items, and
  validation commands.
- Added safe Git metadata lookup for public `measured_ref` and
  `measured_commit`.
- Added public-safe string filtering for selected report values.
- Added `build_report()` for the default `manifest_validator_advisory` mode.
- Added blocked report behavior for unsupported modes, non-default profile
  paths, unavailable validators, and unsafe input attempts.
- Added deterministic default report artifact path construction.
- Added CLI support for printing JSON or writing the default report artifact.

`tests/test_cwe_profile_advisory_report.py`

- Added focused report helper tests for:
  - success schema and advisory-only flags;
  - family entries remaining symbolic and public-safe;
  - validator errors preserved symbolically without raw private value echo;
  - validator warnings preserved symbolically;
  - unsupported modes blocked;
  - non-default profile paths blocked without raw path echo;
  - deterministic date/short-commit report path;
  - report generation not mutating the loaded manifest.

`tools/select_validation_mappings.py`

- Added focused validation mapping for the new helper and test file.
- Preserved the upstream `tools/check_coverage_floor.py` mapping added after
  the #603 branch was first created.

Generated JSON report

- Added
  `docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json`.
- The report records `passed_advisory`, seven families, zero validator errors,
  zero validator warnings, explicit non-claims, false enforcement/CI/CodeQL
  mutation/assurance flags, and blocked/deferred input categories.

## Change Type

- Code changed: yes, local advisory tooling only.
- Tests changed: yes, focused new helper tests.
- Docs changed: yes, contract artifact from Codex B plus this handoff.
- Report artifact changed: yes, one public-safe advisory JSON report.
- Runtime product behavior changed: no.

## Interface Changes

New local tooling interface:

```powershell
py tools\generate_cwe_profile_advisory_report.py
py tools\generate_cwe_profile_advisory_report.py --write-report --report-date 2026-07-01
```

New report artifact schema:

- `security_cwe_mapped_local_validation_profile_advisory_report.v1`

No parser payloads, app APIs, analytics schema, workbook columns, webhook
shape, Apps Script interfaces, CI status checks, or CodeQL alert lifecycle
interfaces changed.

## Contracted Area Status

Stayed inside Security/Quality advisory tooling.

Scanner summaries remain deferred. The helper does not read local scanner
outputs, raw SARIF, CodeQL API responses, private artifacts, raw logs, local
app data, SQLite contents, secrets, endpoint values, workbook exports, failed
post payloads, runtime logs, private decklists, or arbitrary user files.

## Validation Run

```powershell
py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py tests\test_cwe_profile_advisory_report.py
py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
py tools\generate_cwe_profile_advisory_report.py --write-report --report-date 2026-07-01
py -m json.tool docs\quality_reports\security\cwe_mapped_local_validation_profile\2026-07-01-024eda7-cwe-profile-advisory-report.json
py -m ruff check tools\generate_cwe_profile_advisory_report.py tests\test_cwe_profile_advisory_report.py
git diff --check
py tools\check_agent_docs.py
```

Results:

- Focused CWE profile/report tests passed: `32 passed`.
- Manifest JSON syntax validation passed.
- Existing profile validator passed with `errors: 0`, `warnings: 0`.
- New helper generated the JSON report artifact for short commit `024eda7`.
- Generated report JSON syntax validation passed.
- Ruff on changed helper/test passed.
- `git diff --check` passed.
- `py tools\check_agent_docs.py` passed.
- Path-scoped protected-surface scan passed with `forbidden: 0`,
  `warnings: 0`.
- Path-scoped secret/private-marker scan passed with `forbidden: 0`,
  `warnings: 0`.

## Protected-Surface Status

Expected posture before final scan:

- Parser/runtime behavior unchanged.
- Analytics behavior unchanged.
- Workbook/webhook/App Script/Sheets behavior unchanged.
- OpenAI/model-provider/AI/coaching/Line Tracer behavior unchanged.
- CI/enforcement/CodeQL alert state unchanged.

## Secret/Private-Marker Status

Expected posture before final scan:

The generated report includes symbolic blocked item names such as
`sqlite_contents`, `raw_sarif_files`, and `private_evidence_packets`, but no raw
private contents, raw paths, raw hashes, secrets, endpoint values, logs,
database contents, or local-only scanner outputs.

## Still Unverified

- Codex E has not independently reviewed the report schema and non-claim
  language.
- No PR was opened.
- No CI run has executed this helper.
- Scanner-summary aggregation remains intentionally deferred.

## Forbidden Scope

Forbidden scope was not touched:

- No CI gate or enforcement change.
- No CodeQL alert mutation or dismissal.
- No scanner summary aggregation.
- No private evidence packet, raw SARIF, raw CodeQL API response, raw log,
  SQLite content, workbook export, app-data file, transport-failure artifact, runtime
  log, secret, endpoint value, or local-only scanner output was read into the
  report helper.
- No parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/
  coaching/Line Tracer/production behavior changed.

## Reviewer Focus

Ask Codex E to pay special attention to:

- Whether the helper reads only the allowed manifest, validator result, and
  public Git/repo metadata.
- Whether the JSON report schema matches the contract.
- Whether non-claims are explicit enough to avoid CodeQL closure, security
  assurance, privacy assurance, release readiness, deploy readiness, CI
  enforcement, parser truth, analytics truth, AI truth, or coaching truth
  overclaims.
- Whether unsupported modes and non-default profile paths fail closed without
  raw value echo.
- Whether the generated report is safe to commit as a public repo artifact.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #603.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/603

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/cwe-profile-advisory-report-603

Base branch:
main

Contract:
docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md

Implementation handoff:
docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md

Generated report:
docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json

Goal:
Review the #603 implementation against the contract. Verify that the helper
consumes only the CWE profile manifest, existing profile validator result, and
public repo metadata; that the generated report schema and status vocabulary
match the contract; that non-claims are explicit; and that no scanner summary,
CodeQL lifecycle, CI enforcement, private evidence, parser/runtime/analytics,
workbook/App Script, OpenAI/AI/coaching, Line Tracer, production, or release
readiness scope was introduced.

Inspect:
- git status --short --branch --untracked-files=all
- docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md
- tools/generate_cwe_profile_advisory_report.py
- tests/test_cwe_profile_advisory_report.py
- tools/select_validation_mappings.py
- docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json
- docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md
- existing profile manifest and validator files from issue #597

Run validation:
- py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py tests\test_cwe_profile_advisory_report.py
- py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
- py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
- py tools\generate_cwe_profile_advisory_report.py --write-report --report-date 2026-07-01
- py -m json.tool docs\quality_reports\security\cwe_mapped_local_validation_profile\2026-07-01-024eda7-cwe-profile-advisory-report.json
- py -m ruff check tools\generate_cwe_profile_advisory_report.py tests\test_cwe_profile_advisory_report.py
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over changed files with base origin/main
- path-scoped secret/private-marker scan over changed files with base origin/main

Review requirements:
- Lead with findings ordered by severity.
- Treat scanner aggregation, raw SARIF reads, CodeQL API calls, private evidence reads, CI/enforcement changes, or assurance/readiness overclaims as blocking.
- Treat raw private path/value echo as blocking.
- Do not stage, commit, push, open a PR, mutate CodeQL alerts, or close issue #603.

Final report must include:
- findings first
- contract conformance verdict
- validation run and result
- advisory-only status
- public-safe report status
- protected-surface status
- secret/private-marker status
- remaining risk
- whether Codex F submitter is recommended
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/603"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "C"
  next_thread: "E"
  contract_artifact: "docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md"
  target_artifact: "docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md"
  generated_report: "docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json"
  branch: "codex/cwe-profile-advisory-report-603"
  base_branch: "main"
  refreshed_base_commit: "024eda7d9408c0bb72d645af4d41d604539291ba"
  risk_tier: "High workflow and security-communication risk; low runtime risk"
  decision: "First helper consumes only the CWE profile manifest, existing validator result, and public repo metadata; scanner summaries remain deferred."
  validation:
    - "py -m pytest -q tests\\test_cwe_mapped_local_validation_profile.py tests\\test_cwe_profile_advisory_report.py -> passed, 32 passed"
    - "py -m json.tool docs\\security\\cwe_mapped_local_validation_profile.v1.json -> passed"
    - "py tools\\check_cwe_mapped_local_validation_profile.py docs\\security\\cwe_mapped_local_validation_profile.v1.json -> passed"
    - "py tools\\generate_cwe_profile_advisory_report.py --write-report --report-date 2026-07-01 -> passed"
    - "py -m json.tool docs\\quality_reports\\security\\cwe_mapped_local_validation_profile\\2026-07-01-024eda7-cwe-profile-advisory-report.json -> passed"
    - "py -m ruff check tools\\generate_cwe_profile_advisory_report.py tests\\test_cwe_profile_advisory_report.py -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  advisory_only: true
  ci_change_authorized: false
  enforcement_authorized: false
  codeql_alert_mutation_authorized: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
