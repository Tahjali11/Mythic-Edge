# Repo Extraction Candidate Matrix Report

## Report Header

| Field | Value |
| --- | --- |
| `report_schema` | `repo_extraction_candidate_matrix.v1` |
| `source_issue` | https://github.com/Tahjali11/Mythic-Edge/issues/465 |
| `source_contract` | `docs/contracts/repo_extraction_candidate_matrix.md` |
| `generated_from_ref` | `5aac58f07407ad6a582ea5907518d29a59de713d` |
| `generated_at_utc` | `2026-06-22T10:20:37Z` |
| `repository` | `Tahjali11/Mythic-Edge` |
| `repository_url` | `https://github.com/Tahjali11/Mythic-Edge` |
| `report_status` | `matrix_ready_with_open_questions` |
| `non_claims` | `not_extraction_authorization`, `not_file_move_authorization`, `not_repo_split_authorization`, `not_import_change_authorization`, `not_package_metadata_change_authorization`, `not_ci_change_authorization`, `not_parser_behavior_ready`, `not_pipeline_activation_ready_for_issue_388`, `not_private_harvest_authorized`, `not_fixture_promotion_authorized`, `not_corpus_status_change_authorized`, `not_release_readiness`, `not_deploy_readiness`, `not_production_readiness`, `not_parser_truth_transfer`, `not_analytics_truth_transfer`, `not_ai_truth`, `not_coaching_truth` |

## Scope And Method

Role performed: Codex C, Report Implementer.

This report is a public-safe governance matrix. It classifies current repo path
groups and future extraction candidates from committed Mythic Edge metadata only.
It does not move files, split repositories, change imports, change package
metadata, change CI, change protected behavior, create issues, create PRs, or
inspect sibling repositories.

Inputs used:

- GitHub issue #465 and tracker #388 context.
- Adjacent GitHub issues #340 and #463 as routing context only.
- `docs/contracts/repo_extraction_candidate_matrix.md`.
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`.
- `docs/contracts/internal_project_boundaries.md`.
- `docs/implementation_handoffs/internal_project_boundaries_comparison.md`.
- `docs/contract_test_reports/internal_project_boundaries.md`.
- `docs/internal_project_map.md`.
- `README.md`, `docs/project_roadmap.md`, `pyproject.toml`, `.github/`,
  `src/`, `frontend/`, `tools/`, `tests/`, and `tests/fixtures/`.
- Transient inventory commands: `git ls-files`, `find`, `rg --files`-equivalent
  path inspection, and focused `wc -l` for the known oversized-file candidates.

Sibling repositories were not inspected. Sibling repo names below are future
destination labels only.

## Summary Decisions

- Mythic Edge should stay monorepo-first at this ref, per ADR-0006.
- Corpus / Provenance has the clearest future public-spoke signal, but still
  needs a corpus release contract, versioning policy, and consumer tests before
  movement.
- Parser extraction remains a future candidate, but is red for now because
  parser truth, event classes, identity, final reconciliation, and tests are
  still tightly coupled to the primary repo.
- Analytics transfer and visibility questions route to issue #340 instead of
  being solved here.
- Oversized-file decomposition routes to issue #463 instead of becoming repo
  extraction by itself.
- Local App / UI, Workbook / Transport, Match Journal, and repo authority docs
  should remain in the primary repo for now.
- Generated, private, local, runtime, database, and workbook-export artifacts
  are excluded from extraction planning.

## Candidate Matrix

| candidate_id | path_or_module_group | current_project_area | current_classification | proposed_owning_repo | visibility_candidate | candidate_type | non_owning_consumers | source_inputs | outputs_or_artifacts | public_api_or_artifact_contract_status | dependency_direction | private_or_protected_data_risk | test_coverage_and_portability | release_cadence_fit | extraction_readiness | blockers | recommended_next_issue | rollback_or_migration_notes | non_claims |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `repo_authority_docs` | `AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, `docs/codex_module_workflow.md`, `docs/agent_threads/`, `docs/templates/`, `docs/decisions/` | Quality / Governance | clear_owner | `Tahjali11/Mythic-Edge` | public | `stay_primary_repo` | All Codex roles, issue contracts, PRs, reviewers | Committed governance docs and accepted ADRs | Repo authority and workflow rules | Stable repo-local authority; not a package API | All layers may read; no runtime reverse dependency | Low private-data risk, high authority-drift risk | `tools/check_agent_docs.py`, secret/protected-surface checks | Tied to source repo lifecycle | red | Extracting authority docs would make repo authority ambiguous | `no_action` | Keep authority docs with the repo unless a future ADR explicitly defines a reusable governance package | `not_repo_split_authorization`, `not_truth_transfer` |
| `workflow_validation_tools` | `tools/check_*.py`, `tools/select_validation.py`, `tools/run_*`, `tests/test_check_*`, `tests/test_select_validation.py`, hardening report tools | Quality / Governance | shared support | `future_mythic_edge_governance_or_tooling_repo` | public | `shared_support_needs_interface_hardening` | Codex roles, local validation, CI workflow | Git diff, changed paths, repo docs, tests, public-safe artifacts | Validation reports, selector recommendations, advisory checks | Useful command interfaces exist, but repo-specific policy is embedded | Governance tools inspect all layers; must not become runtime behavior | Medium; tools deliberately scan protected/private markers | Focused tool tests exist; portability would need fixture isolation | Could release independently only after policy/versioning split | yellow | Repo-specific protected-surface policy, branch assumptions, and path semantics are not standalone yet | `Codex_B_contract` | Define a governance-tool package contract and prove current repo can pin a version before moving | `not_ci_change_authorization`, `not_merge_readiness` |
| `parser_core_runtime` | `src/mythic_edge_parser/events.py`, `router.py`, `stream.py`, `event_bus.py`, `log/`, `parsers/`, parser-owned `app/state.py`, `models.py`, `extractors.py`, `event_identity.py`, `gameplay_actions.py`, `opponent_card_observations.py` | Parser | clear_owner | `future_mythic_edge_parser_repo` | public | `repo_extraction_candidate` | Local App / UI, Analytics, Workbook / Transport, Corpus / Provenance tests | MTGA log text and parser-normalized inputs under approved tests | Parser events, normalized match/game/action facts, diagnostics | Internal module APIs are tested but not independently packaged | Future consumers should depend on versioned parser outputs, not parser internals | High; parser touches raw-log source boundaries and protected truth surfaces | Strong in-repo tests, but cross-repo package tests are not defined | Poor until parser event and output contracts stabilize | red | Parser truth ownership, final reconciliation, identity, and protected surfaces remain too coupled for movement | `route_to_parser_public_interface_contract` | Require stable event/output schemas, package contract, consumer compatibility tests, and rollback plan | `not_parser_behavior_ready`, `not_pipeline_activation_ready_for_issue_388` |
| `corpus_public_safe_artifacts` | `tests/fixtures/`, golden replay manifests, parser corpus manifests, schema snapshots, corpus parity reports | Corpus / Provenance | shared support | `Tahjali11/Mythic-Edge-Corpus` | public | `public_spoke_candidate` | Parser tests, golden replay, feature-equity checks, drift/provenance tools | Committed public-safe fixtures and metadata only | Versioned fixture manifests, replay manifests, schema snapshots, corpus reports | Artifact contracts exist, but release/package contract is not defined here | Parser may consume pinned corpus releases for tests; corpus should not depend on production parser code | Medium; fixture provenance must prevent private/raw artifact leakage | Strong in-repo fixture tests; cross-repo consumption tests still needed | Good after release contract and fixture manifest versioning | green | No sibling repo inspection authorized; no corpus release contract in this issue | `route_to_corpus_release_contract` | First copy/version public-safe artifacts under a release contract; keep rollback by retaining in-repo fixtures until pinned consumption passes | `not_fixture_promotion_authorized`, `not_corpus_status_change_authorized` |
| `evidence_provenance_modules` | `src/mythic_edge_parser/app/evidence_*`, `runtime_field_evidence.py`, `golden_replay.py`, `corpus_parity_report.py`, `feature_equity_corpus_ratchet.py`, recovery/proof/report builders | Corpus / Provenance | clear_owner | `Tahjali11/Mythic-Edge-Corpus` | public | `repo_extraction_candidate` | Parser QA, validation reports, local status/reports, future corpus release tools | Parser-owned outputs, evidence-ledger metadata, public-safe fixtures | Evidence reports, schema snapshots, drift reports, invariant reports, replay reports | Many contracts exist; package boundary is not defined | Should consume parser facts/provenance; must not become a second parser | Medium-high; provenance code is close to raw-log privacy boundaries | Strong focused tests, but many modules import current package internals | Mixed; report builders could version sooner than runtime-adjacent modules | yellow | Broad `app/` namespace, parser-package imports, and report/runtime adjacency need interface hardening | `route_to_corpus_release_contract` | Extract report/artifact builders before runtime-adjacent wiring; prove parser tests pass with pinned artifact package | `not_parser_truth_transfer`, `not_private_harvest_authorized` |
| `analytics_foundation_and_transfer` | `src/mythic_edge_parser/app/analytics_*`, analytics migrations, analytics ingest/view tests, local analytics sidecar | Analytics | clear_owner and bridge code | `Tahjali11/Mythic-Edge-Analytics` | private | `private_spoke_transfer_candidate` | Local App / UI, Match Journal, parser-normalized replay import, tests | Parser-normalized facts, approved provenance metadata, local SQLite schema | SQLite rows, views, local analytics summaries | In-repo contracts and tests exist; private-spoke interface is issue #340 scope | Analytics consumes parser facts; must not read raw logs as truth shortcut | Medium-high; local database and private analytics boundaries need explicit policy | Good in-repo tests; private package parity/fallback tests not present here | Good for derived/private analytics only after #340 staged plan | yellow | Issue #340 owns transfer strategy, versioning, fallback, and private visibility decisions | `route_to_issue_340` | Prototype/copy private candidates first, keep base app functional without private spoke, remove only after parity and rollback proof | `not_analytics_truth_transfer`, `not_private_spoke_authorization` |
| `local_app_and_frontend` | `src/mythic_edge_parser/local_app/`, `frontend/`, `tools/dev_app/`, dev launcher scripts | Local App / UI | clear_owner | `Tahjali11/Mythic-Edge` | private | `stay_primary_repo` | Parser, Analytics, Match Journal, local operator | Parser-normalized facts, SQLite data, setup/config status, user-selected local files | Local backend routes, browser UI, setup/import/status surfaces | Local app API contracts exist by tests, but product surface is integration-owned | Local app consumes backend/parser/analytics; it should not own truth | High; UI and local backend touch local paths, status, imports, and operator artifacts | Strong in-repo backend/frontend tests; cross-repo app packaging not defined | Poor for independent release while private-local-v1 is still integration path | red | Local app is current private-local-v1 front door and integration orchestrator | `no_action` | Keep app with primary repo until installer/package strategy explicitly changes | `not_ui_behavior_change`, `not_production_readiness` |
| `local_app_oversized_decomposition` | `frontend/src/App.tsx`, `frontend/src/api.ts`, `src/mythic_edge_parser/local_app/live_capture_control.py` | Local App / UI | bridge code / oversized implementation | `Tahjali11/Mythic-Edge` | private | `internal_decomposition_only` | Local frontend/backend tests, private-local-v1 operator | Existing UI/API/live-capture code paths | Same UI/API/live-capture behavior after refactor | Decomposition contracts belong to issue #463 children | No repo boundary change; only behavior-preserving internal splits | Medium-high due UI/API/live-capture protected surfaces | Existing tests plus future focused decomposition tests required | Better as internal refactor than independent release | yellow | File size is a decomposition signal, not extraction readiness | `route_to_issue_463` | Split by behavior-preserving modules with baseline tests; no repo move | `not_repo_extraction_authorization`, `not_api_shape_change` |
| `match_journal_surfaces` | Match Journal migrations, repository, service, cockpit/runtime modules, Match Journal tests | Local App / UI | bridge code | `Tahjali11/Mythic-Edge` | private | `stay_primary_repo` | Local App / UI, Analytics queries, human review surfaces | Parser-normalized match/game IDs and human-entered notes | Local journal records, notes, labels, cockpit bundles | In-repo schema/service contracts exist | Journal consumes parser facts; notes do not become parser truth | Medium; human annotations and local SQLite data are private/local | Focused schema/repository/service/cockpit tests exist | Poor until local app packaging is stable | red | Tight coupling to local app, local SQLite, and human annotations | `no_action` | Keep journal local; any future plugin boundary needs annotation privacy contract | `not_parser_truth`, `not_analytics_truth`, `not_coaching_truth` |
| `workbook_transport` | `src/mythic_edge_parser/app/sheet_schema.py`, `outputs.py`, `sheet_exports.py`, `tools/google_apps_script/Code.gs`, workbook/webhook tests | Workbook / Transport | clear_owner and bridge code | `Tahjali11/Mythic-Edge` | undecided | `stay_primary_repo` | Parser outputs, workbook/App Script transport, legacy Google Sheets path | Parser-normalized match/game rows | Sheet rows, webhook payloads, Apps Script mappings | Protected row/schema contracts exist and are tightly governed | Transport consumes parser outputs; workbook does not feed parser truth | High; workbook exports, webhook URLs, and Apps Script are protected surfaces | Focused schema/output/webhook tests exist | Poor; transport must remain compatible with parser row contracts | red | Workbook schema and webhook/App Script parity require scoped contracts for any change | `no_action` | Keep in primary repo until workbook/transport split has full parity and rollback plan | `not_workbook_truth`, `not_webhook_change`, `not_apps_script_change` |
| `shared_card_catalog_support` | `card_catalog.py`, `card_catalog_refresh.py`, `grp_id_catalog.py`, `grp_id_candidates.py`, `arena_id_validation.py`, `tools/scryfall_parser/` | Shared Support | shared support | `undecided` | public | `optional_dependency_candidate` | Parser, Corpus / Provenance, Analytics, validation tools | Approved public card/catalog data and committed validation fixtures | Catalog lookup helpers, candidate reports, refresh outputs | Helper APIs exist, but generated-data and approved-source policy need stronger boundary | Parser may use catalog support; downstream analytics must not rewrite parser identity | Medium; generated card data and refresh outputs must stay controlled | Focused tests exist for catalog and identifier helpers | Good only after optional-provider/source-data contract matures | yellow | External-data source policy, generated-data handling, and optional dependency behavior need contract | `route_to_optional_dependency_contract` | Define source snapshot/versioning and fallback before extracting catalog tooling | `not_card_truth_transfer`, `not_generated_data_authorization` |
| `quality_docs_artifact_history` | `docs/contracts/`, `docs/implementation_handoffs/`, `docs/contract_test_reports/`, `docs/problem_representations/` | Quality / Governance | clear_owner | `Tahjali11/Mythic-Edge` | public | `stay_primary_repo` | Codex roles, reviewers, submitters, deployers | Current issue/contracts/reports | Durable workflow history and review evidence | Artifact naming is stable but repo-specific | Docs follow source repo authority; they should not be split away from code they govern | Low private-data risk when scans pass; high context-drift risk if separated | Agent-doc, secret, protected-surface, selector checks | Tied to source repo lifecycle | red | Splitting history from governed code would weaken review context | `no_action` | Keep artifacts with the source repo; use archival exports only under separate policy | `not_authority_transfer`, `not_sibling_repo_action` |
| `root_and_legacy_operator_scripts` | root scripts such as `sync_*`, `refresh_*`, `record_*`, `import_*`, `live_print_*`, and launcher shortcuts | Shared Support | ambiguous | `undecided` | private | `shared_support_needs_interface_hardening` | Local operator, parser/runtime helpers, validation/debug workflows | Local operator-selected inputs and committed helper code | Local convenience actions or reports | Mixed; many scripts are not stable package APIs | Scripts may call parser/app internals; should not define truth | Medium-high; operator scripts can touch local paths or generated data | Uneven focused tests; some tool coverage exists | Poor until grouped by owner and interface | yellow | Need script inventory, owner classification, generated-artifact policy, and replacement path | `Codex_A_problem_representation` | Deprecate or wrap scripts before any movement; preserve operator rollback commands | `not_runtime_behavior_change`, `not_local_artifact_authorization` |
| `generated_local_artifacts` | `data/`, local SQLite files, runtime status, failed posts, local JSONL, local logs, workbook exports, ignored build/cache outputs | Generated / Local Artifacts | generated/excluded | `no_separate_repo` | not_applicable | `generated_or_local_artifact_excluded` | Local runtime only | Local/private/generated machine state | Local artifacts only | Not source artifacts | No dependency direction; must stay out of committed source | High by definition | Exclusion and scanner policy only | Not releasable | not_candidate | These are not repo extraction candidates | `no_action` | Do not commit, package, mirror, or transfer generated/private/local artifacts | `not_source_artifact`, `not_private_harvest_authorized` |
| `future_ai_surfaces` | Future AI/advisor/coaching modules; no current authorized runtime module | Future AI Integration | ambiguous / deferred | `future_ai_or_advisor_repo` | private | `not_candidate` | Future local app or analytics consumers only after contract | None in this report | None in this report | No current runtime contract | Future AI may consume deterministic analytics/provenance; it must not own truth | High due model-provider, coaching, and hidden-information boundaries | No current endpoint/runtime tests in this repo for AI behavior | Deferred | not_candidate | No authorized AI runtime, no model-provider contract, no coaching truth contract | `no_action` | Keep deferred until separate issue/contract and explicit user approval | `not_ai_truth`, `not_coaching_truth`, `not_openai_runtime_authorization` |

## Green / Yellow / Red Interpretation

- `green` means a future Codex A planning issue may be worth considering. It
  does not authorize movement.
- `yellow` means the boundary has useful separation signals but needs contracts,
  interface hardening, versioning, portability tests, or privacy review before
  extraction planning.
- `red` means the row should stay in the primary repo for now.
- `not_candidate` means the row is excluded, generated/local, deferred, or not
  useful as a repo boundary.

## Open Questions

- Should any corpus row move from `green` to `yellow` until a sibling-repo
  read-only reference is explicitly authorized?
- Should #340 produce the private analytics transfer matrix before any
  `Tahjali11/Mythic-Edge-Analytics` destination label becomes stronger than a
  candidate?
- Should issue #463 decompose oversized source files before any parser,
  evidence, frontend, API, or live-capture extraction planning issue?
- Should future governance/tooling extraction start with a package contract for
  validation helpers or remain repo-local because the rules are repo-specific?

## Preserved Flags

| Flag | Value |
| --- | --- |
| `parser_behavior_ready` | `false` |
| `pipeline_activation_ready_for_issue_388` | `false` |
| `private_harvest_authorized` | `false` |
| `fixture_promotion_authorized` | `false` |
| `corpus_status_change_authorized` | `false` |

## Protected Boundary Confirmation

This report did not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- router semantics;
- match or game identity;
- deduplication;
- imports;
- package metadata;
- CI workflows;
- local app behavior;
- frontend behavior;
- analytics behavior;
- SQLite schema or migrations;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- production behavior.

No sibling repository was inspected or mutated.

## Validation Log

- `git status --short --branch` passed; worktree changes are scoped to the
  Codex B contract and this Codex C report.
- `git ls-files >/dev/null` passed; transient committed-file inventory was
  available and no raw inventory file was committed.
- `git diff --check` passed.
- `python3 tools/check_agent_docs.py` passed:
  `checked_files: 36`, `errors: 0`, `warnings: 0`.
- `printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
  passed: `forbidden: 0`, `warnings: 0`.
- `printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
  passed: `forbidden: 0`, `warnings: 0`.
- `printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  passed with `selection_status: ok`; required checks were `diff_check`,
  `protected_surface_gate`, and `secret_private_marker_scan`, with
  `agent_docs_checker` recommended.

## Recommended Next Role

Codex E: Module Reviewer / contract-test reviewer.

Reviewer focus:

- Verify the report preserves ADR-0006 monorepo-first policy.
- Verify green/yellow/red labels are planning labels only.
- Verify #340 and #463 are routed, not solved here.
- Verify no sibling repository inspection was required.
- Verify false parser-evidence readiness and authorization flags remain false.
- Verify no protected behavior, imports, package metadata, CI, files, issues, or
  PRs were changed.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test reviewer for issue #465.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/465

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Contract:
docs/contracts/repo_extraction_candidate_matrix.md

Report:
docs/contract_test_reports/repo_extraction_candidate_matrix.md

Review focus:
- Verify the report follows the contract-required header, vocabulary, matrix
  columns, and protected boundaries.
- Verify it is public-safe and repo-relative.
- Verify it does not authorize file movement, repo splitting, import changes,
  package metadata changes, CI changes, parser/runtime/workbook/webhook/App
  Script/analytics/AI behavior changes, sibling repo work, issue creation, PR
  creation, #388 activation, or #381 activation.
- Verify issue #340 and issue #463 are routed as adjacent scopes rather than
  implemented inside #465.
- Verify parser_behavior_ready=false,
  pipeline_activation_ready_for_issue_388=false,
  private_harvest_authorized=false, fixture_promotion_authorized=false, and
  corpus_status_change_authorized=false.

Suggested validation:
- git status --short --branch
- git diff --check
- python3 tools/check_agent_docs.py
- printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
- printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
- printf '%s\n' docs/contract_test_reports/repo_extraction_candidate_matrix.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin

End with findings first, validation reviewed or rerun, remaining risks, next
recommended role, and workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/465"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/456"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/548"
  previous_merge_commit: "5aac58f07407ad6a582ea5907518d29a59de713d"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/repo_extraction_candidate_matrix.md"
  target_artifact: "docs/contract_test_reports/repo_extraction_candidate_matrix.md"
  verdict: "repo_extraction_candidate_matrix_ready_for_review"
  risk_tier: "Medium-High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/repo-extraction-candidate-matrix-465"
  report_status: "matrix_ready_with_open_questions"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  sibling_repositories_inspected: false
  files_moved: false
  imports_changed: false
  package_metadata_changed: false
  ci_changed: false
```
