# Quality Protected-Surface Coverage Floor Readiness Contract

## Module

`quality_protected_surface_coverage_floor_readiness`

This contract defines what "protected-surface coverage" should mean for Mythic
Edge and what evidence must exist before any per-surface coverage floor can be
considered. It does not implement measurement tooling, change CI, or add a
protected-surface gate.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/605>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/566>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Completed global floor issue: <https://github.com/Tahjali11/Mythic-Edge/issues/595>
- Completed global floor PR: <https://github.com/Tahjali11/Mythic-Edge/pull/604>
- Prior contract:
  `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`
- Prior review:
  `docs/contract_test_reports/quality_coverage_global_line_floor_enforcement_readiness.md`

## Owning Layer

Quality and validation tooling.

Coverage tooling owns measured execution evidence for a specific command,
coverage source, ref/commit, and report artifact. Coverage does not own parser
truth, protected-surface authorization, security assurance, privacy assurance,
release readiness, deploy readiness, production readiness, analytics truth, AI
truth, or coaching truth.

## Internal Project Area

Quality / validation gates.

## Truth Owner

The proposed protected-surface coverage report owns only advisory coverage
measurement metadata. The current protected-surface checker remains the owner
of protected path classification. Parser/state code remains the owner of parser
truth.

## Bridge-Code Status

`shared_support`

This work bridges coverage reporting with protected-surface classification, but
it must not merge the two into one blocking authority. The existing global
coverage floor remains the only active coverage gate.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/quality_protected_surface_coverage_floor_readiness.md`

Future implementation artifacts, if Codex C proceeds:

- a report-only helper or extension for protected-surface coverage measurement;
- focused tests for that helper;
- an implementation handoff under `docs/implementation_handoffs/`;
- optionally, one public-safe advisory report under `docs/quality_reports/`.

This contract does not authorize edits to CI, `pyproject.toml`, parser source,
analytics schema, workbook schema, webhook payload shape, Apps Script, or
production behavior.

## Observed Current Behavior

Current coverage posture after #595 / PR #604:

```yaml
implemented_gate: blocking_85_00_percent_global_python_line_coverage_floor
branch_coverage_posture: advisory_only
line_coverage_percent: 87.55
branch_coverage_percent: 74.80
tests_passed: 2015
tests_skipped: 4
raw_coverage_artifacts_committed: false
```

Current tooling:

- `.github/workflows/repo-checks.yml` runs tests with coverage in GitHub
  Actions and checks the global 85.00% Python line floor.
- `tools/run_repo_checks.ps1 -Coverage` runs the local equivalent coverage
  command and checks the same global 85.00% line floor.
- `tools/check_coverage_floor.py` reads coverage XML and enforces only the
  aggregate line rate.
- `pyproject.toml` measures coverage for `src/mythic_edge_parser` with branch
  measurement enabled.
- `tools/check_protected_surfaces.py` classifies changed paths as allowed,
  warning-level protected surfaces, or forbidden local/private/generated
  artifacts.
- `tools/check_protected_surfaces.py` is path-classification tooling. It does
  not read coverage data.

## Protected-Surface Coverage Definition

Protected-surface coverage means advisory measurement of line coverage for
repo-owned Python source files that are classified as protected or
protected-adjacent by Mythic Edge governance.

It answers:

> For the current measured ref, how much of each measurable protected Python
> surface was executed by the approved coverage command?

It does not answer:

- whether parser behavior is correct;
- whether a protected-surface change is authorized;
- whether CodeQL or security alerts are closed;
- whether private data is safe;
- whether the project is release-ready;
- whether production behavior is ready;
- whether branch coverage should block work.

## Measurement And Reporting Recommendation

The first #605 implementation slice should be advisory-only measurement and
reporting.

Recommended first posture:

```yaml
recommended_posture: advisory_measurement_report_only
protected_surface_floor_authorized: false
ci_change_authorized: false
global_line_floor_increase_authorized: false
branch_coverage_enforcement_authorized: false
```

Plain English: measure the protected surfaces separately, publish a safe
summary, then use that evidence to decide later whether any per-surface floor is
reasonable. Do not create a blocking protected-surface floor from guesses.

## Public Interface

Future Codex C may add one advisory report command, but it must not add a CI
gate.

Recommended report path:

`docs/quality_reports/coverage/protected_surface/<YYYY-MM-DD>-<short-commit>-protected-surface-coverage-advisory.json`

Recommended report schema:

```yaml
schema_version: "protected_surface_coverage_advisory.v1"
repository: "Tahjali11/Mythic-Edge"
measured_ref: ""
measured_commit: ""
coverage_command: ""
coverage_source: "src/mythic_edge_parser"
global_line_coverage_percent: 0.0
global_branch_coverage_percent: 0.0
global_line_floor_percent: 85.0
global_line_floor_status: "passed | failed | not_run"
branch_coverage_status: "advisory_only"
protected_surface_floor_status: "not_authorized"
groups:
  - group_id: ""
    protected_category_id: ""
    internal_project_area: ""
    coverage_scope_status: "measured | not_applicable_current_coverage_scope | unmapped | exempt_candidate"
    files:
      - path: ""
        line_coverage_percent: 0.0
        branch_coverage_percent: 0.0
        branch_coverage_status: "advisory_only"
        coverage_status: "measured | missing_from_coverage_xml | not_applicable_current_coverage_scope"
        notes: []
non_claims: []
raw_artifacts_committed: false
```

The report must use repo-relative paths only. It must not include absolute local
paths, raw terminal logs, raw XML, HTML coverage output, `.coverage` contents,
private logs, generated app data, secrets, workbook exports, or local-only
artifacts.

## Inputs

Allowed first-slice inputs:

- coverage XML produced by the repo-approved coverage command;
- the current Git ref and commit hash;
- `tools/check_protected_surfaces.py` category definitions or classifier
  output;
- tracked repo files under the current coverage source;
- `docs/internal_project_map.md` if Codex C needs area labels and the file is
  present on the branch;
- the #595 contract/review artifacts for global floor context.

Forbidden first-slice inputs:

- raw coverage databases;
- HTML coverage output;
- raw terminal coverage transcripts;
- local absolute paths;
- private logs;
- generated app data;
- secrets or credential-bearing values;
- workbook exports;
- runtime status files;
- failed-post queue artifacts;
- private JSONL artifacts;
- SQLite databases;
- raw Player.log content.

## Outputs

Allowed outputs:

- one public-safe JSON advisory report;
- aggregate percentages;
- per-group and per-file line coverage percentages for tracked repo files;
- branch coverage percentages labeled advisory-only;
- symbolic status labels;
- repo-relative paths;
- implementation handoff and review report.

Forbidden outputs:

- raw coverage XML contents copied into docs;
- `.coverage` data;
- HTML coverage directories;
- full missing-line terminal reports;
- local absolute paths;
- private/local artifact paths;
- raw log snippets;
- release-readiness, parser-correctness, security-assurance, or privacy-
  assurance claims.

## Candidate Protected-Surface Groups

Codex C should start from existing protected-surface categories and report each
group in three dimensions:

1. protected category;
2. repo-relative file path;
3. internal project area.

Candidate measurable Python groups:

| group_id | source category | candidate paths | first posture |
| --- | --- | --- | --- |
| `parser_event_classes` | `parser_event_classes` | `src/mythic_edge_parser/events.py` | measured if present in coverage XML |
| `parser_state_final_reconciliation` | `parser_state_final_reconciliation` | `src/mythic_edge_parser/app/state.py`, `src/mythic_edge_parser/app/models.py` | measured |
| `extractor_behavior` | `extractor_behavior` | `src/mythic_edge_parser/app/extractors.py` | measured |
| `match_game_identity` | `match_game_identity` | `src/mythic_edge_parser/app/gameplay_actions.py`, `src/mythic_edge_parser/app/state.py`, `src/mythic_edge_parser/app/transforms.py`, `src/mythic_edge_parser/parsers/**` | measured |
| `workbook_schema_and_exports` | `workbook_schema` | `src/mythic_edge_parser/app/sheet_schema.py`, `src/mythic_edge_parser/app/sheet_exports.py`, `src/mythic_edge_parser/app/transforms.py` | measured |
| `webhook_payload_and_transport` | `webhook_payload_shape` | `src/mythic_edge_parser/app/outputs.py`, `src/mythic_edge_parser/app/runner.py`, `src/mythic_edge_parser/app/transforms.py` | measured |
| `environment_runtime_python_paths` | `environment_runtime_paths` | `src/mythic_edge_parser/app/config.py` | measured |
| `analytics_schema_and_ingest` | protected-adjacent analytics area | `src/mythic_edge_parser/app/analytics_*.py`, analytics migration loader and ingest surfaces | advisory candidate, no floor |
| `local_app_security_and_artifact_safety` | protected-adjacent local app area | local app API, import, config, path, and setup status modules under `src/mythic_edge_parser/local_app/` | advisory candidate, no floor |

Candidate non-measurable or currently out-of-scope groups:

| group_id | reason |
| --- | --- |
| `apps_script_behavior` | Apps Script is not Python and is outside the current coverage source. |
| `workflow_authority_docs` | Authority docs are not executable Python coverage targets. |
| `workflow_ci_yaml` | GitHub workflow YAML is not Python coverage. |
| `local_artifact_checker_tools` | Tooling is currently outside `src/mythic_edge_parser`; measuring it would require a separate coverage-source policy decision. |
| `forbidden_local_artifact_paths` | Local/generated/private artifacts must not be committed; they are not coverage targets. |

Non-measurable groups must use `not_applicable_current_coverage_scope`, not
fake coverage percentages.

## Grouping Policy

The first report should group by all three:

- protected category, because this matches governance language;
- file path, because coverage findings must be actionable;
- internal project area, because roadmap planning needs ownership context.

No first-slice floor should be assigned to category, file, or project-area
groups. Candidate floors require later evidence.

## Branch Coverage Policy

Branch coverage must remain advisory-only.

The protected-surface report may include per-file or per-group branch coverage
when coverage XML provides it, but branch coverage must not:

- fail CI;
- fail local repo checks;
- define a threshold;
- override line coverage status;
- become a release-readiness or parser-correctness claim.

If branch data is unavailable or too noisy for a file, the report should use
`branch_coverage_status: advisory_unavailable` or omit the percentage with a
clear note.

## Advisory Versus Blocking Boundary

The first #605 implementation must not be blocking.

Allowed:

- parse current coverage XML;
- map measurable repo Python files to protected-surface groups;
- emit a public-safe advisory report;
- classify missing or non-measurable groups;
- recommend future floor candidates based on evidence.

Forbidden:

- adding a protected-surface coverage gate to CI;
- changing `.github/workflows/repo-checks.yml`;
- changing `tools/run_repo_checks.ps1`;
- raising the global 85.00% line floor;
- adding branch coverage enforcement;
- changing `pyproject.toml` coverage source or omit rules;
- failing builds on per-surface coverage;
- treating coverage as protected-surface authorization.

## Preconditions For Any Future Protected-Surface Floor

A later issue and contract are required before any protected-surface floor can
become blocking.

Minimum evidence before a floor proposal:

1. At least one advisory report from the current intended base.
2. A deterministic group map with tests.
3. Clear handling for files outside coverage scope.
4. A stale-ref policy matching the global floor lane.
5. Evidence that report output is public-safe and repo-relative.
6. Codex E review confirming no fake readiness or assurance claims.
7. Candidate threshold rationale per group.
8. Exception policy for:
   - generated files;
   - thin glue;
   - external integration code;
   - docs-only authority text;
   - files intentionally measured by other validation, not coverage.
9. A rollback or disable plan.
10. Explicit user approval for any CI or blocking behavior.

Candidate floors must be conservative and evidence-based. A low-value floor
that creates noisy bureaucracy should be deferred.

## Error Behavior

Future report tooling should fail closed as an advisory report failure when:

- coverage XML is missing;
- coverage XML is malformed;
- the measured commit is absent;
- protected-surface mapping is ambiguous;
- a protected Python path cannot be reconciled with coverage data;
- report output would include unsafe local or private values.

Advisory failures must not fail CI unless a later contract explicitly promotes
the report to a gate.

## Side Effects

This Codex B pass writes only this contract.

Future Codex C side effects may include:

- a report helper;
- focused tests;
- one intentionally committed public-safe advisory report;
- an implementation handoff.

Future Codex C must not create or commit raw coverage artifacts.

## Compatibility

The global 85.00% Python line floor remains authoritative for current coverage
enforcement.

The protected-surface report must not create a second global floor, duplicate
`tools/check_coverage_floor.py`, or conflict with the current repo check
workflow. If a helper needs coverage XML, it should consume the same XML family
produced by existing repo-approved coverage commands.

## Validation Requirements

For this Codex B contract:

```powershell
git diff --check -- docs\contracts\quality_protected_surface_coverage_floor_readiness.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_protected_surface_coverage_floor_readiness.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_protected_surface_coverage_floor_readiness.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

For later Codex C implementation:

- compare current repo state to this contract before editing;
- produce
  `docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md`;
- add focused tests for:
  - coverage XML parsing for file-level rates;
  - protected-surface category mapping;
  - non-Python or out-of-scope surfaces reported as not applicable;
  - missing/malformed coverage XML;
  - repo-relative path output;
  - branch coverage advisory-only status;
  - no per-surface gate or CI edit;
- run the current global coverage command to produce local ignored XML only
  when needed for the advisory report;
- validate any generated report JSON;
- run focused pytest for new helper tests;
- run Ruff on changed Python files;
- run `git diff --check`;
- run `py tools\check_agent_docs.py`;
- run path-scoped protected-surface and secret/private-marker scans on changed
  files.

For Codex E review:

- verify the report is advisory-only;
- verify branch coverage remains advisory-only;
- verify global 85.00% line floor was not raised;
- verify CI was not changed;
- verify raw coverage artifacts remain ignored and untracked;
- verify protected surfaces were not modified except approved report tooling;
- verify non-claims are present and not contradicted by report text.

## Acceptance Criteria

- This contract defines protected-surface coverage as advisory measurement for
  measurable protected Python files.
- This contract recommends advisory measurement/reporting only for the first
  slice.
- This contract defines candidate protected-surface groups.
- This contract requires category, file-path, and internal-project-area
  grouping.
- This contract keeps branch coverage advisory-only.
- This contract forbids a protected-surface gate, CI change, global floor
  increase, branch floor, and coverage-source change in #605.
- This contract defines future evidence required before any protected-surface
  floor can become blocking.
- This contract preserves parser, analytics, workbook, webhook, Apps Script,
  production, AI/model-provider, and private-artifact boundaries.

## Unknowns And Suspected Gaps

- Current per-file protected-surface coverage is unknown because #604 recorded
  only global line and branch percentages.
- The current protected-surface checker is path-based and diff-oriented, so a
  report helper may need a separate deterministic expansion step for tracked
  files.
- Some protected surfaces are not in the current Python coverage source and
  should not be forced into fake coverage numbers.
- It is unknown whether protected-surface coverage should later use one floor
  per category, one floor per project area, one floor per file, or no floor at
  all.

## Out Of Scope

- Implementing code in Codex B.
- Changing CI.
- Adding a protected-surface coverage gate.
- Raising the global 85.00% line floor.
- Adding branch coverage enforcement.
- Changing coverage source configuration.
- Running coverage in this Codex B pass.
- Changing parser behavior.
- Changing analytics schema or ingest behavior.
- Changing workbook schema.
- Changing webhook payload shape.
- Changing Apps Script behavior.
- Changing production behavior.
- Changing OpenAI/model-provider, AI, coaching, or Line Tracer behavior.
- Committing raw coverage artifacts or local-only artifacts.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/605

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/quality_protected_surface_coverage_floor_readiness.md

Goal:
Compare current coverage tooling, protected-surface classification, repo checks,
and #604 global line-floor behavior against the contract. Implement only the
first advisory protected-surface coverage measurement/reporting slice if the
comparison confirms it can be done without changing CI or adding a gate.

Do:
- Produce docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md.
- Add only advisory measurement/report tooling and focused tests if needed.
- Use repo-relative paths and public-safe report fields only.
- Keep branch coverage advisory-only.
- Keep the global 85.00% line floor unchanged.
- Keep raw coverage artifacts ignored and untracked.
- Report non-Python or out-of-current-scope protected surfaces as not applicable, not as fake percentages.

Do not:
- Change CI.
- Add a protected-surface coverage gate.
- Raise the global coverage floor.
- Add branch coverage enforcement.
- Change pyproject coverage source configuration.
- Change parser behavior, analytics schema, workbook schema, webhook payload shape, Apps Script behavior, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, or Line Tracer behavior.
- Commit .coverage files, coverage XML, HTML coverage output, raw terminal logs, private logs, generated app data, workbook exports, secrets, or local-only artifacts.

Validation:
- focused tests for new helper/report behavior
- validate any generated advisory JSON report
- py -m ruff check on changed Python files
- git diff --check
- py tools/check_agent_docs.py
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

End with validation results, raw-artifact status, protected-surface status,
remaining risks, next recommended role Codex E, and a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/605"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #605 and merged #595/#604 coverage gate evidence"
  contract_artifact: "docs/contracts/quality_protected_surface_coverage_floor_readiness.md"
  target_artifact: "docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md"
  risk_tier: "High workflow and validation-gate policy risk; low runtime risk"
  base_branch: "main"
  target_branch: "main_after_explicit_user_approval"
  branch: "codex/protected-surface-coverage-readiness-566"
  decision: "First slice should be advisory protected-surface coverage measurement/reporting only. No per-surface floor is authorized."
  branch_coverage_posture: "advisory_only"
  protected_surface_floor_status: "not_authorized"
  validation:
    - "git diff --check -- docs\\contracts\\quality_protected_surface_coverage_floor_readiness.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not change CI."
    - "Do not add a protected-surface coverage gate."
    - "Do not raise the global 85.00% line floor."
    - "Do not add branch coverage enforcement."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/production/OpenAI/AI/coaching behavior."
    - "Do not commit raw coverage artifacts or local-only artifacts."
```
