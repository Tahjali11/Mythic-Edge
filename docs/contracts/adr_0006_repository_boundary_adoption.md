# ADR-0006 Repository Boundary Adoption Contract

## Module

ADR-0006 repository boundary strategy adoption.

Plain English: ADR-0006 is a proposed durable policy for keeping Mythic Edge
monorepo-first while preserving future package and repository split options.
This contract defines what must be reviewed and revised before ADR-0006 can be
accepted as project policy.

This is a contract-writing artifact only. It does not accept ADR-0006, move
files, split repositories, rename packages, change imports, add CI gates, open
a PR, merge anything, or change runtime behavior.

## Source Issue

- Source artifact:
  `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- Related issue:
  <https://github.com/Tahjali11/Mythic-Edge/issues/215>
- New governance issue:
  recommended by the handoff, but not created by this Codex B pass.
- Tracker: N/A
- Branch:
  `codex/adr-0006-repository-boundary-adoption`

Observed during this Codex B pass:

```text
## codex/adr-0006-repository-boundary-adoption
```

The requested branch did not exist locally or on `origin` during initial
inspection. Codex B created it locally from the clean
`codex/analytics-foundation` baseline at commit `a603302`, which was even with
`origin/codex/analytics-foundation` at the time of branch creation.

## Authority And Source Artifacts Read

- handoff from Codex A
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
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
- GitHub issue #215

## Risk Tier

Medium.

The immediate work is governance documentation, but accepting ADR-0006 creates
durable precedent for future package and repository boundaries. If the ADR is
accepted with stale citations or unclear authority, future agents may treat a
proposed repository split, package split, or boundary enforcement gate as more
authorized than it is.

## Owning Layer

Owning layer: Quality / Governance.

Truth boundary:

- Parser/state truth ownership remains governed by ADR-0001.
- Player.log evidence and drift boundaries remain governed by ADR-0003.
- Protected-surface and schema-change authorization remains governed by
  ADR-0004.
- External integrations and collaboration surfaces remain governed by
  ADR-0005.
- ADR-0006, if accepted, may govern repository/package boundary strategy only.
  It must not become authorization for behavior changes or protected-surface
  changes.

## Files Owned By This Contract

This contract owns only:

- `docs/contracts/adr_0006_repository_boundary_adoption.md`

Future Codex C implementation is authorized to edit only:

- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/README.md`, only if ADR-0006 status or summary changes
- `docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md`

Codex C must route back to Codex B before editing any other authority docs,
templates, workflow docs, issue templates, PR templates, source code, tests,
tools, CI configuration, package metadata, imports, or runtime files.

## Public Interface

The public interface is governance policy, not runtime API.

Other threads may rely on the final adoption artifact for:

- ADR-0006 status semantics;
- repository-boundary vocabulary;
- monorepo-first policy;
- future extraction order as policy guidance;
- package and repository split preconditions;
- cross-repo truth ownership boundaries;
- review evidence required before acceptance;
- non-goals and protected-surface exclusions.

Accepted ADR-0006 must remain below active instructions, `AGENTS.md`,
`docs/agent_rules.yml`, `docs/agent_constitution.md`, current issues, and
current contracts in authority order.

## Inputs

### ADR-0006 Draft

Path:

```text
docs/decisions/ADR-0006-repository-boundary-strategy.md
```

Observed input state:

- Status is `Proposed`.
- Related issues are `N/A`.
- Related PRs are `TBD`.
- Decision owners cite Codex A and Codex D from earlier framing/fixer work.
- Related contracts do not yet cite the completed issue #215 internal project
  boundary contract, comparison, or contract-test report.
- The decision already states monorepo-first and no current repository split.
- The decision already states that repository boundaries do not change truth
  ownership.
- The decision already names non-goals and protected surfaces.

### Internal Project Boundary Package

Paths:

```text
docs/contracts/internal_project_boundaries.md
docs/implementation_handoffs/internal_project_boundaries_comparison.md
docs/contract_test_reports/internal_project_boundaries.md
```

Observed input state:

- Issue #215 is closed.
- The contract names Parser, Corpus / Provenance, Analytics, Local App / UI,
  Workbook / Transport, Quality / Governance, and future AI Integration.
- The comparison reports that ADR-0006 is useful proposed context but not
  accepted authority.
- The contract-test report found no blocking findings and confirmed no file
  moves, repository splits, package renames, import changes, CI gates, or
  runtime behavior changes.

## Outputs

Codex B output:

- this contract.

Expected Codex C output:

- a revised ADR-0006 adoption candidate;
- an updated ADR index row if the status or decision summary changes;
- an implementation handoff comparing revisions against this contract.

No runtime output, generated artifact, database, workbook, webhook, Apps
Script deployment, local artifact, or CI gate is produced by this contract.

## Readiness Verdict

ADR-0006 is ready for formal review, but it should be revised before
acceptance.

The current proposed ADR has the right broad direction:

- stay monorepo-first;
- design internal boundaries before extraction;
- treat repository boundaries as packaging/ownership boundaries, not truth
  shortcuts;
- require future issue, contract, review, user approval, compatibility tests,
  and protected-surface checks before extraction.

It needs revision before acceptance because its citations, workflow evidence,
issue linkage, owner metadata, and vocabulary predate the completed internal
project boundaries package.

## Required Guarantees

- ADR-0006 remains documentation/governance only.
- ADR-0006 adoption must not split repositories.
- ADR-0006 adoption must not move files.
- ADR-0006 adoption must not rename packages.
- ADR-0006 adoption must not change imports.
- ADR-0006 adoption must not add CI gates.
- ADR-0006 adoption must not change parser/runtime/analytics/UI/workbook/
  webhook/App Script/Sheets/AI/production behavior.
- ADR-0006 adoption must not authorize protected-surface changes by
  implication.
- ADR-0006 adoption must preserve the authority order in
  `docs/decisions/README.md` and `docs/agent_rules.yml`.
- ADR-0006 adoption must cite the issue #215 boundary package or explain why
  a newer governance issue supersedes issue #215 as the adoption source.
- ADR-0006 adoption must clearly distinguish current monorepo policy from
  possible future extraction policy.
- ADR-0006 adoption must keep future AI/model-provider runtime integration and
  coaching evaluation out of scope unless a separate contract authorizes them.

## Required ADR Revisions Before Acceptance

### Status And Effective Date

ADR-0006 may be prepared as an acceptance candidate only after this contract is
used by Codex C and reviewed by Codex E.

Allowed status handling:

- keep `Status: Proposed` if the next pass is only preparing a review draft; or
- change to `Status: Accepted` in the adoption PR only if the ADR text states
  that acceptance becomes effective after reviewed merge into the approved
  branch.

Codex B does not accept ADR-0006.

### Related Issues

Replace or supplement `N/A` with:

- issue #215, because it produced the internal project boundary contract,
  comparison, and review evidence;
- the new governance issue, if one exists before implementation.

If no new governance issue exists by Codex C, the handoff must say so and the
PR should not use `Closes #215` because #215 is already closed and satisfied.

### Related PRs

`Related PRs` may remain `TBD` during Codex C if the PR does not exist yet.

Before final integration, either:

- ADR-0006 records the adoption PR link; or
- the PR description, submitter handoff, and deployer handoff record the PR as
  adoption evidence.

### Related Contracts And Reports

ADR-0006 must cite:

- `docs/contracts/internal_project_boundaries.md`
- `docs/implementation_handoffs/internal_project_boundaries_comparison.md`
- `docs/contract_test_reports/internal_project_boundaries.md`
- `docs/contracts/adr_0006_repository_boundary_adoption.md`

It may continue citing ADRs 0001 through 0005.

### Decision Owners

Update decision-owner metadata so it reflects the adoption workflow, not only
the earlier draft authors.

Acceptable owner wording:

- Codex A: architecture framing / readiness assessment;
- Codex B: ADR adoption contract;
- Codex C: adoption comparison / revision;
- Codex E: adoption review / contract test.

Codex F/G ownership belongs in PR/deployer evidence unless the file is updated
after PR creation.

### Vocabulary Alignment

ADR-0006 must align with the internal project boundary names from issue #215:

- Parser
- Corpus / Provenance
- Analytics
- Local App / UI
- Workbook / Transport
- Quality / Governance
- future AI Integration

Existing wording such as `advisor`, `recommendation`, `workflow`, and
`app/evidence` may remain only when it is mapped to these project names or
explicitly described as a future sub-boundary.

### Monorepo-First Policy

ADR-0006 must preserve this policy:

- Mythic Edge remains one primary repository until a future issue, contract,
  review, and explicit user-approved migration plan authorizes extraction.
- Internal project boundaries should be kept clear inside the monorepo before
  any package or repository split.
- The current primary repository remains the integration and orchestration home
  unless a future accepted ADR supersedes this policy.

### Future Extraction Order

The preferred future extraction order may remain:

1. Corpus / Provenance first.
2. Parser second.
3. Analytics after parser and provenance stabilize.
4. AI Integration / advisor last.
5. Workflow assets only if they become reusable outside Mythic Edge.

ADR-0006 must clarify that this is planning guidance, not authorization to
extract.

Workbook / Transport and Local App / UI should remain in the primary repo by
default unless a future issue, contract, and ADR explicitly authorize a split.

### Dependency Direction

The future dependency direction must be clarified using current project names.

Required intent:

```text
Corpus / Provenance -> no production code dependency by default
Parser -> may consume pinned sanitized corpus releases for tests
Workbook / Transport -> consumes parser-normalized row contracts
Analytics -> consumes validated parser facts and provenance metadata
Local App / UI -> consumes backend, analytics, setup/status, and display APIs
AI Integration -> consumes deterministic analytics and provenance summaries
Quality / Governance -> may inspect all layers without becoming runtime behavior
```

No future repository or package may become a truth shortcut merely because it
has a separate boundary.

### Data And Privacy Boundaries

ADR-0006 must preserve:

- no raw private Player.log files in future corpus repositories;
- no secrets, credentials, API keys, tokens, webhook URLs, transport failure
  payload artifacts, runtime status files, generated private data, workbook
  exports, generated SQLite databases, or local-only artifacts in extracted
  repositories;
- sanitized or synthetic evidence only for committed corpus artifacts unless a
  later policy explicitly authorizes a narrower safe artifact class.

### Validation Evidence

The validation/review section must be updated from old draft/fixer evidence to
include the current adoption path:

- issue #215 package evidence;
- this contract;
- Codex C comparison or implementation handoff;
- Codex E review or contract-test report;
- path-scoped protected-surface scan;
- path-scoped secret/private-marker scan;
- `git diff --check`.

Runtime parser tests are not required for docs-only ADR adoption unless Codex C
changes runtime code, which this contract forbids.

### Non-Goals And Protected Surfaces

ADR-0006 must continue to state that it does not authorize:

- repository split;
- file move;
- package rename;
- import change;
- CI gate;
- parser behavior change;
- parser state final reconciliation change;
- parser event class, event kind, or payload shape change;
- match/game identity or deduplication change;
- analytics behavior change;
- SQLite schema or migration change;
- local app/UI behavior change;
- workbook schema change;
- webhook payload shape change;
- Apps Script behavior change;
- Google Sheets behavior change;
- AI/model-provider behavior change;
- production behavior change;
- secret, credential, environment variable, or local-artifact change.

## Unknowns

- Whether a new governance issue will be created before Codex C starts.
- Whether the adoption PR should target this new branch directly or another
  approved governance integration branch.
- Whether ADR-0006 should be accepted in the next PR or remain Proposed after
  revision for one more review cycle.
- Whether future `local_app_*` and `workbook_transport_*` contract prefixes
  will be adopted before any physical docs or package reorganization.
- Whether the phrase "competitively-oriented decision support tool" should
  remain as architecture context or be softened to avoid being read as product
  or monetization policy.

## Suspected Gaps

- ADR-0006 currently lacks issue #215 citations and current review evidence.
- ADR-0006 currently has `Related issues: N/A`, which is stale after issue
  #215.
- ADR-0006 currently has `Related PRs: TBD`, which is acceptable before PR
  creation but must be accounted for in submitter/deployer evidence.
- The current decision-owner metadata does not describe the full adoption
  workflow.
- Some ADR wording uses older or broader names such as `advisor` and
  `app/evidence`; these should be reconciled with the internal project names.
- The dependency direction text uses `app/evidence`, which is ambiguous now
  that the repo distinguishes Corpus / Provenance, Local App / UI, and
  Workbook / Transport.
- Future workflow asset extraction needs an explicit ADR-0005 reminder that
  tools, skills, prompts, templates, and connectors do not supersede repo
  authority by implication.

## Error Behavior

If Codex C finds ADR-0006 conflicts with accepted ADRs 0001 through 0005:

- do not force acceptance;
- document the conflict;
- route back to Codex B or Codex A.

If Codex C finds no new governance issue exists:

- do not close or reopen issue #215;
- do not use `Closes #215`;
- record the missing issue as an implementation/handoff risk;
- continue only if the user accepts this contract as sufficient source
  authority, otherwise route back to Codex A for issue creation.

If Codex E finds stale citations, missing review evidence, or ambiguity around
whether status should become `Accepted`:

- route to Codex D for narrow docs fixes when the fix is concrete;
- route to Codex B if the adoption contract is ambiguous;
- route to Codex A if the problem framing or branch target is wrong.

## Side Effects

Allowed side effect in this Codex B pass:

- create `docs/contracts/adr_0006_repository_boundary_adoption.md`.

Forbidden side effects in this Codex B pass:

- editing ADR-0006;
- editing the ADR index;
- creating a GitHub issue;
- opening a PR;
- moving files;
- splitting repositories;
- renaming packages;
- changing imports;
- adding CI gates;
- editing runtime code, tests, tools, package metadata, workflow docs, or
  templates;
- changing parser/runtime/analytics/UI/workbook/webhook/App Script/Sheets/AI/
  production behavior.

## Dependency Order

Expected future workflow:

1. Codex C compares ADR-0006 to this contract, issue #215, the internal
   boundary package, and accepted ADRs 0001 through 0005.
2. Codex C makes only the authorized ADR/index docs revisions and writes an
   implementation handoff.
3. Codex E reviews the ADR adoption candidate against this contract.
4. Codex D fixes concrete review findings only if needed.
5. Codex F stages only reviewed governance docs and opens a draft PR.
6. Codex G handles merge/close/tracker evidence only after explicit user
   request and merge gates pass.

## Compatibility

ADR-0006 must remain compatible with:

- ADR-0001 parser truth ownership;
- ADR-0002 deterministic-local/LLM boundary;
- ADR-0003 Player.log drift policy;
- ADR-0004 protected-surface authorization policy;
- ADR-0005 external integration and collaboration surface policy;
- issue #215 internal project boundary contract;
- current monorepo and single Python package state.

## Validation Requirements

Codex B validation for this contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/adr_0006_repository_boundary_adoption.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/adr_0006_repository_boundary_adoption.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Recommended Codex C validation:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/adr_0006_repository_boundary_adoption.md
docs/decisions/ADR-0006-repository-boundary-strategy.md
docs/decisions/README.md
docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/adr_0006_repository_boundary_adoption.md
docs/decisions/ADR-0006-repository-boundary-strategy.md
docs/decisions/README.md
docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Runtime tests are not required for docs-only ADR adoption unless an
implementation thread changes runtime behavior, which this contract forbids.

## Acceptance Criteria

- `docs/contracts/adr_0006_repository_boundary_adoption.md` exists.
- The contract records that ADR-0006 is currently Proposed.
- The contract records that issue #215 is related and closed.
- The contract records that a new governance issue is recommended but was not
  created in this pass.
- The contract defines what must change before ADR-0006 can be accepted.
- The contract distinguishes accepted ADR authority from proposed ADR context.
- The contract preserves monorepo-first policy.
- The contract forbids repository split, file moves, package renames, import
  changes, CI gates, and runtime behavior changes.
- The contract defines Codex C and Codex E validation expectations.
- The contract includes a pasteable Codex C prompt.
- Codex B validation is reported.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer / comparison thread.

Codex C should revise ADR-0006 only within this contract's approved docs-only
scope and produce an implementation handoff. If a new governance issue exists
by then, Codex C should cite it. If no new issue exists, Codex C should record
that gap and avoid closing issue #215.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for ADR-0006 repository boundary adoption.

Source contract:
docs/contracts/adr_0006_repository_boundary_adoption.md

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/215

Branch:
codex/adr-0006-repository-boundary-adoption

Goal:
Compare docs/decisions/ADR-0006-repository-boundary-strategy.md against the adoption contract, issue #215, the internal project boundary package, and accepted ADRs 0001 through 0005. Revise ADR-0006 and the ADR index only as needed to satisfy the adoption contract. Produce docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md.

Before editing, briefly state:
- what ADR-0006 is supposed to do;
- what it currently does;
- why it is not ready for acceptance as-is;
- the exact minimal docs-only fix plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/decisions/README.md
- docs/decisions/ADR_TEMPLATE.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md
- docs/decisions/ADR-0006-repository-boundary-strategy.md
- docs/contracts/internal_project_boundaries.md
- docs/implementation_handoffs/internal_project_boundaries_comparison.md
- docs/contract_test_reports/internal_project_boundaries.md
- docs/contracts/adr_0006_repository_boundary_adoption.md
- issue #215
- new governance issue if one exists

Allowed edits:
- docs/decisions/ADR-0006-repository-boundary-strategy.md
- docs/decisions/README.md, only if ADR-0006 status or summary changes
- docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md

Do:
- update stale ADR-0006 issue, contract, handoff, review, and validation citations;
- align ADR-0006 vocabulary with Parser, Corpus / Provenance, Analytics, Local App / UI, Workbook / Transport, Quality / Governance, and future AI Integration;
- preserve monorepo-first policy;
- preserve the rule that future extraction needs its own issue, contract, review, validation, user approval, compatibility plan, and protected-surface checks;
- preserve the rule that repository boundaries do not change truth ownership;
- keep or prepare Status: Accepted only as allowed by the contract;
- document whether a new governance issue exists;
- write the comparison handoff.

Do not:
- split repositories;
- move files;
- rename packages;
- change imports;
- add CI gates;
- edit source code, tests, tools, package metadata, workflow docs, role docs, templates, issue templates, or PR templates;
- change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, analytics behavior, SQLite schema/migrations, local app/UI behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, AI/model-provider behavior, production behavior, secrets, credentials, environment variables, raw logs, generated data, runtime status files, transport failure payload artifacts, workbook exports, generated SQLite files, local JSONL artifacts, or local-only artifacts;
- target main;
- close issue #215 unless explicitly asked;
- stage, commit, push, open a PR, or merge unless explicitly asked.

Validation:
git status --short --branch
git diff --check
@'
docs/contracts/adr_0006_repository_boundary_adoption.md
docs/decisions/ADR-0006-repository-boundary-strategy.md
docs/decisions/README.md
docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/adr_0006_repository_boundary_adoption.md
docs/decisions/ADR-0006-repository-boundary-strategy.md
docs/decisions/README.md
docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

Final handoff must include:
- role performed;
- source contract used;
- branch;
- files changed;
- exact ADR sections changed;
- whether ADR-0006 status changed;
- whether the ADR index changed;
- whether a new governance issue exists;
- validation results;
- protected-surface status;
- forbidden scope status;
- remaining risks;
- next recommended role;
- pasteable Codex E prompt;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "new governance issue recommended; related issue https://github.com/Tahjali11/Mythic-Edge/issues/215"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/decisions/ADR-0006-repository-boundary-strategy.md"
  target_artifact: "docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md"
  contract_artifact: "docs/contracts/adr_0006_repository_boundary_adoption.md"
  risk_tier: "Medium"
  branch: "codex/adr-0006-repository-boundary-adoption"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface check"
    - "path-scoped secret/private-marker check"
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
