# Workflow Freshness Guard Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue

N/A - implementation issue recommended if desired.

## Contract

- `docs/contracts/workflow_freshness_guard.md`

## Internal Project Area

Quality / Governance.

## Truth Owner

Workflow / Governance freshness classification. The checker reports current
Git/GitHub/artifact evidence but does not own project truth, parser truth,
issue lifecycle truth, PR lifecycle truth, merge readiness, or cleanup
authority.

## Bridge-Code Status

`shared_support`

## Branch And Worktree

- Base branch requested by handoff: `codex/analytics-foundation`
- Isolated implementation branch/worktree used:
  `codex/workflow-freshness-guard` in sibling worktree
  `MythicEdge-workflow-freshness-guard`
- Reason for separate worktree: the primary `MythicEdge` checkout contained
  active #331 CodeQL work and unrelated untracked artifacts. This slice was
  isolated to avoid absorbing #331 changes.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/workflow_handoff.md`
- `docs/templates/current_status.md`
- `docs/contracts/workflow_freshness_guard.md`
- `tools/check_agent_docs.py`
- `tests/test_check_agent_docs.py`
- `git status --short --branch --untracked-files=all`
- `git worktree list`
- Live issue state for #302, #304, #315, #321, #330, and #331

## Current Behavior Compared To Contract

Current workflow templates did not include explicit freshness fields. Current
status summaries had no compact way to report branch/worktree/untracked
artifact freshness. No workflow freshness checker existed.

The contract required a recommended, non-blocking freshness block in
`workflow_handoff`, a `freshness_summary` section in current-status reports,
and an advisory report-only checker if straightforward. This implementation
adds those surfaces without making freshness a CI gate and without mutating
Git, GitHub, worktrees, stashes, branches, PRs, or artifacts.

## Implementation Option Chosen

Implemented the first contracted docs/tooling slice:

- Update `docs/templates/workflow_handoff.md` with an optional recommended
  `freshness` block and compatibility note for older handoffs.
- Update `docs/templates/current_status.md` with an advisory
  `freshness_summary` shape.
- Add `tools/check_workflow_freshness.py` as a report-only checker.
- Add focused tests for branch mismatch, untracked artifact routing, missing
  artifact routing, closed issue reentry, JSON/text output shape, and worktree
  paths containing spaces.

## Files Changed

- `docs/contracts/workflow_freshness_guard.md`
- `docs/templates/workflow_handoff.md`
- `docs/templates/current_status.md`
- `tools/check_workflow_freshness.py`
- `tests/test_check_workflow_freshness.py`
- `docs/implementation_handoffs/workflow_freshness_guard_comparison.md`

## Exact Sections Changed

- `docs/templates/workflow_handoff.md`: added recommended `freshness` metadata
  fields and advisory compatibility prose.
- `docs/templates/current_status.md`: added `freshness_summary` metadata shape
  and non-CI/non-product-schema prose.
- `tools/check_workflow_freshness.py`: added report-only advisory checker with
  Git branch/ahead-behind status, dirty/untracked path listing, artifact state
  classification, optional GitHub issue lookup, optional worktree
  classification, text output, and deterministic JSON output.
- `tests/test_check_workflow_freshness.py`: added focused coverage for the
  checker behavior.

## Code/Test/Interface Status

- Runtime/product code changed: no.
- Governance docs changed: yes.
- Tooling code changed: yes, report-only local governance checker.
- Tests changed: yes.
- Interface changes: new optional CLI command
  `py tools\check_workflow_freshness.py`; new recommended handoff/current
  status metadata fields only.
- CI gates changed: no.

## Freshness Model Implemented

Implemented report-only classifications for:

- `fresh`
- `fresh_with_warnings`
- `closed_issue_reentry`
- `branch_mismatch`
- `artifact_untracked`
- `artifact_missing`
- `github_state_unknown`

Implemented route recommendations for:

- `continue_current_role`
- `route_to_codex_b`
- `route_to_codex_c`
- `ask_user`

The checker also reports dirty paths, untracked artifacts, optional worktrees,
source/target artifact state, issue/tracker state, branch/upstream, and
ahead/behind counts.

## Live Issue Evidence

Verified with GitHub CLI:

- #302: CLOSED
- #304: CLOSED
- #315: CLOSED
- #321: CLOSED
- #330: OPEN
- #331: OPEN

## Advisory Checker Behavior

The checker is intentionally non-mutating. It does not stage, commit, push,
delete, prune, clean, close issues, reopen issues, open PRs, merge PRs, or
change CI. It returns exit code 0 for advisory freshness verdicts so it can be
used in reports without becoming a gate.

Live smoke checks showed:

- Running against `--branch codex/analytics-foundation` from the isolated
  worktree reports `branch_mismatch`, as expected.
- Running against `--branch codex/workflow-freshness-guard` with the source
  contract reports `artifact_untracked`, as expected.
- Worktree paths containing spaces are preserved through porcelain parsing.

## Validation Run

- `py -m pytest -q tests\test_check_workflow_freshness.py tests\test_check_agent_docs.py`
  -> passed, 24 tests.
- `py -m ruff check tools\check_workflow_freshness.py tests\test_check_workflow_freshness.py`
  -> passed.
- `py tools\check_agent_docs.py` -> passed.
- `py tools\check_workflow_freshness.py --issue 331 --branch codex/analytics-foundation --source-artifact docs\contracts\workflow_freshness_guard.md --target-artifact docs\implementation_handoffs\workflow_freshness_guard_comparison.md --include-worktrees --json`
  -> passed command execution; report result `branch_mismatch`, expected
  because this implementation used an isolated branch/worktree.
- `py tools\check_workflow_freshness.py --issue 331 --branch codex/workflow-freshness-guard --source-artifact docs\contracts\workflow_freshness_guard.md --include-worktrees`
  -> passed command execution; report result `artifact_untracked`, expected
  for the copied contract artifact before submission.
- `py tools\check_workflow_freshness.py --issue 331 --branch codex/workflow-freshness-guard --source-artifact docs\contracts\workflow_freshness_guard.md --target-artifact docs\implementation_handoffs\workflow_freshness_guard_comparison.md --include-worktrees --json`
  -> passed command execution; report result `artifact_untracked`, expected
  because the contract and handoff are untracked candidate artifacts before
  submitter work.
- `git diff --check` -> passed.
- Path-scoped protected-surface scan over changed files -> passed, forbidden
  0, warnings 2. Warnings were expected contract-authorized workflow authority
  docs: `docs/templates/workflow_handoff.md` and
  `docs/templates/current_status.md`.
- Path-scoped secret/private-marker scan over changed files -> passed,
  forbidden 0, warnings 0.
- Direct ASCII/trailing-whitespace/final-newline checks for new files ->
  passed.

## Protected-Surface Status

No product protected surfaces were changed. Parser behavior, parser state final
reconciliation, analytics schema, workbook schema, webhook payload shape, Apps
Script behavior, Sheets behavior, local app behavior, OpenAI/AI/coaching
behavior, production behavior, and generated/private artifact policy were not
changed.

## Secret / Private-Marker Status

No raw logs, private JSONL artifacts, generated SQLite files, runtime
artifacts, failed posts, workbook exports, secrets, credentials, tokens,
webhook URLs, spreadsheet IDs, environment values, or local-only artifacts were
read, printed, copied, committed, or created.

## Remaining Risks / Unverified

- The checker is intentionally advisory; a later issue/contract is required
  before any role treats it as a hard gate.
- The original primary worktree still contains active #331 work and unrelated
  local artifacts; this slice did not mutate or clean that worktree.
- The checker does not yet inspect PR state. It accepts issue/tracker and
  artifact context for the first slice.
- Path-scoped safety scans need final execution after this handoff is included.

## Forbidden Scope

Forbidden scope touched: false.

No worktrees, stashes, issues, branches, PRs, or untracked artifacts were
deleted, pruned, cleaned, staged, committed, pushed, closed, reopened, or
merged. The only worktree mutation was the user-requested isolated worktree for
this run.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for the workflow freshness guard.

Issue:
N/A - implementation issue recommended if desired

Contract:
docs/contracts/workflow_freshness_guard.md

Implementation handoff:
docs/implementation_handoffs/workflow_freshness_guard_comparison.md

Branch/worktree:
codex/workflow-freshness-guard in sibling worktree MythicEdge-workflow-freshness-guard

Goal:
Review the workflow freshness guard implementation against the contract. Confirm whether the template updates, advisory checker, tests, validation, and non-mutating boundaries satisfy the contract. Produce a contract-test report or findings-first review.

Review focus:
- confirm older workflow handoffs remain compatible;
- confirm freshness fields are recommended/advisory, not required as a hard gate;
- confirm current-status freshness summary is reporting metadata only;
- confirm tools/check_workflow_freshness.py is report-only and non-mutating;
- confirm branch mismatch, closed issue reentry, untracked artifact, missing artifact, GitHub unknown, and worktree path handling are covered;
- confirm no #331 CodeQL fixes or product behavior changes were included.

Do not:
- mutate worktrees, stashes, issues, branches, PRs, or untracked artifacts;
- make freshness checks a CI gate;
- implement #331 CodeQL fixes;
- change parser/runtime/workbook/webhook/App Script/Sheets/analytics/local-app/OpenAI/AI/coaching/production behavior;
- stage, commit, push, open a PR, merge, or close issues unless explicitly asked.

Suggested validation:
py -m pytest -q tests\test_check_workflow_freshness.py tests\test_check_agent_docs.py
py -m ruff check tools\check_workflow_freshness.py tests\test_check_workflow_freshness.py
py tools\check_agent_docs.py
py tools\check_workflow_freshness.py --issue 331 --branch codex/analytics-foundation --source-artifact docs\contracts\workflow_freshness_guard.md --target-artifact docs\implementation_handoffs\workflow_freshness_guard_comparison.md --include-worktrees --json
git diff --check
Run path-scoped protected-surface and secret/private-marker scans over changed files.

Final report must include:
- findings first, if any;
- verdict against the contract;
- files inspected;
- validation run;
- protected-surface status;
- secret/private-marker status;
- whether forbidden scope was touched;
- next recommended role;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "N/A - implementation issue recommended if desired"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/workflow_freshness_guard.md"
  target_artifact: "docs/implementation_handoffs/workflow_freshness_guard_comparison.md"
  risk_tier: "Medium"
  branch: "codex/workflow-freshness-guard"
  base_branch: "origin/codex/analytics-foundation"
  worktree: "MythicEdge-workflow-freshness-guard"
  freshness:
    current_branch: "codex/workflow-freshness-guard"
    intended_branch: "codex/analytics-foundation"
    upstream_branch: "origin/codex/analytics-foundation"
    branch_ahead_behind: "0 0"
    issue_state: "N/A"
    tracker_state: "N/A"
    source_artifact_status: "untracked candidate artifact in isolated worktree"
    target_artifact_status: "created in isolated worktree"
    local_dirty_state: "scoped workflow freshness files only"
    untracked_artifacts:
      - "docs/contracts/workflow_freshness_guard.md"
      - "tools/check_workflow_freshness.py"
      - "tests/test_check_workflow_freshness.py"
      - "docs/implementation_handoffs/workflow_freshness_guard_comparison.md"
    worktree_classification: "isolated implementation worktree created because primary checkout had active #331 work"
    freshness_verdict: "fresh_with_expected_isolation_warnings"
    recommended_route: "route_to_codex_e"
    verified_at: "2026-06-09"
  validation:
    - "py -m pytest -q tests\\test_check_workflow_freshness.py tests\\test_check_agent_docs.py -> passed, 24 tests"
    - "py -m ruff check tools\\check_workflow_freshness.py tests\\test_check_workflow_freshness.py -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "workflow freshness checker smoke against #331/codex/analytics-foundation -> command passed, result branch_mismatch expected from isolated worktree"
    - "workflow freshness checker smoke against isolated branch -> command passed, result artifact_untracked expected before submission"
    - "workflow freshness checker smoke against isolated branch with source and target artifacts -> command passed, result artifact_untracked expected before submission"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 2 expected workflow-template warnings"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "new-file ASCII/trailing-whitespace/final-newline checks -> passed"
  stop_conditions:
    - "Do not mutate worktrees, stashes, issues, branches, PRs, or untracked artifacts."
    - "Do not make freshness checks a CI gate without a later contract."
    - "Do not implement #331 CodeQL fixes in this workflow-freshness slice."
    - "Do not change product behavior or protected parser/workbook/analytics/local-app/AI surfaces."
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
