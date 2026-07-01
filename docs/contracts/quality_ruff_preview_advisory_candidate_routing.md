# Quality Ruff Preview Advisory Candidate Routing Contract

## Module

`quality_ruff_preview_advisory_candidate_routing`

Plain English: this contract interprets the merged Ruff preview-mode advisory
report from issue #619 and decides how its findings should be routed. Preview
mode is Ruff's early-access rule mode. In Mythic Edge, it is an early-warning
map only, not an enforcement gate.

This is a Codex B contract artifact only. It does not implement code, enable
Ruff preview mode, change CI, change `pyproject.toml`, promote any Ruff rule,
run autofix, run unsafe-fix, or change product behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/627
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/619
- Source PR: https://github.com/Tahjali11/Mythic-Edge/pull/626
- Contract artifact:
  `docs/contracts/quality_ruff_preview_advisory_candidate_routing.md`

## Tracker

Ruff tracker #567 remains open. This child issue does not complete the tracker.

## Owning Layer

Quality and validation tooling.

Ruff reports own advisory static-analysis evidence for a measured ref and
command. Ruff does not own parser truth, analytics truth, security assurance,
privacy assurance, release readiness, deploy readiness, production readiness,
AI truth, or coaching truth.

## Internal Project Area

Quality / validation gates.

## Truth Owner

The committed #619 sanitized preview advisory report owns only the public-safe
summary of the preview-mode Ruff measurement at its measured commit. This
contract owns only routing policy for future issue creation and candidate
selection.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
sanitized Ruff preview advisory report
  -> preview routing categories
  -> future Codex A/B issue framing, if justified
  -> later stable exact-code candidate work only after non-preview evidence
```

Forbidden reverse flow:

- Preview output must not directly change CI, `pyproject.toml`, normal repo
  checks, parser behavior, fixtures, analytics, workbook behavior, or
  production behavior.
- Preview output must not be treated as proof that a finding is a bug.
- Preview-only rules must not become blocking gates from this contract.

## Files Owned By This Contract

- `docs/contracts/quality_ruff_preview_advisory_candidate_routing.md`

This contract does not authorize edits to:

- `pyproject.toml`;
- `.github/workflows/repo-checks.yml`;
- `tools/run_repo_checks.ps1`;
- Ruff config;
- Ruff helper code;
- parser, analytics, workbook, webhook, Apps Script, Google Sheets, OpenAI,
  AI, coaching, Line Tracer, production, fixtures, corpus, or runtime code.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #567
- Issue #568
- Issue #619
- Issue #627
- PR #626
- `docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`
- `docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md`
- `docs/contract_test_reports/quality_ruff_preview_mode_advisory_discovery.md`
- `docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json`
- `tools/generate_ruff_preview_advisory_report.py`
- `tests/test_ruff_preview_advisory_report.py`
- `pyproject.toml`
- `tools/run_repo_checks.ps1`
- `.github/workflows/repo-checks.yml`

## Source Report Evidence Summary

Source report:

```text
docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json
```

Measured evidence:

```yaml
object: mythic_edge_quality_ruff_preview_advisory_report
schema_version: quality_ruff_preview_advisory_report.v1
branch_or_ref: origin/main
commit: a3227b611f4333b40a6131d710c3ea5d8a7a9ccc
ruff_version: 0.15.12
preview_enabled_for_measurement: true
preview_enabled_in_pyproject: false
preview_enabled_in_ci: false
blocking_promotion_authorized: false
autofix_authorized: false
unsafe_fix_authorized: false
exit_behavior: advisory_exit_zero
command: py -m ruff check src tests tools --preview --select ALL --exit-zero --output-format json --output-file <local-only-raw-json>
```

Totals:

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

Normal repo checks remain non-preview:

- `pyproject.toml` does not enable `preview = true`;
- `.github/workflows/repo-checks.yml` runs normal Ruff without `--preview`;
- `tools/run_repo_checks.ps1` runs normal Ruff without `--preview`.

## Routing Verdict

No preview-derived rule is ready for blocking promotion from the #619 report.

The report is useful for future routing, but it is too broad and too preview
sensitive for direct enforcement. Future Ruff work should depend on stable
non-preview evidence first, then use preview evidence as supporting context.

Recommended posture:

```yaml
preview_mode_status: advisory_only
pyproject_preview_status: not_authorized
ci_preview_status: not_authorized
normal_repo_checks_preview_status: not_authorized
blocking_promotion_status: not_authorized
autofix_status: not_authorized
unsafe_fix_status: not_authorized
future_issue_routing_status: allowed_after_review
```

## Preview-Routing Category Model

Use these routing categories for #619 report interpretation:

| Routing category | Meaning | Allowed next step |
| --- | --- | --- |
| `stable_rule_crosscheck_required` | A triggered rule is not preview-only and looks potentially useful, but it must be confirmed by normal non-preview Ruff evidence before issue creation. | Codex A may frame a later exact-code tranche after normal Ruff advisory evidence confirms the rule. |
| `watch_list_only` | A rule is useful to monitor but not ready for implementation work. | Keep in tracker/watch-list notes; do not create implementation work. |
| `defer_until_stable` | A preview-only rule has zero findings or is not stable enough for Mythic Edge enforcement. | Revisit only after Ruff stabilizes the rule or a later advisory issue authorizes remeasurement. |
| `protected_surface_review_required` | Findings may touch parser, runtime, security, privacy, workbook, analytics, or generated/private artifact surfaces. | Requires a dedicated Codex A/B issue and Codex E review before any candidate work. |
| `style_only_deferred` | Findings are primarily style/formatting or documentation style. | Defer unless a future quality issue proves low churn and clear value. |
| `too_noisy_deferred` | Finding volume or affected-file spread is too high for a safe exact-code tranche. | Do not route until a smaller subgroup or exact-code strategy exists. |
| `not_recommended` | Rule family is not aligned with current Mythic Edge conventions or risk posture. | No issue unless a future problem representation proves a concrete risk. |

`future_candidate_issue` is not a report classification by itself. It is a
later routing outcome that requires:

1. stable non-preview evidence;
2. a small exact-code scope;
3. clear current-base count;
4. low noise;
5. protected-surface classification;
6. contract and review before promotion.

## LOG004 Routing Decision

`LOG004` remains deferred until stable.

Source report evidence:

```yaml
rule_code: LOG004
count: 0
preview_only_rule: true
primary_classification: defer_until_stable
reason: Preview-only rule is measured for awareness but deferred until Ruff stabilizes the rule.
```

Decision:

```yaml
log004_route: defer_until_stable
standalone_issue_now: false
watch_list_status: passive_watch_only
blocking_candidate_status: not_ready
stable_crosscheck_required_before_reconsideration: true
```

Plain English: `LOG004` was the reason preview mode became interesting, but
the actual report shows no current findings. That means it should not receive a
standalone implementation issue now. It may be reconsidered only if Ruff
stabilizes the rule outside preview mode or a future advisory scan finds
meaningful current-base findings.

## Future Candidate Issue Criteria

A future Ruff candidate issue may be created from #619 evidence only when all
of these are true:

1. The rule is stable outside preview mode, or a new issue explicitly remains
   advisory-only.
2. A normal non-preview Ruff command confirms the current-base finding count.
3. The exact rule code is named; broad families are not used.
4. The candidate does not require `--preview`, `--fix`, or `--unsafe-fix`.
5. The candidate is small enough for focused review or explicitly split.
6. The candidate has a clear risk/value story beyond style preference.
7. Protected-surface impact is classified before implementation.
8. Parser, analytics, workbook, webhook, Apps Script, OpenAI, AI, coaching,
   production, fixture, corpus, and private-artifact boundaries are preserved.
9. A contract defines whether the rule should be advisory dry-run or blocking.

## Candidate Inputs From Stable Watch-List Rules

The #619 report surfaced stable, non-preview watch-list rules that may be
worth later issue framing only after normal Ruff crosscheck.

Higher-priority crosscheck pool:

| Rule | Count | Labels | Route |
| --- | ---: | --- | --- |
| `B009` | 24 | runtime_safety | `stable_rule_crosscheck_required` |
| `DTZ001` | 1 | runtime_safety | `stable_rule_crosscheck_required` |
| `PERF403` | 1 | runtime_safety | `stable_rule_crosscheck_required` |
| `RUF001` | 2 | runtime_safety | `stable_rule_crosscheck_required` |
| `RUF022` | 2 | runtime_safety | `stable_rule_crosscheck_required` |
| `RUF059` | 3 | runtime_safety | `stable_rule_crosscheck_required` |
| `RUF100` | 7 | runtime_safety | `stable_rule_crosscheck_required` |
| `S112` | 1 | security_adjacent | `stable_rule_crosscheck_required` |
| `S314` | 2 | security_adjacent | `stable_rule_crosscheck_required` |
| `S606` | 2 | security_adjacent | `stable_rule_crosscheck_required` |
| `S607` | 17 | security_adjacent | `stable_rule_crosscheck_required` |
| `TRY004` | 9 | runtime_safety | `stable_rule_crosscheck_required` |
| `TRY301` | 3 | runtime_safety | `stable_rule_crosscheck_required` |
| `TRY401` | 2 | runtime_safety | `stable_rule_crosscheck_required` |

These are not approved implementation candidates yet. They are a future Codex
A routing pool. Any later issue should decide whether to group related codes or
split them by risk family.

Lower-priority stable watch-list pool:

```text
A002, FAST002, FBT002, FLY002, FURB136, FURB167, FURB188,
PLR1714, PLW1510, PLW2901, PT006, PT017, PTH201, SIM110,
SIM118, UP012, UP034
```

Route: watch-list only unless a future problem representation identifies a
concrete maintenance or runtime risk.

## Triggered Preview-Only Rules

Triggered preview-only rules are not direct candidates for enforcement.

Preview-only rules with `protected_surface_review_required` include examples
such as:

```text
CPY001, ISC004, PLC1901, PLR6201, DOC201, PLR0914, S404,
PLC2701, RUF069, PLR6301, RUF031, DOC501, PLR1702, FURB118,
E302, RUF067, PLR0916, PLR0917, E265, PLW1514, PLR0904,
FURB154, B903
```

Route:

- keep advisory-only;
- do not create implementation issues from preview status alone;
- require protected-surface review before any future issue;
- require stable-rule availability or a separately approved advisory-only
  investigation before implementation.

Triggered preview-only watch-list rules:

```text
FURB113, FURB192, RUF029, RUF056, S405
```

Route: watch-list only. `RUF029`, `RUF056`, and `S405` carry runtime or
security-adjacent labels, but preview-only status still blocks enforcement.

## Zero-Baseline Preview Rules

The report contains 111 zero-baseline preview-only rule codes.

Route:

```yaml
zero_baseline_preview_rules: defer_until_stable
blocking_promotion_allowed: false
ci_change_allowed: false
pyproject_preview_allowed: false
future_use: watch future Ruff stabilization only
```

Zero-baseline preview-only codes may be useful as early awareness, but they
must not be promoted just because they are currently clean. Mythic Edge's Ruff
ratchet relies on stable, useful, low-noise exact-code promotion.

## Protected-Surface Review Requirements

Any rule classified as `protected_surface_review_required` must not go straight
to implementation.

Required review before future candidate selection:

- classify affected path families by protected surface;
- distinguish parser truth surfaces from quality/test-only surfaces;
- inspect whether fixes would touch parser state, parser event classes,
  match/game identity, deduplication, analytics truth, workbook schema,
  webhook payload shape, Apps Script behavior, generated/private artifacts, or
  secrets;
- require a contract before changing any protected surface;
- prefer advisory dry-run or focused test-hardening if the rule would require
  broad style churn.

High-volume protected-surface rules such as `S101`, `D103`, `COM812`,
`PLR2004`, `ANN401`, `ANN001`, `SLF001`, `TRY003`, `CPY001`, and broad
documentation/type/style families are not suitable for direct promotion from
this report.

## Enforcement Deferral Rules

This contract forbids:

- enabling `preview = true` in `pyproject.toml`;
- adding `--preview` to `.github/workflows/repo-checks.yml`;
- adding `--preview` to `tools/run_repo_checks.ps1`;
- promoting preview-only rules to blocking gates;
- promoting broad Ruff families;
- running Ruff autofix or unsafe-fix;
- running a fresh preview measurement in this Codex B thread;
- committing raw Ruff JSON or raw terminal output;
- claiming readiness or assurance from preview output.

Before any preview-derived finding can become blocking, a later issue must
prove:

1. current-base stable Ruff evidence exists without preview mode;
2. exact code selection passes on current base or has a small, reviewed fix
   scope;
3. protected surfaces are classified;
4. no broad family, `ALL`, autofix, or unsafe-fix is used;
5. Codex E verifies the contract, implementation, and validation evidence;
6. Codex G confirms CI and tracker state before any merge/closeout.

## Validation Requirements

For this docs-only contract:

```powershell
git diff --check -- docs\contracts\quality_ruff_preview_advisory_candidate_routing.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_ruff_preview_advisory_candidate_routing.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_ruff_preview_advisory_candidate_routing.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Optional reviewer validation:

```powershell
py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-a3227b6-ruff-preview-advisory-report.json
rg -n "preview|--preview|select ALL|unsafe-fix|autofix|ruff" pyproject.toml .github\workflows\repo-checks.yml tools\run_repo_checks.ps1
```

For later Codex A/B candidate work:

- rerun or inspect normal non-preview Ruff advisory evidence;
- do not rerun preview mode unless a new issue explicitly authorizes it;
- keep raw output local/ignored unless a sanitized report contract authorizes a
  committed artifact.

## Acceptance Criteria

- The contract cites the #619 source report and non-claims.
- The contract defines routing categories for preview-derived findings.
- The contract keeps preview mode out of CI, `pyproject.toml`, and normal repo
  checks.
- The contract states that no preview-derived rule is blocking-ready.
- The contract routes `LOG004` to `defer_until_stable`.
- The contract identifies which categories require protected-surface review.
- The contract defines future candidate issue criteria.
- The contract does not authorize enforcement, autofix, unsafe-fix, broad
  cleanup, parser behavior changes, or readiness/assurance claims.

## Open Questions And Risks

- Ruff preview-mode behavior can change across Ruff versions. Future work must
  re-check rule stability before relying on this report.
- The report includes many stable non-preview findings because the discovery
  command used `--select ALL`. Those stable findings are useful routing clues,
  but they still need normal non-preview validation before candidate work.
- The high volume of protected-surface findings could encourage broad cleanup.
  That is explicitly out of scope.

## Next Workflow Action

Next recommended role: Codex E contract-test/review for this docs-only
routing contract.

If Codex E is clean and the owner wants another #567 child, route to Codex A to
frame a future stable-rule crosscheck issue from the higher-priority pool.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/627

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/619

Contract:
docs/contracts/quality_ruff_preview_advisory_candidate_routing.md

Source report:
docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json

Goal:
Review whether the #627 contract correctly interprets and routes the #619 Ruff
preview advisory report without enabling preview mode, enforcement, broad Ruff
families, autofix, unsafe-fix, parser behavior changes, or readiness claims.

Verify:
- source report totals and LOG004 routing are represented accurately;
- preview-only rules remain advisory/deferred;
- stable watch-list rules are routed only to future non-preview crosscheck;
- protected-surface review is required before candidate work;
- preview mode remains absent from pyproject.toml, CI, and repo-check script;
- raw Ruff JSON remains out of scope;
- no code, config, CI, parser, analytics, workbook, webhook, Apps Script,
  OpenAI, AI, coaching, production, fixture, or corpus behavior changed.

Suggested validation:
- git status --short --branch
- py -m json.tool docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json
- rg -n "preview|--preview|select ALL|unsafe-fix|autofix|ruff" pyproject.toml .github/workflows/repo-checks.yml tools/run_repo_checks.ps1
- git diff --check -- docs/contracts/quality_ruff_preview_advisory_candidate_routing.md
- py tools/check_agent_docs.py
- path-scoped protected-surface scan over the contract
- path-scoped secret/private-marker scan over the contract

Final output:
- findings first;
- validation results;
- whether #627 can route to closure after submit/deploy;
- whether a future Codex A issue is recommended;
- workflow_handoff block.
```

Pasteable future Codex A prompt after clean review:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker / Problem Representation for the next scoped Ruff
tracker child issue.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Source contract:
docs/contracts/quality_ruff_preview_advisory_candidate_routing.md

Goal:
Frame a future stable non-preview Ruff crosscheck issue for the higher-priority
runtime/security-adjacent watch-list pool from #627.

Candidate pool to evaluate:
B009, DTZ001, PERF403, RUF001, RUF022, RUF059, RUF100, S112, S314, S606,
S607, TRY004, TRY301, TRY401

Do not implement code. Do not enable preview mode. Do not change CI,
pyproject.toml, parser behavior, fixtures, corpus status, analytics behavior,
workbook/webhook/App Script behavior, OpenAI/AI/coaching behavior, production
behavior, or run autofix/unsafe-fix.

Output:
- proposed child issue title/body or created issue link;
- exact stable non-preview evidence needed;
- candidate grouping recommendation;
- risk tier;
- protected-surface boundaries;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/627"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/619"
  source_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/626"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json"
  contract_artifact: "docs/contracts/quality_ruff_preview_advisory_candidate_routing.md"
  target_artifact: "docs/contract_test_reports/quality_ruff_preview_advisory_candidate_routing.md"
  risk_tier: "Medium workflow risk; low runtime risk because docs-only advisory routing"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/ruff-preview-routing-627"
  decision: "No preview-derived rule is blocking-ready; LOG004 remains deferred until stable; stable runtime/security-adjacent watch-list codes may feed future Codex A issue framing only after normal non-preview crosscheck."
  preview_mode_authorized: false
  ci_change_authorized: false
  blocking_promotion_authorized: false
  validation:
    - "git diff --check -- docs\\contracts\\quality_ruff_preview_advisory_candidate_routing.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan over contract"
    - "path-scoped secret/private-marker scan over contract"
  stop_conditions:
    - "Do not enable preview mode in pyproject.toml, CI, or normal repo checks."
    - "Do not promote preview rules to blocking gates."
    - "Do not promote broad Ruff families."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not run a fresh Ruff preview measurement unless a later issue explicitly authorizes it."
    - "Do not commit raw Ruff JSON, raw terminal output, local-only artifacts, private paths, generated data, secrets, raw logs, SQLite files, workbook exports, or app-data files."
    - "Do not claim parser correctness, security assurance, privacy assurance, release readiness, deploy readiness, production readiness, analytics truth, AI truth, or coaching truth from preview output."
```
