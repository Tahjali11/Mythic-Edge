# Quality Ruff Third Logging Exact-Code Candidate Selection Contract Test Report

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/618
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568

## Contract

- `docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md`

## Implementation Under Test

- Branch: `codex/ruff-next-tranche-567`
- Base: `origin/main`
- Implementation handoff:
  `docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md`
- Config changed:
  `pyproject.toml`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The implementation must promote only the contracted third Ruff logging/runtime
visibility exact-code tranche:

```text
G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
```

It must preserve the existing `E`, `F`, `I`, `B`, and `DTZ` selections, keep
`LOG004` excluded, avoid broad `G`, broad `LOG`, `ALL`, preview mode, autofix,
unsafe-fix, and broad cleanup, and leave CI/local lint command scope at:

```powershell
py -m ruff check src tests tools
```

This is a quality-tooling configuration promotion only. It must not claim or
change parser truth, runtime behavior, analytics truth, workbook/webhook/App
Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior,
security/privacy assurance, release readiness, deploy readiness, production
behavior, secrets, raw logs, generated artifacts, or local-only artifacts.

## Internal Project Area Reviewed

Quality / Governance, with CI / Tooling as the validation surface.

## Bridge-Code Status Reviewed

`not_bridge_code`

## Findings

No blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-618-001 | none | `not_reproduced` | No contract mismatch found. | not_blocking | Codex E reviewed the config, contract, handoff, CI command, local helper command, and validation output. | Exact-code assertion passed; Ruff checks passed; helper test passed; safety scans passed. | F |

## Checks Run

```text
git status --short --branch --untracked-files=all -> expected #618 package only
git rev-parse HEAD -> 94d337c635769c214c5beecabef93932033210f3
git rev-parse origin/main -> 94d337c635769c214c5beecabef93932033210f3
git rev-list --left-right --count HEAD...origin/main -> 0 0
py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015 -> All checks passed
py -m ruff check src tests tools -> All checks passed
py -m pytest -q tests\test_run_repo_checks_script.py -> 1 passed
git diff --check -> passed
py tools\check_agent_docs.py -> passed, errors 0, warnings 0
ruff select exact-code assertion -> passed
path-scoped protected-surface scan over #618 files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over #618 files -> passed, forbidden 0, warnings 0
changed-file whitespace/final-newline check -> passed
```

## Results

Passed. The implementation satisfies the contract and is ready for Codex F
submission.

## Confirmed Contract Matches

- `pyproject.toml` adds exactly:
  - `G001`
  - `G002`
  - `G003`
  - `G004`
  - `G010`
  - `G101`
  - `G201`
  - `G202`
  - `LOG001`
  - `LOG002`
  - `LOG007`
  - `LOG009`
  - `LOG014`
  - `LOG015`
- Existing selected rules remain intact:
  - `E`
  - `F`
  - `I`
  - `B006`
  - `B008`
  - `B012`
  - `B023`
  - `B904`
  - `DTZ002`
  - `DTZ003`
  - `DTZ004`
  - `DTZ006`
  - `DTZ011`
  - `DTZ012`
  - `DTZ901`
- `LOG004` remains excluded from `pyproject.toml`.
- Broad `G`, broad `LOG`, and `ALL` are not selected.
- Ruff preview mode is not enabled.
- Ruff autofix, fix-only, and unsafe-fix were not introduced.
- `.github/workflows/repo-checks.yml` still runs
  `py -m ruff check src tests tools`.
- `tools/run_repo_checks.ps1` still runs
  `py -m ruff check src tests tools`.
- `tests/test_run_repo_checks_script.py` still covers the local helper lint
  command scope.
- No source cleanup, runtime code, product code, CI shape, parser behavior,
  analytics schema, workbook behavior, webhook behavior, Apps Script/Sheets
  behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production
  behavior changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

No helper or CI command changed, so the existing
`tests/test_run_repo_checks_script.py` coverage is sufficient for this
config-only promotion.

## Drift Notes

- Branch drift: none; branch is even with `origin/main`.
- Repo drift: none found in reviewed scope.
- CI drift: none; CI lint command remains the same.
- Local helper drift: none; local helper lint command remains the same.
- Tracker drift: none reviewed as blocking. Tracker #567 remains open.
- Product/runtime/local-data drift: none found.

## Protected-Surface Status

Passed. Path-scoped protected-surface scan reported forbidden 0, warnings 0.

Protected parser, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema, workbook schema, webhook
payload shape, Apps Script, Google Sheets, output transport, production,
OpenAI/model-provider, AI/coaching, Line Tracer, fixtures, corpus status, and
private evidence workflow surfaces were not touched.

## Secret / Private Marker Status

Passed. Path-scoped secret/private-marker scan reported forbidden 0, warnings
0. No raw Ruff JSON, raw terminal logs, private paths, secrets, credentials,
tokens, webhook URLs, spreadsheet IDs, environment values, generated artifacts,
or local-only files were added.

## Generated Artifact Status

No generated artifacts were created or kept.

## Remaining Risk

- GitHub Actions has not run on a pushed PR for this local package yet.
- `origin/main` may advance before submitter/deployer work; Codex F/G should
  recheck branch freshness and rerun the focused Ruff checks before publishing
  or merging.

## Recommendation

Approve for Codex F.

Codex F should stage only:

- `pyproject.toml`
- `docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md`
- `docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md`
- `docs/contract_test_reports/quality_ruff_third_logging_exact_code_candidate_selection.md`

Do not stage unrelated files, close #618, close tracker #567, merge, enable
preview mode, add `LOG004`, or change CI/product behavior.

## Next Workflow Action

Next role: Codex F.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #618.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/618

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Branch:
codex/ruff-next-tranche-567

Base / target:
origin/main / main after explicit user approval for PR submission only. Do not merge.

Codex E review artifact:
docs/contract_test_reports/quality_ruff_third_logging_exact_code_candidate_selection.md

Approved files to stage:
- pyproject.toml
- docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md
- docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md
- docs/contract_test_reports/quality_ruff_third_logging_exact_code_candidate_selection.md

Goal:
Stage only the reviewed #618 Ruff third logging exact-code tranche package,
commit, push, and open or update a draft PR. Do not merge, close #618, close
tracker #567, add LOG004, enable preview mode, broaden Ruff families, run
autofix/unsafe-fix, or change product behavior.

Before committing, rerun:
- git status --short --branch --untracked-files=all
- git rev-list --left-right --count HEAD...origin/main
- py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
- py -m ruff check src tests tools
- py -m pytest -q tests\test_run_repo_checks_script.py
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over staged files
- path-scoped secret/private-marker scan over staged files

Final output:
- commit hash
- PR URL
- files staged
- validation results
- protected-surface status
- secret/private-marker status
- next recommended role Codex G after PR checks
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/618"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md"
  implementation_handoff: "docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md"
  artifact_produced: "docs/contract_test_reports/quality_ruff_third_logging_exact_code_candidate_selection.md"
  risk_tier: "Medium workflow risk; low runtime risk"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/ruff-next-tranche-567"
  promoted_codes:
    - "G001"
    - "G002"
    - "G003"
    - "G004"
    - "G010"
    - "G101"
    - "G201"
    - "G202"
    - "LOG001"
    - "LOG002"
    - "LOG007"
    - "LOG009"
    - "LOG014"
    - "LOG015"
  excluded_codes:
    - "LOG004"
  validation:
    - "branch sync -> passed, 0 0 with origin/main"
    - "exact candidate Ruff check -> passed"
    - "repo Ruff check -> passed"
    - "repo-check helper test -> passed, 1 test"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "ruff select exact-code assertion -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "changed-file whitespace/final-newline check -> passed"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  codex_f_recommended: true
  next_recommended_role: "Codex F: Module Submitter"
```
