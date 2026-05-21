# Player.log Evidence Ledger Tier 3 Turn-Count Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/145

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/player_log_evidence_ledger_tier3_turn_count.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

- Branch: `codex/player-log-evidence-ledger-tier3-turn-count`
- Base branch: `codex/parser-reliability-intelligence`
- Previous merge commit: `af6d5f554720b159975e8fecfcf008298fd8ca76`
- Changed implementation files:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `tests/test_evidence_ledger.py`
  - `docs/contracts/player_log_evidence_ledger_tier3_turn_count.md`
  - `docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md`

## Findings

No blocking findings.

## Contract Summary

Issue #145 maps Tier 3 turn-count provenance in the Player.log evidence
ledger. The package must add metadata and focused tests for
`game1_turn_count`, `game2_turn_count`, and `game3_turn_count`, define each
field as the maximum observed valid positive turn number for its game slot,
remove broad `turn_count` from Tier 3 future fields, preserve prior #134,
#139, #140, and #143 ledger entries, and avoid parser/runtime/workbook/webhook
or Apps Script behavior changes.

## Checks Run

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
printf 'docs/contracts/player_log_evidence_ledger_tier3_turn_count.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md\nsrc/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
PYTHONPATH=src python3 - <<'PY'
from mythic_edge_parser.app import evidence_ledger
ledger = evidence_ledger.build_player_log_evidence_ledger()
families = {f["output_family"]: f for f in ledger["output_families"]}
entries = {e["entry_id"]: e for e in evidence_ledger.iter_ledger_entries()}
turn_ids = [f"tier3.turn_count.game{i}_turn_count" for i in (1, 2, 3)]
print("tier3_seed_has_turn_counts:", all(f"game{i}_turn_count" in families["game_level_facts"]["seed_fields"] for i in (1, 2, 3)))
print("turn_count_future_field_present:", "turn_count" in families["game_level_facts"]["future_fields"])
for entry_id in turn_ids:
    entry = entries[entry_id]
    print(entry_id, "errors=", evidence_ledger.validate_ledger_entry(entry))
print("ledger_errors=", evidence_ledger.validate_player_log_evidence_ledger())
PY
```

## Results

- `tests/test_evidence_ledger.py`: passed, `51 passed in 0.17s`
- Adjacent parser/state/model tests: passed, `82 passed in 0.12s`
- Full pytest: passed, `910 passed in 1.26s`
- Ruff: passed, `All checks passed!`
- `git diff --check`: passed with no output
- Full protected-surface gate against `origin/main`: passed, `forbidden: 0`, `warnings: 12`
- #145 path-scoped protected-surface gate: passed, `forbidden: 0`, `warnings: 0`
- Ledger introspection: the three turn-count fields are seeded, broad
  `turn_count` is absent from future fields, all three
  `tier3.turn_count.*` entries validate cleanly, and the full ledger validates
  cleanly.

## Confirmed Contract Matches

- `game_level_facts.seed_fields` includes `game1_turn_count`,
  `game2_turn_count`, and `game3_turn_count`.
- Broad `turn_count` is removed from `game_level_facts.future_fields`, while
  `game_timing`, `game_duration`, `pre_postboard`, `sideboarding`, and
  `deck_state` remain deferred.
- `tier3.turn_count.game1_turn_count`,
  `tier3.turn_count.game2_turn_count`, and
  `tier3.turn_count.game3_turn_count` exist and validate.
- Turn-count entries document maximum observed valid positive turn number
  semantics, blank-versus-zero behavior, invalid/degraded zero or negative
  evidence, boolean/float coercion risk, malformed/non-integral evidence,
  queued fallback, conflicts, lower later observations, and truncation/data-loss
  degradation.
- Direct evidence cites GameState turn-info, identity turn number, top-level
  payload turn number, extractor output, and parser state/model output.
- Fallback evidence cites queued GameState fallback, game-slot dependency, and
  prior max-observed observation.
- Turn-count value-source policy uses observed, derived, unknown, and conflict;
  `inferred` and `legacy_enriched` are not used as turn-count truth paths.
- #134 game-result, #139 play/draw, #140 mulligan, and #143 opening-hand
  entries remain present and covered by focused tests.
- All new evidence signals are path-only and do not embed raw logs, raw
  GameState payloads, raw turn payloads, local artifacts, generated data,
  secrets, or workbook exports.
- No parser behavior, turn-count update behavior, GameState parsing,
  turn-info normalization, extractor behavior, parser state final
  reconciliation, parser event classes, workbook schema, webhook payload shape,
  Apps Script behavior, output transport, match/game identity, deduplication,
  secrets, environment variables, raw logs, generated data, runtime status
  files, failed posts, workbook exports, production behavior, or analytics
  truth changed in this slice.

## Contract Mismatches

None found.

## Missing Tests

None found for the #145 contract. Focused tests cover entry existence,
validation, direct/fallback evidence signals, max-observed semantics,
blank-versus-zero behavior, degraded input classes, no inferred or
legacy-enriched turn-count truth path, prior Tier 3 entry preservation, and
remaining deferred scope.

## Drift Notes

- Repo drift: none found in the #145 slice.
- Workbook schema drift: none found.
- Webhook payload drift: none found.
- Apps Script drift: none found.
- Parser/runtime behavior drift: none found.
- Local-data drift: none found.
- Protected-surface note: the full branch comparison to `origin/main` reports
  12 warnings from accumulated parser-reliability integration branch changes,
  but the path-scoped #145 gate reports `forbidden: 0`, `warnings: 0`.

## Recommendation

Approve for Codex F: Module Submitter.

## Remaining Non-Blocking Gaps

- Runtime field-evidence attachment remains intentionally deferred.
- Drift reports, schema snapshots, diagnostics reports, replay reports,
  feature-equity reports, timing/duration provenance, and invariant execution
  remain intentionally deferred.
- Blank turn-count output remains semantically ambiguous until a future
  runtime field-evidence pass can attach per-row evidence.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #145, Tier 3 turn-count provenance under issue #11.

Submit the reviewed metadata/test-only package from branch codex/player-log-evidence-ledger-tier3-turn-count into base branch codex/parser-reliability-intelligence.

Use:
- docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier3_turn_count.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py

Codex E found no blocking findings. Validation passed:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py
- python3 -m pytest -q
- python3 -m ruff check src tests tools
- git diff --check
- python3 tools/check_protected_surfaces.py --base origin/main
- path-scoped protected-surface gate for #145 files

Stage only the reviewed #145 files, commit, push, and open or update a draft PR to codex/parser-reliability-intelligence. Do not target main. Do not merge. Do not close issue #11 or issue #145. Do not include unrelated local files or protected artifacts.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/145"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/143"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/144"
  previous_merge_commit: "af6d5f554720b159975e8fecfcf008298fd8ca76"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md"
  target_artifact: "draft PR to codex/parser-reliability-intelligence"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-turn-count"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "path-scoped protected-surface gate for #145 files -> forbidden: 0, warnings: 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #145."
    - "Do not change parser behavior, turn-count update behavior, GameState parsing, turn-info normalization, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or analytics truth."
    - "Do not reconstruct missing turns, skipped phases, hidden actions, or facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```
