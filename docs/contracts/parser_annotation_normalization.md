# Parser Annotation Normalization Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/113

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/50

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/112

Previous merge commit: `69896381a0c5d69253ef667d4575cdd0fd7e7f2a`

Branch target: `codex/parser-reliability-intelligence`

This contract defines first-class GRE annotation normalization for Mythic Edge.
It is a contract artifact only. It does not implement code, change parser
behavior, change workbook schema, change webhook payloads, change Apps Script,
infer hidden cards, classify archetypes, reconstruct missing GameState data, or
commit raw private `Player.log` excerpts.

## Module

Parser GRE annotation normalization.

Plain English: this module turns raw GRE `GameStateMessage` annotation arrays
into a stable, deterministic, parser-owned annotation evidence view. It must
preserve raw annotation arrays exactly as current GameState payload evidence
while giving parser-adjacent consumers one shared way to read annotation types,
details, affected IDs, object replacements, zone-transfer categories, and
well-known marker signals.

Risk tier: High.

The risk is high because annotation evidence sits between raw Arena log
payloads and gameplay/action interpretation. A weak normalizer could quietly
turn malformed, incomplete, or consumer-specific annotation interpretation into
parser truth.

## Owning Layer

Owning layer: parser and state interpretation, specifically GRE GameState
normalization support.

Truth boundary:

- MTGA `Player.log` annotation arrays are local observable evidence, not
  absolute game truth.
- `src/mythic_edge_parser/parsers/gre/game_state.py` continues to own raw
  GameState payload construction and must continue preserving raw
  `annotations`, raw `persistent_annotations`, and normalized
  `diff_deleted_persistent_annotation_ids`.
- The annotation normalization module owns normalized annotation evidence
  records and annotation-derived helper summaries.
- This module does not own match identity, game identity, final reconciliation,
  deduplication, parser event class schema, workbook rows, webhook delivery,
  Apps Script behavior, output transport, card-performance metrics, archetype
  classification, decklist completion, or hidden-information inference.
- `gameplay_actions.py`, `opponent_card_observations.py`, diagnostics mode,
  golden replay, the evidence ledger, workbook sheets, dashboards, Apps Script,
  output transport, and AI/model output are consumers unless a later contract
  explicitly changes ownership.

Parser truth must stay parser-owned. Workbook formulas, dashboard logic,
webhook transport, Apps Script, analytics surfaces, and AI output must not
become the source of truth for annotation interpretation.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_annotation_normalization.md`

Future implementation artifacts owned by this contract, if authorized by the
Codex C implementation pass:

- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `tests/test_gre_annotations_parser.py`
- `docs/implementation_handoffs/parser_annotation_normalization_comparison.md`

Narrow integration surfaces allowed only when needed to satisfy this contract:

- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_game_state_parser.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `tests/test_gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_opponent_card_observations.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `tests/test_parser_diagnostics_mode.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/test_golden_replay_harness.py`
- optional committed sanitized or synthetic fixture/manifest files under
  existing fixture locations, only if required by implementation tests

Referenced but not silently owned:

- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_opponent_card_observations.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence` after PR #112:

- Issue #113 is open and belongs to tracker #47.
- Tracker #47 remains open.
- Related evidence issue #11 remains open.
- PR #112 is merged into `codex/parser-reliability-intelligence` at
  `69896381a0c5d69253ef667d4575cdd0fd7e7f2a`.
- `game_state.py` shallow-copies raw `gsm.annotations` to
  `payload["annotations"]`; non-list sources become `[]`.
- `game_state.py` shallow-copies raw `gsm.persistentAnnotations` to
  `payload["persistent_annotations"]`; non-list sources become `[]`.
- `game_state.py` normalizes `gsm.diffDeletedPersistentAnnotationIds` to
  `payload["diff_deleted_persistent_annotation_ids"]` using
  `api_common.normalize_int_list()`.
- Focused GameState parser tests protect raw preservation, shallow list
  copying, malformed-section fallback, and integer-list normalization.
- `app/extractors.py` returns only dict annotation entries when downstream
  callers use `_game_state_annotations(payload)`.
- `gameplay_actions.py` currently contains local annotation helpers for
  annotation type lists, integer and string detail values, object replacement
  hints, zone-transfer categories, resolution signals, new-turn-started
  detection, revealed-card cleanup suppression, and user-action related
  gameplay behavior.
- `opponent_card_observations.py` consumes action-entry `annotation_types` and
  `annotation_categories` as possible `source_evidence="annotation"`, but it
  does not own annotation parsing.
- `parser_opponent_card_observations.md` intentionally leaves future
  annotation normalization open for stronger annotation evidence guarantees.
- `parser_feature_equity_with_manasight.md` identifies a dedicated GRE
  annotation helper layer as a Mythic Edge feature-equity gap.
- No dedicated `src/mythic_edge_parser/parsers/gre/annotations.py` module
  exists yet.

## Required Guarantees

### Raw Evidence Preservation

- Raw `payload["annotations"]` must remain present and unchanged in meaning.
- Raw `payload["persistent_annotations"]` must remain present and unchanged in
  meaning.
- Raw list preservation remains shallow-copy behavior unless a later
  GameState payload contract explicitly changes it.
- Normalized annotation records must not replace or delete raw annotation
  arrays.
- Normalized annotation records should not duplicate the full raw annotation
  dictionary by default. Raw evidence remains available in the preserved raw
  arrays.

### First-Class Normalized View

V1 should expose annotation normalization through a parser-side helper module
and add an additive `GameStateEvent.payload["normalized_annotations"]` field.

The additive GameState payload field is authorized by this contract because it
is parser-owned annotation evidence. It must remain local parser payload data
and must not imply a workbook schema, webhook payload, Apps Script, runtime
status schema, or AI-facing output change.

If implementation discovers that adding `normalized_annotations` would force a
protected downstream schema migration, Codex C must stop and route back for a
contract or problem-representation loopback instead of broadening scope.

### Public API

Exact Python names may vary during implementation, but the public behavior must
preserve this shape:

```python
ANNOTATION_RECORD_OBJECT = "mythic_edge_gre_annotation"
ANNOTATION_COLLECTION_OBJECT = "mythic_edge_gre_annotations"
SCHEMA_VERSION = "parser_gre_annotations.v1"

def normalize_annotation_record(
    raw_annotation: object,
    *,
    source_array: str,
    source_index: int,
) -> dict[str, object]:
    ...

def normalize_annotation_arrays(
    *,
    annotations: object,
    persistent_annotations: object = None,
    diff_deleted_persistent_annotation_ids: object = None,
) -> dict[str, object]:
    ...

def annotation_categories_for_instance(
    normalized_annotations: Mapping[str, object],
    instance_id: int,
) -> list[str]:
    ...

def replacement_instance_ids(
    normalized_annotations: Mapping[str, object],
) -> dict[int, int]:
    ...
```

Required API behavior:

- Return JSON-serializable dictionaries and lists.
- Preserve input objects without mutation.
- Avoid filesystem writes.
- Avoid importing workbook, webhook, Apps Script, output transport, OpenAI, or
  model-provider surfaces.
- Never raise for malformed annotation input in normal parser use. Malformed
  values must become empty normalized fields plus degradation flags.
- Use deterministic ordering based on source array order and source index.

## Normalized Payload Shape

### Collection Payload

Required logical shape for `payload["normalized_annotations"]`:

```yaml
object: "mythic_edge_gre_annotations"
schema_version: "parser_gre_annotations.v1"
total_records: 2
degraded_records: 0
review_required: false
source_arrays:
  annotations: 1
  persistent_annotations: 1
annotation_types:
  - "AnnotationType_ZoneTransfer"
marker_types:
  - "zone_transfer"
diff_deleted_persistent_annotation_ids: []
object_replacements:
  - original_instance_id: 11
    new_instance_id: 99
    source_array: "annotations"
    source_index: 0
    confidence: "high"
zone_transfers:
  - affected_ids: [99]
    categories: ["CastSpell"]
    source_zone_ids: [31]
    destination_zone_ids: [27]
    semantic_hints: ["cast_hint"]
    source_array: "annotations"
    source_index: 1
    confidence: "medium"
degradation_flags: []
records:
  - normalized_annotation_record
```

Collection field rules:

- `total_records` counts normalized records from both transient and persistent
  annotation arrays.
- `degraded_records` counts records with nonempty `degradation_flags` or
  `evidence_status` of `degraded`, `unknown`, or `conflict`.
- `review_required` is true when any record or collection-level input requires
  review.
- `source_arrays.annotations` and `source_arrays.persistent_annotations` count
  records produced from each source array.
- `annotation_types` is an ordered, de-duplicated union of record
  `type_names`.
- `marker_types` is an ordered, de-duplicated union of recognized marker names.
- `diff_deleted_persistent_annotation_ids` uses the same normalization policy
  as `api_common.normalize_int_list()`.
- `object_replacements` and `zone_transfers` summarize only observed
  annotation evidence; they must not reconstruct missing GameState objects.

### Record Payload

Required logical shape:

```yaml
object: "mythic_edge_gre_annotation"
schema_version: "parser_gre_annotations.v1"
source_array: "annotations"
source_index: 0
persistent: false
annotation_id: 123
type_names:
  - "AnnotationType_ZoneTransfer"
primary_type: "AnnotationType_ZoneTransfer"
affected_ids: [99]
details:
  - key: "category"
    value_ints: []
    value_strings: ["CastSpell"]
    value_bools: []
    degradation_flags: []
detail_values:
  category: ["CastSpell"]
  orig_id: []
  new_id: []
  zone_src: [31]
  zone_dest: [27]
categories:
  - "CastSpell"
markers:
  zone_transfer: true
  object_id_changed: false
  resolution_start: false
  resolution_complete: false
  new_turn_started: false
  revealed_card_deleted: false
  shuffle: false
  user_action_taken: false
  mana_paid: false
  ability_instance_deleted: false
object_replacement:
  original_instance_id: ""
  new_instance_id: ""
zone_transfer:
  affected_ids: [99]
  categories: ["CastSpell"]
  source_zone_ids: [31]
  destination_zone_ids: [27]
  semantic_hints: ["cast_hint"]
source_evidence: "annotation"
evidence_status: "observed"
value_source: "observed"
confidence: "high"
degradation_flags: []
review_required: false
```

Required record fields:

- `object`
- `schema_version`
- `source_array`
- `source_index`
- `persistent`
- `annotation_id`
- `type_names`
- `primary_type`
- `affected_ids`
- `details`
- `detail_values`
- `categories`
- `markers`
- `object_replacement`
- `zone_transfer`
- `source_evidence`
- `evidence_status`
- `value_source`
- `confidence`
- `degradation_flags`
- `review_required`

Empty numeric values in JSON-facing payloads should use `""` for compatibility
with existing parser-adjacent payload style unless the field is explicitly a
list. Lists must use `[]`.

## Allowed Inputs

Allowed raw inputs:

- `GameStateMessage.annotations`
- `GameStateMessage.persistentAnnotations`
- normalized GameState payload `annotations`
- normalized GameState payload `persistent_annotations`
- normalized GameState payload `diff_deleted_persistent_annotation_ids`
- raw annotation dictionaries reachable through preserved `raw_game_state`
  fallback paths only when current extractor behavior already uses those
  fallback paths

Forbidden inputs:

- workbook formulas
- dashboard output
- Apps Script behavior
- webhook delivery state
- output transport state
- AI/model-provider output
- opponent archetype labels
- inferred or completed decklists
- hidden opponent hand/library/deck contents
- raw private logs committed to the repo
- generated runtime artifacts or failed-post artifacts

## Input Normalization Rules

### Source Arrays

- `annotations` and `persistent_annotations` are accepted only when the source
  value is a list.
- Missing or non-list source values normalize to zero records.
- If a source value is present but not a list, the collection must include a
  degradation flag:
  - `malformed_annotations_section`
  - `malformed_persistent_annotations_section`
- Non-dict list entries must produce degraded placeholder records rather than
  being silently treated as semantic annotation evidence.
- Placeholder records must preserve `source_array`, `source_index`,
  `persistent`, empty normalized semantic fields, and a
  `malformed_annotation_record` degradation flag.

### Annotation Type Names

- Raw `type` may be a string or a list of strings.
- Output `type_names` must be stripped strings, source-order preserving, and
  de-duplicated within each record.
- `primary_type` is the first normalized type name or `""`.
- Missing `type` yields empty `type_names`, empty `primary_type`, and
  `missing_annotation_type`.
- Non-string type entries must not become trusted semantic marker names. They
  should be skipped for marker extraction and flagged as
  `malformed_annotation_type`.

### Affected IDs

- Raw `affectedIds` and `affected_ids` are accepted.
- Integer normalization must match `api_common.normalize_int_list()`:
  booleans are skipped, integers are accepted, strings are stripped and
  accepted only when `.isdigit()` is true, and floats, negative-number strings,
  nested lists, dicts, empty strings, and `None` are skipped.
- Source order is preserved for accepted values.
- Duplicate affected IDs may remain duplicated; consumers that need sets must
  de-duplicate in their own derived summaries.
- Present but non-list affected-ID values produce
  `malformed_affected_ids`.

### Annotation IDs

- Raw `id`, `annotationId`, and `annotation_id` are accepted in that order.
- Integer normalization follows the same scalar rules as the integer-list
  policy above.
- Missing or malformed annotation IDs produce `annotation_id: ""`.
- Missing IDs are not degraded by themselves because not all annotation shapes
  require an ID.

### Details

- Raw `details` may be missing, `None`, or a list of dictionaries.
- Missing details normalize to an empty list and are not degraded by
  themselves.
- Present non-list details produce `malformed_annotation_details`.
- Non-dict detail entries produce a detail-level
  `malformed_annotation_detail` flag and a record-level degradation flag.
- Detail `key` must be a nonempty stripped string to participate in semantic
  extraction. Missing or malformed keys produce `malformed_detail_key`.
- Supported value fields include:
  - `valueInt32`
  - `valueInt64`
  - `valueString`
  - `valueBool`
- Value fields may be scalars or lists. Scalars are treated as one-element
  lists for normalization.
- Integer detail values use the same integer normalization as affected IDs.
- String detail values must be stripped strings. Non-string values should not
  become trusted semantic categories; they must be skipped for semantic
  extraction and flagged as `malformed_detail_string_value`.
- Boolean detail values must remain booleans and must not be accepted as
  integers.
- Unknown detail value keys may be preserved as generic detail metadata but
  must not become semantic categories unless a later contract names them.

## Semantic Extraction Rules

Semantic extraction creates parser-owned annotation evidence. It must not
create match/game facts by itself.

### Persistent Annotations

- Transient records use `source_array: "annotations"` and `persistent: false`.
- Persistent records use `source_array: "persistent_annotations"` and
  `persistent: true`.
- Persistent records use the same record shape and semantic extraction rules as
  transient records.
- `diff_deleted_persistent_annotation_ids` must be surfaced at collection
  level after `api_common.normalize_int_list()`-compatible normalization.
- V1 must not synthesize full annotation records from deletion IDs alone.
- V1 must not solve persistent annotation lifecycle, diff/update/deletion
  mechanics, or state reconstruction.

### Object Replacement

`AnnotationType_ObjectIdChanged` records may produce object replacement
evidence.

Required rules:

- Extract original IDs from detail key `orig_id`.
- Extract new IDs from detail key `new_id`.
- Pair original and new IDs by index in source order.
- Emit one replacement summary for each complete pair.
- If either side is missing or malformed, emit no replacement pair for that
  index and add `incomplete_object_replacement`.
- Object replacement summaries are evidence for consumers such as
  `gameplay_actions.py`; they do not prove card identity by themselves.
- Consumers must still combine replacement evidence with observed GameState
  objects, zones, and action arrays before producing gameplay facts.

### Zone Transfer Categories

`AnnotationType_ZoneTransfer` records may produce zone-transfer evidence.

Required rules:

- Extract category strings from detail key `category`.
- Extract source zone IDs from detail key `zone_src`.
- Extract destination zone IDs from detail key `zone_dest`.
- Preserve all normalized category strings in `categories` and
  `zone_transfer.categories`.
- Preserve `affected_ids` in `zone_transfer.affected_ids`.
- Known category hints:
  - `PlayLand` maps to semantic hint `land_play_hint`.
  - categories beginning with `Cast` map to semantic hint `cast_hint`.
  - `Resolve` maps to semantic hint `resolve_hint`.
- Unknown categories must be preserved and should add
  `unknown_zone_transfer_category` only when a consumer tries to interpret
  them semantically.
- Zone-transfer category hints are annotation evidence, not direct proof of a
  completed gameplay action without supporting GameState/action context.

### Markers

Recognized marker types:

| Raw annotation type | Normalized marker |
| --- | --- |
| `AnnotationType_ObjectIdChanged` | `object_id_changed` |
| `AnnotationType_ZoneTransfer` | `zone_transfer` |
| `AnnotationType_ResolutionStart` | `resolution_start` |
| `AnnotationType_ResolutionComplete` | `resolution_complete` |
| `AnnotationType_NewTurnStarted` | `new_turn_started` |
| `AnnotationType_RevealedCardDeleted` | `revealed_card_deleted` |
| `AnnotationType_Shuffle` | `shuffle` |
| `AnnotationType_UserActionTaken` | `user_action_taken` |
| `AnnotationType_ManaPaid` | `mana_paid` |
| `AnnotationType_AbilityInstanceDeleted` | `ability_instance_deleted` |

Required marker behavior:

- Marker extraction is case-sensitive and exact for v1.
- Unknown annotation types must be preserved in `type_names` but must not set
  marker booleans.
- A record with multiple known type names may set multiple markers.
- The collection `marker_types` list must include every marker set on any
  record, in first-observed order.
- Resolution, new-turn, reveal, shuffle, user-action, mana-paid, and ability
  deletion markers are evidence for parser-adjacent consumers. They do not
  prove missing game objects, hidden cards, completed decklists, or final match
  facts.

## Evidence Vocabulary

### `source_evidence`

Allowed values:

- `annotation`
- `persistent_annotation`
- `diff_deleted_persistent_annotation_id`
- `mixed`
- `unknown`

Records from `annotations` use `annotation`. Records from
`persistent_annotations` use `persistent_annotation`. Collection-level
summaries spanning both may use `mixed`.

### `evidence_status`

Allowed values:

- `observed`
- `degraded`
- `unknown`
- `conflict`

Rules:

- Well-formed raw annotation fields normalize to `observed`.
- Malformed raw fields that still produce a record normalize to `degraded`.
- Empty or unsupported records with no trusted semantic value normalize to
  `unknown` unless a malformed source is clearly degraded.
- Contradictory values inside one record, such as duplicate detail keys that
  cannot be paired deterministically for a requested semantic summary, may use
  `conflict`.

### `value_source`

Allowed values:

- `observed`
- `derived`
- `unknown`
- `conflict`

Rules:

- Raw type names, affected IDs, annotation IDs, and detail key/value values are
  `observed`.
- Marker booleans, object replacement summaries, zone-transfer summaries, and
  semantic hints are `derived` from observed annotation fields.
- Missing or unusable values are `unknown`.
- Contradictory values are `conflict`.

### `confidence`

Allowed values:

- `high`
- `medium`
- `low`
- `unknown`

Rules:

- Well-formed raw values and exact marker-name matches may use `high`.
- Zone-transfer semantic hints should default to `medium` until a consumer
  corroborates them with zones, objects, or action arrays.
- Malformed or degraded records use `low`.
- Records with no trusted semantic value use `unknown`.

### Degradation Flags

Required v1 degradation flags:

- `malformed_annotations_section`
- `malformed_persistent_annotations_section`
- `malformed_annotation_record`
- `missing_annotation_type`
- `malformed_annotation_type`
- `malformed_affected_ids`
- `malformed_annotation_details`
- `malformed_annotation_detail`
- `malformed_detail_key`
- `malformed_detail_string_value`
- `incomplete_object_replacement`
- `malformed_diff_deleted_persistent_annotation_ids`
- `truncation_or_data_loss_evidence`

The implementation may add narrower flags, but tests must protect the required
flags above when their conditions occur.

## Consumer Relationships

### GameState Payloads

Required v1 GameState behavior:

- Add `normalized_annotations` as an additive payload field produced from
  `annotations`, `persistent_annotations`, and
  `diff_deleted_persistent_annotation_ids`.
- Preserve existing raw annotation fields exactly in name and meaning.
- Preserve `raw_game_state` behavior.
- Do not add a new event class.
- Do not change GRE dispatch.
- Do not change game-result emission.

### `gameplay_actions.py`

`gameplay_actions.py` may consume `normalized_annotations` or the annotation
normalizer helper to replace its local ad hoc annotation parsing.

Required behavior:

- Existing action classification behavior covered by `tests/test_gameplay_actions.py`
  must remain stable unless this contract explicitly requires a change.
- Object replacement and zone-transfer helper behavior should come from the
  shared normalizer where practical.
- Turn-start, resolution, reveal cleanup, shuffle/support-object suppression,
  and user-action marker behavior must remain evidence-bound.
- Gameplay actions must not treat annotation hints as direct hidden-information
  facts.

### `opponent_card_observations.py`

Opponent-card observations may consume normalized annotation types,
categories, markers, and degradation flags through gameplay action entries or
direct parser-adjacent helper calls.

Required behavior:

- Annotation evidence may strengthen `source_evidence="annotation"` or
  `source_evidence="mixed"` only when the supporting normalized record is
  observed or derived from observed annotation fields.
- Opponent observations must not infer hidden opponent cards, complete
  decklists, or archetypes from annotation evidence.
- Malformed or data-loss annotation evidence must propagate as degradation or
  review, not as clean high-confidence opponent facts.

### Diagnostics Mode

Diagnostics may report annotation normalization health.

Allowed diagnostics facts:

- annotation record count
- persistent annotation record count
- degraded annotation record count
- recognized marker count by marker type
- malformed annotation degradation flags
- truncation/data-loss interaction

Forbidden diagnostics behavior:

- reconstructing missing annotations from truncation markers
- creating recovered game objects, zones, actions, match identity, game
  identity, winners, final reconciliation facts, or opponent facts
- making diagnostics output parser truth

### Golden Replay

Golden replay may compare reduced expected annotation facts only after Codex C
adds a parser-owned normalized annotation output.

Allowed manifest expectations:

- selected `normalized_annotations` summary fields
- selected marker counts
- selected degradation flags
- selected object replacement or zone-transfer summaries from sanitized or
  synthetic fixtures

Forbidden manifest behavior:

- broad raw annotation snapshots unless explicitly justified and sanitized
- automatic expected-output blessing
- raw private `Player.log` excerpts
- inferred missing GameState facts

### Evidence Ledger

The evidence ledger may later reference normalized annotation records as Tier 5
parser evidence for gameplay/action/card identity facts.

Required relationship:

- The normalizer supplies evidence and confidence labels.
- The ledger describes which parser-managed facts depend on that evidence.
- The ledger must not become a second parser or override normalized annotation
  semantics.

## Unknowns

- Arena may emit annotation types, detail keys, or detail value fields not
  represented in current tests.
- Current synthetic tests cover only selected gameplay-action annotation shapes.
- Persistent annotation lifecycle semantics are not fully understood and are
  intentionally outside v1.
- Timer normalization and GameState diff/update/deletion mechanics remain
  separate backlog modules.
- Future GameState normalization may want a broader object model; this v1
  should stay focused on annotation evidence.

## Suspected Gaps

- Current annotation interpretation is scattered in `gameplay_actions.py`.
- Current downstream consumers do not share one malformed-input policy for
  annotation details.
- Current opponent-card observation confidence can cite `annotation` evidence
  without a shared normalized annotation record.
- Current diagnostics and golden replay do not have a dedicated annotation
  degradation summary.
- Current GameState payloads preserve raw annotation arrays but do not expose a
  stable normalized annotation view.

## Fixture And Validation Strategy

Codex C should prefer synthetic fixtures for unit tests. Sanitized
`Player.log` slices are allowed only when they are necessary for parser-path
coverage and pass existing privacy/sanitization policy.

Required focused test coverage:

- raw annotation arrays remain preserved in `GameStateEvent.payload`
- `normalized_annotations` is additive and JSON-serializable
- non-list `annotations` and `persistentAnnotations` produce empty records and
  collection degradation, without raising
- non-dict annotation entries produce degraded placeholder records
- string and list `type` shapes normalize deterministically
- malformed and missing `type` shapes produce degradation or unknown status
- `affectedIds` normalization matches `api_common.normalize_int_list()`
- details normalize integer, string, and boolean values without accepting bools
  as integers
- `AnnotationType_ObjectIdChanged` creates object replacement summaries from
  `orig_id` and `new_id`
- `AnnotationType_ZoneTransfer` preserves `category`, `zone_src`, and
  `zone_dest` values and maps `PlayLand`, `Cast*`, and `Resolve` hints
- resolution start/complete markers normalize
- new-turn-started markers normalize
- revealed-card-deleted markers normalize
- shuffle, user-action, mana-paid, and ability-instance-deleted markers
  normalize
- persistent annotations use the same record shape with `persistent: true`
- diff-deleted persistent annotation IDs surface at collection level without
  synthesizing missing annotation records
- existing gameplay-action tests keep their current behavior
- opponent-card observations do not gain hidden-information inference
- diagnostics/golden replay integration, if implemented, reports only reduced
  parser-owned annotation facts

Suggested implementation validation:

```bash
python3 -m pytest -q tests/test_gre_annotations_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check
```

If Codex C changes a parser payload shape beyond the additive
`normalized_annotations` field, it must also run the relevant protected-surface
checks and route back for a contract loopback before continuing.

## Protected Surfaces And Stop Conditions

Do not:

- target `main` directly;
- close tracker #47;
- close related issue #11;
- change workbook schema;
- change webhook payload shape;
- change Apps Script behavior;
- change output transport behavior;
- change parser state final reconciliation;
- change parser event classes;
- change match identity, game identity, or deduplication policy;
- add or change secrets, environment variables, API keys, model defaults, or
  webhook URLs;
- commit raw private `Player.log` excerpts;
- commit generated data, runtime status files, failed posts, or workbook
  exports;
- infer hidden cards, complete decklists, classify archetypes, or call OpenAI
  or other model providers;
- move parser truth into workbook formulas, dashboard logic, webhook
  transport, Apps Script, AI output, or analytics surfaces;
- solve timer normalization in this module;
- solve GameState diff/update/deletion mechanics in this module;
- copy Manasight source code.

Stop and route back to Codex B or Codex A if:

- implementation requires a workbook, webhook, Apps Script, runtime status, or
  output schema migration;
- implementation requires changing parser event classes;
- implementation requires changing final reconciliation, match identity, game
  identity, or deduplication behavior;
- raw annotation preservation would be weakened;
- hidden-information or archetype inference appears necessary;
- sanitized fixtures are insufficient and private raw logs would be needed.

## Acceptance Criteria

- `docs/contracts/parser_annotation_normalization.md` defines the durable
  contract for the module.
- The contract clearly names the parser-owned module path and related files.
- The contract preserves raw annotation arrays.
- The contract defines normalized collection and record shapes.
- The contract defines type, detail, affected-ID, persistent annotation,
  object replacement, zone-transfer, and marker rules.
- The contract defines malformed, unknown, degraded, source-evidence,
  value-source, and confidence behavior.
- The contract defines downstream consumer boundaries.
- The contract defines validation obligations for Codex C and Codex E.
- The contract does not implement behavior changes.

## Workflow Decision

Verdict: ready for Codex C: Module Implementer.

A Thinker/problem-representation loopback is not required before implementation
because issue #113 already contains a complete Codex A problem representation,
and this contract resolves the v1 design choice: implement a parser-side
annotation helper and add an additive `normalized_annotations` GameState
payload field while preserving raw annotation arrays.

## Pasteable Prompt For Codex C

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #113: Annotation normalization module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/113
- Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Branch/base: codex/parser-reliability-intelligence
- Previous completed issue: #50 Opponent card observation facts
- Previous PR: #112
- Previous merge commit: 69896381a0c5d69253ef667d4575cdd0fd7e7f2a
- Contract: docs/contracts/parser_annotation_normalization.md

Goal:
Implement the smallest coherent parser-owned GRE annotation normalization module that satisfies the contract. Preserve raw GameState annotation arrays while adding the additive normalized annotation view required by the contract.

Read first:
1. AGENTS.md
2. docs/agent_constitution.md
3. docs/agent_rules.yml
4. docs/codex_module_workflow.md
5. docs/agent_threads/implementation.md
6. docs/contracts/parser_annotation_normalization.md
7. docs/contracts/parser_gre_game_state.md
8. src/mythic_edge_parser/parsers/gre/game_state.py
9. tests/test_gre_game_state_parser.py
10. src/mythic_edge_parser/app/gameplay_actions.py
11. tests/test_gameplay_actions.py
12. docs/contracts/parser_opponent_card_observations.md
13. src/mythic_edge_parser/app/opponent_card_observations.py
14. tests/test_opponent_card_observations.py
15. docs/contracts/parser_diagnostics_mode.md
16. docs/contracts/parser_golden_replay_harness.md
17. docs/contracts/player_log_evidence_ledger.md

Do:
- Create src/mythic_edge_parser/parsers/gre/annotations.py.
- Add focused tests, expected at tests/test_gre_annotations_parser.py.
- Add the additive GameState payload field normalized_annotations.
- Preserve payload annotations, persistent_annotations, diff_deleted_persistent_annotation_ids, and raw_game_state behavior.
- Prefer synthetic fixtures over sanitized Player.log slices.
- Keep gameplay_actions.py behavior stable while using the shared normalizer where practical.
- Keep opponent-card observation behavior free of hidden-information inference.
- Produce docs/implementation_handoffs/parser_annotation_normalization_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Target main directly.
- Close tracker #47.
- Close related issue #11.
- Change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Infer hidden cards, complete decklists, classify archetypes, call OpenAI/model providers, or move parser truth into workbook formulas, dashboard logic, webhook transport, Apps Script, AI, or analytics surfaces.
- Solve timer normalization or GameState diff/update/deletion mechanics in this module.
- Copy Manasight source code or commit raw private Player.log excerpts.
- Stage or commit unless explicitly asked.

Suggested validation:
python3 -m pytest -q tests/test_gre_annotations_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/113"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/50"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/112"
  previous_merge_commit: "69896381a0c5d69253ef667d4575cdd0fd7e7f2a"
  completed_thread: "B"
  next_thread: "C"
  verdict: "ready_for_module_implementation"
  branch: "codex/parser-reliability-intelligence"
  source_artifact: "docs/contracts/parser_annotation_normalization.md"
  target_artifact: "docs/implementation_handoffs/parser_annotation_normalization_comparison.md"
  risk_tier: "High"
  validation:
    - "git diff --no-index --check /dev/null docs/contracts/parser_annotation_normalization.md"
    - "LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_annotation_normalization.md"
    - "documentation contract only; no parser tests required for Codex B"
  recommended_implementation_validation:
    - "python3 -m pytest -q tests/test_gre_annotations_parser.py"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py"
    - "python3 -m pytest -q tests/test_gameplay_actions.py"
    - "python3 -m pytest -q tests/test_opponent_card_observations.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py"
    - "python3 -m ruff check src tests"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not infer hidden cards, complete decklists, classify archetypes, call OpenAI/model providers, or move parser truth into workbook formulas, dashboard logic, webhook transport, Apps Script, AI, or analytics surfaces."
    - "Do not solve timer normalization or GameState diff/update/deletion mechanics in this module."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
```
