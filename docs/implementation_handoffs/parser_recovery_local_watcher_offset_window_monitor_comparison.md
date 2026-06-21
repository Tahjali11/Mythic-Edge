# Implementation Handoff: Parser Recovery Local Watcher Offset-Window Monitor

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/452

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

## Contract

`docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`

## Role Performed

Codex C: Module Implementer.

## Comparison Summary

Confirmed before editing:

- Issue #452 is scoped to synthetic/temp-file metadata helper behavior.
- Pipeline tracker #388 remains inactive for this issue.
- Parent private-evidence issue #434 remains open.
- Previous PR #538 is merged with merge commit
  `892843a35cfd201fc10e6c6a68549c609817dd4f`.
- The contract was present as a Codex B artifact and was copied into a clean
  issue worktree before implementation.
- No existing local watcher offset-window monitor helper existed.

Implemented:

- Added a pure, side-effect-free local watcher offset-window metadata helper.
- Added contracted object/schema constants for monitor report, source
  selection, offset windows, and update-buffer summaries.
- Added source selection helpers that require symbolic labels and block
  non-synthetic local sources without approval before metadata collection.
- Added synthetic temp-file metadata capture that records size/generation
  metadata without returning paths or contents.
- Added source-transition classification for unchanged, appended, truncated,
  recreated, rotated, archived, deleted, and unavailable metadata states.
- Added offset-window start/finish helpers for synthetic `read_from_start`,
  `tail_from_now`, `offset_bounded`, and `metadata_only` review objects.
- Added bounded update-buffer summary helpers for OK, near-limit, over-limit,
  dropped-update, and unknown states.
- Added validators for report/source/window/buffer shape, vocabulary use,
  symbolic labels, false readiness flags, non-claims, privacy markers, and
  forbidden local/private artifact fields.
- Added focused tests for all helper paths and privacy/anti-readiness
  boundaries.

Not implemented:

- No parser behavior changes.
- No `FileTailer` calls, watcher streams, polling loops, source reading,
  offset-state writing, runtime status changes, diagnostics changes, drift
  behavior, golden replay behavior, corpus metadata edits, fixture promotion,
  recovery packets, issue drafts, workbook/webhook/App Script behavior,
  analytics, AI, coaching, CI, merge, deploy, release, or production behavior.
- No private Player.log, UTC_Log, app-data, live MTGA, network, firewall,
  packet, OS/router, diagnostics, drift, watcher, tailer, or private smoke
  evidence was read or generated.
- No #388 or #381 activation.
- No readiness or authorization flags were changed to true.

## Files Changed

- `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`
  - Codex B contract source artifact retained in the clean worktree.
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
  - New synthetic-only metadata helper and validators.
- `tests/test_local_watcher_offset_window_monitor.py`
  - New focused tests for helper behavior and protected boundaries.
- `docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md`
  - This implementation handoff.

## Public Helper Surface

```python
LOCAL_WATCHER_OFFSET_WINDOW_OBJECT
LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION
LOCAL_WATCHER_SOURCE_OBJECT
LOCAL_WATCHER_WINDOW_OBJECT
LOCAL_WATCHER_EVENT_OBJECT
describe_source_selection(...)
capture_synthetic_file_metadata(...)
classify_source_transition(...)
start_offset_window(...)
finish_offset_window(...)
summarize_update_buffer(...)
build_offset_window_monitor_report(...)
validate_offset_window_monitor_report(...)
validate_source_selection(...)
validate_offset_window(...)
validate_update_buffer_summary(...)
```

The helper is not imported by parser runtime paths.

## Tests Added

`tests/test_local_watcher_offset_window_monitor.py` covers:

- symbolic source selection and false content/path/hash flags;
- blocked non-synthetic local source behavior without approval;
- rejection of path-like source labels without echoing the value;
- synthetic temp-file metadata capture without path or content leakage;
- source transition classification for append, truncation, recreate, rotate,
  archive, delete, and unavailable states;
- synthetic read-from-start and tail-from-now offset-window ranges;
- generation-crossing and reversed-range manual review states;
- bounded update-buffer degradation states;
- false readiness flag enforcement;
- embedded local/private marker detection without echoing values.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_local_watcher_offset_window_monitor.py
# 10 passed

PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py
# 8 passed

PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
# 11 passed

python3 -m ruff check src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py tests/test_local_watcher_offset_window_monitor.py
# passed

git diff --check
# passed

python3 tools/check_agent_docs.py
# passed

printf '%s\n' docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py tests/test_local_watcher_offset_window_monitor.py docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed

printf '%s\n' docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py tests/test_local_watcher_offset_window_monitor.py docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed

printf '%s\n' docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py tests/test_local_watcher_offset_window_monitor.py docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
# selection_status: ok

python3 -m ruff check src tests tools
# passed

PYTHONPATH=src python3 -m pytest -q tests
# 1874 passed
```

Not run: Pyright advisory. The selector listed it as advisory only, and the
contract-required plus selector-required checks passed.

## Remaining Risks

- This is metadata-only helper coverage. It does not prove real watcher
  correctness, private source offset safety, parser recovery behavior, fixture
  promotion readiness, #388 activation readiness, release readiness, or
  production behavior.
- Exact offsets and file sizes are allowed only for synthetic/public-fixture
  metadata in this helper. Private/local offset handling remains deferred to a
  separately approved private-evidence workflow.
- The helper validates committed/review objects, but it is not wired into any
  runtime surface.

## Recommended Next Role

Codex E: Adversarial Reviewer.

Review focus:

- Verify the helper does not call `FileTailer`, read file contents, discover
  private paths, write offset state, or touch protected parser/runtime surfaces.
- Verify non-synthetic local sources remain blocked or review-only and never
  expose exact offsets, sizes, paths, hashes, or raw content.
- Verify false readiness and authorization flags remain false.
- Verify validation errors do not echo private/path-like supplied values.
- Verify no corpus metadata, fixture, golden replay, recovery packet, or #388
  activation behavior was introduced.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Adversarial Reviewer for issue #452.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/452

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/451

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/538

Previous merge commit:
892843a35cfd201fc10e6c6a68549c609817dd4f

Contract:
docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md

Implementation handoff:
docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md

Review goal:
Adversarially review the synthetic-only local watcher offset-window monitor
metadata helper for contract compliance, privacy safety, truth-boundary safety,
and protected-surface isolation.

Focus:
- Confirm the implementation is limited to:
  - src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py
  - tests/test_local_watcher_offset_window_monitor.py
  - docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md
  - the contract artifact if it is newly tracked in this PR
- Confirm the helper never reads source contents, tails logs, starts watcher
  streams, discovers private paths, writes offset state, or calls FileTailer.
- Confirm non-synthetic local sources are blocked or review-only and do not
  expose exact private offsets, sizes, paths, timestamps, hashes, or content.
- Confirm false flags remain false:
  - parser_behavior_ready
  - pipeline_activation_ready_for_issue_388
  - private_harvest_authorized
  - fixture_promotion_authorized
  - corpus_status_change_authorized
- Confirm no parser behavior, parser state final reconciliation, parser event
  classes, router semantics, match/game identity, deduplication, diagnostics,
  drift, runtime status, golden replay, corpus metadata, fixture promotion,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, analytics truth, AI truth, coaching behavior, CI
  gates, merge readiness, deploy readiness, release readiness, production
  behavior, or final integration policy changed.
- Confirm validation errors do not echo private/path-like values.
- Confirm no private Player.log, UTC_Log, app-data, live MTGA, network,
  firewall/drop, packet, OS/router, diagnostics, drift, watcher, tailer, or
  private smoke evidence was read or generated.

Suggested validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_local_watcher_offset_window_monitor.py
- PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py
- PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
- python3 -m ruff check src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py tests/test_local_watcher_offset_window_monitor.py
- git diff --check
- python3 tools/check_agent_docs.py
- path-scoped secret/private-marker scan
- path-scoped protected-surface gate
- path-scoped validation selector

Do not close #388, #434, or #452. Do not activate #388 or #381. Do not run
private/live checks. Do not stage or commit unless explicitly instructed.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/452"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/451"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/538"
  previous_merge_commit: "892843a35cfd201fc10e6c6a68549c609817dd4f"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md"
  target_artifact: "docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md"
  verdict: "local_watcher_offset_window_monitor_ready_for_adversarial_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_scope: "synthetic_temp_file_metadata_helper_and_tests_only"
```
