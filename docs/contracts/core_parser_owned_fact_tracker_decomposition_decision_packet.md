# Core Parser-Owned Fact Tracker Decomposition Decision Packet

## Module

`core_parser_owned_fact_tracker_decomposition_decision_packet`

This is a contract-only Codex B decomposition decision packet for the residual
Phase 5 candidate `parser-owned-fact-tracker`.

Plain English: this packet decides whether
`src/mythic_edge_parser/app/parser_owned_fact_tracker.py` is a safe same-repo
decomposition candidate, what must be preserved, what evidence exists, and
what a later implementation role may or may not do. It does not implement code,
move files, change parser behavior, run ARS, run Refactor Scout, or claim
readiness, truth, security assurance, or privacy assurance.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: https://github.com/Tahjali11/Mythic-Edge
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/722
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Decomposition tracker: https://github.com/Tahjali11/Mythic-Edge/issues/463
- Residual promotion queue: https://github.com/Tahjali11/Mythic-Edge/issues/715
- Evidence source:
  https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161
- Candidate ID: `parser-owned-fact-tracker`
- Candidate surface:
  `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- Target artifact:
  `docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md`

## Source Artifacts Inspected

- GitHub issue #722
- GitHub issue #568
- GitHub issue #463
- GitHub issue #715
- GitHub issue #719 and PR #721 as the previous residual candidate pattern
- Automation Artifacts issue #161
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/contracts/parser_owned_fact_capture_tracker.md`
- `docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md`
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- `tests/test_parser_owned_fact_tracker.py`

No raw logs, private `Player.log` files, private evidence, raw diffs, source
repository mutations, ARS runs, or Refactor Scout runs were used by this Codex B
pass.

## Instruction Context

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "High"
  global_router_read: false
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read: []
  protected_surfaces:
    - "parser-owned fact semantics"
    - "parser truth ownership"
    - "source-label behavior"
    - "confidence and finality semantics"
    - "dropped-fact behavior"
    - "privacy/no-echo validation"
    - "lifecycle transition validation"
    - "EventBus behavior"
    - "live-capture behavior"
    - "frontend/API behavior"
    - "workbook/webhook/Apps Script behavior"
    - "SQLite behavior"
    - "CI behavior"
  authority_conflicts_found: false
  authority_conflict_notes: ""
  stop_conditions:
    - "Stop if implementation, file movement, or behavior change is requested inside issue #722."
    - "Stop if decomposition would change parser truth ownership or parser-owned fact semantics."
    - "Stop if private logs, raw Player.log files, raw diffs, or private evidence are needed."
```

## Owning Layer

Primary layer: parser evidence planning and metadata tracking.

The parser/state layer remains the truth owner for parser-managed match, game,
event, card, source-label, confidence, finality, and dropped-fact semantics.
`parser_owned_fact_tracker.py` owns only public-safe metadata tracker objects
used to describe parser-owned fact capture progress.

## Internal Project Area

Parser evidence and Phase 5 decomposition planning.

This surface is parser-truth adjacent because its vocabulary names
parser-owned facts, but it is not itself a parser truth surface. It is a
metadata-only support surface for target matrices, session ledgers, coverage
progress reports, privacy scanning, false-authority flags, and non-claim
validation.

## Truth Owner

- Parser/state and extractor code own parser truth.
- `field_recovery_matrix` owns the seed rows used by the current default target
  matrix.
- `parser_owned_fact_tracker.py` owns tracker schema validation and
  public-safe metadata summaries.
- Contracts and GitHub issues own workflow authority.
- ARS and Refactor Scout evidence, when explicitly authorized, is planning
  evidence only.

This packet does not transfer parser truth to the tracker, workbook, webhook,
Apps Script, SQLite, dashboard, analytics, AI, or ARS layers.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
field_recovery_matrix rows
  -> parser-owned fact target matrix
  -> public-safe session capture ledger
  -> public-safe coverage progress report
```

Forbidden reverse-flow:

```text
tracker report or ledger
  -/-> parser truth
  -/-> fixture promotion
  -/-> corpus status mutation
  -/-> parser behavior readiness
  -/-> pipeline activation readiness
  -/-> security/privacy/reliability assurance
```

## Files Owned By This Contract

Owned by this Codex B pass:

- `docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md`

Referenced but not changed or owned by this pass:

- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_parser_owned_fact_tracker.py`
- `docs/contracts/parser_owned_fact_capture_tracker.md`

## Authorization State

All of the following remain false for issue #722:

- `implementation_authorized: false`
- `file_move_authorized: false`
- `cross_repo_extraction_authorized: false`
- `parser_behavior_change_authorized: false`
- `parser_truth_ownership_change_authorized: false`
- `parser_owned_fact_semantics_change_authorized: false`
- `source_label_behavior_change_authorized: false`
- `confidence_behavior_change_authorized: false`
- `finality_behavior_change_authorized: false`
- `dropped_fact_behavior_change_authorized: false`
- `field_recovery_matrix_behavior_change_authorized: false`
- `target_matrix_schema_change_authorized: false`
- `session_ledger_schema_change_authorized: false`
- `coverage_report_schema_change_authorized: false`
- `privacy_no_echo_behavior_change_authorized: false`
- `lifecycle_transition_behavior_change_authorized: false`
- `eventbus_behavior_change_authorized: false`
- `live_capture_behavior_change_authorized: false`
- `frontend_behavior_change_authorized: false`
- `api_payload_change_authorized: false`
- `workbook_schema_change_authorized: false`
- `webhook_payload_change_authorized: false`
- `apps_script_behavior_change_authorized: false`
- `sqlite_behavior_change_authorized: false`
- `ci_change_authorized: false`
- `ars_run_authorized: false`
- `refactor_scout_run_authorized: false`
- `private_log_read_authorized: false`
- `raw_player_log_read_authorized: false`
- `private_evidence_read_authorized: false`
- `readiness_claimed: false`
- `reliability_readiness_claimed: false`
- `parser_truth_claimed: false`
- `security_assurance_claimed: false`
- `privacy_assurance_claimed: false`

## Observed Current Behavior

`parser_owned_fact_tracker.py` is a large metadata-only module. It currently
combines several separable concerns in one file:

- issue, contract, object, schema, status, source-kind, non-claim, and false
  flag constants;
- default target matrix construction from `field_recovery_matrix`;
- target matrix, fact row, session ledger, session entry, and coverage report
  validators;
- public-safe privacy/no-echo scanning for forbidden local paths, private
  markers, and secret-like keys;
- lifecycle transition validation for capture, candidate, review, promotion,
  fixture, and platform confirmation states;
- session ledger update behavior through `record_capture_session`;
- coverage progress report summary construction;
- copy-safe helper behavior so callers do not mutate shared seed data.

The focused test file `tests/test_parser_owned_fact_tracker.py` already treats
the current module path as the public import surface and checks constants,
builders, validators, lifecycle errors, privacy/no-echo behavior, false flags,
summary counts, and copy safety.

## Problem Statement And First Bad Values

The intended behavior is behavior-preserving same-repo decomposition planning,
not implementation.

The first bad value is treating the tracker as parser truth. The tracker may
name parser-owned facts and capture states, but it must not decide match facts,
game facts, parser source labels, confidence, finality, dropped-fact semantics,
or readiness.

The second bad value is changing validation behavior while moving helpers.
Required fields, status vocabulary, non-claims, false flags, transition errors,
privacy/no-echo error strings, and copy-safe output behavior must remain
unchanged unless a later contract explicitly authorizes a schema migration.

The third bad value is splitting high-risk logic first. Privacy scanning,
lifecycle transition validation, source-kind restrictions, and report summary
construction are coupled to public-safe behavior and should not be the first
decomposition slice.

The fourth bad value is cross-repo extraction. This candidate is parser
evidence support for Mythic Edge itself. No stable independent package boundary
or separate governance model has been proven.

## Codex E Schema And Decision Vocabulary Reconciliation

This section resolves:

- `PARSER-FACTTRACKER-DECOMP-E-001`
- `PARSER-FACTTRACKER-DECOMP-E-002`
- `PARSER-FACTTRACKER-DECOMP-E-003`

The original draft used `parser_owned_fact_metadata_tracker_surface` as the
primary `candidate_surface_class` and used a shortened decision vocabulary.
The first reconciliation then paired the shared
`mixed_governance_runtime_surface` class with
`same_repo_decomposition_candidate`. Together, those drafts created three
ambiguities:

- whether this packet was using the shared Phase 5 packet vocabulary or
  inventing an incompatible parser-specific schema;
- whether `same_repo_decomposition_candidate` was a canonical final decision,
  a recommendation, or an implementation authorization;
- whether issue #722 was overriding the shared cross-field rule that
  `mixed_governance_runtime_surface` may route only to `review_required` or
  `request_scope_split_child`.

Canonical correction:

- this packet is an issue #722 parser-evidence extension that reuses the
  shared Phase 5 packet field names, false-authority flags, ARS/Refactor
  evidence status fields, and decision vocabulary where applicable;
- the primary `candidate_surface_class` is the shared
  `mixed_governance_runtime_surface`, because this candidate is a
  parser-truth-adjacent support surface and not one of the pure
  governance/report/helper classes from the #665 lane;
- the parser-specific label `parser_owned_fact_metadata_tracker_surface` is
  moved to the secondary `candidate_surface_kind` field and must not be treated
  as a canonical Phase 5 primary class;
- `final_decision` uses `review_required`, because the candidate is already a
  single bounded surface and does not need `request_scope_split_child`;
- the proposed same-repo decomposition remains a non-authoritative
  recommendation for review and is not encoded as the packet decision;
- issue #722 defines no routing override for
  `mixed_governance_runtime_surface`; and
- no wording in this contract may treat `review_required` or the same-repo
  recommendation as `implementation_authorized`, `file_move_authorized`,
  `ready_for_codex_c`, or `ready_for_codex_f`.

## Phase 5 Packet Schema And Vocabulary Binding

Base vocabulary reused from the Phase 5 decomposition decision packet family:

- `final_decision` values:
  `same_repo_keep_current_path`, `same_repo_decomposition_candidate`,
  `request_fresh_ars_refactor_evidence`, `request_scope_split_child`,
  `reject_cross_repo_extraction`, `defer`, `unsupported`, and
  `review_required`;
- ARS/Refactor evidence fields:
  `prior_ars_evidence_found`, `prior_refactor_scout_evidence_found`,
  `reviewed_repo`, `reviewed_scope`, `reviewed_commit`,
  `ars_version_contract_bundle`, `current_target_commit`,
  `relevant_changes_since_review`, `evidence_status`,
  `fresh_scoped_evidence_needed`, and `reason`;
- false-authority fields such as `implementation_authorized`,
  `file_move_authorized`, `ars_run_authorized`,
  `refactor_scout_run_authorized`, `source_mutation_authorized`,
  `readiness_claimed`, and `truth_or_assurance_claimed`.

Cross-field routing validation narrows the base decision vocabulary for this
packet:

| `candidate_surface_class` | Permitted `final_decision` values |
| --- | --- |
| `mixed_governance_runtime_surface` | `review_required`, `request_scope_split_child` |

The `candidate_surface_kind` value does not relax or override this rule. For
issue #722, the required pair is:

```yaml
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "parser_owned_fact_metadata_tracker_surface"
final_decision: "review_required"
```

A future validator must fail closed when:

- `candidate_surface_class` is `mixed_governance_runtime_surface` and
  `final_decision` is any value other than `review_required` or
  `request_scope_split_child`;
- `candidate_surface_kind` is used to select a route that the primary class
  forbids;
- `request_scope_split_child` is selected without naming the mixed scopes that
  require separate children; or
- a caller claims an issue-scoped routing override that is not explicitly
  defined by a versioned contract and validated against an allowed class and
  decision pair.

This contract defines no issue-scoped routing override. Any unknown,
ambiguous, or conflicting class/decision pair is invalid and must remain
`review_required` without authorizing implementation or file movement.

Issue #722 extension:

```yaml
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
packet_schema: "core_parser_owned_fact_tracker_decomposition_decision_packet.v1"
schema_extension_owner: "docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md"
schema_extension_scope: "issue_722_parser_owned_fact_tracker_only"
candidate_scope: "parser_owned_fact_tracker_only"
candidate_surface_class_source: "shared_phase_5_vocabulary"
candidate_surface_kind_source: "issue_722_extension"
```

This extension adds exactly one secondary `candidate_surface_kind` value:

- `parser_owned_fact_metadata_tracker_surface`: a parser-evidence metadata
  support surface that builds or validates public-safe parser-owned fact target
  matrices, session ledgers, coverage reports, false-authority flags, and
  non-claim metadata without owning parser truth or changing parser behavior.

This value is allowed only when all of the following are true:

- `packet_schema` is
  `core_parser_owned_fact_tracker_decomposition_decision_packet.v1`;
- `schema_extension_scope` is `issue_722_parser_owned_fact_tracker_only`;
- `candidate_id` is `parser-owned-fact-tracker`;
- `current_path` is
  `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`;
- `candidate_surface_class` is `mixed_governance_runtime_surface`;
- all false-authority fields in this contract remain false.

This contract does not add
`parser_owned_fact_metadata_tracker_surface` to the #665
governance/report/helper schema, any project-wide registry, or any later Phase
5 packet by implication.

## Packet Envelope

```yaml
packet_schema: "core_parser_owned_fact_tracker_decomposition_decision_packet.v1"
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/722"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
residual_promotion_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
evidence_source: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161"
target_artifact: "docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md"
target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
current_target_commit: "9f5d929052ed7a528d8279bcd1578f6b8756eeef"
candidate_scope: "parser_owned_fact_tracker_only"
candidate_id: "parser-owned-fact-tracker"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "parser_owned_fact_metadata_tracker_surface"
current_path: "src/mythic_edge_parser/app/parser_owned_fact_tracker.py"
phase_5_order_preserved: true
final_decision: "review_required"
same_repo_first: true
implementation_authorized: false
file_move_authorized: false
cross_repo_extraction_authorized: false
parser_behavior_change_authorized: false
parser_truth_ownership_change_authorized: false
parser_owned_fact_semantics_change_authorized: false
eventbus_behavior_change_authorized: false
live_capture_behavior_change_authorized: false
frontend_behavior_change_authorized: false
api_payload_change_authorized: false
workbook_webhook_apps_script_change_authorized: false
sqlite_behavior_change_authorized: false
ci_change_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
private_log_read_authorized: false
raw_player_log_read_authorized: false
private_evidence_read_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
truth_or_assurance_claimed: false
```

## Candidate Surface Classification

Primary class:

- `mixed_governance_runtime_surface`

Primary class rationale:

This is the closest shared Phase 5 class because the candidate is a support
surface with workflow/reporting metadata behavior and parser-runtime-adjacent
protected-surface contact. It is not a pure governance/report/helper surface,
and it is not parser truth.

Issue-local secondary kind:

- `parser_owned_fact_metadata_tracker_surface`

Secondary metadata labels are descriptive only and must not be used as the
primary class or as `candidate_surface_kind`:

- `target_matrix_contact`
- `session_capture_ledger_contact`
- `coverage_progress_report_contact`
- `field_recovery_matrix_seed_contact`
- `privacy_no_echo_validation_contact`
- `lifecycle_transition_validation_contact`
- `platform_status_validation_contact`
- `false_authority_non_claim_validation_contact`

## Candidate Row

```yaml
candidate_id: "parser-owned-fact-tracker"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "parser_owned_fact_metadata_tracker_surface"
current_path: "src/mythic_edge_parser/app/parser_owned_fact_tracker.py"
current_behavior: "Builds and validates public-safe parser-owned fact target matrix, session ledger, and coverage progress metadata."
truth_or_authority_owner: "Parser/state code owns parser truth; this module owns metadata tracker schema validation only."
upstream_dependencies:
  - "src/mythic_edge_parser/app/field_recovery_matrix.py"
  - "docs/contracts/parser_owned_fact_capture_tracker.md"
downstream_consumers:
  - "tests/test_parser_owned_fact_tracker.py"
  - "future parser evidence planning workflows"
protected_surface_contact: "mixed_review_required"
proposed_destination: "same_repo_private_support_module_behind_parser_owned_fact_tracker_facade"
why_not_keep_local: "Keeping local remains valid; a constants-only split may reduce file size without changing behavior."
why_not_move_to_existing_repo: "Sibling repos do not own parser evidence metadata or parser-truth-adjacent vocabulary."
why_not_create_new_repo: "A new repo would add version skew around parser evidence metadata without a proven independent governance boundary."
new_public_interface_needed: "private_same_repo"
new_public_interface_description: "The public import path remains mythic_edge_parser.app.parser_owned_fact_tracker; any extracted module is private same-repo support."
behavior_preservation_tests:
  - "PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py"
rollback_plan: "Revert the implementation commit, restore constants to parser_owned_fact_tracker.py, remove any private support module, and do not migrate data or change runtime behavior."
ars_refactor_evidence_status: "current_matching_scope"
non_claims:
  - "not_implementation_authority"
  - "not_file_move_authority"
  - "not_parser_truth"
  - "not_parser_behavior_change"
  - "not_readiness"
  - "not_security_assurance"
  - "not_privacy_assurance"
final_decision: "review_required"
```

Forbidden primary classes for this packet:

- `parser_truth_surface`
- `raw_log_reader_surface`
- `fixture_promotion_surface`
- `corpus_mutation_surface`
- `eventbus_behavior_surface`
- `live_capture_runtime_surface`
- `frontend_behavior_surface`
- `api_payload_surface`
- `workbook_webhook_surface`
- `apps_script_surface`
- `sqlite_behavior_surface`
- `ci_enforcement_surface`
- `security_assurance_surface`
- `readiness_gate_surface`

## Decision Vocabulary

Allowed `final_decision` values:

- `same_repo_keep_current_path`: keep the candidate where it is; no move.
- `same_repo_decomposition_candidate`: later same-repo decomposition may be
  considered after Codex E review and separate implementation authorization.
- `request_fresh_ars_refactor_evidence`: current evidence is missing, stale,
  or mismatched and fresh scoped evidence is needed before implementation.
- `request_scope_split_child`: candidate mixes too much scope and needs a
  narrower child.
- `reject_cross_repo_extraction`: cross-repo extraction is not justified.
- `defer`: leave the candidate parked.
- `unsupported`: candidate is outside this packet scope.
- `review_required`: human or Codex E review must decide before routing.

The shared vocabulary list does not mean every value is valid for every
surface class. The cross-field routing rule above is authoritative for this
packet. In particular, `same_repo_decomposition_candidate` is not permitted
when `candidate_surface_class` is `mixed_governance_runtime_surface`.

Chosen value:

- `review_required`

Forbidden decision values:

- `same_repo_decomposition_authorized`
- `cross_repo_extract_now`
- `implement_now`
- `move_files_now`
- `change_parser_behavior`
- `change_parser_truth_owner`
- `activate_readiness_gate`
- `run_ars_now`
- `run_refactor_scout_now`
- `create_private_evidence_now`

## Decomposition Decision

Final decision: `review_required`

The recommended shape for review is same-repo decomposition with the existing
`parser_owned_fact_tracker.py` path preserved as the public façade. A façade is
the import surface callers already use; here, tests import
`mythic_edge_parser.app.parser_owned_fact_tracker`, so that path must keep
working.

This recommendation is not a decision to implement or move files. Codex E or
the human owner must review the packet and route any later implementation
through separate explicit authority. Until then, `ready_for_codex_c` and
`ready_for_codex_f` remain false.

Cross-repo extraction is rejected for this issue because the surface is
parser-truth adjacent, depends on Mythic Edge parser evidence vocabulary, uses
`field_recovery_matrix` as an internal seed source, and has not proven an
independent governance or versioning boundary.

Keeping the file unchanged is acceptable if a later implementer determines that
the extraction risk exceeds the readability benefit. The safe recommendation is
therefore a reversible, two-pass path:

1. First pass: move only schema/vocabulary constants into a same-repo support
   module while re-exporting them from `parser_owned_fact_tracker.py`.
2. Later pass: only after review, consider extracting pure validators or report
   summary helpers if tests prove no behavior drift.

## Recommended First Implementation Slice

Recommended first slice, if and only if a later issue authorizes Codex C:

`extract_schema_vocabulary_constants`

Possible same-repo target module:

- `src/mythic_edge_parser/app/parser_owned_fact_tracker_schema.py`

The later implementation must preserve the original public import surface:

```python
from mythic_edge_parser.app import parser_owned_fact_tracker
```

The first slice may only relocate immutable schema and vocabulary constants,
then import or re-export them from `parser_owned_fact_tracker.py`. It must not
change constant values, tuple ordering, required-field sets, regex patterns,
source-kind groupings, status vocabulary, non-claim vocabulary, false flag
names, authorization flag names, readiness flag names, or error behavior.

The first slice must not move these behaviors:

- `build_default_fact_target_matrix`
- `fact_row_from_recovery_row`
- `build_empty_session_capture_ledger`
- `record_capture_session`
- `build_coverage_progress_report`
- `validate_fact_target_matrix`
- `validate_fact_row`
- `validate_session_capture_ledger`
- `validate_session_entry`
- `validate_coverage_progress_report`
- privacy/no-echo scanning helpers
- lifecycle transition validation helpers
- platform confirmation validation helpers
- report summary helpers

## Public Interface To Preserve

Public class:

- `ParserOwnedFactTrackerError`

Public builder and validator functions:

- `build_default_fact_target_matrix(...)`
- `fact_row_from_recovery_row(row)`
- `build_empty_session_capture_ledger(...)`
- `record_capture_session(matrix, ledger, session_record)`
- `build_coverage_progress_report(matrix, ledger, previous_report=None, ...)`
- `validate_fact_target_matrix(matrix)`
- `validate_fact_row(fact)`
- `validate_session_capture_ledger(ledger)`
- `validate_session_entry(session, matrix=None, ledger=None)`
- `validate_coverage_progress_report(report)`

Public constants currently imported by tests and possible downstream code must
remain reachable from `parser_owned_fact_tracker.py`, including but not limited
to:

- `SOURCE_ISSUE`
- `PIPELINE_TRACKER`
- `PARENT_PRIVATE_EVIDENCE_ISSUE`
- `CONTRACT_PATH`
- object and schema version constants
- `TARGET_MATRIX_STATUSES`
- `FACT_FAMILIES`
- `LIFECYCLE_STATUSES`
- `PLATFORM_STATUSES`
- `SOURCE_KINDS`
- `PRIVATE_SOURCE_KINDS`
- `SYNTHETIC_SOURCE_KINDS`
- `READINESS_FLAG_FIELDS`
- `AUTHORIZATION_FLAG_FIELDS`
- `FALSE_FLAG_FIELDS`
- `REQUIRED_NON_CLAIMS`
- `ALLOWED_TRANSITIONS`
- `SIDE_TRANSITIONS`
- required-field tuples

## Inputs

Allowed inputs for a later implementation test or refactor pass:

- committed source files in the current Mythic Edge checkout;
- `field_recovery_matrix` rows already present in the repo;
- synthetic or public-safe test objects in `tests/test_parser_owned_fact_tracker.py`;
- issue and contract metadata already public in GitHub or committed docs.

Forbidden inputs:

- raw `Player.log` or `UTC_Log` files;
- private logs or private evidence;
- raw diffs from source repositories;
- local private paths;
- workbook exports;
- SQLite databases;
- provider outputs;
- OpenAI/model outputs;
- ARS or Refactor Scout output unless separately authorized by a later exact
  issue and owner approval.

## Outputs

This Codex B pass outputs only this contract artifact.

A later implementation, if separately authorized, may output code changes only
inside Mythic Edge and must preserve the public interface. It may not create
runtime artifacts, private evidence, candidate dossiers, inventory packages,
fixtures, corpus metadata, source-repo actions, or CI changes.

## Evidence Status

Evidence source #161 is accepted only as scoped planning evidence for this
candidate. It is not implementation authority, file-move authority, ARS run
authority, Refactor Scout run authority, private evidence authority, or
readiness evidence.

Current public issue #722 records that:

- the evidence action covered only the named residual batch candidates;
- target repository was `Tahjali11/Mythic-Edge`;
- target commit was `9528bb3bee9c1d241268cb8a7d1a806b118471de`;
- current `origin/main` was refreshed after PR #721;
- the candidate target file was unchanged between the target commit and current
  `origin/main` at inspection time;
- durable artifacts, candidate dossiers, source-repo actions, scheduling,
  readiness claims, and truth claims remained unauthorized.

If a later implementer finds that the target file changed after this contract,
the implementer must stop and request fresh scoped evidence or owner acceptance
before proceeding.

```yaml
prior_ars_evidence_found: "yes"
prior_refactor_scout_evidence_found: "yes"
reviewed_repo: "Tahjali11/Mythic-Edge"
reviewed_scope: "src/mythic_edge_parser/app/parser_owned_fact_tracker.py"
reviewed_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
ars_version_contract_bundle: "residual_phase_5_batch1_exact_scoped_evidence_execution_authority_contract.v1"
current_target_commit: "9f5d929052ed7a528d8279bcd1578f6b8756eeef"
relevant_changes_since_review: "none_known"
evidence_status: "current_matching_scope"
fresh_scoped_evidence_needed: "no"
reason: "Issue #161 is accepted as no-write scoped planning evidence for parser-owned-fact-tracker at the target commit, and issue #722/local inspection record that the target path did not change through the current origin/main used for this packet. This evidence does not authorize implementation, file movement, ARS runs, Refactor Scout runs, source inspection, private evidence reads, or truth/readiness/assurance claims."
```

## Behavior Preservation Requirements

A later implementation must preserve:

- public module path and imports;
- all public functions, class names, constants, and signatures;
- target matrix object shape and schema version;
- session ledger object shape and schema version;
- coverage progress report object shape and schema version;
- field recovery seed behavior;
- source-kind and private/synthetic source-kind boundaries;
- lifecycle transition rules;
- platform status and cross-platform confirmation rules;
- required reference checks for lifecycle statuses;
- required false readiness and authorization flags;
- required non-claims;
- privacy/no-echo rejection behavior;
- public-safe error category strings;
- copy-safe output behavior;
- existing focused tests and expected outputs.

## Forbidden Behavior Changes

A later implementation must not:

- reinterpret parser-owned facts;
- change parser source-label, confidence, finality, or dropped-fact semantics;
- change parser behavior or parser truth ownership;
- change raw-log ingestion, harvest, replay, fixture promotion, or corpus
  status behavior;
- change EventBus, live-capture, frontend, API, workbook, webhook, Apps Script,
  SQLite, or CI behavior;
- change artifact schemas, status vocabulary, false flags, non-claims, or error
  codes as part of a pure decomposition;
- convert tracker summaries into readiness, reliability, release, deploy, or
  production signals;
- create or read private evidence.

## Error Behavior

Any later implementation must fail closed when:

- a public constant disappears from `parser_owned_fact_tracker.py`;
- a builder or validator signature changes;
- any required false flag can become true;
- non-claim vocabulary is missing or renamed;
- privacy scanner output echoes a forbidden value;
- lifecycle transitions accept a forbidden skip;
- private source kinds can produce public review states without a private or
  blocked delta;
- cross-platform confirmation can pass without required platform states;
- copy-safe builders share mutable seed state;
- a new module import creates a circular import or stale reference.

Fail closed means the later role must stop, record the mismatch, and route to
Codex B or Codex E instead of patching behavior opportunistically.

## Validation Plan For A Later Implementation

Focused validation required for the first implementation slice:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
python3 -m compileall -q src/mythic_edge_parser/app/parser_owned_fact_tracker.py
```

If a new support module is added, include it in compile validation:

```bash
python3 -m compileall -q src/mythic_edge_parser/app/parser_owned_fact_tracker.py src/mythic_edge_parser/app/parser_owned_fact_tracker_schema.py
```

Recommended public-interface smoke check:

```bash
PYTHONPATH=src python3 - <<'PY'
from mythic_edge_parser.app import parser_owned_fact_tracker as tracker

matrix = tracker.build_default_fact_target_matrix()
ledger = tracker.build_empty_session_capture_ledger()
report = tracker.build_coverage_progress_report(matrix, ledger)

assert tracker.validate_fact_target_matrix(matrix) == []
assert tracker.validate_session_capture_ledger(ledger) == []
assert tracker.validate_coverage_progress_report(report) == []
assert matrix["readiness_flags"]["parser_behavior_ready"] is False
assert report["summary_counts"]["parser_behavior_ready_fact_count"] == 0
PY
```

Broader validation only if the implementation touches imports used by adjacent
evidence modules:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_field_recovery_matrix.py
```

These commands are validation expectations for a future Codex C pass. They do
not authorize implementation in issue #722.

## Acceptance Criteria

- This contract exists at the target artifact path.
- The contract names the parser evidence metadata layer and parser truth
  boundary.
- The contract references evidence source #161 without treating it as
  implementation authority.
- The contract classifies the candidate with a shared primary
  `candidate_surface_class`, keeps issue-local `candidate_surface_kind`
  secondary, and keeps contact labels non-authoritative.
- The `mixed_governance_runtime_surface` and `review_required` pair satisfies
  the shared Phase 5 cross-field routing rule, and invalid pairs fail closed.
- The contract recommends same-repo decomposition first and rejects immediate
  cross-repo extraction.
- The contract identifies the smallest safe first slice.
- The contract preserves all protected parser-owned fact, source-label,
  confidence, finality, dropped-fact, privacy/no-echo, lifecycle, and false
  authority boundaries.
- The contract defines validation expectations for a later implementation.
- The contract contains explicit non-claims and a workflow handoff.

## Open Questions And Contract Risks

- The exact support-module filename should be chosen by a later Codex C pass
  after checking current import style and avoiding circular imports.
- If any downstream code imports constants by object identity rather than value,
  the later implementation must preserve the import façade and run focused
  tests before proceeding.
- If current `origin/main` changes this candidate file after this packet, fresh
  scoped evidence or owner acceptance is required before implementation.

## Next Workflow Action

Next role: Codex E contract review.

Pasteable next-role prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic-Edge issue #722.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/722

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Evidence source:
https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161

Contract artifact:
docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md

Review the contract-only decomposition decision packet for
src/mythic_edge_parser/app/parser_owned_fact_tracker.py. Verify that it uses the
shared Phase 5 packet vocabulary with `candidate_surface_class:
mixed_governance_runtime_surface`, keeps the parser-specific
`parser_owned_fact_metadata_tracker_surface` label only as
`candidate_surface_kind`, pairs that class with `final_decision:
review_required` under the shared cross-field rule, treats the same-repo shape
only as a recommendation, uses canonical ARS/Refactor evidence fields,
preserves parser truth ownership and parser-owned fact semantics, references
#161 only as scoped planning evidence, and does not authorize implementation,
file movement, ARS/Refactor runs, private log reads, parser behavior changes,
source-label, confidence, finality, dropped-fact, EventBus, live-capture,
frontend/API, workbook/webhook/Apps Script/SQLite/CI changes, or
readiness/truth/assurance claims.

Expected output:
- Findings first, ordered by severity.
- Whether the contract is ready for a later scoped Codex C implementation issue
  or needs Codex B clarification.
- Validation evidence reviewed.
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/722"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  residual_promotion_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
  evidence_source: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161"
  completed_thread: "B"
  next_thread: "E"
  verdict: "parser_owned_fact_tracker_cross_field_routing_fixed_ready_for_contract_review"
  finding_ids_fixed:
    - "PARSER-FACTTRACKER-DECOMP-E-001"
    - "PARSER-FACTTRACKER-DECOMP-E-002"
    - "PARSER-FACTTRACKER-DECOMP-E-003"
  target_artifact: "docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md"
  candidate_id: "parser-owned-fact-tracker"
  candidate_surface: "src/mythic_edge_parser/app/parser_owned_fact_tracker.py"
  candidate_surface_class: "mixed_governance_runtime_surface"
  candidate_surface_kind: "parser_owned_fact_metadata_tracker_surface"
  final_decision: "review_required"
  recommended_first_slice: "extract_schema_vocabulary_constants"
  ready_for_codex_c: false
  ready_for_codex_f: false
  risk_tier: "High"
  implementation_authorized: false
  file_move_authorized: false
  cross_repo_extraction_authorized: false
  parser_behavior_change_authorized: false
  parser_truth_ownership_change_authorized: false
  parser_owned_fact_semantics_change_authorized: false
  source_label_behavior_change_authorized: false
  confidence_behavior_change_authorized: false
  finality_behavior_change_authorized: false
  dropped_fact_behavior_change_authorized: false
  eventbus_behavior_change_authorized: false
  live_capture_behavior_change_authorized: false
  frontend_behavior_change_authorized: false
  api_payload_change_authorized: false
  workbook_webhook_apps_script_change_authorized: false
  sqlite_behavior_change_authorized: false
  ci_change_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  private_log_read_authorized: false
  raw_player_log_read_authorized: false
  private_evidence_read_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
