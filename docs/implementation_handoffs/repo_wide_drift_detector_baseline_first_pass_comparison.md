# Repo-Wide Drift Detector Baseline First Pass Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/96

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/82

## Contract

`docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`

Related policy artifacts:

- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md`
- `docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/repo_wide_golden_fixture_first_pass.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed before editing:

- `codex/repo-wide-hardening-run`

Initial status:

```text
## codex/repo-wide-hardening-run...origin/codex/repo-wide-hardening-run
?? docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
```

The untracked contract was the source artifact for issue #96 and was treated as in scope.

Final status after validation and removal of the temporary `.tmp\issue-96.md` helper:

```text
## codex/repo-wide-hardening-run...origin/codex/repo-wide-hardening-run
 M tests/fixtures/golden_fixture_manifest.json
 M tests/test_log_drift_sensor.py
?? docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
?? docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md
?? tests/fixtures/player_log_drift_flush_timing_expected.json
```

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md`
- `docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/repo_wide_golden_fixture_first_pass.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `audit_player_log_drift.py`
- `tests/test_log_drift_sensor.py`
- `tests/fixtures/flush_timing_corpus_slice.log`
- `tests/fixtures/golden_fixture_manifest.json`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `tools/check_surface_authorization.py`
- `tests/test_check_surface_authorization.py`
- `tools/select_validation.py`
- `tests/test_select_validation.py`

## Current Behavior Compared To Contract

The current drift sensor already builds a report with `object`, `status`, `analyzed_at`, `source_path`, `entry_counts`, `headers`, `routed_event_kinds`, unmatched/unknown top lists, and `baseline_delta`.

The existing focused tests already strip comment lines from `tests/fixtures/flush_timing_corpus_slice.log`, write a temporary `Player.log`, and call the drift sensor against that temporary file.

The current gap was not detector behavior. The gap was that the repo did not yet have a governed, manifest-linked, normalized expected output for one report-only drift reference.

## What Changed

Implemented the smallest local fixture/test reference path authorized by the contract:

- Extended `tests/fixtures/golden_fixture_manifest.json` with one `player_log_drift_flush_timing_v1` fixture entry.
- Added `tests/fixtures/player_log_drift_flush_timing_expected.json` as a normalized report reference.
- Added one focused test in `tests/test_log_drift_sensor.py` that loads the manifest, verifies the drift fixture metadata, rebuilds the normalized drift report from the existing fixture through a temporary `Player.log`, checks volatile/local fields are absent from the expected reference, and compares actual to expected.
- Produced this implementation handoff.

## Files Changed

- `tests/fixtures/golden_fixture_manifest.json`
- `tests/fixtures/player_log_drift_flush_timing_expected.json`
- `tests/test_log_drift_sensor.py`
- `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`

Also present as an untracked source artifact before this implementation pass:

- `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`

## Code Changed

No production parser, detector, CLI, runtime, workbook, webhook, or Apps Script code changed.

Test code changed in `tests/test_log_drift_sensor.py`.

## Tests Added Or Updated

Updated `tests/test_log_drift_sensor.py`:

- Added manifest loading for `player_log_drift_flush_timing_v1`.
- Added normalized drift report construction from `build_player_log_drift_report(..., baseline_payload={})`.
- Added comparison against `tests/fixtures/player_log_drift_flush_timing_expected.json`.
- Added checks that the committed expected reference excludes `analyzed_at`, `source_path`, `report_path`, and `baseline_path`.
- Added checks that the committed expected reference does not include a Windows absolute path marker, local `Users` path marker, or `Player.log` marker.

## Fixture Candidate Selected

Selected input fixture:

- `tests/fixtures/flush_timing_corpus_slice.log`

No new `.log` fixture was added. The existing `.log` fixture was not edited.

## Manifest Fields Added

The new manifest entry includes:

- `fixture_id`: `player_log_drift_flush_timing_v1`
- `fixture_classes`: `sanitized_player_log_excerpt`, `drift_report_expected_output`, `report_only_reference`
- `input_path`: `tests/fixtures/flush_timing_corpus_slice.log`
- `expected_output_path`: `tests/fixtures/player_log_drift_flush_timing_expected.json`
- `expected_output_kind`: `normalized_drift_report_reference`
- issue, tracker, contract, policy-contract, and ADR provenance
- redaction, evidence-preservation, parser-surface, expected-output-field, tier, invariant, update-policy, limitation, and not-applicable metadata

## Normalized Expected Output Fields Added

`tests/fixtures/player_log_drift_flush_timing_expected.json` includes only these detector-produced report fields under `normalized_report`:

- `object`
- `status`
- `entry_counts`
- `headers`
- `routed_event_kinds`
- `top_unknown_signatures`
- `top_unmatched_api_names`
- `top_unmatched_request_api_names`
- `baseline_delta`

It excludes:

- `analyzed_at`
- `source_path`
- `report_path`
- `baseline_path`
- local temporary paths
- runtime status paths
- raw log bodies
- raw JSON bodies
- secrets, webhook URLs, workbook IDs, deployment IDs, failed posts, generated data, and workbook exports

## Contract Matches

- Reuses `tests/fixtures/flush_timing_corpus_slice.log` as the only first-pass input fixture.
- Adds no `.log` fixture and does not edit the existing `.log` fixture.
- Uses the existing comment-stripping test-input behavior.
- Calls `build_player_log_drift_report()` with an empty in-memory baseline.
- Adds a committed normalized drift-report reference rather than a runtime drift baseline.
- Adds manifest provenance and update-policy metadata for the drift reference.
- Keeps the reference report-only and does not add a live drift gate.
- Preserves the documented request-name-only status gap as out of scope.
- Preserves parser truth ownership and downstream workbook/webhook/App Script boundaries.

## Contract Mismatches

No implementation mismatch was found that required changing detector behavior.

The only pre-existing mismatch was missing coverage/artifact support: no manifest-backed normalized drift-report expected output existed before this pass.

## Missing Safeguards Or Missing Tests

Addressed in this pass:

- Missing manifest metadata for the drift fixture.
- Missing committed normalized report expected output.
- Missing focused test comparing current detector output to the committed report reference.
- Missing focused test assertion that the committed report reference excludes volatile/local detector fields.

Still intentionally missing:

- CLI output coverage.
- Temporary-file `--refresh-baseline` behavior coverage.
- Missing or malformed baseline payload reference coverage.
- Broad drift fixture coverage.
- Evidence-ledger Tier 6 mapping from drift findings to affected parser-managed outputs.
- Request-name-only status semantics resolution.

## Fixture/Evidence Drift-Budget Interpretation

This pass creates authorized fixture/reference drift:

- `tests/fixtures/golden_fixture_manifest.json` gains one issue #96 entry.
- `tests/fixtures/player_log_drift_flush_timing_expected.json` is a new normalized expected-output reference.

It does not create parser behavior drift, detector behavior drift, workbook/schema drift, webhook payload drift, Apps Script drift, runtime baseline drift, or production drift.

## Report-Only No-Gate Confirmation

This pass does not:

- create or refresh a runtime drift baseline
- commit a runtime drift report
- call `write_player_log_drift_report()` for the new expected reference
- use `--refresh-baseline`
- add a failing live drift CI gate
- change detector status semantics or report shape

## Secret/Private-Marker Status

Broad changed-file scan:

- `py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run`
- Result: passed, but scanned `0` paths because current changes include untracked files and unstaged edits not visible to the base/head changed-file mode.

Path-scoped scan over the contract, handoff, manifest, expected output, and focused test:

- Result: warning, with `0` forbidden findings and `8` artifact-path-reference warnings.
- Warnings were textual policy/not-applicable references to runtime status and failed-post artifact categories in the contract, handoff, and manifest. No secret, credential, webhook URL, workbook ID, deployment ID, raw private log, or generated-data finding was reported.

## Protected-Surface Status

Broad changed-file scan:

- `py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run`
- Result: passed, but scanned `0` changed paths for the same untracked/unstaged reason.

Path-scoped scan over the contract, handoff, manifest, expected output, and focused test:

- Result: passed, `forbidden: 0`, `warnings: 0`.

## Surface-Authorization Status

Broad changed-file scan:

- `py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-96.md --authorization-file contract=docs\contracts\repo_wide_drift_detector_baseline_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_drift_detector_baseline_first_pass_comparison.md`
- Result: `authorization_status: ok`, but scanned `0` changed paths.

Path-scoped scan over the contract, handoff, manifest, expected output, and focused test:

- Result: `authorization_status: ok`.
- All five paths were reported as `NOT_PROTECTED allowed`.
- Temporary `.tmp\issue-96.md` was created for this validation command and removed afterward so it would not remain as a local artifact.

## Validation-Selector Status

Broad changed-file selector:

- `py tools\select_validation.py --base origin/codex/repo-wide-hardening-run`
- Result: `selection_status: ok`, with advisory `zero_changed_paths`.

Path-scoped selector over the contract, handoff, manifest, expected output, and focused test:

- Result: `selection_status: ok`.
- Required commands selected: `git diff --check`, protected-surface gate, Ruff, secret/private-marker scan, and `tests/test_log_drift_sensor.py`.
- Recommended command selected: `py tools\check_agent_docs.py`.

## Validation Run

Pre-edit focused validation:

```text
py -m pytest -q tests\test_log_drift_sensor.py
...                                                                      [100%]
3 passed in 0.60s
```

Post-edit focused validation:

```text
py -m pytest -q tests\test_log_drift_sensor.py
....                                                                     [100%]
4 passed in 0.47s
```

Additional validation:

```text
git status --short --branch
## codex/repo-wide-hardening-run...origin/codex/repo-wide-hardening-run
 M tests/fixtures/golden_fixture_manifest.json
 M tests/test_log_drift_sensor.py
?? .tmp/
?? docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
?? docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md
?? tests/fixtures/player_log_drift_flush_timing_expected.json
```

Note: `.tmp/` contained only the temporary issue authorization note used for surface-authorization validation. It was removed after the command ran.

```text
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
124 passed, 1 skipped in 1.14s
```

```text
py -m ruff check src tests tools
All checks passed!
```

```text
py -m pyright
19 errors, 5 warnings, 0 informations
```

Raw Pyright failed due environment/import resolution in this shell: `pytest`, `requests`, and `bs4` could not be resolved, and the command ended with the Windows Store `python` alias message. This appears to be the existing raw-Pyright resolver issue rather than an issue #96 code change failure.

Repo advisory wrapper:

```text
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
Running Pyright advisory check with local Python 3.13 interpreter
0 errors, 0 warnings, 0 informations
```

```text
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
result: passed
```

The broad secret/private-marker scan reported `scanned_paths: 0`. Path-scoped scan over touched paths reported `forbidden: 0`, `warnings: 8`, with warnings limited to textual artifact category references.

```text
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
result: passed
```

The broad protected-surface scan reported `changed_paths: 0`. Path-scoped scan over touched paths passed with `forbidden: 0`, `warnings: 0`.

```text
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-96.md --authorization-file contract=docs\contracts\repo_wide_drift_detector_baseline_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_drift_detector_baseline_first_pass_comparison.md
authorization_status: ok
```

The broad surface-authorization scan reported `changed_paths: 0`. Path-scoped authorization over touched paths also returned `authorization_status: ok`.

```text
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
selection_status: ok
```

The broad selector reported advisory `zero_changed_paths`. Path-scoped selector returned `selection_status: ok` and selected the expected required/recommended commands.

```text
py tools\check_agent_docs.py
result: passed
```

```text
git diff --check
```

Result: exit code `0`. Git printed a line-ending warning for `tests/test_log_drift_sensor.py`:

```text
warning: in the working copy of 'tests/test_log_drift_sensor.py', CRLF will be replaced by LF the next time Git touches it
```

## Still Unverified

Still out of scope:

- live local `Player.log` drift
- runtime baseline refresh policy
- workbook state
- deployed Apps Script state
- production behavior
- evidence-ledger implementation behavior

## Forbidden Scope Touched

No forbidden runtime/parser/workbook/webhook/App Script/deployment surface was intentionally touched.

No raw local logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, CI gates, production behavior, or `main` target were touched.

## Reviewer Focus

Codex E should verify:

- the selected input fixture remains exactly `tests/fixtures/flush_timing_corpus_slice.log`
- no new `.log` input fixture was added
- `tests/fixtures/flush_timing_corpus_slice.log` was not edited
- the expected reference excludes volatile/local fields and is not a runtime baseline
- the manifest entry contains all required provenance and not-applicable fields
- the focused test fails if the expected reference is missing or mismatched
- detector behavior and `--refresh-baseline` behavior were not changed
- protected-surface and secret/private-marker scans are clean or explicitly authorized

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for repo-wide hardening issue #96: Drift detector baseline first pass.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/96

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_drift_detector_baseline_first_pass.md

Implementation handoff:
docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md

Expected review artifact:
docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md

Review the implementation against the contract and handoff. Lead with findings. Verify that the selected input fixture is exactly tests/fixtures/flush_timing_corpus_slice.log, no new .log fixture was added, the existing .log fixture was not changed, the expected output is exactly tests/fixtures/player_log_drift_flush_timing_expected.json, and the expected output is a normalized report reference rather than a runtime baseline.

Confirm that the expected output excludes analyzed_at, source_path, report paths, baseline paths, local temp paths, raw log bodies, raw JSON bodies, secrets, webhook URLs, workbook IDs, deployment IDs, runtime artifacts, failed posts, generated data, and workbook exports.

Confirm that the manifest entry for player_log_drift_flush_timing_v1 contains required provenance and not-applicable fields, the focused test compares current detector output to the committed expected reference, and no detector behavior, --refresh-baseline behavior, parser behavior, workbook schema, webhook payload shape, Apps Script behavior, CI gate behavior, Pyright gate behavior, runtime status files, raw logs, generated data, failed posts, workbook exports, live workbook state, deployed Apps Script state, production behavior, or main target was changed.

Run or review:
git status --short --branch
py -m pytest -q tests\test_log_drift_sensor.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-96.md --authorization-file contract=docs\contracts\repo_wide_drift_detector_baseline_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_drift_detector_baseline_first_pass_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check

If .tmp\issue-96.md is absent locally, recreate a temporary authorization note from issue #96 before running the surface-authorization command, then remove it afterward unless the user asks to keep local helper files.

Produce docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md with findings, validation, remaining risks, and next recommended role. Do not stage, commit, open a PR, close issues, mark tracker #82 complete, target main, or change runtime/parser/workbook/webhook/App Script behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/96"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/repo_wide_drift_detector_baseline_first_pass.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md"
  expected_review_artifact: "docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "py -m pytest -q tests\\test_log_drift_sensor.py -> passed, 4 passed"
    - "py -m pytest -q tests\\test_check_secret_patterns.py tests\\test_check_protected_surfaces.py tests\\test_check_surface_authorization.py tests\\test_select_validation.py -> passed, 124 passed, 1 skipped"
    - "py -m ruff check src tests tools -> passed"
    - "py -m pyright -> failed due existing shell resolver/import issue, 19 errors and 5 warnings for missing pytest/requests/bs4 plus Windows Store python alias message"
    - "powershell -ExecutionPolicy Bypass -File tools\\run_pyright_advisory.ps1 -> passed, 0 errors, 0 warnings"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run -> passed, scanned 0 changed paths"
    - "path-scoped secret/private-marker scan over touched paths -> warning, 0 forbidden, 8 textual artifact-reference warnings"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run -> passed, scanned 0 changed paths"
    - "path-scoped protected-surface gate over touched paths -> passed, 0 forbidden, 0 warnings"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\\issue-96.md --authorization-file contract=docs\\contracts\\repo_wide_drift_detector_baseline_first_pass.md --authorization-file handoff=docs\\implementation_handoffs\\repo_wide_drift_detector_baseline_first_pass_comparison.md -> ok, scanned 0 changed paths"
    - "path-scoped surface authorization over touched paths -> ok, all paths NOT_PROTECTED allowed"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run -> ok, zero_changed_paths advisory"
    - "path-scoped validation selector over touched paths -> ok"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> exit 0 with CRLF warning for tests/test_log_drift_sensor.py"
  stop_conditions:
    - "Do not change src/mythic_edge_parser/app/log_drift_sensor.py."
    - "Do not change audit_player_log_drift.py."
    - "Do not change detector behavior, detector status semantics, detector report shape, or --refresh-baseline behavior."
    - "Do not generate, refresh, or commit drift baselines."
    - "Do not commit runtime drift reports."
    - "Do not add a failing live drift CI gate."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match identity, game identity, deduplication, sync field names, runtime family names, runtime event_type values, or runtime scope values."
    - "Do not add new .log fixture data or modify tests/fixtures/flush_timing_corpus_slice.log."
    - "Do not refresh schema snapshots or modify unrelated parser expected outputs."
    - "Do not implement sanitizer tooling or the Player.log evidence ledger."
    - "Do not touch secrets, credentials, environment variables, raw local logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, Pyright gate behavior, production behavior, or main."
    - "Do not stage, commit, open a PR, close issues, or mark tracker #82 complete unless explicitly asked."
```
