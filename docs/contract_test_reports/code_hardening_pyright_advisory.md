# Code Hardening Pyright Advisory Contract-Test Report

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/45

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch reviewed: `codex/code-hardening-suite`

## Source Artifacts

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`
- `pyproject.toml`
- `pyrightconfig.json`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `.github/pull_request_template.md`
- `tools/check_protected_surfaces.py`

## Role Performed

Codex E: Module Reviewer / contract-test thread.

## Findings

No blocking findings.

The Codex C implementation satisfies the Pyright advisory contract. Pyright is
reproducible through the Python `pyright` package, configured in basic advisory
mode over `src` and `tests`, and remains outside the required CI and default
local repo-check gates. Existing Pyright findings are recorded as advisory
baseline data, not as submit-blocking failures.

## Confirmed Contract Matches

- `pyproject.toml` adds `pyright>=1.1,<2` to the Python dev optional dependency
  group.
- No npm, npx, `package.json`, `package-lock.json`, pnpm lockfile, or yarn
  lockfile was introduced.
- `pyrightconfig.json` exists and includes `src` and `tests`.
- `pyrightconfig.json` uses `typeCheckingMode: basic`.
- `pyrightconfig.json` targets `pythonVersion: 3.11`.
- `pyrightconfig.json` has no local absolute paths.
- `pyrightconfig.json` excludes only local/generated/private artifact paths and
  does not broadly exclude parser/runtime source.
- `.github/workflows/repo-checks.yml` still runs required tests, the protected
  surface gate on pull requests, and Ruff; it does not run Pyright.
- `tools/run_repo_checks.ps1` still runs tests and Ruff by default; it does not
  run Pyright.
- `.github/pull_request_template.md` retains the drift-budget section and
  protected-surface disclosure expectations.
- `tools/check_protected_surfaces.py` is unchanged and continues to classify
  protected source/workflow surfaces while failing only forbidden artifacts or
  gate errors.
- No parser/runtime code, workbook schema, webhook payload shape, Apps Script
  behavior, parser event classes, match/game identity, deduplication, secrets,
  environment variables, raw logs, generated data, runtime status files, failed
  posts, or workbook exports changed in this implementation pass.

## Contract Mismatches

None found.

## Advisory Pyright Baseline Verification

Command:

```powershell
pyright --project pyrightconfig.json
```

Observed result:

```text
exit code: 1
60 errors
5 warnings
0 information
```

This is accepted advisory output under the issue #45 contract. The command ran
and produced findings; zero findings is not required in this rollout.

Representative categories match the implementation handoff:

- `likely_interface_drift`
- `optional_or_none_risk`
- `dynamic_payload_boundary`
- `missing_type_information`
- `test_typing_noise`
- `false_positive_or_needs_triage`

No finding was fixed during review, and no broad typing refactor was performed.

## Non-Blocking Residual Risks

- Pyright prints a trailing Windows environment warning:
  `Python was not found; run without arguments to install from the Microsoft Store...`
  The advisory report still completes, so this is not a tooling/config blocker,
  but it is worth noting as a future local-environment cleanup item.
- The contract's observed-state section says `docs/agent_rules.yml` was absent
  on the inspected branch. It is now present. This is stale narrative context,
  not a functional mismatch in the Pyright rollout.
- Because `pyright` now lives in the dev optional dependency group, CI installs
  it when installing `.[dev]`, even though CI does not run it. This matches the
  reproducible dependency strategy, but a future package-resolution issue would
  affect dev dependency installation rather than a Pyright findings gate.
- Current Pyright findings are intentionally not triaged to zero. Follow-up
  work should use new issues/contracts before touching protected parser,
  runtime, workbook, webhook, Apps Script, identity, dedupe, or reconciliation
  behavior.

## Drift Classification

- Repo tooling drift: authorized by issue #45 and the Pyright advisory contract.
- Parser/runtime behavior drift: none found.
- Workbook schema drift: none found.
- Webhook payload shape drift: none found.
- Apps Script drift: none found.
- Parser event class drift: none found.
- Match/game identity drift: none found.
- Deduplication drift: none found.
- Secret/local artifact drift: none found.
- Tracker drift: tracker #33 remains open; this review did not mark it complete.

## Validation

```powershell
git diff --check
```

Result:

```text
passed with no whitespace-error output
```

PowerShell emitted a non-failing CRLF normalization warning for
`pyproject.toml`.

```powershell
py -m pytest -q
```

Result:

```text
369 passed in 3.52s
```

```powershell
py -m ruff check src tests tools
```

Result:

```text
All checks passed!
```

```powershell
pyright --project pyrightconfig.json
```

Result:

```text
exit code: 1
60 errors
5 warnings
0 information
```

This is accepted advisory baseline output, not a required/failing gate.

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

Additional worktree-path protected-surface check:

```powershell
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Result:

```text
changed_paths: 5
forbidden: 0
warnings: 0
result: passed
```

## Recommendation

Approve this contract-test pass and route to Codex F: Module Submitter.

Rationale: no blocking findings remain, required tests and Ruff pass, Pyright
is advisory and reproducible, the baseline is recorded honestly, and protected
surfaces remain unchanged.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for https://github.com/Tahjali11/Mythic-Edge/issues/45.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Goal:
Submit the Pyright advisory type-checking hardening work as a draft PR targeting codex/code-hardening-suite. Do not target main, merge, close issue #45, or mark tracker #33 complete.

Source artifacts:
- docs/contracts/code_hardening_pyright_advisory.md
- docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md
- docs/contract_test_reports/code_hardening_pyright_advisory.md
- pyproject.toml
- pyrightconfig.json
- .github/workflows/repo-checks.yml
- tools/run_repo_checks.ps1
- .github/pull_request_template.md
- tools/check_protected_surfaces.py

Reviewer result:
- No blocking findings.
- Pyright remains advisory and is not a required/failing CI gate.
- Zero Pyright findings is not required.
- The dependency strategy uses the Python pyright package.
- pyrightconfig.json includes src and tests, uses basic mode, targets Python 3.11, avoids local absolute paths, and does not broadly exclude parser/runtime source.
- CI and default local repo checks still run required tests/gates/Ruff only.
- Baseline findings are summarized honestly without broad typing refactors.
- Protected surfaces were preserved.

Before submitting:
1. Inspect git status and the full diff.
2. Stage only issue #45 files.
3. Confirm no npm/npx/package-lock files, raw logs, generated data, runtime status files, failed posts, workbook exports, secrets, or unrelated local artifacts are included.
4. Run:
   git diff --check
   py -m pytest -q
   py -m ruff check src tests tools
   pyright --project pyrightconfig.json
   py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
5. Treat Pyright findings as advisory baseline output, not a failing gate.

Final handoff must include:
- role performed
- issue and tracker
- branch name
- PR URL
- files committed
- validation result
- Pyright advisory baseline summary
- forbidden/protected-surface confirmation
- residual risks
- next recommended role
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/45"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/code_hardening_pyright_advisory.md"
  reviewed_artifacts:
    - "docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md"
    - "pyproject.toml"
    - "pyrightconfig.json"
    - ".github/workflows/repo-checks.yml"
    - "tools/run_repo_checks.ps1"
    - ".github/pull_request_template.md"
    - "tools/check_protected_surfaces.py"
  produced_artifact: "docs/contract_test_reports/code_hardening_pyright_advisory.md"
  branch: "codex/code-hardening-suite"
  recommendation: "approve and submit"
  validation:
    - "git diff --check -> passed with non-failing CRLF warning for pyproject.toml"
    - "py -m pytest -q -> 369 passed in 3.52s"
    - "py -m ruff check src tests tools -> All checks passed!"
    - "pyright --project pyrightconfig.json -> exit 1, 60 errors, 5 warnings; accepted advisory baseline"
    - "py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed"
    - "worktree paths piped to protected-surface gate -> passed"
  stop_conditions:
    - "Do not make Pyright a required/failing CI gate."
    - "Do not require zero Pyright findings."
    - "Do not run broad typing refactors."
    - "Do not change protected parser/runtime/workbook/App Script surfaces."
    - "Do not switch to npm/npx/package-lock as the primary toolchain."
    - "Do not target main."
    - "Do not mark tracker #33 complete."
```
