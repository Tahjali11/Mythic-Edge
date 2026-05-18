# Parser GameState Diff Mechanics Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/117

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/115

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/116

Previous merge commit: `1afd981bc36ea3ebb68564a04f7ca985367ca9bf`

Branch target: `codex/parser-reliability-intelligence`

This contract defines first-class GRE GameState diff, update, linkage, queue,
and deletion-marker mechanics for Mythic Edge. It is a contract artifact only.
It does not implement code, change parser behavior, change workbook schema,
change webhook payloads, change Apps Script, reconstruct missing GameState
data, treat diffs as complete snapshots, or commit raw private `Player.log`
excerpts.

## Module

Parser GRE GameState diff mechanics.

Plain English: this module turns already-preserved GRE `GameStateMessage`
update metadata into a stable parser-owned evidence view. It should tell
downstream consumers whether a GameState payload is regular or queued, whether
the raw update marker says `full`, `diff`, unknown, or degraded, whether a
previous GameState link is present or malformed, and whether deletion markers
are present.

Risk tier: High.

The risk is high because this surface sits directly between raw Arena GRE
evidence and downstream parser intelligence. A weak model can make Mythic Edge
silently treat partial diffs as complete snapshots, retain stale object facts,
ignore deletion evidence, or let later analytics infer facts that the log did
not prove.

## Owning Layer

Owning layer: parser and state interpretation, specifically GRE GameState
normalization support.

Truth boundary:

- MTGA `Player.log` GameState payloads are local observable evidence, not
  absolute game truth.
- `src/mythic_edge_parser/parsers/gre/game_state.py` owns raw GameState payload
  construction and must continue preserving current raw and shallow-copied
  fields.
- The GameState diff mechanics module owns normalized update-kind, queue,
  linkage, deletion-marker, degradation, and review-required metadata.
- This module must not reconstruct full GameState object graphs from diffs.
- This module must not infer hidden cards, complete object state, complete
  decklists, archetypes, player mistakes, clock-pressure conclusions, or
  gameplay advice.
- Diagnostics mode, golden replay, saved replay, evidence ledger, gameplay
  actions, opponent-card observations, workbook sheets, dashboards, Apps
  Script, output transport, analytics modules, and AI/model output are
  consumers unless a later contract explicitly changes ownership.

Parser truth must stay parser-owned. Workbook formulas, dashboard logic,
webhook transport, Apps Script, analytics surfaces, and AI output must not
become the source of truth for GameState diff interpretation.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_game_state_diff_mechanics.md`

Future implementation artifacts owned by this contract, if authorized by the
Codex C implementation pass:

- `src/mythic_edge_parser/parsers/gre/game_state_diff.py`
- `tests/test_gre_game_state_diff_parser.py`
- `docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md`

Narrow integration surfaces allowed only when needed to satisfy this contract:

- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `tests/test_parser_diagnostics_mode.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/test_golden_replay_harness.py`
- optional committed sanitized or synthetic fixture/manifest files under
  existing fixture locations, only if required by implementation tests

Referenced but not silently owned:

- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_annotation_normalization.md`
- `docs/contracts/parser_timer_normalization.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_opponent_card_observations.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`
- related focused tests for annotations, timers, diagnostics, golden replay,
  opponent observations, gameplay actions, parser snapshots, and parser
  regressions

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence` after PR #116:

- Issue #117 is open and belongs to tracker #47.
- Tracker #47 remains open.
- Related evidence issue #11 remains open.
- PR #116 is merged into `codex/parser-reliability-intelligence` at
  `1afd981bc36ea3ebb68564a04f7ca985367ca9bf`.
- `gre.try_parse()` sends both regular `gameStateMessage` payloads and nested
  `queuedGameStateMessage.gameStateMessage` payloads through
  `build_game_state_payload()`.
- `gre._message_game_state()` prefers a current dict `gameStateMessage` over
  a nested queued dict.
- `game_state.py` sets payload `type` to `queued_game_state_message` when the
  GRE message type equals `GREMessageType_QueuedGameStateMessage`; otherwise
  it uses `game_state_message`.
- `game_state.py` preserves message `type`, `msgId`, `gameStateId`, and
  normalized `systemSeatIds`.
- `game_state.py` shallow-copies raw `players`, `zones`, `gameObjects`,
  `annotations`, `persistentAnnotations`, `timers`, and `actions` list
  sections, using `[]` for non-list sections.
- `game_state.py` adds parser-owned `normalized_annotations` and
  `normalized_timers` views while preserving raw arrays.
- `game_state.py` exposes:
  - `payload["update"]` as `str(gsm.get("update") or "")`
  - `payload["pending_message_count"]` through the local `_maybe_int()`
  - `payload["prev_game_state_id"]` through the local `_maybe_int()`
  - `payload["diff_deleted_instance_ids"]` through
    `api_common.normalize_int_list()`
  - `payload["diff_deleted_persistent_annotation_ids"]` through
    `api_common.normalize_int_list()`
  - `payload["raw_game_state"]` as the original GRE message object
- Existing focused tests cover preservation and malformed behavior for the
  current raw update, pending count, previous-state ID, and deletion ID fields.
- Current deletion ID list normalization rejects bools, floats, signed numeric
  strings, malformed strings, and `None` values.
- Current `_maybe_int()` behavior for `pending_message_count` and
  `prev_game_state_id` accepts Python `int()` conversions, including bools,
  floats, signed strings, and whitespace-padded numeric strings.
- Current parser payload schema snapshots protect the top-level
  `GameStateEvent.payload` key order.
- No dedicated first-class `game_state_diff_mechanics` normalized object exists
  yet.

## Required Guarantees

### Raw Evidence Preservation

- Existing raw and shallow-copied GameState fields must remain present and
  unchanged in meaning.
- The existing top-level `update`, `pending_message_count`,
  `prev_game_state_id`, `diff_deleted_instance_ids`, and
  `diff_deleted_persistent_annotation_ids` fields must remain present and
  backward compatible.
- The new normalized object must not replace, delete, reorder, mutate, or
  reinterpret raw `game_objects`, raw `annotations`, raw
  `persistent_annotations`, raw `timers`, raw `actions`, or preserved
  `raw_game_state`.
- The normalized object should not duplicate the full raw GRE message by
  default. Raw evidence remains available in existing payload fields.

### First-Class Normalized View

V1 should expose GameState diff mechanics through a parser-side helper module
and add an additive `GameStateEvent.payload["game_state_diff_mechanics"]`
field.

The additive GameState payload field is authorized by this contract because it
is parser-owned GameState update evidence. It must remain local parser payload
data and must not imply a workbook schema, webhook payload, Apps Script,
runtime status schema, local status artifact, failed-post payload, workbook
export, or AI-facing output change.

Because parser payload keys are snapshot-protected, Codex C must update
`tests/fixtures/schema_snapshots/parser_payload_keys.json` only for the
additive `game_state_diff_mechanics` key and only under this issue/contract.
Any broader snapshot, workbook, webhook, Apps Script, runtime artifact, parser
event class, match identity, game identity, or deduplication change is out of
scope and must stop for loopback.

### No Reconstruction

- A GameState message with `update_kind == "diff"` must never be represented
  as a complete state snapshot.
- A GameState message with deletion markers must not cause this module to
  synthesize missing objects, remove raw objects, or rebuild prior state.
- Missing or malformed prior-state linkage must become degraded/reviewable
  metadata, not a guessed link.
- Downstream consumers may use this object to lower confidence, mark review,
  avoid stale evidence, or report data-loss risk. They must not use it to
  invent hidden or missing game facts.

## Public API

Exact Python names may vary during implementation, but the public behavior must
preserve this shape:

```python
GAME_STATE_DIFF_MECHANICS_OBJECT = "mythic_edge_gre_game_state_diff_mechanics"
SCHEMA_VERSION = "parser_gre_game_state_diff_mechanics.v1"

def build_game_state_diff_mechanics(
    *,
    message: Mapping[str, object],
    gsm: Mapping[str, object],
    payload_type: str,
    game_state_id: object,
    update: str,
    pending_message_count: int | None,
    prev_game_state_id: int | None,
    diff_deleted_instance_ids: list[int],
    diff_deleted_persistent_annotation_ids: list[int],
) -> dict[str, object]:
    ...
```

Required API behavior:

- Return JSON-serializable dictionaries and lists.
- Preserve input objects without mutation.
- Avoid filesystem writes.
- Avoid importing workbook, webhook, Apps Script, output transport, OpenAI, or
  model-provider surfaces.
- Never raise for malformed GameState update metadata in normal parser use.
  Malformed values must become empty normalized fields plus degradation flags.
- Use deterministic ordering for list fields and flags.
- Treat helper functions as parser-owned evidence helpers, not analytics APIs.

The helper may be integrated from `game_state.py` after the current top-level
GameState payload fields are computed, so the new object can mirror current
backward-compatible normalization for top-level fields while adding stricter
degradation evidence where needed.

## Normalized Payload Shape

Required logical shape for
`payload["game_state_diff_mechanics"]`:

```yaml
object: "mythic_edge_gre_game_state_diff_mechanics"
schema_version: "parser_gre_game_state_diff_mechanics.v1"
source_payload_type: "game_state_message"
message_type: "GREMessageType_GameStateMessage"
queued: false
game_state_id: 42
game_state_id_normalized: 42
msg_id: 7
update_raw: "diff"
update_kind: "diff"
state_completeness: "partial_update"
is_complete_snapshot: false
pending_message_count: 4
prev_game_state_id: 41
prev_game_state_id_status: "linked"
linkage_status: "linked"
deletion_evidence_present: true
diff_deleted_instance_ids: [10, 11]
diff_deleted_persistent_annotation_ids: [20, 21]
deletion_counts:
  instance_ids: 2
  persistent_annotation_ids: 2
section_counts:
  players: 2
  zones: 3
  game_objects: 5
  annotations: 1
  persistent_annotations: 1
  timers: 1
  actions: 1
source_fields_used:
  update: true
  pendingMessageCount: true
  prevGameStateId: true
  diffDeletedInstanceIds: true
  diffDeletedPersistentAnnotationIds: true
evidence_status: "observed"
value_source: "observed"
confidence: "high"
degradation_flags: []
review_required: false
```

Required top-level keys:

- `object`
- `schema_version`
- `source_payload_type`
- `message_type`
- `queued`
- `game_state_id`
- `game_state_id_normalized`
- `msg_id`
- `update_raw`
- `update_kind`
- `state_completeness`
- `is_complete_snapshot`
- `pending_message_count`
- `prev_game_state_id`
- `prev_game_state_id_status`
- `linkage_status`
- `deletion_evidence_present`
- `diff_deleted_instance_ids`
- `diff_deleted_persistent_annotation_ids`
- `deletion_counts`
- `section_counts`
- `source_fields_used`
- `evidence_status`
- `value_source`
- `confidence`
- `degradation_flags`
- `review_required`

Allowed empty values:

- Unknown integer-like scalar fields use `""` inside this normalized object
  when no trusted value is available.
- Unknown string fields use `""`.
- Unknown or absent lists use `[]`.
- Unknown object sections use stable empty dictionaries with the same required
  keys.

## Update Kind Semantics

`update_raw`:

- Preserves the observed `gsm["update"]` value after string conversion and
  trimming when the raw value is string-like or scalar-like.
- Uses `""` when the field is missing, `None`, falsey, or cannot be represented
  safely.
- Must not replace the existing top-level `payload["update"]` behavior.

`update_kind` allowed values:

- `full`
- `diff`
- `unknown`
- `degraded`

Required normalization:

- Case-insensitive raw value `full` maps to `full`.
- Case-insensitive raw value `diff` maps to `diff`.
- Missing or empty raw value maps to `unknown`.
- Any other non-empty raw value maps to `degraded` and adds
  `unknown_update_kind`.
- Non-string scalar raw values may be represented in `update_raw`, but must not
  silently become known update kinds unless their string form exactly matches a
  known value after trimming and case normalization.

`state_completeness` allowed values:

- `complete_snapshot`
- `partial_update`
- `unknown`
- `degraded`

Required mapping:

- `update_kind == "full"` means `state_completeness == "complete_snapshot"`
  and `is_complete_snapshot is True`.
- `update_kind == "diff"` means `state_completeness == "partial_update"` and
  `is_complete_snapshot is False`.
- `update_kind == "unknown"` means `state_completeness == "unknown"` and
  `is_complete_snapshot is False`.
- `update_kind == "degraded"` means `state_completeness == "degraded"` and
  `is_complete_snapshot is False`.

Deletion markers, previous-state IDs, and pending message counts are additional
mechanics evidence. They must not override the raw update kind by themselves.
For example, a `full` update with deletion markers remains a `full` update with
`deletion_evidence_present == true`, not an inferred diff.

## Queued And Regular Source Semantics

`source_payload_type`:

- Must be copied from the GameState payload type produced by `game_state.py`.
- Allowed values in v1 are `game_state_message` and
  `queued_game_state_message`.

`queued`:

- `true` when `source_payload_type == "queued_game_state_message"`.
- `false` otherwise.

Required behavior:

- Regular and queued GameState messages must use the same normalized mechanics
  object shape.
- A queued message is not automatically degraded.
- Queue status does not prove that the nested GameState is stale, complete, or
  partial. It is a source classification only.
- Current GRE dispatch precedence must remain unchanged: a current
  `gameStateMessage` dict remains selected ahead of nested queued content.

## Linkage Semantics

`game_state_id`:

- Copies the existing top-level GameState payload `game_state_id` value for
  compatibility.

`game_state_id_normalized`:

- Uses a conservative ID-like integer normalization for comparison.
- Valid values are non-bool integers and unsigned digit strings after
  whitespace trimming.
- Invalid, missing, bool, float, signed string, and malformed values become
  `""` in this normalized object.
- This stricter comparison field does not change the existing top-level
  `payload["game_state_id"]` behavior.

`prev_game_state_id`:

- Copies the existing top-level GameState payload `prev_game_state_id` value
  when present.
- Uses `""` when no normalized top-level previous-state ID is available.
- This preserves current compatibility, including the existing local
  `_maybe_int()` behavior.

`prev_game_state_id_status` allowed values:

- `not_applicable`
- `linked`
- `present_unverified`
- `missing`
- `malformed`
- `self_reference`
- `future_reference`
- `unknown`

`linkage_status` uses the same allowed values in v1.

Required linkage rules:

- `linked`: previous-state ID and current GameState ID are both normalized,
  previous-state ID is lower than current GameState ID, and the raw update kind
  does not create a conflict.
- `present_unverified`: previous-state ID is present, but the current GameState
  ID cannot be normalized for comparison.
- `not_applicable`: update kind is `full`, no previous-state ID is present,
  and no linkage evidence is needed.
- `missing`: update kind is `diff` and no previous-state ID is present.
- `malformed`: a raw `prevGameStateId` field is present but cannot be
  normalized by the existing top-level payload behavior.
- `self_reference`: previous-state ID equals current GameState ID.
- `future_reference`: previous-state ID is greater than current GameState ID.
- `unknown`: update kind is unknown or degraded and linkage cannot be classified
  more specifically.

Degradation flags must accompany `missing`, `malformed`, `self_reference`,
`future_reference`, and `unknown` statuses when the status affects confidence.

## Pending Message Count Semantics

`pending_message_count`:

- Copies the existing top-level GameState payload `pending_message_count` value
  when present.
- Uses `""` when no normalized top-level count is available.
- Must not change the current top-level `_maybe_int()` behavior.

Required behavior:

- Negative counts are degraded with `negative_pending_message_count`.
- A raw `pendingMessageCount` field that is present but not normalized into a
  top-level count adds `malformed_pending_message_count`.
- A valid pending message count does not by itself prove that a payload is
  complete or partial.

## Deletion Marker Semantics

`diff_deleted_instance_ids`:

- Copies the existing top-level normalized deletion ID list.
- Source order is preserved.
- Invalid source members remain omitted according to the existing
  `api_common.normalize_int_list()` behavior.

`diff_deleted_persistent_annotation_ids`:

- Copies the existing top-level normalized persistent annotation deletion ID
  list.
- Source order is preserved.
- The same values must also remain available through
  `payload["normalized_annotations"]["diff_deleted_persistent_annotation_ids"]`.

`deletion_counts`:

- `instance_ids` equals `len(diff_deleted_instance_ids)`.
- `persistent_annotation_ids` equals
  `len(diff_deleted_persistent_annotation_ids)`.

`deletion_evidence_present`:

- `true` when either deletion ID list is non-empty.
- `false` otherwise.

Required behavior:

- Deletion IDs are durable parser-owned evidence that prior object or
  persistent annotation evidence may be stale.
- Deletion IDs must not cause this module to remove raw objects, synthesize
  missing objects, synthesize annotation records, or reconstruct prior state.
- A malformed deletion list must add the matching degradation flag while
  preserving any normalized valid IDs already available through current list
  normalization.

Required degradation flags for deletion source shapes:

- `malformed_diff_deleted_instance_ids` when the raw
  `diffDeletedInstanceIds` field is present and is not a list.
- `malformed_diff_deleted_persistent_annotation_ids` when the raw
  `diffDeletedPersistentAnnotationIds` field is present and is not a list.
- `deletion_evidence_present` is a boolean output, not a degradation flag.

## Section Count Semantics

`section_counts` should summarize observed list-section counts after current
GameState shallow-copy fallback:

- `players`
- `zones`
- `game_objects`
- `annotations`
- `persistent_annotations`
- `timers`
- `actions`

Required behavior:

- Counts are observed payload counts only.
- Counts must not be treated as completeness guarantees.
- Non-list raw sections that already become `[]` in the top-level GameState
  payload count as `0`.
- Section counts must not duplicate raw section contents.

## Evidence Labels

Allowed `evidence_status` values:

- `observed`
- `unknown`
- `degraded`
- `conflict`

Allowed `value_source` values:

- `observed`
- `derived`
- `unknown`
- `conflict`

Allowed `confidence` values:

- `high`
- `medium`
- `low`
- `unknown`

Required mapping:

- Clean known `full` or `diff` update mechanics with no degradation flags use
  `evidence_status == "observed"`, `value_source == "observed"`, and
  `confidence == "high"`.
- Unknown update kind with no other malformed fields uses
  `evidence_status == "unknown"`, `value_source == "unknown"`, and
  `confidence == "unknown"`.
- Malformed source shapes, missing required diff linkage, self-referential
  linkage, future linkage, or unknown non-empty update strings use
  `evidence_status == "degraded"` and `confidence == "low"` unless a direct
  contradiction is found.
- Contradictory evidence uses `evidence_status == "conflict"`,
  `value_source == "conflict"`, `confidence == "low"`, and
  `review_required == true`.
- `review_required` is `true` whenever any degradation flag is present or
  `evidence_status` is `degraded`, `unknown`, or `conflict`.

## Degradation Flags

Allowed v1 degradation flags:

- `unknown_update_kind`
- `missing_update_kind`
- `missing_prev_game_state_id`
- `malformed_prev_game_state_id`
- `self_referential_prev_game_state_id`
- `future_prev_game_state_id`
- `malformed_pending_message_count`
- `negative_pending_message_count`
- `malformed_diff_deleted_instance_ids`
- `malformed_diff_deleted_persistent_annotation_ids`
- `malformed_game_state_id`
- `unknown_linkage_status`
- `conflicting_update_and_linkage_evidence`
- `truncation_or_data_loss_evidence`

Flag rules:

- Missing update kind should add `missing_update_kind` only when the missing
  update marker affects confidence. A regular clean payload with no update
  marker may remain unknown/reviewable rather than failed.
- `missing_prev_game_state_id` applies when `update_kind == "diff"` and no
  previous-state ID is present.
- `truncation_or_data_loss_evidence` is reserved for future integration with
  truncation/data-loss markers. It must not be invented from ordinary missing
  fields.
- Codex C may add one or two narrower flags if focused tests prove a real
  malformed source shape not covered here. Broader vocabulary changes should
  route back to Codex B.

## Source Fields Used

`source_fields_used` must be a stable dictionary of booleans:

- `update`
- `pendingMessageCount`
- `prevGameStateId`
- `diffDeletedInstanceIds`
- `diffDeletedPersistentAnnotationIds`
- `gameStateId`
- `msgId`
- `type`

Required behavior:

- A key is `true` when the raw source field is present in `message` or `gsm`.
- A key is `false` when the raw source field is absent.
- Presence does not imply validity.

## Relationship To Existing Surfaces

### `game_state.py`

- `game_state.py` remains the integration point that adds
  `payload["game_state_diff_mechanics"]`.
- Existing top-level payload fields remain backward compatible.
- This contract authorizes one additive payload key only.

### GRE Dispatch

- `parsers/gre/__init__.py` should not need behavior changes.
- Regular and queued messages already reach `build_game_state_payload()`.
- If Codex C discovers a dispatch bug that blocks this contract, it must stop
  and route back for problem framing rather than broadening the implementation.

### Annotation Normalization

- `normalized_annotations` continues to own annotation records, object
  replacements, zone-transfer summaries, and collection-level persistent
  annotation deletion IDs.
- GameState diff mechanics may mirror the same
  `diff_deleted_persistent_annotation_ids` list as deletion mechanics
  evidence.
- GameState diff mechanics must not synthesize normalized annotation records
  for deleted persistent annotation IDs.

### Timer Normalization

- `normalized_timers` continues to own timer evidence.
- GameState diff mechanics may count timer records in `section_counts`.
- GameState diff mechanics must not build clock-pressure analytics or infer
  player mistakes from timer evidence.

### Diagnostics Mode

- Diagnostics mode may summarize counts of `full`, `diff`, `unknown`, and
  degraded GameState mechanics.
- Diagnostics mode may report deletion-marker presence and malformed linkage as
  review/fail evidence according to its own contract.
- Diagnostics mode must remain an observer/acceptance harness, not a second
  parser.

### Golden Replay

- Golden replay may assert selected reduced fields from
  `game_state_diff_mechanics`, such as `update_kind`, `state_completeness`,
  `is_complete_snapshot`, `linkage_status`, deletion counts, and
  `review_required`.
- Golden replay manifests must use sanitized or synthetic fixtures only.
- Golden replay must not require full raw GameState object snapshots for this
  module.

### Saved Replay

- Saved replay may preserve and replay the additive normalized object.
- Saved replay must not treat the object as reconstructed state.

### Evidence Ledger, Drift, And Provenance

- Future evidence-ledger entries may cite this module when a fact depends on
  full GameState evidence, diff-only evidence, deletion markers, or degraded
  linkage.
- The ledger must not become a second parser or override this module's
  classifications.
- Drift reports may flag new or malformed update/linkage/deletion shapes.
- Drift reports must not treat unknown GameState mechanics as silent success.

### Gameplay Actions

- Gameplay actions may consume `game_state_diff_mechanics` to avoid treating
  diff-only or deletion-bearing evidence as clean full-state evidence.
- Gameplay actions must not infer hidden cards, stale objects, or complete game
  object state from diff-only evidence.
- This contract does not require broad gameplay-action rewrites in v1. If
  Codex C finds current action extraction needs a behavior change to preserve
  this truth boundary, it must keep it narrow and parser-adjacent or route back
  to Codex B.

### Opponent Card Observations

- Opponent-card observations may consume degradation and deletion evidence to
  mark observations as degraded or review-required.
- Opponent-card observations must not infer hidden opponent cards, complete
  decklists, or archetypes from diff-only evidence.
- This module does not change the opponent observation payload contract.

### Workbook, Webhook, Apps Script, Runtime Status, Failed Posts, And Exports

- No workbook schema change is authorized.
- No webhook payload shape change is authorized.
- No Apps Script behavior change is authorized.
- No runtime status file schema change is authorized.
- No failed-post payload change is authorized.
- No workbook export change is authorized.

## Compatibility Expectations

- Existing parser payload keys remain present.
- Existing top-level raw update/deletion fields keep their current behavior.
- `game_state_diff_mechanics` is additive and parser-owned.
- Parser event classes must not change.
- Match identity, game identity, final reconciliation, and deduplication must
  not change.
- No new secrets, credentials, webhook URLs, environment variables, OpenAI
  configuration, or model-provider defaults are authorized.
- The module must stay deterministic and local.
- Tests must not depend on raw private logs.

## Fixture Strategy

Allowed fixtures:

- Small synthetic GRE GameState dictionaries embedded in focused unit tests.
- Committed sanitized `Player.log` slices only if they contain no private data,
  secrets, usernames, local paths, raw tokens, webhook URLs, or generated
  runtime artifacts.
- Golden replay manifests that assert reduced parser-owned fields, not broad
  raw snapshots.

Forbidden fixtures:

- Raw private `Player.log` excerpts.
- Failed posts.
- Runtime status files.
- Generated workbook exports.
- Secrets, credentials, API keys, webhook URLs, or local absolute user paths.
- Copied Manasight source code.

Fixture minimization:

- Prefer synthetic dict-level tests for normalization rules.
- Add replay fixtures only when they prove parser routing or replay behavior
  that unit tests cannot prove.
- Expected outputs should cover representative full, diff, queued, deletion,
  missing-link, malformed-link, and unknown-update cases without becoming a
  giant raw GameState snapshot.

## Test Obligations For Codex C

Focused implementation tests must prove:

- `build_game_state_diff_mechanics()` returns the required object marker and
  schema version.
- Regular and queued GameState payloads get the additive
  `game_state_diff_mechanics` field.
- `full` update maps to `complete_snapshot` and
  `is_complete_snapshot == true`.
- `diff` update maps to `partial_update` and
  `is_complete_snapshot == false`.
- Missing update kind maps to unknown/review behavior without crashing.
- Unknown non-empty update kind is degraded and review-required.
- Clean previous-state linkage is `linked`.
- Diff update without previous-state ID is degraded with
  `missing_prev_game_state_id`.
- Malformed previous-state ID is degraded with
  `malformed_prev_game_state_id`.
- Self-referential and future previous-state IDs are degraded.
- Deletion ID lists are copied from the existing normalized top-level lists.
- Deletion counts and `deletion_evidence_present` are correct.
- Malformed deletion source shapes add the matching degradation flags.
- Section counts are counts only and do not imply completeness.
- The normalized object does not mutate `message`, `gsm`, or raw payload
  sections.
- Existing annotation and timer normalization behavior is unchanged.
- Existing top-level `update`, `pending_message_count`, `prev_game_state_id`,
  and deletion ID fields keep current behavior.
- Parser payload schema snapshot changes are limited to the additive key.

Recommended validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_gre_game_state_diff_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gre_annotations_parser.py tests/test_gre_timers_parser.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parsers.py tests/test_parser_regressions.py
python3 -m ruff check src tests tools
git diff --check
```

If the implementation touches diagnostics, golden replay, gameplay actions, or
opponent observations, Codex C must also run the touched focused tests and
explain why the integration was necessary.

## Review Obligations For Codex E

Codex E should verify:

- The implementation is additive and parser-local.
- The normalized object shape matches this contract.
- A diff GameState is never classified as a complete snapshot.
- Deletion markers are preserved as evidence and not used for reconstruction.
- Unknown and malformed linkage becomes degraded or review-required metadata.
- No parser event class, workbook, webhook, Apps Script, runtime status,
  failed-post, workbook export, match identity, game identity, final
  reconciliation, deduplication, secret, credential, environment variable,
  OpenAI, or model-provider surface changed.
- Snapshot updates are limited to the authorized additive payload key.
- Fixtures are synthetic or sanitized and do not include private raw logs.
- Validation commands were run and reported with exact results.

## Suspected Gaps

- Current gameplay-action extraction contains partial-diff inference helpers
  that predate this normalized mechanics object. That behavior may be correct
  enough for current tests, but it lacks a first-class way to distinguish clean
  full-state evidence from diff/deletion-bearing evidence.
- Current diagnostics and golden replay cannot yet summarize GameState update
  mechanics as a stable parser-owned category.
- Current evidence-ledger work can describe value-source/confidence/finality
  concepts, but there is no dedicated GameState mechanics object to cite.
- Current top-level `_maybe_int()` behavior for `prev_game_state_id` and
  `pending_message_count` is more permissive than deletion ID normalization.
  The new normalized object should preserve top-level compatibility while
  exposing stricter degradation evidence where appropriate.

## Unknowns

- Arena may emit additional `update` marker values beyond `full` and `diff`.
  V1 must degrade unknown non-empty values rather than silently accepting them.
- Some full GameState messages may include previous-state IDs or deletion
  markers. V1 must preserve that evidence without inferring diff semantics from
  deletion markers alone.
- The complete relationship between queued GameState messages and prior
  GameState linkage may need future corpus evidence. V1 treats queued status as
  source classification, not completeness proof.
- Future state reconstruction, if ever needed, requires a separate high-risk
  contract. This contract explicitly does not authorize it.

## Stop Conditions

Codex C must stop and route back to Codex B or Codex A if implementation would
require any of the following:

- Reconstructing missing GameState data.
- Treating a diff GameState as a complete snapshot.
- Changing parser event classes.
- Changing parser state final reconciliation.
- Changing match identity, game identity, or deduplication.
- Changing workbook schema, webhook payload shape, Apps Script behavior,
  output transport, runtime status files, failed posts, or workbook exports.
- Adding secrets, credentials, webhook URLs, API keys, environment variables,
  OpenAI calls, model-provider calls, or model defaults.
- Committing raw private `Player.log` excerpts, generated data, local logs,
  failed posts, runtime status files, or workbook exports.
- Copying Manasight source code.
- Building clock-pressure analytics, gameplay advice, player-mistake labels,
  hidden-card inference, decklist completion, archetype classification,
  AI/analytics truth, feature-equity corpus ratchet/reporting, or field-level
  parity audit behavior.
- Broadly rewriting gameplay actions, opponent-card observations, diagnostics,
  golden replay, or saved replay beyond narrow consumption of this additive
  parser-owned metadata.

## Acceptance Criteria

- `docs/contracts/parser_game_state_diff_mechanics.md` exists and defines this
  contract.
- The contract names the owning layer, truth boundary, public API, normalized
  payload shape, update semantics, queued semantics, linkage semantics,
  deletion-marker semantics, degradation labels, consumers, fixture strategy,
  validation obligations, and stop conditions.
- The next role is Codex C: Module Implementer on
  `codex/parser-reliability-intelligence`.
- No code behavior is changed by the contract-writing pass.

## Recommended Next Role

Codex C: Module Implementer.

Codex C should compare this contract against current code, implement only the
smallest coherent parser-local code/test changes needed to satisfy the
contract, produce
`docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md`,
and route to Codex E for review.

## Pasteable Prompt For Codex C

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #117: GameState diff/update/deletion mechanics module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Related resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/117
- Branch/base: codex/parser-reliability-intelligence
- Contract: docs/contracts/parser_game_state_diff_mechanics.md
- Previous completed issue: #115 GameState timer normalization
- Previous PR: #116
- Previous merge commit: 1afd981bc36ea3ebb68564a04f7ca985367ca9bf

Goal:
Compare the current GameState parser implementation and focused tests against
the GameState diff mechanics contract. Implement only the smallest coherent
parser-local code and test changes needed to satisfy the contract.

Read first:
1. AGENTS.md
2. docs/agent_constitution.md
3. docs/agent_rules.yml
4. docs/agent_threads/implementation.md
5. docs/codex_module_workflow.md
6. docs/contracts/parser_game_state_diff_mechanics.md
7. src/mythic_edge_parser/parsers/gre/game_state.py
8. src/mythic_edge_parser/parsers/gre/__init__.py
9. src/mythic_edge_parser/parsers/gre/annotations.py
10. src/mythic_edge_parser/parsers/gre/timers.py
11. tests/test_gre_game_state_parser.py
12. tests/test_event_schema_snapshots.py
13. docs/contracts/parser_annotation_normalization.md
14. docs/contracts/parser_timer_normalization.md
15. docs/contracts/parser_diagnostics_mode.md
16. docs/contracts/parser_golden_replay_harness.md
17. docs/contracts/parser_opponent_card_observations.md

Implement:
- Add a parser-owned GRE GameState diff mechanics helper module, expected path:
  src/mythic_edge_parser/parsers/gre/game_state_diff.py.
- Add focused tests, expected path:
  tests/test_gre_game_state_diff_parser.py.
- Add the additive GameState payload key:
  payload["game_state_diff_mechanics"].
- Update parser payload schema snapshots only for the authorized additive key.
- Preserve existing top-level update, pending_message_count, prev_game_state_id,
  diff_deleted_instance_ids, diff_deleted_persistent_annotation_ids,
  normalized_annotations, normalized_timers, and raw_game_state behavior.
- Produce docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md
  with observed comparison, changes made, validation run, open risks, files
  changed, and next recommended role.

Do not:
- Do not target main directly.
- Do not close tracker #47.
- Do not close related issue #11.
- Do not reconstruct missing GameState data or treat diff GameState messages as full state snapshots.
- Do not change parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status files, failed posts, workbook exports, secrets, credentials, environment variables, OpenAI/model-provider behavior, or AI/analytics truth.
- Do not infer hidden cards, complete decklists, archetypes, gameplay advice, player mistakes, or clock-pressure analytics.
- Do not copy Manasight source code or commit raw private Player.log excerpts, generated data, local logs, failed posts, runtime status files, or workbook exports.
- Do not solve feature-equity corpus ratchet/reporting or field-level parity audit in this module.
- Do not stage or commit unless explicitly asked.

Required validation:
- python3 -m pytest -q tests/test_gre_game_state_diff_parser.py
- python3 -m pytest -q tests/test_gre_game_state_parser.py
- python3 -m pytest -q tests/test_gre_annotations_parser.py tests/test_gre_timers_parser.py
- python3 -m pytest -q tests/test_event_schema_snapshots.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py
- python3 -m pytest -q tests/test_golden_replay_harness.py
- python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
- python3 -m pytest -q tests/test_parsers.py tests/test_parser_regressions.py
- python3 -m ruff check src tests tools
- git diff --check
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/117"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_game_state_diff_mechanics.md"
  target_artifact: "docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md"
  verdict: "ready_for_module_implementer"
  branch: "codex/parser-reliability-intelligence"
  risk_tier: "High"
  validation:
    - "git diff --check"
    - "git diff --no-index --check /dev/null docs/contracts/parser_game_state_diff_mechanics.md"
    - "LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_game_state_diff_mechanics.md"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not reconstruct missing GameState data or treat diff GameState messages as full state snapshots."
    - "Do not change parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status files, failed posts, workbook exports, secrets, credentials, environment variables, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not infer hidden cards, complete decklists, archetypes, gameplay advice, player mistakes, or clock-pressure analytics."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts, generated data, local logs, failed posts, runtime status files, or workbook exports."
    - "Do not solve feature-equity corpus ratchet/reporting or field-level parity audit in this module."
```
