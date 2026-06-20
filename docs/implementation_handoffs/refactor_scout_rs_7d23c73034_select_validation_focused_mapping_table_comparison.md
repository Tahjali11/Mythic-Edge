# Refactor Scout RS-7D23C73034 Select Validation Focused Mapping Table Comparison

## Metadata

- Repository: Tahjali11/Mythic-Edge
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/512
- Source contract: `docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md`
- Target branch: `main`
- Risk tier: Medium-High
- Selected candidate: `RS-7D23C73034-SELECT-VALIDATION-FOCUSED-MAPPING-TABLE`

## Contract Comparison

The contract authorizes a behavior-preserving refactor only. Refactor Scout artifacts remain non-authoritative backlog context, and `tools/select_validation.py` remains the executable selector authority.

Confirmed matches:

- `tools/select_validation.py` still owns CLI execution, argument parsing, advisory selection, JSON output shape, exit policy, and public helper surfaces.
- `FOCUSED_TEST_MAPPINGS` and `PROTECTED_CATEGORY_GROUPS` remain available from the selector module for compatibility with existing tests and callers.
- The focused mapping data was moved into `tools/select_validation_mappings.py` without changing command strings, priorities, recommendation IDs, categories, notes, warnings, or Pyright advisory behavior.
- No CI, parser/runtime/workbook/webhook/App Script, analytics, AI/coaching, protected-surface, private artifact, or secret-handling behavior was changed.

## Files Changed

- `tools/select_validation.py`
  - Added a local file-based loader for selector mapping constants.
  - Re-exported mapping constants from the selector module to preserve existing public access.
- `tools/select_validation_mappings.py`
  - Added the extracted focused mapping table and protected category groups.
- `tests/test_select_validation.py`
  - Added a focused compatibility test proving mapping constants load through the selector entrypoint.
- `docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md`
  - Added this implementation comparison and review handoff.

## Validation Run

- `python3 -m pytest -q tests/test_select_validation.py` passed: 35 tests.
- `python3 -m pytest -q tests/test_hardening_orchestrator.py` passed: 19 tests.
- `python3 tools/select_validation.py --base origin/main` passed with zero changed paths reported by Git because new files are currently untracked.
- Path-scoped selector check for changed files passed and selected the expected required checks: `diff_check`, `protected_surface_gate`, `ruff`, `secret_private_marker_scan`, and `select_validation_tests`. It also recommended `agent_docs_checker` and emitted the non-blocking `pyright_advisory`.
- Path-scoped secret/private-marker scan passed: 5 scanned paths, 0 forbidden, 0 warnings.
- Path-scoped protected-surface gate passed: 5 changed paths, 0 forbidden, 0 warnings.
- `python3 -m ruff check tools tests` passed.
- `git diff --check` passed.
- Direct trailing-whitespace scan over the tracked and untracked changed files passed.
- `python3 tools/check_agent_docs.py` passed: 34 checked files, 0 errors, 0 warnings.
- `python3 tools/run_pyright_advisory_report.py` completed as advisory/non-blocking with `status: advisory_findings`, `exit_code: 1`, and 388 type findings.

## Remaining Risks

- The selector mapping data is now split across two files. The added compatibility test covers the intended selector entrypoint import path, including the test suite's `spec_from_file_location` pattern.
- There is no intended behavior change. Review should compare recommendation output for representative path sets if extra assurance is desired.
- The contract file existed as an untracked input when implementation began. This pass did not alter the contract.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #512, Refactor Scout RS-7D23C73034 select-validation focused mapping table.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/512

Branch:
main

Source contract:
docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md

Implementation handoff:
docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md

Goal:
Review whether Codex C preserved validation selector behavior while extracting focused mapping data into a separate local mapping module. Treat Refactor Scout artifacts as non-authoritative context only.

Review focus:
- Confirm tools/select_validation.py remains the executable selector authority.
- Confirm CLI behavior, public helper surfaces, constants exposed through the selector module, recommendation IDs, command strings, priorities, categories, notes, warnings, JSON output shape, and exit policies are unchanged.
- Confirm Pyright remains advisory and no CI gate or validation policy changed.
- Confirm tools/select_validation_mappings.py is pure mapping data and import-compatible with direct CLI execution and tests that load select_validation.py via spec_from_file_location.
- Confirm tests cover the new entrypoint compatibility boundary.
- Confirm no protected parser/runtime/workbook/webhook/App Script, analytics, AI/coaching, protected-surface, private-artifact, or secret-handling behavior changed.

Suggested validation:
- python3 -m pytest -q tests/test_select_validation.py
- python3 -m pytest -q tests/test_hardening_orchestrator.py
- python3 tools/select_validation.py --base origin/main
- Path-scoped selector, secret/private-marker, and protected-surface checks for changed files.
- python3 -m ruff check tools tests
- git diff --check

Do not:
- Treat Refactor Scout artifacts as implementation authority.
- Change validation policy, selector recommendations, command output, CLI behavior, CI gates, Pyright advisory status, protected-surface behavior, parser truth, workbook/webhook/App Script behavior, analytics truth, AI/coaching behavior, production behavior, private artifacts, or secrets handling.
- Stage, commit, push, close issue #512, or target another repository unless explicitly asked.

End with:
- findings first, ordered by severity
- validation run
- residual risks
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/512"
  tracker: ""
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md"
  target_artifact: "docs/implementation_handoffs/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table_comparison.md"
  risk_tier: "Medium-High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  selected_candidate: "RS-7D23C73034-SELECT-VALIDATION-FOCUSED-MAPPING-TABLE"
  artifact_authority: "non_authoritative_refactor_scout_context"
  validation:
    - "python3 -m pytest -q tests/test_select_validation.py"
    - "python3 -m pytest -q tests/test_hardening_orchestrator.py"
    - "python3 tools/select_validation.py --base origin/main"
    - "path-scoped selector check for changed files"
    - "path-scoped secret/private-marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "python3 -m ruff check tools tests"
    - "git diff --check"
  stop_conditions:
    - "Do not treat Refactor Scout artifacts as implementation authority."
    - "Do not change validation policy, selector recommendations, command output, CLI behavior, CI gates, Pyright advisory status, protected-surface behavior, parser truth, workbook/webhook/App Script behavior, analytics truth, AI/coaching behavior, production behavior, private artifacts, or secrets handling."
```
