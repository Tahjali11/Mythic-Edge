# Repo-Wide Validation Selector Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/87

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Related hardening artifacts:

- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/repo_wide_agent_docs_consistency_checker.md`
- `docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tools/check_agent_docs.py`
- `tests/test_check_agent_docs.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `.github/workflows/repo-checks.yml`
- `.github/pull_request_template.md`
- `pyproject.toml`

Branch target: `codex/repo-wide-hardening-run`

This contract defines a deterministic validation selector for repo-wide
hardening handoffs and pull requests. It is a contract artifact only. It does
not implement the selector, edit CI, change parser/runtime behavior, change
workbook or webhook shape, change Apps Script behavior, add fixtures, commit
secrets, or mark tracker #82 complete.

## Module

Repo-wide validation selector.

Likely implementation artifact:

- `tools/select_validation.py`

Likely tests:

- `tests/test_select_validation.py`

Expected later handoff/report artifacts:

- `docs/implementation_handoffs/repo_wide_validation_selector_comparison.md`
- `docs/contract_test_reports/repo_wide_validation_selector.md`

Plain English: given an explicit base ref and a changed path set, the selector
answers "what are the smallest meaningful validation commands this thread
should run and report?" It must not run those commands or claim they passed.

## Owning Layer

Repository coordination and code-hardening workflow tooling.

Truth boundary:

- The selector owns deterministic mapping from changed repo paths to validation
  recommendations and explanations.
- The selector does not own parser truth, parser behavior, parser state final
  reconciliation, workbook schema, webhook payload shape, Apps Script behavior,
  parser event classes, match identity, game identity, deduplication, secrets
  policy, fixture provenance truth, runtime status truth, or PR merge
  readiness.
- `tools/check_protected_surfaces.py` owns path-based forbidden/protected
  classification. The selector may reuse its merged helper functions for path
  warnings, but it must still recommend the gate instead of replacing it.
- `tools/check_secret_patterns.py` owns content scanning for secrets and
  private markers. The selector must recommend it; it must not duplicate
  scanner regexes or content findings.
- Module contracts, issue scope, PR drift budgets, reviews, and Codex G merge
  gates own whether selected validation is sufficient for integration.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_validation_selector.md`

Expected future implementation files owned by this contract:

- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `docs/implementation_handoffs/repo_wide_validation_selector_comparison.md`
- `docs/contract_test_reports/repo_wide_validation_selector.md`

Related files referenced but not owned by this contract:

- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `.github/workflows/repo-checks.yml`
- `.github/pull_request_template.md`
- `pyproject.toml`
- parser, runtime, workbook, webhook, Apps Script, fixture, and governance
  files whose paths are classified for validation recommendations

## Observed Current Behavior

Observed on `codex/repo-wide-hardening-run` during this contract pass:

- `tools/select_validation.py` does not exist as a tracked file.
- `tests/test_select_validation.py` does not exist as a tracked file.
- Any untracked local copies of #87 implementation artifacts are not contract
  sources for this Codex B pass.
- `tools/check_protected_surfaces.py` exists as a path-based gate with:
  - CLI: `python3 tools/check_protected_surfaces.py --base <git-ref>`
  - optional `--repo-root`
  - optional `--paths-from-stdin`
  - changed-path collection from `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`
  - exit `0` for no forbidden paths, exit `1` for forbidden paths, and exit
    `2` for configuration errors
- `tools/check_secret_patterns.py` exists as a content scanner with:
  - CLI: `python3 tools/check_secret_patterns.py --base <git-ref>`
  - optional `--repo-root`
  - optional `--paths-from-stdin`
  - optional `--all` advisory mode
  - changed-file mode that may fail on forbidden content
  - warning-only findings that still exit `0`
- `tools/check_agent_docs.py` exists as a tracked governance-doc consistency
  checker after merge commit `33570de258afd3e402243cd66175b9ca958fd871`.
  Its baseline CLI is `python3 tools/check_agent_docs.py`, with optional
  `--repo-root` and `--format text|json`.
- Issue #86, the agent docs consistency checker, is closed.
- `.github/workflows/repo-checks.yml` currently runs tests, the protected
  surface gate on pull requests, and Ruff. It does not run the validation
  selector.
- `.github/workflows/repo-checks.yml` does not currently run
  `tools/check_agent_docs.py`.

Current gap:

- Codex handoffs and PRs do not have one deterministic repo-local place that
  maps changed paths to focused validation commands.

## Required Guarantee

The selector must produce stable, explainable validation recommendations from
the changed path set.

Required properties:

- It must require an explicit base ref.
- It must not silently assume `main`.
- It must compute changed paths from `<base>...HEAD` unless
  `--paths-from-stdin` is supplied.
- It must not run selected validation commands.
- It must not claim selected commands passed.
- It must distinguish `required`, `recommended`, and `advisory` commands.
- It must deduplicate commands and list them in stable order.
- It must explain which path categories triggered each command.
- It must recommend the protected-surface gate and secret/private-marker scan
  for non-empty changed path sets.
- It must keep docs-only changes narrow and must not select the full parser
  suite for docs-only changes without a specific path category reason.
- It must recommend the tracked agent-docs checker for governance authority
  docs.
- It must keep optional checker integration based on tracked files, not
  untracked workspace artifacts.

## Public Interface

### Primary CLI

Required invocation:

```bash
python3 tools/select_validation.py --base <git-ref>
```

Windows-compatible invocation:

```powershell
py tools\select_validation.py --base <git-ref>
```

Required arguments:

- `--base <git-ref>`: explicit base branch or ref for `<base>...HEAD`.

Required optional arguments:

- `--repo-root <path>`: repository root to inspect. Default: `"."`.
- `--paths-from-stdin`: read newline-delimited paths from stdin instead of
  running `git diff`. This is required for deterministic tests and handoff
  drafting.

Allowed optional argument:

- `--format text|json`: if implemented, default must be `text`. JSON output is
  authorized but not required for the first implementation.

Not allowed in the first implementation:

- `--run`
- automatic test execution
- automatic CI edits
- automatic PR readiness or merge-readiness verdicts

### Test-Facing Python Helpers

The stable public interface is the CLI. The implementation may expose
standard-library-only helper functions or dataclasses for tests, such as:

- path normalization
- changed-path collection
- tracked-file detection
- path category classification
- recommendation selection
- report rendering

No parser/runtime code may depend on these helpers.

## Inputs

### Base Ref

Type: `str`

Source:

- Codex handoff
- local user command
- GitHub Actions or PR base context if a later issue authorizes CI use

Examples:

- `origin/main`
- `origin/codex/repo-wide-hardening-run`

Contract:

- The base ref is required.
- The selector must pass the base ref through in recommended commands that
  need a base ref.
- Missing or invalid base refs are configuration errors.

### Changed Paths

Primary source:

```bash
git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD
```

Required behavior:

- Normalize paths to repo-relative forward-slash form.
- Strip leading `./`.
- Ignore blank path lines.
- Deduplicate normalized paths.
- Sort paths lexicographically before categorizing for stable reports.
- Preserve paths exactly enough for humans to identify the changed file.
- Do not read file contents.
- Do not print private absolute path segments. If an absolute path is supplied
  through stdin and cannot be normalized under `--repo-root`, report it as an
  ignored outside-repo path without echoing private user directories.

### Explicit Paths From Stdin

When `--paths-from-stdin` is present:

- Read newline-delimited paths from stdin.
- Still require `--base` so selected commands can be rendered consistently.
- Do not run `git diff`.
- Use the same normalization, deduplication, sorting, categorization, and
  rendering behavior as changed-file mode.

### Tracked Tool Availability

For checker integrations, tracked availability must be based on Git, not mere
filesystem presence.

Required rule:

- Recommend `tools/check_agent_docs.py` for governance authority docs because
  that path is tracked on `codex/repo-wide-hardening-run` after merge commit
  `33570de258afd3e402243cd66175b9ca958fd871`.
- Still verify tracked availability by Git, such as by
  `git ls-files --error-unmatch tools/check_agent_docs.py` succeeding, so
  untracked local files cannot change selector output on other branches.

Rationale:

- The selector should be stable across local worktrees. Tracked checker files
  may influence recommendations; untracked implementation drafts must not.

## Outputs

The selector prints a deterministic recommendation report. It recommends what
to run; it does not report validation results from commands it did not run.

Required text report shape:

```text
Validation Selector
mode: changed-files
base: origin/codex/repo-wide-hardening-run
head: HEAD
changed_paths: 3
categories: 2
required: 4
recommended: 1
advisory: 0
warnings: 1

REQUIRED protected_surface_gate
command: python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
reason: Changed paths must be checked for forbidden and protected surfaces.
categories: always_changed_paths, parser_surface
paths: src/mythic_edge_parser/parsers/match_state.py

RECOMMENDED pyright_advisory
command: python3 -m pyright
reason: Parser source changed; type checking is useful before review.
categories: parser_surface
paths: src/mythic_edge_parser/parsers/match_state.py

WARNING match_game_identity src/mythic_edge_parser/parsers/match_state.py - Protected match/game identity surface; issue/contract must authorize this change.

selection_status: ok
```

Required vocabulary:

- `required`: minimum command for the touched surface.
- `recommended`: broader validation that is useful because risk is higher,
  multiple surfaces changed, or the touched files affect shared behavior.
- `advisory`: context-aware command or manual check that may be useful but is
  not always required.
- `warning`: path classification note that must be considered in the PR drift
  budget or handoff.
- `selection_status`: selector completion status. Allowed values are `ok`,
  `warning`, and `error`.

Forbidden wording:

- Do not say `validation passed`, `checks passed`, `ready to merge`, or
  equivalent language unless the selector actually ran those checks, which it
  must not do in the first implementation.
- Do not use `selection_status: passed`. Use `ok` for successful selection.

If `--format json` is implemented, the JSON object must include:

- `mode`
- `base`
- `head`
- `changed_paths`
- `categories`
- `recommendations`
- `warnings`
- `notes`
- `selection_status`

JSON support is optional in the first implementation. Text support is required.

## Recommendation Model

### Global Rules

For any non-empty changed path set, select these required commands:

| Command ID | Priority | Command |
| --- | --- | --- |
| `protected_surface_gate` | `required` | `python3 tools/check_protected_surfaces.py --base <base>` |
| `secret_private_marker_scan` | `required` | `python3 tools/check_secret_patterns.py --base <base>` |
| `diff_check` | `required` | `git diff --check` |

For a zero-path changed set:

- Do not select required commands.
- Emit `selection_status: ok`.
- Emit an advisory note that baseline reporters may still run the protected
  surface gate, secret/private-marker scanner, and `git diff --check` when they
  need explicit zero-diff evidence.

### Path Categories

The selector must classify changed paths into one or more categories.

Required categories:

| Category | Example paths | Required or recommended selection |
| --- | --- | --- |
| `parser_surface` | `src/mythic_edge_parser/parsers/**`, `src/mythic_edge_parser/events.py` | focused parser tests, Ruff; Pyright recommended |
| `parser_state_or_model_surface` | `src/mythic_edge_parser/app/state.py`, `src/mythic_edge_parser/app/models.py` | focused state/model tests, parser regression tests recommended, Ruff, Pyright recommended |
| `extractor_surface` | `src/mythic_edge_parser/app/extractors.py` | extractor tests, Ruff, Pyright recommended |
| `runtime_app_surface` | `src/mythic_edge_parser/app/runner.py`, `src/mythic_edge_parser/app/config.py`, `src/mythic_edge_parser/stream.py` | focused runtime tests, Ruff, Pyright recommended |
| `workbook_schema_or_export_surface` | `src/mythic_edge_parser/app/sheet_schema.py`, `src/mythic_edge_parser/app/sheet_exports.py`, schema snapshot fixtures | sheet/schema/snapshot tests, Ruff, Pyright recommended |
| `webhook_or_output_surface` | `src/mythic_edge_parser/app/outputs.py`, `src/mythic_edge_parser/app/transforms.py` | output/transform/runner tests, Ruff, Pyright recommended |
| `apps_script_surface` | `tools/google_apps_script/**` | schema snapshot parity tests, protected-surface gate, secret scan |
| `hardening_tool_surface` | `tools/check_*.py`, `tools/select_validation.py`, `tests/test_check_*.py`, `tests/test_select_validation.py` | matching focused tool tests, Ruff |
| `governance_docs_surface` | `AGENTS.md`, `docs/agent_constitution.md`, `docs/agent_rules.yml`, `docs/codex_module_workflow.md`, `docs/agent_threads/**`, `docs/templates/**`, `.github/ISSUE_TEMPLATE/**`, `.github/pull_request_template.md` | docs checks, protected-surface gate, secret scan, tracked agent-docs checker |
| `contract_or_report_docs_surface` | `docs/contracts/**`, `docs/implementation_handoffs/**`, `docs/contract_test_reports/**`, `docs/problem_representations/**` | docs checks, secret scan, protected-surface gate |
| `ci_or_dependency_surface` | `.github/workflows/**`, `pyproject.toml` | Ruff, focused tests where possible, full tests recommended, Pyright recommended |
| `fixture_surface` | `tests/fixtures/**` | relevant replay/snapshot/fixture tests, secret scan |
| `test_surface` | `tests/test_*.py` | changed test file itself, Ruff for Python tests |
| `docs_only_surface` | `README.md`, ordinary Markdown outside authority/contract/report docs | docs checks, secret scan, protected-surface gate |

Categories may overlap. For example, `src/mythic_edge_parser/app/transforms.py`
is both a workbook and webhook/output surface.

### Focused Test Mapping

The selector must prefer specific focused tests where a known mapping exists.

Required mappings:

| Changed path | Required focused tests |
| --- | --- |
| `tools/select_validation.py`, `tests/test_select_validation.py` | `python3 -m pytest -q tests/test_select_validation.py` |
| `tools/check_secret_patterns.py`, `tests/test_check_secret_patterns.py` | `python3 -m pytest -q tests/test_check_secret_patterns.py` |
| `tools/check_protected_surfaces.py`, `tests/test_check_protected_surfaces.py` | `python3 -m pytest -q tests/test_check_protected_surfaces.py` |
| `src/mythic_edge_parser/parsers/gre/connect_resp.py` | `python3 -m pytest -q tests/test_gre_connect_resp_parser.py` |
| `src/mythic_edge_parser/parsers/gre/game_result.py` | `python3 -m pytest -q tests/test_gre_game_result_parser.py` |
| `src/mythic_edge_parser/parsers/gre/game_state.py` | `python3 -m pytest -q tests/test_gre_game_state_parser.py` |
| `src/mythic_edge_parser/parsers/gre/turn_info.py` | `python3 -m pytest -q tests/test_gre_turn_info_parser.py` |
| `src/mythic_edge_parser/parsers/match_state.py` | `python3 -m pytest -q tests/test_match_state_parser.py tests/test_match_summary_from_match_state.py` |
| `src/mythic_edge_parser/parsers/api_common.py` | `python3 -m pytest -q tests/test_api_common.py` |
| `src/mythic_edge_parser/parsers/client_actions.py` | `python3 -m pytest -q tests/test_client_actions_parser.py` |
| `src/mythic_edge_parser/app/event_identity.py` | `python3 -m pytest -q tests/test_event_identity.py` |
| `src/mythic_edge_parser/app/state.py` | `python3 -m pytest -q tests/test_state.py` |
| `src/mythic_edge_parser/app/models.py` | `python3 -m pytest -q tests/test_app_models.py tests/test_events.py` |
| `src/mythic_edge_parser/app/extractors.py` | `python3 -m pytest -q tests/test_app_extractors.py` |
| `src/mythic_edge_parser/app/runner.py` | `python3 -m pytest -q tests/test_runner.py` |
| `src/mythic_edge_parser/app/outputs.py` | `python3 -m pytest -q tests/test_app_outputs.py` |
| `src/mythic_edge_parser/app/sheet_schema.py` | `python3 -m pytest -q tests/test_sheet_schema.py tests/test_event_schema_snapshots.py` |
| `src/mythic_edge_parser/app/sheet_exports.py` | `python3 -m pytest -q tests/test_sheet_exports.py tests/test_event_schema_snapshots.py` |
| `src/mythic_edge_parser/app/transforms.py` | `python3 -m pytest -q tests/test_transforms.py tests/test_event_schema_snapshots.py` |
| `src/mythic_edge_parser/app/runtime_surfaces.py` | `python3 -m pytest -q tests/test_runtime_surfaces.py` |
| `src/mythic_edge_parser/app/diagnostics.py` | `python3 -m pytest -q tests/test_diagnostics.py` |
| `src/mythic_edge_parser/app/log_drift_sensor.py` | `python3 -m pytest -q tests/test_log_drift_sensor.py` |
| `src/mythic_edge_parser/app/status_api.py` | `python3 -m pytest -q tests/test_status_api.py` |
| `src/mythic_edge_parser/stream.py` | `python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py` |
| `tests/fixtures/parser_regression_*` | `python3 -m pytest -q tests/test_parser_regressions.py` |
| `tests/fixtures/schema_snapshots/**` | `python3 -m pytest -q tests/test_event_schema_snapshots.py` |

Fallback behavior:

- If a Python source path has no known mapping, select `python3 -m ruff check
  src tests tools` as required and select `python3 -m pytest -q tests` as
  recommended.
- If a changed test file has no known source mapping, select that test file as
  required.
- If multiple changed paths select the same command, emit the command once and
  aggregate all triggering categories and paths.

### Broad Checks

Required broad check:

- `python3 -m ruff check src tests tools` is required when any Python file
  under `src/`, `tests/`, or `tools/` changes, or when `pyproject.toml`
  changes.

Recommended broad checks:

- `python3 -m pyright` is recommended when source files under `src/`, Python
  hardening tools under `tools/`, or `pyproject.toml` change.
- `python3 -m pytest -q tests` is recommended when:
  - `pyproject.toml` changes
  - `.github/workflows/**` changes
  - more than one protected parser/runtime/workbook/output category changes
  - a source path has no focused test mapping
  - the implementation handoff needs broader confidence before Codex E review

The selector must explain why a broad check was selected.

### Agent Docs Checker

For governance docs changes:

- Always select the global required commands for non-empty path sets.
- Do not select a full parser suite solely because governance docs changed.
- Because `tools/check_agent_docs.py` is tracked on
  `codex/repo-wide-hardening-run`, select:

```bash
python3 tools/check_agent_docs.py
```

Priority:

- `required` for governance authority files:
  - `AGENTS.md`
  - `docs/agent_constitution.md`
  - `docs/agent_rules.yml`
  - `docs/codex_module_workflow.md`
  - `docs/agent_threads/**`
  - `docs/templates/**`
  - `.github/ISSUE_TEMPLATE/**`
  - `.github/pull_request_template.md`
- `recommended` for contract/report docs that mention role or workflow rules.

If this contract is reused on a branch where the checker is not tracked, emit
an advisory note instead of a command:

```text
ADVISORY agent_docs_checker_unavailable - Governance docs changed, but tools/check_agent_docs.py is not tracked on this branch.
```

## Protected-Surface Warnings

The selector may import `classify_paths` or equivalent stable helper behavior
from `tools/check_protected_surfaces.py`.

Required behavior if path classification is used:

- Include protected and forbidden path classifications as `WARNING` lines in
  selector output.
- Keep the protected-surface gate selected as a required command.
- Do not downgrade forbidden path classifications.
- Do not claim protected-surface warnings are authorized.
- Do not decide whether a PR may merge.

If the selector does not import the helper in the first implementation, it must
still select the protected-surface gate for non-empty path sets and tests must
cover that recommendation.

## Error Behavior

Configuration errors:

- Missing `--base`: argparse usage error, exit `2`.
- Invalid `--format`: argparse usage error, exit `2`.
- Git diff failure: print a deterministic error report to stderr, set
  `selection_status: error`, exit `2`.
- Repository root cannot be inspected: print a deterministic error report to
  stderr, set `selection_status: error`, exit `2`.

Input path issues:

- Blank lines are ignored.
- Duplicate paths are deduplicated.
- Outside-repo absolute paths from stdin are ignored or redacted in a warning.
- Missing files may still be categorized by path because changed paths can
  include deleted or renamed paths. The selector must not require files to
  exist unless checking tracked availability for optional future tools.

Recommendation issues:

- Unknown path categories must not crash selection.
- Unknown source paths should receive fallback Python or docs recommendations
  based on extension and top-level directory.
- The selector must not emit an empty report unless the path set is empty.

## Side Effects

Allowed side effects:

- Read Git metadata.
- Read newline-delimited stdin when requested.
- Read tracked-file metadata to determine checker availability.
- Print a report to stdout or stderr.

Forbidden side effects:

- Running selected validation commands.
- Editing files.
- Editing CI.
- Opening or updating issues.
- Opening, updating, staging, committing, pushing, or merging PRs.
- Reading raw MTGA logs, runtime status files, failed posts, workbook exports,
  generated card data, or private local artifacts.
- Posting webhooks or touching workbook/Apps Script state.

## Dependency Order

1. Keep this contract as the source of truth for #87 implementation.
2. Implement `tools/select_validation.py` with no parser/runtime dependencies.
3. Add `tests/test_select_validation.py` with representative path-set tests.
4. Write `docs/implementation_handoffs/repo_wide_validation_selector_comparison.md`.
5. Run focused selector validation.
6. Route to Codex E for contract testing.
7. Leave CI integration, if any, to a later explicit issue and contract.

## Compatibility

- The first implementation must use only the Python standard library and repo
  files already tracked on `codex/repo-wide-hardening-run`.
- Existing commands in `AGENTS.md`, workflow docs, the PR template, and GitHub
  Actions remain valid.
- The selector is advisory/local in #87. It must not become a required CI gate
  without a later issue and contract.
- The selector must remain useful if local untracked checker drafts exist.
- Text output must remain stable enough to paste into Codex handoffs and PR
  descriptions.
- JSON output, if implemented, must be additive and must not replace the text
  report.

## Tests Required

Focused selector tests:

```bash
python3 -m pytest -q tests/test_select_validation.py
```

Required test coverage:

- missing `--base` exits `2`
- invalid base diff reports `selection_status: error`
- changed-path mode uses `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`
- stdin mode does not run `git diff`
- path normalization deduplicates and sorts paths
- zero changed paths emits no required commands and includes a baseline
  advisory note
- docs-only changes select global docs-safe checks and do not select the full
  parser suite
- governance docs changes select `check_agent_docs.py` when the tool is tracked
- governance docs changes do not select `check_agent_docs.py` when tests mock
  the tool as untracked
- hardening tool changes select the matching tool test
- selector changes select `tests/test_select_validation.py`
- parser module changes select focused parser tests, Ruff, and recommended
  Pyright
- workbook schema/export changes select sheet/schema/snapshot tests
- webhook/output changes select output/transform/runner tests as applicable
- fixture changes select regression or snapshot tests as applicable
- CI/dependency changes recommend broader tests and Pyright
- protected and forbidden path classifications are surfaced as warnings when
  classification helpers are used
- duplicate commands are emitted once with aggregated triggers
- output says selected/recommended, not passed
- optional JSON output, if implemented, contains the contracted field names

Implementation validation should include:

```bash
python3 -m pytest -q tests/test_select_validation.py
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
printf 'src/mythic_edge_parser/parsers/match_state.py\n' | python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
python3 -m ruff check src tests tools
```

Broader checks to consider before submitter or review completion:

```bash
python3 -m pyright
python3 -m pytest -q tests
git diff --check
```

## Acceptance Criteria

- `docs/contracts/repo_wide_validation_selector.md` exists and is cited by the
  implementation handoff.
- `tools/select_validation.py` exists and implements the contracted CLI.
- `tests/test_select_validation.py` exists and covers the required scenarios.
- Selector output is deterministic for the same path set.
- Selector output includes reasons, categories, and triggering paths for each
  selected command.
- Selector output uses `required`, `recommended`, and `advisory` consistently.
- Selector output never claims unrun checks passed.
- Selector recommends `check_secret_patterns.py` and
  `check_protected_surfaces.py` for non-empty changed path sets.
- Selector recommends `check_agent_docs.py` for governance docs while keeping
  checker integration conditional on tracked file availability.
- No parser behavior, parser state final reconciliation, workbook schema,
  webhook payload shape, Apps Script behavior, parser event classes,
  match/game identity, deduplication, secrets, environment variables, raw logs,
  generated data, runtime status files, failed posts, workbook exports, or CI
  required/failing behavior changes are made by #87 implementation unless a
  later explicit issue and contract authorize them.

## Open Questions And Contract Risks

- The focused path-to-test table is intentionally useful but not exhaustive.
  Unknown Python paths must fall back to Ruff plus recommended full tests.
- CI integration is intentionally deferred. A later issue must decide whether
  the selector should run in GitHub Actions or remain a handoff helper.
- Agent-docs checker integration is intentionally based on tracked-file
  availability so local untracked drafts cannot change selector behavior.
- If the selector imports helpers from `tools/check_protected_surfaces.py`,
  Codex E should verify that the dependency stays acyclic and does not weaken
  the protected-surface gate.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for repo-wide hardening issue #87: Validation selector.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/87
- Branch: codex/repo-wide-hardening-run
- Contract: docs/contracts/repo_wide_validation_selector.md
- Previous completed child: #84 Secret and private-marker scanner, PR #85 merged
- Previous completed child: #86 Agent docs consistency checker, merge commit 33570de258afd3e402243cd66175b9ca958fd871

Goal:
Implement the smallest coherent validation selector that satisfies the contract.

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/repo_wide_validation_selector.md
- tools/check_secret_patterns.py
- tools/check_protected_surfaces.py
- tools/check_agent_docs.py
- tests/test_check_secret_patterns.py
- tests/test_check_protected_surfaces.py
- tests/test_check_agent_docs.py
- .github/pull_request_template.md

Do:
- Create tools/select_validation.py.
- Create tests/test_select_validation.py.
- Keep the tool advisory: recommend commands, do not run them.
- Require an explicit --base.
- Support --repo-root and --paths-from-stdin.
- Recommend protected-surface and secret/private-marker checks for non-empty path sets.
- Recommend check_agent_docs.py for governance docs because it is now tracked.
- Keep checker integration conditional on tracked files, not untracked workspace drafts.
- Produce docs/implementation_handoffs/repo_wide_validation_selector_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Edit CI.
- Run selected checks automatically from the selector.
- Claim selected checks passed.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Target main directly.
- Mark tracker #82 complete.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/87"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/repo_wide_validation_selector.md"
  target_artifact: "tools/select_validation.py, tests/test_select_validation.py, docs/implementation_handoffs/repo_wide_validation_selector_comparison.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "python3 -m pytest -q tests/test_select_validation.py"
    - "python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/check_agent_docs.py"
    - "python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "python3 -m ruff check src tests tools"
  stop_conditions:
    - "Do not edit CI in #87 implementation."
    - "Do not depend on untracked implementation drafts."
    - "Do not run selected validation commands from inside the selector."
    - "Do not claim selected checks passed."
    - "Do not change parser/runtime/workbook/App Script behavior or protected surfaces."
    - "Do not target main directly."
    - "Do not mark tracker #82 complete."
```
