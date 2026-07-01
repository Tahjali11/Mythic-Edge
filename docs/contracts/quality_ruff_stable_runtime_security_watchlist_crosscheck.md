# Quality Contract: Ruff Stable Runtime/Security Watch-List Crosscheck

## Module

`quality_ruff_stable_runtime_security_watchlist_crosscheck`

Plain English: this contract records a stable, non-preview Ruff crosscheck for
the higher-priority runtime/security-adjacent watch-list pool routed by #627.
It decides how to classify the current findings and what evidence a later
cleanup or promotion issue would need.

This is a Codex B contract artifact only. It does not implement code, change
Ruff configuration, change CI, enable preview mode, run autofix, run
unsafe-fix, promote any rule, or change product behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/631
- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/627
- Source contract:
  `docs/contracts/quality_ruff_preview_advisory_candidate_routing.md`
- Source PR: https://github.com/Tahjali11/Mythic-Edge/pull/629

## Tracker

- Ruff tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568

Tracker #567 remains open. This contract does not complete the Ruff ratchet
queue.

## Owning Layer

Quality and validation tooling.

Ruff owns only static-analysis evidence for the measured command and ref. Ruff
does not own parser truth, runtime truth, security assurance, privacy
assurance, release readiness, deploy readiness, production readiness, analytics
truth, AI truth, or coaching truth.

## Internal Project Area

Quality / validation gates.

## Truth Owner

- Current stable crosscheck evidence owner: the exact non-preview Ruff command
  recorded in this contract.
- Candidate routing owner: this contract.
- Future cleanup or promotion owner: a later scoped issue, contract,
  implementation handoff, and review.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
#627 preview-routing contract
  -> stable non-preview exact-code Ruff crosscheck
  -> candidate grouping / watch-list routing
  -> future scoped issue only if justified
```

Forbidden reverse flow:

- Ruff findings must not directly change parser behavior, runtime behavior,
  analytics, workbook behavior, webhook behavior, Apps Script behavior, CI, or
  production behavior.
- Ruff findings must not be treated as proof of a security bug.
- A nonzero finding count must not be promoted to a blocking gate before a
  cleanup issue reaches zero baseline and receives a later promotion contract.

## Files Owned By This Contract

- `docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`

This contract does not authorize edits to:

- `pyproject.toml`;
- `.github/workflows/repo-checks.yml`;
- `tools/run_repo_checks.ps1`;
- Ruff helper tooling;
- parser, analytics, workbook, webhook, Apps Script, Google Sheets, OpenAI,
  AI, coaching, Line Tracer, production, fixtures, corpus, local app runtime,
  or security-sensitive behavior.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #631
- Issue #627
- Tracker #567
- Project roadmap #568
- `docs/contracts/quality_ruff_preview_advisory_candidate_routing.md`
- `docs/contract_test_reports/quality_ruff_preview_advisory_candidate_routing.md`
- `docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json`
- `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- `docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md`
- `docs/contracts/quality_ruff_second_bug_risk_tranche.md`
- `docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`

## Stable Non-Preview Crosscheck Policy

The #631 crosscheck must use stable Ruff only:

```powershell
py -m ruff check src tests tools --select B009,DTZ001,PERF403,RUF001,RUF022,RUF059,RUF100,S112,S314,S606,S607,TRY004,TRY301,TRY401 --output-format json
```

Allowed:

- exact `--select` for the candidate pool;
- JSON output for local parsing;
- summarized, repo-relative counts in contract/review artifacts.

Forbidden:

- `--preview`;
- `--fix`;
- `--unsafe-fix`;
- broad families such as `B`, `S`, `TRY`, `RUF`, `ALL`;
- committed raw Ruff JSON or raw terminal output;
- treating findings as proof of product bugs or security issues.

## Current Crosscheck Evidence

Measured ref:

```yaml
repository: Tahjali11/Mythic-Edge
branch: codex/ruff-stable-runtime-security-crosscheck-631
base_ref: origin/main
measured_commit: 048e31146f185840f032ec3ff45f93e6822b8fce
ruff_version: ruff 0.15.12
preview_enabled: false
autofix_used: false
unsafe_fix_used: false
command_exit_code: 1
total_findings: 86
```

Exit code `1` is expected for this read-only crosscheck because the selected
rules currently have findings. The command produced parseable JSON and no
unknown-rule error, so every candidate code is active in stable non-preview
Ruff 0.15.12.

Current finding counts:

| Rule | Current count | Stable active? | Primary surface summary |
| --- | ---: | --- | --- |
| `B009` | 24 | yes | local app import jobs and surface-authorization tooling |
| `DTZ001` | 1 | yes | test-only datetime usage |
| `PERF403` | 1 | yes | parser-adjacent Arena id validation |
| `RUF001` | 2 | yes | parser-adjacent card/catalog text |
| `RUF022` | 2 | yes | package export ordering |
| `RUF059` | 3 | yes | parser-adjacent GRP candidates and local environment tooling |
| `RUF100` | 17 | yes | runtime status API, tests, and tools |
| `S112` | 1 | yes | local launcher tooling |
| `S314` | 2 | yes | quality tools parsing local coverage XML |
| `S606` | 2 | yes | local launcher process calls |
| `S607` | 17 | yes | local launcher, local-environment tooling, tests, and report helpers |
| `TRY004` | 9 | yes | parser-adjacent card/deck/hand validation and CWE profile tooling |
| `TRY301` | 3 | yes | tests and security-quality summary tooling |
| `TRY401` | 2 | yes | parser runtime and stream exception logging |

Stale-source note: #627 listed `RUF100` as 7 findings from the earlier preview
report context. Current stable non-preview evidence at `048e311` reports 17.
Future roles must use fresh exact-code evidence rather than copying #627
counts.

## Path Evidence By Rule

| Rule | Repo-relative findings |
| --- | --- |
| `B009` | 19 in `src/mythic_edge_parser/local_app/import_jobs.py`; 5 in `tools/check_surface_authorization.py` |
| `DTZ001` | 1 in `tests/test_app_extractors.py` |
| `PERF403` | 1 in `src/mythic_edge_parser/app/arena_id_validation.py` |
| `RUF001` | 1 in `src/mythic_edge_parser/app/card_catalog.py`; 1 in `src/mythic_edge_parser/app/grp_id_candidates.py` |
| `RUF022` | 1 in `src/mythic_edge_parser/__init__.py`; 1 in `src/mythic_edge_parser/log/__init__.py` |
| `RUF059` | 2 in `src/mythic_edge_parser/app/grp_id_candidates.py`; 1 in `tools/check_local_environment.py` |
| `RUF100` | 7 in `src/mythic_edge_parser/app/status_api.py`; 1 in `tests/test_evidence_ledger.py`; 9 across tools under `tools/` |
| `S112` | 1 in `tools/auto_launcher/manasight_launcher_auto.py` |
| `S314` | 1 in `tools/check_coverage_floor.py`; 1 in `tools/generate_protected_surface_coverage_report.py` |
| `S606` | 2 in `tools/auto_launcher/manasight_launcher_auto.py` |
| `S607` | 5 in tests; 5 in `tools/auto_launcher/manasight_launcher_auto.py`; 7 across local-environment/dev-app/report helper tools |
| `TRY004` | 8 across parser-adjacent app files; 1 in `tools/check_cwe_mapped_local_validation_profile.py` |
| `TRY301` | 1 in `tests/test_diagnostics.py`; 2 in `tools/generate_security_quality_summary.py` |
| `TRY401` | 1 in `src/mythic_edge_parser/app/runner.py`; 1 in `src/mythic_edge_parser/stream.py` |

Path-fed protected-surface scan over the touched path set:

```yaml
forbidden: 0
warnings: 1
warning:
  category: webhook_payload_shape
  path: src/mythic_edge_parser/app/runner.py
  rule: "Protected webhook payload surface; issue/contract must authorize this change."
```

The scanner warning comes from `TRY401` touching `runner.py`. It is a review
signal, not authorization to change that file.

## Candidate Grouping Recommendation

### Security-Adjacent Process/XML Behavior

Rules:

- `S314`
- `S606`
- `S607`

Recommendation:

```yaml
route: advisory_watch_list_with_cleanup_contract_required
promotion_ready: false
```

Why:

- `S314` touches coverage/report tooling that parses local coverage XML. It is
  security-adjacent but not evidence of an exploitable issue.
- `S606` and `S607` touch process-launching helper code. Those changes need a
  focused launcher/security contract because a mechanical cleanup could change
  Windows process behavior.
- `S607` is broad and noisy at 17 findings.

Do not promote these rules until a later issue reviews the process/XML threat
model, validates behavior, and reaches zero baseline.

### Control-Flow And Exception-Handling Clarity

Rules:

- `S112`
- `TRY004`
- `TRY301`
- `TRY401`

Recommendation:

```yaml
route: split_before_cleanup
promotion_ready: false
```

Why:

- `TRY301` is small and tool/test-focused, so it may be a plausible later
  cleanup candidate.
- `TRY004` touches parser-adjacent card, deck, GRP, and hand confirmation
  code. It requires protected-surface review before implementation.
- `TRY401` touches `runner.py` and `stream.py`, which are parser/runtime
  surfaces. It should not be changed without a runtime contract.
- `S112` touches launcher tooling and should travel with launcher/process
  review, not as a standalone gate.

### Runtime Correctness And Stale-Suppression Cleanup

Rules:

- `B009`
- `DTZ001`
- `RUF100`

Recommendation:

```yaml
route: cleanup_required_before_promotion
promotion_ready: false
```

Why:

- `B009` has 24 findings, mostly in local app import jobs. It may be valuable,
  but it is too concentrated in local app/security-adjacent code to promote
  without cleanup and review.
- `DTZ001` has one test-only finding and is a small possible cleanup.
- `RUF100` has 17 stale-suppression findings across runtime status, tests, and
  tools. It is a good cleanup candidate, but not a promotion candidate while
  nonzero.

### Lower-Risk Maintainability, Performance, And Text Hygiene

Rules:

- `PERF403`
- `RUF001`
- `RUF022`
- `RUF059`

Recommendation:

```yaml
route: small_future_cleanup_candidates_with_human_review
promotion_ready: false
```

Why:

- `PERF403`, `RUF022`, and `RUF059` are small enough for a later exact-code
  cleanup issue.
- `RUF001` touches user-visible or domain text in card/catalog code. It needs
  human semantic review before changing string characters.
- Parser-adjacent files still require focused tests and protected-surface
  awareness.

## Candidate Status Table

| Rule | Status | Later route |
| --- | --- | --- |
| `B009` | cleanup_needed_before_any_promotion | Later local-app/security-adjacent cleanup issue; split from broad promotion. |
| `DTZ001` | small_cleanup_candidate | Could be grouped with low-risk test/tool cleanup, then exact zero-baseline promotion after review. |
| `PERF403` | small_cleanup_candidate | Could be grouped with low-risk parser-adjacent maintainability cleanup after focused test review. |
| `RUF001` | watch_list_human_text_review_required | Do not mechanically edit domain/user-visible text. |
| `RUF022` | small_cleanup_candidate | Plausible package-surface cleanup before promotion. |
| `RUF059` | small_cleanup_candidate_with_parser_review | Plausible cleanup, but parser-adjacent GRP evidence needs focused tests. |
| `RUF100` | cleanup_needed_before_any_promotion | Good cleanup candidate, but count is nonzero and spread across runtime/tools/tests. |
| `S112` | watch_list_launcher_review_required | Keep with launcher/process-control review. |
| `S314` | advisory_watch_list_security_review_required | Do not claim security issue; review local XML parser inputs before cleanup. |
| `S606` | watch_list_process_review_required | Process-launch behavior is sensitive; no promotion before focused contract. |
| `S607` | too_broad_for_next_tranche | High count and process/path semantics; split and review before cleanup. |
| `TRY004` | cleanup_candidate_protected_review_required | Parser-adjacent exception semantics require focused tests and review. |
| `TRY301` | small_cleanup_candidate | Plausible later tool/test cleanup candidate. |
| `TRY401` | watch_list_runtime_review_required | Touches runtime protected surfaces; do not promote before runtime review. |

## Promotion Boundary

No rule in this pool is ready for blocking promotion now.

A later exact-code promotion requires all of these:

1. Fresh current-base stable non-preview Ruff evidence.
2. Exact rule code scope only.
3. Zero findings after a reviewed cleanup issue, or zero findings before
   promotion.
4. No `--preview`, broad family, `ALL`, autofix, or unsafe-fix.
5. Protected-surface classification for every touched path.
6. Focused tests proving behavior is preserved.
7. Codex E review confirming no parser/product/runtime behavior drift.
8. Codex G confirmation that CI and tracker state are current before merge.

Nonzero rules must go through cleanup first. This contract is not a cleanup
contract.

## Advisory Versus Promotion Boundary

Advisory evidence may be used to:

- name current finding counts;
- identify path families;
- route future issue scope;
- decide whether a rule is too noisy or risky.

Advisory evidence must not:

- alter `pyproject.toml`;
- alter `.github/workflows/repo-checks.yml`;
- alter `tools/run_repo_checks.ps1`;
- create a CI gate;
- prove security/privacy readiness;
- prove parser/runtime correctness;
- justify broad cleanup;
- replace protected-surface review.

## Protected-Surface Classification Requirements

Future cleanup issues must classify touched paths before editing:

- parser truth / parser-adjacent app files;
- parser runtime files;
- local app security/privacy files;
- quality/security tooling;
- tests;
- workflow files;
- generated/private/local artifact surfaces.

Any issue touching `src/mythic_edge_parser/app/runner.py`,
`src/mythic_edge_parser/stream.py`, parser card identity surfaces, local app
import/upload paths, launcher process code, or security scanner tooling must
include focused behavior-preservation tests and path-scoped protected-surface
and secret/private-marker scans.

## Validation Requirements

For this Codex B contract:

```powershell
git diff --check -- docs\contracts\quality_ruff_stable_runtime_security_watchlist_crosscheck.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Read-only evidence commands used by Codex B:

```powershell
py -m ruff --version
py -m ruff check src tests tools --select B009,DTZ001,PERF403,RUF001,RUF022,RUF059,RUF100,S112,S314,S606,S607,TRY004,TRY301,TRY401 --output-format json
py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-a3227b6-ruff-preview-advisory-report.json
rg -n "preview|--preview|select ALL|unsafe-fix|autofix|ruff" pyproject.toml .github\workflows\repo-checks.yml tools\run_repo_checks.ps1
```

For later cleanup or promotion issues:

```powershell
git status --short --branch
py -m ruff check src tests tools --select <exact-code-or-small-exact-code-set>
py -m pytest -q <focused tests for touched behavior>
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/main
py tools\check_secret_patterns.py --base origin/main
```

If a later issue touches frontend, local app UI, launcher behavior, or
packaging, add the relevant focused checks from that contract.

## Acceptance Criteria

- The contract records current stable non-preview evidence for all #631
  candidate codes.
- The contract names current finding counts for each exact code.
- The contract records that every candidate code is active in stable Ruff
  0.15.12.
- The contract classifies touched path families and protected-surface risk.
- The contract identifies plausible later cleanup candidates.
- The contract identifies watch-list-only and too-broad candidates.
- The contract keeps every rule advisory-only for this issue.
- The contract forbids preview mode, broad families, autofix, unsafe-fix, CI
  changes, `pyproject.toml` changes, and product behavior changes.
- The contract does not claim readiness, truth, security, privacy, deploy, or
  production assurance.

## Open Questions And Risks

- Several candidates are valuable but not small enough for direct promotion:
  `B009`, `RUF100`, and `S607` should be split or cleaned before any promotion
  discussion.
- Some low-count rules touch parser-adjacent or runtime surfaces. Small count
  does not make them low risk.
- Ruff rule behavior can change across versions. Future roles must record the
  Ruff version and rerun exact commands on the current base.
- This contract does not decide whether the next #567 child should prioritize
  cleanup value, security posture, or low-churn zero-baseline promotion.

## Out Of Scope

- Implementing fixes.
- Editing `pyproject.toml`.
- Editing CI or repo-check scripts.
- Enabling preview mode.
- Running Ruff autofix or unsafe-fix.
- Promoting any rule to a blocking gate.
- Broad cleanup.
- Parser behavior changes.
- Runtime behavior changes.
- Analytics, workbook, webhook, Apps Script, Sheets, OpenAI/model-provider,
  AI/coaching, Line Tracer, production, fixture, corpus, generated/private
  artifact, or local-only artifact changes.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test.

Because this contract already performs the read-only crosscheck and no code is
implemented, the next safe step is review. After review, a future Codex A issue
can frame one narrow cleanup candidate, likely either a small low-churn
cleanup group (`DTZ001`, `PERF403`, `RUF022`, `RUF059`, `TRY301`) or a
separate higher-risk cleanup issue for `B009`, `RUF100`, `S607`, or runtime
exception rules.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/631

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/627

Contract:
docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md

Goal:
Review whether the #631 contract accurately records stable non-preview Ruff
crosscheck evidence for B009, DTZ001, PERF403, RUF001, RUF022, RUF059, RUF100,
S112, S314, S606, S607, TRY004, TRY301, and TRY401 without authorizing
implementation, preview mode, autofix, unsafe-fix, CI changes, pyproject
changes, or rule promotion.

Verify:
- current-base evidence uses stable non-preview Ruff only;
- counts match the exact-code command on current origin/main;
- RUF100 source-count drift is called out;
- protected-surface and path-family risks are classified accurately;
- no rule is promoted or treated as security/privacy/parser/release assurance;
- next routing is review first, then a future scoped issue if desired.

Suggested validation:
- git status --short --branch
- py -m ruff --version
- py -m ruff check src tests tools --select B009,DTZ001,PERF403,RUF001,RUF022,RUF059,RUF100,S112,S314,S606,S607,TRY004,TRY301,TRY401 --output-format json
- git diff --check -- docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md
- py tools/check_agent_docs.py
- path-scoped protected-surface scan over the contract
- path-scoped secret/private-marker scan over the contract

Final output:
- findings first;
- validation results;
- verdict on #631 contract;
- recommended next #567 child, if any;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/631"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/627"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_ruff_preview_advisory_candidate_routing.md"
  contract_artifact: "docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md"
  target_artifact: "docs/contract_test_reports/quality_ruff_stable_runtime_security_watchlist_crosscheck.md"
  risk_tier: "Medium workflow risk; low runtime risk because docs-only advisory routing"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/ruff-stable-runtime-security-crosscheck-631"
  measured_commit: "048e31146f185840f032ec3ff45f93e6822b8fce"
  ruff_version: "ruff 0.15.12"
  decision: "All #631 candidate codes are active stable non-preview Ruff rules, but all have nonzero findings and remain advisory/watch-list only. Future cleanup or promotion requires a separate scoped issue."
  validation:
    - "stable non-preview exact-code Ruff crosscheck run read-only"
    - "source preview report JSON parsed"
    - "normal Ruff surfaces inspected for preview/autofix/unsafe-fix"
    - "git diff --check over contract"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan over contract"
    - "path-scoped secret/private-marker scan over contract"
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
