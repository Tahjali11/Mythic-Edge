# Repo-Wide Drift Detector Baseline First Pass Contract-Test Report

## Findings

No blocking findings.

The implementation satisfies the issue #96 contract. The pass stays report-only, reuses the existing sanitized fixture, adds one normalized expected drift-report reference, extends the existing manifest with provenance metadata, and does not change detector/runtime/parser/workbook/webhook/App Script behavior.

Non-blocking validation caveat: raw `py -m pyright` still fails in this local shell because imports such as `pytest`, `bs4`, and `requests` are unresolved by that invocation. The repo-approved Pyright advisory wrapper passed with `0 errors, 0 warnings, 0 informations`, so this is recorded as local resolver noise, not a module blocker.

Non-blocking formatting caveat: `git diff --check` passed with a warning that `tests/test_log_drift_sensor.py` will have CRLF replaced by LF when Git touches it.

## Issue And Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/96
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
- Branch: `codex/repo-wide-hardening-run`
- Contract: `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`
- Implementation handoff: `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`

## Implementation Reviewed

Reviewed changed paths:

- `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`
- `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`
- `tests/test_log_drift_sensor.py`
- `tests/fixtures/golden_fixture_manifest.json`
- `tests/fixtures/player_log_drift_flush_timing_expected.json`

No source, tool, CI, Apps Script, workbook, runtime data, or `.log` fixture path was changed.

## Contract Matches

- Selected input fixture is exactly `tests/fixtures/flush_timing_corpus_slice.log`.
- No new `.log` fixture was added.
- `tests/fixtures/flush_timing_corpus_slice.log` was not changed.
- Expected output path is exactly `tests/fixtures/player_log_drift_flush_timing_expected.json`.
- Expected output is a normalized drift-report reference, not a runtime baseline.
- Expected output excludes `analyzed_at`, `source_path`, report paths, baseline paths, local temp paths, raw log bodies, raw JSON bodies, secrets, webhook URLs, workbook IDs, deployment IDs, runtime artifacts, failed posts, generated data, and workbook exports.
- Manifest entry `player_log_drift_flush_timing_v1` contains required provenance fields, policy links, evidence-tier notes, update policy, limitations, and explicit `not_applicable` reasons.
- Focused test compares current detector output against the committed expected reference and fails if the reference is missing or mismatched.
- Detector behavior and `--refresh-baseline` behavior were not changed.
- No failing CI gate, Pyright gate, runtime baseline, runtime status file, raw log, generated data, failed post, workbook export, live workbook, deployed Apps Script, production behavior, or main targeting was introduced.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocker-level missing tests.

Residual gaps are intentionally out of scope for this first pass:

- CLI behavior and `--refresh-baseline` temporary-file semantics remain covered only by existing focused behavior, not a new committed baseline workflow.
- The request-name-only detector status gap remains a known future issue; this pass records observed behavior without changing detector semantics.
- The expected reference proves one sanitized drift fixture path only, not broad drift detector coverage.

## Validation Results

Commands run:

```powershell
git status --short --branch
py -m pytest -q tests\test_log_drift_sensor.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
py -m ruff check src tests tools
py -m pyright
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-96.md --authorization-file contract=docs\contracts\repo_wide_drift_detector_baseline_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_drift_detector_baseline_first_pass_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
py -m pytest -q
```

Results:

- Branch is `codex/repo-wide-hardening-run` and is even with `origin/codex/repo-wide-hardening-run`.
- `py -m pytest -q tests\test_log_drift_sensor.py` -> `4 passed`.
- Hardening tool tests -> `124 passed, 1 skipped`.
- `py -m pytest -q` -> `761 passed, 1 skipped`.
- `py -m ruff check src tests tools` -> passed.
- Raw `py -m pyright` -> failed from local dependency resolver noise.
- `powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1` -> `0 errors, 0 warnings, 0 informations`.
- Base secret/private-marker scan -> passed with `scanned_paths: 0`.
- Base protected-surface gate -> passed with `changed_paths: 0`.
- Base surface authorization -> passed with `changed_paths: 0`.
- Base validation selector -> `selection_status: ok` with expected `zero_changed_paths` advisory.
- `git diff --check` -> passed with CRLF warning only.
- `py tools\check_agent_docs.py` -> passed.

Because several intended files are untracked, path-scoped validation was also run over the five implementation paths:

- Path-scoped secret/private-marker scan -> `forbidden: 0`, `warnings: 8`.
- Path-scoped protected-surface gate -> passed, `forbidden: 0`, `warnings: 0`.
- Path-scoped surface authorization -> `authorization_status: ok`.
- Path-scoped validation selector -> `selection_status: ok`; required commands included diff check, protected-surface gate, Ruff, secret/private-marker scan, and `tests/test_log_drift_sensor.py`.

The temporary `.tmp\issue-96.md` authorization helper was created only for the requested surface-authorization run and removed afterward.

Post-report artifact checks:

- `git diff --check` -> passed with CRLF warning only.
- Report-only secret/private-marker scan -> warning-only, `forbidden: 0`, for a stop-condition reference to failed posts.
- Report-only protected-surface gate -> passed, `forbidden: 0`, `warnings: 0`.
- `py tools\check_agent_docs.py` -> passed.

## Secret And Private-Marker Status

No forbidden findings.

The eight path-scoped warnings were expected textual artifact references:

- policy text references to runtime status and failed-post categories in the contract/handoff
- manifest `not_applicable` placeholders for runtime status and failed-post artifacts

These are not private data, raw log bodies, secrets, webhook URLs, workbook IDs, deployment IDs, generated data, runtime artifacts, failed posts, or workbook exports.

## Protected-Surface Status

Protected-surface status is clean.

Path-scoped protected-surface gate reported:

- `changed_paths: 5`
- `forbidden: 0`
- `warnings: 0`

Path-scoped surface authorization reported all five implementation paths as `NOT_PROTECTED allowed` and `authorization_status: ok`.

## Forbidden Scope Status

Forbidden scope was not touched.

Confirmed not changed:

- detector runtime behavior
- `--refresh-baseline` behavior
- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- CI gate behavior
- Pyright gate behavior
- runtime status files
- raw logs and `.log` fixtures
- generated data
- failed posts
- workbook exports
- live workbook state
- deployed Apps Script state
- production behavior
- main target

## Remaining Risks

- GitHub Actions have not run for this unsubmitted package.
- Raw `py -m pyright` remains noisy in this local shell; the advisory wrapper is the reliable repo-approved signal.
- The normalized expected report locks one detector fixture/reference only and does not prove broad drift coverage.
- The request-name-only status gap and `--refresh-baseline` workflow remain future follow-up areas, as the contract intended.

## Recommendation

Approve for Codex F / Module Submitter.

Codex F should stage only the reviewed issue #96 paths, commit, push, and open or update a draft PR targeting `codex/repo-wide-hardening-run`, not `main`.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for repo-wide hardening issue #96.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/96

Branch:
codex/repo-wide-hardening-run

Reviewed artifacts:
- docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
- docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md
- docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md

Reviewed implementation files:
- tests/test_log_drift_sensor.py
- tests/fixtures/golden_fixture_manifest.json
- tests/fixtures/player_log_drift_flush_timing_expected.json

Submit only the reviewed issue #96 package. Do not stage unrelated files. Do not stage `.tmp` helper files. Do not target main. Do not close issue #96 or mark tracker #82 complete unless explicitly instructed.

Before committing, confirm:
- no `.log` fixture changed or was added
- no runtime baseline, runtime status file, raw log, generated data, failed post, workbook export, live workbook, deployed Apps Script, source behavior, CI gate, or Pyright gate changed
- validation remains green or any limitations are recorded

Open or update a draft PR targeting codex/repo-wide-hardening-run.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/96"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/repo_wide_drift_detector_baseline_first_pass.md"
  reviewed_handoff: "docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md"
  target_artifact: "draft PR targeting codex/repo-wide-hardening-run"
  review_artifact: "docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  findings:
    - "No blocking findings."
    - "Raw pyright command has local resolver noise; Pyright advisory wrapper passed cleanly."
  validation:
    - "py -m pytest -q tests\\test_log_drift_sensor.py -> 4 passed"
    - "hardening tool tests -> 124 passed, 1 skipped"
    - "py -m pytest -q -> 761 passed, 1 skipped"
    - "py -m ruff check src tests tools -> passed"
    - "powershell -ExecutionPolicy Bypass -File tools\\run_pyright_advisory.ps1 -> 0 errors, 0 warnings, 0 informations"
    - "path-scoped secret/private-marker scan -> warning-only, forbidden 0"
    - "path-scoped protected-surface gate -> passed, forbidden 0, warnings 0"
    - "path-scoped surface authorization -> ok"
    - "path-scoped validation selector -> ok"
    - "git diff --check -> passed with CRLF warning only"
  residual_risk:
    - "GitHub Actions not run."
    - "Raw pyright invocation remains noisy in this local shell."
    - "Only one normalized drift-report reference is covered."
  stop_conditions:
    - "Do not target main."
    - "Do not close issue #96 or mark tracker #82 complete unless explicitly instructed."
    - "Do not stage unrelated files or temporary .tmp helper files."
    - "Do not change detector behavior, --refresh-baseline behavior, parser behavior, workbook schema, webhook payload shape, Apps Script behavior, CI gates, Pyright gates, runtime artifacts, raw logs, generated data, failed posts, workbook exports, live workbook state, deployed Apps Script state, or production behavior."
```
