# Ruff Preview-Mode Advisory Discovery Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/619

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Project Roadmap

https://github.com/Tahjali11/Mythic-Edge/issues/568

## Contract

`docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`

## Role Performed

Codex C/D: Module Implementer / current-base refresh fixer.

## Branch And Base

- Branch: `codex/ruff-preview-advisory-619`
- Base ref measured: `origin/main`
- Measured commit:
  `a3227b611f4333b40a6131d710c3ea5d8a7a9ccc`
- Branch was first fast-forwarded from `18595fd` to `8791928`, then refreshed
  from `8791928` to `07c9cab` after Codex E found CT-619-001, then refreshed
  again from `07c9cab` to `a3227b6` after `origin/main` advanced during the
  fixer pass.

Before measurement, the only untracked repo artifact was the in-scope Codex B
contract:

- `docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`

No unrelated dirty tracked files were present.

## Source Artifacts Used

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`
- issue #619
- tracker #567
- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`

## Current Behavior Compared To Contract

Current repo behavior before this slice:

- Ruff normal checks remain stable, non-preview checks through
  `py -m ruff check src tests tools`.
- `pyproject.toml` does not enable `preview = true`.
- `.github/workflows/repo-checks.yml` does not enable preview mode.
- `tools/run_repo_checks.ps1` does not enable preview mode.
- Existing `tools/generate_ruff_advisory_report.py` safely sanitizes stable
  Ruff JSON and rejects local paths, private markers, secret-like values,
  diagnostic messages, source snippets, and autofix command flags.
- The existing stable report schema is
  `quality_ruff_advisory_report.v1`, so it must not be reused as-is for a
  preview-mode report.

Contract gap:

- There was no preview-specific sanitized report shape that records preview
  measurement status, preview-only rules, classification labels, `LOG004`
  handling, and explicit non-claims.

## Implementation Option Chosen

Implemented a narrow wrapper helper:

- keep existing stable Ruff sanitizer as the safety boundary;
- add a preview-specific report builder and CLI;
- summarize affected path families instead of emitting full affected paths;
- keep raw preview Ruff JSON and Ruff rule metadata under ignored `_review_/`;
- commit only the sanitized preview report and implementation handoff.

## Files Changed

- `docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`
  - in-scope Codex B contract, preserved as the source contract.
- `tools/generate_ruff_preview_advisory_report.py`
  - new preview-specific sanitized report helper.
- `tests/test_ruff_preview_advisory_report.py`
  - focused tests for preview schema, `LOG004`, classification, path-family
    summarization, CLI output, and malformed metadata failure.
- `docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json`
  - sanitized preview advisory report.
- `docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md`
  - this handoff.

## Code Changed

Tooling-only code changed.

No parser, runtime, analytics, workbook, webhook, Apps Script, Sheets,
OpenAI/model-provider, AI, coaching, production, CI, or normal Ruff gate
behavior changed.

## Tests Added Or Updated

Added:

- `tests/test_ruff_preview_advisory_report.py`

Existing stable Ruff advisory tests were preserved and run together with the
new preview tests.

## Interface Changes

Added a new local tooling CLI:

```powershell
py tools\generate_ruff_preview_advisory_report.py `
  --input <local-only-raw-preview-json> `
  --rule-metadata-input <local-only-ruff-rule-metadata-json> `
  --branch-or-ref origin/main `
  --commit <commit> `
  --ruff-version "ruff 0.15.12" `
  --command "py -m ruff check src tests tools --preview --select ALL --exit-zero --output-format json --output-file <local-only-raw-json>" `
  --measured-checkout-root .
```

Added committed report schema:

- object: `mythic_edge_quality_ruff_preview_advisory_report`
- schema version: `quality_ruff_preview_advisory_report.v1`

This is a docs/tooling report schema only. It is not a runtime or CI interface.

## Preview Measurement

Measured command:

```powershell
py -m ruff check src tests tools --preview --select ALL --exit-zero --output-format json --output-file _review_\quality_ruff_preview_advisory\2026-07-01-a3227b6\ruff-preview-all.json
```

Raw preview JSON status:

- local-only;
- under ignored `_review_/`;
- not committed;
- raw contents not pasted into this handoff.

Ruff rule metadata was also generated locally under ignored `_review_/` and
was not committed.

Ruff warnings observed during preview measurement:

- `D203` and `D211` are incompatible; Ruff ignored `D203`.
- `D212` and `D213` are incompatible; Ruff ignored `D213`.

These are preview/advisory measurement caveats only. They were not turned into
configuration changes.

## Sanitized Preview Report Summary

Report artifact:

`docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json`

High-level totals:

```yaml
findings: 19119
triggered_rule_codes: 144
preview_only_rule_codes: 139
triggered_preview_only_rule_codes: 28
zero_baseline_preview_rule_codes: 111
```

Classification summary:

```yaml
defer_until_stable: 111
protected_surface_review_required: 104
style_only: 4
watch_list: 36
```

`LOG004` classification:

```yaml
rule_code: LOG004
count: 0
preview_only_rule: true
primary_classification: defer_until_stable
reason: Preview-only rule is measured for awareness but deferred until Ruff stabilizes the rule.
```

## Contracted Area Status

The implementation stayed in Quality / Governance tooling and report artifacts.

No protected parser/runtime/product behavior changed. Preview mode remains
advisory-only and absent from normal repo checks.

## Validation Run

```powershell
git fetch --prune
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
py -m ruff --version
git check-ignore -v _review_\quality_ruff_preview_advisory\2026-07-01-a3227b6\ruff-preview-all.json
py -m ruff check src tests tools --preview --select ALL --exit-zero --output-format json --output-file _review_\quality_ruff_preview_advisory\2026-07-01-a3227b6\ruff-preview-all.json
py -m ruff rule --all --output-format json
py tools\generate_ruff_preview_advisory_report.py ...
py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-a3227b6-ruff-preview-advisory-report.json
py -m pytest -q tests\test_ruff_preview_advisory_report.py tests\test_ruff_advisory_report.py
py -m ruff check tools\generate_ruff_preview_advisory_report.py tests\test_ruff_preview_advisory_report.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over changed files
path-scoped secret/private-marker scan over changed files
```

Results before final hygiene pass:

- Branch fast-forwarded to match current `origin/main`.
- `HEAD` and `origin/main`:
  `a3227b611f4333b40a6131d710c3ea5d8a7a9ccc`.
- Ruff version: `ruff 0.15.12`.
- Raw preview JSON path: ignored by `.gitignore`.
- Sanitized preview report JSON: valid.
- Focused preview/stable Ruff advisory tests: passed, `46 passed`.
- Focused Ruff check for new helper/tests: passed.
- Normal repo Ruff check: passed.
- `git diff --check`: passed.
- `py tools\check_agent_docs.py`: passed.
- Path-scoped protected-surface scan: passed, `forbidden 0`, `warnings 0`.
- Path-scoped secret/private-marker scan: passed, `forbidden 0`,
  `warnings 0`.
- `git diff -- pyproject.toml .github\workflows\repo-checks.yml
  tools\run_repo_checks.ps1`: no diff.
- Search for preview-mode configuration in `pyproject.toml`,
  `.github\workflows\repo-checks.yml`, and `tools\run_repo_checks.ps1`: no
  matches.
- Ignored local artifacts under `_review_/quality_ruff_preview_advisory/`:
  `ruff-preview-all.json` and `ruff-rules-all.json`; both remain untracked.

## CT-619-001 Refresh Status

Fixed locally. The stale reports for commits `8791928` and `07c9cab` were
removed from the active package and replaced with the current-base report for
commit `a3227b6`. The measured report commit now matches `origin/main`.

## Still Unverified

- GitHub CI did not run in this local Codex C thread.
- No PR was opened.
- No CodeQL, security, privacy, parser, release, deploy, production,
  analytics-truth, AI-truth, or coaching-readiness claim is made.
- Preview-only classifications are advisory and must be reviewed before any
  future exact-code issue.

## Reviewer Focus

Codex E should verify:

- preview mode remains absent from `pyproject.toml`, CI, and
  `tools/run_repo_checks.ps1`;
- raw preview JSON and Ruff rule metadata remain ignored and untracked;
- the committed report uses the preview-specific schema;
- the report does not include raw diagnostic messages, source snippets, local
  absolute paths, private markers, secrets, raw logs, generated artifacts, or
  readiness overclaims;
- `LOG004` is not treated as stable blocking-ready;
- classification labels are advisory only;
- no parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/
  coaching/production behavior changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #619.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/619

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/ruff-preview-advisory-619

Contract:
docs/contracts/quality_ruff_preview_mode_advisory_discovery.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md

Sanitized report:
docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json

Review goal:
Verify that the #619 implementation satisfies the contract while keeping Ruff
preview mode advisory-only. Lead with findings ordered by severity.

Check:
- preview mode remains absent from pyproject.toml, CI, and tools/run_repo_checks.ps1;
- raw preview JSON and Ruff rule metadata are ignored and untracked;
- committed report has preview-specific schema and explicit non-claims;
- report records measured ref/commit, Ruff version, command, scan scope, totals,
  classifications, and LOG004 deferral;
- report does not include raw diagnostic messages, source snippets, local
  absolute paths, private markers, secrets, raw logs, generated artifacts, or
  readiness overclaims;
- LOG004 is not treated as stable blocking-ready;
- no parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/
  coaching/production behavior changed.

Suggested validation:
git status --short --branch --untracked-files=all
py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-a3227b6-ruff-preview-advisory-report.json
py -m pytest -q tests\test_ruff_preview_advisory_report.py tests\test_ruff_advisory_report.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
git check-ignore -v _review_\quality_ruff_preview_advisory\2026-07-01-a3227b6\ruff-preview-all.json
git check-ignore -v _review_\quality_ruff_preview_advisory\2026-07-01-a3227b6\ruff-rules-all.json

Also run path-scoped protected-surface and secret/private-marker scans over
changed tracked files.

Produce:
docs/contract_test_reports/quality_ruff_preview_mode_advisory_discovery.md

Do not edit implementation files unless explicitly asked. Do not stage, commit,
push, open a PR, merge, close issue #619, or mark tracker #567 complete.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/619"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "D/C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_ruff_preview_mode_advisory_discovery.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md"
  report_artifact: "docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json"
  risk_tier: "Medium workflow risk; low runtime risk because advisory-only"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/ruff-preview-advisory-619"
  measured_ref: "origin/main"
  measured_commit: "a3227b611f4333b40a6131d710c3ea5d8a7a9ccc"
  ruff_version: "ruff 0.15.12"
  preview_measurement: "refreshed current-base advisory-only"
  enforcement_authorized: false
  ci_change_authorized: false
  pyproject_preview_authorized: false
  ruff_autofix_authorized: false
  ruff_unsafe_fix_authorized: false
  log004_classification: "defer_until_stable"
  raw_preview_json_status: "local-only ignored under _review_; not committed"
  ct_619_001_status: "fixed locally; report commit matches current origin/main"
  validation:
    - "py -m json.tool sanitized preview report -> passed"
    - "py -m pytest -q tests\\test_ruff_preview_advisory_report.py tests\\test_ruff_advisory_report.py -> passed, 46 passed"
    - "py -m ruff check tools\\generate_ruff_preview_advisory_report.py tests\\test_ruff_preview_advisory_report.py -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not enable preview mode in pyproject.toml, CI, or normal repo checks."
    - "Do not promote preview rules to blocking gates."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not commit raw Ruff JSON or raw terminal output."
    - "Do not claim parser correctness, security assurance, privacy assurance, release readiness, deploy readiness, production readiness, analytics truth, AI truth, or coaching truth."
    - "Do not change parser behavior, fixtures, corpus status, analytics behavior, workbook behavior, webhook behavior, Apps Script behavior, OpenAI/model-provider behavior, AI/coaching behavior, or production behavior."
```
