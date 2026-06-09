# ADR-0007 Acceptance And Issue #307 Lifecycle Contract

## Module

ADR-0007 acceptance and issue #307 lifecycle closeout.

Plain English: ADR-0007 already exists as a reviewed, merged `Proposed` ADR.
This contract defines whether the evidence is strong enough to accept it, what
small docs-only changes are allowed to mark it accepted, and what Codex G must
verify before closing issue #307.

This is a contract-writing artifact only. It does not accept ADR-0007, close
issue #307, change parser/runtime behavior, remove compatibility aliases,
rewrite `state.py`, open a PR, merge anything, or touch preserved stashes.

## Source Issue

- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/307
- Source PRs:
  - https://github.com/Tahjali11/Mythic-Edge/pull/308
  - https://github.com/Tahjali11/Mythic-Edge/pull/309
- PR #308 merge commit: `19192f718f8b50e1d7fe962d02455b0c933985ad`
- PR #309 merge commit: `0bfef5066cb2264fda7337ee511ffb8bf67490f7`
- Branch: `codex/analytics-foundation`
- Contract artifact: `docs/contracts/adr_0007_acceptance_lifecycle.md`
- Risk tier: High

Observed during this Codex B pass:

```text
git status --short --branch --untracked-files=all
## codex/analytics-foundation...origin/codex/analytics-foundation
```

The branch was clean at inspection time. `git rev-list --left-right --count
HEAD...origin/codex/analytics-foundation` returned `0 0`, so the local branch
was even with origin after fetch.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/contracts/parser_runtime_state_decomposition.md`
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`
- `docs/contract_test_reports/parser_runtime_state_decomposition.md`
- `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md`
- `docs/contract_test_reports/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `docs/contracts/adr_0006_repository_boundary_adoption.md`
- `docs/project_roadmap.md`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/posting_state.py`
- `tests/test_state.py`
- GitHub issue #307
- GitHub PR #308
- GitHub PR #309
- `git stash list`

## Owning Layer

Owning layer: Quality / Governance.

Truth boundary:

- Parser/state remains the owner of event interpretation, normalized
  match/game facts, parser state, final reconciliation, identity, and
  deduplication.
- ADR-0007 may become accepted governance precedent for future parser runtime
  state decomposition strategy.
- ADR-0007 acceptance must not become authorization for parser behavior changes,
  alias removal, future state-cluster extraction, or protected-surface changes.

## Files Owned By This Contract

Codex B owns only:

- `docs/contracts/adr_0007_acceptance_lifecycle.md`

Future Codex C may edit only:

- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md`

Codex C must route back to Codex B before editing source code, tests, tools,
workflow docs, role docs, templates, CI configuration, package metadata,
schemas, migrations, local app files, workbook/App Script files, or any other
ADR.

Expected Codex E artifact after Codex C:

- `docs/contract_test_reports/adr_0007_acceptance_lifecycle.md`

## Public Interface

The public interface is governance status, not runtime API.

After acceptance, future Mythic Edge threads may cite ADR-0007 as durable
precedent for parser runtime state decomposition strategy. That precedent is
limited to:

- one coherent runtime state cluster per issue and contract;
- behavior-preserving extraction by default;
- compatibility aliases as intentional bridge code;
- reset semantics as a protected compatibility behavior;
- parser truth ownership remaining in parser/state;
- protected-surface changes requiring explicit issue, contract, review, and
  validation authority.

Accepted ADR-0007 remains below active instructions, `AGENTS.md`,
`docs/agent_rules.yml`, `docs/agent_constitution.md`, and current scoped issues
and contracts.

## Observed Current Status

Issue #307 is open.

PR #308 is merged into `codex/analytics-foundation`. It completed the
behavior-preserving `PostingState` pilot:

- `src/mythic_edge_parser/app/posting_state.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_state.py`
- `docs/contracts/parser_runtime_state_decomposition.md`
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`
- `docs/contract_test_reports/parser_runtime_state_decomposition.md`

PR #309 is merged into `codex/analytics-foundation`. It added the ADR-0007
docs package:

- `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md`
- `docs/contract_test_reports/adr_0007_parser_runtime_state_decomposition_strategy.md`

ADR-0007 currently says:

```text
Status: Proposed
```

`docs/decisions/README.md` also indexes ADR-0007 as `Proposed`.

## Acceptance Readiness Verdict

ADR-0007 is ready to accept through a small docs-only Codex C/E/F/G lifecycle.

Evidence is sufficient because:

- PR #308 landed the `PostingState` pilot.
- The pilot was scoped to downstream posting and delivery bookkeeping, not
  parser truth.
- The pilot preserved parser truth ownership, helper APIs, reset semantics,
  compatibility aliases, and row snapshot copy behavior.
- Codex E found no blocking findings for the pilot.
- PR #308 merged into the approved integration branch.
- PR #309 created ADR-0007 as `Proposed`, updated the ADR index, and added the
  ADR contract, handoff, and review report.
- Codex E found no blocking findings for the ADR-0007 Proposed package.
- PR #309 merged into the approved integration branch.
- GitHub checks for PR #309 passed.
- Protected-surface validation for the ADR package passed with forbidden 0 and
  warnings 0.
- Secret/private-marker validation for the ADR package had forbidden 0 and only
  the expected ADR README policy wording warning.
- ADR-0007 explicitly says it does not authorize broad parser rewrites, parser
  behavior changes, alias removal, protected-surface changes, package moves,
  import churn, CI gates, or production behavior.

Missing evidence is limited to lifecycle evidence:

- ADR-0007 has not yet been changed from `Proposed` to `Accepted`.
- `docs/decisions/README.md` has not yet been updated from `Proposed` to
  `Accepted`.
- A final issue #307 completion comment has not yet been posted.
- Issue #307 has not yet been closed.

## Contract Decision

Accept ADR-0007, but only through a later reviewed docs-only implementation
thread.

Codex B does not mark the ADR accepted. Codex C may prepare the minimal docs
edit that changes ADR-0007 and the ADR index from `Proposed` to `Accepted`.
Codex E should verify that the status-only adoption remains within this
contract. Codex F should submit the reviewed package. Codex G should merge the
package and close #307 only after merge gates pass.

## Required ADR Acceptance Edits

Codex C should make the smallest possible docs-only update.

Required edit in:

```text
docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md
```

- Change `Status: Proposed` to `Status: Accepted`.
- Add PR #309 and merge commit `0bfef5066cb2264fda7337ee511ffb8bf67490f7`
  to related PR/evidence sections if they are missing.
- Add this contract to related contracts:
  `docs/contracts/adr_0007_acceptance_lifecycle.md`.
- Add the future acceptance comparison/report paths if Codex C/E create them.
- Update follow-up wording so it no longer says ADR-0007 must be routed
  through Codex E before becoming durable precedent.
- Preserve future follow-ups for any later state-cluster extraction or alias
  removal.
- State that acceptance becomes effective through reviewed merge into
  `codex/analytics-foundation`.

Required edit in:

```text
docs/decisions/README.md
```

- Change the ADR-0007 index status from `Proposed` to `Accepted`.
- Preserve the decision summary unless Codex C finds a concrete mismatch.

Required new handoff:

```text
docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md
```

## Files Out Of Scope

Codex C must not edit:

- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/posting_state.py`
- `tests/test_state.py`
- other parser/runtime code
- local app code
- analytics code
- workbook, webhook, Apps Script, or Google Sheets files
- CI configuration
- validation tools
- stashes
- generated/private/local artifacts
- issue or PR state

Codex G owns issue closure and final lifecycle comments after reviewed merge.

## Acceptance Guarantees

Accepting ADR-0007 guarantees only this governance rule:

Future parser runtime state decomposition should proceed one behavior-preserving
state cluster at a time, with explicit contracts, compatibility bridges, and
validation.

Accepting ADR-0007 does not authorize:

- parser behavior changes;
- parser state final reconciliation changes;
- parser event class, event kind, or payload shape changes;
- match/game identity changes;
- deduplication changes;
- alias removal;
- another state-cluster extraction;
- broad `state.py` rewrite;
- package moves or import churn;
- analytics schema or ingest changes;
- local app behavior changes;
- workbook schema changes;
- webhook payload shape changes;
- Apps Script or Google Sheets behavior changes;
- OpenAI/model-provider, AI/coaching, Line Tracer, or production behavior;
- CI gate changes;
- raw/private/generated/local artifact handling changes.

## Issue #307 Lifecycle Recommendation

Issue #307 should close after ADR-0007 is accepted and merged, unless Codex G
finds a concrete missing artifact or unresolved blocker.

Rationale:

- #307 framed the parser runtime state decomposition strategy.
- The first `PostingState` pilot is complete and merged.
- The Proposed ADR package is complete and merged.
- This contract recommends acceptance based on existing evidence.
- No additional implementation is required under #307 once the ADR status and
  index are updated to `Accepted`.

Future parser-state decompositions should be new child issues or contracts, not
reopened work under #307.

## Codex G Closeout Criteria

Codex G may close #307 only after verifying:

- The ADR acceptance PR is merged into `codex/analytics-foundation`.
- ADR-0007 says `Status: Accepted`.
- `docs/decisions/README.md` indexes ADR-0007 as `Accepted`.
- The acceptance PR used an approved base and did not target `main`.
- GitHub checks passed or named failures were explicitly waived by the user.
- Codex E found no blocking findings or all findings were fixed/accepted.
- The final diff is docs-only and within this contract.
- No parser/runtime code, tests, tools, CI, local app, analytics, workbook,
  webhook, Apps Script, Google Sheets, AI/model-provider, production, secret,
  generated, raw log, SQLite, failed-post, workbook export, or local-only
  artifact scope was touched.
- The issue completion comment records:
  - PR #308 and merge commit `19192f718f8b50e1d7fe962d02455b0c933985ad`;
  - PR #309 and merge commit `0bfef5066cb2264fda7337ee511ffb8bf67490f7`;
  - the ADR acceptance PR and merge commit;
  - durable artifacts produced;
  - validation/check status;
  - any preserved stashes or local follow-up material as excluded local state.

## Stash And Local-Material Handling

This contract observed preserved local stashes, including labels for #294,
#304, and #307 follow-up material.

Codex B does not inspect stash contents beyond listing labels, and does not
apply, drop, modify, or route stashes.

Recommended handling:

- Keep preserved stashes untouched during ADR-0007 acceptance.
- Mention relevant labels in handoffs only as local routing context.
- Do not treat stashed #294/#304/#302 material as part of #307 acceptance.
- Do not let stash cleanup block ADR acceptance unless a stash contains the
  only copy of a required #307 acceptance artifact.
- Route stash cleanup separately if the user asks for Codex G cleanup or local
  checkout hygiene.

## Error Behavior

If Codex C finds ADR-0007 already accepted:

- do not duplicate the edit;
- verify the README index;
- produce the comparison handoff and route to Codex E or G depending on
  whether reviewed acceptance evidence already exists.

If Codex C finds ADR-0007 text accidentally authorizes parser behavior changes,
alias removal, or protected-surface changes:

- do not accept as-is;
- revise the wording within this contract's docs-only scope if the fix is
  narrow and obvious;
- otherwise route back to Codex B.

If Codex E finds missing acceptance evidence:

- route to Codex D for concrete docs fixes, or to Codex B if the lifecycle
  contract is wrong.

If Codex G finds the acceptance PR merged but issue #307 still implies future
  work:

- leave #307 open;
- post a blocker comment naming the missing work and route to the correct next
  role.

## Side Effects

Allowed side effect in this Codex B pass:

- create `docs/contracts/adr_0007_acceptance_lifecycle.md`.

Expected future side effects:

- Codex C changes ADR-0007 status and README index status.
- Codex E creates or updates the contract-test report.
- Codex F opens a draft PR.
- Codex G may merge and close #307 after explicit user request and merge-gate
  verification.

Forbidden side effects in this Codex B pass:

- editing ADR-0007;
- editing the ADR index;
- closing issue #307;
- opening or merging PRs;
- applying or dropping stashes;
- editing runtime code, tests, tools, schemas, migrations, CI, local app,
  analytics, workbook, webhook, Apps Script, Google Sheets, AI/model-provider,
  production, or local-artifact files.

## Dependency Order

Expected future workflow:

1. Codex C applies the minimal ADR status/index update and writes the
   implementation handoff.
2. Codex E reviews the acceptance update against this contract.
3. Codex D fixes concrete review findings only if needed.
4. Codex F submits a reviewed docs-only PR using `Closes #307` only if Codex E
   agrees the acceptance package fully satisfies #307; otherwise use
   `Refs #307`.
5. Codex G handles merge, final issue comment, and issue closure after explicit
   user request and merge-gate verification.

## Validation Requirements

Codex B validation for this contract:

```powershell
git status --short --branch --untracked-files=all
git diff --check -- docs\contracts\adr_0007_acceptance_lifecycle.md
py tools\check_agent_docs.py
@'
docs/contracts/adr_0007_acceptance_lifecycle.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/adr_0007_acceptance_lifecycle.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Recommended Codex C validation:

```powershell
git status --short --branch --untracked-files=all
git diff --check -- docs\contracts\adr_0007_acceptance_lifecycle.md docs\decisions\ADR-0007-parser-runtime-state-decomposition-strategy.md docs\decisions\README.md docs\implementation_handoffs\adr_0007_acceptance_lifecycle_comparison.md
py tools\check_agent_docs.py
@'
docs/contracts/adr_0007_acceptance_lifecycle.md
docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md
docs/decisions/README.md
docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/adr_0007_acceptance_lifecycle.md
docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md
docs/decisions/README.md
docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Runtime tests are not required unless Codex C edits runtime behavior, which
this contract forbids.

## Acceptance Criteria

- `docs/contracts/adr_0007_acceptance_lifecycle.md` exists.
- The contract records ADR-0007 current status as `Proposed`.
- The contract records PR #308 and PR #309 merge evidence.
- The contract gives an acceptance readiness verdict.
- The contract defines required evidence for acceptance.
- The contract defines the exact files in scope for acceptance.
- The contract defines files and behavior out of scope.
- The contract defines issue #307 lifecycle recommendation.
- The contract defines Codex G closeout criteria.
- The contract defines stash/local-material handling.
- The contract includes validation expectations.
- The contract includes a pasteable Codex C prompt.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer / comparison thread.

Codex C should make the minimal docs-only acceptance update, then route to
Codex E for review.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/307

Branch:
codex/analytics-foundation

Source contract:
docs/contracts/adr_0007_acceptance_lifecycle.md

Goal:
Apply the minimal docs-only acceptance update for ADR-0007. Change ADR-0007 and the ADR index from Proposed to Accepted only within the contract's scope, record PR #309 merge evidence if missing, and produce docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status with untracked files.
- Verify issue #307 is open.
- Verify PR #308 and PR #309 are merged.
- Confirm ADR-0007 currently says Status: Proposed.
- Preserve all stashes and unrelated local material; do not apply or drop stashes.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/adr_0007_acceptance_lifecycle.md
- docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md
- docs/decisions/README.md
- docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md
- docs/implementation_handoffs/adr_0007_parser_runtime_state_decomposition_strategy_comparison.md
- docs/contract_test_reports/adr_0007_parser_runtime_state_decomposition_strategy.md
- PR #308
- PR #309
- issue #307

Allowed edits:
- docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md
- docs/decisions/README.md
- docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md

Do:
- Change ADR-0007 status to Accepted.
- Change the ADR index row for ADR-0007 to Accepted.
- Add PR #309 and merge commit 0bfef5066cb2264fda7337ee511ffb8bf67490f7 to ADR evidence if missing.
- Add docs/contracts/adr_0007_acceptance_lifecycle.md as related contract evidence.
- Remove or revise stale wording that says ADR-0007 still needs review before becoming durable precedent.
- Preserve the rule that future state-cluster extraction and alias removal still require separate contracts.
- Produce the implementation handoff.

Do not:
- edit parser/runtime code or tests
- remove compatibility aliases
- rewrite state.py
- change parser behavior, parser state final reconciliation, parser event classes, event kinds, parser payload shapes, match/game identity, deduplication, analytics schema, live capture semantics, local app behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, or credential policy
- edit CI or validation tools
- apply, drop, or modify stashes
- target main
- close #307
- stage, commit, push, open a PR, or merge unless explicitly asked

Validation:
git status --short --branch --untracked-files=all
git diff --check -- docs\contracts\adr_0007_acceptance_lifecycle.md docs\decisions\ADR-0007-parser-runtime-state-decomposition-strategy.md docs\decisions\README.md docs\implementation_handoffs\adr_0007_acceptance_lifecycle_comparison.md
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over the contract, ADR, README, and handoff.

Final handoff must include:
- role performed
- issue reviewed
- branch and git status
- files changed
- ADR status before and after
- README index status before and after
- validation results
- protected-surface status
- secret/private-marker status
- stash/local-material handling
- whether forbidden scope was touched
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/307"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md"
  contract_artifact: "docs/contracts/adr_0007_acceptance_lifecycle.md"
  target_artifact: "docs/implementation_handoffs/adr_0007_acceptance_lifecycle_comparison.md"
  source_prs:
    - "https://github.com/Tahjali11/Mythic-Edge/pull/308"
    - "https://github.com/Tahjali11/Mythic-Edge/pull/309"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  current_adr_status: "Proposed"
  recommended_adr_status: "Accepted through reviewed docs-only update"
  validation:
    - "git status --short --branch --untracked-files=all"
    - "git diff --check -- docs\\contracts\\adr_0007_acceptance_lifecycle.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not accept ADR-0007 directly from Codex B."
    - "Do not implement parser/runtime code."
    - "Do not remove aliases or authorize alias removal."
    - "Do not apply, drop, or modify stashes."
    - "Do not close #307 outside Codex G closeout."
    - "Do not target main."
```
