# Contract Test Report: Player.log Evidence Ledger Tier 3 Opening-Hand

## Findings

### Resolved: opening-hand entry display names did not match the contract

- Contract evidence: `docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md` lines 215-225 require the nine `tier3.opening_hand.*` entries to use display names `Opening Hand Size`, `Opening Hand`, and `Mulliganed Away`.
- Review-time implementation evidence: `src/mythic_edge_parser/app/evidence_ledger.py` set the display names to game-prefixed labels: `G1 Opening Hand Size`, `G2 Opening Hand Size`, `G3 Opening Hand Size`, `G1 Opening Hand`, `G2 Opening Hand`, `G3 Opening Hand`, `G1 Mulliganed Away`, `G2 Mulliganed Away`, and `G3 Mulliganed Away`.
- Review-time test evidence: `tests/test_evidence_ledger.py` asserted the game-prefixed display labels, so focused tests passed while preserving the contract mismatch.
- Codex D fix: all nine opening-hand entries now expose the exact contracted display names, and focused tests assert those row-facing aliases.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/143

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md`

## Implementation Under Test

Branch: `codex/player-log-evidence-ledger-tier3-opening-hand`

Base branch: `codex/parser-reliability-intelligence`

Prior merged dependency:

- PR #142 / merge commit `33a8bc2cba188389fe885b2446da51ac48c8555e`
- Local branch `HEAD` is `33a8bc2` before the uncommitted #143 package changes.

Changed files reviewed:

- `docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md`
- `docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`

Contract-test artifact added:

- `docs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md`

## Contract Summary

Issue #143 expands the Player.log evidence ledger with Tier 3 opening-hand
ownership provenance metadata only. The package must preserve prior #134,
#139, and #140 entries, seed nine opening-hand fields, distinguish observed
exact-hand size from derived mulligan fallback size, document local private-hand
ownership and card-resolution dependencies, document mulliganed-away discarded
and bottomed-card evidence, keep evidence path-only, and avoid parser/runtime/
workbook/webhook/App Script/output behavior changes.

## Checks Run

```bash
git fetch --prune
git status --short --branch
git merge-base --is-ancestor 33a8bc2cba188389fe885b2446da51ac48c8555e HEAD
gh issue view 143 --json number,title,state,url,body
PYTHONPATH=src python3 - <<'PY'
from mythic_edge_parser.app import evidence_ledger
ids = [
    'tier3.opening_hand.game1_opening_hand_size',
    'tier3.opening_hand.game2_opening_hand_size',
    'tier3.opening_hand.game3_opening_hand_size',
    'tier3.opening_hand.game1_opening_hand',
    'tier3.opening_hand.game2_opening_hand',
    'tier3.opening_hand.game3_opening_hand',
    'tier3.opening_hand.game1_mulliganed_away',
    'tier3.opening_hand.game2_mulliganed_away',
    'tier3.opening_hand.game3_mulliganed_away',
]
entries = {entry['entry_id']: entry for entry in evidence_ledger.iter_ledger_entries()}
families = {family['output_family']: family for family in evidence_ledger.build_player_log_evidence_ledger()['output_families']}
print('tier3 seed fields:', families['game_level_facts']['seed_fields'])
print('tier3 future fields:', families['game_level_facts']['future_fields'])
for entry_id in ids:
    entry = entries[entry_id]
    print(entry_id, entry['display_name'], entry['coverage_status'], evidence_ledger.validate_ledger_entry(entry))
print('ledger errors', evidence_ledger.validate_player_log_evidence_ledger())
PY
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py
python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
printf 'docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md\nsrc/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

After creating this report, Codex E reran:

```bash
git diff --check
printf 'docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md\ndocs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md\nsrc/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

## Results

- Branch dependency check -> `33a8bc2cba188389fe885b2446da51ac48c8555e` is an ancestor of `HEAD`; local `HEAD` is `33a8bc2`.
- Issue check -> issue #143 is open.
- Ledger introspection before Codex D -> all nine `tier3.opening_hand.*` entries validated cleanly, but display names were game-prefixed and did not match the contract table.
- `validate_player_log_evidence_ledger()` -> `[]`
- `python3 -m pytest -q tests/test_evidence_ledger.py` -> 47 passed in 0.14s
- `python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py` -> 107 passed in 0.13s
- `python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py` -> 35 passed in 0.10s
- `python3 -m pytest -q tests/test_golden_replay_harness.py` -> 13 passed in 0.15s
- `python3 -m pytest -q` -> 906 passed in 1.24s
- `python3 -m ruff check src tests tools` -> All checks passed
- `git diff --check` -> passed before and after this report was created
- Broad `origin/main` protected-surface check -> passed, forbidden 0, warnings 12
- Path-scoped protected-surface check before this report -> passed, 4 changed paths, forbidden 0, warnings 0
- Path-scoped protected-surface check after this report -> passed, 5 changed paths, forbidden 0, warnings 0
- Codex D rerun after the display-name fix:
  - `python3 -m pytest -q tests/test_evidence_ledger.py` -> 47 passed in 0.22s
  - `python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py` -> 107 passed in 0.13s
  - `python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py` -> 35 passed in 0.11s
  - `python3 -m pytest -q tests/test_golden_replay_harness.py` -> 13 passed in 0.15s
  - `python3 -m pytest -q` -> 906 passed in 1.22s
  - `python3 -m ruff check src tests tools` -> All checks passed
  - `git diff --check` -> passed
  - path-scoped protected-surface check -> passed, 5 changed paths, forbidden 0, warnings 0
- Codex E re-review after the display-name fix:
  - ledger introspection -> all nine `tier3.opening_hand.*` display names match the contract and entries validate cleanly
  - `python3 -m pytest -q tests/test_evidence_ledger.py` -> 47 passed in 0.19s
  - `python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py` -> 107 passed in 0.13s
  - `python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py` -> 35 passed in 0.10s
  - `python3 -m pytest -q tests/test_golden_replay_harness.py` -> 13 passed in 0.15s
  - `python3 -m pytest -q` -> 906 passed in 1.22s
  - `python3 -m ruff check src tests tools` -> All checks passed
  - `git diff --check` -> passed
  - path-scoped protected-surface check -> passed, 5 changed paths, forbidden 0, warnings 0
  - broad `origin/main` protected-surface check -> passed, forbidden 0, warnings 12 outside issue #143 file set

## Confirmed Contract Matches

- The branch contains PR #142 / merge commit `33a8bc2cba188389fe885b2446da51ac48c8555e` before the local #143 changes.
- `game_level_facts.seed_fields` includes all nine contracted opening-hand fields.
- `game_level_facts.future_fields` no longer lists broad `opening_hand`.
- Remaining deferred Tier 3 fields still include `turn_count`, `game_timing`, `game_duration`, `pre_postboard`, `sideboarding`, and `deck_state`.
- All nine `tier3.opening_hand.*` entries exist and validate.
- Opening-hand size entries distinguish exact observed local private-hand length from derived #140 mulligan fallback.
- Exact opening-hand entries cite local private-hand zone evidence, local hand instance-id evidence, instance-to-GRP lookup, card-name resolution, hand snapshot history, #137 local-seat/participant dependencies, and #140 mulligan dependency for expected-size checks.
- Mulliganed-away entries cite latest/discarded hand snapshot evidence, hand snapshot history, bottomed-card difference evidence, match-summary model surface evidence, #140 mulligan-flow dependency, and exact opening-hand dependency.
- Mulliganed-away metadata says those cards are not evidence for mulligan count and must not rewrite #140 entries.
- Placeholder-containing lists, unplayed-slot blanks, malformed owner-seat evidence, missing private-hand evidence, missing GRP mapping, and unresolved card names are documented as degraded or expected blank behavior.
- New evidence signals use `path_only_no_values` privacy class.
- #134 game-result, #139 play/draw, and #140 mulligan entries remain present and valid.
- No parser behavior, local private-hand extraction behavior, opening-hand selection behavior, mulliganed-away capture behavior, card-name resolution behavior, GRP catalog behavior, generated card data, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth changes were found in the issue #143 package.

## Contract Mismatches

- Resolved mismatch: the nine `display_name` values for `tier3.opening_hand.*` entries now use the contracted row-facing aliases without game prefixes.

## Missing Tests

- Resolved: focused tests now assert the contracted row-facing display names.

## Drift Notes

- Drift classification: resolved metadata contract drift with matching test coverage.
- Broad `origin/main` protected-surface validation reports 12 existing branch-scope warnings for protected parser files outside the issue #143 file set. The path-scoped protected-surface check for the issue #143 package plus this report passes with forbidden 0 and warnings 0.
- This review did not find workbook schema drift, webhook payload drift, Apps Script drift, parser behavior drift, parser state final reconciliation drift, runtime output drift, issue lifecycle drift, PR lifecycle drift, or tracker drift.

## Changed and Untracked File Awareness

Current reviewed file set after Codex D fixed the blocker:

- `docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md`
- `docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md`
- `docs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`

Codex F should stage only this reviewed package unless the user explicitly expands scope.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #143, Tier 3 opening-hand provenance under tracker #11.

Context:
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/142
- Previous merge commit: 33a8bc2cba188389fe885b2446da51ac48c8555e
- Branch: codex/player-log-evidence-ledger-tier3-opening-hand
- Base branch: codex/parser-reliability-intelligence
- Reviewed report: docs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md

Goal:
Submit the reviewed Tier 3 opening-hand provenance package as a draft PR to codex/parser-reliability-intelligence.

Scope:
- Stage only the reviewed files:
  - docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
  - docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md
  - docs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md
  - src/mythic_edge_parser/app/evidence_ledger.py
  - tests/test_evidence_ledger.py
- Commit and push codex/player-log-evidence-ledger-tier3-opening-hand.
- Open a draft PR targeting codex/parser-reliability-intelligence, or update the draft PR if one already exists.
- Use Refs #143 and tracker reference #11. Do not use Closes #11.

Validation:
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py
python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
printf 'docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md\ndocs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md\nsrc/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin

Do not change parser behavior, local private-hand extraction behavior, opening-hand selection behavior, mulliganed-away capture behavior, card-name resolution, GRP catalog behavior, generated card data, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth.
Do not rework, remove, or weaken #134, #139, or #140 provenance.
Do not map turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior.
Do not commit raw private Player.log excerpts, raw hand payloads, local diagnostics artifacts, generated card data, or workbook exports.
Do not merge, mark the PR ready, close issue #11, close issue #143, or mark tracker #11 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/143"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/142"
  previous_merge_commit: "33a8bc2cba188389fe885b2446da51ac48c8555e"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md"
  target_artifact: "Draft PR targeting codex/parser-reliability-intelligence"
  verdict: "no_blocking_findings_ready_for_submitter"
  risk_tier: "High"
  branch: "codex/player-log-evidence-ledger-tier3-opening-hand"
  base_branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py -> 47 passed in 0.22s"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py -> 107 passed in 0.13s"
    - "python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py -> 35 passed in 0.11s"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 13 passed in 0.15s"
    - "python3 -m pytest -q -> 906 passed in 1.22s"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check after report -> passed, 5 changed paths, forbidden 0, warnings 0"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed, forbidden 0, warnings 12 outside issue #143 file set"
    - "Codex E re-review ledger introspection -> all nine display names match contract and entries validate cleanly"
    - "Codex E re-review python3 -m pytest -q tests/test_evidence_ledger.py -> 47 passed in 0.19s"
    - "Codex E re-review python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py -> 107 passed in 0.13s"
    - "Codex E re-review python3 -m pytest -q tests/test_app_extractors.py tests/test_grp_id_catalog.py -> 35 passed in 0.10s"
    - "Codex E re-review python3 -m pytest -q tests/test_golden_replay_harness.py -> 13 passed in 0.15s"
    - "Codex E re-review python3 -m pytest -q -> 906 passed in 1.22s"
    - "Codex E re-review python3 -m ruff check src tests tools -> All checks passed"
    - "Codex E re-review git diff --check -> passed"
    - "Codex E re-review path-scoped protected-surface check -> passed, 5 changed paths, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #143."
    - "Do not change parser behavior, local private-hand extraction behavior, opening-hand selection behavior, mulliganed-away capture behavior, card-name resolution, GRP catalog behavior, generated card data, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not rework, remove, or weaken #134, #139, or #140 provenance."
    - "Do not map turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior."
    - "Do not reconstruct missing GameState data, infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move parser truth into AI/analytics truth."
    - "Do not commit raw private Player.log excerpts, raw hand payloads, local diagnostics artifacts, generated card data, or workbook exports."
    - "Codex F may stage only reviewed files, commit, push, and open or update a draft PR; do not merge, mark ready, close issues, or mark tracker #11 complete."
```
