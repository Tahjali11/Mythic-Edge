# Code Hardening Independent Test-Authoring Policy Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/72

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target: `codex/code-hardening-suite`

Previous hardening context:

- Issue #68 / PR #69 added the golden fixture policy linked to the evidence
  ledger.
- Issue #70 / PR #71 added the drift detector baseline policy and merged into
  `codex/code-hardening-suite` at
  `416536f681dceeb7a889a7bd6c08451a9825a4b4`.
- Tracker #33 remains open.
- Tracker #33 names independent test-authoring policy for high-risk changes as
  the next queue item.

Agent docs read:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/review.md`
- `docs/templates/module_contract.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/workflow_handoff.md`
- `.github/pull_request_template.md`

Accepted ADRs read:

- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Current hardening contracts read:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`

This is a contract-writing artifact only. It does not implement the policy,
edit workflow docs, edit rules, edit templates, edit the PR template, add
tests, add CI gates, change parser behavior, change schemas, change fixtures,
change snapshots, change baselines, touch secrets, touch raw logs, touch
generated data, touch local artifacts, target `main`, or mark tracker #33
complete.

## Module

Independent test-authoring policy for high-risk Mythic Edge changes.

Plain English: before a high-risk change touches a sensitive part of Mythic
Edge, the project should know what evidence would prove the change is safe and
what evidence would prove it is wrong. That evidence should be identified by a
workflow thread that is not the implementation thread shaping the patch.

This policy covers independent test identification and, when separately
authorized, independent test authoring. It is workflow governance. It is not a
runtime parser feature and it does not define parser truth.

## Owning Layer

Owning layer: Mythic Edge workflow governance and code-hardening review policy.

Truth boundary:

- Parser and state interpretation remain the truth owners for event
  interpretation and normalized match/game facts.
- Independent tests, test plans, contract-test checklists, snapshots, fixtures,
  drift reports, protected-surface warnings, PR drift budgets, review comments,
  and AI outputs are evidence and review surfaces.
- Those evidence surfaces do not own parser truth, workbook truth, webhook
  truth, Apps Script truth, schema truth, match/game identity, deduplication,
  final reconciliation, deployment readiness, or production state.
- The policy may require evidence before implementation begins. It does not
  authorize the implementation itself.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/code_hardening_independent_test_authoring_policy.md`

Expected future comparison or implementation artifacts:

- `docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md`
- `docs/contract_test_reports/code_hardening_independent_test_authoring_policy.md`

Related files referenced but not owned by this contract:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `.github/pull_request_template.md`
- current hardening contracts under `docs/contracts/`
- accepted ADRs under `docs/decisions/`

Future files that require separate implementation authorization:

- workflow docs or role docs
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `.github/pull_request_template.md`
- tests, fixtures, snapshots, drift baselines, or CI workflow files

## Public Interface

This contract creates no runtime public interface.

The policy interface for later workflow implementation is:

- a definition of independent test identification
- a definition of independent test authoring
- trigger categories for mandatory independent evidence
- low-risk and medium-risk escape hatches
- evidence required before implementation begins
- role responsibilities for Codex A, B, optional E2, C, E, F, and G
- stop conditions when independent evidence is missing or inadequate
- validation expectations for future implementation and review threads

## Definitions

### Independent

Independent means workflow-independent, not necessarily a different human
person.

An independent test pass:

- is not performed by the Codex C implementation thread for the change under
  test
- starts from the issue, contract, current code/tests, protected-surface rules,
  and accepted ADRs
- does not start from the implementer's preferred patch
- produces a durable artifact before high-risk implementation begins
- names expected behavior, likely failure modes, test gaps, validation
  commands, and stop conditions
- may identify tests, author tests, or create an adversarial checklist when the
  current issue and contract allow that scope

Independence is broken when the implementation thread silently rewrites,
narrows, deletes, or ignores the independent evidence requirements without
routing back to Codex B, Codex E2, or the user.

### Independent Test Identification

Independent test identification is a durable pre-implementation artifact that
lists what tests, assertions, fixtures, snapshots, drift reports, manual review
checks, or validation commands are required.

It may live in:

- the module contract when the test inventory is concrete enough
- a Codex E2 adversarial contract-test checklist
- a contract-test report created before implementation
- a future workflow artifact explicitly authorized by the issue and contract

It does not have to create test files.

### Independent Test Authoring

Independent test authoring means a non-implementation workflow thread writes or
updates focused tests before Codex C implements the behavior change.

Independent test authoring is stronger than test identification. It is
appropriate when:

- the change is high risk and behavior-changing
- a focused failing test can be written safely before the implementation
- expected behavior is unambiguous
- the test can avoid touching protected runtime or data surfaces outside scope
- the issue and contract authorize adding or editing tests

This contract does not authorize adding tests in the contract-writer pass.

### Codex E2: Adversarial Contract Tester

Codex E2 is an optional mode of Codex E, not a new permanent role.

E2 may be used before Codex C for high-risk work to identify or author tests
from an adversarial review posture: "What would prove this implementation is
wrong, unsafe, under-tested, or overfitted?"

E2 should use `docs/agent_threads/contract_test.md` and the relevant contract,
but its output may be a pre-implementation checklist or test plan rather than
a post-implementation review report.

### High-Risk Change

A high-risk change is any change that can alter parser truth, protected
runtime/data/schema surfaces, deployment behavior, external integration
behavior, or durable workflow authority.

The exact triggers are listed below. The policy should classify by actual
diff and semantic effect, not by file extension alone.

## Why Independent Test Work Is Needed

High-risk changes can look clean while still weakening Mythic Edge.

Tests selected or authored only by the implementation thread can accidentally
be shaped around the patch instead of the contract. That creates overfitting:
the tests prove the patch does what the patch already does, but not that it
preserves parser truth, protected surfaces, schema boundaries, fixture policy,
or likely failure modes.

Independent test identification or authoring reduces these risks:

- implementation-biased tests
- missing contract tests for protected surfaces
- accidental movement of truth into workbook formulas, Apps Script,
  dashboards, AI outputs, or review notes
- broad implementation work starting before validation evidence is defined
- schema snapshot, golden fixture, drift baseline, or CI-gate updates that
  normalize drift before review
- PRs that pass mechanical checks but lack contract-level evidence
- reviewer confusion about whether a test is required, optional, or merely
  nice to have

The goal is not ceremony for every small edit. The goal is to make high-risk
truth/schema/deployment work harder to rubber-stamp and easier to review from
evidence.

## Observed Current Behavior

Observed on `codex/code-hardening-suite` during this contract pass:

- Current HEAD is
  `416536f681dceeb7a889a7bd6c08451a9825a4b4`, the PR #71 merge for drift
  detector baseline policy.
- The working tree was clean before this contract file was created.
- Tracker #33 describes the standard hardening flow:
  `A Thinker -> B Contract Writer -> C Implementer -> E Reviewer -> F
  Submitter -> G Deployer`.
- Tracker #33 recommends a modified flow for high-risk hardening issues:
  `A Thinker -> B Contract Writer -> E/E2 Contract Test Author or
  Adversarial Reviewer -> C Implementer -> E Reviewer -> F Submitter -> G
  Deployer`.
- Tracker #33 states that E2 is an optional mode of Codex E, not a new
  permanent role.
- `AGENTS.md`, `docs/agent_constitution.md`, and `docs/agent_rules.yml`
  require problem representation, module contract, implementation against the
  contract, review or contract testing, and validation evidence for high-risk
  changes.
- `docs/agent_threads/implementation.md` requires high-risk implementation to
  have a problem representation, module contract, and planned review or
  contract testing before code changes.
- `docs/agent_threads/contract_test.md` defines post-implementation contract
  verification, but it does not yet define a pre-implementation E2 pass.
- `.github/pull_request_template.md` requires risk tier, layer ownership,
  drift budget, contract verification, tests, still-unverified notes, and a
  workflow handoff.
- The protected-surface gate reports protected workflow and runtime surfaces
  and fails forbidden local/private/generated artifacts, but warnings are not
  automatic authorization or automatic rejection.
- Parser event schema snapshots, golden fixture policy, and drift detector
  baseline policy all require explicit approval for updates that could
  normalize drift.
- No existing contract specifically defines when independent test
  identification or authoring must happen before Codex C begins high-risk
  implementation.

## Required Guarantees

### Policy Scope Guarantee

The independent test-authoring policy must remain workflow governance.

It must not:

- change parser behavior
- change parser state final reconciliation
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change parser event classes, event kind values, or payload shapes
- change match identity, game identity, or deduplication
- create or refresh fixtures, snapshots, baselines, or expected outputs
- create failing CI gates
- authorize deployment behavior changes
- treat tests as parser truth

### Minimum Evidence Guarantee

When this policy is triggered, Codex C must not begin implementation until an
independent evidence artifact exists.

At minimum, that artifact must include:

- source issue or problem representation
- module contract or explicit contract draft
- risk tier and trigger category
- protected-surface disclosure
- current test inventory and known gaps
- required tests, review checks, or validation commands
- expected behavior and likely failure modes
- expected pre-implementation result for each test when knowable
- distinction between behavior-changing tests and regression/guard tests
- stop conditions that route back to Codex A or B when the evidence exposes
  ambiguity
- explicit statement that the artifact does not authorize protected-surface
  changes by itself

### High-Risk Trigger Guarantee

All high-risk changes must have independent test identification before Codex C
begins implementation.

Some high-risk changes should additionally route through Codex E2 for
adversarial test identification or test authoring before Codex C begins. E2 is
mandatory when the contract or issue says it is mandatory, and strongly
recommended when the change touches parser truth, schema shape, deployment
behavior, committed evidence, or failing gates.

### Non-Blocking Low-Risk Guarantee

Low-risk work must not be blocked by unnecessary independent-test ceremony.

Low-risk changes may proceed without E2 when they are obvious, local,
reversible, and do not change policy authority or protected surfaces.

Examples:

- typo fixes
- formatting-only edits
- broken-link fixes
- small docs clarifications that do not change rules
- generated handoff or report artifacts that do not change policy, behavior,
  schema, fixtures, snapshots, baselines, gates, or production state
- focused low-risk tests for already-scoped behavior

If a low-risk-looking change touches workflow authority docs, protected
surfaces, fixture policy, schema policy, gate behavior, or truth ownership, it
must be reclassified by semantic effect.

### Medium-Risk Escape Hatch

Medium-risk work does not automatically require Codex E2.

For medium-risk work, Codex B should define required tests in the contract.
Independent test identification is optional unless one of these is true:

- the issue or contract marks it required
- the change affects a broad shared parser utility
- the implementation would be hard to review after the fact
- the expected behavior is easy to overfit
- the change touches workflow authority docs or validation policy
- the user explicitly requests independent test identification

### Stop And Route Guarantee

Any workflow thread must stop and route back when:

- the issue and contract disagree about required evidence
- the independent test plan exposes ambiguous expected behavior
- implementing the test plan requires protected-surface changes not authorized
  by the issue and contract
- the implementation thread wants to narrow or remove independent test
  requirements
- the test plan would require committing raw logs, local artifacts, generated
  data, runtime files, failed posts, workbook exports, secrets, or credentials
- a failing CI gate would be created without an explicit escalation contract
- the work would move parser truth downstream

## Trigger Categories

### Mandatory Independent Test Identification

Independent test identification is required before implementation for changes
that affect any of these categories:

- parser truth ownership or movement of truth between layers
- parser state final reconciliation
- match identity
- game identity
- winner fields
- game result or match result semantics
- play/draw semantics
- mulligan count semantics
- opening-hand capture or interpretation
- deduplication keys or posted-once guards
- parser event classes
- event `kind` values
- parser payload shapes
- runtime event family, `event_type`, or `scope` values
- `MatchLogRow`, `GameLogRow`, sync fields, workbook-facing row keys, or sheet
  schema
- webhook payload shape
- Apps Script receiver, dispatch, field-map, or upsert behavior
- workbook schema or live/deployed workbook behavior
- golden fixtures, expected parser outputs, schema snapshots, drift baselines,
  drift report expected outputs, or evidence-ledger semantics
- failing CI gates, repo-check gates, validation policy, or required tooling
  escalation
- secrets, environment variable contracts, deployment behavior, or external
  connection behavior
- broad shared parser utilities where many parser modules depend on behavior
- future AI/analytics work that could affect parser truth labels, confidence
  labels, uncertainty policy, privacy boundaries, or user-facing decisions

### Strong E2 Candidates

Codex E2 adversarial test identification or test authoring should be used
before Codex C when any of these are true:

- a failing test can be written before the implementation
- a protected surface can drift while ordinary tests still pass
- a snapshot, fixture, expected output, or baseline update could normalize
  drift
- the change modifies a required or future-failing gate
- the change touches deployment or external integration behavior
- the change crosses parser, webhook, Apps Script, workbook, dashboard, or AI
  layer boundaries
- the implementation requires compatibility with old and new behavior at the
  same time
- the contract has enough detail to test, but enough risk that implementation
  bias would be costly

### Optional Triggers

Independent test identification is optional but recommended for:

- medium-risk interface changes
- shared helper refactors with broad call sites and no intended behavior
  change
- policy/template changes that affect later protected-surface review
- new validation tools that are advisory-only
- large docs changes that alter workflow expectations without changing runtime
  behavior

### Non-Triggers

Independent test identification is not required for:

- typo fixes
- formatting-only edits
- tiny wording clarifications that do not change policy authority
- local comments
- link fixes
- docs-only handoff/report artifacts that record already-completed work
- small low-risk tests whose expected behavior is already named by an existing
  contract
- reverting an accidental uncommitted local change before it is staged, when
  the user explicitly asks and no protected artifact is being preserved

## Evidence Required Before Implementation Begins

For triggered high-risk work, the required pre-implementation evidence package
must include:

| Evidence | Required content |
| --- | --- |
| Source issue | GitHub issue or problem representation link. |
| Contract | Module contract or contract draft naming behavior, protected surfaces, validation, and stop conditions. |
| Risk classification | Risk tier, trigger category, and why the policy applies. |
| Truth boundary | Owning truth layer and downstream consumer layers. |
| Protected-surface disclosure | Files, schemas, artifacts, gates, or runtime surfaces likely to be touched. |
| Current coverage inventory | Existing tests, snapshots, fixtures, checks, and known gaps. |
| Required-test plan | Focused tests, regression tests, contract tests, snapshot checks, fixture checks, drift checks, or manual review checks required. |
| Expected pre-implementation result | Which tests should fail before implementation, which should pass, and which are guard-only. |
| Validation commands | Focused commands first, broader commands when risk justifies them. |
| Stop conditions | Exact conditions that route back to Codex A, B, or E2. |
| Forbidden scope | Explicit protected surfaces and artifacts that remain out of scope. |
| Handoff routing | Next role and whether E2 is mandatory, optional, or not required. |

If actual tests are authored before implementation, the evidence package must
also include:

- files changed
- why the tests are independent from the implementation
- whether any tests intentionally fail before implementation
- how to run only the new/focused tests
- what would make the test invalid or too broad
- confirmation that tests do not contain raw logs, secrets, generated data,
  runtime status files, failed posts, workbook exports, or local-only artifacts

## Role Responsibilities

### Codex A: Thinker

Codex A should:

- classify risk tier and trigger category
- identify whether independent test identification or E2 is required
- name protected surfaces and truth boundaries early
- include the policy expectation in the issue or problem representation
- route to Codex B for contract writing

Codex A should not:

- implement tests or behavior changes
- treat E2 as required for low-risk work by default

### Codex B: Module Contract Writer

Codex B should:

- define required guarantees and test obligations
- state whether independent evidence is already sufficient in the contract or
  whether E2 must run before Codex C
- define trigger category, expected validation, stop conditions, and protected
  surfaces
- keep the artifact under `docs/contracts/`
- avoid implementing behavior, tests, gates, templates, or workflow docs unless
  explicitly authorized by a different role/scope

Codex B may satisfy independent test identification when the contract includes
a concrete enough test inventory for Codex C and Codex E to use directly.

Codex B should route to E2 before C when:

- the issue marks E2 required
- the contract cannot confidently identify all tests
- the change is high-risk and behavior-changing
- test authoring before implementation would materially reduce overfitting
- the validation plan needs adversarial review before code is written

### Codex E2: Adversarial Contract Tester

Codex E2 should:

- operate as a specialized Codex E mode
- start from the issue, contract, current code/tests, ADRs, and protected
  surface rules
- identify missing tests and adversarial cases before implementation
- author tests only when the issue and contract authorize test edits
- produce a durable artifact, normally under `docs/contract_test_reports/` or
  a clearly named pre-implementation checklist/report
- route to Codex C only when evidence is clear enough to implement safely

Codex E2 should not:

- implement production behavior
- change parser truth or schemas
- update snapshots, fixtures, expected outputs, or baselines unless explicitly
  authorized
- become a new permanent workflow role without a future governance change

### Codex C: Module Implementer

Codex C should:

- confirm the required independent evidence exists before editing high-risk
  behavior
- restate intended behavior, current behavior, likely failure point, and exact
  plan before significant edits
- implement the smallest coherent change that satisfies the contract and
  independent evidence
- add or update the tests required by the contract and E2 artifact
- route back to Codex B or E2 if the test plan is ambiguous, too broad, or
  unsafe
- produce an implementation handoff

Codex C must not:

- silently narrow independent test requirements
- start high-risk implementation when required independent evidence is missing
- use passing tests as permission to touch protected surfaces outside scope

### Codex E: Module Reviewer

Codex E should:

- verify the implementation against the issue, contract, independent evidence,
  diff, and validation
- lead with findings
- treat missing required independent evidence as a blocking review finding for
  triggered high-risk work
- distinguish missing tests from contract ambiguity
- route to D, B, A, F, or none as appropriate

### Codex F: Module Submitter

Codex F should:

- inspect status and stage only reviewed files
- confirm the required independent evidence is linked in the handoff or PR
  body for triggered high-risk work
- ensure the PR drift budget names protected-surface authorization and
  residual gaps
- stop if required evidence, review, validation, or protected-surface
  disclosure is missing

Codex F must not:

- submit high-risk implementation as ready when independent evidence is
  missing
- use the PR template as authorization for protected-surface change

### Codex G: Integration Deployer

Codex G should:

- verify merge readiness against issue, contract, review, PR drift budget,
  CI, protected-surface output, and independent evidence
- treat missing required independent evidence as a merge-readiness blocker for
  triggered high-risk work
- accept an override only when the user explicitly approves the missing
  evidence and the residual risk is recorded
- avoid merging to `main` or production branches unless explicitly approved

## Relationship To Existing Hardening Policies

### Protected-Surface Gate

The protected-surface gate reports path-level risk. It does not decide whether
tests are sufficient.

If protected warnings appear in a high-risk PR, the independent evidence must
explain:

- why the protected surface is in scope
- what tests or checks constrain the change
- what remains unverified
- what issue and contract authorize the semantic change

### PR Drift Budget

The PR drift budget records semantic drift and authorization. It does not
create authorization.

For triggered high-risk work, the PR drift budget should cite the independent
evidence artifact when relevant, especially under:

- `Runtime/parser behavior`
- `Parser event shape/classes`
- `Workbook/webhook/App Script shape`
- `Parser truth ownership`
- `Fixtures/evidence`
- `Protected-surface authorization`
- `Residual drift / accepted gaps`

### Parser Event Schema Snapshots

Schema snapshots protect shape drift. They must not be auto-updated to make a
high-risk implementation pass.

If schema snapshots are affected, independent evidence must distinguish:

- expected schema preservation
- authorized schema drift
- snapshot fixture update
- parser behavior bug
- Apps Script parity drift

### Golden Fixtures

Golden fixtures are committed evidence and expected-output artifacts. They
must not be created, refreshed, or reinterpreted as part of independent testing
unless a specific issue and contract authorize fixture work.

Independent test plans may require fixture review or future fixture creation,
but they do not by themselves authorize committing raw or sanitized evidence.

### Drift Detector Baselines

Drift detector baselines are report-only unless a future issue and contract
escalate them.

Independent evidence for a baseline or gate change must preserve the
report-only default and must not normalize drift through an unreviewed baseline
refresh.

### Pyright Advisory

Pyright remains advisory under the current hardening suite policy.

Independent evidence may require Pyright output for a high-risk typing or
tooling change, but zero Pyright findings is not required unless a future
contract escalates Pyright to a required gate.

## Error Behavior

If a triggered high-risk issue lacks independent evidence:

- Codex C must stop before implementation.
- Codex E should report a blocking process finding if implementation already
  happened.
- Codex F should not submit the PR as ready.
- Codex G should treat the PR as not merge-ready unless the user explicitly
  accepts the override and residual risk.

If independent evidence conflicts with the contract:

- route to Codex B for contract clarification.

If independent evidence changes the problem framing:

- route to Codex A.

If independent tests expose a concrete implementation defect after Codex C:

- route to Codex D or Codex C depending on the workflow state.

If independent tests require unauthorized protected-surface changes:

- stop and route back to Codex B or A.

## Side Effects

Allowed side effect in this Codex B thread:

- create
  `docs/contracts/code_hardening_independent_test_authoring_policy.md`

Forbidden side effects in this Codex B thread:

- no workflow doc implementation
- no rule or template edits
- no PR template edits
- no test creation
- no CI gate changes
- no parser behavior changes
- no schema changes
- no fixture, snapshot, expected-output, or baseline changes
- no raw-log, generated-data, runtime-status, failed-post, workbook-export, or
  local-only artifact changes
- no tracker closure

## Dependency Order

Future implementation/comparison work should proceed in this order:

1. Confirm the target branch is `codex/code-hardening-suite`.
2. Confirm the issue and contract authorize policy implementation or
   comparison.
3. Inspect `git status` and exclude unrelated files.
4. Compare existing workflow docs, rules, templates, and PR template against
   this contract.
5. Decide whether implementation is docs-only, rules-only, template-only, or
   comparison-only under the current instruction.
6. If implementation is authorized, make the smallest governance-doc updates
   needed to reflect the policy.
7. Do not add tests, CI gates, fixtures, snapshots, baselines, or runtime
   behavior unless separately authorized.
8. Run focused documentation and protected-surface validation.
9. Produce the implementation handoff.
10. Route to Codex E for review.

Stop and route back to Codex B or A if satisfying the policy would require a
new permanent role, CI enforcement, parser behavior change, schema change,
fixture creation, snapshot update, baseline refresh, deployment policy change,
or merge-to-main policy change not authorized by the current issue and
contract.

## Compatibility

- Existing A/B/C/D/E/F/G role names remain valid.
- E2 remains an optional Codex E mode, not a new permanent role.
- Existing low-risk workflow escape hatches remain valid.
- Existing high-risk requirements for issue, contract, implementation,
  review/contract test, validation, and submitter handoff remain valid.
- Existing protected-surface gate behavior remains unchanged.
- Existing PR drift budget labels remain unchanged.
- Existing snapshot, fixture, drift-baseline, and Pyright advisory policies
  remain unchanged.
- Existing branch policy remains `codex/code-hardening-suite`, not `main`.

## Unknowns

- Whether E2 should later get a dedicated role file, or remain described only
  as a specialized Codex E mode.
- Whether pre-implementation E2 artifacts should live under
  `docs/contract_test_reports/`, `docs/implementation_handoffs/`, or a future
  dedicated directory.
- Whether actual independent test authoring should happen on a separate branch
  before Codex C, or in the same branch with careful handoff ordering.
- Whether every high-risk issue should require E2, or whether a detailed Codex
  B contract is sufficient for some high-risk changes.
- How to handle urgent high-risk bug fixes when CI or a focused failing test
  already provides independent evidence.
- Whether Codex G should have a formal override checklist for missing
  independent evidence, or only record explicit user approval and residual
  risk.
- Whether future tooling should automatically detect trigger categories from
  changed paths and PR drift-budget fields.

## Suspected Gaps

- Current workflow docs require high-risk review and validation, but do not yet
  require independent test identification before implementation begins.
- `docs/agent_threads/contract_test.md` is post-implementation oriented and
  does not describe pre-implementation E2 behavior.
- The PR template asks for contract verification but does not explicitly ask
  whether triggered high-risk work had independent pre-implementation test
  evidence.
- Codex B contracts often list required tests, but the repo does not yet define
  when that is sufficient versus when E2 should run before C.
- Protected-surface warnings can identify sensitive paths, but they do not
  require a pre-implementation adversarial test plan by themselves.
- Existing hardening policies prevent auto-updating snapshots, fixtures, and
  baselines, but they do not yet define a general independent-test gate for
  high-risk behavior changes.

## Validation Requirements

### Contract-Writer Validation

Because this Codex B thread creates only a new Markdown file:

```powershell
git diff --check
git diff --no-index --check -- NUL docs\contracts\code_hardening_independent_test_authoring_policy.md
```

Recommended path-scoped protected-surface check:

```powershell
'docs/contracts/code_hardening_independent_test_authoring_policy.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Runtime parser tests are not required for a docs-only contract writer pass.

### Future Codex C Comparison Validation

For a docs-only comparison:

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_independent_test_authoring_policy.md','docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
rg -n "independent|E2|high-risk|test author|protected surface|truth ownership" AGENTS.md docs .github\pull_request_template.md
```

If Codex C edits workflow docs, rules, templates, or the PR template:

```powershell
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

If executable tests or tooling are added by a future authorized issue:

```powershell
py -m pytest -q <focused tests>
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Before any future PR that changes workflow authority docs, templates, tests,
or CI gates:

```powershell
py -m pytest -q
py -m ruff check src tests tools
pyright --project pyrightconfig.json
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
git diff --check
```

Interpretation:

- Pyright remains advisory unless a future contract escalates it.
- Full-suite validation is recommended before submitter work if tests, CI,
  tooling, parser behavior, fixtures, snapshots, baselines, or workflow
  authority docs change.
- If only this contract file changes, runtime parser tests are not required.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- sync field names
- runtime family names
- runtime `event_type` values
- runtime `scope` values
- fixtures
- expected parser outputs
- schema snapshots
- drift baselines
- drift report expected outputs
- CI failure gates
- deployment behavior
- production behavior
- merge-to-main policy
- secrets, credentials, tokens, API keys, or webhook URLs
- environment variable contracts
- raw local logs
- generated card/tier data
- runtime status files
- failed posts
- workbook exports
- local-only artifacts

## Out Of Scope

This issue does not authorize:

- implementing the policy
- editing workflow docs, rules, templates, or PR templates
- adding tests
- adding CI gates
- changing parser behavior
- changing parser state final reconciliation
- changing workbook schema
- changing webhook payload shape
- changing Apps Script behavior
- changing parser event classes, event kind values, or parser payload shapes
- changing match identity, game identity, or deduplication
- changing fixtures, expected outputs, schema snapshots, or drift baselines
- touching secrets, environment variables, raw logs, generated data, runtime
  status files, failed posts, workbook exports, or local-only artifacts
- targeting `main`
- marking tracker #33 complete

## Acceptance Criteria

- `docs/contracts/code_hardening_independent_test_authoring_policy.md` exists.
- The contract explains why high-risk changes need independent test
  identification or authoring before implementation.
- The contract defines what independent means in the Mythic Edge workflow.
- The contract defines high-risk trigger categories.
- The contract defines evidence required before implementation begins.
- The contract explains the relationship to Codex B, Codex C, Codex E, optional
  Codex E2, Codex F, and Codex G.
- The contract defines low-risk and medium-risk escape hatches.
- The contract preserves parser truth ownership and protected-surface rules.
- The contract distinguishes observed current behavior, required guarantees,
  unknowns, suspected gaps, out-of-scope changes, and validation expectations.
- The contract includes a pasteable Codex C handoff prompt.
- The contract does not implement the policy, edit governance docs/templates,
  add tests, add CI gates, change parser behavior, change schemas, change
  fixtures/snapshots/baselines, touch protected artifacts, target `main`, or
  mark tracker #33 complete.

## Handoff Packet

Role performed: Codex B: Module Contract Writer.

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue used: https://github.com/Tahjali11/Mythic-Edge/issues/72

Contract artifact produced:
`docs/contracts/code_hardening_independent_test_authoring_policy.md`

Risk tier: Medium for policy-only contract writing. Escalate to High if future
work edits workflow authority docs in a blocking way, adds tests, adds CI
gates, changes protected-surface enforcement behavior, or changes parser,
schema, fixture, snapshot, baseline, deployment, or production behavior.

Owning truth layer: Mythic Edge workflow governance and code-hardening review
policy; parser/state remains truth owner for event interpretation and
normalized match/game facts.

Public interface:

- independent test identification vocabulary
- independent test authoring vocabulary
- high-risk trigger categories
- pre-implementation evidence package
- role responsibilities and stop conditions
- validation and protected-surface expectations

Invariants:

- Independent means separate from the implementation thread.
- High-risk triggered work requires independent test identification before
  implementation.
- E2 remains an optional Codex E mode, not a new permanent role.
- Tests and test plans are evidence surfaces, not truth owners.
- Low-risk work should not be blocked by unnecessary process.
- Parser truth ownership and protected-surface rules remain unchanged.

Required validation: listed above.

Acceptance criteria: listed above.

Unknowns and suspected gaps: listed above.

Next recommended role: Codex C: Module Implementer / comparison thread.

Pasteable Codex C prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for the Code Hardening child issue: Independent test-authoring policy for high-risk changes.

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
- docs/agent_threads/module_contract.md
- docs/agent_threads/contract_test.md
- docs/agent_threads/implementation.md
- docs/agent_threads/review.md
- docs/templates/module_contract.md
- docs/templates/contract_test_report.md
- docs/templates/implementation_handoff.md
- docs/templates/workflow_handoff.md
- .github/pull_request_template.md
- docs/decisions/README.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- docs/contracts/code_hardening_independent_test_authoring_policy.md
- current hardening contracts under docs/contracts/

Goal:
Compare the current workflow docs, agent rules, templates, PR template, ADRs, and hardening contracts against docs/contracts/code_hardening_independent_test_authoring_policy.md. Produce docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md. Keep the pass comparison/docs-focused unless the user explicitly authorizes implementation.

Before editing:
- Confirm the branch is codex/code-hardening-suite.
- Inspect git status and exclude unrelated changes.
- State what the independent test-authoring policy is supposed to do, what current workflow docs already do, what gaps remain, and the exact minimal comparison or implementation plan.

Do:
- Compare current A/B/C/D/E/F/G workflow docs against the contract.
- Compare contract-test, implementation, review, submitter/deployer expectations against the contract.
- Compare the PR template drift budget and contract verification sections against the contract.
- Identify whether Codex B contract test sections already satisfy independent test identification for some high-risk work.
- Identify where optional Codex E2 behavior is present, absent, or only tracker-level.
- Produce docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md with files inspected, observed matches, gaps, protected-surface status, validation, remaining risks, and next recommended role.

Do not:
- Implement the policy unless explicitly authorized.
- Edit workflow docs, agent rules, templates, or PR templates unless explicitly authorized.
- Add tests or CI gates.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, fixtures, expected outputs, schema snapshots, or drift baselines.
- Make E2 a new permanent role unless a future governance issue and contract authorize it.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_independent_test_authoring_policy.md','docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py tools\check_agent_docs.py
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/72"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/code_hardening_independent_test_authoring_policy.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_independent_test_authoring_policy_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "git diff --no-index --check -- NUL docs\\contracts\\code_hardening_independent_test_authoring_policy.md"
  stop_conditions:
    - "Do not implement the policy unless explicitly authorized."
    - "Do not edit workflow docs, agent rules, templates, or PR templates unless explicitly authorized."
    - "Do not add tests or CI gates."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, fixtures, expected outputs, schema snapshots, or drift baselines."
    - "Do not make E2 a new permanent role unless a future governance issue and contract authorize it."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
