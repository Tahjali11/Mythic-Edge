# Analytics Legacy JSONL Import Quality Breakdown Contract

## Module

Sanitized import-quality breakdown for legacy JSONL manual imports in the
local developer app.

Plain English: this contract makes degraded manual imports explain *why* the
legacy JSONL adapter skipped records without exposing raw local files, raw
payloads, raw hashes, raw paths, or changing parser behavior.

This is a reporting-only contract. It does not define a new parser, a new
SQLite schema, a raw artifact retention policy, a live Player.log watcher, an
analytics dashboard, Line Tracer, AI coaching, or destructive import controls.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/212>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Related manual import issue: <https://github.com/Tahjali11/Mythic-Edge/issues/211>
- Manual import contract:
  `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- Legacy adapter contract:
  `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
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
contract pass. Unrelated local launcher/test changes were present and are not
owned by this contract.

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
- source issue #212
- `docs/project_roadmap.md`
- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- `docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`

## Risk Tier

Medium.

Reason: this slice is reporting-only if it adds sanitized counts and display
fields without changing replay, parser, ingest, schema, or storage semantics.

It becomes High if implementation changes parser interpretation, saved-event
replay semantics, deduplication behavior, SQLite schema, backend route
authority, frontend destructive actions, raw artifact retention, or protected
surfaces.

## Owning Layer

Primary owner: local analytics usability / import reporting layer.

Truth boundaries:

- Parser/state owns MTGA event interpretation, match/game identity, final
  reconciliation, parser event classes, and parser-managed facts.
- `analytics_legacy_jsonl_adapter.py` owns safe adaptation of generated
  legacy JSONL event archives into parser-normalized replay input.
- `analytics_ingest.py` owns writing already-normalized parser facts into
  local SQLite.
- `import_jobs.py` owns local backend orchestration and sanitized job-status
  responses.
- The frontend owns safe display of import quality only.
- Legacy JSONL `derived` fields remain diagnostic only and must not become
  parser truth.

The quality breakdown may explain adapter and ingest health. It must not
decide what happened in Arena, infer missing gameplay facts, classify decks,
judge player mistakes, or promote skipped legacy data into analytics truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`

Future Codex C implementation files authorized by this contract:

- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`, only for displaying the quality breakdown cleanly
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md`

Referenced but not owned:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/state.py`
- analytics migration SQL
- SQLite generated database files
- raw local JSONL artifacts

Codex C must route back to Codex B before changing parser behavior, replay
semantics, SQLite schema/migrations, backend route inventory beyond the
existing manual import job routes, or frontend behavior outside import-quality
display.

## Observed Current Behavior

The manual import workflow exists on the current branch:

- `POST /api/imports/jsonl` runs a synchronous manual import for an explicit
  local `.jsonl` path.
- `GET /api/imports/jobs/{job_id}` returns the process-local sanitized job
  summary for that backend process.
- Backend responses already avoid echoing the submitted full path.
- The frontend displays source label, adapter events processed, adapter events
  skipped, match/game row counts, warnings, and errors.
- The workflow writes parser-normalized facts into the app-owned SQLite
  database only after source validation and successful adapter replay.

The current legacy JSONL adapter exposes:

- `files_processed`
- `records_seen`
- `events_processed`
- `events_skipped`
- `unsupported_kind_counts`
- `warnings`

Observed skip/reporting behavior in current adapter code:

- blank JSONL lines increment `events_skipped` and are not counted in
  `records_seen`;
- nonblank records increment `records_seen`;
- duplicate nonblank `raw_bytes_hash` values increment `events_skipped` and
  are skipped before event-kind reconstruction;
- unsupported event kinds increment `unsupported_kind_counts` and
  `events_skipped`;
- incomplete match summaries are reported as warnings such as
  `incomplete_match_summaries_skipped:<count>`;
- stale legacy `derived.match_id` values are reported as warnings such as
  `derived_match_id_mismatch:<safe_label>`;
- invalid JSON, non-object records, malformed supported records, invalid UTF-8,
  unsafe source labels, unreadable files, and no-ingestable-row outcomes fail
  the adapter rather than producing a degraded success.

Observed gap:

- `events_skipped` combines blank lines, duplicate raw hashes, unsupported
  event kinds, and other skipped conditions into one number.
- The job response and frontend do not show a structured reason breakdown.
- The frontend cannot explain whether a degraded import is probably harmless,
  adapter/reporting follow-up, parser backlog, analytics ingest backlog, or
  source-artifact quality trouble.
- Adapter warnings are currently raw category strings, not a compact structured
  warning-code/count object.

## Contract Decision

Add an additive sanitized quality object named `quality`.

Required placement:

- `LegacyJsonlAdapterResult.quality`
- manual import job response under `adapter.quality`
- frontend `ManualImportAdapter.quality`
- frontend manual import result display

The existing top-level fields must remain compatible:

- `files_processed`
- `records_seen`
- `events_processed`
- `events_skipped`
- `unsupported_kind_counts`
- `warnings`

The first implementation must not remove, rename, or change the meaning of
those existing fields. It may derive them from the new quality counters
internally only if observable semantics remain the same.

Recommended public constant:

```text
ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION = "analytics_legacy_jsonl_import_quality_breakdown.v1"
```

Recommended object value:

```text
mythic_edge_legacy_jsonl_import_quality
```

## Public Interface

### Adapter Result

`LegacyJsonlAdapterResult` should gain a backward-compatible field:

```python
quality: dict[str, object]
```

or an equivalent frozen dataclass that serializes to the same JSON-compatible
shape. The field must be optional only during internal construction; public
adapter results from `adapt_legacy_jsonl_artifacts(...)` must include it.

### Manual Import Job Response

`adapter` in the manual import job response must include:

```json
{
  "status": "degraded",
  "files_processed": 1,
  "records_seen": 457,
  "events_processed": 121,
  "events_skipped": 336,
  "unsupported_kind_counts": {},
  "warnings": ["events_skipped"],
  "quality": {}
}
```

The `quality` object must be present for terminal `succeeded`, `degraded`, and
`failed` adapter/job states. For `not_started` adapter state, it may be present
with zero counts or omitted from the `not_started` placeholder if frontend and
backend validators tolerate that placeholder explicitly.

### Frontend Type/API Surface

The frontend should add a `LegacyJsonlImportQuality` or equivalent type and
validate enough of the object to prevent incompatible or malformed backend
responses from being silently accepted.

The frontend should display a compact breakdown, not raw data. Suggested
display rows:

- quality status
- processed kind counts
- skipped reasons
- unsupported kind counts
- output gaps
- adapter warning codes
- ingest warning codes
- routing hints

The UI may collapse zero-count sections.

## Quality Object Schema

Required `quality` shape:

```json
{
  "object": "mythic_edge_legacy_jsonl_import_quality",
  "schema_version": "analytics_legacy_jsonl_import_quality_breakdown.v1",
  "quality_status": "degraded",
  "records_seen": 457,
  "events_processed": 121,
  "events_skipped": 336,
  "processed_kind_counts": {
    "MatchState": 12,
    "GameState": 80,
    "GameResult": 29
  },
  "unsupported_kind_counts": {
    "ConnectionError": 10
  },
  "skipped_reason_counts": {
    "blank_line": 0,
    "duplicate_raw_hash": 300,
    "unsupported_kind": 36
  },
  "blank_line_count": 0,
  "duplicate_raw_hash_count": 300,
  "unsupported_kind_skip_count": 36,
  "output_gap_counts": {
    "incomplete_match_summary": 0,
    "incomplete_game_summary": 0,
    "incomplete_summary_unclassified": 0
  },
  "adapter_warning_counts": {
    "events_skipped": 1
  },
  "adapter_warning_codes": ["events_skipped"],
  "ingest_warning_codes": [],
  "routing_hints": [
    {
      "code": "duplicate_raw_hashes",
      "category": "harmless_or_repeated_export",
      "severity": "info",
      "count": 300
    }
  ],
  "privacy": {
    "has_private_path_echo": false,
    "raw_payload_exposed": false,
    "raw_hash_exposed": false
  }
}
```

Required scalar fields:

- `object`
- `schema_version`
- `quality_status`
- `records_seen`
- `events_processed`
- `events_skipped`
- `blank_line_count`
- `duplicate_raw_hash_count`
- `unsupported_kind_skip_count`

Required mapping fields:

- `processed_kind_counts`
- `unsupported_kind_counts`
- `skipped_reason_counts`
- `output_gap_counts`
- `adapter_warning_counts`

Required list fields:

- `adapter_warning_codes`
- `ingest_warning_codes`
- `routing_hints`

Required privacy fields:

- `privacy.has_private_path_echo = false`
- `privacy.raw_payload_exposed = false`
- `privacy.raw_hash_exposed = false`

Allowed `quality_status` values:

- `complete`
- `degraded`
- `failed`

Allowed first-version skipped reason keys:

- `blank_line`
- `duplicate_raw_hash`
- `unsupported_kind`

Allowed first-version output gap keys:

- `incomplete_match_summary`
- `incomplete_game_summary`
- `incomplete_summary_unclassified`

If current code can only detect incomplete summary gaps as a combined match/game
adapter warning, it must use `incomplete_summary_unclassified` and leave the
specific match/game counts at `0`. Do not invent a split that current code
cannot prove safely.

## Field Semantics

`records_seen`:

- preserves current adapter meaning: nonblank JSONL records seen by the
  adapter;
- does not include blank lines unless a later contract explicitly adds a
  separate physical-line count.

`events_processed`:

- count of supported, reconstructed events passed into current parser/state
  replay logic.

`events_skipped`:

- preserves current adapter meaning and must remain equal to the top-level
  adapter field;
- for successful/degraded adapter results, it should equal the sum of
  `blank_line_count + duplicate_raw_hash_count + unsupported_kind_skip_count`
  unless a future additional skipped reason is added under this contract with
  tests.

`processed_kind_counts`:

- counts supported event kinds that were actually reconstructed and fed to
  parser/state;
- keys must use the same safe label policy as unsupported kinds;
- must not include raw payload values, raw hashes, file names, or source paths.

`unsupported_kind_counts`:

- preserves existing behavior;
- counts unsupported kinds only when the record reaches unsupported-kind
  handling;
- records skipped earlier because of duplicate raw hash must not be counted as
  unsupported kinds.

`duplicate_raw_hash_count`:

- counts nonblank records skipped because their nonblank `raw_bytes_hash`
  already appeared in the selected import scope;
- must never expose raw hash values;
- must not change dedupe scope or ordering.

`blank_line_count`:

- counts blank JSONL lines skipped before JSON parsing;
- blank lines are usually harmless, but the UI must present that as a routing
  hint, not as proof that all skipped data is irrelevant.

`output_gap_counts`:

- counts parser-normalized output gaps discovered after replay, such as
  incomplete summaries skipped while building replay rows;
- output gaps are analytically important and must not be folded into harmless
  input skips.

`adapter_warning_codes` and `adapter_warning_counts`:

- codes are sanitized warning categories such as
  `events_skipped`, `unsupported_event_kinds`, `derived_match_id_mismatch`, and
  `incomplete_match_summaries_skipped`;
- dynamic suffixes such as specific match IDs should be counted but not exposed
  by default in the quality object;
- the existing top-level `warnings` list may remain for compatibility.

`ingest_warning_codes`:

- should copy or derive sanitized warning codes from the ingest result when the
  manual import job has an ingest result;
- the adapter may return an empty list because it does not own ingest.

`routing_hints`:

- are conservative triage labels for humans;
- they must not assert that skipped data is definitely irrelevant unless a
  future contract proves that claim for a specific category;
- they must not become parser truth, analytics truth, or UI-owned data quality
  policy.

## Routing Hint Policy

Allowed routing hint categories:

- `harmless_expected_skip`
- `harmless_or_repeated_export`
- `adapter_reporting_follow_up`
- `parser_or_adapter_backlog`
- `analytics_ingest_backlog`
- `source_artifact_problem`
- `unsupported_legacy_shape`
- `unknown`

Allowed severities:

- `info`
- `warning`
- `action_needed`

Required first-version hints:

- `blank_line_count > 0` should produce a hint with category
  `harmless_expected_skip` and severity `info`.
- `duplicate_raw_hash_count > 0` should produce a hint with category
  `harmless_or_repeated_export` and severity `info` or `warning`.
- `unsupported_kind_skip_count > 0` should produce a hint with category
  `parser_or_adapter_backlog` or `unknown` and severity `warning`.
- incomplete summary output gaps should produce a hint with category
  `analytics_ingest_backlog` or `source_artifact_problem` and severity
  `warning` or `action_needed`.
- malformed/invalid adapter failure should produce a hint with category
  `source_artifact_problem` or `unsupported_legacy_shape`.

Routing hints must not display raw payload snippets, full paths, raw hashes,
stack traces, private file names, secrets, tokens, webhook URLs, API keys, or
SQLite internals.

## Error Behavior

Malformed input must preserve existing fail-fast adapter behavior unless Codex
B later changes this contract.

Required failure reporting:

- invalid JSONL should fail safely with a sanitized adapter/job error code;
- invalid UTF-8 should fail safely with a sanitized adapter/job error code;
- non-object JSONL records should fail safely;
- malformed supported saved-event records should fail safely;
- unsupported event kinds remain skippable when parser-normalized rows are
  still produced;
- no-ingestable-row output remains a failure, not a degraded success;
- unsafe source labels, missing paths, URLs, UNC paths, directories, and
  non-`.jsonl` files remain rejected or failed under the existing manual import
  contract.

For failed adapter states, `quality_status` must be `failed`. Counters may
represent work completed before the failure only if they can be reported
without leaking raw data and without changing fail-fast semantics. If not,
return zero/default counters plus a sanitized `adapter_warning_codes` or
`routing_hints` entry that describes the failure category.

## Side Effects

Allowed side effects for future Codex C implementation:

- add sanitized counters and quality-object construction in memory;
- include the quality object in existing adapter and manual import job
  responses;
- display the quality object in the existing Manual Import frontend surface;
- add synthetic tests and implementation handoff documentation.

Forbidden side effects:

- no raw JSONL copying;
- no raw Player.log storage;
- no new SQLite migration or schema change;
- no generated database committed to the repo;
- no persistent job-history file;
- no new backend routes unless routed back to Codex B;
- no destructive UI actions;
- no live watcher behavior;
- no Google Sheets, workbook, webhook, Apps Script, Match Journal, OpenAI, AI,
  Line Tracer, or production behavior.

## Compatibility

Codex C must preserve:

- existing adapter function name and call pattern;
- existing `LegacyJsonlAdapterResult` top-level fields;
- existing manual import job object and schema version unless the implementation
  deliberately bumps the schema and updates frontend tests;
- existing `POST /api/imports/jsonl` and `GET /api/imports/jobs/{job_id}`
  routes;
- existing path redaction and source label safety behavior;
- existing adapter fail-fast behavior for malformed records;
- existing parser replay and ingest call boundaries.

If adding `adapter.quality` requires a manual import job schema version bump,
Codex C must update backend and frontend constants/tests together and explain
the compatibility decision in the implementation handoff. A schema bump is
allowed because the response shape changes, but it must remain additive and
local-app-only.

## Unknowns And Open Questions

- Whether `incomplete_game_summary_count` can be distinguished safely from
  current adapter state without changing parser/state behavior.
- Whether duplicate raw-hash counts should later be split per selected file or
  only aggregate across the import scope.
- Whether routing hints should eventually classify specific unsupported event
  kinds into stable categories; v1 should stay conservative.
- Whether future persistent import history should store sanitized quality
  summaries under app-data; this is out of scope for v1.
- Whether frontend should show all zero-count fields or hide zero sections for
  readability.

## Suspected Gaps

- Current adapter stats do not expose `blank_line_count`.
- Current adapter stats do not expose `duplicate_raw_hash_count`.
- Current adapter stats do not expose `processed_kind_counts`.
- Current adapter warnings are not structured as warning-code counts.
- Current manual import job summaries do not include `adapter.quality`.
- Current frontend only renders the coarse `adapter.events_skipped` number.
- Current tests cover unsupported/duplicate safe summaries but do not prove
  reason-level skip counts or frontend rendering of quality breakdowns.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- saved-event replay semantics
- parser state final reconciliation
- parser event classes
- event kind values
- match/game identity
- deduplication semantics
- analytics SQLite schema or migration SQL
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- Google Sheets behavior
- Match Journal behavior
- OpenAI/model-provider behavior
- AI/coaching behavior
- Line Tracer behavior
- production behavior
- secrets, credentials, tokens, API keys, webhook URLs, or environment-variable
  contracts
- raw Player.log files
- private legacy JSONL artifacts
- raw payloads, raw saved-event lines, raw hashes, or raw paths
- generated SQLite database/WAL/SHM/journal files inside the repo
- runtime status files
- failed-delivery payload artifacts
- workbook exports
- generated card/tier data
- destructive import/database/job/launcher/UI actions

## Out Of Scope

- Implementation code in this Codex B pass.
- Opening a PR or targeting `main`.
- Changing parser behavior.
- Changing adapter replay semantics or dedupe scope.
- Changing analytics ingest semantics.
- Adding, editing, sanitizing, or committing real private JSONL artifacts.
- Storing raw JSONL payloads or raw Player.log lines in SQLite.
- Adding a SQLite schema/migration for import quality.
- Persistent import history.
- Browser file upload, drag/drop import, copied imports under app-data, or raw
  content upload.
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

- quality schema/version/object is present on successful adapter results;
- blank lines increment `blank_line_count` and `skipped_reason_counts.blank_line`;
- duplicate raw hashes increment `duplicate_raw_hash_count` without exposing
  hash values;
- unsupported event kinds increment `unsupported_kind_skip_count` and preserve
  `unsupported_kind_counts`;
- processed supported events increment `processed_kind_counts`;
- `events_skipped` remains compatible with the existing top-level field;
- stale `derived` mismatch warnings become sanitized warning codes/counts;
- incomplete summaries become structured output-gap counts when safely
  distinguishable, or unclassified output-gap counts otherwise;
- malformed JSONL still fails without raw line or payload echoing.

Focused backend/manual import tests:

```powershell
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
```

Required backend coverage:

- manual import job response includes `adapter.quality`;
- degraded import with unsupported and duplicate records shows structured
  reason counts;
- failed adapter import reports `quality_status = failed` or equivalent safe
  failure quality;
- job response does not expose full submitted paths, raw payloads, raw hashes,
  stack traces, secrets, URLs, or private path markers;
- existing rejected path cases still reject before app-data/database creation.

Frontend validation:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Required frontend coverage:

- TypeScript types include the quality object;
- API validation rejects incompatible quality schema/object if Codex C chooses
  strict validation;
- Manual Import result displays skipped reason counts and routing hints;
- zero-count sections are handled cleanly;
- frontend does not render raw path, raw payload, or raw hash values;
- destructive controls remain absent.

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
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md
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
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md
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

- `LegacyJsonlAdapterResult` exposes a sanitized quality object.
- Existing adapter top-level stats remain backward-compatible.
- Manual import job responses include `adapter.quality`.
- Frontend types/API/display handle the quality object.
- The quality object distinguishes blank lines, duplicate raw-hash skips,
  unsupported-kind skips, processed kind counts, adapter warning codes, ingest
  warning codes, and output gaps where safely observable.
- The UI gives conservative routing hints without claiming skipped data is
  definitely irrelevant.
- No raw payloads, raw paths, raw hashes, secrets, stack traces, or private
  local artifacts are exposed.
- Synthetic tests prove the reporting behavior and privacy boundaries.
- No parser, replay, ingest, SQLite schema, workbook, webhook, Apps Script,
  Google Sheets, OpenAI/AI, production, or destructive-action behavior changes
  are made.
- Focused backend, adapter, frontend, Ruff, diff, protected-surface, and
  secret/private-marker validations are recorded.

Codex B validation for this contract:

```powershell
git diff --check
@'
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #212.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Related manual import issue:
https://github.com/Tahjali11/Mythic-Edge/issues/211

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md

Goal:
Compare the current legacy JSONL adapter, manual import backend job response,
frontend API/types/display, and focused tests against the contract. Implement
only the reporting-only sanitized import-quality breakdown. Produce
docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated local changes.
- State what the quality breakdown is supposed to do, what current code already
  reports, what gap remains, and the minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
- docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
- docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- src/mythic_edge_parser/local_app/import_jobs.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- tests/test_analytics_manual_jsonl_import.py
- frontend focused tests

Implement only:
- additive sanitized adapter quality object;
- reason-level skip counts for blank lines, duplicate raw hashes, and
  unsupported kinds;
- processed kind counts;
- sanitized adapter warning code/count fields;
- output gap counts where safely observable without changing behavior;
- manual import job propagation under adapter.quality;
- frontend type/API/display support for quality breakdown;
- synthetic tests proving reporting and privacy boundaries;
- implementation handoff.

Do not:
- change parser behavior;
- change saved-event replay semantics or dedupe scope;
- change parser state final reconciliation;
- change parser event classes or event kind values;
- change match/game identity;
- change analytics SQLite schema/migrations;
- store raw JSONL or raw Player.log payloads;
- expose raw payloads, raw paths, raw hashes, stack traces, secrets, webhook
  URLs, API keys, or private local artifacts;
- add live Player.log watching;
- add Google Sheets, workbook, webhook, Apps Script, Match Journal, OpenAI/AI,
  Line Tracer, coaching, production, or destructive UI/backend behavior;
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
- implemented quality schema
- validation results
- remaining unverified layers
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/212"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_manual_import_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/211"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #212"
  target_artifact: "docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md"
  contract_artifact: "docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface scan for docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md"
    - "path-scoped secret/private-marker scan for docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change saved-event replay semantics or dedupe scope."
    - "Do not change analytics SQLite schema or migrations."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose raw payloads, raw paths, raw hashes, or destructive import/database/job actions."
```
