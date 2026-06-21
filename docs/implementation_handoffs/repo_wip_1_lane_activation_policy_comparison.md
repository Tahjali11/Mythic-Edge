# Repo WIP-1 Lane Activation Policy Implementation Handoff

## Role Performed

Codex C: Module Implementer.

## Source Issue

- https://github.com/Tahjali11/Mythic-Edge/issues/543

## Source Artifact

- `docs/contracts/repo_wip_1_lane_activation_policy.md`
- Issue #543 problem representation and Codex H constitutional synthesis
  comment.

## Contract Comparison

Confirmed matches:

- Proposed ADR-0008 was created at the contracted path because no
  `ADR-0008-*` file existed at implementation start.
- ADR-0008 records WIP-1 as a repo coordination policy, not runtime product
  behavior.
- ADR-0008 names the required exceptions, required metadata, clearing
  behavior, tracker-selected queue behavior, active PR behavior, and sibling
  repo adoption boundary.
- `docs/decisions/README.md` now indexes ADR-0008 as `Proposed`.
- `AGENTS.md` has a terse entrypoint warning to verify the repo active lane
  before non-trivial work.
- `docs/agent_constitution.md` now contains the durable workflow gate
  language.
- `docs/codex_module_workflow.md` now has a Start / Intake Gate for active
  lane verification and exception recording.
- `docs/agent_rules.yml` now exposes `lane_activation_policy` vocabulary and a
  `lane_activation` optional handoff schema.
- `docs/templates/problem_representation.md` and
  `docs/templates/workflow_handoff.md` now expose optional lane activation and
  exception metadata.

Contract boundaries preserved:

- No runtime code changed.
- No parser, runtime, workbook, webhook, Apps Script, analytics, AI, CI,
  release, deploy, or production behavior changed.
- No sibling repository was inspected or mutated.
- No GitHub issues, PRs, labels, trackers, automations, worktrees, or stashes
  were mutated.
- Historical issue comments, PR bodies, and old handoffs were not rewritten.

## Files Changed

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/contracts/repo_wip_1_lane_activation_policy.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/repo_wip_1_lane_activation_policy_comparison.md`
- `docs/templates/problem_representation.md`
- `docs/templates/workflow_handoff.md`

## Key Decisions

- Kept WIP-1 as an operating default with named exceptions instead of a hard
  ban on all parallel work.
- Kept exception recording public-safe and repo-authoritative; local worktree
  names, local status indexes, stale prompts, local skills, and chat memory are
  evidence only.
- Added the optional `lane_activation` block to public handoffs without
  invalidating older handoffs.
- Left sibling-repo adoption as future watch-list work only.

## Validation Run

Final validation:

- `python3 tools/check_agent_docs.py` passed with 35 checked files, 0 errors,
  and 0 warnings.
- `git diff --check` passed.
- Path-fed `python3 tools/check_secret_patterns.py --base origin/main
  --paths-from-stdin` passed for 10 changed docs files with 0 forbidden
  findings and 0 warnings.
- Path-fed `python3 tools/check_protected_surfaces.py --base origin/main
  --paths-from-stdin` passed with 0 forbidden findings and 5 expected
  `workflow_authority_docs` warnings.
- Path-fed `python3 tools/check_surface_authorization.py --base origin/main
  --paths-from-stdin --authorization-file
  contract=docs/contracts/repo_wip_1_lane_activation_policy.md` returned
  `authorization_status: ok` and authorized all 5 workflow-authority doc
  warnings.
- Path-fed `python3 tools/select_validation.py --base origin/main
  --paths-from-stdin --format text` returned required checks plus the
  protected-surface authorization recommendation; `selection_status: warning`
  because workflow-authority docs changed, with authorization verified by the
  command above.
- `LC_ALL=C rg -n '[^[:ascii:]]' ...` found no non-ASCII matches in changed
  files.
- Local absolute path marker scan found no matches in changed files.

Pre-handoff structural check:

- `git diff --check` passed.
- `python3 tools/check_agent_docs.py` initially failed because ADR-0008
  referenced this implementation handoff before the handoff file existed.

## Remaining Risks

- Existing open issues and PRs are not inventoried or classified by this
  implementation. That is a follow-up governance task after adoption if the
  user wants it.
- `.github/ISSUE_TEMPLATE/module_workflow.yml` and PR templates remain
  unchanged by contract.
- This package makes ADR-0008 `Proposed`; it should not be treated as accepted
  durable precedent until reviewed and merged through the normal workflow.

## Recommended Next Role

Codex E: Module Reviewer / Contract Tester.

Review focus:

- Confirm ADR-0008 is properly `Proposed` and does not skip ADR numbering.
- Confirm WIP-1 remains a workflow coordination policy only.
- Confirm exceptions are scoped, named, and expiring.
- Confirm templates do not include local absolute paths.
- Confirm no runtime or sibling-repo behavior changed.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #543.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/543

Contract:
docs/contracts/repo_wip_1_lane_activation_policy.md

Implementation handoff:
docs/implementation_handoffs/repo_wip_1_lane_activation_policy_comparison.md

Branch:
main

Goal:
Adversarially review the docs-only WIP-1 repo lane activation governance
package against the contract. Confirm it creates proposed ADR-0008 without
skipping numbering, adds only the contracted governance/template surfaces, and
does not turn local worktrees, stale prompts, local status indexes, skills, or
handoffs into authority over current GitHub and repo governance.

Review:
- docs/contracts/repo_wip_1_lane_activation_policy.md
- docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md
- docs/decisions/README.md
- AGENTS.md
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_rules.yml
- docs/templates/problem_representation.md
- docs/templates/workflow_handoff.md
- docs/implementation_handoffs/repo_wip_1_lane_activation_policy_comparison.md

Check especially:
- ADR-0008 is `Proposed`, linked to issue #543 and the contract, and does not
  claim acceptance before review/merge.
- The WIP-1 default is repo-scoped and does not make local worktrees or local
  status indexes authoritative.
- Named exceptions are present and require scope plus expiration metadata.
- Parked, deferred, tracker-selected, active PR, and clearing-condition
  semantics match the contract.
- Sibling-repo adoption remains future watch-list work only.
- Templates expose optional `lane_activation` metadata without requiring local
  absolute paths.
- No runtime code, parser behavior, workbook/webhook/App Script behavior,
  analytics behavior, AI/model-provider behavior, CI gates, release policy,
  deploy policy, production behavior, sibling repos, historical comments, or
  old handoffs changed.

Validation:
- python3 tools/check_agent_docs.py
- git diff --check
- path-fed secret/private marker scan for changed docs files
- path-fed protected-surface scan for changed docs files
- path-fed validation selector for changed docs files

Do not:
- Edit files while reviewing unless the user explicitly asks for fixer work.
- Stage, commit, push, open a PR, merge, close, relabel, or update trackers.
- Create sibling-repo adoption issues or PRs.
- Treat ADR-0008 as accepted before review and merge.
- Change parser/runtime/workbook/webhook/App Script/analytics/AI/release/
  deploy/production behavior.

End with:
- findings first, ordered by severity;
- validation run;
- residual risks;
- recommendation for next role;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/543"
  tracker: ""
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/repo_wip_1_lane_activation_policy.md"
  target_artifact: "docs/implementation_handoffs/repo_wip_1_lane_activation_policy_comparison.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  internal_project_area: "Quality / Governance"
  bridge_code_status: "not_bridge_code"
  lane_activation:
    repo: "Tahjali11/Mythic-Edge"
    active_issue_or_lane: "https://github.com/Tahjali11/Mythic-Edge/issues/543"
    lane_status: "active"
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
    - "python3 tools/check_agent_docs.py passed with 35 checked files, 0 errors, and 0 warnings."
    - "git diff --check passed."
    - "Path-fed secret/private marker scan passed for 10 changed docs files with 0 forbidden findings and 0 warnings."
    - "Path-fed protected-surface scan passed with 0 forbidden findings and 5 expected workflow_authority_docs warnings."
    - "Path-fed protected-surface authorization check returned authorization_status: ok."
    - "Path-fed validation selector returned selection_status: warning because workflow-authority docs changed; required checks were run and authorization was verified."
    - "ASCII scan found no non-ASCII matches in changed files."
    - "Local absolute path marker scan found no matches in changed files."
  stop_conditions:
    - "Do not skip ADR-0008 unless the user explicitly reserves or redirects ADR numbering."
    - "Do not create sibling-repo adoption issues or PRs."
    - "Do not edit runtime code or parser/runtime/workbook/webhook/App Script/analytics/AI behavior."
    - "Do not make local worktrees, stale prompts, local status indexes, skills, or handoffs authoritative over GitHub issue/PR/repo governance."
    - "Do not close, relabel, stage, commit, push, open PRs, merge, mutate worktrees, mutate stashes, or alter automations."
```
