# Player.log Evidence Ledger Tier 5 Card Identity Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/163

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

docs/contracts/player_log_evidence_ledger_tier5_card_identity.md

## Implementation Under Test

Branch: codex/player-log-evidence-ledger-tier5-card-identity

Changed files reviewed:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md

## Contract Summary

Issue #163 seeds exactly one Tier 5 evidence-ledger field, `grp_id`, under
`card_identity_and_gameplay_actions`. The package must document direct and
fallback card identity evidence without promoting card names, catalog lookup,
deck identity, gameplay-action provenance, opponent-card-observation provenance,
analytics, model-provider output, or AI output into parser truth.

## Checks Run

```bash
git status --short --branch
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py
python3 -m ruff check src tests tools
git diff --check
printf 'src/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\ndocs/contracts/player_log_evidence_ledger_tier5_card_identity.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md\ndocs/contract_test_reports/player_log_evidence_ledger_tier5_card_identity.md\n' | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
python3 -m pytest -q
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
```

## Results

No blocking findings remain after the Codex D Module Fixer follow-up.

The prior blocker is resolved: `opponent_card_observation.grp_id` metadata now
documents observed/high and derived/medium source-confidence paths instead of
collapsing opponent-card observation evidence to fixed `derived`/`medium`.
Focused regression coverage now fails if the metadata loses the opponent
observation `value_source`, `confidence`, visibility, or degradation context.

## Confirmed Contract Matches

- Tier 5 `card_identity_and_gameplay_actions` is now `seeded_sample`.
- Tier 5 `seed_fields` is exactly `["grp_id"]`.
- Tier 5 `future_fields` keeps `gameplay_action` and
  `opponent_card_observation`.
- No separate Tier 5 seed fields were added for observed/fallback ID facets,
  card names, display labels, catalog resolution, deck identity, collection
  ownership, gameplay action, opponent-card observation, analytics, model
  provider output, or AI.
- `tier5.card_identity.grp_id` exists and validates under the existing ledger
  schema.
- The `grp_id` entry uses parser owner
  `src/mythic_edge_parser/app/gameplay_actions.py`.
- Direct evidence documents GameState object `grpId`, direct canonical
  gameplay-action `grp_id`, and opponent-card-observation `grp_id` context.
- Opponent-card-observation `grp_id` evidence preserves observed/high and
  derived/medium source-confidence paths using opponent-observation
  `value_source`, `confidence`, visibility, and degradation context.
- Fallback evidence documents object-source ID, overlay ID, parent-chain ID,
  prior-instance ID, replacement-chain ID, submitted `grpId` lists,
  opening-hand resolution path context, GRP catalog enrichment, active deck
  display context, and GRP candidate review context.
- Catalog, active deck, local decklist, card-name, display-label, layout,
  card-face, and candidate information remains enrichment/review context and
  not parser truth.
- Tier 3 opening-hand, Tier 4 submitted-deck card-content, and Tier 4
  deck-state boundary tests remain intact.
- No workbook schema, webhook payload shape, Apps Script behavior, parser state
  final reconciliation, parser event class, router, match/game identity,
  deduplication, raw log, generated data, runtime status file, failed post,
  workbook export, OpenAI/model-provider, production behavior, or AI/analytics
  truth changes were found.

## Contract Mismatches

- None remaining.

## Missing Tests

- None blocking. Codex D added focused coverage for
  `opponent_card_observation.grp_id` source/confidence mirroring.

## Drift Notes

- No workbook schema drift found.
- No webhook payload drift found.
- No Apps Script drift found.
- No parser behavior, parser state final reconciliation, parser event class,
  match/game identity, deduplication, output transport, runtime artifact, raw
  log, generated data, failed post, workbook export, or AI/analytics truth
  drift found.
- The changed-path check against `src tools main.py
  live_print_filtered_v11_match_summary.py` reports only
  `src/mythic_edge_parser/app/evidence_ledger.py`, which is within this
  metadata package's owned implementation scope.

## Validation Results

- `python3 -m pytest -q tests/test_evidence_ledger.py`: passed, 77 passed.
- `python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py`: passed, 47 passed.
- `python3 -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- Protected-surface check with changed paths against
  `origin/codex/parser-reliability-intelligence`: passed, `forbidden: 0`,
  `warnings: 0`.
- `python3 -m pytest -q`: passed, 936 passed.

## Recommendation

approve

## Next Workflow Action

Next role: Codex F / Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/163"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_tier5_card_identity.md"
  target_artifact: "Draft PR for Tier 5 card identity provenance metadata"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier5-card-identity"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py - passed, 77 passed"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py - passed, 47 passed"
    - "python3 -m ruff check src tests tools - passed"
    - "git diff --check - passed"
    - "changed-path protected-surface check against origin/codex/parser-reliability-intelligence - passed, forbidden 0, warnings 0"
    - "python3 -m pytest -q - passed, 936 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #163."
    - "Do not change parser behavior, card identity parsing behavior, GRP normalization behavior, gameplay action behavior, opponent-card observation behavior, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth."
```
