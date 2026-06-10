# Workflow Freshness Guard Contract

## Module

`workflow_freshness_guard`

Plain English: this contract defines a lightweight Mythic Edge workflow guard
for continuing Codex threads. The guard exists to catch stale handoffs,
closed-issue reentry, branch/worktree mismatch, and untracked artifact lifecycle
drift before implementation or submission begins.

This is a Codex B contract-writing artifact only. It does not implement tooling,
change product behavior, close issues, mutate worktrees, delete stashes, create
CI gates, or alter parser/workbook/analytics/local-app/AI behavior.

## Source Issue

No GitHub issue was supplied for this contract-writing pass.

Source evidence requested by the user:

- closed issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/302
  - https://github.com/Tahjali11/Mythic-Edge/issues/304
  - https://github.com/Tahjali11/Mythic-Edge/issues/315
  - https://github.com/Tahjali11/Mythic-Edge/issues/321
- open issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/330
  - https://github.com/Tahjali11/Mythic-Edge/issues/331
- current worktree list from `git worktree list`
- untracked artifact:
  `docs/contracts/codeql_code_scanning_alert_triage.md`
- workflow templates:
  - `docs/templates/workflow_handoff.md`
  - `docs/templates/current_status.md`
- governance checker:
  - `tools/check_agent_docs.py`
  - `tests/test_check_agent_docs.py`

Current observed branch during this contract pass:

```text
codex/analytics-foundation
```

Current observed local artifact drift:

```text
?? docs/contracts/codeql_code_scanning_alert_triage.md
```

## Tracker

N/A.

This contract is governance/workflow infrastructure. If a future issue is
created for implementation, that issue should link this contract as its source
artifact.

## Risk Tier

Medium.

Reasons:

- the first slice is governance/template/advisory tooling, not runtime code;
- the failure mode is real and repeated across issue handoffs, worktrees, and
  untracked artifacts;
- the guard can influence routing decisions across A-G workflow roles;
- over-enforcement could create ceremony or block low-risk work unnecessarily;
- any later hard gate or CI requirement must be separately contracted.

## Owning Layer

Workflow / Governance.

The guard owns workflow freshness metadata and routing recommendations only. It
does not own product truth, parser truth, analytics truth, local app truth,
GitHub issue lifecycle truth, or merge readiness by itself.

## Internal Project Area

Quality / Governance.

Adjacent areas:

- External / Collaboration Surface, because GitHub issues, PRs, and CodeQL
  alerts are collaboration/evidence surfaces;
- Generated / Local Artifacts, because untracked files and worktree-local
  artifacts need classification;
- Local App / UI, Parser, Analytics, and AI are protected downstream areas that
  must remain out of scope for this workflow guard.

## Truth Owner

Truth ownership for freshness inputs remains with the source systems:

- `git status` owns local dirty/untracked branch evidence;
- `git worktree list` owns local worktree evidence;
- GitHub issues and PRs own open/closed/merged state;
- durable repo artifacts own contract/handoff/report content;
- `tools/check_agent_docs.py` owns static governance-doc consistency checks;
- this workflow guard owns the classification and routing vocabulary for those
  inputs.

The guard must not treat a pasted handoff, chat memory, local skill, or older
issue comment as current truth until live repo/GitHub state is verified when it
matters.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
Git / GitHub / workflow artifacts / templates
  -> freshness classification
  -> advisory routing recommendation
  -> Codex role decision before implementation or submission
```

Forbidden reverse flow:

- a freshness warning must not close or reopen issues;
- a freshness warning must not delete or prune worktrees;
- a freshness warning must not stage, commit, push, or discard untracked files;
- a freshness warning must not override a current issue, accepted contract,
  Codex G completion comment, or user instruction;
- a freshness warning must not authorize protected product-surface changes.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/workflow_freshness_guard.md`

Expected Codex C implementation artifacts may include:

- updates to `docs/templates/workflow_handoff.md`
- updates to `docs/templates/current_status.md`
- an advisory, report-only workflow freshness checker, likely:
  `tools/check_workflow_freshness.py`
- focused tests for that checker, likely:
  `tests/test_check_workflow_freshness.py`
- optional static governance-doc checker updates:
  - `tools/check_agent_docs.py`
  - `tests/test_check_agent_docs.py`

Codex C may only update `tools/check_agent_docs.py` if it is validating static
template/doc shape. It must not turn live GitHub, worktree, or untracked
artifact checks into required `check_agent_docs` failures unless a later
contract explicitly authorizes that gate.

## Public Interface

### Freshness Field Model

Every continuing workflow thread should verify and, when relevant, record these
fields before implementation, review, submission, or deployer work begins.

Required verification fields:

- `current_branch`
- `intended_branch`
- `upstream_branch`
- `branch_ahead_behind`
- `worktree_path`
- `worktree_issue_hint`
- `issue_state`
- `tracker_state`
- `source_artifact_status`
- `target_artifact_status`
- `local_dirty_state`
- `untracked_artifacts`
- `related_open_prs`
- `last_known_merge_or_closeout`
- `freshness_verdict`
- `recommended_route`

Recommended optional fields:

- `source_issue`
- `parent_issue`
- `related_issues`
- `source_pr`
- `merge_commit`
- `expected_artifact`
- `artifact_tracked`
- `artifact_untracked`
- `artifact_staged`
- `artifact_missing`
- `artifact_superseded`
- `worktree_classification`
- `closed_issue_reentry_reason`
- `user_confirmation_required`

### Recommended `workflow_handoff` Additions

The first implementation slice should update `docs/templates/workflow_handoff.md`
to recommend, not require as a hard gate, these freshness fields:

```yaml
freshness:
  current_branch: ""
  intended_branch: ""
  upstream_branch: ""
  branch_ahead_behind: ""
  issue_state: ""
  tracker_state: ""
  source_artifact_status: ""
  target_artifact_status: ""
  local_dirty_state: ""
  untracked_artifacts:
    - ""
  worktree_classification: ""
  freshness_verdict: ""
  recommended_route: ""
  verified_at: ""
```

The template should say that older handoffs without `freshness` remain valid as
historical artifacts, but a continuing thread must verify freshness live when
the state could have changed.

### Recommended `current_status` Additions

The first implementation slice should update `docs/templates/current_status.md`
with a compact freshness section for status briefs:

```yaml
freshness_summary:
  branch: ""
  upstream: ""
  ahead_behind: ""
  worktree_count: ""
  dirty_paths:
    - ""
  untracked_candidate_artifacts:
    - ""
  stale_or_closed_issue_worktrees:
    - ""
  active_open_issues:
    - ""
  freshness_risks:
    - ""
  next_safe_route: ""
```

This is a reporting shape, not a product schema and not a CI contract.

### Advisory Checker Decision

The first slice should be both:

- docs/template update, and
- advisory tooling.

The checker should be report-only. It should never mutate state.

Suggested command shape:

```powershell
py tools\check_workflow_freshness.py --issue 331 --branch codex/analytics-foundation --json
py tools\check_workflow_freshness.py --issue 331 --branch codex/analytics-foundation
```

Optional flags for Codex C to evaluate:

- `--parent-issue`
- `--tracker`
- `--source-artifact`
- `--target-artifact`
- `--expected-branch`
- `--include-worktrees`
- `--no-gh`

`--no-gh` should let the checker run from local Git/artifact evidence only
when GitHub is unavailable. In that mode, issue/PR freshness must be reported as
`unknown`, not assumed open or closed.

## Inputs

### Local Git State

Source commands:

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/<branch>
git worktree list
```

Required interpretation:

- dirty tracked files must be listed, not summarized away;
- untracked files must be classified before staging or ignoring;
- branch ahead/behind must be recorded when a continuing thread might submit,
  review, or merge work;
- worktree list must be treated as local coordination evidence only.

### GitHub Issue And PR State

Source commands:

```powershell
gh issue view <issue> --json number,title,state,url,closedAt,body,comments
gh pr view <pr> --json number,title,state,mergedAt,mergeCommit,baseRefName,headRefName
```

Required interpretation:

- open issues may continue through the role named by the handoff;
- closed issues require a reentry reason before new work continues;
- merged PR evidence may justify issue closure or follow-up routing, but only
  Codex G should perform lifecycle closeout unless the user explicitly asks
  otherwise;
- if GitHub is unavailable, the checker must report unknown issue freshness and
  route to manual user confirmation or a live refresh.

### Durable Artifact State

Source evidence:

- existence of expected artifact path;
- Git tracked/untracked/staged state;
- file path matches the handoff target;
- artifact title/content references the same issue or source context;
- artifact is not a generated/private/local artifact.

Required interpretation:

- tracked artifacts on the intended branch are official repo artifacts;
- untracked artifacts are candidate artifacts until staged/committed through
  the workflow;
- missing artifacts require B revision, C blocker, or cleanup decision;
- stale/superseded local artifacts require classification, not silent deletion.

## Outputs

### Freshness Verdict

The advisory checker and updated templates should use these verdicts:

- `fresh`
- `fresh_with_warnings`
- `stale_handoff`
- `closed_issue_reentry`
- `branch_mismatch`
- `worktree_mismatch`
- `artifact_untracked`
- `artifact_missing`
- `artifact_superseded_or_stale`
- `github_state_unknown`
- `blocked_needs_user_decision`

### Recommended Routes

Route outcomes:

- `continue_current_role`
- `route_to_codex_a`
- `route_to_codex_b`
- `route_to_codex_c`
- `route_to_codex_e`
- `route_to_codex_f`
- `route_to_codex_g`
- `ask_user`
- `cleanup_classification_only`
- `stop_noop`

The checker must not automatically perform the route. It only reports the
recommended route.

### Report Shape

Human-readable output should include:

- branch/worktree summary;
- issue/tracker summary;
- source/target artifact summary;
- dirty and untracked path summary;
- freshness verdict;
- recommended route;
- explicit stop conditions.

JSON output should be deterministic and include:

```json
{
  "result": "fresh_with_warnings",
  "issue": {
    "number": 331,
    "state": "OPEN",
    "url": "https://github.com/Tahjali11/Mythic-Edge/issues/331"
  },
  "branch": {
    "current": "codex/analytics-foundation",
    "intended": "codex/analytics-foundation",
    "upstream": "origin/codex/analytics-foundation",
    "ahead": 0,
    "behind": 0
  },
  "artifacts": [
    {
      "path": "docs/contracts/codeql_code_scanning_alert_triage.md",
      "status": "untracked_candidate_artifact",
      "recommended_route": "route_to_codex_c_after_preservation"
    }
  ],
  "worktrees": [
    {
      "path": "<local-worktree>/MythicEdge-live-capture-diagnostics-302",
      "branch": "codex/live-capture-diagnostics-restore-302",
      "classification": "closed_issue_worktree_candidate"
    }
  ],
  "warnings": [],
  "stop_conditions": []
}
```

The example values are illustrative. The checker must compute current values.

## Invariants

- Freshness checks are advisory unless a later contract makes a specific field
  required by a role.
- Freshness checks must run before implementation on stale or ambiguous
  handoffs.
- The guard must distinguish local checkout state from project truth.
- The guard must not treat closed issues as always invalid; legitimate follow-up
  work can continue if the route is explicit.
- The guard must not treat untracked files as disposable.
- The guard must not treat worktree existence as proof that work is active.
- The guard must not classify private/generated artifacts by reading their
  contents.
- The guard must not mutate Git, GitHub, worktrees, stashes, runtime files, or
  product state.
- Low-risk typo/docs work should not be blocked by expensive live checks when a
  local verification is enough.

## Error Behavior

### Closed Issue Reentry

If the source issue is closed:

- classify as `closed_issue_reentry`;
- inspect closure comments for completion evidence if available;
- allow continuation only when the handoff or user explicitly names:
  - a follow-up issue;
  - a reconciliation role;
  - a blocker resolution task;
  - a Codex G lifecycle audit;
  - a docs-only postmortem or contract refinement.

If no legitimate reentry reason exists, route to `ask_user` or
`cleanup_classification_only`.

### Branch Or Worktree Mismatch

If the current branch differs from the intended branch:

- classify as `branch_mismatch`;
- do not edit until the user or handoff authorizes working on the observed
  branch;
- if unrelated worktree changes exist, preserve them and route to Codex A/B/G
  depending on the source of the mismatch.

If a separate worktree exists for the same issue:

- classify it as `possible_duplicate_worktree`;
- do not delete or prune it;
- report the path, branch, issue hint, and whether the issue is open or closed;
- ask the user or route to Codex G if cleanup/lifecycle handling is needed.

### Untracked Artifact Lifecycle Drift

If a target artifact exists only as an untracked file:

- classify as `artifact_untracked`;
- inspect whether it appears to match the active issue and expected target path;
- if complete, route to Codex C/F/G according to the workflow stage and note
  that preservation/submission is required before another worktree can rely on
  it;
- if incomplete, route back to Codex B revision;
- if stale or superseded, route to cleanup classification only;
- do not delete, move, stage, or commit it without explicit role/user
  authorization.

### GitHub Unavailable

If `gh issue view` or `gh pr view` cannot verify state:

- classify issue/PR freshness as `github_state_unknown`;
- do not assume open or closed;
- proceed only for local docs inspection or low-risk artifact classification;
- route implementation/submission/deployment work to user confirmation or a
  later live refresh.

## Stale Issue / Worktree / Artifact Classification Model

### Issue State Classes

- `open_active`: issue is open and matches the handoff target.
- `open_related`: issue is open but is parent, tracker, or sibling context.
- `closed_completed`: issue is closed with completion evidence.
- `closed_superseded`: issue is closed because work moved elsewhere.
- `closed_needs_reentry_reason`: issue is closed and the new prompt wants more
  work without naming a follow-up or reconciliation reason.
- `unknown`: issue state could not be verified.

### Worktree Classes

- `primary_current_worktree`: current checkout path.
- `active_issue_worktree`: worktree branch appears tied to an open issue.
- `closed_issue_worktree_candidate`: worktree branch appears tied to a closed
  issue, such as observed #302, #304, #315, and #321 worktrees.
- `review_or_reconciliation_worktree`: worktree may remain useful for review,
  recovery, or diff inspection.
- `unknown_or_unlinked_worktree`: no reliable issue hint is available.
- `cleanup_candidate_user_confirmation_required`: safe to ask about, never safe
  to delete automatically.

### Artifact Classes

- `tracked_official_artifact`: tracked on current branch.
- `untracked_candidate_artifact`: local file appears to match a requested
  durable artifact but has not been submitted.
- `staged_pending_submission`: staged for commit, but not yet official on the
  branch.
- `missing_expected_artifact`: target path absent.
- `superseded_local_artifact`: path or content points to a completed/replaced
  scope.
- `private_or_generated_forbidden_artifact`: must not be committed; report path
  classification without dumping contents.
- `unknown_requires_user_or_role_review`: cannot safely classify automatically.

## Route Back Rules

Route to Codex A when:

- the issue is closed and the requested work is really a new problem;
- the handoff source is stale or superseded and needs reframing;
- a new GitHub issue or tracker relationship is needed.

Route to Codex B when:

- the target contract is missing, untracked, incomplete, or stale;
- a handoff points to a contract that no longer matches current issue state;
- freshness fields reveal ambiguous scope or route decisions.

Route to Codex C when:

- the source issue is open;
- the contract is tracked or explicitly available in the current worktree;
- branch/worktree state is aligned or the user authorizes the observed branch;
- dirty/untracked files are classified and do not conflict.

Route to Codex E when:

- implementation exists and needs contract verification against current issue,
  branch, and artifact state;
- a stale handoff claims completion but the artifacts or validation need
  independent confirmation.

Route to Codex G when:

- the issue is closed or merge evidence exists and lifecycle status needs
  reconciliation;
- stale worktree cleanup, branch deletion, tracker closure, or issue closeout is
  being considered;
- PR/merge readiness needs deployer-level verification.

Route to the user when:

- deletion, cleanup, issue reopening/closure, branch switching, or artifact
  discard is needed;
- GitHub state cannot be verified but implementation/submission would depend on
  it;
- multiple plausible routes exist with different workflow consequences.

## Side Effects

Codex B side effects:

- creates this contract only.

Expected Codex C side effects, if implemented:

- edits workflow templates;
- may add a report-only checker;
- may add focused tests for that checker;
- may update static governance-doc consistency checks for new template fields.

Forbidden side effects:

- no worktree deletion, pruning, or mutation;
- no stash mutation;
- no issue closure or reopening;
- no PR creation or merge;
- no CI gate creation;
- no parser/runtime/workbook/analytics/local-app/OpenAI/AI behavior changes;
- no generated/private/local artifact creation or cleanup.

## Compatibility

Older handoffs remain valid historical artifacts. A missing `freshness` block in
an older handoff should not invalidate the artifact. It should trigger live
verification in the continuing thread.

Existing `workflow_handoff` keys remain valid:

- `issue`
- `tracker`
- `completed_thread`
- `next_thread`
- `source_artifact`
- `target_artifact`
- `risk_tier`
- `branch`
- `validation`
- `stop_conditions`

The first slice should add recommended freshness guidance without breaking old
handoffs or requiring every past contract/report to be rewritten.

## Tests Required

Codex C should add focused tests for any new advisory checker and any static
template/schema changes.

Suggested commands:

```powershell
py -m pytest -q tests\test_check_agent_docs.py
py -m pytest -q tests\test_check_workflow_freshness.py
py tools\check_agent_docs.py
py tools\check_workflow_freshness.py --issue 331 --branch codex/analytics-foundation --source-artifact docs\contracts\codeql_code_scanning_alert_triage.md
git diff --check
```

Path-scoped safety scans:

```powershell
@'
docs/contracts/workflow_freshness_guard.md
docs/templates/workflow_handoff.md
docs/templates/current_status.md
tools/check_workflow_freshness.py
tests/test_check_workflow_freshness.py
tools/check_agent_docs.py
tests/test_check_agent_docs.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
docs/contracts/workflow_freshness_guard.md
docs/templates/workflow_handoff.md
docs/templates/current_status.md
tools/check_workflow_freshness.py
tests/test_check_workflow_freshness.py
tools/check_agent_docs.py
tests/test_check_agent_docs.py
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Codex C should adjust the path list to changed files only.

## Acceptance Criteria

- `docs/templates/workflow_handoff.md` documents freshness fields or explicitly
  links to the freshness guard contract.
- `docs/templates/current_status.md` includes a freshness summary shape for
  current repo/issue/worktree status.
- A report-only checker exists or Codex C documents why the first slice should
  remain template-only.
- The checker can classify:
  - open issue continuation;
  - closed issue reentry;
  - branch mismatch;
  - worktree mismatch;
  - untracked candidate artifact;
  - missing expected artifact;
  - GitHub unavailable/unknown state.
- The checker reports but does not mutate.
- Static governance-doc tests pass.
- The implementation preserves low-risk escape hatches and avoids turning
  freshness into a broad CI gate.
- No product behavior or protected parser/workbook/analytics/local-app/AI
  surface is changed.

## Open Questions / Contract Risks

- Whether the checker should live as a standalone `tools/check_workflow_freshness.py`
  or as a subcommand of an existing workflow tool is left to Codex C if a clear
  local pattern exists.
- Whether future Codex F/G should require freshness output before PR submission
  is intentionally deferred.
- Whether stale worktree cleanup should get its own issue is intentionally
  deferred; this contract only classifies and routes.
- Whether untracked candidate artifacts should be auto-detected by matching
  `docs/contracts`, `docs/implementation_handoffs`, and
  `docs/contract_test_reports` paths is allowed, but the checker must not read
  private/generated artifacts to classify them.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Source contract:
docs/contracts/workflow_freshness_guard.md

Current branch:
codex/analytics-foundation

Goal:
Implement the first workflow freshness guard slice without product behavior
changes. Compare the current workflow templates and agent-doc checker against
the contract, then make the smallest docs/tooling changes needed.

Expected implementation handoff:
docs/implementation_handoffs/workflow_freshness_guard_comparison.md

Required source context:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/workflow_handoff.md
- docs/templates/current_status.md
- docs/contracts/workflow_freshness_guard.md
- tools/check_agent_docs.py
- tests/test_check_agent_docs.py
- current `git status --short --branch --untracked-files=all`
- current `git worktree list`
- live issue state for #302, #304, #315, #321, #330, and #331 when GitHub is available

Implement only the contracted workflow freshness surfaces:
- update workflow/current-status templates with recommended freshness fields;
- add a report-only advisory checker if straightforward;
- add focused tests for any checker or static template validation;
- preserve older handoff compatibility;
- keep the checker advisory and non-mutating.

Do not:
- close or reopen issues;
- delete, prune, move, or mutate worktrees or stashes;
- stage, commit, push, open a PR, or merge unless explicitly asked;
- make freshness a CI gate;
- implement CodeQL fixes from #331;
- change parser/runtime/workbook/webhook/App Script/Sheets/analytics/local-app/OpenAI/AI/coaching/production behavior;
- read, print, copy, hash, or commit raw logs, private JSONL artifacts, generated SQLite files, runtime artifacts, failed posts, workbook exports, secrets, credentials, tokens, webhook URLs, spreadsheet IDs, environment values, or local-only artifacts.

Validation:
- py -m pytest -q tests\test_check_agent_docs.py
- py -m pytest -q tests\test_check_workflow_freshness.py, if added
- py tools\check_agent_docs.py
- run the new advisory checker against #331 / codex/analytics-foundation if added
- git diff --check
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Final output:
- role performed
- contract used
- implementation handoff path
- files changed
- freshness model implemented
- advisory checker behavior, if added
- validation run
- protected-surface and secret/private-marker status
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "N/A - implementation issue recommended if desired"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/workflow_freshness_guard.md"
  target_artifact: "docs/implementation_handoffs/workflow_freshness_guard_comparison.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  internal_project_area: "Quality / Governance"
  truth_owner: "Workflow / Governance freshness classification"
  bridge_code_status: "shared_support"
  validation:
    - "git status --short --branch --untracked-files=all"
    - "git worktree list"
    - "gh issue view 302/304/315/321/330/331"
    - "git diff --check"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not mutate worktrees, stashes, issues, branches, PRs, or untracked artifacts."
    - "Do not make freshness checks a CI gate without a later contract."
    - "Do not implement #331 CodeQL fixes in this workflow-freshness slice."
    - "Do not change product behavior or protected parser/workbook/analytics/local-app/AI surfaces."
```
