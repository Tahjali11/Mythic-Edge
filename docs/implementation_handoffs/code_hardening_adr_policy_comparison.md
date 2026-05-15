# Code Hardening ADR Policy Implementation Comparison

Role performed: Codex C: Module Implementer / comparison thread.

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/62

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Contract used: `docs/contracts/code_hardening_adr_policy.md`

Branch: `codex/code-hardening-suite`

Baseline confirmation:

- Current branch was confirmed as `codex/code-hardening-suite`.
- Local branch was confirmed aligned with `origin/codex/code-hardening-suite`.
- Current `HEAD` was confirmed as `8016d82`, the PR #61 merge commit required by the contract.
- Pre-existing unrelated untracked files were observed and left out of this module:
  - `docs/project_roadmap.md`
  - `docs/python_tooling_inventory.md`
- The source contract `docs/contracts/code_hardening_adr_policy.md` was present as an untracked source artifact and was read but not modified by this thread.

## Purpose Compared

ADRs are supposed to be the stable place to record durable cross-project design or process decisions: the context, decision, consequences, and supersession path future threads should cite.

Before this implementation, Mythic Edge had strong issue, contract, review, handoff, drift-budget, and protected-surface workflows, but it lacked:

- a `docs/decisions/` entrypoint
- an ADR template
- ADR status, numbering, authority, and supersession rules
- narrow references from active governance docs to accepted ADRs
- a PR field for `Related ADRs`

That gap mattered because long-lived policy rationale could remain scattered across issues, PRs, contracts, and chat history. Future Codex threads need a repo-owned source that sits below active governing docs and above stale memory or examples.

## Implementation Plan Used

The implementation stayed docs-only and local to the allowed contract scope:

1. Create the ADR directory README.
2. Create the ADR template without consuming a numbered ADR.
3. Add narrow ADR references to the constitution, rule index, workflow doc, and PR template.
4. Preserve issue/contract/review/protected-surface requirements and branch policy.
5. Do not create seed ADRs or numbered ADR files.

## Files Changed

Created:

- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/implementation_handoffs/code_hardening_adr_policy_comparison.md`

Modified:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `.github/pull_request_template.md`

Related but not modified by this thread:

- `docs/contracts/code_hardening_adr_policy.md`

Code changed: no.

Tests changed: no.

Docs changed: yes.

Interface changes:

- Added the governance documentation interface `docs/decisions/`.
- Added `Related ADRs:` to the PR template.
- Added ADR authority and conflict-routing references to governance docs.

## Contract Matches

- `docs/decisions/README.md` now defines ADR purpose, authority, required and not-required categories, status values, naming and numbering rules, required fields, update/supersession policy, citation guidance, and an empty index.
- `docs/decisions/ADR_TEMPLATE.md` now includes the required fields: title, status, date, decision owners/workflow role, related issues, related PRs, related contracts/handoffs/reports, context, decision, scope, non-goals, alternatives, consequences, truth ownership impact, protected surfaces, validation/review evidence, supersedes, superseded by, follow-ups, and notes.
- No seed ADRs or numbered ADR files were created.
- `docs/agent_constitution.md` now has a narrow ADR subsection under artifact-first handoffs.
- `docs/agent_rules.yml` now lists ADR docs in document architecture, places accepted ADRs above older docs/examples/memory, and adds concise ADR conflict behavior.
- `docs/codex_module_workflow.md` now tells workflow roles to cite related ADRs or route conflicts before implementation.
- `.github/pull_request_template.md` now has a `Related ADRs:` field under linked issue and contract.
- ADRs remain below active governing docs and scoped issue/contract authority.
- ADRs are explicitly not automatic authorization for protected-surface changes.
- Existing problem representations, module contracts, handoffs, review reports, PR drift budgets, protected-surface checks, and branch policy were preserved.

## Contract Mismatches

No intentional contract mismatches remain in the implemented docs.

One operational caveat remains: the protected-surface gate's normal `--base` mode checks the committed branch diff (`origin/codex/code-hardening-suite...HEAD`). Because this Module Implementer thread did not commit, that required command reports zero changed paths. A supplemental local path-list check was run to classify the actual working-tree files.

## Missing Safeguards Or Missing Tests

- No automated ADR linter exists yet to enforce required fields, monotonic numbering, status values, or README index updates.
- No automated YAML/schema check is part of the required validation, though a direct YAML parse was run for `docs/agent_rules.yml`.
- No seed ADRs exist yet by design; the tracker lists seed architecture decision records as the next separate queue item.
- The protected-surface gate does not inspect untracked files in normal mode. Codex F should stage only intended files and rerun protected-surface validation before opening a PR.

## Snapshot And Data Safety Notes

- No raw logs, runtime status files, failed posts, workbook exports, generated card data, secrets, webhook URLs, local absolute paths as requirements, live workbook IDs, or production deployment details were added.
- No snapshot files were created.
- No parser/runtime/workbook/webhook/Apps Script behavior changed.

## Validation Run And Result

Required validation:

- `git diff --check` -> passed with no output.
- `py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite` -> passed; reported `changed_paths: 0`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- `rg -n "Architecture Decision Records|ADR|docs/decisions|Related ADRs" docs\agent_constitution.md docs\agent_rules.yml docs\codex_module_workflow.md .github\pull_request_template.md docs\decisions\README.md docs\decisions\ADR_TEMPLATE.md` -> passed; found the ADR references in the expected files.

Supplemental validation:

- `docs/agent_rules.yml` YAML parse via Python/PyYAML -> passed.
- Local protected-surface path-list check with `--paths-from-stdin` -> passed; reported `changed_paths: 8`, `forbidden: 0`, `warnings: 4`, and expected `workflow_authority_docs` warnings for:
  - `.github/pull_request_template.md`
  - `docs/agent_constitution.md`
  - `docs/agent_rules.yml`
  - `docs/codex_module_workflow.md`

Runtime parser tests were skipped because this was a docs-only governance change and no runtime code changed.

## Protected-Surface Status

Protected workflow authority docs were intentionally touched:

- `.github/pull_request_template.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`

Those warnings are authorized by issue #62 and `docs/contracts/code_hardening_adr_policy.md`.

No protected parser/runtime/workbook/webhook/Apps Script surfaces were touched.

## Still-Unverified Layers

- GitHub PR rendering of the new `Related ADRs:` field.
- Future Codex E contract-test review.
- Future Codex F staging/commit/push behavior.
- Protected-surface gate output after the intended files are committed or pushed to a PR branch.
- Any future seed ADR content, which remains out of scope for issue #62.

## Next Recommended Role

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Review focus:

- Confirm the ADR README and template satisfy the contract without becoming seed ADRs.
- Confirm ADR authority is below active governing docs and current issue/contract authority, above handoffs/reports that do not supersede ADRs by themselves, and above stale memory/examples.
- Confirm no protected-surface policy was weakened.
- Confirm the PR template field is narrow and does not require ADRs for every small PR.
- Confirm unrelated untracked docs remain outside this module.

## Pasteable Next-Thread Prompt

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer / contract-test thread for the Code Hardening child issue: ADR policy and constitutional amendment.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/62

Branch target:
codex/code-hardening-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/review.md
- docs/agent_threads/contract_test.md
- docs/contracts/code_hardening_adr_policy.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/templates/workflow_handoff.md
- .github/pull_request_template.md
- docs/decisions/README.md
- docs/decisions/ADR_TEMPLATE.md
- docs/implementation_handoffs/code_hardening_adr_policy_comparison.md
- issue #33
- issue #62

Task:
Review the ADR policy implementation against docs/contracts/code_hardening_adr_policy.md. This is a docs-only governance review. Lead with findings ordered by severity. If clean, say so clearly and record residual risks.

Check:
- docs/decisions/README.md defines purpose, authority, required/not-required categories, lifecycle statuses, naming, required fields, update/supersession policy, citations, and index scope.
- docs/decisions/ADR_TEMPLATE.md includes all required template fields and is not a numbered seed ADR.
- No seed ADRs or numbered ADR files were created.
- docs/agent_constitution.md, docs/agent_rules.yml, docs/codex_module_workflow.md, and .github/pull_request_template.md received only narrow ADR references.
- ADR authority remains below active governing docs and current issue/contract authority, above handoffs/reports that do not supersede ADRs by themselves, and above stale memory/examples.
- ADRs are not treated as automatic authorization for protected-surface changes.
- PR template still preserves issue/contract, drift-budget, risk-tier, layer ownership, tests, contract verification, still-unverified, and workflow handoff sections.
- Unrelated untracked files are not absorbed into this module.

Do not:
- Implement fixes unless explicitly asked.
- Create seed ADRs or numbered ADR files.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy.
- Treat ADRs as automatic authorization for protected-surface changes.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "Architecture Decision Records|ADR|docs/decisions|Related ADRs" docs\agent_constitution.md docs\agent_rules.yml docs\codex_module_workflow.md .github\pull_request_template.md docs\decisions\README.md docs\decisions\ADR_TEMPLATE.md

Output:
Produce docs/contract_test_reports/code_hardening_adr_policy.md or provide a PR review-style report if asked. Include findings, contract matches, contract mismatches, missing safeguards/tests, validation run, residual risk, and next recommended role.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/62"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/code_hardening_adr_policy.md"
  target_artifact: "docs/contract_test_reports/code_hardening_adr_policy.md"
  implementation_artifact: "docs/implementation_handoffs/code_hardening_adr_policy_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite"
    - "rg -n \"Architecture Decision Records|ADR|docs/decisions|Related ADRs\" docs\\agent_constitution.md docs\\agent_rules.yml docs\\codex_module_workflow.md .github\\pull_request_template.md docs\\decisions\\README.md docs\\decisions\\ADR_TEMPLATE.md"
  stop_conditions:
    - "Do not create seed ADRs or numbered ADR files under issue #62."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy."
    - "Do not treat ADRs as automatic authorization for protected-surface changes."
    - "Do not broadly rewrite the constitution, workflow, PR template, or rule index."
    - "Do not absorb unrelated untracked files into this module."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
