# CodeQL Code Scanning Alert Triage Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issues

- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/330
- Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/331

## Contract Used

- `docs/contracts/codeql_code_scanning_alert_triage.md`

## Branch And Git Status

- Branch: `codex/analytics-foundation`
- Branch sync before implementation: `0 0` with `origin/codex/analytics-foundation`
- No separate worktree was needed because the active checkout was on the expected branch and only the #331 contract was present as local work.
- Unrelated untracked file preserved and not included in this scope:
  `docs/contracts/workflow_freshness_guard.md`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/codeql_code_scanning_alert_triage.md`
- `.github/workflows/repo-checks.yml`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_gameplay_actions.py`
- `tests/test_evidence_runtime_status.py`
- `tests/test_evidence_validation_report_wiring.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_protected_surfaces.py`

## Refreshed CodeQL Snapshot

The live GitHub CodeQL snapshot still showed 16 open alerts before local
implementation:

| Alert range | Rule | Severity | File family | Classification |
| --- | --- | --- | --- | --- |
| #16-#9 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | `likely_false_positive` |
| #8-#7 | `py/path-injection` | high | `src/mythic_edge_parser/app/runtime_surfaces.py` | `fix_required` |
| #6-#4 | `py/path-injection` | high | `src/mythic_edge_parser/app/gameplay_actions.py` | `fix_required` |
| #3 | `py/incomplete-url-substring-sanitization` | high | `src/mythic_edge_parser/app/evidence_validation_report_wiring.py` | `fix_required` |
| #2 | `py/incomplete-url-substring-sanitization` | high | `src/mythic_edge_parser/app/evidence_runtime_status.py` | `fix_required` |
| #1 | `actions/missing-workflow-permissions` | medium | `.github/workflows/repo-checks.yml` | `fix_required` |

No CodeQL alerts were dismissed.

## Current Behavior Compared To Contract

Manual JSONL import already treats paths as explicit local operator-selected
inputs. Existing guards reject URL-like values, UNC-like values, blank or
non-string values, non-`.jsonl` paths, missing files, directories, and duplicate
resolved paths. Existing status responses avoid raw path echo. Focused manual
import tests cover those boundaries, so no import behavior change was made.

Runtime timeline and gameplay-action status writers used parser-produced
`match_id` values directly in generated status filenames. That was the clearest
path-injection gap because parser identity should remain raw in payloads while
filesystem path segments should be derived from a safe name.

Evidence privacy helpers used substring checks for runtime/webhook URL hosts.
That could classify lookalike hosts as trusted runtime artifacts. The contract
allowed a small shared helper to parse URL-like tokens and compare exact hosts.

The repository checks workflow did not declare explicit token permissions. The
contract recommended read-only `contents: read`.

## Implementation Option Chosen

Implemented the smallest behavior-preserving fixes:

- Added a safe generated-status filename helper.
- Used safe filename stems for runtime timeline and gameplay-action generated
  status files while preserving raw `match_id` in payloads and loaders.
- Added an exact-host runtime artifact URL helper and used it from both privacy
  report surfaces.
- Added explicit read-only workflow token permissions.
- Added focused regression tests for the changed behavior.
- Documented manual JSONL import CodeQL alerts as likely false positives, with
  tests preserved as evidence.

## Files Changed

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
- `docs/contracts/codeql_code_scanning_alert_triage.md` (preserved Codex B contract artifact)
- `docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md`

## Exact Sections Changed

- `.github/workflows/repo-checks.yml`: added top-level read-only
  `permissions: contents: read`.
- `status_file_names.py`: added `safe_status_file_stem` for generated status
  path segments.
- `runtime_surfaces.py`: timeline reads/writes and match-history
  `timeline_path` now use the safe generated filename stem.
- `gameplay_actions.py`: match-action generated JSON/Markdown filenames and
  match-action payload lookup now use the safe generated filename stem.
- `privacy_url_detection.py`: added exact-host URL-token detection for
  runtime/webhook artifact URLs.
- `evidence_runtime_status.py` and `evidence_validation_report_wiring.py`:
  replaced substring runtime URL detection with the exact-host helper.
- `tests/test_runtime_surfaces.py`: added path-escape regression coverage for
  generated timeline files.
- `tests/test_gameplay_actions.py`: added path-escape regression coverage for
  generated action JSON and Markdown files.
- `tests/test_evidence_runtime_status.py` and
  `tests/test_evidence_validation_report_wiring.py`: added trusted-host and
  lookalike-host privacy tests with raw-value non-echo assertions.
- `tests/test_github_workflow_permissions.py`: added a focused workflow
  permission test.

## Code/Test/Doc Status

- Code changed: yes.
- Tests changed: yes.
- Docs changed: yes, handoff plus preserved contract artifact.
- Schema changed: no.
- Fixtures changed: no.
- Generated/private artifacts changed: no.

## Alert Classification Detail

| Alert | Classification | Evidence / action |
| --- | --- | --- |
| #16-#9 | `likely_false_positive` | Manual JSONL import accepts explicit local operator-selected `.jsonl` files by design. Existing guards reject URL/UNC/blank/non-string/non-`.jsonl`/missing/directory inputs, resolve paths for duplicate detection, and avoid raw path echo. Focused manual import tests passed. No dismissal performed. |
| #8-#7 | `fix_required` | Runtime timelines used raw match IDs in generated filenames. Added safe stem derivation and regression coverage proving path-looking match IDs stay under the timeline root while payload match identity is unchanged. |
| #6-#4 | `fix_required` | Gameplay action status files used raw match IDs in generated filenames. Added safe stem derivation and regression coverage proving generated JSON/Markdown files stay under the action root while payload match identity is unchanged. |
| #3 | `fix_required` | Evidence validation privacy reporting used substring runtime URL checks. Replaced with exact-host URL-token detection and added trusted/lookalike host tests. |
| #2 | `fix_required` | Runtime status privacy reporting used substring runtime URL checks. Replaced with exact-host URL-token detection and added trusted/lookalike host tests. |
| #1 | `fix_required` | Repo checks workflow lacked explicit token permissions. Added read-only `contents: read` and a focused test rejecting write permissions. |

## Validation Run

- `py -m pytest -q tests\test_runtime_surfaces.py tests\test_gameplay_actions.py`
  -> passed, 25 tests.
- `py -m pytest -q tests\test_evidence_runtime_status.py tests\test_evidence_validation_report_wiring.py`
  -> passed, 34 tests.
- `py -m pytest -q tests\test_github_workflow_permissions.py`
  -> passed, 1 test.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py`
  -> passed, 14 tests, 1 Starlette deprecation warning.
- `py -m pytest -q tests\test_runtime_surfaces.py tests\test_gameplay_actions.py tests\test_evidence_runtime_status.py tests\test_evidence_validation_report_wiring.py tests\test_github_workflow_permissions.py tests\test_analytics_manual_jsonl_import.py tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py`
  -> passed, 150 tests, 1 platform skip, 1 Starlette deprecation warning.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed with a CRLF/LF warning for
  `tests/test_gameplay_actions.py`.
- `py tools\check_agent_docs.py` -> passed.
- `py tools\check_secret_patterns.py --all` -> advisory failed with
  pre-existing all-repo findings: forbidden 538, warnings 901.
- `py tools\check_secret_patterns.py --base origin/codex/analytics-foundation`
  -> passed, scanned paths 0 because the package is uncommitted/untracked and
  requires path-fed validation.
- `py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation`
  -> passed, changed paths 0 for the same uncommitted/untracked reason.
- Path-fed protected-surface scan over the explicit package file list ->
  passed, forbidden 0, warnings 2. Warnings were expected contract-authorized
  protected surfaces: `.github/workflows/repo-checks.yml` and
  `src/mythic_edge_parser/app/gameplay_actions.py`.
- Path-fed secret/private-marker scan over the explicit package file list ->
  failed, forbidden 29, warnings 11. The findings are existing scanner
  categories in touched files, including runtime-status marker text, raw
  Player.log marker text in privacy tests, placeholder runtime/private path
  tests, and existing synthetic Apps Script placeholder tests. No raw private
  values were printed in this handoff, and no private/generated artifact was
  added.
- Direct ASCII/trailing-whitespace/final-newline checks for new files ->
  passed.

## CodeQL Verification Status

CodeQL alert closure is not locally verifiable. The GitHub alert list was
refreshed before implementation, but alerts will remain open until this branch
is pushed and GitHub CodeQL/code scanning reruns or a reviewer approves any
future dismissal rationale.

## Protected-Surface Status

Protected surfaces were touched only where the contract explicitly authorized
focused hardening:

- runtime status generated filenames;
- gameplay-action generated filenames;
- evidence privacy URL classification;
- repo-checks workflow permissions.

Parser truth ownership, parser payload identity, match/game identity,
deduplication, analytics schema, workbook/webhook/App Script/Sheets behavior,
AI/coaching behavior, and production behavior were not changed.

## Secret / Private Artifact Status

No raw Player.log content, private JSONL artifacts, generated SQLite files,
runtime artifacts, failed posts, workbook exports, app-data files, private
paths, raw hashes, secrets, credentials, environment values, or local-only
artifacts were created, copied, printed, stored, or committed.

All new tests use synthetic placeholder values.

## Remaining Risk / Unverified

- CodeQL closure remains unverified until GitHub code scanning reruns.
- Manual JSONL import alerts are classified as likely false positives, not
  dismissed. Codex E should inspect source-to-sink evidence and decide whether
  to route to D, F, or a narrower follow-up.
- Path-fed secret/private-marker scan over whole touched files fails on
  pre-existing scanner findings in files this contract had to touch. Codex E
  should treat that as a review item and confirm whether changed-line evidence
  is sufficient or route a narrow scanner-baseline follow-up.
- The untracked `docs/contracts/workflow_freshness_guard.md` is unrelated and
  remains untouched.

## Forbidden Scope

Forbidden scope touched: false.

No parser state final reconciliation, parser event classes, parser payload
shape, match/game identity, analytics schema, workbook schema, webhook payload
shape, Apps Script behavior, Sheets behavior, OpenAI/model-provider behavior,
AI/coaching behavior, Line Tracer behavior, production behavior, credential
policy, or broad CI gate posture was changed.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #331.

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/331

Branch:
codex/analytics-foundation

Contract:
docs/contracts/codeql_code_scanning_alert_triage.md

Implementation handoff:
docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md

Expected review artifact:
docs/contract_test_reports/codeql_code_scanning_alert_triage.md

Goal:
Review the active #331 CodeQL/code-scanning triage implementation against the contract. Confirm or reject the alert classifications, source-to-sink evidence, focused fixes, tests, protected-surface boundaries, and CodeQL residual risk. Produce the contract-test report.

Before reviewing:
- Confirm branch and git status.
- Verify issues #330 and #331 are still open if GitHub CLI is available.
- Refresh current CodeQL open alerts.
- Read the contract and implementation handoff.
- Inspect changed code/tests/workflow files.

Review focus:
- Alerts #9-#16: verify manual JSONL import likely-false-positive rationale and existing guard/test coverage.
- Alerts #7-#8: verify runtime timeline filenames use safe generated stems while raw match IDs remain payload/parser truth.
- Alerts #4-#6: verify gameplay-action generated filenames use safe generated stems while raw match IDs remain payload/parser truth.
- Alerts #2-#3: verify runtime/webhook URL privacy detection uses exact-host parsing and does not echo raw values.
- Alert #1: verify repo-checks workflow uses least-privilege read-only token permissions.

Do not:
- dismiss CodeQL alerts without explicit user approval after review;
- change parser truth, parser state final reconciliation, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, analytics schema/migrations, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, production behavior, credential policy, or broad CI gate posture;
- print, commit, copy, or expose raw Player.log content, private JSONL artifacts, generated SQLite files, runtime artifacts, failed posts, workbook exports, app-data files, private paths, raw hashes, secrets, credentials, environment values, or local-only artifacts;
- stage, commit, push, open a PR, close #330, or close #331.

Suggested validation:
py -m pytest -q tests\test_runtime_surfaces.py tests\test_gameplay_actions.py tests\test_evidence_runtime_status.py tests\test_evidence_validation_report_wiring.py tests\test_github_workflow_permissions.py tests\test_analytics_manual_jsonl_import.py tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files via --paths-from-stdin.

Final report must include:
- findings first, ordered by severity;
- alert-by-alert classification table;
- validation results;
- CodeQL rerun/status evidence or residual risk;
- protected-surface status;
- secret/private-artifact status;
- whether forbidden scope was touched;
- recommendation to Codex D, F, or back to B/A;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/331"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "C"
  next_thread: "E"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/codeql_code_scanning_alert_triage.md"
  implementation_handoff: "docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md"
  review_artifact: "docs/contract_test_reports/codeql_code_scanning_alert_triage.md"
  alert_snapshot:
    total_open_before_local_fix: 16
    path_injection_high: 13
    incomplete_url_substring_sanitization_high: 2
    missing_workflow_permissions_medium: 1
  classifications:
    likely_false_positive:
      - "CodeQL alerts #9-#16: manual JSONL import local operator path selection"
    fix_required:
      - "CodeQL alerts #7-#8: runtime generated status filenames"
      - "CodeQL alerts #4-#6: gameplay-action generated status filenames"
      - "CodeQL alerts #2-#3: incomplete URL substring sanitization"
      - "CodeQL alert #1: missing workflow permissions"
  validation:
    - "focused CodeQL triage tests -> passed, 150 passed, 1 skipped, 1 warning"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with CRLF/LF warning for tests/test_gameplay_actions.py"
    - "py tools/check_agent_docs.py -> passed"
    - "all-repo secret scan advisory -> failed with pre-existing findings, forbidden 538, warnings 901"
    - "path-fed protected-surface scan -> passed, forbidden 0, warnings 2 expected authorized surfaces"
    - "path-fed secret/private-marker scan -> failed on pre-existing findings in touched files, forbidden 29, warnings 11"
    - "new-file ASCII/trailing-whitespace/final-newline check -> passed"
  codeql_status: "local closure unverified until branch is pushed and GitHub CodeQL reruns"
  forbidden_scope_touched: false
  generated_private_artifacts_kept: false
  unrelated_untracked_preserved:
    - "docs/contracts/workflow_freshness_guard.md"
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
