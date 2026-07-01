# Quality Protected-Surface Coverage Floor Candidate Selection Contract

## Module

`quality_protected_surface_coverage_floor_candidate_selection`

Plain English: this contract selects the first protected-surface coverage group
that is mature enough to discuss as a future floor candidate. A coverage floor
is a threshold that can fail validation when coverage drops below it. This
contract does not add such a floor.

This is a Codex B contract artifact only. It does not implement code, change
CI, change coverage settings, add a protected-surface floor, raise the global
85.00% line floor, enforce branch coverage, or change product behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/622
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/617
- Source PR: https://github.com/Tahjali11/Mythic-Edge/pull/620
- Contract artifact:
  `docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md`

## Tracker

Tracker #566 remains open for coverage-ratchet work. This child issue does not
complete the tracker.

## Owning Layer

Quality and validation tooling.

Coverage tooling owns measured execution evidence for a specific command,
coverage source, ref/commit, report artifact, and coverage configuration.
Coverage does not own parser truth, parser correctness, security assurance,
privacy assurance, release readiness, deploy readiness, production readiness,
analytics truth, AI truth, or coaching truth.

## Internal Project Area

Quality / validation gates.

## Truth Owner

The #617 advisory report owns only public-safe protected-surface coverage
measurement metadata for its measured ref and command. The parser/state layer
owns parser truth. This contract owns only the candidate-selection decision for
future protected-surface floor work.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
global coverage gate evidence
  + protected-surface advisory coverage report
  + protected-surface category vocabulary
  -> candidate selection contract
  -> later floor proposal issue, if explicitly authorized
```

Forbidden reverse flow:

- Candidate selection must not change parser/state behavior.
- Candidate selection must not authorize CI, coverage, or workflow gate changes.
- Coverage numbers must not imply parser correctness.
- Coverage numbers must not imply security assurance, privacy assurance,
  release readiness, deploy readiness, production readiness, analytics truth,
  AI truth, or coaching truth.

## Files Owned By This Contract

- `docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md`

Future artifacts may be created only by later authorized roles:

- `docs/contract_test_reports/quality_protected_surface_coverage_floor_candidate_selection.md`
- `docs/implementation_handoffs/quality_protected_surface_coverage_floor_candidate_selection_comparison.md`
- a later issue-specific floor implementation contract, if the owner approves
  moving from candidate selection to implementation.

This contract does not authorize edits to:

- `.github/workflows/repo-checks.yml`
- `pyproject.toml`
- `tools/check_coverage_floor.py`
- `tools/generate_protected_surface_coverage_report.py`
- `tools/run_repo_checks.ps1`
- parser, analytics, workbook, webhook, Apps Script, Google Sheets, OpenAI,
  AI, coaching, Line Tracer, production, fixtures, corpus, or runtime code.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #622
- Tracker #566
- Project roadmap #568
- Issue #617
- PR #620
- `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/contracts/quality_protected_surface_coverage_floor_readiness.md`
- `docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`
- `docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md`
- `docs/contract_test_reports/quality_protected_surface_coverage_current_base_remeasurement.md`
- `docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json`
- `tools/generate_protected_surface_coverage_report.py`
- `tools/check_coverage_floor.py`
- `tests/test_protected_surface_coverage_report.py`
- `.github/workflows/repo-checks.yml`
- `pyproject.toml`

## Observed Current Behavior

Current coverage posture:

- #595 / PR #604 implemented the blocking 85.00% global Python line coverage
  floor.
- #605 / PR #609 implemented protected-surface coverage advisory measurement
  and report tooling.
- #612 / PR #615 interpreted the first protected-surface report and did not
  authorize a protected-surface floor from that evidence.
- #617 / PR #620 produced a current-base protected-surface coverage advisory
  report.
- Branch coverage remains advisory-only.
- Protected-surface floors remain unauthorized.
- The global 85.00% line floor remains unchanged.

The #617 report records:

```yaml
report: docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json
measured_ref: origin/main
measured_commit: 94d337c635769c214c5beecabef93932033210f3
global_line_coverage_percent: 87.55
global_branch_coverage_percent: 74.80
global_line_floor_status: passed
branch_coverage_status: advisory_only
protected_surface_floor_status: not_authorized
protected_surface_floor_authorized: false
global_line_floor_increase_authorized: false
branch_coverage_enforcement_authorized: false
ci_change_authorized: false
raw_artifacts_committed: false
```

This contract was written from a branch tracking current `origin/main` at
`8791928`. That means the #617 report is the accepted source evidence for this
candidate-selection decision, but any later floor implementation must re-check
the intended base before changing CI or gates.

## Candidate Group Decision

`parser_state_final_reconciliation` should become Mythic Edge's first
protected-surface floor candidate.

Decision:

```yaml
candidate_group: parser_state_final_reconciliation
candidate_status: selected_for_future_floor_proposal
candidate_posture: line_only_conservative_candidate
floor_implementation_authorized_now: false
ci_change_authorized_now: false
branch_coverage_enforcement_authorized_now: false
global_line_floor_increase_authorized_now: false
```

Why this is the best first candidate:

- It is small enough to keep the first protected-surface floor understandable.
- It maps to a high-risk parser truth surface: parser state and final
  reconciliation.
- It has two measured Python files, not a one-file sample.
- Both measured files are close to one another, reducing outlier risk.
- It has a clear internal project area: Parser.
- Its measured line coverage is above the active global 85.00% floor with a
  moderate buffer.

Measured #617 evidence:

| File | Line coverage | Branch posture |
| --- | ---: | --- |
| `src/mythic_edge_parser/app/models.py` | 90.45% | advisory-only |
| `src/mythic_edge_parser/app/state.py` | 90.21% | advisory-only |

Summary:

```yaml
files: 2
average_line_coverage_percent: 90.33
minimum_line_coverage_percent: 90.21
branch_coverage_posture: advisory_only
```

## Threshold-Policy Recommendation

No threshold is implemented by this contract.

If a later issue explicitly authorizes implementation, the first proposal
should be a conservative line-only candidate below the fresh measured minimum.
The reasonable future proposal range is:

```yaml
future_candidate_floor_range_percent: "87.00 to 88.00"
preferred_initial_candidate_percent: 88.00
metric_allowed: line_coverage_only
metric_forbidden: branch_coverage
shape_preference: per_candidate_group_with_per_file_minimum_guard
```

Plain English: because the current minimum file coverage is 90.21%, a future
88.00% line-only guard would leave a little room for harmless line churn while
still catching meaningful erosion in `models.py` or `state.py`.

A later implementation issue must not choose a threshold from this contract
alone. It must first confirm:

1. the current intended base still measures both candidate files at or above
   90.00% line coverage;
2. the global 85.00% line floor still passes;
3. no branch coverage enforcement is introduced;
4. the owner explicitly authorizes a floor or dry-run gate;
5. Codex E reviews the candidate threshold and failure message before merge.

If fresh current-base measurement drops either candidate file below 90.00%,
the future floor proposal should pause and route to test-hardening or
remeasurement instead of implementation.

## Overlap Handling

`parser_state_final_reconciliation` overlaps conceptually with
`match_game_identity` because parser state and models participate in match and
game identity workflows.

The future floor must handle that overlap this way:

- The selected candidate is not a `match_game_identity` floor.
- A failure must be explained as coverage erosion in parser state/final
  reconciliation support, not as proof of match/game identity breakage.
- The floor must not change match identity, game identity, deduplication,
  parser final reconciliation, parser event classes, fixtures, or corpus
  behavior.
- If future work wants a `match_game_identity` floor, it needs a separate
  issue because that group has 28 files and a lower current file minimum
  of 83.08%.

## Deferred Group Classification

| Group | Classification | Reason |
| --- | --- | --- |
| `match_game_identity` | promising_deferred | Broad 28-file parser group with strong average but 83.08% minimum; needs overlap and file-minimum policy before any floor. |
| `extractor_behavior` | watch_list | Strong line coverage, but one file only. A single-file floor needs separate rationale. |
| `workbook_schema_and_exports` | promising_deferred | Strong average, but current file minimum is 83.08%, below the active global line floor. |
| `parser_event_classes` | watch_list | One-file 100% signal; useful to watch, too small for this first floor. |
| `environment_runtime_python_paths` | watch_list | One-file 100% signal; useful to watch, too small for this first floor. |
| `local_app_security_and_artifact_safety` | test_hardening_or_subgrouping | Useful group, but too broad and uneven for a first floor. |
| `webhook_payload_and_transport` | test_hardening_first | Current average and minimum are too close to or below the global floor. |
| `analytics_schema_and_ingest` | test_hardening_or_regrouping | Current minimum is too low and the group is too uneven. |
| `apps_script_behavior` | not_applicable_current_python_coverage_scope | Apps Script is outside the current Python coverage source. |
| `workflow_authority_docs` | not_applicable_current_python_coverage_scope | Governance docs are not executable Python coverage targets. |
| `workflow_ci_yaml` | not_applicable_current_python_coverage_scope | GitHub workflow YAML is outside the current Python coverage source. |
| `local_artifact_checker_tools` | not_applicable_current_python_coverage_scope | Current coverage source does not include these quality tools. |
| `forbidden_local_artifact_paths` | not_applicable_current_python_coverage_scope | Local/generated/private artifact paths are not coverage targets. |

## Public Interface

This contract defines workflow and validation policy only.

Allowed future public interface, if separately authorized:

- a narrowly scoped protected-surface line floor for
  `parser_state_final_reconciliation`;
- public-safe failure output that names only repo-relative files, measured
  values, required floor, command label, branch-coverage advisory status, and
  stale-ref guidance.

Forbidden from this contract:

- active CI changes;
- active `pyproject.toml` changes;
- new `--cov-fail-under` values beyond the current global 85.00% line floor;
- branch coverage floors;
- protected-surface floors for other groups;
- parser or product behavior changes.

## Inputs

Required inputs for this contract:

| Input | Source | Required fields |
| --- | --- | --- |
| Problem representation | Issue #622 | candidate group, source report, boundaries, acceptance criteria |
| Source measurement | #617 advisory report | measured ref, measured commit, global line percent, branch posture, group files and line rates |
| Prior policy | #612 candidate floor policy contract | line-only policy, stale-ref policy, branch advisory boundary, blockers |
| Active global floor | #595 / PR #604 and `tools/check_coverage_floor.py` | 85.00% line floor, branch advisory message |

Inputs that must not be used:

- raw coverage databases;
- raw terminal logs;
- private/local artifacts;
- raw Player.log data;
- generated SQLite files;
- workbook exports;
- secrets, credentials, tokens, keys, webhook URLs, spreadsheet IDs, or
  environment values.

## Outputs

This contract outputs:

- candidate group decision;
- deferred group classification;
- non-binding threshold-policy recommendation;
- overlap handling;
- validation and review requirements for any later floor proposal.

No runtime output, report helper output, coverage XML, CI output, workbook
output, webhook payload, SQLite data, or production artifact is created by this
contract.

## Invariants

- The global 85.00% Python line coverage floor remains unchanged.
- Branch coverage remains advisory-only.
- Protected-surface floor status remains `not_authorized`.
- No protected-surface floor may be implemented without a later issue, fresh
  current-base validation, explicit owner approval, and Codex E review.
- Coverage numbers must stay evidence, not parser truth.
- The future candidate may use line coverage only.
- Any future failure message must be public-safe and must not echo private
  paths, raw coverage artifact paths, raw logs, secrets, or local-only data.
- Raw coverage artifacts must remain local/ignored and uncommitted.

## Error Behavior

If a later thread finds any of the following, it must not implement a floor:

- the source report is missing, malformed, or not parseable as JSON;
- the intended base has advanced and no fresh current-base measurement exists;
- either candidate file drops below 90.00% line coverage before floor
  implementation;
- the global 85.00% line floor fails;
- branch coverage is used as a threshold;
- the future implementation would require changing parser behavior or tests
  unrelated to coverage reporting;
- failure output would expose private/local paths or raw artifact locations;
- CI or `pyproject.toml` changes are broader than the explicitly approved
  candidate group.

If any of those occur, route back to Codex B for contract revision or Codex A
for reframing.

## Side Effects

Allowed side effect in this thread:

- create this docs-only contract artifact.

Forbidden side effects:

- run or commit new coverage measurements;
- commit `.coverage`, coverage XML, HTML coverage output, terminal logs, or
  local-only artifacts;
- edit CI, coverage config, parser code, tests, fixtures, corpus files,
  analytics code, workbook code, webhook code, Apps Script, Google Sheets,
  OpenAI/model-provider code, AI/coaching code, or production behavior;
- create, close, or mutate GitHub issues or PRs from this contract alone.

## Dependency Order

If future implementation is explicitly authorized, the required order is:

1. Codex A or owner confirms an implementation issue and approval record.
2. Codex B updates or writes a floor implementation contract if the approval
   includes concrete CI/tooling changes.
3. Codex C remeasures the current intended base and compares against this
   candidate contract.
4. Codex C implements only the approved line-only candidate mechanism.
5. Codex E verifies scope, threshold, stale-ref behavior, failure text,
   raw-artifact safety, and branch advisory status.
6. Codex F/G handle publication or integration only after review is clean.

## Compatibility

This contract must remain compatible with:

- the active global 85.00% Python line floor;
- existing protected-surface advisory report schema
  `protected_surface_coverage_advisory.v1`;
- advisory-only branch coverage;
- existing `tools/check_coverage_floor.py` global-floor behavior;
- existing protected-surface scanner and secret/private-marker scanner
  boundaries.

No later implementation may silently convert this candidate selection into a
repo-wide protected-surface floor.

## Validation Required

For this docs-only contract:

```powershell
git diff --check -- docs\contracts\quality_protected_surface_coverage_floor_candidate_selection.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md
'@ | py tools\check_secret_patterns.py --paths-from-stdin
```

For a later candidate-floor implementation issue, validation must include:

```powershell
git status --short --branch
git rev-parse origin/main
py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-94d337c-protected-surface-coverage-advisory.json
py -m pytest -q tests\test_protected_surface_coverage_report.py
py tools\check_coverage_floor.py --coverage-xml <local ignored coverage xml> --command-label "<approved current-base coverage command>"
git diff --check
py tools\check_agent_docs.py
```

A later implementation must also prove:

- the global 85.00% line floor still passes;
- branch coverage remains advisory-only;
- raw coverage artifacts are not tracked;
- no forbidden product surfaces changed;
- path-scoped protected-surface and secret/private-marker scans pass over the
  changed files.

## Acceptance Criteria

- The contract selects or rejects `parser_state_final_reconciliation`.
- The contract preserves `protected_surface_floor_authorized: false`.
- The contract preserves branch coverage as advisory-only.
- The contract preserves the global 85.00% line floor unchanged.
- The contract explains why other groups are deferred.
- The contract defines a non-binding future threshold range without
  implementing or authorizing it.
- The contract defines stale-ref and fresh-measurement rules.
- The contract preserves parser, analytics, workbook, webhook, Apps Script,
  Google Sheets, OpenAI, AI, coaching, Line Tracer, production, private
  artifact, and generated artifact boundaries.

## Open Questions And Contract Risks

- The #617 report was measured at `94d337c`, while current `origin/main` has
  advanced. This is acceptable for candidate selection, but not for floor
  implementation.
- Existing report data exposes per-file line percentages, not a dedicated
  candidate-floor enforcement shape. A later implementation must choose and
  review that shape explicitly.
- A future 88.00% threshold is reasonable only if fresh measurement still shows
  a clear buffer above that value.
- `parser_state_final_reconciliation` is a parser truth surface, so any future
  implementation must avoid changing parser behavior just to satisfy coverage.

## Next Workflow Action

Next recommended role: Codex E contract-test/review for #622.

Do not route directly to a floor implementation unless the owner explicitly
authorizes a later implementation issue or approval record.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/622

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract artifact:
docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md

Source evidence:
- docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json
- docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md
- docs/contract_test_reports/quality_protected_surface_coverage_current_base_remeasurement.md
- docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md

Goal:
Review whether the #622 contract correctly selects `parser_state_final_reconciliation`
as a future protected-surface floor candidate without authorizing any floor,
CI change, global line-floor increase, branch coverage enforcement, parser
behavior change, or product behavior change.

Verify:
- candidate selection is supported by the #617 report;
- deferred group classifications match the report evidence;
- branch coverage remains advisory-only;
- protected-surface floor status remains not authorized;
- threshold guidance is non-binding and requires fresh measurement before use;
- stale-ref, raw-artifact, privacy, and protected-surface boundaries are clear;
- no implementation files, CI files, coverage settings, parser files, fixtures,
  or runtime/product files changed.

Suggested validation:
- git status --short --branch
- py -m json.tool docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json
- git diff --check -- docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md
- py tools/check_agent_docs.py
- path-scoped protected-surface scan over the contract/report files
- path-scoped secret/private-marker scan over the contract/report files

Do not:
- implement a floor;
- change CI;
- raise the global 85.00% line floor;
- enforce branch coverage;
- run or commit new coverage measurements unless explicitly authorized;
- change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior;
- close tracker #566.

Final output:
- findings first;
- validation results;
- whether the contract can route to closure for #622;
- whether a future implementation issue is recommended;
- remaining risks;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/622"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json"
  target_artifact: "docs/contract_test_reports/quality_protected_surface_coverage_floor_candidate_selection.md"
  contract_artifact: "docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md"
  risk_tier: "Medium-High workflow/validation-gate risk; low runtime risk"
  branch: "codex/protected-surface-coverage-floor-candidate-622"
  candidate_group: "parser_state_final_reconciliation"
  decision: "Selected as first future protected-surface line-only floor candidate; implementation not authorized."
  floor_authorized_now: false
  ci_change_authorized: false
  branch_coverage_enforcement_authorized: false
  validation:
    - "git diff --check -- docs\\contracts\\quality_protected_surface_coverage_floor_candidate_selection.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan over contract"
    - "path-scoped secret/private-marker scan over contract"
  stop_conditions:
    - "Do not implement a protected-surface floor from this contract alone."
    - "Do not change CI or pyproject.toml."
    - "Do not raise the global 85.00% line floor."
    - "Do not enforce branch coverage."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not commit raw coverage artifacts, private logs, generated data, SQLite files, workbook exports, secrets, credentials, private paths, or local-only artifacts."
```
