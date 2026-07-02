# Quality Ruff Low-Churn Exact-Code Cleanup Candidate Selection Contract

## Contract Metadata

- Role: Codex B / Module Contract Writer
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/638>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/567>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/631>
- Source contract: `docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`
- Source report: `docs/contract_test_reports/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`
- Target branch: `codex/ruff-low-churn-candidate-638`
- Base ref: `origin/main`
- Measured commit for this Codex B pass: `6f876a78c5294b58111f43a364596498004fc3eb`
- Risk tier: Medium workflow risk; low runtime risk if the later cleanup stays test/tool-only

## Purpose

Select the smallest stable non-preview Ruff exact-code cleanup candidate set after
#631. This contract is a selection and routing artifact only. It does not
authorize rule promotion, CI changes, `pyproject.toml` changes, preview mode,
autofix, unsafe-fix, or broad cleanup.

The later cleanup goal is to remove a tiny set of existing low-churn findings
before any future zero-baseline or blocking-promotion issue considers those
rules. A cleanup pass is not a promotion pass.

## Observed Current Behavior

#631 measured a broader stable non-preview Ruff watch-list pool and found all
candidate rules nonzero. Issue #638 narrowed the first follow-up selection pool
to:

- `DTZ001`
- `PERF403`
- `RUF022`
- `RUF059`
- `TRY301`

Fresh current-base evidence from this Codex B pass used:

```powershell
py -m ruff check src tests tools --select DTZ001,PERF403,RUF022,RUF059,TRY301 --output-format json --exit-zero
```

The command reported 10 findings:

| Rule | Count | Current path family |
| --- | ---: | --- |
| `DTZ001` | 1 | test-only |
| `PERF403` | 1 | parser-adjacent source |
| `RUF022` | 2 | package export surfaces |
| `RUF059` | 3 | parser-adjacent source plus local environment tooling |
| `TRY301` | 3 | test/tool-only |

Finding path evidence:

| Rule | Findings |
| --- | --- |
| `DTZ001` | `tests/test_app_extractors.py` |
| `PERF403` | `src/mythic_edge_parser/app/arena_id_validation.py` |
| `RUF022` | `src/mythic_edge_parser/__init__.py`; `src/mythic_edge_parser/log/__init__.py` |
| `RUF059` | `src/mythic_edge_parser/app/grp_id_candidates.py` x2; `tools/check_local_environment.py` |
| `TRY301` | `tests/test_diagnostics.py`; `tools/generate_security_quality_summary.py` x2 |

## Selected Candidate Code Set

Selected for a later cleanup candidate pass:

- `DTZ001`
- `TRY301`

Why this set:

- The current findings are limited to tests and tools.
- The set is small: 4 total findings across 3 files.
- The cleanup should be behavior-preserving and reviewable.
- No parser source, package export surface, local app runtime surface, workbook,
  webhook, Apps Script, analytics truth, AI truth, production behavior, fixture,
  or corpus behavior needs to change.

This selected set is not approved for blocking promotion. A later promotion
issue would need fresh zero-baseline evidence after cleanup, Codex E review, and
explicit authorization to edit Ruff configuration or CI.

## Deferred Rules

| Rule | Decision | Reason |
| --- | --- | --- |
| `PERF403` | Defer to parser-adjacent cleanup issue | The finding is in `src/mythic_edge_parser/app/arena_id_validation.py`. It may be safe, but the file is parser-adjacent and should travel with focused behavior tests. |
| `RUF022` | Defer to package-surface cleanup issue | Sorting `__all__` touches package export surfaces. It is likely low-risk, but should be reviewed as an interface/package-surface cleanup. |
| `RUF059` | Defer to parser-adjacent/local-tool cleanup issue | Two findings are in `src/mythic_edge_parser/app/grp_id_candidates.py`, which is parser-adjacent card identity evidence. It needs focused parser-adjacent review before cleanup. |

Rules outside the #638 first selection pool remain deferred under #631:

- `B009`
- `RUF001`
- `RUF100`
- `S112`
- `S314`
- `S606`
- `S607`
- `TRY004`
- `TRY401`

Those rules must not be absorbed into the #638 cleanup pass.

## Required Guarantees

A later Codex C cleanup may proceed only if it preserves all of these
guarantees:

1. Only `DTZ001` and `TRY301` findings are changed.
2. No `pyproject.toml`, CI, repo-check, or Ruff rule-selection file is changed.
3. No preview mode, autofix, unsafe-fix, broad family, or `ALL` rule selection
   is used.
4. No product, parser, runtime, analytics, workbook, webhook, Apps Script,
   OpenAI/model-provider, AI/coaching, Line Tracer, production, fixture, or
   corpus behavior is changed.
5. The `DTZ001` test cleanup keeps the same assertion intent and uses explicit
   timezone-aware datetime construction where needed.
6. The `TRY301` cleanup keeps the same exception type, message expectations,
   and validation failure behavior.
7. Any touched tool code remains public-safe and does not read, print, write, or
   expose secrets, raw logs, generated artifacts, local-only artifacts, raw
   scanner output, endpoint values, workbook exports, failed-post payloads, or
   private paths.

## Protected-Surface Classification

Selected code set:

| Rule | Current files | Protected-surface status |
| --- | --- | --- |
| `DTZ001` | `tests/test_app_extractors.py` | Test-only. No protected source file expected. |
| `TRY301` | `tests/test_diagnostics.py`; `tools/generate_security_quality_summary.py` | Test/tool-only. Security summary tooling is public-safe advisory reporting code; changes must preserve non-claim and redaction behavior. |

Deferred code set:

| Rule | Current files | Protected-surface concern |
| --- | --- | --- |
| `PERF403` | `src/mythic_edge_parser/app/arena_id_validation.py` | Parser-adjacent Arena id validation. |
| `RUF022` | package `__init__.py` files | Package export ordering/interface surface. |
| `RUF059` | `src/mythic_edge_parser/app/grp_id_candidates.py`; `tools/check_local_environment.py` | Parser-adjacent GRP evidence plus local environment tooling. |

If fresh Codex C evidence shows `DTZ001` or `TRY301` now touches protected
parser/runtime/local-app/security surfaces beyond the paths above, Codex C must
stop and route back to Codex B.

## Current-Base Ruff Evidence Required

Before making any cleanup edits, Codex C must rerun:

```powershell
py -m ruff check src tests tools --select DTZ001,TRY301 --output-format json --exit-zero
```

Codex C must record:

- Ruff version;
- branch and commit;
- exact finding count by code;
- exact path list by code;
- whether any finding paths differ from this contract;
- whether any finding touches protected surfaces.

Codex C must stop before editing if:

- either selected rule is not active in stable non-preview Ruff;
- the selected findings are no longer limited to the expected test/tool paths;
- the finding count expands materially;
- cleanup would require changing parser source, runtime source, local app
  behavior, product behavior, `pyproject.toml`, CI, or validation tooling
  configuration;
- cleanup requires preview mode, autofix, unsafe-fix, broad families, or `ALL`;
- cleanup would create readiness, security, privacy, parser truth, analytics
  truth, AI truth, release, deploy, or production claims.

After cleanup, Codex C should verify selected-code cleanup with:

```powershell
py -m ruff check src tests tools --select DTZ001,TRY301
```

That command should pass for the selected exact-code set before Codex C routes
to review. Passing this command still does not authorize promotion.

## Validation Requirements For Later Codex C

Codex C should run the smallest focused validation first:

```powershell
py -m pytest -q tests/test_app_extractors.py tests/test_diagnostics.py tests/test_generate_security_quality_summary.py
```

If `tests/test_generate_security_quality_summary.py` is not present, Codex C
must inspect existing tests for `tools/generate_security_quality_summary.py` and
run the closest focused security-summary tests. If no focused tests exist, Codex
C must either add behavior-preserving focused tests or route back for scope
clarification before changing tool exception flow.

Codex C should also run:

```powershell
py -m ruff check src tests tools --select DTZ001,TRY301
py -m ruff check src tests tools
git diff --check
py tools/check_agent_docs.py
```

Codex C must run path-scoped protected-surface and secret/private-marker scans
over every changed path:

```powershell
git diff --name-only --diff-filter=ACMRTUXB origin/main...HEAD |
  py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin

git diff --name-only --diff-filter=ACMRTUXB origin/main...HEAD |
  py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

If Codex C changes only unstaged working-tree files before committing, it may
feed the explicit changed path list to the same scanners instead of relying on
`origin/main...HEAD`.

## Promotion Boundary

This contract does not authorize promotion of `DTZ001` or `TRY301`.

A future promotion issue would need:

1. reviewed cleanup merged or otherwise current on the intended base;
2. zero findings for the exact rule code or codes on fresh current base;
3. Codex E confirmation that behavior did not drift;
4. explicit authorization to edit `pyproject.toml`, repo checks, or CI;
5. Codex G confirmation that the target branch and tracker state are current.

No branch coverage, security assurance, privacy assurance, release readiness,
deploy readiness, production readiness, parser correctness, analytics truth, AI
truth, or coaching truth should be inferred from a Ruff cleanup.

## Out Of Scope

- Implementing cleanup in this Codex B pass.
- Editing `pyproject.toml`.
- Changing CI or repo checks.
- Promoting Ruff rules.
- Enabling preview mode.
- Running Ruff autofix or unsafe-fix.
- Broad cleanup.
- Changing parser behavior, parser state final reconciliation, parser event
  classes, match/game identity, deduplication, analytics truth, workbook
  behavior, webhook behavior, Apps Script behavior, OpenAI/model-provider
  behavior, AI/coaching behavior, Line Tracer behavior, production behavior,
  fixtures, or corpus status.
- Touching raw logs, generated artifacts, local-only artifacts, workbook
  exports, failed posts, secrets, credentials, endpoint values, tokens, private
  paths, or private scanner output.

## Acceptance Criteria

- This contract selects `DTZ001` and `TRY301` only.
- Current-base stable non-preview Ruff evidence is recorded.
- `PERF403`, `RUF022`, and `RUF059` are explicitly deferred.
- Later implementation is limited to cleanup consideration, not promotion.
- Protected-surface classification is documented.
- Validation and stop conditions are documented.
- The next role is Codex C only if the user authorizes implementation.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/638

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md

Goal:
Compare the current repo against the contract and, only if fresh evidence still
matches the contract, perform the tiny behavior-preserving Ruff cleanup for
DTZ001 and TRY301 findings only.

Before editing:
- Confirm branch and git status.
- Rerun:
  py -m ruff check src tests tools --select DTZ001,TRY301 --output-format json --exit-zero
- Confirm findings are limited to the expected test/tool paths.
- Stop and route back to Codex B if finding paths, counts, or protected-surface
  exposure materially differ.

Allowed implementation scope:
- Fix DTZ001 and TRY301 findings only.
- Preserve test intent, exception types, exception messages, and public-safe
  security-summary behavior.
- Add focused behavior-preserving tests only if needed to make the cleanup safe.

Do not:
- edit pyproject.toml;
- change CI or repo checks;
- promote any Ruff rule;
- enable preview mode;
- run autofix or unsafe-fix;
- clean up PERF403, RUF022, RUF059, or any other rule;
- change parser behavior, runtime behavior, local app behavior, analytics truth,
  workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior,
  production behavior, fixtures, or corpus status;
- touch raw logs, generated artifacts, local-only artifacts, workbook exports,
  failed posts, secrets, credentials, endpoint values, tokens, private paths, or
  private scanner output.

Validation:
- py -m pytest -q tests/test_app_extractors.py tests/test_diagnostics.py tests/test_generate_security_quality_summary.py
- If the security-summary focused test file is absent, run the closest existing
  focused tests or add behavior-preserving tests before changing tool exception
  flow.
- py -m ruff check src tests tools --select DTZ001,TRY301
- py -m ruff check src tests tools
- git diff --check
- py tools/check_agent_docs.py
- path-scoped protected-surface scan for changed files
- path-scoped secret/private-marker scan for changed files

Output:
- comparison artifact or implementation handoff path
- files changed
- selected-code Ruff before/after evidence
- validation run
- protected-surface and secret/private-marker scan results
- remaining risks
- next recommended role: Codex E
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/638"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/631"
  contract_artifact: "docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md"
  selected_candidate_codes:
    - "DTZ001"
    - "TRY301"
  deferred_candidate_codes:
    - "PERF403"
    - "RUF022"
    - "RUF059"
  branch: "codex/ruff-low-churn-candidate-638"
  base_ref: "origin/main"
  risk_tier: "Medium workflow risk; low runtime risk if cleanup remains test/tool-only"
  enforcement_authorized: false
  ci_change_authorized: false
  pyproject_change_authorized: false
  preview_mode_authorized: false
  autofix_authorized: false
  next_recommended_role: "Codex C: Module Implementer / comparison thread"
```
