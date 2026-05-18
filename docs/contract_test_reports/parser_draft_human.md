# Parser DraftHuman Contract-Test Report

## Findings

No blocking findings.

### Non-blocking: golden replay and corpus coverage remain intentionally absent

The contract treats focused parser tests, router/package reachability, and
schema snapshot samples as the minimum implementation evidence. Golden replay
and feature-equity corpus coverage are full reliability evidence only when a
safe sanitized or synthetic fixture can be added without scope expansion.

Codex C did not add a DraftHuman golden fixture, and the feature-equity corpus
ratchet still reports `ok` over the existing two manifests with zero DraftHuman
coverage. This is acceptable for the first parser pass, but the PR should state
that live MTGA DraftHuman payload field names, golden replay DraftHuman
coverage, and nonzero corpus ratchet DraftHuman evidence remain unverified.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/123

## Trackers

- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/parser_draft_human.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Reviewed files:

- `docs/contracts/parser_draft_human.md`
- `docs/implementation_handoffs/parser_draft_human_comparison.md`
- `src/mythic_edge_parser/parsers/draft_human.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_draft_human_parser.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`

## Contract Summary

The implementation must add first-class Premier and Traditional human draft
parser support for exact `Draft.Notify`, `EventPlayerDraftMakePick`, and
`LogBusinessEvents` markers. It must emit the existing `DraftHumanEvent`,
preserve the full parsed top-level payload as raw evidence, normalize a stable
payload shape, narrow `LogBusinessEvents` to picked-card evidence, route only
from Unity and UNKNOWN headers, update focused tests and DraftHuman payload
schema snapshots, preserve DraftBot behavior, and avoid DraftComplete,
parser-state, workbook, webhook, Apps Script, secret, raw-log, corpus-baseline,
and production behavior changes outside the explicit contract.

## Checks Run

```powershell
git status --short --branch
git fetch --prune origin
gh issue view 123 --json number,title,state,url,body,labels
git rev-list --left-right --count HEAD...origin/codex/parser-reliability-intelligence
py -m pytest -q tests\test_draft_human_parser.py tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_draft_bot_parser.py tests\test_router_unit.py tests\test_parsers.py
py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
py -m ruff check src tests tools
git diff --check
@'
docs/contracts/parser_draft_human.md
docs/implementation_handoffs/parser_draft_human_comparison.md
src/mythic_edge_parser/parsers/draft_human.py
src/mythic_edge_parser/parsers/__init__.py
src/mythic_edge_parser/router.py
tests/test_draft_human_parser.py
tests/test_router_unit.py
tests/test_event_schema_snapshots.py
tests/fixtures/schema_snapshots/parser_payload_keys.json
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
py -m pytest -q
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
Test-Path tools\check_secret_patterns.py
git diff --name-status origin/codex/parser-reliability-intelligence -- tests\fixtures\golden_replay tests\fixtures\feature_equity_corpus
gh pr list --head codex/parser-reliability-intelligence --json number,title,state,isDraft,baseRefName,headRefName,url
```

## Results

- Issue #123 is open.
- Branch is `codex/parser-reliability-intelligence`.
- Branch is even with `origin/codex/parser-reliability-intelligence`: `0 0`.
- Focused DraftHuman/schema snapshot tests: `47 passed in 0.64s`.
- DraftBot/router/parser regression slice: `70 passed in 0.56s`.
- Related parser reliability slice: `45 passed in 0.95s`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed.
- Path-scoped protected-surface check:
  `changed_paths: 9`, `forbidden: 0`, `warnings: 2`, `result: passed`.
- The two path-scoped warnings are for contract-authorized parser files:
  `src/mythic_edge_parser/parsers/draft_human.py` and
  `src/mythic_edge_parser/parsers/__init__.py`.
- Full local test suite: `819 passed in 4.72s`.
- Golden replay over existing committed manifests:
  `pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- Feature-equity corpus ratchet over existing committed manifests:
  `ok (2 manifests, 2 source files)`.
- `tools/check_secret_patterns.py` is not present on this branch.
- No golden replay fixture or feature-equity corpus baseline path changed.
- No open PR exists with head `codex/parser-reliability-intelligence`.

## Confirmed Contract Matches

- `src/mythic_edge_parser/parsers/draft_human.py` exists and exposes
  `try_parse(entry, timestamp)`.
- The parser recognizes only the contract markers:
  `Draft.Notify`, `EventPlayerDraftMakePick`, and `LogBusinessEvents`.
- Marker matching is exact and case-sensitive; `Draft.Notify` is matched with
  `re.escape()` rather than an unescaped dot pattern.
- The parser emits the existing `DraftHumanEvent`; `DraftHumanEvent.kind`
  remains `"DraftHuman"` and `performance_class` remains durable per-event.
- Metadata preserves timestamp and raw bytes with `EventMetadata(timestamp,
  entry.body.encode())`.
- All payload types use the contract key set and key order:
  `type`, `source_method`, `api_direction`, `draft_id`, `event_id`,
  `draft_status`, `pack_number`, `pick_number`, `pack_card_ids`,
  `picked_card_id`, `picked_card_ids`, `business_event_type`,
  `raw_draft_human`.
- `api_direction` is derived deterministically from the first exact request or
  response marker.
- Marker-wrapped payloads normalize from the nested marker object when it is a
  mapping, while `raw_draft_human` preserves the full parsed top-level object.
- `LogBusinessEvents` emits only when the top-level object, nested mapping, or
  first matching list item contains valid picked-card evidence.
- Missing optional non-business fields use default `""`, `None`, or `[]`
  values.
- Integer normalization accepts non-bool nonnegative integers and digit-only
  strings, while rejecting booleans, floats, negative values, signed strings,
  blank strings, containers, and arbitrary objects.
- Card ID list normalization preserves source order and duplicates and skips
  invalid members.
- `picked_card_id` uses a valid scalar picked-card value when present, otherwise
  falls back to the first normalized picked-card list value only when the scalar
  field is absent.
- Malformed marker-like input and non-dictionary JSON return `None`.
- `parsers.draft_human` is imported through `parsers.__init__` and included in
  `__all__`.
- Router dispatch includes `parsers.draft_human` for
  `EntryHeader.UNITY_CROSS_THREAD_LOGGER` and `EntryHeader.UNKNOWN` only, after
  `draft_bot` and before `rank`.
- Router tests cover Unity and UNKNOWN reachability and preserve DraftBot
  precedence.
- Schema snapshot samples include `DraftHuman.human_draft_notify`,
  `DraftHuman.human_draft_make_pick`, and
  `DraftHuman.human_draft_business_pick` payload keys.
- The implementation does not add DraftComplete behavior.
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

- no committed golden replay DraftHuman fixture;
- no nonzero feature-equity corpus DraftHuman coverage;
- no live MTGA human draft payload evidence validating every source alias;
- no live evidence for whether `LogBusinessEvents` can contain multiple draft
  picks that would require multi-event emission;
- no repo-approved secret/private-content scanner exists on this branch.

## Drift Notes

- Repo drift: expected issue #123 parser, router, test, snapshot, contract, and
  handoff changes only.
- Branch drift: no local/remote branch divergence for
  `codex/parser-reliability-intelligence`.
- Fixture drift: no golden replay fixture or feature-equity corpus baseline
  changed.
- Workbook drift: not inspected and not in scope.
- Deployment drift: not inspected and not in scope.
- Local-data drift: no raw private logs, generated data, runtime status files,
  failed posts, workbook exports, secrets, or local-only artifacts were added.
- PR lifecycle drift: no PR exists yet for the current head branch.

## Protected-Surface Status

Clean for issue #123. The touched protected parser surfaces are authorized by
`docs/contracts/parser_draft_human.md`. No forbidden downstream, runtime,
secret, raw-log, generated-data, workbook, webhook, Apps Script, or production
surface was changed.

## Recommendation

Approve for Codex F: Module Submitter.

Codex F must stage only the issue #123 reviewed package and must not target
`main`. If a draft PR is required, Codex F should stop and ask for the approved
non-main base branch before opening one.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for parser reliability issue #123.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/123

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Reviewed artifacts/files:
- docs/contracts/parser_draft_human.md
- docs/implementation_handoffs/parser_draft_human_comparison.md
- docs/contract_test_reports/parser_draft_human.md
- src/mythic_edge_parser/parsers/draft_human.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/router.py
- tests/test_draft_human_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Codex E verdict:
No blocking findings. The issue #123 DraftHuman parser package is ready to submit.

Expected scope:
- Stage only the reviewed issue #123 files listed above.
- Do not stage unrelated parser reliability branch files, raw logs, generated data, runtime status files, failed posts, workbook exports, secrets, or local-only artifacts.
- Commit the reviewed issue #123 package.
- Push codex/parser-reliability-intelligence.
- Do not open a PR to main. If the workflow requires a draft PR, stop and ask for the approved non-main base branch before opening one.
- Link issue #123 and trackers #47/#11 in the commit or PR text where appropriate.

Validation evidence from Codex E:
- py -m pytest -q tests\test_draft_human_parser.py tests\test_event_schema_snapshots.py -> 47 passed
- py -m pytest -q tests\test_draft_bot_parser.py tests\test_router_unit.py tests\test_parsers.py -> 70 passed
- py -m pytest -q tests\test_parser_small_modules.py tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py -> 45 passed
- py -m ruff check src tests tools -> passed
- git diff --check -> passed
- path-scoped protected-surface gate -> passed with 2 contract-authorized parser warnings
- py -m pytest -q -> 819 passed
- py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay -> pass
- py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json -> ok

Residual risks to mention:
- Remote CI has not run yet.
- No PR exists yet for head codex/parser-reliability-intelligence.
- tools/check_secret_patterns.py is not present on this branch.
- Live MTGA human draft payload field names remain unverified.
- No committed golden replay DraftHuman fixture exists.
- Feature-equity corpus DraftHuman coverage remains zero by design.
- Live workbook state, deployed Apps Script state, and production behavior were not inspected.

Stop conditions:
- Do not change parser behavior beyond the reviewed DraftHuman package.
- Do not add DraftComplete behavior.
- Do not change DraftBot behavior.
- Do not copy Manasight code.
- Do not add raw private Player.log excerpts.
- Do not update golden fixtures or corpus baselines unless the user explicitly routes a new implementation/fixer pass.
- Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates.
- Do not target main.
- Do not mark issue #123, tracker #47, or related tracker #11 complete.
- Do not stage unrelated files.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/123"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/parser_draft_human.md"
  implementation_handoff: "docs/implementation_handoffs/parser_draft_human_comparison.md"
  review_artifact: "docs/contract_test_reports/parser_draft_human.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  verdict: "ready for Codex F"
  findings:
    blocking: []
    non_blocking:
      - "Golden replay and feature-equity corpus DraftHuman coverage remain unimplemented and should be named as residual risk."
  validation:
    - "git rev-list --left-right --count HEAD...origin/codex/parser-reliability-intelligence -> 0 0"
    - "py -m pytest -q tests\\test_draft_human_parser.py tests\\test_event_schema_snapshots.py -> 47 passed in 0.64s"
    - "py -m pytest -q tests\\test_draft_bot_parser.py tests\\test_router_unit.py tests\\test_parsers.py -> 70 passed in 0.56s"
    - "py -m pytest -q tests\\test_parser_small_modules.py tests\\test_feature_equity_corpus_ratchet.py tests\\test_golden_replay_harness.py -> 45 passed in 0.95s"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface gate -> passed with 2 contract-authorized parser warnings"
    - "py -m pytest -q -> 819 passed in 4.72s"
    - "py -m mythic_edge_parser.app.golden_replay tests\\fixtures\\golden_replay -> pass"
    - "py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\\fixtures\\golden_replay --baseline tests\\fixtures\\feature_equity_corpus\\feature_equity_corpus_baseline.v1.json -> ok"
    - "tools/check_secret_patterns.py unavailable on this branch"
    - "gh pr list --head codex/parser-reliability-intelligence -> []"
  forbidden_scope_touched: false
  remaining_unverified:
    - "Remote CI"
    - "Live MTGA human draft payload field names"
    - "Golden replay DraftHuman fixture coverage"
    - "Feature-equity corpus nonzero DraftHuman coverage"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
  stop_conditions:
    - "Do not stage unrelated files outside the issue #123 reviewed package."
    - "Do not change parser behavior beyond the reviewed DraftHuman package."
    - "Do not add DraftComplete behavior."
    - "Do not change DraftBot behavior."
    - "Do not update golden fixtures or corpus baselines in submitter work."
    - "Do not target main."
    - "Do not mark issue #123, tracker #47, or related tracker #11 complete."
```
