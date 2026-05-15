# Parser Sheet Exports Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/52

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_sheet_exports.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Changed files under review:

- `src/mythic_edge_parser/app/sheet_exports.py`
- `tests/test_sheet_exports.py`
- `docs/contracts/parser_sheet_exports.md`
- `docs/implementation_handoffs/parser_sheet_exports_comparison.md`

## Findings First

No blocking findings.

## Contract Summary

`sheet_exports.py` is the runtime workbook export row-construction boundary. It
builds workbook-facing runtime row dictionaries from parser/runtime artifacts,
attaches metadata from `sheet_schema.py`, suppresses repeated runtime exports in
memory, and returns rows for output transport.

It must not post webhooks, write workbooks, define workbook schema, edit Apps
Script mappings, mutate parser state, interpret raw MTGA events, or move
parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook
delivery, output transport, or AI-generated interpretation.

## Confirmed Contract Matches

- `collect_runtime_sheet_rows()` remains the public runtime row collection API.
- Rows still emit in the contracted family order: Action Log, Deck Snapshot,
  Collection Snapshot, Parser Status, then Card Performance.
- Every emitted row includes `event_family`, `event_type`, and `scope` from
  `sheet_schema.runtime_sheet_spec()`.
- Collection Snapshot exports now support nested `inventory.wildcards` while
  preserving flat wildcard keys and the existing emitted row field names.
- `_safe_int()` blanks booleans and invalid values while preserving current
  Python `int()` behavior for valid integers, numeric strings, and floats.
- `_load_json_dict()` covers missing files, invalid JSON, non-dict top-level
  JSON, successful cache reuse, and cache refresh.
- `reset_sheet_export_state()` clears posted action keys, snapshot fingerprints,
  and JSON cache state.
- Action Log dedupe uses the documented key fields and ignores documented
  non-key fields.
- Snapshot dedupe ignores only documented transient fields and re-emits for
  non-transient changes.
- Non-dict entries in accepted Action Log, Deck Snapshot, and Card Performance
  list sections are skipped.
- Focused tests cover Apps Script-consumed snake_case data keys without changing
  Apps Script behavior or mappings.
- No schema constants, Apps Script mappings, webhook transport, parser state
  final reconciliation, parser event classes, match identity, game identity,
  raw logs, generated data, runtime status files, failed posts, or workbook
  exports changed.

## Contract Mismatches

None found.

The prior implementation mismatch around nested collection wildcard payloads is
resolved by a sheet-export-local fallback from flat wildcard keys to
`inventory.wildcards.{common,uncommon,rare,mythic}`. Workbook-facing row names
remain `wildcards_common`, `wildcards_uncommon`, `wildcards_rare`, and
`wildcards_mythic`.

## Missing Tests

No blocking missing tests remain for this contract pass.

Focused tests now cover the required high-risk behaviors:

- JSON loader degradation and cache behavior
- reset state cleanup
- disabled family flag behavior
- runtime row metadata and exact row field shape
- Apps Script-consumed snake_case keys
- nested collection wildcard input
- Action Log dedupe key behavior
- snapshot transient-field behavior
- non-dict entry skips in accepted list sections

## Drift Notes

Drift classification: no blocking drift.

- Contract drift: none found.
- Workbook schema drift: none found.
- Apps Script drift: none found.
- Webhook payload drift: none found.
- Parser truth drift: none found.
- Runtime artifact drift: none found in committed changes.
- Tracker drift: none found; issue #52 and tracker #5 remain open.

Remaining non-blocking unverified layers:

- Live workbook tabs were not inspected.
- Deployed Apps Script was not executed.
- Live webhook delivery was not executed.
- Same-mtime filesystem cache edge cases were not exercised through the real
  filesystem beyond the contract-covered cache-key boundary.

## Validation Evidence

```bash
git diff --check -- docs/contracts/parser_sheet_exports.md
```

Result: passed with no output.

```bash
python3 -m pytest -q tests/test_sheet_exports.py
```

Result: `16 passed in 0.22s`

```bash
python3 -m pytest -q tests/test_sheet_exports.py tests/test_analytics_sidecar.py
```

Result: `21 passed in 0.32s`

```bash
python3 -m pytest -q tests/test_sheet_schema.py tests/test_runtime_surfaces.py tests/test_app_outputs.py
```

Result: `53 passed in 0.30s`

```bash
python3 -m pytest -q tests/test_runner.py tests/test_app_outputs.py
```

Result: `37 passed in 0.40s`

```bash
python3 -m ruff check src tests
```

Result: `All checks passed!`

```bash
git diff --check
```

Result: passed with no output.

```bash
python3 -m pytest -q
```

Result: `568 passed in 1.24s`

```bash
git diff --name-only -- src/mythic_edge_parser/app/state.py src/mythic_edge_parser/app/models.py src/mythic_edge_parser/events.py src/mythic_edge_parser/parsers src/mythic_edge_parser/app/sheet_schema.py src/mythic_edge_parser/app/outputs.py tools/google_apps_script/Code.gs .env .env.local data generated failed_posts exports
```

Result: passed with no output.

## Recommendation

Approve for submitter review.

Next recommended role: Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #52:
https://github.com/Tahjali11/Mythic-Edge/issues/52

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_sheet_exports.md
- docs/implementation_handoffs/parser_sheet_exports_comparison.md
- docs/contract_test_reports/parser_sheet_exports.md
- src/mythic_edge_parser/app/sheet_exports.py
- tests/test_sheet_exports.py
- docs/codex_module_workflow.md
- .github/pull_request_template.md

Goal:
Prepare the parser sheet exports contract-audit work for PR review. Verify the
Codex E report has no blocking findings, run or confirm validation, stage only
the issue #52 artifacts, commit them, push the branch, and open or update a
draft PR targeting codex/parser-module-audit-suite.

Confirm:
- PR target is codex/parser-module-audit-suite, not main.
- The PR remains scoped to parser sheet exports contract/test work.
- The nested collection wildcard compatibility fix preserves flat wildcard
  behavior and emitted row field names.
- No schema constants or Apps Script mappings changed.
- No parser behavior outside sheet export contract requirements changed.
- No parser state final reconciliation, workbook schema, webhook payload shape,
  Apps Script behavior, parser event classes, match identity, game identity,
  secrets, environment variables, raw logs, generated data, runtime status
  files, failed posts, or workbook exports changed.
- Tracker #5 is not marked complete.

Validation:
Run or confirm:
git diff --check
python3 -m pytest -q tests/test_sheet_exports.py
python3 -m pytest -q tests/test_sheet_exports.py tests/test_analytics_sidecar.py
python3 -m pytest -q tests/test_sheet_schema.py tests/test_runtime_surfaces.py tests/test_app_outputs.py
python3 -m pytest -q tests/test_runner.py tests/test_app_outputs.py
python3 -m pytest -q
python3 -m ruff check src tests

Output:
- PR URL or updated PR status.
- Validation results.
- Scope/protected-surface confirmation.
- workflow_handoff block routing to Codex E for PR re-review, or Codex G only
  if the repo workflow explicitly says this submitter pass is complete and the
  PR is ready for integration deployment.

Do not merge.
Do not close issue #52.
Do not mark tracker #5 complete.
Do not target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/52"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_sheet_exports.md"
  target_artifact: "module PR targeting codex/parser-module-audit-suite"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  verdict: "No blocking findings. Ready for Codex F: Module Submitter."
  validation:
    - "git diff --check -- docs/contracts/parser_sheet_exports.md -> passed"
    - "python3 -m pytest -q tests/test_sheet_exports.py -> 16 passed"
    - "python3 -m pytest -q tests/test_sheet_exports.py tests/test_analytics_sidecar.py -> 21 passed"
    - "python3 -m pytest -q tests/test_sheet_schema.py tests/test_runtime_surfaces.py tests/test_app_outputs.py -> 53 passed"
    - "python3 -m pytest -q tests/test_runner.py tests/test_app_outputs.py -> 37 passed"
    - "python3 -m ruff check src tests -> passed"
    - "git diff --check -> passed"
    - "python3 -m pytest -q -> 568 passed"
  stop_conditions:
    - "Do not merge."
    - "Do not close issue #52."
    - "Do not mark tracker #5 complete."
    - "Do not target main."
    - "Do not change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation."
```
