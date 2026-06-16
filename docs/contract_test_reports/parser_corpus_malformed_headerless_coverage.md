# Parser Corpus Malformed Headerless Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/372
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/370
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/371
- previous_merge_commit: `4dac867bd22fbb8465c9c8c44b250d129f653121`
- contract:
  `docs/contracts/parser_corpus_malformed_headerless_coverage.md`
- branch: `codex/parser-corpus-malformed-headerless-coverage`
- base_branch: `codex/parser-parity`
- report_lifecycle: final_approval
- risk_tier: High

## Source Snapshot

PR #371 is present in the local branch:

- required merge commit:
  `4dac867bd22fbb8465c9c8c44b250d129f653121`
- local HEAD before implementation:
  `4dac867bd22fbb8465c9c8c44b250d129f653121`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 9
- covered_report_only: 0
- partial: 3
- missing: 21
- blocked_external_boundary: 6

Pre-change log/runtime rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `log_runtime.detailed_logs_disabled` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `detailed_logs_disabled_synthetic_v1` |
| `log_runtime.timestamp_anomaly` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `timestamp_anomaly_synthetic_v1` |
| `log_runtime.rotation` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `log_runtime.malformed_or_headerless` | `missing` | `external_reference_only` | none |
| `log_runtime.unknown_entry` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single synthetic metadata path authorized by the contract:

- manifest entry: `malformed_headerless_synthetic_v1`
- session ledger entry: `malformed_headerless_synthetic_v1`
- scenario family: `log_runtime.malformed_or_headerless`
- coverage status: `covered_synthetic`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`
- parser event families: none
- parser claim families:
  - `line_buffer_header_classification`
  - `line_buffer_headerless_orphan_noise_ignored`
  - `line_buffer_unknown_header_boundary`
  - `line_buffer_partial_line_boundary`
  - `line_buffer_multiline_boundary`
  - `malformed_headerless_privacy_boundary`

The synthetic entry ties existing `LineBuffer`, `EntryHeader`, and focused
header-boundary tests into the corpus coverage row. It does not add raw log
fixtures, private runtime reports, local app-data contents, external corpus
material, or parser source changes.

## Focused Line-Buffer Evidence

Existing focused line-buffer tests verify:

- known header classification and clean single-line `LogEntry` emission;
- orphan/headerless noise ignored when no entry is open;
- unknown bracketed headers emitted as `EntryHeader.UNKNOWN`;
- partial single-line fragments joined before emission or finalized on
  `flush()`;
- multiline entries finalized before the next header;
- committed line-buffer corpus slices produce clean entry bodies without
  orphan noise leaking into single-line entries.

This implementation did not change line-buffer source or line-buffer tests.
The new corpus metadata uses those tests only as parser behavior evidence for
the narrow `log_runtime.malformed_or_headerless` family.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 10
- covered_report_only: 0
- partial: 3
- missing: 20
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

Post-change log/runtime rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `log_runtime.detailed_logs_disabled` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `detailed_logs_disabled_synthetic_v1` |
| `log_runtime.timestamp_anomaly` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `timestamp_anomaly_synthetic_v1` |
| `log_runtime.rotation` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `log_runtime.malformed_or_headerless` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `malformed_headerless_synthetic_v1` |
| `log_runtime.unknown_entry` | `missing` | `external_reference_only` | none |

The malformed/headerless row includes this non-claim note:

```text
Synthetic malformed/headerless coverage proves line-buffer and header-boundary metadata only; it does not prove unknown-entry routing, log drift detection, log rotation, semantic recovery from arbitrary malformed Player.log payloads, private smoke, release readiness, analytics truth, AI truth, coaching truth, or production behavior.
```

## Privacy And Protected-Surface Assertions

- No parser source behavior changed.
- No `LineBuffer` behavior, header classification behavior, tailer behavior,
  router semantics, parser event class, parser state final reconciliation,
  diagnostics report shape, log drift behavior, golden replay behavior,
  feature-equity behavior, runtime status schema, match/game identity,
  deduplication, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets sync, output transport, runtime artifact, failed delivery
  artifact, workbook export, local app behavior, analytics truth, AI truth,
  coaching behavior, CI gate, merge policy, deploy policy, or production
  surface changed.
- No raw log fixture, private Player.log excerpt, private smoke output, actual
  malformed-log runtime report, local app-data content, local path, golden
  replay fixture, feature-equity baseline, runtime artifact, workbook export,
  generated/private artifact, external corpus content, or credential was
  added.
- The synthetic session entry records no raw log lines, raw entry bodies,
  private paths, raw payloads, external logs, decklists, private machine
  identifiers, account identifiers, IP/network traces, or private report
  locations.

## Explicit Non-Claims

- This report does not claim unknown-entry routing coverage.
- This report does not claim log drift detection coverage.
- This report does not claim log rotation support.
- This report does not claim semantic recovery from arbitrary malformed
  Player.log payloads.
- This report does not redefine issue #368 detailed logs disabled coverage.
- This report does not redefine issue #370 timestamp anomaly coverage.
- This report does not claim private smoke success, release readiness,
  production reliability, diagnostics truth, analytics truth, AI truth, or
  coaching truth.
- This report does not claim full Mythic Edge corpus parity or full
  log-runtime parity.
- This report does not decide merge readiness, deploy readiness,
  public/private-release readiness, issue closure, or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md`

## Next Recommended Role

Codex E: Module Reviewer.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

No contract mismatches were found. No missing focused tests or safeguards were
identified for the contracted metadata-only coverage slice.

Validation caveat: the literal contract-suggested secret/private-marker scan
that includes unchanged `tests/test_log_entry_headers.py`,
`tests/test_entry_buffer_edges.py`, and `tests/test_line_buffer_corpus.py`
reproduces pre-existing `raw_player_log_content` findings in those unchanged
line-buffer evidence tests. The six-file changed-package scan passes with 0
forbidden findings and 0 warnings.

### Contract-Test Verdict

Pass. The package is ready for Codex F: Module Submitter.

The implementation matches the contracted V1 synthetic metadata slice:

- only `log_runtime.malformed_or_headerless` moved from `missing` to
  `covered_synthetic`;
- `log_runtime.detailed_logs_disabled` remains `covered_synthetic` through
  issue #368 and `detailed_logs_disabled_synthetic_v1`;
- `log_runtime.timestamp_anomaly` remains `covered_synthetic` through issue
  #370 and `timestamp_anomaly_synthetic_v1`;
- `log_runtime.rotation` remains `blocked_external_boundary`;
- `log_runtime.unknown_entry` remains `missing`;
- `connection.connection_error_payload` remains `covered_synthetic` through
  issue #364 and `connection_error_payload_synthetic_v1`;
- `connection.disconnect` remains `covered_synthetic` through issue #366 and
  `connection_disconnect_synthetic_v1`;
- `connection.reconnect` remains `blocked_external_boundary`;
- `connection.firewall_or_network_drop` remains `missing`;
- `malformed_headerless_synthetic_v1` exists in both the corpus manifest and
  session ledger;
- the manifest entry has `parser_event_families: []` by design;
- the session-ledger entry records synthetic line-buffer summary counts only;
- evidence remains grounded in existing LineBuffer and header-boundary behavior,
  not router unknown-entry stats, diagnostics, drift reports, golden replay,
  feature-equity reports, private Player.log checks, or live runtime reports;
- no line-buffer behavior, header classification, tailer behavior, parser
  behavior, router semantics, parser events, or protected downstream surfaces
  changed;
- no raw/private/external logs, private runtime reports, local app-data
  contents, local paths, runtime artifacts, private reports, credentials,
  webhook URLs, or raw payload dumps are committed.

### Validation Results

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 20 missing)`

```bash
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from mythic_edge_parser.app.corpus_parity_report import build_corpus_parity_report
report = build_corpus_parity_report(
    Path("tests/fixtures/parser_corpus/corpus_manifest.v1.json"),
    session_ledger_path=Path("tests/fixtures/parser_corpus/session_ledger.v1.json"),
)
print(report["status"])
print(report["summary"])
PY
```

- passed: status `partial_coverage_map_ready`; summary shows 45 families, 6
  committed, 10 synthetic, 20 missing, 6 blocked external boundary.

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_line_buffer_corpus.py
```

- passed: 20 passed

```bash
python3 -m pytest -q tests/test_tailer_router_integration.py
```

- passed: 1 passed

```bash
python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
python3 tools/check_agent_docs.py
```

- passed: errors 0, warnings 0

```bash
git diff --check
```

- passed with no output

```bash
printf '%s\n' docs/contracts/parser_corpus_malformed_headerless_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_malformed_headerless_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_malformed_headerless_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: `selection_status: ok`

```bash
python3 -m pytest -q
```

- passed: 1767 passed

### Protected-Surface Status

No protected parser/runtime/downstream surfaces changed. The reviewed package
is limited to:

- `docs/contracts/parser_corpus_malformed_headerless_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md`

Live GitHub check during review confirmed:

- issue #372 is open;
- tracker #158 is open;
- issue #370 is closed;
- PR #371 is merged into `codex/parser-parity` with merge commit
  `4dac867bd22fbb8465c9c8c44b250d129f653121`.

Local source-surface check showed no changes under `src`, `tools`, `.github`,
`main.py`, or `live_print_filtered_v11_match_summary.py`.

### Remaining Risks

- This is synthetic entry-boundary metadata only, not private Player.log smoke
  evidence or live MTGA runtime proof.
- It does not cover unknown-entry routing, log drift detection, log rotation,
  semantic recovery from arbitrary malformed Player.log payloads, release
  readiness, analytics truth, AI truth, coaching truth, or production behavior.
- The pre-existing raw-log-shaped synthetic strings in unchanged line-buffer
  tests still trip the literal secret/private-marker scan when those files are
  included by path; this slice did not change those tests.

### Next Recommended Role

Codex F: Module Submitter.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/372"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/370"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/371"
  previous_merge_commit: "4dac867bd22fbb8465c9c8c44b250d129f653121"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md"
  target_artifact: "draft PR for synthetic malformed/headerless coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-malformed-headerless-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_line_buffer_corpus.py"
    - "python3 -m pytest -q tests/test_tailer_router_integration.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan for the six reviewed files"
    - "path-scoped protected-surface check for the six reviewed files"
    - "path-scoped validation selector check for the six reviewed files"
    - "python3 -m pytest -q"
  validation_caveat:
    - "The literal contract-suggested secret/private-marker scan including unchanged tests/test_log_entry_headers.py, tests/test_entry_buffer_edges.py, and tests/test_line_buffer_corpus.py fails on pre-existing raw_player_log_content findings in those unchanged line-buffer evidence files; the six-file changed-package scan passes cleanly."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #372 or tracker #158."
    - "Do not change LineBuffer behavior, header classification behavior, tailer behavior, parser behavior, timestamp parsing behavior, router semantics, parser state final reconciliation, parser event classes, diagnostics behavior, drift sensor behavior, golden replay behavior, feature-equity behavior, runtime status behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge/deploy policy, release readiness, production behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed-delivery artifacts, workbook exports, or local runtime artifacts."
    - "Do not invent a malformed/headerless parser event or event family; this coverage is entry-boundary evidence."
    - "Do not move log_runtime.unknown_entry or log_runtime.rotation to covered status."
    - "Do not redefine issue #368 detailed logs disabled coverage or issue #370 timestamp anomaly coverage."
    - "Do not use router unknown-entry stats, diagnostics, drift reports, golden replay, feature-equity reports, private Player.log checks, or live runtime reports as the sole coverage basis."
    - "Do not import, copy, mirror, or commit external/raw/private logs, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, parser source, malformed-log runtime reports, local app-data contents, local paths, private reports, credentials, tokens, API keys, webhook URLs, Manasight raw logs, external raw corpus contents, or private strategy notes."
    - "Do not claim full Mythic Edge corpus parity, full log-runtime parity, unknown-entry routing, log drift detection, log rotation support, semantic recovery from arbitrary malformed Player.log payloads, private-smoke readiness, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
```
