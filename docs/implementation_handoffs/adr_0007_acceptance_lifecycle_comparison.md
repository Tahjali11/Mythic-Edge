# ADR-0007 Acceptance Lifecycle Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue Reviewed

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/307
- Source PRs:
  - https://github.com/Tahjali11/Mythic-Edge/pull/308
  - https://github.com/Tahjali11/Mythic-Edge/pull/309

## Contract Used

`docs/contracts/adr_0007_acceptance_lifecycle.md`

## Branch And Git Status

- Worktree branch: `codex/adr-0007-acceptance-lifecycle-307`
- Base branch: `origin/codex/analytics-foundation`
- Branch sync before editing: `0 0`
- Git status before editing: only `docs/contracts/adr_0007_acceptance_lifecycle.md` was untracked.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/adr_0007_acceptance_lifecycle.md`
- `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md`
- `docs/contract_test_reports/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/decisions/README.md`
- GitHub issue #307 metadata
- GitHub PR #308 metadata
- GitHub PR #309 metadata

## Current Behavior Compared To Contract

Before this pass, ADR-0007 was present as a reviewed Proposed ADR. The ADR
index also listed ADR-0007 as `Proposed`.

The contract records that the `PostingState` pilot from PR #308 and the
Proposed ADR package from PR #309 were both merged into
`codex/analytics-foundation`. The remaining contract gap was lifecycle-only:
ADR-0007 and the ADR index needed a narrow docs-only status update from
`Proposed` to `Accepted`, plus acceptance evidence and this implementation
handoff.

## Implementation Option Chosen

Implemented the smallest docs-only acceptance update authorized by the
contract.

This pass did not edit parser/runtime code, tests, tools, CI, analytics,
local app, workbook, webhook, Apps Script, Sheets, AI, production, generated
artifact, or private/local artifact surfaces.

## Files Changed

- `docs/contracts/adr_0007_acceptance_lifecycle.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md`

## Exact Sections Changed

`docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`

- Changed `Status: Proposed` to `Status: Accepted`.
- Added PR #309 as related PR evidence.
- Added PR #309 merge commit `0bfef5066cb2264fda7337ee511ffb8bf67490f7`.
- Added `docs/contracts/adr_0007_acceptance_lifecycle.md`.
- Added this acceptance comparison handoff path.
- Revised the Follow-Ups section so it no longer treats ADR-0007 as a Proposed
  ADR awaiting durable-precedent review.
- Preserved future follow-ups for separate state-cluster extraction and alias
  removal contracts.
- Added a note that acceptance becomes durable precedent only through reviewed
  merge into `codex/analytics-foundation`.

`docs/decisions/README.md`

- Changed the ADR-0007 index status from `Proposed` to `Accepted`.
- Preserved the existing decision summary.

`docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md`

- Added this Codex C implementation handoff.

## Status Before And After

- ADR-0007 before: `Proposed`
- ADR-0007 after: `Accepted`
- ADR README index before: `Proposed`
- ADR README index after: `Accepted`

## Validation Run

- `git status --short --branch --untracked-files=all` -> active #307
  acceptance package only:
  - `M docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
  - `M docs/decisions/README.md`
  - `?? docs/contracts/adr_0007_acceptance_lifecycle.md`
  - `?? docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md`
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation`
  -> `0 0`
- `git diff --check -- docs\contracts\adr_0007_acceptance_lifecycle.md docs\decisions\ADR-0007-parser-runtime-state-decomposition-strategy.md docs\decisions\README.md docs\implementation_handoffs\adr_0007_acceptance_lifecycle_comparison.md`
  -> passed
- `py tools\check_agent_docs.py` -> passed, checked files 47, errors 0,
  warnings 0
- path-scoped protected-surface scan over the contract, ADR, README, and
  handoff -> passed, forbidden 0, warnings 0
- path-scoped secret/private-marker scan over the contract, ADR, README, and
  handoff -> warning only, forbidden 0, warnings 1
  - Warning is existing ADR README policy wording about failed-post payload
    markers, not a secret, raw private artifact, or newly introduced private
    value.
- direct trailing-whitespace and final-newline check for new contract and
  handoff files -> passed
- generated frontend build output status -> `frontend/dist` absent

## Protected-Surface Status

Passed: forbidden 0, warnings 0.

The package is docs-only governance status metadata.

## Secret/Private-Marker Status

Warning only: forbidden 0, warnings 1.

The warning is in existing `docs/decisions/README.md` protected-surface policy
wording. No raw private values, raw local paths, raw logs, SQLite files,
generated artifacts, secrets, credentials, or local-only artifacts were added.

## Generated/Private Artifact Status

No generated/private artifacts were created or retained by this docs-only pass.
`frontend/dist` is absent.

## Stash And Local-Material Handling

No stashes were applied, dropped, modified, or inspected as part of this pass.
The primary checkout was not mutated.

## Forbidden Scope

Forbidden scope touched: false.

No parser/runtime behavior, parser state final reconciliation, parser event
classes, event kinds, parser payload shapes, match/game identity,
deduplication, analytics schema or ingest behavior, live capture semantics,
local app behavior, workbook schema, webhook payload shape, Apps Script
behavior, Google Sheets behavior, output transport, OpenAI/model-provider
behavior, AI/coaching behavior, Line Tracer behavior, production behavior,
CI gates, dependency metadata, generated artifacts, or local/private artifacts
were changed.

## Remaining Risks

- Codex E still needs to review this acceptance package against the contract.
- Codex F still needs to submit a reviewed docs-only PR.
- Codex G owns merge closeout and issue #307 closure after reviewed merge.

## Next Recommended Role

Codex E: Governance Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Governance Reviewer / contract-test thread for issue #307 ADR-0007 acceptance lifecycle.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/307

Source PRs:
https://github.com/Tahjali11/Mythic-Edge/pull/308
https://github.com/Tahjali11/Mythic-Edge/pull/309

Branch:
codex/adr-0007-acceptance-lifecycle-307

Base branch:
origin/codex/analytics-foundation

Contract:
docs/contracts/adr_0007_acceptance_lifecycle.md

ADR artifact:
docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md

Implementation handoff:
docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md

Goal:
Review the docs-only ADR-0007 acceptance lifecycle update against the contract. Verify that ADR-0007 and the ADR index were changed from Proposed to Accepted only within the authorized governance scope, with PR #309 merge evidence recorded, and without runtime/parser/protected-surface changes.

Review focus:
- ADR-0007 status is Accepted.
- docs/decisions/README.md indexes ADR-0007 as Accepted.
- PR #309 and merge commit 0bfef5066cb2264fda7337ee511ffb8bf67490f7 are recorded.
- docs/contracts/adr_0007_acceptance_lifecycle.md is recorded as related acceptance evidence.
- Acceptance is described as durable only after reviewed merge into codex/analytics-foundation.
- Future parser state-cluster extraction and alias removal still require separate issues/contracts/reviews.
- No parser/runtime code, tests, tools, CI, analytics, local app, workbook, webhook, Apps Script, Sheets, AI, production, generated, private, or local-only artifact scope was touched.

Validation:
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git diff --check -- docs/contracts/adr_0007_acceptance_lifecycle.md docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md docs/decisions/README.md docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md
py tools/check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over the contract, ADR, README, and handoff.

Do not:
- edit parser/runtime code or tests
- remove compatibility aliases
- rewrite state.py
- change parser behavior, parser state final reconciliation, parser event classes, event kinds, parser payload shapes, match/game identity, deduplication, analytics schema, live capture semantics, local app behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, or credential policy
- apply, drop, or modify stashes
- target main
- close #307
- stage, commit, push, open a PR, or merge unless explicitly asked

Final output:
- findings first
- contract compliance summary
- validation run and result
- protected-surface/privacy status
- remaining risk
- whether to route to Codex D, Codex F, or hold
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/307"
  completed_thread: "C"
  next_thread: "E"
  worktree: "MythicEdge-adr-0007-acceptance-307"
  branch: "codex/adr-0007-acceptance-lifecycle-307"
  base_branch: "origin/codex/analytics-foundation"
  contract_artifact: "docs/contracts/adr_0007_acceptance_lifecycle.md"
  adr_artifact: "docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md"
  implementation_handoff: "docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md"
  source_prs:
    - "https://github.com/Tahjali11/Mythic-Edge/pull/308"
    - "https://github.com/Tahjali11/Mythic-Edge/pull/309"
  adr_status_before: "Proposed"
  adr_status_after: "Accepted"
  readme_index_status_before: "Proposed"
  readme_index_status_after: "Accepted"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex E: Governance Reviewer / contract-test thread"
```
