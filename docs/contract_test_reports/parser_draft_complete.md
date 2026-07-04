# Parser DraftComplete Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/124

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence-ledger issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/parser_draft_complete.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Worktree:

- `/Users/<redacted>/Documents/New project/Mythic-Edge-issue-124`

Branch target:

- `codex/parser-reliability-intelligence`

Worktree note:

- The worktree is detached at `origin/codex/parser-reliability-intelligence`
  commit `11ce81d`, not currently on a named local branch. This is not a
  contract blocker, but Codex F should create or attach the intended submission
  branch before staging and pushing.

Changed files reviewed:

- `docs/contracts/parser_draft_complete.md`
- `src/mythic_edge_parser/parsers/draft_complete.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_draft_complete_parser.py`
- `tests/test_router_unit.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `docs/implementation_handoffs/parser_draft_complete_comparison.md`

## Findings

No blocking findings.

## Contract-Test Verdict

The implementation satisfies the DraftComplete parser contract in the reviewed
scope. `DraftCompleteDraft` request and response markers emit the existing
`DraftCompleteEvent`, payload keys and normalization behavior match the
contract, DraftBot and DraftHuman behavior remains preserved, router reachability
is limited to Unity and UNKNOWN headers in the contracted order, and the schema
snapshot update is limited to `DraftComplete.draft_complete_draft`.

Next recommended role: Codex F: Module Submitter.

## Contract Summary

The DraftComplete module must add first-class parser-owned recognition for the
exact `DraftCompleteDraft` marker, preserve raw parsed payload evidence, emit
the existing `DraftCompleteEvent` with a stable payload shape, avoid false
positives against DraftBot/DraftHuman/prose markers, and wire the parser into
Unity and UNKNOWN router buckets without changing event classes, parser state,
workbook/webhook/App Script surfaces, draft advice, ratings, or analytics
truth.

## Checks Run

```bash
git fetch --prune
gh issue view 124 --json number,title,state,body,labels,url
python3 -m pytest -q tests/test_draft_complete_parser.py
python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py
python3 -m pytest -q tests/test_router_unit.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m ruff check src tests tools
git diff --check
for f in docs/contracts/parser_draft_complete.md src/mythic_edge_parser/parsers/draft_complete.py tests/test_draft_complete_parser.py docs/implementation_handoffs/parser_draft_complete_comparison.md; do out=$(git diff --no-index --check /dev/null "$f" 2>&1 || true); if [ -n "$out" ]; then printf '%s\n%s\n' "$f" "$out"; exit 1; fi; done; printf 'new-file whitespace check passed\n'
python3 tools/check_protected_surfaces.py --base origin/main
printf '%s\n' docs/contracts/parser_draft_complete.md src/mythic_edge_parser/parsers/draft_complete.py src/mythic_edge_parser/parsers/__init__.py src/mythic_edge_parser/router.py tests/test_draft_complete_parser.py tests/test_router_unit.py tests/test_event_schema_snapshots.py tests/fixtures/schema_snapshots/parser_payload_keys.json docs/implementation_handoffs/parser_draft_complete_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --base origin/main
python3 -m pytest -q tests
```

## Results

- Issue #124: open, tracker #47-linked, parser reliability branch scope
  confirmed.
- DraftComplete parser tests: `39 passed in 0.05s`.
- DraftBot and DraftHuman regression tests: `76 passed in 0.08s`.
- Router unit tests: `17 passed in 0.04s`.
- Event schema snapshot tests: `6 passed in 0.13s`.
- Feature-equity corpus ratchet tests: `7 passed in 0.18s`.
- Golden replay harness tests: `12 passed in 0.18s`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- New-file whitespace check: `new-file whitespace check passed`.
- Branch-scope protected-surface gate against `origin/main`: `changed_paths: 77`,
  `forbidden: 0`, `warnings: 11`, `result: passed`.
- Explicit #124 changed-path protected-surface gate: `changed_paths: 9`,
  `forbidden: 0`, `warnings: 2`, `result: passed`.
- `tools/check_secret_patterns.py`: unavailable in this worktree.
- Full local test suite: `858 passed in 1.06s`.

The two explicit #124 protected-surface warnings are contract-authorized parser
package changes:

- `src/mythic_edge_parser/parsers/draft_complete.py`
- `src/mythic_edge_parser/parsers/__init__.py`

The branch-scope protected-surface warnings include prior parser reliability
work already present on `codex/parser-reliability-intelligence`, plus the
current parser package surface:

- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/parsers/draft_bot.py`
- `src/mythic_edge_parser/parsers/draft_human.py`
- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state_diff.py`
- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/truncation.py`

## Confirmed Contract Matches

- `src/mythic_edge_parser/parsers/draft_complete.py` exists and exposes the
  contracted `try_parse(entry, timestamp)` hook plus the
  `DRAFT_COMPLETE_DRAFT_MARKER` marker constant.
- The implementation emits the existing `DraftCompleteEvent`; no new event
  class was added.
- `DraftCompleteEvent.kind` remains `"DraftComplete"`.
- `DraftCompleteEvent.performance_class` remains `DurablePerEvent`.
- Parser metadata preserves timestamp and raw entry body bytes.
- Exact `==> DraftCompleteDraft` and `<== DraftCompleteDraft` markers emit
  `api_direction` values of `request` and `response`.
- Marker matching is exact and case-sensitive for the tested contract cases,
  including rejection of case variants, suffix variants, dotted variants,
  generic prose, DraftBot markers, DraftHuman markers, `LogBusinessEvents`,
  and `PickGrpId`.
- The payload uses the contracted stable key set and order:
  `type`, `source_method`, `api_direction`, `draft_id`, `event_id`,
  `queue_id`, `draft_status`, `completion_status`, `draft_type`,
  `draft_mode`, `completion_source`, `is_bot_draft`, `is_human_draft`,
  `raw_draft_complete`.
- Direct payloads normalize accepted aliases from the top-level dictionary.
- Marker-wrapped payloads normalize from the nested `DraftCompleteDraft`
  dictionary when that nested value is a mapping.
- Marker-wrapped non-mapping payloads fall back to top-level normalization and
  preserve the full top-level raw payload.
- Missing optional fields emit the contracted defaults: `""`, `None`, and
  `"DraftCompleteDraft"`.
- String fields accept only strings and strip whitespace.
- Boolean fields accept only real booleans and reject strings, integers,
  floats, containers, objects, and `None`.
- Malformed JSON, missing JSON, and non-dictionary JSON return `None`.
- `raw_draft_complete` preserves the full parsed top-level JSON object and
  does not normalize card ratings, decklists, archetypes, draft advice, or
  hidden facts.
- `src/mythic_edge_parser/parsers/__init__.py` imports and exports
  `draft_complete`.
- `src/mythic_edge_parser/router.py` dispatches DraftComplete only from
  `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN` headers.
- DraftComplete is ordered after DraftHuman and before Rank in both contracted
  router buckets.
- Existing DraftBot and DraftHuman focused tests pass unchanged.
- Router tests confirm DraftBot and DraftHuman route to their existing event
  families with DraftComplete present in dispatch order.
- `tests/test_event_schema_snapshots.py` imports `draft_complete` and includes
  a `DraftComplete.draft_complete_draft` sample event.
- `tests/fixtures/schema_snapshots/parser_payload_keys.json` adds only the
  expected DraftComplete payload-key entry for this module.
- `tests/fixtures/schema_snapshots/parser_event_classes.json` did not change.
- No parser state final reconciliation, workbook schema, webhook payload
  shape, Apps Script behavior, match/game identity, deduplication, secrets,
  environment variables, raw logs, generated data, runtime status files,
  failed posts, workbook exports, production behavior, draft pick coaching,
  card ratings, deck construction analytics, hidden-card inference, archetype
  classification, gameplay advice, OpenAI/model-provider behavior, or
  AI/analytics truth changes were found in the #124 scope.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

Focused tests cover direct and marker-wrapped payloads, defaults, nested
non-mapping fallback, string normalization boundaries, boolean normalization
boundaries, malformed marker-like inputs, non-dict JSON, false positives,
first-marker policy, public package import, Unity and UNKNOWN router
reachability, routed/unknown stats, and DraftBot/DraftHuman route preservation.

Non-blocking gap: no safe committed golden replay fixture or feature-equity
corpus fixture was added, so the feature-equity corpus baseline still records
zero `DraftComplete` counts. The contract allows this as a remaining
unverified layer when safe fixture coverage is not added in the implementation
pass.

## Drift Notes

- Repo drift: expected addition of DraftComplete contract, parser module,
  router/package wiring, focused tests, schema snapshot payload-key entry,
  implementation handoff, and this contract-test report.
- Parser behavior drift: contract-authorized DraftComplete event recognition
  only.
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
  #124 scope.
- Worktree drift: the review worktree is detached at
  `origin/codex/parser-reliability-intelligence` commit `11ce81d`; Codex F
  should attach/create the intended branch before submitter work.

## Remaining Non-Blocking Gaps

- Remote CI has not run in this local Codex E pass.
- `tools/check_secret_patterns.py` is absent in this worktree, so the optional
  branch-native content scanner was recorded as unavailable.
- No live private `Player.log` evidence, workbook writes, webhook delivery,
  Apps Script behavior, runtime status files, failed posts, workbook exports,
  CI in GitHub, or production behavior was exercised.
- Draft golden replay and feature-equity corpus count coverage remain future
  fixture work.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #124: DraftComplete parser module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Related evidence-ledger issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/124
- Branch/base: codex/parser-reliability-intelligence
- Worktree reviewed by Codex E: /Users/<redacted>/Documents/New project/Mythic-Edge-issue-124
- Contract: docs/contracts/parser_draft_complete.md
- Implementation handoff: docs/implementation_handoffs/parser_draft_complete_comparison.md
- Contract-test report: docs/contract_test_reports/parser_draft_complete.md

Important worktree note:
- The reviewed worktree is detached at origin/codex/parser-reliability-intelligence commit 11ce81d.
- Before staging/pushing, create or attach the intended issue branch for the DraftComplete submission.

Goal:
Prepare the DraftComplete parser package for PR submission into codex/parser-reliability-intelligence.

Scope to include:
- docs/contracts/parser_draft_complete.md
- docs/implementation_handoffs/parser_draft_complete_comparison.md
- docs/contract_test_reports/parser_draft_complete.md
- src/mythic_edge_parser/parsers/draft_complete.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/router.py
- tests/test_draft_complete_parser.py
- tests/test_router_unit.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Codex E verdict:
No blocking findings. The implementation satisfies the DraftComplete parser contract in the reviewed scope. DraftCompleteDraft request/response markers emit the existing DraftCompleteEvent; payload normalization, raw evidence preservation, false-positive boundaries, router/package wiring, DraftBot/DraftHuman preservation, and schema snapshot updates match the contract.

Validation reviewed:
- python3 -m pytest -q tests/test_draft_complete_parser.py -> 39 passed
- python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py -> 76 passed
- python3 -m pytest -q tests/test_router_unit.py -> 17 passed
- python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed
- python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py -> 7 passed
- python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed
- python3 -m ruff check src tests tools -> All checks passed
- git diff --check -> passed
- new-file whitespace check -> passed
- branch-scope protected-surface gate -> forbidden 0, warnings 11, result passed
- explicit #124 protected-surface gate -> forbidden 0, warnings 2, result passed
- python3 -m pytest -q tests -> 858 passed

Remaining non-blocking gaps:
- No safe committed golden replay fixture or feature-equity corpus fixture was added, so DraftComplete corpus count remains zero until fixture coverage is added.
- tools/check_secret_patterns.py is unavailable in this worktree.
- Remote CI has not run from this local Codex E pass.

Submitter responsibilities:
- Verify exact staged scope.
- Attach/create the intended submission branch from the detached worktree state.
- Create or update the draft PR against codex/parser-reliability-intelligence.
- Do not target main.
- Do not merge, close issue #124, close tracker #47, or close related issue #11.
- Leave merge/deployment/issue closure/tracker updates for Codex G.

Stop conditions:
- Do not include unrelated local files.
- Do not change DraftBot or DraftHuman behavior.
- Do not create a new event class or change DraftCompleteEvent.kind.
- Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or environment variable contracts.
- Do not commit raw private Player.log excerpts.
- Do not build draft coaching, ratings, AI advice, deck construction analytics, hidden-card inference, archetype classification, gameplay advice, or AI/analytics truth.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/124"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_draft_complete.md"
  target_artifact: "docs/contract_test_reports/parser_draft_complete.md"
  verdict: "No blocking findings. Ready for Codex F."
  branch: "codex/parser-reliability-intelligence"
  worktree: "/Users/<redacted>/Documents/New project/Mythic-Edge-issue-124"
  risk_tier: "High"
  validation:
    - "python3 -m pytest -q tests/test_draft_complete_parser.py -> 39 passed"
    - "python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py -> 76 passed"
    - "python3 -m pytest -q tests/test_router_unit.py -> 17 passed"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed"
    - "python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py -> 7 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed"
    - "python3 -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed"
    - "new-file whitespace check -> passed"
    - "branch-scope protected-surface gate -> forbidden 0, warnings 11, result passed"
    - "explicit #124 protected-surface gate -> forbidden 0, warnings 2, result passed"
    - "python3 -m pytest -q tests -> 858 passed"
  remaining_gaps:
    - "No golden replay fixture or feature-equity corpus baseline update was added; DraftComplete corpus count remains zero until safe fixture coverage is added."
    - "tools/check_secret_patterns.py is unavailable in this worktree."
    - "Remote CI has not run from this local Codex E pass."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not include unrelated local files."
    - "Do not change DraftBot or DraftHuman behavior."
    - "Do not create a new event class or change DraftCompleteEvent.kind."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or environment variable contracts."
    - "Do not commit raw private Player.log excerpts."
    - "Do not build draft coaching, ratings, AI advice, deck construction analytics, hidden-card inference, archetype classification, gameplay advice, or AI/analytics truth."
```
