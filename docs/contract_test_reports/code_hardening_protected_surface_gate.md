# Code Hardening Protected-Surface Gate Contract-Test Report

## Findings

No blocking findings.

The prior blocking fixture-exemption mismatch is resolved by the Module Fixer
follow-up.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/34

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

`docs/contracts/code_hardening_protected_surface_gate.md`

## Implementation Under Test

Branch/worktree: `codex/code-hardening-suite`

Worktree path:
`/Users/<redacted>/Documents/New project/Mythic-Edge-code-hardening-suite`

Implementation handoff:
`docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md`

Reviewed implementation surfaces:

- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `.github/workflows/repo-checks.yml`
- `tools/build_markdown_pdf.py`

Changed-file scope reviewed:

- `.github/workflows/repo-checks.yml`
- `tools/build_markdown_pdf.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md`
- `docs/contract_test_reports/code_hardening_protected_surface_gate.md`

Runtime/parser/workbook/App Script implementation code was not changed.

## Contract Summary

The protected-surface diff gate is repo-workflow tooling. It inspects committed
branch diffs against an explicit base ref, fails clearly forbidden committed
artifacts, warns on ambiguous protected-source changes, and stays read-only.
It must not scan file contents or untracked files in the first version, and it
must not become parser, workbook, webhook, Apps Script, runtime, deployment,
or secret-content truth.

## Module Fixer Follow-Up

Codex D addressed the previous Codex E blocker:

- Documented sanitized fixture paths under `tests/fixtures/**` no longer fail
  solely because they match local MTGA log filename patterns.
- `tests/fixtures/Player.log`,
  `tests/fixtures/sample.Player.log`, and
  `tests/fixtures/sample.player.log` now classify as allowed.
- Real `Player.log`-style paths outside `tests/fixtures/**` still fail as
  `local_mtga_log`.
- `data/match_logs/**` still fails as `local_mtga_log`.
- The fixture exemption remains limited to documented `tests/fixtures/**`
  behavior.
- The implementation handoff and this contract-test report record the Module
  Fixer follow-up.

## Checks Run

```bash
python3 -m pytest -q tests/test_check_protected_surfaces.py
printf 'tests/fixtures/Player.log\ntests/fixtures/sample.Player.log\ntests/fixtures/sample.player.log\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'Player.log\nsample.Player.log\ndata/match_logs/raw.jsonl\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'src/mythic_edge_parser/app/state.py\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
python3 -m ruff check tools tests
python3 -m ruff check src tests tools
git diff --check
git diff --name-only -- src tools/google_apps_script main.py live_print_filtered_v11_match_summary.py data workbook_exports exports .github/workflows tools
python3 -m pytest -q
```

## Results

- `python3 -m pytest -q tests/test_check_protected_surfaces.py`
  -> `54 passed in 0.10s`.
- Fixture stdin repro with `tests/fixtures/Player.log`,
  `tests/fixtures/sample.Player.log`, and
  `tests/fixtures/sample.player.log`
  -> `changed_paths: 3`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- Non-fixture control with `Player.log`, `sample.Player.log`, and
  `data/match_logs/raw.jsonl`
  -> expected failure: `changed_paths: 3`, `forbidden: 3`, `warnings: 0`,
  `result: failed`.
- Warning-only protected-surface control with
  `src/mythic_edge_parser/app/state.py`
  -> `forbidden: 0`, `warnings: 1`, `result: passed`.
- `python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite`
  -> `changed_paths: 0`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- `python3 -m ruff check tools tests` -> `All checks passed!`.
- `python3 -m ruff check src tests tools` -> `All checks passed!`.
- `git diff --check` -> passed with no output.
- `git diff --name-only -- src tools/google_apps_script main.py live_print_filtered_v11_match_summary.py data workbook_exports exports .github/workflows tools`
  -> `.github/workflows/repo-checks.yml` and `tools/build_markdown_pdf.py`.
- `python3 -m pytest -q` -> `1 failed, 368 passed in 1.16s`.

Full-suite failure:

```text
tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook
assert payload["log_path"] == "Player.log"
actual: "C:\\Users\\<redacted>\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log"
```

The full-suite failure is the known unrelated runner path-display failure. It
is outside issue #34 and was not fixed in this hardening-gate pass.

## Contract-Test Verdict

Pass.

The Module Fixer follow-up satisfies the protected-surface diff gate contract.
The prior sanitized fixture mismatch is resolved, and no new blocking finding
was found.

## Confirmed Contract Matches

- The gate remains repo-workflow tooling only and does not become parser,
  workbook, webhook, Apps Script, runtime, or deployment truth.
- `python3 tools/check_protected_surfaces.py --base <git-ref>` remains the
  stable public CLI.
- Changed paths are collected with `<base>...HEAD`.
- Deleted files do not create false forbidden failures in the first version.
- Path normalization handles Windows separators, leading `./`, repeated
  leading slashes, redundant `.` segments, and paths that do not exist.
- Matching remains case-sensitive.
- Documented sanitized fixtures under `tests/fixtures/**` do not warn or fail
  solely because they match local MTGA log filename patterns.
- Real `Player.log`-style paths outside `tests/fixtures/**` still fail as
  `local_mtga_log`.
- `data/match_logs/**` still fails as `local_mtga_log`.
- Forbidden committed artifacts fail with exit code `1`.
- Protected-surface changes warn/report with exit code `0`.
- Usage/configuration/git errors return exit code `2`.
- Forbidden classifications take precedence over protected warnings.
- Report output includes gate name, base, head, changed count, forbidden
  count, warning count, category ids, normalized paths, and result.
- CI integration remains pull-request-only and uses the PR base ref.
- Protected warnings do not fail CI.
- The implementation does not scan file contents.
- The implementation does not scan untracked files by default.
- Focused tests cover the contracted classification, report, exit, git diff,
  CI behavior, and fixture exemption behavior.
- No parser behavior, parser state final reconciliation, workbook schema,
  webhook payload shape, Apps Script behavior, parser event classes, extractor
  behavior, match/game identity, deduplication, final reconciliation, secrets,
  raw logs, generated data, runtime status files, failed posts, or workbook
  exports changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

The previous missing test is covered by:

- allowed Player.log-style fixture path checks in
  `tests/test_check_protected_surfaces.py`
- a focused gate-level regression that evaluates all three documented
  Player.log-style fixture names together

## Drift Notes

- No parser behavior drift found.
- No parser state final reconciliation drift found.
- No workbook schema, webhook payload, Apps Script, parser event class,
  extractor, match/game identity, deduplication, runtime artifact, failed-post,
  generated-data, raw-log, or workbook-export drift found in the reviewed
  surface.
- `.github/workflows/repo-checks.yml` changed as authorized CI wiring for the
  hardening gate.
- `tools/build_markdown_pdf.py` changed only for Ruff formatting in the new
  `tools` lint surface.
- `docs/agent_rules.yml` remains absent on `codex/code-hardening-suite`; the
  contract records this as a non-blocking source-of-truth risk for a separate
  authorized workflow.

## Remaining Non-Blocking Gaps

- GitHub Actions runtime behavior has not been observed in CI yet.
- The gate has not been exercised against a real PR containing forbidden
  committed artifacts.
- The gate has not been exercised against a real PR containing protected
  warnings only.
- PowerShell wrappers are not integrated with the gate in this first rollout.
- Content secret scanning, untracked-file scanning, GitHub annotation output,
  and protected-warning CI failures remain intentionally out of scope.
- Full test suite still has the known unrelated runner path-display failure.

## Recommendation

Approve for submitter work.

Next recommended role: Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #34 and the protected-surface diff gate.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/34

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch/worktree:
codex/code-hardening-suite
/Users/<redacted>/Documents/New project/Mythic-Edge-code-hardening-suite

Use:
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md
- docs/contract_test_reports/code_hardening_protected_surface_gate.md
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- .github/workflows/repo-checks.yml
- tools/build_markdown_pdf.py

Reviewer verdict:
No blocking findings. The protected-surface diff gate is ready for submitter work.

Submitter requirements:
- Verify current branch and changed-file scope.
- Stage only the reviewed code-hardening gate artifacts.
- Commit and push the branch.
- Open or update a draft PR targeting codex/code-hardening-suite, not main.
- Do not merge, close issue #34, or mark tracker #33 complete; those are Codex G responsibilities.

Validation to run or verify:
python3 -m pytest -q tests/test_check_protected_surfaces.py
printf 'tests/fixtures/Player.log\ntests/fixtures/sample.Player.log\ntests/fixtures/sample.player.log\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'Player.log\nsample.Player.log\ndata/match_logs/raw.jsonl\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
python3 -m ruff check tools tests
python3 -m ruff check src tests tools
git diff --check

Known unrelated validation context:
Full pytest currently fails only at tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook due to runner path-display behavior. Do not fix that in this hardening-gate submitter pass.

Do not make ambiguous protected-surface warnings fail CI without explicit user approval.
Do not add content secret scanning unless routed through a new contract.
Do not scan untracked files by default unless the contract is amended.
Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not merge, close issue #34, mark tracker #33 complete, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/34"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/code_hardening_protected_surface_gate.md"
  target_artifact: "docs/contract_test_reports/code_hardening_protected_surface_gate.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "python3 -m pytest -q tests/test_check_protected_surfaces.py -> 54 passed in 0.10s"
    - "fixture stdin repro -> changed_paths: 3, forbidden: 0, warnings: 0, result: passed"
    - "non-fixture control -> changed_paths: 3, forbidden: 3, warnings: 0, result: failed as expected"
    - "warning-only protected-surface control -> forbidden: 0, warnings: 1, result: passed"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite -> changed_paths: 0, forbidden: 0, warnings: 0, result: passed"
    - "python3 -m ruff check tools tests -> All checks passed!"
    - "python3 -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed with no output"
    - "python3 -m pytest -q -> 1 failed, 368 passed in 1.16s: tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook"
  stop_conditions:
    - "Do not make ambiguous protected-surface warnings fail CI without explicit user approval."
    - "Do not add content secret scanning unless routed through a new contract."
    - "Do not scan untracked files by default unless the contract is amended."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not merge, close issue #34, or mark tracker #33 complete; route deployer work to Codex G."
    - "Do not target main; hardening PR work belongs on codex/code-hardening-suite."
```
