# Parser Draft Fixture Coverage Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/126

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/parser_draft_bot.md`
- `docs/contracts/parser_draft_human.md`
- `docs/contracts/parser_draft_complete.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`

## Implementation Under Test

Local detached worktree:
`/Users/tahjblow/Documents/New project/Mythic-Edge-issue-126`

Base target:
`codex/parser-reliability-intelligence`

Implementation handoff:
`docs/implementation_handoffs/parser_draft_fixture_coverage_comparison.md`

Changed and untracked files under review:

- `docs/implementation_handoffs/parser_draft_fixture_coverage_comparison.md`
- `tests/fixtures/draft_parser_family_slice.log`
- `tests/fixtures/golden_replay/draft_parser_family.manifest.json`
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
- `tests/test_golden_replay_harness.py`
- `tests/test_feature_equity_corpus_ratchet.py`

## Findings

No blocking findings.

## Contract-Test Verdict

Pass. The issue #126 package adds safe draft parser family fixture coverage and
count-only corpus baseline updates without changing parser behavior or protected
downstream surfaces. It is ready for Codex F: Module Submitter.

## Confirmed Contract Matches

- The new fixture is explicitly synthetic and states that it is not a raw
  `Player.log` excerpt.
- The fixture replays through the normal `LineBuffer` and `Router` path and
  emits `DraftBot`, `DraftHuman`, and `DraftComplete` event families.
- Golden replay reports the draft manifest as `pass`, with no degradation,
  review, diff, fail, truncation, or data-loss signals.
- The synthetic `GameState` line is used only as a diagnostics/parser-state
  anchor. The manifest does not claim match completion, game result, hidden-card
  inference, decklist truth, archetype classification, coaching, workbook,
  webhook, Apps Script, or AI/model-provider truth.
- The feature-equity corpus baseline update is count-only and records the new
  observed draft-family counts, routed-entry count, source-file count, and the
  extra GameState anchor count.
- Focused tests now assert three committed golden manifests, nonzero draft
  event-family counts, draft payload-type counts, and an updated corpus
  baseline diff expectation.
- Parser source, router source, event classes, parser state reconciliation,
  workbook schema, webhook payloads, Apps Script behavior, output transport,
  match/game identity, deduplication, secrets, environment contracts, raw logs,
  generated data, runtime status files, failed posts, workbook exports,
  draft coaching, ratings, hidden-information inference, and model-provider
  behavior were not changed by the issue #126 patch.

## Contract Mismatches

None.

## Missing Tests

None blocking.

The new golden/corpus coverage is family-level rather than exhaustive subtype
coverage. For example, the draft fixture covers one `DraftHuman` subtype and one
`DraftBot` subtype while focused parser tests continue to cover the broader
marker matrix. This matches issue #126's stated nonzero corpus-coverage goal,
but future fixture expansion could add more draft subtype replay evidence.

## Drift Notes

- Worktree drift: the review worktree is detached at `7540473`, the #125
  DraftComplete merge commit, with issue #126 changes still unstaged/untracked.
  Submitter work should attach or copy the package onto a branch targeting
  `codex/parser-reliability-intelligence`, not `main`.
- Branch-scope protected-surface warnings appear when checking the entire
  branch against `origin/main`; those are inherited parser-reliability changes
  from earlier modules, not issue #126 changed-file findings.
- Existing vocabulary note: the fixture is synthetic via `source_kind` and
  `sanitization_status`, while the current golden replay validator still uses
  `source_privacy_class: sanitized_committable`. The corpus therefore counts it
  under `fixtures_sanitized_committable`, not `fixtures_synthetic_committable`.
  This follows the current harness behavior and is not a blocker for issue #126.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py
# 13 passed in 0.11s

python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py
# 7 passed in 0.11s

python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
# 115 passed in 0.06s

python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py
# 23 passed in 0.08s

PYTHONPATH=src python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
# Golden replay: pass (3 manifests, 3 pass, 0 degraded, 0 review, 0 diff, 0 fail)

PYTHONPATH=src python3 -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests/fixtures/golden_replay --baseline tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
# Feature-equity corpus ratchet: ok (3 manifests, 3 source files)

python3 -m pytest -q tests
# 859 passed in 1.10s

python3 -m ruff check src tests tools
# All checks passed!

git diff --check
# passed

printf '<issue #126 changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# Protected Surface Gate: passed; forbidden: 0; warnings: 0

python3 tools/check_protected_surfaces.py --base origin/main
# Protected Surface Gate: passed; forbidden: 0; warnings: 12 branch-scope inherited parser reliability warnings
```

`tools/check_secret_patterns.py` is not present in this parser-reliability
worktree. A direct `rg` scan over the issue #126 changed paths found only
intentional test placeholders and explanatory `Player.log` references; no live
secret, webhook, workbook, local-path, failed-post, runtime-status, generated
data, or private-log fixture content was found.

## Protected-Surface Review

The issue #126 changed-file set is limited to docs, tests, a synthetic fixture
log, a golden replay manifest, and a count-only feature-equity corpus baseline.
No parser/runtime/workbook/webhook/App Script behavior files changed.

## Remaining Non-Blocking Gaps

- Live private draft evidence remains intentionally unused.
- Draft golden/corpus coverage is not exhaustive across every draft marker
  subtype; focused parser tests remain the primary subtype-level coverage.
- CI has not been run by this reviewer.

## Recommendation

Approve for the next workflow role.

Next role: Codex F: Module Submitter.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/126"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_draft_fixture_coverage.md"
  target_artifact: "Codex F Module Submitter package for issue #126"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  branch: "codex/parser-reliability-intelligence"
  worktree: "/Users/tahjblow/Documents/New project/Mythic-Edge-issue-126"
  risk_tier: "Medium"
  validation:
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 13 passed"
    - "python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py -> 7 passed"
    - "python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py -> 115 passed"
    - "python3 -m pytest -q tests/test_router_unit.py tests/test_event_schema_snapshots.py -> 23 passed"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests/fixtures/golden_replay --baseline tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json -> ok"
    - "python3 -m pytest -q tests -> 859 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47 or related issue #11."
    - "Do not change parser behavior, router behavior, parser state final reconciliation, parser event classes, DraftBot/DraftHuman/DraftCompleteEvent.kind, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, runtime status files, failed posts, workbook exports, production behavior, secrets, environment variable contracts, or AI/model-provider behavior."
    - "Do not commit raw private Player.log evidence, local logs, local private reports, generated data, credentials, tokens, webhook URLs, API keys, or workbook exports."
```
