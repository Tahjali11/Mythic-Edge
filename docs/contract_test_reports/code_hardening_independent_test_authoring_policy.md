# Contract Test Report: Code Hardening Independent Test-Authoring Policy

## Findings First

No blocking findings.

Non-blocking residual risks:

1. The policy remains intentionally unimplemented. The comparison correctly
   identifies that active workflow docs do not yet enforce independent
   pre-implementation evidence before Codex C begins triggered high-risk work
   (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:261`).
2. E2 exists only at tracker, issue, and contract level until a future
   authorized implementation updates durable workflow docs
   (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:215`,
   `docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:223`).
3. The PR template and implementation handoff template do not yet require a
   high-risk PR to cite independent evidence, but this is accurately classified
   as future implementation scope, not a defect in this comparison pass
   (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:273`,
   `docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:277`).

## Issue

- Role performed: Codex E: Module Reviewer / contract-test thread
- Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/72
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33
- Branch target: `codex/code-hardening-suite`

## Contract

- `docs/contracts/code_hardening_independent_test_authoring_policy.md`
- Supporting governance:
  - `AGENTS.md`
  - `docs/agent_constitution.md`
  - `docs/agent_rules.yml`
  - `docs/codex_module_workflow.md`
  - `docs/agent_threads/contract_test.md`
  - `docs/agent_threads/review.md`
  - `docs/templates/contract_test_report.md`

## Implementation Under Test

- `docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md`

This was a docs-only Codex C comparison artifact. No policy implementation,
workflow doc edit, template edit, test change, CI gate, parser behavior change,
schema change, fixture change, snapshot refresh, baseline refresh, protected
artifact change, branch targeting, PR creation, or tracker closure was under
review.

## Contract Summary

The contract defines independent test identification and optional independent
test authoring for high-risk Mythic Edge workflow changes. Its central rule is
that triggered high-risk work must have an independent evidence artifact before
Codex C starts implementation. E2 is defined as an optional Codex E mode, not a
new permanent role. The policy remains workflow governance and must not change
parser behavior, protected surfaces, schemas, fixtures, snapshots, baselines,
deployment behavior, or truth ownership.

## Artifacts Reviewed

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`
- `docs/templates/contract_test_report.md`
- `docs/contracts/code_hardening_independent_test_authoring_policy.md`
- `docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md`
- `.github/pull_request_template.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- Current hardening contracts under `docs/contracts/`
- GitHub issue #72 and tracker #33

## Confirmed Contract Matches

- The comparison correctly states the policy goal: prevent high-risk
  implementation work from selecting tests only after a patch exists
  (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:44`).
- The comparison correctly preserves the existing A/B/C/D/E/F/G workflow and
  treats E2 as an optional Codex E mode rather than a new permanent role
  (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:55`,
  `docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:56`).
- The comparison accurately identifies existing governance support for
  high-risk gates in AGENTS, the constitution, agent rules, workflow docs, and
  implementation rules
  (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:69`).
- The comparison correctly distinguishes current support from the missing
  pre-implementation independent-evidence gate
  (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:85`).
- The comparison correctly says Codex B contract test inventories can satisfy
  independent test identification for some medium/high-risk work when concrete
  enough
  (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:181`).
- The comparison accurately identifies the PR template gap for high-risk
  independent evidence without over-claiming a current rule
  (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:173`).
- The comparison preserves parser truth ownership and does not treat tests,
  snapshots, or ADRs as automatic authorization for semantic or protected
  surface changes
  (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:197`).
- The comparison stayed inside the contract boundary and made no implementation
  or protected-surface changes
  (`docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md:288`).

## Contract Mismatches

None found.

## Missing Safeguards Or Tests

No missing executable tests are expected for this review because issue #72 and
the contract authorize a planning/comparison pass only.

The comparison correctly identifies missing future governance safeguards:

- no formal active-doc gate for pre-implementation independent evidence
- no durable E2 description in `docs/agent_threads/contract_test.md`
- no `docs/agent_rules.yml` encoding for E2 or independent test identification
- no durable high-risk `A -> B -> E/E2 -> C -> E -> F -> G` route in
  `docs/codex_module_workflow.md`
- no PR template or implementation handoff field requiring high-risk
  independent evidence citation
- no pre-implementation E2 checklist shape in the contract-test report template
- older hardening contracts do not classify E2 as mandatory, optional, or not
  needed

These are non-blocking for this comparison artifact because implementing them
is explicitly out of scope for this issue.

## Protected-Surface Confirmation

No forbidden scope was touched by the reviewed comparison. The reviewed artifact
does not change parser behavior, parser state final reconciliation, workbook
schema, webhook payload shape, Apps Script behavior, parser event classes, event
kind values, parser payload shapes, match/game identity, deduplication, tests,
CI gates, fixtures, expected outputs, schema snapshots, drift baselines,
secrets, environment variables, raw logs, generated data, runtime status files,
failed posts, workbook exports, local-only artifacts, production deployment
behavior, or merge-to-main policy.

## Drift Notes

- Repo drift: none found in the reviewed docs-only scope.
- Workbook drift: not applicable; no workbook behavior or workbook exports were
  reviewed or changed.
- Deployment drift: not applicable; no Apps Script, deployment, or external
  connection behavior was reviewed or changed.
- Local-data drift: none found in the reviewed scope.

## Files Changed By This Review

- `docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md`

## Validation

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
@('docs/contracts/code_hardening_independent_test_authoring_policy.md','docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md','docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md') | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
if (Test-Path tools\check_agent_docs.py) { py tools\check_agent_docs.py } else { Write-Output 'tools\check_agent_docs.py not present on this branch' }
rg -n "[ \t]+$" docs\contracts\code_hardening_independent_test_authoring_policy.md docs\implementation_handoffs\code_hardening_independent_test_authoring_policy_comparison.md docs\contract_test_reports\code_hardening_independent_test_authoring_policy.md
```

Results:

- `git diff --check` passed with no output.
- `py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite` passed with `changed_paths: 0`, `forbidden: 0`, `warnings: 0`.
- Path-scoped protected-surface check for the three intended issue #72 docs passed with `changed_paths: 3`, `forbidden: 0`, `warnings: 0`.
- `tools\check_agent_docs.py` is not present on this branch, so the suggested agent-doc validation was recorded as unavailable rather than treated as a policy failure.
- Trailing-whitespace scan found no matches. The `rg` command exited `1`, which is expected for no matches.

## Remaining Risks

- The project still needs a future authorized implementation thread if the user
  wants the independent test-authoring policy enforced in durable governance
  docs and handoff templates.
- Existing high-risk work can still rely on contract-level test inventories
  unless a future issue/contract explicitly requires E2.
- `py tools\check_agent_docs.py` is not present on this branch at report
  creation time, so that suggested validation can only be recorded as
  unavailable unless the tool is added by a separately authorized issue.

## Recommendation

Approve this comparison for Module Submitter.

Next recommended role: Codex F: Module Submitter.

## Pasteable Next-Thread Prompt

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex F: Module Submitter for the Code Hardening child issue: Independent test-authoring policy for high-risk changes.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/72

Branch target:
codex/code-hardening-suite

Submit only the reviewed docs-only issue #72 package:
- docs/contracts/code_hardening_independent_test_authoring_policy.md
- docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md
- docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md

Before staging:
- inspect git status
- confirm no unrelated files are staged or included
- do not stage docs/python_tooling_inventory.md or any unrelated local files

Run or preserve validation evidence:
- git diff --check
- py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
- 'docs/contracts/code_hardening_independent_test_authoring_policy.md','docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md','docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
- py tools\check_agent_docs.py if present; if unavailable on this branch, record that as a validation limitation, not a policy failure

Commit, push, and open a draft PR to codex/code-hardening-suite. Do not target main. Do not merge. Do not mark tracker #33 complete.

Final handoff must include current branch, commit hash, PR URL, target branch, files staged, validation result, remaining risk, and next recommended role.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/72"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md"
  target_artifact: "docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check -> passed with no output"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed with changed_paths: 0, forbidden: 0, warnings: 0"
    - "issue #72 path-scoped protected-surface check -> passed with changed_paths: 3, forbidden: 0, warnings: 0"
    - "py tools\\check_agent_docs.py -> unavailable on this branch; recorded as validation limitation"
    - "trailing-whitespace scan on issue #72 docs -> no matches"
  stop_conditions:
    - "Do not implement the policy in this submitter pass."
    - "Do not edit workflow docs, agent rules, templates, PR templates, tests, CI gates, parser behavior, schemas, fixtures, snapshots, baselines, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts."
    - "Do not make E2 a new permanent role."
    - "Do not stage unrelated files outside the reviewed issue #72 docs-only package."
    - "Do not target main."
    - "Do not mark tracker #33 complete."
```
