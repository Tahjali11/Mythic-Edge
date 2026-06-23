# Parser Evidence Confidence-Claim Vocabulary Contract

## Module

Planning contract for issue #558, the confidence-claim vocabulary for the
parser evidence pipeline under tracker #388.

Plain English: this contract defines the words Mythic Edge may use when local,
synthetic, reviewed, committed, packaged, or ratcheted evidence moves through
the harvest-to-corpus loop. The vocabulary exists so future automation can
describe evidence pressure without accidentally approving parser truth,
fixture promotion, corpus status changes, readiness, analytics truth, AI
truth, coaching truth, release readiness, deploy readiness, or production
behavior.

The Codex B pass wrote only this contract. This Codex D fixer pass updates
only the schema label wording so it matches the approved vocabularies below.
It does not implement code, run a dry run, read private logs, create fixtures,
edit corpus metadata, activate #388, or authorize #560 corpus automation
readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/558
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Latest completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/559
- Latest completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/563
- Latest completed merge commit: `ad4a12cc52f12f545d383121c8230c2841a6fba6`
- Related future gate: https://github.com/Tahjali11/Mythic-Edge/issues/560
- Related fact tracker: https://github.com/Tahjali11/Mythic-Edge/issues/481
- Related corpus-pressure issue: https://github.com/Tahjali11/Mythic-Edge/issues/527
- Related run-statistics issue: https://github.com/Tahjali11/Mythic-Edge/issues/531
- Base branch: `main`
- Target branch: `main`
- Working branch: `codex/parser-evidence-confidence-claim-vocabulary-558`
- Latest verified base commit: `ad4a12cc52f12f545d383121c8230c2841a6fba6`
- Risk tier: High

Observed during this Codex B / D pass:

- Issue #558 is open.
- Tracker #388 is open and not broadly active.
- Parent private-evidence issue #434 is open.
- Issue #559 is closed and PR #563 is merged.
- Issue #560 is open and intentionally deferred behind this vocabulary.
- The operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- A clean issue worktree was used because the primary checkout contained
  unrelated local governance and workflow changes.

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Tracker #388 remains open. This contract does not activate #388 or #381.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #558 and its Codex A reconciliation comment
- Tracker #388
- Parent private-evidence issue #434
- Issue #559 and PR #563
- Issue #560
- Issue #481
- Issue #527
- Issue #531
- `docs/contracts/parser_evidence_pipeline_activation_contract.md`
- `docs/contracts/parser_evidence_bounded_local_dry_run.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- `docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md`
- `docs/contracts/parser_recovery_human_approved_parser_corpus_update_workflow.md`
- `docs/contracts/parser_owned_fact_capture_tracker.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/local_artifacts_manifest.json`
- Existing parser-owned fact tracker, corpus ratchet, and #388 helper source
  and tests by inspection only.

No private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop,
packet, OS/router, diagnostics, drift, watcher, private smoke, workbook
export, SQLite, or generated local artifact was run, tailed, hashed, copied,
summarized, or read.

## Observed Current Behavior

The #388 lane now has reviewed contracts for a source-adapter boundary,
candidate reports, review packets, fixture-promotion proof objects, golden
replay fixture/manifest draft packets, corpus metadata diff objects,
PR-assist packets, pipeline activation semantics, and bounded local dry-run
semantics.

Those artifacts use many correct false-readiness flags, but there is not yet
a single repo-owned vocabulary that says what each intermediate evidence state
does and does not prove.

Current preserved readiness and authorization flags remain:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
dry_run_execution_authorized: false
implementation_authorized: false
```

## Problem

The first bad value is treating an intermediate evidence state as a stronger
claim than it actually supports.

Examples of bad upgrades:

- `candidate_observed` becomes "parser support exists."
- `review_packet_generated` becomes "human-approved."
- `human_approved` becomes "fixture promoted."
- `promotion_proof_generated` becomes "promotion authorized."
- `corpus_metadata_updated` becomes "coverage confirmed."
- `ratchet_passed` becomes "parser behavior ready."
- `dry_run_completed_public_safe` becomes "#388 active."
- private evidence becomes committed corpus confidence.

Without a common vocabulary, #560 corpus automation readiness could overclaim
the Manasight-like loop, #481 fact tracking could flatten local/private states
into committed confidence, #527 corpus-pressure automation could appear to
approve truth, and #531 run statistics could be mistaken for coverage
confirmation.

## Scope Decision

This contract approves vocabulary only.

In scope:

- claim and status state names;
- evidence requirements per state;
- privacy boundary per state;
- review and approval requirements per state;
- allowed downstream effects per state;
- forbidden promotions and overclaims;
- relation to #559 dry-run statuses;
- relation to #560 corpus automation readiness;
- relation to #481, #527, and #531;
- validation expectations for later implementation or review.

Out of scope:

- code implementation;
- dry-run execution;
- private evidence reads;
- private harvest execution;
- fixture creation;
- fixture-promotion packets;
- expected-output edits;
- corpus manifest or session-ledger edits;
- corpus package publication;
- corpus ratchet execution;
- baseline PR creation;
- parser behavior changes;
- #388 or #381 activation;
- #560 readiness clearance;
- PR creation, commits, pushes, or merges.

## Owning Layer

Owning layer: Quality / Governance, with Corpus / Provenance support.

Quality / Governance owns the confidence-claim vocabulary, role routing,
approval semantics, non-claims, and stop conditions.

Corpus / Provenance owns the evidence-state subjects that the vocabulary may
describe, such as candidate summaries, review packets, proof objects, fixture
drafts, manifest/session-ledger diffs, corpus packages, and ratchet reports.

Parser remains the truth owner for parser interpretation, parser events,
router behavior, parser state, match/game identity, deduplication, and final
reconciliation.

## Internal Project Area

Primary: Quality / Governance.

Supporting: Corpus / Provenance.

This contract is not a parser behavior module, corpus metadata mutation,
fixture-promotion package, private-evidence execution packet, analytics
module, AI module, coaching module, CI gate, merge gate, deploy gate, or
production module.

## Truth Owner

This contract owns claim vocabulary only.

Truth owners remain:

- parser facts: parser and state layer;
- private source evidence: local operator-owned private evidence surfaces;
- candidate summaries: #382 candidate-report boundary;
- review packets: #383 review-packet boundary;
- fixture-promotion proof objects: #384 proof boundary;
- fixture and manifest drafts: #385 draft boundary;
- corpus metadata diffs: #386 diff boundary;
- PR-assist packets: #387 PR-assist boundary;
- dry-run process status: #559 bounded dry-run boundary;
- fact-level progress: #481 parser-owned fact tracker boundary;
- corpus package and ratchet readiness: future #560 and Mythic-Edge-Corpus
  contracts.

No confidence state in this contract owns parser truth, fixture truth, corpus
truth, analytics truth, AI truth, coaching truth, release readiness, deploy
readiness, or production behavior.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no code. A later Codex C may implement validators,
schema constants, or docs wiring only if a reviewed follow-up contract
explicitly authorizes it.

## Files Owned By This Contract

- `docs/contracts/parser_evidence_confidence_claim_vocabulary.md`

Potential later review artifacts, if separately authorized:

- `docs/contract_test_reports/parser_evidence_confidence_claim_vocabulary.md`
- `docs/implementation_handoffs/parser_evidence_confidence_claim_vocabulary_comparison.md`

This contract does not authorize edits to:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- golden replay fixtures;
- expected-output files;
- parser source;
- analytics source;
- workbook, webhook, or Apps Script code;
- private evidence artifacts;
- local generated artifacts.

## Public Interface

The vocabulary should be treated as a public workflow interface for future
contracts and reports.

Future machine-readable claim objects, if separately authorized, should use:

```yaml
schema_version: "parser_evidence_confidence_claim.v1"
object: "mythic_edge_parser_evidence_confidence_claim"
claim_id: "<public-safe id>"
claim_state: "<one allowed state>"
subject_type: "<one allowed subject-type label>"
subject_ref: "<repo-relative or public-safe symbolic ref>"
evidence_refs: []
privacy_boundary: "<one allowed privacy-boundary label>"
review_requirement: "<one allowed review-requirement label>"
allowed_downstream_effects: []
forbidden_downstream_effects: []
authorization_flags:
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  dry_run_execution_authorized: false
  implementation_authorized: false
non_claims: []
```

Claim objects are coordination metadata only. They must not be consumed by
runtime parser code, workbook sync code, analytics scoring, AI/coaching
systems, production deployment, or release tooling as truth.

Schema label rule: future machine-readable claim objects must use exactly the
label vocabularies in this contract. They must not use shortcut labels such
as `synthetic`, `external_boundary`, `none`, `human_review`, `codex_e`,
`codex_f`, `codex_g`, or `later_contract` when the approved labels are
`synthetic_only`, `external_reference_only`, `blocked_external`,
`none_report_only`, `human_review_required`, `codex_e_required`,
`codex_f_required`, `codex_g_required`, and `later_contract_required`.

## Subject Type Classes

Allowed subject-type labels:

- `candidate_source`: candidate source or observation pressure.
- `candidate_summary`: #382-compatible candidate summary.
- `review_packet`: #383-compatible review packet.
- `reviewer_decision`: human reviewer decision metadata.
- `promotion_proof`: #384-compatible promotion proof object.
- `fixture_draft`: #385-compatible fixture or manifest draft packet.
- `committed_fixture`: sanitized committed fixture or expected-output artifact.
- `corpus_metadata_diff`: #386-compatible corpus metadata diff object.
- `corpus_package`: future Mythic-Edge-Corpus package metadata.
- `ratchet_report`: corpus ratchet comparison report.
- `dry_run_report`: #559-compatible bounded local dry-run report.
- `run_statistics`: #531-compatible run statistics or dropped-fact counters.
- `parser_fact`: #481-compatible parser-owned fact tracker subject.
- `external_dependency`: external or sibling-repo dependency metadata.

Subject-type labels describe the referenced artifact class only. They do not
raise authority, approval, privacy, readiness, or truth.

## Claim-State Vocabulary

### `candidate_observed`

Meaning: a synthetic, public, or local/private source appears to contain
evidence relevant to one or more parser-owned facts or scenario families.

Evidence requirement: source class, symbolic source id, candidate reason, and
public-safe family/fact hints.

Privacy boundary: may be local/private only.

Review requirement: none for observation; human review required before any
candidate can advance.

Allowed downstream effect: may be listed in local candidate planning or #481
fact tracker as evidence pressure.

Forbidden overclaim: not parser support, not candidate harvested, not coverage
confirmed, not fixture promotion.

### `candidate_harvested`

Meaning: an approved synthetic or local-only harvest process produced a
candidate summary from an allowed source class.

Evidence requirement: #382-compatible candidate summary id, source class,
privacy classification, non-claim flags, and validation summary.

Privacy boundary: public-safe for synthetic; local/private for private
sources.

Review requirement: human review before approval.

Allowed downstream effect: may feed `review_packet_generated`.

Forbidden overclaim: not human approval, not parser truth, not fixture truth,
not corpus status movement.

### `review_packet_generated`

Meaning: a #383-compatible review packet exists for a candidate.

Evidence requirement: candidate summary id, review packet id, privacy report,
review routing, and false authorization flags.

Privacy boundary: public-safe only if all fields are sanitized; otherwise
local/private.

Review requirement: human reviewer decision required to advance.

Allowed downstream effect: may feed `human_approved`, `coverage_rejected`, or
`coverage_deferred`.

Forbidden overclaim: not approval, not proof, not fixture promotion, not
coverage confirmation.

### `human_approved`

Meaning: a human reviewer approved a review packet for the next scoped
planning step.

Evidence requirement: reviewer decision id, approval date, subject refs,
allowed next step, expiration or staleness rule, and explicit non-claims.

Privacy boundary: approval text may be public-safe, but private evidence
references remain local-only.

Review requirement: Codex E review is still required before committed artifact
changes; Codex F/G are required for submission and merge.

Allowed downstream effect: may feed `promotion_proof_generated` or
`fixture_draft_generated` if the relevant contract allows it.

Forbidden overclaim: not fixture promotion authorization, not corpus metadata
authorization, not parser behavior verification.

### `fixture_draft_generated`

Meaning: a #385-compatible fixture or manifest draft packet exists.

Evidence requirement: draft packet id, source review packet id, public-safe
fixture summary, manifest summary, privacy checks, and no-write flags.

Privacy boundary: draft payloads may be local-only unless proven sanitized.

Review requirement: Codex E review and later scoped fixture-promotion contract
before committed fixture changes.

Allowed downstream effect: may support `promotion_proof_generated` or future
fixture-promotion review.

Forbidden overclaim: not a committed fixture, not golden replay truth, not
corpus status movement.

### `promotion_proof_generated`

Meaning: a #384-compatible proof object describes whether a candidate appears
ready for fixture-promotion review.

Evidence requirement: proof id, approved review packet id, fixture/draft refs
if any, check refs, before/after coverage comparison, and false flags.

Privacy boundary: public-safe only if all evidence refs are sanitized.

Review requirement: Codex E review required; Codex F/G required for any later
committed changes.

Allowed downstream effect: may inform a future fixture-promotion issue.

Forbidden overclaim: not fixture-promotion authorization, not corpus update
authorization, not parser behavior readiness.

### `sanitized_fixture_committed`

Meaning: a sanitized fixture or expected-output artifact has been committed
through a reviewed PR path.

Evidence requirement: PR link, merge commit, fixture path, manifest path,
forbidden-content scan, golden replay validation, and scoped issue/contract.

Privacy boundary: public committed.

Review requirement: Codex E/F/G path complete.

Allowed downstream effect: may support corpus metadata update review,
ratchet comparison, or scoped coverage claims.

Forbidden overclaim: not global parser behavior readiness, not private smoke
success, not full corpus parity.

### `corpus_metadata_updated`

Meaning: corpus manifest/session-ledger metadata has changed through a
reviewed PR path.

Evidence requirement: PR link, merge commit, changed metadata refs, related
fixture refs, validation commands, and preserved known gaps.

Privacy boundary: public committed.

Review requirement: Codex E/F/G path complete.

Allowed downstream effect: may feed package validation or corpus parity
reports.

Forbidden overclaim: not coverage confirmed unless package and ratchet gates
also pass for the same scoped subject.

### `corpus_package_validated`

Meaning: a future Mythic-Edge-Corpus package preview or validation gate has
passed for a named reviewed package.

Evidence requirement: package id, corpus repo issue/PR refs, validation
summary, artifact refs, and non-claims.

Privacy boundary: public committed/package metadata only.

Review requirement: #560 or a corpus-repo contract must define the exact
acceptable evidence.

Allowed downstream effect: may feed `ratchet_passed`.

Forbidden overclaim: not Mythic Edge parser truth, not release readiness, not
production readiness.

### `ratchet_passed`

Meaning: a future corpus ratchet comparison passed for a named package or
baseline proposal.

Evidence requirement: ratchet report id, baseline ref, package ref,
comparison status, changed counts, and non-claims.

Privacy boundary: public committed/package metadata only.

Review requirement: human/Codex review before baseline or metadata changes.

Allowed downstream effect: may support `coverage_confirmed` only when the
same scoped subject also has committed sanitized evidence and reviewed
metadata.

Forbidden overclaim: not semantic parser correctness by itself, not baseline
update authorization, not parser behavior readiness.

### `coverage_confirmed`

Meaning: a specific scoped fact, family, or fixture-backed evidence claim has
met the full evidence chain defined by its owning contract.

Minimum evidence requirement:

- committed sanitized fixture or approved public evidence;
- reviewed metadata update, if metadata changes are part of the claim;
- passing relevant golden replay, corpus parity, privacy, protected-surface,
  package, and ratchet checks;
- Codex E/F/G review path for committed artifacts;
- explicit subject scope.

Privacy boundary: public committed evidence only.

Review requirement: complete scoped review path.

Allowed downstream effect: may be used as scoped corpus evidence for #481 or
future #560 readiness analysis.

Forbidden overclaim: not global parser behavior readiness, not strict
`pipeline_activation_ready_for_issue_388`, not release readiness, not
production readiness, not analytics truth, AI truth, or coaching truth.

### `coverage_rejected`

Meaning: a candidate, review packet, proof, fixture draft, metadata diff, or
ratchet result was reviewed and rejected for the scoped claim.

Evidence requirement: rejected subject ref, reviewer decision, reason code,
and whether rework is allowed.

Privacy boundary: public-safe reason codes only if private evidence exists.

Review requirement: human or Codex E review depending on the subject.

Allowed downstream effect: may update #481 progress reports or #531 dropped
fact counters.

Forbidden overclaim: rejection of one claim does not prove parser breakage
outside the scoped subject.

### `coverage_deferred`

Meaning: a claim is intentionally postponed because the subject is out of
current scope, blocked, stale, duplicate, noisy, or awaiting another issue.

Evidence requirement: deferred subject ref, deferral reason, owner issue, and
expiration or revisit rule.

Privacy boundary: public-safe if reason text contains no private source data.

Review requirement: owner issue decides whether to revisit.

Allowed downstream effect: may keep #481 and #560 honest about remaining
work.

Forbidden overclaim: deferred does not mean covered, rejected, or ready.

### `private_evidence_local_only`

Meaning: evidence exists only in a private/local boundary and may not be
committed or summarized as public evidence.

Evidence requirement: symbolic local-only ref, approval context, source class,
retention rule, and redaction status. No raw private values.

Privacy boundary: local/private only.

Review requirement: #434 and a later explicit private-evidence contract.

Allowed downstream effect: may inform local review and candidate planning.

Forbidden overclaim: not committed evidence, not coverage confirmed, not
public corpus confidence.

### `external_boundary_blocked`

Meaning: a claim depends on external evidence, source-repo/corpus-repo
automation, or a boundary outside current Mythic Edge authority.

Evidence requirement: blocked subject, external dependency, owner issue or
repo, and unblock condition.

Privacy boundary: public-safe dependency metadata only.

Review requirement: owning external or sibling-repo workflow.

Allowed downstream effect: may block #560 readiness or defer a #481 fact row.

Forbidden overclaim: not rejected, not covered, not Mythic Edge parser truth.

### `dry_run_shape_verified`

Meaning: a future #559-approved fixture-safe dry run completed the public-safe
handoff shape.

Evidence requirement: #559 dry-run report id, run mode, input refs, output
refs, validation summary, and false flags.

Privacy boundary: public-safe only.

Review requirement: #559 contract review and explicit user approval before
execution.

Allowed downstream effect: may support process-readiness analysis.

Forbidden overclaim: not evidence coverage, not fixture promotion, not #388
activation, not private harvest authorization.

## State Transition Rules

Allowed forward transitions:

```text
candidate_observed
  -> candidate_harvested
  -> review_packet_generated
  -> human_approved
  -> promotion_proof_generated
  -> fixture_draft_generated
  -> sanitized_fixture_committed
  -> corpus_metadata_updated
  -> corpus_package_validated
  -> ratchet_passed
  -> coverage_confirmed
```

Allowed terminal or side transitions:

```text
review_packet_generated -> coverage_rejected
review_packet_generated -> coverage_deferred
human_approved -> coverage_deferred
promotion_proof_generated -> coverage_rejected
promotion_proof_generated -> coverage_deferred
private_evidence_local_only -> candidate_observed
external_boundary_blocked -> coverage_deferred
dry_run_shape_verified -> coverage_deferred
```

Forbidden transitions:

- `candidate_observed` directly to `coverage_confirmed`;
- `private_evidence_local_only` directly to any public committed state;
- `dry_run_shape_verified` directly to evidence coverage;
- `ratchet_passed` directly to parser behavior readiness;
- any state directly to strict `pipeline_activation_ready_for_issue_388=true`;
- any state directly to fixture promotion or corpus metadata mutation without
  the owning scoped contract and review path.

## Privacy Boundary Classes

Allowed privacy boundary labels:

- `public_committed`: committed repo-safe artifact.
- `public_report_only`: public-safe report or handoff with no raw/private
  payload.
- `synthetic_only`: synthetic data with no private or external raw source.
- `local_private`: local-only private evidence or output.
- `external_reference_only`: external or sibling-repo metadata reference only.
- `blocked_private`: private evidence exists or may exist, but the current
  contract cannot inspect or publish it.
- `blocked_external`: required evidence belongs to a sibling repo or external
  boundary not authorized here.

Private and blocked classes must not be used as public corpus confidence.

## Review Requirement Classes

Allowed review requirement labels:

- `none_report_only`: no approval claim is made.
- `human_review_required`: human approval required before the next state.
- `codex_e_required`: independent review required.
- `codex_f_required`: submitter path required for committed artifacts.
- `codex_g_required`: deployer/merge/closeout path required.
- `private_evidence_contract_required`: parent #434 or equivalent approval
  required.
- `corpus_repo_contract_required`: #560 or Mythic-Edge-Corpus contract
  required.
- `later_contract_required`: this state cannot advance without a new scoped
  contract.

## Allowed Downstream Effects

Allowed effects are intentionally small:

- `route_to_review`;
- `route_to_rework`;
- `route_to_defer`;
- `route_to_fact_tracker`;
- `route_to_fixture_promotion_contract`;
- `route_to_corpus_metadata_diff_review`;
- `route_to_corpus_repo_gate`;
- `route_to_ratchet_review`;
- `route_to_coverage_confirmation_review`;
- `report_process_shape_only`;
- `report_local_private_only`;
- `report_external_blocker_only`.

Forbidden effects:

- `approve_parser_truth`;
- `approve_fixture_promotion`;
- `edit_corpus_metadata`;
- `publish_corpus_package`;
- `update_baseline`;
- `activate_388`;
- `activate_381`;
- `claim_parser_behavior_ready`;
- `claim_pipeline_activation_ready`;
- `claim_release_ready`;
- `claim_production_ready`;
- `claim_analytics_truth`;
- `claim_ai_truth`;
- `claim_coaching_truth`.

## Relation To #559

#559 dry-run reports may use `dry_run_shape_verified` only when the
fixture-safe dry-run completed under the reviewed #559 contract and explicit
user approval.

#559 statuses such as `dry_run_completed_public_safe` may support process
evidence. They must not be mapped to:

- `candidate_harvested`;
- `human_approved`;
- `sanitized_fixture_committed`;
- `corpus_metadata_updated`;
- `coverage_confirmed`;
- `pipeline_activation_ready_for_issue_388=true`.

## Relation To #560

#560 must consume this vocabulary before judging corpus automation readiness.

#560 may not claim a complete Manasight-like loop unless the relevant
Mythic-Edge-Corpus package, validation, release, dispatch, ratchet, and
baseline proposal gates define their own evidence and can map back into these
states without overclaiming.

This contract does not decide whether #560 is ready. It supplies the language
#560 must use.

## Relation To #481

#481 parser-owned fact tracker may use this vocabulary as fact-lifecycle
metadata. A fact row may move through private capture, candidate, review,
approval, fixture, and confirmation states only when the referenced evidence
meets this contract's requirements.

#481 must not treat `private_evidence_local_only`, `candidate_observed`,
`candidate_harvested`, `review_packet_generated`, `dry_run_shape_verified`, or
`ratchet_passed` as `coverage_confirmed`.

## Relation To #527

#527 corpus-pressure automation may use these states to describe pressure,
proposed improvements, and review-needed paths. It must not let automation
approve parser truth, fixture promotion, baseline updates, or readiness.

The strongest default state #527 may claim from automation alone is
`coverage_deferred`, `external_boundary_blocked`, or a review-needed state
unless a separate contract proves a stronger transition.

## Relation To #531

#531 run statistics and dropped-fact counters may support
`candidate_observed`, `coverage_rejected`, or `coverage_deferred` with reason
codes. Counters alone must not produce `coverage_confirmed`.

High counts, low counts, dropped facts, parse stats, and unresolved identifiers
are operational signals. They are not parser truth approval or corpus
confidence by themselves.

## Error Behavior

Confidence-claim processing must fail closed.

Required blocked statuses:

- `blocked_unknown_state`;
- `blocked_missing_evidence`;
- `blocked_private_boundary`;
- `blocked_external_boundary`;
- `blocked_missing_review`;
- `blocked_forbidden_transition`;
- `blocked_overclaim`;
- `blocked_stale_evidence`;
- `blocked_forbidden_content`;
- `blocked_authorization_flag_true`.

If a claim object uses an unknown state, missing evidence, private source
data, an unreviewed transition, a true false-authority flag, or forbidden
overclaim language, the consuming workflow must stop and route to Codex A or
B for reframing.

## Side Effects

Contract-authoring/fixer side effects allowed by this contract:

- create or update `docs/contracts/parser_evidence_confidence_claim_vocabulary.md`.

Side effects not allowed:

- code implementation;
- dry-run execution;
- private evidence reads;
- fixture creation;
- fixture promotion;
- corpus metadata edits;
- package publication;
- ratchet execution;
- baseline update;
- issue creation;
- PR creation;
- commits;
- pushes;
- scheduled automation;
- production-facing changes.

## Invariants

- Every confidence state must name the evidence it requires.
- Every confidence state must name its privacy boundary.
- Every confidence state must name its review requirement.
- Every confidence state must name allowed and forbidden downstream effects.
- Local/private evidence must stay local/private until a later contract and
  explicit approval produce public-safe derived evidence.
- Automation may create pressure and routing signals; it must not approve
  truth.
- `coverage_confirmed` must be scoped, evidence-backed, public-safe, and
  reviewed.
- No state may set these flags to true:
  - `parser_behavior_ready`;
  - `pipeline_activation_ready_for_issue_388`;
  - `private_harvest_authorized`;
  - `fixture_promotion_authorized`;
  - `corpus_status_change_authorized`;
  - `dry_run_execution_authorized`;
  - `implementation_authorized`.

## Compatibility

This contract preserves existing schema and status vocabulary from:

- `parser_evidence_harvest_candidate_summary.v1`;
- `parser_evidence_harvest_review_packet.v1`;
- `parser_evidence_fixture_promotion_proof.v1`;
- `parser_evidence_golden_replay_fixture_manifest_drafts.v1`;
- `parser_evidence_corpus_metadata_diff.v1`;
- `parser_evidence_bounded_local_dry_run.v1`;
- `parser_owned_fact_target_matrix.v1`;
- `parser_feature_equity_corpus_ratchet_report.v1`.

Existing report-only or synthetic-only states remain report-only or
synthetic-only unless a later reviewed contract authorizes a transition.

## Validation Requirements

Contract validation for this artifact:

```bash
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_evidence_confidence_claim_vocabulary.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_confidence_claim_vocabulary.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_confidence_claim_vocabulary.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Later Codex C validation, if a validator implementation is separately
authorized:

```bash
python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_feature_equity_corpus_ratchet.py
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

## Acceptance Criteria

- The contract exists at
  `docs/contracts/parser_evidence_confidence_claim_vocabulary.md`.
- It defines all issue-requested confidence states.
- Each state identifies evidence requirement, privacy boundary, review
  requirement, allowed downstream effect, and forbidden overclaim.
- It distinguishes local/private, synthetic, report-only, human-approved,
  committed, packaged, ratcheted, and confirmed evidence.
- It defines relation to #559, #560, #481, #527, and #531.
- It preserves false readiness and authorization flags.
- It includes validation expectations and non-claims.

## Next Workflow Action

Next role: Codex E for contract review.

After review and contract-only submission, Codex G may close #558 if the PR is
merged and tracker #388 is updated. Only then should #560 be reconciled as the
next corpus automation readiness gate.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #558.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/558

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract artifact:
docs/contracts/parser_evidence_confidence_claim_vocabulary.md

Review goal:
Review the #558 confidence-claim vocabulary contract. Confirm it defines
evidence requirements, privacy boundaries, review requirements, allowed
downstream effects, forbidden overclaims, #559 dry-run mapping, #560
dependency behavior, and #481/#527/#531 interactions without authorizing code,
dry-run execution, private evidence reads, fixture promotion, corpus metadata
edits, automation readiness, parser behavior readiness, release readiness,
production readiness, analytics truth, AI truth, or coaching truth. Verify the
Codex D fix for `CONFCLAIM-E-001`: the future machine-readable schema uses
only label vocabularies defined by this contract, including subject-type,
privacy-boundary, and review-requirement labels.

Expected output:
- Findings first, if any.
- Contract verdict.
- Validation reviewed or run.
- Remaining risks and non-claims.
- Recommended next role.
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/558"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/559"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/563"
  completed_thread: "D"
  next_thread: "E"
  finding_id: "CONFCLAIM-E-001"
  verdict: "schema_label_vocabulary_mismatch_fixed_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-evidence-confidence-claim-vocabulary-558"
  latest_verified_commit: "ad4a12cc52f12f545d383121c8230c2841a6fba6"
  target_artifact: "docs/contracts/parser_evidence_confidence_claim_vocabulary.md"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  dry_run_execution_authorized: false
  implementation_authorized: false
  recommended_after_review: "Codex F/G for contract-only submission, then Codex A/B for #560 corpus automation readiness reconciliation."
  validation:
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "printf '%s\\n' docs/contracts/parser_evidence_confidence_claim_vocabulary.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_evidence_confidence_claim_vocabulary.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_evidence_confidence_claim_vocabulary.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not implement code, run dry runs, read private evidence, create fixtures, promote fixtures, update corpus metadata, execute ratchets, or create baseline PRs."
    - "Do not activate #388 or #381."
    - "Do not claim parser behavior readiness, strict pipeline activation readiness, fixture-promotion readiness, corpus status change readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, security assurance, privacy assurance, or full parser regression parity."
```
