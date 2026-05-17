# Repo-Wide Hardening Report Generator Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/100

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch target: `codex/repo-wide-hardening-run`

Recent repo-wide hardening context:

- Issue #96 / PR #97 drift detector baseline first pass merged into
  `codex/repo-wide-hardening-run` at
  `5fdc433e06554c809533ea49391d6441fecc03a2`.
- Issue #96 remains open intentionally per lifecycle stop condition.
- Issue #98 / PR #99 Pyright advisory report artifact merged into
  `codex/repo-wide-hardening-run` at
  `fd23db71d4878c58359839f8499d1914b98f8326`.
- Issue #98 remains open intentionally per lifecycle stop condition.
- Tracker #82 remains open.

Agent docs read:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Repo-wide hardening contracts and reports read:

- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`
- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`
- `docs/contracts/repo_wide_golden_fixture_first_pass.md`
- `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`
- `docs/contracts/repo_wide_pyright_advisory_report.md`
- `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`
- `.github/pull_request_template.md`

Tooling surfaces read:

- `tools/check_secret_patterns.py`
- `tools/check_agent_docs.py`
- `tools/check_protected_surfaces.py`
- `tools/check_surface_authorization.py`
- `tools/select_validation.py`
- `tools/run_pyright_advisory_report.py`

This is a contract-writing artifact only. It does not implement code, add a
report generator, add tests, add CI gates, create report output, close issues,
mark tracker #82 complete, or change parser/runtime/workbook/webhook/Apps
Script behavior.

## Module

Repo-wide hardening report generator.

Plain English: the generator should assemble a durable, deterministic Markdown
status report from approved repo-local artifacts and operator-supplied
evidence. It answers "what changed, what was checked, what remains risky, and
what is next?" without re-running the world, inventing evidence, deciding merge
readiness, or becoming a new source of truth.

Likely future implementation artifact:

- `tools/generate_hardening_report.py`

Likely focused tests:

- `tests/test_hardening_report_generator.py`

Expected future implementation handoff:

- `docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md`

Expected future Codex E report:

- `docs/contract_test_reports/repo_wide_hardening_report_generator.md`

Expected first generated status report artifact, if Codex C implements report
writing:

- `docs/contract_test_reports/repo_wide_hardening_status_report.md`

The generated status report is not the final post-hardening comparison report.
A later thread may use the generator to help produce a post-hardening
comparison, but that later report must remain a separate queue item and must
not be treated as complete under issue #100.

## Owning Layer

Owning layer: repo-wide hardening evidence assembly and reporting.

Truth boundary:

- The generator owns deterministic report assembly from explicitly named
  evidence.
- The generator does not own parser truth, parser event interpretation,
  match/game identity, parser state final reconciliation, workbook schema
  truth, webhook payload truth, Apps Script behavior, issue lifecycle truth,
  PR merge readiness, CI truth, deployment readiness, or tracker completion.
- Parser/state contracts continue to own parser-managed facts.
- Existing tools own their own validation results:
  - `tools/check_secret_patterns.py` owns secret/private-marker scan results.
  - `tools/check_protected_surfaces.py` owns path-based protected-surface
    classifications.
  - `tools/check_surface_authorization.py` owns protected-surface
    authorization report status.
  - `tools/check_agent_docs.py` owns governance-doc consistency results.
  - `tools/select_validation.py` owns validation recommendation selection.
  - `tools/run_pyright_advisory_report.py` owns Pyright advisory report
    classification.
- Codex E review and Codex G integration/deployer judgment remain responsible
  for review findings, merge readiness, and deploy readiness.

The generator may summarize evidence. It must not upgrade summarized evidence
into authority.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_hardening_report_generator.md`

Future implementation surfaces allowed by this contract:

- `tools/generate_hardening_report.py`
- `tests/test_hardening_report_generator.py`
- `docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md`
- `docs/contract_test_reports/repo_wide_hardening_report_generator.md`
- `docs/contract_test_reports/repo_wide_hardening_status_report.md`

Optional narrow implementation surface:

- `tools/select_validation.py`, only if Codex C adds a focused recommendation
  mapping for the new generator or its tests.
- `tests/test_select_validation.py`, only if the selector mapping changes.

Referenced but not owned:

- issue #82
- issue #96 / PR #97
- issue #98 / PR #99
- issue #100
- existing repo-wide contracts, handoffs, and reports
- hardening checker tools and their focused tests
- `.github/workflows/repo-checks.yml`
- `.github/pull_request_template.md`
- parser, runtime, workbook, webhook, Apps Script, fixture, snapshot, baseline,
  generated-data, and local artifact paths

This contract does not authorize touching parser/runtime/workbook/webhook/Apps
Script behavior, CI gate behavior, live GitHub issue state, production state,
secrets, raw logs, generated data, runtime status files, failed posts, or
workbook exports.

## Observed Current Behavior

Observed during this Codex B pass:

- The current branch is `codex/repo-wide-hardening-run`.
- The branch is even with `origin/codex/repo-wide-hardening-run`.
- Issue #100 is open and names this contract as the expected artifact.
- Tracker #82 is open.
- Issue #96 remains open intentionally after PR #97 merge.
- Issue #98 remains open intentionally after PR #99 merge.
- The repo has several repo-wide hardening tools with stable text output and,
  in some cases, JSON output.
- Existing handoffs and issue comments already summarize hardening status, but
  they do so manually in prose.
- `docs/contract_test_reports/repo_wide_hardening_baseline.md` provides a
  baseline snapshot for the repo-wide hardening run.
- `tools/select_validation.py` recommends validation commands but does not run
  them.
- `tools/run_pyright_advisory_report.py` produces a stable advisory Pyright
  report and keeps Pyright non-gating.
- `tools/check_secret_patterns.py`, `tools/check_protected_surfaces.py`,
  `tools/check_surface_authorization.py`, and `tools/check_agent_docs.py`
  produce tool-owned evidence.
- No tracked report generator currently exists for assembling these evidence
  streams into one durable repo-wide hardening status report.

Current gap:

- There is no deterministic, reusable reporting layer that assembles current
  repo-wide hardening evidence without inventing missing results, running
  validation implicitly, or turning report assembly into merge-readiness
  automation.

## Required Guarantee

The report generator must produce a deterministic Markdown report from
explicitly named sources.

Required properties:

- Use only Python standard library in the first implementation.
- Default to reading repo-local artifacts and optional operator-supplied
  metadata.
- Do not query GitHub live in the first implementation.
- Do not run validation commands in the first implementation.
- Do not run CI checks, mark checks passed, or infer CI state.
- Do not decide merge readiness, deploy readiness, tracker completion, or issue
  closure.
- Do not close #96, #98, #100, or tracker #82.
- Do not claim a validation command passed unless an evidence item explicitly
  supplies that result.
- Label absent evidence as `missing`, `not_supplied`, or `not_run`, not as
  passed.
- Keep report output deterministic for the same repo files and input manifest.
- Sort paths, issues, PRs, commands, and artifact lists in stable order.
- Avoid wall-clock timestamps unless supplied explicitly by the input
  manifest.
- Use repo-relative paths in durable output.
- Redact or reject private absolute local paths, usernames, webhook URLs,
  workbook IDs, deployment IDs, API keys, tokens, credentials, raw log content,
  failed-post payloads, runtime status payloads, generated data dumps, and
  workbook exports.
- Preserve parser truth ownership and protected-surface boundaries.

## Public Interface

### Primary CLI

Recommended first implementation command:

```bash
python3 tools/generate_hardening_report.py --output docs/contract_test_reports/repo_wide_hardening_status_report.md
```

Windows equivalent:

```powershell
py tools\generate_hardening_report.py --output docs\contract_test_reports\repo_wide_hardening_status_report.md
```

Required arguments:

- None, when printing to stdout.

Required optional arguments:

- `--repo-root <path>`, default `"."`.
- `--output <path>`, optional Markdown output path.
- `--evidence-manifest <path>`, optional JSON file containing
  operator-supplied issue, PR, CI, command, and residual-risk evidence.

Allowed optional arguments:

- `--format markdown|json`, default `markdown`. JSON output is optional in the
  first implementation and must be additive if implemented.

Forbidden first-pass arguments:

- `--run`
- `--refresh`
- `--query-github`
- `--close-issues`
- `--decide-readiness`
- `--update-tracker`
- any flag that executes validation commands, opens network connections,
  mutates issues, mutates PRs, edits CI, refreshes baselines, or changes
  protected surfaces

### Side-Effect Rules

Without `--output`:

- Print the Markdown report to stdout.
- Do not write files.

With `--output`:

- Write only the requested Markdown report file.
- The default approved durable output path is:

```text
docs/contract_test_reports/repo_wide_hardening_status_report.md
```

- Refuse output paths under local/generated/private artifact areas, including
  `data/`, runtime logs, failed posts, raw logs, workbook exports, generated
  card data, generated tier data, and machine-local temporary artifact
  directories.
- Prefer creating only the parent directory for the approved report path if it
  is missing.

### Python Helper Surface

The stable public interface is the CLI and generated Markdown shape. The
implementation may expose standard-library-only helpers for tests, such as:

- artifact inventory collection
- evidence-manifest loading
- manifest validation
- evidence redaction
- report model assembly
- Markdown rendering
- optional JSON rendering

No parser/runtime module may import these helpers.

## Input Model

### Repo-Local Artifact Inventory

The generator may inspect expected repo-local artifact paths and report whether
they are present or missing. Presence is not validation success.

Expected artifact groups:

- baseline report:
  - `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- repo-wide contracts:
  - `docs/contracts/repo_wide_validation_selector.md`
  - `docs/contracts/repo_wide_secret_private_marker_scanner.md`
  - `docs/contracts/repo_wide_agent_docs_consistency_checker.md`
  - `docs/contracts/repo_wide_protected_surface_authorization_checker.md`
  - `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`
  - `docs/contracts/repo_wide_golden_fixture_first_pass.md`
  - `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`
  - `docs/contracts/repo_wide_pyright_advisory_report.md`
  - `docs/contracts/repo_wide_hardening_report_generator.md`
- implementation handoffs:
  - `docs/implementation_handoffs/repo_wide_validation_selector_comparison.md`
  - `docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md`
  - `docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md`
  - `docs/implementation_handoffs/repo_wide_protected_surface_authorization_checker_comparison.md`
  - `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`
  - `docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md`
  - `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`
  - `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`
  - `docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md`
- contract-test/review reports:
  - `docs/contract_test_reports/repo_wide_validation_selector.md`
  - `docs/contract_test_reports/repo_wide_secret_private_marker_scanner.md`
  - `docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md`
  - `docs/contract_test_reports/repo_wide_protected_surface_authorization_checker.md`
  - `docs/contract_test_reports/repo_wide_workbook_webhook_schema_snapshots.md`
  - `docs/contract_test_reports/repo_wide_golden_fixture_first_pass.md`
  - `docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md`
  - `docs/contract_test_reports/repo_wide_pyright_advisory_report.md`
  - `docs/contract_test_reports/repo_wide_hardening_report_generator.md`
- generated status report:
  - `docs/contract_test_reports/repo_wide_hardening_status_report.md`
- repo-local tools:
  - `tools/check_secret_patterns.py`
  - `tools/check_agent_docs.py`
  - `tools/check_protected_surfaces.py`
  - `tools/check_surface_authorization.py`
  - `tools/select_validation.py`
  - `tools/run_pyright_advisory_report.py`
  - `tools/generate_hardening_report.py`

Required behavior:

- Render present/missing artifact status.
- Do not parse arbitrary prose as proof that validation passed unless the
  evidence manifest or explicitly supported tool-report parser supplies a
  structured status.
- Do not treat presence of a handoff or report file as proof that the work is
  reviewed, merged, or complete.

### Operator-Supplied Evidence Manifest

The first implementation may accept a JSON manifest for issue, PR, CI,
validation, and residual-risk evidence that is not safely available from
repo-local files.

Recommended schema:

```json
{
  "object": "mythic_edge_hardening_report_inputs",
  "schema_version": 1,
  "tracker": "https://github.com/Tahjali11/Mythic-Edge/issues/82",
  "source_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/100",
  "branch": "codex/repo-wide-hardening-run",
  "head": "fd23db71d4878c58359839f8499d1914b98f8326",
  "issues": [
    {
      "number": 96,
      "url": "https://github.com/Tahjali11/Mythic-Edge/issues/96",
      "state": "open",
      "role": "lifecycle_item",
      "note": "Intentionally remains open per stop condition.",
      "source": "operator_supplied"
    }
  ],
  "pull_requests": [
    {
      "number": 99,
      "url": "https://github.com/Tahjali11/Mythic-Edge/pull/99",
      "state": "merged",
      "base": "codex/repo-wide-hardening-run",
      "merge_commit": "fd23db71d4878c58359839f8499d1914b98f8326",
      "source": "operator_supplied"
    }
  ],
  "validation": [
    {
      "command": "py -m pytest -q tests",
      "status": "passed",
      "summary": "766 passed, 1 skipped",
      "source": "tracker_comment"
    }
  ],
  "ci": [
    {
      "context": "PR #99",
      "status": "passed",
      "source": "operator_supplied"
    }
  ],
  "residual_risks": [
    {
      "risk": "Issue #96 remains open as a lifecycle item.",
      "severity": "medium",
      "source": "operator_supplied"
    }
  ],
  "next_recommended_role": "Codex C: Module Implementer / comparison thread"
}
```

Required manifest behavior:

- Missing manifest is allowed.
- Missing manifest fields must render as missing evidence.
- Malformed JSON must exit with configuration error.
- Unknown fields may be ignored or surfaced under an "Ignored Manifest Fields"
  section, but they must not crash report generation.
- Manifest values must be redacted before rendering.
- The generator must not trust manifest status strings blindly if they contain
  unsupported values. Unsupported statuses should become `unknown` or a
  configuration warning.

Allowed status vocabulary:

- `passed`
- `failed`
- `warning`
- `advisory`
- `not_run`
- `not_supplied`
- `missing`
- `unknown`

Allowed issue/PR state vocabulary:

- `open`
- `closed`
- `merged`
- `draft`
- `ready_for_review`
- `unknown`

### Tool Report Inputs

The first implementation may parse a narrow set of existing repo-local report
shapes only if doing so stays deterministic and well tested.

Allowed first-pass parsing:

- `tools/run_pyright_advisory_report.py --format json` output supplied through
  the manifest or a future explicit file path.
- `tools/select_validation.py --format json` output, if a future implementation
  supplies it.
- Direct artifact presence/absence by path.

Not required in the first implementation:

- parsing every Markdown handoff
- parsing GitHub comments
- parsing CI logs
- parsing terminal transcripts
- running tools to produce fresh JSON

If parsing is not implemented, the report must still list the relevant artifact
as present/missing and mark validation evidence as `not_supplied`.

## Output Model

### Markdown Report

The required first output format is Markdown.

Required heading:

```text
# Repo-Wide Hardening Status Report
```

Required metadata block:

```text
report_kind: repo_wide_hardening_status
schema_version: 1
generator: tools/generate_hardening_report.py
tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
source_issue: https://github.com/Tahjali11/Mythic-Edge/issues/100
branch: codex/repo-wide-hardening-run
evidence_mode: repo_local_and_operator_supplied
merge_readiness: not_decided_by_report
deploy_readiness: not_decided_by_report
tracker_completion: not_decided_by_report
```

Required sections:

- `## Evidence Sources`
- `## Artifact Inventory`
- `## Completed Or Merged Items`
- `## Open Lifecycle Items`
- `## Validation Evidence`
- `## Tool Evidence`
- `## Protected Surface And Secret Scan Evidence`
- `## Pyright Advisory Evidence`
- `## Golden Fixture And Drift Baseline Status`
- `## Missing Evidence`
- `## Residual Risks`
- `## Next Recommended Role`
- `## Workflow Handoff`

Required rendering rules:

- Use stable section order.
- Use stable item order.
- Use repo-relative paths.
- Avoid full raw command logs unless the manifest supplies a concise summary.
- Include source labels for evidence items:
  - `repo_local_artifact`
  - `operator_supplied`
  - `tool_report`
  - `tracker_comment`
  - `pr_metadata`
  - `ci_summary`
  - `missing`
- Include confidence labels for evidence items:
  - `confirmed`
  - `reported`
  - `inferred_from_presence`
  - `missing`
  - `unknown`
- Include finality labels where useful:
  - `final`
  - `advisory`
  - `lifecycle_open`
  - `pending_review`
  - `unknown`
- Clearly state that the report does not decide merge or deploy readiness.

### JSON Output

JSON output is optional in the first implementation. If implemented, it must
mirror the Markdown content with this minimum shape:

```json
{
  "object": "mythic_edge_repo_wide_hardening_status_report",
  "schema_version": 1,
  "tracker": "https://github.com/Tahjali11/Mythic-Edge/issues/82",
  "source_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/100",
  "branch": "codex/repo-wide-hardening-run",
  "evidence_mode": "repo_local_and_operator_supplied",
  "merge_readiness": "not_decided_by_report",
  "deploy_readiness": "not_decided_by_report",
  "artifacts": [],
  "issues": [],
  "pull_requests": [],
  "validation": [],
  "missing_evidence": [],
  "residual_risks": [],
  "workflow_handoff": {}
}
```

JSON support must not replace Markdown support.

## Required Report Semantics

### Evidence Summary

The report may say:

- an artifact exists
- an artifact is missing
- an operator supplied a status
- a tool report says `passed`, `warning`, `failed`, or `advisory`
- a validation command was reported as run with a supplied result
- a validation command has no supplied result
- a risk remains open
- a next role is recommended

The report must not say:

- "checks passed" unless each check listed has explicit supplied evidence
- "CI passed" unless CI evidence is supplied
- "ready to merge"
- "ready to deploy"
- "tracker complete"
- "issue can be closed"
- "protected-surface change is authorized" unless the authorization tool or
  supplied evidence explicitly says so
- "Pyright is clean" unless a Pyright advisory report or supplied validation
  evidence says so

### Missing Evidence

Missing evidence is first-class output.

Examples:

- no evidence manifest supplied
- CI status not supplied
- issue state not supplied
- PR state not supplied
- focused validation result not supplied
- protected-surface command result not supplied
- secret/private-marker command result not supplied
- Pyright advisory result not supplied
- full-suite result not supplied

Required behavior:

- Render missing evidence in its own section.
- Do not hide missing evidence because an artifact exists.
- Do not infer missing commands as passed.
- Do not fail report generation solely because optional evidence is missing.

### Report-Only Lifecycle Boundaries

The generator may summarize that #96 and #98 remain open intentionally, if that
evidence is supplied by the issue/problem representation or manifest.

It must not:

- close #96
- close #98
- close #100
- close or mark tracker #82 complete
- update issue labels
- comment on GitHub
- open a PR
- merge a PR
- mark a PR ready for review

### Relationship To Codex G

The generated status report is input to later workflow roles. It is not a
replacement for Codex G.

Codex G still owns:

- integration readiness review
- branch freshness review
- PR status review
- check status review
- merge conflict review
- production/deploy readiness review
- final "what can merge and what cannot" recommendations

The report may recommend "Next role: Codex E" or "Next role: Codex G" only as
a handoff suggestion. It must not decide that the work is ready.

## Distinction From Post-Hardening Comparison Report

Issue #100 defines a reusable generator mechanism.

The generator's first durable output is:

- `docs/contract_test_reports/repo_wide_hardening_status_report.md`

A future post-hardening comparison report would be a separate artifact and
separate issue/thread. It may compare:

- baseline hardening state
- completed child issues and PRs
- final validation evidence
- residual lifecycle items
- merge/deploy readiness evidence

That future comparison must not be created, claimed complete, or used to close
tracker #82 under this contract unless a later issue explicitly authorizes it.

## Redaction And Data Retention

Required redaction guarantees:

- Do not render full local absolute paths.
- Do not render usernames from local machine paths.
- Do not render webhook URLs.
- Do not render Google workbook IDs, document IDs, or Apps Script deployment
  IDs unless they are already public issue/PR URLs.
- Do not render API keys, OAuth tokens, bearer tokens, passwords, client
  secrets, private keys, or credential-like values.
- Do not render raw MTGA `Player.log` content.
- Do not render failed-post payloads.
- Do not render runtime status payloads.
- Do not render generated card data dumps.
- Do not render workbook exports.
- Do not render full terminal transcripts when a concise command summary is
  sufficient.

Allowed durable values:

- repo-relative paths
- GitHub issue and PR URLs for this repository
- Git commit hashes supplied as public repo metadata
- command names and concise summaries
- status labels
- artifact names
- redacted placeholders such as `<redacted-local-path>` or
  `<redacted-secret>`

If safe redaction is not possible, report generation should fail with a
configuration error rather than writing a risky report.

## Error Behavior

Configuration errors exit `2`:

- malformed evidence manifest
- unsupported output format
- output path outside approved report locations
- output path under forbidden local/generated/private artifact paths
- unreadable repo root
- impossible redaction of a value that must not be rendered

Reportable missing evidence exits `0`:

- no evidence manifest supplied
- optional artifact missing
- CI evidence not supplied
- issue/PR metadata not supplied
- validation command result not supplied

Unexpected errors:

- print a concise error to stderr
- exit `2`
- do not write partial output unless the implementation can guarantee atomic
  replacement of the requested report file

## Side Effects

Allowed side effects in this Codex B thread:

- create `docs/contracts/repo_wide_hardening_report_generator.md`

Forbidden side effects in this Codex B thread:

- no code implementation
- no tests
- no generated report output
- no CI edits
- no GitHub issue/PR mutation
- no parser/runtime/workbook/webhook/Apps Script changes
- no secrets, raw logs, generated data, runtime status files, failed posts, or
  workbook exports
- no PR
- no issue closure
- no tracker closure

Allowed side effects in future Codex C implementation:

- add `tools/generate_hardening_report.py`
- add `tests/test_hardening_report_generator.py`
- optionally add narrow selector mapping/tests for the generator
- produce `docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md`
- produce `docs/contract_test_reports/repo_wide_hardening_status_report.md`

Forbidden side effects in future Codex C implementation:

- executing validation commands from inside the generator
- querying GitHub live from inside the generator
- adding CI gates or merge-readiness automation
- deciding tracker completion, issue closure, PR readiness, merge readiness, or
  deploy readiness
- refreshing fixtures, snapshots, baselines, or expected outputs
- changing parser/runtime/workbook/webhook/Apps Script behavior
- touching protected data or production state

## Validation Requirements

Contract-writer validation for this Codex B pass:

```powershell
git diff --check
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_hardening_report_generator.md
'@ | py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
docs/contracts/repo_wide_hardening_report_generator.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
docs/contracts/repo_wide_hardening_report_generator.md
'@ | py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\contracts\repo_wide_hardening_report_generator.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_hardening_report_generator.md
'@ | py tools\select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
py tools\check_agent_docs.py
```

Focused Codex C validation:

```powershell
git status --short --branch
py -m pytest -q tests\test_hardening_report_generator.py
py tools\generate_hardening_report.py
py tools\generate_hardening_report.py --output docs\contract_test_reports\repo_wide_hardening_status_report.md
py -m ruff check src tests tools
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-100.md --authorization-file contract=docs\contracts\repo_wide_hardening_report_generator.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_hardening_report_generator_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

If Codex C changes `tools/select_validation.py`, also run:

```powershell
py -m pytest -q tests\test_hardening_report_generator.py tests\test_select_validation.py
```

Before Codex F submits a PR:

```powershell
py -m pytest -q tests
py -m ruff check src tests tools
py tools\generate_hardening_report.py --output docs\contract_test_reports\repo_wide_hardening_status_report.md
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-100.md --authorization-file contract=docs\contracts\repo_wide_hardening_report_generator.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_hardening_report_generator_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

Validation interpretation:

- A generated report with missing evidence may still be valid if the missing
  evidence is explicitly labeled.
- A generated report that claims unsupplied checks passed is invalid.
- A generated report that decides merge/deploy readiness is invalid.
- A generated report that embeds private paths, secrets, raw logs, failed-post
  payloads, runtime status payloads, generated data, or workbook exports is
  invalid.

## Required Tests

Focused tests for `tests/test_hardening_report_generator.py` should cover:

- CLI with no manifest prints Markdown to stdout.
- CLI with `--output` writes only the requested approved report path.
- CLI rejects output under `data/`, raw log, runtime status, failed-post,
  generated data, workbook export, or local artifact paths.
- Missing evidence manifest is allowed and renders missing evidence.
- Malformed evidence manifest exits `2`.
- Minimal valid evidence manifest renders tracker, issue, PR, validation,
  residual risk, and next-role data.
- Unsupported manifest statuses render as `unknown` or deterministic warnings.
- Artifact inventory is stable and sorted.
- Artifact presence is labeled as presence, not validation success.
- Missing artifact entries are labeled missing.
- Report includes required metadata fields and required sections.
- Report includes `merge_readiness: not_decided_by_report`.
- Report includes `deploy_readiness: not_decided_by_report`.
- Report includes `tracker_completion: not_decided_by_report`.
- Report does not include wall-clock timestamps unless explicitly supplied.
- Report redacts or rejects local absolute paths and usernames.
- Report redacts or rejects webhook URLs, workbook IDs, deployment IDs,
  tokens, passwords, and credential-like values.
- Report does not embed raw log snippets, failed-post payloads, runtime status
  payloads, generated data dumps, or workbook exports.
- Report distinguishes `repo_local_artifact`, `operator_supplied`,
  `tool_report`, `tracker_comment`, `pr_metadata`, `ci_summary`, and
  `missing` source labels.
- Report distinguishes `confirmed`, `reported`, `inferred_from_presence`,
  `missing`, and `unknown` confidence labels.
- Report distinguishes advisory Pyright evidence from required/failing gates.
- Report distinguishes generated status report from future post-hardening
  comparison report.
- Generator does not execute validation commands in tests unless a test uses a
  mocked command runner to prove execution is disabled.
- Generator does not query GitHub or network services.
- JSON output, if implemented, contains the contracted field names and does
  not replace Markdown support.

## Acceptance Criteria

- `docs/contracts/repo_wide_hardening_report_generator.md` exists and links
  issue #100 and tracker #82.
- The contract names the generator as report-only evidence assembly tooling.
- The contract defines current observed behavior, required guarantees,
  unknowns, suspected gaps, protected surfaces, validation requirements, and
  acceptance criteria.
- The contract defines the future public interface for
  `tools/generate_hardening_report.py`.
- The contract defines `docs/contract_test_reports/repo_wide_hardening_status_report.md`
  as the approved first generated report path.
- The contract distinguishes the generated status report from a future
  post-hardening comparison report.
- The contract permits optional operator-supplied JSON evidence but does not
  require live GitHub querying.
- The contract forbids automatic validation command execution in the first
  implementation.
- The contract forbids CI gates, merge-readiness automation, issue closure,
  tracker completion, fixture/snapshot/baseline refresh, parser behavior
  changes, workbook/webhook/Apps Script changes, and protected-data changes.
- The contract defines required report sections and evidence labels.
- Missing evidence is required to stay visible.
- Validation commands for Codex C/E/F are defined.
- The contract routes next work to Codex C.

## Unknowns

- Whether Codex C should implement JSON output in the first pass or keep the
  generator Markdown-only.
- Whether a future issue should authorize live GitHub metadata collection after
  the repo-local/operator-supplied workflow proves stable.
- Whether the status report should eventually accept tool JSON files directly
  or keep all non-repo evidence in one manifest.
- Whether the generated status report should be overwritten in place or kept as
  dated release snapshots in a future queue.
- Whether a later post-hardening comparison report should be generated by the
  same tool with a different mode or written as a separate review artifact.
- Whether Codex G will want additional fields for final integration readiness
  after the hardening queue is complete.

## Suspected Gaps

- Current hardening status is spread across issues, PRs, contracts, handoffs,
  reports, and tool outputs.
- Existing reports are useful but not assembled into one durable status view.
- Existing issue comments contain important lifecycle context that should not
  be scraped live in the first implementation.
- Existing tools produce validation evidence, but the report generator has no
  safe policy yet for parsing or referencing all of those outputs.
- Without a redaction policy, a status report could accidentally embed local
  paths, terminal output, workbook IDs, or private snippets.
- Without explicit wording, a status report could be mistaken for Codex G merge
  readiness.

## Stop Conditions

Stop and route back to Codex B or A if Codex C needs to:

- query GitHub live from the generator
- execute validation commands from the generator
- add CI gates or merge-readiness automation
- decide merge readiness, deploy readiness, issue closure, or tracker
  completion
- close #96, #98, #100, or #82
- refresh fixtures, snapshots, baselines, or expected outputs
- parse raw terminal logs or CI logs in a way that could embed private content
- embed local absolute paths, usernames, secrets, raw logs, failed-post
  payloads, runtime status payloads, generated data, or workbook exports
- change parser behavior
- change parser state final reconciliation
- change parser event classes or event kind values
- change parser payload shape
- change match identity
- change game identity
- change deduplication
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- touch live workbook state or deployed Apps Script state
- touch secrets, credentials, environment variables, raw logs, generated data,
  runtime status files, failed posts, workbook exports, local-only artifacts,
  or production behavior
- target `main`
- mark tracker #82 complete

## Expected Codex C Handoff

Codex C should produce:

- `docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md`

The handoff must include:

- role performed
- issue and tracker used
- contract used
- branch and git status
- files inspected
- observed current behavior compared to the contract
- implementation option chosen
- files changed
- exact CLI/report/test sections changed
- generated status report path, if created
- whether JSON output was implemented or deferred
- whether selector mapping was changed or deferred
- validation run and result
- secret/private-marker scan result
- protected-surface result
- surface-authorization result
- validation-selector result
- proof that the generator did not run validation commands
- proof that the generator did not query GitHub live
- proof that missing evidence is visible
- proof that merge/deploy readiness is not decided by the report
- proof that protected/private data is not embedded
- forbidden scopes touched or not touched
- remaining risks
- next recommended role
- pasteable Codex E prompt
- `workflow_handoff` block

## Expected Codex E Report

Codex E should produce:

- `docs/contract_test_reports/repo_wide_hardening_report_generator.md`

The report must lead with findings and verify:

- The generator is report-only.
- Missing evidence is labeled missing.
- The generator does not run validation commands.
- The generator does not query GitHub live.
- The generator does not decide merge readiness, deploy readiness, issue
  closure, or tracker completion.
- The generated status report path is
  `docs/contract_test_reports/repo_wide_hardening_status_report.md`.
- The generated status report is not treated as the future post-hardening
  comparison report.
- The report redacts or rejects private local paths, usernames, secrets,
  webhook URLs, workbook IDs, deployment IDs, raw logs, failed-post payloads,
  runtime status payloads, generated data, and workbook exports.
- Tests cover manifest behavior, missing evidence, deterministic rendering,
  redaction, output-path restrictions, and no command/network execution.
- No CI gates or merge-readiness automation were added.
- No parser/runtime/workbook/webhook/Apps Script protected surfaces changed.
- #96, #98, #100, and tracker #82 were not closed.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for repo-wide hardening issue #100: Hardening report generator.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/100

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_hardening_report_generator.md

Goal:
Compare the current repo-wide hardening artifacts and tools against the contract. Implement only the smallest report-only generator needed to produce a deterministic Markdown hardening status report from repo-local artifacts and optional operator-supplied evidence.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/repo_wide_hardening_report_generator.md
- docs/contract_test_reports/repo_wide_hardening_baseline.md
- docs/contracts/repo_wide_validation_selector.md
- docs/contracts/repo_wide_secret_private_marker_scanner.md
- docs/contracts/repo_wide_protected_surface_authorization_checker.md
- docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md
- docs/contracts/repo_wide_golden_fixture_first_pass.md
- docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
- docs/contracts/repo_wide_pyright_advisory_report.md
- docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md
- tools/check_secret_patterns.py
- tools/check_agent_docs.py
- tools/check_protected_surfaces.py
- tools/check_surface_authorization.py
- tools/select_validation.py
- tools/run_pyright_advisory_report.py
- .github/pull_request_template.md

Before editing:
- Confirm branch is codex/repo-wide-hardening-run.
- Inspect git status and exclude unrelated changes.
- State what the hardening report generator is supposed to do, what current hardening reports/tools already do, what reporting gap remains, and the exact minimal implementation plan.

Do:
- Add a standard-library-only report generator, preferably tools/generate_hardening_report.py.
- Add focused tests, preferably tests/test_hardening_report_generator.py.
- Produce deterministic Markdown output.
- Support stdout output and --output docs/contract_test_reports/repo_wide_hardening_status_report.md.
- Support an optional JSON evidence manifest for operator-supplied issue, PR, CI, validation, and residual-risk evidence.
- Label missing evidence as missing/not_supplied/not_run.
- Keep artifact presence distinct from validation success.
- Include merge_readiness: not_decided_by_report, deploy_readiness: not_decided_by_report, and tracker_completion: not_decided_by_report.
- Redact or reject private local paths, usernames, secrets, webhook URLs, workbook IDs, deployment IDs, raw logs, failed-post payloads, runtime status payloads, generated data, and workbook exports.
- Produce docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md.
- Produce docs/contract_test_reports/repo_wide_hardening_status_report.md if the generator writes a durable first report.

Do not:
- Query GitHub live from the generator.
- Run validation commands from the generator.
- Add CI gates or merge-readiness automation.
- Decide merge readiness, deploy readiness, issue closure, or tracker completion.
- Close #96, #98, #100, or tracker #82.
- Refresh fixtures, snapshots, baselines, expected outputs, or drift reports.
- Change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, production behavior, or main.
- Stage, commit, open a PR, close issues, or merge unless explicitly asked.

Validation:
git status --short --branch
py -m pytest -q tests\test_hardening_report_generator.py
py tools\generate_hardening_report.py
py tools\generate_hardening_report.py --output docs\contract_test_reports\repo_wide_hardening_status_report.md
py -m ruff check src tests tools
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-100.md --authorization-file contract=docs\contracts\repo_wide_hardening_report_generator.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_hardening_report_generator_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check

If .tmp\issue-100.md is absent locally, create a temporary authorization note from issue #100 before running the surface-authorization command, then remove it afterward unless explicitly asked to keep local helper files.

Final handoff must include:
- role performed
- issue/tracker
- contract used
- files changed
- exact CLI/report/test sections changed
- generated status report path, if created
- validation run and result
- missing-evidence behavior
- redaction/private-data behavior
- no-command-execution and no-live-GitHub confirmation
- merge/deploy readiness no-authority confirmation
- protected-surface status
- surface-authorization status
- secret/private-marker status
- validation-selector status
- what remains unverified
- whether forbidden scope was touched
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/100"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/repo_wide_hardening_report_generator.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md"
  expected_review_artifact: "docs/contract_test_reports/repo_wide_hardening_report_generator.md"
  expected_generated_report: "docs/contract_test_reports/repo_wide_hardening_status_report.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "git diff --check"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\\contracts\\repo_wide_hardening_report_generator.md"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_agent_docs.py"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not add CI gates or merge-readiness automation."
    - "Do not query GitHub live from the future first-pass generator."
    - "Do not run validation commands from the future first-pass generator."
    - "Do not close #96, #98, #100, or tracker #82."
    - "Do not refresh fixtures, snapshots, baselines, expected outputs, or drift reports."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, production behavior, or merge-to-main policy."
    - "Do not target main."
```
