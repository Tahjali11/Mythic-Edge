# Repo-Wide Hardening Baseline Report

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/83

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Tracker update: https://github.com/Tahjali11/Mythic-Edge/issues/82#issuecomment-4466121535

Role: Codex C: Implementer / Baseline Reporter

Branch: `codex/repo-wide-hardening-run`

Risk tier: Low

Report date: 2026-05-16

## Summary

Baseline repo-wide hardening validation is clean on
`codex/repo-wide-hardening-run`.

The branch was clean before this report was created and was even with
`origin/main`:

- `HEAD`: `3da1242`
- `HEAD...origin/main`: `0 0`
- protected-surface changed paths: `0`
- forbidden protected-surface paths: `0`
- warning protected-surface paths: `0`

No hardening tools were implemented in this issue. No parser behavior, parser
state final reconciliation, workbook schema, webhook payload shape, Apps Script
behavior, parser event classes, match/game identity, deduplication, secrets,
environment variables, raw logs, generated data, runtime status files, failed
posts, or workbook exports were changed.

## Baseline Commands

### `git status --short --branch`

```text
## codex/repo-wide-hardening-run...origin/main
```

### `git rev-parse --short HEAD`

```text
3da1242
```

### `git rev-list --left-right --count HEAD...origin/main`

```text
0	0
```

### `python3 -m pytest -q tests`

```text
........................................................................ [ 10%]
........................................................................ [ 21%]
........................................................................ [ 32%]
........................................................................ [ 42%]
........................................................................ [ 53%]
........................................................................ [ 64%]
........................................................................ [ 75%]
........................................................................ [ 85%]
........................................................................ [ 96%]
......................                                                   [100%]
670 passed in 1.06s
```

### `python3 -m ruff check src tests tools`

```text
All checks passed!
```

### `python3 -m pyright`

```text
0 errors, 0 warnings, 0 informations
```

Pyright note: a PowerShell advisory wrapper exists at
`tools/run_pyright_advisory.ps1`, but this baseline ran on macOS and used the
requested cross-platform Python invocation, `python3 -m pyright`.

### `python3 tools/check_protected_surfaces.py --base origin/main`

```text
Protected Surface Gate
base: origin/main
head: HEAD
changed_paths: 0
forbidden: 0
warnings: 0

result: passed
```

### `git diff --check`

Result: passed with no output.

## Skipped Checks

- No live MTGA parser run was executed.
- No live workbook, webhook, or Apps Script integration run was executed.
- GitHub Actions were not re-run by this local baseline pass.
- The PowerShell-only Pyright advisory wrapper was not run on macOS.

## Residual Risks

- This report is a local validation snapshot, not a replacement for CI after a
  PR is opened.
- The protected-surface gate was run against `origin/main` while the branch had
  no changed paths. Future hardening child issues must rerun it after their
  scoped changes.
- Pyright is currently clean, so future advisory reports should distinguish new
  findings from tool/config drift.
- The repo-wide hardening wave still needs scoped child issues and a final
  post-hardening comparison report before tracker #82 can be considered done.

## Next Selected Hardening Child Issue

Next selected queue item from tracker #82:

```text
Secret and private-marker scanner
```

Recommended next child issue title:

```text
[hardening] Secret and private-marker scanner
```

Selected scope:

- Add a deterministic scanner for webhook URLs, API keys, tokens, local file
  paths, raw Player.log markers, failed-post artifacts, runtime artifacts, and
  workbook exports.
- Keep committed fixtures sanitized.
- Keep the tool deterministic and focused.
- Do not change parser truth, workbook schema, webhook payloads, Apps Script,
  environment semantics, or generated/private artifacts.

## Workflow Handoff

Next recommended role: Codex A: Thinker, then Codex B if the child issue needs
a contract before implementation.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex A: Thinker for the next repo-wide hardening child issue under tracker #82.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Baseline issue:
https://github.com/Tahjali11/Mythic-Edge/issues/83

Baseline artifact:
docs/contract_test_reports/repo_wide_hardening_baseline.md

Selected child issue:
[hardening] Secret and private-marker scanner

Goal:
Create the problem representation for a deterministic secret and private-marker scanner. The scanner should detect webhook URLs, API keys, tokens, local file paths, raw Player.log markers, failed-post artifacts, runtime artifacts, generated data, and workbook exports before they enter commits or PRs.

Include:
- scope
- protected surfaces
- expected scanner inputs and outputs
- allowed false-positive handling
- fixture/sanitization policy
- validation plan
- whether a module contract is required
- workflow_handoff block to Codex B or C

Do not implement the scanner in the Thinker pass.
Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not target main directly.
Do not mark tracker #82 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/83"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "C"
  next_thread: "A"
  source_artifact: "repo-wide hardening workflow setup"
  target_artifact: "TBD - problem representation for secret and private-marker scanner"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "git status --short --branch"
    - "git rev-parse --short HEAD"
    - "git rev-list --left-right --count HEAD...origin/main"
    - "python3 -m pytest -q tests"
    - "python3 -m ruff check src tests tools"
    - "python3 -m pyright"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "git diff --check"
  stop_conditions:
    - "Do not implement new hardening tools in the baseline report issue."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main directly."
    - "Do not mark tracker #82 complete."
```
