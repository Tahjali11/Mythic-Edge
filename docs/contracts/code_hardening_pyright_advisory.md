# Code Hardening Pyright Advisory Type-Checking Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/45

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target: `codex/code-hardening-suite`

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Issue #45 also names `docs/agent_rules.yml` as a rule source. On the current
`codex/code-hardening-suite` branch inspected for this contract, that file is
not present. This contract therefore treats `docs/agent_constitution.md`,
tracker #33, issue #45, the protected-surface gate contract, the PR drift-budget
contract, and this contract as the available policy sources. Adding or syncing
`docs/agent_rules.yml` remains a separate explicitly authorized workflow
change.

Related hardening context:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- PR #37, protected-surface diff gate, merged into
  `codex/code-hardening-suite` at `cc9f524`
- PR #42, PR drift-budget section, merged into
  `codex/code-hardening-suite` at `3dcb430`

This contract defines the first Pyright rollout for the Code Hardening suite.
It is a contract artifact only. It does not implement code, add Pyright as a
required CI gate, require fixing all findings, target `main`, or mark tracker
#33 complete.

## Module

Pyright advisory type-checking.

Likely first implementation artifacts:

- `pyrightconfig.json`
- `pyproject.toml`
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`
- `docs/contract_test_reports/code_hardening_pyright_advisory.md`

Optional implementation artifacts, only if they preserve advisory behavior:

- a local wrapper such as `tools/run_pyright_advisory.ps1`
- an optional switch in `tools/run_repo_checks.ps1`
- a non-blocking GitHub Actions report step

Plain English: Pyright should start as a flashlight, not a hammer. The first
rollout should make type-risk visible and reproducible without blocking normal
tests, Ruff, parser audit work, workbook work, or hardening work.

## Owning Layer

Repository coordination and code hardening.

Truth boundary:

- Pyright can report interface, optional-value, import, callback, and type
  drift risks.
- Pyright findings do not define parser truth.
- Parser/state remains the owner of event interpretation, match/game identity,
  final reconciliation, and parser-managed facts.
- Workbook schema, webhook payload shape, Apps Script behavior, parser event
  classes, match/game identity, deduplication, and final reconciliation remain
  protected surfaces that require explicit issue/contract authority before
  behavior changes.
- Type-checking configuration and reports must not become a workaround layer
  that silently excludes important parser/runtime code from review.

## Files Owned By This Contract

- `docs/contracts/code_hardening_pyright_advisory.md`

Expected future implementation files owned by this contract:

- `pyrightconfig.json`
- `pyproject.toml`, only for a reproducible advisory Pyright dependency
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`
- `docs/contract_test_reports/code_hardening_pyright_advisory.md`

Optional files this contract may allow Codex C to touch:

- `.github/workflows/repo-checks.yml`, only for a clearly non-blocking
  advisory step
- `tools/run_repo_checks.ps1`, only for an opt-in advisory switch that is not
  part of the default required repo check
- a small dedicated wrapper under `tools/`, only if it simplifies local
  advisory invocation without changing parser behavior

Related files referenced but not owned by this contract:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`, when present on the target branch
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `.github/pull_request_template.md`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tools/check_protected_surfaces.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/runner.py`
- parser modules under `src/mythic_edge_parser/parsers/`
- tests that exercise parser/runtime interfaces

## Observed Current State

Current branch: `codex/code-hardening-suite`

Observed configuration:

- `pyproject.toml` defines package metadata, Python `>=3.11`, runtime
  dependencies, and the `dev` optional dependency group.
- The current `dev` group includes pytest, pytest-cov, and Ruff.
- No Pyright dependency is configured in `pyproject.toml`.
- No `pyrightconfig.json` is present.
- No `package.json`, `package-lock.json`, pnpm lockfile, or yarn lockfile is
  present for Node-based Pyright installation.
- `.github/workflows/repo-checks.yml` runs tests, the protected-surface gate on
  pull requests, and Ruff on Windows/Python 3.13.
- `tools/run_repo_checks.ps1` runs tests and Ruff locally, with optional
  coverage. It does not run Pyright.
- No Pyright CI step, local Pyright wrapper, or baseline report is present.

Observed hardening context:

- The protected-surface gate already fails forbidden committed artifacts and
  reports protected-source warnings without failing warnings-only diffs.
- The PR template already includes a drift-budget section requiring authors to
  disclose behavior, event-shape, workbook/webhook/App Script, parser truth,
  fixture/evidence, protected-surface, residual drift, and follow-up status.

## Public Interface

### Configuration

Required first configuration location:

```text
pyrightconfig.json
```

Required configuration posture:

- Advisory first.
- `typeCheckingMode` should be `basic` unless a future contract escalates.
- `pythonVersion` should target the project minimum, currently `3.11`, unless
  Codex C records a compatibility reason to choose otherwise.
- The config must include project source code under `src`.
- The config should include tests unless Codex C records an explicit
  report-oriented reason to defer test coverage.
- The config may exclude local/generated/private artifacts such as `.venv`,
  build outputs, caches, `data/**`, workbook exports, failed posts, runtime
  status, and other non-source generated paths.
- The config must not use broad ignores to hide the parser/runtime package.
- The config must not contain local absolute machine paths.

Allowed configuration examples:

```json
{
  "include": ["src", "tests"],
  "exclude": [
    ".venv",
    "build",
    "dist",
    "data",
    "workbook_exports",
    "exports",
    ".pytest_cache"
  ],
  "pythonVersion": "3.11",
  "typeCheckingMode": "basic"
}
```

The example is illustrative. Codex C must compare the actual config against
the contract and explain any differences in the implementation handoff.

### Dependency Strategy

Preferred first dependency strategy:

- Add the Python `pyright` package to `[project.optional-dependencies].dev` in
  `pyproject.toml`.
- Keep dependency versioning broad enough for normal maintenance, for example
  `pyright>=1.1,<2`, unless Codex C records a reason to pin more tightly.

Fallback strategy:

- If the Python package cannot provide a reproducible local command in this
  repo, Codex C must stop and route back to Codex B before introducing npm,
  npx, package locks, or a second package-manager ecosystem.

Forbidden first-rollout dependency behavior:

- Do not add unpinned ad hoc `npx pyright` usage as the only reproducible path.
- Do not require a global Pyright install.
- Do not require Node/npm setup unless the contract is amended or the user
  explicitly approves it.

### Invocation

Required advisory local command shape:

```powershell
pyright --project pyrightconfig.json
```

Equivalent commands may be documented only after Codex C verifies they work in
the repo environment, for example:

```powershell
py -m pyright --project pyrightconfig.json
```

Advisory interpretation:

- The command may exit nonzero while findings exist.
- A nonzero Pyright exit caused only by type findings is not a failed
  implementation by itself.
- Codex C/E must record the exit behavior and summarize findings.
- Tool installation failure, invalid config, or a command that cannot run is a
  blocker for the advisory rollout.

### Local Repo Check Integration

Required first behavior:

- Do not add Pyright to the default required `tools/run_repo_checks.ps1`
  sequence.
- The existing default repo checks must remain tests plus Ruff unless a later
  contract escalates Pyright.

Allowed first behavior:

- Add an opt-in switch such as `-PyrightAdvisory`, or add a dedicated wrapper,
  only if it clearly treats findings as advisory and records the command output.

### CI Integration

Required first behavior:

- Do not make Pyright a required or failing CI gate.
- Do not make protected branch merge readiness depend on zero Pyright findings.

Allowed first behavior:

- Codex C may add a non-blocking advisory GitHub Actions step only if it is
  clearly named advisory and configured so type findings do not fail Repo
  Checks.
- If CI integration is added, it must preserve the existing required tests,
  protected-surface gate, and Ruff behavior.
- If Codex C cannot prove non-blocking behavior, it must keep the first rollout
  local-only and record that decision.

## Inputs

### Python Source And Tests

Primary inputs:

- `src/mythic_edge_parser/**`
- `tests/**`, unless explicitly deferred in the config/report

Expected dynamic boundaries:

- parser event payloads represented as JSON-like dictionaries
- `Any` at raw log and payload boundaries
- optional timestamps, winners, game numbers, callbacks, queues, and runtime
  status fields
- tests that use lightweight `SimpleNamespace`, monkeypatching, and dict
  fixtures

The first rollout should report risks in these areas, not force an immediate
rewrite of dynamic parser boundaries.

### Configuration Inputs

Configuration sources:

- `pyrightconfig.json`
- Python version and package metadata from `pyproject.toml`
- current import paths from `src` layout and pytest `pythonpath`

Required config limits:

- No local absolute paths.
- No references to ignored local data folders as source.
- No silent exclusion of `src/mythic_edge_parser`.

### Tooling Inputs

Tooling sources:

- `[project.optional-dependencies].dev` in `pyproject.toml`
- local command invocation
- optional CI or PowerShell wrapper, if implemented

Tooling must be reproducible from a clean clone using documented dev setup.

## Outputs

### Advisory Command Result

Output type: terminal report from Pyright.

Destination:

- local terminal
- implementation handoff summary
- optional non-blocking CI logs

Required recorded evidence:

- exact command
- whether the command ran
- exit code
- config file used
- total finding count, if available
- representative finding categories
- whether findings are advisory, accepted baseline, follow-up, or blockers

### Baseline Report Policy

The first implementation must create a report-oriented baseline section in:

```text
docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md
```

Codex E should later summarize or verify that baseline in:

```text
docs/contract_test_reports/code_hardening_pyright_advisory.md
```

Baseline policy:

- The baseline is a snapshot of current type-checking risk, not a pass/fail
  gate.
- The baseline must not require fixing all Pyright findings.
- The baseline should summarize findings by category and high-risk files rather
  than committing large raw output.
- The baseline should avoid local absolute paths; use repo-relative paths.
- The baseline should not include secrets, raw logs, runtime status payloads,
  failed posts, generated data, workbook exports, or private local artifacts.
- The baseline should distinguish `tooling/config blockers` from ordinary
  advisory type findings.
- If the finding volume is too large to summarize usefully, Codex C must record
  the volume, top categories, and a follow-up recommendation rather than
  broadening scope into cleanup.

No standalone machine-generated Pyright output file is required in the first
rollout. A future contract may add a dedicated baseline file if the team wants
drift comparisons over time.

## Finding Categories

Allowed first-rollout categories:

### `tooling_config_blocker`

Use for issues that prevent the advisory rollout from being reproducible.

Examples:

- Pyright command cannot run after documented install.
- `pyrightconfig.json` is invalid.
- Config excludes all important source directories.
- Import resolution fails because packaging paths are misconfigured.

These are blockers for Codex C/E before submitter work.

### `likely_interface_drift`

Use for findings that suggest a real mismatch between call sites, signatures,
attributes, imports, or callbacks.

Examples:

- missing attribute on a known event object
- wrong callback arity
- incompatible assignment between model/state/output interfaces
- import path cannot be resolved for a committed source module

These are not automatically fixed in the first rollout. They should become
follow-up candidates unless a tiny tooling-only fix is clearly safe.

### `optional_or_none_risk`

Use for findings around `None`, optional timestamps, optional payload fields,
or values that may be blank/unknown.

These are useful hardening signals because parser truth often distinguishes
unknown from final facts. Fixes still require focused issues if they affect
parser behavior.

### `dynamic_payload_boundary`

Use for findings caused by intentional JSON-like payload dictionaries,
`Any`, runtime event payloads, or test fixtures.

These may be accepted advisory findings in the first baseline. Do not erase
them by blanket-ignore unless the report explains the boundary.

### `missing_type_information`

Use for missing stubs or third-party packages with incomplete type data.

These should not block the first rollout unless they prevent useful analysis of
the project source.

### `test_typing_noise`

Use for test-only monkeypatching, `SimpleNamespace`, fixture dictionaries, and
other patterns that are acceptable in tests but noisy for static typing.

Codex C may recommend later test typing cleanup, but must not refactor test
fixtures broadly during the first rollout.

### `false_positive_or_needs_triage`

Use when Pyright reports something that appears safe but needs human or later
contract review.

These should be named honestly rather than hidden.

### `protected_surface_fix_required`

Use only when a finding appears to require touching protected parser/runtime,
workbook, webhook, Apps Script, identity, dedupe, or reconciliation behavior.

This category is a stop condition for the first implementation. Route to a new
issue/contract instead of fixing it inside Pyright adoption.

## Advisory Versus Required Behavior

Required first-rollout policy:

- Pyright findings are advisory.
- Existing tests, protected-surface gate, and Ruff remain the required gates.
- A nonzero Pyright exit caused by type findings may be accepted in the
  baseline.
- Codex C may fix tiny setup/config/import issues only when they are tooling
  issues and do not change runtime behavior.
- Codex C must not perform broad code annotation or behavior cleanup to make
  Pyright pass.
- Codex C must not make zero Pyright findings an acceptance criterion.

Required wording for handoffs and PRs:

- Use `Advisory Pyright findings remain` when findings are accepted in the
  first baseline.
- Use `Tooling/config blocker` only for failures that prevent the advisory
  check from running or reporting.
- Use the PR drift budget to state that parser/runtime behavior has `No drift`
  unless a separate issue/contract authorizes a real behavior change.

## Protected Surfaces

This issue must preserve:

- parser behavior and parser event interpretation
- parser state final reconciliation
- parser event classes and payload shapes
- match/game identity
- deduplication and posted-row state semantics
- workbook schema and workbook-facing row shape
- webhook payload shape
- Apps Script behavior
- secrets, webhook URLs, API keys, tokens, credentials, and environment
  variable semantics
- local MTGA logs, raw logs, runtime logs, runtime status files, failed posts,
  generated data, and workbook exports as non-committed artifacts

Workflow/tooling surfaces intentionally in scope:

- Pyright configuration
- dev dependency metadata needed to run Pyright
- local advisory command documentation
- optional non-blocking advisory CI/reporting behavior
- hardening contracts, handoffs, and reports

## Error Behavior

Expected first rollout behavior:

- Invalid Pyright config is a blocker.
- Missing Pyright command after documented setup is a blocker.
- Pyright type findings are advisory baseline data.
- CI must not fail because of Pyright type findings in the first rollout.
- Local wrapper scripts, if added, must clearly distinguish command/tooling
  failure from advisory type findings.

Stop and route back to Codex B or A if:

- the only viable invocation requires a new package manager strategy not
  described by this contract
- Pyright cannot analyze source without broad excludes
- useful Pyright output requires changing parser behavior first
- implementing a finding would touch a protected surface without explicit
  authorization

## Side Effects

Allowed side effects for Codex C:

- Add Pyright advisory configuration.
- Add a reproducible dev dependency for Pyright.
- Run Pyright locally to produce advisory evidence.
- Write an implementation handoff with baseline findings.
- Optionally add a non-blocking local wrapper or CI report step if advisory
  behavior is preserved.

Forbidden side effects:

- Do not change parser behavior.
- Do not change parser state final reconciliation.
- Do not change parser event classes or payload shapes.
- Do not change workbook schema.
- Do not change webhook payload shape.
- Do not change Apps Script behavior.
- Do not change match/game identity or deduplication.
- Do not change secrets or environment variables.
- Do not commit raw logs, generated data, runtime status files, failed posts,
  or workbook exports.
- Do not make Pyright required or failing in CI.
- Do not mark tracker #33 complete.

## Dependency Order

Future implementation should proceed in this order:

1. Confirm branch is `codex/code-hardening-suite`.
2. Compare `pyproject.toml`, repo checks, PR template, and existing hardening
   contracts against this contract.
3. Add the minimal reproducible Pyright dependency.
4. Add `pyrightconfig.json` with advisory/basic posture.
5. Run the advisory command and record baseline evidence.
6. Decide whether any optional wrapper or non-blocking CI report is necessary.
7. Run required non-Pyright validation.
8. Produce the implementation handoff.
9. Route to Codex E for contract-test review.

If implementation requires broad type cleanup, parser/runtime changes, package
manager changes beyond the contract, CI failure gating, or protected-surface
changes, stop and route back.

## Compatibility

Compatibility that must remain stable:

- Existing package install remains `py -m pip install -e .[dev]`.
- Existing required CI gates remain tests, protected-surface gate, and Ruff.
- Existing default `tools/run_repo_checks.ps1` behavior remains tests and Ruff
  unless a later contract escalates Pyright.
- Existing PR drift-budget and protected-surface sections remain intact.
- Pyright config must be portable across clean clones and local machines.
- Hardening PRs target `codex/code-hardening-suite`, not `main`.

Breaking changes that require a new or amended contract:

- making Pyright findings fail CI
- requiring zero Pyright findings for submitter or deployer readiness
- switching to npm/npx/package-lock as the primary toolchain
- excluding `src/mythic_edge_parser` from analysis
- broad source annotations or refactors to satisfy Pyright
- changing parser/runtime/workbook/App Script behavior because of Pyright
- adding content secret scanning or generated artifact scanning to this module

## Tests And Validation Required

Contract-writer validation:

```powershell
git diff --check
```

Minimum implementation validation:

```powershell
git diff --check
py -m pytest -q
py -m ruff check src tests tools
pyright --project pyrightconfig.json
```

Interpretation:

- `git diff --check`, tests, and Ruff must pass unless failures are clearly
  pre-existing and documented.
- `pyright --project pyrightconfig.json` must run and produce an advisory
  result.
- A nonzero Pyright exit due to findings is allowed in the first rollout if the
  baseline records it.
- A Pyright command/config/install failure is not allowed.

Protected-surface validation expected for hardening implementation:

```powershell
py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Expected focused checks:

- confirm `pyrightconfig.json` exists and includes source analysis
- confirm Pyright dependency is reproducible from dev setup
- confirm Pyright is not a required/failing CI gate
- confirm default `tools/run_repo_checks.ps1` behavior is not changed to fail
  on Pyright findings
- confirm baseline/report summarizes findings instead of requiring cleanup
- confirm no parser/runtime/workbook/App Script protected behavior changed

If optional non-blocking CI is added, Codex E/F should verify the workflow step
is non-blocking before treating the PR as ready.

## Future Escalation Criteria

Pyright may become a required CI gate only through a future issue and contract.

Minimum criteria before escalation:

- Pyright advisory rollout has landed on the hardening branch.
- Invocation and config are reproducible from a clean clone.
- Baseline findings are categorized.
- `tooling_config_blocker` findings are resolved.
- Remaining findings are either fixed, explicitly accepted with rationale, or
  converted into follow-up issues.
- No broad excludes hide important parser/runtime source.
- CI has run the advisory step or local equivalent long enough to prove it is
  stable and understandable.
- Required tests, Ruff, and protected-surface gate remain green.
- The PR template drift budget and protected-surface gate continue to require
  issue/contract citations for protected behavior changes.
- The user explicitly approves making Pyright required.

Possible escalation path:

1. Advisory local command.
2. Optional non-blocking CI report.
3. Warning budget or finding-count budget with accepted baseline.
4. Required CI only after baseline cleanup and explicit contract approval.

## Open Questions

- Whether tests should remain included in first Pyright analysis or be deferred
  if test-only typing noise overwhelms source findings.
- Whether a dedicated wrapper is worth adding or whether the raw `pyright`
  command is clearer.
- Whether a future baseline file is useful after the first implementation
  handoff/report, or whether it would create noisy drift.
- How strict future required mode should become after advisory cleanup.
- Whether missing type stubs should be fixed through dependencies, stubs,
  local type narrowing, or accepted advisory notes.

## Acceptance Criteria

- `docs/contracts/code_hardening_pyright_advisory.md` exists.
- The contract defines Pyright as advisory/report-oriented for the first
  rollout.
- The contract names `pyrightconfig.json` as the first configuration location.
- The contract defines a reproducible local invocation strategy.
- The contract allows recording current findings without requiring them all to
  be fixed.
- The contract defines baseline/report policy and finding categories.
- The contract explicitly forbids making Pyright a required/failing CI gate in
  the first rollout.
- The contract preserves parser/runtime/workbook/App Script protected surfaces.
- The contract defines stop conditions and future escalation criteria.
- The contract routes next work to Codex C on `codex/code-hardening-suite`.

## Handoff Packet

Role performed: Codex B: Module Contract Writer.

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/45

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Contract produced: `docs/contracts/code_hardening_pyright_advisory.md`

Risk tier: Medium.

Owning truth layer: repository coordination and code hardening.

Public interface:

- `pyrightconfig.json`
- `pyright --project pyrightconfig.json`
- first baseline/report in
  `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`

Invariants:

- Pyright findings are advisory in the first rollout.
- Existing tests, protected-surface gate, and Ruff remain required gates.
- Parser truth stays in parser/state.
- Protected surfaces require issue/contract authority before behavior changes.
- Hardening PRs target `codex/code-hardening-suite`, not `main`.

Required tests and validation:

- `git diff --check`
- `py -m pytest -q`
- `py -m ruff check src tests tools`
- `pyright --project pyrightconfig.json`, interpreted as advisory
- `py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite`

Acceptance criteria: listed above.

Open questions or contract risks: listed above.

Next recommended thread role: Codex C: Module Implementer / comparison thread.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for https://github.com/Tahjali11/Mythic-Edge/issues/45.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target:
codex/code-hardening-suite

Use:
- docs/agent_constitution.md
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/code_hardening_pyright_advisory.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- pyproject.toml
- .github/workflows/repo-checks.yml
- tools/run_repo_checks.ps1
- .github/pull_request_template.md
- issue #33
- issue #45
- issue #34 / PR #37 protected-surface diff gate context
- issue #39 / PR #42 drift-budget context

Goal:
Compare the current repo tooling and hardening surfaces against docs/contracts/code_hardening_pyright_advisory.md. Implement only the smallest report-oriented Pyright advisory rollout needed to satisfy the contract, then produce docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md.

Before editing, briefly state:
- what Pyright advisory checking is supposed to do
- what the repo is currently doing
- whether the gap is missing config, missing dependency, missing report evidence, CI ambiguity, or contract ambiguity
- the exact minimal implementation plan

Do:
- Keep Pyright advisory/report-oriented.
- Add reproducible Pyright config and invocation only as required by the contract.
- Record baseline findings without requiring all findings to be fixed.
- Keep existing tests, protected-surface gate, and Ruff as the required gates.
- Preserve parser/runtime/workbook/App Script protected surfaces.
- Fill the implementation handoff with command output summaries, finding categories, validation, remaining risks, and next recommended role.

Do not:
- Make Pyright a required/failing CI gate.
- Require zero Pyright findings.
- Run broad typing refactors.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Switch to npm/npx/package-lock as the primary toolchain unless routed back through a contract update.
- Target main.
- Mark tracker #33 complete.
- Stage or commit unless explicitly asked.

Validation:
git diff --check
py -m pytest -q
py -m ruff check src tests tools
pyright --project pyrightconfig.json
py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/45"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/code_hardening_pyright_advisory.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not make Pyright a required/failing CI gate."
    - "Do not require zero Pyright findings in the first rollout."
    - "Do not run broad typing refactors."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not switch to npm/npx/package-lock as the primary toolchain unless routed back through a contract update."
    - "Do not target main; hardening PR work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
