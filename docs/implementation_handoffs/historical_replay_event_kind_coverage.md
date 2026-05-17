# Historical Replay Event Kind Coverage Handoff

## Role Performed

Codex C: focused implementation pass.

## Branch

`codex/historical-replay-event-kind-coverage`

Base: `origin/codex/repo-wide-hardening-run`

## Problem

The historical replay quality report found saved JSONL records with five event
kinds that were present in the archived data but skipped by
`saved_event_replay.py`:

- `MatchConnectionState`
- `TcpConnectionClose`
- `DeckCollection`
- `WebSocketClosed`
- `ConnectionError`

These event kinds already have parser event classes, live parser modules, and
focused parser tests. The concrete gap was the replay adapter's
`EVENT_CLASS_BY_KIND` mapping, which did not rehydrate those saved records back
into typed event objects during local historical replay.

## Change Summary

Updated `src/mythic_edge_parser/app/saved_event_replay.py` so saved JSONL replay
can reconstruct the five existing event kinds listed above.

Updated `tests/test_saved_event_replay.py` to:

- include the five event kinds in the exact supported replay mapping
- prove a saved JSONL file containing those historical kinds replays five
  events with zero skips
- preserve unknown-kind behavior for unsupported `Collection`, `Inventory`,
  malformed, blank, or differently cased kinds

Updated `docs/contracts/parser_saved_event_replay.md` so the saved replay
contract reflects the current twelve supported replay event kinds.

## Truth And Boundary Notes

This change affects only local saved-event replay.

It does not:

- parse raw MTGA `Player.log` text differently
- change live router/parser behavior
- change parser state final reconciliation
- change match identity, game identity, or production deduplication
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- touch secrets, credentials, raw logs, generated data, runtime status files,
  failed posts, or workbook exports

## Validation To Run

```powershell
py -m pytest -q tests\test_saved_event_replay.py
py -m pytest -q tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_router_smoke.py tests\test_saved_event_replay.py
py -m ruff check src tests
git diff --check
```

## Remaining Questions

- Whether `Inventory` should also become replayable later.
- Whether the historical replay quality report should be re-run after this
  branch to confirm the unsupported-kind count drops for the five newly
  supported replay kinds.
- Whether future replay tooling should report unknown archived kinds by kind
  name instead of only incrementing `events_skipped`.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for the historical
replay event kind coverage branch.

Branch:
codex/historical-replay-event-kind-coverage

Review:
- docs/contracts/parser_saved_event_replay.md
- docs/implementation_handoffs/historical_replay_event_kind_coverage.md
- src/mythic_edge_parser/app/saved_event_replay.py
- tests/test_saved_event_replay.py
- tests/test_connection_parsers.py
- tests/test_collection_parser.py
- tests/test_router_smoke.py

Goal:
Verify that saved JSONL replay now reconstructs the five historical event kinds
observed in the local replay quality report:

- MatchConnectionState
- TcpConnectionClose
- DeckCollection
- WebSocketClosed
- ConnectionError

Lead with findings ordered by severity. Confirm whether the change is narrowly
scoped to saved-event replay and focused tests. Do not implement changes unless
explicitly asked.

Validation to consider:
py -m pytest -q tests\test_saved_event_replay.py
py -m pytest -q tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_router_smoke.py tests\test_saved_event_replay.py
py -m ruff check src tests
git diff --check

Do not change parser state final reconciliation, workbook schema, webhook
payload shape, Apps Script behavior, parser event classes, match identity, game
identity, production deduplication semantics, secrets, environment variables,
raw logs, generated data, runtime status files, failed posts, workbook exports,
or production behavior.
```

```yaml
workflow_handoff:
  issue: "N/A - local branch created from historical replay evidence"
  tracker: "N/A"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "historical replay quality report in ignored data/status output"
  target_artifact: "docs/implementation_handoffs/historical_replay_event_kind_coverage.md"
  risk_tier: "Medium"
  branch: "codex/historical-replay-event-kind-coverage"
  validation:
    - "py -m pytest -q tests\\test_saved_event_replay.py"
    - "py -m pytest -q tests\\test_connection_parsers.py tests\\test_collection_parser.py tests\\test_router_smoke.py tests\\test_saved_event_replay.py"
    - "py -m ruff check src tests"
    - "git diff --check"
  stop_conditions:
    - "Do not touch raw logs or generated local data."
    - "Do not change parser state final reconciliation."
    - "Do not change workbook schema, webhook payload shape, or Apps Script behavior."
    - "Do not change parser event classes without a new contract update."
```
