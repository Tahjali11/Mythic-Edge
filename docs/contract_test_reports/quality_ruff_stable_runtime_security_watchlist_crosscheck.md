# Contract Test Report: Ruff Stable Runtime/Security Watch-List Crosscheck

## Findings

No blocking findings.

The #631 contract accurately records a stable non-preview Ruff crosscheck for
the named watch-list rules, keeps every rule advisory-only, and does not
authorize implementation, Ruff promotion, preview mode, autofix, unsafe-fix,
CI edits, `pyproject.toml` edits, or product behavior changes.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/631

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Contract

`docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`

## Source Artifact

`docs/contracts/quality_ruff_preview_advisory_candidate_routing.md`

## Implementation Under Test

Branch: `codex/ruff-stable-runtime-security-crosscheck-631`

Changed package:

- `docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`

No code, tests, CI, Ruff config, parser, analytics, workbook, webhook,
OpenAI/model-provider, AI/coaching, Line Tracer, production, generated, or
local/private artifact files are part of this package.

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The contract must record current-base stable non-preview Ruff evidence for
`B009`, `DTZ001`, `PERF403`, `RUF001`, `RUF022`, `RUF059`, `RUF100`, `S112`,
`S314`, `S606`, `S607`, `TRY004`, `TRY301`, and `TRY401`, classify the rule
pool as advisory/watch-list only, and preserve the boundary that future cleanup
or promotion requires a separate scoped issue, contract, implementation, and
review.

## Internal Project Area Reviewed

Quality / validation gates.

No mismatch found against the stated internal project area. Ruff evidence is
treated as static-analysis routing evidence only, not parser truth, security
assurance, privacy assurance, deploy readiness, release readiness, production
readiness, analytics truth, AI truth, or coaching truth.

## Bridge-Code Status Reviewed

`shared_support`

The documented bridge from #627 preview-routing evidence to #631 stable
non-preview crosscheck evidence is coherent and advisory-only. No reverse flow
into parser/runtime behavior, CI, Ruff configuration, or production behavior
was observed.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
git diff --name-status origin/main...HEAD
git ls-files --others --exclude-standard
gh issue view 631 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 567 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m ruff --version
py -m ruff check src tests tools --select B009,DTZ001,PERF403,RUF001,RUF022,RUF059,RUF100,S112,S314,S606,S607,TRY004,TRY301,TRY401 --output-format json
py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-a3227b6-ruff-preview-advisory-report.json
rg -n "preview|--preview|select ALL|unsafe-fix|autofix|ruff" pyproject.toml .github\workflows\repo-checks.yml tools\run_repo_checks.ps1
git diff --check -- docs\contracts\quality_ruff_stable_runtime_security_watchlist_crosscheck.md
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Additional reviewer-only protected-surface crosscheck:

```powershell
py -m ruff check src tests tools --select B009,DTZ001,PERF403,RUF001,RUF022,RUF059,RUF100,S112,S314,S606,S607,TRY004,TRY301,TRY401 --output-format json
# then path-feed the repo-relative finding paths to:
py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

## Results

- Branch check: on `codex/ruff-stable-runtime-security-crosscheck-631`.
- Branch sync: `HEAD...origin/main` reported `0 0`.
- Issue state: #631 is open.
- Tracker state: #567 is open.
- Changed/untracked scope before this report: only
  `docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`.
- Ruff version: `ruff 0.15.12`.
- Exact-code Ruff crosscheck: expected exit code `1`; total findings `86`;
  per-code counts matched the contract.
- Source preview advisory report: JSON parsed successfully.
- Normal Ruff surfaces: `pyproject.toml`, `.github/workflows/repo-checks.yml`,
  and `tools/run_repo_checks.ps1` showed normal Ruff usage only; no preview,
  autofix, unsafe-fix, or broad `select ALL` adoption in normal repo checks.
- Contract diff check: passed.
- Agent docs check: passed.
- Contract path protected-surface scan: passed, forbidden `0`, warnings `0`.
- Contract path secret/private-marker scan: passed, forbidden `0`, warnings
  `0`.
- Ruff finding path protected-surface crosscheck: passed, forbidden `0`,
  warnings `1`; the warning is the expected `webhook_payload_shape` signal for
  `src/mythic_edge_parser/app/runner.py`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | No findings opened. | not_blocking | N/A | Current-base validation matched contract evidence. | F |

## Confirmed Contract Matches

- The contract uses stable non-preview Ruff evidence only.
- The measured commit is current with `origin/main` in this worktree.
- Every named rule is active in stable Ruff `0.15.12`.
- The exact-code Ruff crosscheck reports `86` findings, matching the contract.
- Per-code counts match the contract exactly:
  `B009` 24, `DTZ001` 1, `PERF403` 1, `RUF001` 2, `RUF022` 2, `RUF059` 3,
  `RUF100` 17, `S112` 1, `S314` 2, `S606` 2, `S607` 17, `TRY004` 9,
  `TRY301` 3, and `TRY401` 2.
- The contract correctly records that `RUF100` drifted from the older #627
  source count and that current exact-code evidence must be used.
- The path-family classification is consistent with reviewer evidence.
- The `runner.py` protected-surface warning is explicitly treated as a future
  contract/review signal, not authorization to edit runtime code.
- The contract forbids preview mode, broad families, autofix, unsafe-fix,
  implementation, CI changes, `pyproject.toml` changes, and rule promotion.
- No readiness, security assurance, privacy assurance, parser truth, analytics
  truth, AI truth, coaching truth, production, release, deploy, or fixture/corpus
  claim is made.

## Contract Mismatches

None found.

## Missing Tests

None blocking.

This is a docs-only advisory-routing contract. No implementation tests are
required in this thread. Future cleanup or promotion issues must add focused
behavior-preservation tests for any touched runtime, parser-adjacent, launcher,
local app, security-tooling, or protected-surface paths.

## Drift Notes

- Repo drift: none observed; branch is even with `origin/main`.
- Issue lifecycle drift: none observed; #631 remains open and ready for
  reviewed docs-only submission.
- Tracker drift: none observed; #567 remains open and must not be marked
  complete from this child issue.
- CI drift: not checked in GitHub because this local docs-only branch has not
  been submitted as a PR in this thread.
- Protected-surface drift: none observed in changed files.

## Protected-Surface Status

Changed-doc scan: passed, forbidden `0`, warnings `0`.

Reviewer Ruff finding path crosscheck: passed, forbidden `0`, warnings `1`.
The single warning is expected and non-blocking for this report because no
protected source file was changed; it confirms that future cleanup touching
`src/mythic_edge_parser/app/runner.py` must go through a scoped contract.

## Secret / Private Artifact Status

Changed-doc scan: passed, forbidden `0`, warnings `0`.

No raw Ruff JSON, raw terminal dump, local-only artifact, generated artifact,
secret, credential, raw log, workbook export, SQLite file, app-data artifact,
or private path was added by this report.

## Generated Artifact Status

No generated/private artifacts were kept.

This review artifact is a durable repo documentation artifact, not a generated
runtime/private artifact.

## Recommendation

Approve.

Route #631 to Codex F for docs-only submitter handling. Codex F should stage
only:

- `docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`
- `docs/contract_test_reports/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`

After submission, any next #567 child should be framed by Codex A as a separate
narrow cleanup or follow-up issue. No rule in this #631 pool is blocking-ready
from this contract-test result.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #631.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/631

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Branch:
codex/ruff-stable-runtime-security-crosscheck-631

Base:
origin/main

Reviewed artifacts:
- docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md
- docs/contract_test_reports/quality_ruff_stable_runtime_security_watchlist_crosscheck.md

Codex E verdict:
No blocking findings. The #631 contract accurately records the stable
non-preview Ruff crosscheck and keeps all candidate rules advisory/watch-list
only. No implementation, CI, pyproject, preview, autofix, unsafe-fix, broad
cleanup, or rule promotion is authorized.

Goal:
Stage only the reviewed #631 docs, commit, push the branch, and open a draft PR
against the approved base. Do not close #631, mark tracker #567 complete, or
claim rule-promotion readiness.

Suggested validation before commit:
git status --short --branch --untracked-files=all
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over the two reviewed docs
path-scoped secret/private-marker scan over the two reviewed docs

Do not:
- stage unrelated files
- edit implementation
- edit pyproject.toml or CI
- enable preview mode
- run autofix or unsafe-fix
- promote any Ruff rule
- change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior
- expose raw/private/generated/local artifacts or secrets

Final output:
- branch and commit
- PR URL
- files staged
- validation result
- remaining risk
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/631"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md"
  target_artifact: "docs/contract_test_reports/quality_ruff_stable_runtime_security_watchlist_crosscheck.md"
  risk_tier: "Medium workflow risk; low runtime risk because docs-only advisory routing"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/ruff-stable-runtime-security-crosscheck-631"
  measured_commit: "048e31146f185840f032ec3ff45f93e6822b8fce"
  ruff_version: "ruff 0.15.12"
  verdict: "approved_for_codex_f_docs_only_submission"
  validation:
    - "git status --short --branch --untracked-files=all -> branch codex/ruff-stable-runtime-security-crosscheck-631; untracked #631 contract before report"
    - "git rev-list --left-right --count HEAD...origin/main -> 0 0"
    - "py -m ruff --version -> ruff 0.15.12"
    - "stable non-preview exact-code Ruff crosscheck -> exit 1 expected; 86 findings; all per-code counts matched contract"
    - "source preview advisory report JSON parse -> passed"
    - "normal Ruff surfaces inspection -> no preview/autofix/unsafe-fix/broad select ALL adoption in pyproject, CI, or repo-check script"
    - "git diff --check -- docs\\contracts\\quality_ruff_stable_runtime_security_watchlist_crosscheck.md -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "contract path protected-surface scan -> passed, forbidden 0, warnings 0"
    - "contract path secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "Ruff finding path protected-surface crosscheck -> passed, forbidden 0, warnings 1 expected runner.py webhook_payload_shape signal"
  protected_surface_status: "passed; changed docs forbidden 0 warnings 0; finding path crosscheck warning 1 expected and non-blocking"
  secret_private_marker_status: "passed; changed docs forbidden 0 warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  stop_conditions:
    - "Do not implement code from this contract."
    - "Do not edit pyproject.toml or CI."
    - "Do not enable preview mode."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not promote any rule."
    - "Do not run broad cleanup."
    - "Do not change parser/product/runtime behavior."
    - "Do not claim readiness, truth, security, privacy, deploy, or production assurance."
```
