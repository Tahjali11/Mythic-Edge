# Security Quality Current Evidence Bundle Contract

## Module

`security_quality_current_evidence_bundle`

Plain English: this contract defines the evidence packet Mythic Edge needs
before any later security-quality gate policy can be discussed. It does not
create a gate. It only says what current, public-safe evidence must be present,
how each source must be labeled, and what conditions block a later gate-policy
issue.

## Source Issue

- Child issue: <https://github.com/Tahjali11/Mythic-Edge/issues/639>
- Parent security workflow:
  <https://github.com/Tahjali11/Mythic-Edge/issues/330>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/630>
- Existing aggregate contract:
  `docs/contracts/security_quality_scanner_summary_aggregation.md`
- Source report:
  `docs/quality_reports/security/security_quality_summary/2026-07-01-048e311-security-quality-summary.json`
- Source review:
  `docs/contract_test_reports/security_quality_evidence_refresh_after_local_app_hardening.md`

## Tracker

Parent security workflow #330 remains open. Project roadmap #568 remains open.

## Owning Layer

Quality / Governance security reporting.

This contract owns evidence completeness and vocabulary for public-safe
security-quality summaries. It does not own CodeQL truth, scanner truth,
security assurance, privacy assurance, release readiness, deploy readiness,
production readiness, parser truth, analytics truth, AI truth, or coaching
truth.

## Internal Project Area

Quality / Governance.

Adjacent areas:

- Security-quality reporting;
- GitHub CodeQL lifecycle evidence;
- local scanner summary evidence;
- CI/repo-check workflow evidence;
- generated report artifacts under `docs/quality_reports/security/`.

## Truth Owner

Truth ownership stays split:

- GitHub CodeQL/code scanning owns live CodeQL alert lifecycle state.
- `tools/check_cwe_mapped_local_validation_profile.py` owns CWE profile
  manifest validation results.
- `tools/generate_cwe_profile_advisory_report.py` owns the CWE advisory report
  schema.
- `tools/check_protected_surfaces.py` owns protected-surface path
  classification for the scoped paths it is asked to inspect.
- `tools/check_secret_patterns.py` owns secret/private-marker scan results for
  the scoped path set or all tracked files when `--all` is used.
- GitHub Actions owns workflow/check conclusions.
- `tools/generate_security_quality_summary.py` owns only the public-safe
  aggregation shape when given public-safe summary inputs.
- This contract owns the current evidence bundle policy and status vocabulary.

No source may be promoted into security/privacy/release/deploy/production
assurance.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
current CodeQL lifecycle counts
  + current or explicitly stale/deferred CWE advisory report
  + protected-surface scanner summary
  + secret/private-marker scanner summary
  + CI/repo-check status summary
  -> public-safe security-quality evidence bundle
  -> later Codex A/B gate-policy discussion as advisory evidence only
```

Forbidden reverse flow:

- The bundle must not mutate CodeQL alerts.
- The bundle must not change scanner behavior.
- The bundle must not change CI.
- The bundle must not weaken protected-surface or secret/private-marker rules.
- The bundle must not change parser, runtime, analytics, workbook, webhook,
  Apps Script, Sheets, OpenAI/model-provider, AI/coaching, Line Tracer, or
  production behavior.

## Files Owned By This Contract

This Codex B pass owns:

- `docs/contracts/security_quality_current_evidence_bundle.md`

This contract references but does not replace:

- `docs/contracts/security_quality_scanner_summary_aggregation.md`
- `tools/generate_security_quality_summary.py`
- `tests/test_security_quality_summary.py`
- `docs/quality_reports/security/security_quality_summary/*.json`
- `docs/contract_test_reports/security_quality_evidence_refresh_after_local_app_hardening.md`

Future Codex C may create, if explicitly routed:

- `docs/implementation_handoffs/security_quality_current_evidence_bundle_comparison.md`
- a current advisory report under:
  `docs/quality_reports/security/security_quality_summary/`
- optional temporary public-safe summary JSON inputs outside the repo or under
  a Codex C-approved ignored scratch path, if needed by the existing helper.

Temporary summary inputs must not be committed unless a future contract
explicitly makes them durable public-safe artifacts.

## Artifact Path Decision

Codex B chooses a new contract path:

`docs/contracts/security_quality_current_evidence_bundle.md`

Reason:

- `security_quality_scanner_summary_aggregation.md` remains the generic helper
  and schema contract.
- #639 is narrower: it defines what must be current and complete before a
  later gate-policy issue.
- Updating #610's contract would blur helper behavior with gate-policy
  readiness vocabulary.

## Observed Current Behavior

Issue #630 produced a public-safe advisory report:

- schema: `security_quality_scanner_summary_aggregation.v1`
- report:
  `docs/quality_reports/security/security_quality_summary/2026-07-01-048e311-security-quality-summary.json`
- measured commit:
  `048e31146f185840f032ec3ff45f93e6822b8fce`
- overall status: `advisory_warnings`
- freshness status: `mixed`
- advisory only: `true`
- enforcement authorized: `false`
- CI change authorized: `false`
- CodeQL alert mutation authorized: `false`
- security/privacy/release/deploy/production/parser/analytics/AI/coaching
  claims: all `false`

The #630 report sources were:

| Source | Status | Freshness | Result |
| --- | --- | --- | --- |
| CodeQL | `provided_by_codex_g` | `current` | `provided_summary` |
| CWE profile report | `stale` | `stale` | `passed_advisory` |
| Protected-surface scan | `not_collected` | `not_collected` | `not_collected` |
| Secret/private-marker scan | `not_collected` | `not_collected` | `not_collected` |
| CI/repo-check status | `not_collected` | `not_collected` | `not_collected` |

The #630 contract-test report recorded two non-blocking gaps:

- the issue-specific implementation handoff artifact was absent;
- CodeQL source-state vocabulary was imprecise because the source was a Codex A
  public-safe lifecycle summary, while the report used `provided_by_codex_g`.

This Codex B pass performed a count-only live CodeQL readback for
`refs/heads/main` and observed:

```yaml
codeql_lifecycle_counts:
  open: 0
  fixed: 3
  dismissed: 14
```

This is lifecycle evidence only. It is not security assurance, privacy
assurance, release readiness, deploy readiness, production readiness, or
CodeQL alert mutation.

## Existing Aggregation Contract Suitability

The existing #610 contract and helper can safely represent the current evidence
bundle if Codex C provides only public-safe summary inputs.

Supported helper inputs include:

- `--codeql-state-source summary-file --codeql-summary <public-safe-json>`
- `--cwe-report <public-safe-cwe-report-json>`
- `--protected-surface-summary <public-safe-json>`
- `--secret-private-summary <public-safe-json>`
- `--ci-summary <public-safe-json>`

The helper must not ingest raw CodeQL payloads, raw SARIF, raw scanner finding
lists, snippets, raw private paths, or local-only outputs. Codex C should use
temporary public-safe summary files when needed, and commit only the final
public-safe report unless a later contract authorizes durable source-summary
artifacts.

If Codex C discovers that the helper cannot represent a required current
source without unsafe input handling, Codex C must stop and route back to
Codex B.

## Evidence Bundle Scope

A complete current evidence bundle must include one row for each source:

1. CodeQL lifecycle counts for `refs/heads/main`.
2. CWE mapped local validation profile advisory report.
3. Protected-surface scanner summary.
4. Secret/private-marker scanner summary.
5. CI/repo-check status summary.

Each row must identify:

- `source_id`
- `source_type`
- `authority_or_tool`
- `measured_ref`
- `measured_commit`
- `collected_at_policy`
- `freshness_status`
- `source_status`
- `result`
- `counts`
- `public_safe`
- `raw_payload_included`
- `local_private_data_included`
- `non_claims`
- `notes`

`raw_payload_included` and `local_private_data_included` must be `false` for
every accepted source row.

## Source Requirements

### CodeQL Lifecycle Counts

Required before gate-policy discussion:

- current count-only readback for `refs/heads/main`;
- at minimum: open, fixed, and dismissed counts;
- collection method labeled as `queried_live_count_only`,
  `provided_by_codex_g`, or `provided_public_summary`;
- ref and collection date policy;
- explicit non-claim that CodeQL open `0` is lifecycle evidence only.

Safe fields:

- `repository`
- `repository_url`
- `ref`
- `measured_commit` or `analysis_commit`
- `state_counts`
- optional severity/rule counts if already summarized without alert payloads
- `tool_name`
- `source_url`
- `freshness_status`

Block later gate-policy discussion if:

- open CodeQL count is greater than `0`;
- CodeQL counts cannot be collected safely;
- the report would need raw alert payloads, snippets, locations, code flows, or
  SARIF to represent the source;
- CodeQL lifecycle state is stale relative to the intended base.

### CWE Mapped Local Validation Profile

Required before gate-policy discussion:

- current advisory CWE profile report measured at the intended base commit; or
- explicit `stale` / `deferred` status with a blocker explaining why a current
  report cannot be produced yet.

Safe fields:

- schema version;
- measured ref and commit;
- overall status;
- validator result;
- errors and warnings counts;
- profile family count;
- family IDs and CWE IDs already present in the public-safe report;
- advisory-only and non-claim flags.

Block later gate-policy discussion if:

- the CWE report is stale and no current report is produced;
- the CWE validator fails with errors;
- report generation requires raw/private data;
- any output claims formal CWE compliance.

### Protected-Surface Scanner Summary

Required before gate-policy discussion:

- a current protected-surface scanner summary for the evidence-bundle changed
  path set at minimum; and
- if a future gate policy would rely on broader protected-surface status, an
  explicit follow-up must define a broader safe measurement method because
  `tools/check_protected_surfaces.py` is currently a diff/path-scoped checker.

Safe fields:

- tool name;
- mode, such as `paths_from_stdin` or `diff_against_base`;
- base;
- head;
- changed/scanned path count;
- forbidden count;
- warnings count;
- result;
- optional symbolic category counts if implemented without raw paths or
  snippets.

Block later gate-policy discussion if:

- forbidden count is greater than `0`;
- warnings are not explained or routed;
- the scanner cannot summarize without raw finding lists or private paths;
- the intended gate policy assumes all-repo protected-surface coverage from a
  checker that only measured a diff or supplied path set.

### Secret / Private-Marker Scanner Summary

Required before gate-policy discussion:

- current changed-path/path-fed scan over any bundle artifacts; and
- a current all-tracked-files advisory scan summary if the gate policy would
  claim repo-wide private-artifact readiness.

Safe fields:

- tool name;
- mode, such as `paths_from_stdin`, `diff_against_base`, or `all_tracked_files`;
- base/head when applicable;
- scanned path count;
- skipped path count;
- forbidden count;
- warnings count;
- result;
- optional symbolic category counts when they do not expose values, paths,
  line numbers, hashes, excerpts, or private markers.

Block later gate-policy discussion if:

- forbidden count is greater than `0`;
- warnings are unexplained;
- output cannot be summarized without raw values, excerpts, private paths,
  hashes, endpoint values, or local-only artifacts;
- all-repo advisory findings are treated as release/security assurance rather
  than triage evidence.

### CI / Repo-Check Status Summary

Required before gate-policy discussion:

- current status for GitHub CodeQL and Repo Checks on the intended base or
  evidence-bundle PR;
- local validation command results for the evidence-bundle branch;
- freshness label explaining whether checks correspond to the same commit as
  the report.

Safe fields:

- workflow/check name;
- conclusion;
- commit;
- branch or ref;
- run URL when public-safe;
- collected date policy;
- freshness status.

Block later gate-policy discussion if:

- required GitHub checks are failing on the evidence-bundle PR or intended base;
- check state is missing and not intentionally deferred;
- local validation fails for the report artifact;
- CI status is used as a security/privacy assurance claim.

## Public-Safe Summary Rules

Allowed content:

- symbolic statuses;
- counts;
- booleans;
- dates or UTC timestamps that do not include local paths;
- public issue, PR, workflow, and report links;
- public commit IDs;
- repo-relative paths for intentional report artifacts;
- tool names and command names;
- non-claim booleans.

Forbidden content:

- raw SARIF;
- raw CodeQL payloads;
- raw CodeQL alert messages, locations, snippets, code flows, or descriptions;
- raw protected-surface or secret/private-marker finding lists;
- raw scanner excerpts;
- raw Player.log or UTC_Log content;
- raw JSONL payloads;
- SQLite contents;
- local app data;
- workbook exports;
- failed-post payloads;
- runtime logs;
- private decklists;
- local absolute paths;
- endpoint values, webhook URLs, spreadsheet IDs, environment values, secrets,
  credentials, API keys, or tokens;
- raw hashes or fingerprints;
- arbitrary user files;
- local-only scanner output files.

If an input includes forbidden content, the report must fail closed with a
symbolic blocked status and must not echo the unsafe value.

## Status Vocabulary

Source collection statuses:

- `collected_current`
- `provided_public_summary`
- `queried_live_count_only`
- `stale`
- `not_collected`
- `not_applicable`
- `deferred_with_reason`
- `blocked_unsafe_input`
- `blocked_tool_unavailable`
- `blocked_schema_unknown`
- `failed`

Evidence bundle overall statuses:

- `complete_advisory_bundle`
- `complete_with_advisory_warnings`
- `incomplete_missing_sources`
- `blocked_current_open_codeql`
- `blocked_scanner_forbidden`
- `blocked_unsafe_input`
- `blocked_tool_unavailable`
- `blocked_validation_failure`

Freshness statuses:

- `current`
- `mixed`
- `stale`
- `not_collected`
- `unknown`

## Blocker / Advisory / Watch-List Vocabulary

### Blocker

Use `blocker` when evidence prevents later gate-policy consideration until a
follow-up resolves it.

Examples:

- current CodeQL open count greater than `0`;
- scanner forbidden count greater than `0`;
- required source cannot be summarized safely;
- raw/private values appear in a report;
- current report cannot be generated without unsafe inputs;
- required GitHub or local validation fails;
- helper or scanner would need weakening to produce the bundle.

### Advisory

Use `advisory` when evidence is useful but does not itself block the repo from
continuing normal scoped work.

Examples:

- CodeQL open `0` lifecycle counts;
- scanner warnings that are explained and routed;
- stale source explicitly carried as historical context;
- branch/diff-scoped scanner results;
- all-repo private-marker advisory findings that need triage but are not
  committed as raw data in the bundle.

### Watch List

Use `watch_list` when a pattern needs tracking but is not yet actionable as a
blocker.

Examples:

- repeated not-collected source families;
- CodeQL lifecycle drift after future merges;
- missing public-safe scanner summary producer;
- imprecise source vocabulary, such as #630's `provided_by_codex_g` label for
  a Codex A-supplied summary;
- lack of all-repo protected-surface summary support.

### Deferred

Use `deferred_with_reason` only when the bundle names why the source is not
required for the current advisory evidence step and identifies what issue or
contract should handle it later.

## Advisory-Only Boundary

This contract remains advisory-only.

It may:

- define evidence completeness;
- route missing sources to follow-up work;
- recommend Codex C report execution;
- block later gate-policy discussion when evidence is incomplete or unsafe.

It must not:

- change CI;
- create a required gate;
- mutate CodeQL alerts;
- claim security assurance;
- claim privacy assurance;
- claim release readiness;
- claim deploy readiness;
- claim production readiness;
- claim parser, analytics, AI, or coaching truth;
- weaken protected-surface, secret/private-marker, CodeQL, CWE, or CI checks.

Any future security-quality gate requires a new issue, problem representation,
contract, explicit user approval, fresh current evidence, rollback plan, and
Codex E/G review.

## Validation Requirements

Codex C report execution should run:

```powershell
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
```

Codex C should collect CodeQL counts with count-only output and no raw payload
persistence:

```powershell
gh api '/repos/Tahjali11/Mythic-Edge/code-scanning/alerts?state=open&ref=refs/heads/main&per_page=100' --jq 'length'
gh api '/repos/Tahjali11/Mythic-Edge/code-scanning/alerts?state=fixed&ref=refs/heads/main&per_page=100' --jq 'length'
gh api '/repos/Tahjali11/Mythic-Edge/code-scanning/alerts?state=dismissed&ref=refs/heads/main&per_page=100' --jq 'length'
```

Codex C should validate or refresh CWE evidence:

```powershell
py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
py tools\generate_cwe_profile_advisory_report.py --write-report --report-date <YYYY-MM-DD>
py -m json.tool docs\quality_reports\security\cwe_mapped_local_validation_profile\<current-report>.json
```

Codex C should validate the aggregate helper and report:

```powershell
py -m pytest -q tests\test_security_quality_summary.py
py -m pytest -q tests\test_cwe_profile_advisory_report.py tests\test_cwe_mapped_local_validation_profile.py
py -m ruff check tools\generate_security_quality_summary.py tests\test_security_quality_summary.py
py tools\generate_security_quality_summary.py --report-date <YYYY-MM-DD> --write-report <plus public-safe summary inputs as needed>
py -m json.tool docs\quality_reports\security\security_quality_summary\<current-report>.json
git diff --check
py tools\check_agent_docs.py
```

Codex C must run path-scoped safety scans over changed files:

```powershell
@'
docs/contracts/security_quality_current_evidence_bundle.md
docs/implementation_handoffs/security_quality_current_evidence_bundle_comparison.md
docs/quality_reports/security/security_quality_summary/<current-report>.json
docs/quality_reports/security/cwe_mapped_local_validation_profile/<current-report>.json
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin

@'
docs/contracts/security_quality_current_evidence_bundle.md
docs/implementation_handoffs/security_quality_current_evidence_bundle_comparison.md
docs/quality_reports/security/security_quality_summary/<current-report>.json
docs/quality_reports/security/cwe_mapped_local_validation_profile/<current-report>.json
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Codex C should omit nonexistent paths from path-scoped scans.

If Codex C uses temporary public-safe summary JSON inputs for CodeQL, scanner,
or CI source rows, it must scan them before use and delete or leave them outside
the repo unless a later contract authorizes committing them.

## Acceptance Criteria

- A current evidence bundle contract exists at
  `docs/contracts/security_quality_current_evidence_bundle.md`.
- The contract chooses a new #639 artifact rather than changing #610's generic
  aggregation contract.
- CodeQL lifecycle evidence is separated from local scanner evidence.
- Every source family has required current evidence or a blocker/deferred
  reason.
- Public-safe summary rules are explicit.
- Blocker, advisory, watch-list, deferred, stale, not-collected, and current
  vocabulary is defined.
- Later gate-policy consideration is blocked unless required sources are
  current, public-safe, and validation-clean.
- The contract preserves all non-claims and protected-surface boundaries.

## Next Workflow Action

Next recommended role: Codex C / report execution.

Codex C should produce the current evidence bundle report if it can do so using
only the existing helper, public-safe summary inputs, and current validation.
If the existing helper cannot safely represent required sources, Codex C must
route back to Codex B.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / report execution.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/639

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/security_quality_current_evidence_bundle.md

Related aggregation contract:
docs/contracts/security_quality_scanner_summary_aggregation.md

Goal:
Produce a current, public-safe security-quality evidence bundle report before
any security-quality gate-policy discussion. Keep this report advisory-only.

Expected handoff:
docs/implementation_handoffs/security_quality_current_evidence_bundle_comparison.md

Do:
- Confirm branch and git status.
- Refresh current origin/main.
- Collect count-only CodeQL lifecycle counts for refs/heads/main.
- Refresh or explicitly classify CWE advisory report evidence.
- Include protected-surface, secret/private-marker, and CI/repo-check summaries
  only as public-safe counts/statuses.
- Use the existing aggregate helper if it can safely represent the evidence.
- Commit only intentional public-safe report artifacts and handoff files if a
  later submitter role is authorized.
- Label every source as current, stale, not_collected, deferred, blocked, or
  not_applicable.
- Preserve all non-claim booleans.

Do not:
- change CI;
- create or enforce a gate;
- mutate, dismiss, reopen, or close CodeQL alerts;
- read, persist, echo, or commit raw SARIF, raw CodeQL payloads, raw scanner
  finding lists, raw Player.log, raw JSONL payloads, SQLite contents, local app
  data, workbook exports, failed posts, runtime artifacts, secrets,
  credentials, tokens, endpoints, private paths, decklists, generated/private
  artifacts, or local-only artifacts;
- claim security assurance, privacy assurance, formal compliance, release
  readiness, deploy readiness, production readiness, parser truth, analytics
  truth, AI truth, or coaching truth;
- change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI
  /coaching/Line Tracer/production behavior.

Stop and route back to Codex B if:
- a required source cannot be summarized safely;
- the helper cannot represent current source vocabulary without a contract
  change;
- producing the bundle requires scanner weakening, CI changes, or product
  behavior changes;
- raw/private data would be exposed.

Validation:
- git status --short --branch
- git rev-parse HEAD
- git rev-parse origin/main
- count-only CodeQL open/fixed/dismissed reads for refs/heads/main
- py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
- py tools\generate_cwe_profile_advisory_report.py --write-report --report-date <YYYY-MM-DD>
- py -m pytest -q tests\test_security_quality_summary.py
- py -m pytest -q tests\test_cwe_profile_advisory_report.py tests\test_cwe_mapped_local_validation_profile.py
- py -m ruff check tools\generate_security_quality_summary.py tests\test_security_quality_summary.py
- py -m json.tool <current CWE report>
- py -m json.tool <current security-quality summary report>
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Final output:
- files changed
- report artifact path or blocked reason
- source freshness table
- CodeQL lifecycle summary
- local scanner summary status
- validation results
- non-claims preserved
- protected-surface status
- secret/private-marker status
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/639"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifacts:
    - "docs/quality_reports/security/security_quality_summary/2026-07-01-048e311-security-quality-summary.json"
    - "docs/contract_test_reports/security_quality_evidence_refresh_after_local_app_hardening.md"
    - "docs/contracts/security_quality_scanner_summary_aggregation.md"
  contract_artifact: "docs/contracts/security_quality_current_evidence_bundle.md"
  target_artifact: "docs/implementation_handoffs/security_quality_current_evidence_bundle_comparison.md"
  expected_report_path: "docs/quality_reports/security/security_quality_summary/<YYYY-MM-DD>-<short-commit>-security-quality-summary.json"
  risk_tier: "Medium security-communication risk; low runtime risk if report-only"
  base_branch: "main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/security-quality-evidence-bundle-639"
  decision: "Create a new #639 current-evidence-bundle contract rather than changing the generic #610 aggregation contract."
  current_codeql_count_only_evidence:
    ref: "refs/heads/main"
    open: 0
    fixed: 3
    dismissed: 14
  enforcement_authorized: false
  ci_change_authorized: false
  codeql_alert_mutation_authorized: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  release_readiness_claimed: false
  deploy_readiness_claimed: false
  production_readiness_claimed: false
  stop_conditions:
    - "Do not change CI or create/enforce a security-quality gate."
    - "Do not mutate, dismiss, reopen, or close CodeQL alerts."
    - "Do not read, persist, echo, or commit raw scanner, CodeQL, SARIF, Player.log, JSONL, SQLite, local app, workbook, failed-post, runtime, secret, endpoint, private-path, generated/private, or local-only payloads."
    - "Do not claim security assurance, privacy assurance, release readiness, deploy readiness, production readiness, parser truth, analytics truth, AI truth, or coaching truth."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior."
```
