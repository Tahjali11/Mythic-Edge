# Agent Constitution V2 Synthesis Contract

Problem representation:
`docs/problem_representations/agent_constitution_v2_synthesis.md`

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/1

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Branch target: `codex/parser-module-audit-suite`

This contract defines the documentation architecture and acceptance rules for
synthesizing role-labeled Codex v2 constitution drafts into the next
authoritative Mythic Edge constitution package. It is a contract artifact only.
It does not adopt V2, replace `docs/agent_constitution.md`, modify
`AGENTS.md`, or implement the final documentation package.

## Module

Agent constitution V2 synthesis.

The module is the repository coordination and agent workflow documentation
package that governs how Codex threads choose roles, route work, preserve truth
ownership, validate changes, submit PRs, merge reviewed work, close issues, and
update trackers.

## Owning Layer

Repository coordination and agent workflow.

This contract governs documentation and workflow rules only. It must not change
parser behavior, workbook schema, webhook payload shape, Apps Script behavior,
match/game identity, deduplication, final reconciliation, secrets, raw logs,
generated data, runtime status files, failed posts, or workbook exports.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/agent_constitution_v2_synthesis.md`

Final V2 adoption work may update or create only the documentation artifacts
listed in this contract's target architecture, plus archive/move operations for
role-labeled drafts. This contract does not itself authorize parser/runtime
behavior changes.

## Target Documentation Architecture

The accepted target architecture is Markdown plus a required machine-readable
rule index.

Required first-adoption package:

- `AGENTS.md`
  - short entrypoint for agents
  - may be updated by the implementation thread only if the contract is
    satisfied and the update remains terse
  - should point to active constitution, role docs, and `docs/agent_rules.yml`
- `docs/agent_constitution.md`
  - human-readable authoritative constitution
  - should remain understandable to the user and beginner-friendly for
    explaining workflow concepts
  - should not become a giant duplicated mirror of every role doc
- `docs/agent_rules.yml`
  - required in V2
  - terse, Codex-optimized machine-readable rule index
  - should encode routing, safety, lifecycle, role, validation, source
    priority, and stop-condition rules
- `docs/agent_threads/*.md`
  - human-readable role docs
  - should be updated only where V2 changes role boundaries, handoff fields, or
    lifecycle obligations
- `docs/templates/*.md`
  - human-usable artifact templates
  - should be updated where V2 changes handoff, prompt, lifecycle, or status
    shapes
- `.github/pull_request_template.md`
  - PR body shape
  - should align with V2 PR lifecycle and required links
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
  - issue intake shape
  - should align with V2 source, risk, lifecycle, and tracker rules

Allowed but not required in first-adoption package:

- `docs/agent_threads/*.yml`
  - per-role YAML specs
  - V2 must define the schema for these files
  - V2 must not require every per-role YAML file in the first adoption PR
- explanatory companion docs
  - longer user-facing rationale may exist outside the terse rule package if
    the implementation thread finds a clear need

Required post-adoption cleanup:

- Role-labeled v2 draft files must be archived after adoption rather than left
  beside active rule files.
- Archive target should be explicit and stable, for example
  `docs/archive/agent_constitution_v2_drafts/`.
- The adoption PR must not delete draft history unless the user explicitly asks
  for deletion.

## Source Artifact Priority

The synthesis implementation must treat sources in this order:

1. active system and developer instructions
2. explicit user instructions and accepted decisions in the current task
3. `docs/problem_representations/agent_constitution_v2_synthesis.md`
4. `AGENTS.md`
5. `docs/agent_constitution.md`
6. `docs/codex_module_workflow.md`
7. `docs/agent_threads/*.md`
8. `docs/templates/*.md`
9. `.github/pull_request_template.md`
10. `.github/ISSUE_TEMPLATE/module_workflow.yml`
11. role-labeled Codex V2 draft files listed below
12. older docs, examples, and prior chat memory

Accepted decisions in the user prompt are contract requirements even when a
draft suggests a different path.

Role-labeled V2 draft sources:

- `docs/agent_constitution_v2_codex_a_thinker_draft.md`
- `docs/agent_constitution_v2_codex_f.md`
- `docs/v2_constitution_codex_a.md`
- `docs/v2_constitution_codex_b.md`
- `docs/v2_constitution_codex_c.md`
- `docs/v2_constitution_codex_d.md`
- `docs/v2_constitution_codex_e.md`

Generic V2 drafts without a Codex role marker in the filename are not source
artifacts for the final synthesis. They may be moved to the same archive folder
if the implementation thread determines they are obsolete, but they must not be
used as primary authority.

## Sacred V1 Rules That Must Be Preserved

V2 must not weaken these V1 rules:

- Parser and state interpretation own event interpretation and normalized
  match/game facts.
- Parser-owned truth must not move into workbook formulas, dashboard logic,
  Apps Script transport, webhook transport, or AI-generated interpretation.
- Secrets, webhook URLs, API keys, tokens, credentials, local MTGA logs, failed
  posts, runtime status files, generated card data, and raw workbook exports
  must never be committed.
- Webhook payload shape, workbook schema, deployed Apps Script assumptions,
  match identity, game identity, deduplication, winner fields, play/draw
  fields, mulligan counts, and final reconciliation are high-risk surfaces.
- High-risk work requires a problem representation, module contract,
  implementation against the contract, review or contract-test verification,
  and validation evidence.
- Agents must not delete archive, raw, debug, helper, summary, observability,
  or generated-data layers without explicit user approval and a rollback path.
- Agents must not claim validation passed without command output, test
  evidence, corrected output, CI evidence, or a verified code path.
- Agents must stop or reroute when a problem representation and module contract
  materially conflict.
- Agents must not silently expand scope beyond the stated problem.
- Module submitter work must not stage unrelated files or local-only artifacts.
- Module PR work must not target `main` unless explicitly approved.

V2 may make these rules shorter or more machine-readable, but it must not make
them weaker.

## Machine-Readable Rule Structure

V2 must introduce `docs/agent_rules.yml`.

The YAML file should be a terse index, not a full duplicate of the human
constitution. It should prefer stable IDs and compact arrays over prose.

Required top-level structure:

```yaml
version: 2
status: active
authority_order:
  - system_and_developer
  - current_user_instruction
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - current_issue_or_problem_representation
  - current_contract
  - current_handoff_or_report
  - docs/agent_threads
  - docs/templates
  - older_docs_examples_memory
source_priority:
  # compact source order for synthesis/routing decisions
sacred_rules:
  # V1 non-negotiables, by stable id
protected_surfaces:
  parser_downstream_surfaces:
    - workbook_schema
    - webhook_payload_shape
    - apps_script_behavior
    - parser_event_classes
    - parser_state_final_reconciliation
    - extractor_behavior
    - match_identity
    - game_identity
    - deduplication
    - secrets
    - environment_variables
    - raw_logs
    - generated_data
    - runtime_status_files
    - failed_posts
    - workbook_exports
  local_artifact_surfaces:
    - local_logs
    - failed_post_queues
    - generated_card_data
    - raw_workbook_exports
roles:
  A: {}
  B: {}
  C: {}
  D: {}
  E: {}
  F: {}
  G: {}
routing:
  normal_path:
    - A
    - B
    - C
    - E
    - F
    - G
  loopbacks: {}
risk_tiers: {}
issue_lifecycle: {}
pr_lifecycle: {}
tracker_hygiene: {}
branch_policy: {}
validation_gates: {}
prompt_schema: {}
handoff_schema: {}
current_status_schema: {}
archive_policy: {}
```

Required YAML behavior:

- It must include stable role IDs A through G.
- It must encode the accepted Codex G role as the integration deployer.
- It must encode that `docs/agent_constitution.md` remains human-readable.
- It must encode that `docs/agent_rules.yml` is Codex-optimized and terse.
- It must encode that per-role YAML specs are optional in the first adoption
  PR.
- It must include protected-surface bundles so prompts can reference a bundle
  instead of repeating long forbidden lists.
- It must include issue, PR, tracker, validation, and branch gates.
- It must include a current-status summary schema.
- It must not contradict `docs/agent_constitution.md`.

### Optional Per-Role YAML Schema

V2 must define this schema for future per-role YAML files, but the first
adoption PR does not need to create all of them:

```yaml
id: ""
name: ""
mission: ""
may_edit_code: false
may_commit: false
may_merge: false
must_read:
  - ""
may_change:
  - ""
must_not_change:
  - ""
required_output:
  - ""
required_artifact: ""
required_handoff_fields:
  - ""
validation_expectations:
  - ""
stop_conditions:
  - ""
next_roles:
  - ""
```

## Role Model

V2 role IDs are A through G.

| ID | Role | Owns | Must Not |
| --- | --- | --- | --- |
| A | Thinker | problem framing, scope, risk, first inspection order, issue/problem representation | implement code |
| B | Module Contract Writer | module/workflow contract, public interfaces, truth boundaries, invariants, tests, acceptance criteria | implement behavior changes |
| C | Module Implementer | smallest coherent code/test/doc implementation against an approved contract; comparison handoff | silently expand scope or bypass contract |
| D | Module Fixer | concrete review, contract-test, CI, or user finding fixes | reopen broad design without routing back |
| E | Module Reviewer / Contract Tester | contract-test or PR review, findings, verdicts, routing | silently fix code when asked to review |
| F | Module Submitter | stage intended files, commit, push, open or update draft PR | merge PRs or target production without approval |
| G | Integration Deployer | mark approved PR ready when appropriate, merge/close/update tracker after all gates pass | bypass CI/review/scope gates or merge to `main` without explicit approval |

V2 must use `Codex G: Integration Deployer` for merge, issue closure, and
tracker-update responsibilities. Prior draft language that called this role
`F2` should be normalized to `G`.

Normal path:

```text
A Thinker -> B Module Contract Writer -> C Module Implementer -> E Module Reviewer -> F Module Submitter -> G Integration Deployer
```

D remains a loopback role used only for concrete fix targets.

## Issue Lifecycle Rules

V2 must define issue closure rules.

Required rules:

- V2 synthesis should get its own issue linked to issue #1.
- Issue #1 may later close as completed V1 once the V2 path is established.
- Tracker issues remain open until the entire tracked queue or phase is
  complete.
- A tracker must not close just because one child issue or module finishes.
- Module audit issues may close only after required artifacts exist, review is
  clean or accepted, PR work is merged into the approved base, validation/CI is
  recorded, and the tracker is updated if applicable.
- Bug issues may close after the fix PR is merged, validation is recorded, and
  no follow-up implementation is implied.
- Planning/docs issues may close when their requested planning/docs artifacts
  are complete and no implementation remains; otherwise open/link a follow-up
  implementation issue.
- Constitution issues may close when rule changes are merged, affected role
  docs/templates are updated if needed, validation is recorded, and a decision
  note says no amendment work remains.

Required completion comment fields:

- PR number
- merge commit
- base branch
- durable artifacts produced
- validation or CI result
- tracker status or next queue item when applicable

## PR Lifecycle Rules

V2 must define PR readiness and merge rules.

Required rules:

- PRs default to draft unless the user explicitly asks otherwise.
- Module audit PRs target the non-production integration branch first.
- `main` may not be targeted unless explicitly approved.
- PR bodies must use or align with `.github/pull_request_template.md`.
- PR bodies must link relevant issue, tracker, contract, implementation
  handoff, review/contract-test report, and constitution/role docs when
  applicable.
- Use `Closes #...` only when the PR fully satisfies the issue.
- Use `Refs #...` for partial, planning-only, contract-only, tracker, or
  follow-up work.
- F may submit a PR only after review has no blocking findings and validation
  is present or explicitly explained.
- G may merge only after the user asks for deployer/merge work and all merge
  gates pass.

Required merge gates:

- PR is not draft.
- PR base branch is approved.
- PR target is not `main` unless explicitly approved.
- CI/checks pass or the user explicitly waives named failures.
- Review has no blocking findings.
- Diff remains within reviewed scope.
- No forbidden files, secrets, local artifacts, generated data, raw logs,
  runtime status files, failed posts, or workbook exports are included.
- Issue closing behavior is correct.
- Tracker update behavior is correct.

After merge, G must:

- confirm merge method and merge commit
- confirm source branch deletion or preservation
- sync the local integration branch when working locally
- close fully satisfied issues with completion comments
- update trackers
- name the next workflow step

## Tracker Hygiene Rules

V2 must define tracker update rules.

Tracker update is required when:

- a child module/constitution issue is created
- a child PR is opened
- a child PR is merged
- a child issue is closed
- a child issue is blocked
- the next queue item changes

Tracker update fields:

- issue number and title
- PR number and base branch
- merge commit if merged
- durable artifacts produced
- validation or CI status
- blocker or residual risk
- next queue item
- related open issues

Trackers should summarize progress without becoming the source of parser truth.

## Current-Status Summary Expectations

V2 must define a compact status summary format for status questions and
handoffs.

Required machine-readable shape:

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
      checks: ""
      next_action: ""
  recently_merged:
    - pr: ""
      merge_commit: ""
      issue_closed: ""
      tracker_updated: ""
  active_tracker: ""
  next_recommended_action: ""
```

When the user asks about current GitHub state, status should be verified with
`gh` or GitHub before answering unless the user explicitly asks for conceptual
guidance only.

## Conflict Triage Rules

Contradictory Codex suggestions must be resolved in this order:

1. preserve active system/developer/user instructions
2. preserve accepted decisions in this contract
3. preserve V1 sacred safety rules
4. preserve parser truth ownership
5. prefer the rule that prevents irreversible or high-risk drift
6. prefer current repo workflow proven by successful issues/PRs
7. prefer shorter, machine-readable rules when they are equally safe
8. prefer one canonical source plus links over duplicated prose
9. preserve minority/high-risk concerns as open questions rather than silently
   dropping them

Examples:

- Drafts that call the deployer role `F2` conflict with the accepted decision;
  V2 must use Codex G.
- Drafts that make every per-role YAML file mandatory conflict with the
  accepted decision; V2 must define the schema but not require every file in the
  first adoption PR.
- Drafts that leave role-labeled V2 files beside active rule files conflict
  with the accepted decision; V2 must archive them after adoption.

## Outputs

The Module Implementer should produce the final documentation package described
by this contract. Expected outputs are:

- updated `docs/agent_constitution.md`
- new `docs/agent_rules.yml`
- updated `AGENTS.md` only if needed to point to active V2/YAML rules
- updated `docs/codex_module_workflow.md` if needed for role G/lifecycle
  alignment
- updated `docs/agent_threads/*.md` where role/lifecycle changes require it
- updated `docs/templates/*.md` where handoff/status/prompt schema changes
  require it
- updated `.github/pull_request_template.md` if PR lifecycle requirements are
  not already represented
- updated `.github/ISSUE_TEMPLATE/module_workflow.yml` if issue lifecycle or
  source fields require it
- archived role-labeled V2 draft files after V2 adoption
- implementation handoff under
  `docs/implementation_handoffs/agent_constitution_v2_synthesis.md`

The implementation thread may propose smaller changes if it finds an
acceptance-risk reason, but it must not silently omit `docs/agent_rules.yml`,
Codex G, or draft archival policy.

## Invariants

- V2 must preserve every sacred V1 safety rule.
- `docs/agent_constitution.md` remains the human-readable constitution.
- `docs/agent_rules.yml` becomes the required Codex-optimized rule index.
- Per-role YAML schema is defined, but every per-role YAML file is not required
  in the first adoption PR.
- Codex G exists as the integration deployer role.
- Role-labeled draft files are source artifacts before adoption and archived
  artifacts after adoption.
- V2 synthesis receives its own issue linked to issue #1.
- Issue #1 can later close as completed V1 once the V2 path is established.
- The documentation package must not create parser/runtime/workbook behavior
  changes.

## Error Behavior

If source artifacts conflict:

- apply the conflict triage rules
- preserve the disagreement as an open risk when it affects safety or workflow
  authority
- route back to Module Contract Writer if implementation cannot resolve the
  conflict without changing this contract

If final documentation and `docs/agent_rules.yml` disagree:

- treat the implementation as not ready for reviewer approval
- route to Module Fixer or Module Contract Writer depending on whether the
  mismatch is implementation drift or contract ambiguity

If `docs/agent_rules.yml` becomes too verbose:

- keep only stable operational indexes in YAML
- move explanatory prose to Markdown

If Markdown becomes too terse for users:

- keep user-facing explanations in `docs/agent_constitution.md`
- keep YAML optimized for Codex

## Side Effects

Allowed side effects for implementation:

- documentation file edits
- creation of `docs/agent_rules.yml`
- possible creation of an archive directory for role-labeled V2 drafts
- moving role-labeled V2 draft files to the archive after adoption

Forbidden side effects:

- parser behavior changes
- workbook schema changes
- webhook payload shape changes
- Apps Script behavior changes
- match/game identity changes
- deduplication changes
- final reconciliation changes
- secrets/environment variable changes
- raw log changes
- generated data changes
- runtime status file changes
- failed-post changes
- workbook export changes
- merge to `main` without explicit approval

## Dependency Order

Implementation should proceed in this order:

1. Confirm or create the V2 synthesis GitHub issue linked to #1.
2. Read this contract and all source artifacts.
3. Draft `docs/agent_rules.yml` first as the machine-readable spine.
4. Update `docs/agent_constitution.md` to match the YAML spine while remaining
   human-readable.
5. Update `AGENTS.md` only as a terse entrypoint if needed.
6. Update role docs for A through G.
7. Update workflow docs/templates/PR/issue templates to match lifecycle rules.
8. Archive role-labeled V2 draft files after the active package is ready.
9. Write the implementation handoff.
10. Run documentation and repo validation.
11. Route to Module Reviewer in contract-test mode.

If step 1 cannot be completed locally, the implementation handoff must say what
GitHub issue should be created and must not pretend the issue exists.

## Compatibility

V2 must remain compatible with existing workflow artifacts:

- existing problem representations
- existing contracts under `docs/contracts/`
- existing implementation handoffs
- existing contract-test reports
- existing PR template fields
- existing issue template fields
- existing `workflow_handoff` blocks

V2 may add fields to handoff/status schemas, but it must not make older
artifacts unreadable or invalid for practical continuation.

## Tests Required

Documentation validation:

```bash
git diff --check
```

Repo validation, because constitution changes affect workflow but should not
change runtime behavior:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
```

Manual/inspection validation:

- Verify `docs/agent_rules.yml` parses as YAML.
- Verify `docs/agent_rules.yml` and `docs/agent_constitution.md` do not
  contradict each other.
- Verify all role IDs A through G are present in Markdown and YAML.
- Verify Codex G owns merge/close/tracker-update duties.
- Verify F does not merge.
- Verify V1 non-negotiables are preserved.
- Verify source priority and conflict triage are explicit.
- Verify issue, PR, tracker, and current-status schemas are present.
- Verify role-labeled V2 drafts are archived after adoption, not left beside
  active rule files.
- Verify no parser/runtime/workbook/App Script files changed.

## Acceptance Criteria

- `docs/contracts/agent_constitution_v2_synthesis.md` exists and defines this
  contract.
- The final V2 implementation creates `docs/agent_rules.yml`.
- The final V2 implementation keeps `docs/agent_constitution.md`
  human-readable.
- The final V2 implementation defines but does not require every per-role YAML
  spec in the first adoption PR.
- Codex A, B, C, D, E, F, and G are all defined.
- Codex G is the integration deployer and owns merge/close/tracker-update work.
- Source artifact priority is explicit.
- V1 sacred rules are preserved.
- Issue lifecycle, PR lifecycle, tracker hygiene, current-status summary, and
  conflict triage rules are explicit.
- Old role-labeled V2 draft files have an archive plan and are archived by the
  adoption implementation.
- Validation evidence is recorded.
- No out-of-scope parser/runtime/workbook/App Script behavior changes are made.

## Open Contract Risks

- `docs/agent_rules.yml` and `docs/agent_constitution.md` may drift if the same
  rule is duplicated too fully in both places.
- Adding Codex G may require a new role doc; if that doc is added in the first
  adoption PR, templates and workflow docs must also be updated.
- GitHub issue creation and tracker updates may require network/authenticated
  `gh` access that is unavailable in some Codex contexts.
- Archiving draft files may produce a large docs diff if many unrelated generic
  drafts are present; only role-labeled source drafts are required by this
  contract.
- There may be current untracked draft files from other role experiments; the
  implementation thread must separate source drafts from unrelated drafts.

## Next Workflow Action

Next role: Module Implementer (Codex C)

Review should come after implementation because this contract is complete
enough to produce the documentation package, and the accepted decisions already
resolve the major open questions.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for the Constitution V2 synthesis contract.

Goal:
Implement the final documentation package described by docs/contracts/agent_constitution_v2_synthesis.md without changing parser/runtime/workbook behavior.

Use:
- docs/problem_representations/agent_constitution_v2_synthesis.md
- docs/contracts/agent_constitution_v2_synthesis.md
- docs/agent_constitution.md
- AGENTS.md
- docs/codex_module_workflow.md
- docs/agent_threads/*.md
- docs/templates/*.md
- .github/pull_request_template.md
- .github/ISSUE_TEMPLATE/module_workflow.yml
- docs/agent_constitution_v2_codex_a_thinker_draft.md
- docs/agent_constitution_v2_codex_f.md
- docs/v2_constitution_codex_a.md
- docs/v2_constitution_codex_b.md
- docs/v2_constitution_codex_c.md
- docs/v2_constitution_codex_d.md
- docs/v2_constitution_codex_e.md

Required decisions:
- Create docs/agent_rules.yml as a terse machine-readable rule index.
- Keep docs/agent_constitution.md human-readable.
- Define the per-role YAML schema, but do not require every per-role YAML file in the first adoption PR.
- Add Codex G: Integration Deployer as the merge/close/tracker-update role.
- Archive role-labeled V2 draft files after V2 adoption.
- Ensure V2 synthesis has its own issue linked to #1, or document the exact issue-creation blocker.

Produce:
- the V2 documentation package required by the contract
- docs/implementation_handoffs/agent_constitution_v2_synthesis.md

Do not:
- change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports
- target main unless explicitly approved
- stage or commit unless explicitly asked
```

```yaml
workflow_handoff:
  issue: "docs/problem_representations/agent_constitution_v2_synthesis.md"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/1"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/agent_constitution_v2_synthesis.md"
  target_artifact: "docs/implementation_handoffs/agent_constitution_v2_synthesis.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not adopt V2 without satisfying docs/contracts/agent_constitution_v2_synthesis.md."
    - "Do not omit docs/agent_rules.yml from the V2 adoption package."
    - "Do not replace V1 sacred rules with weaker V2 wording."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main unless explicitly approved."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Contract produced: `docs/contracts/agent_constitution_v2_synthesis.md`

Key decisions:

- V2 must include `docs/agent_rules.yml`.
- `docs/agent_constitution.md` remains the human-readable constitution.
- Per-role YAML schema is required, but every per-role YAML file is not
  required in the first adoption PR.
- Codex G exists and owns integration deployment, issue closure, and tracker
  update gates.
- Role-labeled drafts are source artifacts before adoption and archived after
  adoption.
- V2 synthesis should receive its own issue linked to #1; issue #1 can later
  close as completed V1 once the V2 path is established.

Unresolved contract risks:

- YAML/Markdown rule drift.
- GitHub issue/tracker operations may need authenticated `gh` access.
- Codex G role docs/templates may need careful updates to avoid overlap with
  Module Submitter.
- Existing untracked draft files must be separated from contract-required
  role-labeled drafts.

Recommended next role: Codex C, Module Implementer.
