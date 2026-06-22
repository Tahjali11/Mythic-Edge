# Parser Parity GRE Annotation Semantics Contract

## Module

`parser_parity_gre_annotation_semantics`

Plain English: this contract defines the next safe boundary for promoting
selected GRE annotation types into explicit parser-owned semantic facts. GRE
annotations are structured records inside Arena `GameStateMessage` payloads.
Mythic Edge already preserves raw annotation arrays and normalizes a small
marker set. This contract defines how future work may add a typed,
provenance-bearing semantic-fact layer for the #484 target annotation types
without copying external parser source, importing external logs, reading
private logs, changing downstream schemas, or claiming gameplay advice.

This Codex B pass writes only this contract. It does not implement code, open
a PR, activate #388 or #381, read private logs, run private harvest, create
fixtures, edit corpus metadata, change parser behavior, or claim readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/484
- Parent umbrella: https://github.com/Tahjali11/Mythic-Edge/issues/483
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/481
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/550
- Previous merge commit:
  `39248f5d9245d8f0f44bd3e5aabef3c84ade1d36`
- Base branch: `main`
- Target branch: `main`
- Contract branch: `codex/parser-parity-gre-annotation-semantics-484`
- Risk tier: High

Observed during this Codex B pass:

- The primary checkout was on a gone #455 branch with an unrelated modified
  `docs/project_roadmap.md` edit.
- To preserve unrelated local work, this contract was written in a clean
  sibling worktree on branch
  `codex/parser-parity-gre-annotation-semantics-484`.
- The clean worktree was created from `origin/main`.
- `HEAD` was `4cc363adeb8fa25b5f3f6ef28595aff7581c8e80`.
- The previous #481 merge commit
  `39248f5d9245d8f0f44bd3e5aabef3c84ade1d36` is present in
  `origin/main`.
- Issue #484 is open.
- Parent umbrella #483 is open.
- Pipeline tracker #388 is open and inactive.
- Parent private-evidence issue #434 is open.
- Issue #481 is closed and PR #550 is merged.

Current authorization facts to preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
```

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
- Issue #484
- Parent umbrella #483
- Pipeline tracker #388
- Parent private-evidence issue #434
- Issue #481 and PR #550
- `docs/contracts/parser_annotation_normalization.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_gre_turn_info.md`
- `docs/contracts/parser_owned_fact_capture_tracker.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md`
- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- `tests/test_gre_annotations_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_gameplay_actions.py`
- `tests/test_parser_owned_fact_tracker.py`

No Manasight source code, Manasight raw logs, Manasight corpus payloads,
private `Player.log`, private `UTC_Log`, app-data, live MTGA, diagnostics,
network, watcher, private smoke, or private harvest evidence was copied,
imported, summarized, or read.

## Owning Layer

Primary owning layer: Parser.

Supporting layer: Corpus / Provenance.

`src/mythic_edge_parser/parsers/gre/annotations.py` owns GRE annotation
normalization. `src/mythic_edge_parser/parsers/gre/game_state.py` owns the
additive `GameStateEvent.payload["normalized_annotations"]` payload field.
Corpus / Provenance may later track which semantic facts have synthetic,
reviewed, or golden evidence, but corpus metadata does not own parser truth.

## Internal Project Area

Primary: Parser.

Supporting:

- Corpus / Provenance, for future evidence, fixture, golden replay, and
  parser-owned fact tracker integration.
- Quality / Governance, for workflow, contract, and protected-surface review.

This contract is not analytics, AI, coaching, workbook/transport, local app,
release readiness, production behavior, private-evidence execution, or #388
activation work.

## Truth Owner

Truth owner for normalized GRE annotation semantic facts:

- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`, only as the carrier of
  additive normalized GameState payload data

Truth owner for downstream gameplay-action facts remains:

- `src/mythic_edge_parser/app/gameplay_actions.py`

Truth owner for parser-owned fact tracking remains:

- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- its future public-safe matrix, ledger, and report artifacts

This contract does not make annotations, corpus metadata, public reference
taxonomies, downstream analytics, workbook formulas, dashboard logic, Apps
Script, webhook transport, AI output, or coaching output a truth owner for
gameplay facts.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code in Codex B. If a future Codex C pass
is explicitly authorized after review, the allowed data flow is:

```text
GameStateMessage.annotations / persistentAnnotations
  -> preserved raw GameState payload arrays
  -> existing normalized annotation records
  -> additive typed semantic fact records
  -> optional downstream parser consumers
  -> optional future corpus/provenance evidence summaries
```

Forbidden reverse flow:

- corpus metadata must not rewrite normalized annotation semantics;
- parser-owned fact tracker rows must not become parser behavior;
- gameplay-action consumers must not infer hidden cards from annotation
  semantic facts;
- analytics, AI, workbook, webhook, and Apps Script surfaces must not define
  parser annotation truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_parity_gre_annotation_semantics.md`

Potential future implementation files, only if separately authorized:

- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `tests/test_gre_annotations_parser.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`, only for additive
  payload compatibility if needed
- `tests/test_gre_game_state_parser.py`
- `docs/implementation_handoffs/parser_parity_gre_annotation_semantics_comparison.md`

Potential future evidence or tracker files, only if separately authorized:

- synthetic public-safe fixtures under existing fixture directories;
- parser-owned fact tracker matrix fixtures or public-safe report fixtures;
- golden replay fixture/manifest additions after separate fixture-promotion
  authority.

Referenced but not behavior-owned by this contract:

- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- workbook/webhook/App Script/output/analytics/AI surfaces

## Observed Current Behavior

Current `annotations.py` behavior:

- Normalizes raw annotation records into
  `object: "mythic_edge_gre_annotation"`.
- Normalizes collection payloads into
  `object: "mythic_edge_gre_annotations"`.
- Preserves `source_array`, `source_index`, `persistent`, `annotation_id`,
  `type_names`, `primary_type`, `affected_ids`, `details`,
  `detail_values`, `categories`, `markers`, `source_evidence`,
  `evidence_status`, `value_source`, `confidence`, `degradation_flags`, and
  `review_required`.
- Preserves unknown annotation type names in `type_names`.
- Degrades malformed annotation sections, malformed records, malformed types,
  malformed affected IDs, malformed details, malformed detail keys, malformed
  detail string values, incomplete object replacements, and malformed
  diff-deleted persistent annotation IDs.
- Recognizes these marker types:
  - `AnnotationType_ObjectIdChanged`
  - `AnnotationType_ZoneTransfer`
  - `AnnotationType_ResolutionStart`
  - `AnnotationType_ResolutionComplete`
  - `AnnotationType_NewTurnStarted`
  - `AnnotationType_RevealedCardDeleted`
  - `AnnotationType_Shuffle`
  - `AnnotationType_UserActionTaken`
  - `AnnotationType_ManaPaid`
  - `AnnotationType_AbilityInstanceDeleted`
- Builds special summaries only for object replacement and zone transfer.

Current #484 target annotation surface:

- `AnnotationType_DamageDealt`
- `AnnotationType_CounterAdded`
- `AnnotationType_TargetSpec`
- `AnnotationType_ModifiedLife`
- `AnnotationType_PowerToughnessModCreated`
- `AnnotationType_TriggeringObject`
- `AnnotationType_ManaPaid`
- `AnnotationType_UserActionTaken`
- `AnnotationType_Scry`
- `AnnotationType_Shuffle`
- `AnnotationType_Designation`
- `AnnotationType_ChoiceResult`
- `AnnotationType_LinkInfo`

Current gap against the target surface:

| Annotation type | Current state | Gap |
| --- | --- | --- |
| `AnnotationType_DamageDealt` | Preserved only as a raw/generic `type_names` value when present. | No explicit `damage_dealt` semantic fact. |
| `AnnotationType_CounterAdded` | Preserved only as a raw/generic `type_names` value when present. | No explicit `counter_added` semantic fact. |
| `AnnotationType_TargetSpec` | Preserved only as a raw/generic `type_names` value when present. | No explicit `target_spec` semantic fact. |
| `AnnotationType_ModifiedLife` | Preserved only as a raw/generic `type_names` value when present. | No explicit `modified_life` semantic fact. |
| `AnnotationType_PowerToughnessModCreated` | Preserved only as a raw/generic `type_names` value when present. | No explicit `power_toughness_mod_created` semantic fact. |
| `AnnotationType_TriggeringObject` | Preserved only as a raw/generic `type_names` value when present. | No explicit `triggering_object` semantic fact. |
| `AnnotationType_ManaPaid` | Recognized as marker `mana_paid`; generic details preserved. | Marker only; no typed semantic fact. |
| `AnnotationType_UserActionTaken` | Recognized as marker `user_action_taken`; generic details preserved. | Marker only; no typed semantic fact. |
| `AnnotationType_Scry` | Preserved only as a raw/generic `type_names` value when present. | No explicit `scry` semantic fact. |
| `AnnotationType_Shuffle` | Recognized as marker `shuffle`; generic details preserved. | Marker only; no typed semantic fact. |
| `AnnotationType_Designation` | Preserved only as a raw/generic `type_names` value when present. | No explicit `designation` semantic fact. |
| `AnnotationType_ChoiceResult` | Preserved only as a raw/generic `type_names` value when present. | No explicit `choice_result` semantic fact. |
| `AnnotationType_LinkInfo` | Preserved only as a raw/generic `type_names` value when present. | No explicit `link_info` semantic fact. |

Current `game_state.py` behavior:

- Preserves raw `annotations` and `persistent_annotations`.
- Adds `normalized_annotations` by calling `normalize_annotation_arrays()`.
- Does not change parser event classes, workbook rows, webhook payloads, Apps
  Script, output transport, analytics, or AI surfaces.

## Problem Statement

Mythic Edge can preserve many GRE annotation records, but several
competitive-relevant annotation types remain generic strings plus generic
detail lists. That is safe, but it makes future parser-owned fact work harder
because downstream consumers cannot distinguish "this type was preserved" from
"this type has a reviewed semantic projection."

The project needs a narrow semantic-fact layer that answers:

- which selected annotation type was observed;
- where it came from in the original annotation arrays;
- what raw details were normalized;
- which type-specific semantic fields are known, unknown, degraded, or
  review-required;
- whether the fact is observed, derived, unknown, or conflict;
- whether the fact is synthetic-only, report-only, or later confirmed by
  golden replay evidence.

## First Bad Value

The first bad value is any annotation semantic field, parser-owned fact
tracker row, corpus report, golden replay expectation, gameplay-action output,
ledger entry, analytics ingest row, workbook field, AI summary, or handoff
that treats generic annotation preservation as any of the following:

- proven semantic support for all target annotation types;
- hidden-card truth;
- complete decklist truth;
- player intent;
- strategic advice;
- player-mistake proof;
- exact causal game truth;
- parser behavior readiness;
- #388 or #381 activation readiness;
- fixture promotion approval;
- corpus status movement approval;
- release, deploy, production, analytics, AI, or coaching readiness.

## Scope Decision

Recommended future path: additive semantic-fact planning first.

This contract approves a future design boundary for typed GRE annotation
semantic facts. It does not authorize Codex B implementation.

If later explicitly authorized, Codex C may extend `annotations.py` with
additive semantic-fact records for the #484 target surface and focused
synthetic tests. Codex C must preserve existing normalized annotation record
shape and raw GameState annotation preservation.

The narrow future implementation path is:

1. Add semantic fact vocabulary and constants.
2. Add a deterministic semantic fact builder from existing normalized records.
3. Add collection-level summaries such as `semantic_fact_count`,
   `semantic_kinds`, and `semantic_facts`.
4. Keep unknown/future annotation types preserved in `type_names` without
   failing parsing.
5. Add focused synthetic unit tests for every #484 target annotation type.
6. Route any golden replay, parser-owned fact tracker, or corpus status work
   to a later explicit evidence/promotion issue unless a future handoff
   authorizes those files.

Codex C must route back to Codex B or Codex A if the target semantic facts
cannot be represented from observed annotation fields without hidden inference,
raw private evidence, downstream schema changes, or parser behavior changes
outside additive annotation normalization.

## Public Interface

Future implementation may add these logical public constants:

```python
ANNOTATION_SEMANTIC_FACT_OBJECT = "mythic_edge_gre_annotation_semantic_fact"
ANNOTATION_SEMANTICS_SCHEMA_VERSION = "parser_gre_annotation_semantics.v1"
```

Future implementation may add these logical helper behaviors, exact Python
names subject to implementation review:

```python
def semantic_facts_for_record(record: Mapping[str, object]) -> list[dict[str, object]]:
    ...

def semantic_facts_for_collection(
    normalized_annotations: Mapping[str, object],
) -> dict[str, object]:
    ...
```

Required compatibility:

- `normalize_annotation_record()` must continue returning existing record
  fields.
- `normalize_annotation_arrays()` must continue returning existing collection
  fields.
- Existing `marker_types`, `object_replacements`, `zone_transfers`,
  `annotation_categories_for_instance()`, and `replacement_instance_ids()`
  behavior must remain compatible.
- Any new fields must be additive.
- Existing tests for annotations, GameState payloads, and gameplay actions
  must continue to pass unless a later implementation contract explicitly
  authorizes a behavior change.

## Semantic Fact Shape

Every semantic fact must be JSON-serializable and public-safe.

Required logical shape:

```yaml
object: "mythic_edge_gre_annotation_semantic_fact"
schema_version: "parser_gre_annotation_semantics.v1"
semantic_kind: "damage_dealt"
source_array: "annotations"
source_index: 0
persistent: false
annotation_id: 123
raw_type_names:
  - "AnnotationType_DamageDealt"
primary_type: "AnnotationType_DamageDealt"
affected_ids: []
normalized_details: []
semantic_fields: {}
field_statuses: {}
value_source: "observed"
confidence: "low"
degradation_flags: []
review_required: true
non_claims: []
```

Required fields:

- `object`
- `schema_version`
- `semantic_kind`
- `source_array`
- `source_index`
- `persistent`
- `annotation_id`
- `raw_type_names`
- `primary_type`
- `affected_ids`
- `normalized_details`
- `semantic_fields`
- `field_statuses`
- `value_source`
- `confidence`
- `degradation_flags`
- `review_required`
- `non_claims`

Semantic facts must not include raw annotation dictionaries, raw log text,
local paths, private decklists, external corpus payloads, model output, or
advice text.

## Target Semantic Kinds

V1 target semantic kinds:

| Raw annotation type | Semantic kind | V1 field policy |
| --- | --- | --- |
| `AnnotationType_DamageDealt` | `damage_dealt` | May expose observed amount/source/target fields only when present in normalized details. Missing amount or target context degrades. |
| `AnnotationType_CounterAdded` | `counter_added` | May expose observed counter type, amount, and target IDs only when present. Missing counter identity degrades. |
| `AnnotationType_TargetSpec` | `target_spec` | May expose observed target IDs, target player/seat hints, target zone hints, and target type labels only when present. Ambiguous targets require review. |
| `AnnotationType_ModifiedLife` | `modified_life` | May expose observed life total, life delta, and player/seat hints only when present. Must not infer winners or game result. |
| `AnnotationType_PowerToughnessModCreated` | `power_toughness_mod_created` | May expose observed power/toughness deltas and affected IDs only when present. Must not infer final combat math. |
| `AnnotationType_TriggeringObject` | `triggering_object` | May expose observed triggering object IDs and controller hints only when present. Must not infer full stack or intent. |
| `AnnotationType_ManaPaid` | `mana_paid` | May expose observed mana symbols/amounts/payer/source hints only when present. Must not infer optimal sequencing. |
| `AnnotationType_UserActionTaken` | `user_action_taken` | May expose observed user-action labels, choice IDs, or seat hints only when present. Must not infer player intent or mistakes. |
| `AnnotationType_Scry` | `scry` | May expose observed scry count and player/seat hints only when present. Must not expose hidden card identities. |
| `AnnotationType_Shuffle` | `shuffle` | May expose observed zone/player/library hints only when present. Must not prove randomization quality. |
| `AnnotationType_Designation` | `designation` | May expose observed designation labels and target IDs only when present. Must not classify archetypes or strategy. |
| `AnnotationType_ChoiceResult` | `choice_result` | May expose observed choice IDs, selected option labels, and selected target IDs only when present. Must not recommend choices. |
| `AnnotationType_LinkInfo` | `link_info` | May expose observed linked object IDs and link labels only when present. Must not infer hidden relationships beyond observed links. |

The field policy is intentionally conservative. If Arena detail keys vary or
are unknown, the future implementation must preserve normalized detail values
and mark the semantic field as `unknown`, `degraded`, or `review_required`
instead of fabricating a value.

## Normalized Field Policy

Allowed `semantic_fields` values are derived only from already-normalized
annotation record fields:

- `type_names`
- `primary_type`
- `affected_ids`
- `annotation_id`
- `details`
- `detail_values`
- `categories`
- `markers`

Allowed field value kinds:

- strings;
- integers;
- booleans;
- lists of strings, integers, or booleans;
- empty string `""` for scalar unknowns;
- empty list `[]` for list unknowns.

Forbidden field value kinds:

- raw annotation dictionaries;
- raw `Player.log` lines;
- raw external corpus payloads;
- local absolute paths;
- private decklist entries;
- model output;
- nested unbounded raw payloads;
- advice text;
- scores, EV, win probabilities, or player-mistake labels.

Every semantic field must have a matching `field_statuses` entry:

- `observed`
- `derived`
- `unknown`
- `degraded`
- `conflict`
- `review_required`

## Value Source, Confidence, And Degradation

Allowed `value_source` values:

- `observed`
- `derived`
- `unknown`
- `conflict`

Rules:

- Raw type names, affected IDs, annotation IDs, and normalized details are
  `observed`.
- Semantic kind names and type-specific field projections are `derived` from
  observed annotation fields.
- Missing or unsupported detail values are `unknown`.
- Contradictory details that cannot be represented deterministically are
  `conflict`.

Allowed `confidence` values:

- `high`
- `medium`
- `low`
- `unknown`
- `review_required`

Rules:

- `high` is allowed only for exact raw type-name recognition and simple
  observed fields with no degradation.
- `medium` is allowed for conservative type-specific projections from
  observed detail fields.
- `low` is required when the record has malformed or incomplete supporting
  fields.
- `unknown` is required when the semantic type is recognized but no trusted
  semantic fields are present.
- `review_required` is required for conflicts, unsupported target shapes, or
  policy-sensitive claims.

Required degradation flags:

- `semantic_type_preserved_generic_only`
- `semantic_detail_missing`
- `semantic_detail_malformed`
- `semantic_detail_unsupported`
- `semantic_field_unknown`
- `semantic_field_conflict`
- `semantic_target_ambiguous`
- `hidden_information_boundary`
- `external_reference_only`
- `requires_private_evidence_review`
- `requires_golden_replay_confirmation`

Future implementation may add narrower flags, but it must not remove the
existing annotation-normalization degradation flags from
`parser_annotation_normalization.md`.

## Required Non-Claims

Every semantic fact, collection-level semantic summary, future parser-owned
fact tracker row, and future report packet must preserve these non-claims:

- `not_hidden_card_truth`
- `not_complete_decklist_truth`
- `not_archetype_truth`
- `not_player_intent_truth`
- `not_gameplay_advice`
- `not_player_mistake_label`
- `not_optimal_play_truth`
- `not_exact_causal_truth`
- `not_match_result_truth`
- `not_game_result_truth`
- `not_workbook_truth`
- `not_webhook_truth`
- `not_apps_script_truth`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`
- `not_parser_behavior_readiness`
- `not_pipeline_activation_readiness`
- `not_fixture_promotion`
- `not_corpus_status_change`
- `not_release_readiness`
- `not_deploy_readiness`
- `not_production_behavior`

Missing non-claims are invalid. Additional non-claims are allowed only if they
are public-safe and do not weaken this required set.

## Parser-Owned Fact Tracker Relationship

Issue #481 created the parser-owned fact capture tracker boundary. #484 may
later feed that tracker, but this contract does not edit tracker code or
tracker fixtures.

Future tracker rows, if separately authorized, should use fact IDs such as:

- `gameplay_action.gre_annotation.damage_dealt`
- `gameplay_action.gre_annotation.counter_added`
- `gameplay_action.gre_annotation.target_spec`
- `gameplay_action.gre_annotation.modified_life`
- `gameplay_action.gre_annotation.power_toughness_mod_created`
- `gameplay_action.gre_annotation.triggering_object`
- `gameplay_action.gre_annotation.mana_paid`
- `gameplay_action.gre_annotation.user_action_taken`
- `gameplay_action.gre_annotation.scry`
- `gameplay_action.gre_annotation.shuffle`
- `gameplay_action.gre_annotation.designation`
- `gameplay_action.gre_annotation.choice_result`
- `gameplay_action.gre_annotation.link_info`

Tracker rows must begin as `not_captured`, `deferred_feature_expansion`, or
`review_required` unless a future implementation package includes
contract-authorized synthetic or reviewed evidence. A tracker row must not
skip directly to `promoted_golden_fixture` or readiness states.

## Fixture And Evidence Strategy

The narrowest safe validation path is synthetic-first:

1. Unit-level synthetic annotation records for each #484 target type.
2. Collection-level tests proving multiple semantic facts preserve order and
   source indexes.
3. GameState payload compatibility tests proving raw arrays are preserved and
   additive semantic summaries do not break existing payload consumers.
4. Gameplay-action regression tests only if future semantic facts are consumed
   by gameplay actions.
5. Golden replay confirmation only after separate fixture-promotion authority.
6. Parser-owned fact tracker or corpus metadata updates only after separate
   evidence/tracker authority.

Committed fixtures must be synthetic or sanitized Mythic Edge-owned data. They
must not contain Manasight logs, Manasight raw corpus payloads, private
`Player.log` excerpts, private `UTC_Log` excerpts, decklists, strategy notes,
generated private artifacts, runtime artifacts, workbook exports, SQLite
files, credentials, tokens, API keys, or webhook URLs.

Facts may be described as stronger than synthetic/report-only only after
committed golden replay or reviewed sanitized evidence exists under a later
contract.

## Error Behavior

Malformed or incomplete input must fail closed:

- Missing or malformed annotation records produce degraded placeholders, not
  exceptions in normal parser use.
- Unknown annotation type names remain preserved in `type_names` without
  failing parsing.
- Target annotation types with missing detail keys may produce semantic facts
  with unknown fields, low confidence, degradation flags, and review-required
  status.
- Contradictory detail values must use `conflict` or `review_required`, not
  arbitrary winner selection.
- Unsupported detail keys must remain generic normalized detail values until a
  later contract names them.
- Hidden-card, advice, player-mistake, exact-EV, archetype, decklist,
  analytics, AI, or coaching claims must be rejected or represented only as
  non-claims.

## Side Effects

This Codex B contract has exactly one intended side effect:

- writes `docs/contracts/parser_parity_gre_annotation_semantics.md`

Future implementation must not have side effects beyond files explicitly
authorized by a later Codex C handoff. In particular, future implementation
must not:

- read private logs;
- write local/private artifacts;
- mutate corpus manifests or session ledgers;
- create GitHub issues or PRs;
- edit workbook/webhook/App Script/output/analytics/AI surfaces;
- enable #388 or #381;
- change parser event classes;
- change match/game identity or final reconciliation.

## Dependency Order

If future implementation is explicitly authorized, use this order:

1. Extend semantic vocabulary in `annotations.py` without changing existing
   public helper behavior.
2. Add focused `tests/test_gre_annotations_parser.py` coverage for every #484
   target annotation type.
3. Add GameState payload compatibility coverage only if the collection payload
   shape changes additively.
4. Run existing gameplay-action tests to prove current consumers still work.
5. Write
   `docs/implementation_handoffs/parser_parity_gre_annotation_semantics_comparison.md`.
6. Route to Codex E for contract review.

Do not update corpus metadata, golden replay manifests, tracker fixtures, or
downstream consumers unless a future handoff explicitly authorizes that broader
scope.

## Compatibility

Must remain compatible:

- raw `annotations` field in `GameStateEvent.payload`;
- raw `persistent_annotations` field in `GameStateEvent.payload`;
- `diff_deleted_persistent_annotation_ids`;
- existing `normalized_annotations` collection fields;
- existing normalized record fields;
- existing marker names;
- `annotation_categories_for_instance()`;
- `replacement_instance_ids()`;
- `gameplay_actions.py` behavior covered by existing tests;
- parser event class schemas;
- workbook/webhook/App Script/output payload boundaries.

Unknown annotation types must continue to be preserved, not rejected.

## Tests Required For Later Implementation

Focused validation, if implementation is later authorized:

```bash
python3 -m pytest -q tests/test_gre_annotations_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
git diff --check
```

Additional validation if future implementation touches adjacent surfaces:

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_parser_regressions.py
python3 -m pytest -q tests/test_evidence_ledger.py
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
```

Validation must not be described as parser behavior readiness, #388
activation, fixture-promotion readiness, release readiness, deploy readiness,
production readiness, analytics truth, AI truth, or coaching truth.

## Acceptance Criteria

- This contract identifies current Mythic Edge annotation fields and gaps
  against the #484 target surface.
- The target semantic fact shape includes source array, source index, raw type
  names, normalized detail fields, value source, confidence, degradation flags,
  review-required status, and non-claims.
- Unknown annotation types remain preserved without parser failure.
- Target semantic kinds are explicit and additive.
- Field policy forbids fabricated hidden-card, gameplay-advice,
  player-mistake, archetype, decklist, analytics, AI, and coaching claims.
- Synthetic fixture requirements are defined for a later implementation.
- Golden replay and parser-owned fact tracker movement are deferred to later
  explicit evidence authority.
- Protected parser/runtime/workbook/webhook/App Script/output/analytics/AI
  surfaces remain unchanged.

## Open Questions And Contract Risks

- Arena detail keys for some #484 target annotation types may vary by client
  version, format, event, or card mechanic.
- Some target annotation types may require more than one synthetic example to
  cover common detail-key variants.
- Some semantic fields may remain unknown until reviewed sanitized evidence
  exists.
- Promoting semantic facts into gameplay-action outputs may need a separate
  contract if it changes action classification.
- Golden replay confirmation and parser-owned fact tracker integration remain
  separate lifecycle steps.

## Recommended Next Role

Codex E should review this contract for scope, truth boundary, target semantic
fact shape, non-claims, protected-surface coverage, and whether the future
Codex C scope is narrow enough.

Codex C should wait for explicit implementation authorization after contract
review/submission before editing parser code, tests, fixtures, tracker rows,
or corpus metadata.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #484.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/484

Parent umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/483

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Contract:
docs/contracts/parser_parity_gre_annotation_semantics.md

Review focus:
- Verify the contract is planning-only and does not implement code.
- Verify it preserves parser_behavior_ready=false, pipeline_activation_ready_for_issue_388=false, private_harvest_authorized=false, fixture_promotion_authorized=false, corpus_status_change_authorized=false, and implementation_authorized=false.
- Verify it does not copy Manasight source code, import external logs, read private logs, or authorize private harvest.
- Verify current Mythic Edge annotation support and gaps are accurately described.
- Verify the semantic fact shape carries source array, source index, raw type names, normalized detail fields, value source, confidence, degradation flags, review-required status, and non-claims.
- Verify unknown annotation types remain preserved without failing parsing.
- Verify future Codex C scope is additive and does not change parser event classes, parser state final reconciliation, match/game identity, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics truth, AI truth, or coaching truth.
- Verify synthetic-first validation is required before any stronger support claim.

Suggested validation:
- git diff --check
- python3 tools/check_secret_patterns.py docs/contracts/parser_parity_gre_annotation_semantics.md
- python3 tools/check_protected_surfaces.py --base origin/main

Lead with findings. If clean, route to Codex F for docs-only submission or Codex C only if the user explicitly authorizes implementation.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/484"
  parent_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/483"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/481"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/550"
  previous_merge_commit: "39248f5d9245d8f0f44bd3e5aabef3c84ade1d36"
  completed_thread: "B"
  next_thread: "E"
  verdict: "gre_annotation_semantic_parity_contract_written"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-parity-gre-annotation-semantics-484"
  target_artifact: "docs/contracts/parser_parity_gre_annotation_semantics.md"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
```
