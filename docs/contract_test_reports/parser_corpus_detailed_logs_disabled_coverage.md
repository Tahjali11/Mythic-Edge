# Parser Corpus Detailed Logs Disabled Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/368
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/366
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/367
- previous_merge_commit: `d3a98f01d2fe048340489009ad703149e1fc30ef`
- contract:
  `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`
- branch: `codex/parser-corpus-detailed-logs-disabled-coverage`
- base_branch: `codex/parser-parity`
- report_lifecycle: final_approval
- risk_tier: High

## Source Snapshot

PR #367 is present in the local branch:

- required merge commit:
  `d3a98f01d2fe048340489009ad703149e1fc30ef`
- local HEAD before implementation:
  `d3a98f01d2fe048340489009ad703149e1fc30ef`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 7
- covered_report_only: 0
- partial: 3
- missing: 23
- blocked_external_boundary: 6

Pre-change log/runtime rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `log_runtime.detailed_logs_disabled` | `missing` | `external_reference_only` | none |
| `log_runtime.rotation` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `log_runtime.malformed_or_headerless` | `missing` | `external_reference_only` | none |
| `log_runtime.timestamp_anomaly` | `missing` | `external_reference_only` | none |
| `log_runtime.unknown_entry` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single synthetic metadata path authorized by the contract:

- manifest entry: `detailed_logs_disabled_synthetic_v1`
- session ledger entry: `detailed_logs_disabled_synthetic_v1`
- scenario family: `log_runtime.detailed_logs_disabled`
- coverage status: `covered_synthetic`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`
- parser evidence family:
  - `DetailedLoggingStatus`
- parser claim families:
  - `detailed_logging_status_event`
  - `detailed_logs_disabled_marker`
  - `detailed_logging_metadata_parser`
  - `detailed_logging_privacy_boundary`

The synthetic entry ties existing parser behavior for explicit
`DETAILED LOGS: DISABLED` metadata handling into the corpus coverage row. It
does not add raw log fixtures, private settings evidence, local app-data
contents, runtime artifacts, external corpus material, or parser source
changes.

## Focused Parser Evidence

Existing focused parser tests verify:

- metadata parser emits `DetailedLoggingStatus` for `DETAILED LOGS: DISABLED`;
- disabled status produces payload `{"enabled": False}`;
- enabled status remains covered separately as parser behavior context;
- metadata parser preserves event kind and payload semantics;
- router, log-entry/header, tailer/router integration, and schema snapshot
  tests exercise adjacent dispatch and event shape behavior.

This implementation did not change those parser tests or parser source. The
new corpus metadata uses them only as parser behavior evidence for the narrow
`log_runtime.detailed_logs_disabled` family.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 8
- covered_report_only: 0
- partial: 3
- missing: 22
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

Post-change log/runtime rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `log_runtime.detailed_logs_disabled` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `detailed_logs_disabled_synthetic_v1` |
| `log_runtime.rotation` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `log_runtime.malformed_or_headerless` | `missing` | `external_reference_only` | none |
| `log_runtime.timestamp_anomaly` | `missing` | `external_reference_only` | none |
| `log_runtime.unknown_entry` | `missing` | `external_reference_only` | none |

The detailed logs disabled row includes this non-claim note:

```text
Synthetic detailed logs disabled coverage proves parser-owned DetailedLoggingStatus metadata only; it does not prove live MTGA settings, log rotation, malformed/headerless log handling, timestamp anomaly handling, unknown-entry routing, private smoke, release readiness, analytics truth, AI truth, coaching truth, or production behavior.
```

## Privacy And Protected-Surface Assertions

- No parser source behavior changed.
- No line-buffer/header classification behavior, stream/tailer behavior,
  parser event class, router, parser state final reconciliation, diagnostics
  report shape, runtime status schema, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, runtime artifact, failed delivery artifact, workbook
  export, local app behavior, analytics truth, AI truth, coaching behavior, CI
  gate, merge policy, deploy policy, or production surface changed.
- No raw log fixture, private Player.log excerpt, private smoke output,
  actual MTGA settings dump, local app-data content, local path, golden replay
  fixture, feature-equity baseline, runtime artifact, workbook export,
  generated/private artifact, external corpus content, or credential was
  added.
- The synthetic session entry records no raw log lines, private paths, raw
  payloads, external logs, decklists, private machine identifiers, account
  identifiers, settings paths, strategy notes, or private report locations.

## Explicit Non-Claims

- This report does not claim live MTGA settings truth.
- This report does not claim log rotation coverage.
- This report does not claim malformed/headerless log coverage.
- This report does not claim timestamp anomaly coverage.
- This report does not claim unknown-entry coverage.
- This report does not redefine issue #364 connection error payload coverage.
- This report does not redefine issue #366 connection disconnect coverage.
- This report does not claim private smoke success, release readiness,
  production reliability, diagnostics truth, analytics truth, AI truth, or
  coaching truth.
- This report does not claim full Mythic Edge corpus parity.
- This report does not decide merge readiness, deploy readiness,
  public/private-release readiness, issue closure, or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md`

## Next Recommended Role

Codex E: Module Reviewer.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

No contract mismatches, missing focused tests, privacy leaks,
protected-surface drift, parser behavior changes, metadata parser changes,
line-buffer/header classification changes, router changes, event-class
changes, stream/tailer behavior changes, diagnostics/runtime-status behavior
changes, or adjacent log-runtime/connection coverage overclaims were found in
the reviewed package.

Validation caveat: the literal contract-suggested secret/private-marker scan
that includes unchanged parser evidence files reproduces pre-existing
`raw_player_log_content` findings in `tests/test_parser_small_modules.py` and
`tests/test_parsers.py`. Those files are not changed by this package. The
path-scoped scan over the six changed implementation/report files passes with
0 forbidden findings and 0 warnings.

### Contract-Test Verdict

Pass. The package is ready for Codex F: Module Submitter.

The implementation matches the contracted V1 synthetic metadata slice:

- only `log_runtime.detailed_logs_disabled` moved from `missing` to
  `covered_synthetic`;
- `log_runtime.rotation` remains `blocked_external_boundary`;
- `log_runtime.malformed_or_headerless` remains `missing`;
- `log_runtime.timestamp_anomaly` remains `missing`;
- `log_runtime.unknown_entry` remains `missing`;
- `connection.connection_error_payload` remains `covered_synthetic` through
  issue #364 and `connection_error_payload_synthetic_v1`;
- `connection.disconnect` remains `covered_synthetic` through issue #366 and
  `connection_disconnect_synthetic_v1`;
- `connection.reconnect` remains `blocked_external_boundary`;
- `connection.firewall_or_network_drop` remains `missing`;
- `detailed_logs_disabled_synthetic_v1` exists in both the corpus manifest and
  session ledger;
- the manifest/session entry is synthetic, committed, privacy-safe metadata;
- existing focused parser tests prove explicit `DETAILED LOGS: DISABLED`
  parser behavior and are used as behavior evidence without changing parser
  source or parser tests;
- corpus report notes explicitly preserve live-settings, log-rotation,
  malformed/headerless-log, timestamp-anomaly, unknown-entry, private-smoke,
  release-readiness, analytics, AI, coaching, and production non-claims;
- no raw/private/external logs, private settings dumps, local app-data
  contents, local paths, runtime artifacts, private reports, credentials,
  webhook URLs, or raw payload dumps are committed;
- no parser source, metadata parser, line-buffer/header classification, parser
  event classes, router, stream/tailer, diagnostics, runtime status, workbook,
  webhook, Apps Script, output, analytics, AI, local app, CI, merge, deploy,
  release, or production surface changed.

### Validation Results

Live workflow state was verified:

- issue #368: open;
- tracker #158: open;
- previous issue #366: closed;
- previous PR #367: merged into `codex/parser-parity`;
- previous merge commit `d3a98f01d2fe048340489009ad703149e1fc30ef`:
  present in local ancestry;
- current branch: `codex/parser-corpus-detailed-logs-disabled-coverage`;
- base branch: `origin/codex/parser-parity`.

Commands run by Codex E:

- `git status --short --branch` -> expected branch and tracked/untracked
  review package only.
- `git diff -- tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py`
  -> tracked diff limited to manifest, session ledger, and focused corpus
  parity tests.
- `git log --oneline -8 --decorate` and `git rev-parse HEAD` -> local HEAD is
  `d3a98f01d2fe048340489009ad703149e1fc30ef`.
- `git merge-base --is-ancestor d3a98f01d2fe048340489009ad703149e1fc30ef HEAD`
  -> passed.
- `gh issue view 368 --repo Tahjali11/Mythic-Edge --json number,title,state,url,labels`
  -> issue #368 is open.
- `gh issue view 158 --repo Tahjali11/Mythic-Edge --json number,title,state,url`
  -> tracker #158 is open.
- `gh issue view 366 --repo Tahjali11/Mythic-Edge --json number,title,state,url`
  -> previous issue #366 is closed.
- `gh pr view 367 --repo Tahjali11/Mythic-Edge --json number,title,state,isDraft,baseRefName,headRefName,mergeCommit,url`
  -> PR #367 is merged into `codex/parser-parity` with merge commit
  `d3a98f01d2fe048340489009ad703149e1fc30ef`.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  -> `partial_coverage_map_ready` with 45 families, 6 committed, and 22
  missing.
- Direct `build_corpus_parity_report(...)` row inspection confirmed:
  `log_runtime.detailed_logs_disabled` is `covered_synthetic`;
  `log_runtime.rotation` remains `blocked_external_boundary`;
  `log_runtime.malformed_or_headerless`, `log_runtime.timestamp_anomaly`, and
  `log_runtime.unknown_entry` remain `missing`;
  `connection.connection_error_payload` and `connection.disconnect` remain
  `covered_synthetic`;
  `connection.reconnect` remains `blocked_external_boundary`; and
  `connection.firewall_or_network_drop` remains `missing`.
- `python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_parser_small_modules.py tests/test_parsers.py`
  -> 51 passed.
- `python3 -m pytest -q tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_event_schema_snapshots.py tests/test_tailer_router_integration.py`
  -> 34 passed.
- `python3 -m pytest -q tests/test_stream_integration.py` -> 3 passed.
- `python3 -m ruff check src tests tools` -> all checks passed.
- `python3 tools/check_agent_docs.py` -> passed with 0 errors and 0 warnings.
- `git diff --check` -> passed with no output.
- Path-scoped `python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin`
  over the six reviewed files -> passed with 0 forbidden and 0 warnings.
- Path-scoped `python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin`
  over the six reviewed files -> passed with 0 forbidden and 0 warnings.
- Path-scoped `python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin`
  over the six reviewed files -> `selection_status: ok`.
- Literal contract-suggested `python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin`
  including unchanged `tests/test_parser_small_modules.py` and
  `tests/test_parsers.py` -> failed with 56 pre-existing
  `raw_player_log_content` findings in those unchanged parser evidence files.
- Literal contract-suggested `python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin`
  including unchanged parser evidence files -> passed with 0 forbidden and 0
  warnings.
- Literal contract-suggested `python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin`
  including unchanged parser evidence files -> `selection_status: ok`.
- `git diff --no-index --check /dev/null <untracked-report-doc>` for the
  three new docs -> no whitespace output.
- `git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py .github`
  -> no output.
- `python3 -m pytest -q` -> 1767 passed.

### Protected-Surface Status

Changed tracked diff is limited to:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`

New untracked review artifacts:

- `docs/contracts/parser_corpus_detailed_logs_disabled_coverage.md`
- `docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md`
- `docs/implementation_handoffs/parser_corpus_detailed_logs_disabled_coverage_comparison.md`

No `src`, `tools`, `.github`, parser source, metadata parser, line-buffer,
parser event class, router, stream/tailer, diagnostics, runtime status,
workbook, webhook, Apps Script, analytics, AI, CI, local app, generated data,
failed-delivery, workbook-export, release, or production files are changed by
this package.

### Remaining Non-Blocking Gaps

- This remains synthetic metadata coverage, not replayed private Player.log
  coverage.
- Parser-owned `DetailedLoggingStatus` metadata is narrower than live MTGA
  settings truth or local runtime readiness.
- Log rotation, malformed/headerless logs, timestamp anomalies, unknown-entry
  routing, private smoke, runtime-health, diagnostics, and release-readiness
  evidence remain future contract work.
- Corpus coverage remains review metadata and does not become parser truth,
  runtime truth, diagnostics truth, workbook truth, analytics truth, AI truth,
  readiness, deploy, release, or tracker authority.

### Next Recommended Role

Codex F: Module Submitter.

Codex F should stage only the six reviewed files and submit this package
toward `codex/parser-parity`. Codex F must not target `main` directly, close
issue #368, close tracker #158, or widen the scope.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/368"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/366"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/367"
  previous_merge_commit: "d3a98f01d2fe048340489009ad703149e1fc30ef"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_detailed_logs_disabled_coverage.md"
  target_artifact: "draft PR for synthetic detailed logs disabled coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-detailed-logs-disabled-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_parser_small_modules.py tests/test_parsers.py"
    - "python3 -m pytest -q tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_event_schema_snapshots.py tests/test_tailer_router_integration.py"
    - "python3 -m pytest -q tests/test_stream_integration.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan for the six reviewed files"
    - "path-scoped protected-surface check for the six reviewed files"
    - "path-scoped validation selector check for the six reviewed files"
    - "python3 -m pytest -q"
  validation_caveat:
    - "The literal contract-suggested secret/private-marker scan including unchanged tests/test_parser_small_modules.py and tests/test_parsers.py fails on pre-existing raw_player_log_content findings in those unchanged parser evidence files; the six-file changed-package scan passes cleanly."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #368 or tracker #158."
    - "Do not change parser behavior, metadata parser marker matching, line-buffer/header classification, parser state final reconciliation, parser event classes, router semantics, stream/tailer behavior, diagnostics behavior, runtime status behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge/deploy policy, release readiness, production behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed-delivery artifacts, workbook exports, or local runtime artifacts."
    - "Do not move log_runtime.rotation to covered status."
    - "Do not move log_runtime.malformed_or_headerless, log_runtime.timestamp_anomaly, or log_runtime.unknown_entry to covered status."
    - "Do not redefine issue #364 connection error payload coverage or issue #366 connection disconnect coverage."
    - "Do not import, copy, mirror, or commit external/raw/private logs, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, parser source, MTGA settings dumps, local app-data contents, local paths, private reports, credentials, tokens, API keys, webhook URLs, or private strategy notes."
    - "Do not claim full Mythic Edge corpus parity, full log-runtime parity, live settings truth, log-rotation coverage, malformed/headerless-log coverage, timestamp-anomaly coverage, unknown-entry routing coverage, private-smoke readiness, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
```
