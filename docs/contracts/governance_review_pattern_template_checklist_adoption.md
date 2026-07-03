# Governance Review-Pattern Template Checklist Adoption Contract

## Module

`governance_review_pattern_template_checklist_adoption`

This contract defines how the review-pattern lessons captured in issue #649
may be adopted into Mythic Edge workflow templates and role checklists after
separate implementation review. It is a contract-first governance artifact for
issue #650. It does not edit templates, role docs, constitution text, ADRs, CI,
runtime code, or protected-surface gates by itself.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: https://github.com/Tahjali11/Mythic-Edge
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/650
- Source intake issue: https://github.com/Tahjali11/Mythic-Edge/issues/649
- Project roadmap / tracker: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Base branch: `main`
- Target branch: `main`
- Working branch used for this contract: `codex/governance-review-pattern-template-checklist-650`
- Target artifact:
  `docs/contracts/governance_review_pattern_template_checklist_adoption.md`
- Risk tier: High

## Owning Layer

Repository coordination and agent workflow.

## Internal Project Area

Quality / Governance.

## Truth Owner

Current repo governance docs, accepted ADRs, active GitHub issues, current
contracts, reviewed PRs, and deployer-recorded merge evidence own the truth for
this workflow guidance. Codex H intake comments, review comments, local skills,
memory, and stale prompts are evidence and routing inputs only.

This contract does not change parser truth, analytics truth, workbook truth,
webhook truth, Apps Script truth, AI truth, coaching truth, security assurance,
privacy assurance, release readiness, deploy readiness, or production
readiness.

## Bridge-Code Status

`not_bridge_code`

This is a governance contract. It does not bridge runtime project areas or move
data across parser, workbook, analytics, AI, or security boundaries.

## Authorization State

The following flags remain false for issue #650 and for this Codex B pass:

- `implementation_authorized: false`
- `constitution_edits_authorized: false`
- `agent_rules_edits_authorized: false`
- `adr_edits_authorized: false`
- `template_edits_authorized_in_codex_b: false`
- `role_doc_edits_authorized_in_codex_b: false`
- `ci_changes_authorized: false`
- `gate_activation_authorized: false`
- `protected_surface_enforcement_change_authorized: false`
- `parser_behavior_change_authorized: false`
- `workbook_schema_change_authorized: false`
- `webhook_shape_change_authorized: false`
- `apps_script_change_authorized: false`
- `openai_runtime_authorized: false`
- `analytics_behavior_change_authorized: false`
- `production_behavior_authorized: false`
- `readiness_claimed: false`
- `security_assurance_claimed: false`
- `privacy_assurance_claimed: false`

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md` by targeted governance search
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/workflow_handoff.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`
- `docs/decisions/ADR-0009-optional-dependency-provider-model.md`
- `docs/internal_project_map.md`
- GitHub issue #649
- GitHub issue #650

## Observed Current Behavior

Issue #649 captured five fresh review-pattern themes from the July 2-3 quality
loop:

1. Public-safe sanitization and no-echo standards.
2. Contract vocabulary and example coherence.
3. Authority and readiness gate semantics.
4. Fail-closed schema validation with cross-field checks.
5. Protected-surface enforcement rollout policy.

Issue #650 exists to translate those themes into a scoped adoption contract.
The issue explicitly rejects treating #649 or Codex H classification as direct
authority to edit constitution text, ADRs, role docs, templates, CI gates,
runtime behavior, or protected-surface enforcement.

Live repository authority records ADR-0008 as `Accepted` and ADR-0009 as
`Proposed`. ADR-0008 may be cited as accepted WIP-1 lane precedent. ADR-0009
may be inspected as context only and must not be treated as accepted precedent.

The main local checkout had unrelated governance edits. This contract was
written in a clean issue-scoped worktree so unrelated work stayed untouched.

## Problem Statement And First Bad Values

The intended behavior is that recurring review failures become usable workflow
guidance in the templates and role checklists that Codex roles actually read.

The first bad value is treating a Codex H intake comment or issue #649 as if it
directly authorizes governance edits. Codex H is advisory; adoption must route
through the normal A-G workflow.

The second bad value is leaving repeated failures conversational only. If
public-safe/no-echo rules, authority semantics, vocabulary coherence,
fail-closed validation expectations, and advisory enforcement boundaries do
not enter the right template/checklist surfaces, later threads can rediscover
the same problems.

The third bad value is over-adoption. A template checklist improvement must not
quietly become an ADR change, constitution change, CI gate, protected-surface
enforcement change, parser behavior change, or readiness claim.

## Scope Decision

This issue adopts a contract-first path:

- Codex B defines what later template or role-doc implementation may change.
- Codex B does not edit templates, role docs, constitution text, ADRs, CI, or
  runtime code.
- A later Codex C may implement only the contracted docs/template changes if a
  reviewed handoff routes that work.
- A later Codex E must review the contract before submitter work.

## Adoption Classification Vocabulary

Each #649 theme must use exactly one of these adoption labels:

- `template_adopt_now`: Safe to route to later template or role-checklist
  implementation after this contract is reviewed.
- `watch_list`: Preserve as an observation for later review, but do not route
  immediate template edits from this issue.
- `issue_local_only`: Keep the lesson inside issue-specific contracts,
  reviews, or PR bodies; do not generalize to workflow templates yet.
- `separate_ADR_or_constitution_issue_required`: Requires a dedicated issue and
  review path before any durable rule or authority-doc change.
- `reject_for_now`: Do not adopt from the current evidence.

## Theme Classification Table

| #649 theme | classification | adoption boundary | later candidate surfaces |
| --- | --- | --- | --- |
| Public-safe sanitization and no-echo standards | `template_adopt_now` | Adopt checklist language that requires public-safe scans and forbids echoing private markers. Do not create new secret tooling, CI gates, or publication authority. | `docs/templates/module_contract.md`, `docs/templates/contract_test_report.md`, `docs/templates/implementation_handoff.md`, `docs/templates/workflow_handoff.md`, `docs/agent_threads/module_contract.md`, `docs/agent_threads/contract_test.md`, `docs/agent_threads/review.md`, `docs/agent_threads/module_submitter.md`, `docs/agent_threads/integration_deployer.md` |
| Contract vocabulary and example coherence | `template_adopt_now` | Adopt checklist language requiring enums, examples, blocker codes, non-claim lists, and downstream validator expectations to agree. Do not require broad ADR or constitution changes from this issue. | `docs/templates/module_contract.md`, `docs/templates/contract_test_report.md`, `docs/templates/implementation_handoff.md`, `docs/agent_threads/module_contract.md`, `docs/agent_threads/contract_test.md`, `docs/agent_threads/review.md` |
| Authority and readiness gate semantics | `template_adopt_now` | Adopt "necessary but not sufficient" checklist language for validator, preflight, report-only, review-ready, and approval-gate states. Do not authorize writes, artifact creation, source action, gate activation, or readiness claims by checklist success. | `docs/templates/problem_representation.md`, `docs/templates/module_contract.md`, `docs/templates/workflow_handoff.md`, `docs/templates/implementation_handoff.md`, `docs/agent_threads/problem_representation.md`, `docs/agent_threads/module_contract.md`, `docs/agent_threads/review.md`, `docs/agent_threads/module_submitter.md`, `docs/agent_threads/integration_deployer.md` |
| Fail-closed schema validation with cross-field checks | `template_adopt_now` | Adopt checklist language requiring unknown-key, type, boolean-authority, expiration, and cross-field consistency checks when a contract defines schemas or validators. Do not implement validators in this issue. | `docs/templates/module_contract.md`, `docs/templates/contract_test_report.md`, `docs/templates/implementation_handoff.md`, `docs/agent_threads/module_contract.md`, `docs/agent_threads/contract_test.md`, `docs/agent_threads/review.md` |
| Protected-surface enforcement rollout policy | `template_adopt_now` | Adopt advisory rollout checklist language only: coverage floors, Ruff candidates, and security-quality gates require current-base evidence and separate issues/contracts before enforcement. Do not activate enforcement or change thresholds. | `docs/templates/problem_representation.md`, `docs/templates/module_contract.md`, `docs/templates/contract_test_report.md`, `docs/templates/workflow_handoff.md`, `docs/agent_threads/problem_representation.md`, `docs/agent_threads/module_contract.md`, `docs/agent_threads/contract_test.md`, `docs/agent_threads/review.md`, `docs/agent_threads/integration_deployer.md` |

## Explicit Non-Adoption Surfaces

This issue must not edit or route direct edits to these surfaces unless a later
issue explicitly authorizes them:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/decisions/*.md`
- `.github/workflows/*`
- runtime code under `src/`, `tools/`, `frontend/`, or `tests/`
- parser fixtures, corpus metadata, private evidence artifacts, or generated
  reports

`docs/agent_threads/constitutional_lawyer.md` is a watch-list surface for
future governance synthesis only. This contract does not change Codex H
authority or create a new constitutional amendment path.

## Required Checklist Content For Later Implementation

### Public-Safe Sanitization And No-Echo

Later template/checklist edits should require authors and reviewers to check
that public artifacts do not include:

- local absolute paths or machine-specific path roots
- URI-shaped private markers such as local file shares or local file schemes
- raw Player.log or UTC_Log lines
- raw private reports, raw diffs, source snippets, private counts, private
  offsets, private timestamps, or private filenames when the contract requires
  symbolic or bucketed reporting
- secrets, credentials, API keys, tokens, webhook URLs, workbook IDs, provider
  outputs, or model outputs
- exact private validation data, private decklists, screenshots, app-data
  paths, or local-only runtime artifacts

When a field is unsafe to publish, the allowed template response should be a
symbolic category, redacted placeholder, bucketed value, or fail-closed
rejection. Templates should avoid instructing Codex to paste the unsafe source
value back into the public artifact.

### Contract Vocabulary And Example Coherence

Later template/checklist edits should require:

- every status, enum, blocker code, refusal code, readiness state, route label,
  and non-claim label to be defined before examples use it
- examples to use only allowed values from the same contract
- blocker requirements to have matching closed vocabulary entries
- non-claim lists to stay consistent across related contracts when a chain uses
  shared vocabulary
- downstream validator or consumer expectations to be named when a contract
  defines an artifact shape

If a later role cannot reconcile examples with vocabulary, the expected route
is Codex B contract clarification, not silent implementation.

### Authority And Readiness Gate Semantics

Later template/checklist edits should state that these statuses are necessary
evidence only, not sufficient authority:

- validator success
- preflight success
- dry-run success
- report-only success
- review-ready status
- advisory route status
- no-blocking-finding review status
- existence of an issue, contract, handoff, local artifact, or source packet

Those statuses must not be used by themselves to authorize:

- writing durable artifacts
- creating claims, findings, candidate dossiers, issues, PRs, comments,
  reviews, labels, branches, commits, or status checks
- source-repo inspection or mutation
- CI gate activation
- protected-surface enforcement
- parser behavior changes
- fixture promotion or corpus status changes
- release, deploy, production, security, privacy, parser, analytics, AI, or
  coaching readiness claims

Templates should prefer explicit language such as "passes prerequisite checks"
or "eligible for later review" over "approved", "ready", or "cleared" unless
the current issue and role truly authorize that stronger state.

### Fail-Closed Schema Validation With Cross-Field Checks

Later template/checklist edits should require contracts that define schema-like
artifacts or validators to name:

- required fields
- optional fields
- forbidden fields or unknown-key behavior
- field types, including arrays, objects, booleans, strings, and enums
- authority flags that must remain booleans and must not pass as strings
- expiration semantics, including stale, expired, revoked, superseded, and
  mismatched authority states when relevant
- cross-field dependencies, such as operation matching target path, issue,
  artifact family, repository, source context, or authorization source
- downstream compatibility expectations when one artifact feeds another
  validator, preflight, or handoff

The default malformed-input behavior is fail-closed:

- reject the package
- preserve a public-safe reason category
- avoid echoing private source values
- route to Codex B for contract clarification or Codex D/C only when the fix is
  concrete and authorized

### Protected-Surface Enforcement Rollout Policy

Later template/checklist edits should preserve the distinction between:

- measurement
- advisory baseline
- candidate selection
- report-only gate
- blocking enforcement

Coverage floors, Ruff rule promotion, and security-quality gates require fresh
current-base evidence and separate issue/contract authorization before any
threshold, fail-under value, CI rule, or blocking gate changes. A successful
measurement or advisory report does not authorize enforcement.

Protected-surface rollout language should also require exact scope:

- exact coverage surface or threshold candidate
- exact Ruff code or rule family
- exact security-quality gate family
- exact protected surface touched or explicitly not touched
- exact validation evidence required before promotion

## ADR Policy

ADR-0008 is accepted and may be cited for WIP-1 lane activation and active-slot
coordination.

ADR-0009 is proposed and non-precedential. It may be read as context, but
issue #650 must not rely on it as accepted authority.

This contract does not create ADR-0010, reserve an ADR number, change ADR
status, amend accepted ADRs, or require a new ADR. If later review concludes a
theme needs durable authority beyond templates/checklists, route that request
to a separate Codex A/B issue.

## Public Interface

This contract defines a future docs/template implementation interface, not a
runtime interface.

Future roles may depend on these contract outputs:

- the five-theme classification table
- the allowed adoption label vocabulary
- the candidate template and role-doc surfaces
- the explicit non-adoption surfaces
- the required checklist content categories
- the validation expectations for later docs implementation
- the non-claim and stop-condition vocabulary

## Inputs

Allowed inputs for later implementation:

- issue #650
- issue #649 and its Codex H review-pattern intake comment
- tracker #568 as roadmap context
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/*.md`
- `docs/templates/*.md`
- `docs/decisions/README.md`
- accepted ADRs
- proposed ADRs only as explicitly labeled non-precedential context
- reviewed PRs and review artifacts cited by #649 when used as evidence

Forbidden inputs:

- private logs, private screenshots, private reports, local-only runtime
  artifacts, raw workbook exports, secrets, credentials, API keys, tokens, or
  webhook URLs
- unreviewed local worktree state as authority
- proposed ADR-0009 as accepted precedent
- sibling-repo mutation evidence unless a repo-scoped handoff authorizes it
- source snippets, raw diffs, or private paths copied from unrelated local
  checkouts

## Outputs

The only output of this Codex B pass is this contract artifact.

A later Codex C, if separately routed after review, may produce a focused docs
implementation that edits only the contracted template or role-checklist
surfaces. That later implementation must not edit constitution text, ADRs,
agent rules, CI, runtime code, parser behavior, or protected-surface
enforcement unless a separate issue explicitly authorizes those surfaces.

## Invariants

- Codex H remains advisory until adoption routes through normal A-G workflow.
- Template checklist success is not write authority.
- Validator or preflight success is necessary evidence only, not sufficient
  approval for creation, mutation, activation, or readiness claims.
- Proposed ADRs are not accepted precedent.
- Public artifacts must not echo unsafe private source values.
- Protected-surface enforcement requires separate authorization.
- Parser truth ownership is unchanged.
- Issue #568 remains the roadmap/tracker context and is not closed by this
  contract.

## Error Behavior

If later implementation discovers a target template or role doc already
contains conflicting guidance, route to Codex B for contract clarification.

If later implementation would require constitution, ADR, agent-rules, CI, or
runtime changes, stop and route to a separate issue or Codex A/B framing pass.

If a public-safe checklist would require naming a private source value, do not
echo the value. Use a symbolic reason category or fail-closed rejection.

If ADR-0009 becomes accepted before implementation starts, later roles may cite
that updated state only after verifying live repo state. This contract records
the state observed during issue #650 Codex B work, not a permanent statement
about future ADR status.

## Side Effects

This Codex B contract writes one file:

- `docs/contracts/governance_review_pattern_template_checklist_adoption.md`

It does not:

- edit templates
- edit role docs
- edit constitution text
- edit agent rules
- edit ADRs
- edit CI
- open, close, label, or update GitHub issues
- open or update PRs
- stage, commit, push, or merge
- change runtime code or parser behavior
- activate protected-surface enforcement

## Dependency Order For Later Work

If separately authorized, later adoption should proceed in this order:

1. Codex E reviews this contract against issue #650 and issue #649.
2. Codex C implements focused docs/template changes only after review clears
   this contract.
3. Codex E performs contract-test review of the docs/template diff.
4. Codex F submits a draft PR only if Codex E has no blocking findings.
5. Codex G considers merge/closeout only after explicit user deployer
   authorization and normal merge gates.

## Compatibility

Existing templates and role docs remain valid until a later implementation PR
changes them. Older handoffs without the new checklist language remain
historical artifacts and should be interpreted under the rules active when they
were written, plus current repo safety rules for any resumed work.

## Validation Required For Later Implementation

For this contract:

```bash
git diff --check
printf '%s\n' docs/contracts/governance_review_pattern_template_checklist_adoption.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_agent_docs.py
```

For later docs/template implementation, if separately routed:

```bash
git diff --check
printf '%s\n' <changed-docs> | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_agent_docs.py
```

Later review should also run a focused public-safe scan for:

- local absolute paths
- local file/share URI markers
- raw logs
- secrets, credentials, API keys, tokens, and webhook URLs
- private report values, exact private counts, private filenames, private
  offsets, private timestamps, source snippets, and raw diffs
- unauthorized `*_authorized: true` or `*_claimed: true` flag flips

## Acceptance Criteria

- This contract exists at
  `docs/contracts/governance_review_pattern_template_checklist_adoption.md`.
- Each #649 theme is classified with exactly one adoption label.
- The contract names candidate template/checklist surfaces for later
  implementation.
- The contract names explicit non-adoption surfaces.
- The contract preserves ADR-0008 as accepted and ADR-0009 as proposed
  non-precedential context.
- The contract does not authorize template edits, constitution edits, ADR
  edits, CI changes, code changes, gate activation, protected-surface
  enforcement, parser behavior changes, or readiness/truth/assurance claims.
- Validation expectations are clear for later Codex C/E work.

## Remaining Risks

- Some #649 evidence came from sibling repositories. This contract uses that
  evidence as review-pattern input only; it does not authorize sibling-repo
  edits.
- Template/checklist edits can accumulate ceremony. Later implementation should
  keep wording compact and role-specific rather than duplicating every checklist
  into every file.
- If future constitutional synthesis under #568 wants to elevate one of these
  themes beyond templates, it should create a separate issue or ADR path.

## Next Workflow Action

Next recommended role: Codex E contract review.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer / Contract Tester for issue #650.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/650

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/649

Contract under review:
docs/contracts/governance_review_pattern_template_checklist_adoption.md

Review goal:
Verify that the contract correctly classifies each #649 review-pattern theme,
keeps adoption limited to future template/checklist work, preserves ADR-0008
accepted status and ADR-0009 proposed/non-precedential status, and does not
authorize constitution edits, ADR edits, template edits in Codex B, CI changes,
gate activation, protected-surface enforcement, parser behavior changes, or
readiness/security/privacy/truth claims.

Protected boundaries:
Do not implement code. Do not edit templates, role docs, constitution, agent
rules, ADRs, CI, runtime code, or protected-surface enforcement. Do not stage,
commit, push, open a PR, close issues, or claim readiness/security/privacy
assurance.

Expected output:
Findings first, validation checked, recommendation, next role, and
workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/650"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/649"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #649 Codex H review-pattern intake"
  target_artifact: "docs/contracts/governance_review_pattern_template_checklist_adoption.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/governance-review-pattern-template-checklist-650"
  internal_project_area: "Quality / Governance"
  truth_owner: "repository coordination and agent workflow"
  bridge_code_status: "not_bridge_code"
  implementation_authorized: false
  constitution_edits_authorized: false
  agent_rules_edits_authorized: false
  adr_edits_authorized: false
  template_edits_authorized_in_codex_b: false
  role_doc_edits_authorized_in_codex_b: false
  ci_changes_authorized: false
  gate_activation_authorized: false
  protected_surface_enforcement_change_authorized: false
  parser_behavior_change_authorized: false
  readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  validation:
    - "git diff --check"
    - "printf '%s\n' docs/contracts/governance_review_pattern_template_checklist_adoption.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not edit constitution, ADRs, templates, role docs, or agent rules in Codex B."
    - "Do not activate CI gates or protected-surface enforcement."
    - "Do not treat proposed ADR-0009 as accepted precedent."
    - "Do not claim readiness, security assurance, privacy assurance, parser truth, analytics truth, AI truth, coaching truth, release readiness, deploy readiness, or production readiness."
```
