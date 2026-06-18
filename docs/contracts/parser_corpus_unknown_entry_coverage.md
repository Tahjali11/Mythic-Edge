# Parser Corpus Unknown Entry Coverage Contract

## Module

Unknown-entry corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`log_runtime.unknown_entry` with report-only drift/diagnostics metadata. It
proves only that Mythic Edge has a safe, reviewed way to surface unknown routed
entries, unknown signatures, and unmatched API names for drift review. It does
not prove that the parser understood those entries, that unknown entries are
safe to ignore, that live private Player.log drift is healthy, or that Mythic
Edge has full log-runtime or corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/377
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/375
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/376
- Previous merge commit:
  `3a0ae4598af3bcffa5170decf1e7cf816bb29c6d`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-unknown-entry-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `3a0ae4598af3bcffa5170decf1e7cf816bb29c6d`
- target_artifact:
  `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/fixtures/golden_fixture_manifest.json`
- `tests/fixtures/player_log_drift_flush_timing_expected.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_corpus_parity_report.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_evidence_ledger.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, or external
  corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`log_runtime.unknown_entry` scenario family. Router, drift, diagnostics, and
evidence-ledger modules own the underlying report behavior and provenance
vocabulary. Corpus parity artifacts own only the coverage status claim that
Mythic Edge has safe repo-owned report evidence for this narrow family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence, but it is not a Parser behavior module and is not a
runtime, diagnostics implementation, analytics, workbook, local app, AI,
coaching, release, or production module.

## Truth Owner

Truth owner for `log_runtime.unknown_entry` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for unknown-entry counts and review samples:

- `src/mythic_edge_parser/router.py`
- `RouterStats.unknown`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `build_player_log_drift_report(...)`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `build_parser_diagnostics_report(...)`

Truth owner for provenance vocabulary:

- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`

Truth boundary:

- `Router.route(...)` owns incrementing `RouterStats.unknown` when a log entry
  does not produce parser events.
- `build_player_log_drift_report(...)` owns unknown-entry report evidence for
  one analyzed input, including unknown counts, unknown signatures, unmatched
  API names, unmatched request API names, and baseline deltas.
- `build_parser_diagnostics_report(...)` owns local diagnostics review status
  derived from unknown counts and drift flags.
- Evidence-ledger Tier 6 owns the rule that `unknown_entry_count` is scoped to
  one analyzed input and that unknown signatures/API names are review samples.
- Corpus parity artifacts own the report-only coverage row for
  `log_runtime.unknown_entry`.
- Unknown entries are not parser facts. They are evidence that Mythic Edge did
  not classify or parse a log entry into a trusted event.
- Corpus coverage status is review metadata. It is not parser truth,
  diagnostics readiness, live drift health, workbook truth, analytics truth, AI
  truth, coaching truth, merge readiness, deploy readiness, public/private
  release readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing RouterStats.unknown / drift report / diagnostics unknown evidence
  -> bounded committed report-only corpus manifest/session-ledger metadata
  -> corpus parity coverage row for log_runtime.unknown_entry
```

Forbidden reverse flow:

- Corpus coverage status must not change router or parser behavior.
- Corpus metadata must not change router dispatch, parser modules, parser
  event classes, diagnostics report shape, drift report behavior,
  evidence-ledger behavior, golden replay behavior, feature-equity behavior,
  runtime status behavior, workbook output, analytics, AI, coaching, release
  policy, or production behavior.
- Corpus metadata must not turn unknown signatures or unmatched API names into
  parser-understood facts, automatic parser-gap issues, trusted parser inputs,
  analytics labels, AI prompts, gameplay advice, or live-drift health claims.

Protected surfaces explicitly not touched:

- parser behavior
- router semantics
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- diagnostics report shape
- drift report behavior
- evidence-ledger behavior
- golden replay behavior
- feature-equity behavior
- runtime status artifacts or schema
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- delivery retry artifacts
- workbook exports
- SQLite/local app behavior
- analytics truth
- AI truth
- coaching behavior
- OpenAI/model-provider behavior
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_unknown_entry_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_log_drift_sensor.py`, only for focused test evidence that does
  not change behavior
- `tests/test_parser_diagnostics_mode.py`, only for focused test evidence that
  does not change behavior
- `docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `tests/fixtures/golden_fixture_manifest.json`
- `tests/fixtures/player_log_drift_flush_timing_expected.json`
- relevant diagnostics, drift, golden replay, feature-equity, and
  protected-surface tests

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- router dispatch or `RouterStats` semantic changes
- parser event class changes
- new unknown-entry parser event kinds
- automatic parser-gap issue creation
- diagnostics report shape changes
- drift report shape changes
- evidence-ledger schema/vocabulary changes
- golden replay behavior changes
- feature-equity behavior changes
- runtime status changes
- local live smoke execution
- new committed log fixtures
- changes to the existing drift input fixture
- Manasight corpus import
- log rotation, reconnect, firewall/network-drop, missing-message-type,
  timestamp-anomaly, malformed/headerless, pre-match-idle, private-log-drift,
  live-diagnostics, analytics-readiness, AI, coaching, CI, final integration,
  and production surfaces

## Public Interface

The public corpus interface remains the existing corpus parity report API:

```python
build_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]

write_corpus_parity_report(...) -> dict[str, Any]

validate_corpus_manifest(payload: Mapping[str, Any]) -> list[str]
validate_session_ledger(payload: Mapping[str, Any]) -> list[str]
```

The command-line interface remains:

```bash
python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

The underlying drift/diagnostics interfaces referenced by this contract are
existing evidence only:

```text
Router().route(entry: LogEntry) -> list[GameEvent]
Router().stats -> RouterStats
RouterStats.unknown: int

build_player_log_drift_report(
    source_path: Path,
    *,
    baseline_payload: dict[str, Any] | None = None,
) -> dict[str, Any]

build_parser_diagnostics_report(
    source_log: Path,
    *,
    profile: str = "live_game",
    status context argument unchanged,
    drift_baseline: dict[str, Any] | None = None,
    evidence_ledger_review: Mapping[str, Any] | None = None,
) -> dict[str, Any]
```

No new public parser, router, diagnostics, drift, runtime, workbook, webhook,
Apps Script, analytics, AI, or production interface is authorized by this
contract.

## Observed Current Behavior

Observed on `codex/parser-parity` at
`3a0ae4598af3bcffa5170decf1e7cf816bb29c6d`:

- Issue #377 is open under tracker #158.
- Tracker #158 remains open.
- Issue #375 is closed and PR #376 is merged into `codex/parser-parity`.
- The current corpus parity report is still partial:
  `partial_coverage_map_ready` with 45 scenario families, 6 committed
  families, and 19 missing families.
- `log_runtime.unknown_entry` exists in the corpus taxonomy.
- `log_runtime.unknown_entry` currently reports:
  - `coverage_status`: `missing`
  - `coverage_basis`: `external_reference_only`
  - `mythic_edge_entries`: `[]`
- `log_runtime.rotation` remains `blocked_external_boundary`.
- `log_runtime.detailed_logs_disabled`, `log_runtime.timestamp_anomaly`, and
  `log_runtime.malformed_or_headerless` are already covered as synthetic
  metadata.
- `tests/fixtures/golden_fixture_manifest.json` already includes
  `player_log_drift_flush_timing_v1` as a sanitized report-only drift fixture
  reference.
- `tests/fixtures/player_log_drift_flush_timing_expected.json` is a committed
  normalized drift report reference.
- The normalized drift report reference currently contains:
  - `status`: `review`
  - `entry_counts.unknown`: `7`
  - `top_unknown_signatures`: `4` signature rows
  - `top_unmatched_api_names`: `3` API-name rows
  - `top_unmatched_request_api_names`: `3` request API-name rows
  - `routed_event_kinds`: `{}`
- `tests/test_log_drift_sensor.py` verifies that the drift report reference
  contains no volatile keys, no local paths, no raw log bodies, and no runtime
  report/baseline paths.
- `tests/test_parser_diagnostics_mode.py` verifies that unknown signatures
  produce review status and are sanitized.
- `tests/test_evidence_ledger.py` verifies that Tier 6
  `unknown_entry_count` is run-scoped and that unknown entries are review
  samples, not parser truth.

## Required Guarantees

### Scenario Family Boundary

Codex C may close only this corpus coverage gap:

- `log_runtime.unknown_entry`

The implementation must not mark any of these families as covered:

- `log_runtime.rotation`
- `connection.reconnect`
- `connection.firewall_or_network_drop`
- `drift_debug.missing_message_type`
- `drift_debug.rename_or_rotation_collision`
- `drift_debug.recycle_or_rollback`
- `mythic_edge.live_diagnostics`
- `mythic_edge.private_log_report_only_drift`
- any parser, timer, deck API, gameplay-stress, analytics, AI, coaching, or
  release-readiness family not explicitly named above

### Coverage Status

The authorized V1 coverage status is:

```yaml
coverage_status: "covered_report_only"
coverage_basis:
  - "diagnostics_only"
  - "fixture_metadata_only"
  - "evidence_ledger_only"
```

`covered_report_only` is required because the coverage claim is grounded in
report outputs and review samples. It must not be upgraded to
`covered_synthetic` unless a later contract explicitly authorizes a synthetic
fixture that proves unknown-entry detection behavior without implying parser
support for unknown semantic content.

`parser_behavior_verified` is intentionally not required for this row. The
report can cite existing router/drift behavior, but the corpus coverage claim
must stay about review visibility, not parser understanding.

### Manifest Entry

Codex C should add exactly one manifest entry for this scenario family:

```yaml
entry_id: "unknown_entry_drift_report_reference_v1"
entry_type: "diagnostics_report"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/377"
authorized_by_contract: "docs/contracts/parser_corpus_unknown_entry_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  drift_fixture_manifest: "tests/fixtures/golden_fixture_manifest.json"
  normalized_drift_report_reference: "tests/fixtures/player_log_drift_flush_timing_expected.json"
  drift_sensor_test: "tests/test_log_drift_sensor.py"
  diagnostics_test: "tests/test_parser_diagnostics_mode.py"
  evidence_ledger_test: "tests/test_evidence_ledger.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
scenario_families:
  - "log_runtime.unknown_entry"
parser_event_families: []
parser_claim_families:
  - "router_unknown_entry_count"
  - "drift_unknown_signature_review_samples"
  - "drift_unmatched_api_name_review_samples"
  - "diagnostics_unknown_entries_review_status"
  - "evidence_ledger_unknown_entry_count_boundary"
  - "unknown_entry_privacy_boundary"
coverage_status: "covered_report_only"
coverage_basis:
  - "diagnostics_only"
  - "fixture_metadata_only"
  - "evidence_ledger_only"
known_gaps:
  - "Report-only unknown-entry coverage does not prove parser support for unknown semantic content, automatic parser-gap creation, log rotation, missing-message-type recovery, reconnect or network-drop behavior, live private Player.log drift health, diagnostics readiness, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
review_notes:
  - "Unknown-entry coverage proves that existing drift/diagnostics reports can surface unknown counts and review samples from a committed normalized report reference; it does not mean the parser understood the unknown entries."
```

Codex C may adjust wording only if the final wording preserves all non-claims,
privacy boundaries, scenario-family limits, and `covered_report_only` status
above.

Codex C must not include `tests/fixtures/flush_timing_corpus_slice.log` as a
path in the parser corpus manifest. The corpus manifest should reference the
normalized drift report reference and fixture manifest, not the underlying
log-like fixture path.

### Session Ledger Entry

Codex C should add exactly one session ledger entry with this logical shape:

```yaml
session_id: "unknown_entry_drift_report_reference_v1"
title: "Report-only unknown-entry drift evidence"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/377"
authorized_by_contract: "docs/contracts/parser_corpus_unknown_entry_coverage.md"
scenario_families:
  - "log_runtime.unknown_entry"
format_family: "log_runtime"
match_shape: "unknown_entry_drift_report_reference_only"
record_summary: "normalized_drift_report_reference_only"
parser_coverage:
  event_families: {}
  unknown_entries: 7
  truncation_count: 0
  drift_report_status: "review"
  unknown_signatures: 4
  unmatched_api_names: 3
  unmatched_request_api_names: 3
  routed_event_families: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Unknown-entry drift evidence is review-only and does not prove parser support, parser correctness, live private drift health, diagnostics readiness, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
  external_logs_included: false
  decklists_included: false
```

The session ledger may describe counts and report-reference evidence, but it
must not include raw log lines, raw entry bodies, raw payload objects, private
paths, external corpus filenames, local diagnostics outputs, SQLite files,
runtime artifacts, decklists, workbook exports, credentials, or live private
report contents.

### Unknown Entry Evidence Model

The report-only evidence model may claim unknown-entry coverage only when
focused tests demonstrate all of the following:

- A committed normalized drift report reference exists and is validated.
- Unknown entries are counted as unknown entries, not routed parser events.
- `parser_event_families` for the corpus row remains empty.
- Unknown signatures, unmatched API names, and unmatched request API names are
  review samples only.
- Diagnostics status becomes `review` when unknown evidence is present.
- Unknown samples are sanitized and do not include raw log bodies, local paths,
  webhook endpoints, credentials, account identity, or private payloads.
- Evidence-ledger Tier 6 continues to document `unknown_entry_count` as scoped
  to one analyzed input.
- Numeric zero remains valid only for a particular analyzed input; it is not a
  global no-drift claim.

If existing focused tests already prove the evidence model, Codex C may cite
them and keep drift/diagnostics tests unchanged. If any one of the above is not
explicitly covered, Codex C may add focused tests without touching
implementation behavior.

### Non-Claims

The unknown-entry corpus row must not claim:

- parser support for unknown semantic content;
- new parser event kinds;
- automatic parser-gap issue creation;
- log rotation coverage;
- missing message type recovery;
- reconnect, firewall, or network-drop coverage;
- private-log drift health;
- live diagnostics readiness;
- private smoke success;
- diagnostics readiness;
- release readiness;
- production behavior;
- analytics truth;
- AI truth;
- coaching truth;
- hidden-card, decklist, or archetype truth.

## Inputs

Allowed inputs:

- the current issue #377 problem representation and tracker #158 context;
- existing Mythic Edge corpus manifest and session ledger JSON;
- existing normalized drift report reference:
  `tests/fixtures/player_log_drift_flush_timing_expected.json`;
- existing drift fixture metadata:
  `tests/fixtures/golden_fixture_manifest.json`;
- existing drift sensor tests;
- existing parser diagnostics tests;
- existing evidence-ledger Tier 6 tests;
- current `codex/parser-parity` source and tests;
- public Manasight category names only through already merged taxonomy
  artifacts, if needed for wording.

Forbidden inputs:

- new log-like fixture files;
- modifications to the existing drift input fixture;
- local private MTGA logs;
- live private diagnostics reports;
- Manasight logs or external corpus payloads;
- generated databases;
- runtime status files;
- delivery retry artifacts;
- workbook exports;
- credentials, tokens, API keys, webhook endpoints, or secrets;
- OpenAI/model-provider output.

## Outputs

Future Codex C should produce:

- an updated corpus manifest entry for
  `unknown_entry_drift_report_reference_v1`;
- an updated session ledger entry for
  `unknown_entry_drift_report_reference_v1`;
- focused corpus parity tests proving the row, session ledger, coverage matrix,
  summary count, and non-claims;
- focused drift/diagnostics/evidence-ledger tests only if existing tests do
  not already prove the evidence model;
- `docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md`;
- `docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md`.

Expected report behavior after implementation:

- `log_runtime.unknown_entry` should become `covered_report_only`.
- `covered_report_only` should increase by one.
- `missing` should decrease by one.
- `covered_synthetic` should remain unchanged.
- `parser_event_families` for the new entry should remain empty.
- The overall corpus parity report should remain
  `partial_coverage_map_ready` while other gaps remain.
- `log_runtime.rotation`, `connection.reconnect`,
  `connection.firewall_or_network_drop`, and
  `mythic_edge.private_log_report_only_drift` should remain unchanged.

## Invariants

- Corpus parity metadata must remain report-only.
- No new log-like fixture file may be added in this slice.
- The existing drift input fixture must not be edited in this slice.
- No private, external, generated, delivery, workbook, or credential artifact
  may be committed.
- `source_privacy.raw_private_log_committed`,
  `source_privacy.external_logs_committed`, and
  `source_privacy.local_private_artifacts_committed` must remain `false`.
- `log_runtime.unknown_entry` must have exactly one new Mythic Edge entry in
  this slice.
- The new manifest entry and session ledger entry must use the same stable id:
  `unknown_entry_drift_report_reference_v1`.
- The coverage status must be `covered_report_only`.
- The coverage basis must include `diagnostics_only`,
  `fixture_metadata_only`, and `evidence_ledger_only`.
- `parser_event_families` must remain empty because unknown entries emit no
  trusted parser event family.
- Unknown signatures and unmatched API names must remain review samples, not
  parser facts.
- The implementation must not change parser behavior or protected surfaces.

## Error Behavior

- If `log_runtime.unknown_entry` is already covered by another entry, Codex C
  must stop and route back to Codex B rather than adding a duplicate.
- If the normalized drift report reference contains raw bodies, private paths,
  volatile timestamps, runtime report paths, secrets, or unredacted endpoints,
  Codex C must stop and route to D or B depending on whether the test/reference
  is wrong or the contract needs clarification.
- If unknown-entry coverage requires changing router, parser, diagnostics,
  drift, evidence-ledger, golden replay, feature-equity, runtime status,
  workbook, webhook, Apps Script, analytics, AI, CI, release, or production
  behavior, Codex C must stop and route back to Codex A or B.
- If validation finds forbidden private/external/generated content in the
  manifest, session ledger, tests, handoff, or report, Codex C must remove it
  from scope and rerun privacy checks before review.

## Side Effects

Codex B side effects:

- writes this contract only.

Future Codex C side effects authorized by this contract:

- edit committed corpus metadata and focused tests;
- write implementation handoff and contract-test report docs.

No runtime state, local private artifacts, generated databases, workbook tabs,
webhooks, Apps Script deployments, GitHub Actions gates, issues, PRs, trackers,
or production surfaces are changed by this contract.

## Dependency Order

1. Confirm branch base is `codex/parser-parity` at or after
   `3a0ae4598af3bcffa5170decf1e7cf816bb29c6d`.
2. Re-read this contract, issue #377, and the drift/diagnostics/evidence-ledger
   authority docs.
3. Verify existing drift, diagnostics, evidence-ledger, and corpus tests still
   prove the evidence model.
4. Add the manifest entry and session ledger entry.
5. Update `tests/test_corpus_parity_report.py` for the new entry, session
   ledger shape, coverage matrix row, summary counts, and non-claims.
6. Add focused drift/diagnostics/evidence-ledger tests only if required by the
   evidence model.
7. Run validation.
8. Write the implementation handoff and contract-test report.

## Compatibility

- Existing corpus manifest and session ledger schema versions remain
  unchanged.
- Existing corpus CLI and report JSON shape remain unchanged.
- Existing drift report object and normalized report reference shape remain
  unchanged.
- Existing diagnostics report object and report semantics remain unchanged.
- Existing evidence-ledger schema/vocabulary remains unchanged.
- Existing golden fixture manifest remains the source of drift fixture
  provenance; Codex C does not need to edit it unless a test exposes a
  contract mismatch.
- Existing coverage statuses and coverage basis vocabulary remain unchanged.

## Tests Required

Minimum Codex C validation:

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py
python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m ruff check src tests
git diff --check
python3 tools/check_agent_docs.py
```

Recommended privacy/protected-surface validation:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_unknown_entry_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_log_drift_sensor.py \
  tests/test_parser_diagnostics_mode.py \
  tests/test_evidence_ledger.py \
  docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_unknown_entry_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_log_drift_sensor.py \
  tests/test_parser_diagnostics_mode.py \
  tests/test_evidence_ledger.py \
  docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_unknown_entry_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_log_drift_sensor.py \
  tests/test_parser_diagnostics_mode.py \
  tests/test_evidence_ledger.py \
  docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md \
  | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

If `tools/check_secret_patterns.py` is unavailable on this branch, Codex C must
record that explicitly and rely on corpus report forbidden-content validation,
`git diff --check`, and manual changed-file inspection.

Optional adjacency checks if report semantics are touched:

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
```

## Acceptance Criteria

- `docs/contracts/parser_corpus_unknown_entry_coverage.md` exists and is the
  contract source for issue #377.
- The corpus manifest contains exactly one
  `unknown_entry_drift_report_reference_v1` entry.
- The session ledger contains exactly one
  `unknown_entry_drift_report_reference_v1` session.
- `log_runtime.unknown_entry` reports `covered_report_only`.
- `covered_synthetic` does not change for this issue.
- `parser_event_families` remains empty for the new entry.
- Existing drift/diagnostics/evidence-ledger tests prove unknown entries are
  review evidence, not parser-understood facts.
- Corpus report validation passes with no forbidden private or external
  content findings.
- Focused corpus tests prove the manifest row, session row, report matrix row,
  summary count changes, and non-claim wording.
- No parser behavior, protected surface, raw/private artifact, external corpus
  import, analytics truth, AI truth, coaching behavior, release policy, or
  production behavior changes.
- Codex C produces an implementation handoff and a contract-test report.

## Open Questions And Suspected Gaps

- The current schema has `committed_count_only_report` but not a more precise
  `committed_normalized_report_reference` source kind. This contract uses the
  existing vocabulary and does not authorize schema expansion.
- The normalized drift report reference is derived from an existing sanitized
  log-like fixture, but the parser corpus manifest should point to the
  normalized report reference rather than to the log-like input.
- The current reference has `routed_event_kinds: {}`. That is expected for
  unknown-entry coverage and must not be reinterpreted as parser event
  coverage.
- Broader live drift, private report-only drift, missing-message-type, and log
  rotation coverage remain future work.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #377, unknown-entry corpus coverage.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/377
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/375
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/376
- Previous merge commit: 3a0ae4598af3bcffa5170decf1e7cf816bb29c6d
- Base branch: codex/parser-parity
- Implementation branch: codex/parser-corpus-unknown-entry-coverage
- Contract: docs/contracts/parser_corpus_unknown_entry_coverage.md
- Expected handoff: docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md
- Expected report: docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md

Goal:
Implement the smallest metadata/test-only package needed to mark exactly log_runtime.unknown_entry as covered_report_only in the parser corpus parity report, using existing normalized drift/diagnostics/evidence-ledger unknown-entry evidence.

Do:
- Compare current corpus manifest, session ledger, drift tests, diagnostics tests, evidence-ledger tests, and corpus report behavior against the contract before editing.
- Add the unknown_entry_drift_report_reference_v1 manifest entry and session ledger entry.
- Update tests/test_corpus_parity_report.py for the new entry, session entry, matrix row, summary counts, and non-claims.
- Add focused drift, diagnostics, or evidence-ledger tests only if existing tests do not prove the contracted unknown-entry evidence model.
- Produce docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md.
- Produce docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md.

Do not:
- Change parser behavior, router semantics, diagnostics report shape, drift report behavior, evidence-ledger behavior, golden replay behavior, feature-equity behavior, runtime status artifacts, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge policy, deploy policy, or production behavior.
- Mark log_runtime.rotation, connection.reconnect, connection.firewall_or_network_drop, drift_debug.missing_message_type, drift_debug.rename_or_rotation_collision, mythic_edge.live_diagnostics, mythic_edge.private_log_report_only_drift, analytics readiness, AI, coaching, or release-readiness families as covered.
- Add new log-like fixtures or change the existing drift input fixture.
- Claim parser support for unknown semantic content, new parser event kinds, automatic parser-gap issue creation, live private drift health, diagnostics readiness, private smoke success, release readiness, analytics truth, AI truth, coaching truth, or full corpus parity.
- Add any forbidden private, external, generated, delivery, workbook, or credential artifact named in the contract.
- Target main directly.
- Close tracker #158 or issue #377.
- Stage or commit unless explicitly asked.

Validation:
Run at minimum:
python3 -m pytest -q tests/test_corpus_parity_report.py
python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m ruff check src tests
git diff --check
python3 tools/check_agent_docs.py

Also run changed-file secret/protected-surface/selector checks if the tools are available on this branch.

End with:
- role performed
- files changed
- validation run
- remaining risks
- next recommended role
- workflow_handoff block to Codex E
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/377"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/376"
  previous_merge_commit: "3a0ae4598af3bcffa5170decf1e7cf816bb29c6d"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_unknown_entry_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_unknown_entry_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_unknown_entry_coverage.md"
  verdict: "contract_ready_for_report_only_unknown_entry_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-unknown-entry-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py"
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m ruff check src tests"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158 or issue #377."
    - "Do not change parser behavior, router semantics, diagnostics report shape, drift report behavior, evidence-ledger behavior, golden replay behavior, feature-equity behavior, runtime status artifacts, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge policy, deploy policy, or production behavior."
    - "Do not mark adjacent log-runtime, connection, drift-debug, live-diagnostics, private-log-drift, analytics-readiness, AI, coaching, or release-readiness families as covered."
    - "Do not add new log-like fixtures or change the existing drift input fixture."
    - "Do not claim parser support for unknown semantic content, new parser event kinds, automatic parser-gap issue creation, live private drift health, diagnostics readiness, private smoke success, release readiness, analytics truth, AI truth, coaching truth, or full corpus parity."
    - "Do not commit any forbidden private, external, generated, delivery, workbook, or credential artifact named in this contract."
```
