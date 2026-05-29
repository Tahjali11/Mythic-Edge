# Quality Pyright Evidence-Ledger Tests Comparison

## Issue

Recommended new child issue under tracker #136.

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/136>

## Contract

`docs/contracts/quality_pyright_evidence_ledger_tests.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifact Used

Pyright advisory report and Codex A grouping, as formalized by
`docs/contracts/quality_pyright_evidence_ledger_tests.md`.

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`

Initial status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation [ahead 1]
?? docs/contracts/analytics_local_developer_app_shell.md
?? docs/contracts/quality_pyright_evidence_ledger_tests.md
```

Tracker #136 was confirmed open. The unrelated untracked
`docs/contracts/analytics_local_developer_app_shell.md` artifact was left
untouched.

Final status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation [ahead 1]
 M tests/test_evidence_ledger.py
?? docs/contracts/analytics_app_backend_setup_status.md
?? docs/contracts/analytics_local_developer_app_shell.md
?? docs/contracts/quality_pyright_evidence_ledger_tests.md
?? docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md
```

The untracked `docs/contracts/analytics_app_backend_setup_status.md` appeared
after the initial inspection and was also left untouched.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_pyright_evidence_ledger_tests.md`
- `pyrightconfig.json`
- `tools/run_pyright_advisory_report.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `tests/test_evidence_schema_snapshot.py`
- `tests/test_evidence_schema_drift_report.py`

## Current Behavior Compared To Contract

Contract matches:

- Pyright is configured as an advisory static analysis surface and remains
  non-gating.
- `tools/run_pyright_advisory_report.py --format json` produces a stable
  advisory report with classified findings.
- `tests/test_evidence_ledger.py` remains included in Pyright coverage.
- Evidence-ledger source behavior already returns dynamic JSON-like
  `dict[str, Any]` values from `build_player_log_evidence_ledger()` and
  `iter_ledger_entries()`.
- The test module already has exact evidence-ledger assertions for families,
  entry IDs, direct/fallback evidence, policies, privacy, and validator
  behavior.

Contract mismatch / quality gap found:

- Test-local helpers in `tests/test_evidence_ledger.py` narrowed the dynamic
  ledger shape to `dict[str, object]`.
- Pyright then treated nested values such as `seed_fields`, `future_fields`,
  `direct_evidence`, and `fallback_evidence` as plain `object`, causing
  advisory findings for iteration, indexing, set operations, and argument
  types.
- Baseline Pyright count for `tests/test_evidence_ledger.py`: `557`.
- Baseline repo-wide advisory count: `645`.

Missing safeguards/tests:

- No missing runtime safeguard was identified.
- The missing quality safeguard was test-local type visibility for dynamic
  evidence-ledger data.
- No additional evidence-ledger behavioral test was required because the
  existing assertions were retained and continued to pass.

## Implementation Option Chosen

Implemented the smallest contract-authorized test-local typing cleanup:

- Preserve the evidence-ledger runtime implementation.
- Preserve all exact assertions.
- Keep Pyright advisory-only.
- Improve only the dynamic helper annotations and one intentional negative
  validator call in `tests/test_evidence_ledger.py`.

## Files Changed

- `tests/test_evidence_ledger.py`
- `docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md`

## Exact Sections Changed

`tests/test_evidence_ledger.py`:

- Added standard-library typing imports: `Any`, `cast`.
- Changed `_entries_by_id()` to return `dict[str, dict[str, Any]]` and assert
  that each dynamic `entry_id` is a string before using it as a key.
- Changed `_family()` and `_tier*_family()` helpers from `dict[str, object]`
  to `dict[str, Any]` to preserve the producer's dynamic JSON-like shape.
- Changed `_signal_ids()` and `_all_signal_ids()` to accept
  `dict[str, Any]`, with a list assertion before iterating dynamic signal
  lists.
- Cast the intentional `"not-a-mapping"` negative validator input to `Any`,
  preserving the runtime assertion while making the invalid-input test intent
  explicit to Pyright.

`docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md`:

- Added this comparison/implementation handoff.

## Code Changed

Runtime code changed: no.

Tests changed: yes, `tests/test_evidence_ledger.py`.

Docs changed: yes, implementation handoff only.

Quality-only change: yes.

## Pyright Advisory Evidence

Before:

```text
py tools\run_pyright_advisory_report.py --format json
status: advisory_findings
errors: 645
warnings: 0
information: 0
type_findings: 645
local_resolver_noise: 0
tooling_config_blockers: 0

file grouping:
pyright_exit 1
tests/test_evidence_ledger.py 557
total 645
tests/test_evidence_ledger.py rules:
reportArgumentType: 59
reportAttributeAccessIssue: 10
reportCallIssue: 2
reportGeneralTypeIssues: 260
reportIndexIssue: 45
reportOperatorIssue: 181
```

After:

```text
py tools\run_pyright_advisory_report.py --format json
status: advisory_findings
errors: 88
warnings: 0
information: 0
type_findings: 88
local_resolver_noise: 0
tooling_config_blockers: 0

file grouping:
pyright_exit 1
tests/test_evidence_ledger.py 0
total 88
tests/test_evidence_ledger.py rules: {}
```

Residual Pyright findings remain outside `tests/test_evidence_ledger.py`.
Zero repo-wide Pyright findings was not required by the contract and was not
attempted.

## Validation Run

```text
git status --short --branch
py -m pytest -q tests\test_evidence_ledger.py
py -m ruff check tests\test_evidence_ledger.py
py tools\run_pyright_advisory_report.py --format json
py -m pytest -q tests\test_evidence_schema_snapshot.py tests\test_evidence_schema_drift_report.py
py -m ruff check src tests tools
py tools\check_agent_docs.py
git diff --check
@'
tests/test_evidence_ledger.py
docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
tests/test_evidence_ledger.py
docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
py tools\check_secret_patterns.py --all
```

Results:

```text
py -m pytest -q tests\test_evidence_ledger.py -> 101 passed
py -m ruff check tests\test_evidence_ledger.py -> All checks passed
py tools\run_pyright_advisory_report.py --format json -> advisory_findings, helper exit 0
py -m pytest -q tests\test_evidence_schema_snapshot.py tests\test_evidence_schema_drift_report.py -> 35 passed
py -m ruff check src tests tools -> All checks passed
py tools\check_agent_docs.py -> passed
git diff --check -> passed
path-scoped protected-surface gate -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan -> failed on pre-existing literal marker tests in tests/test_evidence_ledger.py
py tools\check_secret_patterns.py --all -> failed on pre-existing repo findings outside this slice
```

The secret/private-marker failures did not correspond to new diff lines. The
changed lines only added typing imports, helper annotations/narrowing, and an
explicit `cast(Any, "not-a-mapping")` for a negative validator test.

## Protected-Surface Status

No parser, runtime, workbook, webhook, Apps Script, Google Sheets, Match
Journal, OpenAI/model-provider, AI/coaching, or production behavior was
changed.

No Pyright config, CI gate, source evidence-ledger behavior, fixtures,
snapshots, drift baselines, secrets, raw logs, generated data, runtime status
files, failed posts, workbook exports, or local-only artifacts were changed.

## Secret/Private-Marker Status

No private data, raw logs, secrets, webhook URLs, workbook IDs, deployment IDs,
generated artifacts, or local-only artifacts were added in the diff.

The path-scoped secret/private-marker scan over the touched files failed on
pre-existing literal marker assertions in `tests/test_evidence_ledger.py`:

```text
tests/test_evidence_ledger.py:3604
tests/test_evidence_ledger.py:3686
tests/test_evidence_ledger.py:3687
```

Those lines exercise evidence-ledger privacy validation and were not edited in
this slice.

## Assertions And Boundaries

- No evidence-ledger assertions were weakened, skipped, xfailed, deleted, or
  replaced with broad smoke tests.
- No `# type: ignore`, file-level Pyright suppression, or Pyright config
  exclusion was added.
- The tests still inspect the same ledger families, entry IDs, direct evidence,
  fallback evidence, policies, privacy checks, and validator behavior.

## Still Unverified

- The remaining repo-wide Pyright advisory findings outside
  `tests/test_evidence_ledger.py` were not remediated.
- `tools/run_pyright_advisory.ps1` wrapper behavior was not changed or
  revalidated; the contract explicitly kept wrapper edits out of scope.
- Live workbook state, deployed Apps Script state, Google Sheets behavior,
  OpenAI/model-provider behavior, and production behavior were not exercised.

## Reviewer Focus

Codex E should verify:

- The helper annotation changes do not weaken any assertion.
- The `Any` and `cast` usage stays localized to the dynamic ledger boundary and
  intentional invalid-input validator test.
- `tests/test_evidence_ledger.py` remains included in Pyright and is at zero
  diagnostics.
- Pyright remains advisory and non-gating.
- No referenced-but-not-owned files were edited.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for quality_pyright_evidence_ledger_tests.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Issue:
Recommended new child issue under #136.

Branch:
codex/analytics-foundation

Contract:
docs/contracts/quality_pyright_evidence_ledger_tests.md

Implementation handoff:
docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md

Risk tier:
Medium

Review goal:
Review Codex C's implementation against the contract. Focus on whether the Pyright cleanup in tests/test_evidence_ledger.py preserves evidence-ledger assertion strength, keeps Pyright advisory-only, and avoids touching forbidden parser/runtime/workbook/webhook/App Script/Sheets/AI/production surfaces.

Before reviewing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and identify unrelated or untracked files, especially docs/contracts/analytics_local_developer_app_shell.md.
- Read the contract and implementation handoff.
- Inspect the diff for tests/test_evidence_ledger.py and docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md.
- Do not assume the implementation is correct; review findings first.

Review checks:
- Confirm no runtime source code, Pyright config, CI gate, wrapper, fixture, snapshot, drift baseline, secret, raw log, generated artifact, workbook export, or local-only artifact was changed.
- Confirm no evidence-ledger assertions were weakened, skipped, xfailed, deleted, or replaced with smoke checks.
- Confirm Any/cast usage is limited to dynamic JSON-like ledger boundaries and the intentional invalid-input validator test.
- Confirm tests/test_evidence_ledger.py remains included in Pyright and has zero Pyright diagnostics.
- Confirm repo-wide Pyright findings remain advisory and zero repo-wide findings are not required.

Validation:
git status --short --branch
py -m pytest -q tests\test_evidence_ledger.py
py -m ruff check tests\test_evidence_ledger.py
py tools\run_pyright_advisory_report.py --format json
git diff --check

Also run the file-grouping probe from the contract and verify:
- tests/test_evidence_ledger.py -> 0 diagnostics
- repo-wide residual diagnostics are outside this contract's owned file

If time allows:
py -m pytest -q tests\test_evidence_schema_snapshot.py tests\test_evidence_schema_drift_report.py
@'
tests/test_evidence_ledger.py
docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

Do not:
- edit source behavior
- edit pyrightconfig.json
- edit tools/run_pyright_advisory_report.py or tools/run_pyright_advisory.ps1
- make Pyright required or failing
- require zero repo-wide Pyright findings
- add broad type ignores or Pyright suppressions
- weaken evidence-ledger assertions
- change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior
- target main
- close tracker #136
- stage, commit, push, open a PR, or merge unless explicitly asked

Final report must include:
- role performed
- contract and handoff reviewed
- files reviewed
- findings first, ordered by severity, with file/line references
- validation run and result
- Pyright advisory/no-gate confirmation
- protected-surface status
- secret/private-marker status
- whether forbidden scope was touched
- verdict
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "recommended new child issue under #136"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_pyright_evidence_ledger_tests.md"
  target_artifact: "docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_evidence_ledger.py -> 101 passed"
    - "py -m ruff check tests\\test_evidence_ledger.py -> passed"
    - "py tools\\run_pyright_advisory_report.py --format json -> advisory_findings, helper exit 0"
    - "file grouping probe -> tests/test_evidence_ledger.py 0, repo total 88"
    - "py -m pytest -q tests\\test_evidence_schema_snapshot.py tests\\test_evidence_schema_drift_report.py -> 35 passed"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface gate -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> failed on pre-existing literal marker assertions in tests/test_evidence_ledger.py"
    - "py tools\\check_secret_patterns.py --all -> failed on pre-existing repo findings outside this slice"
  stop_conditions:
    - "Do not make Pyright a required/failing gate."
    - "Do not require zero repo-wide Pyright findings."
    - "Do not weaken evidence-ledger test assertions."
    - "Do not edit source evidence-ledger behavior, Pyright config, report wrappers, CI gates, fixtures, snapshots, or drift baselines."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not target main or close tracker #136."
```
