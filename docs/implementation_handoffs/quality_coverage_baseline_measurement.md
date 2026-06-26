# Quality Coverage Baseline Measurement

## Role

Codex C: Contract-Limited Measurement / Report Implementer for issue #573.

## Source Artifacts

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/573
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Active parser evidence tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Contract: `docs/contracts/quality_coverage_baseline_ratchet_design.md`
- Prior PR: https://github.com/Tahjali11/Mythic-Edge/pull/572

## Local State

- Primary checkout state: dirty, on a gone branch, with unrelated governance WIP.
- Measurement checkout: clean sibling worktree on branch `codex/quality-coverage-baseline-measurement-573`.
- Measured source ref: `origin/main`.
- Measured commit: `f31923ec2b0da629be3eeb8e7971b21aa57fe9fc`.
- Commit title: `Add coverage baseline ratchet design contract (#572)`.
- Live state checked before measurement:
  - #566 tracker open.
  - #568 project roadmap open.
  - #388 parser evidence tracker open.
  - PR #572 merged to `main` at the measured commit.
  - No open pull requests matched `coverage` at measurement time.

## Measurement Command

Command ID: `quality_coverage_baseline.local_pytest_cov.v1`

Branch coverage: enabled by `pyproject.toml`.

Sanitized environment label: `local-macos-python-3.14.3-arm64`.

Run ID: `2026-06-26-f31923e-local-macos-r1`.

```bash
RUN_ID="2026-06-26-f31923e-local-macos-r1"
RUN_DIR="_review_/quality_coverage_baseline/${RUN_ID}"
mkdir -p "$RUN_DIR"
COVERAGE_FILE="$RUN_DIR/.coverage" python3 -m pytest -q tests \
  --cov=src/mythic_edge_parser \
  --cov-report=term-missing \
  --cov-report="xml:${RUN_DIR}/coverage.xml" \
  > "$RUN_DIR/coverage_terminal.txt" 2>&1
```

Coverage command exit code: `0`.

No `--cov-fail-under` threshold was used.

## Sanitized Aggregate Result

Status: `passed_advisory_measurement`.

The raw coverage XML was parsed locally for aggregate values only. Raw coverage files and the terminal coverage log remain local and ignored.

| Metric | Value |
| --- | ---: |
| Tests passed | 1,949 |
| Total line coverage | 87.56% |
| Covered statements | 22,383 |
| Total statements | 25,564 |
| Missing statements | 3,181 |
| Total branch coverage | 74.87% |
| Covered branches | 7,745 |
| Total branches | 10,344 |
| Missing branches | 2,599 |
| Measured file count | 116 |
| Measured package count | 9 |

## Raw Output Handling

- Raw output directory: `_review_/quality_coverage_baseline/2026-06-26-f31923e-local-macos-r1/`.
- `_review_*/` is ignored by `.gitignore`.
- `git check-ignore` confirmed the local coverage database, XML report, and terminal capture in the accepted run directory are ignored by `.gitignore:23`.
- Raw coverage outputs were not staged and are not part of this report artifact.
- A shell-wrapper attempt before the accepted run used an invalid zsh variable name and was discarded; no public aggregate values were derived from that attempt.

## Validation Run

- `git status --short --branch` in the sibling worktree showed branch
  `codex/quality-coverage-baseline-measurement-573` at the measured commit.
- `git fetch --prune origin` completed before worktree creation.
- `gh issue view 573`, `gh issue view 566`, `gh issue view 568`,
  `gh issue view 388`, and `gh pr view 572` were inspected before
  measurement.
- `gh pr list --state open --search "coverage"` returned no open matching
  pull requests.
- Coverage command exited `0`.
- Aggregate coverage values were parsed from the local ignored XML report;
  raw file-by-file missing-line output was not copied into this artifact.
- `git check-ignore` confirmed the accepted run's local coverage database,
  XML report, and terminal capture are ignored by `.gitignore:23`.
- `printf '%s\n' docs/implementation_handoffs/quality_coverage_baseline_measurement.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
  passed: `forbidden: 0`, `warnings: 0`.
- `printf '%s\n' docs/implementation_handoffs/quality_coverage_baseline_measurement.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
  passed: `forbidden: 0`, `warnings: 0`.
- `git diff --check` passed.
- New-file whitespace check using
  `git diff --check --no-index /dev/null docs/implementation_handoffs/quality_coverage_baseline_measurement.md`
  produced no whitespace output. The command's raw `--no-index` exit code was
  `1` because the new file differs from `/dev/null`, which is expected.
- ASCII, trailing-whitespace, and final-newline check for this report passed.
- `git status --short` showed only this report as a non-ignored untracked file.
- `git status --short --ignored` confirmed `_review_/` is ignored.

## Files Changed

- `docs/implementation_handoffs/quality_coverage_baseline_measurement.md`

No product code, tests, CI, parser behavior, corpus metadata, workbook, webhook, Apps Script, analytics, AI, or runtime behavior was changed.

## Non-Claims

This measurement does not claim:

- parser truth;
- parser behavior readiness;
- tracker #388 activation readiness;
- issue #381 activation readiness;
- fixture promotion readiness;
- corpus readiness;
- release readiness;
- deploy readiness;
- production readiness;
- security assurance;
- privacy assurance;
- analytics truth;
- AI truth;
- coaching truth.

## Remaining Risks

- This is one local advisory measurement on the named commit and sanitized environment only.
- The Python version differs from the current GitHub Actions Windows runner shape, so later CI-facing baseline work should either remeasure in CI or explicitly account for environment differences.
- Coverage is execution evidence only. It does not prove parser correctness, corpus fixture validity, or private evidence readiness.
- No global floor, protected-surface floor, new-code expectation, or CI enforcement was selected or activated.

## Recommended Next Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer / Contract Tester for issue #573.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/573

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Active parser evidence tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Contract:
docs/contracts/quality_coverage_baseline_ratchet_design.md

Implementation handoff / measurement report:
docs/implementation_handoffs/quality_coverage_baseline_measurement.md

Goal:
Review the sanitized advisory coverage baseline measurement against the #569 contract and issue #573. Lead with findings, if any. Verify that the report records only public-safe aggregate coverage evidence, uses the approved non-enforcing command shape, keeps raw coverage outputs local and ignored, does not use --cov-fail-under, does not change CI or product code, and preserves all parser truth/readiness, corpus readiness, release readiness, security assurance, privacy assurance, analytics truth, AI truth, and coaching truth non-claims.

Suggested validation:
- Inspect `docs/implementation_handoffs/quality_coverage_baseline_measurement.md`.
- Confirm raw coverage outputs are not tracked or staged.
- Run `printf '%s\n' docs/implementation_handoffs/quality_coverage_baseline_measurement.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`.
- Run `printf '%s\n' docs/implementation_handoffs/quality_coverage_baseline_measurement.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`.
- Run `git diff --check`.

Do not implement product code.
Do not change CI.
Do not activate coverage enforcement.
Do not use --cov-fail-under.
Do not commit raw coverage outputs, terminal logs, local absolute paths, or missing-line reports.
Do not activate #388 or #381.
Do not claim parser truth/readiness, corpus readiness, release readiness, deploy readiness, production readiness, security assurance, privacy assurance, analytics truth, AI truth, or coaching truth.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/573"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  active_parser_evidence_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/569"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/572"
  previous_merge_commit: "f31923ec2b0da629be3eeb8e7971b21aa57fe9fc"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_coverage_baseline_ratchet_design.md"
  target_artifact: "docs/implementation_handoffs/quality_coverage_baseline_measurement.md"
  verdict: "advisory_coverage_baseline_measurement_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-coverage-baseline-measurement-573"
  measured_commit: "f31923ec2b0da629be3eeb8e7971b21aa57fe9fc"
  coverage_measurement_exit_code: 0
  total_line_coverage_percent: 87.56
  total_branch_coverage_percent: 74.87
  tests_passed: 1949
  ci_change_authorized: false
  coverage_enforcement_authorized: false
  coverage_fail_under_used: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
```
