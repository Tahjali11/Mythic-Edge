# Core GRP ID Candidate-Reporting Decomposition Evidence Reconciliation Contract

## Contract Status

```yaml
object: "core_grp_id_candidate_reporting_decomposition_evidence_reconciliation"
schema_version: "core_grp_id_candidate_reporting_decomposition_evidence_reconciliation.v2"
contract_id: "core_grp_id_candidate_reporting_decomposition_evidence_reconciliation"
repository: "Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/729"
historical_decision_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/727"
artifact_kind: "decision_packet_evidence_reconciliation"
decision_status: "review_required"
risk_tier: "high"
ready_for_owner_implementation_routing: false
ready_for_codex_c: false
implementation_authorized: false
same_repo_helper_creation_authorized: false
renderer_creation_authorized: false
file_move_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
replay_authorized: false
rerun_authorized: false
source_reread_authorized: false
result_reconstruction_authorized: false
evidence_retention_authorized: false
private_evidence_read_authorized: false
source_mutation_authorized: false
truth_claimed: false
parser_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
release_readiness_claimed: false
production_readiness_claimed: false
```

`review_required` permits only independent review of this companion contract.
It does not authorize implementation, a renderer child, source inspection,
tool execution, evidence retention, or Codex C.

## Codex E Finding Reconciliation

- `GRPID-RECON-E-001`: revised pending independent confirmation. Version 2
  adds exact local vocabularies, fixed sentinels, version-pinned Automation
  imports, and a complete field-to-vocabulary matrix for every packet status
  and sentinel. Existing values and fail-closed derivations are unchanged.

This closure revision does not make the ephemeral result reviewable, retain
evidence, strengthen the final decision, or authorize implementation.

## Module

Post-execution evidence reconciliation for the historical GRP ID
candidate-reporting decomposition decision packet.

This contract is documentation and workflow-state reconciliation only. It does
not modify the candidate surface, its public facade, scoring, ranking,
promotion, confirmation, deferral, reports, output paths, CLI, launcher, or
parser/card-identity behavior.

## Source Issues And Trackers

- Reconciliation issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/729
- Historical decision issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/727
- Historical decision PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/728
- Residual promotion queue:
  https://github.com/Tahjali11/Mythic-Edge/issues/715
- Decomposition tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/463
- Project roadmap:
  https://github.com/Tahjali11/Mythic-Edge/issues/568
- Automation authority and result lifecycle issue:
  https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/165
- Automation authority PR:
  https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/pull/166

## Governing Authority

This contract follows:

- `AGENTS.md`;
- `docs/agent_rules.yml`;
- `docs/agent_constitution.md`;
- `docs/codex_module_workflow.md`;
- `docs/agent_threads/module_contract.md`;
- `docs/templates/module_contract.md`;
- `docs/decisions/ADR-0001-parser-owns-truth.md`;
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`;
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`;
- `docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md`;
- `docs/contract_test_reports/core_grp_id_candidate_reporting_decomposition_decision_packet.md`; and
- the public-safe Automation authority and lifecycle references named here.

External Automation artifacts are evidence and access coordination surfaces.
They do not own Core parser truth, Core decomposition decisions, or Core
implementation authority.

## Owning Layer And Internal Project Area

- Primary internal project area: `Shared Support`.
- Bridge-code status: `shared_support`.
- Parser truth owner: Core parser/card-identity code for confirmed
  parser-managed identity.
- Reconciliation truth owner: this Core contract for the effective post-#727
  evidence lifecycle and routing state only.
- Automation lifecycle owner: Mythic-Edge-Automation-Artifacts for its packet,
  approval consumption, claim, ordered tool-attempt lifecycle, and result
  envelope validity.

Candidate rows and candidate reports remain review support. They do not become
confirmed parser truth because an Automation attempt completed.

## Files Owned By This Contract

This contract owns only:

- `docs/contracts/core_grp_id_candidate_reporting_decomposition_evidence_reconciliation.md`.

It does not own or amend:

- `docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md`;
- `docs/contract_test_reports/core_grp_id_candidate_reporting_decomposition_decision_packet.md`;
- `src/mythic_edge_parser/app/grp_id_candidates.py`;
- the proposed private renderer;
- tests, fixtures, reports, runtime artifacts, or Automation artifacts.

## Verified Public Metadata Boundary

The following metadata was verified without reading the target source, raw
diffs, adjacent files, private evidence, or ephemeral classifications:

| Reference | Verified state | Permitted conclusion | Explicit non-conclusion |
| --- | --- | --- | --- |
| Core issue #727 | Closed after docs-only PR #728 | Historical packet lifecycle completed | Implementation was not authorized |
| Core PR #728 | Merged into `main` | Historical contract and review are committed | Candidate behavior was not changed |
| Core merge commit | `322a87b5f72c6e6e17872fad83bb2b671ddc8f59` | Exact reconciliation target commit | Safety, correctness, or decomposability |
| Core target path | `src/mythic_edge_parser/app/grp_id_candidates.py` | Exact public target selector | Permission to read it in this thread |
| Git tree metadata | Blob `517d8061e09f2e220792062c57615a048efa460e` at the target commit/path | Target identity matches the approved Automation binding | Source-content or behavioral review |
| Automation issue #165 | Closed after authority PR #166 | V2 authority contract lifecycle completed | The consumed packet may be reused |
| Automation PR #166 | Merged at `d0d9d850f9c609d0cf1e0504f79f52e76ed75169` | V2 authority contract is durable | Execution or result authority by itself |
| Owner approval | Issue #165 comment `4947100745` | Exact single-use packet and attempt were approved | General or repeat authority |
| Initial lifecycle claim commit | `abe1698b853c6f9ef7e541e6d2e3438d6de90b0a` | Claim existed before the terminal update | Retained evidence content |
| Terminal lifecycle claim commit | `92f483ca2b8d6e74d36d057cf67297abe9c498e3` | Claim reached terminal committed state | Tool classifications or recommendations |
| Terminal lifecycle claim | `claim_status: completed`, approval consumed, composite attempt completed classified | The exact composite lifecycle completed once | Any classification label or finding |
| Core issue #729 | Records the owner-supplied sanitized execution re-review status | The envelope was accepted as contract-conformant and ephemeral, with overall status `complete_review_required` | A retained result envelope or independent reproduction |

## Historical Baseline And Companion Authority

### Historical baseline

Issue #727 and its merged contract remain the immutable historical baseline for:

- the candidate identity and surface;
- the original evidence snapshot available when #727 was decided;
- the public-facade requirement;
- the renderer-only, same-repo, non-authoritative recommendation;
- the mixed governance/runtime classification;
- behavior-preservation boundaries;
- consumer and validation boundaries;
- every false-authority field and non-claim; and
- `final_decision: review_required` at that historical decision point.

The historical fields remain historically accurate, including
`actual_tool_evidence_result_ref: none`, prior tool evidence `no`, reviewed
target fields `none`, and the then-current fresh-evidence requirement. This
contract must not silently rewrite those original values.

### Companion scope

This companion is authoritative only for facts that occurred after the #727
snapshot:

- the V2 Automation contract and exact owner approval;
- single-use claim creation and consumption;
- the terminal composite-attempt lifecycle;
- the sanitized result-envelope and overall statuses recorded by issue #729;
- the absence of retained tool-result content;
- current Core routing after that ephemeral attempt; and
- requirements for any later retained or repeat evidence request.

### Read-together rule

Consumers must read the historical packet and this companion together.

| Question | Controlling artifact |
| --- | --- |
| What did #727 know and decide at merge time? | Historical #727 contract |
| What facade and renderer-only boundaries were preserved? | Historical #727 contract |
| Did the later single-use Automation attempt complete? | This companion, bound to the lifecycle claim |
| Is retained reviewable tool evidence currently available? | This companion |
| May the consumed packet be replayed? | Automation V2 contract and this companion, both fail closed |
| May Core implementation begin? | A later separate Core issue and contract only; currently no |

If the two contracts appear inconsistent, preserve the historical snapshot and
apply the more restrictive current routing. Ambiguity returns to Codex B; it
never authorizes implementation.

## Closed Reconciliation Vocabulary

Only the literals below are valid in this companion packet.

Version 2 closes status and sentinel bindings that were implicit in version 1.
It changes no evidence, lifecycle fact, recommendation, decision, or authority.
The historical #727 packet remains version 1 and unchanged.

### Baseline relationship

- `historical_baseline_preserved_unchanged`
- `invalid_baseline_missing_or_rewritten`

### Composite lifecycle

- `completed_consumed_single_use`
- `incomplete`
- `conflict_review_required`

### Evidence availability

- `retained_reviewable_result_available`
- `lifecycle_and_sanitized_envelope_status_only`
- `unavailable`
- `conflict_review_required`

### Actual result reference availability

- `unavailable_ephemeral_not_retained`
- `available_retained_result`
- `conflict_review_required`

### Evidence retention

- `none`
- `retained_under_separate_authority`
- `conflict_review_required`

### Reproducibility

- `not_reproducible_without_new_packet_approval_and_execution`
- `reproducible_from_retained_reviewed_result`
- `conflict_review_required`

### Reviewed target

- `execution_target_binding_confirmed_result_not_reviewable`
- `retained_result_reviewed_for_exact_target`
- `not_reviewed`
- `conflict_review_required`

### Fresh-evidence requirement

- `new_retained_reviewable_scoped_evidence_required_before_implementation`
- `retained_reviewable_evidence_requirement_satisfied`
- `conflict_review_required`

### Renderer recommendation

- `historical_renderer_only_recommendation_review_required`
- `keep_intact_selected_by_later_review`
- `renderer_child_may_be_proposed_by_later_contract`
- `conflict_review_required`

### Packet reuse

- `forbidden_consumed_packet`
- `new_packet_approval_and_execution_required`
- `conflict_review_required`

### Version-pinned Automation lifecycle and result imports

This companion imports only the following exact public-safe literals from
`residual_phase_5_scoped_evidence_execution_authority_contract.v2.md` as merged
in Automation Artifacts commit
`d0d9d850f9c609d0cf1e0504f79f52e76ed75169` and instantiated by the terminal
claim at `92f483ca2b8d6e74d36d057cf67297abe9c498e3`:

- `claim_status`: `completed`
- `approval_use_status`: `consumed_by_successful_claim_push`
- `status_reason`: `composite_attempt_completed_classified`
- `result_envelope_status`: `accepted_contract_conformant_ephemeral_result`
- `overall_result_status`: `complete_review_required`

No other Automation literal is imported. A later upstream vocabulary change,
additional literal, alias, or version does not enter this packet automatically.
It requires a new Core companion version and independent review.

### Retained tool-evidence presence

- `yes`
- `no`
- `conflict_review_required`

This vocabulary describes retained, reviewable evidence available to Core. It
does not describe whether a tool step executed.

### Effective evidence status

This companion permits only:

- `review_required`.

### Fresh scoped evidence needed

This companion permits only:

- `yes`.

The literal is a closed routing sentinel, not a truthy string or boolean.

### Reviewed-result field sentinel

This companion permits only:

- `none`.

It applies to `reviewed_repo`, `reviewed_scope`, `reviewed_commit`, and
`reviewed_blob` because no retained result exists to review. It does not erase
the separately populated execution-target binding.

### Fixed false authority sentinel

The packet fields `future_renderer_child_authorized` and `ready_for_codex_c`
must contain the YAML/JSON boolean `false`. Strings, integers, null, unknown,
missing values, or `true` are invalid.

### Final decision

This companion permits only:

- `review_required`.

Any stronger Phase 5 decision requires a new versioned Core decision contract
after durable, independently reviewable evidence and exact owner routing.

Unknown keys, unknown literals, missing required fields, multiple selected
statuses, or contradictory prose invalidate the companion packet.

### Exact field-to-vocabulary binding

Every packet status or sentinel field is bound below. Fixed literals have one
valid value in this companion version.

| Packet field | Binding | Valid value in this packet |
| --- | --- | --- |
| `packet_schema` | Fixed companion schema | `core_grp_id_candidate_reporting_decomposition_evidence_reconciliation.v2` |
| `historical_packet_schema` | Fixed historical schema | `core_grp_id_candidate_reporting_decomposition_decision_packet.v1` |
| `relationship_to_historical_packet` | Baseline relationship | `historical_baseline_preserved_unchanged` |
| `candidate_surface_class` | Fixed candidate class | `mixed_governance_runtime_surface` |
| `candidate_surface_kind` | Fixed candidate kind | `parser_identity_candidate_reporting_surface` |
| `target_ref` | Fixed public target ref | `refs/heads/main` |
| `ordered_tool_steps` | Fixed ordered list | `ars_static_classification`, then `refactor_scout_static_classification` |
| `claim_status` | Version-pinned Automation import | `completed` |
| `approval_use_status` | Version-pinned Automation import | `consumed_by_successful_claim_push` |
| `status_reason` | Version-pinned Automation import | `composite_attempt_completed_classified` |
| `composite_lifecycle_status` | Composite lifecycle | `completed_consumed_single_use` |
| `result_envelope_status` | Version-pinned Automation import | `accepted_contract_conformant_ephemeral_result` |
| `overall_result_status` | Version-pinned Automation import | `complete_review_required` |
| `actual_tool_evidence_result_ref` | Fixed unavailable-result sentinel | `none` |
| `actual_tool_evidence_result_ref_status` | Actual result reference availability | `unavailable_ephemeral_not_retained` |
| `evidence_availability` | Evidence availability | `lifecycle_and_sanitized_envelope_status_only` |
| `evidence_retention` | Evidence retention | `none` |
| `reproducibility_status` | Reproducibility | `not_reproducible_without_new_packet_approval_and_execution` |
| `effective_prior_ars_evidence_found` | Retained tool-evidence presence | `no` |
| `effective_prior_refactor_scout_evidence_found` | Retained tool-evidence presence | `no` |
| `reviewed_repo` | Reviewed-result field sentinel | `none` |
| `reviewed_scope` | Reviewed-result field sentinel | `none` |
| `reviewed_commit` | Reviewed-result field sentinel | `none` |
| `reviewed_blob` | Reviewed-result field sentinel | `none` |
| `reviewed_target_status` | Reviewed target | `execution_target_binding_confirmed_result_not_reviewable` |
| `effective_evidence_status` | Effective evidence status | `review_required` |
| `fresh_evidence_requirement` | Fresh-evidence requirement | `new_retained_reviewable_scoped_evidence_required_before_implementation` |
| `fresh_scoped_evidence_needed_before_implementation` | Fresh scoped evidence needed | `yes` |
| `renderer_recommendation_status` | Renderer recommendation | `historical_renderer_only_recommendation_review_required` |
| `future_renderer_child_authorized` | Fixed false authority sentinel | `false` |
| `packet_reuse_status` | Packet reuse | `forbidden_consumed_packet` |
| `future_retained_result_request` | Packet reuse | `new_packet_approval_and_execution_required` |
| `final_decision` | Final decision | `review_required` |
| `ready_for_codex_c` | Fixed false authority sentinel | `false` |

Unknown, missing, additional, multiply selected, differently typed, or
cross-field contradictory values fail closed to `review_required`. Every
authority flag remains false. A consumer must not infer an unlisted value from
prose, upstream code, issue state, or a later Automation contract.

## Companion Reconciliation Packet

```yaml
  packet_schema: "core_grp_id_candidate_reporting_decomposition_evidence_reconciliation.v2"
historical_packet_schema: "core_grp_id_candidate_reporting_decomposition_decision_packet.v1"
relationship_to_historical_packet: "historical_baseline_preserved_unchanged"
repository: "Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/729"
historical_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/727"
historical_contract: "docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md"
historical_review: "docs/contract_test_reports/core_grp_id_candidate_reporting_decomposition_decision_packet.md"
historical_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/728"
historical_merge_commit: "322a87b5f72c6e6e17872fad83bb2b671ddc8f59"
candidate_id: "grp-id-candidate-reporting"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "parser_identity_candidate_reporting_surface"
target_repository: "Tahjali11/Mythic-Edge"
target_ref: "refs/heads/main"
target_commit: "322a87b5f72c6e6e17872fad83bb2b671ddc8f59"
target_path: "src/mythic_edge_parser/app/grp_id_candidates.py"
target_blob: "517d8061e09f2e220792062c57615a048efa460e"
automation_repository: "Tahjali11/Mythic-Edge-Automation-Artifacts"
automation_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/165"
automation_contract_ref: "automations/adversarial-review-scout/policy/residual_phase_5_scoped_evidence_execution_authority_contract.v2.md"
automation_contract_merge_commit: "d0d9d850f9c609d0cf1e0504f79f52e76ed75169"
packet_id: "grp-id-20260711-9774b7348068"
composite_attempt_id: "grp-id-composite-20260711-bf0261bb056e"
ordered_tool_steps:
  - "ars_static_classification"
  - "refactor_scout_static_classification"
owner_approval_ref: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/165#issuecomment-4947100745"
initial_claim_commit: "abe1698b853c6f9ef7e541e6d2e3438d6de90b0a"
terminal_claim_commit: "92f483ca2b8d6e74d36d057cf67297abe9c498e3"
lifecycle_claim_ref: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/blob/92f483ca2b8d6e74d36d057cf67297abe9c498e3/automations/adversarial-review-scout/claims/manual/residual-phase5-grp-id-grp-id-20260711-9774b7348068.json"
claim_status: "completed"
approval_use_status: "consumed_by_successful_claim_push"
status_reason: "composite_attempt_completed_classified"
composite_lifecycle_status: "completed_consumed_single_use"
result_envelope_status: "accepted_contract_conformant_ephemeral_result"
overall_result_status: "complete_review_required"
sanitized_result_status_ref: "https://github.com/Tahjali11/Mythic-Edge/issues/729"
actual_tool_evidence_result_ref: "none"
actual_tool_evidence_result_ref_status: "unavailable_ephemeral_not_retained"
evidence_availability: "lifecycle_and_sanitized_envelope_status_only"
evidence_retention: "none"
reproducibility_status: "not_reproducible_without_new_packet_approval_and_execution"
effective_prior_ars_evidence_found: "no"
effective_prior_refactor_scout_evidence_found: "no"
reviewed_repo: "none"
reviewed_scope: "none"
reviewed_commit: "none"
reviewed_blob: "none"
reviewed_target_status: "execution_target_binding_confirmed_result_not_reviewable"
execution_target_repository: "Tahjali11/Mythic-Edge"
execution_target_scope: "src/mythic_edge_parser/app/grp_id_candidates.py"
execution_target_commit: "322a87b5f72c6e6e17872fad83bb2b671ddc8f59"
execution_target_blob: "517d8061e09f2e220792062c57615a048efa460e"
effective_evidence_status: "review_required"
fresh_evidence_requirement: "new_retained_reviewable_scoped_evidence_required_before_implementation"
fresh_scoped_evidence_needed_before_implementation: "yes"
renderer_recommendation_status: "historical_renderer_only_recommendation_review_required"
future_renderer_child_authorized: false
packet_reuse_status: "forbidden_consumed_packet"
future_retained_result_request: "new_packet_approval_and_execution_required"
final_decision: "review_required"
ready_for_codex_c: false
```

`effective_prior_ars_evidence_found` and
`effective_prior_refactor_scout_evidence_found` mean retained, reviewable tool
evidence currently available to Core. They remain `no`. The separate
composite-lifecycle fields truthfully record that both declared steps executed
inside the consumed attempt. This distinction prevents both false absence of
execution and false availability of evidence.

## Evidence And Lifecycle Reconciliation Matrix

| Evidence class | Durable reference | Current status | Can Core review its content? | What it proves | What it cannot support |
| --- | --- | --- | --- | --- | --- |
| Historical #727 packet | Merged contract and review at PR #728 | Preserved | Yes, as docs | Original candidate boundary and decision snapshot | Later tool execution |
| V2 Automation authority | Issue #165, PR #166, merged contract | Completed | Yes, as authority docs | Exact future-attempt rules and no-retention boundary | That an attempt ran |
| Exact owner approval | Issue #165 comment `4947100745` | Consumed | Yes, as approval text | One exact single-use composite attempt was approved | Reuse, replay, or general execution |
| Initial lifecycle claim | Commit `abe1698...` | Successfully pushed | Metadata only | Approval was consumed before the composite attempt continued | Tool-result content |
| Terminal lifecycle claim | Commit `92f483c...` | `completed` | Lifecycle fields only | Exact packet and composite attempt reached terminal completion | Classifications, observations, or recommendation |
| Ephemeral result envelope | No retained artifact | Accepted then discarded | No | Sanitized status recorded by issue #729 says contract-conformant result existed | Any result field, label, finding, or reproduction |
| Overall result status | Issue #729 | `complete_review_required` | Status semantics only | The Automation contract's complete/review-required derivation was satisfied | Which labels occurred or what should change |
| Target binding | Claim plus Git tree metadata | Exact match | Metadata only | Attempt bound to exact repo/ref/commit/path/blob | Source behavior, correctness, or decomposition safety |

Lifecycle proof answers whether the exact authorized operation was claimed,
consumed, and completed. Retained evidence would answer what the tools observed
in a form another reviewer can inspect. The first exists; the second does not.

## Actual Tool-Result Reference Decision

`actual_tool_evidence_result_ref` must remain `none`.

Neither the lifecycle claim nor issue #729 is the actual tool result:

- the lifecycle claim intentionally excludes tool results and classifications;
- issue #729 records sanitized envelope and lifecycle statuses, not the
  ephemeral result fields; and
- pointing the result field at either reference would falsely imply that a
  reviewer can inspect or reproduce the result.

The companion therefore uses separate references:

- `lifecycle_claim_ref` for durable execution lifecycle proof; and
- `sanitized_result_status_ref` for the owner-recorded contract-conformance and
  overall-status summary.

Those references must never be consumed as classification, finding,
recommendation, or implementation evidence.

## Consumed Single-Use Lifecycle Consistency

The lifecycle is internally consistent only because all of these facts match:

1. packet ID is `grp-id-20260711-9774b7348068` in approval and claim;
2. composite attempt ID is
   `grp-id-composite-20260711-bf0261bb056e`;
3. the claim lists exactly two ordered, once-only steps;
4. the target repository, ref, commit, path, and blob match the approval;
5. the initial claim commit precedes the terminal claim commit;
6. `approval_use_status` is `consumed_by_successful_claim_push`;
7. terminal `claim_status` is `completed`;
8. terminal reason is `composite_attempt_completed_classified`;
9. evidence mode is `no_write_gate_result` with retention `none`; and
10. the V2 contract makes any existing same-packet claim permanently block
    replay regardless of terminal outcome or expiration.

If any fact becomes missing, contradictory, unknown, or mismatched, effective
status becomes `conflict_review_required`; replay and implementation remain
blocked.

## Meaning Of `complete_review_required`

Under the reviewed Automation V2 contract, `complete_review_required` means
only that both ordered tool steps reached the contract's completed-classified
path and the exact envelope derivation selected the complete, independently
review-required status.

Together with `accepted_contract_conformant_ephemeral_result`, it may support:

- recording that the exact bounded composite attempt completed;
- recording that its ephemeral envelope passed the reviewed schema,
  vocabulary, derivation, and no-echo boundary;
- recording that both tools produced some allowed nonempty classifications at
  execution time; and
- requiring independent Core reconciliation rather than treating execution as
  self-authorizing.

It cannot support:

- reconstructing or naming either tool's classification labels;
- inferring which structural signal was observed;
- converting a classification into a finding or recommendation;
- choosing renderer extraction, `keep_intact`, or another decomposition;
- claiming safety, correctness, separability, decomposability, or review
  completeness;
- satisfying Core's need for durable reviewable implementation evidence;
- creating a renderer or implementation child;
- authorizing Codex C; or
- changing parser/card-identity truth, scoring, ranking, reports, output, CLI,
  launcher, tests, CI, release, or production behavior.

## Effective Decision And Renderer-Only Recommendation

The effective Core decision remains:

```yaml
final_decision: "review_required"
renderer_recommendation_status: "historical_renderer_only_recommendation_review_required"
ready_for_codex_c: false
```

The historical renderer-only recommendation is preserved as a bounded review
candidate. It does not become `keep_intact`, because the ephemeral lifecycle
does not contain durable evidence supporting that stronger choice. It does not
become a decomposition or implementation candidate, because the absent result
content cannot be independently reviewed.

A later separately approved child may be proposed only after a new retained,
reviewable evidence route is completed and a new Core decision contract selects
that route. This companion does not create or authorize that child.

## Future Retained-Result Requirement

The consumed packet, attempt, approval, and claim cannot be replayed, reopened,
extended, or repurposed. Unchanged target blob identity does not change that
rule.

Any future request for retained reviewable evidence requires all of:

1. fresh target ref/commit/path/blob validation;
2. a new versioned Automation authority contract or explicit reviewed amendment
   authorizing a bounded retained public-safe result;
3. a new packet ID;
4. a new composite attempt ID;
5. new exact owner approval;
6. a new unique lifecycle claim and claim key;
7. a newly executed bounded tool attempt;
8. an exact retained-result schema, retention period, revocation,
   supersession, deletion, no-echo, and public-safety contract;
9. independent Automation review of the retained envelope;
10. independent Core Codex E review; and
11. a new Core decision contract before any implementation issue or Codex C
    routing.

No classification from the consumed ephemeral result may be seeded, copied,
remembered, inferred, or treated as expected output in that future attempt.

## False-Authority Matrix

All values are literal and must remain false in this companion:

```yaml
implementation_authorized: false
ready_for_codex_c: false
same_repo_helper_creation_authorized: false
renderer_creation_authorized: false
file_move_authorized: false
cross_repo_extraction_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
replay_authorized: false
rerun_authorized: false
source_reread_authorized: false
result_reconstruction_authorized: false
evidence_retention_authorized: false
source_mutation_authorized: false
source_repo_action_authorized: false
private_log_read_authorized: false
raw_player_log_read_authorized: false
private_evidence_read_authorized: false
fixture_creation_authorized: false
fixture_promotion_authorized: false
card_identity_change_authorized: false
parser_behavior_change_authorized: false
parser_truth_ownership_change_authorized: false
submitted_deck_interpretation_change_authorized: false
candidate_scoring_change_authorized: false
candidate_ranking_change_authorized: false
evidence_weight_change_authorized: false
promotion_behavior_change_authorized: false
confirmation_behavior_change_authorized: false
deferral_behavior_change_authorized: false
report_schema_change_authorized: false
report_text_change_authorized: false
report_output_path_change_authorized: false
report_write_behavior_change_authorized: false
cli_behavior_change_authorized: false
launcher_behavior_change_authorized: false
api_payload_change_authorized: false
workbook_webhook_apps_script_change_authorized: false
ci_change_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
analytics_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
release_readiness_claimed: false
deploy_readiness_claimed: false
production_readiness_claimed: false
production_behavior_claimed: false
truth_or_assurance_claimed: false
```

A missing, true, null, unknown, caller-overridden, or prose-contradicted value
invalidates the packet and leaves routing blocked.

## Required Non-Claims

The companion does not claim:

- the candidate is safe, unsafe, correct, incorrect, separable, decomposable,
  or suitable for renderer extraction;
- the module should remain intact;
- any ephemeral classification label, observation, finding, severity,
  rationale, or recommendation;
- parser/card-identity truth or successful behavior validation;
- evidence reproducibility or retained evidence availability;
- implementation, file movement, helper creation, or Codex C authority;
- security or privacy assurance;
- release, deploy, or production readiness; or
- production behavior.

The exact target path and blob are public binding metadata. Their presence is
not source review, behavioral evidence, or permission to inspect the blob.

## Inputs

Allowed inputs for this docs-only reconciliation:

- Core governance docs, accepted ADRs, issue metadata, contracts, reviews, and
  PR metadata;
- Automation issue, PR, authority-contract, approval, and lifecycle-claim
  metadata;
- the sanitized envelope statuses supplied in issue #729;
- public Git object type and exact path/blob identity metadata; and
- no other source or evidence content.

Forbidden inputs:

- target source contents;
- raw diffs, patches, blame, adjacent files, or repository-history contents;
- ephemeral classification labels or tool-result fields;
- local reports, generated evidence, raw output, exceptions, logs, Player.log,
  decklists, hand evidence, SQLite, workbooks, runtime artifacts, or private
  paths; and
- remembered, reconstructed, inferred, or model-generated substitutes for the
  discarded result.

## Outputs And Side Effects

Allowed output:

- this one docs-only companion contract.

Allowed side effects:

- none beyond creating the untracked contract file in the isolated worktree.

Forbidden side effects:

- editing the #727 historical contract or review;
- changing runtime source, tests, fixtures, reports, snapshots, or generated
  artifacts;
- running Automation tools or creating claims;
- creating an implementation issue, renderer, branch action, PR, commit, push,
  merge, or tracker closeout; and
- changing external, production, parser, analytics, workbook, AI, or CI state.

## Invariants And Cross-Field Derivations

1. Historical baseline preserved plus later lifecycle completion does not
   mutate the historical snapshot.
2. `claim_status: completed`, consumed approval, and terminal composite reason
   derive `completed_consumed_single_use` only when packet, attempt, steps, and
   target binding all match.
3. Retention `none` requires actual result reference `none`, result-reference
   status `unavailable_ephemeral_not_retained`, evidence availability
   `lifecycle_and_sanitized_envelope_status_only`, and retained prior-tool
   evidence `no` for both tools.
4. Lifecycle completion permits exact execution-target metadata but not
   populated reviewed-result fields. `reviewed_repo`, `reviewed_scope`,
   `reviewed_commit`, and `reviewed_blob` remain `none`.
5. `complete_review_required` requires `final_decision: review_required`; it
   cannot produce a renderer, keep-intact, or implementation decision.
6. No retained reviewable result requires fresh evidence before implementation,
   even though a fresh ephemeral execution occurred.
7. Consumed single-use state requires replay and rerun authority false and a
   completely new packet path for any future request.
8. `ready_for_codex_c` may become true only in a later Core contract after the
   evidence, review, and owner-routing gates are independently satisfied.
9. Every truth, readiness, assurance, behavior-change, and implementation flag
   remains false regardless of lifecycle or validation success.
10. Unknown keys, unknown statuses, conflicting references, target drift, or
    missing evidence fail closed to `review_required`.

## Error And Drift Behavior

Return to Codex B or the owner and keep all authority false if:

- issue, PR, commit, packet, attempt, approval, claim, path, or blob references
  do not match;
- the claim lifecycle is missing, replayed, reordered, expired before claim,
  revoked, superseded, or contradictory;
- the target ref advances or its path/blob binding changes;
- someone attempts to use the lifecycle claim or issue #729 as the actual tool
  result;
- an ephemeral label or source-derived observation appears;
- any role tries to reconstruct the discarded result;
- a future retained-result proposal lacks a new packet, approval, claim, and
  execution authority;
- the renderer recommendation is promoted without durable evidence; or
- any implementation, truth, readiness, security, privacy, release, deploy, or
  production claim is requested.

Target drift does not authorize source inspection. It blocks this companion's
use for current routing and requires a new metadata-only framing pass.

## Validation Requirements

This Codex B pass must validate only documentation, references, lifecycle
consistency, and scope:

```powershell
git status --short --branch
git cat-file -t 322a87b5f72c6e6e17872fad83bb2b671ddc8f59
git ls-tree 322a87b5f72c6e6e17872fad83bb2b671ddc8f59 -- src/mythic_edge_parser/app/grp_id_candidates.py
py tools/check_agent_docs.py
py tools/check_protected_surfaces.py --base origin/main
py tools/check_secret_patterns.py --base origin/main
git diff --check
```

Validation must also prove:

- #727 is closed and PR #728 merged at the exact Core target commit;
- issue #165 and PR #166 identify the accepted V2 authority contract;
- the approval, initial claim commit, terminal claim commit, packet, attempt,
  tool order, target binding, consumed status, terminal status, output mode, and
  no-retention rule are mutually consistent;
- every status and cross-field derivation is closed;
- no target contents, raw diff, ephemeral label, private value, local path,
  source snippet, or result reconstruction appears;
- all false-authority and non-claim fields are present;
- only this contract changed; and
- no runtime source, tests, fixtures, generated reports, or private artifacts
  were added or modified.

Passing these checks validates the docs-only reconciliation only. It does not
validate source behavior or authorize implementation.

## Acceptance Criteria

- [x] #727 remains the identifiable, unchanged historical baseline.
- [x] This companion controls only post-#727 lifecycle and current routing.
- [x] Lifecycle proof and retained evidence are distinct.
- [x] The lifecycle claim and #729 are not misrepresented as an actual result.
- [x] Evidence availability, retention, reproducibility, reviewed-target,
      fresh-evidence, final-decision, and Codex C states are exact.
- [x] Every packet status and sentinel field is bound to a closed local
      vocabulary, exact fixed literal, or version-pinned Automation import.
- [x] `complete_review_required` has bounded support and explicit non-support.
- [x] Missing ephemeral classifications are neither reconstructed nor inferred.
- [x] The renderer-only recommendation remains historical and
      `review_required`.
- [x] Any future retained result requires a new packet, approval, claim, and
      execution route.
- [x] Every false-authority and non-claim flag remains preserved.
- [x] No code, test, fixture, generated artifact, or external state changes.
- [x] Independent Codex E review is required next.

## Unresolved Risks

- The actual classification labels and result rows are intentionally
  unavailable and cannot be independently inspected.
- `complete_review_required` proves a valid ephemeral result state, not its
  content or usefulness for Core decomposition.
- A future retained-result design would change the Automation retention
  boundary and therefore requires new Automation authority, not merely a Core
  issue.
- Source drift after the bound commit invalidates target freshness without
  revealing whether the old result would still apply.
- The renderer-only boundary remains plausible historical framing, not a
  reviewed implementation recommendation.

## Next Workflow Action

Next role: Codex E, independent contract reviewer.

Codex E must review this companion against issue #729, the immutable #727
packet, the Automation V2 contract, and the terminal lifecycle claim. Codex E
must not inspect source or reconstruct ephemeral labels. A passing review may
make the companion eligible for owner consideration as a docs artifact only;
it must not route to Codex C or create a renderer child.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Core Decision-Packet Reconciliation Reviewer.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/729

Historical issue:
https://github.com/Tahjali11/Mythic-Edge/issues/727

Review:
- docs/contracts/core_grp_id_candidate_reporting_decomposition_evidence_reconciliation.md
- docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md
- docs/contract_test_reports/core_grp_id_candidate_reporting_decomposition_decision_packet.md
- public-safe Automation issue #165 authority and lifecycle metadata only

Verify that #727 remains an unchanged historical baseline; lifecycle proof is
separate from retained evidence; the lifecycle claim and issue #729 are not
used as an actual tool-result reference; all evidence, reproducibility,
retention, reviewed-target, fresh-evidence, decision, renderer, and Codex C
states are closed and cross-field coherent; complete_review_required is not
treated as a recommendation; and a future retained-result request requires a
new packet, approval, claim, and execution.

Reconcile `GRPID-RECON-E-001`. Verify that every status and sentinel in the
companion packet is bound by the exact field-to-vocabulary table; only the five
listed Automation literals are imported from the exact version-pinned
authority; and unknown, missing, additional, differently typed, or
contradictory values fail closed with every authority flag false.

Do not inspect or reread target source, raw diffs, adjacent files, repository
history contents, private/local evidence, or ephemeral classifications. Do not
run ARS or Refactor Scout, reconstruct labels, implement code, create a
renderer, move files, authorize Codex C, or claim safety, correctness,
decomposability, truth, readiness, security/privacy assurance, release, deploy,
or production behavior. Lead with findings and route ambiguity back to Codex B.
```

## instruction_context

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0001"
    - "ADR-0004"
    - "ADR-0005"
  protected_surfaces:
    - "parser and card identity truth"
    - "decomposition and implementation authority"
    - "Automation single-use lifecycle"
    - "ephemeral evidence and no-echo boundary"
    - "generated and private artifacts"
  authority_conflicts_found: false
  authority_conflict_notes: "none"
  stop_conditions:
    - "Do not inspect target source or repository-history contents."
    - "Do not reconstruct ephemeral classifications or result fields."
    - "Do not run or replay Automation tools or retain evidence."
    - "Do not authorize Codex C, implementation, helper creation, or file movement."
    - "Do not claim truth, readiness, safety, correctness, decomposability, or assurance."
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/729"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  residual_promotion_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
  historical_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/727"
  automation_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/165"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/729"
  target_artifact: "docs/contracts/core_grp_id_candidate_reporting_decomposition_evidence_reconciliation.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_approval"
  branch: "codex/grp-id-evidence-reconciliation-729"
  target_commit: "322a87b5f72c6e6e17872fad83bb2b671ddc8f59"
  target_blob: "517d8061e09f2e220792062c57615a048efa460e"
  packet_id: "grp-id-20260711-9774b7348068"
  composite_attempt_id: "grp-id-composite-20260711-bf0261bb056e"
  lifecycle_claim_status: "completed"
  result_envelope_status: "accepted_contract_conformant_ephemeral_result"
  overall_result_status: "complete_review_required"
  evidence_retained: false
  actual_tool_evidence_result_ref: "none"
  final_decision: "review_required"
  renderer_recommendation_status: "historical_renderer_only_recommendation_review_required"
  replay_authorized: false
  rerun_authorized: false
  ready_for_codex_c: false
  implementation_authorized: false
  source_reread_authorized: false
  evidence_retention_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  finding_reconciliation:
    GRPID-RECON-E-001: "vocabulary_closed_pending_codex_e_confirmation"
  validation:
    - "py tools/check_agent_docs.py -> passed, errors 0, warnings 0"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "all seven cited result/status fields found in exact field-binding table"
    - "schema-v2 consistency and Automation-import marker checks passed"
    - "git diff and direct untracked-file whitespace checks passed"
    - "changed scope contains only the revised contract and preserved Codex E report"
  stop_conditions:
    - "Preserve #727 and do not rewrite its historical evidence snapshot."
    - "Do not use lifecycle or sanitized status references as actual tool evidence."
    - "Do not inspect source, rerun tools, reconstruct labels, retain evidence, or implement code."
    - "Do not authorize Codex C or any truth, readiness, assurance, or production claim."
```
