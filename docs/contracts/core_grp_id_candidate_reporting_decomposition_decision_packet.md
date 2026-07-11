# Core GRP ID Candidate Reporting Decomposition Decision Packet Contract

## Module

This contract records the Phase 5 decomposition decision packet for
`grp-id-candidate-reporting` at:

`src/mythic_edge_parser/app/grp_id_candidates.py`

The decision is docs-only. The module remains the public facade. The packet
recommends only a possible future extraction of pure report rendering behind
that facade and keeps the canonical decision `review_required`.

## Source Issue And Authority

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/727
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Decomposition tracker: https://github.com/Tahjali11/Mythic-Edge/issues/463
- Residual promotion queue: https://github.com/Tahjali11/Mythic-Edge/issues/715
- Approval-packet validation provenance:
  https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/159
- Execution-authority contract provenance:
  https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161
- Constitution: `docs/agent_constitution.md`
- Role rules: `docs/agent_threads/module_contract.md`
- Template: `docs/templates/module_contract.md`
- Accepted repository-boundary policy:
  `docs/decisions/ADR-0006-repository-boundary-strategy.md`

Current target commit:

`4b5c3d7d6ffd566858f123039db2d4bf8690e6e4`

Authority-contract target commit:

`9528bb3bee9c1d241268cb8a7d1a806b118471de`

The target file has the same Git blob at both commits:

`517d8061e09f2e220792062c57615a048efa460e`

The identical blob supports docs-only source-drift framing. It is not an ARS or
Refactor Scout result. Issue #159 durably proves approval-packet classification,
and issue #161 durably proves the later execution-authority contract. Their
closeouts explicitly record that no ARS run, Refactor Scout run, or source
inspection occurred. No durable prior tool-evidence result is cited by this
packet.

The lineage does not create execution authority, implementation authority,
file-move authority, or a readiness, truth, security, or privacy claim. Any
later blob drift fails closed. Even without blob drift, the shared mixed-surface
gate requires fresh scoped evidence before implementation routing.

## Instruction Context

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
    - "docs/decisions/ADR-0001-parser-owns-truth.md"
    - "docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md"
    - "docs/decisions/ADR-0006-repository-boundary-strategy.md"
  protected_surfaces:
    - "parser/card-identity candidate scoring and ranking"
    - "Arena grpId and card identity semantics"
    - "submitted-deck and private hand-confirmation evidence"
    - "candidate promotion, confirmation, and deferral lifecycle"
    - "generated JSON and Markdown report schemas, text, paths, and writes"
  authority_conflicts_found: false
  authority_conflict_notes: "None. Issue #727 authorizes a docs-only decision packet and explicitly blocks implementation."
  stop_conditions:
    - "Do not authorize Codex C, implementation, or file movement."
    - "Stop on target-file blob drift from 517d8061e09f2e220792062c57615a048efa460e."
    - "Stop if renderer extraction cannot preserve the public facade and exact output behavior."
    - "Stop before reading private evidence or running ARS or Refactor Scout."
```

## Owning Layer And Truth Boundary

Internal project area: Parser, with shared Corpus / Provenance and Analytics
consumers.

Truth owner:

- MTGA `Player.log` remains the observable raw evidence source.
- Parser/state and approved card-identity code own parser-managed identity
  interpretation.
- Candidate rows, scores, evidence summaries, and generated reports are review
  support. They are not confirmed parser truth by themselves.
- Promotion and manual confirmation remain protected lifecycle operations in
  the existing facade. A renderer must never own or trigger them.
- Downstream Analytics, workbook, webhook, Apps Script, UI, launcher, and AI
  surfaces must not reinterpret candidate output as confirmed identity.

Bridge-code status: `shared_support`.

Allowed flow:

```text
parser/card evidence -> candidate scoring and lifecycle facade -> local reports and operator review
```

Forbidden reverse flow:

```text
report text, launcher display, workbook, analytics, or AI output -/-> parser/card identity truth
```

## Files Owned By This Contract

This Codex B pass owns only:

- `docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md`

The following are inspected interfaces, not files authorized for change:

- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `score_grp_id_candidates.py`
- `tools/auto_launcher/manasight_launcher_auto.py`
- `src/mythic_edge_parser/app/card_catalog_refresh.py`
- `src/mythic_edge_parser/app/hand_confirmations.py`
- `tests/test_grp_id_candidates.py`

The possible future private renderer module named later in this contract is a
recommendation only. It is not owned for creation by issue #727 or this pass.

## Observed Current Behavior

`grp_id_candidates.py` currently combines:

- public dataclasses for submitted-deck evidence, scores, evidence channels,
  candidate rows, reports, promotions, deferrals, and inferred review;
- local input loading for submitted decks, override data, card catalogs, and
  hand-confirmation evidence;
- fingerprint, card-type, color, mana, cooccurrence, count, and manual
  confirmation scoring;
- deterministic ranking, evidence summaries, confirmation state, and
  suggestion decisions;
- JSON payload assembly and JSON report writes;
- Markdown report rendering and writes;
- inferred-review report rendering and writes; and
- promotion, confirmation, and deferral updates to local override data.

Current direct consumers include:

- `tests/test_grp_id_candidates.py`;
- `src/mythic_edge_parser/app/card_catalog_refresh.py`;
- `src/mythic_edge_parser/app/hand_confirmations.py`;
- the root CLI `score_grp_id_candidates.py`; and
- `tools/auto_launcher/manasight_launcher_auto.py`, which invokes that CLI for
  `--confirm-grp-id`, `--defer-grp-id`, and `--promote-singletons` actions.

The decomposition reason is mixed responsibility and reviewability, not line
count alone.

## Codex E Finding Reconciliation

This revision addresses the Codex E findings for independent re-review:

- `GRPID-DECOMP-E-001`: the issue-specific envelope now preserves every base
  Phase 5 field or names its versioned override. `target_commit` is restored as
  the envelope baseline; `current_target_commit` remains the separate evidence
  field. Issue #664 and all EventBus, API/frontend/live-capture, and parser-state
  deferrals are explicit.
- `GRPID-DECOMP-E-002`: the consumer and validation boundaries now include the
  direct `score_grp_id_candidates.py` CLI and the launcher invocations that
  execute it for confirm, defer, and singleton-promotion actions.
- `GRPID-DECOMP-E-003`: unchanged committed-blob lineage remains sufficient for
  this docs-only framing pass, while the canonical shared field requires fresh
  scoped evidence before any implementation routing. Blob lineage is not tool
  evidence.
- `GRPID-DECOMP-E-004`: the private renderer may receive already-built report
  values in memory, but it may not read source files or create new/public echo.
  Existing local-only report output remains exact and unchanged.
- `GRPID-DECOMP-E-005`: #159 and #161 are now classified only as
  approval-packet and execution-authority-contract provenance. Prior ARS and
  Refactor Scout evidence flags and reviewed-target fields fail closed because
  no durable tool-result artifact is linked.

These corrections do not change the recommendation, authorize implementation,
or weaken any parser-truth, privacy, false-authority, or non-claim boundary.

## Phase 5 Packet Schema And Vocabulary Binding

This packet is not a direct instance of the #665
`core_governance_report_helper_phase_5_decomposition_decision_packet.v1`
schema because this candidate touches parser/card-identity support and private
local evidence. It is an issue #727 schema extension that reuses the shared
Phase 5 field names, false-authority flags, ARS/Refactor evidence fields,
decision vocabulary, and cross-field fail-closed behavior.

Base vocabulary reused:

- `final_decision` values:
  `same_repo_keep_current_path`, `same_repo_decomposition_candidate`,
  `request_fresh_ars_refactor_evidence`, `request_scope_split_child`,
  `reject_cross_repo_extraction`, `defer`, `unsupported`, and
  `review_required`;
- ARS/Refactor fields:
  `prior_ars_evidence_found`, `prior_refactor_scout_evidence_found`,
  `reviewed_repo`, `reviewed_scope`, `reviewed_commit`,
  `ars_version_contract_bundle`, `current_target_commit`,
  `relevant_changes_since_review`, `evidence_status`,
  `fresh_scoped_evidence_needed`, and `reason`;
- required candidate-row fields from the shared Phase 5 packet; and
- false-authority and non-claim behavior.

Issue #727 extension:

```yaml
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
packet_schema: "core_grp_id_candidate_reporting_decomposition_decision_packet.v1"
schema_extension_owner: "docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md"
schema_extension_scope: "issue_727_grp_id_candidate_reporting_only"
candidate_scope: "grp_id_candidate_reporting_only"
candidate_surface_class_source: "shared_phase_5_vocabulary"
candidate_surface_kind_source: "issue_727_extension"
```

The extension adds exactly one secondary `candidate_surface_kind`:

- `parser_identity_candidate_reporting_surface`: a parser/card-identity
  support surface that builds deterministic candidate scores and review
  reports and performs separately guarded promotion/review lifecycle actions,
  without making a candidate row confirmed parser truth by itself.

This secondary kind is allowed only when:

- `packet_schema` is
  `core_grp_id_candidate_reporting_decomposition_decision_packet.v1`;
- `schema_extension_scope` is
  `issue_727_grp_id_candidate_reporting_only`;
- `candidate_id` is `grp-id-candidate-reporting`;
- `current_path` is
  `src/mythic_edge_parser/app/grp_id_candidates.py`;
- `candidate_surface_class` is `mixed_governance_runtime_surface`;
- `final_decision` is `review_required`; and
- every false-authority flag in this contract remains false.

The issue-local kind does not extend the shared #665 registry and cannot relax
the primary-class routing rule. A validator that understands only #665 must
fail closed rather than coerce this packet into a pure governance/helper row.

Base-envelope preservation and versioned overrides:

| Base Phase 5 field | Issue #727 rule |
| --- | --- |
| `packet_schema` | Versioned override to `core_grp_id_candidate_reporting_decomposition_decision_packet.v1`; `base_phase_5_packet_schema` preserves the inherited schema identity. |
| `candidate_scope` | Versioned override to `grp_id_candidate_reporting_only`. |
| `target_commit` | Preserved as the packet baseline. It is not replaced by the evidence-block field `current_target_commit`. |
| `related_ars_gate_issue` | Preserved and bound to issue #664 whenever ARS or Refactor evidence status is considered. |
| `eventbus_support_deferred` | Preserved and must be `true`. |
| `api_frontend_live_capture_deferred` | Preserved and must be `true`. |
| `parser_state_deferred` | Preserved and must be `true`. |
| Every other required base envelope field | Preserved under its base name and fail-closed requirement. |

No omitted base field is implicitly replaced. Any future extension must name
its replacement field, compatibility meaning, and validator behavior in a new
packet schema version.

Cross-field routing for this packet:

| `candidate_surface_class` | Permitted `final_decision` values |
| --- | --- |
| `mixed_governance_runtime_surface` | `review_required`, `request_scope_split_child` |

Required issue #727 pair:

```yaml
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "parser_identity_candidate_reporting_surface"
final_decision: "review_required"
```

The issue description's `parser_truth_surface` label is preserved as a risk
and protected-contact classification, not used as the canonical Phase 5
primary class. The candidate-reporting module is truth-adjacent, but its
candidate rows are not confirmed parser truth. Treating the module as a pure
`parser_truth_surface` would erase that distinction and is forbidden.

## Packet Envelope

```yaml
packet_schema: "core_grp_id_candidate_reporting_decomposition_decision_packet.v1"
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
schema_extension_owner: "docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md"
schema_extension_scope: "issue_727_grp_id_candidate_reporting_only"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/727"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
residual_promotion_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
approval_packet_validation_provenance: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/159#issuecomment-4935133049"
execution_authority_contract_provenance: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161#issuecomment-4920908510"
actual_tool_evidence_result_ref: "none"
target_artifact: "docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md"
target_commit: "4b5c3d7d6ffd566858f123039db2d4bf8690e6e4"
authority_contract_target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
current_target_commit: "4b5c3d7d6ffd566858f123039db2d4bf8690e6e4"
authority_contract_target_blob: "517d8061e09f2e220792062c57615a048efa460e"
current_target_blob: "517d8061e09f2e220792062c57615a048efa460e"
candidate_scope: "grp_id_candidate_reporting_only"
candidate_id: "grp-id-candidate-reporting"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "parser_identity_candidate_reporting_surface"
current_path: "src/mythic_edge_parser/app/grp_id_candidates.py"
phase_5_order_preserved: true
eventbus_support_deferred: true
api_frontend_live_capture_deferred: true
parser_state_deferred: true
final_decision: "review_required"
recommended_first_slice: "extract_pure_report_renderers_only"
same_repo_first: true
ready_for_codex_c: false
implementation_authorized: false
same_repo_helper_creation_authorized: false
file_move_authorized: false
cross_repo_extraction_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
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

An absent, true, unknown, stale, revoked, superseded, or prose-contradicted
false-authority field invalidates the packet. Unknown keys fail closed until a
new versioned contract defines them.

## Required Candidate Row

The canonical candidate row contains every shared required field plus the
issue #727 extension fields needed to preserve private evidence, generated
reports, the direct CLI, and launcher consumers.

```yaml
candidate_id: "grp-id-candidate-reporting"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "parser_identity_candidate_reporting_surface"
current_path: "src/mythic_edge_parser/app/grp_id_candidates.py"
current_behavior: "Loads local candidate evidence, computes deterministic candidate scores and review states, renders local JSON and Markdown reports, and performs guarded promotion, confirmation, and deferral updates."
truth_or_authority_owner: "Parser/card-identity code owns confirmed parser-managed identity; candidate rows and reports remain review support and do not become confirmed parser truth by themselves."
upstream_dependencies:
  - "src/mythic_edge_parser/app/grp_id_catalog.py"
  - "src/mythic_edge_parser/app/grp_id_overrides.py"
  - "src/mythic_edge_parser/app/hand_confirmations.py"
  - "submitted-deck and local match-log artifacts through existing facade behavior"
downstream_consumers:
  - "score_grp_id_candidates.py"
  - "tools/auto_launcher/manasight_launcher_auto.py"
  - "src/mythic_edge_parser/app/card_catalog_refresh.py"
  - "src/mythic_edge_parser/app/hand_confirmations.py"
  - "tests/test_grp_id_candidates.py"
protected_surface_contact: "mixed_review_required"
proposed_destination: "same_repo_private_renderer_module_behind_grp_id_candidates_facade"
why_not_keep_local: "Keeping the module intact remains valid. A renderer-only split may improve reviewability by isolating pure formatting without moving scoring, identity, evidence loading, lifecycle writes, public dataclasses, or the facade."
why_not_move_to_existing_repo: "Sibling repositories do not own Mythic Edge parser/card-identity candidate reporting or its private local evidence boundary."
why_not_create_new_repo: "A new repository would create version skew and a new public interface for a renderer that has no proven independent ownership boundary."
new_public_interface_needed: "private_same_repo"
new_public_interface_description: "The existing public facade remains mythic_edge_parser.app.grp_id_candidates. A future renderer helper, if separately authorized, is private same-repo support and receives already-built report objects only."
behavior_preservation_tests:
  - "PYTHONPATH=src python3 -m pytest -q tests/test_grp_id_candidates.py"
  - "PYTHONPATH=src python3 score_grp_id_candidates.py --help"
  - "focused CLI tests or an isolated subprocess harness for default scoring, --confirm-grp-id, --defer-grp-id, and --promote-singletons without private inputs"
  - "focused launcher tests proving _project_helper_command and _run_project_helper still invoke score_grp_id_candidates.py with the same argument vectors"
  - "byte-for-byte or normalized snapshot comparison for JSON payloads, Markdown text, summary lines, paths, ordering, and newline behavior"
rollback_plan: "Revert the later implementation commit, restore renderer functions to grp_id_candidates.py, remove the private support module, and preserve existing local artifacts without migration or rewrite."
ars_refactor_evidence_status: "approval_gate_and_authority_contract_only_no_tool_result_fresh_implementation_evidence_required"
private_input_boundary: "no_direct_file_read_no_new_or_public_echo_existing_local_report_preserved"
generated_output_boundary: "existing_local_paths_and_write_behavior_unchanged"
direct_cli_boundary: "score_grp_id_candidates.py remains a direct consumer of the grp_id_candidates facade with all current flags, stdout labels, exit behavior, and report-path display unchanged"
launcher_boundary: "manasight_launcher_auto.py continues invoking score_grp_id_candidates.py for --confirm-grp-id, --defer-grp-id, and --promote-singletons with unchanged command construction and output parsing"
recommended_first_slice: "extract_pure_report_renderers_only"
non_claims:
  - "not_implementation_authority"
  - "not_codex_c_authority"
  - "not_file_move_authority"
  - "not_same_repo_helper_creation_authority"
  - "not_cross_repo_extraction_authority"
  - "not_ars_or_refactor_scout_run_authority"
  - "not_private_evidence_read_authority"
  - "not_fixture_creation_or_promotion_authority"
  - "not_card_identity_change_authority"
  - "not_parser_truth"
  - "not_analytics_truth"
  - "not_security_assurance"
  - "not_privacy_assurance"
  - "not_release_readiness"
  - "not_deploy_readiness"
  - "not_production_readiness"
  - "not_production_behavior"
final_decision: "review_required"
```

`ars_refactor_evidence_status` above is issue-local summary metadata. The
canonical evidence block below remains authoritative for the shared Phase 5
evidence fields.

## Evidence Provenance And Fail-Closed Tool Status

The durable lineage is classified before the shared evidence block:

```yaml
approval_packet_validation_provenance:
  issue_ref: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/159"
  closeout_ref: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/159#issuecomment-4935133049"
  status: "approval_packet_classification_completed"
  proves: "public-safe approval packet classification only"
  does_not_prove: "ARS run, Refactor Scout run, source inspection, or candidate evidence result"
execution_authority_contract_provenance:
  issue_ref: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161"
  closeout_ref: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161#issuecomment-4920908510"
  status: "execution_authority_contract_completed_execution_not_authorized"
  proves: "future exact owner-approval and execution boundary only"
  does_not_prove: "ARS run, Refactor Scout run, source inspection, or candidate evidence result"
actual_tool_evidence_result_ref: "none"
```

The following shared Phase 5 evidence fields therefore fail closed:

```yaml
prior_ars_evidence_found: "no"
prior_refactor_scout_evidence_found: "no"
reviewed_repo: "none"
reviewed_scope: "none"
reviewed_commit: "none"
reviewed_blob: "none"
ars_version_contract_bundle: "none"
current_target_commit: "4b5c3d7d6ffd566858f123039db2d4bf8690e6e4"
current_target_blob: "517d8061e09f2e220792062c57615a048efa460e"
relevant_changes_since_review: "not_applicable"
prior_tool_evidence_status: "absent"
contract_framing_source_status: "committed_target_blob_lineage_only_not_tool_evidence"
evidence_status: "fresh_scoped_evidence_required_before_implementation"
fresh_scoped_evidence_needed: "yes"
fresh_scoped_evidence_needed_for_contract_framing: "no"
fresh_scoped_evidence_needed_before_implementation: "yes"
reason: "Issues #159 and #161 prove approval-packet validation and an execution-authority contract, but their closeouts explicitly state that no ARS run, Refactor Scout run, or source inspection occurred. No durable candidate evidence result is linked, so prior tool-evidence and reviewed-target fields remain fail-closed. The unchanged Git blob is docs-only drift context, not tool evidence. Because the candidate is a mixed governance/runtime surface, fresh scoped evidence remains required before implementation routing. This contract does not authorize issue #664 execution, ARS, Refactor Scout, implementation, file movement, source reads, private evidence access, or any truth, readiness, security, or privacy claim."
```

`prior_tool_evidence_status`, `contract_framing_source_status`, and
`fresh_scoped_evidence_needed_for_contract_framing` are issue #727 extension
fields. They distinguish source-drift context from actual ARS/Refactor evidence
and do not replace or weaken canonical `evidence_status` or
`fresh_scoped_evidence_needed`. Those canonical fields govern later routing and
require fresh scoped evidence before any implementation child may proceed.

Issue #664 remains the applicable ARS gate. This contract records the gate but
does not authorize an ARS or Refactor Scout run. If fresh evidence is later
approved, its reviewed repository, scope, commit, contract bundle, and result
must replace the historical-only implementation basis before Codex C can be
considered.

## Decomposition Decision

Canonical Phase 5 decision: `review_required`.

Non-authoritative recommendation for Codex E review:

- Keep `src/mythic_edge_parser/app/grp_id_candidates.py` as the public facade.
- If a later owner-approved child is created, consider only pure report
  rendering as the first same-repo slice.
- A possible private helper name is
  `src/mythic_edge_parser/app/grp_id_candidate_report_renderer.py`.
- Keep dataclasses, payload loading, scoring, ranking, evidence evaluation,
  report construction, promotion, confirmation, deferral, inferred-review
  construction, and all local writes in the facade for the first slice.
- The renderer may receive complete already-built report objects and read their
  in-memory fields, including local/private-derived values already present under
  the existing local report contract. It may return text only. It must not load
  files, discover paths, score candidates, decide identity, promote or defer
  candidates, choose output paths, or broaden where any value is emitted.

This recommendation is not encoded as `same_repo_decomposition_candidate`
because the primary class is `mixed_governance_runtime_surface`; the shared
cross-field rule keeps the packet at `review_required` until independent
review and later owner routing.

## Recommended Renderer-Only Slice Boundary

If Codex E later finds the recommendation coherent and a separate owner-approved
implementation child is created, the first slice should be limited to pure
Markdown text construction behind the existing facade.

Possible private helper:

`src/mythic_edge_parser/app/grp_id_candidate_report_renderer.py`

Possible private same-repo functions, with final names left to a later
implementation contract:

```python
def render_grp_id_candidate_markdown(report: GrpIdCandidateReport) -> str: ...

def render_inferred_review_markdown(report: InferredReviewReport) -> str: ...
```

The existing public writers remain in `grp_id_candidates.py` and retain path
selection, directory handling, encoding, file writes, return values, and error
behavior:

- `write_grp_id_candidate_markdown(...)`
- `write_inferred_review_reports(...)`

The following stay in the facade in the first slice:

- `_report_payload(...)` and all JSON payload assembly;
- `write_grp_id_candidate_report(...)`;
- all report-object construction;
- all dataclasses and `summary_line()` methods;
- all input loading, scoring, ranking, and evidence evaluation;
- all promotion, confirmation, and deferral logic; and
- all output-path selection and file writes.

The renderer accepts already-built report objects and returns strings only. It
may inspect fields on those objects solely to reproduce the existing Markdown
text. It must have no filesystem, environment, network, workbook, subprocess,
parser state, override, or local-evidence side effects. This exact boundary is
a review recommendation, not implementation authority.

## Public And Consumer Interfaces To Preserve

The existing module path remains public:

```python
from mythic_edge_parser.app import grp_id_candidates
```

Public dataclass identity, constructor fields, defaults, ordering, equality,
and `asdict` output must remain unchanged, including:

- `SubmittedDeckSnapshot`
- `CandidateScore`
- `EvidenceChannel`
- `CandidateEvidenceSummary`
- `GrpIdCandidateRow`
- `GrpIdCandidateReport`
- `PromotedSuggestion`
- `InferredReviewSuggestion`
- `ManualConfirmationEvidence`
- `InferredReviewReport`
- `DeferredSuggestion`
- `CandidateScoringContext`
- `CandidateReportInputs`

Public functions used by direct consumers remain reachable with unchanged
signatures and behavior, including:

- `build_grp_id_candidate_report(...)`
- `write_grp_id_candidate_report(...)`
- `write_grp_id_candidate_markdown(...)`
- `load_grp_id_candidate_report(...)`
- `promote_auto_suggestions(...)`
- `promote_auto_suggestions_with_details(...)`
- `confirm_candidate_suggestion(...)`
- `defer_candidate_suggestion(...)`
- `build_inferred_review_report(...)`
- `write_inferred_review_reports(...)`

The direct root CLI `score_grp_id_candidates.py` is a required compatibility
consumer. A later implementation must preserve:

- its imports from `mythic_edge_parser.app.grp_id_candidates`;
- arguments `--decklist`, `--format`, `--promote-singletons`,
  `--confirm-grp-id`, `--defer-grp-id`, and `--hand-confirmations`;
- default scoring versus saved-report behavior;
- current argument precedence and combinations;
- stdout prefixes and ordering, including `Confirmed:`, `Deferred:`,
  `Promoted overrides:`, `Promoted:`, the report summary line, `Report:`, and
  `Readable report:`;
- exit code and exception behavior; and
- existing local-only path behavior without echoing new private values.

The launcher is also a required compatibility consumer. A later implementation
must preserve these existing invocations:

```text
score_grp_id_candidates.py --confirm-grp-id <grp_id>
score_grp_id_candidates.py --defer-grp-id <grp_id>
score_grp_id_candidates.py --promote-singletons
```

It must also preserve the launcher's helper-command construction, subprocess
working directory, busy states, success/failure handling, parsed output
prefixes, and user-visible status behavior. The renderer extraction must not
require launcher imports from a new helper module.

## Inputs And Privacy Boundary

Allowed contract evidence:

- committed source and tests at the current target commit;
- public GitHub issue and PR metadata;
- the public-safe #159 approval-packet and #161 authority-contract provenance,
  plus committed Git blob identity as source-drift context only; and
- synthetic or temporary test data already authorized by focused tests.

Forbidden inputs:

- raw `Player.log` or `UTC_Log` content;
- private decklists or hand-confirmation content;
- local match logs, workbook exports, SQLite databases, runtime status files,
  failed posts, generated private data, screenshots, secrets, credentials,
  tokens, webhook URLs, or environment values;
- local absolute paths in public artifacts; and
- new ARS, Refactor Scout, corpus, fixture, or private evidence runs.

No later renderer may read an input file. Existing facade-owned paths and
inputs remain unchanged and local-only.

For this packet, `no_echo` means:

- no new field, value, path, destination, console output, exception detail,
  public artifact, telemetry, or report variant may expose local/private data;
- no existing path may be exposed in a new place or at a broader scope;
- no raw input artifact or private exception payload may be included; and
- public contract, review, handoff, test, and snapshot artifacts remain
  synthetic, symbolic, or redacted.

`no_echo` does not mean suppressing or rewriting values that the current local
report already emits under its existing contract. The renderer may receive and
format already-built values such as the submitted-deck source path, card names,
evidence details, and private-hand observation counts when, and only when, they
are already present in the existing report object and output. Byte-for-byte
local report preservation is required. Redacting, removing, adding, or moving
such values is a behavior and privacy-contract change that requires a separate
issue and approval.

Fail closed if the renderer would require a direct file read, receive a new
private field, broaden exposure, add a destination, or make exact existing
local-output preservation impossible.

## Outputs And Side Effects

This Codex B pass creates only this contract.

The current runtime side effects that a later decomposition must preserve, but
that this contract does not authorize changing or executing, include:

- JSON and Markdown candidate report writes to existing local generated paths;
- inferred-review JSON and Markdown writes to existing local generated paths;
- override writes from promotion and manual confirmation;
- candidate-review state writes from deferral; and
- CLI and launcher stdout/status presentation.

A renderer-only extraction may not add, remove, redirect, rename, reorder, or
duplicate any side effect. It may not create directories, select paths, write
files, mutate report objects, or perform promotion/confirmation/deferral.

## Behavior-Preservation Invariants

A later implementation, if separately authorized, must preserve:

- exact Arena `grpId`, instance, overlay, object-source, card-name, and catalog
  identity semantics;
- parser truth ownership and candidate-report review-support status;
- all dataclass objects, fields, defaults, ordering, and import identity;
- constant values, evidence-channel weights, and ranking tie-breakers;
- submitted-deck resolution and drift behavior;
- fingerprint, card-type, color, mana, cooccurrence, count, and manual
  confirmation scoring;
- candidate ordering, limits, score margins, evidence summaries, percentages,
  status labels, and reasons;
- promotion eligibility, confirmation, deferral, and inferred-review behavior;
- JSON schema, key ordering where observed, value types, path strings, and
  encoding;
- Markdown headings, labels, row order, tables, punctuation, escaping,
  whitespace, and final-newline behavior;
- report paths, write order, overwrite behavior, and error behavior;
- `GrpIdCandidateReport.summary_line()` and
  `InferredReviewReport.summary_line()` output;
- root CLI arguments, branching, stdout, exit behavior, and facade imports;
- launcher command vectors, output parsing, status text, and error handling;
- no-new/public-echo behavior while preserving the exact existing local-only
  report fields, paths, and text; and
- all false-authority flags and non-claims in this packet.

## Error And Drift Behavior

Fail closed and route back to Codex B or Codex E if:

- the target blob is not
  `517d8061e09f2e220792062c57615a048efa460e`;
- any required candidate-row or false-authority field is absent, unknown,
  contradictory, or true;
- the primary class/final-decision pair differs from
  `mixed_governance_runtime_surface` and `review_required`;
- a proposed helper becomes public or requires a cross-repo interface;
- any public dataclass or function must move, change identity, or change
  signature;
- output text, payload shape, ordering, path, encoding, newline, or write
  behavior cannot be proven identical;
- direct CLI or launcher behavior changes or is not covered by validation;
- a circular import, stale reference, new/private exposure, public echo, raw
  exception leak, or broadened path exposure appears;
- scoring, identity, evidence loading, promotion, confirmation, deferral, or
  inferred-review construction must move to complete the first slice; or
- any code change, Codex C routing, source read, ARS/Refactor execution,
  fixture action, downstream change, or claim would require broader authority.

## Validation Required Before Any Later Implementation Routing

These are future validation boundaries only. They do not authorize Codex C.

Before any implementation routing, a separately authorized fresh scoped
evidence pass under the applicable issue #664 gate must cover this exact mixed
surface and current target commit. Codex E must review that evidence and the
packet must be updated with the current scope, commit, contract bundle, and
result. Approval/authority provenance and committed blob identity cannot satisfy
this tool-evidence gate.

Focused module validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_grp_id_candidates.py
```

Direct CLI compatibility validation must include the CLI itself, not only
module imports:

```bash
PYTHONPATH=src python3 score_grp_id_candidates.py --help
```

A later approved test plan must use synthetic/temp paths or mocks to exercise
the CLI's default scoring path and the `--confirm-grp-id`, `--defer-grp-id`,
and `--promote-singletons` paths without reading private evidence or mutating
real local artifacts.

Launcher compatibility validation must prove that
`tools/auto_launcher/manasight_launcher_auto.py` still invokes the root CLI
with the exact argument vectors above. Use focused launcher tests or a mocked
helper-command/subprocess harness; do not launch the real local app or read
private data merely to validate decomposition.

Renderer preservation validation must compare pre-change and post-change:

- JSON report payloads;
- candidate Markdown reports;
- inferred-review JSON and Markdown reports;
- summary lines;
- report paths and write order;
- dataclass identity and public imports; and
- deterministic candidate ordering and scores.

Privacy-boundary validation must use synthetic or temporary already-built
report objects containing sentinel path-like and private-derived values that
the current local report already supports. It must prove:

- the renderer performs no direct file, environment, network, or subprocess
  read;
- existing local report text is byte-for-byte unchanged;
- no new field, path, stdout/stderr text, exception detail, artifact, or
  destination exposes the sentinels; and
- public snapshots and committed evidence contain only synthetic or redacted
  values.

Repository checks for any later implementation:

```bash
python3 -m compileall -q src/mythic_edge_parser/app/grp_id_candidates.py score_grp_id_candidates.py tools/auto_launcher/manasight_launcher_auto.py
python3 -m ruff check src tests tools score_grp_id_candidates.py
python3 tools/check_agent_docs.py
git diff --check
```

Run path-scoped protected-surface, secret/private-marker, and validation
selection checks over every changed file. Run the full test suite before
integration because the facade is parser/card-identity adjacent and has direct
CLI and launcher consumers.

## Acceptance Criteria For This Contract

- The issue #727 schema extension is explicit and cannot be mistaken for a
  direct #665 governance/helper packet.
- Every required base Phase 5 envelope field is preserved or has an explicit
  versioned override, including issue #664, `target_commit`, and all three
  deferred-surface flags.
- The canonical candidate row includes every shared required field and the
  issue-specific private-input, generated-output, CLI, and launcher fields.
- `new_public_interface_needed` is `private_same_repo`, consistent with the
  possible renderer helper, while the existing facade remains public.
- `candidate_surface_class`, `candidate_surface_kind`, and `final_decision`
  form the required fail-closed pair.
- `review_required` remains the final decision.
- The renderer-only same-repo recommendation remains non-authoritative.
- #159 and #161 remain accurately classified as approval-packet and
  execution-authority-contract provenance, not tool evidence.
- Prior ARS and Refactor Scout evidence is fail-closed as absent; committed blob
  identity supports docs-only source-drift framing, while canonical evidence
  fields require fresh scoped evidence before implementation routing.
- The direct CLI and launcher invocation paths are named as consumers and
  validation requirements.
- Parser/card-identity truth, report output, lifecycle, and privacy remain
  unchanged; no-new/public-echo is enforced without suppressing or rewriting
  existing local-only report values.
- Every false-authority and non-claim flag remains false or explicitly
  non-claiming.
- Codex C, implementation, file movement, and helper creation remain blocked.

## Open Questions And Remaining Risk

- Codex E must decide whether pure Markdown and inferred-review rendering are
  small and independent enough to justify a future child, or whether the
  module should remain intact.
- A future child would need to decide whether JSON payload assembly is pure
  rendering or should remain with facade-owned path/write behavior. This
  contract does not move it.
- No implementation child should be created from this packet until Codex E
  confirms the schema, consumer inventory, and renderer-only boundary.

## Next Workflow Action

Next role: Codex E, independent contract reviewer.

Pasteable next-thread prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #727.

Review:
- https://github.com/Tahjali11/Mythic-Edge/issues/727
- docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md
- src/mythic_edge_parser/app/grp_id_candidates.py
- score_grp_id_candidates.py
- tools/auto_launcher/manasight_launcher_auto.py
- tests/test_grp_id_candidates.py
- the shared Phase 5 schema in docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md
- the #159 approval-packet and #161 execution-authority-contract provenance
  named by the contract

Re-review `GRPID-DECOMP-E-001` through `GRPID-DECOMP-E-005`. Verify the
issue-specific schema extension preserves or explicitly overrides every base
envelope field; the canonical candidate row and private same-repo interface are
coherent; the direct CLI plus launcher paths remain covered; #159/#161 are
classified only as approval/authority provenance; prior tool-evidence and
reviewed-target fields fail closed; fresh scoped evidence is required before
implementation; and no-new/public-echo is separated from exact existing local
report preservation.

Also verify `final_decision` remains `review_required`, the recommendation is
renderer-only and non-authoritative, parser/card-identity truth does not move
downstream, and every false-authority/non-claim flag remains preserved.

Do not implement code, authorize Codex C, move files, read private evidence,
run ARS or Refactor Scout, change runtime behavior, or claim readiness, truth,
security assurance, or privacy assurance. Lead with findings and route back to
Codex B if any contract ambiguity remains.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/727"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
  residual_promotion_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
  approval_packet_validation_provenance: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/159#issuecomment-4935133049"
  execution_authority_contract_provenance: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161#issuecomment-4920908510"
  actual_tool_evidence_result_ref: "none"
  completed_thread: "B_contract_revision"
  next_thread: "E_contract_review"
  verdict: "grp_id_candidate_reporting_decision_packet_revised_for_grpid_decomp_e_001_through_e_005"
  findings_addressed:
    - "GRPID-DECOMP-E-001"
    - "GRPID-DECOMP-E-002"
    - "GRPID-DECOMP-E-003"
    - "GRPID-DECOMP-E-004"
    - "GRPID-DECOMP-E-005"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/727"
  target_artifact: "docs/contracts/core_grp_id_candidate_reporting_decomposition_decision_packet.md"
  risk_tier: "high"
  base_branch: "main"
  target_branch: "main_after_review_and_explicit_approval"
  branch: "codex/grp-id-candidate-reporting-decision-packet-727"
  authority_contract_target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
  target_commit: "4b5c3d7d6ffd566858f123039db2d4bf8690e6e4"
  current_target_commit: "4b5c3d7d6ffd566858f123039db2d4bf8690e6e4"
  target_blob: "517d8061e09f2e220792062c57615a048efa460e"
  eventbus_support_deferred: true
  api_frontend_live_capture_deferred: true
  parser_state_deferred: true
  prior_ars_evidence_found: "no"
  prior_refactor_scout_evidence_found: "no"
  reviewed_repo: "none"
  reviewed_scope: "none"
  reviewed_commit: "none"
  ars_version_contract_bundle: "none"
  prior_tool_evidence_status: "absent"
  contract_framing_source_status: "committed_target_blob_lineage_only_not_tool_evidence"
  evidence_status: "fresh_scoped_evidence_required_before_implementation"
  fresh_scoped_evidence_needed: "yes"
  fresh_scoped_evidence_needed_for_contract_framing: "no"
  fresh_scoped_evidence_needed_before_implementation: "yes"
  private_input_boundary: "no_direct_file_read_no_new_or_public_echo_existing_local_report_preserved"
  final_decision: "review_required"
  recommended_first_slice: "extract_pure_report_renderers_only"
  ready_for_codex_c: false
  implementation_authorized: false
  same_repo_helper_creation_authorized: false
  file_move_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  private_evidence_read_authorized: false
  card_identity_change_authorized: false
  parser_behavior_change_authorized: false
  parser_truth_ownership_change_authorized: false
  report_schema_change_authorized: false
  report_output_change_authorized: false
  cli_behavior_change_authorized: false
  launcher_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  validation:
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
    - "path-scoped validation selection"
  stop_conditions:
    - "Do not authorize Codex C or implement code."
    - "Do not move files or create the recommended helper."
    - "Do not read private evidence or run ARS/Refactor Scout."
    - "Stop on target blob drift or any interface/output preservation ambiguity."
```
