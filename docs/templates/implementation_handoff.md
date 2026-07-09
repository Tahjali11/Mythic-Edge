# Implementation Handoff

## Issue

Link to the GitHub issue.

## Tracker

Link to the tracker issue, if any.

## Contract

Link to the module contract.

## Internal Project Area

Name the contracted internal project area from `docs/internal_project_map.md`.

## Truth Owner

Name the truth owner confirmed during implementation.

## Bridge-Code Status

State one of `not_bridge_code`, `bridge_code`, `shared_support`,
`ambiguous_pending_follow_up`, or `deferred_future_boundary`.

## Role Performed

Codex C: Module Implementer, or Codex D: Module Fixer.

## What Changed

Plain-English summary of the implementation or fix.

## Files Changed

- TODO

## Code Changed

State whether runtime code changed. If yes, list the owned files and behavior
surface.

## Tests Added Or Updated

- TODO

## Interface Changes

List changed function signatures, payload fields, workbook columns, environment
variables, script entrypoints, docs schemas, issue lifecycle rules, or PR
lifecycle rules.

## Contracted Area Status

State whether the implementation stayed inside the contracted internal project
area and whether any downstream consumers or bridge-code boundaries were
touched.

## Governance Checklist Outcome

- Public-safe/no-echo boundary:
- Vocabulary and example coherence:
- Authority/readiness semantics:
- Fail-closed schema or validator checks:
- Protected-surface rollout phase:

Use "not applicable" only when the contract clearly does not involve that
check. Prerequisite success should not be described as sufficient authority for
durable writes, source-repo action, gate activation, enforcement, readiness,
or truth/assurance claims unless the current issue and role explicitly
authorize it.

## Validation Run

```bash

```

## Still Unverified

- TODO

## Reviewer Focus

Ask the contract test thread to pay special attention to:

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
  completed_thread: "C"
  next_thread: "E"
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  base_branch: ""
  target_branch: ""
  branch: ""
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
  role: "C_or_D"
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
