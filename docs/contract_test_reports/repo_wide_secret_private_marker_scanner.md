# Repo-Wide Secret And Private-Marker Scanner Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/84

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/82

## Contract

`docs/contracts/repo_wide_secret_private_marker_scanner.md`

## Implementation Under Test

Branch: `codex/repo-wide-hardening-run`

Files under review:

- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md`
- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/contract_test_reports/repo_wide_secret_private_marker_scanner.md`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `.gitignore`
- `.github/workflows/repo-checks.yml`
- `.github/pull_request_template.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `tests/fixtures/`

## Findings First

No blocking finding remains after the Codex D fixer pass.

Resolved finding:

- Windows profile usernames containing spaces are now fully redacted in
  `private_local_path` report excerpts.
- `WINDOWS_USER_PATH_RE` now treats spaces as part of the Windows profile
  directory name while still stopping at path separators, colons, quotes,
  brackets, and line boundaries.
- `tests/test_check_secret_patterns.py` now covers a synthetic
  `C:\Users\<redacted>\...` profile path with a multi-token username and proves
  the raw path, full username, and both username fragments are absent from the
  rendered report.

Codex E re-review result:

- Confirmed with focused tests and a synthetic reviewer repro that Windows
  profile usernames containing spaces are fully redacted.
- Confirmed no post-space username fragment leaks in rendered reports.
- Confirmed POSIX private local path redaction remains covered.
- Confirmed scanner modes, warning behavior, and advisory `--all` behavior
  still match the contract.
- Confirmed no protected downstream parser/runtime/workbook/App Script surfaces
  changed.

## Contract-Test Verdict

No blocking findings. Ready for Codex F: Module Submitter.

The previous blocking redaction defect has a focused implementation fix and a
direct regression test. This pass did not broaden scanner behavior beyond the
contracted private-local-path redaction rule.

## Confirmed Matches

- Changed-file mode uses `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`.
- Changed-file mode exits `1` for forbidden findings and `2` for configuration
  errors; warning-only reports remain non-failing.
- `--paths-from-stdin` scans supplied repo-contained paths and reports an error
  for outside-root paths.
- `--all` scans tracked files through `git ls-files` and remains advisory
  because findings return exit code `0`.
- Live-looking webhook URLs are classified as `live_webhook_url` and redacted
  in focused tests.
- Credential assignments, auth headers, passwords, tokens, private key markers,
  and client secrets are classified under `credential_value` when
  non-placeholder.
- Placeholder, fake, dummy, configured, sample, test, redacted, not-real,
  `YOUR_*`, and angle-bracket placeholder contexts are treated as warnings or
  allowed context rather than forbidden live secrets.
- POSIX and Windows private local user paths are forbidden and usernames are
  redacted.
- Windows profile usernames containing spaces are fully redacted.
- Raw Player.log-style markers outside sanitized fixture context are forbidden.
- Sanitized fixture markers under `tests/fixtures/` do not fail by default.
- Failed-post, runtime-status, generated-data, and workbook-export markers have
  stable category IDs.
- Binary, oversized, decode-replacement, unreadable-file, and outside-root
  symlink handling match the contract in focused tests.
- Findings are sorted deterministically.
- Existing protected-surface path gate files are unchanged.
- No CI edits were made.
- No parser behavior, parser state final reconciliation, workbook schema,
  webhook payload shape, Apps Script behavior, parser event classes,
  match/game identity, deduplication, environment semantics, runtime semantics,
  raw logs, generated data, runtime status files, failed posts, workbook
  exports, or protected surfaces outside the contract changed.

## Missing Tests

No blocking test gap remains for the reviewed finding.

Added focused coverage:

- `test_windows_profile_path_with_spaced_username_is_fully_redacted`

Non-blocking context:

- The required `python3 tools/check_secret_patterns.py --base origin/main`
  command currently scans zero paths because the scanner implementation files
  are untracked in this local worktree. The focused tests and
  `--paths-from-stdin` self-scan validate the content behavior directly.

## Drift Classification

- Contract drift: none found.
- Implementation drift: resolved; the Windows spaced-profile redaction mismatch
  is fixed.
- Test drift: resolved; focused regression coverage now exists.
- CI drift: none found; `.github/workflows/repo-checks.yml` was not changed.
- Protected-surface drift: none found.
- Tracker drift: none found; issue #84 and tracker #82 remain open.

## Validation Results

```bash
python3 -m pytest -q tests/test_check_secret_patterns.py
```

Result: `23 passed in 0.03s`

```bash
python3 -m pytest -q tests/test_check_protected_surfaces.py
```

Result: `54 passed in 0.03s`

```bash
printf 'tools/check_secret_patterns.py\ntests/test_check_secret_patterns.py\ndocs/contract_test_reports/repo_wide_secret_private_marker_scanner.md\ndocs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Result: warning-only report, exit `0`, `scanned_paths: 4`,
`forbidden: 0`, `warnings: 13`.

```bash
python3 tools/check_secret_patterns.py --base origin/main
```

Result:

```text
Secret / Private Marker Scan
mode: changed-files
base: origin/main
head: HEAD
scanned_paths: 0
skipped_paths: 0
forbidden: 0
warnings: 0

result: passed
```

```bash
python3 tools/check_protected_surfaces.py --base origin/main
```

Result:

```text
Protected Surface Gate
base: origin/main
head: HEAD
changed_paths: 0
forbidden: 0
warnings: 0

result: passed
```

```bash
python3 -m ruff check src tests tools
```

Result: `All checks passed!`

```bash
git diff --check
```

Result: passed with no output.

```bash
python3 -m pytest -q tests
```

Result: `693 passed in 1.03s`

```bash
python3 tools/check_secret_patterns.py --all
```

Result: advisory all-repo report, exit `0`, `result: failed`,
`scanned_paths: 309`, `forbidden: 304`, `warnings: 273`.

Reviewer repro:

- Built a synthetic Windows profile path in memory with a multi-token username.
- Scanned it through `scan_text()` and rendered the report.
- Checked the rendered report for the raw path, full username, and both
  username fragments.

Result:

```text
contains_full_path= False
contains_full_username= False
contains_first_fragment= False
contains_second_fragment= False
```

## Remaining Non-Blocking Gaps

- No CI run was triggered.
- No live MTGA parser run was executed.
- No live workbook, webhook, or Apps Script integration was inspected.
- No all-repo baseline or allowlist policy was established; `--all` remains
  advisory by contract.
- The changed-file scanner command will become more representative after the
  implementation artifacts are committed, because the current local files are
  untracked.

## Changed/Untracked File Awareness

Current untracked review package:

- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/contract_test_reports/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md`
- `tests/test_check_secret_patterns.py`
- `tools/check_secret_patterns.py`

No tracked protected downstream files were modified in this re-review.

## Next Recommended Role

Codex F: Module Submitter.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/84"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/repo_wide_secret_private_marker_scanner.md"
  target_artifact: "module submitter package for repo-wide secret/private-marker scanner"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  verdict: "No blocking findings. Ready for Codex F: Module Submitter."
  validation:
    - "python3 -m pytest -q tests/test_check_secret_patterns.py -> 23 passed in 0.03s"
    - "python3 -m pytest -q tests/test_check_protected_surfaces.py -> 54 passed in 0.03s"
    - "paths-from-stdin self-scan -> exit 0, forbidden 0, warnings 13"
    - "python3 tools/check_secret_patterns.py --base origin/main -> passed, scanned_paths 0"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed, changed_paths 0"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed with no output"
    - "python3 -m pytest -q tests -> 693 passed in 1.02s"
    - "python3 tools/check_secret_patterns.py --all -> advisory exit 0, result failed, scanned_paths 309, forbidden 304, warnings 273"
    - "reviewer synthetic Windows spaced-username repro -> no raw path, full username, or username fragments in report"
  stop_conditions:
    - "Do not stage, commit, merge, target main, or mark tracker #82 complete."
    - "Do not edit CI unless separately authorized."
    - "Do not change parser/runtime/workbook/App Script behavior."
    - "Do not commit real secret examples, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not print full secret values or private usernames in scanner reports."
```
