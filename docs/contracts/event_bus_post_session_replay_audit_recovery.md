# EventBus Post-Session Replay Audit And Recovery Contract

Status: contract only
Codex role: B, Module Contract Writer
Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/473
Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
Latest verified `origin/main`: `48da1214fbd2adb1ce47d442711dca2807ebb59b`

## Purpose

This contract defines the boundary for a future post-session replay audit and
review workflow after EventBus delivery is suspected to be incomplete,
discontinuous, cancelled, or degraded.

Plain English behavior:

- Live parser/runtime delivery remains the primary parser path.
- EventBus sequence and gap diagnostics, if later implemented, are in-memory
  diagnostic signals only.
- Post-session replay audit may be considered only after separate authorization.
- Replay audit can support human review, drift analysis, and scoped recovery
  planning, but it must not become the live truth path or an automatic repair
  mechanism.
- Recovery means a reviewed candidate for later human-approved parser/corpus
  work. It does not mean automatic parser fact rewrite, fixture promotion,
  corpus status movement, workbook repair, webhook replay, or readiness.

This Codex B pass writes only this contract. It does not implement code, open a
PR, read private logs, run replay audit, promote fixtures, update corpus
metadata, change parser behavior, change EventBus behavior, create runtime
artifacts, change CI, or claim reliability readiness or parser truth.

## Source Context

Source issue:

- Issue #473:
  https://github.com/Tahjali11/Mythic-Edge/issues/473
- Project roadmap:
  https://github.com/Tahjali11/Mythic-Edge/issues/568
- Latest completed issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/472
- Latest completed PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/661
- Latest merge commit:
  `48da1214fbd2adb1ce47d442711dca2807ebb59b`

Prerequisites:

- Issue #460 / PR #654 established completeness-preserving EventBus
  backpressure.
- Issue #471 / PR #655 established EventBus consumer delivery classifications.
- Issue #467 / PR #658 established privacy-safe queue pressure metrics.
- Issue #470 / PR #657 established heavy-subscriber worker-queue planning.
- Issue #468 / PR #659 established EventBus capacity configuration boundaries.
- Issue #469 / PR #660 established concurrent fanout completeness boundaries.
- Issue #472 / PR #661 established EventBus sequence ID and subscriber gap
  detection boundaries.

Related parser-evidence work:

- Issue #381: UTC_Log source adapter boundary.
- Issue #382: local harvest candidate report boundary.
- Tracker #388: parser evidence pipeline.
- Parent private-evidence issue #434.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- GitHub issue #473
- GitHub issue #568
- GitHub PR #661
- `docs/contracts/event_bus_completeness_over_liveness_backpressure.md`
- `docs/contracts/event_bus_consumer_delivery_classification.md`
- `docs/contracts/event_bus_queue_pressure_metrics.md`
- `docs/contracts/event_bus_heavy_subscriber_worker_queues.md`
- `docs/contracts/event_bus_capacity_configuration_and_default_tuning.md`
- `docs/contracts/event_bus_concurrent_fanout_completeness.md`
- `docs/contracts/event_bus_sequence_ids_and_subscriber_gap_detection.md`
- `docs/contracts/parser_evidence_pipeline_activation_contract.md`
- `docs/contracts/parser_evidence_bounded_local_dry_run.md`
- `docs/contracts/parser_evidence_confidence_claim_vocabulary.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_saved_event_replay.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/local_artifacts_manifest.json`
- `src/mythic_edge_parser/event_bus.py`
- `tests/test_event_bus.py`
- `tests/test_event_bus_queue_pressure_metrics.py`

No private `Player.log`, `UTC_Log`, app-data, live MTGA data, runtime status
files, local-only artifacts, workbook exports, raw diffs, source patches,
secrets, credentials, tokens, API keys, or webhook URLs were read.

## Owning Layer

Primary internal project area: Quality / Governance.

Supporting internal project areas:

- Parser, for EventBus delivery and parser/state interpretation.
- Corpus / Provenance, for replay, evidence, fixture, and review vocabulary.
- Generated / Local Artifacts, for any future private local run inputs and
  local-only outputs.

Truth owner: parser and state interpretation.

This contract owns workflow and report vocabulary only. It does not own parser
facts, MTGA raw log truth, EventBus delivery implementation, parser event
classes, corpus status, fixture truth, workbook truth, webhook truth, API
truth, analytics truth, AI truth, coaching truth, release readiness, deploy
readiness, or production behavior.

## Bridge-Code Status

`deferred_future_boundary`

No bridge code is authorized by this contract.

If later authorized, a post-session replay audit helper would be bridge-code
planning from local/private evidence and EventBus diagnostics into public-safe
review metadata:

```text
EventBus diagnostic signal
  -> separately authorized local replay/audit run
  -> sanitized audit summary
  -> human review
  -> later scoped recovery, fixture, corpus, or parser issue if approved
```

Forbidden reverse flow:

- replay audit must not rewrite live parser state;
- replay audit must not redefine parser truth;
- review metadata must not become fixture promotion;
- workbook, webhook, API, analytics, AI, or coaching output must not correct
  parser facts.

## Files Owned By This Contract

- `docs/contracts/event_bus_post_session_replay_audit_recovery.md`

Potential future artifacts, not authorized by this contract:

- a public-safe implementation handoff, likely:
  `docs/implementation_handoffs/event_bus_post_session_replay_audit_recovery_comparison.md`
- a public-safe contract-test report, likely:
  `docs/contract_test_reports/event_bus_post_session_replay_audit_recovery.md`
- a future helper module and tests only if separately contracted and approved.

This contract does not authorize edits to:

- `src/mythic_edge_parser/event_bus.py`
- parser event classes;
- parser state or final reconciliation;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- golden replay fixtures;
- expected-output files;
- runtime status artifacts;
- workbook, webhook, API, Apps Script, analytics, AI, or CI surfaces.

## Observed Current Behavior

Current EventBus state on `origin/main`:

- `EventBus.publish()` preserves completeness by waiting for subscriber queue
  capacity.
- `EventBus.subscribe(consumer_id=...)` records public-safe consumer
  classification metadata.
- `EventBus.queue_pressure_snapshot()` reports public-safe diagnostic metrics.
- `EventBus.reset_queue_pressure_metrics()` resets metrics without changing
  delivery.
- No EventBus-owned sequence IDs, subscriber gap snapshots, or replay audit
  surfaces are implemented.

Current replay and evidence state:

- `parser_saved_event_replay.md` covers replaying generated saved-event JSONL
  archives. It is not a raw `Player.log` replay path and does not own parser
  truth.
- `parser_golden_replay_harness.md` covers committed sanitized `Player.log`
  fixture replay. It does not authorize raw private log commits or automatic
  expected-output updates.
- `parser_evidence_utc_log_source_adapter.md` keeps `UTC_Log` adapter work
  synthetic/local-only by default and prevents `UTC_Log` from becoming a second
  parser truth source.
- `parser_evidence_local_harvest_candidate_reports.md` defines advisory
  candidate reports without private source reads or fixture promotion.
- `parser_evidence_confidence_claim_vocabulary.md` prevents intermediate
  evidence states from being upgraded into parser truth, fixture promotion, or
  readiness.

## Problem Statement And First Bad Values

First bad value:

```text
EventBus gap or suspect delivery signal
  -> no post-session replay audit boundary
  -> future recovery workflow may improvise from private logs
```

Why it is bad: EventBus diagnostics can identify a delivery concern, but the
repo needs a reviewed boundary before any private `Player.log` or `UTC_Log`
evidence is used to audit or recover from that concern.

Second bad value:

```text
replay audit result
  -> treated as corrected live parser truth
```

Why it is bad: replay can help review a past session, but it must not become
the primary live truth path, rewrite parser state, backfill workbook/webhook
outputs, or prove parser correctness.

Third bad value:

```text
UTC_Log replay evidence
  -> treated as a second live parser source
```

Why it is bad: `UTC_Log` can only be an optional, separately authorized,
post-session evidence source. It must not bypass the normal `Player.log` parser
path or the #381 source-adapter boundary.

Fourth bad value:

```text
audit report generated
  -> fixture promotion or corpus status movement implied
```

Why it is bad: audit reports are review evidence. Fixture promotion, corpus
metadata updates, and expected-output changes require their own contracts,
human review, validation, and Codex E/F/G path.

Fifth bad value:

```text
private replay run
  -> public artifact includes raw path, raw line, offset, hash, or private note
```

Why it is bad: post-session audit sits directly beside local private evidence.
All public output must be symbolic, bucketed, redacted, or fail-closed.

## Scope Decision

In scope for this contract:

- post-session replay audit vocabulary;
- source precedence rules for live parser output, `Player.log`, and optional
  `UTC_Log`;
- allowed and forbidden input classes;
- public-safe audit report shape expectations;
- human review and recovery-candidate routing;
- relationship to #460, #471, #467, #468, #469, #470, and #472;
- relationship to #381, #382, #388, #434, saved-event replay, and golden
  replay;
- validation expectations for any later implementation.

Out of scope:

- implementing code;
- reading or running private `Player.log`;
- reading or running private `UTC_Log`;
- reading app-data, live MTGA data, network data, diagnostics, workbook
  exports, SQLite databases, runtime artifacts, or private smoke outputs;
- running replay audit;
- normalizing private `UTC_Log`;
- creating replay reports, recovery packets, fixtures, manifests, expected
  outputs, corpus metadata diffs, runtime artifacts, or PR-assist artifacts;
- changing EventBus behavior;
- implementing sequence IDs or gap detection;
- changing parser facts, parser event classes, parser state final
  reconciliation, match identity, game identity, or deduplication;
- changing workbook, webhook, API, Apps Script, analytics, AI, CI, deploy, or
  production behavior;
- claiming reliability readiness, parser truth, fixture-promotion readiness,
  corpus readiness, release readiness, deploy readiness, production readiness,
  analytics truth, AI truth, or coaching truth.

## Source Precedence

The future audit workflow must preserve this source order:

1. Live parser/runtime path
   - Primary parser path.
   - Owns live parser processing and normalized parser facts.
   - May produce EventBus diagnostic signals if future sequence/gap work is
     separately implemented.
2. Raw `Player.log`
   - Primary observable post-session source for local private audit when
     explicitly authorized.
   - Local/private by default.
   - Not committed unless reduced to reviewed sanitized fixtures under separate
     fixture-promotion authority.
3. Optional `UTC_Log`
   - Secondary local evidence source only.
   - Must pass through the #381 source-adapter boundary or a later approved
     successor.
   - Never a second live parser truth path.
4. Committed sanitized fixtures and golden replay manifests
   - Public regression evidence only after separate fixture review and merge.
   - Not a substitute for private audit authorization.
5. Workbook, webhook, API, analytics, AI, and coaching outputs
   - Downstream consumers only.
   - Must not be used to correct parser truth.

## Audit Trigger Vocabulary

Allowed future `audit_trigger` values:

- `event_bus_gap_detected`
- `event_bus_duplicate_detected`
- `event_bus_out_of_order_detected`
- `event_bus_external_cancellation`
- `event_bus_close_path_review`
- `queue_pressure_review`
- `worker_queue_review`
- `manual_operator_review`
- `golden_replay_diff_review`
- `harvest_candidate_review`
- `unknown_trigger_fail_closed`

These values are review triggers only. They do not authorize private evidence
reads, replay execution, parser behavior changes, fixture promotion, corpus
status changes, runtime artifact creation, or readiness claims.

Forbidden trigger labels:

- `parser_truth_failed`
- `parser_truth_confirmed`
- `private_replay_authorized`
- `recovery_authorized`
- `fixture_promotion_authorized`
- `corpus_update_authorized`
- `reliability_ready`
- `production_safe`

## Audit Status Vocabulary

Allowed future `audit_status` values:

- `audit_not_authorized`
- `audit_contract_only`
- `audit_candidate`
- `audit_blocked_missing_authority`
- `audit_blocked_private_input`
- `audit_blocked_unsafe_output`
- `audit_blocked_source_conflict`
- `audit_blocked_unsupported_claim`
- `audit_private_local_only`
- `audit_sanitized_summary_only`
- `audit_inconclusive`
- `audit_review_required`
- `audit_recovery_candidate`
- `audit_deferred`
- `audit_rejected`
- `audit_unknown_fail_closed`

Status meanings:

- `audit_not_authorized`: no replay audit may run.
- `audit_contract_only`: this document or a successor defines vocabulary only.
- `audit_candidate`: a public-safe diagnostic signal suggests an audit might be
  useful.
- `audit_blocked_missing_authority`: required issue, approval, or private gate
  is absent.
- `audit_blocked_private_input`: required input is private/local and not
  authorized.
- `audit_blocked_unsafe_output`: output would echo raw/private material.
- `audit_blocked_source_conflict`: source precedence or evidence conflicts
  require review before continuing.
- `audit_blocked_unsupported_claim`: requested output would overclaim truth,
  readiness, assurance, fixture promotion, or recovery authority.
- `audit_private_local_only`: a future authorized run may remain local/private
  and must not create public committed evidence.
- `audit_sanitized_summary_only`: only symbolic or redacted public summary is
  allowed.
- `audit_inconclusive`: evidence does not support a stronger claim.
- `audit_review_required`: human/Codex review is required before any next step.
- `audit_recovery_candidate`: a reviewed, public-safe candidate exists for a
  later scoped recovery or fixture/corpus issue.
- `audit_deferred`: audit or recovery is intentionally postponed.
- `audit_rejected`: the candidate is rejected for the scoped concern.
- `audit_unknown_fail_closed`: input or state is unclear and must not proceed.

## Recovery Vocabulary

Allowed future `recovery_route` values:

- `no_recovery`
- `human_review_only`
- `parser_bug_issue_candidate`
- `fixture_candidate_review`
- `corpus_metadata_review`
- `confidence_degradation_review`
- `golden_replay_fixture_review`
- `eventbus_followup_issue_candidate`
- `blocked_private_evidence`
- `blocked_unsupported_claim`
- `unknown_fail_closed`

Recovery route meanings:

- `no_recovery`: no follow-up action is supported.
- `human_review_only`: review may inspect public-safe summaries but no artifact
  or parser change follows automatically.
- `parser_bug_issue_candidate`: a later problem representation may be drafted
  for a parser bug, but no issue is created by this contract.
- `fixture_candidate_review`: a later fixture-promotion workflow may review a
  candidate, but no fixture is created or promoted here.
- `corpus_metadata_review`: a later corpus workflow may review metadata impact,
  but no manifest/session-ledger mutation is authorized.
- `confidence_degradation_review`: a later contract may review whether scoped
  confidence/finality labels should degrade.
- `golden_replay_fixture_review`: a later golden replay workflow may consider a
  sanitized fixture.
- `eventbus_followup_issue_candidate`: a later EventBus issue may be proposed.
- `blocked_private_evidence`: required source evidence remains private or
  unauthorized.
- `blocked_unsupported_claim`: requested recovery would overclaim or mutate a
  protected surface.
- `unknown_fail_closed`: recovery path is unclear and must stop.

Forbidden recovery behavior:

- automatic parser fact rewrite;
- automatic EventBus replay into live subscribers;
- automatic workbook row repair;
- automatic webhook resend;
- automatic Apps Script, API, analytics, AI, or coaching changes;
- automatic fixture creation or expected-output update;
- automatic corpus status movement;
- automatic GitHub issue, PR, branch, commit, tracker, or label mutation;
- readiness, truth, release, deploy, production, analytics, AI, or coaching
  claims.

## Private Input Refusal And Future Authority Boundary

This contract does not authorize private inputs. It only defines the exact
refusal boundary for issue #473 and the minimum topics a later execution
contract must define before a private input can be considered.

Issue #473 is not an execution issue. It is a contract-boundary issue. It must
not be used as the authority record for reading private `Player.log`, reading
private `UTC_Log`, running replay audit, or creating local replay artifacts.

For issue #473 and for any implementation directly routed from this contract,
private inputs are always blocked. A later private/local replay-audit execution
must start from a separate future issue and a separate reviewed contract whose
stated purpose is the bounded private/local replay-audit execution or no-write
preflight. That future issue must be distinct from #473, active at the time of
execution, name the private source class, name the operation, name the
local-only artifact policy, and preserve no-echo rules. A future Codex C or D
implementation prompt is not sufficient unless it cites that separate reviewed
execution contract and explicit human approval.

Private input authority must be explicit, current, scoped, and bound to the
operation. It is not inherited from:

- this contract existing;
- issue #473 existing;
- parent private-evidence issue #434 existing;
- tracker #388 existing;
- any completed predecessor issue or PR;
- the #381 `UTC_Log` adapter boundary;
- the #382 harvest candidate boundary;
- a generic "authorization granted" note without scoped source and operation
  metadata;
- a caller-provided boolean such as `private_log_read_authorized=true`;
- a local path, file name, or private source pointer.

Valid `authority_status` values for issue #473 packets:

- `authority_not_required_public_safe`
- `authority_missing_required`
- `authority_private_execution_out_of_scope`
- `authority_ambiguous_fail_closed`

No issue #473 packet may use a status that claims private execution authority.

Reserved future execution-contract fields, not authority in issue #473:

```yaml
authority_ref: "public-safe issue/comment/contract/handoff reference"
authority_status: "authority_bound_execution_issue"
authority_execution_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/<number>"
authority_execution_contract: "repo-relative contract path"
authority_operation: "post_session_private_player_log_audit"
authority_source_class: "private_player_log_window"
authority_target_artifact_family: "event_bus_post_session_replay_audit"
authority_target_repository: "Tahjali11/Mythic-Edge"
authority_privacy_mode: "local_private_only"
authority_no_echo_required: true
authority_expiration_condition: "single scoped run, issue closure, or explicit revocation"
authorized_by: "human_owner_or_named_review_gate"
```

Reserved future `authority_status` values, forbidden as authority in issue #473:

- `authority_bound_execution_issue`
- `authority_bound_private_local_execution_issue`
- `authority_expired`
- `authority_revoked`
- `authority_stale`
- `authority_superseded`
- `authority_mismatched_issue`
- `authority_mismatched_contract`
- `authority_mismatched_operation`
- `authority_mismatched_source_class`
- `authority_mismatched_repository`

Reserved future private `authority_operation` values, forbidden as authority in
issue #473:

- `post_session_private_player_log_audit`
- `post_session_private_utc_log_audit`
- `post_session_private_replay_comparison`
- `post_session_private_sanitized_summary_review`

Reserved future private `authority_source_class` values, forbidden as authority
in issue #473:

- `private_player_log_window`
- `private_normalized_utc_log_window`
- `private_local_replay_summary`

Authority validation rules:

- Public-safe diagnostics, committed sanitized fixtures, and synthetic tests may
  use `authority_not_required_public_safe`.
- Any private `Player.log`, private `UTC_Log`, private local replay summary, or
  local-only reduced comparison inside issue #473 must produce
  `authority_private_execution_out_of_scope`, `authority_missing_required`, or
  `authority_ambiguous_fail_closed`.
- The execution issue, execution contract path, operation, source class, target
  artifact family, repository, and expiration condition must all match the
  requested input in the later execution contract, not in issue #473.
- The execution issue must not be #473.
- Parent issue #434 may be a prerequisite gate, but it is not sufficient by
  itself.
- Issue #381 may authorize adapter shape, but it is not sufficient authority to
  read a private `UTC_Log` source.
- Issue #382 may authorize candidate-report shape, but it is not sufficient
  authority to read private evidence.
- Stale, closed, expired, revoked, superseded, mismatched, invented, ambiguous,
  or caller-supplied-only authority must fail closed.
- A Boolean authority flag must be treated as an output assertion to verify,
  never as input authority to trust.
- Failed authority checks must produce `audit_blocked_missing_authority`,
  `audit_blocked_private_input`, or `audit_unknown_fail_closed` without echoing
  the private source hint.

## Allowed Inputs

Allowed in this Codex B pass:

- public repo docs and source files;
- public GitHub issue and PR metadata;
- current EventBus contracts and tests;
- existing public-safe parser-evidence contracts.

Allowed future public-safe inputs:

- #472-compatible in-memory continuity snapshots or public-safe reason
  categories;
- #467-compatible queue pressure snapshots;
- #471-compatible consumer ids and classes;
- public-safe parser-owned reduced summaries;
- committed sanitized fixtures and golden replay manifests;
- synthetic `Player.log` or synthetic `UTC_Log` strings in tests;

Blocked private source-class labels for refusal only:

- explicit operator-selected local `Player.log` windows with authority source
  class `private_player_log_window`;
- explicit operator-selected local `UTC_Log` windows normalized under the #381
  adapter or a later approved successor, with authority source class
  `private_normalized_utc_log_window`;
- local-only reduced replay summaries that pass no-echo checks and use source
  class `private_local_replay_summary`.

These classes are not allowed by this contract. They are listed only so issue
#473 artifacts can refuse them consistently without echoing private hints. They
are not pre-approved future inputs. A later execution issue that is distinct
from #473 may define them as inputs only through its own reviewed contract.
They must remain local/private unless that later execution contract and review
prove a sanitized public summary is safe.

## Forbidden Inputs

This contract, its examples, future public reports, and any future
implementation must not read, copy, hash, summarize, echo, or commit:

- private raw `Player.log` content;
- private raw `UTC_Log` content;
- raw log lines or raw JSON payload bodies;
- raw event payloads;
- exact private paths;
- source hashes from private files;
- exact private offsets, byte ranges, file sizes, or timestamp windows;
- app-data contents;
- live MTGA state;
- network, firewall/drop, packet, OS/router, or diagnostics data;
- private smoke outputs;
- runtime status files from a real run;
- failed posts;
- workbook exports;
- generated SQLite databases;
- generated card/tier data;
- decklists, sealed pools, draft picks, strategy notes, screenshots, or private
  operator notes;
- secrets, credentials, tokens, API keys, webhook URLs, or model/provider
  outputs.

## Public-Safe Audit Packet Shape

A future public-safe packet, if separately authorized, should use this logical
shape. Packet-shape or packet-writing authorization is not private-input
authority. Under issue #473, the packet must either use public-safe inputs or
record a fail-closed refusal; it must not read private logs or run replay
audit.

```yaml
object: "mythic_edge_event_bus_post_session_replay_audit"
schema_version: "event_bus_post_session_replay_audit.v1"
audit_id: "symbolic-public-safe-id"
contract_source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/473"
execution_issue: null
audit_status: "audit_candidate"
audit_trigger: "event_bus_gap_detected"
source_precedence:
  live_parser_primary: true
  player_log_primary_post_session_source: true
  utc_log_secondary_optional_source: true
input_summary:
  live_diagnostic_refs: []
  private_source_refs: []
  committed_fixture_refs: []
  raw_private_input_included: false
  raw_path_included: false
  raw_hash_included: false
  raw_content_included: false
authority:
  authority_status: "authority_missing_required"
  authority_ref: null
  authority_execution_issue: null
  authority_execution_contract: null
  authority_operation: null
  authority_source_class: null
  authority_target_artifact_family: "event_bus_post_session_replay_audit"
  authority_target_repository: "Tahjali11/Mythic-Edge"
  authority_no_echo_required: true
comparison_summary:
  comparison_status: "comparison_not_run"
  affected_consumer_class: "truth_critical"
  affected_scope: "symbolic-session-or-window"
  reason_categories: []
review:
  review_status: "human_review_required"
  recovery_route: "human_review_only"
authorization_flags:
  implementation_authorized: false
  private_log_read_authorized: false
  replay_audit_authorized: false
  fixture_promotion_authorized: false
  corpus_status_mutation_authorized: false
  eventbus_behavior_change_authorized: false
  parser_behavior_change_authorized: false
  runtime_artifact_creation_authorized: false
  ci_change_authorized: false
non_claims:
  - "not_parser_truth"
  - "not_reliability_readiness"
```

The packet shape is a future logical contract only. This Codex B pass does not
create packets or authorize durable packet files.

## Comparison Vocabulary

Allowed future `comparison_status` values:

- `comparison_not_run`
- `comparison_not_authorized`
- `comparison_blocked_private_input`
- `comparison_blocked_unsafe_output`
- `comparison_synthetic_only`
- `comparison_private_local_only`
- `comparison_sanitized_summary_only`
- `comparison_no_difference_observed`
- `comparison_difference_observed`
- `comparison_inconclusive`
- `comparison_review_required`
- `comparison_unknown_fail_closed`

Allowed future reason categories:

- `eventbus_gap_signal`
- `eventbus_duplicate_signal`
- `eventbus_out_of_order_signal`
- `external_cancellation_signal`
- `close_path_signal`
- `queue_pressure_signal`
- `worker_queue_pressure_signal`
- `late_subscriber_baseline`
- `source_precedence_conflict`
- `player_log_window_unavailable`
- `utc_log_window_unavailable`
- `utc_log_adapter_required`
- `private_source_not_authorized`
- `sanitization_required`
- `fixture_promotion_required_later`
- `corpus_metadata_review_required`
- `parser_bug_review_required`
- `unsupported_claim`

Forbidden comparison outputs:

- raw lines;
- raw payload objects;
- exact local paths;
- exact private offsets or byte ranges;
- exact private source hashes;
- workbook row payloads from private sessions;
- webhook replay payloads;
- AI/model interpretation;
- hidden-card or gameplay-advice conclusions.

## Privacy And No-Echo Rules

All future public-facing audit material must be no-echo.

No-echo means public output may include:

- symbolic source references;
- public issue/PR links;
- repo-relative paths for committed sanitized files;
- consumer ids from the approved EventBus classification vocabulary;
- public-safe status labels;
- bucketed or synthetic counts;
- reason categories;
- non-claim flags.

No-echo means public output must not include:

- raw private log text;
- exact private file paths;
- private line contents;
- private source hashes;
- exact private offsets, byte ranges, or timestamp windows;
- local machine names or user names;
- secrets, tokens, keys, credentials, or webhook URLs;
- private deck, draft, sideboard, card-choice, strategy, or operator-note
  content.

If a future helper cannot produce a public-safe summary without echoing private
material, it must return `audit_blocked_unsafe_output` or
`comparison_blocked_unsafe_output`.

## Relationship To EventBus Contracts

Issue #460:

- Backpressure completeness remains the core delivery invariant.
- Replay audit must not authorize dropping, sampling, coalescing, or repairing
  live EventBus delivery.

Issue #471:

- Audit reports must consume the approved consumer classification vocabulary.
- `truth_critical`, `mixed`, and `unknown` consumers require fail-closed review
  before any recovery route.
- Audit reports must not reclassify consumers.

Issue #467:

- Queue pressure metrics are diagnostic only.
- Metrics may help select an audit candidate, but they do not authorize replay
  execution or recovery.

Issue #468:

- Capacity changes remain separate.
- Audit results must not auto-tune EventBus capacity.

Issue #469:

- Fanout changes remain separate.
- Audit results must not authorize concurrent fanout behavior changes.

Issue #470:

- Worker queues remain separate.
- Audit results must not move heavy work into queues or create durable retry
  queues.

Issue #472:

- Sequence/gap diagnostics, if later implemented, may trigger audit
  consideration.
- Sequence/gap diagnostics are not replay authorization.
- Audit must not require parser event class changes or `Subscriber.recv()`
  return-type changes.

## Relationship To Parser Evidence Contracts

Issue #381 / UTC_Log source adapter:

- `UTC_Log` is optional secondary evidence.
- Private `UTC_Log` handling must go through the #381 adapter boundary or a
  later approved successor.
- `UTC_Log` must not become a second live parser path.

Issue #382 / harvest candidate reports:

- Audit candidates may feed a later harvest candidate review.
- Candidate metadata is advisory and does not authorize fixture promotion or
  parser changes.

Tracker #388 and parent #434:

- Private evidence execution requires a scoped private-evidence gate.
- This contract does not activate #388, #381, #382, or private harvest.
- This contract does not clear pipeline activation readiness.

Saved event replay:

- Saved-event replay is generated JSONL replay and not raw `Player.log` replay.
- It may be useful as a public-safe test surface, but it does not prove raw log
  parsing behavior.

Golden replay:

- Golden replay consumes committed sanitized fixtures.
- A post-session audit may recommend a later sanitized fixture review, but it
  must not create or update fixtures by itself.

Confidence-claim vocabulary:

- Audit statuses must not be upgraded into `coverage_confirmed`, parser truth,
  fixture truth, private smoke success, corpus readiness, or release readiness.

## Error Behavior

Missing replay authority:

- return or record `audit_blocked_missing_authority`;
- classify the issue #473 packet authority as `authority_missing_required`,
  `authority_private_execution_out_of_scope`, or
  `authority_ambiguous_fail_closed`;
- do not emit reserved future execution-contract statuses such as
  `authority_mismatched_*`, `authority_expired`, `authority_revoked`,
  `authority_stale`, or `authority_superseded` from issue #473 artifacts;
- do not read private sources;
- do not create local or public artifacts.

Private source required but not authorized:

- return or record `audit_blocked_private_input`;
- do not print the private path or source hint;
- preserve `private_log_read_authorized=false`.

Unsafe output risk:

- return or record `audit_blocked_unsafe_output`;
- redact nothing silently if the remaining report would be misleading;
- prefer fail-closed over partial public output.

Source conflict:

- return or record `audit_blocked_source_conflict` or `audit_review_required`;
- do not choose `Player.log`, `UTC_Log`, workbook, or analytics truth by
  convenience;
- route to human review.

Unsupported recovery request:

- return or record `audit_blocked_unsupported_claim`;
- preserve all protected-surface false flags.

Unknown status:

- return or record `audit_unknown_fail_closed`;
- stop before replay execution or recovery routing.

## Side Effects

Allowed side effects in this Codex B pass:

- write this contract file only.

Forbidden side effects in this Codex B pass:

- no code implementation;
- no PR creation;
- no private log reads;
- no replay execution;
- no runtime artifact creation;
- no fixture creation or promotion;
- no corpus metadata edits;
- no EventBus behavior changes;
- no parser behavior changes;
- no parser event class changes;
- no workbook, webhook, API, Apps Script, analytics, AI, CI, deploy, release, or
  production changes.

Future side effects, if separately authorized, must be explicitly named by a
new issue/contract and must remain local-only or public-safe as appropriate.

## Compatibility

This contract preserves:

- existing `EventBus` public method names;
- existing `Subscriber.recv() -> GameEvent | None` behavior;
- existing queue pressure snapshot semantics;
- existing consumer classification vocabulary;
- existing parser event classes;
- existing parser state final reconciliation;
- existing saved-event replay boundary;
- existing golden replay fixture safety boundary;
- existing UTC_Log adapter boundary;
- existing private-evidence gates.

If future implementation requires changing any of these, stop and route back to
Codex B.

## Validation Expectations For Later Implementation

A later implementation, if separately authorized, should provide deterministic
public-safe evidence that:

- audit authority flags default to false;
- private source inputs are rejected without authority;
- stale, closed, expired, revoked, superseded, mismatched, invented,
  ambiguous, or caller-supplied-only authority is rejected without reading the
  private source;
- #473, #381, #382, #388, and #434 are treated as prerequisite or adjacent
  governance only, not private input authority by themselves;
- unsafe output is rejected without echoing raw/private values;
- `Player.log` remains the primary post-session raw evidence source;
- `UTC_Log` remains optional and secondary;
- EventBus diagnostics are treated as audit triggers only;
- consumer classifications are copied, not reclassified;
- recovery routes do not mutate parser facts or protected surfaces;
- public reports include required non-claims;
- public reports never include raw event payloads, private paths, private
  offsets, source hashes, secrets, or raw log lines;
- existing EventBus tests still pass;
- saved-event replay and golden replay boundaries are not weakened.

Suggested future validation commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_event_bus_queue_pressure_metrics.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_saved_event_replay.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
git diff --check
```

If a future implementation adds a dedicated audit helper, add a focused test
file before broader parser or replay tests.

## Acceptance Criteria

- This contract defines post-session replay audit purpose, source precedence,
  private input authority rules, privacy boundaries, comparison vocabulary,
  review routing, and recovery vocabulary.
- The contract keeps live parser/runtime delivery as the primary parser path.
- The contract keeps replay audit unauthorized in this Codex B pass.
- The contract keeps private `Player.log` and `UTC_Log` reads unauthorized.
- The contract states that issue #473 is a boundary issue and cannot authorize
  private input execution; later private replay execution requires a separate
  future issue, a separate reviewed execution contract, and explicit human
  approval.
- The contract fails closed for missing, stale, revoked, expired, superseded,
  mismatched, invented, ambiguous, or caller-supplied-only authority.
- The contract defines no-echo behavior for public artifacts.
- The contract preserves EventBus, parser, workbook, webhook, API, Apps Script,
  analytics, AI, CI, fixture, and corpus protected surfaces.
- The contract preserves `reliability_readiness_claimed=false` and
  `parser_truth_claimed=false`.
- The contract routes next work to Codex E review, not implementation.

## Stop Conditions

Stop and route back to Codex B if later work requires:

- reading private `Player.log` or `UTC_Log`;
- normalizing private `UTC_Log`;
- running replay audit;
- creating durable audit reports or recovery packets;
- creating fixtures, manifest drafts, expected outputs, proof objects, or
  corpus metadata diffs;
- changing parser behavior;
- changing parser event classes;
- changing parser state final reconciliation, match identity, game identity, or
  deduplication;
- changing EventBus behavior, sequence IDs, gap detection, capacity, fanout, or
  worker queues outside their own approved contracts;
- changing workbook, webhook, API, Apps Script, analytics, AI, CI, deploy,
  release, or production behavior;
- making recovery, parser truth, reliability readiness, fixture-promotion
  readiness, corpus readiness, release readiness, deploy readiness, production
  readiness, analytics truth, AI truth, or coaching truth claims.

## Recommended Next Role

Recommended next role: Codex E.

Codex E should review this contract against issue #473, the completed EventBus
contract chain, the parser evidence contracts, and current EventBus code. Codex
E should route back to Codex B if the source precedence, privacy/no-echo rules,
audit status vocabulary, or recovery boundary is ambiguous.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic-Edge issue #473.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/473

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source artifact:
docs/contracts/event_bus_post_session_replay_audit_recovery.md

Review the EventBus post-session replay audit and recovery contract against
#460, #471, #467, #468, #469, #470, #472, parser evidence contracts, and
current EventBus code. Specifically verify that `EVENTBUS-REPLAY-E-001` is
resolved: issue #473 must not authorize private input reads or replay
execution, and any future private/local execution must require a separate
future issue and separate reviewed execution contract.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not read private Player.log or UTC_Log files.
- Do not run replay audit.
- Do not create runtime artifacts, fixtures, expected outputs, corpus metadata
  diffs, recovery packets, issues, or PRs.
- Do not change EventBus behavior, parser behavior, parser event classes, API
  payloads, workbook/webhook payloads, Apps Script behavior, analytics, AI, CI,
  deploy, release, or production behavior.
- Do not claim reliability readiness, parser truth, fixture-promotion readiness,
  corpus readiness, release readiness, deploy readiness, production readiness,
  analytics truth, AI truth, or coaching truth.

Expected output:
- Findings first, ordered by severity.
- Whether the contract is ready for Codex F or must return to Codex B.
- Validation expectations.
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/472"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/661"
  latest_merge_commit: "48da1214fbd2adb1ce47d442711dca2807ebb59b"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/473"
  completed_thread: "B"
  next_thread: "E"
  finding_id: "EVENTBUS-REPLAY-E-001"
  verdict: "private_input_boundary_conflict_resolved_ready_for_review"
  target_artifact: "docs/contracts/event_bus_post_session_replay_audit_recovery.md"
  phase_4_closeout_ready: false
  phase_4_remaining_blocker: "issue_473_contract_review_submission_merge"
  risk_tier: "High"
  implementation_authorized: false
  private_log_read_authorized: false
  replay_audit_authorized: false
  fixture_promotion_authorized: false
  corpus_status_mutation_authorized: false
  sequence_id_implementation_authorized: false
  gap_detection_implementation_authorized: false
  eventbus_behavior_change_authorized: false
  parser_behavior_change_authorized: false
  parser_event_class_change_authorized: false
  api_payload_change_authorized: false
  workbook_webhook_change_authorized: false
  runtime_artifact_creation_authorized: false
  ci_change_authorized: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
```
