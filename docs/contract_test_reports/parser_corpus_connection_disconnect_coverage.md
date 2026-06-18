# Parser Corpus Connection Disconnect Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/366
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/364
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/365
- previous_merge_commit: `5513f406f227fe53bea87de73bf6e86f4b58d30a`
- contract:
  `docs/contracts/parser_corpus_connection_disconnect_coverage.md`
- branch: `codex/parser-corpus-connection-disconnect-coverage`
- base_branch: `codex/parser-parity`
- report_lifecycle: final_approval
- risk_tier: High

## Source Snapshot

PR #365 is present in the local branch:

- required merge commit:
  `5513f406f227fe53bea87de73bf6e86f4b58d30a`
- local HEAD before implementation:
  `5513f406f227fe53bea87de73bf6e86f4b58d30a`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 6
- covered_report_only: 0
- partial: 3
- missing: 24
- blocked_external_boundary: 6

Pre-change connection rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `connection.connection_error_payload` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `connection_error_payload_synthetic_v1` |
| `connection.disconnect` | `missing` | `external_reference_only` | none |
| `connection.reconnect` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `connection.firewall_or_network_drop` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single synthetic metadata path authorized by the contract:

- manifest entry: `connection_disconnect_synthetic_v1`
- session ledger entry: `connection_disconnect_synthetic_v1`
- scenario family: `connection.disconnect`
- coverage status: `covered_synthetic`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`
- parser evidence families:
  - `MatchConnectionState`
  - `TcpConnectionClose`
  - `WebSocketClosed`
- parser claim families:
  - `connection_state_transition`
  - `tcp_connection_close_payload`
  - `websocket_closed_payload`
  - `disconnect_privacy_boundary`

The synthetic entry ties existing parser behavior for connection
state-transition and close event handling into the corpus coverage row. It
does not add raw log fixtures, local runtime artifacts, network traces,
external corpus material, or parser source changes.

## Focused Parser Evidence

Existing focused parser tests in `tests/test_connection_parsers.py` verify:

- Unity state-change markers emit `MatchConnectionState`;
- parsed state payloads preserve parser-owned `old` and `new` transition
  values;
- TCP close markers emit `TcpConnectionClose`;
- websocket close markers emit `WebSocketClosed`;
- parsed close payload mappings are preserved by the parser;
- malformed, non-mapping, non-Unity, and unrelated inputs are rejected.

This implementation did not change those parser tests or parser source. The
new corpus metadata uses them only as parser behavior evidence for the narrow
`connection.disconnect` family.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 7
- covered_report_only: 0
- partial: 3
- missing: 23
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

Post-change connection rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `connection.connection_error_payload` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `connection_error_payload_synthetic_v1` |
| `connection.disconnect` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `connection_disconnect_synthetic_v1` |
| `connection.reconnect` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `connection.firewall_or_network_drop` | `missing` | `external_reference_only` | none |

The disconnect row includes this non-claim note:

```text
Synthetic connection disconnect coverage proves parser-owned MatchConnectionState, TcpConnectionClose, and WebSocketClosed metadata only; it does not prove reconnect, firewall/drop behavior, network reliability, private smoke, release readiness, analytics truth, AI truth, coaching truth, or production behavior.
```

## Privacy And Protected-Surface Assertions

- No parser source behavior changed.
- No parser event class, router, parser state final reconciliation,
  diagnostics report shape, runtime status schema, match/game identity,
  deduplication, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets sync, output transport, runtime artifact, failed delivery
  artifact, workbook export, local app behavior, analytics truth, AI truth,
  coaching behavior, CI gate, merge policy, deploy policy, or production
  surface changed.
- No raw log fixture, private Player.log excerpt, private smoke output,
  network trace, local path, golden replay fixture, feature-equity baseline,
  runtime artifact, workbook export, generated/private artifact, external
  corpus content, or credential was added.
- The synthetic session entry records no raw log lines, private paths, raw
  payloads, external logs, decklists, IP addresses, hostnames, port values,
  firewall logs, network identifiers, strategy notes, or private report
  locations.

## Explicit Non-Claims

- This report does not claim reconnect coverage.
- This report does not claim firewall or network-drop coverage.
- This report does not redefine issue #364 connection error payload coverage.
- This report does not claim live runtime resilience, private smoke success,
  release readiness, production reliability, diagnostics truth, analytics
  truth, AI truth, or coaching truth.
- This report does not claim full Mythic Edge corpus parity.
- This report does not decide merge readiness, deploy readiness,
  public/private-release readiness, issue closure, or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_connection_disconnect_coverage_comparison.md`

## Next Recommended Role

Codex E: Module Reviewer.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

No contract mismatches, missing focused tests, privacy leaks,
protected-surface drift, parser behavior changes, router changes, event-class
changes, diagnostics/runtime-status behavior changes, or adjacent connection
coverage overclaims were found in the reviewed package.

### Contract-Test Verdict

Pass. The package is ready for Codex F: Module Submitter.

The implementation matches the contracted V1 synthetic metadata slice:

- only `connection.disconnect` moved from `missing` to `covered_synthetic`;
- `connection.connection_error_payload` remains `covered_synthetic` through
  issue #364 and `connection_error_payload_synthetic_v1`;
- `connection.reconnect` remains `blocked_external_boundary`;
- `connection.firewall_or_network_drop` remains `missing`;
- `connection_disconnect_synthetic_v1` exists in both the corpus manifest and
  session ledger;
- the manifest/session entry is synthetic, committed, privacy-safe metadata;
- existing focused connection parser tests are used as behavior evidence
  without changing parser source or parser tests;
- corpus report notes explicitly preserve reconnect, firewall/drop,
  network-reliability, private-smoke, release-readiness, analytics, AI,
  coaching, and production non-claims;
- no raw/private/external logs, network traces, local paths, runtime artifacts,
  IP addresses, hostnames, port values, private reports, credentials, webhook
  URLs, or raw payload dumps are committed;
- no parser source, parser event classes, router, diagnostics, runtime status,
  workbook, webhook, Apps Script, output, analytics, AI, local app, CI, merge,
  deploy, release, or production surface changed.

### Validation Results

Live workflow state was verified:

- issue #366: open;
- tracker #158: open;
- previous issue #364: closed;
- previous PR #365: merged into `codex/parser-parity`;
- previous merge commit `5513f406f227fe53bea87de73bf6e86f4b58d30a`:
  present in local ancestry;
- current branch: `codex/parser-corpus-connection-disconnect-coverage`;
- base branch: `origin/codex/parser-parity`.

Commands run by Codex E:

- `git status --short --branch` -> expected branch and tracked/untracked
  review package only.
- `git diff -- tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py`
  -> tracked diff limited to manifest, session ledger, and focused corpus
  parity tests.
- `git log --oneline -6 --decorate` and `git rev-parse HEAD` -> local HEAD
  is `5513f406f227fe53bea87de73bf6e86f4b58d30a`.
- `git merge-base --is-ancestor 5513f406f227fe53bea87de73bf6e86f4b58d30a HEAD`
  -> passed.
- `gh issue view 366 --repo Tahjali11/Mythic-Edge --json number,title,state,url,labels`
  -> issue #366 is open.
- `gh issue view 158 --repo Tahjali11/Mythic-Edge --json number,title,state,url`
  -> tracker #158 is open.
- `gh issue view 364 --repo Tahjali11/Mythic-Edge --json number,title,state,url`
  -> previous issue #364 is closed.
- `gh pr view 365 --repo Tahjali11/Mythic-Edge --json number,title,state,isDraft,baseRefName,headRefName,mergeCommit,url`
  -> PR #365 is merged into `codex/parser-parity` with merge commit
  `5513f406f227fe53bea87de73bf6e86f4b58d30a`.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  -> `partial_coverage_map_ready` with 45 families, 6 committed, and 23
  missing.
- Direct `build_corpus_parity_report(...)` row inspection confirmed:
  `connection.connection_error_payload` remains `covered_synthetic`;
  `connection.disconnect` is `covered_synthetic`;
  `connection.reconnect` remains `blocked_external_boundary`; and
  `connection.firewall_or_network_drop` remains `missing`.
- `python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py`
  -> 32 passed.
- `python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py`
  -> 23 passed.
- `python3 -m ruff check src tests tools` -> all checks passed.
- `python3 tools/check_agent_docs.py` -> passed with 0 errors and 0 warnings.
- `git diff --check` -> passed with no output.
- Path-scoped `python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin`
  over the six reviewed files -> passed with 0 forbidden and 0 warnings.
- Path-scoped `python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin`
  over the six reviewed files -> passed with 0 forbidden and 0 warnings.
- Path-scoped `python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin`
  over the six reviewed files -> `selection_status: ok`.
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

- `docs/contracts/parser_corpus_connection_disconnect_coverage.md`
- `docs/contract_test_reports/parser_corpus_connection_disconnect_coverage.md`
- `docs/implementation_handoffs/parser_corpus_connection_disconnect_coverage_comparison.md`

No `src`, `tools`, `.github`, parser source, parser event class, router,
diagnostics, runtime status, workbook, webhook, Apps Script, analytics, AI, CI,
local app, generated data, failed-delivery, workbook-export, release, or
production files are changed by this package.

### Remaining Non-Blocking Gaps

- This remains synthetic metadata coverage, not replayed private Player.log
  coverage.
- Parser-owned connection state/close metadata is narrower than live connection
  resilience.
- Reconnect, firewall/network-drop, private smoke, runtime-health,
  diagnostics, and release-readiness evidence remain future contract work.
- Corpus coverage remains review metadata and does not become parser truth,
  runtime truth, diagnostics truth, workbook truth, analytics truth, AI truth,
  readiness, deploy, release, or tracker authority.

### Next Recommended Role

Codex F: Module Submitter.

Codex F should stage only the six reviewed files and submit this package
toward `codex/parser-parity`. Codex F must not target `main` directly, close
issue #366, close tracker #158, or widen the scope.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/366"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/364"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/365"
  previous_merge_commit: "5513f406f227fe53bea87de73bf6e86f4b58d30a"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_connection_disconnect_coverage.md"
  target_artifact: "draft PR for synthetic connection disconnect coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-connection-disconnect-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py"
    - "python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan for the six reviewed files"
    - "path-scoped protected-surface check for the six reviewed files"
    - "path-scoped validation selector check for the six reviewed files"
    - "python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #366 or tracker #158."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics behavior, runtime status behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge/deploy policy, release readiness, production behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed-delivery artifacts, workbook exports, or local runtime artifacts."
    - "Do not move connection.reconnect or connection.firewall_or_network_drop to covered status."
    - "Do not redefine issue #364 connection error payload coverage."
    - "Do not import, copy, mirror, or commit external/raw/private logs, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, parser source, network traces, IP addresses, hostnames, port values, private reports, credentials, tokens, API keys, webhook URLs, or private strategy notes."
    - "Do not claim full Mythic Edge corpus parity, reconnect coverage, firewall/network-drop coverage, runtime resilience, private-smoke success, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
```
