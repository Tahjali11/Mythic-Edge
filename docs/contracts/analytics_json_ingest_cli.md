# Analytics JSON Ingest CLI Contract

## Module

Analytics JSON-to-SQLite ingest CLI v1.

This contract defines a local command-line usability layer that reads supported
Mythic Edge parser-normalized replay JSON files, validates them, writes
parser-normalized facts into a caller-specified local SQLite analytics
database, and prints a deterministic summary.

The CLI is not a raw Player.log parser, not a saved-event replay runner, not a
golden-replay adapter, not a runtime sidecar, not a Match Journal bridge, not a
Google Sheets export, and not an AI or coaching layer.

Plain English: this command can load already-structured Mythic Edge analytics
JSON into SQLite. It cannot decide what happened in Arena.

## Source Issue

Issue:

- https://github.com/Tahjali11/Mythic-Edge/issues/205

Tracker:

- https://github.com/Tahjali11/Mythic-Edge/issues/204

Base branch:

```text
main
```

Branch:

```text
codex/analytics-json-ingest-cli
```

## Related Authority

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/problem_representations/local_analytics_foundation.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_migration_loader.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`
- `docs/contracts/analytics_field_evidence_ingest.md`
- `docs/contracts/analytics_derived_sql_views.md`
- `docs/contracts/analytics_replay_view_validation_harness.md`

## Risk Tier

Medium-High.

Reasons:

- The CLI is local-only, but it writes generated SQLite databases from private
  user JSON files.
- It may become the user's first practical path from historical JSON files to
  analytics output, so accepted input shape and failure behavior must be clear.
- It must not accept arbitrary JSON, raw logs, runtime artifacts, workbook
  exports, Match Journal notes, or model-provider output as analytics truth.
- It must not leak full local paths or commit generated databases.

## Owning Layer And Truth Boundary

Primary owning layer: local analytics usability / adapter layer.

The analytics JSON ingest CLI owns:

- command-line argument parsing for analytics JSON ingest
- file and directory input discovery for supported JSON files
- top-level JSON loading and shape validation
- strict acceptance of parser-normalized replay JSON already supported by
  `ingest_parser_normalized_replay(...)`
- opening a caller-specified SQLite database path
- applying existing analytics migrations through the existing ingest API
- invoking existing analytics ingest APIs
- producing deterministic local summary output
- CLI exit-code behavior

The analytics JSON ingest CLI does not own:

- parser event interpretation
- parser state final reconciliation
- parser match identity
- parser game identity
- parser deduplication
- parser-owned row shape
- raw Player.log parsing
- saved-event replay reconstruction
- golden replay comparison behavior
- runtime status artifacts
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- Match Journal behavior
- overlay behavior
- Google Sheets sync/export behavior
- analytics SQL schema or view definitions
- OpenAI/model-provider behavior
- AI coaching or gameplay advice
- hidden-card inference
- archetype classification as inferred fact
- player-mistake labels as facts
- merge readiness or deploy readiness

Truth boundaries:

- Parser/state owns parser-managed match, game, card, gameplay, and final
  reconciliation facts.
- Analytics ingest owns copying parser-normalized facts into local SQLite with
  deterministic IDs and provenance labels.
- The CLI owns only local file-to-ingest orchestration and reporting.
- SQLite analytics tables and views are downstream storage/query surfaces, not
  parser truth, workbook truth, AI truth, merge readiness, deploy readiness, or
  gameplay advice.

## Observed Current Behavior

Current `main` at `61b90fa`:

- Tracker #204 is open for analytics usability and local ingest.
- Issue #205 is open for JSON-to-SQLite analytics ingest CLI.
- `src/mythic_edge_parser/app/analytics_ingest.py` exists and exposes:
  - `ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION`
  - `AnalyticsReplayIngestError`
  - `ParserNormalizedReplayInput`
  - `AnalyticsReplayIngestResult`
  - `normalize_parser_normalized_replay(...)`
  - `deterministic_ingest_run_id(...)`
  - `ingest_parser_normalized_replay(...)`
- `ingest_parser_normalized_replay(...)` accepts parser-normalized replay
  mappings with:
  - `source_kind`
  - `source_artifact_label`
  - `match_log_rows`
  - `game_log_rows`
  - optional `gameplay_action_entries`
  - optional `opponent_card_observations`
  - optional `field_evidence_entries`
  - optional `parser_commit`
  - optional `parser_version`
  - optional `generated_at`
- Allowed replay `source_kind` values are currently:
  - `sanitized_golden_replay`
  - `saved_event_replay`
- `normalize_parser_normalized_replay(...)` rejects unsafe
  `source_artifact_label` values that look like local paths or URLs.
- `ingest_parser_normalized_replay(...)` applies analytics migrations to a
  caller-owned SQLite connection.
- Existing focused tests cover in-memory ingest, idempotency, malformed replay
  failures, unsafe source labels, gameplay action ingest, opponent-card
  observation ingest, field-evidence ingest, derived views, and replay-to-view
  validation.
- No `src/mythic_edge_parser/app/analytics_json_ingest.py` module exists.
- No user-facing analytics JSON ingest CLI exists.
- No tool wrapper exists for JSON-to-SQLite analytics ingest.
- `pyproject.toml` has no analytics ingest console script.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_json_ingest_cli.md`

Future implementation files authorized by this contract:

- `src/mythic_edge_parser/app/analytics_json_ingest.py`
- `tests/test_analytics_json_ingest_cli.py`
- `docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md`

Existing files authorized for narrow additive integration:

- `pyproject.toml`, only if Codex C adds an optional console-script entry
  for the contracted CLI

Existing files Codex C may read but should not change unless a direct, minimal
test import or bug fix is required:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_replay_view_harness.py`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_derived_views.py`

Files and surfaces not owned by this contract:

- parser modules
- parser state
- parser event classes
- saved-event replay behavior
- golden replay behavior
- runtime surface writers
- analytics schema migrations
- analytics derived SQL view definitions
- Match Journal modules
- overlay modules
- Google Sheets sync/export
- workbook schema
- webhook transport
- Apps Script
- OpenAI/model-provider code
- raw user JSON game files
- generated SQLite databases
- raw logs
- runtime artifacts
- failed delivery artifacts
- workbook exports
- secrets, credentials, API keys, tokens, or webhook URLs

If implementation requires analytics schema changes, ingest API semantic
changes, parser behavior, runtime behavior, Match Journal behavior, adapter
support for other JSON shapes, environment-variable contracts, or downstream
integration changes, Codex C must stop and route back to Codex B.

## Public Interface

Future implementation must add:

```text
mythic_edge_parser.app.analytics_json_ingest
```

Required public constants:

```python
ANALYTICS_JSON_INGEST_CLI_SCHEMA_VERSION = "analytics_json_ingest_cli.v1"
ANALYTICS_JSON_INGEST_MAX_BYTES = 10_485_760
SUPPORTED_ANALYTICS_JSON_SHAPES = ("parser_normalized_replay",)
REQUIRED_ANALYTICS_VIEWS = (
    "v_opening_hand_cards",
    "v_opening_lines",
    "v_gameplay_action_review",
    "v_mulligan_outcomes",
    "v_game1_vs_postboard",
    "v_play_draw_splits",
    "v_sample_size_warnings",
    "v_matchup_label_performance",
    "v_opponent_card_observation_review",
)
```

Required public functions:

```python
build_arg_parser() -> argparse.ArgumentParser
main(argv: Sequence[str] | None = None) -> int
```

Recommended helper shapes, public or private at Codex C's discretion:

```python
discover_analytics_json_inputs(inputs: Sequence[Path]) -> tuple[Path, ...]
load_analytics_json_file(path: Path) -> Mapping[str, object]
classify_analytics_json_payload(payload: Mapping[str, object]) -> str
ingest_analytics_json_inputs(...) -> AnalyticsJsonIngestCliResult
```

The CLI must be runnable as a module:

```bash
python3 -m mythic_edge_parser.app.analytics_json_ingest \
  --input path/to/replay.json \
  --database data/analytics/mythic_edge.sqlite3 \
  --print-summary
```

Optional console script:

```text
mythicedge-analytics-ingest-json
```

Codex C may add this console script only if it is a thin wrapper around
`mythic_edge_parser.app.analytics_json_ingest:main`. A separate `tools/`
wrapper is not required in v1 and should not be added unless Codex C finds a
repo-local pattern that makes it clearly smaller than a console script.

### CLI Arguments

Required arguments:

- `--input PATH`
- `--database PATH`

Rules:

- `--input` may be specified multiple times.
- Each input path may be a JSON file or a directory.
- Directory inputs expand to immediate child `*.json` files only, sorted by
  filename. Recursive directory ingest is deferred.
- At least one supported JSON file must be discovered.
- `--database` is required and must name a local SQLite file path. The CLI must
  not default to `data/analytics/mythic_edge.sqlite3`.

Optional arguments:

- `--print-summary`: print deterministic JSON summary to stdout
- `--check-views`: query required derived views after ingest; default should be
  enabled unless Codex C documents a smaller equally safe default
- `--fail-on-warning`: convert warnings to exit code `1`

Forbidden arguments in v1:

- no raw-log or Player.log input option
- no saved-event replay option
- no golden-replay manifest option
- no runtime status input option
- no workbook export input option
- no Match Journal input option
- no OpenAI/model-provider option
- no environment-variable override option
- no delete/reset/drop-database option
- no recursive directory option
- no `--continue-on-error` option

## Inputs

### Supported Shape: Parser-Normalized Replay JSON

The only supported v1 JSON shape is the top-level parser-normalized replay
mapping accepted by `normalize_parser_normalized_replay(...)` and
`ingest_parser_normalized_replay(...)`.

Required top-level fields:

- `source_kind`
- `source_artifact_label`
- `match_log_rows`
- `game_log_rows`

Optional top-level fields:

- `gameplay_action_entries`
- `opponent_card_observations`
- `field_evidence_entries`
- `parser_commit`
- `parser_version`
- `generated_at`

Allowed `source_kind` values are inherited from
`normalize_parser_normalized_replay(...)`:

- `sanitized_golden_replay`
- `saved_event_replay`

Rules:

- The CLI must call the existing replay normalizer or enforce exactly
  equivalent validation before writing to SQLite.
- The CLI must not broaden `source_kind` values.
- `source_artifact_label` must be a safe label, not a local path or URL.
- The CLI must not silently create a `source_artifact_label` from a full local
  path. If a future user flow needs label derivation from basenames, it needs a
  contract update.
- `match_log_rows` and `game_log_rows` must be lists of mappings.
- Optional payload arrays must be lists of mappings when present.

### File And Directory Inputs

Accepted file inputs:

- UTF-8 JSON files with `.json` extension
- top-level JSON object only
- file size at or below `ANALYTICS_JSON_INGEST_MAX_BYTES`

Accepted directory inputs:

- local directories containing supported `.json` files as immediate children
- deterministic lexical order by filename, with duplicate resolved paths
  processed once

Rejected inputs:

- missing paths
- directories with no `.json` files
- `.jsonl` files
- raw `Player.log` text
- raw Arena payload dumps
- top-level JSON arrays
- arbitrary JSON with unrecognized shape
- runtime status files as parser truth
- failed delivery artifacts or retry queues
- workbook exports
- OpenAI/model-provider output
- human Match Journal notes
- generated SQLite database files
- remote URLs

### Explicitly Deferred Adapters

The CLI must reject these shapes in v1 even if they contain useful data:

- full golden replay reports
- golden replay manifests
- reduced parser-owned expected-output JSON such as
  `{"match_log_row": ..., "game_log_rows": ...}`
- saved-event JSONL files
- runtime `active_match_snapshot_latest.json`
- runtime `match_history_latest.json`
- runtime timeline/action/deck/collection JSON artifacts
- workbook export JSON
- Match Journal JSON

These shapes may become adapters later only through a new scoped contract that
proves the mapping is lossless and does not infer missing facts.

## Outputs

### SQLite Output

Allowed output:

- caller-specified local SQLite database file
- adjacent SQLite WAL/SHM/journal files produced by SQLite at runtime

Rules:

- The CLI may create the database parent directory.
- The CLI must not delete, reset, or drop an existing database.
- The CLI must not create a database unless all input files pass CLI-level
  discovery and supported-shape validation.
- The CLI must call `ingest_parser_normalized_replay(...)` for each supported
  replay.
- Re-ingesting the same supported input into the same database must not
  duplicate facts.
- Generated database artifacts must remain local and uncommitted.

### Summary Output

When `--print-summary` is supplied, the CLI must print one deterministic JSON
object to stdout.

Required summary fields:

- `ok`
- `object`
- `schema_version`
- `status`
- `database_label`
- `files_seen`
- `files_supported`
- `files_ingested`
- `files_unsupported`
- `unsupported_files`
- `ingest_runs`
- `row_counts`
- `warnings`
- `skipped`
- `view_readiness`

Required values:

```text
object = "mythic_edge_analytics_json_ingest_summary"
schema_version = "analytics_json_ingest_cli.v1"
```

Rules:

- `database_label` must be a safe basename or redacted label, not a full local
  absolute path.
- File labels in `unsupported_files` and `ingest_runs` must use safe basenames
  or source artifact labels, not full local absolute paths.
- `row_counts` must aggregate table counts from `AnalyticsReplayIngestResult`
  across the final database state after all ingest calls.
- `warnings` must include CLI-level warnings and ingest-result warnings.
- `skipped` must aggregate ingest-result skipped counts.
- `view_readiness` must report each required analytics view as queryable,
  missing, or failed, with row counts for queryable views.
- Summary output must not include raw Player.log payloads, full raw JSON
  payloads, full local paths, secrets, workbook exports, failed delivery
  artifacts, or
  model-provider responses.

### Exit Codes

Required exit codes:

- `0`: all discovered files were supported, ingest completed, and required
  view checks passed
- `1`: validation, unsupported input, ingest, migration, view readiness, or
  warning failure when `--fail-on-warning` is set
- `2`: CLI usage error from argument parsing

Rules:

- Unsupported JSON must not be reported as success.
- If any input file is unsupported or malformed, the command must exit `1`
  and must not write any database rows.
- If all inputs are valid but one ingest call fails, the command must exit `1`
  and must not claim success. Codex C should prefer a transaction or preflight
  strategy that avoids partial multi-file success when feasible.
- `main(...)` should catch known ingest/IO/JSON/migration errors and return an
  exit code rather than dumping a traceback for expected user mistakes.

## Invariants

- The CLI must not parse raw Player.log.
- The CLI must not accept arbitrary JSON as analytics truth.
- The CLI must not infer missing match/game facts.
- The CLI must not change parser-owned row shape.
- The CLI must not mutate parser-owned facts.
- The CLI must not mutate workbook, webhook, Apps Script, Match Journal,
  overlay, Google Sheets, OpenAI, or AI/coaching surfaces.
- The CLI must call existing analytics ingest APIs rather than writing fact
  tables directly.
- The CLI must not create or commit user JSON files.
- The CLI must not create or commit generated SQLite artifacts.
- The CLI must not print full local absolute paths by default.
- The CLI must keep SQLite analytics output downstream of parser-normalized
  facts.

## Error Behavior

Input discovery errors:

- missing input path: exit `1`
- directory with no candidate JSON files: exit `1`
- no supported files after discovery: exit `1`
- duplicate resolved input files: process once and record a warning

JSON loading errors:

- unreadable file: exit `1`
- file too large: exit `1`
- invalid UTF-8: exit `1`
- invalid JSON: exit `1`
- top-level non-object JSON: exit `1`

Shape errors:

- unsupported JSON shape: exit `1`
- unsupported `source_kind`: exit `1`
- unsafe `source_artifact_label`: exit `1`
- malformed replay rows: exit `1`

Database errors:

- database path points to a directory: exit `1`
- parent directory cannot be created: exit `1`
- SQLite open, migration, or ingest failure: exit `1`

Error messages:

- must be concise and actionable
- must identify files by safe basename or sanitized label only
- must not echo raw payloads, full local paths, secrets, tokens, API keys,
  webhook URLs, workbook IDs, or raw Player.log excerpts

## Side Effects

Allowed side effects:

- read caller-specified local JSON files
- create the caller-specified database parent directory
- create or update the caller-specified local SQLite database
- create SQLite-managed adjacent WAL/SHM/journal files at runtime
- print a deterministic summary to stdout when requested
- print concise errors to stderr
- create temporary files/databases in tests under `tmp_path`
- implementation handoff documentation

Forbidden side effects:

- reading raw Player.log files
- parsing saved-event JSONL files
- reading runtime status files as parser truth
- reading failed delivery artifacts or workbook exports
- writing runtime status files
- writing failed delivery artifacts
- writing workbook exports
- posting webhooks
- calling Apps Script
- writing Google Sheets
- changing Match Journal data
- changing overlay state
- calling OpenAI/model providers
- creating GitHub issues, PRs, comments, or tracker updates from CLI code
- committing user JSON, generated SQLite databases, WAL/SHM/journal files,
  raw logs, generated data, runtime artifacts, failed delivery artifacts, workbook exports,
  secrets, credentials, API keys, tokens, or webhook URLs

## Dependency Order

Codex C should implement in this order:

1. Add `src/mythic_edge_parser/app/analytics_json_ingest.py` with constants,
   argument parser, safe file discovery, JSON loading, shape classification,
   summary helpers, and `main(...)`.
2. Add focused tests for file ingest into a temporary SQLite database.
3. Add focused tests for directory ingest of multiple parser-normalized replay
   JSON files.
4. Add strict failure tests for unsupported shapes and unsafe labels with no
   database row writes.
5. Add idempotency and view-readiness tests.
6. Add optional console-script entry only if Codex C selects it.
7. Add implementation handoff.
8. Run focused validation and protected-surface checks.

## Compatibility

The CLI must remain compatible with:

- `analytics_local_sqlite_schema.v1`
- `analytics_parser_normalized_replay_ingest.v1`
- existing analytics migration loader behavior
- existing analytics derived view names
- existing parser-normalized replay input shape
- Python module execution via `python3 -m mythic_edge_parser.app.analytics_json_ingest`

The CLI must not require:

- a new schema migration
- a default database path
- a new environment variable
- raw Player.log access
- live parser runtime state
- status API state
- Match Journal input
- overlay/cockpit input
- Google Sheets sync/export
- OpenAI/model-provider access

Deferred compatibility:

- recursive directory ingest is deferred
- golden replay report or manifest adapters are deferred
- saved-event JSONL replay-to-analytics adapters are deferred
- runtime status/match-history/active-match artifact adapters are deferred
- workbook export adapters are deferred
- Match Journal annotation adapters are deferred
- console-script alias is optional

## Tests Required

Codex C must add focused tests in:

```text
tests/test_analytics_json_ingest_cli.py
```

Required test behaviors:

- CLI version/schema constants are public.
- `build_arg_parser()` accepts the contracted arguments.
- `main(...)` returns `2` for argparse usage errors.
- Single parser-normalized replay JSON file ingests into a temporary SQLite
  database.
- Directory input ingests multiple supported JSON files in deterministic order.
- Multiple `--input` values are supported.
- Duplicate resolved input files are processed once and reported as a warning.
- Re-running the CLI with the same input and database does not duplicate facts.
- Unsupported JSON shape exits `1` and creates no database rows.
- Raw-looking `.jsonl` or Player.log-style inputs are rejected.
- Unsafe `source_artifact_label` exits `1` and creates no database rows.
- Invalid JSON exits `1` with a safe message.
- Top-level JSON arrays are rejected.
- Oversize files are rejected without loading the full payload into summary
  output.
- The CLI refuses to proceed when any discovered file is unsupported.
- Summary output includes files seen, ingested count, unsupported count, row
  counts, warnings, skipped counts, and view-readiness.
- Summary output avoids full local absolute paths.
- View readiness checks query all required analytics views.
- Generated SQLite files are created only under `tmp_path` or caller-specified
  local paths during tests.
- No user JSON, generated SQLite artifact, raw log, runtime artifact, failed
  post, workbook export, secret, token, or webhook URL is added to the repo.

Validation commands:

```bash
python3 -m pytest -q tests/test_analytics_json_ingest_cli.py
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py
python3 -m pytest -q tests/test_analytics_replay_view_harness.py
python3 -m pytest -q tests/test_analytics_schema.py
python3 -m pytest -q tests/test_analytics_derived_views.py
python3 -m ruff check src tests tools
git diff --check
```

Generated artifact scan:

```bash
find . -path './.git' -prune -o \
  \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' \
     -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \
     -o -name '*.sqlite-journal' \) -print
```

Protected checks for Codex C/E/F:

```bash
printf '%s\n' \
  docs/contracts/analytics_json_ingest_cli.md \
  src/mythic_edge_parser/app/analytics_json_ingest.py \
  tests/test_analytics_json_ingest_cli.py \
  docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin

printf '%s\n' \
  docs/contracts/analytics_json_ingest_cli.md \
  src/mythic_edge_parser/app/analytics_json_ingest.py \
  tests/test_analytics_json_ingest_cli.py \
  docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

If Codex C adds a console script, include `pyproject.toml` in the path-scoped
checks.

## Acceptance Criteria

The contract is implementation-ready when:

- The owning layer is named as local analytics usability / adapter layer.
- The only supported v1 input shape is parser-normalized replay JSON.
- Other JSON artifact adapters are explicitly deferred.
- The module CLI, required arguments, output summary, exit codes, and error
  behavior are defined.
- The database output path is caller-specified and not environment-driven.
- The CLI is required to call existing analytics ingest APIs.
- Strict preflight prevents unsupported files from being reported as success.
- Tests and protected-surface checks are named.
- The next role is Codex C.

Implementation is acceptable only if:

- It changes only the CLI module, focused tests, optional console-script entry,
  and handoff docs.
- It does not change analytics schema, derived views, existing ingest API
  semantics, parser behavior, runtime behavior, workbook/webhook/App Script
  behavior, Match Journal behavior, overlay behavior, Google Sheets behavior,
  OpenAI/model-provider behavior, or AI/coaching behavior.
- It does not create or commit user JSON files or generated SQLite artifacts.
- It does not parse raw Player.log or infer missing facts.
- It does not make analytics CLI summaries parser truth, workbook truth,
  analytics truth, merge readiness, deploy readiness, gameplay advice,
  hidden-card inference, archetype classification, player-mistake labels, or
  AI coaching.

## Open Questions And Contract Risks

- The user's roughly 50 game JSON files may not yet match the contracted
  parser-normalized replay shape. If they are golden replay reports, runtime
  match-history snapshots, or another Mythic Edge artifact shape, a follow-up
  adapter contract is required.
- The contract deliberately forbids path-derived `source_artifact_label`
  generation in v1. That keeps privacy tight, but it may require the user's
  files to include safe labels before ingest.
- The preferred no-partial-multi-file behavior may require a preflight pass
  that normalizes every input before opening or writing the target database.
- A console-script alias is optional. Module execution is the stable required
  interface.

## Codex C Handoff Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #205, Analytics JSON-to-SQLite ingest CLI.

  Context:
  - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
  - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/205
  - Branch: codex/analytics-json-ingest-cli
  - Base: main
  - Contract: docs/contracts/analytics_json_ingest_cli.md
  - Expected handoff artifact: docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md

  Goal:
  Compare current main against the analytics JSON ingest CLI contract. Implement only the smallest local CLI and focused tests needed to satisfy the contract.

  Read first:
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - docs/codex_module_workflow.md
  - docs/agent_threads/implementation.md
  - docs/contracts/analytics_json_ingest_cli.md
  - docs/contracts/analytics_local_sqlite_schema.md
  - docs/contracts/analytics_parser_normalized_replay_ingest.md
  - docs/contracts/analytics_derived_sql_views.md
  - docs/contracts/analytics_replay_view_validation_harness.md
  - src/mythic_edge_parser/app/analytics_ingest.py
  - src/mythic_edge_parser/app/analytics_migration_loader.py
  - src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
  - tests/test_analytics_parser_normalized_replay_ingest.py
  - tests/test_analytics_replay_view_harness.py
  - tests/test_analytics_schema.py
  - tests/test_analytics_derived_views.py
  - pyproject.toml

  Implement:
  - src/mythic_edge_parser/app/analytics_json_ingest.py
  - tests/test_analytics_json_ingest_cli.py
  - optional pyproject.toml console-script entry only if selected
  - docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md

  Required behavior:
  - Support python3 -m mythic_edge_parser.app.analytics_json_ingest --input PATH --database PATH --print-summary.
  - Accept only parser-normalized replay JSON accepted by ingest_parser_normalized_replay(...).
  - Support file inputs, repeated --input values, and non-recursive directory inputs containing *.json files.
  - Require caller-specified --database; do not add a default database path or environment-variable contract.
  - Preflight all discovered JSON before writing database rows.
  - Call existing analytics ingest APIs rather than writing fact tables directly.
  - Print deterministic JSON summary with file counts, row counts, warnings, skipped counts, and view readiness.
  - Keep full local paths and private payloads out of summary and error output.
  - Return contracted exit codes.

  Do not:
  - Open a PR or commit unless explicitly asked.
  - Continue or close paused Match Journal/status API work.
  - Change analytics schema, derived views, existing ingest API semantics, parser behavior, runtime behavior, workbook/webhook/App Script behavior, Match Journal behavior, overlay behavior, Google Sheets behavior, OpenAI/model-provider behavior, or AI/coaching behavior.
  - Commit user JSON game files, generated SQLite databases, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed delivery artifacts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs.
  - Parse raw Player.log or saved-event JSONL.
  - Add adapters for golden replay reports, manifests, runtime status/match-history artifacts, workbook exports, Match Journal notes, or arbitrary JSON.
  - Infer missing facts, hidden cards, decklists, archetypes, player mistakes, gameplay advice, or coaching.

  Validation:
  - python3 -m pytest -q tests/test_analytics_json_ingest_cli.py
  - python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py
  - python3 -m pytest -q tests/test_analytics_replay_view_harness.py
  - python3 -m pytest -q tests/test_analytics_schema.py
  - python3 -m pytest -q tests/test_analytics_derived_views.py
  - python3 -m ruff check src tests tools
  - git diff --check
  - Run generated SQLite artifact scan.
  - Run path-scoped secret/private marker and protected-surface checks for changed files.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/205"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/analytics_json_ingest_cli.md"
  target_artifact: "docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md"
  verdict: "contract_ready_for_module_implementer"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/analytics-json-ingest-cli"
  validation:
    - "documentation-only contract writer pass"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_json_ingest_cli.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_replay_view_harness.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_schema.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_derived_views.py"
    - "Codex C should run python3 -m ruff check src tests tools"
    - "Codex C should run git diff --check"
    - "Codex C should run generated SQLite artifact scan"
    - "Codex C should run path-scoped secret/private marker and protected-surface checks"
  stop_conditions:
    - "Do not continue or close paused Match Journal/status API work unless explicitly instructed."
    - "Do not change analytics schema, derived views, existing ingest API semantics, parser/runtime/workbook/webhook/App Script/Match Journal/overlay/Sheets/OpenAI/AI/coaching behavior."
    - "Do not commit user JSON game files or generated SQLite artifacts."
    - "Do not parse raw Player.log or saved-event JSONL in this module."
    - "Do not add adapters for uncontracted JSON shapes."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/205"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/analytics_json_ingest_cli.md"
  target_artifact: "docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md"
  verdict: "contract_ready_for_module_implementer"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/analytics-json-ingest-cli"
  validation:
    - "documentation-only contract writer pass"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_json_ingest_cli.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_replay_view_harness.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_schema.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_derived_views.py"
    - "Codex C should run python3 -m ruff check src tests tools"
    - "Codex C should run git diff --check"
    - "Codex C should run generated SQLite artifact scan"
    - "Codex C should run path-scoped secret/private marker and protected-surface checks"
  stop_conditions:
    - "Do not continue or close paused Match Journal/status API work unless explicitly instructed."
    - "Do not change analytics schema, derived views, existing ingest API semantics, parser/runtime/workbook/webhook/App Script/Match Journal/overlay/Sheets/OpenAI/AI/coaching behavior."
    - "Do not commit user JSON game files or generated SQLite artifacts."
    - "Do not parse raw Player.log or saved-event JSONL in this module."
    - "Do not add adapters for uncontracted JSON shapes."
```
