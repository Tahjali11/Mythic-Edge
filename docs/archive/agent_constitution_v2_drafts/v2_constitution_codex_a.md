---
status: draft
source_label: "Codex A: Thinker"
related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/1"
draft_type: "v2 constitution update proposal"
replaces_existing_constitution: false
---

# v2 Constitution: Codex A

This is a standalone Codex A: Thinker draft. It does not replace
`docs/agent_constitution.md`.

This file proposes updates to the V1 Mythic Edge Agent Constitution based on
how the workflow has actually been used across module audits, tracker updates,
issue closure, PR merge handoffs, and parser-resilience planning.

## Executive Summary

V1 taught Codex how to do the work.

V2 should also teach Codex how to finish the work cleanly.

The strongest V2 improvement is to make the constitution more machine-readable
and more modular:

- keep `AGENTS.md` as the short entrypoint
- keep `docs/agent_constitution.md` as the global human-readable constitution
- add a machine-readable rule index
- keep role-specific behavior in role files
- add issue, PR, tracker, and merge lifecycle rules
- add current-status and source-priority rules
- preserve every V1 sacred safety rule

## Sacred V1 Rules To Preserve

These rules must not be weakened by V2:

```yaml
sacred_rules:
  parser_truth_ownership:
    rule: "Parser and state layers own event interpretation, match facts, and game facts."
    cannot_move_truth_to:
      - workbook formulas
      - dashboard logic
      - Apps Script transport
      - webhook transport
      - AI-generated interpretation

  secret_and_local_artifact_safety:
    never_commit:
      - secrets
      - webhook URLs
      - API keys
      - tokens
      - credentials
      - local MTGA logs
      - failed posts
      - runtime status files
      - generated card data
      - raw workbook exports

  high_risk_change_gate:
    requires:
      - problem representation
      - module contract
      - implementation against contract
      - independent review or contract test
      - validation evidence

  protected_surfaces:
    require_explicit_problem_and_contract:
      - webhook payload shape
      - workbook schema
      - deployed Apps Script assumptions
      - match identity
      - game identity
      - deduplication
      - final reconciliation
      - winner fields
      - play/draw fields
      - mulligan counts

  validation_truth:
    rule: "Do not claim validation passed without command output, CI evidence, corrected output, or a verified code path."
```

## Recommended Documentation Shape

Codex performs best when the first-read document is short and points to
specialized rules. V2 should optimize for relevant-section reading, not full
document reading.

```yaml
recommended_docs:
  entrypoint:
    path: "AGENTS.md"
    purpose: "Tiny high-priority summary Codex is likely to read first."
    max_style: "short, directive, links out"

  global_constitution:
    path: "docs/agent_constitution.md"
    purpose: "Human-readable global rules and safety model."
    max_style: "moderate length, stable principles"

  machine_rule_index:
    path: "docs/agent_rules.yml"
    purpose: "Machine-readable routing, role, lifecycle, and safety rules."
    max_style: "terse YAML"

  role_docs:
    path: "docs/agent_threads/*.md"
    purpose: "Human-readable role instructions."
    max_style: "short, role-specific"

  role_specs:
    path: "docs/agent_threads/*.yml"
    purpose: "Machine-readable role inputs, outputs, permissions, stop conditions."
    max_style: "strict YAML"

  templates:
    path: "docs/templates/*.md"
    purpose: "Reusable artifact shapes."
    max_style: "copyable forms"
```

## Whole File Vs Modular Reading

### Whole Constitution File

Pros:

- easier for a human to browse
- fewer files to maintain
- one obvious source of truth
- simpler for early project stages

Cons:

- higher token cost
- more likely to be truncated
- harder for Codex to find role-specific constraints
- more repeated rules
- more tempting for agents to skim

### Modular Constitution Package

Pros:

- Codex can read only relevant sections
- role files stay short and precise
- machine-readable YAML can reduce ambiguity
- easier to update one workflow area without touching everything
- better for long-running multi-thread projects

Cons:

- more files to maintain
- needs a clear authority order
- risk of duplicate or conflicting rules
- requires a machine-readable index or map

Recommendation:

```yaml
recommendation:
  use: "modular constitution package"
  keep_human_entrypoint: true
  add_machine_readable_index: true
  avoid_duplicate_rules: true
```

## Source Artifact Priority

V2 should tell Codex which project artifact to trust when sources disagree.

```yaml
source_priority:
  - active system and developer instructions
  - explicit user instruction in current thread
  - root AGENTS.md
  - current GitHub issue
  - current pull request
  - module contract
  - implementation handoff
  - review or contract-test report
  - docs/agent_constitution.md
  - role-specific docs in docs/agent_threads
  - workflow templates in docs/templates
  - older docs and examples
  - prior chat memory

conflict_policy:
  if_safety_rule_conflicts_with_convenience:
    action: "prefer safety"
  if_contract_conflicts_with_implementation:
    action: "stop and route to Module Contract Writer or user"
  if_user_request_conflicts_with_non_negotiable:
    action: "call out conflict and ask before proceeding"
  if_two_codex_suggestions_conflict:
    action: "prefer the shorter, safer, more testable rule"
```

## GitHub State Verification

Codex should not answer current repo-status questions from memory when `gh` can
verify the answer.

```yaml
github_state_verification:
  must_verify_with_gh_when_user_asks_about:
    - open issues
    - issue closure readiness
    - pull request status
    - draft status
    - merge status
    - base branch
    - merge commit
    - CI status
    - tracker queue state
    - whether work is completed

  useful_commands:
    issue_view: "gh issue view <number> --comments --json number,title,state,body,comments,labels,url"
    issue_list: "gh issue list --state open --limit 50 --json number,title,labels,url,updatedAt"
    pr_view: "gh pr view <number> --json number,title,state,isDraft,mergedAt,mergeCommit,baseRefName,headRefName,statusCheckRollup,url"
    pr_list: "gh pr list --state open --limit 30 --json number,title,isDraft,baseRefName,headRefName,statusCheckRollup,url"
```

## Issue Lifecycle Rules

V2 should define issue types and closure rules.

```yaml
issue_lifecycle:
  tracker:
    closes_when: "entire tracked queue or phase is complete"
    do_not_close_when: "one child module finishes"
    required_update_events:
      - child issue created
      - child PR merged
      - child issue closed
      - child blocked
      - next queue item changes

  module_audit:
    closes_when_all_true:
      - module contract exists
      - implementation or comparison handoff exists
      - review or contract-test report exists
      - PR merged into approved base branch
      - CI passed or failure explained
      - tracker updated if applicable

  bug:
    closes_when_all_true:
      - fix PR merged
      - validation recorded
      - completion comment names PR and merge commit
      - no follow-up implementation implied

  planning_or_docs:
    closes_when: "docs fully satisfy the issue and no implementation remains"
    remains_open_when: "docs define future implementation work"
    alternative: "open a follow-up implementation issue, then close planning issue with link"

  constitution:
    closes_when_all_true:
      - rule change merged
      - affected role docs or templates updated if needed
      - validation recorded
      - decision note posted
      - no remaining amendment work implied
```

## Pull Request Lifecycle Rules

```yaml
pull_request_lifecycle:
  default_state: "draft"
  default_module_audit_base: "codex/parser-module-audit-suite"
  main_target_requires_explicit_user_approval: true

  ready_to_mark_ready_when_all_true:
    - review has no blocking findings
    - required validation passed or failure explained
    - PR scope matches linked issue and contract
    - no secrets or local artifacts included
    - base branch is correct

  merge_ready_when_all_true:
    - PR is not draft
    - checks pass or user explicitly waives
    - no blocking review findings
    - base branch is correct
    - issue closing behavior is correct

  after_merge:
    - close fully satisfied module or bug issues
    - update tracker if applicable
    - leave planning/docs issue open when implementation remains
    - name next queue item when applicable
```

## Tracker Hygiene

Tracker updates should be mandatory for module audit work.

```yaml
tracker_update_required_when:
  - module issue created
  - module PR opened
  - module PR merged
  - module issue closed
  - module blocked
  - next queue item changes

tracker_update_fields:
  - module name
  - issue number
  - PR number
  - merge commit if merged
  - durable artifacts produced
  - validation or CI status
  - next queue item
  - related open issues
```

## Role Split Recommendation

V1 has one Module Submitter role. Actual usage suggests splitting the final
publishing work into two roles.

```yaml
roles:
  F1_submitter:
    owns:
      - inspect worktree
      - stage intended files
      - commit
      - push branch
      - open or update draft PR
    must_not:
      - merge PR
      - close issue unless explicitly asked

  F2_integrator:
    owns:
      - verify PR readiness
      - mark PR ready
      - merge approved PR into approved base
      - close completed issues
      - update tracker
      - sync integration branch status
    must_not:
      - merge into main unless explicitly approved
      - bypass failing CI without explicit user waiver
```

Recommendation:

```yaml
recommended_change:
  split_submitter_role: true
  new_role_name: "Integration Deployer"
  route_after_clean_review: "F1 Submitter or F2 Integrator depending on whether PR already exists"
```

## Current Status Block

V2 should require status summaries to include a compact machine-readable block.

```yaml
repo_status:
  branch: ""
  open_issues:
    - number: ""
      title: ""
      purpose: ""
      next_action: ""
  open_prs:
    - number: ""
      title: ""
      base: ""
      draft: ""
      next_action: ""
  recently_merged:
    - pr: ""
      merge_commit: ""
      issue_closed: ""
      tracker_updated: ""
  active_tracker: ""
  next_recommended_action: ""
```

## Machine-Readable Role Specification Shape

Each role should eventually have a YAML spec that Codex can read cheaply.

```yaml
role_spec_template:
  id: ""
  name: ""
  mission: ""
  may_edit_code: false
  may_commit: false
  may_merge: false
  must_read:
    - ""
  allowed_outputs:
    - ""
  required_artifact: ""
  required_handoff_fields:
    - ""
  stop_conditions:
    - ""
  forbidden_changes:
    - ""
  next_roles:
    - ""
```

## Parser Drift And Evidence Rule

Issue #11 shows that V2 should promote parser evidence tracking into the global
constitution.

```yaml
parser_evidence_rule:
  volatile_log_derived_fields_should_name:
    - raw evidence source
    - parser-owned output field
    - value source
    - confidence level
    - finality
    - fallback behavior
    - drift flag or detection expectation
    - downstream fields affected
    - degradation behavior when evidence disappears

  uncertainty_policy:
    rule: "Unknown or inferred values must remain explicit."
    forbidden: "Do not convert uncertainty into false certainty for workbook convenience."
```

## Recommendation For Resolving Conflicting Codex Suggestions

When the v2 suggestions disagree, use this triage order:

```yaml
suggestion_triage:
  - preserve V1 sacred safety rules
  - prefer parser truth ownership
  - prefer machine-readable and shorter rules
  - prefer current repo workflow proven by actual successful PRs
  - prefer rules with clear validation
  - prefer modular rules over duplicated prose
  - preserve minority suggestions as open questions when risk is high
```

## Proposed Next Workflow

This v2 constitution work should itself follow the Mythic Edge workflow.

```yaml
workflow_plan:
  A_thinker:
    output: "GitHub issue or problem representation for v2 synthesis"
    status: "needed"

  B_contract_writer:
    output: "docs/contracts/agent_constitution_v2.md"
    status: "recommended"

  C_implementer:
    output:
      - "updated AGENTS.md if needed"
      - "updated docs/agent_constitution.md"
      - "new docs/agent_rules.yml"
      - "optional role YAML specs"
      - "updated templates"
    status: "after contract"

  E_reviewer:
    output: "contract-test report confirming v2 preserves V1 sacred rules"
    status: "required before adoption"

  F_submitter:
    output: "draft PR"
    status: "after clean review"
```

## Open Questions For V2 Synthesis

- Should V2 replace `docs/agent_constitution.md` directly, or should V2 first land as `docs/agent_constitution_v2.md`?
- Should `docs/agent_rules.yml` be required, or should role specs remain Markdown-only for now?
- Should `F2 Integration Deployer` be added immediately, or should it receive its own follow-up issue?
- Should issue lifecycle rules live in the constitution, `docs/codex_module_workflow.md`, or both with one canonical source?
- Should the current v2 draft files remain as source artifacts after the final synthesis PR merges?
