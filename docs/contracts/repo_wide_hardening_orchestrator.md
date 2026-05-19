# Repo-Wide Hardening Orchestrator Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/103

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch target: `codex/repo-wide-hardening-run`

Previous completed deterministic hardening module: #100 Hardening report
generator, PR #101, merge commit
`d92b161aa0b3aa18a3af3baabd69968f9735aed4`

Dependency note: issue #103 is queued after issue #102 is completed or
explicitly deferred. This contract does not depend on any #102 implementation
detail and does not authorize LLM/model-provider behavior.

Agent and workflow documents read:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `.github/pull_request_template.md`

Repo-wide hardening artifacts and tools read:

- issue #103
- issue #102 for dependency status and boundary awareness
- `docs/contracts/repo_wide_validation_selector.md`
- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `docs/contracts/repo_wide_hardening_report_generator.md`
- `tools/generate_hardening_report.py`
- `tests/test_hardening_report_generator.py`
- `tools/check_secret_patterns.py`
- `tools/check_agent_docs.py`
- `tools/check_protected_surfaces.py`
- `tools/check_surface_authorization.py`
- `tools/run_pyright_advisory_report.py`
- `.github/workflows/repo-checks.yml`

This is a contract-writing artifact only. It does not implement code, edit CI,
target `main`, close tracker #82, mark tracker #82 complete, call OpenAI or
any model provider, or change parser/runtime/workbook/webhook/Apps Script
behavior or protected surfaces.

## Module

Repo-wide Hardening Orchestrator.

Likely implementation artifact:

- `tools/run_hardening_orchestrator.py`

Likely focused tests:

- `tests/test_hardening_orchestrator.py`

Expected implementation handoff:

- `docs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md`

Expected review report:

- `docs/contract_test_reports/repo_wide_hardening_orchestrator.md`

Plain English: Mythic Edge has several focused hardening tools. The
orchestrator should provide one local, deterministic entrypoint that can plan
or run a named bundle of those tools, record the exact commands and results,
and make handoffs easier to read. It must preserve each tool's separate
responsibility and must not become a CI gate, hidden mega-tool, merge verdict,
deploy verdict, tracker verdict, parser truth source, or model-backed review
system.

## Owning Layer

Owning layer: repo-wide hardening tool coordination and local validation
ergonomics.

Truth boundary:

- The orchestrator owns deterministic command planning, optional local command
  execution, command-result capture, and summary formatting.
- `tools/select_validation.py` owns changed-path validation recommendations.
- `tools/check_secret_patterns.py` owns secret/private-marker scan results.
- `tools/check_protected_surfaces.py` owns path-based protected-surface
  classifications.
- `tools/check_surface_authorization.py` owns protected-surface authorization
  report status.
- `tools/check_agent_docs.py` owns governance-doc consistency results.
- `tools/run_pyright_advisory_report.py` owns Pyright advisory classification.
- `tools/generate_hardening_report.py` owns deterministic hardening status
  report assembly from explicit evidence.
- Parser/state remains the truth owner for parser-managed facts.
- Codex E or a human reviewer owns review findings.
- Codex G owns merge, close, tracker-update, and deployer lifecycle decisions
  only after explicit user approval and satisfied gates.

The orchestrator must not own:

- parser truth
- parser behavior
- parser state final reconciliation
- workbook schema truth
- webhook payload truth
- Apps Script behavior
- parser event classes
- match identity
- game identity
- deduplication
- secret policy beyond invoking the existing scanner
- protected-surface classification beyond invoking existing tools
- protected-surface authorization beyond invoking existing tools
- validation truth beyond faithfully reporting executed command results
- CI pass/fail truth
- PR readiness
- merge readiness
- deploy readiness
- issue closure
- tracker completion
- OpenAI/API/model-provider behavior
- credential, token, webhook URL, environment-variable, or model-default policy

## Files Owned By This Contract

This contract owns:

- `docs/contracts/repo_wide_hardening_orchestrator.md`

Future implementation surfaces allowed by this contract:

- `tools/run_hardening_orchestrator.py`
- `tests/test_hardening_orchestrator.py`
- `docs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator.md`

Optional narrow implementation surface:

- `tools/select_validation.py`, only if Codex C adds a focused mapping for
  `tools/run_hardening_orchestrator.py` or its test file.
- `tests/test_select_validation.py`, only if the selector mapping changes.

Referenced but not owned:

- issue #82
- issue #102
- issue #103
- `.github/workflows/repo-checks.yml`
- `.github/pull_request_template.md`
- existing hardening tools and their focused tests
- parser, runtime, workbook, webhook, Apps Script, fixture, raw-log,
  generated-data, failed-post artifact, local retry queue, and workbook export
  paths

This contract does not authorize touching parser/runtime/workbook/webhook/Apps
Script behavior, CI gate behavior, production state, credentials, local raw
artifacts, generated data, or workbook exports.

## Observed Current Behavior

Observed during this Codex B pass:

- The current branch is `codex/repo-wide-hardening-run`.
- The branch is even with `origin/codex/repo-wide-hardening-run`.
- The worktree contains untracked #102 artifacts from prior work; this
  contract does not modify or absorb them.
- Issue #103 is open and names `docs/contracts/repo_wide_hardening_orchestrator.md`
  as the expected contract artifact.
- Issue #103 says the orchestrator should come after #102 is completed or
  explicitly deferred and must not depend on unmerged #102 implementation
  details.
- Issue #102 is open on GitHub. The local #102 contract draft says executable
  implementation should be deferred; this #103 contract relies on the user's
  #103 handoff and does not require #102 implementation.
- `tools/select_validation.py`, `tools/check_secret_patterns.py`,
  `tools/check_protected_surfaces.py`, `tools/check_surface_authorization.py`,
  `tools/check_agent_docs.py`, `tools/run_pyright_advisory_report.py`, and
  `tools/generate_hardening_report.py` already exist.
- `.github/workflows/repo-checks.yml` runs tests, the protected-surface gate on
  pull requests, and Ruff. This contract does not authorize CI edits.

Current gap:

- There is no deterministic local command that coordinates the existing
  hardening tools into one plan/run summary while preserving each tool's
  separate output and authority.

## Required Guarantee

The orchestrator must be a thin coordinator, not a replacement for the
individual hardening tools.

Required properties:

- Require an explicit `--base <git-ref>` for every profile.
- Never silently assume `main`.
- Default to plan-only behavior.
- Execute commands only when `--run` is supplied and the selected profile
  permits execution.
- Use only Python standard library in the first implementation.
- Use subprocess execution without `shell=True`.
- Capture and report exact command strings, command labels, exit codes,
  stdout/stderr summaries, and result labels for every executed command.
- Preserve stable command order within each profile.
- Preserve each tool's own status vocabulary and exit behavior.
- Distinguish skipped, planned, advisory, warning, failed, and error states.
- Never report a skipped or planned command as passed.
- Never hide individual command failures behind an overall success label.
- Never invent validation evidence.
- Never claim CI passed unless CI evidence is supplied by an external artifact
  in a future contract; the first implementation must not query CI.
- Never query live GitHub.
- Never edit CI.
- Never call OpenAI or any model provider.
- Never import or call #102 LLM advisory implementation details.
- Never decide merge readiness, deploy readiness, PR readiness, issue closure,
  or tracker completion.
- Never change parser/runtime/workbook/webhook/Apps Script behavior or
  protected surfaces.

## Public Interface

### Primary CLI

Required command:

```bash
python3 tools/run_hardening_orchestrator.py --base <git-ref> --profile <profile>
```

Windows-compatible command:

```powershell
py tools\run_hardening_orchestrator.py --base <git-ref> --profile <profile>
```

Required arguments:

- `--base <git-ref>`: explicit base branch or ref for changed-file based
  tools. Examples: `origin/main`, `origin/codex/repo-wide-hardening-run`.

Required optional arguments:

- `--repo-root <path>`: repository root to inspect. Default: `"."`.
- `--profile plan|quick|full|post-hardening`: default must be `plan`.
- `--run`: execute the selected runnable profile. Without `--run`, the
  orchestrator must render a plan and execute no commands.
- `--paths-from-stdin`: read newline-delimited paths once from stdin and feed
  those paths to compatible underlying tools.
- `--authorization-file <kind=path>`: repeatable source for
  `tools/check_surface_authorization.py`.
- `--format text|json`: default `text`. JSON is required for deterministic
  tests and later machine-readable summaries.

Allowed optional arguments:

- `--summary-output <path>`: write the orchestrator summary to an explicitly
  requested Markdown file under `docs/contract_test_reports/`.
- `--hardening-report-output <path>`: only valid with `--profile
  post-hardening --run`; forwards an explicit output path to
  `tools/generate_hardening_report.py`. The path must be under
  `docs/contract_test_reports/`.
- `--evidence-manifest <path>`: only valid when the profile includes
  `tools/generate_hardening_report.py`; forwards the manifest path to the
  report generator.

Forbidden first-pass arguments and behavior:

- `--query-github`
- `--update-ci`
- `--close-issues`
- `--update-tracker`
- `--decide-readiness`
- `--deploy`
- `--openai`
- `--model`
- any flag that opens network connections, calls model providers, mutates
  issues, mutates PRs, edits CI, changes credentials, changes environment
  variables, touches live workbook or Apps Script state, or changes protected
  parser/runtime/workbook/webhook surfaces

### Test-Facing Python Helpers

The stable public interface is the CLI and the rendered summary shape. The
implementation may expose standard-library-only helper functions or
dataclasses for tests, such as:

- command plan construction
- command record models
- fake runner injection
- command-result classification
- JSON rendering
- text rendering
- safe output-path validation

No parser/runtime code may import these helpers.

## Command Profiles

### `plan`

Purpose: default no-execution overview.

Behavior:

- Do not execute commands.
- Render the quick-profile command plan.
- Mark every command as `planned`.
- Set `orchestrator_status: plan_only`.
- Exit `0`.

### `quick`

Purpose: fast local hardening check bundle for handoffs.

Planned commands:

- `python3 tools/check_protected_surfaces.py --base <base>`
- `python3 tools/check_secret_patterns.py --base <base>`
- `python3 tools/select_validation.py --base <base>`
- `python3 tools/check_agent_docs.py`
- `git diff --check`

Optional command:

- `python3 tools/check_surface_authorization.py --base <base> ...`, only when
  one or more `--authorization-file` arguments are supplied. If authorization
  files are absent, render this command as `skipped` with reason
  `authorization_files_not_supplied`; do not render it as passed.

Without `--run`:

- Render the plan and execute nothing.

With `--run`:

- Execute the planned commands in stable order.
- Record each command's exit code.
- Preserve `tools/check_secret_patterns.py` warning-only exit `0` behavior as
  `warning`, not `failed`.
- Preserve `tools/check_protected_surfaces.py` forbidden exit `1` behavior as
  `failed`.
- Preserve `tools/check_surface_authorization.py` `authorization_status:
  review` as `warning`, not `passed`.

### `full`

Purpose: broader local validation bundle for implementation/review work.

Planned commands:

- all runnable `quick` commands
- `python3 -m pytest -q tests`
- `python3 -m ruff check src tests tools`
- `python3 tools/run_pyright_advisory_report.py`

Behavior:

- Requires `--run` for execution.
- Pyright remains advisory and non-blocking according to
  `tools/run_pyright_advisory_report.py`.
- A Pyright `status: advisory_findings` result must be rendered as
  `advisory`, not as a required failure.
- A Pyright helper exit `2` for tooling/config blockers must be rendered as
  `error`.

### `post-hardening`

Purpose: local bundle for preparing the final post-hardening comparison report.

Planned commands:

- all runnable `full` commands
- `python3 tools/generate_hardening_report.py`

Behavior:

- Requires `--run` for execution.
- The report generator command may include `--evidence-manifest` only when the
  caller supplies that argument.
- The report generator command may include `--output` only when the caller
  supplies `--hardening-report-output`.
- Generated reports remain evidence summaries only. They do not decide merge
  readiness, deploy readiness, issue closure, or tracker completion.

### #102 LLM Advisory Scaffold

No profile may include #102 LLM advisory behavior in the first implementation.

If #102 is later implemented, the orchestrator may include it only after a new
or amended contract explicitly authorizes an off-by-default advisory
relationship. Even then, model-provider calls must stay outside this contract.

## Inputs

### Base Ref

Type: `str`

Source: caller-supplied CLI argument.

Required: yes.

Rules:

- Must not default to `main`.
- Must be rendered in the summary.
- Must be forwarded to changed-file based tools.

### Profile

Type: enum string.

Allowed values:

- `plan`
- `quick`
- `full`
- `post-hardening`

Default: `plan`.

### Run Flag

Type: boolean.

Source: `--run`.

Default: `false`.

Rules:

- Without `--run`, no subprocess command may execute.
- `plan` must stay plan-only even if a future user attempts to combine it with
  execution.

### Changed Paths From Stdin

Type: newline-delimited repo-relative paths.

Source: stdin when `--paths-from-stdin` is set.

Rules:

- Read stdin once.
- Feed the same path set to compatible tools that support `--paths-from-stdin`.
- Reject or redact outside-repo paths.
- Do not write the path list to disk.

### Authorization Files

Type: repeated `kind=path` values.

Source: caller-supplied CLI argument.

Rules:

- Forward only to `tools/check_surface_authorization.py`.
- Do not parse authorization files as broad proof in the orchestrator.
- If absent, authorization must be reported as skipped/not configured, not
  passed.

### Evidence Manifest And Report Output

Type: repo-local paths.

Source: caller-supplied CLI arguments.

Rules:

- Valid only for the `post-hardening` profile when the report generator is
  included.
- Forward to `tools/generate_hardening_report.py`.
- Do not parse the manifest as orchestrator authority.
- Reject summary and report output paths outside `docs/contract_test_reports/`.

## Outputs

### Text Summary

Default output format: text to stdout.

Required fields:

```text
Hardening Orchestrator
schema_version: 1
profile: <profile>
run_mode: plan|run
base: <base>
orchestrator_status: <status>
merge_readiness: not_decided_by_orchestrator
deploy_readiness: not_decided_by_orchestrator
tracker_completion: not_decided_by_orchestrator
```

Required sections:

- `Commands`
- `Skipped Commands`
- `Warnings And Advisory Results`
- `Missing Or Not Configured`
- `Summary`
- `Workflow Handoff`

Every command row must include:

- command id
- priority: `required`, `recommended`, or `advisory`
- status
- exact command string
- exit code when executed
- source tool
- short sanitized stdout/stderr summary or skip reason

### JSON Summary

Required object shape:

```json
{
  "object": "mythic_edge_hardening_orchestrator",
  "schema_version": 1,
  "profile": "quick",
  "run_mode": "plan",
  "base": "origin/codex/repo-wide-hardening-run",
  "orchestrator_status": "plan_only",
  "merge_readiness": "not_decided_by_orchestrator",
  "deploy_readiness": "not_decided_by_orchestrator",
  "tracker_completion": "not_decided_by_orchestrator",
  "commands": []
}
```

JSON output must preserve the same command statuses as text output.

### Markdown Summary File

If `--summary-output` is supplied:

- Write only the requested Markdown summary file.
- Require a path under `docs/contract_test_reports/`.
- Also print the summary to stdout unless Codex C documents a narrower
  behavior in the implementation handoff.

## Result Vocabulary

Command statuses:

- `planned`: command listed but not executed
- `passed`: command executed successfully with no parsed warning/advisory state
- `failed`: required command returned a failing result or nonzero failure exit
- `warning`: command completed but reported warning or review-needed status
- `advisory`: command completed with advisory findings that are not blocking by
  contract
- `skipped`: command was intentionally skipped with a reason
- `not_configured`: command could not run because optional inputs were absent
- `error`: orchestrator or tool configuration error

Overall `orchestrator_status` values:

- `plan_only`: no commands executed
- `passed`: all executed required commands passed and no warning/advisory states
  were reported
- `warning`: no required command failed, but one or more warning states were
  reported
- `advisory`: no required command failed, and only advisory findings were
  reported
- `failed`: at least one required command failed
- `error`: orchestrator configuration failed, a required tool was unavailable,
  or command execution could not be attempted safely

Exit code policy:

- Exit `0` for `plan_only`, `passed`, `warning`, and `advisory`.
- Exit `1` for `failed`.
- Exit `2` for `error` or CLI usage/configuration errors.

Warnings and advisory findings may still require human review. Exit `0` must
not be described as merge-ready, deploy-ready, or tracker-complete.

## Error Behavior And Stop Conditions

Malformed CLI arguments:

- Print a concise configuration error.
- Exit `2`.
- Do not execute commands.
- Do not write outputs.

Missing required base ref:

- Exit `2`.
- Do not assume `main`.

Unknown profile:

- Exit `2`.
- Do not execute commands.

Missing optional authorization files:

- Render surface authorization as `skipped` or `not_configured`.
- Do not render authorization as passed.

Underlying command exit `1`:

- Preserve the command's exit code in the command row.
- Classify required command failures as `failed`.
- Exit orchestrator `1` after all allowed commands in the profile have
  completed, unless Codex C chooses fail-fast and documents that behavior.

Underlying command exit `2` or subprocess execution error:

- Classify as `error`.
- Exit orchestrator `2`.

Stop conditions:

- Stop if implementation requires CI edits.
- Stop if implementation calls live GitHub.
- Stop if implementation calls OpenAI or any model provider.
- Stop if implementation reads, writes, or changes credentials, tokens,
  webhook URLs, environment-variable contracts, or model defaults.
- Stop if implementation changes parser/runtime/workbook/webhook/Apps Script
  behavior or protected surfaces.
- Stop if implementation treats orchestrator output as merge, deploy, PR,
  tracker, or parser truth.
- Stop if implementation would collapse individual tool output into one opaque
  summary without command-level evidence.

## Side Effects

Allowed first-pass side effects:

- Execute local subprocess commands only when `--run` is supplied.
- Print text or JSON summaries to stdout.
- Optionally write a Markdown summary under `docs/contract_test_reports/` when
  `--summary-output` is supplied.
- Optionally cause `tools/generate_hardening_report.py` to write an explicitly
  requested report under `docs/contract_test_reports/` in the `post-hardening`
  profile only.

Forbidden side effects:

- CI edits
- GitHub issue, PR, comment, label, or tracker mutation
- network calls
- OpenAI/model-provider calls
- credential lookup or writes
- environment-variable contract changes
- parser/runtime/workbook/webhook/Apps Script behavior changes
- local raw artifact, generated data, failed-post artifact, runtime status, or
  workbook export writes

## Dependency Order

Implementation should proceed in this order:

1. Implement data models and command-plan construction.
2. Implement text and JSON rendering for planned commands.
3. Implement fake-runner/dependency-injection support for tests.
4. Implement explicit `--run` execution.
5. Add command-result classification.
6. Add optional `--summary-output` validation.
7. Add optional `post-hardening` report-generator forwarding.
8. Update `tools/select_validation.py` only if adding the orchestrator's
   focused test mapping.
9. Write the implementation handoff.

Do not edit CI in this issue.

## Compatibility

The orchestrator must preserve:

- validation selector recommendation semantics
- secret/private-marker scanner forbidden/warning behavior
- protected-surface gate forbidden/protected path behavior
- surface authorization `ok`/`review`/`error` status
- agent-docs checker error/warning behavior
- Pyright advisory non-blocking policy
- hardening report generator report-only semantics
- tracker #82 lifecycle rules
- the #102 no-model-provider dependency boundary
- parser truth ownership

The orchestrator may summarize existing tool output, but it must not redefine
or weaken it.

## Tests Required

Implementation validation:

```bash
python3 -m pytest -q tests/test_hardening_orchestrator.py
python3 tools/run_hardening_orchestrator.py --help
python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile plan
python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile quick
python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile quick --run
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
python3 tools/check_agent_docs.py
python3 tools/run_pyright_advisory_report.py
python3 -m ruff check src tests tools
git diff --check
```

If Codex C adds a selector mapping:

```bash
python3 -m pytest -q tests/test_select_validation.py
```

Focused tests must verify:

- missing `--base` exits `2`
- default profile is plan-only and executes no subprocesses
- `--profile plan` renders stable command rows
- `--profile quick` without `--run` executes no commands
- `--profile quick --run` executes fake commands in stable order
- skipped authorization is not rendered as passed
- scanner warning output is classified as `warning`
- protected-surface forbidden output is classified as `failed`
- surface authorization review output is classified as `warning`
- Pyright advisory findings remain `advisory`
- required command exit `1` makes orchestrator exit `1`
- configuration/subprocess errors make orchestrator exit `2`
- stdout/stderr summaries are sanitized and bounded
- JSON output preserves command-level status and exit codes
- output paths outside `docs/contract_test_reports/` are rejected
- no OpenAI/API/model-provider command exists
- no live GitHub, CI edit, credential, environment-variable, parser/runtime,
  workbook, webhook, or Apps Script behavior is required

Tests must use fake subprocess results or runner injection. They must not run
the full test suite from unit tests.

## Acceptance Criteria

- `docs/contracts/repo_wide_hardening_orchestrator.md` exists.
- Codex C implements `tools/run_hardening_orchestrator.py` and focused tests,
  unless review routes back to B first.
- The orchestrator defaults to plan-only behavior.
- Executing commands requires explicit `--run`.
- The CLI requires explicit `--base`.
- The profile vocabulary is stable.
- Every command result includes command id, exact command string, status, and
  exit code when executed.
- Skipped commands are never reported as passed.
- Warning and advisory states remain distinct from required failures.
- No OpenAI/API/model-provider behavior exists.
- No CI edits are made.
- No protected parser/runtime/workbook/webhook/Apps Script behavior changes
  are made.
- Output never claims merge readiness, deploy readiness, PR readiness, issue
  closure, tracker completion, parser truth, workbook schema truth, or CI truth.
- Tracker #82 remains open and not complete.

## Open Questions And Contract Risks

- Whether `quick --run` should fail fast or continue collecting later command
  results after a required failure. This contract permits either if documented
  in the implementation handoff, but preserving as many command results as
  practical is preferred.
- Whether the first implementation should write a Markdown summary artifact or
  keep summaries stdout-only. The contract permits explicit `--summary-output`
  but does not require using it in normal validation.
- Whether `post-hardening` should eventually become the main entrypoint for
  final comparison evidence. That final comparison still needs its own issue or
  problem representation.
- Whether a future #102 advisory scaffold should ever be orchestrated. This
  contract says no for the first implementation.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for repo-wide hardening issue #103: Hardening Orchestrator.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/103
- Contract: docs/contracts/repo_wide_hardening_orchestrator.md
- Branch/base: codex/repo-wide-hardening-run
- Proposed tool path: tools/run_hardening_orchestrator.py
- Proposed tests: tests/test_hardening_orchestrator.py
- Previous completed deterministic hardening module: #100 Hardening report generator, PR #101, merge commit d92b161aa0b3aa18a3af3baabd69968f9735aed4
- Dependency note: do not depend on unmerged #102 implementation details, and do not include LLM/model-provider behavior.

Goal:
Compare the current repo state against the hardening orchestrator contract. Implement the smallest coherent local deterministic orchestrator and focused tests needed to satisfy the contract.

Do:
- Preserve each hardening tool's separate authority.
- Default the orchestrator to plan-only behavior.
- Require explicit --run for command execution.
- Require explicit --base.
- Add focused tests using fake subprocess results or runner injection.
- Keep command statuses, exit codes, and skipped/not-configured states explicit.
- Write docs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Edit CI.
- Target main.
- Close tracker #82 or mark it complete.
- Collapse individual hardening tools into one opaque mega-tool.
- Call OpenAI or any model provider.
- Add credentials, API keys, tokens, webhook URLs, environment-variable contracts, or model defaults.
- Depend on unmerged #102 implementation details.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, raw logs, generated data, runtime status files, failed-post artifacts, workbook exports, production behavior, or protected surfaces.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/103"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/repo_wide_hardening_orchestrator.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "git diff --check"
    - "printf 'docs/contracts/repo_wide_hardening_orchestrator.md\\n' | python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin"
    - "printf 'docs/contracts/repo_wide_hardening_orchestrator.md\\n' | python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not edit CI."
    - "Do not target main."
    - "Do not close tracker #82 or mark it complete."
    - "Do not collapse individual hardening tools into one opaque mega-tool."
    - "Do not call OpenAI or any model provider."
    - "Do not depend on unmerged #102 implementation details."
    - "Do not let the orchestrator become validation truth, merge readiness, deploy readiness, tracker completion, PR readiness, issue closure, CI truth, or parser truth."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior or protected surfaces."
```
