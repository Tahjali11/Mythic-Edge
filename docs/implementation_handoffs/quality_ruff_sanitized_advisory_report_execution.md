# Quality Ruff Sanitized Advisory Report Execution Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/588

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Project Roadmap

https://github.com/Tahjali11/Mythic-Edge/issues/568

## Contract

`docs/contracts/quality_ruff_current_advisory_measurement_report.md`

## Role Performed

Codex C: Approval-gated Ruff advisory measurement executor.

## Approval Scope Used

The owner granted approval after issue #588 was created. This pass treated that
approval as scoped to the #588 gate:

```yaml
ruff_measurement_execution_authorized: true
report_artifact_creation_authorized: true
target_branch_or_ref: "origin/main"
target_commit: "51d5d8352c10204663d904765a8820bb464a52ac"
raw_ruff_json_committed: false
ci_change_authorized: false
ruff_blocking_promotion_authorized: false
ruff_autofix_authorized: false
parser_behavior_change_authorized: false
```

## Target Verification

- Repository: `Tahjali11/Mythic-Edge`
- Clean worktree: dedicated issue worktree; local path intentionally omitted
  from committed docs.
- Working branch:
  `codex/quality-ruff-sanitized-advisory-report-588`
- Target ref: `origin/main`
- Approved target commit:
  `51d5d8352c10204663d904765a8820bb464a52ac`
- Measured checkout commit:
  `51d5d8352c10204663d904765a8820bb464a52ac`
- Ruff version: `ruff 0.15.12`

The primary checkout was dirty and on a deleted branch, so this pass used a
clean dedicated issue worktree from `origin/main`.

## Measurement Status

`measurement_blocked_raw_source_snippet_public`

The contracted all-rules advisory Ruff command ran with `--exit-zero` and
wrote raw JSON under ignored local evidence storage:

```bash
python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json > _review_/quality_ruff_advisory/2026-06-30-51d5d83-local-macos-r1/ruff-all.json
```

Ruff exited 0. It emitted the expected compatibility warnings for conflicting
docstring rules. No CI, Ruff config, source, parser, corpus, workbook,
webhook, Apps Script, analytics, AI, coaching, release, deploy, or production
behavior changed.

The raw JSON was valid. A local rule-catalog extraction recorded 956 exact Ruff
rule codes from `python3 -m ruff rule --all --output-format json`.

## Blocker

The helper failed closed while generating the sanitized report:

```text
ERROR: measurement_blocked_raw_source_snippet_public
```

Local-only diagnosis found that raw Ruff diagnostic messages for the exact rule
codes `SIM103`, `UP035`, and `UP042` triggered the helper's
raw-source-or-fix-message guard. No raw diagnostic messages, source snippets,
fix text, local paths, or raw Ruff records were copied into this handoff.

This appears narrower than the report contract's message-handling allowance.
The contract permits diagnostic messages to be ignored or reduced to symbolic
signals when they are not emitted publicly. The helper currently rejects these
records before it can ignore the messages and build an otherwise sanitized
summary.

## Files Changed

- `docs/implementation_handoffs/quality_ruff_sanitized_advisory_report_execution.md`

No sanitized report artifact was adopted. An empty failed report output file
was removed. Raw Ruff JSON and rule-catalog files remain only under ignored
`_review_/` local evidence storage and are not staged.

## Generated Local Evidence

Ignored local evidence remains under:

```text
_review_/quality_ruff_advisory/2026-06-30-51d5d83-local-macos-r1/
```

Contents are not staged and are ignored by Git:

- raw all-rules Ruff JSON;
- temporary Ruff rule catalog JSON;
- temporary exact rule-code list.

These files must stay local and uncommitted. They must not be pasted into
issues, PRs, comments, trackers, or public docs.

## Validation Run

Passed:

```bash
git fetch --prune origin
git rev-parse --verify HEAD
git rev-parse --verify origin/main
git diff --quiet --exit-code
git diff --cached --quiet --exit-code
git status --short --branch --untracked-files=all
python3 -m ruff --version
python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json > _review_/quality_ruff_advisory/2026-06-30-51d5d83-local-macos-r1/ruff-all.json
python3 -m json.tool _review_/quality_ruff_advisory/2026-06-30-51d5d83-local-macos-r1/ruff-all.json >/dev/null
python3 -m ruff rule --all --output-format json > _review_/quality_ruff_advisory/2026-06-30-51d5d83-local-macos-r1/ruff-rules.json
python3 -m json.tool _review_/quality_ruff_advisory/2026-06-30-51d5d83-local-macos-r1/ruff-rules.json >/dev/null
```

Blocked as designed:

```bash
python3 tools/generate_ruff_advisory_report.py \
  --input _review_/quality_ruff_advisory/2026-06-30-51d5d83-local-macos-r1/ruff-all.json \
  --rule-codes-file _review_/quality_ruff_advisory/2026-06-30-51d5d83-local-macos-r1/ruff-rule-codes.json \
  --branch-or-ref origin/main \
  --commit 51d5d8352c10204663d904765a8820bb464a52ac \
  --ruff-version 'ruff 0.15.12' \
  --scan-scope src tests tools \
  --command 'python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json' \
  --measured-checkout-root '<clean-measured-checkout-root>'
```

Result:

```text
ERROR: measurement_blocked_raw_source_snippet_public
```

## Still Unverified

- No committed sanitized Ruff advisory report exists for issue #588.
- Zero-baseline candidates were not adopted because helper processing stopped
  before public report generation.
- Whether the helper should ignore raw diagnostic messages for `SIM103`,
  `UP035`, and `UP042` needs a narrow Codex D fix or Codex E review decision.
- No CI or blocking Ruff promotion was attempted.

## Recommended Next Role

Codex D: Module Fixer.

Fix only the concrete helper behavior that blocks #588 report creation: raw
diagnostic message text should be usable as temporary local input without being
emitted, when the final report remains public-safe and symbolic.

## Pasteable Codex D Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex D: Module Fixer for issue #588.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Operating repo/worktree:
Use a clean issue worktree for branch
`codex/quality-ruff-sanitized-advisory-report-588`.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/588

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source contract:
docs/contracts/quality_ruff_current_advisory_measurement_report.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_sanitized_advisory_report_execution.md

Problem:
The approved Ruff advisory measurement ran against origin/main at
51d5d8352c10204663d904765a8820bb464a52ac. Raw Ruff JSON remains local and
uncommitted under `_review_/`. The helper failed closed with
`measurement_blocked_raw_source_snippet_public` because raw diagnostic messages
for exact rule codes `SIM103`, `UP035`, and `UP042` triggered the
raw-source-or-fix-message guard before the helper could emit a sanitized
summary.

Goal:
Make the smallest contract-preserving helper/test fix so raw diagnostic
messages can be ignored or reduced to symbolic-only handling without emitting
raw messages, source snippets, fix text, local paths, private markers, or
secret-shaped values. Then rerun the helper to produce the sanitized #588
report if and only if validation passes.

Protected boundaries:
- Do not commit raw Ruff JSON or `_review_*/` files.
- Do not emit raw diagnostic message text in reports, handoffs, issue comments,
  PR bodies, tracker comments, or public docs.
- Do not change CI or Ruff config.
- Do not promote Ruff rules to blocking.
- Do not run Ruff autofix or unsafe-fix.
- Do not create cleanup issues.
- Do not change parser behavior, fixture state, corpus status,
  release/deploy/production behavior, analytics, AI, or coaching behavior.
- Do not activate #388 or #381.
- Do not claim parser truth, security assurance, privacy assurance, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  or coaching truth.

Expected output:
- Fix summary.
- Files changed.
- Sanitized report status.
- Validation run and results.
- Remaining risks or unverified layers.
- Recommended next role: Codex E if fixed, or Codex B/E if the contract is
  ambiguous.
- Pasteable Codex E prompt if fixed.
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/588"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/584"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/587"
  completed_thread: "C"
  next_thread: "D"
  verdict: "measurement_ran_helper_blocked_raw_diagnostic_message_guard"
  risk_tier: "High"
  branch: "codex/quality-ruff-sanitized-advisory-report-588"
  target_commit: "51d5d8352c10204663d904765a8820bb464a52ac"
  ruff_version: "ruff 0.15.12"
  ruff_measurement_execution_authorized: true
  report_artifact_creation_authorized: true
  raw_ruff_json_committed: false
  sanitized_report_created: false
  blocker: "measurement_blocked_raw_source_snippet_public"
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  parser_behavior_change_authorized: false
```

## Codex D Fixer Addendum

Codex D fixed the concrete raw diagnostic message blocker from the Codex C
handoff, then corrected rebound finding `RUFF-SANREPORT-E-001`. The helper now
ignores natural-language Ruff diagnostic message text when the message is not
emitted in the public report, while still failing closed for explicit raw source
snippets, copied source lines, source patches, fix edits, diff previews,
secret-like message text, raw private payload markers, and readiness, truth, or
assurance overclaims.

Focused regression coverage now proves synthetic natural-language diagnostic
message text is accepted as local input only when it is omitted from rendered
report output, while explicit source snippets and fix-edit previews still fail
closed without echoing submitted content.

Sanitized report status: still blocked, not created. After the message fix and
focused validation passed, rerunning the helper advanced to a different
fail-closed boundary: `measurement_blocked_private_marker` from normalized
diagnostic filename fields. That blocker is outside the un-emitted diagnostic
message exception and should be reviewed or clarified before any path-redaction
or path-omission behavior is implemented.

Additional validation run by Codex D:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_ruff_advisory_report.py
python3 -m py_compile tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py
python3 -m ruff check src tests tools --no-cache
```

Results:

- focused tests: 39 passed;
- py_compile: passed;
- Ruff: passed.

No raw Ruff JSON, `_review_/` files, sanitized report artifact, CI changes,
Ruff config changes, autofix output, parser behavior changes, fixture changes,
corpus status changes, readiness claims, truth claims, or assurance claims were
created or adopted.

Recommended next role after this D addendum: Codex E to confirm the rebound
message fix and route the remaining filename/private-marker blocker to Codex B
if the contract should allow symbolic path omission, or back to Codex D only if
the existing contract already defines the intended path handling.

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/588"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/584"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/587"
  completed_thread: "D"
  next_thread: "E"
  verdict: "raw_diagnostic_message_guard_rebound_fixed_report_still_blocked_by_filename_private_marker"
  risk_tier: "High"
  branch: "codex/quality-ruff-sanitized-advisory-report-588"
  target_commit: "51d5d8352c10204663d904765a8820bb464a52ac"
  ruff_version: "ruff 0.15.12"
  ruff_measurement_execution_authorized: true
  report_artifact_creation_authorized: true
  raw_ruff_json_committed: false
  sanitized_report_created: false
  fixed_blocker: "measurement_blocked_raw_source_snippet_public"
  remaining_blocker: "measurement_blocked_private_marker"
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  parser_behavior_change_authorized: false
```

## Codex D Follow-up Addendum: Symbolic Filename Omission

Codex D fixed the contract-clarified private-marker diagnostic filename
blocker. The helper now keeps public-safe Ruff diagnostic filenames as
repo-relative `affected_paths`, but when a Ruff-native diagnostic filename
normalizes under the measured checkout and contains private-marker vocabulary,
the path is omitted from public output and counted symbolically instead.

The report now preserves the affected finding count with symbolic-only fields:

- `omitted_affected_path_count`
- `path_handling_policy: symbolic_private_marker_filename_omission`
- `path_omission_reason: path_omitted_private_marker_filename`
- approved top-level `path_scope_buckets`

The helper still fails closed for secret-shaped paths, outside-checkout paths,
generated/private artifact paths, unsafe URI/UNC/local path shapes, raw source
snippets, fix edits, raw private payload markers, and readiness/truth/assurance
overclaims.

The sanitized report artifact was created:

```text
docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json
```

Report summary:

- findings: 17,665
- triggered rule codes: 115
- zero-baseline rule codes: 841
- rule summaries with symbolically omitted paths: 10
- omitted affected path count: 73

Raw Ruff JSON remains local and ignored under `_review_/`; it is not tracked,
staged, or copied into the report or handoff.

Validation run by Codex D:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_ruff_advisory_report.py
python3 -m py_compile tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py
python3 -m ruff check src tests tools
git diff --check
python3 -m json.tool docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json >/dev/null
python3 tools/check_secret_patterns.py --base origin/main --repo-root . --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --repo-root . --paths-from-stdin
python3 -m pytest -q
```

Results:

- focused Ruff advisory tests: 41 passed;
- py_compile: passed;
- Ruff: passed;
- git diff whitespace check: passed;
- sanitized report JSON parse: passed;
- path-scoped secret/private marker scan over changed files: forbidden 0,
  warnings 0;
- path-scoped protected-surface scan over changed files: forbidden 0,
  warnings 0;
- changed-file whitespace/final-newline scan: passed;
- full tests: 1,990 passed.

No CI changes, Ruff config changes, blocking rule promotion, autofix output,
parser behavior changes, fixture changes, corpus status changes, release,
deploy, production, analytics, AI, coaching, readiness, truth, or assurance
claims were made.

Recommended next role after this D follow-up: Codex E to review the helper
change and sanitized report against the clarified contract.

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/588"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/584"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/587"
  completed_thread: "D"
  next_thread: "E"
  verdict: "sanitized_report_created_symbolic_private_marker_filename_omission_ready_for_review"
  risk_tier: "High"
  branch: "codex/quality-ruff-sanitized-advisory-report-588"
  target_commit: "51d5d8352c10204663d904765a8820bb464a52ac"
  ruff_version: "ruff 0.15.12"
  ruff_measurement_execution_authorized: true
  report_artifact_creation_authorized: true
  raw_ruff_json_committed: false
  sanitized_report_created: true
  report_artifact: "docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json"
  fixed_blocker: "measurement_blocked_private_marker"
  symbolic_private_marker_filename_omission_authorized: true
  private_marker_filename_output_authorized: false
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  parser_behavior_change_authorized: false
```
