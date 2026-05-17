# Repo-Wide Agent Docs Consistency Checker Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/86

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/82

## Contract

`docs/contracts/repo_wide_agent_docs_consistency_checker.md`

## Implementation Under Test

Branch: `codex/repo-wide-hardening-run`

Files under review:

- `docs/contracts/repo_wide_agent_docs_consistency_checker.md`
- `docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md`
- `docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md`
- `tools/check_agent_docs.py`
- `tests/test_check_agent_docs.py`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/*.md`
- `docs/templates/*.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-*.md`

## Findings First

No blocking finding remains after the Codex D fixer pass.

Resolved finding:

- `tools/check_agent_docs.py` now verifies that
  `docs/codex_module_workflow.md` describes Codex D as loopback-only.
- The invariant is separate from the existing `routing.normal_path` check, so
  preserving `A -> B -> C -> E -> F -> G` is not enough if the active workflow
  doc drops the D loopback-only prose.
- `tests/test_check_agent_docs.py` now has focused regression coverage that
  removes only the D loopback prose while keeping `routing.normal_path`
  unchanged and expects a deterministic `normal_path_mismatch` finding.

Codex E re-review result:

- Confirmed the previous blocker is fixed.
- Confirmed the targeted reviewer mutation now fails with
  `normal_path_mismatch` against `docs/codex_module_workflow.md`.
- Confirmed live repo-mode agent-doc checking still passes.
- Confirmed the checker package secret scan is warning-only with no forbidden
  findings.
- Confirmed no CI, parser/runtime/workbook/App Script, local artifact, or
  protected downstream surfaces changed.

## Contract-Test Verdict

No blocking findings. Ready for Codex F: Module Submitter.

The previous blocking missed invariant has a focused implementation fix and
direct regression coverage. The fixer pass did not rewrite agent docs, edit CI,
add dependencies, or touch parser/runtime/workbook/App Script behavior.

## Confirmed Matches

- `tools/check_agent_docs.py` provides deterministic repo-mode checking.
- The implementation uses standard-library-only parsing; no YAML dependency was
  added.
- CLI supports `python3 tools/check_agent_docs.py`, `--repo-root`, and
  `--format text|json`.
- Required governance files are checked.
- Repo-local references in backticks and Markdown links are checked
  conservatively.
- URLs, anchors, shell-command-looking references, placeholders, and irrelevant
  non-file references are ignored by the reference extractor.
- Glob references require at least one matching file.
- Archived docs are ignored unless active docs cite them in a way that could
  look authoritative.
- A-G role names and Codex H auxiliary role are compared against the contract
  registry.
- H remains auxiliary and outside the normal path.
- D remains loopback-only and outside the normal happy path.
- `docs/agent_rules.yml` and `docs/codex_module_workflow.md` preserve
  `A -> B -> C -> E -> F -> G`.
- Removing D loopback-only prose from the workflow doc now fails even when the
  normal path remains intact.
- Authority-order checks verify critical relative ordering without requiring
  full prose equality.
- `docs/templates/workflow_handoff.md` required keys and `next_thread` values
  are checked.
- `docs/agent_rules.yml` `prompt_schema.required` and
  `handoff_schema.required` are checked.
- `.github/ISSUE_TEMPLATE/module_workflow.yml` source/target artifact, branch,
  protected surfaces, validation, and stop-condition fields are checked.
- ADR status sets, numbered ADR status lines, README index entries, README
  status matches, and recommended-field warnings are checked.
- Protected-surface and external-surface boundary text checks cover the
  contract terms.
- Warnings exit `0`; error findings exit `1`; configuration/runtime errors
  exit `2`.
- Findings are sorted deterministically.
- `.github/workflows/repo-checks.yml` was not edited and
  `check_agent_docs.py` was not wired into CI.
- No parser behavior, parser state final reconciliation, workbook schema,
  webhook payload shape, Apps Script behavior, parser event classes,
  match/game identity, deduplication, secrets, environment variables, raw logs,
  generated data, runtime status files, failed posts, workbook exports, or
  protected surfaces outside this contract changed.

## Missing Tests

No blocking test gap remains for the reviewed finding.

Added focused coverage:

- `test_missing_d_loopback_workflow_prose_is_error`

Non-blocking gaps:

- Markdown parsing remains intentionally conservative and is not a complete
  Markdown link validator.
- JSON output has a smoke check but no separate schema contract test beyond the
  current implementation tests.
- CI integration remains intentionally deferred.

## Drift Classification

- Contract drift: none found.
- Implementation drift: resolved; the D loopback-only prose invariant is now
  checked.
- Test drift: resolved; focused regression coverage now exists.
- CI drift: none found.
- Protected-surface drift: none found.
- Tracker drift: none found; issue #86 and tracker #82 remain open.

## Validation Results

```bash
python3 -m pytest -q tests/test_check_agent_docs.py
```

Result: `17 passed in 0.08s`

```bash
python3 tools/check_agent_docs.py
```

Result:

```text
Agent Docs Consistency Check
mode: repo
checked_files: 29
errors: 0
warnings: 0

result: passed
```

```bash
python3 tools/check_agent_docs.py --format json
```

Result: JSON output rendered successfully with `result: passed`, `errors: 0`,
and `warnings: 0`.

```bash
python3 -m pytest -q tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py
```

Result: `77 passed in 0.05s`

```bash
python3 tools/check_secret_patterns.py --base origin/main
```

Result: warning-only report, exit `0`, `scanned_paths: 6`,
`forbidden: 0`, `warnings: 19`.

```bash
python3 tools/check_protected_surfaces.py --base origin/main
```

Result: passed, `changed_paths: 6`, `forbidden: 0`, `warnings: 0`.

```bash
python3 -m ruff check src tests tools
```

Result: `All checks passed!`

```bash
git diff --check
```

Result: passed with no output.

```bash
python3 -m pytest -q tests
```

Result: `710 passed in 1.09s`

Reviewer mutation:

- Removed the D loopback-only sentence from a temporary minimal
  `docs/codex_module_workflow.md` fixture.
- Preserved `routing.normal_path` as `A -> B -> C -> E -> F -> G`.
- `checker.run_check()` returned exit code `1` with
  `normal_path_mismatch` for `docs/codex_module_workflow.md`.

Additional fixer checks:

```bash
printf 'tools/check_agent_docs.py\ntests/test_check_agent_docs.py\ndocs/contracts/repo_wide_agent_docs_consistency_checker.md\ndocs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md\ndocs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Result: warning-only report, exit `0`, `scanned_paths: 5`,
`forbidden: 0`, `warnings: 3`.

## Changed/Untracked File Awareness

Untracked review package:

- `docs/contracts/repo_wide_agent_docs_consistency_checker.md`
- `docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md`
- `docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md`
- `tests/test_check_agent_docs.py`
- `tools/check_agent_docs.py`

No tracked protected downstream files were modified during this fixer pass.

## Remaining Non-Blocking Gaps

- No CI run was triggered.
- No live MTGA parser run was executed.
- No live workbook, webhook, or Apps Script integration was inspected.
- `check_agent_docs.py` remains local/advisory and is not a CI gate.
- The checker intentionally validates concrete governance invariants rather
  than proving every sentence of the agent docs semantically.

## Next Recommended Role

Codex F: Module Submitter.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/86"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md"
  target_artifact: "module submitter package for repo-wide agent docs consistency checker"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  verdict: "No blocking findings. Ready for Codex F: Module Submitter."
  validation:
    - "python3 -m pytest -q tests/test_check_agent_docs.py -> 17 passed in 0.08s"
    - "python3 tools/check_agent_docs.py -> passed, checked_files 29, errors 0, warnings 0"
    - "python3 tools/check_agent_docs.py --format json -> passed, result passed"
    - "python3 -m pytest -q tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py -> 77 passed in 0.05s"
    - "python3 tools/check_secret_patterns.py --base origin/main -> warning-only exit 0, scanned_paths 6, forbidden 0, warnings 19"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed, changed_paths 6, forbidden 0, warnings 0"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed with no output"
    - "python3 -m pytest -q tests -> 710 passed in 1.09s"
    - "reviewer mutation removing D loopback prose -> normal_path_mismatch, exit 1"
    - "agent-checker package paths-from-stdin secret scan -> warning-only exit 0, scanned_paths 5, forbidden 0, warnings 3"
  stop_conditions:
    - "Do not stage, commit, merge, target main, or mark tracker #82 complete."
    - "Do not edit CI unless separately authorized."
    - "Do not rewrite agent docs for this fixer unless the contract-test finding cannot be resolved in the checker/tests."
    - "Do not add dependencies."
    - "Do not change parser/runtime/workbook/App Script behavior."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
```
