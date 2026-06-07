# Analytics Legacy JSONL Batch Import Contract

## Module

Legacy JSONL batch import and source artifact grouping for the local developer
app.

Plain English: this contract lets the local app import several selected legacy
`.jsonl` files as one historical batch, so old parser open/close session
boundaries do not force the user to manually stitch matches together. It keeps
raw file boundaries as provenance and quality context only.

This contract does not implement code. It does not define folder recursion,
browser upload, copied import retention, persistent import history, live
Player.log watching, an analytics dashboard, Line Tracer, AI coaching, a
SQLite schema change, or destructive import/database/job controls.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/213>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Related quality issue: <https://github.com/Tahjali11/Mythic-Edge/issues/212>
- Related manual import issue: <https://github.com/Tahjali11/Mythic-Edge/issues/211>
- Legacy adapter contract:
  `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- Manual import contract:
  `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- Import quality contract:
  `docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`
- Parser-normalized ingest contract:
  `docs/contracts/analytics_parser_normalized_replay_ingest.md`

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
5d7347552885
```

Local branch state observed:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
```

`HEAD...origin/codex/analytics-foundation` was even (`0 0`) during this
contract pass. The worktree contained active #212 implementation changes and
unrelated launcher changes; this Codex B pass does not own or modify them.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- tracker #204
- umbrella issue #207
- manual import issue #211
- quality issue #212
- source issue #213
- `docs/project_roadmap.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- `docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md`
- `docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`

## Risk Tier

High.

Reasons:

- this changes the local app import request shape;
- it reads multiple private local artifacts in one job;
- it can combine events across old parser session files;
- it depends on raw-hash dedupe scope across the batch;
- it can blur file provenance, parser truth, and analytics ingest identity if
  labels are sloppy;
- it can accidentally expose raw paths, raw file names, raw hashes, or raw
  payloads;
- it can accidentally create partial-ingest semantics or a persistent import
  history before those are contracted.

The slice stays acceptable only if it is additive, explicit, synthetic-test
backed, and preserves all protected parser, replay, SQLite, workbook, webhook,
Apps Script, Sheets, OpenAI/AI, production, and destructive-action boundaries.

## Owning Layer

Primary owner: local analytics usability / manual historical import loop.

Truth boundaries:

- Parser/state owns MTGA event interpretation, match/game identity, final
  reconciliation, parser event classes, and parser-managed facts.
- The legacy JSONL adapter owns safe file selection, deterministic batch
  ordering, parser replay orchestration, replay bundle construction,
  raw-hash-dedupe reporting, and sanitized source-artifact reporting.
- `analytics_ingest.py` owns writing already-normalized parser facts into
  local SQLite.
- SQLite owns downstream queryable storage, not parser truth.
- The local backend owns import orchestration and sanitized job-status
  responses.
- The frontend owns explicit user selection and safe display only.
- Legacy JSONL `derived` fields remain diagnostic only and must not become
  parser truth.

The batch import may say "these selected legacy event archives were replayed
as one batch and produced these parser-normalized rows." It must not decide
what happened in Arena by trusting legacy derived labels, analytics joins,
frontend state, or raw payload text directly.

## Dependency On Issue #212

Batch import must reuse the #212 import-quality contract.

Required dependency:

- batch-level import quality must use the
  `analytics_legacy_jsonl_import_quality_breakdown.v1` shape;
- per-file summaries must use the same safe count vocabulary where applicable;
- no parallel quality schema may be invented for batch import.

If Codex C starts #213 before #212 is complete in the branch it is editing, it
must either:

- implement #212 first in the same reviewed stack, or
- stop and route back to Codex B/G for sequencing.

Do not implement a temporary `skip_breakdown`, `batch_quality`, or UI-only
report shape that conflicts with `adapter.quality`.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_legacy_jsonl_batch_import.md`

Future Codex C implementation files authorized by this contract:

- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`, only for batch-import display
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md`

Referenced but not owned:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/analytics_migrations/*.sql`
- SQLite generated database files
- raw local JSONL artifacts

Codex C must route back to Codex B before changing parser behavior, saved-event
replay semantics, parser event classes, match/game identity, deduplication
semantics, analytics schema/migrations, backend route inventory beyond the
existing import route, raw artifact retention, or frontend behavior outside
manual import selection/status display.

## Observed Current Behavior

Current adapter behavior:

- `adapt_legacy_jsonl_artifacts(source, source_artifact_label=None)` accepts a
  single file or a directory-shaped source.
- For a file, it processes that single `.jsonl`.
- For a directory, it uses `saved_event_replay.latest_jsonl_files(...)`, which
  recursively selects one highest-versioned JSONL file per parent directory.
- It replays selected files through current parser/state logic in one state
  reset/replay scope.
- It deduplicates nonblank `raw_bytes_hash` values across selected files in
  that adapter call.
- It emits parser-normalized replay input accepted by
  `ingest_parser_normalized_replay(...)`.
- In the local #212 worktree state, it also emits an additive sanitized
  `quality` object with processed kind counts, skipped reason counts, output
  gaps, warning codes, routing hints, and privacy flags.

Current manual import behavior:

- `POST /api/imports/jsonl` accepts a single `source_path` string.
- The route rejects URLs, UNC paths, directories, missing files, non-`.jsonl`
  files, and non-file paths.
- The route reads the selected file in place and does not copy raw JSONL into
  the repo or app data.
- The route writes parser-normalized facts into the app-owned SQLite database
  only after source validation and successful adapter replay.
- The job summary is process-local and in memory.
- The frontend displays one path input and a sanitized import summary.

Current ingest behavior:

- `ingest_parser_normalized_replay(...)` accepts `source_kind` values
  `sanitized_golden_replay` and `saved_event_replay`.
- `source_artifact_label` must be safe and must not be a local path or URL.
- Ingest uses deterministic IDs and upserts into existing SQLite tables.
- SQLite schema/migrations do not contain import-quality or batch-history
  tables.

Observed gaps:

- The local app cannot submit several explicit files in one job.
- The current single-file request shape cannot represent a source group.
- The current frontend has no multi-file selection/input display.
- No backend tests prove deterministic ordering for shuffled input paths.
- No tests prove duplicate raw-hash counting across explicit files.
- No tests prove per-file safe summaries or aggregate quality rollups.
- No tests prove idempotent re-import of a batch into SQLite.

## Contract Decision

First implementation should extend the existing manual import route rather
than add a new route.

Required first-slice behavior:

1. `POST /api/imports/jsonl` continues to accept the existing single-file
   `source_path` request.
2. `POST /api/imports/jsonl` additionally accepts an explicit `source_paths`
   array for batch import.
3. Requests must provide exactly one of `source_path` or `source_paths`.
4. Batch import accepts only explicit local `.jsonl` files.
5. Batch import rejects directories and does not recurse folders.
6. Batch import reads files in place and does not copy them into app data.
7. Batch import validates the whole selected file list before creating app-data
   folders or opening SQLite.
8. Batch import processes files in deterministic internal order.
9. Batch import replays all selected files in one parser-state replay scope.
10. Batch import deduplicates nonblank raw hashes across the whole batch.
11. Batch import produces one combined parser-normalized replay and one ingest
    call when safe.
12. Batch import produces aggregate `adapter.quality` and safe per-file source
    summaries.
13. Batch import remains process-local job status only.

Folder recursion, directory import, browser upload, drag/drop, copied imports,
app-data import retention, persistent import history, background workers,
cancellation, retries, import deletion, and database reset/delete/wipe remain
deferred.

## Definitions

### Source Artifact

A source artifact is one explicitly selected local `.jsonl` file containing
generated legacy saved-event records. It is an input artifact, not parser truth.

Source artifact facts that may be reported:

- safe display label;
- generated source artifact label;
- selected index after deterministic sorting;
- status category;
- record/event/skip counts;
- sanitized unsupported kind counts;
- sanitized warning codes;
- sanitized #212-style quality counts where applicable.

Source artifact facts that must not be reported:

- absolute path;
- raw file name when unsafe;
- raw JSONL line;
- raw payload;
- raw `raw_bytes_hash` value;
- secret-like text;
- webhook URL, API key, token, workbook ID, or stack trace.

### Batch / Source Group

A batch/source group is one explicit list of selected source artifacts imported
as one job, one adapter replay scope, and one SQLite ingest run.

The batch/source group owns only import provenance and quality context. It does
not own parser truth or replace match/game identity.

### Batch Source Label

The batch `source_artifact_label` must be safe and deterministic.

Allowed examples:

- `legacy_jsonl_batch:2_files:<short_hash>`
- `legacy_jsonl_batch_2026_05_30`
- user-provided safe labels such as `historic_batch_may_2026`

Forbidden labels:

- absolute paths;
- URLs;
- labels containing slashes or backslashes;
- raw Player.log snippets;
- raw JSONL payload snippets;
- raw hashes;
- webhook URLs, workbook IDs, API keys, tokens, secrets, or private path
  markers.

If a user supplies `source_artifact_label`, use the existing safe-label rules.
If no label is supplied, generate a safe batch label from non-sensitive stable
metadata such as count and a short digest of selected file basenames/order. The
digest source must not be exposed.

## Public Interface

### Adapter Surface

Recommended new adapter constant:

```text
ANALYTICS_LEGACY_JSONL_BATCH_IMPORT_SCHEMA_VERSION = "analytics_legacy_jsonl_batch_import.v1"
```

Recommended new adapter function:

```python
adapt_legacy_jsonl_file_batch(
    sources: Sequence[Path],
    *,
    source_artifact_label: str | None = None,
) -> LegacyJsonlAdapterResult
```

The function may return the existing `LegacyJsonlAdapterResult` if that result
gains batch/source-artifact summary fields, or a compatible
`LegacyJsonlBatchAdapterResult` that exposes the same existing result fields:

- `replay`
- `source_kind`
- `source_artifact_label`
- `files_processed`
- `records_seen`
- `events_processed`
- `events_skipped`
- `unsupported_kind_counts`
- `warnings`
- `quality`

Required additional batch fields, either as result attributes or serializable
fields consumed by the backend:

- `source_mode = "explicit_file_batch"`
- `files_selected`
- `files_accepted`
- `files_rejected`
- `source_artifacts`

`adapt_legacy_jsonl_artifacts(Path(...))` must remain compatible for existing
single-file and adapter-level directory callers. Codex C may share internal
helpers, but it must not make current file/directory adapter behavior silently
change.

### Backend Request Surface

Existing single-file request remains valid:

```json
{
  "source_path": "Z:\\synthetic\\events_a.jsonl",
  "source_artifact_label": "optional_safe_label"
}
```

New batch request:

```json
{
  "source_paths": [
    "Z:\\synthetic\\events_a.jsonl",
    "Z:\\synthetic\\events_b.jsonl"
  ],
  "source_artifact_label": "optional_safe_batch_label"
}
```

Required request behavior:

- accept exactly one of `source_path` or `source_paths`;
- reject requests that provide both;
- reject non-object requests;
- reject blank arrays;
- reject non-string entries;
- reject duplicate selected paths after normalization/resolution;
- reject URLs;
- reject UNC/network paths in v1;
- reject directories;
- reject missing files;
- reject non-`.jsonl` files;
- reject more than a documented maximum number of files.

Recommended maximum:

```text
MAX_LEGACY_JSONL_BATCH_FILES = 100
```

The maximum is a local-app safety bound, not an analytics truth rule. Codex C
may choose a smaller maximum if tests and UI copy reflect it.

### Backend Job Source Fields

Manual import job `source` should remain backward-compatible and may gain:

- `source_mode`: `single_file` or `explicit_file_batch`
- `files_selected`
- `files_accepted`
- `files_rejected`
- `source_group_label`
- `source_artifacts`

For batch imports:

- `source_display_label` should be a safe summary such as
  `2 selected JSONL files`;
- `source_file_extension` may remain `.jsonl`;
- `path_echoed` must remain `false`;
- full raw paths must not appear in any response field.

### Adapter Summary Fields

Manual import job `adapter` should remain backward-compatible and may gain:

- `source_mode`
- `files_selected`
- `files_accepted`
- `files_rejected`
- `source_artifacts`

`adapter.quality` must be the aggregate #212 quality object for the whole
batch.

Per-file source artifact summary shape:

```json
{
  "batch_index": 0,
  "source_artifact_label": "legacy_jsonl_file:0:<short_hash>",
  "source_display_label": "events_a.jsonl",
  "status": "processed",
  "records_seen": 10,
  "events_processed": 8,
  "events_skipped": 2,
  "processed_kind_counts": {"MatchState": 1},
  "unsupported_kind_counts": {},
  "skipped_reason_counts": {
    "blank_line": 0,
    "duplicate_raw_hash": 2,
    "unsupported_kind": 0
  },
  "adapter_warning_codes": []
}
```

Allowed per-file status values:

- `processed`
- `processed_with_skips`
- `rejected`
- `failed`

Per-file summaries must not include parser-normalized row data, raw payloads,
raw hashes, raw paths, stack traces, or SQLite internals.

### Frontend Surface

The frontend may extend the Manual Import section with:

- a multi-line local path input;
- a list editor for selected `.jsonl` paths;
- an explicit "batch import" mode;
- batch file-count display;
- batch-level quality display;
- safe per-file/source-artifact summaries.

The frontend must continue to:

- clear raw entered paths after terminal result or failure;
- call backend routes rather than parsing JSONL itself;
- avoid browser file upload in v1;
- avoid drag/drop raw file handling in v1;
- avoid localStorage/sessionStorage persistence of raw paths;
- avoid rendering raw paths in job result cards.

## Input Ordering

Batch imports must process files in deterministic internal order.

Required v1 ordering:

1. normalize and resolve each accepted path in backend memory;
2. sort accepted files by a deterministic local key before adapter replay;
3. use that sorted order for parser replay, raw-hash dedupe, source artifact
   summaries, and tests;
4. never echo the sort key if it contains a raw path.

Recommended local sort key:

```text
(resolved path string casefolded for internal ordering only, original normalized string as tie breaker)
```

Reason: this makes shuffled user input produce the same batch result on the
same machine without committing to path strings as public data.

The public output must expose only `batch_index` in sorted order and safe
labels. It must not expose absolute paths or path-derived sort keys.

## Replay And Dedupe Semantics

Batch import must replay all accepted files in one parser-state scope:

- reset parser runtime state once before the batch replay;
- seed any required in-memory card lookup exactly as the existing adapter does;
- process selected files in deterministic order;
- maintain one `seen_raw_hashes` set across the whole batch;
- skip duplicate nonblank raw hashes across files;
- build one combined parser-normalized replay from final parser state;
- reset parser runtime state after success or failure.

Batch import must not:

- replay files one by one and then concatenate match/game rows if that would
  lose state continuity;
- dedupe per file only;
- expose raw hash values;
- change parser match/game identity or deduplication logic;
- change saved-event event class mapping;
- change `saved_event_replay.latest_jsonl_files(...)` semantics.

## Output And Ingest Semantics

Batch import should produce one combined replay:

- `source_kind = "saved_event_replay"`
- `source_artifact_label = <safe batch label>`
- `match_log_rows`
- `game_log_rows`
- `gameplay_action_entries`
- `opponent_card_observations`
- `field_evidence_entries`
- `parser_commit`
- `parser_version`
- `generated_at`

First version may continue to output empty gameplay/action/observation/evidence
lists if the current adapter does.

SQLite ingest must remain all-or-nothing for the batch:

- validate all selected paths before app-data or DB creation;
- adapt all selected files into one replay before opening/creating SQLite;
- call `ingest_parser_normalized_replay(...)` once per successful batch;
- do not partially ingest some files if another selected file fails;
- do not create a SQLite migration or import-history table for batch metadata.

Existing ingest idempotency and upsert semantics must be preserved. Re-importing
the same batch should not duplicate SQLite facts.

## Batch Quality Aggregation

Aggregate `adapter.quality` must reuse the #212 schema:

```text
analytics_legacy_jsonl_import_quality_breakdown.v1
```

Batch-level aggregate fields must roll up across all accepted files:

- `records_seen`
- `events_processed`
- `events_skipped`
- `processed_kind_counts`
- `unsupported_kind_counts`
- `skipped_reason_counts`
- `blank_line_count`
- `duplicate_raw_hash_count`
- `unsupported_kind_skip_count`
- `output_gap_counts`
- `adapter_warning_counts`
- `adapter_warning_codes`
- `ingest_warning_codes`
- `routing_hints`
- `privacy`

Required rollup rules:

- per-file `records_seen` sums to aggregate `records_seen`;
- per-file `events_processed` sums to aggregate `events_processed`;
- per-file `events_skipped` sums to aggregate `events_skipped` for input skip
  reasons;
- per-file processed kind counts sum to aggregate `processed_kind_counts`;
- per-file unsupported kind counts sum to aggregate `unsupported_kind_counts`;
- duplicate raw hashes across files count in the file where the duplicate is
  encountered in deterministic replay order;
- output gap counts are batch-level parser replay/output gaps, not per-file
  proof of causality;
- `privacy.has_private_path_echo`, `privacy.raw_payload_exposed`, and
  `privacy.raw_hash_exposed` must remain `false`.

Batch-level `quality_status`:

- `complete` only when there are no skips, output gaps, adapter warnings, or
  ingest warnings;
- `degraded` when a batch produces ingestable rows with skips, unsupported
  kinds, output gaps, adapter warnings, or ingest warnings;
- `failed` when adapter or ingest failure prevents a successful batch import.

## Error Behavior

### Request Validation

Request validation failures must return sanitized rejected jobs and must not
create app-data directories or SQLite databases.

Required error categories to consider:

- `source_request_invalid`
- `source_path_required`
- `source_paths_required`
- `source_path_and_source_paths_conflict`
- `source_paths_empty`
- `source_paths_too_many`
- `source_path_invalid`
- `source_path_duplicate`
- `source_path_url_not_allowed`
- `source_path_unc_not_allowed`
- `source_path_missing`
- `source_path_directory_not_allowed`
- `source_path_extension_not_allowed`
- `source_path_not_file`
- `source_artifact_label_invalid`

The exact set may differ, but tests must prove invalid paths are rejected
without raw path echo and before database creation.

### Adapter Failure

Malformed selected files should fail the whole batch safely:

- invalid JSON;
- invalid UTF-8;
- non-object JSONL record;
- malformed supported saved-event record;
- no ingestable parser-normalized rows across the whole batch.

Failed batch jobs must not write partial SQLite facts. Failed-quality summaries
may include sanitized failure categories and file counts, but must not include
raw lines, raw payloads, raw paths, raw hashes, stack traces, or SQL internals.

### Degraded Success

The batch may succeed with `degraded` status when it produces ingestable rows
but has:

- blank lines;
- duplicate raw hashes;
- unsupported event kinds;
- stale legacy-derived mismatch warnings;
- incomplete summary output gaps;
- ingest warnings.

Degraded does not mean bad data was fixed downstream. It means parser-normalized
rows were produced with visible caveats.

## Side Effects

Allowed side effects for future Codex C implementation:

- validate explicit file-list requests;
- add batch adapter orchestration and safe source artifact summaries;
- call existing parser/state replay and existing analytics ingest boundaries;
- create app-data folders and SQLite database only after successful validation
  and adapter replay;
- update frontend Manual Import display and tests;
- add synthetic tests and implementation handoff documentation.

Forbidden side effects:

- no raw JSONL copying;
- no raw Player.log storage;
- no new SQLite migration or schema change;
- no generated database committed to the repo;
- no persistent job-history file;
- no folder recursion;
- no browser upload or drag/drop raw file import;
- no new destructive backend routes or UI controls;
- no live watcher behavior;
- no Google Sheets, workbook, webhook, Apps Script, Match Journal, OpenAI, AI,
  Line Tracer, or production behavior.

## Compatibility

Codex C must preserve:

- existing single-file `source_path` request behavior;
- existing `POST /api/imports/jsonl` route;
- existing `GET /api/imports/jobs/{job_id}` route;
- existing process-local job storage behavior;
- existing path redaction and safe source label behavior;
- existing adapter file input behavior;
- existing adapter directory input behavior for adapter-level callers;
- existing manual import job top-level fields;
- existing `adapter.quality` #212 shape;
- existing parser replay and SQLite ingest call boundaries.

If implementation needs to bump the local app manual import schema version,
Codex C must update backend constants, frontend constants, API validation, and
tests together, then explain why the bump was necessary in the implementation
handoff. A schema bump is allowed only for the local app job response/request
shape, not for SQLite.

## Unknowns And Open Questions

- Whether user-facing batch input should be a multi-line text area, a repeated
  path list, or a small "add path" control.
- Whether batch size should cap at 25, 50, or 100 files in the first UI.
- Whether per-file safe display labels should use sanitized basenames or only
  generic `file 1`, `file 2` labels when basenames are unsafe.
- Whether future folder import should use adapter directory semantics or a
  separate explicit folder contract.
- Whether persistent sanitized import history should later store batch summaries
  under app-data; this is out of scope for v1.
- Whether output gaps can ever be attributed to a specific source artifact
  without misleading the user; v1 should keep output gaps batch-level.

## Suspected Gaps

- Current backend validation accepts only `source_path`, not `source_paths`.
- Current frontend import request type accepts only one `source_path`.
- Current frontend UI has one path input, not a batch selector/list.
- Current job summaries do not include `source_mode`, `files_selected`,
  `files_accepted`, `files_rejected`, or `source_artifacts`.
- Current adapter does not expose a public explicit-file-list function.
- Current tests do not cover cross-file reconstruction, shuffled input
  determinism, or duplicate raw-hash counts across explicit files.
- Current #212 quality implementation is present locally but not yet known to
  be merged/tracked at the time this contract was written.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- saved-event replay semantics;
- parser state final reconciliation;
- parser event classes;
- event kind values;
- match/game identity;
- parser-owned deduplication semantics;
- analytics SQLite schema or migration SQL;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- output transport;
- Google Sheets behavior;
- Match Journal behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- production behavior;
- secrets, credentials, tokens, API keys, webhook URLs, or environment-variable
  contracts;
- raw Player.log files;
- private legacy JSONL artifacts;
- raw payloads, raw saved-event lines, raw hashes, or raw paths;
- generated SQLite database/WAL/SHM/journal files inside the repo;
- runtime status files;
- failed-delivery payload artifacts;
- workbook exports;
- generated card/tier data;
- destructive import/database/job/launcher/UI actions.

## Out Of Scope

- Implementation code in this Codex B pass.
- Opening a PR or targeting `main`.
- Changing parser behavior.
- Changing saved-event replay event mapping or directory latest-file
  semantics.
- Changing parser match/game identity or deduplication.
- Changing analytics SQLite schema/migrations.
- Adding, editing, sanitizing, or committing real private JSONL artifacts.
- Storing raw JSONL payloads or raw Player.log lines in SQLite.
- Adding a persistent import history.
- Copying JSONL files into app data by default.
- Browser file upload, drag/drop, or raw-content upload.
- Recursive folder import.
- Import deletion, job deletion, retries, cancellation, queue management, or
  database reset/wipe/clear.
- Live Player.log watching or watcher process control.
- Curated analytics dashboards beyond the Manual Import result panel.
- Google Sheets sync, workbook export, webhook posting, Apps Script changes,
  Match Journal, Line Tracer, AI/OpenAI/coaching behavior, gameplay advice,
  hidden-card inference, archetype classification, or production deployment.

## Tests Required

Focused adapter tests:

```powershell
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py
```

Required adapter coverage:

- explicit two-file batch reconstructs one match/game when supported events are
  split across files;
- shuffled input paths produce the same deterministic replay result and source
  artifact order;
- duplicate raw hashes across files increment aggregate and per-file duplicate
  counts without exposing hashes;
- unsupported kinds aggregate across files;
- safe per-file summaries include counts and safe labels only;
- adapter-level single-file behavior still works;
- adapter-level directory behavior still uses existing latest-file selection
  semantics;
- malformed one-file-in-batch failure does not produce replay rows or raw
  payload/path/hash output.

Focused backend/manual import tests:

```powershell
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
```

Required backend coverage:

- `source_paths` batch request succeeds with synthetic files;
- existing `source_path` single-file request still succeeds;
- request with both `source_path` and `source_paths` rejects safely;
- empty, too-large, non-string, duplicate, missing, URL, UNC, directory, and
  non-`.jsonl` batch entries reject before database creation;
- batch job response includes safe batch source fields and per-file summaries;
- batch job response includes aggregate `adapter.quality`;
- no raw submitted path, raw payload, raw hash, stack trace, URL, secret, or
  private marker appears in JSON responses;
- re-importing the same batch into the same temp app database does not
  duplicate SQLite facts;
- no destructive routes or DELETE methods are added.

Frontend validation:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Required frontend coverage:

- TypeScript request type supports `source_path` and `source_paths` with exact
  one-of intent;
- UI can submit a batch without browser file upload;
- UI clears raw entered paths after terminal result or failure;
- UI displays safe batch count, aggregate quality, and per-file summaries;
- UI handles rejected, failed, degraded, and succeeded batch states;
- no raw paths, raw payloads, raw hashes, or destructive controls render.

Adjacent checks:

```powershell
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all
```

Path-scoped protected-surface check:

```powershell
@'
docs/contracts/analytics_legacy_jsonl_batch_import.md
docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
src/mythic_edge_parser/local_app/import_jobs.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
tests/test_analytics_manual_jsonl_import.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/api.test.ts
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Path-scoped secret/private-marker check:

```powershell
@'
docs/contracts/analytics_legacy_jsonl_batch_import.md
docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
src/mythic_edge_parser/local_app/import_jobs.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
tests/test_analytics_manual_jsonl_import.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/api.test.ts
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated artifact check:

- Codex C/E should report `git status --short --branch` and confirm no raw
  JSONL artifacts, raw Player.log files, generated SQLite DB/WAL/SHM/journal
  files inside the repo, runtime artifacts, failed-delivery artifacts, workbook
  exports, screenshots with private data, or `node_modules/` files are changed
  or untracked.

## Acceptance Criteria

Codex C satisfies this contract when:

- existing single-file manual import behavior is preserved;
- explicit `source_paths` batch requests are supported by the backend and
  frontend;
- batch validation rejects unsafe or invalid file lists before app-data/DB
  creation;
- batch adapter replay processes accepted files in deterministic order;
- batch adapter dedupes raw hashes across the whole batch without exposing
  hashes;
- one combined parser-normalized replay is ingested once per successful batch;
- batch job summaries expose safe batch/source-artifact fields and aggregate
  #212 `adapter.quality`;
- per-file summaries use safe labels and counts only;
- re-importing the same batch is idempotent for SQLite facts;
- no raw payloads, raw paths, raw hashes, secrets, stack traces, generated
  private artifacts, or destructive controls are exposed;
- no parser, saved-event replay, SQLite schema, workbook, webhook, Apps
  Script, Google Sheets, OpenAI/AI, Line Tracer, Match Journal, production, or
  destructive-action behavior changes are made;
- focused backend, adapter, frontend, Ruff, diff, protected-surface, and
  secret/private-marker validations are recorded.

Codex B validation for this contract:

```powershell
git diff --check
@'
docs/contracts/analytics_legacy_jsonl_batch_import.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_legacy_jsonl_batch_import.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #213.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Related quality issue:
https://github.com/Tahjali11/Mythic-Edge/issues/212

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_legacy_jsonl_batch_import.md

Goal:
Compare the current legacy JSONL adapter, manual import backend job response,
frontend API/types/display, and focused tests against the contract. Implement
only the explicit multi-file legacy JSONL batch import and source artifact
grouping behavior. Produce
docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated local changes.
- Reconcile the #212 import-quality work: if the #212 quality shape is not
  present in this branch/worktree, stop and route sequencing back instead of
  inventing a parallel quality shape.
- State what batch import is supposed to do, what current code already does,
  what gaps remain, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_legacy_jsonl_batch_import.md
- docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
- docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
- docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
- docs/contracts/analytics_parser_normalized_replay_ingest.md
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- src/mythic_edge_parser/local_app/import_jobs.py
- src/mythic_edge_parser/local_app/backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- tests/test_analytics_manual_jsonl_import.py
- frontend focused tests

Implement only:
- explicit `source_paths` request support on existing manual import route;
- exact-one-of `source_path` / `source_paths` validation;
- deterministic accepted-file ordering;
- one parser replay scope across the selected files;
- raw-hash dedupe across the whole batch;
- one combined parser-normalized replay and one SQLite ingest call;
- safe batch/source artifact labels and summaries;
- aggregate #212 `adapter.quality`;
- frontend API/type/display support for batch import;
- focused synthetic tests and implementation handoff.

Do not:
- change parser behavior;
- change saved-event replay semantics or latest-file directory selection;
- change parser state final reconciliation;
- change parser event classes or event kind values;
- change match/game identity or parser-owned deduplication;
- change analytics SQLite schema/migrations;
- store, copy, sanitize, fixture, or commit real private JSONL or Player.log data;
- expose raw payloads, raw paths, raw hashes, stack traces, secrets, webhook
  URLs, API keys, or private local artifacts;
- add folder recursion, browser upload, drag/drop import, copied import
  retention, persistent import history, cancellation, retries, deletion,
  database reset/wipe/clear, live Player.log watching, Google Sheets, workbook,
  webhook, Apps Script, Match Journal, OpenAI/AI, Line Tracer, coaching,
  production, or destructive UI/backend behavior;
- target main;
- open a PR, stage, commit, push, close issues, or mark tracker #204 complete.

Validation:
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all

Also run path-scoped protected-surface and secret/private-marker scans over the
contract, implementation handoff, touched adapter/backend/frontend/test files.

Final handoff must include:
- role performed
- issue/tracker/umbrella reviewed
- contract used
- files changed
- exact adapter/backend/frontend/test sections changed
- observed behavior before implementation
- implemented batch request/source-artifact/quality shape
- validation results
- remaining unverified layers
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/213"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_quality_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/212"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #213"
  target_artifact: "docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md"
  contract_artifact: "docs/contracts/analytics_legacy_jsonl_batch_import.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface scan for docs/contracts/analytics_legacy_jsonl_batch_import.md"
    - "path-scoped secret/private-marker scan for docs/contracts/analytics_legacy_jsonl_batch_import.md"
  stop_conditions:
    - "Do not target main."
    - "Do not implement #213 before reconciling #212 import-quality availability."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change saved-event replay semantics or latest-file directory selection."
    - "Do not change analytics SQLite schema or migrations."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose raw payloads, raw paths, raw hashes, or destructive import/database/job actions."
```
