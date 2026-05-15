# Code Hardening Parser Event Schema Snapshots Contract-Test Report

## Findings

No blocking findings.

### Non-Blocking Submitter Scope Note: Exclude Unrelated Untracked Docs

`docs/project_roadmap.md` and `docs/python_tooling_inventory.md` are present as
untracked files in the working tree, but they are not part of issue #60 and
were already called out as unrelated by Codex C. They should not be staged for
the issue #60 PR unless separately authorized through another issue/contract.

Review impact:

- This does not block the issue #60 snapshot package.
- This is not a parser behavior issue.
- This is not a protected runtime/workbook/App Script surface change.
- It is a submitter-scope risk only.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/60

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

`docs/contracts/code_hardening_parser_event_schema_snapshots.md`

## Implementation Under Test

Branch: `codex/code-hardening-suite`

Implementation handoff:

- `docs/implementation_handoffs/code_hardening_parser_event_schema_snapshots_comparison.md`

Files reviewed for issue #60:

- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/implementation_handoffs/code_hardening_parser_event_schema_snapshots_comparison.md`
- `docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/apps_script_repo_parity.json`
- `tests/fixtures/schema_snapshots/parser_event_classes.json`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `tests/fixtures/schema_snapshots/runtime_export_row_keys.json`
- `tests/fixtures/schema_snapshots/sheet_schema_surfaces.json`
- `tests/fixtures/schema_snapshots/workbook_row_keys.json`

Runtime/source surfaces inspected:

- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `tools/google_apps_script/Code.gs`

## Contract Summary

Issue #60 is a test-only Code Hardening rollout. The snapshot suite should make
accidental schema drift visible for parser event classes, parser payload
top-level key sets, workbook-facing row keys, sync fields, runtime row families,
runtime export row keys, and repo-side Apps Script parity.

The contract requires snapshots to remain deterministic and schema-level. They
must exclude volatile/private/generated values such as raw logs, raw bytes,
hashes, timestamps as values, local paths, secrets, webhook URLs, generated
card/tier data, runtime status files, failed posts, workbook exports, live
workbook state, and deployed Apps Script state.

Snapshot updates must be explicit and reviewed. The tests must not authorize
parser behavior changes, parser state final reconciliation changes, workbook
schema changes, webhook payload changes, Apps Script behavior changes, parser
event class changes, event kind changes, parser payload shape changes,
match/game identity changes, deduplication changes, or tracker #33 closure.

## Checks Run

```powershell
git fetch --prune origin main codex/code-hardening-suite
git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_events.py tests\test_app_models.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_app_outputs.py
py -m pytest -q tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py tests\test_gre_game_result_parser.py tests\test_match_state_parser.py tests\test_parser_small_modules.py tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_parser_regressions.py
py -m ruff check src tests
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
git diff --check
py -m pytest -q
py -m ruff check src tests tools
rg -n "script.google.com/macros/s/|AKfy|WEBHOOK_URL|spreadsheetId|deploymentTag|C:\\Users\\|/Users/|data/match_logs/|data/runtime_logs/|data/failed_posts/|data/status/|api[_-]?key|token|secret|password|webhook_url" tests/fixtures/schema_snapshots
```

## Results

- `git fetch --prune origin main codex/code-hardening-suite` -> fetched target
  refs.
- `git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite`
  -> `0 0`.
- `py -m pytest -q tests\test_event_schema_snapshots.py` -> `6 passed in 0.75s`.
- `py -m pytest -q tests\test_events.py tests\test_app_models.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_app_outputs.py`
  -> `25 passed in 0.75s`.
- `py -m pytest -q tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py tests\test_gre_game_result_parser.py tests\test_match_state_parser.py tests\test_parser_small_modules.py tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_parser_regressions.py`
  -> `76 passed in 0.75s`.
- `py -m ruff check src tests` -> `All checks passed!`.
- `py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite`
  -> `changed_paths: 0; forbidden: 0; warnings: 0; result: passed`.
- Working-tree protected-surface path check including untracked files ->
  `changed_paths: 11; forbidden: 0; warnings: 0; result: passed`.
- `git diff --check` -> passed with no output.
- `py -m pytest -q` -> `408 passed in 4.28s`.
- `py -m ruff check src tests tools` -> `All checks passed!`.
- Secret/private/local marker scan over `tests/fixtures/schema_snapshots` ->
  no matches.

## Confirmed Contract Matches

- Current branch is `codex/code-hardening-suite`.
- `HEAD` is even with `origin/codex/code-hardening-suite`.
- Branch is at or after PR #59's api_common hardening merge baseline.
- Implementation is test-only plus docs/fixtures.
- Production parser/runtime code was not changed.
- Snapshot tests are deterministic in normal compare mode.
- Snapshot update behavior is opt-in through
  `MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS=1`.
- Snapshot mismatch and missing-snapshot failures use an explicit message that
  says not to auto-update snapshots without issue, contract, and review
  approval.
- Snapshot fixtures are stable JSON under `tests/fixtures/schema_snapshots/`.
- Parser event class snapshots cover class names, `kind` values, performance
  classes, dataclass field names, and `GameEvent` union membership.
- Parser payload snapshots store top-level payload key sets grouped by event
  kind and stable discriminator.
- Workbook row snapshots store `MatchLogRow` and `GameLogRow` ordered keys and
  stable row metadata.
- Workbook row tests explicitly assert `MGTA Start Time` remains present.
- Match/game sync fields are snapshotted and asserted as subsets of row keys.
- Sheet schema snapshots cover sync fields, runtime sheet specs, headers, and
  `SYNC_FIELDS_BY_ROW_KIND`.
- Runtime export snapshots cover runtime row families, metadata, and row key
  sets without actual runtime values.
- Apps Script parity snapshots are repo-side only and compare dispatch
  families, field-map keys, runtime landing headers, and runtime build-object
  data keys.
- Snapshot fixtures do not include forbidden/private/local markers found by the
  focused marker scan.
- Protected-surface checks passed.
- Pyright remains advisory; zero Pyright findings were not required.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests.

Accepted non-blocking limits:

- Parser payload snapshots use deterministic synthetic samples and current
  parser builders. They are a schema inventory, not an exhaustive semantic
  parser proof.
- Apps Script parity is static repo-source parity only. It does not prove live
  workbook state or deployed Apps Script state.
- Existing parser regression fixtures remain separate value-oriented tests.
- Pyright was not run in this E thread because issue #60 treats Pyright as
  advisory and does not require zero findings.

## Drift Notes

- No parser behavior drift found.
- No parser truth ownership drift found.
- No production workbook schema, webhook payload, or Apps Script behavior
  change found.
- No raw local log, generated data, runtime status, failed post, or workbook
  export artifact was included in the reviewed issue #60 package.
- Live workbook state and deployed Apps Script state were not inspected and are
  explicitly outside the repo-side snapshot proof.
- `docs/project_roadmap.md` and `docs/python_tooling_inventory.md` remain
  unrelated untracked files and must stay out of this module unless separately
  authorized.

## Recommendation

Approve for Codex F: Module Submitter.

No Codex D fixer pass is recommended because no implementation bug, contract
mismatch, missing required test, unsafe snapshot content, or validation failure
was found.

Codex F should stage only the reviewed issue #60 package and must not stage
`docs/project_roadmap.md` or `docs/python_tooling_inventory.md` unless
separately authorized.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and the mythic-edge-workflow skill.

Act as Codex F: Module Submitter for issue #60.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/60

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Reviewed issue #60 files:
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/implementation_handoffs/code_hardening_parser_event_schema_snapshots_comparison.md
- docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/apps_script_repo_parity.json
- tests/fixtures/schema_snapshots/parser_event_classes.json
- tests/fixtures/schema_snapshots/parser_payload_keys.json
- tests/fixtures/schema_snapshots/runtime_export_row_keys.json
- tests/fixtures/schema_snapshots/sheet_schema_surfaces.json
- tests/fixtures/schema_snapshots/workbook_row_keys.json

Reviewer verdict:
No blocking findings. Issue #60 parser event schema snapshot tests are ready for submitter work.

Submitter scope warning:
Do not stage docs/project_roadmap.md or docs/python_tooling_inventory.md for this PR unless the user separately authorizes them through an issue/contract. They are untracked and outside the reviewed issue #60 package.

Submitter tasks:
1. Verify current branch and working-tree status.
2. Stage only the reviewed issue #60 files.
3. Commit with a concise issue-linked message.
4. Push the branch.
5. Open or update a draft PR targeting codex/code-hardening-suite, not main.
6. Do not merge, close tracker #33, or target main.

Validation already checked by Codex E:
- py -m pytest -q tests\test_event_schema_snapshots.py -> 6 passed
- adjacent schema/model/export/output slice -> 25 passed
- adjacent parser slice -> 76 passed
- py -m pytest -q -> 408 passed
- py -m ruff check src tests tools -> All checks passed
- git diff --check -> passed
- protected-surface checks -> passed
- snapshot fixture secret/private/local marker scan -> no matches

Do not change parser behavior, auto-update snapshots, add volatile/private/generated snapshot data, change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/60"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md"
  target_artifact: "draft PR targeting codex/code-hardening-suite"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git fetch --prune origin main codex/code-hardening-suite -> fetched target refs"
    - "git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite -> 0 0"
    - "py -m pytest -q tests\\test_event_schema_snapshots.py -> 6 passed in 0.75s"
    - "py -m pytest -q tests\\test_events.py tests\\test_app_models.py tests\\test_sheet_schema.py tests\\test_sheet_exports.py tests\\test_app_outputs.py -> 25 passed in 0.75s"
    - "py -m pytest -q tests\\test_client_actions_parser.py tests\\test_gre_connect_resp_parser.py tests\\test_gre_game_state_parser.py tests\\test_gre_game_result_parser.py tests\\test_match_state_parser.py tests\\test_parser_small_modules.py tests\\test_connection_parsers.py tests\\test_collection_parser.py tests\\test_parser_regressions.py -> 76 passed in 0.75s"
    - "py -m ruff check src tests -> All checks passed"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed"
    - "working-tree protected-surface path check including untracked files -> passed"
    - "git diff --check -> passed with no output"
    - "py -m pytest -q -> 408 passed in 4.28s"
    - "py -m ruff check src tests tools -> All checks passed"
    - "snapshot fixture secret/private/local marker scan -> no matches"
  stop_conditions:
    - "Do not stage docs/project_roadmap.md or docs/python_tooling_inventory.md for issue #60 unless separately authorized."
    - "Do not change parser behavior."
    - "Do not auto-update snapshots without explicit issue/contract/review approval."
    - "Do not add snapshot files containing volatile/private/generated data."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main."
    - "Do not mark tracker #33 complete."
```
