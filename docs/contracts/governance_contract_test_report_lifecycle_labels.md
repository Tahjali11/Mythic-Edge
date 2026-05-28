# Governance Contract-Test Report Lifecycle Labels Contract

## Module

Governance documentation for contract-test report lifecycle labels.

## Source Issue

Proposed follow-up issue: `[governance] Add contract-test report lifecycle labels`.

Source context: Codex H review of archived v2 constitution drafts.

## Tracker

N/A.

## Owning Layer

Mythic Edge workflow governance owns this contract. This contract does not own
parser behavior, runtime behavior, workbook behavior, webhook behavior, Apps
Script behavior, production behavior, or data interpretation.

## Files Owned By This Contract

This contract authorizes a later implementation/comparison pass to evaluate and
edit only:

- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

The later pass may create a comparison or implementation handoff under
`docs/implementation_handoffs/`.

The later pass must not edit `AGENTS.md`, `docs/agent_constitution.md`,
`docs/agent_rules.yml`, `docs/codex_module_workflow.md`,
`docs/agent_threads/review.md`, or ADRs unless a follow-up contract explicitly
authorizes those surfaces.

## Public Interface

The public interface is the durable shape of Codex E contract-test reports under
`docs/contract_test_reports/` and the role guidance that tells Codex E how to
use that shape.

Future contract-test reports may depend on these labels when a module moves
through C -> E -> D -> E -> F loopbacks:

- `report_lifecycle`
- `finding_lifecycle`
- `finding_id`
- `finding_status`
- `blocking_status`
- `verification_evidence`
- `next_route`

These are documentation/reporting labels only. They are not programmatic CI
gates unless a future contract separately authorizes tooling.

## Observed Current Behavior

`docs/agent_threads/contract_test.md` currently requires Codex E to verify an
implementation against a contract, list confirmed matches, contract mismatches,
missing tests, drift classification, recommendations, and a workflow handoff.

`docs/templates/contract_test_report.md` currently has sections for results,
confirmed contract matches, contract mismatches, missing tests, drift notes, and
a recommendation of approve, request implementation fix, request contract
clarification, or split follow-up issue.

The current active template does not provide explicit labels for:

- original findings from the first contract-test pass
- fixed-state follow-up findings after Codex D or C changes
- superseded findings after contract or scope clarification
- remaining blockers after a follow-up pass
- final approval after D/E loopbacks

Archived Codex D and Codex E v2 drafts described this lifecycle more clearly:
original findings should be preserved, fixed-state follow-ups should be labeled,
and a report should not imply a finding is fixed until focused validation,
documentation, and implementation behavior agree.

## Target Problem

After D/E loopbacks, a contract-test report can become ambiguous. A next role may
not be able to tell whether a finding is:

- still an active blocker
- fixed and verified
- fixed but not yet independently verified
- superseded by a contract or scope change
- intentionally deferred to a follow-up issue
- part of a final approval state

This creates issue lifecycle drift and review handoff risk. The risk is
governance confusion, not parser behavior.

## Required Guarantees

### Report Lifecycle Labels

The later implementation pass must add a compact report-level label set to
`docs/agent_threads/contract_test.md` and
`docs/templates/contract_test_report.md`.

Required `report_lifecycle` values:

- `initial_contract_test`: first Codex E contract-test report for a package.
- `followup_after_fixer`: Codex E follow-up after Codex D or Codex C changes.
- `contract_clarification_review`: Codex E follow-up after Codex B clarifies or
  amends the contract.
- `final_approval`: Codex E report state where no blocking findings remain and
  the next route may be Codex F or `none`, depending on the workflow.

The template must make clear that `final_approval` is not allowed when any
`remaining_blocker` finding exists.

### Finding Lifecycle Labels

The later implementation pass must add a compact finding-level label set.

Required `finding_lifecycle` values:

- `original_finding`: finding first recorded in the initial contract-test or
  review pass.
- `fixed_state_followup`: later status update for a previously recorded
  finding after a fix attempt.
- `superseded`: finding no longer applies because the contract, scope, or
  source artifact changed.
- `remaining_blocker`: finding still blocks Codex F/G submission or closure.
- `remaining_non_blocking`: finding or risk remains, but does not block the
  next workflow role.
- `deferred_followup`: finding is explicitly routed to a separate issue or later
  contract instead of blocking the current package.

The template may include `not_reproduced` as an optional label if the later
implementation pass decides it is useful, but it is not required by this
contract.

### Finding Status Fields

Each active or historical finding in a loopback-aware contract-test report must
be able to state:

- stable finding id, such as `P1`, `P2`, or `G1`
- severity or priority, when applicable
- `finding_lifecycle`
- current blocking status
- original evidence or source report
- current verification evidence
- next route: D, B, A, F, G, follow-up issue, or none

The implementation pass may choose a table, bullets, or a short structured
section, but the shape must be easy to paste into future reports.

### Preservation Rules

Contract-test report updates must preserve original evidence unless the original
wording is actively misleading. When wording is revised, the report must make
the lifecycle explicit instead of silently deleting the original finding.

Superseded findings must cite the superseding artifact or decision, such as a
revised contract, issue comment, or follow-up scope decision.

Fixed findings must not be labeled as fixed until Codex E has verification
evidence. A Codex D handoff may say a fix was attempted, but Codex E owns the
verified fixed-state label.

Remaining blockers must remain visible in the recommendation and
`workflow_handoff` routing.

### Final Approval Rules

A report may use `final_approval` only when:

- no `remaining_blocker` findings remain
- focused validation for the contracted surface passed or any skipped validation
  is explicitly justified
- contract, implementation, tests, and report no longer materially disagree
- remaining non-blocking risks are named and routed
- protected surfaces were not changed outside the contract

Final approval does not authorize merging to production, deploying Apps Script,
changing live workbook state, or closing a tracker unless the current workflow
role and user prompt separately authorize those actions.

## Unknowns

- Whether future reports should use a strict table or allow either tables or
  labeled bullets.
- Whether `not_reproduced` should be an official label or remain a free-text
  note.
- Whether `docs/agent_threads/review.md` should eventually mention the same
  labels for PR review mode. This contract intentionally leaves that out to keep
  the first change narrow.
- Whether historical reports should ever be backfilled. This contract does not
  require backfilling old reports.

## Suspected Gaps

- The active contract-test template can approve or request fixes, but does not
  show how to preserve original findings after D fixes them.
- The active role doc tells Codex E to report mismatches, but does not say how
  to mark fixed, superseded, or deferred findings.
- A submitter or integration thread can see an old blocking finding without a
  clear fixed-state label and may stop unnecessarily or route to the wrong role.
- A report can become stale after contract clarification because there is no
  standard `superseded` label.

## Protected Surfaces

This governance contract must not authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event classes
- event kind values
- parser payload shapes
- match or game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- live workbook state
- deployed Apps Script state
- runtime status files
- failed posts
- workbook exports
- secrets, credentials, environment variables, webhook URLs, or API keys
- raw private Player.log excerpts
- generated data
- CI gates
- production behavior

## Out Of Scope

- Implementing a new permanent Codex role.
- Promoting optional E2/adversarial review into a standing role.
- Making contract-test lifecycle labels machine-enforced.
- Rewriting the constitution.
- Rewriting `docs/agent_rules.yml`.
- Rewriting the overall A-G workflow.
- Backfilling every historical contract-test report.
- Creating or closing GitHub issues.
- Staging, committing, pushing, opening a PR, or merging.

## Validation Requirements

For this contract-writer pass:

```powershell
git status --short --branch
git diff --check
```

For the later Codex C implementation/comparison pass:

```powershell
git status --short --branch
git diff --check
py tools\check_agent_docs.py
@'
docs/agent_threads/contract_test.md
docs/templates/contract_test_report.md
docs/implementation_handoffs/governance_contract_test_report_lifecycle_labels_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/constitution-feedback-round-2026-05-28 --paths-from-stdin
```

If `tools\check_agent_docs.py` is not present on the branch, Codex C must state
that and run the nearest available docs validation instead.

## Acceptance Criteria

- `docs/agent_threads/contract_test.md` defines the report-level and
  finding-level lifecycle labels.
- `docs/templates/contract_test_report.md` includes lightweight fields or
  sections for lifecycle labels.
- The updated template preserves the current required sections: checks run,
  confirmed matches, contract mismatches, missing tests, drift notes,
  recommendation, next workflow action, and `workflow_handoff`.
- The update explains that original findings must be preserved or explicitly
  marked superseded, not silently erased.
- The update explains that verified fixed-state labels belong to Codex E after
  validation.
- The update explains that final approval is invalid while remaining blockers
  exist.
- The change does not edit parser, runtime, workbook, webhook, Apps Script, CI
  gate, secret, generated-data, or production surfaces.
- Validation commands are run or explicitly blocked with reasons.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the governance issue:
[governance] Add contract-test report lifecycle labels.

Branch:
codex/constitution-feedback-round-2026-05-28

Source contract:
docs/contracts/governance_contract_test_report_lifecycle_labels.md

Goal:
Compare the active contract-test role doc and report template against the contract, then implement only the narrow docs/template changes needed to add lifecycle labels for original findings, fixed-state follow-ups, superseded findings, final approval, and remaining blockers after D/E loopbacks.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/agent_threads/review.md
- docs/templates/contract_test_report.md
- docs/templates/workflow_handoff.md
- docs/contracts/governance_contract_test_report_lifecycle_labels.md
- docs/archive/agent_constitution_v2_drafts/v2_constitution_codex_d.md
- docs/archive/agent_constitution_v2_drafts/v2_constitution_codex_e.md

Before editing:
- Confirm the branch is codex/constitution-feedback-round-2026-05-28.
- Inspect git status and exclude unrelated changes.
- State what the lifecycle labels are supposed to do, what the current docs already do, what gaps remain, and the exact minimal edit plan.

Do:
- Update docs/agent_threads/contract_test.md with the compact report_lifecycle and finding_lifecycle label guidance.
- Update docs/templates/contract_test_report.md with lightweight lifecycle fields or sections.
- Preserve the existing report sections and recommendation flow.
- Produce docs/implementation_handoffs/governance_contract_test_report_lifecycle_labels_comparison.md with files inspected, matches, gaps closed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Rewrite the constitution.
- Edit AGENTS.md, docs/agent_constitution.md, docs/agent_rules.yml, docs/codex_module_workflow.md, docs/agent_threads/review.md, or ADRs unless a follow-up contract authorizes it.
- Create a new permanent E2 role.
- Add CI gates or machine enforcement.
- Backfill old contract-test reports.
- Change parser behavior, runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or production behavior.
- Stage, commit, push, open a PR, merge, or close issues unless explicitly asked.

Validation:
git status --short --branch
git diff --check
py tools\check_agent_docs.py
@'
docs/agent_threads/contract_test.md
docs/templates/contract_test_report.md
docs/implementation_handoffs/governance_contract_test_report_lifecycle_labels_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/constitution-feedback-round-2026-05-28 --paths-from-stdin

Final handoff must include:
- role performed
- source contract used
- files changed
- exact docs/template sections changed
- lifecycle labels added
- validation run
- protected-surface status
- what remains unverified
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "proposed: [governance] Add contract-test report lifecycle labels"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "Codex A problem representation handoff from Codex H archived V2 constitution draft review"
  target_artifact: "docs/implementation_handoffs/governance_contract_test_report_lifecycle_labels_comparison.md"
  risk_tier: "Low-Medium"
  branch: "codex/constitution-feedback-round-2026-05-28"
  validation:
    - "git status --short --branch"
    - "git diff --check"
  stop_conditions:
    - "Do not edit authority docs beyond docs/agent_threads/contract_test.md and docs/templates/contract_test_report.md in Codex C."
    - "Do not rewrite the constitution or rules file from this contract."
    - "Do not promote E2 to a permanent role."
    - "Do not add CI gates or machine enforcement."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
    - "Do not stage, commit, push, open a PR, merge, or close issues unless explicitly asked."
```
