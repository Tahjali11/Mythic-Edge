# Parser Opponent Card Observations Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/50

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/48

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/111

Previous merge commit: `76b63622494b0bbc6150e6bd19973b4ac8e0be0c`

## Contract

- `docs/contracts/parser_opponent_card_observations.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Changed files reviewed:

- `docs/contracts/parser_opponent_card_observations.md`
- `docs/implementation_handoffs/parser_opponent_card_observations_comparison.md`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_card_performance.py`

Unrelated local files observed and excluded from this review:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Findings

No blocking findings.

## Contract-Test Verdict

The implementation satisfies the parser opponent-card observation contract in
the reviewed scope. The module is a pure parser-intelligence helper, preserves
parser/state truth ownership, keeps opponent observations out of
card-performance aggregation, and does not expose new workbook, webhook,
Apps Script, runtime status, generated-data, model-provider, or output
transport behavior.

Next recommended role: Codex F: Module Submitter.

## Contract Summary

The opponent-card observation module must record deterministic
parser-supported facts about opponent-visible cards and actions without
guessing hidden cards, completing decklists, classifying archetypes, or moving
truth into AI, analytics, workbook formulas, dashboard logic, Apps Script, or
webhook transport. V1 may emit local JSON-serializable helper payloads from
gameplay action entries, but it must not add workbook columns, webhook fields,
Apps Script behavior, runtime status schema, parser event classes, or parser
state final-reconciliation behavior.

## Checks Run

```bash
git fetch --prune
gh issue view 50 --json number,title,state,body,labels,url
gh issue view 47 --json number,title,state,url
python3 -m pytest -q tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
printf '%s\n' src/mythic_edge_parser/app/opponent_card_observations.py tests/test_opponent_card_observations.py tests/test_card_performance.py docs/contracts/parser_opponent_card_observations.md docs/implementation_handoffs/parser_opponent_card_observations_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m pytest -q
python3 tools/select_validation.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
```

## Results

- Issue #50: open, tracker #47-linked, parser reliability branch scope
  confirmed.
- Tracker #47: open.
- Focused opponent-observation tests: `10 passed in 0.03s`.
- Gameplay/card-performance/catalog compatibility tests:
  `24 passed in 0.13s`.
- Golden replay focused tests: `12 passed in 0.12s`.
- Golden replay CLI over committed manifests:
  `Golden replay: pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- Protected-surface gate against `origin/main`: `changed_paths: 33`,
  `forbidden: 0`, `warnings: 4`, `result: passed`.
- Explicit #50 changed-path protected-surface gate:
  `changed_paths: 5`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- Full local test suite: `717 passed in 1.01s`.
- `tools/select_validation.py`: unavailable on this branch.
- `tools/check_secret_patterns.py`: unavailable on this branch.

The four protected-surface warnings from the `origin/main` branch diff are
from previously merged parser reliability issue #107 surfaces:
`src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`, and
`src/mythic_edge_parser/parsers/truncation.py`. The explicit #50 local
changed-path protected-surface check has no warnings.

## Confirmed Contract Matches

- `src/mythic_edge_parser/app/opponent_card_observations.py` exposes the
  contracted constants and helper functions:
  `OPPONENT_CARD_OBSERVATION_OBJECT`,
  `OPPONENT_CARD_OBSERVATIONS_OBJECT`, `SCHEMA_VERSION`,
  `build_opponent_card_observation()`, and
  `build_opponent_card_observations_payload()`.
- The helper returns JSON-serializable dictionaries and does not mutate input
  action entries.
- Non-mapping inputs, non-opponent entries, unsupported action types, and
  hidden draw-from-library-to-hand entries return neutral `None`.
- Emitted observations always use `actor_relation="opponent"`.
- Clean visible opponent spell observations preserve match/game context,
  timestamp, turn, actor/local seats, instance ID, GRP IDs, identity hint
  source, action type, visibility, source evidence, evidence status, value
  source, confidence, raw action types, annotations, and degradation flags.
- Actor seat can be derived from direct action-array seat evidence when the
  action entry lacks `actor_seat_id`.
- Canonical, observed, overlay, object-source, and parent IDs remain visible
  when they differ.
- Missing local or actor seat mapping emits degraded/review-required
  observations rather than guessing clean seat identity.
- Missing card identity emits degraded/review-required observations without
  guessing IDs or names.
- Candidate and contradicted name resolution remain lower-confidence
  enrichment and do not overwrite observed ID evidence as clean resolved names.
- Unresolved known IDs preserve the ID and use placeholder display text without
  claiming a resolved card name.
- Contradictory seat evidence produces conflict status, low confidence, a
  degradation flag, and review requirement.
- Collection payloads report total observation count, degraded count, and
  aggregate review status.
- The helper has no filesystem writes and imports no workbook, webhook,
  Apps Script, OpenAI/model-provider, diagnostics, golden replay, output
  transport, generated-data, or runtime status surfaces.
- `tests/test_card_performance.py` now freezes that opponent action entries
  remain excluded from card-performance aggregation.
- Existing golden replay manifests remain compatible because no required
  opponent-observation manifest section was added.
- No workbook schema, webhook payload shape, Apps Script behavior, output
  transport, parser state final reconciliation, parser event classes,
  match/game identity, deduplication, secrets, environment variables, raw
  logs, generated data, runtime status files, failed posts, workbook exports,
  or production deployment behavior changes were found in the #50 module
  scope.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

Focused tests cover clean observation shape, input immutability, action-array
seat derivation, ID preservation, non-opponent/non-mapping neutral behavior,
missing seat mapping degradation, hidden draw suppression, missing card
identity degradation, candidate and contradicted name resolution, contradictory
seat evidence, unresolved known ID behavior, collection counts, and
card-performance opponent exclusion.

Non-blocking note: ambiguous and name-only resolution statuses are handled by
the same status-normalization and degradation branches, but they do not have
separate one-case focused tests in this pass. The current contract does not
require a golden replay fixture for v1, and the implementation handoff records
that decision.

## Drift Notes

- Repo drift: expected addition of a pure opponent-observation helper,
  focused tests, a card-performance exclusion test update, contract, handoff,
  and this contract-test report.
- Parser behavior drift: none found.
- Parser state final reconciliation drift: none found.
- Parser event class drift: none found.
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
  #50 scope.
- Previous issue #107 drift: still present in branch comparisons against
  `origin/main` and not part of this #50 finding set.

## Remaining Non-Blocking Gaps

- Remote CI has not run in this local Codex E pass.
- The active branch does not contain `tools/select_validation.py` or
  `tools/check_secret_patterns.py`; these optional hardening validations were
  recorded as unavailable.
- No golden replay opponent-observation fixture was added in v1; focused unit
  tests cover the helper boundaries, and existing golden replay compatibility
  passed.
- The helper is not yet integrated into runtime gameplay action artifacts,
  workbook/webhook output, diagnostics summaries, or analytics surfaces. That
  is intentional v1 scope and would need a new contract if expanded.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for parser reliability issue #50.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/50

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Use:
- docs/contracts/parser_opponent_card_observations.md
- docs/implementation_handoffs/parser_opponent_card_observations_comparison.md
- docs/contract_test_reports/parser_opponent_card_observations.md

Goal:
Stage only the reviewed opponent-card observation package, commit, push, and
open or update a draft PR against codex/parser-reliability-intelligence. Do
not target main.

Reviewed files:
- docs/contracts/parser_opponent_card_observations.md
- docs/implementation_handoffs/parser_opponent_card_observations_comparison.md
- docs/contract_test_reports/parser_opponent_card_observations.md
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_opponent_card_observations.py
- tests/test_card_performance.py

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
- No automatic archetype, decklist, hidden-card, likely-copy, AI/model-provider,
  or analytics truth behavior was added.

Validation evidence to include:
- python3 -m pytest -q tests/test_opponent_card_observations.py -> 10 passed
- python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py -> 24 passed
- python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed
- python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass
- python3 -m ruff check src tests tools -> All checks passed!
- git diff --check -> passed
- python3 tools/check_protected_surfaces.py --base origin/main -> passed with only prior #107 protected-surface warnings
- explicit #50 local changed-path protected-surface stdin check -> passed with 0 warnings
- python3 -m pytest -q -> 717 passed
- tools/select_validation.py and tools/check_secret_patterns.py were unavailable on this branch

Do not stage unrelated files. Do not merge, close issue #50, mark tracker #47
complete, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/50"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/111"
  previous_merge_commit: "76b63622494b0bbc6150e6bd19973b4ac8e0be0c"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_opponent_card_observations.md"
  target_artifact: "docs/contract_test_reports/parser_opponent_card_observations.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  verdict: "No blocking findings. Ready for Codex F."
  validation:
    - "python3 -m pytest -q tests/test_opponent_card_observations.py -> 10 passed"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py -> 24 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed"
    - "python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass"
    - "python3 -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed with only prior #107 protected-surface warnings"
    - "explicit #50 local changed-path protected-surface stdin check -> passed with 0 warnings"
    - "python3 -m pytest -q -> 717 passed"
    - "not run - tools/select_validation.py unavailable on this branch"
    - "not run - tools/check_secret_patterns.py unavailable on this branch"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not infer hidden opponent cards, complete opponent decklists, classify archetypes, call OpenAI/model providers, or move parser truth into workbook formulas, dashboard logic, webhook transport, Apps Script, AI, or analytics surfaces."
    - "Do not make card performance aggregate opponent cards."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
    - "Do not stage unrelated docs/.DS_Store, repo-wide hardening local report, or LLM advisory scaffold files."
```
