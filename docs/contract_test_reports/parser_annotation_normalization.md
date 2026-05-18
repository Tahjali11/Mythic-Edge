# Parser Annotation Normalization Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/113

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/50

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/112

Previous merge commit: `69896381a0c5d69253ef667d4575cdd0fd7e7f2a`

## Contract

- `docs/contracts/parser_annotation_normalization.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Changed files reviewed:

- `docs/contracts/parser_annotation_normalization.md`
- `docs/implementation_handoffs/parser_annotation_normalization_comparison.md`
- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `tests/test_gre_annotations_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`

Unrelated local files observed and excluded from this review:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Findings

No blocking findings.

## Contract-Test Verdict

The implementation satisfies the parser annotation normalization contract in
the reviewed scope. `normalized_annotations` is an additive parser-owned
GameState payload field, raw annotation arrays remain preserved, malformed
annotation evidence degrades/requires review instead of becoming clean parser
facts, and gameplay actions consume the shared normalizer without expanding
runtime output, workbook, webhook, Apps Script, parser state final
reconciliation, parser event class, match/game identity, or downstream truth
surfaces.

Next recommended role: Codex F: Module Submitter.

## Contract Summary

The annotation normalization module must preserve raw GRE GameState annotation
arrays while adding a stable parser-owned normalized annotation evidence view.
It may expose normalized records and summaries for parser-adjacent consumers,
but it must not reconstruct missing GameState data, infer hidden cards, solve
timer/diff/update/deletion mechanics, create new event classes, or move truth
into workbook formulas, dashboards, webhook transport, Apps Script, AI, or
analytics surfaces.

## Checks Run

```bash
git fetch --prune
gh issue view 113 --json number,title,state,body,labels,url
python3 -m pytest -q tests/test_gre_annotations_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_saved_event_replay.py
python3 -m ruff check src tests
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
printf '%s\n' src/mythic_edge_parser/parsers/gre/annotations.py src/mythic_edge_parser/parsers/gre/game_state.py src/mythic_edge_parser/app/gameplay_actions.py tests/test_gre_annotations_parser.py tests/test_gre_game_state_parser.py tests/fixtures/schema_snapshots/parser_payload_keys.json docs/contracts/parser_annotation_normalization.md docs/implementation_handoffs/parser_annotation_normalization_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
python3 -m pytest -q tests
python3 tools/check_secret_patterns.py --base origin/main
```

## Results

- Issue #113: open, tracker #47-linked, parser reliability branch scope
  confirmed.
- Annotation normalizer tests: `6 passed in 0.03s`.
- GameState parser tests: `5 passed in 0.03s`.
- Gameplay action tests: `16 passed in 0.17s`.
- Opponent-card observation tests: `10 passed in 0.03s`.
- Parser diagnostics mode tests: `10 passed in 0.06s`.
- Golden replay harness tests: `12 passed in 0.21s`.
- Parser regression tests: `2 passed in 0.10s`.
- Event schema snapshot tests: `6 passed in 0.09s`.
- Saved event replay tests: `26 passed in 0.06s`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- Protected-surface gate against `origin/main`: `changed_paths: 39`,
  `forbidden: 0`, `warnings: 4`, `result: passed`.
- Explicit #113 changed-path protected-surface gate: `changed_paths: 8`,
  `forbidden: 0`, `warnings: 3`, `result: passed`.
- Golden replay CLI over committed manifests:
  `Golden replay: pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- Full local test suite: `723 passed in 1.05s`.
- `tools/check_secret_patterns.py`: unavailable on this branch.

The four branch-scope protected-surface warnings from `origin/main` are from
previously merged parser reliability issue #107 surfaces:
`src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`, and
`src/mythic_edge_parser/parsers/truncation.py`.

The three explicit #113 warnings are contract-authorized parser-owned changes:
`src/mythic_edge_parser/parsers/gre/annotations.py`,
`src/mythic_edge_parser/parsers/gre/game_state.py`, and
`src/mythic_edge_parser/app/gameplay_actions.py`.

## Confirmed Contract Matches

- `src/mythic_edge_parser/parsers/gre/annotations.py` exposes the contracted
  constants and public helpers:
  `ANNOTATION_RECORD_OBJECT`, `ANNOTATION_COLLECTION_OBJECT`,
  `SCHEMA_VERSION`, `normalize_annotation_record()`,
  `normalize_annotation_arrays()`, `annotation_categories_for_instance()`, and
  `replacement_instance_ids()`.
- Normalized collection payloads include the contracted object, schema,
  counts, source array counts, annotation types, marker types,
  diff-deleted-persistent IDs, object replacements, zone transfers,
  degradation flags, review status, and records.
- Normalized records include the contracted source, identity, type, affected
  ID, detail, marker, replacement, zone-transfer, evidence, value-source,
  confidence, degradation, and review fields.
- Record and collection payloads are JSON-serializable and deterministic by
  source array order and source index.
- Raw `annotations`, `persistent_annotations`, and
  `diff_deleted_persistent_annotation_ids` remain present in GameState payloads
  with their existing raw-preservation semantics.
- `normalized_annotations` is additive and parser-owned on
  `GameStateEvent.payload`.
- `raw_game_state` behavior remains unchanged.
- Malformed annotation sections produce collection-level degradation flags.
- Non-dict annotation entries produce degraded placeholder records.
- Missing and malformed annotation types are flagged and do not become trusted
  marker names.
- Affected IDs and detail integer values use
  `api_common.normalize_int_list()` semantics, including skipping booleans,
  floats, negative strings, invalid strings, empty strings, nested values, and
  dictionaries.
- Detail string values require actual strings; malformed string values are
  flagged rather than becoming semantic categories.
- Boolean detail values remain boolean values and do not become integers.
- Object replacement summaries require paired `orig_id` and `new_id` evidence.
- Zone-transfer categories, source/destination zones, semantic hints, and
  affected IDs are preserved as annotation evidence, not reconstructed game
  facts.
- Marker extraction is exact and case-sensitive for the contracted marker
  types.
- `annotation_categories_for_instance()` and `replacement_instance_ids()`
  expose normalized annotation evidence only.
- `gameplay_actions.py` now consumes the shared normalizer for annotation
  type/category/replacement behavior while keeping persistent annotations out
  of gameplay-action classification.
- Existing gameplay-action, opponent-card observation, diagnostics, golden
  replay, schema snapshot, parser regression, and saved replay behavior remain
  compatible under the validation run.
- No workbook schema, webhook payload shape, Apps Script behavior, output
  transport, parser state final reconciliation, parser event class, match/game
  identity, deduplication, secrets, environment variables, raw logs, generated
  data, runtime status file, failed-post, workbook export, hidden-card,
  decklist, archetype, model-provider, timer normalization, or GameState
  diff/update/deletion mechanics changes were found in the #113 scope.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

Focused tests cover collection summaries, input immutability, persistent
annotation source records, malformed sections, placeholder records, type and
affected-ID boundaries, detail value normalization, object replacement
degradation, zone-transfer summaries, well-known markers, additive GameState
payload behavior, raw annotation preservation, malformed GameState sections,
schema snapshot keys, gameplay-action compatibility, opponent-observation
compatibility, diagnostics compatibility, golden replay compatibility, parser
regressions, and saved event replay.

Non-blocking note: broader live Arena annotation drift, persistent annotation
lifecycle semantics, timer normalization, and GameState diff/update/deletion
mechanics remain intentionally outside v1.

## Drift Notes

- Repo drift: expected addition of a parser-side GRE annotation normalizer,
  additive GameState payload field, focused tests, schema snapshot update,
  contract, handoff, and this contract-test report.
- Parser behavior drift: contract-authorized additive normalized annotation
  evidence only.
- Raw GameState payload drift: none found for raw annotation fields or
  `raw_game_state`.
- Parser event class drift: none found.
- Parser state final reconciliation drift: none found.
- Match/game identity drift: none found.
- Deduplication drift: none found.
- Workbook schema drift: none found.
- Webhook payload drift: none found.
- Apps Script drift: none found.
- Output transport drift: none found.
- Runtime status schema drift: none found.
- Failed-post schema drift: none found.
- Local-data drift: no raw private logs, generated runtime artifacts, failed
  posts, runtime status files, or workbook exports were added in the reviewed
  #113 scope.
- Previous issue #107 drift: still present in branch comparisons against
  `origin/main` and not part of this #113 finding set.

## Remaining Non-Blocking Gaps

- Remote CI has not run in this local Codex E pass.
- `tools/check_secret_patterns.py` is absent on this branch, so the optional
  branch-native content scanner was recorded as unavailable.
- Persistent annotation lifecycle, timer normalization, GameState
  diff/update/deletion mechanics, and broader Arena annotation drift remain
  future work, as the contract states.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for parser reliability issue #113.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/113

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Use:
- docs/contracts/parser_annotation_normalization.md
- docs/implementation_handoffs/parser_annotation_normalization_comparison.md
- docs/contract_test_reports/parser_annotation_normalization.md

Goal:
Stage only the reviewed annotation-normalization package, commit, push, and
open or update a draft PR against codex/parser-reliability-intelligence. Do
not target main.

Reviewed files:
- docs/contracts/parser_annotation_normalization.md
- docs/implementation_handoffs/parser_annotation_normalization_comparison.md
- docs/contract_test_reports/parser_annotation_normalization.md
- src/mythic_edge_parser/parsers/gre/annotations.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/app/gameplay_actions.py
- tests/test_gre_annotations_parser.py
- tests/test_gre_game_state_parser.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Confirm before staging:
- No raw private Player.log excerpts, secrets, webhook URLs, generated runtime
  artifacts, runtime status files, failed posts, or workbook exports are included.
- The unrelated local files docs/.DS_Store,
  docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md,
  docs/contracts/repo_wide_llm_advisory_review_scaffold.md, and
  docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md
  are not staged.
- Workbook schema, webhook payload shape, Apps Script behavior, output
  transport, parser event classes, parser state final reconciliation,
  extractor behavior, match/game identity, deduplication, runtime status
  schema, failed-post schema, workbook exports, and production deployment
  behavior are unchanged.
- No hidden-card inference, decklist completion, archetype classification,
  model-provider calls, timer normalization, or GameState diff/update/deletion
  mechanics were added.

Validation evidence to include:
- python3 -m pytest -q tests/test_gre_annotations_parser.py -> 6 passed
- python3 -m pytest -q tests/test_gre_game_state_parser.py -> 5 passed
- python3 -m pytest -q tests/test_gameplay_actions.py -> 16 passed
- python3 -m pytest -q tests/test_opponent_card_observations.py -> 10 passed
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py -> 10 passed
- python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed
- python3 -m pytest -q tests/test_parser_regressions.py -> 2 passed
- python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed
- python3 -m pytest -q tests/test_saved_event_replay.py -> 26 passed
- python3 -m ruff check src tests -> All checks passed!
- git diff --check -> passed
- python3 tools/check_protected_surfaces.py --base origin/main -> passed with only prior #107 protected-surface warnings
- explicit #113 local changed-path protected-surface stdin check -> passed with contract-authorized parser-owned warnings only
- python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass
- python3 -m pytest -q tests -> 723 passed
- tools/check_secret_patterns.py was unavailable on this branch

Do not stage unrelated files. Do not merge, close issue #113, mark tracker #47
complete, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/113"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/50"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/112"
  previous_merge_commit: "69896381a0c5d69253ef667d4575cdd0fd7e7f2a"
  completed_thread: "E"
  next_thread: "F"
  verdict: "No blocking findings. Ready for Codex F."
  branch: "codex/parser-reliability-intelligence"
  source_artifact: "docs/contracts/parser_annotation_normalization.md"
  target_artifact: "docs/contract_test_reports/parser_annotation_normalization.md"
  risk_tier: "High"
  validation:
    - "python3 -m pytest -q tests/test_gre_annotations_parser.py -> 6 passed"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py -> 5 passed"
    - "python3 -m pytest -q tests/test_gameplay_actions.py -> 16 passed"
    - "python3 -m pytest -q tests/test_opponent_card_observations.py -> 10 passed"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py -> 10 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed"
    - "python3 -m pytest -q tests/test_parser_regressions.py -> 2 passed"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed"
    - "python3 -m pytest -q tests/test_saved_event_replay.py -> 26 passed"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed with only prior #107 protected-surface warnings"
    - "explicit #113 local changed-path protected-surface stdin check -> passed with contract-authorized parser-owned warnings only"
    - "python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass"
    - "python3 -m pytest -q tests -> 723 passed"
    - "not run - tools/check_secret_patterns.py unavailable on this branch"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not infer hidden cards, complete decklists, classify archetypes, call model providers, or move parser truth downstream."
    - "Do not solve timer normalization or GameState diff/update/deletion mechanics in this module."
    - "Do not stage unrelated docs/.DS_Store, repo-wide hardening local report, or LLM advisory scaffold files."
```
