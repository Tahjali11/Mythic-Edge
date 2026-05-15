# Code Hardening Pyright Advisory Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/45

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

`docs/contracts/code_hardening_pyright_advisory.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

This pass compared the current hardening/tooling surfaces against the Pyright
advisory contract, added the smallest reproducible advisory rollout, and
recorded the first baseline. Work stayed on `codex/code-hardening-suite`.

## What Pyright Advisory Checking Is Supposed To Do

Pyright is supposed to be a type-risk flashlight for the first rollout, not a
hammer. It should make type and interface risks visible from a clean dev setup,
while existing tests, Ruff, and the protected-surface gate remain the required
checks.

Plain English: this adds a way to ask "what would a type checker worry about?"
without pretending every finding must be fixed today.

## Current Behavior Before This Pass

- `pyproject.toml` had pytest, pytest-cov, and Ruff in the `dev` optional
  dependency group.
- `pyrightconfig.json` did not exist.
- `pyright` was not importable/runnable through the local Python environment.
- `.github/workflows/repo-checks.yml` ran tests, protected-surface gate, and
  Ruff; it did not run Pyright.
- `tools/run_repo_checks.ps1` ran tests and Ruff; it did not run Pyright.
- No `package.json`, `package-lock.json`, pnpm lockfile, or yarn lockfile was
  present.

One contract observation is now stale: the contract says `docs/agent_rules.yml`
was not present on the inspected branch, but this branch now has
`docs/agent_rules.yml`. This did not require a code change.

## What Changed

Implemented the minimal local advisory rollout:

- Added `pyright>=1.1,<2` to `[project.optional-dependencies].dev` in
  `pyproject.toml`.
- Added `pyrightconfig.json` with:
  - `include`: `src`, `tests`
  - local/generated artifact excludes
  - `pythonVersion`: `3.11`
  - `typeCheckingMode`: `basic`
- Installed the updated dev environment locally with `py -m pip install -e .[dev]`.
- Ran `pyright --project pyrightconfig.json` and recorded the advisory
  baseline in this handoff.

No wrapper script, CI step, or default repo-check integration was added.

## Contract Matches

- Pyright remains advisory and report-oriented.
- Zero Pyright findings is not required.
- Pyright is not added to `.github/workflows/repo-checks.yml`.
- Pyright is not added to the default `tools/run_repo_checks.ps1` sequence.
- The first dependency strategy uses the Python `pyright` package in
  `pyproject.toml`.
- No npm, npx, `package.json`, or package lockfile was introduced.
- `pyrightconfig.json` exists and includes both `src` and `tests`.
- The config targets Python `3.11`, matching the project minimum.
- The config uses `basic` type checking.
- The config excludes local/generated artifact areas without excluding
  `src/mythic_edge_parser`.
- No local absolute machine paths are committed in the config.
- Existing required gates remain tests, Ruff, and the protected-surface gate.
- Parser/runtime/workbook/App Script protected surfaces were not changed.

## Contract Mismatches

No blocking contract mismatch remains after this pass.

The comparison found missing first-rollout artifacts (`pyrightconfig.json` and
the reproducible Python dev dependency). Both were added.

## Advisory Pyright Baseline

Command:

```powershell
pyright --project pyrightconfig.json
```

Result:

```text
exit code: 1
111 files analyzed
60 errors
5 warnings
0 information
```

This is accepted advisory baseline output for the first rollout. The nonzero
exit is from type findings, not an invalid config or command failure.

Summary by Pyright rule:

```text
error reportArgumentType: 31
error reportAttributeAccessIssue: 17
error reportMissingImports: 9
warning reportMissingModuleSource: 5
error reportOptionalMemberAccess: 2
error reportOperatorIssue: 1
```

Top files by finding count:

```text
tests/test_collection_parser.py: 12
src/mythic_edge_parser/app/arena_id_validation.py: 10
src/mythic_edge_parser/app/runner.py: 5
src/mythic_edge_parser/app/analytics_sidecar.py: 4
tests/test_tier_sync.py: 3
tests/test_app_outputs.py: 3
src/mythic_edge_parser/app/grp_id_candidates.py: 3
src/mythic_edge_parser/app/tier_sync.py: 2
src/mythic_edge_parser/app/card_catalog.py: 2
tests/test_stream_unit.py: 2
```

Representative categories:

- `likely_interface_drift`: callback and interface-shape findings in
  `runner.py`, `analytics_sidecar.py`, parser/router dispatch code, and several
  tests.
- `optional_or_none_risk`: `int(...)` and optional member findings around
  optional payload values and optional paths.
- `dynamic_payload_boundary`: `Any` / `Unknown` values at parser payload,
  card-ID, and runtime-artifact boundaries.
- `missing_type_information`: missing or unresolved third-party import
  information for `pytest`, `requests`, and `bs4`.
- `test_typing_noise`: fake sessions, fake routers/tailers, fixture shapes,
  and test assertions that are runtime-valid but static-type noisy.
- `false_positive_or_needs_triage`: findings that may be safe but need later
  human or module-specific review.

No `protected_surface_fix_required` change was made. If any baseline finding
requires protected parser/runtime/workbook/App Script behavior changes, it must
be routed through a future issue and contract.

Note: the Pyright command also printed this environment message after the
report:

```text
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App Execution aliases.
```

The command still produced a complete report and summary. Reviewer should decide
whether this is a non-blocking environment warning or a future
tooling/config follow-up. It did not prevent the advisory rollout from running.

## Files Changed

- `pyproject.toml`
- `pyrightconfig.json`
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`

Pre-existing source artifact:

- `docs/contracts/code_hardening_pyright_advisory.md` was already present as an
  untracked source artifact before this C-thread work began.

## Code Changed

No parser/runtime code changed.

Tooling/config changed:

- `pyproject.toml`: added the Python `pyright` dev dependency.
- `pyrightconfig.json`: added first advisory Pyright configuration.

## Tests Added Or Updated

None.

No test behavior changed.

## Interface Changes

Added advisory tooling interfaces:

- `pyrightconfig.json`
- `pyright --project pyrightconfig.json`
- Python dev dependency: `pyright>=1.1,<2`

No function signatures, parser event classes, parser payload shapes, workbook
columns, webhook payloads, Apps Script entrypoints, environment variable
semantics, runtime status files, match/game identity, deduplication behavior,
or final reconciliation behavior changed.

## Validation Run

Local dev install:

```powershell
py -m pip install -e .[dev]
```

Result:

```text
Successfully installed mythic-edge-parser-0.1.0 nodeenv-1.10.0 pyright-1.1.409
```

Pyright availability:

```powershell
pyright --version
py -m pyright --version
```

Result:

```text
pyright 1.1.409
pyright 1.1.409
```

Advisory Pyright baseline:

```powershell
pyright --project pyrightconfig.json
```

Result:

```text
exit code: 1
111 files analyzed
60 errors
5 warnings
0 information
```

Required tests:

```powershell
py -m pytest -q
```

Result:

```text
369 passed in 3.61s
```

Required lint:

```powershell
py -m ruff check src tests tools
```

Result:

```text
All checks passed!
```

Diff whitespace:

```powershell
git diff --check
```

Result:

```text
passed with no whitespace-error output
```

PowerShell also printed this non-failing line-ending warning:

```text
warning: in the working copy of 'pyproject.toml', CRLF will be replaced by LF the next time Git touches it
```

Protected-surface gate, committed diff mode:

```powershell
py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Result:

```text
changed_paths: 0
forbidden: 0
warnings: 0
result: passed
```

Protected-surface gate, current worktree paths via stdin:

```powershell
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Result:

```text
changed_paths: 3
forbidden: 0
warnings: 0
result: passed
```

## Protected Scope Confirmation

This pass did not change parser behavior, parser state final reconciliation,
workbook schema, webhook payload shape, Apps Script behavior, parser event
classes, match/game identity, deduplication, secrets, environment variables,
raw logs, generated data, runtime status files, failed posts, or workbook
exports.

Pyright was not made a required or failing CI gate, and zero Pyright findings
was not made an acceptance criterion.

## Still Unverified

- CI was not run in GitHub.
- No optional non-blocking CI advisory step was added or verified.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Pyright findings were not fixed, by design.
- The trailing Pyright environment message about `Python was not found` was not
  investigated beyond confirming the report still runs.
- `docs/agent_rules.yml` now exists despite the contract's observed-current-
  state note that it was absent; this is repo drift in the contract narrative,
  not a blocker for the Pyright advisory rollout.

## Reviewer Focus

Ask Codex E to focus on:

- whether adding `pyright>=1.1,<2` to `pyproject.toml` satisfies the
  reproducible dependency requirement without introducing a Node/npm toolchain
- whether `pyrightconfig.json` includes enough source/test coverage and avoids
  broad parser/runtime excludes
- whether keeping CI and `tools/run_repo_checks.ps1` unchanged correctly
  preserves advisory-only behavior
- whether the Pyright baseline categorization is honest and actionable
- whether the trailing `Python was not found` message should be treated as a
  non-blocking environment warning or a tooling/config follow-up
- whether `docs/agent_rules.yml` being present now should route back to Codex B
  for a contract note update or remain a harmless observed-state drift

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer / contract-test thread for https://github.com/Tahjali11/Mythic-Edge/issues/45.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Review:
- docs/contracts/code_hardening_pyright_advisory.md
- docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md
- pyproject.toml
- pyrightconfig.json
- .github/workflows/repo-checks.yml
- tools/run_repo_checks.ps1
- .github/pull_request_template.md
- tools/check_protected_surfaces.py

Goal:
Verify that the Codex C implementation satisfies the Pyright advisory contract while keeping Pyright advisory-only and preserving parser/runtime/workbook/App Script protected surfaces.

Focus on:
- Pyright remains advisory, not a required/failing CI gate
- zero Pyright findings is not required
- the dependency strategy uses the Python `pyright` package, not npm/npx/package-lock
- `pyrightconfig.json` includes `src` and `tests`, uses basic mode, targets Python 3.11, avoids local absolute paths, and does not broadly exclude parser/runtime source
- CI and default local repo checks still run only required tests/gates/Ruff
- baseline findings are summarized honestly without broad typing refactors
- protected-surface validation and drift-budget expectations are preserved

Do not implement changes during review unless explicitly asked. Lead with findings, ordered by severity. If there are no blocking findings, say so clearly and identify any non-blocking residual risks.

Validation to consider:
git diff --check
py -m pytest -q
py -m ruff check src tests tools
pyright --project pyrightconfig.json
py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite

Do not make Pyright a required/failing CI gate. Do not require zero Pyright findings. Do not run broad typing refactors. Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports. Do not switch to npm/npx/package-lock as the primary toolchain unless routed back through a contract update. Do not target main or mark tracker #33 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/45"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/code_hardening_pyright_advisory.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "py -m pip install -e .[dev] -> installed pyright 1.1.409"
    - "pyright --version -> pyright 1.1.409"
    - "pyright --project pyrightconfig.json -> exit 1, 111 files analyzed, 60 errors, 5 warnings; accepted advisory baseline"
    - "py -m pytest -q -> 369 passed in 3.61s"
    - "py -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed with no whitespace-error output; non-failing CRLF warning for pyproject.toml"
    - "py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite -> changed_paths 0, passed"
    - "worktree paths piped to protected-surface gate -> changed_paths 3, passed"
  stop_conditions:
    - "Do not make Pyright a required/failing CI gate."
    - "Do not require zero Pyright findings in the first rollout."
    - "Do not run broad typing refactors."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not switch to npm/npx/package-lock as the primary toolchain unless routed back through a contract update."
    - "Do not target main; hardening PR work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
