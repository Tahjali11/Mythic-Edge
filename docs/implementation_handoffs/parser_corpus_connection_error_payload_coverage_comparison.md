# Parser Corpus Connection Error Payload Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/364

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_connection_error_payload_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`synthetic_connection_error_payload_coverage_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `connection_error_payload_synthetic_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching synthetic session ledger metadata.
- `tests/test_corpus_parity_report.py`
  - Updated summary counts and connection error payload row assertions.
  - Added focused checks for adjacent connection-family non-claims.
  - Added focused checks for the synthetic entry shape and privacy flags.
- `docs/contract_test_reports/parser_corpus_connection_error_payload_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_connection_error_payload_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_connection_error_payload_coverage.md`

No parser source, parser event class, router, parser state final
reconciliation, diagnostics/runtime status behavior, raw fixture, golden
replay fixture, feature-equity baseline, runtime artifact, workbook export,
generated/private artifact, network trace, private report, or external corpus
content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 5
- missing: 25
- `connection.connection_error_payload`: `missing`
- `connection.reconnect`: `blocked_external_boundary`
- `connection.disconnect`: `missing`
- `connection.firewall_or_network_drop`: `missing`

This matched the contract's expected starting state after issue #361.

## Contract Changes Implemented

Implemented exactly one authorized coverage promotion:

| Scenario family | Before | After |
| --- | --- | --- |
| `connection.connection_error_payload` | `missing` | `covered_synthetic` |

Preserved the required adjacent-family boundary:

- `connection.reconnect` remains `blocked_external_boundary`.
- `connection.disconnect` remains `missing`.
- `connection.firewall_or_network_drop` remains `missing`.

Added the required synthetic metadata:

- entry id: `connection_error_payload_synthetic_v1`
- session id: `connection_error_payload_synthetic_v1`
- source kind: `synthetic_committed_fixture`
- privacy class: `synthetic_committable`
- sanitization status: `synthetic`
- parser event families: `ConnectionError`
- parser claim families:
  - `connection_error_event`
  - `connection_error_type_discriminator`
  - `connection_error_payload_preservation`
  - `connection_error_privacy_boundary`
- coverage basis: `fixture_metadata_only`, `parser_behavior_verified`

The corpus row includes the required non-claim that connection error payload
coverage is synthetic parser-owned metadata only.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins the manifest entry, session
ledger entry, corpus summary counts, connection error payload coverage row,
adjacent family statuses, and privacy redaction flags.

Existing `tests/test_connection_parsers.py` covers `ConnectionError` parser
behavior for Unity JSON payload markers, connection-manager text markers,
matchmaking connection-lost text, malformed JSON rejection, unknown reconnect
result rejection, and unrelated-line rejection. It was included in validation.

No connection parser source or parser tests were changed.

## Contract Mismatches

No blocking mismatches were found.

The manifest/session ledger schemas accepted the synthetic entry shape. No
parser behavior change was required.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future reconnect, disconnect, firewall/network-drop, private smoke, runtime
health, or release-readiness evidence will require separate contracts.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata
behavior.

Future connection/runtime children should not inherit support claims from this
synthetic connection error payload entry.

## Validation Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 24 missing)`

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_connection_parsers.py
```

- passed: 32 passed

```bash
python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py
```

- passed: 23 passed

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
printf '%s\n' docs/contracts/parser_corpus_connection_error_payload_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_connection_error_payload_coverage_comparison.md docs/contract_test_reports/parser_corpus_connection_error_payload_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_connection_error_payload_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_connection_error_payload_coverage_comparison.md docs/contract_test_reports/parser_corpus_connection_error_payload_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_connection_error_payload_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_connection_error_payload_coverage_comparison.md docs/contract_test_reports/parser_corpus_connection_error_payload_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok
- required checks selected: diff check, protected-surface gate, Ruff,
  secret/private-marker scan, and `tests/test_corpus_parity_report.py`
- recommended check selected: agent docs checker

Optional broader validation was not run because the contract's focused bundle
passed and this package only changes corpus metadata, one focused test file,
and report/contract docs.

## Still Unverified

- No CI was inspected.
- No PR was opened.
- No actual private logs or app data were inspected.
- No external corpus contents were fetched or inspected.
- No live reconnect, disconnect, firewall/network-drop, private smoke,
  runtime-health, release-readiness, analytics, AI, coaching, or production
  evidence was attempted.

## Residual Risks

- This is synthetic metadata coverage, not replayed private Player.log
  coverage.
- Parser-owned connection error payload metadata is narrower than live
  connection resilience.
- Corpus coverage remains review metadata and not parser truth, runtime truth,
  diagnostics truth, workbook truth, analytics truth, AI truth, merge
  readiness, deploy readiness, release readiness, or tracker completion
  authority.

## Next Recommended Role

Codex E: Module Reviewer.

If review is clean, route to Codex F for module submission to
`codex/parser-parity`. If review finds overclaiming, privacy leakage, or scope
drift, route to Codex D with concrete findings.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #364 under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/364

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/361

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/362

Previous merge commit:
425b48b6937a95ef31f43435fb637a1b71cfe6b1

Branch:
codex/parser-corpus-connection-error-payload-coverage

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_connection_error_payload_coverage.md

Artifacts to review:
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/contract_test_reports/parser_corpus_connection_error_payload_coverage.md
- docs/implementation_handoffs/parser_corpus_connection_error_payload_coverage_comparison.md

Review focus:
- Verify only connection.connection_error_payload moved from missing to covered_synthetic.
- Verify connection.reconnect remains blocked_external_boundary.
- Verify connection.disconnect remains missing.
- Verify connection.firewall_or_network_drop remains missing.
- Verify connection_error_payload_synthetic_v1 exists in both corpus manifest and session ledger.
- Verify the new entry is synthetic, committed, and privacy-safe.
- Verify no external/raw/private log artifacts, network traces, local paths, runtime artifacts, IP addresses, hostnames, private reports, or strategy notes are committed.
- Verify no parser source, router, event class, diagnostics, or runtime status behavior changed.
- Verify corpus report notes preserve the reconnect/disconnect/network reliability/private smoke/release readiness non-claims.

Expected verdict if clean:
ready_for_module_submitter

Do not:
- Target main directly.
- Close #158 or #364.
- Implement parser behavior changes.
- Change connection parser behavior, router semantics, parser event classes, diagnostics behavior, runtime status behavior, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, coaching behavior, CI gates, merge readiness, deploy readiness, release readiness, or production behavior.
- Add raw log fixtures, external corpus contents, private Player.log excerpts, private local logs, generated/private artifacts, workbook exports, network traces, IP addresses, hostnames, credentials, tokens, API keys, or webhook URLs.
- Claim full Mythic Edge corpus parity, reconnect support, disconnect support, firewall/network-drop support, runtime resilience, private smoke success, release readiness, analytics truth, AI truth, or coaching truth.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/364"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/361"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/362"
  previous_merge_commit: "425b48b6937a95ef31f43435fb637a1b71cfe6b1"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_connection_error_payload_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_connection_error_payload_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_connection_error_payload_coverage.md"
  verdict: "synthetic_connection_error_payload_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-connection-error-payload-coverage"
  base_branch: "codex/parser-parity"
```
