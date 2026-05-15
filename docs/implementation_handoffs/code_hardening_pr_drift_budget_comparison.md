# Code Hardening PR Drift Budget Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/39

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Source contract: `docs/contracts/code_hardening_pr_drift_budget.md`

Target branch: `codex/code-hardening-suite`

Role: Codex C: Module Implementer

Risk tier: Medium

## Summary Of Implementation Comparison

The current pull request template was missing the contracted `## Drift Budget`
section. This pass adds only that section to `.github/pull_request_template.md`
and preserves the existing PR gates, risk tier, layer ownership, changes,
tests, contract verification, still-unverified, and workflow handoff sections.

Changed files for this module:

- `.github/pull_request_template.md`
- `docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md`

No code, CI, tooling, parser/runtime behavior, workbook schema, webhook
payload shape, Apps Script behavior, parser event classes, parser state final
reconciliation, match/game identity, deduplication, secrets, raw logs,
generated data, runtime status files, failed posts, or workbook exports were
changed.

## Findings First

### Resolved: missing Drift Budget section

Contract requirement:

- Insert `## Drift Budget` after `## Layer Ownership`.
- Insert it before `## Changes`.
- Preserve all eight required fields.
- Preserve the four allowed response labels.
- Preserve the authorization sentence requiring issue and contract citations
  for `Authorized drift` or `Residual drift`.

Initial state:

- `.github/pull_request_template.md` did not contain `## Drift Budget`.

Resolution:

- Added the contracted section after `## Layer Ownership` and before
  `## Changes`.

### No behavior/schema/truth authorization added

The new template wording exposes drift; it does not authorize protected
changes by itself. Protected-surface changes still require the current issue
and contract.

## Confirmed Matches

- `## Summary` remains present.
- `## Linked Issue And Contract` remains present.
- `## Risk Tier` remains present with existing checkboxes.
- `## Layer Ownership` remains present.
- `## Changes` remains present after the new Drift Budget section.
- `## Tests` remains present.
- `## Contract Verification` remains present.
- `## Still Unverified` remains present.
- `## Workflow Handoff` remains present with the YAML block.
- The Drift Budget section includes all required fields:
  - `Runtime/parser behavior`
  - `Parser event shape/classes`
  - `Workbook/webhook/App Script shape`
  - `Parser truth ownership`
  - `Fixtures/evidence`
  - `Protected-surface authorization`
  - `Residual drift / accepted gaps`
  - `Follow-up required`
- The section names the four allowed response labels:
  - `No drift`
  - `Authorized drift`
  - `Residual drift`
  - `N/A`
- The section states that any `Authorized drift` or `Residual drift` requires
  an issue and contract citation.

## Contract Mismatches

No unresolved contract mismatch is known after this pass.

Expected validation nuance:

- `.github/pull_request_template.md` is a workflow authority document, so the
  protected-surface gate should warn on it when this change is committed into
  a branch diff. That warning is expected and authorized by issue #39 and
  `docs/contracts/code_hardening_pr_drift_budget.md`.

## Missing Safeguards

No blocking missing safeguard remains for this PR-template-only implementation.

Safeguards preserved:

- The template does not imply template-only authorization for parser truth,
  schema, workbook, webhook, Apps Script, event shape, match/game identity, or
  deduplication changes.
- Existing contract verification checkboxes remain.
- Existing workflow handoff block remains.
- The protected-surface diff gate remains unchanged.

## Missing Or Weak Tests

No focused tests were added because the contract does not require a test file
for this PR-template-only edit.

The contract-required validation is command-based:

- `git diff --check`
- protected-surface gate command
- `rg` checks for the section and required fields

Repo-level pytest/Ruff validation is not required because no code, tests, CI,
or tooling were changed.

## Validation Evidence

Commands run before writing this final handoff:

```bash
rg -n "## Drift Budget" .github/pull_request_template.md
```

Result:

```text
26:## Drift Budget
```

```bash
rg -n "Runtime/parser behavior|Parser event shape/classes|Workbook/webhook/App Script shape|Parser truth ownership|Fixtures/evidence|Protected-surface authorization|Residual drift / accepted gaps|Follow-up required" .github/pull_request_template.md
```

Result:

```text
30:- Runtime/parser behavior:
31:- Parser event shape/classes:
32:- Workbook/webhook/App Script shape:
33:- Parser truth ownership:
34:- Fixtures/evidence:
35:- Protected-surface authorization:
36:- Residual drift / accepted gaps:
37:- Follow-up required:
```

```bash
git diff --check
```

Result: passed with no output.

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Result:

```text
Protected Surface Gate
base: origin/codex/code-hardening-suite
head: HEAD
changed_paths: 0
forbidden: 0
warnings: 0

result: passed
```

Because the gate inspects committed branch diffs, Codex C also ran a direct
path seam for the modified PR template:

```bash
printf ".github/pull_request_template.md\n" | python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Result:

```text
Protected Surface Gate
base: origin/codex/code-hardening-suite
head: HEAD
changed_paths: 1
forbidden: 0
warnings: 1

WARNING workflow_authority_docs .github/pull_request_template.md - Protected workflow authority surface; issue/contract must authorize this change.

result: passed
```

Protected source/data sanity:

```bash
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports
```

Result: passed with no output.

## Still-Unverified Layers

- GitHub Actions/Windows CI was not run.
- Submitter/deployer PR checks have not run.
- The drift budget has not yet been filled in a real PR body.
- Tracker #33 remains open and must not be marked complete by this role.
- `docs/agent_rules.yml` is still absent on this hardening branch, as recorded
  by the contract.

## Unrelated Worktree Files

The following untracked files were present before or during this module pass
and are unrelated to issue #39:

```text
docs/contracts/code_hardening_live_diagnostics_mode.md
docs/implementation_handoffs/code_hardening_live_diagnostics_mode_comparison.md
src/mythic_edge_parser/app/live_diagnostics.py
tests/test_live_diagnostics.py
```

They were not edited or intentionally absorbed into this PR drift-budget
module.

Related untracked source artifact from Codex B:

```text
docs/contracts/code_hardening_pr_drift_budget.md
```

## Protected Surface Evidence

No protected parser/runtime/workbook/App Script/data artifact surfaces were
edited by this module.

Edited protected workflow surface:

- `.github/pull_request_template.md`

Authorization:

- issue #39
- `docs/contracts/code_hardening_pr_drift_budget.md`

## Next Recommended Role

Next recommended role: Codex E: Module Reviewer in contract-test mode.

Reason: the contracted template section is implemented, the existing template
gates are preserved, and validation should now verify placement, exact fields,
and the expected protected-surface warning.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #39:
https://github.com/Tahjali11/Mythic-Edge/issues/39

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Use:
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md
- .github/pull_request_template.md
- docs/contracts/code_hardening_protected_surface_gate.md
- tools/check_protected_surfaces.py
- docs/agent_constitution.md
- docs/codex_module_workflow.md

Goal:
Verify the Module Implementer patch against the PR drift-budget contract.

Confirm:
- `.github/pull_request_template.md` contains `## Drift Budget`.
- The section is placed after `## Layer Ownership` and before `## Changes`.
- The section includes all eight required fields.
- The section names `No drift`, `Authorized drift`, `Residual drift`, and `N/A`.
- The section states that `Authorized drift` or `Residual drift` requires an issue and contract citation.
- Existing PR template sections and gates remain present.
- The wording exposes semantic drift but does not authorize protected changes by itself.
- The implementation did not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Unrelated untracked diagnostics-mode files were not absorbed into this module.
- The protected-surface warning on `.github/pull_request_template.md`, if observed, is expected and authorized by issue #39 and the contract.

Validation:
Run:
git diff --check
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
printf ".github/pull_request_template.md\n" | python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
rg -n "## Drift Budget" .github/pull_request_template.md
rg -n "Runtime/parser behavior|Parser event shape/classes|Workbook/webhook/App Script shape|Parser truth ownership|Fixtures/evidence|Protected-surface authorization|Residual drift / accepted gaps|Follow-up required" .github/pull_request_template.md

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not weaken protected-surface review or imply template-only authorization for schema/truth changes.
Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not absorb unrelated untracked diagnostics-mode files into this module.
Do not stage, commit, merge, target main, or mark tracker #33 complete.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/39"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/code_hardening_pr_drift_budget.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite"
    - "printf \".github/pull_request_template.md\\n\" | python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin"
    - "rg -n \"## Drift Budget\" .github/pull_request_template.md"
    - "rg -n \"Runtime/parser behavior|Parser event shape/classes|Workbook/webhook/App Script shape|Parser truth ownership|Fixtures/evidence|Protected-surface authorization|Residual drift / accepted gaps|Follow-up required\" .github/pull_request_template.md"
  stop_conditions:
    - "Do not weaken protected-surface review or imply template-only authorization for schema/truth changes."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not absorb unrelated untracked diagnostics-mode files into this module."
    - "Do not target main; hardening PR work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
