# Parser Sheet Schema Contract Test Report

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/46

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Contract: `docs/contracts/parser_sheet_schema.md`

Implementation handoff: `docs/implementation_handoffs/parser_sheet_schema_comparison.md`

Branch: `codex/parser-module-audit-suite`

Role: Codex E: Module Reviewer

Risk tier: High

## Findings First

No blocking findings.

The Module Implementer patch is scoped to focused schema-boundary tests and
documentation artifacts:

- `tests/test_sheet_schema.py`
- `docs/contracts/parser_sheet_schema.md`
- `docs/implementation_handoffs/parser_sheet_schema_comparison.md`

No `sheet_schema.py` constants, Apps Script mappings, workbook-facing field
names, runtime row families, event types, scopes, row kinds, parser behavior,
parser state final reconciliation, workbook schema, webhook payload shape,
parser event classes, match/game identity, deduplication behavior, secrets,
environment variables, raw logs, generated data, runtime status files, failed
posts, or workbook exports changed.

## Contract-Test Verdict

Pass.

The implementation handoff and focused test additions satisfy the parser
sheet-schema contract for the reviewed scope. This module can move to Codex F:
Module Submitter.

## Confirmed Contract Matches

- `sheet_schema.py` remains a Python-side workbook/schema registry only.
- `RuntimeSheetSpec` remains frozen and slotted.
- `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS` remain ordered, stable
  tuples.
- `"MGTA Start Time"` remains present in the Match Log sync tuple,
  `MatchSummary.to_match_log_row()`, and the Apps Script Match Log field map.
- `RUNTIME_SHEET_SPECS` contains exactly the five contracted runtime row
  families: `ActionLogRow`, `DeckSnapshotRow`, `CollectionSnapshotRow`,
  `ParserStatusRow`, and `CardPerformanceRow`.
- Each runtime sheet spec has the expected family, event type, scope, and exact
  header tuple.
- `runtime_sheet_headers(family)` returns the exact header tuple from the
  corresponding spec.
- `SYNC_FIELDS_BY_ROW_KIND` maps exactly `"match_log"` and `"game_log"` to the
  public sync-field tuples.
- Unknown `runtime_sheet_spec()`, `runtime_sheet_headers()`, and
  `sync_fields()` inputs raise `KeyError`.
- Apps Script Match Log and Game Log field-map keys match the Python sync-field
  tuples by exact order.
- Python runtime header tuples match Apps Script
  `WORKBOOK_SCHEMA.landingHeaders` arrays by exact order.
- Apps Script runtime row-object builders cover the corresponding runtime
  landing headers by exact order.
- Representative model-produced Match Log and Game Log rows still include every
  sync-field key through the adjacent model tests.
- Runtime row family emission remains covered by sheet-export tests.
- Parser-owned truth was not moved into workbook formulas, dashboard logic, Apps
  Script, webhook delivery, output transport, or AI-generated interpretation.

## Contract Mismatches

None.

## Missing Tests

No blocking missing tests remain for the issue #46 contract scope.

Focused coverage now includes:

- full runtime sheet spec coverage for every runtime family
- exact ordered Match Log and Game Log sync-field snapshots
- exact ordered Apps Script sync-field map alignment
- exact ordered Apps Script runtime landing-header alignment
- exact ordered Apps Script runtime row-object key coverage
- `RuntimeSheetSpec` immutability and slotted shape
- lookup-helper `KeyError` behavior
- row-kind registry coverage
- legacy `"MGTA Start Time"` compatibility spelling coverage

## Drift Classification

- Repo drift: none found. The only tracked diff is
  `tests/test_sheet_schema.py`; the contract and implementation handoff are
  untracked workflow artifacts for issue #46.
- Workbook schema drift: none found.
- Webhook payload shape drift: none found.
- Apps Script behavior drift: none found.
- Parser behavior drift: none found.
- Parser state final reconciliation drift: none found.
- Parser event class drift: none found.
- Match/game identity drift: none found.
- Deduplication drift: none found.
- Secret/local artifact drift: none found.
- Tracker drift: tracker #5 was not marked complete.
- Branch drift: review was performed on `codex/parser-module-audit-suite`, not
  `main`.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_sheet_schema.py
```

Result:

```text
27 passed in 0.07s
```

```bash
python3 -m pytest -q tests/test_app_models.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py
```

Result:

```text
28 passed in 0.18s
```

```bash
python3 -m pytest -q tests/test_state.py tests/test_runner.py tests/test_app_outputs.py tests/test_transforms.py
```

Result:

```text
65 passed in 0.29s
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

```bash
python3 -m pytest -q
```

Result:

```text
557 passed in 2.34s
```

Protected-surface spot checks:

```bash
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports .github
```

Result: passed with no output.

```bash
git diff -- src/mythic_edge_parser/app/sheet_schema.py tools/google_apps_script/Code.gs src/mythic_edge_parser/app/state.py src/mythic_edge_parser/app/models.py src/mythic_edge_parser/app/sheet_exports.py src/mythic_edge_parser/app/outputs.py src/mythic_edge_parser/app/transforms.py src/mythic_edge_parser/app/runtime_surfaces.py
```

Result: passed with no output.

## Remaining Non-Blocking Gaps

- Tests parse Apps Script source text rather than executing Apps Script.
- Live workbook tabs were not inspected.
- Deployed Apps Script behavior was not executed.
- Live webhook delivery was not exercised.
- GitHub Actions and Windows CI were not run locally.
- A broader generated schema snapshot/drift artifact may be useful later, but it
  is outside this contract-test pass.

## Next Recommended Role

Codex F: Module Submitter.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/46"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_sheet_schema.md"
  target_artifact: "PR for issue #46 on codex/parser-module-audit-suite"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  verdict: "No blocking findings. Ready for Codex F: Module Submitter."
  validation:
    - "python3 -m pytest -q tests/test_sheet_schema.py -> 27 passed in 0.07s"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py -> 28 passed in 0.18s"
    - "python3 -m pytest -q tests/test_state.py tests/test_runner.py tests/test_app_outputs.py tests/test_transforms.py -> 65 passed in 0.29s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed"
    - "python3 -m pytest -q -> 557 passed in 2.34s"
  stop_conditions:
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation."
    - "Do not change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration."
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Do not mark tracker #5 complete."
```
