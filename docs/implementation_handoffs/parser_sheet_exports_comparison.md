# Parser Sheet Exports Implementation Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/52

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Source contract: `docs/contracts/parser_sheet_exports.md`

Target branch: `codex/parser-module-audit-suite`

Role: Codex C: Module Implementer

Risk tier: High

## Summary Of Implementation Comparison

The current `sheet_exports.py` implementation already matched the parser sheet
exports contract for its core boundary: it builds runtime workbook-facing row
dictionaries, sources row metadata from `sheet_schema.py`, suppresses repeated
runtime exports in memory, and does not post webhooks, write workbooks, mutate
parser state, or own parser truth.

This comparison found one clear contract mismatch and several focused test
coverage gaps:

- The contract accepts collection payloads with nested `inventory.wildcards`,
  but `sheet_exports.py` only read flat `wildcards_common` style inventory keys.
- Focused tests did not cover JSON loader/cache behavior, reset state cleanup,
  export flag load gating, exact row metadata/field shape, Apps
  Script-consumed snake_case field coverage, action-key semantics,
  collection/card-performance fingerprint behavior, or non-dict entry skips.

This pass adds the smallest parser-local compatibility fix for nested
collection wildcards while preserving existing flat wildcard behavior and row
field names. It also adds focused tests for the uncovered contract guarantees.

Changed files:

- `src/mythic_edge_parser/app/sheet_exports.py`
- `tests/test_sheet_exports.py`
- `docs/implementation_handoffs/parser_sheet_exports_comparison.md`

Referenced source artifact already present in the worktree:

- `docs/contracts/parser_sheet_exports.md`

Repository hygiene note:

- `docs/contracts/parser_sheet_exports.md` was already untracked at the start of
  this pass and remains the source artifact for issue #52.
- No files were staged or committed.

## Findings First

### Resolved: nested collection wildcards were not exported

Contract requirement:

- Accepted collection payloads may provide wildcard counts as
  `inventory.wildcards.common`, `.uncommon`, `.rare`, and `.mythic`.

Initial state:

- `_collection_snapshot_row()` read only flat keys:
  `wildcards_common`, `wildcards_uncommon`, `wildcards_rare`, and
  `wildcards_mythic`.

Resolution:

- `_collection_snapshot_row()` now reads the existing flat keys first and falls
  back to the nested `inventory.wildcards` dict when flat keys are absent.
- The output row shape is unchanged: it still emits `wildcards_common`,
  `wildcards_uncommon`, `wildcards_rare`, and `wildcards_mythic`.
- A focused test now proves the nested accepted shape is exported correctly.

### Resolved: sheet export focused tests were too narrow

Contract requirement:

- Cover reset state cleanup, `_load_json_dict()` behavior, `_safe_int()`,
  disabled family flags, runtime metadata, Apps Script-compatible snake_case
  row fields, action dedupe, snapshot dedupe, non-dict list entries, and
  missing/invalid file-loaded payloads.

Initial state:

- Existing tests covered boolean `_safe_int()` handling, one-pass family
  emission, repeated export suppression for broad snapshots, parser-status
  transient/core changes, and deck `generated_at` transient behavior.

Resolution:

- Added focused tests for the missing contract guarantees in
  `tests/test_sheet_exports.py`.
- No schema constants or Apps Script mappings were changed.

## Confirmed Matches

- `collect_runtime_sheet_rows()` remains the public runtime sheet row
  collection API.
- Returned rows are dictionaries with `event_family`, `event_type`, and `scope`
  metadata sourced from `sheet_schema.runtime_sheet_spec()`.
- Emitted family order remains Action Log, Deck Snapshot, Collection Snapshot,
  Parser Status, Card Performance.
- Family flags gate row emission and default artifact loading.
- `_safe_int()` blanks booleans and invalid values, while preserving Python
  `int()` behavior for valid ints, numeric strings, and floats.
- `_load_json_dict()` returns `{}` for missing files, invalid JSON, and non-dict
  top-level JSON.
- `_load_json_dict()` reuses cached successful loads for unchanged cache keys
  and refreshes when the cache key changes.
- `reset_sheet_export_state()` clears posted action keys, snapshot
  fingerprints, and JSON cache state.
- Action rows dedupe on the documented key fields and ignore documented
  non-key fields.
- Non-dict entries in accepted Action Log, Deck Snapshot, and Card Performance
  lists are skipped.
- Deck, Collection, Parser Status, and Card Performance snapshot dedupe remains
  process-local and fingerprint-based.
- Deck, Collection, and Card Performance dedupe ignores `generated_at`.
- Parser Status dedupe ignores the documented transient fields and re-emits
  when core context changes.
- Each runtime row family emits the snake_case fields consumed by Apps Script.
- `mulligan_tax` remains the Card Performance row field.
- No parser state final reconciliation, schema constants, Apps Script mappings,
  webhook payload field names, output transport behavior, secrets,
  environment variables, raw logs, runtime status files, failed posts, or
  workbook exports were changed.

## Contract Mismatches

No unresolved implementation mismatch is known after this pass.

Resolved mismatch:

- Collection Snapshot rows now support the contract-accepted nested
  `inventory.wildcards` payload shape without changing existing flat-key
  behavior or workbook-facing row field names.

## Missing Safeguards

No blocking missing safeguard remains in the reviewed sheet export scope.

Safeguards added or strengthened:

- Focused tests verify disabled export flags do not load default artifacts.
- Focused tests verify emitted row metadata and row field names stay within the
  contract.
- Focused tests verify Apps Script-consumed snake_case keys are covered by
  emitted rows.
- Focused tests verify reset state cleanup includes JSON cache state.

Behavior deliberately left unchanged:

- All-blank action-key behavior remains as observed by the contract.
- Truthy non-dict top-level direct payload overrides remain outside the accepted
  direct-input shape.
- Snapshot dedupe remains ordered-list sensitive.
- Mtime-keyed cache invalidation remains unchanged.
- The module still does not validate workbook tabs or execute Apps Script.

## Missing Or Weak Tests

Blocking focused test gaps from the contract were addressed.

Remaining non-blocking gaps:

- Tests parse Apps Script source text for consumed `data` keys but do not
  execute Apps Script.
- Tests do not inspect a live workbook.
- Tests do not exercise live webhook delivery.
- Tests do not force same-mtime content changes through the real filesystem;
  cache reuse/refresh is verified through the module cache key boundary.
- Tests do not intentionally change the all-blank action-key behavior because
  the contract calls that a future loopback candidate, not a Codex C fix.

## Validation Evidence

Commands run:

```bash
git diff --check -- docs/contracts/parser_sheet_exports.md
```

Result: passed with no output.

```bash
python -m pytest -q tests/test_sheet_exports.py
```

Result:

```text
16 passed in 0.16s
```

```bash
python -m pytest -q tests/test_sheet_exports.py tests/test_analytics_sidecar.py
```

Result:

```text
21 passed in 0.23s
```

```bash
python -m pytest -q tests/test_sheet_schema.py tests/test_runtime_surfaces.py tests/test_app_outputs.py
```

Result:

```text
53 passed in 0.23s
```

```bash
python -m pytest -q tests/test_runner.py tests/test_app_outputs.py
```

Result:

```text
37 passed in 0.31s
```

```bash
python -m ruff check src tests
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

- The nested wildcard compatibility fix is sheet-export local and does not
  change workbook schema, Apps Script mappings, or row field names.
- Existing flat wildcard behavior remains intact.
- Export flags prevent disabled default artifact loading and row emission.
- Emitted row metadata still comes from `sheet_schema.runtime_sheet_spec()`.
- Every emitted row family keeps the Apps Script-compatible snake_case keys.
- Duplicate suppression remains process-local export behavior only.
- No parser-owned truth moved into workbook formulas, dashboard logic, Apps
  Script, webhook delivery, output transport, or AI-generated interpretation.

## Next Workflow Action

Next role: Codex E: Module Reviewer

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #52:
https://github.com/Tahjali11/Mythic-Edge/issues/52

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_sheet_exports.md
- docs/implementation_handoffs/parser_sheet_exports_comparison.md
- src/mythic_edge_parser/app/sheet_exports.py
- tests/test_sheet_exports.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_sheet_schema.py
- src/mythic_edge_parser/app/analytics_sidecar.py
- tests/test_analytics_sidecar.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/card_performance.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_runtime_surfaces.py
- src/mythic_edge_parser/app/outputs.py
- tests/test_app_outputs.py
- src/mythic_edge_parser/app/runner.py
- tests/test_runner.py
- tools/google_apps_script/Code.gs
- any directly referenced export-adjacent files or focused tests named by the contract

Goal:
Verify the Module Implementer changes against the parser sheet exports contract.

Confirm:
- sheet_exports.py remains the runtime workbook export row builder and does not post webhooks, write workbooks, mutate parser state, or own parser truth.
- Collection Snapshot exports support the contract-accepted nested inventory.wildcards payload shape while preserving existing flat wildcard keys and emitted row field names.
- collect_runtime_sheet_rows() remains the public collection API and returns families in the documented order.
- Family flags prevent disabled default artifact loading and row emission.
- Every emitted family includes event_family, event_type, and scope sourced from sheet_schema.py.
- Each row family emits the snake_case fields consumed by Apps Script.
- _safe_int() blanks booleans and invalid values while preserving current int() conversion behavior.
- _load_json_dict() handles missing files, invalid JSON, non-dict JSON, cache reuse, and cache refresh.
- reset_sheet_export_state() clears fingerprints, posted action keys, and JSON cache state.
- Action row dedupe uses the documented key fields and ignores documented non-key fields.
- Snapshot row dedupe ignores only documented transient keys and re-emits on non-transient changes.
- Non-dict entries in accepted list sections are skipped.
- No parser behavior outside sheet export contract requirements changed.
- No parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.
- Schema constants and Apps Script mappings were not changed.
- Parser-owned truth was not moved into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation.

Validation:
Run:
git diff --check -- docs/contracts/parser_sheet_exports.md
python -m pytest -q tests/test_sheet_exports.py
python -m pytest -q tests/test_sheet_exports.py tests/test_analytics_sidecar.py
python -m ruff check src tests
git diff --check

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior outside sheet export contract requirements.
Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration.
Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation.
Do not stage, commit, merge, target main, or mark tracker #5 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/52"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_sheet_exports.md"
  target_artifact: "docs/implementation_handoffs/parser_sheet_exports_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check -- docs/contracts/parser_sheet_exports.md"
    - "python -m pytest -q tests/test_sheet_exports.py"
    - "python -m pytest -q tests/test_sheet_exports.py tests/test_analytics_sidecar.py"
    - "python -m pytest -q tests/test_sheet_schema.py tests/test_runtime_surfaces.py tests/test_app_outputs.py"
    - "python -m pytest -q tests/test_runner.py tests/test_app_outputs.py"
    - "python -m ruff check src tests"
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior outside sheet export contract requirements."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation."
    - "Do not target main for module PR work."
    - "Do not mark tracker #5 complete."
```
