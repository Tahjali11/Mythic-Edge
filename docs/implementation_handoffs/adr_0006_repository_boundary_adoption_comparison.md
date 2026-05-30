# ADR-0006 Repository Boundary Adoption Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

Codex D addendum: Module Fixer / narrow governance metadata pass for the
Codex E non-blocking finding that PR/ADR metadata did not cite issue #217
directly.

Codex D status addendum: Module Fixer / narrow governance status pass for the
Codex G blocker that ADR-0006 and the ADR index still showed `Proposed` after
issue #217 entered the acceptance path.

## Related Issue

- ADR adoption governance issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/217
- ADR adoption issue status observed during Codex D metadata pass: OPEN
- Related internal boundary issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/215
- Internal boundary issue status observed during Codex C: CLOSED
- Related draft PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/216
- PR status observed during Codex D metadata pass: OPEN draft, targeting
  `codex/analytics-foundation`.
- Historical note: Codex C did not find or create the adoption governance
  issue or adoption PR; those surfaces now exist and are cited in ADR-0006
  metadata.

## Source Artifact And Contract

- Source artifact:
  `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- Contract:
  `docs/contracts/adr_0006_repository_boundary_adoption.md`
- Target artifact:
  `docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md`
- Branch: `codex/adr-0006-repository-boundary-adoption`
- Risk tier: Medium

## Branch And Git Status

Initial status:

```text
## codex/adr-0006-repository-boundary-adoption
?? docs/contracts/adr_0006_repository_boundary_adoption.md
```

The untracked contract was treated as the Codex B source artifact. No
unrelated dirty files were absorbed into this module.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/implementation_handoffs/internal_project_boundaries_comparison.md`
- `docs/contract_test_reports/internal_project_boundaries.md`
- `docs/contracts/adr_0006_repository_boundary_adoption.md`
- GitHub issue #215
- GitHub issue #217
- GitHub PR #216

## Current Behavior Compared To Contract

### What ADR-0006 Is Supposed To Do

ADR-0006 is supposed to preserve Mythic Edge as a monorepo-first project while
recording safe future repository/package boundary strategy. It should clarify
that internal boundaries are planning and ownership guidance, not authority to
split repositories, move files, rename packages, change imports, add CI gates,
or change parser/runtime/analytics/UI/workbook/webhook/App Script/Sheets/AI/
production behavior.

### What The Repo Already Provided

- ADR-0006 already existed and was marked `Status: Proposed`.
- ADR-0006 already preserved monorepo-first policy.
- ADR-0006 already said repository boundaries do not change truth ownership.
- ADR-0006 already listed protected-surface non-goals.
- `docs/decisions/README.md` already defined ADR authority order and Proposed
  versus Accepted status semantics.
- Issue #215 already produced and reviewed the internal project boundary
  package:
  - `docs/contracts/internal_project_boundaries.md`
  - `docs/implementation_handoffs/internal_project_boundaries_comparison.md`
  - `docs/contract_test_reports/internal_project_boundaries.md`

### Contract Gaps Found

- ADR-0006 still listed related issues as `N/A`, even though issue #215 now
  supplies direct boundary-package evidence.
- ADR-0006 owner metadata reflected earlier drafting/fixer work rather than
  the current adoption workflow.
- ADR-0006 did not cite the issue #215 boundary contract, implementation
  handoff, contract-test report, or the ADR-0006 adoption contract.
- ADR-0006 vocabulary still used older terms such as `corpus`, `advisor`,
  `recommendation`, `workflow`, and `app/evidence` without mapping them to the
  internal project names from issue #215.
- The dependency-direction block still used ambiguous `app/evidence` wording.
- The validation section still described older Codex D draft validation rather
  than the current adoption evidence path.
- `docs/decisions/README.md` summarized ADR-0006 using older boundary names.

## Implementation Option Chosen

Docs-only adoption-candidate revision.

During the Codex C pass, ADR-0006 remained `Status: Proposed` because that
pass prepared the ADR for Codex E review. Codex C did not accept the ADR, open
a PR, merge, or create a new governance issue.

## Files Changed

- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md`

Untracked source artifact preserved:

- `docs/contracts/adr_0006_repository_boundary_adoption.md`

Codex D metadata pass changed:

- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md`
- PR #216 body metadata, to cite issue #217 directly while keeping the PR
  draft.

Codex D status acceptance pass changed:

- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md`
- `docs/contract_test_reports/adr_0006_repository_boundary_adoption.md`

Codex D metadata pass preserved unrelated work:

- `docs/contracts/internal_project_boundary_annotation_organization.md`

## Exact ADR/Docs/Governance Sections Changed

### `docs/decisions/ADR-0006-repository-boundary-strategy.md`

- Updated `Decision owners / workflow role` to reflect Codex A, B, C, and E
  adoption workflow ownership.
- Updated `Related issues` to cite issue #215 and record that no separate ADR
  adoption governance issue exists from this pass.
- Updated `Related PRs` to clarify that no adoption PR was opened during Codex
  C.
- Updated `Related contracts, handoffs, or review reports` to cite the issue
  #215 boundary package and ADR-0006 adoption contract/handoff.
- Updated `Context` to use local MTGA decision-support framing and current
  internal project vocabulary.
- Updated `Decision` to align future boundary names with Parser, Corpus /
  Provenance, Analytics, Local App / UI, Workbook / Transport, Quality /
  Governance, and future AI Integration.
- Clarified future extraction order as planning guidance only.
- Clarified that Workbook / Transport and Local App / UI remain in the primary
  repo by default.
- Replaced the dependency-direction block with current project names.
- Updated `Scope`, `Non-Goals`, `Alternatives Considered`, `Consequences`,
  `Truth Ownership Impact`, and `Protected Surfaces Touched` to match current
  internal boundary vocabulary and protected-surface exclusions.
- Replaced old validation notes with the current issue #215 package, ADR-0006
  adoption contract, Codex C handoff, and pending Codex E review path.
- Added follow-up language for a dedicated adoption governance issue if the
  project wants one before PR submission.
- During Codex C, updated `Notes` to keep `Status: Proposed` for review and
  warn against using `Closes #215` for that adoption-candidate pass.
- Codex D status acceptance pass changed the current ADR status from
  `Proposed` to `Accepted` and preserved the note that the accepted status
  becomes durable precedent only after the approved submitter/deployer path
  lands the change on the approved branch.

### `docs/decisions/README.md`

- Updated only the ADR-0006 index summary row.
- Codex D status acceptance pass updated the ADR-0006 index row from
  `Proposed` to `Accepted`.

## Code/Test/Interface Status

- Code changed: no.
- Tests changed: no.
- Docs changed: yes.
- ADR-only/governance-only: yes.
- Runtime behavior changed: no.
- Interface changes: no runtime interface changes.
- ADR status changed: yes, ADR-0006 now records `Accepted` for issue #217's
  acceptance path.
- ADR index changed: yes, ADR-0006 now records `Accepted`.
- CI gates added: no.

## Protected And Forbidden Scope Confirmation

No repositories were split. No files were moved. No packages were renamed. No
imports were changed. No CI gates were added.

No intentional changes were made to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- event kind values;
- parser payload shapes;
- match identity;
- game identity;
- deduplication;
- analytics behavior;
- SQLite schema or migrations;
- local app/UI behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- AI/model-provider behavior;
- production behavior;
- secrets, credentials, environment variables, raw logs, generated data,
  runtime status files, transport failure payload artifacts, workbook exports,
  generated SQLite files, local JSONL artifacts, fixtures, snapshots, drift
  baselines, or local-only artifacts.

## Validation Run

- `git status --short --branch` -> on
  `codex/adr-0006-repository-boundary-adoption`; changed files are ADR-0006,
  ADR README, this handoff, and the contract-test report.
- `gh pr view 216 --repo Tahjali11/Mythic-Edge ...` -> PR #216 is OPEN,
  draft, targets `codex/analytics-foundation`, merge state CLEAN.
- `gh issue view 217 --repo Tahjali11/Mythic-Edge ...` -> issue #217 is OPEN
  and routes the remaining blocker to Codex D status acceptance.
- `gh pr checks 216 --repo Tahjali11/Mythic-Edge` -> two remote `tests` checks
  passed on the currently pushed PR head.
- `rg` status check over ADR-0006 and the ADR index -> both now show
  `Accepted` for ADR-0006.
- `git diff --check` -> passed.
- `python3 tools/check_agent_docs.py` -> passed; checked 30 files, errors 0,
  warnings 0.
- Path-scoped protected-surface scan over the four D-touched files -> passed;
  forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over the four D-touched files ->
  completed with forbidden 0 and warnings 1. The warning is an existing
  protected-surface wording reference in `docs/decisions/README.md`, not a
  secret or private artifact.
- Generated/raw artifact status check for SQLite, database, JSONL, Player.log,
  frontend build, `node_modules`, and Vite markers in
  `git status --short --ignored=matching` -> no matches.

## Remaining Risks Or Unverified Layers

- ADR-0006 now records `Status: Accepted` for issue #217's acceptance path,
  but PR #216 remains draft and still requires the approved reviewer,
  submitter, and deployer path before merge.
- Issue #217 remains open until the adoption PR lands and Codex G verifies
  completion.
- PR #216 remains the draft ADR-0006 adoption PR and targets
  `codex/analytics-foundation`, not `main`.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Production behavior was not exercised.

## Reviewer Focus

Codex E should verify:

- ADR-0006 records `Status: Accepted`.
- `docs/decisions/README.md` records ADR-0006 as `Accepted`.
- The acceptance-status change is authorized by issue #217 and the adoption
  contract, and preserves the note that durable precedent lands through the
  approved submitter/deployer path.
- ADR-0006 metadata still cites issue #217, PR #216, issue #215, and the
  internal project boundary package accurately.
- Monorepo-first policy is preserved.
- Future extraction order remains planning guidance only, not authorization.
- No forbidden runtime, repo-layout, package, import, CI, protected-surface, or
  local-artifact scope was touched.

## Next Recommended Role

Codex E: Module Reviewer / confirmation thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for the ADR-0006 repository boundary adoption status fix.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/217

Related PR:
https://github.com/Tahjali11/Mythic-Edge/pull/216

Related boundary issue:
https://github.com/Tahjali11/Mythic-Edge/issues/215

Branch:
codex/adr-0006-repository-boundary-adoption

Target branch:
codex/analytics-foundation

Source artifact:
docs/decisions/ADR-0006-repository-boundary-strategy.md

Contract:
docs/contracts/adr_0006_repository_boundary_adoption.md

Implementation handoff:
docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md

Risk tier:
Medium

Task:
Confirm the Codex D status acceptance fix for the Codex G blocker that ADR-0006 and the ADR index still showed Proposed.

Review focus:
- ADR-0006 now says Status: Accepted.
- docs/decisions/README.md now lists ADR-0006 as Accepted.
- The accepted status is limited to the ADR adoption path and does not mark PR #216 ready, merge PR #216, close issue #217, close issue #215, or target main.
- Monorepo-first policy is preserved.
- Future extraction order remains planning guidance only, not authorization.
- Data/privacy and protected-surface exclusions remain intact.
- No repositories were split, files moved, packages renamed, imports changed, CI gates added, or runtime/protected behavior changed.

Do not:
- mark PR #216 ready for review
- merge PR #216
- close issue #217 or issue #215
- use Closes #215
- target main
- split repositories
- move files
- rename packages
- change imports
- add CI gates
- change parser/runtime/analytics/UI/workbook/webhook/App Script/Sheets/AI/production behavior
- touch secrets, credentials, raw logs, generated data, runtime artifacts, transport failure payloads, workbook exports, local JSONL artifacts, generated SQLite files, fixtures, snapshots, drift baselines, or local-only artifacts
- stage, commit, push, or mark any tracker complete unless explicitly asked

Validation:
git status --short --branch
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' docs/decisions/ADR-0006-repository-boundary-strategy.md docs/decisions/README.md docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md docs/contract_test_reports/adr_0006_repository_boundary_adoption.md | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
printf '%s\n' docs/decisions/ADR-0006-repository-boundary-strategy.md docs/decisions/README.md docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md docs/contract_test_reports/adr_0006_repository_boundary_adoption.md | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
gh pr checks 216 --repo Tahjali11/Mythic-Edge

Final review report must include findings, validation, ADR status verdict, protected-surface status, secret/private-marker status, generated artifact status, forbidden-scope status, next recommended role, and workflow_handoff.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer / narrow governance status pass"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/217"
  related_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/216"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/215"
  tracker: ""
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  source_artifact: "docs/decisions/ADR-0006-repository-boundary-strategy.md"
  contract_artifact: "docs/contracts/adr_0006_repository_boundary_adoption.md"
  target_artifact: "docs/contract_test_reports/adr_0006_repository_boundary_adoption.md"
  implementation_handoff: "docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md"
  risk_tier: "Medium"
  branch: "codex/adr-0006-repository-boundary-adoption"
  finding_fixed:
    - "ADR-0006 and docs/decisions/README.md still showed Proposed after issue #217 entered the acceptance path."
  files_changed:
    - "docs/decisions/ADR-0006-repository-boundary-strategy.md"
    - "docs/decisions/README.md"
    - "docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md"
    - "docs/contract_test_reports/adr_0006_repository_boundary_adoption.md"
  adr_status: "Accepted"
  pr_status: "open draft"
  stop_conditions:
    - "Do not split repositories."
    - "Do not move files."
    - "Do not rename packages."
    - "Do not change imports."
    - "Do not add CI gates."
    - "Do not change parser/runtime/analytics/UI/workbook/webhook/App Script/Sheets/AI/production behavior."
    - "Do not target main."
```
