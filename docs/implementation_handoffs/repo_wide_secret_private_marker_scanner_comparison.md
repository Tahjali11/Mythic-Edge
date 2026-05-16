# Repo-Wide Secret And Private-Marker Scanner Implementation Handoff

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/84

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Contract: `docs/contracts/repo_wide_secret_private_marker_scanner.md`

Role performed: Codex C: Module Implementer; Codex D: Module Fixer follow-up

Branch: `codex/repo-wide-hardening-run`

Risk tier: Medium

## Summary Of Implementation Comparison

Current repo state before this pass had a protected-surface path gate but no
content scanner:

- `tools/check_protected_surfaces.py` existed and remained unchanged.
- `tests/test_check_protected_surfaces.py` existed and remained unchanged.
- `tools/check_secret_patterns.py` did not exist.
- `tests/test_check_secret_patterns.py` did not exist.
- `docs/contract_test_reports/repo_wide_hardening_baseline.md` and
  `docs/contracts/repo_wide_secret_private_marker_scanner.md` were already
  present as untracked source artifacts in this worktree.

This pass implemented the smallest deterministic local scanner needed by the
contract and added focused scanner tests. No parser/runtime/workbook/App Script
behavior was changed.

Codex D follow-up resolved the reviewer-blocking Windows profile redaction
finding. Windows profile usernames containing spaces are now redacted as a full
profile directory name instead of leaving the post-space fragment visible.

## Findings

No blocking contract ambiguity was found.

Contract mismatch fixed:

- Missing scanner implementation: added `tools/check_secret_patterns.py`.
- Missing scanner focused tests: added `tests/test_check_secret_patterns.py`.
- Missing implementation handoff: added this document.
- Reviewer-blocking Windows spaced-profile redaction mismatch: updated
  `WINDOWS_USER_PATH_RE` and added focused regression coverage.

Remaining non-blocking nuance:

- The scanner command `python3 tools/check_secret_patterns.py --base origin/main`
  reports zero changed paths while these files are uncommitted/untracked,
  because the contract explicitly uses `git diff --name-only --diff-filter=ACMRTUXB
  <base>...HEAD`. Focused tests and the `--paths-from-stdin` seam validate the
  content behavior directly.

## Changes Made

Implemented `tools/check_secret_patterns.py`:

- CLI modes:
  - changed-file mode with `--base <git-ref>`
  - `--paths-from-stdin` test/local seam
  - `--all` tracked-file advisory mode
- Git changed-file collection:
  - uses `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`
  - normalizes, deduplicates, sorts, and repo-constrains paths
- All-repo advisory collection:
  - uses `git ls-files`
  - keeps findings report-only/non-failing unless configuration errors occur
- Finding categories:
  - `live_webhook_url`
  - `credential_value`
  - `private_local_path`
  - `raw_player_log_content`
  - `failed_post_payload`
  - `runtime_status_payload`
  - `generated_data_dump`
  - `workbook_export_marker`
  - warning categories required by the contract, including binary, oversized,
    decode-replacement, placeholder, artifact-path, sanitized-fixture, and
    ambiguous-private markers
- Redaction:
  - report rendering stores and prints only redacted excerpts
  - webhook URLs, credential values, auth headers, private usernames,
    spreadsheet IDs, workbook markers, and raw private snippets are not printed
    in full
  - Windows profile usernames containing spaces are redacted as a single
    profile directory in `private_local_path` excerpts
- File handling:
  - binary files warn as skipped
  - oversized text files warn as skipped
  - UTF-8 replacement decoding warns but still scans
  - unreadable files and outside-root symlinks return configuration errors

Added `tests/test_check_secret_patterns.py`:

- CLI usage and git error behavior
- contract diff command construction
- path normalization, sorting, deduplication, and repo-root containment
- stdin scan seam
- all-repo advisory non-failing behavior
- live-looking webhook, credential, private path, raw Player.log, artifact
  payload, runtime status, generated data, and workbook marker categories
- placeholder and sanitized fixture warning behavior
- redaction assertions proving synthetic forbidden values are absent from
  rendered reports
- focused Windows profile path coverage proving a multi-token username and its
  fragments are absent from rendered reports
- binary, oversized, decode-replacement, unreadable-file, and outside-root
  symlink handling
- deterministic finding ordering

## Confirmed Matches

- Changed-file mode is the only failing mode for forbidden findings.
- `--all` returns exit code `0` for findings and remains advisory/report-only.
- Warnings do not fail.
- Configuration errors return exit code `2`.
- Reports use the contracted header shape:
  - `Secret / Private Marker Scan`
  - `mode`
  - `base`
  - `head`
  - `scanned_paths`
  - `skipped_paths`
  - `forbidden`
  - `warnings`
  - sorted `FORBIDDEN` and `WARNING` finding lines
  - final `result`
- Findings are sorted by severity, path, line, category, and reason.
- Full forbidden values used by tests are not present in rendered reports.
- Windows private profile paths with spaces in the profile name do not expose
  residual username fragments in rendered reports.
- Sanitized fixture markers under `tests/fixtures/` do not fail by default.
- Existing protected-surface path gate is preserved unchanged.

## Missing Safeguards

No required safeguard remains knowingly missing in the implemented scanner.

Future hardening may still add:

- a repo-wide baseline/allowlist policy for all-repo advisory findings
- JSON or GitHub annotation output
- CI integration after reviewer confidence in local signal quality
- fixture manifest/provenance metadata from the golden fixture policy

Those are outside this first implementation contract unless a future issue
authorizes them.

## CI Integration Decision

Deferred.

The contract allows but does not require CI integration. This pass intentionally
did not edit `.github/workflows/repo-checks.yml` so the first scanner rollout
can be reviewed locally before becoming a PR gate.

Reviewer/local command:

```bash
python3 tools/check_secret_patterns.py --base origin/main
```

If a future PR wires this into CI, the contract requires pull-request-only
execution using:

```powershell
py tools\check_secret_patterns.py --base origin/${{ github.base_ref }}
```

with checkout `fetch-depth: 0`, non-failing warnings, and no failing `--all`
mode.

## Validation Evidence

Passed:

```bash
python3 -m pytest -q tests/test_check_secret_patterns.py
```

```text
23 passed in 0.03s
```

Passed:

```bash
python3 -m pytest -q tests/test_check_protected_surfaces.py
```

```text
54 passed in 0.03s
```

Passed with warning-only scanner report:

```bash
printf 'tools/check_secret_patterns.py\ntests/test_check_secret_patterns.py\ndocs/contract_test_reports/repo_wide_secret_private_marker_scanner.md\ndocs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

```text
exit 0; forbidden 0; warnings 13
```

Passed:

```bash
python3 tools/check_secret_patterns.py --base origin/main
```

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

Passed:

```bash
python3 tools/check_protected_surfaces.py --base origin/main
```

```text
Protected Surface Gate
base: origin/main
head: HEAD
changed_paths: 0
forbidden: 0
warnings: 0

result: passed
```

Passed:

```bash
python3 -m ruff check src tests tools
```

```text
All checks passed!
```

Passed:

```bash
git diff --check
```

```text
<no output>
```

Passed:

```bash
python3 -m pytest -q tests
```

```text
693 passed in 1.03s
```

Advisory mode remains non-failing:

```bash
python3 tools/check_secret_patterns.py --all
```

```text
exit 0; result: failed; scanned_paths: 309; forbidden: 304; warnings: 273
```

## Open Risks

- Regex choices are intentionally conservative but still need reviewer
  contract-testing for false positives and false negatives.
- All-repo advisory mode may surface legacy policy text or known workbook/App
  Script references. This is expected until a future baseline/allowlist issue.
- Fixture sanitization remains policy-driven because existing fixtures do not
  yet have machine-readable provenance metadata.
- The changed-file validation command will only scan committed `HEAD` diffs
  under the current contract; uncommitted work must be covered by tests or
  `--paths-from-stdin` until a future contract authorizes working-tree mode.

## Still-Unverified Layers

- No live MTGA parser run was executed.
- No live workbook, webhook, or Apps Script integration was inspected.
- No CI run was triggered.
- No all-repo baseline/allowlist was established.
- No tracker #82 completion action was taken.

## Protected Surfaces

Not changed:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- match identity
- game identity
- deduplication
- secrets or environment variable semantics
- runtime semantics
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports
- existing protected-surface path gate behavior

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer in contract-test mode.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer in contract-test mode for issue #84:
https://github.com/Tahjali11/Mythic-Edge/issues/84

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch:
codex/repo-wide-hardening-run

Use:
- docs/contracts/repo_wide_secret_private_marker_scanner.md
- docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md
- docs/contract_test_reports/repo_wide_hardening_baseline.md
- tools/check_secret_patterns.py
- tests/test_check_secret_patterns.py
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- .gitignore
- .github/workflows/repo-checks.yml
- .github/pull_request_template.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/contracts/code_hardening_protected_surface_gate.md
- tests/fixtures/

Goal:
Verify the Module Implementer scanner and Codex D redaction fix against the
secret/private-marker scanner contract.

Confirm:
- changed-file mode uses git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD
- changed-file mode fails only for forbidden findings or configuration errors
- --paths-from-stdin scans supplied repo-contained paths and errors on outside-root paths
- --all scans tracked files only and remains advisory/non-failing for findings
- live-looking webhook URLs are forbidden and redacted
- credential assignments, auth headers, passwords, tokens, private key markers, and client secrets are forbidden when non-placeholder and redacted
- placeholder, fake, dummy, configured, sample, test, redacted, not-real, YOUR_*, and angle-bracket placeholders do not become forbidden live secrets
- private local user paths are forbidden and usernames are redacted
- Windows profile usernames containing spaces are fully redacted without leaking post-space fragments
- raw Player.log-style markers outside sanitized fixture context are forbidden
- sanitized fixture markers under tests/fixtures/ do not fail by default
- failed-post, runtime-status, generated-data, and workbook-export markers classify with stable categories
- binary, oversized, decode-replacement, unreadable, and outside-root symlink behavior matches the contract
- reports never print full sensitive values used by tests
- findings are sorted deterministically
- existing protected-surface path gate is unchanged
- no parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, runtime semantics, raw logs, generated data, runtime status files, failed posts, workbook exports, or protected surfaces outside the contract changed

Validation:
Run:
python3 -m pytest -q tests/test_check_secret_patterns.py
python3 -m pytest -q tests/test_check_protected_surfaces.py
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main
python3 -m ruff check src tests tools
git diff --check

If feasible, also run:
python3 -m pytest -q tests
python3 tools/check_secret_patterns.py --all

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not stage, commit, merge, target main, mark tracker #82 complete, edit CI, or change parser/runtime/workbook/App Script behavior during review.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/84"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/repo_wide_secret_private_marker_scanner.md"
  target_artifact: "Codex E contract-test re-review for repo-wide secret/private-marker scanner"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  verdict: "Fixer pass complete: Windows profile usernames containing spaces are fully redacted and covered by focused regression test."
  validation:
    - "python3 -m pytest -q tests/test_check_secret_patterns.py -> 23 passed in 0.03s"
    - "python3 -m pytest -q tests/test_check_protected_surfaces.py -> 54 passed in 0.03s"
    - "paths-from-stdin self-scan -> exit 0, forbidden 0, warnings 13"
    - "python3 tools/check_secret_patterns.py --base origin/main -> passed, scanned_paths 0"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed, changed_paths 0"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed with no output"
    - "python3 -m pytest -q tests -> 693 passed in 1.03s"
    - "python3 tools/check_secret_patterns.py --all -> advisory exit 0, result failed, scanned_paths 309, forbidden 304, warnings 273"
  stop_conditions:
    - "Do not commit real secret examples, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not print full secret values in scanner reports."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, runtime semantics, or protected surfaces outside this contract."
    - "Do not add network calls or third-party secret scanning services."
    - "Do not make all-repo mode or warnings fail CI."
    - "Do not target main directly."
    - "Do not mark tracker #82 complete."
```
