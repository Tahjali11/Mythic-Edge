# ADR-0006 Repository Boundary Adoption Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

Codex D addendum: Module Fixer / narrow governance metadata pass for the
Codex E non-blocking finding that PR/ADR metadata did not cite issue #217
directly.

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

ADR-0006 remains `Status: Proposed` because this Codex C pass prepares the ADR
for Codex E review. It does not accept the ADR, open a PR, merge, or create a
new governance issue.

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
- Updated `Notes` to keep `Status: Proposed` for review and warn against
  using `Closes #215` for this adoption pass.

### `docs/decisions/README.md`

- Updated only the ADR-0006 index summary row.
- ADR-0006 status remains `Proposed`.

## Code/Test/Interface Status

- Code changed: no.
- Tests changed: no.
- Docs changed: yes.
- ADR-only/governance-only: yes.
- Runtime behavior changed: no.
- Interface changes: no runtime interface changes.
- ADR status changed: no, ADR-0006 remains `Proposed`.
- ADR index changed: yes, summary text only.
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
  ADR README, untracked adoption contract, and this handoff.
- `gh issue view 215 --repo Tahjali11/Mythic-Edge --json number,title,state,url`
  -> issue #215 is CLOSED.
- `gh issue list --repo Tahjali11/Mythic-Edge --search "ADR-0006 repository boundary adoption" --json number,title,state,url`
  -> `[]`; no matching new ADR adoption governance issue found.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed; checked 46 files, errors 0,
  warnings 0.
- Path-scoped protected-surface scan over the ADR adoption contract, ADR-0006,
  ADR README, and this handoff -> passed; forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over the same four files ->
  forbidden 0, warnings 1. The warning is an existing protected-surface wording
  reference in `docs/decisions/README.md`, not a secret or private artifact.
- Generated artifact status check for SQLite, database, JSONL, Player.log,
  WAL/SHM/journal markers in `git status --short --ignored=matching` -> no
  matches.

## Remaining Risks Or Unverified Layers

- ADR-0006 remains Proposed and should not be treated as accepted authority
  until Codex E review and the approved submitter/deployer path complete.
- Issue #217 now exists as the direct ADR-0006 adoption governance issue.
- PR #216 now exists as the draft ADR-0006 adoption PR and remains draft.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Production behavior was not exercised.

## Reviewer Focus

Codex E should verify:

- ADR-0006 remains Proposed and is not treated as accepted by this pass.
- ADR-0006 metadata cites issue #217 directly.
- ADR-0006 metadata cites PR #216 directly.
- The revised ADR satisfies the adoption contract without expanding scope.
- The issue #215 boundary package citations are accurate.
- The boundary vocabulary aligns with Parser, Corpus / Provenance, Analytics,
  Local App / UI, Workbook / Transport, Quality / Governance, and future AI
  Integration.
- The ADR index summary update is appropriate and status-preserving.
- No forbidden runtime, repo-layout, package, import, CI, protected-surface, or
  local-artifact scope was touched.

## Next Recommended Role

Codex E: Module Reviewer / confirmation thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for the ADR-0006 repository boundary adoption metadata fix.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/217

Related PR:
https://github.com/Tahjali11/Mythic-Edge/pull/216

Related boundary issue:
https://github.com/Tahjali11/Mythic-Edge/issues/215

Branch:
codex/adr-0006-repository-boundary-adoption

Source artifact:
docs/decisions/ADR-0006-repository-boundary-strategy.md

Contract:
docs/contracts/adr_0006_repository_boundary_adoption.md

Implementation handoff:
docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md

Risk tier:
Medium

Task:
Confirm the Codex D metadata fix for the prior non-blocking finding that PR/ADR metadata did not cite issue #217 directly. Lead with findings ordered by severity.

Review focus:
- ADR-0006 remains Status: Proposed unless the contract-authorized acceptance path has actually happened.
- The ADR cites issue #217 directly as the ADR adoption governance issue.
- The ADR cites PR #216 directly as the draft adoption PR.
- The ADR still cites issue #215 and the internal project boundary package as related evidence.
- The decision-owner metadata reflects Codex A/B/C/E adoption workflow roles.
- Vocabulary aligns with Parser, Corpus / Provenance, Analytics, Local App / UI, Workbook / Transport, Quality / Governance, and future AI Integration.
- Monorepo-first policy is preserved.
- Future extraction order is planning guidance only, not authorization.
- Dependency direction uses current internal project names.
- Data/privacy and protected-surface exclusions remain intact.
- The implementation handoff routing/status notes reflect issue #217 and PR #216 without rewriting historical Codex C observations.
- No repositories were split, files moved, packages renamed, imports changed, CI gates added, or runtime/protected behavior changed.

Do not:
- Accept ADR-0006 by review fiat.
- Split repositories.
- Move files.
- Rename packages.
- Change imports.
- Add CI gates.
- Change parser/runtime/analytics/UI/workbook/webhook/App Script/Sheets/AI/production behavior.
- Touch secrets, credentials, raw logs, generated data, runtime artifacts, transport failure payloads, workbook exports, local JSONL artifacts, generated SQLite files, fixtures, snapshots, drift baselines, or local-only artifacts.
- Stage, commit, push, mark PR #216 ready for review, merge, close issues, or mark any tracker complete unless explicitly asked.

Validation:
git status --short --branch
git diff --check
py tools\check_agent_docs.py
@'
docs/decisions/ADR-0006-repository-boundary-strategy.md
docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/decisions/ADR-0006-repository-boundary-strategy.md
docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

Final review report must include:
- role performed
- issue/PR used
- source artifact reviewed
- contract and handoff reviewed
- files reviewed
- findings ordered by severity
- validation run and result
- ADR status verdict
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- recommendation: route to D, B/A, F, or accept/no-op
- pasteable next-role prompt if applicable
- workflow_handoff block
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer / narrow governance metadata pass"
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
    - "PR/ADR metadata did not cite issue #217 directly."
  files_changed:
    - "docs/decisions/ADR-0006-repository-boundary-strategy.md"
    - "docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md"
  pr_metadata_updated: true
  adr_status: "Proposed"
  stop_conditions:
    - "Do not accept ADR-0006 without scoped contract/review."
    - "Do not split repositories."
    - "Do not move files."
    - "Do not rename packages."
    - "Do not change imports."
    - "Do not add CI gates."
    - "Do not change parser/runtime/analytics/UI/workbook/webhook/App Script/Sheets/AI/production behavior."
    - "Do not target main."
```
