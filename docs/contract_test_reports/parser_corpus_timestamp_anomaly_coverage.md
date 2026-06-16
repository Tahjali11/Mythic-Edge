# Parser Corpus Timestamp Anomaly Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/370
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/368
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/369
- previous_merge_commit: `c7dfefc1e1c00f521ace4243f974d12c17596994`
- contract:
  `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- branch: `codex/parser-corpus-timestamp-anomaly-coverage`
- base_branch: `codex/parser-parity`
- report_lifecycle: final_approval
- risk_tier: High

## Source Snapshot

PR #369 is present in the local branch:

- required merge commit:
  `c7dfefc1e1c00f521ace4243f974d12c17596994`
- local HEAD before implementation:
  `c7dfefc1e1c00f521ace4243f974d12c17596994`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 8
- covered_report_only: 0
- partial: 3
- missing: 22
- blocked_external_boundary: 6

Pre-change log/runtime rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `log_runtime.detailed_logs_disabled` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `detailed_logs_disabled_synthetic_v1` |
| `log_runtime.rotation` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `log_runtime.malformed_or_headerless` | `missing` | `external_reference_only` | none |
| `log_runtime.timestamp_anomaly` | `missing` | `external_reference_only` | none |
| `log_runtime.unknown_entry` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single synthetic metadata path authorized by the contract:

- manifest entry: `timestamp_anomaly_synthetic_v1`
- session ledger entry: `timestamp_anomaly_synthetic_v1`
- scenario family: `log_runtime.timestamp_anomaly`
- coverage status: `covered_synthetic`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`
- parser event families: none
- parser claim families:
  - `router_timestamp_missing_stat`
  - `router_timestamp_parse_failure_stat`
  - `router_timestamp_anomalies_aggregate`
  - `timestamp_anomaly_privacy_boundary`

The synthetic entry ties existing router behavior for
`timestamp_missing`, `timestamp_parse_failure`, and `timestamp_anomalies` into
the corpus coverage row. It does not add raw log fixtures, private runtime
reports, actual Player.log timestamp-drift evidence, local app-data contents,
external corpus material, or parser source changes.

## Focused Router Evidence

Existing focused router tests verify:

- valid first-line timestamp extraction;
- first-line-only timestamp extraction behavior;
- invalid timestamp values returning no parsed timestamp;
- `Router.route(...)` increments `timestamp_missing` for unrouted entries with
  no timestamp marker;
- `Router.route(...)` increments `timestamp_parse_failure` for unrouted entries
  with invalid timestamp values;
- `RouterStats.timestamp_anomalies` aggregates missing and parse-failed
  timestamp counts, including routed truncation markers that still count as
  timestamp anomalies.

This implementation did not change router source or router tests. The new
corpus metadata uses those tests only as parser behavior evidence for the
narrow `log_runtime.timestamp_anomaly` family.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 9
- covered_report_only: 0
- partial: 3
- missing: 21
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
| `log_runtime.timestamp_anomaly` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `timestamp_anomaly_synthetic_v1` |
| `log_runtime.unknown_entry` | `missing` | `external_reference_only` | none |

The timestamp anomaly row includes this non-claim note:

```text
Synthetic timestamp anomaly coverage proves router-owned timestamp_missing, timestamp_parse_failure, and timestamp_anomalies stats only; it does not prove malformed/headerless log handling, unknown-entry routing, log rotation, real local Player.log timestamp drift, private smoke, release readiness, analytics truth, AI truth, coaching truth, or production behavior.
```

## Privacy And Protected-Surface Assertions

- No parser source behavior changed.
- No timestamp parsing behavior, router semantics, parser event class, parser
  state final reconciliation, diagnostics report shape, log drift behavior,
  golden replay behavior, feature-equity behavior, runtime status schema,
  match/game identity, deduplication, workbook schema, webhook payload shape,
  Apps Script behavior, Google Sheets sync, output transport, runtime artifact,
  failed delivery artifact, workbook export, local app behavior, analytics
  truth, AI truth, coaching behavior, CI gate, merge policy, deploy policy, or
  production surface changed.
- No raw log fixture, private Player.log excerpt, private smoke output, actual
  runtime timestamp drift report, local app-data content, local path, golden
  replay fixture, feature-equity baseline, runtime artifact, workbook export,
  generated/private artifact, external corpus content, or credential was added.
- The synthetic session entry records no raw log lines, private paths, raw
  payloads, external logs, decklists, private machine identifiers, account
  identifiers, timestamp strings from private logs, IP/network traces, or
  private report locations.

## Explicit Non-Claims

- This report does not claim malformed/headerless log handling.
- This report does not claim unknown-entry routing coverage.
- This report does not claim log rotation support.
- This report does not redefine issue #368 detailed logs disabled coverage.
- This report does not redefine issue #364 connection error payload coverage.
- This report does not redefine issue #366 connection disconnect coverage.
- This report does not claim real local Player.log timestamp drift evidence.
- This report does not claim private smoke success, release readiness,
  production reliability, diagnostics truth, analytics truth, AI truth, or
  coaching truth.
- This report does not claim full Mythic Edge corpus parity or full
  log-runtime parity.
- This report does not decide merge readiness, deploy readiness,
  public/private-release readiness, issue closure, or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md`

## Next Recommended Role

Codex E: Module Reviewer.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

No contract mismatches, missing focused tests, privacy leaks,
protected-surface drift, parser behavior changes, timestamp parsing changes,
router semantic changes, parser event-class changes, diagnostics/drift/golden
replay/feature-equity behavior changes, runtime-status behavior changes, or
adjacent log-runtime/connection coverage overclaims were found in the reviewed
package.

Validation caveat: the literal contract-suggested secret/private-marker scan
that includes unchanged `tests/test_router_unit.py` reproduces pre-existing
`raw_player_log_content` findings in that unchanged router test file. The
six-file changed-package scan passes with 0 forbidden findings and 0 warnings.

### Contract-Test Verdict

Pass. The package is ready for Codex F: Module Submitter.

The implementation matches the contracted V1 synthetic metadata slice:

- only `log_runtime.timestamp_anomaly` moved from `missing` to
  `covered_synthetic`;
- `log_runtime.detailed_logs_disabled` remains `covered_synthetic` through
  issue #368 and `detailed_logs_disabled_synthetic_v1`;
- `log_runtime.rotation` remains `blocked_external_boundary`;
- `log_runtime.malformed_or_headerless` remains `missing`;
- `log_runtime.unknown_entry` remains `missing`;
- `connection.connection_error_payload` remains `covered_synthetic` through
  issue #364 and `connection_error_payload_synthetic_v1`;
- `connection.disconnect` remains `covered_synthetic` through issue #366 and
  `connection_disconnect_synthetic_v1`;
- `connection.reconnect` remains `blocked_external_boundary`;
- `connection.firewall_or_network_drop` remains `missing`;
- `timestamp_anomaly_synthetic_v1` exists in both the corpus manifest and
  session ledger;
- the manifest entry has `parser_event_families: []` by design;
- the session-ledger entry records synthetic router stats summary counts only;
- no parser behavior, router semantics, timestamp parsing, or protected
  downstream surfaces changed;
- no raw/private/external logs, private runtime reports, local app-data
  contents, local paths, runtime artifacts, private reports, credentials,
  webhook URLs, or raw payload dumps are committed.

### Validation Results

Live workflow state was verified:

- issue #370: open;
- tracker #158: open;
- previous issue #368: closed;
- previous PR #369: merged into `codex/parser-parity`;
- previous merge commit `c7dfefc1e1c00f521ace4243f974d12c17596994`:
  present in local ancestry;
- current branch: `codex/parser-corpus-timestamp-anomaly-coverage`;
- base branch: `origin/codex/parser-parity`.

Commands run by Codex E:

- `git status --short --branch` -> expected branch and tracked/untracked
  review package only.
- `git diff -- tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py`
  -> tracked diff limited to manifest, session ledger, and focused corpus
  parity tests.
- `git log --oneline -8 --decorate` and `git rev-parse HEAD` -> local HEAD is
  `c7dfefc1e1c00f521ace4243f974d12c17596994`.
- `git merge-base --is-ancestor c7dfefc1e1c00f521ace4243f974d12c17596994 HEAD`
  -> passed.
- `gh issue view 370 --repo Tahjali11/Mythic-Edge --json number,title,state,url,labels`
  -> issue #370 is open.
- `gh issue view 158 --repo Tahjali11/Mythic-Edge --json number,title,state,url`
  -> tracker #158 is open.
- `gh issue view 368 --repo Tahjali11/Mythic-Edge --json number,title,state,url`
  -> previous issue #368 is closed.
- `gh pr view 369 --repo Tahjali11/Mythic-Edge --json number,title,state,isDraft,baseRefName,headRefName,mergeCommit,url`
  -> PR #369 is merged into `codex/parser-parity` with merge commit
  `c7dfefc1e1c00f521ace4243f974d12c17596994`.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  -> `partial_coverage_map_ready` with 45 families, 6 committed, and 21
  missing.
- Direct `build_corpus_parity_report(...)` row inspection confirmed:
  `log_runtime.timestamp_anomaly` is `covered_synthetic`;
  `log_runtime.detailed_logs_disabled` remains `covered_synthetic`;
  `log_runtime.rotation` remains `blocked_external_boundary`;
  `log_runtime.malformed_or_headerless` and `log_runtime.unknown_entry`
  remain `missing`;
  `connection.connection_error_payload` and `connection.disconnect` remain
  `covered_synthetic`;
  `connection.reconnect` remains `blocked_external_boundary`; and
  `connection.firewall_or_network_drop` remains `missing`.
- `python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_router_unit.py tests/test_parser_regressions.py`
  -> 27 passed.
- `python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py`
  -> 35 passed.
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
  including unchanged `tests/test_router_unit.py` -> failed with 6
  pre-existing `raw_player_log_content` findings and 2 ambiguous-marker
  warnings in that unchanged router evidence file.
- Literal contract-suggested `python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin`
  including unchanged `tests/test_router_unit.py` -> passed with 0 forbidden
  and 0 warnings.
- Literal contract-suggested `python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin`
  including unchanged `tests/test_router_unit.py` -> `selection_status: ok`.
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

- `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- `docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md`
- `docs/implementation_handoffs/parser_corpus_timestamp_anomaly_coverage_comparison.md`

No `src`, `tools`, `.github`, parser source, router source, timestamp parsing,
parser event class, diagnostics, drift sensor, golden replay, feature-equity,
runtime status, workbook, webhook, Apps Script, analytics, AI, CI, local app,
generated data, failed-delivery, workbook-export, release, or production files
are changed by this package.

### Remaining Non-Blocking Gaps

- This remains synthetic router-stat corpus metadata, not replayed private
  Player.log timestamp drift coverage.
- Router-owned timestamp anomaly counts are narrower than malformed/headerless
  log handling, unknown-entry routing, log rotation, or live runtime
  resilience.
- Diagnostics, drift sensor, golden replay, and feature-equity reports remain
  downstream consumers of router counts, not timestamp truth owners.
- Corpus coverage remains review metadata and does not become parser truth,
  runtime truth, diagnostics truth, workbook truth, analytics truth, AI truth,
  readiness, deploy, release, or tracker authority.

### Next Recommended Role

Codex F: Module Submitter.

Codex F should stage only the six reviewed files and submit this package
toward `codex/parser-parity`. Codex F must not target `main` directly, close
issue #370, close tracker #158, or widen the scope.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/370"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/368"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/369"
  previous_merge_commit: "c7dfefc1e1c00f521ace4243f974d12c17596994"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_timestamp_anomaly_coverage.md"
  target_artifact: "draft PR for synthetic timestamp anomaly coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-timestamp-anomaly-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_router_unit.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan for the six reviewed files"
    - "path-scoped protected-surface check for the six reviewed files"
    - "path-scoped validation selector check for the six reviewed files"
    - "python3 -m pytest -q"
  validation_caveat:
    - "The literal contract-suggested secret/private-marker scan including unchanged tests/test_router_unit.py fails on pre-existing raw_player_log_content findings in that unchanged router evidence file; the six-file changed-package scan passes cleanly."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #370 or tracker #158."
    - "Do not change parser behavior, timestamp parsing behavior, router semantics, parser state final reconciliation, parser event classes, diagnostics behavior, drift sensor behavior, golden replay behavior, feature-equity behavior, runtime status behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge/deploy policy, release readiness, production behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed-delivery artifacts, workbook exports, or local runtime artifacts."
    - "Do not invent a timestamp anomaly parser event or event family; this coverage is router-stat evidence."
    - "Do not move log_runtime.malformed_or_headerless, log_runtime.unknown_entry, or log_runtime.rotation to covered status."
    - "Do not redefine issue #368 detailed logs disabled coverage, issue #364 connection error payload coverage, or issue #366 connection disconnect coverage."
    - "Do not use diagnostics, drift reports, golden replay, feature-equity reports, private Player.log checks, or live runtime reports as the sole coverage basis."
    - "Do not import, copy, mirror, or commit external/raw/private logs, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, parser source, runtime timestamp drift reports, local app-data contents, local paths, private reports, credentials, tokens, API keys, webhook URLs, Manasight raw logs, external raw corpus contents, or private strategy notes."
    - "Do not claim full Mythic Edge corpus parity, full log-runtime parity, malformed/headerless log handling, unknown-entry routing, log rotation support, private-smoke readiness, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
```
