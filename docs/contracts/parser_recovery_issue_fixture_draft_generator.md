# Parser Recovery Issue And Fixture Draft Generator Contract

## Module

Parser recovery issue and fixture draft generator for planning-only parser
evidence recovery workflows.

Plain English: this contract defines how a future helper may build
deterministic, public-safe, in-memory draft objects from an approved recovery
candidate packet and related public-safe recovery metadata. The draft objects
may help a reviewer prepare a future parser-recovery issue, fixture candidate
summary, golden replay manifest candidate summary, and review checklist. They
must not create GitHub issues, write files, create fixtures, write manifests,
edit corpus metadata, promote corpus rows, change parser behavior, or activate
#388 or #381.

This Codex B pass writes only this contract. It does not implement code, open
a PR, run private checks, create issue draft files, create fixture files, edit
manifest or corpus metadata, change parser behavior, or claim parser recovery.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/455
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/454
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/546
- Previous merge commit: `115e5950ce9006d97fe79af28378f16364644344`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- The operating checkout was on `main` at
  `115e5950ce9006d97fe79af28378f16364644344`.
- PR #546 was merged at
  `115e5950ce9006d97fe79af28378f16364644344`.
- Issue #455 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- The target contract did not exist before this pass.

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
- Issue #455 and Codex A reconciliation comment
- Issue #454 and PR #546
- Pipeline tracker #388
- Parent private-evidence issue #434
- `docs/contracts/parser_recovery_candidate_packet_generator.md`
- `docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md`
- `src/mythic_edge_parser/app/recovery_candidate_packet_generator.py`
- `tests/test_recovery_candidate_packet_generator.py`
- `docs/contracts/parser_recovery_field_evidence_comparison_report.md`
- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`
- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`

No private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop,
packet, OS/router, diagnostics, drift, watcher, or private smoke evidence was
run, tailed, hashed, copied, summarized, or read.

## Observed Current Behavior

Issue #451 added a Field Recovery Matrix helper for parser recovery planning.
Issue #452 added synthetic-only symbolic offset-window metadata. Issue #453
added a field-evidence comparison report. Issue #454 added an in-memory
recovery candidate packet generator:

- `src/mythic_edge_parser/app/recovery_candidate_packet_generator.py`
- `tests/test_recovery_candidate_packet_generator.py`

The #454 helper produces public-safe recovery candidate packet reports and
packets with:

- `parser_behavior_ready=false`;
- `pipeline_activation_ready_for_issue_388=false`;
- `file_writing_authorized=false`;
- `private_harvest_authorized=false`;
- `fixture_promotion_authorized=false`;
- `corpus_status_change_authorized=false`;
- `field_recovery_ready=false`.

It also preserves non-claims such as `not_parser_truth`,
`not_fixture_promotion`, `not_corpus_status_change`, and
`not_file_writing_authorization`.

No helper currently exists to convert approved recovery candidate packets into
issue text drafts, fixture draft summaries, manifest draft summaries, or
review checklists. No committed issue draft artifacts, fixture draft files,
manifest draft files, corpus metadata edits, or GitHub issue/PR actions are
authorized.

In this contract, `file_writing_authorized: false` means the future helper
must not write issue draft files, fixture draft files, manifest draft files,
recovery packet files, fixture-promotion packets, proof files, metadata diffs,
local artifacts, fixtures, manifests, or corpus metadata. The only write
authorized in this Codex B pass is this docs contract.

## Problem

After recovery candidate packets exist, Mythic Edge needs a bounded way to
prepare human-readable review drafts without turning those drafts into action.
Without a contract, a future draft generator could accidentally:

- create GitHub issues or PRs from generated text;
- use closing keywords that close issue #455, #388, #434, or future recovery
  issues unintentionally;
- treat a recovery candidate packet as parser restoration authority;
- treat fixture or manifest draft summaries as committed fixture plans;
- write local or committed draft files without a file-writing contract;
- copy private paths, raw log snippets, exact offsets, file sizes,
  timestamps, hashes, raw payload values, decklists, card choices, or strategy
  notes into public draft text;
- promote fixture drafts, corpus statuses, #388, #381, private harvest, or
  parser behavior readiness;
- let issue text, fixture summaries, manifest summaries, workbook formulas,
  analytics, AI, or coaching own parser recovery truth.

The first bad value is any issue draft, fixture draft summary, manifest draft
summary, review checklist, next-role hint, lifecycle phrase, or generated
body text that causes parser behavior, fixture creation, corpus metadata,
private harvest, GitHub issue/PR lifecycle, or readiness flags to move forward
without a separate scoped contract, implementation, validation, review, and
approved workflow step.

## Scope Decision

This contract defines a planning-only, in-memory draft schema and validation
boundary.

Implementation is not authorized by this Codex B pass. If the user later
explicitly authorizes Codex C implementation, Codex C may add a deterministic,
side-effect-free Python helper and focused tests that build draft reports in
memory from:

1. #454 recovery candidate packet reports and packets;
2. #453 field-evidence comparison report rows already validated by #454;
3. #451 Field Recovery Matrix rows already validated by #454;
4. #452 sanitized symbolic offset-window metadata already accepted by #454;
5. #385 fixture/manifest draft vocabulary as review-only vocabulary; and
6. #386 metadata diff vocabulary as review-only vocabulary.

The future helper must not write issue draft files or local artifacts. A later
artifact writer, GitHub issue creator, PR-assist integration, fixture writer,
manifest writer, corpus metadata updater, diagnostics/drift integration,
golden replay integration, local app integration, or private-evidence
workflow requires its own issue and contract.

This contract does not authorize:

- code implementation in Codex B;
- private source discovery;
- private source reads;
- exact private offset, size, timestamp, path, or hash collection;
- watcher startup;
- tailer startup;
- diagnostics or drift execution;
- local or committed draft writing;
- GitHub issue creation;
- GitHub PR creation;
- branch creation, staging, commits, pushes, PR comments, issue comments, or
  tracker updates;
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
- `corpus_status_change_authorized=true`;
- `issue_creation_authorized=true`;
- `pr_creation_authorized=true`.

## Owning Layer

Primary owner: Quality / Governance.

Supporting owner: Corpus / Provenance.

Quality / Governance owns draft issue text rules, lifecycle wording,
protected-surface checks, privacy/secret checks, refusal vocabulary,
review-checklist shape, and Codex role routing.

Corpus / Provenance owns the review-only fixture draft and manifest draft
summary vocabulary, source evidence basis labels, corpus metadata non-claims,
and compatibility with recovery candidate packets.

Parser remains the only owner of parser facts, parser behavior, parser events,
router semantics, parser state final reconciliation, match/game identity,
deduplication, and parser-owned output values.

## Internal Project Area

Primary: Quality / Governance.

Supporting: Corpus / Provenance and Generated / Local Artifacts boundaries.

This contract sits in Quality / Governance because it defines workflow draft
objects, issue lifecycle safety, false readiness flags, protected-surface
assertions, and validation gates. It uses Corpus / Provenance vocabulary from
the recovery candidate packet and fixture/manifest draft contracts, but does
not move corpus metadata or write fixture artifacts.

## Truth Owner

This contract owns only issue-and-fixture draft generator vocabulary,
in-memory object shape, validation behavior, and non-claim requirements. It
does not own parser facts, private evidence, fixture expected output, corpus
status, readiness metrics, analytics truth, AI truth, coaching truth, issue
lifecycle, PR lifecycle, or tracker completion.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
#451 Field Recovery Matrix
  + #452 symbolic offset-window metadata
  + #453 field-evidence comparison rows
  + #454 recovery candidate packets
  + #385/#386 review-only fixture/manifest/metadata vocabulary
  -> in-memory issue and fixture draft report
  -> human review and later Codex A/B routing
```

Forbidden reverse flow:

```text
issue/fixture draft report
  -/-> parser behavior
  -/-> parser state final reconciliation
  -/-> router behavior
  -/-> fixture files
  -/-> golden replay manifests
  -/-> corpus manifest/session ledger edits
  -/-> GitHub issue or PR creation
  -/-> tracker status changes
  -/-> private harvest approval
  -/-> #388/#381 activation
```

No parser/runtime/workbook/webhook/App Script/local-app/analytics/AI surface is
allowed to consume these drafts as truth.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/parser_recovery_issue_fixture_draft_generator.md`

If later explicitly authorized for implementation, the contract may own:

- `src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py`
- `tests/test_recovery_issue_fixture_draft_generator.py`
- `docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md`

This contract does not own:

- `src/mythic_edge_parser/app/recovery_candidate_packet_generator.py`
- parser runtime modules;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- golden replay fixtures;
- golden replay manifests;
- expected-output files;
- issue comments;
- pull requests;
- tracker comments;
- local draft artifacts.

## Public Interface

This contract defines a future in-memory helper interface only. The interface
must not be implemented until explicitly authorized by a later user prompt or
workflow artifact.

Recommended constants:

```python
RECOVERY_ISSUE_FIXTURE_DRAFT_REPORT_OBJECT = (
    "mythic_edge_parser_recovery_issue_fixture_draft_report"
)
RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION = (
    "parser_recovery_issue_fixture_draft_generator.v1"
)
RECOVERY_ISSUE_DRAFT_OBJECT = (
    "mythic_edge_parser_recovery_issue_draft"
)
RECOVERY_FIXTURE_DRAFT_SUMMARY_OBJECT = (
    "mythic_edge_parser_recovery_fixture_draft_summary"
)
RECOVERY_MANIFEST_DRAFT_SUMMARY_OBJECT = (
    "mythic_edge_parser_recovery_manifest_draft_summary"
)
RECOVERY_DRAFT_REVIEW_CHECKLIST_OBJECT = (
    "mythic_edge_parser_recovery_draft_review_checklist"
)
```

Recommended future helper functions:

```python
build_recovery_issue_fixture_draft_report(...)
build_recovery_issue_draft(...)
build_recovery_fixture_draft_summary(...)
build_recovery_manifest_draft_summary(...)
validate_recovery_issue_fixture_draft_report(...)
validate_recovery_issue_draft(...)
validate_recovery_fixture_draft_summary(...)
validate_recovery_manifest_draft_summary(...)
```

No CLI, environment variable, runtime service, diagnostics section, drift
report section, runtime status field, workbook column, webhook payload, Apps
Script surface, corpus metadata field, fixture schema, golden replay manifest,
GitHub issue, GitHub PR, or parser event is authorized by this interface.

## Draft Report Shape

A future report is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_issue_fixture_draft_report` |
| `schema_version` | yes | `parser_recovery_issue_fixture_draft_generator.v1` |
| `source_issue` | yes | Issue #455 URL |
| `pipeline_tracker` | yes | Tracker #388 URL |
| `parent_private_evidence_issue` | yes | Parent #434 URL |
| `previous_issue` | yes | Issue #454 URL |
| `previous_pr` | yes | PR #546 URL |
| `status` | yes | Report status vocabulary below |
| `status_reasons` | yes | Symbolic reason codes only |
| `source_packet_report_ref` | yes | Public-safe #454 report reference |
| `drafts` | yes | List of draft groups |
| `summary` | yes | Counts by status/type; never a readiness metric |
| `privacy` | yes | False assertions and symbolic privacy status |
| `protected_surface_assertions` | yes | All protected-surface booleans false |
| `readiness_flags` | yes | All readiness flags false |
| `authorization_flags` | yes | All authorization flags false |
| `limitations` | yes | Non-authority notes |
| `non_claims` | yes | Required non-claim vocabulary |

Allowed report statuses:

- `drafts_ready_for_review`
- `empty`
- `review_required`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `invalid_input`
- `fail_closed`

`drafts_ready_for_review` means only that public-safe in-memory draft objects
were constructed for review. It is not issue creation authority, PR creation
authority, file-writing authority, fixture promotion readiness, parser
behavior readiness, private harvest authorization, #388 activation readiness,
release readiness, or production behavior.

## Draft Group Shape

A draft group connects one accepted #454 recovery candidate packet to a
logical issue draft, fixture draft summary, manifest draft summary, and review
checklist.

| Field | Required | Meaning |
| --- | --- | --- |
| `draft_group_id` | yes | Deterministic symbolic ID from public-safe fields |
| `source_packet_id` | yes | #454 packet ID |
| `field_id` | yes | Source packet field ID |
| `field_family` | yes | Source packet field family |
| `draft_status` | yes | Draft status vocabulary below |
| `draft_type` | yes | Draft type vocabulary below |
| `issue_draft` | yes | In-memory issue draft object or blocked summary |
| `fixture_draft_summary` | yes | In-memory fixture draft summary or blocked summary |
| `manifest_draft_summary` | yes | In-memory manifest draft summary or blocked summary |
| `review_checklist` | yes | In-memory review checklist object |
| `stop_reasons` | yes | Symbolic stop reasons |
| `next_role_hint` | yes | `codex_a_problem_representation`, `codex_b_contract`, `review_only`, `blocked`, or `no_action` |
| `non_claims` | yes | Required non-claim vocabulary |

Draft group IDs must be deterministic and must use only:

- schema version;
- source packet ID;
- field ID;
- field family;
- draft type;
- draft status;
- public issue URLs;
- public schema versions.

Draft group IDs must not include:

- raw field values;
- local paths;
- private offsets;
- private file sizes;
- timestamps from private sources;
- hashes;
- raw event payloads;
- decklists, card choices, or strategy notes;
- secrets or credentials.

## Issue Draft Shape

An issue draft is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_issue_draft` |
| `schema_version` | yes | `parser_recovery_issue_fixture_draft_generator.v1` |
| `draft_id` | yes | Public-safe deterministic ID |
| `draft_status` | yes | Draft status vocabulary |
| `title` | yes | Public-safe title, no private values |
| `body_sections` | yes | Ordered public-safe sections |
| `refs` | yes | Public issue/PR references only |
| `suggested_labels` | yes | Optional label names as review suggestions only |
| `suggested_tracker_update` | yes | Optional text as review suggestion only |
| `lifecycle_wording_status` | yes | `refs_only` or blocked status |
| `forbidden_lifecycle_terms_found` | yes | Boolean; must be false for ready drafts |
| `privacy_status` | yes | Public-safe privacy status |
| `protected_surface_assertions` | yes | All protected-surface booleans false |
| `readiness_flags` | yes | All readiness flags false |
| `authorization_flags` | yes | All authorization flags false |
| `non_claims` | yes | Required non-claim vocabulary |

Allowed body sections:

- `problem`
- `source_packet_summary`
- `evidence_basis`
- `proposed_scope`
- `proposed_fixture_summary`
- `proposed_manifest_summary`
- `required_review_questions`
- `protected_boundaries`
- `validation_expectations`
- `non_claims`
- `workflow_handoff_stub`

The issue draft body must use `Refs` wording for linked issues. It must not use
closing keywords such as `Closes`, `Fixes`, `Fix`, `Resolves`, `Resolve`,
`Closed by`, or `Done by`. This rule applies to plain text, Markdown links,
workflow handoff text, and suggested PR body text.

Suggested labels, tracker updates, issue titles, and issue body sections are
advisory text only. The future helper must not call GitHub, create issues,
edit issues, comment on trackers, apply labels, or close issues.

## Fixture Draft Summary Shape

A fixture draft summary is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_fixture_draft_summary` |
| `schema_version` | yes | `parser_recovery_issue_fixture_draft_generator.v1` |
| `draft_id` | yes | Public-safe deterministic ID |
| `draft_status` | yes | Draft status vocabulary |
| `source_packet_id` | yes | #454 packet ID |
| `fixture_evidence_class` | yes | Fixture evidence class vocabulary below |
| `scenario_family` | yes | Symbolic scenario family or `review_required` |
| `event_family_scope` | yes | Symbolic parser event families only |
| `expected_parser_fact_scope` | yes | Parser-owned expected sections only |
| `minimal_window_summary` | yes | Symbolic/count-only summary, no raw lines |
| `proposed_fixture_path` | yes | Optional repo-relative proposal or `not_applicable` |
| `file_writing_authorized` | yes | Always false |
| `fixture_promotion_authorized` | yes | Always false |
| `forbidden_content_summary` | yes | Symbolic absence/presence statuses |
| `review_gates` | yes | Gates required before any future fixture |
| `non_claims` | yes | Required non-claim vocabulary |

Allowed fixture evidence classes:

- `synthetic_only_candidate`
- `committed_sanitized_candidate`
- `metadata_only_candidate`
- `private_gated_candidate`
- `external_gated_candidate`
- `blocked_no_fixture_candidate`
- `review_required_candidate`

Fixture draft summaries are summaries only. They must not contain raw line
text, raw JSON payloads, local absolute paths, private offsets, private file
sizes, private timestamps, hashes, raw card/deck information, or hostile test
payload values.

## Manifest Draft Summary Shape

A manifest draft summary is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_manifest_draft_summary` |
| `schema_version` | yes | `parser_recovery_issue_fixture_draft_generator.v1` |
| `draft_id` | yes | Public-safe deterministic ID |
| `draft_status` | yes | Draft status vocabulary |
| `source_packet_id` | yes | #454 packet ID |
| `proposed_manifest_path` | yes | Optional repo-relative proposal or `not_applicable` |
| `manifest_object` | yes | Expected manifest object or `not_applicable` |
| `manifest_schema_version` | yes | Expected schema or `not_applicable` |
| `expected_sections` | yes | Parser-owned expected sections only |
| `corpus_manifest_change` | yes | Always `not_authorized` in this slice |
| `session_ledger_change` | yes | Always `not_authorized` in this slice |
| `file_writing_authorized` | yes | Always false |
| `corpus_status_change_authorized` | yes | Always false |
| `review_gates` | yes | Gates required before any future manifest |
| `non_claims` | yes | Required non-claim vocabulary |

Allowed expected sections for v1 summaries are inherited from
`docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md` and
must remain parser-owned expected sections:

- `router_stats`
- `event_family_counts`
- `event_kind_sequence`
- `diagnostics_summary`
- `truncation_and_data_loss`
- `unknowns_and_degradation`
- `parser_state`
- `final_reconciliation`
- `parser_owned_rows`

Manifest draft summaries must not be stored under `tests/fixtures/` and must
not be confused with committed golden replay manifests. They are in-memory
review summaries only.

## Review Checklist Shape

A review checklist is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_draft_review_checklist` |
| `schema_version` | yes | `parser_recovery_issue_fixture_draft_generator.v1` |
| `checklist_id` | yes | Public-safe deterministic ID |
| `source_packet_id` | yes | #454 packet ID |
| `required_human_checks` | yes | Symbolic checklist items |
| `required_codex_checks` | yes | Symbolic checklist items |
| `blocking_questions` | yes | Public-safe questions |
| `privacy_checks` | yes | Symbolic privacy checks |
| `protected_surface_checks` | yes | Symbolic protected-surface checks |
| `next_role_hint` | yes | Symbolic next role only |
| `non_claims` | yes | Required non-claim vocabulary |

The checklist may recommend a future Codex A or Codex B thread. It must not
recommend Codex F/G action unless a later reviewed package exists, and it must
not claim that an issue, fixture, manifest, PR, corpus edit, or parser change
is ready to execute.

## Draft Status Vocabulary

Allowed `draft_status` values:

- `draft_ready_for_review`
- `review_required`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `blocked_authorization`
- `blocked_privacy`
- `blocked_overclaim`
- `not_a_draft_candidate`
- `insufficient_packet_review`
- `insufficient_fixture_basis`
- `insufficient_manifest_basis`
- `conflict`
- `invalid_input`

Status rules:

- `candidate_ready_for_review` packets from #454 may produce
  `draft_ready_for_review` only when all lifecycle wording, privacy,
  protected-surface, false-readiness, and non-claim checks pass.
- #454 packets with `review_required` may produce `review_required` drafts,
  but the issue text must ask for human review rather than action.
- `blocked_private_evidence` packets must remain
  `blocked_private_evidence`.
- `blocked_external_boundary` packets must remain
  `blocked_external_boundary`.
- `blocked_privacy`, `blocked_authorization`, `blocked_unsupported_claim`,
  `stale_input`, `conflict`, and `invalid_input` packets must not become
  draft-ready.
- Unknown packet statuses, unknown candidate categories, unknown field IDs,
  unknown evidence IDs, or unknown next-role hints must route to
  `review_required`, `invalid_input`, or `fail_closed`.

## Draft Type Vocabulary

Allowed `draft_type` values:

- `issue_only_review_draft`
- `issue_plus_fixture_summary_draft`
- `issue_plus_manifest_summary_draft`
- `issue_fixture_manifest_review_draft`
- `blocked_private_evidence_summary`
- `blocked_external_boundary_summary`
- `no_action_summary`
- `review_required_summary`

Draft types are review labels only. They do not authorize file writing,
fixture creation, manifest creation, issue creation, or PR creation.

## Report Status Precedence

If multiple statuses apply, future implementation must use this precedence:

```text
fail_closed
invalid_input
blocked_privacy
blocked_authorization
blocked_private_evidence
blocked_external_boundary
blocked_overclaim
conflict
review_required
empty
drafts_ready_for_review
```

## Non-Claim Vocabulary

Required non-claims:

- `not_parser_truth`
- `not_issue_creation_authority`
- `not_pr_creation_authority`
- `not_file_writing_authorization`
- `not_field_recovery_readiness`
- `not_private_harvest_authorization`
- `not_fixture_promotion`
- `not_corpus_status_change`
- `not_parser_behavior_readiness`
- `not_pipeline_activation_readiness`
- `not_watcher_correctness`
- `not_private_smoke_success`
- `not_merge_readiness`
- `not_deploy_readiness`
- `not_release_readiness`
- `not_production_behavior`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`

The generator must preserve these non-claims on the report, every draft group,
every issue draft, every fixture draft summary, every manifest draft summary,
and every review checklist object.

## Inputs

### Recovery Candidate Packet Report

Accepted source:

- `recovery_candidate_packet_generator.build_recovery_candidate_packet_report(...)`,
  or
- an already validated report from
  `validate_recovery_candidate_packet_report(...)`.

The draft generator may read:

- `object`
- `schema_version`
- `source_issue`
- `pipeline_tracker`
- `parent_private_evidence_issue`
- `status`
- `status_reasons`
- `packets`
- `summary`
- `privacy`
- `protected_surface_assertions`
- `limitations`
- `non_claims`

The draft generator must not treat candidate packet report status as
authorization. It must preserve all #454 false readiness and authorization
flags.

### Recovery Candidate Packets

Accepted source:

- #454 packet objects already validated by
  `validate_recovery_candidate_packet(...)`.

The draft generator may read:

- `packet_id`
- `field_id`
- `display_name`
- `field_family`
- `candidate_status`
- `candidate_category`
- `candidate_summary`
- `field_recovery_matrix_ref`
- `comparison_row_ref`
- `expected_evidence_summary`
- `current_evidence_summary`
- `evidence_delta`
- `source_evidence_refs`
- `offset_window_refs`
- `confidence`
- `finality`
- `degradation_flags`
- `comparison_status`
- `candidate_recovery_hints`
- `stop_reasons`
- `privacy_status`
- `reviewer_decision`
- `review_required`
- `next_role_hint`
- `non_claims`

The draft generator must not raise confidence, finality, or readiness above
the source packet.

### Reviewer Decision Scaffold

Accepted source:

- #454 reviewer decision objects with `decision` still `undecided`, or
  later reviewed decision objects only if a later contract explicitly adds
  them.

The draft generator may read:

- `decision`
- `decision_reason`
- `allowed_next_step`
- `requires_new_issue`
- `requires_private_evidence_approval`
- `requires_parser_contract`
- `requires_fixture_promotion_contract`
- `requires_corpus_status_contract`
- `non_claims`

`requires_new_issue=true` may only be represented as a suggested future Codex A
route. It is not issue creation authority.

### Fixture And Manifest Vocabulary References

The draft generator may use #385 fixture/manifest draft vocabulary as static
review vocabulary only. It may not call any fixture/manifest draft builder
unless a later implementation contract explicitly authorizes that call.

Allowed referenced concepts:

- draft status names;
- fixture evidence class names;
- parser-owned expected sections;
- fixture minimization rules;
- manifest expected-section boundaries;
- non-claim language.

The draft generator must not create fixture draft files, manifest draft files,
expected-output files, or corpus manifest/session ledger edits.

### Corpus Metadata Vocabulary References

The draft generator may use #386 metadata diff vocabulary as static review
vocabulary only. It must not build or write metadata diff artifacts in this
slice.

Allowed referenced concepts:

- manifest/session-ledger consistency checklist names;
- metadata movement blocked/required labels;
- corpus status non-claim language;
- public-safe issue and contract refs.

### Context

Optional context may include:

- `source_issue`: Issue #455 URL;
- `pipeline_tracker`: Tracker #388 URL;
- `parent_private_evidence_issue`: Parent #434 URL;
- `previous_issue`: Issue #454 URL;
- `previous_pr`: PR #546 URL;
- public schema versions;
- symbolic run labels;
- all readiness and authorization flags set to `false`;
- protected-surface assertions set to `false`.

If context tries to set any readiness, authorization, protected-surface,
private-harvest, file-writing, issue-creation, PR-creation, fixture-promotion,
corpus-status, parser, runtime, workbook, analytics, AI, coaching, merge,
deploy, release, or production claim to true, the generator must fail closed.

## Forbidden Inputs

The draft generator must reject or fail closed on:

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
- secrets, credentials, tokens, API keys, webhook URLs, bearer tokens, or Apps
  Script URLs;
- caller-supplied true readiness or authorization flags;
- caller-supplied protected-surface claims;
- caller-supplied issue-closing, PR-opening, branch, commit, staging, tracker,
  merge, deploy, release, or production instructions;
- body text containing GitHub closing keywords.

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
- `closes`
- `fixes`
- `resolves`
- `issue_creation_authorized`
- `pr_creation_authorized`

Forbidden values must not be echoed in errors, stop reasons, generated issue
draft text, fixture summaries, manifest summaries, or validation output.

## Outputs

The only authorized output for a future helper is an in-memory mapping.

The helper must not write:

- issue draft files;
- recovery candidate packet files;
- fixture draft files;
- golden replay fixture files;
- golden replay manifest draft files;
- expected-output files;
- fixture-promotion packets;
- proof files;
- metadata diffs;
- PR-assist artifacts;
- local-only artifacts;
- runtime status files;
- diagnostics or drift reports;
- corpus manifest or session-ledger entries;
- workbook or webhook payloads.

The helper must not create, edit, comment on, label, close, or link GitHub
issues or PRs.

Any future persisted draft artifact requires a new issue and contract naming
the exact path, privacy scan, review gate, and file-writing authority.

## Invariants

- Draft objects are review metadata only.
- All readiness and authorization flags remain false.
- Draft text must use `Refs`-only lifecycle wording.
- Draft text must not contain GitHub closing keywords.
- Draft text must not suggest that Codex F or Codex G can act without a later
  reviewed package and explicit user authorization.
- Draft summaries must use symbolic evidence labels and status vocabulary
  only.
- Draft summaries must preserve source packet confidence, finality,
  degradation flags, candidate status, and non-claims.
- Draft summaries must never raise confidence, finality, or recovery
  authority.
- Blocked private candidates remain blocked behind #434 and later explicit
  private-evidence approval.
- Blocked external candidates remain blocked behind a later external-boundary
  issue.
- Stale, degraded, conflicting, unknown, invalid, or malformed inputs route to
  review or fail closed.
- Summary counts are review aids only and must not become readiness metrics.
- Unknown statuses, unknown field IDs, unknown ledger entry IDs, unknown draft
  types, and unknown next-role hints require review or fail closed.
- The helper must be deterministic for the same input.
- The helper must be copy-safe and must not mutate caller inputs.
- The helper must not import or call parser runtime modules such as router,
  state, `FileTailer`, stream watchers, runner, local app, workbook transport,
  analytics runtime, AI/model-provider code, GitHub clients, subprocess Git,
  or network clients.
- The helper must not create, stage, commit, push, open PRs, edit issues,
  update trackers, close issues, or trigger Codex F/G behavior.

## Error Behavior

Malformed or unsafe input must return symbolic errors or fail-closed report
statuses. The helper must avoid value echo in all error output.

Expected behavior:

- missing or invalid candidate packet report: report status `invalid_input`;
- candidate packet validation errors: draft status `invalid_input`;
- missing candidate packets: report status `empty`;
- unknown field ID: draft status `review_required`;
- duplicate packet IDs: draft status `conflict`;
- unknown evidence-ledger entry ID: draft status `review_required`;
- unknown candidate status: draft status `invalid_input`;
- unknown draft type: draft status `invalid_input`;
- forbidden source evidence: report status `fail_closed`;
- raw field values or payload values: report status `fail_closed`;
- privacy marker found: report status `fail_closed`;
- protected-surface assertion not false: report status `fail_closed`;
- any readiness or authorization flag true: report status `fail_closed`;
- issue lifecycle closing keyword found: draft status `blocked_authorization`
  or report status `fail_closed`;
- stale source packet: affected draft status `review_required`;
- blocked private packet: affected draft status `blocked_private_evidence`;
- blocked external packet: affected draft status `blocked_external_boundary`;
- unavailable source context: affected draft status `not_a_draft_candidate` or
  `review_required`;
- contradiction or failed invariant: affected draft status `conflict`;
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
3. Reuse #454 packet schemas and validators directly.
4. Add draft report, issue draft, fixture summary, manifest summary, and
   checklist builders that consume already validated packet objects.
5. Add fail-closed scanners for private markers, local paths, raw payload keys,
   exact offsets/sizes/timestamps/hashes, secrets, true readiness flags,
   protected-surface claims, issue/PR creation claims, and GitHub closing
   keywords.
6. Add deterministic ordering and draft ID generation from public-safe fields.
7. Add focused synthetic tests.
8. Write an implementation handoff.
9. Defer any issue creation, PR creation, file writer, fixture draft artifact,
   golden replay manifest artifact, fixture-promotion packet, corpus metadata
   update, or #388/#381 activation to separate contracts.

## Compatibility

Future implementation must remain compatible with:

- #451 Field Recovery Matrix schema and false-claim rules;
- #452 symbolic offset-window metadata and local-only privacy boundary;
- #453 field-evidence comparison report schema and confidence/finality
  policies;
- #454 recovery candidate packet schema and validator behavior;
- #385 fixture/manifest draft vocabulary;
- #386 metadata diff vocabulary;
- #387 PR-assist boundary preserving Codex F/G separation;
- #516/#518 #388 activation and planning boundaries.

Compatibility does not authorize stale start-condition wording from older
issues, automatic GitHub lifecycle actions, private harvest, file writing,
fixture promotion, corpus status movement, or parser behavior changes.

## Tests Required

If implementation is later explicitly authorized, add focused tests for:

- report object shape and deterministic JSON serialization;
- issue draft shape and `Refs`-only lifecycle wording;
- rejection of `Closes`, `Fixes`, `Resolves`, and equivalent closing
  lifecycle phrases;
- fixture draft summary shape;
- manifest draft summary shape;
- review checklist shape;
- false readiness and authorization flags on report and nested objects;
- required non-claims on report and nested objects;
- `candidate_ready_for_review` packet becoming review-only draft-ready;
- `review_required` packet remaining review-required;
- blocked-private packet remaining blocked-private;
- blocked-external packet remaining blocked-external;
- invalid, stale, conflict, and unsupported packets refusing action;
- no value echo for raw/private markers;
- direct rejection of forbidden keys;
- local path and secret marker rejection;
- true readiness, issue creation, PR creation, file writing, fixture promotion,
  corpus status, or protected-surface claims failing closed;
- copy safety;
- deterministic draft ordering and IDs;
- no runtime/parser/workbook/local-app/analytics/AI/GitHub imports;
- no file writes.

Recommended validation commands for a later Codex C implementation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_recovery_issue_fixture_draft_generator.py
PYTHONPATH=src python3 -m pytest -q tests/test_recovery_candidate_packet_generator.py tests/test_field_evidence_comparison_report.py tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py
python3 -m ruff check src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py tests/test_recovery_issue_fixture_draft_generator.py
git diff --check
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
python3 tools/select_validation.py --base origin/main
```

Recommended path-scoped scans for a later Codex C implementation:

```bash
printf '%s\n' \
  docs/contracts/parser_recovery_issue_fixture_draft_generator.md \
  src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py \
  tests/test_recovery_issue_fixture_draft_generator.py \
  docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Any positive match must be reviewed. Public GitHub URLs are allowed only when
they are issue, PR, repo, or docs references and not webhook URLs.

## Acceptance Criteria

Codex B acceptance criteria:

- Contract exists at
  `docs/contracts/parser_recovery_issue_fixture_draft_generator.md`.
- Contract cites #455, #388, #434, #454, PR #546, and the relevant recovery
  contracts.
- Contract defines in-memory issue draft, fixture draft summary, manifest
  draft summary, and review checklist object shapes.
- Contract defines status, draft type, lifecycle wording, privacy, non-claim,
  and false-readiness rules.
- Contract explicitly forbids private reads, file writes, automatic issue/PR
  creation, fixture promotion, corpus status changes, parser changes, and
  pipeline activation.
- `git diff --check` passes.
- `python3 tools/check_agent_docs.py` passes.

Future Codex C acceptance criteria, only if explicitly authorized:

- Implementation adds only the helper, focused tests, and implementation
  handoff named by this contract.
- Helper remains in-memory, deterministic, side-effect-free, and copy-safe.
- Helper emits no GitHub issue/PR actions and no files.
- Helper preserves all false readiness and authorization flags.
- Helper fails closed on forbidden content and lifecycle closing keywords.
- Focused tests and adjacent recovery tests pass.

## Open Questions And Risks

- Codex A may need to decide whether #455 should receive implementation at
  all, because the current handoff preserves `implementation_authorized=false`.
- Future issue creation remains deliberately separate from draft generation.
  A later GitHub issue creator would be a high-risk workflow surface requiring
  a separate contract and explicit user authorization.
- Future fixture/manifest draft file writing remains deliberately separate
  from in-memory summary generation.
- A generated issue draft may still be tempting to paste into GitHub without
  review. Future implementation must make non-claims and `Refs`-only wording
  highly visible.
- This contract does not decide #456 human-approved parser/corpus update
  workflow. That remains a later issue.

## Next Workflow Action

Next role:

- Codex A for lifecycle/reordering if implementation should remain
  unauthorized.
- Codex C only if the user explicitly authorizes a synthetic-only, in-memory
  implementation pass.

Pasteable Codex C prompt if implementation is explicitly authorized:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #455.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/455

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/454

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/546

Previous merge commit:
115e5950ce9006d97fe79af28378f16364644344

Base branch:
main

Contract:
docs/contracts/parser_recovery_issue_fixture_draft_generator.md

Goal:
Implement the deterministic, public-safe, in-memory issue and fixture draft
generator defined by the contract.

Expected files, if implementation is explicitly authorized:
- src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py
- tests/test_recovery_issue_fixture_draft_generator.py
- docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md

Scope:
- Compare current code to the contract.
- Build in-memory draft report, issue draft, fixture draft summary, manifest
  draft summary, and review checklist helpers.
- Consume only validated #454 recovery candidate packet reports/packets and
  public-safe contract vocabulary.
- Preserve all false readiness and authorization flags.
- Enforce `Refs`-only issue lifecycle wording.
- Fail closed on raw/private markers, local paths, exact offsets/sizes/
  timestamps/hashes, secrets, true readiness flags, protected-surface claims,
  issue/PR creation claims, file-writing claims, fixture-promotion claims,
  corpus-status claims, and GitHub closing keywords.

Do not:
- activate #388 or #381;
- run or read private Player.log, UTC_Log, app-data, live MTGA, diagnostics,
  drift, watcher, network, firewall/drop, packet, OS/router, or private smoke
  checks;
- create GitHub issues or PRs;
- write issue draft files, fixture files, manifest files, expected-output
  files, packet files, proof files, metadata diff files, PR-assist artifacts,
  local/generated artifacts, corpus manifest entries, or session ledger
  entries;
- change parser behavior, parser event classes, router semantics, parser
  state final reconciliation, match/game identity, deduplication, workbook
  schema, webhook payload shape, Apps Script behavior, analytics truth, AI
  truth, coaching truth, CI gates, release readiness, deploy readiness,
  production behavior, or final integration policy;
- claim parser_behavior_ready, pipeline_activation_ready_for_issue_388,
  file_writing_authorized, private_harvest_authorized,
  fixture_promotion_authorized, corpus_status_change_authorized,
  issue_creation_authorized, or pr_creation_authorized.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_recovery_issue_fixture_draft_generator.py
- PYTHONPATH=src python3 -m pytest -q tests/test_recovery_candidate_packet_generator.py tests/test_field_evidence_comparison_report.py tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py
- python3 -m ruff check src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py tests/test_recovery_issue_fixture_draft_generator.py
- git diff --check
- python3 tools/check_agent_docs.py
- python3 tools/check_secret_patterns.py --all
- python3 tools/check_protected_surfaces.py --base origin/main
- python3 tools/select_validation.py --base origin/main
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/455"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/454"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/546"
  completed_thread: "B"
  next_thread: "A_or_C_after_explicit_implementation_authorization"
  source_artifact: "GitHub issue #455 Codex A reconciliation comment"
  target_artifact: "docs/contracts/parser_recovery_issue_fixture_draft_generator.md"
  verdict: "issue_fixture_draft_generator_contract_complete_planning_only"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "115e5950ce9006d97fe79af28378f16364644344"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  file_writing_authorized: false
  issue_creation_authorized: false
  pr_creation_authorized: false
  validation:
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not activate #388 or #381."
    - "Do not close #388, #455, or #434."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, diagnostics, drift, watcher, network, firewall/drop, packet, OS/router, or private smoke checks."
    - "Do not create GitHub issues, PRs, branches, commits, recovery packet files, fixture-promotion packets, fixtures, manifests, expected-output files, corpus metadata edits, or local/generated artifacts."
    - "Do not authorize parser changes, private harvest execution, file-writing, fixture promotion, corpus status changes, PR creation, issue creation, or pipeline activation."
    - "Do not claim parser behavior readiness, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, or coaching truth."
```
