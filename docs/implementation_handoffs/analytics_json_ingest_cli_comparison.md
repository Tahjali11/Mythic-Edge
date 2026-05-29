# Analytics JSON Ingest CLI Implementation Comparison

## Summary

Codex C compared current `main` against
`docs/contracts/analytics_json_ingest_cli.md` for issue #205 and implemented
the smallest local module CLI needed to load supported parser-normalized
replay JSON into a caller-specified SQLite analytics database.

The implementation adds a `python -m` module entrypoint over the existing
analytics ingest API. It does not change analytics schema migrations, derived
views, existing ingest API semantics, parser behavior, runtime behavior,
workbook/webhook/App Script behavior, Match Journal behavior, overlay
behavior, Google Sheets behavior, OpenAI/model-provider behavior, or
AI/coaching behavior.

## Findings First

- No blocking contract mismatches remain in the implemented #205 scope.
- No analytics schema, view, or ingest API changes were needed.
- No console script was added; the contracted module CLI is sufficient for v1.
- The CLI preflights all discovered JSON files before opening or writing the
  caller database, so unsupported or malformed inputs do not create database
  rows.

## Confirmed Matches

- `ANALYTICS_JSON_INGEST_CLI_SCHEMA_VERSION` is present with value
  `analytics_json_ingest_cli.v1`.
- `ANALYTICS_JSON_INGEST_MAX_BYTES` is present with value `10_485_760`.
- `SUPPORTED_ANALYTICS_JSON_SHAPES` is present with only
  `parser_normalized_replay`.
- `REQUIRED_ANALYTICS_VIEWS` names the nine contracted derived views.
- `build_arg_parser()` and `main(argv=None)` are public.
- The module runs via
  `python3 -m mythic_edge_parser.app.analytics_json_ingest` when the package is
  on `PYTHONPATH` or installed.
- CLI arguments support repeated `--input`, required `--database`,
  `--print-summary`, enabled-by-default `--check-views`, `--no-check-views`,
  and `--fail-on-warning`.
- Directory inputs expand only immediate `*.json` children in deterministic
  lexical order.
- Duplicate resolved inputs are processed once and reported as safe warnings.
- The only accepted shape is a top-level parser-normalized replay mapping that
  passes `normalize_parser_normalized_replay(...)`.
- Ingest calls use `ingest_parser_normalized_replay(...)`; the CLI does not
  write fact tables directly.
- The database path is caller-specified; there is no default database path or
  environment-variable contract.
- Deterministic JSON summaries include safe file/database labels, file counts,
  ingest run metadata, row counts, warnings, skipped counts, unsupported files,
  and view readiness.
- Full local paths and private payloads are kept out of summary and expected
  error output.
- Exit codes match the contract:
  - `0` for successful ingest/view checks without warning failure
  - `1` for expected validation, unsupported-input, warning, database, ingest,
    or view-readiness failures
  - `2` for argparse usage errors

## Changes Made

- Added `src/mythic_edge_parser/app/analytics_json_ingest.py`.
- Added `tests/test_analytics_json_ingest_cli.py`.
- Added this handoff:
  `docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md`.

## Tests Added

`tests/test_analytics_json_ingest_cli.py` covers:

- public constants and argument parser shape
- argparse usage error exit code
- single parser-normalized replay file ingest into temporary SQLite
- deterministic summary output and required view readiness
- directory ingest of multiple JSON files in lexical order
- repeated `--input` values and duplicate-input warning
- idempotent re-ingest into the same database
- unsupported JSON shape failure with no database creation
- unsafe `source_artifact_label` failure with no database creation
- invalid JSON and top-level array rejection
- oversize file rejection without echoing payload
- `.jsonl` and Player.log-style input rejection
- database-path-is-directory rejection
- `--fail-on-warning` converting duplicate warnings to exit code `1`
- `--no-check-views` marking required views as `not_checked`

## Contract Mismatches Fixed Or Still Open

Fixed:

- The analytics JSON ingest CLI was missing; it now exists.
- Focused CLI tests were missing; they now exist.

Still open:

- None in the #205 implementation scope.

Deferred by contract:

- Raw Player.log parsing.
- Saved-event JSONL adapters.
- Golden replay report/manifest adapters.
- Runtime status, match-history, workbook export, Match Journal, arbitrary
  JSON, OpenAI/model-provider, AI/coaching, and external website adapters.
- Recursive directory ingest.
- Console-script alias.

## Validation Run

- `python3 -m pytest -q tests/test_analytics_json_ingest_cli.py`
  - Passed: 13 tests.
- `python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py`
  - Passed: 24 tests.
- `python3 -m pytest -q tests/test_analytics_replay_view_harness.py`
  - Passed: 2 tests.
- `python3 -m pytest -q tests/test_analytics_schema.py`
  - Passed: 12 tests.
- `python3 -m pytest -q tests/test_analytics_derived_views.py`
  - Passed: 8 tests.
- `python3 -m ruff check src tests tools`
  - Passed.
- `git diff --check`
  - Passed.
- Module help smoke check:
  - `PYTHONPATH=src python3 -m mythic_edge_parser.app.analytics_json_ingest --help`
  - Passed. The plain source checkout is not installed, so `PYTHONPATH=src` is
    needed for a direct module smoke check from the repo root.
- Generated SQLite artifact scan:
  - Command:
    `find . -path './.git' -prune -o \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name '*.sqlite-journal' \) -print`
  - Passed: no matching artifacts printed.
- Path-scoped secret/private marker scan:
  - Command:
    `printf '%s\n' docs/contracts/analytics_json_ingest_cli.md src/mythic_edge_parser/app/analytics_json_ingest.py tests/test_analytics_json_ingest_cli.py docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
  - Passed: scanned 4 paths, forbidden 0, warnings 0.
- Path-scoped protected-surface gate:
  - Command:
    `printf '%s\n' docs/contracts/analytics_json_ingest_cli.md src/mythic_edge_parser/app/analytics_json_ingest.py tests/test_analytics_json_ingest_cli.py docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
  - Passed: changed paths 4, forbidden 0, warnings 0.
- No-index whitespace checks for untracked files:
  - Ran `git diff --no-index --check /dev/null <path>` for the contract,
    CLI module, focused tests, and handoff.
  - Exit code was 1 as expected for file differences against `/dev/null`;
    no whitespace-error output was produced.

## Remaining Risks And Unverified Layers

- The CLI is tested against synthetic parser-normalized replay JSON and
  temporary SQLite databases. It has not been run against the user's private
  historical JSON files, and those files were not read or committed.
- The CLI does not add adapters for other Mythic Edge JSON artifact shapes.
  That is intentional for #205.
- The CLI summary is a local usability report only. It is not parser truth,
  analytics truth, workbook truth, merge readiness, deploy readiness,
  gameplay advice, hidden-card inference, archetype classification,
  player-mistake truth, or AI coaching.
- Generated SQLite databases remain local caller artifacts and must not be
  committed.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #205, Analytics JSON-to-SQLite ingest CLI.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/205
- Branch: codex/analytics-json-ingest-cli
- Base: main
- Source contract: docs/contracts/analytics_json_ingest_cli.md
- Implementation handoff: docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md
- Implemented files:
  - src/mythic_edge_parser/app/analytics_json_ingest.py
  - tests/test_analytics_json_ingest_cli.py

Goal:
Review the #205 implementation against the analytics JSON ingest CLI contract.
Focus on accepted input shape, preflight-before-write behavior, database path
handling, deterministic summary output, safe error output, exit codes, view
readiness, tests, and whether any analytics schema/view/ingest API,
parser/runtime/workbook/webhook/App Script/Match Journal/overlay/Sheets/AI
surface changed unexpectedly.

Do:
- Read the contract and handoff first.
- Review src/mythic_edge_parser/app/analytics_json_ingest.py.
- Review tests/test_analytics_json_ingest_cli.py.
- Confirm no analytics schema migrations, derived SQL views, existing ingest
  API semantics, parser behavior, runtime behavior, workbook/webhook/App Script
  behavior, Match Journal behavior, overlay behavior, Google Sheets behavior,
  OpenAI/model-provider behavior, or AI/coaching behavior changed.
- Confirm the CLI accepts only parser-normalized replay JSON accepted by
  ingest_parser_normalized_replay(...).
- Confirm unsupported/malformed files fail preflight before database writes.
- Confirm summaries and errors avoid full local paths and private payloads.
- Run or verify:
  - python3 -m pytest -q tests/test_analytics_json_ingest_cli.py
  - python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py
  - python3 -m pytest -q tests/test_analytics_replay_view_harness.py
  - python3 -m pytest -q tests/test_analytics_schema.py
  - python3 -m pytest -q tests/test_analytics_derived_views.py
  - python3 -m ruff check src tests tools
  - git diff --check
  - generated SQLite artifact scan
  - path-scoped secret/private marker and protected-surface checks
- Produce review findings first, then validation evidence, residual risks, and
  next recommended role.

Do not:
- Open a PR or commit unless explicitly asked.
- Continue or close paused Match Journal/status API work.
- Change analytics schema, derived views, existing ingest API semantics,
  parser behavior, runtime behavior, workbook/webhook/App Script behavior,
  Match Journal behavior, overlay behavior, Google Sheets behavior,
  OpenAI/model-provider behavior, or AI/coaching behavior.
- Commit user JSON game files, generated SQLite databases, WAL, SHM, journal
  files, raw logs, generated data, runtime artifacts, failed delivery
  artifacts, workbook exports, secrets, credentials, API keys, tokens, or
  webhook URLs.
- Parse raw Player.log or saved-event JSONL.
- Add adapters for uncontracted JSON shapes.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/205"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_json_ingest_cli.md"
  target_artifact: "docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md"
  verdict: "implementation_ready_for_module_review"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/analytics-json-ingest-cli"
  validation:
    - "python3 -m pytest -q tests/test_analytics_json_ingest_cli.py"
    - "python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py"
    - "python3 -m pytest -q tests/test_analytics_replay_view_harness.py"
    - "python3 -m pytest -q tests/test_analytics_schema.py"
    - "python3 -m pytest -q tests/test_analytics_derived_views.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "generated SQLite artifact scan passed"
    - "path-scoped secret/private marker scan passed"
    - "path-scoped protected-surface gate passed"
  stop_conditions:
    - "Do not continue or close paused Match Journal/status API work unless explicitly instructed."
    - "Do not change analytics schema, derived views, existing ingest API semantics, parser/runtime/workbook/webhook/App Script/Match Journal/overlay/Sheets/OpenAI/AI/coaching behavior."
    - "Do not commit user JSON game files or generated SQLite artifacts."
    - "Do not parse raw Player.log or saved-event JSONL in this module."
    - "Do not add adapters for uncontracted JSON shapes."
```
