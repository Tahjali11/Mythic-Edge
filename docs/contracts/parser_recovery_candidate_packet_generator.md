# Parser Recovery Candidate Packet Generator Contract

## Module

Recovery candidate packet generator for parser drift recovery planning.

Plain English: this contract defines how a future helper may assemble
deterministic, public-safe, in-memory review packets from Field Recovery Matrix
rows, automated field-evidence comparison rows, reduced evidence summaries, and
optional sanitized symbolic offset-window metadata. The packets may help a
reviewer understand whether a field has a possible recovery path, but they
must not write artifacts, read private logs, promote fixtures, move corpus
statuses, restore parser fields, activate #388 or #381, or claim readiness.

This Codex B pass writes only this contract. It does not implement code, open a
PR, run private checks, create packet files, create fixture-promotion files,
edit corpus metadata, change parser behavior, or claim parser recovery.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/454
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/453
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/540
- Previous merge commit: `507952919718b729556bdd3a544ff14ce48f08a0`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- Local `main` and `origin/main` were both
  `c4b0776855c599ec2a6130b226740f36bb67071f`.
- PR #540 was merged at
  `507952919718b729556bdd3a544ff14ce48f08a0`, and that merge commit is an
  ancestor of current `main`.
- Issue #454 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- Open PRs #391 and #374 were present but not selected by this lane. This
  contract treats the user-supplied #454 prompt as the active planning lane
  and preserves the stop condition that a stricter WIP-1 interpretation should
  stop before implementation.

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- Issue #454 and Codex A reconciliation comment
- Issue #453 and PR #540
- Pipeline tracker #388
- Parent private-evidence issue #434
- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`
- `docs/contracts/parser_recovery_field_evidence_comparison_report.md`
- `docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md`
- `docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md`
- `docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `src/mythic_edge_parser/app/field_evidence_comparison_report.py`
- `tests/test_field_recovery_matrix.py`
- `tests/test_local_watcher_offset_window_monitor.py`
- `tests/test_field_evidence_comparison_report.py`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`

No private Player.log, UTC_Log, app-data, live MTGA, network,
firewall/drop, packet, OS/router, diagnostics, drift, watcher, tailer, or
private smoke evidence was run, tailed, hashed, copied, summarized, or read.

## Observed Current Behavior

Issue #451 added a report-only Field Recovery Matrix helper:

- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`

The matrix provides deterministic field rows with:

- field IDs and field families;
- evidence-ledger entry IDs;
- required direct evidence;
- allowed and forbidden fallback evidence;
- recovery categories;
- parser and analytics output policies;
- confidence, finality, degradation, stale-source, review, restoration, and
  non-claim metadata;
- false readiness and authorization flags.

Issue #452 added a synthetic-only local watcher / offset-window metadata
helper:

- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `tests/test_local_watcher_offset_window_monitor.py`

The offset-window helper uses symbolic source/window labels and synthetic or
public-fixture metadata only. It blocks non-synthetic local sources without
approval and does not read private source contents, return local paths, write
offset state, call `FileTailer`, start a watcher, or prove watcher
correctness.

Issue #453 added a deterministic field-evidence comparison report:

- `src/mythic_edge_parser/app/field_evidence_comparison_report.py`
- `tests/test_field_evidence_comparison_report.py`

The comparison report compares Field Recovery Matrix rows against reduced
current field-evidence summaries and optional sanitized watcher context. It is
in-memory, report-only, and side-effect-free. It preserves all readiness and
authorization flags as false and fails closed when caller inputs include
privacy markers, local absolute paths, raw payload keys, true readiness or
authorization claims, or protected-surface claims.

No dedicated recovery candidate packet generator contract, helper, test, or
packet artifact existed before this contract.

Current #388 and #454 state preserves:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
file_writing_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
```

In this contract, `file_writing_authorized: false` means the future helper
must not write recovery packet files, fixture-promotion packets, proof files,
metadata diffs, local artifacts, fixtures, manifests, or corpus metadata. The
only write authorized in this Codex B pass is this docs contract.

## Problem

After the Field Recovery Matrix, symbolic offset-window monitor, and
field-evidence comparison report, Mythic Edge needs a narrow review packet
shape that can summarize possible recovery candidates without forcing
reviewers to inspect raw event payloads or private evidence.

Without a contract, a future candidate packet generator could accidentally:

- treat a candidate packet as parser restoration authority;
- treat approximate, degraded, stale, blocked, or review-required evidence as
  parser truth;
- treat symbolic offset-window metadata as proof of source completeness or
  watcher correctness;
- copy raw private paths, offsets, file sizes, timestamps, hashes, raw payload
  values, or private snippets into committed output;
- write local or committed packet artifacts without an explicit file-writing
  contract;
- promote fixture drafts, corpus statuses, #388, #381, private harvest, or
  parser behavior readiness;
- let workbook formulas, Apps Script, analytics, AI, coaching, local app
  reports, or review summaries own parser recovery truth.

The first bad value is any recovery candidate packet, reviewer-decision field,
status, summary, or next-step hint that causes parser behavior, fixtures,
corpus metadata, private harvest, field recovery, or readiness flags to move
forward without a separate scoped contract, implementation, validation, review,
and approved workflow step.

## Scope Decision

This contract defines a planning-only, in-memory packet schema and validation
boundary.

Implementation is not authorized by this Codex B pass. If the user later
explicitly authorizes Codex C implementation, Codex C may add a deterministic,
side-effect-free Python helper and focused tests that build recovery candidate
packet reports in memory from:

1. Field Recovery Matrix rows;
2. field-evidence comparison report rows;
3. reduced evidence summaries that already passed #453 validation; and
4. optional sanitized symbolic offset-window metadata that already passed #452
   validation.

The future helper must not write packet files or local artifacts. A later
artifact-writer, PR-assist, fixture-promotion, corpus metadata, diagnostics,
drift, golden replay, local app, or private-evidence integration requires its
own issue and contract.

This contract does not authorize:

- code implementation in Codex B;
- private source discovery;
- private source reads;
- exact private offset, size, timestamp, path, or hash collection;
- watcher startup;
- tailer startup;
- diagnostics or drift execution;
- local or committed packet writing;
- proof file writing;
- metadata diff writing;
- fixture creation or promotion;
- golden replay manifest writing;
- corpus status changes;
- parser behavior changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`;
- `file_writing_authorized=true`;
- `private_harvest_authorized=true`;
- `fixture_promotion_authorized=true`;
- `corpus_status_change_authorized=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Quality / Governance support.

Corpus / Provenance owns the candidate packet vocabulary, review packet
schema, expected input dependency policy, public-safe evidence summary rules,
and candidate status semantics.

Quality / Governance owns workflow routing, protected-surface assertions,
secret/private-marker validation, WIP-1 stop behavior, role boundaries,
validation expectations, and non-claim enforcement.

Parser remains the owner of parser facts, parser behavior, parser events,
router semantics, parser state final reconciliation, match/game identity,
deduplication, and normalized output values.

Generated / Local Artifacts owns any future local-only private evidence,
offset state, packet exports, proof files, fixture drafts, or private review
outputs only if a later explicit issue and contract authorize them.

Analytics, workbook/transport, Apps Script, local app, AI, and coaching
surfaces are consumers only. They must not own recovery candidate truth or
parser recovery truth.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Quality / Governance, for workflow safety and validation.
- Parser, for parser-owned field identity and output-policy boundaries.
- Generated / Local Artifacts, for future local-only review outputs if
  separately approved.

This contract is not a parser behavior contract, not a private-evidence
execution contract, not a fixture-promotion contract, not a diagnostics or
drift contract, not a local app contract, not a workbook or transport
contract, not an analytics contract, not an AI/coaching contract, not a CI
gate, and not a release/deploy/production readiness gate.

## Truth Owner

Truth owner for parser values remains the existing parser, router, event,
state, model, extractor, match/game identity, deduplication, and final
reconciliation layers.

Truth owner for expected field recovery categories and output policies remains:

- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`

Truth owner for local watcher / offset-window metadata remains:

- `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `tests/test_local_watcher_offset_window_monitor.py`

Truth owner for comparison row status and candidate recovery hints remains:

- `docs/contracts/parser_recovery_field_evidence_comparison_report.md`
- `src/mythic_edge_parser/app/field_evidence_comparison_report.py`
- `tests/test_field_evidence_comparison_report.py`

This contract owns only the recovery candidate packet schema, candidate status
vocabulary, reviewer decision scaffold, fail-closed packet validation rules,
and public-safe packet non-claims. It does not own parser facts, private
evidence, fixture expected output, corpus status, analytics truth, AI truth,
coaching truth, readiness, or tracker completion.

## Bridge-Code Status

`deferred_future_boundary`

This Codex B pass authorizes no bridge code.

If later implemented, the helper may become shared support from Corpus /
Provenance to Quality / Governance and future parser recovery review
workflows.

Allowed future data flow:

```text
Field Recovery Matrix rows
  + field-evidence comparison report rows
  + reduced public-safe evidence summaries
  + optional sanitized symbolic offset-window metadata
  -> in-memory recovery candidate packet report
  -> human/Codex review
  -> later scoped issue, if separately authorized
```

Forbidden reverse flow:

```text
recovery candidate packet report
  -/-> parser value overwrite
  -/-> parser event or router behavior change
  -/-> parser state final reconciliation change
  -/-> workbook formula reconstruction
  -/-> webhook or Apps Script payload change
  -/-> diagnostics, drift, or runtime status integration
  -/-> analytics / AI / coaching truth
  -/-> fixture promotion
  -/-> corpus status promotion
  -/-> private harvest authorization
  -/-> packet file writing
  -/-> #388 or #381 activation
```

## Files Owned By This Contract

This contract owns:

- `docs/contracts/parser_recovery_candidate_packet_generator.md`

If implementation later receives explicit user authorization, Codex C may add
or update only:

- `src/mythic_edge_parser/app/recovery_candidate_packet_generator.py`
- `tests/test_recovery_candidate_packet_generator.py`
- `docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md`

If Codex E later reviews an implementation, it may add:

- `docs/contract_test_reports/parser_recovery_candidate_packet_generator.md`

Read-only references for later Codex C:

- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `src/mythic_edge_parser/app/field_evidence_comparison_report.py`
- `tests/test_field_recovery_matrix.py`
- `tests/test_local_watcher_offset_window_monitor.py`
- `tests/test_field_evidence_comparison_report.py`
- #454, #388, #434, #453, PR #540

Not owned by this contract:

- parser modules;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- match/game identity or deduplication;
- diagnostics, drift, golden replay, feature-equity, evidence-ledger,
  workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, merge, deploy, release, production, or tracker lifecycle
  behavior;
- GitHub issue body edits;
- scheduled or manual private evidence execution;
- raw/private/generated/runtime artifacts.

## Public Interface

This contract defines a future in-memory helper interface only. The interface
must not be implemented until explicitly authorized by a later user prompt or
workflow artifact.

Recommended constants:

```python
RECOVERY_CANDIDATE_PACKET_REPORT_OBJECT = (
    "mythic_edge_parser_recovery_candidate_packet_report"
)
RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION = (
    "parser_recovery_candidate_packet_generator.v1"
)
RECOVERY_CANDIDATE_PACKET_OBJECT = (
    "mythic_edge_parser_recovery_candidate_packet"
)
RECOVERY_CANDIDATE_REVIEW_DECISION_OBJECT = (
    "mythic_edge_parser_recovery_candidate_review_decision"
)
```

Recommended future helper functions:

```python
build_recovery_candidate_packet_report(...)
build_recovery_candidate_packet(...)
validate_recovery_candidate_packet_report(...)
validate_recovery_candidate_packet(...)
validate_recovery_candidate_review_decision(...)
```

No CLI, environment variable, runtime service, diagnostics section, drift
report section, runtime status field, workbook column, webhook payload, Apps
Script surface, corpus metadata field, fixture schema, golden replay manifest,
or parser event is authorized by this interface.

### Packet Report Shape

A report is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_candidate_packet_report` |
| `schema_version` | yes | `parser_recovery_candidate_packet_generator.v1` |
| `source_issue` | yes | Issue #454 URL |
| `pipeline_tracker` | yes | Tracker #388 URL |
| `parent_private_evidence_issue` | yes | Parent #434 URL |
| `status` | yes | Report status vocabulary below |
| `status_reasons` | yes | Symbolic reason codes only |
| `field_recovery_matrix_schema_version` | yes | Source matrix schema version |
| `field_evidence_comparison_schema_version` | yes | Source comparison schema version |
| `watcher_context_schema_version` | yes | Source watcher schema version or `not_applicable` |
| `parser_behavior_ready` | yes | Always `false` |
| `pipeline_activation_ready_for_issue_388` | yes | Always `false` |
| `file_writing_authorized` | yes | Always `false` |
| `private_harvest_authorized` | yes | Always `false` |
| `fixture_promotion_authorized` | yes | Always `false` |
| `corpus_status_change_authorized` | yes | Always `false` |
| `field_recovery_ready` | yes | Always `false` |
| `packets` | yes | List of recovery candidate packets |
| `summary` | yes | Counts by status/category; never a readiness metric |
| `privacy` | yes | False assertions and symbolic privacy status |
| `protected_surface_assertions` | yes | All protected-surface booleans false |
| `limitations` | yes | Non-authority notes |
| `non_claims` | yes | Required non-claim vocabulary |

Allowed report statuses:

- `candidate_packets_ready`
- `empty`
- `review_required`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `invalid_input`
- `fail_closed`

`candidate_packets_ready` means only that public-safe in-memory packets were
constructed for review. It is not field recovery readiness, fixture promotion
readiness, parser behavior readiness, private harvest authorization, #388
activation readiness, release readiness, or production behavior.

### Packet Shape

A packet is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_candidate_packet` |
| `schema_version` | yes | `parser_recovery_candidate_packet_generator.v1` |
| `packet_id` | yes | Deterministic symbolic ID from public-safe fields only |
| `field_id` | yes | Matrix/comparison field ID |
| `display_name` | yes | Public-safe display label |
| `field_family` | yes | Matrix field family |
| `candidate_status` | yes | Candidate status vocabulary below |
| `candidate_category` | yes | Candidate category vocabulary below |
| `candidate_summary` | yes | Short symbolic prose with no raw evidence values |
| `field_recovery_matrix_ref` | yes | Public-safe matrix row reference |
| `comparison_row_ref` | yes | Public-safe comparison row reference |
| `expected_evidence_summary` | yes | Expected evidence, copied from #453 row |
| `current_evidence_summary` | yes | Current reduced evidence, copied from #453 row |
| `evidence_delta` | yes | Symbolic expected/current difference |
| `source_evidence_refs` | yes | Symbolic source refs only |
| `offset_window_refs` | yes | Symbolic window refs only |
| `confidence` | yes | From comparison row; never raised by packet |
| `finality` | yes | From comparison row; never raised by packet |
| `degradation_flags` | yes | Union of comparison and packet degradation flags |
| `comparison_status` | yes | Source comparison status |
| `candidate_recovery_hints` | yes | Source #453 hints plus packet-safe hints |
| `stop_reasons` | yes | Symbolic stop reasons |
| `privacy_status` | yes | Packet privacy status vocabulary below |
| `reviewer_decision` | yes | Initial review decision scaffold |
| `review_required` | yes | Boolean |
| `next_role_hint` | yes | `review_only`, `codex_a_problem_representation`, `blocked`, etc. |
| `non_claims` | yes | Required non-claim vocabulary |

Packet IDs must be deterministic and must use only:

- `schema_version`;
- `field_id`;
- `comparison_status`;
- `candidate_category`;
- `candidate_status`;
- symbolic source/window refs;
- public issue URLs;
- public schema versions.

Packet IDs must not include:

- raw field values;
- local paths;
- private offsets;
- private file sizes;
- timestamps from private sources;
- hashes;
- raw event payloads;
- decklists, card choices, or strategy notes;
- secrets or credentials.

### Candidate Status Vocabulary

Allowed `candidate_status` values:

- `candidate_ready_for_review`
- `review_required`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `blocked_unsupported_claim`
- `blocked_privacy`
- `blocked_authorization`
- `not_a_candidate`
- `stale_input`
- `conflict`
- `invalid_input`

Status rules:

- `direct` comparison rows may become `candidate_ready_for_review` only when
  the parser output policy is `preserve_existing_parser_behavior`, confidence
  is not raised, no privacy/degraded/stale/conflict flags are present, and
  the packet makes no new parser claim.
- `equivalent` and `derived_bounded` rows must be `review_required` unless
  blocked by another rule.
- `approximate_analytics_only` rows must be `review_required` or
  `not_a_candidate`; they must never imply parser restoration.
- `unavailable` rows must be `not_a_candidate` or `review_required`.
- `blocked_private_evidence` rows must remain `blocked_private_evidence`
  until a separate #434-approved private-evidence workflow exists.
- `blocked_external_boundary` rows must remain
  `blocked_external_boundary` until a separate external-boundary issue
  resolves the evidence gap.
- `stale`, `degraded`, `conflict`, `invalid_input`, and unknown statuses must
  route to review or fail closed.

### Candidate Category Vocabulary

Allowed `candidate_category` values:

- `direct_preservation_candidate`
- `equivalent_mapping_candidate`
- `derived_bounded_candidate`
- `approximate_review_candidate`
- `analytics_display_only_candidate`
- `blocked_private_candidate`
- `blocked_external_candidate`
- `unavailable_no_candidate`
- `conflict_review_candidate`
- `stale_evidence_review_candidate`
- `unsupported_claim_blocked`

Candidate categories are labels for review only. They do not authorize parser
restoration, fixture promotion, corpus status movement, private harvest, file
writing, or #388/#381 activation.

### Reviewer Decision Scaffold

Every packet must include a reviewer decision object:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_candidate_review_decision` |
| `decision` | yes | Initial value must be `undecided` |
| `decision_reason` | yes | Symbolic reason or `not_reviewed` |
| `allowed_next_step` | yes | Symbolic next-step value |
| `requires_new_issue` | yes | Boolean |
| `requires_private_evidence_approval` | yes | Boolean |
| `requires_parser_contract` | yes | Boolean |
| `requires_fixture_promotion_contract` | yes | Boolean |
| `requires_corpus_status_contract` | yes | Boolean |
| `non_claims` | yes | Required non-claims |

Allowed reviewer `decision` values:

- `undecided`
- `accept_for_later_problem_representation`
- `reject_no_recovery_path`
- `needs_private_evidence_approval`
- `needs_external_boundary_issue`
- `needs_matrix_update_contract`
- `needs_parser_contract`
- `needs_fixture_promotion_contract`
- `needs_corpus_status_contract`
- `defer`
- `blocked`

The decision scaffold is not an automated decision engine. It must not write
issues, create branches, open PRs, edit trackers, stage files, promote
fixtures, or close work.

### Privacy Status Vocabulary

Allowed `privacy_status` values:

- `public_safe`
- `symbolic_only`
- `redacted`
- `review_required`
- `blocked_private_marker`
- `blocked_exact_path`
- `blocked_exact_offset`
- `blocked_exact_size`
- `blocked_exact_timestamp`
- `blocked_raw_hash`
- `blocked_raw_payload`
- `blocked_secret_marker`
- `blocked_local_artifact`

Any blocked privacy status must force report status `fail_closed` or packet
status `blocked_privacy`. Returned errors must be symbolic and must not echo
submitted private values.

### Non-Claim Vocabulary

Required non-claims:

- `not_parser_truth`
- `not_field_recovery_readiness`
- `not_private_harvest_authorization`
- `not_fixture_promotion`
- `not_corpus_status_change`
- `not_parser_behavior_readiness`
- `not_pipeline_activation_readiness`
- `not_file_writing_authorization`
- `not_watcher_correctness`
- `not_private_smoke_success`
- `not_merge_readiness`
- `not_deploy_readiness`
- `not_release_readiness`
- `not_production_behavior`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`

The generator must preserve these non-claims on the report, every packet, and
every reviewer decision object.

## Inputs

### Field Recovery Matrix Rows

Accepted source:

- `field_recovery_matrix.build_field_recovery_matrix()`, or
- an already validated matrix object from
  `validate_field_recovery_matrix(...)`.

Required fields are those defined by
`docs/contracts/parser_recovery_field_recovery_matrix.md`.

The packet generator may read:

- `field_id`
- `display_name`
- `field_family`
- `output_surfaces`
- `evidence_ledger_entry_ids`
- `required_direct_evidence`
- `allowed_fallback_evidence`
- `forbidden_fallback_evidence`
- `recovery_category`
- `parser_output_policy`
- `analytics_output_policy`
- `minimum_confidence`
- `allowed_finality`
- `degradation_flags`
- `stale_source_behavior`
- `review_required`
- `restoration_requirements`
- `non_claims`

The packet generator must not treat restoration requirements as authorization.
They are explanatory checklist items only.

### Field-Evidence Comparison Report Rows

Accepted source:

- `field_evidence_comparison_report.build_field_evidence_comparison_report(...)`,
  or
- rows already validated by
  `validate_field_evidence_comparison_row(...)`.

The packet generator may read:

- `field_id`
- `display_name`
- `field_family`
- `expected_evidence`
- `current_evidence`
- `recovery_category`
- `parser_output_policy`
- `analytics_output_policy`
- `comparison_status`
- `confidence`
- `finality`
- `degradation_flags`
- `stale_source_status`
- `watcher_window_status`
- `candidate_recovery_hints`
- `review_required`
- `stop_reasons`
- `non_claims`

The packet generator must not raise confidence or finality above the comparison
row's value.

### Reduced Evidence Summaries

Optional reduced evidence summaries may be supplied only if they are already
public-safe and contain symbolic metadata. Allowed fields:

- `field_id`
- `evidence_ledger_entry_ids`
- `observed_signal_ids`
- `source_event_families`
- `source_event_kinds`
- `value_source`
- `confidence`
- `finality`
- `degradation_flags`
- `invariant_status`
- `stale_source_status`
- `source_window_refs`
- `review_required`
- false privacy/content flags from #453

Forbidden reduced evidence fields are listed under Forbidden Inputs.

### Symbolic Offset-Window Metadata

Optional offset-window metadata may be supplied only when it is:

- generated by the #452 helper or shaped exactly like its validated output;
- symbolic-only;
- synthetic, public-fixture, or explicitly represented as blocked/review-only;
- free of exact private paths, offsets, sizes, timestamps, hashes, raw content,
  and private source identifiers.

Allowed offset-window fields:

- `window_id`
- `source_label`
- `source_class`
- `privacy_class`
- `window_mode`
- `window_status`
- `start_marker_status`
- `end_marker_status`
- `offset_range_status`
- `source_transition_status`
- `source_generation_status`
- `stale_window_status`
- `buffer_status`
- `backpressure_status`
- `error_status`
- `review_required`
- `non_claims`

For private or local-only windows, the packet generator may include only
symbolic labels and status categories. It must not include synthetic offset or
size fields unless the source is synthetic/public-fixture and already
validated by #452.

### Context

Optional context may include:

- `source_issue`: Issue #454 URL;
- `pipeline_tracker`: Tracker #388 URL;
- `parent_private_evidence_issue`: Parent #434 URL;
- `previous_issue`: Issue #453 URL;
- `previous_pr`: PR #540 URL;
- public schema versions;
- symbolic run labels;
- all readiness and authorization flags set to `false`;
- protected-surface assertions set to `false`.

If context tries to set any readiness, authorization, protected-surface,
private-harvest, file-writing, fixture-promotion, corpus-status, parser,
runtime, workbook, analytics, AI, coaching, merge, deploy, release, or
production claim to true, the generator must fail closed.

## Forbidden Inputs

The packet generator must reject or fail closed on:

- raw Player.log content;
- raw UTC_Log content;
- MTGA app-data contents;
- live MTGA data;
- private diagnostics, drift, watcher, tailer, network, firewall/drop, packet,
  OS/router, or private smoke outputs;
- raw event payloads;
- raw private lines;
- raw field values or parser values;
- raw hashes or content hashes;
- exact local paths;
- exact private offsets;
- exact private file sizes;
- exact private timestamps;
- exact filesystem IDs, inodes, archive names, or source-generation IDs from
  private sources;
- screenshots;
- runtime status files;
- failed posts;
- workbook exports;
- SQLite files;
- decklists;
- card choices;
- strategy notes;
- generated/private/local artifacts;
- secrets, credentials, tokens, API keys, webhook URLs, or bearer tokens;
- caller-supplied true readiness or authorization flags;
- caller-supplied protected-surface claims;
- arbitrary issue-closing, PR-opening, branch, commit, staging, or tracker
  instructions.

Forbidden keys should include at least:

- `value`
- `field_value`
- `parser_value`
- `raw_payload`
- `raw_payload_value`
- `raw_payload_values`
- `raw_private_line`
- `raw_private_lines`
- `raw_line`
- `raw_lines`
- `raw_hash`
- `content_hash`
- `exact_offset`
- `exact_start_offset`
- `exact_end_offset`
- `exact_file_size`
- `exact_file_size_bytes`
- `exact_timestamp`
- `private_report_path`
- `local_absolute_path`
- `decklist`
- `card_choices`
- `strategy_notes`

Forbidden values must not be echoed in errors, stop reasons, packet summaries,
or validation output.

## Outputs

The only authorized output for a future helper is an in-memory mapping.

The helper must not write:

- recovery candidate packet files;
- fixture-promotion packets;
- proof files;
- metadata diffs;
- issue drafts;
- PR-assist artifacts;
- local-only artifacts;
- runtime status files;
- diagnostics or drift reports;
- golden replay fixtures;
- golden replay manifests;
- expected-output files;
- corpus manifest or session-ledger entries;
- workbook or webhook payloads.

Any future persisted packet artifact requires a new issue and contract naming
the exact path, privacy scan, review gate, and file-writing authority.

## Invariants

- Candidate packets are review metadata only.
- All readiness and authorization flags remain false.
- Packet summaries must use symbolic evidence labels and status vocabulary
  only.
- Packets must preserve comparison-row confidence, finality, degradation
  flags, parser output policy, and analytics output policy.
- Packets must never raise confidence, finality, or recovery authority.
- Direct candidates may describe existing parser behavior as sufficient, but
  must not authorize new parser behavior.
- Equivalent and derived candidates require review and later scoped contracts
  before any restoration.
- Approximate analytics-only candidates must never restore parser output.
- Blocked private candidates remain blocked behind #434 and later explicit
  private-evidence approval.
- Blocked external candidates remain blocked behind a later external-boundary
  issue.
- Stale, degraded, conflicting, unknown, invalid, or malformed inputs route to
  review or fail closed.
- Summary counts are review aids only and must not become readiness metrics.
- Unknown statuses, unknown field IDs, unknown ledger entry IDs, unknown
  candidate categories, and unknown reviewer decisions require review or fail
  closed.
- The helper must be deterministic for the same input.
- The helper must be copy-safe and must not mutate caller inputs.
- The helper must not import or call parser runtime modules such as router,
  state, `FileTailer`, stream watchers, runner, local app, workbook transport,
  analytics runtime, or AI/model-provider code.
- The helper must not create, stage, commit, push, open PRs, edit issues,
  update trackers, close issues, or trigger Codex F/G behavior.

## Error Behavior

Malformed or unsafe input must return symbolic errors or fail-closed report
statuses. The helper must avoid value echo in all error output.

Expected behavior:

- missing or invalid matrix object: report status `invalid_input`;
- matrix validation errors: report status `invalid_input`;
- missing or invalid comparison report object: report status `invalid_input`;
- comparison row validation errors: packet status `invalid_input` or report
  status `invalid_input`;
- reduced evidence summary not a mapping: packet status `invalid_input`;
- unknown field ID: packet status `review_required`;
- duplicate comparison rows for a field: packet status `conflict`;
- unknown evidence-ledger entry ID: packet status `review_required`;
- unknown candidate category: report status `invalid_input`;
- unknown reviewer decision value: packet status `invalid_input`;
- forbidden current evidence source: report status `fail_closed`;
- raw field values or payload values: report status `fail_closed`;
- privacy marker found: report status `fail_closed`;
- protected-surface assertion not false: report status `fail_closed`;
- any readiness or authorization flag true: report status `fail_closed`;
- stale watcher context: affected packets status `stale_input`;
- blocked watcher/private context: affected packets status
  `blocked_private_evidence`;
- unavailable source context: affected packets status `not_a_candidate` or
  `review_required`;
- contradiction or failed invariant: affected packets status `conflict`;
- report-only or blocked evidence used as parser restoration: report status
  `fail_closed`.

The helper should return as many public-safe symbolic errors as useful for
review, but must stop before including forbidden values or moving protected
surfaces.

## Side Effects

None.

This contract authorizes no runtime side effects and no file side effects
beyond the contract file itself in Codex B.

If later implementation is explicitly authorized, the helper must remain:

- in-memory only;
- deterministic;
- copy-safe;
- side-effect-free;
- free of network calls;
- free of private source reads;
- free of file writes;
- free of GitHub writes;
- free of parser/runtime/local-app/workbook/analytics/AI integration.

## Dependency Order

If implementation is later explicitly authorized:

1. Keep this contract as the source of truth.
2. Add constants and validators in a new in-memory helper module.
3. Reuse existing #451, #452, and #453 vocabularies directly.
4. Add packet-report and packet builders that consume already validated
   inputs.
5. Add fail-closed scans for private markers, forbidden keys, readiness claims,
   authorization claims, protected-surface claims, and local artifacts.
6. Add deterministic ordering and packet ID generation from public-safe fields.
7. Add focused unit tests for all statuses, privacy failures, false flags, and
   no-runtime-import boundaries.
8. Write an implementation handoff.
9. Route to Codex E for adversarial contract testing.

Do not add artifact writing, CLI integration, diagnostics integration, corpus
metadata integration, fixture-promotion integration, parser behavior changes,
or #388/#381 activation in this issue.

## Compatibility

The helper must preserve the existing public helper surfaces from:

- `field_recovery_matrix`;
- `local_watcher_offset_window_monitor`;
- `field_evidence_comparison_report`.

It must not require changes to those modules unless a later contract
explicitly authorizes a narrow compatibility fix.

Existing false flags must remain false:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
file_writing_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
field_recovery_ready: false
```

Existing `candidate_recovery_hints` from #453 remain hints only. This contract
may add packet-level categories, but it must not reinterpret #453 comparison
rows as authorization.

## Tests Required

If implementation is later explicitly authorized, Codex C must add focused
tests for:

- report object shape and required false readiness/authorization flags;
- packet object shape and deterministic JSON serialization;
- deterministic packet ordering and packet ID generation;
- direct comparison rows becoming review packets without parser behavior
  claims;
- equivalent and derived-bounded rows requiring later parser contract and
  fixture review;
- approximate analytics-only rows never restoring parser output;
- unavailable rows producing no parser recovery candidate;
- blocked-private rows remaining behind #434;
- blocked-external rows remaining behind external-boundary follow-up;
- stale, degraded, conflict, review-required, invalid, and unknown rows;
- reviewer decision scaffold defaults and validation;
- summary counts marked as not readiness metrics;
- symbolic offset-window metadata consumption;
- private/local source context routing to blocked/review states;
- forbidden keys and forbidden private markers;
- local absolute paths, exact private offsets, exact private file sizes, exact
  private timestamps, raw hashes, raw payload values, and secret markers
  failing closed without value echo;
- context, matrix, comparison, current evidence, watcher, packet, and review
  decision inputs that try to set readiness/authorization/protected-surface
  claims true;
- copy safety;
- no parser runtime imports;
- no file writes.

Recommended focused validation commands for later Codex C:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_recovery_candidate_packet_generator.py
PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py
python3 -m ruff check src/mythic_edge_parser/app/recovery_candidate_packet_generator.py tests/test_recovery_candidate_packet_generator.py
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Codex C should run broader tests only if the selector recommends them or if
implementation touches shared helpers unexpectedly.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_recovery_candidate_packet_generator.md`.
- Contract links issue #454, tracker #388, parent issue #434, previous issue
  #453, PR #540, and merge commit
  `507952919718b729556bdd3a544ff14ce48f08a0`.
- Contract defines owning layer, truth boundary, internal project area, and
  bridge-code status.
- Contract defines a public-safe in-memory report and packet schema.
- Contract defines candidate status, candidate category, reviewer decision,
  privacy status, and non-claim vocabularies.
- Contract defines allowed inputs and forbidden inputs.
- Contract preserves false readiness and authorization flags.
- Contract forbids private reads, file writes, packet artifacts, fixture
  promotion, corpus status changes, parser behavior changes, and #388/#381
  activation.
- Contract defines fail-closed behavior for private markers, local artifacts,
  forbidden keys, readiness claims, authorization claims, and protected-surface
  claims.
- Contract defines deterministic validation expectations for a later Codex C
  implementation.
- Contract routes implementation only after explicit authorization.

## Open Questions And Risks

- #454 is selected as the active planning lane by the user prompt, but open PRs
  #391 and #374 exist. A stricter WIP-1 reading may require parking, merging,
  closing, or exception metadata before Codex C implementation.
- The #453 comparison report has representative matrix coverage, not a complete
  parser field universe. Candidate packet volume and usefulness may depend on
  future Field Recovery Matrix expansion.
- Future persisted packet artifacts are intentionally not authorized here.
  Their privacy review, retention policy, path, and validation require a
  separate contract.
- Candidate packets may be tempting to treat as parser work tickets. This
  contract allows only review scaffolding, not issue creation, parser changes,
  or fixture promotion.

## Next Workflow Action

Next role:

Codex C only after explicit user implementation authorization. Until then,
pause or route back to Codex A/G for sequencing/authorization.

Pasteable prompt, if the user explicitly authorizes implementation:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #454.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/454

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/453

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/540

Previous merge commit:
507952919718b729556bdd3a544ff14ce48f08a0

Base branch:
main

Contract:
docs/contracts/parser_recovery_candidate_packet_generator.md

Goal:
Implement the deterministic, public-safe, in-memory recovery candidate packet
generator and focused tests exactly as contracted.

Expected implementation files:
- src/mythic_edge_parser/app/recovery_candidate_packet_generator.py
- tests/test_recovery_candidate_packet_generator.py
- docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md

Do not write recovery packet files, fixture-promotion files, proof files,
metadata diffs, local artifacts, fixtures, manifests, corpus metadata, or
runtime artifacts. Do not run or read private Player.log, UTC_Log, app-data,
live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift,
watcher, tailer, or private smoke checks. Do not change parser behavior,
parser event classes, router semantics, parser state final reconciliation,
match/game identity, deduplication, workbook schema, webhook payload shape,
Apps Script behavior, Google Sheets sync, output transport, diagnostics,
drift, golden replay, feature-equity, evidence-ledger behavior, analytics
behavior, AI/model-provider behavior, coaching behavior, CI gates, merge
readiness, deploy readiness, release readiness, production behavior, or final
integration policy.

Preserve:
- parser_behavior_ready=false
- pipeline_activation_ready_for_issue_388=false
- file_writing_authorized=false
- private_harvest_authorized=false
- fixture_promotion_authorized=false
- corpus_status_change_authorized=false
- field_recovery_ready=false

Run the focused validation listed in the contract and write the implementation
handoff. Route to Codex E for adversarial contract testing.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/454"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/453"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/540"
  previous_merge_commit: "507952919718b729556bdd3a544ff14ce48f08a0"
  completed_thread: "B"
  next_thread: "C_after_explicit_user_implementation_authorization"
  source_artifact: "GitHub issue #454 plus Codex A reconciliation comment"
  target_artifact: "docs/contracts/parser_recovery_candidate_packet_generator.md"
  verdict: "recovery_candidate_packet_generator_contract_ready_but_implementation_not_authorized_by_default"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  validation:
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped secret scan over the contract file"
    - "path-scoped protected-surface scan over the contract file"
    - "path-scoped validation selector over the contract file"
  stop_conditions:
    - "Do not implement code until the user explicitly authorizes Codex C implementation."
    - "Do not close #388, #454, or #434."
    - "Do not activate #388 or #381."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, watcher, tailer, or private smoke checks."
    - "Do not create recovery packet files, fixture-promotion files, proof files, metadata diff files, issue drafts, PR-assist artifacts, local artifacts, fixtures, manifests, corpus metadata edits, runtime artifacts, or workbook exports."
    - "Do not promote blocked, report-only, private-evidence, external-boundary, approximate, fallback, watcher, offset-window, degraded, stale, unavailable, or review-required signals to parser truth."
    - "Do not change parser behavior, parser event classes, parser state final reconciliation, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, diagnostics, drift, golden replay, feature-equity, evidence-ledger behavior, analytics behavior, AI/model-provider behavior, coaching behavior, CI gates, merge readiness, deploy readiness, release readiness, production behavior, or final integration policy."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, file-writing authorization, fixture-promotion readiness, field recovery readiness, private smoke success, watcher correctness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
