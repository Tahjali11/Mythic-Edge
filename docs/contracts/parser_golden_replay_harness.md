# Parser Golden Replay Harness Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/48

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/49

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/110

Previous merge commit: `a61ed4e5cd8898e25913796080a9c46e66fcff8a`

Branch target: `codex/parser-reliability-intelligence`

This contract defines the v1 golden replay harness for committed sanitized
`Player.log` fixture slices. It is a contract artifact only. It does not
implement code, create fixtures, update expected output, change parser
behavior, change parser state final reconciliation, or authorize raw private
log material in the repository.

## Module

Parser golden replay harness.

Plain English: the harness should replay small committed sanitized
`Player.log` slices through the normal Mythic Edge parser path and compare the
parser-owned observed outputs against explicit expected manifests. It should
make parser drift obvious without becoming a second parser, a workbook truth
source, or a snapshot update shortcut.

Risk tier: High.

The code surface is test/harness-oriented, but the risk is high because a
misdesigned golden replay pass can create false confidence, bless private log
content, hide missing parser evidence, or silently move truth out of parser
modules and state.

## Owning Layer

Owning layer: parser reliability test harness.

Parser truth boundary:

- MTGA `Player.log` is local observable evidence, not absolute game truth.
- `LineBuffer`, `Router`, parser modules, event classes, and parser state own
  parser interpretation.
- The golden replay harness observes parser-owned outputs and compares them to
  expected manifests.
- The harness must not own parser semantics, reconstruct missing `GameState`
  data, infer hidden game facts, override final reconciliation, or promote
  downstream workbook/dashboard/API behavior into parser truth.
- Workbook formulas, dashboard logic, Apps Script, webhook delivery, output
  transport, and AI/analytics output remain downstream consumers.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_golden_replay_harness.md`

Future implementation artifacts owned by this contract, if authorized by the
Codex C implementation pass:

- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/test_golden_replay_harness.py`
- `docs/implementation_handoffs/parser_golden_replay_harness_comparison.md`
- optional committed manifest files under a focused fixture location such as
  `tests/fixtures/golden_replay/`

Related files referenced but not silently owned:

- `docs/contracts/parser_diagnostics_mode.md`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `tests/test_parser_diagnostics_mode.py`
- `docs/contracts/parser_saved_event_replay.md`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `tests/test_saved_event_replay.py`
- `tests/test_parser_regressions.py`
- `tests/fixtures/parser_regression_match_slice.log`
- `tests/fixtures/parser_regression_match_expected.json`
- `tests/fixtures/parser_regression_bo3_slice.log`
- `tests/fixtures/parser_regression_bo3_expected.json`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`

## Public Interface

V1 should expose a small local API. Exact Python names may vary during
implementation, but the public behavior must preserve this shape:

```python
def build_golden_replay_report(
    manifest_paths: Sequence[Path],
) -> dict[str, Any]:
    ...

def run_golden_replay(
    manifest_path: Path,
) -> GoldenReplayFixtureResult:
    ...

def main(argv: Sequence[str] | None = None) -> int:
    ...
```

Required public expectations:

- A local CLI should be available through a Python module entrypoint, for
  example `python3 -m mythic_edge_parser.app.golden_replay`.
- The CLI should accept explicit manifest paths or a directory of committed
  manifests.
- Generated reports must be local review artifacts. They must not be committed
  by default and must not change runtime status file schema.
- The harness must return nonzero on `fail`, `diff`, or unexpected `review`
  outcomes. A later implementation may choose whether expected `degraded`
  outcomes return zero, but that decision must be explicit in tests and report
  metadata.
- The harness must not read private local logs implicitly. Inputs must be
  explicit committed sanitized fixtures referenced by manifests.
- No environment variable contract is required for v1.

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence` during this contract pass:

- Issue #48 is open and belongs to tracker #47.
- Tracker #47 is open.
- Local HEAD is the #110 merge commit for parser diagnostics mode.
- `docs/contracts/parser_diagnostics_mode.md`,
  `src/mythic_edge_parser/app/parser_diagnostics.py`, and
  `tests/test_parser_diagnostics_mode.py` are present.
- `src/mythic_edge_parser/app/parser_diagnostics.py` can build a local
  diagnostics report for a fixture, local log, or live-game profile. It uses
  existing parser/router/drift/runtime evidence and does not act as a second
  parser.
- `src/mythic_edge_parser/app/saved_event_replay.py` replays generated JSONL
  saved event records, reconstructs supported event classes, deduplicates by
  `raw_bytes_hash`, and does not parse raw `Player.log` slices.
- `tests/test_parser_regressions.py` already contains a local replay pattern:
  it resets parser state, seeds a card lookup, reads sanitized fixture `.log`
  files, skips comment lines, feeds lines through `LineBuffer`, routes entries
  through `Router`, updates parser state, collects event traces, and compares
  broad JSON snapshots.
- Current parser regression fixtures cover a Bo1 match and a Bo3 match with
  rank, match start, client actions, game state, game result, sideboarding,
  match summary rows, match log rows, game log rows, and router stats.
- Current expected snapshots are broad whole-object oracles. They are useful
  regression coverage, but they do not provide a manifest layer that separates
  parser-owned facts, known gaps, expected degradation, privacy metadata, and
  update authorization.
- The golden fixture policy contract defines sanitized fixture requirements,
  redaction rules, expected-output pairing, and update/review policy.
- The Player.log evidence ledger contract defines value-source, confidence,
  finality, drift, degradation, and fixture-gap vocabulary that future golden
  replay reports may reference.

## Required Guarantees

### Harness Purpose

The harness must:

- replay committed sanitized `Player.log` fixture slices through the normal
  parser path;
- compare parser-owned observed outputs against explicit expected manifests;
- produce deterministic local reports that classify each fixture as `pass`,
  `degraded`, `review`, `diff`, or `fail`;
- make missing parser events, changed match/game identity, lost
  truncation/data-loss evidence, changed final reconciliation facts, and
  unexpected unknowns visible;
- help Codex C, D, and E threads diagnose parser drift without inventing facts.

The harness must not:

- parse through an alternate parser;
- infer match, game, card, or winner facts from incomplete evidence;
- reconstruct missing `GameState` data;
- treat workbook rows, dashboard calculations, Apps Script behavior, webhook
  payloads, or AI output as parser truth;
- silently update expected manifests;
- query or mutate live MTGA, live workbooks, live Apps Script, webhooks, failed
  posts, runtime status files, or generated data.

### Fixture Acceptance And Sanitization

V1 accepted inputs:

- committed sanitized `Player.log` slice files;
- committed synthetic log slices that are clearly labeled as synthetic;
- committed manifest JSON files that reference those slices by repository
  relative path.

Required fixture traits:

- minimal lines needed for the covered behavior;
- stable timestamps only when ordering, duration, or timestamp parsing matters;
- stable relationship-preserving placeholders for match IDs, user IDs, player
  names, seat IDs, team IDs, object IDs, and card IDs when those values are
  needed for parser behavior;
- comments only for fixture intent and sanitization context;
- no raw private local log excerpt unless it has been redacted and reviewed.

Forbidden fixture content:

- raw private `Player.log` files or full session dumps;
- real account IDs, display names, screen names, opponent identities, local
  user paths, machine names, access tokens, API keys, bearer tokens, webhook
  URLs, Apps Script deployment URLs, spreadsheet IDs, failed posts, runtime
  status files, workbook exports, generated card/tier data, or private
  free-text content;
- real-looking replacement PII;
- evidence invented to make a parser output look directly observed.

Required manifest privacy fields:

```yaml
fixture_id: "bo1_match_win_basic"
schema_version: "parser_golden_replay_manifest.v1"
source_kind: "sanitized_player_log_slice"
sanitization_status: "sanitized"
source_privacy_class: "sanitized_committable"
raw_private_log_committed: false
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
authorized_by_contract: "docs/contracts/parser_golden_replay_harness.md"
known_gaps: []
```

Allowed `source_kind` values:

- `sanitized_player_log_slice`
- `synthetic_player_log_slice`

Allowed `sanitization_status` values:

- `sanitized`
- `synthetic`
- `legacy_unclassified`
- `requires_review`

New fixtures must use `sanitized` or `synthetic`. Existing legacy fixtures may
be classified as `legacy_unclassified` only during a manifest retrofit, and
that status must produce a report note.

### Expected Manifest Shape

Each manifest must pair one replayable input fixture with reduced expected
parser-owned facts. Whole-object snapshots are allowed only when the manifest
explicitly says they are intentional and the expected output remains sanitized,
stable, and parser-owned.

Required logical shape:

```yaml
object: "mythic_edge_golden_replay_manifest"
schema_version: "parser_golden_replay_manifest.v1"
fixture_id: "bo1_match_win_basic"
description: "Sanitized Bo1 match win with rank, submit deck, GameState, and GameResult."
source:
  log_path: "tests/fixtures/golden_replay/bo1_match_win_basic.log"
  source_kind: "sanitized_player_log_slice"
  sanitization_status: "sanitized"
  source_privacy_class: "sanitized_committable"
  raw_private_log_committed: false
coverage:
  covered_event_families:
    - "MatchState"
    - "ClientAction"
    - "GameState"
    - "GameResult"
  known_gaps: []
  expected_degradation: []
  expected_truncation_signals: []
expected:
  router_stats:
    routed: 0
    unknown: 0
    timestamp_missing: 0
    timestamp_parse_failure: 0
  event_family_counts: {}
  event_kind_sequence: []
  diagnostics_summary:
    overall_status: "pass"
  truncation_and_data_loss:
    truncation_count: 0
    data_loss_events: []
  unknowns_and_degradation:
    unknown_entry_count: 0
    degraded_outputs: []
  parser_state:
    match_id: ""
    current_game_number: 1
    player_team: 1
  final_reconciliation:
    match_winner_team: ""
    match_result_type: ""
    match_result_reason: ""
  parser_owned_rows:
    match_log_row: {}
    game_log_rows: []
```

Expected facts should prefer small stable comparisons:

- router stats and timestamp anomalies;
- event family counts and, where useful, event kind sequence;
- diagnostics summary fields reused from diagnostics mode;
- truncation/data-loss observations;
- unknown/degraded evidence expectations;
- parser-state-owned match identity, game identity, winner, result, rank,
  play/draw, turn count, mulligan, opening-hand, sideboarding, and final
  reconciliation facts;
- selected parser-owned row values when they are produced by parser/state or
  parser transforms and are explicitly listed in the manifest.

Expected facts must not include:

- workbook formulas or dashboard-derived values;
- live workbook exports;
- webhook transport payload assertions;
- Apps Script behavior assertions;
- raw private payloads;
- local paths from temporary directories;
- volatile generated timestamps unrelated to the fixture;
- AI-generated interpretation.

### Report Shape

Required logical report shape:

```yaml
object: "mythic_edge_golden_replay_report"
schema_version: "parser_golden_replay_report.v1"
generated_at: "2026-05-18T00:00:00+00:00"
suite_status: "pass"
summary:
  manifests_total: 0
  pass: 0
  degraded: 0
  review: 0
  diff: 0
  fail: 0
  fixtures_with_truncation: 0
  fixtures_with_data_loss: 0
results:
  - fixture_id: "bo1_match_win_basic"
    status: "pass"
    manifest_path: "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json"
    fixture_path: "tests/fixtures/golden_replay/bo1_match_win_basic.log"
    privacy:
      sanitization_status: "sanitized"
      raw_private_log_committed: false
      review_required: false
    comparisons:
      router_stats: "pass"
      event_family_counts: "pass"
      diagnostics_summary: "pass"
      truncation_and_data_loss: "pass"
      parser_state: "pass"
      final_reconciliation: "pass"
      parser_owned_rows: "pass"
    diffs: []
    degradation: []
    review_notes: []
```

Allowed status values:

- `pass`: expected parser-owned facts matched and no expected degradation was
  present.
- `degraded`: expected parser-owned facts matched, but the manifest explicitly
  declared expected degradation such as truncation, data loss, unknown evidence,
  or fixture gaps.
- `review`: the replay completed, but the harness observed unexpected unknowns,
  unexpected degradation, legacy/unclassified fixture metadata, optional
  diagnostic warnings, or evidence that needs human review before it can be
  treated as clean regression coverage.
- `diff`: observed parser-owned output differs from the expected manifest.
- `fail`: fixture safety validation failed, the manifest is malformed, the
  fixture cannot be read, parser replay raises an exception, forbidden private
  material is detected by available checks, or required expected sections are
  missing.

Suite status precedence:

1. `fail`
2. `diff`
3. `review`
4. `degraded`
5. `pass`

Diff entries must identify the manifest path, fixture ID, comparison section,
JSON pointer or field path when available, expected value, observed value, and
whether the affected value is parser-owned truth, diagnostics evidence, or
privacy metadata. Diff output must not print raw private log lines.

### Relationship To Parser Diagnostics Mode

The golden replay harness may call or embed
`build_parser_diagnostics_report(..., profile="fixture")` to reuse diagnostics
mode vocabulary for parser health, event-family coverage,
truncation/data-loss, unknown/degraded classification, final reconciliation
evidence, and transport separation.

Required boundaries:

- Diagnostics mode remains an observer/report harness, not parser truth.
- Golden replay manifests may assert selected diagnostics summary fields, but
  diagnostics output must not replace parser-owned expected facts.
- Golden replay must not write `parser_diagnostics_latest.json` unless a user
  explicitly asks for a local diagnostics report path outside committed
  artifacts.
- Diagnostics transport-health fields must remain separate from parser-health
  and parser-output comparisons.

### Relationship To Saved Event Replay

`saved_event_replay.py` consumes generated saved-event JSONL records and
reconstructs event objects. The golden replay harness consumes sanitized raw
`Player.log` slice fixtures and exercises `LineBuffer`, `Router`, parser
modules, transforms, diagnostics evidence, and parser state.

Required boundaries:

- Saved event replay is not a substitute for raw fixture replay.
- Golden replay must not bypass `LineBuffer` or `Router` by replaying saved
  event JSONL when validating raw `Player.log` fixture coverage.
- Saved event replay tests remain relevant validation if event reconstruction
  mappings are touched, but they do not prove raw log parsing behavior.
- A future contract may add a separate saved-event golden replay mode, but v1
  does not.

### Fixture Minimization Policy

Golden fixtures must stay small enough to review. Prefer:

- one behavior family per fixture when feasible;
- one Bo1 fixture and one Bo3 fixture as baseline coverage before adding
  specialized cases;
- relationship-preserving placeholders instead of real identities;
- reduced expected facts over huge snapshots;
- explicit known gaps rather than padding the fixture with unrelated log
  material.

Allowed reasons to broaden a fixture:

- a parser behavior requires multi-event state interaction;
- final reconciliation requires game and match result evidence;
- sideboarding, mulligan, opening-hand, or play/draw facts require earlier
  context;
- truncation/data-loss classification requires adjacent marker evidence.

### Expected-Output Update Policy

There must be no automatic bless/update mode in v1.

Expected manifests may be updated only when:

- a separate issue and contract authorize the parser behavior change;
- the existing expected output is proven wrong under the current contract;
- a fixture is redacted or minimized without changing behavior;
- the manifest is being expanded to add privacy, coverage, or evidence-ledger
  metadata without changing observed parser-owned facts.

Every expected-output update must:

- cite the issue and contract;
- explain whether the change is behavior drift, redaction, minimization,
  metadata expansion, or fixture correction;
- include reviewable old/new diffs;
- keep parser-owned truth in parser modules and state;
- route to Codex E for contract-test review before submitter work.

Updating expected output just because a test failed is forbidden.

## Error Behavior

Malformed manifest:

- classify the fixture as `fail`;
- report the missing or invalid fields;
- do not attempt partial parser truth comparison.

Unreadable fixture:

- classify as `fail`;
- report the path relative to the repo when possible;
- do not search private local paths for a replacement.

Parser/router exception during replay:

- classify as `fail`;
- include sanitized exception class and message;
- do not print raw fixture lines except committed sanitized line numbers or
  short sanitized context if the implementation provides it.

Unexpected unknown or truncation evidence:

- classify as `review` unless expected by the manifest;
- classify as `degraded` when expected by the manifest and all expected facts
  otherwise match;
- classify as `diff` when expected truncation/data-loss evidence is missing or
  changed.

Private or forbidden content:

- classify as `fail` when available validators detect forbidden content;
- stop submitter/deployer work until the content is removed or redacted;
- do not accept the fixture as a golden oracle.

## Side Effects

Allowed future side effects:

- read committed sanitized fixture and manifest files;
- build in-memory replay results;
- write an optional local report only to an explicit user-provided path or a
  temporary test path;
- print sanitized report summaries to stdout;
- add committed manifest fixtures only under Codex C implementation scope and
  Codex E review.

Forbidden side effects:

- no parser behavior changes;
- no parser state final reconciliation changes;
- no workbook schema changes;
- no webhook payload shape changes;
- no Apps Script behavior changes;
- no output transport changes;
- no parser event class changes;
- no match/game identity or deduplication changes;
- no secrets or environment variable contract changes;
- no raw private log commits;
- no generated data commits;
- no runtime status file schema changes;
- no failed-post commits;
- no workbook export commits;
- no live MTGA or live workbook access in tests;
- no AI/model-provider calls.

## Compatibility

- Existing parser regression fixtures remain valid legacy regression coverage.
- Existing expected parser regression snapshots remain current oracles until a
  separate issue, contract, and review approve changes.
- Existing diagnostics mode report shape remains owned by
  `parser_diagnostics.py`; golden replay may consume selected fields but must
  not redefine diagnostics mode.
- Existing saved-event replay behavior remains owned by `saved_event_replay.py`.
- Existing parser event classes and event `kind` values remain unchanged.
- Existing workbook row fields and historical rows remain compatible.
- Existing protected-surface and fixture-policy contracts remain in force.

## Unknowns

- Whether v1 manifests should live in a dedicated
  `tests/fixtures/golden_replay/` directory or beside the existing regression
  fixtures.
- Whether existing `parser_regression_*` fixtures should be migrated into
  golden replay manifests immediately or left as legacy regression snapshots
  until touched.
- Whether v1 should compare reduced selected facts only or also preserve a
  small optional whole-snapshot comparison for current broad regression
  coverage.
- Whether expected `degraded` outcomes should produce a zero CLI exit code by
  default.
- Whether future evidence-ledger metadata should become required in golden
  manifests before the evidence ledger has a machine-readable implementation.
- Whether a future secret/private-marker scanner will be available on this
  branch and become required for fixture acceptance.

## Suspected Gaps

- There is no dedicated golden replay module yet.
- There is no machine-readable manifest layer for current parser regression
  fixtures.
- Current expected snapshots are broad and useful but do not separately label
  parser-owned facts, diagnostics evidence, privacy metadata, known gaps, and
  expected degradation.
- Existing fixtures are labeled sanitized in comments but do not have
  machine-readable sanitization status.
- There is no explicit expected-output update command or bless mode, which is
  good for safety but means future updates need a deliberate workflow.
- Current branch has `tools/check_protected_surfaces.py`; a content-oriented
  secret/private-marker scanner may not be available here.

## Validation Requirements

Contract-writer validation for this docs-only pass:

```bash
git diff --check
```

Future focused implementation validation:

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
```

Future review validation should add broader tests if implementation touches
shared parser state, transforms, runtime surfaces, fixture data, expected
manifests, or schema-adjacent outputs:

```bash
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
```

If a secret/private-marker scanner exists in the active branch, Codex C/E/F
should run it against committed fixture and manifest paths before submitter
work.

## Acceptance Criteria

- `docs/contracts/parser_golden_replay_harness.md` exists.
- The contract names issue #48, tracker #47, related issue #11, previous issue
  #49, PR #110, and the parser reliability branch.
- The contract marks risk tier High.
- The contract names parser reliability test harness as the owning layer.
- The contract preserves parser/state truth ownership.
- The contract defines fixture acceptance and sanitization rules.
- The contract defines expected manifest shape.
- The contract defines report shape and status semantics for `pass`, `fail`,
  `diff`, `review`, and `degraded`.
- The contract defines relationship to parser diagnostics mode.
- The contract defines relationship to saved event replay.
- The contract defines fixture minimization and expected-output update policy.
- The contract names validation commands for future implementation and review
  roles.
- The contract names protected surfaces and stop conditions.
- The contract does not implement code, create fixtures, update expected
  output, target `main`, close tracker #47, or close related issue #11.

## Next Workflow Action

Next role: Codex C, Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #48 and docs/contracts/parser_golden_replay_harness.md.

  Goal:
  Implement the smallest coherent deterministic local golden replay harness needed to satisfy the contract. The harness must replay committed sanitized Player.log fixture slices through the normal parser path and compare parser-owned observed outputs against explicit expected manifests. It must not become a second parser or truth source.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/48
    - Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/49
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/110
    - Previous merge commit: a61ed4e5cd8898e25913796080a9c46e66fcff8a
    - Branch/base: codex/parser-reliability-intelligence

  Use:
    - AGENTS.md
    - docs/agent_constitution.md
    - docs/agent_rules.yml
    - docs/codex_module_workflow.md
    - docs/agent_threads/implementation.md
    - docs/contracts/parser_golden_replay_harness.md
    - docs/contracts/parser_diagnostics_mode.md
    - docs/contracts/parser_saved_event_replay.md
    - docs/contracts/code_hardening_golden_fixture_policy.md
    - docs/contracts/player_log_evidence_ledger.md
    - src/mythic_edge_parser/app/parser_diagnostics.py
    - src/mythic_edge_parser/app/saved_event_replay.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/transforms.py
    - src/mythic_edge_parser/log/entry.py
    - src/mythic_edge_parser/router.py
    - tests/test_parser_diagnostics_mode.py
    - tests/test_saved_event_replay.py
    - tests/test_parser_regressions.py
    - tests/fixtures/parser_regression_match_slice.log
    - tests/fixtures/parser_regression_match_expected.json
    - tests/fixtures/parser_regression_bo3_slice.log
    - tests/fixtures/parser_regression_bo3_expected.json

  Do:
    - Compare current parser regression replay behavior against the contract before editing.
    - Add a small local golden replay module and focused tests.
    - Reuse the normal LineBuffer, Router, parser modules, transforms, diagnostics evidence, and parser state path.
    - Prefer reduced parser-owned expected manifests over broad whole-object snapshots.
    - Include fixture privacy/sanitization metadata checks.
    - Keep generated replay reports local-only unless the report is an intentional committed expected manifest.
    - Produce docs/implementation_handoffs/parser_golden_replay_harness_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

  Do not:
    - Target main directly.
    - Close tracker #47 or related issue #11.
    - Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, output transport, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
    - Reconstruct missing GameState data or infer match/game/card facts from incomplete evidence.
    - Copy Manasight source code.
    - Commit raw private Player.log excerpts.
    - Add automatic expected-output bless/update behavior.
    - Make golden replay a merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/49"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/110"
  previous_merge_commit: "a61ed4e5cd8898e25913796080a9c46e66fcff8a"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_golden_replay_harness.md"
  target_artifact: "docs/implementation_handoffs/parser_golden_replay_harness_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, output transport, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not reconstruct missing GameState data or infer match/game/card facts from incomplete evidence."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
    - "Do not add automatic expected-output bless/update behavior."
    - "Do not make golden replay a merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source."
```
