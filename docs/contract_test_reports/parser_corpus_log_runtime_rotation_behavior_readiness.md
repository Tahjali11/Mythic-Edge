# Parser Corpus Log Runtime Rotation Behavior Readiness Report

## Verdict

`log_runtime.rotation` has one reduced synthetic behavior-readiness uplift
ready for Codex E review.

The evidence is intentionally narrow. It proves that existing repo-owned
tailer/stream behavior covers a reduced synthetic packet:

- `FileTailer` detects one size-shrink rotation shape;
- replacement content is read from the beginning;
- `MtgaEventStream` publishes a sanitized `LogFileRotatedEvent` for a rotated
  tail batch; and
- the `LogFileRotatedEvent` schema snapshot remains compatible.

This report does not claim live log-rotation support, live watcher
correctness, robust log-rotation resilience, file identity tracking,
duplicate/replay prevention, recycle/rollback truth, parser support, release
readiness, deploy readiness, production behavior, analytics truth, AI truth,
coaching truth, tracker completion, #388/#381 activation, or full corpus
parity.

## Evidence Added

- Corpus manifest entry:
  `log_runtime_rotation_synthetic_tailer_stream_v1`
- Session-ledger entry:
  `log_runtime_rotation_synthetic_tailer_stream_v1`
- Corpus parity assertions pinning:
  - status movement to `covered_synthetic`;
  - `parser_behavior_verified` basis;
  - `LogFileRotated` event family;
  - readiness metric count movement;
  - adjacent-row non-promotion; and
  - required non-claims.

The #444 entry `log_runtime_rotation_boundary_report_v1` remains present and
report-only.

## Parser-Owned Evidence

The tailer leg is covered by
`tests/test_tailer.py::test_poll_reports_rotation_and_reads_replacement_content`.
It verifies a repo-owned temp file where a prior end offset is followed by a
shorter replacement write, `TailBatch.rotated is True`, and the replacement
entry is read from the beginning.

The stream leg is covered by
`tests/test_stream_integration.py::test_stream_emits_rotated_event_with_sanitized_log_path`.
It verifies a fake tailer batch with `rotated=True`, published
`LogFileRotatedEvent`, payload `type == "log_file_rotated"`, display-path
payload `path == "Player.log"`, and empty raw metadata.

The event-shape leg is covered by `tests/test_event_schema_snapshots.py`,
which includes the `LogFileRotatedEvent` payload sample.

## Corpus Status Effect

Before issue #502:

```yaml
log_runtime.rotation:
  coverage_status: "covered_report_only"
  coverage_basis:
    - "fixture_metadata_only"
  mythic_edge_entries:
    - "log_runtime_rotation_boundary_report_v1"
```

After issue #502:

```yaml
log_runtime.rotation:
  coverage_status: "covered_synthetic"
  coverage_basis:
    - "fixture_metadata_only"
    - "parser_behavior_verified"
  mythic_edge_entries:
    - "log_runtime_rotation_boundary_report_v1"
    - "log_runtime_rotation_synthetic_tailer_stream_v1"
```

Current overall corpus summary:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 21
covered_report_only: 12
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
```

## Privacy And Protected Boundaries

- No private Player.log, UTC_Log, live MTGA, live filesystem watcher check,
  network check, private smoke output, Manasight raw log, external corpus
  input, generated data, SQLite artifact, runtime artifact, workbook export,
  secret, credential, token, API key, webhook URL, exact private path, exact
  private offset, exact private file size, raw hash, or local-only artifact was
  used.
- No parser behavior, tailer behavior, stream behavior, parser event classes,
  router semantics, diagnostics, drift, golden replay, feature-equity,
  evidence-ledger, analytics behavior, workbook schema, webhook payload shape,
  Apps Script behavior, Google Sheets sync, output transport, CI gates, merge
  readiness, deploy readiness, production behavior, or final integration
  policy changed.
- `drift_debug.rename_or_rotation_collision` remains report-only.
- `drift_debug.recycle_or_rollback` remains blocked external-boundary.
- `log_runtime.unknown_entry` remains report-only.

## Non-Claims

This report does not claim:

- live log-rotation support;
- live watcher correctness;
- tailer correctness beyond the reduced packet;
- stream production readiness;
- robust log-rotation resilience;
- file identity tracking;
- duplicate/replay prevention;
- recycle/rollback truth;
- parser support;
- private smoke success;
- live Player.log health;
- release readiness;
- deploy readiness;
- production behavior;
- analytics truth;
- AI truth;
- coaching truth;
- tracker completion;
- #388 or #381 activation;
- full corpus parity.

## Validation

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
  passed: 7 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_event_schema_snapshots.py tests/test_corpus_parity_report.py`
  passed: 24 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=21, report_only=12, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  completed with `selection_status: ok`: changed paths 6, required 5,
  recommended 1, warnings 0.
- Path-scoped secret/private-marker scan passed: scanned paths 6, forbidden 0,
  warnings 0.
- Path-scoped protected-surface scan passed: changed paths 6, forbidden 0,
  warnings 0.
- `git diff --check` passed.

## Residual Risks

- The evidence is synthetic and proves only the reduced tailer/stream packet.
- It does not prove live watcher correctness, robust log-rotation resilience,
  duplicate/replay prevention, recycle/rollback truth, file identity tracking,
  private smoke success, parser support, release readiness, deploy readiness,
  production behavior, analytics truth, AI truth, coaching truth, tracker
  completion, or full corpus parity.
- Overall corpus readiness remains blocked by report-only, private-evidence,
  and external-boundary rows.

## Codex E Review Target

Codex E should confirm that this is a safe additive metadata/test/docs uplift
and that the new `covered_synthetic` status is bounded to the focused
tailer/stream packet only.

## Codex E Contract-Test Review

Review result: approved for Codex F submission.

No blocking findings were found. The package keeps the #444
`log_runtime_rotation_boundary_report_v1` entry as report-only boundary
metadata and adds only the reduced
`log_runtime_rotation_synthetic_tailer_stream_v1` packet. The synthetic packet
is bounded to existing `FileTailer` size-shrink replacement behavior,
sanitized `MtgaEventStream` `LogFileRotatedEvent` publication, and event
schema snapshot compatibility.

The review confirmed that `drift_debug.rename_or_rotation_collision` remains
report-only, `drift_debug.recycle_or_rollback` remains
blocked-external-boundary, and `log_runtime.unknown_entry` remains report-only.
The corpus summary remains `parser_behavior_ready=false` and
`pipeline_activation_ready_for_issue_388=false`.

Validation rerun by Codex E:

- `PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_event_schema_snapshots.py tests/test_corpus_parity_report.py`
  passed: 24 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed `parser_behavior_ready=no`.
- Path-scoped secret/private-marker scan passed: scanned paths 6, forbidden 0,
  warnings 0.
- Path-scoped protected-surface scan passed: changed paths 6, forbidden 0,
  warnings 0.
- Path-scoped validation selector completed with `selection_status: ok`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- `PYTHONPATH=src python3 -m pytest -q` passed: 1778 tests.

Remaining risk is intentionally scoped: this is synthetic behavior evidence
only. It does not prove live file-system watcher correctness, robust
log-rotation resilience, file identity tracking, duplicate/replay prevention,
recycle/rollback truth, private smoke success, parser support, release
readiness, deploy readiness, production behavior, analytics truth, AI truth,
coaching truth, tracker completion, #388/#381 activation, or full corpus
parity.

Next recommended role: Codex F: Module Submitter.
