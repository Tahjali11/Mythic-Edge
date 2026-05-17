# Repo-Wide Pyright Advisory Report Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/98

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch target: `codex/repo-wide-hardening-run`

Related earlier policy issue: https://github.com/Tahjali11/Mythic-Edge/issues/45

Previous repo-wide hardening item:

- Issue #96 / PR #97 drift detector baseline first pass merged into
  `codex/repo-wide-hardening-run` at
  `5fdc433e06554c809533ea49391d6441fecc03a2`.
- Issue #96 remains open intentionally per lifecycle stop condition.
- Tracker #82 remains open.

Agent docs read:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Pyright and repo-wide hardening artifacts read:

- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`
- `docs/contract_test_reports/code_hardening_pyright_advisory.md`
- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md`
- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`
- `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`
- `docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`

Tooling surfaces read:

- `pyproject.toml`
- `pyrightconfig.json`
- `tools/run_pyright_advisory.ps1`
- `tools/select_validation.py`
- `.github/workflows/repo-checks.yml`

This is a contract-writing artifact only. It does not implement code, edit
Pyright config, edit wrappers, edit the selector, edit CI, change parser or
runtime behavior, target `main`, close #96, or mark tracker #82 complete.

## Module

Repo-wide Pyright advisory report artifact.

Plain English: Pyright is useful engineering evidence, but it is not a
production gate in Mythic Edge. This contract defines how future threads should
produce a stable advisory Pyright summary so local resolver noise, real type
findings, and tooling/config blockers are not mixed together in handoffs.

## Owning Layer

Owning layer: repo-wide hardening validation/reporting tooling.

Truth boundary:

- Pyright reports static type-checking evidence.
- Pyright output does not own parser truth, parser event interpretation,
  match/game identity, workbook schema truth, webhook payload truth, Apps
  Script behavior, or deploy readiness.
- Parser and state interpretation remain the truth owners for parser-managed
  match and game facts.
- Existing tests, Ruff, protected-surface checks, issue scope, contract scope,
  Codex E review, Codex F submission, and Codex G deployer gates remain the
  normal readiness evidence.
- A Pyright advisory report may identify follow-up risk. It must not silently
  authorize behavior changes or protected-surface changes.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_pyright_advisory_report.md`

Expected future Codex C implementation or comparison artifact:

- `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`

Expected future Codex E review or contract-test report:

- `docs/contract_test_reports/repo_wide_pyright_advisory_report.md`

Recommended future implementation files, if Codex C confirms the current repo
still matches issue #98:

- `tools/run_pyright_advisory_report.py`
- `tests/test_pyright_advisory_report.py`
- narrow updates to `tools/select_validation.py`
- narrow updates to `tests/test_select_validation.py`

Optional future compatibility surface:

- `tools/run_pyright_advisory.ps1`, only to delegate to the report helper or
  preserve a Windows shortcut. The first implementation does not need to change
  this file if the cross-platform helper and selector recommendation are
  sufficient.

Referenced but not owned by this contract:

- `pyproject.toml`
- `pyrightconfig.json`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `.github/pull_request_template.md`
- parser, runtime, workbook, webhook, and Apps Script source files whose type
  findings may be summarized but must not be changed under this contract

This contract does not authorize changing Pyright's type-checking posture,
dependency strategy, CI gate behavior, parser behavior, workbook schema,
webhook payload shape, Apps Script behavior, or protected runtime surfaces.

## Observed Current Behavior

Observed on `codex/repo-wide-hardening-run` during this Codex B pass:

- The branch is even with `origin/codex/repo-wide-hardening-run`.
- Issue #98 is open and names this contract as the expected next artifact.
- Tracker #82 is open and names Pyright advisory report artifact as the next
  queue item after #96 / PR #97.
- `pyright>=1.1,<2` is present in `[project.optional-dependencies].dev` in
  `pyproject.toml`.
- `pyrightconfig.json` exists.
- `pyrightconfig.json` includes `src` and `tests`, excludes local/generated
  artifact paths, targets Python `3.11`, and uses `typeCheckingMode: basic`.
- `.github/workflows/repo-checks.yml` installs `.[dev]`, runs tests, runs the
  protected-surface gate for pull requests, and runs Ruff. It does not run
  Pyright.
- `tools/select_validation.py` recommends `python3 -m pyright` as
  `pyright_advisory` for source, Python tooling, or dependency metadata
  changes.
- `tools/run_pyright_advisory.ps1` exists as a Windows PowerShell wrapper.
- The PowerShell wrapper resolves the active Python interpreter through the
  Windows `py` launcher and runs:

```powershell
pyright --project pyrightconfig.json --pythonpath <resolved-interpreter>
```

- The PowerShell wrapper prints the resolved interpreter path before running
  Pyright.
- The PowerShell wrapper currently exits as a failure when Pyright returns a
  nonzero exit code.

Observed current validation evidence:

- `powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1`
  ran successfully in this Codex B pass and reported
  `0 errors, 0 warnings, 0 informations`.
- `py -m pyright --version` reported `pyright 1.1.409`.
- Raw `py -m pyright` failed in this Windows shell with 19 errors and 5
  warnings, all centered on missing import source/resolution for dependencies
  such as `pytest`, `requests`, and `bs4`, followed by the Windows Store
  `python` app-execution-alias message.
- Recent repo-wide hardening handoffs and reports record the same split:
  raw `py -m pyright` is noisy in this Windows shell, while
  `tools/run_pyright_advisory.ps1` reports clean advisory output.
- The baseline repo-wide hardening report used `python3 -m pyright` on macOS
  and recorded `0 errors, 0 warnings, 0 informations`, while noting that the
  PowerShell-only wrapper was not run on macOS.

Current gap:

- Handoffs and reviews repeat the raw-vs-wrapper caveat in prose, but there is
  no stable repo-approved Pyright advisory report shape.
- There is no cross-platform report helper that resolves the active interpreter
  and renders normalized advisory fields for both Windows and macOS/Linux.
- The validation selector currently recommends the raw command without naming
  the repo-approved wrapper/report caveat.
- There is no focused test coverage for parsing/summarizing Pyright output into
  stable report categories.

## Public Interface

### Advisory Report Command

Recommended first implementation command:

```bash
python3 tools/run_pyright_advisory_report.py
```

Windows equivalent:

```powershell
py tools\run_pyright_advisory_report.py
```

Required behavior:

- Resolve the active Python interpreter from the interpreter running the helper.
- Run Pyright with the repo config and that interpreter path:

```text
pyright --project pyrightconfig.json --pythonpath <resolved-python-executable>
```

- Print a stable advisory report to stdout.
- Exit `0` when a report is produced, including reports with advisory type
  findings or local resolver noise.
- Exit `2` for tooling/config blockers that prevent a usable advisory report.
- Never become a required/failing CI gate in this issue.

Allowed arguments for the first implementation:

- `--project <path>`, default `pyrightconfig.json`
- `--repo-root <path>`, default `.`
- `--format text|json`, default `text`
- `--raw-output-lines <n>`, optional small excerpt limit if Codex C implements
  output excerpts

Not required in the first implementation:

- writing a report file
- GitHub annotations
- baseline comparison
- warning budgets
- strict mode
- CI integration

### Existing PowerShell Wrapper

Current Windows-approved command:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
```

Contract role:

- The PowerShell wrapper remains an approved Windows shortcut for current
  handoffs.
- If Codex C adds the cross-platform report helper, the PowerShell wrapper may
  remain unchanged or delegate to the helper.
- If Codex C touches the PowerShell wrapper, it must preserve advisory intent,
  avoid printing private full interpreter paths in durable report output, and
  distinguish Pyright findings from tooling/config blockers.
- Codex C must not use the wrapper change to make Pyright required or failing.

### Raw Pyright Commands

Raw commands:

```powershell
py -m pyright
py -m pyright --project pyrightconfig.json
```

```bash
python3 -m pyright
python3 -m pyright --project pyrightconfig.json
```

Contract role:

- Raw Pyright commands are supplemental evidence.
- Raw commands may be useful on macOS/Linux when they resolve the active
  environment correctly.
- Raw commands are not the preferred Windows signal when the repo-approved
  wrapper/report command is available.
- If a raw command reports only local resolver/import noise while the approved
  wrapper/report command is clean, record the raw result as
  `local_resolver_noise`, not as a blocking type regression.
- If both raw and approved commands report the same real type findings, record
  them as advisory type findings.
- If the approved command cannot run, classify the failure as a
  tooling/config blocker.

### Selector Recommendation

Current selector behavior:

- `tools/select_validation.py` recommends `python3 -m pyright`.

Required future behavior after the report helper exists:

- Recommend the repo-approved report command for `pyright_advisory`:

```bash
python3 tools/run_pyright_advisory_report.py
```

- Preserve the selector's core rule: it recommends commands, it does not run
  them, and it must not claim validation passed.
- Keep Pyright as `recommended`, not `required`, unless a future issue and
  contract explicitly escalate Pyright.
- The selector may include a reason such as:

```text
Source, hardening tool, or dependency configuration changed; run the repo-approved Pyright advisory report so type findings are separated from local resolver noise.
```

Windows users may run the equivalent:

```powershell
py tools\run_pyright_advisory_report.py
```

## Stable Report Fields

The text report must start with this heading:

```text
Pyright Advisory Report
```

Required text fields:

```text
mode: advisory
project: pyrightconfig.json
python: <normalized-python>
platform: windows|macos|linux|unknown
runner: tools/run_pyright_advisory_report.py
command: pyright --project pyrightconfig.json --pythonpath <python>
pyright_version: <version-or-unknown>
exit_code: <integer>
errors: <integer-or-unknown>
warnings: <integer-or-unknown>
information: <integer-or-unknown>
type_findings: <integer>
local_resolver_noise: <integer>
tooling_config_blockers: <integer>
status: clean|advisory_findings|local_resolver_noise|tooling_config_blocker|error
gate_behavior: advisory_non_blocking
```

Required privacy and stability rules:

- Do not print full local user paths in the stable report fields.
- Do not print usernames from resolved interpreter paths.
- Normalize the Python executable field to a safe value such as
  `<resolved-python>` or a path with user segments redacted.
- Use repo-relative paths for findings.
- Do not print raw logs, runtime status payloads, failed-post payloads,
  workbook export content, secrets, tokens, webhook URLs, or generated data.
- If output excerpts are included, keep them short and redacted.

Required optional sections when findings exist:

```text
Type Findings:
- <rule>: <count>

Local Resolver Noise:
- <category>: <count>

Tooling / Config Blockers:
- <category>: <count>
```

Allowed JSON shape, if Codex C implements `--format json`:

```json
{
  "object": "mythic_edge_pyright_advisory_report",
  "schema_version": 1,
  "mode": "advisory",
  "project": "pyrightconfig.json",
  "python": "<normalized-python>",
  "platform": "windows",
  "runner": "tools/run_pyright_advisory_report.py",
  "command": "pyright --project pyrightconfig.json --pythonpath <python>",
  "pyright_version": "1.1.409",
  "exit_code": 0,
  "summary": {
    "errors": 0,
    "warnings": 0,
    "information": 0
  },
  "classification": {
    "type_findings": 0,
    "local_resolver_noise": 0,
    "tooling_config_blockers": 0
  },
  "status": "clean",
  "gate_behavior": "advisory_non_blocking"
}
```

JSON support is useful but optional in the first implementation. Text output is
required.

## Finding Classification

### `type_findings`

Use for Pyright findings that remain after the approved advisory command runs
with the resolved active Python interpreter.

Examples:

- likely interface drift
- optional or `None` risk
- argument type mismatch
- attribute access risk on project-owned objects
- operator mismatch
- missing type information that is still visible under the approved command
- test typing noise that remains under the approved command

Interpretation:

- These are advisory findings.
- They may become follow-up issues.
- They do not require immediate fixes in this report-artifact issue.
- If fixing one would touch protected parser/runtime/workbook/webhook/App
  Script surfaces, stop and route to a new issue/contract.

### `local_resolver_noise`

Use for findings that appear in a raw invocation but disappear when the
repo-approved wrapper/report command runs with the resolved Python interpreter.

Examples:

- raw `py -m pyright` cannot resolve `pytest`, `requests`, or `bs4` in this
  Windows shell
- raw command ends with the Windows Store `python` app-execution-alias message
- raw command uses a different environment than the active project interpreter

Interpretation:

- Record the noise honestly.
- Do not treat it as a parser/type regression when the approved command is
  clean.
- Do not hide it in handoffs; name it so reviewers understand why raw output
  and wrapper output differ.
- If raw noise becomes confusing enough to block reviews, route to a future
  tooling issue rather than changing parser code.

### `tooling_config_blocker`

Use when the approved advisory report cannot produce useful Pyright evidence.

Examples:

- Pyright is not installed after documented dev setup.
- `pyrightconfig.json` is unreadable or invalid.
- the helper cannot resolve an active Python interpreter
- the helper cannot locate the repo root or config
- the helper cannot run Pyright at all
- the config broadly excludes `src` or all useful project code

Interpretation:

- This is a blocker for Codex C/E on this issue.
- Fixing it may be in scope only if it is a narrow reporting/tooling change.
- If resolving it requires changing dependency strategy, type-checking posture,
  CI behavior, or parser/runtime behavior, route back to Codex B or A.

## Advisory-Only Posture

Required guarantees:

- Pyright remains advisory.
- Existing tests, Ruff, protected-surface checks, secret/private-marker checks,
  surface authorization checks, selector output, contract review, and PR/deploy
  gates remain the normal readiness evidence.
- Zero Pyright findings is not required for this issue.
- A report with `status: advisory_findings` is allowed when the command ran and
  findings are categorized.
- A report with `status: local_resolver_noise` is allowed when the approved
  command is clean and raw command noise is documented.
- A report with `status: tooling_config_blocker` must route to fixing or
  follow-up before submitter work.
- Pyright findings do not authorize broad type cleanup or parser behavior
  changes.
- Pyright must not become required or failing in CI under this issue.
- Pyright must not become a merge/deploy gate under this issue.

Future escalation to required CI or zero-finding budgets requires a separate
issue, contract, review, and explicit user approval.

## Cross-Platform Command Expectations

Windows preferred commands:

```powershell
py tools\run_pyright_advisory_report.py
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
```

macOS/Linux preferred command:

```bash
python3 tools/run_pyright_advisory_report.py
```

Fallback supplemental raw commands:

```powershell
py -m pyright --project pyrightconfig.json
```

```bash
python3 -m pyright --project pyrightconfig.json
```

Rules:

- Handoffs should prefer the repo-approved report command once it exists.
- Raw commands may be listed as supplemental local evidence.
- If macOS/Linux cannot run the Python helper but raw `python3 -m pyright`
  remains clean, Codex C must record that portability gap and route if needed.
- Do not introduce npm, npx, `package.json`, or package lockfiles as the
  primary Pyright path under this contract.

## Report Storage Policy

First implementation storage:

- Print the stable report to stdout.
- Record the stable report summary in the Codex C implementation handoff.
- Codex E records review findings in its contract-test report.

Not authorized in the first implementation:

- committing generated Pyright output files
- writing reports under `data/`
- writing reports under runtime status paths
- writing reports under failed-post, generated data, workbook export, or raw
  log paths
- adding a persistent baseline file for Pyright output
- adding CI-uploaded artifacts

Allowed future option:

- A later issue may add optional local ignored output such as `.tmp/` for
  reviewer convenience, but this contract does not require or authorize
  committing generated report files.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event classes
- event kind values
- parser payload shape
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- live workbook state
- deployed Apps Script state
- secrets, credentials, environment variables, API keys, tokens, or webhook
  URLs
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports
- local-only artifacts
- production behavior
- CI required/failing gate behavior
- Pyright strictness or type-checking mode
- Pyright dependency strategy beyond the existing Python-package strategy
- merge-to-main policy

Allowed future implementation surfaces under this exact contract:

- `tools/run_pyright_advisory_report.py`
- `tests/test_pyright_advisory_report.py`
- narrow `tools/select_validation.py` command text update
- narrow `tests/test_select_validation.py` expectation update
- optional `tools/run_pyright_advisory.ps1` delegation/compatibility update
- `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`
- `docs/contract_test_reports/repo_wide_pyright_advisory_report.md`

Any required change outside these surfaces must route back to Codex B or A.

## Error Behavior

If the approved report helper cannot import or run:

- report `status: error` if possible
- exit `2`
- do not claim Pyright evidence was produced

If Pyright is missing:

- classify as `tooling_config_blocker`
- exit `2`
- recommend verifying `py -m pip install -e .[dev]` or equivalent dev setup

If `pyrightconfig.json` is missing or invalid:

- classify as `tooling_config_blocker`
- exit `2`
- do not create a new Pyright config under this issue unless Codex B explicitly
  amends the contract

If the approved command produces type findings:

- classify findings as `type_findings`
- print `status: advisory_findings`
- exit `0`
- do not require fixes in this issue

If the raw command is noisy but the approved command is clean:

- classify raw-only noise as `local_resolver_noise`
- print or record the distinction in the handoff
- do not treat the raw command as a blocking failure

If the report would need to print private local paths:

- redact or normalize them
- never include full user directory segments in durable report output

## Side Effects

Allowed side effects in this Codex B thread:

- create `docs/contracts/repo_wide_pyright_advisory_report.md`

Forbidden side effects in this Codex B thread:

- no code implementation
- no wrapper edits
- no selector edits
- no tests
- no CI edits
- no Pyright config changes
- no parser/runtime/workbook/webhook/App Script behavior changes
- no generated report files
- no PR creation
- no issue closure
- no tracker closure

Allowed side effects in future Codex C implementation, if this contract is the
active source artifact:

- add a cross-platform report helper
- add focused tests for report parsing/classification
- update selector command text to recommend the repo-approved helper
- optionally update the PowerShell wrapper as a compatibility shortcut
- write the implementation handoff

## Validation Requirements

Contract-writer validation for this Codex B pass:

```powershell
git diff --check
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_pyright_advisory_report.md
'@ | py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
docs/contracts/repo_wide_pyright_advisory_report.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
docs/contracts/repo_wide_pyright_advisory_report.md
'@ | py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\contracts\repo_wide_pyright_advisory_report.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_pyright_advisory_report.md
'@ | py tools\select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
py tools\check_agent_docs.py
```

Observed Pyright context commands for this Codex B pass:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
py -m pyright --version
py -m pyright
```

Focused Codex C validation:

```powershell
git status --short --branch
py -m pytest -q tests\test_pyright_advisory_report.py tests\test_select_validation.py
py tools\run_pyright_advisory_report.py
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
py -m ruff check src tests tools
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-98.md --authorization-file contract=docs\contracts\repo_wide_pyright_advisory_report.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_pyright_advisory_report_comparison.md
git diff --check
```

macOS/Linux Codex C or laptop validation, when available:

```bash
python3 tools/run_pyright_advisory_report.py
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
python3 -m pytest -q tests/test_pyright_advisory_report.py tests/test_select_validation.py
python3 -m ruff check src tests tools
```

Before Codex F submits a PR:

```powershell
py -m pytest -q tests
py -m ruff check src tests tools
py tools\run_pyright_advisory_report.py
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

Interpretation:

- `run_pyright_advisory_report.py` producing `status: clean`,
  `status: advisory_findings`, or `status: local_resolver_noise` is acceptable
  for this issue if the report is well formed and honest.
- `status: tooling_config_blocker` or `status: error` must be fixed or routed
  before submitter work.
- Full tests and Ruff remain required before submitter work if Python tooling
  changes.
- GitHub Actions remain submitter/deployer evidence and must not include a new
  Pyright failing gate from this issue.

## Acceptance Criteria

- `docs/contracts/repo_wide_pyright_advisory_report.md` exists.
- The contract links issue #98, tracker #82, and earlier Pyright advisory issue
  #45.
- The contract preserves the advisory-only Pyright posture.
- The contract distinguishes raw Pyright commands from the repo-approved
  wrapper/report behavior.
- The contract chooses the smallest coherent future implementation path:
  cross-platform advisory report helper plus narrow selector command update.
- Stable text report fields are defined.
- Optional JSON report fields are defined as additive.
- Type findings, local resolver noise, and tooling/config blockers are
  distinguished.
- Windows and macOS/Linux command expectations are defined.
- The relationship to `tools/select_validation.py` is explicit.
- Validation evidence for Codex C/E/F is defined.
- Protected surfaces and out-of-scope gate changes are named.
- The contract does not implement code, edit CI, make Pyright required/failing,
  change parser/runtime/workbook/webhook/App Script behavior, target `main`,
  close #96, or mark tracker #82 complete.
- The contract routes next work to Codex C.

## Unknowns

- Whether the PowerShell wrapper should delegate to the new Python helper or
  remain a separate Windows shortcut.
- Whether JSON output is worth adding in the first implementation or should be
  deferred until another tool consumes it.
- Whether future PRs should paste the full report or only the key status fields.
- Whether the selector should mention the Windows `py` equivalent directly in
  output or keep command text POSIX-style and rely on handoffs for Windows
  translation.
- Whether a future CI advisory artifact is useful once the local report helper
  is stable.
- Whether the raw Windows resolver noise should eventually be fixed by local
  environment setup, Pyright configuration, package metadata, or wrapper-only
  policy.

## Suspected Gaps

- Current selector recommendation still points to raw `python3 -m pyright`.
- Current PowerShell wrapper output is useful locally but not a stable
  cross-platform report shape.
- Current PowerShell wrapper prints a full local interpreter path.
- Current handoffs classify raw resolver noise manually rather than through a
  shared report helper.
- Current tests do not lock Pyright output parsing or classification.
- Current CI does not run Pyright, by design; no CI advisory artifact exists.

## Stop Conditions

Stop and route back to Codex B or A if Codex C needs to:

- make Pyright required or failing
- require zero Pyright findings
- change `typeCheckingMode`
- change `pyrightconfig.json` source coverage or broad excludes
- change `pyproject.toml` dependency strategy
- introduce npm, npx, `package.json`, or package lockfiles
- edit CI to run Pyright
- change parser behavior
- change parser state final reconciliation
- change parser event classes or event kinds
- change parser payload shape
- change match identity
- change game identity
- change deduplication
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- touch live workbook state or deployed Apps Script state
- touch secrets, credentials, environment variables, raw logs, generated data,
  runtime status files, failed posts, workbook exports, local-only artifacts,
  or production behavior
- target `main`
- close issue #96
- mark tracker #82 complete

## Expected Codex C Handoff

Codex C should produce:

- `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`

The handoff must include:

- role performed
- issue and tracker used
- contract used
- branch and git status
- files inspected
- what was implemented or intentionally left unchanged
- chosen implementation option
- exact report fields implemented
- exact selector command text changed, if changed
- exact test sections added or changed
- Windows validation result
- macOS/Linux validation status or unverified note
- raw Pyright vs repo-approved report comparison
- classification of type findings, local resolver noise, and tooling/config
  blockers
- validation run and result
- secret/private-marker scan result
- protected-surface result
- surface-authorization result
- validation-selector result
- Pyright advisory/no-gate confirmation
- forbidden scopes touched or not touched
- remaining risks
- next recommended role
- pasteable Codex E prompt
- `workflow_handoff` block

## Expected Codex E Report

Codex E should produce:

- `docs/contract_test_reports/repo_wide_pyright_advisory_report.md`

The report must lead with findings and verify:

- Pyright remains advisory-only.
- Pyright is not added as a required/failing CI gate.
- Zero Pyright findings is not required.
- The repo-approved report command is stable and redacts/normalizes local
  interpreter paths.
- Raw Pyright output is not treated as authoritative over the approved
  wrapper/report command.
- Type findings, local resolver noise, and tooling/config blockers are
  classified as contracted.
- Selector output recommends the repo-approved advisory report command, if
  Codex C updates selector behavior.
- Tests cover report parsing/classification and selector command text, if those
  files are touched.
- No parser/runtime/workbook/webhook/App Script protected surfaces changed.
- No secrets, raw logs, generated data, runtime status files, failed posts,
  workbook exports, local-only artifacts, production behavior, main targeting,
  #96 closure, or #82 closure occurred.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for repo-wide hardening issue #98: Pyright advisory report artifact.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/98

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_pyright_advisory_report.md

Goal:
Compare current Pyright tooling, selector behavior, and hardening reports against the contract. Implement only the smallest report-only advisory tooling needed to produce a stable Pyright advisory report and selector recommendation.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/repo_wide_pyright_advisory_report.md
- docs/contracts/code_hardening_pyright_advisory.md
- docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md
- docs/contract_test_reports/code_hardening_pyright_advisory.md
- docs/contract_test_reports/repo_wide_hardening_baseline.md
- docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md
- docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md
- docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md
- docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md
- docs/contracts/repo_wide_validation_selector.md
- docs/contracts/repo_wide_protected_surface_authorization_checker.md
- docs/contracts/repo_wide_secret_private_marker_scanner.md
- pyproject.toml
- pyrightconfig.json
- tools/run_pyright_advisory.ps1
- tools/select_validation.py
- tests/test_select_validation.py
- .github/workflows/repo-checks.yml

Before editing:
- Confirm branch is codex/repo-wide-hardening-run.
- Inspect git status and exclude unrelated changes.
- State what the Pyright advisory report is supposed to do, what current Pyright tooling already does, what reporting gap remains, and the exact minimal implementation plan.

Do:
- Keep Pyright advisory-only and non-gating.
- Add a cross-platform report helper, preferably tools/run_pyright_advisory_report.py, that runs Pyright with pyrightconfig.json and the active Python interpreter path.
- Print a stable text report with the fields required by the contract.
- Redact or normalize local interpreter paths in durable report output.
- Classify type findings, local resolver noise, and tooling/config blockers.
- Add focused tests, preferably tests/test_pyright_advisory_report.py, for report parsing/classification and path redaction.
- Update tools/select_validation.py only to recommend the repo-approved Pyright advisory report command instead of the raw pyright command.
- Update tests/test_select_validation.py only for that selector recommendation change.
- Produce docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md.

Do not:
- Make Pyright required or failing.
- Require zero Pyright findings.
- Change typeCheckingMode.
- Change pyrightconfig.json source coverage or broad excludes.
- Change pyproject.toml dependency strategy.
- Introduce npm, npx, package.json, or package lockfiles.
- Edit CI unless the user explicitly authorizes a later issue/contract to do so.
- Change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, production behavior, or main.
- Close issue #96.
- Mark tracker #82 complete.
- Stage, commit, open a PR, close issues, or merge unless explicitly asked.

Validation:
git status --short --branch
py -m pytest -q tests\test_pyright_advisory_report.py tests\test_select_validation.py
py tools\run_pyright_advisory_report.py
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
py -m ruff check src tests tools
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-98.md --authorization-file contract=docs\contracts\repo_wide_pyright_advisory_report.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_pyright_advisory_report_comparison.md
git diff --check

Final handoff must include:
- role performed
- issue/tracker
- contract used
- files changed
- exact report/helper/test/selector sections changed
- validation run and result
- Pyright advisory/no-gate confirmation
- raw Pyright vs approved report comparison
- type finding / resolver noise / tooling blocker classification
- protected-surface status
- surface-authorization status
- secret/private-marker status
- validation-selector status
- what remains unverified
- whether forbidden scope was touched
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/98"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/repo_wide_pyright_advisory_report.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md"
  expected_review_artifact: "docs/contract_test_reports/repo_wide_pyright_advisory_report.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "git diff --check"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\\contracts\\repo_wide_pyright_advisory_report.md"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_agent_docs.py"
  stop_conditions:
    - "Do not implement code, wrapper changes, selector changes, tests, or CI edits in Codex B."
    - "Do not make Pyright required or failing."
    - "Do not require zero Pyright findings."
    - "Do not change Pyright config, typeCheckingMode, source coverage, or dependency strategy in Codex B."
    - "Do not edit CI unless a later contract and user instruction explicitly authorize it."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, production behavior, or merge-to-main policy."
    - "Do not target main."
    - "Do not close issue #96."
    - "Do not mark tracker #82 complete."
```
