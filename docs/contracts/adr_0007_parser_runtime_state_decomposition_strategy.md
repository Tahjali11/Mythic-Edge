# ADR-0007 Parser Runtime State Decomposition Strategy Contract

## Metadata

- Role: Codex B / Module Contract Writer
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/307
- Source PR: https://github.com/Tahjali11/Mythic-Edge/pull/308
- Source merge commit: `19192f718f8b50e1d7fe962d02455b0c933985ad`
- Branch: `codex/analytics-foundation`
- Contract artifact: `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`
- Expected ADR artifact: `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- Risk tier: High
- ADR status before this contract: not created

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/contracts/parser_runtime_state_decomposition.md`
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`
- `docs/contract_test_reports/parser_runtime_state_decomposition.md`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/posting_state.py`
- `tests/test_state.py`
- GitHub issue #307
- GitHub PR #308

## Observed Current Behavior

The parser runtime state decomposition pilot has already landed through PR #308 on `codex/analytics-foundation`. The merged pilot extracted `PostingState` into `src/mythic_edge_parser/app/posting_state.py`, nested it under `ParserRuntimeState.posting`, and preserved the existing import-compatible aliases and helper APIs in `state.py`.

The original pilot contract explicitly avoided creating ADR-0007 before the first extraction. That stop condition is now satisfied: the pilot has been implemented, reviewed, submitted, merged, and validated as behavior-preserving.

`docs/decisions/README.md` currently indexes ADR-0001 through ADR-0006. ADR-0007 does not exist yet, and issue #307 remains open. The correct next step is therefore a contract-first ADR adoption thread, not another parser-state implementation pass.

## Contract Decision

Codex C may create the ADR artifact and update the ADR index, but must not implement runtime changes in the ADR adoption slice.

The expected ADR artifact is:

`docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`

Codex C may also update:

`docs/decisions/README.md`

The ADR must start with status `Proposed` unless the user explicitly authorizes marking it `Accepted` in the Codex C prompt or a later reviewed adoption thread. This contract does not itself accept ADR-0007.

## ADR Purpose

ADR-0007 should record the durable architecture rule proven by the `PostingState` pilot: parser runtime state may be decomposed into smaller, named state clusters only through incremental, behavior-preserving extractions with compatibility bridges and focused validation.

The ADR should prevent future parser-state work from becoming a large rewrite, a hidden truth-ownership change, or an alias-breaking cleanup. It should make the successful `PostingState` extraction the precedent for future state decomposition, not permission to split all state at once.

## Required ADR Scope

ADR-0007 must define:

- Parser runtime state decomposition as a staged architecture strategy.
- `PostingState` as the first accepted pilot pattern.
- One coherent state cluster per implementation contract.
- Behavior preservation as the default requirement.
- Compatibility aliases as intentional bridges, not accidental leftovers.
- Reset semantics as part of the public runtime-state contract.
- Import compatibility for existing callers during transition periods.
- Explicit contracts before removing legacy aliases.
- Parser truth ownership boundaries for state clusters that affect match/game interpretation.
- Protected-surface review requirements for high-risk state clusters.
- Validation expectations for every future extraction.

## State Cluster Guidance

The ADR should name likely parser runtime state clusters without requiring immediate extraction.

Recommended cluster categories:

- Posting and downstream delivery bookkeeping.
- Match lifecycle state.
- Game lifecycle state.
- Player, seat, team, and identity state.
- Mulligan and opening-hand state.
- Draft, deck, and sideboard state.
- Runtime diagnostics and drift status.
- Analytics or local-app bridge state, if any, only where it does not own parser truth.

The ADR should distinguish parser-truth state from downstream bookkeeping:

- Parser-truth clusters affect normalized match facts, game facts, event interpretation, player identity, game identity, or final reconciliation.
- Downstream bookkeeping clusters track delivery, posting, local status, diagnostics, or transport progress and must not reinterpret parser facts.

`PostingState` belongs in downstream bookkeeping. It is the safest precedent because it tracks posted rows and delivery bookkeeping, not Arena event interpretation.

## Compatibility Bridge Rules

Future state-cluster extractions must preserve compatibility unless a later contract explicitly authorizes a breaking cleanup.

Required bridge rules:

- Existing public aliases must continue to point at the same nested state containers after extraction.
- `reset_runtime_state()` must clear both the nested cluster and any compatibility aliases.
- Helper APIs must keep their existing behavior and signatures unless a separate contract changes them.
- Tests must prove alias identity where compatibility aliases remain.
- Tests must prove reset behavior and posted-once guard behavior where applicable.
- Alias removal must be treated as a separate contract/test/review decision, not part of an extraction by default.

## Truth Ownership Guarantees

ADR-0007 must preserve ADR-0001 parser ownership:

- The parser/state layer owns event interpretation and normalized match/game facts.
- State decomposition must not move truth to workbook, webhook, local app, analytics, AI, or tests.
- Compatibility bridges must not become alternate truth sources.
- Downstream status, diagnostics, posting, and analytics state may describe parser output, but may not reinterpret it.

## Protected-Surface Guarantees

ADR-0007 must preserve ADR-0004 protected-surface rules. It must not authorize:

- Parser behavior changes.
- Parser state final reconciliation changes.
- Parser event class changes.
- Match/game identity or deduplication changes.
- Workbook schema changes.
- Webhook payload shape changes.
- Apps Script behavior changes.
- Analytics schema or ingest changes.
- Local app behavior changes.
- Production behavior changes.

If a future state cluster touches one of these surfaces, that extraction needs an explicit issue, contract, implementation handoff, review or contract-test report, and protected-surface validation.

## Relationship To Existing ADRs

ADR-0007 should explicitly relate to:

- ADR-0001: parser/state owns truth; decomposition must preserve this.
- ADR-0003: Player.log evidence drift should be handled with explicit uncertainty, not hidden state rewrites.
- ADR-0004: protected-surface changes require scoped authorization and validation.
- ADR-0006: internal repository boundaries remain monorepo-first; this ADR does not authorize moving packages, renaming modules, or changing imports broadly.

## Out Of Scope

This contract does not authorize:

- Creating ADR-0007 as `Accepted` without explicit approval.
- Implementing any new parser-state extraction.
- Removing compatibility aliases.
- Rewriting `state.py`.
- Changing parser behavior.
- Changing parser state final reconciliation.
- Changing parser event classes.
- Changing match/game identity or deduplication.
- Changing workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, analytics behavior, local app behavior, AI/model-provider behavior, or production behavior.
- Adding CI gates.
- Targeting `main`.
- Closing issue #307.

## Expected ADR Structure

ADR-0007 should follow `docs/decisions/ADR_TEMPLATE.md` and the ADR guidance in `docs/decisions/README.md`.

Required sections:

- Title.
- Status.
- Date.
- Decision owners.
- Related issues, PRs, contracts, handoffs, and reports.
- Context.
- Decision.
- Scope.
- Non-goals.
- Alternatives considered.
- Consequences.
- Truth ownership.
- Protected surfaces.
- Validation and review evidence.
- Supersedes.
- Superseded by.
- Follow-ups.
- Notes.

## Evidence To Cite In ADR-0007

ADR-0007 should cite:

- Issue #307 as the motivating issue.
- PR #308 as the successful pilot implementation.
- Merge commit `19192f718f8b50e1d7fe962d02455b0c933985ad`.
- `docs/contracts/parser_runtime_state_decomposition.md`.
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`.
- `docs/contract_test_reports/parser_runtime_state_decomposition.md`.
- `src/mythic_edge_parser/app/posting_state.py`.
- `src/mythic_edge_parser/app/state.py`.
- `tests/test_state.py`.
- The validation evidence recorded in PR #308.

## Acceptance Criteria

Codex C satisfies this contract when:

- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md` exists.
- `docs/decisions/README.md` indexes ADR-0007.
- ADR-0007 starts as `Proposed` unless explicit user approval says otherwise.
- ADR-0007 records `PostingState` as the proven pilot.
- ADR-0007 preserves parser truth ownership and protected-surface rules.
- ADR-0007 does not authorize broad parser-state rewrites.
- ADR-0007 does not implement code.
- Issue #307 remains open unless a later Codex G or user-approved issue-lifecycle thread closes it.

## Validation Expectations

Codex C should run:

```powershell
git status --short --branch
git diff --check -- docs\contracts\adr_0007_parser_runtime_state_decomposition_strategy.md docs\decisions\ADR-0007-parser-runtime-state-decomposition-strategy.md docs\decisions\README.md
py tools\check_agent_docs.py
@'
docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md
docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md
docs/decisions/README.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md
docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md
docs/decisions/README.md
'@ | py tools\check_secret_patterns.py --paths-from-stdin
```

No runtime pytest is required unless Codex C edits runtime code, which is out of scope for this ADR adoption slice.

## Expected Codex C Scope

Codex C should:

- Compare the current ADR index and ADR template against this contract.
- Create ADR-0007.
- Update the ADR index.
- Produce an implementation handoff at `docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md`.
- Preserve unrelated untracked or dirty files.

Codex C should not:

- Edit parser runtime code.
- Edit tests.
- Remove aliases.
- Change validation tooling.
- Stage, commit, push, open a PR, merge, or close #307 unless explicitly asked.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #307.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/307

Branch:
codex/analytics-foundation

Source contract:
docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md

Expected ADR artifact:
docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md

Expected implementation handoff:
docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md

Context:
PR #308 merged the behavior-preserving PostingState pilot into codex/analytics-foundation at merge commit 19192f718f8b50e1d7fe962d02455b0c933985ad. ADR-0007 has not been created yet. This is an ADR adoption implementation pass only.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and preserve unrelated changes.
- Confirm ADR-0007 does not already exist.
- Read docs/decisions/README.md and docs/decisions/ADR_TEMPLATE.md.
- Read docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md.
- Read docs/contracts/parser_runtime_state_decomposition.md, docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md, and docs/contract_test_reports/parser_runtime_state_decomposition.md.

Do:
- Create docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md.
- Update docs/decisions/README.md to index ADR-0007.
- Set ADR status to Proposed unless the user explicitly authorizes Accepted.
- Record PostingState as the proven parser runtime state decomposition pilot.
- Preserve parser truth ownership and protected-surface rules.
- Produce docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md.

Do not:
- Implement parser runtime code.
- Remove compatibility aliases.
- Rewrite state.py.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, analytics behavior, local app behavior, AI/model-provider behavior, or production behavior.
- Add CI gates.
- Target main.
- Close #307.
- Stage, commit, push, open a PR, or merge unless explicitly asked.

Validation:
git status --short --branch
git diff --check -- docs\contracts\adr_0007_parser_runtime_state_decomposition_strategy.md docs\decisions\ADR-0007-parser-runtime-state-decomposition-strategy.md docs\decisions\README.md
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over the contract, ADR, and ADR README.

Final handoff must include:
- role performed
- issue reviewed
- branch and git status
- ADR artifact produced
- README index update
- implementation handoff produced
- ADR status chosen and why
- validation run and results
- protected-surface status
- secret/private-marker status
- forbidden scope touched yes/no
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/307"
  source_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/308"
  merge_commit: "19192f718f8b50e1d7fe962d02455b0c933985ad"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md"
  target_artifact: "docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md"
  expected_handoff: "docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  adr_0007_status_before_c: "not_created"
  recommended_adr_0007_status: "Proposed unless explicitly approved otherwise"
  stop_conditions:
    - "Do not implement parser runtime code in the ADR adoption slice."
    - "Do not remove compatibility aliases."
    - "Do not rewrite state.py."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not target main."
    - "Do not close #307."
```
