# Code Hardening Pyright Findings Cleanup

## Issue

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Related Pyright advisory issue: https://github.com/Tahjali11/Mythic-Edge/issues/45

## Contract

- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`
- `docs/contract_test_reports/code_hardening_pyright_advisory.md`

## Role Performed

Codex D: Module Fixer / Pyright findings cleanup.

## What Pyright Reported

Initial command:

```powershell
pyright --project pyrightconfig.json
```

Initial result:

```text
90 errors
5 warnings
```

The findings split into two groups:

- Environment resolution noise: `19 errors` and `5 warnings` came from bare
  `pyright` not finding the same Python environment that `py -m pytest` uses.
  The affected imports were `pytest`, `requests`, and `bs4`.
- Real static type findings: `71 errors` remained when Pyright was pointed at
  the active Python interpreter with `--pythonpath`.

The real findings were grouped by rule:

```text
reportArgumentType: 45
reportAttributeAccessIssue: 18
reportOptionalMemberAccess: 5
reportCallIssue: 2
reportOperatorIssue: 1
```

Representative causes:

- dynamic parser/runtime payload values needed explicit narrowing before
  `int(...)`, `.get(...)`, or callback use
- test helpers intentionally passed malformed data into safe functions
- parser modules and stream collaborators needed structural protocols
- callback helpers returned callables but were typed as `object`
- event parser tests needed covariant `Sequence` typing instead of concrete
  `list` typing
- local Pyright needed a wrapper to use the same Python interpreter as pytest

## What Changed

Added `tools/run_pyright_advisory.ps1` to resolve the active Python interpreter
through the Windows `py` launcher and pass it to Pyright with `--pythonpath`.
This avoids local PATH drift where `python` is unavailable but `py` works.

Made narrow type-safety updates in source files:

- explicit runtime export flag arguments in `analytics_sidecar.py`
- local safe integer narrowing in dynamic payload readers
- callable callback return types in `runner.py`
- structural parser/stream typing in `router.py` and `stream.py`
- saved-event kind narrowing while preserving nested payload pass-through
- small signature widening where existing code already guarded dynamic input

Made test-only typing clarifications:

- explicit `assert ... is not None` before optional path reads
- `cast(Any, ...)` for deliberately invalid state injection
- helper functions for parser outputs that may be one event or a list
- covariant `Sequence` typing for event lists
- dynamic `setattr` for frozen dataclass mutation test

## Review Loopback Fixes

Codex E found two behavior risks in the initial Pyright cleanup:

- `saved_event_replay.py` converted present malformed nested saved-event
  payloads to `{}`. The replay contract preserves v1 pass-through behavior, so
  malformed present payloads must remain visible through event construction.
- `grp_id_candidates.py` suppressed present nonblank malformed
  `runner_up_gap` values. The cleanup now preserves the previous direct
  conversion behavior: missing or blank values become `None`; malformed
  present values fail fast.

Fixes made in this loopback:

- removed the nested saved-event payload normalization from
  `event_from_saved_record()`
- restored direct nonblank `runner_up_gap` conversion through a local typed
  variable
- added focused regression coverage for malformed saved-event payloads and
  malformed `runner_up_gap` values

## Interface Changes

No parser payload shape, workbook schema, webhook payload shape, Apps Script
behavior, parser event classes, match/game identity, deduplication, or final
reconciliation behavior changed.

Tooling interface added:

```powershell
tools\run_pyright_advisory.ps1
```

## Validation Run

```powershell
tools\run_pyright_advisory.ps1
```

Result:

```text
0 errors, 0 warnings, 0 informations
```

```powershell
py -m pytest -q
```

Result:

```text
670 passed
```

```powershell
py -m ruff check src tests tools
```

Result:

```text
All checks passed!
```

```powershell
py tools\check_protected_surfaces.py --base origin/main
```

Result:

```text
changed_paths: 55
forbidden: 0
warnings: 5
result: passed
```

Additional working-tree path check:

```powershell
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result:

```text
changed_paths: 29
forbidden: 0
warnings: 3
result: passed
```

Review loopback focused validation:

```powershell
py -m pytest -q tests\test_saved_event_replay.py tests\test_grp_id_candidates.py
```

Result before the D fix:

```text
2 failed, 35 passed
```

Result after the D fix:

```text
37 passed
```

```powershell
py -m pytest -q tests\test_saved_event_replay.py tests\test_grp_id_candidates.py tests\test_runtime_surfaces.py tests\test_runner.py
```

Result:

```text
62 passed
```

Current path-scoped protected-surface check for the working tree:

```powershell
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Result:

```text
changed_paths: 29
forbidden: 0
warnings: 3
result: passed
```

## Still Unverified

- Bare `pyright --project pyrightconfig.json` still reports environment
  resolution findings in this shell because `python` is not on PATH. The
  wrapper is the verified local command.
- No GitHub Actions run has been observed for this cleanup.

## Reviewer Focus

- Confirm the source edits are type-narrowing only and do not alter parser
  truth, workbook schema, webhook shape, Apps Script behavior, identity, or
  deduplication.
- Confirm the review loopback fixes preserve saved-event replay malformed
  nested-payload behavior and candidate-report `runner_up_gap` fail-fast
  behavior.
- Confirm `tools/run_pyright_advisory.ps1` is acceptable as the local Pyright
  command for this Windows environment.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test confirmation.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/45"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/code_hardening_pyright_findings_cleanup.md"
  target_artifact: "docs/contract_test_reports/code_hardening_pyright_findings_cleanup.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "tools\\run_pyright_advisory.ps1 -> 0 errors, 0 warnings"
    - "py -m pytest -q tests\\test_saved_event_replay.py tests\\test_grp_id_candidates.py -> 37 passed"
    - "py -m pytest -q tests\\test_saved_event_replay.py tests\\test_grp_id_candidates.py tests\\test_runtime_surfaces.py tests\\test_runner.py -> 62 passed"
    - "py -m pytest -q -> 670 passed"
    - "py -m ruff check src tests tools -> All checks passed"
    - "path-scoped protected-surface check against origin/codex/code-hardening-suite -> passed"
  stop_conditions:
    - "Do not make Pyright a required CI gate unless a future contract says so."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, identity, deduplication, or final reconciliation during review."
```
