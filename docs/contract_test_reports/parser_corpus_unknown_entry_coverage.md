# Parser Corpus Unknown Entry Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/377
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/375
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/376
- previous_merge_commit: `3a0ae4598af3bcffa5170decf1e7cf816bb29c6d`
- contract: `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- branch: `codex/parser-corpus-unknown-entry-coverage`
- base_branch: `codex/parser-parity`
- report_lifecycle: final_approval
- risk_tier: High

## Source Snapshot

PR #376 is present in the local branch:

- required merge commit:
  `3a0ae4598af3bcffa5170decf1e7cf816bb29c6d`
- local HEAD before implementation:
  `3a0ae45`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 11
- covered_report_only: 0
- partial: 3
- missing: 19
- blocked_external_boundary: 6

Pre-change log-runtime rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `log_runtime.detailed_logs_disabled` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `detailed_logs_disabled_synthetic_v1` |
| `log_runtime.rotation` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `log_runtime.malformed_or_headerless` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `malformed_headerless_synthetic_v1` |
| `log_runtime.timestamp_anomaly` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `timestamp_anomaly_synthetic_v1` |
| `log_runtime.unknown_entry` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single report-only metadata path authorized by the contract:

- manifest entry: `unknown_entry_drift_report_reference_v1`
- session ledger entry: `unknown_entry_drift_report_reference_v1`
- scenario family: `log_runtime.unknown_entry`
- coverage status: `covered_report_only`
- coverage basis:
  - `diagnostics_only`
  - `fixture_metadata_only`
  - `evidence_ledger_only`
- parser event families: none
- parser claim families:
  - `router_unknown_entry_count`
  - `drift_unknown_signature_review_samples`
  - `drift_unmatched_api_name_review_samples`
  - `diagnostics_unknown_entries_review_status`
  - `evidence_ledger_unknown_entry_count_boundary`
  - `unknown_entry_privacy_boundary`

The report-only entry points to the existing normalized drift report reference
and fixture manifest. It does not point to the underlying log-like fixture
path in the parser corpus manifest, add new fixtures, edit existing drift
input fixtures, or change parser/router/diagnostics/drift behavior.

## Evidence Model

Existing focused tests prove the contracted evidence model:

- `tests/test_log_drift_sensor.py` verifies the committed normalized drift
  report reference, unknown counts, unknown signatures, unmatched API-name
  samples, no volatile keys, no local paths, and no raw log bodies.
- `tests/test_parser_diagnostics_mode.py` verifies unknown evidence drives
  diagnostics review status and redacts sensitive endpoint-like text.
- `tests/test_evidence_ledger.py` verifies Tier 6 `unknown_entry_count` is
  scoped to one analyzed input and treats unknown signatures/API names as
  review samples, not trusted parser inputs.

No drift, diagnostics, evidence-ledger, router, or parser implementation was
changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 11
- covered_report_only: 1
- partial: 3
- missing: 18
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

Post-change log-runtime rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `log_runtime.detailed_logs_disabled` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `detailed_logs_disabled_synthetic_v1` |
| `log_runtime.rotation` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `log_runtime.malformed_or_headerless` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `malformed_headerless_synthetic_v1` |
| `log_runtime.timestamp_anomaly` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `timestamp_anomaly_synthetic_v1` |
| `log_runtime.unknown_entry` | `covered_report_only` | `diagnostics_only`, `evidence_ledger_only`, `fixture_metadata_only` | `unknown_entry_drift_report_reference_v1` |

The unknown-entry row includes this non-claim note:

```text
Unknown-entry coverage proves that existing drift/diagnostics reports can surface unknown counts and review samples from a committed normalized report reference; it does not mean the parser understood the unknown entries.
```

## Privacy And Protected-Surface Assertions

- No parser source behavior changed.
- No router semantics, parser event class, parser state final reconciliation,
  diagnostics report shape, drift report behavior, evidence-ledger behavior,
  golden replay behavior, feature-equity behavior, runtime status, workbook,
  webhook, Apps Script, Google Sheets, analytics, AI, coaching, CI,
  merge/deploy policy, or production surface changed.
- No raw log fixture, private Player.log excerpt, new log-like fixture,
  modified drift input fixture, private smoke output, live diagnostics report,
  runtime artifact, workbook export, generated/private artifact, external
  corpus content, credential, token, API key, or webhook URL was added.
- The corpus manifest references the normalized drift report reference and
  fixture manifest only, not the underlying log-like fixture path.
- The session ledger records summary counts only and includes no raw log
  lines, raw entry bodies, raw payload objects, private paths, external
  corpus filenames, local diagnostics outputs, SQLite files, runtime
  artifacts, decklists, workbook exports, credentials, or live private report
  contents.

## Explicit Non-Claims

- This report does not claim parser support for unknown semantic content.
- This report does not claim new parser event kinds.
- This report does not claim automatic parser-gap issue creation.
- This report does not claim log rotation coverage.
- This report does not claim missing message type recovery.
- This report does not claim reconnect, firewall, or network-drop coverage.
- This report does not claim private-log drift health.
- This report does not claim live diagnostics readiness, private smoke
  success, release readiness, or production behavior.
- This report does not claim analytics truth, AI truth, coaching truth,
  hidden-card truth, decklist truth, archetype truth, full log-runtime parity,
  or full Mythic Edge corpus parity.
- This report does not decide merge readiness, deploy readiness,
  public/private-release readiness, issue closure, or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md`

## Next Recommended Role

Codex E: Module Reviewer.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

No contract mismatches were found. No missing focused tests or safeguards were
identified for the contracted report-only unknown-entry coverage slice.

Validation caveat: the literal contract-suggested secret/private-marker scan
that includes unchanged `tests/test_log_drift_sensor.py`,
`tests/test_parser_diagnostics_mode.py`, and `tests/test_evidence_ledger.py`
reproduces pre-existing scanner findings in those unchanged evidence tests.
The six-file changed-package scan passes with 0 forbidden findings and 0
warnings.

### Contract-Test Verdict

Pass. The package is ready for Codex F: Module Submitter.

The implementation matches the contracted report-only metadata slice:

- only `log_runtime.unknown_entry` moved from `missing` to
  `covered_report_only`;
- `covered_synthetic` remained unchanged at 11;
- `covered_report_only` increased from 0 to 1;
- `missing` decreased from 19 to 18;
- `unknown_entry_drift_report_reference_v1` exists exactly once in the corpus
  manifest and session ledger;
- the manifest entry uses `parser_event_families: []`;
- the coverage basis is `diagnostics_only`, `evidence_ledger_only`, and
  `fixture_metadata_only`;
- the corpus manifest references the normalized drift report reference and
  fixture manifest, not the underlying log-like fixture path;
- unknown entries remain drift/diagnostics review samples and do not become
  parser-understood facts or parser event families;
- adjacent log-runtime, connection, drift-debug, private-log-drift,
  live-diagnostics, analytics, AI, coaching, and release-readiness families
  were not newly covered;
- no parser behavior, router semantics, diagnostics report shape, drift report
  behavior, evidence-ledger behavior, golden replay behavior, feature-equity
  behavior, runtime, workbook, webhook, Apps Script, analytics, AI, coaching,
  CI, merge/deploy, or production surface changed;
- no raw/private/external logs, new log-like fixtures, modified drift input
  fixtures, local app-data contents, runtime artifacts, workbook exports,
  generated/private artifacts, credentials, endpoint secrets, or external
  corpus contents are committed.

### Validation Results

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
```

- passed: 15 passed

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
```

- passed: 101 passed

```bash
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 18 missing)`

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
for family in [
    "log_runtime.unknown_entry",
    "log_runtime.rotation",
    "connection.reconnect",
    "connection.firewall_or_network_drop",
    "drift_debug.missing_message_type",
    "drift_debug.rename_or_rotation_collision",
    "mythic_edge.live_diagnostics",
    "mythic_edge.private_log_report_only_drift",
]:
    row = next(row for row in report["coverage_matrix"] if row["scenario_family"] == family)
    print(family, row)
PY
```

- passed: status `partial_coverage_map_ready`; summary shows 45 families, 6
  committed, 11 synthetic, 1 report-only, 18 missing, and 6 blocked external
  boundary.
- `log_runtime.unknown_entry`: `covered_report_only` with
  `unknown_entry_drift_report_reference_v1`.
- Adjacent checked families retained their previous missing or external
  boundary statuses.

```bash
python3 -m ruff check src tests
python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
git diff --check
```

- passed with no output

```bash
python3 tools/check_agent_docs.py
```

- passed: errors 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_unknown_entry_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_unknown_entry_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_unknown_entry_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: `selection_status: ok`

```bash
python3 -m pytest -q
```

- passed: 1768 passed

### Protected-Surface Status

No protected parser/runtime/downstream surfaces changed. The reviewed package
is limited to:

- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md`

Live GitHub check during review confirmed:

- issue #377 is open;
- tracker #158 is open;
- issue #375 is closed;
- PR #376 is merged into `codex/parser-parity` with merge commit
  `3a0ae4598af3bcffa5170decf1e7cf816bb29c6d`.

Local source-surface check showed no changes under `src`, `tools`, `.github`,
`main.py`, or `live_print_filtered_v11_match_summary.py`.

### Remaining Risks

- This is report-only unknown-entry corpus coverage, not parser support for
  unknown semantic content.
- It does not cover new parser event kinds, automatic parser-gap issue
  creation, log rotation, missing-message-type recovery, reconnect,
  firewall/network-drop behavior, private-log drift health, live diagnostics
  readiness, private smoke success, release readiness, analytics truth, AI
  truth, coaching truth, production behavior, full log-runtime parity, or full
  Mythic Edge corpus parity.
- The pre-existing raw-log-shaped/runtime-status/endpoint-like strings in
  unchanged evidence tests still trip the literal secret/private-marker scan
  when those files are included by path; this slice did not change those files.

### Next Recommended Role

Codex F: Module Submitter.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/377"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/376"
  previous_merge_commit: "3a0ae4598af3bcffa5170decf1e7cf816bb29c6d"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md"
  target_artifact: "draft PR for report-only unknown-entry coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-unknown-entry-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py"
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m ruff check src tests"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped secret/private-marker scan for the six reviewed files"
    - "path-scoped protected-surface check for the six reviewed files"
    - "path-scoped validation selector check for the six reviewed files"
    - "python3 -m pytest -q"
  validation_caveat:
    - "The literal contract-suggested secret/private-marker scan including unchanged tests/test_log_drift_sensor.py, tests/test_parser_diagnostics_mode.py, and tests/test_evidence_ledger.py fails on pre-existing scanner findings in those unchanged evidence files; the six-file changed-package scan passes cleanly."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #377 or tracker #158."
    - "Do not change parser behavior, router semantics, diagnostics report shape, drift report behavior, evidence-ledger behavior, golden replay behavior, feature-equity behavior, runtime, workbook, webhook, Apps Script, analytics truth, AI truth, coaching behavior, CI gates, merge policy, deploy policy, release readiness, production behavior, secrets, environment variables, raw logs, generated data, runtime artifacts, delivery retry artifacts, workbook exports, or local private artifacts."
    - "Do not claim parser support for unknown semantic content, new parser event kinds, automatic parser-gap issue creation, live private drift health, diagnostics readiness, private smoke success, release readiness, analytics truth, AI truth, coaching truth, full log-runtime parity, or full corpus parity."
    - "Do not add new log-like fixtures, edit the existing drift input fixture, or commit raw/private/external logs, generated databases, workbook exports, credentials, tokens, API keys, endpoint secrets, or external corpus contents."
```
