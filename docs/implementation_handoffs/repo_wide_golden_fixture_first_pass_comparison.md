# Repo-Wide Golden Fixture First Pass Implementation Handoff

## Issue

Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/94

## Tracker

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

## Contract

Source contract: `docs/contracts/repo_wide_golden_fixture_first_pass.md`

Related policy and ADRs:

- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Worktree

- Branch confirmed: `codex/repo-wide-hardening-run`
- Branch tracks: `origin/codex/repo-wide-hardening-run`
- Tracker #82 confirmed open.
- Child issue #94 confirmed open.
- Initial dirty state: only
  `docs/contracts/repo_wide_golden_fixture_first_pass.md` was untracked and
  treated as the in-scope source contract.
- Unrelated changes: none observed.

## What The First Golden Fixture Pass Is Supposed To Do

This pass establishes the first governed golden fixture acceptance path for one
existing sanitized parser replay fixture. It proves the workflow, not broad
parser correctness.

The contract requires one small path:

- reuse the existing `tests/fixtures/parser_regression_match_slice.log`
- add machine-readable fixture provenance metadata
- add a reduced parser-owned expected output containing only `match_log_row`
  and `game_log_rows`
- add focused test coverage that replays the fixture through the current parser
  regression path and compares the reduced actual output to the reduced
  expected output
- keep parser behavior, fixture input data, the legacy full expected output,
  schema snapshots, workbook/webhook/App Script surfaces, raw logs, generated
  data, runtime artifacts, and production behavior unchanged

## Current Behavior Before This Pass

`tests/test_parser_regressions.py` already replayed two parser regression
fixture pairs through `LineBuffer`, `Router`, parser transforms, and parser
state.

The existing Bo1 pair was:

- input: `tests/fixtures/parser_regression_match_slice.log`
- full legacy expected output:
  `tests/fixtures/parser_regression_match_expected.json`

That full expected output includes parser internals such as router stats,
event traces, parser context, match summary debug output, match rows,
match-log row output, and game-log row output.

The gap was not parser behavior. The gap was governance:

- no golden fixture manifest existed
- no v1 provenance metadata existed for the first selected fixture
- no reduced parser-owned golden expected output existed
- no focused test tied manifest metadata to input fixture, reduced expected
  output, and current parser-owned replay output

## Implementation Produced

Added the first governed fixture manifest:

- `tests/fixtures/golden_fixture_manifest.json`

The manifest has one entry:

- fixture ID: `parser_regression_match_bo1_v1`
- fixture classes:
  - `sanitized_player_log_excerpt`
  - `parser_replay_fixture`
- input path: `tests/fixtures/parser_regression_match_slice.log`
- expected output path:
  `tests/fixtures/parser_regression_match_golden_expected.json`
- expected output kind: `reduced_parser_owned_output`
- source issue, tracker, source contract, policy contract, and related ADRs
- redaction status and redaction categories
- minimum evidence families preserved
- parser surfaces under test
- expected output fields
- evidence-ledger tier notes
- not-applicable evidence-ledger/runtime/deployment fields with reasons
- update approval policy and known limitations

Added the first reduced parser-owned golden expected output:

- `tests/fixtures/parser_regression_match_golden_expected.json`

The reduced expected output contains exactly:

- `match_log_row`
- `game_log_rows`

It intentionally excludes:

- `event_traces`
- `router_stats`
- `context`
- `match_summary_debug`
- `match_summary_row`
- `raw_json`
- raw log lines
- local paths
- webhook URLs
- runtime status payloads
- failed post payloads
- workbook exports
- generated data
- live workbook or deployed Apps Script identifiers

Added focused test coverage in `tests/test_parser_regressions.py`:

- loads `tests/fixtures/golden_fixture_manifest.json`
- finds fixture ID `parser_regression_match_bo1_v1`
- verifies required manifest fields and not-applicable fields are present
- verifies the manifest points to the contracted input and expected output
- verifies evidence-ledger value-source, confidence, finality, and drift flag
  fields are marked `not_applicable`
- verifies the reduced expected output has only `match_log_row` and
  `game_log_rows`
- verifies forbidden internal keys such as `event_traces`, `router_stats`,
  `context`, `match_summary_debug`, `match_summary_row`, and `raw_json` do not
  appear in the reduced expected output
- replays the input fixture through the existing parser regression helper
- reduces actual output to `match_log_row` and `game_log_rows`
- compares reduced actual output to the new reduced expected output

## Files Changed

- `tests/test_parser_regressions.py`
- `tests/fixtures/golden_fixture_manifest.json`
- `tests/fixtures/parser_regression_match_golden_expected.json`
- `docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md`

Also present as the in-scope source artifact:

- `docs/contracts/repo_wide_golden_fixture_first_pass.md`

## Files Intentionally Not Changed

- `tests/fixtures/parser_regression_match_slice.log`
- `tests/fixtures/parser_regression_match_expected.json`
- schema snapshot fixtures
- drift baselines
- parser/runtime source files
- workbook/webhook/App Script files
- sanitizer tooling
- evidence-ledger implementation files
- raw local logs
- generated data
- runtime status files
- failed posts
- workbook exports

## Code Changed

No production/runtime code changed.

## Tests Changed

Test-only change in `tests/test_parser_regressions.py`.

The new test is:

- `test_golden_fixture_manifest_replays_to_reduced_parser_owned_expected_output`

## Fixture Metadata Changed

Added:

- `tests/fixtures/golden_fixture_manifest.json`

Manifest drift interpretation:

- `Fixtures/evidence`: Authorized drift for adding the manifest under issue
  #94 and the source contract.
- `Fixtures/evidence`: No drift for the existing `.log` input because it was
  not modified.
- `Fixtures/evidence`: No drift for the existing full expected output because
  it was not modified.
- `Runtime/parser behavior`: No drift.
- `Parser event shape/classes`: No drift.
- `Workbook/webhook/App Script shape`: No drift.
- `Parser truth ownership`: No drift.

## Reduced Expected Output Changed

Added:

- `tests/fixtures/parser_regression_match_golden_expected.json`

Reduced expected output drift interpretation:

- `Fixtures/evidence`: Authorized drift for adding the reduced expected output
  under issue #94 and the source contract.
- The file is a reviewable test oracle for one selected fixture. It does not
  define parser truth and must not be auto-updated on failure.

## Interface Changes

None.

No function signatures, parser payload fields, parser event classes, event kind
values, match/game identity rules, deduplication rules, sync field names,
runtime family names, runtime `event_type` values, runtime `scope` values,
workbook columns, webhook payloads, Apps Script entrypoints, environment
variables, CI gates, production behavior, live workbook state, or deployed Apps
Script state changed.

## Contract Matches

- The first fixture candidate is exactly
  `tests/fixtures/parser_regression_match_slice.log`.
- No new `.log` fixture was added.
- The existing input fixture was not modified.
- The existing full expected output was not modified.
- A JSON manifest was added at the contracted path.
- The manifest contains one entry for
  `parser_regression_match_bo1_v1`.
- The manifest points to the contracted input fixture and reduced expected
  output fixture.
- The reduced expected output contains only `match_log_row` and
  `game_log_rows`.
- The focused test reuses the existing parser regression replay helper.
- Evidence-ledger value-source, confidence, finality, and drift flag fields are
  explicitly marked `not_applicable`.
- No parser behavior or protected downstream surface changed.

## Contract Mismatches

No contract mismatch requiring production code changes was found.

## Missing Safeguards Or Missing Tests

Still missing by design:

- full golden replay harness from issue #48
- evidence-ledger fixture implementation
- drift-report expected output fixtures
- drift baseline refresh workflow
- sanitizer provenance generation
- fixture manifest coverage for all legacy parser regression fixtures
- proof of sanitizer completeness for the preexisting committed fixture

This pass intentionally covers one first-path fixture only.

## Secret And Private-Marker Status

The final path-scoped secret/private-marker scan over the touched fixture,
test, contract, and handoff paths reported:

- forbidden findings: `0`
- warnings: `7`

Warning interpretation:

- Two warnings are policy/stop-condition references to failed-post payloads in
  the source contract.
- Three warnings are policy/stop-condition references to failed-post or runtime
  status payloads in this handoff.
- Two warnings are required manifest `not_applicable` fields for
  `runtime_status_artifact` and `failed_post_artifact`, both using explicit
  placeholder-not-applicable wording.

No raw local log, secret, live webhook URL, credential, local path, generated
data dump, runtime status payload, failed post payload, or workbook export was
added.

## Protected Surface Status

Path-scoped protected-surface checks over the touched fixture, test, contract,
and handoff paths reported:

- forbidden paths: `0`
- warnings: `0`

No protected runtime or downstream surface was touched.

## Validation Run

Focused and required validation:

```powershell
git status --short --branch
```

Result: branch is `codex/repo-wide-hardening-run`; intended changes are
`tests/test_parser_regressions.py`, the in-scope untracked source contract,
this handoff, `tests/fixtures/golden_fixture_manifest.json`, and
`tests/fixtures/parser_regression_match_golden_expected.json`.

Temporary validation note: `.tmp/issue-94.md` was created only as a local issue
source for `check_surface_authorization.py` and is not part of the intended
repo diff.

```powershell
py -m pytest -q tests\test_parser_regressions.py
```

Result: `3 passed`.

```powershell
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
```

Result: `124 passed, 1 skipped`.

```powershell
py -m ruff check src tests tools
```

Result: `All checks passed!`

```powershell
py -m pyright
```

Result: failed in this shell with resolver/environment findings: missing
imports for `pytest`, `requests`, and `bs4`, followed by a Windows app-execution
alias message. This is the raw Pyright command and matches prior repo-wide
hardening environment noise rather than a fixture-specific regression.

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
```

Result: passed. The repo advisory wrapper resolved the active Python
interpreter and reported `0 errors, 0 warnings, 0 informations`.

```powershell
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
```

Result: passed with `scanned_paths: 0`, `forbidden: 0`, `warnings: 0`. This is
a HEAD-based check; unstaged and untracked local changes are covered by the
path-scoped check below.

```powershell
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
```

Result: passed with `changed_paths: 0`, `forbidden: 0`, `warnings: 0`.

```powershell
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-94.md --authorization-file contract=docs\contracts\repo_wide_golden_fixture_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_golden_fixture_first_pass_comparison.md
```

Result: passed with `changed_paths: 0`, `authorization_status: ok`.

```powershell
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
```

Result: passed with `changed_paths: 0`, `selection_status: ok`, and the
expected zero-diff advisory.

Path-scoped safety and selector checks:

```powershell
@('tests/test_parser_regressions.py','tests/fixtures/golden_fixture_manifest.json','tests/fixtures/parser_regression_match_golden_expected.json','docs/contracts/repo_wide_golden_fixture_first_pass.md','docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md') | py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: warning-only, `forbidden: 0`, `warnings: 7`.

```powershell
@('tests/test_parser_regressions.py','tests/fixtures/golden_fixture_manifest.json','tests/fixtures/parser_regression_match_golden_expected.json','docs/contracts/repo_wide_golden_fixture_first_pass.md','docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md') | py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: passed with `changed_paths: 5`, `forbidden: 0`, `warnings: 0`.

```powershell
@('tests/test_parser_regressions.py','tests/fixtures/golden_fixture_manifest.json','tests/fixtures/parser_regression_match_golden_expected.json','docs/contracts/repo_wide_golden_fixture_first_pass.md','docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md') | py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file issue=.tmp\issue-94.md --authorization-file contract=docs\contracts\repo_wide_golden_fixture_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_golden_fixture_first_pass_comparison.md
```

Result: passed with `changed_paths: 5`, `protected: 0`, `forbidden: 0`,
`authorization_status: ok`.

```powershell
@('tests/test_parser_regressions.py','tests/fixtures/golden_fixture_manifest.json','tests/fixtures/parser_regression_match_golden_expected.json','docs/contracts/repo_wide_golden_fixture_first_pass.md','docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md') | py tools\select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: passed with `changed_paths: 5`, `selection_status: ok`. Required
recommendations included parser regression tests, Ruff, secret/private-marker
scan, protected-surface gate, and `git diff --check`; recommended
`tools/check_agent_docs.py`.

```powershell
py tools\check_agent_docs.py
```

Result: passed with `checked_files: 45`, `errors: 0`, `warnings: 0`.

```powershell
git diff --check
```

Result: passed with no whitespace errors. Git also printed the local line-ending
notice that `tests/test_parser_regressions.py` will be normalized from CRLF to
LF the next time Git touches it.

## Still Unverified

- Codex E contract-test review.
- Full test suite before submitter work.
- CI/PR checks.
- Live workbook state, intentionally out of scope.
- Deployed Apps Script state, intentionally out of scope.
- Evidence-ledger implementation, intentionally out of scope.
- Drift baseline behavior, intentionally out of scope.
- Sanitizer completeness for the preexisting committed fixture.

## Reviewer Focus

Codex E should verify:

- the selected fixture is exactly
  `tests/fixtures/parser_regression_match_slice.log`
- no new `.log` fixture was added
- the existing input fixture content was not changed
- the existing full expected output was not changed
- the manifest contains the contracted required provenance fields
- not-applicable fields have explicit reasons
- the reduced expected output contains only allowed parser-owned output fields
- the focused test fails on missing or mismatched golden metadata/output
- secret/private-marker scan has no forbidden findings
- scanner warnings are expected policy/not-applicable references rather than
  committed private data
- protected-surface checks are clean
- no parser behavior, schema, webhook/App Script behavior, CI gate, secret,
  raw log, generated data, runtime status file, failed post, workbook export,
  live workbook state, deployed Apps Script state, or production behavior
  changed

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for repo-wide hardening issue #94: First sanitized golden fixture implementation pass.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/94

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_golden_fixture_first_pass.md

Implementation handoff:
docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md

Review the diff against the issue, tracker, contract, handoff, and focused tests.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/review.md
- docs/agent_threads/contract_test.md
- docs/contracts/repo_wide_golden_fixture_first_pass.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md
- docs/contract_test_reports/code_hardening_golden_fixture_policy.md
- docs/contracts/player_log_evidence_ledger.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- tests/test_parser_regressions.py
- tests/fixtures/golden_fixture_manifest.json
- tests/fixtures/parser_regression_match_golden_expected.json
- tests/fixtures/parser_regression_match_slice.log
- tests/fixtures/parser_regression_match_expected.json
- tools/check_secret_patterns.py
- tools/check_protected_surfaces.py
- tools/check_surface_authorization.py
- tools/select_validation.py

Lead with findings. Verify:
- the selected fixture is exactly tests/fixtures/parser_regression_match_slice.log
- no new .log fixture was added
- tests/fixtures/parser_regression_match_slice.log was not modified
- tests/fixtures/parser_regression_match_expected.json was not modified
- the manifest contains required provenance fields
- not-applicable fields have explicit reasons
- the reduced expected output contains only match_log_row and game_log_rows
- the focused parser regression test fails on missing or mismatched golden metadata/output
- the secret/private-marker scan has no forbidden findings
- warning-only scanner findings are expected policy/not-applicable references, not private data
- protected-surface checks are clean or explicitly authorized
- parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match identity, game identity, deduplication, sync field names, runtime family names, runtime event_type values, runtime scope values, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, CI gates, production behavior, and main targeting were not changed

Validation to check or rerun:
git status --short --branch
py -m pytest -q tests\test_parser_regressions.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-94.md --authorization-file contract=docs\contracts\repo_wide_golden_fixture_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_golden_fixture_first_pass_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check

Do not edit files in review-only mode. Do not stage, commit, open a PR, merge, close issues, target main, or mark tracker #82 complete.

Produce docs/contract_test_reports/repo_wide_golden_fixture_first_pass.md or a review verdict with findings, validation evidence, fixture drift-budget interpretation, protected-surface status, secret/private-marker status, remaining risks, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/94"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/repo_wide_golden_fixture_first_pass.md"
  implementation_artifact: "docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md"
  target_artifact: "docs/contract_test_reports/repo_wide_golden_fixture_first_pass.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "py -m pytest -q tests\\test_parser_regressions.py -> 3 passed"
    - "py -m pytest -q tests\\test_check_secret_patterns.py tests\\test_check_protected_surfaces.py tests\\test_check_surface_authorization.py tests\\test_select_validation.py -> 124 passed, 1 skipped"
    - "py -m ruff check src tests tools -> All checks passed"
    - "py -m pyright -> failed from raw resolver/environment noise; advisory wrapper passed"
    - "powershell -ExecutionPolicy Bypass -File tools\\run_pyright_advisory.ps1 -> 0 errors, 0 warnings, 0 informations"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run -> passed with changed paths 0"
    - "path-scoped secret/private-marker scan -> warning only, forbidden 0, warnings 7"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run -> passed with changed paths 0"
    - "path-scoped protected-surface gate -> passed, forbidden 0, warnings 0"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\\issue-94.md --authorization-file contract=docs\\contracts\\repo_wide_golden_fixture_first_pass.md --authorization-file handoff=docs\\implementation_handoffs\\repo_wide_golden_fixture_first_pass_comparison.md -> authorization_status ok"
    - "path-scoped surface authorization check -> authorization_status ok"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run -> selection_status ok with zero-diff advisory"
    - "path-scoped validation selector -> selection_status ok"
    - "py tools\\check_agent_docs.py -> passed with checked_files 45, errors 0, warnings 0"
    - "git diff --check -> passed with no whitespace errors; local CRLF-to-LF notice printed"
  stop_conditions:
    - "Do not change parser behavior."
    - "Do not change parser state final reconciliation."
    - "Do not change workbook schema, webhook payload shape, or Apps Script behavior."
    - "Do not change parser event classes, event kind values, parser payload shapes, match identity, game identity, deduplication, sync field names, runtime family names, runtime event_type values, or runtime scope values."
    - "Do not add new .log fixture data."
    - "Do not modify tests/fixtures/parser_regression_match_slice.log."
    - "Do not modify tests/fixtures/parser_regression_match_expected.json."
    - "Do not refresh schema snapshots or add drift baselines."
    - "Do not implement sanitizer tooling or the Player.log evidence ledger."
    - "Do not touch secrets, credentials, environment variables, raw local logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, CI gates, production behavior, or main."
    - "Do not stage, commit, open a PR, close issues, or mark tracker #82 complete unless explicitly asked."
```
