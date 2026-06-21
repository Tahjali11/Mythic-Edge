# Parser Recovery Field Recovery Matrix Contract

## Module

Field Recovery Matrix for parser drift recovery after the initial #388
parser-evidence planning sequence.

Plain English: this contract defines how Mythic Edge should classify each
parser-owned field when Player.log or UTC_Log evidence changes. The matrix
must distinguish direct evidence, equivalent evidence, bounded derivation,
analytics-only approximation, unavailable evidence, private-evidence blocks,
external-boundary blocks, and review-required states. It prevents plausible
fallbacks from becoming high-confidence parser truth.

This Codex B pass does not implement code, open a PR, activate #388 or #381,
read private logs, create fixtures, promote corpus rows, write recovery
packets, change parser behavior, or claim parser behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/451
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/387
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/537
- Previous merge commit: `a020311871738d4ea04d9244ac1635ef3936975c`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- Operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` and `origin/main` were both
  `a020311871738d4ea04d9244ac1635ef3936975c`.
- Issue #451 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- Issues #381 through #387 were closed.
- #387 / PR #537 was merged into `main`.
- The checkout was clean before this contract was added.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`
- `docs/internal_project_map.md`
- Issue #451
- Tracker #388
- Parent issue #434
- Issue #387 and PR #537
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- `docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md`
- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`

No private Player.log, UTC_Log, app-data, diagnostics, drift, live MTGA,
network, firewall/drop, packet, OS/router, or private smoke checks were run
or read.

## Observed Current Behavior

The #388 evidence-pipeline planning sequence now has contracts and synthetic
or in-memory planning modules for:

- #381 UTC_Log source adapter;
- #382 local harvest candidate reports;
- #383 harvest review packets;
- #384 fixture promotion proof objects;
- #386 corpus metadata diff objects;
- #385 golden replay fixture and manifest drafts;
- #387 reviewed fixture-promotion PR-assist packets.

Those slices preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
evidence_pipeline_planning_ready_for_issue_388: false
file_writing_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
```

Existing evidence-ledger work defines field provenance vocabulary:

- value sources: `observed`, `derived`, `inferred`, `unknown`, `conflict`,
  and `legacy_enriched`;
- confidence labels: `high`, `medium`, `low`, and `unknown`;
- finality labels: `live`, `provisional`, `final`, and `reconciled`;
- invariant statuses: `passed`, `failed`, `not_applicable`, `not_checked`,
  and `degraded`;
- field-evidence records that require review for conflicts, failed
  invariants, and low-confidence final or reconciled values.

No dedicated field recovery matrix contract, module, test, recovery packet,
or committed matrix artifact existed before this contract.

## Problem

If MTGA changes Player.log or UTC_Log output, Mythic Edge needs a field-level
way to decide what each parser-owned field may do next. Some fields may still
have direct evidence. Some may have semantically equivalent evidence from a
new source. Some may be derivable with bounded confidence. Some may support
analytics display only. Some must become unavailable until a later reviewed
parser contract and fixture evidence restore them.

Without a recovery matrix, a future drift response could accidentally:

- treat approximate evidence as parser truth;
- treat analytics-only summaries as parser output fields;
- infer missing match or game facts from incomplete evidence;
- allow private-evidence or external-boundary gaps to masquerade as covered
  parser behavior;
- promote fallback evidence without fixture proof;
- move truth into workbook formulas, Apps Script, analytics, AI, or coaching;
- claim #388 activation or parser behavior readiness from recovery planning.

The first bad value is any field whose recovery category is not `direct` or
reviewed `equivalent` being restored as high-confidence parser truth without
a new scoped contract, parser implementation, fixture evidence, and review.

## Scope Decision

This contract approves a future metadata/schema implementation of the Field
Recovery Matrix only.

Codex C may implement an in-repo static matrix schema, validator, and a small
seed matrix derived from existing evidence-ledger field IDs and parser-owned
field families. That implementation must remain review/report metadata. It
must not change parser behavior, output rows, workbook schema, webhook
payloads, diagnostics reports, golden replay manifests, corpus metadata,
runtime status, analytics behavior, AI behavior, or coaching behavior.

This contract does not authorize:

- private log reads;
- live diagnostics runs;
- watcher implementation;
- recovery packet generation;
- issue or fixture draft generation;
- fixture file writing;
- golden replay manifest writing;
- expected-output writing;
- corpus status changes;
- parser output changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Parser and Quality / Governance
support.

Corpus / Provenance owns the recovery matrix vocabulary, evidence-category
mapping, field evidence dependency policy, and recovery review rules.

Parser owns event interpretation, parser events, router behavior, parser
state, match/game identity, deduplication, final reconciliation, and
parser-owned output values.

Quality / Governance owns workflow routing, validation, protected-surface
checks, private-evidence gates, and non-claim enforcement.

Analytics, workbook/transport, Apps Script, local app, AI, and coaching
surfaces are consumers only. They must not become recovery truth owners.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, for parser-owned field identity and output policy.
- Quality / Governance, for review and protected-surface rules.
- Generated / Local Artifacts, for any future local-only recovery packets if
  separately authorized.

This contract is not a parser behavior contract, not a private-evidence
execution contract, not a fixture-promotion contract, not a workbook or
transport contract, not an analytics contract, not an AI/coaching contract,
not a CI gate, and not a release/deploy/production readiness gate.

## Truth Owner

Truth owner for parser values remains the existing parser, router, event,
state, model, extractor, match/game identity, deduplication, and final
reconciliation layers.

Truth owner for field provenance vocabulary remains:

- `docs/contracts/player_log_evidence_ledger_schema.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`

Truth owner for local field-evidence sidecar behavior remains:

- `docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `tests/test_runtime_field_evidence.py`

Truth owner for this recovery-matrix vocabulary is this contract and any
later reviewed implementation handoff and contract-test report.

The matrix must not own parser facts, fixture expected output, corpus status,
private evidence, analytics truth, AI truth, coaching truth, workbook truth,
merge readiness, deploy readiness, release readiness, production behavior, or
tracker completion.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code in Codex B.

If later implemented, the matrix is shared support from Corpus / Provenance to
Quality / Governance and future recovery review workflows.

Allowed future data flow:

```text
evidence ledger entries + field-evidence records + diagnostics/drift context
  -> field recovery matrix category and output policy
  -> human/Codex recovery review decision
  -> later scoped parser contract or fixture workflow, if approved
```

Forbidden reverse flow:

```text
field recovery matrix
  -/-> parser value overwrite
  -/-> workbook formula reconstruction
  -/-> webhook or Apps Script payload change
  -/-> analytics/AI/coaching truth
  -/-> fixture promotion
  -/-> corpus status promotion
  -/-> #388 activation
```

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_recovery_field_recovery_matrix.md`

Future Codex C implementation files authorized by this contract:

- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`
- `docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md`
- `docs/contract_test_reports/parser_recovery_field_recovery_matrix.md`

Referenced but not silently owned:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`

Not owned by this contract:

- raw Player.log or UTC_Log files;
- normalized private log copies;
- local app-data;
- runtime status files;
- failed posts;
- workbook exports;
- private reports;
- fixture files;
- golden replay manifests;
- expected-output files;
- recovery packet files;
- corpus manifest or session ledger edits.

## Public Interface

Future implementation may add a report-only module:

```python
src/mythic_edge_parser/app/field_recovery_matrix.py
```

Required constants:

```python
FIELD_RECOVERY_MATRIX_OBJECT = "mythic_edge_parser_field_recovery_matrix"
FIELD_RECOVERY_MATRIX_SCHEMA_VERSION = "parser_field_recovery_matrix.v1"
FIELD_RECOVERY_MATRIX_ROW_OBJECT = "mythic_edge_parser_field_recovery_matrix_row"
```

Recommended public functions:

```python
def build_field_recovery_matrix() -> dict[str, Any]:
    ...

def iter_field_recovery_rows() -> Iterable[dict[str, Any]]:
    ...

def validate_field_recovery_matrix(matrix: Mapping[str, Any]) -> list[str]:
    ...

def validate_field_recovery_row(row: Mapping[str, Any]) -> list[str]:
    ...
```

These functions must be pure metadata helpers. They must not read private
logs, inspect live files, run diagnostics, run golden replay, write output
files, mutate parser state, or change runtime behavior.

## Matrix Object Shape

Required top-level fields:

| Field | Requirement |
| --- | --- |
| `object` | `mythic_edge_parser_field_recovery_matrix` |
| `schema_version` | `parser_field_recovery_matrix.v1` |
| `source_issue` | `https://github.com/Tahjali11/Mythic-Edge/issues/451` |
| `pipeline_tracker` | `https://github.com/Tahjali11/Mythic-Edge/issues/388` |
| `parent_private_evidence_issue` | `https://github.com/Tahjali11/Mythic-Edge/issues/434` |
| `status` | `planning_matrix_ready`, `review_required`, or `invalid` |
| `parser_behavior_ready` | `false` |
| `pipeline_activation_ready_for_issue_388` | `false` |
| `private_harvest_authorized` | `false` |
| `fixture_promotion_authorized` | `false` |
| `corpus_status_change_authorized` | `false` |
| `rows` | list of field recovery rows |
| `non_claims` | required non-claims |

The matrix may include a `matrix_summary` object with counts by recovery
category, output policy, and review status. Summary counts are review aids
only and must not become readiness metrics.

## Field Recovery Row Shape

Each row must describe one parser-owned field or one tightly scoped parser
output facet.

Required row fields:

| Field | Requirement |
| --- | --- |
| `object` | `mythic_edge_parser_field_recovery_matrix_row` |
| `field_id` | stable lower-case dot-separated ID |
| `display_name` | public-safe label |
| `field_family` | match, game, queue, rank, participant, gameplay_action, runtime_health, etc. |
| `parser_owner` | parser module or parser-owned model surface |
| `output_surfaces` | parser-owned rows or local review surfaces, not workbook truth |
| `evidence_ledger_entry_ids` | zero or more ledger entry IDs |
| `required_direct_evidence` | list of required source signals |
| `allowed_fallback_evidence` | list of fallback source signals |
| `forbidden_fallback_evidence` | list of explicitly forbidden fallbacks |
| `recovery_category` | one allowed recovery category |
| `parser_output_policy` | one allowed parser output policy |
| `analytics_output_policy` | one allowed analytics/display policy |
| `minimum_confidence` | `high`, `medium`, `low`, or `unknown` |
| `allowed_finality` | list using evidence-ledger finality labels |
| `degradation_flags` | list of symbolic degradation flags |
| `stale_source_behavior` | one allowed stale-source behavior |
| `review_required` | boolean |
| `restoration_requirements` | list of required gates before parser restoration |
| `non_claims` | required non-claims |

Rows must not contain raw log excerpts, exact private paths, raw hashes,
source snippets, packet captures, decklists, strategy notes, private reports,
or local-only artifact paths.

## Field Identity Vocabulary

Field IDs must be stable, lower-case, dot-separated, and scoped to the parser
output concept rather than a downstream display label.

Examples:

- `match.match_id`
- `match.event_id`
- `match.queue_type`
- `game.game1_result`
- `game.game1_starting_player`
- `game.game1_play_draw`
- `participant.local_player_team`
- `gameplay_action.action_type`
- `gameplay_action.actor_relation`
- `runtime_health.unknown_entry_count`
- `runtime_health.truncation_count`

Workbook column names, dashboard labels, analytics view aliases, and AI
phrases may be referenced as consumers, but they must not be primary field
IDs.

## Recovery Categories

Allowed `recovery_category` values:

- `direct`
- `equivalent`
- `derived_bounded`
- `approximate_analytics_only`
- `unavailable`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `review_required`

### `direct`

The same parser-owned source evidence still exists and is still parsed by the
approved parser path.

Parser output policy:

- Existing parser behavior may continue.
- New or changed parser output still requires a scoped parser contract and
  implementation.

Confidence/finality:

- May use evidence-ledger high-confidence and final/reconciled labels when
  the ledger entry and field-evidence record support them.

### `equivalent`

Different evidence appears to provide the same semantic parser fact with the
same or stronger source quality, but parser restoration still requires review.

Parser output policy:

- Must not be restored as parser truth until a new scoped parser contract,
  implementation, sanitized/synthetic fixture evidence, and Codex E review
  prove equivalence.

Confidence/finality:

- Maximum `medium` confidence before implementation review.
- May become `high` only after reviewed parser implementation and fixture
  evidence.

### `derived_bounded`

The fact can be deterministically derived from parser-owned ingredients with
known constraints and reviewable degradation behavior.

Parser output policy:

- May be parser output only if the parser already owns that derivation or a
  future parser contract authorizes it.
- Must preserve explicit degradation flags and avoid hidden inference.

Confidence/finality:

- Maximum `medium` confidence unless an existing ledger entry says otherwise.
- Must lower confidence when source ingredients are stale, missing,
  contradictory, truncated, or partial.

### `approximate_analytics_only`

The evidence can support an approximate display or analysis hint, but it is
not parser truth.

Parser output policy:

- Must not populate or restore parser-owned fields.
- Must not write workbook/parser rows as if the value were a fact.

Analytics/display policy:

- May be exposed only as degraded, approximate, review-needed, or
  unavailable-aware context in an authorized analytics/display contract.

### `unavailable`

No safe direct, equivalent, or bounded evidence is available.

Parser output policy:

- Leave the parser field blank, unknown, omitted, or unavailable according to
  existing parser contracts.
- Do not invent zeros, false values, losses, wins, names, decklists, or
  identities.

### `blocked_private_evidence`

Recovery depends on private/local evidence that has not been approved,
redacted, reviewed, or transformed into a public-safe artifact.

Parser output policy:

- No parser restoration or corpus status change.
- Route to #434 or a later private-evidence child issue.

### `blocked_external_boundary`

Recovery depends on external, platform, network, provider, or game-client
behavior outside current repo authority.

Parser output policy:

- No parser restoration or corpus status change.
- Route to a future explicit external-boundary or corpus issue.

### `review_required`

Evidence is conflicting, ambiguous, stale, policy-changing, or outside the
current vocabulary.

Parser output policy:

- Stop before parser restoration, fixture promotion, or status movement.
- Route to Codex A or B for reframing or contract update.

## Parser Output Policy

Allowed `parser_output_policy` values:

- `preserve_existing_parser_behavior`
- `restore_only_after_parser_contract_and_fixture_review`
- `emit_degraded_only_if_existing_parser_contract_allows`
- `blank_or_unknown_until_recovered`
- `never_parser_truth_analytics_only`
- `blocked_until_private_evidence_review`
- `blocked_until_external_boundary_resolved`
- `manual_review_required`

The matrix must not authorize parser output by itself. Parser restoration
requires a new scoped parser issue/contract unless the row is `direct` and
the existing parser behavior already emits the value.

## Analytics And Display Output Policy

Allowed `analytics_output_policy` values:

- `may_display_parser_value_with_evidence_label`
- `may_display_degraded_context_only`
- `may_display_approximate_context_only`
- `may_display_unavailable`
- `must_not_display_as_fact`
- `not_applicable`

Analytics and display surfaces may use the matrix only to explain confidence,
availability, degradation, review status, and non-claims. They must not use it
to fill parser-owned facts, infer hidden cards, classify archetypes, label
player mistakes, provide gameplay advice, or claim coaching truth.

## Confidence, Finality, And Degradation Policy

The matrix must reuse evidence-ledger vocabulary:

- confidence: `high`, `medium`, `low`, `unknown`;
- finality: `live`, `provisional`, `final`, `reconciled`;
- value source: `observed`, `derived`, `inferred`, `unknown`, `conflict`,
  `legacy_enriched`.

General rules:

- `approximate_analytics_only` rows cannot have parser confidence above
  `low`.
- `unavailable`, `blocked_private_evidence`, and
  `blocked_external_boundary` rows must use `unknown` or `low` confidence.
- `review_required=true` is required for conflicts, stale sources,
  unknown vocabulary, failed invariants, or low-confidence final/reconciled
  values.
- Truncation, data loss, unknown entries, timestamp anomalies, source
  rotation, incomplete windows, and missing source ingredients must be
  represented as degradation flags.
- Confidence can be lowered by matrix policy, but the matrix must not raise a
  value above the evidence-ledger entry's supported confidence.

## Stale Source Behavior

Allowed `stale_source_behavior` values:

- `preserve_prior_final_value_with_review_note`
- `lower_confidence_and_mark_degraded`
- `blank_or_unknown_for_new_outputs`
- `route_to_review_required`
- `blocked_until_fresh_evidence`
- `not_applicable`

Stale source behavior must be conservative. A stale source may explain why a
previous field was available, but it must not prove current parser support or
fresh match/game facts.

## Evidence Requirements

Each row should identify:

- required direct evidence signals;
- fallback evidence signals;
- forbidden fallback signals;
- expected evidence-ledger entry IDs;
- field-evidence record requirements;
- diagnostics/drift/truncation dependency notes;
- fixture/golden replay proof requirements for restoration.

Required direct evidence must be parser-owned or parser-adjacent evidence
already authorized by a current contract. Fallback evidence must be bounded,
typed, and explicit. Forbidden fallback evidence should name common tempting
but unsafe substitutes.

Examples of forbidden fallbacks:

- workbook formulas reconstructing parser truth;
- dashboard or analytics labels;
- AI/model-provider guesses;
- approximate deck or archetype labels;
- private log notes without redaction and review;
- generic diagnostics pass status;
- local app readiness or runtime status;
- stale source values without review;
- external taxonomy labels.

## Evidence-Ledger And Field-Evidence Consumption

The matrix may consume evidence-ledger and runtime field-evidence artifacts
only as provenance metadata.

Allowed consumption:

- reference ledger entry IDs;
- reuse value-source, confidence, finality, drift, invariant, and degradation
  vocabulary;
- use field-evidence `review_required` as a lower-bound review signal;
- summarize whether direct/fallback evidence is present, missing, stale,
  conflicted, or degraded.

Forbidden consumption:

- changing the parser field value;
- overwriting parser output;
- suppressing parser output;
- writing workbook rows;
- changing webhook payloads;
- changing Apps Script behavior;
- changing runtime status schema;
- treating invariant or diagnostics pass status as parser truth;
- using field evidence to bypass a parser contract or fixture review.

## Review Rules For Restoring Fields After Drift

A field may be restored as parser-owned output after drift only when all
required gates are satisfied:

1. A field recovery row identifies the target field, current category, and
   required evidence.
2. A scoped Codex A problem representation or equivalent issue selects that
   field or small field family.
3. A scoped Codex B contract authorizes parser behavior or parser-adjacent
   recovery.
4. Codex C implements the smallest parser-owned change against that contract.
5. Synthetic or sanitized committed fixture evidence proves direct,
   equivalent, or bounded derivation behavior.
6. Golden replay, diagnostics, evidence-ledger, and protected-surface checks
   run as required by the scoped contract.
7. Codex E reviews the implementation and validation evidence.
8. Codex F/G handle submission and deployment only after normal approval.

The matrix alone satisfies none of those gates.

## Forbidden Promotion Rules

The following must never be promoted by this matrix:

- `approximate_analytics_only` to parser truth;
- `blocked_private_evidence` to parser truth without #434-approved evidence,
  redaction, review, and a scoped parser contract;
- `blocked_external_boundary` to parser truth without a scoped external
  evidence contract and parser contract;
- `review_required` to parser truth without resolving the review blocker;
- generic diagnostics `pass` to field-level parser truth;
- corpus coverage status to parser behavior readiness;
- previous/stale source availability to current parser support;
- AI, analytics, workbook, dashboard, or Apps Script output to parser truth.

## Relationship To #452 Through #456

Issues #452 through #456 are reserved or staged parser-recovery/evidence
follow-ups after #451. This contract must not solve them.

The matrix may define reusable row and category vocabulary for those future
issues. It must not:

- create those issue artifacts;
- implement watcher, comparison-report, recovery-packet, issue-draft,
  fixture-draft, or update workflows;
- activate #388;
- authorize private harvest;
- authorize fixture promotion;
- promote any corpus status.

Each later child issue must name its own source artifact, target artifact,
allowed inputs, forbidden inputs, output policy, validation evidence, and
stop conditions.

## Relationship To Mythic-Edge-Corpus #1 Through #6

After #451, the queued Mythic-Edge-Corpus automation sequence is:

1. local corpus package preview;
2. fail-if-unsafe PR validation;
3. release publishing;
4. `repository_dispatch` into Mythic Edge;
5. ratchet comparison;
6. auto-open baseline PR, intentionally last and review-gated.

This contract may inform that sequence's evidence labels and non-claims, but
it does not create corpus packages, publish releases, dispatch workflows,
compare ratchets, open baseline PRs, promote fixtures, or change corpus
status.

## Required Non-Claims

Every matrix object, row, future report, and handoff must preserve:

- `not_parser_truth`
- `not_source_recovery_authority`
- `not_fixture_promotion`
- `not_corpus_status_change`
- `not_private_harvest_authorization`
- `not_parser_behavior_readiness`
- `not_pipeline_activation_readiness`
- `not_merge_readiness`
- `not_deploy_readiness`
- `not_release_readiness`
- `not_production_behavior`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`

## Error Behavior

Future validators must fail closed when:

- a row uses an unknown recovery category;
- a row lacks required non-claims;
- a row lacks an output policy;
- a parser field has approximate or blocked evidence but parser output policy
  suggests restoration;
- a row contains raw/private markers, local absolute paths, raw hashes,
  source snippets, or private artifact references;
- a row references unknown evidence-ledger entries without
  `review_required=true`;
- a row attempts to use analytics, workbook, Apps Script, dashboard, or AI
  output as parser truth;
- a row changes readiness flags to true.

Expected failure status:

- `invalid_matrix`
- `invalid_row`
- `review_required`
- `blocked_private_marker`
- `blocked_local_artifact`
- `blocked_truth_boundary_violation`
- `needs_contract_update`

## Side Effects

Codex B side effects:

- writes only this contract artifact.

Future Codex C side effects, if authorized:

- may add static metadata helpers and tests;
- may write an implementation handoff;
- may not write local runtime artifacts, recovery packets, fixtures,
  manifests, expected outputs, corpus metadata, PR-assist outputs, private
  reports, or generated data.

No runtime side effects are authorized.

## Compatibility

The matrix must preserve existing evidence-ledger vocabulary and field
evidence validation rules.

The matrix must preserve existing #388 planning flags:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
evidence_pipeline_planning_ready_for_issue_388: false
file_writing_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
```

The matrix must not require workbook schema, webhook payload, Apps Script,
analytics schema, runtime status, golden replay manifest, or corpus manifest
changes.

## Codex C Implementation Scope

Codex C may implement:

- a static recovery matrix module;
- category and policy constants;
- validator helpers;
- seed rows for a small representative set of existing evidence-ledger field
  families;
- tests proving the anti-promotion rules and failure modes;
- an implementation handoff.

Codex C must not implement:

- parser extraction changes;
- watcher behavior;
- diagnostics or drift execution changes;
- recovery packet file writing;
- issue/fixture draft generation;
- fixture or manifest writing;
- corpus metadata mutation;
- private-evidence execution;
- runtime status, workbook, webhook, Apps Script, analytics, AI, or coaching
  changes.

## Required Codex C Validation

Suggested validation if implementation proceeds:

```bash
python3 -m pytest -q tests/test_field_recovery_matrix.py
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m ruff check src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_recovery_field_recovery_matrix.md src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_recovery_field_recovery_matrix.md src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_recovery_field_recovery_matrix.md src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

If Codex C chooses a docs-only implementation, replace the code/test paths
with the actual changed files and explain why no runtime tests were needed.

## Codex E Review Focus

Codex E should verify:

- no parser behavior changed;
- no private evidence was read or committed;
- recovery categories fail closed;
- approximate, blocked, unavailable, and review-required rows cannot restore
  parser output;
- evidence-ledger vocabulary is reused rather than forked;
- readiness flags remain false;
- #388 and #381 remain inactive;
- #434 remains the private-evidence gate;
- analytics/display policy does not become parser truth;
- protected-surface and secret/private-marker checks cover changed files.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/parser_recovery_field_recovery_matrix.md`.
- The contract defines field identity vocabulary, recovery categories, parser
  output policy, analytics/display policy, confidence/finality/degradation
  behavior, stale-source behavior, evidence requirements, review rules, and
  forbidden promotion rules.
- The contract preserves #388 non-activation and false readiness flags.
- The contract defines future Codex C/E validation expectations.
- No code, fixtures, manifests, expected outputs, corpus metadata, private
  evidence, recovery packets, or runtime artifacts are created by Codex B.

## Recommended Next Role

Codex C: Module Implementer for the Field Recovery Matrix static schema,
validator, representative seed rows, and focused tests.

Implementation is appropriate only if it remains metadata-only and preserves
all protected boundaries.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #451.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/451

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/387

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/537

Contract:
docs/contracts/parser_recovery_field_recovery_matrix.md

Base branch:
main

Goal:
Implement the Field Recovery Matrix as metadata-only schema/validation with
representative seed rows and focused tests.

Scope:
- Add a static report-only recovery matrix module, likely
  `src/mythic_edge_parser/app/field_recovery_matrix.py`.
- Add focused tests, likely `tests/test_field_recovery_matrix.py`.
- Reuse evidence-ledger value-source, confidence, finality, degradation, and
  review-required vocabulary.
- Prove approximate, blocked, unavailable, and review-required rows cannot
  restore parser output.
- Preserve false readiness flags and non-claims.
- Write `docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md`.

Protected boundaries:
- Do not change parser behavior, parser event classes, parser state final
  reconciliation, router semantics, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, analytics behavior, AI/model-provider behavior,
  coaching behavior, CI gates, merge readiness, deploy readiness, release
  readiness, production behavior, or final integration policy.
- Do not activate #388 or #381.
- Do not run or read private Player.log, UTC_Log, app-data, live MTGA,
  network, firewall/drop, packet, OS/router, diagnostics, drift, or private
  smoke checks.
- Do not create committed fixtures, golden replay manifests, expected-output
  files, fixture-promotion packets, proof files, metadata diff files,
  recovery packets, issue/fixture drafts, local watcher outputs, or
  local/generated artifacts.
- Do not promote blocked, report-only, private-evidence, external-boundary,
  approximate, fallback, or review-required rows to parser truth.
- Do not claim parser_behavior_ready, pipeline activation readiness,
  fixture-promotion readiness, field recovery readiness, private smoke
  success, release readiness, production readiness, analytics truth, AI
  truth, coaching truth, or full parser regression parity.

Validation:
- python3 -m pytest -q tests/test_field_recovery_matrix.py
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m ruff check src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py
- git diff --check
- python3 tools/check_agent_docs.py
- path-scoped secret/private marker scan
- path-scoped protected-surface check
- path-scoped validation selector

Expected output:
- Implementation summary
- Validation summary
- Remaining risks
- workflow_handoff block to Codex E
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/451"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/387"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/537"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #451 problem representation"
  target_artifact: "docs/contracts/parser_recovery_field_recovery_matrix.md"
  verdict: "field_recovery_matrix_contract_ready_for_metadata_implementation"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "a020311871738d4ea04d9244ac1635ef3936975c"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  evidence_pipeline_planning_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  validation:
    - "Codex B docs-only validation required before handoff"
  stop_conditions:
    - "Do not activate #388 or #381."
    - "Do not close #451, #388, or #434 without explicit lifecycle approval."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks."
    - "Do not create committed fixtures, golden replay manifests, expected outputs, fixture-promotion packets, proof files, metadata diff files, recovery packets, issue/fixture drafts, local watcher outputs, or local/generated artifacts."
    - "Do not change parser behavior, parser event classes, parser state final reconciliation, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics behavior, AI/model-provider behavior, coaching behavior, CI gates, merge readiness, deploy readiness, release readiness, production behavior, or final integration policy."
    - "Do not promote blocked, report-only, private-evidence, external-boundary, approximate, fallback, or review-required rows to parser truth."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, field recovery readiness, private smoke success, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
