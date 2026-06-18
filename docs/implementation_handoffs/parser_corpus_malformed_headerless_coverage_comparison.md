# Parser Corpus Malformed Headerless Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/372

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_malformed_headerless_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`synthetic_malformed_headerless_coverage_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `malformed_headerless_synthetic_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching synthetic line-buffer summary session ledger metadata.
- `tests/test_corpus_parity_report.py`
  - Updated summary counts and malformed/headerless row assertions.
  - Added focused checks for empty `parser_event_families`, line-buffer claim
    families, session-ledger line-buffer counts, privacy flags, and adjacent
    log-runtime non-claims.
- `docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_malformed_headerless_coverage.md`

No parser source, line-buffer source, header classification behavior, tailer
behavior, router behavior, parser event class, diagnostics/drift/golden-replay
behavior, feature-equity behavior, runtime artifact, workbook export,
generated/private artifact, raw fixture, or external corpus content was added
or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 9
- missing: 21
- `log_runtime.detailed_logs_disabled`: `covered_synthetic`
- `log_runtime.timestamp_anomaly`: `covered_synthetic`
- `log_runtime.rotation`: `blocked_external_boundary`
- `log_runtime.malformed_or_headerless`: `missing`
- `log_runtime.unknown_entry`: `missing`
- `connection.connection_error_payload`: `covered_synthetic`
- `connection.disconnect`: `covered_synthetic`

This matched the contract's expected starting state after issue #370.

## Contract Changes Implemented

Implemented exactly one authorized coverage promotion:

| Scenario family | Before | After |
| --- | --- | --- |
| `log_runtime.malformed_or_headerless` | `missing` | `covered_synthetic` |

Preserved the required adjacent-family boundary:

- `log_runtime.detailed_logs_disabled` remains `covered_synthetic` through
  issue #368 and `detailed_logs_disabled_synthetic_v1`.
- `log_runtime.timestamp_anomaly` remains `covered_synthetic` through issue
  #370 and `timestamp_anomaly_synthetic_v1`.
- `log_runtime.rotation` remains `blocked_external_boundary`.
- `log_runtime.unknown_entry` remains `missing`.
- `connection.connection_error_payload` remains `covered_synthetic` through
  issue #364 and `connection_error_payload_synthetic_v1`.
- `connection.disconnect` remains `covered_synthetic` through issue #366 and
  `connection_disconnect_synthetic_v1`.
- `connection.reconnect` remains `blocked_external_boundary`.
- `connection.firewall_or_network_drop` remains `missing`.

Added the required synthetic metadata:

- entry id: `malformed_headerless_synthetic_v1`
- session id: `malformed_headerless_synthetic_v1`
- source kind: `synthetic_committed_fixture`
- privacy class: `synthetic_committable`
- sanitization status: `synthetic`
- parser event families: none
- parser claim families:
  - `line_buffer_header_classification`
  - `line_buffer_headerless_orphan_noise_ignored`
  - `line_buffer_unknown_header_boundary`
  - `line_buffer_partial_line_boundary`
  - `line_buffer_multiline_boundary`
  - `malformed_headerless_privacy_boundary`
- coverage basis: `fixture_metadata_only`, `parser_behavior_verified`

The session-ledger validator accepted the contract-required
`parser_coverage.line_buffer_*` fields without schema changes.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- manifest validation and session-ledger validation;
- the `malformed_headerless_synthetic_v1` manifest entry shape;
- empty `parser_event_families` for entry-boundary evidence;
- synthetic line-buffer session counts:
  - `line_buffer_headerless_orphan_lines_ignored: 1`
  - `line_buffer_unknown_header_entries: 1`
  - `line_buffer_partial_fragments_joined: 1`
  - `line_buffer_multiline_entries_finalized: 1`
  - `line_buffer_single_line_headers_emitted: 1`
- game-row non-applicability;
- privacy redaction flags;
- the report summary movement from 9 to 10 synthetic families and 21 to 20
  missing families;
- the exact `log_runtime.malformed_or_headerless` matrix row;
- adjacent log-runtime and connection family non-claims.

Existing line-buffer tests already cover:

- known header classification and clean single-line emission;
- orphan/headerless noise ignored when no entry is open;
- unknown bracketed headers emitted as `EntryHeader.UNKNOWN`;
- partial header fragments joined before emission or finalized by `flush()`;
- multiline entries finalized before the next header;
- committed line-buffer corpus slices that keep single-line entry bodies clean.

No line-buffer tests or parser behavior tests were changed because the
existing evidence already satisfied the contract.

## Contract Mismatches

No blocking mismatches were found.

The manifest/session ledger schemas accepted the synthetic entry shape and the
machine-readable line-buffer count fields. No line-buffer or parser behavior
change was required.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future unknown-entry, log-rotation, reconnect, firewall/network-drop, private
smoke, runtime health, or release-readiness evidence will require separate
contracts.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata
behavior.

Future log/runtime children should not inherit support claims from this
synthetic malformed/headerless entry.

## Validation Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 20 missing)`

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

Path-scoped checks for the changed implementation/report files included the
untracked source contract:

```bash
printf '%s\n' docs/contracts/parser_corpus_malformed_headerless_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_malformed_headerless_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_malformed_headerless_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok
- required checks selected: diff check, protected-surface gate, Ruff,
  secret/private-marker scan, and `tests/test_corpus_parity_report.py`
- recommended check selected: agent docs checker

The literal contract-suggested path-scoped secret scan was also attempted with
unchanged `tests/test_log_entry_headers.py`, `tests/test_entry_buffer_edges.py`,
and `tests/test_line_buffer_corpus.py` included. It failed with pre-existing
`raw_player_log_content` findings in those unchanged line-buffer evidence
tests. The changed implementation/report file scan above passed with no
findings.

An ASCII scan over the six changed files returned no non-ASCII matches.

## Still Unverified

- No private Player.log malformed-log smoke was run. That is explicitly out of
  scope.
- No unknown-entry routing, log drift detection, log-rotation, reconnect, or
  firewall/network-drop support was implemented or claimed.
- No full corpus parity, release readiness, merge readiness, deploy readiness,
  analytics truth, AI truth, or coaching truth is claimed.

## Risks

- The new row is synthetic line-buffer metadata, not real local runtime
  malformed-log evidence.
- Future reviewers should keep router unknown-entry stats as downstream
  routing evidence only; line-buffer/header-boundary behavior remains the
  evidence basis for this row.
- Future log-runtime issues should avoid treating this coverage as proof for
  unknown entries, drift reports, rotation, semantic malformed-log recovery,
  or live MTGA behavior.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #372, malformed/headerless log
corpus coverage under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/372

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Previous completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/370

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/371

Previous merge commit:
4dac867bd22fbb8465c9c8c44b250d129f653121

Branch:
codex/parser-corpus-malformed-headerless-coverage

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_malformed_headerless_coverage.md

Implementation handoff:
docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md

Contract test report:
docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md

Review goal:
Review the Codex C implementation against the contract. Verify that the
package moves only `log_runtime.malformed_or_headerless` from `missing` to
`covered_synthetic`, keeps the evidence grounded in existing LineBuffer and
header-boundary behavior, keeps `parser_event_families` empty, preserves
adjacent family statuses and non-claims, and does not change parser behavior
or protected downstream surfaces.

Check:
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md`
- `docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md`
- existing line-buffer evidence in `tests/test_log_entry_headers.py`,
  `tests/test_entry_buffer_edges.py`, and `tests/test_line_buffer_corpus.py`

Do not:
- Implement code or broaden the module scope.
- Change LineBuffer behavior, header classification behavior, tailer behavior,
  parser behavior, timestamp parsing behavior, router semantics, parser event
  classes, diagnostics behavior, drift sensor behavior, golden replay
  behavior, feature-equity behavior, runtime status behavior, workbook schema,
  webhook payload shape, Apps Script behavior, Google Sheets sync, analytics,
  AI/model-provider behavior, CI gates, merge/deploy policy, or production
  behavior.
- Commit raw/private Player.log excerpts, malformed-log runtime reports, local
  app-data contents, generated artifacts, SQLite files, workbook exports,
  failed posts, credentials, webhook URLs, Manasight raw logs, or external raw
  corpus contents.
- Claim unknown-entry routing, log drift detection, log rotation support, full
  log-runtime parity, semantic recovery from arbitrary malformed Player.log
  payloads, private smoke readiness, release readiness, merge readiness,
  deploy readiness, analytics truth, AI truth, or coaching truth.
- Close tracker #158 or issue #372.
- Target main directly.

Suggested validation:
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_line_buffer_corpus.py
- python3 -m pytest -q tests/test_tailer_router_integration.py
- python3 -m ruff check src tests tools
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker, protected-surface, and selector checks for the changed files

End with:
- findings first, ordered by severity
- contract-test verdict
- validation run
- residual risks
- next recommended role
- workflow_handoff block to Codex F if ready
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/372"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/370"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/371"
  previous_merge_commit: "4dac867bd22fbb8465c9c8c44b250d129f653121"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_malformed_headerless_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_malformed_headerless_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_malformed_headerless_coverage.md"
  verdict: "synthetic_malformed_headerless_coverage_ready_for_review"
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
    - "path-scoped changed-file secret/private-marker scan"
    - "path-scoped changed-file protected-surface gate"
    - "path-scoped changed-file validation selector"
  stop_conditions:
    - "Do not implement LineBuffer behavior, header classification, tailer behavior, parser behavior, or router semantic changes in this corpus coverage slice."
    - "Do not invent a malformed/headerless parser event or event family; this coverage is entry-boundary evidence."
    - "Do not use router unknown-entry stats, diagnostics, drift reports, golden replay, feature-equity reports, private Player.log checks, or live runtime reports as the sole coverage basis."
    - "Do not commit raw/private Player.log excerpts, raw local logs, malformed-log runtime reports, private app-data contents, generated artifacts, SQLite files, workbook exports, failed posts, runtime artifacts, credentials, tokens, API keys, webhook URLs, Manasight raw logs, or external raw corpus contents."
    - "Do not claim full Mythic Edge corpus parity, full log-runtime parity, unknown-entry routing, log drift detection, log rotation support, semantic recovery from arbitrary malformed Player.log payloads, private smoke readiness, release readiness, merge readiness, deploy readiness, analytics truth, AI truth, gameplay advice, hidden-card inference, archetype classification, or coaching truth."
    - "Do not target main directly or close tracker #158 or issue #372."
```
