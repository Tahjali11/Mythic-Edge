# Workflow Freshness Guard Contract-Test Report

## Confirmation Update

Codex E confirmation verdict: both prior findings are fixed.

- CT-WFG-001 fixed: the checker now defines `worktree_mismatch`, accepts
  `--expected-worktree`, returns `worktree_mismatch` with `ask_user`, and emits
  a stop condition when the current checkout does not match the expected
  worktree.
- CT-WFG-002 fixed: when `--no-gh` is used with a supplied issue number, the
  checker now returns `github_state_unknown` and `ask_user` before artifact
  continuation routes, while preserving source/target artifact classifications
  in the report.

The fixed implementation remains advisory and report-only. No Git, GitHub,
worktree, stash, branch, PR, issue, parser/runtime, workbook/webhook,
analytics/local-app, OpenAI/AI/coaching, or production behavior was mutated.

## Findings

Fixed in Codex D confirmation pass; no blocking findings remain.

### CT-WFG-001 P1: checker does not implement the contract-required worktree mismatch classification

The contract lists `worktree_mismatch` as a freshness verdict and requires the
checker to classify worktree mismatch. The implementation can list worktrees
when `--include-worktrees` is supplied, but it has no `worktree_mismatch`
verdict, no expected/current worktree comparison input, and no result-selection
path that considers worktree reports. The focused tests only cover preserving
paths with spaces through porcelain parsing.

Impact: a continuing thread can still be run from the wrong sibling worktree or
a stale issue worktree without the checker producing the explicit mismatch
verdict the contract requires. This leaves one of the motivating failure modes
partially unguarded.

Evidence:

- `docs/contracts/workflow_freshness_guard.md` requires `worktree_mismatch` and
  checker coverage for worktree mismatch.
- `tools/check_workflow_freshness.py` defines verdict constants for fresh,
  closed issue, branch mismatch, artifact states, and GitHub unknown, but not
  worktree mismatch.
- `tools/check_workflow_freshness.py` renders worktree classifications, but
  `_choose_result(...)` receives no worktree evidence and cannot elevate a
  worktree mismatch to a verdict or stop condition.
- `tests/test_check_workflow_freshness.py` covers worktree path parsing, not
  worktree mismatch routing.

Recommendation: route to Codex D to add a narrow expected-worktree or worktree
hint check, a `worktree_mismatch` verdict, stop-condition text, and focused
tests.

Fixed-state confirmation: fixed. The checker now includes
`VERDICT_WORKTREE_MISMATCH`, `_matches_expected_worktree(...)`,
`--expected-worktree`, result-selection logic, and tests for mismatch and
directory-name match cases.

### CT-WFG-002 P2: `--no-gh` can route to Codex C while issue freshness is unknown

The contract says `--no-gh` should report issue/PR freshness as unknown and
that GitHub-unavailable states should route implementation/submission work to
manual confirmation or live refresh. In the current checker, artifact findings
are evaluated before `issue.state == "unknown"`, so a run with `--no-gh` plus
untracked source/target artifacts returns `artifact_untracked` and
`route_to_codex_c` while the issue state is unknown.

Impact: if GitHub is unavailable, the checker can recommend continuing Codex C
work based on local artifacts even though it cannot verify whether the source
issue is open, closed, or superseded. That weakens the freshness guard for stale
handoffs.

Evidence:

- Smoke command with `--no-gh`, issue `331`, and the untracked source/target
  artifacts returned `result: artifact_untracked`, `recommended_route:
  route_to_codex_c`, and `issue.state: unknown`.
- `tests/test_check_workflow_freshness.py` codifies this behavior in
  `test_untracked_source_artifact_routes_to_codex_c_without_github(...)`.
- The checker only returns `github_state_unknown` when there are no missing or
  untracked artifact findings ahead of the unknown issue-state check.

Recommendation: route to Codex D to preserve local artifact classification but
surface GitHub unknown as either the top-level verdict, a stop condition, or an
explicit user-confirmation route whenever the issue state matters.

Fixed-state confirmation: fixed. The checker now evaluates supplied issue
unknown state before artifact continuation routes and retains artifact details
in the report.

## Role Performed

Codex E: Module Reviewer / contract-test thread.

## Issue Reviewed

N/A - implementation issue recommended if desired.

## Branch / Worktree

- Branch: `codex/workflow-freshness-guard`
- Base branch: `origin/codex/analytics-foundation`
- Worktree: `MythicEdge-workflow-freshness-guard`
- Branch sync: `0 0`

## Contract And Handoff Reviewed

- `docs/contracts/workflow_freshness_guard.md`
- `docs/implementation_handoffs/workflow_freshness_guard_comparison.md`
- `docs/implementation_handoffs/workflow_freshness_guard_fixer.md`

## Files Reviewed

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/contracts/workflow_freshness_guard.md`
- `docs/implementation_handoffs/workflow_freshness_guard_comparison.md`
- `docs/templates/current_status.md`
- `docs/templates/workflow_handoff.md`
- `tools/check_workflow_freshness.py`
- `tests/test_check_workflow_freshness.py`
- `docs/implementation_handoffs/workflow_freshness_guard_fixer.md`

## Contract Matches

- Workflow handoff template includes recommended freshness fields.
- Current-status template includes a compact freshness summary.
- The checker is report-only and returns exit code 0 for advisory results.
- The checker does not stage, commit, push, delete worktrees, mutate stashes,
  close/reopen issues, open PRs, merge, or create CI gates.
- Branch mismatch, closed issue reentry, missing artifact, untracked artifact,
  GitHub unknown, and worktree-list parsing have focused coverage.
- Worktree mismatch is now covered through `--expected-worktree`.
- GitHub-unknown state now takes precedence over artifact continuation routes
  when an issue number is supplied.
- Older handoffs remain compatible because the freshness block is advisory.
- No product behavior or protected parser/workbook/analytics/local-app/AI
  surface changed.

## Contract Mismatches

None remaining for the two reviewed findings.

## Missing Tests Or Safeguards

No remaining test gap for the two reviewed findings. PR-state freshness remains
deferred by the first-slice scope and is not a blocker for this confirmation.

## Validation Run

- `git status --short --branch --untracked-files=all` -> branch confirmed;
  scoped modified/untracked workflow-freshness files only.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation`
  -> `0 0`.
- `git diff --name-status` -> modified templates only; untracked files are
  visible through `git status`.
- `py -m pytest -q tests\test_check_workflow_freshness.py tests\test_check_agent_docs.py`
  -> passed, 24 tests.
- `py -m ruff check tools\check_workflow_freshness.py tests\test_check_workflow_freshness.py`
  -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Checker smoke against `codex/analytics-foundation` -> command passed and
  returned expected `branch_mismatch` from isolated worktree.
- Checker smoke against `codex/workflow-freshness-guard` -> command passed and
  returned `artifact_untracked` for unsubmitted contract/handoff artifacts.
- Checker smoke with `--no-gh` and no artifact args -> command passed and
  returned `github_state_unknown`.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` after report creation -> passed.
- Path-scoped protected-surface scan after report creation -> passed,
  forbidden 0, warnings 2. Warnings are expected and contract-authorized for
  workflow-template files.
- Path-scoped secret/private-marker scan after report creation -> passed,
  forbidden 0, warnings 0.
- Confirmation `py -m pytest -q tests\test_check_workflow_freshness.py tests\test_check_agent_docs.py`
  -> passed, 26 tests.
- Confirmation focused Ruff -> passed.
- Confirmation repo-wide Ruff -> passed.
- Confirmation checker smoke for expected worktree mismatch -> returned
  `worktree_mismatch` and `ask_user`.
- Confirmation checker smoke for `--no-gh` with source/target artifacts ->
  returned `github_state_unknown` and `ask_user`, while preserving artifact
  classifications.
- Confirmation checker smoke for matching expected worktree -> returned
  `fresh_with_warnings` because local package artifacts remain unsubmitted.
- Confirmation `git diff --check` -> passed.
- Confirmation `py tools\check_agent_docs.py` -> passed.
- Confirmation path-scoped protected-surface scan -> passed, forbidden 0,
  warnings 2 expected workflow-template warnings.
- Confirmation path-scoped secret/private-marker scan -> passed, forbidden 0,
  warnings 0.

## Protected-Surface Status

Passed. Forbidden 0, warnings 2. The two warnings are expected
workflow-authority-doc warnings for `docs/templates/workflow_handoff.md` and
`docs/templates/current_status.md`, which are directly authorized by the
contract.

## Secret / Private-Marker Status

Passed. Forbidden 0, warnings 0.

## Generated / Private Artifact Status

No generated/private/local artifacts were created or kept. No raw logs,
private JSONL artifacts, generated SQLite files, runtime files, failed posts,
workbook exports, secrets, credentials, tokens, webhook URLs, spreadsheet IDs,
environment values, or local-only artifacts were read, printed, copied, or
committed.

## Forbidden Scope

Forbidden scope touched: false.

No parser/runtime/workbook/webhook/App Script/Sheets/analytics/local-app/OpenAI
/AI/coaching/production behavior changed. No worktrees, stashes, issues,
branches, PRs, or untracked artifacts were mutated.

## Recommendation

Route to Codex F if the user wants this governance/tooling package submitted.
If no implementation issue is desired, first decide whether to create one or
submit as a governance/tooling package with the existing "N/A" source context.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "N/A - implementation issue recommended if desired"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/workflow_freshness_guard.md"
  review_artifact: "docs/contract_test_reports/workflow_freshness_guard.md"
  implementation_handoff: "docs/implementation_handoffs/workflow_freshness_guard_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/workflow_freshness_guard_fixer.md"
  risk_tier: "Medium"
  branch: "codex/workflow-freshness-guard"
  base_branch: "origin/codex/analytics-foundation"
  worktree: "MythicEdge-workflow-freshness-guard"
  findings_confirmed_fixed:
    - "CT-WFG-001 P1: checker now implements worktree_mismatch classification through --expected-worktree."
    - "CT-WFG-002 P2: --no-gh with supplied issue now routes to github_state_unknown/ask_user before artifact continuation routes."
  validation:
    - "pytest checker/agent-doc tests -> passed, 26 tests"
    - "ruff focused checker/tests -> passed"
    - "ruff repo-wide -> passed"
    - "agent docs -> passed"
    - "checker smoke -> worktree_mismatch/github_state_unknown/matching expected-worktree paths observed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 2 expected workflow-template warnings"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex F: Module Submitter"
```
