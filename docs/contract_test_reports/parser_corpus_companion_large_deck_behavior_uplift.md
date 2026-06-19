# Parser Corpus Companion / Large-Deck Behavior Uplift Report

## Verdict

`gameplay_stress.companion_or_large_deck` has one reduced synthetic
parser-behavior uplift ready for Codex E review.

The evidence is narrow. It proves that existing parser outputs preserve a
companion-shaped StartHook deck payload field and a large-deck-like
SubmitDeckResp list shape. It does not claim companion presence, companion
legality, companion castability, large-deck legality, complete decklist truth,
deck identity truth, private smoke success, readiness, analytics truth, AI
truth, coaching truth, tracker completion, or #388/#381 activation.

## Evidence Added

- Collection parser evidence:
  `test_collection_parse_preserves_synthetic_companion_shaped_deck_field`
- Client-action parser evidence:
  `test_client_actions_submit_deck_preserves_synthetic_large_deck_list_shape`
- Scanner-safe client-action test markers:
  explicit synthetic test-marker constants preserve the existing test inputs
  without committing private log material.
- Corpus manifest entry:
  `companion_large_deck_synthetic_deck_shape_v1`
- Session-ledger entry:
  `companion_large_deck_synthetic_deck_shape_v1`

The #408 entry `companion_large_deck_boundary_report_v1` remains present and
report-only.

## Parser-Owned Evidence

The focused parser tests verify:

- emitted `DeckCollection` event;
- preserved synthetic `Companions` field in the correlated deck payload;
- preserved StartHook `raw_start_hook`;
- emitted `ClientAction` event with payload type `submit_deck_resp`;
- preserved synthetic `deck_cards` list length 80;
- preserved synthetic `sideboard_cards`;
- preserved request context and raw client action payload.

The corpus metadata records event families only as existing parser event kinds:

- `DeckCollection`
- `ClientAction`

## Corpus Status Effect

Before issue #494:

```yaml
gameplay_stress.companion_or_large_deck:
  coverage_status: "covered_report_only"
  coverage_basis:
    - "fixture_metadata_only"
  mythic_edge_entries:
    - "companion_large_deck_boundary_report_v1"
```

After issue #494:

```yaml
gameplay_stress.companion_or_large_deck:
  coverage_status: "covered_synthetic"
  coverage_basis:
    - "fixture_metadata_only"
    - "parser_behavior_verified"
  mythic_edge_entries:
    - "companion_large_deck_boundary_report_v1"
    - "companion_large_deck_synthetic_deck_shape_v1"
```

Current overall corpus summary:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 17
covered_report_only: 16
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
```

## Privacy And Protected Boundaries

- No private Player.log, UTC_Log, live MTGA, private deck, private smoke,
  Manasight raw log, external corpus input, generated data, SQLite artifact,
  runtime artifact, workbook export, secret, credential, token, API key, or
  webhook URL was used.
- No parser behavior, parser event classes, parser state final reconciliation,
  router semantics, match/game identity, diagnostics, drift, golden replay,
  feature-equity, evidence-ledger, workbook schema, webhook payload shape, Apps
  Script behavior, Google Sheets sync, output transport, analytics truth,
  AI/model-provider behavior, coaching behavior, CI gates, merge readiness,
  deploy readiness, production behavior, or final integration policy changed.
- The #408 report-only row was preserved.

## Non-Claims

This report does not claim:

- companion presence;
- companion legality;
- companion castability;
- in-game companion availability;
- large-deck legality;
- complete decklist truth;
- exact deck identity;
- deck ownership;
- sideboard choice truth;
- hidden-card truth;
- archetype classification;
- gameplay advice;
- analytics truth;
- AI truth;
- coaching truth;
- private smoke success;
- release readiness;
- production behavior;
- full corpus parity;
- tracker completion;
- #388 or #381 activation.

## Validation

- `PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py`
  passed: 65 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_corpus_parity_report.py`
  passed: 72 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=17, report_only=16, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- Path-scoped secret/private-marker scan completed with exit code 0,
  forbidden 0, warnings 3. Warnings were explicit synthetic test-marker
  constants in `tests/test_client_actions_parser.py`.
- Path-scoped protected-surface scan passed: forbidden 0, warnings 0.
- ASCII scan over changed files passed.
- Trailing-whitespace scan over changed files passed.
- Generated SQLite/local DB artifact scan returned no files.

## Residual Risks

- The new evidence is synthetic and proves only reduced deck-shape preservation
  in focused parser tests.
- It does not prove real companion behavior, large-deck legality, complete
  decklists, exact deck identity, hidden-card truth, private MTGA behavior,
  analytics truth, AI truth, coaching truth, release readiness, production
  behavior, or full corpus parity.
- Overall corpus readiness remains blocked by report-only, private-evidence,
  and external-boundary rows.

## Codex E Contract-Test Review

### Findings

No blocking findings.

No non-blocking contract mismatches were found.

### Contract-Test Verdict

Pass. The implementation satisfies the #494 contract.

`gameplay_stress.companion_or_large_deck` moves from `covered_report_only` to
`covered_synthetic` only through the two contracted synthetic evidence legs:

- `DeckCollection` preserves an obviously synthetic `Companions` field from a
  correlated StartHook deck payload.
- `ClientAction` / `submit_deck_resp` preserves and normalizes an obviously
  synthetic 80-card submitted `deck_cards` list.

The #408 `companion_large_deck_boundary_report_v1` entry remains present as
report-only non-claim metadata. The new
`companion_large_deck_synthetic_deck_shape_v1` entry is additive and limits its
claim to reduced deck-shape preservation.

The implementation does not change parser source, parser behavior, parser event
classes, parser state final reconciliation, router semantics, match/game
identity, workbook schema, webhook payload shape, Apps Script behavior,
analytics truth, AI truth, coaching truth, release readiness, production
behavior, #388/#381 activation, tracker completion, or full corpus parity.

### Contract Matches

- Both reduced synthetic parser evidence legs are present and tested.
- The manifest row uses `covered_synthetic` with `fixture_metadata_only` and
  `parser_behavior_verified`.
- The new synthetic entry uses existing parser event families only:
  `DeckCollection` and `ClientAction`.
- The session ledger records zero companion legality, companion castability,
  large-deck legality, decklist completion, and deck identity claims.
- Corpus parity metrics move exactly one family from report-only to synthetic:
  `covered_synthetic: 17`, `covered_report_only: 16`.
- `parser_behavior_ready` remains `false`.
- `pipeline_activation_ready_for_issue_388` remains `false`.
- Companion presence, companion legality, companion castability, large-deck
  legality, complete decklists, deck identity, hidden-card truth, archetype
  classification, gameplay advice, analytics truth, AI truth, coaching truth,
  release readiness, production behavior, tracker completion, and full corpus
  parity remain explicit non-claims.

### Contract Mismatches

None found.

The contract recommended the manifest `entry_type` value
`focused_parser_tests`, but used "prefer" language. The implementation uses the
existing validator-supported `session_ledger_entry` value and documents the
reason in the implementation handoff. Codex E accepts this as compatible with
the current manifest schema, not a blocker.

### Missing Tests

None blocking. Focused tests cover the collection-parser companion-shaped field
preservation, client-action large-list preservation, manifest/session-ledger
metadata, corpus summary counts, readiness counts, matrix row, and non-claims.

### Validation Rerun

Codex E reran:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_corpus_parity_report.py
```

- passed: 72 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json --out /tmp/mythic_edge_issue_494_corpus_report.json
```

- passed: `partial_coverage_map_ready`
- summary: `45 families; committed=6, synthetic=17, report_only=16, blocked=6 [private=2, external=4], missing=0`
- `parser_behavior_ready: false`
- `pipeline_activation_ready_for_issue_388: false`

```bash
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

- passed: agent docs errors 0, warnings 0; Ruff all checks passed; diff check
  no output

```bash
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md tests/test_collection_parser.py tests/test_client_actions_parser.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

- completed with exit code 0
- forbidden: 0
- warnings: 3
- warning details: three explicit synthetic client-action marker constants in
  `tests/test_client_actions_parser.py`
- Codex E classification: non-blocking warning-only synthetic test markers;
  no secret or private artifact was committed

```bash
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md tests/test_collection_parser.py tests/test_client_actions_parser.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

- passed: forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md tests/test_collection_parser.py tests/test_client_actions_parser.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

- passed: `selection_status: ok`

Additional Codex E checks:

- ASCII scan over changed files: passed
- trailing-whitespace scan over changed files: passed
- generated SQLite/local DB artifact scan: no files found

### Drift Classification

- repo drift: none found
- workbook drift: none found
- deployment drift: none found
- local-data drift: none found
- issue/tracker drift: none found
- protected-surface drift: none found

### Recommendation

Approve for Codex F module submission.

### Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/494"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/492"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/493"
  previous_merge_commit: "8d1e48c9c6bd0a20926829c2d7de1d516a24ac20"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/408"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md"
  implementation_handoff: "docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md"
  verdict: "ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-companion-large-deck-behavior-uplift-494"
  base_branch: "main"
  selected_family: "gameplay_stress.companion_or_large_deck"
  prior_status: "covered_report_only"
  current_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json --out /tmp/mythic_edge_issue_494_corpus_report.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan completed with forbidden 0, warnings 3"
    - "path-scoped protected-surface gate passed"
    - "path-scoped validation selector passed"
    - "ASCII, trailing-whitespace, and generated SQLite/local DB artifact scans passed"
  stop_conditions:
    - "Do not target main directly unless explicitly approved."
    - "Do not close tracker #158, pipeline tracker #388, parent issue #434, or issue #494."
    - "Do not activate #388 or #381."
    - "Do not claim companion presence, companion legality, companion castability, large-deck legality, complete decklist truth, deck identity truth, readiness, analytics truth, AI truth, coaching truth, full corpus parity, or tracker completion."
```
