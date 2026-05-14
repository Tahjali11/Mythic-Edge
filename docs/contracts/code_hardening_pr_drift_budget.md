# Code Hardening PR Drift Budget Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/39

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`
- `.github/pull_request_template.md`

Issue #39 also names `docs/agent_rules.yml` as a rule source. On the current
`codex/code-hardening-suite` branch inspected for this contract, that file is
not present. This contract therefore treats `docs/agent_constitution.md`,
tracker #33, issue #39, the protected-surface gate contract, and this contract
as the available policy sources. Adding or syncing `docs/agent_rules.yml`
remains a separate explicitly authorized workflow change.

Related hardening context:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `tools/check_protected_surfaces.py`
- `.github/workflows/repo-checks.yml`

Branch target: `codex/code-hardening-suite`

This contract defines the pull request template drift-budget section for the
Code Hardening suite. It is a contract artifact only. It does not edit the PR
template, implement code, or change parser/runtime/workbook/App Script
behavior.

## Module

PR drift budget section.

Implementation artifact:

- `.github/pull_request_template.md`

Likely implementation handoff:

- `docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md`

Likely review artifact:

- `docs/contract_test_reports/code_hardening_pr_drift_budget.md`

Plain English: every PR should carry a small semantic drift budget that names
what changed, what did not change, whether protected surfaces moved, and what
residual risk remains. The template should expose drift for reviewers; it must
not authorize protected changes by itself.

## Owning Layer

Repository coordination and PR lifecycle.

Truth boundary:

- Parser and state interpretation remain the source of parser truth.
- Module issues and contracts authorize behavior, schema, event-shape, fixture,
  and protected-surface changes.
- The PR template records the author's drift disclosure; it does not create
  authority to change parser truth, workbook schema, webhook payloads, Apps
  Script behavior, match/game identity, deduplication, runtime status files, or
  local/generated artifacts.
- The protected-surface diff gate flags path-level risk. The drift budget
  records semantic risk and authorization.
- Codex E reviewers verify the drift budget against the contract and diff.
- Codex F submitters fill the drift budget before opening or updating a PR.
- Codex G deployers treat missing, vague, or contradictory drift budgets as a
  merge-readiness risk.

## Files Owned By This Contract

- `docs/contracts/code_hardening_pr_drift_budget.md`

Expected future implementation file owned by this contract:

- `.github/pull_request_template.md`

Expected future handoff/report files:

- `docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md`
- `docs/contract_test_reports/code_hardening_pr_drift_budget.md`

Related files whose behavior is referenced but not owned by this contract:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`, when present on the target branch
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `.github/workflows/repo-checks.yml`
- `tools/check_protected_surfaces.py`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `tools/google_apps_script/Code.gs`
- parser/runtime/workbook source files that may be named by drift disclosures

## Public Interface

The stable public interface is a new Markdown section in
`.github/pull_request_template.md`:

```markdown
## Drift Budget

Use `No drift`, `Authorized drift`, `Residual drift`, or `N/A`. For any `Authorized drift` or `Residual drift`, cite the issue and contract that allow it.

- Runtime/parser behavior:
- Parser event shape/classes:
- Workbook/webhook/App Script shape:
- Parser truth ownership:
- Fixtures/evidence:
- Protected-surface authorization:
- Residual drift / accepted gaps:
- Follow-up required:
```

The wording above is the required content. Codex C may make tiny formatting
adjustments to fit the surrounding template, but it must preserve every field,
the four allowed response labels, and the authorization sentence.

## Placement

Required placement:

- Insert the section after `## Layer Ownership`.
- Insert it before `## Changes`.

Rationale:

- Authors should name the truth-producing layer first.
- The drift budget should then classify semantic drift before the freeform
  change summary.
- Keeping it before `## Changes` makes the budget visible early without
  replacing the existing tests, contract verification, protected-surface, or
  workflow handoff sections.

## Inputs

### Pull Request Diff

Type: changed files and semantic change summary.

Sources:

- local branch diff
- implementation handoff
- module contract
- focused test evidence
- protected-surface gate output

The drift budget must be filled from the actual diff and artifacts, not from
intent alone.

### Issue And Contract Authorization

Type: links or file paths.

Required for:

- `Authorized drift`
- `Residual drift`
- any protected surface touched by the PR
- any behavior/schema/event-shape/fixture/truth ownership change

Valid authorization examples:

- `Authorized drift - issue #39 and docs/contracts/code_hardening_pr_drift_budget.md authorize PR-template workflow wording only.`
- `Authorized drift - issue #24 and docs/contracts/parser_gre_game_result.md authorize GameResult winner precedence tests.`
- `Residual drift - issue #34 contract-test report records known unrelated runner path-display failure; follow-up remains outside this PR.`

Invalid authorization examples:

- `Authorized by PR template.`
- `Probably safe.`
- `Tests pass.`
- `No drift` when protected files changed and the change is semantic.

### Protected-Surface Gate Output

Type: text command output from `tools/check_protected_surfaces.py`.

Use:

- A warning from the gate should cause the author to fill
  `Protected-surface authorization` with the issue/contract that permits the
  warned path.
- A forbidden result must block submitter/deployer work until fixed or routed
  to a new contract.
- A passing gate does not prove there is no semantic drift; authors still must
  fill the drift budget.

## Outputs

### PR Template Section

Destination: `.github/pull_request_template.md`

Required fields:

| Field | Required response |
| --- | --- |
| `Runtime/parser behavior` | Whether runtime or parser behavior changed. |
| `Parser event shape/classes` | Whether parser event classes or payload shape changed. |
| `Workbook/webhook/App Script shape` | Whether workbook rows/schema, webhook payloads, or Apps Script assumptions changed. |
| `Parser truth ownership` | Whether truth moved between parser/state and downstream layers. |
| `Fixtures/evidence` | Whether fixtures were added, removed, regenerated, reinterpreted, or only used locally. |
| `Protected-surface authorization` | Issue/contract citation for protected surfaces, or `No drift`. |
| `Residual drift / accepted gaps` | Any known remaining drift or accepted risk. |
| `Follow-up required` | Follow-up issue/report/link, or `N/A`. |

Allowed response labels:

- `No drift`: no semantic change in this category.
- `Authorized drift`: category changed and the current issue/contract
  explicitly authorizes it.
- `Residual drift`: a known gap, risk, unrelated failure, or incomplete check
  remains and must be visible to reviewers/deployers.
- `N/A`: category does not apply to the PR.

Rules:

- `Authorized drift` must cite an issue and contract.
- `Residual drift` must cite a report, issue, check failure, or follow-up.
- `No drift` must not be used to hide a behavior, shape, fixture, or protected
  source change.
- `N/A` must not be used for protected-surface authorization when protected
  paths changed.

### Expected Filled Example

```markdown
## Drift Budget

Use `No drift`, `Authorized drift`, `Residual drift`, or `N/A`. For any `Authorized drift` or `Residual drift`, cite the issue and contract that allow it.

- Runtime/parser behavior: No drift.
- Parser event shape/classes: No drift.
- Workbook/webhook/App Script shape: No drift.
- Parser truth ownership: No drift.
- Fixtures/evidence: N/A.
- Protected-surface authorization: Authorized drift - issue #39 and `docs/contracts/code_hardening_pr_drift_budget.md` authorize `.github/pull_request_template.md` workflow wording only.
- Residual drift / accepted gaps: No drift.
- Follow-up required: N/A.
```

## Invariants

- The drift budget exposes semantic drift; it does not authorize drift.
- Protected-surface changes still require an issue and contract.
- Template-only authorization is invalid for schema, parser truth, event shape,
  webhook payload, Apps Script, match/game identity, deduplication, secrets,
  raw logs, generated data, runtime status files, failed posts, or workbook
  exports.
- Existing PR template sections for issue/contract links, risk tier, layer
  ownership, changes, tests, contract verification, still-unverified items, and
  workflow handoff must remain.
- The section must stay short enough for Codex F to complete reliably.
- Reviewer/deployer roles must not treat a checked or filled drift budget as a
  substitute for reviewing the diff.

## Error Behavior

If the drift-budget section is absent after implementation:

- Codex E should report a blocking contract mismatch.

If required fields are missing:

- Codex E should report a blocking contract mismatch.

If a PR uses `No drift` while the diff or implementation handoff shows
behavior/schema/truth/fixture/protected-surface drift:

- Codex E should report a blocking finding and route to Codex D or Codex F to
  correct the PR description, or to Codex B/A if the underlying change lacks
  authorization.

If a PR uses `Authorized drift` without an issue and contract:

- Codex E/F/G should treat the PR as not ready.

If a PR records `Residual drift` with no follow-up or acceptance rationale:

- Codex E should decide whether it is blocking. Codex G must not merge a PR
  with unresolved blocking residual drift.

If the protected-surface gate reports forbidden artifacts:

- Submitter/deployer work must stop until the artifact is removed or an
  explicitly approved contract changes the policy.

## Side Effects

Allowed implementation side effect:

- Edit `.github/pull_request_template.md` to add the drift-budget section.

Allowed documentation side effects:

- Create/update
  `docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md`.
- Create/update
  `docs/contract_test_reports/code_hardening_pr_drift_budget.md`.

Forbidden side effects:

- Do not change parser behavior.
- Do not change parser state final reconciliation.
- Do not change parser event classes or payload shapes.
- Do not change workbook schema.
- Do not change webhook payload shape.
- Do not change Apps Script behavior.
- Do not change match/game identity or deduplication.
- Do not change secrets or environment variables.
- Do not commit raw logs, generated data, runtime status files, failed posts,
  or workbook exports.
- Do not change CI behavior in this module unless a new contract authorizes it.
- Do not mark tracker #33 complete.

## Dependency Order

Future implementation should proceed in this order:

1. Compare the current PR template to this contract.
2. Add the drift-budget section after `## Layer Ownership` and before
   `## Changes`.
3. Preserve all existing PR template sections and links.
4. Run documentation and protected-surface validation.
5. Produce the implementation handoff.
6. Route to Codex E for contract-test review.

If implementation requires changing `docs/agent_rules.yml`,
`docs/agent_constitution.md`, CI, tooling, parser/runtime files, workbook
schema, webhook payloads, or Apps Script, stop and route back to Codex B or A.

## Compatibility

- The existing PR template remains Markdown.
- Existing section names remain stable unless this contract explicitly inserts
  the new section between them.
- Existing checkboxes under `Risk Tier` and `Contract Verification` remain.
- Existing `Workflow Handoff` YAML block remains.
- Existing protected-surface diff gate behavior remains unchanged.
- Existing branch policy remains: hardening PRs target
  `codex/code-hardening-suite`, not `main`, unless explicitly approved.

## Tests Required

Contract-writer validation:

```bash
git diff --check
```

Implementation validation:

```bash
git diff --check
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "## Drift Budget" .github/pull_request_template.md
rg -n "Runtime/parser behavior|Parser event shape/classes|Workbook/webhook/App Script shape|Parser truth ownership|Fixtures/evidence|Protected-surface authorization|Residual drift / accepted gaps|Follow-up required" .github/pull_request_template.md
```

Repo-level validation is not required for a PR-template-only edit unless the
implementation touches code, tests, CI, or tooling. If code, tests, CI, or
tooling are touched, add focused validation and run:

```bash
python3 -m pytest -q
python3 -m ruff check src tests tools
```

## Acceptance Criteria

- `docs/contracts/code_hardening_pr_drift_budget.md` exists.
- `.github/pull_request_template.md` contains `## Drift Budget`.
- The section is placed after `## Layer Ownership` and before `## Changes`.
- The section includes all eight required fields.
- The section names the four allowed response labels.
- The section states that `Authorized drift` or `Residual drift` requires an
  issue and contract citation.
- Existing PR template gates are preserved.
- The implementation does not change parser/runtime/workbook/App Script
  behavior or protected data/artifact surfaces.
- The implementation handoff records validation and any unrelated untracked
  files.

## Handoff Packet

Role performed: Codex B: Module Contract Writer

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/39

Contract produced: `docs/contracts/code_hardening_pr_drift_budget.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Risk tier: Medium

Owning truth layer: repository coordination and PR lifecycle

Public interface:

- New `.github/pull_request_template.md` section named `## Drift Budget`.
- Required fields: runtime/parser behavior, parser event shape/classes,
  workbook/webhook/App Script shape, parser truth ownership,
  fixtures/evidence, protected-surface authorization, residual drift /
  accepted gaps, and follow-up required.

Invariants:

- The PR template exposes drift but does not authorize protected changes.
- Protected-surface changes require an issue and contract.
- Parser truth remains parser/state owned.
- Existing PR gates stay intact.

Required tests:

- `git diff --check`
- `python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite`
- `rg` checks for the drift-budget section and required fields

Acceptance criteria:

- Add only the contracted PR template section.
- Preserve existing PR template sections.
- Preserve all protected surfaces and branch policy.

Open questions or contract risks:

- `docs/agent_rules.yml` is still absent on the hardening branch even though
  issue #39 names it. This contract records the absence and does not add it.
- The protected-surface gate will warn on `.github/pull_request_template.md`
  as `workflow_authority_docs`; that warning is expected and must be cited as
  authorized by issue #39 and this contract.
- The current worktree contains unrelated untracked diagnostics-mode files;
  implementer/submitter roles must not absorb them into this module.

Next recommended thread role: Codex C: Module Implementer

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for issue #39 and docs/contracts/code_hardening_pr_drift_budget.md.

Goal:
Update the pull request template with the contracted drift-budget section, preserving existing PR gates and avoiding any parser/runtime/workbook/App Script behavior changes.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/39
- https://github.com/Tahjali11/Mythic-Edge/issues/33
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/contracts/code_hardening_protected_surface_gate.md
- .github/pull_request_template.md
- tools/check_protected_surfaces.py

Do:
- Compare the current PR template against the contract before editing.
- Add the Drift Budget section after `## Layer Ownership` and before `## Changes`.
- Preserve existing PR template sections and workflow handoff block.
- Produce docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md with the comparison, files changed, validation run, open risks, and next recommended role.

Do not:
- Implement code or change CI/tooling unless the contract is routed back for expansion.
- Change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Weaken protected-surface review or imply template-only authorization for schema/truth changes.
- Absorb unrelated untracked diagnostics-mode files into this module.
- Target main; hardening PR work belongs on codex/code-hardening-suite.
- Mark tracker #33 complete.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/39"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/code_hardening_pr_drift_budget.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "not run - implementation validation belongs to Codex C"
  stop_conditions:
    - "Do not implement code or edit the PR template in the contract writer pass."
    - "Do not weaken protected-surface review or imply template-only authorization for schema/truth changes."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not absorb unrelated untracked diagnostics-mode files into this module."
    - "Do not target main; hardening PR work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
