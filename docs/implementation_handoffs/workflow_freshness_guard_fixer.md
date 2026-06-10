# Workflow Freshness Guard - Fixer Handoff

## Issue

N/A - implementation issue recommended if desired.

## Contract

`docs/contracts/workflow_freshness_guard.md`

## Review Report

`docs/contract_test_reports/workflow_freshness_guard.md`

## Implementation Handoff

`docs/implementation_handoffs/workflow_freshness_guard_comparison.md`

## Risk Tier

Medium.

## Internal Project Area

Quality / Governance.

## Truth Owner

Workflow / Governance freshness classification. The checker reports current Git, GitHub, artifact, and worktree evidence but does not own project truth, parser truth, issue lifecycle truth, PR lifecycle truth, merge readiness, or cleanup authority.

## Bridge-Code Status

shared_support

## Role Performed

Codex D: Module Fixer.

## Findings Fixed

- CT-WFG-001 P1: checker did not implement the contract-required worktree mismatch classification.
- CT-WFG-002 P2: `--no-gh` could route to Codex C while issue freshness was unknown.

## What Changed

Added `worktree_mismatch` as a checker verdict and added `--expected-worktree` for comparing the current checkout path against an expected worktree path or directory name. A mismatch now routes to `ask_user` with a stop condition before implementation continues.

Changed result selection so an unknown GitHub issue state for a supplied issue number takes precedence over artifact routing. Local artifact classifications are still reported, but the top-level result becomes `github_state_unknown` and the route becomes `ask_user`.

## Files Changed

- `tools/check_workflow_freshness.py`
- `tests/test_check_workflow_freshness.py`
- `docs/implementation_handoffs/workflow_freshness_guard_fixer.md`

## Code Changed

Yes. Report-only governance checker behavior changed. Product/runtime code changed: no.

## Tests Added Or Updated

- Updated `--no-gh` plus untracked artifact coverage to expect `github_state_unknown` and `ask_user` while preserving artifact classification.
- Added expected worktree mismatch coverage.
- Added expected worktree directory-name match coverage.

## Interface Changes

- Added optional checker flag: `--expected-worktree`.
- Added checker verdict: `worktree_mismatch`.

The checker remains advisory and report-only.

## Contracted Area Status

The fix stayed inside governance/template/advisory tooling. It does not mutate Git, GitHub, worktrees, stashes, branches, PRs, artifacts, parser/runtime code, workbook/webhook surfaces, analytics/local-app behavior, AI/coaching behavior, production behavior, or generated/private/local artifacts.

## Validation Run

```powershell
py -m pytest -q tests\test_check_workflow_freshness.py tests\test_check_agent_docs.py
py -m ruff check tools\check_workflow_freshness.py tests\test_check_workflow_freshness.py
py tools\check_workflow_freshness.py --issue 331 --branch codex/workflow-freshness-guard --expected-worktree different-worktree --no-gh --json
py tools\check_workflow_freshness.py --issue 331 --branch codex/workflow-freshness-guard --source-artifact docs\contracts\workflow_freshness_guard.md --target-artifact docs\implementation_handoffs\workflow_freshness_guard_comparison.md --no-gh --json
py -m ruff check src tests tools
py tools\check_agent_docs.py
git diff --check
```

Results:

- Focused pytest -> passed, 26 tests.
- Focused Ruff -> passed.
- Worktree mismatch smoke -> returned `worktree_mismatch` and `ask_user`.
- `--no-gh` artifact smoke -> returned `github_state_unknown` and `ask_user` while listing untracked source/target artifacts.
- Repo-wide Ruff -> passed.
- Agent docs -> passed, errors 0, warnings 0.
- `git diff --check` -> passed.

## Protected-Surface Status

Path-scoped protected-surface scan over changed workflow-freshness files: passed, forbidden 0, warnings 2. The warnings are the expected workflow-authority-doc warnings for `docs/templates/workflow_handoff.md` and `docs/templates/current_status.md`.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan over changed workflow-freshness files: passed, forbidden 0, warnings 0.

## Generated / Private Artifact Status

No generated/private/local artifacts were created or kept. No raw logs, private JSONL artifacts, generated SQLite files, runtime files, failed posts, workbook exports, secrets, credentials, tokens, webhook URLs, spreadsheet IDs, environment values, or local-only artifacts were read, printed, copied, committed, or created.

## Still Unverified

- The checker remains advisory only; no hard workflow gate was added.
- PR-state freshness remains deferred from this first checker slice.
- No implementation issue exists yet; one is recommended if the user wants this governance slice submitted independently.

## Reviewer Focus

Ask Codex E to confirm:

- `worktree_mismatch` is implemented as a verdict and route.
- `--expected-worktree` handles path or directory-name comparisons.
- `--no-gh` with a supplied issue number routes to user confirmation before implementation/submission, even when artifacts are untracked.
- Artifact classifications remain present in the report.
- No product/protected behavior or mutating workflow behavior was added.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for the workflow freshness guard.

Issue:
N/A - implementation issue recommended if desired

Contract:
docs/contracts/workflow_freshness_guard.md

Prior review artifact:
docs/contract_test_reports/workflow_freshness_guard.md

Implementation handoff:
docs/implementation_handoffs/workflow_freshness_guard_comparison.md

Fixer handoff:
docs/implementation_handoffs/workflow_freshness_guard_fixer.md

Branch/worktree:
codex/workflow-freshness-guard
MythicEdge-workflow-freshness-guard

Confirm only the Codex D fixes:
- CT-WFG-001: checker now implements `worktree_mismatch` and `--expected-worktree`.
- CT-WFG-002: `--no-gh` with an issue number no longer routes to Codex C while issue state is unknown.
- Artifact classifications remain visible.
- The checker remains report-only and non-mutating.
- No parser/runtime/workbook/webhook/App Script/Sheets/analytics/local-app/OpenAI/AI/coaching/production behavior changed.

Suggested validation:
py -m pytest -q tests\test_check_workflow_freshness.py tests\test_check_agent_docs.py
py -m ruff check tools\check_workflow_freshness.py tests\test_check_workflow_freshness.py
py tools\check_workflow_freshness.py --issue 331 --branch codex/workflow-freshness-guard --expected-worktree different-worktree --no-gh --json
py tools\check_workflow_freshness.py --issue 331 --branch codex/workflow-freshness-guard --source-artifact docs\contracts\workflow_freshness_guard.md --target-artifact docs\implementation_handoffs\workflow_freshness_guard_comparison.md --no-gh --json
py tools\check_agent_docs.py
git diff --check

Run path-scoped protected-surface and secret/private-marker scans over changed workflow-freshness files.
```

```yaml
workflow_handoff:
  issue: "N/A - implementation issue recommended if desired"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/workflow_freshness_guard.md"
  review_artifact: "docs/contract_test_reports/workflow_freshness_guard.md"
  implementation_handoff: "docs/implementation_handoffs/workflow_freshness_guard_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/workflow_freshness_guard_fixer.md"
  risk_tier: "Medium"
  branch: "codex/workflow-freshness-guard"
  base_branch: "origin/codex/analytics-foundation"
  worktree: "MythicEdge-workflow-freshness-guard"
  findings_fixed:
    - "CT-WFG-001 P1: checker now implements worktree_mismatch classification through --expected-worktree."
    - "CT-WFG-002 P2: --no-gh with supplied issue now routes to github_state_unknown/ask_user before artifact continuation routes."
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex E confirmation thread"
```
