# Analytics JSON Ingest CLI Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/205

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Contract

- `docs/contracts/analytics_json_ingest_cli.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch:

```text
codex/analytics-json-ingest-cli
```

Base:

```text
main
```

Changed-file scope reviewed:

- `docs/contracts/analytics_json_ingest_cli.md`
- `docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md`
- `src/mythic_edge_parser/app/analytics_json_ingest.py`
- `tests/test_analytics_json_ingest_cli.py`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Findings First

No blocking findings.

The implementation satisfies the #205 analytics JSON ingest CLI contract in
the reviewed scope. It accepts only parser-normalized replay JSON through the
existing analytics ingest API, preflights supported shape before opening or
writing SQLite output, keeps summaries/errors path-safe, and does not change
parser/runtime/workbook/webhook/App Script/Match Journal/overlay/Sheets/AI
surfaces.

## Contract Summary

The #205 CLI must provide a local `python -m
mythic_edge_parser.app.analytics_json_ingest` usability layer that reads
supported parser-normalized replay JSON files or non-recursive folders, writes
to a caller-specified SQLite analytics database through existing ingest APIs,
and prints deterministic summary output. It must reject unsupported or unsafe
input shapes without treating arbitrary JSON, raw logs, runtime artifacts,
workbook exports, Match Journal notes, or model-provider output as analytics
truth.

## Checks Run

```bash
git status --short --branch
git fetch --prune
gh issue view 205 --repo Tahjali11/Mythic-Edge --json number,title,state,body,labels,comments
python3 -m pytest -q tests/test_analytics_json_ingest_cli.py
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py
python3 -m pytest -q tests/test_analytics_replay_view_harness.py
python3 -m pytest -q tests/test_analytics_schema.py
python3 -m pytest -q tests/test_analytics_derived_views.py
python3 -m ruff check src tests tools
git diff --check
PYTHONPATH=src python3 -m mythic_edge_parser.app.analytics_json_ingest --help
find . -path './.git' -prune -o \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name '*.sqlite-journal' \) -print
printf '%s\n' docs/contracts/analytics_json_ingest_cli.md src/mythic_edge_parser/app/analytics_json_ingest.py tests/test_analytics_json_ingest_cli.py docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/analytics_json_ingest_cli.md src/mythic_edge_parser/app/analytics_json_ingest.py tests/test_analytics_json_ingest_cli.py docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --cached --name-only
for f in docs/contracts/analytics_json_ingest_cli.md src/mythic_edge_parser/app/analytics_json_ingest.py tests/test_analytics_json_ingest_cli.py docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md; do git diff --no-index --check /dev/null "$f" || rc=$?; done; exit 0
python3 -m pytest -q
```

## Results

- Issue #205 is open and matches the contract scope.
- `python3 -m pytest -q tests/test_analytics_json_ingest_cli.py` passed:
  13 passed.
- `python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py`
  passed: 24 passed.
- `python3 -m pytest -q tests/test_analytics_replay_view_harness.py` passed:
  2 passed.
- `python3 -m pytest -q tests/test_analytics_schema.py` passed:
  12 passed.
- `python3 -m pytest -q tests/test_analytics_derived_views.py` passed:
  8 passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed with no output.
- Module help smoke check passed with `PYTHONPATH=src`.
- Generated SQLite artifact scan printed no matching artifacts.
- Path-scoped secret/private marker scan passed: scanned 4 paths, forbidden 0,
  warnings 0.
- Path-scoped protected-surface gate passed: changed paths 4, forbidden 0,
  warnings 0.
- `git diff --cached --name-only` printed no staged files.
- No-index whitespace checks for the four untracked #205 files passed with no
  whitespace-error output after rerunning with a non-`path` loop variable.
- `python3 -m pytest -q` passed: 1425 passed.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | none | `not_reproduced` | No blocking findings in the initial Codex E review. | not_blocking | N/A | Focused validation, full pytest, ruff, whitespace checks, path-scoped secret/private marker scan, protected-surface gate, module help smoke check, and generated artifact scan all passed. | F |

## Confirmed Contract Matches

- Required constants are present with contracted values:
  `ANALYTICS_JSON_INGEST_CLI_SCHEMA_VERSION`,
  `ANALYTICS_JSON_INGEST_MAX_BYTES`,
  `SUPPORTED_ANALYTICS_JSON_SHAPES`, and `REQUIRED_ANALYTICS_VIEWS`.
- Public `build_arg_parser()` and `main(argv=None)` are present.
- The module is runnable through
  `python3 -m mythic_edge_parser.app.analytics_json_ingest` when the source
  package is importable.
- CLI arguments support repeated `--input`, required `--database`,
  `--print-summary`, default-enabled view checks through
  `--check-views` / `--no-check-views`, and `--fail-on-warning`.
- Directory input is non-recursive and sorted by immediate `*.json` child
  filename.
- Duplicate resolved inputs are processed once and reported as warnings.
- The only accepted input shape is parser-normalized replay JSON accepted by
  `normalize_parser_normalized_replay(...)`.
- Ingest uses `ingest_parser_normalized_replay(...)` rather than direct fact
  table writes.
- Unsupported shapes, unsafe labels, invalid JSON, top-level arrays, oversize
  files, `.jsonl`, and Player.log-style inputs fail without creating a
  database in the covered tests.
- Successful summaries include required schema/object fields, counts,
  warnings, skipped counts, ingest runs, row counts, and view readiness.
- Summary and expected error paths use safe basenames instead of full local
  absolute paths in the covered tests.
- Re-ingesting the same supported input into the same database remains
  idempotent.
- No console script, tools wrapper, raw-log adapter, saved-event JSONL adapter,
  golden-replay adapter, runtime artifact adapter, workbook adapter, Match
  Journal adapter, or OpenAI/model-provider integration was added.
- No analytics schema migration, derived view definition, existing ingest API
  semantic, parser, runtime, workbook, webhook, Apps Script, Match Journal,
  overlay, Google Sheets, OpenAI/model-provider, or AI/coaching behavior drift
  was found in the reviewed scope.

## Contract Mismatches

None.

## Missing Tests

None blocking.

Focused tests cover the contract-required parser-normalized file ingest,
directory ingest, duplicate handling, idempotency, unsupported-shape failure,
unsafe-label failure, invalid JSON, top-level arrays, oversize files, raw-looking
input rejection, database path directory rejection, warning exit behavior, and
view-check opt-out behavior.

## Drift Notes

- Repo drift: none found beyond the intended four-file #205 scope plus this
  contract-test report.
- Workbook drift: none found.
- Deployment drift: none found.
- Local-data drift: none found; no generated SQLite database artifacts were
  printed by the artifact scan.
- Issue lifecycle drift: none found; issue #205 is open.
- PR lifecycle drift: no PR was reviewed in this Codex E pass.
- Tracker drift: none found; tracker #204 is referenced by the issue and
  handoff.

## Remaining Risks And Unverified Layers

- The CLI was validated with synthetic parser-normalized replay JSON and
  temporary SQLite databases. It was not run against the user's private
  historical JSON files, and those files were not read or committed.
- If the user's roughly 50 JSON files are golden replay reports, runtime
  snapshots, workbook exports, or another uncontracted artifact shape, a
  follow-up adapter contract is required before ingest.
- The CLI summary is local usability output only. It is not parser truth,
  analytics truth, workbook truth, merge readiness, deploy readiness, gameplay
  advice, hidden-card inference, archetype classification, player-mistake truth,
  or AI coaching.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #205, Analytics JSON-to-SQLite ingest CLI.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/205
- Branch: codex/analytics-json-ingest-cli
- Base: main
- Contract: docs/contracts/analytics_json_ingest_cli.md
- Implementation handoff: docs/implementation_handoffs/analytics_json_ingest_cli_comparison.md
- Contract-test report: docs/contract_test_reports/analytics_json_ingest_cli.md

Codex E verdict:
- No blocking findings.
- Focused validation, full pytest, ruff, generated-artifact scan, path-scoped secret/private marker scan, and protected-surface gate passed.
- No analytics schema/view/ingest API, parser/runtime/workbook/webhook/App Script/Match Journal/overlay/Sheets/OpenAI/AI/coaching drift was found.

Goal:
Prepare the reviewed #205 package for submitter custody without merging or closing the issue.

Do:
- Inspect git status and stage only the reviewed #205 files plus the contract-test report.
- Preserve base branch main and branch codex/analytics-json-ingest-cli.
- Re-run submitter preflight validation as needed:
  - python3 -m pytest -q tests/test_analytics_json_ingest_cli.py
  - python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py
  - python3 -m pytest -q tests/test_analytics_replay_view_harness.py
  - python3 -m pytest -q tests/test_analytics_schema.py
  - python3 -m pytest -q tests/test_analytics_derived_views.py
  - python3 -m ruff check src tests tools
  - git diff --check
  - generated SQLite artifact scan
  - path-scoped secret/private marker and protected-surface checks

Do not:
- Merge or close issue #205 unless an approved deployer workflow explicitly authorizes it.
- Change analytics schema, derived views, existing ingest API semantics, parser behavior, runtime behavior, workbook/webhook/App Script behavior, Match Journal behavior, overlay behavior, Google Sheets behavior, OpenAI/model-provider behavior, or AI/coaching behavior.
- Commit user JSON game files, generated SQLite databases, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed delivery artifacts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs.
- Parse raw Player.log or saved-event JSONL.
- Add adapters for uncontracted JSON shapes.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/205"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/analytics_json_ingest_cli.md"
  target_artifact: "docs/contract_test_reports/analytics_json_ingest_cli.md"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/analytics-json-ingest-cli"
  validation:
    - "python3 -m pytest -q tests/test_analytics_json_ingest_cli.py -> 13 passed"
    - "python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py -> 24 passed"
    - "python3 -m pytest -q tests/test_analytics_replay_view_harness.py -> 2 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py -> 12 passed"
    - "python3 -m pytest -q tests/test_analytics_derived_views.py -> 8 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with no output"
    - "module help smoke check -> passed"
    - "generated SQLite artifact scan -> no output"
    - "path-scoped secret/private marker scan -> passed, scanned 4 paths, forbidden 0, warnings 0"
    - "path-scoped protected-surface gate -> passed, changed paths 4, forbidden 0, warnings 0"
    - "git diff --cached --name-only -> no staged files"
    - "python3 -m pytest -q -> 1425 passed"
  stop_conditions:
    - "Do not merge or close issue #205 unless an approved deployer workflow explicitly authorizes it."
    - "Do not change analytics schema, derived views, existing ingest API semantics, parser/runtime/workbook/webhook/App Script/Match Journal/overlay/Sheets/OpenAI/AI/coaching behavior."
    - "Do not commit user JSON game files or generated SQLite artifacts."
    - "Do not parse raw Player.log or saved-event JSONL in this module."
    - "Do not add adapters for uncontracted JSON shapes."
```
