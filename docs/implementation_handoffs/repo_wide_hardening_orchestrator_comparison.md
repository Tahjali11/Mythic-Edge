# Repo-Wide Hardening Orchestrator Implementation Handoff

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/103

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Contract: `docs/contracts/repo_wide_hardening_orchestrator.md`

Role performed: Codex C: Module Implementer

Branch: `codex/repo-wide-hardening-run`

Risk tier: Medium

Related ADRs: N/A

## Summary Of Comparison

The current repo already had separate deterministic hardening tools, but no
single local entrypoint for planning or running a stable bundle of those tools:

- `tools/check_protected_surfaces.py` owns protected/forbidden path
  classification.
- `tools/check_secret_patterns.py` owns secret/private-marker scanning.
- `tools/select_validation.py` owns changed-path validation recommendations.
- `tools/check_surface_authorization.py` owns authorization evidence checks.
- `tools/check_agent_docs.py` owns governance-doc consistency checks.
- `tools/run_pyright_advisory_report.py` owns Pyright advisory classification.
- `tools/generate_hardening_report.py` owns deterministic hardening report
  assembly.
- `tools/run_hardening_orchestrator.py` did not exist.
- `tests/test_hardening_orchestrator.py` did not exist.

This pass implemented a thin local orchestrator that plans or optionally runs
those existing tools while preserving command-level output, exit codes, and
tool-specific status distinctions. It does not replace the tools, edit CI,
query GitHub, call model providers, decide readiness, or change protected
parser/runtime/workbook/webhook/App Script behavior.

## Findings

No blocking contract ambiguity was found.

Contract mismatches fixed:

- Missing orchestrator implementation.
- Missing focused orchestrator tests.
- Missing validation-selector focused test mapping for the new orchestrator
  tool and test file.
- Missing implementation handoff for #103.

## Changes Made

Implemented `tools/run_hardening_orchestrator.py`:

- CLI:
  - `--base <git-ref>` required
  - `--repo-root <path>`
  - `--profile plan|quick|full|post-hardening`
  - `--run`
  - `--paths-from-stdin`
  - repeatable `--authorization-file kind=path`
  - `--format text|json`
  - `--summary-output <path>`
  - `--hardening-report-output <path>`
  - `--evidence-manifest <path>`
- default behavior is plan-only
- `--run` is required for execution, and `profile=plan` remains plan-only
- stable command profiles:
  - `plan`: quick-profile command plan only
  - `quick`: protected-surface gate, secret/private scan, selector,
    optional surface authorization, agent-docs checker, `git diff --check`
  - `full`: runnable quick commands plus pytest, Ruff, and Pyright advisory
  - `post-hardening`: full profile plus hardening report generator
- optional surface authorization is `skipped` with
  `authorization_files_not_supplied` when no authorization file is supplied
- command result statuses remain explicit:
  - `planned`
  - `passed`
  - `failed`
  - `warning`
  - `advisory`
  - `skipped`
  - `error`
- overall orchestrator statuses remain explicit:
  - `plan_only`
  - `passed`
  - `warning`
  - `advisory`
  - `failed`
  - `error`
- warning/advisory preservation:
  - secret scanner warning output becomes `warning`
  - protected-surface forbidden output becomes `failed`
  - surface authorization `authorization_status: review` becomes `warning`
  - Pyright `status: advisory_findings` remains `advisory`
- stdin path mode:
  - reads stdin once
  - deduplicates/sorts repo-relative paths
  - rejects outside-repo absolute paths with a redacted error
  - forwards the same path set to compatible tools
- output behavior:
  - text summary by default
  - JSON summary with the contracted object shape
  - optional Markdown summary output under `docs/contract_test_reports/`
  - optional hardening report output under `docs/contract_test_reports/` only
    for `post-hardening --run`
- subprocess execution uses `subprocess.run(..., shell=False)` through command
  lists.

Added `tests/test_hardening_orchestrator.py`:

- missing `--base` exits `2`
- default profile is plan-only and executes no subprocesses
- stable command rows for `plan`
- `quick` without `--run` executes nothing
- `quick --run` executes fake commands in stable order
- stdin paths are forwarded once to compatible tools
- outside-repo stdin paths are rejected and redacted
- skipped authorization is not rendered as passed
- secret scanner warnings become `warning`
- protected-surface forbidden output becomes `failed`
- surface authorization review output becomes `warning`
- Pyright advisory findings remain `advisory`
- subprocess/tool configuration errors become `error`
- summaries are sanitized and bounded
- JSON preserves command-level status and exit codes
- output paths outside `docs/contract_test_reports/` are rejected
- post-hardening report generator forwarding is explicit
- summary output writes text even when stdout is JSON
- no OpenAI, model-provider, or live GitHub commands are planned

Updated `tools/select_validation.py` and `tests/test_select_validation.py`:

- added focused mappings for:
  - `tools/run_hardening_orchestrator.py`
  - `tests/test_hardening_orchestrator.py`
- added selector regression coverage for the mapping.

## Files Changed

Owned by #103:

- `tools/run_hardening_orchestrator.py`
- `tests/test_hardening_orchestrator.py`
- `docs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md`

Narrow related selector mapping:

- `tools/select_validation.py`
- `tests/test_select_validation.py`

Source contract present in the worktree:

- `docs/contracts/repo_wide_hardening_orchestrator.md`

Unrelated untracked files present and not absorbed:

- `docs/.DS_Store`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Interface Changes

New local CLI:

```bash
python3 tools/run_hardening_orchestrator.py --base <git-ref> --profile <profile>
```

The CLI is local-only and deterministic. It is not a CI gate, PR readiness
gate, merge verdict, deploy verdict, issue-closure verdict, tracker-completion
verdict, parser truth source, or model-backed review system.

No parser/runtime/workbook/webhook/App Script interfaces changed.

## Validation Run

Passed:

```bash
python3 -m pytest -q tests/test_hardening_orchestrator.py
```

```text
19 passed in 0.03s
```

Passed:

```bash
python3 -m pytest -q tests/test_hardening_orchestrator.py tests/test_select_validation.py
```

```text
46 passed in 0.16s
```

Passed:

```bash
python3 tools/run_hardening_orchestrator.py --help
```

```text
usage: run_hardening_orchestrator.py ...
```

Passed:

```bash
python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile plan
```

```text
profile: plan
run_mode: plan
orchestrator_status: plan_only
```

Passed:

```bash
python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile quick
```

```text
profile: quick
run_mode: plan
orchestrator_status: plan_only
surface_authorization: authorization_files_not_supplied
```

Passed:

```bash
python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile quick --run
```

```text
profile: quick
run_mode: run
orchestrator_status: passed
surface_authorization: authorization_files_not_supplied
```

Passed:

```bash
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
```

```text
changed_paths: 0
selection_status: ok
```

Passed:

```bash
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
```

```text
scanned_paths: 0
forbidden: 0
warnings: 0
result: passed
```

Passed:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
```

```text
changed_paths: 0
forbidden: 0
warnings: 0
result: passed
```

Passed:

```bash
python3 tools/check_agent_docs.py
```

```text
checked_files: 29
errors: 0
warnings: 0
result: passed
```

Passed:

```bash
python3 tools/run_pyright_advisory_report.py
```

```text
status: clean
errors: 0
warnings: 0
information: 0
```

Passed:

```bash
python3 -m ruff check src tests tools
```

```text
All checks passed!
```

Passed:

```bash
git diff --check
```

```text
<no output>
```

Passed scoped safety scan for new/changed #103 files:

```bash
printf 'tools/run_hardening_orchestrator.py\ntests/test_hardening_orchestrator.py\ndocs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md\ntools/select_validation.py\ntests/test_select_validation.py\n' | python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
scanned_paths: 5
forbidden: 0
warnings: 0
result: passed
```

Passed scoped protected-surface scan for new/changed #103 files:

```bash
printf 'tools/run_hardening_orchestrator.py\ntests/test_hardening_orchestrator.py\ndocs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md\ntools/select_validation.py\ntests/test_select_validation.py\n' | python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
changed_paths: 5
forbidden: 0
warnings: 0
result: passed
```

Important validation nuance:

- Changed-file tools report zero changed paths while this implementation is
  uncommitted/untracked because they intentionally use
  `git diff <base>...HEAD`. Focused tests and direct CLI runs validate the new
  behavior until submitter work creates the committed branch diff.

## Open Risks

- `quick --run` continues after required command failures so it can collect
  more command-level evidence. The orchestrator then exits `1` if any required
  command failed, or `2` if configuration/tool errors occur.
- The orchestrator can summarize tool output, but reviewers must still inspect
  underlying tool reports when warnings, advisory findings, failures, or errors
  appear.
- `post-hardening` planning/forwarding is implemented and tested with fake
  subprocesses, but the profile was not executed in validation because it can
  produce report artifacts and is not part of the requested validation list.
- Untracked #102 deferral files remain present and should not be included in
  the #103 submission unless the submitter is explicitly asked to include them.

## Next Recommended Role

Next role: Codex E: Module Reviewer / Contract Tester.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for repo-wide hardening issue #103: Hardening Orchestrator.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/103
- Branch/base: codex/repo-wide-hardening-run
- Contract: docs/contracts/repo_wide_hardening_orchestrator.md
- Implementation handoff: docs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md
- Implementation files: tools/run_hardening_orchestrator.py, tests/test_hardening_orchestrator.py
- Selector mapping files: tools/select_validation.py, tests/test_select_validation.py
- Dependency note: do not review #102 LLM advisory implementation details; #102 remains deferred/no-code.

Goal:
Verify the Codex C implementation against the hardening orchestrator contract.

Confirm:
- The orchestrator requires explicit --base and never assumes main.
- Default behavior is plan-only and executes no commands.
- Command execution requires explicit --run.
- Profiles plan, quick, full, and post-hardening are stable and match the contract.
- The orchestrator preserves each underlying tool's separate authority and does not collapse them into an opaque mega-tool.
- Command rows include command id, priority, status, exact command string, source tool, exit code when executed, and sanitized summary or skip reason.
- Skipped surface authorization is not reported as passed.
- Warning, advisory, failed, skipped, planned, and error states remain distinct.
- quick --run executes commands in stable order and continues collecting command-level evidence.
- Pyright advisory findings remain advisory and non-blocking.
- post-hardening report-generator forwarding is explicit and output paths are constrained to docs/contract_test_reports/.
- JSON output preserves command-level statuses and exit codes.
- Summary output writes Markdown/text under docs/contract_test_reports/.
- The orchestrator does not call OpenAI, model providers, live GitHub, CI mutation, credentials, environment-variable contracts, parser/runtime/workbook/webhook/App Script behavior, or protected surfaces.
- Selector mapping changes are limited to the new orchestrator tool/test focused test mapping.
- Unrelated untracked #102 files and docs/.DS_Store are not absorbed into #103.

Validation:
Run:
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
python3 -m pytest -q tests/test_select_validation.py

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
- A workflow_handoff block.

Do not change files in review-only mode.
Do not edit CI, target main, stage, commit, push, close tracker #82, call model providers, or absorb unrelated #102 artifacts.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/103"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/repo_wide_hardening_orchestrator.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md"
  produced_artifacts:
    - "tools/run_hardening_orchestrator.py"
    - "tests/test_hardening_orchestrator.py"
    - "docs/implementation_handoffs/repo_wide_hardening_orchestrator_comparison.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "python3 -m pytest -q tests/test_hardening_orchestrator.py"
    - "python3 tools/run_hardening_orchestrator.py --help"
    - "python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile plan"
    - "python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile quick"
    - "python3 tools/run_hardening_orchestrator.py --base origin/codex/repo-wide-hardening-run --profile quick --run"
    - "python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/check_agent_docs.py"
    - "python3 tools/run_pyright_advisory_report.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 -m pytest -q tests/test_select_validation.py"
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
