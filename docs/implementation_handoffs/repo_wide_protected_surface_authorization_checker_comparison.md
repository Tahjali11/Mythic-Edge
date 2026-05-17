# Repo-Wide Protected-Surface Authorization Checker Implementation Handoff

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/90

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Contract: `docs/contracts/repo_wide_protected_surface_authorization_checker.md`

Role performed: Codex C: Module Implementer; Codex D: Module Fixer follow-up

Branch: `codex/repo-wide-hardening-run`

Risk tier: Medium

Related ADRs: N/A

## Summary Of Implementation Comparison

The current repo had the protected-surface path gate and validation selector,
but no deterministic checker for comparing protected categories against local
authorization evidence:

- `tools/check_protected_surfaces.py` owned path classification and remained
  unchanged.
- `tools/select_validation.py` selected validation commands but did not
  recommend an authorization-evidence checker.
- `tools/check_surface_authorization.py` did not exist.
- `tests/test_check_surface_authorization.py` did not exist.

This pass implemented the smallest advisory checker required by the contract.
It reads only local source files supplied with `--authorization-file`, consumes
the existing protected-surface gate for classifications, and reports whether
protected warning categories have accepted explicit authorization evidence.
It does not fetch live GitHub issue or PR data, edit CI, run semantic parser
checks, claim protected behavior is safe, or make missing authorization fail
the process.

Codex D follow-up fixed the Codex E blocking finding that negated
category-specific wording could be falsely accepted as authorization. Evidence
such as `workbook_schema not in scope` is now rejected as weak evidence and
reports `MISSING_AUTHORIZATION` plus `SCOPE_WARNING`, not `AUTHORIZED`.

## Findings

No blocking contract ambiguity was found.

Contract mismatches fixed:

- Missing `tools/check_surface_authorization.py`.
- Missing focused tests in `tests/test_check_surface_authorization.py`.
- Missing selector recommendation for the checker when protected or forbidden
  path classifications appear.
- Missing implementation handoff artifact for #90.
- Reviewer-blocking negated authorization wording could falsely authorize a
  protected category because `in scope` matched inside `not in scope`.

No parser behavior, parser state, workbook schema, webhook payload shape,
Apps Script behavior, parser event classes, match/game identity,
deduplication, secrets, environment variables, raw logs, generated data,
runtime status files, failed posts, workbook exports, CI behavior, or protected
surface path rules were changed.

## Changes Made

Implemented `tools/check_surface_authorization.py`:

- CLI:
  - `--base <git-ref>` required
  - `--repo-root <path>`
  - `--paths-from-stdin`
  - repeatable `--authorization-file kind=path`
  - optional `--format text|json`
- Modes:
  - changed-file mode uses the existing gate's
    `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD` collection
  - stdin mode reads newline-delimited paths and does not run `git diff`
- Classification:
  - imports and uses `tools/check_protected_surfaces.py`
  - treats `warning` classifications as requiring evidence
  - treats `forbidden` classifications as not authorizable
  - treats `allowed` classifications as `NOT_PROTECTED`
- Authorization evidence:
  - supports `issue`, `contract`, `handoff`, `report`, `pr`, and `generic`
    source kinds
  - applies the contracted source-kind precedence for primary evidence display
  - recognizes contracted category aliases and authorization markers
  - requires citations for `pr` and `generic` sources
  - rejects broad or weak wording such as `all protected surfaces authorized`,
    `unchanged or authorized`, `not in scope`, `out of scope`,
    `not authorized`, stop-condition-style text, and report output lines that
    would otherwise self-authorize
- Reports:
  - `AUTHORIZED`
  - `MISSING_AUTHORIZATION`
  - `FORBIDDEN_PATH`
  - `NOT_PROTECTED`
  - `UNVERIFIABLE_SOURCE`
  - `SCOPE_WARNING`
  - `authorization_status: ok|review|error`
- Exit behavior:
  - exit `0` for generated reports, including `authorization_status: review`
  - exit `2` only for usage/configuration/source-read errors
  - no exit `1` behavior

Updated `tools/select_validation.py`:

- added focused test mappings for the new checker and test file
- recommends
  `python3 tools/check_surface_authorization.py --base <base> --authorization-file issue=<issue-body-file> --authorization-file contract=<contract-file> --authorization-file pr=<pr-body-file>`
  when the existing protected-surface gate reports warning or forbidden
  classifications
- keeps the recommendation `recommended`, not required
- does not run the checker

Added `tests/test_check_surface_authorization.py`:

- missing `--base` exit behavior
- invalid git base error report
- stdin mode without `git diff`
- changed-file mode git diff command
- direct use of protected-surface gate classification helpers
- `NOT_PROTECTED`, `FORBIDDEN_PATH`, `AUTHORIZED`,
  `MISSING_AUTHORIZATION`, `UNVERIFIABLE_SOURCE`, and `SCOPE_WARNING`
  reports
- exact category ID and accepted alias authorization
- unrelated category evidence
- broad boilerplate rejection
- negated category-specific scope text rejection
- PR/generic citation requirement
- issue/contract source evidence without extra citation
- unreadable source and invalid source syntax errors
- duplicate source/path deterministic behavior
- no forbidden validation-result wording
- JSON field shape

Updated `tests/test_select_validation.py`:

- protected warning paths recommend `check_surface_authorization.py`
- forbidden paths recommend `check_surface_authorization.py`
- docs-only allowed paths do not recommend it
- recommendation includes authorization-file placeholders and remains
  `recommended`

## Interface Changes

New CLI:

```bash
python3 tools/check_surface_authorization.py --base <git-ref> --authorization-file <kind=path>
```

Optional CLI arguments:

```bash
--repo-root <path>
--paths-from-stdin
--authorization-file <kind=path>
--format text|json
```

No parser/runtime/workbook/App Script interfaces changed.

## Validation Evidence

Passed:

```bash
python3 -m pytest -q tests/test_check_surface_authorization.py
```

```text
23 passed in 0.03s
```

Passed reviewer negated-evidence repro:

```bash
printf 'src/mythic_edge_parser/app/sheet_schema.py\n' | python3 tools/check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=<(printf 'workbook_schema not in scope\n')
```

```text
authorized: 0
missing_authorization: 1
scope_warnings: 1
MISSING_AUTHORIZATION workbook_schema src/mythic_edge_parser/app/sheet_schema.py - No accepted authorization evidence found.
SCOPE_WARNING workbook_schema contract=/dev/fd/12 - Rejected or weak authorization wording.
authorization_status: review
```

Passed:

```bash
python3 -m pytest -q tests/test_select_validation.py
```

```text
25 passed in 0.07s
```

Passed:

```bash
python3 -m pytest -q tests/test_select_validation.py tests/test_check_protected_surfaces.py
```

```text
79 passed in 0.08s
```

Passed:

```bash
printf 'docs/contracts/repo_wide_protected_surface_authorization_checker.md\n' | python3 tools/check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs/contracts/repo_wide_protected_surface_authorization_checker.md
```

```text
authorization_status: ok
```

Passed:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
```

```text
changed_paths: 0
result: passed
```

Passed:

```bash
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
```

```text
changed_paths: 0
selection_status: ok
```

Passed selector stdin integration smoke:

```bash
printf 'src/mythic_edge_parser/app/state.py\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
RECOMMENDED protected_surface_authorization
WARNING parser_state_final_reconciliation src/mythic_edge_parser/app/state.py
selection_status: warning
```

Passed:

```bash
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
```

```text
scanned_paths: 0
result: passed
```

Passed package protected-surface scan for the #90 files:

```bash
printf 'docs/contracts/repo_wide_protected_surface_authorization_checker.md\ndocs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md\ntests/test_check_surface_authorization.py\ntools/check_surface_authorization.py\n' | python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
changed_paths: 4
forbidden: 0
warnings: 0
result: passed
```

Passed package secret scan for the #90 files with warning-only documentation
matches:

```bash
printf 'docs/contracts/repo_wide_protected_surface_authorization_checker.md\ndocs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md\ntests/test_check_surface_authorization.py\ntools/check_surface_authorization.py\n' | python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
forbidden: 0
warnings: 2
result: warning
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
python3 tools/check_agent_docs.py
```

```text
errors: 0
warnings: 0
result: passed
```

Passed:

```bash
python3 -m pyright
```

```text
0 errors, 0 warnings, 0 informations
```

Passed:

```bash
python3 -m pytest -q tests
```

```text
758 passed in 1.33s
```

Passed:

```bash
git diff --check
```

```text
<no output>
```

Important validation nuance:

- Changed-file validation commands use committed diff semantics from
  `git diff <base>...HEAD`, so they currently report zero changed paths while
  this implementation is still unstaged/uncommitted in the working tree.
  Focused tests and stdin smoke checks validate the changed behavior directly.

## Still Unverified

- No live GitHub issue or PR text was fetched by design.
- CI integration is deferred; this pass did not edit workflows.
- The checker verifies deterministic authorization text, not semantic
  correctness of protected-surface changes.
- A source file can be incomplete or stale; human review still owns that
  interpretation.
- Submitter validation should rerun changed-file mode after the branch has a
  committed diff.

## CI Decision

Deferred.

The contract explicitly forbids CI edits in #90 implementation. This pass did
not edit `.github/workflows/repo-checks.yml`.

## Reviewer Focus

Codex E should verify:

- the checker imports/reuses `tools/check_protected_surfaces.py` and does not
  maintain a competing protected path table
- forbidden classifications are never authorizable
- missing authorization and weak authorization remain advisory exit `0`
- config/source errors exit `2`
- source-kind citation rules match the contract
- rejected wording does not accidentally authorize protected categories
- selector integration is limited to recommending the checker
- no protected parser/runtime/workbook/App Script behavior changed

## Next Workflow Action

Next role: Codex E: Module Reviewer / Contract Tester.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer in contract-test mode for repo-wide hardening issue #90: Protected-surface authorization checker.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/90
- Branch: codex/repo-wide-hardening-run
- Contract: docs/contracts/repo_wide_protected_surface_authorization_checker.md
- Implementation handoff: docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/review.md
- docs/contracts/repo_wide_protected_surface_authorization_checker.md
- docs/contracts/code_hardening_protected_surface_gate.md
- tools/check_surface_authorization.py
- tests/test_check_surface_authorization.py
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- tools/select_validation.py
- tests/test_select_validation.py
- tools/check_secret_patterns.py
- tools/check_agent_docs.py
- .github/pull_request_template.md

Goal:
Verify the Codex C implementation and Codex D negated-evidence fixer pass
against the protected-surface authorization checker contract.

Confirm:
- tools/check_surface_authorization.py exists and implements the contracted CLI.
- The checker requires --base and supports --repo-root, --paths-from-stdin, repeated --authorization-file kind=path, and --format text|json.
- Changed-file mode uses git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD through the protected-surface gate behavior.
- Stdin mode does not run git diff.
- The checker imports/reuses tools/check_protected_surfaces.py classification helpers rather than maintaining a competing path table.
- SEVERITY_WARNING classifications require authorization evidence.
- SEVERITY_FORBIDDEN classifications are reported as FORBIDDEN_PATH and are never AUTHORIZED.
- SEVERITY_ALLOWED classifications are reported as NOT_PROTECTED.
- Accepted category aliases and authorization markers match the contract.
- issue, contract, handoff, and report sources can authorize without extra citation.
- pr and generic sources require a citation.
- Broad/boilerplate wording such as "all protected surfaces authorized" and "unchanged or authorized" reports SCOPE_WARNING plus MISSING_AUTHORIZATION.
- Negated wording such as "workbook_schema not in scope" reports SCOPE_WARNING plus MISSING_AUTHORIZATION and is not AUTHORIZED.
- Unrelated-category evidence reports SCOPE_WARNING plus MISSING_AUTHORIZATION.
- Missing sources for protected warnings report UNVERIFIABLE_SOURCE plus MISSING_AUTHORIZATION.
- Unreadable sources and invalid authorization-file syntax exit 2 with authorization_status: error.
- Missing authorization and forbidden paths remain advisory exit 0.
- Output uses authorization_status: ok|review|error and does not claim protected behavior is safe, checks passed, or merge readiness.
- tools/select_validation.py only recommends the checker for protected/forbidden classifications and does not run it.
- No CI edits were made.
- No parser behavior, parser state, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or protected path rules changed.

Validation:
Run:
python3 -m pytest -q tests/test_check_surface_authorization.py
python3 -m pytest -q tests/test_select_validation.py
printf 'src/mythic_edge_parser/app/sheet_schema.py\n' | python3 tools/check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=<(printf 'workbook_schema not in scope\n')
printf 'src/mythic_edge_parser/app/state.py\n' | python3 tools/check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs/contracts/repo_wide_protected_surface_authorization_checker.md
printf 'src/mythic_edge_parser/app/state.py\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
python3 -m ruff check src tests tools
git diff --check

If feasible, also run:
python3 -m pytest -q tests
python3 -m pyright

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change files in review-only mode.
Do not fetch live GitHub issue or PR data.
Do not edit CI, stage, commit, push, merge, close tracker #82, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/90"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "Codex E contract-test review for protected-surface authorization checker"
  target_artifact: "tools/check_surface_authorization.py, tests/test_check_surface_authorization.py, docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  verdict: "Fixer pass complete: negated protected-surface evidence is rejected as weak evidence and no longer reports AUTHORIZED."
  validation:
    - "python3 -m pytest -q tests/test_check_surface_authorization.py -> 23 passed in 0.03s"
    - "printf 'src/mythic_edge_parser/app/sheet_schema.py\\n' | python3 tools/check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=<(printf 'workbook_schema not in scope\\n') -> authorization_status: review; authorized: 0; missing_authorization: 1; scope_warnings: 1"
    - "python3 -m pytest -q tests/test_select_validation.py"
    - "python3 -m pytest -q tests/test_select_validation.py tests/test_check_protected_surfaces.py -> 79 passed in 0.08s"
    - "printf 'docs/contracts/repo_wide_protected_surface_authorization_checker.md\\n' | python3 tools/check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs/contracts/repo_wide_protected_surface_authorization_checker.md"
    - "printf 'src/mythic_edge_parser/app/state.py\\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin with #90 file list -> changed_paths: 4; forbidden: 0; warnings: 0; result: passed"
    - "python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin with #90 file list -> forbidden: 0; warnings: 2; result: warning"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py -> result: passed"
    - "python3 -m pyright -> 0 errors, 0 warnings, 0 informations"
    - "python3 -m pytest -q tests -> 758 passed in 1.33s"
    - "git diff --check"
  stop_conditions:
    - "Do not edit CI in #90 implementation or review unless a future contract authorizes it."
    - "Do not fetch live GitHub issue or PR data."
    - "Do not make the checker strict/failing for missing authorization."
    - "Do not treat forbidden paths as authorizable."
    - "Do not change parser/runtime/workbook/App Script behavior or protected surfaces."
    - "Do not target main directly."
    - "Do not close tracker #82."
    - "Do not mark tracker #82 complete."
```
