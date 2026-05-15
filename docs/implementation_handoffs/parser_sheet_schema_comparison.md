# Parser Sheet Schema Implementation Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/46

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Source contract: `docs/contracts/parser_sheet_schema.md`

Target branch: `codex/parser-module-audit-suite`

Role: Codex C: Module Implementer

Risk tier: High

## Summary Of Implementation Comparison

The current `sheet_schema.py` implementation matches the parser sheet-schema
contract for the reviewed runtime behavior: it is a pure Python-side workbook
schema registry, exposes stable sync-field tuples, runtime landing-header
tuples, frozen `RuntimeSheetSpec` records, runtime family/event-type/scope
vocabulary, and direct fail-fast lookup helpers.

No runtime code or schema constant change was needed. The comparison found
missing focused tests around ordered schema stability, runtime family coverage,
Apps Script runtime landing-header alignment, unknown-key behavior, and the
legacy `"MGTA Start Time"` compatibility spelling. This pass adds those tests
in `tests/test_sheet_schema.py` only.

Changed files:

- `tests/test_sheet_schema.py`
- `docs/implementation_handoffs/parser_sheet_schema_comparison.md`

Referenced source artifact already present in the worktree:

- `docs/contracts/parser_sheet_schema.md`

Repository hygiene note:

- `docs/contracts/parser_sheet_schema.md` was already untracked at the start of
  this pass and remains the source artifact for issue #46.
- No files were staged or committed.

## Findings First

### Resolved: runtime sheet specs were weakly covered

Contract requirement:

- Every `RUNTIME_SHEET_SPECS` entry has the expected family, event type, scope,
  and exact header tuple.
- Registry keys match the corresponding `RuntimeSheetSpec.family` values.

Initial state:

- `tests/test_sheet_schema.py` directly asserted only the Action Log runtime
  sheet spec.

Resolution:

- Added parametrized coverage for all five runtime families:
  `ActionLogRow`, `DeckSnapshotRow`, `CollectionSnapshotRow`,
  `ParserStatusRow`, and `CardPerformanceRow`.
- Added a registry-key test proving every mapping key matches the spec family.

### Resolved: ordered sync fields were not protected strongly enough

Contract requirement:

- `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS` order is stable.
- Apps Script Match Log and Game Log field-map keys match Python sync fields.

Initial state:

- Apps Script field-map tests compared sets, so order drift would not fail.

Resolution:

- Added explicit ordered snapshots for Match Log and Game Log sync fields.
- Changed Apps Script field-map extraction to return ordered tuples.
- Updated the Apps Script field-map tests to compare exact ordered tuples.

### Resolved: runtime header alignment with Apps Script was untested

Contract requirement:

- Python runtime header tuples must match Apps Script
  `WORKBOOK_SCHEMA.landingHeaders` arrays by exact order.

Initial state:

- No focused test compared runtime landing headers between Python and Apps
  Script.

Resolution:

- Added exact-order tests for Action Log, Deck Snapshot, Collection Snapshot,
  Parser Status, and Card Performance landing headers.
- Added exact-order tests that each Apps Script runtime row-object builder
  covers the corresponding runtime header tuple.

### Resolved: fail-fast lookup behavior was untested

Contract requirement:

- Unknown `runtime_sheet_spec()`, `runtime_sheet_headers()`, and
  `sync_fields()` inputs raise direct `KeyError`.

Initial state:

- Unknown-key behavior was documented by the contract but not covered in
  `tests/test_sheet_schema.py`.

Resolution:

- Added a focused test for `KeyError` behavior across all three lookup helpers.

### Resolved: legacy `"MGTA Start Time"` spelling was not explicitly guarded

Contract requirement:

- `"MGTA Start Time"` is a legacy external compatibility spelling that must
  remain present across Python sync fields, model rows, and Apps Script field
  maps unless a future migration contract authorizes a change.

Initial state:

- The spelling existed in implementation and Apps Script, but no focused test
  named it as a protected compatibility value.

Resolution:

- Added a focused test proving `"MGTA Start Time"` remains present in
  `MATCH_LOG_SYNC_FIELDS`, `MatchSummary.to_match_log_row()`, and
  `buildMatchLogFieldMap_()`.

## Confirmed Matches

- `sheet_schema.py` remains a schema-vocabulary registry only.
- The module has no file, network, workbook, runtime-state, webhook, or Apps
  Script side effects at import time.
- `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS` are tuples.
- Runtime landing headers are tuples.
- `RuntimeSheetSpec` is frozen and slotted.
- Runtime families remain exactly:
  `ActionLogRow`, `DeckSnapshotRow`, `CollectionSnapshotRow`,
  `ParserStatusRow`, and `CardPerformanceRow`.
- Runtime event types remain exactly:
  `action_log_row`, `deck_snapshot_row`, `collection_snapshot_row`,
  `parser_status_row`, and `card_performance_row`.
- Runtime scopes remain exactly:
  `Match`, `Deck`, `Collection`, `Runtime`, and `Card`.
- `RUNTIME_SHEET_SPECS` maps each family to a spec with matching family,
  event type, scope, and headers.
- `SYNC_FIELDS_BY_ROW_KIND` maps exactly `"match_log"` and `"game_log"` to the
  public sync-field tuples.
- `runtime_sheet_spec()`, `runtime_sheet_headers()`, and `sync_fields()` remain
  direct lookup helpers that raise `KeyError` for unknown values.
- Apps Script Match Log and Game Log field-map keys align with Python sync
  fields by exact order.
- Apps Script runtime landing headers align with Python runtime header tuples by
  exact order.
- Apps Script runtime row-object builders cover the matching runtime landing
  headers by exact order.
- Representative model tests already prove Match Log and Game Log rows include
  every Python sync field.
- Existing sheet-export tests already prove runtime rows emit the five expected
  runtime families.

## Contract Mismatches

No implementation contract mismatch was found in `sheet_schema.py`.

The only mismatches found were missing or weak tests. They were resolved in
`tests/test_sheet_schema.py`.

## Missing Safeguards

No runtime safeguard change was required.

Test safeguards added:

- Ordered sync-field snapshots.
- Exact-order Apps Script sync-field map alignment.
- Exact-order Apps Script runtime landing-header alignment.
- Exact-order Apps Script runtime row-object key coverage.
- Runtime spec coverage for every family.
- Direct `KeyError` coverage for unknown lookup inputs.
- Legacy `"MGTA Start Time"` compatibility coverage.

Behavior deliberately left unchanged:

- Schema constants remain unchanged.
- Apps Script mappings and landing headers remain unchanged.
- Direct dictionary lookup behavior remains unchanged.
- `RUNTIME_SHEET_SPECS` and `SYNC_FIELDS_BY_ROW_KIND` remain mutable
  dictionaries, matching observed current behavior in the contract.

## Missing Or Weak Tests

Blocking focused test gaps from the contract were addressed.

Remaining non-blocking gaps:

- Tests parse Apps Script source text rather than executing Apps Script.
- Tests do not inspect a live workbook or deployed Apps Script project.
- Tests do not add a broader generated schema snapshot artifact. The contract
  names that as possible future hardening work, not a requirement for this
  pass.

## Validation Evidence

Commands run:

```bash
python3 -m pytest -q tests/test_sheet_schema.py
```

Result:

```text
27 passed in 0.08s
```

```bash
python3 -m pytest -q tests/test_app_models.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py
```

Result:

```text
28 passed in 0.19s
```

```bash
python3 -m pytest -q tests/test_state.py tests/test_runner.py tests/test_app_outputs.py tests/test_transforms.py
```

Result:

```text
65 passed in 0.31s
```

```bash
python3 -m ruff check src tests
```

Result:

```text
All checks passed!
```

```bash
git diff --check
```

Result: passed with no output.

## Still-Unverified Layers

- Live workbook tabs were not inspected.
- Deployed Apps Script behavior was not executed.
- Live webhook delivery was not executed.
- Raw MTGA log ingestion was not executed.
- GitHub Actions/Windows CI was not executed.
- Submitter/deployer PR checks have not run.
- Tracker #5 was not marked complete.

## Reviewer Focus

Ask Codex E to verify:

- No schema constants, Apps Script mappings, workbook-facing field names, event
  families, event types, scopes, or row kinds changed.
- Ordered sync-field tests are intentionally exact and preserve `"MGTA Start
  Time"`.
- Apps Script parsing tests compare exact order for landing headers and field
  maps, not only set membership.
- `sheet_schema.py` remains a schema registry and does not move parser-owned
  truth into workbook formulas, dashboard logic, Apps Script, webhook delivery,
  output transport, or AI-generated interpretation.
- Adjacent model/export/state/runner/output/transform tests still pass.

## Next Workflow Action

Next role: Codex E: Module Reviewer

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #46:
https://github.com/Tahjali11/Mythic-Edge/issues/46

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_sheet_schema.md
- docs/implementation_handoffs/parser_sheet_schema_comparison.md
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_sheet_schema.py
- src/mythic_edge_parser/app/models.py
- tests/test_app_models.py
- src/mythic_edge_parser/app/sheet_exports.py
- tests/test_sheet_exports.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_runtime_surfaces.py
- src/mythic_edge_parser/app/state.py
- tests/test_state.py
- src/mythic_edge_parser/app/runner.py
- tests/test_runner.py
- src/mythic_edge_parser/app/outputs.py
- tests/test_app_outputs.py
- src/mythic_edge_parser/app/transforms.py
- tests/test_transforms.py
- tools/google_apps_script/Code.gs
- any directly referenced schema-adjacent files or focused tests named by the contract

Goal:
Verify the Module Implementer comparison and focused test additions against the parser sheet-schema contract.

Confirm:
- sheet_schema.py remains the Python-side workbook/schema registry only.
- No schema constants, Apps Script mappings, workbook-facing field names, event families, event types, scopes, or row kinds changed.
- RuntimeSheetSpec remains frozen and slotted.
- Every RUNTIME_SHEET_SPECS entry has the expected family, event type, scope, and exact header tuple.
- runtime_sheet_headers(family) returns the same tuple as the corresponding spec.
- Unknown runtime_sheet_spec(), runtime_sheet_headers(), and sync_fields() inputs raise KeyError.
- SYNC_FIELDS_BY_ROW_KIND maps exactly "match_log" and "game_log" to the public sync-field tuples.
- MATCH_LOG_SYNC_FIELDS and GAME_LOG_SYNC_FIELDS order is stable.
- Apps Script Match Log and Game Log field-map keys match Python sync fields by exact order.
- Runtime Python header tuples match Apps Script WORKBOOK_SCHEMA.landingHeaders arrays by exact order.
- Apps Script runtime row-object builders cover the corresponding runtime landing headers by exact order.
- Representative model-produced Match Log and Game Log rows include every sync-field key.
- "MGTA Start Time" is present in the Match Log sync tuple, model row, and Apps Script field map.
- Runtime row families emitted by sheet_exports.py remain exactly ActionLogRow, DeckSnapshotRow, CollectionSnapshotRow, ParserStatusRow, and CardPerformanceRow.
- No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.
- Parser-owned truth was not moved into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation.

Validation:
Run:
python3 -m pytest -q tests/test_sheet_schema.py
python3 -m pytest -q tests/test_app_models.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py
python3 -m pytest -q tests/test_state.py tests/test_runner.py tests/test_app_outputs.py tests/test_transforms.py
python3 -m ruff check src tests
git diff --check

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation.
Do not change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration.
Do not stage, commit, merge, target main, or mark tracker #5 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/46"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_sheet_schema.md"
  target_artifact: "docs/implementation_handoffs/parser_sheet_schema_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_sheet_schema.py"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_runner.py tests/test_app_outputs.py tests/test_transforms.py"
    - "python3 -m ruff check src tests"
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation."
    - "Do not change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration."
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Do not mark tracker #5 complete."
```
