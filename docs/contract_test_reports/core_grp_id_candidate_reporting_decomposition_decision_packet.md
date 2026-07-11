# Core GRP ID Candidate Reporting Decomposition Decision Packet Review

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/727

## Trackers

- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Decomposition tracker: https://github.com/Tahjali11/Mythic-Edge/issues/463
- Residual promotion queue: https://github.com/Tahjali11/Mythic-Edge/issues/715

## Contract

`docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md`

## Implementation Under Test

No implementation is under test. This is an independent docs-only contract
clarification review on branch
`codex/grp-id-candidate-reporting-decision-packet-727` at
`4b5c3d7d6ffd566858f123039db2d4bf8690e6e4`.

## Report Lifecycle

`report_lifecycle: final_approval`

## Findings

No blocking findings remain.

### GRPID-DECOMP-E-005 - P1 - Fixed-state follow-up

`finding_lifecycle: fixed_state_followup`

Observed:

- #159 and #161 are now labeled only as approval-packet validation and
  execution-authority-contract provenance.
- `actual_tool_evidence_result_ref` is `none`.
- `prior_ars_evidence_found` and `prior_refactor_scout_evidence_found` are both
  `no`.
- `reviewed_repo`, `reviewed_scope`, `reviewed_commit`, `reviewed_blob`, and
  `ars_version_contract_bundle` are all `none`.
- `evidence_status` remains
  `fresh_scoped_evidence_required_before_implementation`, and
  `fresh_scoped_evidence_needed` remains `yes`.

Derived:

The revised packet now matches the linked #159/#161 durable lifecycle and no
longer presents approval/authority provenance as an ARS or Refactor Scout
result. GRPID-DECOMP-E-005 is fixed and no longer blocking.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GRPID-DECOMP-E-001 | P1 | `fixed_state_followup` | fixed | not_blocking | Issue-specific packet omitted or did not explicitly override required base Phase 5 envelope fields. | Base schema identity, `target_commit`, issue #664, and all three deferred-surface fields are now explicit at contract lines 181-360. | none |
| GRPID-DECOMP-E-002 | P1 | `fixed_state_followup` | fixed | not_blocking | Direct CLI and launcher consumers were missing. | Candidate row, compatibility boundaries, and validation now cover `score_grp_id_candidates.py` and `manasight_launcher_auto.py`; current source references confirm both paths. | none |
| GRPID-DECOMP-E-003 | P1 | `fixed_state_followup` | fixed | not_blocking | Historical evidence was incorrectly sufficient for later implementation routing. | Canonical fields now require fresh scoped evidence before implementation while allowing unchanged-blob evidence only for docs framing at contract lines 431-463. | none |
| GRPID-DECOMP-E-004 | P1 | `fixed_state_followup` | fixed | not_blocking | Literal no-read/no-echo language conflicted with exact preservation of existing local-only report text. | Contract lines 465-530 and 599-641 now permit already-built in-memory report values, prohibit direct reads and new/public echo, and require exact existing local-output preservation. | none |
| GRPID-DECOMP-E-005 | P1 | `fixed_state_followup` | fixed | not_blocking | Prior ARS and Refactor Scout evidence flags were not supported by the linked durable lifecycle. | Contract lines 446-499 now classify #159/#161 as provenance only, set actual tool evidence to `none`, fail all prior-tool/reviewed-target fields closed, and retain the fresh pre-implementation evidence gate. | none |

## Contract Summary

The packet must decide whether the mixed GRP ID candidate-reporting surface may
later support a behavior-preserving same-repo decomposition. The current module
remains the public facade, the non-authoritative recommendation is limited to
pure Markdown rendering, and `final_decision` remains `review_required`.

No implementation, helper creation, file movement, private-evidence read, ARS
or Refactor Scout run, behavior change, or readiness/truth/assurance claim is
authorized.

## Internal Project Area Reviewed

Parser/card-identity candidate reporting with Corpus / Provenance and Analytics
consumers. Candidate rows and reports remain review support; confirmed identity
truth remains parser/card-identity owned.

## Bridge-Code Status Reviewed

`shared_support`, with a possible future private same-repo Markdown renderer
behind the existing `grp_id_candidates` facade.

## Confirmed Contract Matches

- GRPID-DECOMP-E-001 is fixed. The issue-specific schema extension now
  preserves or explicitly overrides every required base envelope field.
- GRPID-DECOMP-E-002 remains fixed. The root CLI and launcher invocation paths
  are direct consumers with explicit compatibility and future validation
  requirements.
- GRPID-DECOMP-E-003 is fixed. Historical unchanged-blob evidence is framing
  only; fresh scoped evidence is required before implementation routing.
- GRPID-DECOMP-E-004 is fixed. The renderer may consume already-built values
  only to reproduce existing local-only text, while direct reads, new fields,
  new destinations, and new/public echo fail closed.
- GRPID-DECOMP-E-005 is fixed. Approval and authority-contract provenance is
  separate from actual tool evidence, all prior-tool and reviewed-target fields
  fail closed, and fresh scoped evidence remains required before implementation.
- The existing module remains the public facade.
- The possible first slice is pure Markdown rendering only and is explicitly
  non-authoritative.
- JSON assembly, report-object construction, paths, writes, dataclasses,
  scoring, ranking, identity decisions, promotion, confirmation, deferral, and
  inferred-review construction remain in the facade.
- Parser/card-identity truth does not move into reports, Analytics, workbook,
  UI, launcher, or AI surfaces.
- `final_decision` is `review_required`.
- `ready_for_codex_c`, implementation, helper creation, file movement, ARS,
  Refactor Scout, private-evidence read, behavior-change, and claim flags remain
  false.
- The public contract and report contain no raw private evidence or local
  absolute paths.

## Contract Mismatches

- None.

## Open Question

- None for this docs-only contract review.

## Checks Run

```text
git status --short --branch --untracked-files=all
git fetch --prune origin
git rev-list --left-right --count HEAD...origin/main
gh issue view 727 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body,comments
gh issue view 715 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
gh issue view 159 --repo Tahjali11/Mythic-Edge-Automation-Artifacts --json number,title,state,url,body,comments
gh issue view 161 --repo Tahjali11/Mythic-Edge-Automation-Artifacts --json number,title,state,url,body,comments
git rev-parse HEAD:src/mythic_edge_parser/app/grp_id_candidates.py
git rev-parse 9528bb3bee9c1d241268cb8a7d1a806b118471de:src/mythic_edge_parser/app/grp_id_candidates.py
py tools/check_agent_docs.py
git diff --check
py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
py tools/select_validation.py --base origin/main --paths-from-stdin
```

## Results

- Branch and `origin/main` matched at
  `4b5c3d7d6ffd566858f123039db2d4bf8690e6e4` with left/right count `0 0`.
- Issue #727 is open and has no comments. Trackers #568, #463, and #715 are
  open.
- Historical and current target Git blobs both equal
  `517d8061e09f2e220792062c57615a048efa460e`.
- Current source references confirm the candidate module's public facade,
  report writers, CLI imports/labels, launcher command vectors, and adjacent
  consumers named by the revised contract.
- Agent docs passed: errors 0, warnings 0.
- `git diff --check` passed.
- Protected-surface scan passed: forbidden 0, warnings 0.
- Secret/private-marker scan passed: forbidden 0, warnings 0.
- Validation selector passed: warnings 0; docs-only checks were selected.
- Runtime tests were not run because no implementation or runtime behavior is
  under test or authorized in this docs-only review.

## Missing Tests

None for the current docs-only revision. A later implementation remains
responsible for focused module, CLI, launcher, byte-preservation, privacy,
full-suite, and protected-surface validation after exact authority and fresh
evidence exist.

## Drift Notes

- Source drift: none for the target module; the Git blob is unchanged.
- Contract drift: resolved for GRPID-DECOMP-E-001 through E-005.
- Evidence-provenance drift: resolved. Approval/authority provenance and actual
  tool evidence are now explicitly separate.
- Local-data, workbook, deployment, and PR lifecycle drift: not inspected and
  not required for this docs-only review.

## Recommendation

Approve the revised docs-only decision packet for Codex F submission after the
submitter confirms an explicitly authorized PR target. This approval does not
authorize Codex C, implementation, helper creation, file movement, ARS,
Refactor Scout, private-evidence access, or behavior changes.

## Next Workflow Action

Next role: Codex F / Module Submitter, with target-branch authority checked
before staging or publication.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex F: Module Submitter for issue #727.

Reviewed files:
- docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md
- docs/contract_test_reports/core_grp_id_candidate_reporting_decomposition_decision_packet.md

All findings GRPID-DECOMP-E-001 through E-005 are fixed. Re-run the docs-only
validation and stage only the two reviewed files. Confirm explicit authority
for the PR target before committing, pushing, or opening a draft PR. The review
base is origin/main, but this handoff does not independently authorize targeting
main. If target authority is absent, stop and request it.

Preserve final_decision review_required, ready_for_codex_c false, fresh scoped
evidence required before implementation, and every implementation/file-move/
helper/private-read/tool-run/behavior-change/readiness/truth/assurance flag as
false.

Do not implement code, create the renderer, move files, run ARS or Refactor
Scout, inspect private evidence, merge, close #727, or mark trackers complete.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/727"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  residual_promotion_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
  completed_thread: "E_contract_re_review"
  next_thread: "F_module_submitter_after_target_authority_check"
  source_artifact: "docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md"
  target_artifact: "docs/contract_test_reports/core_grp_id_candidate_reporting_decomposition_decision_packet.md"
  risk_tier: "High"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_approval"
  branch: "codex/grp-id-candidate-reporting-decision-packet-727"
  reviewed_commit: "4b5c3d7d6ffd566858f123039db2d4bf8690e6e4"
  final_decision: "review_required"
  finding_status:
    GRPID-DECOMP-E-001: "fixed_state_confirmed"
    GRPID-DECOMP-E-002: "fixed_state_confirmed"
    GRPID-DECOMP-E-003: "fixed_state_confirmed"
    GRPID-DECOMP-E-004: "fixed_state_confirmed"
    GRPID-DECOMP-E-005: "fixed_state_confirmed"
  ready_for_codex_c: false
  implementation_authorized: false
  same_repo_helper_creation_authorized: false
  file_move_authorized: false
  private_evidence_read_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  forbidden_scope_touched: false
  generated_private_artifacts_kept: false
  codex_f_recommended: true
  main_target_authorized_by_this_review: false
  next_recommended_role: "Codex F: docs-only submitter after explicit target-branch authority check"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "High"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "docs/decisions/ADR-0001-parser-owns-truth.md"
    - "docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md"
    - "docs/decisions/ADR-0006-repository-boundary-strategy.md"
  protected_surfaces:
    - "parser/card-identity candidate scoring and ranking"
    - "private hand-confirmation and submitted-deck evidence"
    - "promotion, confirmation, and deferral lifecycle"
    - "generated JSON and Markdown report schema, text, paths, and writes"
    - "CLI and launcher behavior"
  authority_conflicts_found: false
  authority_conflict_notes: "None. The revised contract now keeps approval/authority provenance separate from absent tool evidence and fails closed before implementation."
  stop_conditions:
    - "Do not authorize Codex C or implementation."
    - "Do not move files or create the proposed renderer helper."
    - "Do not run ARS or Refactor Scout or read private evidence."
    - "Stop before any parser/card-identity, report, CLI, launcher, output, or truth behavior change."
```
