# Parser Evidence UTC_Log Source Adapter Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/381

## Tracker

- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434

## Contract

`docs/contracts/parser_evidence_utc_log_source_adapter.md`

## Internal Project Area

Corpus / Provenance, with Parser support.

## Truth Owner

The adapter owns only source-format normalization metadata for synthetic
UTC_Log-style text. Existing parser entry/header/replay code remains the truth
owner for parser interpretation.

## Bridge-Code Status

`bridge_code`

The implementation bridges synthetic UTC_Log-style source text into
Player.log-equivalent text for existing parser paths. It does not parse events,
emit events, create fixtures, promote corpus rows, or read private/local logs.

## Role Performed

Codex C: Module Implementer.

## What Changed

- Added a small UTC_Log source adapter module.
- Added synthetic-only tests for UTC frame-prefix stripping, line-ending
  normalization, content/order preservation, existing `LineBuffer`
  compatibility, malformed synthetic warnings, and fail-closed private/local
  source behavior.
- Preserved existing parser/log/stream behavior without edits.
- Wrote this implementation handoff for Codex E review.

## Files Changed

- `src/mythic_edge_parser/app/utc_log_source_adapter.py`
- `tests/test_utc_log_source_adapter.py`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/implementation_handoffs/parser_evidence_utc_log_source_adapter_comparison.md`

## Code Changed

Runtime support code was added under
`src/mythic_edge_parser/app/utc_log_source_adapter.py`.

The module exposes:

- `UtcLogCandidate`
- `UtcLogNormalizationStats`
- `UtcLogNormalizationResult`
- `UtcLogSourceAccessError`
- `normalize_utc_log_text(...)`
- `describe_user_selected_utc_log_candidate(...)`

`normalize_utc_log_text(...)` accepts only synthetic source text by default and
returns Player.log-equivalent text plus normalization stats. It strips only the
existing parser-owned UTC frame-prefix shape, `^\[\d+\]\s+`, and normalizes
line endings to `\n`.

`describe_user_selected_utc_log_candidate(...)` fails closed and performs no
private/local metadata read.

## Tests Added Or Updated

- Added `tests/test_utc_log_source_adapter.py`.
- No existing parser, stream, or log-entry tests were changed.

## Interface Changes

No CLI, environment variable, local app route, runtime status field, workbook
field, webhook field, corpus manifest field, session-ledger field, fixture
format, parser event class, parser state contract, or parser route changed.

The new Python API is local support code for future evidence-pipeline work.

## Contracted Area Status

The implementation stayed within the contracted area. It did not read private
`Player.log`, private `UTC_Log`, app-data, live MTGA, network, firewall/drop,
packet, OS/router, private smoke, local offset windows, or private reports.

The adapter treats `UTC_Log` as a source format, not parser truth and not a
second parser.

## Validation Run

```bash
python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_log_entry_headers.py
python3 -m pytest -q tests/test_entry_buffer_edges.py tests/test_stream_unit.py
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
printf '<changed paths>' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '<changed paths>' | python3 tools/select_validation.py --base origin/main --paths-from-stdin
python3 -m pytest -q tests
python3 tools/run_pyright_advisory_report.py
```

Results:

- `python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_log_entry_headers.py`
  - Passed, 12 tests.
- `python3 -m pytest -q tests/test_entry_buffer_edges.py tests/test_stream_unit.py`
  - Passed, 7 tests.
- `python3 -m ruff check src tests tools`
  - Passed.
- `python3 tools/check_agent_docs.py`
  - Passed with 34 files checked, 0 errors, 0 warnings.
- `git diff --check`
  - Passed.
- Path-scoped secret/private marker scan:
  - `printf '<changed paths>' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
  - Passed with 4 scanned paths, 0 forbidden, 0 warnings.
- Path-scoped protected-surface gate:
  - `printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
  - Passed with 4 changed paths, 0 forbidden, 0 warnings.
- Path-scoped validation selector:
  - `printf '<changed paths>' | python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  - Passed with `selection_status: ok`.
- `python3 -m pytest -q tests`
  - Passed, 1790 tests.
- `python3 tools/run_pyright_advisory_report.py`
  - Advisory non-blocking findings reported: 388 type findings, 0 local
    resolver noise, 0 tooling config blockers.

The path-scoped forms were used for secret/private, protected-surface, and
selector checks because the implementation files are currently untracked in
this local worktree; plain `--base origin/main` reports zero changed paths
until files are staged or otherwise included in git diff output.

## Still Unverified

- No private/local UTC_Log source was read, normalized, discovered, hashed,
  copied, or summarized.
- No #382 harvest report path was started.
- No fixture-promotion packet, corpus metadata promotion, or private evidence
  execution was attempted.
- `parser_behavior_ready` and strict pipeline activation readiness remain
  unclaimed.

## Reviewer Focus

- Confirm the adapter strips only the contracted UTC frame prefix and preserves
  source order/content otherwise.
- Confirm private/local source operations fail closed without exact path or
  content leakage.
- Confirm tests remain synthetic-only.
- Confirm the adapter returns normalized text and metadata only, not parser
  entries/events or downstream truth.
- Confirm no protected parser/runtime/workbook/webhook/App Script surfaces were
  changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #381.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/381

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_evidence_utc_log_source_adapter.md

Implementation handoff:
docs/implementation_handoffs/parser_evidence_utc_log_source_adapter_comparison.md

Review focus:
- Verify the implementation stays synthetic-only.
- Verify UTC frame-prefix and line-ending normalization match the contract.
- Verify source line order/content is preserved except contracted
  normalization.
- Verify private/local source operations fail closed without path/content
  leakage.
- Verify the adapter does not emit parser events or become a second parser.
- Verify parser/runtime/workbook/webhook/App Script/output surfaces were not
  changed.
- Verify validation evidence and remaining non-claims are accurate.

Do not run private Player.log, UTC_Log, app-data, live MTGA, network,
firewall/drop, packet, OS/router, or private smoke checks.
Do not create fixtures, fixture-promotion packets, corpus promotions, or #382
harvest reports.
Do not claim parser_behavior_ready, strict pipeline activation readiness,
fixture-promotion readiness, release readiness, production readiness,
analytics truth, AI truth, coaching truth, or full parser regression parity.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/381"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_evidence_utc_log_source_adapter.md"
  target_artifact: "docs/implementation_handoffs/parser_evidence_utc_log_source_adapter_comparison.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_log_entry_headers.py"
    - "python3 -m pytest -q tests/test_entry_buffer_edges.py tests/test_stream_unit.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "printf '<changed paths>' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf '<changed paths>' | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
    - "python3 -m pytest -q tests"
    - "python3 tools/run_pyright_advisory_report.py"
  stop_conditions:
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, or private smoke checks."
    - "Do not implement private archive discovery or arbitrary private directory scanning."
    - "Do not print exact private paths, raw private content, raw hashes, exact offsets, or exact file sizes."
    - "Do not create committed fixtures or fixture-promotion packets."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not proceed to #382 harvest reports."
    - "Do not claim parser_behavior_ready, strict pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
