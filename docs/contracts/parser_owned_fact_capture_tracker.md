# Parser-Owned Fact Capture Tracker Contract

## Module

`parser_owned_fact_capture_tracker`

Plain English: this contract defines the fact-level scoreboard for the local
harvest-to-golden-fixture workflow. The tracker may describe which
parser-owned facts are current capture targets, which are deferred, which were
privately captured, which became review candidates, which were approved, and
which were later promoted into sanitized golden replay fixtures.

The tracker is not a raw-log reader, source adapter, harvest runner, review
packet generator, fixture-promotion tool, corpus metadata mutator, parser
behavior change, or truth approver.

This Codex B pass writes only this contract. It does not implement code, open
a PR, activate #388 or #381, read private logs, run private harvest, write
local/private artifacts, create fixtures, edit corpus metadata, or claim
readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/481
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/465
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/549
- Previous merge commit: `ace067d3491565b2825a4c2c9fa1777a9c87ce30`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- The primary checkout was on a gone #455 branch with an unrelated modified
  `docs/project_roadmap.md` edit.
- To preserve unrelated local work, this contract was written in a clean
  sibling worktree on branch
  `codex/parser-owned-fact-capture-tracker-481`.
- The clean worktree was created from `origin/main`.
- `HEAD` was `ace067d3491565b2825a4c2c9fa1777a9c87ce30`.
- Issue #481 was open.
- Pipeline tracker #388 was open and inactive.
- Issue #381 remained inactive.
- Parent private-evidence issue #434 was open.
- Issue #465 was closed and PR #549 was merged.

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Tracker #388 remains open and inactive. This contract does not activate #388
or #381.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- Issue #481 and Codex A reconciliation comment
- Pipeline tracker #388
- Parent private-evidence issue #434
- Issue #465 and PR #549
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md`
- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `docs/contracts/parser_recovery_human_approved_parser_corpus_update_workflow.md`
- `docs/contract_test_reports/repo_extraction_candidate_matrix.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`
- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py`
- `src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- Focused existing tests for harvest, recovery, fixture, corpus, and live
  parser-owned fact capture surfaces by inspection.

No private `Player.log`, `UTC_Log`, app-data, live MTGA, network,
firewall/drop, packet, OS/router, diagnostics, drift, watcher, tailer, private
smoke, or private harvest evidence was run, tailed, hashed, copied,
summarized, or read.

## Stale Start-Condition Reconciliation

Issue #481's original body refers to an older #158 synthetic-or-stronger start
condition. Current controlling state supersedes that wording for
planning/contract work:

- #158 is closed as classification/report-preconditions complete.
- #516 amended #388 activation criteria.
- #518 added the parser evidence-pipeline planning umbrella.
- #388 remains open and inactive.
- #381 remains inactive.
- `parser_behavior_ready=false`.
- `pipeline_activation_ready_for_issue_388=false`.
- `private_harvest_authorized=false`.
- `fixture_promotion_authorized=false`.
- `corpus_status_change_authorized=false`.

This contract may proceed as planning and schema work only. It does not start
private harvest, implementation, fixture promotion, corpus status movement,
parser behavior changes, or readiness claims.

## Observed Current Behavior

The #388 evidence-pipeline chain now has public-safe planning and in-memory
support surfaces for:

- #381 `UTC_Log` source-adapter boundary;
- #382 local harvest candidate summaries;
- #383 harvest review packets;
- #384 fixture promotion proof objects;
- #386 corpus metadata diff objects;
- #385 golden replay fixture and manifest draft packets;
- #387 reviewed fixture-promotion PR-assist packets.

The recovery planning chain now has public-safe planning and in-memory support
surfaces for:

- #451 field recovery matrix;
- #452 local watcher / offset-window monitor;
- #453 field-evidence comparison report;
- #454 recovery candidate packet generator;
- #455 issue/fixture/manifest draft generator;
- #456 human-approved parser/corpus update workflow.

The current `field_recovery_matrix` implementation can build a default
planning matrix with 8 seed rows across these field families:

- `match`;
- `queue`;
- `game`;
- `analytics`;
- `deck_state`;
- `runtime_health`;
- `gameplay_action`.

The existing `live_app_parser_owned_fact_capture_sqlite` slice is a different
boundary. It writes final/reconciled parser-owned match/game facts into local
SQLite for the local app. It is not a capture-campaign scoreboard, not a
private harvest ledger, and not fixture promotion.

There is no dedicated parser-owned fact target matrix, session capture ledger,
coverage progress report, tracker module, tracker CLI, focused test file, or
committed synthetic tracker fixture for issue #481.

## Problem Statement

Mythic Edge can now create review-only evidence objects, proof objects,
metadata diffs, draft packets, recovery packets, and human approval records.
What is missing is a durable fact-level scoreboard that answers:

- which parser-owned facts matter in the current competitive capture scope;
- which facts are deferred for later feature-expansion campaigns;
- which private sessions captured evidence for each fact;
- which captures generated candidate summaries;
- which candidates became review packets;
- which review packets were approved, rejected, or deferred;
- which candidates have proof or draft metadata;
- which approved facts were promoted to sanitized golden fixtures;
- which facts are confirmed on Windows, macOS, or both;
- which high-value facts remain missing.

Without this tracker, the project can produce evidence artifacts but cannot
easily see coverage progress, duplication, noisy captures, platform gaps, or
next capture priorities.

## First Bad Value

The first bad value is any target-matrix row, session-ledger row, progress
report section, command output, local artifact, handoff, or next-role prompt
that implies any of the following without a later explicit issue, contract,
review, validation, and approval:

- private logs may be read;
- a private capture is approved;
- a candidate is parser truth;
- a reviewer decision promotes a fixture;
- corpus metadata may be edited;
- parser behavior may change;
- #388 or #381 is active;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`;
- `private_harvest_authorized=true`;
- `fixture_promotion_authorized=true`;
- `corpus_status_change_authorized=true`;
- release, deploy, production, analytics, AI, or coaching readiness is true.

## Scope Decision

This contract approves a future metadata-only tracker implementation boundary,
but does not implement it in Codex B.

If later explicitly authorized, Codex C may implement deterministic target
matrix, session capture ledger, and coverage progress report helpers using
synthetic fixtures and supplied public-safe/in-memory objects. Codex C may not
read private logs or execute private harvest.

The narrowest acceptable future implementation may include:

- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`;
- `tests/test_parser_owned_fact_tracker.py`;
- synthetic test fixtures under `tests/fixtures/parser_owned_fact_tracker/`;
- an implementation handoff under
  `docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md`;
- no real private source reads;
- no real private ledger writes in tests;
- no fixture creation;
- no corpus metadata edits;
- no parser behavior changes.

The command surface in this contract is an interface and safety contract. It
does not mean Codex B ran commands or that Codex C may operate on real private
sources by default. Any future local-private execution still requires explicit
approval naming the source class, artifact class, and privacy boundary.

## Owning Layer

Primary owner: Corpus / Provenance.

Supporting owners:

- Quality / Governance, for lifecycle state, role routing, validation,
  privacy gates, and false readiness flags.
- Parser, as the truth owner for parser-owned facts listed in the target
  matrix.
- Generated / Local Artifacts, for any future private session ledger,
  coverage snapshots, candidate summaries, and local-only reports.

Analytics, local app, workbook/transport, Apps Script, AI, and coaching
surfaces are consumers only. They must not become truth owners for this
tracker.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Quality / Governance;
- Parser;
- Generated / Local Artifacts.

This contract is not a parser behavior contract, not a live app contract, not
an analytics storage contract, not a workbook/transport contract, not an
AI/coaching contract, not a CI gate, not a merge gate, and not a
release/deploy/production readiness gate.

## Truth Owner

Truth owner for parser fact values:

- existing parser, router, events, state, models, extractors, match/game
  identity, deduplication, and final reconciliation layers.

Truth owner for recovery field identity and recovery category vocabulary:

- `docs/contracts/parser_recovery_field_recovery_matrix.md`;
- `src/mythic_edge_parser/app/field_recovery_matrix.py`;
- `tests/test_field_recovery_matrix.py`.

Truth owner for harvest candidate, review packet, proof, diff, draft, and
PR-assist object shapes:

- their existing contracts and reviewed implementations.

Truth owner for this tracker vocabulary:

- this contract;
- any later reviewed implementation handoff and contract-test report, if
  implementation is explicitly authorized.

The tracker must not own parser facts, raw source content, fixture expected
output, corpus status, private-evidence approval, analytics truth, AI truth,
coaching truth, merge readiness, deploy readiness, release readiness,
production behavior, or tracker completion.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code in Codex B.

If later implemented, the tracker is bridge support from Corpus / Provenance
and Generated / Local Artifacts into Quality / Governance reports.

Allowed future data flow:

```text
field recovery matrix + evidence pipeline objects + local-only session summaries
  -> parser-owned fact target matrix
  -> local session capture ledger
  -> coverage progress report
  -> human/Codex routing decision
```

Forbidden reverse flow:

```text
tracker row or progress report
  -/-> raw log read
  -/-> parser behavior change
  -/-> parser truth approval
  -/-> fixture promotion
  -/-> corpus status change
  -/-> GitHub issue/PR lifecycle action
  -/-> readiness, release, deploy, production, analytics, AI, or coaching truth
```

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_owned_fact_capture_tracker.md`

Potential future implementation artifacts, not created by this Codex B pass:

- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- `tests/test_parser_owned_fact_tracker.py`
- `tests/fixtures/parser_owned_fact_tracker/`
- `docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md`
- `docs/contract_test_reports/parser_owned_fact_capture_tracker.md`

Potential future local-only generated artifacts, never committed:

- `parser_owned_fact_tracker/target_matrix.v1.json`
- `parser_owned_fact_tracker/session_capture_ledger.v1.json`
- `parser_owned_fact_tracker/coverage_progress_report.latest.json`
- `parser_owned_fact_tracker/coverage_progress_report.latest.md`
- `parser_owned_fact_tracker/coverage_snapshots/*.json`
- `parser_owned_fact_tracker/coverage_snapshots/*.md`
- `harvest_sessions/*/session_summary.json`
- `harvest_sessions/*/coverage_delta.json`
- `harvest_sessions/*/remaining_targets.md`
- `harvest_sessions/*/environment_report.json`
- `harvest_sessions/*/privacy_scan.json`
- `harvest_candidates/*/candidate_summary.json`
- `harvest_candidates/*/candidate_summary.md`
- `harvest_candidates/*/parser_fact_preview.json`
- `harvest_candidates/*/redacted_context.md`
- `harvest_candidates/*/private_pointer.json`
- `harvest_candidates/*/privacy_report.json`
- `harvest_candidates/*/reviewer_decision.json`

Not owned by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- golden replay manifests;
- raw/private logs;
- local app SQLite databases;
- runtime status files;
- workbook exports;
- parser source behavior.

## Public Interface

No public runtime interface is approved in Codex B.

If later implemented, the smallest public module interface should be a
deterministic builder/validator surface over supplied public-safe or
synthetic data:

```python
build_default_fact_target_matrix(...)
validate_fact_target_matrix(matrix)
record_capture_session(matrix, ledger, session_record)
build_coverage_progress_report(matrix, ledger, *, previous_report=None)
validate_session_capture_ledger(ledger)
validate_coverage_progress_report(report)
```

Potential CLI commands, if separately implemented:

```bash
python3 -m mythic_edge_parser.app.parser_owned_fact_tracker init --private-root <private-root> --scope competitive-current
python3 -m mythic_edge_parser.app.parser_owned_fact_tracker record-session --private-root <private-root> --session-id <symbolic-session-id> --platform <windows|macos> --source-kind <source-kind> --match-type <match-type> --format <format> --candidate-summary <private-ref> --reviewer-decision <private-ref>
python3 -m mythic_edge_parser.app.parser_owned_fact_tracker report --private-root <private-root> --scope competitive-current --write-markdown
```

Optional future convenience command, not approved until #381/#382 source and
candidate surfaces are explicitly active for local-private execution:

```bash
python3 -m mythic_edge_parser.app.parser_owned_fact_tracker harvest-and-record --private-root <private-root> --source <operator-selected-source-ref> --platform <windows|macos> --label <symbolic-label> --match-scope <scope> --scope competitive-current
```

Command rules:

- `init` may create a private target matrix and empty ledger only under an
  explicit private root.
- `record-session` may ingest approved local harvest outputs and update the
  private session capture ledger.
- `report` may regenerate a coverage progress report from the target matrix
  and session ledger.
- `harvest-and-record`, if ever implemented, must delegate source reading and
  candidate generation to #381/#382 approved surfaces. It must not create a
  second raw-log reader inside the fact tracker.
- Commands must write only under an explicit private root by default.
- Commands must refuse repo-relative output paths unless the call is running
  in a synthetic test fixture mode explicitly designed for tests.
- Commands must not commit, stage, upload, hash, summarize, or expose raw
  private `Player.log` or `UTC_Log` contents.

## Target Matrix Schema

Object name:

```text
mythic_edge_parser_owned_fact_target_matrix
```

Schema version:

```text
parser_owned_fact_target_matrix.v1
```

Required top-level fields:

| Field | Meaning |
| --- | --- |
| `object` | `mythic_edge_parser_owned_fact_target_matrix` |
| `schema_version` | `parser_owned_fact_target_matrix.v1` |
| `matrix_id` | Stable symbolic matrix ID |
| `scope` | Capture scope, such as `competitive_current` |
| `created_at_utc` | UTC timestamp |
| `source_issue` | Issue #481 |
| `pipeline_tracker` | Issue #388 |
| `parent_private_evidence_issue` | Issue #434 |
| `source_matrix_refs` | Recovery matrix and contract refs used |
| `readiness_flags` | Required false readiness flags |
| `authorization_flags` | Required false authorization flags |
| `facts` | Fact target rows |
| `summary` | Counts by scope, family, lifecycle, and platform |
| `non_claims` | Required non-claims |

Required fact row fields:

| Field | Meaning |
| --- | --- |
| `fact_id` | Stable dotted ID, for example `match.match_id` |
| `display_name` | Human-readable label |
| `fact_family` | `match`, `game`, `queue`, `rank`, `participant`, `gameplay_action`, `runtime_health`, `deck_state`, `analytics`, or future reviewed family |
| `competitive_scope` | Scope vocabulary value |
| `deferred_reason` | Null or deferred reason |
| `priority` | `critical`, `high`, `medium`, `low`, or `deferred` |
| `parser_owner` | Repo-relative parser owner or contract owner |
| `source_field_recovery_matrix_row_ids` | Related #451 field IDs |
| `evidence_ledger_entry_ids` | Related evidence-ledger entries, if known |
| `required_capture_evidence` | Public-safe evidence categories required |
| `allowed_capture_sources` | Allowed source classes |
| `forbidden_capture_sources` | Forbidden source classes |
| `expected_outputs` | Parser-owned row/report surfaces affected |
| `platform_requirements` | Per-platform expectations |
| `current_lifecycle_status` | Lifecycle status vocabulary value |
| `platform_status` | Per-platform status map |
| `candidate_ids` | Candidate summary IDs, not file paths |
| `review_packet_ids` | Review packet IDs |
| `promotion_proof_ids` | Promotion proof IDs |
| `fixture_draft_ids` | Fixture/manifest draft IDs |
| `promoted_fixture_ids` | Sanitized fixture IDs after later approved promotion |
| `corpus_entry_ids` | Corpus manifest/session ledger IDs after later approved promotion |
| `known_gaps` | Public-safe gap notes |
| `next_capture_target` | Public-safe next target recommendation |
| `non_claims` | Row-level non-claims |

The target matrix may seed rows from `field_recovery_matrix`, but it must not
silently treat the current 8-row recovery matrix as complete parser-owned fact
coverage. A future implementation should expose `target_matrix_status` values
that distinguish `seed_matrix_ready`, `expanded_matrix_ready`,
`review_required`, and `invalid`.

## Scope Vocabulary

Allowed competitive-scope values:

- `competitive_current`
- `deferred_feature_expansion`
- `support_only`
- `out_of_scope_now`
- `historical_reference`
- `review_required`

Default current competitive focus:

- Traditional BO3 constructed match identity and final reconciliation.
- Draft event flow, draft deck submission, and draft-with-games evidence.
- Match/game identity.
- Event ID, format, queue, rank context, submit-deck seen, and sideboarding
  entered.
- Game results, match results, play/draw, mulligans, opening hand size, and
  turn count.
- Parser-owned match/game row facts.
- High-value competitive stress cases that affect truth, such as action
  attribution, event ordering, opponent/user concede, disconnect/reconnect,
  and safe timer evidence.

Default deferrals:

- BO1-first coverage campaigns.
- Alchemy, conjure, and spellbook coverage campaigns.
- Store, pack, inbox, crafting, collection-economy, and non-competitive API
  surfaces unless needed as support evidence.
- Hidden-card truth, opponent intent, player mistake labels, matchup
  certainty, strategic correctness, or AI coaching claims.

Allowed deferred reason values:

- `bo1_current_phase_deferred`
- `alchemy_conjure_spellbook_current_phase_deferred`
- `store_pack_inbox_crafting_non_competitive_deferred`
- `hidden_card_truth_forbidden`
- `opponent_intent_forbidden`
- `gameplay_advice_forbidden`
- `analytics_only_support`
- `requires_future_contract`
- `requires_private_evidence_approval`
- `requires_external_boundary_resolution`
- `not_applicable`

## Lifecycle Status Vocabulary

Allowed fact lifecycle statuses:

- `out_of_scope_now`
- `deferred_feature_expansion`
- `not_captured`
- `captured_private`
- `candidate_generated`
- `review_packet_created`
- `human_approved`
- `promotion_proof_ready`
- `fixture_manifest_draft_ready`
- `promoted_golden_fixture`
- `confirmed_windows`
- `confirmed_macos`
- `confirmed_cross_platform`
- `rejected_or_noisy`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `review_required`
- `invalid`

Allowed transition shape:

```text
not_captured
  -> captured_private
  -> candidate_generated
  -> review_packet_created
  -> human_approved
  -> promotion_proof_ready
  -> fixture_manifest_draft_ready
  -> promoted_golden_fixture
  -> confirmed_windows or confirmed_macos
  -> confirmed_cross_platform
```

Allowed side transitions:

- any status -> `review_required`;
- `not_captured` -> `blocked_private_evidence`;
- `not_captured` -> `blocked_external_boundary`;
- `not_captured` -> `deferred_feature_expansion`;
- `candidate_generated` -> `rejected_or_noisy`;
- `review_packet_created` -> `rejected_or_noisy`;
- `human_approved` -> `promotion_proof_ready` only after a later approved
  proof object exists;
- `promoted_golden_fixture` -> platform confirmation only after a later
  approved fixture and validation evidence exists.

Forbidden transitions:

- `captured_private` directly to `promoted_golden_fixture`;
- any status directly to `parser_behavior_ready=true`;
- any status directly to `pipeline_activation_ready_for_issue_388=true`;
- any status directly to corpus status mutation;
- any status directly to parser behavior change;
- any private or blocked status directly to public fixture promotion.

## Platform Status Handling

Supported platform keys:

- `windows`
- `macos`
- `cross_platform`

Allowed platform status values:

- `not_required`
- `not_captured`
- `captured_private`
- `candidate_generated`
- `review_packet_created`
- `human_approved`
- `promoted_fixture_confirmed`
- `confirmed`
- `rejected_or_noisy`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `unknown`

Rules:

- Windows-only or macOS-only confirmation must remain visible.
- `confirmed_cross_platform` requires both Windows and macOS confirmation or
  a later explicit contract that changes platform requirements.
- A missing platform must not be counted as confirmed.
- Private platform evidence must remain local-only unless separately
  authorized and sanitized.

## Session Capture Ledger Schema

Object name:

```text
mythic_edge_parser_owned_fact_session_capture_ledger
```

Schema version:

```text
parser_owned_fact_session_capture_ledger.v1
```

Required top-level fields:

| Field | Meaning |
| --- | --- |
| `object` | `mythic_edge_parser_owned_fact_session_capture_ledger` |
| `schema_version` | `parser_owned_fact_session_capture_ledger.v1` |
| `ledger_id` | Stable symbolic ledger ID |
| `scope` | Scope vocabulary value |
| `updated_at_utc` | UTC timestamp |
| `source_issue` | Issue #481 |
| `pipeline_tracker` | Issue #388 |
| `parent_private_evidence_issue` | Issue #434 |
| `target_matrix_ref` | Private or synthetic matrix ref |
| `sessions` | Session entries |
| `summary` | Counts by platform, source kind, lifecycle, and target facts |
| `privacy` | Public-safe privacy assertion summary |
| `readiness_flags` | Required false readiness flags |
| `authorization_flags` | Required false authorization flags |
| `non_claims` | Required non-claims |

Required session entry fields:

| Field | Meaning |
| --- | --- |
| `session_id` | Stable symbolic session ID |
| `platform` | `windows`, `macos`, or `unknown` |
| `source_kind` | Source kind vocabulary value |
| `scope` | Scope vocabulary value |
| `format_family` | Public-safe format label, such as `standard` or `limited` |
| `queue_family` | Public-safe queue label |
| `match_type` | `traditional_bo3`, `bo1`, `draft_with_games`, or reviewed value |
| `capture_started_at_utc` | Optional public-safe UTC timestamp |
| `capture_finished_at_utc` | Optional public-safe UTC timestamp |
| `source_window_ref` | Symbolic private pointer ref, not exact path/offset/hash |
| `candidate_summary_refs` | Candidate summary IDs/refs |
| `review_packet_refs` | Review packet IDs/refs |
| `reviewer_decision_refs` | Reviewer decision IDs/refs |
| `promotion_proof_refs` | Proof IDs/refs |
| `fixture_draft_refs` | Draft IDs/refs |
| `promoted_fixture_refs` | Sanitized fixture IDs/refs after later approved promotion |
| `fact_deltas` | Per-fact lifecycle deltas |
| `privacy_scan` | Public-safe summary only |
| `environment_summary` | Symbolic OS/platform summary only |
| `remaining_targets` | Public-safe next targets |
| `authorization_flags` | Required false authorization flags |
| `non_claims` | Required non-claims |

Allowed `source_kind` values:

- `synthetic_fixture`
- `synthetic_player_log`
- `synthetic_utc_log`
- `user_selected_player_log`
- `user_selected_normalized_utc_log`
- `local_harvest_candidate_summary`
- `harvest_review_packet`
- `fixture_promotion_proof`
- `golden_replay_fixture_manifest_draft`
- `corpus_metadata_diff`
- `human_approved_update_record`

Private source kinds may appear only in local-only ledgers or synthetic tests
that explicitly model a blocked/private status. They must not cause source
content reads by the tracker.

## Coverage Progress Report Schema

Object name:

```text
mythic_edge_parser_owned_fact_coverage_progress_report
```

Schema version:

```text
parser_owned_fact_coverage_progress_report.v1
```

Required top-level fields:

| Field | Meaning |
| --- | --- |
| `object` | `mythic_edge_parser_owned_fact_coverage_progress_report` |
| `schema_version` | `parser_owned_fact_coverage_progress_report.v1` |
| `report_id` | Stable symbolic report ID |
| `scope` | Scope vocabulary value |
| `generated_at_utc` | UTC timestamp |
| `target_matrix_ref` | Matrix ref |
| `session_capture_ledger_ref` | Ledger ref |
| `previous_report_ref` | Optional previous report ref |
| `summary_counts` | Counts by lifecycle, family, scope, and platform |
| `new_private_captures` | Public-safe session/fact refs only |
| `new_candidates_generated` | Candidate IDs/refs only |
| `reviewer_decisions` | Approval/rejection/deferral counts and refs |
| `promotion_progress` | Proof/draft/promoted fixture counts and refs |
| `windows_only_confirmations` | Fact refs |
| `macos_only_confirmations` | Fact refs |
| `cross_platform_confirmations` | Fact refs |
| `current_competitive_scope_gaps` | Current gaps |
| `deferred_feature_expansion_facts` | Deferred facts and reasons |
| `next_recommended_capture_targets` | Prioritized public-safe targets |
| `blocked_or_review_required` | Blocked/review-required rows |
| `privacy` | Public-safe privacy assertion summary |
| `validation` | Public-safe validation commands/status refs |
| `readiness_flags` | Required false readiness flags |
| `authorization_flags` | Required false authorization flags |
| `non_claims` | Required non-claims |

The Markdown report, if written locally, must mirror the JSON report and must
not include raw source contents, exact private paths, hashes, offsets, byte
ranges, private timestamps beyond approved symbolic UTC summary values, deck
lists, strategy notes, private notes, screenshots, workbook exports, or
secrets.

## Required False Flags

Every matrix, ledger, report, session entry, fact row, command result, and
handoff must preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
file_writing_authorized: false
issue_creation_authorized: false
pr_creation_authorized: false
```

Future Codex C may set `implementation_authorized` to true only inside the
implementation handoff for the implemented metadata-only tracker. The tracker
objects themselves must still preserve the runtime/evidence false flags above
unless a later contract explicitly changes them.

## Required Non-Claims

Every matrix, ledger, report, command output, local-only artifact, and handoff
must include or preserve:

- `not_parser_truth`
- `not_raw_log_reader`
- `not_private_harvest_authorization`
- `not_fixture_promotion`
- `not_corpus_status_change`
- `not_parser_behavior_readiness`
- `not_pipeline_activation_readiness`
- `not_release_readiness`
- `not_deploy_readiness`
- `not_production_behavior`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`
- `not_hidden_card_truth`
- `not_gameplay_advice`
- `not_player_mistake_label`
- `not_automatic_truth_approval`

## Inputs

Allowed inputs for future implementation:

- existing recovery matrix rows from `field_recovery_matrix`;
- public-safe evidence-ledger entry IDs and contract refs;
- #382 candidate summary objects supplied in memory or from synthetic fixtures;
- #383 harvest review packet objects supplied in memory or from synthetic
  fixtures;
- #384 fixture promotion proof objects supplied in memory or from synthetic
  fixtures;
- #386 corpus metadata diff objects supplied in memory or from synthetic
  fixtures;
- #385 golden replay fixture/manifest draft objects supplied in memory or from
  synthetic fixtures;
- #387 PR-assist object refs, if a later implementation exists;
- #451 through #456 recovery planning objects supplied in memory or from
  synthetic fixtures;
- committed public-safe corpus manifest and session ledger for read-only
  reference;
- synthetic target matrix and synthetic ledger fixtures;
- local-only private artifact refs that are symbolic and already produced by
  approved upstream surfaces.

Forbidden inputs:

- raw private `Player.log` or `UTC_Log` content;
- raw log lines, raw payloads, raw event bodies, raw source text, raw source
  excerpts, or raw stack traces;
- exact private paths;
- source hashes derived from private content;
- exact private offsets, byte ranges, file sizes, or local timestamps unless a
  later private-evidence contract explicitly authorizes a symbolic form;
- app-data contents;
- live MTGA data;
- network, firewall/drop, packet, OS/router, diagnostics, drift, watcher,
  tailer, private smoke, or private harvest execution output unless supplied
  as an approved public-safe summary by a separate contract;
- generated SQLite files;
- runtime status files;
- workbook exports;
- screenshots;
- decklists, deck names, card choices, sealed pools, draft pools, sideboard
  plans, strategy notes, or private notes;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  environment values.

## Outputs

Allowed future committed outputs, only if Codex C implementation is
separately authorized:

- Python metadata-only tracker module;
- synthetic tests;
- synthetic fixture examples;
- implementation handoff;
- contract-test report.

Allowed future local-only outputs, only after explicit local-private approval:

- private target matrix;
- private session capture ledger;
- private coverage progress report JSON;
- private coverage progress report Markdown;
- private coverage snapshots;
- private session summaries;
- private remaining-target summaries.

Forbidden outputs:

- raw/private logs;
- normalized private log copies;
- raw source excerpts;
- private path lists;
- raw hashes;
- exact offset/byte-range files;
- fixture files;
- golden replay manifests;
- expected-output files;
- corpus manifest edits;
- session ledger edits;
- SQLite database files;
- runtime artifacts;
- workbook exports;
- GitHub issues;
- PR branches;
- commits;
- PRs;
- tracker completion comments.

## Invariants

- The tracker is a scoreboard, not a truth owner.
- Parser facts remain owned by parser/state.
- Private capture status remains local-only until separately authorized and
  sanitized.
- A private capture must not become a fixture without review, proof, draft,
  human approval, implementation, review, submission, and deployer gates.
- BO1 and Alchemy/conjure/spellbook deferrals must be visible as deferrals,
  not counted as current competitive-core missing facts.
- Store/economy/non-competitive API facts must be visible as support-only or
  deferred unless later re-scoped.
- Hidden-card truth, opponent intent, player mistakes, strategic correctness,
  sideboarding advice, matchup certainty, AI coaching, and gameplay advice are
  forbidden fact targets.
- Platform gaps must remain visible.
- Local/private artifacts must never be committed by default.
- Exact private paths must not appear in committed docs, fixtures, reports, or
  tests.
- Tracker reports must not use `Closes` wording for #388, #381, #434, or #481
  unless a later deployer pass explicitly satisfies the relevant issue.

## Error Behavior

Future implementation must fail closed when:

- an input object has an unsupported `object` or `schema_version`;
- an input contains raw/private/source-content keys;
- a symbolic ID looks like a local path, URL, secret, token, webhook URL, or
  private filename;
- a lifecycle transition skips required review/proof/draft/promotion gates;
- a platform status claims cross-platform confirmation without both platform
  requirements satisfied;
- a deferred fact is counted as a current competitive gap;
- a report tries to set readiness or authorization flags to true;
- a command is asked to write inside the repo instead of an explicit private
  root, unless running an explicitly synthetic test-fixture mode;
- a private source kind is supplied without explicit upstream approval
  metadata.

Failure output must be sanitized and must not echo forbidden values.

## Side Effects

Allowed future Codex C side effects, if implementation is explicitly
authorized:

- create or update the tracker module;
- add synthetic tests and synthetic fixtures;
- write implementation handoff and contract-test report.

Forbidden side effects in this contract:

- reading, tailing, copying, hashing, normalizing, or summarizing private
  logs;
- starting watchers, tailers, diagnostics, drift, network, firewall/drop,
  packet, OS/router, live MTGA, or private smoke checks;
- writing local/private artifacts;
- writing fixtures or manifests;
- editing corpus metadata;
- changing parser behavior;
- changing workbook, webhook, Apps Script, Google Sheets, local app,
  analytics, OpenAI/model-provider, AI, coaching, CI, merge, deploy, or
  production behavior;
- creating GitHub issues or PRs;
- staging, committing, pushing, merging, or closing trackers.

## Dependency Order

Future implementation should proceed in this order:

1. Define schema constants and validators for the target matrix, ledger, and
   report.
2. Build a default target matrix from reviewed seed rows and explicit
   contract-owned defaults.
3. Add synthetic fixtures for matrix, session ledger, and progress report.
4. Implement ledger update from supplied synthetic/public-safe session
   entries only.
5. Implement progress report generation.
6. Add optional CLI only after pure builders and validators are covered.
7. Keep local-private command execution disabled until a later explicit
   approval names the source class and local artifact class.

## Compatibility

The tracker must preserve compatibility with:

- `field_recovery_matrix` seed row IDs and recovery categories;
- #382 candidate summary IDs and scenario family hints;
- #383 review packet IDs and reviewer decisions;
- #384 proof IDs and proof statuses;
- #386 metadata diff IDs and proposed status-transition vocabulary;
- #385 draft packet IDs;
- committed corpus manifest/session ledger schemas as read-only references;
- `live_app_parser_owned_fact_capture_sqlite` as a separate local SQLite
  ingest boundary.

The tracker must not require any existing private artifact folder to exist in
tests. Synthetic tests must use temporary paths or in-memory dictionaries.

## Tests Required

Codex B validation for this contract:

```bash
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Minimum future Codex C validation, if implementation is separately
authorized:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_field_recovery_matrix.py tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py
PYTHONPATH=src python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_golden_replay_harness.py
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
python3 tools/select_validation.py --base origin/main
git diff --check
```

Codex C must also run a focused public-artifact scan over changed files for:

- local absolute paths;
- private/live markers;
- raw log snippets;
- raw payload values;
- raw diffs;
- source patch artifacts;
- generated local artifacts;
- SQLite files;
- workbook exports;
- screenshots;
- secrets;
- tokens;
- credentials;
- API keys;
- webhook URLs;
- readiness overclaims;
- parser truth overclaims.

## Acceptance Criteria

- Contract exists at `docs/contracts/parser_owned_fact_capture_tracker.md`.
- Contract defines target matrix, session capture ledger, and progress report
  schema.
- Contract defines lifecycle statuses and allowed transitions.
- Contract defines competitive-current and deferred feature-expansion
  vocabulary.
- Contract defines Windows/macOS/cross-platform status semantics.
- Contract distinguishes #481 from #381/#382 raw source and candidate
  generation surfaces.
- Contract distinguishes #481 from the live app SQLite parser-owned fact
  capture boundary.
- Contract preserves all false readiness and authorization flags.
- Contract forbids private log reads, fixture promotion, corpus metadata
  edits, parser behavior changes, and automatic truth approval.
- Contract defines focused future validation.
- Codex B validation passes.

## Open Questions

- Should the first implementation seed only the current 8 recovery-matrix
  rows, or should Codex A/B first define a larger reviewed competitive-current
  fact list?
- Should local-private command writing be implemented in the first Codex C
  pass, or should the first pass stay pure in-memory plus synthetic fixtures?
- Should cross-platform confirmation require both Windows and macOS for every
  current competitive fact, or only for facts with platform-sensitive source
  behavior?
- Should the progress report be local-only forever, or should a reduced
  public-safe summary format be contracted later?

## Next Workflow Action

Recommended next role: Codex C if the user explicitly authorizes
metadata-only implementation against this contract. Otherwise route to Codex E
for contract review.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #481.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/481

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_owned_fact_capture_tracker.md

Goal:
Implement the metadata-only parser-owned fact capture tracker: target matrix,
session capture ledger, and coverage progress report builders/validators using
synthetic tests only.

Protected boundaries:
- Do not read, tail, copy, hash, normalize, summarize, upload, or commit
  private Player.log or UTC_Log content.
- Do not run private harvest, live MTGA, diagnostics, drift, watcher, tailer,
  network, firewall/drop, packet, OS/router, or private smoke checks.
- Do not write local/private artifacts except synthetic test fixtures.
- Do not create fixtures, golden replay manifests, expected-output files,
  fixture-promotion packets, proof files, metadata diff files, or corpus
  metadata edits.
- Do not edit tests/fixtures/parser_corpus/corpus_manifest.v1.json or
  tests/fixtures/parser_corpus/session_ledger.v1.json.
- Do not change parser behavior, parser event classes, parser state final
  reconciliation, router semantics, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, analytics behavior, OpenAI/model-provider behavior,
  AI/coaching behavior, CI gates, merge readiness, deploy readiness,
  production behavior, or final integration policy.
- Preserve parser_behavior_ready=false,
  pipeline_activation_ready_for_issue_388=false,
  private_harvest_authorized=false, fixture_promotion_authorized=false, and
  corpus_status_change_authorized=false.

Expected implementation:
- src/mythic_edge_parser/app/parser_owned_fact_tracker.py
- tests/test_parser_owned_fact_tracker.py
- optional synthetic fixtures under tests/fixtures/parser_owned_fact_tracker/
- docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
- PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_field_recovery_matrix.py tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py
- PYTHONPATH=src python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_golden_replay_harness.py
- python3 tools/check_secret_patterns.py --all
- python3 tools/check_protected_surfaces.py --base origin/main
- python3 tools/select_validation.py --base origin/main
- git diff --check

Expected output:
- implementation summary
- files changed
- validation run
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/481"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/465"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/549"
  previous_merge_commit: "ace067d3491565b2825a4c2c9fa1777a9c87ce30"
  completed_thread: "B"
  next_thread: "C_or_E"
  source_artifact: "GitHub issue #481 problem representation"
  target_artifact: "docs/contracts/parser_owned_fact_capture_tracker.md"
  verdict: "parser_owned_fact_capture_tracker_contract_created"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-owned-fact-capture-tracker-481"
  internal_project_area: "Corpus / Provenance"
  truth_owner: "parser remains truth owner; tracker owns capture/progress metadata only"
  bridge_code_status: "deferred_future_boundary"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  stop_conditions:
    - "Do not activate #388 or #381."
    - "Do not close #481, #388, or #434."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, watcher, tailer, private smoke, or private harvest evidence."
    - "Do not create committed fixtures, fixture-promotion packets, proof files, metadata diff files, review packets, recovery packet files, local/generated artifacts, or corpus metadata edits."
    - "Do not edit tests/fixtures/parser_corpus/corpus_manifest.v1.json or tests/fixtures/parser_corpus/session_ledger.v1.json."
    - "Do not change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching behavior or production behavior."
    - "Do not claim parser behavior readiness, pipeline activation readiness, private harvest readiness, fixture promotion, corpus status change, release readiness, production readiness, analytics truth, AI truth, or coaching truth."
```
