# Refactor Scout RS-7D23C73034 Select Validation Focused Mapping Table Contract

## Module

`refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table`

Plain English: this contract authorizes a narrow, behavior-preserving
refactor of `tools/select_validation.py` so focused validation mapping data and
mapping-adjacent helpers may be separated from selector decision flow without
changing validation policy, CLI behavior, report shape, recommendation
priorities, command strings, protected-surface handling, or downstream review
semantics.

The Refactor Scout artifact is non-authoritative backlog context. This source
repo contract, issue #512, and later review evidence are the authority for any
implementation.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/512
- Source artifact:
  `RS-7D23C73034-SELECT-VALIDATION-FOCUSED-MAPPING-TABLE`
- Artifact source repository: `Tahjali11/Mythic-Edge-Automation-Artifacts`
- Artifact source URL:
  `https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/blob/main/refactor-scout/candidates/RS-7D23C73034-SELECT-VALIDATION-FOCUSED-MAPPING-TABLE.md`
- Target file or cluster: `tools/select_validation.py`
- Target artifact:
  `docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md`
- Base branch: `main`
- Target branch: `main`
- Risk tier: Medium-High

Issue #512 was manually created after the user explicitly overrode the
Refactor Scout missing-label gate for this issue only:

```yaml
issue_creation_status: "manual_override_missing_label_gate"
missing_label: "automation:refactor-scout"
```

That override does not create the missing label, does not authorize future
automated issue creation, and does not make Refactor Scout artifacts
implementation authority.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/contracts/validation_matrix_reconciliation.md`
- `docs/contract_test_reports/validation_matrix_reconciliation.md`
- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `tools/run_hardening_orchestrator.py`
- `tests/test_hardening_orchestrator.py`
- `.github/workflows/repo-checks.yml`
- `tools/check_protected_surfaces.py`
- `tools/check_secret_patterns.py`
- `tools/check_agent_docs.py`
- Refactor Scout candidate
  `RS-7D23C73034-SELECT-VALIDATION-FOCUSED-MAPPING-TABLE`
- Refactor Scout `candidate_registry.md` and `candidate_registry.json` as
  read-only non-authoritative context

## Tracker

N/A.

Related context only:

- https://github.com/Tahjali11/Mythic-Edge/issues/463
- https://github.com/Tahjali11/Mythic-Edge/issues/465

Neither issue is a tracker for this contract, and this contract does not close
or update them.

## Owning Layer

Primary owner: Quality / Governance.

Internal project area: Quality / Governance.

Bridge-code status: `shared_support`

Allowed data flow:

```text
repo-relative changed paths
  -> selector category and focused-test mapping data
  -> validation recommendations
  -> Codex/human validation planning
```

Forbidden reverse flow:

- selector mappings must not change parser truth;
- selector output must not prove validation passed;
- selector output must not decide merge readiness, deploy readiness, release
  readiness, production behavior, tracker completion, or protected-surface
  authorization;
- selector output must not alter CI gates or Pyright gate policy.

## Truth Owner

`tools/select_validation.py` remains the executable changed-path validation
selector authority.

`tools/run_hardening_orchestrator.py` remains the local bundle planner/runner
authority.

`docs/validation_matrix.md` remains a non-authoritative reference only.

Individual checkers own their own findings:

- `tools/check_protected_surfaces.py`
- `tools/check_secret_patterns.py`
- `tools/check_surface_authorization.py`
- `tools/check_agent_docs.py`
- `tools/check_local_environment.py`
- `tools/run_pyright_advisory_report.py`

This contract owns only the refactor boundary for selector mapping data. It
does not own validation policy changes.

## Observed Current Behavior

Current `tools/select_validation.py`:

- is a standalone script, not part of a Python package;
- exposes constants, dataclasses, normalization helpers, categorization
  helpers, selector functions, rendering functions, parser construction, and
  `main`;
- contains `FOCUSED_TEST_MAPPINGS` as an in-file tuple;
- contains `PROTECTED_CATEGORY_GROUPS` as an in-file set;
- contains path-category logic in `categorize_path`;
- contains command-id derivation in `_command_id_for_pytest`;
- contains selector decision flow in `select_recommendations`;
- dynamically loads `tools/check_protected_surfaces.py` via
  `importlib.util.spec_from_file_location`;
- is loaded by `tests/test_select_validation.py` using
  `importlib.util.spec_from_file_location`, not a package import;
- is invoked by `tools/run_hardening_orchestrator.py` as
  `python3 tools/select_validation.py --base <base>`;
- is referenced by hardening reports and docs as the executable selector.

Current `tests/test_select_validation.py` pins:

- base argument behavior;
- changed-path and stdin modes;
- path normalization and outside-repo redaction;
- zero changed path advisory behavior;
- docs-only behavior;
- governance docs and contract/report docs routing;
- hardening tool focused tests;
- parser, workbook, webhook, fixture, frontend, local app, analytics, local
  artifact, CI/dependency, and protected-surface routing;
- Pyright as advisory;
- JSON output fields;
- report wording as selection vocabulary, not validation results.

## Scope Decision

Implementation may proceed only as behavior-preserving internal extraction.

Codex C may split mapping data from selector decision logic if, and only if,
the resulting selector produces the same outputs for all currently tested
paths and preserves the current public interface.

Preferred implementation shape:

- keep `tools/select_validation.py` as the CLI entrypoint and executable
  selector authority;
- optionally add `tools/select_validation_mappings.py` for mapping constants
  and pure mapping helpers;
- update `tests/test_select_validation.py` only to pin extraction boundaries
  or import-mode compatibility;
- produce
  `docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md`.

If the import mechanics for a helper module become awkward because `tools/` is
not a package and tests load the script with `spec_from_file_location`, Codex C
must either:

- keep the relevant constants in `tools/select_validation.py`, or
- use a path-local import/load pattern that works both when the script is run
  as `python3 tools/select_validation.py` and when tests load it by file spec.

Codex C must not introduce package-level assumptions that make either entry
path fail.

## Files Owned By This Contract

Codex B creates:

- `docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md`

Future Codex C may edit:

- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md`

Future Codex C may add:

- `tools/select_validation_mappings.py`, only if import compatibility is
  preserved exactly

Referenced but not owned:

- `tools/run_hardening_orchestrator.py`
- `tests/test_hardening_orchestrator.py`
- `docs/contracts/validation_matrix_reconciliation.md`
- `docs/validation_matrix.md`
- `.github/workflows/repo-checks.yml`
- protected-surface, secret, surface-authorization, agent-docs, local
  environment, and Pyright tools

Not owned:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- analytics behavior;
- local app behavior;
- frontend behavior;
- AI/coaching behavior;
- CI gate policy;
- Pyright gate policy;
- private/local/generated artifacts;
- production behavior.

## Public Interface

The following `tools/select_validation.py` surfaces must remain compatible:

- CLI:
  - `--base`
  - `--repo-root`
  - `--paths-from-stdin`
  - `--format text|json`
- exit codes:
  - `0` for successful selection, including warnings;
  - `2` for argument/configuration/git-diff errors;
- output modes:
  - text report from `render_report`;
  - JSON report from `render_json`;
- JSON top-level fields:
  - `base`
  - `categories`
  - `changed_paths`
  - `head`
  - `mode`
  - `notes`
  - `recommendations`
  - `selection_status`
  - `warnings`
- dataclasses:
  - `Recommendation`
  - `SelectorWarning`
  - `AdvisoryNote`
  - `SelectionResult`
- constants used by tests or adjacent tooling:
  - mode, priority, and status constants;
- callable helpers:
  - `normalize_path`
  - `normalize_paths`
  - `categorize_path`
  - `categorize_paths`
  - `collect_changed_paths`
  - `is_tracked_file`
  - `classify_protected_warnings`
  - `select_recommendations`
  - `run_selector_for_paths`
  - `run_selector`
  - `render_report`
  - `render_json`
  - `build_parser`
  - `main`

Any new helper module is internal. External callers must continue to use
`tools/select_validation.py` and the surfaces above.

## Inputs

Primary inputs:

- repo-relative changed paths;
- optional stdin path list;
- git base ref;
- repository root;
- tracked-file state from Git;
- protected-surface classifications from
  `tools/check_protected_surfaces.py`.

Input normalization requirements:

- normalize path separators to `/`;
- trim leading `./`;
- deduplicate and sort paths;
- ignore outside-repo absolute paths with redacted warning text;
- do not expose local absolute paths in selector output.

## Outputs

Selector outputs must remain recommendation-only.

Recommendations include:

- `priority`;
- `command_id`;
- `command`;
- `reason`;
- `categories`;
- `paths`.

Warnings include:

- `category_id`;
- redacted or repo-relative `path`;
- `reason`.

Notes include:

- `note_id`;
- `message`.

Selector output must not claim that validation passed, checks passed, a PR is
ready to merge, a deployment is ready, or a protected-surface change is
authorized.

## Invariants

- This is a refactor contract, not a behavior-change contract.
- `tools/select_validation.py` remains the executable selector authority.
- `tools/run_hardening_orchestrator.py` remains the orchestrator authority.
- `docs/validation_matrix.md` remains non-authoritative.
- No new canonical `docs/validation_matrix.json` may be created.
- Existing recommendation command strings, command IDs, priorities, category
  labels, paths metadata, warning labels, note labels, and JSON/text report
  shapes must remain unchanged unless a future contract explicitly authorizes
  a validation-policy change.
- Pyright remains advisory.
- Protected-surface authorization remains recommended review evidence, not
  automatic authorization.
- Selector warnings do not change exit code from 0.
- Errors continue to exit 2.
- Refactor Scout remains non-authoritative.

## Error Behavior

Codex C must stop and route back to Codex B if implementation would require:

- changing selector policy;
- changing command strings;
- changing priorities;
- changing CLI arguments or exit codes;
- changing JSON/text output shape;
- changing protected-surface warning behavior;
- changing Pyright from advisory to required/recommended;
- changing hardening orchestrator behavior;
- creating a canonical executable validation matrix config;
- adding CI gates;
- touching protected parser/runtime/workbook/webhook/App Script/analytics/AI
  behavior surfaces.

If helper-module import compatibility fails under either CLI execution or the
current `spec_from_file_location` test import path, Codex C must keep the
mapping data in `tools/select_validation.py` or add a narrowly tested loader
without changing public behavior.

## Side Effects

Allowed side effects in Codex C:

- move mapping constants or pure mapping helpers;
- add an internal helper module if safe;
- update focused selector tests;
- write the implementation handoff.

Forbidden side effects:

- running or changing CI;
- creating or editing GitHub issues;
- modifying Refactor Scout artifacts;
- editing validation policy docs unless a mismatch is found and routed back to
  Codex B;
- changing source-repo behavior outside selector internals;
- committing private/local/generated artifacts.

## Dependency Order

Codex C should proceed in this order:

1. Re-run baseline selector tests before editing, if practical.
2. Identify constants and helper code that can move without policy changes.
3. Implement the smallest extraction.
4. Verify both script execution and importlib loading still work.
5. Run focused selector tests.
6. Run orchestrator tests if selector invocation or output integration is
   touched.
7. Run validation selector over the changed file list.
8. Run protected-surface and secret/private-marker checks on changed paths.
9. Write the implementation handoff.

## Compatibility

Compatibility must be preserved for:

- direct CLI usage;
- `--paths-from-stdin`;
- `--format json`;
- hardening orchestrator invocation;
- tests loading the script by file path;
- docs and reports that refer to `tools/select_validation.py`;
- Windows GitHub Actions running repo checks with Python;
- source-repo workflows that paste path-scoped selector commands.

## Tests Required

Minimum Codex C validation:

```bash
python3 -m pytest -q tests/test_select_validation.py
python3 -m pytest -q tests/test_hardening_orchestrator.py
python3 tools/select_validation.py --base origin/main
printf '%s\n' tools/select_validation.py tests/test_select_validation.py docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
printf '%s\n' tools/select_validation.py tests/test_select_validation.py docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' tools/select_validation.py tests/test_select_validation.py docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m ruff check tools tests
git diff --check
```

If Codex C adds `tools/select_validation_mappings.py`, include it in every
path-scoped validation command and add or update tests proving the helper works
through the current test import path.

Recommended Codex B validation for this contract-only pass:

```bash
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

## Acceptance Criteria

- The contract exists at the target artifact path.
- It treats the Refactor Scout artifact as non-authoritative context.
- It authorizes only behavior-preserving extraction.
- It names `tools/select_validation.py` as the executable selector authority.
- It preserves the validation matrix reconciliation decisions.
- It names exact public interfaces that must not change.
- It names the helper-module import compatibility risk.
- It defines validation evidence for Codex C.
- It does not authorize validation policy changes, CI gate changes, parser
  truth changes, protected-surface changes, private artifact changes, or
  production behavior changes.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #512.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Source artifact:
docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md

Target artifact:
docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md

Goal:
Implement only the behavior-preserving selector mapping extraction authorized
by the contract. Keep `tools/select_validation.py` as the executable selector
authority. Do not change selector policy, CLI behavior, output shape,
recommendation priorities, command strings, protected-surface behavior,
Pyright advisory status, CI gates, parser truth, runtime behavior,
workbook/webhook/App Script behavior, analytics truth, AI/coaching behavior,
or production behavior.

Use:
- issue #512
- docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md
- tools/select_validation.py
- tests/test_select_validation.py
- tools/run_hardening_orchestrator.py
- tests/test_hardening_orchestrator.py
- docs/contracts/validation_matrix_reconciliation.md

Validation:
- python3 -m pytest -q tests/test_select_validation.py
- python3 -m pytest -q tests/test_hardening_orchestrator.py
- python3 tools/select_validation.py --base origin/main
- path-scoped selector, secret/private-marker, and protected-surface checks for changed files
- python3 -m ruff check tools tests
- git diff --check
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/512"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md"
  target_artifact: "docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md"
  risk_tier: "Medium-High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  selected_candidate: "RS-7D23C73034-SELECT-VALIDATION-FOCUSED-MAPPING-TABLE"
  artifact_authority: "non_authoritative_refactor_scout_context"
  validation:
    - "python3 tools/check_agent_docs.py"
    - "printf '%s\\n' docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --check"
  stop_conditions:
    - "Do not implement code outside the selector mapping extraction authorized by this contract."
    - "Do not change validation policy, selector recommendations, command output, CLI behavior, CI gates, Pyright advisory status, protected-surface behavior, parser truth, workbook/webhook/App Script behavior, analytics truth, AI/coaching behavior, production behavior, private artifacts, or secrets handling."
    - "Do not treat Refactor Scout artifacts as implementation authority."
```
