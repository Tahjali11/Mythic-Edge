# Implementation Handoff: Ruff Low-Churn Exact-Code Cleanup Candidate Selection

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/638

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Project Roadmap

https://github.com/Tahjali11/Mythic-Edge/issues/568

## Contract

`docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md`

## Internal Project Area

Quality / Ruff advisory cleanup.

## Truth Owner

Ruff cleanup owns style/lint conformance only. It does not own parser truth,
runtime truth, security assurance, privacy assurance, release readiness,
analytics truth, AI truth, or coaching truth.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifacts Used

- Issue #638
- Tracker #567
- Project roadmap #568
- Source issue #631
- `docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`

## Branch And Git Status

Branch:

```text
codex/ruff-low-churn-candidate-638
```

Base:

```text
origin/main
```

Current base commit at implementation time:

```text
6f876a78c5294b58111f43a364596498004fc3eb
```

Branch sync:

```text
git rev-list --left-right --count HEAD...origin/main -> 0 0
```

Starting status:

```text
## codex/ruff-low-churn-candidate-638...origin/main
?? docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md
```

Final status:

```text
## codex/ruff-low-churn-candidate-638...origin/main
 M tests/test_app_extractors.py
 M tests/test_diagnostics.py
 M tools/generate_security_quality_summary.py
?? docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md
?? docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md
```

## Files Inspected

- `docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md`
- `tests/test_app_extractors.py`
- `tests/test_diagnostics.py`
- `tools/generate_security_quality_summary.py`
- `tests/test_security_quality_summary.py`

## Current Behavior Compared To Contract

The contract authorized cleanup consideration for `DTZ001` and `TRY301` only.
It explicitly deferred `PERF403`, `RUF022`, `RUF059`, preview mode, autofix,
unsafe-fix, Ruff promotion, CI changes, and `pyproject.toml` changes.

Fresh current-base evidence before editing:

```powershell
py -m ruff check src tests tools --select DTZ001,TRY301 --output-format json --exit-zero
```

Ruff version:

```text
ruff 0.15.12
```

Fresh findings:

| Code | Count | Paths |
| --- | ---: | --- |
| `DTZ001` | 1 | `tests/test_app_extractors.py:343` |
| `TRY301` | 3 | `tests/test_diagnostics.py:46`; `tools/generate_security_quality_summary.py:759`; `tools/generate_security_quality_summary.py:762` |

The findings remained limited to the expected test/tool paths, so Codex C
proceeded with the tiny behavior-preserving cleanup.

## Implementation Option Chosen

Implemented only the selected exact-code cleanup:

- `DTZ001`
- `TRY301`

No broad cleanup, promotion, config change, CI change, preview mode, autofix,
unsafe-fix, or deferred-code cleanup was performed.

## Files Changed

- `tests/test_app_extractors.py`
- `tests/test_diagnostics.py`
- `tools/generate_security_quality_summary.py`
- `docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md`
  - preserved as the Codex B contract artifact.
- `docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md`

## Exact Sections Changed

### `tests/test_app_extractors.py`

Changed the test timestamp in
`test_event_datetime_and_safe_iso_use_valid_metadata_timestamp` from a naive
`datetime` to a timezone-aware UTC `datetime`.

The assertion now compares `_safe_iso(event)` to `timestamp.isoformat()` so the
test still verifies the same behavior: `_safe_iso` preserves the provided valid
metadata timestamp.

### `tests/test_diagnostics.py`

Added `_raise_router_failure_for_test()` and called it from the existing
`try`/`except` block in `test_record_router_failure_updates_status_and_writes_entry`.

The exception type, exception message, recorded failure behavior, and assertions
are unchanged.

Also replaced a pre-existing raw-log-shaped header fixture with
`synthetic-router-header` so the touched file remains public-safe under the
path-scoped secret/private-marker scan. The test does not assert the header
value, and router failure body/status behavior is unchanged.

### `tools/generate_security_quality_summary.py`

Added two small helpers:

- `_validate_codeql_state_source`
- `_required_codeql_summary_path`

The helpers preserve the same `UnsafeInputError` source IDs and reasons:

- `codeql`, `blocked_unsupported_mode`
- `codeql`, `blocked_unavailable`

No report schema, output shape, public-safe redaction behavior, CodeQL state
mutation behavior, or external behavior changed.

## Code Changed

Runtime/product code changed: no.

Tool code changed: yes, in `tools/generate_security_quality_summary.py`.

The tool change is behavior-preserving and only moves existing validation raises
into helpers to satisfy `TRY301`.

## Tests Changed

Yes.

- `tests/test_app_extractors.py`
- `tests/test_diagnostics.py`

No new test file was added because the existing focused tests already covered
the touched behavior.

## Interface Changes

None.

No public CLI options, function signatures used by callers, payload fields,
workbook columns, environment variables, CI gates, Ruff configuration, parser
interfaces, or report schemas changed.

## Deferred Rules Preserved

Not touched:

- `PERF403`
- `RUF022`
- `RUF059`

Also not touched:

- `pyproject.toml`
- CI / repo checks
- preview mode
- autofix / unsafe-fix
- any broad Ruff family

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# before implementation:
# ## codex/ruff-low-churn-candidate-638...origin/main
# ?? docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md

git rev-list --left-right --count HEAD...origin/main
# 0 0

py -m ruff --version
# ruff 0.15.12

py -m ruff check src tests tools --select DTZ001,TRY301 --output-format json --exit-zero
# pre-implementation: 4 findings
# DTZ001: tests/test_app_extractors.py
# TRY301: tests/test_diagnostics.py
# TRY301: tools/generate_security_quality_summary.py x2

py -m ruff check src tests tools --select DTZ001,TRY301
# All checks passed!

py -m pytest -q tests\test_app_extractors.py tests\test_diagnostics.py tests\test_security_quality_summary.py
# 42 passed in 0.66s

py -m ruff check src tests tools
# All checks passed!

git diff --check
# passed

py tools\check_agent_docs.py
# passed: checked_files 52, errors 0, warnings 0

@'
tests/test_app_extractors.py
tests/test_diagnostics.py
tools/generate_security_quality_summary.py
docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md
docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

@'
tests/test_app_extractors.py
tests/test_diagnostics.py
tools/generate_security_quality_summary.py
docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md
docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
# result: warning
# forbidden 0, warnings 1
# warning: pre-existing artifact_path_reference in tests/test_diagnostics.py test name

changed-file whitespace/final-newline check
# passed
```

## Protected-Surface Status

Passed.

Path-scoped scan over changed files and the untracked contract/handoff:

- forbidden: `0`
- warnings: `0`
- result: passed

Assessment:

- No parser source files changed.
- No parser state final reconciliation, parser event classes, match/game
  identity, deduplication, workbook/webhook/App Script/Sheets behavior,
  analytics truth, AI/coaching behavior, Line Tracer behavior, or production
  behavior changed.
- Tool change is limited to public-safe advisory security-summary validation
  control flow.

## Secret / Private-Marker Status

Passed with one warning and no forbidden findings.

Path-scoped scan over changed files and the untracked contract/handoff:

- forbidden: `0`
- warnings: `1`
- result: warning

Warning:

- `tests/test_diagnostics.py` contains a pre-existing
  `artifact_path_reference` warning in a test name mentioning runtime status.

No raw logs, generated artifacts, local-only artifacts, workbook exports,
failed posts, secrets, credentials, endpoint values, tokens, private paths, or
private scanner output were added.

## Still Unverified

- Codex E has not independently reviewed the cleanup against the contract.
- GitHub CI has not run for this branch.
- Secret/private-marker scan has one warning in a touched diagnostics test name;
  Codex E should verify it is acceptable and not introduced as private data.

## Reviewer Focus

Codex E should verify:

- fresh Ruff evidence matched the contract before edits;
- only `DTZ001` and `TRY301` were cleaned;
- `PERF403`, `RUF022`, and `RUF059` remain untouched;
- no `pyproject.toml`, CI, preview, autofix, unsafe-fix, or rule promotion
  occurred;
- the test timestamp change preserves test intent;
- the diagnostics exception helper preserves exception type/message and status
  behavior;
- the security-summary helper split preserves blocked-input behavior and
  public-safe output boundaries.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #638.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/638

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/ruff-low-churn-candidate-638

Contract:
docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md

Goal:
Review the Codex C low-churn Ruff cleanup against the contract. Confirm the
cleanup is limited to DTZ001 and TRY301, behavior-preserving, and does not
promote any Ruff rule or touch deferred findings.

Review focus:
- Confirm fresh pre-edit Ruff evidence was limited to expected test/tool paths.
- Confirm only tests/test_app_extractors.py, tests/test_diagnostics.py, and tools/generate_security_quality_summary.py changed.
- Confirm DTZ001 and TRY301 now pass.
- Confirm full stable Ruff still passes.
- Confirm PERF403, RUF022, RUF059, pyproject.toml, CI, preview mode, autofix, unsafe-fix, and broad cleanup were not touched.
- Confirm exception types/messages and public-safe security-summary behavior are preserved.
- Confirm no parser/runtime/local app/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

Suggested validation:
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
py -m ruff check src tests tools --select DTZ001,TRY301
py -m pytest -q tests\test_app_extractors.py tests\test_diagnostics.py tests\test_security_quality_summary.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.

Do not:
- Edit files in Codex E unless explicitly asked.
- Edit pyproject.toml, CI, Ruff config, preview mode, autofix, or unsafe-fix.
- Clean up PERF403, RUF022, RUF059, or any other rule.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics truth, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, production behavior, fixtures, or corpus status.
- Stage, commit, push, open a PR, merge, or close issues unless explicitly asked.

Final output must include:
- findings first, ordered by severity;
- contract-test verdict;
- validation run and results;
- protected-surface and secret/private-marker status;
- whether #638 can route to Codex F or needs Codex D/B/A;
- next recommended role;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/638"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md"
  risk_tier: "Medium workflow risk; low runtime risk because cleanup remained test/tool-only"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/ruff-low-churn-candidate-638"
  selected_cleaned_codes:
    - "DTZ001"
    - "TRY301"
  deferred_candidate_codes:
    - "PERF403"
    - "RUF022"
    - "RUF059"
  validation:
    - "py -m ruff check src tests tools --select DTZ001,TRY301 --output-format json --exit-zero -> pre-edit 4 expected findings"
    - "py -m ruff check src tests tools --select DTZ001,TRY301 -> passed"
    - "py -m pytest -q tests\\test_app_extractors.py tests\\test_diagnostics.py tests\\test_security_quality_summary.py -> 42 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> warning, forbidden 0, warnings 1 pre-existing diagnostics test-name wording"
    - "changed-file whitespace/final-newline check -> passed"
  stop_conditions:
    - "Do not edit pyproject.toml, CI, Ruff config, preview mode, autofix, or unsafe-fix."
    - "Do not clean up PERF403, RUF022, RUF059, or any other rule in this slice."
    - "Do not change parser/runtime/local app/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior, fixtures, or corpus status."
    - "Do not touch raw logs, generated artifacts, local-only artifacts, workbook exports, failed posts, secrets, credentials, endpoint values, tokens, private paths, or private scanner output."
```
