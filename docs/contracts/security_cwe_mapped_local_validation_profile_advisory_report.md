# Security CWE-Mapped Local Validation Profile Advisory Report Contract

## Module

- Module name: `security_cwe_mapped_local_validation_profile_advisory_report`
- Role: Codex B / Module Contract Writer
- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/603>
- Parent security workflow: <https://github.com/Tahjali11/Mythic-Edge/issues/330>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source profile contract: `docs/contracts/security_cwe_mapped_local_validation_profile.md`
- Source implementation issue: <https://github.com/Tahjali11/Mythic-Edge/issues/597>
- Source implementation PR: <https://github.com/Tahjali11/Mythic-Edge/pull/602>
- Expected implementation handoff:
  `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md`
- Risk tier: High workflow and security-communication risk; low runtime risk if
  kept advisory-only and input-limited.

## Plain-English Intent

Mythic Edge now has a public-safe, advisory CWE-mapped local validation profile.
That profile names the repo's preventive security-check families and maps them
to exact CWE IDs. The next step is a report helper that can produce a durable,
reviewable summary of the profile and validator result.

The report must be careful about what it proves. It may say whether the local
profile manifest is shaped correctly and whether its advisory vocabulary is
safe to display. It must not say that CodeQL alerts are closed, that the repo is
secure, that private data is protected, that a release is ready, or that any CI
gate is active.

## Observed Current Behavior

At the time of this contract:

- PR #602 is merged into `main` with the advisory profile package.
- `docs/security/cwe_mapped_local_validation_profile.v1.json` exists.
- The manifest has `profile_status: advisory_profile`.
- The manifest defines seven advisory families:
  - `local_path_traversal` with primary `CWE-22`;
  - `generated_filename_id_to_path` with primary `CWE-73`;
  - `subprocess_command_line_invocation` with primary `CWE-78`;
  - `url_host_validation` with primary `CWE-187`;
  - `secret_private_artifact_exposure` with primary `CWE-538`;
  - `temporary_file_handling` with primary `CWE-377`;
  - `workflow_permission_scope` with primary `CWE-732`.
- `tools/check_cwe_mapped_local_validation_profile.py` validates the manifest
  shape, exact-CWE policy, safety flags, and public-safe display boundaries.
- `tests/test_cwe_mapped_local_validation_profile.py` exercises the validator,
  including failure cases for unsafe text and unsupported enforcement posture.
- `docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md`
  records that the #597 advisory profile package passed contract-test review.

## Responsibility Boundary

This contract authorizes only a future advisory report helper and report shape.

The report is allowed to own:

- the local profile manifest validation result;
- symbolic profile metadata;
- advisory family inventory;
- validator error and warning counts;
- symbolic validator issue codes and JSON-path-like locations;
- explicit non-claims;
- next recommended workflow role and validation evidence.

The report does not own:

- CodeQL alert lifecycle state;
- vulnerability truth;
- security assurance;
- privacy assurance;
- release readiness;
- deploy readiness;
- parser truth;
- analytics truth;
- CI enforcement;
- issue closure decisions.

## Allowed Inputs

The first implementation slice should consume only:

1. `docs/security/cwe_mapped_local_validation_profile.v1.json`;
2. the validator result produced by
   `tools/check_cwe_mapped_local_validation_profile.py` or its in-process
   validation helpers;
3. public repo metadata needed to identify the measured ref, measured commit,
   report helper version, contract path, and source issues;
4. this contract and the #597 handoff/review artifacts for static metadata
   references.

The helper may read Git metadata such as the current commit hash and branch/ref
name, but it must not infer release readiness from those values.

## Deferred Inputs

The first report helper should not aggregate local scanner outputs.

A later contract may allow public-safe summaries from repo-owned tools such as
protected-surface checks or secret-pattern checks, but only if all of these are
true:

- the summary is explicitly symbolic, count-based, and repo-relative;
- the summary does not include raw scanner output;
- the summary does not include private paths, raw values, or local-only files;
- the summary has its own tests proving unsafe values are not echoed;
- the report still labels the information advisory-only.

## Forbidden Inputs

The report helper must not read, parse, embed, summarize, or link to:

- private evidence packets;
- raw log files;
- local app data;
- generated SQLite databases or SQLite contents;
- raw SARIF files;
- raw CodeQL API responses;
- secrets, tokens, credentials, API keys, endpoint values, or environment
  values;
- workbook exports;
- failed-post queue artifacts;
- generated/private/local-only scanner outputs;
- arbitrary user-provided files.

If a future caller tries to supply one of these inputs, the helper must fail
closed with a symbolic status and must not echo the unsafe value.

## Report Artifact Path

Future implementation should write intentional durable reports under:

`docs/quality_reports/security/cwe_mapped_local_validation_profile/`

Recommended filename pattern:

`<YYYY-MM-DD>-<short-commit>-cwe-profile-advisory-report.json`

The report should be JSON for deterministic review and testability. A Markdown
summary may be added later, but JSON is the contract source for the first slice.

Generated reports are repo artifacts only when intentionally produced by an
implementation or review thread. The helper must not write reports into local
app data, runtime folders, user profile paths, or temporary private locations.

## Report Schema Recommendation

The first report version should use:

`schema_version: "security_cwe_mapped_local_validation_profile_advisory_report.v1"`

Required top-level fields:

- `schema_version`
- `report_id`
- `repository`
- `repository_url`
- `contract_ref`
- `source_issue`
- `parent_issue`
- `source_profile_contract`
- `source_profile_manifest`
- `source_validator`
- `measured_ref`
- `measured_commit`
- `generated_at_policy`
- `run_mode`
- `overall_status`
- `profile_status`
- `profile_family_count`
- `families`
- `validator`
- `non_claims`
- `privacy_redaction`
- `advisory_only`
- `enforcement_authorized`
- `ci_change_authorized`
- `codeql_alert_mutation_authorized`
- `security_assurance_claimed`
- `privacy_assurance_claimed`
- `validation_commands`
- `next_recommended_role`

Required `families[]` fields:

- `family_id`
- `primary_cwe_id`
- `primary_cwe_title`
- `mapping_review_status`
- `rollout_status`
- `codeql_rule_ids`
- `local_detector_ids`
- `reporting_policy`
- `non_claims`

Required `validator` fields:

- `tool`
- `result`
- `exit_code`
- `errors_count`
- `warnings_count`
- `errors`
- `warnings`

Required `validator.errors[]` and `validator.warnings[]` fields:

- `code`
- `location`
- `message`

Validator messages must be symbolic and public-safe. Locations may identify
manifest paths such as `families[0].primary_cwe_id`; they must not identify
absolute local paths or private files.

## Status Vocabulary

Allowed `run_mode` values:

- `manifest_validator_advisory`: default first-slice mode; validates only the
  manifest and records the validator result.
- `contract_review_only`: report was produced from static contract inspection
  without running the validator.
- `unsupported_input_blocked`: caller requested inputs outside this contract.

Allowed `overall_status` values:

- `passed_advisory`: the manifest validator passed with zero errors and zero
  warnings.
- `warning_advisory`: the manifest validator passed with zero errors and one
  or more warnings.
- `failed_advisory`: the manifest validator reported one or more errors.
- `blocked_unsafe_input`: the helper refused an unsafe or forbidden input.
- `blocked_unsupported_mode`: the helper refused a mode that is not authorized
  by this contract.
- `blocked_validator_unavailable`: the helper could not run or import the
  profile validator.

Allowed `validator.result` values:

- `passed`
- `failed`
- `not_run`
- `blocked`

The report must preserve validator failures as advisory report state. A failed
advisory report is not a CI gate, release blocker, or CodeQL closure signal by
itself.

## Required Non-Claims

Every report must include explicit non-claims equivalent to:

- This report is advisory local validation evidence only.
- This report does not mutate, dismiss, reopen, or close CodeQL alerts.
- This report does not prove that CodeQL has zero open alerts.
- This report is not formal CWE compliance.
- This report is not security assurance.
- This report is not privacy assurance.
- This report is not release readiness.
- This report is not deploy readiness.
- This report is not CI enforcement.
- This report is not parser truth, analytics truth, AI truth, or coaching
  truth.
- This report does not authorize production, workbook, webhook, Apps Script,
  Google Sheets, OpenAI, model-provider, Line Tracer, or coaching behavior
  changes.

## Privacy And Redaction Requirements

All output must be public-safe and repo-relative.

Allowed output forms:

- repo-relative paths for repo-owned docs, tools, tests, and manifest files;
- Git refs and commit hashes;
- issue and PR URLs;
- CWE IDs and titles from the approved manifest;
- CodeQL rule IDs as symbolic scanner provenance;
- local detector IDs as symbolic detector names;
- counts, booleans, statuses, and issue codes.

Forbidden output forms:

- absolute user-machine paths;
- raw private paths;
- raw local app data paths;
- raw hashes of private files;
- raw log excerpts;
- private report contents;
- secret-like values;
- endpoint values;
- spreadsheet IDs;
- environment values;
- raw scanner payloads.

If unsafe text is detected, the report must use a symbolic placeholder such as
`<redacted>` or `<unsafe-input>` and must record `blocked_unsafe_input` or
`failed_advisory`, depending on whether the unsafe text came from caller input
or the manifest under validation.

## Advisory Versus Blocking Boundary

This report is advisory-only.

The report helper must not:

- add CI workflow steps;
- enable blocking validation;
- change `pyproject.toml`;
- change GitHub branch protection;
- change CodeQL alert state;
- make release-readiness decisions;
- make deployment-readiness decisions;
- claim that a security issue is fixed.

The report may recommend a future route, such as Codex C implementation review,
Codex E contract testing, or a separate enforcement-readiness issue. That
recommendation is workflow guidance only.

## Future Enforcement Preconditions

Any future enforcement issue requires a new problem representation and contract.

Before enforcement can be considered, Mythic Edge must have:

- explicit user approval for enforcement scope;
- a current profile report reviewed by Codex E;
- a current CodeQL lifecycle statement from the GitHub security workflow, kept
  separate from the local report;
- a stable policy for warnings versus errors;
- evidence that unsafe values are never echoed in failures;
- path-scoped protected-surface and secret/private-marker scans for the helper,
  tests, and report artifacts;
- a clear rollback plan for any CI or workflow change;
- no unresolved conflict with parser truth ownership, privacy boundaries, or
  release-readiness language.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser truth ownership;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, ingest behavior, or analytics truth;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- secrets, credentials, tokens, API keys, endpoint values, or environment
  values;
- raw logs, generated data, local app data, SQLite files, workbook exports, or
  local-only artifacts.

## Validation Expectations For Codex C

Codex C should implement only the report helper, focused tests, generated
public-safe report fixture/artifact if explicitly needed, and implementation
handoff.

Expected validation:

- `py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py`
- focused tests for the new report helper;
- `py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json`
- `py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json`
- run the new helper against the manifest and validate the produced JSON;
- `py -m ruff check` on changed Python test/tool files;
- `git diff --check`;
- `py tools\check_agent_docs.py`;
- path-scoped protected-surface scan over changed files;
- path-scoped secret/private-marker scan over changed files.

Automated tests must cover:

- successful advisory report generation;
- validator warnings and errors preserved symbolically;
- unsupported input mode blocked;
- unsafe local path or endpoint-like text not echoed;
- advisory-only flags remain false for CI, enforcement, CodeQL mutation,
  security assurance, and privacy assurance;
- report schema fields are present and deterministic enough for review;
- no live CodeQL API calls or raw SARIF reads occur.

## Codex E Review Expectations

Codex E should verify:

- the helper reads only allowed inputs;
- the report schema matches this contract;
- report statuses use the approved vocabulary;
- non-claims are present in every report;
- unsafe values are not echoed in success or failure output;
- no CI, CodeQL, parser, analytics, workbook, production, OpenAI, AI, coaching,
  or Line Tracer behavior changed;
- generated report artifacts are public-safe and repo-relative.

## Suspected Gaps

- The current validator has a text report, but no durable JSON advisory report
  artifact.
- Existing security scanners may have useful summaries, but mixing them into
  the first CWE-profile report would blur local advisory vocabulary with actual
  security findings. Keep that deferred.
- The parent CodeQL workflow still needs to remain the only place that speaks
  about CodeQL alert lifecycle state.

## Acceptance Criteria

The #603 implementation should be accepted only if:

- the report helper exists and is covered by focused tests;
- the generated report follows the schema and status vocabulary above;
- the helper consumes only allowed inputs;
- unsafe text is blocked or redacted without echoing raw values;
- the report includes required non-claims;
- validation passes;
- Codex E confirms advisory-only status and protected-surface preservation.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/603

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Base branch:
main

Contract:
docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md

Goal:
Implement the advisory CWE-mapped local validation profile report helper and
produce the implementation handoff:
docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md

Read the contract, the #597 profile manifest, validator, tests, handoff, and
contract-test report. Compare the current code to the contract before editing.

Implement only:
- a public-safe advisory JSON report helper;
- focused tests for the helper;
- any intentional public-safe report artifact required by the contract;
- the implementation handoff.

The first helper must consume only:
- docs/security/cwe_mapped_local_validation_profile.v1.json;
- tools/check_cwe_mapped_local_validation_profile.py validator results;
- public repo metadata such as ref/commit and source issue URLs.

Do not consume local scanner outputs, raw SARIF, CodeQL API responses, private
artifacts, raw logs, local app data, SQLite contents, secrets, endpoint values,
workbook exports, generated/private/local-only artifacts, or arbitrary user
files.

Do not change CI, enable enforcement, mutate CodeQL alerts, claim CodeQL
closure, claim formal CWE compliance, claim security/privacy assurance, claim
release readiness, or claim deploy readiness.

Do not change parser behavior, parser truth ownership, analytics schema,
workbook behavior, Apps Script behavior, production behavior, OpenAI/model-
provider behavior, AI/coaching behavior, or Line Tracer behavior.

Validation expected:
- py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py
- focused tests for the new report helper
- py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
- py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
- run the new helper and validate the produced JSON
- py -m ruff check on changed Python tool/test files
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

End with the implementation handoff, validation results, remaining risks, next
recommended role Codex E, and a workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/603"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifacts:
    - "docs/contracts/security_cwe_mapped_local_validation_profile.md"
    - "docs/security/cwe_mapped_local_validation_profile.v1.json"
    - "tools/check_cwe_mapped_local_validation_profile.py"
    - "tests/test_cwe_mapped_local_validation_profile.py"
    - "docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_tooling.md"
    - "docs/contract_test_reports/security_cwe_mapped_local_validation_profile.md"
  contract_artifact: "docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md"
  target_artifact: "docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md"
  expected_report_path: "docs/quality_reports/security/cwe_mapped_local_validation_profile/<YYYY-MM-DD>-<short-commit>-cwe-profile-advisory-report.json"
  branch: "codex/cwe-profile-advisory-report-603"
  base_branch: "main"
  risk_tier: "High workflow and security-communication risk; low runtime risk"
  decision: "First report helper should consume only the CWE profile manifest, validator result, and public repo metadata. Scanner summaries remain deferred unless a later contract authorizes public-safe aggregation."
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not change CI or enable enforcement."
    - "Do not mutate CodeQL alerts or claim CodeQL closure."
    - "Do not claim formal CWE compliance, security assurance, privacy assurance, release readiness, deploy readiness, or production readiness."
    - "Do not read private artifacts, raw logs, local app data, SQLite contents, raw SARIF, secrets, endpoint values, workbook exports, failed-post queue artifacts, or local-only scanner outputs."
    - "Do not change parser/runtime/analytics/workbook/App Script/production/OpenAI/AI/coaching/Line Tracer behavior."
```
