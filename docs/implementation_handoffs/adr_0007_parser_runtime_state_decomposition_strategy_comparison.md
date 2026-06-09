# ADR-0007 Parser Runtime State Decomposition Strategy Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/307

## Tracker

N/A

## Contract

`docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`

## Internal Project Area

Quality / Governance and Parser architecture policy.

## Truth Owner

Parser/state remains the truth owner for event interpretation, normalized
match/game facts, final reconciliation, identity, and deduplication.

ADR-0007 is governance documentation. It does not create parser truth and does
not change runtime behavior.

## Bridge-Code Status

`bridge_code`

The ADR records the approved strategy for future parser runtime state bridge
work. `state.py` remains the compatibility bridge for aliases and helper APIs.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Restoration Follow-Up

Codex E later reported `CT-307-ADR-001`: the ADR-0007 governance package was present only in a stash, not in the active checkout.

Codex C restored the ADR-0007 package back into the active checkout from the stash label:

- `codex-preserve-307-adr-before-294-restore`

Because stash indices drift as new stashes are created, the label above is the durable restoration evidence. During this restoration pass, the active #302 live-capture diagnostics package was preserved first under:

- `codex-preserve-302-before-307-adr-restore`

A stray #302 contract-test report that resurfaced during the final status pass was also preserved separately under:

- `codex-preserve-stray-302-report-before-307-final`

The prior Codex E report for ADR-0007 remained active as:

- `docs/contract_test_reports/adr_0007_parser_runtime_state_decomposition_strategy.md`

## Package-Isolation Worktree Follow-Up

Codex E later reported that the active primary checkout showed unrelated #294
auto-refresh work while the ADR-0007 package needed review. Codex C created an
isolated worktree for this package:

- Worktree: sibling checkout `MythicEdge-adr-0007-307`
- Worktree branch: `codex/adr-0007-package-isolation-307`
- Base: `origin/codex/analytics-foundation`

The ADR-0007 package was restored into that isolated worktree from:

- `codex-preserve-307-adr-before-294-restore-final`

The primary `codex/analytics-foundation` checkout remains available for the
active #294 package and was not mutated by this package-isolation worktree
restore.

## Source Artifacts Used

- GitHub issue #307
- GitHub PR #308
- Merge commit `19192f718f8b50e1d7fe962d02455b0c933985ad`
- `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `docs/contracts/parser_runtime_state_decomposition.md`
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`
- `docs/contract_test_reports/parser_runtime_state_decomposition.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `src/mythic_edge_parser/app/posting_state.py`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `docs/contracts/parser_runtime_state_decomposition.md`
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`
- `docs/contract_test_reports/parser_runtime_state_decomposition.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `src/mythic_edge_parser/app/posting_state.py`

## Current Behavior Compared To Contract

Before this slice:

- PR #308 had already merged the `PostingState` pilot into
  `codex/analytics-foundation`.
- Merge commit `19192f718f8b50e1d7fe962d02455b0c933985ad` was present on the
  current branch.
- Issue #307 remained open.
- `docs/decisions/README.md` indexed ADR-0001 through ADR-0006.
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
  did not exist.
- The source contract existed locally as an untracked Codex B artifact.

Contract-required gap:

- Create ADR-0007 as a Proposed ADR unless explicitly approved otherwise.
- Index ADR-0007 in `docs/decisions/README.md`.
- Do not implement parser runtime code or accept the ADR in this slice.

## Implementation Option Chosen

Implemented the docs-only ADR adoption option authorized by the contract.

ADR-0007 was created as `Proposed`, not `Accepted`, because the handoff and
contract explicitly recommend Proposed unless the user explicitly approves
otherwise.

## What Changed

- Created `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`.
- Updated `docs/decisions/README.md` to index ADR-0007.
- Created this implementation handoff.

## Files Changed

- `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md`

## Exact Doc Sections Changed

`docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`

- Added full ADR record following `docs/decisions/ADR_TEMPLATE.md`.
- Status set to `Proposed`.
- Recorded issue #307, PR #308, merge commit, pilot contract, handoff, report,
  and related ADRs.
- Recorded `PostingState` as the proven pilot pattern.
- Defined one-state-cluster-per-contract strategy.
- Preserved compatibility aliases as intentional bridge code.
- Preserved parser truth ownership and protected-surface rules.
- Listed non-goals and future follow-ups.

`docs/decisions/README.md`

- Added ADR-0007 to the ADR index with status `Proposed`.

## Code Changed

No runtime code changed.

## Tests Added Or Updated

No tests changed. Runtime tests are not required for this docs-only ADR adoption
slice.

## Interface Changes

No function signatures, payload fields, workbook columns, environment variables,
script entrypoints, parser event classes, imports, aliases, or CI gates changed.

Docs interface changed:

- ADR index now includes Proposed ADR-0007.

## Contracted Area Status

Stayed inside the contracted ADR adoption scope.

No parser runtime implementation, alias removal, state.py rewrite, analytics
change, local app change, workbook/webhook/App Script/Sheets change, AI change,
or production behavior change was made.

## Validation Run

- `git diff --check -- docs\contracts\adr_0007_parser_runtime_state_decomposition_strategy.md docs\decisions\ADR-0007-parser-runtime-state-decomposition-strategy.md docs\decisions\README.md docs\implementation_handoffs\adr_0007_parser_runtime_state_decomposition_strategy_comparison.md` -> passed
- `py tools\check_agent_docs.py` -> passed, checked files 47, errors 0, warnings 0
- path-scoped protected-surface scan over the contract, ADR, README, and handoff -> passed, forbidden 0, warnings 0
- path-scoped secret/private-marker scan over the contract, ADR, README, and handoff -> warning only, forbidden 0, warnings 1
  - Warning was in existing `docs/decisions/README.md` protected-surface policy text mentioning failed-post payload markers, not a new secret or private artifact.

Restoration validation rerun after reactivating the ADR-0007 package:

- `gh issue view 307 --repo Tahjali11/Mythic-Edge --json number,title,state,url` -> issue #307 is open
- `gh pr view 308 --repo Tahjali11/Mythic-Edge --json number,state,mergedAt,mergeCommit,baseRefName,headRefName,url,title` -> PR #308 is merged into `codex/analytics-foundation` at merge commit `19192f718f8b50e1d7fe962d02455b0c933985ad`
- `git diff --check` -> passed
- `py tools/check_agent_docs.py` -> passed
- path-scoped protected-surface scan over restored ADR-0007 files -> passed, forbidden 0, warnings 0
- path-scoped secret/private-marker scan over restored ADR-0007 files -> warning only, forbidden 0, warnings 1
  - Warning remains the existing `docs/decisions/README.md` protected-surface policy wording, not a secret or private artifact.

Package-isolation worktree validation:

- `git diff --check` over the ADR-0007 package paths -> passed
- `py tools/check_agent_docs.py` -> passed
- path-scoped protected-surface scan over the ADR-0007 package paths -> passed, forbidden 0, warnings 0
- path-scoped secret/private-marker scan initially failed because this handoff included an absolute local worktree path; the path was replaced with a non-private sibling-worktree label before final validation.
- final path-scoped secret/private-marker scan over the ADR-0007 package paths -> warning only, forbidden 0, warnings 1
  - Warning remains the existing `docs/decisions/README.md` protected-surface policy wording, not a secret or private artifact.

## Still Unverified

- Codex E has not yet reviewed ADR-0007.
- ADR-0007 is not Accepted.
- Issue #307 remains open.
- No runtime parser validation was run because no runtime code changed.

## Reviewer Focus

Codex E should verify:

- ADR-0007 status is Proposed.
- ADR-0007 does not authorize broad parser-state rewrites.
- ADR-0007 correctly records `PostingState` as the pilot.
- ADR-0007 preserves parser truth ownership and protected-surface policy.
- ADR-0007 does not authorize alias removal.
- `docs/decisions/README.md` index entry is accurate.
- No runtime code, tests, imports, parser behavior, or CI gates changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #307 ADR-0007 adoption.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/307

Source PR:
https://github.com/Tahjali11/Mythic-Edge/pull/308

Merge commit:
19192f718f8b50e1d7fe962d02455b0c933985ad

Branch:
codex/analytics-foundation

Contract:
docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md

ADR artifact:
docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md

Implementation handoff:
docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md

Risk tier:
High

Goal:
Review the docs-only ADR-0007 adoption against the contract. Verify that ADR-0007 records the parser runtime state decomposition strategy proven by the PostingState pilot without accepting the ADR, changing runtime code, removing aliases, rewriting state.py, or expanding protected-surface authority.

Review focus:
- ADR-0007 exists and follows ADR template expectations.
- ADR status is Proposed unless explicit user approval says otherwise.
- ADR cites issue #307, PR #308, merge commit 19192f718f8b50e1d7fe962d02455b0c933985ad, the parser runtime decomposition contract, implementation handoff, contract-test report, PostingState, state.py, and tests.
- ADR records PostingState as the first pilot pattern.
- ADR requires one coherent state cluster per future implementation contract.
- ADR preserves parser truth ownership under ADR-0001.
- ADR preserves protected-surface policy under ADR-0004.
- ADR does not authorize broad parser-state rewrites, alias removal, parser behavior changes, analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior changes, import churn, package moves, or CI gates.
- docs/decisions/README.md indexes ADR-0007 accurately as Proposed.

Validation:
git status --short --branch --untracked-files=all
git diff --check -- docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md docs/decisions/README.md docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md
py tools/check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over the contract, ADR, README, and handoff.

Do not:
- edit parser runtime code
- remove aliases
- mark ADR-0007 Accepted without explicit user approval
- stage, commit, push, open a PR, merge, close issue #307, or target main unless explicitly asked

Final output:
- findings first
- contract compliance summary
- validation run and result
- protected-surface/privacy status
- remaining risk
- whether to route to Codex D, Codex F, or hold for explicit ADR acceptance approval
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/307"
  source_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/308"
  merge_commit: "19192f718f8b50e1d7fe962d02455b0c933985ad"
  completed_thread: "C"
  next_thread: "E"
  contract_artifact: "docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md"
  target_artifact: "docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md"
  implementation_handoff: "docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  adr_status: "Proposed"
  verdict: "restored_active_ready_for_contract_review"
  restoration_source: "stash label codex-preserve-307-adr-before-294-restore"
  package_isolation_worktree: "sibling checkout MythicEdge-adr-0007-307"
  package_isolation_branch: "codex/adr-0007-package-isolation-307"
  package_isolation_source: "stash label codex-preserve-307-adr-before-294-restore-final"
  preserved_unrelated_package: "stash label codex-preserve-302-before-307-adr-restore"
  preserved_stray_unrelated_report: "stash label codex-preserve-stray-302-report-before-307-final"
  forbidden_scope_touched: false
```
