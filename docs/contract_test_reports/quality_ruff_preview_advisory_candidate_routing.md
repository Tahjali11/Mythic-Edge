# Contract Test Report: Ruff Preview Advisory Candidate Routing

## Findings

No blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-627-001 | P3 | `remaining_non_blocking` | Source metadata wording is slightly imprecise: the contract summarizes `ruff_version` as `0.15.12`, while the committed sanitized report records `ruff 0.15.12`. | non_blocking | `docs/contracts/quality_ruff_preview_advisory_candidate_routing.md` source evidence summary uses `ruff_version: 0.15.12`. | `docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json` parses successfully and reports `ruff_version: ruff 0.15.12`; routing decisions, counts, classifications, and non-claim boundaries remain accurate. | F, with optional docs polish if desired |

## Role Performed

Codex E: Module Reviewer / contract-test thread.

## Issue And Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/627
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/619
- Source PR: https://github.com/Tahjali11/Mythic-Edge/pull/626

## Contract Reviewed

- Contract: `docs/contracts/quality_ruff_preview_advisory_candidate_routing.md`
- Source report: `docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json`

No separate Codex C implementation handoff was expected for this slice. The package under review is a Codex B docs-only routing contract.

## Implementation Under Test

- Branch: `codex/ruff-preview-routing-627`
- Base: `origin/main`
- Branch sync: `0 0`
- Changed files:
  - `docs/contracts/quality_ruff_preview_advisory_candidate_routing.md`
  - `docs/contract_test_reports/quality_ruff_preview_advisory_candidate_routing.md`

## Contract Summary

The contract interprets the merged #619 Ruff preview advisory report and defines safe routing for future Ruff work. It must not enable Ruff preview mode, promote preview-only rules, alter CI, change `pyproject.toml`, authorize autofix or unsafe-fix, or claim parser, security, privacy, release, deploy, production, analytics, AI, or coaching readiness.

## Confirmed Contract Matches

- The source report exists and parses as valid JSON.
- The source report records `preview_enabled_for_measurement: true`, while `preview_enabled_in_pyproject`, `preview_enabled_in_ci`, `blocking_promotion_authorized`, `autofix_authorized`, and `unsafe_fix_authorized` are all false.
- Normal Ruff surfaces remain non-preview:
  - `.github/workflows/repo-checks.yml` runs `py -m ruff check src tests tools`;
  - `tools/run_repo_checks.ps1` runs `py -m ruff check src tests tools`;
  - `pyproject.toml` does not enable preview mode.
- `LOG004` remains correctly routed to `defer_until_stable`; the source report records count `0`, preview-only `true`, and classification `defer_until_stable`.
- Preview-only rules remain advisory or deferred and are not promoted to blocking candidates.
- Stable non-preview watch-list rules are routed only to future Codex A framing after normal non-preview crosscheck.
- Protected-surface review is required before any future candidate work that may touch parser, runtime, security, privacy, workbook, analytics, generated artifacts, or related protected surfaces.
- The contract does not authorize broad Ruff families, `--select ALL` enforcement, autofix, unsafe-fix, raw output commits, CI changes, parser behavior changes, fixture/corpus changes, analytics behavior changes, workbook/webhook/App Script changes, OpenAI/AI/coaching changes, Line Tracer changes, or production changes.

## Alert / Rule Routing Verification

| Rule group | Contract route | Verification verdict |
| --- | --- | --- |
| `LOG004` | `defer_until_stable` | Matches source report: count `0`, preview-only `true`, classification `defer_until_stable`. |
| Higher-priority stable watch-list pool | Future stable non-preview crosscheck only | Matches source report for `B009`, `DTZ001`, `PERF403`, `RUF001`, `RUF022`, `RUF059`, `RUF100`, `S112`, `S314`, `S606`, `S607`, `TRY004`, `TRY301`, and `TRY401`. |
| Triggered preview-only rules | Advisory-only / deferred until stable | Matches contract boundary; no blocking promotion authorized. |
| Zero-baseline preview rules | Defer until stable | Matches contract boundary; clean preview-only rules are not treated as gate-ready. |

## Contract Mismatches

- Non-blocking source metadata wording precision: the source report stores `ruff_version` as `ruff 0.15.12`, while the contract summary shortens it to `0.15.12`. This does not affect the candidate routing decision, enforcement boundaries, or validation results.

## Missing Tests Or Safeguards

None required for this docs-only routing contract. The important safeguard is policy-level: future Ruff candidate issues must rerun normal non-preview evidence before implementation or promotion.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
git diff --name-status origin/main...HEAD
py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-a3227b6-ruff-preview-advisory-report.json
rg -n "preview|--preview|select ALL|unsafe-fix|autofix|ruff" pyproject.toml .github\workflows\repo-checks.yml tools\run_repo_checks.ps1
git diff --check -- docs\contracts\quality_ruff_preview_advisory_candidate_routing.md
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

## Validation Results

- Branch status: `codex/ruff-preview-routing-627...origin/main`
- Branch sync: `0 0`
- Source report JSON validation: passed.
- Normal Ruff surface inspection: passed; no preview mode, autofix, unsafe-fix, or `--select ALL` enforcement found in normal repo checks.
- Contract diff check: passed.
- Final `git diff --check`: passed.
- New-file whitespace/final-newline check over the untracked contract and report: passed.
- Agent docs check: passed, errors `0`, warnings `0`.
- Protected-surface scan over contract and report: passed, forbidden `0`, warnings `0`.
- Secret/private-marker scan over contract and report: passed, forbidden `0`, warnings `0`.

## Protected-Surface Status

Passed. The reviewed package is docs-only and does not touch parser/runtime, analytics schema, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, Line Tracer, corpus, fixtures, CI behavior, production behavior, or generated/private artifact surfaces.

## Secret / Private-Artifact Status

Passed. No raw logs, raw Ruff output, private paths, secrets, credentials, generated data, app-data artifacts, workbook exports, SQLite contents, or local-only artifacts were introduced.

## Generated Artifact Status

No generated private artifacts were kept. The committed source report is the previously merged sanitized advisory summary from #619/#626; raw Ruff JSON remains out of scope.

## Drift Notes

- Issue lifecycle: #627 remains open during review.
- PR lifecycle: source PR #626 is merged to `main`.
- Repo drift: none observed; branch is synced with `origin/main`.
- Enforcement drift: none observed; preview mode remains absent from `pyproject.toml`, CI, and the repo-check helper.

## Recommendation

Approve for Codex F submission, with one non-blocking documentation precision note for the `ruff_version` source metadata wording. If the owner wants perfect field parity before submission, route to Codex D for a one-line contract polish; otherwise Codex F can stage the reviewed #627 docs-only artifact package.

## Next Workflow Action

Next recommended role: Codex F submitter.

Pasteable Codex F prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #627.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/627

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Branch:
codex/ruff-preview-routing-627

Base:
main

Reviewed artifacts:
- docs/contracts/quality_ruff_preview_advisory_candidate_routing.md
- docs/contract_test_reports/quality_ruff_preview_advisory_candidate_routing.md

Goal:
Stage, commit, push, and open a draft PR for the docs-only Ruff preview advisory candidate routing package after Codex E review. Stage only the reviewed #627 files.

Codex E verdict:
No blocking findings. One non-blocking documentation precision note remains: the source report records `ruff_version: ruff 0.15.12`, while the contract summary shortens it to `0.15.12`. This does not affect routing, enforcement boundaries, or validation. If you choose to polish this before commit, keep the edit limited to that exact metadata wording.

Validation to rerun before commit:
- git status --short --branch --untracked-files=all
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over reviewed files
- path-scoped secret/private-marker scan over reviewed files

Do not:
- enable Ruff preview mode;
- change pyproject.toml, CI, or tools/run_repo_checks.ps1;
- promote any Ruff rule to blocking;
- run autofix or unsafe-fix;
- commit raw Ruff JSON, raw terminal output, generated/private artifacts, local-only artifacts, secrets, raw logs, SQLite contents, workbook exports, or app-data files;
- change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/corpus/fixture/production behavior;
- close #627 or tracker #567 unless explicitly authorized.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/627"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  completed_thread: "E"
  next_thread: "F"
  branch: "codex/ruff-preview-routing-627"
  base_branch: "main"
  source_artifact: "docs/contracts/quality_ruff_preview_advisory_candidate_routing.md"
  target_artifact: "docs/contract_test_reports/quality_ruff_preview_advisory_candidate_routing.md"
  source_report: "docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json"
  findings:
    - "No blocking findings."
    - "CT-627-001 P3 non-blocking: contract summary shortens source report ruff_version from 'ruff 0.15.12' to '0.15.12'."
  verdict: "approved_for_codex_f_with_non_blocking_docs_precision_note"
  decision: "No preview-derived rule is blocking-ready; LOG004 remains deferred until stable; stable non-preview watch-list codes may feed future Codex A framing only after normal non-preview crosscheck."
  preview_mode_authorized: false
  ci_change_authorized: false
  blocking_promotion_authorized: false
  autofix_authorized: false
  unsafe_fix_authorized: false
  validation:
    - "branch sync -> 0 0 with origin/main"
    - "source Ruff preview advisory JSON parse -> passed"
    - "normal Ruff surface inspection -> no preview/autofix/unsafe-fix enforcement found"
    - "git diff --check -- contract -> passed"
    - "final git diff --check -> passed"
    - "new-file whitespace/final-newline check -> passed"
    - "agent docs -> passed, errors 0, warnings 0"
    - "path-scoped protected-surface scan over contract and report -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over contract and report -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
