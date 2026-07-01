# Quality Ruff Third Logging Exact-Code Candidate Selection Contract

## Module

`quality_ruff_third_logging_exact_code_candidate_selection`

This contract selects the third narrow Ruff ratchet tranche for Mythic Edge.
Ruff is a Python static-analysis tool: it checks source files for known bug,
style, and maintainability patterns without running the application.

This tranche is limited to exact logging/runtime visibility rule codes that are
clean on the current base. It does not implement the promotion, edit
`pyproject.toml`, change CI, run autofix, or change product behavior.

## Source Artifacts

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/618>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/567>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source advisory report:
  `docs/quality_reports/ruff_advisory/2026-07-01-62bc9c2-ruff-advisory-report.json`
- Prior Ruff contracts:
  - `docs/contracts/quality_ruff_advisory_zero_baseline_design.md`
  - `docs/contracts/quality_ruff_current_advisory_measurement_report.md`
  - `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
  - `docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md`
  - `docs/contracts/quality_ruff_second_bug_risk_tranche.md`
- Prior Ruff reports:
  - `docs/contract_test_reports/quality_ruff_zero_baseline_candidate_selection.md`
  - `docs/contract_test_reports/quality_ruff_first_exact_code_dry_run.md`
  - `docs/contract_test_reports/quality_ruff_first_exact_code_blocking_promotion.md`
  - `docs/contract_test_reports/quality_ruff_second_bug_risk_tranche.md`
  - `docs/contract_test_reports/quality_ruff_current_advisory_remeasurement_after_second_tranche.md`
- Repo workflow authority:
  - `AGENTS.md`
  - `docs/agent_rules.yml`
  - `docs/agent_constitution.md`
  - `docs/codex_module_workflow.md`
  - `docs/agent_threads/module_contract.md`
  - `docs/templates/module_contract.md`

## Role And Scope

Role performed: Codex B / Module Contract Writer.

This is a contract-only artifact. It does not implement code, promote Ruff
rules, edit `pyproject.toml`, change GitHub Actions, run Ruff autofix, run
unsafe-fix, rerun the all-rules Ruff advisory measurement, perform broad
cleanup, or change product behavior.

## Owning Layer

Owning layer: Quality / Governance.

Ruff owns static-analysis findings only for the exact command, configured rule
selection, ref/commit, Ruff version, and scan scope. Ruff output does not own
parser truth, fixture authority, corpus status, production readiness,
security/privacy assurance, analytics truth, AI truth, or coaching truth.

## Internal Project Area

Primary: Quality / Governance.

Supporting area: CI / Tooling, as future implementation only.

## Truth Owner

The truth owner for this contract is repo quality governance. This contract may
define which exact Ruff rule codes are eligible for a later blocking
validation gate. It does not prove runtime behavior, parser correctness,
security posture, release readiness, or production readiness.

## Bridge-Code Status

`not_bridge_code`

This contract is workflow/tooling policy. It does not bridge parser facts into
downstream systems and does not change runtime behavior.

## Files Owned By This Contract

- `docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md`

Future Codex C work may reference or change these files only within the
implementation scope defined below:

- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tests/test_run_repo_checks_script.py`
- `docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md`

## Observed Current Behavior

Tracker #567 remains open for earned Ruff rule promotion. Roadmap #568 remains
open for the broader quality-loop sequence.

#601 / PR #606 promoted the first exact DTZ tranche. #608 / PR #611 promoted
the second exact `B` bug-risk tranche. #613 / PR #616 completed the sanitized
Ruff advisory remeasurement after the second tranche.

Current committed Ruff selection in `pyproject.toml` includes only:

```toml
select = [
  "E",
  "F",
  "I",
  "B006",
  "B008",
  "B012",
  "B023",
  "B904",
  "DTZ002",
  "DTZ003",
  "DTZ004",
  "DTZ006",
  "DTZ011",
  "DTZ012",
  "DTZ901",
]
```

Current CI and local repo-check lint scope both run:

```powershell
py -m ruff check src tests tools
```

The source advisory report records:

```yaml
schema_version: quality_ruff_advisory_report.v1
repository: Tahjali11/Mythic-Edge
branch_or_ref: origin/main
commit: 62bc9c2a61b414d5e168148cb078a44842fc42bc
ruff_version: "ruff 0.15.12"
scan_scope:
  - src
  - tests
  - tools
totals:
  findings: 17984
  triggered_rule_codes: 116
  zero_baseline_rule_codes: 840
```

The source report lists every recommended candidate code as:

```yaml
count: 0
disposition: zero_baseline_candidate
protected_surface_impact: none
```

Current-base validation passed during this Codex B pass:

```powershell
py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
```

Result:

```text
All checks passed!
```

Issue #618 also records that selecting `LOG004` produces this Ruff warning:

```text
warning: Selection `LOG004` has no effect because preview is not enabled.
```

Therefore `LOG004` is excluded even though the sanitized report lists it as a
zero-baseline candidate.

## Contract Summary

The third Ruff tranche should use exact logging/runtime visibility rule codes.
It is eligible to proceed directly to Codex C blocking-promotion implementation
after fresh current-base validation.

No additional advisory dry-run is required because:

- the candidate set is exact-code only;
- the candidate set is zero-baseline in the latest sanitized advisory report;
- the candidate set passes current-base exact-code validation;
- no source cleanup is required;
- no autofix, unsafe-fix, broad family, or preview mode is required;
- the precedent from #608 allows a later Codex C implementation after fresh
  validation for a clean exact-code tranche.

```yaml
recommended_promotion_posture: blocking_exact_code_promotion_after_fresh_codex_c_validation
additional_advisory_dry_run_required: false
codex_b_implemented_behavior: false
```

## Candidate Exact-Code Decision

The following exact rule codes are approved as the third logging/runtime
visibility candidate tranche, subject to fresh Codex C validation:

| Rule | Ruff title | Decision | Reason |
| --- | --- | --- | --- |
| `G001` | `logging-string-format` | Candidate for blocking promotion | Prevents eager `.format()` logging interpolation. |
| `G002` | `logging-percent-format` | Candidate for blocking promotion | Prevents eager percent-format logging interpolation. |
| `G003` | `logging-string-concat` | Candidate for blocking promotion | Prevents eager string concatenation in logging calls. |
| `G004` | `logging-f-string` | Candidate for blocking promotion | Prevents eager f-string interpolation in logging calls. |
| `G010` | `logging-warn` | Candidate for blocking promotion | Prevents deprecated `logging.warn` use. |
| `G101` | `logging-extra-attr-clash` | Candidate for blocking promotion | Prevents `extra` keys that clash with built-in logging fields. |
| `G201` | `logging-exc-info` | Candidate for blocking promotion | Keeps exception logging context explicit. |
| `G202` | `logging-redundant-exc-info` | Candidate for blocking promotion | Prevents redundant exception logging context. |
| `LOG001` | `direct-logger-instantiation` | Candidate for blocking promotion | Encourages supported logger construction patterns. |
| `LOG002` | `invalid-get-logger-argument` | Candidate for blocking promotion | Prevents invalid `logging.getLogger` arguments. |
| `LOG007` | `exception-without-exc-info` | Candidate for blocking promotion | Keeps exception reporting from losing traceback context. |
| `LOG009` | `undocumented-warn` | Candidate for blocking promotion | Prevents ambiguous deprecated warning/logging usage. |
| `LOG014` | `exc-info-outside-except-handler` | Candidate for blocking promotion | Prevents exception-info use where there is no active exception. |
| `LOG015` | `root-logger-call` | Candidate for blocking promotion | Avoids root logger calls that make diagnostics harder to attribute. |

These rules are useful for Mythic Edge because the project depends heavily on
diagnostics, sanitized reports, local app status, live capture status, scanner
output, and workflow handoffs. Logging mistakes make those surfaces harder to
debug even when parser behavior is unchanged.

## Excluded Code Decision

`LOG004` must remain excluded from this tranche.

Reasons:

- Ruff reports that selecting `LOG004` has no effect unless preview mode is
  enabled.
- Preview mode is not authorized by #618 or this contract.
- A no-effect selection is not a meaningful blocking gate.
- Enabling preview mode would be broader than exact-code promotion.

Future reconsideration of `LOG004` requires a separate issue or contract that
explicitly evaluates Ruff preview mode or a future Ruff version where `LOG004`
is no longer preview-only.

## Deferred Codes And Families

This contract defers:

- `LOG004`;
- broad `G`;
- broad `LOG`;
- `ALL`;
- preview mode;
- exploratory `ASYNC`, `S`, `RET`, and `TRY` spot-check groups from issue
  #618;
- any style-only or high-volume cleanup not named in the candidate table;
- any rule with current findings or protected-surface review requirements.

The `S` security-like rules should route through the security workflow or a
separate contract before promotion. `TRY200` remaps to `B904`, which is already
promoted by #608 / PR #611, so it is not a new candidate here.

## Implementation Boundary For Codex C

Codex C may implement the promotion only after repeating current-base
validation. The expected implementation shape is:

1. Confirm the branch is fresh enough against `origin/main`.
2. Run the exact candidate check before editing:

```powershell
py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
```

3. If the exact candidate check passes, add only the selected exact codes to
   `pyproject.toml`.
4. Keep existing selected codes intact.
5. Keep `.github/workflows/repo-checks.yml` using
   `py -m ruff check src tests tools`.
6. Keep `tools/run_repo_checks.ps1` using
   `py -m ruff check src tests tools`.
7. Update `tests/test_run_repo_checks_script.py` only if a concrete local
   repo-check helper change requires it.
8. Produce
   `docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md`.

If current-base validation fails, Codex C must not add the rules. It should
write the comparison handoff with the first failing rule, command result, and
branch freshness state, then route back to Codex B or A.

## Required Guarantees

Future implementation must guarantee:

- only exact codes `G001`, `G002`, `G003`, `G004`, `G010`, `G101`, `G201`,
  `G202`, `LOG001`, `LOG002`, `LOG007`, `LOG009`, `LOG014`, and `LOG015` are
  added;
- existing selected rules remain present;
- `LOG004` remains excluded;
- broad `G`, broad `LOG`, `ALL`, preview mode, autofix, unsafe-fix, and broad
  cleanup are not introduced;
- local and CI Ruff scope remains `src tests tools`;
- native Ruff output remains the failure surface unless Codex C proves a
  helper is needed and routes back to Codex B;
- no runtime, parser, analytics, workbook, AI, coaching, production, security,
  privacy, fixture, corpus, or readiness claim is made from this lint
  promotion.

## CI Promotion Blockers

Codex C, E, F, or G must block promotion when any of these are true:

- current-base exact-code validation was not run;
- current-base exact-code validation reports any finding;
- the branch is stale and validation was not repeated after refresh;
- source cleanup is required before the gate can be clean;
- implementation adds `LOG004`, broad `G`, broad `LOG`, `ALL`, or preview mode;
- implementation uses Ruff autofix, fix-only, or unsafe-fix;
- implementation reruns or depends on an all-rules advisory scan;
- implementation changes CI beyond preserving the existing Ruff command scope;
- implementation commits raw Ruff JSON, raw terminal logs, source snippets,
  local-only files, generated artifacts, private paths, secrets, credentials,
  tokens, webhook URLs, spreadsheet IDs, or environment values;
- implementation changes parser behavior, fixtures, corpus status, analytics
  truth, AI truth, coaching truth, workbook behavior, Apps Script behavior,
  Google Sheets behavior, output transport, production behavior, or security
  scanner behavior;
- implementation claims security/privacy assurance, parser correctness,
  release readiness, deploy readiness, or production readiness.

## Validation Requirements

For this Codex B contract:

```powershell
git status --short --branch --untracked-files=all
py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
py -m ruff check src tests tools
git diff --check -- docs\contracts\quality_ruff_third_logging_exact_code_candidate_selection.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

For Codex C implementation:

```powershell
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
py -m ruff check src tests tools
py -m pytest -q tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
```

Codex C must also run path-scoped protected-surface and secret/private-marker
scans over changed files.

For Codex E:

- verify the implementation adds exact codes only;
- verify `LOG004`, broad `G`, broad `LOG`, `ALL`, and preview mode remain
  excluded;
- verify no autofix or unsafe-fix was used;
- verify current-base exact-code validation passed;
- verify local and CI Ruff scope remains `src tests tools`;
- verify existing selected `E`, `F`, `I`, `DTZ`, and `B` codes remain intact;
- verify no runtime/product/protected-surface behavior changed;
- produce
  `docs/contract_test_reports/quality_ruff_third_logging_exact_code_candidate_selection.md`.

For Codex G:

- verify target branch and explicit merge approval before any merge to `main`;
- verify CI after final push;
- close issue #618 only after reviewed implementation merges and completion
  evidence is recorded;
- update tracker #567 without closing it unless the whole Ruff tracker is
  complete.

## Protected-Surface Assessment

This Codex B contract is docs-only and touches workflow/validation policy
only.

Protected surfaces preserved:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity and deduplication;
- fixtures, snapshots, corpus status, and private evidence workflow;
- analytics truth and SQLite schema;
- workbook schema;
- webhook payload shape;
- Apps Script and Google Sheets behavior;
- output transport and production behavior;
- OpenAI/model-provider/AI/coaching behavior;
- security/privacy assurance claims;
- secrets, credentials, raw logs, generated data, runtime artifacts,
  failed-post payloads, workbook exports, and local-only artifacts.

Future `pyproject.toml` and repo-check helper changes are workflow validation
surface changes only. They must stay limited to this exact Ruff tranche.

## Out Of Scope

- Code implementation in Codex B.
- Editing `pyproject.toml` in Codex B.
- Editing CI in Codex B.
- Promoting Ruff rules in Codex B.
- Adding `LOG004`.
- Enabling broad `G`, broad `LOG`, `ALL`, or preview mode.
- Running Ruff autofix, fix-only, or unsafe-fix.
- Rerunning all-rules Ruff advisory measurement.
- Performing broad cleanup.
- Mixing coverage issue #605/#617 work into this Ruff issue.
- Security-like `S` rule promotion.
- Parser behavior, fixture, corpus, analytics, workbook, webhook, Apps Script,
  Sheets, OpenAI, AI, coaching, production, release, or deployment changes.
- Security/privacy assurance, parser correctness, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching truth
  claims.

## Acceptance Criteria

- The contract exists at
  `docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md`.
- The contract records the source advisory report metadata.
- The contract selects exactly the 14 candidate logging/runtime visibility
  rule codes.
- The contract explicitly excludes `LOG004`.
- The contract recommends direct Codex C implementation after fresh
  current-base validation.
- The contract defines CI promotion blockers.
- The contract preserves exact-code-only promotion discipline.
- The contract forbids broad families, preview mode, autofix, unsafe-fix,
  broad cleanup, and readiness/truth/assurance overclaims.
- Codex B changes only this contract artifact.

## Unknowns And Suspected Gaps

Unknowns:

- Whether `origin/main` will advance before Codex C, E, F, or G handles the
  tranche.
- Whether concurrent work will introduce one of the selected logging findings
  before merge.
- Whether native Ruff output will be clear enough for every future failure.

Suspected gaps:

- No candidate-set blocking gap was found in this Codex B pass.
- The main risk is stale validation evidence, not current rule suitability.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/618

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/ruff-next-tranche-567

Base:
origin/main

Contract:
docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md

Goal:
Compare the current Ruff configuration, CI lint command, local repo-check
helper, prior Ruff contracts/reports, and source advisory report against the
contract. If current-base validation still passes, implement the third
logging/runtime visibility exact-code Ruff blocking promotion for exactly:

G001, G002, G003, G004, G010, G101, G201, G202, LOG001, LOG002, LOG007,
LOG009, LOG014, LOG015.

Before editing:
- Confirm branch and git status.
- Confirm whether the branch is still even with `origin/main`.
- Run `py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015`.
- Run `py -m ruff check src tests tools`.
- Inspect `pyproject.toml`, `.github/workflows/repo-checks.yml`, `tools/run_repo_checks.ps1`, and `tests/test_run_repo_checks_script.py`.

Do:
- Create `docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md`.
- If validation is fresh and passing, add exactly the selected 14 rule codes to the Ruff selected-code list in `pyproject.toml`.
- Preserve existing selected codes.
- Keep CI and local lint scope at `src tests tools`.
- Update local repo-check helper tests only if a scoped implementation change requires it.

Do not:
- Add `LOG004`.
- Enable broad `G`, broad `LOG`, `ALL`, or preview mode.
- Run Ruff autofix, fix-only, or unsafe-fix.
- Rerun all-rules Ruff advisory measurement.
- Perform broad cleanup.
- Change CI unless inspection proves the existing CI lint command has drifted from the repo-approved path scope.
- Change parser behavior, fixtures, corpus status, analytics truth, AI truth, coaching truth, workbook behavior, Apps Script/Sheets behavior, production behavior, security/privacy assurance, release readiness, or deploy readiness.
- Target main directly without explicit user approval.
- Close tracker #567.

Validation:
- py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
- py -m ruff check src tests tools
- py -m pytest -q tests\test_run_repo_checks_script.py
- git diff --check
- py tools\check_agent_docs.py

Also run path-scoped protected-surface and secret/private-marker scans over changed files.

Final handoff must include:
- role performed
- issue/tracker/roadmap
- contract artifact used
- implementation handoff produced
- files changed
- candidate codes promoted
- excluded code decision for `LOG004`
- validation results
- protected-surface status
- secret/private-marker status
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/618"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/quality_reports/ruff_advisory/2026-07-01-62bc9c2-ruff-advisory-report.json"
  target_artifact: "docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md"
  contract_artifact: "docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md"
  risk_tier: "Medium workflow risk; low runtime risk"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/ruff-next-tranche-567"
  candidate_codes:
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
  recommended_promotion_posture: "blocking exact-code promotion after fresh Codex C validation"
  validation:
    - "git status --short --branch --untracked-files=all"
    - "py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015"
    - "py -m ruff check src tests tools"
    - "git diff --check -- docs\\contracts\\quality_ruff_third_logging_exact_code_candidate_selection.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not change pyproject.toml or CI in Codex B."
    - "Do not enable broad G, broad LOG, ALL, preview mode, autofix, or unsafe-fix."
    - "Do not include LOG004."
    - "Do not claim security/privacy/release/production/parser/analytics/AI readiness."
```
