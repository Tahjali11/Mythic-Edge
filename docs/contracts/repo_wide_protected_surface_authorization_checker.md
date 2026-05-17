# Repo-Wide Protected-Surface Authorization Checker Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/90

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Source handoff:

- Previous completed child issue: #87 Validation selector
- Previous PR: #89
- Previous merge commit: `15bdf7c9661383fdcc6dfe456f8efa6c68662b72`

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`
- `docs/templates/workflow_handoff.md`

Related hardening artifacts:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `docs/contracts/repo_wide_validation_selector.md`
- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `tools/check_secret_patterns.py`
- `docs/contracts/repo_wide_agent_docs_consistency_checker.md`
- `tools/check_agent_docs.py`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`

Branch target: `codex/repo-wide-hardening-run`

This contract defines a deterministic checker for protected-surface
authorization evidence. It is a contract artifact only. It does not implement
the checker, edit CI, target `main`, close tracker #82, mark tracker #82
complete, or change parser/runtime/workbook/App Script behavior or protected
surfaces.

## Module

Repo-wide protected-surface authorization checker.

Likely implementation artifact:

- `tools/check_surface_authorization.py`

Likely tests:

- `tests/test_check_surface_authorization.py`

Expected later handoff/report artifacts:

- `docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md`
- `docs/contract_test_reports/repo_wide_protected_surface_authorization_checker.md`

Plain English: the existing protected-surface gate says "this changed path is
sensitive." This checker asks "did the supplied issue, contract, handoff,
report, or PR text explicitly authorize that exact protected category?"

## Owning Layer

Repository coordination and code-hardening workflow tooling.

Truth boundary:

- `tools/check_protected_surfaces.py` owns path classification and the
  protected/forbidden category vocabulary.
- This checker owns deterministic comparison between protected category IDs
  and supplied authorization evidence.
- This checker does not own parser truth, parser behavior, parser state final
  reconciliation, workbook schema truth, webhook payload truth, Apps Script
  behavior, parser event classes, match identity, game identity,
  deduplication, secret policy, runtime status truth, fixture provenance
  truth, PR readiness, or merge readiness.
- Human review, Codex E, Codex F, and Codex G still own interpretation,
  submission, and merge judgment.
- A clean authorization report is evidence. It is not proof that parser
  behavior, schema behavior, webhook payloads, Apps Script behavior, or
  deployed behavior are safe.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`

Expected future implementation files owned by this contract:

- `tools/check_surface_authorization.py`
- `tests/test_check_surface_authorization.py`
- `docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md`
- `docs/contract_test_reports/repo_wide_protected_surface_authorization_checker.md`

Related files referenced but not owned by this contract:

- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `tools/check_secret_patterns.py`
- `tools/check_agent_docs.py`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/templates/workflow_handoff.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`

## Observed Current Behavior

Observed on `codex/repo-wide-hardening-run` during this contract pass:

- `tools/check_surface_authorization.py` does not exist.
- `tests/test_check_surface_authorization.py` does not exist.
- `tools/check_protected_surfaces.py` classifies changed paths as:
  - `allowed`
  - `warning`
  - `forbidden`
- Protected warnings currently say an issue/contract must authorize the change,
  but the gate does not inspect issue, contract, handoff, report, or PR text.
- `tools/select_validation.py` imports protected-surface classification
  warnings and recommends validation commands. It does not verify
  authorization text.
- `.github/pull_request_template.md` contains a drift budget and protected
  surface checklist, including `Protected-surface authorization`.
- `docs/agent_rules.yml`, `docs/agent_constitution.md`, and `AGENTS.md`
  require explicit authorization for protected-surface changes.
- `tools/check_secret_patterns.py` scans content for secrets/private markers.
- `tools/check_agent_docs.py` checks governance-doc consistency.

Current gap:

- A Codex thread can see a protected-surface warning and still claim
  authorization vaguely. There is no deterministic checker that compares the
  warning category with explicit authorization evidence.

## Required Guarantee

The checker must produce a deterministic advisory report that answers, per
changed path classification:

- protected warning category is explicitly authorized
- protected warning category is missing explicit authorization
- changed path is forbidden and cannot be authorized by ordinary workflow text
- changed path is not protected
- authorization source is missing, unreadable, vague, stale, or mismatched

Required properties:

- It must require an explicit `--base`.
- It must use the current protected-surface gate for path classification rather
  than maintaining a competing path table.
- It must support `--paths-from-stdin` for deterministic tests.
- It must support local authorization source files and must not require live
  GitHub API access.
- It must not treat broad template language as authorization.
- It must not treat forbidden paths as authorizable.
- It must not run semantic parser, workbook, webhook, or Apps Script checks.
- It must not claim parser/runtime/workbook/App Script behavior is safe.
- It must start as advisory/reporting-focused, not a CI-failing gate.

## Public Interface

### Primary CLI

Primary invocation:

```bash
python3 tools/check_surface_authorization.py --base <git-ref> --authorization-file <kind=path>
```

Windows-compatible invocation:

```powershell
py tools\check_surface_authorization.py --base <git-ref> --authorization-file <kind=path>
```

Required argument:

- `--base <git-ref>`: explicit base branch or ref for `<base>...HEAD`.

Optional arguments required for first-version support:

- `--repo-root <path>`: repository root to inspect. Default: `"."`.
- `--paths-from-stdin`: read newline-delimited paths from stdin instead of
  running `git diff`.
- `--authorization-file <kind=path>`: repeatable local authorization source.
  The CLI must allow zero source files so missing-evidence behavior can be
  tested and reported deterministically.

Allowed optional argument:

- `--format text|json`: if implemented, default must be `text`. JSON output is
  authorized but not required for the first implementation.

Accepted authorization source kinds:

- `issue`
- `contract`
- `handoff`
- `report`
- `pr`
- `generic`

Example:

```bash
python3 tools/check_surface_authorization.py \
  --base origin/codex/repo-wide-hardening-run \
  --authorization-file issue=docs/problem_representations/example.md \
  --authorization-file contract=docs/contracts/example.md \
  --authorization-file pr=.tmp/pr-body.md
```

Test seam example:

```bash
printf 'src/mythic_edge_parser/app/sheet_schema.py\n' | \
  python3 tools/check_surface_authorization.py \
    --base origin/codex/repo-wide-hardening-run \
    --paths-from-stdin \
    --authorization-file contract=tests/fixtures/authorization_contract.md
```

Not allowed in the first implementation:

- live GitHub issue or PR fetching
- CI edits
- automatic PR readiness or merge-readiness verdicts
- automatic protected-surface authorization from broad phrases
- any `--strict` or warning-failing behavior

### Test-Facing Python Helpers

The stable public interface is the CLI. The implementation may expose
standard-library-only helper functions or dataclasses for tests, such as:

- changed-path collection
- authorization source parsing
- protected classification loading
- source text normalization
- evidence-block extraction
- category alias matching
- report rendering

No parser/runtime code may depend on these helpers.

## Inputs

### Base Ref

Type: `str`

Source:

- local user command
- Codex handoff
- future orchestrator command if separately authorized

Contract:

- The base ref is required.
- The checker must not silently assume `main`.
- The checker must pass the base ref to changed-path collection and report it.
- Missing or invalid base refs are configuration errors.

### Changed Paths

Primary source:

```bash
git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD
```

Required behavior:

- Use the protected-surface gate's path normalization and classification where
  practical.
- Sort and deduplicate paths for stable reports.
- Classify paths even if they no longer exist in the working tree.
- Do not scan changed-file content.
- Do not inspect untracked files.

### Explicit Paths From Stdin

When `--paths-from-stdin` is present:

- Read newline-delimited paths from stdin.
- Still require `--base` for report shape.
- Do not run `git diff`.
- Use the same classification and report behavior as changed-file mode.

### Protected-Surface Classifications

Source of truth:

- `tools/check_protected_surfaces.py`

Required behavior:

- Import or reuse `classify_paths`, `Classification`, and severity constants
  where practical.
- Do not duplicate the path rule tables unless the implementation handoff
  explicitly justifies a fallback and tests prove exact parity.
- Treat `SEVERITY_FORBIDDEN` as not authorizable.
- Treat `SEVERITY_WARNING` as requiring authorization evidence.
- Treat `SEVERITY_ALLOWED` as `not_protected`.

The checker must consume the category ID returned by the gate. If the gate
returns one category for a path that might conceptually touch multiple
surfaces, this checker must not infer extra categories.

### Authorization Sources

Authorization source files are local text or Markdown files supplied with
`--authorization-file <kind=path>`.

Required behavior:

- Read only supplied authorization source files.
- Do not fetch issue or PR bodies from GitHub in the first version.
- Do not require source files to be committed.
- Do not write source files.
- If a supplied source cannot be read, exit `2` with
  `authorization_status: error`.
- If no authorization source is supplied and protected warnings exist, emit
  `UNVERIFIABLE_SOURCE` and keep advisory exit `0`.

Source kind precedence for primary evidence display:

1. `issue`
2. `contract`
3. `handoff`
4. `report`
5. `pr`
6. `generic`

Precedence chooses the primary evidence line when multiple sources authorize
the same category. It does not let lower-priority text override higher-priority
safety rules.

## Authorization Vocabulary

### Protected Category Aliases

The checker must recognize the protected category IDs produced by
`tools/check_protected_surfaces.py` and the approved aliases below.

| Category ID | Accepted aliases |
| --- | --- |
| `parser_event_classes` | `parser_event_classes`, `parser event classes`, `event class shape`, `parser event surface` |
| `parser_state_final_reconciliation` | `parser_state_final_reconciliation`, `parser state final reconciliation`, `final reconciliation`, `parser state surface` |
| `extractor_behavior` | `extractor_behavior`, `extractor behavior`, `extractor surface` |
| `match_game_identity` | `match_game_identity`, `match/game identity`, `match identity`, `game identity`, `deduplication`, `match/game identity and deduplication` |
| `workbook_schema` | `workbook_schema`, `workbook schema`, `sheet schema`, `workbook-facing row shape`, `workbook exports` |
| `webhook_payload_shape` | `webhook_payload_shape`, `webhook payload shape`, `webhook shape`, `output payload shape` |
| `apps_script_behavior` | `apps_script_behavior`, `Apps Script behavior`, `deployed Apps Script`, `Apps Script receiver behavior` |
| `environment_runtime_paths` | `environment_runtime_paths`, `environment variables`, `runtime paths`, `environment/runtime path surface`, `CI behavior` |
| `workflow_authority_docs` | `workflow_authority_docs`, `workflow authority docs`, `agent docs`, `workflow docs`, `validation gates`, `branch policy`, `issue lifecycle`, `PR lifecycle` |

Normalization rules:

- Matching is case-insensitive.
- Underscores, slashes, hyphens, and repeated whitespace may normalize to
  single spaces for alias matching.
- The canonical category ID must always match exactly after normalization.

### Accepted Positive Evidence

An authorization source explicitly authorizes a protected category only when
the same evidence block contains:

- at least one accepted category alias, and
- at least one accepted authorization marker.

Accepted authorization markers:

- `authorized`
- `explicitly authorized`
- `authorized drift`
- `accepted drift`
- `contract authorizes`
- `issue authorizes`
- `scope includes`
- `in scope`
- `allowed change`
- `allowed protected surface`

Accepted evidence block shapes:

```text
authorized_protected_surfaces: workbook_schema, webhook_payload_shape
```

```text
Protected-surface authorization: Authorized drift - workbook_schema - issue #46 and docs/contracts/parser_sheet_schema.md.
```

```text
Scope includes workbook_schema changes to src/mythic_edge_parser/app/sheet_schema.py.
```

```text
This contract explicitly authorizes Apps Script behavior changes for tools/google_apps_script/Code.gs.
```

Evidence block:

- A single line, bullet item, table row, or paragraph separated by blank lines.
- For `pr` and `generic` source kinds, the block must also contain a citation:
  - GitHub issue reference such as `#90`
  - GitHub URL
  - repo contract path such as `docs/contracts/...`
  - workflow handoff/report path such as `docs/implementation_handoffs/...` or
    `docs/contract_test_reports/...`
- For `issue`, `contract`, `handoff`, and `report` source kinds, the source
  kind itself is sufficient citation.

### Rejected Or Weak Evidence

The checker must not treat these as authorization:

- `all protected surfaces authorized`
- `parser_downstream_surfaces`
- `protected surfaces unchanged or authorized`
- `workbook schema unchanged or authorized`
- `webhook payload shape unchanged or authorized`
- `do not change workbook schema`
- `do not change parser behavior`
- `no drift`
- `N/A`
- a PR checklist item with no category-specific citation
- a category name appearing only in a stop condition, protected-surface bundle,
  or "do not change" list
- a category name appearing only in the title of an unrelated contract

Weak or rejected evidence should produce `SCOPE_WARNING` when it mentions a
changed protected category but fails the accepted positive evidence rules.

## Outputs

The checker prints a deterministic advisory report. It reports evidence status;
it does not report semantic validation results.

Required report categories:

- `AUTHORIZED`: protected category has matching explicit authorization
  evidence.
- `MISSING_AUTHORIZATION`: protected category was touched but no accepted
  evidence was found.
- `FORBIDDEN_PATH`: path is forbidden by the protected-surface gate and cannot
  be authorized by ordinary issue, contract, handoff, report, or PR text.
- `NOT_PROTECTED`: changed path has no protected classification.
- `UNVERIFIABLE_SOURCE`: required or useful authorization evidence was missing
  or not supplied.
- `SCOPE_WARNING`: source text mentions authorization vaguely, contradicts
  itself, names a different category, or uses rejected boilerplate.

Required text report shape:

```text
Protected Surface Authorization Check
mode: paths-from-stdin
base: origin/codex/repo-wide-hardening-run
head: HEAD
changed_paths: 2
protected: 1
forbidden: 1
authorized: 1
missing_authorization: 0
scope_warnings: 0
unverifiable_sources: 0

AUTHORIZED workbook_schema src/mythic_edge_parser/app/sheet_schema.py
evidence: contract=docs/contracts/parser_sheet_schema.md - authorized_protected_surfaces: workbook_schema

FORBIDDEN_PATH runtime_status data/status/runtime.json - Forbidden path cannot be authorized by ordinary workflow text.

authorization_status: review
```

Allowed `authorization_status` values:

- `ok`: no protected or forbidden paths require review, or all protected
  warnings have accepted evidence and no forbidden paths are present.
- `review`: report generated and human review is required because missing
  authorization, forbidden paths, unverifiable sources, or scope warnings are
  present.
- `error`: configuration or unreadable-source error.

Forbidden wording:

- Do not say `authorized to merge`.
- Do not say `safe`.
- Do not say `parser behavior passed`.
- Do not say `schema behavior passed`.
- Do not say `checks passed` unless referring only to the checker process
  itself.

If `--format json` is implemented, the JSON object must include:

- `mode`
- `base`
- `head`
- `changed_paths`
- `classifications`
- `authorization_sources`
- `authorized`
- `missing_authorization`
- `forbidden_paths`
- `not_protected`
- `unverifiable_sources`
- `scope_warnings`
- `authorization_status`

JSON support is optional in the first implementation. Text support is required.

## Exit Behavior

First-version exit behavior is advisory:

- exit `0`: report generated, including reports with
  `authorization_status: ok` or `authorization_status: review`
- exit `2`: usage/configuration error, invalid base, invalid
  `--authorization-file` syntax, unreadable supplied authorization source, or
  repository inspection failure

First-version behavior must not use exit `1`.

A future issue and contract may introduce strict mode or CI-failing behavior.
This contract does not authorize it.

## Relationship To Existing Tools

### `tools/check_protected_surfaces.py`

- Owns path classification and category IDs.
- This checker consumes its classifications.
- This checker must not weaken forbidden-path behavior.
- This checker must not redefine path patterns.

### `tools/select_validation.py`

This contract authorizes a narrow selector integration after
`tools/check_surface_authorization.py` exists.

Required selector behavior after implementation:

- Recommend the authorization checker when protected-surface classifications
  include warnings or forbidden paths.
- Do not run the authorization checker.
- Do not edit CI.
- Use a placeholder command that shows required authorization files, for
  example:

```bash
python3 tools/check_surface_authorization.py --base <base> --authorization-file issue=<issue-body-file> --authorization-file contract=<contract-file> --authorization-file pr=<pr-body-file>
```

Priority:

- `recommended` for protected warning or forbidden classifications.

Required selector tests after integration:

- protected warning paths recommend `check_surface_authorization.py`
- forbidden paths recommend `check_surface_authorization.py`
- ordinary docs-only paths do not recommend it
- selector output still does not claim checks passed

### `tools/check_secret_patterns.py`

- Owns content scanning for secrets and private markers.
- This checker must not duplicate secret regex scanning.
- Authorization text must never count as permission to commit secrets, local
  MTGA logs, raw logs, generated data, runtime status files, failed posts, or
  workbook exports.

### `tools/check_agent_docs.py`

- Owns governance-doc consistency checks.
- This checker may read supplied governance text as authorization evidence.
- This checker must not replace the agent-docs checker or rewrite governance
  authority.

### Future Orchestrator

A future `tools/run_hardening_checks.py` may run this checker with other
hardening tools. This issue must not create the orchestrator.

## Error Behavior

Configuration errors:

- missing `--base`: argparse usage error, exit `2`
- invalid base diff: `authorization_status: error`, exit `2`
- invalid `--authorization-file` syntax: `authorization_status: error`,
  exit `2`
- unknown authorization source kind: `authorization_status: error`, exit `2`
- unreadable supplied source: `authorization_status: error`, exit `2`
- invalid `--format`: argparse usage error, exit `2`

Advisory review cases:

- no authorization source supplied while protected warnings exist:
  `UNVERIFIABLE_SOURCE`, exit `0`
- protected warning with vague evidence only: `MISSING_AUTHORIZATION` plus
  `SCOPE_WARNING`, exit `0`
- protected warning with mismatched category evidence:
  `MISSING_AUTHORIZATION` plus `SCOPE_WARNING`, exit `0`
- forbidden path: `FORBIDDEN_PATH`, exit `0`

## Side Effects

Allowed side effects:

- Read Git metadata.
- Read newline-delimited stdin when requested.
- Read supplied authorization source files.
- Import or load `tools/check_protected_surfaces.py`.
- Print a report to stdout or stderr.

Forbidden side effects:

- Editing files.
- Editing CI.
- Staging, committing, pushing, or merging.
- Opening or updating issues or PRs.
- Fetching live GitHub issue or PR data.
- Running selected validation commands.
- Reading raw MTGA logs, runtime status files, failed posts, workbook exports,
  generated card data, or private local artifacts.
- Posting webhooks or touching workbook/Apps Script state.

## Dependency Order

1. Keep this contract as the source of truth for #90 implementation.
2. Implement `tools/check_surface_authorization.py`.
3. Add `tests/test_check_surface_authorization.py`.
4. If the checker is implemented and tested, update `tools/select_validation.py`
   only for the narrow recommendation integration defined above.
5. Add or update selector tests only for that integration.
6. Write
   `docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md`.
7. Run focused validation.
8. Route to Codex E for contract testing.
9. Leave CI integration, strict mode, and orchestrator work to later explicit
   issues and contracts.

## Compatibility

- The first implementation must use only the Python standard library and
  tracked repo files.
- Existing `tools/check_protected_surfaces.py` CLI and exit behavior must
  remain unchanged.
- Existing `tools/select_validation.py` behavior may only be extended with a
  recommendation; it must not run the authorization checker.
- Existing PR template, issue template, agent docs, and CI files must remain
  unchanged in #90 unless a future contract loopback explicitly authorizes
  wording changes.
- Text output must remain stable enough to paste into handoffs and PR
  descriptions.
- JSON output, if implemented, must be additive and must not replace text
  output.

## Tests Required

Focused authorization checker tests:

```bash
python3 -m pytest -q tests/test_check_surface_authorization.py
```

Required test coverage:

- missing `--base` exits `2`
- invalid base diff reports `authorization_status: error`
- `--paths-from-stdin` does not run `git diff`
- changed-path mode uses `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`
- checker consumes `tools/check_protected_surfaces.py` classification helpers
- allowed path reports `NOT_PROTECTED`
- forbidden path reports `FORBIDDEN_PATH` and is never `AUTHORIZED`
- protected path with exact category ID in accepted evidence reports
  `AUTHORIZED`
- protected path with accepted alias in accepted evidence reports `AUTHORIZED`
- protected path with no source reports `UNVERIFIABLE_SOURCE` and
  `MISSING_AUTHORIZATION`
- protected path with unrelated category evidence reports
  `MISSING_AUTHORIZATION`
- protected path with broad `all protected surfaces authorized` text reports
  `SCOPE_WARNING` and `MISSING_AUTHORIZATION`
- protected path with PR template boilerplate `unchanged or authorized` reports
  `SCOPE_WARNING` and `MISSING_AUTHORIZATION`
- `pr` or `generic` source without citation does not authorize the category
- `issue` or `contract` source with accepted evidence authorizes without an
  extra citation
- unreadable supplied source exits `2`
- duplicate authorization files and duplicate paths render deterministically
- output uses `authorization_status: ok`, `review`, or `error`
- output does not claim parser behavior, schema behavior, webhook behavior, or
  Apps Script behavior passed
- optional JSON output, if implemented, contains the contracted field names

Selector integration tests, if Codex C updates `tools/select_validation.py`:

```bash
python3 -m pytest -q tests/test_select_validation.py
```

Required selector coverage:

- protected warning path recommends `check_surface_authorization.py`
- forbidden path recommends `check_surface_authorization.py`
- allowed docs-only path does not recommend it
- recommendation is advisory/recommended and includes authorization-file
  placeholders

Implementation validation should include:

```bash
python3 -m pytest -q tests/test_check_surface_authorization.py
python3 tools/check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=<fixture-or-local-source>
python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run
python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
python3 -m ruff check src tests tools
```

If selector integration is included:

```bash
python3 -m pytest -q tests/test_select_validation.py
```

Before submitter or review completion, consider:

```bash
python3 -m pyright
python3 -m pytest -q tests
python3 tools/check_agent_docs.py
git diff --check
```

## Acceptance Criteria

- `docs/contracts/repo_wide_protected_surface_authorization_checker.md` exists
  and is cited by the implementation handoff.
- `tools/check_surface_authorization.py` exists and implements the contracted
  CLI.
- `tests/test_check_surface_authorization.py` exists and covers the required
  cases.
- The checker consumes current protected-surface classifications instead of
  maintaining a competing path table.
- The checker reports `AUTHORIZED`, `MISSING_AUTHORIZATION`,
  `FORBIDDEN_PATH`, `NOT_PROTECTED`, `UNVERIFIABLE_SOURCE`, and
  `SCOPE_WARNING` as contracted.
- The checker rejects broad template or "unchanged or authorized" wording as
  insufficient.
- The checker never treats forbidden paths as authorizable.
- The checker remains advisory and does not edit CI.
- Any selector integration is limited to recommendation behavior and has
  focused selector tests.
- No parser behavior, parser state final reconciliation, workbook schema,
  webhook payload shape, Apps Script behavior, parser event classes,
  match/game identity, deduplication, secrets, environment variables, raw logs,
  generated data, runtime status files, failed posts, workbook exports, or CI
  required/failing behavior changes are made by #90 implementation.

## Open Questions And Contract Risks

- The first version intentionally uses deterministic text matching rather than
  semantic interpretation. It may require human review for nuanced wording.
- Source files supplied by users can be incomplete or stale. The checker should
  say `review`, not pretend that absence of evidence proves unsafe code.
- The checker cannot verify the semantic correctness of a protected-surface
  change. It only verifies explicit authorization evidence.
- Strict or CI-failing behavior is deferred to a future issue and contract.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for repo-wide hardening issue #90: Protected-surface authorization checker.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/90
- Branch: codex/repo-wide-hardening-run
- Contract: docs/contracts/repo_wide_protected_surface_authorization_checker.md
- Previous completed child: #87 Validation selector, PR #89 merged
- Previous merge commit: 15bdf7c9661383fdcc6dfe456f8efa6c68662b72

Goal:
Implement the smallest coherent protected-surface authorization checker that satisfies the contract.

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/repo_wide_protected_surface_authorization_checker.md
- docs/contracts/code_hardening_protected_surface_gate.md
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- docs/contracts/repo_wide_validation_selector.md
- tools/select_validation.py
- tests/test_select_validation.py
- tools/check_secret_patterns.py
- tools/check_agent_docs.py
- .github/pull_request_template.md

Do:
- Create tools/check_surface_authorization.py.
- Create tests/test_check_surface_authorization.py.
- Use the existing protected-surface gate classification helpers rather than maintaining a competing path table.
- Keep the checker advisory/reporting-focused with exit 0 for generated review reports and exit 2 for configuration errors.
- Support --base, --repo-root, --paths-from-stdin, and repeated --authorization-file kind=path inputs.
- Reject broad or boilerplate authorization language such as "all protected surfaces authorized" and "unchanged or authorized."
- If the checker is complete and tested, update tools/select_validation.py only to recommend the checker when protected/forbidden classifications appear.
- Produce docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Edit CI.
- Fetch live GitHub issue or PR data.
- Make the checker strict/failing for missing authorization.
- Treat forbidden paths as authorizable.
- Claim parser/runtime/workbook/App Script behavior is safe.
- Change parser behavior, parser state, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Target main directly.
- Close tracker #82.
- Mark tracker #82 complete.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/90"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/repo_wide_protected_surface_authorization_checker.md"
  target_artifact: "tools/check_surface_authorization.py, tests/test_check_surface_authorization.py, docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "python3 -m pytest -q tests/test_check_surface_authorization.py"
    - "python3 tools/check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=<fixture-or-local-source>"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/select_validation.py --base origin/codex/repo-wide-hardening-run"
    - "python3 tools/check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "python3 -m ruff check src tests tools"
  stop_conditions:
    - "Do not edit CI in #90 implementation."
    - "Do not fetch live GitHub issue or PR data."
    - "Do not make the checker strict/failing for missing authorization."
    - "Do not treat forbidden paths as authorizable."
    - "Do not change parser/runtime/workbook/App Script behavior or protected surfaces."
    - "Do not target main directly."
    - "Do not close tracker #82."
    - "Do not mark tracker #82 complete."
```
