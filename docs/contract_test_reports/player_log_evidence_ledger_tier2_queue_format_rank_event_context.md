# Player.log Evidence Ledger Tier 2 Queue / Format / Rank / Event-Context Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/167

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md

## Implementation Under Test

Branch: codex/player-log-evidence-ledger-tier2-context

Changed files reviewed:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md

## Contract Summary

Issue #167 seeds exactly four Tier 2 evidence-ledger fields under
`queue_format_rank_event_context`: `event_id`, `super_format`,
`constructed_rank`, and `queue_type`. The package must document direct,
fallback, derived, carried-forward, unknown, and degraded provenance for
queue/format/rank/event context without changing parser behavior or promoting
workbook labels, EventIdentity facets, runtime filters, analytics, Match
Journal, overlays, SQLite, Google Sheets sync, model-provider output, or AI
into truth owners.

## Checks Run

```bash
git status --short --branch
gh issue view 167 --repo Tahjali11/Mythic-Edge --json number,title,state,body,labels,assignees,url
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_event_identity.py
python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py
python3 -m pytest -q tests/test_runtime_surfaces.py
python3 -m ruff check src tests tools
git diff --check
printf 'src/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\ndocs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md\n' | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
python3 -m pytest -q
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
```

## Results

No blocking findings. The implementation matches the Tier 2
queue/format/rank/event-context provenance contract and remains metadata/test
only.

## Confirmed Contract Matches

- Tier 2 `queue_format_rank_event_context` is now `seeded_sample`.
- Tier 2 `seed_fields` is exactly
  `["event_id", "super_format", "constructed_rank", "queue_type"]`.
- Tier 2 `future_fields` is exactly `[]`.
- No separate Tier 2 seed fields were added for workbook-facing labels,
  `match_win_condition`, rank buckets, constructed/limited rank facets,
  EventIdentity fields, runtime filters, analytics segments, archetypes,
  Match Journal, overlays, SQLite, Google Sheets sync, model-provider output,
  or AI.
- The four required entries exist and validate:
  - `tier2.queue_format_rank_event_context.event_id`
  - `tier2.queue_format_rank_event_context.super_format`
  - `tier2.queue_format_rank_event_context.constructed_rank`
  - `tier2.queue_format_rank_event_context.queue_type`
- `event_id` distinguishes game-room config evidence from player-level fallback
  and parser-state precedence context.
- `super_format` distinguishes raw GameState `superFormat` evidence from
  row-facing `MTGA Format` fallback labels.
- `constructed_rank` distinguishes direct Rank payload evidence from
  `carried_forward_pre_match` rank snapshots and row-facing `My Rank` bucket
  facets.
- `queue_type` documents `MTGA Queue Type` as a parser-derived row label with
  observed `matchWinCondition` dependency and weaker event-id,
  sideboarding/total-games, and raw-condition fallback paths.
- EventIdentity classifier outputs remain derived facets and are not separate
  seed fields.
- Runtime history filters remain downstream consumers and do not own
  queue/format/rank/event truth.
- Prior Tier 1, Tier 3, Tier 4, and Tier 5 seed fields and entries remain
  present.
- Path-only privacy is preserved; no raw Player.log excerpts or raw payload
  values were added.
- No workbook schema, webhook payload shape, Apps Script behavior, parser
  behavior, event identity classifier behavior, rank parsing behavior,
  match-state parsing behavior, parser state final reconciliation, parser event
  class, ActionLogRow shape, match/game identity, deduplication, output
  transport, runtime artifact, Match Journal, overlay, SQLite, Google Sheets
  sync, analytics truth, AI truth, model-provider behavior, raw log, generated
  data, failed post, runtime status file, or workbook export changes were
  found.

## Contract Mismatches

- None.

## Missing Tests

- None blocking. Focused tests now pin the Tier 2 family seed scope, exact
  entry IDs, direct/fallback paths, value-source/confidence/finality policies,
  degradation language, downstream non-truth boundaries, built-in ledger
  validation, and prior Tier 1/Tier 3/Tier 4/Tier 5 preservation.

## Drift Notes

- No workbook schema drift found.
- No webhook payload drift found.
- No Apps Script drift found.
- No parser behavior, event identity classifier, rank parser, match-state
  parser, parser state final reconciliation, parser event class, ActionLogRow,
  match/game identity, deduplication, output transport, runtime artifact, Match
  Journal, overlay, SQLite, Google Sheets sync, analytics, AI, model-provider,
  raw log, generated data, failed post, runtime status file, or workbook export
  drift found.
- The changed-path check against `src tools main.py
  live_print_filtered_v11_match_summary.py` reports only
  `src/mythic_edge_parser/app/evidence_ledger.py`, which is within this
  metadata package's owned implementation scope.

## Validation Results

- `python3 -m pytest -q tests/test_evidence_ledger.py`: passed, 89 passed.
- `python3 -m pytest -q tests/test_event_identity.py`: passed, 36 passed.
- `python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py`: passed, 47 passed.
- `python3 -m pytest -q tests/test_runtime_surfaces.py`: passed, 7 passed.
- `python3 -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- Protected-surface check with changed paths against
  `origin/codex/parser-reliability-intelligence`: passed, `forbidden: 0`,
  `warnings: 0`.
- `python3 -m pytest -q`: passed, 948 passed.

## Recommendation

approve

## Next Workflow Action

Next role: Codex F / Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/167"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md"
  target_artifact: "Draft PR for Tier 2 queue/format/rank/event-context provenance metadata"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "Medium-High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier2-context"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py - passed, 89 passed"
    - "python3 -m pytest -q tests/test_event_identity.py - passed, 36 passed"
    - "python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py - passed, 47 passed"
    - "python3 -m pytest -q tests/test_runtime_surfaces.py - passed, 7 passed"
    - "python3 -m ruff check src tests tools - passed"
    - "git diff --check - passed"
    - "changed-path protected-surface check against origin/codex/parser-reliability-intelligence - passed, forbidden 0, warnings 0"
    - "python3 -m pytest -q - passed, 948 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #11 or issue #167."
    - "Do not change parser behavior, event identity classifier behavior, rank parsing behavior, match-state parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, analytics truth, AI truth, model-provider behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, or archetype classification behavior."
```
