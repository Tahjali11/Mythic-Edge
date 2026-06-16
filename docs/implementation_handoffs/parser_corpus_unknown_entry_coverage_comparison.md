# Parser Corpus Unknown Entry Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/377

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_unknown_entry_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`report_only_unknown_entry_coverage_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `unknown_entry_drift_report_reference_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching report-only unknown-entry drift summary metadata.
- `tests/test_corpus_parity_report.py`
  - Updated summary counts and unknown-entry row assertions.
  - Added focused checks for manifest/session shape, empty parser event
    families, report-only basis, normalized report-reference path, privacy
    flags, and adjacent non-claims.
- `docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_unknown_entry_coverage.md`

No parser source, router source, diagnostics source, drift source,
evidence-ledger source, golden replay behavior, feature-equity behavior,
runtime artifact, workbook export, generated/private artifact, raw fixture, or
external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 11
- covered_report_only: 0
- missing: 19
- `log_runtime.detailed_logs_disabled`: `covered_synthetic`
- `log_runtime.rotation`: `blocked_external_boundary`
- `log_runtime.malformed_or_headerless`: `covered_synthetic`
- `log_runtime.timestamp_anomaly`: `covered_synthetic`
- `log_runtime.unknown_entry`: `missing`

This matched the contract's expected starting state after issue #375.

## Contract Changes Implemented

Implemented exactly one authorized coverage promotion:

| Scenario family | Before | After |
| --- | --- | --- |
| `log_runtime.unknown_entry` | `missing` | `covered_report_only` |

Preserved the required adjacent-family boundary:

- `log_runtime.rotation` remains `blocked_external_boundary`.
- `connection.reconnect` remains `blocked_external_boundary`.
- `connection.firewall_or_network_drop` remains `missing`.
- `drift_debug.missing_message_type` remains unchanged.
- `drift_debug.rename_or_rotation_collision` remains unchanged.
- `mythic_edge.live_diagnostics` remains unchanged.
- `mythic_edge.private_log_report_only_drift` remains `missing`.

Added the required report-only metadata:

- entry id: `unknown_entry_drift_report_reference_v1`
- session id: `unknown_entry_drift_report_reference_v1`
- source kind: `committed_count_only_report`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- parser event families: none
- parser claim families:
  - `router_unknown_entry_count`
  - `drift_unknown_signature_review_samples`
  - `drift_unmatched_api_name_review_samples`
  - `diagnostics_unknown_entries_review_status`
  - `evidence_ledger_unknown_entry_count_boundary`
  - `unknown_entry_privacy_boundary`
- coverage basis: `diagnostics_only`, `fixture_metadata_only`,
  `evidence_ledger_only`

The corpus manifest references:

- `tests/fixtures/golden_fixture_manifest.json`
- `tests/fixtures/player_log_drift_flush_timing_expected.json`
- focused drift, diagnostics, evidence-ledger, and corpus parity tests

It intentionally does not reference the underlying log-like fixture path.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- manifest validation and session-ledger validation;
- the `unknown_entry_drift_report_reference_v1` manifest entry shape;
- empty `parser_event_families`;
- report-only coverage status and basis;
- normalized drift report reference path;
- absence of the underlying log-like fixture path from the corpus manifest
  entry;
- session-ledger drift summary counts:
  - `unknown_entries: 7`
  - `drift_report_status: review`
  - `unknown_signatures: 4`
  - `unmatched_api_names: 3`
  - `unmatched_request_api_names: 3`
  - `routed_event_families: 0`
- game-row non-applicability;
- privacy redaction flags;
- report summary movement from 0 to 1 report-only family and 19 to 18
  missing families;
- the exact `log_runtime.unknown_entry` matrix row;
- adjacent private-log-drift non-claim.

Existing tests already covered the contracted evidence model, so no drift,
diagnostics, or evidence-ledger tests were changed:

- `tests/test_log_drift_sensor.py`
  - committed normalized drift report reference;
  - unknown counts and review samples;
  - no volatile keys, local paths, or raw log bodies in the reference.
- `tests/test_parser_diagnostics_mode.py`
  - unknown evidence produces review status;
  - sensitive endpoint-like text is redacted.
- `tests/test_evidence_ledger.py`
  - Tier 6 `unknown_entry_count` is scoped to one analyzed input;
  - unknown signatures and API names remain review samples, not trusted parser
    inputs.

## Contract Mismatches

No blocking mismatches were found.

The existing drift/diagnostics/evidence-ledger behavior and tests already
satisfied the evidence model. The implementation stayed metadata/test-only.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future log rotation, missing-message-type, reconnect, firewall/network-drop,
private-log-drift, live diagnostics, private smoke, release-readiness,
analytics, AI, or coaching evidence will require separate contracts.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata
behavior.

Future log-runtime children should not inherit support claims from this
report-only unknown-entry row.

## Validation Run

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
python3 -m ruff check src tests
```

- passed: all checks passed

```bash
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

Changed-package path-scoped checks included the untracked Codex B source
contract and the Codex C handoff/report:

```bash
printf '%s\n' docs/contracts/parser_corpus_unknown_entry_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_unknown_entry_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_unknown_entry_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok

Validation caveat:

- The literal contract-suggested secret/private-marker scan that also included
  unchanged `tests/test_log_drift_sensor.py`,
  `tests/test_parser_diagnostics_mode.py`, and `tests/test_evidence_ledger.py`
  reproduced pre-existing scanner findings in unchanged evidence tests.
- The actual changed-package scan, including the new contract, metadata,
  corpus test, handoff, and report, passed with 0 forbidden findings and 0
  warnings.

## Open Risks

- This is report-only corpus coverage. It does not prove parser support for
  unknown semantic content.
- The corpus parity report remains `partial_coverage_map_ready`; this package
  does not complete tracker #158.
- Live private Player.log drift health, live diagnostics readiness, release
  readiness, analytics truth, AI truth, coaching truth, and production
  behavior remain unverified.
- External Manasight metadata remains taxonomy/category context only and was
  not imported, copied, mirrored, or committed.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer for issue #377, parser corpus unknown-entry coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/377
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/375
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/376
    - Previous merge commit: 3a0ae4598af3bcffa5170decf1e7cf816bb29c6d
    - Branch: codex/parser-corpus-unknown-entry-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_unknown_entry_coverage.md
    - Handoff: docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md

  Goal:
    Review the implementation package against the contract. Confirm that only log_runtime.unknown_entry moved to covered_report_only, that parser_event_families remains empty, and that unknown entries remain review/drift evidence rather than parser-understood facts.

  Review:
    - tests/fixtures/parser_corpus/corpus_manifest.v1.json
    - tests/fixtures/parser_corpus/session_ledger.v1.json
    - tests/test_corpus_parity_report.py
    - docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md
    - docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md
    - Existing evidence tests: tests/test_log_drift_sensor.py, tests/test_parser_diagnostics_mode.py, tests/test_evidence_ledger.py

  Do:
    - Verify the branch is based on codex/parser-parity and includes merge commit 3a0ae4598af3bcffa5170decf1e7cf816bb29c6d.
    - Confirm unknown_entry_drift_report_reference_v1 is the only new corpus coverage entry.
    - Confirm log_runtime.unknown_entry is covered_report_only with diagnostics_only, fixture_metadata_only, and evidence_ledger_only basis.
    - Confirm covered_synthetic did not change for this issue.
    - Confirm parser_event_families remains empty for the unknown-entry row.
    - Confirm the corpus manifest references the normalized drift report reference, not the underlying log-like fixture path.
    - Confirm adjacent log-runtime, connection, drift-debug, private-log-drift, live-diagnostics, analytics, AI, coaching, and release-readiness families were not newly covered.
    - Confirm no raw/private/external logs, local artifacts, generated data, workbook exports, credentials, or external corpus contents were committed.
    - Run or inspect validation and produce Codex E findings plus verdict.

  Do not:
    - Implement fixes.
    - Target main directly.
    - Close issue #377 or tracker #158.
    - Change parser behavior, router semantics, diagnostics report shape, drift report behavior, evidence-ledger behavior, golden replay behavior, feature-equity behavior, runtime, workbook, webhook, Apps Script, analytics, AI, coaching, CI, merge/deploy, or production behavior.
    - Claim parser support for unknown semantic content, new parser event kinds, automatic parser-gap issue creation, live private drift health, diagnostics readiness, private smoke success, release readiness, analytics truth, AI truth, coaching truth, or full corpus parity.

  Validation:
    - python3 -m pytest -q tests/test_corpus_parity_report.py
    - python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 -m ruff check src tests
    - git diff --check
    - python3 tools/check_agent_docs.py
    - path-scoped secret/private-marker scan
    - path-scoped protected-surface gate
    - selector check for the changed package

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/377"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/376"
  previous_merge_commit: "3a0ae4598af3bcffa5170decf1e7cf816bb29c6d"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_unknown_entry_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md"
  verdict: "report_only_unknown_entry_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-unknown-entry-coverage"
  base_branch: "codex/parser-parity"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/377"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/376"
  previous_merge_commit: "3a0ae4598af3bcffa5170decf1e7cf816bb29c6d"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_unknown_entry_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md"
  verdict: "report_only_unknown_entry_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-unknown-entry-coverage"
  base_branch: "codex/parser-parity"
```
