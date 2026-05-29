# Analytics Legacy JSONL Artifact Adapter Contract

## Module

Local analytics adapter for generated legacy JSONL event archives.

This contract defines how Mythic Edge may adapt existing local JSONL event
archives into parser-normalized replay input accepted by
`ingest_parser_normalized_replay(...)`.

It does not define a raw Player.log parser, a new parser behavior path, a
SQLite schema change, a user-facing CLI, a generated fixture, a sanitizer, a
Google Sheets sync, a workbook export, or an AI/coaching surface.

## Source Artifact

- Chat problem representation for legacy JSONL artifact adapter
- Tracker reconciliation against issue #204
- Current `codex/analytics-foundation` branch state
- Key-only local JSONL shape inspection with no raw payload dump

## Tracker

- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Prior child issue #205 is closed and covered JSON-to-SQLite CLI problem
  representation. This adapter contract is a fresh docs artifact under #204
  unless a later workflow role opens a child issue for it.

## Branch

`codex/analytics-foundation`

Inspected branch head:

```text
be86be8e533604c79aa0000a0f1b11a564cd5d14
```

The local branch was even with `origin/codex/analytics-foundation` during this
contract pass.

## Risk Tier

Medium-High.

Reason: this is a local adapter over private generated artifacts. It should
help the user test existing structured game archives against SQLite analytics,
but it touches protected local artifact classes and can easily blur the line
between parser replay, legacy derived labels, raw payloads, and analytics
truth.

## Owning Layer

Primary owner: local analytics usability / artifact adapter layer.

Truth boundaries:

- Parser/state owns event interpretation, match/game identity, final
  reconciliation, and parser-normalized match/game facts.
- `saved_event_replay.py` owns generated JSONL event reconstruction and
  replay-local raw-hash dedupe.
- `analytics_ingest.py` owns local SQLite storage of parser-normalized replay
  facts.
- The legacy JSONL adapter owns only safe file selection, shape validation,
  parser replay orchestration, replay bundle construction, and adapter
  reporting.
- Legacy JSONL `derived` fields are not parser truth. They may be used only for
  diagnostics or mismatch warnings.
- SQLite analytics tables and views remain downstream storage/query surfaces,
  not parser truth, workbook truth, AI truth, hidden-card inference, gameplay
  advice, merge readiness, or deploy readiness.

Plain English: the adapter may say "these generated JSONL events can be
replayed through the current parser into this normalized analytics bundle." It
may not decide what happened in Arena by trusting old derived labels or raw
payload text directly.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`

Future implementation files authorized for Codex C:

- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `docs/implementation_handoffs/analytics_legacy_jsonl_artifact_adapter_comparison.md`

Reference-only source surfaces:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `docs/contracts/parser_saved_event_replay.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_field_evidence_ingest.md`
- `docs/contracts/analytics_replay_view_validation_harness.md`

Not owned by this contract:

- parser modules and parser event classes
- parser state final reconciliation behavior
- match/game identity or deduplication behavior
- workbook schema, webhook payload shape, Apps Script behavior, output
  transport, Google Sheets sync, Match Journal, overlay, OpenAI/model-provider
  behavior, AI/coaching behavior, CI gates, merge policy, deploy policy, and
  production behavior
- local JSONL artifacts, raw logs, failed posts, generated SQLite databases,
  runtime status files, generated card data, workbook exports, secrets, or
  credentials

## Observed Current Behavior

Repository behavior:

- Issue #204 is open and tracks analytics usability and local ingest.
- Issue #205 is closed and documents the broader JSON-to-SQLite CLI need.
- No `analytics_json_ingest_cli` module or CLI contract is present on this
  branch.
- `analytics_ingest.py` already ingests parser-normalized replay mappings into
  SQLite, including match rows, game rows, gameplay actions, opponent-card
  observations, and field evidence.
- `analytics_ingest.py` accepts only `source_kind` values
  `sanitized_golden_replay` and `saved_event_replay`.
- `saved_event_replay.py` can reconstruct supported event objects from JSONL
  records shaped like `kind`, `timestamp`, `raw_bytes_hash`, and `payload`.
- `saved_event_replay.latest_jsonl_files(...)` selects the highest versioned
  `*.jsonl` file per parent directory.
- `saved_event_replay.replay_latest_saved_events(...)` dedupes nonblank
  `raw_bytes_hash` values across selected files during one replay call.
- `transforms.to_serializable(event)` writes generated event archive records
  with top-level `kind`, `timestamp`, `raw_bytes_hash`, `payload`, and
  optional `derived` for `GameState`.
- `outputs.append_local_jsonl(...)` appends those records to generated local
  JSONL files.
- `state.py` can build `MatchLogRow` and `GameLogRow` dictionaries from
  current in-memory match summaries.

Local artifact shape observed without raw payload dump:

- The local generated archive files are JSONL.
- Top-level keys observed in local match-log archives were:
  - `kind`
  - `timestamp`
  - `raw_bytes_hash`
  - `payload`
  - `derived`
- `derived` was observed only as generated parser context for `GameState`
  records and must not be treated as parser truth.
- Observed event kind labels included `GameState`, `ClientAction`,
  `GameResult`, `MatchState`, `EventLifecycle`, `Rank`,
  `MatchConnectionState`, `TcpConnectionClose`, `DetailedLoggingStatus`,
  `DeckCollection`, `WebSocketClosed`, and `ConnectionError`.
- The adapter contract does not copy, sanitize, fixture, or commit those local
  JSONL files.

Current gap:

- No module converts generated legacy JSONL event archives into a
  parser-normalized replay mapping for `analytics_ingest.py`.
- No focused tests prove that legacy generated JSONL can be replayed through
  current parser/state code without trusting legacy `derived` fields.
- No focused tests prove that such an adapter avoids raw payload storage in
  SQLite.

## Public Interface

Codex C should add one small app module:

```text
mythic_edge_parser.app.analytics_legacy_jsonl_adapter
```

Required public constant:

```text
ANALYTICS_LEGACY_JSONL_ADAPTER_SCHEMA_VERSION = "analytics_legacy_jsonl_artifact_adapter.v1"
```

Recommended public function:

```python
adapt_legacy_jsonl_artifacts(
    source: Path,
    *,
    source_artifact_label: str | None = None,
) -> LegacyJsonlAdapterResult
```

Recommended result shape:

```python
@dataclass(frozen=True, slots=True)
class LegacyJsonlAdapterResult:
    replay: dict[str, object]
    source_kind: str
    source_artifact_label: str
    files_processed: int
    records_seen: int
    events_processed: int
    events_skipped: int
    unsupported_kind_counts: dict[str, int]
    warnings: list[str]
```

Codex C may choose equivalent names, but the result must expose the same
semantic information and tests must cover it.

Forbidden public interface expansion in this slice:

- no CLI entrypoint
- no default database path opener
- no environment-variable contract
- no live parser/tailer integration
- no raw Player.log reader
- no Google Sheets, workbook, webhook, Apps Script, Match Journal, overlay,
  OpenAI/model-provider, or AI/coaching interface

## Inputs

Allowed sources:

- a single generated legacy JSONL file;
- a folder containing generated legacy JSONL files, using the current
  `saved_event_replay.latest_jsonl_files(...)` selection semantics unless the
  implementation documents a narrower explicit-file-only first pass.

Required JSONL record shape:

```python
{
    "kind": "MatchState",
    "timestamp": "2026-05-10T17:01:00+00:00",
    "raw_bytes_hash": "stored-event-hash",
    "payload": {"type": "match_started"},
    "derived": {"match_id": "..."}  # optional, diagnostic only
}
```

Consumed fields:

- `kind`: used for exact event reconstruction through current parser event
  classes.
- `timestamp`: used only as event metadata timestamp.
- `raw_bytes_hash`: used only for replay-local dedupe.
- `payload`: used as the parser event payload.
- `derived`: not used for parser truth; optional diagnostic/mismatch context
  only.

Supported event kinds for reconstruction must follow
`saved_event_replay.EVENT_CLASS_BY_KIND` unless Codex C adds focused tests and
the current event classes already support the additional generated kind.

Unsupported event kinds must not fail the whole adapter solely because they are
unsupported. They must be counted and skipped.

## Outputs

The adapter output must be a parser-normalized replay mapping accepted by
`ingest_parser_normalized_replay(...)`.

Required replay fields:

- `source_kind`
- `source_artifact_label`
- `match_log_rows`
- `game_log_rows`
- `gameplay_action_entries`
- `opponent_card_observations`
- `field_evidence_entries`
- `parser_commit`
- `parser_version`
- `generated_at`

Required values:

- `source_kind = "saved_event_replay"`
- `source_artifact_label` must be a safe label, not a local path or URL.
- `match_log_rows` must contain only parser-normalized rows built from current
  parser/state summaries.
- `game_log_rows` must contain only parser-normalized rows built from current
  parser/state summaries.

First implementation may output empty lists for:

- `gameplay_action_entries`
- `opponent_card_observations`
- `field_evidence_entries`

Reason: current gameplay-action observation code can write runtime artifacts
when used through its live observation path. This adapter slice must not create
runtime status files. Pure in-memory gameplay-action extraction can be a later
contract unless Codex C finds an existing safe, no-write path and proves it.

The adapter must not output:

- raw JSONL record bodies;
- raw `payload` copies;
- raw Player.log lines;
- local file paths;
- full source file names when a safe label is enough;
- workbook rows or webhook payloads;
- AI/coaching output.

## Required Guarantees

### Parser Truth

The adapter must replay supported JSONL records through current parser/state
logic to build parser-normalized match/game rows.

It must not use legacy `derived` values as fact sources for:

- match id;
- game number;
- turn number;
- active player;
- phase/stage/step;
- play/draw;
- mulligans;
- opening hand;
- result;
- queue/rank/event context.

Legacy `derived` values may be compared with newly produced parser state to
emit non-fatal warnings, but warnings must not change the produced facts.

### State Isolation

The adapter must isolate parser replay state:

- reset parser runtime state before replaying an artifact;
- avoid leaking replayed state into a live parser session;
- avoid depending on pre-existing in-memory parser state;
- avoid writing runtime status artifacts, action logs, active match snapshots,
  failed posts, workbook exports, or generated SQLite files;
- restore or reset state after failure when feasible.

### Source Label Safety

`source_artifact_label` must be deterministic and safe.

Allowed examples:

- `legacy_jsonl_saved_event_replay_v1`
- `legacy_jsonl_2026_05_10_v11`
- `legacy_jsonl_bundle:<short_hash>`

Forbidden examples:

- absolute local paths;
- URLs;
- labels containing raw Player.log excerpts;
- labels containing webhook URLs, workbook IDs, API keys, tokens, or secrets.

### Dedupe And File Selection

For folder input, the adapter should preserve current saved-event replay
semantics:

- recursively find `*.jsonl` files;
- group by parent directory;
- select the highest `_v<number>_` file per parent directory;
- sort by parent directory name;
- dedupe nonblank `raw_bytes_hash` values across the selected files.

If Codex C chooses explicit single-file input only for the first pass, it must
document that narrower scope in the implementation handoff and leave folder
support for a follow-up contract.

### Match/Game Row Construction

The adapter must produce match/game rows only when current parser state can
produce them without guessing.

Required behavior:

- produce `match_log_rows` from ready `MatchSummary.to_match_log_row(final=True)`
  output;
- produce `game_log_rows` from `GameSummary.to_game_log_row(...)` rows for
  games with summary data;
- skip incomplete summaries that cannot produce a parser-normalized match row;
- report skipped/incomplete counts or warnings;
- fail clearly when no parser-normalized match/game rows can be produced.

The adapter must not fabricate missing games, results, play/draw, mulligans,
opening hands, ranks, event ids, or queue labels.

### SQLite Boundary

The adapter itself should not write SQLite.

Codex C may add a focused test that passes adapter output into
`ingest_parser_normalized_replay(...)` with an in-memory SQLite connection to
prove compatibility. A future CLI may combine adapter plus SQLite ingest, but
that user-facing command is outside this contract.

## Error Behavior

Required failures:

- source path does not exist;
- source path is neither a JSONL file nor a supported directory;
- selected file cannot be read as UTF-8;
- a nonblank line is not valid JSON;
- a JSONL record is not an object;
- supported event reconstruction raises because the record is malformed;
- replay produces no ingestable parser-normalized match/game rows.

Required non-fatal skips:

- blank JSONL lines;
- unsupported event kinds;
- duplicate nonblank `raw_bytes_hash` values after the first processed record.

Failure messages and warnings must not include raw payload bodies, raw
Player.log lines, local absolute paths, webhook URLs, workbook IDs, secrets, or
credentials. Prefer safe labels and basenames.

## Side Effects

Allowed side effects:

- read local JSONL files supplied by the caller;
- allocate and reset in-memory parser state;
- return parser-normalized replay data and adapter stats;
- write implementation handoff documentation.

Forbidden side effects:

- copy, sanitize, commit, or fixture local JSONL artifacts;
- write raw JSONL payloads into SQLite;
- create or commit generated SQLite databases, WAL, SHM, or journal files;
- write runtime status files, action logs, failed posts, workbook exports, or
  generated card data;
- post webhook payloads;
- edit live Google Sheets or Apps Script;
- change parser behavior, parser state final reconciliation, parser event
  classes, match/game identity, deduplication, workbook schema, webhook shape,
  output transport, Match Journal, overlay, AI/OpenAI behavior, production
  behavior, CI gates, or merge/deploy policy.

## Compatibility

The adapter must preserve the current saved-event replay contract unless this
contract explicitly narrows behavior.

Compatibility expectations:

- saved JSONL record shape remains owned by `transforms.to_serializable()` and
  `outputs.append_local_jsonl()`;
- latest-file selection remains owned by `saved_event_replay.py`;
- parser-normalized replay shape remains owned by `analytics_ingest.py`;
- no change to existing tests should be needed except for adding focused
  adapter tests.

## Unknowns

- The exact user-facing command shape is not selected in this adapter contract.
- It is unknown whether every local legacy JSONL day has enough final match
  evidence to produce a completed `MatchLogRow`.
- It is unknown whether pure in-memory gameplay-action extraction should be
  factored out of `gameplay_actions.py` in a later slice.
- It is unknown whether a future adapter should emit field evidence for the
  replayed rows. This slice may leave `field_evidence_entries` empty.
- It is unknown whether issue #204 should receive a new child issue for this
  adapter before Codex C starts.

## Suspected Gaps

- No adapter module exists.
- No tests prove generated legacy JSONL can become parser-normalized replay
  input.
- Current gameplay-action live observation code may write runtime artifacts, so
  it is not safe to use directly inside this adapter without a no-write path.
- Local JSONL archives include unsupported event kinds that current
  `saved_event_replay.py` does not reconstruct.
- The old `derived` block is tempting but unsafe as a fact source.

## Tests Required

Codex C should add:

```text
tests/test_analytics_legacy_jsonl_artifact_adapter.py
```

Required focused coverage:

- synthetic JSONL file with supported events adapts into replay shape accepted
  by `normalize_parser_normalized_replay(...)`;
- adapter output uses `source_kind = "saved_event_replay"`;
- `source_artifact_label` is safe and not a local path;
- match/game rows come from current parser state, not legacy `derived` fields;
- a deliberately wrong `derived.match_id` does not affect the produced
  `match_log_rows` or `game_log_rows`;
- unsupported event kinds are counted/skipped without raw payload output;
- duplicate `raw_bytes_hash` values are deduped;
- invalid JSON fails clearly without raw line echoing;
- malformed object rows fail clearly;
- no ingestable match/game rows fails clearly;
- adapter output can be passed to `ingest_parser_normalized_replay(...)` with
  `sqlite3.connect(":memory:")`;
- no runtime status/action-log/generated SQLite artifacts are created by the
  adapter tests.

Recommended validation:

```powershell
py -m pytest -q tests/test_analytics_legacy_jsonl_artifact_adapter.py tests/test_saved_event_replay.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_replay_view_harness.py
py -m ruff check src tests
git diff --check
@'
docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Acceptance Criteria

- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md` exists and is
  tracked.
- A future Codex C implementation can adapt synthetic generated JSONL event
  archives into parser-normalized replay input.
- Adapter output can be ingested into in-memory SQLite through the existing
  analytics ingest API.
- Legacy `derived` fields are not used as parser truth.
- Unsupported event kinds and duplicate hashes are reported safely.
- Invalid records fail without raw payload leakage.
- No raw Player.log payloads, raw saved-event lines, local JSONL files,
  generated SQLite databases, runtime artifacts, workbook exports, secrets, or
  credentials are committed or stored.
- Parser behavior, parser state final reconciliation, parser event classes,
  match/game identity, deduplication, workbook/webhook/App Script behavior,
  Google Sheets sync, Match Journal, overlay, AI/OpenAI behavior, production
  behavior, and `main` targeting remain untouched.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the analytics legacy JSONL artifact adapter.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Branch:
codex/analytics-foundation

Source contract:
docs/contracts/analytics_legacy_jsonl_artifact_adapter.md

Goal:
Compare current code to the contract. If the contract is clear, implement the narrow adapter that converts generated legacy JSONL event archives into parser-normalized replay mappings accepted by `ingest_parser_normalized_replay(...)`.

Before editing, state:
- what the adapter is supposed to do;
- what current code already does;
- what gap remains;
- the exact minimal implementation plan.

Implementation boundaries:
- Do not copy, sanitize, fixture, or commit local JSONL artifacts.
- Do not store raw Player.log payloads or raw saved-event lines in SQLite.
- Do not treat legacy `derived` fields as parser truth.
- Do not add a CLI in this slice.
- Do not change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, Google Sheets sync, Match Journal, overlay, OpenAI/model-provider behavior, AI/coaching behavior, production behavior, CI gates, or target main.

Expected files:
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- docs/implementation_handoffs/analytics_legacy_jsonl_artifact_adapter_comparison.md

Validation:
py -m pytest -q tests/test_analytics_legacy_jsonl_artifact_adapter.py tests/test_saved_event_replay.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_replay_view_harness.py
py -m ruff check src tests
git diff --check
@'
docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

Final handoff must include role performed, tracker used, source contract used, files changed, exact functions/tests changed, validation run, protected-surface/secret-scan status, remaining risks, next recommended role, and workflow_handoff.
```

```yaml
workflow_handoff:
  issue: "No new issue opened by Codex B"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  role_performed: "Codex B: Module Contract Writer"
  completed_thread: "B"
  next_thread: "C"
  branch: "codex/analytics-foundation"
  source_artifact: "chat problem representation for legacy JSONL artifact adapter"
  target_artifact: "docs/contracts/analytics_legacy_jsonl_artifact_adapter.md"
  risk_tier: "Medium-High"
  validation:
    - "git fetch --prune"
    - "git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0"
    - "gh issue view 204 -> OPEN tracker"
    - "gh issue view 205 -> CLOSED prior CLI problem representation"
    - "local JSONL shape inspected by keys/counts only; no raw payload dump"
  stop_conditions:
    - "Do not commit, copy, sanitize, fixture, or raw-dump the local JSONL artifact."
    - "Do not store raw Player.log payloads or raw saved-event lines in SQLite."
    - "Do not treat legacy derived fields as parser truth."
    - "Do not add a CLI in this adapter slice."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/AI behavior."
    - "Do not target main unless explicitly approved."
```
