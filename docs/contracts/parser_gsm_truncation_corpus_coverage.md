# Parser GSM Truncation Corpus Coverage Contract

## Module

GSM truncation/data-loss corpus coverage for the parser corpus parity report.

Plain English: this slice should let Mythic Edge's corpus parity report say
that the `drift_debug.gsm_truncation` scenario family has safe committed
synthetic coverage for the parser-owned truncation/data-loss signal. It must
not change how truncation is parsed, reconstruct omitted GameState data, or
turn corpus coverage into parser truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/351
- Previous completed child issue: https://github.com/Tahjali11/Mythic-Edge/issues/291
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/292
- Previous merge commit: `46bf9f87a77fa943fd18e2e5151737d077ea8308`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/gsm-truncation-corpus-coverage`
- base_branch: `main`
- observed_base_commit: `3b55867cfc7e3ffbc06c544727b3ac01edd174ab`
- target_artifact: `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- expected_next_artifact: `docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md`
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
- `docs/contracts/parser_gsm_truncation.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/truncation.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_gsm_truncation_parser.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`

## Owning Layer

Owning layer: Corpus / Provenance.

The parser owns the deterministic `TruncationEvent` and the fact that a GSM
truncation marker is parser-observed data-loss evidence. The corpus parity
module owns only metadata and report coverage for whether that scenario family
has safe committed, synthetic, report-only, partial, missing, or blocked
coverage.

## Internal Project Area

Corpus / Provenance.

This slice reads Parser evidence and tests, but it is not a Parser behavior
module. The contract is a corpus/report contract over existing parser-owned
GSM truncation support.

## Truth Owner

Truth owner for truncation interpretation:

- `src/mythic_edge_parser/parsers/truncation.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/router.py`

Truth owner for corpus coverage status:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`

The corpus coverage status is review metadata. It is not parser truth,
diagnostics truth, replay truth, workbook truth, analytics truth, AI truth,
merge readiness, deploy readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing parser-owned TruncationEvent and focused parser/diagnostics/drift tests
  -> parser corpus manifest/session-ledger metadata
  -> corpus parity compatibility report row for drift_debug.gsm_truncation
```

Forbidden reverse flow:

- Corpus report status must not change parser behavior.
- Corpus metadata must not change `TruncationEvent` shape.
- Corpus coverage must not alter router semantics, diagnostics behavior,
  golden replay behavior, final reconciliation, workbook output, analytics, or
  AI/coaching behavior.
- Corpus coverage must not reconstruct omitted GameState objects, zones,
  actions, annotations, timers, card facts, match facts, or game facts.

Protected surfaces explicitly not touched:

- parser behavior
- `TruncationEvent` payload shape
- router dispatch semantics
- diagnostics report semantics
- golden replay report semantics
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- runtime status artifacts
- failed delivery artifacts
- SQLite/local app/analytics behavior
- OpenAI/model-provider behavior
- production behavior

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`

Future implementation files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md`
- `docs/contract_test_reports/parser_gsm_truncation_corpus_coverage.md`

Existing files that may be read, but not changed unless Codex C discovers a
contract-test-only reason and records it:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_gsm_truncation_parser.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`

Out of scope unless a later contract explicitly authorizes it:

- `src/mythic_edge_parser/parsers/truncation.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- golden replay fixture files or expected manifests
- feature-equity corpus baseline files
- parser event schema snapshots
- workbook, webhook, Apps Script, local app, analytics, AI, and production
  surfaces

## Public Interface

The public interface remains the existing corpus parity report API:

```python
def build_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def validate_corpus_manifest(payload: Mapping[str, Any]) -> list[str]:
    ...

def validate_session_ledger(payload: Mapping[str, Any]) -> list[str]:
    ...
```

The contracted report row is the existing `coverage_matrix` entry whose
`scenario_family` is `drift_debug.gsm_truncation`.

No new public Python API is required for this slice.

No new CLI flag is required for this slice.

No new environment variable is authorized.

## Observed Current Behavior

Observed from current `origin/main` after PR #292 and roadmap PR #293:

- Issue #351 is open.
- Tracker #158 is open.
- Issue #291 is closed and PR #292 was squash-merged into `main`.
- `src/mythic_edge_parser/app/corpus_parity_report.py` defines the corpus
  manifest, session ledger, scenario taxonomy, and compatibility report.
- The current corpus parity report command returns:

```text
Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 28 missing)
```

- The current report keeps `drift_debug.gsm_truncation` at `partial` because
  the only current corpus entry for that family is
  `feature_equity_corpus_baseline_v1`, which is `count_ratchet_only`.
- The existing parser already supports first-class GSM truncation markers:
  - `EntryHeader.TRUNCATION_MARKER`
  - `TRUNCATION_MARKER_PREFIX`
  - `parsers.truncation.try_parse(...)`
  - `TruncationEvent`
  - router dispatch through the truncation parser bucket
  - diagnostics and drift tests that count truncation/data-loss evidence
- Focused current tests pass for corpus parity plus GSM truncation parser
  behavior.

## Inputs

### Corpus Manifest Entry

Type: JSON object inside `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.

Required V1 entry id:

```text
gsm_truncation_marker_synthetic_v1
```

Required fields:

```yaml
entry_id: "gsm_truncation_marker_synthetic_v1"
entry_type: "session_ledger_entry"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/351"
authorized_by_contract: "docs/contracts/parser_gsm_truncation_corpus_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  focused_parser_test: "tests/test_gsm_truncation_parser.py"
  diagnostics_test: "tests/test_parser_diagnostics_mode.py"
  drift_test: "tests/test_log_drift_sensor.py"
scenario_families:
  - "drift_debug.gsm_truncation"
parser_event_families:
  - "Truncation"
parser_claim_families:
  - "truncation_data_loss_evidence"
coverage_status: "covered_synthetic"
coverage_basis:
  - "parser_behavior_verified"
  - "fixture_metadata_only"
  - "diagnostics_only"
known_gaps:
  - "Synthetic marker coverage proves data-loss detection only; it does not reconstruct omitted GameState data."
review_notes:
  - "GSM truncation is parser-owned data-loss evidence, not recovered GameState truth."
```

The exact path keys may be adjusted during Codex C if tests show a narrower
shape fits the existing validator better, but the paths must stay committed
repo-relative documentation or test paths. They must not point to raw logs,
external corpora, private local artifacts, generated reports, SQLite files, or
runtime artifacts.

### Session Ledger Entry

Type: JSON object inside `tests/fixtures/parser_corpus/session_ledger.v1.json`.

Required V1 session id:

```text
gsm_truncation_marker_synthetic_v1
```

Required fields:

```yaml
session_id: "gsm_truncation_marker_synthetic_v1"
title: "Synthetic GSM truncation data-loss marker"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
scenario_families:
  - "drift_debug.gsm_truncation"
format_family: "parser_drift_debug"
match_shape: "not_applicable_data_loss_marker"
record_summary: "synthetic_marker_summary_only"
parser_coverage:
  event_families:
    Truncation: 1
  unknown_entries: 0
  truncation_count: 1
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Truncation marker coverage does not recover omitted GameState objects, annotations, zones, actions, timers, or game facts."
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
```

The ledger entry may summarize the marker as synthetic and redacted, but it
must not paste raw private `Player.log` excerpts or raw payload objects.

### Existing Parser Evidence

Allowed evidence sources for the V1 coverage claim:

- `tests/test_gsm_truncation_parser.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`
- existing `parser_gsm_truncation.md` contract

These are supporting evidence sources only. The corpus manifest/session ledger
must not derive new parser facts from test text.

## Outputs

### Corpus Parity Report Row

When the report is built from the updated manifest and session ledger, the row
for `drift_debug.gsm_truncation` must satisfy:

```yaml
scenario_family: "drift_debug.gsm_truncation"
coverage_status: "covered_synthetic"
coverage_basis:
  - "count_ratchet_only"
  - "diagnostics_only"
  - "fixture_metadata_only"
  - "parser_behavior_verified"
mythic_edge_entries:
  - "feature_equity_corpus_baseline_v1"
  - "gsm_truncation_marker_synthetic_v1"
notes:
  - "..."
```

The exact order of `coverage_basis`, entries, and notes may follow the current
report sorting rules.

The row must not use `covered_committed` in V1. A future sanitized real-log
fixture could justify `covered_committed`, but only through a separate scoped
issue or contract because it would require fixture provenance and privacy
review.

### Corpus Parity Summary

Under the current 45-family taxonomy and current manifest shape, Codex C
should expect the report summary to move from:

```yaml
covered_synthetic: 1
partial: 4
```

to:

```yaml
covered_synthetic: 2
partial: 3
```

Other summary counts should remain unchanged unless Codex C finds current
`main` has moved again. If counts differ because main moved, Codex C must
document the current baseline in the implementation handoff.

The top-level report status may remain `partial_coverage_map_ready` because
many other scenario families remain missing, partial, or blocked. This issue
does not try to complete tracker #158.

## Invariants

- GSM truncation corpus coverage is about observing a data-loss marker, not
  recovering omitted GameState data.
- `0` truncation counts in existing sessions remain valid explicit absence
  counts.
- A synthetic truncation marker may move `drift_debug.gsm_truncation` to
  `covered_synthetic`; it must not move it to `covered_committed`.
- No corpus fixture or report may contain raw/private `Player.log` excerpts,
  raw payload objects, private paths, external corpus content, generated
  runtime artifacts, SQLite files, workbook exports, secrets, credentials,
  tokens, API keys, or webhook URLs.
- Existing parser, router, diagnostics, replay, workbook, webhook, Apps
  Script, analytics, AI, and production behavior must remain unchanged.
- Existing `TruncationEvent` payload shape remains parser-owned and unchanged.
- Corpus parity reports remain metadata/review artifacts only.
- The report must not infer hidden facts, missing game objects, annotations,
  actions, timers, match/game identity, winners, or final reconciliation from
  the marker.

## Error Behavior

Malformed manifest or session-ledger additions must fail validation through
the existing corpus parity validators rather than being silently accepted.

If Codex C cannot represent the coverage without adding a new schema enum,
changing parser code, changing diagnostics behavior, changing golden replay
behavior, or committing a log-like fixture, it must stop and route back to
Codex B with a contract clarification.

If a proposed fixture or metadata path trips secret/private-marker or
protected-surface checks, Codex C must stop and either remove the risky
artifact or route to Codex D only for a concrete checker finding.

If current `main` has changed enough that the expected summary counts are no
longer valid, Codex C may update expected counts in tests only after recording
the observed current baseline in the implementation handoff.

## Side Effects

Allowed side effects for Codex C:

- edit the corpus manifest fixture;
- edit the session ledger fixture;
- edit focused corpus parity report tests;
- write an implementation handoff;
- optionally write a contract-test report if the workflow reaches Codex E.

Forbidden side effects:

- parser behavior changes;
- parser event class changes;
- router behavior changes;
- diagnostics behavior changes;
- golden replay behavior changes;
- feature-equity baseline changes unless a later contract explicitly routes
  that work;
- generated report artifacts committed to the repo;
- runtime status writes;
- SQLite or local app artifact writes;
- webhook/App Script/Google Sheets/output transport changes;
- AI/model-provider calls or behavior.

## Dependency Order

Codex C should implement in this order:

1. Capture the current corpus parity report row and summary for
   `drift_debug.gsm_truncation`.
2. Add the synthetic GSM truncation manifest entry.
3. Add the matching session-ledger entry.
4. Update focused corpus parity report tests to assert the row, summary delta,
   privacy posture, and non-truth limitations.
5. Run focused corpus/truncation validation.
6. Write the implementation handoff.

Do not change parser or diagnostics code to make corpus tests pass.

## Compatibility

The following must remain compatible:

- `parser_corpus_manifest.v1`
- `parser_corpus_session_ledger.v1`
- `parser_corpus_compatibility_report.v1`
- existing `COVERAGE_STATUSES`
- existing `COVERAGE_BASIS_VALUES`
- existing corpus parity CLI invocation
- existing `TruncationEvent` shape and parser contract
- existing tests for GSM truncation parser behavior
- existing feature-equity baseline semantics

This contract does not authorize `parser_corpus_manifest.v2`, new coverage
status labels, or new parser event fields.

## Tests Required

Codex C should run:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

If protected-surface tooling emits an authorization warning, Codex C/E should
run the repo's surface-authorization checker if present and document whether
the warning is expected metadata-only corpus fixture drift.

Codex E should additionally verify:

- no raw/private log-like file was added;
- no external corpus file or Manasight source was copied;
- no generated report artifact was committed;
- the `drift_debug.gsm_truncation` row is `covered_synthetic`, not
  `covered_committed`;
- the report limitations still state that corpus coverage does not prove
  parser correctness or readiness;
- all changed paths are within the authorized docs/fixtures/tests/handoff
  scope.

Codex F should stage only reviewed files.

Codex G should not close tracker #158 unless explicitly instructed by the
user.

## Acceptance Criteria

- `docs/contracts/parser_gsm_truncation_corpus_coverage.md` exists.
- Codex C can update corpus manifest/session-ledger metadata without parser
  behavior changes.
- The corpus parity report row for `drift_debug.gsm_truncation` becomes
  `covered_synthetic` through the authorized synthetic coverage entry.
- The report keeps truncation as data-loss evidence only.
- The report does not claim recovered GameState data.
- Secret/private-marker and protected-surface checks pass for changed files.
- No raw/private/external/generated/local artifacts are committed.
- The implementation handoff records current counts, changed files,
  validation, and remaining corpus gaps.

## Open Questions And Contract Risks

- Future work may decide to add a golden replay synthetic truncation fixture,
  but this contract does not require it. If Codex C finds a golden replay
  fixture is necessary, it must stay synthetic/sanitized and must not change
  golden replay behavior.
- Future work may decide to update the feature-equity corpus baseline to count
  a truncation fixture. This contract does not authorize that update.
- A future sanitized real-log fixture could move the family to
  `covered_committed`; this contract intentionally keeps V1 at
  `covered_synthetic`.
- The broader tracker still has many missing, partial, or blocked scenario
  families. This issue should not be treated as corpus parity completion.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #351 under tracker #158.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/351

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Branch:
  codex/gsm-truncation-corpus-coverage

  Contract:
  docs/contracts/parser_gsm_truncation_corpus_coverage.md

  Goal:
  Implement the smallest metadata/test update needed to add honest GSM
  truncation/data-loss corpus coverage to the parser corpus parity report.

  Do:
    - Compare current corpus parity behavior against the contract before editing.
    - Update tests/fixtures/parser_corpus/corpus_manifest.v1.json with the
      contracted synthetic GSM truncation coverage entry.
    - Update tests/fixtures/parser_corpus/session_ledger.v1.json with the
      contracted synthetic GSM truncation session entry.
    - Update focused corpus parity tests so drift_debug.gsm_truncation becomes
      covered_synthetic, not covered_committed.
    - Preserve existing parser-owned GSM truncation behavior and report
      boundaries.
    - Produce docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md.

  Do not:
    - Change parser behavior, TruncationEvent shape, router behavior,
      diagnostics behavior, golden replay behavior, replay behavior, workbook
      schema, webhook payload shape, Apps Script behavior, analytics truth, AI
      truth, or production behavior.
    - Commit raw/private Player.log excerpts, external raw corpora, local logs,
      generated data, runtime artifacts, SQLite files, workbook exports,
      secrets, credentials, tokens, API keys, or webhook URLs.
    - Reconstruct missing GameState data.
    - Broaden this issue into unknown-entry, log rotation, reconnect,
      Conjure/Spellbook, analytics, AI, overlay, Match Journal, workbook,
      webhook, Apps Script, or production behavior.
    - Stage or commit unless explicitly asked.

  Validation:
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py
    - python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py
    - python3 -m ruff check src tests tools
    - python3 tools/check_agent_docs.py
    - git diff --check
    - git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
    - git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
    - git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/351"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_gsm_truncation_corpus_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md"
  verdict: "contract_ready_for_metadata_test_implementation"
  risk_tier: "High"
  branch: "codex/gsm-truncation-corpus-coverage"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not change parser behavior, TruncationEvent shape, router behavior, diagnostics behavior, replay behavior, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, or production behavior."
    - "Do not commit raw/private Player.log excerpts, external raw corpora, local logs, generated data, runtime artifacts, SQLite files, workbook exports, secrets, credentials, tokens, API keys, or webhook URLs."
    - "Do not reconstruct missing GameState data from truncation markers."
    - "Do not broaden this issue beyond GSM truncation/data-loss corpus coverage."
    - "Do not close tracker #158."
```
