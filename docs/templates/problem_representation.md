# Problem Representation

Use this for Codex A. It should define the problem clearly enough that Codex B
can write a contract without reconstructing chat history.

## Summary

One or two sentences describing the bug, feature, audit target, or confusing
behavior.

## Source Request Or Issue

Link to the originating request or GitHub issue.

## Tracker

Link to the tracker issue, if any.

## Lane Activation

Name the repo active slot and whether this issue is active, parked, deferred,
or only tracker-selected next work.

```yaml
lane_activation:
  repo: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: ""
  lane_status: ""
  tracker_selected_next_lane: ""
  exception:
    name: ""
    blocked_active_issue_or_pr: ""
    reason: ""
    allowed_scope: ""
    expiration_condition: ""
    authorized_by: ""
    recorded_in: ""
```

Use an exception only for a named, scoped, expiring second lane:
`security_hotfix`, `privacy_or_raw_log_leak`, `data_loss_or_corruption`,
`ci_blocking_all_work`, `dependency_security_update`,
`blocked_lane_unblocker`, `repo_bootstrap_or_split`, or
`explicit_user_override`.

## Intended Behavior

Describe what the code, document, workflow, or artifact is supposed to do.

## Actual Behavior

Describe what is happening now. Include exact bad output, missing output, or
confusing state when known.

## Why This Matters

Explain the user impact, debugging impact, workbook impact, downstream
analytics impact, governance risk, or maintenance cost.

## Project Layer

Choose the main layer:

- MTGA raw log source
- parser and state interpretation
- webhook / transport layer
- workbook landing sheets
- helper formulas
- dashboard / reporting tabs
- AI analysis
- repository coordination and agent workflow

## Internal Project Area

Choose the ADR-0006/internal-project-map area when it helps routing:

- Parser
- Corpus / Provenance
- Analytics
- Local App / UI
- Workbook / Transport
- Quality / Governance
- Future AI Integration
- Shared Support
- Generated / Local Artifacts
- External / Collaboration Surface
- N/A / unclear

Future AI Integration is deferred vocabulary only. Naming it does not authorize
OpenAI/model-provider runtime integration, AI-owned truth, hidden-card truth,
gameplay correctness truth, or strategic certainty.

If this is bridge-code work, name both source and consuming project areas.

## First Bad Value

Name the first observed place where data, state, authority, or routing becomes
wrong or ambiguous. If unknown, list inspection points in order.

## Inputs

List representative logs, payloads, fixtures, workbook tabs, docs, prompts,
commands, issues, PRs, or artifacts involved.

## Expected Output

List the final parser-managed fields, webhook rows, workbook columns, visible
dashboard effect, docs artifact, workflow decision, or GitHub outcome expected.

## Scope

In scope:

- TODO

Out of scope:

- TODO

## Governance And Authority Checks

For validator, preflight, dry-run, report-only, review-ready, advisory, or
no-blocking-finding states, state whether the status is prerequisite evidence
only. Do not frame it as authority for durable writes, source-repo action, gate
activation, protected-surface enforcement, readiness, or truth claims unless
the current issue and role explicitly authorize that stronger state.

If protected-surface enforcement may be relevant, name the current rollout
phase: measurement, advisory baseline, candidate selection, report-only gate,
or blocking enforcement.

For public artifacts, name public-safe/no-echo boundaries. Unsafe private
source values should become symbolic categories, redacted placeholders,
bucketed values, or fail-closed rejections instead of being pasted back.

## Risks And Likely Breakpoints

List likely import, shared state, interface, workbook, deployment, issue,
tracker, PR lifecycle, authority, privacy, or data-drift risks.

## Validation Evidence Needed

List the smallest checks that would prove the issue is fixed or the artifact is
complete.

```bash

```

## Open Questions

- TODO

## Next Workflow Action

Next role:

Pasteable prompt:

```text

```

```yaml
workflow_handoff:
  repository: ""
  repository_url: ""
  issue: ""
  tracker: ""
  completed_thread: "A"
  next_thread: "B"
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  base_branch: ""
  target_branch: ""
  branch: ""
  lane_activation:
    repo: ""
    active_issue_or_lane: ""
    lane_status: ""
    tracker_selected_next_lane: ""
    exception:
      name: ""
      blocked_active_issue_or_pr: ""
      reason: ""
      allowed_scope: ""
      expiration_condition: ""
      authorized_by: ""
      recorded_in: ""
  validation:
    - ""
  stop_conditions:
    - ""
```

For medium-risk and high-risk work, include:

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "A"
  risk_tier: ""
  global_router_read: false
  repo_agents_read: false
  repo_rules_read: false
  repo_constitution_read: false
  repo_workflow_read: false
  role_doc_read: false
  issue_or_tracker_read: false
  contract_or_handoff_read: false
  accepted_adrs_read:
    - ""
  protected_surfaces:
    - ""
  authority_conflicts_found: false
  authority_conflict_notes: ""
  stop_conditions:
    - ""
```
