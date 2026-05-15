# Code Hardening Parser Event Schema Snapshots Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/60

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

`docs/contracts/code_hardening_parser_event_schema_snapshots.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Baseline Status

Branch used:

```text
codex/code-hardening-suite
```

Baseline checks:

```text
HEAD: 3d9cee0
HEAD...origin/codex/code-hardening-suite: 0 ahead / 0 behind
PR #59 merge commit 3d9cee0772d24c5b04631c00ebd4a8834b8a640f is an ancestor of HEAD.
```

Unrelated untracked files present before implementation and not absorbed into
this module:

- `docs/project_roadmap.md`
- `docs/python_tooling_inventory.md`

The source contract `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
was also already present as an untracked source artifact before this C pass.

## What The Snapshots Are Supposed To Protect

The issue #60 snapshots are test-only guardrails for accidental schema drift.
They protect stable schema surfaces that downstream parser, workbook, Apps
Script, and future analytics code depend on:

- parser event class names, `kind` values, performance classes, and `GameEvent`
  union membership
- parser-produced payload top-level key sets grouped by event kind and stable
  discriminator
- ordered `MatchLogRow` and `GameLogRow` keys
- `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS`
- runtime sheet specs, headers, row families, event types, scopes, and emitted
  runtime row key sets
- repo-side Apps Script parity for dispatch families, field maps, runtime
  landing headers, and snake_case runtime row keys

Plain English: the test should make a schema change visible as a reviewable
diff. It should not change parser behavior, redefine truth, or prove live
workbook/deployed Apps Script state.

## Current Behavior Compared To Contract

Existing tests already covered many individual values and parser behaviors, but
the contract gaps were still present:

- no focused inventory of all concrete event classes, `kind` values,
  performance classes, and `GameEvent` union members
- no focused parser payload key inventory grouped across parser modules
- no focused snapshot for `MatchLogRow` / `GameLogRow` key order
- no focused snapshot for all runtime sheet specs, sync fields, runtime row
  key sets, and Apps Script repo parity
- no explicit failure message telling future agents not to auto-update schema
  snapshots without approval

No runtime schema mismatch requiring production code changes was found.

## What Changed

Added focused deterministic schema snapshot tests:

- `tests/test_event_schema_snapshots.py`

Added stable JSON snapshot fixtures:

- `tests/fixtures/schema_snapshots/parser_event_classes.json`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `tests/fixtures/schema_snapshots/workbook_row_keys.json`
- `tests/fixtures/schema_snapshots/sheet_schema_surfaces.json`
- `tests/fixtures/schema_snapshots/runtime_export_row_keys.json`
- `tests/fixtures/schema_snapshots/apps_script_repo_parity.json`

The test file includes an opt-in update mode:

```powershell
$env:MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS = "1"
py -m pytest -q tests\test_event_schema_snapshots.py
Remove-Item Env:\MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS
```

Normal CI/local behavior is compare-only. Missing or mismatched snapshots fail
with a message that says not to auto-update snapshots without explicit
issue/contract/review approval.

## Files Changed

Implementation files changed by this pass:

- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/apps_script_repo_parity.json`
- `tests/fixtures/schema_snapshots/parser_event_classes.json`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `tests/fixtures/schema_snapshots/runtime_export_row_keys.json`
- `tests/fixtures/schema_snapshots/sheet_schema_surfaces.json`
- `tests/fixtures/schema_snapshots/workbook_row_keys.json`
- `docs/implementation_handoffs/code_hardening_parser_event_schema_snapshots_comparison.md`

Source artifact used but not authored in this C pass:

- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`

Unrelated untracked files left untouched:

- `docs/project_roadmap.md`
- `docs/python_tooling_inventory.md`

## Code Changed

Test-only plus this handoff.

No production parser/runtime code changed.

## Tests Changed

Added `tests/test_event_schema_snapshots.py` with six focused snapshot tests:

- parser event class schema snapshot
- parser payload key snapshot
- workbook row key snapshot
- sheet schema surface snapshot
- runtime export row key snapshot
- Apps Script repo parity snapshot

## Interface Changes

None.

No parser behavior, parser event classes, event `kind` values, parser payload
shapes, parser state final reconciliation, workbook schema, webhook payload
shape, Apps Script behavior, match/game identity, deduplication, secrets,
environment variables, runtime status files, failed posts, generated data, raw
logs, or workbook exports changed.

## Contract Matches

- Correct branch target used: `codex/code-hardening-suite`.
- Branch is at the expected PR #59 baseline.
- Snapshot tests are deterministic and clean-clone safe.
- Snapshot fixtures are JSON, UTF-8, two-space indented, and stable.
- Snapshot content is schema-level only.
- Parser payload snapshots store top-level key sets, not full raw nested source
  payloads.
- Workbook row snapshots preserve key order.
- Runtime sheet specs and runtime export row keys are covered.
- Apps Script assertions are repo-side only and do not call Apps Script or
  inspect live workbook/deployment state.
- Snapshot update mode is opt-in and not default.
- Protected-surface path check passed.

## Contract Mismatches

None found.

## Missing Safeguards Or Missing Tests

No issue #60 required snapshot surface remains knowingly uncovered.

Remaining non-blocking limits:

- The parser payload snapshot uses deterministic synthetic parser samples plus
  current parser builders. It is a schema inventory, not an exhaustive parser
  semantic proof.
- Apps Script parity is static repo-source parity only. It does not prove the
  live workbook or deployed Apps Script matches the repo.
- Existing parser regression fixtures remain value-oriented and separate from
  these schema snapshots.

## Snapshot Data Safety Notes

Snapshots intentionally include only stable schema content:

- class names
- `kind` and performance class values
- dataclass field names
- payload key names
- row key names and stable row metadata values
- sync fields
- runtime headers
- Apps Script field-map/header/data-key names

Snapshots intentionally exclude:

- actual raw log lines
- actual `EventMetadata.raw_bytes`
- actual raw byte hashes
- timestamps/current dates
- local absolute paths
- webhook URLs, API keys, tokens, credentials, or environment values
- runtime status contents
- failed posts
- workbook exports
- generated card/tier data
- live workbook or deployed Apps Script state

A focused fixed-string scan over the snapshot fixtures found no forbidden
secret, webhook, local-path, live workbook, or generated-data markers.

## Validation Run

Initial missing-snapshot check:

```powershell
py -m pytest -q tests\test_event_schema_snapshots.py
```

Result:

```text
6 failed with explicit missing-snapshot/update-policy messages.
```

Initial fixture creation under explicit update mode:

```powershell
$env:MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS='1'; py -m pytest -q tests\test_event_schema_snapshots.py; Remove-Item Env:\MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS
```

Result:

```text
6 passed in 0.51s
```

Focused snapshot validation in normal compare mode:

```powershell
py -m pytest -q tests\test_event_schema_snapshots.py
```

Result:

```text
6 passed in 0.53s
```

Adjacent schema/model/export/output validation:

```powershell
py -m pytest -q tests\test_events.py tests\test_app_models.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_app_outputs.py
```

Result:

```text
25 passed in 0.69s
```

Adjacent parser validation:

```powershell
py -m pytest -q tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py tests\test_gre_game_result_parser.py tests\test_match_state_parser.py tests\test_parser_small_modules.py tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_parser_regressions.py
```

Result:

```text
76 passed in 0.69s
```

Lint:

```powershell
py -m ruff check src tests
```

Result:

```text
All checks passed!
```

Protected-surface gate requested by the contract:

```powershell
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Result:

```text
Protected Surface Gate
base: origin/codex/code-hardening-suite
head: HEAD
changed_paths: 0
forbidden: 0
warnings: 0

result: passed
```

Working-tree path check including untracked files:

```powershell
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Result:

```text
Protected Surface Gate
base: origin/codex/code-hardening-suite
head: HEAD
changed_paths: 10
forbidden: 0
warnings: 0

result: passed
```

Diff whitespace:

```powershell
git diff --check
```

Result:

```text
passed with no output
```

## Still Unverified

- Full `py -m pytest -q` was not run in this C thread.
- Pyright was not run; issue #60 keeps Pyright advisory-only and does not
  require zero findings.
- GitHub Actions were not checked because this implementer thread did not open
  a PR.
- Live workbook state and deployed Apps Script state were not inspected.
- Raw local logs, generated data, runtime status files, failed posts, and
  workbook exports were not inspected.

## Reviewer Focus

Ask Codex E to verify:

- the snapshot fixture contents are schema-only and do not include volatile,
  private, generated, or local data
- parser payload snapshots are broad enough for issue #60 without becoming a
  second parser
- Apps Script parity checks stay repo-side and do not imply live deployment
  verification
- update-mode behavior is opt-in and the failure message is clear
- unrelated untracked docs are not accidentally absorbed into this module

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and the mythic-edge-workflow skill.

Act as Codex E: Module Reviewer / contract-test thread for issue #60.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/60

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Source artifacts:
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/implementation_handoffs/code_hardening_parser_event_schema_snapshots_comparison.md
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/sheet_exports.py
- tools/google_apps_script/Code.gs

Goal:
Review the issue #60 implementation against the schema snapshot contract. Verify that the new snapshot tests and fixtures protect the required event/schema/workbook/runtime/Apps Script repo-side surfaces without changing parser behavior or including volatile/private/generated data.

Review focus:
- findings first, ordered by severity
- contract matches and mismatches
- missing tests or over-broad/brittle snapshots
- snapshot data safety
- update-policy safety
- whether any protected parser/runtime/workbook/App Script surface changed
- validation evidence and remaining unverified layers

Do not:
- change parser behavior
- change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports
- auto-update snapshots
- target main
- mark tracker #33 complete
- stage, commit, open a PR, or merge unless explicitly asked

Suggested validation:
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_events.py tests\test_app_models.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_app_outputs.py
py -m pytest -q tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py tests\test_gre_game_result_parser.py tests\test_match_state_parser.py tests\test_parser_small_modules.py tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_parser_regressions.py
py -m ruff check src tests
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
git diff --check

Produce:
docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/60"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/code_hardening_parser_event_schema_snapshots.md"
  target_artifact: "docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "py -m pytest -q tests\\test_event_schema_snapshots.py -> 6 passed in 0.53s"
    - "py -m pytest -q tests\\test_events.py tests\\test_app_models.py tests\\test_sheet_schema.py tests\\test_sheet_exports.py tests\\test_app_outputs.py -> 25 passed in 0.69s"
    - "py -m pytest -q tests\\test_client_actions_parser.py tests\\test_gre_connect_resp_parser.py tests\\test_gre_game_state_parser.py tests\\test_gre_game_result_parser.py tests\\test_match_state_parser.py tests\\test_parser_small_modules.py tests\\test_connection_parsers.py tests\\test_collection_parser.py tests\\test_parser_regressions.py -> 76 passed in 0.69s"
    - "py -m ruff check src tests -> All checks passed"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed"
    - "working-tree protected-surface path check including untracked files -> passed"
    - "git diff --check -> passed with no output"
  stop_conditions:
    - "Do not change parser behavior."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not add snapshot files containing volatile/private/generated data."
    - "Do not auto-update snapshots without explicit issue/contract/review approval."
    - "Do not absorb unrelated untracked files into this module."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
