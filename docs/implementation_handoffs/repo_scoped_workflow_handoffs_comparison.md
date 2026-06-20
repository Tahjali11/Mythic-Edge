# Repo-Scoped Workflow Handoffs Implementation Handoff

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/506
- Tracker: N/A
- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Base branch: `main`
- Target branch: `main`
- Contract: `docs/contracts/repo_scoped_workflow_handoffs.md`
- Risk tier: Medium

## Comparison Summary

The contract requires future Mythic Edge workflow handoffs to identify the
owning GitHub repository and public URL, keep local absolute paths out of
public artifacts, distinguish base/target/working branches, and hard stop
before mutation when a local checkout cannot be verified against the handoff
repository identity.

Current templates and static checks previously preserved issue, tracker, role,
artifact, risk, branch, validation, and stop-condition metadata, but they did
not require `repository`, `repository_url`, `base_branch`, or `target_branch`.
The GitHub module issue template also exposed only one generic branch field.

## Changes Made

- Added `repository`, `repository_url`, `base_branch`, and `target_branch` to
  canonical public workflow handoff examples.
- Preserved `branch` as a compatibility field for the current working branch.
- Added public-safe local prompt guidance for `Operating repo/worktree:` outside
  public `workflow_handoff` blocks.
- Added checkout mismatch hard-stop guidance and read-only sibling repository
  reference guidance.
- Added repository identity and branch routing fields to the GitHub module
  issue template.
- Added a `workflow_handoff_schema` section to `docs/agent_rules.yml`.
- Updated `tools/check_agent_docs.py` so static docs checks require the new
  public handoff fields and issue-template fields.
- Added focused checker tests for missing `repository_url` in the canonical
  handoff template and issue template.

## Files Changed

- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/templates/workflow_handoff.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/contract_test_report.md`
- `tools/check_agent_docs.py`
- `tests/test_check_agent_docs.py`
- `docs/implementation_handoffs/repo_scoped_workflow_handoffs_comparison.md`

The Codex B source contract `docs/contracts/repo_scoped_workflow_handoffs.md`
was present in the worktree and used as the source artifact. This Codex C pass
did not rewrite it.

## Validation Run

- `python3 tools/check_agent_docs.py` -> passed
- `python3 -m pytest -q tests/test_check_agent_docs.py` -> 19 passed
- `python3 -m ruff check tools/check_agent_docs.py tests/test_check_agent_docs.py` -> passed
- `git diff --check` -> passed
- path-scoped secret/private-marker scan over 13 changed paths -> passed with
  0 forbidden and 0 warnings
- path-scoped protected-surface scan over 13 changed paths -> passed with 0
  forbidden findings and expected workflow-authority warnings for the
  governance docs/templates authorized by #506

## Remaining Risks

- Historical issue comments, PR bodies, and old handoffs remain unchanged by
  design, so older artifacts may still omit repository identity.
- The checker remains a static governance-doc consistency check. It does not
  perform live remote validation, inspect GitHub state, enforce CI policy, or
  authorize cross-repo automation.
- Future sibling repositories will need to adopt the same public handoff shape
  in their own repo-scoped governance artifacts.

## Recommended Next Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #506, repo-scoped workflow handoffs.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Base branch:
main

Target branch:
main

Review:
- docs/contracts/repo_scoped_workflow_handoffs.md
- docs/implementation_handoffs/repo_scoped_workflow_handoffs_comparison.md
- docs/templates/workflow_handoff.md
- docs/templates/problem_representation.md
- docs/templates/module_contract.md
- docs/templates/implementation_handoff.md
- docs/templates/contract_test_report.md
- .github/ISSUE_TEMPLATE/module_workflow.yml
- .github/pull_request_template.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- tools/check_agent_docs.py
- tests/test_check_agent_docs.py

Goal:
Verify the implementation satisfies the repo-scoped workflow handoff contract
without rewriting historical handoffs, leaking local absolute paths into public
artifacts, mutating other repositories, adding CI gates, or changing product
behavior.

Reviewer focus:
- canonical handoff templates include repository and repository_url
- branch routing uses base_branch and target_branch while preserving branch
- public examples contain no local absolute paths
- Operating repo/worktree guidance stays outside public workflow_handoff blocks
- checkout mismatch behavior is a hard stop before mutation
- sibling repository references are read-only unless separately routed
- checker/tests cover the new static schema expectations

Validation to rerun:
- python3 tools/check_agent_docs.py
- python3 -m pytest -q tests/test_check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker scan for changed files
- path-scoped protected-surface scan for changed files

Do not:
- target or mutate any other repository
- rewrite historical issue comments, PR bodies, or old handoffs
- add local absolute paths to public docs, issues, PR templates, or handoff examples
- implement live remote-check automation, cross-repo automation, or new CI gates
- change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching behavior
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/506"
  tracker: ""
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/repo_scoped_workflow_handoffs.md"
  target_artifact: "docs/implementation_handoffs/repo_scoped_workflow_handoffs_comparison.md"
  risk_tier: "Medium"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  internal_project_area: "Quality / Governance"
  truth_owner: "workflow routing metadata; GitHub and git remain authoritative"
  bridge_code_status: "N/A"
  allowed_read_only_references: []
  validation:
    - "python3 tools/check_agent_docs.py"
    - "python3 -m pytest -q tests/test_check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan for changed files"
    - "path-scoped protected-surface scan for changed files"
  stop_conditions:
    - "Hard stop before mutation if the local checkout remote does not match repository_url."
    - "Do not add local absolute paths to public docs, issues, PR templates, or handoff examples."
    - "Do not rewrite historical issue comments, PR bodies, or old handoffs."
    - "Do not mutate any other repository or worktree."
    - "Do not change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching behavior."
```
