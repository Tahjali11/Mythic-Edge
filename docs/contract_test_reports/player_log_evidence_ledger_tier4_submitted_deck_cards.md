# Player.log Evidence Ledger Tier 4 Submitted-Deck Cards Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/159

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

- Branch: `codex/player-log-evidence-ledger-tier4-submitted-deck-cards`
- Base branch: `codex/parser-reliability-intelligence`
- Previous merge commit: `b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e`
- Changed implementation files:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `tests/test_evidence_ledger.py`
  - `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
  - `docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md`

## Findings

No blocking findings.

## Contract Summary

Issue #159 maps Tier 4 submitted-deck card-content provenance in the
Player.log evidence ledger. The implementation must seed exactly one new Tier
4 ledger field, `submitted_deck_cards`, preserve the #151
`sideboarding_entered` and `submit_deck_seen` signal entries, keep Tier 3
`deck_state` deferred, document submitted mainboard/sideboard `grpId` list
content as parser-observed payload evidence, keep counts and signatures as
derived facets inside the single entry, and reject deck-state, sideboard-delta,
decklist identity, card-name, collection ownership, workbook, Apps Script,
analytics, model-provider, and AI truth.

## Checks Run

```bash
git fetch --prune
git status --short --branch
gh issue view 159 --json number,title,state,url,body,labels,assignees
PYTHONPATH=src python3 - <<'PY'
from mythic_edge_parser.app import evidence_ledger
ledger = evidence_ledger.build_player_log_evidence_ledger()
families = {f["output_family"]: f for f in ledger["output_families"]}
entries = {e["entry_id"]: e for e in evidence_ledger.iter_ledger_entries()}
tier4 = families["sideboarding_and_deck_state"]
ids = (
    "tier4.sideboarding_submit_deck.sideboarding_entered",
    "tier4.sideboarding_submit_deck.submit_deck_seen",
    "tier4.submitted_deck_cards.submitted_deck_cards",
)
print("tier4_status:", tier4["status"])
print("tier4_seed_fields:", tier4["seed_fields"])
print("tier4_future_fields:", tier4["future_fields"])
print("tier3_future_fields:", families["game_level_facts"]["future_fields"])
for entry_id in ids:
    entry = entries[entry_id]
    print(entry_id, "errors=", evidence_ledger.validate_ledger_entry(entry))
    print(" owner=", entry["parser_owner"])
    print(" direct=", [s["signal_id"] for s in entry["direct_evidence"]])
    print(" fallback=", [s["signal_id"] for s in entry["fallback_evidence"]])
    print(" values=", entry["value_source_policy"])
    print(" privacy=", sorted({s["privacy_class"] for s in (*entry["direct_evidence"], *entry["fallback_evidence"])}))
print("ledger_errors=", evidence_ledger.validate_player_log_evidence_ledger())
PY
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py
python3 -m ruff check src tests tools
git diff --check
python3 -m pytest -q
python3 tools/check_protected_surfaces.py --base origin/main
printf 'docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md\nsrc/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

## Results

- Issue #159: open, title `[parser-resilience] Map Tier 4 submitted-deck card-content provenance`.
- Worktree branch: `codex/player-log-evidence-ledger-tier4-submitted-deck-cards`, tracking `origin/codex/parser-reliability-intelligence`.
- Ledger introspection: Tier 4 `sideboarding_and_deck_state` is `seeded_sample`, Tier 4 `seed_fields` are `["sideboarding_entered", "submit_deck_seen", "submitted_deck_cards"]`, Tier 4 `future_fields` are empty, Tier 3 `future_fields` are `["deck_state"]`, the two #151 entries remain present and validating, the submitted-deck entry validates cleanly, all direct/fallback evidence privacy classes are `path_only_no_values`, and the full ledger validates cleanly.
- `tests/test_evidence_ledger.py`: passed, `68 passed in 0.27s`
- Adjacent client-action/diagnostics/runtime/GRP tests: passed, `79 passed in 0.16s`
- Ruff: passed, `All checks passed!`
- `git diff --check`: passed with no output
- Full pytest: passed, `927 passed in 1.40s`
- Full protected-surface gate against `origin/main`: passed, `forbidden: 0`, `warnings: 12`
- #159 path-scoped protected-surface gate: passed, `forbidden: 0`, `warnings: 0`

## Confirmed Contract Matches

- Tier 4 `sideboarding_and_deck_state` remains `seeded_sample`.
- Tier 4 `seed_fields` include `sideboarding_entered`, `submit_deck_seen`, and `submitted_deck_cards`.
- Tier 4 `future_fields` no longer include `submitted_deck_cards`.
- Tier 3 `game_level_facts.future_fields` still includes only `deck_state`.
- Existing #151 `sideboarding_entered` and `submit_deck_seen` entries remain present and validate cleanly.
- `tier4.submitted_deck_cards.submitted_deck_cards` exists and validates.
- The submitted-deck entry uses parser owner `src/mythic_edge_parser/parsers/client_actions.py`.
- Direct evidence documents `submit_deck_resp`, `payload.deck_cards`, `payload.sideboard_cards`, request context, and event timestamp context.
- Fallback evidence documents raw preserved payload paths, active submitted-deck artifact, counts/signature, runtime active deck state, and GRP candidate snapshot as derived or downstream fallback surfaces.
- Value-source policy is direct `observed`, fallback `derived`, missing `unknown`, and contradiction `conflict`.
- Counts and submitted-deck signature are derived facets inside `submitted_deck_cards`, not separate top-level ledger fields.
- Repeated payload semantics are documented as event-scoped direct evidence plus latest-observed runtime fallback.
- Empty or malformed submitted card lists are documented as unknown or degraded card-content evidence while preserving #151 `submit_deck_seen` signal semantics.
- The entry rejects sideboard deltas, deck names, deck IDs, decklist identity, card names, collection ownership, GRP scoring, pre/postboard labels, sideboarding signals, workbook formulas, Apps Script, analytics, model-provider output, and AI truth as parser truth.
- All direct and fallback evidence signals use `path_only_no_values`.
- No parser behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, GRP candidate scoring, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth changed in this slice.

## Contract Mismatches

None found.

## Missing Tests

None found for the #159 contract. Focused tests cover Tier 4 family metadata,
submitted-deck entry existence and validation, parser owner, direct evidence,
fallback/degraded evidence, value-source/confidence/finality policy, derived
count/signature facets, repeated payload semantics, empty/malformed-list
degradation, downstream truth rejection, privacy classes, prior Tier 1/Tier 3
and #151 entry preservation, and deferred `deck_state` scope.

## Drift Notes

- Repo drift: none found in the #159 slice.
- Workbook schema drift: none found.
- Webhook payload drift: none found.
- Apps Script drift: none found.
- Parser/runtime behavior drift: none found.
- Runtime artifact drift: none found; the implementation documents existing
  runtime artifacts as downstream fallback metadata without changing write
  behavior.
- Local-data drift: none found.
- Protected-surface note: the full branch comparison to `origin/main` reports
  12 warnings from accumulated parser-reliability integration branch changes,
  but the path-scoped #159 gate reports `forbidden: 0`, `warnings: 0`.
- Worktree awareness: the implementation branch currently has unstaged
  modified files for `src/mythic_edge_parser/app/evidence_ledger.py` and
  `tests/test_evidence_ledger.py`, plus untracked contract and handoff docs.
  No files were staged or committed during review.

## Recommendation

Approve for Codex F: Module Submitter.

## Remaining Non-Blocking Gaps

- Runtime field-evidence attachment remains intentionally deferred.
- Broad deck-state, sideboard deltas, deck identity, decklist alignment, card
  names, collection ownership, archetypes, matchup plans, card-performance
  analytics, gameplay advice, player-mistake labels, model-provider behavior,
  and AI interpretation remain intentionally deferred.
- Counts and submitted-deck signature are only metadata facets in this slice;
  they are not separate ledger fields.
- Future field-evidence consumers must preserve the contract's at-least-one
  non-empty normalized list rule for card-content truth.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #159, Tier 4 submitted-deck card-content provenance under tracker #11.

Submit the reviewed metadata/test-only package from branch codex/player-log-evidence-ledger-tier4-submitted-deck-cards into base branch codex/parser-reliability-intelligence.

Use:
- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py

Codex E found no blocking findings. Validation passed:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_client_actions_parser.py tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py
- python3 -m ruff check src tests tools
- git diff --check
- python3 -m pytest -q
- python3 tools/check_protected_surfaces.py --base origin/main
- path-scoped protected-surface gate for #159 files

Stage only the reviewed #159 files, commit, push, and open or update a draft PR to codex/parser-reliability-intelligence. Do not target main. Do not merge. Do not close issue #11 or issue #159. Do not include unrelated local files, raw submitted-deck payloads, generated data, runtime artifacts, secrets, or protected artifacts.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/159"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/151"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/157"
  previous_merge_commit: "b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md"
  target_artifact: "draft PR to codex/parser-reliability-intelligence"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier4-submitted-deck-cards"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 -m pytest -q"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "path-scoped protected-surface gate for #159 files -> forbidden: 0, warnings: 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #159."
    - "Do not change parser behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, GRP candidate scoring, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not add separate top-level count/signature fields, runtime field-evidence attachment, sideboard deltas, deck names, deck IDs, decklist identity, archetype labels, matchup plans, card-performance analytics, gameplay advice, player-mistake labels, card-name truth, collection ownership truth, or model-provider behavior."
    - "Do not commit raw private Player.log excerpts, raw submitted-deck payloads, raw decklists, local runtime active-deck artifacts, failed posts, runtime status files, workbook exports, API keys, tokens, credentials, webhook URLs, real submitted card IDs, or generated data."
```
