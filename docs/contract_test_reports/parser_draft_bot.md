# Parser DraftBot Contract-Test Report

## Findings

No blocking findings.

### Non-blocking: golden replay and corpus coverage remain intentionally absent

The contract defines focused parser tests, router/package reachability, and
schema snapshot samples as the minimum implementation evidence. Golden replay
and feature-equity corpus coverage are full reliability evidence only when a
safe sanitized or synthetic fixture can be added without scope expansion. Codex
C did not add such a fixture, and the feature-equity corpus ratchet still
reports `ok` over the existing two manifests with zero DraftBot coverage.

This is acceptable for the first parser pass, but the PR should state that live
MTGA DraftBot field names, golden replay DraftBot coverage, and nonzero corpus
ratchet DraftBot evidence remain unverified.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/122

## Trackers

- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/parser_draft_bot.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Reviewed files:

- `docs/contracts/parser_draft_bot.md`
- `docs/implementation_handoffs/parser_draft_bot_comparison.md`
- `src/mythic_edge_parser/parsers/draft_bot.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_draft_bot_parser.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`

## Contract Summary

The implementation must add first-class Quick Draft / bot draft parser support
for exact `BotDraftDraftStatus` and `BotDraftDraftPick` API markers. It must
emit the existing `DraftBotEvent`, preserve raw parsed draft payload evidence,
normalize a stable small payload shape, route only from Unity and UNKNOWN
headers, update focused tests and DraftBot payload schema snapshots, and avoid
DraftHuman, DraftComplete, parser state, workbook, webhook, Apps Script, secret,
raw-log, corpus-baseline, and production behavior changes outside the explicit
contract.

## Checks Run

```powershell
git fetch --prune origin
gh issue view 122 --json number,title,state,url,body,labels
git status --short --branch
git rev-list --left-right --count HEAD...origin/codex/parser-reliability-intelligence
py -m pytest -q tests\test_draft_bot_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
py -m pytest -q tests\test_router_unit.py tests\test_parsers.py
py -m ruff check src tests tools
git diff --check
@'
docs/contracts/parser_draft_bot.md
docs/implementation_handoffs/parser_draft_bot_comparison.md
src/mythic_edge_parser/parsers/draft_bot.py
src/mythic_edge_parser/parsers/__init__.py
src/mythic_edge_parser/router.py
tests/test_draft_bot_parser.py
tests/test_router_unit.py
tests/test_event_schema_snapshots.py
tests/fixtures/schema_snapshots/parser_payload_keys.json
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py -m pytest -q
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
py tools\check_protected_surfaces.py --base origin/main
gh pr list --head codex/parser-reliability-intelligence --json number,title,state,isDraft,baseRefName,headRefName,url
```

Secret/private scanner check:

```powershell
Test-Path tools\check_secret_patterns.py
```

## Results

- Issue #122 is open.
- Branch is `codex/parser-reliability-intelligence`.
- Branch is even with `origin/codex/parser-reliability-intelligence`: `0 0`.
- Focused DraftBot tests: `35 passed in 0.46s`.
- Schema snapshot tests: `6 passed in 0.53s`.
- Related parser reliability slice:
  `45 passed in 0.92s`.
- Router/parser slice:
  `35 passed in 0.51s`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed.
- Path-scoped protected-surface check:
  `changed_paths: 9`, `forbidden: 0`, `warnings: 2`, `result: passed`.
- The two path-scoped warnings are for contract-authorized parser files:
  `src/mythic_edge_parser/parsers/draft_bot.py` and
  `src/mythic_edge_parser/parsers/__init__.py`.
- Full local test suite: `778 passed in 4.66s`.
- Golden replay over existing committed manifests:
  `pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- Feature-equity corpus ratchet over existing committed manifests:
  `ok (2 manifests, 2 source files)`.
- Branch-wide protected-surface gate passed with `forbidden: 0` and 9 warnings
  from earlier parser reliability branch work outside issue #122.
- `tools/check_secret_patterns.py` is not present on this branch.
- No open PR exists with head `codex/parser-reliability-intelligence`.

## Confirmed Contract Matches

- `src/mythic_edge_parser/parsers/draft_bot.py` exists and exposes
  `try_parse(entry, timestamp)`.
- The parser recognizes only the contract markers:
  `BotDraftDraftStatus` and `BotDraftDraftPick`.
- Marker matching is case-sensitive and focused tests reject case variants,
  human draft markers, draft completion markers, and generic prose.
- The parser emits the existing `DraftBotEvent`; `DraftBotEvent.kind` remains
  `"DraftBot"` and `performance_class` remains durable per-event.
- Metadata preserves timestamp and raw bytes with `EventMetadata(timestamp,
  entry.body.encode())`.
- Both payload types use the contract key set and key order:
  `type`, `source_method`, `api_direction`, `draft_id`, `event_id`,
  `draft_status`, `pack_number`, `pick_number`, `pack_card_ids`,
  `picked_card_id`, `picked_card_ids`, `raw_draft_bot`.
- `api_direction` is derived deterministically from the first exact request or
  response marker.
- Marker-wrapped payloads normalize from the nested marker object when it is a
  mapping, while `raw_draft_bot` preserves the full parsed top-level object.
- Missing optional fields use default `""`, `None`, or `[]` values.
- Integer normalization accepts non-bool nonnegative integers and digit-only
  strings, while rejecting booleans, floats, negative values, signed strings,
  blank strings, containers, and arbitrary objects.
- Card ID list normalization preserves source order and duplicates and skips
  invalid members.
- `picked_card_id` uses the scalar picked-card value when present, otherwise
  falls back to the first normalized picked-card list value.
- Malformed marker-like input and non-dictionary JSON return `None`.
- `parsers.draft_bot` is imported through `parsers.__init__` and included in
  `__all__`.
- Router dispatch includes `parsers.draft_bot` for
  `EntryHeader.UNITY_CROSS_THREAD_LOGGER` and `EntryHeader.UNKNOWN` only, after
  `event_lifecycle` and before `rank`.
- Router tests cover Unity and UNKNOWN routing and preserve the EventLifecycle
  precedence case.
- Schema snapshot samples include both `DraftBot.bot_draft_status` and
  `DraftBot.bot_draft_pick` payload keys.
- The implementation does not add DraftHuman or DraftComplete behavior.
- The implementation does not change parser state final reconciliation,
  workbook schema, webhook payload shape, Apps Script behavior, parser event
  classes, event kind values, match/game identity, deduplication, runtime
  status files, failed posts, workbook exports, generated data, secrets,
  environment variables, production behavior, or CI gates.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocking missing tests for the implemented first pass.

Remaining non-blocking gaps:

- no committed golden replay DraftBot fixture;
- no nonzero feature-equity corpus DraftBot coverage;
- no live MTGA bot draft payload evidence validating every source alias;
- no repo-approved secret/private-content scanner exists on this branch.

## Drift Notes

- Repo drift: expected issue #122 parser, router, test, snapshot, contract, and
  handoff changes only.
- Branch drift: branch-wide protected-surface warnings exist from earlier parser
  reliability work outside issue #122; path-scoped issue #122 warnings are
  limited to contract-authorized parser files.
- Workbook drift: not inspected and not in scope.
- Deployment drift: not inspected and not in scope.
- Local-data drift: no raw private logs, generated data, runtime status files,
  failed posts, workbook exports, secrets, or local-only artifacts were added.
- PR lifecycle drift: no PR exists yet for the current head branch.

## Protected-Surface Status

Clean for issue #122. The touched protected parser surfaces are authorized by
`docs/contracts/parser_draft_bot.md`. No forbidden downstream, runtime,
secret, raw-log, generated-data, workbook, webhook, Apps Script, or production
surface was changed.

## Recommendation

Approve for Codex F: Module Submitter.

Codex F must stage only the issue #122 reviewed package and must not target
`main`. If a draft PR is required, Codex F should stop and ask for the approved
non-main base branch before opening one.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for parser reliability issue #122.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/122

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Reviewed artifacts/files:
- docs/contracts/parser_draft_bot.md
- docs/implementation_handoffs/parser_draft_bot_comparison.md
- docs/contract_test_reports/parser_draft_bot.md
- src/mythic_edge_parser/parsers/draft_bot.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/router.py
- tests/test_draft_bot_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Codex E verdict:
No blocking findings. The issue #122 DraftBot parser package is ready to submit.

Expected scope:
- Stage only the reviewed issue #122 files listed above.
- Do not stage unrelated parser reliability branch files, raw logs, generated data, runtime status files, failed posts, workbook exports, secrets, or local-only artifacts.
- Commit the reviewed issue #122 package.
- Push codex/parser-reliability-intelligence.
- Do not open a PR to main. If the workflow requires a draft PR, stop and ask for the approved non-main base branch before opening one.
- Link issue #122 and trackers #47/#11 in the commit or PR text where appropriate.

Validation evidence from Codex E:
- py -m pytest -q tests\test_draft_bot_parser.py -> 35 passed
- py -m pytest -q tests\test_event_schema_snapshots.py -> 6 passed
- py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py -> 45 passed
- py -m pytest -q tests\test_router_unit.py tests\test_parsers.py -> 35 passed
- py -m ruff check src tests tools -> passed
- git diff --check -> passed
- path-scoped protected-surface gate -> passed with 2 contract-authorized parser warnings
- py -m pytest -q -> 778 passed
- py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay -> pass
- py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json -> ok

Residual risks to mention:
- Remote CI has not run yet.
- No PR exists yet for head codex/parser-reliability-intelligence.
- tools/check_secret_patterns.py is not present on this branch.
- Live MTGA bot draft payload field names remain unverified.
- No committed golden replay DraftBot fixture exists.
- Feature-equity corpus DraftBot coverage remains zero by design.
- Live workbook state, deployed Apps Script state, and production behavior were not inspected.

Stop conditions:
- Do not change parser behavior beyond the reviewed DraftBot package.
- Do not add DraftHuman or DraftComplete behavior.
- Do not add raw private Player.log excerpts.
- Do not update golden fixtures or corpus baselines unless the user explicitly routes a new implementation/fixer pass.
- Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates.
- Do not target main.
- Do not mark issue #122, tracker #47, or related tracker #11 complete.
- Do not stage unrelated files.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/122"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/parser_draft_bot.md"
  implementation_handoff: "docs/implementation_handoffs/parser_draft_bot_comparison.md"
  review_artifact: "docs/contract_test_reports/parser_draft_bot.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  verdict: "ready for Codex F"
  findings:
    blocking: []
    non_blocking:
      - "Golden replay and feature-equity corpus DraftBot coverage remain unimplemented and should be named as residual risk."
  validation:
    - "git rev-list --left-right --count HEAD...origin/codex/parser-reliability-intelligence -> 0 0"
    - "py -m pytest -q tests\\test_draft_bot_parser.py -> 35 passed in 0.46s"
    - "py -m pytest -q tests\\test_event_schema_snapshots.py -> 6 passed in 0.53s"
    - "py -m pytest -q tests\\test_parser_small_modules.py tests\\test_feature_equity_corpus_ratchet.py tests\\test_golden_replay_harness.py -> 45 passed in 0.92s"
    - "py -m pytest -q tests\\test_router_unit.py tests\\test_parsers.py -> 35 passed in 0.51s"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface gate -> passed with 2 contract-authorized parser warnings"
    - "py -m pytest -q -> 778 passed in 4.66s"
    - "py -m mythic_edge_parser.app.golden_replay tests\\fixtures\\golden_replay -> pass"
    - "py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\\fixtures\\golden_replay --baseline tests\\fixtures\\feature_equity_corpus\\feature_equity_corpus_baseline.v1.json -> ok"
    - "tools/check_secret_patterns.py unavailable on this branch"
    - "gh pr list --head codex/parser-reliability-intelligence -> []"
  forbidden_scope_touched: false
  remaining_unverified:
    - "Remote CI"
    - "Live MTGA bot draft payload field names"
    - "Golden replay DraftBot fixture coverage"
    - "Feature-equity corpus nonzero DraftBot coverage"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
  stop_conditions:
    - "Do not stage unrelated files outside the issue #122 reviewed package."
    - "Do not change parser behavior beyond the reviewed DraftBot package."
    - "Do not add DraftHuman or DraftComplete behavior."
    - "Do not update golden fixtures or corpus baselines in submitter work."
    - "Do not target main."
    - "Do not mark issue #122, tracker #47, or related tracker #11 complete."
```
