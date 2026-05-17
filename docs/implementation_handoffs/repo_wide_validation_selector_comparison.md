# Repo-Wide Validation Selector Implementation Handoff

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/87

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Contract: `docs/contracts/repo_wide_validation_selector.md`

Role performed: Codex C: Module Implementer; Codex D: Module Fixer follow-up

Branch: `codex/repo-wide-hardening-run`

Risk tier: Medium

## Summary Of Implementation Comparison

Current repo state before this pass had the protected-surface gate and
secret/private-marker scanner, but no deterministic validation selector:

- `tools/check_protected_surfaces.py` exists and remains unchanged.
- `tools/check_secret_patterns.py` exists and remains unchanged.
- `tools/select_validation.py` did not exist.
- `tests/test_select_validation.py` did not exist.
- `docs/contracts/repo_wide_validation_selector.md` was already present as the
  untracked source contract artifact for this issue.

This pass implemented the smallest advisory selector required by the contract.
It recommends validation commands; it does not run them or claim they passed.

Codex D follow-up resolved the reviewer-blocking `agent_docs_checker`
metadata mismatch. The selector now reports only the categories and paths that
actually trigger the agent-docs checker recommendation, including mixed
governance plus contract/report path sets.

## Findings

No blocking contract ambiguity was found.

Contract mismatch fixed:

- Missing selector implementation: added `tools/select_validation.py`.
- Missing focused tests: added `tests/test_select_validation.py`.
- Missing implementation handoff: added this document.
- Reviewer-blocking `agent_docs_checker` metadata mismatch: fixed trigger
  category/path aggregation and added focused regression coverage.

Important validation nuance:

- `python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run`
  currently reports zero changed paths in this local worktree because the #87
  files are untracked. This matches the contract's use of
  `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`. Focused tests
  and `--paths-from-stdin` cover the selector behavior directly until submitter
  work creates a committed branch diff.

## Changes Made

Implemented `tools/select_validation.py`:

- CLI:
  - `python3 tools/select_validation.py --base <git-ref>`
  - `--repo-root <path>`
  - `--paths-from-stdin`
  - optional `--format text|json`
- changed-path collection:
  - uses `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`
  - requires explicit `--base`
  - normalizes, deduplicates, and sorts paths
  - redacts outside-repo absolute stdin paths in warnings
- advisory recommendation model:
  - `required`
  - `recommended`
  - `advisory`
  - `warning`
  - `selection_status: ok|warning|error`
- global non-empty path recommendations:
  - `python3 tools/check_protected_surfaces.py --base <base>`
  - `python3 tools/check_secret_patterns.py --base <base>`
  - `git diff --check`
- category mapping for:
  - parser surfaces
  - parser state/model surfaces
  - extractor surfaces
  - runtime app surfaces
  - workbook schema/export surfaces
  - webhook/output surfaces
  - Apps Script surfaces
  - hardening tool surfaces
  - governance docs
  - contract/report docs
  - CI/dependency files
  - fixtures
  - tests
  - ordinary docs-only files
- focused test mappings from the contract, including parser modules, app
  surfaces, hardening tools, schema snapshots, and parser regression fixtures
- broad check selection:
  - Ruff required for Python or dependency validation surfaces
  - Pyright recommended for source/tool/dependency changes
  - full pytest recommended for dependency/CI changes, unmapped source changes,
    or multiple protected categories
- protected-surface path classification:
  - reuses `tools/check_protected_surfaces.py` helper behavior
  - surfaces protected and forbidden classifications as selector `WARNING`
    lines
  - keeps the actual protected-surface gate selected as a required command
- future agent-docs checker integration:
  - selects `python3 tools/check_agent_docs.py` only when
    `git ls-files --error-unmatch tools/check_agent_docs.py` succeeds
  - otherwise emits an advisory note for governance doc changes
  - does not depend on unmerged #86 implementation files
  - reports governance-only, contract/report-only, and mixed path metadata from
    the actual triggering path sets

Added `tests/test_select_validation.py`:

- missing `--base` exit behavior
- invalid git base error report
- contract git diff command usage
- stdin mode without git diff
- path normalization, sorting, deduplication, and outside-root redaction
- zero-path advisory behavior
- docs-only narrow recommendations
- conditional `check_agent_docs.py` recommendation behavior
- trigger-accurate `agent_docs_checker` metadata for governance-only,
  contract/report-only, and mixed governance plus contract/report path sets
- hardening tool focused test mappings
- selector self-test mapping
- parser, workbook, webhook/output, fixture, CI/dependency recommendations
- protected and forbidden path classifications as warnings
- duplicate command aggregation
- report wording avoids validation-result claims
- JSON output field shape

## Confirmed Matches

- The selector requires `--base`.
- The selector supports `--repo-root` and `--paths-from-stdin`.
- The selector is advisory and does not run selected commands.
- The selector does not say `validation passed`, `checks passed`, or `ready to
  merge`.
- Non-empty path sets select protected-surface, secret/private-marker, and
  diff-check commands.
- Zero-path selection emits no required commands and includes a baseline
  advisory note.
- Docs-only changes do not select the full parser suite.
- `check_agent_docs.py` integration is tracked-file conditional.
- `agent_docs_checker` metadata is trigger-accurate and aggregates mixed
  governance plus contract/report paths.
- Duplicate commands are emitted once with aggregated categories and paths.
- Protected/forbidden path classifications are warnings, not merge decisions.
- CI was not edited.

## Missing Safeguards

No required safeguard remains knowingly missing in the implemented selector.

Future hardening may still add:

- CI integration through a separate issue and contract
- a runner/orchestrator that executes selected commands
- richer path-to-test mappings as modules evolve
- GitHub annotations
- stricter treatment of warnings after a baseline policy exists

Those are outside this #87 implementation contract.

## Open Risks

- The focused path-to-test table is useful but not exhaustive. Unknown source
  paths fall back to Ruff plus recommended full tests.
- The selector reuses `tools/check_protected_surfaces.py`; Codex E should
  confirm the dependency stays acyclic and does not weaken the gate.
- The selector cannot know whether selected validation is sufficient for
  integration; contracts, reviewers, submitters, and Codex G still own that
  judgment.
- The selector does not inspect file contents, so the secret/private-marker
  scanner remains required for content safety.
- Local untracked files are not part of `git diff <base>...HEAD`; focused tests
  and stdin mode cover behavior before submitter work creates a committed diff.

## CI Decision

Deferred.

The contract explicitly forbids CI edits in #87. This pass did not edit
`.github/workflows/repo-checks.yml`.

## Validation Evidence

Passed:

```bash
python3 -m pytest -q tests/test_select_validation.py
```

```text
22 passed in 0.04s
```

Passed:

```bash
printf 'AGENTS.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
agent_docs_checker categories: governance_docs_surface
agent_docs_checker paths: AGENTS.md
```

Passed:

```bash
printf 'docs/contracts/repo_wide_validation_selector.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
agent_docs_checker categories: contract_or_report_docs_surface
agent_docs_checker paths: docs/contracts/repo_wide_validation_selector.md
```

Passed:

```bash
printf 'AGENTS.md\ndocs/contracts/repo_wide_validation_selector.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
agent_docs_checker categories: contract_or_report_docs_surface, governance_docs_surface
agent_docs_checker paths: AGENTS.md, docs/contracts/repo_wide_validation_selector.md
```

Passed:

```bash
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
```

```text
Validation Selector
mode: changed-files
base: origin/codex/repo-wide-hardening-run
head: HEAD
changed_paths: 0
categories: 0
required: 0
recommended: 0
advisory: 1
warnings: 0

ADVISORY zero_changed_paths - No changed paths were selected. Baseline reporters may still run the protected-surface gate, secret/private-marker scan, and git diff --check for explicit zero-diff evidence.

selection_status: ok
```

Passed:

```bash
printf 'src/mythic_edge_parser/parsers/match_state.py\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
Validation Selector
mode: paths-from-stdin
base: origin/codex/repo-wide-hardening-run
head: HEAD
changed_paths: 1
categories: 1
required: 5
recommended: 1
advisory: 0
warnings: 1

selection_status: warning
```

The stdin report selected the focused match-state parser tests, Ruff, the
protected-surface gate, the secret/private-marker scan, `git diff --check`, and
recommended Pyright. It also surfaced the protected match/game identity
classification as a selector warning.

Passed:

```bash
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
```

```text
Secret / Private Marker Scan
mode: changed-files
base: origin/codex/repo-wide-hardening-run
head: HEAD
scanned_paths: 0
skipped_paths: 0
forbidden: 0
warnings: 0

result: passed
```

Passed:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
```

```text
Protected Surface Gate
base: origin/codex/repo-wide-hardening-run
head: HEAD
changed_paths: 0
forbidden: 0
warnings: 0

result: passed
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

Passed:

```bash
python3 tools/check_agent_docs.py
```

```text
errors: 0; warnings: 0; result: passed
```

Passed:

```bash
python3 -m pytest -q tests
```

```text
732 passed in 1.09s
```

Passed:

```bash
python3 -m pyright
```

```text
0 errors, 0 warnings, 0 informations
```

Passed with warnings only and exit code `0`:

```bash
printf 'docs/contracts/repo_wide_validation_selector.md\ndocs/implementation_handoffs/repo_wide_validation_selector_comparison.md\ndocs/contract_test_reports/repo_wide_validation_selector.md\ntests/test_select_validation.py\ntools/select_validation.py\n' | python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
scanned_paths: 5; forbidden: 0; warnings: 2; result: warning
```

Passed:

```bash
printf 'docs/contracts/repo_wide_validation_selector.md\ndocs/implementation_handoffs/repo_wide_validation_selector_comparison.md\ndocs/contract_test_reports/repo_wide_validation_selector.md\ntests/test_select_validation.py\ntools/select_validation.py\n' | python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

```text
changed_paths: 5; forbidden: 0; warnings: 0; result: passed
```

## Still-Unverified Layers

- No selected validation command is run by the selector itself.
- No live MTGA parser run was executed.
- No live workbook, webhook, or Apps Script integration was inspected.
- No CI run was triggered.
- No tracker #82 completion action was taken.

## Protected Surfaces

Not changed:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- match identity
- game identity
- deduplication
- secrets or environment variable semantics
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports
- CI required/failing behavior

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer in contract-test mode.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer in contract-test mode for repo-wide hardening issue #87:
https://github.com/Tahjali11/Mythic-Edge/issues/87

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch:
codex/repo-wide-hardening-run

Use:
- docs/contracts/repo_wide_validation_selector.md
- docs/contract_test_reports/repo_wide_validation_selector.md
- docs/implementation_handoffs/repo_wide_validation_selector_comparison.md
- tools/select_validation.py
- tests/test_select_validation.py
- tools/check_secret_patterns.py
- tools/check_protected_surfaces.py
- tests/test_check_secret_patterns.py
- tests/test_check_protected_surfaces.py
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- .github/pull_request_template.md

Goal:
Re-review the Module Implementer selector and Codex D recommendation-metadata
fix against the validation selector contract.

Confirm:
- The selector requires an explicit --base and does not silently assume main.
- Changed-path mode uses git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD.
- --paths-from-stdin does not run git diff.
- --repo-root is honored.
- The selector recommends commands but does not run them.
- The selector never claims selected checks passed or that a PR is ready to merge.
- Non-empty path sets select protected-surface gate, secret/private-marker scan, and git diff --check as required commands.
- Zero changed paths select no required commands and include the baseline advisory note.
- Path categories cover parser, parser state/model, extractor, runtime app, workbook schema/export, webhook/output, Apps Script, hardening tool, governance docs, contract/report docs, CI/dependency, fixtures, tests, and docs-only changes.
- Focused test mappings match the contract.
- Ruff is required for changed Python or dependency validation surfaces.
- Pyright is recommended for source/tool/dependency changes.
- Full pytest is recommended for CI/dependency changes, unmapped source changes, or multiple protected parser/runtime/workbook/output categories.
- Governance docs changes do not select check_agent_docs.py unless tools/check_agent_docs.py is tracked by git.
- agent_docs_checker recommendation metadata reports only the categories and paths that actually triggered it.
- governance-only path sets report only governance_docs_surface.
- contract/report-only path sets report only contract_or_report_docs_surface and keep the command recommended.
- mixed governance plus contract/report path sets aggregate both categories and both triggering paths.
- Protected and forbidden path classifications from check_protected_surfaces.py are surfaced as selector warnings without replacing the gate.
- Duplicate commands are emitted once with aggregated categories and paths.
- Text output includes reasons, categories, paths, warnings, and selection_status.
- JSON output, if kept, includes the contracted field names.
- CI was not edited.
- No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or protected surfaces outside this contract changed.

Validation:
Run:
python3 -m pytest -q tests/test_select_validation.py
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
printf 'AGENTS.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
printf 'docs/contracts/repo_wide_validation_selector.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
printf 'AGENTS.md\ndocs/contracts/repo_wide_validation_selector.md\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
printf 'src/mythic_edge_parser/parsers/match_state.py\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
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

Do not stage, commit, merge, target main, mark tracker #82 complete, edit CI, run selected checks from inside the selector, claim selected checks passed, depend on unmerged #86 implementation details, or change parser/runtime/workbook/App Script behavior during review.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/87"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/repo_wide_validation_selector.md"
  target_artifact: "Codex E contract-test re-review for repo-wide validation selector"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  verdict: "Fixer pass complete: agent_docs_checker recommendation metadata now reports the actual triggering categories and paths."
  validation:
    - "python3 -m pytest -q tests/test_select_validation.py -> 22 passed in 0.04s"
    - "governance-only selector repro -> agent_docs_checker categories governance_docs_surface, paths AGENTS.md"
    - "contract/report-only selector repro -> agent_docs_checker categories contract_or_report_docs_surface, paths docs/contracts/repo_wide_validation_selector.md"
    - "mixed selector repro -> agent_docs_checker categories contract_or_report_docs_surface and governance_docs_surface, paths AGENTS.md and docs/contracts/repo_wide_validation_selector.md"
    - "python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run -> zero changed paths, selection_status ok"
    - "parser stdin selector smoke check -> expected focused checks and selection_status warning"
    - "python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run -> passed, scanned_paths 0"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run -> passed, changed_paths 0"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed with no output"
    - "python3 tools/check_agent_docs.py -> passed"
    - "python3 -m pytest -q tests -> 732 passed in 1.09s"
    - "python3 -m pyright -> 0 errors, 0 warnings, 0 informations"
    - "new package secret scan -> warning-only exit 0, scanned_paths 5, forbidden 0, warnings 2"
    - "new package protected-surface scan -> passed, changed_paths 5, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not edit CI in #87 implementation."
    - "Do not depend on unmerged implementation details from #86."
    - "Do not run selected validation commands from inside the selector."
    - "Do not claim selected checks passed."
    - "Do not change parser/runtime/workbook/App Script behavior or protected surfaces."
    - "Do not target main directly."
    - "Do not mark tracker #82 complete."
```
