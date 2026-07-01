# Security Quality Scanner Summary Aggregation Contract

## Module

`security_quality_scanner_summary_aggregation`

Plain English: this contract defines a safe summary layer for Mythic Edge's
security and quality scanner signals. It lets a future helper summarize
CodeQL lifecycle state, the advisory CWE profile report, protected-surface
scanner results, and secret/private-marker scanner results without pretending
that those signals prove the repo is secure, private, release-ready, or
production-ready.

This is a Codex B contract artifact only. It does not implement code, change
CI, enable enforcement, mutate GitHub CodeQL alerts, read private artifacts, or
weaken any scanner.

## Source Issue

- Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/610
- Parent security workflow:
  https://github.com/Tahjali11/Mythic-Edge/issues/330
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Prior advisory report issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/603
- Prior advisory report PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/607
- Contract artifact:
  `docs/contracts/security_quality_scanner_summary_aggregation.md`

## Tracker

Parent security workflow #330 remains open. Project roadmap #568 remains the
cross-workflow roadmap anchor.

## Owning Layer

Quality / Governance security reporting.

The aggregate summary owns only a public-safe status summary of security and
quality signals. It does not own scanner truth, CodeQL alert lifecycle truth,
parser truth, vulnerability truth, release readiness, deployment readiness, or
security/privacy assurance.

## Internal Project Area

Quality / Governance.

Adjacent areas:

- Security-quality reporting;
- External / Collaboration Surface for GitHub CodeQL status;
- Generated / Local Artifacts for scanner inputs that must not be read or
  copied;
- Parser and local app only as protected surfaces that this contract must not
  change.

## Truth Owner

Truth ownership is intentionally split:

- GitHub CodeQL/code scanning owns live CodeQL alert lifecycle state.
- `tools/check_cwe_mapped_local_validation_profile.py` owns local CWE profile
  manifest validation results.
- `tools/generate_cwe_profile_advisory_report.py` owns the existing advisory
  CWE profile report schema.
- `tools/check_protected_surfaces.py` owns protected-surface path
  classification results.
- `tools/check_secret_patterns.py` owns secret/private-marker scan results.
- This aggregate summary owns only the public-safe composition of those
  summaries and must preserve source boundaries in every row.

The aggregate summary must never convert local scanner success into security
assurance, privacy assurance, CodeQL closure, release readiness, deploy
readiness, parser truth, analytics truth, AI truth, or coaching truth.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
live or provided CodeQL summary
  + CWE profile advisory report
  + protected-surface scanner summary
  + secret/private-marker scanner summary
  -> public-safe aggregate security-quality summary report
  -> Codex review / tracker / release-readiness discussion as advisory evidence
```

Forbidden reverse flow:

- Aggregate summary output must not mutate CodeQL alerts.
- Aggregate summary output must not change scanner behavior.
- Aggregate summary output must not weaken scanner categories, redaction, or
  exit-code behavior.
- Aggregate summary output must not change parser, analytics, workbook,
  webhook, Apps Script, Google Sheets, OpenAI, AI, coaching, or production
  behavior.

## Files Owned By This Contract

This contract owns the future report boundary for:

- `docs/contracts/security_quality_scanner_summary_aggregation.md`
- Future implementation handoff:
  `docs/implementation_handoffs/security_quality_scanner_summary_aggregation_comparison.md`
- Future contract-test report:
  `docs/contract_test_reports/security_quality_scanner_summary_aggregation.md`

Future implementation may add, if authorized by Codex C under this contract:

- `tools/generate_security_quality_summary.py`
- focused tests for the helper;
- a public-safe report artifact under:
  `docs/quality_reports/security/security_quality_summary/`

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #610
- parent issue #330
- project roadmap #568
- `docs/contracts/security_cwe_mapped_local_validation_profile.md`
- `docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md`
- `docs/security/cwe_mapped_local_validation_profile.v1.json`
- `docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json`
- `tools/check_cwe_mapped_local_validation_profile.py`
- `tools/generate_cwe_profile_advisory_report.py`
- `tools/check_protected_surfaces.py`
- `tools/check_secret_patterns.py`

## Observed Current Behavior

- Issue #610 is open and asks for a contract-only boundary for aggregate
  security-quality summaries.
- Parent #330 remains open for broader CodeQL remediation and prevention
  workflow.
- Issue #603 / PR #607 completed the public-safe advisory CWE profile report
  helper.
- The current advisory CWE report has:
  - `schema_version:
    security_cwe_mapped_local_validation_profile_advisory_report.v1`;
  - `overall_status: passed_advisory`;
  - `advisory_only: true`;
  - `enforcement_authorized: false`;
  - `ci_change_authorized: false`;
  - `codeql_alert_mutation_authorized: false`;
  - `security_assurance_claimed: false`;
  - `privacy_assurance_claimed: false`.
- The issue #610 problem representation records that Codex A observed live
  CodeQL API access working and open CodeQL alerts on `refs/heads/main` as
  `0` at issue creation time.
- This Codex B pass did not refresh live CodeQL alert state or read raw CodeQL
  payloads. A future implementation/review thread must refresh any live CodeQL
  counts before using them as current lifecycle evidence.

## Contract Summary

The first aggregate summary should be a public-safe, advisory JSON report. It
may combine symbolic summaries from:

1. GitHub CodeQL/code-scanning lifecycle state;
2. the existing CWE-mapped local validation profile advisory report;
3. protected-surface scanner result summary;
4. secret/private-marker scanner result summary;
5. optional repo-check or CI status as workflow evidence only.

The report must keep each source separate. It must say where each signal came
from, what ref or commit it applies to, when it was collected or provided, and
whether it is fresh, stale, missing, or unsupported.

The first implementation may be authorized after this contract, but only as a
report helper and tests. It must remain advisory-only and must not change CI or
scanner behavior.

## Allowed Scanner And Status Inputs

### CodeQL Status Input

Preferred source for live CodeQL state:

- a read-only GitHub code-scanning API query that extracts only safe summary
  fields; or
- a Codex G-provided lifecycle summary copied from a verified GitHub closeout
  or tracker comment.

Safe CodeQL fields:

- `source: github_code_scanning`
- `repository`
- `repository_url`
- `ref`
- `analysis_commit` or `measured_commit`
- `queried_at_policy` or `provided_at_policy`
- `state_counts`, such as open/fixed/dismissed counts
- `severity_counts`, if available without raw payloads
- symbolic `rule_id` counts, if available without paths, snippets, messages,
  or raw alert bodies
- `tool_name`, such as CodeQL
- `workflow_run_url` or analysis URL, if public-safe
- `freshness_status`

The aggregate summary must label CodeQL state as live GitHub lifecycle
evidence when it comes directly from GitHub, or as manually provided lifecycle
evidence when it is supplied by Codex G.

The first helper may support either:

- `--codeql-summary <path>` that accepts a public-safe summary JSON file using
  this contract's allowed CodeQL fields; or
- `--codeql-state-source none` and mark CodeQL as `not_collected`.

The helper should not make live GitHub API calls in the first slice unless
Codex C explicitly documents the exact query, limits the output to safe fields,
and adds tests or dry-run evidence proving raw alert payloads are not persisted
or echoed.

### CWE Advisory Report Input

Allowed input:

- `docs/quality_reports/security/cwe_mapped_local_validation_profile/<report>.json`

Allowed fields:

- `schema_version`
- `report_id`
- `repository`
- `repository_url`
- `measured_ref`
- `measured_commit`
- `overall_status`
- `profile_status`
- `profile_family_count`
- `validator.result`
- `validator.exit_code`
- `validator.errors_count`
- `validator.warnings_count`
- `advisory_only`
- `enforcement_authorized`
- `ci_change_authorized`
- `codeql_alert_mutation_authorized`
- `security_assurance_claimed`
- `privacy_assurance_claimed`
- family IDs and primary CWE IDs only when copied from the existing public-safe
  report

The aggregate summary must not reclassify CWE profile findings. It may only
summarize the existing advisory report status and link to the report artifact.

### Protected-Surface Scanner Input

Allowed source:

- `tools/check_protected_surfaces.py` result summary, preferably produced by a
  current run against a named base such as `origin/main`.

Allowed fields:

- `tool: tools/check_protected_surfaces.py`
- `mode`, such as changed-path scan or paths-from-stdin
- `base`
- `head`
- `scanned_paths` or `changed_paths` count
- `forbidden` count
- `warnings` count
- `result`
- optional symbolic category counts, if implemented without exposing paths

Forbidden from this source:

- raw command output containing full finding lines;
- private paths;
- raw local paths;
- raw snippets;
- path lists when those paths are not repo-relative and public-safe.

### Secret/Private-Marker Scanner Input

Allowed source:

- `tools/check_secret_patterns.py` result summary, preferably produced by a
  current changed-path or path-fed run against a named base such as
  `origin/main`.

Allowed fields:

- `tool: tools/check_secret_patterns.py`
- `mode`
- `base`
- `head`
- `scanned_paths`
- `skipped_paths`
- `forbidden` count
- `warnings` count
- `result`
- optional symbolic category counts, if implemented without excerpts,
  line numbers, or file contents

Forbidden from this source:

- finding excerpts;
- raw lines;
- raw Player.log content;
- raw private paths;
- raw hashes;
- raw secret-like values;
- endpoint values;
- local-only all-repo scanner dumps.

### Optional Repo-Check Or CI Status Input

Optional workflow evidence may be included only as status metadata:

- workflow name;
- run URL;
- conclusion;
- commit;
- branch/ref;
- collected timestamp;
- whether it is current, stale, missing, or not collected.

Repo-check or CI status must not be labeled as security assurance, privacy
assurance, release readiness, deploy readiness, or CodeQL closure.

## Forbidden Inputs

The aggregate helper and report must not read, parse, embed, summarize, or link
to:

- raw SARIF;
- raw CodeQL API payloads;
- raw CodeQL alert messages, locations, code flows, snippets, or descriptions;
- private evidence packets;
- raw Player.log or UTC_Log files;
- local app data;
- SQLite databases or SQLite contents;
- secrets, credentials, API keys, tokens, endpoint values, webhook URLs,
  spreadsheet IDs, or environment values;
- workbook exports;
- failed-post payloads;
- runtime logs;
- private decklists;
- arbitrary user files;
- generated/private artifacts;
- local-only scanner output files;
- raw protected-surface or secret/private-marker finding lists.

If an input contains forbidden fields or unsafe text, the helper must fail
closed with `blocked_unsafe_input` and must not echo the unsafe value.

## CodeQL Lifecycle Boundary

CodeQL status must remain separate from local advisory scanner state.

Allowed CodeQL status vocabulary:

- `not_collected`
- `provided_by_codex_g`
- `queried_live_summary`
- `stale`
- `blocked_unavailable`
- `blocked_unsafe_input`

Allowed CodeQL lifecycle fields:

- `open_count`
- `fixed_count`
- `dismissed_count`
- `severity_counts`
- `rule_id_counts`
- `ref`
- `analysis_commit`
- `queried_at_policy`
- `source_url`
- `freshness_status`

The aggregate summary must not:

- dismiss, reopen, close, or mutate CodeQL alerts;
- claim CodeQL closure unless the report cites current GitHub lifecycle
  evidence and still labels it as CodeQL lifecycle state only;
- treat local scanner success as CodeQL success;
- treat CodeQL `open_count: 0` as security assurance or privacy assurance.

## Local Scanner Summary Boundary

Local scanner summaries are advisory validation evidence. They are useful for
workflow routing, but they are not equivalent to live CodeQL alert state.

Allowed local scanner source states:

- `not_collected`
- `collected_current`
- `provided_summary`
- `stale`
- `blocked_unsafe_input`
- `blocked_tool_unavailable`
- `failed`

The report should preserve each scanner's own result. For example:

- a protected-surface result of `passed` means the scoped path set had no
  forbidden or warning classifications under that tool's rules;
- a secret/private-marker result of `failed` means the scanner found forbidden
  items in the scoped path set or hit an error;
- neither result proves repository security, privacy safety, release
  readiness, or parser correctness.

## Report Schema Recommendation

Future implementation should write intentional durable reports under:

`docs/quality_reports/security/security_quality_summary/`

Recommended filename pattern:

`<YYYY-MM-DD>-<short-commit>-security-quality-summary.json`

Recommended top-level schema:

```json
{
  "schema_version": "security_quality_scanner_summary_aggregation.v1",
  "report_id": "security-quality-summary:<short-commit>:<date>",
  "repository": "Tahjali11/Mythic-Edge",
  "repository_url": "https://github.com/Tahjali11/Mythic-Edge",
  "source_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/610",
  "parent_security_workflow": "https://github.com/Tahjali11/Mythic-Edge/issues/330",
  "project_roadmap": "https://github.com/Tahjali11/Mythic-Edge/issues/568",
  "contract_ref": "docs/contracts/security_quality_scanner_summary_aggregation.md",
  "measured_ref": "<branch-or-ref>",
  "measured_commit": "<commit>",
  "generated_at_policy": "date_only_or_utc_timestamp_without_local_paths",
  "overall_status": "advisory_passed",
  "freshness_status": "current",
  "sources": [],
  "codeql": {},
  "cwe_profile_report": {},
  "protected_surface_scan": {},
  "secret_private_marker_scan": {},
  "ci_or_repo_check_status": {},
  "blocked_inputs": [],
  "non_claims": [],
  "privacy_redaction": {},
  "advisory_only": true,
  "enforcement_authorized": false,
  "ci_change_authorized": false,
  "codeql_alert_mutation_authorized": false,
  "security_assurance_claimed": false,
  "privacy_assurance_claimed": false,
  "release_readiness_claimed": false,
  "deploy_readiness_claimed": false,
  "parser_truth_claimed": false,
  "analytics_truth_claimed": false,
  "ai_truth_claimed": false,
  "coaching_truth_claimed": false,
  "validation_commands": [],
  "next_recommended_role": "Codex E"
}
```

Allowed `overall_status` values:

- `advisory_passed`
- `advisory_warnings`
- `advisory_failed`
- `partial_missing_sources`
- `blocked_unsafe_input`
- `blocked_unsupported_mode`
- `blocked_tool_unavailable`

Allowed `freshness_status` values:

- `current`
- `stale`
- `mixed`
- `not_collected`
- `unknown`

Required source fields for each source summary:

- `source_id`
- `source_type`
- `status`
- `tool_or_authority`
- `measured_ref`
- `measured_commit`
- `collected_at_policy`
- `freshness_status`
- `result`
- `counts`
- `public_safe`
- `raw_payload_included`
- `local_private_data_included`
- `notes`

`raw_payload_included` and `local_private_data_included` must be `false` for
accepted report sources.

## Stale Evidence Policy

Scanner evidence must be labeled stale when:

- the measured commit differs from the aggregate report commit;
- the measured ref is not the report's target ref;
- the report is copied from an older PR/branch without refresh evidence;
- CodeQL state came from issue comments rather than a current live query or
  Codex G closeout;
- scanner command output does not name the base/head/ref;
- the helper cannot determine freshness.

Stale evidence may still be included as historical context if it is
public-safe, but it must not drive closure, readiness, or assurance language.

If evidence is mixed, the report must use `freshness_status: mixed` and list
which sources are stale or not collected.

## Advisory Versus Blocking Boundary

The aggregate summary is advisory-only.

It may:

- collect public-safe summaries;
- identify missing or stale evidence;
- route follow-up work to Codex A, B, C, E, F, or G;
- help Codex G write tracker updates;
- recommend that a future issue consider enforcement.

It must not:

- change CI;
- add a required gate;
- fail a release by itself;
- claim security assurance or privacy assurance;
- close CodeQL alert lifecycle work;
- mutate GitHub alerts;
- weaken scanners;
- create public security disclosure details;
- make parser, analytics, AI, coaching, release, deploy, or production truth
  claims.

Any future blocking use requires a new issue, problem representation, contract,
explicit user approval, fresh evidence, and rollback plan.

## Error Behavior

The helper must fail closed when:

- a source file is missing and the source is required;
- a source schema is unknown;
- a source includes raw payload fields;
- a source includes private/local-only paths or secret-like text;
- a live CodeQL query mode is requested without explicit support;
- scanner output cannot be parsed into allowed summary fields;
- measured ref or commit cannot be determined.

Failure output must be symbolic. It may include source IDs, safe status labels,
counts, and repo-relative artifact paths. It must not echo raw unsafe input.

## Side Effects

Codex B side effects:

- creates this docs contract only.

Future Codex C side effects, if authorized:

- may create a report helper;
- may create focused tests;
- may write one intentional public-safe JSON report artifact under
  `docs/quality_reports/security/security_quality_summary/`;
- may create an implementation handoff.

Forbidden side effects:

- CI changes;
- CodeQL alert mutation;
- scanner policy weakening;
- external writes;
- credential or OAuth changes;
- private artifact reads or writes;
- runtime, parser, analytics, workbook, webhook, Apps Script, Sheets, OpenAI,
  AI, coaching, Line Tracer, or production behavior changes.

## Validation Requirements

Codex C should validate a future helper with:

```powershell
py -m pytest -q tests\test_security_quality_summary.py
py -m pytest -q tests\test_cwe_profile_advisory_report.py tests\test_cwe_mapped_local_validation_profile.py
py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
py -m json.tool docs\quality_reports\security\cwe_mapped_local_validation_profile\2026-07-01-024eda7-cwe-profile-advisory-report.json
py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
py -m ruff check tools\generate_security_quality_summary.py tests\test_security_quality_summary.py
git diff --check
py tools\check_agent_docs.py
```

Codex C must also run path-scoped scans over changed files:

```powershell
@'
docs/contracts/security_quality_scanner_summary_aggregation.md
tools/generate_security_quality_summary.py
tests/test_security_quality_summary.py
docs/implementation_handoffs/security_quality_scanner_summary_aggregation_comparison.md
docs/quality_reports/security/security_quality_summary/<report>.json
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin

@'
docs/contracts/security_quality_scanner_summary_aggregation.md
tools/generate_security_quality_summary.py
tests/test_security_quality_summary.py
docs/implementation_handoffs/security_quality_scanner_summary_aggregation_comparison.md
docs/quality_reports/security/security_quality_summary/<report>.json
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Codex C should omit nonexistent paths from path-scoped scans.

Focused tests must prove:

- allowed summary inputs produce the expected JSON shape;
- raw CodeQL-like payload fields are rejected or ignored safely;
- raw SARIF-looking input is blocked;
- private local paths are not echoed;
- secret-like values are not echoed;
- raw scanner finding excerpts are not included;
- stale source evidence is labeled stale;
- CodeQL lifecycle state remains separate from local advisory scanner state;
- all non-claim booleans remain false;
- no live GitHub call is made unless explicitly supported and tested.

## Codex E Review Requirements

Codex E should verify:

- the helper reads only allowed inputs;
- CodeQL status, CWE advisory report status, protected-surface summary, and
  secret/private-marker summary remain separate;
- every source has ref/commit/freshness labeling;
- no raw payloads, raw findings, private paths, snippets, secrets, endpoints,
  local app data, SQLite contents, or local-only outputs appear in reports;
- reports include required non-claims;
- no CI, enforcement, CodeQL mutation, scanner weakening, parser, analytics,
  workbook, webhook, Apps Script, Sheets, OpenAI, AI, coaching, Line Tracer,
  or production behavior changed;
- stale evidence cannot be used as closure/readiness evidence.

## Protected-Surface Assessment

This contract does not touch protected runtime surfaces.

Future implementation may touch quality/reporting helpers and tests only.
Protected parser, runtime, analytics, workbook, webhook, Apps Script, Sheets,
OpenAI, AI, coaching, Line Tracer, production, fixture, corpus, generated data,
raw log, and private artifact surfaces remain out of scope.

This contract does not weaken:

- `tools/check_protected_surfaces.py`;
- `tools/check_secret_patterns.py`;
- `tools/check_cwe_mapped_local_validation_profile.py`;
- existing CodeQL or GitHub workflow behavior.

## Acceptance Criteria

Codex C satisfies this contract only when:

- `docs/implementation_handoffs/security_quality_scanner_summary_aggregation_comparison.md`
  exists;
- any helper reads only allowed public-safe inputs;
- any report artifact follows
  `security_quality_scanner_summary_aggregation.v1`;
- every source is labeled by source type, ref/commit, freshness, and advisory
  status;
- CodeQL lifecycle state is not conflated with local scanner state;
- unsafe inputs fail closed without echoed raw values;
- validation passes;
- Codex E can review the aggregate report without private or local-only data.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer.

Codex C should implement only the advisory report helper, focused tests, and
implementation handoff if the user wants this contract implemented next.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/610

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/security-summary-aggregation-330

Contract:
docs/contracts/security_quality_scanner_summary_aggregation.md

Goal:
Compare the current CWE advisory report helper, profile validator,
protected-surface scanner, secret/private-marker scanner, and issue #610
requirements against the contract. If the contract matches current repo state,
implement the public-safe advisory aggregate summary helper and focused tests.

Expected implementation handoff:
docs/implementation_handoffs/security_quality_scanner_summary_aggregation_comparison.md

Do:
- Implement only an advisory report helper, focused tests, and the
  implementation handoff.
- Keep CodeQL lifecycle state separate from local scanner state.
- Use only public-safe symbolic summaries, counts, refs, commits, statuses,
  and non-claim fields.
- Label stale or missing evidence clearly.
- Keep the report advisory-only.

Do not:
- Change CI.
- Enable enforcement.
- Mutate, dismiss, reopen, or close CodeQL alerts.
- Read raw SARIF, raw CodeQL payloads, raw scanner finding lists, private
  evidence, raw Player.log files, local app data, SQLite contents, secrets,
  endpoint values, workbook exports, failed-post payloads, runtime logs,
  private decklists, arbitrary user files, generated/private artifacts, or
  local-only scanner outputs.
- Claim formal CWE compliance, security assurance, privacy assurance, release
  readiness, deploy readiness, production readiness, parser truth, analytics
  truth, AI truth, or coaching truth.
- Change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/
  production behavior.
- Weaken existing protected-surface or secret/private-marker scanners.

Validation expected:
- py -m pytest -q tests\test_security_quality_summary.py
- py -m pytest -q tests\test_cwe_profile_advisory_report.py tests\test_cwe_mapped_local_validation_profile.py
- py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
- py -m json.tool docs\quality_reports\security\cwe_mapped_local_validation_profile\2026-07-01-024eda7-cwe-profile-advisory-report.json
- py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
- py -m ruff check tools\generate_security_quality_summary.py tests\test_security_quality_summary.py
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Final handoff must include:
- role performed
- issue and parent workflow
- contract artifact used
- files changed
- report schema implemented
- allowed inputs implemented
- forbidden inputs blocked
- validation results
- protected-surface status
- secret/private-marker status
- remaining risks
- next recommended role: Codex E
- pasteable Codex E prompt
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/610"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifacts:
    - "GitHub issue #610"
    - "GitHub issue #330"
    - "GitHub issue #568"
    - "docs/contracts/security_cwe_mapped_local_validation_profile.md"
    - "docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md"
    - "docs/security/cwe_mapped_local_validation_profile.v1.json"
    - "docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json"
    - "tools/check_cwe_mapped_local_validation_profile.py"
    - "tools/generate_cwe_profile_advisory_report.py"
    - "tools/check_protected_surfaces.py"
    - "tools/check_secret_patterns.py"
  contract_artifact: "docs/contracts/security_quality_scanner_summary_aggregation.md"
  target_artifact: "docs/implementation_handoffs/security_quality_scanner_summary_aggregation_comparison.md"
  expected_report_path: "docs/quality_reports/security/security_quality_summary/<YYYY-MM-DD>-<short-commit>-security-quality-summary.json"
  risk_tier: "High workflow and security-communication risk; low runtime risk if advisory-only"
  branch: "codex/security-summary-aggregation-330"
  base_branch: "main"
  target_branch: "main_after_explicit_user_approval"
  decision: "Authorize a later advisory helper implementation that aggregates only public-safe symbolic summaries and keeps CodeQL lifecycle state separate from local scanner state."
  validation:
    - "git status --short --branch --untracked-files=all -> clean before contract creation"
  stop_conditions:
    - "Do not change CI or enable enforcement."
    - "Do not mutate, dismiss, reopen, or close CodeQL alerts."
    - "Do not read raw SARIF, raw CodeQL payloads, raw scanner finding lists, private evidence, raw logs, local app data, SQLite contents, secrets, endpoint values, workbook exports, failed-post payloads, runtime logs, private decklists, arbitrary user files, generated/private artifacts, or local-only scanner outputs."
    - "Do not claim formal CWE compliance, security assurance, privacy assurance, release readiness, deploy readiness, production readiness, parser truth, analytics truth, AI truth, or coaching truth."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not weaken existing protected-surface or secret/private-marker scanners."
```
