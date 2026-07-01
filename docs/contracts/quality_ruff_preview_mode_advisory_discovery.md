# Ruff Preview-Mode Advisory Discovery Contract

## Module

`quality_ruff_preview_mode_advisory_discovery`

Plain English: this contract defines how Mythic Edge may use Ruff preview mode
as an early-warning discovery tool. Preview mode can reveal unstable or future
Ruff rules before they are ready for normal repo checks. This contract keeps
that evidence advisory-only and prevents it from becoming CI enforcement,
`pyproject.toml` configuration, broad cleanup, autofix, or a readiness claim.

This is a Codex B contract artifact only. It does not implement code, run a
preview-mode measurement, change CI, edit Ruff configuration, promote rules,
run autofix, run unsafe-fix, or change product behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/619
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Related current tranche: https://github.com/Tahjali11/Mythic-Edge/issues/618
- Contract artifact:
  `docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`

## Tracker

Tracker #567 remains open for Ruff all-rules advisory sweeps and earned
zero-baseline CI promotion. Issue #619 is a report-only preview discovery
child. It does not close the tracker and does not authorize blocking
promotion.

## Owning Layer

Quality / Governance.

Ruff owns static-analysis findings for the exact command, Ruff version,
branch/ref, commit, and scan scope used. A Ruff preview-mode advisory report
does not own parser truth, analytics truth, security assurance, privacy
assurance, release readiness, deploy readiness, production readiness, AI truth,
or coaching truth.

## Internal Project Area

Primary area: Quality / Governance.

Supporting area: Shared Support, because the existing Ruff advisory report
helper is shared validation tooling. It must not become runtime behavior or a
hidden CI gate.

## Truth Owner

The future sanitized preview report owns only a public-safe summary of one
preview-mode Ruff measurement. It is not source truth for code behavior. It
does not prove that a preview rule is stable, useful, safe to promote, or
eligible for CI.

## Bridge-Code Status

`not_bridge_code`

This is a quality-reporting contract. It does not bridge parser facts into
analytics, UI, workbook, Apps Script, Google Sheets, OpenAI, AI, coaching, or
production systems.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`

Future Codex C work may add, if and only if implemented under this contract:

- `docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md`
- a sanitized preview report under:
  `docs/quality_reports/ruff_advisory/<YYYY-MM-DD>-<short-commit>-ruff-preview-advisory-report.json`
- focused tests if the report helper or wrapper changes

Future implementation may extend existing Ruff advisory reporting code or add a
narrow preview wrapper, but it must not create a second unsynchronized Ruff
authority.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- issue #619
- tracker #567
- roadmap #568
- related issue #618
- `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- `docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md`
- `docs/contracts/quality_ruff_second_bug_risk_tranche.md`
- `docs/contracts/quality_ruff_current_advisory_measurement_report.md`
- `docs/contract_test_reports/quality_ruff_current_advisory_remeasurement_after_second_tranche.md`
- `docs/quality_reports/ruff_advisory/2026-07-01-62bc9c2-ruff-advisory-report.json`
- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`

Codex B also observed that the handoff source branch
`codex/analytics-foundation` did not contain the current Ruff report artifacts.
This contract was therefore written in a fresh issue-scoped worktree based on
`origin/main`. The local absolute worktree path is intentionally omitted from
this public contract artifact.

Branch:

```text
codex/ruff-preview-advisory-619
```

## Observed Current Behavior

Current committed Ruff configuration in `pyproject.toml` selects stable exact
codes only:

```toml
[tool.ruff.lint]
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

Current GitHub Actions lint command:

```powershell
py -m ruff check src tests tools
```

Current local repo-check lint command:

```powershell
py -m ruff check src tests tools
```

Current Ruff version observed in this Codex B pass:

```text
ruff 0.15.12
```

The latest sanitized stable advisory report records:

```yaml
branch_or_ref: origin/main
commit: 62bc9c2a61b414d5e168148cb078a44842fc42bc
ruff_version: "ruff 0.15.12"
scan_scope:
  - src
  - tests
  - tools
command: "py -m ruff check src tests tools --select ALL --exit-zero --output-format json --output-file <local-only-raw-json>"
findings: 17984
triggered_rule_codes: 116
zero_baseline_rule_codes: 840
exit_behavior: advisory_exit_zero
```

Related issue #618 observed that `LOG004` has no effect unless Ruff preview
mode is enabled. The stable sanitized report still lists `LOG004` as a
zero-baseline candidate, which is accurate only for the stable command that did
not activate preview behavior. That evidence must not be used to promote
`LOG004` as a stable exact-code gate.

## Problem Statement

Ruff preview mode is useful because it can show Mythic Edge future rules before
they become stable. It is risky because preview rules are unstable, may change
meaning, and may produce output that should not become normal CI behavior.

The first bad value is enabling preview mode in `pyproject.toml`, CI, or normal
repo checks before Mythic Edge has observed and classified preview-only rules.

The second bad value is treating preview zero findings as stable
zero-baseline evidence. A preview-only zero finding means "nothing was found in
this preview measurement," not "this rule is stable enough to block CI."

The third bad value is committing raw preview Ruff JSON or raw terminal output.
Preview output can contain local paths, source-like diagnostic messages,
private-marker filenames, or rule details that need the existing sanitized
report boundary.

## Contract Summary

Mythic Edge may run a future advisory-only Ruff preview discovery measurement
after Codex C validates this contract and uses a local-only raw output path.

The future preview measurement must:

- use preview mode only for the one advisory command;
- keep raw Ruff JSON local and ignored;
- emit only a sanitized preview report if the report passes public-safety
  checks;
- classify preview exact codes as candidates, watch-list items, style-only,
  noisy, protected-surface-review-required, deferred until stable, or not
  recommended;
- preserve all current blocking Ruff configuration and CI behavior;
- make no readiness, assurance, truth, release, deploy, production, parser,
  analytics, AI, or coaching claim.

This contract does not authorize normal preview-mode enforcement.

## Preview-Mode Advisory Boundary

Preview mode may be used only as:

```yaml
mode: advisory_discovery
blocking: false
ci_gate: false
normal_repo_check: false
pyproject_preview_enabled: false
autofix: false
unsafe_fix: false
source_cleanup: false
```

Preview mode must not be used in:

- `pyproject.toml`;
- `.github/workflows/repo-checks.yml`;
- `tools/run_repo_checks.ps1`;
- required local validation commands;
- broad cleanup passes;
- future exact-code blocking gates without a separate issue and contract.

## Allowed Command Shape

Codex C may run this command shape only after confirming branch freshness and a
clean worktree:

```powershell
py -m ruff check src tests tools --preview --select ALL --exit-zero --output-format json --output-file _review_/quality_ruff_preview_advisory/<run-id>/ruff-preview-all.json
```

Required command properties:

- `--preview` is required for this discovery issue.
- `--select ALL` is allowed only because `--exit-zero` keeps the command
  report-only.
- `--exit-zero` is required.
- `--output-format json` is required for sanitized processing.
- `--output-file` must point under ignored `_review_/`.
- scan scope must be exactly `src tests tools` unless a later contract narrows
  it.
- no `--fix`;
- no `--fix-only`;
- no `--unsafe-fixes`;
- no `--preview` in normal repo checks.

Codex B did not run this preview command.

## Raw Output Handling

Raw preview Ruff JSON must remain local-only.

Required raw-output handling:

- write raw JSON only under ignored `_review_/quality_ruff_preview_advisory/`;
- do not commit raw JSON;
- do not paste raw JSON into docs, issues, PRs, tracker comments, or handoffs;
- do not keep raw JSON in `docs/quality_reports/`;
- delete or leave ignored local raw output according to existing local review
  artifact practice, but never stage it;
- fail closed if raw output contains unsupported records, paths outside the
  measured checkout, secret-like values, raw source snippets, fix edits, raw
  logs, private payloads, local-only artifacts, or public-unsafe path text that
  cannot be omitted symbolically.

## Sanitized Preview Report Shape

If Codex C creates a committed report, it must be sanitized and must use a
preview-specific public shape. Recommended path:

```text
docs/quality_reports/ruff_advisory/<YYYY-MM-DD>-<short-commit>-ruff-preview-advisory-report.json
```

Recommended top-level fields:

```json
{
  "object": "mythic_edge_quality_ruff_preview_advisory_report",
  "schema_version": "quality_ruff_preview_advisory_report.v1",
  "repository": "Tahjali11/Mythic-Edge",
  "repository_url": "https://github.com/Tahjali11/Mythic-Edge",
  "branch_or_ref": "origin/main",
  "commit": "<measured-commit>",
  "ruff_version": "ruff 0.15.12",
  "scan_scope": ["src", "tests", "tools"],
  "commands": [
    "py -m ruff check src tests tools --preview --select ALL --exit-zero --output-format json --output-file <local-only-raw-json>"
  ],
  "exit_behavior": "advisory_exit_zero",
  "preview_enabled_for_measurement": true,
  "preview_enabled_in_pyproject": false,
  "preview_enabled_in_ci": false,
  "blocking_promotion_authorized": false,
  "autofix_authorized": false,
  "unsafe_fix_authorized": false,
  "totals": {
    "findings": 0,
    "triggered_rule_codes": 0,
    "preview_only_rule_codes": 0,
    "zero_baseline_preview_rule_codes": 0
  },
  "rule_summaries": [],
  "classification_summary": {},
  "non_claims": []
}
```

Codex C may extend the existing `tools/generate_ruff_advisory_report.py`
helper or add a narrow wrapper, but the committed preview report must not
masquerade as the existing stable `quality_ruff_advisory_report.v1` report.
It must include explicit preview fields and non-claims.

## Candidate Classification Model

Each exact preview rule summary must have exactly one primary classification:

| Classification | Meaning | Allowed follow-up |
| --- | --- | --- |
| `candidate_exact_code` | Potential future exact-code tranche once the rule is stable and revalidated. | Create/draft a later non-preview candidate issue only after stability evidence. |
| `watch_list` | Worth watching, but not yet actionable. | Keep in later advisory comparisons. |
| `style_only` | Mostly style or formatting churn. | Defer unless later repo style policy asks for it. |
| `too_noisy` | Too many findings or too much churn for current roadmap. | Defer; no cleanup issue without a separate contract. |
| `protected_surface_review_required` | Findings touch parser, runtime, analytics, local app security, workbook/transport, governance, private artifact, or other protected surfaces. | Route to a protected-surface contract before cleanup or promotion. |
| `defer_until_stable` | Rule is preview-only or behavior may change before stable Ruff release. | Reconsider when Ruff makes the rule stable. |
| `not_recommended` | Not aligned with Mythic Edge conventions or risk posture. | No action unless a later issue reverses the decision. |

Secondary labels are allowed for explanation, such as:

- `logging_visibility`;
- `runtime_safety`;
- `security_adjacent`;
- `maintainability`;
- `diagnostic_quality`;
- `test_only`;
- `docs_only`;
- `local_app_only`;
- `parser_protected_surface`.

Secondary labels must not imply readiness, security assurance, or parser truth.

## LOG004 Policy

`LOG004` is the motivating example for this issue.

Current policy:

- `LOG004` must remain excluded from issue #618 and any stable exact-code
  promotion while Ruff reports that it has no effect without preview mode.
- `LOG004` may be measured in the #619 preview discovery report.
- If preview measurement reports zero findings for `LOG004`, classify it as
  `defer_until_stable` or `watch_list`, not as immediately blocking-ready.
- If preview measurement reports findings for `LOG004`, classify by affected
  path and risk. It must not trigger cleanup or promotion automatically.
- `LOG004` can receive a later non-preview promotion issue only after a future
  Ruff version makes it effective without preview or after a separate contract
  explicitly authorizes preview-mode gate exploration.

## Required Non-Claims

Every preview report must include these non-claims:

- not CI readiness;
- not blocking-promotion readiness;
- not parser behavior readiness;
- not parser truth;
- not fixture promotion readiness;
- not corpus readiness;
- not security assurance;
- not privacy assurance;
- not release readiness;
- not deploy readiness;
- not production readiness;
- not analytics truth;
- not AI truth;
- not coaching truth;
- not preview-mode adoption approval.

## Enforcement Deferral Rules

No preview-derived rule may become blocking until all are true:

1. A later issue specifically names the exact rule code.
2. A later contract states whether the rule is now stable or still preview-only.
3. Current-base validation passes on the exact rule code.
4. The rule has zero findings under the command intended for enforcement.
5. The rule does not require broad cleanup, autofix, or unsafe-fix.
6. A review confirms protected-surface impact is acceptable.
7. CI and local validation surfaces are explicitly authorized to change.
8. The rule can be explained without readiness or assurance overclaims.

Preview-derived candidate reports may recommend future issue titles, but they
must not create issues automatically unless a later prompt explicitly
authorizes issue creation.

## Stop Conditions

Codex C must stop without committing a preview report when:

- worktree is dirty before measurement;
- target ref/commit is stale or ambiguous;
- Ruff is missing or not version-recorded;
- command omits `--preview`, `--select ALL`, `--exit-zero`, or
  `--output-format json`;
- command includes `--fix`, `--fix-only`, or `--unsafe-fixes`;
- command would change source files;
- raw JSON path is not under ignored `_review_/`;
- raw JSON is malformed;
- sanitized helper cannot distinguish preview mode from stable mode;
- sanitized report contains local absolute paths, private-marker path text,
  raw source snippets, fix edits, raw logs, raw payloads, secrets, credentials,
  tokens, webhook URLs, endpoint values, spreadsheet IDs, generated/private
  artifacts, or local-only artifacts;
- report text claims security/privacy assurance, readiness, parser truth,
  analytics truth, AI truth, coaching truth, or CI promotion authorization;
- Codex C needs to edit `pyproject.toml`, CI, repo-check scripts, or source
  files outside the authorized report/helper/test scope.

## Future Implementation Scope

Recommended Codex C scope:

1. Compare current helper/report behavior against this contract.
2. Add the smallest helper/wrapper/test change needed to emit a
   preview-specific sanitized report shape.
3. Run the preview advisory measurement into ignored `_review_/`.
4. Generate the sanitized preview report under
   `docs/quality_reports/ruff_advisory/`.
5. Write
   `docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md`.

Codex C may change only:

- `tools/generate_ruff_advisory_report.py` or a narrowly named wrapper helper;
- focused tests for the report helper/wrapper;
- the preview sanitized report artifact;
- the implementation handoff.

Codex C must not edit:

- `pyproject.toml`;
- `.github/workflows/repo-checks.yml`;
- `tools/run_repo_checks.ps1`;
- parser/runtime/source behavior;
- current blocking Ruff rule selection.

If Codex C finds the existing helper can already safely produce the required
preview-specific schema without code changes, it may leave helper code
unchanged and create only the sanitized report plus handoff.

## Validation Requirements

### Codex B Validation

For this contract:

```powershell
git status --short --branch --untracked-files=all
git diff --check -- docs\contracts\quality_ruff_preview_mode_advisory_discovery.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_ruff_preview_mode_advisory_discovery.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_ruff_preview_mode_advisory_discovery.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Because this is a new untracked file in Codex B, also run a no-index new-file
whitespace check or record the normal `git diff --check` caveat.

Codex B must not run the preview all-rules measurement.

### Codex C Validation

Before measurement:

```powershell
git fetch --prune
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
py -m ruff --version
```

Preview measurement, if the worktree is clean:

```powershell
py -m ruff check src tests tools --preview --select ALL --exit-zero --output-format json --output-file _review_/quality_ruff_preview_advisory/<run-id>/ruff-preview-all.json
```

After helper/report work:

```powershell
py -m json.tool docs\quality_reports\ruff_advisory\<YYYY-MM-DD>-<short-commit>-ruff-preview-advisory-report.json
py -m pytest -q tests\test_ruff_advisory_report.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Run path-scoped protected-surface and secret/private-marker scans over changed
tracked files. Also verify the raw preview JSON path is ignored:

```powershell
git check-ignore -v _review_\quality_ruff_preview_advisory\<run-id>\ruff-preview-all.json
```

### Codex E Review Requirements

Codex E must verify:

- preview mode remains absent from `pyproject.toml`, CI, and repo-check
  scripts;
- raw preview JSON is ignored and untracked;
- committed report has a preview-specific schema or explicit preview fields;
- report records command, commit, Ruff version, scan scope, and non-claims;
- report does not contain raw findings, source snippets, fix edits, local
  paths, private markers, secrets, raw logs, generated/local artifacts, or
  overclaims;
- `LOG004` is not treated as stable blocking-ready;
- classification labels are advisory;
- no parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/
  coaching/production behavior changed.

### Codex G Requirements

If a PR later exists, Codex G must verify:

- PR remains report/helper scoped;
- no CI or Ruff config gate changed;
- issue #619 may close only after reviewed sanitized report or an explicit
  documented no-report decision;
- tracker #567 remains open unless the whole tracker is complete.

## Protected-Surface Assessment

Risk tier: Medium workflow risk; low runtime risk if kept advisory-only.

This contract touches Quality / Governance only.

Protected surfaces preserved:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity and deduplication;
- fixtures, snapshots, corpus status, and private evidence workflow;
- analytics truth;
- workbook schema and webhook payload shape;
- Apps Script and Google Sheets behavior;
- OpenAI/model-provider/AI/coaching behavior;
- Line Tracer behavior;
- production behavior;
- CI gates;
- `pyproject.toml` blocking Ruff selection;
- secrets, credentials, raw logs, generated/private artifacts, SQLite files,
  app-data files, failed posts, workbook exports, and local-only artifacts.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`.
- Contract defines preview mode as advisory discovery only.
- Contract defines allowed preview command/report shape.
- Contract keeps raw preview JSON local and untracked.
- Contract requires a preview-specific sanitized report shape.
- Contract defines candidate classification labels.
- Contract defines `LOG004` handling.
- Contract forbids preview mode in `pyproject.toml`, CI, and normal repo
  checks.
- Contract forbids autofix, unsafe-fix, broad cleanup, and blocking promotion.
- Contract defines Codex C/E/G validation.
- Codex B changes only this contract artifact.

## Unknowns And Suspected Gaps

Unknowns:

- Whether the existing Ruff advisory report helper can safely emit a
  preview-specific schema with a small change, or whether a wrapper is cleaner.
- Which preview rules will trigger on current `origin/main`; Codex B did not
  run the preview measurement.
- Whether future Ruff versions will make `LOG004` stable outside preview mode.

Suspected gaps:

- The current stable advisory report can list preview-only rules like `LOG004`
  as zero-baseline candidates because the stable command does not activate
  them. A preview-specific report needs explicit fields to prevent this
  confusion.
- Existing report classification does not include the #619 labels
  `watch_list`, `style_only`, `too_noisy`, or `defer_until_stable` as a
  preview-specific decision model.

## Next Workflow Action

Next role: Codex C: Module Implementer / report execution.

Codex C should run only after confirming the branch, worktree, and target base
with the user or current handoff. This Codex B pass used a fresh issue worktree
from `origin/main` because the handoff source branch lacked current Ruff report
artifacts.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / report execution.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/619

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/quality_ruff_preview_mode_advisory_discovery.md

Goal:
Compare the current Ruff advisory helper/report behavior against the contract,
then implement the smallest safe preview-mode advisory discovery report path.
Run Ruff preview mode only as an advisory measurement, keep raw JSON local and
ignored, and commit only a sanitized preview-specific report plus an
implementation handoff.

Before editing or measuring:
- Confirm branch and git status.
- Fetch and confirm the target base/ref.
- Preserve unrelated worktree changes.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md,
  docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and
  docs/contracts/quality_ruff_preview_mode_advisory_discovery.md.
- Inspect tools/generate_ruff_advisory_report.py,
  tests/test_ruff_advisory_report.py, pyproject.toml,
  .github/workflows/repo-checks.yml, and tools/run_repo_checks.ps1.

Allowed scope:
- a narrow helper/wrapper/test update if needed for preview-specific sanitized
  report output;
- docs/quality_reports/ruff_advisory/<YYYY-MM-DD>-<short-commit>-ruff-preview-advisory-report.json;
- docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md.

Do not:
- enable preview mode in pyproject.toml, CI, or tools/run_repo_checks.ps1;
- change current blocking Ruff rule selection;
- promote preview rules to blocking gates;
- run Ruff autofix, fix-only, or unsafe-fix;
- perform broad cleanup;
- commit raw Ruff JSON or raw terminal output;
- treat LOG004 or any preview-only rule as stable blocking-ready;
- claim parser correctness, security assurance, privacy assurance, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  or coaching truth;
- change parser behavior, fixtures, corpus status, analytics behavior,
  workbook behavior, webhook behavior, Apps Script behavior,
  OpenAI/model-provider behavior, AI/coaching behavior, or production behavior.

Validation:
git fetch --prune
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
py -m ruff --version
py -m ruff check src tests tools --preview --select ALL --exit-zero --output-format json --output-file _review_/quality_ruff_preview_advisory/<run-id>/ruff-preview-all.json
py -m json.tool docs\quality_reports\ruff_advisory\<YYYY-MM-DD>-<short-commit>-ruff-preview-advisory-report.json
py -m pytest -q tests\test_ruff_advisory_report.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
git check-ignore -v _review_\quality_ruff_preview_advisory\<run-id>\ruff-preview-all.json

Also run path-scoped protected-surface and secret/private-marker scans over
changed tracked files.

Final output must include:
- role performed
- issue/tracker/roadmap
- contract used
- measured ref and commit
- Ruff version
- raw preview JSON local path status, without printing raw contents
- sanitized report artifact path
- preview classification summary
- LOG004 classification
- files changed
- validation results
- protected-surface status
- secret/private-marker status
- forbidden scope confirmation
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/619"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #619"
  contract_artifact: "docs/contracts/quality_ruff_preview_mode_advisory_discovery.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md"
  expected_report_artifact: "docs/quality_reports/ruff_advisory/<YYYY-MM-DD>-<short-commit>-ruff-preview-advisory-report.json"
  risk_tier: "Medium workflow risk; low runtime risk if advisory-only"
  branch_observed_by_codex_b: "codex/ruff-preview-advisory-619"
  base_branch_observed_by_codex_b: "origin/main"
  source_handoff_branch_note: "Codex A handoff named codex/analytics-foundation, but Codex B used a fresh origin/main worktree because the source branch lacked current Ruff report artifacts."
  preview_measurement_run_by_codex_b: false
  enforcement_authorized: false
  ci_change_authorized: false
  pyproject_preview_authorized: false
  ruff_autofix_authorized: false
  ruff_unsafe_fix_authorized: false
  decision: "Authorize a later advisory-only preview discovery report with raw JSON kept local and a preview-specific sanitized report shape; do not enable preview mode in normal repo checks."
  validation:
    - "git diff --check -- docs\\contracts\\quality_ruff_preview_mode_advisory_discovery.md"
    - "new-file no-index whitespace check if artifact is untracked"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan over contract artifact"
    - "path-scoped secret/private-marker scan over contract artifact"
  stop_conditions:
    - "Do not enable preview mode in pyproject.toml, CI, or normal repo checks."
    - "Do not promote preview rules to blocking gates."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not commit raw Ruff JSON or raw terminal output."
    - "Do not claim parser correctness, security assurance, privacy assurance, release readiness, deploy readiness, production readiness, analytics truth, AI truth, or coaching truth."
    - "Do not change parser behavior, fixtures, corpus status, analytics behavior, workbook behavior, webhook behavior, Apps Script behavior, OpenAI/model-provider behavior, AI/coaching behavior, or production behavior."
```
