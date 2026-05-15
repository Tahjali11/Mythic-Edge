# Code Hardening Independent Test-Authoring Policy Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/72

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Contract:
`docs/contracts/code_hardening_independent_test_authoring_policy.md`

Branch target: `codex/code-hardening-suite`

Role performed: Codex C: Module Implementer / comparison thread.

This pass compared the current workflow docs, agent rules, templates, PR
template, ADRs, and hardening contracts against the independent test-authoring
policy contract. It intentionally did not implement the policy.

## Source Artifacts Used

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/module_submitter.md`
- `docs/templates/module_contract.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/workflow_handoff.md`
- `.github/pull_request_template.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/contracts/code_hardening_independent_test_authoring_policy.md`
- current hardening contracts under `docs/contracts/`
- current hardening implementation handoffs and contract-test reports under
  `docs/implementation_handoffs/` and `docs/contract_test_reports/`
- GitHub issue #72 and tracker #33

## What The Policy Is Supposed To Do

The independent test-authoring policy is supposed to prevent high-risk
implementation work from choosing tests only after a patch already exists.

For triggered high-risk work, the project should have independent test
identification, adversarial contract-test planning, or separately authorized
test authoring before Codex C starts implementation.

The policy should:

- preserve the existing Mythic Edge A/B/C/D/E/F/G workflow
- treat E2 as an optional Codex E mode, not a new permanent role
- define when Codex B's contract test inventory is enough
- define when a separate E2 adversarial pass should happen before Codex C
- make required tests and stop conditions visible before high-risk work starts
- avoid adding ceremony to low-risk edits
- preserve parser truth ownership and protected-surface rules

## What Current Docs Already Do

### Workflow And Risk Gates

Observed matches:

- `AGENTS.md` already says high-risk changes require a problem
  representation, module contract, implementation against the contract,
  independent review, and submitter handoff before PR submission.
- `docs/agent_constitution.md` already requires problem representation,
  module contract, implementation against contract, review or contract test,
  and validation evidence for high-risk work.
- `docs/agent_rules.yml` encodes the same high-risk gate as
  `implementation_against_contract`, `review_or_contract_test`, and
  `validation_evidence`.
- `docs/codex_module_workflow.md` already makes durable artifacts the shared
  memory between roles and says implementation should start from issue and
  contract.
- `docs/agent_threads/implementation.md` already says high-risk
  implementation needs a problem representation, module contract, and planned
  module review or contract testing before code changes.

Current limitation:

- These docs require review or contract testing, but they do not yet require
  independent test identification before implementation begins.

### Module Contract Writer

Observed matches:

- `docs/agent_threads/module_contract.md` requires Codex B to define owning
  truth layer, public interfaces, invariants, error behavior, side effects,
  dependency order, and tests.
- `docs/templates/module_contract.md` includes `Tests Required`,
  `Acceptance Criteria`, and workflow handoff sections.
- Most existing hardening contracts define validation commands, protected
  surfaces, acceptance criteria, and a Codex C handoff.

Current limitation:

- The current module-contract role does not explicitly state when a contract's
  test inventory is sufficient independent test identification versus when it
  must route to E2 before Codex C.

### Contract Test And Review

Observed matches:

- `docs/agent_threads/contract_test.md` is a specialized Codex E mode for
  checking implementation against a written contract.
- It is required for high-risk implementation and recommended for medium-risk
  implementation with interface or cross-layer effects.
- `docs/templates/contract_test_report.md` captures confirmed matches,
  mismatches, missing tests, drift notes, recommendation, and next workflow
  action.
- `docs/agent_threads/review.md` instructs higher-risk review to focus on
  truth ownership, interface contracts, workbook/deployment drift, secrets,
  and validation gaps.

Current limitation:

- Contract-test documentation is post-implementation oriented. It does not
  describe a pre-implementation E2 adversarial test planning pass.

### Implementation Thread

Observed matches:

- `docs/agent_threads/implementation.md` requires Codex C to inspect relevant
  files before editing, state intended behavior/current behavior/failure
  point/edit plan before significant edits, add or update focused tests, and
  preserve behavior outside the contract.
- The implementation handoff template has sections for tests, validation,
  still-unverified items, and reviewer focus.

Current limitation:

- Codex C is not yet told to stop specifically when triggered high-risk work
  lacks independent pre-implementation evidence.

### Submitter And Integration Readiness

Observed matches:

- `docs/agent_threads/module_submitter.md` requires upstream artifacts,
  review with no blocking findings, validation, scope inspection, and safe PR
  targeting before submission.
- `docs/agent_rules.yml` defines Codex G / Integration Deployer, merge gates,
  tracker hygiene, and deployer ownership of merge readiness.
- `docs/agent_rules.yml` says the merge owner is G and submitter may not
  merge.

Current limitation:

- Submitter and deployer rules do not yet mention missing independent
  evidence as a blocker for triggered high-risk work.

### PR Template

Observed matches:

- `.github/pull_request_template.md` asks for linked issue/contract, related
  ADRs, risk tier, layer ownership, drift budget, tests, contract
  verification, still-unverified items, and workflow handoff.
- The drift budget requires protected-surface authorization and residual-drift
  disclosure.
- Contract verification asks whether risk-tier requirements were followed and
  parser truth was not moved downstream.

Current limitation:

- The PR template does not explicitly ask whether triggered high-risk work had
  independent pre-implementation test identification, E2 evidence, or a
  contract section sufficient to satisfy the policy.

## Hardening Contract Comparison

### Contracts That Already Provide Strong Test Inventories

These existing contracts contain detailed validation sections that can satisfy
independent test identification for some medium/high-risk work when the
contract itself is concrete enough:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`

Observed pattern:

- They define owning layer, protected surfaces, required or recommended
  validation, out-of-scope behavior, acceptance criteria, and Codex C handoff.
- They consistently route implementation/comparison work to Codex E for
  contract-test review.
- They preserve parser truth ownership and do not treat tests or snapshots as
  automatic authorization for semantic change.

Gap:

- They do not label their test inventory as "independent test identification"
  because the policy did not exist yet.
- They do not consistently state whether E2 is mandatory, optional, or not
  needed before Codex C.

### E2 Presence

Observed:

- Tracker #33 names a recommended high-risk flow:
  `A -> B -> E/E2 -> C -> E -> F -> G`.
- Tracker #33 explicitly says E2 is an optional Codex E mode, not a permanent
  role.
- Issue #72 and the new policy contract define E2 more clearly.

Absent:

- `docs/agent_threads/contract_test.md` does not yet include
  pre-implementation E2 behavior.
- `docs/agent_rules.yml` does not yet encode E2.
- `docs/codex_module_workflow.md` does not yet document E2 in the normal or
  high-risk workflow.
- No dedicated E2 template exists.

Interpretation:

- E2 currently exists at tracker/issue/contract level, not in the durable
  active workflow docs.
- That is acceptable for this comparison pass because implementation was not
  authorized.

## Contract Matches

- The current repo already protects parser truth ownership through
  `AGENTS.md`, `docs/agent_constitution.md`, `docs/agent_rules.yml`, ADR-0001,
  and hardening contracts.
- The current repo already requires high-risk work to have problem
  representation, module contract, implementation against contract, review or
  contract testing, validation evidence, and submitter handoff.
- Existing hardening contracts already contain substantial validation
  inventories and protected-surface stop conditions.
- Existing review and contract-test rules already support finding missing
  tests and routing back to D, B, or A.
- Existing submitter/deployer rules already stop on missing artifacts,
  validation gaps, blocking review findings, forbidden files, or production
  target ambiguity.
- Existing PR drift budget already exposes protected-surface authorization and
  residual drift.
- Existing ADRs already state that protected-surface and schema changes need
  explicit issue, contract, review, and validation authority.

## Contract Gaps

These are comparison findings, not implementation changes made in this pass:

1. Pre-implementation independent evidence is not yet a formal gate in the
   active workflow docs.

2. E2 is not yet documented in `docs/agent_threads/contract_test.md` as a
   pre-implementation adversarial contract-test mode.

3. `docs/agent_rules.yml` does not yet encode E2 or the independent
   test-identification requirement.

4. `docs/codex_module_workflow.md` does not yet include the high-risk
   `A -> B -> E/E2 -> C -> E -> F -> G` route as durable workflow guidance.

5. `.github/pull_request_template.md` does not ask high-risk PRs to cite the
   independent evidence artifact or explain why Codex B's test inventory was
   sufficient.

6. `docs/templates/implementation_handoff.md` does not ask Codex C to record
   whether triggered high-risk work had required independent evidence before
   implementation.

7. `docs/templates/contract_test_report.md` can report missing tests after
   implementation, but it does not currently provide a pre-implementation E2
   checklist shape.

8. Existing hardening contracts generally list tests and validation, but do
   not classify E2 as mandatory, optional, or not needed.

## No Implementation Performed

Per the user instruction and contract boundaries, this pass did not:

- implement the policy
- edit workflow docs
- edit agent rules
- edit templates
- edit the PR template
- add tests
- add CI gates
- change parser behavior
- change parser state final reconciliation
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change parser event classes, event kind values, or parser payload shapes
- change match/game identity or deduplication
- touch fixtures, expected outputs, schema snapshots, drift baselines, secrets,
  raw logs, generated data, runtime status files, failed posts, workbook
  exports, or local-only artifacts
- stage, commit, push, open a PR, target `main`, or mark tracker #33 complete

## Files Changed

- `docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md`

Related existing untracked source artifact in this working tree:

- `docs/contracts/code_hardening_independent_test_authoring_policy.md`

## Interface Changes

None.

No runtime interface, parser interface, workbook schema, webhook payload, Apps
Script behavior, event class, event kind, fixture shape, snapshot shape,
baseline shape, CI gate, or environment-variable contract changed.

## Tests Added Or Updated

None.

This was a docs-only comparison pass.

## Protected-Surface Status

The comparison artifact is a documentation handoff under
`docs/implementation_handoffs/`.

No protected runtime, schema, parser, fixture, snapshot, baseline, secret,
local artifact, workbook, webhook, Apps Script, or deployment surface was
touched.

The source contract remains an untracked file in `docs/contracts/` from the
Codex B pass. That file is expected input for this comparison thread, not an
unrelated change.

## Recommended Future Implementation Scope

If the user authorizes implementation later, keep it narrow and governance-doc
focused. The likely minimal implementation package would be:

- update `docs/agent_threads/contract_test.md` to describe E2 as an optional
  pre-implementation Codex E mode
- update `docs/agent_threads/implementation.md` to tell Codex C to stop when
  triggered high-risk work lacks required independent evidence
- update `docs/codex_module_workflow.md` to document the optional high-risk
  E2 route without changing the normal path
- update `docs/agent_rules.yml` with a terse rule for independent
  test-identification triggers and E2 routing
- optionally update `.github/pull_request_template.md` or
  `docs/templates/implementation_handoff.md` to record independent evidence
  for triggered high-risk work

Implementation should not add tests or CI gates unless a future issue and
contract explicitly authorize executable enforcement.

## Still Unverified

- No policy implementation has been reviewed because no policy implementation
  was made.
- No Codex E contract-test review has been performed yet for this comparison
  artifact.
- No live GitHub PR or CI state exists for this comparison artifact.
- No final decision has been made about whether E2 should receive a dedicated
  template, remain only in `contract_test.md`, or be represented in
  `docs/agent_rules.yml`.
- No user override policy for missing independent evidence has been encoded in
  active workflow docs.

## Reviewer Focus

Codex E should verify:

- the comparison accurately distinguishes current workflow behavior from the
  new policy contract
- the recorded gaps are policy gaps, not runtime behavior bugs
- no implementation occurred in this pass
- the next recommended scope is narrow and does not accidentally make E2 a
  permanent role
- parser truth ownership and protected-surface rules remain unchanged
- the source contract and this handoff are the only intended changed files

## Validation Run

Validation should be interpreted as docs-only comparison validation.

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_independent_test_authoring_policy.md','docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py tools\check_agent_docs.py
```

Results are recorded in the final response for this Codex C thread.

Recorded results:

- `git diff --check` passed with no output. Because the contract and handoff
  files are untracked, direct no-index whitespace checks were also run against
  both files.
- `git diff --no-index --check -- NUL docs\contracts\code_hardening_independent_test_authoring_policy.md`
  produced no whitespace findings. Exit code `1` is expected for a new-file
  diff against `NUL`.
- `git diff --no-index --check -- NUL docs\implementation_handoffs\code_hardening_independent_test_authoring_policy_comparison.md`
  produced no whitespace findings. Exit code `1` is expected for a new-file
  diff against `NUL`.
- `py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite`
  passed with `changed_paths: 0`, `forbidden: 0`, `warnings: 0`. This command
  uses git diff and therefore does not see the untracked docs.
- Path-scoped protected-surface check for the source contract and comparison
  handoff passed with `changed_paths: 2`, `forbidden: 0`, `warnings: 0`.
- `py tools\check_agent_docs.py` did not run because
  `tools\check_agent_docs.py` is not present on the current branch.
- Trailing-whitespace scan for both docs found no matches.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer / contract-test thread for the Code Hardening child issue: Independent test-authoring policy for high-risk changes.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/72

Branch target:
codex/code-hardening-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/agent_threads/review.md
- docs/templates/contract_test_report.md
- docs/contracts/code_hardening_independent_test_authoring_policy.md
- docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md
- .github/pull_request_template.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- current hardening contracts under docs/contracts/

Goal:
Review the Codex C comparison artifact against the independent test-authoring policy contract. Produce docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md or an equivalent review report.

Review for:
- whether the comparison accurately identifies existing workflow support for high-risk gates
- whether the gaps around pre-implementation independent evidence and optional E2 are correct
- whether Codex B contract test sections can satisfy independent test identification for some high-risk work
- whether the comparison keeps E2 as an optional Codex E mode, not a new permanent role
- whether the comparison preserves parser truth ownership and protected-surface rules
- whether the comparison avoided implementation, tests, CI gates, workflow doc edits, schema changes, fixtures, snapshots, baselines, parser behavior, and protected artifacts

Do not:
- Implement the policy.
- Edit workflow docs, agent rules, templates, PR templates, tests, CI gates, parser behavior, schemas, fixtures, snapshots, baselines, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts.
- Make E2 a new permanent role.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Suggested validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_independent_test_authoring_policy.md','docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md','docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py tools\check_agent_docs.py
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/72"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md"
  target_artifact: "docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite"
    - "'docs/contracts/code_hardening_independent_test_authoring_policy.md','docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md' | py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin"
    - "py tools\\check_agent_docs.py"
  stop_conditions:
    - "Do not implement the policy in the review pass."
    - "Do not edit workflow docs, agent rules, templates, PR templates, tests, or CI gates."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, fixtures, expected outputs, schema snapshots, or drift baselines."
    - "Do not make E2 a new permanent role without a future governance issue and contract."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
