# Quality Ruff Zero-Baseline Candidate Selection Contract

## Module

`quality_ruff_zero_baseline_candidate_selection`

This contract selects the first small set of exact Ruff rule codes that Mythic
Edge may review for future zero-baseline promotion. A zero-baseline rule is an
exact Ruff rule code that reported zero findings for a named commit, Ruff
version, command, and scan scope.

This contract does not make Ruff more blocking by itself.

## Source Artifacts

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/596>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/567>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source report issue: <https://github.com/Tahjali11/Mythic-Edge/issues/588>
- Source report PR: <https://github.com/Tahjali11/Mythic-Edge/pull/592>
- Source report artifact:
  `docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json`
- Prior contracts and handoffs:
  - `docs/contracts/quality_ruff_advisory_zero_baseline_design.md`
  - `docs/contracts/quality_ruff_current_advisory_measurement_report.md`
  - `docs/implementation_handoffs/quality_ruff_sanitized_advisory_report_execution.md`

## Role And Scope

Role performed: Codex B / Module Contract Writer.

This is a contract-only artifact. It does not implement code, edit
`pyproject.toml`, change CI, promote Ruff to a blocking gate, run Ruff autofix,
run unsafe fixes, perform broad cleanup, or rerun the all-rules Ruff advisory
scan.

## Truth Ownership

Ruff owns only static-analysis findings for the exact command, ref/commit,
Ruff version, and scan scope used. A Ruff zero-baseline result does not own
parser truth, fixture authority, corpus status, production readiness,
security/privacy assurance, analytics truth, AI truth, or coaching truth.

## Observed Current Behavior

Current blocking Ruff configuration in `pyproject.toml` is narrow:

```toml
[tool.ruff.lint]
select = ["E", "F", "I"]
```

Current GitHub Actions behavior runs:

```powershell
py -m ruff check src tests tools
```

Current local repo-check behavior runs:

```powershell
py -m ruff check src tests
```

No current committed config promotes the source report's zero-baseline
candidates.

The source report records:

```yaml
measured_commit: 51d5d8352c10204663d904765a8820bb464a52ac
ruff_version: "ruff 0.15.12"
scan_command: "python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json"
rule_summaries: 956
triggered_exact_rule_codes: 115
total_findings: 17665
zero_baseline_candidates: 841
advisory_rules: 34
protected_surface_review_required_rules: 81
ruff_blocking_promotion_authorized: false
ruff_autofix_authorized: false
raw_ruff_json_committed: false
```

Current inspection for this contract observed the worktree at
`5ab26801fa2713537f538c6f43b3bd38d2e5a6f1`. Therefore the source report is
the authoritative sanitized evidence for #588, but it is stale for direct
current-base promotion until a later thread runs the exact candidate check on
the current base.

## Contract Summary

Mythic Edge may use the #588 sanitized report to select a small first review
tranche, but it must not promote any rule directly from the report.

Recommended first tranche:

```yaml
first_tranche_exact_codes:
  - DTZ002
  - DTZ003
  - DTZ004
  - DTZ006
  - DTZ011
  - DTZ012
  - DTZ901
selection_status: candidate_for_later_exact_code_promotion_review
blocking_promotion_authorized_by_this_contract: false
```

Plain English: the first safe tranche should focus only on exact datetime/time
zone rules that have zero findings and no protected-surface impact in the
sanitized report. This is smaller and safer than promoting broad families like
`B`, `S`, `PL`, `ANN`, `D`, `PTH`, `RUF`, or `ALL`.

## First-Tranche Candidate Policy

An exact Ruff code may enter the first tranche only when all are true:

1. The sanitized report count is `0`.
2. The sanitized report disposition is `zero_baseline_candidate`.
3. The sanitized report protected-surface impact is `none`.
4. The code is exact, not a broad family.
5. The code is not already covered by the current blocking `E`, `F`, or `I`
   selection.
6. The code does not require cleanup to become clean.
7. The code does not require `--fix`, `--fix-only`, or `--unsafe-fixes`.
8. The code is compatible with Mythic Edge's current conventions.
9. The code can be validated with an exact-code Ruff command on the current
   base before any config or CI change.
10. The future failure message can explain the rule group without overclaiming
    security, parser, release, or production readiness.

## Selected First-Tranche Candidates

The first tranche is the exact DTZ zero-baseline subset:

| Code | Local Ruff rule title | Report count | Disposition | Protected surface |
| --- | --- | ---: | --- | --- |
| `DTZ002` | `call-datetime-today` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ003` | `call-datetime-utcnow` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ004` | `call-datetime-utcfromtimestamp` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ006` | `call-datetime-fromtimestamp` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ011` | `call-date-today` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ012` | `call-date-fromtimestamp` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ901` | `datetime-min-max` | 0 | `zero_baseline_candidate` | `none` |

Rationale:

- The tranche is small enough for exact review.
- The rule family is behavior-adjacent because Mythic Edge has parser,
  evidence, live-capture, and analytics surfaces where time handling matters.
- The exact selected codes have zero findings in the sanitized report.
- The selected codes do not require current source cleanup.
- The selected codes do not require autofix.
- The selected codes avoid broad family promotion.
- The tranche excludes the nonzero or protected-surface DTZ rules listed below.

## Deferred DTZ Rules

These DTZ rules must not be included in the first tranche:

| Code | Report count | Disposition | Protected surface | Required route |
| --- | ---: | --- | --- | --- |
| `DTZ001` | 1 | `advisory` | `none` | cleanup/review first |
| `DTZ005` | 8 | `protected_surface_review_required` | `parser_truth_surface` | protected-surface contract first |
| `DTZ007` | 1 | `protected_surface_review_required` | `parser_truth_surface` | protected-surface contract first |

## Reserve Candidate Buckets

The following exact-code buckets are clean enough to evaluate in later tranches,
but they are not selected for the first tranche because they are broader,
noisier, more style-shaped, or closer to protected-surface behavior:

- `B` exact zero candidates:
  `B002`, `B003`, `B004`, `B005`, `B006`, `B007`, `B008`, `B011`, `B012`,
  `B013`, `B014`, `B015`, `B016`, `B017`, `B018`, `B019`, `B020`, `B021`,
  `B022`, `B023`, `B024`, `B025`, `B026`, `B027`, `B028`, `B029`, `B030`,
  `B031`, `B032`, `B033`, `B034`, `B035`, `B039`, `B043`, `B901`, `B903`,
  `B904`, `B909`, `B911`, `B912`.
- `RET` exact zero candidates:
  `RET501`, `RET502`, `RET503`, `RET505`, `RET506`, `RET507`, `RET508`.
- `PIE` exact zero candidates:
  `PIE790`, `PIE794`, `PIE796`, `PIE800`, `PIE804`, `PIE807`, `PIE808`.
- `ERA001`.
- `LOG` exact zero candidates:
  `LOG001`, `LOG002`, `LOG004`, `LOG007`, `LOG009`, `LOG014`, `LOG015`.

These reserve buckets need a later issue/contract before promotion. Do not
promote them under #596.

## Deferred Broad Families

The following remain deferred for first-tranche promotion:

- `ALL`;
- all broad families, including `B`, `S`, `PL`, `ANN`, `D`, `PTH`, `RUF`,
  `TRY`, `SIM`, `PERF`, `RET`, `PIE`, and `LOG`;
- docstring-heavy rules (`D*`);
- type-annotation-heavy rules (`ANN*`);
- path-style rules (`PTH*`) until Windows, local-artifact, and private-path
  boundaries have a dedicated review;
- security-like `S*` rules until security triage confirms exact-rule behavior;
- style, formatting, or docs rules whose first effect would be noisy churn;
- any rule with nonzero findings;
- any rule whose current report disposition is not `zero_baseline_candidate`.

## Advisory-Only Rules

The following exact codes have findings but no protected-surface label in the
sanitized report. They remain advisory-only and must not be promoted directly:

```text
A002, ANN201, B009, DTZ001, FAST002, FBT002, FLY002, FURB136,
FURB167, FURB188, ISC003, PERF403, PLR1714, PLW1510, PLW2901,
PT006, PT017, PTH201, Q000, Q003, RUF001, RUF022, RUF059, RUF100,
S112, S606, S607, SIM110, SIM118, TRY004, TRY301, TRY401, UP012,
UP034
```

Advisory-only means the finding can inform future cleanup, but it must not
block CI or local validation without a later contract and behavior-preserving
implementation/review path.

## Protected-Surface Review Rules

The following exact codes have findings and require protected-surface review
before any cleanup, promotion, or blocking behavior:

```text
ANN001, ANN002, ANN003, ANN202, ANN401, ARG001, ARG002, ARG005,
B010, B905, BLE001, C420, C901, COM812, D100, D101, D102, D103,
D104, D105, D107, D202, DTZ005, DTZ007, EM101, EM102, FBT001,
FBT003, FURB110, FURB162, FURB171, INP001, ISC001, PERF401,
PIE810, PLC0206, PLC0415, PLR0911, PLR0912, PLR0913, PLR0915,
PLR1730, PLR2004, PLW0602, PLW0603, PT007, PT011, PYI041,
RET504, RUF005, RUF043, S101, S104, S105, S108, S110, S324,
S603, S608, SIM101, SIM102, SIM103, SIM105, SIM108, SIM114,
SIM300, SLF001, T201, TC001, TC002, TC003, TC006, TID252, TRY003,
TRY300, TRY400, UP022, UP028, UP035, UP037, UP042
```

These rules are static-analysis evidence only. They do not prove
vulnerabilities, parser bugs, privacy leaks, production risk, release
readiness failure, analytics truth failure, AI truth failure, or coaching truth
failure.

## CI Promotion Blockers

A later CI or config promotion must be blocked when any of these are true:

- the candidate is a broad family rather than exact codes;
- the candidate is not one of this contract's first-tranche DTZ codes;
- current-base exact-code Ruff validation has not been run;
- current-base exact-code validation reports any finding for the selected
  codes;
- the implementation needs source cleanup before the rules are clean;
- the implementation uses or depends on `--fix`, `--fix-only`, or
  `--unsafe-fixes`;
- the implementation commits raw Ruff JSON, raw terminal logs, local absolute
  paths, private artifacts, generated artifacts, raw snippets, fix diffs, or
  local-only files;
- CI changes are not explicitly authorized by a later implementation prompt;
- failure output exposes raw Ruff JSON, local/private paths, raw source
  snippets, secrets, generated artifacts, or private markers;
- the future gate claims parser correctness, fixture promotion, corpus
  readiness, security/privacy assurance, release readiness, production
  readiness, analytics truth, AI truth, or coaching truth;
- protected surfaces would be changed without a dedicated issue/contract;
- #388 or #381 would be activated by implication.

## Required Future Validation

For this Codex B contract:

```powershell
git status --short --branch
git diff --check -- docs\contracts\quality_ruff_zero_baseline_candidate_selection.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_ruff_zero_baseline_candidate_selection.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_ruff_zero_baseline_candidate_selection.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Do not rerun the all-rules Ruff advisory measurement for this Codex B pass.

For Codex C, if a later prompt explicitly authorizes implementation:

```powershell
git status --short --branch
py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Codex C must also run path-scoped protected-surface and secret/private-marker
scans on changed files, and produce
`docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md`.

For Codex E:

- verify the implementation uses only exact first-tranche codes;
- verify current-base exact-code Ruff validation passed;
- verify existing `E`, `F`, and `I` behavior remains intact;
- verify no broad families, autofix, unsafe-fix, raw output, parser behavior,
  fixture, corpus, CI overclaim, or protected-surface change slipped in;
- produce
  `docs/contract_test_reports/quality_ruff_zero_baseline_candidate_selection.md`.

For Codex G:

- verify PR target and base freshness;
- verify CI evidence after any rebase or merge-base change;
- update #596 and tracker #567 without closing tracker #567 unless the broader
  tracker is actually complete;
- do not claim #388/#381 activation, parser readiness, security/privacy
  assurance, release readiness, production readiness, analytics truth, AI truth,
  or coaching truth.

## Protected Surfaces

This contract touches workflow and validation policy only.

Protected surfaces preserved:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity and deduplication;
- fixtures, snapshots, corpus status, and raw evidence promotion;
- #388 and #381 activation state;
- workbook schema;
- webhook payload shape;
- Apps Script and Google Sheets behavior;
- analytics truth;
- AI/coaching/model-provider behavior;
- production behavior;
- secrets, credentials, raw logs, generated data, runtime artifacts, failed
  posts, workbook exports, and local-only artifacts.

CI and validation gates are workflow protected surfaces. This contract selects
candidate rules for later review; it does not edit CI or activate a blocking
gate.

## Acceptance Criteria

- The contract records the #588 sanitized report metadata.
- The contract selects a tiny exact-code first tranche.
- The first tranche contains only zero-count `DTZ` exact codes with
  protected-surface impact `none`.
- Nonzero `DTZ` codes are deferred.
- Advisory-only rules remain advisory.
- Protected-surface-review-required rules remain review-required.
- Broad-family promotion remains forbidden.
- CI promotion blockers and validation expectations are defined.
- No code, CI, or Ruff configuration changes are made in Codex B.

## Unknowns And Suspected Gaps

- Current-base all-rules Ruff status is unknown in this Codex B pass because
  rerunning the all-rules scan is out of scope.
- Current-base exact-code DTZ status must be verified by Codex C before any
  promotion.
- The exact implementation surface is intentionally left to Codex C comparison.
  A later implementation should avoid a second unsynchronized Ruff authority.
- Failure-message polish may require a helper or documentation note if native
  Ruff output is not understandable enough.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/596

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/quality_ruff_zero_baseline_candidate_selection.md

Goal:
Compare the current Ruff config, CI workflow, repo check helper, and sanitized
Ruff advisory report against the contract. Validate the first-tranche exact
codes on the current base:

DTZ002, DTZ003, DTZ004, DTZ006, DTZ011, DTZ012, DTZ901.

If and only if explicitly authorized in this implementation prompt, implement
the smallest coherent promotion path for those exact codes. Keep broad Ruff
families, all-rules output, advisory rules, protected-surface-review-required
rules, autofix, unsafe-fix, and broad cleanup out of scope.

Do not:
- edit parser behavior;
- change fixtures, snapshots, corpus status, #388/#381 activation, production
  behavior, security/privacy assurance, analytics truth, AI truth, or coaching
  truth;
- run Ruff autofix or unsafe-fix;
- promote broad families such as ALL, DTZ, B, S, PL, ANN, D, PTH, RUF, TRY, or
  SIM;
- commit raw Ruff JSON, raw terminal logs, local absolute paths, generated
  artifacts, raw snippets, fix diffs, private artifacts, secrets, credentials,
  or local-only files;
- close tracker #567.

Validation:
- git status --short --branch
- py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
- py -m ruff check src tests tools
- focused tests only if helper/config behavior changes
- py tools/check_agent_docs.py
- git diff --check
- path-scoped protected-surface scan on changed files
- path-scoped secret/private-marker scan on changed files

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- current-base exact-code validation result
- implementation or deferral decision
- files changed
- validation run and results
- protected-surface status
- raw-artifact status
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/596"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json"
  contract_artifact: "docs/contracts/quality_ruff_zero_baseline_candidate_selection.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md"
  risk_tier: "High"
  branch: "codex/ruff-zero-baseline-readiness-567"
  selected_first_tranche:
    - "DTZ002"
    - "DTZ003"
    - "DTZ004"
    - "DTZ006"
    - "DTZ011"
    - "DTZ012"
    - "DTZ901"
  blocking_promotion_authorized_by_codex_b: false
  ruff_autofix_authorized: false
  ruff_unsafe_fix_authorized: false
  all_rules_rerun_authorized: false
  validation:
    - "git diff --check -- docs\\contracts\\quality_ruff_zero_baseline_candidate_selection.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not edit pyproject.toml in Codex B."
    - "Do not change CI in Codex B."
    - "Do not promote Ruff to a blocking gate in Codex B."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not rerun all-rules Ruff without separate authorization."
    - "Do not change parser behavior, fixtures, corpus status, #388/#381 activation, production behavior, security/privacy assurance, analytics truth, AI truth, or coaching truth."
```
