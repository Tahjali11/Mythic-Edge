# Repo Extraction Candidate Matrix Contract

## Module

`repo_extraction_candidate_matrix`

Plain English: this contract defines how Mythic Edge should produce a
repo-owned audit matrix for possible future repository extraction candidates.
The matrix is a governance and planning artifact. It may classify path groups,
scripts, docs, fixtures, tools, and workflows as possible future extraction
candidates, but it must not move files, split repositories, change imports,
change packaging, publish packages, add CI gates, or change runtime behavior.

The matrix should help Mythic Edge answer "what could eventually move, why,
what blocks it, who consumes it, and what proof is needed first?" It must not
answer "move it now."

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/465
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/456
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/548
- Previous merge commit: `5aac58f07407ad6a582ea5907518d29a59de713d`
- Related ADR: `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- Related boundary contract: `docs/contracts/internal_project_boundaries.md`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388

Tracker #388 remains open and inactive for parser-evidence pipeline activation.
This issue is a governance/audit child selected after #456. It does not
activate #388 or #381.

## Owning Layer

Primary owner: Quality / Governance.

This contract is about repository coordination, boundary audit vocabulary, and
future workflow routing. It does not create runtime product behavior.

## Internal Project Area

Quality / Governance, with read-only classification references to:

- Parser;
- Corpus / Provenance;
- Analytics;
- Local App / UI;
- Workbook / Transport;
- Shared Support;
- Generated / Local Artifacts;
- External / Collaboration Surface;
- Future AI Integration.

## Truth Owner

The contract and later matrix own governance classification only.

Truth boundaries remain unchanged:

- Parser/state remains truth owner for parser-managed facts.
- Corpus / Provenance remains evidence/provenance support, not parser truth.
- Analytics may own deterministic derived analytics only where separately
  contracted.
- Local App / UI owns access, display, and orchestration only.
- Workbook / Transport consumes parser-normalized rows and does not own parser
  truth.
- AI/model-provider surfaces remain deferred consumers and do not own parser,
  analytics, schema, validation, merge, deploy, or hidden-game truth.

A repository boundary is an ownership and packaging boundary, not a truth
shortcut.

## Bridge-Code Status

`shared_support`

This contract defines a shared governance report shape. It may inspect bridge
code and shared support paths, but it does not change their behavior or
classification by itself.

Allowed data flow:

```text
committed repo metadata and current governance artifacts
  -> extraction candidate matrix
  -> follow-up routing recommendations
```

Forbidden reverse flow:

```text
extraction matrix classification
  -/-> file move
  -/-> import/package/CI change
  -/-> parser truth transfer
  -/-> analytics truth transfer
  -/-> production readiness
  -/-> source-repo or sibling-repo lifecycle action
```

## Source Artifacts Inspected For This Contract

- GitHub issue #465
- GitHub tracker #388
- GitHub issue #456
- GitHub PR #548
- GitHub issues #340 and #463 as adjacent context only
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/implementation_handoffs/internal_project_boundaries_comparison.md`
- `docs/contract_test_reports/internal_project_boundaries.md`
- `docs/internal_project_map.md`
- `docs/project_roadmap.md`
- `README.md`
- `pyproject.toml`
- `.github/workflows/`
- `src/mythic_edge_parser/`
- `frontend/`
- `tools/`
- `tests/`
- `tests/fixtures/`
- `docs/contracts/`
- `docs/problem_representations/`
- `docs/implementation_handoffs/`
- `docs/contract_test_reports/`

Sibling repositories were not inspected or mutated in this Codex B pass.
Future sibling-repo reference checks require an explicit
`allowed_read_only_references` handoff entry.

## Observed Current Behavior

The main repository is still the primary integration repository. It contains:

- parser package code under `src/mythic_edge_parser/`;
- parser, evidence, analytics, workbook/transport, and shared support modules
  under the broad `src/mythic_edge_parser/app/` namespace;
- local app backend under `src/mythic_edge_parser/local_app/`;
- React/Vite frontend under `frontend/`;
- repo tooling under `tools/`;
- workbook/App Script transport support under `tools/google_apps_script/`;
- committed public-safe parser/corpus fixtures under `tests/fixtures/`;
- flat docs artifact directories under `docs/contracts/`,
  `docs/implementation_handoffs/`, and `docs/contract_test_reports/`;
- a single Python package name, `mythic-edge-parser`;
- package data for analytics and Match Journal migrations under the existing
  package root.

ADR-0006 is accepted and says Mythic Edge remains monorepo-first until a future
issue, contract, review, accepted ADR path when needed, and explicit
user-approved migration plan authorize extraction.

Issue #340 owns the analytics transfer/private-spoke strategy question.
Issue #463 owns behavior-preserving decomposition of oversized files. Issue
#465 must not subsume or implement either one.

## Problem Statement

Mythic Edge needs a durable extraction candidate matrix so repository-splitting
decisions are based on ownership, stable interfaces, dependency direction,
privacy posture, tests, versioning, consumers, and rollback instead of file
size, vibes, or the mere existence of sibling repositories.

Without this contract, a future thread could propose moving files because a
path is large or because another repo exists, while skipping:

- stable input/output contract proof;
- dependency direction proof;
- test portability proof;
- versioning strategy;
- consumer compatibility proof;
- private/protected-surface policy;
- rollback and migration notes;
- truth-owner preservation.

## First Bad Value

The first bad value is any report row, readiness label, candidate score,
follow-up issue, or route recommendation that implies:

- the file should move now;
- a sibling repo is now the truth owner;
- imports/packages/CI should change;
- parser behavior, analytics behavior, local app behavior, workbook transport,
  Apps Script, Google Sheets, OpenAI/model-provider behavior, AI/coaching, or
  production behavior should change;
- #388 or #381 is activated;
- parser behavior readiness, pipeline activation readiness, private harvest,
  fixture promotion, corpus status change, merge readiness, deploy readiness,
  or release readiness is now true.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/repo_extraction_candidate_matrix.md`

Expected later report artifact:

- `docs/contract_test_reports/repo_extraction_candidate_matrix.md`

Possible later implementation handoff, only if a future workflow uses Codex C
to generate the report:

- `docs/implementation_handoffs/repo_extraction_candidate_matrix_comparison.md`

This contract does not own source code, tests, frontend code, workflows,
fixtures, package metadata, sibling repos, generated data, or runtime
artifacts.

## Public Interface

The public interface is the later matrix report shape. The report must be
Markdown and public-safe.

Required report header fields:

| Field | Requirement |
| --- | --- |
| `report_schema` | `repo_extraction_candidate_matrix.v1` |
| `source_issue` | Link to issue #465 |
| `source_contract` | This contract path |
| `generated_from_ref` | Git ref or commit used for inspection |
| `generated_at_utc` | UTC timestamp |
| `repository` | `Tahjali11/Mythic-Edge` |
| `repository_url` | `https://github.com/Tahjali11/Mythic-Edge` |
| `report_status` | See report status vocabulary |
| `non_claims` | Required non-claims |

Required matrix columns:

| Column | Meaning |
| --- | --- |
| `candidate_id` | Stable public-safe ID for the row |
| `path_or_module_group` | Repo-relative path, glob, or named module group |
| `current_project_area` | Internal project area from `docs/internal_project_map.md` |
| `current_classification` | clear owner, shared support, bridge code, ambiguous, generated/excluded |
| `proposed_owning_repo` | Candidate future owner or `stay_primary_repo` |
| `visibility_candidate` | `public`, `private`, `undecided`, or `not_applicable` |
| `candidate_type` | Extraction/decomposition/transfer/stay classification |
| `non_owning_consumers` | Known consumers that would depend on the owner |
| `source_inputs` | Public-safe committed source inputs used by the candidate |
| `outputs_or_artifacts` | Public-safe outputs/artifacts produced |
| `public_api_or_artifact_contract_status` | Contract maturity |
| `dependency_direction` | Allowed dependency direction |
| `private_or_protected_data_risk` | Privacy/protected-surface risk label |
| `test_coverage_and_portability` | Current test evidence and portability notes |
| `release_cadence_fit` | How well the candidate fits independent releases |
| `extraction_readiness` | `red`, `yellow`, `green`, or `not_candidate` |
| `blockers` | Concrete blockers to extraction |
| `recommended_next_issue` | Existing issue, new issue type, or no action |
| `rollback_or_migration_notes` | Required rollback/migration proof before movement |
| `non_claims` | Row-level non-claims |

Optional columns:

- `related_issue`
- `related_contract`
- `related_adr`
- `package_or_distribution_strategy`
- `consumer_compatibility_tests_needed`
- `sibling_repo_reference_needed`
- `owner_confidence`
- `review_notes`

## Inputs

Allowed inputs for the later report:

- committed repo files on the selected Mythic Edge ref;
- `git ls-files` output used transiently for inventory;
- `rg --files` output used transiently for inventory;
- current GitHub issue #465 and tracker #388;
- adjacent issue #340 as analytics transfer context only;
- adjacent issue #463 as decomposition context only;
- accepted ADRs, especially ADR-0006;
- `docs/internal_project_map.md`;
- existing contracts, implementation handoffs, and contract-test reports;
- `README.md`, `docs/project_roadmap.md`, and `pyproject.toml`;
- `.github/workflows/` committed workflow definitions;
- repo-owned tools and tests;
- public-safe committed fixtures.

Forbidden inputs:

- raw or private `Player.log` / `UTC_Log` content;
- app-data, live MTGA, network, firewall/drop, packet, OS/router,
  diagnostics, drift, watcher, tailer, private smoke, or private harvest
  evidence;
- generated SQLite databases;
- runtime artifacts;
- workbook exports;
- local absolute paths;
- secrets, credentials, tokens, API keys, webhook URLs;
- raw private reports;
- sibling repository content unless explicitly authorized through
  `allowed_read_only_references`;
- source-repo mutation, branch, issue, PR, comment, review, label, or status
  changes in any sibling repository.

## Outputs

Primary later output:

- `docs/contract_test_reports/repo_extraction_candidate_matrix.md`

The output is final as an audit snapshot for its inspected commit. It is not
final as extraction authorization.

Required report status vocabulary:

- `matrix_ready_for_review`
- `matrix_ready_with_open_questions`
- `matrix_partial_due_to_missing_reference`
- `matrix_blocked_by_checkout_mismatch`
- `matrix_blocked_by_forbidden_input`
- `matrix_blocked_by_sibling_repo_scope`
- `matrix_failed_validation`

Required candidate type vocabulary:

- `stay_primary_repo`
- `repo_extraction_candidate`
- `private_spoke_transfer_candidate`
- `public_spoke_candidate`
- `internal_decomposition_only`
- `optional_dependency_candidate`
- `shared_support_needs_interface_hardening`
- `generated_or_local_artifact_excluded`
- `defer_to_existing_issue`
- `not_candidate`

Required proposed owning repo vocabulary:

- `Tahjali11/Mythic-Edge`
- `Tahjali11/Mythic-Edge-Corpus`
- `Tahjali11/Mythic-Edge-Analytics`
- `future_mythic_edge_parser_repo`
- `future_mythic_edge_governance_or_tooling_repo`
- `future_ai_or_advisor_repo`
- `no_separate_repo`
- `undecided`

Sibling repo labels are destination candidates only. They do not authorize
inspection, mutation, dependency changes, or issue creation in those repos.

## Extraction Readiness Vocabulary

`green`

- Candidate may be worth a future Codex A extraction or transfer planning
  issue.
- Public interface or artifact contract is stable enough to discuss.
- Dependency direction is one-way and documented.
- Tests are portable or portable-test gaps are small and concrete.
- Private/protected-surface risk is low or controlled by existing policy.
- Rollback path is plausible.
- Green does not authorize moving files.

`yellow`

- Candidate has some separation signals but needs interface hardening,
  dependency cleanup, test portability, versioning, privacy review, or
  consumer compatibility proof before extraction planning.
- Yellow should usually route to a contract, decomposition, interface, or
  validation issue before any migration issue.

`red`

- Candidate should stay in the primary repo for now.
- Reasons may include parser truth ownership, unstable interfaces, circular
  dependencies, private/protected data risk, missing tests, tight local app
  coupling, workbook/transport coupling, migration complexity, or no rollback
  path.

`not_candidate`

- The row is generated/local/private/excluded, a downstream display surface
  that should not move, or a path where extraction is not useful.

Readiness labels are planning labels only. They are not implementation
authorization, merge readiness, deploy readiness, release readiness, production
readiness, parser behavior readiness, pipeline activation readiness, analytics
truth, AI truth, or coaching truth.

## Invariants

- The matrix must be repo-relative and public-safe.
- The matrix must not include local absolute paths.
- The matrix must not include raw private logs, raw Player.log excerpts, raw
  UTC_Log contents, generated SQLite databases, runtime artifacts, workbook
  exports, secrets, credentials, tokens, API keys, or webhook URLs.
- The matrix must not move files, rename modules, change imports, change
  package metadata, or change CI.
- The matrix must not make a sibling repo a truth owner by implication.
- The matrix must distinguish extraction candidates from decomposition
  candidates.
- The matrix must distinguish private-spoke transfer candidates from public
  extraction candidates.
- The matrix must route #340-owned analytics/private-spoke transfer questions
  back to #340 or a child issue, not solve them inside #465.
- The matrix must route #463-owned oversized-file decomposition questions back
  to #463 or a child issue, not solve them inside #465.
- `parser_behavior_ready` must remain `false`.
- `pipeline_activation_ready_for_issue_388` must remain `false`.
- `private_harvest_authorized` must remain `false`.
- `fixture_promotion_authorized` must remain `false`.
- `corpus_status_change_authorized` must remain `false`.

## Error Behavior

If the local checkout remote does not match
`https://github.com/Tahjali11/Mythic-Edge`, stop before editing.

If the current branch does not include the previous merge commit
`5aac58f07407ad6a582ea5907518d29a59de713d`, stop or create a clean worktree
from current `origin/main`.

If the report generator finds a dirty worktree with unrelated changes, preserve
those changes and use a clean issue-specific worktree.

If a sibling repo is needed but the handoff lacks `allowed_read_only_references`,
mark the affected rows `matrix_partial_due_to_missing_reference` or
`matrix_blocked_by_sibling_repo_scope` rather than inspecting the sibling repo.

If any forbidden private/local/raw marker is detected in the candidate matrix,
validation must fail and the report must be rewritten without echoing the
forbidden value.

If an extraction-readiness classification conflicts with ADR-0006 or
`docs/internal_project_map.md`, record the conflict as an open question and do
not route implementation.

## Side Effects

Allowed side effects for Codex B:

- create or update this contract file only.

Allowed side effects for a later report pass:

- create or update
  `docs/contract_test_reports/repo_extraction_candidate_matrix.md`;
- optionally create
  `docs/implementation_handoffs/repo_extraction_candidate_matrix_comparison.md`
  if the workflow routes through Codex C.

Forbidden side effects:

- file moves;
- repository split;
- import changes;
- package metadata changes;
- package publication;
- CI gate changes;
- parser/runtime behavior changes;
- analytics behavior changes;
- local app/UI behavior changes;
- workbook/webhook/App Script/Sheets behavior changes;
- OpenAI/model-provider runtime behavior;
- issue creation, PR creation, comments, labels, milestones, or status checks
  in this or sibling repos;
- generated/private/local artifacts.

## Dependency Order

1. Keep this contract as the source for the report shape.
2. Generate or manually produce the report from current committed repo state.
3. Run report-focused validation.
4. Route follow-up recommendations one issue at a time.
5. Create new extraction, transfer, decomposition, interface-hardening, or
   optional-dependency issues only when explicitly authorized.
6. Do not perform any migration until a later issue, contract, review,
   validation, and user-approved migration plan authorize it.

## Compatibility

The later matrix must preserve current monorepo compatibility assumptions:

- package name remains `mythic-edge-parser`;
- import root remains `mythic_edge_parser`;
- `src/mythic_edge_parser/app/` may remain broad;
- flat docs artifact directories remain valid;
- flat tests remain valid;
- frontend remains under `frontend/`;
- tools remain under `tools/`;
- existing sibling repos are not required dependencies of this repo by
  implication;
- private analytics and future corpus/parser repos remain optional/future
  planning surfaces unless separately contracted.

## Follow-Up Routing Rules

Allowed follow-up recommendations:

- `no_action`
- `Codex_A_problem_representation`
- `Codex_B_contract`
- `Codex_C_report_only_implementation`
- `route_to_issue_340`
- `route_to_issue_463`
- `route_to_ADR_update`
- `route_to_optional_dependency_contract`
- `route_to_private_spoke_transfer_plan`
- `route_to_parser_public_interface_contract`
- `route_to_corpus_release_contract`
- `route_to_test_portability_issue`

Forbidden follow-up recommendations:

- immediate file move;
- immediate repo split;
- immediate import/package/CI change;
- immediate sibling-repo issue/PR creation without authorization;
- immediate parser, analytics, local app, workbook, webhook, Apps Script,
  Google Sheets, AI/coaching, or production behavior change.

## Tests Required

Codex B validation for this contract:

```bash
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/repo_extraction_candidate_matrix.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/repo_extraction_candidate_matrix.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/repo_extraction_candidate_matrix.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Later report validation:

```bash
git status --short --branch
git ls-files
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

If the report includes generated inventory summaries, it must name the
inventory commands used, but it must not commit raw temporary inventory files.

## Acceptance Criteria

- Contract exists at `docs/contracts/repo_extraction_candidate_matrix.md`.
- Contract defines the matrix columns and controlled vocabulary.
- Contract defines the inspection scope and sibling-repo boundary.
- Contract distinguishes extraction, decomposition, transfer, optional
  dependency, shared support, and no-action rows.
- Contract preserves ADR-0006 monorepo-first policy.
- Contract preserves #340 and #463 as adjacent scopes.
- Contract preserves all false parser-evidence readiness and authorization
  flags.
- Contract defines report-focused validation.
- Contract routes the next role without authorizing implementation, file
  movement, repo splitting, import/package/CI changes, protected-surface
  changes, or sibling-repo mutation.

## Open Questions For The Report

- Should any candidate receive a `green` label before a dedicated interface
  contract exists, or should `green` mean only "ready for Codex A planning"?
- Should sibling repo issue queues be inspected in the report pass, and if so,
  which repos should be named in `allowed_read_only_references`?
- Should the later report use only `red/yellow/green`, or include an optional
  numerical score for sorting?
- Which path groups should route to #340 versus stay under #465?
- Which oversized-file candidates should route to #463 rather than become repo
  extraction candidates?

## Next Workflow Action

Next recommended role: Codex C if the user wants the report artifact produced
from this contract, otherwise Codex E for contract review.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Report Implementer for issue #465.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/465

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/456

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/548

Contract:
docs/contracts/repo_extraction_candidate_matrix.md

Goal:
Produce the repo extraction candidate matrix report at
docs/contract_test_reports/repo_extraction_candidate_matrix.md.

Scope:
- Build a public-safe, repo-relative matrix from committed Mythic Edge files,
  ADR-0006, internal project boundary docs, current docs/contracts/reports, and
  current GitHub issue context.
- Classify extraction candidates, decomposition-only candidates,
  private-spoke transfer candidates, shared-support/interface-hardening
  candidates, and no-action rows.
- Preserve #340 and #463 as adjacent scopes rather than solving them inside
  this report.

Protected boundaries:
- Do not move files.
- Do not split repositories.
- Do not change imports, packaging, CI gates, parser behavior, analytics
  behavior, local app behavior, workbook schema, webhook payload shape, Apps
  Script behavior, Google Sheets behavior, OpenAI/model-provider behavior,
  AI/coaching behavior, or production behavior.
- Do not inspect sibling repositories unless the handoff explicitly includes
  allowed_read_only_references.
- Do not create GitHub issues or PRs.
- Do not activate #388 or #381.
- Preserve parser_behavior_ready=false,
  pipeline_activation_ready_for_issue_388=false,
  private_harvest_authorized=false, fixture_promotion_authorized=false, and
  corpus_status_change_authorized=false.

Validation:
- git status --short --branch
- git ls-files
- git diff --check
- python3 tools/check_agent_docs.py
- path-fed secret/private-marker scan for the report
- path-fed protected-surface scan for the report
- path-fed validation selector for the report

Expected output:
- docs/contract_test_reports/repo_extraction_candidate_matrix.md
- optional docs/implementation_handoffs/repo_extraction_candidate_matrix_comparison.md
- summary of decisions
- validation run
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/465"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/456"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/548"
  previous_merge_commit: "5aac58f07407ad6a582ea5907518d29a59de713d"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #465 problem representation"
  target_artifact: "docs/contracts/repo_extraction_candidate_matrix.md"
  expected_report: "docs/contract_test_reports/repo_extraction_candidate_matrix.md"
  verdict: "repo_extraction_candidate_matrix_contract_created"
  risk_tier: "Medium-High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/repo-extraction-candidate-matrix-465"
  internal_project_area: "Quality / Governance"
  truth_owner: "governance classification only"
  bridge_code_status: "shared_support"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  stop_conditions:
    - "Do not split repositories or move files."
    - "Do not change imports, packaging, CI gates, parser/runtime/workbook/webhook/App Script/analytics/AI/coaching behavior, or production behavior."
    - "Do not make a separate repo a truth owner by implication."
    - "Do not inspect sibling repositories unless allowed_read_only_references explicitly authorizes them."
    - "Do not commit raw/private logs, UTC_Log content, generated/private/runtime artifacts, SQLite databases, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, or local-only artifacts."
```
