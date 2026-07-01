# Code Hardening Protected-Surface Gate Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/34

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Source contract: `docs/contracts/code_hardening_protected_surface_gate.md`

Target branch: `codex/code-hardening-suite`

Role: Codex C: Module Implementer

Risk tier: Medium

## Summary Of Implementation Comparison

The initial comparison found a clear contract mismatch: the branch had the
contract artifact, but no executable protected-surface gate and no focused
classification tests. The implementation now adds a small read-only gate,
focused tests, and conservative pull-request CI wiring.

Files added:

- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md`

Files changed:

- `.github/workflows/repo-checks.yml`
- `tools/build_markdown_pdf.py`

The `tools/build_markdown_pdf.py` change is style-only. It was required because
the contract validation scope includes `python3 -m ruff check tools tests`, and
the existing file had Ruff import/line-length findings once `tools` entered the
lint surface.

## Findings First

### Resolved: missing executable gate

Contract requirement:

- public command `python3 tools/check_protected_surfaces.py --base <git-ref>`
- committed branch diff comparison from `<base>...HEAD`
- path-based classification
- forbidden artifacts exit `1`
- protected warnings exit `0`
- configuration/git errors exit `2`
- stable plain-text report

Initial state:

- `tools/check_protected_surfaces.py` did not exist.

Resolution:

- Added `tools/check_protected_surfaces.py`.
- The tool uses `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`.
- Deleted files are excluded from the changed-file list to avoid false
  forbidden failures for files removed by the branch.
- The tool is read-only and does not scan contents, inspect untracked files,
  mutate runtime state, stage, commit, fetch network resources, post webhooks,
  or touch workbook/App Script/parser behavior.

### Resolved: missing focused tests

Contract requirement:

- tests for path normalization, forbidden classification, protected warning
  classification, precedence, exit behavior, report shape, git diff
  integration, and CI/local integration if implemented.

Initial state:

- `tests/test_check_protected_surfaces.py` did not exist.

Resolution:

- Added `tests/test_check_protected_surfaces.py` with focused tests covering:
  path normalization, Windows separators, leading `./`, repeated slashes,
  nonexistent paths, forbidden categories, protected warnings, allowed
  false positives, forbidden-over-warning precedence, exit-code behavior,
  report fields, git diff command construction, git failure handling,
  missing-base usage error, stdin path seam, and CI workflow invocation.

### Resolved: missing CI invocation

Contract requirement:

- expected first CI integration runs on `pull_request`, uses the PR base ref,
  and fails only for forbidden files.

Initial state:

- `.github/workflows/repo-checks.yml` ran tests and Ruff only.

Resolution:

- Added a pull-request-only step:

```yaml
py tools/check_protected_surfaces.py --base origin/${{ github.base_ref }}
```

- Added `fetch-depth: 0` to make base comparison available.
- Kept push-event gate behavior out of scope because base detection is
  ambiguous for push events in the first rollout.

## Confirmed Matches

- Owning layer remains repository coordination and agent workflow.
- The gate does not own parser truth, workbook schema truth, webhook payload
  truth, Apps Script truth, match/game identity truth, final reconciliation, or
  runtime status truth.
- The public CLI uses an explicit `--base` argument.
- The default report is stable plain text and includes gate name, base, head,
  changed path count, forbidden count, warning count, findings, and result.
- Exit code `0` is returned for allowed-only and warnings-only reports.
- Exit code `1` is returned when a forbidden path is present.
- Exit code `2` is returned for usage/configuration/git errors.
- Path normalization converts backslashes to forward slashes, strips leading
  `./`, strips repeated leading slashes, and collapses redundant `.` segments.
- Matching is case-sensitive.
- Classification tests do not require paths to exist.
- Forbidden paths take precedence over protected warnings.
- Sanitized fixtures under `tests/fixtures/**` are not forbidden merely because
  they use `.log` or workbook extensions.
- Protected-surface warnings are visible but non-failing.
- No content secret scanning was added.
- No untracked-file scan was added.
- No parser/runtime/workbook/App Script behavior was changed.

## Contract Mismatches

No unresolved implementation mismatch is known after this pass.

The branch still has one workflow/source-of-truth mismatch recorded by the
contract itself: issue #34 names `docs/agent_rules.yml`, but that file is not
present on `codex/code-hardening-suite`. This pass did not add it because the
contract says to add or sync it only through a separate explicitly authorized
workflow change. The first gate therefore encodes the contract policy table in
the tool.

## Missing Safeguards

No blocking missing safeguard remains for the first rollout.

Intentionally out of scope for this implementation:

- content-based secret scanning
- untracked-file scanning
- making protected warnings fail CI
- semantic validation of parser, workbook, webhook, or Apps Script behavior
- automatic PR template interpretation
- reading GitHub issue bodies to decide whether a protected change is
  authorized
- parsing `docs/agent_rules.yml`

## Missing Or Weak Tests

No blocking missing focused test remains for the contracted first rollout.

Non-blocking test gaps:

- The PowerShell wrappers are not tested for gate invocation because this pass
  did not integrate the gate into `tools/run_repo_checks.ps1` or
  `tools/run_touched_file_checks.ps1`.
- JSON or GitHub annotation output is untested because neither optional output
  mode was implemented.
- Push-event CI behavior is untested because the gate is deliberately
  pull-request-only in the first CI rollout.

## Validation Evidence

Commands run:

```bash
python3 -m pytest -q tests/test_check_protected_surfaces.py
```

Result:

```text
48 passed in 0.07s
```

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Result:

```text
Protected Surface Gate
base: origin/codex/code-hardening-suite
head: HEAD
changed_paths: 0
forbidden: 0
warnings: 0

result: passed
```

```bash
python3 -m ruff check tools tests
```

Result:

```text
All checks passed!
```

```bash
git diff --check
```

Result: passed with no output.

Additional confidence checks run:

```bash
python3 -m ruff check src tests tools
```

Result:

```text
All checks passed!
```

```bash
git diff --name-only -- src tools/google_apps_script main.py live_print_filtered_v11_match_summary.py data workbook_exports exports
```

Result: passed with no output.

```bash
python3 -m pytest -q
```

Result:

```text
361 passed, 1 failed
```

Failure:

```text
tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook
assert payload["log_path"] == "Player.log"
actual: "C:\\Users\\<redacted>\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log"
```

This full-suite failure is outside issue #34. It touches runner startup
diagnostics and Windows-style path display, not the protected-surface gate. It
was not fixed in this pass because runtime behavior is a protected surface and
the issue scope is the hardening gate.

## Module Fixer Follow-Up

Codex D addressed the contract-test blocker reported in
`docs/contract_test_reports/code_hardening_protected_surface_gate.md`.

Finding classification: implementation bug under existing contract, plus a
focused missing-test gap.

Files changed by the fixer follow-up:

- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md`
- `docs/contract_test_reports/code_hardening_protected_surface_gate.md`

Fix summary:

- Reused the existing documented-fixture helper for the `local_mtga_log` rule.
- Added focused coverage for `tests/fixtures/Player.log`,
  `tests/fixtures/sample.Player.log`, and
  `tests/fixtures/sample.player.log`.
- Preserved forbidden behavior for real `Player.log`-style files outside
  `tests/fixtures/**` and for `data/match_logs/**`.

Post-fix validation:

```bash
python3 -m pytest -q tests/test_check_protected_surfaces.py
# Pass: 54 passed in 0.04s.

printf 'tests/fixtures/Player.log\ntests/fixtures/sample.Player.log\ntests/fixtures/sample.player.log\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# Pass: forbidden: 0, warnings: 0, result: passed.

printf 'Player.log\ndata/match_logs/raw.jsonl\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# Expected fail: forbidden: 2, result: failed.

python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
# Pass: changed_paths: 0, forbidden: 0, warnings: 0, result: passed.

python3 -m ruff check tools tests
# Pass: All checks passed!

python3 -m ruff check src tests tools
# Pass: All checks passed!

git diff --check
# Pass: no output.

git diff --name-only -- src tools/google_apps_script main.py live_print_filtered_v11_match_summary.py data workbook_exports exports .github/workflows tools
# Output: .github/workflows/repo-checks.yml and tools/build_markdown_pdf.py.
# These were pre-existing reviewed implementation-scope changes.

python3 -m pytest -q
# Expected unrelated failure: 1 failed, 368 passed in 1.91s.
# Failure: tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook.
```

## Still-Unverified Layers

- GitHub Actions runtime behavior has not been observed in CI yet.
- Submitter/deployer PR checks have not run.
- The full test suite currently has one unrelated runner startup path-display
  failure in `tests/test_runner.py`.
- The missing `docs/agent_rules.yml` rule-index layer remains unresolved by
  contract direction.
- The gate has not been exercised against a real PR containing forbidden
  committed artifacts.
- The gate has not been exercised against a real PR containing protected
  warnings only.

## Protected Surfaces Verification

This implementation did not edit parser source, workbook schema, webhook
payload shape, Apps Script behavior, parser event classes, extractor behavior,
match identity, game identity, deduplication, final reconciliation, secrets,
environment variables, raw logs, generated data, runtime status files, failed
posts, or workbook exports.

CI workflow behavior changed only to add the contracted pull-request gate and
lint `tools` along with `src` and `tests`.

## Next Recommended Role

Next recommended role: Codex E: Module Reviewer in contract-test mode.

Reason: the implementation now has a concrete tool, focused tests, CI wiring,
and validation evidence. Reviewer should verify the contract semantics,
especially fail-vs-warn classification, path normalization, exit codes, and
the conservative CI invocation.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #34:
https://github.com/Tahjali11/Mythic-Edge/issues/34

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Use:
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- .github/workflows/repo-checks.yml
- tools/run_repo_checks.ps1
- tools/run_touched_file_checks.ps1
- .github/pull_request_template.md
- docs/agent_constitution.md
- docs/codex_module_workflow.md

Goal:
Verify the Module Implementer patch against the protected-surface diff gate contract.

Confirm:
- The gate is repo-workflow tooling only and does not become parser, workbook, webhook, Apps Script, runtime, or deployment truth.
- `python3 tools/check_protected_surfaces.py --base <git-ref>` is the stable public CLI.
- Changed paths are collected with `<base>...HEAD`.
- Deleted files do not create false forbidden failures in the first version.
- Path normalization handles Windows separators, leading `./`, repeated leading slashes, and paths that do not exist.
- Matching remains case-sensitive.
- Forbidden committed artifacts fail with exit code `1`.
- Protected-surface changes warn/report but return exit code `0`.
- Usage/configuration/git errors return exit code `2`.
- Forbidden classifications take precedence over protected warnings.
- Report output includes gate name, base, head, changed count, forbidden count, warning count, category ids, normalized paths, and result.
- CI integration is pull-request-only, uses the PR base ref, and does not make protected warnings fail.
- The implementation does not scan file contents or untracked files.
- Focused tests cover the contract-required classification, report, exit, git diff, and CI behavior.
- No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_check_protected_surfaces.py
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
python3 -m ruff check tools tests
git diff --check

If feasible, also run:
python3 -m pytest -q
python3 -m ruff check src tests tools

Known validation context from Codex C:
- Focused protected-surface gate tests passed.
- `python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite` passed.
- `python3 -m ruff check tools tests` passed.
- `git diff --check` passed.
- `python3 -m ruff check src tests tools` passed.
- Full `python3 -m pytest -q` has one unrelated failure in `tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook`.

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not stage, commit, merge, or target main.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/34"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/code_hardening_protected_surface_gate.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "python3 -m pytest -q tests/test_check_protected_surfaces.py"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite"
    - "python3 -m ruff check tools tests"
    - "git diff --check"
    - "python3 -m ruff check src tests tools"
    - "python3 -m pytest -q (fails: tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook)"
  stop_conditions:
    - "Do not make ambiguous protected-surface warnings fail CI without explicit user approval."
    - "Do not add content secret scanning unless routed through a new contract."
    - "Do not scan untracked files by default unless the contract is amended."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main; hardening PR work belongs on codex/code-hardening-suite."
```
