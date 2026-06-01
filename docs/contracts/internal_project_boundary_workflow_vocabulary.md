# Internal Project Boundary Workflow Vocabulary Contract

## Module

Docs-only workflow vocabulary alignment after ADR-0006 and the internal project
map.

Plain English: this contract defines how future Mythic Edge issues, templates,
contracts, handoffs, reviews, and PR metadata should refer to internal project
areas without changing code, layout, imports, runtime behavior, or validation
gates.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/221
- Tracker: N/A
- Related completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/215
- Related completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/218
- Related ADR: `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- Primary source map: `docs/internal_project_map.md`
- Base branch: `codex/analytics-foundation`
- Working branch: `codex/internal-boundary-workflow-vocabulary`
- Risk tier: Medium

Observed source status during this Codex B pass:

```text
issue #221 -> OPEN
issue #218 -> CLOSED
ADR-0006 -> Status: Accepted
branch -> codex/internal-boundary-workflow-vocabulary
base commit -> dc4f8c2 Add Python tooling inventory (#220)
```

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/templates/problem_representation.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/workflow_handoff.md`
- `docs/project_roadmap.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/internal_project_map.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/contracts/internal_project_boundary_annotation_organization.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- recent issue and PR title examples from GitHub

## Owning Layer

Primary owner: Quality / Governance.

This contract is a workflow and template vocabulary contract. It does not own
parser truth, analytics truth, workbook truth, deployment readiness, AI truth,
or protected-surface authorization.

## Files Owned By This Contract

This Codex B pass may create or edit only:

- `docs/contracts/internal_project_boundary_workflow_vocabulary.md`

Future Codex C implementation for issue #221 may edit:

- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/workflow_handoff.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md`

Future Codex C may edit these only if the comparison finds a precise wording
gap that cannot be fixed in the templates above:

- `docs/codex_module_workflow.md`
- `docs/internal_project_map.md`

Optional edits to `docs/codex_module_workflow.md` or `docs/internal_project_map.md`
must be short cross-reference notes. They must not introduce new gates,
change role authority, change branch policy, change ADR policy, or redefine the
accepted internal project map.

Future Codex E contract-test or review for issue #221 may create or edit:

- `docs/contract_test_reports/internal_project_boundary_workflow_vocabulary.md`

This contract does not authorize edits to:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/*.md`
- `docs/decisions/*.md`
- `README.md`
- source files under `src/`
- frontend files under `frontend/`
- tools under `tools/`
- tests under `tests/`
- fixtures, snapshots, generated files, runtime artifacts, or local-only
  artifacts

If those files appear necessary, stop and route back to Codex B or the user.

## Public Interface

The public interface is documentation vocabulary used by future workflow
artifacts:

- problem representations;
- module contracts;
- implementation handoffs;
- contract-test reports;
- workflow handoffs;
- GitHub issue template fields;
- PR template metadata;
- issue title prefixes;
- PR title prefixes;
- pasteable next-thread prompts.

The vocabulary must help humans and Codex threads answer:

- Which internal project area owns this work?
- Which layer owns truth?
- Is this bridge code?
- Which protected surfaces are in scope or explicitly out of scope?
- Which downstream surfaces consume the output?
- Which title prefix should future work use?

## Observed Current Behavior

- `docs/internal_project_map.md` defines the accepted internal project
  vocabulary and maps current path families.
- `docs/internal_project_map.md` asks whether `.github` issue and PR templates
  should learn the accepted internal project vocabulary.
- `.github/ISSUE_TEMPLATE/module_workflow.yml` has a `Primary project layer`
  dropdown with older pipeline-layer choices such as `webhook / transport
  layer`, `workbook landing sheets`, `helper formulas`, `dashboard / reporting
  tabs`, and `AI analysis`.
- `docs/templates/problem_representation.md` asks for `Project Layer`, but not
  for `Internal Project Area`.
- `docs/templates/module_contract.md` asks for `Owning Layer`, but not
  explicitly for internal project area, truth owner, or bridge-code status.
- `docs/templates/implementation_handoff.md` does not ask for internal project
  area or bridge-code status.
- `docs/templates/contract_test_report.md` does not ask reviewers to confirm
  internal project area or bridge-code classification.
- `docs/templates/workflow_handoff.md` defines a compact handoff shape without
  optional internal project vocabulary fields.
- `.github/pull_request_template.md` has a useful `Layer Ownership` section,
  but does not explicitly name internal project area, truth owner, or
  bridge-code classification.
- Recent issue titles already use several prefixes, including
  `[architecture]`, `[analytics]`, `[analytics/app]`, `[workflow]`,
  `[governance]`, and `[parser-resilience]`.

This is not a runtime bug. The gap is workflow consistency and routing clarity.

## Required Vocabulary

The canonical internal project area values are:

- `Parser`
- `Corpus / Provenance`
- `Analytics`
- `Local App / UI`
- `Workbook / Transport`
- `Quality / Governance`
- `Future AI Integration`
- `Shared Support`
- `Generated / Local Artifacts`
- `External / Collaboration Surface`

Template text may use `N/A` or `unclear` for work that does not fit neatly yet,
but final contracts and reviews should prefer one of the canonical values or
explicitly explain why classification is ambiguous.

## Required Guarantees

### Keep Project Layer And Internal Project Area Separate

Problem representations and issue templates must keep the older pipeline
concept when it is useful, but add internal project area as a separate concept.

Reason:

- `Project Layer` describes where data or workflow behavior sits in the
  pipeline, such as raw log source, parser/state interpretation, workbook
  transport, dashboard display, AI analysis, or repository workflow.
- `Internal Project Area` describes ownership and routing under ADR-0006 and
  `docs/internal_project_map.md`, such as Parser, Analytics, Local App / UI, or
  Quality / Governance.

Do not replace every `Project Layer` reference with `Internal Project Area`.
They answer different questions.

### Template Field Decisions

Future Codex C should make these docs/template decisions:

- `docs/templates/problem_representation.md`
  - Keep `## Project Layer`.
  - Add `## Internal Project Area`.
  - Add short guidance to choose from the canonical internal project vocabulary.
  - Add a note that bridge-code work should name both source and consuming
    project areas.

- `.github/ISSUE_TEMPLATE/module_workflow.yml`
  - Keep the existing `Primary project layer` field.
  - Add a separate optional `Internal project area` field.
  - Do not make the new field a hard blocker for issue creation.
  - Include canonical values plus `N/A / unclear`.
  - Mention `docs/internal_project_map.md` in the field description.

- `docs/templates/module_contract.md`
  - Keep `## Owning Layer`.
  - Add `## Internal Project Area`.
  - Add `## Truth Owner`.
  - Add `## Bridge-Code Status`.
  - Bridge-code status options should be:
    - `not_bridge_code`
    - `bridge_code`
    - `shared_support`
    - `ambiguous_pending_follow_up`
    - `deferred_future_boundary`

- `docs/templates/implementation_handoff.md`
  - Add fields for internal project area and bridge-code status.
  - Ask implementers to state whether the implementation stayed inside the
    contracted internal project area.

- `docs/templates/contract_test_report.md`
  - Add fields for internal project area and bridge-code status reviewed.
  - Ask reviewers to flag mismatches between the issue, contract, handoff, PR,
    and `docs/internal_project_map.md`.
  - Do not create a new lifecycle category for internal project mismatches;
    use the existing finding lifecycle table.

- `docs/templates/workflow_handoff.md`
  - Add optional machine-readable keys:
    - `internal_project_area`
    - `truth_owner`
    - `bridge_code_status`
  - Mark them optional so older handoffs remain valid.

- `.github/pull_request_template.md`
  - Update `Layer Ownership` to ask for:
    - internal project area;
    - truth owner;
    - bridge-code status;
    - downstream consumers touched.
  - Preserve the drift budget and protected-surface sections.
  - Do not turn vocabulary fields into merge-readiness authority.

### Issue Title Prefix Guidance

The contract chooses these preferred future title prefixes:

| Internal project area | Preferred prefix | Notes |
| --- | --- | --- |
| Parser | `[parser]` | Parser modules, parser state, router, event shape, parser-owned facts. |
| Corpus / Provenance | `[corpus/provenance]` | Evidence ledger, golden fixtures, drift baselines, replay evidence, feature-equity corpus. |
| Analytics | `[analytics]` | SQLite schema, migrations, ingest, deterministic views, analytics reports. |
| Local App / UI | `[local-app]` | Local backend/UI setup, launcher, import screens, local orchestration outside a specific analytics umbrella. |
| Workbook / Transport | `[workbook/transport]` | Sheet schemas, webhook payloads, Apps Script parity, workbook-facing rows. |
| Quality / Governance | `[quality]` or `[governance]` | Use `[quality]` for checks/tooling/validation. Use `[governance]` for rules, ADRs, templates, and workflow policy. |
| Architecture / boundary hygiene | `[architecture]` | Boundary maps, repository structure policy, architecture docs. |
| Future AI Integration | `[ai]` | Deferred/future only; does not authorize OpenAI or model-provider runtime integration. |
| Shared Support | Prefer the primary consumer prefix | Name bridge/shared-support status in body instead of using `[shared]` by itself. |
| Generated / Local Artifacts | Prefer the governing project prefix | Name artifact status in body. Do not imply generated/private artifacts may be committed. |
| External / Collaboration Surface | `[external-integration]` or `[governance]` | Use `[external-integration]` for tool/collaboration surface policy, `[governance]` for rules. |

Compatibility notes:

- Existing issues do not need to be renamed.
- `[analytics/app]` remains acceptable for the current analytics local-app
  umbrella, especially issues under #207 or #204 that already use that prefix.
- Future app-agnostic Local App / UI work should prefer `[local-app]`.
- Existing `[parser-resilience]` issues may remain as historical tracker
  language. New evidence-ledger/corpus work should prefer
  `[corpus/provenance]` when the work is primarily provenance, fixture, drift,
  or ledger evidence rather than parser behavior.
- `[provenance]` may be used as a readability shorthand only when the issue
  body explicitly names `Corpus / Provenance` as the internal project area.
- Do not use `[bridge]` alone. Use the primary owner prefix and describe bridge
  status in the issue body, contract, or PR metadata.

Example bridge-code titles:

- `[analytics] Legacy JSONL artifact adapter bridge`
- `[workbook/transport] Apps Script parity bridge`
- `[local-app] Setup status bridge for parser runtime health`
- `[quality] Protected-surface checker report bridge`

### Bridge-Code Classification

Bridge-code classification must remain descriptive. It does not authorize
changes outside the current issue and contract.

Required bridge-code fields in templates where relevant:

- source internal project area;
- consuming internal project area;
- truth owner;
- allowed data flow;
- forbidden reverse-flow;
- protected surfaces touched or explicitly not touched.

Bridge-code work must not move truth downstream. For example:

- analytics may ingest parser-normalized facts, but may not reinterpret raw logs
  as parser truth;
- Local App / UI may display setup or import state, but may not own parser truth
  or analytics truth;
- Workbook / Transport may receive parser-normalized rows, but may not feed
  workbook formulas or Apps Script state back into parser truth;
- Future AI Integration may explain or propose hypotheses only under a later
  scoped issue and contract.

### Future AI Integration Language

Future AI Integration may appear in vocabulary lists as a deferred internal
project area.

Template text must say that this vocabulary does not authorize:

- OpenAI API runtime integration;
- model-provider runtime integration;
- AI coaching evaluation;
- AI-owned parser truth;
- AI-owned analytics truth;
- hidden-card truth;
- gameplay correctness truth;
- strategic certainty.

### Not A Hard Gate

This issue should make good routing the default, not add process friction.

The new fields should be lightweight and mostly optional where strictness would
block issue creation or old handoffs. Reviewers may flag missing or inconsistent
internal project vocabulary as a finding when it creates real scope, truth, or
protected-surface ambiguity.

Do not add CI gates, required automation, import enforcement, or merge blockers
for vocabulary alone in issue #221.

## Inputs

Primary inputs:

- issue #221 problem representation;
- accepted ADR-0006;
- `docs/internal_project_map.md`;
- current workflow and artifact templates;
- current GitHub issue and PR templates;
- recent issue and PR title examples.

## Outputs

Codex B output:

- `docs/contracts/internal_project_boundary_workflow_vocabulary.md`

Expected Codex C outputs:

- template and PR/issue-template wording updates allowed by this contract;
- `docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md`

Expected Codex E output:

- `docs/contract_test_reports/internal_project_boundary_workflow_vocabulary.md`

## Invariants

- ADR-0006 remains accepted and is not amended by this issue.
- `docs/internal_project_map.md` remains the primary map for internal project
  ownership.
- Workflow vocabulary does not authorize protected-surface changes.
- Templates must not imply that internal project vocabulary outranks current
  user instructions, governing docs, accepted ADRs, current issues, or current
  contracts.
- Existing issue titles, PR titles, handoffs, reports, and contracts do not
  need mass renaming.
- Bridge-code status is descriptive unless a current issue and contract
  authorize concrete behavior changes.

## Error Behavior

If Codex C finds a conflict between this contract and accepted ADR-0006,
`docs/internal_project_map.md`, or a higher-priority governance doc, it must
stop and route back to Codex B.

If a template edit would require changing role authority or enforcement policy,
Codex C must stop and route to a new governance issue or Codex B.

If `.github/ISSUE_TEMPLATE/module_workflow.yml` cannot be validated after
editing, Codex C must treat that as blocking.

If a wording change appears to require runtime code, tests, tools, package
metadata, fixtures, snapshots, generated artifacts, or local-only artifacts,
Codex C must stop and report scope drift.

## Side Effects

Allowed side effects for future Codex C:

- Markdown template wording changes.
- GitHub issue template YAML wording/field changes.
- PR template wording changes.
- A docs-only implementation handoff.

Forbidden side effects:

- source code changes;
- test changes;
- tool behavior changes;
- package metadata changes;
- CI changes;
- runtime behavior changes;
- generated artifact changes;
- issue closure;
- PR creation;
- branch merge;
- production or external-system changes.

## Dependency Order

Future Codex C should update in this order:

1. Confirm branch and clean worktree.
2. Re-read issue #221, this contract, accepted ADR-0006, and
   `docs/internal_project_map.md`.
3. Compare current templates against the contract.
4. Update docs templates first.
5. Update `.github/ISSUE_TEMPLATE/module_workflow.yml`.
6. Update `.github/pull_request_template.md`.
7. Add only narrow cross-reference notes to `docs/codex_module_workflow.md` or
   `docs/internal_project_map.md` if the comparison proves they are needed.
8. Write the implementation comparison handoff.
9. Run validation.

## Compatibility

Compatibility requirements:

- Existing handoffs without `internal_project_area`, `truth_owner`, or
  `bridge_code_status` remain valid.
- Existing issues and PRs using `[analytics/app]`, `[parser-resilience]`,
  `[workflow]`, `[architecture]`, or other historical prefixes remain valid.
- Existing `Project Layer` language remains meaningful and must not be erased
  where it still describes pipeline or workflow position.
- Older contracts with only `Owning Layer` remain valid, but new templates
  should guide future contracts to name internal project area and truth owner
  explicitly.
- `workflow_handoff` blocks should accept the new keys as optional additions,
  not required schema.

## Tests Required

Codex B validation for this contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Future Codex C validation:

```powershell
git status --short --branch
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
docs/templates/problem_representation.md
docs/templates/module_contract.md
docs/templates/implementation_handoff.md
docs/templates/contract_test_report.md
docs/templates/workflow_handoff.md
.github/ISSUE_TEMPLATE/module_workflow.yml
.github/pull_request_template.md
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
docs/templates/problem_representation.md
docs/templates/module_contract.md
docs/templates/implementation_handoff.md
docs/templates/contract_test_report.md
docs/templates/workflow_handoff.md
.github/ISSUE_TEMPLATE/module_workflow.yml
.github/pull_request_template.md
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
git diff --name-only
```

If `.github/ISSUE_TEMPLATE/module_workflow.yml` changes, Codex C must also run
one focused YAML validation check. A valid option is:

```powershell
py -c "from pathlib import Path; import yaml; yaml.safe_load(Path('.github/ISSUE_TEMPLATE/module_workflow.yml').read_text())"
```

If the local environment lacks the YAML module, Codex C must say so and run an
equivalent available syntax or structure check instead of silently skipping the
issue-template validation.

Runtime tests are not required if the diff is docs/template-only and stays
inside the allowed files.

## Acceptance Criteria

Issue #221 implementation satisfies this contract when:

- problem representation template keeps `Project Layer` and adds
  `Internal Project Area`;
- module contract template names internal project area, truth owner, and
  bridge-code status;
- implementation handoff template carries internal project area and bridge-code
  status;
- contract-test report template asks reviewers to verify vocabulary alignment
  when relevant;
- workflow handoff template documents optional `internal_project_area`,
  `truth_owner`, and `bridge_code_status` keys;
- GitHub issue template keeps the existing project-layer field and adds a
  separate optional internal-project-area field;
- PR template asks for internal project area, truth owner, bridge-code status,
  and downstream consumers without adding merge authority;
- title prefix guidance is recorded in the implementation handoff or a touched
  approved template surface;
- no runtime files, tests, tools, package metadata, fixtures, snapshots,
  generated artifacts, or local-only artifacts changed;
- validation passes or failures are explained with next routing;
- protected surfaces remain untouched.

## Unknowns

- Whether future issue titles should eventually replace `[analytics/app]` with
  `[local-app]` everywhere is unresolved. This contract preserves existing
  `[analytics/app]` issue lineage and prefers `[local-app]` for future
  app-agnostic local UI/backend work.
- Whether future evidence-ledger work should use `[parser-resilience]` or
  `[corpus/provenance]` depends on tracker context. This contract does not
  rename historical issues.
- Whether `docs/codex_module_workflow.md` needs a cross-reference may depend on
  how much the templates alone clarify the workflow.
- Whether GitHub issue template fields should become required may be revisited
  only after evidence that optional fields are not enough.

## Suspected Gaps

- Current workflow templates do not consistently ask for internal project area.
- Current PR template has layer ownership language but not the newer ADR-0006
  vocabulary.
- Current GitHub issue template has older layer choices but no internal project
  area field.
- Handoff schema lacks optional internal project area, truth owner, and
  bridge-code status keys.
- Title prefixes are mostly conventional and issue-specific rather than mapped
  to the accepted internal project vocabulary.

## Protected Surfaces And Forbidden Changes

Do not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- parser event kind values;
- parser payload shapes;
- extractor behavior;
- match identity;
- game identity;
- deduplication;
- analytics behavior;
- SQLite schema or migrations;
- local app/backend behavior;
- frontend UI behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- CI gates;
- Pyright gate behavior;
- production behavior;
- AI/model-provider behavior;
- package name;
- imports;
- file layout.

Do not create, commit, expose, print, or modify:

- secrets;
- credentials;
- API keys;
- tokens;
- webhook URLs;
- environment variables;
- raw local logs;
- generated data;
- runtime status artifacts;
- transport failure payload artifacts;
- workbook exports;
- local JSONL artifacts;
- generated SQLite files;
- local-only artifacts.

## Stop Conditions

Stop and route back to Codex B or the user if:

- implementation would require changing files outside the allowed file list;
- `.github/ISSUE_TEMPLATE/module_workflow.yml` cannot be validated;
- a wording change would create a new hard gate or merge requirement;
- a wording change would alter Codex role authority;
- a wording change would amend ADR-0006 or the internal project map instead of
  referencing them;
- a protected surface would be touched;
- generated/private/local artifacts would be introduced;
- branch target or PR base is unclear during submitter/deployer work.

## Expected Codex C Handoff

Codex C should produce:

- docs/template/workflow vocabulary edits allowed by this contract;
- `docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md`.

Codex C should not stage, commit, push, open a PR, close issue #221, or target
`main` unless explicitly asked by the user in a later role.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #221.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/221

Branch:
codex/internal-boundary-workflow-vocabulary

Base branch:
codex/analytics-foundation

Contract:
docs/contracts/internal_project_boundary_workflow_vocabulary.md

Goal:
Implement the docs/template-only workflow vocabulary alignment authorized by the contract.

Before editing:
- Confirm the branch is codex/internal-boundary-workflow-vocabulary.
- Inspect git status and exclude unrelated changes.
- Read issue #221, the contract, accepted ADR-0006, docs/internal_project_map.md, and all templates named by the contract.
- State what the workflow vocabulary is supposed to do, what current templates actually do, what gaps remain, and the exact minimal docs/template plan.

Do:
- Keep Project Layer and add Internal Project Area where the contract requires both.
- Add internal project area, truth owner, and bridge-code status guidance to allowed templates.
- Add an optional internal-project-area field to .github/ISSUE_TEMPLATE/module_workflow.yml while keeping the existing project-layer field.
- Update .github/pull_request_template.md Layer Ownership to ask for internal project area, truth owner, bridge-code status, and downstream consumers.
- Preserve existing compatibility for old handoffs, historical issue prefixes, and current tracker naming.
- Produce docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md.

Do not:
- Edit AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/agent_threads/*.md, ADRs, README.md, source, frontend, tools, tests, fixtures, snapshots, package metadata, generated files, runtime artifacts, or local-only artifacts.
- Move files, rename packages, change imports, split repositories, add CI gates, enforce import boundaries, add a boundary checker, or make vocabulary fields merge-blocking gates.
- Change parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior.
- Touch secrets, raw logs, generated data, runtime status artifacts, transport failure payload artifacts, workbook exports, local JSONL artifacts, generated SQLite files, or local-only artifacts.
- Target main, stage, commit, push, open a PR, merge, or close issue #221 unless explicitly asked.

Validation:
git status --short --branch
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
docs/templates/problem_representation.md
docs/templates/module_contract.md
docs/templates/implementation_handoff.md
docs/templates/contract_test_report.md
docs/templates/workflow_handoff.md
.github/ISSUE_TEMPLATE/module_workflow.yml
.github/pull_request_template.md
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
docs/templates/problem_representation.md
docs/templates/module_contract.md
docs/templates/implementation_handoff.md
docs/templates/contract_test_report.md
docs/templates/workflow_handoff.md
.github/ISSUE_TEMPLATE/module_workflow.yml
.github/pull_request_template.md
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
git diff --name-only

If .github/ISSUE_TEMPLATE/module_workflow.yml changes, run a focused YAML validation check. If PyYAML is unavailable, report that and run an equivalent available syntax or structure check.

Final handoff must include:
- role performed
- issue reviewed
- contract used
- files changed
- vocabulary decisions implemented
- compatibility decisions
- forbidden scope status
- validation results
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/221"
  tracker: "N/A"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue problem representation for workflow vocabulary alignment"
  target_artifact: "docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md"
  contract_artifact: "docs/contracts/internal_project_boundary_workflow_vocabulary.md"
  risk_tier: "Medium"
  branch: "codex/internal-boundary-workflow-vocabulary"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface scan for contract"
    - "path-scoped secret/private-marker scan for contract"
  stop_conditions:
    - "Do not move files, rename packages, change imports, split repositories, add CI gates, enforce import boundaries, or make vocabulary fields merge-blocking gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior."
    - "Do not touch secrets, raw logs, generated data, runtime artifacts, workbook exports, local JSONL artifacts, generated SQLite files, or local-only artifacts."
```
