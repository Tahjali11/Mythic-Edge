# Repo-Wide Validation Selector Contract Test Report

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/87

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Contract: `docs/contracts/repo_wide_validation_selector.md`

Implementation handoff: `docs/implementation_handoffs/repo_wide_validation_selector_comparison.md`

Role performed: Codex E: Module Reviewer in contract-test mode; Codex D fixer
follow-up re-review

Branch: `codex/repo-wide-hardening-run`

Risk tier: Medium

## Findings

### Blocking

No blocking findings remain after the Codex D fixer pass.

### Resolved Previous Findings

The previous `agent_docs_checker` metadata blocker is resolved.

Confirmed behavior:

- Governance-only path reports only `governance_docs_surface` and the governance path.
- Contract/report-only path reports only `contract_or_report_docs_surface` and the contract/report path.
- Mixed governance plus contract/report paths aggregate both categories and both triggering paths.
- Focused tests cover those three cases.

The follow-up Ruff line-length blocker is resolved.

Confirmed behavior:

- The long `agent_docs_checker` reason string is wrapped.
- `python3 -m ruff check src tests tools` passes.

## Contract-Test Verdict

No blocking findings.

The validation selector package is ready for Codex F: Module Submitter.

## Confirmed Matches

- `--base` is required; missing base exits `2`.
- Changed-path mode uses `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`.
- `--paths-from-stdin` does not run `git diff`.
- `--repo-root` is honored.
- The selector recommends commands and does not run them.
- The selector avoids `validation passed`, `checks passed`, `ready to merge`, and `selection_status: passed`.
- Non-empty path sets select the protected-surface gate, secret/private-marker scan, and `git diff --check`.
- Zero changed paths select no required commands and include the baseline advisory note.
- Required path categories are represented in the implementation.
- Focused test mappings match the contract for sampled parser, workbook, webhook/output, fixture, CI/dependency, and hardening-tool paths.
- Ruff is selected as required for changed Python or dependency validation surfaces.
- Pyright is selected as recommended for source/tool/dependency changes.
- Full pytest is selected as recommended for CI/dependency changes, unmapped source changes, or multiple protected parser/runtime/workbook/output categories.
- `tools/check_agent_docs.py` selection is gated by Git-tracked file availability.
- Protected and forbidden path classifications from `tools/check_protected_surfaces.py` are surfaced as selector warnings without replacing the gate.
- Duplicate commands are emitted once with aggregated categories and paths.
- Text output includes reasons, categories, paths, warnings, and `selection_status`.
- JSON output includes the contracted top-level fields.
- CI was not edited.
- No parser/runtime/workbook/App Script behavior changed.

## Validation Results

Passed:

```bash
python3 -m pytest -q tests/test_select_validation.py
```

```text
22 passed in 0.04s
```

Passed:

```bash
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
```

Result: zero changed paths, zero required commands, baseline advisory, `selection_status: ok`.

Passed:

```bash
printf 'src/mythic_edge_parser/parsers/match_state.py\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: selected protected-surface gate, secret/private-marker scan, `git diff --check`, Ruff, focused match-state tests, recommended Pyright, and one protected-surface warning.

Passed:

```bash
printf 'AGENTS.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: `agent_docs_checker` is required and reports only `governance_docs_surface` with `AGENTS.md`.

Passed:

```bash
printf 'docs/contracts/repo_wide_validation_selector.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: `agent_docs_checker` is recommended and reports only `contract_or_report_docs_surface` with the contract path.

Passed:

```bash
printf 'AGENTS.md\ndocs/contracts/repo_wide_validation_selector.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: `agent_docs_checker` is required and reports both triggering categories and both triggering paths.

Passed:

```bash
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --format json
```

Result: JSON includes `mode`, `base`, `head`, `changed_paths`, `categories`, `recommendations`, `warnings`, `notes`, and `selection_status`.

Passed:

```bash
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
```

Result: `scanned_paths: 0`, `forbidden: 0`, `warnings: 0`, `result: passed`.

Passed:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
```

Result: `changed_paths: 0`, `forbidden: 0`, `warnings: 0`, `result: passed`.

Passed:

```bash
python3 -m ruff check src tests tools
```

Result: `All checks passed!`

Passed:

```bash
git diff --check
```

Result: no output.

Passed:

```bash
python3 tools/check_agent_docs.py
```

Result: `errors: 0`, `warnings: 0`, `result: passed`.

Passed:

```bash
python3 -m pytest -q tests
```

```text
732 passed in 1.20s
```

Passed:

```bash
python3 -m pyright
```

```text
0 errors, 0 warnings, 0 informations
```

Additional untracked-package safety checks:

```bash
printf 'docs/contracts/repo_wide_validation_selector.md\ndocs/implementation_handoffs/repo_wide_validation_selector_comparison.md\ndocs/contract_test_reports/repo_wide_validation_selector.md\ntests/test_select_validation.py\ntools/select_validation.py\n' | python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: warning-only report, exit `0`, `scanned_paths: 5`,
`forbidden: 0`, `warnings: 2`.

```bash
printf 'docs/contracts/repo_wide_validation_selector.md\ndocs/implementation_handoffs/repo_wide_validation_selector_comparison.md\ndocs/contract_test_reports/repo_wide_validation_selector.md\ntests/test_select_validation.py\ntools/select_validation.py\n' | python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: passed, `changed_paths: 5`, `forbidden: 0`, `warnings: 0`.

## Changed And Untracked File Awareness

Current branch:

```text
codex/repo-wide-hardening-run
```

Staged files:

```text
<none>
```

Untracked files observed during review:

```text
docs/contract_test_reports/repo_wide_validation_selector.md
docs/contracts/repo_wide_validation_selector.md
docs/implementation_handoffs/repo_wide_validation_selector_comparison.md
tests/test_select_validation.py
tools/select_validation.py
```

Because the #87 package is untracked, changed-file mode correctly reports zero changed paths from `git diff <base>...HEAD`. Submitter work should rerun changed-file validation after the package is committed to a PR branch.

## Protected-Surface Review

No tracked diff was present under parser/runtime/workbook/App Script behavior surfaces. CI was not edited.

Confirmed unchanged by this review:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- match/game identity
- deduplication
- secrets and environment variables
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports
- CI required/failing behavior

## Remaining Non-Blocking Gaps

- Changed-file mode validation is currently zero-diff because the #87 package is untracked. This is expected from the contracted `git diff <base>...HEAD` behavior, but submitter validation should rerun after commit.
- CI integration remains intentionally deferred.

## Next Recommended Role

Codex F: Module Submitter.

Submitter scope:

- Confirm the #87 package files are the intended submitter scope.
- Commit and prepare the package for PR review on the repo-wide hardening branch flow.
- Rerun changed-file validation after commit, because the current local package is untracked and changed-file mode therefore reports zero changed paths.
- Do not edit CI or protected parser/runtime/workbook/App Script surfaces.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/87"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/repo_wide_validation_selector.md"
  target_artifact: "Codex F submitter package for repo-wide validation selector"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  verdict: "No blocking findings remain after Codex D fixer pass."
  validation:
    - "python3 -m pytest -q tests/test_select_validation.py -> 22 passed in 0.04s"
    - "python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run -> zero changed paths, selection_status ok"
    - "printf 'src/mythic_edge_parser/parsers/match_state.py\\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin -> selection_status warning with expected focused checks"
    - "printf 'AGENTS.md\\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin -> agent_docs_checker governance metadata correct"
    - "printf 'docs/contracts/repo_wide_validation_selector.md\\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin -> agent_docs_checker contract/report metadata correct"
    - "printf 'AGENTS.md\\ndocs/contracts/repo_wide_validation_selector.md\\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin -> agent_docs_checker mixed metadata correct"
    - "python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run -> passed, scanned_paths 0"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run -> passed, changed_paths 0"
    - "python3 -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed"
    - "python3 tools/check_agent_docs.py -> passed"
    - "python3 -m pytest -q tests -> 732 passed in 1.20s"
    - "python3 -m pyright -> 0 errors"
    - "new package secret scan -> warning-only exit 0, scanned_paths 5, forbidden 0, warnings 2"
    - "new package protected-surface scan -> passed, changed_paths 5, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main or mark tracker #82 complete."
    - "Do not edit CI in #87 unless separately authorized."
    - "Rerun changed-file selector validation after commit because current package is untracked."
    - "Do not run selected validation commands from inside the selector."
    - "Do not claim selected checks passed from selector output."
    - "Do not change parser/runtime/workbook/App Script behavior or protected surfaces."
```
