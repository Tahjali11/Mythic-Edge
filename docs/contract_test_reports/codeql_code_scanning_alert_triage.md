# Contract Test Report: CodeQL Code Scanning Alert Triage

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/331

## Parent Issue

https://github.com/Tahjali11/Mythic-Edge/issues/330

## Contract

`docs/contracts/codeql_code_scanning_alert_triage.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:

- `docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md`

Changed files reviewed:

- `.github/workflows/repo-checks.yml`
- `src/mythic_edge_parser/app/status_file_names.py`
- `src/mythic_edge_parser/app/privacy_url_detection.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_gameplay_actions.py`
- `tests/test_evidence_runtime_status.py`
- `tests/test_evidence_validation_report_wiring.py`
- `tests/test_github_workflow_permissions.py`
- `docs/contracts/codeql_code_scanning_alert_triage.md`
- `docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md`

Reference files reviewed:

- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `frontend` not touched
- issue #331 and parent issue #330
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`
- `docs/templates/contract_test_report.md`

Unrelated local file excluded from this review:

- `docs/contracts/workflow_freshness_guard.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Findings

No blocking findings.

### CT-331-001: GitHub CodeQL Closure Remains Pending

- Severity: P3
- `finding_lifecycle`: `remaining_non_blocking`
- `finding_status`: expected external verification gap
- `blocking_status`: not blocking Codex F
- Evidence: refreshed GitHub CodeQL API snapshot still reports 16 open alerts
  before this unpushed local package can be scanned by GitHub.
- Verification evidence: local tests and source review support the fixes, but
  CodeQL closure cannot be claimed until the branch is pushed and GitHub code
  scanning reruns or a later approved dismissal happens.
- Next route: Codex F, then GitHub CodeQL rerun/PR checks.

### CT-331-002: Whole-File Secret/Private-Marker Scan Still Flags Existing Fixture Markers

- Severity: P3
- `finding_lifecycle`: `remaining_non_blocking`
- `finding_status`: validation caveat
- `blocking_status`: not blocking Codex F
- Evidence: path-fed secret/private-marker scan over touched files fails with
  existing scanner/test fixture markers in files that this security package
  necessarily touches.
- Verification evidence: changed-line review shows the new implementation uses
  synthetic placeholders and non-echo assertions; no raw private values,
  generated artifacts, credentials, or local-only artifacts were introduced.
- Next route: Codex F with this caveat preserved. If future workflow requires
  a zero-finding whole-file scan for security-test files, route a separate
  scanner-baseline/tooling issue rather than changing this CodeQL fix package.

## Contract Summary

The #331 contract requires alert-family triage and focused remediation for the
current CodeQL snapshot: local JSONL import path alerts, runtime/gameplay
generated filename alerts, evidence privacy URL-classification alerts, and
repo-check workflow permissions. The implementation must avoid alert dismissal,
avoid scanner suppression, preserve parser truth and payload identity, avoid raw
private artifact exposure, and avoid unrelated parser/runtime/analytics/
workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production
behavior changes.

## Current CodeQL Snapshot

The live CodeQL API still reports 16 open alerts:

| Alert range | Rule | File family | Current local classification |
| --- | --- | --- | --- |
| #16-#9 | `py/path-injection` | `src/mythic_edge_parser/local_app/import_jobs.py` | `likely_false_positive` |
| #8-#7 | `py/path-injection` | `src/mythic_edge_parser/app/runtime_surfaces.py` | `fix_required`, locally remediated |
| #6-#4 | `py/path-injection` | `src/mythic_edge_parser/app/gameplay_actions.py` | `fix_required`, locally remediated |
| #3 | `py/incomplete-url-substring-sanitization` | `src/mythic_edge_parser/app/evidence_validation_report_wiring.py` | `fix_required`, locally remediated |
| #2 | `py/incomplete-url-substring-sanitization` | `src/mythic_edge_parser/app/evidence_runtime_status.py` | `fix_required`, locally remediated |
| #1 | `actions/missing-workflow-permissions` | `.github/workflows/repo-checks.yml` | `fix_required`, locally remediated |

No CodeQL alert was dismissed, suppressed, or marked resolved locally.

## Source-To-Sink Review

### Alerts #16-#9: Manual JSONL Import Paths

Classification accepted: `likely_false_positive`.

`import_jobs.py` accepts explicit local operator-selected JSONL inputs by
design. Existing guards reject URL-like values, UNC-like values, blank or
non-string values, missing paths, directories, non-JSONL extensions, non-file
paths, and duplicate resolved paths. Existing tests cover quoted local paths,
batch duplicate resolution, invalid local paths, URL/UNC rejection, no raw path
echo, and no database creation on invalid/malformed inputs.

No implementation change was needed for this family.

### Alerts #8-#7: Runtime Timeline Generated Filenames

Classification accepted: `fix_required`, locally remediated.

`runtime_surfaces.py` now derives generated timeline filenames through
`safe_status_file_stem(...)` while preserving raw parser-owned `match_id` inside
payloads and history identity. Regression coverage proves path-looking match IDs
stay under the intended timeline root and payload identity remains unchanged.

### Alerts #6-#4: Gameplay Action Generated Filenames

Classification accepted: `fix_required`, locally remediated.

`gameplay_actions.py` now derives generated action JSON/Markdown filenames
through `safe_status_file_stem(...)` while preserving raw parser-owned
`match_id` inside payloads and lookups. Regression coverage proves
path-looking match IDs stay under the intended action root and payload identity
remains unchanged.

### Alerts #3-#2: URL Classification In Evidence Privacy Reports

Classification accepted: `fix_required`, locally remediated.

Both evidence privacy surfaces now call `contains_runtime_artifact_url(...)`
instead of raw substring checks. The helper tokenizes HTTP(S) URL-looking text,
parses hosts, and checks host identity/prefix semantics rather than trusting any
substring in the full payload. Tests cover true runtime/webhook-looking hosts,
lookalike hosts, and raw-value non-echo.

Residual note: a bare host with a terminal dot is still reported through the
broader forbidden-content path, but not as a runtime-artifact URL. This is not a
raw-value leak and is not blocking this CodeQL family fix.

### Alert #1: GitHub Workflow Permissions

Classification accepted: `fix_required`, locally remediated.

`.github/workflows/repo-checks.yml` now declares read-only contents permission.
Focused tests assert the workflow does not request write permissions for
contents, actions, or security-events.

## Confirmed Contract Matches

- CodeQL alert inventory was refreshed during review.
- No alerts were dismissed, suppressed, or bypassed.
- The local implementation maps every alert family to a classification.
- Parser-visible match IDs remain raw payload identity; only generated file
  names are sanitized.
- Runtime timeline and gameplay-action status files remain under their intended
  roots in regression tests.
- Evidence privacy URL detection no longer trusts full-payload substring checks.
- Workflow token permissions are explicit and least-privilege for repo checks.
- Manual JSONL import behavior remains compatible and covered by focused tests.
- No parser final reconciliation, event classes, match/game identity,
  deduplication, analytics schema/migrations, workbook/webhook/App Script/Sheets
  behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, credential
  policy, production behavior, or broad CI gate posture changed.
- No generated/private/local artifacts were kept.

## Contract Mismatches

None blocking.

## Missing Tests Or Safeguards

No blocking missing tests.

Non-blocking residual: CodeQL itself has not rerun against this local package,
so GitHub alert closure remains unverified.

## Validation Run

```text
git fetch --prune origin
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
gh issue view 331 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
gh issue view 330 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
gh api -H "Accept: application/vnd.github+json" "/repos/Tahjali11/Mythic-Edge/code-scanning/alerts?state=open&per_page=100"
py -m pytest -q tests\test_runtime_surfaces.py tests\test_gameplay_actions.py tests\test_evidence_runtime_status.py tests\test_evidence_validation_report_wiring.py tests\test_github_workflow_permissions.py tests\test_analytics_manual_jsonl_import.py tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
path-fed protected-surface scan over changed #331 files
path-fed secret/private-marker scan over changed #331 files
```

Results:

- Branch: `codex/analytics-foundation`
- Branch sync: `0 0`
- Issue #331: open
- Parent issue #330: open
- CodeQL API: 16 open alerts still visible before GitHub rerun
- Focused tests: 150 passed, 1 platform skip, 1 existing warning
- Ruff: passed
- `git diff --check`: passed with CRLF/LF warning for
  `tests/test_gameplay_actions.py`
- Agent docs: passed, errors 0, warnings 0
- Protected-surface scan: passed, forbidden 0, warnings 2
- Secret/private-marker scan: failed whole-file scan with forbidden 29,
  warnings 11, reviewed as pre-existing/test-fixture marker caveat

## Protected-Surface Status

Passed with expected warnings:

- `.github/workflows/repo-checks.yml` is a protected environment/runtime path
  surface, explicitly authorized by the #331 contract for least-privilege
  permissions.
- `src/mythic_edge_parser/app/gameplay_actions.py` is a protected
  match/game-identity-adjacent surface, explicitly authorized by the #331
  contract for generated filename hardening only.

Forbidden protected-surface count: 0.

## Secret / Private Marker Status

Whole-file path-fed scan result: failed, forbidden 29, warnings 11.

Review classification: non-blocking validation caveat. Findings are existing
fixture/scanner markers in touched files plus documentation references; changed
lines do not introduce raw private content, secrets, private local paths,
generated artifacts, runtime files, workbook exports, or local-only artifacts.

Do not report this package as having a clean secret/private-marker scan. Report
it as reviewed with known whole-file scanner-fixture hits.

## Generated / Private Artifact Status

- Generated/private artifacts kept: false.
- Disposable temp filename-check directory created during review and removed.
- No raw logs, JSONL artifacts, SQLite databases, runtime artifacts, failed
  posts, workbook exports, credentials, tokens, endpoint values, environment
  values, or local-only artifacts were added.

## Forbidden Scope

Forbidden scope touched: false.

## Recommendation

Approve for Codex F / Module Submitter with caveats:

- GitHub CodeQL closure remains pending until the branch is pushed and CodeQL
  reruns.
- The secret/private-marker scan is not clean at whole-file granularity because
  touched security-test files contain existing scanner fixtures. Preserve this
  caveat in the PR body rather than claiming a clean scan.
- Stage only the #331 package files. Do not stage
  `docs/contracts/workflow_freshness_guard.md`.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #331.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/331

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/analytics-foundation

Contract:
docs/contracts/codeql_code_scanning_alert_triage.md

Implementation handoff:
docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md

Codex E report:
docs/contract_test_reports/codeql_code_scanning_alert_triage.md

Goal:
Submit the reviewed CodeQL/code-scanning alert triage package. Stage only the
reviewed #331 files, commit, push, and open/update a draft PR to the approved
non-main integration branch. Do not close #331 or #330; lifecycle handling
routes to Codex G after PR checks and CodeQL rerun evidence.

Reviewed #331 files to stage only:
- .github/workflows/repo-checks.yml
- docs/contracts/codeql_code_scanning_alert_triage.md
- docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md
- docs/contract_test_reports/codeql_code_scanning_alert_triage.md
- src/mythic_edge_parser/app/status_file_names.py
- src/mythic_edge_parser/app/privacy_url_detection.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/evidence_runtime_status.py
- src/mythic_edge_parser/app/evidence_validation_report_wiring.py
- tests/test_runtime_surfaces.py
- tests/test_gameplay_actions.py
- tests/test_evidence_runtime_status.py
- tests/test_evidence_validation_report_wiring.py
- tests/test_github_workflow_permissions.py

Do not stage:
- docs/contracts/workflow_freshness_guard.md
- raw/private/generated/local artifacts
- unrelated files

Validation evidence:
- focused security/CodeQL regression tests -> passed, 150 passed, 1 skipped, 1 warning
- ruff -> passed
- git diff --check -> passed with CRLF/LF warning for tests/test_gameplay_actions.py
- agent docs -> passed
- protected-surface scan -> passed, forbidden 0, warnings 2 expected/authorized
- secret/private-marker scan -> whole-file path-fed scan failed on existing security fixture markers; changed-line review found no new raw/private/secrets exposure

Important:
- Do not claim GitHub CodeQL alerts are closed until the branch is pushed and CodeQL reruns.
- Do not dismiss CodeQL alerts.
- Do not target main.
- Do not close #331 or #330.
- Do not change parser truth, parser final reconciliation, event classes, match/game identity, deduplication, analytics schema/migrations, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, production behavior, or credential policy.

Final output must include branch, commit hash, PR URL, target branch, staged files, validation status, CodeQL rerun status/pending risk, protected-surface status, secret/private-marker caveat, generated artifact status, forbidden-scope confirmation, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/331"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "E"
  next_thread: "F"
  role_performed: "Codex E: Module Reviewer / CodeQL triage contract-test thread"
  branch: "codex/analytics-foundation"
  branch_sync: "0 0"
  contract_artifact: "docs/contracts/codeql_code_scanning_alert_triage.md"
  implementation_handoff: "docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md"
  review_artifact: "docs/contract_test_reports/codeql_code_scanning_alert_triage.md"
  findings:
    - "CT-331-001 P3 non-blocking: GitHub CodeQL closure remains pending until branch push and CodeQL rerun."
    - "CT-331-002 P3 non-blocking: whole-file secret/private-marker scan flags existing fixture markers in touched security-test files; changed-line review found no new raw/private exposure."
  verdict: "approved_for_codex_f_with_validation_caveats"
  codeql_status: "16 open alerts still visible before GitHub rerun; local closure unverified"
  validation:
    - "focused CodeQL/security regression tests -> passed, 150 passed, 1 skipped, 1 existing warning"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with CRLF/LF warning for tests/test_gameplay_actions.py"
    - "py tools/check_agent_docs.py -> passed"
    - "path-fed protected-surface scan -> passed, forbidden 0, warnings 2 expected/authorized"
    - "path-fed secret/private-marker scan -> failed whole-file scan, forbidden 29, warnings 11; reviewed as existing fixture marker caveat"
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  unrelated_untracked_preserved:
    - "docs/contracts/workflow_freshness_guard.md"
  next_recommended_role: "Codex F: Module Submitter"
```
